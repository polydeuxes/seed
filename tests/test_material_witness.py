from __future__ import annotations

from dataclasses import replace
from pathlib import Path
import shutil
import subprocess
import sys

import pytest

from seed_runtime.byte_measurement import (
    assertions_of_recorded_byte_position_pair_measurement,
    assertions_of_recorded_byte_measurement,
    record_byte_position_pair_count_layer,
    record_byte_count_layer,
)
from seed_runtime.events import EventLedger
from seed_runtime.material_ingest import ingest_material


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from compiled_format_invocation import (  # noqa: E402
    AddedPositionOccurrence,
    AddedPositionAdmissionOccurrence,
    COMPILED_IMPLEMENTATION_FUNCTIONS,
    CompiledImplementationFunction,
    ExactMaterialReference,
    admit_added_position_occurrences,
    added_position_admission_occurrence,
    added_position_admission_occurrences,
    admission_added_position_occurrences,
    added_position_occurrences,
    compare_added_position_invocations,
    compare_added_position_pairs,
    compare_removed_position_invocations,
    compiled_invocation,
    compiled_invocations,
    compiled_reference_invocations,
    added_position_invocations,
    removed_position_invocations,
    removed_position_occurrences,
    exact_byte_material_references,
    exact_byte_pair_material_references,
    preserves_original_order,
)
from compiled_material_invocation import (  # noqa: E402
    MATERIAL_IMPLEMENTATION_FUNCTIONS,
    MaterialImplementationFunction,
    MaterialAddedReturnCompareOccurrence,
    admit_invocation_occurrences,
    occurrences_across,
    invocation_occurrence,
    first_recurring_added_return_compare,
    recurring_added_result_coordinates,
    reference_occurrences_across,
)
from material_admission import (  # noqa: E402
    admission_occurrence,
    compare_admission_result_pairs,
    preserves,
)


def _implementation_functions_available():
    return all(
        shutil.which(implementation_function.invocation[0]) is not None
        for implementation_function in MATERIAL_IMPLEMENTATION_FUNCTIONS
    )


def _book_paths() -> tuple[Path, ...]:
    return tuple(
        path
        for path in sorted((ROOT / "book_of_seed").rglob("*"))
        if path.is_file()
    )


@pytest.fixture(scope="module")
def measured_book_pairs():
    ledger = EventLedger()
    paths = _book_paths()
    ingests = tuple(
        ingest_material(
            ledger,
            locality_identity="book-material",
            exact_bytes=path.read_bytes(),
            source_role="fixture material",
            source_boundary=str(path.relative_to(ROOT)),
        )
        for path in paths
    )
    byte_measurement = record_byte_count_layer(
        ledger,
        source_locality_identities=("book-material",),
        recording_locality_identity="book-material-measurement",
    )
    pair_measurement = record_byte_position_pair_count_layer(
        ledger,
        source_measurement_event_identity=byte_measurement.identity,
        recording_locality_identity="book-material-measurement",
    )
    assertions = assertions_of_recorded_byte_position_pair_measurement(
        ledger, pair_measurement.identity
    )
    byte_assertions = assertions_of_recorded_byte_measurement(
        ledger, byte_measurement.identity
    )
    pairs = tuple(
        sorted(
            bytes(assertion.representation)
            for assertion in assertions or ()
            if assertion.result == "count" and assertion.representation is not None
        )
    )
    byte_values = tuple(
        sorted(
            assertion.representation
            for assertion in byte_assertions or ()
            if assertion.result == "count" and assertion.representation is not None
        )
    )
    pair_material = exact_byte_pair_material_references(
        ledger, pair_measurement.identity
    )
    byte_material = exact_byte_material_references(
        ledger, byte_measurement.identity
    )
    return (
        paths,
        ingests,
        assertions,
        pairs,
        byte_assertions,
        byte_values,
        pair_material,
        byte_material,
    )


@pytest.fixture(scope="module")
def book_pair_invocation_occurrences(measured_book_pairs):
    return occurrences_across(
        measured_book_pairs[3], boundary_identity="book-pair-material"
    )


@pytest.fixture(scope="module")
def book_pair_compiled_material_occurrences(measured_book_pairs):
    invocation = ("/usr/bin/env", "-i", "/bin/bash", "--noprofile", "--norc", "-n")
    if any(not Path(part).is_file() for part in (invocation[0], invocation[2])):
        pytest.skip("compiled implementation function is unavailable")
    function = MaterialImplementationFunction(
        identity="compiled-0",
        invocation=invocation,
    )
    occurrences = reference_occurrences_across(
        measured_book_pairs[6],
        boundary_identity="book-pair-compiled-material-invocation",
        implementation_functions=(function,),
    )[0]
    return function, occurrences


@pytest.fixture(scope="module")
def book_pair_format_occurrences(measured_book_pairs):
    return compiled_reference_invocations(
        measured_book_pairs[6], boundary_identity="book-pair-format"
    )


@pytest.fixture(scope="module")
def book_byte_format_comparisons(measured_book_pairs):
    material = measured_book_pairs[5]
    pairs = tuple(bytes((first, second)) for first in material for second in material)
    pair_occurrences = compiled_invocations(
        pairs, boundary_identity="book-byte-format"
    )
    found = []
    for implementation_function, pair_row in zip(COMPILED_IMPLEMENTATION_FUNCTIONS, pair_occurrences):
        pair_returned = {
            tuple(occurrence.exact_material): occurrence.returned
            for occurrence in pair_row
        }
        comparisons = {
            (first, second): (
                tuple(
                    (pair_returned[first, other], pair_returned[second, other])
                    for other in material
                ),
                tuple(
                    (pair_returned[other, first], pair_returned[other, second])
                    for other in material
                ),
            )
            for position, first in enumerate(material)
            for second in material[position + 1 :]
        }
        found.append((implementation_function.identity, pair_returned, comparisons))
    return tuple(found)


@pytest.fixture(scope="module")
def book_three_byte_format_occurrences(
    measured_book_pairs, book_byte_format_comparisons
):
    material = measured_book_pairs[5]
    returned_pairs = frozenset(
        bytes(pair)
        for _, pair_returned, _ in book_byte_format_comparisons
        for pair, returned in pair_returned.items()
        if returned
    )
    occurrences = added_position_occurrences(
        tuple(
            reference
            for reference in measured_book_pairs[6]
            if reference.exact_material in returned_pairs
        ),
        measured_book_pairs[7],
        boundary_identity="book-three-byte-addition",
    )
    return returned_pairs, occurrences, added_position_invocations(
        occurrences, boundary_identity="book-three-byte-format"
    )


@pytest.fixture(scope="module")
def book_added_position_comparisons(
    book_pair_format_occurrences, book_three_byte_format_occurrences
):
    return compare_added_position_invocations(
        book_pair_format_occurrences,
        book_three_byte_format_occurrences[2],
        boundary_identity="book-added-position-compare",
    )


