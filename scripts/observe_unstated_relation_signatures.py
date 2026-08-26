"""Ask whether three unstated relation labels preserve three relations.

A road records three relation labels the grammar does not state.  Whether those
are three relations, or one spelled three ways, is not settled by the spelling.

Each relation coordinate is read for its signature: the coordinates the mapping
carries and what its endpoints are.  What the recording occurrence carries
around it is not part of the signature, because one relation recorded beside
different coordinates is still one relation.  The relations the grammar states
are read the same way, so a label duplicating one of them shows itself.

A label is never used to group.  Two labels landing in one signature are one
physiology spelled twice, and one label landing in two is one spelling over two
physiologies.

Usage:
    .venv/bin/python scripts/observe_unstated_relation_signatures.py
"""

from __future__ import annotations

import argparse
from collections import defaultdict
import json
from pathlib import Path
import sys
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

GRAMMAR = Path(__file__).resolve().parents[1] / "book_of_seed" / "witness_grammar.json"
AROUND = (
    "responsibility",
    "exact_act",
    "act",
    "scope",
    "unknown",
    "role",
    "book_clause_identity",
)


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


def _endpoint(value: Any) -> str:
    if isinstance(value, dict):
        return "mapping of " + ", ".join(sorted(value))
    if isinstance(value, list):
        return f"list of {len(value)}"
    if isinstance(value, str):
        return "a word or identity"
    return type(value).__name__


def main() -> int:
    argparse.ArgumentParser(description=__doc__).parse_args()

    from tests.test_byte_measurement import _ledger, _movement_source

    coordinates = json.loads(GRAMMAR.read_text(encoding="utf-8"))["book_coordinates"]
    stated = {
        coordinates["02.Acts.A"]["Yield"]["relation"],
        coordinates["06.Locality.A"]["Locality"]["relation"],
    }
    ledger = _ledger(b"ta\n")
    _movement_source(ledger)

    signatures: dict[tuple, list[str]] = defaultdict(list)
    for event in ledger.list():
        for _path, coordinate in _relation_coordinates(event.material):
            label = str(coordinate.get("relation"))
            signature = (
                tuple(sorted(coordinate)),
                _endpoint(coordinate["first_subject"]),
                _endpoint(coordinate["second_subject"]),
            )
            signatures[signature].append(label)

    print(f"  relation coordinates read: "
          f"{sum(len(v) for v in signatures.values())}")
    print(f"  distinct signatures among them: {len(signatures)}\n")

    for index, (signature, labels) in enumerate(
        sorted(signatures.items(), key=lambda item: -len(item[1])), start=1
    ):
        carried, first, second = signature
        print(f"  signature {index}: {len(labels)} occurrence(s)")
        print(f"    the mapping carries: {', '.join(carried)}")
        print(f"    first subject:  {first}")
        print(f"    second subject: {second}")
        marks = sorted(set(labels))
        print(
            f"    labels found here: {marks}"
            f"{'   STATED' if any(m in stated for m in marks) else ''}\n"
        )

    spellings: dict[str, set] = defaultdict(set)
    for index, (_signature, labels) in enumerate(
        sorted(signatures.items(), key=lambda item: -len(item[1])), start=1
    ):
        for label in labels:
            spellings[label].add(index)
    print("  each label, and the signatures it appears under:")
    for label in sorted(spellings):
        print(f"    {label:16} {sorted(spellings[label])}")

    print(
        "\n  Signatures are grouped before any label is read.  A label is a name\n"
        "  an implementation gave a coordinate and is not evidence that two\n"
        "  coordinates differ.  Bounded to one road, and nothing here names\n"
        "  anything or says a signature ought to be stated by the grammar."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
