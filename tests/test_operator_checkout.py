"""Operator movement: an exact destination Locality."""

from __future__ import annotations

from copy import deepcopy
from io import BytesIO
from pathlib import Path

import pytest


from seed_runtime.events import CORRUPTED, EventLedger, SQLiteEventLedger
from seed_runtime.operator_checkpoint import (
    get_operator_checkpoint_material_occurrence,
)
from seed_runtime.operator_checkout import (
    OperatorCheckoutRequest,
    request_operator_checkout,
)
from seed_runtime.operator_command import AddressedOperatorCommand, OperatorCommandFrame
from seed_runtime.operator_console import run_persistent_operator_console
from seed_runtime.operator_current_coordinates import (
    advance_operator_current_coordinates,
    read_operator_current_coordinates,
)
from seed_runtime.recorded_boundary_locality import (
    RECORDED_BOUNDARY_LOCALITY_ACT_OCCURRENCE_EVENT,
    RECORDED_BOUNDARY_LOCALITY_RECORDED_KIND,
    RecordedBoundaryLocalityError,
    get_recorded_boundary_locality,
    get_recorded_boundary_locality_act_occurrence,
    record_recorded_boundary_locality_act_occurrence,
    record_recorded_boundary_locality_result,
)


def _command(exact_bytes=b"/checkout\n", arguments=b""):
    return AddressedOperatorCommand(
        locality_identity="source",
        addressed_through_event_occurrence_identity="current_coordinates-boundary",
        frame=OperatorCommandFrame(
            exact_bytes=exact_bytes,
            name=b"checkout",
            arguments=arguments,
        ),
    )


class _IntegrityAdversaryLedger(EventLedger):
    def __init__(self):
        super().__init__()
        self.corrupted = set()

    def integrity_of(self, event_identity):
        if event_identity in self.corrupted:
            return CORRUPTED
        return super().integrity_of(event_identity)


class _UnreadableUnrelatedSQLiteLedger(SQLiteEventLedger):
    unreadable_identity = None

    def _row_to_event(self, row):
        if row is not None and row["identity"] == self.unreadable_identity:
            raise ValueError("unrelated material must not be decoded")
        return super()._row_to_event(row)


def _coordinates_with_through_occurrence_reference(ledger, *, locality="source"):
    run_persistent_operator_console(
        ledger=ledger,
        locality_identity=locality,
        input_stream=BytesIO(b"/checkpoint\n"),
    )
    reference_result = next(
        event
        for event in ledger.list_locality(locality)
        if event.exact_material == b"/checkpoint\n"
    )
    get_operator_checkpoint_material_occurrence(ledger, reference_result.identity)
    return reference_result, read_operator_current_coordinates(
        ledger, locality_identity=locality
    )


def _act(ledger, current_coordinates):
    return record_recorded_boundary_locality_act_occurrence(
        ledger, source_current_coordinates=current_coordinates
    )


@pytest.mark.parametrize("exact", (b"/checkout", b"/checkout\n", b"/checkout\r\n"))
def test_checkout_request_is_exact_argument_free_operator_control(exact):
    assert request_operator_checkout(_command(exact)) == OperatorCheckoutRequest()


@pytest.mark.parametrize("exact", (b"/checkout x\n", b"/checkout \n"))
def test_checkout_request_refuses_payload(exact):
    with pytest.raises(ValueError, match="accepts no material"):
        request_operator_checkout(_command(exact, b"x"))


