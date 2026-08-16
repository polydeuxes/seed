from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from book_material_measurement import measured_book_material  # noqa: E402
from compiled_bash_measurement_harness import implementation_functions  # noqa: E402
from compiled_material_measurement_harness import (  # noqa: E402
    measure_added_material,
    measure_functions,
)
from compiled_material_invocation import (  # noqa: E402
    first_recurring_added_return_compare_across,
)


def test_bash_syntax_and_dungeon_receive_the_same_exact_material():
    _, pair_references, byte_references = measured_book_material()
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

    earlier, coordinates, later = first_recurring_added_return_compare_across(
        additions,
        source_rows,
        boundary_identity="compiled-bash-distinct-function-recurrence",
        act_occurrence_count_limit=len(additions),
    )

    assert coordinates is not None
    assert len(coordinates) == len(functions)
    assert later is not None
    assert tuple(comparison.result_coordinates for comparison in later) == coordinates
    assert len(
        {
            comparison.addition_occurrence.act_occurrence_identity
            for comparison in later
        }
    ) == 1
    assert all(
        comparison.addition_occurrence.act_occurrence_identity
        != later[0].addition_occurrence.act_occurrence_identity
        for row in earlier
        for comparison in row
    )
