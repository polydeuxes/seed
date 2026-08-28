"""Current coordinates are exact through one occurrence boundary."""

from copy import deepcopy
from tests.binary_input import binary_input

import pytest


import seed_runtime.operator_current_coordinates as operator_standing_module
from seed_runtime.byte_measurement import (
    BYTE_MEASUREMENT_RECORDED_KIND,
    BYTE_PAIR_MEASUREMENT_RECORDED_KIND,
    BYTE_PAIR_APPLICABILITY_ACT_OCCURRENCE_EVENT,
    BYTE_PAIR_APPLICABILITY_RECORDED_KIND,
    BYTE_PAIR_MEASUREMENT_ACT_OCCURRENCE_EVENT,
    ByteMeasurementError,
    result_positions_of_recorded_byte_position_pair_measurement,
    get_byte_position_pair_measurement_subject_to_act_binding,
    record_byte_measurement_subject_to_act_binding,
    record_byte_measurement_act_occurrence,
    record_byte_measurement_result,
    record_byte_position_pair_count_layer,
)
from seed_runtime.events import CORRUPTED, EventLedger, SQLiteEventLedger
from seed_runtime.witness_material_source import record_witness_material_source
from tests.operator_material_source_test_witness import (
    record_operator_material_occurrence,
)
from seed_runtime.material_source import MaterialSourceError
from seed_runtime.occurrence_position_measurement import (
    OCCURRENCE_POSITION_RECORDED_KIND,
    measure_occurrence_position,
    record_occurrence_position_measurement_subject_to_act_binding,
    record_occurrence_position_measurement_act_occurrence,
    record_occurrence_position_measurement_result,
)
from seed_runtime.operator_console import run_persistent_operator_console
from seed_runtime.operator_current_coordinates import (
    advance_operator_current_coordinates,
    read_operator_current_coordinates,
    read_operator_current_coordinates_through,
)


class DictSubclass(dict):
    pass


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


def _attempt(ledger, text, *, locality="s", locality_standing=None):
    exact = text.encode() if type(text) is str else text
    event = record_witness_material_source(
        ledger,
        locality_identity=locality,
        exact_bytes=exact,
        source_boundary="test operator material boundary",
    )
    standing = {
        "current_standing": {
            "material_result_occurrence": {
                "subject_reference": event.material["result_identity"],
                "result_occurrence_identity": event.identity,
            }
        }
    }
    if locality_standing is not None:
        standing["locality_standing"] = locality_standing
    return standing


