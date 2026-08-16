from __future__ import annotations

from dataclasses import replace
from pathlib import Path
import sys
from types import SimpleNamespace

import pytest

from seed_runtime.events import EventLedger
from seed_runtime.material_ingest import ingest_material


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from compiled_format_invocation import (  # noqa: E402
    COMPILED_IMPLEMENTATION_FUNCTIONS,
    CompiledImplementationFunction,
    added_position_admission_occurrence,
    added_position_admission_occurrences,
    added_position_invocations,
    added_position_occurrences,
    compare_added_position_invocations,
    compiled_reference_invocations,
)
from compiled_material_invocation import (  # noqa: E402
    MATERIAL_IMPLEMENTATION_FUNCTIONS,
    MaterialAddedCompareOccurrence,
    MaterialImplementationFunction,
    compare_added_material_invocations,
    ingest_result_reference,
    reference_occurrences_across,
)
from material_admission import compare_admission_result_pairs  # noqa: E402


COMPILED_EXECUTABLE = ROOT / ".venv" / "bin" / "piper"
COMPILED_MATERIAL = (
    Path.home() / ".local" / "share" / "piper-voices" / "en_US-lessac-medium.onnx"
)
COMPILED_FUNCTION_AVAILABLE = COMPILED_EXECUTABLE.is_file() and COMPILED_MATERIAL.is_file()


def _codec_functions() -> tuple[CompiledImplementationFunction, ...]:
    return tuple(
        CompiledImplementationFunction(
            identity=f"compiled-{position + len(COMPILED_IMPLEMENTATION_FUNCTIONS)}",
            invocation=lambda material, name=name: material.decode(name),
        )
        for position, name in enumerate(("ascii", "utf-8", "big5hkscs"))
    )


def _material_functions() -> tuple[MaterialImplementationFunction, ...]:
    first = len(COMPILED_IMPLEMENTATION_FUNCTIONS) + len(_codec_functions())
    functions = tuple(
        MaterialImplementationFunction(
            identity=f"compiled-{first + position}",
            invocation=function.invocation,
        )
        for position, function in enumerate(MATERIAL_IMPLEMENTATION_FUNCTIONS)
    )
    return (
        *functions,
        MaterialImplementationFunction(
            identity=f"compiled-{first + len(functions)}",
            invocation=(
                "/usr/bin/env",
                "-i",
                "/bin/bash",
                "--noprofile",
                "--norc",
                "-n",
            ),
        ),
    )


@pytest.fixture(scope="module")
def small_boundary_material():
    if not COMPILED_FUNCTION_AVAILABLE:
        pytest.skip("compiled implementation function is unavailable")
    book = (ROOT / "book_of_seed" / "README.md").read_bytes()
    start = book.index(b"Seed")
    ledger = EventLedger()
    source = ingest_material(
        ledger,
        locality_identity="small-boundary-source",
        exact_bytes=book[start : start + 4],
        source_role="fixture material",
        source_boundary="fixture-0",
    )
    added = ingest_material(
        ledger,
        locality_identity="small-boundary-added",
        exact_bytes=b" ",
        source_role="fixture material",
        source_boundary="fixture-1",
    )
    source_reference = ingest_result_reference(ledger, source.identity)
    added_reference = ingest_result_reference(ledger, added.identity)
    additions = added_position_occurrences(
        (source_reference,),
        (added_reference,),
        boundary_identity="small-boundary-material-addition",
    )
    earlier_function_count = sum(
        map(
            len,
            (
                COMPILED_IMPLEMENTATION_FUNCTIONS,
                _codec_functions(),
                _material_functions(),
            ),
        )
    )
    implementation = MaterialImplementationFunction(
        identity=f"compiled-{earlier_function_count}",
        invocation=(
            str(COMPILED_EXECUTABLE),
            "-m",
            str(COMPILED_MATERIAL),
            "--output-raw",
        ),
    )
    source_invocations = reference_occurrences_across(
        (source_reference,),
        implementation_functions=(implementation,),
        boundary_identity="small-boundary-source-invocation",
        max_workers=1,
    )
    result_invocations = reference_occurrences_across(
        tuple(addition.result_reference for addition in additions),
        implementation_functions=(implementation,),
        boundary_identity="small-boundary-result-invocation",
        max_workers=1,
    )
    comparisons = compare_added_material_invocations(
        additions,
        source_invocations,
        result_invocations,
        boundary_identity="small-boundary-addition-compare",
    )
    return (
        ledger,
        source_reference,
        added_reference,
        additions,
        implementation,
        source_invocations,
        result_invocations,
        comparisons,
    )


