"""Carry one calculator result beside one exact path through distinctions.

The path around byte ``0x3d`` meets exact findings from an earlier-to-claim
pair comparison while carrying Unknown for its represented relation.  The external
result enters through its own invocation lifecycle; no current Responsibility
compares it with the path finding or establishes arithmetic meaning.
"""

from __future__ import annotations

import json
from copy import deepcopy
from io import BytesIO
from pathlib import Path

import pytest

from scripts.operator_host_provider import invoke_operator_host
from seed_runtime.addressed_byte_occurrence_reference_determination import (
    _record_addressed_byte_occurrence_reference_determination_lifecycle_from_carried_standing,
)
from seed_runtime.comparison_of_ordered_relation_path_with_recorded_pair_findings import (
    COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_RESULT_KIND,
    get_recorded_comparison_of_ordered_relation_path_with_recorded_pair_findings,
    move_recorded_path_comparison_finding_assertion_to_locality,
    recorded_distinction_pins_from_current_standing,
    record_comparison_of_ordered_relation_path_with_recorded_pair_findings_act_occurrence,
    record_comparison_of_ordered_relation_path_with_recorded_pair_findings_applicability_act_occurrence,
    record_comparison_of_ordered_relation_path_with_recorded_pair_findings_applicability_result,
    record_comparison_of_ordered_relation_path_with_recorded_pair_findings_responsibility_assignment,
    record_comparison_of_ordered_relation_path_with_recorded_pair_findings_result,
)
from seed_runtime.comparison_of_recorded_byte_pair_measurements import (
    RECORDED_PAIR_MEASUREMENT_COMPARISON_RESULT_KIND,
    record_recorded_pair_measurement_comparison_act_occurrence,
    record_recorded_pair_measurement_comparison_applicability_act_occurrence,
    record_recorded_pair_measurement_comparison_applicability_result,
    record_recorded_pair_measurement_comparison_responsibility_assignment,
    record_recorded_pair_measurement_comparison_result,
)
from seed_runtime.byte_measurement import (
    BYTE_MEASUREMENT_RECORDED_KIND,
    ByteMeasurementError,
    record_byte_position_pair_count_layer,
)
from seed_runtime.events import EventLedger, SQLiteEventLedger
from seed_runtime.witness_material_acquisition import WITNESS_MATERIAL_ACQUISITION_RECORDED_KIND, record_witness_material_acquisition
from seed_runtime.measurement_of_position_coordinates_of_byte_pair_occurrences import (
    BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND,
    _source_position_coordinate_reference,
    references_to_recorded_position_coordinates_of_byte_pair_occurrences,
    move_recorded_position_assertion_to_locality,
)
from seed_runtime.measurement_of_shared_position_of_byte_pair_occurrences import (
    get_recorded_shared_position_measurement,
    record_shared_position_applicability_act_occurrence,
    record_shared_position_applicability_result,
    record_shared_position_measurement_act_occurrence,
    record_shared_position_measurement_result,
    record_shared_position_responsibility_assignment_from_addressed_byte_occurrence_reference_determination_result,
)
from seed_runtime.operator_console import run_persistent_operator_console
from seed_runtime.operator_current_coordinates import (
    advance_operator_current_coordinates,
    read_operator_current_coordinates,
)
from seed_runtime.declared_measurement_responsibilities import (
    record_declared_measurements_from_current_bounded_locality_replay,
)


CLAIM = b"2+2=5\n"
EARLIER_MATERIAL = b"2+2=\n"
ADDRESSED_POSITION = 3


def _advance(ledger, standing, *events):
    return advance_operator_current_coordinates(
        ledger,
        (event.identity for event in events),
        locality_identity=standing["locality_identity"],
        prior=standing,
    )


def _standing(ledger):
    return read_operator_current_coordinates(
        ledger, locality_identity="calculator-claim"
    )


