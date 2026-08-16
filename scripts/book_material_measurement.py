#!/usr/bin/env python3

from __future__ import annotations

from pathlib import Path
import sys

SCRIPT_DIRECTORY = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIRECTORY))
sys.path.insert(0, str(SCRIPT_DIRECTORY.parent))

from compiled_format_invocation import (
    exact_byte_pair_material_references,
    moved_exact_byte_material_references,
)
from seed_runtime.byte_measurement import (
    record_byte_count_layer,
    record_byte_position_pair_count_layer,
)
from seed_runtime.events import EventLedger
from seed_runtime.material_ingest import ingest_material


def measured_book_material():
    ledger = EventLedger()
    paths = tuple(
        path
        for path in sorted((SCRIPT_DIRECTORY.parent / "book_of_seed").rglob("*"))
        if path.is_file()
    )
    for path in paths:
        ingest_material(
            ledger,
            locality_identity="book-material",
            exact_bytes=path.read_bytes(),
            source_role="fixture material",
            source_boundary=str(path.relative_to(SCRIPT_DIRECTORY.parent)),
        )
    byte_occurrence = record_byte_count_layer(
        ledger,
        source_localities=("book-material",),
        recording_locality_identity="book-byte-measurement",
    )
    pair_occurrence = record_byte_position_pair_count_layer(
        ledger,
        source_measurement_event_identity=byte_occurrence.identity,
        recording_locality_identity="book-pair-measurement",
    )
    return (
        ledger,
        exact_byte_pair_material_references(ledger, pair_occurrence.identity),
        moved_exact_byte_material_references(
            ledger,
            byte_occurrence.identity,
            destination_locality="book-pair-measurement",
        ),
    )
