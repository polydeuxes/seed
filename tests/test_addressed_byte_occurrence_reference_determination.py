"""Each exact source-byte position reference is one exact subject."""

from copy import deepcopy

import pytest

from seed_runtime.addressed_byte_occurrence_reference_determination import (
    DETERMINATION_ACT_OCCURRENCE_EVENT,
    DETERMINATION_RESULT_KIND,
    AddressedByteOccurrenceReferenceDeterminationError,
    get_addressed_byte_occurrence_reference_determination_act_occurrence,
    get_recorded_addressed_byte_occurrence_reference_determination,
    record_addressed_byte_occurrence_reference_determination_act_occurrence,
    record_addressed_byte_occurrence_reference_determination_result,
)
from seed_runtime.events import EventLedger, SQLiteEventLedger
from seed_runtime.measurement_of_position_coordinates_of_byte_pair_occurrences import (
    _source_position_coordinate_reference,
    record_byte_pair_occurrence_position_measurement_act_occurrence,
    record_byte_pair_occurrence_position_measurement_result,
    record_byte_pair_occurrence_position_measurement_subject_to_act_binding,
    references_to_recorded_byte_pair_occurrences_carrying_addressed_source_position_coordinate,
)
from seed_runtime.operator_current_coordinates import (
    advance_operator_current_coordinates,
    read_operator_current_coordinates,
)
from seed_runtime.yield_relation import RECORDED_YIELD_RELATION_EVENT
from tests.operator_material_source_test_witness import (
    record_operator_material_occurrence,
)


def _advance(ledger, current_coordinates, *events):
    interval = ledger.locality_occurrence_interval(
        locality_identity=current_coordinates["locality_identity"],
        after_occurrence_identity=current_coordinates[
            "through_event_occurrence_identity"
        ],
        through_occurrence_identity=events[-1].identity,
    )
    return advance_operator_current_coordinates(
        ledger,
        (event.identity for event in interval),
        locality_identity=current_coordinates["locality_identity"],
        prior=current_coordinates,
    )


def _direct(ledger, exact=b"2+2=5\n", locality="addressed-byte"):
    source = record_operator_material_occurrence(
        ledger,
        locality_identity=locality,
        exact=exact,
        source_boundary="exact supplied material boundary",
    )
    current = read_operator_current_coordinates(ledger, locality_identity=locality)
    binding = record_byte_pair_occurrence_position_measurement_subject_to_act_binding(
        ledger,
        source_material_result_occurrence_identity=source.identity,
        current_coordinates=current,
    )
    current = _advance(ledger, current, binding)
    act = record_byte_pair_occurrence_position_measurement_act_occurrence(
        ledger,
        binding_event_identity=binding.identity,
        binding_current_coordinates=current,
    )
    current = _advance(ledger, current, act)
    result = record_byte_pair_occurrence_position_measurement_result(
        ledger, act_occurrence_event_identity=act.identity
    )
    return source, result, _advance(ledger, current, result)


def _coordinate(ledger, source, exact, position):
    return _source_position_coordinate_reference(
        source_material_result_occurrence_identity=source.identity,
        source_locality_identity=source.locality_identity,
        completeness_boundary_identity=(
            ledger.append_boundary_through_occurrence(source.identity).identity
        ),
        position=position,
        exact_material=exact[position : position + 1],
    )


def _determination_source(
    ledger, exact=b"2+2=5\n", position=3, locality="addressed-byte"
):
    source, direct_result, current = _direct(ledger, exact, locality)
    coordinate = _coordinate(ledger, source, exact, position)
    return {
        "source": source,
        "direct_result": direct_result,
        "coordinate": coordinate,
        "current_coordinates": current,
    }


