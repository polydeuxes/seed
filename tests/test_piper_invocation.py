from __future__ import annotations

from pathlib import Path
import sys

import pytest

from seed_runtime.events import EventLedger
from seed_runtime.material_ingest import ingest_material


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from compiled_format_invocation import (  # noqa: E402
    added_position_occurrences,
)
from compiled_material_invocation import (  # noqa: E402
    MaterialAddedCompareOccurrence,
    compare_added_material_invocations,
    ingest_result_reference,
)
from piper_invocation import (  # noqa: E402
    piper_implementation_function,
    piper_invocations,
)


PIPER = ROOT / ".venv" / "bin" / "piper"
MODEL = Path.home() / ".local" / "share" / "piper-voices" / "en_US-lessac-medium.onnx"
PIPER_AVAILABLE = PIPER.is_file() and MODEL.is_file()


@pytest.fixture(scope="module")
def piper_material():
    if not PIPER_AVAILABLE:
        pytest.skip("Piper implementation function is unavailable")
    book = (ROOT / "book_of_seed" / "README.md").read_bytes()
    start = book.index(b"Seed")
    ledger = EventLedger()
    source = ingest_material(
        ledger,
        locality_identity="piper-source",
        exact_bytes=book[start : start + 4],
        source_role="fixture material",
        source_boundary="fixture-0",
    )
    added = ingest_material(
        ledger,
        locality_identity="piper-added",
        exact_bytes=b" ",
        source_role="fixture material",
        source_boundary="fixture-1",
    )
    source_reference = ingest_result_reference(ledger, source.identity)
    added_reference = ingest_result_reference(ledger, added.identity)
    additions = added_position_occurrences(
        (source_reference,),
        (added_reference,),
        boundary_identity="piper-material-addition",
    )
    implementation = piper_implementation_function(
        executable=PIPER,
        model=MODEL,
        identity="compiled-0",
    )
    source_invocations = piper_invocations(
        (source_reference,),
        (implementation,),
        boundary_identity="piper-source-invocation",
    )
    result_invocations = piper_invocations(
        tuple(addition.result_reference for addition in additions),
        (implementation,),
        boundary_identity="piper-result-invocation",
    )
    comparisons = compare_added_material_invocations(
        additions,
        source_invocations,
        result_invocations,
        boundary_identity="piper-addition-compare",
    )
    return (
        ledger,
        source_reference,
        added_reference,
        additions,
        implementation,
        source_invocations,
        result_invocations,
        comparisons,
    )


def test_piper_receives_exact_book_material_without_a_text_conversion(piper_material):
    source_reference = piper_material[1]
    source_invocation = piper_material[5][0][0]

    assert source_reference.exact_material == b"Seed"
    assert source_invocation.exact_material == source_reference.exact_material
    assert source_invocation.source_reference == source_reference
    assert source_invocation.implementation_function == piper_material[4]
    assert source_invocation.returncode == 0
    assert source_invocation.stdout_bytes
    assert source_invocation.stderr_bytes == b""


def test_every_addition_position_has_an_exact_piper_invocation(piper_material):
    additions = piper_material[3]
    result_invocations = piper_material[6][0]

    assert tuple(addition.position for addition in additions) == (0, 1, 2, 3, 4)
    assert len(result_invocations) == len(additions)
    assert tuple(
        invocation.source_reference for invocation in result_invocations
    ) == tuple(addition.result_reference for addition in additions)
    assert len({invocation.occurrence_identity for invocation in result_invocations}) == len(
        result_invocations
    )
    assert all(invocation.returncode == 0 for invocation in result_invocations)
    assert all(invocation.stdout_bytes for invocation in result_invocations)


def test_piper_comparison_keeps_each_addition_and_both_invocations(piper_material):
    additions = piper_material[3]
    comparisons = piper_material[7][0]

    assert len(comparisons) == len(additions)
    assert tuple(comparison.addition_occurrence for comparison in comparisons) == additions
    assert len({comparison.occurrence_identity for comparison in comparisons}) == len(
        comparisons
    )
    assert all(
        comparison.source_invocation.source_reference
        == comparison.addition_occurrence.source_reference
        for comparison in comparisons
    )
    assert all(
        comparison.result_invocation.source_reference
        == comparison.addition_occurrence.result_reference
        for comparison in comparisons
    )
    assert any(comparison.distinction for comparison in comparisons)


def test_each_piper_result_can_enter_a_fresh_locality_as_exact_material(
    piper_material,
):
    ledger = piper_material[0]
    invocations = piper_material[6][0]
    ingests = tuple(
        ingest_material(
            ledger,
            locality_identity=f"piper-result-{position}",
            exact_bytes=invocation.stdout_bytes,
            source_role="fixture material",
            source_boundary=f"fixture-result-{position}",
        )
        for position, invocation in enumerate(invocations)
    )
    references = tuple(
        ingest_result_reference(ledger, event.identity) for event in ingests
    )

    assert len({event.locality_identity for event in ingests}) == len(ingests)
    assert tuple(reference.exact_material for reference in references) == tuple(
        invocation.stdout_bytes for invocation in invocations
    )
    assert len({reference.result_identity for reference in references}) == len(
        references
    )


def test_piper_compare_refuses_a_result_from_another_addition(piper_material):
    additions = piper_material[3]
    source = piper_material[5][0][0]
    results = piper_material[6][0]

    with pytest.raises(ValueError, match="result differs from its addition Act"):
        MaterialAddedCompareOccurrence(
            boundary_identity="changed-piper-compare",
            occurrence_position=0,
            addition_occurrence=additions[0],
            source_invocation=source,
            result_invocation=results[1],
        )
