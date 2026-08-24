"""Observe what the runtime Yield requirements establish, coordinate by coordinate.

`read_requirements_of_yield_relation` answers three predicates, and
`_carries_exact_result` admits an exact result into current Standing when all
three hold.  The Book states a different requirement set for the same Yield
relation.  Whether one accounts for the other cannot be read off the names.

So this changes exactly one coordinate at a time in the recorded material and
records which predicates stop holding.  A Book coordinate whose change no
predicate notices is not established by this gate, whatever either side calls
it.

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
    .venv/bin/python scripts/observe_yield_requirement_reach.py
"""

from __future__ import annotations

import argparse
from copy import deepcopy
import json
from pathlib import Path
import sys
from typing import Any, Callable

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from seed_runtime.events import EventLedger
from seed_runtime.yield_relation import (
    read_requirements_of_yield_relation,
)

from tests.operator_material_acquisition_test_witness import (
    record_operator_material_occurrence,
)

LOCALITY = "yield-reach"


def _yield_material():
    """One exact recorded result and the two yield_relation occurrences it names."""

    ledger = EventLedger()
    result = record_operator_material_occurrence(
        ledger,
        locality_identity=LOCALITY,
        exact=b"2+2=5\n",
        source_boundary="exact supplied material boundary",
    )
    yield_relation = ledger.get(result.material["yield_relation_identity"])
    act_occurrence = ledger.get(result.material["act_occurrence_identity"])
    return ledger, result, yield_relation, act_occurrence


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


def _change(event, change: Callable[[dict[str, Any]], None]) -> None:
    material = deepcopy(event.material)
    change(material)
    object.__setattr__(event, "material", material)


def _set(mapping: dict[str, Any], key: str, value: Any) -> bool:
    """Change one coordinate where it is recorded.  False when it is absent."""

    if key in mapping:
        mapping[key] = value
        return True
    for nested in mapping.values():
        if isinstance(nested, dict) and _set(nested, key, value):
            return True
    return False


# Each entry names one Book coordinate of the 02.Acts.A Yield relation and one
# exact change to the material that carries it.
CHANGES: list[tuple[str, str, Callable]] = [
    (
        "first_subject (exact Act occurrence)",
        "result",
        lambda m: _set(m, "act_occurrence_identity", "substituted-occurrence"),
    ),
    (
        "second_subject (exact result)",
        "result",
        lambda m: _set(m, "result_identity", "substituted-result"),
    ),
    (
        "relation_occurrence",
        "result",
        lambda m: m.__setitem__(
            "yield_relation_identity", "substituted-yield_relation"
        ),
    ),
    ("Authority", "act_occurrence", lambda m: _set(m, "authority", "substituted")),
    ("Scope", "act_occurrence", lambda m: _set(m, "scope", "substituted")),
    ("Locality", "result", lambda m: _set(m, "locality_identity", "substituted")),
    ("limits", "result", lambda m: _set(m, "limits", ["substituted"])),
    ("Unknown", "result", lambda m: _set(m, "unknown", ["substituted"])),
    # Negative controls.  These name no Book coordinate of the Yield relation.
    # A predicate that stops holding here is not establishing any particular
    # coordinate; it is noticing that the material changed at all.
    (
        "[control] a coordinate the Yield grammar never names",
        "result",
        lambda m: m.__setitem__("an_unnamed_coordinate", "substituted"),
    ),
    (
        "[control] source_boundary, named by no Yield requirement",
        "result",
        lambda m: _set(m, "source_boundary", "substituted"),
    ),
]


def main() -> int:
    argparse.ArgumentParser(description=__doc__).parse_args()

    ledger, result, yield_relation, act_occurrence = _yield_material()
    baseline = _requirements(ledger, result)
    print(f"  baseline requirements: {baseline}")
    if not all(baseline.values()):
        raise SystemExit("the control Yield does not pass; nothing to observe")
    print()

    rows = []
    for coordinate, holder, change in CHANGES:
        ledger, result, yield_relation, act_occurrence = _yield_material()
        target = {"result": result, "yield_relation": yield_relation, "act_occurrence": act_occurrence}[
            holder
        ]
        present = {"found": False}

        def apply(material, change=change, present=present):
            present["found"] = bool(change(material))

        _change(target, apply)
        after = _requirements(ledger, result)
        noticed = sorted(k for k, v in baseline.items() if v and not after[k])
        rows.append(
            {
                "book_coordinate": coordinate,
                "changed_in": holder,
                "coordinate_present_in_material": present["found"],
                "requirements_that_stopped_holding": noticed,
            }
        )

    # A predicate that stops holding for a coordinate the grammar never names
    # is not establishing coordinates.  The controls say which predicates those
    # are; nothing here reads a predicate's name to decide.
    blanket = set()
    for row in rows:
        if row["book_coordinate"].startswith("[control]"):
            blanket.update(row["requirements_that_stopped_holding"])

    width = max(len(r["book_coordinate"]) for r in rows)
    print(f"  predicates that also stop holding for an unnamed coordinate: "
          f"{sorted(blanket) or 'none'}\n")
    print("  one coordinate changed at a time:\n")
    established = 0
    for row in rows:
        noticed = row["requirements_that_stopped_holding"]
        specific = [name for name in noticed if name not in blanket]
        row["predicates_specific_to_this_coordinate"] = specific
        if row["book_coordinate"].startswith("[control]"):
            mark, detail = "control        ", ", ".join(noticed) or "nothing"
        elif specific:
            established += 1
            mark, detail = "ESTABLISHED    ", ", ".join(specific)
        elif noticed:
            mark, detail = "blanket only   ", (
                f"only {', '.join(noticed)}, which an unnamed coordinate also trips"
            )
        else:
            mark, detail = "NOT established", (
                "no predicate stopped holding"
                if row["coordinate_present_in_material"]
                else "coordinate absent from the recorded material"
            )
        print(f"    {mark} {row['book_coordinate']:{width}}  {detail}")

    stated = [r for r in rows if not r["book_coordinate"].startswith("[control]")]
    print(
        f"\n  {established} of {len(stated)} stated Yield coordinates are "
        f"established by a predicate specific to them"
    )
    print(json.dumps(rows, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
