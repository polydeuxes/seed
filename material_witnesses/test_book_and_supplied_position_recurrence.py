"""Observe later-position recurrence in Book and supplied prose material."""

from __future__ import annotations

from pathlib import Path
import sys

import pytest

from seed_runtime.events import EventLedger
from seed_runtime.witness_material_source import record_witness_material_source


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from compiled_format_invocation import (  # noqa: E402
    exact_position_material_references,
    recurring_position_materials,
)
from compiled_material_invocation import (  # noqa: E402
    material_acquisition_result_reference,
)


def _recurring_material(reference):
    return recurring_position_materials(
        exact_position_material_references(reference),
        material_count=24,
    )


def _assert_later_position_recurrence(recurring):
    assert recurring
    assert any(
        exact_material == current.exact_material
        for _, exact_material, current in recurring
    )
    assert any(
        exact_material != current.exact_material
        for _, exact_material, current in recurring
    )
    assert all(
        first.position < current.position
        and second.position < current.position
        and first.source_reference == second.source_reference
        == current.source_reference
        for (first, second), _, current in recurring
    )


def test_book_and_supplied_material_have_later_position_recurrence():
    supplied_path = ROOT / "corpus" / "english_grimm_fairy_tales.txt"
    if not supplied_path.is_file():
        pytest.skip("supplied fixture material is unavailable")

    ledger = EventLedger()
    book_references = []
    for path in (ROOT / "book_of_seed").rglob("*"):
        if not path.is_file():
            continue
        source_result = record_witness_material_source(
            ledger,
            locality_identity="book-material",
            exact_bytes=path.read_bytes(),
            source_boundary=str(path.relative_to(ROOT)),
        )
        book_references.append(
            material_acquisition_result_reference(ledger, source_result.identity)
        )

    supplied_material = b"".join(
        supplied_path.read_bytes().splitlines(keepends=True)[:300]
    )
    supplied_result = record_witness_material_source(
        ledger,
        locality_identity="supplied-position-material",
        exact_bytes=supplied_material,
        source_boundary="corpus/english_grimm_fairy_tales.txt:first-300-lines",
    )
    supplied_reference = material_acquisition_result_reference(
        ledger, supplied_result.identity
    )

    book_recurring = tuple(
        found
        for reference in book_references
        for found in _recurring_material(reference)
    )
    _assert_later_position_recurrence(book_recurring)
    _assert_later_position_recurrence(_recurring_material(supplied_reference))
