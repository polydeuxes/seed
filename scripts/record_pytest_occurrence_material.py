#!/usr/bin/env python3
"""Record occurrence material produced while pytest exercises exact witnesses."""

from __future__ import annotations

import argparse
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from seed_runtime.events import EventLedger, SQLiteEventLedger


def _arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("targets", nargs="+")
    return parser.parse_args()


def _encoded(value: object) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode()


def main() -> int:
    arguments = _arguments()
    occurrences: list[dict[str, object]] = []
    appenders = {
        EventLedger: EventLedger.append,
        SQLiteEventLedger: SQLiteEventLedger.append,
    }
    batch_appenders = {
        EventLedger: EventLedger.append_many,
        SQLiteEventLedger: SQLiteEventLedger.append_many,
    }

    def record(event) -> None:
        occurrences.append(
            {
                "identity": event.identity,
                "event_label": event.kind,
                "material": deepcopy(event.material),
                "exact_material_hex": (
                    None if event.exact_material is None else event.exact_material.hex()
                ),
                "locality_identity": event.locality_identity,
            }
        )

    for ledger_type, append in appenders.items():
        def recording_append(self, *values, _append=append, **coordinates):
            event = _append(self, *values, **coordinates)
            record(event)
            return event

        ledger_type.append = recording_append

    for ledger_type, append_many in batch_appenders.items():
        def recording_append_many(
            self, events, _append_many=append_many
        ):
            recorded = _append_many(self, events)
            for event in recorded:
                record(event)
            return recorded

        ledger_type.append_many = recording_append_many

    pytest_result = pytest.main(
        [
            "-q",
            "--assert=plain",
            "-p",
            "no:cacheprovider",
            *arguments.targets,
        ]
    )
    finding = {
        "operation": (
            "exact occurrence material recorded while pytest exercises supplied "
            "witness paths; event labels retained only for later comparison"
        ),
        "pytest_result": int(pytest_result),
        "occurrence_count": len(occurrences),
        "occurrences": occurrences,
        "known_loss": None if pytest_result == pytest.ExitCode.OK else "pytest refusal",
    }
    encoded = _encoded(finding)
    arguments.output.write_bytes(encoded)
    print(f"artifact: {arguments.output}")
    print(f"artifact bytes: {len(encoded)}")
    print(f"artifact sha256: {sha256(encoded).hexdigest()}")
    print(f"occurrences: {len(occurrences)}")
    return int(pytest_result)


if __name__ == "__main__":
    raise SystemExit(main())
