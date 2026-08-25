"""Recorded prior Standing remains addressable without entering another Locality."""

from __future__ import annotations

from io import BytesIO

import pytest


from seed_runtime.events import EventLedger, SQLiteEventLedger
from seed_runtime.material_source import exact_material_result_bytes
from seed_runtime.witness_material_source import WITNESS_MATERIAL_SOURCE_RECORDED_KIND
from seed_runtime.operator_checkpoint import (
    STANDING_BOUNDARY_REFERENCE_RECORDED_KIND,
    record_standing_boundary_reference_responsibility_assignment,
    record_standing_boundary_reference_act_occurrence,
    record_standing_boundary_reference_result,
)
from seed_runtime.operator_command import AddressedOperatorCommand, OperatorCommandFrame
from seed_runtime.operator_console import run_persistent_operator_console
from seed_runtime.operator_locality_standing import (
    CarriedRecordedStandingError,
    advance_operator_locality_standing,
    read_carried_recorded_standing,
    read_operator_locality_standing,
)
from seed_runtime.operator_standing_continuation import (
    STANDING_LOCALITY_CONTINUATION_RECORDED_KIND,
)
from seed_runtime.standing_boundary_locality import (
    RECORDED_STANDING_BOUNDARY_LOCALITY_RECORDED_KIND,
)


@pytest.fixture(autouse=True)
def _skip_unrelated_measurement_work(monkeypatch):
    class _AlreadyMeasured(set):
        def __contains__(self, _item):
            return True

    monkeypatch.setattr(
        "seed_runtime.operator_console._recorded_byte_measurement_material_references",
        lambda _ledger: _AlreadyMeasured(),
    )


def _run(material: bytes) -> EventLedger:
    ledger = EventLedger()
    run_persistent_operator_console(
        ledger=ledger,
        locality_identity="source",
        input_stream=BytesIO(material),
    )
    return ledger


def _acquired_materials(ledger: EventLedger, standing: dict) -> list[bytes]:
    return [
        exact_material_result_bytes(ledger.get(occurrence["result_occurrence_identity"]))
        for occurrence in standing["material_acquisition_result_occurrences"]
    ]


def test_checkpoint_reads_its_exact_prior_coordinates_after_later_material():
    ledger = _run(b"a\n/checkpoint\nlater\n")
    checkpoint = next(
        event
        for event in ledger.list_locality("source")
        if event.kind == STANDING_BOUNDARY_REFERENCE_RECORDED_KIND
    )

    reading = read_carried_recorded_standing(
        ledger,
        locality_identity="source",
        recorded_occurrence_identity=checkpoint.identity,
    )
    current = read_operator_locality_standing(ledger, locality_identity="source")

    assert reading["standing"]["through_event_occurrence_identity"] == reading[
        "source_standing_reference"
    ]["source_standing_through_event_occurrence_identity"]
    assert _acquired_materials(ledger, reading["standing"]) == [
        b"a\n",
        b"/checkpoint\n",
    ]
    assert _acquired_materials(ledger, current) == [
        b"a\n",
        b"/checkpoint\n",
        b"later\n",
    ]
    assert reading["standing"] is not current


def test_memory_makes_one_prior_boundary_available_without_copying_its_standing():
    ledger = _run(b"a\n/memory\nb\n")
    continuation = next(
        event
        for event in ledger.list()
        if event.kind == STANDING_LOCALITY_CONTINUATION_RECORDED_KIND
    )
    destination = continuation.locality_identity

    reading = read_carried_recorded_standing(
        ledger,
        locality_identity=destination,
        recorded_occurrence_identity=continuation.identity,
    )
    destination_standing = read_operator_locality_standing(
        ledger, locality_identity=destination
    )

    assert reading["standing"]["locality_identity"] == "source"
    assert _acquired_materials(ledger, reading["standing"]) == [
        b"a\n",
        b"/memory\n",
    ]
    assert _acquired_materials(ledger, destination_standing) == [
        b"b\n"
    ]
    assert reading["standing"]["recorded_relation_Standing"] == {}
    assert destination_standing["recorded_relation_Standing"] == {
        continuation.identity: None
    }


