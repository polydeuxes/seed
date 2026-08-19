"""Carry one calculator result beside one exact path through distinctions.

The path around byte ``0x3d`` meets exact findings from an earlier-to-claim
pair comparison while carrying Unknown for its represented relation.  The external
result enters through its own invocation lifecycle; no current Responsibility
compares it with the path finding or establishes arithmetic meaning.
"""

from __future__ import annotations

import json
from copy import deepcopy
from io import BytesIO, StringIO
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
    record_comparison_of_ordered_relation_path_with_recorded_pair_findings_act_evidence,
    record_comparison_of_ordered_relation_path_with_recorded_pair_findings_applicability_act_evidence,
    record_comparison_of_ordered_relation_path_with_recorded_pair_findings_applicability_result,
    record_comparison_of_ordered_relation_path_with_recorded_pair_findings_responsibility_assignment,
    record_comparison_of_ordered_relation_path_with_recorded_pair_findings_result,
)
from seed_runtime.comparison_of_recorded_byte_pair_measurements import (
    RECORDED_PAIR_MEASUREMENT_COMPARISON_RESULT_KIND,
    record_recorded_pair_measurement_comparison_act_evidence,
    record_recorded_pair_measurement_comparison_applicability_act_evidence,
    record_recorded_pair_measurement_comparison_applicability_result,
    record_recorded_pair_measurement_comparison_responsibility_assignment,
    record_recorded_pair_measurement_comparison_result,
)
from seed_runtime.candidate_standing_from_exact_result_assertions import (
    boundaries_of_recorded_candidate_standing,
    exact_source_assertion_materials_from_every_ordered_pair_candidate,
    get_recorded_candidate_standing,
    ordered_candidate_locality_standing_through_result_occurrence_beside_represented_relation_coordinates,
    record_one_source_and_ordered_pair_candidate_standings,
)
from seed_runtime.byte_measurement import (
    BYTE_MEASUREMENT_RECORDED_KIND,
    ByteMeasurementError,
    record_byte_position_pair_count_layer,
)
from seed_runtime.events import EventLedger, SQLiteEventLedger
from seed_runtime.material_ingest import MATERIAL_INGEST_OCCURRED_KIND, ingest_material
from seed_runtime.measurement_of_position_coordinates_of_byte_pair_occurrences import (
    BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND,
    _source_position_coordinate_reference,
    references_to_recorded_position_coordinates_of_byte_pair_occurrences,
    move_recorded_position_assertion_to_locality,
)
from seed_runtime.measurement_of_shared_position_of_byte_pair_occurrences import (
    get_recorded_shared_position_measurement,
    record_shared_position_applicability_act_evidence,
    record_shared_position_applicability_result,
    record_shared_position_measurement_act_evidence,
    record_shared_position_measurement_result,
    record_shared_position_responsibility_assignment_from_addressed_byte_occurrence_reference_determination_result,
)
from seed_runtime.operator_console import run_persistent_operator_console
from seed_runtime.operator_locality_standing import (
    advance_operator_locality_standing,
    read_operator_locality_standing,
)
from seed_runtime.standing_measurement_declarations import (
    record_declared_measurements_from_current_standing,
)


CLAIM = b"2+2=5\n"
EARLIER_MATERIAL = b"2+2=\n"
ADDRESSED_POSITION = 3


def _advance(ledger, standing, *events):
    return advance_operator_locality_standing(
        ledger,
        (event.identity for event in events),
        locality_identity=standing["locality_identity"],
        prior=standing,
    )


