from __future__ import annotations

from dataclasses import replace
from pathlib import Path
import sys

import pytest

from seed_runtime.events import EventLedger
from seed_runtime.material_ingest import ingest_material


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from compiled_format_invocation import (  # noqa: E402
    COMPILED_IMPLEMENTATION_FUNCTIONS,
    compare_compiled_reference_invocations,
    compiled_reference_invocations,
    exact_material_partition_references,
)
from compiled_material_invocation import (  # noqa: E402
    MATERIAL_IMPLEMENTATION_FUNCTIONS,
    compare_material_reference_invocations,
    ingest_result_reference,
    reference_occurrences_across,
)
from material_fixture_books import (  # noqa: E402
    MATERIAL_WINDOWS,
    supplied_book_material,
)


@pytest.fixture(scope="module")
def exact_casting_material():
    paths = tuple(ROOT / "corpus" / name for name, _ in MATERIAL_WINDOWS)
    if any(not path.is_file() for path in paths):
        pytest.skip("supplied fixture material is unavailable")
    books = supplied_book_material(ROOT)
    ledger = EventLedger()
    occurrences = tuple(
        ingest_material(
            ledger,
            locality_identity=locality,
            exact_bytes=material,
            source_role="fixture material",
            source_boundary=boundary,
        )
        for locality, material, boundary in (
            (
                "material-casting-corpus",
                b"".join(books),
                "sixteen supplied books",
            ),
            (
                "material-casting-operator",
                b"what does this exact material distinguish?\n",
                "operator material",
            ),
            (
                "material-casting-today",
                b"one bounded session material\n",
                "today material",
            ),
            (
                "material-casting-lineage",
                b"one exact earlier lineage material\n",
                "lineage material",
            ),
        )
    )
    corpus_reference, operator_reference, today_reference, lineage_reference = tuple(
        ingest_result_reference(ledger, occurrence.identity)
        for occurrence in occurrences
    )
    return (
        books,
        corpus_reference,
        exact_material_partition_references(
            corpus_reference,
            tuple(map(len, books)),
        ),
        operator_reference,
        today_reference,
        lineage_reference,
    )


def test_sixteen_books_are_exact_references_into_one_material_occurrence(
    exact_casting_material,
):
    books, corpus_reference, book_references, *_ = exact_casting_material

    assert len(book_references) == len(MATERIAL_WINDOWS) == 16
    assert tuple(reference.exact_material for reference in book_references) == books
    assert {reference.source_reference for reference in book_references} == {
        corpus_reference
    }
    assert tuple(reference.first_position for reference in book_references) == tuple(
        sum(map(len, books[:position])) for position in range(len(books))
    )
    assert tuple(reference.last_position for reference in book_references) == tuple(
        sum(map(len, books[: position + 1])) - 1
        for position in range(len(books))
    )


def _cast_against_books(subject, books, *, boundary_identity):
    references = (subject, *books)
    invocations = compiled_reference_invocations(
        references,
        boundary_identity=f"{boundary_identity}-invocation",
    )
    compiled_comparisons = compare_compiled_reference_invocations(
        invocations,
        tuple((subject, book) for book in books),
        boundary_identity=f"{boundary_identity}-compare",
    )
    material_invocations = reference_occurrences_across(
        references,
        boundary_identity=f"{boundary_identity}-material-invocation",
        implementation_functions=MATERIAL_IMPLEMENTATION_FUNCTIONS,
        max_workers=16,
        time_limit_second_count=5.0,
        material_byte_count_limit=4096,
    )
    material_comparisons = compare_material_reference_invocations(
        material_invocations,
        tuple((subject, book) for book in books),
        boundary_identity=f"{boundary_identity}-material-compare",
    )
    return (
        references,
        invocations,
        compiled_comparisons,
        material_invocations,
        material_comparisons,
    )


