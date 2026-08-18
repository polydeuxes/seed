"""Carry one calculator result beside one exact path through distinctions.

The path around byte ``0x3d`` meets exact findings from an earlier-to-claim
pair comparison while its represented relation remains Unknown.  The external
result enters through its own invocation lifecycle; no current Responsibility
compares it with the path finding or establishes arithmetic meaning.
"""

from __future__ import annotations

import json
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
from seed_runtime.byte_measurement import (
    BYTE_MEASUREMENT_RECORDED_KIND,
    record_byte_position_pair_count_layer,
)
from seed_runtime.events import EventLedger
from seed_runtime.material_ingest import MATERIAL_INGEST_OCCURRED_KIND, ingest_material
from seed_runtime.measurement_of_position_coordinates_of_byte_pair_occurrences import (
    BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND,
    _source_position_coordinate_reference,
    references_to_recorded_position_coordinates_of_byte_pair_occurrences,
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
    return {
        "ledger": ledger,
        "claim_source": claim_source,
        "path_result": path_result,
        "path_comparison": path_comparison,
        "claim_standing": claim_standing,
        "system_locality": system_locality,
        "stdout": stdout,
        "stdout_result": stdout_result,
        "raw_output": raw_output.getvalue(),
    }


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
        "what this ordered relation path represents remains Unknown"
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
        "what the relation of the ordered path and recorded comparison findings represents remains Unknown"
    ]
    assert reading["unknown"] == [
        "what the relation of path and comparison findings represents remains Unknown"
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
