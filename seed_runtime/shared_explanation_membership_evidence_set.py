"""Read-only set over already-produced shared explanation membership evidence."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from seed_runtime.shared_explanation_membership_evidence_projection import (
    MEMBERSHIP_STATES,
    BoundedInquiryReference,
    SharedExplanationMembershipEvidenceProjection,
)

SET_CONVENTION = "shared_explanation_membership_evidence_set_v1"


def _jsonable(value: Any) -> Any:
    if isinstance(value, tuple):
        return [_jsonable(v) for v in value]
    if isinstance(value, dict):
        return {k: _jsonable(v) for k, v in value.items()}
    return value


@dataclass(frozen=True)
class IdentityOccurrence:
    identity_kind: str
    identity_ref: str
    result_ref: str
    occurrence_index: int

    def to_json_dict(self) -> dict[str, Any]:
        return _jsonable(asdict(self))


@dataclass(frozen=True)
class SharedExplanationMembershipEvidenceSet:
    artifact_type: str
    producer: str
    bounded_inquiry_ref: str
    bounded_demand_ref: str
    supplied_result_count: int
    collection_empty: bool
    collection_partial: bool
    completeness_claim: str
    membership_results: tuple[SharedExplanationMembershipEvidenceProjection, ...]
    belongs_results: tuple[SharedExplanationMembershipEvidenceProjection, ...]
    does_not_belong_results: tuple[SharedExplanationMembershipEvidenceProjection, ...]
    unknown_results: tuple[SharedExplanationMembershipEvidenceProjection, ...]
    conflict_results: tuple[SharedExplanationMembershipEvidenceProjection, ...]
    state_partitions: dict[str, tuple[str, ...]]
    duplicate_identity_occurrences: tuple[IdentityOccurrence, ...]
    set_boundary: str
    non_selection_boundary: str
    read_only: bool = True
    writes_event_ledger: bool = False
    mutates_cluster: bool = False
    set_convention: str = SET_CONVENTION

    def to_json_dict(self) -> dict[str, Any]:
        return _jsonable(asdict(self))


def build_shared_explanation_membership_evidence_set(
    inquiry: BoundedInquiryReference,
    results: tuple[SharedExplanationMembershipEvidenceProjection, ...],
    *,
    collection_partial: bool = True,
) -> SharedExplanationMembershipEvidenceSet:
    preserved = tuple(results)
    for result in preserved:
        if result.bounded_inquiry_ref != inquiry.inquiry_ref:
            raise ValueError("membership evidence set requires one bounded inquiry reference")
        if result.bounded_demand_ref != inquiry.demand_ref:
            raise ValueError("membership evidence set requires one bounded demand reference")

    state_partition_results: dict[str, tuple[SharedExplanationMembershipEvidenceProjection, ...]] = {
        state: tuple(r for r in preserved if r.membership_state == state)
        for state in MEMBERSHIP_STATES
    }
    partitions: dict[str, tuple[str, ...]] = {
        state: tuple(r.candidate_projection_ref for r in state_partition_results[state])
        for state in MEMBERSHIP_STATES
    }

    occurrences: list[IdentityOccurrence] = []
    for index, result in enumerate(preserved):
        occurrences.append(
            IdentityOccurrence(
                "candidate_projection_ref",
                result.candidate_projection_ref,
                result.candidate_projection_ref,
                index,
            )
        )
        occurrences.append(
            IdentityOccurrence(
                "candidate_source_explanation_ref",
                result.candidate_source_explanation_ref,
                result.candidate_projection_ref,
                index,
            )
        )
        for source_identity in result.duplicate_source_identity_refs:
            occurrences.append(
                IdentityOccurrence(
                    "duplicate_source_identity_ref",
                    source_identity,
                    result.candidate_projection_ref,
                    index,
                )
            )

    return SharedExplanationMembershipEvidenceSet(
        artifact_type="SharedExplanationMembershipEvidenceSet",
        producer="build_shared_explanation_membership_evidence_set",
        bounded_inquiry_ref=inquiry.inquiry_ref,
        bounded_demand_ref=inquiry.demand_ref,
        supplied_result_count=len(preserved),
        collection_empty=not preserved,
        collection_partial=collection_partial,
        completeness_claim="none; supplied collection only",
        membership_results=preserved,
        belongs_results=state_partition_results["belongs"],
        does_not_belong_results=state_partition_results["does_not_belong"],
        unknown_results=state_partition_results["unknown"],
        conflict_results=state_partition_results["conflict"],
        state_partitions=partitions,
        duplicate_identity_occurrences=tuple(occurrences),
        set_boundary=(
            "Consumes one explicit bounded inquiry reference and supplied "
            "SharedExplanationMembershipEvidenceProjection records; preserves collection identity only."
        ),
        non_selection_boundary=(
            "Does not select rendering projections, rank, sequence, compose, deduplicate, infer semantic "
            "relevance, fabricate missing Unknowns, create handoffs, authorize, execute, write events, or mutate."
        ),
        read_only=all(r.read_only for r in preserved),
        writes_event_ledger=False,
        mutates_cluster=False,
    )


def shared_explanation_membership_evidence_set_json(
    s: SharedExplanationMembershipEvidenceSet,
) -> dict[str, Any]:
    return s.to_json_dict()


def format_shared_explanation_membership_evidence_set(
    s: SharedExplanationMembershipEvidenceSet,
) -> str:
    lines = [
        "Shared Explanation Membership Evidence Set",
        f"bounded_inquiry_ref: {s.bounded_inquiry_ref}",
        f"bounded_demand_ref: {s.bounded_demand_ref or 'none'}",
        f"supplied_result_count: {s.supplied_result_count}",
        f"collection_empty: {str(s.collection_empty).lower()}",
        f"collection_partial: {str(s.collection_partial).lower()}",
        f"completeness_claim: {s.completeness_claim}",
        f"set_boundary: {s.set_boundary}",
        f"non_selection_boundary: {s.non_selection_boundary}",
        f"read_only: {str(s.read_only).lower()}",
        f"writes_event_ledger: {str(s.writes_event_ledger).lower()}",
        f"mutates_cluster: {str(s.mutates_cluster).lower()}",
        "all_supplied_result_identities:",
    ]
    lines += [f"- {r.candidate_projection_ref}" for r in s.membership_results] or ["- none"]
    lines.append("belongs_result_identities:")
    lines += [f"- {r.candidate_projection_ref}" for r in s.belongs_results] or ["- none"]
    lines.append("state_partitions:")
    for state in MEMBERSHIP_STATES:
        lines.append(f"  {state}:")
        lines += [f"  - {ref}" for ref in s.state_partitions[state]] or ["  - none"]
    lines.append("duplicate_identity_occurrences:")
    lines += [
        f"- {o.identity_kind} {o.identity_ref} in {o.result_ref} occurrence_index={o.occurrence_index}"
        for o in s.duplicate_identity_occurrences
    ] or ["- none"]
    return "\n".join(lines)