def _pair_measurement(ledger, declared):
    byte_result = next(
        event
        for event in declared.result_occurrences
        if event.kind == BYTE_MEASUREMENT_RECORDED_KIND
    )
    return record_byte_position_pair_count_layer(
        ledger,
        source_measurement_event_identity=byte_result.identity,
        recording_locality_identity="calculator-claim",
    )


def _pair_comparison(ledger, earlier, later):
    assignment = record_recorded_pair_measurement_comparison_responsibility_assignment(
        ledger,
        earlier_result_event_identity=earlier.identity,
        later_result_event_identity=later.identity,
        locality_standing=_standing(ledger),
    )
    applicability_act = record_recorded_pair_measurement_comparison_applicability_act_occurrence(
        ledger,
        responsibility_assignment_event_identity=assignment.identity,
        locality_standing=_standing(ledger),
    )
    applicability = record_recorded_pair_measurement_comparison_applicability_result(
        ledger,
        act_occurrence_event_identity=applicability_act.identity,
    )
    act = record_recorded_pair_measurement_comparison_act_occurrence(
        ledger,
        responsibility_assignment_event_identity=assignment.identity,
        applicability_result_event_identity=applicability.identity,
        locality_standing=_standing(ledger),
    )
    return record_recorded_pair_measurement_comparison_result(
        ledger, act_occurrence_event_identity=act.identity
    )


def _path_comparison(ledger, path, pair_comparison):
    assignment = record_comparison_of_ordered_relation_path_with_recorded_pair_findings_responsibility_assignment(
        ledger,
        path_result_event_identity=path.identity,
        comparison_result_event_identity=pair_comparison.identity,
        locality_standing=_standing(ledger),
    )
    applicability_act = record_comparison_of_ordered_relation_path_with_recorded_pair_findings_applicability_act_occurrence(
        ledger,
        responsibility_assignment_event_identity=assignment.identity,
        locality_standing=_standing(ledger),
    )
    applicability = record_comparison_of_ordered_relation_path_with_recorded_pair_findings_applicability_result(
        ledger,
        act_occurrence_event_identity=applicability_act.identity,
    )
    act = record_comparison_of_ordered_relation_path_with_recorded_pair_findings_act_occurrence(
        ledger,
        responsibility_assignment_event_identity=assignment.identity,
        applicability_result_event_identity=applicability.identity,
        locality_standing=_standing(ledger),
    )
    return record_comparison_of_ordered_relation_path_with_recorded_pair_findings_result(
        ledger, act_occurrence_event_identity=act.identity
    )


def _claim_path(ledger):
    earlier_source = record_witness_material_acquisition(
        ledger,
        locality_identity="calculator-claim",
        exact_bytes=EARLIER_MATERIAL,
        source_boundary="earlier exact supplied material boundary",
    )
    earlier_declared = record_declared_measurements_from_current_bounded_locality_replay(
        ledger,
        locality_identity=earlier_source.locality_identity,
    )
    earlier_pair = _pair_measurement(ledger, earlier_declared)
    source = record_witness_material_acquisition(
        ledger,
        locality_identity="calculator-claim",
        exact_bytes=CLAIM,
        source_boundary="exact supplied claim boundary",
        provenance_occurrence_references=(earlier_source.identity,),
    )
    declared = record_declared_measurements_from_current_bounded_locality_replay(
        ledger,
        locality_identity=source.locality_identity,
    )
    standing = declared.bounded_locality_replay
    direct_result = next(
        event
        for event in declared.result_occurrences
        if event.kind == BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND
    )
    claim_pair = _pair_measurement(ledger, declared)
    pair_comparison = _pair_comparison(ledger, earlier_pair, claim_pair)
    standing = _standing(ledger)
    coordinate = _source_position_coordinate_reference(
        source_material_acquisition_occurrence_identity=source.identity,
        source_locality_identity=source.locality_identity,
        completeness_boundary_identity=(
            ledger.append_boundary_through_occurrence(source.identity).identity
        ),
        position=ADDRESSED_POSITION,
        exact_material=CLAIM[ADDRESSED_POSITION : ADDRESSED_POSITION + 1],
    )
    standing, determination_result = _record_addressed_byte_occurrence_reference_determination_lifecycle_from_carried_standing(
        ledger,
        direct_result_event_identity=direct_result.identity,
        addressed_source_byte_position_coordinate_reference=coordinate,
        locality_standing=standing,
    )
    shared_assignment = record_shared_position_responsibility_assignment_from_addressed_byte_occurrence_reference_determination_result(
        ledger,
        determination_result_event_identity=determination_result.identity,
        locality_standing=standing,
    )
    standing = _advance(ledger, standing, shared_assignment)
    shared_applicability_act = record_shared_position_applicability_act_occurrence(
        ledger,
        assignment_event_identity=shared_assignment.identity,
        locality_standing=standing,
    )
    standing = _advance(ledger, standing, shared_applicability_act)
    shared_applicability = record_shared_position_applicability_result(
        ledger,
        applicability_act_occurrence_event_identity=shared_applicability_act.identity,
    )
    standing = _advance(ledger, standing, shared_applicability)
    shared_act = record_shared_position_measurement_act_occurrence(
        ledger,
        applicability_result_event_identity=shared_applicability.identity,
        locality_standing=standing,
    )
    standing = _advance(ledger, standing, shared_act)
    shared_result = record_shared_position_measurement_result(
        ledger,
        measurement_act_occurrence_event_identity=shared_act.identity,
    )
    standing = _advance(ledger, standing, shared_result)
    path_comparison = _path_comparison(ledger, shared_result, pair_comparison)
    standing = _standing(ledger)
    return source, shared_result, path_comparison, standing


