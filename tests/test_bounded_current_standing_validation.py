"""A Responsibility proves the Standing coordinates it consumes, not all of it.

`_current_standing` used to rebuild the complete Locality Standing and require
the supplied Standing to equal it whole.  That authenticated every sibling
branch this Responsibility never reads, and the rebuild is the full-Locality
replay.

The exact coordinates this Responsibility consumes are the source Measurement
result, its Locality, the Standing boundary, and the through occurrence.  Each
is validated against the ledger, so every refusal is kept while an unrelated
branch of the supplied Standing no longer has to be reconstructed to be
believed.
"""

from __future__ import annotations

from copy import deepcopy

import pytest

import seed_runtime.measurement_of_position_coordinates_of_byte_pair_occurrences as position_module
import seed_runtime.operator_locality_standing as standing_module
from seed_runtime.addressed_byte_occurrence_reference_determination import (
    AddressedByteOccurrenceReferenceDeterminationError,
    _current_standing,
    record_addressed_byte_occurrence_reference_determination_act_evidence,
)
from seed_runtime.events import EventLedger

from tests.operator_material_acquisition_test_witness import (
    record_operator_material_occurrence,
)
from tests.test_addressed_byte_occurrence_reference_determination import (
    _through_applicability,
)


def _position_material():
    """One exact source and the current Standing that carries it."""

    ledger = EventLedger()
    source = record_operator_material_occurrence(
        ledger,
        locality_identity="entrance-witness",
        exact=b"2+2=5\n",
        source_boundary="exact supplied material boundary",
    )
    return ledger, source, standing_module.read_operator_locality_standing(
        ledger, locality_identity="entrance-witness"
    )


def test_an_unrelated_branch_of_the_supplied_standing_is_not_authenticated():
    """The decisive witness: this Responsibility reads only what it consumes.

    A coordinate the determination never reads is changed in the supplied
    Standing.  The Responsibility must neither reconstruct the Locality to
    notice, nor refuse merely because the whole mapping now differs.
    """

    ledger = EventLedger()
    recorded = _through_applicability(ledger)

    unrelated = deepcopy(recorded["standing"])
    unrelated["representations"] = {"an unread sibling branch": None}

    determination_act = (
        record_addressed_byte_occurrence_reference_determination_act_evidence(
            ledger,
            applicability_result_event_identity=recorded["applicability"].identity,
            applicability_standing=unrelated,
        )
    )

    assert determination_act.identity


def test_a_substituted_through_occurrence_is_refused():
    ledger = EventLedger()
    recorded = _through_applicability(ledger)

    forged = deepcopy(recorded["standing"])
    forged["through_event_occurrence_identity"] = recorded["assignment"].identity

    with pytest.raises(AddressedByteOccurrenceReferenceDeterminationError):
        record_addressed_byte_occurrence_reference_determination_act_evidence(
            ledger,
            applicability_result_event_identity=recorded["applicability"].identity,
            applicability_standing=forged,
        )


def test_a_stale_standing_is_refused_at_the_append_tip():
    ledger = EventLedger()
    recorded = _through_applicability(ledger)

    stale = deepcopy(recorded["standing"])
    stale["through_event_occurrence_identity"] = recorded[
        "applicability_act"
    ].identity

    with pytest.raises(AddressedByteOccurrenceReferenceDeterminationError):
        record_addressed_byte_occurrence_reference_determination_act_evidence(
            ledger,
            applicability_result_event_identity=recorded["applicability"].identity,
            applicability_standing=stale,
        )


def test_a_substituted_source_measurement_result_is_refused():
    ledger = EventLedger()
    recorded = _through_applicability(ledger)

    forged = deepcopy(recorded["standing"])
    forged["measurement_occurrences"] = {"forged occurrence": {"not": "exact"}}

    with pytest.raises(AddressedByteOccurrenceReferenceDeterminationError):
        record_addressed_byte_occurrence_reference_determination_act_evidence(
            ledger,
            applicability_result_event_identity=recorded["applicability"].identity,
            applicability_standing=forged,
        )


def test_a_wrong_locality_in_the_supplied_standing_is_refused():
    ledger = EventLedger()
    recorded = _through_applicability(ledger)

    forged = deepcopy(recorded["standing"])
    forged["locality_identity"] = "another-locality"

    with pytest.raises(AddressedByteOccurrenceReferenceDeterminationError):
        record_addressed_byte_occurrence_reference_determination_act_evidence(
            ledger,
            applicability_result_event_identity=recorded["applicability"].identity,
            applicability_standing=forged,
        )


def test_a_standing_that_is_no_mapping_is_refused():
    ledger = EventLedger()
    recorded = _through_applicability(ledger)

    with pytest.raises(AddressedByteOccurrenceReferenceDeterminationError):
        record_addressed_byte_occurrence_reference_determination_act_evidence(
            ledger,
            applicability_result_event_identity=recorded["applicability"].identity,
            applicability_standing=["not", "a", "mapping"],
        )


def test_this_standing_validation_reconstructs_no_locality_standing(monkeypatch):
    """The full-Locality replay is gone from this validation.

    Bounded to the site this slice changed.  Other reconstruction sites remain
    on the wider determination road, notably the position-coordinate
    Measurement's own assignment read, and are not this slice's subject.
    """

    ledger = EventLedger()
    recorded = _through_applicability(ledger)

    calls = []

    def refuse(*arguments, **keywords):
        calls.append(keywords.get("locality_identity"))
        raise AssertionError("this validation reconstructed Locality Standing")

    monkeypatch.setattr(
        standing_module, "read_operator_locality_standing", refuse
    )
    monkeypatch.setattr(
        standing_module, "read_operator_locality_standing_through", refuse
    )

    validated = _current_standing(
        ledger,
        source_result=recorded["direct_result"],
        locality_standing=recorded["standing"],
    )

    assert validated is recorded["standing"]
    assert calls == []


def test_the_position_assignment_refuses_a_forged_standing_boundary():
    ledger, source, standing = _position_material()
    forged = deepcopy(standing)
    forged["through_event_occurrence_identity"] = "evt_absent"

    with pytest.raises(ValueError):
        position_module.record_byte_pair_occurrence_position_measurement_responsibility_assignment(
            ledger,
            source_material_acquisition_occurrence_identity=source.identity,
            locality_standing=forged,
        )


def test_the_position_assignment_authenticates_no_unread_branch():
    """One entrance, and it rebuilds no Locality to notice a sibling.

    A rebuilding entrance refuses here.  This records, so the validation reads
    only the coordinates the Responsibility consumes.
    """

    ledger, source, standing = _position_material()
    unread = deepcopy(standing)
    unread["representations"] = {"an unread sibling branch": None}

    assignment = position_module.record_byte_pair_occurrence_position_measurement_responsibility_assignment(
        ledger,
        source_material_acquisition_occurrence_identity=source.identity,
        locality_standing=unread,
    )

    assert assignment.identity


PYTEST_ADMISSION = (
    test_the_position_assignment_refuses_a_forged_standing_boundary,
    test_the_position_assignment_authenticates_no_unread_branch,
    test_an_unrelated_branch_of_the_supplied_standing_is_not_authenticated,
    test_a_substituted_through_occurrence_is_refused,
    test_a_stale_standing_is_refused_at_the_append_tip,
    test_a_substituted_source_measurement_result_is_refused,
    test_a_wrong_locality_in_the_supplied_standing_is_refused,
    test_a_standing_that_is_no_mapping_is_refused,
    test_this_standing_validation_reconstructs_no_locality_standing,
)
