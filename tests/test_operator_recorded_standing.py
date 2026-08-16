"""Recorded prior Standing remains addressable without entering another Locality."""

from __future__ import annotations

from io import BytesIO, StringIO

import pytest

from seed_runtime.events import EventLedger, SQLiteEventLedger
from seed_runtime.material_ingest import (
    MATERIAL_INGEST_OCCURRED_KIND,
    ingested_material_bytes,
)
from seed_runtime.operator_checkpoint import (
    STANDING_BOUNDARY_REFERENCE_RECORDED_KIND,
    record_standing_boundary_reference_responsibility_assignment,
    record_standing_boundary_reference_responsible_act_evidence,
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
from seed_runtime.operator_representation import record_operator_representation
from seed_runtime.operator_standing_continuation import (
    STANDING_LOCALITY_CONTINUATION_RECORDED_KIND,
)
from seed_runtime.standing_boundary_locality import (
    RECORDED_STANDING_BOUNDARY_LOCALITY_RECORDED_KIND,
)


def _run(material: bytes) -> EventLedger:
    ledger = EventLedger()
    run_persistent_operator_console(
        ledger=ledger,
        locality_identity="source",
        input_stream=BytesIO(material),
        output_stream=StringIO(),
    )
    return ledger


def _ingested_materials(ledger: EventLedger, standing: dict) -> list[bytes]:
    return [
        ingested_material_bytes(ledger.get(occurrence["evidence_event_identity"]))
        for occurrence in standing["ingest_occurrences"]
    ]


def test_checkpoint_reads_its_exact_prior_standing_without_returning_to_it():
    ledger = _run(b"book material\n/checkpoint\nlater source material\n")
    checkpoint = next(
        event
        for event in ledger.list_locality("source")
        if event.kind == STANDING_BOUNDARY_REFERENCE_RECORDED_KIND
    )

    point = read_carried_recorded_standing(
        ledger,
        locality_identity="source",
        recorded_occurrence_identity=checkpoint.identity,
    )
    current = read_operator_locality_standing(ledger, locality_identity="source")

    assert point["standing"]["as_of_event_identity"] == point[
        "source_standing_reference"
    ]["source_standing_as_of_event_identity"]
    assert _ingested_materials(ledger, point["standing"]) == [b"book material\n"]
    assert _ingested_materials(ledger, current) == [
        b"book material\n",
        b"later source material\n",
    ]
    assert point["standing"] is not current


def test_memory_makes_one_prior_boundary_available_without_copying_its_standing():
    ledger = _run(b"book material\n/memory\ndestination material\n")
    continuation = next(
        event
        for event in ledger.list()
        if event.kind == STANDING_LOCALITY_CONTINUATION_RECORDED_KIND
    )
    destination = continuation.locality_identity

    point = read_carried_recorded_standing(
        ledger,
        locality_identity=destination,
        recorded_occurrence_identity=continuation.identity,
    )
    destination_standing = read_operator_locality_standing(
        ledger, locality_identity=destination
    )

    assert point["standing"]["locality_identity"] == "source"
    assert _ingested_materials(ledger, point["standing"]) == [b"book material\n"]
    assert _ingested_materials(ledger, destination_standing) == [
        b"destination material\n"
    ]
    assert point["standing"]["recorded_relation_standings"] == {}
    assert destination_standing["recorded_relation_standings"] == {
        continuation.identity: None
    }


def test_checkout_resolves_the_checkpoint_cut_not_either_later_branch():
    ledger = _run(
        b"book material\n/checkpoint\nlater source material\n"
        b"/checkout\ndestination material\n"
    )
    relation = next(
        event
        for event in ledger.list()
        if event.kind == RECORDED_STANDING_BOUNDARY_LOCALITY_RECORDED_KIND
    )

    point = read_carried_recorded_standing(
        ledger,
        locality_identity=relation.locality_identity,
        recorded_occurrence_identity=relation.identity,
    )

    assert point["standing"]["locality_identity"] == "source"
    assert _ingested_materials(ledger, point["standing"]) == [b"book material\n"]
    assert point["standing"]["recorded_standing_boundary_references"] == {}
    assert point["standing"]["recorded_standing_boundary_locality_relations"] == {}


def test_an_exact_reference_is_not_globally_available_by_identity():
    ledger = _run(b"book material\n/checkpoint\n/checkout\n")
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


def test_empty_recorded_boundary_reads_exactly_empty_standing():
    ledger = EventLedger()
    standing = read_operator_locality_standing(ledger, locality_identity="source")
    representation = record_operator_representation(
        ledger, locality_identity="source", locality_standing=standing
    )
    standing = advance_operator_locality_standing(
        ledger,
        representation["recorded_occurrence_references"],
        locality_identity="source",
        prior=standing,
    )
    command = AddressedOperatorCommand(
        command_identity="command",
        locality_identity="source",
        addressed_at_representation_event_identity=representation[
            "representation_event_identity"
        ],
        frame=OperatorCommandFrame(
            exact_bytes=b"/checkpoint\n", name=b"checkpoint", arguments=b""
        ),
    )
    assignment = record_standing_boundary_reference_responsibility_assignment(
        ledger, addressed_command=command, locality_standing=standing
    )
    act = record_standing_boundary_reference_responsible_act_evidence(
        ledger,
        responsibility_assignment_event_identity=assignment.identity,
        responsibility_assignment_standing=read_operator_locality_standing(
            ledger, locality_identity="source"
        ),
    )
    checkpoint = record_standing_boundary_reference_result(
        ledger, responsible_act_evidence_event_identity=act.identity
    )

    point = read_carried_recorded_standing(
        ledger,
        locality_identity="source",
        recorded_occurrence_identity=checkpoint.identity,
    )

    assert point["source_standing_reference"][
        "source_standing_as_of_event_identity"
    ] is None
    assert point["standing"]["as_of_event_identity"] is None
    assert point["standing"]["event_count"] == 0


def test_the_read_adds_no_applicability_admission_or_compare_coordinate():
    ledger = _run(b"book material\n/checkpoint\n")
    checkpoint = next(
        event
        for event in ledger.list()
        if event.kind == STANDING_BOUNDARY_REFERENCE_RECORDED_KIND
    )

    point = read_carried_recorded_standing(
        ledger,
        locality_identity="source",
        recorded_occurrence_identity=checkpoint.identity,
    )

    assert not {"applicability", "admission", "participation", "compare"}.intersection(
        point
    )
    assert not {"applicability", "admission", "participation", "compare"}.intersection(
        point["standing"]
    )


def test_unrelated_occurrences_do_not_change_the_recorded_read():
    ledger = _run(b"book material\n/checkpoint\n")
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
        if event.kind == MATERIAL_INGEST_OCCURRED_KIND
    ]


def test_recorded_standing_reference_survives_durable_reopen(tmp_path):
    path = tmp_path / "recorded-standing.sqlite"
    ledger = SQLiteEventLedger(str(path))
    run_persistent_operator_console(
        ledger=ledger,
        locality_identity="source",
        input_stream=BytesIO(b"book material\n/checkpoint\nlater source material\n"),
        output_stream=StringIO(),
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
        point = read_carried_recorded_standing(
            reopened,
            locality_identity="source",
            recorded_occurrence_identity=checkpoint_identity,
        )
        assert _ingested_materials(reopened, point["standing"]) == [
            b"book material\n"
        ]
    finally:
        reopened.close()
