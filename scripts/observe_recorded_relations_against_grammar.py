"""Set the relations a road records beside the relations the grammar states.

The grammar states relations and what each requires.  A road records relation
coordinates.  Whether those are the same relations is not settled by either
side alone, and is measurable.

Every relation coordinate a road records is read by shape, a mapping naming a
first subject, a second subject, and a relation or the occurrence of one.  The
relation each names is then set beside the relations the grammar states.

Coordinates naming evidence are counted separately and never counted as
relations.  An occurrence recorded as evidence for a relation is not that
relation, and reading one as the other is what this measures.

Usage:
    .venv/bin/python scripts/observe_recorded_relations_against_grammar.py
"""

from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import sys
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

GRAMMAR = Path(__file__).resolve().parents[1] / "book_of_seed" / "witness_grammar.json"


def _relation_coordinates(value: Any, path: tuple[str, ...] = ()):
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


def main() -> int:
    argparse.ArgumentParser(description=__doc__).parse_args()

    from tests.test_byte_measurement import _ledger, _movement_source

    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))
    stated = set(grammar["relations"])
    requires = sorted(
        {item for spec in grammar["relations"].values() for item in spec["requires"]}
    )

    ledger = _ledger("ta\n")
    _movement_source(ledger)
    occurrences = ledger.list()

    recorded: Counter[str] = Counter()
    evidence: Counter[str] = Counter()
    for event in occurrences:
        for _path, coordinate in _relation_coordinates(event.material):
            recorded[str(coordinate.get("relation"))] += 1
        for key in event.material:
            if "evidence" in key.lower():
                evidence[key] += 1

    print(f"  one road, {len(occurrences)} occurrences\n")
    print(f"  the grammar states {len(stated)} relations: {', '.join(sorted(stated))}")
    print(f"  each requires: {', '.join(requires)}\n")

    print("  relation coordinates the road records:")
    for name, count in recorded.most_common():
        mark = "stated" if name in stated else "NOT STATED"
        print(f"    {count:5}  {name:16} {mark}")

    unrecorded = sorted(stated - set(recorded))
    print(f"\n  relations the grammar states and this road records none of:")
    for name in unrecorded:
        print(f"    {name}")

    print("\n  coordinates naming evidence, counted apart from relations:")
    for key, count in evidence.most_common(6):
        print(f"    {count:5}  {key}")

    print(
        "\n  A coordinate naming evidence for a relation is not that relation.\n"
        "  This road records references to evidence for a Yield and records no\n"
        "  Yield relation, so a reader taking the first for the second reads a\n"
        "  relation that no occurrence here established.\n"
        "\n  Bounded to one road.  A relation absent here is not absent from Seed,\n"
        "  and nothing here says which side should change."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
