"""Measure the population of recorded coordinates one exact rule applies to.

A road tells you what one journey carried.  It cannot tell you what a corpus
holds, and reading a road's answer as a corpus answer is how a coordinate
survives a cut that reported itself complete.

The 2+2=5 work already answers this shape.  Exact coordinates preserve complete
addressability, so the population a rule applies to is brought forth without
instantiating what it does not apply to.  Here the rule is a key name and the
subject is the material recorded in one corpus, so nothing is enumerated: no
occurrence kinds, no roads, no modules, no registry.

Declared for each corpus read:

    subject                every coordinate recorded in its material
    rule                   the exact key equals the one named
    completeness boundary  the occurrences that corpus holds
    findings               the count, and the exact occurrence references

Usage:
    .venv/bin/python scripts/measure_recorded_coordinate_population.py KEY DB...
"""

from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path
import shutil
import sys
import tempfile
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from seed_runtime.events import SQLiteEventLedger


def _coordinates(value: Any, key: str, path: tuple[str, ...] = ()):
    if isinstance(value, dict):
        for name, nested in value.items():
            if name == key:
                yield path + (str(name),), nested
            else:
                yield from _coordinates(nested, key, path + (str(name),))
    elif isinstance(value, list):
        for position, nested in enumerate(value):
            yield from _coordinates(nested, key, path + (str(position),))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("key")
    parser.add_argument("corpus", nargs="+", type=Path)
    arguments = parser.parse_args()

    for corpus in arguments.corpus:
        if not corpus.exists():
            print(f"  {corpus}: absent")
            continue
        with tempfile.TemporaryDirectory() as directory:
            # read a copy, so measuring a corpus cannot revise it
            copy = Path(directory) / corpus.name
            shutil.copy(corpus, copy)
            ledger = SQLiteEventLedger(str(copy))
            try:
                occurrences = ledger.list()
                carrying: list[str] = []
                paths: Counter[str] = Counter()
                for event in occurrences:
                    found = list(_coordinates(event.material, arguments.key))
                    if found:
                        carrying.append(event.identity)
                    for path, _value in found:
                        paths["." + ".".join(path)] += 1
            finally:
                ledger.close()

        print(f"\n  {corpus.name}")
        print(f"    completeness boundary: {len(occurrences)} recorded occurrences")
        print(f"    rule: the exact key {arguments.key!r}")
        print(f"    occurrences carrying it: {len(carrying)}")
        print(f"    coordinates it applies to: {sum(paths.values())}")
        for path, count in paths.most_common(8):
            print(f"      {count:5}  {path[:76]}")
        if carrying:
            print(f"    first references: {', '.join(carrying[:4])}")
    print(
        "\n  Each count is bounded by the corpus it was read from and says nothing"
        "\n  about material no corpus here recorded.  A corpus records what was"
        "\n  produced when it was written, so this measures what is held, never"
        "\n  what current production would write."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