def _record(ledger, exact=b"2+2=5\n", position=3, locality="addressed-byte"):
    recorded = _determination_source(ledger, exact, position, locality)
    act = record_addressed_byte_occurrence_reference_determination_act_occurrence(
        ledger,
        direct_result_event_identity=recorded["direct_result"].identity,
        addressed_source_byte_position_coordinate_reference=recorded["coordinate"],
        current_coordinates=recorded["current_coordinates"],
    )
    current = _advance(ledger, recorded["current_coordinates"], act)
    result = record_addressed_byte_occurrence_reference_determination_result(
        ledger,
        determination_act_occurrence_event_identity=act.identity,
        current_coordinates=current,
    )
    return {
        **recorded,
        "determination_act": act,
        "result": result,
        "current_coordinates": _advance(ledger, current, result),
    }


def test_interior_address_preserves_every_and_only_ordered_result_position_reference():
    ledger = EventLedger()
    recorded = _record(ledger)
    expected = references_to_recorded_byte_pair_occurrences_carrying_addressed_source_position_coordinate(
        ledger,
        recorded["direct_result"].identity,
        recorded["coordinate"],
    )
    material = get_recorded_addressed_byte_occurrence_reference_determination(
        ledger, recorded["result"].identity
    )
    assert material["ordered_result_position_references"] == [
        reference.result_position_reference for reference in expected
    ]
    assert [reference.exact_pair for reference in expected] == [b"2=", b"=5"]


@pytest.mark.parametrize(
    ("exact", "position", "expected_count"),
    ((b"ab", 0, 1), (b"ab", 1, 1), (b"x", 0, 0), (b"aaa", 1, 2)),
)
def test_zero_one_and_two_reference_multiplicities_survive(
    exact, position, expected_count
):
    recorded = _record(EventLedger(), exact=exact, position=position)
    assert len(
        recorded["result"].material["ordered_result_position_references"]
    ) == expected_count


def test_determination_records_no_prospective_binding_or_applicability():
    ledger = EventLedger()
    recorded = _record(ledger)
    kinds = tuple(event.kind for event in ledger.list_locality("addressed-byte"))
    assert DETERMINATION_ACT_OCCURRENCE_EVENT in kinds
    assert DETERMINATION_RESULT_KIND in kinds
    assert not any(
        "addressed_byte_occurrence_reference_determination.applicability"
        in kind
        or "addressed_byte_occurrence_reference_determination."
        "determination_subject_to_act_binding" in kind
        for kind in kinds
    )
    assert "subject_to_act_binding_reference" not in recorded[
        "determination_act"
    ].material
    assert "applicability_result_reference" not in recorded["result"].material


def test_act_refuses_stale_changed_and_other_locality_coordinates_atomically():
    ledger = EventLedger()
    source, direct_result, current = _direct(ledger, b"ab")
    coordinate = _coordinate(ledger, source, b"ab", 0)
    stale = deepcopy(current)
    record_operator_material_occurrence(
        ledger,
        locality_identity="addressed-byte",
        exact=b"later",
        source_boundary="later boundary",
    )
    before = len(ledger.list())
    with pytest.raises(AddressedByteOccurrenceReferenceDeterminationError):
        record_addressed_byte_occurrence_reference_determination_act_occurrence(
            ledger,
            direct_result_event_identity=direct_result.identity,
            addressed_source_byte_position_coordinate_reference=coordinate,
            current_coordinates=stale,
        )
    changed = deepcopy(
        read_operator_current_coordinates(ledger, locality_identity="addressed-byte")
    )
    changed["measurement_occurrences"] = {}
    with pytest.raises(AddressedByteOccurrenceReferenceDeterminationError):
        record_addressed_byte_occurrence_reference_determination_act_occurrence(
            ledger,
            direct_result_event_identity=direct_result.identity,
            addressed_source_byte_position_coordinate_reference=coordinate,
            current_coordinates=changed,
        )
    assert len(ledger.list()) == before