def test_compiled_function_receives_the_exact_book_material(small_boundary_material):
    source_reference = small_boundary_material[1]
    source_invocation = small_boundary_material[5][0][0]

    assert source_reference.exact_material == b"Seed"
    assert source_invocation.exact_material == source_reference.exact_material
    assert source_invocation.source_reference == source_reference
    assert source_invocation.implementation_function == small_boundary_material[4]
    assert source_invocation.returncode == 0
    assert source_invocation.stdout_bytes
    assert source_invocation.stderr_bytes == b""


def test_every_addition_position_has_an_exact_invocation(small_boundary_material):
    additions = small_boundary_material[3]
    result_invocations = small_boundary_material[6][0]

    assert tuple(addition.position for addition in additions) == (0, 1, 2, 3, 4)
    assert len(result_invocations) == len(additions)
    assert tuple(
        invocation.source_reference for invocation in result_invocations
    ) == tuple(addition.result_reference for addition in additions)
    assert len({invocation.occurrence_identity for invocation in result_invocations}) == len(
        result_invocations
    )
    assert all(invocation.returncode == 0 for invocation in result_invocations)
    assert all(invocation.stdout_bytes for invocation in result_invocations)


def test_comparison_keeps_each_addition_and_both_invocations(small_boundary_material):
    additions = small_boundary_material[3]
    comparisons = small_boundary_material[7][0]

    assert len(comparisons) == len(additions)
    assert tuple(comparison.addition_occurrence for comparison in comparisons) == additions
    assert len({comparison.occurrence_identity for comparison in comparisons}) == len(
        comparisons
    )
    assert all(
        comparison.source_invocation.source_reference
        == comparison.addition_occurrence.source_reference
        for comparison in comparisons
    )
    assert all(
        comparison.result_invocation.source_reference
        == comparison.addition_occurrence.result_reference
        for comparison in comparisons
    )
    assert any(comparison.distinction for comparison in comparisons)


def test_comparisons_enter_the_same_addition_admission(small_boundary_material):
    additions = small_boundary_material[3]
    comparisons = small_boundary_material[7]

    admission = added_position_admission_occurrence(
        additions,
        comparisons,
        boundary_identity="small-boundary-addition-admission",
    )

    assert admission.source_material == additions
    assert admission.comparison_occurrences == comparisons
    assert {
        occurrence.act_occurrence_identity
        for same_coordinates in admission.admitted_material
        for occurrence in same_coordinates
    } == {occurrence.act_occurrence_identity for occurrence in additions}
    assert admission.result_reference.admission_occurrence is admission


def test_addition_admission_refuses_a_lookalike_compare(small_boundary_material):
    additions = small_boundary_material[3]
    comparisons = small_boundary_material[7]
    exact = comparisons[0][0]
    lookalike = SimpleNamespace(
        implementation_function_identity=exact.implementation_function_identity,
        added_position_act_occurrence_identity=(
            exact.added_position_act_occurrence_identity
        ),
        occurrence_identity=exact.occurrence_identity,
        source_coordinates=exact.source_coordinates,
        result_coordinates=exact.result_coordinates,
    )

    with pytest.raises(TypeError, match="exact addition Compare occurrences"):
        added_position_admission_occurrence(
            additions,
            ((lookalike, *comparisons[0][1:]),),
            boundary_identity="lookalike-small-boundary-admission",
        )


def test_small_boundary_refuses_a_lookalike_material_reference():
    lookalike = SimpleNamespace(exact_material=b"Seed")

    with pytest.raises(TypeError, match="exact references"):
        compiled_reference_invocations(
            (lookalike,),
            boundary_identity="lookalike-small-boundary",
        )


