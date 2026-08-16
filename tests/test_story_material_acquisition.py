from __future__ import annotations

from dataclasses import replace
from pathlib import Path
import sys

import pytest

from seed_runtime.events import EventLedger
from seed_runtime.material_ingest import ingest_material
from seed_runtime.occurrence_position_measurement import (
    get_recorded_occurrence_position_measurement,
    measure_occurrence_position,
    record_occurrence_position_measurement_responsible_act_evidence,
    record_occurrence_position_measurement_result,
)


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from compiled_format_invocation import (  # noqa: E402
    COMPILED_IMPLEMENTATION_FUNCTIONS,
    admit_compiled_invocation_rows,
    compiled_reference_invocations,
)
from compiled_material_invocation import ingest_result_reference  # noqa: E402
from material_fixture_story import (  # noqa: E402
    STORY_MATERIAL_COUNT,
    supplied_story_material,
)


@pytest.fixture(scope="module")
def acquired_story_material():
    try:
        exact_material = supplied_story_material(ROOT)
    except FileNotFoundError as error:
        pytest.skip(str(error))
    ledger = EventLedger()
    ingests = tuple(
        ingest_material(
            ledger,
            locality_identity="supplied-story-material",
            exact_bytes=material,
            source_role="fixture material",
            source_boundary=f"fixture-{position}",
        )
        for position, material in enumerate(exact_material)
    )
    boundary = ledger.append_boundary()
    references = tuple(
        ingest_result_reference(ledger, occurrence.identity)
        for occurrence in ingests
    )
    invocation_rows = compiled_reference_invocations(
        references,
        boundary_identity="supplied-story-material-invocation",
        implementation_functions=COMPILED_IMPLEMENTATION_FUNCTIONS,
    )
    admission = admit_compiled_invocation_rows(
        invocation_rows,
        boundary_identity="supplied-story-material-admission",
    )
    positions = measure_occurrence_position(
        ledger,
        source_locality_identity="supplied-story-material",
        through=boundary,
    )
    position_act_evidence = (
        record_occurrence_position_measurement_responsible_act_evidence(
            ledger,
            recording_locality_identity="supplied-story-material",
            finding=positions,
        )
    )
    position_result = record_occurrence_position_measurement_result(
        ledger,
        finding=positions,
        responsible_act_evidence_event_identity=position_act_evidence.identity,
    )
    return (
        exact_material,
        ledger,
        ingests,
        boundary,
        references,
        invocation_rows,
        admission,
        positions,
        position_result,
    )


def test_each_story_material_has_one_exact_ordered_ingest_occurrence(
    acquired_story_material,
):
    exact_material, ledger, ingests, boundary, references, _, _, _, _ = (
        acquired_story_material
    )

    assert len(exact_material) == len(ingests) == len(references) == (
        STORY_MATERIAL_COUNT
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
            tuple(occurrence.identity for occurrence in ingests),
            locality_identity="supplied-story-material",
        )
    ) == ingests
    assert tuple(ledger.list(through=boundary))[-1] == ingests[-1]


def test_each_compiled_function_receives_the_same_story_occurrence_order(
    acquired_story_material,
):
    _, _, _, _, references, invocation_rows, admission, _, _ = (
        acquired_story_material
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
    acquired_story_material,
):
    _, ledger, ingests, _, _, invocation_rows, _, positions, recorded = (
        acquired_story_material
    )

    positions_by_identity = dict(positions.occurrences)
    ingest_positions = tuple(
        positions_by_identity[ingest.identity]
        for ingest in ingests
    )
    assert ingest_positions == tuple(sorted(ingest_positions))
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
        == ingest_positions
        for row in invocation_rows
    )


def test_story_occurrence_order_refuses_one_reordered_compiled_function(
    acquired_story_material,
):
    invocation_rows = acquired_story_material[5]
    reordered = (
        invocation_rows[0][1],
        invocation_rows[0][0],
        *invocation_rows[0][2:],
    )

    with pytest.raises(ValueError, match="same exact material"):
        admit_compiled_invocation_rows(
            (reordered, *invocation_rows[1:]),
            boundary_identity="reordered-story-material-admission",
        )


def test_story_admission_refuses_one_changed_invocation_result(
    acquired_story_material,
):
    invocation_rows = acquired_story_material[5]
    admission = acquired_story_material[6]
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
