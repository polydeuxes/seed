"""Presentation-local admission over shared explanation membership evidence sets."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from seed_runtime.shared_explanation_membership_evidence_set import (
    SharedExplanationMembershipEvidenceSet,
)

ADMISSION_CONVENTION = "shared_explanation_presentation_admission_v1"


def _jsonable(value: Any) -> Any:
    if isinstance(value, tuple):
        return [_jsonable(v) for v in value]
    if isinstance(value, dict):
        return {k: _jsonable(v) for k, v in value.items()}
    return value


@dataclass(frozen=True)
class RequestedPresentationBoundary:
    presentation_ref: str
    bounded_inquiry_ref: str
    bounded_demand_ref: str = ""

    def to_json_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class PresentationAdmissionEvidence:
    presentation_ref: str
    admitted_projection_refs: tuple[str, ...] = ()
    supporting_references: tuple[str, ...] = ()
    non_admission_reasons_by_projection_ref: dict[str, tuple[str, ...]] | None = None

    def to_json_dict(self) -> dict[str, Any]:
        return _jsonable(asdict(self))


@dataclass(frozen=True)
class SharedExplanationPresentationAdmission:
    artifact_type: str
    producer: str
    presentation_ref: str
    bounded_inquiry_ref: str
    bounded_demand_ref: str
    supplied_result_count: int
    admitted_to_sequencing_results: tuple[Any, ...]
    admitted_to_sequencing_projection_refs: tuple[str, ...]
    belonging_but_unadmitted_results: tuple[Any, ...]
    belonging_but_unadmitted_projection_refs: tuple[str, ...]
    non_admission_reasons_by_projection_ref: dict[str, tuple[str, ...]]
    non_member_results: tuple[Any, ...]
    unknown_results: tuple[Any, ...]
    conflict_results: tuple[Any, ...]
    duplicate_identity_occurrences: tuple[Any, ...]
    admission_evidence_refs: tuple[str, ...]
    admission_boundary: str
    non_sequencing_boundary: str
    read_only: bool = True
    writes_event_ledger: bool = False
    mutates_cluster: bool = False
    admission_convention: str = ADMISSION_CONVENTION

    def to_json_dict(self) -> dict[str, Any]:
        return _jsonable(asdict(self))


def admit_shared_explanation_presentation(
    evidence_set: SharedExplanationMembershipEvidenceSet,
    requested_presentation: RequestedPresentationBoundary,
    admission_evidence: PresentationAdmissionEvidence,
) -> SharedExplanationPresentationAdmission:
    """Admit already-belonging projections to one requested presentation boundary.

    This is a read-only boundary gate. It consumes one membership evidence set,
    one explicit requested-presentation boundary, and explicit admission evidence;
    it does not reinterpret membership or construct a presentation view.
    """
    if requested_presentation.bounded_inquiry_ref != evidence_set.bounded_inquiry_ref:
        raise ValueError("presentation admission requires the evidence-set bounded inquiry")
    if requested_presentation.bounded_demand_ref != evidence_set.bounded_demand_ref:
        raise ValueError("presentation admission requires the evidence-set bounded demand")
    if admission_evidence.presentation_ref != requested_presentation.presentation_ref:
        raise ValueError("presentation admission evidence must target the requested presentation")

    admitted_refs = tuple(str(ref) for ref in admission_evidence.admitted_projection_refs if ref)
    admitted_ref_set = set(admitted_refs)
    evidence_reasons = admission_evidence.non_admission_reasons_by_projection_ref or {}

    admitted = tuple(r for r in evidence_set.belongs_results if r.candidate_projection_ref in admitted_ref_set)
    unadmitted_belongs = tuple(r for r in evidence_set.belongs_results if r.candidate_projection_ref not in admitted_ref_set)

    reasons: dict[str, tuple[str, ...]] = {}
    for result in unadmitted_belongs:
        supplied = tuple(evidence_reasons.get(result.candidate_projection_ref, ()))
        reasons[result.candidate_projection_ref] = supplied or (
            "belongs to inquiry but lacks explicit admission evidence for this requested presentation",
        )

    return SharedExplanationPresentationAdmission(
        artifact_type="SharedExplanationPresentationAdmission",
        producer="admit_shared_explanation_presentation",
        presentation_ref=requested_presentation.presentation_ref,
        bounded_inquiry_ref=evidence_set.bounded_inquiry_ref,
        bounded_demand_ref=evidence_set.bounded_demand_ref,
        supplied_result_count=evidence_set.supplied_result_count,
        admitted_to_sequencing_results=admitted,
        admitted_to_sequencing_projection_refs=tuple(r.candidate_projection_ref for r in admitted),
        belonging_but_unadmitted_results=unadmitted_belongs,
        belonging_but_unadmitted_projection_refs=tuple(r.candidate_projection_ref for r in unadmitted_belongs),
        non_admission_reasons_by_projection_ref=reasons,
        non_member_results=evidence_set.does_not_belong_results,
        unknown_results=evidence_set.unknown_results,
        conflict_results=evidence_set.conflict_results,
        duplicate_identity_occurrences=evidence_set.duplicate_identity_occurrences,
        admission_evidence_refs=tuple(admission_evidence.supporting_references),
        admission_boundary=(
            "Consumes one SharedExplanationMembershipEvidenceSet, one explicit requested-presentation "
            "boundary, and explicit presentation-local admission evidence; only already-belonging "
            "results can be admitted to later sequencing."
        ),
        non_sequencing_boundary=(
            "Admission to sequencing is not first encounter order, ranking, deduplication, view "
            "composition, membership reinterpretation, authorization, execution, event writing, or mutation."
        ),
        read_only=evidence_set.read_only,
        writes_event_ledger=False,
        mutates_cluster=False,
    )


def shared_explanation_presentation_admission_json(
    admission: SharedExplanationPresentationAdmission,
) -> dict[str, Any]:
    return admission.to_json_dict()


def format_shared_explanation_presentation_admission(
    admission: SharedExplanationPresentationAdmission,
) -> str:
    lines = [
        "Shared Explanation Presentation Admission",
        f"presentation_ref: {admission.presentation_ref}",
        f"bounded_inquiry_ref: {admission.bounded_inquiry_ref}",
        f"bounded_demand_ref: {admission.bounded_demand_ref or 'none'}",
        f"supplied_result_count: {admission.supplied_result_count}",
        f"admission_boundary: {admission.admission_boundary}",
        f"non_sequencing_boundary: {admission.non_sequencing_boundary}",
        f"read_only: {str(admission.read_only).lower()}",
        f"writes_event_ledger: {str(admission.writes_event_ledger).lower()}",
        f"mutates_cluster: {str(admission.mutates_cluster).lower()}",
        "admitted_to_sequencing_projection_refs:",
    ]
    lines += [f"- {ref}" for ref in admission.admitted_to_sequencing_projection_refs] or ["- none"]
    lines.append("belonging_but_unadmitted_projection_refs:")
    lines += [f"- {ref}" for ref in admission.belonging_but_unadmitted_projection_refs] or ["- none"]
    lines.append("non_admission_reasons_by_projection_ref:")
    for ref, reasons in admission.non_admission_reasons_by_projection_ref.items():
        lines.append(f"  {ref}:")
        lines += [f"  - {reason}" for reason in reasons]
    if not admission.non_admission_reasons_by_projection_ref:
        lines.append("  none")
    for label, results in (
        ("non_member_projection_refs", admission.non_member_results),
        ("unknown_projection_refs", admission.unknown_results),
        ("conflict_projection_refs", admission.conflict_results),
    ):
        lines.append(label + ":")
        lines += [f"- {r.candidate_projection_ref}" for r in results] or ["- none"]
    return "\n".join(lines)
