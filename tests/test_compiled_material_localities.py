from __future__ import annotations

from pathlib import Path
import sys

import pytest

from seed_runtime.byte_measurement import (
    assertions_of_recorded_byte_measurement,
    record_byte_count_layer,
)
from seed_runtime.events import EventLedger
from seed_runtime.material_ingest import ingest_material


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from compiled_format_invocation import (  # noqa: E402
    AddedPositionOccurrence,
    ExactMaterialReference,
)
from compiled_material_invocation import (  # noqa: E402
    MaterialImplementationFunction,
    admit_invocation_occurrences,
    compare_added_material_invocations,
    ingest_result_reference,
    reference_occurrences_across,
)


def _measured_material():
    ledger = EventLedger()
    ingest_material(
        ledger,
        locality_identity="one-byte-material",
        exact_bytes=bytes(range(256)),
        source_role="fixture material",
        source_boundary="fixture-0",
    )
    measurement = record_byte_count_layer(
        ledger,
        source_locality_identities=("one-byte-material",),
        recording_locality_identity="one-byte-measurement",
    )
    assertions = assertions_of_recorded_byte_measurement(ledger, measurement.identity)
    references = tuple(
        ExactMaterialReference(
            recorded_occurrence_identity=assertion.recorded_occurrence_identity,
            assertion_identity=assertion.assertion_identity,
            exact_material=bytes((assertion.representation,)),
        )
        for assertion in assertions or ()
        if assertion.result == "count" and assertion.representation is not None
    )
    return ledger, references


@pytest.fixture(scope="module")
def material_invocations():
    ledger, references = _measured_material()
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
    admission = admit_invocation_occurrences(
        source_occurrences,
        boundary_identity="one-byte-compiled-material-admission",
    )
    smallest_count = min(len(material) for material in admission.admitted_material)
    smallest_material = tuple(
        material
        for material in admission.admitted_material
        if len(material) == smallest_count
    )
    if len(smallest_material) != 1:
        raise ValueError("one exact bounded Admission is required")
    bounded_material = smallest_material[0]
    additions = tuple(
        AddedPositionOccurrence(
            boundary_identity="one-byte-pair-addition",
            occurrence_position=position,
            source_reference=source,
            position=1,
            added_reference=added,
            result_material=source.exact_material + added.exact_material,
        )
        for position, (source, added) in enumerate(
            (source, added)
            for source in bounded_material
            for added in bounded_material
        )
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
        bounded_material,
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
    _, references, bounded_material, additions, _, _ = material_pair_invocations
    exact_pairs = tuple(
        (source, added)
        for source in bounded_material
        for added in bounded_material
    )

    assert 1 < len(bounded_material) < len(references)
    assert len(additions) == len(bounded_material) ** 2
    assert tuple(addition.source_reference for addition in additions) == tuple(
        source for source, _ in exact_pairs
    )
    assert tuple(addition.added_reference for addition in additions) == tuple(
        added for _, added in exact_pairs
    )
    assert tuple(addition.position for addition in additions) == (1,) * len(additions)
    assert tuple(addition.result_material for addition in additions) == tuple(
        source.exact_material + added.exact_material
        for source, added in exact_pairs
    )
    assert len({addition.act_occurrence_identity for addition in additions}) == len(
        additions
    )
    assert len({addition.result_identity for addition in additions}) == len(additions)


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
