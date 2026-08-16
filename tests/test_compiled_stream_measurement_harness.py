from __future__ import annotations

from pathlib import Path
import sys

import pytest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from compiled_stream_measurement_harness import (  # noqa: E402
    implementation_functions,
    measure_functions,
    measured_material,
)
from compiled_material_invocation import admit_invocation_rows  # noqa: E402


def test_stream_functions_admit_the_same_exact_material_together():
    _, references = measured_material()
    functions = implementation_functions()

    assert len({function.identity for function in functions}) == len(functions) == 5
    assert all(
        function.invocation[
            function.invocation.index("-protocol_whitelist") + 1
        ]
        == "pipe,data"
        for function in functions[:4]
    )
    occurrences, admission = measure_functions(
        functions,
        references[:4],
        time_limit_second_count=5.0,
        max_workers=8,
    )

    assert len(occurrences) == len(functions)
    assert all(
        tuple(occurrence.source_reference for occurrence in row) == references[:4]
        for row in occurrences
    )
    assert all(
        tuple(occurrence.exact_material for occurrence in row)
        == tuple(reference.exact_material for reference in references[:4])
        for row in occurrences
    )
    assert admission.source_material == references[:4]
    assert len(admission.invocation_result_references) == len(functions) * 4

    with pytest.raises(ValueError, match="one exact function"):
        admit_invocation_rows(
            (occurrences[0], occurrences[0]),
            boundary_identity="duplicate-stream-function",
        )
    with pytest.raises(ValueError, match="same exact material"):
        admit_invocation_rows(
            (occurrences[0], tuple(reversed(occurrences[1]))),
            boundary_identity="reordered-stream-material",
        )
