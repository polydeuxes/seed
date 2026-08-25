from __future__ import annotations

from pathlib import Path
import sys

import pytest




ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from compiled_material_acquisition import (  # noqa: E402
    measure_added_material,
    measure_material,
)
from material_measurement_test_witness import measured_one_byte_material  # noqa: E402
from material_admission import admission_occurrence  # noqa: E402
from compiled_material_invocation import (  # noqa: E402
    MaterialImplementationFunction,
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
    test_constructed_output_crosses_the_exact_material_byte_count_boundary,
)