@pytest.fixture(scope="module")
def book_added_position_admission(
    book_three_byte_format_occurrences, book_added_position_comparisons
):
    return admit_added_position_occurrences(
        book_three_byte_format_occurrences[1],
        book_added_position_comparisons,
    )


@pytest.fixture(scope="module")
def book_added_position_admission_occurrences(
    book_three_byte_format_occurrences,
    book_added_position_comparisons,
    book_added_position_admission,
):
    return added_position_admission_occurrences(
        book_three_byte_format_occurrences[1],
        book_added_position_comparisons,
        boundary_identity="book-added-position-admission",
    )


@pytest.fixture(scope="module")
def book_added_position_admission_comparisons(
    book_added_position_admission_occurrences,
):
    references = tuple(
        occurrence.result_reference
        for occurrence in book_added_position_admission_occurrences
    )
    return compare_admission_result_pairs(
        references,
        boundary_identity="book-added-position-admission-compare",
    )


@pytest.fixture(scope="module")
def book_added_position_pair_comparisons(
    book_three_byte_format_occurrences, book_added_position_comparisons
):
    return compare_added_position_pairs(
        book_three_byte_format_occurrences[1],
        book_added_position_comparisons,
        boundary_identity="book-added-position-pair-compare",
    )


@pytest.fixture(scope="module")
def book_removed_position_invocation_occurrences(measured_book_pairs):
    occurrences = removed_position_occurrences(
        measured_book_pairs[6],
        measured_book_pairs[7],
        boundary_identity="book-pair-removal",
    )
    invocations = removed_position_invocations(
        occurrences, boundary_identity="book-removed-position-format"
    )
    return occurrences, invocations


@pytest.fixture(scope="module")
def book_removed_position_comparisons(
    book_pair_format_occurrences, book_removed_position_invocation_occurrences
):
    return compare_removed_position_invocations(
        book_pair_format_occurrences,
        book_removed_position_invocation_occurrences[1],
        boundary_identity="book-removed-position-compare",
    )


@pytest.fixture(scope="module")
def book_removal_result_additions(
    measured_book_pairs,
    book_removed_position_invocation_occurrences,
    book_removed_position_comparisons,
):
    admitted_removal_identities = {
        comparison.removed_position_act_occurrence_identity
        for row in book_removed_position_comparisons
        for comparison in row
        if comparison.distinction
    }
    admitted_removals = tuple(
        removal
        for removal in book_removed_position_invocation_occurrences[0]
        if removal.act_occurrence_identity in admitted_removal_identities
    )
    source_references = tuple(
        removal.result_reference for removal in admitted_removals
    )
    source_invocations = compiled_reference_invocations(
        source_references,
        boundary_identity="book-removal-result-format",
    )
    additions = added_position_occurrences(
        source_references,
        measured_book_pairs[7],
        boundary_identity="book-removal-result-addition",
    )
    result_invocations = added_position_invocations(
        additions,
        boundary_identity="book-removal-result-addition-format",
    )
    comparisons = compare_added_position_invocations(
        source_invocations,
        result_invocations,
        boundary_identity="book-removal-result-addition-compare",
    )
    return (
        admitted_removal_identities,
        admitted_removals,
        source_references,
        additions,
        comparisons,
    )


def _admission(occurrences, coordinate=lambda occurrence: occurrence.coordinates):
    same_result = {}
    for occurrence in occurrences:
        same_result.setdefault(coordinate(occurrence), set()).add(
            occurrence.exact_material
        )
    return frozenset(frozenset(material) for material in same_result.values())


def _admission_counts(admission):
    return (
        len(admission),
        sum(len(material) == 1 for material in admission),
        max(map(len, admission)),
    )


def _one_byte_apart(first: bytes, second: bytes) -> bool:
    return len(first) == len(second) and sum(
        left != right for left, right in zip(first, second)
    ) == 1


def _return_boundaries(occurrences):
    same_result = {}
    for occurrence in occurrences:
        material = occurrence.exact_material
        for position in range(len(material)):
            same_result.setdefault(
                (len(material), position, material[:position], material[position + 1 :]),
                [],
            ).append(occurrence)
    return tuple(
        (first.exact_material, second.exact_material)
        for material_at_coordinate in same_result.values()
        for position, first in enumerate(material_at_coordinate)
        for second in material_at_coordinate[position + 1 :]
        if first.returned != second.returned
    )


IMPLEMENTATION_FUNCTIONS_AVAILABLE = _implementation_functions_available()


def test_every_current_book_material_has_its_own_ingest(measured_book_pairs):
    paths, ingests, *_ = measured_book_pairs

    assert len(paths) == len(ingests)
    assert len({ingest.identity for ingest in ingests}) == len(paths)
    assert tuple(ingest.exact_material for ingest in ingests) == tuple(
        path.read_bytes() for path in paths
    )


def test_pair_material_comes_from_the_complete_recorded_measurement(measured_book_pairs):
    _, _, assertions, pairs, _, _, pair_material, _ = measured_book_pairs
    recorded = tuple(
        sorted(
            bytes(assertion.representation)
            for assertion in assertions or ()
            if assertion.result == "count" and assertion.representation is not None
        )
    )

    assert pairs
    assert pairs == recorded
    assert len(pairs) == len(set(pairs))
    assert all(len(pair) == 2 for pair in pairs)
    assert tuple(reference.exact_material for reference in pair_material) == pairs
    assert {reference.locality_identity for reference in pair_material} == {
        "book-material-measurement"
    }


def test_byte_material_comes_from_the_complete_recorded_measurement(measured_book_pairs):
    _, _, _, _, assertions, material, _, byte_material = measured_book_pairs
    recorded = tuple(
        sorted(
            assertion.representation
            for assertion in assertions or ()
            if assertion.result == "count" and assertion.representation is not None
        )
    )

    assert material
    assert material == recorded
    assert len(material) == len(set(material))
    assert tuple(reference.exact_material for reference in byte_material) == tuple(
        bytes((value,)) for value in material
    )
    assert {reference.locality_identity for reference in byte_material} == {
        "book-material-measurement"
    }


@pytest.mark.skipif(
    not IMPLEMENTATION_FUNCTIONS_AVAILABLE,
    reason="one material implementation function is absent",
)
def test_every_measured_pair_reaches_every_implementation_function(book_pair_invocation_occurrences, measured_book_pairs):
    pairs = measured_book_pairs[3]

    assert len(book_pair_invocation_occurrences) == len(MATERIAL_IMPLEMENTATION_FUNCTIONS)
    assert tuple(
        row[0].implementation_function_identity for row in book_pair_invocation_occurrences
    ) == tuple(implementation_function.identity for implementation_function in MATERIAL_IMPLEMENTATION_FUNCTIONS)
    assert all(
        tuple(occurrence.exact_material for occurrence in row) == pairs
        for row in book_pair_invocation_occurrences
    )
    assert all(
        len({occurrence.exact_material for occurrence in row}) == len(pairs)
        for row in book_pair_invocation_occurrences
    )


