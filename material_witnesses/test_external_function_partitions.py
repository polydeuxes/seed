"""Recover the cross-function questions before their script Admission layer.

The Bash and media matrices began at `87d93140` and `27ad8129`.  These tests
retain the exact supplied material and bounded external results.  The observed
partitions remain material-witness observations.
"""

from __future__ import annotations

from pathlib import Path
import sys

import pytest

from seed_runtime.events import EventLedger
from seed_runtime.material_ingest import ingest_material

from material_witnesses.audio_ladder import occurrence_material


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from compiled_material_invocation import (  # noqa: E402
    MaterialImplementationFunction,
    ingest_result_reference,
    reference_occurrences_across,
)


def _source_references(exact_material: tuple[bytes, ...], *, boundary: str):
    ledger = EventLedger()
    ingests = tuple(
        ingest_material(
            ledger,
            locality_identity=f"{boundary}-source",
            exact_bytes=material,
            source_role="operator supplied material",
            source_boundary=f"{boundary}-source-{position}",
        )
        for position, material in enumerate(exact_material)
    )
    references = tuple(
        ingest_result_reference(ledger, occurrence.identity) for occurrence in ingests
    )
    return ledger, ingests, references


BASH_FUNCTIONS = (
    MaterialImplementationFunction(
        identity="material-witness-bash-syntax",
        invocation=(
            "/usr/bin/env",
            "-i",
            "/bin/bash",
            "--noprofile",
            "--norc",
            "-n",
        ),
    ),
    MaterialImplementationFunction(
        identity="material-witness-bash-bounded",
        invocation=(
            "/usr/bin/prlimit",
            "--cpu=1",
            "--as=268435456",
            "--nproc=32",
            "--nofile=64",
            "--",
            "/usr/bin/bwrap",
            "--unshare-all",
            "--die-with-parent",
            "--new-session",
            "--clearenv",
            "--ro-bind",
            "/usr",
            "/usr",
            "--symlink",
            "usr/bin",
            "/bin",
            "--symlink",
            "usr/lib",
            "/lib",
            "--symlink",
            "usr/lib64",
            "/lib64",
            "--proc",
            "/proc",
            "--dev",
            "/dev",
            "--tmpfs",
            "/tmp",
            "--dir",
            "/home",
            "--chdir",
            "/tmp",
            "/bin/bash",
            "--noprofile",
            "--norc",
        ),
    ),
)


def test_bash_functions_receive_the_same_exact_material_and_partition_it():
    exact_material = (b"printf hello\n", b"(\n")
    _, _, references = _source_references(
        exact_material, boundary="bash-material-witness"
    )
    rows = reference_occurrences_across(
        references,
        boundary_identity="bash-material-witness-invocation",
        implementation_functions=BASH_FUNCTIONS,
        max_workers=2,
        time_limit_second_count=2.0,
        material_byte_count_limit=65536,
    )

    assert len(rows) == len(BASH_FUNCTIONS)
    assert all(
        tuple(occurrence.source_reference for occurrence in row) == references
        for row in rows
    )
    assert all(
        tuple(occurrence.exact_material for occurrence in row) == exact_material
        for row in rows
    )
    assert any(
        rows[0][position].coordinates != rows[1][position].coordinates
        for position in range(len(references))
    )


MEDIA_FUNCTIONS = (
    MaterialImplementationFunction(
        identity="material-witness-media-probe",
        invocation=(
            "/usr/bin/ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=format_name",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            "pipe:0",
        ),
    ),
    MaterialImplementationFunction(
        identity="material-witness-media-file",
        invocation=("/usr/bin/file", "-b", "-"),
    ),
    MaterialImplementationFunction(
        identity="material-witness-media-pcm",
        invocation=(
            "/usr/bin/ffmpeg",
            "-nostdin",
            "-v",
            "error",
            "-f",
            "s16le",
            "-ar",
            "48000",
            "-ac",
            "1",
            "-i",
            "pipe:0",
            "-f",
            "null",
            "-",
        ),
    ),
    MaterialImplementationFunction(
        identity="material-witness-media-rgb",
        invocation=(
            "/usr/bin/ffmpeg",
            "-nostdin",
            "-v",
            "error",
            "-f",
            "rawvideo",
            "-pixel_format",
            "rgb24",
            "-video_size",
            "2x2",
            "-i",
            "pipe:0",
            "-frames:v",
            "1",
            "-f",
            "null",
            "-",
        ),
    ),
)


@pytest.mark.skipif(
    any(not Path(function.invocation[0]).is_file() for function in MEDIA_FUNCTIONS),
    reason="one external media implementation function is absent",
)
def test_media_functions_receive_the_same_material_and_form_distinct_partitions():
    exact_material = (
        occurrence_material(60.0),
        bytes((0, 0, 0, 255, 0, 0, 0, 255, 0, 0, 0, 255)),
    )
    _, _, references = _source_references(
        exact_material, boundary="media-material-witness"
    )
    rows = reference_occurrences_across(
        references,
        boundary_identity="media-material-witness-invocation",
        implementation_functions=MEDIA_FUNCTIONS,
        max_workers=4,
        time_limit_second_count=5.0,
        material_byte_count_limit=65536,
    )

    assert len(rows) == len(MEDIA_FUNCTIONS)
    assert all(
        tuple(occurrence.exact_material for occurrence in row) == exact_material
        for row in rows
    )
    columns = tuple(zip(*rows))
    assert all(len({occurrence.coordinates for occurrence in column}) > 1 for column in columns)
