"""Source and destination are addressed by one Locality relation occurrence."""

from __future__ import annotations

from copy import deepcopy

import pytest


from seed_runtime.events import CORRUPTED, EventLedger, SQLiteEventLedger
from seed_runtime.witness_material_source import record_witness_material_source
from seed_runtime.operator_current_coordinates import (
    advance_operator_current_coordinates,
    read_operator_current_coordinates,
)
from seed_runtime.operator_locality_continuation import (
    LOCALITY_CONTINUATION_ACT_OCCURRENCE_EVENT,
    LOCALITY_CONTINUATION_RECORDED_KIND,
    LocalityContinuationError,
    get_recorded_locality_continuation,
    record_locality_continuation_act_occurrence,
    record_locality_continuation_result,
)


def _source_boundary(
    ledger: EventLedger, locality_identity: str = "source"
) -> tuple[object, str]:
    source = record_witness_material_source(
        ledger,
        locality_identity=locality_identity,
        exact_bytes=b"\x00\xffprior\n",
        source_boundary="fixture boundary",
    )
    return source, source.identity


def _act(
    ledger: EventLedger,
    boundary: str,
    *,
    source_locality_identity: str = "source",
):
    return record_locality_continuation_act_occurrence(
        ledger,
        source_locality_identity=source_locality_identity,
        source_through_event_occurrence_identity=boundary,
    )


def test_two_stage_continuation_records_exact_relation_without_copying_source_coordinates():
    ledger = EventLedger()
    source, boundary = _source_boundary(ledger)

    act_occurrence = _act(ledger, boundary)
    destination = act_occurrence.locality_identity
    after_act = read_operator_current_coordinates(
        ledger, locality_identity=destination
    )

    assert act_occurrence.kind == LOCALITY_CONTINUATION_ACT_OCCURRENCE_EVENT
    assert destination != "source"
    assert act_occurrence.exact_material is None
    assert act_occurrence.material["source_coordinate_reference"][
        "source_through_event_occurrence_identity"
    ] == boundary
    assert "subject_to_act_binding_reference" not in act_occurrence.material
    assert all(
        event.kind
        != "operator.locality_continuation_subject_to_act_binding_recorded"
        for event in ledger.list_events()
    )
    assert "act_occurrence_identity" not in act_occurrence.material
    assert "continuation_act_identity" not in act_occurrence.material
    assert act_occurrence.material["act"] == "Preservation"
    assert after_act["event_count"] == 1
    assert after_act["locality_continuation_relation_occurrences"] == {}
    assert after_act["subject_to_act_binding_occurrences"] == {}
    assert after_act["material_result_occurrences"] == []
    assert after_act["measurement_occurrences"] == {}
    assert after_act["exact_result_occurrences"] == {}

    result = record_locality_continuation_result(
        ledger,
        act_occurrence_event_identity=act_occurrence.identity,
    )
    recorded = get_recorded_locality_continuation(
        ledger, result.identity
    )
    source_reference = recorded["source_coordinate_reference"]

    assert result.kind == LOCALITY_CONTINUATION_RECORDED_KIND
    assert result.exact_material is None
    assert source_reference == {
        "source_locality_identity": "source",
        "source_through_event_occurrence_identity": source.identity,
    }
    assert recorded["destination_locality_identity"] == destination
    assert "locality_relation" not in recorded
    assert result.identity not in {
        act_occurrence.identity,
    }
    assert "subject_to_act_binding_reference" not in recorded
    assert recorded["exact_act"] == "Preservation"
    assert "applicability" not in recorded
    assert "priority" not in recorded
    advanced = advance_operator_current_coordinates(
        ledger,
        (result.identity,),
        locality_identity=destination,
        prior=after_act,
    )
    replayed = read_operator_current_coordinates(
        ledger, locality_identity=destination
    )
    assert advanced == replayed
    assert replayed["locality_continuation_relation_occurrences"] == {result.identity: None}
    assert replayed["subject_to_act_binding_occurrences"] == {}
    assert replayed["material_result_occurrences"] == []
    assert replayed["measurement_occurrences"] == {}
    assert replayed["exact_result_occurrences"] == {
        result.identity: {
            "act_occurrence_event_identity": act_occurrence.identity,
            "subject_reference": act_occurrence.material[
                "source_coordinate_reference"
            ],
        },
    }


