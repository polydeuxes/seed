"""01.Current.A.1 reads an exact result with its subject-to-Act binding."""

from __future__ import annotations

from copy import deepcopy

import pytest

from seed_runtime.events import EventLedger, SQLiteEventLedger
from seed_runtime.operator_current_coordinates import (
    _advance_current_coordinates_with_operator_material_source_occurrence,
    _subject_to_act_binding_of_exact_result,
    advance_operator_current_coordinates,
    read_operator_current_coordinates,
)
from seed_runtime.operator_material_boundary import OperatorBoundaryMaterial
from seed_runtime.operator_material_source import (
    OperatorMaterialSourceError,
    record_operator_material_source_act_occurrence,
    record_operator_material_source_result,
    record_operator_material_source_subject_to_act_binding,
)
from seed_runtime.witness_material_source import record_witness_material_source
from tests.operator_material_source_test_witness import (
    record_operator_material_occurrence,
)


REQUIRED_BINDING_COORDINATES = {
    "recorded_occurrence_identity",
    "book_clause_identity",
    "exact_act_identity",
    "subject_reference",
    "result_boundary_identity",
}


def _recorded(ledger: EventLedger, locality: str = "probe", exact: bytes = b"abc"):
    return record_operator_material_occurrence(
        ledger,
        exact=exact,
        locality_identity=locality,
    )


def _current_result_binding(
    ledger: EventLedger, locality: str, result_identity: str
):
    current = read_operator_current_coordinates(
        ledger,
        locality_identity=locality,
    )
    return current["exact_result_occurrences"][result_identity]


def _mutate_act_occurrence(ledger: EventLedger, result, change):
    stored = ledger.get(result.material["act_occurrence_event_identity"])
    material = deepcopy(stored.material)
    change(material)
    object.__setattr__(stored, "material", material)


def test_current_result_carries_its_exact_subject_to_act_binding():
    ledger = EventLedger()
    result = _recorded(ledger)
    act_occurrence = ledger.get(result.material["act_occurrence_event_identity"])

    carried = _current_result_binding(ledger, "probe", result.identity)

    assert carried == act_occurrence.material[
        "subject_to_act_binding_reference"
    ]
    assert set(carried) == REQUIRED_BINDING_COORDINATES
    assert carried["book_clause_identity"] == "01.Source.G"
    assert carried["subject_reference"] == {
        "source_boundary": "operator boundary",
    }


def test_complete_replay_reads_the_same_result_binding():
    ledger = EventLedger()
    result = _recorded(ledger)

    current = read_operator_current_coordinates(ledger, locality_identity="probe")
    replayed = advance_operator_current_coordinates(
        ledger,
        [occurrence.identity for occurrence in ledger.list_locality("probe")],
        locality_identity="probe",
    )

    assert replayed["exact_result_occurrences"] == current[
        "exact_result_occurrences"
    ]
    assert replayed["exact_result_occurrences"][result.identity] is not None


def test_result_binding_remains_exact_after_sqlite_reopen(tmp_path):
    database = tmp_path / "current-result-binding.sqlite"
    ledger = SQLiteEventLedger(str(database))
    try:
        result = _recorded(ledger)
        before = _current_result_binding(ledger, "probe", result.identity)
    finally:
        ledger.close()

    reopened = SQLiteEventLedger(str(database))
    try:
        after = _current_result_binding(reopened, "probe", result.identity)
    finally:
        reopened.close()

    assert after == before


@pytest.mark.parametrize("coordinate", sorted(REQUIRED_BINDING_COORDINATES))
def test_changed_result_binding_coordinate_is_refused(coordinate):
    ledger = EventLedger()
    result = _recorded(ledger)

    def change(material):
        material["subject_to_act_binding_reference"][coordinate] = "changed"

    _mutate_act_occurrence(ledger, result, change)

    with pytest.raises((OperatorMaterialSourceError, ValueError)):
        _current_result_binding(ledger, "probe", result.identity)


def test_missing_result_binding_reference_adds_no_current_binding():
    ledger = EventLedger()
    result = _recorded(ledger)
    _mutate_act_occurrence(
        ledger,
        result,
        lambda material: material.pop("subject_to_act_binding_reference"),
    )

    assert _subject_to_act_binding_of_exact_result(ledger, result) is None


def test_witness_result_carries_its_recorded_binding():
    ledger = EventLedger()
    result = record_witness_material_source(
        ledger,
        locality_identity="witness",
        exact_bytes=b"\x00\xffprior\n",
        source_boundary="fixture boundary",
    )

    carried = _current_result_binding(ledger, "witness", result.identity)
    act_occurrence = ledger.get(result.material["act_occurrence_event_identity"])

    assert carried == act_occurrence.material[
        "subject_to_act_binding_reference"
    ]
    assert set(carried) == REQUIRED_BINDING_COORDINATES
    assert carried["book_clause_identity"] == "01.Source.H"
    assert carried["subject_reference"] == {
        "source_boundary": "fixture boundary",
    }


