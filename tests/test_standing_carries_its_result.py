"""01.Standing.A.1 — the exact result is one coordinate of Standing for the
exact subject of its Responsibility branch.

Current Standing recorded only that a result occurrence was admitted.  The
Responsibility branch that yielded it, the exact subject that branch is for,
and the Book clause governing it were all resolved at the admission gate and
then discarded.  These witness that the ownership already carried by the
responsible Act evidence is preserved beside the result instead, and that a
result whose Act evidence records no such reference keeps no composed owner.
"""

from __future__ import annotations

from copy import deepcopy

import pytest

from seed_runtime.events import EventLedger, SQLiteEventLedger
from seed_runtime.operator_locality_standing import (
    _carry_operator_material_acquisition_occurrence_into_standing,
    advance_operator_locality_standing,
    read_operator_locality_standing,
)
from seed_runtime.witness_material_acquisition import (
    record_witness_material_acquisition,
)

from seed_runtime.operator_material_acquisition import (
    OperatorMaterialAcquireError,
    record_operator_material_acquire_responsibility_assignment,
    record_operator_material_acquire_responsible_act_evidence,
    record_operator_material_acquire_result,
)
from seed_runtime.operator_material_boundary import OperatorBoundaryMaterial
from seed_runtime.operator_representation import record_operator_representation

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
    act_evidence = ledger.get(
        result.material["responsible_act_evidence_identity"]
    )

    assert carried == act_evidence.material["responsibility_assignment_reference"]
    assert REQUIRED <= set(carried)


def test_the_carried_ownership_answers_branch_subject_and_clause_directly():
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


def test_one_Responsibility_branch_carries_each_admitted_result():
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


def test_the_ownership_survives_a_sqlite_close_and_reopen(tmp_path):
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
    """Substitution is refused where the Act evidence is read, not preserved.

    The ownership is never repaired into Standing: the responsible Act evidence
    stops being exact, so the Standing read refuses before any coordinate is
    carried beside the result.
    """

    ledger = EventLedger()
    result = _acquired(ledger)
    stored = ledger.get(result.material["responsible_act_evidence_identity"])

    mutated = deepcopy(stored.material)
    mutated["responsibility_assignment_reference"][coordinate] = "substituted"
    object.__setattr__(stored, "material", mutated)

    with pytest.raises(OperatorMaterialAcquireError):
        _ownership(ledger, "probe", result.identity)


def test_a_result_whose_evidence_records_no_reference_keeps_no_owner():
    """Absence of an established owner is recorded as absence, never composed."""

    ledger = EventLedger()
    acquired = record_witness_material_acquisition(
        ledger,
        locality_identity="witness",
        exact_bytes=b"\x00\xffprior\n",
        source_boundary="fixture boundary",
    )
    standing = read_operator_locality_standing(
        ledger, locality_identity="witness"
    )

    assert acquired.identity in standing["exact_result_occurrences"]
    assert standing["exact_result_occurrences"][acquired.identity] is None


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
    representation = record_operator_representation(
        ledger, locality_identity=locality, locality_standing=standing
    )
    standing = advance_operator_locality_standing(
        ledger,
        representation["recorded_occurrence_references"],
        locality_identity=locality,
        prior=standing,
    )
    assignment = record_operator_material_acquire_responsibility_assignment(
        ledger,
        locality_identity=locality,
        addressed_representation_event_identity=representation[
            "representation_event_identity"
        ],
        locality_standing=standing,
    )
    standing = _carry_operator_material_acquisition_occurrence_into_standing(
        ledger,
        standing,
        assignment,
        prior_through_event_occurrence_identity=representation[
            "representation_event_identity"
        ],
    )
    act_evidence = record_operator_material_acquire_responsible_act_evidence(
        ledger,
        responsibility_assignment_event_identity=assignment.identity,
        responsibility_assignment_standing=read_operator_locality_standing(
            ledger, locality_identity=locality
        ),
    )
    standing = _carry_operator_material_acquisition_occurrence_into_standing(
        ledger,
        standing,
        act_evidence,
        prior_through_event_occurrence_identity=assignment.identity,
    )
    result = record_operator_material_acquire_result(
        ledger,
        responsible_act_evidence_event_identity=act_evidence.identity,
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
        prior_through_event_occurrence_identity=act_evidence.identity,
    )

    replayed = read_operator_locality_standing(
        ledger, locality_identity=locality
    )

    assert (
        carried["exact_result_occurrences"]
        == replayed["exact_result_occurrences"]
    )
    assert carried["exact_result_occurrences"][result.identity] == (
        act_evidence.material["responsibility_assignment_reference"]
    )


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


PYTEST_ADMISSION = (
    test_the_admitted_result_carries_its_exact_Responsibility_ownership,
    test_the_carried_ownership_answers_branch_subject_and_clause_directly,
    test_one_Responsibility_branch_carries_each_admitted_result,
    test_a_complete_replay_produces_the_same_ownership,
    test_the_ownership_survives_a_sqlite_close_and_reopen,
    test_a_substituted_ownership_coordinate_is_refused,
    test_a_result_whose_evidence_records_no_reference_keeps_no_owner,
    test_live_incremental_carry_and_complete_replay_agree,
    test_the_carried_result_establishes_no_Standing_for_itself_as_a_subject,
)
