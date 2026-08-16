from __future__ import annotations

from dataclasses import replace
from pathlib import Path
import sys

import pytest

from seed_runtime.events import EventLedger
from seed_runtime.material_ingest import MATERIAL_INGEST_OCCURRED_KIND, ingest_material


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from compiled_format_invocation import (  # noqa: E402
    COMPILED_IMPLEMENTATION_FUNCTIONS,
    admit_compiled_invocation_rows,
    compiled_reference_invocations,
)
from compiled_material_invocation import ingest_result_reference  # noqa: E402


@pytest.fixture(scope="module")
def acquired_book_material():
    ledger = EventLedger()
    paths = tuple(
        path
        for path in sorted((ROOT / "book_of_seed").rglob("*"))
        if path.is_file()
    )
    ingests = tuple(
        ingest_material(
            ledger,
            locality_identity="book-material-acquisition",
            exact_bytes=path.read_bytes(),
            source_role="fixture material",
            source_boundary=str(path.relative_to(ROOT)),
        )
        for path in paths
    )
    completeness_boundary = ledger.append_boundary()
    references = tuple(
        ingest_result_reference(ledger, occurrence.identity)
        for occurrence in ingests
    )
    invocation_rows = compiled_reference_invocations(
        references,
        boundary_identity="book-material-acquisition-invocation",
        implementation_functions=COMPILED_IMPLEMENTATION_FUNCTIONS,
    )
    admission = admit_compiled_invocation_rows(
        invocation_rows,
        boundary_identity="book-material-acquisition-admission",
    )
    return (
        ledger,
        paths,
        ingests,
        completeness_boundary,
        references,
        invocation_rows,
        admission,
    )


def test_every_current_book_file_has_one_exact_ingest_result(
    acquired_book_material,
):
    ledger, paths, ingests, boundary, references, _, _ = acquired_book_material
    bounded_ingests = tuple(
        occurrence
        for occurrence in ledger.list_locality(
            "book-material-acquisition", through=boundary
        )
        if occurrence.kind == MATERIAL_INGEST_OCCURRED_KIND
    )

    assert paths == tuple(
        path
        for path in sorted((ROOT / "book_of_seed").rglob("*"))
        if path.is_file()
    )
    assert bounded_ingests == ingests
    assert tuple(reference.recorded_occurrence_identity for reference in references) == tuple(
        occurrence.identity for occurrence in ingests
    )
    assert tuple(reference.exact_material for reference in references) == tuple(
        path.read_bytes() for path in paths
    )
    assert len({reference.result_identity for reference in references}) == len(paths)
    assert len({reference.act_occurrence_identity for reference in references}) == len(
        paths
    )
    assert all(
        reference.locality_identity == "book-material-acquisition"
        for reference in references
    )
    assert tuple(occurrence.material["source_boundary"] for occurrence in ingests) == tuple(
        str(path.relative_to(ROOT)) for path in paths
    )
    assert all(
        occurrence.material["dimensions"]["authority"] == "unestablished"
        for occurrence in ingests
    )


def test_every_function_receives_the_same_complete_book_source(
    acquired_book_material,
):
    _, paths, _, _, references, invocation_rows, _ = acquired_book_material

    assert len(invocation_rows) == len(COMPILED_IMPLEMENTATION_FUNCTIONS)
    assert tuple(
        row[0].implementation_function_identity for row in invocation_rows
    ) == tuple(function.identity for function in COMPILED_IMPLEMENTATION_FUNCTIONS)
    assert all(
        tuple(occurrence.source_coordinate for occurrence in row) == references
        for row in invocation_rows
    )
    assert all(
        tuple(occurrence.exact_material for occurrence in row)
        == tuple(path.read_bytes() for path in paths)
        for row in invocation_rows
    )
    assert all(
        tuple(occurrence.invocation_position for occurrence in row)
        == tuple(range(len(paths)))
        for row in invocation_rows
    )


def test_this_exact_book_is_admitted_under_the_exact_invocation_coordinates(
    acquired_book_material,
):
    _, _, _, _, references, invocation_rows, admission = acquired_book_material

    assert admission.source_material == references
    assert {
        reference
        for same_coordinates in admission.admitted_material
        for reference in same_coordinates
    } == set(references)
    assert len(admission.invocation_result_references) == (
        len(references) * len(invocation_rows)
    )
    assert tuple(
        reference.invocation_occurrence
        for reference in admission.invocation_result_references
    ) == tuple(occurrence for row in invocation_rows for occurrence in row)


def test_book_admission_refuses_an_incomplete_reordered_or_repeated_function_row(
    acquired_book_material,
):
    _, _, _, _, _, invocation_rows, _ = acquired_book_material

    with pytest.raises(ValueError, match="same exact material"):
        admit_compiled_invocation_rows(
            (invocation_rows[0], invocation_rows[1][:-1]),
            boundary_identity="incomplete-book-material-admission",
        )
    with pytest.raises(ValueError, match="same exact material"):
        admit_compiled_invocation_rows(
            (invocation_rows[0], tuple(reversed(invocation_rows[1]))),
            boundary_identity="reordered-book-material-admission",
        )
    with pytest.raises(ValueError, match="one exact function"):
        admit_compiled_invocation_rows(
            (invocation_rows[0], invocation_rows[0]),
            boundary_identity="repeated-book-function-admission",
        )


def test_later_material_does_not_enter_the_book_completeness_boundary(
    acquired_book_material,
):
    ledger, _, ingests, boundary, _, _, _ = acquired_book_material
    later = ingest_material(
        ledger,
        locality_identity="book-material-acquisition",
        exact_bytes=b"later material",
        source_role="fixture material",
        source_boundary="later",
    )

    bounded_ingests = tuple(
        occurrence
        for occurrence in ledger.list_locality(
            "book-material-acquisition", through=boundary
        )
        if occurrence.kind == MATERIAL_INGEST_OCCURRED_KIND
    )
    assert bounded_ingests == ingests
    assert later not in bounded_ingests


def test_book_admission_recomputes_from_its_exact_invocation_results(
    acquired_book_material,
):
    _, _, _, _, _, invocation_rows, admission = acquired_book_material
    altered = replace(
        invocation_rows[0][0],
        returned=not invocation_rows[0][0].returned,
    )

    with pytest.raises(ValueError, match="differs from its invocation results"):
        replace(
            admission,
            invocation_result_references=(
                replace(
                    admission.invocation_result_references[0],
                    invocation_occurrence=altered,
                ),
                *admission.invocation_result_references[1:],
            ),
        )
