"""A finite decimal representation attributed to pi, measured only as bytes."""

from copy import deepcopy
from tests.binary_input import binary_input
from io import StringIO

from seed_runtime.byte_measurement import (
    assertions_of_recorded_byte_measurement,
    record_byte_position_pair_count_layer,
    record_byte_count_layer,
)
from seed_runtime.events import EventLedger
from seed_runtime.operator_console import run_persistent_operator_console


SHORT = "3.14159265358979323846"
LONG = SHORT + "264338327950288419716939937510"


def _supply(ledger: EventLedger, locality: str, material: str) -> None:
    run_persistent_operator_console(
        ledger=ledger,
        locality_identity=locality,
        input_stream=binary_input(material + "\n"),
        output_stream=StringIO(),
    )


def _measure(ledger: EventLedger, source: str, result: str):
    byte_event = record_byte_count_layer(
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
        bytes(assertion["assertion_subject"]["representation"]).decode("ascii"):
        assertion["dimensions"]["content"]["count"]
        for assertion in event.material["assertions"]
        if assertion["result"] == "count"
    }


def test_seed_measures_one_bounded_decimal_representation_not_all_of_pi():
    ledger = EventLedger()
    _supply(ledger, "short-source", SHORT)
    byte_event, pair_event = _measure(ledger, "short-source", "short")

    byte_assertions = assertions_of_recorded_byte_measurement(ledger, byte_event.identity)
    pair_counts = _pair_counts(pair_event)

    assert any(assertion.representation == 46 for assertion in byte_assertions)
    assert pair_counts["3."] == 1
    assert pair_counts[".1"] == 1
    assert pair_counts["59"] == 1
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

    short_source = assertions_of_recorded_byte_measurement(ledger, short_bytes.identity)[0]
    long_source = assertions_of_recorded_byte_measurement(ledger, long_bytes.identity)[0]
    assert short_source.assertion_identity != long_source.assertion_identity
    assert short_bytes.material == short_material
    assert _pair_counts(short_pairs) == short_pair_counts
    assert _pair_counts(long_pairs)["10"] == 1
    assert long_pairs.material["completeness_boundary"] != short_pairs.material[
        "completeness_boundary"
    ]
