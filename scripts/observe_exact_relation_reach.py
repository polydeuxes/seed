"""Observe the whole surface the blanket Yield predicate is sensitive to.

`exact_relation` stops holding when a coordinate the Yield grammar never names
is changed, so it cannot say which coordinate it establishes.  What it can be
asked is its reach: every coordinate whose change it notices.

Each leaf coordinate carried by the recorded result, the Yield evidence and the
responsible Act evidence is changed one at a time, and the predicates are read
again.  The reach is then set beside the coordinates the Book states for this
relation, so coverage and over-coupling are counted rather than argued.

Usage:
    .venv/bin/python scripts/observe_exact_relation_reach.py
"""

from __future__ import annotations

import argparse
from copy import deepcopy
import json
from pathlib import Path
import sys
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from seed_runtime.events import EventLedger
from seed_runtime.evidence_of_yield_relation import (
    read_requirements_of_yield_relation,
)

from tests.operator_material_acquisition_test_witness import (
    record_operator_material_occurrence,
)

LOCALITY = "exact-relation-reach"

# The coordinates 02.Acts.A states for the Yield relation, and the material
# names each is carried under.  Nothing else in this file reads these.
STATED_YIELD_COORDINATES = {
    "act_occurrence_identity": "first_subject",
    "result_identity": "second_subject",
    "evidence_of_yield_relation_identity": "relation_occurrence",
    "authority": "Authority",
    "scope": "Scope",
    "evidence_scope": "Scope",
    "locality_identity": "Locality",
    "limits": "limits",
    "unknown": "Unknown",
}


def _material():
    ledger = EventLedger()
    result = record_operator_material_occurrence(
        ledger,
        locality_identity=LOCALITY,
        exact=b"2+2=5\n",
        source_boundary="exact supplied material boundary",
    )
    return (
        ledger,
        result,
        ledger.get(result.material["evidence_of_yield_relation_identity"]),
        ledger.get(result.material["responsible_act_evidence_identity"]),
    )


def _requirements(ledger, result) -> dict[str, bool]:
    return read_requirements_of_yield_relation(
        ledger,
        recorded_result_event_identity=result.identity,
        evidence_of_yield_relation_event_identity=result.material.get(
            "evidence_of_yield_relation_identity"
        ),
        responsible_act_evidence_event_identity=result.material.get(
            "responsible_act_evidence_identity"
        ),
    )


def _leaves(value: object, path: tuple[str, ...] = ()):
    if isinstance(value, dict):
        for key, nested in value.items():
            yield from _leaves(nested, path + (str(key),))
    elif isinstance(value, list):
        for position, nested in enumerate(value):
            yield from _leaves(nested, path + (str(position),))
    else:
        yield path, value


def _substitute(material: dict[str, Any], path: tuple[str, ...]) -> None:
    holder: Any = material
    for part in path[:-1]:
        holder = holder[part] if isinstance(holder, dict) else holder[int(part)]
    last = path[-1]
    existing = holder[last] if isinstance(holder, dict) else holder[int(last)]
    changed = (
        "substituted"
        if not isinstance(existing, str) or existing != "substituted"
        else "substituted twice"
    )
    if isinstance(holder, dict):
        holder[last] = changed
    else:
        holder[int(last)] = changed


def main() -> int:
    argparse.ArgumentParser(description=__doc__).parse_args()

    ledger, result, evidence, act_evidence = _material()
    baseline = _requirements(ledger, result)
    holders = {"result": result, "evidence": evidence, "act_evidence": act_evidence}
    paths = {
        name: [path for path, _value in _leaves(event.material)]
        for name, event in holders.items()
    }
    print(f"  baseline: {baseline}")
    print(
        "  leaf coordinates: "
        + ", ".join(f"{name} {len(p)}" for name, p in paths.items())
    )

    noticed: list[dict[str, Any]] = []
    unnoticed: list[dict[str, Any]] = []
    for holder_name, holder_paths in paths.items():
        for path in holder_paths:
            ledger, result, evidence, act_evidence = _material()
            target = {
                "result": result,
                "evidence": evidence,
                "act_evidence": act_evidence,
            }[holder_name]
            material = deepcopy(target.material)
            try:
                _substitute(material, path)
            except (KeyError, IndexError, TypeError, ValueError):
                continue
            object.__setattr__(target, "material", material)
            after = _requirements(ledger, result)
            stopped = sorted(k for k, v in baseline.items() if v and not after[k])
            row = {
                "carried_in": holder_name,
                "coordinate_path": list(path),
                "stated_yield_coordinate": next(
                    (
                        STATED_YIELD_COORDINATES[part]
                        for part in reversed(path)
                        if part in STATED_YIELD_COORDINATES
                    ),
                    None,
                ),
                "predicates_that_stopped_holding": stopped,
            }
            (noticed if stopped else unnoticed).append(row)

    total = len(noticed) + len(unnoticed)
    over = [r for r in noticed if r["stated_yield_coordinate"] is None]
    covered = {r["stated_yield_coordinate"] for r in noticed} - {None}
    missed = [
        r for r in unnoticed if r["stated_yield_coordinate"] is not None
    ]

    print(f"\n  changed one leaf coordinate at a time: {total}")
    print(f"    noticed by some predicate   {len(noticed)}")
    print(f"    noticed by none             {len(unnoticed)}")
    print(
        f"\n  of the noticed, {len(over)} carry no coordinate the Yield relation states"
    )
    print(f"  stated coordinates reached: {sorted(covered)}")
    print(
        f"  stated coordinates changed with every predicate still holding: "
        f"{sorted({r['stated_yield_coordinate'] for r in missed}) or 'none'}"
    )
    print("\n  a sample of the over-coupled surface:")
    for row in over[:12]:
        print(f"    {'.'.join(row['coordinate_path'])[:74]}")
    Path("exact_relation_reach.json").write_text(
        json.dumps(
            {"noticed": noticed, "unnoticed": unnoticed}, indent=1
        ),
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
