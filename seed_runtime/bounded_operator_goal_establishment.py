"""Read-only establishment of a bounded operator goal from lawful ingress evidence."""
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from typing import Iterable

from seed_runtime.downstream_interpretation_admission import DownstreamInterpretationAdmission

CONVENTION = "bounded_operator_goal_establishment_v1"
BOUNDED_GOAL_ESTABLISHMENT_CONSUMER_REF = "consumer:bounded-operator-goal-establishment"
BOUNDED_GOAL_ESTABLISHMENT_PURPOSE_REF = "purpose:bounded-operator-goal-establishment"


@dataclass(frozen=True)
class MeaningRelationApplicabilityExamination:
    """Consumer-owned standing for one exact warranted meaning relation."""

    consumer_ref: str
    purpose_ref: str
    condition_examined: str
    applicability: str
    reason: str
    evidence: dict[str, object]
    conflicts: tuple[str, ...] = ()
    unknowns: tuple[str, ...] = ()


def examine_meaning_relation_applicability(
    meaning_relation_occurrence: dict[str, object],
) -> MeaningRelationApplicabilityExamination:
    """Examine the current consumer boundary without inventing an admission.

    This consumer currently establishes a goal only from an exact admitted
    interpretation.  A warranted meaning relation is therefore relevant input,
    but is not itself positive evidence of applicability to this consumer.
    """
    payload = meaning_relation_occurrence.get("payload", {})
    conflicts = _refs(payload.get("conflicts", ())) if isinstance(payload, dict) else ()
    condition = (
        "an exact DownstreamInterpretationAdmission admitted for the bounded "
        "operator goal establishment consumer and purpose"
    )
    evidence = {
        "meaning_relation_warrant_occurrence": meaning_relation_occurrence,
        "consumer_ref": BOUNDED_GOAL_ESTABLISHMENT_CONSUMER_REF,
        "purpose_ref": BOUNDED_GOAL_ESTABLISHMENT_PURPOSE_REF,
        "condition_examined": condition,
        "condition_evidence": [],
    }
    if conflicts:
        return MeaningRelationApplicabilityExamination(
            BOUNDED_GOAL_ESTABLISHMENT_CONSUMER_REF,
            BOUNDED_GOAL_ESTABLISHMENT_PURPOSE_REF,
            condition,
            "conflict",
            "the warranted relation carries unresolved conflict",
            evidence,
            conflicts,
        )
    return MeaningRelationApplicabilityExamination(
        BOUNDED_GOAL_ESTABLISHMENT_CONSUMER_REF,
        BOUNDED_GOAL_ESTABLISHMENT_PURPOSE_REF,
        condition,
        "unknown",
        "no consumer-local admitted interpretation evidence was supplied",
        evidence,
        unknowns=("consumer-local admission evidence is absent",),
    )


class BoundedOperatorGoalEstablishmentError(ValueError):
    pass


def _refs(values: Iterable[str] = ()) -> tuple[str, ...]:
    return tuple(sorted({str(value) for value in values if value}))


def _stable(prefix: str, payload: object) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    return prefix + ":" + hashlib.sha256(encoded).hexdigest()


@dataclass(frozen=True)
class BoundedOperatorGoalEstablishment:
    artifact_type: str
    goal_establishment_id: str
    ingress_artifact_type: str
    ingress_artifact_ref: str
    ingress_lineage: tuple[str, ...]
    establishment_state: str
    establishment_reason: str
    intended_outcome: str
    known_scope: tuple[str, ...]
    unresolved_scope: tuple[str, ...]
    unknowns: tuple[str, ...]
    conflicts: tuple[str, ...]
    known_loss: tuple[str, ...]
    upstream_source_material_refs: tuple[str, ...] = ()
    upstream_selection_refs: tuple[str, ...] = ()
    upstream_applicability_refs: tuple[str, ...] = ()
    upstream_admission_refs: tuple[str, ...] = ()
    consumed_admitted_meaning_snapshot: dict[str, object] | None = None

    def to_json_dict(self) -> dict[str, object]:
        data = asdict(self)
        for key, value in data.items():
            if isinstance(value, tuple):
                data[key] = list(value)
        return data


