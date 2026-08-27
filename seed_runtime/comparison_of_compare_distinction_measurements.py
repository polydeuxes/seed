"""Compare requires exact measured Distinction results."""

from __future__ import annotations

from copy import deepcopy
from typing import Any, NamedTuple

from seed_runtime.event import Event
from seed_runtime.events import CORRUPTED, EventLedger
from seed_runtime.measurement_of_compare_distinctions import (
    COMPARE_DISTINCTION_MEASUREMENT_RESULT_KIND,
    _producing_pair_measurement_subject,
    get_recorded_compare_distinction_measurement,
)
from seed_runtime.yield_relation import (
    RECORDED_YIELD_RELATION_EVENT,
    _record_yield_relation,
    read_requirements_of_yield_relation,
)


COMPARE_BINDING_KIND = (
    "operator.comparison_of_compare_distinction_measurements.subject_to_act_binding_recorded"
)
APPLICABILITY_BINDING_KIND = (
    "operator.comparison_of_compare_distinction_measurements.applicability_subject_to_act_binding_recorded"
)
APPLICABILITY_ACT_OCCURRENCE_KIND = (
    "operator.comparison_of_compare_distinction_measurements.applicability_act_occurrence_recorded"
)
APPLICABILITY_RESULT_KIND = (
    "operator.comparison_of_compare_distinction_measurements.applicability_recorded"
)
COMPARE_ACT_OCCURRENCE_KIND = (
    "operator.comparison_of_compare_distinction_measurements.compare_act_occurrence_recorded"
)
COMPARE_RESULT_KIND = (
    "operator.comparison_of_compare_distinction_measurements.recorded"
)

COMPARE_ACT = "Compare exact Measurement results"
APPLICABILITY_ACT = "Applicability of exact Measurement results to Compare"
APPLICABILITY_RESULT = "Applicability result of exact Measurement results"
COMPARE_RESULT = "Compare result of exact Measurement results"

EVENT_KIND_BOOK_CLAUSES = {
    COMPARE_BINDING_KIND: "04.Compare",
    APPLICABILITY_BINDING_KIND: "01.Current.E.1",
    APPLICABILITY_ACT_OCCURRENCE_KIND: "02.Acts.A",
    APPLICABILITY_RESULT_KIND: "01.Current.E.1",
}


class _Inputs(NamedTuple):
    earlier: Event
    later: Event
    earlier_reading: dict[str, Any]
    later_reading: dict[str, Any]
    earlier_producing_subject: dict[str, Any]
    later_producing_subject: dict[str, Any]


def _identity(value: Any, message: str) -> str:
    if type(value) is not str or not value:
        raise ValueError(message)
    return value


def _measurement_reference(event: Event) -> dict[str, Any]:
    return {
        "recorded_occurrence_identity": event.identity,
        "result_identity": event.material["result_identity"],
        "act_occurrence_identity": event.material["act_occurrence_identity"],
        "act_occurrence_event_identity": event.material[
            "act_occurrence_event_identity"
        ],
        "yield_relation_identity": event.material["yield_relation_identity"],
    }


def _binding_reference(binding: Event) -> dict[str, Any]:
    return {
        "recorded_occurrence_identity": binding.identity,
        "book_clause_identity": binding.material["book_clause_identity"],
        "exact_act_identity": binding.material["exact_act_identity"],
        "subject_reference": deepcopy(binding.material["subject_reference"]),
        "result_boundary_identity": binding.material["result_boundary_identity"],
    }


def _inputs(
    ledger: EventLedger,
    *,
    earlier_result_occurrence_identity: str,
    later_result_occurrence_identity: str,
    current_coordinates: dict[str, Any],
) -> _Inputs:
    measurements = current_coordinates.get("measurement_occurrences")
    earlier = ledger.get(earlier_result_occurrence_identity)
    later = ledger.get(later_result_occurrence_identity)
    if (
        type(measurements) is not dict
        or earlier is None
        or later is None
        or earlier.identity == later.identity
        or earlier.kind != COMPARE_DISTINCTION_MEASUREMENT_RESULT_KIND
        or later.kind != COMPARE_DISTINCTION_MEASUREMENT_RESULT_KIND
        or earlier.locality_identity != later.locality_identity
        or earlier.locality_identity != current_coordinates.get("locality_identity")
        or earlier.identity not in measurements
        or later.identity not in measurements
        or ledger.integrity_of(earlier.identity) == CORRUPTED
        or ledger.integrity_of(later.identity) == CORRUPTED
    ):
        raise ValueError("Compare requires exact current Measurement results")
    ledger.occurrences_in_append_order(
        (earlier.identity, later.identity),
        locality_identity=earlier.locality_identity,
    )
    return _Inputs(
        earlier,
        later,
        get_recorded_compare_distinction_measurement(
            ledger,
            earlier.identity,
            prior_coordinates=current_coordinates,
        ),
        get_recorded_compare_distinction_measurement(
            ledger,
            later.identity,
            prior_coordinates=current_coordinates,
        ),
        _producing_pair_measurement_subject(
            ledger,
            measurement_result_occurrence_identity=earlier.identity,
            current_coordinates=current_coordinates,
        ),
        _producing_pair_measurement_subject(
            ledger,
            measurement_result_occurrence_identity=later.identity,
            current_coordinates=current_coordinates,
        ),
    )


