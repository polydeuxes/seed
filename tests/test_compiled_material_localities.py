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
    admission_added_position_occurrences,
    exact_byte_material_references,
)
from compiled_material_invocation import (  # noqa: E402
    MaterialImplementationFunction,
    admit_invocation_occurrences,
    admit_invocation_return_occurrences,
    compare_added_material_invocations,
    ingest_result_reference,
    material_locality_admission_occurrences,
    reference_occurrences_across,
)
from material_fixture_measurement import measured_one_byte_material  # noqa: E402
from material_admission import admission_occurrence  # noqa: E402


@pytest.fixture(scope="module")
def material_invocations():
    ledger, references = measured_one_byte_material()
    function = MaterialImplementationFunction(
        identity="compiled-0",
        invocation=(
            sys.executable,
            "-I",
            str(Path(__file__).with_name("compiled_tic_tac_toe.py")),
        ),
    )
    occurrences = reference_occurrences_across(
        references,
        boundary_identity="one-byte-compiled-material",
        implementation_functions=(function,),
    )[0]
    return ledger, references, occurrences


@pytest.fixture(scope="module")
def material_pair_invocations(material_invocations):
    ledger, references, source_occurrences = material_invocations
    locality_admissions = material_locality_admission_occurrences(
        source_occurrences,
        boundary_identity="one-byte-compiled-material-admission",
    )
    if len(locality_admissions) != 1:
        raise ValueError("one exact material Locality is required")
    admission = locality_admissions[0].material_admission
    additions = admission_added_position_occurrences(
        admission.result_reference,
        boundary_identity="one-byte-pair-addition",
        admitted_material_act_occurrence_count_limit=len(references) ** 2,
    )
    implementation_function = source_occurrences[0].implementation_function
    result_occurrences = reference_occurrences_across(
        tuple(addition.result_reference for addition in additions),
        boundary_identity="one-byte-pair-compiled-material",
        implementation_functions=(implementation_function,),
    )[0]
    comparisons = compare_added_material_invocations(
        additions,
        (source_occurrences,),
        (result_occurrences,),
        boundary_identity="one-byte-pair-compare",
    )[0]
    return (
        ledger,
        references,
        admission,
        additions,
        result_occurrences,
        comparisons,
    )


def test_every_measured_byte_reaches_the_compiled_function(material_invocations):
    _, references, occurrences = material_invocations

    assert len(references) == len(occurrences) == 256
    assert tuple(reference.exact_material for reference in references) == tuple(
        bytes((value,)) for value in range(256)
    )
    assert {reference.locality_identity for reference in references} == {
        "one-byte-measurement"
    }
    assert tuple(occurrence.source_reference for occurrence in occurrences) == references
    assert len({occurrence.occurrence_identity for occurrence in occurrences}) == 256
    assert all(occurrence.returned for occurrence in occurrences)


def test_compiled_function_establishes_distinct_raw_coordinates(
    material_invocations,
):
    _, references, occurrences = material_invocations
    admission = admit_invocation_occurrences(
        occurrences,
        boundary_identity="one-byte-compiled-material-admission",
    )

    assert admission.source_material == references
    assert len({occurrence.returncode for occurrence in occurrences}) > 1
    assert len(admission.admitted_material) > 1


def test_return_admission_does_not_replace_exact_result_material(
    material_invocations,
):
    _, _, occurrences = material_invocations
    changed = (
        replace(occurrences[0], stdout_bytes=b"provider material"),
        *occurrences[1:],
    )
    exact = admit_invocation_occurrences(
        changed,
        boundary_identity="one-byte-exact-material-admission",
    )
    returned = admit_invocation_return_occurrences(
        changed,
        boundary_identity="one-byte-return-admission",
    )

    assert len(exact.admitted_material) > len(returned.admitted_material)
    assert returned.source_material == exact.source_material
    assert returned.invocation_result_references[0].coordinates[-2] == (
        b"provider material"
    )
    wrong = admission_occurrence(
        (returned.source_material,),
        boundary_identity="wrong-return-admission",
        source_material=returned.source_material,
    )
    with pytest.raises(ValueError, match="differs from its invocation results"):
        replace(returned, admission_occurrence=wrong)


def test_one_byte_material_crosses_the_return_code_boundary(material_invocations):
    _, _, occurrences = material_invocations

    assert any(
        first.returncode != second.returncode
        for position, first in enumerate(occurrences)
        for second in occurrences[position + 1 :]
    )


