"""Presentation-local encounter sequencing for admitted shared explanations."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from seed_runtime.shared_explanation_presentation_admission import (
    SharedExplanationPresentationAdmission,
)

SEQUENCING_CONVENTION = "shared_explanation_encounter_sequencing_v1"
SUPPORTED_OPTIONAL_ROLES = (
    "answer",
    "immediate_reason",
    "support",
    "limitations",
    "next_lawful_movement",
)


def _jsonable(value: Any) -> Any:
    if isinstance(value, tuple):
        return [_jsonable(v) for v in value]
    if isinstance(value, dict):
        return {k: _jsonable(v) for k, v in value.items()}
    return value


@dataclass(frozen=True)
class PresentationLocalSequencingEvidence:
    projection_ref: str
    encounter_order: int
    supporting_references: tuple[str, ...] = ()
    optional_role: str = ""

    def __post_init__(self) -> None:
        if self.encounter_order < 0:
            raise ValueError("encounter_order must be explicit and non-negative")
        if self.optional_role and self.optional_role not in SUPPORTED_OPTIONAL_ROLES:
            raise ValueError("unsupported optional encounter role")

    def to_json_dict(self) -> dict[str, Any]:
        return _jsonable(asdict(self))


@dataclass(frozen=True)
class SharedExplanationEncounterSequencing:
    artifact_type: str
    producer: str
    presentation_ref: str
    bounded_inquiry_ref: str
    bounded_demand_ref: str
    constitutional_derivation_projection_refs: tuple[str, ...]
    encounter_sequence_results: tuple[Any, ...]
    encounter_sequence_projection_refs: tuple[str, ...]
    sequencing_evidence_by_projection_ref: dict[
        str, tuple[PresentationLocalSequencingEvidence, ...]
    ]
    optional_roles_by_projection_ref: dict[str, str]
    unsequenced_admitted_results: tuple[Any, ...]
    unsequenced_admitted_projection_refs: tuple[str, ...]
    belonging_but_unadmitted_results: tuple[Any, ...]
    non_member_results: tuple[Any, ...]
    unknown_results: tuple[Any, ...]
    conflict_results: tuple[Any, ...]
    duplicate_identity_occurrences: tuple[Any, ...]
    sequencing_boundary: str
    non_composition_boundary: str
    read_only: bool = True
    writes_event_ledger: bool = False
    mutates_cluster: bool = False
    sequencing_convention: str = SEQUENCING_CONVENTION

    def to_json_dict(self) -> dict[str, Any]:
        return _jsonable(asdict(self))


def sequence_shared_explanation_encounters(
    admission: SharedExplanationPresentationAdmission,
    sequencing_evidence: tuple[PresentationLocalSequencingEvidence, ...],
) -> SharedExplanationEncounterSequencing:
    """Order admitted projections only from explicit presentation-local evidence."""
    admitted_refs = set(admission.admitted_to_sequencing_projection_refs)
    evidence_by_ref: dict[str, list[PresentationLocalSequencingEvidence]] = {}
    for evidence in sequencing_evidence:
        if evidence.projection_ref in admitted_refs:
            evidence_by_ref.setdefault(evidence.projection_ref, []).append(evidence)

    ordered_ref_keys = sorted(
        evidence_by_ref,
        key=lambda ref: min(e.encounter_order for e in evidence_by_ref[ref]),
    )
    sequenced = tuple(
        result
        for ref in ordered_ref_keys
        for result in admission.admitted_to_sequencing_results
        if result.candidate_projection_ref == ref
    )
    sequenced_ids = {id(result) for result in sequenced}
    unsequenced = tuple(
        result
        for result in admission.admitted_to_sequencing_results
        if id(result) not in sequenced_ids
    )

    return SharedExplanationEncounterSequencing(
        artifact_type="SharedExplanationEncounterSequencing",
        producer="sequence_shared_explanation_encounters",
        presentation_ref=admission.presentation_ref,
        bounded_inquiry_ref=admission.bounded_inquiry_ref,
        bounded_demand_ref=admission.bounded_demand_ref,
        constitutional_derivation_projection_refs=admission.admitted_to_sequencing_projection_refs,
        encounter_sequence_results=sequenced,
        encounter_sequence_projection_refs=tuple(
            r.candidate_projection_ref for r in sequenced
        ),
        sequencing_evidence_by_projection_ref={
            ref: tuple(values) for ref, values in evidence_by_ref.items()
        },
        optional_roles_by_projection_ref={
            ref: evidence.optional_role
            for ref, values in evidence_by_ref.items()
            for evidence in values
            if evidence.optional_role
        },
        unsequenced_admitted_results=unsequenced,
        unsequenced_admitted_projection_refs=tuple(
            r.candidate_projection_ref for r in unsequenced
        ),
        belonging_but_unadmitted_results=admission.belonging_but_unadmitted_results,
        non_member_results=admission.non_member_results,
        unknown_results=admission.unknown_results,
        conflict_results=admission.conflict_results,
        duplicate_identity_occurrences=admission.duplicate_identity_occurrences,
        sequencing_boundary=(
            "Consumes one SharedExplanationPresentationAdmission and explicit presentation-local "
            "sequencing evidence; admitted projections may be reordered for operator encounter."
        ),
        non_composition_boundary=(
            "Encounter sequencing preserves constitutional derivation order separately; it is not "
            "composition, constitutional ranking, deduplication, membership, admission, authorization, "
            "execution, event writing, or cluster mutation."
        ),
        read_only=admission.read_only,
        writes_event_ledger=False,
        mutates_cluster=False,
    )


def shared_explanation_encounter_sequencing_json(
    sequencing: SharedExplanationEncounterSequencing,
) -> dict[str, Any]:
    return sequencing.to_json_dict()


def format_shared_explanation_encounter_sequencing(
    sequencing: SharedExplanationEncounterSequencing,
) -> str:
    lines = [
        "Shared Explanation Encounter Sequencing",
        f"presentation_ref: {sequencing.presentation_ref}",
        f"bounded_inquiry_ref: {sequencing.bounded_inquiry_ref}",
        f"bounded_demand_ref: {sequencing.bounded_demand_ref or 'none'}",
        f"sequencing_boundary: {sequencing.sequencing_boundary}",
        f"non_composition_boundary: {sequencing.non_composition_boundary}",
        f"read_only: {str(sequencing.read_only).lower()}",
        f"writes_event_ledger: {str(sequencing.writes_event_ledger).lower()}",
        f"mutates_cluster: {str(sequencing.mutates_cluster).lower()}",
        "constitutional_derivation_projection_refs:",
    ]
    lines += [
        f"- {ref}" for ref in sequencing.constitutional_derivation_projection_refs
    ] or ["- none"]
    lines.append("encounter_sequence_projection_refs:")
    lines += [f"- {ref}" for ref in sequencing.encounter_sequence_projection_refs] or [
        "- none"
    ]
    lines.append("unsequenced_admitted_projection_refs:")
    lines += [
        f"- {ref}" for ref in sequencing.unsequenced_admitted_projection_refs
    ] or ["- none"]
    lines.append("optional_roles_by_projection_ref:")
    for ref, role in sequencing.optional_roles_by_projection_ref.items():
        lines.append(f"  {ref}: {role}")
    if not sequencing.optional_roles_by_projection_ref:
        lines.append("  none")
    return "\n".join(lines)