def _compare_binding_material(
    inputs: _Inputs,
    *,
    through_event_occurrence_identity: str,
    exact_act_identity: str,
    compare_act_occurrence_identity: str,
    compare_result_identity: str,
) -> dict[str, Any]:
    earlier_reference = _measurement_reference(inputs.earlier)
    later_reference = _measurement_reference(inputs.later)
    return {
        "subject_reference": {
            "earlier_measurement_result_reference": deepcopy(earlier_reference),
            "later_measurement_result_reference": deepcopy(later_reference),
        },
        "exact_act_identity": exact_act_identity,
        "compare_act_occurrence_identity": compare_act_occurrence_identity,
        "compare_result_identity": compare_result_identity,
        "result_boundary_identity": compare_result_identity,
        "book_clause_identity": "04.Compare",
        "earlier_measurement_result_reference": earlier_reference,
        "later_measurement_result_reference": later_reference,
        "earlier_later_measurement_reference": deepcopy(
            inputs.earlier_producing_subject["later_measurement_reference"]
        ),
        "later_earlier_measurement_reference": deepcopy(
            inputs.later_producing_subject["earlier_measurement_reference"]
        ),
        "through_event_occurrence_identity": through_event_occurrence_identity,
    }


def record_compare_subject_to_act_binding(
    ledger: EventLedger,
    *,
    earlier_result_occurrence_identity: str,
    later_result_occurrence_identity: str,
    current_coordinates: dict[str, Any],
) -> Event:
    """Record two complete measured results before Compare."""

    inputs = _inputs(
        ledger,
        earlier_result_occurrence_identity=earlier_result_occurrence_identity,
        later_result_occurrence_identity=later_result_occurrence_identity,
        current_coordinates=current_coordinates,
    )
    boundary = _identity(
        current_coordinates.get("through_event_occurrence_identity"),
        "Compare binding requires one exact through-occurrence boundary",
    )
    boundary_event = ledger.get(boundary)
    if (
        boundary_event is None
        or boundary_event.locality_identity != inputs.earlier.locality_identity
        or ledger.integrity_of(boundary_event.identity) == CORRUPTED
        or ledger.append_boundary_through_occurrence(boundary_event.identity)
        != ledger.append_boundary()
    ):
        raise ValueError("Compare binding requires exact current coordinates")
    identities = {
        "exact_act_identity": ledger.mint_identity(
            "compare_distinction_results_act"
        ),
        "compare_act_occurrence_identity": ledger.mint_identity(
            "compare_distinction_results_occurrence"
        ),
        "compare_result_identity": ledger.mint_identity(
            "compare_distinction_results_result"
        ),
    }
    return ledger.append(
        COMPARE_BINDING_KIND,
        _compare_binding_material(
            inputs,
            through_event_occurrence_identity=boundary,
            **identities,
        ),
        locality_identity=inputs.earlier.locality_identity,
    )


