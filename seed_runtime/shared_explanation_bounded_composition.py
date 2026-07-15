"""Read-only bounded composition over one shared explanation encounter sequencing."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from seed_runtime.shared_explanation_encounter_sequencing import (
    SharedExplanationEncounterSequencing,
)

COMPOSITION_CONVENTION = "shared_explanation_bounded_composition_v1"


def _jsonable(value: Any) -> Any:
    if isinstance(value, tuple):
        return [_jsonable(v) for v in value]
    if isinstance(value, dict):
        return {k: _jsonable(v) for k, v in value.items()}
    return value


@dataclass(frozen=True)
class SharedExplanationBoundedComposition:
    artifact_type: str
    producer: str
    presentation_ref: str
    bounded_inquiry_ref: str
    bounded_demand_ref: str
    source_sequencing_artifact_type: str
    source_sequencing_producer: str
    source_sequencing_convention: str
    constitutional_derivation_projection_refs: tuple[str, ...]
    encounter_sequence_results: tuple[Any, ...]
    encounter_sequence_projection_refs: tuple[str, ...]
    sequencing_evidence_by_projection_ref: dict[str, tuple[Any, ...]]
    optional_roles_by_projection_ref: dict[str, str]
    unsequenced_admitted_results: tuple[Any, ...]
    unsequenced_admitted_projection_refs: tuple[str, ...]
    belonging_but_unadmitted_results: tuple[Any, ...]
    non_member_results: tuple[Any, ...]
    unknown_results: tuple[Any, ...]
    conflict_results: tuple[Any, ...]
    duplicate_identity_occurrences: tuple[Any, ...]
    composition_boundary: str
    inquiry_status_boundary: str
    non_interpretation_boundary: str
    source_identity_boundary: str
    read_only: bool = True
    writes_event_ledger: bool = False
    mutates_cluster: bool = False
    composition_convention: str = COMPOSITION_CONVENTION

    def to_json_dict(self) -> dict[str, Any]:
        return _jsonable(asdict(self))


def compose_shared_explanation_bounded_view(
    sequencing: SharedExplanationEncounterSequencing,
) -> SharedExplanationBoundedComposition:
    """Preserve one sequencing artifact as one complete bounded presentation snapshot.

    Composition is a read-only boundary over exactly the supplied sequencing artifact.
    It does not reorder, select, assign roles, deduplicate, resolve uncertainty,
    reinterpret source meaning, record, or mutate cluster state.
    """
    return SharedExplanationBoundedComposition(
        artifact_type="SharedExplanationBoundedComposition",
        producer="compose_shared_explanation_bounded_view",
        presentation_ref=sequencing.presentation_ref,
        bounded_inquiry_ref=sequencing.bounded_inquiry_ref,
        bounded_demand_ref=sequencing.bounded_demand_ref,
        source_sequencing_artifact_type=sequencing.artifact_type,
        source_sequencing_producer=sequencing.producer,
        source_sequencing_convention=sequencing.sequencing_convention,
        constitutional_derivation_projection_refs=sequencing.constitutional_derivation_projection_refs,
        encounter_sequence_results=sequencing.encounter_sequence_results,
        encounter_sequence_projection_refs=sequencing.encounter_sequence_projection_refs,
        sequencing_evidence_by_projection_ref=sequencing.sequencing_evidence_by_projection_ref,
        optional_roles_by_projection_ref=sequencing.optional_roles_by_projection_ref,
        unsequenced_admitted_results=sequencing.unsequenced_admitted_results,
        unsequenced_admitted_projection_refs=sequencing.unsequenced_admitted_projection_refs,
        belonging_but_unadmitted_results=sequencing.belonging_but_unadmitted_results,
        non_member_results=sequencing.non_member_results,
        unknown_results=sequencing.unknown_results,
        conflict_results=sequencing.conflict_results,
        duplicate_identity_occurrences=sequencing.duplicate_identity_occurrences,
        composition_boundary=(
            "Consumes exactly one SharedExplanationEncounterSequencing and preserves it as one "
            "complete bounded presentation snapshot."
        ),
        inquiry_status_boundary=(
            "A complete bounded presentation is not a completed inquiry; it does not imply the "
            "operator is finished, the inquiry is closed, or later intervention cannot constrain, "
            "expand, fork, supersede, or reopen the inquiry frontier."
        ),
        non_interpretation_boundary=(
            "Does not reorder, select, assign roles, deduplicate, resolve Unknowns or conflicts, "
            "reinterpret source meaning, communicate step-wise, bind conversation references, "
            "transition frontiers, speak, transport, record, write events, or mutate cluster state."
        ),
        source_identity_boundary=(
            "Source identities, sequencing evidence, read-only boundaries, non-members, duplicates, "
            "and belonging-but-unadmitted material are preserved from the supplied sequencing artifact."
        ),
        read_only=sequencing.read_only,
        writes_event_ledger=False,
        mutates_cluster=False,
    )


def shared_explanation_bounded_composition_json(
    composition: SharedExplanationBoundedComposition,
) -> dict[str, Any]:
    return composition.to_json_dict()


def format_shared_explanation_bounded_composition(
    composition: SharedExplanationBoundedComposition,
) -> str:
    lines = [
        "Shared Explanation Bounded Composition",
        f"presentation_ref: {composition.presentation_ref}",
        f"bounded_inquiry_ref: {composition.bounded_inquiry_ref}",
        f"bounded_demand_ref: {composition.bounded_demand_ref or 'none'}",
        f"source_sequencing_artifact_type: {composition.source_sequencing_artifact_type}",
        f"source_sequencing_convention: {composition.source_sequencing_convention}",
        f"composition_boundary: {composition.composition_boundary}",
        f"inquiry_status_boundary: {composition.inquiry_status_boundary}",
        f"non_interpretation_boundary: {composition.non_interpretation_boundary}",
        f"source_identity_boundary: {composition.source_identity_boundary}",
        f"read_only: {str(composition.read_only).lower()}",
        f"writes_event_ledger: {str(composition.writes_event_ledger).lower()}",
        f"mutates_cluster: {str(composition.mutates_cluster).lower()}",
        "constitutional_derivation_projection_refs:",
    ]
    lines += [f"- {ref}" for ref in composition.constitutional_derivation_projection_refs] or ["- none"]
    lines.append("encounter_sequence_projection_refs:")
    lines += [f"- {ref}" for ref in composition.encounter_sequence_projection_refs] or ["- none"]
    lines.append("unsequenced_admitted_projection_refs:")
    lines += [f"- {ref}" for ref in composition.unsequenced_admitted_projection_refs] or ["- none"]
    lines.append("optional_roles_by_projection_ref:")
    for ref, role in composition.optional_roles_by_projection_ref.items():
        lines.append(f"  {ref}: {role}")
    if not composition.optional_roles_by_projection_ref:
        lines.append("  none")
    for label, results in (
        ("belonging_but_unadmitted_projection_refs", composition.belonging_but_unadmitted_results),
        ("non_member_projection_refs", composition.non_member_results),
        ("unknown_projection_refs", composition.unknown_results),
        ("conflict_projection_refs", composition.conflict_results),
    ):
        lines.append(label + ":")
        lines += [f"- {r.candidate_projection_ref}" for r in results] or ["- none"]
    lines.append("duplicate_identity_occurrences:")
    lines += [
        f"- {o.identity_kind} {o.identity_ref} in {o.result_ref} occurrence_index={o.occurrence_index}"
        for o in composition.duplicate_identity_occurrences
    ] or ["- none"]
    return "\n".join(lines)