def test_two_stage_relation_uses_one_reference_and_one_destination_locality():
    ledger = EventLedger()
    reference_result, source_coordinates = _coordinates_with_through_occurrence_reference(ledger)
    act = _act(ledger, source_coordinates)
    destination = act.locality_identity
    before_result = read_operator_current_coordinates(
        ledger, locality_identity=destination
    )
    result = record_recorded_boundary_locality_result(
        ledger, act_occurrence_event_identity=act.identity
    )
    recorded = get_recorded_boundary_locality(ledger, result.identity)

    assert act.kind == RECORDED_BOUNDARY_LOCALITY_ACT_OCCURRENCE_EVENT
    assert result.kind == RECORDED_BOUNDARY_LOCALITY_RECORDED_KIND
    assert tuple(sorted(act.material)) == (
        "act",
        "subject_reference",
    )
    assert tuple(sorted(result.material)) == (
        "act_occurrence_event_identity",
    )
    assert destination != "source"
    assert recorded["through_occurrence_boundary_reference"] == {
        "recorded_occurrence_identity": reference_result.identity,
    }
    assert "through_occurrence_boundary_reference" not in result.material
    assert recorded["destination_locality_identity"] == destination
    assert "destination_locality_identity" not in result.material
    assert "locality_relation" not in recorded
    assert len(
        {
            act.identity,
            result.identity,
        }
    ) == 2
    assert "result_identity" not in act.material
    assert "result_identity" not in result.material
    assert "act_occurrence_identity" not in act.material
    assert "act_occurrence_identity" not in result.material
    assert "exact_act_identity" not in act.material
    assert "exact_act_identity" not in result.material
    assert "subject_to_act_binding_reference" not in act.material
    assert "subject_to_act_binding_reference" not in result.material
    assert not any(
        event.kind
        == "operator.recorded_boundary_locality_subject_to_act_binding_recorded"
        for event in ledger.list()
    )
    advanced = advance_operator_current_coordinates(
        ledger,
        (result.identity,),
        locality_identity=destination,
        prior=before_result,
    )
    replayed = read_operator_current_coordinates(
        ledger, locality_identity=destination
    )
    assert advanced == replayed
    assert replayed["recorded_boundary_locality_relations"] == {
        result.identity: None
    }
    assert replayed["locality_continuation_relation_occurrences"] == {}


def test_act_reader_refuses_changed_subject_coordinates():
    ledger = EventLedger()
    _reference_result, source_coordinates = (
        _coordinates_with_through_occurrence_reference(ledger)
    )
    act = _act(ledger, source_coordinates)
    ledger.get(act.identity).material["subject_reference"] = {
        "recorded_occurrence_identity": "different"
    }

    with pytest.raises((RecordedBoundaryLocalityError, TypeError, ValueError)):
        read_operator_current_coordinates(
            ledger, locality_identity=act.locality_identity
        )


def test_act_order_reads_only_its_exact_occurrence_identities(tmp_path):
    ledger = _UnreadableUnrelatedSQLiteLedger(str(tmp_path / "order.sqlite"))
    unrelated = ledger.append(
        "unrelated",
        {"material": "unreadable"},
        locality_identity="unrelated",
    )
    _reference_result, source_coordinates = (
        _coordinates_with_through_occurrence_reference(ledger)
    )
    act = _act(ledger, source_coordinates)
    ledger.unreadable_identity = unrelated.identity

    assert get_recorded_boundary_locality_act_occurrence(
        ledger, act.identity
    ).identity == act.identity
    ledger.close()


def test_act_refuses_a_subject_outside_its_append_boundary():
    ledger = EventLedger()
    future_q_identity = "evt_000003"
    act = ledger.append(
        RECORDED_BOUNDARY_LOCALITY_ACT_OCCURRENCE_EVENT,
        {
            "act": "Preservation",
            "subject_reference": {
                "recorded_occurrence_identity": future_q_identity,
            },
        },
        locality_identity="destination",
    )
    reference_result, _source_coordinates = (
        _coordinates_with_through_occurrence_reference(ledger)
    )
    assert reference_result.identity == future_q_identity

    with pytest.raises(
        RecordedBoundaryLocalityError, match="requires its prior subject"
    ):
        get_recorded_boundary_locality_act_occurrence(ledger, act.identity)


def test_relation_descendants_carry_one_exact_reference():
    ledger = EventLedger()
    reference_result, source_coordinates = _coordinates_with_through_occurrence_reference(ledger)
    first = record_recorded_boundary_locality_result(
        ledger,
        act_occurrence_event_identity=_act(ledger, source_coordinates).identity,
    )
    first_coordinates = read_operator_current_coordinates(
        ledger, locality_identity=first.locality_identity
    )
    second = record_recorded_boundary_locality_result(
        ledger,
        act_occurrence_event_identity=_act(ledger, first_coordinates).identity,
    )
    relations = [first, second]
    assert len(relations) == 2
    assert relations[0].locality_identity != relations[1].locality_identity
    expected = {
        "recorded_occurrence_identity": reference_result.identity,
    }
    assert [
        get_recorded_boundary_locality(ledger, relation.identity)[
            "through_occurrence_boundary_reference"
        ]
        for relation in relations
    ] == [expected, expected]
    before = get_operator_checkpoint_material_occurrence(
        ledger, reference_result.identity
    )
    assert get_operator_checkpoint_material_occurrence(
        ledger, reference_result.identity
    ) == before


