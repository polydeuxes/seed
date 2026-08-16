from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from compiled_game_measurement_harness import implementation_functions  # noqa: E402
from compiled_format_invocation import (  # noqa: E402
    admission_added_position_occurrences,
)
from compiled_material_invocation import (  # noqa: E402
    compare_added_material_invocations,
)
from compiled_material_measurement_harness import measure  # noqa: E402
from material_fixture_measurement import measured_one_byte_material  # noqa: E402


def test_each_game_function_receives_every_exact_one_byte_material():
    _, references = measured_one_byte_material()
    found = []
    for function in implementation_functions():
        occurrences, exact, returned = measure(
            function,
            references,
            time_limit_second_count=5.0,
            max_workers=8,
        )
        assert tuple(occurrence.source_reference for occurrence in occurrences) == (
            references
        )
        assert exact.source_material == returned.source_material == references
        found.append(returned.admitted_material)

        additions = admission_added_position_occurrences(
            returned.result_reference,
            boundary_identity=f"{function.identity}-bounded-addition",
            admitted_material_act_occurrence_count_limit=len(references) ** 2,
        )
        result_occurrences, _, result_returned = measure(
            function,
            tuple(addition.result_reference for addition in additions),
            time_limit_second_count=5.0,
            max_workers=8,
        )
        comparisons = compare_added_material_invocations(
            additions,
            (occurrences,),
            (result_occurrences,),
            boundary_identity=f"{function.identity}-bounded-addition-compare",
        )[0]
        assert len(comparisons) == len(additions) == len(result_occurrences)
        assert result_returned.source_material == tuple(
            addition.result_reference for addition in additions
        )

    assert len(found) == 4
    assert all(len(admitted_material) > 1 for admitted_material in found)
