from copy import deepcopy
from tests.binary_input import binary_input
from io import StringIO

import pytest

from seed_runtime.byte_measurement import (
    BYTE_MEASUREMENT_RECORDED_KIND,
    BYTE_PAIR_MEASUREMENT_RECORDED_KIND,
    ByteMeasurementError,
    record_byte_measurement_responsible_act_evidence,
    record_byte_measurement_result,
    record_byte_position_pair_count_layer,
)
from seed_runtime.events import CORRUPTED, EventLedger
from seed_runtime.material_ingest import ingest_material
from seed_runtime.occurrence_position_measurement import (
    OCCURRENCE_POSITION_RECORDED_KIND,
    measure_occurrence_position,
    record_occurrence_position_measurement_responsible_act_evidence,
    record_occurrence_position_measurement_result,
)
from seed_runtime.operator_ingest import run_operator_ingest
from seed_runtime.operator_material_boundary import operator_boundary_material
from seed_runtime.operator_console import run_persistent_operator_console
from seed_runtime.operator_locality_standing import (
    advance_operator_locality_standing,
    read_operator_locality_standing,
)


class DictSubclass(dict):
    pass


def _record_byte_measurement(
    ledger, *, source_localities, recording_locality_identity
):
    act_evidence = record_byte_measurement_responsible_act_evidence(
        ledger,
        source_localities=source_localities,
        recording_locality_identity=recording_locality_identity,
    )
    return record_byte_measurement_result(
        ledger,
        responsible_act_evidence_event_identity=act_evidence.identity,
    )


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


def _record_measurement(ledger, measurement_kind):
    if measurement_kind == BYTE_MEASUREMENT_RECORDED_KIND:
        return _record_byte_measurement(
            ledger,
            source_localities=("s",),
            recording_locality_identity="s",
        )
    if measurement_kind == BYTE_PAIR_MEASUREMENT_RECORDED_KIND:
        byte = _record_byte_measurement(
            ledger,
            source_localities=("s",),
            recording_locality_identity="s",
        )
        return record_byte_position_pair_count_layer(
            ledger,
            source_measurement_event_identity=byte.identity,
            recording_locality_identity="s",
        )
    finding = measure_occurrence_position(
        ledger,
        source_locality_identity="s",
    )
    act_evidence = record_occurrence_position_measurement_responsible_act_evidence(
        ledger,
        recording_locality_identity="s",
        finding=finding,
    )
    return record_occurrence_position_measurement_result(
        ledger,
        finding=finding,
        responsible_act_evidence_event_identity=act_evidence.identity,
    )


def _measurement_ledger():
    ledger = EventLedger()
    ingest_material(
        ledger,
        locality_identity="s",
        exact_bytes=b"material",
        source_role="operator",
        source_boundary="test boundary",
    )
    return ledger


def _measurement_coordinates(event):
    return {
        "recorded_occurrence_identity": event.identity,
        "result_identity": event.material["result_identity"],
        "act_occurrence_identity": event.material["act_occurrence_identity"],
        "responsible_act_evidence_identity": event.material[
            "responsible_act_evidence_identity"
        ],
        "evidence_of_yield_relation_identity": event.material["evidence_of_yield_relation_identity"],
    }


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


def test_locality_standing_carries_exact_measurement_identities_in_append_order():
    ledger = _measurement_ledger()
    byte = _record_measurement(ledger, BYTE_MEASUREMENT_RECORDED_KIND)
    pair = record_byte_position_pair_count_layer(
        ledger,
        source_measurement_event_identity=byte.identity,
        recording_locality_identity="s",
    )
    positions = _record_measurement(ledger, OCCURRENCE_POSITION_RECORDED_KIND)

    standing = _standing(ledger)

    assert type(standing["measurement_occurrences"]) is dict
    assert standing["measurement_occurrences"] == {
        byte.identity: _measurement_coordinates(byte),
        pair.identity: _measurement_coordinates(pair),
        positions.identity: _measurement_coordinates(positions),
    }
    assert list(standing["measurement_occurrences"]) == [
        byte.identity,
        pair.identity,
        positions.identity,
    ]
    assert all(
        set(occurrence)
        == {
            "recorded_occurrence_identity",
            "result_identity",
            "act_occurrence_identity",
            "responsible_act_evidence_identity",
            "evidence_of_yield_relation_identity",
        }
        for occurrence in standing["measurement_occurrences"].values()
    )
    assert "assertions" not in str(standing["measurement_occurrences"])
    assert "occurrences" not in {
        key
        for occurrence in standing["measurement_occurrences"].values()
        for key in occurrence
    }
    assert all(
        type(identity) is str
        and type(reference) is dict
        and reference["recorded_occurrence_identity"] == identity
        for identity, reference in standing["measurement_occurrences"].items()
    )


