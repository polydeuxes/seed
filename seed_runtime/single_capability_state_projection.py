"""Immutable read-only projection for one normalized capability string."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from seed_runtime.capabilities import normalize_capability
from seed_runtime.capability_candidates import CapabilityCandidateInspection
from seed_runtime.capability_catalog import CapabilityCatalog, CapabilityRecommendation
from seed_runtime.capability_inventory import CapabilityInventoryEntry, build_capability_inventory
from seed_runtime.capability_verification import CapabilityVerificationInspection
from seed_runtime.models import ToolNeed, ToolSpec
from seed_runtime.serialization import to_plain
from seed_runtime.state import State
from seed_runtime.verification_evidence import VerificationEvidenceInspection

_BOUNDARY_NOTES = (
    "single_capability_projection_not_global_capability_identity",
    "same_normalized_string_correlation_only",
    "requested_state_proves_demand_only",
    "catalog_known_proves_metadata_presence_only",
    "provider_recommendations_are_advisory_unselected",
    "registered_operations_are_contract_associations_only",
    "candidate_evidence_is_not_capability_availability",
    "verification_evidence_is_not_verification_failure_or_success",
    "verification_status_comes_from_existing_inventory_owner",
    "freshness_comes_from_existing_inventory_support",
    "no_provider_selection",
    "no_operation_selection",
    "no_capability_verification",
    "no_execution_or_authorization",
    "read_only_projection",
)


@dataclass(frozen=True)
class RegisteredOperationAssociation:
    name: str
    toolkit_id: str
    capabilities: list[str] = field(default_factory=list)
    fallback_matched_name: bool = False
    boundary: str = "operation_contract_association_only"


@dataclass(frozen=True)
class SingleCapabilityStateProjection:
    capability_name: str
    requested: list[ToolNeed] = field(default_factory=list)
    catalog_known: bool | str = "unknown"
    provider_recommendations: list[CapabilityRecommendation] = field(default_factory=list)
    registered_operations: list[RegisteredOperationAssociation] = field(default_factory=list)
    candidate_evidence: list[Any] = field(default_factory=list)
    verification_evidence: list[Any] = field(default_factory=list)
    verification_status: str = "unknown"
    verification_support: Any = None
    freshness: Any = None
    unknowns: list[str] = field(default_factory=list)
    boundary_notes: list[str] = field(default_factory=lambda: list(_BOUNDARY_NOTES))
    read_only: bool = True
    writes_event_ledger: bool = False
    mutates_cluster: bool = False


def build_single_capability_state_projection(
    state: State,
    capability_name: str,
    *,
    catalog: CapabilityCatalog | None = None,
    candidate_inspection: CapabilityCandidateInspection | None = None,
    verification_evidence_inspection: VerificationEvidenceInspection | None = None,
    verification_inspection: CapabilityVerificationInspection | None = None,
    inventory: list[CapabilityInventoryEntry] | None = None,
    now: datetime | None = None,
) -> SingleCapabilityStateProjection:
    """Compose existing owner-produced artifacts for one capability string only."""

    normalized = normalize_capability(capability_name)
    unknowns: list[str] = []

    requested = [
        need for need in state.tool_needs.values()
        if normalize_capability(need.capability) == normalized
    ]

    catalog_entry = None if catalog is None else catalog.get(normalized)
    if catalog is None:
        unknowns.append("catalog_owner_artifact_missing")

    operations = [_operation_assoc(tool, normalized) for tool in state.tools.values()]
    operations = sorted([op for op in operations if op is not None], key=lambda op: op.name)

    candidate_evidence: list[Any] = []
    if candidate_inspection is None:
        unknowns.append("candidate_inspection_owner_artifact_missing")
    else:
        candidate_evidence = [
            candidate for candidate in candidate_inspection.candidates
            if normalize_capability(candidate.candidate) == normalized
        ]

    verification_evidence: list[Any] = []
    if verification_evidence_inspection is None:
        unknowns.append("verification_evidence_owner_artifact_missing")
    else:
        verification_evidence = [
            evidence for evidence in verification_evidence_inspection.evidence
            if normalize_capability(evidence.candidate) == normalized
        ]

    inventory_entry = None
    entries = inventory
    if entries is None:
        entries = build_capability_inventory(state, now=now or datetime.now(timezone.utc))
    matching_inventory = [
        entry for entry in entries if normalize_capability(entry.capability) == normalized
    ]
    if matching_inventory:
        inventory_entry = sorted(
            matching_inventory,
            key=lambda entry: (
                (entry.support is not None),
                _verification_state_rank(entry.state),
                entry.latest_observed_at or entry.observed_at or datetime.min.replace(tzinfo=timezone.utc),
                entry.capability,
            ),
            reverse=True,
        )[0]

    verification_status = "unknown"
    verification_support = None
    freshness = None
    if inventory_entry is None:
        unknowns.append("capability_inventory_entry_missing")
    else:
        verification_status = inventory_entry.state
        verification_support = inventory_entry.support
        freshness = {
            "observed_at": inventory_entry.observed_at,
            "latest_observed_at": inventory_entry.latest_observed_at,
            "age_seconds": inventory_entry.age_seconds,
            "reason": inventory_entry.reason,
        }

    if verification_inspection is None:
        unknowns.append("verification_inspection_owner_artifact_missing")

    return SingleCapabilityStateProjection(
        capability_name=normalized,
        requested=sorted(requested, key=lambda need: need.id),
        catalog_known=("unknown" if catalog is None else catalog_entry is not None),
        provider_recommendations=([] if catalog_entry is None else list(catalog_entry.recommendations)),
        registered_operations=operations,
        candidate_evidence=candidate_evidence,
        verification_evidence=verification_evidence,
        verification_status=verification_status,
        verification_support=verification_support,
        freshness=freshness,
        unknowns=unknowns,
    )


def _verification_state_rank(state: str) -> int:
    return {
        "verified": 4,
        "provider_reported": 3,
        "stale": 2,
        "unverified": 1,
        "unknown": 0,
    }.get(state, 0)


def _operation_assoc(tool: ToolSpec, normalized: str) -> RegisteredOperationAssociation | None:
    capabilities = list(tool.capabilities)
    if normalized in {normalize_capability(capability) for capability in capabilities}:
        return RegisteredOperationAssociation(tool.name, tool.toolkit_id, capabilities)
    if normalize_capability(tool.name) == normalized:
        return RegisteredOperationAssociation(tool.name, tool.toolkit_id, capabilities, True)
    return None


def single_capability_state_projection_json(projection: SingleCapabilityStateProjection) -> dict[str, Any]:
    return to_plain(projection)


def format_single_capability_state_projection(projection: SingleCapabilityStateProjection) -> str:
    lines = [
        f"Single capability state projection: {projection.capability_name}",
        "Boundary: read-only immutable composition; same normalized string correlation only, not a global capability identity.",
        f"read_only: {str(projection.read_only).lower()}",
        f"writes_event_ledger: {str(projection.writes_event_ledger).lower()}",
        f"mutates_cluster: {str(projection.mutates_cluster).lower()}",
        f"requested: {len(projection.requested)} demand artifact(s)",
        f"catalog_known: {projection.catalog_known}",
        f"provider_recommendations: {len(projection.provider_recommendations)} advisory unselected record(s)",
        f"registered_operations: {len(projection.registered_operations)} contract association(s)",
        f"candidate_evidence: {len(projection.candidate_evidence)} owner-produced candidate record(s); empty is not capability absence",
        f"verification_evidence: {len(projection.verification_evidence)} owner-produced evidence record(s); empty is not verification failure",
        f"verification_status: {projection.verification_status}",
        f"unknowns: {', '.join(projection.unknowns) if projection.unknowns else 'none'}",
        "boundary_notes:",
    ]
    lines.extend(f"  - {note}" for note in projection.boundary_notes)
    if projection.registered_operations:
        lines.append("registered_operation_names:")
        lines.extend(f"  - {op.name} (selection: none)" for op in projection.registered_operations)
    if projection.provider_recommendations:
        lines.append("provider_recommendation_names:")
        lines.extend(f"  - {rec.provider} (selected: false)" for rec in projection.provider_recommendations)
    return "\n".join(lines)