def test_changed_source_or_act_invalidates_later_readers():
    ledger = EventLedger()
    recorded = _record(ledger)
    recorded["direct_result"].material["result_identity"] = "changed"
    with pytest.raises(AddressedByteOccurrenceReferenceDeterminationError):
        get_recorded_addressed_byte_occurrence_reference_determination(
            ledger, recorded["result"].identity
        )

    ledger = EventLedger()
    recorded = _record(ledger)
    recorded["determination_act"].material["determination_result_identity"] = "changed"
    with pytest.raises(AddressedByteOccurrenceReferenceDeterminationError):
        get_recorded_addressed_byte_occurrence_reference_determination(
            ledger, recorded["result"].identity
        )


def test_one_act_refuses_a_second_result():
    ledger = EventLedger()
    recorded = _record(ledger)
    with pytest.raises(
        AddressedByteOccurrenceReferenceDeterminationError,
        match="already recorded",
    ):
        record_addressed_byte_occurrence_reference_determination_result(
            ledger,
            determination_act_occurrence_event_identity=recorded[
                "determination_act"
            ].identity,
        )


@pytest.mark.parametrize("intervening_change", ("append", "mutate"))
def test_result_rechecks_coordinates_after_its_population_read(
    monkeypatch, intervening_change
):
    ledger = EventLedger()
    recorded = _determination_source(ledger)
    act = record_addressed_byte_occurrence_reference_determination_act_occurrence(
        ledger,
        direct_result_event_identity=recorded["direct_result"].identity,
        addressed_source_byte_position_coordinate_reference=recorded["coordinate"],
        current_coordinates=recorded["current_coordinates"],
    )
    current = _advance(ledger, recorded["current_coordinates"], act)
    original = ledger.iter_locality_kind
    changed = False

    def intervene(locality_identity, kind):
        nonlocal changed
        events = tuple(original(locality_identity, kind))
        if kind == DETERMINATION_RESULT_KIND and not changed:
            changed = True
            if intervening_change == "append":
                ledger.append(
                    "test.intervening.unrelated",
                    {"source": "intervening occurrence"},
                    locality_identity=locality_identity,
                )
            else:
                act.material["determination_result_identity"] = "changed"
        return iter(events)

    monkeypatch.setattr(ledger, "iter_locality_kind", intervene)
    before = len(ledger.list())
    with pytest.raises(AddressedByteOccurrenceReferenceDeterminationError):
        record_addressed_byte_occurrence_reference_determination_result(
            ledger,
            determination_act_occurrence_event_identity=act.identity,
            current_coordinates=current,
        )
    expected_growth = 1 if intervening_change == "append" else 0
    assert len(ledger.list()) == before + expected_growth
    assert changed is True
    assert not tuple(original(act.locality_identity, DETERMINATION_RESULT_KIND))


def test_act_and_result_have_no_yield():
    ledger = EventLedger()
    recorded = _record(ledger)
    assert "yield_relation_identity" not in recorded["result"].material
    assert not tuple(
        ledger.iter_locality_kind(
            recorded["source"].locality_identity, RECORDED_YIELD_RELATION_EVENT
        )
    )


def test_call_local_coordinates_equal_full_replay():
    ledger = EventLedger()
    recorded = _record(ledger)
    replayed = read_operator_current_coordinates(
        ledger, locality_identity=recorded["source"].locality_identity
    )
    assert recorded["current_coordinates"] == replayed
    assert recorded["result"].identity in replayed["measurement_occurrences"]


def test_result_survives_sqlite_restart(tmp_path):
    database = tmp_path / "addressed-determination.sqlite"
    ledger = SQLiteEventLedger(str(database))
    recorded = _record(ledger)
    act_identity = recorded["determination_act"].identity
    result_identity = recorded["result"].identity
    ledger.close()

    reopened = SQLiteEventLedger(str(database))
    assert get_addressed_byte_occurrence_reference_determination_act_occurrence(
        reopened, act_identity
    ).identity == act_identity
    assert get_recorded_addressed_byte_occurrence_reference_determination(
        reopened, result_identity
    )["result_identity"] == recorded["result"].material["result_identity"]
    reopened.close()