@pytest.mark.skipif(
    not IMPLEMENTATION_FUNCTIONS_AVAILABLE,
    reason="one material implementation function is absent",
)
def test_distinct_implementation_functions_establish_their_admissions(book_pair_invocation_occurrences):
    admissions = tuple(
        _admission(occurrences) for occurrences in book_pair_invocation_occurrences
    )
    comparisons = {
        (first, second): preserves(admissions[first], admissions[second])
        for first in range(len(admissions))
        for second in range(len(admissions))
    }

    assert len(set(admissions)) > 1
    counts = tuple(_admission_counts(admission) for admission in admissions)
    assert all(largest > 1 for _, _, largest in counts)
    assert all(single < admitted for admitted, single, _ in counts)
    assert all(
        preserves(admission, frozenset({frozenset().union(*admission)}))
        for admission in admissions
    )
    assert any(
        comparisons[first, second] != comparisons[second, first]
        for first in range(len(admissions))
        for second in range(first + 1, len(admissions))
    )
    assert any(
        not comparisons[first, second] and not comparisons[second, first]
        for first in range(len(admissions))
        for second in range(first + 1, len(admissions))
    )


def test_measured_book_pairs_reach_one_compiled_material_function(
    book_pair_compiled_material_occurrences,
    measured_book_pairs,
):
    function, occurrences = book_pair_compiled_material_occurrences

    assert function.invocation == (
        "/usr/bin/env",
        "-i",
        "/bin/bash",
        "--noprofile",
        "--norc",
        "-n",
    )
    assert tuple(occurrence.invocation_position for occurrence in occurrences) == tuple(
        range(len(measured_book_pairs[6]))
    )
    assert tuple(occurrence.source_reference for occurrence in occurrences) == (
        measured_book_pairs[6]
    )
    assert all(occurrence.returned for occurrence in occurrences)
    assert len({occurrence.coordinates for occurrence in occurrences}) > 1


def test_compiled_material_function_exposes_one_byte_return_code_boundaries(
    book_pair_compiled_material_occurrences,
):
    _, occurrences = book_pair_compiled_material_occurrences
    same_position = {}
    for occurrence in occurrences:
        material = occurrence.exact_material
        for position in range(len(material)):
            same_position.setdefault(
                (position, material[:position], material[position + 1 :]),
                [],
            ).append(occurrence)
    boundaries = tuple(
        (first.exact_material, second.exact_material)
        for material_at_position in same_position.values()
        for position, first in enumerate(material_at_position)
        for second in material_at_position[position + 1 :]
        if first.returncode != second.returncode
    )

    assert boundaries
    assert all(_one_byte_apart(first, second) for first, second in boundaries)


def test_compiled_material_results_enter_one_exact_admission(
    book_pair_compiled_material_occurrences,
    measured_book_pairs,
):
    _, occurrences = book_pair_compiled_material_occurrences
    admission = admit_invocation_occurrences(
        occurrences,
        boundary_identity="book-pair-compiled-material-admission",
    )

    assert admission.source_material == measured_book_pairs[6]
    assert len(admission.admitted_material) > 1
    assert {
        reference
        for same_coordinates in admission.admitted_material
        for reference in same_coordinates
    } == set(measured_book_pairs[6])


def test_every_measured_pair_reaches_every_compiled_format_implementation_function(
    book_pair_format_occurrences, measured_book_pairs
):
    pairs = measured_book_pairs[3]

    assert len(book_pair_format_occurrences) == len(COMPILED_IMPLEMENTATION_FUNCTIONS)
    assert all(
        tuple(occurrence.exact_material for occurrence in row) == pairs
        for row in book_pair_format_occurrences
    )
    assert all(
        tuple(occurrence.source_coordinate for occurrence in row)
        == measured_book_pairs[6]
        for row in book_pair_format_occurrences
    )


def test_compiled_format_implementation_functions_admit_the_same_material_differently(
    book_pair_format_occurrences,
):
    return_admissions = tuple(
        _admission(occurrences, lambda occurrence: occurrence.returned)
        for occurrences in book_pair_format_occurrences
    )

    assert len(set(return_admissions)) > 1
    assert sum(len(admission) > 1 for admission in return_admissions) > 1
    assert all(
        any(len(material) > 1 for material in admission)
        for admission in return_admissions
    )


def test_one_byte_differences_establish_compiled_invocation_boundaries(
    book_pair_format_occurrences,
):
    boundaries = tuple(
        _return_boundaries(occurrences)
        for occurrences in book_pair_format_occurrences
    )

    assert any(boundaries)
    assert all(
        _one_byte_apart(first, second)
        for invocation_boundaries in boundaries
        for first, second in invocation_boundaries
    )
    assert len({frozenset(invocation_boundaries) for invocation_boundaries in boundaries}) > 1


def test_every_ordered_pair_is_compared_for_each_compiled_function(
    book_byte_format_comparisons, measured_book_pairs
):
    material = measured_book_pairs[5]
    expected_pairs = {(first, second) for first in material for second in material}
    expected_comparisons = len(material) * (len(material) - 1) // 2

    for _, pair_returned, comparisons in book_byte_format_comparisons:
        assert set(pair_returned) == expected_pairs
        assert len(comparisons) == expected_comparisons
        assert all(
            len(outgoing) == len(incoming) == len(material)
            for outgoing, incoming in comparisons.values()
        )


def test_compiled_functions_establish_different_pairwise_distinctions(
    book_byte_format_comparisons,
):
    distinctions = tuple(
        frozenset(
            pair
            for pair, directions in comparisons.items()
            if any(
                first != second
                for direction in directions
                for first, second in direction
            )
        )
        for _, _, comparisons in book_byte_format_comparisons
    )

    assert len(set(distinctions)) > 1
    assert any(not distinction for distinction in distinctions)
    assert any(distinction for distinction in distinctions)


def test_three_byte_results_keep_their_measured_material_references(
    book_three_byte_format_occurrences, measured_book_pairs
):
    returned_pairs, occurrences, _ = book_three_byte_format_occurrences
    material = set(measured_book_pairs[5])
    source_references = {
        (
            reference.recorded_occurrence_identity,
            reference.assertion_identity,
        )
        for reference in measured_book_pairs[6]
    }
    added_references = {
        (
            reference.recorded_occurrence_identity,
            reference.assertion_identity,
        )
        for reference in measured_book_pairs[7]
    }

    assert returned_pairs
    assert occurrences
    assert all(
        occurrence.source_material in returned_pairs
        and occurrence.added_material in {
            bytes((item,)) for item in material
        }
        and len(occurrence.result_material) == 3
        and preserves_original_order(
            source_material=occurrence.source_material,
            result_material=occurrence.result_material,
            added_position=occurrence.position,
        )
        for occurrence in occurrences
    )
    assert all(
        (
            occurrence.source_reference.recorded_occurrence_identity,
            occurrence.source_reference.assertion_identity,
        )
        in source_references
        and (
            occurrence.added_reference.recorded_occurrence_identity,
            occurrence.added_reference.assertion_identity,
        )
        in added_references
        for occurrence in occurrences
    )
    assert len(
        {
            (
                occurrence.source_reference.recorded_occurrence_identity,
                occurrence.source_reference.assertion_identity,
                occurrence.position,
                occurrence.added_reference.recorded_occurrence_identity,
                occurrence.added_reference.assertion_identity,
            )
            for occurrence in occurrences
        }
    ) == len(occurrences)
    assert len({occurrence.act_occurrence_identity for occurrence in occurrences}) == len(
        occurrences
    )
    assert len({occurrence.result_identity for occurrence in occurrences}) == len(
        occurrences
    )


