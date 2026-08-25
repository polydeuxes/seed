from __future__ import annotations

from pathlib import Path
import sys




ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from compiled_material_invocation import MaterialImplementationFunction  # noqa: E402
from compiled_material_measurement_harness import measure  # noqa: E402
from material_measurement_test_witness import measured_one_byte_material  # noqa: E402


def test_harness_preserves_exact_and_return_admissions_separately():
    _, references = measured_one_byte_material()
    occurrences, exact, returned = measure(
        MaterialImplementationFunction(
            identity="compiled-0",
            invocation=("/bin/cat",),
        ),
        references[:3],
        time_boundary_second_count=1.0,
        max_workers=1,
    )

    assert tuple(occurrence.source_reference for occurrence in occurrences) == (
        references[:3]
    )
    assert len(exact.admitted_material) == 3
    assert len(returned.admitted_material) == 1
    assert returned.admitted_material[0] == references[:3]


PYTEST_ADMISSION = (
    test_harness_preserves_exact_and_return_admissions_separately,
)
