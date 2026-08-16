from __future__ import annotations

from pathlib import Path
import shutil
import sys

import pytest

from seed_runtime.events import EventLedger
from seed_runtime.material_ingest import ingest_material


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from compiled_material_invocation import (  # noqa: E402
    MaterialImplementationFunction,
    ingest_result_reference,
    reference_occurrences_across,
)
from material_fixture_books import MATERIAL_WINDOWS, supplied_book_material  # noqa: E402


@pytest.fixture(scope="module")
def supplied_material_in_order():
    paths = tuple(ROOT / "corpus" / name for name, _ in MATERIAL_WINDOWS)
    if any(not path.is_file() for path in paths):
        pytest.skip("supplied fixture material is unavailable")
    return supplied_book_material(ROOT)


def test_each_supplied_material_carries_the_same_line_count(
    supplied_material_in_order,
):
    assert len(supplied_material_in_order) == len(MATERIAL_WINDOWS) == 16
    assert all(
        len(material.splitlines()) == 300 for material in supplied_material_in_order
    )


def test_supplied_order_survives_distinct_localities_and_compiled_invocations(
    supplied_material_in_order,
):
    executable = shutil.which("cat")
    if executable is None:
        pytest.skip("compiled implementation function is unavailable")
    ledger = EventLedger()
    ingests = tuple(
        ingest_material(
            ledger,
            locality_identity=f"supplied-material-{position}",
            exact_bytes=material,
            source_role="fixture material",
            source_boundary=f"fixture-{position}",
        )
        for position, material in enumerate(supplied_material_in_order)
    )
    references = tuple(
        ingest_result_reference(ledger, event.identity) for event in ingests
    )
    occurrences = reference_occurrences_across(
        references,
        boundary_identity="supplied-material-invocation",
        implementation_functions=(
            MaterialImplementationFunction(
                identity="compiled-0",
                invocation=(executable,),
            ),
        ),
        wait_seconds=31.0,
    )[0]

    assert len({event.locality_identity for event in ingests}) == len(ingests)
    assert tuple(reference.locality_identity for reference in references) == tuple(
        event.locality_identity for event in ingests
    )
    assert tuple(occurrence.invocation_position for occurrence in occurrences) == tuple(
        range(len(references))
    )
    assert tuple(occurrence.source_reference for occurrence in occurrences) == references
    assert all(occurrence.wait_seconds == 31.0 for occurrence in occurrences)
    assert tuple(occurrence.exact_material for occurrence in occurrences) == (
        supplied_material_in_order
    )
    assert tuple(occurrence.stdout_bytes for occurrence in occurrences) == (
        supplied_material_in_order
    )
    assert all(occurrence.returncode == 0 for occurrence in occurrences)
    assert all(occurrence.stderr_bytes == b"" for occurrence in occurrences)