def _standing(ledger, *, locality="s"):
    return read_operator_current_coordinates(
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
    binding = record_occurrence_position_measurement_subject_to_act_binding(
        ledger,
        recording_locality_identity="s",
        finding=finding,
        current_coordinates=_standing(ledger),
    )
    act_occurrence = record_occurrence_position_measurement_act_occurrence(
        ledger,
        binding_event_identity=binding.identity,
        current_coordinates=_standing(ledger),
    )
    return record_occurrence_position_measurement_result(
        ledger,
        act_occurrence_event_identity=act_occurrence.identity,
    )


def _measurement_ledger():
    ledger = EventLedger()
    record_operator_material_occurrence(
        ledger,
        locality_identity="s",
        exact=b"material",
        source_boundary="test boundary",
    )
    return ledger


def _measurement_coordinates(event):
    coordinates = {
        "recorded_occurrence_identity": event.identity,
        "result_identity": event.material["result_identity"],
        "act_occurrence_identity": event.material["act_occurrence_identity"],
        "act_occurrence_event_identity": event.material[
            "act_occurrence_event_identity"
        ],
    }
    yield_relation_identity = event.material.get("yield_relation_identity")
    if type(yield_relation_identity) is str:
        coordinates["yield_relation_identity"] = yield_relation_identity
    return coordinates


def _pair_lifecycle(ledger):
    result = _record_measurement(ledger, BYTE_PAIR_MEASUREMENT_RECORDED_KIND)
    measurement_act = ledger.get(
        result.material["act_occurrence_event_identity"]
    )
    applicability = ledger.get(
        result.material["input_applicability_event_identity"]
    )
    applicability_act = ledger.get(
        applicability.material["act_occurrence_event_identity"]
    )
    assignment = ledger.get(
        result.material["subject_to_act_binding_reference"][
            "recorded_occurrence_identity"
        ]
    )
    return assignment, applicability_act, applicability, measurement_act, result


def test_pair_standing_replay_carries_both_subject_to_act_bindings_and_result():
    ledger = _measurement_ledger()
    measurement_binding, applicability_act, _applicability, _measurement_act, result = (
        _pair_lifecycle(ledger)
    )
    applicability_binding_identity = applicability_act.material[
        "subject_to_act_binding_reference"
    ]["recorded_occurrence_identity"]

    standing = _standing(ledger)

    assert standing["subject_to_act_binding_occurrences"].get(
        applicability_binding_identity, object()
    ) is None
    assert standing["subject_to_act_binding_occurrences"].get(
        measurement_binding.identity, object()
    ) is None
    assert result.identity in standing["measurement_occurrences"]


def test_pair_standing_replay_refuses_changed_subject_to_act_binding():
    ledger = _measurement_ledger()
    measurement_binding, _applicability_act, _applicability, _measurement_act, _result = (
        _pair_lifecycle(ledger)
    )
    measurement_binding.material["measurement_rule"] = "changed rule"

    with pytest.raises(ByteMeasurementError, match="binding coordinates"):
        _standing(ledger)


def test_pair_standing_replay_and_public_readers_survive_sqlite_reopen(tmp_path):
    path = tmp_path / "pair-standing-replay.sqlite"
    ledger = SQLiteEventLedger(path)
    record_operator_material_occurrence(
        ledger,
        locality_identity="s",
        exact=b"material",
        source_boundary="test boundary",
    )
    assignment, _applicability_act, _applicability, _measurement_act, result = (
        _pair_lifecycle(ledger)
    )
    ledger.close()

    reopened = SQLiteEventLedger(path)
    assert result.identity in _standing(reopened)["measurement_occurrences"]
    assert get_byte_position_pair_measurement_subject_to_act_binding(
        reopened, assignment.identity
    ).identity == assignment.identity
    assert result_positions_of_recorded_byte_position_pair_measurement(
        reopened, result.identity
    )
    reopened.close()


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
        for occurrence in standing_one["material_result_occurrences"]
    }
    two_subjects = {
        occurrence["subject_reference"]
        for occurrence in standing_two["material_result_occurrences"]
    }
    assert one_subjects == {first["current_standing"]["material_result_occurrence"]["subject_reference"]}
    assert two_subjects == {second["current_standing"]["material_result_occurrence"]["subject_reference"]}
    assert not {
        occurrence["result_occurrence_identity"]
        for occurrence in standing_one["material_result_occurrences"]
    } & {
        occurrence["result_occurrence_identity"]
        for occurrence in standing_two["material_result_occurrences"]
    }


def test_current_coordinates_carry_exact_measurement_identities_in_append_order():
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
    exact_measurement_coordinates = {
        "recorded_occurrence_identity",
        "result_identity",
        "act_occurrence_identity",
        "act_occurrence_event_identity",
    }
    assert (
        set(standing["measurement_occurrences"][byte.identity])
        == exact_measurement_coordinates
    )
    assert (
        set(standing["measurement_occurrences"][pair.identity])
        == exact_measurement_coordinates
    )
    assert (
        set(standing["measurement_occurrences"][positions.identity])
        == exact_measurement_coordinates
    )
    assert "result_positions" not in str(standing["measurement_occurrences"])
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


def test_current_coordinates_carry_no_measurement_without_a_recorded_result():
    ledger = _measurement_ledger()

    assert _standing(ledger)["measurement_occurrences"] == {}


@pytest.mark.parametrize("carrier", ([], DictSubclass()))
def test_advance_refuses_a_nonexact_prior_measurement_accumulator(carrier):
    ledger = _measurement_ledger()
    standing = _standing(ledger)
    standing["measurement_occurrences"] = carrier

    with pytest.raises(ValueError, match="exact Measurement occurrences"):
        advance_operator_current_coordinates(
            ledger,
            (),
            locality_identity="s",
            prior=standing,
        )