def test_each_returned_material_enters_a_fresh_locality(material_invocations):
    ledger, _, occurrences = material_invocations
    events = tuple(
        ingest_material(
            ledger,
            locality_identity=f"compiled-material-result-{position}",
            exact_bytes=occurrence.stdout_bytes,
            source_role="fixture material",
            source_boundary=f"fixture-result-{position}",
        )
        for position, occurrence in enumerate(occurrences)
    )
    references = tuple(
        ingest_result_reference(ledger, event.identity) for event in events
    )

    assert len({event.locality_identity for event in events}) == len(events)
    assert tuple(reference.exact_material for reference in references) == tuple(
        occurrence.stdout_bytes for occurrence in occurrences
    )
    assert len({reference.exact_material for reference in references}) < len(
        references
    )
    assert len({reference.result_identity for reference in references}) == len(
        references
    )


def test_each_ordered_material_pair_has_one_exact_addition_occurrence(
    material_pair_invocations,
):
    _, references, admission, additions, _, _ = material_pair_invocations
    admitted_positions = {
        addition.admitted_material_position for addition in additions
    }
    assert len(admitted_positions) == 1
    bounded_material = admission.admitted_material[admitted_positions.pop()]
    exact_pairs = tuple(
        (source, position, added)
        for source in bounded_material
        for position in range(len(source.exact_material) + 1)
        for added in bounded_material
    )

    assert 1 < len(bounded_material) < len(references)
    assert len(additions) == len(bounded_material) ** 2 * 2
    assert tuple(addition.source_reference for addition in additions) == tuple(
        source for source, _, _ in exact_pairs
    )
    assert tuple(addition.added_reference for addition in additions) == tuple(
        added for _, _, added in exact_pairs
    )
    assert tuple(addition.position for addition in additions) == tuple(
        position for _, position, _ in exact_pairs
    )
    assert tuple(addition.result_material for addition in additions) == tuple(
        source.exact_material[:position]
        + added.exact_material
        + source.exact_material[position:]
        for source, position, added in exact_pairs
    )
    assert all(
        addition.admission_result_reference == admission.result_reference
        for addition in additions
    )
    assert all(
        addition.admitted_material_act_occurrence_count_limit
        == len(references) ** 2
        for addition in additions
    )
    assert len({addition.act_occurrence_identity for addition in additions}) == len(
        additions
    )
    assert len({addition.result_identity for addition in additions}) == len(additions)


def test_act_occurrence_limit_never_splits_admitted_material(
    material_pair_invocations,
):
    _, references, admission, additions, _, _ = material_pair_invocations
    limit = len(references) ** 2

    for admitted_position, admitted_material in enumerate(
        admission.admitted_material
    ):
        expected_count = sum(
            (len(source.exact_material) + 1) * len(admitted_material)
            for source in admitted_material
        )
        found = tuple(
            addition
            for addition in additions
            if addition.admitted_material_position == admitted_position
        )
        if expected_count <= limit:
            assert len(found) == expected_count
        else:
            assert found == ()


def test_addition_cannot_cross_its_exact_admitted_material(
    material_pair_invocations,
):
    _, references, _, additions, _, _ = material_pair_invocations
    addition = additions[0]
    other = next(
        reference
        for reference in references
        if reference
        not in addition.admission_result_reference.admitted_material[
            addition.admitted_material_position
        ]
    )

    with pytest.raises(ValueError, match="differs from its Admission"):
        replace(
            addition,
            added_reference=other,
            result_material=(
                addition.source_material[: addition.position]
                + other.exact_material
                + addition.source_material[addition.position :]
            ),
        )


def test_each_added_result_reaches_the_same_compiled_function(
    material_pair_invocations,
):
    _, _, _, additions, occurrences, _ = material_pair_invocations

    assert len(occurrences) == len(additions)
    assert tuple(occurrence.source_reference for occurrence in occurrences) == tuple(
        addition.result_reference for addition in additions
    )
    assert tuple(occurrence.exact_material for occurrence in occurrences) == tuple(
        addition.result_material for addition in additions
    )
    assert len({occurrence.occurrence_identity for occurrence in occurrences}) == len(
        occurrences
    )


def test_exact_addition_occurrence_binds_source_and_result_invocations(
    material_pair_invocations,
):
    _, _, _, additions, result_occurrences, comparisons = material_pair_invocations

    assert len(comparisons) == len(additions) == len(result_occurrences)
    assert tuple(
        comparison.added_position_act_occurrence_identity
        for comparison in comparisons
    ) == tuple(addition.act_occurrence_identity for addition in additions)
    assert tuple(
        comparison.result_invocation.occurrence_identity
        for comparison in comparisons
    ) == tuple(occurrence.occurrence_identity for occurrence in result_occurrences)
    assert any(comparison.distinction for comparison in comparisons)
    assert any(not comparison.distinction for comparison in comparisons)


def test_added_result_coordinates_establish_more_than_one_admission(
    material_pair_invocations,
):
    _, _, _, additions, occurrences, _ = material_pair_invocations
    admission = admit_invocation_occurrences(
        occurrences,
        boundary_identity="one-byte-pair-compiled-material-admission",
    )

    assert admission.source_material == tuple(
        addition.result_reference for addition in additions
    )
    assert len(admission.admitted_material) > 1
