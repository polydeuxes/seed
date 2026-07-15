"""Read-only establishment of a bounded operator goal from lawful ingress evidence."""
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from typing import Iterable

from seed_runtime.closed_choice_selection_binding import ClosedChoiceSelectionBinding
from seed_runtime.operator_expression_interpretation import OperatorExpressionInterpretationProjection

CONVENTION = "bounded_operator_goal_establishment_v1"
BOUNDARY_NOTES = (
    "Bounded operator goal establishment is not constitutional meta-target establishment.",
    "Bounded operator goal establishment is not operator operating constraint enforcement.",
    "A provisional bounded goal may be enough orientation for reversible continuation without perfect goal resolution.",
    "Goal established is not inquiry opened, resources observed, constraints satisfied, work authorized, or goal satisfied.",
    "Corrections may establish a later bounded goal without rewriting the exact ingress lineage preserved here.",
)
LAWFUL_INGRESS_TYPES = ("ClosedChoiceSelectionBinding", "OperatorExpressionInterpretationProjection")


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
    outcome_resolution: str
    known_scope: tuple[str, ...]
    unresolved_scope: tuple[str, ...]
    sufficiency_conditions: tuple[str, ...]
    sufficiency_state: str
    stop_conditions: tuple[str, ...]
    operator_acceptance_provenance: tuple[str, ...]
    operator_constraints: tuple[str, ...]
    unknowns: tuple[str, ...]
    ambiguities: tuple[str, ...]
    conflicts: tuple[str, ...]
    known_loss: tuple[str, ...]
    correction_of_goal_ref: str = ""
    correction_possible_without_rewriting_ingress: bool = True
    inquiry_opened: bool = False
    resources_observed: bool = False
    constraints_enforced: bool = False
    work_authorized: bool = False
    execution_started: bool = False
    recording_started: bool = False
    satisfaction_judged: bool = False
    read_only: bool = True
    writes_event_ledger: bool = False
    mutates_cluster: bool = False
    boundary_notes: tuple[str, ...] = BOUNDARY_NOTES
    establishment_convention: str = CONVENTION

    def to_json_dict(self) -> dict[str, object]:
        data = asdict(self)
        for key, value in data.items():
            if isinstance(value, tuple):
                data[key] = list(value)
        return data


def establish_bounded_operator_goal_from_closed_choice(
    binding: ClosedChoiceSelectionBinding,
    *,
    sufficiency_conditions: tuple[str, ...] = (),
    stop_conditions: tuple[str, ...] = (),
    unresolved_scope: tuple[str, ...] = (),
    known_loss: tuple[str, ...] = (),
    correction_of_goal_ref: str = "",
) -> BoundedOperatorGoalEstablishment:
    """Establish a bounded operator goal from an exact closed-choice selection binding."""
    if binding.artifact_type != "ClosedChoiceSelectionBinding":
        raise BoundedOperatorGoalEstablishmentError("closed-choice ingress must be a ClosedChoiceSelectionBinding artifact")

    unknowns = _refs(binding.unknown_selection_evidence)
    conflicts = _refs(binding.conflicting_selection_evidence)
    unsupported = _refs(binding.unsupported_selection_evidence)
    if binding.binding_state != "bound" or not binding.bound_option_ref:
        state = "refused"
        reason = "closed_choice_selection_does_not_support_bounded_orientation"
        intended = ""
        resolution = "none"
    else:
        state = "established" if sufficiency_conditions else "provisional"
        reason = "closed_choice_selection_supplies_bounded_operator_orientation"
        intended = binding.bound_option_label or binding.bound_option_ref
        resolution = "presented closed-choice option"

    lineage = _refs((binding.binding_id, binding.choice_set_ref, binding.exact_choice_set_fingerprint, binding.token_capture_ref))
    payload = {
        "ingress": binding.binding_id,
        "state": state,
        "intended": intended,
        "known_scope": [binding.bound_option_ref] if binding.bound_option_ref else [],
        "unresolved_scope": sorted((*unresolved_scope, *unsupported)),
        "sufficiency": sorted(sufficiency_conditions),
        "stops": sorted(stop_conditions),
        "unknowns": unknowns,
        "conflicts": conflicts,
        "known_loss": sorted(known_loss),
        "correction_of": correction_of_goal_ref,
        "convention": CONVENTION,
    }
    return BoundedOperatorGoalEstablishment(
        "BoundedOperatorGoalEstablishment",
        _stable("bounded-operator-goal-establishment", payload),
        binding.artifact_type,
        binding.binding_id,
        lineage,
        state,
        reason,
        intended,
        resolution,
        (binding.bound_option_ref,) if binding.bound_option_ref else (),
        _refs((*unresolved_scope, *unsupported)),
        _refs(sufficiency_conditions),
        "provisional" if state == "provisional" else ("established" if state == "established" else "unsupported"),
        _refs(stop_conditions),
        _refs((binding.token_capture_ref,)),
        (),
        unknowns,
        (),
        conflicts,
        _refs(known_loss),
        correction_of_goal_ref,
    )


