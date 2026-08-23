"""Distinguish append boundary, Locality projection, branch, subject and result.

The active Book says that one Responsibility branch of current Standing carries
its exact result as a coordinate of Standing for that branch's exact subject.
The live reader is named ``operator_locality_standing``, while the ledger has a
separate immutable append-prefix boundary.  This observer makes those addresses
visible without treating either implementation representation as constitutional
law.

It records one ordinary, fully owned material-acquisition result in each of two
Localities.  Appending the second occurrence changes the ledger's global append
boundary but cannot change the first Locality's source-derived projection.  It
then records another result in the first Locality and shows that its projection
grows while retaining the earlier independently owned branch/result coordinate.

Usage:
    .venv/bin/python scripts/observe_standing_subject_boundary.py
"""

from __future__ import annotations

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from seed_runtime.events import EventLedger
from seed_runtime.operator_locality_standing import read_operator_locality_standing
from tests.operator_material_acquisition_test_witness import (
    record_operator_material_occurrence,
)


def _owned_results(standing: dict) -> dict:
    return {
        identity: owner
        for identity, owner in standing["exact_result_occurrences"].items()
        if owner is not None
    }


def main() -> int:
    ledger = EventLedger()

    empty = read_operator_locality_standing(
        ledger, locality_identity="first-locality"
    )
    first = record_operator_material_occurrence(
        ledger,
        locality_identity="first-locality",
        exact=b"first",
        source_boundary="first exact observer boundary",
    )
    boundary_after_first = ledger.append_boundary()
    first_at_first_boundary = read_operator_locality_standing(
        ledger, locality_identity="first-locality"
    )

    second = record_operator_material_occurrence(
        ledger,
        locality_identity="second-locality",
        exact=b"second",
        source_boundary="second exact observer boundary",
    )
    boundary_after_second = ledger.append_boundary()
    first_after_other_locality = read_operator_locality_standing(
        ledger, locality_identity="first-locality"
    )
    second_standing = read_operator_locality_standing(
        ledger, locality_identity="second-locality"
    )

    third = record_operator_material_occurrence(
        ledger,
        locality_identity="first-locality",
        exact=b"third",
        source_boundary="third exact observer boundary",
    )
    first_after_own_append = read_operator_locality_standing(
        ledger, locality_identity="first-locality"
    )

    assert boundary_after_first != boundary_after_second
    assert first_at_first_boundary == first_after_other_locality
    assert first.identity in _owned_results(first_at_first_boundary)
    assert second.identity in _owned_results(second_standing)
    assert first.identity in _owned_results(first_after_own_append)
    assert third.identity in _owned_results(first_after_own_append)
    assert (
        first_at_first_boundary["through_event_occurrence_identity"]
        == first_after_other_locality["through_event_occurrence_identity"]
    )
    assert (
        first_after_own_append["through_event_occurrence_identity"]
        == third.identity
    )

    empty_populations = {
        key: len(value)
        for key, value in empty.items()
        if isinstance(value, (dict, list))
    }
    first_owner = _owned_results(first_at_first_boundary)[first.identity]
    third_owner = _owned_results(first_after_own_append)[third.identity]
    first_through_changed = (
        first_at_first_boundary["through_event_occurrence_identity"]
        != first_after_other_locality["through_event_occurrence_identity"]
    )

    print("  empty first-Locality projection")
    print(f"    through occurrence: {empty['through_event_occurrence_identity']}")
    print(f"    event count:        {empty['event_count']}")
    print(
        "    nonempty carried populations: "
        f"{sum(count > 0 for count in empty_populations.values())}"
    )
    print()
    print("  one exact owned result in the first Locality")
    print(f"    result occurrence:  {first.identity}")
    print(f"    branch occurrence:  {first_owner['recorded_occurrence_identity']}")
    print(f"    exact subject:       {first_owner['assignment_subject_identity']}")
    print(f"    Book clause:         {first_owner['book_clause_identity']}")
    print()
    print("  another Locality advances the global append prefix")
    print(
        "    append boundary changed: "
        f"{boundary_after_first.identity != boundary_after_second.identity}"
    )
    print(
        "    first Locality projection changed: "
        f"{first_at_first_boundary != first_after_other_locality}"
    )
    print(
        "    first Locality through occurrence changed: "
        f"{first_through_changed}"
    )
    print()
    print("  another result in the first Locality")
    print(
        "    first result retained: "
        f"{first.identity in first_after_own_append['exact_result_occurrences']}"
    )
    print(f"    later result:         {third.identity}")
    print(f"    later branch:         {third_owner['recorded_occurrence_identity']}")
    print(f"    later exact subject:  {third_owner['assignment_subject_identity']}")
    print(
        "    owned result coordinates: "
        f"{len(_owned_results(first_after_own_append))}"
    )
    print()
    print(
        "  The append prefix, the Locality-bounded projection, each exact\n"
        "  Responsibility branch, the branch's subject, and its result are five\n"
        "  separately addressable implementation surfaces. This observer states\n"
        "  no generic Standing movement or replacement relation among them."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
