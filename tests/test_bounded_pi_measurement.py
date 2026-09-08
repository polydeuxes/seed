"""One exact bounded byte Measurement."""

from copy import deepcopy

from seed_runtime.byte_measurement import (
    result_positions_of_recorded_byte_measurement,
    record_byte_measurement_subject_to_act_binding,
    record_byte_position_pair_count_layer,
    record_byte_measurement_act_occurrence,
    record_byte_measurement_result,
)
from seed_runtime.events import EventLedger
from seed_runtime.operator_current_coordinates import read_operator_current_coordinates
from tests.operator_material_source_test_witness import (
    record_operator_material_occurrence,
)


def _record_byte_measurement(
    ledger, *, source_localities, recording_locality_identity
):
    assignment = record_byte_measurement_subject_to_act_binding(
        ledger,
        source_localities=source_localities,
        recording_locality_identity=recording_locality_identity,
        current_coordinates=read_operator_current_coordinates(
            ledger, locality_identity=recording_locality_identity
        ),
    )
    act_occurrence = record_byte_measurement_act_occurrence(
        ledger,
        subject_to_act_binding_event_identity=assignment.identity,
        current_coordinates=read_operator_current_coordinates(
            ledger, locality_identity=recording_locality_identity
        ),
    )
    return record_byte_measurement_result(
        ledger,
        act_occurrence_event_identity=act_occurrence.identity,
    )


SHORT = b"3.14159"
LONG = SHORT + b"26"


def _supply(ledger: EventLedger, locality: str, material: bytes) -> None:
    record_operator_material_occurrence(
        ledger=ledger,
        locality_identity=locality,
        exact=material,
        source_boundary=f"{locality} boundary",
    )


def _measure(ledger: EventLedger, source: str, result: str):
    byte_event = _record_byte_measurement(
        ledger,
        source_localities=(source,),
        recording_locality_identity=f"{result}-bytes",
    )
    pair_event = record_byte_position_pair_count_layer(
        ledger,
        source_measurement_event_identity=byte_event.identity,
        recording_locality_identity=f"{result}-pairs",
    )
    return byte_event, pair_event


def _pair_counts(event):
    return {
        bytes(result_position["subject"]["content"]): result_position["dimensions"][
            "content"
        ]["count"]
        for result_position in event.material["result_positions"]
        if result_position["result"] == "count"
    }


def test_one_bounded_decimal_material_does_not_gain_its_human_attribution():
    ledger = EventLedger()
    _supply(ledger, "short-source", SHORT)
    byte_event, pair_event = _measure(ledger, "short-source", "short")

    byte_result_positions = result_positions_of_recorded_byte_measurement(ledger, byte_event.identity)
    pair_counts = _pair_counts(pair_event)

    assert any(
        result_position["subject"].get("content") == 46
        for result_position in byte_result_positions
    )
    assert pair_counts[b"3."] == 1
    assert pair_counts[b".1"] == 1
    assert pair_counts[b"59"] == 1
    assert all(count == 1 for count in pair_counts.values())
    assert "pi" not in str(byte_event.material).lower()
    assert "pi" not in str(pair_event.material).lower()


def test_a_longer_prefix_is_new_material_and_does_not_rewrite_the_shorter_one():
    ledger = EventLedger()
    _supply(ledger, "short-source", SHORT)
    short_bytes, short_pairs = _measure(ledger, "short-source", "short")
    short_material = deepcopy(short_bytes).material
    short_pair_counts = _pair_counts(short_pairs)

    _supply(ledger, "long-source", LONG)
    long_bytes, long_pairs = _measure(ledger, "long-source", "long")

    short_source = result_positions_of_recorded_byte_measurement(ledger, short_bytes.identity)[0]
    long_source = result_positions_of_recorded_byte_measurement(ledger, long_bytes.identity)[0]
    assert (
        short_bytes.identity,
        short_source["dimensions"]["position"],
    ) != (
        long_bytes.identity,
        long_source["dimensions"]["position"],
    )
    assert short_bytes.material == short_material
    assert _pair_counts(short_pairs) == short_pair_counts
    assert _pair_counts(long_pairs)[b"26"] == 1
    assert long_pairs.material["completeness_boundary"] != short_pairs.material[
        "completeness_boundary"
    ]
