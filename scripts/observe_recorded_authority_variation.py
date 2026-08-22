"""Observe how much an Authority coordinate varies across recorded occurrences.

A gate that never compares a coordinate may be failing to check it, or the
coordinate may carry nothing to check.  Those are different, and which one
holds is measurable: record lawful occurrences, collect every Authority
coordinate they carry, and count the distinct values.

A coordinate taking one value across every occurrence that records it
distinguishes no occurrence from another, whatever the reader does with it.

Usage:
    .venv/bin/python scripts/observe_recorded_authority_variation.py
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from hashlib import sha256
import json
from pathlib import Path
import sys
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from seed_runtime.events import EventLedger

from tests.operator_material_acquisition_test_witness import (
    record_operator_material_occurrence,
)
from seed_runtime.witness_material_acquisition import (
    record_witness_material_acquisition,
)

COORDINATES = ("authority", "scope", "responsibility", "responsible_boundary")


def _digest(value: object) -> str:
    return sha256(
        json.dumps(value, sort_keys=True, default=str).encode("utf-8")
    ).hexdigest()[:12]


def _carried(value: Any, coordinate: str, found: list):
    if isinstance(value, dict):
        for key, nested in value.items():
            if key == coordinate:
                found.append(nested)
            else:
                _carried(nested, coordinate, found)
    elif isinstance(value, list):
        for nested in value:
            _carried(nested, coordinate, found)


def main() -> int:
    argparse.ArgumentParser(description=__doc__).parse_args()

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

    occurrences = ledger.list()
    print(f"  lawful occurrences recorded: {len(occurrences)}")
    print(f"  distinct occurrence kinds:   {len({e.kind for e in occurrences})}\n")

    for coordinate in COORDINATES:
        values: list[Any] = []
        by_kind: dict[str, set] = defaultdict(set)
        for event in occurrences:
            found: list = []
            _carried(event.material, coordinate, found)
            for value in found:
                values.append(value)
                by_kind[event.kind].add(_digest(value))
        distinct = Counter(_digest(value) for value in values)
        carriers = len([k for k, v in by_kind.items() if v])
        varies_within_kind = [k for k, v in by_kind.items() if len(v) > 1]
        print(
            f"    {coordinate:22} recorded {len(values):3} times across "
            f"{carriers:2} occurrence kinds, {len(distinct):2} distinct values, "
            f"varying within {len(varies_within_kind)} kind(s)"
        )

    print(
        "\n  A coordinate that never varies within an occurrence kind is settled\n"
        "  by that kind.  It separates one kind from another and no occurrence\n"
        "  from another occurrence of its kind, so a reader that already resolved\n"
        "  the kind learns nothing further by comparing it."
    )
    print(
        "\n  What this does not establish: whether the value ought to vary, or\n"
        "  what occurrence would establish it if it did.  Only that across these\n"
        "  lawful recordings it does not."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
