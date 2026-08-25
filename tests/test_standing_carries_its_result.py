"""01.Current.A.1 — the exact result is one coordinate of Standing for the
exact subject of its Responsibility.

Current Standing recorded only that a result occurrence was admitted.  The
Responsibility that yielded it, its exact subject, and the Book clause
governing it were all resolved at the admission gate and
then discarded.  These witness that the ownership already carried by the
responsible Act occurrence is preserved beside the result instead, and that a
result whose Act occurrence records no such reference keeps no composed owner.
"""

from __future__ import annotations

from copy import deepcopy

import pytest

from seed_runtime.events import EventLedger, SQLiteEventLedger
from seed_runtime.operator_locality_standing import (
    _carry_operator_material_acquisition_occurrence_into_standing,
    _responsibility_ownership_of_exact_result,
    advance_operator_locality_standing,
    read_operator_locality_standing,
)
from seed_runtime.witness_material_source import (
    record_witness_material_source,
)

from seed_runtime.operator_material_acquisition import (
    OperatorMaterialAcquireError,
    record_operator_material_acquire_responsibility_assignment,
    record_operator_material_acquire_act_occurrence,
    record_operator_material_acquire_result,
)
from seed_runtime.operator_material_boundary import OperatorBoundaryMaterial
from tests.operator_material_acquisition_test_witness import (
    record_operator_material_occurrence,
)

REQUIRED = {
    "recorded_occurrence_identity",
    "assignment_identity",
    "assignment_subject_identity",
    "book_clause_identity",
    "result_boundary_identity",
}


def _acquired(ledger: EventLedger, locality: str = "probe", exact: bytes = b"abc"):
    return record_operator_material_occurrence(
        ledger, exact=exact, locality_identity=locality
    )


def _ownership(ledger: EventLedger, locality: str, result_identity: str):
    standing = read_operator_locality_standing(
        ledger, locality_identity=locality
    )
    return standing["exact_result_occurrences"][result_identity]


def test_the_admitted_result_carries_its_exact_Responsibility_ownership():
    ledger = EventLedger()
    result = _acquired(ledger)

    carried = _ownership(ledger, "probe", result.identity)
    act_occurrence = ledger.get(
        result.material["act_occurrence_event_identity"]
    )

    assert carried == act_occurrence.material["responsibility_assignment_reference"]
    assert REQUIRED <= set(carried)


def test_the_carried_ownership_answers_subject_and_clause_directly():
    """Answered from the result's own coordinate, reconstructing no Standing."""

    ledger = EventLedger()
    result = _acquired(ledger)
    standing = read_operator_locality_standing(ledger, locality_identity="probe")

    carried = standing["exact_result_occurrences"][result.identity]

    assert carried["assignment_identity"]
    assert carried["assignment_subject_identity"]
    assert carried["book_clause_identity"] == "01.Source.G"
    assert (
        carried["recorded_occurrence_identity"]
        in standing["responsibility_assignment_occurrences"]
    )


def test_one_Responsibility_carries_each_admitted_result():
    ledger = EventLedger()
    first = _acquired(ledger, locality="one", exact=b"first")
    second = _acquired(ledger, locality="two", exact=b"second")

    owners = {
        first.identity: _ownership(ledger, "one", first.identity),
        second.identity: _ownership(ledger, "two", second.identity),
    }

    assert all(type(o["assignment_identity"]) is str for o in owners.values())
    assert (
        owners[first.identity]["assignment_identity"]
        != owners[second.identity]["assignment_identity"]
    )


def test_a_complete_replay_produces_the_same_ownership():
    ledger = EventLedger()
    result = _acquired(ledger)

    read = read_operator_locality_standing(ledger, locality_identity="probe")
    replayed = advance_operator_locality_standing(
        ledger,
        [occurrence.identity for occurrence in ledger.list_locality("probe")],
        locality_identity="probe",
    )

    assert (
        replayed["exact_result_occurrences"] == read["exact_result_occurrences"]
    )
    assert replayed["exact_result_occurrences"][result.identity] is not None


def test_the_ownership_is_recovered_after_a_sqlite_close_and_reopen(tmp_path):
    database = tmp_path / "standing-carries-result.sqlite"
    ledger = SQLiteEventLedger(str(database))
    try:
        result = _acquired(ledger)
        before = _ownership(ledger, "probe", result.identity)
    finally:
        ledger.close()

    reopened = SQLiteEventLedger(str(database))
    try:
        after = _ownership(reopened, "probe", result.identity)
    finally:
        reopened.close()

    assert before is not None
    assert after == before


@pytest.mark.parametrize("coordinate", sorted(REQUIRED))
def test_a_substituted_ownership_coordinate_is_refused(coordinate):
    """Substitution is refused where the Act occurrence is read, not preserved.

    The ownership is never repaired into Standing: the responsible Act occurrence
    stops being exact, so the Standing read refuses before any coordinate is
    carried beside the result.
    """

    ledger = EventLedger()
    result = _acquired(ledger)
    stored = ledger.get(result.material["act_occurrence_event_identity"])

    mutated = deepcopy(stored.material)
    mutated["responsibility_assignment_reference"][coordinate] = "substituted"
    object.__setattr__(stored, "material", mutated)

    with pytest.raises(OperatorMaterialAcquireError):
        _ownership(ledger, "probe", result.identity)


def test_a_result_whose_act_occurrence_records_no_reference_has_no_A1_coordinate():
    """Absence of an owner is no positive A.1 coordinate, never ``None``."""

    ledger = EventLedger()
    acquired = record_witness_material_source(
        ledger,
        locality_identity="witness",
        exact_bytes=b"\x00\xffprior\n",
        source_boundary="fixture boundary",
    )
    standing = read_operator_locality_standing(
        ledger, locality_identity="witness"
    )

    assert acquired.identity not in standing["exact_result_occurrences"]


