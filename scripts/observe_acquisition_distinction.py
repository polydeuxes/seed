#!/usr/bin/env python3
"""Cat-test Acquisition against exact material and source occurrences.

The operation records equal exact material through one and two distinct
operator source occurrences, then performs the same declared exact-byte
Measurement. It compares the private content address with the exact occurrence
references and findings carried by the Measurement.

Plain source material is absent from the frozen artifact.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from seed_runtime.byte_measurement import (
    assertions_of_recorded_byte_measurement,
    record_byte_measurement_act_occurrence,
    record_byte_measurement_responsibility_assignment,
    record_byte_measurement_result,
)
from seed_runtime.events import EventLedger
from seed_runtime.operator_locality_standing import read_operator_locality_standing
from tests.operator_material_acquisition_test_witness import (
    record_operator_material_occurrence,
)


OUTPUT = Path("/tmp/seed_acquisition_distinction.json")
_MATERIAL = b"tatatata"


def _encoded(value: object) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode()


def _digest(material: bytes) -> str:
    return sha256(material).hexdigest()


def _measure(occurrence_count: int) -> dict:
    ledger = EventLedger()
    locality = f"acquisition-cat-{occurrence_count}"
    sources = tuple(
        record_operator_material_occurrence(
            ledger,
            locality_identity=locality,
            exact=_MATERIAL,
            source_boundary=f"source-boundary-{number}",
        )
        for number in range(occurrence_count)
    )
    standing = read_operator_locality_standing(
        ledger, locality_identity=locality
    )
    assignment = record_byte_measurement_responsibility_assignment(
        ledger,
        source_localities=(locality,),
        recording_locality_identity=locality,
        locality_standing=standing,
    )
    act = record_byte_measurement_act_occurrence(
        ledger,
        responsibility_assignment_event_identity=assignment.identity,
        responsibility_assignment_standing=read_operator_locality_standing(
            ledger, locality_identity=locality
        ),
    )
    result = record_byte_measurement_result(
        ledger, act_occurrence_event_identity=act.identity
    )
    assertions = assertions_of_recorded_byte_measurement(ledger, result.identity)
    if assertions is None:
        raise ValueError("exact-byte Measurement result is absent")
    source = next(
        assertion
        for assertion in assertions
        if type(assertion.material.get("dimensions")) is dict
        and type(
            assertion.material["dimensions"].get("content")
        ) is dict
        and type(
            assertion.material["dimensions"]["content"].get("source_material")
        ) is list
    )
    source_references = source.material["dimensions"]["content"]["source_material"]
    count_findings = {
        _digest(bytes((assertion.content,))): assertion.material["dimensions"][
            "content"
        ]["count"]
        for assertion in assertions
        if assertion.result == "count" and assertion.content is not None
    }
    private_references = tuple(
        ledger._exact_material_reference(event.identity) for event in sources
    )
    event_material = _encoded([event.material for event in sources])
    return {
        "source_occurrence_count": len(sources),
        "distinct_source_occurrence_count": len(
            dict.fromkeys(event.identity for event in sources)
        ),
        "distinct_result_identity_count": len(
            dict.fromkeys(event.material["result_identity"] for event in sources)
        ),
        "distinct_Act_occurrence_count": len(
            dict.fromkeys(
                event.material["act_occurrence_event_identity"] for event in sources
            )
        ),
        "distinct_Responsibility_assignment_count": len(
            dict.fromkeys(
                event.material["responsibility_assignment_reference"][
                    "recorded_occurrence_identity"
                ]
                for event in sources
            )
        ),
        "distinct_Yield_count": len(
            dict.fromkeys(event.material["yield_relation_identity"] for event in sources)
        ),
        "distinct_private_exact_material_reference_count": len(
            dict.fromkeys(private_references)
        ),
        "private_exact_material_reference_is_carried_by_source_occurrence": any(
            reference is not None and reference.encode() in event_material
            for reference in private_references
        ),
        "source_boundary_sha256": [
            _digest(event.material["source_boundary"].encode()) for event in sources
        ],
        "Measurement_source_occurrence_references": source_references,
        "Measurement_source_occurrence_reference_count": len(source_references),
        "count_findings": count_findings,
        "Measurement_result_carried_in_current_Standing": result.identity
        in read_operator_locality_standing(
            ledger, locality_identity=locality
        )["measurement_occurrences"],
    }


def observe() -> dict:
    one = _measure(1)
    two = _measure(2)
    return {
        "operation": (
            "record equal exact material through one and two distinct source "
            "occurrences; perform the same declared exact-byte Measurement"
        ),
        "exact_material_sha256": _digest(_MATERIAL),
        "one_source_occurrence": one,
        "two_source_occurrences": two,
        "equal_material_has_one_private_reference": (
            two["distinct_private_exact_material_reference_count"] == 1
        ),
        "equal_material_retains_two_exact_source_occurrences": (
            two["distinct_source_occurrence_count"] == 2
            and two["Measurement_source_occurrence_reference_count"] == 2
        ),
        "two_occurrences_double_each_byte_count": all(
            two["count_findings"].get(material_identity) == count * 2
            for material_identity, count in one["count_findings"].items()
        ),
        "known_loss": (
            "the private exact-material reference is an implementation address; "
            "no material-continuity relation is recorded"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()

    started = time.perf_counter()
    result = observe()
    result["wall_seconds"] = round(time.perf_counter() - started, 6)
    encoded = _encoded(result)
    args.output.write_bytes(encoded)
    print(
        json.dumps(
            {
                "artifact": str(args.output),
                "artifact_sha256": _digest(encoded),
                "artifact_bytes": len(encoded),
                "wall_seconds": result["wall_seconds"],
                "equal_material_has_one_private_reference": result[
                    "equal_material_has_one_private_reference"
                ],
                "equal_material_retains_two_exact_source_occurrences": result[
                    "equal_material_retains_two_exact_source_occurrences"
                ],
                "two_occurrences_double_each_byte_count": result[
                    "two_occurrences_double_each_byte_count"
                ],
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