@pytest.fixture(scope="module")
def calculator_boundary_witness():
    if not Path("/usr/bin/gnome-calculator").is_file():
        pytest.skip("fixed calculator invocation is unavailable")
    ledger = EventLedger()
    earlier_source = record_witness_material_acquisition(
        ledger,
        locality_identity="calculator-claim",
        exact_bytes=EARLIER_MATERIAL,
        source_boundary="earlier exact Witness material boundary",
    )
    claim_source = record_witness_material_acquisition(
        ledger,
        locality_identity="calculator-claim",
        exact_bytes=CLAIM,
        source_boundary="exact Witness claim boundary",
        provenance_occurrence_references=(earlier_source.identity,),
    )
    run_persistent_operator_console(
        ledger=ledger,
        locality_identity="calculator-operator",
        input_stream=BytesIO(b"!calculator 2+2\n"),
        operator_invocation_provider=invoke_operator_host,
    )
    invocation_locality = next(
        event.material["destination_locality_identity"]
        for event in ledger.list()
        if event.kind == "operator.invocation_locality_recorded"
    )
    stdout = next(
        event
        for event in ledger.list()
        if event.kind == WITNESS_MATERIAL_ACQUISITION_RECORDED_KIND
        and event.locality_identity == invocation_locality
        and event.exact_material == b"4\n"
    )
    return {
        "ledger": ledger,
        "earlier_source": earlier_source,
        "claim_source": claim_source,
        "invocation_locality": invocation_locality,
        "stdout": stdout,
    }


@pytest.fixture(scope="module")
def calculator_relation_witness(calculator_boundary_witness):
    pytest.skip(
        "calculator Witness material stops before Measurement until its "
        "material-to-this-Seed Locality relation and Act occurrence exist"
    )


def test_calculator_examples_remain_exact_witness_material(
    calculator_boundary_witness,
):
    witness = calculator_boundary_witness

    assert witness["earlier_source"].exact_material == EARLIER_MATERIAL
    assert witness["claim_source"].exact_material == CLAIM
    assert witness["claim_source"].material[
        "provenance_occurrence_references"
    ] == [witness["earlier_source"].identity]


def test_calculator_stdout_remains_exact_provenanced_o2(
    calculator_boundary_witness,
):
    witness = calculator_boundary_witness
    stdout = witness["stdout"]

    assert stdout.exact_material == b"4\n"
    assert stdout.material["provenance_occurrence_references"]