def test_added_position_refuses_a_different_source_order():
    assert preserves_original_order(
        source_material=b"ab",
        result_material=b"axb",
        added_position=1,
    )
    assert not preserves_original_order(
        source_material=b"ab",
        result_material=b"bxa",
        added_position=1,
    )
    assert not preserves_original_order(
        source_material=b"ab",
        result_material=b"axb",
        added_position=0,
    )


def test_equal_result_material_keeps_each_exact_added_position_occurrence():
    source = ExactMaterialReference(
        "source-occurrence", "source-assertion", "fixture-locality", b"aa"
    )
    added = ExactMaterialReference(
        "added-occurrence", "added-assertion", "fixture-locality", b"a"
    )
    added_occurrences = added_position_occurrences(
        (source,), (added,), boundary_identity="equal-material-addition"
    )
    implementation_function = CompiledImplementationFunction(
        identity="fixture", invocation=lambda material: material
    )
    occurrences = added_position_invocations(
        added_occurrences,
        boundary_identity="equal-material-positions",
        implementation_functions=(implementation_function,),
    )[0]

    assert tuple(
        occurrence.result_material for occurrence in added_occurrences
    ) == (b"aaa", b"aaa", b"aaa")
    assert tuple(occurrence.position for occurrence in added_occurrences) == (0, 1, 2)
    assert len(
        {occurrence.act_occurrence_identity for occurrence in added_occurrences}
    ) == 3
    assert len({occurrence.result_identity for occurrence in added_occurrences}) == 3
    assert {
        occurrence.result_reference.locality_identity
        for occurrence in added_occurrences
    } == {"fixture-locality"}
    assert tuple(
        (
            occurrence.source_material,
            occurrence.added_position,
            occurrence.added_material,
        )
        for occurrence in occurrences
    ) == ((b"aa", 0, b"a"), (b"aa", 1, b"a"), (b"aa", 2, b"a"))
    assert len({occurrence.occurrence_identity for occurrence in occurrences}) == 3
    assert all(
        hash(occurrence) == hash(occurrence.act_occurrence_identity)
        and hash(occurrence.result_reference) == hash(occurrence.result_identity)
        for occurrence in added_occurrences
    )
    assert all(
        occurrence.source_coordinate is added_occurrence
        for occurrence, added_occurrence in zip(occurrences, added_occurrences)
    )
    assert all(
        preserves_original_order(
            source_material=occurrence.source_material,
            result_material=occurrence.result_material,
            added_position=occurrence.position,
        )
        for occurrence in added_occurrences
    )
    with pytest.raises(ValueError, match="crossed Localities"):
        replace(added_occurrences[0], locality_identity="other-locality")


def test_a_different_source_order_is_refused_before_the_implementation_function():
    supplied = []
    source = ExactMaterialReference(
        "source-occurrence", "source-assertion", "fixture-locality", b"ab"
    )
    added = ExactMaterialReference(
        "added-occurrence", "added-assertion", "fixture-locality", b"x"
    )
    implementation_function = CompiledImplementationFunction(
        identity="fixture",
        invocation=lambda material: supplied.append(material),
    )

    with pytest.raises(ValueError, match="exact source order"):
        AddedPositionOccurrence(
            boundary_identity="different-source-addition",
            locality_identity="fixture-locality",
            occurrence_position=0,
            source_reference=source,
            position=1,
            added_reference=added,
            result_material=b"bxa",
        )

    assert supplied == []


def test_equal_source_material_keeps_distinct_source_assertion_references():
    first = ExactMaterialReference(
        "source-a", "assertion-a", "fixture-locality", b"aa"
    )
    second = ExactMaterialReference(
        "source-b", "assertion-b", "fixture-locality", b"aa"
    )
    added = ExactMaterialReference(
        "added", "added-assertion", "fixture-locality", b"a"
    )

    occurrences = added_position_occurrences(
        (first, second), (added,), boundary_identity="equal-source-addition"
    )

    assert len(occurrences) == 6
    assert {occurrence.source_reference for occurrence in occurrences} == {
        first,
        second,
    }
    assert len({occurrence.act_occurrence_identity for occurrence in occurrences}) == 6
    assert len({occurrence.result_identity for occurrence in occurrences}) == 6


def test_admitted_material_addition_refuses_cross_locality_material():
    first = ExactMaterialReference(
        "source-a", "assertion-a", "fixture-locality-a", b"a"
    )
    second = ExactMaterialReference(
        "source-b", "assertion-b", "fixture-locality-b", b"b"
    )
    admission = admission_occurrence(
        ((first, second),),
        boundary_identity="cross-locality-admission",
        source_material=(first, second),
    )

    with pytest.raises(ValueError, match="crossed Localities"):
        admission_added_position_occurrences(
            admission.result_reference,
            boundary_identity="cross-locality-addition",
            admitted_material_act_occurrence_count_limit=8,
        )


def test_every_three_byte_result_reaches_every_compiled_implementation_function(
    book_three_byte_format_occurrences,
):
    _, added_occurrences, occurrences = book_three_byte_format_occurrences
    exact_material = tuple(
        occurrence.result_material for occurrence in added_occurrences
    )

    assert len(occurrences) == len(COMPILED_IMPLEMENTATION_FUNCTIONS)
    assert all(
        tuple(occurrence.exact_material for occurrence in row) == exact_material
        for row in occurrences
    )


def test_three_byte_results_establish_different_compiled_invocation_boundaries(
    book_three_byte_format_occurrences,
):
    _, _, occurrences = book_three_byte_format_occurrences
    admissions = tuple(
        _admission(row, lambda occurrence: occurrence.returned)
        for row in occurrences
    )
    boundaries = tuple(_return_boundaries(row) for row in occurrences)

    assert len(set(admissions)) > 1
    assert any(boundaries)
    assert len({frozenset(found) for found in boundaries}) > 1