def test_reopened_ledger_does_not_reissue_locality_continuation_identities(tmp_path):
    path = tmp_path / "continuation.sqlite"
    ledger = SQLiteEventLedger(str(path))
    _source, boundary = _source_boundary(ledger)
    first_act = _act(ledger, boundary)
    first_result = record_locality_continuation_result(
        ledger, act_occurrence_event_identity=first_act.identity
    )
    first_identities = {
        first_act.locality_identity,
        first_act.identity,
        first_result.identity,
    }
    ledger.close()

    ledger = SQLiteEventLedger(str(path))
    second_act = _act(ledger, boundary)
    second_result = record_locality_continuation_result(
        ledger, act_occurrence_event_identity=second_act.identity
    )
    second_identities = {
        second_act.locality_identity,
        second_act.identity,
        second_result.identity,
    }

    assert len(first_identities) == len(second_identities) == 3
    assert first_identities.isdisjoint(second_identities)
    assert "result_identity" not in get_recorded_locality_continuation(
        ledger, first_result.identity
    )
    assert "result_identity" not in get_recorded_locality_continuation(
        ledger, second_result.identity
    )


def test_durable_continuation_material_contains_no_operator_shorthand():
    ledger = EventLedger()
    _source, boundary = _source_boundary(ledger)
    act_occurrence = _act(ledger, boundary)
    record_locality_continuation_result(
        ledger,
        act_occurrence_event_identity=act_occurrence.identity,
    )
    durable = repr(
        [
            (event.kind, event.material)
            for event in ledger.list_locality(act_occurrence.locality_identity)
        ]
    ).lower()

    for shorthand in (
        "memory",
        "important",
        "command",
        "cut",
        "source-boundary locality relation",
    ):
        assert shorthand not in durable


def test_later_source_occurrences_do_not_move_the_exact_source_cut():
    ledger = EventLedger()
    source, boundary = _source_boundary(ledger)
    act_occurrence = _act(ledger, boundary)
    later = record_witness_material_source(
        ledger,
        locality_identity="source",
        exact_bytes=b"later",
        source_boundary="fixture boundary",
    )

    result = record_locality_continuation_result(
        ledger,
        act_occurrence_event_identity=act_occurrence.identity,
    )
    reference = get_recorded_locality_continuation(
        ledger, result.identity
    )["source_coordinate_reference"]

    assert reference["source_through_event_occurrence_identity"] == source.identity
    assert reference["source_through_event_occurrence_identity"] != later.identity


def test_source_occurrence_from_another_locality_is_refused():
    ledger = EventLedger()
    _source, boundary = _source_boundary(ledger)

    with pytest.raises(LocalityContinuationError):
        _act(ledger, boundary, source_locality_identity="other")


def test_missing_source_occurrence_is_refused():
    ledger = EventLedger()

    with pytest.raises(LocalityContinuationError):
        _act(ledger, "missing")


def test_corrupted_source_occurrence_is_refused(monkeypatch):
    ledger = EventLedger()
    _source, boundary = _source_boundary(ledger)
    integrity_of = ledger.integrity_of
    monkeypatch.setattr(
        ledger,
        "integrity_of",
        lambda identity: CORRUPTED if identity == boundary else integrity_of(identity),
    )

    with pytest.raises(LocalityContinuationError):
        _act(ledger, boundary)


def test_continuation_carries_only_its_direct_source_coordinates():
    ledger = EventLedger()
    _source, first_boundary = _source_boundary(ledger, "a")
    first_act = _act(
        ledger, first_boundary, source_locality_identity="a"
    )
    first_result = record_locality_continuation_result(
        ledger,
        act_occurrence_event_identity=first_act.identity,
    )
    first_destination = first_result.locality_identity
    second_act = _act(
        ledger,
        first_result.identity,
        source_locality_identity=first_destination,
    )
    second_result = record_locality_continuation_result(
        ledger,
        act_occurrence_event_identity=second_act.identity,
    )
    second_recorded = get_recorded_locality_continuation(
        ledger, second_result.identity
    )

    assert second_recorded["source_coordinate_reference"] == {
        "source_locality_identity": first_destination,
        "source_through_event_occurrence_identity": first_result.identity,
    }
    assert read_operator_current_coordinates(
        ledger, locality_identity=second_result.locality_identity
    )["locality_continuation_relation_occurrences"] == {second_result.identity: None}