def test_locality_standing_carries_no_measurement_without_a_recorded_result():
    ledger = _measurement_ledger()

    assert _standing(ledger)["measurement_occurrences"] == {}


@pytest.mark.parametrize("carrier", ([], DictSubclass()))
def test_advance_refuses_a_nonexact_prior_measurement_accumulator(carrier):
    ledger = _measurement_ledger()
    standing = _standing(ledger)
    standing["measurement_occurrences"] = carrier

    with pytest.raises(ValueError, match="exact Measurement occurrences"):
        advance_operator_locality_standing(
            ledger,
            (),
            locality_identity="s",
            prior=standing,
        )


def test_locality_standing_carries_only_exact_yielded_result_identities():
    ledger = EventLedger()
    source = ingest_material(
        ledger,
        locality_identity="s",
        exact_bytes=b"raw result",
        source_role="operator",
        source_boundary="test boundary",
    )
    measurement = _record_byte_measurement(
        ledger,
        source_localities=("s",),
        recording_locality_identity="s",
    )

    standing = _standing(ledger)

    assert standing["exact_result_occurrences"] == {source.identity: None}
    assert all(
        type(identity) is str for identity in standing["exact_result_occurrences"]
    )
    assert measurement.identity not in standing["exact_result_occurrences"]


def test_locality_standing_refuses_raw_result_with_missing_or_crossed_yield():
    ledger = EventLedger()
    source = ingest_material(
        ledger,
        locality_identity="s",
        exact_bytes=b"raw result",
        source_role="operator",
        source_boundary="test boundary",
    )
    other = ingest_material(
        ledger,
        locality_identity="s",
        exact_bytes=b"other result",
        source_role="operator",
        source_boundary="test boundary",
    )
    source.material["evidence_of_yield_relation_identity"] = other.material[
        "evidence_of_yield_relation_identity"
    ]

    standing = _standing(ledger)

    assert source.identity not in standing["exact_result_occurrences"]
    assert standing["exact_result_occurrences"] == {other.identity: None}


def test_locality_standing_refuses_corrupted_raw_result(monkeypatch):
    ledger = EventLedger()
    source = ingest_material(
        ledger,
        locality_identity="s",
        exact_bytes=b"raw result",
        source_role="operator",
        source_boundary="test boundary",
    )
    integrity_of = ledger.integrity_of
    monkeypatch.setattr(
        ledger,
        "integrity_of",
        lambda identity: (
            CORRUPTED if identity == source.identity else integrity_of(identity)
        ),
    )

    assert _standing(ledger)["exact_result_occurrences"] == {}


@pytest.mark.parametrize(
    "evidence_coordinate",
    ("responsible_act_evidence_identity", "evidence_of_yield_relation_identity"),
)
def test_locality_standing_refuses_corrupted_raw_evidence_of_yield_relation(
    monkeypatch, evidence_coordinate
):
    ledger = EventLedger()
    source = ingest_material(
        ledger,
        locality_identity="s",
        exact_bytes=b"raw result",
        source_role="operator",
        source_boundary="test boundary",
    )
    corrupted_identity = source.material[evidence_coordinate]
    integrity_of = ledger.integrity_of
    monkeypatch.setattr(
        ledger,
        "integrity_of",
        lambda identity: (
            CORRUPTED if identity == corrupted_identity else integrity_of(identity)
        ),
    )

    assert _standing(ledger)["exact_result_occurrences"] == {}


@pytest.mark.parametrize(
    ("measurement_kind", "error_type"),
    (
        (BYTE_MEASUREMENT_RECORDED_KIND, ByteMeasurementError),
        (BYTE_PAIR_MEASUREMENT_RECORDED_KIND, ByteMeasurementError),
        (OCCURRENCE_POSITION_RECORDED_KIND, ValueError),
    ),
)
def test_locality_standing_refuses_a_corrupted_measurement(
    monkeypatch, measurement_kind, error_type
):
    ledger = EventLedger()
    ingest_material(
        ledger,
        locality_identity="s",
        exact_bytes=b"material",
        source_role="operator",
        source_boundary="test boundary",
    )
    measurement = _record_measurement(ledger, measurement_kind)
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


@pytest.mark.parametrize(
    ("measurement_kind", "error_type"),
    (
        (BYTE_MEASUREMENT_RECORDED_KIND, ByteMeasurementError),
        (BYTE_PAIR_MEASUREMENT_RECORDED_KIND, ByteMeasurementError),
        (OCCURRENCE_POSITION_RECORDED_KIND, ValueError),
    ),
)
def test_locality_standing_refuses_measurement_with_missing_yield(
    measurement_kind, error_type
):
    ledger = _measurement_ledger()
    measurement = _record_measurement(ledger, measurement_kind)
    measurement.material["evidence_of_yield_relation_identity"] = None

    with pytest.raises(error_type, match="Yield|yield"):
        _standing(ledger)