def test_operator_today_and_lineage_material_are_discriminated_in_separate_castings(
    exact_casting_material,
):
    _, _, books, operator, today, lineage = exact_casting_material
    castings = tuple(
        _cast_against_books(subject, books, boundary_identity=name)
        for name, subject in (
            ("operator", operator),
            ("today", today),
            ("lineage", lineage),
        )
    )

    for (
        references,
        invocations,
        compiled_comparisons,
        material_invocations,
        material_comparisons,
    ), subject in zip(
        castings, (operator, today, lineage)
    ):
        assert references == (subject, *books)
        assert len(invocations) == len(COMPILED_IMPLEMENTATION_FUNCTIONS)
        assert all(len(row) == 17 for row in invocations)
        assert len(compiled_comparisons) == len(COMPILED_IMPLEMENTATION_FUNCTIONS)
        assert len(material_invocations) == len(MATERIAL_IMPLEMENTATION_FUNCTIONS)
        assert all(len(row) == 17 for row in material_invocations)
        assert len(material_comparisons) == len(MATERIAL_IMPLEMENTATION_FUNCTIONS)
        comparisons = (*compiled_comparisons, *material_comparisons)
        assert len(comparisons) == 9
        assert all(len(row) == 16 for row in comparisons)
        assert all(
            comparison.first_reference == subject
            for row in comparisons
            for comparison in row
        )
        assert tuple(
            comparison.second_reference for comparison in comparisons[0]
        ) == books
        assert len(
            {
                comparison.occurrence_identity
                for row in comparisons
                for comparison in row
            }
        ) == (
            len(COMPILED_IMPLEMENTATION_FUNCTIONS)
            + len(MATERIAL_IMPLEMENTATION_FUNCTIONS)
        ) * len(books)

    assert (
        castings[0][2][0][0].occurrence_identity
        != castings[1][2][0][0].occurrence_identity
    )
    assert all(
        today not in (comparison.first_reference, comparison.second_reference)
        and lineage not in (comparison.first_reference, comparison.second_reference)
        for row in (*castings[0][2], *castings[0][4])
        for comparison in row
    )
    assert any(
        comparison.distinction
        for row in castings[0][4]
        for comparison in row
    )


def test_casting_stops_at_compare_without_granting_admission_or_applicability(
    exact_casting_material,
):
    _, _, books, operator, *_ = exact_casting_material
    casting = _cast_against_books(
        operator, books, boundary_identity="bounded-operator"
    )
    comparisons = (*casting[2], *casting[4])

    assert {
        comparison.distinction
        for row in comparisons
        for comparison in row
    } <= {False, True}
    assert all(
        not hasattr(comparison, "admitted_material")
        and not hasattr(comparison, "applicability")
        for row in comparisons
        for comparison in row
    )


def test_material_partition_and_compare_refuse_crossed_coordinates(
    exact_casting_material,
):
    books, corpus_reference, book_references, operator, today, *_ = (
        exact_casting_material
    )
    references = (operator, *book_references)
    invocations = compiled_reference_invocations(
        references,
        boundary_identity="adversarial-casting-invocation",
    )

    with pytest.raises(ValueError, match="differs from its exact source boundary"):
        exact_material_partition_references(
            corpus_reference,
            (*tuple(map(len, books[:-1])), len(books[-1]) - 1),
        )
    with pytest.raises(ValueError, match="differs from its exact source"):
        replace(book_references[0], exact_material=b"not its exact material")
    with pytest.raises(ValueError, match="absent from its invocation boundary"):
        compare_compiled_reference_invocations(
            invocations,
            ((operator, today),),
            boundary_identity="absent-casting-compare",
        )
    with pytest.raises(ValueError, match="entered Compare twice"):
        compare_compiled_reference_invocations(
            invocations,
            ((operator, book_references[0]), (operator, book_references[0])),
            boundary_identity="duplicate-casting-compare",
        )
    with pytest.raises(ValueError, match="cannot compare with itself"):
        compare_compiled_reference_invocations(
            invocations,
            ((operator, operator),),
            boundary_identity="self-casting-compare",
        )
