from __future__ import annotations

from dataclasses import replace
import json
from pathlib import Path
import re
import sys

import pytest

from seed_runtime.events import EventLedger
from seed_runtime.material_ingest import MATERIAL_INGEST_OCCURRED_KIND, ingest_material
from seed_runtime.byte_measurement import (
    record_byte_measurement_responsible_act_evidence,
    record_byte_measurement_result,
    record_byte_position_pair_count_layer,
)


def _record_byte_measurement(
    ledger, *, source_localities, recording_locality_identity
):
    act_evidence = record_byte_measurement_responsible_act_evidence(
        ledger,
        source_localities=source_localities,
        recording_locality_identity=recording_locality_identity,
    )
    return record_byte_measurement_result(
        ledger,
        responsible_act_evidence_event_identity=act_evidence.identity,
    )


def _complete_admitted_pair_occurrence_counts(
    source_admission_result_reference,
    added_admission_result_reference,
):
    return tuple(
        (
            source_admitted_position,
            added_admitted_position,
            sum(
                (len(source.exact_material) + 1)
                * len(added_admitted_material)
                for source in source_admitted_material
            ),
        )
        for source_admitted_position, source_admitted_material in enumerate(
            source_admission_result_reference.admitted_material
        )
        for added_admitted_position, added_admitted_material in enumerate(
            added_admission_result_reference.admitted_material
        )
        if {
            source.locality_identity for source in source_admitted_material
        }
        == {added.locality_identity for added in added_admitted_material}
    )


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from compiled_format_invocation import (  # noqa: E402
    COMPILED_IMPLEMENTATION_FUNCTIONS,
    added_position_admission_occurrence,
    added_position_invocations,
    admission_result_added_position_occurrences,
    admit_compiled_invocation_rows,
    compare_added_position_invocations,
    compiled_reference_invocations,
    exact_byte_material_references,
    exact_byte_pair_material_references,
    exact_position_material_references,
    first_recurring_added_compare_across,
    recurring_added_compares_across,
    recurring_position_materials,
    moved_exact_byte_material_references,
)
from compiled_material_invocation import ingest_result_reference  # noqa: E402
from material_admission import compare_admission_result_pairs  # noqa: E402
from tests.test_book_admission import (  # noqa: E402
    book_admission,
    scan_active_line,
)


THIS_BOOK_MATERIAL_ACQUISITION_WITNESS = (
    "this_book_material_acquisition_witness"
)
FIDELITY_SUBJECT = THIS_BOOK_MATERIAL_ACQUISITION_WITNESS


def test_book_material_acquisition_witness_has_one_admitted_subject():
    grammar = json.loads(
        (ROOT / "book_of_seed" / "grammar.json").read_text(encoding="utf-8")
    )
    subject_words = set(
        re.findall(
            r"[A-Za-z]+",
            scan_active_line(THIS_BOOK_MATERIAL_ACQUISITION_WITNESS).lower(),
        )
    )

    fidelity = grammar["clauses"]["01.Source.C"]

    assert fidelity["test_subject_relation"] == {
        "first_subject": "test_subject",
        "relation": "witness_for",
        "second_subject": "this_Fidelity",
        "first_subject_distinct_from": "this_Witness",
    }
    assert {
        coordinates["subject"]: coordinates
        for coordinates in fidelity["test_subjects"]
    }[THIS_BOOK_MATERIAL_ACQUISITION_WITNESS] == {
        "subject": THIS_BOOK_MATERIAL_ACQUISITION_WITNESS,
        "material_reference": "this_Book",
    }
    assert subject_words <= book_admission()


