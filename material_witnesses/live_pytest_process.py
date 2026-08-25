"""Run one live Seed-to-pytest invocation and report its exact source results."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory

from seed_runtime.events import SQLiteEventLedger
from seed_runtime.witness_material_source import (
    WITNESS_MATERIAL_SOURCE_RECORDED_KIND,
)


def observe_live_pytest_process(database: Path) -> dict:
    nodeid = (
        b"tests/test_implementation_function_measurement.py::"
        b"test_compiled_code_supplies_exact_identities"
    )
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "seed_runtime.process_entry",
            "--db",
            str(database),
        ],
        input=b"!pytest " + nodeid + b"\n",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        cwd=str(Path(__file__).resolve().parent.parent),
    )
    if result.returncode:
        raise RuntimeError(result.stderr.decode("utf-8", errors="replace"))

    ledger = SQLiteEventLedger(database)
    try:
        source_results = [
            event
            for event in ledger.list()
            if event.kind == WITNESS_MATERIAL_SOURCE_RECORDED_KIND
        ]
    finally:
        ledger.close()

    by_boundary = {
        event.material["source_boundary"]: event for event in source_results
    }
    required_boundaries = {
        "implementation function catalog",
        "implementation function measurement",
        "invocation completion",
    }
    if len(source_results) < 6 or not required_boundaries <= set(by_boundary):
        raise RuntimeError("live pytest invocation omitted exact source results")
    if not all(
        event.material["source_boundary"].startswith(
            ("invocation output occurrence ", "invocation error occurrence ")
        )
        or event.material["source_boundary"] in required_boundaries
        for event in source_results
    ):
        raise RuntimeError("live pytest invocation carried another source boundary")

    provenance = [
        event.material["provenance_occurrence_references"]
        for event in source_results
    ]
    source_result_identities = {event.identity for event in source_results}
    if not all(type(references) is list and len(references) >= 2 for references in provenance):
        raise RuntimeError("live pytest source provenance is incomplete")
    if len({tuple(references[:2]) for references in provenance}) != 1:
        raise RuntimeError("live pytest source provenance crossed its invocation")
    if not set(provenance[0][:2]).isdisjoint(source_result_identities):
        raise RuntimeError("live pytest source provenance cites its own results")
    if not all(
        set(references[2:]) <= source_result_identities
        for references in provenance
    ):
        raise RuntimeError("live pytest source provenance cites another result")

    catalog = by_boundary["implementation function catalog"]
    measurement = by_boundary["implementation function measurement"]
    completion = by_boundary["invocation completion"]
    if not catalog.exact_material or not measurement.exact_material:
        raise RuntimeError("live pytest invocation omitted exact result material")
    if completion.exact_material != b"":
        raise RuntimeError("live pytest completion material is not exact")

    return {
        "source_result_count": len(source_results),
        "source_boundaries": sorted(by_boundary),
        "catalog_byte_count": len(catalog.exact_material),
        "measurement_byte_count": len(measurement.exact_material),
        "completion_byte_count": len(completion.exact_material),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--db")
    args = parser.parse_args(argv)
    if args.db:
        report = observe_live_pytest_process(Path(args.db))
    else:
        with TemporaryDirectory(prefix="seed-live-pytest-") as directory:
            report = observe_live_pytest_process(Path(directory) / "seed.db")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
