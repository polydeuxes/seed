from __future__ import annotations

from pathlib import Path
import shutil
import sys

import pytest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from compiled_codex_rendering_harness import (  # noqa: E402
    implementation_functions,
    rendering_material,
)
from compiled_material_invocation import occurrences_across  # noqa: E402


@pytest.mark.skipif(shutil.which("codex") is None, reason="Codex CLI is unavailable")
def test_codex_renderers_preserve_exact_keystroke_material_without_enter():
    material = rendering_material()
    functions = implementation_functions()
    occurrences = occurrences_across(
        material,
        boundary_identity="compiled-codex-rendering",
        implementation_functions=functions,
        time_limit_second_count=2.0,
        material_byte_count_limit=65536,
    )

    assert len(occurrences) == len(functions) == 3
    assert all(b"\n" not in found and b"\r" not in found for found in material)
    assert all(found.endswith(b"\x03") for found in material)
    assert all(
        tuple(occurrence.exact_material for occurrence in row) == material
        for row in occurrences
    )
    assert all(
        occurrence.stdout_bytes is None or type(occurrence.stdout_bytes) is bytes
        for row in occurrences
        for occurrence in row
    )
    assert all(
        occurrence.stderr_bytes is None or type(occurrence.stderr_bytes) is bytes
        for row in occurrences
        for occurrence in row
    )
    assert all(
        type(occurrence.stdout_bytes) is bytes
        and len(occurrence.stdout_bytes) > 100
        and b"\x1b[" in occurrence.stdout_bytes
        for occurrence in occurrences[2]
    )
    assert len({occurrence.coordinates for occurrence in occurrences[2]}) > 1
