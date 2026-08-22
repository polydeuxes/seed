"""Observe how many kinds of thing one key carries on a single road.

A key is not a coordinate.  Everything recorded under one name is one
coordinate only if the things recorded there are one kind of thing, and that is
measurable without deciding what any of them mean.

One lawful road is recorded and every value carried under the Authority key is
read for its shape.  Values are grouped by what they are, never by the name
they are filed under, and no shape is called Authority here.

Usage:
    .venv/bin/python scripts/observe_authority_key_shapes.py
"""

from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path
import sys
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

COORDINATE = "authority"


def _shape(value: Any) -> str:
    """What one recorded value is, said without naming what it means."""

    if isinstance(value, dict):
        return "a mapping of " + ", ".join(sorted(value))
    if isinstance(value, list):
        return f"a list of {len(value)}"
    if isinstance(value, str):
        if " " in value.strip() and len(value) > 24:
            return "a sentence"
        return f"one word or phrase: {value!r}"
    return type(value).__name__


def _carried(value: Any, path: tuple = ()):
    if isinstance(value, dict):
        for key, nested in value.items():
            if key == COORDINATE:
                yield path + (key,), nested
            else:
                yield from _carried(nested, path + (str(key),))
    elif isinstance(value, list):
        for position, nested in enumerate(value):
            yield from _carried(nested, path + (str(position),))


def main() -> int:
    argparse.ArgumentParser(description=__doc__).parse_args()

    from tests.test_byte_measurement import _ledger, _movement_source

    ledger = _ledger("ta\n")
    _movement_source(ledger)

    shapes: Counter[str] = Counter()
    for event in ledger.list():
        for _path, value in _carried(event.material):
            shapes[_shape(value)] += 1

    print(f"  one lawful road, {len(ledger.list())} occurrences recorded\n")
    print(f"  values carried under the {COORDINATE} key: {sum(shapes.values())}")
    print(f"  distinct shapes among them: {len(shapes)}\n")
    for shape, count in shapes.most_common():
        print(f"    {count:4}  {shape[:96]}")

    print(
        "\n  These are grouped by what each value is, not by what it is called.\n"
        "  A key carrying a mapping, a word, and a sentence is carrying more than\n"
        "  one kind of thing, whatever any of them turn out to be.  Nothing here\n"
        "  says which of them is Authority, or that any of them is."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