def test_live_incremental_carry_and_complete_replay_agree():
    """The console carries occurrences one at a time; replay reads them all.

    Both reach current Standing, so both must carry the same ownership beside
    the same result.  This is the equivalence the third admission site would
    have broken while the other two preserved it.
    """

    ledger = EventLedger()
    locality = "incremental"

    standing = read_operator_locality_standing(
        ledger, locality_identity=locality
    )
    assignment = record_operator_material_acquire_responsibility_assignment(
        ledger,
        locality_identity=locality,
        locality_standing=standing,
    )
    standing = _carry_operator_material_acquisition_occurrence_into_standing(
        ledger,
        standing,
        assignment,
        prior_through_event_occurrence_identity=None,
    )
    act_occurrence = record_operator_material_acquire_act_occurrence(
        ledger,
        responsibility_assignment_event_identity=assignment.identity,
        responsibility_assignment_standing=read_operator_locality_standing(
            ledger, locality_identity=locality
        ),
    )
    standing = _carry_operator_material_acquisition_occurrence_into_standing(
        ledger,
        standing,
        act_occurrence,
        prior_through_event_occurrence_identity=assignment.identity,
    )
    result = record_operator_material_acquire_result(
        ledger,
        act_occurrence_event_identity=act_occurrence.identity,
        boundary_material=OperatorBoundaryMaterial(
            exact_bytes=b"incremental",
            eof=False,
            material_boundary="operator boundary",
            known_loss=(),
        ),
    )
    carried = _carry_operator_material_acquisition_occurrence_into_standing(
        ledger,
        standing,
        result,
        prior_through_event_occurrence_identity=act_occurrence.identity,
    )

    replayed = read_operator_locality_standing(
        ledger, locality_identity=locality
    )

    assert (
        carried["exact_result_occurrences"]
        == replayed["exact_result_occurrences"]
    )
    assert carried["exact_result_occurrences"][result.identity] == (
        act_occurrence.material["responsibility_assignment_reference"]
    )


def _ownership_of(ledger: EventLedger, result):
    return _responsibility_ownership_of_exact_result(ledger, result)


def _mutate_act_occurrence(ledger: EventLedger, result, change):
    stored = ledger.get(result.material["act_occurrence_event_identity"])
    material = deepcopy(stored.material)
    change(material)
    object.__setattr__(stored, "material", material)
    return stored


def test_ownership_present_but_incomplete_is_refused_not_read_as_absent():
    """A recorded reference missing a coordinate is not a result without owner."""

    ledger = EventLedger()
    result = _acquired(ledger)
    _mutate_act_occurrence(
        ledger,
        result,
        lambda material: material["responsibility_assignment_reference"].pop(
            "assignment_subject_identity"
        ),
    )

    with pytest.raises(ValueError, match="exact coordinates"):
        _ownership_of(ledger, result)


def test_ownership_that_is_not_a_coordinate_mapping_is_refused():
    ledger = EventLedger()
    result = _acquired(ledger)
    _mutate_act_occurrence(
        ledger,
        result,
        lambda material: material.__setitem__(
            "responsibility_assignment_reference", "not a mapping"
        ),
    )

    with pytest.raises(ValueError, match="exact coordinates"):
        _ownership_of(ledger, result)


def test_ownership_naming_an_absent_assignment_is_refused():
    ledger = EventLedger()
    result = _acquired(ledger)
    _mutate_act_occurrence(
        ledger,
        result,
        lambda material: material["responsibility_assignment_reference"].__setitem__(
            "recorded_occurrence_identity", "evt_absent"
        ),
    )

    with pytest.raises(ValueError, match="exact assignment"):
        _ownership_of(ledger, result)


@pytest.mark.parametrize(
    "coordinate",
    [
        "assignment_identity",
        "assignment_subject_identity",
        "book_clause_identity",
        "result_boundary_identity",
    ],
)
def test_ownership_disagreeing_with_its_assignment_is_refused(coordinate):
    """A syntactically whole reference cannot substitute ownership or subject.

    The named assignment owns these coordinates, so a carried value that does
    not agree with the recorded assignment is refused rather than preserved.
    """

    ledger = EventLedger()
    result = _acquired(ledger)
    _mutate_act_occurrence(
        ledger,
        result,
        lambda material: material["responsibility_assignment_reference"].__setitem__(
            coordinate, "substituted-but-well-formed"
        ),
    )

    with pytest.raises(ValueError, match="disagrees with its assignment"):
        _ownership_of(ledger, result)


def test_a_result_with_no_recorded_reference_is_still_no_owner_not_a_refusal():
    """Absence stays absence; only a recorded reference must be exact."""

    ledger = EventLedger()
    result = _acquired(ledger)
    _mutate_act_occurrence(
        ledger,
        result,
        lambda material: material.pop("responsibility_assignment_reference"),
    )

    assert _ownership_of(ledger, result) is None


def test_the_carried_result_establishes_no_Standing_for_itself_as_a_subject():
    ledger = EventLedger()
    result = _acquired(ledger)
    standing = read_operator_locality_standing(ledger, locality_identity="probe")

    carried = standing["exact_result_occurrences"][result.identity]

    assert result.identity not in standing[
        "responsibility_assignment_occurrences"
    ]
    assert carried["assignment_subject_identity"] != result.identity
    assert carried["recorded_occurrence_identity"] != result.identity
