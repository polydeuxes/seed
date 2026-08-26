from __future__ import annotations

from copy import deepcopy
from io import BytesIO
from pathlib import Path

import pytest


from seed_runtime.events import CORRUPTED, EventLedger, SQLiteEventLedger
from seed_runtime.operator_checkpoint import (
    THROUGH_OCCURRENCE_BOUNDARY_REFERENCE_RECORDED_KIND,
    get_recorded_through_occurrence_boundary_reference,
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
    RECORDED_BOUNDARY_LOCALITY_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
    RecordedBoundaryLocalityError,
    get_recorded_boundary_locality,
    record_recorded_boundary_locality_subject_to_act_binding,
    record_recorded_boundary_locality_act_occurrence,
    record_recorded_boundary_locality_result,
)
from seed_runtime.yield_relation import read_requirements_of_yield_relation


def _command(exact_bytes=b"/checkout\n", arguments=b""):
    return AddressedOperatorCommand(
        command_identity="command",
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


def _coordinates_with_through_occurrence_reference(ledger, *, locality="source"):
    run_persistent_operator_console(
        ledger=ledger,
        locality_identity=locality,
        input_stream=BytesIO(b"/checkpoint\n"),
    )
    reference_result = next(
        event
        for event in ledger.list_locality(locality)
        if event.kind == THROUGH_OCCURRENCE_BOUNDARY_REFERENCE_RECORDED_KIND
    )
    return reference_result, read_operator_current_coordinates(
        ledger, locality_identity=locality
    )


def _binding(ledger, current_coordinates):
    return record_recorded_boundary_locality_subject_to_act_binding(
        ledger, source_current_coordinates=current_coordinates
    )


def _act(ledger, binding):
    current_coordinates = read_operator_current_coordinates(
        ledger, locality_identity=binding.locality_identity
    )
    return record_recorded_boundary_locality_act_occurrence(
        ledger,
        subject_to_act_binding_event_identity=binding.identity,
        current_coordinates=current_coordinates,
    )


@pytest.mark.parametrize("exact", (b"/checkout", b"/checkout\n", b"/checkout\r\n"))
def test_checkout_request_is_exact_argument_free_operator_control(exact):
    assert request_operator_checkout(_command(exact)) == OperatorCheckoutRequest()


@pytest.mark.parametrize("exact", (b"/checkout x\n", b"/checkout \n"))
def test_checkout_request_refuses_payload(exact):
    with pytest.raises(ValueError, match="accepts no material"):
        request_operator_checkout(_command(exact, b"x"))


def test_three_stage_relation_uses_one_reference_and_one_destination_locality():
    ledger = EventLedger()
    reference_result, source_coordinates = _coordinates_with_through_occurrence_reference(ledger)
    binding = _binding(ledger, source_coordinates)
    destination = binding.locality_identity
    after_binding = read_operator_current_coordinates(
        ledger, locality_identity=destination
    )
    act = record_recorded_boundary_locality_act_occurrence(
        ledger,
        subject_to_act_binding_event_identity=binding.identity,
        current_coordinates=after_binding,
    )
    before_result = read_operator_current_coordinates(
        ledger, locality_identity=destination
    )
    result = record_recorded_boundary_locality_result(
        ledger, act_occurrence_event_identity=act.identity
    )
    recorded = get_recorded_boundary_locality(ledger, result.identity)

    assert binding.kind == (
        RECORDED_BOUNDARY_LOCALITY_SUBJECT_TO_ACT_BINDING_RECORDED_KIND
    )
    assert "through_occurrence_boundary_reference" not in binding.material
    assert "destination_locality_identity" not in binding.material
    assert binding.material["subject_reference"] == binding.material["scope"][
        "through_occurrence_boundary_reference"
    ]
    assert binding.material["scope"]["destination_locality_identity"] == destination
    assert act.kind == RECORDED_BOUNDARY_LOCALITY_ACT_OCCURRENCE_EVENT
    assert result.kind == RECORDED_BOUNDARY_LOCALITY_RECORDED_KIND
    assert destination != "source"
    assert recorded["through_occurrence_boundary_reference"] == {
        "recorded_occurrence_identity": reference_result.identity,
        "result_identity": reference_result.material["result_identity"],
    }
    assert recorded["locality_relation"] == {
        "first_subject": recorded["through_occurrence_boundary_reference"],
        "second_subject": destination,
        "relation_occurrence_identity": recorded[
            "locality_relation_occurrence_identity"
        ],
    }
    assert len(
        {
            binding.identity,
            binding.material["exact_act_identity"],
            binding.material["act_occurrence_identity"],
            binding.material["locality_relation_occurrence_identity"],
            binding.material["result_identity"],
            act.identity,
            result.identity,
            result.material["yield_relation_identity"],
        }
    ) == 8
    assert read_requirements_of_yield_relation(
        ledger,
        recorded_result_event_identity=result.identity,
        yield_relation_event_identity=result.material["yield_relation_identity"],
        act_occurrence_event_identity=act.identity,
    ) == {
        "exact_relation": True,
        "occurrence_witness": True,
        "intact_occurrence": True,
    }
    carried = advance_operator_current_coordinates(
        ledger,
        (result.material["yield_relation_identity"], result.identity),
        locality_identity=destination,
        prior=before_result,
    )
    replayed = read_operator_current_coordinates(
        ledger, locality_identity=destination
    )
    assert carried == replayed
    assert replayed["recorded_boundary_locality_relations"] == {
        result.identity: None
    }
    assert replayed["locality_continuation_relation_occurrences"] == {}
    assert replayed["recorded_through_occurrence_boundary_references"] == {}


def test_relation_descendants_carry_one_exact_reference():
    ledger = EventLedger()
    reference_result, source_coordinates = _coordinates_with_through_occurrence_reference(ledger)
    first = record_recorded_boundary_locality_result(
        ledger,
        act_occurrence_event_identity=_act(
            ledger, _binding(ledger, source_coordinates)
        ).identity,
    )
    first_coordinates = read_operator_current_coordinates(
        ledger, locality_identity=first.locality_identity
    )
    second = record_recorded_boundary_locality_result(
        ledger,
        act_occurrence_event_identity=_act(
            ledger, _binding(ledger, first_coordinates)
        ).identity,
    )
    relations = [first, second]
    assert len(relations) == 2
    assert relations[0].locality_identity != relations[1].locality_identity
    expected = {
        "recorded_occurrence_identity": reference_result.identity,
        "result_identity": reference_result.material["result_identity"],
    }
    assert [
        get_recorded_boundary_locality(ledger, relation.identity)[
            "through_occurrence_boundary_reference"
        ]
        for relation in relations
    ] == [expected, expected]
    before = get_recorded_through_occurrence_boundary_reference(ledger, reference_result.identity)
    assert get_recorded_through_occurrence_boundary_reference(ledger, reference_result.identity) == before


def test_zero_and_two_carried_references_both_refuse_selection():
    ledger = EventLedger()
    empty = read_operator_current_coordinates(ledger, locality_identity="source")
    with pytest.raises(
        RecordedBoundaryLocalityError, match="exactly one carried reference"
    ):
        _binding(ledger, empty)

    run_persistent_operator_console(
        ledger=ledger,
        locality_identity="source",
        input_stream=BytesIO(b"/checkpoint\n/checkpoint\n"),
    )
    ambiguous = read_operator_current_coordinates(
        ledger, locality_identity="source"
    )
    with pytest.raises(
        RecordedBoundaryLocalityError, match="exactly one carried reference"
    ):
        _binding(ledger, ambiguous)


def test_different_locality_or_corrupted_reference_refuses_before_destination_write():
    ledger = _IntegrityAdversaryLedger()
    reference_result, current_coordinates = _coordinates_with_through_occurrence_reference(ledger)
    different_locality = deepcopy(current_coordinates)
    different_locality["locality_identity"] = "elsewhere"
    before = tuple(ledger.list())
    with pytest.raises(RecordedBoundaryLocalityError, match="different"):
        _binding(ledger, different_locality)
    assert tuple(ledger.list()) == before

    ledger.corrupted.add(reference_result.identity)
    with pytest.raises(ValueError, match="corrupted"):
        _binding(ledger, current_coordinates)
    assert tuple(ledger.list()) == before


def test_one_relation_act_cannot_yield_twice():
    ledger = EventLedger()
    _reference_result, current_coordinates = (
        _coordinates_with_through_occurrence_reference(ledger)
    )
    act = _act(ledger, _binding(ledger, current_coordinates))
    record_recorded_boundary_locality_result(
        ledger, act_occurrence_event_identity=act.identity
    )
    with pytest.raises(
        RecordedBoundaryLocalityError, match="already carries a Yield"
    ):
        record_recorded_boundary_locality_result(
            ledger, act_occurrence_event_identity=act.identity
        )


@pytest.mark.parametrize(
    "coordinate",
    (
        "through_occurrence_boundary_reference",
        "destination_locality_identity",
        "locality_relation",
        "participation",
        "subject_to_act_binding_reference",
        "scope",
        "unknown",
        "yield_relation_identity",
    ),
)
def test_changed_relation_result_coordinates_are_refused(coordinate):
    ledger = EventLedger()
    _reference_result, current_coordinates = (
        _coordinates_with_through_occurrence_reference(ledger)
    )
    act = _act(ledger, _binding(ledger, current_coordinates))
    result = record_recorded_boundary_locality_result(
        ledger, act_occurrence_event_identity=act.identity
    )
    ledger.get(result.identity).material[coordinate] = "different"
    with pytest.raises((RecordedBoundaryLocalityError, TypeError, ValueError)):
        get_recorded_boundary_locality(ledger, result.identity)


def test_reference_and_relation_survive_restart_without_copying_source_history(
    tmp_path,
):
    path = tmp_path / "checkout.sqlite"
    ledger = SQLiteEventLedger(str(path))
    reference_result, current_coordinates = _coordinates_with_through_occurrence_reference(ledger)
    first = record_recorded_boundary_locality_result(
        ledger,
        act_occurrence_event_identity=_act(
            ledger, _binding(ledger, current_coordinates)
        ).identity,
    )
    ledger.close()

    ledger = SQLiteEventLedger(str(path))
    first_coordinates = read_operator_current_coordinates(
        ledger, locality_identity=first.locality_identity
    )
    second = record_recorded_boundary_locality_result(
        ledger,
        act_occurrence_event_identity=_act(
            ledger, _binding(ledger, first_coordinates)
        ).identity,
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
        act_occurrence_event_identity=_act(
            ledger, _binding(ledger, current_coordinates)
        ).identity,
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
        act_occurrence_event_identity=_act(
            ledger, _binding(ledger, current_coordinates)
        ).identity,
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