def test_checkout_resolves_the_checkpoint_cut_not_either_later_branch():
    ledger = _run(
        b"a\n/checkpoint\n/checkout\nc\n"
    )
    relation = next(
        event
        for event in ledger.list()
        if event.kind == RECORDED_STANDING_BOUNDARY_LOCALITY_RECORDED_KIND
    )

    reading = read_carried_recorded_standing(
        ledger,
        locality_identity=relation.locality_identity,
        recorded_occurrence_identity=relation.identity,
    )

    assert reading["standing"]["locality_identity"] == "source"
    assert _acquired_materials(ledger, reading["standing"]) == [
        b"a\n",
        b"/checkpoint\n",
    ]
    assert reading["standing"]["recorded_standing_boundary_references"] == {}
    assert reading["standing"]["recorded_standing_boundary_locality_relations"] == {}


def test_an_exact_reference_is_not_globally_available_by_identity():
    ledger = _run(b"a\n/checkpoint\n/checkout\n")
    checkpoint = next(
        event
        for event in ledger.list()
        if event.kind == STANDING_BOUNDARY_REFERENCE_RECORDED_KIND
    )
    relation = next(
        event
        for event in ledger.list()
        if event.kind == RECORDED_STANDING_BOUNDARY_LOCALITY_RECORDED_KIND
    )

    with pytest.raises(CarriedRecordedStandingError, match="not carried"):
        read_carried_recorded_standing(
            ledger,
            locality_identity=relation.locality_identity,
            recorded_occurrence_identity=checkpoint.identity,
        )
    with pytest.raises(CarriedRecordedStandingError, match="not carried"):
        read_carried_recorded_standing(
            ledger,
            locality_identity="source",
            recorded_occurrence_identity=relation.identity,
        )


def test_the_read_adds_no_applicability_admission_or_compare_coordinate():
    ledger = _run(b"a\n/checkpoint\n")
    checkpoint = next(
        event
        for event in ledger.list()
        if event.kind == STANDING_BOUNDARY_REFERENCE_RECORDED_KIND
    )

    reading = read_carried_recorded_standing(
        ledger,
        locality_identity="source",
        recorded_occurrence_identity=checkpoint.identity,
    )

    assert not {"applicability", "admission", "participation", "compare"}.intersection(
        reading
    )
    assert not {"applicability", "admission", "participation", "compare"}.intersection(
        reading["standing"]
    )


def test_unrelated_occurrences_do_not_change_the_recorded_read():
    ledger = _run(b"a\n/checkpoint\n")
    checkpoint = next(
        event
        for event in ledger.list()
        if event.kind == STANDING_BOUNDARY_REFERENCE_RECORDED_KIND
    )
    before = read_carried_recorded_standing(
        ledger,
        locality_identity="source",
        recorded_occurrence_identity=checkpoint.identity,
    )
    ledger.append("unrelated", locality_identity="other")
    after = read_carried_recorded_standing(
        ledger,
        locality_identity="source",
        recorded_occurrence_identity=checkpoint.identity,
    )

    assert after == before
    assert not [
        event
        for event in ledger.list_locality("other")
        if event.kind == WITNESS_MATERIAL_SOURCE_RECORDED_KIND
    ]


def test_recorded_standing_reference_is_recovered_after_durable_reopen(tmp_path):
    path = tmp_path / "recorded-standing.sqlite"
    ledger = SQLiteEventLedger(str(path))
    run_persistent_operator_console(
        ledger=ledger,
        locality_identity="source",
        input_stream=BytesIO(b"a\n/checkpoint\n"),
    )
    checkpoint = next(
        event
        for event in ledger.list_locality("source")
        if event.kind == STANDING_BOUNDARY_REFERENCE_RECORDED_KIND
    )
    checkpoint_identity = checkpoint.identity
    ledger.close()

    reopened = SQLiteEventLedger(str(path))
    try:
        reading = read_carried_recorded_standing(
            reopened,
            locality_identity="source",
            recorded_occurrence_identity=checkpoint_identity,
        )
        assert _acquired_materials(reopened, reading["standing"]) == [
            b"a\n",
            b"/checkpoint\n",
        ]
    finally:
        reopened.close()