@pytest.fixture(scope="module")
def acquired_book_material():
    ledger = EventLedger()
    paths = tuple(
        path
        for path in (ROOT / "book_of_seed").rglob("*")
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


@pytest.fixture(scope="module")
def acquired_book_relations(acquired_book_material):
    ledger, _, ingests, _, _, _, book_admission = acquired_book_material
    byte_measurement = _record_byte_measurement(
        ledger,
        source_localities=("book-material-acquisition",),
        recording_locality_identity="book-material-byte-measurement",
    )
    pair_measurement = record_byte_position_pair_count_layer(
        ledger,
        source_measurement_event_identity=byte_measurement.identity,
        recording_locality_identity="book-material-pair-measurement",
    )
    pair_references = exact_byte_pair_material_references(
        ledger, pair_measurement.identity
    )
    byte_references = moved_exact_byte_material_references(
        ledger,
        byte_measurement.identity,
        destination_locality="book-material-pair-measurement",
    )
    pair_invocation_rows = compiled_reference_invocations(
        pair_references,
        boundary_identity="book-pair-acquisition-invocation",
        implementation_functions=COMPILED_IMPLEMENTATION_FUNCTIONS,
    )
    byte_invocation_rows = compiled_reference_invocations(
        byte_references,
        boundary_identity="book-byte-acquisition-invocation",
        implementation_functions=COMPILED_IMPLEMENTATION_FUNCTIONS,
    )
    pair_admission = admit_compiled_invocation_rows(
        pair_invocation_rows,
        boundary_identity="book-pair-acquisition-admission",
    )
    byte_admission = admit_compiled_invocation_rows(
        byte_invocation_rows,
        boundary_identity="book-byte-acquisition-admission",
    )
    additions = admission_result_added_position_occurrences(
        pair_admission.result_reference,
        byte_admission.result_reference,
        boundary_identity="book-acquired-addition",
        admitted_material_act_occurrence_count_limit=4096,
    )
    earlier_comparisons, prospective_coordinates, later_comparisons = (
        first_recurring_added_compare_across(
            additions,
            pair_invocation_rows,
            boundary_identity="book-acquired-addition-prospective",
            act_occurrence_count_limit=len(additions),
        )
    )
    result_invocation_rows = added_position_invocations(
        additions,
        boundary_identity="book-acquired-addition-invocation",
        implementation_functions=COMPILED_IMPLEMENTATION_FUNCTIONS,
    )
    comparisons = compare_added_position_invocations(
        pair_invocation_rows,
        result_invocation_rows,
        boundary_identity="book-acquired-addition-compare",
    )
    addition_admission = added_position_admission_occurrence(
        additions,
        comparisons,
        boundary_identity="book-acquired-addition-admission",
    )
    return (
        ingests,
        book_admission,
        byte_measurement,
        pair_measurement,
        pair_references,
        byte_references,
        pair_invocation_rows,
        byte_invocation_rows,
        pair_admission,
        byte_admission,
        additions,
        earlier_comparisons,
        prospective_coordinates,
        later_comparisons,
        result_invocation_rows,
        comparisons,
        addition_admission,
    )


@pytest.fixture(scope="module")
def complete_book_admission_acts(acquired_book_material):
    ledger, _, _, _, _, book_invocation_rows, book_admission = acquired_book_material
    byte_measurement = _record_byte_measurement(
        ledger,
        source_localities=("book-material-acquisition",),
        recording_locality_identity="book-material-acquisition",
    )
    byte_references = exact_byte_material_references(
        ledger, byte_measurement.identity
    )
    byte_invocation_rows = compiled_reference_invocations(
        byte_references,
        boundary_identity="complete-book-byte-invocation",
        implementation_functions=COMPILED_IMPLEMENTATION_FUNCTIONS,
    )
    byte_admission = admit_compiled_invocation_rows(
        byte_invocation_rows,
        boundary_identity="complete-book-byte-admission",
    )
    act_occurrence_count_limit = min(
        count
        for _, _, count in _complete_admitted_pair_occurrence_counts(
            book_admission.result_reference,
            byte_admission.result_reference,
        )
    )
    additions = admission_result_added_position_occurrences(
        book_admission.result_reference,
        byte_admission.result_reference,
        boundary_identity="complete-book-admission-addition",
        admitted_material_act_occurrence_count_limit=act_occurrence_count_limit,
    )
    earlier_comparisons, prospective_coordinates, later_comparisons = (
        first_recurring_added_compare_across(
            additions,
            book_invocation_rows,
            boundary_identity="complete-book-admission-addition-prospective",
            act_occurrence_count_limit=len(additions),
        )
    )
    result_invocation_rows = added_position_invocations(
        additions,
        boundary_identity="complete-book-admission-addition-invocation",
        implementation_functions=COMPILED_IMPLEMENTATION_FUNCTIONS,
    )
    comparisons = compare_added_position_invocations(
        book_invocation_rows,
        result_invocation_rows,
        boundary_identity="complete-book-admission-addition-compare",
    )
    return (
        book_admission,
        book_invocation_rows,
        byte_measurement,
        byte_references,
        byte_invocation_rows,
        byte_admission,
        additions,
        result_invocation_rows,
        comparisons,
        earlier_comparisons,
        prospective_coordinates,
        later_comparisons,
    )


@pytest.fixture(scope="module")
def later_book_material_acquisition(acquired_book_material):
    ledger, paths, _, earlier_boundary, earlier_references, _, earlier_admission = (
        acquired_book_material
    )
    later_ingests = tuple(
        ingest_material(
            ledger,
            locality_identity="book-material-acquisition-later",
            exact_bytes=path.read_bytes(),
            source_role="fixture material",
            source_boundary=str(path.relative_to(ROOT)),
        )
        for path in paths
    )
    later_boundary = ledger.append_boundary()
    later_references = tuple(
        ingest_result_reference(ledger, occurrence.identity)
        for occurrence in later_ingests
    )
    later_invocation_rows = compiled_reference_invocations(
        later_references,
        boundary_identity="book-material-acquisition-later-invocation",
        implementation_functions=COMPILED_IMPLEMENTATION_FUNCTIONS,
    )
    later_admission = admit_compiled_invocation_rows(
        later_invocation_rows,
        boundary_identity="book-material-acquisition-later-admission",
    )
    return (
        ledger,
        paths,
        earlier_boundary,
        earlier_references,
        earlier_admission,
        later_ingests,
        later_boundary,
        later_references,
        later_invocation_rows,
        later_admission,
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
        for path in (ROOT / "book_of_seed").rglob("*")
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


def test_book_measurements_retain_every_exact_file_occurrence(
    acquired_book_relations,
):
    ingests, _, byte_measurement, pair_measurement, *_ = acquired_book_relations
    source_references = byte_measurement.material[
        "responsibility_assignment_evidence"
    ]["source_occurrence_references"]

    assert tuple(
        reference["ingest_occurrence_identity"] for reference in source_references
    ) == tuple(occurrence.identity for occurrence in ingests)
    assert byte_measurement.material["source_localities"] == [
        "book-material-acquisition"
    ]
    assert pair_measurement.material["source_assertion_reference"] == {
        "recorded_occurrence_identity": byte_measurement.identity,
        "assertion_identity": byte_measurement.material["assertions"][0][
            "dimensions"
        ]["identity"],
    }


def test_complete_book_admission_reaches_recurring_addition_relations(
    acquired_book_relations,
):
    (
        _,
        book_admission,
        _,
        _,
        pair_references,
        byte_references,
        pair_invocation_rows,
        byte_invocation_rows,
        pair_admission,
        byte_admission,
        additions,
        _,
        _,
        _,
        result_invocation_rows,
        comparisons,
        addition_admission,
    ) = acquired_book_relations

    assert book_admission.source_material
    assert pair_admission.source_material == pair_references
    assert byte_admission.source_material == byte_references
    assert len(pair_invocation_rows) == len(byte_invocation_rows) == len(
        COMPILED_IMPLEMENTATION_FUNCTIONS
    )
    assert additions
    assert all(len(row) == len(additions) for row in result_invocation_rows)
    assert all(len(row) == len(additions) for row in comparisons)
    assert addition_admission.source_material == additions
    assert any(
        len(same_coordinates) > 1
        for same_coordinates in addition_admission.admitted_material
    )
    assert {
        occurrence
        for same_coordinates in addition_admission.admitted_material
        for occurrence in same_coordinates
    } == set(additions)


def test_book_relations_freeze_one_distinct_function_vector_before_later_invocation(
    acquired_book_relations,
):
    (
        _,
        _,
        _,
        _,
        _,
        _,
        _,
        _,
        _,
        _,
        _,
        earlier_comparisons,
        prospective_coordinates,
        later_comparisons,
        _,
        _,
        _,
    ) = acquired_book_relations

    assert prospective_coordinates is not None
    assert later_comparisons is not None
    assert len(prospective_coordinates) == len(COMPILED_IMPLEMENTATION_FUNCTIONS)
    assert any(coordinate is None for coordinate in prospective_coordinates)
    assert any(coordinate is not None for coordinate in prospective_coordinates)
    assert all(
        coordinate is None or comparison.result_returned == coordinate
        for coordinate, comparison in zip(
            prospective_coordinates, later_comparisons
        )
    )
    later_act = later_comparisons[0].added_position_act_occurrence_identity
    assert all(
        comparison.added_position_act_occurrence_identity != later_act
        for row in earlier_comparisons
        for comparison in row
    )
    assert len(
        {
            comparison.implementation_function_identity
            for comparison in later_comparisons
        }
    ) == len(COMPILED_IMPLEMENTATION_FUNCTIONS)


def test_complete_book_admission_drives_later_exact_material_acts(
    complete_book_admission_acts,
):
    (
        book_admission,
        _,
        _,
        _,
        _,
        byte_admission,
        additions,
        result_invocation_rows,
        comparisons,
        _,
        _,
        _,
    ) = complete_book_admission_acts

    assert additions
    assert all(
        addition.source_admission_result_reference == book_admission.result_reference
        and addition.added_admission_result_reference
        == byte_admission.result_reference
        for addition in additions
    )
    assert all(
        addition.source_reference
        in book_admission.admitted_material[
            addition.source_admitted_material_position
        ]
        and addition.added_reference
        in byte_admission.admitted_material[
            addition.added_admitted_material_position
        ]
        for addition in additions
    )
    complete_pair_occurrence_counts = _complete_admitted_pair_occurrence_counts(
        book_admission.result_reference,
        byte_admission.result_reference,
    )
    least_complete_pair_occurrence_count = min(
        count for _, _, count in complete_pair_occurrence_counts
    )
    assert len(additions) == least_complete_pair_occurrence_count
    assert {
        (
            addition.source_admitted_material_position,
            addition.added_admitted_material_position,
        )
        for addition in additions
    } == {
        (source_position, added_position)
        for source_position, added_position, count in (
            complete_pair_occurrence_counts
        )
        if count == least_complete_pair_occurrence_count
    }
    assert admission_result_added_position_occurrences(
        book_admission.result_reference,
        byte_admission.result_reference,
        boundary_identity="incomplete-book-admission-addition",
        admitted_material_act_occurrence_count_limit=(
            least_complete_pair_occurrence_count - 1
        ),
    ) == ()
    assert all(len(row) == len(additions) for row in result_invocation_rows)
    assert all(len(row) == len(additions) for row in comparisons)
    assert any(
        comparison.distinction
        for row in comparisons
        for comparison in row
    )


def test_complete_book_later_acts_refuse_broken_admission_lineage(
    complete_book_admission_acts,
):
    book_admission, _, _, _, _, byte_admission, additions, _, _, _, _, _ = (
        complete_book_admission_acts
    )
    addition = additions[0]

    with pytest.raises(ValueError, match="differs from its Admissions"):
        replace(
            addition,
            source_admission_result_reference=byte_admission.result_reference,
        )
    with pytest.raises(ValueError, match="differs from its Admissions"):
        replace(
            addition,
            added_admission_result_reference=book_admission.result_reference,
        )


def test_complete_book_compare_refuses_a_mismatched_act_result_occurrence(
    complete_book_admission_acts,
):
    (
        _,
        _,
        _,
        _,
        _,
        _,
        additions,
        result_invocation_rows,
        _,
        _,
        _,
        _,
    ) = complete_book_admission_acts
    different = next(
        addition
        for addition in additions[1:]
        if addition.result_material != additions[0].result_material
    )
    with pytest.raises(ValueError, match="differs from its exact source"):
        replace(
            result_invocation_rows[0][0],
            source_coordinate=different,
        )


def test_complete_book_admission_freezes_one_coordinate_before_later_invocation(
    complete_book_admission_acts,
):
    (
        book_admission,
        _,
        _,
        _,
        _,
        _,
        additions,
        _,
        _,
        earlier_comparisons,
        prospective_coordinates,
        later_comparisons,
    ) = complete_book_admission_acts

    assert prospective_coordinates is not None
    assert later_comparisons is not None
    assert any(coordinate is not None for coordinate in prospective_coordinates)
    compared_coordinates = tuple(
        (coordinate, comparison.result_returned)
        for coordinate, comparison in zip(
            prospective_coordinates, later_comparisons
        )
        if coordinate is not None
    )
    assert compared_coordinates
    assert any(
        coordinate != returned
        for coordinate, returned in compared_coordinates
    )
    later_act = later_comparisons[0].added_position_act_occurrence_identity
    assert all(
        comparison.added_position_act_occurrence_identity != later_act
        for row in earlier_comparisons
        for comparison in row
    )
    later_addition = next(
        addition
        for addition in additions
        if addition.act_occurrence_identity == later_act
    )
    assert (
        later_addition.source_admission_result_reference
        == book_admission.result_reference
    )


def test_complete_book_recurrence_continues_after_one_prospective_conflict(
    complete_book_admission_acts,
):
    (
        _,
        book_invocation_rows,
        _,
        _,
        _,
        _,
        additions,
        _,
        _,
        _,
        _,
        _,
    ) = complete_book_admission_acts

    comparisons, recurring = recurring_added_compares_across(
        additions,
        book_invocation_rows,
        boundary_identity="complete-book-recurrence-after-conflict",
        act_occurrence_count_limit=10,
    )

    assert len(recurring) > 1
    occurrence_positions = tuple(
        later[0].occurrence_position for _, later in recurring
    )
    assert occurrence_positions == tuple(sorted(occurrence_positions))
    first_coordinates, first_later = recurring[0]
    assert any(
        coordinate is not None and coordinate != comparison.result_returned
        for coordinate, comparison in zip(first_coordinates, first_later)
    )
    assert all(
        row[occurrence_positions[0]] == comparison
        for row, comparison in zip(comparisons, first_later)
    )
    assert occurrence_positions[1] > occurrence_positions[0]


def test_book_and_supplied_material_have_later_position_recurrence(
    acquired_book_material,
):
    ledger, _, _, _, book_references, _, _ = acquired_book_material
    supplied_path = ROOT / "corpus" / "english_grimm_fairy_tales.txt"
    if not supplied_path.is_file():
        pytest.skip("supplied fixture material is unavailable")
    supplied_material = b"".join(
        supplied_path.read_bytes().splitlines(keepends=True)[:300]
    )
    supplied_ingest = ingest_material(
        ledger,
        locality_identity="supplied-position-material",
        exact_bytes=supplied_material,
        source_role="fixture material",
        source_boundary="corpus/english_grimm_fairy_tales.txt:first-300-lines",
    )
    supplied_reference = ingest_result_reference(ledger, supplied_ingest.identity)

    book_recurring = tuple(
        found
        for reference in book_references
        for found in recurring_position_materials(
            exact_position_material_references(reference),
            material_count=24,
        )
    )
    supplied_recurring = recurring_position_materials(
        exact_position_material_references(supplied_reference),
        material_count=24,
    )

    for recurring in (book_recurring, supplied_recurring):
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


def test_earlier_and_later_book_admissions_keep_distinct_occurrence_sets(
    later_book_material_acquisition,
):
    (
        ledger,
        paths,
        earlier_boundary,
        earlier_references,
        earlier_admission,
        later_ingests,
        later_boundary,
        later_references,
        later_invocation_rows,
        later_admission,
    ) = later_book_material_acquisition

    assert tuple(reference.exact_material for reference in earlier_references) == tuple(
        reference.exact_material for reference in later_references
    ) == tuple(path.read_bytes() for path in paths)
    assert all(
        earlier.recorded_occurrence_identity != later.recorded_occurrence_identity
        and earlier.act_occurrence_identity != later.act_occurrence_identity
        and earlier.result_identity != later.result_identity
        for earlier, later in zip(earlier_references, later_references)
    )
    assert all(
        reference.locality_identity == "book-material-acquisition-later"
        for reference in later_references
    )
    assert tuple(
        occurrence
        for occurrence in ledger.list_locality(
            "book-material-acquisition-later", through=later_boundary
        )
        if occurrence.kind == MATERIAL_INGEST_OCCURRED_KIND
    ) == later_ingests
    assert all(
        occurrence not in ledger.list(through=earlier_boundary)
        for occurrence in later_ingests
    )
    assert tuple(
        tuple(occurrence.returned for occurrence in row)
        for row in later_invocation_rows
    ) == tuple(
        tuple(
            reference.invocation_occurrence.returned
            for reference in earlier_admission.invocation_result_references
            if reference.invocation_occurrence.implementation_function_identity
            == row[0].implementation_function_identity
        )
        for row in later_invocation_rows
    )
    assert earlier_admission.source_material == earlier_references
    assert later_admission.source_material == later_references
    with pytest.raises(ValueError, match="same exact material occurrences"):
        compare_admission_result_pairs(
            (earlier_admission.result_reference, later_admission.result_reference),
            boundary_identity="book-material-acquisition-through-time-compare",
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