def test_calculator_o2_records_no_measurement_path_compare_or_candidate(
    calculator_boundary_witness,
):
    witness = calculator_boundary_witness
    events = witness["ledger"].list()
    o2_identity = witness["stdout"].identity

    assert not tuple(
        event
        for event in events
        if event.kind == BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND
        and event.material.get("source_material_acquisition_occurrence_identity")
        == o2_identity
    )
    assert not tuple(
        event
        for event in events
        if event.kind
        in {
            COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_RESULT_KIND,
            RECORDED_PAIR_MEASUREMENT_COMPARISON_RESULT_KIND,
        }
        and event.locality_identity == witness["invocation_locality"]
    )


def test_claim_preserves_one_uninterpreted_path(calculator_relation_witness):
    witness = calculator_relation_witness
    reading = get_recorded_shared_position_measurement(
        witness["ledger"], witness["path_result"].identity
    )
    assertion = reading["assertions"][0]

    assert witness["claim_source"].exact_material == CLAIM
    assert assertion["result"] == "ordered_relation_path"
    assert assertion["dimensions"]["content"][
        "shared_position_coordinate_reference"
    ]["exact_material"] == [0x3D]
    assert reading["unknown"] == [
        "what this ordered relation path represents: Unknown"
    ]
    assert witness["path_result"].identity in witness["claim_standing"][
        "measurement_occurrences"
    ]


def test_claim_path_reaches_recorded_distinctions_without_acquiring_meaning(
    calculator_relation_witness,
):
    witness = calculator_relation_witness
    reading = get_recorded_comparison_of_ordered_relation_path_with_recorded_pair_findings(
        witness["ledger"], witness["path_comparison"].identity
    )
    roles = reading["finding"]["relation_findings"]

    assert [role["pair_subject"] for role in roles] == [[0x32, 0x3D], [0x3D, 0x35]]
    assert [
        [reference["finding_category"] for reference in role["comparison_finding_references"]]
        for role in roles
    ] == [
        ["conflicting_findings", "findings_of_later_result"],
        ["findings_of_later_result"],
    ]
    assert reading["finding"]["unknown"] == [
        "what the relation of the ordered path and recorded comparison findings represents: Unknown"
    ]
    assert reading["unknown"] == [
        "what the relation of path and comparison findings represents: Unknown"
    ]
    assert witness["path_comparison"].identity in witness["claim_standing"][
        "comparison_result_occurrences"
    ]

    pins = recorded_distinction_pins_from_current_standing(
        witness["ledger"], locality_identity="calculator-claim"
    )
    assert tuple(
        (pin.pair_subject, pin.recorded_finding_reference["finding_category"])
        for pin in pins
    ) == (
        (b"2=", "conflicting_findings"),
        (b"2=", "findings_of_later_result"),
        (b"=5", "findings_of_later_result"),
    )


def test_calculator_result_preserves_its_own_occurrence_and_provenance(
    calculator_relation_witness,
):
    witness = calculator_relation_witness
    references = references_to_recorded_position_coordinates_of_byte_pair_occurrences(
        witness["ledger"], witness["stdout_result"].identity
    )
    witness_standing = read_operator_current_coordinates(
        witness["ledger"], locality_identity=witness["invocation_locality"]
    )

    assert witness["stdout"].exact_material == b"4\n"
    assert len(witness["stdout"].material["provenance_occurrence_references"]) == 2
    assert tuple(
        (reference.exact_pair, reference.first_position, reference.second_position)
        for reference in references
    ) == ((b"4\n", 0, 1),)
    assert witness["stdout_result"].identity in witness_standing[
        "measurement_occurrences"
    ]