def _read_compare_binding(
    ledger: EventLedger,
    event_identity: str,
    *,
    prior_coordinates: dict[str, Any] | None = None,
) -> tuple[Event, _Inputs]:
    binding = ledger.get(event_identity)
    if (
        binding is None
        or binding.kind != COMPARE_BINDING_KIND
        or ledger.integrity_of(binding.identity) == CORRUPTED
    ):
        raise ValueError("measured Distinction Compare binding is not exact")
    material = binding.material
    earlier_reference = material.get("earlier_measurement_result_reference")
    later_reference = material.get("later_measurement_result_reference")
    boundary = material.get("through_event_occurrence_identity")
    if prior_coordinates is None:
        from seed_runtime.operator_current_coordinates import (
            read_operator_current_coordinates_through,
        )

        prior_coordinates = read_operator_current_coordinates_through(
            ledger,
            locality_identity=binding.locality_identity,
            through_event_occurrence_identity=boundary,
        )
    inputs = _inputs(
        ledger,
        earlier_result_occurrence_identity=(
            earlier_reference.get("recorded_occurrence_identity")
            if type(earlier_reference) is dict
            else None
        ),
        later_result_occurrence_identity=(
            later_reference.get("recorded_occurrence_identity")
            if type(later_reference) is dict
            else None
        ),
        current_coordinates=prior_coordinates,
    )
    identities = {
        coordinate: _identity(
            material.get(coordinate),
            "measured Distinction Compare binding is not exact",
        )
        for coordinate in (
            "exact_act_identity",
            "compare_act_occurrence_identity",
            "compare_result_identity",
        )
    }
    carried = prior_coordinates.get("subject_to_act_binding_occurrences")
    if (
        len(set(identities.values())) != 3
        or (
            prior_coordinates.get("through_event_occurrence_identity") != boundary
            and not (
                type(carried) is dict
                and carried.get(binding.identity, object()) is None
            )
        )
        or material
        != _compare_binding_material(
            inputs,
            through_event_occurrence_identity=boundary,
            **identities,
        )
    ):
        raise ValueError("measured Distinction Compare binding is not exact")
    return binding, inputs


def _applicability_binding_material(
    comparison_binding: Event,
    *,
    through_event_occurrence_identity: str,
    exact_act_identity: str,
    applicability_act_occurrence_identity: str,
    applicability_result_identity: str,
) -> dict[str, Any]:
    return {
        "subject_reference": deepcopy(comparison_binding.material["subject_reference"]),
        "exact_act_identity": exact_act_identity,
        "applicability_act_occurrence_identity": (
            applicability_act_occurrence_identity
        ),
        "applicability_result_identity": applicability_result_identity,
        "addressed_act_identity": comparison_binding.material["exact_act_identity"],
        "result_boundary_identity": applicability_result_identity,
        "book_clause_identity": "01.Current.E.1",
        "compare_subject_to_act_binding_reference": _binding_reference(
            comparison_binding
        ),
        "earlier_later_measurement_reference": deepcopy(
            comparison_binding.material["earlier_later_measurement_reference"]
        ),
        "later_earlier_measurement_reference": deepcopy(
            comparison_binding.material["later_earlier_measurement_reference"]
        ),
        "through_event_occurrence_identity": through_event_occurrence_identity,
    }


def record_applicability_subject_to_act_binding(
    ledger: EventLedger,
    *,
    compare_binding_event_identity: str,
    current_coordinates: dict[str, Any],
) -> Event:
    """Record Applicability to the exact addressed Compare binding."""

    comparison_binding, _inputs_reading = _read_compare_binding(
        ledger,
        compare_binding_event_identity,
        prior_coordinates=current_coordinates,
    )
    carried = current_coordinates.get("subject_to_act_binding_occurrences")
    boundary = _identity(
        current_coordinates.get("through_event_occurrence_identity"),
        "Applicability binding requires one through-occurrence boundary",
    )
    if (
        type(carried) is not dict
        or carried.get(comparison_binding.identity, object()) is not None
    ):
        raise ValueError("Applicability requires its current Compare binding")
    identities = {
        "exact_act_identity": ledger.mint_identity(
            "compare_distinction_results_applicability_act"
        ),
        "applicability_act_occurrence_identity": ledger.mint_identity(
            "compare_distinction_results_applicability_occurrence"
        ),
        "applicability_result_identity": ledger.mint_identity(
            "compare_distinction_results_applicability_result"
        ),
    }
    return ledger.append(
        APPLICABILITY_BINDING_KIND,
        _applicability_binding_material(
            comparison_binding,
            through_event_occurrence_identity=boundary,
            **identities,
        ),
        locality_identity=comparison_binding.locality_identity,
    )


