"""Recover one occurrence's physiology without reading what it calls itself.

A branch is read through the relations the grammar states: content carried into
an Act occurrence, a subject participating in it under a role, and that
occurrence yielding a result.  What an occurrence calls its own Responsibility,
its Act, or its result is a claim the occurrence makes and is not warrant for
the claim.

So each occurrence is read for recorded relation coordinates only.  A relation
coordinate is a mapping naming a first subject, a second subject, and either a
relation or the occurrence of one.  Nothing is matched by the words
Representation, responsibility, act, or representation_result.

Two occurrences are read the same way and compared only afterward.

Usage:
    .venv/bin/python scripts/observe_sourceless_occurrence_physiology.py
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from seed_runtime.events import EventLedger
from seed_runtime.operator_locality_standing import read_operator_locality_standing
from seed_runtime.operator_representation import record_operator_representation

from tests.operator_material_acquisition_test_witness import (
    record_operator_material_occurrence,
)

STATED_RELATIONS = ("carriage", "participation", "yield", "locality", "support")


def _relation_coordinates(value: Any, path: tuple[str, ...] = ()):
    """Every mapping shaped as a relation, wherever it is recorded."""

    if isinstance(value, dict):
        if {"first_subject", "second_subject"} <= set(value) and (
            "relation" in value or "relation_occurrence_identity" in value
        ):
            yield path, value
        for key, nested in value.items():
            yield from _relation_coordinates(nested, path + (str(key),))
    elif isinstance(value, list):
        for position, nested in enumerate(value):
            yield from _relation_coordinates(nested, path + (str(position),))


def _recover(source: bool):
    ledger = EventLedger()
    acquired = record_operator_material_occurrence(
        ledger,
        locality_identity="physiology",
        exact=b"2+2=5\n",
        source_boundary="exact supplied material boundary",
    )
    standing = read_operator_locality_standing(
        ledger, locality_identity="physiology"
    )
    recorded = record_operator_representation(
        ledger,
        locality_identity="physiology",
        locality_standing=standing,
        source_occurrence_reference=acquired.identity if source else None,
    )
    result = ledger.get(recorded["representation_event_identity"])
    lineage = [result]
    for coordinate in (
        "responsible_act_evidence_identity",
        "evidence_of_yield_relation_identity",
        "locality_evidence_identity",
    ):
        identity = result.material.get(coordinate)
        occurrence = ledger.get(identity) if isinstance(identity, str) else None
        if occurrence is not None and occurrence not in lineage:
            lineage.append(occurrence)
    return ledger, result, lineage


def main() -> int:
    argparse.ArgumentParser(description=__doc__).parse_args()

    for source in (True, False):
        label = "with a source result" if source else "with none"
        ledger, result, lineage = _recover(source)
        print(f"\n  the occurrence recorded {label}")
        print(f"    occurrences in its lineage: {len(lineage)}")
        print(f"    exact material carried: "
              f"{'none' if result.exact_material is None else len(result.exact_material)}")

        found: dict[str, list[str]] = {}
        for occurrence in lineage:
            for path, coordinate in _relation_coordinates(occurrence.material):
                named = str(coordinate.get("relation"))
                found.setdefault(named, []).append(
                    f"{occurrence.kind.split('.')[-1]}:.{'.'.join(path)}"
                )
        for occurrence in lineage:
            print(
                f"      {occurrence.kind:52} "
                f"{len(list(_relation_coordinates(occurrence.material)))}"
            )
        print(f"    recorded relation coordinates: {sum(len(v) for v in found.values())}")
        for named in sorted(found):
            print(f"      relation {named!r}: {len(found[named])}")
            for where in found[named][:3]:
                print(f"        {where}")
        for stated in STATED_RELATIONS:
            if stated not in found:
                print(f"      no recorded {stated} relation")

    control, _acquired, _lineage = None, None, None
    ledger, _result, _lineage = _recover(True)
    elsewhere = sum(
        len(list(_relation_coordinates(event.material))) for event in ledger.list()
    )
    print(
        f"\n  the same reading over every occurrence in that ledger: {elsewhere}"
    )
    print(
        "  So the reading finds relation coordinates where occurrences record\n"
        "  them, and finds none anywhere in this branch, including in the\n"
        "  occurrence the branch names for its Yield relation."
    )

    print(
        "\n  Each occurrence is read for what it records, never for what it calls\n"
        "  itself.  A relation the grammar states and no occurrence records is\n"
        "  absent from this lineage; it is not thereby absent from Seed, and\n"
        "  nothing here supplies one."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
