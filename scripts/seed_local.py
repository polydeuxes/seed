#!/usr/bin/env python3
"""Local Seed runtime CLI backed by Ollama-compatible intent classification."""

from __future__ import annotations

import argparse
import ipaddress
from collections import Counter, defaultdict
import json
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Literal

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from seed_runtime.action_plans import ActionPlanService, ActionPlanTransitionError
from seed_runtime.architecture_conformance_audit import (
    architecture_conformance_audit_json,
    build_architecture_conformance_audit,
    format_architecture_conformance_audit,
)
from seed_runtime.audit_snapshots import (
    compare_audit_snapshots,
    create_audit_snapshot,
    format_audit_compare,
    format_audit_snapshots,
    list_audit_snapshots,
)
from seed_runtime.ansible_inventory_source import AnsibleInventoryObservationSource
from seed_runtime.candidate_requests import (
    inspect_candidate_requests,
    inspect_candidate_routes,
)
from seed_runtime.capability_candidates import build_capability_candidates
from seed_runtime.capability_inventory import (
    CapabilityInventoryEntry,
    build_capability_inventory,
)
from seed_runtime.capability_needs import (
    build_capability_needs,
    capability_needs_json,
    format_capability_needs,
)
from seed_runtime.container_ownership_authority import (
    CONSTRAINED_AUTHORITY_PROFILE,
    container_ownership_authority_json,
    evaluate_container_ownership_authority_slice,
    format_container_ownership_authority,
)
from seed_runtime.service_ownership_authority import (
    service_ownership_authority_json,
    evaluate_service_ownership_authority_slice,
    format_service_ownership_authority,
)
from seed_runtime.listener_endpoint_authority import (
    CONSTRAINED_AUTHORITY_PROFILE as LISTENER_ENDPOINT_AUTHORITY_PROFILE,
    listener_endpoint_authority_json,
    evaluate_listener_endpoint_authority_slice,
    format_listener_endpoint_authority,
)
from seed_runtime.capability_relationship import (
    build_capability_relationship,
    capability_relationship_json,
    format_capability_relationship,
)
from seed_runtime.capability_promotion_readiness import (
    build_capability_promotion_readiness_inspection,
)
from seed_runtime.capability_verification import (
    build_capability_verification_inspection,
)
from seed_runtime.verification_evidence import build_verification_evidence
from seed_runtime.context import DecisionInputComposer
from seed_runtime.context_views import (
    DecisionContextView,
    build_decision_context_view,
)
from seed_runtime.classification_coverage import (
    build_classification_coverage_diagnostic,
    format_classification_coverage,
)
from seed_runtime.confidence import (
    FactConfidence,
    build_confidence_summary,
    build_fact_confidences,
    find_fact_confidence,
)
from seed_runtime.consumer_dependency_audit import (
    build_consumer_audit,
    consumer_audit_json,
    format_consumer_audit,
)
from seed_runtime.component_audit import (
    build_component_audit,
    component_audit_json,
    format_component_audit,
)
from seed_runtime.emitter_consumer_audit import (
    build_emitter_consumer_audit,
    emitter_consumer_audit_json,
    format_emitter_consumer_audit,
)
from seed_runtime.emitter_attribution_audit import (
    build_emitter_attribution_audit,
    emitter_attribution_audit_json,
    format_emitter_attribution_audit,
)
from seed_runtime.correlation_audit import (
    build_correlation_audit,
    correlation_audit_json,
    format_correlation_audit,
)
from seed_runtime.contradictions import (
    Contradiction,
    build_contradiction_summary,
    build_contradictions,
)
from seed_runtime.decisions import DecisionValidator
from seed_runtime.diagnostic_inventory import (
    diagnostic_inventory_json,
    diagnostic_surface_definition_json,
    diagnostic_surface_explanation_json,
    format_diagnostic_inventory,
    format_diagnostic_surface_definition,
    format_diagnostic_surface_explanation,
)
from seed_runtime.documentation_structure import (
    DocumentationStructureDetailExpansions,
    DocumentationStructureDrilldownOptions,
    DocumentationStructureMembershipOptions,
    DocumentationStructureOptions,
    DocumentationStructureOutputBounds,
    DocumentationStructureRecurrenceOptions,
    DocumentationStructureSelectionFilters,
    documentation_structure_json,
    format_documentation_structure,
    observe_documentation_structure,
)
from seed_runtime.diagnostic_shape_audit import (
    FILTERABLE_AUDIT_STATUSES,
    build_diagnostic_shape_audit,
    diagnostic_shape_audit_json,
    format_diagnostic_shape_audit,
)
from seed_runtime.question_surface_inventory import (
    BOUNDED_ASK_ARG_VALUES,
    BOUNDED_ASK_DISPATCH_SURFACES,
    BOUNDED_ASK_REQUIRED_SURFACE_ARGS,
    bounded_status_for_question_family,
    build_question_surface_inventory,
    format_question_family_definition,
    format_composed_question_family_explanation,
    format_question_surface_inventory,
    question_family_definition_json,
    composed_question_family_explanation_json,
    question_surface_inventory_json,
)
from seed_runtime.projection_shape import (
    build_projection_shape,
    format_projection_shape,
    format_projection_stage_definition,
    format_projection_stage_explanation,
    projection_shape_json,
    projection_stage_definition_json,
    projection_stage_explanation_json,
)
from seed_runtime.projected_state_consumers import (
    build_projected_state_consumers,
    format_projected_state_consumers,
    projected_state_consumers_json,
)
from seed_runtime.implementation_trait_characterization import (
    build_implementation_trait_characterization,
    format_implementation_trait_characterization,
    implementation_trait_characterization_json,
)
from seed_runtime.observation_inventory import (
    build_observation_inventory,
    format_observation_inventory,
)
from seed_runtime.observation_domains import (
    build_observation_domains,
    format_observation_domains,
    observation_domains_json,
)
from seed_runtime.observation_permission import (
    build_observation_permission,
    format_observation_permission,
    observation_permission_json,
)
from seed_runtime.observation_utilization import (
    build_observation_utilization_audit,
    format_observation_utilization,
    observation_utilization_json,
)
from seed_runtime.ops_brief import build_ops_brief, format_ops_brief
from seed_runtime.operational_story import (
    build_operational_story,
    format_operational_story,
    operational_story_json,
)
from seed_runtime.operational_graph import (
    build_operational_graph,
    build_operational_graph_confidence,
    build_operational_graph_taxonomy,
    format_operational_graph,
    format_operational_graph_confidence,
    format_operational_graph_taxonomy,
    operational_graph_confidence_json,
    operational_graph_json,
    operational_graph_taxonomy_json,
)
from seed_runtime.operational_surface_inventory import (
    build_operational_surface_classification_audit,
    build_operational_surface_inventory,
    build_visibility_coverage_audit,
    format_operational_surface_classification_audit,
    format_operational_surface_inventory,
    format_visibility_coverage_audit,
    operational_surface_classification_audit_json,
    operational_surface_inventory_json,
    visibility_coverage_audit_json,
)
from seed_runtime.investigation_path_audit import (
    build_investigation_path_audit,
    format_investigation_path_audit,
    investigation_path_audit_json,
)
from seed_runtime.impact_audit import (
    build_impact_audit,
    format_impact_audit,
    impact_audit_json,
)
from seed_runtime.history_brief import (
    build_history_brief,
    format_history_brief,
    history_brief_json,
)
from seed_runtime.repository_observation import (
    format_repository_observation,
    observe_repository,
    repository_observation_json,
)
from seed_runtime.snapshot_policy_audit import (
    build_snapshot_policy_audit,
    format_snapshot_policy_audit,
    snapshot_policy_audit_json,
)
from seed_runtime.pressure_audit import (
    build_pressure_audit,
    format_pressure_audit,
    pressure_audit_json,
)
from seed_runtime.privilege_discovery import (
    build_privilege_discovery,
    format_privilege_discovery,
    privilege_discovery_json,
)
from seed_runtime.reasoning_path_audit import (
    build_reasoning_path_audit,
    format_reasoning_path_audit,
    reasoning_path_audit_json,
)
from seed_runtime.reference_selection import (
    build_reference_selection,
    format_reference_selection,
    reference_selection_json,
)
from seed_runtime.selection_path_audit import (
    build_selection_path_audit,
    format_selection_path_audit,
    selection_path_audit_json,
)
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
from seed_runtime.execution_status import (
    CliExecutionStatusConsumer,
    ExecutionStatusConsumer,
    emit_status,
)
from seed_runtime.fact_index import load_or_build_fact_index
from seed_runtime.evidence_graph import (
    FactEvidenceView,
    build_evidence_graph,
    build_evidence_summary,
    find_evidence_for_fact,
    unsupported_fact_views,
)
from seed_runtime.explanations import (
    BeliefExplanation,
    Explanation,
    ExplanationBuilder,
    FactExplanation,
)
from seed_runtime.execution_proposals import ExecutionProposalService
from seed_runtime.handoff_plans import (
    HandoffPlanNotFoundError,
    HandoffPlanService,
    HandoffPlanStatusError,
)
from seed_runtime.ids import new_id
from seed_runtime.inference_catalog import InferenceCatalog
from seed_runtime.knowledge_reachability import (
    build_knowledge_reachability_audit_result,
    format_knowledge_reachability_table,
    knowledge_reachability_json,
)
from seed_runtime.local_host_mounts import (
    MOUNT_COLLAPSE_GROUP_ORDER,
    classify_mount_collapse_group,
    mount_display_priority,
)
from seed_runtime.inquiry_orientation import (
    build_inquiry_orientation,
    format_inquiry_orientation,
    record_inquiry_note,
    select_inquiry_note,
)
from seed_runtime.inquiry_artifacts import (
    build_inquiry_artifacts,
    format_inquiry_artifacts,
    inquiry_artifacts_json,
)
from seed_runtime.integrity_summary import (
    ProjectionIntegritySummary,
    build_projection_integrity_summary,
)
from seed_runtime.intent_classifier import (
    IntentDecisionProducer,
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
from seed_runtime.projection_store import (
    ProjectionStore,
    SQLiteProjectionStore,
    STATE_PROJECTION_NAME,
    STATE_PROJECTION_VERSION,
    STATE_SUMMARY_PROJECTION_NAME,
    STATE_SUMMARY_PROJECTION_VERSION,
    SummaryProjectionSnapshot,
    StateCacheStatus,
    project_state_with_cache,
    state_from_payload,
    rebuild_state_cache,
)
from seed_runtime.observation_sources import (
    JsonObservationSource,
    LocalHostObservationSource,
    ObservationCollectionService,
    ObservationIngestionDiagnostics,
    PrometheusObservationSource,
    RepositorySourceObservationSource,
    diff_observations_json,
    export_observations_json,
)
from seed_runtime.observations import ObservationIngestor
from seed_runtime.ownership_discrepancies import (
    build_ownership_discrepancies,
    diagnostic_capability_need_records,
    format_ownership_discrepancies,
    ownership_discrepancies_json,
)
from seed_runtime.registry import ToolRegistry
from seed_runtime.rule_inventory import collect_rule_inventory
from seed_runtime.runtime import Runtime
from seed_runtime.runtime_trace import RuntimeTrace, load_runtime_trace
from seed_runtime.serialization import to_plain
from seed_runtime.secrets import (
    SECRET_FIELD_NAMES,
    normalize_field_name,
    reject_secret_fields,
)
from seed_runtime.state import ProjectionBuildDiagnostics, State, StateProjector
from seed_runtime.source_navigation import (
    build_source_navigation,
    format_source_navigation,
)
from seed_runtime.state_summary_views import state_summary
from seed_runtime.state_views import (
    CapabilityView,
    FactView,
    IssueView,
    ObservationView,
    RequirementView,
    StateSummary,
    build_capability_view,
    build_fact_view,
    build_issue_view,
    build_observation_view,
    build_requirement_view,
    build_state_summary,
)
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
    decision_input_composer: DecisionInputComposer
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
        decision_input = self.decision_input_composer.compose(
            self.workspace_id, self.session_id, input_event, state
        )
        return self.model_client.complete(decision_input)


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
    pending_observations: list[Observation] = []
    pending_actor: Literal["system", "user"] | None = None
    facts: list[Fact | None] = []

    def flush_pending() -> None:
        nonlocal pending_observations, pending_actor
        if not pending_observations or pending_actor is None:
            return
        facts.extend(
            ingestor.ingest_many(
                pending_observations,
                workspace_id,
                actor=pending_actor,
                session_id=session_id,
            )
        )
        pending_observations = []
        pending_actor = None

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
        actor: Literal["system", "user"] = (
            "user" if seed.source_type == "user" else "system"
        )
        if pending_actor is not None and actor != pending_actor:
            flush_pending()
        pending_actor = actor
        pending_observations.append(observation)
    flush_pending()
    return [fact for fact in facts if fact is not None]


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
    status_consumer: ExecutionStatusConsumer | None = None,
    diagnostics: list[ObservationIngestionDiagnostics] | None = None,
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
        status_consumer=status_consumer,
        diagnostics=diagnostics,
    )


def format_observation_ingestion_diagnostics(
    diagnostics: list[ObservationIngestionDiagnostics],
) -> str:
    """Format ingestion timing diagnostics for comparable source inspection."""

    lines = ["Observation ingestion timings:"]
    for diagnostic in diagnostics:
        lines.extend(
            [
                f"- source: {diagnostic.source_name}",
                f"  source collection: {diagnostic.source_collection_seconds:.6f}s",
                f"  normalization: {diagnostic.normalization_seconds:.6f}s",
                "  event generation + ledger write: "
                f"{diagnostic.event_generation_and_ledger_write_seconds:.6f}s",
                f"  total: {diagnostic.total_seconds:.6f}s",
                f"  total observations: {diagnostic.total_observations}",
                f"  total events: {diagnostic.total_events}",
                f"  facts promoted: {diagnostic.facts_promoted}",
                f"  observations/sec: {diagnostic.observations_per_second:.2f}",
                f"  events/sec: {diagnostic.events_per_second:.2f}",
            ]
        )
        for key in sorted(diagnostic.source_counters):
            lines.append(f"  {key}: {diagnostic.source_counters[key]}")
    return "\n".join(lines)


