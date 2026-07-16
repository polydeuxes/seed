"""Read-only interpretation applicability projection for one bounded downstream purpose."""
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json

from seed_runtime.contextual_interpretation_selection import ContextualInterpretationSelectionResult

CONVENTION = "interpretation_applicability_projection_v1"
APPLICABILITY_OUTCOMES = {"applicable", "inapplicable", "unknown", "conflict"}
REQUIREMENT_EVIDENCE_STATES = {"satisfied", "unsatisfied", "unknown", "conflict", "refused"}
BOUNDARY_NOTES = (
    "Selected meaning is preserved unchanged and is not determined by consumer requirements.",
    "Applicability is not downstream admission.",
    "This projection evaluates one supplied bounded consumer contract; it is not a purpose registry or universal consumer interpreter.",
    "Purpose-local requirement evidence remains consumer-owned.",
    "Known consumer examples are not a complete consumer ontology.",
    "This projection stops before goal establishment, correction application, inquiry movement, authorization, execution, presentation, recording, event-ledger writes, state mutation, or cluster mutation.",
)


class InterpretationApplicabilityProjectionError(ValueError):
    pass


def _stable(prefix: str, payload: object) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    return prefix + ":" + hashlib.sha256(encoded).hexdigest()


@dataclass(frozen=True)
class BoundedDownstreamPurpose:
    purpose_ref: str
    purpose_label: str
    consumer_ref: str
    consumer_label: str
    accepted_interpretation_shape: str
    purpose_local_requirements: tuple[str, ...]
    known_refusals: tuple[str, ...] = ()
    provenance: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.purpose_ref or not self.consumer_ref:
            raise InterpretationApplicabilityProjectionError("bounded downstream purpose requires purpose_ref and consumer_ref")
        if not self.accepted_interpretation_shape:
            raise InterpretationApplicabilityProjectionError("bounded downstream purpose requires an accepted interpretation shape")


@dataclass(frozen=True)
class PurposeLocalRequirementEvidence:
    evidence_ref: str
    purpose_ref: str
    consumer_ref: str
    requirement_ref: str
    state: str
    rationale: str = ""
    provenance: tuple[str, ...] = ()
    consumer_owned: bool = True

    def __post_init__(self) -> None:
        if not self.evidence_ref or not self.purpose_ref or not self.consumer_ref or not self.requirement_ref:
            raise InterpretationApplicabilityProjectionError(
                "requirement evidence requires evidence_ref, purpose_ref, consumer_ref, and requirement_ref"
            )
        if self.state not in REQUIREMENT_EVIDENCE_STATES:
            raise InterpretationApplicabilityProjectionError(
                f"requirement evidence state must be one of {sorted(REQUIREMENT_EVIDENCE_STATES)}"
            )


@dataclass(frozen=True)
class InterpretationApplicabilityProjection:
    artifact_type: str
    projection_id: str
    selection_result_id: str
    bounded_downstream_purpose: BoundedDownstreamPurpose
    requirement_evidence: tuple[PurposeLocalRequirementEvidence, ...]
    selected_candidate_ref: str | None
    selected_candidate: object | None
    selected_meaning_snapshot: dict[str, object] | None
    applicability: str
    applicability_reason: str
    known_refusals: tuple[str, ...]
    unknowns: tuple[str, ...]
    conflicts: tuple[str, ...]
    provenance: tuple[str, ...]
    downstream_admission: None = None
    admitted: bool = False
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


def project_interpretation_applicability(
    selection_result: ContextualInterpretationSelectionResult,
    purpose: BoundedDownstreamPurpose,
    *,
    requirement_evidence: tuple[PurposeLocalRequirementEvidence, ...] = (),
) -> InterpretationApplicabilityProjection:
    """Project applicability for one selected interpretation and one supplied consumer contract."""
    if not selection_result.interpretation_selected or selection_result.selected_candidate is None:
        raise InterpretationApplicabilityProjectionError("applicability projection requires one selected interpretation")

    foreign = tuple(
        e.evidence_ref
        for e in requirement_evidence
        if e.purpose_ref != purpose.purpose_ref or e.consumer_ref != purpose.consumer_ref
    )
    relevant = tuple(e for e in requirement_evidence if e.evidence_ref not in foreign)
    missing_requirements = tuple(req for req in purpose.purpose_local_requirements if not any(e.requirement_ref == req for e in relevant))
    refused = tuple(e for e in relevant if e.state == "refused")
    conflicts = [f"foreign requirement evidence refused: {ref}" for ref in foreign]
    conflicts.extend(f"{e.requirement_ref}:{e.rationale or e.state}" for e in relevant if e.state == "conflict")
    unknowns = [f"missing requirement evidence: {req}" for req in missing_requirements]
    unknowns.extend(f"{e.requirement_ref}:{e.rationale or e.state}" for e in relevant if e.state == "unknown")

    states_by_requirement = {req: {e.state for e in relevant if e.requirement_ref == req} for req in purpose.purpose_local_requirements}
    if conflicts or any("conflict" in states for states in states_by_requirement.values()):
        applicability, reason = "conflict", "purpose-local evidence conflicts or belongs to another bounded consumer contract"
    elif purpose.known_refusals or refused or any("refused" in states for states in states_by_requirement.values()) or any("unsatisfied" in states for states in states_by_requirement.values()):
        applicability, reason = "inapplicable", "bounded consumer contract has a known refusal or unsatisfied purpose-local requirement"
    elif unknowns or any("unknown" in states for states in states_by_requirement.values()) or missing_requirements:
        applicability, reason = "unknown", "purpose-local requirement evidence is incomplete or unknown"
    elif purpose.purpose_local_requirements and all(states == {"satisfied"} for states in states_by_requirement.values()):
        applicability, reason = "applicable", "all supplied purpose-local requirements are satisfied for this bounded consumer contract"
    else:
        applicability, reason = "unknown", "bounded consumer contract supplies no purpose-local requirements establishing applicability"

    selected_snapshot = asdict(selection_result.selected_candidate) if selection_result.selected_candidate is not None else None
    provenance = tuple(purpose.provenance) + tuple(p for e in requirement_evidence for p in ((e.evidence_ref,) + e.provenance))
    payload = {
        "selection_result_id": selection_result.selection_result_id,
        "purpose": asdict(purpose),
        "evidence": [asdict(e) for e in requirement_evidence],
        "applicability": applicability,
        "convention": CONVENTION,
    }
    return InterpretationApplicabilityProjection(
        "InterpretationApplicabilityProjection",
        _stable("interpretation-applicability-projection", payload),
        selection_result.selection_result_id,
        purpose,
        requirement_evidence,
        selection_result.selected_candidate_ref,
        selection_result.selected_candidate,
        selected_snapshot,
        applicability,
        reason,
        purpose.known_refusals + tuple(e.evidence_ref for e in refused),
        tuple(unknowns),
        tuple(conflicts),
        provenance,
    )