def test_one_continuation_act_occurrence_cannot_address_two_results():
    ledger = EventLedger()
    _source, boundary = _source_boundary(ledger)
    act_occurrence = _act(ledger, boundary)
    record_locality_continuation_result(
        ledger,
        act_occurrence_event_identity=act_occurrence.identity,
    )

    with pytest.raises(
        LocalityContinuationError,
        match="one Locality continuation Act occurrence cannot address two results",
    ):
        record_locality_continuation_result(
            ledger,
            act_occurrence_event_identity=act_occurrence.identity,
        )


@pytest.mark.parametrize(
    "coordinate",
    (
        "source_coordinate_reference",
        "destination_locality_identity",
    ),
)
def test_changed_result_coordinates_are_refused(coordinate):
    ledger = EventLedger()
    _source, boundary = _source_boundary(ledger)
    act_occurrence = _act(ledger, boundary)
    result = record_locality_continuation_result(
        ledger,
        act_occurrence_event_identity=act_occurrence.identity,
    )
    changed = ledger.get(result.identity)
    changed.material[coordinate] = "different"

    with pytest.raises(LocalityContinuationError):
        get_recorded_locality_continuation(ledger, result.identity)


def test_equal_source_cuts_keep_distinct_occurrences_and_destinations():
    ledger = EventLedger()
    _source, boundary = _source_boundary(ledger)
    first_act = _act(ledger, boundary)
    second_act = _act(ledger, boundary)
    first = record_locality_continuation_result(
        ledger, act_occurrence_event_identity=first_act.identity
    )
    second = record_locality_continuation_result(
        ledger, act_occurrence_event_identity=second_act.identity
    )

    assert first_act.identity != second_act.identity
    assert first.locality_identity != second.locality_identity
    assert "act_occurrence_identity" not in first.material
    assert "act_occurrence_identity" not in second.material
    assert "continuation_act_identity" not in first.material
    assert "continuation_act_identity" not in second.material
    assert first.identity != second.identity


def test_act_occurrence_without_result_is_not_carried_as_a_relation():
    ledger = EventLedger()
    _source, boundary = _source_boundary(ledger)
    act_occurrence = _act(ledger, boundary)

    standing = read_operator_current_coordinates(
        ledger, locality_identity=act_occurrence.locality_identity
    )

    assert standing["locality_continuation_relation_occurrences"] == {}
    assert standing["subject_to_act_binding_occurrences"] == {}
    assert standing["through_event_occurrence_identity"] == act_occurrence.identity


def test_prior_relation_carrier_must_remain_one_identity_dictionary():
    ledger = EventLedger()
    _source, boundary = _source_boundary(ledger)
    act_occurrence = _act(ledger, boundary)
    result = record_locality_continuation_result(
        ledger, act_occurrence_event_identity=act_occurrence.identity
    )
    standing = read_operator_current_coordinates(
        ledger, locality_identity=result.locality_identity
    )
    broken = deepcopy(standing)
    broken["locality_continuation_relation_occurrences"] = [result.identity]

    with pytest.raises(
        ValueError, match="exact Locality continuation relations"
    ):
        advance_operator_current_coordinates(
            ledger,
            (),
            locality_identity=result.locality_identity,
            prior=broken,
        )


def test_act_occurrence_refuses_a_source_boundary_after_it():
    ledger = EventLedger()
    _source, boundary = _source_boundary(ledger)
    act = _act(ledger, boundary)
    later, _later_boundary = _source_boundary(ledger)
    changed = ledger.get(act.identity)
    changed.material["source_coordinate_reference"] = {
        "source_locality_identity": later.locality_identity,
        "source_through_event_occurrence_identity": later.identity,
    }

    with pytest.raises(LocalityContinuationError, match="prior source boundary"):
        record_locality_continuation_result(
            ledger,
            act_occurrence_event_identity=act.identity,
        )
