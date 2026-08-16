from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from compiled_bash_measurement_harness import (  # noqa: E402
    implementation_functions,
    measured_bash_material,
)
from compiled_material_measurement_harness import (  # noqa: E402
    measure_added_material,
    measure_functions,
)


def test_bash_syntax_and_dungeon_receive_the_same_exact_material():
    _, pair_references, byte_references = measured_bash_material()
    functions = implementation_functions()

    occurrences, admission = measure_functions(
        functions,
        pair_references[:4],
        boundary_identity="compiled-bash",
        time_limit_second_count=2.0,
        max_workers=4,
        material_byte_count_limit=65536,
    )

    assert len(occurrences) == len(functions) == 2
    assert tuple(
        tuple(occurrence.source_reference for occurrence in row)
        for row in occurrences
    ) == (pair_references[:4], pair_references[:4])
    assert admission.source_material == pair_references[:4]
    assert "--unshare-all" in functions[1].invocation
    assert "--ro-bind" in functions[1].invocation
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

    additions, source_rows, result_rows, comparisons = measure_added_material(
        functions,
        pair_references[:4],
        byte_references[:4],
        boundary_identity="compiled-bash-material",
        time_limit_second_count=2.0,
        max_workers=4,
        material_byte_count_limit=65536,
        act_occurrence_count_limit=256,
    )

    assert additions
    assert len(source_rows) == len(result_rows) == len(comparisons) == 2
    assert all(len(row) == len(additions) for row in result_rows)
    assert all(len(row) == len(additions) for row in comparisons)
    assert all(
        comparison.addition_occurrence.act_occurrence_identity
        == addition.act_occurrence_identity
        for row in comparisons
        for comparison, addition in zip(row, additions)
    )
