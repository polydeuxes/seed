from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from compiled_stream_measurement_harness import (  # noqa: E402
    implementation_functions,
    measured_material,
)
from compiled_material_measurement_harness import measure  # noqa: E402


def test_each_stream_function_preserves_one_exact_invocation_occurrence():
    _, references = measured_material()
    functions = implementation_functions()

    assert len({function.identity for function in functions}) == len(functions) == 4
    assert all(
        function.invocation[
            function.invocation.index("-protocol_whitelist") + 1
        ]
        == "pipe,data"
        for function in functions
    )
    for function in functions:
        occurrences, exact, returned = measure(
            function,
            references[:1],
            time_limit_second_count=5.0,
            max_workers=1,
        )
        assert len(occurrences) == 1
        assert len(occurrences[0].exact_material) == 2
        assert occurrences[0].source_reference == references[0]
        assert exact.source_material == returned.source_material == references[:1]