def test_each_addition_compare_keeps_both_invocation_occurrences_and_the_act(
    book_added_position_comparisons, book_three_byte_format_occurrences
):
    additions = book_three_byte_format_occurrences[1]
    expected = len(COMPILED_IMPLEMENTATION_FUNCTIONS) * len(additions)
    comparisons = tuple(
        comparison
        for row in book_added_position_comparisons
        for comparison in row
    )

    assert len(comparisons) == expected
    assert len({comparison.occurrence_identity for comparison in comparisons}) == expected
    assert {
        comparison.added_position_act_occurrence_identity
        for comparison in comparisons
    } == {addition.act_occurrence_identity for addition in additions}
    assert len(
        {comparison.source_invocation_occurrence_identity for comparison in comparisons}
    ) == len(COMPILED_IMPLEMENTATION_FUNCTIONS) * len(
        {addition.source_reference for addition in additions}
    )
    assert len(
        {comparison.result_invocation_occurrence_identity for comparison in comparisons}
    ) == expected


def test_addition_compare_finds_same_and_different_return_coordinates(
    book_added_position_comparisons,
):
    distinctions = tuple(
        comparison.distinction
        for row in book_added_position_comparisons
        for comparison in row
    )

    assert any(distinctions)
    assert any(not distinction for distinction in distinctions)


def test_addition_admission_preserves_every_exact_act_occurrence(
    book_added_position_admission, book_three_byte_format_occurrences
):
    additions = book_three_byte_format_occurrences[1]
    admitted = tuple(
        occurrence
        for same_coordinates in book_added_position_admission
        for occurrence in same_coordinates
    )

    assert len(admitted) == len(additions)
    assert {occurrence.act_occurrence_identity for occurrence in admitted} == {
        occurrence.act_occurrence_identity for occurrence in additions
    }
    assert len({occurrence.act_occurrence_identity for occurrence in admitted}) == len(
        admitted
    )


def test_addition_admission_finds_recurring_complete_compare_coordinates(
    book_added_position_admission, book_added_position_comparisons
):
    found = {}
    for row in book_added_position_comparisons:
        for comparison in row:
            found.setdefault(
                comparison.added_position_act_occurrence_identity, []
            ).append(
                (
                    comparison.implementation_function_identity,
                    comparison.source_returned,
                    comparison.result_returned,
                )
            )
    coordinates = {
        identity: tuple(coordinate) for identity, coordinate in found.items()
    }

    assert len(book_added_position_admission) > 1
    assert any(
        len(same_coordinates) > 1
        for same_coordinates in book_added_position_admission
    )
    for same_coordinates in book_added_position_admission:
        assert len(
            {
                coordinates[occurrence.act_occurrence_identity]
                for occurrence in same_coordinates
            }
        ) == 1


def test_addition_admission_refuses_incomplete_compare_coverage(
    book_three_byte_format_occurrences, book_added_position_comparisons
):
    incomplete = (
        book_added_position_comparisons[0][:-1],
        *book_added_position_comparisons[1:],
    )

    with pytest.raises(ValueError, match="every addition Act occurrence"):
        admit_added_position_occurrences(
            book_three_byte_format_occurrences[1],
            incomplete,
        )


def test_equal_result_material_keeps_distinct_occurrences_in_one_admission():
    source = ExactMaterialReference(
        "source", "source-assertion", "fixture-locality", b"aa"
    )
    added = ExactMaterialReference(
        "added", "added-assertion", "fixture-locality", b"a"
    )
    implementation_function = CompiledImplementationFunction(
        identity="fixture", invocation=lambda material: material
    )
    additions = added_position_occurrences(
        (source,), (added,), boundary_identity="equal-result-addition"
    )
    source_invocations = compiled_reference_invocations(
        (source,),
        boundary_identity="equal-result-source",
        implementation_functions=(implementation_function,),
    )
    result_invocations = added_position_invocations(
        additions,
        boundary_identity="equal-result-result",
        implementation_functions=(implementation_function,),
    )
    comparisons = compare_added_position_invocations(
        source_invocations,
        result_invocations,
        boundary_identity="equal-result-compare",
    )

    admission = admit_added_position_occurrences(additions, comparisons)

    assert admission == (additions,)
    assert tuple(occurrence.position for occurrence in admission[0]) == (0, 1, 2)
    assert len({occurrence.act_occurrence_identity for occurrence in admission[0]}) == 3


def test_each_function_and_complete_admission_has_one_exact_occurrence(
    book_added_position_admission_occurrences,
    book_three_byte_format_occurrences,
):
    additions = book_three_byte_format_occurrences[1]
    addition_identities = {
        occurrence.act_occurrence_identity for occurrence in additions
    }

    assert len(book_added_position_admission_occurrences) == (
        len(COMPILED_IMPLEMENTATION_FUNCTIONS) + 1
    )
    assert len(
        {
            occurrence.act_occurrence_identity
            for occurrence in book_added_position_admission_occurrences
        }
    ) == len(book_added_position_admission_occurrences)
    assert len(
        {
            occurrence.result_identity
            for occurrence in book_added_position_admission_occurrences
        }
    ) == len(book_added_position_admission_occurrences)
    for occurrence in book_added_position_admission_occurrences:
        assert occurrence.source_material == additions
        assert occurrence.comparison_occurrences
        assert {
            addition.act_occurrence_identity
            for admitted in occurrence.admitted_material
            for addition in admitted
        } == addition_identities


def test_addition_admission_refuses_a_result_without_its_compare_occurrences(
    book_added_position_admission_occurrences,
):
    exact = book_added_position_admission_occurrences[-1]
    first, second, *remaining = exact.admitted_material
    changed = type(exact.admission_occurrence)(
        boundary_identity="changed-addition-admission",
        occurrence_position=0,
        source_material=exact.source_material,
        admitted_material=(first + second, *remaining),
    )

    with pytest.raises(ValueError, match="differs from its Compare occurrences"):
        AddedPositionAdmissionOccurrence(
            admission_occurrence=changed,
            addition_occurrences=exact.addition_occurrences,
            comparison_occurrences=exact.comparison_occurrences,
        )


def test_every_ordered_admission_result_pair_has_one_exact_compare_occurrence(
    book_added_position_admission_occurrences,
    book_added_position_admission_comparisons,
):
    occurrence_count = len(book_added_position_admission_occurrences)
    expected = occurrence_count * (occurrence_count - 1)
    exact_pairs = {
        (first.result_identity, second.result_identity)
        for first in book_added_position_admission_occurrences
        for second in book_added_position_admission_occurrences
        if first is not second
    }

    assert len(book_added_position_admission_comparisons) == expected
    assert len(
        {
            comparison.act_occurrence_identity
            for comparison in book_added_position_admission_comparisons
        }
    ) == expected
    assert len(
        {
            comparison.result_identity
            for comparison in book_added_position_admission_comparisons
        }
    ) == expected
    assert {
        (
            comparison.first_reference.result_identity,
            comparison.second_reference.result_identity,
        )
        for comparison in book_added_position_admission_comparisons
    } == exact_pairs
    assert all(
        comparison.result_reference.compare_occurrence is comparison
        and comparison.first_reference.admission_occurrence
        in book_added_position_admission_occurrences
        and comparison.second_reference.admission_occurrence
        in book_added_position_admission_occurrences
        and comparison.result_reference.first_reference
        == comparison.first_reference
        and comparison.result_reference.second_reference
        == comparison.second_reference
        and comparison.result_reference.result is comparison.result
        for comparison in book_added_position_admission_comparisons
    )

    for comparison in book_added_position_admission_comparisons:
        assert comparison.first_reference.admission_occurrence.comparison_occurrences
        assert comparison.second_reference.admission_occurrence.comparison_occurrences


