"""Ask whether a branch coordinate distinguishes anything containment does not.

`branch_of_current_Standing` survived the last pass on the ground that the Book
states no branch relation and no relation occurrence for one. That establishes
it is not a relation. It does not establish it is a coordinate, because a third
answer exists: being carried by that exact current Standing may already supply
the identity, leaving the key as serialization of the containment.

One question decides it. Can two otherwise identical exact Responsibilities
differ only in which current Standing they are branches of? If they can, the
identity has to be preserved somewhere and nothing else preserves it. If they
cannot, containment already carries it.

The recorded road is asked rather than the file, so the answer comes from
occurrences rather than from what the grammar happens to declare.

Usage:
    .venv/bin/python scripts/observe_branch_coordinate_discrimination.py
"""

from __future__ import annotations

import argparse
from collections import defaultdict
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

GRAMMAR = Path(__file__).resolve().parents[1] / "book_of_seed" / "witness_grammar.json"


def main() -> int:
    argparse.ArgumentParser(description=__doc__).parse_args()

    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))
    declared = grammar["book_coordinates"]

    carrying = {
        reference: body["branch_of_current_Standing"]
        for reference, body in declared.items()
        if "branch_of_current_Standing" in body
    }
    print(f"  coordinates carrying the branch coordinate: {len(carrying)}")
    for reference, value in carrying.items():
        print(f"    {reference:16} {value}")

    from tests.test_byte_measurement import _ledger, _movement_source

    ledger = _ledger("ta\n")
    _movement_source(ledger)
    occurrences = ledger.list()

    # Group recorded occurrences by the Responsibility they claim, then ask
    # whether one Responsibility is ever carried by more than one Standing.
    by_responsibility: dict[str, set[str]] = defaultdict(set)
    for event in occurrences:
        material = event.material
        responsibility = material.get("responsibility") or material.get(
            "responsibility_assignment_reference"
        )
        if not isinstance(responsibility, str):
            continue
        boundary = material.get("standing_boundary_reference") or material.get(
            "current_standing_boundary"
        )
        by_responsibility[responsibility].add(
            boundary if isinstance(boundary, str) else "<none recorded>"
        )

    print(f"\n  one road, {len(occurrences)} occurrences")
    print(f"  distinct Responsibilities claimed: {len(by_responsibility)}")
    several = {
        responsibility: boundaries
        for responsibility, boundaries in by_responsibility.items()
        if len(boundaries) > 1
    }
    print(f"  Responsibilities recorded under more than one Standing boundary: "
          f"{len(several)}")
    for responsibility, boundaries in list(several.items())[:6]:
        print(f"    {responsibility}: {len(boundaries)} boundaries")

    recorded = sum(
        1
        for boundaries in by_responsibility.values()
        for boundary in boundaries
        if boundary != "<none recorded>"
    )
    print(f"  Responsibility-to-boundary pairs naming a boundary at all: {recorded}")

    print(
        "\n  The clauses carrying the coordinate say which current Standing by\n"
        "  naming what that Standing carries, not by naming the Standing. Two\n"
        "  Responsibilities alike in every other coordinate would then be told\n"
        "  apart by their subject matter, which their own subject already carries.\n"
        "\n  This road cannot settle it. If no Responsibility here is recorded under\n"
        "  two boundaries, that is one road's population and not a demonstration\n"
        "  that none can be. The coordinate stays a surviving candidate, and the\n"
        "  question it needs is whether any Responsibility is ever a branch of two\n"
        "  Standings, which no measurement of a single road answers.\n"
        "\n  Bounded to one road. Nothing here says the coordinate should go or stay."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
