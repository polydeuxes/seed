"""Read what Responsibility branches a current Standing carries.

Asking what consumes a result presumes a chain.  The Book carries independent
Responsibility branches under one Standing, and an exhaustive subject set for
one establishes no order, Applicability, or completion for another.  So the
question a Standing can answer is not what follows a result.  It is which
branches this Standing carries, and what each one already holds.

For every Locality in a recorded corpus, the current Standing is read and each
Responsibility branch it carries is resolved to the occurrence that recorded it.
What that occurrence holds is then read: its subject, its exact Act, its Scope,
its Locality.

Nothing is proposed.  A branch that holds everything it needs is not thereby
work Seed will do, and a branch missing something is not thereby a defect.

Three durable corpora in this repository are addressable as recorded material
and are refused by the current Standing reader: their representation
occurrences carry no locality_standing_through_event_occurrence_identity, which
current Standing requires.  Those records remain retrievable and preserve what
their own recording boundary established; what is refused is projecting them
into current Standing, which they never established.  Refusing looks correct,
and fabricating the missing boundary would not.  With no corpus given, one road
is recorded and read.

Usage:
    .venv/bin/python scripts/observe_standing_responsibility_branches.py [DB...]
"""

from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path
import shutil
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from seed_runtime.events import SQLiteEventLedger
from seed_runtime.operator_locality_standing import read_operator_locality_standing

HELD = (
    "responsibility",
    "exact_act",
    "act",
    "scope",
    "unknown",
    "book_clause_identity",
    "assignment_subject_identity",
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("corpus", nargs="*", type=Path)
    arguments = parser.parse_args()

    if not arguments.corpus:
        from tests.test_byte_measurement import _ledger, _movement_source

        ledger = _ledger("ta\n")
        _movement_source(ledger)
        localities = sorted({e.locality_identity for e in ledger.list()})
        print(f"\n  one recorded road: {len(localities)} Locality(ies)")
        for locality in localities:
            standing = read_operator_locality_standing(
                ledger, locality_identity=locality
            )
            branches = standing.get("subject_to_act_binding_occurrences") or {}
            print(
                f"\n    Locality {locality!r}: "
                f"{len(branches)} Responsibility branch(es)"
            )
            held: Counter[str] = Counter()
            subjects = 0
            for identity in branches:
                occurrence = ledger.get(identity)
                if occurrence is None:
                    held["branch occurrence absent"] += 1
                    continue
                for coordinate in HELD:
                    if coordinate in occurrence.material:
                        held[coordinate] += 1
                if "assignment_subject_identity" in occurrence.material:
                    subjects += 1
            if branches:
                print(f"      branches carrying an exact subject: {subjects}")
                for coordinate, count in held.most_common():
                    print(f"        {count:3}  {coordinate}")
                named = Counter()
                subject_values = set()
                for identity in branches:
                    occurrence = ledger.get(identity)
                    if occurrence is None:
                        continue
                    named[str(occurrence.material.get("responsibility"))[:58]] += 1
                    subject_values.add(
                        str(occurrence.material.get("assignment_subject_identity"))
                    )
                print(f"      distinct subjects among them: {len(subject_values)}")
                print(f"      distinct Responsibilities named: {len(named)}")
                for name, count in named.most_common(6):
                    print(f"        {count:3}  {name}")

    for corpus in arguments.corpus:
        if not corpus.exists():
            print(f"  {corpus}: absent")
            continue
        with tempfile.TemporaryDirectory() as directory:
            copy = Path(directory) / corpus.name
            shutil.copy(corpus, copy)
            ledger = SQLiteEventLedger(str(copy))
            try:
                localities = sorted({e.locality_identity for e in ledger.list()})
                print(f"\n  {corpus.name}: {len(localities)} Locality(ies)")
                for locality in localities:
                    standing = read_operator_locality_standing(
                        ledger, locality_identity=locality
                    )
                    branches = standing.get(
                        "subject_to_act_binding_occurrences"
                    ) or {}
                    print(
                        f"\n    Locality {locality!r}: "
                        f"{len(branches)} Responsibility branch(es)"
                    )
                    held: Counter[str] = Counter()
                    subjects = 0
                    for identity in branches:
                        occurrence = ledger.get(identity)
                        if occurrence is None:
                            held["branch occurrence absent"] += 1
                            continue
                        for coordinate in HELD:
                            if coordinate in occurrence.material:
                                held[coordinate] += 1
                        if "assignment_subject_identity" in occurrence.material:
                            subjects += 1
                    if branches:
                        print(f"      branches carrying an exact subject: {subjects}")
                        for coordinate, count in held.most_common():
                            print(f"        {count:3}  {coordinate}")
            finally:
                ledger.close()

    print(
        "\n  Each branch is read where its own occurrence recorded it.  A branch\n"
        "  carrying its subject and its exact Act is not thereby available work,\n"
        "  and one carrying less is not thereby incomplete: what a branch needs\n"
        "  is its own Responsibility's to say, and no sibling's."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