def test_every_function_admission_preserves_each_function_admission(
    book_added_position_admission_occurrences,
    book_added_position_admission_comparisons,
):
    every_function = book_added_position_admission_occurrences[-1].result_reference
    from_every_function = tuple(
        comparison
        for comparison in book_added_position_admission_comparisons
        if comparison.first_reference == every_function
    )
    toward_every_function = tuple(
        comparison
        for comparison in book_added_position_admission_comparisons
        if comparison.second_reference == every_function
    )

    assert len(from_every_function) == len(COMPILED_IMPLEMENTATION_FUNCTIONS)
    assert all(comparison.result for comparison in from_every_function)
    assert len(toward_every_function) == len(COMPILED_IMPLEMENTATION_FUNCTIONS)
    assert any(not comparison.result for comparison in toward_every_function)
    assert any(
        comparison.result for comparison in book_added_position_admission_comparisons
    )
    assert any(
        not comparison.result
        for comparison in book_added_position_admission_comparisons
    )


def test_every_exact_added_position_pair_has_one_compare_occurrence(
    book_added_position_pair_comparisons,
    book_three_byte_format_occurrences,
    book_added_position_comparisons,
):
    additions = book_three_byte_format_occurrences[1]
    additions_by_identity = {
        occurrence.act_occurrence_identity: occurrence for occurrence in additions
    }
    addition_identities = set(additions_by_identity)
    source_references = {occurrence.source_reference for occurrence in additions}
    added_references = {occurrence.added_reference for occurrence in additions}
    participation = {identity: 0 for identity in addition_identities}
    compare_occurrences = {identity: [] for identity in addition_identities}
    for row in book_added_position_comparisons:
        for comparison in row:
            compare_occurrences[
                comparison.added_position_act_occurrence_identity
            ].append(comparison)

    assert len(book_added_position_pair_comparisons) == len(additions)
    assert len(
        {
            comparison.occurrence_identity
            for comparison in book_added_position_pair_comparisons
        }
    ) == len(book_added_position_pair_comparisons)
    for comparison in book_added_position_pair_comparisons:
        assert comparison.source_reference in source_references
        assert comparison.added_reference in added_references
        assert comparison.first_position < comparison.second_position
        assert (
            comparison.first_added_position_act_occurrence_identity
            in addition_identities
        )
        assert (
            comparison.second_added_position_act_occurrence_identity
            in addition_identities
        )
        first = additions_by_identity[
            comparison.first_added_position_act_occurrence_identity
        ]
        second = additions_by_identity[
            comparison.second_added_position_act_occurrence_identity
        ]
        assert first.source_reference == second.source_reference == (
            comparison.source_reference
        )
        assert first.added_reference == second.added_reference == (
            comparison.added_reference
        )
        assert first.position == comparison.first_position
        assert second.position == comparison.second_position
        assert comparison.first_compare_occurrence_identities == tuple(
            found.occurrence_identity
            for found in compare_occurrences[first.act_occurrence_identity]
        )
        assert comparison.second_compare_occurrence_identities == tuple(
            found.occurrence_identity
            for found in compare_occurrences[second.act_occurrence_identity]
        )
        assert comparison.first_returned_coordinates == tuple(
            (
                found.implementation_function_identity,
                found.source_returned,
                found.result_returned,
            )
            for found in compare_occurrences[first.act_occurrence_identity]
        )
        assert comparison.second_returned_coordinates == tuple(
            (
                found.implementation_function_identity,
                found.source_returned,
                found.result_returned,
            )
            for found in compare_occurrences[second.act_occurrence_identity]
        )
        assert len(comparison.first_compare_occurrence_identities) == len(
            COMPILED_IMPLEMENTATION_FUNCTIONS
        )
        assert len(comparison.second_compare_occurrence_identities) == len(
            COMPILED_IMPLEMENTATION_FUNCTIONS
        )
        participation[
            comparison.first_added_position_act_occurrence_identity
        ] += 1
        participation[
            comparison.second_added_position_act_occurrence_identity
        ] += 1
    assert set(participation.values()) == {2}


def test_added_position_pairs_find_same_and_different_complete_coordinates(
    book_added_position_pair_comparisons,
):
    distinctions = tuple(
        comparison.distinction
        for comparison in book_added_position_pair_comparisons
    )

    assert any(distinctions)
    assert any(not distinction for distinction in distinctions)


def test_addition_compare_refuses_a_missing_source_reference():
    first = ExactMaterialReference(
        "source-a", "assertion-a", "fixture-locality", b"a"
    )
    second = ExactMaterialReference(
        "source-b", "assertion-b", "fixture-locality", b"b"
    )
    added = ExactMaterialReference(
        "added", "added-assertion", "fixture-locality", b"b"
    )
    implementation_function = CompiledImplementationFunction(
        identity="fixture", invocation=lambda material: material
    )
    additions = added_position_occurrences(
        (first,), (added,), boundary_identity="addition"
    )
    source_invocations = compiled_reference_invocations(
        (first, second),
        boundary_identity="source",
        implementation_functions=(implementation_function,),
    )
    result_invocations = added_position_invocations(
        additions,
        boundary_identity="result",
        implementation_functions=(implementation_function,),
    )

    with pytest.raises(ValueError, match="no exact source invocation"):
        compare_added_position_invocations(
            (source_invocations[0][1:],),
            result_invocations,
            boundary_identity="compare",
        )


def test_addition_compare_refuses_a_result_without_its_act_occurrence():
    source = ExactMaterialReference(
        "source", "source-assertion", "fixture-locality", b"a"
    )
    implementation_function = CompiledImplementationFunction(
        identity="fixture", invocation=lambda material: material
    )
    source_invocations = compiled_reference_invocations(
        (source,),
        boundary_identity="source",
        implementation_functions=(implementation_function,),
    )
    result_invocations = compiled_invocations(
        (b"ab",),
        boundary_identity="result",
        implementation_functions=(implementation_function,),
    )

    with pytest.raises(ValueError, match="exact addition occurrence"):
        compare_added_position_invocations(
            source_invocations,
            result_invocations,
            boundary_identity="compare",
        )


def test_each_measured_pair_position_has_an_exact_removal_occurrence(
    book_removed_position_invocation_occurrences, measured_book_pairs
):
    occurrences, _ = book_removed_position_invocation_occurrences
    source_references = set(measured_book_pairs[6])
    removed_references = set(measured_book_pairs[7])

    assert len(occurrences) == len(source_references) * 2
    assert all(
        occurrence.source_reference in source_references
        and occurrence.removed_reference in removed_references
        and occurrence.source_material[
            occurrence.position : occurrence.position + 1
        ]
        == occurrence.removed_material
        and occurrence.result_material
        == occurrence.source_material[: occurrence.position]
        + occurrence.source_material[occurrence.position + 1 :]
        for occurrence in occurrences
    )
    assert len({occurrence.act_occurrence_identity for occurrence in occurrences}) == len(
        occurrences
    )
    assert len({occurrence.result_identity for occurrence in occurrences}) == len(
        occurrences
    )


