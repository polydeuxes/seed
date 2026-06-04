#!/usr/bin/env python3
"""Local Seed runtime CLI backed by Ollama-compatible intent classification."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import json
import sys
from dataclasses import dataclass
from datetime import datetime, timedelta
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from seed_runtime.action_plans import ActionPlanService, ActionPlanTransitionError
from seed_runtime.ansible_inventory_source import AnsibleInventoryObservationSource
from seed_runtime.context import ContextComposer
from seed_runtime.decisions import DecisionValidator
from seed_runtime.events import EventLedger, SQLiteEventLedger
from seed_runtime.facts import (
    Fact,
    FactConflict,
    FactSupport,
    StaleFactRefreshRecommendation,
    is_fact_expired,
    is_measurement_predicate,
)
from seed_runtime.execution import ToolExecutor
from seed_runtime.execution_proposals import ExecutionProposalService
from seed_runtime.handoff_plans import (
    HandoffPlanNotFoundError,
    HandoffPlanService,
    HandoffPlanStatusError,
)
from seed_runtime.ids import new_id
from seed_runtime.intent_classifier import (
    IntentDecisionModel,
    IntentPromptModelClient,
    TextIntentClassifier,
)
from seed_runtime.models import Event, Observation, ToolNeed, ToolSpec, utc_now
from seed_runtime.observation_normalizers import (
    EndpointAliasNormalizer,
    EndpointIdentityNormalizer,
    ObservationNormalizationPipeline,
)
from seed_runtime.predicate_catalog import PredicateCatalog
from seed_runtime.predicate_normalizers import PredicateNormalizer
from seed_runtime.observation_sources import (
    JsonObservationSource,
    LocalHostObservationSource,
    ObservationCollectionService,
    PrometheusObservationSource,
    diff_observations_json,
    export_observations_json,
)
from seed_runtime.observations import ObservationIngestor
from seed_runtime.registry import ToolRegistry
from seed_runtime.runtime import Runtime
from seed_runtime.serialization import to_plain
from seed_runtime.secrets import (
    SECRET_FIELD_NAMES,
    normalize_field_name,
    reject_secret_fields,
)
from seed_runtime.state import State, StateProjector
from seed_runtime.tool_needs import ToolNeedService

DEFAULT_ENDPOINT = "http://localhost:11434/api/generate"
DEFAULT_MODEL = "qwen2.5:3b"
DEFAULT_WORKSPACE = "local"
DEFAULT_SESSION = "local"


@dataclass(frozen=True)
class DevFactSeed:
    """Local development fact shorthand supplied from the seed_local CLI."""

    subject_id: str
    predicate: str
    value: Any
    source_type: str = "user"
    confidence: float = 1.0
    expires_at: datetime | None = None
    ttl_seconds: int | None = None


@dataclass(frozen=True)
class DevObservationSeed:
    """External observation supplied from the seed_local CLI."""

    subject: str
    predicate: str
    value: Any
    source_type: str = "user"
    confidence: float = 1.0
    expires_at: datetime | None = None
    ttl_seconds: int | None = None
    ingested_by: str = "scripts.seed_local --observe"


@dataclass(frozen=True)
class DevRegisteredProviderSeed:
    """Local development provider/tool registration supplied from the CLI."""

    provider_name: str


@dataclass
class LocalSeedApp:
    """Container for a locally configured Seed runtime and its event ledger."""

    runtime: Runtime
    ledger: EventLedger
    projector: StateProjector
    context_composer: ContextComposer
    model_client: IntentPromptModelClient
    workspace_id: str = DEFAULT_WORKSPACE
    session_id: str = DEFAULT_SESSION

    def run(self, text: str) -> dict[str, Any]:
        response = self.runtime.handle_user_message(
            self.workspace_id, self.session_id, text
        )
        return {
            "response": to_plain(response),
            "events": [
                to_plain(event) for event in self.ledger.list(self.workspace_id)
            ],
        }

    def create_action_plan(self, result: dict[str, Any]) -> dict[str, Any] | None:
        """Create a safe, text-only plan for the top tool recommendation, if any."""

        response = result.get("response")
        if not isinstance(response, dict) or response.get("kind") != "tool_need":
            return None

        payload = response.get("payload")
        if not isinstance(payload, dict):
            return None

        tool_need_payload = payload.get("tool_need")
        recommendations = payload.get("recommendations")
        if not isinstance(tool_need_payload, dict):
            return None
        if not isinstance(recommendations, list) or not recommendations:
            return None

        top_recommendation = recommendations[0]
        if not isinstance(top_recommendation, dict):
            return None
        top_provider = top_recommendation.get("provider")
        if not isinstance(top_provider, str) or not top_provider:
            return None

        tool_need = ToolNeed(**tool_need_payload)
        state = self.projector.project(self.workspace_id)
        ranked_recommendations = self.runtime.recommendation_ranker.rank(
            tool_need.capability,
            self.runtime.capability_catalog.recommend_for(tool_need),
            state,
        )
        full_recommendation = next(
            (
                recommendation
                for recommendation in ranked_recommendations
                if recommendation.provider == top_provider
            ),
            None,
        )
        if full_recommendation is None:
            return None

        plan = ActionPlanService(self.ledger).create_plan(
            tool_need,
            full_recommendation,
            state,
            session_id=self.session_id,
            causation_id=tool_need.requested_by_event_id,
        )
        plain_plan = to_plain(plan)
        payload["action_plan_id"] = plan.id
        result["events"] = [
            to_plain(event) for event in self.ledger.list(self.workspace_id)
        ]
        return plain_plan

    def seed_facts(self, facts: list[DevFactSeed]) -> list[Fact]:
        """Ingest local development fact shorthand through observations."""

        return seed_dev_facts(
            self.ledger,
            self.workspace_id,
            facts,
            session_id=self.session_id,
        )

    def observe(self, observations: list[DevObservationSeed]) -> list[Fact]:
        """Append external observations and derived facts into the ledger."""

        return ingest_observations(
            self.ledger,
            self.workspace_id,
            observations,
            session_id=self.session_id,
        )

    def observe_json(self, path: str | Path) -> list[Fact]:
        """Append observations from a local JSON inventory file."""

        return ingest_json_observations(
            self.ledger,
            self.workspace_id,
            path,
            session_id=self.session_id,
        )

    def seed_registered_providers(
        self, providers: list[DevRegisteredProviderSeed]
    ) -> None:
        """Append dev-only tool registration events into the ledger."""

        seed_dev_registered_providers(
            self.ledger,
            self.workspace_id,
            providers,
            session_id=self.session_id,
        )

    def raw(self, text: str) -> str:
        input_event = Event(
            id=new_id("evt"),
            kind="input.user_message",
            workspace_id=self.workspace_id,
            actor="user",
            payload={"text": text},
            session_id=self.session_id,
        )
        state = self.projector.project(self.workspace_id)
        context = self.context_composer.compose(
            self.workspace_id, self.session_id, input_event, state
        )
        return self.model_client.complete(context)


def seed_dev_facts(
    ledger: EventLedger,
    workspace_id: str,
    facts: list[DevFactSeed],
    *,
    session_id: str | None = None,
) -> list[Fact]:
    """Ingest --fact compatibility shorthand through ObservationIngestor."""

    observation_seeds = [
        DevObservationSeed(
            subject=seed.subject_id,
            predicate=seed.predicate,
            value=seed.value,
            source_type=seed.source_type,
            confidence=seed.confidence,
            expires_at=seed.expires_at,
            ttl_seconds=seed.ttl_seconds,
            ingested_by="scripts.seed_local --fact",
        )
        for seed in facts
    ]
    return ingest_observations(
        ledger, workspace_id, observation_seeds, session_id=session_id
    )


def ingest_observations(
    ledger: EventLedger,
    workspace_id: str,
    observations: list[DevObservationSeed],
    *,
    session_id: str | None = None,
) -> list[Fact]:
    """Ingest CLI observations through the canonical observation pipeline."""

    ingestor = ObservationIngestor(ledger)
    facts: list[Fact] = []
    for seed in observations:
        observed_at = utc_now()
        expires_at = seed.expires_at
        if expires_at is None and seed.ttl_seconds is not None:
            expires_at = observed_at + timedelta(seconds=seed.ttl_seconds)
        metadata: dict[str, Any] = {"ingested_by": seed.ingested_by}
        if seed.ttl_seconds is not None:
            metadata["ttl_seconds"] = seed.ttl_seconds
        observation = Observation(
            id=new_id("obs"),
            source_type=seed.source_type,
            observed_at=observed_at,
            subject=seed.subject,
            predicate=seed.predicate,
            value=seed.value,
            confidence=seed.confidence,
            metadata=metadata,
            expires_at=expires_at,
        )
        facts.append(
            ingestor.ingest(
                observation,
                workspace_id,
                actor="user" if seed.source_type == "user" else "system",
                session_id=session_id,
            )
        )
    return facts


def build_observation_normalization_pipeline(
    predicate_catalog_path: str | Path | None = None,
) -> ObservationNormalizationPipeline:
    """Build the default alias/identity/predicate normalization pipeline."""

    return ObservationNormalizationPipeline(
        [
            EndpointAliasNormalizer(),
            EndpointIdentityNormalizer(),
            PredicateNormalizer(PredicateCatalog.load(predicate_catalog_path)),
        ]
    )


def ingest_json_observations(
    ledger: EventLedger,
    workspace_id: str,
    path: str | Path,
    *,
    session_id: str | None = None,
    predicate_catalog_path: str | Path | None = None,
) -> list[Fact]:
    """Ingest observations from a local JSON file through source collection."""

    return ObservationCollectionService(
        ObservationIngestor(ledger),
        normalization_pipeline=build_observation_normalization_pipeline(
            predicate_catalog_path
        ),
    ).collect(
        JsonObservationSource(path),
        workspace_id,
        actor="system",
        session_id=session_id,
    )


def ingest_observation_source(
    ledger: EventLedger,
    workspace_id: str,
    source: Any,
    *,
    session_id: str | None = None,
    predicate_catalog_path: str | Path | None = None,
) -> list[Fact]:
    """Collect a live read-only source through ObservationCollectionService."""

    return ObservationCollectionService(
        ObservationIngestor(ledger),
        normalization_pipeline=build_observation_normalization_pipeline(
            predicate_catalog_path
        ),
    ).collect(
        source,
        workspace_id,
        actor="system",
        session_id=session_id,
    )


class FilteredObservationSource:
    """Apply CLI observation filters before ingestion."""

    def __init__(
        self,
        source: Any,
        *,
        prometheus_instance: str | None = None,
        prometheus_mountpoint: str | None = None,
    ) -> None:
        self.source = source
        self.name = getattr(source, "name", "filtered-observation-source")
        self.source_type = getattr(source, "source_type", None)
        self.prometheus_instance = prometheus_instance
        self.prometheus_mountpoint = prometheus_mountpoint

    def collect(self) -> list[Observation]:
        observations = self.source.collect()
        return [
            observation
            for observation in observations
            if _matches_prometheus_observation_filters(
                observation,
                instance=self.prometheus_instance,
                mountpoint=self.prometheus_mountpoint,
            )
        ]


def _matches_prometheus_observation_filters(
    observation: Observation,
    *,
    instance: str | None = None,
    mountpoint: str | None = None,
) -> bool:
    labels = observation.metadata.get("metric_labels")
    if not isinstance(labels, dict):
        labels = {}
    if (
        instance is not None
        and labels.get("instance", observation.subject) != instance
    ):
        return False
    if mountpoint is not None and labels.get("mountpoint") != mountpoint:
        return False
    return True


def build_prometheus_observation_source(args: argparse.Namespace) -> Any:
    source = PrometheusObservationSource(
        args.observe_prometheus, timeout_seconds=args.observe_timeout
    )
    if args.prometheus_instance is None and args.prometheus_mountpoint is None:
        return source
    return FilteredObservationSource(
        source,
        prometheus_instance=args.prometheus_instance,
        prometheus_mountpoint=args.prometheus_mountpoint,
    )


def seed_dev_registered_providers(
    ledger: EventLedger,
    workspace_id: str,
    providers: list[DevRegisteredProviderSeed],
    *,
    session_id: str | None = None,
) -> None:
    """Append dev-only registered-tool state without loading or registering tools."""

    for seed in providers:
        provider_name = seed.provider_name.strip()
        if not provider_name:
            continue
        tool = ToolSpec(
            name=provider_name,
            summary=f"Dev-only seeded provider registration for {provider_name}.",
            toolkit_id=provider_name,
            input_schema={},
            output_schema={},
            policy_action=provider_name,
            implementation="scripts.seed_local:dev_only_noop",
            risk_class="L1",
        )
        ledger.append(
            "tool.registered",
            workspace_id,
            {
                "tool": to_plain(tool),
                "source": "scripts.seed_local --registered-provider",
                "dev_only": True,
            },
            actor="system",
            session_id=session_id,
        )


def build_local_app(
    *,
    endpoint: str = DEFAULT_ENDPOINT,
    model: str = DEFAULT_MODEL,
    timeout_seconds: float = 30.0,
    workspace_id: str = DEFAULT_WORKSPACE,
    session_id: str = DEFAULT_SESSION,
    max_decision_retries: int = 1,
    database_path: str | None = None,
) -> LocalSeedApp:
    """Construct a local Seed runtime using the current intent-classifier path."""

    ledger: EventLedger = (
        SQLiteEventLedger(database_path) if database_path else EventLedger()
    )
    registry = ToolRegistry()
    registry.load_manifest(REPO_ROOT / "toolkits/core/echo/toolkit.yaml")
    projector = StateProjector(ledger)
    context_composer = ContextComposer(registry)
    model_client = IntentPromptModelClient.for_endpoint(
        endpoint,
        timeout_seconds=timeout_seconds,
        extra_payload={"model": model, "stream": False, "format": "json"},
    )
    classifier = TextIntentClassifier(model_client)
    model = IntentDecisionModel(classifier)
    runtime = Runtime(
        ledger,
        projector,
        context_composer,
        DecisionValidator(registry),
        ToolExecutor(ledger, registry, projector),
        ToolNeedService(ledger, projector),
        model,
        max_decision_retries=max_decision_retries,
    )
    return LocalSeedApp(
        runtime=runtime,
        ledger=ledger,
        projector=projector,
        context_composer=context_composer,
        model_client=model_client,
        workspace_id=workspace_id,
        session_id=session_id,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run Seed locally with Ollama /api/generate intent classification.",
        epilog=(
            "Examples:\n"
            "  python scripts/seed_local.py --fact jellyfin host node115 "
            "--fact jellyfin runtime docker 'restart jellyfin?'\n"
            "  python scripts/seed_local.py --db .seed-local.sqlite "
            "--registered-provider docker_container_lifecycle "
            "--fact jellyfin host node115 --preconditions plan_000001\n"
            "  python scripts/seed_local.py --db .seed-local.sqlite "
            "--proposal plan_000001\n"
            "  python scripts/seed_local.py --db .seed-local.sqlite "
            "--handoff plan_000001\n"
            "  python scripts/seed_local.py --db .seed-local.sqlite "
            "--authorize-proposal eprop_000001"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("message", nargs="*", help="message to send in one-shot mode")
    parser.add_argument(
        "--db",
        help=(
            "SQLite event ledger path for sharing local state across runs; "
            "use this with --plan and lifecycle commands to revisit plan IDs"
        ),
    )
    parser.add_argument(
        "--http", action="store_true", help="serve a small local HTTP API"
    )
    parser.add_argument(
        "--host", default="127.0.0.1", help="HTTP bind host when using --http"
    )
    parser.add_argument(
        "--port", type=int, default=8765, help="HTTP bind port when using --http"
    )
    parser.add_argument(
        "--events",
        action="store_true",
        help=(
            "include the full event ledger with message output; when provided "
            "without a message, list persisted event summaries and exit"
        ),
    )
    parser.add_argument(
        "--events-only",
        action="store_true",
        help="list persisted event summaries and exit",
    )
    parser.add_argument(
        "--raw",
        action="store_true",
        help="print raw model output before running the normal runtime",
    )
    parser.add_argument(
        "--raw-only",
        action="store_true",
        help="print raw model output and exit without running the runtime",
    )
    parser.add_argument(
        "--plan",
        action="store_true",
        help=(
            "when a tool need has ranked recommendations, print a safe, "
            "non-executable plan for the top recommendation"
        ),
    )
    parser.add_argument(
        "--preconditions",
        metavar="PLAN_ID",
        help=(
            "print an inspect-only execution precondition report for an "
            "action plan without executing or approving it"
        ),
    )
    parser.add_argument(
        "--proposal",
        metavar="PLAN_ID",
        help=(
            "create and print a concrete inspect-only execution proposal for an "
            "action plan when preconditions are satisfied; never executes tools"
        ),
    )
    parser.add_argument(
        "--handoff",
        metavar="PLAN_ID",
        help=(
            "create and print a non-executable provider handoff plan for an "
            "accepted action plan; never executes or approves"
        ),
    )
    parser.add_argument(
        "--authorize-proposal",
        metavar="PROPOSAL_ID",
        help=(
            "grant short-lived execution authorization for an exact concrete "
            "execution proposal; never executes tools"
        ),
    )
    parser.add_argument(
        "--authorize-execution",
        metavar="PROPOSAL_ID",
        help=argparse.SUPPRESS,
    )
    parser.add_argument(
        "--tool-name",
        metavar="TOOL",
        help=argparse.SUPPRESS,
    )
    parser.add_argument(
        "--tool-arguments-json",
        metavar="JSON",
        help=argparse.SUPPRESS,
    )
    parser.add_argument(
        "--grant-method",
        choices=[
            "interactive_prompt",
            "ssh_agent",
            "sudo_timestamp",
            "external_vault_token_ref",
        ],
        help=("optional secret-free grant metadata marker for " "--authorize-proposal"),
    )
    parser.add_argument(
        "--ttl-seconds",
        type=int,
        default=300,
        help="execution authorization time-to-live in seconds (default: 300)",
    )
    parser.add_argument(
        "--accept-plan",
        metavar="PLAN_ID",
        help="accept a previously created action plan without executing it",
    )
    parser.add_argument(
        "--approve-plan",
        metavar="PLAN_ID",
        help="approve an accepted action plan without executing it",
    )
    parser.add_argument(
        "--reject-plan",
        metavar="PLAN_ID",
        help="reject a previously created action plan without executing it",
    )
    parser.add_argument(
        "--reason",
        help="human-readable reason required by --reject-plan",
    )
    parser.add_argument(
        "--supersede-plan",
        metavar="PLAN_ID",
        help="mark a previously created action plan as superseded without executing it",
    )
    parser.add_argument(
        "--replacement-plan",
        metavar="REPLACEMENT_ID",
        help="replacement action plan id required by --supersede-plan",
    )
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Ollama model name")
    parser.add_argument(
        "--endpoint",
        default=DEFAULT_ENDPOINT,
        help="Ollama-compatible generate endpoint",
    )
    parser.add_argument(
        "--timeout", type=float, default=30.0, help="model request timeout in seconds"
    )
    parser.add_argument("--workspace", default=DEFAULT_WORKSPACE, help="workspace id")
    parser.add_argument("--session", default=DEFAULT_SESSION, help="session id")
    parser.add_argument(
        "--fact",
        action="append",
        nargs=3,
        metavar=("SUBJECT", "PREDICATE", "VALUE"),
        default=[],
        help=(
            "dev shorthand for an Observation-derived Fact before handling messages "
            "or precondition reports; repeat as --fact SUBJECT PREDICATE VALUE "
            "(for example: --fact jellyfin host node115, "
            "--fact jellyfin runtime docker)"
        ),
    )
    parser.add_argument(
        "--fact-expires-at",
        help="ISO timestamp when dev-only --fact entries should expire",
    )
    parser.add_argument(
        "--fact-ttl-seconds",
        type=int,
        help="seconds from observation time until dev-only --fact entries expire",
    )
    parser.add_argument(
        "--observe",
        action="append",
        nargs=3,
        metavar=("SUBJECT", "PREDICATE", "VALUE"),
        default=[],
        help="canonical intake: ingest an external Observation and derive a Fact",
    )
    parser.add_argument(
        "--alias",
        action="append",
        nargs=2,
        metavar=("SUBJECT", "ALIAS"),
        default=[],
        help=(
            "record SUBJECT alias ALIAS as an Observation-derived Fact; repeat to "
            "link stable hostnames to raw instance labels"
        ),
    )
    parser.add_argument(
        "--observe-json",
        metavar="PATH",
        help="ingest external Observations from a local JSON inventory file",
    )
    parser.add_argument(
        "--observe-ansible-inventory",
        metavar="PATH",
        help=(
            "read-only identity intake from a local static Ansible .ini, .yml, "
            "or .yaml inventory"
        ),
    )
    parser.add_argument(
        "--observe-local-host",
        action="store_true",
        help=(
            "read-only discovery intake for this host using Python stdlib APIs; "
            "does not execute shell commands"
        ),
    )
    parser.add_argument(
        "--observe-prometheus",
        metavar="BASE_URL",
        help=(
            "read-only Prometheus API intake from BASE_URL using only allowlisted "
            "safe metric queries"
        ),
    )
    parser.add_argument(
        "--predicate-catalog",
        metavar="PATH",
        help="load canonical predicates and provider mappings from a JSON file",
    )
    parser.add_argument(
        "--show-predicate-catalog",
        action="store_true",
        help="print canonical predicates and provider mappings, then exit",
    )
    parser.add_argument(
        "--verbose-observations",
        action="store_true",
        help="print every ingested observation-derived fact instead of a summary",
    )
    parser.add_argument(
        "--prometheus-instance",
        metavar="INSTANCE",
        help="only ingest Prometheus observations for INSTANCE",
    )
    parser.add_argument(
        "--prometheus-mountpoint",
        metavar="MOUNTPOINT",
        help="only ingest Prometheus filesystem observations for MOUNTPOINT",
    )
    parser.add_argument(
        "--observe-timeout",
        type=float,
        default=5.0,
        help="live observation source HTTP timeout in seconds (default: 5.0)",
    )
    parser.add_argument(
        "--export-observations-json",
        metavar="PATH",
        help="export projected observations/facts to a local JSON inventory file",
    )
    parser.add_argument(
        "--diff-observations-json",
        metavar="PATH",
        help=(
            "dry-run compare a local JSON observation inventory against current "
            "projected state without ingesting it"
        ),
    )
    parser.add_argument(
        "--source-type",
        choices=["user", "discovery", "provider", "imported"],
        default="user",
        help="source type for --observe entries (default: user)",
    )
    parser.add_argument(
        "--confidence",
        type=float,
        default=1.0,
        help="confidence for --observe entries from 0.0 to 1.0 (default: 1.0)",
    )
    parser.add_argument(
        "--registered-provider",
        action="append",
        metavar="PROVIDER_NAME",
        default=[],
        help=(
            "dev-only provider/tool registration state to append before "
            "precondition reports; records inspectable state only and does not "
            "load, register, approve, or execute real tools"
        ),
    )
    parser.add_argument(
        "--state-summary",
        action="store_true",
        help=(
            "print a concise read-only summary of the projected world model; "
            "does not ingest observations or execute tools"
        ),
    )
    parser.add_argument(
        "--fact-support",
        nargs=2,
        metavar=("SUBJECT", "PREDICATE"),
        help=(
            "print projected support groups for a subject/predicate; "
            "measurement predicates show only the latest current sample unless "
            "--include-history is used"
        ),
    )
    parser.add_argument(
        "--include-history",
        "--history",
        dest="include_history",
        action="store_true",
        help=(
            "include prior measurement samples in --fact-support output "
            "(durable fact output is unchanged)"
        ),
    )
    parser.add_argument(
        "--best-fact",
        nargs=2,
        metavar=("SUBJECT", "PREDICATE"),
        help="print the projected current belief for a subject/predicate",
    )
    parser.add_argument(
        "--fact-conflicts",
        action="store_true",
        help="print projected active fact conflicts and their winning values",
    )
    parser.add_argument(
        "--include-expired",
        action="store_true",
        help=(
            "include expired facts in --fact-support, --best-fact, and "
            "--fact-conflicts query output"
        ),
    )
    parser.add_argument(
        "--stale-facts",
        action="store_true",
        help="print expired facts that no longer influence projected state",
    )
    parser.add_argument(
        "--stale-fact-refreshes",
        action="store_true",
        help="print capability recommendations for refreshing expired facts",
    )
    return parser


def validate_lifecycle_args(
    args: argparse.Namespace, parser: argparse.ArgumentParser
) -> None:
    lifecycle_flags = [
        bool(args.preconditions),
        bool(args.proposal),
        bool(args.handoff),
        bool(args.authorize_proposal or args.authorize_execution),
        bool(args.accept_plan),
        bool(args.approve_plan),
        bool(args.reject_plan),
        bool(args.supersede_plan),
        bool(args.fact_support),
        bool(args.best_fact),
        bool(args.fact_conflicts),
        bool(args.stale_facts),
        bool(args.stale_fact_refreshes),
        bool(args.events_only),
    ]
    if sum(lifecycle_flags) > 1:
        parser.error(
            "choose only one of --preconditions, --proposal, --handoff, "
            "--authorize-proposal, --accept-plan, --approve-plan, "
            "--reject-plan, --supersede-plan, --fact-support, --best-fact, "
            "--fact-conflicts, --stale-facts, --stale-fact-refreshes, "
            "or --events-only"
        )
    if args.proposal and not args.db:
        parser.error("--proposal requires --db")
    if args.handoff and not args.db:
        parser.error("--handoff requires --db")
    authorization_requested = args.authorize_proposal or args.authorize_execution
    if authorization_requested and not args.db:
        parser.error("--authorize-proposal requires --db")
    if args.tool_name:
        parser.error("--tool-name is no longer accepted; authorize a proposal ID")
    if args.tool_arguments_json:
        parser.error(
            "--tool-arguments-json is no longer accepted; authorize a proposal ID"
        )
    if args.grant_method and not authorization_requested:
        parser.error("--grant-method can only be used with --authorize-proposal")
    if args.ttl_seconds != 300 and not authorization_requested:
        parser.error("--ttl-seconds can only be used with --authorize-proposal")
    if args.reject_plan and not args.reason:
        parser.error("--reject-plan requires --reason")
    if args.reason and not args.reject_plan:
        parser.error("--reason can only be used with --reject-plan")
    if args.supersede_plan and not args.replacement_plan:
        parser.error("--supersede-plan requires --replacement-plan")
    if args.replacement_plan and not args.supersede_plan:
        parser.error("--replacement-plan can only be used with --supersede-plan")
    if args.include_expired and not (
        args.fact_support or args.best_fact or args.fact_conflicts
    ):
        parser.error(
            "--include-expired can only be used with --fact-support, "
            "--best-fact, or --fact-conflicts"
        )
    if args.include_history and not args.fact_support:
        parser.error("--include-history can only be used with --fact-support")
    if args.fact_expires_at and args.fact_ttl_seconds is not None:
        parser.error("choose only one of --fact-expires-at or --fact-ttl-seconds")
    if (args.fact_expires_at or args.fact_ttl_seconds is not None) and not (
        args.fact or args.observe
    ):
        parser.error("fact expiry options require at least one --fact or --observe")
    if args.fact_ttl_seconds is not None and args.fact_ttl_seconds < 0:
        parser.error("--fact-ttl-seconds must be non-negative")
    if args.confidence < 0.0 or args.confidence > 1.0:
        parser.error("--confidence must be between 0.0 and 1.0")
    if args.observe_timeout <= 0:
        parser.error("--observe-timeout must be positive")
    if args.fact_expires_at:
        try:
            datetime.fromisoformat(args.fact_expires_at)
        except ValueError:
            parser.error("--fact-expires-at must be an ISO timestamp")


def parse_dev_fact(
    args: list[str],
    *,
    expires_at: datetime | None = None,
    ttl_seconds: int | None = None,
) -> DevFactSeed:
    subject_id, predicate, raw_value = args
    value = _parse_fact_value(raw_value)
    if normalize_field_name(predicate) in SECRET_FIELD_NAMES:
        raise ValueError(f"secret field is not allowed in --fact: {predicate}")
    reject_secret_fields(
        {"subject": subject_id, "predicate": predicate, "value": value},
        "--fact",
    )
    return DevFactSeed(
        subject_id=subject_id,
        predicate=predicate,
        value=value,
        source_type="user",
        confidence=1.0,
        expires_at=expires_at,
        ttl_seconds=ttl_seconds,
    )


def parse_observation(
    args: list[str],
    *,
    source_type: str,
    confidence: float,
    expires_at: datetime | None = None,
    ttl_seconds: int | None = None,
) -> DevObservationSeed:
    subject, predicate, raw_value = args
    value = _parse_fact_value(raw_value)
    if normalize_field_name(predicate) in SECRET_FIELD_NAMES:
        raise ValueError(f"secret field is not allowed in --observe: {predicate}")
    reject_secret_fields(
        {"subject": subject, "predicate": predicate, "value": value},
        "--observe",
    )
    return DevObservationSeed(
        subject=subject,
        predicate=predicate,
        value=value,
        source_type=source_type,
        confidence=confidence,
        expires_at=expires_at,
        ttl_seconds=ttl_seconds,
    )


def parse_alias(args: list[str]) -> DevObservationSeed:
    """Return the Observation seed represented by --alias SUBJECT ALIAS."""

    subject, alias = args
    reject_secret_fields({"subject": subject, "alias": alias}, "--alias")
    return DevObservationSeed(
        subject=subject,
        predicate="alias",
        value=alias,
        source_type="user",
        confidence=1.0,
        ingested_by="scripts.seed_local --alias",
    )


def parse_registered_provider(provider_name: str) -> DevRegisteredProviderSeed:
    return DevRegisteredProviderSeed(provider_name=provider_name)


def _parse_fact_value(value: str) -> Any:
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return value


def format_response_summary(result: dict[str, Any]) -> str:
    response = result.get("response", {})
    if not isinstance(response, dict):
        return str(response)

    message = str(response.get("message") or "").strip()
    payload = (
        response.get("payload") if isinstance(response.get("payload"), dict) else {}
    )
    output = payload.get("output")

    lines = []
    if message:
        lines.append(message)
    else:
        lines.append(str(response.get("kind") or "response"))
    if output is not None:
        lines.append("Output: " + json.dumps(output, sort_keys=True))

    recommendations = payload.get("recommendations")
    if isinstance(recommendations, list) and recommendations:
        lines.append("Recommendations:")
        formatted_recommendations = _format_recommendations(recommendations)
        if formatted_recommendations:
            lines.extend(formatted_recommendations)
    return "\n".join(lines)


def _format_recommendations(recommendations: list[Any]) -> list[str]:
    lines: list[str] = []
    for index, recommendation in enumerate(recommendations, start=1):
        if lines:
            lines.append("")
        if isinstance(recommendation, dict):
            provider = recommendation.get("provider")
            if provider is None:
                lines.append(f"{index}. {recommendation}")
                continue
            score = recommendation.get("score")
            if score is None:
                lines.append(f"{index}. {provider}")
            else:
                lines.append(f"{index}. {provider} (score={score})")
            reasons = recommendation.get("reasons")
            if not isinstance(reasons, list):
                reasons = recommendation.get("reasoning")
            if isinstance(reasons, list):
                for reason in reasons:
                    if reason is not None:
                        lines.append(f"   - {reason}")
        elif recommendation is not None:
            lines.append(f"{index}. {recommendation}")
    return lines


def format_cli_output(
    result: dict[str, Any],
    *,
    include_events: bool = False,
    raw_output: str | None = None,
    action_plan: dict[str, Any] | None = None,
) -> str:
    sections: list[str] = []
    if raw_output is not None:
        sections.extend(["Raw model output:", raw_output])
    sections.append(format_response_summary(result))
    if action_plan is not None:
        sections.append(format_action_plan(action_plan))
    if include_events:
        sections.extend(
            [
                "Events:",
                json.dumps(result.get("events", []), indent=2, sort_keys=True),
            ]
        )
    return "\n".join(sections)


def seed_dev_state_from_args(args: argparse.Namespace, ledger: EventLedger) -> None:
    """Seed dev-only facts and provider registrations requested by CLI args."""

    fact_expires_at = (
        datetime.fromisoformat(args.fact_expires_at) if args.fact_expires_at else None
    )
    fact_seeds = [
        parse_dev_fact(
            fact, expires_at=fact_expires_at, ttl_seconds=args.fact_ttl_seconds
        )
        for fact in args.fact
    ]
    if fact_seeds:
        seed_dev_facts(
            ledger,
            args.workspace,
            fact_seeds,
            session_id=args.session,
        )

    observation_seeds = [
        parse_observation(
            observation,
            source_type=args.source_type,
            confidence=args.confidence,
            expires_at=fact_expires_at,
            ttl_seconds=args.fact_ttl_seconds,
        )
        for observation in args.observe
    ]
    observation_seeds.extend(parse_alias(alias) for alias in args.alias)
    if observation_seeds:
        ingest_observations(
            ledger,
            args.workspace,
            observation_seeds,
            session_id=args.session,
        )

    if args.observe_json:
        ingest_json_observations(
            ledger,
            args.workspace,
            args.observe_json,
            session_id=args.session,
        )

    if args.observe_ansible_inventory:
        ingest_observation_source(
            ledger,
            args.workspace,
            AnsibleInventoryObservationSource(args.observe_ansible_inventory),
            session_id=args.session,
        )

    if args.observe_local_host:
        ingest_observation_source(
            ledger,
            args.workspace,
            LocalHostObservationSource(),
            session_id=args.session,
        )

    if args.observe_prometheus:
        ingest_observation_source(
            ledger,
            args.workspace,
            build_prometheus_observation_source(args),
            session_id=args.session,
        )

    provider_seeds = [
        parse_registered_provider(provider_name)
        for provider_name in args.registered_provider
    ]
    if provider_seeds:
        seed_dev_registered_providers(
            ledger,
            args.workspace,
            provider_seeds,
            session_id=args.session,
        )


def _format_fact_value(value: Any) -> str:
    if isinstance(value, str):
        return value
    return json.dumps(value, sort_keys=True)


def _format_datetime(value: Any) -> str:
    isoformat = getattr(value, "isoformat", None)
    if callable(isoformat):
        return isoformat()
    return str(value)


def list_events_from_args(args: argparse.Namespace) -> list[Event]:
    """Return persisted event ledger entries for the requested workspace."""

    ledger: EventLedger = SQLiteEventLedger(args.db) if args.db else EventLedger()
    try:
        seed_dev_state_from_args(args, ledger)
        return ledger.list_events(args.workspace)
    finally:
        close = getattr(ledger, "close", None)
        if close is not None:
            close()


def format_event_summaries(events: list[Event]) -> str:
    """Format event ledger entries as compact debug summaries."""

    if not events:
        return "no events"

    lines = [f"Events: {len(events)}"]
    for event in events:
        summary = _event_payload_summary(event)
        line = (
            f"{event.id} {event.timestamp.isoformat()} "
            f"workspace={event.workspace_id} actor={event.actor} kind={event.kind}"
        )
        if event.session_id:
            line += f" session={event.session_id}"
        if summary:
            line += f" {summary}"
        lines.append(line)
    return "\n".join(lines)


def _event_payload_summary(event: Event) -> str:
    payload = event.payload
    if event.kind in {"observation.observed", "fact.observed", "fact.inferred"}:
        data = payload.get("observation") or payload.get("fact") or payload
        subject = data.get("subject") or data.get("subject_id")
        predicate = data.get("predicate")
        if subject is not None and predicate is not None:
            return f"subject={subject} predicate={predicate}"
    if event.kind == "evidence.observed":
        data = payload.get("evidence", payload)
        evidence_id = data.get("id")
        kind = data.get("kind")
        if evidence_id is not None:
            return f"evidence_id={evidence_id} evidence_kind={kind}"
    if event.kind == "tool.registered":
        data = payload.get("tool", payload)
        tool_name = data.get("name")
        if tool_name is not None:
            return f"tool={tool_name}"
    return ""

def fact_query_state(args: argparse.Namespace) -> State:
    """Seed requested dev state and return the projected State for fact queries."""

    ledger: EventLedger = SQLiteEventLedger(args.db) if args.db else EventLedger()
    try:
        seed_dev_state_from_args(args, ledger)
        history_limit = (
            max(1, len(ledger.list_events(args.workspace)))
            if getattr(args, "include_history", False)
            else 1
        )
        return StateProjector(
            ledger, measurement_history_limit=history_limit
        ).project(args.workspace)
    finally:
        close = getattr(ledger, "close", None)
        if close is not None:
            close()


def projected_state_from_args(args: argparse.Namespace) -> State:
    """Return persisted projected State without ingesting or executing anything."""

    ledger: EventLedger = SQLiteEventLedger(args.db) if args.db else EventLedger()
    try:
        return StateProjector(ledger).project(args.workspace)
    finally:
        close = getattr(ledger, "close", None)
        if close is not None:
            close()


def state_summary(state: State, *, top_entity_limit: int = 10) -> dict[str, Any]:
    """Build a concise operator summary using only the projected State."""

    current_measurements = [
        fact
        for fact in state.facts.values()
        if is_measurement_predicate(fact.predicate) and not is_fact_expired(fact)
    ]
    durable_facts = [
        fact
        for fact in state.facts.values()
        if not is_measurement_predicate(fact.predicate)
    ]

    entity_aliases: dict[str, set[str]] = defaultdict(set)
    entity_fact_counts: Counter[str] = Counter()
    for fact in state.facts.values():
        canonical = state.alias_resolver.canonical(fact.subject_id)
        entity_aliases[canonical].update(state.alias_resolver.resolve(fact.subject_id))
        entity_fact_counts[canonical] += 1
    for entity in state.entities.values():
        canonical = state.alias_resolver.canonical(entity.name)
        entity_aliases[canonical].update({entity.name, *entity.aliases})
        entity_fact_counts.setdefault(canonical, 0)

    top_entities = [
        {
            "name": canonical,
            "aliases": sorted(entity_aliases[canonical] - {canonical}),
            "fact_count": entity_fact_counts[canonical],
        }
        for canonical in sorted(
            entity_aliases, key=lambda name: (-entity_fact_counts[name], name)
        )[:top_entity_limit]
    ]

    availability = Counter({"up": 0, "down": 0, "unknown": 0})
    for fact in current_measurements:
        if fact.predicate == "availability_status":
            status = fact.value if fact.value in availability else "unknown"
            availability[status] += 1

    filesystems: dict[tuple[str, str, str], dict[str, Any]] = defaultdict(dict)
    for fact in current_measurements:
        if fact.predicate not in {"filesystem_free_bytes", "filesystem_total_bytes"}:
            continue
        mountpoint = fact.dimensions.get("mountpoint")
        if mountpoint is None:
            continue
        canonical = state.alias_resolver.canonical(fact.subject_id)
        dimensions_key = json.dumps(
            fact.dimensions, sort_keys=True, separators=(",", ":")
        )
        key = (canonical, mountpoint, dimensions_key)
        field = "free" if fact.predicate == "filesystem_free_bytes" else "total"
        filesystems[key][field] = fact.value

    filesystem_summary = [
        {"host": host, "mountpoint": mountpoint, **values}
        for (host, mountpoint, _dimensions), values in sorted(filesystems.items())
        if "free" in values and "total" in values
    ]

    return {
        "entity_count": len(entity_aliases),
        "fact_count": len(state.facts),
        "durable_fact_count": len(durable_facts),
        "measurement_current_sample_count": len(current_measurements),
        "conflict_count": len(state.fact_conflicts),
        "stale_fact_count": len(state.get_stale_facts()),
        "observation_source_counts": dict(
            sorted(Counter(obs.source_type for obs in state.observations.values()).items())
        ),
        "top_entities": top_entities,
        "availability": dict(availability),
        "filesystems": filesystem_summary,
    }


def format_state_summary(summary: dict[str, Any]) -> str:
    """Format the projected state summary for concise terminal inspection."""

    lines = [
        "State summary",
        f"entities: {summary['entity_count']}",
        f"facts: {summary['fact_count']}",
        f"durable facts: {summary['durable_fact_count']}",
        f"measurement current samples: {summary['measurement_current_sample_count']}",
        f"conflicts: {summary['conflict_count']}",
        f"stale facts: {summary['stale_fact_count']}",
        "observation sources:",
    ]
    sources = summary["observation_source_counts"]
    lines.extend(
        [f"  {source}: {count}" for source, count in sources.items()]
        or ["  (none)"]
    )
    lines.append("top entities:")
    for entity in summary["top_entities"]:
        aliases = ", ".join(entity["aliases"]) or "none"
        lines.append(
            f"  {entity['name']} (aliases: {aliases}; facts: {entity['fact_count']})"
        )
    if not summary["top_entities"]:
        lines.append("  (none)")
    lines.extend(
        [
            "availability:",
            f"  up: {summary['availability']['up']}",
            f"  down: {summary['availability']['down']}",
            f"  unknown: {summary['availability']['unknown']}",
        ]
    )
    if summary["filesystems"]:
        lines.append("filesystems:")
        for filesystem in summary["filesystems"]:
            lines.append(
                f"  {filesystem['host']} {filesystem['mountpoint']}: "
                f"{filesystem['free']}/{filesystem['total']} bytes free/total"
            )
    return "\n".join(lines)


def diff_observations_json_from_args(args: argparse.Namespace) -> dict[str, Any]:
    """Dry-run compare a JSON observation inventory with projected state."""

    state = fact_query_state(args)
    input_path = Path(args.diff_observations_json)
    payload = json.loads(input_path.read_text(encoding="utf-8"))
    diff = diff_observations_json(state, payload)
    plain_diff = to_plain(diff)
    return {"path": str(input_path), "diff": plain_diff}


def format_observation_inventory_diff(result: dict[str, Any]) -> str:
    diff = result["diff"]
    lines = [f"observation inventory diff for {result['path']}:"]
    for category in (
        "new_facts",
        "matching_facts",
        "changed_facts",
        "expired_incoming",
        "conflicts_introduced",
    ):
        lines.append(f"{category}: {len(diff[category])}")
    lines.append(json.dumps(diff, indent=2, sort_keys=True))
    return "\n".join(lines)


def export_observations_json_from_args(args: argparse.Namespace) -> dict[str, Any]:
    """Seed requested dev state and write the projected observation inventory."""

    payload = export_observations_json(fact_query_state(args))
    output_path = Path(args.export_observations_json)
    output_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return {
        "path": str(output_path),
        "observation_count": len(payload["observations"]),
    }


def format_fact_supports(
    supports: list[FactSupport],
    subject: str,
    predicate: str,
    *,
    historical_samples_hidden: bool = False,
) -> str:
    if not supports:
        return f"no fact support for {subject} {predicate}"

    sections: list[str] = []
    for support in supports:
        sections.append(
            "\n".join(
                [
                    f"value: {_format_fact_value(support.value)}",
                    f"semantics: {support.predicate_semantics}",
                    f"support_kind: {support.support_kind}",
                    f"aggregate_confidence: {support.confidence}",
                    f"expired: {str(support.expired).lower()}",
                    f"expires_at: {_format_datetime(support.expires_at)}",
                    "supporting_fact_ids: " + ", ".join(support.supporting_fact_ids),
                    "source_types: " + ", ".join(support.source_types),
                    f"first_observed: {_format_datetime(support.observed_at)}",
                    f"latest_observed: {_format_datetime(support.latest_observed_at)}",
                ]
            )
        )
    output = "\n\n".join(sections)
    if historical_samples_hidden:
        output += "\n\nhistorical samples hidden; use --include-history"
    return output


def _fact_support_for_measurement_sample(
    state: State, fact: Fact
) -> FactSupport:
    return FactSupport(
        subject=state.alias_resolver.canonical(fact.subject_id),
        predicate=fact.predicate,
        value=fact.value,
        dimensions=dict(fact.dimensions),
        supporting_fact_ids=[fact.id],
        source_types=[fact.source_type],
        confidence=fact.confidence,
        observed_at=fact.observed_at,
        latest_observed_at=fact.observed_at,
        expired=is_fact_expired(fact),
        expires_at=fact.expires_at,
        predicate_semantics="measurement",
        support_kind="current_sample",
    )


def fact_support_query(
    state: State,
    subject: str,
    predicate: str,
    *,
    include_expired: bool = False,
    include_history: bool = False,
) -> tuple[list[FactSupport], bool]:
    if not is_measurement_predicate(predicate):
        return (
            state.get_fact_supports(
                subject, predicate, include_expired=include_expired
            ),
            False,
        )

    resolved_subjects = state.resolve_fact_subjects(subject)
    samples = [
        fact
        for fact in state.facts.values()
        if fact.predicate == predicate
        and fact.subject_id in resolved_subjects
        and (include_expired or not is_fact_expired(fact))
    ]
    samples.sort(key=lambda fact: (fact.observed_at, fact.id))

    if include_history:
        return (
            [_fact_support_for_measurement_sample(state, fact) for fact in samples],
            False,
        )

    current = state.get_fact_support(
        subject, predicate, include_expired=include_expired
    )
    if current is None:
        return [], bool(samples)
    current_ids = set(current.supporting_fact_ids)
    historical_samples_hidden = any(fact.id not in current_ids for fact in samples)
    return [current], historical_samples_hidden


def format_best_fact(
    state: State, subject: str, predicate: str, *, include_expired: bool = False
) -> str:
    best_fact = state.get_best_fact(subject, predicate, include_expired=include_expired)
    best_support = state.get_fact_support(
        subject, predicate, include_expired=include_expired
    )
    if best_fact is None or best_support is None:
        return f"no current belief for {subject} {predicate}"

    return "\n".join(
        [
            f"subject: {best_fact.subject_id}",
            f"predicate: {best_fact.predicate}",
            f"value: {_format_fact_value(best_support.value)}",
            f"semantics: {best_support.predicate_semantics}",
            f"support_kind: {best_support.support_kind}",
            f"confidence: {best_support.confidence}",
            f"expired: {str(is_fact_expired(best_fact)).lower()}",
            f"expires_at: {_format_datetime(best_fact.expires_at)}",
            (
                "reason: latest current measurement"
                if best_support.predicate_semantics == "measurement"
                else "reason: best-supported current belief"
            ),
            f"support_count: {len(best_support.supporting_fact_ids)}",
        ]
    )


def _format_fact_expiry_statuses(fact_ids: list[str], facts: dict[str, Fact]) -> str:
    statuses: list[str] = []
    for fact_id in fact_ids:
        fact = facts.get(fact_id)
        if fact is None:
            continue
        statuses.append(
            f"{fact_id} (expired: {str(is_fact_expired(fact)).lower()}, "
            f"expires_at: {_format_datetime(fact.expires_at)})"
        )
    return ", ".join(statuses)


def format_fact_conflicts(conflicts: list[FactConflict], facts: dict[str, Fact]) -> str:
    if not conflicts:
        return "no active fact conflicts"

    sections: list[str] = []
    for conflict in conflicts:
        best_fact = facts.get(conflict.best_fact_id) if conflict.best_fact_id else None
        winning_value = conflict.winning_value
        if winning_value is None and best_fact is not None:
            winning_value = best_fact.value
        sections.append(
            "\n".join(
                [
                    f"subject: {conflict.subject}",
                    f"predicate: {conflict.predicate}",
                    "values: "
                    + ", ".join(_format_fact_value(value) for value in conflict.values),
                    f"winning_value: {_format_fact_value(winning_value)}",
                    f"winning_fact_id: {conflict.best_fact_id}",
                    "conflicting_fact_ids: " + ", ".join(conflict.conflicting_fact_ids),
                    "winning_fact_status: "
                    + _format_fact_expiry_statuses(
                        [conflict.best_fact_id] if conflict.best_fact_id else [], facts
                    ),
                    "conflicting_fact_statuses: "
                    + _format_fact_expiry_statuses(
                        conflict.conflicting_fact_ids, facts
                    ),
                    f"reason: {conflict.reason}",
                ]
            )
        )
    return "\n\n".join(sections)


def format_observed_facts(facts: list[Fact]) -> str:
    if not facts:
        return "ingested 0 observation(s)\nno observations ingested"

    sections: list[str] = [f"ingested {len(facts)} observation(s)"]
    for fact in facts:
        sections.append(
            "\n".join(
                [
                    f"fact_id: {fact.id}",
                    f"subject: {fact.subject_id}",
                    f"predicate: {fact.predicate}",
                    f"value: {_format_fact_value(fact.value)}",
                    f"source_type: {fact.source_type}",
                    f"confidence: {fact.confidence}",
                    f"observed_at: {_format_datetime(fact.observed_at)}",
                    "evidence_ids: " + ", ".join(fact.evidence_ids),
                ]
            )
        )
    return "\n\n".join(sections)


def format_observed_fact_summary(facts: list[Fact]) -> str:
    if not facts:
        return (
            "ingested 0 observation(s)\n"
            "hosts/instances discovered: none\n"
            "counts by predicate: none"
        )

    hosts = sorted({fact.subject_id for fact in facts})
    predicate_counts: dict[str, int] = {}
    for fact in facts:
        predicate_counts[fact.predicate] = (
            predicate_counts.get(fact.predicate, 0) + 1
        )

    sections = [
        f"ingested {len(facts)} observation(s)",
        "hosts/instances discovered: " + ", ".join(hosts),
        "counts by predicate:",
    ]
    sections.extend(
        f"- {predicate}: {predicate_counts[predicate]}"
        for predicate in sorted(predicate_counts)
    )
    return "\n".join(sections)


def ingest_observations_from_args(args: argparse.Namespace) -> list[Fact]:
    ledger: EventLedger = SQLiteEventLedger(args.db) if args.db else EventLedger()
    try:
        fact_expires_at = (
            datetime.fromisoformat(args.fact_expires_at)
            if args.fact_expires_at
            else None
        )
        fact_seeds = [
            parse_dev_fact(
                fact, expires_at=fact_expires_at, ttl_seconds=args.fact_ttl_seconds
            )
            for fact in args.fact
        ]
        observation_seeds = [
            parse_observation(
                observation,
                source_type=args.source_type,
                confidence=args.confidence,
                expires_at=fact_expires_at,
                ttl_seconds=args.fact_ttl_seconds,
            )
            for observation in args.observe
        ]
        observation_seeds.extend(parse_alias(alias) for alias in args.alias)
        facts = seed_dev_facts(
            ledger, args.workspace, fact_seeds, session_id=args.session
        )
        facts.extend(
            ingest_observations(
                ledger,
                args.workspace,
                observation_seeds,
                session_id=args.session,
            )
        )
        if args.observe_json:
            facts.extend(
                ingest_json_observations(
                    ledger,
                    args.workspace,
                    args.observe_json,
                    session_id=args.session,
                    predicate_catalog_path=args.predicate_catalog,
                )
            )
        if args.observe_ansible_inventory:
            facts.extend(
                ingest_observation_source(
                    ledger,
                    args.workspace,
                    AnsibleInventoryObservationSource(args.observe_ansible_inventory),
                    session_id=args.session,
                    predicate_catalog_path=args.predicate_catalog,
                )
            )
        if args.observe_local_host:
            facts.extend(
                ingest_observation_source(
                    ledger,
                    args.workspace,
                    LocalHostObservationSource(),
                    session_id=args.session,
                    predicate_catalog_path=args.predicate_catalog,
                )
            )
        if args.observe_prometheus:
            facts.extend(
                ingest_observation_source(
                    ledger,
                    args.workspace,
                    build_prometheus_observation_source(args),
                    session_id=args.session,
                    predicate_catalog_path=args.predicate_catalog,
                )
            )
        return facts
    finally:
        close = getattr(ledger, "close", None)
        if close is not None:
            close()


def format_stale_facts(facts: list[Fact]) -> str:
    if not facts:
        return "no stale facts"

    sections: list[str] = []
    for fact in facts:
        sections.append(
            "\n".join(
                [
                    f"subject: {fact.subject_id}",
                    f"predicate: {fact.predicate}",
                    f"value: {_format_fact_value(fact.value)}",
                    f"source_type: {fact.source_type}",
                    f"confidence: {fact.confidence}",
                    f"expired: {str(is_fact_expired(fact)).lower()}",
                    f"expires_at: {_format_datetime(fact.expires_at)}",
                ]
            )
        )
    return "\n\n".join(sections)


def format_stale_fact_refresh_recommendations(
    recommendations: list[StaleFactRefreshRecommendation],
) -> str:
    if not recommendations:
        return "no stale fact refresh recommendations"

    sections: list[str] = []
    for recommendation in recommendations:
        sections.append(
            "\n".join(
                [
                    f"fact_id: {recommendation.fact_id}",
                    f"subject: {recommendation.subject}",
                    f"predicate: {recommendation.predicate}",
                    f"value: {_format_fact_value(recommendation.value)}",
                    f"recommended_capability: {recommendation.recommended_capability}",
                    f"reason: {recommendation.reason}",
                ]
            )
        )
    return "\n\n".join(sections)


def precondition_report(args: argparse.Namespace) -> dict[str, Any]:
    """Return an inspect-only precondition report for a stored action plan."""

    ledger: EventLedger = SQLiteEventLedger(args.db) if args.db else EventLedger()
    try:
        seed_dev_state_from_args(args, ledger)
        state = StateProjector(ledger).project(args.workspace)
        plan = state.action_plans.get(args.preconditions)
        if plan is None:
            raise ValueError(
                f"action plan not found in workspace {args.workspace!r}: "
                f"{args.preconditions}"
            )
        report = ActionPlanService(ledger).precondition_report(plan, state)
        return to_plain(report)
    finally:
        close = getattr(ledger, "close", None)
        if close is not None:
            close()


def execution_proposal(args: argparse.Namespace) -> dict[str, Any]:
    """Create an inspect-only execution proposal for a stored action plan."""

    ledger: EventLedger = SQLiteEventLedger(args.db) if args.db else EventLedger()
    try:
        seed_dev_state_from_args(args, ledger)
        state = StateProjector(ledger).project(args.workspace)
        plan = state.action_plans.get(args.proposal)
        if plan is None:
            return {
                "proposal_failure": {
                    "action_plan_id": args.proposal,
                    "missing_reason": "plan not found",
                    "detail": (
                        f"action plan not found in workspace {args.workspace!r}: "
                        f"{args.proposal}"
                    ),
                }
            }

        report = ActionPlanService(ledger).precondition_report(plan, state)
        if not report.plan_ready:
            failure = ExecutionProposalService().diagnose_failure(plan, state)
            report_payload = to_plain(report)
            if failure is not None:
                report_payload["missing_reason"] = failure.missing_reason
                report_payload["missing_detail"] = failure.detail
            return {"precondition_report": report_payload}

        proposal_service = ExecutionProposalService(ledger)
        proposal = proposal_service.create_proposal(
            plan,
            state,
            session_id=args.session,
            causation_id=plan.id,
        )
        if proposal is None:
            failure = proposal_service.diagnose_failure(plan, state)
            if failure is None:
                failure_payload = {
                    "action_plan_id": plan.id,
                    "missing_reason": "proposal builder returned None",
                    "detail": (
                        "execution proposal could not be generated for action plan: "
                        f"{plan.id}"
                    ),
                }
            else:
                failure_payload = to_plain(failure)
            return {"proposal_failure": failure_payload}
        return {"execution_proposal": to_plain(proposal)}
    finally:
        close = getattr(ledger, "close", None)
        if close is not None:
            close()


def handoff_plan(args: argparse.Namespace) -> dict[str, Any]:
    """Create a non-executable handoff plan for an accepted action plan."""

    ledger: EventLedger = SQLiteEventLedger(args.db)
    try:
        seed_dev_state_from_args(args, ledger)
        state = StateProjector(ledger).project(args.workspace)
        service = HandoffPlanService(ledger)
        try:
            plan = service.create_handoff_plan(
                state,
                args.handoff,
                session_id=args.session,
                causation_id=args.handoff,
            )
        except HandoffPlanNotFoundError as exc:
            return {
                "handoff_failure": {
                    "action_plan_id": args.handoff,
                    "missing_reason": "plan not found",
                    "detail": str(exc),
                }
            }
        except HandoffPlanStatusError as exc:
            return {
                "handoff_failure": {
                    "action_plan_id": args.handoff,
                    "missing_reason": "plan not accepted",
                    "detail": str(exc),
                }
            }
        return {"handoff_plan": to_plain(plan)}
    finally:
        close = getattr(ledger, "close", None)
        if close is not None:
            close()


def format_handoff_plan(result: dict[str, Any]) -> str:
    failure = result.get("handoff_failure")
    if isinstance(failure, dict):
        return format_proposal_failure(failure)

    plan = result.get("handoff_plan")
    if not isinstance(plan, dict):
        raise ValueError("handoff plan result is missing")
    return "\n".join(
        [
            f"handoff_plan_id: {plan.get('id')}",
            f"action_plan_id: {plan.get('action_plan_id')}",
            f"provider: {plan.get('provider')}",
            f"backend_type: {plan.get('backend_type')}",
            f"operation: {plan.get('operation')}",
            f"target: {plan.get('target')}",
            f"policy_summary: {plan.get('policy_summary')}",
            f"secret_boundary: {plan.get('secret_boundary')}",
        ]
    )


def grant_execution_authorization(args: argparse.Namespace) -> dict[str, Any]:
    """Grant JIT execution authorization for an exact proposal without executing."""

    ledger: EventLedger = SQLiteEventLedger(args.db)
    try:
        proposal_id = args.authorize_proposal or args.authorize_execution
        grant_metadata: dict[str, Any] = {}
        if args.grant_method == "interactive_prompt":
            grant_metadata["interactive_prompt"] = True
        elif args.grant_method == "ssh_agent":
            grant_metadata["ssh_agent"] = "SSH_AUTH_SOCK"
        elif args.grant_method == "sudo_timestamp":
            grant_metadata["sudo_timestamp"] = "sudo_timestamp"
        elif args.grant_method == "external_vault_token_ref":
            grant_metadata["external_vault_token_ref"] = (
                f"external_vault_token_ref:{proposal_id}"
            )

        authorization = ActionPlanService(ledger).grant_execution_authorization(
            args.workspace,
            proposal_id,
            granted_by="seed_local_cli",
            session_id=args.session,
            ttl_seconds=args.ttl_seconds,
            **grant_metadata,
        )
        return to_plain(authorization)
    finally:
        close = getattr(ledger, "close", None)
        if close is not None:
            close()


def format_execution_authorization(authorization: dict[str, Any]) -> str:
    return "\n".join(
        [
            f"execution_authorization_id: {authorization.get('id')}",
            f"execution_proposal_id: {authorization.get('execution_proposal_id')}",
            f"action_plan_id: {authorization.get('action_plan_id')}",
            f"tool_name: {authorization.get('tool_name')}",
            f"arguments_fingerprint: {authorization.get('arguments_fingerprint')}",
            f"expires_at: {authorization.get('expires_at')}",
            "secret_seen_by_seed: false",
        ]
    )


def format_execution_proposal(result: dict[str, Any]) -> str:
    failure = result.get("proposal_failure")
    if isinstance(failure, dict):
        return format_proposal_failure(failure)

    report = result.get("precondition_report")
    if isinstance(report, dict):
        return format_missing_preconditions(report)

    proposal = result.get("execution_proposal")
    if not isinstance(proposal, dict):
        raise ValueError("execution proposal result is missing")

    return "\n".join(
        [
            f"execution_proposal_id: {proposal.get('id')}",
            f"action_plan_id: {proposal.get('action_plan_id')}",
            f"provider: {proposal.get('provider')}",
            f"tool_name: {proposal.get('tool_name')}",
            "tool_arguments: "
            + json.dumps(proposal.get("tool_arguments", {}), sort_keys=True),
            f"arguments_fingerprint: {proposal.get('arguments_fingerprint')}",
            f"authorized: {str(bool(proposal.get('authorized'))).lower()}",
            f"executable: {str(bool(proposal.get('executable'))).lower()}",
        ]
    )


def format_proposal_failure(failure: dict[str, Any]) -> str:
    lines = [
        f"action_plan_id: {failure.get('action_plan_id')}",
        f"missing_reason: {failure.get('missing_reason')}",
    ]
    detail = failure.get("detail")
    if detail:
        lines.append(f"detail: {detail}")
    return "\n".join(lines)


def format_missing_preconditions(report: dict[str, Any]) -> str:
    lines = [
        f"action_plan_id: {report.get('action_plan_id')}",
        f"missing_reason: {report.get('missing_reason', 'preconditions missing')}",
        f"plan_ready: {str(bool(report.get('plan_ready'))).lower()}",
        f"proposal_authorized: {str(bool(report.get('proposal_authorized'))).lower()}",
        f"executable: {str(bool(report.get('executable'))).lower()}",
        "missing:",
    ]
    missing_preconditions = report.get("missing_preconditions")
    if isinstance(missing_preconditions, list) and missing_preconditions:
        for precondition in missing_preconditions:
            if isinstance(precondition, dict):
                lines.append(f"- {precondition.get('id')}")
            else:
                lines.append(f"- {precondition}")
    else:
        lines.append("- none")
    return "\n".join(lines)


def format_precondition_report(report: dict[str, Any]) -> str:
    lines = [
        f"action_plan_id: {report.get('action_plan_id')}",
        f"plan_ready: {str(bool(report.get('plan_ready'))).lower()}",
        f"proposal_authorized: {str(bool(report.get('proposal_authorized'))).lower()}",
        f"executable: {str(bool(report.get('executable'))).lower()}",
        "missing:",
    ]

    missing_preconditions = report.get("missing_preconditions")
    if isinstance(missing_preconditions, list) and missing_preconditions:
        for precondition in missing_preconditions:
            if isinstance(precondition, dict):
                lines.append(f"- {precondition.get('id')}")
            else:
                lines.append(f"- {precondition}")
    else:
        lines.append("- none")

    lines.append("preconditions:")
    preconditions = report.get("preconditions")
    if isinstance(preconditions, list) and preconditions:
        for precondition in preconditions:
            if isinstance(precondition, dict):
                lines.extend(
                    [
                        f"- id: {precondition.get('id')}",
                        "  satisfied: "
                        f"{str(bool(precondition.get('satisfied'))).lower()}",
                        f"  reason: {precondition.get('reason')}",
                    ]
                )
            else:
                lines.append(f"- {precondition}")
    else:
        lines.append("- none")
    return "\n".join(lines)


def format_action_plan_status(plan: dict[str, Any]) -> str:
    lines = [
        f"action_plan_id: {plan.get('id')}",
        f"status: {plan.get('status')}",
    ]
    error = plan.get("error")
    if error:
        lines.append(f"error: {error}")
    rejection_reason = plan.get("rejection_reason")
    if rejection_reason:
        lines.append(f"rejection_reason: {rejection_reason}")
    if plan.get("approved") is True:
        lines.append("approved: true")
    replacement_plan_id = plan.get("replacement_plan_id")
    if replacement_plan_id:
        lines.append(f"replacement_plan_id: {replacement_plan_id}")
    return "\n".join(lines)


def update_action_plan_lifecycle(args: argparse.Namespace) -> dict[str, Any] | None:
    plan_id = (
        args.accept_plan or args.approve_plan or args.reject_plan or args.supersede_plan
    )
    if not plan_id:
        return None

    ledger: EventLedger = SQLiteEventLedger(args.db) if args.db else EventLedger()
    service = ActionPlanService(ledger)
    try:
        try:
            if args.accept_plan:
                plan = service.accept_plan(
                    args.workspace, args.accept_plan, session_id=args.session
                )
            elif args.approve_plan:
                plan = service.approve_plan(
                    args.workspace, args.approve_plan, session_id=args.session
                )
                approved_plan = to_plain(plan)
                approved_plan["approved"] = True
                return approved_plan
            elif args.reject_plan:
                plan = service.reject_plan(
                    args.workspace,
                    args.reject_plan,
                    args.reason,
                    session_id=args.session,
                )
            else:
                plan = service.supersede_plan(
                    args.workspace,
                    args.supersede_plan,
                    args.replacement_plan,
                    session_id=args.session,
                )
        except ActionPlanTransitionError:
            return _format_transition_error_plan(args, ledger, plan_id)
        return to_plain(plan)
    finally:
        close = getattr(ledger, "close", None)
        if close is not None:
            close()


def _format_transition_error_plan(
    args: argparse.Namespace, ledger: EventLedger, plan_id: str
) -> dict[str, Any]:
    state = StateProjector(ledger).project(args.workspace)
    plan = state.action_plans.get(plan_id)
    status = plan.status if plan is not None else "unknown"
    target_status = _lifecycle_target_status(args)
    return {
        "id": plan_id,
        "status": status,
        "error": f"invalid transition {status} -> {target_status}",
    }


def _lifecycle_target_status(args: argparse.Namespace) -> str:
    if args.accept_plan:
        return "accepted"
    if args.approve_plan:
        return "approved"
    if args.reject_plan:
        return "rejected"
    return "superseded"


def format_action_plan(plan: dict[str, Any]) -> str:
    lines = ["Plan:"]
    summary = str(plan.get("summary") or "").strip()
    if summary:
        lines.append(summary)
    plan_id = str(plan.get("id") or "").strip()
    if plan_id:
        lines.append(f"action_plan_id: {plan_id}")
    steps = plan.get("steps")
    if isinstance(steps, list):
        for step in steps:
            if step is not None:
                lines.append(f"- {step}")
    return "\n".join(lines)


def run_http(app: LocalSeedApp, host: str, port: int) -> None:
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:  # noqa: N802 - stdlib handler API
            if self.path != "/health":
                self._write_json(404, {"error": "not found"})
                return
            self._write_json(200, {"ok": True})

        def do_POST(self) -> None:  # noqa: N802 - stdlib handler API
            if self.path not in {"/", "/message"}:
                self._write_json(404, {"error": "not found"})
                return
            try:
                payload = self._read_json()
                reject_secret_fields(payload, "http_request")
                text = payload.get("message", payload.get("text"))
                if not isinstance(text, str) or not text.strip():
                    raise ValueError("POST JSON requires non-empty 'message' or 'text'")
                result = app.raw(text) if payload.get("raw") else app.run(text)
                if isinstance(result, str):
                    self._write_json(200, {"response": result, "events": []})
                else:
                    self._write_json(200, result)
            except Exception as exc:  # keep local dev server dependency-light
                self._write_json(500, {"error": str(exc)})

        def log_message(self, format: str, *args: object) -> None:
            return

        def _read_json(self) -> dict[str, Any]:
            length = int(self.headers.get("Content-Length", "0"))
            body = self.rfile.read(length).decode("utf-8") if length else "{}"
            data = json.loads(body)
            if not isinstance(data, dict):
                raise ValueError("request body must be a JSON object")
            return data

        def _write_json(self, status: int, payload: dict[str, Any]) -> None:
            body = json.dumps(payload, indent=2, sort_keys=True).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

    server = ThreadingHTTPServer((host, port), Handler)
    print(f"Seed local HTTP server listening on http://{host}:{port}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping Seed local HTTP server.", file=sys.stderr)
    finally:
        server.server_close()


def run_shell(
    app: LocalSeedApp,
    *,
    raw: bool = False,
    raw_only: bool = False,
    events: bool = False,
    plan: bool = False,
) -> None:
    print("Seed local shell. Press Ctrl-D or type 'exit' to quit.", file=sys.stderr)
    while True:
        try:
            text = input("seed> ").strip()
        except EOFError:
            print(file=sys.stderr)
            return
        if text in {"exit", "quit"}:
            return
        if not text:
            continue
        if raw_only:
            print(app.raw(text))
            continue
        raw_output = app.raw(text) if raw else None
        result = app.run(text)
        action_plan = app.create_action_plan(result) if plan else None
        print(
            format_cli_output(
                result,
                include_events=events,
                raw_output=raw_output,
                action_plan=action_plan,
            )
        )


def format_predicate_catalog(catalog: PredicateCatalog) -> str:
    """Format canonical predicates and raw-provider mappings for debugging."""

    lines = ["canonical predicates:"]
    for predicate in catalog.list_predicates():
        allowed = (
            " [" + ", ".join(str(value) for value in predicate.allowed_values) + "]"
            if predicate.allowed_values
            else ""
        )
        lines.append(
            f"- {predicate.predicate}: {predicate.kind}/{predicate.value_type}{allowed}"
        )
    lines.append("mappings:")
    for mapping in catalog.list_mappings():
        source = mapping.source_name or "*"
        lines.append(
            f"- {source}:{mapping.predicate} -> {mapping.canonical_predicate}"
        )
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    validate_lifecycle_args(args, parser)
    if args.show_predicate_catalog:
        print(format_predicate_catalog(PredicateCatalog.load(args.predicate_catalog)))
        return 0

    if args.state_summary:
        print(format_state_summary(state_summary(projected_state_from_args(args))))
        return 0

    if args.preconditions:
        print(format_precondition_report(precondition_report(args)))
        return 0

    if args.proposal:
        result = execution_proposal(args)
        output = format_execution_proposal(result)
        if "proposal_failure" in result:
            print(output, file=sys.stderr)
            return 1
        print(output)
        return 0

    if args.handoff:
        result = handoff_plan(args)
        output = format_handoff_plan(result)
        if "handoff_failure" in result:
            print(output, file=sys.stderr)
            return 1
        print(output)
        return 0

    if args.authorize_proposal or args.authorize_execution:
        print(format_execution_authorization(grant_execution_authorization(args)))
        return 0

    updated_plan = update_action_plan_lifecycle(args)
    if updated_plan is not None:
        print(format_action_plan_status(updated_plan))
        return 0

    if args.fact_support:
        subject, predicate = args.fact_support
        state = fact_query_state(args)
        supports, historical_samples_hidden = fact_support_query(
            state,
            subject,
            predicate,
            include_expired=args.include_expired,
            include_history=args.include_history,
        )
        print(
            format_fact_supports(
                supports,
                subject,
                predicate,
                historical_samples_hidden=historical_samples_hidden,
            )
        )
        return 0

    if args.best_fact:
        subject, predicate = args.best_fact
        state = fact_query_state(args)
        print(
            format_best_fact(
                state, subject, predicate, include_expired=args.include_expired
            )
        )
        return 0

    if args.fact_conflicts:
        state = fact_query_state(args)
        print(
            format_fact_conflicts(
                state.get_fact_conflicts(include_expired=args.include_expired),
                state.facts,
            )
        )
        return 0

    if args.stale_facts:
        state = fact_query_state(args)
        print(format_stale_facts(state.get_stale_facts()))
        return 0

    if args.stale_fact_refreshes:
        state = fact_query_state(args)
        print(
            format_stale_fact_refresh_recommendations(
                state.get_stale_fact_refresh_recommendations()
            )
        )
        return 0

    if args.diff_observations_json:
        print(format_observation_inventory_diff(diff_observations_json_from_args(args)))
        return 0

    if args.export_observations_json:
        result = export_observations_json_from_args(args)
        print(
            f"exported {result['observation_count']} observation(s) to {result['path']}"
        )
        return 0

    message = " ".join(args.message).strip()
    if args.events_only or (args.events and not message and not args.http):
        print(format_event_summaries(list_events_from_args(args)))
        return 0

    if (
        args.observe
        or args.fact
        or args.alias
        or args.observe_json
        or args.observe_ansible_inventory
        or args.observe_local_host
        or args.observe_prometheus
    ) and not message and not args.http:
        observed_facts = ingest_observations_from_args(args)
        if args.observe_prometheus and not args.verbose_observations:
            print(format_observed_fact_summary(observed_facts))
        else:
            print(format_observed_facts(observed_facts))
        return 0

    app = build_local_app(
        endpoint=args.endpoint,
        model=args.model,
        timeout_seconds=args.timeout,
        workspace_id=args.workspace,
        session_id=args.session,
        database_path=args.db,
    )
    seed_dev_state_from_args(args, app.ledger)

    if args.http:
        run_http(app, args.host, args.port)
        return 0

    message = " ".join(args.message).strip()
    if message:
        if args.raw_only:
            print(app.raw(message))
            return 0
        raw_output = app.raw(message) if args.raw else None
        result = app.run(message)
        action_plan = app.create_action_plan(result) if args.plan else None
        print(
            format_cli_output(
                result,
                include_events=args.events,
                raw_output=raw_output,
                action_plan=action_plan,
            )
        )
        return 0

    run_shell(
        app, raw=args.raw, raw_only=args.raw_only, events=args.events, plan=args.plan
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
