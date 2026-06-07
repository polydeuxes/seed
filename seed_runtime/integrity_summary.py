"""Read-only Projection Integrity Summary composition.

The Projection Integrity Summary is a small read model over existing projected
State integrity signals. It aggregates already-derived counts only: it does not
create facts or evidence, execute Runtime behavior, call providers, verify
capabilities, refresh stale facts, resolve contradictions, or mutate projected
State.
"""

from __future__ import annotations

from collections import Counter
import copy
from dataclasses import dataclass, field

from seed_runtime.capability_inventory import (
    CapabilityInventoryEntry,
    build_capability_inventory,
)
from seed_runtime.contradictions import Contradiction, build_contradictions
from seed_runtime.evidence_graph import EvidenceSummary, build_evidence_summary
from seed_runtime.facts import FactConflict, StaleFactRefreshRecommendation
from seed_runtime.state import GraphValidationIssue, State


@dataclass(frozen=True)
class ProjectionIntegritySummary:
    """Aggregate existing integrity signals from projected State.

    Counts preserve the meaning of their source structures. They are integrity
    signals, not truth, correctness, health, execution, repair, or provider
    availability decisions.
    """

    unsupported_fact_count: int
    fact_conflict_count: int
    contradiction_count: int
    graph_issue_count: int
    stale_fact_count: int
    refresh_recommendation_count: int
    verified_capability_count: int
    unverified_capability_count: int
    stale_capability_count: int
    unknown_capability_count: int
    provider_reported_capability_count: int
    caveats: list[str] = field(default_factory=list)
    projection_version: str = "v1"
    last_event_id: str | None = None


DEFAULT_INTEGRITY_SUMMARY_CAVEATS: tuple[str, ...] = (
    "Integrity signals are projection-backed counts, not truth or correctness judgments.",
    "Unsupported, unverified, stale, contradicted, or missing evidence does not mean false.",
    "Refresh recommendations are inventory signals only; no refresh or verification is executed.",
)


def build_projection_integrity_summary(
    state: State,
    *,
    evidence_summary: EvidenceSummary | None = None,
    fact_conflicts: list[FactConflict] | None = None,
    contradictions: list[Contradiction] | None = None,
    graph_issues: list[GraphValidationIssue] | None = None,
    stale_facts_count: int | None = None,
    refresh_recommendations: list[StaleFactRefreshRecommendation] | None = None,
    capability_inventory: list[CapabilityInventoryEntry] | None = None,
) -> ProjectionIntegritySummary:
    """Compose a deterministic read-only integrity summary from existing views.

    Optional arguments allow callers that already built a source view to pass it
    through, avoiding duplicated work while preserving the source semantics.
    """

    existing_evidence_summary = evidence_summary or build_evidence_summary(state)
    existing_fact_conflicts = (
        fact_conflicts
        if fact_conflicts is not None
        else copy.deepcopy(state).get_fact_conflicts()
    )
    existing_contradictions = (
        contradictions if contradictions is not None else build_contradictions(state)
    )
    existing_graph_issues = (
        graph_issues if graph_issues is not None else state.get_graph_issues()
    )
    existing_stale_fact_count = (
        stale_facts_count
        if stale_facts_count is not None
        else len(state.get_stale_facts())
    )
    existing_refresh_recommendations = (
        refresh_recommendations
        if refresh_recommendations is not None
        else state.get_stale_fact_refresh_recommendations()
    )
    existing_capability_inventory = (
        capability_inventory
        if capability_inventory is not None
        else build_capability_inventory(copy.deepcopy(state))
    )
    capability_counts = Counter(entry.state for entry in existing_capability_inventory)

    return ProjectionIntegritySummary(
        unsupported_fact_count=existing_evidence_summary.unsupported_fact_count,
        fact_conflict_count=len(existing_fact_conflicts),
        contradiction_count=len(existing_contradictions),
        graph_issue_count=len(existing_graph_issues),
        stale_fact_count=existing_stale_fact_count,
        refresh_recommendation_count=len(existing_refresh_recommendations),
        verified_capability_count=capability_counts["verified"],
        unverified_capability_count=capability_counts["unverified"],
        stale_capability_count=capability_counts["stale"],
        unknown_capability_count=capability_counts["unknown"],
        provider_reported_capability_count=capability_counts["provider_reported"],
        caveats=list(DEFAULT_INTEGRITY_SUMMARY_CAVEATS),
        projection_version=state.projection_version,
        last_event_id=state.last_event_id,
    )
