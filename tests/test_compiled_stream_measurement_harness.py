from __future__ import annotations

from pathlib import Path
import sys

import pytest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from compiled_stream_measurement_harness import (  # noqa: E402
    implementation_functions,
    measured_material,
)
from compiled_material_invocation import (  # noqa: E402
    admit_invocation_rows,
    compare_added_material_invocations,
)
from compiled_material_measurement_harness import (  # noqa: E402
    measure_added_material,
    measure_functions,
)


def test_stream_functions_admit_the_same_exact_material_together():
    _, references, byte_references = measured_material()
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
        boundary_identity="compiled-stream",
        time_limit_second_count=5.0,
        max_workers=8,
        material_byte_count_limit=65536,
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

    additions, source_rows, result_rows, comparisons = measure_added_material(
        functions,
        references[:4],
        byte_references[:4],
        boundary_identity="compiled-stream-material",
        time_limit_second_count=5.0,
        max_workers=8,
        material_byte_count_limit=65536,
        act_occurrence_count_limit=256,
    )

    assert additions
    assert len(source_rows) == len(result_rows) == len(comparisons) == len(functions)
    assert all(len(row) == len(additions) for row in result_rows)
    assert all(len(row) == len(additions) for row in comparisons)
    assert all(
        comparison.addition_occurrence.act_occurrence_identity
        == addition.act_occurrence_identity
        for row in comparisons
        for comparison, addition in zip(row, additions)
    )
    assert any(
        comparison.source_coordinates != comparison.result_coordinates
        for row in comparisons
        for comparison in row
    )
    with pytest.raises(ValueError, match="each exact source and result"):
        compare_added_material_invocations(
            additions,
            source_rows,
            tuple(row[:-1] for row in result_rows),
            boundary_identity="missing-stream-addition-result",
        )