def test_one_small_boundary_compares_all_implementation_functions(
    small_boundary_material,
):
    source_reference = small_boundary_material[1]
    additions = small_boundary_material[3]
    additional_comparisons = small_boundary_material[7]
    compiled_functions = COMPILED_IMPLEMENTATION_FUNCTIONS + _codec_functions()
    material_functions = _material_functions()

    compiled_sources = compiled_reference_invocations(
        (source_reference,),
        boundary_identity="small-boundary-compiled-source",
        implementation_functions=compiled_functions,
    )
    compiled_results = added_position_invocations(
        additions,
        boundary_identity="small-boundary-compiled-result",
        implementation_functions=compiled_functions,
    )
    compiled_comparisons = compare_added_position_invocations(
        compiled_sources,
        compiled_results,
        boundary_identity="small-boundary-compiled-compare",
    )
    material_sources = reference_occurrences_across(
        (source_reference,),
        boundary_identity="small-boundary-material-source",
        implementation_functions=material_functions,
    )
    material_results = reference_occurrences_across(
        tuple(addition.result_reference for addition in additions),
        boundary_identity="small-boundary-material-result",
        implementation_functions=material_functions,
    )
    material_comparisons = compare_added_material_invocations(
        additions,
        material_sources,
        material_results,
        boundary_identity="small-boundary-material-compare",
    )
    comparison_rows = (
        *compiled_comparisons,
        *material_comparisons,
        *additional_comparisons,
    )
    admissions = added_position_admission_occurrences(
        additions,
        comparison_rows,
        boundary_identity="small-boundary-admission",
    )
    every_function_admission = admissions[-1]
    comparisons = compare_admission_result_pairs(
        tuple(admission.result_reference for admission in admissions),
        boundary_identity="small-boundary-admission-compare",
    )

    expected_function_count = len(compiled_functions) + len(material_functions) + 1
    assert len(comparison_rows) == expected_function_count
    assert all(len(row) == len(additions) for row in comparison_rows)
    assert len({row[0].implementation_function_identity for row in comparison_rows}) == (
        len(comparison_rows)
    )
    assert len({admission.act_occurrence_identity for admission in admissions}) == len(
        admissions
    )
    assert {
        occurrence.act_occurrence_identity
        for same_coordinates in every_function_admission.admitted_material
        for occurrence in same_coordinates
    } == {occurrence.act_occurrence_identity for occurrence in additions}
    assert len({admission.admitted_material for admission in admissions}) > 1
    from_every_function = tuple(
        comparison
        for comparison in comparisons
        if comparison.first_reference == every_function_admission.result_reference
    )
    toward_every_function = tuple(
        comparison
        for comparison in comparisons
        if comparison.second_reference == every_function_admission.result_reference
    )
    assert len(from_every_function) == len(toward_every_function) == len(
        comparison_rows
    )
    assert all(comparison.result for comparison in from_every_function)
    assert any(not comparison.result for comparison in toward_every_function)


def test_each_returned_material_can_enter_a_fresh_locality(
    small_boundary_material,
):
    ledger = small_boundary_material[0]
    invocations = small_boundary_material[6][0]
    ingests = tuple(
        ingest_material(
            ledger,
            locality_identity=f"small-boundary-result-{position}",
            exact_bytes=invocation.stdout_bytes,
            source_role="fixture material",
            source_boundary=f"fixture-result-{position}",
        )
        for position, invocation in enumerate(invocations)
    )
    references = tuple(
        ingest_result_reference(ledger, event.identity) for event in ingests
    )

    assert len({event.locality_identity for event in ingests}) == len(ingests)
    assert tuple(reference.exact_material for reference in references) == tuple(
        invocation.stdout_bytes for invocation in invocations
    )
    assert len({reference.result_identity for reference in references}) == len(
        references
    )


def test_compare_refuses_a_result_from_another_addition(small_boundary_material):
    additions = small_boundary_material[3]
    source = small_boundary_material[5][0][0]
    results = small_boundary_material[6][0]

    with pytest.raises(ValueError, match="result differs from its addition Act"):
        MaterialAddedCompareOccurrence(
            boundary_identity="changed-small-boundary-compare",
            occurrence_position=0,
            addition_occurrence=additions[0],
            source_invocation=source,
            result_invocation=results[1],
        )


def test_compare_refuses_different_time_limits(small_boundary_material):
    addition = small_boundary_material[3][0]
    source = small_boundary_material[5][0][0]
    result = replace(
        small_boundary_material[6][0][0],
        time_limit_second_count=31.0,
    )

    with pytest.raises(ValueError, match="cannot cross time limits"):
        MaterialAddedCompareOccurrence(
            boundary_identity="changed-time-limit-compare",
            occurrence_position=0,
            addition_occurrence=addition,
            source_invocation=source,
            result_invocation=result,
        )
