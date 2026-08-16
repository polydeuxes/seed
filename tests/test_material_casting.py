from __future__ import annotations

from dataclasses import replace
from pathlib import Path
import sys

import pytest

from seed_runtime.events import EventLedger
from seed_runtime.byte_measurement import (
    record_byte_measurement_responsible_act_evidence,
    record_byte_measurement_result,
    record_byte_position_pair_count_layer,
)
from seed_runtime.material_ingest import ingest_material
from seed_runtime.operator_checkpoint import (
    record_standing_boundary_reference_responsibility_assignment,
    record_standing_boundary_reference_responsible_act_evidence,
    record_standing_boundary_reference_result,
)
from seed_runtime.operator_command import AddressedOperatorCommand, OperatorCommandFrame
from seed_runtime.operator_locality_standing import (
    advance_operator_locality_standing,
    read_carried_recorded_standing,
    read_operator_locality_standing,
)
from seed_runtime.operator_representation import record_operator_representation


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
from material_pair_investigation import (  # noqa: E402
    compare_pair_occurrences,
    exact_recurrent_material_pair_references,
    exact_pair_occurrences,
    recurrent_adjacent_pair_subjects,
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
                "material-casting-source-locality",
                b"".join(books),
                "sixteen supplied books",
            ),
            (
                "material-casting-source-locality",
                b"what does this exact material distinguish?\n",
                "operator material",
            ),
            (
                "material-casting-source-locality",
                b"one bounded session material\n",
                "today material",
            ),
            (
                "material-casting-source-locality",
                b"one exact earlier lineage material\n",
                "lineage material",
            ),
            (
                "material-casting-unrelated-locality",
                b"available elsewhere is not applicable here\n",
                "unrelated Locality material",
            ),
        )
    )
    (
        corpus_reference,
        operator_reference,
        today_reference,
        lineage_reference,
        unrelated_locality_reference,
    ) = tuple(
        ingest_result_reference(ledger, occurrence.identity) for occurrence in occurrences
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
        unrelated_locality_reference,
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


def _record_checkpoint(ledger, *, locality_identity):
    standing = read_operator_locality_standing(
        ledger, locality_identity=locality_identity
    )
    representation = record_operator_representation(
        ledger,
        locality_identity=locality_identity,
        locality_standing=standing,
    )
    standing = advance_operator_locality_standing(
        ledger,
        representation["recorded_occurrence_references"],
        locality_identity=locality_identity,
        prior=standing,
    )
    command = AddressedOperatorCommand(
        command_identity="material-casting-checkpoint-command",
        locality_identity=locality_identity,
        addressed_at_representation_event_identity=representation[
            "representation_event_identity"
        ],
        frame=OperatorCommandFrame(
            exact_bytes=b"/checkpoint\n", name=b"checkpoint", arguments=b""
        ),
    )
    assignment = record_standing_boundary_reference_responsibility_assignment(
        ledger,
        addressed_command=command,
        locality_standing=standing,
    )
    act = record_standing_boundary_reference_responsible_act_evidence(
        ledger,
        responsibility_assignment_event_identity=assignment.identity,
        responsibility_assignment_standing=read_operator_locality_standing(
            ledger, locality_identity=locality_identity
        ),
    )
    return record_standing_boundary_reference_result(
        ledger, responsible_act_evidence_event_identity=act.identity
    )


def test_operator_material_casts_against_exact_corpus_checkpoint_standing(
    exact_casting_material,
):
    books = exact_casting_material[0]
    locality_identity = "checkpointed-material-casting-locality"
    ledger = EventLedger()
    corpus = ingest_material(
        ledger,
        locality_identity=locality_identity,
        exact_bytes=b"".join(books),
        source_role="fixture material",
        source_boundary="sixteen supplied books",
    )
    checkpoint = _record_checkpoint(
        ledger, locality_identity=locality_identity
    )
    operator = ingest_material(
        ledger,
        locality_identity=locality_identity,
        exact_bytes=b"what does this exact material distinguish?\n",
        source_role="operator material",
        source_boundary="operator material",
    )

    point = read_carried_recorded_standing(
        ledger,
        locality_identity=locality_identity,
        recorded_occurrence_identity=checkpoint.identity,
    )
    assert [
        occurrence["evidence_event_identity"]
        for occurrence in point["standing"]["ingest_occurrences"]
    ] == [corpus.identity]
    corpus_reference = ingest_result_reference(ledger, corpus.identity)
    operator_reference = ingest_result_reference(ledger, operator.identity)
    book_references = exact_material_partition_references(
        corpus_reference, tuple(map(len, books))
    )

    casting = _cast_against_books(
        operator_reference,
        book_references,
        boundary_identity="checkpointed-operator",
    )
    comparisons = (*casting[2], *casting[4])

    assert operator.identity not in {
        occurrence["evidence_event_identity"]
        for occurrence in point["standing"]["ingest_occurrences"]
    }
    assert len(comparisons) == 9
    assert all(len(row) == 16 for row in comparisons)
    assert all(
        not hasattr(comparison, "applicability")
        and not hasattr(comparison, "admitted_material")
        for row in comparisons
        for comparison in row
    )


def test_recurrent_book_pairs_keep_identity_in_fresh_operator_material():
    paths = tuple(ROOT / "corpus" / name for name, _ in MATERIAL_WINDOWS)
    if any(not path.is_file() for path in paths):
        pytest.skip("supplied fixture material is unavailable")
    books = supplied_book_material(ROOT)
    locality_identity = "checkpointed-pair-casting-locality"
    ledger = EventLedger()
    corpus = ingest_material(
        ledger,
        locality_identity=locality_identity,
        exact_bytes=b"".join(books),
        source_role="fixture material",
        source_boundary="sixteen supplied books",
    )
    measurement_act = record_byte_measurement_responsible_act_evidence(
        ledger,
        source_localities=(locality_identity,),
        recording_locality_identity=locality_identity,
    )
    measurement = record_byte_measurement_result(
        ledger,
        responsible_act_evidence_event_identity=measurement_act.identity,
    )
    pair_measurement = record_byte_position_pair_count_layer(
        ledger,
        source_measurement_event_identity=measurement.identity,
        recording_locality_identity=locality_identity,
    )
    checkpoint = _record_checkpoint(ledger, locality_identity=locality_identity)
    operator = ingest_material(
        ledger,
        locality_identity=locality_identity,
        exact_bytes=b"what does this exact material distinguish?\n",
        source_role="operator material",
        source_boundary="operator material",
    )

    point = read_carried_recorded_standing(
        ledger,
        locality_identity=locality_identity,
        recorded_occurrence_identity=checkpoint.identity,
    )
    assert [
        occurrence["evidence_event_identity"]
        for occurrence in point["standing"]["ingest_occurrences"]
    ] == [corpus.identity]
    assert measurement.identity in point["standing"]["measurement_occurrences"]
    assert pair_measurement.identity in point["standing"]["measurement_occurrences"]
    assert operator.identity not in {
        occurrence["evidence_event_identity"]
        for occurrence in point["standing"]["ingest_occurrences"]
    }

    corpus_reference = ingest_result_reference(ledger, corpus.identity)
    pair_references = exact_recurrent_material_pair_references(
        ledger, pair_measurement.identity
    )
    pair_subjects = recurrent_adjacent_pair_subjects(
        (corpus_reference,), pair_references
    )

    expected_counts: dict[bytes, int] = {}
    corpus_material = b"".join(books)
    for position in range(len(corpus_material) - 1):
        material = corpus_material[position : position + 2]
        expected_counts[material] = expected_counts.get(material, 0) + 1
    expected_materials = {
        material for material, count in expected_counts.items() if count >= 2
    }
    assert {
        subject.pair_reference.exact_material
        for subject in pair_subjects
    } == expected_materials

    operator_reference = ingest_result_reference(ledger, operator.identity)
    surviving = []
    comparisons = []
    for subject_position, subject in enumerate(pair_subjects):
        occurrences = exact_pair_occurrences(subject, operator_reference)
        if not occurrences:
            continue
        surviving.append((subject, occurrences))
        comparisons.extend(
            compare_pair_occurrences(
                subject,
                occurrences,
                boundary_identity=(
                    f"checkpointed-operator-pair-{subject_position}"
                ),
            )
        )

    assert surviving
    assert comparisons
    assert any(
        {occurrence.direction for occurrence in occurrences}
        == {"before", "after"}
        for _subject, occurrences in surviving
    )
    assert any(comparison.distinction for comparison in comparisons)
    assert any(not comparison.distinction for comparison in comparisons)
    assert all(
        comparison.premise_occurrence.pair_identity
        == comparison.current_occurrence.pair_identity
        for comparison in comparisons
    )
    assert all(
        not hasattr(comparison, coordinate)
        for comparison in comparisons
        for coordinate in (
            "candidate",
            "admitted_material",
            "admission",
            "applicability",
            "meaning",
            "reference",
            "standing",
            "yield_evidence_identity",
        )
    )


def test_operator_today_and_lineage_material_are_discriminated_in_separate_castings(
    exact_casting_material,
):
    _, _, books, operator, today, lineage, _ = exact_casting_material
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
    books, corpus_reference, book_references, operator, today, _, unrelated = (
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
    crossed_invocations = compiled_reference_invocations(
        (operator, unrelated),
        boundary_identity="crossed-locality-casting-invocation",
    )
    with pytest.raises(ValueError, match="crossed Localities"):
        compare_compiled_reference_invocations(
            crossed_invocations,
            ((operator, unrelated),),
            boundary_identity="crossed-locality-casting-compare",
        )
    crossed_material_invocations = reference_occurrences_across(
        (operator, unrelated),
        boundary_identity="crossed-locality-material-invocation",
        implementation_functions=(MATERIAL_IMPLEMENTATION_FUNCTIONS[0],),
        max_workers=2,
        time_limit_second_count=5.0,
        material_byte_count_limit=4096,
    )
    with pytest.raises(ValueError, match="crossed Localities"):
        compare_material_reference_invocations(
            crossed_material_invocations,
            ((operator, unrelated),),
            boundary_identity="crossed-locality-material-compare",
        )
