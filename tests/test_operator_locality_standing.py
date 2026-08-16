from copy import deepcopy
from tests.binary_input import binary_input
from io import StringIO

import pytest

from seed_runtime.byte_measurement import (
    BYTE_MEASUREMENT_RECORDED_KIND,
    ByteMeasurementError,
)
from seed_runtime.events import CORRUPTED, EventLedger
from seed_runtime.occurrence_position_measurement import (
    OCCURRENCE_POSITION_RECORDED_KIND,
)
from seed_runtime.operator_ingest import run_operator_ingest
from seed_runtime.operator_material_boundary import operator_boundary_material
from seed_runtime.operator_console import run_persistent_operator_console
from seed_runtime.operator_locality_standing import read_operator_locality_standing


def _attempt(ledger, text, *, locality="s", locality_standing=None):
    return run_operator_ingest(
        ledger=ledger,
        locality_identity=locality,
        boundary_material=operator_boundary_material(binary_input(text)),
        locality_standing=locality_standing,
    )


def _standing(ledger, *, locality="s"):
    return read_operator_locality_standing(
        ledger, locality_identity=locality
    )


def test_events_from_different_localities_cannot_influence_one_another():
    ledger = EventLedger()
    first = _attempt(ledger, "first locality material\n", locality="s1")
    second = _attempt(ledger, "second locality material\n", locality="s2")

    standing_one = _standing(ledger, locality="s1")
    standing_two = _standing(ledger, locality="s2")

    assert standing_one["locality_identity"] == "s1"
    assert standing_two["locality_identity"] == "s2"
    one_subjects = {
        occurrence["subject_reference"]
        for occurrence in standing_one["ingest_occurrences"]
    }
    two_subjects = {
        occurrence["subject_reference"]
        for occurrence in standing_two["ingest_occurrences"]
    }
    assert one_subjects == {first["current_standing"]["ingest_occurrence"]["subject_reference"]}
    assert two_subjects == {second["current_standing"]["ingest_occurrence"]["subject_reference"]}
    assert not {
        occurrence["evidence_event_identity"]
        for occurrence in standing_one["ingest_occurrences"]
    } & {
        occurrence["evidence_event_identity"]
        for occurrence in standing_two["ingest_occurrences"]
    }


@pytest.mark.parametrize(
    ("measurement_kind", "error_type"),
    (
        (BYTE_MEASUREMENT_RECORDED_KIND, ByteMeasurementError),
        (OCCURRENCE_POSITION_RECORDED_KIND, ValueError),
    ),
)
def test_locality_standing_refuses_a_corrupted_measurement(
    monkeypatch, measurement_kind, error_type
):
    ledger = EventLedger()
    run_persistent_operator_console(
        ledger=ledger,
        locality_identity="s",
        input_stream=binary_input("material\n"),
        output_stream=StringIO(),
    )
    measurement = next(
        event for event in ledger.list() if event.kind == measurement_kind
    )
    integrity_of = ledger.integrity_of
    monkeypatch.setattr(
        ledger,
        "integrity_of",
        lambda identity: (
            CORRUPTED
            if identity == measurement.identity
            else integrity_of(identity)
        ),
    )

    with pytest.raises(error_type, match="corrupted"):
        _standing(ledger)


def test_next_attempt_reads_standing_from_earlier_same_locality_events():
    ledger = EventLedger()
    first = _attempt(ledger, "earlier material\n")

    standing = _standing(ledger)
    second = _attempt(ledger, "later material\n", locality_standing=standing)

    assert second["locality_standing"] is standing
    inherited = second["locality_standing"]["ingest_occurrences"]
    assert [occurrence["subject_reference"] for occurrence in inherited] == [
        first["current_standing"]["ingest_occurrence"]["subject_reference"]
    ]
    assert first["current_standing"]["ingest_occurrence"]["subject_reference"] == (
        inherited[0]["subject_reference"]
    )


def test_representation_is_deterministic_regardless_of_unrelated_ledger_events():
    ledger = EventLedger()
    _attempt(ledger, "locality material\n")
    before = _standing(ledger)

    ledger.append("unrelated.kind", {"noise": True}, locality_identity="s")
    ledger.append("unrelated.kind", {}, locality_identity="elsewhere")
    _attempt(ledger, "other locality material\n", locality="elsewhere")
    after = _standing(ledger)

    assert after == before
    assert _standing(ledger) == after


def test_unknown_conflict_and_absence_remain_distinct():
    ledger = EventLedger()
    _attempt(ledger, "material\n")

    standing = _standing(ledger)

    # Unknowns are only what locality events positively carry.
    assert standing["unknowns"] == [
        "the asserted source relation remains Unknown",
        "what this material represents remains Unknown",
    ]
    # No locality event records a conflict or a relation standing; both stay
    # empty rather than being promoted to Unknown or to a negative Assertion.
    assert standing["conflicts"] == []
    assert standing["recorded_relation_standings"] == []
    next_attempt = _attempt(ledger, "next\n", locality_standing=standing)
    assert next_attempt["locality_standing"]["recorded_relation_standings"] == []


def test_one_attempt_behavior_unchanged_without_earlier_locality_history():
    baseline_ledger = EventLedger()
    baseline = _attempt(baseline_ledger, "solo material\n")
    assert "locality_standing" not in baseline

    # The console passes Standing containing C0 to the first interaction,
    # and its interaction output is a bounded Representation, not the Representation.
    input_stream = binary_input("solo material\n")
    output_stream = StringIO()
    console_ledger = EventLedger()
    run_persistent_operator_console(
        ledger=console_ledger,
        locality_identity="s",
        input_stream=input_stream,
        output_stream=output_stream,
    )
    emitted = output_stream.getvalue()
    assert "Bounded Representation" in emitted
    assert "Locality Standing" not in emitted


def test_console_supplies_prior_locality_standing_to_later_interactions():
    input_stream = binary_input("first material\nsecond material\n")
    output_stream = StringIO()
    ledger = EventLedger()

    run_persistent_operator_console(
        ledger=ledger,
        locality_identity="s",
        input_stream=input_stream,
        output_stream=output_stream,
    )

    emitted = output_stream.getvalue()
    assert emitted.count("Bounded Representation") == 3
    standing = _standing(ledger)
    assert len(standing["representations"]) == 3
    first_identity, second_identity, third_identity = list(standing["representations"])
    assert list(standing["representations"])[-1] == third_identity
    # The later Representation's recorded representation Act input Standing taken
    # through a strictly later occurrence than the first one's.
    positions = {event.identity: index for index, event in enumerate(ledger.list())}
    first_representation = standing["representations"][first_identity]
    assert first_representation["locality_standing_as_of_event_identity"] is None
    later_boundary = positions[
        standing["representations"][third_identity]["locality_standing_as_of_event_identity"]
    ]
    # The first Representation's own representation Act and emission occurrences fall
    # inside the prefix the later representation Act input.
    assert positions[first_representation["representation_event_identity"]] < later_boundary
    assert positions[first_representation["emitted_event_identity"]] < later_boundary


def test_representation_does_not_mutate_ledger_or_synthesize_events():
    ledger = EventLedger()
    _attempt(ledger, "material\n")
    events_before = deepcopy(ledger.list())

    _standing(ledger)

    assert ledger.list() == events_before