def _read_applicability_binding(
    ledger: EventLedger,
    event_identity: str,
    *,
    prior_coordinates: dict[str, Any] | None = None,
) -> tuple[Event, Event, _Inputs]:
    binding = ledger.get(event_identity)
    reference = (
        binding.material.get("compare_subject_to_act_binding_reference")
        if binding is not None
        else None
    )
    if (
        binding is None
        or binding.kind != APPLICABILITY_BINDING_KIND
        or type(reference) is not dict
        or ledger.integrity_of(binding.identity) == CORRUPTED
    ):
        raise ValueError("measured Distinction Applicability binding is not exact")
    comparison_binding, inputs = _read_compare_binding(
        ledger,
        reference.get("recorded_occurrence_identity"),
        prior_coordinates=prior_coordinates,
    )
    material = binding.material
    identities = {
        coordinate: _identity(
            material.get(coordinate),
            "measured Distinction Applicability binding is not exact",
        )
        for coordinate in (
            "exact_act_identity",
            "applicability_act_occurrence_identity",
            "applicability_result_identity",
        )
    }
    boundary = material.get("through_event_occurrence_identity")
    if (
        len(set(identities.values())) != 3
        or reference != _binding_reference(comparison_binding)
        or material
        != _applicability_binding_material(
            comparison_binding,
            through_event_occurrence_identity=boundary,
            **identities,
        )
    ):
        raise ValueError("measured Distinction Applicability binding is not exact")
    ledger.occurrences_in_append_order(
        (comparison_binding.identity, binding.identity),
        locality_identity=binding.locality_identity,
    )
    return binding, comparison_binding, inputs


def _applicability_act_material(binding: Event) -> dict[str, Any]:
    return {
        "applicability_act_identity": binding.material["exact_act_identity"],
        "act_occurrence_identity": binding.material[
            "applicability_act_occurrence_identity"
        ],
        "result_identity": binding.material["applicability_result_identity"],
        "act": APPLICABILITY_ACT,
        "subject_to_act_binding_reference": _binding_reference(binding),
        "addressed_act_identity": binding.material["addressed_act_identity"],
        "compare_subject_to_act_binding_reference": deepcopy(
            binding.material["compare_subject_to_act_binding_reference"]
        ),
        "earlier_later_measurement_reference": deepcopy(
            binding.material["earlier_later_measurement_reference"]
        ),
        "later_earlier_measurement_reference": deepcopy(
            binding.material["later_earlier_measurement_reference"]
        ),
    }


def record_applicability_act_occurrence(
    ledger: EventLedger,
    *,
    applicability_binding_event_identity: str,
    current_coordinates: dict[str, Any],
) -> Event:
    binding, _comparison_binding, _inputs_reading = _read_applicability_binding(
        ledger,
        applicability_binding_event_identity,
        prior_coordinates=current_coordinates,
    )
    carried = current_coordinates.get("subject_to_act_binding_occurrences")
    if (
        type(carried) is not dict
        or carried.get(binding.identity, object()) is not None
    ):
        raise ValueError("Applicability Act requires its current binding")
    return ledger.append(
        APPLICABILITY_ACT_OCCURRENCE_KIND,
        _applicability_act_material(binding),
        locality_identity=binding.locality_identity,
    )


def _read_applicability_act(
    ledger: EventLedger,
    event_identity: str,
    *,
    prior_coordinates: dict[str, Any] | None = None,
) -> tuple[Event, Event, Event, _Inputs]:
    act = ledger.get(event_identity)
    reference = (
        act.material.get("subject_to_act_binding_reference")
        if act is not None
        else None
    )
    if (
        act is None
        or act.kind != APPLICABILITY_ACT_OCCURRENCE_KIND
        or type(reference) is not dict
        or ledger.integrity_of(act.identity) == CORRUPTED
    ):
        raise ValueError("measured Distinction Applicability Act is not exact")
    binding, comparison_binding, inputs = _read_applicability_binding(
        ledger,
        reference.get("recorded_occurrence_identity"),
        prior_coordinates=prior_coordinates,
    )
    if (
        act.locality_identity != binding.locality_identity
        or reference != _binding_reference(binding)
        or act.material != _applicability_act_material(binding)
    ):
        raise ValueError("measured Distinction Applicability Act is not exact")
    return act, binding, comparison_binding, inputs


