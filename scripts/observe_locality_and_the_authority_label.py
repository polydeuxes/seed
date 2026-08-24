"""Observe which coordinates move when an occurrence moves between Localities.

One coordinate on this road is produced by a call taking no input, so it cannot
answer to the occurrence that carries it.  The question here is not what that
coordinate is called.  It is whether anything it holds separates two
occurrences that a Locality does not already separate.

Lawful occurrences are recorded across distinct Localities through the same
production shape, and each coordinate is read for whether it moved with them.
They are distinct occurrences, so identities and recording moments differ of
necessity; Locality is what was varied deliberately.

This disposes nothing about what either coordinate is.  A coordinate that does
not move may still be preserving a distinction that these recordings do not
exercise.

Usage:
    .venv/bin/python scripts/observe_locality_and_the_authority_label.py
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from hashlib import sha256
import json
from pathlib import Path
import sys
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from seed_runtime.events import EventLedger
from seed_runtime.yield_relation import (
    read_requirements_of_yield_relation,
)

from tests.operator_material_acquisition_test_witness import (
    record_operator_material_occurrence,
)

READ = ("authority", "scope", "responsibility", "responsible_boundary", "act")
LOCALITIES = ("first-locality", "second-locality", "third-locality", "fourth-locality")


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


def main() -> int:
    argparse.ArgumentParser(description=__doc__).parse_args()

    ledger = EventLedger()
    results = {}
    for locality in LOCALITIES:
        results[locality] = record_operator_material_occurrence(
            ledger,
            locality_identity=locality,
            exact=b"2+2=5\n",
            source_boundary="exact supplied material boundary",
        )

    print(
        f"  {len(LOCALITIES)} occurrences of one exact Act over one exact\n"
        f"  material, produced through the same shape, with the Locality\n"
        f"  deliberately varied.  Each is its own occurrence, so identities and\n"
        f"  recording moments differ too; the Locality is what was varied on\n"
        f"  purpose.\n"
    )

    # keyed by kind and path so one occurrence carrying two of a coordinate is
    # never read as two occurrences disagreeing.
    moved: dict[str, list[tuple[str, tuple[str, ...], int]]] = defaultdict(list)
    for coordinate in READ:
        seen: dict[tuple[str, tuple[str, ...]], set] = defaultdict(set)
        for event in ledger.list():
            for path, value in _paths(event.material, coordinate):
                seen[(event.kind, path)].add(_digest(value))
        for (kind, path), values in seen.items():
            moved[coordinate].append((kind, path, len(values)))

    print("  coordinate                 paths   paths whose value moved with Locality")
    for coordinate in READ:
        rows = moved[coordinate]
        changed = [row for row in rows if row[2] > 1]
        print(f"    {coordinate:22} {len(rows):5}   {len(changed)}")

    print("\n  the Locality of the occurrences themselves:")
    localities = {event.locality_identity for event in ledger.list()}
    print(f"    distinct recorded Localities: {len(localities)}")

    print(
        "\n  whether the Yield gate answers differently across those Localities:"
    )
    readings = set()
    for locality, result in results.items():
        requirements = read_requirements_of_yield_relation(
            ledger,
            recorded_result_event_identity=result.identity,
            yield_relation_event_identity=result.material.get(
                "yield_relation_identity"
            ),
            act_occurrence_event_identity=result.material.get(
                "act_occurrence_identity"
            ),
        )
        readings.add(tuple(sorted(requirements.items())))
    print(f"    distinct readings across {len(LOCALITIES)} Localities: {len(readings)}")

    print(
        "\n  What this does not dispose: a coordinate that did not move may be\n"
        "  preserving a distinction these recordings never exercised, and a\n"
        "  coordinate that moved with Locality is not thereby the same\n"
        "  coordinate as Locality."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
