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
from seed_runtime.evidence_of_yield_relation import (
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


def _substitute_everywhere(value: Any, coordinate: str, replacement: Any) -> int:
    """Change one coordinate wherever it is recorded.  Returns how many sites."""

    changed = 0
    if isinstance(value, dict):
        for key in list(value):
            if key == coordinate:
                value[key] = replacement
                changed += 1
            else:
                changed += _substitute_everywhere(value[key], coordinate, replacement)
    elif isinstance(value, list):
        for item in value:
            changed += _substitute_everywhere(item, coordinate, replacement)
    return changed


# Coordinates recorded by more than one occurrence.  The same coordinate name
# answers differently depending on which occurrence carries the substitution,
# so each carrier is asked separately.
CARRIED_IN_SEVERAL = ("authority", "scope", "limits", "unknown", "standing")

CONSISTENT = [
    ("second_subject", "result_identity", "substituted-result"),
    ("limits", "limits", ["substituted"]),
    ("Unknown", "unknown", ["substituted"]),
]


def main() -> int:
    argparse.ArgumentParser(description=__doc__).parse_args()

    ledger, result, evidence, act_evidence = _material()
    baseline = _requirements(ledger, result)
    print(f"  baseline: {baseline}\n")

    print("  the coordinate substituted in every occurrence that records it:\n")
    for stated, coordinate, replacement in CONSISTENT:
        ledger, result, evidence, act_evidence = _material()
        sites = 0
        for event in (result, evidence, act_evidence):
            material = deepcopy(event.material)
            sites += _substitute_everywhere(material, coordinate, replacement)
            object.__setattr__(event, "material", material)
        after = _requirements(ledger, result)
        held = all(after.values())
        stopped = sorted(k for k, v in baseline.items() if v and not after[k])
        mark = "SATISFIED WHILE FALSE" if held else "refused"
        print(
            f"    {mark:22} {stated:15} changed at {sites} recorded sites"
            f"   {'' if held else 'stopped: ' + ', '.join(stopped)}"
        )

    print("\n  the same coordinate, substituted at each occurrence recording it:\n")
    for coordinate in CARRIED_IN_SEVERAL:
        for holder_name in ("result", "evidence", "act_evidence"):
            ledger, result, evidence, act_evidence = _material()
            target = {
                "result": result,
                "evidence": evidence,
                "act_evidence": act_evidence,
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
        "\n    Act evidence records its own.  The copy is compared; the record is"
        "\n    not.  A result carrying one Authority while its Act evidence records"
        "\n    another is admitted."
    )

    print(
        "\n  the one envelope coordinate the broad predicate depends on,"
        "\n  varied alone with the occurrence identity held:\n"
    )
    ledger, result, evidence, act_evidence = _material()
    original_kind = evidence.kind
    other_kind = act_evidence.kind
    object.__setattr__(evidence, "kind", other_kind)
    after = _requirements(ledger, result)
    stopped = sorted(k for k, v in baseline.items() if v and not after[k])
    print(f"    Yield evidence recorded as {original_kind}")
    print(f"    read instead as            {other_kind}")
    print(
        f"    predicates that stopped:   {', '.join(stopped) or 'none'}"
        f"   ({len(stopped)} of {len(baseline)})"
    )
    print(
        "\n    every other observed coordinate of that occurrence is unchanged,"
        "\n    so this is the case the dependency refuses: an occurrence whose"
        "\n    recorded material agrees throughout, standing as the relation"
        "\n    occurrence while recorded as something else."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
