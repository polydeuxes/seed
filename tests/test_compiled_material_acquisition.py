from __future__ import annotations

from pathlib import Path
import sys

import pytest




ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from compiled_material_acquisition import (  # noqa: E402
    implementation_functions,
    measure_added_material,
    measure_material,
    measure_material_and_act_results,
    measure_material_time_counts,
)
from material_measurement_test_witness import measured_one_byte_material  # noqa: E402
from material_admission import admission_occurrence  # noqa: E402
from compiled_material_invocation import (  # noqa: E402
    MaterialImplementationFunction,
    first_recurring_added_return_compare,
)


def test_material_climb_refuses_the_collective_act_occurrence_count():
    _, references = measured_one_byte_material()
    first_material = references[:2]
    second_material = references[2:4]
    admissions = tuple(
        admission_occurrence(
            (material,),
            boundary_identity=f"count-admission-{position}",
            source_material=material,
        )
        for position, material in enumerate((first_material, second_material))
    )

    with pytest.raises(ValueError, match="exact count boundary"):
        measure_added_material(
            (),
            references[:4],
            (),
            admissions,
            time_boundary_second_count=0.01,
            act_occurrence_count_boundary=12,
        )


def test_each_compiled_function_preserves_every_one_byte_input_boundary():
    _, references = measured_one_byte_material()
    functions = implementation_functions()
    time_counts = (0.0078125, 0.03125, 0.25)
    measurements, exact_compares, return_compares = measure_material_time_counts(
        functions, references, time_counts
    )
    second_count, source_occurrences, _, _ = measurements[0]
    _, occurrences, exact, returned = measurements[-1]

    assert len(occurrences) == len(exact) == len(returned) == len(functions)
    assert tuple(measurement[0] for measurement in measurements) == time_counts
    assert len(
        {
            occurrence.occurrence_identity
            for _, found, _, _ in measurements
            for row in found
            for occurrence in row
        }
    ) == len(time_counts) * len(functions) * len(references)
    assert all(
        occurrence.time_boundary_second_count == second_count
        for second_count, found, _, _ in measurements
        for row in found
        for occurrence in row
    )
    assert all(
        occurrence.input_boundary_accepted_byte_count is not None
        and 0
        <= occurrence.input_boundary_accepted_byte_count
        <= len(occurrence.exact_material)
        for _, found, _, _ in measurements
        for row in found
        for occurrence in row
    )
    for position in range(len(functions)):
        assert tuple(
            occurrence.source_reference for occurrence in occurrences[position]
        ) == (
            references
        )
        assert (
            exact[position].source_material
            == returned[position].source_material
            == references
        )
    admission_count = len(time_counts) * len(functions)
    comparison_count = admission_count * (admission_count - 1)
    assert len(exact_compares) == len(return_compares) == comparison_count
    assert {comparison.first_reference for comparison in exact_compares} == {
        admission.result_reference
        for _, _, found, _ in measurements
        for admission in found
    }
    assert {comparison.first_reference for comparison in return_compares} == {
        admission.result_reference
        for _, _, _, found in measurements
        for admission in found
    }
    all_occurrences = tuple(
        occurrence for row in occurrences for occurrence in row
    )
    assert all(
        occurrence.material_byte_count_boundary == 4096
        for occurrence in all_occurrences
    )
    truncated = tuple(
        occurrence
        for occurrence in all_occurrences
        if occurrence.stdout_byte_count_boundary_reached
        or occurrence.stderr_byte_count_boundary_reached
    )
    assert all(not occurrence.returned for occurrence in truncated)
    assert all(
        len(occurrence.stdout_bytes or b"") <= 4096
        and len(occurrence.stderr_bytes or b"") <= 4096
        for occurrence in all_occurrences
    )
    assert any(len(admission.admitted_material) > 1 for admission in returned)
    assert any(len(admission.admitted_material) == 1 for admission in returned)
    assert any(
        first_returned.admitted_material != second_returned.admitted_material
        for position, first_returned in enumerate(measurements[0][3])
        for second_returned in (measurements[-1][3][position],)
    )

    act_occurrence_count_boundary = len(references) * len(functions)

    (
        additions,
        result_occurrences,
        result_exact,
        result_returned,
        comparisons,
        return_comparisons,
        addition_admissions,
        return_addition_admissions,
        result_exact_compares,
        result_return_compares,
    ) = measure_added_material(
        functions,
        references,
        source_occurrences,
        returned,
        time_boundary_second_count=second_count,
        act_occurrence_count_boundary=act_occurrence_count_boundary,
    )

    assert len({addition.act_occurrence_identity for addition in additions}) == len(
        additions
    )
    assert len(additions) <= act_occurrence_count_boundary
    assert all(
        addition.admitted_material_act_occurrence_count_boundary
        == act_occurrence_count_boundary
        for addition in additions
    )
    assert all(
        occurrence.time_boundary_second_count == time_counts[0]
        for row in result_occurrences
        for occurrence in row
    )
    source_admission_references = {
        addition.source_admission_result_reference for addition in additions
    }
    assert source_admission_references
    assert source_admission_references <= {
        admission.result_reference for admission in returned
    }
    assert (
        len(result_occurrences)
        == len(comparisons)
        == len(return_comparisons)
        == len(functions)
    )
    for position in range(len(functions)):
        assert len(comparisons[position]) == len(additions)
        assert len(return_comparisons[position]) == len(additions)
        assert all(
            comparison.source_coordinates
            == comparison.source_invocation.return_coordinates
            and comparison.result_coordinates
            == comparison.result_invocation.return_coordinates
            for comparison in return_comparisons[position]
        )
        assert tuple(
            occurrence.source_reference
            for occurrence in result_occurrences[position]
        ) == tuple(
            addition.result_reference for addition in additions
        )
        assert (
            result_exact[position].source_material
            == result_returned[position].source_material
            == tuple(addition.result_reference for addition in additions)
        )
    assert len(addition_admissions) == len(functions) + 1
    assert len(return_addition_admissions) == len(functions) + 1
    assert len(addition_admissions[-1].comparison_occurrences) == len(functions)
    assert len(return_addition_admissions[-1].comparison_occurrences) == len(
        functions
    )
    result_comparison_count = len(functions) * (len(functions) - 1)
    assert len(result_exact_compares) == len(result_return_compares) == (
        result_comparison_count
    )

    (
        all_references,
        all_occurrences,
        all_exact,
        all_returned,
        all_exact_compares,
        all_return_compares,
    ) = measure_material_and_act_results(
        functions,
        references,
        additions,
        time_boundary_second_count=second_count,
    )

    assert all_references == references + tuple(
        addition.result_reference for addition in additions
    )
    assert len(set(all_references)) == len(all_references)
    assert any(
        first.exact_material == second.exact_material and first != second
        for position, first in enumerate(all_references)
        for second in all_references[position + 1 :]
    )
    assert len(all_occurrences) == len(all_exact) == len(all_returned) == len(
        functions
    )
    for position in range(len(functions)):
        assert tuple(
            occurrence.source_reference for occurrence in all_occurrences[position]
        ) == all_references
        assert (
            all_exact[position].source_material
            == all_returned[position].source_material
            == all_references
        )
    assert len(all_exact_compares) == len(all_return_compares) == (
        result_comparison_count
    )

    later = None
    for function_position, function in enumerate(functions):
        earlier, coordinates, later_compare = (
            first_recurring_added_return_compare(
                additions,
                occurrences[function_position],
                function,
                boundary_identity=(
                    f"compiled-material-recurrence-{function_position}"
                ),
                act_occurrence_count_boundary=len(additions),
            )
        )
        if later_compare is None:
            continue
        assert all(
            comparison.addition_occurrence.act_occurrence_identity
            != later_compare.addition_occurrence.act_occurrence_identity
            for comparison in earlier
        )
        assert len(earlier) + 1 < len(additions)
        later = (coordinates, later_compare.result_coordinates)
        break
    assert later is not None
    assert later[0] == later[1]


def test_constructed_output_crosses_the_exact_material_byte_count_boundary():
    _, references = measured_one_byte_material()
    function = MaterialImplementationFunction(
        identity="constructed-output-boundary",
        invocation=(
            sys.executable,
            "-I",
            "-c",
            "import sys; sys.stdin.buffer.read(); "
            "sys.stdout.buffer.write(b'x' * 4097)",
        ),
    )

    occurrences, _exact, _returned = measure_material(
        (function,),
        references[:1],
        boundary_identity="constructed-output-boundary",
        time_boundary_second_count=1.0,
    )

    occurrence = occurrences[0][0]
    assert occurrence.material_byte_count_boundary == 4096
    assert occurrence.stdout_bytes == b"x" * 4096
    assert occurrence.stderr_bytes == b""
    assert occurrence.stdout_byte_count_boundary_reached is True
    assert occurrence.stderr_byte_count_boundary_reached is False
    assert occurrence.returned is False
    assert occurrence.returncode is None


PYTEST_ADMISSION = (
    test_material_climb_refuses_the_collective_act_occurrence_count,
    test_each_compiled_function_preserves_every_one_byte_input_boundary,
    test_constructed_output_crosses_the_exact_material_byte_count_boundary,
)
