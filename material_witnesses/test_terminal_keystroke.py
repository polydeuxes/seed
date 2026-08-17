"""Interrogate one opaque PTY/readline boundary with exact material.

This is the `dfcfcac0` experiment restored outside Seed Fidelity.  The fixed
subprocess is an operator-owned material witness.  Its result is not a Seed
Measurement or Admission occurrence.
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


EXACT_MATERIAL = (
    b"printf 012x\x7f3\rexit\r",
    b"printf 0123\rexit\r",
)
IMPLEMENTATION_FUNCTION = MaterialImplementationFunction(
    identity="material-witness-pty-readline-0",
    invocation=(
        "/usr/bin/env",
        "-i",
        "TERM=dumb",
        "HOME=/tmp",
        "PS1=",
        "PS2=",
        "/usr/bin/script",
        "-qefc",
        "/bin/bash --noprofile --norc -i",
        "/dev/null",
    ),
)


@pytest.fixture(scope="module")
def terminal_witness_observation():
    required = tuple(
        Path(path) for path in ("/usr/bin/env", "/usr/bin/script", "/bin/bash")
    )
    if any(not path.is_file() for path in required):
        pytest.skip("opaque PTY implementation function is unavailable")

    ledger = EventLedger()
    ingests = tuple(
        ingest_material(
            ledger,
            locality_identity="terminal-material-witness-source",
            exact_bytes=material,
            source_role="operator supplied material",
            source_boundary=f"terminal-material-witness-source-{position}",
        )
        for position, material in enumerate(EXACT_MATERIAL)
    )
    references = tuple(
        ingest_result_reference(ledger, occurrence.identity) for occurrence in ingests
    )
    invocations = reference_occurrences_across(
        references,
        boundary_identity="terminal-material-witness-invocation",
        implementation_functions=(IMPLEMENTATION_FUNCTION,),
        max_workers=1,
        time_limit_second_count=2.0,
        material_byte_count_limit=65536,
    )[0]
    return ledger, ingests, references, invocations


def test_exact_material_reaches_the_external_function_unchanged(
    terminal_witness_observation,
):
    _, ingests, references, invocations = terminal_witness_observation

    assert tuple(occurrence.exact_material for occurrence in ingests) == EXACT_MATERIAL
    assert tuple(reference.exact_material for reference in references) == EXACT_MATERIAL
    assert tuple(occurrence.exact_material for occurrence in invocations) == EXACT_MATERIAL
    assert tuple(occurrence.source_reference for occurrence in invocations) == references


def test_the_external_result_preserves_every_bounded_process_coordinate(
    terminal_witness_observation,
):
    _, _, _, invocations = terminal_witness_observation

    for occurrence in invocations:
        assert occurrence.result_reference.coordinates == occurrence.coordinates
        assert occurrence.stdout_bytes is None or type(occurrence.stdout_bytes) is bytes
        assert occurrence.stderr_bytes is None or type(occurrence.stderr_bytes) is bytes


def test_one_exact_del_byte_changes_the_external_result(
    terminal_witness_observation,
):
    _, _, references, invocations = terminal_witness_observation

    assert EXACT_MATERIAL[0] == b"printf 012x" + bytes((127,)) + b"3\rexit\r"
    assert invocations[0].return_coordinates == invocations[1].return_coordinates
    assert invocations[0].stdout_bytes != invocations[1].stdout_bytes
    assert invocations[0].coordinates != invocations[1].coordinates
    assert references[0].result_identity != references[1].result_identity