def ingest_observation_source(
    ledger: EventLedger,
    workspace_id: str,
    source: Any,
    *,
    session_id: str | None = None,
    predicate_catalog_path: str | Path | None = None,
    status_consumer: ExecutionStatusConsumer | None = None,
    diagnostics: list[ObservationIngestionDiagnostics] | None = None,
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
        status_consumer=status_consumer,
        diagnostics=diagnostics,
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
    if instance is not None and labels.get("instance", observation.subject) != instance:
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
    decision_input_composer = DecisionInputComposer(registry)
    model_client = IntentPromptModelClient.for_endpoint(
        endpoint,
        timeout_seconds=timeout_seconds,
        extra_payload={"model": model, "stream": False, "format": "json"},
    )
    classifier = TextIntentClassifier(model_client)
    model = IntentDecisionProducer(classifier)
    runtime = Runtime(
        ledger,
        projector,
        decision_input_composer,
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
        decision_input_composer=decision_input_composer,
        model_client=model_client,
        workspace_id=workspace_id,
        session_id=session_id,
    )


def _confidence_arg(value: str) -> float | str:
    if value == "__report__":
        return value
    return float(value)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run Seed locally with Ollama /api/generate intent classification.",
        epilog=(
            "Examples:\n"
            "  python scripts/seed_local.py --fact web_service host example_host "
            "--fact web_service runtime docker 'restart web_service?'\n"
            "  python scripts/seed_local.py --db .seed-local.sqlite "
            "--registered-provider docker_container_lifecycle "
            "--fact web_service host example_host --preconditions plan_000001\n"
            "  python scripts/seed_local.py --db .seed-local.sqlite "
            "--proposal plan_000001\n"
            "  python scripts/seed_local.py --db .seed-local.sqlite "
            "--handoff plan_000001\n"
            "  python scripts/seed_local.py --db .seed-local.sqlite "
            "--authorize-proposal eprop_000001  # experimental/legacy"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "message",
        nargs="*",
        help=(
            "message to send in one-shot mode; use `ask --question-family "
            "<exact-question-family>` for bounded question-family presentation dispatch"
        ),
    )
    parser.add_argument(
        "--question-family",
        help=(
            "with `ask`, dispatch an exact Question Family identifier through "
            "its existing inquiry surface"
        ),
    )
    parser.add_argument(
        "--surface-args",
        nargs="*",
        metavar="VALUE",
        help=(
            "with `ask --question-family`, forward explicit operator-provided "
            "implementation surface parameters unchanged to the existing inquiry surface"
        ),
    )
    parser.add_argument(
        "--presentation",
        action="store_true",
        help=(
            "with `ask --question-family`, return the existing composed "
            "QuestionFamily explanation instead of dispatching to the raw answer surface"
        ),
    )
    parser.add_argument(
        "--db",
        help=(
            "SQLite event ledger path for sharing local state across runs; "
            "use this with state/query commands; --plan lifecycle side paths are experimental/legacy"
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
            "experimental/legacy side path: when a tool need has ranked "
            "recommendations, print a safe, non-executable plan for the top "
            "recommendation; not Core MVP runtime routing"
        ),
    )
    parser.add_argument(
        "--preconditions",
        metavar="PLAN_ID",
        help=(
            "experimental/legacy side path: print an inspect-only execution "
            "precondition report for an action plan without executing or "
            "approving it"
        ),
    )
    parser.add_argument(
        "--proposal",
        metavar="PLAN_ID",
        help=(
            "experimental/legacy side path: create and print a concrete "
            "inspect-only execution proposal for an action plan when "
            "preconditions are satisfied; never executes tools"
        ),
    )
    parser.add_argument(
        "--handoff",
        metavar="PLAN_ID",
        help=(
            "experimental/legacy side path: create and print a non-executable "
            "provider handoff plan for an accepted action plan; never executes "
            "or approves; not Core MVP runtime routing"
        ),
    )
    parser.add_argument(
        "--authorize-proposal",
        metavar="PROPOSAL_ID",
        help=(
            "experimental/legacy side path: grant short-lived execution "
            "authorization metadata for an exact concrete execution proposal; "
            "never executes tools"
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

    parser.add_argument(
        "--audit-snapshot",
        choices=["observation_inventory", "ownership_discrepancies"],
        help="save a local operational audit snapshot for one supported kind",
    )
    parser.add_argument(
        "--audit-snapshots",
        action="store_true",
        help="list local operational audit snapshots",
    )
    parser.add_argument(
        "--audit-compare",
        nargs=2,
        metavar=("SNAPSHOT_A", "SNAPSHOT_B"),
        help="compare two local operational audit snapshots",
    )
    parser.add_argument(
        "--kind",
        choices=["observation_inventory", "ownership_discrepancies"],
        help="audit snapshot kind for --audit-compare",
    )

    parser.add_argument(
        "--documentation-structure",
        action="store_true",
        help="observe read-only structural metadata for top-level repository Markdown docs",
    )
    documentation_selection_group = parser.add_argument_group(
        "documentation structure selection filters"
    )
    documentation_selection_group.add_argument(
        "--document",
        metavar="PATH",
        help="limit --documentation-structure to one repository-relative docs/*.md document",
    )
    documentation_selection_group.add_argument(
        "--missing-front-matter",
        action="store_true",
        help="limit --documentation-structure to docs missing YAML front matter",
    )
    documentation_selection_group.add_argument(
        "--missing-trailing-newline",
        action="store_true",
        help="limit --documentation-structure to docs without a trailing newline",
    )
    documentation_selection_group.add_argument(
        "--empty-sections",
        action="store_true",
        help="limit --documentation-structure to docs with structurally empty sections",
    )
    documentation_detail_group = parser.add_argument_group(
        "documentation structure detail expansions"
    )
    documentation_detail_group.add_argument(
        "--sections",
        action="store_true",
        help="include section inventory blocks in --documentation-structure output",
    )
    documentation_detail_group.add_argument(
        "--links",
        action="store_true",
        help="include link observation blocks in --documentation-structure output",
    )
    documentation_detail_group.add_argument(
        "--code-fences",
        action="store_true",
        help="include fenced code block observation blocks in --documentation-structure output",
    )
    documentation_detail_group.add_argument(
        "--recurrence",
        action="store_true",
        help="show read-only corpus-level recurrence over observed documentation structure",
    )
    documentation_detail_group.add_argument(
        "--rare",
        action="store_true",
        help="with --documentation-structure --recurrence, show low-frequency structural labels",
    )
    documentation_detail_group.add_argument(
        "--missing-common-sections",
        action="store_true",
        help="with --documentation-structure --recurrence, show structurally common section labels absent from documents",
    )
    documentation_detail_group.add_argument(
        "--outliers",
        action="store_true",
        help="with --documentation-structure, rank documents by structural signals only",
    )
    documentation_detail_group.add_argument(
        "--skeletons",
        action="store_true",
        help="with --documentation-structure --recurrence, include section skeleton signature rows",
    )
    documentation_detail_group.add_argument(
        "--where",
        metavar="CATEGORY:KEY",
        help="with --documentation-structure, drill down to exact structural occurrences; supports section-label:<label>",
    )
    documentation_detail_group.add_argument(
        "--membership",
        metavar="CATEGORY:KEY",
        help="with --documentation-structure, list documents in an exact structural set; supports section-label:<label>",
    )

    documentation_output_group = parser.add_argument_group(
        "documentation structure output bounds"
    )
    documentation_output_group.add_argument(
        "--limit",
        type=int,
        metavar="N",
        help="with --documentation-structure, emit at most N matching document rows",
    )
    documentation_output_group.add_argument(
        "--top",
        type=int,
        metavar="N",
        help="with --documentation-structure, emit the top N documents by structural issue count",
    )
    documentation_output_group.add_argument(
        "--summary-only",
        action="store_true",
        help="with --documentation-structure, emit summary and boundary without document rows or detail blocks",
    )
    documentation_output_group.add_argument(
        "--min-count",
        type=int,
        metavar="N",
        help="with --documentation-structure --recurrence, emit itemized recurrence entries observed at least N times",
    )
    documentation_output_group.add_argument(
        "--max-count",
        type=int,
        metavar="N",
        help="with --documentation-structure --recurrence --rare, emit rare entries observed at most N times",
    )
    parser.add_argument(
        "--container-ownership-authority",
        action="store_true",
        help="show bounded read-only container ownership authority reasoning",
    )
    parser.add_argument(
        "--service-ownership-authority",
        action="store_true",
        help="show bounded read-only service ownership authority reasoning",
    )
    parser.add_argument(
        "--listener-endpoint-authority",
        action="store_true",
        help="show bounded read-only local listener endpoint authority reasoning",
    )
    parser.add_argument(
        "--diagnostic-inventory",
        action="store_true",
        help="list diagnostic/test-like operational surfaces and their declared shape",
    )
    parser.add_argument(
        "--diagnostic-surface-definition",
        metavar="DIAGNOSTIC",
        help="explain the implementation-backed identity of one diagnostic surface",
    )
    parser.add_argument(
        "--diagnostic-surface-explanation",
        metavar="DIAGNOSTIC",
        help="compose existing explanation fields for one diagnostic surface",
    )
    parser.add_argument(
        "--question-surface-inventory",
        "--question-families",
        action="store_true",
        help="list known question families and the existing Seed surfaces that answer them",
    )
    parser.add_argument(
        "--question-family-definition",
        metavar="QUESTION_FAMILY",
        help="explain the implementation-backed identity of one QuestionFamily",
    )
    parser.add_argument(
        "--question-family-explanation",
        metavar="QUESTION_FAMILY",
        help="compose existing QuestionFamily explanation fields for presentation",
    )
    parser.add_argument(
        "--diagnostic-shape-audit",
        action="store_true",
        help="compare diagnostic registry declarations with static implementation shape",
    )
    parser.add_argument(
        "--projected-state-consumers",
        action="store_true",
        help="show which known surfaces consume projected state and other evidence sources",
    )
    parser.add_argument(
        "--implementation-trait-characterization",
        action="store_true",
        help="show implementation-backed trait-to-concern characterization for exposed visibility traits",
    )
    parser.add_argument(
        "--architecture-conformance-audit",
        action="store_true",
        help="compare architecture evidence with observed operational structure",
    )
    parser.add_argument(
        "--component-audit",
        metavar="COMPONENT",
        help="summarize a component's current repository role from read-only visibility evidence",
    )
    parser.add_argument(
        "--operational-story",
        action="store_true",
        help="compose existing operational evidence into a read-only story view",
    )
    parser.add_argument(
        "--reasoning-path",
        nargs=2,
        metavar=("DOMAIN", "SUBJECT"),
        help="show the evidence-backed derivation path for an operational conclusion",
    )
    parser.add_argument(
        "--selection-path",
        metavar="TARGET",
        help="show read-only selection evidence for why an operational conclusion was selected",
    )
    parser.add_argument(
        "--reference-selection",
        metavar="DOMAIN",
        choices=["history"],
        help="show read-only comparison-reference selection visibility for a question domain",
    )
    parser.add_argument(
        "--operational-graph",
        action="store_true",
        help="build the implementation-backed operational relationship graph",
    )
    parser.add_argument(
        "--operational-graph-confidence",
        action="store_true",
        help="analyze operational graph edge confidence quality",
    )
    parser.add_argument(
        "--exclude-aggregate",
        action="store_true",
        help="exclude aggregate endpoint edges from --operational-graph-confidence",
    )
    parser.add_argument(
        "--operational-graph-taxonomy",
        action="store_true",
        help="summarize operational graph node classifications and aggregate connectivity",
    )
    parser.add_argument(
        "operational_graph_confidence_tier",
        nargs="?",
        choices=["high", "medium", "low"],
        help="optional confidence tier filter for --operational-graph-confidence",
    )
    parser.add_argument(
        "--operational-graph-confidence-tier",
        dest="operational_graph_confidence_tier_option",
        choices=["high", "medium", "low"],
        help="optional confidence tier filter for --operational-graph-confidence",
    )
    parser.add_argument(
        "--operational-surface-inventory",
        action="store_true",
        help="discover operational CLI surfaces from implementation evidence",
    )
    parser.add_argument(
        "--visibility-coverage-audit",
        action="store_true",
        help="audit which discovered operational surfaces are visible in diagnostic inventory",
    )
    parser.add_argument(
        "--operational-surface-classification-audit",
        action="store_true",
        help="classify discovered CLI elements as primary surfaces, filters, modifiers, debug, manual-input, legacy, or unknown",
    )
    parser.add_argument(
        "--mismatches",
        action="store_true",
        help="with --diagnostic-shape-audit, show only mismatch rows",
    )
    parser.add_argument(
        "--status",
        choices=FILTERABLE_AUDIT_STATUSES,
        help="with --diagnostic-shape-audit, show only rows with this audit status",
    )
    parser.add_argument(
        "--consumer-audit",
        action="store_true",
        help="audit implementation-backed consumers of predicates and diagnostics",
    )
    parser.add_argument(
        "--emitter-consumer-audit",
        action="store_true",
        help="audit implementation-backed emitted outputs and their visible consumers",
    )
    parser.add_argument(
        "--emitter-attribution-audit",
        action="store_true",
        help="explain why emitted artifacts have attributed or unknown emitters",
    )
    parser.add_argument(
        "--include-rendered",
        action="store_true",
        help="with emitter audits, include rendered/fallback/guardrail strings with a distinct classification",
    )
    parser.add_argument(
        "--observation-inventory",
        action="store_true",
        help="discover observation providers and predicates from implementation",
    )
    parser.add_argument(
        "--observation-utilization",
        action="store_true",
        help="audit where observation predicates participate after collection",
    )
    parser.add_argument(
        "--observation-domains",
        nargs="?",
        const="__all__",
        metavar="DOMAIN",
        help="show read-only observation-domain coverage and gap visibility derived from existing evidence",
    )
    parser.add_argument(
        "--observation-permission",
        nargs="?",
        const="__all__",
        metavar="DOMAIN",
        help="show read-only observation-domain permission visibility without enforcement or approval storage",
    )
    parser.add_argument(
        "--ops-brief",
        action="store_true",
        help="summarize current operational state from existing read-only audits",
    )
    parser.add_argument(
        "--investigation-path",
        metavar="DOMAIN",
        help="show a read-only evidence-backed investigation path across existing surfaces",
    )
    parser.add_argument(
        "--impact-audit",
        action="store_true",
        help="audit before/after operational outcomes from existing snapshots without recording or mutating cluster state",
    )
    parser.add_argument(
        "--history-brief",
        action="store_true",
        help="summarize supportable historical changes, stability, repository context, and uncertainty",
    )
    parser.add_argument(
        "--snapshot-policy-audit",
        action="store_true",
        help="audit snapshot readiness and usefulness without creating snapshots or mutating state",
    )
    parser.add_argument(
        "--observe-repository",
        metavar="PATH",
        help="observe read-only repository state for an arbitrary local repository path",
    )
    parser.add_argument(
        "--pressure-audit",
        action="store_true",
        help="rank current operational pressure from existing read-only audits",
    )
    parser.add_argument(
        "--privilege-discovery",
        action="store_true",
        help="explain privilege boundaries for current capability needs without escalation",
    )
    parser.add_argument(
        "--capability-relationship",
        nargs="?",
        const="__all__",
        metavar="CAPABILITY",
        help="explain read-only capability relationship visibility for all or one capability",
    )
    parser.add_argument(
        "--correlation-audit",
        action="store_true",
        help="expose suspected disconnects between evidence, consumers, and pressure surfaces",
    )
    parser.add_argument(
        "--provider",
        help="limit --observation-inventory to one provider name",
    )
    parser.add_argument(
        "--predicate",
        help="limit --observation-inventory to one predicate",
    )
    parser.add_argument(
        "--projection-shape",
        action="store_true",
        help="show read-only implementation-backed projection stage shape",
    )
    parser.add_argument(
        "--projection-stage-definition",
        metavar="STAGE",
        help="explain read-only implementation-backed identity for one projection stage",
    )
    parser.add_argument(
        "--projection-stage-explanation",
        metavar="STAGE",
        help="compose existing explanation fields for one projection stage",
    )
    parser.add_argument(
        "--knowledge-reachability-audit",
        action="store_true",
        help="audit knowledge reachability across preserved, projected, read-model, inquiry, and rendered surfaces",
    )
    parser.add_argument(
        "--knowledge-reachability-audit-family",
        choices=[
            "runtime",
            "relationships",
            "ownership",
            "projection",
            "repository",
            "inquiry",
        ],
        help="limit knowledge reachability audit to one candidate family",
    )
    parser.add_argument(
        "--knowledge-reachability-audit-subject",
        help="limit knowledge reachability audit to one candidate string",
    )
    parser.add_argument(
        "--candidate-kind",
        choices=[
            "repository_concept",
            "code_symbol",
            "schema_field",
            "runtime_value",
            "platform_value",
            "generated_identifier",
            "network_identifier",
            "presentation_label",
            "relationship_label",
            "unknown",
        ],
        help="limit knowledge reachability audit to one candidate kind",
    )
    parser.add_argument(
        "--knowledge-reachability-audit-json",
        action="store_true",
        help="render knowledge reachability audit as JSON",
    )
    parser.add_argument(
        "--knowledge-reachability-audit-debug",
        action="store_true",
        help="print structured reachability audit diagnostics to stderr",
    )
    parser.add_argument(
        "--knowledge-reachability-audit-limit",
        type=int,
        default=500,
        help="maximum candidates to evaluate by default (default: 500)",
    )
    parser.add_argument(
        "--knowledge-reachability-audit-all",
        action="store_true",
        help="evaluate all discovered candidates without the default cap",
    )
    parser.add_argument(
        "--knowledge-reachability-audit-max-seconds",
        type=float,
        default=60.0,
        help="soft maximum evaluation seconds before rendering partial results (default: 60)",
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
            "(for example: --fact web_service host example_host, "
            "--fact web_service runtime docker)"
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
        "--observe-repository-source",
        metavar="PATH",
        help=(
            "read-only repository source intake for allowlisted Python files; "
            "emits only imports and defines observations"
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
        "--show-inference-catalog",
        action="store_true",
        help="print deterministic inference rules, then exit",
    )
    parser.add_argument(
        "--rules",
        "--explain-rules",
        dest="rules",
        action="store_true",
        help=(
            "print Seed's read-only deterministic rule inventory as JSON, "
            "then exit; does not project state, append events, or execute tools"
        ),
    )
    parser.add_argument(
        "--verbose-observations",
        action="store_true",
        help="print every ingested observation-derived fact instead of a summary",
    )
    parser.add_argument(
        "--quiet-output",
        action="store_true",
        help=(
            "for observation workflows, suppress normal stdout knowledge rendering "
            "while preserving execution-status output and ingestion"
        ),
    )
    parser.add_argument(
        "--observe-timings",
        action="store_true",
        help="print comparable observation ingestion timing diagnostics",
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
        nargs="?",
        const="__report__",
        default=1.0,
        type=_confidence_arg,
        help=(
            "print confidence aggregation when used without a value; with a numeric "
            "value, set confidence for --observe entries from 0.0 to 1.0 "
            "(default: 1.0)"
        ),
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
        "--impact",
        metavar="ENTITY",
        help=(
            "print a concise projected-state impact view for an entity; "
            "resolves aliases and never ingests observations or executes tools"
        ),
    )
    parser.add_argument(
        "--unhealthy",
        "--down",
        dest="unhealthy",
        action="store_true",
        help=(
            "print current down endpoints and graph errors from projected state; "
            "never ingests observations or executes tools"
        ),
    )
    parser.add_argument(
        "--include-warnings",
        action="store_true",
        help="include graph warnings in --unhealthy output",
    )
    parser.add_argument(
        "--relationships",
        action="store_true",
        help="print projected topology relationships and exit",
    )
    parser.add_argument(
        "--relationship-subject",
        metavar="SUBJECT",
        help="filter --relationships by subject",
    )
    parser.add_argument(
        "--relationship",
        metavar="RELATIONSHIP",
        help="filter --relationships by relationship name",
    )
    parser.add_argument(
        "--relationship-object",
        metavar="OBJECT",
        help="filter --relationships by object",
    )
    parser.add_argument(
        "--graph-issues",
        action="store_true",
        help="print projected graph validation issues and exit",
    )
    parser.add_argument(
        "--graph-issue-summary",
        action="store_true",
        help=(
            "print a read-only grouped summary of projected graph validation "
            "issues and exit"
        ),
    )
    parser.add_argument(
        "--graph-issue-limit",
        type=int,
        default=10,
        help="maximum graph issue categories to show in --graph-issue-summary",
    )
    parser.add_argument(
        "--graph-issue-examples",
        type=int,
        default=3,
        help="maximum example issues per category in --graph-issue-summary",
    )
    parser.add_argument(
        "--severity",
        choices=["warning", "error"],
        help="filter --graph-issues by severity",
    )
    parser.add_argument(
        "--classification-coverage",
        action="store_true",
        help="inspect projected entity classification coverage; read-only unless --record is also supplied",
    )
    parser.add_argument(
        "--record",
        action="store_true",
        help="with --classification-coverage, append diagnostic self-observation evidence",
    )
    parser.add_argument(
        "--entity-types",
        action="store_true",
        help="print projected current entity types and exit",
    )
    parser.add_argument(
        "--entity-type",
        metavar="ENTITY",
        help="print projected type assertions for one entity and exit",
    )
    parser.add_argument(
        "--candidate-requests",
        metavar="TEXT",
        help=(
            "inspect language-derived candidate requests as read-only JSON; "
            "does not select capabilities, evaluate policy, or execute tools"
        ),
    )
    parser.add_argument(
        "--candidate-routes",
        metavar="TEXT",
        help=(
            "inspect language-derived candidate routes as read-only JSON; "
            "does not select capabilities, evaluate policy, or execute tools"
        ),
    )
    parser.add_argument(
        "--record-inquiry-note",
        metavar="TEXT",
        help="append raw operator prose to the isolated inquiry-note probe store",
    )
    parser.add_argument(
        "--inquiry-orientation",
        nargs="?",
        const="__latest__",
        metavar="NOTE_ID",
        help="render a bounded read-only orientation view for an inquiry note",
    )
    parser.add_argument(
        "--inquiry-artifacts",
        action="store_true",
        help="show read-only repository-visible inquiry artifact classifications",
    )
    parser.add_argument(
        "--state-build",
        action="store_true",
        help=(
            "print a concise read-only summary of the projected world model; "
            "does not ingest observations or execute tools"
        ),
    )
    parser.add_argument(
        "--state-build-cache-debug",
        action="store_true",
        help=(
            "print read-only state-build cache eligibility, hit/miss status, "
            "last-event ids, and phase timings; does not ingest observations or execute tools"
        ),
    )
    parser.add_argument(
        "--integrity-summary",
        action="store_true",
        help=(
            "print a concise read-only Projection Integrity Summary; "
            "aggregates existing projected integrity signals only"
        ),
    )
    parser.add_argument(
        "--rebuild-state-cache",
        action="store_true",
        help="clear and rebuild the persisted projection cache for --db",
    )
    parser.add_argument(
        "--state-cache-status",
        action="store_true",
        help="print projection cache hit/miss status for --db",
    )
    parser.add_argument(
        "--why",
        nargs=2,
        metavar=("ENTITY", "PREDICATE"),
        help="explain why Seed holds, rejects, or considers a current belief ambiguous",
    )
    parser.add_argument(
        "--evidence",
        action="store_true",
        help=(
            "print a read-only Evidence Graph summary and linked evidence list; "
            "does not execute runtime behavior or append events"
        ),
    )
    parser.add_argument(
        "--why-fact",
        nargs="+",
        metavar="ARG",
        help="explain evidence for SUBJECT PREDICATE [OBJECT] from projected State",
    )
    parser.add_argument(
        "--unsupported-facts",
        action="store_true",
        help="print projected facts with no linked supporting evidence",
    )
    parser.add_argument(
        "--contradictions",
        action="store_true",
        help=(
            "print read-only contradictions from projected State and Evidence Graph; "
            "does not resolve facts, execute runtime behavior, or append events"
        ),
    )
    parser.add_argument(
        "--confidence-fact",
        nargs="+",
        metavar="ARG",
        help="print confidence for SUBJECT PREDICATE [OBJECT] from projected State",
    )
    parser.add_argument(
        "--trace-run",
        metavar="RUN_ID",
        help=(
            "print a read-only ordered historical runtime trace for RUN_ID; "
            "does not replay, call providers/policy/tools, or append events"
        ),
    )
    parser.add_argument(
        "--why-run",
        metavar="RUN_ID",
        help=(
            "print a concise read-only explanation for historical runtime RUN_ID; "
            "does not replay, call providers/policy/tools, or append events"
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
        "--source-navigation",
        metavar="QUERY",
        help=(
            "print read-only source navigation from preserved imports/defines facts; "
            "does not inspect repository files, parse source, or append events"
        ),
    )
    parser.add_argument(
        "--current-facts",
        nargs="*",
        metavar=("SUBJECT", "PREDICATE"),
        help=(
            "print all projected Fact views; optionally pass SUBJECT PREDICATE "
            "for the legacy current-fact query"
        ),
    )
    parser.add_argument(
        "--current-facts-cache-debug",
        action="store_true",
        help=(
            "print current-facts cache status and phase timings; "
            "does not ingest observations or execute tools"
        ),
    )
    parser.add_argument(
        "--current-observations",
        action="store_true",
        help="print read-only projected Observation views and exit",
    )
    parser.add_argument(
        "--current-requirements",
        action="store_true",
        help="print read-only projected Requirement views and exit",
    )
    parser.add_argument(
        "--current-capabilities",
        action="store_true",
        help="print read-only projected Capability views and exit",
    )
    parser.add_argument(
        "--capability-status",
        action="store_true",
        help=(
            "print read-only capability verification inventory as deterministic JSON "
            "and exit; derives only from projected facts/evidence"
        ),
    )
    parser.add_argument(
        "--capability-candidates",
        nargs="?",
        const="__all__",
        metavar="FILTER",
        help=(
            "print read-only evidence-derived capability candidates as deterministic JSON; "
            "optional FILTER such as ssh, python, docker, git, or curl; does not select, "
            "evaluate policy, plan, or execute tools"
        ),
    )
    parser.add_argument(
        "--verification-evidence",
        nargs="?",
        const="__all__",
        metavar="FILTER",
        help=(
            "print read-only locally acquired verification evidence as deterministic JSON; "
            "optional FILTER such as ssh, python, docker, git, or curl; inspects PATH "
            "without invoking tools, selecting capabilities, evaluating policy, planning, "
            "authorizing, or executing"
        ),
    )
    parser.add_argument(
        "--capability-promotion-readiness",
        nargs="?",
        const="__all__",
        metavar="FILTER",
        help=(
            "print read-only capability verification promotion-readiness as deterministic JSON; "
            "optional FILTER such as ssh, python, docker, git, or curl; does not promote, "
            "create capability_verified facts, select, evaluate policy, authorize, or execute"
        ),
    )
    parser.add_argument(
        "--capability-verification",
        nargs="?",
        const="__all__",
        metavar="FILTER",
        help=(
            "print read-only candidate capability verification status as deterministic JSON; "
            "optional FILTER such as ssh, python, docker, git, or curl; does not select, "
            "evaluate policy, plan, authorize, or execute tools"
        ),
    )
    parser.add_argument(
        "--current-issues",
        action="store_true",
        help="print read-only projected Issue views and exit",
    )
    parser.add_argument(
        "--decision-context",
        action="store_true",
        help="print the read-only Decision Context View and exit",
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
            "include expired facts in --fact-support, --best-fact, "
            "--current-facts, and --fact-conflicts query output"
        ),
    )
    parser.add_argument(
        "--inferred-facts",
        metavar="ENTITY",
        help="print projected inferred facts for an entity",
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
    parser.add_argument(
        "--ownership-discrepancies",
        action="store_true",
        help=(
            "infer provisional storage/service ownership candidates from existing "
            "facts and report ambiguous or conflicting ownership; read-only unless --record is also supplied"
        ),
    )
    parser.add_argument(
        "--capability-needs",
        action="store_true",
        help="print recorded diagnostic capability needs and exit",
    )
    parser.add_argument(
        "--diagnostic",
        help="limit --capability-needs to one diagnostic name",
    )
    parser.add_argument(
        "--subject",
        help="limit --ownership-discrepancies to one subject",
    )
    parser.add_argument(
        "--json",
        dest="json_output",
        action="store_true",
        help="render supported diagnostic commands as JSON",
    )
    return parser


def apply_bounded_ask_dispatch(
    args: argparse.Namespace, parser: argparse.ArgumentParser
) -> None:
    """Map `ask --question-family` to the existing exact inquiry surface."""

    if args.question_family is None:
        if args.message == ["ask"] and args.question_surface_inventory:
            args.message = []
            return
        if args.surface_args is not None:
            parser.error(
                "--surface-args can only be used as "
                "`ask --question-family <exact-question-family> --surface-args ...`"
            )
        if args.presentation:
            parser.error(
                "--presentation can only be used as "
                "`ask --question-family <exact-question-family> --presentation`"
            )
        if args.message and args.message[0] == "ask":
            parser.error("ask requires --question-family <exact-question-family>")
        return
    if args.message != ["ask"]:
        parser.error(
            "--question-family can only be used as "
            "`ask --question-family <exact-question-family>`"
        )

    inventory_families = {
        row.question_family for row in build_question_surface_inventory()
    }
    family = args.question_family
    if family not in inventory_families:
        parser.error(f"unknown Question Family: {family}")

    eligibility = bounded_status_for_question_family(family)
    if eligibility == "eligible_now" and args.surface_args is not None:
        parser.error(
            f"Question Family '{family}' does not accept --surface-args by "
            "current implementation-backed eligibility"
        )

    if eligibility == "eligible_with_parameters":
        required_count = len(BOUNDED_ASK_REQUIRED_SURFACE_ARGS[family])
        surface_args = args.surface_args
        if surface_args is None:
            parser.error(
                f"Question Family '{family}' requires --surface-args with "
                f"exactly {required_count} explicit operator-provided value(s)"
            )
        if len(surface_args) != required_count:
            parser.error(
                f"Question Family '{family}' requires exactly {required_count} "
                f"--surface-args value(s); received {len(surface_args)}"
            )
        if args.presentation:
            args.question_family_explanation = family
            args.message = []
            return
        surface_value = surface_args[0] if required_count == 1 else surface_args
        setattr(args, BOUNDED_ASK_DISPATCH_SURFACES[family], surface_value)
        args.message = []
        return

    if eligibility != "eligible_now":
        if eligibility == "diagnostic_only":
            parser.error(
                f"Question Family '{family}' is diagnostic_only and is not an "
                "inquiry-answer surface for bounded ask"
            )
        parser.error(
            f"Question Family '{family}' is not_dispatchable by current "
            "implementation-backed eligibility"
        )

    if args.presentation:
        args.question_family_explanation = family
        args.message = []
        return

    setattr(
        args,
        BOUNDED_ASK_DISPATCH_SURFACES[family],
        BOUNDED_ASK_ARG_VALUES.get(family, True),
    )
    if family == "knowledge reachability" and args.json_output:
        args.knowledge_reachability_audit_json = True
        args.json_output = False
    args.message = []


def normalize_confidence_args(
    args: argparse.Namespace, parser: argparse.ArgumentParser
) -> None:
    """Disambiguate --confidence report mode from observe confidence values."""

    raw_confidence = args.confidence
    args.confidence_report = raw_confidence == "__report__"
    if args.confidence_report:
        args.observe_confidence = 1.0
        return
    try:
        args.observe_confidence = float(raw_confidence)
    except (TypeError, ValueError):
        parser.error(
            "--confidence must be used without a value or with a number from 0.0 to 1.0"
        )
    if args.observe_confidence < 0.0 or args.observe_confidence > 1.0:
        parser.error("--confidence must be between 0.0 and 1.0")


def validate_lifecycle_args(
    args: argparse.Namespace, parser: argparse.ArgumentParser
) -> None:
    normalize_confidence_args(args, parser)
    lifecycle_flags = [
        bool(args.preconditions),
        bool(args.proposal),
        bool(args.handoff),
        bool(args.authorize_proposal or args.authorize_execution),
        bool(args.accept_plan),
        bool(args.approve_plan),
        bool(args.reject_plan),
        bool(args.supersede_plan),
        bool(args.impact),
        bool(args.unhealthy),
        bool(args.why),
        bool(args.evidence),
        bool(args.why_fact),
        bool(args.unsupported_facts),
        bool(args.contradictions),
        bool(args.confidence_report),
        bool(args.confidence_fact),
        bool(args.trace_run),
        bool(args.why_run),
        bool(args.fact_support),
        bool(args.best_fact),
        bool(args.current_facts is not None),
        bool(args.current_facts_cache_debug and args.current_facts is None),
        bool(args.source_navigation),
        bool(args.current_observations),
        bool(args.current_requirements),
        bool(args.current_capabilities),
        bool(args.capability_status),
        bool(args.capability_candidates),
        bool(args.verification_evidence),
        bool(args.capability_verification),
        bool(args.capability_promotion_readiness),
        bool(args.current_issues),
        bool(args.decision_context),
        bool(args.candidate_requests),
        bool(args.candidate_routes),
        bool(args.inquiry_artifacts),
        bool(args.state_build),
        bool(args.state_build_cache_debug),
        bool(args.integrity_summary),
        bool(args.inferred_facts),
        bool(args.fact_conflicts),
        bool(args.stale_facts),
        bool(args.stale_fact_refreshes),
        bool(args.ownership_discrepancies),
        bool(args.capability_needs),
        bool(args.documentation_structure),
        bool(args.container_ownership_authority),
        bool(args.service_ownership_authority),
        bool(args.listener_endpoint_authority),
        bool(args.diagnostic_shape_audit),
        bool(args.diagnostic_surface_definition),
        bool(args.projected_state_consumers),
        bool(args.implementation_trait_characterization),
        bool(args.question_surface_inventory),
        bool(args.projection_shape),
        bool(args.projection_stage_definition),
        bool(args.projection_stage_explanation),
        bool(args.component_audit),
        bool(args.operational_story),
        bool(args.architecture_conformance_audit),
        bool(args.operational_graph),
        bool(args.operational_graph_confidence),
        bool(args.operational_graph_taxonomy),
        bool(args.operational_surface_inventory),
        bool(args.visibility_coverage_audit),
        bool(args.operational_surface_classification_audit),
        bool(args.consumer_audit),
        bool(args.emitter_consumer_audit),
        bool(args.emitter_attribution_audit),
        bool(args.observation_inventory),
        bool(args.observation_utilization),
        bool(args.observation_permission),
        bool(args.ops_brief),
        bool(args.investigation_path),
        bool(args.impact_audit),
        bool(args.history_brief),
        bool(args.snapshot_policy_audit),
        bool(args.pressure_audit),
        bool(args.privilege_discovery),
        bool(args.capability_relationship),
        bool(args.correlation_audit),
        bool(args.audit_snapshot),
        bool(args.audit_snapshots),
        bool(args.audit_compare),
        bool(args.rebuild_state_cache),
        bool(args.state_cache_status),
        bool(args.events_only),
    ]
    if sum(lifecycle_flags) > 1:
        parser.error(
            "choose only one of --preconditions, --proposal, --handoff, "
            "--authorize-proposal, --accept-plan, --approve-plan, "
            "--reject-plan, --supersede-plan, --impact, --unhealthy, --why, "
            "--evidence, --why-fact, --unsupported-facts, --contradictions, "
            "--confidence, --confidence-fact, --trace-run, "
            "--why-run, --fact-support, --best-fact, "
            "--current-facts, --current-facts-cache-debug, "
            "--current-observations, --current-requirements, "
            "--current-capabilities, --capability-status, --capability-candidates, "
            "--verification-evidence, --capability-verification, "
            "--capability-promotion-readiness, --current-issues, "
            "--decision-context, --candidate-requests, --candidate-routes, --inquiry-artifacts, "
            "--state-build, --state-build-cache-debug, --integrity-summary, "
            "--inferred-facts, --fact-conflicts, --stale-facts, "
            "--stale-fact-refreshes, --ownership-discrepancies, "
            "--documentation-structure, --diagnostic-shape-audit, --component-audit, --operational-story, --reasoning-path, --selection-path, --reference-selection, --architecture-conformance-audit, --operational-graph, --operational-surface-inventory, --visibility-coverage-audit, --operational-surface-classification-audit, --consumer-audit, --emitter-consumer-audit, --emitter-attribution-audit, --observation-inventory, --observation-utilization, --observation-domains, --observation-permission, --ops-brief, --investigation-path, --impact-audit, --history-brief, --snapshot-policy-audit, --observe-repository, --pressure-audit, --privilege-discovery, --capability-relationship, --correlation-audit, --audit-snapshot, --audit-snapshots, --audit-compare, --rebuild-state-cache, --state-cache-status, "
            "or --events-only"
        )
    if args.current_facts is not None and len(args.current_facts) not in {0, 2}:
        parser.error("--current-facts accepts either no values or SUBJECT PREDICATE")
    # Cache-debug surfaces are standalone read-only views.  A cache-debug flag
    # owns dispatch for its underlying view and may also be combined with the
    # legacy view flag when that view accepts additional query arguments.
    if args.why_fact is not None and len(args.why_fact) not in {2, 3}:
        parser.error("--why-fact accepts SUBJECT PREDICATE [OBJECT]")
    if args.confidence_fact is not None and len(args.confidence_fact) not in {2, 3}:
        parser.error("--confidence-fact accepts SUBJECT PREDICATE [OBJECT]")
    if args.rebuild_state_cache and not args.db:
        parser.error("--rebuild-state-cache requires --db")
    if (args.rebuild_state_cache or args.state_cache_status) and args.predicate_catalog:
        parser.error("state cache commands require the built-in predicate catalog")
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
        args.fact_support or args.best_fact or args.current_facts or args.fact_conflicts
    ):
        parser.error(
            "--include-expired can only be used with --fact-support, "
            "--best-fact, --current-facts, or --fact-conflicts"
        )
    if args.include_history and not args.fact_support:
        parser.error("--include-history can only be used with --fact-support")
    graph_confidence_tier = (
        args.operational_graph_confidence_tier
        or args.operational_graph_confidence_tier_option
    )
    if graph_confidence_tier and not args.operational_graph_confidence:
        parser.error("confidence tier filter requires --operational-graph-confidence")
    if args.exclude_aggregate and not args.operational_graph_confidence:
        parser.error("--exclude-aggregate requires --operational-graph-confidence")
    documentation_structure_filter_requested = any(
        (
            args.missing_front_matter,
            args.missing_trailing_newline,
            args.empty_sections,
            args.links,
            args.code_fences,
            args.sections,
            args.document is not None,
            args.limit is not None,
            args.top is not None,
            args.summary_only,
            args.min_count is not None,
            args.max_count is not None,
            args.recurrence,
            args.rare,
            args.missing_common_sections,
            args.outliers,
            args.where is not None,
            args.membership is not None,
        )
    )
    if documentation_structure_filter_requested and not args.documentation_structure:
        parser.error(
            "--document, --missing-front-matter, --missing-trailing-newline, "
            "--empty-sections, --links, --code-fences, --sections, --recurrence, --rare, --missing-common-sections, --outliers, --where, --membership, --limit, "
            "--top, --summary-only, --min-count, and --max-count require "
            "--documentation-structure"
        )
    if args.documentation_structure:
        if args.limit is not None and args.limit < 0:
            parser.error("--limit must be zero or greater")
        if args.top is not None and args.top < 0:
            parser.error("--top must be zero or greater")
        if args.min_count is not None and args.min_count < 1:
            parser.error("--min-count must be one or greater")
        if args.max_count is not None and args.max_count < 1:
            parser.error("--max-count must be one or greater")
        if (
            args.max_count is not None
            and args.min_count is not None
            and args.max_count < args.min_count
        ):
            parser.error("--max-count must be greater than or equal to --min-count")
        if (
            args.rare or args.missing_common_sections or args.skeletons
        ) and not args.recurrence:
            parser.error(
                "--rare, --missing-common-sections, and --skeletons require --recurrence"
            )
    if args.audit_compare and not args.kind:
        parser.error("--audit-compare requires --kind")
    if args.kind and not args.audit_compare:
        parser.error("--kind can only be used with --audit-compare")
    if args.provider and not (
        args.observation_inventory or args.observation_utilization
    ):
        parser.error(
            "--provider can only be used with --observation-inventory or --observation-utilization"
        )
    if args.predicate and not (
        args.observation_inventory
        or args.observation_utilization
        or args.consumer_audit
    ):
        parser.error(
            "--predicate can only be used with --observation-inventory, --observation-utilization, or --consumer-audit"
        )
    if args.subject and not (args.ownership_discrepancies or args.capability_needs):
        parser.error(
            "--subject can only be used with --ownership-discrepancies or --capability-needs"
        )
    if args.diagnostic and not (args.capability_needs or args.consumer_audit):
        parser.error(
            "--diagnostic can only be used with --capability-needs or --consumer-audit"
        )
    if args.json_output and not (
        args.ownership_discrepancies
        or args.capability_needs
        or args.diagnostic_inventory
        or args.diagnostic_surface_definition
        or args.diagnostic_surface_explanation
        or args.question_surface_inventory
        or args.question_family_definition
        or args.question_family_explanation
        or args.container_ownership_authority
        or args.service_ownership_authority
        or args.listener_endpoint_authority
        or args.documentation_structure
        or args.diagnostic_shape_audit
        or args.projected_state_consumers
        or args.implementation_trait_characterization
        or args.projection_shape
        or args.projection_stage_definition
        or args.projection_stage_explanation
        or args.component_audit
        or args.operational_story
        or args.reasoning_path
        or args.selection_path
        or args.reference_selection
        or args.architecture_conformance_audit
        or args.operational_graph
        or args.operational_graph_confidence
        or args.operational_graph_taxonomy
        or args.operational_surface_inventory
        or args.visibility_coverage_audit
        or args.operational_surface_classification_audit
        or args.consumer_audit
        or args.emitter_consumer_audit
        or args.emitter_attribution_audit
        or args.observation_inventory
        or args.observation_utilization
        or args.observation_domains
        or args.observation_permission
        or args.ops_brief
        or args.investigation_path
        or args.impact_audit
        or args.history_brief
        or args.snapshot_policy_audit
        or args.observe_repository
        or args.pressure_audit
        or args.privilege_discovery
        or args.capability_relationship
        or args.correlation_audit
        or args.inquiry_artifacts
        or args.audit_compare
    ):
        parser.error(
            "--json can only be used with --ownership-discrepancies, "
            "--capability-needs, --container-ownership-authority, --service-ownership-authority, --listener-endpoint-authority, --diagnostic-inventory, --question-surface-inventory, --question-family-definition, --question-family-explanation, --documentation-structure, --diagnostic-shape-audit, --component-audit, --operational-story, --reasoning-path, --selection-path, --reference-selection, --architecture-conformance-audit, --operational-graph, --operational-surface-inventory, --visibility-coverage-audit, --operational-surface-classification-audit, --consumer-audit, --emitter-consumer-audit, --emitter-attribution-audit, --observation-inventory, --observation-utilization, --observation-domains, --observation-permission, --ops-brief, --investigation-path, --impact-audit, --history-brief, --snapshot-policy-audit, --observe-repository, --pressure-audit, --privilege-discovery, --capability-relationship, --correlation-audit, --inquiry-artifacts, or --audit-compare, or --projection-shape, or --projection-stage-definition, or --projection-stage-explanation"
        )
    if args.question_family_definition and args.message:
        parser.error(
            "--question-family-definition does not accept a free-text question argument"
        )
    if args.question_family_explanation and args.message:
        parser.error(
            "--question-family-explanation does not accept a free-text question argument"
        )
    if args.question_surface_inventory and args.message and args.message != ["ask"]:
        parser.error(
            "--question-surface-inventory does not accept a free-text question argument"
        )
    if args.severity and not args.graph_issues:
        parser.error("--severity can only be used with --graph-issues")
    if args.graph_issue_limit < 0:
        parser.error("--graph-issue-limit must be non-negative")
    if args.graph_issue_examples < 0:
        parser.error("--graph-issue-examples must be non-negative")
    if args.include_warnings and not args.unhealthy:
        parser.error("--include-warnings can only be used with --unhealthy")
    if args.fact_expires_at and args.fact_ttl_seconds is not None:
        parser.error("choose only one of --fact-expires-at or --fact-ttl-seconds")
    if (args.fact_expires_at or args.fact_ttl_seconds is not None) and not (
        args.fact or args.observe
    ):
        parser.error("fact expiry options require at least one --fact or --observe")
    if args.fact_ttl_seconds is not None and args.fact_ttl_seconds < 0:
        parser.error("--fact-ttl-seconds must be non-negative")
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
            confidence=args.observe_confidence,
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

    if args.observe_repository_source:
        ingest_observation_source(
            ledger,
            args.workspace,
            RepositorySourceObservationSource(args.observe_repository_source),
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


def _state_projector_from_args(
    args: argparse.Namespace, ledger: EventLedger, *, measurement_history_limit: int = 1
) -> StateProjector:
    return StateProjector(
        ledger,
        measurement_history_limit=measurement_history_limit,
        predicate_catalog=PredicateCatalog.load(args.predicate_catalog),
        inference_catalog=InferenceCatalog.load(),
    )


def _can_use_state_cache(
    args: argparse.Namespace, *, measurement_history_limit: int = 1
) -> bool:
    """Return whether CLI projection can safely use the default state cache."""

    return (
        bool(args.db)
        and args.predicate_catalog is None
        and measurement_history_limit == 1
    )


def _projection_store_from_args(args: argparse.Namespace) -> ProjectionStore | None:
    """Return the configured projection cache store for CLI read-only paths."""

    if not args.db:
        return None
    return SQLiteProjectionStore(args.db)


def _load_or_build_fact_index_from_args(
    args: argparse.Namespace,
    state: State,
    *,
    status_consumer: ExecutionStatusConsumer | None = None,
) -> Any | None:
    """Return the shared fact index cache when the projection cache is eligible."""

    if not _can_use_state_cache(args):
        return None
    store = _projection_store_from_args(args)
    if store is None:
        return None
    try:
        return load_or_build_fact_index(
            state,
            workspace_id=args.workspace,
            store=store,
            status_consumer=status_consumer,
        )
    finally:
        close = getattr(store, "close", None)
        if close is not None:
            close()


def fact_query_state(
    args: argparse.Namespace,
    *,
    status_consumer: ExecutionStatusConsumer | None = None,
) -> State:
    """Seed requested dev state and return the projected State for fact queries."""

    ledger: EventLedger = SQLiteEventLedger(args.db) if args.db else EventLedger()
    store = _projection_store_from_args(args)
    try:
        seed_dev_state_from_args(args, ledger)
        history_limit = (
            max(1, len(ledger.list_events(args.workspace)))
            if getattr(args, "include_history", False)
            else 1
        )
        projector = _state_projector_from_args(
            args, ledger, measurement_history_limit=history_limit
        )
        if store is not None and _can_use_state_cache(
            args, measurement_history_limit=history_limit
        ):
            state, _status = project_state_with_cache(
                ledger,
                args.workspace,
                store,
                projector=projector,
                status_consumer=status_consumer,
            )
            return state
        return projector.project(args.workspace)
    finally:
        for resource in (store, ledger):
            close = getattr(resource, "close", None)
            if close is not None:
                close()


def projected_state_from_args(
    args: argparse.Namespace,
    *,
    status_consumer: ExecutionStatusConsumer | None = None,
) -> State:
    """Return persisted projected State without ingesting or executing anything."""

    ledger: EventLedger = SQLiteEventLedger(args.db) if args.db else EventLedger()
    store = _projection_store_from_args(args)
    try:
        projector = _state_projector_from_args(args, ledger)
        if store is not None and _can_use_state_cache(args):
            state, _status = project_state_with_cache(
                ledger,
                args.workspace,
                store,
                projector=projector,
                status_consumer=status_consumer,
            )
            return state
        return projector.project(args.workspace)
    finally:
        for resource in (store, ledger):
            close = getattr(resource, "close", None)
            if close is not None:
                close()


def projected_state_summary_from_args(
    args: argparse.Namespace,
    *,
    status_consumer: ExecutionStatusConsumer | None = None,
) -> tuple[StateSummary, dict[str, Any]]:
    """Return state-build accounting, using a dependent read-model cache."""

    ledger: EventLedger = SQLiteEventLedger(args.db) if args.db else EventLedger()
    store = _projection_store_from_args(args)
    try:
        latest_events = ledger.list_events(args.workspace)
        current_last_event_id = latest_events[-1].id if latest_events else None
        if store is not None and _can_use_state_cache(args):
            emit_status(
                status_consumer,
                "state_summary_cache_load",
                "Loading state-build cache...",
            )
            snapshot = store.load_summary_snapshot(
                args.workspace,
                STATE_SUMMARY_PROJECTION_NAME,
                STATE_SUMMARY_PROJECTION_VERSION,
                state_projection_version=STATE_PROJECTION_VERSION,
                state_last_event_id=current_last_event_id,
            )
            if snapshot is not None:
                emit_status(
                    status_consumer,
                    "state_summary_cache_load",
                    "State-build cache: hit",
                    completed=True,
                )
                payload = snapshot.summary_payload
                view_summary = StateSummary(**payload["state_view_summary"])
                operator_summary = dict(payload["operator_summary"])
                operator_summary.update(
                    {
                        "projection_version": view_summary.projection_version,
                        "last_event_id": view_summary.last_event_id,
                        "cache_status": "hit",
                        "state_build_cache_status": "hit",
                        "projection_cache_status": "hit",
                        "state_cache_status": "hit",
                    }
                )
                return view_summary, operator_summary

        if store is not None and _can_use_state_cache(args):
            emit_status(
                status_consumer,
                "state_summary_cache_load",
                "State-build cache: miss",
                completed=True,
            )
        projector = _state_projector_from_args(args, ledger)
        if store is not None and _can_use_state_cache(args):
            state, state_cache_status = project_state_with_cache(
                ledger,
                args.workspace,
                store,
                projector=projector,
                status_consumer=status_consumer,
            )
        else:
            state = projector.project(args.workspace)
        view_summary = build_state_summary(state)
        operator_summary = state_summary(state)
        if store is not None and _can_use_state_cache(args):
            cache_status = "hit" if state_cache_status.cache_hit else "miss"
        else:
            cache_status = "unavailable"
        operator_summary.update(
            {
                "projection_version": view_summary.projection_version,
                "last_event_id": view_summary.last_event_id,
                "cache_status": cache_status,
                "state_build_cache_status": "miss",
                "projection_cache_status": cache_status,
                "state_cache_status": cache_status,
            }
        )
        if store is not None and _can_use_state_cache(args):
            store.save_summary_snapshot(
                SummaryProjectionSnapshot(
                    workspace_id=args.workspace,
                    projection_name=STATE_SUMMARY_PROJECTION_NAME,
                    projection_version=STATE_SUMMARY_PROJECTION_VERSION,
                    last_event_id=state.last_event_id,
                    state_projection_version=STATE_PROJECTION_VERSION,
                    state_last_event_id=state.last_event_id,
                    summary_payload={
                        "state_view_summary": to_plain(view_summary),
                        "operator_summary": operator_summary,
                    },
                    created_at=datetime.now(timezone.utc),
                )
            )
        return view_summary, operator_summary
    finally:
        for resource in (store, ledger):
            close = getattr(resource, "close", None)
            if close is not None:
                close()


@dataclass(frozen=True)
class StateSummaryCacheDebugReport:
    cache_eligible: bool
    cache_ineligible_reason: str | None
    summary_cache_status: str
    state_cache_status: str
    current_last_event_id: str | None
    cached_summary_last_event_id: str | None
    cached_state_last_event_id: str | None
    timings: list[tuple[str, float]]
    projection_timings: list[tuple[str, float]]
    projection_counters: dict[str, int]
    notes: list[str]


def _format_cache_status_id(value: str | None) -> str:
    return value if value is not None else "none"


def state_summary_cache_debug_from_args(
    args: argparse.Namespace,
) -> StateSummaryCacheDebugReport:
    """Measure the state-build cache boundary without ingesting or executing tools."""

    timings: list[tuple[str, float]] = []
    notes: list[str] = []
    started = time.perf_counter()

    def timed(name: str, func):
        phase_started = time.perf_counter()
        try:
            return func()
        finally:
            timings.append((name, time.perf_counter() - phase_started))

    store = timed("projection store open", lambda: _projection_store_from_args(args))
    ledger: EventLedger = timed(
        "ledger open", lambda: SQLiteEventLedger(args.db) if args.db else EventLedger()
    )
    current_last_event_id: str | None = None
    cached_summary_last_event_id: str | None = None
    cached_state_last_event_id: str | None = None
    summary_cache_status = "unavailable"
    state_cache_status = "unavailable"
    cache_eligible = _can_use_state_cache(args)
    cache_ineligible_reason = None
    if not args.db:
        cache_ineligible_reason = "--db is required for persisted read-model caches"
    elif args.predicate_catalog is not None:
        cache_ineligible_reason = (
            "custom predicate catalog disables the default state cache"
        )

    try:
        latest_events = timed(
            "event listing / current last event lookup",
            lambda: ledger.list_events(args.workspace),
        )
        current_last_event_id = latest_events[-1].id if latest_events else None
        summary_snapshot = None
        state_snapshot = None
        if store is not None and cache_eligible:
            summary_snapshot = timed(
                "state summary snapshot lookup",
                lambda: store.load_summary_snapshot(
                    args.workspace,
                    STATE_SUMMARY_PROJECTION_NAME,
                    STATE_SUMMARY_PROJECTION_VERSION,
                    state_projection_version=STATE_PROJECTION_VERSION,
                    state_last_event_id=current_last_event_id,
                ),
            )
            summary_cache_status = "hit" if summary_snapshot is not None else "miss"
            if summary_snapshot is not None:
                cached_summary_last_event_id = summary_snapshot.last_event_id
                timed(
                    "state summary snapshot decode / payload reconstruction",
                    lambda: StateSummary(
                        **summary_snapshot.summary_payload["state_view_summary"]
                    ),
                )
                state_cache_status = "skipped"
                notes.append(
                    "state cache lookup skipped because the summary cache satisfied the request"
                )
                return StateSummaryCacheDebugReport(
                    cache_eligible,
                    cache_ineligible_reason,
                    summary_cache_status,
                    state_cache_status,
                    current_last_event_id,
                    cached_summary_last_event_id,
                    cached_state_last_event_id,
                    timings + [("total runtime", time.perf_counter() - started)],
                    [],
                    {},
                    notes,
                )
            state_snapshot = timed(
                "state cache lookup",
                lambda: store.load_snapshot(
                    args.workspace, STATE_PROJECTION_NAME, STATE_PROJECTION_VERSION
                ),
            )
            state_cache_status = (
                "hit"
                if state_snapshot is not None
                and state_snapshot.last_event_id == current_last_event_id
                else "miss"
            )
            if state_snapshot is not None:
                cached_state_last_event_id = state_snapshot.last_event_id
                timed(
                    "state snapshot decode / State reconstruction",
                    lambda: state_from_payload(state_snapshot.state_payload),
                )
        elif store is None:
            notes.append(
                "state and summary caches unavailable because no projection store was configured"
            )

        projector = timed(
            "state projector construction",
            lambda: _state_projector_from_args(args, ledger),
        )
        projection_diagnostics = ProjectionBuildDiagnostics()
        if store is not None and cache_eligible:
            state, _status = timed(
                "projection replay / build",
                lambda: project_state_with_cache(
                    ledger,
                    args.workspace,
                    store,
                    projector=projector,
                    status_consumer=None,
                    diagnostics=projection_diagnostics,
                ),
            )
        else:
            state = timed(
                "projection replay / build",
                lambda: projector.project(
                    args.workspace, diagnostics=projection_diagnostics
                ),
            )
        timed(
            "fact_support construction if separable", lambda: len(state.fact_supports)
        )
        view_summary = timed(
            "compact StateSummary derivation", lambda: build_state_summary(state)
        )
        operator_summary = timed(
            "operator state_summary derivation", lambda: state_summary(state)
        )
        if store is not None and cache_eligible:
            timed(
                "state summary snapshot save",
                lambda: store.save_summary_snapshot(
                    SummaryProjectionSnapshot(
                        workspace_id=args.workspace,
                        projection_name=STATE_SUMMARY_PROJECTION_NAME,
                        projection_version=STATE_SUMMARY_PROJECTION_VERSION,
                        last_event_id=state.last_event_id,
                        state_projection_version=STATE_PROJECTION_VERSION,
                        state_last_event_id=state.last_event_id,
                        summary_payload={
                            "state_view_summary": to_plain(view_summary),
                            "operator_summary": operator_summary,
                        },
                        created_at=datetime.now(timezone.utc),
                    )
                ),
            )
        timed(
            "rendering", lambda: format_state_summary_cache_debug_report_placeholder()
        )
        return StateSummaryCacheDebugReport(
            cache_eligible,
            cache_ineligible_reason,
            summary_cache_status,
            state_cache_status,
            current_last_event_id,
            cached_summary_last_event_id,
            cached_state_last_event_id,
            timings + [("total runtime", time.perf_counter() - started)],
            projection_diagnostics.timings,
            projection_diagnostics.counters,
            notes,
        )
    finally:
        for resource in (store, ledger):
            close = getattr(resource, "close", None)
            if close is not None:
                close()


def format_state_summary_cache_debug_report_placeholder() -> str:
    return ""


def format_state_summary_cache_debug_report(
    report: StateSummaryCacheDebugReport,
) -> str:
    lines = [
        "State Build Cache Debug",
        "",
        "Cache eligibility:",
        f"- status: {'eligible' if report.cache_eligible else 'ineligible'}",
    ]
    if report.cache_ineligible_reason:
        lines.append(f"- reason: {report.cache_ineligible_reason}")
    lines.extend(
        [
            "",
            "State-build cache:",
            f"- status: {report.summary_cache_status}",
            "",
            "Projection cache:",
            f"- status: {report.state_cache_status}",
            "",
            "Last event ids:",
            f"- current last event id: {_format_cache_status_id(report.current_last_event_id)}",
            f"- cached state-build last event id: {_format_cache_status_id(report.cached_summary_last_event_id)}",
            f"- cached projection last event id: {_format_cache_status_id(report.cached_state_last_event_id)}",
        ]
    )
    if report.notes:
        lines.extend(["", "Notes:", *[f"- {note}" for note in report.notes]])
    if report.projection_counters:
        lines.extend(["", "Projection/build structure counts:"])
        for name in sorted(report.projection_counters):
            lines.append(f"- {name}: {report.projection_counters[name]}")
    lines.extend(["", "Timings:"])
    lines.extend(f"- {name}: {elapsed:.6f}s" for name, elapsed in report.timings)
    if report.projection_timings:
        lines.extend(["", "Projection replay / build subphase timings:"])
        lines.extend(
            f"- {name}: {elapsed:.6f}s" for name, elapsed in report.projection_timings
        )
    return "\n".join(lines)


def rebuild_state_cache_from_args(args: argparse.Namespace) -> str:
    """Clear and rebuild the persisted State projection cache."""

    if not args.db:
        raise ValueError("--rebuild-state-cache requires --db")
    ledger = SQLiteEventLedger(args.db)
    store = _projection_store_from_args(args)
    if store is None:
        raise ValueError("--rebuild-state-cache requires --db")
    try:
        state, status = rebuild_state_cache(
            ledger,
            args.workspace,
            store,
            projector=_state_projector_from_args(args, ledger),
        )
        return (
            f"rebuilt state cache for workspace {args.workspace!r} "
            f"({len(state.facts)} facts, last_event_id={status.current_last_event_id or 'none'})"
        )
    finally:
        store.close()
        ledger.close()


def format_state_cache_status_from_args(args: argparse.Namespace) -> str:
    """Return a concise State projection cache status report."""

    if not args.db:
        return "state cache unavailable: --db is required"
    ledger = SQLiteEventLedger(args.db)
    store = _projection_store_from_args(args)
    if store is None:
        return "state cache unavailable: --db is required"
    try:
        events = ledger.list_events(args.workspace)
        latest_event = events[-1] if events else None
        current_last_event_id = latest_event.id if latest_event is not None else None
        snapshot = store.load_snapshot(
            args.workspace, STATE_PROJECTION_NAME, STATE_PROJECTION_VERSION
        )
        snapshot_last_event_id = (
            snapshot.last_event_id if snapshot is not None else None
        )
        cache_hit = (
            snapshot is not None and snapshot.last_event_id == current_last_event_id
        )
        return "\n".join(
            [
                f"cache: {'hit' if cache_hit else 'miss'}",
                f"projection_version: {STATE_PROJECTION_VERSION}",
                f"snapshot last_event_id: {snapshot_last_event_id or 'none'}",
                f"current last_event_id: {current_last_event_id or 'none'}",
            ]
        )
    finally:
        store.close()
        ledger.close()


def _canonical_entities(state: State, entities: Any) -> list[str]:
    """Return deterministic canonical entity names from an iterable."""

    return sorted({state.alias_resolver.canonical(entity) for entity in entities})


def format_entity_impact(state: State, entity: str) -> str:
    """Format a concise entity impact view using only projected State."""

    canonical = state.alias_resolver.canonical(entity)
    resolved = state.alias_resolver.resolve(entity) | {canonical}

    entity_types = state.get_current_entity_types(canonical)
    if entity_types == ["unknown"]:
        entity_types = sorted(
            {
                entity_type
                for name in resolved
                for entity_type in state.get_current_entity_types(name)
                if entity_type != "unknown"
            }
        ) or ["unknown"]
    aliases = [fact.value for fact in state.get_current_facts(canonical, "alias")]
    if not aliases:
        aliases = [
            name
            for name in sorted(resolved - {canonical})
            if not _looks_like_plain_ip_address(name)
        ]

    identity_predicates = ["hostname", "machine_id", "boot_id", "fqdn"]
    identity_facts = [
        fact
        for predicate in identity_predicates
        for fact in state.get_current_facts(canonical, predicate)
    ]
    availability = state.get_best_fact(canonical, "availability_status")
    local_observation = state.get_best_fact(canonical, "local_observation_status")
    endpoint_availability: dict[str, list[tuple[str, str]]] = {}
    for endpoint in sorted(resolved):
        if "endpoint" not in state.get_current_entity_types(endpoint):
            continue
        endpoint_status = state.get_best_fact(endpoint, "availability_status")
        if endpoint_status is None:
            continue
        roles = state.get_current_facts(endpoint, "endpoint_role")
        role_names = [str(role.value) for role in roles] or [endpoint]
        for role in role_names:
            endpoint_availability.setdefault(role, []).append(
                (endpoint, _format_fact_value(endpoint_status.value))
            )
    groups = _canonical_entities(
        state,
        (
            edge.object
            for edge in state.relationships
            if edge.relationship == "member_of" and edge.subject in resolved
        ),
    )
    dependencies = _canonical_entities(
        state,
        (
            dependency
            for name in sorted(resolved)
            for dependency in state.find_dependencies(name)
        ),
    )
    dependents = _canonical_entities(
        state,
        (
            dependent
            for name in sorted(resolved)
            for dependent in state.find_dependents(name)
        ),
    )
    dependencies = [name for name in dependencies if name != canonical]
    dependents = [name for name in dependents if name != canonical]

    conflicts = [
        conflict
        for conflict in state.get_fact_conflicts()
        if state.alias_resolver.canonical(conflict.subject) == canonical
    ]
    issues = [
        issue
        for issue in state.get_graph_issues()
        if issue.subject in resolved or issue.object in resolved
    ]

    mount_predicates = [
        "mount_point",
        "filesystem_type",
        "mounted_device",
        "mount_option",
    ]
    mount_facts = [
        fact
        for predicate in mount_predicates
        for fact in state.get_current_facts(canonical, predicate)
    ]

    storage_predicates = [
        "block_device",
        "partition",
        "block_device_size_bytes",
        "block_device_rotational",
        "block_device_removable",
        "block_device_model",
        "block_device_vendor",
        "block_device_parent",
    ]
    storage_facts = [
        fact
        for predicate in storage_predicates
        for fact in state.get_current_facts(canonical, predicate)
    ]

    listener_predicates = [
        "listening_endpoint",
        "listening_protocol",
        "listening_address",
        "listening_port",
    ]
    listener_facts = [
        fact
        for predicate in listener_predicates
        for fact in state.get_current_facts(canonical, predicate)
    ]

    network_predicates = [
        "network_interface",
        "interface_role",
        "interface_operstate",
        "interface_mac_address",
        "interface_mtu",
        "ip_address",
        "address_assignment_method",
        "default_gateway",
        "dns_resolver",
        "dns_resolver_stub",
        "dns_resolver_upstream",
    ]
    network_facts = [
        fact
        for predicate in network_predicates
        for fact in state.get_current_facts(canonical, predicate)
    ]

    lines = [
        f"entity: {canonical}",
        f"entity types: {', '.join(entity_types)}",
        "aliases:",
        "identity:",
        "availability_status: "
        + (
            _format_fact_value(availability.value)
            if availability is not None
            else "unknown"
        ),
        "local_observation_status: "
        + (
            _format_fact_value(local_observation.value)
            if local_observation is not None
            else "unknown"
        ),
        "local network configuration:",
        "mounts:",
        "storage topology:",
        "listening endpoints:",
        "endpoint availability by role:",
        f"groups/member_of: {', '.join(groups) if groups else 'none'}",
        f"dependencies: {', '.join(dependencies) if dependencies else 'none'}",
        f"dependents: {', '.join(dependents) if dependents else 'none'}",
        "active conflicts:",
    ]
    alias_lines = [f"- {_format_fact_value(alias)}" for alias in aliases] or ["- none"]
    lines[3:3] = alias_lines
    identity_lines = _format_identity_impact(identity_facts)
    identity_heading = lines.index("identity:")
    lines[identity_heading + 1 : identity_heading + 1] = identity_lines or ["- none"]
    network_lines = _format_local_network_impact(network_facts)
    network_heading = lines.index("local network configuration:")
    lines[network_heading + 1 : network_heading + 1] = network_lines or ["- none"]
    mount_lines = _format_mount_impact(mount_facts)
    mount_heading = lines.index("mounts:")
    lines[mount_heading + 1 : mount_heading + 1] = mount_lines or ["- none"]
    storage_lines = _format_storage_topology_impact(storage_facts, mount_facts)
    storage_heading = lines.index("storage topology:")
    lines[storage_heading + 1 : storage_heading + 1] = storage_lines or ["- none"]
    listener_lines = _format_listening_endpoint_impact(listener_facts)
    listener_heading = lines.index("listening endpoints:")
    lines[listener_heading + 1 : listener_heading + 1] = listener_lines or ["- none"]

    endpoint_lines = []
    for role, statuses in sorted(endpoint_availability.items()):
        values = sorted({status for _, status in statuses})
        endpoints = ", ".join(endpoint for endpoint, _ in statuses)
        endpoint_lines.append(f"- {role}: {', '.join(values)} ({endpoints})")
    endpoint_heading = lines.index("endpoint availability by role:")
    lines[endpoint_heading + 1 : endpoint_heading + 1] = endpoint_lines or ["- none"]
    if conflicts:
        for conflict in conflicts:
            winning = (
                _format_fact_value(conflict.winning_value)
                if conflict.winning_value is not None
                else "none"
            )
            lines.append(
                f"- {conflict.predicate}: values="
                + ", ".join(_format_fact_value(value) for value in conflict.values)
                + f"; winning={winning}"
            )
    else:
        lines.append("- none")

    lines.append("graph issues:")
    if issues:
        for issue in issues:
            lines.extend(_format_graph_issue_summary(issue))
    else:
        lines.append("- none")
    return "\n".join(lines)


def _fact_listener_endpoint(fact: Fact) -> str | None:
    if fact.predicate == "listening_endpoint":
        return _format_fact_value(fact.value)
    protocol = fact.dimensions.get("protocol")
    address = fact.dimensions.get("address")
    port = fact.dimensions.get("port")
    if protocol is None or address is None or port is None:
        return None
    formatted_address = str(address)
    if ":" in formatted_address and not formatted_address.startswith("["):
        formatted_address = f"[{formatted_address}]"
    return f"{protocol} {formatted_address}:{port}"


def _format_listening_endpoint_impact(listener_facts: list[Fact]) -> list[str]:
    """Format listener topology without asserting service health or ownership."""

    if not listener_facts:
        return ["- none"]
    endpoints = sorted(
        dict.fromkeys(
            endpoint
            for fact in _sort_facts_for_display(listener_facts)
            if (endpoint := _fact_listener_endpoint(fact)) is not None
        )
    )
    lines = [f"- {endpoint}" for endpoint in endpoints]
    lines.append(
        "- availability/reachability/health/ownership: not inferred from listener facts"
    )
    return lines or ["- none"]


def _fact_mount_point(fact: Fact) -> str | None:
    """Return the mount_point dimension for mount facts when present."""

    mount_point = fact.dimensions.get("mount_point")
    if mount_point is None:
        return None
    return str(mount_point)


def _unique_mount_values(
    predicates: dict[str, list[Fact]], predicate: str
) -> list[str]:
    """Return deterministic unique mount fact values for CLI rendering."""

    return list(
        dict.fromkeys(
            _format_fact_value(fact.value)
            for fact in _sort_facts_for_display(predicates.get(predicate, []))
        )
    )


def _format_mount_impact(mount_facts: list[Fact]) -> list[str]:
    """Format mount facts for operators without asserting health or availability."""

    if not mount_facts:
        return ["- none"]

    by_mount: dict[str, dict[str, list[Fact]]] = defaultdict(lambda: defaultdict(list))
    for fact in mount_facts:
        mount_point = _fact_mount_point(fact)
        if mount_point is None and fact.predicate == "mount_point":
            mount_point = _format_fact_value(fact.value)
        if mount_point is None:
            continue
        by_mount[mount_point][fact.predicate].append(fact)

    visible_mounts: list[
        tuple[str, dict[str, list[Fact]], list[str], list[str], list[str]]
    ] = []
    collapsed_counts: Counter[str] = Counter()
    for mount_point, predicates in sorted(by_mount.items()):
        devices = _unique_mount_values(predicates, "mounted_device")
        fs_types = _unique_mount_values(predicates, "filesystem_type")
        options = _unique_mount_values(predicates, "mount_option")
        collapse_group = classify_mount_collapse_group(mount_point, devices, fs_types)
        if collapse_group is None:
            visible_mounts.append((mount_point, predicates, devices, fs_types, options))
        else:
            collapsed_counts[collapse_group] += 1

    lines: list[str] = []
    for mount_point, _predicates, devices, fs_types, options in sorted(
        visible_mounts, key=lambda item: mount_display_priority(item[0], item[3])
    ):
        summary = f"- {mount_point}:"
        if devices:
            summary += f" device={', '.join(devices)}"
        if fs_types:
            summary += f" type={', '.join(fs_types)}"
        lines.append(summary)
        if options:
            lines.append("  options: " + ", ".join(options))

    for group in MOUNT_COLLAPSE_GROUP_ORDER:
        if collapsed_counts[group]:
            lines.append(f"- {group}: {collapsed_counts[group]} collapsed")
    lines.append("- full mount evidence: use --current-facts")
    lines.append("- health/availability/reachability: not inferred from mount facts")
    return lines


def _fact_storage_device(fact: Fact) -> str | None:
    """Return the storage device dimension for a fact when present."""

    device = fact.dimensions.get("device")
    if device is None:
        return None
    return str(device)


def _format_storage_topology_impact(
    storage_facts: list[Fact], mount_facts: list[Fact]
) -> list[str]:
    """Format storage topology without asserting health or availability."""

    if not storage_facts:
        return ["- none"]

    by_predicate: dict[str, list[Fact]] = defaultdict(list)
    for fact in storage_facts:
        by_predicate[fact.predicate].append(fact)

    devices = sorted(
        dict.fromkeys(
            _format_fact_value(fact.value)
            for fact in _sort_facts_for_display(by_predicate.get("block_device", []))
        )
    )
    partitions = sorted(
        dict.fromkeys(
            _format_fact_value(fact.value)
            for fact in _sort_facts_for_display(by_predicate.get("partition", []))
        )
    )

    mounted_devices: dict[str, list[str]] = defaultdict(list)
    for fact in mount_facts:
        if fact.predicate != "mounted_device":
            continue
        mount_point = _fact_mount_point(fact)
        if mount_point is None:
            continue
        mounted_devices[_format_fact_value(fact.value)].append(mount_point)

    lines: list[str] = ["- devices:"]
    (
        lines.extend(f"  - {device}" for device in devices)
        if devices
        else lines.append("  - none")
    )
    lines.append("- partitions:")
    (
        lines.extend(f"  - {partition}" for partition in partitions)
        if partitions
        else lines.append("  - none")
    )
    relationships = []
    for fact in _sort_facts_for_display(by_predicate.get("block_device_parent", [])):
        child = _fact_storage_device(fact)
        if child is None:
            continue
        relationships.append(f"{child} -> {_format_fact_value(fact.value)}")
    if relationships:
        lines.append("- parent relationships:")
        lines.extend(
            f"  - {relationship}"
            for relationship in sorted(dict.fromkeys(relationships))
        )

    mount_relationships = []
    known_storage_paths = {f"/dev/{name}" for name in devices + partitions}
    for mounted_device, mount_points in mounted_devices.items():
        if mounted_device not in known_storage_paths:
            continue
        for mount_point in sorted(dict.fromkeys(mount_points)):
            mount_relationships.append(f"{mounted_device} -> {mount_point}")
    lines.append("- mount relationships:")
    if mount_relationships:
        lines.extend(
            f"  - {relationship}"
            for relationship in sorted(dict.fromkeys(mount_relationships))
        )
    else:
        lines.append("  - none")
    lines.append(
        "- health/availability/filesystem-health: not inferred from storage facts"
    )
    return lines


def _format_identity_impact(identity_facts: list[Fact]) -> list[str]:
    """Format host identity facts without implying availability or reachability."""

    if not identity_facts:
        return ["- none"]
    by_predicate: dict[str, list[Fact]] = defaultdict(list)
    for fact in identity_facts:
        by_predicate[fact.predicate].append(fact)
    lines: list[str] = []
    for predicate in ("hostname", "machine_id", "boot_id", "fqdn"):
        facts = _sort_facts_for_display(by_predicate.get(predicate, []))
        for fact in facts:
            lines.append(f"- {predicate}: {_format_fact_value(fact.value)}")
    lines.append("- availability/reachability: not inferred from identity facts")
    return lines


def _fact_interface(fact: Fact) -> str | None:
    """Return the interface dimension for a fact when present."""

    interface = fact.dimensions.get("interface")
    if interface is None:
        return None
    return str(interface)


def _network_interface_role(
    interface: str,
    role_facts: dict[str, list[Fact]],
    default_interfaces: set[str],
) -> str:
    """Return a display role without asserting reachability or availability."""

    if interface in default_interfaces:
        return "primary"
    roles = [str(fact.value) for fact in role_facts.get(interface, [])]
    if roles:
        role_priority = {
            "primary": 0,
            "loopback": 1,
            "secondary": 2,
            "container": 3,
            "virtual": 4,
            "vpn": 5,
        }
        return sorted(roles, key=lambda role: (role_priority.get(role, 99), role))[0]
    if interface == "lo":
        return "loopback"
    lowered = interface.lower()
    if lowered.startswith(("tailscale", "wg")):
        return "vpn"
    if lowered.startswith(("docker", "br-", "veth")):
        return "container"
    if lowered.startswith("virbr"):
        return "virtual"
    return "secondary"


def _format_local_network_impact(network_facts: list[Fact]) -> list[str]:
    """Format local network facts for impact output without hiding stored facts."""

    if not network_facts:
        return ["- none"]

    by_predicate: dict[str, list[Fact]] = defaultdict(list)
    for fact in network_facts:
        by_predicate[fact.predicate].append(fact)

    interfaces = {
        str(fact.value)
        for fact in by_predicate.get("network_interface", [])
        if str(fact.value)
    }
    for predicate in (
        "interface_role",
        "interface_operstate",
        "interface_mac_address",
        "interface_mtu",
        "ip_address",
        "address_assignment_method",
        "default_gateway",
    ):
        for fact in by_predicate.get(predicate, []):
            interface = _fact_interface(fact)
            if interface:
                interfaces.add(interface)

    role_facts: dict[str, list[Fact]] = defaultdict(list)
    gateway_by_interface: dict[str, list[str]] = defaultdict(list)
    ip_by_interface: dict[str, list[Fact]] = defaultdict(list)
    assignment_by_interface: dict[str, list[str]] = defaultdict(list)
    for fact in by_predicate.get("interface_role", []):
        interface = _fact_interface(fact)
        if interface:
            role_facts[interface].append(fact)
    for fact in by_predicate.get("default_gateway", []):
        interface = _fact_interface(fact)
        if interface:
            gateway_by_interface[interface].append(_format_fact_value(fact.value))
    for fact in by_predicate.get("ip_address", []):
        interface = _fact_interface(fact)
        if interface:
            ip_by_interface[interface].append(fact)
    for fact in by_predicate.get("address_assignment_method", []):
        interface = _fact_interface(fact)
        if interface:
            assignment_by_interface[interface].append(_format_fact_value(fact.value))

    default_interfaces = set(gateway_by_interface)
    roles = {
        interface: _network_interface_role(interface, role_facts, default_interfaces)
        for interface in interfaces
    }
    collapsed_roles = {"container", "virtual", "vpn"}
    collapsed = sorted(
        interface for interface, role in roles.items() if role in collapsed_roles
    )
    visible = sorted(
        interface for interface in interfaces if interface not in collapsed
    )
    role_priority = {"primary": 0, "loopback": 1, "secondary": 2}
    visible.sort(
        key=lambda interface: (role_priority.get(roles[interface], 50), interface)
    )

    lines: list[str] = []
    for interface in visible:
        role = roles[interface]
        label = (
            "primary/default-route interface"
            if role == "primary"
            else f"{role} interface"
        )
        address_groups = _group_interface_addresses(ip_by_interface.get(interface, []))
        gateways = sorted(dict.fromkeys(gateway_by_interface.get(interface, [])))
        assignments = sorted(dict.fromkeys(assignment_by_interface.get(interface, [])))
        lines.append(f"- {label} {interface}:")
        for address_label in ("ipv4", "ipv6_global", "ipv6_link_local"):
            values = address_groups.get(address_label, [])
            if not values:
                continue
            if len(values) == 1:
                lines.append(f"  {address_label}: {values[0]}")
            else:
                lines.append(f"  {address_label}:")
                lines.extend(f"  - {value}" for value in values)
        if gateways:
            lines.append("  default_gateway_ipv4: " + ", ".join(gateways))
        if assignments:
            lines.append("  address_assignment_method: " + ", ".join(assignments))

    if collapsed:
        counts = Counter(roles[interface] for interface in collapsed)
        count_text = ", ".join(f"{role}={counts[role]}" for role in sorted(counts))
        lines.append(
            f"- virtual/container/vpn interfaces: {len(collapsed)} collapsed ({count_text}); "
            "use --current-facts for full local facts"
        )

    dns_resolver_lines = _format_dns_resolver_impact_lines(by_predicate)
    lines.extend(dns_resolver_lines)
    lines.append("- reachability/availability: not inferred from local network facts")
    return lines or ["- none"]


def _looks_like_plain_ip_address(value: Any) -> bool:
    """Return whether a value is a bare IPv4/IPv6 address, not an identity alias."""

    try:
        ipaddress.ip_address(str(value))
    except ValueError:
        return False
    return True


def _address_group_for_fact(fact: Fact) -> str | None:
    """Classify an interface address for readable impact formatting."""

    value = _format_fact_value(fact.value)
    family = str(fact.dimensions.get("address_family", "")).lower()
    try:
        address = ipaddress.ip_address(value)
    except ValueError:
        if family == "ipv4":
            return "ipv4"
        if family == "ipv6":
            return "ipv6_global"
        return None
    if address.version == 4:
        return "ipv4"
    if address.version == 6 and address.is_link_local:
        return "ipv6_link_local"
    if address.version == 6:
        return "ipv6_global"
    return None


def _group_interface_addresses(facts: list[Fact]) -> dict[str, list[str]]:
    """Group interface addresses without changing the stored facts."""

    grouped: dict[str, list[str]] = defaultdict(list)
    for fact in facts:
        group = _address_group_for_fact(fact)
        if group is None:
            continue
        grouped[group].append(_format_fact_value(fact.value))
    return {key: sorted(dict.fromkeys(values)) for key, values in grouped.items()}


def _sort_facts_for_display(facts: list[Fact]) -> list[Fact]:
    return sorted(
        facts,
        key=lambda fact: (
            json.dumps(fact.dimensions, sort_keys=True),
            _format_fact_value(fact.value),
            fact.id,
        ),
    )


def _format_dns_resolver_impact_lines(by_predicate: dict[str, list[Fact]]) -> list[str]:
    """Format configured DNS facts without implying resolver reachability."""

    lines: list[str] = []
    stub_facts = _sort_facts_for_display(by_predicate.get("dns_resolver_stub", []))
    upstream_facts = _sort_facts_for_display(
        by_predicate.get("dns_resolver_upstream", [])
    )
    if stub_facts:
        for fact in stub_facts:
            lines.append(f"- dns_resolver_stub: {_format_fact_value(fact.value)}")
        if not upstream_facts:
            lines.append("- dns_resolver_upstream: unknown")
    if upstream_facts:
        values = [_format_fact_value(fact.value) for fact in upstream_facts]
        if len(values) == 1:
            lines.append(f"- dns_resolver_upstream: {values[0]}")
        else:
            lines.append("- dns_resolver_upstream:")
            lines.extend(f"  - {value}" for value in values)
    if not stub_facts and not upstream_facts:
        for fact in _sort_facts_for_display(by_predicate.get("dns_resolver", [])):
            lines.append(
                f"- {fact.predicate}{_format_fact_dimensions(fact.dimensions)}: "
                f"{_format_fact_value(fact.value)}"
            )
    return lines


def _format_fact_dimension_pairs(dimensions: dict[str, str]) -> str:
    """Format fact dimensions as deterministic key=value pairs."""

    return ", ".join(f"{key}={dimensions[key]}" for key in sorted(dimensions))


def _format_fact_dimensions(dimensions: dict[str, str]) -> str:
    """Format fact dimensions for compact deterministic CLI output."""

    if not dimensions:
        return ""
    return f" ({_format_fact_dimension_pairs(dimensions)})"


def _format_graph_issue_summary(issue: Any) -> list[str]:
    """Format one graph issue compactly, including actionable guidance."""

    lines = [
        f"- {issue.severity}: {issue.subject} {issue.relationship} "
        f"{issue.object}; {issue.reason}"
    ]
    if issue.hint:
        lines.append(f"  hint: {issue.hint}")
    return lines


def format_unhealthy(state: State, *, include_warnings: bool = False) -> str:
    """Format current down endpoints and graph issues from projected State only."""

    endpoints_by_host: dict[str, list[tuple[str, str]]] = defaultdict(list)
    endpoint_subjects = sorted(
        {
            fact.subject_id
            for fact in state.facts.values()
            if fact.predicate == "availability_status"
        }
    )
    for endpoint in endpoint_subjects:
        if "endpoint" not in state.get_current_entity_types(endpoint):
            continue
        availability = state.get_best_fact(endpoint, "availability_status")
        if availability is None or availability.value != "down":
            continue
        roles = state.get_current_facts(endpoint, "endpoint_role")
        role_names = sorted({str(role.value) for role in roles}) or ["endpoint"]
        host = state.alias_resolver.canonical(endpoint)
        for role in role_names:
            endpoints_by_host[host].append((role, endpoint))

    lines = ["unhealthy endpoints:"]
    if endpoints_by_host:
        for host, endpoints in sorted(endpoints_by_host.items()):
            lines.append(f"{host}:")
            for role, endpoint in sorted(endpoints):
                lines.append(f"  - {role} down {endpoint}")
    else:
        lines.append("- none")

    lines.append("graph errors:")
    errors = state.get_graph_issues("error")
    if errors:
        for issue in errors:
            lines.extend(_format_graph_issue_summary(issue))
    else:
        lines.append("- none")

    if include_warnings:
        lines.append("graph warnings:")
        warnings = state.get_graph_issues("warning")
        if warnings:
            for issue in warnings:
                lines.extend(_format_graph_issue_summary(issue))
        else:
            lines.append("- none")

    return "\n".join(lines)


def format_relationships(state: State, args: argparse.Namespace) -> str:
    """Format filtered projected topology edges for terminal inspection."""

    relationships = state.get_relationships(
        subject=args.relationship_subject,
        relationship=args.relationship,
        object=args.relationship_object,
    )
    return (
        "\n".join(
            f"{edge.subject} {edge.relationship} {edge.object}"
            for edge in relationships
        )
        or "no relationships"
    )


def format_graph_issue_summary(
    state: State, *, category_limit: int = 10, examples_per_category: int = 3
) -> str:
    """Format a grouped read-only orientation summary for graph issues."""

    issues = state.get_graph_issues()
    total = len(issues)
    warning_count = sum(1 for issue in issues if issue.severity == "warning")
    error_count = sum(1 for issue in issues if issue.severity == "error")
    by_severity = Counter(issue.severity for issue in issues)
    grouped: dict[tuple[str, str, str], list[Any]] = defaultdict(list)
    for issue in issues:
        grouped[(issue.severity, issue.relationship, issue.reason)].append(issue)

    sorted_groups = sorted(
        grouped.items(),
        key=lambda item: (
            -len(item[1]),
            item[0][0],
            item[0][1],
            item[0][2],
        ),
    )[:category_limit]

    lines = [
        "Graph Issue Summary",
        "",
        "Totals:",
        f"- warnings: {warning_count}",
        f"- errors: {error_count}",
        f"- total: {total}",
        "",
        "By severity:",
        f"- warning: {by_severity.get('warning', 0)}",
        f"- error: {by_severity.get('error', 0)}",
        "",
        "Top categories:",
    ]
    if not sorted_groups:
        lines.append("- none")
    else:
        for (severity, relationship, reason), category_issues in sorted_groups:
            percent = (len(category_issues) / total * 100) if total else 0.0
            lines.append(
                f"- {severity} | {relationship} | {reason}: "
                f"{len(category_issues)} ({percent:.1f}% of total)"
            )

    lines.extend(["", "Representative examples:"])
    if not sorted_groups:
        lines.append("- none")
    else:
        for (severity, relationship, reason), category_issues in sorted_groups:
            lines.append(f"- {severity} | {relationship} | {reason}")
            examples = sorted(
                category_issues,
                key=lambda issue: (issue.subject, issue.object, issue.id),
            )[:examples_per_category]
            if not examples:
                lines.append("  - none")
                continue
            for issue in examples:
                lines.append(
                    f"  - {issue.subject} {issue.relationship} {issue.object}; "
                    f"reason: {issue.reason}"
                )
                lines.append(
                    "    subject types: "
                    f"expected={','.join(issue.expected_subject_types) or 'none'} "
                    f"actual={','.join(issue.actual_subject_types) or 'none'}"
                )
                lines.append(
                    "    object types: "
                    f"expected={','.join(issue.expected_object_types) or 'none'} "
                    f"actual={','.join(issue.actual_object_types) or 'none'}"
                )
                lines.append(
                    "    counts: "
                    f"source_facts={len(issue.source_fact_ids)} "
                    f"relationships={len(issue.relationship_ids)}"
                )
    return "\n".join(lines)


def format_graph_issues(
    state: State, severity: Literal["warning", "error"] | None = None
) -> str:
    """Format projected graph validation issues for terminal inspection."""

    issues = state.get_graph_issues(severity)
    if not issues:
        return f"no {severity + ' ' if severity else ''}graph issues"
    sections = []
    for issue in issues:
        sections.append(
            "\n".join(
                [
                    f"{issue.severity}: {issue.subject} {issue.relationship} {issue.object}",
                    f"relationship_ids: {','.join(issue.relationship_ids)}",
                    f"source_fact_ids: {','.join(issue.source_fact_ids)}",
                    f"reason: {issue.reason}",
                    *([f"hint: {issue.hint}"] if issue.hint else []),
                    "subject types: "
                    f"expected={','.join(issue.expected_subject_types)} "
                    f"actual={','.join(issue.actual_subject_types)}",
                    "object types: "
                    f"expected={','.join(issue.expected_object_types)} "
                    f"actual={','.join(issue.actual_object_types)}",
                ]
            )
        )
    return "\n\n".join(sections)


def format_entity_types(state: State, entity_id: str | None = None) -> str:
    """Format current entity classifications and their supporting assertions."""

    entity_ids = (
        [entity_id] if entity_id is not None else sorted(state.current_entity_types)
    )
    lines: list[str] = []
    for current_entity_id in entity_ids:
        current_types = state.get_current_entity_types(current_entity_id)
        label = ", ".join(current_types)
        if len(current_types) > 1:
            label += " (ambiguous)"
        lines.append(f"{current_entity_id}: {label}")
        for assertion in state.get_entity_type_assertions(current_entity_id):
            if assertion.entity_type == "unknown" and current_types != ["unknown"]:
                continue
            source_id = (
                assertion.source_fact_id
                or assertion.source_relationship_id
                or "projection"
            )
            lines.append(
                f"  - {assertion.entity_type} confidence={assertion.confidence:g} "
                f"source={assertion.source}:{source_id} reason={assertion.reason}"
            )
    return "\n".join(lines) or "no entity types"


def record_classification_coverage_diagnostic(
    args: argparse.Namespace, diagnostic: Any
) -> list[Fact]:
    """Append classification coverage diagnostic facts via observations."""

    diagnostic_run_subject = f"diagnostic_run:{new_id('diagnostic_run')}"
    observations = [
        DevObservationSeed(
            subject=diagnostic_run_subject,
            predicate=_diagnostic_fact_predicate(name),
            value=value,
            source_type="inferred",
            confidence=1.0,
            ingested_by="scripts.seed_local --classification-coverage --record",
        )
        for name, value in diagnostic.record_facts().items()
    ]
    ledger: EventLedger = SQLiteEventLedger(args.db) if args.db else EventLedger()
    return ingest_observations(
        ledger, args.workspace, observations, session_id=args.session
    )


def record_ownership_discrepancy_capability_needs(
    args: argparse.Namespace, rows: list[Any]
) -> list[Fact]:
    """Append ownership discrepancy capability needs as diagnostic facts."""

    diagnostic_run_subject = f"diagnostic_run:{new_id('diagnostic_run')}"
    observations: list[DevObservationSeed] = [
        DevObservationSeed(
            subject=diagnostic_run_subject,
            predicate="diagnostic_name",
            value="ownership_discrepancies",
            source_type="inferred",
            confidence=1.0,
            ingested_by="scripts.seed_local --ownership-discrepancies --record",
        )
    ]
    for row in rows:
        for record in diagnostic_capability_need_records(row):
            observations.append(
                DevObservationSeed(
                    subject=diagnostic_run_subject,
                    predicate="diagnostic_capability_need",
                    value=record,
                    source_type="inferred",
                    confidence=1.0,
                    ingested_by="scripts.seed_local --ownership-discrepancies --record",
                )
            )
            for name, value in record.items():
                observations.append(
                    DevObservationSeed(
                        subject=diagnostic_run_subject,
                        predicate=_diagnostic_fact_predicate(name),
                        value=value,
                        source_type="inferred",
                        confidence=1.0,
                        ingested_by="scripts.seed_local --ownership-discrepancies --record",
                    )
                )
    ledger: EventLedger = SQLiteEventLedger(args.db) if args.db else EventLedger()
    return ingest_observations(
        ledger, args.workspace, observations, session_id=args.session
    )


def _diagnostic_fact_predicate(name: str) -> str:
    return name.replace("-", " ").replace(" ", "_")


def format_evidence_graph(state: State) -> str:
    """Format the read-only Evidence Graph summary and concise links."""

    summary = build_evidence_summary(state)
    graph = build_evidence_graph(state)
    lines = [
        "Evidence Summary",
        "",
        f"Evidence Nodes: {summary.evidence_count}",
        f"Linked Facts: {summary.linked_fact_count}",
        f"Unsupported Facts: {summary.unsupported_fact_count}",
        f"Average Confidence: {summary.average_confidence:.2f}",
        "",
        f"Projection Version: {summary.projection_version}",
        f"Last Event: {summary.last_event_id or 'none'}",
        "",
        "Evidence",
        "",
    ]
    if not graph.evidence_links:
        lines.append("(none)")
        return "\n".join(lines)
    facts_by_id = {view.fact_id: view for view in graph.fact_evidence}
    nodes_by_id = {node.evidence_id: node for node in graph.evidence_nodes}
    for link in graph.evidence_links:
        fact = facts_by_id.get(link.target_fact_id)
        node = nodes_by_id.get(link.source_evidence_id)
        if fact is None or node is None:
            continue
        source = node.source_event_id or node.evidence_id
        lines.append(
            f"* {node.evidence_type} event {source}: {node.summary} -> "
            f"{fact.subject} {fact.predicate} {_format_view_value(fact.object)}"
        )
    return "\n".join(lines)


def format_why_fact(
    views: list[FactEvidenceView],
    subject: str,
    predicate: str,
    object_value: str | None,
) -> str:
    """Format evidence explanation for a fact query."""

    if not views:
        query = f"{subject} {predicate}" + (f" {object_value}" if object_value else "")
        return "\n".join(["Fact", "", f"No matching fact found for {query}."])
    view = views[0]
    lines = [
        "Fact",
        "",
        f"{view.subject} {view.predicate} {_format_view_value(view.object)}",
        f"confidence: {view.confidence:.2f}",
        "",
        "Explanation",
        "",
        view.explanation,
        "",
        "Evidence",
        "",
    ]
    if view.evidence:
        for node in view.evidence:
            source = node.source_event_id or node.evidence_id
            lines.append(f"* {node.evidence_type} event {source}: {node.summary}")
    else:
        lines.append("(none)")
    lines.extend(["", "Supporting Event IDs", ""])
    if view.supporting_event_ids:
        lines.extend(f"* {event_id}" for event_id in view.supporting_event_ids)
    else:
        lines.append("(none)")
    return "\n".join(lines)


def format_unsupported_facts(views: list[FactEvidenceView]) -> str:
    lines = ["Unsupported Facts", ""]
    if not views:
        lines.append("(none)")
        return "\n".join(lines)
    lines.extend(
        f"* {view.subject} {view.predicate} {_format_view_value(view.object)}"
        for view in views
    )
    return "\n".join(lines)


def format_contradictions(state: State, contradictions: list[Contradiction]) -> str:
    """Format the read-only Contradiction Detection view."""

    summary = build_contradiction_summary(state, contradictions)
    lines = [
        "Contradictions",
        "",
        f"Count: {summary.contradiction_count}",
        f"Affected Facts: {summary.affected_fact_count}",
        f"High Severity: {summary.high_severity_count}",
        f"Medium Severity: {summary.medium_severity_count}",
        f"Low Severity: {summary.low_severity_count}",
        "",
        f"Projection Version: {summary.projection_version}",
        f"Last Event: {summary.last_event_id or 'none'}",
        "",
    ]
    if not contradictions:
        lines.append("(none)")
        return "\n".join(lines)

    facts_by_id = state.facts
    for contradiction in contradictions:
        lines.append(f"* {contradiction.subject} {contradiction.predicate}")
        lines.append(f"  severity: {contradiction.severity}")
        lines.append(f"  reason: {contradiction.reason}")
        lines.append(
            "  values: "
            + ", ".join(_format_view_value(value) for value in contradiction.values)
        )
        lines.append("  facts:")
        for fact_id in contradiction.fact_ids:
            fact = facts_by_id.get(fact_id)
            if fact is None:
                lines.append(f"  {fact_id}: (missing from projected State)")
                continue
            lines.append(
                f"  {fact_id}: {fact.subject_id} {fact.predicate} "
                f"{_format_view_value(fact.value)}"
            )
            evidence_view = contradiction.evidence_by_fact_id.get(fact_id)
            if evidence_view is None or not evidence_view.evidence:
                lines.append("    evidence: none")
            else:
                evidence_bits = []
                for node in evidence_view.evidence:
                    source = node.source_event_id or node.evidence_id
                    evidence_bits.append(f"{node.evidence_type} {source}")
                lines.append("    evidence: " + "; ".join(evidence_bits))
        supporting = ", ".join(contradiction.supporting_event_ids) or "none"
        lines.append(f"  supporting events: {supporting}")
    return "\n".join(lines)


def format_confidence(state: State, fact_confidences: list[FactConfidence]) -> str:
    """Format confidence summary and concise fact confidence list."""

    summary = build_confidence_summary(state, fact_confidences)
    lines = [
        "Confidence Summary",
        "",
        f"Facts: {summary.fact_count}",
        f"Strongly Supported: {summary.strongly_supported_count}",
        f"Weakly Supported: {summary.weakly_supported_count}",
        f"Unsupported: {summary.unsupported_count}",
        f"Contradicted: {summary.contradicted_count}",
        f"Average Confidence: {summary.average_confidence:.2f}",
        "",
        f"Projection Version: {summary.projection_version}",
        f"Last Event: {summary.last_event_id or 'none'}",
        "",
        "Fact Confidence",
        "",
    ]
    if not fact_confidences:
        lines.append("(none)")
        return "\n".join(lines)
    for item in fact_confidences:
        lines.append(
            f"* {item.subject} {item.predicate} {_format_view_value(item.object)} "
            f"confidence={item.confidence:.2f} support={item.support_count} "
            f"contradictions={item.contradiction_count} "
            f"unsupported={_format_bool(item.unsupported)} "
            f"contradicted={_format_bool(item.contradicted)}"
        )
    return "\n".join(lines)


def format_confidence_fact(
    confidences: list[FactConfidence],
    subject: str,
    predicate: str,
    object_value: str | None,
) -> str:
    """Format detailed confidence for a fact query."""

    if not confidences:
        query = f"{subject} {predicate}" + (f" {object_value}" if object_value else "")
        return "\n".join(["Fact", "", f"No matching fact found for {query}."])
    item = confidences[0]
    lines = [
        "Fact",
        "",
        f"{item.subject} {item.predicate} {_format_view_value(item.object)}",
        f"confidence: {item.confidence:.2f}",
        f"support count: {item.support_count}",
        f"contradictions: {item.contradiction_count}",
        f"unsupported: {_format_bool(item.unsupported)}",
        f"contradicted: {_format_bool(item.contradicted)}",
        "",
        "Reasons",
        "",
    ]
    if item.reasons:
        lines.extend(f"* {reason}" for reason in item.reasons)
    else:
        lines.append("(none)")
    lines.extend(["", "Supporting Events", ""])
    if item.supporting_event_ids:
        lines.extend(f"* {event_id}" for event_id in item.supporting_event_ids)
    else:
        lines.append("(none)")
    return "\n".join(lines)


def _format_bool(value: bool) -> str:
    return "true" if value else "false"


def format_state_view_summary(summary: StateSummary) -> str:
    """Format the v1 State View summary."""

    return "\n".join(
        [
            "State Build",
            "",
            f"Facts: {summary.facts_count}",
            f"Observations: {summary.observations_count}",
            f"Requirements: {summary.requirements_count}",
            f"Capabilities: {summary.capabilities_count}",
            f"Issues: {summary.issues_count}",
            "",
            f"Projection Version: {summary.projection_version}",
            f"Last Event: {summary.last_event_id or 'none'}",
        ]
    )


def format_fact_views(views: list[FactView]) -> str:
    lines = ["Current Facts", ""]
    lines.extend(
        f"* {view.subject} {view.predicate} {_format_view_value(view.object)}"
        f"{_format_view_dimensions(view.dimensions)}"
        for view in views
    )
    if not views:
        lines.append("(none)")
    return "\n".join(lines)


def format_observation_views(views: list[ObservationView]) -> str:
    lines = ["Current Observations", ""]
    lines.extend(f"* {view.summary}" for view in views)
    if not views:
        lines.append("(none)")
    return "\n".join(lines)


def format_requirement_views(views: list[RequirementView]) -> str:
    lines = ["Current Requirements", ""]
    lines.extend(f"* {view.requirement_name} ({view.status})" for view in views)
    if not views:
        lines.append("(none)")
    return "\n".join(lines)


def format_capability_views(views: list[CapabilityView]) -> str:
    lines = ["Current Capabilities", ""]
    lines.extend(f"* {view.capability_name} ({view.status})" for view in views)
    if not views:
        lines.append("(none)")
    return "\n".join(lines)


def format_capability_inventory(entries: list[CapabilityInventoryEntry]) -> str:
    """Format capability verification inventory as deterministic JSON."""

    return json.dumps(to_plain(entries), sort_keys=True, indent=2)


def format_projection_integrity_summary(summary: ProjectionIntegritySummary) -> str:
    """Format the read-only Projection Integrity Summary."""

    lines = [
        "Integrity Summary",
        "",
        f"Unsupported facts: {summary.unsupported_fact_count}",
        "See: --unsupported-facts",
        "",
        f"Fact conflicts: {summary.fact_conflict_count}",
        "See: --fact-conflicts",
        "",
        f"Contradictions: {summary.contradiction_count}",
        "See: --contradictions",
        "",
        f"Graph issues: {summary.graph_issue_count}",
        "See: --graph-issues",
        "",
        f"Stale facts: {summary.stale_fact_count}",
        "See: --stale-facts",
        "",
        f"Refresh recommendations: {summary.refresh_recommendation_count}",
        "See: --stale-fact-refreshes",
        "",
        "Capabilities",
        "",
        f"Verified: {summary.verified_capability_count}",
        f"Unverified: {summary.unverified_capability_count}",
        f"Stale: {summary.stale_capability_count}",
        f"Unknown: {summary.unknown_capability_count}",
        f"Provider reported: {summary.provider_reported_capability_count}",
        "",
        "See: --capability-status",
        "",
        "Caveats",
        "",
    ]
    lines.extend(f"* {caveat}" for caveat in summary.caveats)
    lines.extend(
        [
            "",
            f"Projection Version: {summary.projection_version}",
            f"Last Event: {summary.last_event_id or 'none'}",
        ]
    )
    return "\n".join(lines)


def format_issue_views(views: list[IssueView]) -> str:
    lines = ["Current Issues", ""]
    lines.extend(f"* {view.summary} ({view.severity})" for view in views)
    if not views:
        lines.append("(none)")
    return "\n".join(lines)


def format_decision_context_view(view: DecisionContextView) -> str:
    """Format the exact read-only Decision Context View as deterministic JSON."""

    return json.dumps(to_plain(view), sort_keys=True, indent=2)


def _format_view_value(value: Any) -> str:
    if isinstance(value, bool):
        return str(value).lower()
    if isinstance(value, (dict, list)):
        return json.dumps(value, sort_keys=True, separators=(",", ":"))
    return str(value)


def _format_view_dimensions(dimensions: dict[str, str]) -> str:
    if not dimensions:
        return ""
    values = ", ".join(
        f"{key}={_format_view_value(dimensions[key])}" for key in sorted(dimensions)
    )
    return f" ({values})"


_FILESYSTEM_CATEGORY_ORDER = ("root", "boot", "cluster mounts", "other")
_FILESYSTEM_DETAIL_LIMIT = 10


def _filesystem_category(filesystem: dict[str, Any]) -> str:
    mountpoint = str(filesystem.get("mountpoint", ""))
    normalized = mountpoint.rstrip("/") or "/"
    if normalized == "/":
        return "root"
    if (
        normalized == "/media/boot"
        or normalized == "/boot"
        or normalized.startswith("/boot/")
        or normalized.startswith("/System/Volumes/iSCPreboot")
        or "preboot" in normalized.lower()
    ):
        return "boot"
    if normalized.startswith("/mnt/node") or normalized.startswith("/mnt/rpi"):
        return "cluster mounts"
    return "other"


def _filesystem_shape_summary(
    filesystems: list[dict[str, Any]],
    *,
    detail_limit: int = _FILESYSTEM_DETAIL_LIMIT,
) -> dict[str, Any]:
    counts = {category: 0 for category in _FILESYSTEM_CATEGORY_ORDER}
    categorized = {category: [] for category in _FILESYSTEM_CATEGORY_ORDER}
    for filesystem in filesystems:
        category = _filesystem_category(filesystem)
        counts[category] += 1
        categorized[category].append(filesystem)
    detail_category = "root"
    detail_rows = categorized["root"][:detail_limit]
    return {
        "counts": counts,
        "detail_category": detail_category,
        "detail_limit": detail_limit,
        "detail_rows": [dict(row) for row in detail_rows],
        "detail_row_count": len(detail_rows),
        "total_row_count": len(filesystems),
    }


def _counts_by(
    items: list[dict[str, Any]],
    field: str,
    *,
    order: tuple[str, ...] = (),
) -> dict[str, int]:
    counts: dict[str, int] = {}
    for item in items:
        value = str(item.get(field, "unknown"))
        counts[value] = counts.get(value, 0) + 1
    order_index = {value: index for index, value in enumerate(order)}
    return dict(
        sorted(
            counts.items(),
            key=lambda item: (order_index.get(item[0], len(order_index)), item[0]),
        )
    )


def format_state_build(view_summary: StateSummary, summary: dict[str, Any]) -> str:
    """Format the single state-build accounting surface."""

    def cache_status(key: str) -> str:
        value = summary.get(key, "miss")
        return value if value in {"hit", "miss"} else "miss"

    sources = summary["observation_source_counts"]
    lines = [
        "State Build",
        "",
        "Build:",
        f"  state-build cache: {cache_status('state_build_cache_status')}",
        f"  projection cache: {cache_status('projection_cache_status')}",
        f"  state cache: {cache_status('state_cache_status')}",
        "",
        "Projection:",
        f"  version: {view_summary.projection_version}",
        f"  last event: {view_summary.last_event_id or 'none'}",
        "",
        "Projected State:",
        f"  entities: {summary['entity_count']}",
        f"  facts: {summary['fact_count']}",
        f"  observations: {view_summary.observations_count}",
        f"  requirements: {view_summary.requirements_count}",
        f"  capabilities: {view_summary.capabilities_count}",
        f"  issues: {view_summary.issues_count}",
        "",
        "Fact Accounting:",
        f"  durable facts: {summary['durable_fact_count']}",
        f"  measurement current samples: {summary['measurement_current_sample_count']}",
        f"  conflicts: {summary['conflict_count']}",
        f"  stale facts: {summary['stale_fact_count']}",
        "  graph issues: "
        f"{summary['graph_issue_warning_count']} "
        f"warning{'s' if summary['graph_issue_warning_count'] != 1 else ''}, "
        f"{summary['graph_issue_error_count']} "
        f"error{'s' if summary['graph_issue_error_count'] != 1 else ''}",
        "",
        "Observation Sources:",
    ]
    lines.extend(
        [f"  {source}: {count}" for source, count in sources.items()] or ["  (none)"]
    )
    # Default State Build is intentionally not a storage/filesystem detail
    # surface. Storage projection data may exist on explicit storage-focused
    # surfaces, but bounded storage detail is still detail and must not leak here.
    return "\n".join(lines)


def format_state_summary(summary: dict[str, Any]) -> str:
    """Format legacy operator summary dictionaries as a state-build surface."""

    view_summary = StateSummary(
        facts_count=summary["fact_count"],
        observations_count=summary.get("observation_count", 0),
        requirements_count=summary.get("requirement_count", 0),
        capabilities_count=summary.get("capability_count", 0),
        issues_count=summary.get("issue_count", 0),
        projection_version=summary.get("projection_version", STATE_PROJECTION_VERSION),
        last_event_id=summary.get("last_event_id"),
    )
    return format_state_build(view_summary, summary)


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
                    *(
                        [
                            f"dimensions: {_format_fact_dimension_pairs(support.dimensions)}"
                        ]
                        if support.dimensions
                        else []
                    ),
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


def _fact_support_for_measurement_sample(state: State, fact: Fact) -> FactSupport:
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


@dataclass(frozen=True)
class CurrentFactsTimingReport:
    output: str
    cache_status: str
    timings: list[tuple[str, float]]


@dataclass(frozen=True)
class _CurrentFactsCacheVisibility:
    cache_status: str
    state_path_label: str

    @classmethod
    def from_state_cache_status(
        cls, status: StateCacheStatus
    ) -> "_CurrentFactsCacheVisibility":
        """Describe the cache path that explains the measured State timing."""

        if status.cache_hit:
            state_path_label = (
                "state cache hit path (metadata validation + cached projection load)"
            )
        elif status.incremental_replay:
            state_path_label = "state cache miss path (incremental event replay)"
        else:
            state_path_label = "state cache miss path (full projection rebuild)"
        return cls(
            cache_status="hit" if status.cache_hit else "miss",
            state_path_label=state_path_label,
        )


class _TimingProjectionStore:
    def __init__(self, store: ProjectionStore, timings: list[tuple[str, float]]):
        self._store = store
        self._timings = timings

    def _timed(self, name: str, func):
        started = time.perf_counter()
        try:
            return func()
        finally:
            self._timings.append((name, time.perf_counter() - started))

    def load_snapshot(self, *args, **kwargs):
        return self._timed(
            "cache metadata lookup + cached projection row load",
            lambda: self._store.load_snapshot(*args, **kwargs),
        )

    def save_snapshot(self, *args, **kwargs):
        return self._timed(
            "snapshot save", lambda: self._store.save_snapshot(*args, **kwargs)
        )

    def load_derived_index_snapshot(self, *args, **kwargs):
        return self._timed(
            "fact-index cache lookup/load",
            lambda: self._store.load_derived_index_snapshot(*args, **kwargs),
        )

    def save_derived_index_snapshot(self, *args, **kwargs):
        return self._timed(
            "fact-index cache save",
            lambda: self._store.save_derived_index_snapshot(*args, **kwargs),
        )

    def __getattr__(self, name: str):
        return getattr(self._store, name)


def _format_current_facts_timing_report(report: CurrentFactsTimingReport) -> str:
    lines = [
        "Current Facts Timing",
        "",
        "Cache:",
        f"- state cache: {report.cache_status}",
        "",
        "Timings:",
    ]
    lines.extend(f"- {name}: {elapsed:.6f}s" for name, elapsed in report.timings)
    return "\n".join(lines)


def _current_facts_timing_from_args(
    args: argparse.Namespace,
) -> CurrentFactsTimingReport:
    """Build a read-only timing report for the current-facts State path."""

    timings: list[tuple[str, float]] = []
    started = time.perf_counter()

    def timed(name: str, func):
        phase_started = time.perf_counter()
        try:
            return func()
        finally:
            timings.append((name, time.perf_counter() - phase_started))

    ledger: EventLedger = timed(
        "ledger open", lambda: SQLiteEventLedger(args.db) if args.db else EventLedger()
    )
    raw_store = timed(
        "projection store open", lambda: _projection_store_from_args(args)
    )
    store = (
        _TimingProjectionStore(raw_store, timings) if raw_store is not None else None
    )
    try:
        current_facts_args = args.current_facts or []
        if len(current_facts_args) != 0:
            seed_dev_state_from_args(args, ledger)
        history_limit = 1
        projector = timed(
            "state projector construction",
            lambda: _state_projector_from_args(
                args, ledger, measurement_history_limit=history_limit
            ),
        )
        if store is not None and _can_use_state_cache(
            args, measurement_history_limit=history_limit
        ):
            projection_diagnostics = ProjectionBuildDiagnostics()
            state_path_started = time.perf_counter()
            state, status = project_state_with_cache(
                ledger,
                args.workspace,
                store,
                projector=projector,
                status_consumer=None,
                diagnostics=projection_diagnostics,
            )
            cache_visibility = _CurrentFactsCacheVisibility.from_state_cache_status(
                status
            )
            timings.append(
                (
                    cache_visibility.state_path_label,
                    time.perf_counter() - state_path_started,
                )
            )
            timings.extend(projection_diagnostics.timings)
            cache_status = cache_visibility.cache_status
        else:
            state = timed(
                "full projection rebuild (event replay)",
                lambda: projector.project(args.workspace),
            )
            cache_status = "unavailable"

        if len(current_facts_args) == 0:
            views = timed("read-model build", lambda: build_fact_view(state))
            output = timed("render", lambda: format_fact_views(views))
        else:
            subject, predicate = current_facts_args
            fact_index = timed(
                "fact-index build/load",
                lambda: (
                    load_or_build_fact_index(
                        state,
                        workspace_id=args.workspace,
                        store=store,
                        status_consumer=None,
                    )
                    if store is not None and _can_use_state_cache(args)
                    else None
                ),
            )
            output = timed(
                "query/filter + render",
                lambda: format_current_facts(
                    state,
                    subject,
                    predicate,
                    include_expired=args.include_expired,
                    fact_index=fact_index,
                ),
            )
        timings.append(("stdout/output time", 0.0))
        timings.append(("total", time.perf_counter() - started))
        return CurrentFactsTimingReport(output, cache_status, timings)
    finally:
        for resource in (raw_store, ledger):
            close = getattr(resource, "close", None)
            if close is not None:
                close()


def format_current_facts(
    state: State,
    subject: str,
    predicate: str,
    *,
    include_expired: bool = False,
    fact_index: object | None = None,
) -> str:
    """Format every current supported value, one per line."""

    if fact_index is not None:
        facts = fact_index.current_facts(
            state, subject, predicate, include_expired=include_expired
        )
    else:
        facts = state.get_current_facts(
            subject, predicate, include_expired=include_expired
        )
    if not facts:
        return f"no current facts for {subject} {predicate}"
    return "\n".join(
        f"{_format_fact_value(fact.value)}{_format_fact_dimensions(fact.dimensions)}"
        for fact in _sort_facts_for_display(facts)
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


def format_explanation(explanation: Explanation) -> str:
    """Render a deterministic operator-facing why explanation."""

    sections: list[str] = []
    if explanation.current_beliefs:
        sections.append("Current belief:")
        sections.extend(
            _format_belief_explanation(item) for item in explanation.current_beliefs
        )
    else:
        sections.append("No current belief.")

    if explanation.competing_beliefs:
        sections.append("Competing supported values:")
        sections.extend(
            _format_belief_explanation(item) for item in explanation.competing_beliefs
        )
    if explanation.conflict is not None:
        sections.append(f"Conflict: {explanation.conflict.reason}")
    return "\n\n".join(sections)


def _format_belief_explanation(belief: BeliefExplanation) -> str:
    lines = [
        f"{belief.predicate}={_format_fact_value(belief.value)}",
        "",
        "Explanation:",
        "",
        "supporting_fact_ids:",
        *[f"- {fact_id}" for fact_id in belief.supporting_fact_ids],
        "evidence_ids:",
        *([f"- {item}" for item in belief.evidence_ids] or ["- none"]),
        "source_types:",
        *[f"- {item}" for item in belief.source_types],
        f"support_confidence: {belief.support_confidence:.6f}",
        f"observation_time: {belief.latest_observed_at}",
    ]
    for fact in belief.facts:
        lines.extend(["", *_format_recursive_fact_explanation(fact)])
    return "\n".join(lines)


def _format_recursive_fact_explanation(
    fact: FactExplanation, *, indent: str = ""
) -> list[str]:
    lines = [f"{indent}fact: {fact.fact_id}"]
    if fact.inference_rule_id:
        lines.extend(
            [
                f"{indent}inference_rule: {fact.inference_rule_id}",
                f"{indent}derived_from: "
                + (
                    f"{fact.source_fact.predicate}={_format_fact_value(fact.source_fact.value)}"
                    if fact.source_fact is not None
                    else str(fact.source_fact_id)
                ),
                f"{indent}source_fact: {fact.source_fact_id}",
                f"{indent}inferred_confidence: {fact.inferred_confidence:.6f}",
            ]
        )
        if fact.confidence_cap is not None:
            lines.append(f"{indent}confidence_cap: {fact.confidence_cap:.6f}")
    else:
        lines.extend(
            [
                f"{indent}source_type: {fact.source_type}",
                f"{indent}observed_confidence: {fact.observed_confidence:.6f}",
                f"{indent}observation_time: {fact.observed_at}",
                f"{indent}evidence_ids: " + (", ".join(fact.evidence_ids) or "none"),
            ]
        )
    if len(fact.entity_resolution) > 1:
        lines.append(f"{indent}entity_resolution:")
        lines.extend(
            f"{indent}{'-> ' if index else ''}{value}"
            for index, value in enumerate(fact.entity_resolution)
        )
    if fact.source_fact is not None:
        lines.extend(
            _format_recursive_fact_explanation(fact.source_fact, indent=indent + "  ")
        )
    return lines


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
        predicate_counts[fact.predicate] = predicate_counts.get(fact.predicate, 0) + 1

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


def ingest_observations_from_args(
    args: argparse.Namespace,
    status_consumer: ExecutionStatusConsumer | None = None,
    diagnostics: list[ObservationIngestionDiagnostics] | None = None,
) -> list[Fact]:
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
                confidence=args.observe_confidence,
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
                    status_consumer=status_consumer,
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
                    status_consumer=status_consumer,
                    diagnostics=diagnostics,
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
                    status_consumer=status_consumer,
                    diagnostics=diagnostics,
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
                    status_consumer=status_consumer,
                    diagnostics=diagnostics,
                )
            )
        if args.observe_repository_source:
            facts.extend(
                ingest_observation_source(
                    ledger,
                    args.workspace,
                    RepositorySourceObservationSource(args.observe_repository_source),
                    session_id=args.session,
                    predicate_catalog_path=args.predicate_catalog,
                    status_consumer=status_consumer,
                    diagnostics=diagnostics,
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
            f"- {predicate.predicate}: {predicate.kind}/{predicate.value_type}/"
            f"{predicate.cardinality}{allowed}"
        )
    lines.append("mappings:")
    for mapping in catalog.list_mappings():
        source = mapping.source_name or "*"
        lines.append(f"- {source}:{mapping.predicate} -> {mapping.canonical_predicate}")
    return "\n".join(lines)


def format_inference_catalog(catalog: InferenceCatalog) -> str:
    """Format deterministic inference rules for inspection."""

    lines = ["deterministic inference rules:"]
    for rule in catalog.list_rules():
        when_value = (
            "*" if rule.when_value is None else _format_fact_value(rule.when_value)
        )
        lines.append(
            f"- {rule.id}: {rule.when_predicate}={when_value} -> "
            f"{rule.then_predicate}={_format_fact_value(rule.then_value)} "
            f"(confidence={rule.confidence}; reason={rule.reason})"
        )
    return "\n".join(lines)


def format_rule_inventory(entries: list[Any]) -> str:
    """Format deterministic rule inventory entries as stable JSON."""

    return json.dumps(to_plain(entries), indent=2, sort_keys=True)


def format_inferred_facts(state: State, entity: str) -> str:
    """Format inferred projection artifacts for an entity."""

    subjects = state.resolve_fact_subjects(entity)
    facts = sorted(
        (fact for fact in state.inferred_facts.values() if fact.subject_id in subjects),
        key=lambda fact: (fact.predicate, _format_fact_value(fact.value), fact.id),
    )
    if not facts:
        return f"no inferred facts for {entity}"
    return "\n".join(
        f"{fact.predicate}: {_format_fact_value(fact.value)} "
        f"(confidence={fact.confidence}, source_fact_id={fact.source_fact_id}, "
        f"inference_rule_id={fact.inference_rule_id})"
        for fact in facts
    )


def runtime_trace_from_args(args: argparse.Namespace, run_id: str) -> RuntimeTrace:
    """Load a historical runtime trace without seeding state or appending events."""

    ledger: EventLedger = SQLiteEventLedger(args.db) if args.db else EventLedger()
    try:
        return load_runtime_trace(ledger, args.workspace, run_id)
    finally:
        close = getattr(ledger, "close", None)
        if close is not None:
            close()


def _format_trace_value(value: Any) -> str:
    if value is None or value == "":
        return "none"
    if isinstance(value, bool):
        return str(value).lower()
    if isinstance(value, (dict, list)):
        return json.dumps(value, sort_keys=True)
    return str(value)


def _trace_policy_allowed(trace: RuntimeTrace) -> str:
    value = trace.summary.get("policy_allowed")
    if value is None:
        return "unknown"
    return str(bool(value)).lower()


def format_runtime_trace(trace: RuntimeTrace) -> str:
    """Render a deterministic plain-text RuntimeTrace."""

    if not trace.summary.get("found"):
        return f"Runtime trace not found for run_id: {trace.run_id}"

    summary = trace.summary
    decision = trace.decision_record or {}
    event_lines = [
        f"* {event.created_at.isoformat()} {event.event_id} {event.event_type}"
        for event in trace.events
    ]
    if not event_lines:
        event_lines = ["* none"]

    return "\n".join(
        [
            "Runtime Trace",
            f"workspace: {trace.workspace_id}",
            f"run: {trace.run_id}",
            "",
            f"Input: {_format_trace_value(summary.get('input_text'))}",
            "",
            "Decision:",
            f"kind: {_format_trace_value(summary.get('decision_kind'))}",
            f"reason: {_format_trace_value(summary.get('decision_reason'))}",
            f"context_hash: {_format_trace_value(decision.get('context_hash'))}",
            "",
            "Policy:",
            f"allowed: {_trace_policy_allowed(trace)}",
            "",
            "Execution:",
            f"tool: {_format_trace_value(summary.get('selected_tool'))}",
            f"outcome: {_format_trace_value(summary.get('outcome'))}",
            f"response: {_format_trace_value(summary.get('final_response_text'))}",
            f"error: {_format_trace_value(summary.get('error'))}",
            "",
            "Events:",
            *event_lines,
        ]
    )


def _why_decision_phrase(kind: Any, selected_tool: Any) -> str:
    if kind == "answer":
        return "answer"
    if kind == "call_tool":
        tool = _format_trace_value(selected_tool)
        return f"call tool {tool}" if tool != "none" else "call a tool"
    return _format_trace_value(kind)


def _why_policy_phrase(trace: RuntimeTrace) -> str:
    if trace.summary.get("policy_allowed") is True:
        return "allowed"
    if trace.summary.get("policy_allowed") is False or trace.summary.get(
        "policy_denied"
    ):
        return "denied"
    return "had unknown policy status for"


def format_runtime_why(trace: RuntimeTrace) -> str:
    """Render a short human explanation for a historical runtime run."""

    if not trace.summary.get("found"):
        return f"Runtime trace not found for run_id: {trace.run_id}"

    summary = trace.summary
    lines = [
        f"User asked: {_format_trace_value(summary.get('input_text'))}.",
        "",
        "Seed decided to "
        f"{_why_decision_phrase(summary.get('decision_kind'), summary.get('selected_tool'))} "
        f"because: {_format_trace_value(summary.get('decision_reason'))}.",
        "",
        f"Policy {_why_policy_phrase(trace)} the decision.",
        "",
        f"Outcome: {_format_trace_value(summary.get('outcome'))}.",
    ]
    final_response = summary.get("final_response_text")
    error = summary.get("error")
    if final_response:
        lines.extend(["", str(final_response)])
    if error:
        lines.extend(["", f"Error: {error}"])
    return "\n".join(lines)


def inquiry_note_store_path_from_args(args: argparse.Namespace) -> Path:
    """Return the isolated JSONL probe store path for inquiry notes."""

    if args.db:
        return Path(args.db).with_suffix(Path(args.db).suffix + ".inquiry_notes.jsonl")
    return REPO_ROOT / ".seed" / "inquiry_notes.jsonl"


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    if argv is None:
        argv = sys.argv[1:]
    if argv is not None and "--operational-graph-confidence" in argv:
        rewritten = list(argv)
        if "--operational-graph-confidence-tier" not in rewritten:
            for tier in ("high", "medium", "low"):
                if tier in rewritten:
                    rewritten.remove(tier)
                    rewritten.extend(["--operational-graph-confidence-tier", tier])
                    break
        argv = rewritten
    args = parser.parse_args(argv)
    apply_bounded_ask_dispatch(args, parser)
    validate_lifecycle_args(args, parser)
    if args.show_predicate_catalog:
        print(format_predicate_catalog(PredicateCatalog.load(args.predicate_catalog)))
        return 0

    if args.show_inference_catalog:
        print(format_inference_catalog(InferenceCatalog.load()))
        return 0

    if args.rules:
        print(format_rule_inventory(collect_rule_inventory()))
        return 0

    if args.trace_run:
        print(format_runtime_trace(runtime_trace_from_args(args, args.trace_run)))
        return 0

    if args.why_run:
        print(format_runtime_why(runtime_trace_from_args(args, args.why_run)))
        return 0

    if args.inferred_facts:
        print(format_inferred_facts(fact_query_state(args), args.inferred_facts))
        return 0

    if args.impact:
        print(format_entity_impact(projected_state_from_args(args), args.impact))
        return 0

    if args.audit_snapshot:
        ledger: EventLedger = SQLiteEventLedger(args.db) if args.db else EventLedger()
        try:
            events = ledger.list_events(args.workspace)
        finally:
            close = getattr(ledger, "close", None)
            if close is not None:
                close()
        if args.audit_snapshot == "observation_inventory":
            payload = build_observation_inventory().to_json_dict()
        else:
            payload = ownership_discrepancies_json(
                build_ownership_discrepancies(projected_state_from_args(args))
            )
        result = create_audit_snapshot(
            repo_root=REPO_ROOT,
            kind=args.audit_snapshot,
            payload=payload,
            command=f"seed --audit-snapshot {args.audit_snapshot}",
            seed_db=args.db,
            events=events,
            projection_version=STATE_PROJECTION_VERSION,
        )
        print(f"Created audit snapshot {result.snapshot_id}: {result.directory}")
        return 0

    if args.audit_snapshots:
        print(format_audit_snapshots(list_audit_snapshots(REPO_ROOT)))
        return 0

    if args.audit_compare:
        diff = compare_audit_snapshots(
            REPO_ROOT, args.audit_compare[0], args.audit_compare[1], kind=args.kind
        )
        if args.json_output:
            print(json.dumps(diff, indent=2, sort_keys=True))
        else:
            print(format_audit_compare(diff))
        return 0

    if args.container_ownership_authority:
        state = projected_state_from_args(args)
        result = evaluate_container_ownership_authority_slice(
            state, CONSTRAINED_AUTHORITY_PROFILE
        )
        if args.json_output:
            print(
                json.dumps(
                    container_ownership_authority_json(result),
                    indent=2,
                    sort_keys=True,
                )
            )
        else:
            print(format_container_ownership_authority(result))
        return 0

    if args.service_ownership_authority:
        state = projected_state_from_args(args)
        result = evaluate_service_ownership_authority_slice(
            state, CONSTRAINED_AUTHORITY_PROFILE
        )
        if args.json_output:
            print(
                json.dumps(
                    service_ownership_authority_json(result),
                    indent=2,
                    sort_keys=True,
                )
            )
        else:
            print(format_service_ownership_authority(result))
        return 0

    if args.listener_endpoint_authority:
        state = projected_state_from_args(args)
        result = evaluate_listener_endpoint_authority_slice(
            state, LISTENER_ENDPOINT_AUTHORITY_PROFILE
        )
        if args.json_output:
            print(
                json.dumps(
                    listener_endpoint_authority_json(result),
                    indent=2,
                    sort_keys=True,
                )
            )
        else:
            print(format_listener_endpoint_authority(result))
        return 0

    if args.diagnostic_inventory:
        if args.json_output:
            print(json.dumps(diagnostic_inventory_json(), indent=2, sort_keys=True))
        else:
            print(format_diagnostic_inventory())
        return 0

    if args.diagnostic_surface_definition:
        if args.json_output:
            print(
                json.dumps(
                    diagnostic_surface_definition_json(args.diagnostic_surface_definition),
                    indent=2,
                    sort_keys=True,
                )
            )
        else:
            print(format_diagnostic_surface_definition(args.diagnostic_surface_definition))
        return 0

    if args.diagnostic_surface_explanation:
        if args.json_output:
            print(
                json.dumps(
                    diagnostic_surface_explanation_json(args.diagnostic_surface_explanation),
                    indent=2,
                    sort_keys=True,
                )
            )
        else:
            print(format_diagnostic_surface_explanation(args.diagnostic_surface_explanation))
        return 0

    if args.question_surface_inventory:
        rows = build_question_surface_inventory()
        if args.json_output:
            print(
                json.dumps(
                    question_surface_inventory_json(rows), indent=2, sort_keys=True
                )
            )
        else:
            print(format_question_surface_inventory(rows))
        return 0

    if args.question_family_definition:
        rows = build_question_surface_inventory()
        if args.json_output:
            print(
                json.dumps(
                    question_family_definition_json(
                        args.question_family_definition, rows
                    ),
                    indent=2,
                    sort_keys=True,
                )
            )
        else:
            print(
                format_question_family_definition(args.question_family_definition, rows)
            )
        return 0

    if args.question_family_explanation:
        rows = build_question_surface_inventory()
        if args.json_output:
            print(
                json.dumps(
                    composed_question_family_explanation_json(
                        args.question_family_explanation, rows
                    ),
                    indent=2,
                    sort_keys=True,
                )
            )
        else:
            print(
                format_composed_question_family_explanation(
                    args.question_family_explanation, rows
                )
            )
        return 0

    if args.documentation_structure:
        options = DocumentationStructureOptions(
            selection_filters=DocumentationStructureSelectionFilters(
                missing_front_matter=args.missing_front_matter,
                missing_trailing_newline=args.missing_trailing_newline,
                empty_sections=args.empty_sections,
            ),
            detail_expansions=DocumentationStructureDetailExpansions(
                include_sections=args.sections,
                include_links=args.links,
                include_code_fences=args.code_fences,
            ),
            output_bounds=DocumentationStructureOutputBounds(
                limit=args.limit,
                top=args.top,
                summary_only=args.summary_only,
                min_count=args.min_count,
                max_count=args.max_count,
            ),
            recurrence=DocumentationStructureRecurrenceOptions(
                enabled=args.recurrence or args.outliers,
                rare=args.rare,
                missing_common_sections=args.missing_common_sections,
                outliers=args.outliers,
                skeletons=args.skeletons,
            ),
            drilldown=DocumentationStructureDrilldownOptions(where=args.where),
            membership=DocumentationStructureMembershipOptions(target=args.membership),
        )
        try:
            report = observe_documentation_structure(REPO_ROOT, options, args.document)
        except (FileNotFoundError, ValueError) as exc:
            parser.error(str(exc))
        if args.json_output:
            print(
                json.dumps(
                    documentation_structure_json(report), indent=2, sort_keys=True
                )
            )
        else:
            print(format_documentation_structure(report, options))
        return 0

    if args.projected_state_consumers:
        rows = build_projected_state_consumers()
        if args.json_output:
            print(
                json.dumps(
                    projected_state_consumers_json(rows), indent=2, sort_keys=True
                )
            )
        else:
            print(format_projected_state_consumers(rows))
        return 0

    if args.implementation_trait_characterization:
        rows = build_implementation_trait_characterization()
        if args.json_output:
            print(
                json.dumps(
                    implementation_trait_characterization_json(rows),
                    indent=2,
                    sort_keys=True,
                )
            )
        else:
            print(format_implementation_trait_characterization(rows))
        return 0

    if args.projection_shape:
        shape = build_projection_shape()
        if args.json_output:
            print(json.dumps(projection_shape_json(shape), indent=2, sort_keys=True))
        else:
            print(format_projection_shape(shape))
        return 0

    if args.projection_stage_definition:
        if args.json_output:
            print(
                json.dumps(
                    projection_stage_definition_json(args.projection_stage_definition),
                    indent=2,
                    sort_keys=True,
                )
            )
        else:
            print(format_projection_stage_definition(args.projection_stage_definition))
        return 0

    if args.projection_stage_explanation:
        if args.json_output:
            print(
                json.dumps(
                    projection_stage_explanation_json(args.projection_stage_explanation),
                    indent=2,
                    sort_keys=True,
                )
            )
        else:
            print(format_projection_stage_explanation(args.projection_stage_explanation))
        return 0

    if args.diagnostic_shape_audit:
        rows = build_diagnostic_shape_audit()
        shape_status = "mismatch" if args.mismatches else args.status
        if args.json_output:
            print(
                json.dumps(
                    diagnostic_shape_audit_json(rows, status=shape_status),
                    indent=2,
                    sort_keys=True,
                )
            )
        else:
            print(format_diagnostic_shape_audit(rows, status=shape_status))
        return 0

    if args.component_audit:
        audit = build_component_audit(args.component_audit, REPO_ROOT)
        if args.json_output:
            print(json.dumps(component_audit_json(audit), indent=2, sort_keys=True))
        else:
            print(format_component_audit(audit))
        return 0

    if args.architecture_conformance_audit:
        audit = build_architecture_conformance_audit(REPO_ROOT)
        if args.json_output:
            print(
                json.dumps(
                    architecture_conformance_audit_json(audit),
                    indent=2,
                    sort_keys=True,
                )
            )
        else:
            print(format_architecture_conformance_audit(audit))
        return 0

    if args.reasoning_path:
        audit = build_reasoning_path_audit(
            projected_state_from_args(args),
            args.reasoning_path[0],
            args.reasoning_path[1],
            repo_root=REPO_ROOT,
        )
        if args.json_output:
            print(
                json.dumps(reasoning_path_audit_json(audit), indent=2, sort_keys=True)
            )
        else:
            print(format_reasoning_path_audit(audit))
        return 0

    if args.selection_path:
        audit = build_selection_path_audit(
            projected_state_from_args(args),
            args.selection_path,
            repo_root=REPO_ROOT,
        )
        if args.json_output:
            print(
                json.dumps(selection_path_audit_json(audit), indent=2, sort_keys=True)
            )
        else:
            print(format_selection_path_audit(audit))
        return 0

    if args.operational_graph:
        graph = build_operational_graph(REPO_ROOT)
        if args.json_output:
            print(json.dumps(operational_graph_json(graph), indent=2, sort_keys=True))
        else:
            print(format_operational_graph(graph))
        return 0

    if args.operational_graph_taxonomy:
        analysis = build_operational_graph_taxonomy(REPO_ROOT)
        if args.json_output:
            print(
                json.dumps(
                    operational_graph_taxonomy_json(analysis), indent=2, sort_keys=True
                )
            )
        else:
            print(format_operational_graph_taxonomy(analysis))
        return 0

    if args.operational_graph_confidence:
        graph_confidence_tier = (
            args.operational_graph_confidence_tier
            or args.operational_graph_confidence_tier_option
        )
        analysis = build_operational_graph_confidence(
            REPO_ROOT,
            confidence=graph_confidence_tier,
            exclude_aggregate=args.exclude_aggregate,
        )
        if args.json_output:
            print(
                json.dumps(
                    operational_graph_confidence_json(analysis),
                    indent=2,
                    sort_keys=True,
                )
            )
        else:
            print(format_operational_graph_confidence(analysis))
        return 0

    if args.operational_surface_inventory:
        surfaces = build_operational_surface_inventory(build_parser())
        if args.json_output:
            print(
                json.dumps(
                    operational_surface_inventory_json(surfaces),
                    indent=2,
                    sort_keys=True,
                )
            )
        else:
            print(format_operational_surface_inventory(surfaces))
        return 0

    if args.visibility_coverage_audit:
        audit = build_visibility_coverage_audit(build_parser())
        if args.json_output:
            print(
                json.dumps(
                    visibility_coverage_audit_json(audit), indent=2, sort_keys=True
                )
            )
        else:
            print(format_visibility_coverage_audit(audit))
        return 0

    if args.operational_surface_classification_audit:
        audit = build_operational_surface_classification_audit(build_parser())
        if args.json_output:
            print(
                json.dumps(
                    operational_surface_classification_audit_json(audit),
                    indent=2,
                    sort_keys=True,
                )
            )
        else:
            print(format_operational_surface_classification_audit(audit))
        return 0

    if args.observation_inventory:
        inventory = build_observation_inventory(
            provider_filter=args.provider, predicate_filter=args.predicate
        )
        if args.json_output:
            print(json.dumps(inventory.to_json_dict(), indent=2, sort_keys=True))
        else:
            print(format_observation_inventory(inventory))
        return 0

    if args.observation_utilization:
        audit = build_observation_utilization_audit(
            provider_filter=args.provider, predicate_filter=args.predicate
        )
        if args.json_output:
            print(
                json.dumps(
                    observation_utilization_json(audit), indent=2, sort_keys=True
                )
            )
        else:
            print(format_observation_utilization(audit))
        return 0

    if args.observation_domains:
        domain = (
            None if args.observation_domains == "__all__" else args.observation_domains
        )
        report = build_observation_domains(projected_state_from_args(args), domain)
        if args.json_output:
            print(
                json.dumps(observation_domains_json(report), indent=2, sort_keys=True)
            )
        else:
            print(format_observation_domains(report))
        return 0

    if args.observation_permission:
        domain = (
            None
            if args.observation_permission == "__all__"
            else args.observation_permission
        )
        report = build_observation_permission(projected_state_from_args(args), domain)
        if args.json_output:
            print(
                json.dumps(
                    observation_permission_json(report), indent=2, sort_keys=True
                )
            )
        else:
            print(format_observation_permission(report))
        return 0

    if args.ops_brief:
        brief = build_ops_brief(projected_state_from_args(args), repo_root=REPO_ROOT)
        if args.json_output:
            print(json.dumps(brief.to_json_dict(), indent=2, sort_keys=True))
        else:
            print(format_ops_brief(brief))
        return 0

    if args.operational_story:
        story = build_operational_story(
            projected_state_from_args(args), repo_root=REPO_ROOT
        )
        if args.json_output:
            print(json.dumps(operational_story_json(story), indent=2, sort_keys=True))
        else:
            print(format_operational_story(story))
        return 0

    if args.investigation_path:
        audit = build_investigation_path_audit(args.investigation_path)
        if args.json_output:
            print(
                json.dumps(
                    investigation_path_audit_json(audit), indent=2, sort_keys=True
                )
            )
        else:
            print(format_investigation_path_audit(audit))
        return 0 if audit.found else 1

    if args.reference_selection:
        selection = build_reference_selection(REPO_ROOT, args.reference_selection)
        if args.json_output:
            print(
                json.dumps(
                    reference_selection_json(selection), indent=2, sort_keys=True
                )
            )
        else:
            print(format_reference_selection(selection))
        return 0

    if args.impact_audit:
        audit = build_impact_audit(REPO_ROOT)
        if args.json_output:
            print(json.dumps(impact_audit_json(audit), indent=2, sort_keys=True))
        else:
            print(format_impact_audit(audit))
        return 0

    if args.history_brief:
        brief = build_history_brief(REPO_ROOT)
        if args.json_output:
            print(json.dumps(history_brief_json(brief), indent=2, sort_keys=True))
        else:
            print(format_history_brief(brief))
        return 0

    if args.observe_repository:
        observation = observe_repository(args.observe_repository)
        if args.json_output:
            print(
                json.dumps(
                    repository_observation_json(observation), indent=2, sort_keys=True
                )
            )
        else:
            print(format_repository_observation(observation))
        return 0

    if args.snapshot_policy_audit:
        audit = build_snapshot_policy_audit(REPO_ROOT)
        if args.json_output:
            print(
                json.dumps(snapshot_policy_audit_json(audit), indent=2, sort_keys=True)
            )
        else:
            print(format_snapshot_policy_audit(audit))
        return 0

    if args.pressure_audit:
        audit = build_pressure_audit(
            projected_state_from_args(args), repo_root=REPO_ROOT
        )
        if args.json_output:
            print(json.dumps(pressure_audit_json(audit), indent=2, sort_keys=True))
        else:
            print(format_pressure_audit(audit))
        return 0

    if args.privilege_discovery:
        audit = build_privilege_discovery(projected_state_from_args(args))
        if args.json_output:
            print(json.dumps(privilege_discovery_json(audit), indent=2, sort_keys=True))
        else:
            print(format_privilege_discovery(audit))
        return 0

    if args.capability_relationship:
        audit = build_capability_relationship(
            projected_state_from_args(args),
            capability_filter=(
                None
                if args.capability_relationship == "__all__"
                else args.capability_relationship
            ),
        )
        if args.json_output:
            print(
                json.dumps(
                    capability_relationship_json(audit), indent=2, sort_keys=True
                )
            )
        else:
            print(format_capability_relationship(audit))
        return 0

    if args.correlation_audit:
        audit = build_correlation_audit(
            projected_state_from_args(args), repo_root=REPO_ROOT
        )
        if args.json_output:
            print(json.dumps(correlation_audit_json(audit), indent=2, sort_keys=True))
        else:
            print(format_correlation_audit(audit))
        return 0

    if args.unhealthy:
        print(
            format_unhealthy(
                projected_state_from_args(args), include_warnings=args.include_warnings
            )
        )
        return 0

    if args.relationships:
        print(format_relationships(projected_state_from_args(args), args))
        return 0

    if args.graph_issues:
        print(format_graph_issues(projected_state_from_args(args), args.severity))
        return 0

    if args.graph_issue_summary:
        print(
            format_graph_issue_summary(
                projected_state_from_args(args),
                category_limit=args.graph_issue_limit,
                examples_per_category=args.graph_issue_examples,
            )
        )
        return 0

    if args.classification_coverage:
        state = projected_state_from_args(args)
        diagnostic = build_classification_coverage_diagnostic(state)
        if args.record:
            record_classification_coverage_diagnostic(args, diagnostic)
        print(format_classification_coverage(diagnostic))
        return 0

    if args.entity_types or args.entity_type:
        print(format_entity_types(projected_state_from_args(args), args.entity_type))
        return 0

    if args.candidate_requests:
        print(
            json.dumps(
                to_plain(inspect_candidate_requests(args.candidate_requests)),
                indent=2,
                sort_keys=True,
            )
        )
        return 0

    if args.candidate_routes:
        print(
            json.dumps(
                to_plain(inspect_candidate_routes(args.candidate_routes)),
                indent=2,
                sort_keys=True,
            )
        )
        return 0

    if args.inquiry_artifacts:
        view = build_inquiry_artifacts()
        if args.json_output:
            print(json.dumps(inquiry_artifacts_json(view), indent=2, sort_keys=True))
        else:
            print(format_inquiry_artifacts(view))
        return 0

    if args.record_inquiry_note is not None:
        note = record_inquiry_note(
            inquiry_note_store_path_from_args(args),
            args.record_inquiry_note,
            workspace_id=args.workspace,
            session_id=args.session,
        )
        print(f"recorded inquiry note: {note.note_id}")
        if args.inquiry_orientation is None:
            return 0

    if args.inquiry_orientation is not None:
        requested_note_id = (
            None
            if args.inquiry_orientation == "__latest__"
            else args.inquiry_orientation
        )
        note = select_inquiry_note(
            inquiry_note_store_path_from_args(args), requested_note_id
        )
        if note is None:
            message = (
                "No inquiry note found."
                if requested_note_id is None
                else f"Inquiry note not found: {requested_note_id}"
            )
            print(message, file=sys.stderr)
            return 1
        print(
            format_inquiry_orientation(
                build_inquiry_orientation(projected_state_from_args(args), note)
            )
        )
        return 0

    if args.knowledge_reachability_audit:
        ledger: EventLedger = SQLiteEventLedger(args.db) if args.db else EventLedger()
        try:
            result = build_knowledge_reachability_audit_result(
                ledger,
                args.workspace,
                family=args.knowledge_reachability_audit_family,
                candidate_kind=args.candidate_kind,
                subject=args.knowledge_reachability_audit_subject,
                repo_root=REPO_ROOT,
                limit=args.knowledge_reachability_audit_limit,
                all_candidates=args.knowledge_reachability_audit_all,
                max_seconds=args.knowledge_reachability_audit_max_seconds,
                progress=lambda message: print(message, file=sys.stderr, flush=True),
            )
            if args.knowledge_reachability_audit_debug:
                print("[reachability] candidate sources:", file=sys.stderr, flush=True)
                for name, count in (result.metadata.candidate_sources or {}).items():
                    print(
                        f"[reachability]   {name}: {count}", file=sys.stderr, flush=True
                    )
                print("[reachability] scan counts:", file=sys.stderr, flush=True)
                for name, count in (result.metadata.scan_counts or {}).items():
                    print(
                        f"[reachability]   {name}: {count}", file=sys.stderr, flush=True
                    )
                print(
                    "[reachability] algorithmic counters:",
                    file=sys.stderr,
                    flush=True,
                )
                for name, count in (result.metadata.algorithmic_counters or {}).items():
                    print(
                        f"[reachability] {name}={count}",
                        file=sys.stderr,
                        flush=True,
                    )
                print("[reachability] cache visibility:", file=sys.stderr, flush=True)
                for name, status in (result.metadata.cache or {}).items():
                    print(
                        f"[reachability]   {name} cache {status}",
                        file=sys.stderr,
                        flush=True,
                    )
        finally:
            close = getattr(ledger, "close", None)
            if close is not None:
                close()
        if args.knowledge_reachability_audit_json:
            print(
                json.dumps(
                    knowledge_reachability_json(result.rows, result.metadata),
                    indent=2,
                    sort_keys=True,
                )
            )
        else:
            print(format_knowledge_reachability_table(result.rows, result.metadata))
        return 0

    if args.ownership_discrepancies:
        rows = build_ownership_discrepancies(
            projected_state_from_args(args), subject_filter=args.subject
        )
        if args.record:
            record_ownership_discrepancy_capability_needs(args, rows)
        if args.json_output:
            print(
                json.dumps(ownership_discrepancies_json(rows), indent=2, sort_keys=True)
            )
        else:
            print(format_ownership_discrepancies(rows))
        return 0

    if args.capability_needs:
        entries = build_capability_needs(
            projected_state_from_args(args),
            subject_filter=args.subject,
            diagnostic_filter=args.diagnostic,
        )
        if args.json_output:
            print(json.dumps(capability_needs_json(entries), indent=2, sort_keys=True))
        else:
            print(format_capability_needs(entries))
        return 0

    if args.consumer_audit:
        audit = build_consumer_audit(
            predicate_filter=args.predicate,
            diagnostic_filter=args.diagnostic,
        )
        if args.json_output:
            print(json.dumps(consumer_audit_json(audit), indent=2, sort_keys=True))
        else:
            print(format_consumer_audit(audit))
        return 0

    if args.emitter_consumer_audit:
        audit = build_emitter_consumer_audit(
            REPO_ROOT, include_rendered=args.include_rendered
        )
        if args.json_output:
            print(
                json.dumps(emitter_consumer_audit_json(audit), indent=2, sort_keys=True)
            )
        else:
            print(format_emitter_consumer_audit(audit))
        return 0

    if args.emitter_attribution_audit:
        audit = build_emitter_attribution_audit(
            REPO_ROOT, include_rendered=args.include_rendered
        )
        if args.json_output:
            print(
                json.dumps(
                    emitter_attribution_audit_json(audit), indent=2, sort_keys=True
                )
            )
        else:
            print(format_emitter_attribution_audit(audit))
        return 0

    if args.state_build:
        view_summary, operator_summary = projected_state_summary_from_args(
            args, status_consumer=CliExecutionStatusConsumer()
        )
        print(format_state_build(view_summary, operator_summary))
        return 0

    if args.state_build_cache_debug:
        print(
            format_state_summary_cache_debug_report(
                state_summary_cache_debug_from_args(args)
            )
        )
        return 0

    if args.integrity_summary:
        print(
            format_projection_integrity_summary(
                build_projection_integrity_summary(projected_state_from_args(args))
            )
        )
        return 0

    if args.rebuild_state_cache:
        print(rebuild_state_cache_from_args(args))
        return 0

    if args.state_cache_status:
        print(format_state_cache_status_from_args(args))
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

    if args.why:
        subject, predicate = args.why
        state = fact_query_state(args)
        print(format_explanation(ExplanationBuilder(state).why(subject, predicate)))
        return 0

    if args.evidence:
        print(format_evidence_graph(projected_state_from_args(args)))
        return 0

    if args.why_fact:
        subject, predicate, *maybe_object = args.why_fact
        print(
            format_why_fact(
                find_evidence_for_fact(
                    projected_state_from_args(args),
                    subject,
                    predicate,
                    maybe_object[0] if maybe_object else None,
                ),
                subject,
                predicate,
                maybe_object[0] if maybe_object else None,
            )
        )
        return 0

    if args.unsupported_facts:
        print(
            format_unsupported_facts(
                unsupported_fact_views(projected_state_from_args(args))
            )
        )
        return 0

    if args.contradictions:
        state = projected_state_from_args(args)
        evidence_graph = build_evidence_graph(state)
        print(format_contradictions(state, build_contradictions(state, evidence_graph)))
        return 0

    if args.confidence_report:
        state = projected_state_from_args(args)
        evidence_graph = build_evidence_graph(state)
        contradictions = build_contradictions(state, evidence_graph)
        fact_confidences = build_fact_confidences(state, evidence_graph, contradictions)
        print(format_confidence(state, fact_confidences))
        return 0

    if args.confidence_fact:
        subject, predicate, *maybe_object = args.confidence_fact
        state = projected_state_from_args(args)
        evidence_graph = build_evidence_graph(state)
        contradictions = build_contradictions(state, evidence_graph)
        print(
            format_confidence_fact(
                find_fact_confidence(
                    state,
                    subject,
                    predicate,
                    maybe_object[0] if maybe_object else None,
                    evidence_graph,
                    contradictions,
                ),
                subject,
                predicate,
                maybe_object[0] if maybe_object else None,
            )
        )
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

    if args.source_navigation:
        state = fact_query_state(args, status_consumer=CliExecutionStatusConsumer())
        print(
            format_source_navigation(
                build_source_navigation(state, args.source_navigation)
            )
        )
        return 0

    if args.current_facts_cache_debug:
        report = _current_facts_timing_from_args(args)
        print(report.output)
        print()
        print(_format_current_facts_timing_report(report))
        return 0

    if args.current_facts is not None:
        if len(args.current_facts) == 0:
            print(
                format_fact_views(
                    build_fact_view(
                        projected_state_from_args(
                            args, status_consumer=CliExecutionStatusConsumer()
                        )
                    )
                )
            )
            return 0
        subject, predicate = args.current_facts
        status_consumer = CliExecutionStatusConsumer()
        state = fact_query_state(args, status_consumer=status_consumer)
        fact_index = _load_or_build_fact_index_from_args(
            args, state, status_consumer=status_consumer
        )
        print(
            format_current_facts(
                state,
                subject,
                predicate,
                include_expired=args.include_expired,
                fact_index=fact_index,
            )
        )
        return 0

    if args.current_observations:
        print(
            format_observation_views(
                build_observation_view(projected_state_from_args(args))
            )
        )
        return 0

    if args.current_requirements:
        print(
            format_requirement_views(
                build_requirement_view(projected_state_from_args(args))
            )
        )
        return 0

    if args.current_capabilities:
        print(
            format_capability_views(
                build_capability_view(projected_state_from_args(args))
            )
        )
        return 0

    if args.capability_status:
        print(
            format_capability_inventory(
                build_capability_inventory(projected_state_from_args(args))
            )
        )
        return 0

    if args.capability_candidates:
        filter_text = (
            None
            if args.capability_candidates == "__all__"
            else args.capability_candidates
        )
        status_consumer = CliExecutionStatusConsumer()
        state = projected_state_from_args(args, status_consumer=status_consumer)
        fact_index = _load_or_build_fact_index_from_args(
            args, state, status_consumer=status_consumer
        )
        print(
            json.dumps(
                to_plain(
                    build_capability_candidates(
                        state,
                        filter_text=filter_text,
                        fact_index=fact_index,
                    )
                ),
                indent=2,
                sort_keys=True,
            )
        )
        return 0

    if args.verification_evidence:
        filter_text = (
            None
            if args.verification_evidence == "__all__"
            else args.verification_evidence
        )
        print(
            json.dumps(
                to_plain(
                    build_verification_evidence(
                        projected_state_from_args(
                            args, status_consumer=CliExecutionStatusConsumer()
                        ),
                        filter_text=filter_text,
                    )
                ),
                indent=2,
                sort_keys=True,
            )
        )
        return 0

    if args.capability_promotion_readiness:
        filter_text = (
            None
            if args.capability_promotion_readiness == "__all__"
            else args.capability_promotion_readiness
        )
        status_consumer = CliExecutionStatusConsumer()
        state = projected_state_from_args(args, status_consumer=status_consumer)
        fact_index = _load_or_build_fact_index_from_args(
            args, state, status_consumer=status_consumer
        )
        print(
            json.dumps(
                to_plain(
                    build_capability_promotion_readiness_inspection(
                        state,
                        filter_text=filter_text,
                        fact_index=fact_index,
                    )
                ),
                indent=2,
                sort_keys=True,
            )
        )
        return 0

    if args.capability_verification:
        filter_text = (
            None
            if args.capability_verification == "__all__"
            else args.capability_verification
        )
        status_consumer = CliExecutionStatusConsumer()
        state = projected_state_from_args(args, status_consumer=status_consumer)
        fact_index = _load_or_build_fact_index_from_args(
            args, state, status_consumer=status_consumer
        )
        print(
            json.dumps(
                to_plain(
                    build_capability_verification_inspection(
                        state,
                        filter_text=filter_text,
                        fact_index=fact_index,
                    )
                ),
                indent=2,
                sort_keys=True,
            )
        )
        return 0

    if args.current_issues:
        print(format_issue_views(build_issue_view(projected_state_from_args(args))))
        return 0

    if args.decision_context:
        print(
            format_decision_context_view(
                build_decision_context_view(projected_state_from_args(args))
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
        (
            args.observe
            or args.fact
            or args.alias
            or args.observe_json
            or args.observe_ansible_inventory
            or args.observe_local_host
            or args.observe_prometheus
            or args.observe_repository_source
        )
        and not message
        and not args.http
    ):
        status_consumer = CliExecutionStatusConsumer()
        diagnostics: list[ObservationIngestionDiagnostics] = []
        observed_facts = ingest_observations_from_args(
            args,
            status_consumer=status_consumer,
            diagnostics=diagnostics if args.observe_timings else None,
        )
        emit_status(status_consumer, "done", "Done.", completed=True)
        suppress_observation_rendering = args.quiet_output and (
            args.observe_local_host or bool(args.observe_repository_source)
        )
        if not suppress_observation_rendering:
            if args.observe_prometheus and not args.verbose_observations:
                print(format_observed_fact_summary(observed_facts))
            else:
                print(format_observed_facts(observed_facts))
        if args.observe_timings:
            print(format_observation_ingestion_diagnostics(diagnostics))
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
    try:
        raise SystemExit(main())
    except BrokenPipeError:
        try:
            sys.stdout.close()
        finally:
            raise SystemExit(0)
