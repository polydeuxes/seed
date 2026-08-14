"""A finite decimal representation attributed to pi, observed only as bytes."""

from io import StringIO

from seed_runtime.byte_measurement import (
    assertions_of_recorded_byte_measurement,
    record_adjacent_byte_pair_count_layer,
    record_byte_count_layer,
)
from seed_runtime.events import EventLedger
from seed_runtime.operator_console import run_persistent_operator_console


SHORT = "3.14159265358979323846"
LONG = SHORT + "264338327950288419716939937510"


def _supply(ledger: EventLedger, locality: str, material: str) -> None:
    run_persistent_operator_console(
        ledger=ledger,
        workspace_id="bounded-decimal-observation",
        locality_id=locality,
        input_stream=StringIO(material + "\nexit\n"),
        output_stream=StringIO(),
    )


def _observe(ledger: EventLedger, source: str, result: str):
    byte_event = record_byte_count_layer(
        ledger,
        workspace_id="bounded-decimal-observation",
        source_locality_ids=(source,),
        recording_locality_id=f"{result}-bytes",
    )
    pair_event = record_adjacent_byte_pair_count_layer(
        ledger,
        source_measurement_event_id=byte_event.id,
        workspace_id="bounded-decimal-observation",
        recording_locality_id=f"{result}-pairs",
    )
    return byte_event, pair_event


def _pair_counts(event):
    return {
        bytes.fromhex(assertion["assertion_subject"]["pair_hex"]).decode("ascii"):
        assertion["dimensions"]["content"]["total_count"]
        for assertion in event.payload["assertions"]
        if assertion["result"] == "count"
    }


def test_seed_observes_one_bounded_decimal_representation_not_all_of_pi():
    ledger = EventLedger()
    _supply(ledger, "short-source", SHORT)
    byte_event, pair_event = _observe(ledger, "short-source", "short")

    byte_assertions = assertions_of_recorded_byte_measurement(ledger, byte_event.id)
    pair_counts = _pair_counts(pair_event)

    assert any(assertion.byte_hex == "2e" for assertion in byte_assertions)  # decimal point
    assert pair_counts["3."] == 1
    assert pair_counts[".1"] == 1
    assert pair_counts["59"] == 1
    assert all(count == 1 for count in pair_counts.values())
    assert "pi" not in str(byte_event.payload).lower()
    assert "pi" not in str(pair_event.payload).lower()


def test_a_longer_prefix_is_new_material_and_does_not_rewrite_the_shorter_one():
    ledger = EventLedger()
    _supply(ledger, "short-source", SHORT)
    short_bytes, short_pairs = _observe(ledger, "short-source", "short")
    short_payload = short_bytes.model_copy(deep=True).payload
    short_pair_counts = _pair_counts(short_pairs)

    _supply(ledger, "long-source", LONG)
    long_bytes, long_pairs = _observe(ledger, "long-source", "long")

    short_source = assertions_of_recorded_byte_measurement(ledger, short_bytes.id)[0]
    long_source = assertions_of_recorded_byte_measurement(ledger, long_bytes.id)[0]
    assert short_source.assertion_id != long_source.assertion_id
    assert short_bytes.payload == short_payload
    assert _pair_counts(short_pairs) == short_pair_counts
    assert _pair_counts(long_pairs)["10"] == 1
    assert long_pairs.payload["completeness_boundary"] != short_pairs.payload[
        "completeness_boundary"
    ]