def _standing(ledger):
    return read_operator_locality_standing(
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
    applicability_act = record_recorded_pair_measurement_comparison_applicability_act_evidence(
        ledger,
        responsibility_assignment_event_identity=assignment.identity,
        locality_standing=_standing(ledger),
    )
    applicability = record_recorded_pair_measurement_comparison_applicability_result(
        ledger,
        responsible_act_evidence_event_identity=applicability_act.identity,
    )
    act = record_recorded_pair_measurement_comparison_act_evidence(
        ledger,
        responsibility_assignment_event_identity=assignment.identity,
        applicability_result_event_identity=applicability.identity,
        locality_standing=_standing(ledger),
    )
    return record_recorded_pair_measurement_comparison_result(
        ledger, responsible_act_evidence_event_identity=act.identity
    )


def _path_comparison(ledger, path, pair_comparison):
    assignment = record_comparison_of_ordered_relation_path_with_recorded_pair_findings_responsibility_assignment(
        ledger,
        path_result_event_identity=path.identity,
        comparison_result_event_identity=pair_comparison.identity,
        locality_standing=_standing(ledger),
    )
    applicability_act = record_comparison_of_ordered_relation_path_with_recorded_pair_findings_applicability_act_evidence(
        ledger,
        responsibility_assignment_event_identity=assignment.identity,
        locality_standing=_standing(ledger),
    )
    applicability = record_comparison_of_ordered_relation_path_with_recorded_pair_findings_applicability_result(
        ledger,
        responsible_act_evidence_event_identity=applicability_act.identity,
    )
    act = record_comparison_of_ordered_relation_path_with_recorded_pair_findings_act_evidence(
        ledger,
        responsibility_assignment_event_identity=assignment.identity,
        applicability_result_event_identity=applicability.identity,
        locality_standing=_standing(ledger),
    )
    return record_comparison_of_ordered_relation_path_with_recorded_pair_findings_result(
        ledger, responsible_act_evidence_event_identity=act.identity
    )


def _claim_path(ledger):
    earlier_source = ingest_material(
        ledger,
        locality_identity="calculator-claim",
        exact_bytes=EARLIER_MATERIAL,
        source_role="system",
        source_boundary="earlier exact supplied material boundary",
    )
    earlier_declared = record_declared_measurements_from_current_standing(
        ledger,
        locality_identity=earlier_source.locality_identity,
    )
    earlier_pair = _pair_measurement(ledger, earlier_declared)
    source = ingest_material(
        ledger,
        locality_identity="calculator-claim",
        exact_bytes=CLAIM,
        source_role="system",
        source_boundary="exact supplied claim boundary",
        provenance_occurrence_references=(earlier_source.identity,),
    )
    declared = record_declared_measurements_from_current_standing(
        ledger,
        locality_identity=source.locality_identity,
    )
    standing = declared.locality_standing
    direct_result = next(
        event
        for event in declared.result_occurrences
        if event.kind == BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND
    )
    claim_pair = _pair_measurement(ledger, declared)
    pair_comparison = _pair_comparison(ledger, earlier_pair, claim_pair)
    standing = _standing(ledger)
    coordinate = _source_position_coordinate_reference(
        source_ingest_occurrence_identity=source.identity,
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
    shared_applicability_act = record_shared_position_applicability_act_evidence(
        ledger,
        assignment_event_identity=shared_assignment.identity,
        locality_standing=standing,
    )
    standing = _advance(ledger, standing, shared_applicability_act)
    shared_applicability = record_shared_position_applicability_result(
        ledger,
        applicability_act_evidence_event_identity=shared_applicability_act.identity,
    )
    standing = _advance(ledger, standing, shared_applicability)
    shared_act = record_shared_position_measurement_act_evidence(
        ledger,
        applicability_result_event_identity=shared_applicability.identity,
        locality_standing=standing,
    )
    standing = _advance(ledger, standing, shared_act)
    shared_result = record_shared_position_measurement_result(
        ledger,
        measurement_act_evidence_event_identity=shared_act.identity,
    )
    standing = _advance(ledger, standing, shared_result)
    path_comparison = _path_comparison(ledger, shared_result, pair_comparison)
    standing = _standing(ledger)
    return source, shared_result, path_comparison, standing


@pytest.fixture(scope="module")
def calculator_relation_witness():
    if not Path("/usr/bin/gnome-calculator").is_file():
        pytest.skip("fixed calculator invocation is unavailable")
    ledger = EventLedger()
    claim_source, path_result, path_comparison, claim_standing = _claim_path(ledger)
    raw_output = BytesIO()
    run_persistent_operator_console(
        ledger=ledger,
        locality_identity="calculator-operator",
        input_stream=BytesIO(b"!calculator 2+2\n"),
        output_stream=StringIO(),
        raw_output_stream=raw_output,
        operator_invocation_provider=invoke_operator_host,
    )
    system_locality = next(
        event.material["destination_locality_identity"]
        for event in ledger.list()
        if event.kind == "operator.invocation_locality_recorded"
    )
    stdout = next(
        event
        for event in ledger.list()
        if event.kind == MATERIAL_INGEST_OCCURRED_KIND
        and event.locality_identity == system_locality
        and event.exact_material == b"4\n"
    )
    stdout_result = next(
        event
        for event in ledger.list()
        if event.kind == BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND
        and event.material["source_ingest_occurrence_identity"] == stdout.identity
    )
    candidate_source_boundary = ledger.append_boundary()
    (
        candidate_standing_result,
        ordered_pair_candidate_standing_result,
    ) = record_one_source_and_ordered_pair_candidate_standings(
        ledger,
        one_source_recording_locality_identity="calculator-candidate-standing",
        ordered_pair_recording_locality_identity=(
            "calculator-ordered-pair-candidate-standing"
        ),
        source_append_boundary=candidate_source_boundary,
    )
    return {
        "ledger": ledger,
        "claim_source": claim_source,
        "path_result": path_result,
        "path_comparison": path_comparison,
        "claim_standing": claim_standing,
        "system_locality": system_locality,
        "stdout": stdout,
        "stdout_result": stdout_result,
        "candidate_source_boundary": candidate_source_boundary,
        "candidate_standing_result": candidate_standing_result,
        "ordered_pair_candidate_standing_result": (
            ordered_pair_candidate_standing_result
        ),
        "raw_output": raw_output.getvalue(),
    }


def test_complete_unary_candidate_standing_cannot_omit_either_calculator_branch(
    calculator_relation_witness,
):
    witness = calculator_relation_witness
    ledger = witness["ledger"]
    path_finding = get_recorded_comparison_of_ordered_relation_path_with_recorded_pair_findings(
        ledger, witness["path_comparison"].identity
    )["finding"]
    calculator_position = (
        references_to_recorded_position_coordinates_of_byte_pair_occurrences(
            ledger, witness["stdout_result"].identity
        )[0]
    )
    candidate_standing = get_recorded_candidate_standing(
        ledger, witness["candidate_standing_result"].identity
    )
    references = candidate_standing["source_assertion_references"]
    assertion_identities = {
        reference["assertion_identity"] for reference in references
    }

    assert path_finding["identity"] in assertion_identities
    assert calculator_position.assertion_identity in assertion_identities
    assert all(
        candidate["represented_relation"] == "Unknown"
        for candidate in candidate_standing["candidate_assertions"]
    )
    candidate_source_identities = tuple(
        candidate["assertion_subject"]["source_assertion_reference"][
            "assertion_identity"
        ]
        for candidate in candidate_standing["candidate_assertions"]
    )
    assert path_finding["identity"] in candidate_source_identities
    assert calculator_position.assertion_identity in candidate_source_identities
    assert all(
        set(candidate["assertion_subject"])
        == {"source_assertion_reference"}
        for candidate in candidate_standing["candidate_assertions"]
    )
    path_reference = next(
        reference
        for reference in references
        if reference["assertion_identity"] == path_finding["identity"]
    )
    calculator_reference = next(
        reference
        for reference in references
        if reference["assertion_identity"]
        == calculator_position.assertion_identity
    )
    assert path_reference["source_locality_identity"] == "calculator-claim"
    assert (
        calculator_reference["source_locality_identity"]
        == witness["system_locality"]
    )
    assert witness["candidate_standing_result"].locality_identity == (
        "calculator-candidate-standing"
    )
    boundaries = boundaries_of_recorded_candidate_standing(
        ledger, witness["candidate_standing_result"].identity
    )
    assert boundaries["source_ledger_boundary"] == witness[
        "candidate_source_boundary"
    ]
    assert (
        boundaries["source_ledger_boundary"]
        != boundaries["candidate_result_ledger_boundary"]
    )


def test_ordered_pair_candidate_standing_cannot_omit_either_calculator_order(
    calculator_relation_witness,
):
    witness = calculator_relation_witness
    ledger = witness["ledger"]
    path_finding = get_recorded_comparison_of_ordered_relation_path_with_recorded_pair_findings(
        ledger, witness["path_comparison"].identity
    )["finding"]
    calculator_position = (
        references_to_recorded_position_coordinates_of_byte_pair_occurrences(
            ledger, witness["stdout_result"].identity
        )[0]
    )
    result = witness["ordered_pair_candidate_standing_result"]
    standing = get_recorded_candidate_standing(ledger, result.identity)
    source_orders = tuple(
        (
            candidate["assertion_subject"][
                "first_source_assertion_reference"
            ]["assertion_identity"],
            candidate["assertion_subject"][
                "second_source_assertion_reference"
            ]["assertion_identity"],
        )
        for candidate in standing["candidate_assertions"]
    )
    exact_orders = {
        (path_finding["identity"], calculator_position.assertion_identity),
        (calculator_position.assertion_identity, path_finding["identity"]),
    }
    crossing_candidate = next(
        candidate
        for candidate in standing["candidate_assertions"]
        if (
            candidate["assertion_subject"][
                "first_source_assertion_reference"
            ]["assertion_identity"],
            candidate["assertion_subject"][
                "second_source_assertion_reference"
            ]["assertion_identity"],
        )
        == (path_finding["identity"], calculator_position.assertion_identity)
    )
    boundary_before_read = ledger.append_boundary()
    every_exact_ordered_pair = (
        exact_source_assertion_materials_from_every_ordered_pair_candidate(
            ledger,
            candidate_standing_result_event_identity=result.identity,
        )
    )
    _, exact_path_finding, exact_calculator_position = next(
        reading
        for reading in every_exact_ordered_pair
        if reading[0] == crossing_candidate["dimensions"]["identity"]
    )
    candidate_locality_standing, standing_vacancies = (
        ordered_candidate_locality_standing_through_result_occurrence_beside_represented_relation_coordinates(
            ledger,
            candidate_standing_result_event_identity=result.identity,
        )
    )
    every_relation_coordinate = standing_vacancies
    path_source_reference = crossing_candidate["assertion_subject"][
        "first_source_assertion_reference"
    ]
    calculator_source_reference = crossing_candidate["assertion_subject"][
        "second_source_assertion_reference"
    ]

    assert exact_orders <= set(source_orders)
    assert exact_path_finding["identity"] == path_finding["identity"]
    assert exact_calculator_position["dimensions"]["identity"] == (
        calculator_position.assertion_identity
    )
    assert ledger.append_boundary() == boundary_before_read
    assert len(every_exact_ordered_pair) == len(standing["candidate_assertions"])
    assert tuple(
        candidate_identity
        for candidate_identity, *_coordinates in every_relation_coordinate
    ) == tuple(
        candidate["dimensions"]["identity"]
        for candidate in standing["candidate_assertions"]
    )
    assert all(
        relation_coordinate["material"] == "Unknown"
        for *_sources, relation_coordinate in every_relation_coordinate
    )
    assert standing_vacancies == every_relation_coordinate
    assert candidate_locality_standing == {
        "locality_identity": result.locality_identity,
        "through_event_occurrence_identity": result.identity,
        "candidate_result_occurrences": (result.identity,),
    }
    assert "standing_occurrence" not in candidate_locality_standing
    assert "represented_relation" not in candidate_locality_standing
    assert standing["source_ledger_boundary_identity"] == witness[
        "candidate_source_boundary"
    ].identity
    candidate_result_boundary = ledger.append_boundary_through_occurrence(
        result.identity
    )
    assert (
        witness["candidate_source_boundary"] != candidate_result_boundary
    )
    assert all(
        "source_ledger_boundary" not in relation_coordinate
        and "candidate_result_ledger_boundary" not in relation_coordinate
        for *_sources, relation_coordinate in every_relation_coordinate
    )
    assert set(path_source_reference) == set(calculator_source_reference) == {
        "recorded_result_occurrence_identity",
        "recorded_result_occurrence_kind",
        "assertion_identity",
        "assertion_coordinate",
        "source_locality_identity",
        "source_standing_through_event_occurrence_identity",
        "source_standing_coordinate",
        "source_assertion_coordinates",
    }
    assert set(path_source_reference["source_assertion_coordinates"]) == set(
        calculator_source_reference["source_assertion_coordinates"]
    ) == {
        "Evidence",
        "Authority",
        "Scope",
        "limits",
        "Unknown",
    }
    candidate_yield_evidence = ledger.get(
        standing["evidence_of_yield_relation_identity"]
    )
    assert candidate_yield_evidence.material["result_kind"] == (
        "complete Candidate Standing result"
    )
    assert candidate_yield_evidence.material["occurrence_boundary"] == (
        "complete_candidate_standing"
    )
    assert all(
        candidate["represented_relation"] == "Unknown"
        for candidate in standing["candidate_assertions"]
        if (
            candidate["assertion_subject"][
                "first_source_assertion_reference"
            ]["assertion_identity"],
            candidate["assertion_subject"][
                "second_source_assertion_reference"
            ]["assertion_identity"],
        )
        in exact_orders
    )
    assert result.locality_identity == (
        "calculator-ordered-pair-candidate-standing"
    )
    result_locality_standing = read_operator_locality_standing(
        ledger, locality_identity=result.locality_identity
    )
    assert result_locality_standing["comparison_result_occurrences"] == {}
    assert result_locality_standing["recorded_relation_Standing"] == {}


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
    system_standing = read_operator_locality_standing(
        witness["ledger"], locality_identity=witness["system_locality"]
    )

    assert witness["stdout"].exact_material == b"4\n"
    assert len(witness["stdout"].material["provenance_occurrence_references"]) == 2
    assert tuple(
        (reference.exact_pair, reference.first_position, reference.second_position)
        for reference in references
    ) == ((b"4\n", 0, 1),)
    assert witness["stdout_result"].identity in system_standing[
        "measurement_occurrences"
    ]
    assert b"4\n" in witness["raw_output"]


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
        event.locality_identity != witness["system_locality"]
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
    ingest_material(
        ledger,
        locality_identity="unrelated-locality",
        exact_bytes=b"unrelated",
        source_role="test source",
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
    standing = read_operator_locality_standing(
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
    standing = read_operator_locality_standing(
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
            "responsible_act_evidence_identity",
            "evidence_of_yield_relation_identity",
        )
    ) == (
        witness["stdout_result"].material[
            "responsible_act_evidence_identity"
        ],
        witness["stdout_result"].material[
            "evidence_of_yield_relation_identity"
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
            read_operator_locality_standing(
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


def test_two_assertion_movement_coordinates_replay_after_restart(tmp_path):
    path = tmp_path / "calculator-relation-construction.sqlite"
    ledger = SQLiteEventLedger(path)
    _claim_source, _path_result, path_comparison, _claim_standing = _claim_path(
        ledger
    )
    calculator_source = ingest_material(
        ledger,
        locality_identity="calculator-result",
        exact_bytes=b"4\n",
        source_role="system",
        source_boundary="exact calculator result boundary",
    )
    calculator_declared = record_declared_measurements_from_current_standing(
        ledger, locality_identity=calculator_source.locality_identity
    )
    calculator_result = next(
        event
        for event in calculator_declared.result_occurrences
        if event.kind == BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND
    )
    calculator_position = (
        references_to_recorded_position_coordinates_of_byte_pair_occurrences(
            ledger, calculator_result.identity
        )[0]
    )
    destination = "calculator-relation-construction"
    move_recorded_path_comparison_finding_assertion_to_locality(
        ledger,
        comparison_result_occurrence_identity=path_comparison.identity,
        destination_locality=destination,
    )
    move_recorded_position_assertion_to_locality(
        ledger,
        source_assertion_reference=calculator_position.assertion_reference,
        destination_locality=destination,
    )
    expected = deepcopy(
        read_operator_locality_standing(ledger, locality_identity=destination)
    )
    ledger.close()

    reopened = SQLiteEventLedger(path)
    try:
        replayed = read_operator_locality_standing(
            reopened, locality_identity=destination
        )
        assert replayed == expected
        assert tuple(
            coordinates["source_assertion_reference"]
            for coordinates in replayed[
                "assertion_locality_movement_occurrences"
            ].values()
        )[-1] == calculator_position.assertion_reference
        assert replayed["comparison_result_occurrences"] == {}
        assert replayed["applicability_result_occurrences"] == {}
        assert replayed["recorded_relation_Standing"] == {}
    finally:
        reopened.close()