def _applicability_result_material(act: Event) -> dict[str, Any]:
    earlier_middle = act.material["earlier_later_measurement_reference"]
    later_middle = act.material["later_earlier_measurement_reference"]
    return {
        "result_identity": act.material["result_identity"],
        "applicability_act_identity": act.material["applicability_act_identity"],
        "act_occurrence_identity": act.material["act_occurrence_identity"],
        "exact_act": APPLICABILITY_ACT,
        "subject_to_act_binding_reference": deepcopy(
            act.material["subject_to_act_binding_reference"]
        ),
        "addressed_act_identity": act.material["addressed_act_identity"],
        "compare_subject_to_act_binding_reference": deepcopy(
            act.material["compare_subject_to_act_binding_reference"]
        ),
        "earlier_later_measurement_reference": deepcopy(earlier_middle),
        "later_earlier_measurement_reference": deepcopy(later_middle),
        "applicability": (
            "applicable" if earlier_middle == later_middle else "inapplicable"
        ),
    }


def _recorded_applicability_result_material(
    act: Event,
    *,
    yield_relation_identity: str,
) -> dict[str, Any]:
    result = _applicability_result_material(act)
    return {
        "result_identity": result["result_identity"],
        "applicability_act_identity": result["applicability_act_identity"],
        "act_occurrence_identity": result["act_occurrence_identity"],
        "exact_act": result["exact_act"],
        "subject_to_act_binding_reference": deepcopy(
            result["subject_to_act_binding_reference"]
        ),
        "addressed_act_identity": result["addressed_act_identity"],
        "compare_subject_to_act_binding_reference": deepcopy(
            result["compare_subject_to_act_binding_reference"]
        ),
        "earlier_later_measurement_reference": deepcopy(
            result["earlier_later_measurement_reference"]
        ),
        "later_earlier_measurement_reference": deepcopy(
            result["later_earlier_measurement_reference"]
        ),
        "applicability": result["applicability"],
        "act_occurrence_event_identity": act.identity,
        "yield_relation_identity": yield_relation_identity,
    }


def record_applicability_result(
    ledger: EventLedger,
    *,
    act_occurrence_event_identity: str,
    current_coordinates: dict[str, Any] | None = None,
) -> Event:
    act, _binding, _comparison_binding, _inputs_reading = _read_applicability_act(
        ledger,
        act_occurrence_event_identity,
        prior_coordinates=current_coordinates,
    )
    result = _applicability_result_material(act)
    yield_relation = _record_yield_relation(
        ledger,
        locality_identity=act.locality_identity,
        exact_act=APPLICABILITY_ACT,
        act_occurrence_identity=act.material["act_occurrence_identity"],
        act_occurrence_event_identity=act.identity,
        result_kind=APPLICABILITY_RESULT,
        result_identity=result["result_identity"],
        result_content=result,
        occurrence_boundary="compare_distinction_results_applicability",
    )
    return ledger.append(
        APPLICABILITY_RESULT_KIND,
        _recorded_applicability_result_material(
            act,
            yield_relation_identity=yield_relation.identity,
        ),
        locality_identity=act.locality_identity,
    )


def _read_applicability_result(
    ledger: EventLedger,
    event_identity: str,
    *,
    prior_coordinates: dict[str, Any] | None = None,
) -> tuple[dict[str, Any], Event, Event, Event, _Inputs]:
    result = ledger.get(event_identity)
    act_identity = (
        result.material.get("act_occurrence_event_identity")
        if result is not None
        else None
    )
    if (
        result is None
        or result.kind != APPLICABILITY_RESULT_KIND
        or ledger.integrity_of(result.identity) == CORRUPTED
    ):
        raise ValueError("measured Distinction Applicability result is not exact")
    act, binding, comparison_binding, inputs = _read_applicability_act(
        ledger,
        act_identity,
        prior_coordinates=prior_coordinates,
    )
    expected = _recorded_applicability_result_material(
        act,
        yield_relation_identity=result.material.get("yield_relation_identity"),
    )
    yield_identity = result.material.get("yield_relation_identity")
    yield_event = ledger.get(yield_identity) if type(yield_identity) is str else None
    requirements = read_requirements_of_yield_relation(
        ledger,
        recorded_result_event_identity=result.identity,
        yield_relation_event_identity=yield_identity,
        act_occurrence_event_identity=act.identity,
    )
    if (
        result.material != expected
        or result.locality_identity != act.locality_identity
        or yield_event is None
        or yield_event.kind != RECORDED_YIELD_RELATION_EVENT
        or yield_event.material.get("occurrence_boundary")
        != "compare_distinction_results_applicability"
        or not all(requirements.values())
    ):
        raise ValueError("measured Distinction Applicability result is not exact")
    return deepcopy(result.material), result, binding, comparison_binding, inputs