def test_each_removal_result_reaches_every_compiled_implementation_function(
    book_removed_position_invocation_occurrences,
):
    removals, invocations = book_removed_position_invocation_occurrences
    exact_results = tuple(removal.result_material for removal in removals)

    assert len(invocations) == len(COMPILED_IMPLEMENTATION_FUNCTIONS)
    assert all(
        tuple(invocation.exact_material for invocation in row) == exact_results
        for row in invocations
    )
    assert all(
        tuple(invocation.source_coordinate for invocation in row) == removals
        for row in invocations
    )


def test_each_removal_compare_keeps_both_invocation_occurrences_and_the_act(
    book_removed_position_comparisons,
    book_removed_position_invocation_occurrences,
):
    removals = book_removed_position_invocation_occurrences[0]
    comparisons = tuple(
        comparison
        for row in book_removed_position_comparisons
        for comparison in row
    )
    expected = len(COMPILED_IMPLEMENTATION_FUNCTIONS) * len(removals)

    assert len(comparisons) == expected
    assert len({comparison.occurrence_identity for comparison in comparisons}) == expected
    assert {
        comparison.removed_position_act_occurrence_identity
        for comparison in comparisons
    } == {removal.act_occurrence_identity for removal in removals}
    assert len(
        {comparison.result_invocation_occurrence_identity for comparison in comparisons}
    ) == expected


def test_removal_compare_finds_same_and_different_return_coordinates(
    book_removed_position_comparisons,
):
    distinctions = tuple(
        comparison.distinction
        for row in book_removed_position_comparisons
        for comparison in row
    )

    assert any(distinctions)
    assert any(not distinction for distinction in distinctions)


def test_removal_compare_refuses_a_result_without_its_act_occurrence():
    source = ExactMaterialReference(
        "source", "source-assertion", "fixture-locality", b"ab"
    )
    implementation_function = CompiledImplementationFunction(
        identity="fixture", invocation=lambda material: material
    )
    source_invocations = compiled_reference_invocations(
        (source,),
        boundary_identity="source",
        implementation_functions=(implementation_function,),
    )
    result_invocations = compiled_invocations(
        (b"a",),
        boundary_identity="result",
        implementation_functions=(implementation_function,),
    )

    with pytest.raises(ValueError, match="exact removal occurrence"):
        compare_removed_position_invocations(
            source_invocations,
            result_invocations,
            boundary_identity="compare",
        )


def test_removal_result_admission_comes_from_exact_compare_distinctions(
    book_removal_result_additions,
    book_removed_position_comparisons,
):
    admitted_identities, admitted_removals, source_references, _, _ = (
        book_removal_result_additions
    )
    observed = {
        comparison.removed_position_act_occurrence_identity
        for row in book_removed_position_comparisons
        for comparison in row
        if comparison.distinction
    }

    assert admitted_identities == observed
    assert admitted_identities
    assert {
        removal.act_occurrence_identity for removal in admitted_removals
    } == admitted_identities
    assert tuple(removal.result_reference for removal in admitted_removals) == (
        source_references
    )


def test_addition_uses_exact_removal_results_as_its_source(
    book_removal_result_additions,
):
    _, _, source_references, additions, comparisons = book_removal_result_additions
    exact_sources = set(source_references)
    addition_occurrence_identities = {
        addition.act_occurrence_identity for addition in additions
    }

    assert additions
    assert all(addition.source_reference in exact_sources for addition in additions)
    assert len({addition.act_occurrence_identity for addition in additions}) == len(
        additions
    )
    assert len({addition.result_identity for addition in additions}) == len(additions)
    assert all(
        comparison.added_position_act_occurrence_identity
        in addition_occurrence_identities
        for row in comparisons
        for comparison in row
    )
    assert len(tuple(comparison for row in comparisons for comparison in row)) == (
        len(COMPILED_IMPLEMENTATION_FUNCTIONS) * len(additions)
    )


def test_compiled_implementation_function_receives_the_exact_material():
    supplied = []

    def invocation(material):
        supplied.append(material)

    occurrence = compiled_invocation(
        b"\xff\x00",
        CompiledImplementationFunction(identity="fixture", invocation=invocation),
        boundary_identity="exact-material",
    )

    assert supplied == [b"\xff\x00"]
    assert occurrence.exact_material == b"\xff\x00"
    assert occurrence.returned is True


def test_equal_material_at_distinct_coordinates_reaches_the_implementation_function_each_time():
    supplied = []
    material = (b"aa", b"aa", b"ab")
    implementation_function = CompiledImplementationFunction(
        identity="fixture",
        invocation=lambda exact: supplied.append(exact),
    )

    occurrences = compiled_invocations(
        material,
        boundary_identity="distinct-coordinates",
        implementation_functions=(implementation_function,),
    )[0]

    assert supplied == list(material)
    assert tuple(occurrence.exact_material for occurrence in occurrences) == material
    assert len({occurrence.occurrence_identity for occurrence in occurrences}) == 3


def test_compiled_implementation_function_refusal_and_input_boundary_are_distinct():
    supplied = []

    def invocation(material):
        supplied.append(material)
        raise ValueError

    implementation_function = CompiledImplementationFunction(identity="fixture", invocation=invocation)

    occurrence = compiled_invocation(
        b"\x00", implementation_function, boundary_identity="returned-refusal"
    )
    with pytest.raises(TypeError, match="exact bytes"):
        compiled_invocation(
            "material", implementation_function, boundary_identity="input-refusal"
        )

    assert supplied == [b"\x00"]
    assert occurrence.returned is False


def test_a_non_byte_material_is_refused_before_an_implementation_function_occurs(monkeypatch):
    occurrences = []
    monkeypatch.setattr(
        "compiled_material_invocation.subprocess.run",
        lambda *args, **kwargs: occurrences.append((args, kwargs)),
    )

    with pytest.raises(TypeError, match="exact bytes"):
        invocation_occurrence(
            "material",
            MATERIAL_IMPLEMENTATION_FUNCTIONS[0],
            boundary_identity="material",
        )

    assert occurrences == []


def test_exact_bytes_reach_the_implementation_function_without_prior_decoding(monkeypatch):
    supplied = []

    class Completed:
        returncode = 0
        stdout = b"implementation function material"
        stderr = b""

    def compiled_occurrence(*args, **kwargs):
        supplied.append(kwargs["input"])
        return Completed()

    monkeypatch.setattr(
        "compiled_material_invocation.subprocess.run", compiled_occurrence
    )

    found = invocation_occurrence(
        b"\xff\x00",
        MATERIAL_IMPLEMENTATION_FUNCTIONS[0],
        boundary_identity="material",
    )

    assert supplied == [b"\xff\x00"]
    assert found.exact_material == b"\xff\x00"
    assert found.stdout_bytes == b"implementation function material"


