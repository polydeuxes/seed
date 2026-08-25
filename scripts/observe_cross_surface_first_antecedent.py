#!/usr/bin/env python3
"""Measure the live coordinates preceding cross-surface aperture work.

This operation records the four raw sources through their exact acquisition
physiology, performs the already-live exact-byte Measurement separately for
each source, and compares its count findings with the first aperture inventory
of the frozen cross-surface observer.

It does not perform the aperture operation or add a Responsibility for it.
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
from scripts.observe_cross_surface_structure import SOURCE_GROUPS, _projections
from tests.operator_material_acquisition_test_witness import (
    record_operator_material_occurrence,
)


OUTPUT = Path("/tmp/seed_cross_surface_first_antecedent.json")


def _encoded(value: object) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode()


def _digest(material: bytes) -> str:
    return sha256(material).hexdigest()


def _record_source(ledger: EventLedger, source_number: int, exact: bytes) -> dict:
    locality = f"cross-surface-antecedent-{source_number}"
    source = record_operator_material_occurrence(
        ledger,
        locality_identity=locality,
        exact=exact,
        source_boundary="cross-surface antecedent source",
    )
    standing_before = read_operator_locality_standing(
        ledger, locality_identity=locality
    )
    assignment = record_byte_measurement_responsibility_assignment(
        ledger,
        source_localities=(locality,),
        recording_locality_identity=locality,
        locality_standing=standing_before,
    )
    standing_with_assignment = read_operator_locality_standing(
        ledger, locality_identity=locality
    )
    act = record_byte_measurement_act_occurrence(
        ledger,
        responsibility_assignment_event_identity=assignment.identity,
        responsibility_assignment_standing=standing_with_assignment,
    )
    result = record_byte_measurement_result(
        ledger, act_occurrence_event_identity=act.identity
    )
    standing_after = read_operator_locality_standing(
        ledger, locality_identity=locality
    )
    assertions = assertions_of_recorded_byte_measurement(ledger, result.identity)
    if assertions is None:
        raise ValueError("exact-byte Measurement result is absent")
    count_findings = {
        finding.content: finding.material["dimensions"]["content"]["count"]
        for finding in assertions
        if finding.result == "count"
    }
    if None in count_findings:
        raise ValueError("one exact-byte count finding carries no byte material")

    before_projection_observer = len(ledger.list())
    projections = _projections(source_number, exact)
    projection_observer_ledger_occurrence_count = (
        len(ledger.list()) - before_projection_observer
    )
    row_boundaries = {
        projection["row_boundary_sha256"] for projection in projections
    }
    item_boundaries = {
        projection["item_boundary_sha256"] for projection in projections
    }
    counted = {
        _digest(bytes((content,))): count for content, count in count_findings.items()
    }
    yielded = ledger.get(result.material["yield_relation_identity"])
    if yielded is None:
        raise ValueError("exact-byte Measurement result carries no Yield")
    order = ledger.occurrences_in_append_order(
        (assignment.identity, act.identity, yielded.identity, result.identity),
        locality_identity=locality,
    )
    return {
        "source_number": source_number,
        "source_material_sha256": _digest(exact),
        "source_byte_count": len(exact),
        "distinct_source_byte_count": len(set(exact)),
        "count_finding_count": len(count_findings),
        "counted_material": [
            {"material_sha256": identity, "count": counted[identity]}
            for identity in sorted(counted)
        ],
        "count_findings_equal_every_distinct_source_byte": (
            set(count_findings) == set(exact)
        ),
        "projection_count": len(projections),
        "all_projection_row_apertures_have_count_findings": row_boundaries
        <= counted.keys(),
        "all_projection_item_apertures_have_count_findings": item_boundaries
        <= counted.keys(),
        "projection_observer_ledger_occurrence_count": (
            projection_observer_ledger_occurrence_count
        ),
        "Responsibility_precedes_Act_Yield_and_result": tuple(
            event.identity for event in order
        )
        == (assignment.identity, act.identity, yielded.identity, result.identity),
        "result_carried_as_Measurement_in_current_Standing": result.identity
        in standing_after["measurement_occurrences"],
        "result_carried_with_exact_Responsibility_in_current_Standing": result.identity
        in standing_after["exact_result_occurrences"],
    }


def observe() -> dict:
    ledger = EventLedger()
    sources = [
        _record_source(ledger, source_number, exact)
        for source_number, exact in enumerate(SOURCE_GROUPS[0])
    ]
    return {
        "operation": (
            "exact acquisition and exact-byte Measurement for each raw source; "
            "comparison with every first-aperture material in the frozen "
            "cross-surface operation"
        ),
        "source_count": len(sources),
        "sources": sources,
        "all_distinct_source_bytes_have_count_findings": all(
            source["count_findings_equal_every_distinct_source_byte"]
            for source in sources
        ),
        "all_projection_apertures_have_count_findings": all(
            source["all_projection_row_apertures_have_count_findings"]
            and source["all_projection_item_apertures_have_count_findings"]
            for source in sources
        ),
        "all_results_have_exact_Standing_ownership": all(
            source["result_carried_as_Measurement_in_current_Standing"]
            and source[
                "result_carried_with_exact_Responsibility_in_current_Standing"
            ]
            for source in sources
        ),
        "projection_observer_ledger_occurrence_count": sum(
            source["projection_observer_ledger_occurrence_count"]
            for source in sources
        ),
        "known_loss": None,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    arguments = parser.parse_args()

    begun = time.perf_counter()
    finding = observe()
    encoded = _encoded(finding)
    arguments.output.write_bytes(encoded)
    print(f"artifact: {arguments.output}")
    print(f"artifact bytes: {len(encoded)}")
    print(f"artifact sha256: {_digest(encoded)}")
    print(f"sources: {finding['source_count']}")
    print(
        "all distinct bytes measured: "
        f"{finding['all_distinct_source_bytes_have_count_findings']}"
    )
    print(
        "all aperture materials measured: "
        f"{finding['all_projection_apertures_have_count_findings']}"
    )
    print(f"wall seconds: {time.perf_counter() - begun:.3f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