def establish_bounded_operator_goal_from_interpretation(
    interpretation: OperatorExpressionInterpretationProjection,
    *,
    sufficiency_conditions: tuple[str, ...] = (),
    stop_conditions: tuple[str, ...] = (),
    correction_of_goal_ref: str = "",
) -> BoundedOperatorGoalEstablishment:
    """Establish a bounded operator goal from interpreted operator expression evidence."""
    if interpretation.artifact_type != "OperatorExpressionInterpretationProjection":
        raise BoundedOperatorGoalEstablishmentError("expression ingress must be an OperatorExpressionInterpretationProjection artifact")

    orientation = _refs((*interpretation.relation_or_focus_expressions, *interpretation.subject_expressions, *interpretation.object_expressions, *interpretation.scope_expressions))
    unresolved = _refs((*interpretation.unresolved_references, *interpretation.unresolved_lexical_bindings, *(s.exact_text for s in interpretation.unsupported_residual_spans)))
    if interpretation.interpretation_state != "interpreted" or not orientation:
        state = "refused"
        reason = "operator_expression_interpretation_does_not_support_bounded_orientation"
        intended = ""
        resolution = "none"
    else:
        state = "established" if sufficiency_conditions and not interpretation.unknowns else "provisional"
        reason = "operator_expression_interpretation_supplies_bounded_operator_orientation"
        intended = "; ".join(orientation)
        resolution = "interpreted expression components"

    lineage = _refs((interpretation.interpretation_projection_id, interpretation.attributed_expression_ref, *interpretation.provenance))
    payload = {
        "ingress": interpretation.interpretation_projection_id,
        "state": state,
        "intended": intended,
        "known_scope": orientation,
        "unresolved_scope": unresolved,
        "sufficiency": sorted(sufficiency_conditions),
        "stops": sorted(stop_conditions),
        "constraints": sorted(interpretation.operator_stated_effect_constraints),
        "unknowns": sorted(interpretation.unknowns),
        "conflicts": sorted(interpretation.conflicts),
        "known_loss": sorted(interpretation.known_loss),
        "correction_of": correction_of_goal_ref,
        "convention": CONVENTION,
    }
    return BoundedOperatorGoalEstablishment(
        "BoundedOperatorGoalEstablishment",
        _stable("bounded-operator-goal-establishment", payload),
        interpretation.artifact_type,
        interpretation.interpretation_projection_id,
        lineage,
        state,
        reason,
        intended,
        resolution,
        orientation,
        unresolved,
        _refs(sufficiency_conditions),
        "provisional" if state == "provisional" else ("established" if state == "established" else "unsupported"),
        _refs(stop_conditions),
        _refs((interpretation.attributed_expression_ref, *interpretation.provenance)),
        _refs(interpretation.operator_stated_effect_constraints),
        _refs(interpretation.unknowns),
        _refs(a.expression_form or a.inquiry_or_request_kind for a in interpretation.alternative_interpretations),
        _refs(interpretation.conflicts),
        _refs(interpretation.known_loss),
        correction_of_goal_ref,
    )


def bounded_operator_goal_establishment_json(establishment: BoundedOperatorGoalEstablishment) -> dict[str, object]:
    return establishment.to_json_dict()
