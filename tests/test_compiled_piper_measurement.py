from __future__ import annotations

from dataclasses import replace
from pathlib import Path
import sys

import pytest

from seed_runtime.events import EventLedger
from seed_runtime.byte_measurement import record_byte_count_layer
from seed_runtime.material_ingest import ingest_material


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from compiled_material_invocation import (  # noqa: E402
    MaterialAdmissionOccurrence,
)
from compiled_format_invocation import (  # noqa: E402
    admission_removed_position_occurrences,
    exact_byte_material_references,
)
from compiled_piper_measurement import (  # noqa: E402
    piper_implementation_function,
    piper_material_occurrences,
)
from material_fixture_books import (  # noqa: E402
    MATERIAL_WINDOWS,
    supplied_material,
)


COMPILED_EXECUTABLE = ROOT / ".venv" / "bin" / "piper"
COMPILED_MATERIAL = (
    Path.home() / ".local" / "share" / "piper-voices" / "en_US-lessac-medium.onnx"
)


@pytest.fixture(scope="module")
def supplied_piper_material():
    if not COMPILED_EXECUTABLE.is_file() or not COMPILED_MATERIAL.is_file():
        pytest.skip("compiled implementation function is unavailable")
    supplied_path = ROOT / "corpus" / MATERIAL_WINDOWS[0][0]
    if not supplied_path.is_file():
        pytest.skip("supplied fixture material is unavailable")
    exact_material = supplied_material(ROOT, *MATERIAL_WINDOWS[0])
    ledger = EventLedger()
    ingest = ingest_material(
        ledger,
        locality_identity="supplied-piper-material",
        exact_bytes=exact_material,
        source_role="fixture material",
        source_boundary="fixture-0",
    )
    measurement = record_byte_count_layer(
        ledger,
        source_localities=("supplied-piper-material",),
        recording_locality_identity="supplied-piper-byte-measurement",
    )
    references = exact_byte_material_references(ledger, measurement.identity)
    implementation_function = piper_implementation_function(
        COMPILED_EXECUTABLE,
        COMPILED_MATERIAL,
        identity="compiled-0",
    )
    occurrences, admission = piper_material_occurrences(
        references,
        implementation_function,
        boundary_identity="supplied-piper-material",
        time_limit_second_count=12.0,
        material_byte_count_limit=65536,
        max_workers=2,
    )
    return (
        exact_material,
        ingest,
        measurement,
        references,
        implementation_function,
        occurrences,
        admission,
    )


def test_each_measured_material_from_one_supplied_work_reaches_piper(
    supplied_piper_material,
):
    (
        exact_material,
        ingest,
        measurement,
        references,
        implementation_function,
        occurrences,
        _,
    ) = (
        supplied_piper_material
    )

    assert ingest.exact_material == exact_material
    assert {reference.recorded_occurrence_identity for reference in references} == {
        measurement.identity
    }
    assert tuple(reference.exact_material for reference in references) == tuple(
        bytes((value,)) for value in sorted(set(exact_material))
    )
    assert len(references) == len(occurrences)
    assert tuple(occurrence.source_reference for occurrence in occurrences) == references
    assert tuple(occurrence.exact_material for occurrence in occurrences) == tuple(
        reference.exact_material for reference in references
    )
    assert all(
        occurrence.implementation_function == implementation_function
        for occurrence in occurrences
    )
    assert len({occurrence.occurrence_identity for occurrence in occurrences}) == len(
        occurrences
    )
    assert len({occurrence.result_identity for occurrence in occurrences}) == len(
        occurrences
    )


def test_piper_preserves_every_exact_raw_result_coordinate(supplied_piper_material):
    occurrences = supplied_piper_material[5]

    assert all(occurrence.stdout_bytes is not None for occurrence in occurrences)
    assert all(occurrence.stderr_bytes is not None for occurrence in occurrences)
    assert any(occurrence.stdout_bytes for occurrence in occurrences)
    assert all(
        occurrence.returned
        or occurrence.time_limit_reached
        or occurrence.stdout_byte_count_limit_reached
        or occurrence.stderr_byte_count_limit_reached
        for occurrence in occurrences
    )
    assert all(
        occurrence.result_reference.coordinates == occurrence.coordinates
        for occurrence in occurrences
    )


def test_piper_admission_keeps_every_invocation_result(supplied_piper_material):
    references = supplied_piper_material[3]
    occurrences = supplied_piper_material[5]
    admission = supplied_piper_material[6]

    assert admission.source_material == references
    assert admission.invocation_result_references == tuple(
        occurrence.result_reference for occurrence in occurrences
    )
    assert {
        material
        for same_coordinates in admission.admitted_material
        for material in same_coordinates
    } == set(references)
    assert len(admission.admitted_material) > 1
    assert any(
        len(same_coordinates) > 1
        for same_coordinates in admission.admitted_material
    )


def test_piper_admission_refuses_different_invocation_coordinates(
    supplied_piper_material,
):
    occurrences = supplied_piper_material[5]
    admission = supplied_piper_material[6]
    changed = replace(
        occurrences[0],
        stdout_bytes=occurrences[0].stdout_bytes + b"\x00",
    )

    with pytest.raises(ValueError, match="differs from its invocation results"):
        MaterialAdmissionOccurrence(
            admission_occurrence=admission.admission_occurrence,
            invocation_result_references=(
                changed.result_reference,
                *admission.invocation_result_references[1:],
            ),
        )


def test_full_piper_admission_drives_whole_exact_removal_tuples(
    supplied_piper_material,
):
    references = supplied_piper_material[3]
    admission = supplied_piper_material[6]
    act_occurrence_count_limit = min(
        len(reference.exact_material) for reference in references
    )

    removals = admission_removed_position_occurrences(
        admission.result_reference,
        boundary_identity="supplied-piper-material-removal",
        admitted_material_act_occurrence_count_limit=(
            act_occurrence_count_limit
        ),
    )
    eligible_admitted_material = tuple(
        admitted
        for admitted in admission.admitted_material
        if sum(len(reference.exact_material) for reference in admitted)
        <= act_occurrence_count_limit
    )
    eligible_references = tuple(
        reference
        for admitted in eligible_admitted_material
        for reference in admitted
    )

    assert eligible_references
    assert len(removals) == sum(
        len(reference.exact_material) for reference in eligible_references
    )
    assert {removal.source_reference for removal in removals} == set(
        eligible_references
    )
    assert all(
        removal.source_admission_result_reference == admission.result_reference
        and removal.source_reference
        == admission.admitted_material[
            removal.source_admitted_material_position
        ][removal.source_admitted_reference_position]
        and removal.result_reference.source_admission_result_reference
        == admission.result_reference
        and removal.result_reference.source_admitted_material_position
        == removal.source_admitted_material_position
        and removal.result_reference.source_admitted_reference_position
        == removal.source_admitted_reference_position
        for removal in removals
    )
    assert all(
        tuple(
            removal.position
            for removal in removals
            if removal.source_reference == reference
        )
        == tuple(range(len(reference.exact_material)))
        for reference in eligible_references
    )
