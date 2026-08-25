"""Ask what the broad Yield predicate protects that belongs to the relation.

The broad predicate notices a change to almost any carried coordinate, so a
single substitution tells us nothing about which coordinate it establishes.
This asks a different question: can the predicate be satisfied while a stated
coordinate is false?

A coordinate recorded in more than one occurrence is substituted in every
occurrence that records it, so nothing disagrees.  A predicate that holds
through that is establishing agreement between records, not the coordinate.

Separately, the one occurrence-envelope coordinate the predicate depends on is
varied alone, to see what case its dependency refuses and whether anything else
refuses the same case.

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
    .venv/bin/python scripts/observe_broad_yield_predicate.py
"""

from __future__ import annotations

import argparse
from copy import deepcopy
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

LOCALITY = "broad-predicate"


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


def _read(value: Any, coordinate: str) -> Any:
    if isinstance(value, dict):
        if coordinate in value:
            return value[coordinate]
        for nested in value.values():
            found = _read(nested, coordinate)
            if found is not None:
                return found
    return None


def _substitute_value(value: Any, existing: Any, replacement: Any) -> int:
    """Change every site holding this exact value, whatever key records it.

    Substituting by key name leaves the same value standing wherever another
    key records it, and the predicate then refuses a disagreement this control
    created rather than the coordinate it meant to test.
    """

    changed = 0
    if isinstance(value, dict):
        for key in list(value):
            if value[key] == existing:
                value[key] = replacement
                changed += 1
            else:
                changed += _substitute_value(value[key], existing, replacement)
    elif isinstance(value, list):
        for position, item in enumerate(value):
            if item == existing:
                value[position] = replacement
                changed += 1
            else:
                changed += _substitute_value(item, existing, replacement)
    return changed


CONSISTENT = [
    ("second_subject", "result_identity", "substituted-result"),
    ("Unknown", "unknown", ["substituted"]),
]


def main() -> int:
    argparse.ArgumentParser(description=__doc__).parse_args()

    ledger, result, yield_relation, act_occurrence = _material()
    baseline = _requirements(ledger, result)
    print(f"  baseline: {baseline}\n")

    print("  every site holding the value substituted, in all three occurrences:\n")
    for stated, coordinate, replacement in CONSISTENT:
        ledger, result, yield_relation, act_occurrence = _material()
        existing = _read(result.material, coordinate)
        sites = 0
        for event in (result, yield_relation, act_occurrence):
            material = deepcopy(event.material)
            sites += _substitute_value(material, existing, replacement)
            object.__setattr__(event, "material", material)
        after = _requirements(ledger, result)
        held = all(after.values())
        stopped = sorted(k for k, v in baseline.items() if v and not after[k])
        mark = "ACCEPTED AFTER SUBSTITUTION" if held else "refused"
        print(
            f"    {mark:28} {stated:15} changed at {sites} sites"
            f"   {'' if held else 'stopped: ' + ', '.join(stopped)}"
        )
    print(
        "\n    Acceptance here establishes that agreement among the compared\n"
        "    records is enough for this predicate.  It does not establish that\n"
        "    the substituted coordinate is false: no anchor outside these\n"
        "    occurrences was consulted, so this may be another internally\n"
        "    agreeing result rather than a wrong one."
    )

    print("\n  the same coordinate, substituted at each occurrence recording it:\n")
    for coordinate in ("scope", "unknown", "standing"):
        for holder_name in ("result", "yield_relation", "act_occurrence"):
            ledger, result, yield_relation, act_occurrence = _material()
            target = {
                "result": result,
                "yield_relation": yield_relation,
                "act_occurrence": act_occurrence,
            }[holder_name]
            if coordinate not in target.material:
                print(f"    {'not recorded here':22} {coordinate:10} {holder_name}")
                continue
            material = deepcopy(target.material)
            material[coordinate] = "substituted"
            object.__setattr__(target, "material", material)
            after = _requirements(ledger, result)
            stopped = sorted(k for k, v in baseline.items() if v and not after[k])
            mark = "noticed" if stopped else "NOT NOTICED"
            print(f"    {mark:22} {coordinate:10} {holder_name}")

    print(
        "\n    The result carries a copy of these coordinates and the responsible"
        "\n    Act yield_relation records its own.  The copy is compared; the record is"
        "\n    not."
    )

    print(
        "\n  a distinct intact occurrence of another kind addressed as the\n"
        "  relation witness, with no occurrence rewritten:\n"
    )
    ledger, result, yield_relation, act_occurrence = _material()
    material = deepcopy(result.material)
    material["yield_relation_identity"] = act_occurrence.identity
    object.__setattr__(result, "material", material)
    after = _requirements(ledger, result)
    stopped = sorted(k for k, v in baseline.items() if v and not after[k])
    print(f"    proposed witness kind: {act_occurrence.kind}")
    print(f"    lawful witness kind:   {yield_relation.kind}")
    print(f"    predicates that stopped: {', '.join(stopped) or 'none'}")
    print(
        "\n    This occurrence was recorded by its own lawful recorder and is\n"
        "    intact.  It is refused, but it also carries different material, so\n"
        "    this does not establish that its kind is what refused it."
    )

    print(
        "\n  whether kind alone decides, with the same occurrence identity held\n"
        "  and only the envelope read differently:\n"
    )
    ledger, result, yield_relation, act_occurrence = _material()
    object.__setattr__(yield_relation, "kind", act_occurrence.kind)
    after = _requirements(ledger, result)
    stopped = sorted(k for k, v in baseline.items() if v and not after[k])
    print(f"    predicates that stopped: {', '.join(stopped) or 'none'}")
    print(
        "\n    Reaching this case needed an occurrence's recorded envelope to be\n"
        "    rewritten, which no lawful interface permits.  So the adversary the\n"
        "    kind dependency refuses is not an independently recorded wrong-kind\n"
        "    occurrence; constructing one with otherwise matching material is not\n"
        "    reachable through the recorders, because each sets its own kind and\n"
        "    the material it carries with it.  The dependency is reported here as\n"
        "    sensitivity to kind, and no claim is made that kind is the sole\n"
        "    discriminator for an adversary that cannot be built."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
