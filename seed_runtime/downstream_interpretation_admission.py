"""Read-only consumer-local admission for an applicable interpretation projection."""
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json

from seed_runtime.contextual_interpretation_selection import ContextualInterpretationSelectionResult
from seed_runtime.interpretation_applicability_projection import InterpretationApplicabilityProjection

CONVENTION = "downstream_interpretation_admission_v1"
ADMISSION_EVIDENCE_STATES = {"admit", "do_not_admit", "unknown", "conflict", "refused"}
BOUNDARY_NOTES = (
    "Applicable is not admitted.",
    "Admission is local to exactly one consumer and purpose and is not transferable authority for another consumer.",
    "Admitted to a consumer is not consumed by that consumer.",
    "Admission stops before goal establishment, correction application, inquiry movement, authorization, execution, presentation, recording, event-ledger writes, state mutation, or cluster mutation.",
)


class DownstreamInterpretationAdmissionError(ValueError):
    pass


def _stable(prefix: str, payload: object) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    return prefix + ":" + hashlib.sha256(encoded).hexdigest()


@dataclass(frozen=True)
class ConsumerLocalAdmissionEvidence:
    evidence_ref: str
    selection_result_id: str
    projection_id: str
    selected_candidate_ref: str
    purpose_ref: str
    consumer_ref: str
    state: str
    rationale: str = ""
    provenance: tuple[str, ...] = ()
    consumer_local: bool = True

    def __post_init__(self) -> None:
        if not all((self.evidence_ref, self.selection_result_id, self.projection_id, self.selected_candidate_ref, self.purpose_ref, self.consumer_ref)):
            raise DownstreamInterpretationAdmissionError("admission evidence requires refs for evidence, selection, projection, candidate, purpose, and consumer")
        if self.state not in ADMISSION_EVIDENCE_STATES:
            raise DownstreamInterpretationAdmissionError(f"admission evidence state must be one of {sorted(ADMISSION_EVIDENCE_STATES)}")


@dataclass(frozen=True)
class DownstreamInterpretationAdmission:
    artifact_type: str
    admission_id: str
    selection_result_id: str
    projection_id: str
    selected_candidate_ref: str | None
    selected_candidate: object | None
    consumer_ref: str
    consumer_label: str
    purpose_ref: str
    purpose_label: str
    applicability_projection: InterpretationApplicabilityProjection
    admission_evidence: tuple[ConsumerLocalAdmissionEvidence, ...]
    outcome: str
    admitted: bool
    unadmitted: bool
    applicable_but_unadmitted: bool
    applicable_but_unadmitted_reasons: tuple[str, ...]
    known_refusals: tuple[str, ...]
    unknowns: tuple[str, ...]
    conflicts: tuple[str, ...]
    provenance: tuple[str, ...]
    consumed_by_consumer: bool = False
    goal_established: bool = False
    correction_applied: bool = False
    inquiry_moved: bool = False
    authorized: bool = False
    executed: bool = False
    presented: bool = False
    recorded: bool = False
    read_only: bool = True
    writes_event_ledger: bool = False
    mutates_state: bool = False
    mutates_cluster: bool = False
    boundary_notes: tuple[str, ...] = BOUNDARY_NOTES
    convention: str = CONVENTION

    def to_json_dict(self) -> dict[str, object]:
        return asdict(self)


def admit_downstream_interpretation(
    selection_result: ContextualInterpretationSelectionResult,
    applicability_projection: InterpretationApplicabilityProjection,
    *,
    admission_evidence: tuple[ConsumerLocalAdmissionEvidence, ...] = (),
) -> DownstreamInterpretationAdmission:
    """Admit one applicable projected interpretation to one exact consumer-local intake boundary."""
    if applicability_projection.selection_result_id != selection_result.selection_result_id:
        raise DownstreamInterpretationAdmissionError("admission requires the projection for the supplied selection result")

    purpose = applicability_projection.bounded_downstream_purpose
    expected = (selection_result.selection_result_id, applicability_projection.projection_id, selection_result.selected_candidate_ref, purpose.purpose_ref, purpose.consumer_ref)
    local = tuple(
        e for e in admission_evidence
        if (e.selection_result_id, e.projection_id, e.selected_candidate_ref, e.purpose_ref, e.consumer_ref) == expected
    )
    foreign = tuple(e.evidence_ref for e in admission_evidence if e not in local)

    known_refusals = tuple(applicability_projection.known_refusals) + tuple(e.evidence_ref for e in local if e.state == "refused")
    unknowns = list(applicability_projection.unknowns)
    conflicts = list(applicability_projection.conflicts)
    conflicts.extend(f"foreign admission evidence refused for this consumer-local boundary: {ref}" for ref in foreign)
    unknowns.extend(f"{e.evidence_ref}:{e.rationale or e.state}" for e in local if e.state == "unknown")
    conflicts.extend(f"{e.evidence_ref}:{e.rationale or e.state}" for e in local if e.state == "conflict")

    states = {e.state for e in local}
    if applicability_projection.applicability != "applicable":
        outcome, admitted = "unadmitted", False
        reasons = (f"applicability is {applicability_projection.applicability}, not applicable",)
    elif conflicts or "conflict" in states:
        outcome, admitted = "conflict", False
        reasons = ("consumer-local admission evidence is conflicting",)
    elif unknowns or "unknown" in states:
        outcome, admitted = "unknown", False
        reasons = ("consumer-local admission evidence is unknown or incomplete",)
    elif known_refusals or "refused" in states or "do_not_admit" in states:
        outcome, admitted = "unadmitted", False
        reasons = tuple(e.rationale or e.evidence_ref for e in local if e.state in {"refused", "do_not_admit"}) or ("consumer-local admission evidence refuses admission",)
    elif "admit" in states:
        outcome, admitted = "admitted", True
        reasons = ()
    else:
        outcome, admitted = "unadmitted", False
        reasons = ("applicable interpretation lacks explicit admission evidence for this exact consumer and purpose",)

    payload = {"selection_result_id": selection_result.selection_result_id, "projection_id": applicability_projection.projection_id, "evidence": [asdict(e) for e in admission_evidence], "outcome": outcome, "convention": CONVENTION}
    return DownstreamInterpretationAdmission(
        "DownstreamInterpretationAdmission",
        _stable("downstream-interpretation-admission", payload),
        selection_result.selection_result_id,
        applicability_projection.projection_id,
        selection_result.selected_candidate_ref,
        selection_result.selected_candidate,
        purpose.consumer_ref,
        purpose.consumer_label,
        purpose.purpose_ref,
        purpose.purpose_label,
        applicability_projection,
        admission_evidence,
        outcome,
        admitted,
        not admitted,
        applicability_projection.applicability == "applicable" and not admitted,
        reasons,
        known_refusals,
        tuple(unknowns),
        tuple(conflicts),
        tuple(applicability_projection.provenance) + tuple(p for e in admission_evidence for p in ((e.evidence_ref,) + e.provenance)),
    )
