"""Follow the one forwarded Authority back to whatever produced it.

Eleven Authority origins declare a value.  One does not: it returns an
Authority already recorded on another occurrence and carries it onward.  Where
that value came from is a question about provenance, not about that reader.

So the chain is followed by substitution rather than by reading.  Each
declaring producer is changed in turn, one lawful movement road is recorded,
and the forwarded value is read.  The producer whose change reaches it is the
one the chain terminates in.

If no substitution reaches it, the chain terminates somewhere this road does
not exercise, and that is reported rather than guessed.

Usage:
    .venv/bin/python scripts/observe_forwarded_authority_provenance.py
"""

from __future__ import annotations

import argparse
from hashlib import sha256
import importlib
import json
from pathlib import Path
import sys
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

DECLARING = [
    ("addressed_byte_occurrence_reference_determination", "_authority"),
    ("comparison_of_ordered_path_source_position_material", "_authority"),
    ("comparison_of_ordered_relation_path_with_recorded_pair_findings", "_authority"),
    ("comparison_of_recorded_byte_pair_measurements", "_authority"),
    ("measurement_of_shared_position_of_byte_pair_occurrences", "_authority"),
    ("operator_checkpoint", "_authority"),
    ("operator_material_acquisition", "_authority"),
    ("standing_boundary_locality", "_authority"),
    ("byte_measurement", "_authority"),
]

MARK = "traced substitution"


def _digest(value: object) -> str:
    return sha256(
        json.dumps(value, sort_keys=True, default=str).encode("utf-8")
    ).hexdigest()[:12]


def _forwarded() -> Any:
    """The Authority the movement assignment carries, read from its material."""

    from seed_runtime.byte_measurement import (
        record_assertion_locality_movement_responsibility_assignment,
    )
    from seed_runtime.operator_locality_standing import (
        read_operator_locality_standing,
    )
    from tests.test_byte_measurement import _ledger, _movement_source

    ledger = _ledger("ta\n")
    source_result, source = _movement_source(ledger)
    assignment = record_assertion_locality_movement_responsibility_assignment(
        ledger,
        source=source,
        destination_locality="movement",
        source_locality_standing=read_operator_locality_standing(
            ledger, locality_identity=source_result.locality_identity
        ),
        destination_locality_standing=read_operator_locality_standing(
            ledger, locality_identity="movement"
        ),
    )
    return assignment.material.get("authority")


def main() -> int:
    argparse.ArgumentParser(description=__doc__).parse_args()

    baseline = _forwarded()
    print(f"  the forwarded Authority: {json.dumps(baseline, default=str)[:140]}")
    print(f"  digest: {_digest(baseline)}\n")

    print("  each declaring producer changed in turn:\n")
    reached = []
    for module_name, producer_name in DECLARING:
        module = importlib.import_module(f"seed_runtime.{module_name}")
        producer = getattr(module, producer_name, None)
        if producer is None:
            print(f"    {'no such producer':24} {module_name}.{producer_name}")
            continue

        def substituted(*arguments, _producer=producer, **keywords):
            produced = _producer(*arguments, **keywords)
            if isinstance(produced, dict):
                changed = dict(produced)
                changed["standing"] = MARK
                return changed
            return produced

        setattr(module, producer_name, substituted)
        try:
            after = _forwarded()
        except Exception as error:
            after = f"{type(error).__name__}"
        finally:
            setattr(module, producer_name, producer)

        moved = _digest(after) != _digest(baseline)
        if moved:
            reached.append(f"{module_name}.{producer_name}")
        print(
            f"    {'REACHES IT' if moved else 'does not reach it':24} "
            f"{module_name}.{producer_name}"
        )

    print(
        f"\n  producers whose change reaches the forwarded value: "
        f"{', '.join(reached) or 'none of those tried'}"
    )
    if not reached:
        print(
            "\n    So this road does not carry the value from any producer changed\n"
            "    here.  Where it originates is unresolved rather than absent."
        )
    print(
        "\n  This follows the value by changing what declares it and reading what\n"
        "  arrives.  It does not read the chain, and it says nothing about roads\n"
        "  it does not record."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