@pytest.mark.parametrize(
    ("measurement_kind", "error_type"),
    (
        (BYTE_MEASUREMENT_RECORDED_KIND, ByteMeasurementError),
        (BYTE_PAIR_MEASUREMENT_RECORDED_KIND, ByteMeasurementError),
        (OCCURRENCE_POSITION_RECORDED_KIND, ValueError),
    ),
)
def test_locality_standing_refuses_yield_from_another_measurement_occurrence(
    measurement_kind, error_type
):
    ledger = _measurement_ledger()
    measurement = _record_measurement(ledger, measurement_kind)
    other = _record_measurement(ledger, measurement_kind)
    measurement.material["evidence_of_yield_relation_identity"] = other.material[
        "evidence_of_yield_relation_identity"
    ]

    with pytest.raises(error_type, match="Yield|yield"):
        _standing(ledger)


@pytest.mark.parametrize(
    ("measurement_kind", "error_type"),
    (
        (BYTE_MEASUREMENT_RECORDED_KIND, ByteMeasurementError),
        (BYTE_PAIR_MEASUREMENT_RECORDED_KIND, ByteMeasurementError),
        (OCCURRENCE_POSITION_RECORDED_KIND, ValueError),
    ),
)
def test_locality_standing_refuses_corrupted_measurement_yield(
    monkeypatch, measurement_kind, error_type
):
    ledger = _measurement_ledger()
    measurement = _record_measurement(ledger, measurement_kind)
    yield_identity = measurement.material["evidence_of_yield_relation_identity"]
    integrity_of = ledger.integrity_of
    monkeypatch.setattr(
        ledger,
        "integrity_of",
        lambda identity: (
            CORRUPTED if identity == yield_identity else integrity_of(identity)
        ),
    )

    with pytest.raises(error_type, match="Yield|yield"):
        _standing(ledger)


@pytest.mark.parametrize(
    "measurement_kind",
    (
        BYTE_MEASUREMENT_RECORDED_KIND,
        BYTE_PAIR_MEASUREMENT_RECORDED_KIND,
        OCCURRENCE_POSITION_RECORDED_KIND,
    ),
)
def test_unrelated_event_cannot_enter_measurement_occurrences(measurement_kind):
    ledger = _measurement_ledger()
    measurement = _record_measurement(ledger, measurement_kind)
    before = _standing(ledger)
    unrelated = ledger.append(
        "unrelated.measurement",
        deepcopy(measurement.material),
        locality_identity="s",
    )

    after = _standing(ledger)

    assert after == before
    assert unrelated.identity not in after["measurement_occurrences"]


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
    assert standing["unknowns"] == ["represented_relation", "source_relation"]
    # No locality event records a conflict or a relation standing; both stay
    # empty rather than being promoted to Unknown or to a negative Assertion.
    assert standing["conflicts"] == []
    assert standing["recorded_relation_standings"] == {}
    next_attempt = _attempt(ledger, "next\n", locality_standing=standing)
    assert next_attempt["locality_standing"]["recorded_relation_standings"] == {}


def test_one_attempt_records_only_responsible_representation_results():
    baseline_ledger = EventLedger()
    baseline = _attempt(baseline_ledger, "solo material\n")
    assert "locality_standing" not in baseline

    # The console passes Standing containing C0 to the first interaction and
    # does not manufacture outward material for the generic Representation.
    input_stream = binary_input("solo material\n")
    output_stream = StringIO()
    console_ledger = EventLedger()
    run_persistent_operator_console(
        ledger=console_ledger,
        locality_identity="s",
        input_stream=input_stream,
        output_stream=output_stream,
    )
    assert output_stream.getvalue() == ""
    assert len(_standing(console_ledger)["representations"]) == 3


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

    assert output_stream.getvalue() == ""
    standing = _standing(ledger)
    assert len(standing["representations"]) == 5
    representation_identities = list(standing["representations"])
    first_identity = representation_identities[0]
    last_identity = representation_identities[-1]
    # The later Representation's recorded representation Act input Standing taken
    # through a strictly later occurrence than the first one's.
    positions = {event.identity: index for index, event in enumerate(ledger.list())}
    first_representation = standing["representations"][first_identity]
    assert first_representation["locality_standing_as_of_event_identity"] is None
    later_boundary = positions[
        standing["representations"][last_identity]["locality_standing_as_of_event_identity"]
    ]
    # The first Representation Act falls inside the prefix the later Act input.
    assert positions[first_representation["representation_event_identity"]] < later_boundary
    assert first_representation["emitted_event_identity"] is None


def test_representation_does_not_mutate_ledger_or_synthesize_events():
    ledger = EventLedger()
    _attempt(ledger, "material\n")
    events_before = deepcopy(ledger.list())

    _standing(ledger)

    assert ledger.list() == events_before
