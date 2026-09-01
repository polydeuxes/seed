"""Source references and exact current coordinates."""

from __future__ import annotations

from io import BytesIO
from types import SimpleNamespace

import pytest


from seed_runtime.events import EventLedger, SQLiteEventLedger
from seed_runtime.material_source import exact_material_result_bytes
from seed_runtime.operator_checkpoint import (
    THROUGH_OCCURRENCE_BOUNDARY_REFERENCE_RECORDED_KIND,
    record_through_occurrence_boundary_reference_act_occurrence,
    record_through_occurrence_boundary_reference_result,
)
from seed_runtime.operator_command import AddressedOperatorCommand, OperatorCommandFrame
from seed_runtime.operator_console import run_persistent_operator_console
from seed_runtime.operator_current_coordinates import (
    CarriedCoordinateReferenceError,
    advance_operator_current_coordinates,
    read_current_coordinates_through_carried_reference,
    read_operator_current_coordinates,
)
from seed_runtime.operator_locality_continuation import (
    LOCALITY_CONTINUATION_RECORDED_KIND,
)
from seed_runtime.recorded_boundary_locality import (
    RECORDED_BOUNDARY_LOCALITY_RECORDED_KIND,
)


@pytest.fixture(autouse=True)
def _skip_unrelated_measurement_work(monkeypatch):
    monkeypatch.setattr(
        "seed_runtime.operator_console._record_declared_measurements_from_carried_current_coordinates",
        lambda _ledger, current_coordinates, *, locality_identity: SimpleNamespace(
            current_coordinates=current_coordinates,
            result_occurrences=(),
        ),
    )


def _run(material: bytes) -> EventLedger:
    ledger = EventLedger()
    run_persistent_operator_console(
        ledger=ledger,
        locality_identity="source",
        input_stream=BytesIO(material),
    )
    return ledger


def _material_results(ledger: EventLedger, current_coordinates: dict) -> list[bytes]:
    return [
        exact_material_result_bytes(ledger.get(occurrence["result_occurrence_identity"]))
        for occurrence in current_coordinates["material_result_occurrences"]
    ]


def test_checkpoint_reads_its_exact_prior_coordinates_after_later_material():
    ledger = _run(b"a\n/checkpoint\nlater\n")
    checkpoint = next(
        event
        for event in ledger.list_locality("source")
        if event.kind == THROUGH_OCCURRENCE_BOUNDARY_REFERENCE_RECORDED_KIND
    )

    reading = read_current_coordinates_through_carried_reference(
        ledger,
        locality_identity="source",
        recorded_occurrence_identity=checkpoint.identity,
    )
    current = read_operator_current_coordinates(ledger, locality_identity="source")

    assert reading["current_coordinates"]["through_event_occurrence_identity"] == reading[
        "source_coordinate_reference"
    ]["source_through_event_occurrence_identity"]
    assert _material_results(ledger, reading["current_coordinates"]) == [
        b"a\n",
        b"/checkpoint\n",
    ]
    assert _material_results(ledger, current) == [
        b"a\n",
        b"/checkpoint\n",
        b"later\n",
    ]
    assert reading["current_coordinates"] is not current


def test_memory_makes_one_prior_boundary_available_without_copying_source_coordinates():
    ledger = _run(b"a\n/memory\nb\n")
    continuation = next(
        event
        for event in ledger.list()
        if event.kind == LOCALITY_CONTINUATION_RECORDED_KIND
    )
    destination = continuation.locality_identity

    reading = read_current_coordinates_through_carried_reference(
        ledger,
        locality_identity=destination,
        recorded_occurrence_identity=continuation.identity,
    )
    destination_coordinates = read_operator_current_coordinates(
        ledger, locality_identity=destination
    )

    assert reading["current_coordinates"]["locality_identity"] == "source"
    assert _material_results(ledger, reading["current_coordinates"]) == [
        b"a\n",
        b"/memory\n",
    ]
    assert _material_results(ledger, destination_coordinates) == [
        b"b\n"
    ]
    assert reading["current_coordinates"]["locality_continuation_relation_occurrences"] == {}
    assert destination_coordinates["locality_continuation_relation_occurrences"] == {
        continuation.identity: None
    }


