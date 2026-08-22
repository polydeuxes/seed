"""Observe whether an Authority coordinate changes between occurrences.

A gate that never compares a coordinate may be failing to check it, or the
coordinate may hold nothing that separates one occurrence from another.  Which
holds is measurable, but only if one question is not mistaken for another.

Several Authority-shaped coordinates sit at different paths inside a single
occurrence.  Collecting them by occurrence kind alone makes one occurrence
carrying two of them look like two occurrences disagreeing.  So each exact path
is kept apart, and variation is read across occurrences at the same path.

Usage:
    .venv/bin/python scripts/observe_recorded_authority_variation.py
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from hashlib import sha256
import inspect
import json
from pathlib import Path
import sys
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from seed_runtime.events import EventLedger
import seed_runtime.operator_material_acquisition as acquisition

from tests.operator_material_acquisition_test_witness import (
    record_operator_material_occurrence,
)
from seed_runtime.witness_material_acquisition import (
    record_witness_material_acquisition,
)

COORDINATES = ("authority", "scope")


def _digest(value: object) -> str:
    return sha256(
        json.dumps(value, sort_keys=True, default=str).encode("utf-8")
    ).hexdigest()[:12]


def _paths(value: Any, coordinate: str, path: tuple[str, ...] = ()):
    if isinstance(value, dict):
        for key, nested in value.items():
            if key == coordinate:
                yield path + (key,), nested
            else:
                yield from _paths(nested, coordinate, path + (str(key),))
    elif isinstance(value, list):
        for position, nested in enumerate(value):
            yield from _paths(nested, coordinate, path + (str(position),))


def _recorded() -> EventLedger:
    ledger = EventLedger()
    for index, material in enumerate((b"2+2=5\n", b"ab", b"\x00\xff", b"a longer one")):
        record_operator_material_occurrence(
            ledger,
            locality_identity=f"variation-{index}",
            exact=material,
            source_boundary="exact supplied material boundary",
        )
    for index, material in enumerate((b"witness one", b"\x00\xffwitness two")):
        record_witness_material_acquisition(
            ledger,
            locality_identity=f"witness-{index}",
            exact_bytes=material,
            source_boundary="exact supplied material boundary",
        )
    return ledger


def main() -> int:
    argparse.ArgumentParser(description=__doc__).parse_args()

    ledger = _recorded()
    occurrences = ledger.list()
    print(f"  lawful occurrences: {len(occurrences)}, "
          f"kinds: {len({e.kind for e in occurrences})}\n")

    for coordinate in COORDINATES:
        # keyed by the exact occurrence kind and the exact path, so one
        # occurrence carrying two of them is never read as two disagreeing.
        seen: dict[tuple[str, tuple[str, ...]], dict[str, str]] = defaultdict(dict)
        for event in occurrences:
            for path, value in _paths(event.material, coordinate):
                seen[(event.kind, path)][event.identity] = _digest(value)

        changing = 0
        print(f"  {coordinate} by exact kind and path:\n")
        for (kind, path), by_occurrence in sorted(seen.items(), key=lambda i: str(i[0])):
            distinct = len(set(by_occurrence.values()))
            changes = distinct > 1
            changing += changes
            mark = "CHANGES" if changes else "same   "
            print(
                f"    {mark} {len(by_occurrence):2} occurrences, "
                f"{distinct} distinct   {kind}  .{'.'.join(path)}"
            )
        print(
            f"\n    {changing} of {len(seen)} kind/path pairs change between "
            f"occurrences of that kind\n"
        )

    print("  the Authority producer this Yield reads, and what can change it:\n")
    producer = acquisition._authority
    signature = inspect.signature(producer)
    print(f"    {producer.__module__.split('.')[-1]}._authority{signature}")
    print(f"    parameters: {list(signature.parameters) or 'none'}")
    print(f"    two separate calls agree: {producer() == producer()}")
    print(
        "\n    With no parameter there is no input that changes it, so the\n"
        "    recorded result and the responsible Act evidence of one Yield do\n"
        "    not take an Authority from each other.  Each call builds its own,\n"
        "    and they agree because the same literal is built twice."
    )
    print(
        "\n  What this does not establish: whether Authority ought to vary, what\n"
        "  occurrence would establish it if it did, or that a comparison is\n"
        "  unnecessary.  A comparison that refuses nothing today would still\n"
        "  refuse a disagreement a different producer could record."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