def establish_bounded_operator_goal_from_admitted_interpretation(
    admission: DownstreamInterpretationAdmission,
) -> BoundedOperatorGoalEstablishment:
    """Establish one bounded operator goal by consuming an exact consumer-local admission.

    This handoff consumes the admitted selected meaning snapshot and preserved upstream
    artifacts. It does not reinterpret source material, regenerate warrants, reselect a
    candidate, recompute applicability, or recompute admission.
    """
    if admission.artifact_type != "DownstreamInterpretationAdmission":
        raise BoundedOperatorGoalEstablishmentError("admitted-interpretation ingress must be a DownstreamInterpretationAdmission artifact")

    projection = admission.applicability_projection
    selection = projection.selected_candidate
    selected_ref = admission.selected_candidate_ref or ""
    residual_refs: tuple[str, ...] = ()
    candidate_unknowns: tuple[str, ...] = ()
    candidate_conflicts: tuple[str, ...] = ()
    candidate_known_loss: tuple[str, ...] = ()
    proposed_meaning = ""

    # The admission carries the selected candidate and a snapshot produced upstream.
    # Use those values only; do not call warrant, selection, applicability, or
    # admission producers from this goal-establishment owner.
    if selection is not None:
        proposed_meaning = getattr(selection, "proposed_meaning", "")
        candidate_unknowns = _refs(getattr(selection, "unknowns", ()))
        candidate_conflicts = _refs(getattr(selection, "conflicts", ()))
        candidate_known_loss = _refs(getattr(selection, "known_loss", ()))
        residual_refs = _refs(getattr(s, "span_ref", str(s)) for s in getattr(selection, "residual_source_material", ()))

    # Selective introspection of carried upstream objects is lineage preservation,
    # not recomputation.
    app_unknowns = _refs(projection.unknowns)
    app_conflicts = _refs(projection.conflicts)
    admission_unknowns = _refs(admission.unknowns)
    admission_conflicts = _refs(admission.conflicts)
    known_refusals = _refs((*projection.known_refusals, *admission.known_refusals))
    mismatch_reasons: list[str] = []
    if admission.consumer_ref != BOUNDED_GOAL_ESTABLISHMENT_CONSUMER_REF:
        mismatch_reasons.append("admission consumer is not bounded operator goal establishment")
    if admission.purpose_ref != BOUNDED_GOAL_ESTABLISHMENT_PURPOSE_REF:
        mismatch_reasons.append("admission purpose is not bounded operator goal establishment")
    if admission.selection_result_id != projection.selection_result_id:
        mismatch_reasons.append("admission selection identity does not match applicability projection")
    if admission.projection_id != projection.projection_id:
        mismatch_reasons.append("admission projection identity does not match carried applicability projection")
    if admission.selected_candidate_ref != projection.selected_candidate_ref:
        mismatch_reasons.append("admission selected candidate identity does not match applicability projection")

    unknowns = _refs((*candidate_unknowns, *app_unknowns, *admission_unknowns))
    conflicts = _refs((*candidate_conflicts, *app_conflicts, *admission_conflicts, *mismatch_reasons))
    unresolved = _refs((*known_refusals, *admission.applicable_but_unadmitted_reasons, *residual_refs))

    if mismatch_reasons:
        state, reason = "refused", "admission_identity_or_consumer_mismatch"
    elif not admission.admitted or admission.outcome != "admitted":
        state, reason = "refused", "interpretation_not_admitted_to_bounded_goal_establishment"
    elif projection.applicability != "applicable":
        state, reason = "refused", "admitted_interpretation_is_not_applicable"
    elif unknowns:
        state, reason = "refused", "admitted_interpretation_has_unknown_upstream_lineage"
    elif conflicts:
        state, reason = "refused", "admitted_interpretation_has_conflicting_upstream_lineage"
    elif not selected_ref or selection is None:
        state, reason = "refused", "admitted_interpretation_lacks_selected_meaning_identity"
    elif not isinstance(proposed_meaning, str) or not proposed_meaning.strip():
        state, reason = "refused", "admitted_interpretation_lacks_exact_candidate_proposition"
    else:
        state = "established"
        reason = "consumer_local_admitted_interpretation_supplies_bounded_operator_goal_standing"

    intended = "" if state == "refused" else proposed_meaning
    scope = () if state == "refused" else _refs((selected_ref, getattr(selection, "label", "")))
    snapshot = admission.applicability_projection.selected_meaning_snapshot or {}
    snapshot_source_refs = tuple(
        span.get("span_ref", "")
        for span in snapshot.get("source_spans", ())
        if isinstance(span, dict)
    )
    residual_source_refs = tuple(
        span.get("span_ref", "")
        for span in snapshot.get("residual_source_material", ())
        if isinstance(span, dict)
    )
    upstream_source_refs = _refs((admission.selection_result_id, projection.selection_result_id, *snapshot_source_refs, *residual_source_refs, *projection.provenance))
    upstream_selection_refs = _refs((admission.selection_result_id, selected_ref))
    upstream_applicability_refs = _refs((projection.projection_id, *projection.provenance))
    upstream_admission_refs = _refs((admission.admission_id, *(e.evidence_ref for e in admission.admission_evidence), *admission.provenance))
    lineage = _refs((*upstream_source_refs, *upstream_selection_refs, *upstream_applicability_refs, *upstream_admission_refs))

    payload = {
        "ingress": admission.admission_id, "state": state, "selected": selected_ref,
        "unknowns": unknowns, "conflicts": conflicts, "unresolved": unresolved,
        "convention": CONVENTION,
    }
    return BoundedOperatorGoalEstablishment(
        "BoundedOperatorGoalEstablishment", _stable("bounded-operator-goal-establishment", payload),
        admission.artifact_type, admission.admission_id, lineage, state, reason, intended,
        scope, unresolved, unknowns, conflicts,
        _refs(candidate_known_loss), upstream_source_refs,
        upstream_selection_refs, upstream_applicability_refs, upstream_admission_refs, admission.applicability_projection.selected_meaning_snapshot,
    )


def bounded_operator_goal_establishment_json(establishment: BoundedOperatorGoalEstablishment) -> dict[str, object]:
    return establishment.to_json_dict()
