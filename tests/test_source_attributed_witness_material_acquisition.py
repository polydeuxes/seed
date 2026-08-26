from __future__ import annotations

from dataclasses import replace
from pathlib import Path
import sys

import pytest

from seed_runtime.events import EventLedger
from seed_runtime.witness_material_source import record_witness_material_source
from seed_runtime.occurrence_position_measurement import (
    get_recorded_occurrence_position_measurement,
    measure_occurrence_position,
    record_occurrence_position_measurement_responsibility_assignment,
    record_occurrence_position_measurement_act_occurrence,
    record_occurrence_position_measurement_result,
)
from seed_runtime.operator_current_coordinates import read_operator_current_coordinates


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from compiled_format_invocation import (  # noqa: E402
    COMPILED_IMPLEMENTATION_FUNCTIONS,
    admit_compiled_invocation_rows,
    compiled_reference_invocations,
)
from compiled_material_invocation import material_acquisition_result_reference  # noqa: E402
from source_attributed_witness_material import (  # noqa: E402
    SOURCE_ATTRIBUTED_WITNESS_MATERIAL_COUNT,
    supplied_source_attributed_witness_material,
)


@pytest.fixture(scope="module")
def acquired_source_attributed_witness_material():
    try:
        exact_material = supplied_source_attributed_witness_material(ROOT)
    except FileNotFoundError as error:
        pytest.skip(str(error))
    ledger = EventLedger()
    acquisition_results = tuple(
        record_witness_material_source(
            ledger,
            locality_identity="source-attributed-witness-material",
            exact_bytes=material,
            source_boundary=f"source-attributed Witness Material occurrence {position}",
        )
        for position, material in enumerate(exact_material)
    )
    boundary = ledger.append_boundary()
    references = tuple(
        material_acquisition_result_reference(ledger, occurrence.identity)
        for occurrence in acquisition_results
    )
    invocation_rows = compiled_reference_invocations(
        references,
        boundary_identity="source-attributed-witness-material-invocation",
        implementation_functions=COMPILED_IMPLEMENTATION_FUNCTIONS,
    )
    admission = admit_compiled_invocation_rows(
        invocation_rows,
        boundary_identity="source-attributed-witness-material-admission",
    )
    positions = measure_occurrence_position(
        ledger,
        source_locality_identity="source-attributed-witness-material",
        through=boundary,
    )
    position_assignment = (
        record_occurrence_position_measurement_responsibility_assignment(
            ledger,
            recording_locality_identity="source-attributed-witness-material",
            finding=positions,
            locality_standing=read_operator_current_coordinates(
                ledger, locality_identity="source-attributed-witness-material"
            ),
        )
    )
    position_act_occurrence = (
        record_occurrence_position_measurement_act_occurrence(
            ledger,
            responsibility_assignment_event_identity=position_assignment.identity,
            responsibility_assignment_standing=read_operator_current_coordinates(
                ledger, locality_identity="source-attributed-witness-material"
            ),
        )
    )
    position_result = record_occurrence_position_measurement_result(
        ledger,
        act_occurrence_event_identity=position_act_occurrence.identity,
    )
    return (
        exact_material,
        ledger,
        acquisition_results,
        boundary,
        references,
        invocation_rows,
        admission,
        positions,
        position_result,
    )


def test_each_source_attributed_witness_material_has_one_exact_ordered_material_acquisition_result_occurrence(
    acquired_source_attributed_witness_material,
):
    exact_material, ledger, acquisition_results, boundary, references, _, _, _, _ = (
        acquired_source_attributed_witness_material
    )

    assert len(exact_material) == len(acquisition_results) == len(references) == (
        SOURCE_ATTRIBUTED_WITNESS_MATERIAL_COUNT
    )
    assert tuple(reference.exact_material for reference in references) == exact_material
    assert len({reference.recorded_occurrence_identity for reference in references}) == len(
        references
    )
    assert len({reference.act_occurrence_identity for reference in references}) == len(
        references
    )
    assert len({reference.result_identity for reference in references}) == len(references)
    assert tuple(
        ledger.occurrences_in_append_order(
            tuple(occurrence.identity for occurrence in acquisition_results),
            locality_identity="source-attributed-witness-material",
        )
    ) == acquisition_results
    assert tuple(ledger.list(through=boundary))[-1] == acquisition_results[-1]


def test_each_compiled_function_receives_the_same_source_attributed_witness_occurrence_order(
    acquired_source_attributed_witness_material,
):
    _, _, _, _, references, invocation_rows, _, _, _ = (
        acquired_source_attributed_witness_material
    )

    assert len(invocation_rows) == len(COMPILED_IMPLEMENTATION_FUNCTIONS)
    assert all(
        tuple(occurrence.source_coordinate for occurrence in row) == references
        for row in invocation_rows
    )
    assert all(
        tuple(occurrence.invocation_position for occurrence in row)
        == tuple(range(len(references)))
        for row in invocation_rows
    )


def test_source_attributed_witness_invocation_results_enter_one_complete_admission(
    acquired_source_attributed_witness_material,
):
    _, _, _, _, references, invocation_rows, admission, _, _ = (
        acquired_source_attributed_witness_material
    )

    assert admission.source_material == references
    assert 1 < len(admission.admitted_material) < len(references)
    assert any(
        len(same_coordinates) > 1
        for same_coordinates in admission.admitted_material
    )
    assert admission.invocation_result_references == tuple(
        occurrence.result_reference
        for row in invocation_rows
        for occurrence in row
    )


def test_each_invocation_position_matches_the_measured_occurrence_position(
    acquired_source_attributed_witness_material,
):
    _, ledger, acquisition_results, _, _, invocation_rows, _, positions, recorded = (
        acquired_source_attributed_witness_material
    )

    positions_by_identity = dict(positions.occurrences)
    material_acquisition_positions = tuple(
        positions_by_identity[acquisition_result.identity]
        for acquisition_result in acquisition_results
    )
    assert material_acquisition_positions == tuple(sorted(material_acquisition_positions))
    assert get_recorded_occurrence_position_measurement(
        ledger,
        recorded.identity,
    ) == positions
    assert all(
        tuple(
            positions_by_identity[
                occurrence.source_coordinate.recorded_occurrence_identity
            ]
            for occurrence in row
        )
        == material_acquisition_positions
        for row in invocation_rows
    )


def test_source_attributed_witness_occurrence_order_refuses_one_reordered_compiled_function(
    acquired_source_attributed_witness_material,
):
    invocation_rows = acquired_source_attributed_witness_material[5]
    reordered = (
        invocation_rows[0][1],
        invocation_rows[0][0],
        *invocation_rows[0][2:],
    )

    with pytest.raises(ValueError, match="same exact material"):
        admit_compiled_invocation_rows(
            (reordered, *invocation_rows[1:]),
            boundary_identity="reordered-source-attributed-witness-material-admission",
        )


def test_source_attributed_witness_admission_refuses_one_changed_invocation_result(
    acquired_source_attributed_witness_material,
):
    invocation_rows = acquired_source_attributed_witness_material[5]
    admission = acquired_source_attributed_witness_material[6]
    changed = replace(
        invocation_rows[0][0],
        returned=not invocation_rows[0][0].returned,
    )

    with pytest.raises(ValueError, match="differs from its invocation results"):
        replace(
            admission,
            invocation_result_references=(
                changed.result_reference,
                *admission.invocation_result_references[1:],
            ),
        )