def test_recurring_result_coordinates_precede_one_later_invocation(monkeypatch):
    supplied = []

    class Completed:
        stderr = b""

        def __init__(self, material):
            self.stdout = material
            self.returncode = int(material == b"c")

    def compiled_occurrence(*args, **kwargs):
        supplied.append(kwargs["input"])
        return Completed(kwargs["input"])

    monkeypatch.setattr(
        "compiled_material_invocation.subprocess.run", compiled_occurrence
    )
    references = tuple(
        ExactMaterialReference(
            f"source-{position}",
            f"assertion-{position}",
            "recurrence-locality",
            material,
        )
        for position, material in enumerate((b"a", b"b", b"c"))
    )
    admission = admission_occurrence(
        (references,),
        boundary_identity="recurrence-admission",
        source_material=references,
    )
    all_additions = admission_added_position_occurrences(
        admission.result_reference,
        boundary_identity="recurrence-addition",
        admitted_material_act_occurrence_count_limit=18,
    )
    additions = tuple(
        addition
        for addition in all_additions
        if addition.position == 0
        and addition.source_reference == references[0]
    )
    function = MaterialImplementationFunction(
        identity="compiled-0",
        invocation=("compiled-0",),
    )
    source_invocations = {
        reference: invocation_occurrence(
            reference.exact_material,
            function,
            boundary_identity="recurrence-source",
            invocation_position=position,
            source_reference=reference,
        )
        for position, reference in enumerate(references)
    }
    known_additions = additions[:2]
    later_addition = additions[2]
    known_comparisons = tuple(
        MaterialAddedReturnCompareOccurrence(
            boundary_identity="recurrence-compare",
            occurrence_position=position,
            addition_occurrence=addition,
            source_invocation=source_invocations[addition.source_reference],
            result_invocation=invocation_occurrence(
                addition.result_material,
                function,
                boundary_identity="recurrence-result",
                invocation_position=position,
                source_reference=addition.result_reference,
            ),
        )
        for position, addition in enumerate(known_additions)
    )

    coordinates = recurring_added_result_coordinates(
        known_comparisons,
        later_addition,
        source_invocations[later_addition.source_reference],
    )

    assert later_addition.result_material == b"ca"
    assert all(
        comparison.addition_occurrence.result_material
        != later_addition.result_material
        for comparison in known_comparisons
    )
    assert later_addition.result_material not in supplied
    later_invocation = invocation_occurrence(
        later_addition.result_material,
        function,
        boundary_identity="recurrence-later-result",
        source_reference=later_addition.result_reference,
    )
    assert coordinates == later_invocation.return_coordinates

    conflicting = replace(
        known_comparisons[1],
        result_invocation=replace(
            known_comparisons[1].result_invocation,
            returncode=1,
        ),
    )
    assert (
        recurring_added_result_coordinates(
            (known_comparisons[0], conflicting),
            later_addition,
            source_invocations[later_addition.source_reference],
        )
        is None
    )

    supplied.clear()
    earlier, recurring_coordinates, later_compare = (
        first_recurring_added_return_compare(
            all_additions,
            tuple(source_invocations.values()),
            function,
            boundary_identity="recurrence-later",
            act_occurrence_count_limit=len(all_additions),
        )
    )
    assert later_compare is not None
    assert recurring_coordinates == later_compare.result_coordinates
    assert tuple(supplied) == tuple(
        comparison.addition_occurrence.result_material for comparison in earlier
    ) + (later_compare.addition_occurrence.result_material,)
    assert later_compare.addition_occurrence.result_material not in supplied[:-1]
    assert len(supplied) < len(all_additions)

    same_source_coordinates = tuple(
        replace(invocation, returncode=0)
        for invocation in source_invocations.values()
    )
    supplied.clear()
    assert first_recurring_added_return_compare(
        all_additions,
        same_source_coordinates,
        function,
        boundary_identity="recurrence-one-source-coordinate",
        act_occurrence_count_limit=len(all_additions),
    ) == ((), None, None)
    assert supplied == []


def test_time_limit_preserves_an_invocation_that_did_not_return(monkeypatch):
    function = MaterialImplementationFunction(
        identity="compiled-0",
        invocation=("compiled-0",),
    )

    def did_not_return(*args, **kwargs):
        assert kwargs["timeout"] == 0.25
        raise subprocess.TimeoutExpired(
            args[0],
            kwargs["timeout"],
            output=b"available output",
            stderr=None,
        )

    monkeypatch.setattr("compiled_material_invocation.subprocess.run", did_not_return)

    occurrence = invocation_occurrence(
        b"material",
        function,
        boundary_identity="time-limit-boundary",
        time_limit_second_count=0.25,
    )

    assert occurrence.returned is False
    assert occurrence.returncode is None
    assert occurrence.stdout_bytes == b"available output"
    assert occurrence.stderr_bytes is None
    assert occurrence.time_limit_second_count == 0.25
    assert occurrence.time_limit_reached
    assert occurrence.coordinates == (
        0.25,
        None,
        False,
        True,
        False,
        False,
        None,
        b"available output",
        None,
    )


def test_material_byte_count_limit_preserves_the_exact_available_prefix():
    occurrence = invocation_occurrence(
        b"",
        MaterialImplementationFunction(
            identity="compiled-0",
            invocation=(
                "/bin/sh",
                "-c",
                "while :; do printf 0123456789; done",
            ),
        ),
        boundary_identity="material-byte-count-limit",
        time_limit_second_count=1.0,
        material_byte_count_limit=127,
    )

    assert not occurrence.returned
    assert occurrence.returncode is None
    assert not occurrence.time_limit_reached
    assert occurrence.stdout_byte_count_limit_reached
    assert not occurrence.stderr_byte_count_limit_reached
    assert occurrence.stdout_bytes == (b"0123456789" * 13)[:127]
    assert occurrence.stderr_bytes == b""
    assert occurrence.return_coordinates == (
        1.0,
        127,
        False,
        False,
        True,
        False,
        None,
    )


def test_exact_material_at_the_byte_count_limit_can_return():
    occurrence = invocation_occurrence(
        b"abc",
        MaterialImplementationFunction(
            identity="compiled-0",
            invocation=("/bin/cat",),
        ),
        boundary_identity="exact-material-byte-count-limit",
        time_limit_second_count=1.0,
        material_byte_count_limit=3,
    )

    assert occurrence.returned
    assert occurrence.returncode == 0
    assert occurrence.stdout_bytes == b"abc"
    assert occurrence.stderr_bytes == b""
    assert not occurrence.time_limit_reached
    assert not occurrence.stdout_byte_count_limit_reached
    assert not occurrence.stderr_byte_count_limit_reached
