"""Validate only exact current coordinates read by one operation.

The validation previously rebuilt every coordinate current in one Locality and
required the supplied projection to equal that reconstruction. The operation
reads only the source Measurement result, Locality, and exact through
occurrence. Each remains independently checked while an unrelated coordinate
requires no reconstruction.
"""

from __future__ import annotations

from copy import deepcopy

import pytest

import seed_runtime.measurement_of_position_coordinates_of_byte_pair_occurrences as position_module
import seed_runtime.operator_current_coordinates as coordinate_module
from seed_runtime.addressed_byte_occurrence_reference_determination import (
    AddressedByteOccurrenceReferenceDeterminationError,
    _current_standing,
    record_addressed_byte_occurrence_reference_determination_act_occurrence,
)
from seed_runtime.events import EventLedger

from tests.operator_material_source_test_witness import (
    record_operator_material_occurrence,
)
from tests.test_addressed_byte_occurrence_reference_determination import (
    _through_applicability,
)


def _position_material():
    """One exact source and the current coordinates that carry it."""

    ledger = EventLedger()
    source = record_operator_material_occurrence(
        ledger,
        locality_identity="entrance-witness",
        exact=b"2+2=5\n",
        source_boundary="exact supplied material boundary",
    )
    return ledger, source, coordinate_module.read_operator_current_coordinates(
        ledger, locality_identity="entrance-witness"
    )


def test_an_unread_coordinate_does_not_require_full_locality_reconstruction():

    ledger = EventLedger()
    recorded = _through_applicability(ledger)

    unrelated = deepcopy(recorded["standing"])
    unrelated["representations"] = {"an unread sibling branch": None}

    determination_act = (
        record_addressed_byte_occurrence_reference_determination_act_occurrence(
            ledger,
            applicability_result_event_identity=recorded["applicability"].identity,
            applicability_standing=unrelated,
        )
    )

    assert determination_act.identity


def test_a_changed_through_occurrence_is_refused():
    ledger = EventLedger()
    recorded = _through_applicability(ledger)

    changed = deepcopy(recorded["standing"])
    changed["through_event_occurrence_identity"] = recorded["assignment"].identity

    with pytest.raises(AddressedByteOccurrenceReferenceDeterminationError):
        record_addressed_byte_occurrence_reference_determination_act_occurrence(
            ledger,
            applicability_result_event_identity=recorded["applicability"].identity,
            applicability_standing=changed,
        )


def test_earlier_current_coordinates_are_refused_at_the_append_tip():
    ledger = EventLedger()
    recorded = _through_applicability(ledger)

    stale = deepcopy(recorded["standing"])
    stale["through_event_occurrence_identity"] = recorded[
        "applicability_act"
    ].identity

    with pytest.raises(AddressedByteOccurrenceReferenceDeterminationError):
        record_addressed_byte_occurrence_reference_determination_act_occurrence(
            ledger,
            applicability_result_event_identity=recorded["applicability"].identity,
            applicability_standing=stale,
        )


def test_a_changed_source_measurement_result_is_refused():
    ledger = EventLedger()
    recorded = _through_applicability(ledger)

    changed = deepcopy(recorded["standing"])
    changed["measurement_occurrences"] = {"changed occurrence": {"not": "exact"}}

    with pytest.raises(AddressedByteOccurrenceReferenceDeterminationError):
        record_addressed_byte_occurrence_reference_determination_act_occurrence(
            ledger,
            applicability_result_event_identity=recorded["applicability"].identity,
            applicability_standing=changed,
        )


def test_a_changed_locality_in_supplied_coordinates_is_refused():
    ledger = EventLedger()
    recorded = _through_applicability(ledger)

    changed = deepcopy(recorded["standing"])
    changed["locality_identity"] = "another-locality"

    with pytest.raises(AddressedByteOccurrenceReferenceDeterminationError):
        record_addressed_byte_occurrence_reference_determination_act_occurrence(
            ledger,
            applicability_result_event_identity=recorded["applicability"].identity,
            applicability_standing=changed,
        )


def test_supplied_coordinates_that_are_no_mapping_are_refused():
    ledger = EventLedger()
    recorded = _through_applicability(ledger)

    with pytest.raises(AddressedByteOccurrenceReferenceDeterminationError):
        record_addressed_byte_occurrence_reference_determination_act_occurrence(
            ledger,
            applicability_result_event_identity=recorded["applicability"].identity,
            applicability_standing=["not", "a", "mapping"],
        )


def test_this_validation_performs_no_full_locality_read(monkeypatch):

    ledger = EventLedger()
    recorded = _through_applicability(ledger)

    calls = []

    def refuse(*arguments, **keywords):
        calls.append(keywords.get("locality_identity"))
        raise AssertionError("this validation performed a full Locality read")

    monkeypatch.setattr(
        coordinate_module, "read_operator_current_coordinates", refuse
    )
    monkeypatch.setattr(
        coordinate_module, "read_operator_current_coordinates_through", refuse
    )

    validated = _current_standing(
        ledger,
        source_result=recorded["direct_result"],
        locality_standing=recorded["standing"],
    )

    assert validated is recorded["standing"]
    assert calls == []


def test_the_position_binding_refuses_a_changed_through_occurrence():
    ledger, source, current_coordinates = _position_material()
    changed = deepcopy(current_coordinates)
    changed["through_event_occurrence_identity"] = "evt_absent"

    with pytest.raises(ValueError):
        position_module.record_byte_pair_occurrence_position_measurement_subject_to_act_binding(
            ledger,
            source_material_result_occurrence_identity=source.identity,
            current_coordinates=changed,
        )


def test_the_position_binding_reads_no_unrelated_coordinate():
    ledger, source, current_coordinates = _position_material()
    unread = deepcopy(current_coordinates)
    unread["representations"] = {"an unread sibling branch": None}

    binding = position_module.record_byte_pair_occurrence_position_measurement_subject_to_act_binding(
        ledger,
        source_material_result_occurrence_identity=source.identity,
        current_coordinates=unread,
    )

    assert binding.identity
