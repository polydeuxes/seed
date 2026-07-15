"""Read-only membership evidence for one shared explanation rendering projection."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from seed_runtime.shared_explanation_rendering_projection import SharedExplanationRenderingProjection

MEMBERSHIP_STATES = ("belongs", "does_not_belong", "unknown", "conflict")
PROJECTION_CONVENTION = "shared_explanation_membership_evidence_projection_v1"


@dataclass(frozen=True)
class BoundedInquiryReference:
    inquiry_ref: str
    demand_ref: str = ""

    def to_json_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class PreservedLineageEvidence:
    positive_inquiry_refs: tuple[str, ...] = ()
    positive_demand_refs: tuple[str, ...] = ()
    incompatible_inquiry_refs: tuple[str, ...] = ()
    incompatible_demand_refs: tuple[str, ...] = ()
    missing_lineage_refs: tuple[str, ...] = ()
    supporting_references: tuple[str, ...] = ()
    incompatible_references: tuple[str, ...] = ()
    source_identity_refs: tuple[str, ...] = ()

    def to_json_dict(self) -> dict[str, Any]:
        return _jsonable(asdict(self))


@dataclass(frozen=True)
class SharedExplanationMembershipEvidenceProjection:
    artifact_type: str
    producer: str
    bounded_inquiry_ref: str
    bounded_demand_ref: str
    candidate_projection_ref: str
    candidate_source_explanation_ref: str
    candidate_source_artifact_owner: str
    membership_state: str
    membership_reason: str
    supporting_references: tuple[str, ...]
    incompatible_references: tuple[str, ...]
    missing_lineage_refs: tuple[str, ...]
    conflicting_references: tuple[str, ...]
    duplicate_source_identity_refs: tuple[str, ...]
    evidence_input_boundary: str
    non_selection_boundary: str
    read_only: bool = True
    writes_event_ledger: bool = False
    mutates_cluster: bool = False
    projection_convention: str = PROJECTION_CONVENTION

    def __post_init__(self) -> None:
        if self.membership_state not in MEMBERSHIP_STATES:
            raise ValueError("invalid shared explanation membership state")

    def to_json_dict(self) -> dict[str, Any]:
        return _jsonable(asdict(self))


def _jsonable(value: Any) -> Any:
    if isinstance(value, tuple):
        return [_jsonable(v) for v in value]
    if isinstance(value, dict):
        return {k: _jsonable(v) for k, v in value.items()}
    return value


def _tuple(values: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(str(v) for v in values if v)


def _has_duplicate(values: tuple[str, ...]) -> bool:
    return len(set(values)) != len(values)


def project_shared_explanation_membership_evidence(
    inquiry: BoundedInquiryReference,
    candidate: SharedExplanationRenderingProjection,
    lineage: PreservedLineageEvidence,
) -> SharedExplanationMembershipEvidenceProjection:
    """Project membership from explicit preserved lineage only.

    The function consumes exactly one inquiry reference, one already-renderable
    shared explanation projection, and one caller-supplied lineage evidence
    record. It never looks up source artifacts and never infers membership from
    shared wording, source state, stage, or explanation text.
    """
    positive_inquiries = _tuple(lineage.positive_inquiry_refs)
    positive_demands = _tuple(lineage.positive_demand_refs)
    incompatible_inquiries = _tuple(lineage.incompatible_inquiry_refs)
    incompatible_demands = _tuple(lineage.incompatible_demand_refs)
    missing = _tuple(lineage.missing_lineage_refs)
    supporting = _tuple(lineage.supporting_references)
    incompatible = _tuple(lineage.incompatible_references)
    source_identities = _tuple(lineage.source_identity_refs)

    target_positive = inquiry.inquiry_ref in positive_inquiries or (
        bool(inquiry.demand_ref) and inquiry.demand_ref in positive_demands
    )
    incompatible_to_target = bool(incompatible_inquiries or incompatible_demands or incompatible)
    conflicting = target_positive and incompatible_to_target

    if conflicting:
        state = "conflict"
        reason = "explicit lineage preserves both target-positive and incompatible references"
    elif target_positive:
        state = "belongs"
        reason = "explicit positive lineage ties the candidate to this bounded inquiry"
    elif incompatible_to_target:
        state = "does_not_belong"
        reason = "explicit positive lineage ties the candidate to another incompatible inquiry or demand"
    else:
        state = "unknown"
        reason = "explicit lineage evidence is insufficient for membership or non-membership"

    if state == "unknown" and not missing:
        missing = ("lineage evidence absent or does not reference the bounded inquiry",)

    duplicate_visible = source_identities if _has_duplicate(source_identities) else ()
    conflicting_refs = _tuple((*supporting, *incompatible)) if state == "conflict" else ()

    return SharedExplanationMembershipEvidenceProjection(
        artifact_type="SharedExplanationMembershipEvidenceProjection",
        producer="SharedExplanationMembershipEvidenceProjection",
        bounded_inquiry_ref=inquiry.inquiry_ref,
        bounded_demand_ref=inquiry.demand_ref,
        candidate_projection_ref=candidate.source_explanation_identity,
        candidate_source_explanation_ref=candidate.source_explanation_identity,
        candidate_source_artifact_owner=candidate.source_artifact_owner,
        membership_state=state,
        membership_reason=reason,
        supporting_references=supporting,
        incompatible_references=incompatible,
        missing_lineage_refs=missing,
        conflicting_references=conflicting_refs,
        duplicate_source_identity_refs=duplicate_visible,
        evidence_input_boundary=(
            "Consumes one bounded inquiry reference, one SharedExplanationRenderingProjection, "
            "and explicit preserved lineage evidence; performs no lookup and no semantic guessing."
        ),
        non_selection_boundary=(
            "Produces one per-candidate evidence result only; does not select, rank, deduplicate, "
            "sequence, compose, authorize, execute, create handoffs, or mutate state."
        ),
        read_only=candidate.read_only,
        writes_event_ledger=False,
        mutates_cluster=False,
    )


def shared_explanation_membership_evidence_json(
    p: SharedExplanationMembershipEvidenceProjection,
) -> dict[str, Any]:
    return p.to_json_dict()


def format_shared_explanation_membership_evidence(
    p: SharedExplanationMembershipEvidenceProjection,
) -> str:
    lines = [
        "Shared Explanation Membership Evidence Projection",
        f"bounded_inquiry_ref: {p.bounded_inquiry_ref}",
        f"bounded_demand_ref: {p.bounded_demand_ref or 'none'}",
        f"candidate_projection_ref: {p.candidate_projection_ref}",
        f"candidate_source_artifact_owner: {p.candidate_source_artifact_owner}",
        f"membership_state: {p.membership_state}",
        f"membership_reason: {p.membership_reason}",
        f"evidence_input_boundary: {p.evidence_input_boundary}",
        f"non_selection_boundary: {p.non_selection_boundary}",
        f"read_only: {str(p.read_only).lower()}",
        f"writes_event_ledger: {str(p.writes_event_ledger).lower()}",
        f"mutates_cluster: {str(p.mutates_cluster).lower()}",
    ]
    for label, values in (
        ("supporting_references", p.supporting_references),
        ("incompatible_references", p.incompatible_references),
        ("missing_lineage_refs", p.missing_lineage_refs),
        ("conflicting_references", p.conflicting_references),
        ("duplicate_source_identity_refs", p.duplicate_source_identity_refs),
    ):
        lines.append(label + ":")
        lines += [f"- {v}" for v in values] or ["- none"]
    return "\n".join(lines)
