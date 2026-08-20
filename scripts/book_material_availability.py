#!/usr/bin/env python3

from __future__ import annotations

from pathlib import Path
import sys

SCRIPT_DIRECTORY = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIRECTORY))
sys.path.insert(0, str(SCRIPT_DIRECTORY.parent))

from seed_runtime.events import EventLedger
from seed_runtime.witness_material_acquisition import (
    record_witness_material_acquisition,
)


def acquired_book_material():
    """Record exact Book files as Witness material without Measurement pressure."""

    ledger = EventLedger()
    paths = tuple(
        path
        for path in (SCRIPT_DIRECTORY.parent / "book_of_seed").rglob("*")
        if path.is_file()
    )
    acquisition_results = tuple(
        record_witness_material_acquisition(
            ledger,
            locality_identity="book-material",
            exact_bytes=path.read_bytes(),
            source_boundary=str(path.relative_to(SCRIPT_DIRECTORY.parent)),
        )
        for path in paths
    )
    return ledger, paths, acquisition_results
