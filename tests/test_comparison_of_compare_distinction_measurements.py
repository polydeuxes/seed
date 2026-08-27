"""Applicability requires exact Measurement Distinctions."""

from __future__ import annotations

from seed_runtime.comparison_of_compare_distinction_measurements import (
    record_applicability_act_occurrence,
    record_applicability_result,
    record_applicability_subject_to_act_binding,
    record_compare_subject_to_act_binding,
)
from seed_runtime.declared_measurements import (
    record_declared_measurements_from_current_coordinates,
)
from seed_runtime.events import EventLedger
from seed_runtime.measurement_of_compare_distinctions import (
    COMPARE_DISTINCTION_MEASUREMENT_RESULT_KIND,
)
from seed_runtime.operator_console import run_persistent_operator_console
from seed_runtime.operator_current_coordinates import (
    advance_operator_current_coordinates,
)
from tests.binary_input import binary_input


LOCALITY = "comparison-of-compare-distinction-measurements"


def _record_applicability(
    ledger: EventLedger,
    current_coordinates,
    *,
    earlier_result_occurrence_identity: str,
    later_result_occurrence_identity: str,
):
    binding = record_compare_subject_to_act_binding(
        ledger,
        earlier_result_occurrence_identity=earlier_result_occurrence_identity,
        later_result_occurrence_identity=later_result_occurrence_identity,
        current_coordinates=current_coordinates,
    )
    current_coordinates = advance_operator_current_coordinates(
        ledger,
        (binding.identity,),
        locality_identity=LOCALITY,
        prior=current_coordinates,
    )
    applicability_binding = record_applicability_subject_to_act_binding(
        ledger,
        compare_binding_event_identity=binding.identity,
        current_coordinates=current_coordinates,
    )
    current_coordinates = advance_operator_current_coordinates(
        ledger,
        (applicability_binding.identity,),
        locality_identity=LOCALITY,
        prior=current_coordinates,
    )
    applicability_act = record_applicability_act_occurrence(
        ledger,
        applicability_binding_event_identity=applicability_binding.identity,
        current_coordinates=current_coordinates,
    )
    current_coordinates = advance_operator_current_coordinates(
        ledger,
        (applicability_act.identity,),
        locality_identity=LOCALITY,
        prior=current_coordinates,
    )
    applicability_result = record_applicability_result(
        ledger,
        act_occurrence_event_identity=applicability_act.identity,
        current_coordinates=current_coordinates,
    )
    current_coordinates = advance_operator_current_coordinates(
        ledger,
        (
            applicability_result.material["yield_relation_identity"],
            applicability_result.identity,
        ),
        locality_identity=LOCALITY,
        prior=current_coordinates,
    )
    return applicability_result, current_coordinates


def test_exact_middle_measurement_establishes_applicability():
    ledger = EventLedger()
    run_persistent_operator_console(
        ledger=ledger,
        locality_identity=LOCALITY,
        input_stream=binary_input(b"ab\nac\nad\nae\n"),
    )
    recorded = record_declared_measurements_from_current_coordinates(
        ledger,
        locality_identity=LOCALITY,
    )
    measurements = tuple(
        event
        for event in ledger.list()
        if event.kind == COMPARE_DISTINCTION_MEASUREMENT_RESULT_KIND
    )
    assert len(measurements) == 3

    applicable, current_coordinates = _record_applicability(
        ledger,
        recorded.current_coordinates,
        earlier_result_occurrence_identity=measurements[0].identity,
        later_result_occurrence_identity=measurements[1].identity,
    )
    inapplicable, _current_coordinates = _record_applicability(
        ledger,
        current_coordinates,
        earlier_result_occurrence_identity=measurements[0].identity,
        later_result_occurrence_identity=measurements[2].identity,
    )

    assert applicable.material["applicability"] == "applicable"
    assert applicable.material["earlier_later_measurement_reference"] == (
        applicable.material["later_earlier_measurement_reference"]
    )
    assert inapplicable.material["applicability"] == "inapplicable"
    assert inapplicable.material["earlier_later_measurement_reference"] != (
        inapplicable.material["later_earlier_measurement_reference"]
    )
