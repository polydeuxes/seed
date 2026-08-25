"""Inspect one live Seed-to-pytest invocation through Seed's ledger reader."""

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


def inspect_live_pytest_ledger(database: Path) -> dict:
    nodeid = (
        b"tests/test_book_material_acquisition.py::"
        b"test_book_material_witness_has_one_admitted_subject"
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
        raise RuntimeError(result.stderr)

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
    returned_boundaries = {
        "invocation output",
        "invocation error",
        "invocation completion",
    }
    if len(source_results) != 3 or set(by_boundary) != returned_boundaries:
        raise RuntimeError("live pytest invocation omitted exact source results")

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

    output = by_boundary["invocation output"]
    error = by_boundary["invocation error"]
    completion = by_boundary["invocation completion"]
    if not output.exact_material:
        raise RuntimeError("live pytest invocation omitted output material")
    if completion.exact_material != b"":
        raise RuntimeError("live pytest completion material is not exact")

    return {
        "source_result_count": len(source_results),
        "source_boundaries": sorted(by_boundary),
        "output_byte_count": len(output.exact_material),
        "error_byte_count": len(error.exact_material),
        "completion_byte_count": len(completion.exact_material),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--db")
    args = parser.parse_args(argv)
    if args.db:
        report = inspect_live_pytest_ledger(Path(args.db))
    else:
        with TemporaryDirectory(prefix="seed-live-pytest-") as directory:
            report = inspect_live_pytest_ledger(Path(directory) / "seed.db")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
