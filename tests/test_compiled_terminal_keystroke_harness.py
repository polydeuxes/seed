from __future__ import annotations

from pathlib import Path
import sys

import pytest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from compiled_terminal_keystroke_harness import (  # noqa: E402
    PTY_READLINE_IMPLEMENTATION_FUNCTION,
    acquire_terminal_material,
)


EXACT_TERMINAL_MATERIAL = (
    b"printf 012x\x7f3\rexit\r",
    b"printf 0123\rexit\r",
)


@pytest.fixture(scope="module")
def acquired_terminal_material():
    required = tuple(
        Path(path)
        for path in ("/usr/bin/env", "/usr/bin/script", "/bin/bash")
    )
    if any(not path.is_file() for path in required):
        pytest.skip("opaque PTY implementation function is unavailable")
    return acquire_terminal_material(
        EXACT_TERMINAL_MATERIAL,
        boundary_identity="terminal-material-test",
        material_occurrence_count_limit=len(EXACT_TERMINAL_MATERIAL),
        time_limit_second_count=2.0,
        output_material_byte_count_limit=65536,
    )


def test_exact_source_occurrences_reach_the_opaque_pty_function_unchanged(
    acquired_terminal_material,
):
    acquisition = acquired_terminal_material

    assert tuple(
        occurrence.exact_material
        for occurrence in acquisition.ingest_occurrences
    ) == EXACT_TERMINAL_MATERIAL
    assert tuple(
        reference.exact_material for reference in acquisition.source_references
    ) == EXACT_TERMINAL_MATERIAL
    assert tuple(
        occurrence.exact_material
        for occurrence in acquisition.invocation_occurrences
    ) == EXACT_TERMINAL_MATERIAL
    assert tuple(
        occurrence.source_reference
        for occurrence in acquisition.invocation_occurrences
    ) == acquisition.source_references
    assert EXACT_TERMINAL_MATERIAL[0] == (
        b"printf 012x" + bytes((127,)) + b"3\rexit\r"
    )
    assert acquisition.implementation_function == (
        PTY_READLINE_IMPLEMENTATION_FUNCTION
    )


def test_each_raw_result_has_its_exact_source_and_act_occurrence_lineage(
    acquired_terminal_material,
):
    acquisition = acquired_terminal_material

    for ingest, source, occurrence in zip(
        acquisition.ingest_occurrences,
        acquisition.source_references,
        acquisition.invocation_occurrences,
    ):
        result = occurrence.result_reference
        assert source.recorded_occurrence_identity == ingest.identity
        assert source.act_occurrence_identity == ingest.material[
            "act_occurrence_identity"
        ]
        assert source.result_identity == ingest.material["result_identity"]
        assert occurrence.source_reference is source
        assert result.invocation_occurrence is occurrence
        assert result.act_occurrence_identity == occurrence.occurrence_identity
        assert result.result_identity == occurrence.result_identity
        assert result.coordinates == occurrence.coordinates


def test_every_raw_process_coordinate_is_retained_without_decoding(
    acquired_terminal_material,
):
    for occurrence in acquired_terminal_material.invocation_occurrences:
        (
            time_limit,
            output_limit,
            returned,
            time_limit_reached,
            stdout_limit_reached,
            stderr_limit_reached,
            returncode,
            stdout,
            stderr,
        ) = occurrence.result_reference.coordinates

        assert time_limit == occurrence.time_limit_second_count
        assert output_limit == occurrence.material_byte_count_limit
        assert returned is occurrence.returned
        assert time_limit_reached is occurrence.time_limit_reached
        assert stdout_limit_reached is occurrence.stdout_byte_count_limit_reached
        assert stderr_limit_reached is occurrence.stderr_byte_count_limit_reached
        assert returncode == occurrence.returncode
        assert stdout == occurrence.stdout_bytes
        assert stderr == occurrence.stderr_bytes
        assert stdout is None or type(stdout) is bytes
        assert stderr is None or type(stderr) is bytes


def test_raw_coordinates_produce_an_observed_admission_distinction(
    acquired_terminal_material,
):
    acquisition = acquired_terminal_material
    admission = acquisition.admission_occurrence
    occurrences = acquisition.invocation_occurrences

    assert occurrences[0].return_coordinates == occurrences[1].return_coordinates
    assert occurrences[0].stdout_bytes != occurrences[1].stdout_bytes
    assert occurrences[0].coordinates != occurrences[1].coordinates
    assert admission.source_material == acquisition.source_references
    assert admission.invocation_result_references == tuple(
        occurrence.result_reference for occurrence in occurrences
    )
    assert len(admission.admitted_material) == 2
    assert {
        reference.result_identity
        for same_coordinates in admission.admitted_material
        for reference in same_coordinates
    } == {
        reference.result_identity for reference in acquisition.source_references
    }


def test_terminal_material_acquisition_refuses_an_unbounded_source_count():
    with pytest.raises(ValueError, match="occurrence count limit"):
        acquire_terminal_material(
            EXACT_TERMINAL_MATERIAL,
            boundary_identity="terminal-material-over-limit",
            material_occurrence_count_limit=1,
            time_limit_second_count=2.0,
            output_material_byte_count_limit=65536,
        )