def test_no_current_act_compares_recorded_distinction_with_calculator_result(
    calculator_relation_witness,
):
    witness = calculator_relation_witness
    higher_results = tuple(
        event
        for event in witness["ledger"].list()
        if event.kind
        == COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_RESULT_KIND
    )

    assert len(higher_results) == 1
    assert higher_results[0].locality_identity == "calculator-claim"
    reading = get_recorded_comparison_of_ordered_relation_path_with_recorded_pair_findings(
        witness["ledger"], higher_results[0].identity
    )
    assignment = witness["ledger"].get(
        reading["responsibility_assignment_reference"][
            "recorded_occurrence_identity"
        ]
    )
    assert assignment.material["path_source_occurrence_identity"] == witness[
        "claim_source"
    ].identity
    assert assignment.material["comparison_added_occurrence_identity"] == witness[
        "claim_source"
    ].identity
    assert witness["stdout"].identity not in json.dumps(reading, sort_keys=True)
    assert all(
        event.locality_identity != witness["invocation_locality"]
        for event in witness["ledger"].list()
        if event.kind == RECORDED_PAIR_MEASUREMENT_COMPARISON_RESULT_KIND
    )


def test_two_assertion_movements_construct_one_locality_without_a_relation(
    calculator_relation_witness,
):
    witness = calculator_relation_witness
    ledger = witness["ledger"]
    destination = "calculator-relation-construction"
    distinction = move_recorded_path_comparison_finding_assertion_to_locality(
        ledger,
        comparison_result_occurrence_identity=witness["path_comparison"].identity,
        destination_locality=destination,
    )
    record_witness_material_acquisition(
        ledger,
        locality_identity="unrelated-locality",
        exact_bytes=b"unrelated",
        source_boundary="between two Assertion movements",
    )
    calculator_position = (
        references_to_recorded_position_coordinates_of_byte_pair_occurrences(
            ledger, witness["stdout_result"].identity
        )[0]
    )
    calculator = move_recorded_position_assertion_to_locality(
        ledger,
        source_assertion_reference=calculator_position.assertion_reference,
        destination_locality=destination,
    )
    standing = read_operator_current_coordinates(
        ledger, locality_identity=destination
    )
    movements = standing["assertion_locality_movement_occurrences"]

    assert tuple(movements) == (
        distinction.locality_movement_event_identity,
        calculator.locality_movement_event_identity,
    )
    assert tuple(
        coordinates["source_assertion_reference"]
        for coordinates in movements.values()
    ) == (
        distinction.source_assertion_reference,
        calculator_position.assertion_reference,
    )
    assert tuple(
        coordinates["source_assertion_coordinates"]
        for coordinates in movements.values()
    ) == (
        distinction.source_assertion_coordinates,
        calculator.source_assertion_coordinates,
    )
    movement_events = tuple(ledger.get(identity) for identity in movements)
    assert tuple(
        (
            event.material["locality_relation"]["first_subject"],
            event.material["locality_relation"]["second_subject"],
        )
        for event in movement_events
    ) == (
        (distinction.source_assertion_reference, destination),
        (calculator_position.assertion_reference, destination),
    )
    assert len(
        {
            event.material["locality_relation"]["relation_occurrence_identity"]
            for event in movement_events
        }
    ) == 2
    assert standing["comparison_result_occurrences"] == {}
    assert standing["applicability_result_occurrences"] == {}
    assert standing["recorded_relation_Standing"] == {}