def test_advance_refuses_an_omitted_intervening_locality_occurrence():
    ledger = EventLedger()
    first = record_witness_material_source(
        ledger,
        locality_identity="s",
        exact_bytes=b"first",
        source_boundary="first test boundary",
    )
    intervening = record_witness_material_source(
        ledger,
        locality_identity="s",
        exact_bytes=b"intervening",
        source_boundary="intervening test boundary",
    )
    later = record_witness_material_source(
        ledger,
        locality_identity="s",
        exact_bytes=b"later",
        source_boundary="later test boundary",
    )
    prior = read_operator_current_coordinates_through(
        ledger,
        locality_identity="s",
        through_event_occurrence_identity=first.identity,
    )

    with pytest.raises(ValueError, match="complete Locality occurrence interval"):
        advance_operator_current_coordinates(
            ledger,
            (later.identity,),
            locality_identity="s",
            prior=prior,
        )

    interval = ledger.locality_occurrence_interval(
        locality_identity="s",
        after_occurrence_identity=first.identity,
        through_occurrence_identity=later.identity,
    )
    current_coordinates = advance_operator_current_coordinates(
        ledger,
        tuple(event.identity for event in interval),
        locality_identity="s",
        prior=prior,
    )
    recorded_occurrences = {
        occurrence["result_occurrence_identity"]
        for occurrence in current_coordinates["material_result_occurrences"]
    }
    assert recorded_occurrences == {
        first.identity,
        intervening.identity,
        later.identity,
    }
    assert current_coordinates["through_event_occurrence_identity"] == later.identity


def test_current_coordinates_carry_only_exact_yielded_result_identities():
    ledger = EventLedger()
    source = record_operator_material_occurrence(
        ledger,
        locality_identity="s",
        exact=b"raw result",
        source_boundary="test boundary",
    )
    measurement = _record_byte_measurement(
        ledger,
        source_localities=("s",),
        recording_locality_identity="s",
    )

    standing = _standing(ledger)

    source_act = ledger.get(source.material["act_occurrence_event_identity"])
    measurement_act = ledger.get(
        measurement.material["act_occurrence_event_identity"]
    )
    assert standing["exact_result_occurrences"] == {
        source.identity: source_act.material["subject_to_act_binding_reference"],
        measurement.identity: measurement_act.material[
            "subject_to_act_binding_reference"
        ],
    }
    assert all(
        type(identity) is str for identity in standing["exact_result_occurrences"]
    )
    assert all(
        standing["exact_result_occurrences"][identity] is not None
        for identity in (source.identity, measurement.identity)
    )


def test_locality_standing_refuses_raw_result_with_substituted_act():
    ledger = EventLedger()
    source = record_witness_material_source(
        ledger,
        locality_identity="s",
        exact_bytes=b"raw result",
        source_boundary="test boundary",
    )
    other = record_witness_material_source(
        ledger,
        locality_identity="s",
        exact_bytes=b"other result",
        source_boundary="test boundary",
    )
    source.material["act_occurrence_event_identity"] = other.material[
        "act_occurrence_event_identity"
    ]

    with pytest.raises(MaterialSourceError):
        _standing(ledger)


def test_locality_standing_refuses_corrupted_raw_result(monkeypatch):
    ledger = EventLedger()
    source = record_witness_material_source(
        ledger,
        locality_identity="s",
        exact_bytes=b"raw result",
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

    with pytest.raises(
        MaterialSourceError,
        match="absent or corrupted",
    ):
        _standing(ledger)


@pytest.mark.parametrize(
    "required_occurrence_coordinate",
    ("act_occurrence_event_identity",),
)
def test_locality_standing_refuses_corrupted_raw_source_act(
    monkeypatch, required_occurrence_coordinate
):
    ledger = EventLedger()
    source = record_witness_material_source(
        ledger,
        locality_identity="s",
        exact_bytes=b"raw result",
        source_boundary="test boundary",
    )
    corrupted_identity = source.material[required_occurrence_coordinate]
    integrity_of = ledger.integrity_of
    monkeypatch.setattr(
        ledger,
        "integrity_of",
        lambda identity: (
            CORRUPTED if identity == corrupted_identity else integrity_of(identity)
        ),
    )

    with pytest.raises(MaterialSourceError):
        _standing(ledger)


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
    record_operator_material_occurrence(
        ledger,
        locality_identity="s",
        exact=b"material",
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
    inherited = second["locality_standing"]["material_result_occurrences"]
    assert [occurrence["subject_reference"] for occurrence in inherited] == [
        first["current_standing"]["material_result_occurrence"]["subject_reference"]
    ]
    assert first["current_standing"]["material_result_occurrence"]["subject_reference"] == (
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


def test_absent_continuation_remains_absent():
    ledger = EventLedger()
    _attempt(ledger, "material\n")

    current_coordinates = _standing(ledger)

    # No Locality occurrence records a continuation relation. It remains
    # absent rather than becoming a negative Assertion.
    assert current_coordinates["locality_continuation_relation_occurrences"] == {}
    next_attempt = _attempt(
        ledger, "next\n", locality_standing=current_coordinates
    )
    assert next_attempt["locality_standing"]["locality_continuation_relation_occurrences"] == {}
