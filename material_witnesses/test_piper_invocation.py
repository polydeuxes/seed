"""Interrogate one fixed voice implementation with exact prose material.

This is the bounded question introduced by `8f071e92`, restored without the
later script-local Admission vocabulary.  The external stdout remains opaque
bytes.  Sample format and audible presentation are not established here.
"""

from __future__ import annotations

from pathlib import Path
import sys

import pytest

from seed_runtime.events import EventLedger
from seed_runtime.material_ingest import ingest_material


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from compiled_material_invocation import (  # noqa: E402
    MaterialImplementationFunction,
    ingest_result_reference,
    reference_occurrences_across,
)


EXECUTABLE = ROOT / ".venv" / "bin" / "piper"
MODEL = Path.home() / ".local" / "share" / "piper-voices" / "en_US-lessac-medium.onnx"
EXACT_MATERIAL = (b"hello\n", b"goodbye\n")


@pytest.fixture(scope="module")
def piper_witness_observation():
    if not EXECUTABLE.is_file() or not MODEL.is_file():
        pytest.skip("the external voice implementation function is unavailable")

    ledger = EventLedger()
    ingests = tuple(
        ingest_material(
            ledger,
            locality_identity="piper-material-witness-source",
            exact_bytes=material,
            source_role="operator supplied material",
            source_boundary=f"piper-material-witness-source-{position}",
        )
        for position, material in enumerate(EXACT_MATERIAL)
    )
    references = tuple(
        ingest_result_reference(ledger, occurrence.identity) for occurrence in ingests
    )
    implementation_function = MaterialImplementationFunction(
        identity="material-witness-piper-voice-0",
        invocation=(str(EXECUTABLE), "-m", str(MODEL), "--output-raw"),
    )
    invocations = reference_occurrences_across(
        references,
        boundary_identity="piper-material-witness-invocation",
        implementation_functions=(implementation_function,),
        max_workers=1,
        time_limit_second_count=15.0,
        material_byte_count_limit=1048576,
    )[0]
    result_ingests = tuple(
        ingest_material(
            ledger,
            locality_identity="piper-material-witness-result",
            exact_bytes=occurrence.stdout_bytes or b"",
            source_role="system",
            source_boundary=f"external voice stdout occurrence {position}",
            provenance_occurrence_references=(ingests[position].identity,),
        )
        for position, occurrence in enumerate(invocations)
    )
    return (
        ledger,
        ingests,
        references,
        implementation_function,
        invocations,
        result_ingests,
    )


def test_exact_prose_reaches_the_external_voice_function_unchanged(
    piper_witness_observation,
):
    _, ingests, references, implementation_function, invocations, _ = (
        piper_witness_observation
    )

    assert tuple(occurrence.exact_material for occurrence in ingests) == EXACT_MATERIAL
    assert tuple(reference.exact_material for reference in references) == EXACT_MATERIAL
    assert tuple(occurrence.exact_material for occurrence in invocations) == EXACT_MATERIAL
    assert tuple(
        occurrence.input_boundary_accepted_byte_count
        for occurrence in invocations
    ) == tuple(len(material) for material in EXACT_MATERIAL)
    assert tuple(occurrence.source_reference for occurrence in invocations) == references
    assert all(
        occurrence.implementation_function == implementation_function
        for occurrence in invocations
    )


def test_external_voice_results_preserve_distinct_opaque_material(
    piper_witness_observation,
):
    _, _, _, _, invocations, _ = piper_witness_observation

    assert all(occurrence.returned for occurrence in invocations)
    assert all(type(occurrence.stdout_bytes) is bytes for occurrence in invocations)
    assert all(occurrence.stdout_bytes for occurrence in invocations)
    assert invocations[0].stdout_bytes != invocations[1].stdout_bytes
    assert all(
        occurrence.result_reference.coordinates == occurrence.coordinates
        for occurrence in invocations
    )


def test_external_voice_results_enter_seed_only_as_exact_provenanced_material(
    piper_witness_observation,
):
    _, source_ingests, _, _, invocations, result_ingests = piper_witness_observation

    assert tuple(occurrence.exact_material for occurrence in result_ingests) == tuple(
        invocation.stdout_bytes or b"" for invocation in invocations
    )
    assert tuple(
        occurrence.material["provenance_occurrence_references"]
        for occurrence in result_ingests
    ) == tuple([source.identity] for source in source_ingests)