def test_position_assertion_coordinates_stay_distinct_from_movement_coordinates(
    calculator_relation_witness,
):
    witness = calculator_relation_witness
    ledger = witness["ledger"]
    position = references_to_recorded_position_coordinates_of_byte_pair_occurrences(
        ledger, witness["stdout_result"].identity
    )[0]
    carried = move_recorded_position_assertion_to_locality(
        ledger,
        source_assertion_reference=position.assertion_reference,
        destination_locality="calculator-position-coordinate-preservation",
    )
    movement = ledger.get(carried.locality_movement_event_identity)
    assignment = ledger.get(
        movement.material["responsibility_assignment_reference"][
            "recorded_occurrence_identity"
        ]
    )
    producer_assignment = ledger.get(
        witness["stdout_result"].material["responsibility_assignment_reference"][
            "recorded_occurrence_identity"
        ]
    )
    standing = read_operator_current_coordinates(
        ledger, locality_identity=movement.locality_identity
    )
    coordinates = standing["assertion_locality_movement_occurrences"][
        movement.identity
    ]
    source_coordinates = carried.source_assertion_coordinates

    assert source_coordinates["dimensions"]["authority"] == "unestablished"
    assert (
        source_coordinates["dimensions"]["identity"]
        == position.assertion_identity
    )
    assert coordinates["source_assertion_coordinates"] == source_coordinates
    assert assignment.material["authority"] == "unestablished"
    assert assignment.material["authority"] != producer_assignment.material[
        "authority"
    ]
    assert source_coordinates["assertion_scope"] != assignment.material["scope"]
    assert coordinates["source_standing_boundary_identity"] == assignment.material[
        "source_standing_boundary_identity"
    ]
    source_result = ledger.get(
        coordinates["source_assertion_reference"][
            "recorded_occurrence_identity"
        ]
    )
    assert source_result is witness["stdout_result"]
    assert tuple(
        source_result.material[coordinate]
        for coordinate in (
            "act_occurrence_identity",
            "yield_relation_identity",
        )
    ) == (
        witness["stdout_result"].material[
            "act_occurrence_identity"
        ],
        witness["stdout_result"].material[
            "yield_relation_identity"
        ],
    )


def _assert_assertion_movement_standing_requires_exact_source(
    witness, source_name
):
    ledger = witness["ledger"]
    destination = f"calculator-relation-source-integrity-{source_name}"
    move_recorded_path_comparison_finding_assertion_to_locality(
        ledger,
        comparison_result_occurrence_identity=witness["path_comparison"].identity,
        destination_locality=destination,
    )
    calculator_position = (
        references_to_recorded_position_coordinates_of_byte_pair_occurrences(
            ledger, witness["stdout_result"].identity
        )[0]
    )
    move_recorded_position_assertion_to_locality(
        ledger,
        source_assertion_reference=calculator_position.assertion_reference,
        destination_locality=destination,
    )
    source = witness[source_name]
    exact_material = deepcopy(source.material)
    source.material["unknown"] = ["changed after both movement results"]
    try:
        with pytest.raises((ByteMeasurementError, ValueError)):
            read_operator_current_coordinates(
                ledger, locality_identity=destination
            )
    finally:
        source.material.clear()
        source.material.update(exact_material)


def test_assertion_movement_standing_requires_exact_path_comparison_result(
    calculator_relation_witness,
):
    _assert_assertion_movement_standing_requires_exact_source(
        calculator_relation_witness,
        "path_comparison",
    )


def test_assertion_movement_standing_requires_exact_position_measurement_result(
    calculator_relation_witness,
):
    _assert_assertion_movement_standing_requires_exact_source(
        calculator_relation_witness,
        "stdout_result",
    )


def test_calculator_witness_material_remains_available_without_measurement_after_restart(
    tmp_path,
):
    path = tmp_path / "calculator-relation-construction.sqlite"
    ledger = SQLiteEventLedger(path)
    claim_source = record_witness_material_acquisition(
        ledger,
        locality_identity="calculator-result",
        exact_bytes=CLAIM,
        source_boundary="exact Witness claim boundary",
    )
    calculator_source = record_witness_material_acquisition(
        ledger,
        locality_identity="calculator-result",
        exact_bytes=b"4\n",
        source_boundary="exact Witness calculator result boundary",
        provenance_occurrence_references=(claim_source.identity,),
    )
    expected = deepcopy(
        read_operator_current_coordinates(
            ledger, locality_identity=calculator_source.locality_identity
        )
    )
    ledger.close()

    reopened = SQLiteEventLedger(path)
    try:
        replayed = read_operator_current_coordinates(
            reopened, locality_identity=calculator_source.locality_identity
        )
        assert replayed == expected
        assert tuple(
            occurrence["result_occurrence_identity"]
            for occurrence in replayed["material_acquisition_result_occurrences"]
        ) == (claim_source.identity, calculator_source.identity)
        assert replayed["operator_material_locality_relation_occurrences"] == {}
        assert replayed["measurement_occurrences"] == {}
    finally:
        reopened.close()