def test_preservation_act_requires_cardinality_one_current_boundary_reference():
    ledger = EventLedger()
    empty = read_operator_current_coordinates(ledger, locality_identity="source")
    with pytest.raises(
        RecordedBoundaryLocalityError,
        match="exactly one current boundary reference",
    ):
        _act(ledger, empty)

    run_persistent_operator_console(
        ledger=ledger,
        locality_identity="source",
        input_stream=BytesIO(b"/checkpoint\n/checkpoint\n"),
    )
    ambiguous = read_operator_current_coordinates(
        ledger, locality_identity="source"
    )
    with pytest.raises(
        RecordedBoundaryLocalityError,
        match="exactly one current boundary reference",
    ):
        _act(ledger, ambiguous)


@pytest.mark.parametrize(
    ("coordinate", "replacement"),
    (
        ("kind", "different"),
        ("exact_material", b"/different\n"),
    ),
)
def test_corruption_cannot_reduce_two_checkpoint_occurrences_to_one(
    coordinate, replacement
):
    ledger = _IntegrityAdversaryLedger()
    run_persistent_operator_console(
        ledger=ledger,
        locality_identity="source",
        input_stream=BytesIO(b"/checkpoint\n/checkpoint\n"),
    )
    coordinates = read_operator_current_coordinates(
        ledger, locality_identity="source"
    )
    checkpoints = [
        event
        for event in ledger.list_locality("source")
        if event.exact_material == b"/checkpoint\n"
    ]
    assert len(checkpoints) == 2
    changed = ledger.get(checkpoints[1].identity)
    ledger.corrupted.add(changed.identity)
    object.__setattr__(changed, coordinate, replacement)
    before = tuple(ledger.list())

    with pytest.raises(
        RecordedBoundaryLocalityError,
        match="intact material result coordinates",
    ):
        _act(ledger, coordinates)

    assert tuple(ledger.list()) == before


def test_different_locality_or_corrupted_reference_refuses_before_destination_write():
    ledger = _IntegrityAdversaryLedger()
    reference_result, current_coordinates = _coordinates_with_through_occurrence_reference(ledger)
    different_locality = deepcopy(current_coordinates)
    different_locality["locality_identity"] = "elsewhere"
    before = tuple(ledger.list())
    with pytest.raises(RecordedBoundaryLocalityError, match="different"):
        _act(ledger, different_locality)
    assert tuple(ledger.list()) == before

    ledger.corrupted.add(reference_result.identity)
    with pytest.raises(ValueError, match="corrupted"):
        _act(ledger, current_coordinates)
    assert tuple(ledger.list()) == before


def test_one_relation_act_occurrence_cannot_address_two_results():
    ledger = EventLedger()
    _reference_result, current_coordinates = (
        _coordinates_with_through_occurrence_reference(ledger)
    )
    act = _act(ledger, current_coordinates)
    record_recorded_boundary_locality_result(
        ledger, act_occurrence_event_identity=act.identity
    )
    with pytest.raises(
        RecordedBoundaryLocalityError,
        match="one recorded boundary Locality Act occurrence cannot address two results",
    ):
        record_recorded_boundary_locality_result(
            ledger, act_occurrence_event_identity=act.identity
        )


@pytest.mark.parametrize(
    "coordinate",
    (
        "through_occurrence_boundary_reference",
        "destination_locality_identity",
        "subject_to_act_binding_reference",
        "yield_relation_identity",
    ),
)
def test_changed_relation_result_coordinates_are_refused(coordinate):
    ledger = EventLedger()
    _reference_result, current_coordinates = (
        _coordinates_with_through_occurrence_reference(ledger)
    )
    act = _act(ledger, current_coordinates)
    result = record_recorded_boundary_locality_result(
        ledger, act_occurrence_event_identity=act.identity
    )
    ledger.get(result.identity).material[coordinate] = "different"
    with pytest.raises((RecordedBoundaryLocalityError, TypeError, ValueError)):
        get_recorded_boundary_locality(ledger, result.identity)


