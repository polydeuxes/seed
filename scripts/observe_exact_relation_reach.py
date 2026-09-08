"""Observe the carried-material surface the blanket Yield predicate reaches.

`exact_relation` stops holding when a coordinate the Yield grammar never names
is changed, so it cannot say which coordinate it establishes.  What it can be
asked is its reach over the material each occurrence carries.

This enumerates leaves of ``event.material`` only.  The predicates also read
each occurrence's envelope -- its existence, kind, Locality, exact material and
integrity -- and each of those is perturbed separately at the end rather than
counted in the material surface.  A count from this file is a count of carried-material
coordinates, never of everything a predicate can observe.

Each leaf coordinate carried by the recorded result, the Yield yield_relation and the
responsible Act yield_relation is changed one at a time, and the predicates are read
again.  The reach is then set beside the coordinates the Book states for this
relation, so coverage and over-coupling are counted rather than argued.

Every reading here is taken from an in-memory ledger, and three things stay
separate.  That ledger reports an occurrence's integrity as unverifiable and
hands the reader the stored occurrence itself, so a predicate asking whether an
occurrence is not corrupted passes for every occurrence it is asked about here.
Separately, observe_exact_relation_reach.py substitutes that reading, making
the ledger report one occurrence corrupted, and the predicate's response to
that value is exercised there.  A durable ledger answers differently again: it
verifies a recorded occurrence, returns a fresh one to each reader, and refuses
to revise or remove a recorded occurrence at all.

So a change reached here by holding an occurrence is not a change a durable
ledger permits.  These readings say what the predicates read from the material
given to them, never that a state constructed here is reachable.
See scripts/observe_ledger_verification_boundary.py.

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
from seed_runtime.yield_relation import (
    read_requirements_of_yield_relation,
)

from tests.operator_material_source_test_witness import (
    record_operator_material_occurrence,
)

LOCALITY = "exact-relation-reach"

# The coordinates 02.Acts.A states for the Yield relation, and the material
# names each is carried under.  Nothing else in this file reads these.
STATED_YIELD_COORDINATES = {
    "act_occurrence_identity": "first_subject",
    "result_identity": "second_subject",
    "yield_relation_identity": "relation_occurrence",
    "scope": "Scope",
    "locality_identity": "Locality",
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
        ledger.get(result.material["yield_relation_identity"]),
        ledger.get(result.material["act_occurrence_identity"]),
    )


def _requirements(ledger, result) -> dict[str, bool]:
    return read_requirements_of_yield_relation(
        ledger,
        recorded_result_event_identity=result.identity,
        yield_relation_event_identity=result.material.get(
            "yield_relation_identity"
        ),
        act_occurrence_event_identity=result.material.get(
            "act_occurrence_identity"
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


ENVELOPE = [
    (
        f"{holder}.{coordinate}",
        holder,
        (
            lambda ledger, event, coordinate=coordinate: object.__setattr__(
                event,
                coordinate,
                b"substituted"
                if coordinate == "exact_material"
                else "substituted",
            )
        ),
    )
    for holder in ("result", "yield_relation", "act_occurrence")
    for coordinate in ("locality_identity", "kind", "exact_material", "identity")
] + [
    (
        f"{holder}.integrity",
        holder,
        lambda ledger, event: _report_corrupted(ledger, event),
    )
    for holder in ("result", "yield_relation", "act_occurrence")
] + [
    (
        f"{holder}.existence",
        holder,
        lambda ledger, event: _withdraw(ledger, event),
    )
    for holder in ("result", "yield_relation", "act_occurrence")
]


def _report_corrupted(ledger, event) -> None:
    """Have the ledger report this one occurrence as corrupted."""

    from seed_runtime.events import CORRUPTED

    original = ledger.integrity_of

    def integrity_of(identity, _original=original, _identity=event.identity):
        return CORRUPTED if identity == _identity else _original(identity)

    object.__setattr__(ledger, "integrity_of", integrity_of)


def _withdraw(ledger, event) -> None:
    """Make this one occurrence absent to any reader that resolves it."""

    original = ledger.get

    def get(identity, _original=original, _identity=event.identity):
        return None if identity == _identity else _original(identity)

    object.__setattr__(ledger, "get", get)


def main() -> int:
    argparse.ArgumentParser(description=__doc__).parse_args()

    ledger, result, yield_relation, act_occurrence = _material()
    baseline = _requirements(ledger, result)
    holders = {"result": result, "yield_relation": yield_relation, "act_occurrence": act_occurrence}
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
            ledger, result, yield_relation, act_occurrence = _material()
            target = {
                "result": result,
                "yield_relation": yield_relation,
                "act_occurrence": act_occurrence,
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

    print(f"\n  changed one carried-material leaf at a time: {total}")
    print(f"    noticed by some predicate   {len(noticed)}")
    print(f"    noticed by none             {len(unnoticed)}")
    print(
        f"\n  of the noticed, {len(over)} carry no coordinate the Yield relation states"
    )
    print(f"  stated coordinates reached: {sorted(covered)}")
    print(
        f"  stated coordinates changed with every predicate still holding, "
        f"at the carrier reached first: "
        f"{sorted({r['stated_yield_coordinate'] for r in missed}) or 'none'}"
    )
    print(
        "\n  read that line narrowly.  One coordinate name is recorded by more\n"
        "  than one occurrence and answers differently at each.  Scope is\n"
        "  noticed where the recorded result carries it and not\n"
        "  noticed where the responsible Act yield_relation records its own, so a name\n"
        "  appearing above is a statement about one carrier, never about the\n"
        "  coordinate.  scripts/observe_broad_yield_predicate.py asks each\n"
        "  carrier separately."
    )
    print("\n  a sample of the over-coupled surface:")
    for row in over[:12]:
        print(f"    {'.'.join(row['coordinate_path'])[:74]}")
    print("\n  envelope coordinates, which are not carried material:\n")
    envelope_rows = []
    for label, holder_name, change in ENVELOPE:
        ledger, result, yield_relation, act_occurrence = _material()
        target = {
            "result": result,
            "yield_relation": yield_relation,
            "act_occurrence": act_occurrence,
        }[holder_name]
        try:
            change(ledger, target)
        except Exception as error:
            print(f"    {'refused at once':22} {label}  ({type(error).__name__})")
            continue
        after = _requirements(ledger, result)
        stopped = sorted(k for k, v in baseline.items() if v and not after[k])
        envelope_rows.append((label, holder_name, stopped))
        mark = "noticed" if stopped else "NOT NOTICED"
        print(f"    {mark:22} {label}  {', '.join(stopped) or 'every predicate still holds'}")

    # The three predicates are held apart here by position only.  Each is
    # described by the coordinates whose change it notices, so nothing in this
    # section rests on what its implementation calls it.
    order = sorted(baseline)
    signature = {name: [] for name in order}
    for row in noticed:
        for name in row["predicates_that_stopped_holding"]:
            signature[name].append(
                f"{row['carried_in']}:{'.'.join(row['coordinate_path'])}"
            )
    for label, holder_name, stopped in envelope_rows:
        for name in stopped:
            signature[name].append(f"envelope:{label}")

    print("\n  each predicate by what it is sensitive to, named by position:\n")
    for position, name in enumerate(order, start=1):
        print(f"    predicate {position}: notices {len(signature[name])} coordinates")

    shared = set.intersection(*(set(v) for v in signature.values()))
    print(f"    coordinates every predicate notices: {len(shared)}")
    print(
        "\n  which stated Yield coordinate each predicate establishes is not read\n"
        "  from these sets.  Matching a path fragment against a coordinate name\n"
        "  reported Scope and Locality as reached, and changing each of\n"
        "  them directly stopped no predicate.  The per-coordinate experiment is\n"
        "  the measurement; this section counts sensitivity only."
    )

    Path("exact_relation_reach.json").write_text(
        json.dumps(
            {"noticed": noticed, "unnoticed": unnoticed}, indent=1
        ),
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