def test_incremental_carry_and_complete_replay_read_the_same_binding():
    ledger = EventLedger()
    locality = "incremental"
    current = read_operator_current_coordinates(
        ledger,
        locality_identity=locality,
    )
    binding = record_operator_material_source_subject_to_act_binding(
        ledger,
        locality_identity=locality,
        current_coordinates=current,
        source_boundary="operator boundary",
    )
    current = _advance_current_coordinates_with_operator_material_source_occurrence(
        ledger,
        current,
        binding,
        prior_through_event_occurrence_identity=None,
    )
    act_occurrence = record_operator_material_source_act_occurrence(
        ledger,
        subject_to_act_binding_event_identity=binding.identity,
        current_coordinates=current,
    )
    current = _advance_current_coordinates_with_operator_material_source_occurrence(
        ledger,
        current,
        act_occurrence,
        prior_through_event_occurrence_identity=binding.identity,
    )
    result = record_operator_material_source_result(
        ledger,
        act_occurrence_event_identity=act_occurrence.identity,
        boundary_material=OperatorBoundaryMaterial(
            exact_bytes=b"incremental",
            eof=False,
            material_boundary="operator boundary",
            known_loss=(),
        ),
    )
    carried = _advance_current_coordinates_with_operator_material_source_occurrence(
        ledger,
        current,
        result,
        prior_through_event_occurrence_identity=act_occurrence.identity,
    )
    replayed = read_operator_current_coordinates(
        ledger,
        locality_identity=locality,
    )

    assert carried["exact_result_occurrences"] == replayed[
        "exact_result_occurrences"
    ]
    assert carried["exact_result_occurrences"][result.identity] == (
        act_occurrence.material["subject_to_act_binding_reference"]
    )


@pytest.mark.parametrize(
    ("coordinate", "changed"),
    (
        ("known_loss", [1]),
    ),
)
def test_source_binding_refuses_nonexact_prior_lists_without_changing_coordinates(
    coordinate, changed
):
    ledger = EventLedger()
    locality = "incremental-refusal"
    current_coordinates = read_operator_current_coordinates(
        ledger,
        locality_identity=locality,
    )
    binding = record_operator_material_source_subject_to_act_binding(
        ledger,
        locality_identity=locality,
        current_coordinates=current_coordinates,
        source_boundary="operator boundary",
    )
    current_coordinates[coordinate] = changed
    before = deepcopy(current_coordinates)

    with pytest.raises(ValueError, match="coordinates are not exact"):
        _advance_current_coordinates_with_operator_material_source_occurrence(
            ledger,
            current_coordinates,
            binding,
            prior_through_event_occurrence_identity=None,
        )

    assert current_coordinates == before


def test_source_result_refusal_does_not_change_prior_current_coordinates():
    ledger = EventLedger()
    locality = "incremental-result-refusal"
    current_coordinates = read_operator_current_coordinates(
        ledger,
        locality_identity=locality,
    )
    binding = record_operator_material_source_subject_to_act_binding(
        ledger,
        locality_identity=locality,
        current_coordinates=current_coordinates,
        source_boundary="operator boundary",
    )
    current_coordinates = _advance_current_coordinates_with_operator_material_source_occurrence(
        ledger,
        current_coordinates,
        binding,
        prior_through_event_occurrence_identity=None,
    )
    act_occurrence = record_operator_material_source_act_occurrence(
        ledger,
        subject_to_act_binding_event_identity=binding.identity,
        current_coordinates=current_coordinates,
    )
    current_coordinates = _advance_current_coordinates_with_operator_material_source_occurrence(
        ledger,
        current_coordinates,
        act_occurrence,
        prior_through_event_occurrence_identity=binding.identity,
    )
    result = record_operator_material_source_result(
        ledger,
        act_occurrence_event_identity=act_occurrence.identity,
        boundary_material=OperatorBoundaryMaterial(
            exact_bytes=b"incremental",
            eof=False,
            material_boundary="operator boundary",
            known_loss=(),
        ),
    )
    malformed = deepcopy(result)
    del malformed.material["locality_relation"]
    before = deepcopy(current_coordinates)

    with pytest.raises(ValueError, match="result is not exact"):
        _advance_current_coordinates_with_operator_material_source_occurrence(
            ledger,
            current_coordinates,
            malformed,
            prior_through_event_occurrence_identity=act_occurrence.identity,
        )

    assert current_coordinates == before