def test_relation_result_addresses_its_exact_preservation_act():
    ledger = EventLedger()
    _reference_result, current_coordinates = (
        _coordinates_with_through_occurrence_reference(ledger)
    )
    act = _act(ledger, current_coordinates)
    result = record_recorded_boundary_locality_result(
        ledger, act_occurrence_event_identity=act.identity
    )
    assert "exact_act" not in result.material

    ledger.get(act.identity).material["act"] = "Measurement"
    with pytest.raises(RecordedBoundaryLocalityError):
        get_recorded_boundary_locality(ledger, result.identity)


def test_relation_result_requires_its_act_locality():
    ledger = EventLedger()
    _reference_result, current_coordinates = (
        _coordinates_with_through_occurrence_reference(ledger)
    )
    act = _act(ledger, current_coordinates)
    result = record_recorded_boundary_locality_result(
        ledger, act_occurrence_event_identity=act.identity
    )
    assert "destination_locality_identity" not in result.material

    object.__setattr__(
        ledger.get(result.identity), "locality_identity", "elsewhere"
    )
    with pytest.raises(RecordedBoundaryLocalityError):
        get_recorded_boundary_locality(ledger, result.identity)


def test_reference_and_relation_survive_restart_without_copying_source_history(
    tmp_path,
):
    path = tmp_path / "checkout.sqlite"
    ledger = SQLiteEventLedger(str(path))
    reference_result, current_coordinates = _coordinates_with_through_occurrence_reference(ledger)
    first = record_recorded_boundary_locality_result(
        ledger,
        act_occurrence_event_identity=_act(ledger, current_coordinates).identity,
    )
    ledger.close()

    ledger = SQLiteEventLedger(str(path))
    first_coordinates = read_operator_current_coordinates(
        ledger, locality_identity=first.locality_identity
    )
    second = record_recorded_boundary_locality_result(
        ledger,
        act_occurrence_event_identity=_act(ledger, first_coordinates).identity,
    )
    assert second.locality_identity != first.locality_identity
    assert get_recorded_boundary_locality(ledger, second.identity)[
        "through_occurrence_boundary_reference"
    ]["recorded_occurrence_identity"] == reference_result.identity
    source_identities = {
        event.identity for event in ledger.list_locality("source")
    }
    destination_material = repr(
        [event.material for event in ledger.list_locality(second.locality_identity)]
    )
    assert {
        identity for identity in source_identities if identity in destination_material
    } == {reference_result.identity}
    ledger.close()


def test_durable_native_values_do_not_import_operator_or_memory_shorthand():
    ledger = EventLedger()
    _reference_result, current_coordinates = (
        _coordinates_with_through_occurrence_reference(ledger)
    )
    result = record_recorded_boundary_locality_result(
        ledger,
        act_occurrence_event_identity=_act(ledger, current_coordinates).identity,
    )
    durable = repr(
        [
            (event.kind, event.material)
            for event in ledger.list_locality(result.locality_identity)
        ]
    ).lower()
    for absent in ("checkout", "memory", "checkpoint"):
        assert absent not in durable


def test_rosetta_keeps_checkout_and_pointers_as_translation_only():
    root = Path(__file__).resolve().parents[1]
    rosetta = (
        root / "rosetta" / "standing_and_responsibility.md"
    ).read_text(encoding="utf-8")

    assert (
        "Checkout       exact recorded through-occurrence boundary reference + destination "
        "Locality + direct Locality relation; no history copy; no persistent Memory"
    ) in rosetta
    assert (
        "Pointers       one preserved thing + many exact references to it + no identity "
        "collapse; pointer equality establishes no occurrence or current-coordinate equality"
    ) in rosetta


def test_prior_relation_carrier_must_remain_an_identity_dictionary():
    ledger = EventLedger()
    _reference_result, current_coordinates = (
        _coordinates_with_through_occurrence_reference(ledger)
    )
    result = record_recorded_boundary_locality_result(
        ledger,
        act_occurrence_event_identity=_act(ledger, current_coordinates).identity,
    )
    prior = read_operator_current_coordinates(
        ledger, locality_identity=result.locality_identity
    )
    broken = deepcopy(prior)
    broken["recorded_boundary_locality_relations"] = [result.identity]
    with pytest.raises(ValueError, match="boundary Locality relations"):
        advance_operator_current_coordinates(
            ledger,
            (),
            locality_identity=result.locality_identity,
            prior=broken,
        )
