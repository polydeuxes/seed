"""Compare the two position-coordinate assignment entrances under one control.

Both entrances take the same ledger, the same exact source occurrence, and the
same current Standing.  One is validated against a rebuilt Locality Standing,
the other against its consumed coordinates alone.

Each entrance is run over separately built but identically constructed
material.  The question is what an observer could establish before either
assignment is appended.  No control flag, function name, or validator selection
is read while forming that answer; which entrance was taken is disclosed only
after the observed coordinates have been compared.

Usage:
    .venv/bin/python scripts/compare_standing_entrances.py
"""

from __future__ import annotations

import argparse
from hashlib import sha256
import re
import json
from pathlib import Path
import sys
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from seed_runtime.events import EventLedger
from seed_runtime.operator_locality_standing import read_operator_locality_standing
import seed_runtime.measurement_of_position_coordinates_of_byte_pair_occurrences as position_module

from tests.operator_material_source_test_witness import (
    record_operator_material_occurrence,
)

LOCALITY = "entrance-control"
EXACT = b"2+2=5\n"


def _digest(value: object) -> str:
    return sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":"), default=str).encode(
            "utf-8"
        )
    ).hexdigest()[:16]


def _by_position(value: object, positions: dict[str, str]) -> object:
    """Read every identity as its position in this run's append order.

    Both occurrence identities and the named coordinate counts are allocated
    process-wide, so two identically built ledgers do not carry the same
    strings.  Comparing those strings reports a difference this control did not
    build its material to test.  Nothing recorded is changed; the positions are
    read only to compare the two runs.
    """

    if isinstance(value, dict):
        return {
            _by_position(key, positions): _by_position(item, positions)
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [_by_position(item, positions) for item in value]
    if isinstance(value, tuple):
        return tuple(_by_position(item, positions) for item in value)
    if isinstance(value, str):
        return re.sub(r"_\d{6}\b", "_#", positions.get(value, value))
    return value


def _position_of(ledger: EventLedger) -> dict[str, str]:
    return {
        event.identity: f"#append-{index}"
        for index, event in enumerate(ledger.list())
    }


def _material() -> tuple[EventLedger, Any, dict[str, Any]]:
    """Identically constructed material for one entrance."""

    ledger = EventLedger()
    source = record_operator_material_occurrence(
        ledger,
        locality_identity=LOCALITY,
        exact=EXACT,
        source_boundary="exact supplied material boundary",
    )
    standing = read_operator_locality_standing(ledger, locality_identity=LOCALITY)
    return ledger, source, standing


def _observed_before(ledger: EventLedger, source, standing: dict[str, Any]):
    """Everything observable before the assignment occurrence is appended."""

    occurrences = ledger.list_locality(LOCALITY)
    through = standing.get("through_event_occurrence_identity")
    positions = _position_of(ledger)
    return {
        "source_occurrence_kind": source.kind,
        "source_exact_material_digest": _digest(source.exact_material),
        "source_material_digest": _digest(_by_position(source.material, positions)),
        "source_locality": source.locality_identity,
        "standing_coordinate_names": sorted(standing),
        "standing_digest": _digest(_by_position(standing, positions)),
        "standing_through_occurrence_kind": (
            ledger.get(through).kind if through else None
        ),
        "locality_occurrence_count": len(occurrences),
        "locality_occurrence_kinds": [event.kind for event in occurrences],
        "through_occurrence_is_locality_tip": (
            occurrences[-1].identity == through if occurrences else None
        ),
        "ledger_occurrence_count": len(ledger.list()),
    }


def _recorded_assignment(assignment, positions: dict[str, str]) -> dict[str, Any]:
    return {
        "kind": assignment.kind,
        "locality": assignment.locality_identity,
        "material_coordinate_names": sorted(assignment.material),
        "exact_material_is_none": assignment.exact_material is None,
        "material_digest": _digest(_by_position(assignment.material, positions)),
    }


def main() -> int:
    argparse.ArgumentParser(description=__doc__).parse_args()

    entrances = {
        "first": position_module.record_byte_pair_occurrence_position_measurement_subject_to_act_binding,
        "second": position_module._record_byte_pair_occurrence_position_measurement_subject_to_act_binding_from_carried_standing,
    }

    before: dict[str, Any] = {}
    after: dict[str, Any] = {}
    for label, entrance in entrances.items():
        ledger, source, standing = _material()
        before[label] = _observed_before(ledger, source, standing)
        assignment = entrance(
            ledger,
            source_material_result_occurrence_identity=source.identity,
            locality_standing=standing,
        )
        after[label] = _recorded_assignment(assignment, _position_of(ledger))

    print("  observed before either assignment is appended")
    for key in sorted(before["first"]):
        mark = "same" if before["first"][key] == before["second"][key] else "DIFFER"
        print(f"    {mark:6} {key}")
    print(
        f"\n  every observed coordinate identical before: "
        f"{before['first'] == before['second']}"
    )

    print("\n  recorded assignment after each entrance")
    for key in sorted(after["first"]):
        mark = "same" if after["first"][key] == after["second"][key] else "DIFFER"
        print(f"    {mark:6} {key}")
    print(
        f"\n  recorded assignment identical after: "
        f"{after['first'] == after['second']}"
    )

    print(
        "\n  disclosed only now: first is the public entrance, "
        "second the carried-standing entrance"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
