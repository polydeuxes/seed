"""Change what an Authority producer emits and observe what follows.

Counting where a read value goes is a syntactic reading and cannot establish
that no outcome depends on it.  A value reached through a helper, an alias, or
a call is carried in that count as though nothing consulted it.

So the value is changed at its producer and one lawful sequence is recorded
twice, once with each.  Everything the two runs produce is then compared:
occurrence kinds, the order they were recorded in, refusals, the Yield gate's
answer, and the recorded material itself.

The producer takes no argument, so there is no lawful input boundary at which
this value can be varied.  That is reported rather than worked around: the
substitution here replaces the producer, which no caller can do.

Usage:
    .venv/bin/python scripts/observe_authority_perturbation.py
"""

from __future__ import annotations

import argparse
from hashlib import sha256
import inspect
import json
from pathlib import Path
import re
import sys
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from seed_runtime.events import EventLedger
from seed_runtime.yield_relation import (
    read_requirements_of_yield_relation,
)
import seed_runtime.operator_material_acquisition as acquisition

from tests.operator_material_acquisition_test_witness import (
    record_operator_material_occurrence,
)

LOCALITY = "authority-perturbation"


def _by_position(value: Any, positions: dict[str, str]) -> Any:
    """Read identities and counted names as their position, so runs compare."""

    if isinstance(value, dict):
        return {
            _by_position(key, positions): _by_position(item, positions)
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [_by_position(item, positions) for item in value]
    if isinstance(value, str):
        return re.sub(r"_\d{6}\b", "_#", positions.get(value, value))
    return value


def _run() -> dict[str, Any]:
    ledger = EventLedger()
    refusal = None
    try:
        result = record_operator_material_occurrence(
            ledger,
            locality_identity=LOCALITY,
            exact=b"2+2=5\n",
            source_boundary="exact supplied material boundary",
        )
    except Exception as error:
        return {"refusal": f"{type(error).__name__}: {error}"}

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
    occurrences = ledger.list()
    positions = {
        event.identity: f"#append-{index}" for index, event in enumerate(occurrences)
    }
    return {
        "refusal": refusal,
        "occurrence_kinds_in_order": [event.kind for event in occurrences],
        "occurrence_count": len(occurrences),
        "yield_gate": dict(sorted(requirements.items())),
        "exact_material": [
            None if event.exact_material is None else event.exact_material.hex()
            for event in occurrences
        ],
        "material": [_by_position(event.material, positions) for event in occurrences],
    }


def main() -> int:
    argparse.ArgumentParser(description=__doc__).parse_args()

    signature = inspect.signature(acquisition._authority)
    print(f"  producer: _authority{signature}")
    print(f"  parameters: {list(signature.parameters) or 'none'}")
    print(
        "  so no caller can vary it, and there is no lawful input boundary to\n"
        "  perturb.  The producer itself is replaced below, which no lawful\n"
        "  sequence can do.\n"
    )

    original = acquisition._authority
    before = _run()
    substituted = dict(original())
    substituted["standing"] = "substituted standing"
    substituted["limit"] = "a different sentence entirely"
    substituted["source"] = "not the active Book"
    acquisition._authority = lambda: dict(substituted)
    try:
        after = _run()
    finally:
        acquisition._authority = original

    print("  what the two runs produced:\n")
    for key in (
        "refusal",
        "occurrence_count",
        "occurrence_kinds_in_order",
        "yield_gate",
        "exact_material",
    ):
        same = before.get(key) == after.get(key)
        print(f"    {'same' if same else 'DIFFERS':8} {key}")

    material_same = before["material"] == after["material"]
    print(f"    {'same' if material_same else 'DIFFERS':8} recorded material")

    carried = 0
    for one, other in zip(before["material"], after["material"]):
        carried += sum(
            1
            for path, value in _paths(one)
            if _at(other, path) != value
        )
    print(f"\n  coordinates whose recorded value differs: {carried}")
    print(
        "\n  Everything the sequence produced apart from the recorded material is\n"
        "  unchanged when the value is changed at its producer, so nothing this\n"
        "  sequence reaches decided anything by it.  A consumer outside this\n"
        "  sequence is not addressed here."
    )
    return 0


def _paths(value: Any, path: tuple = ()):
    if isinstance(value, dict):
        for key, nested in value.items():
            yield from _paths(nested, path + (key,))
    elif isinstance(value, list):
        for position, nested in enumerate(value):
            yield from _paths(nested, path + (position,))
    else:
        yield path, value


def _at(value: Any, path: tuple) -> Any:
    for part in path:
        try:
            value = value[part]
        except (KeyError, IndexError, TypeError):
            return object()
    return value


if __name__ == "__main__":
    raise SystemExit(main())