def test_checkout_resolves_the_checkpoint_cut_not_either_later_branch():
    ledger = _run(
        b"a\n/checkpoint\n/checkout\nc\n"
    )
    relation = next(
        event
        for event in ledger.list()
        if event.kind == RECORDED_BOUNDARY_LOCALITY_RECORDED_KIND
    )

    reading = read_current_coordinates_through_carried_reference(
        ledger,
        locality_identity=relation.locality_identity,
        recorded_occurrence_identity=relation.identity,
    )

    assert reading["current_coordinates"]["locality_identity"] == "source"
    assert _material_results(ledger, reading["current_coordinates"]) == [
        b"a\n",
        b"/checkpoint\n",
    ]
    assert reading["current_coordinates"]["recorded_through_occurrence_boundary_references"] == {}
    assert reading["current_coordinates"]["recorded_boundary_locality_relations"] == {}


def test_an_exact_reference_is_not_globally_available_by_identity():
    ledger = _run(b"a\n/checkpoint\n/checkout\n")
    checkpoint = next(
        event
        for event in ledger.list()
        if event.kind == THROUGH_OCCURRENCE_BOUNDARY_REFERENCE_RECORDED_KIND
    )
    relation = next(
        event
        for event in ledger.list()
        if event.kind == RECORDED_BOUNDARY_LOCALITY_RECORDED_KIND
    )

    with pytest.raises(CarriedCoordinateReferenceError, match="not carried"):
        read_current_coordinates_through_carried_reference(
            ledger,
            locality_identity=relation.locality_identity,
            recorded_occurrence_identity=checkpoint.identity,
        )
    with pytest.raises(CarriedCoordinateReferenceError, match="not carried"):
        read_current_coordinates_through_carried_reference(
            ledger,
            locality_identity="source",
            recorded_occurrence_identity=relation.identity,
        )


def test_unrelated_occurrences_do_not_change_the_recorded_read():
    ledger = _run(b"a\n/checkpoint\n")
    checkpoint = next(
        event
        for event in ledger.list()
        if event.kind == THROUGH_OCCURRENCE_BOUNDARY_REFERENCE_RECORDED_KIND
    )
    before = read_current_coordinates_through_carried_reference(
        ledger,
        locality_identity="source",
        recorded_occurrence_identity=checkpoint.identity,
    )
    ledger.append("unrelated", locality_identity="other")
    after = read_current_coordinates_through_carried_reference(
        ledger,
        locality_identity="source",
        recorded_occurrence_identity=checkpoint.identity,
    )

    assert after == before


def test_coordinate_reference_is_resolved_after_durable_reopen(tmp_path):
    path = tmp_path / "carried-coordinates.sqlite"
    ledger = SQLiteEventLedger(str(path))
    run_persistent_operator_console(
        ledger=ledger,
        locality_identity="source",
        input_stream=BytesIO(b"a\n/checkpoint\n"),
    )
    checkpoint = next(
        event
        for event in ledger.list_locality("source")
        if event.kind == THROUGH_OCCURRENCE_BOUNDARY_REFERENCE_RECORDED_KIND
    )
    checkpoint_identity = checkpoint.identity
    ledger.close()

    reopened = SQLiteEventLedger(str(path))
    try:
        reading = read_current_coordinates_through_carried_reference(
            reopened,
            locality_identity="source",
            recorded_occurrence_identity=checkpoint_identity,
        )
        assert _material_results(reopened, reading["current_coordinates"]) == [
            b"a\n",
            b"/checkpoint\n",
        ]
    finally:
        reopened.close()
