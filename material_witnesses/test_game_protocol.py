"""Interrogate one stateful game protocol with two exact command streams.

The external implementation preserves state while consuming each complete
stream.  Its results are material-witness testimony, not strategy, a framing
relation, or a Seed competency.
"""

from __future__ import annotations

from pathlib import Path
import sys

import pytest

from seed_runtime.events import EventLedger
from seed_runtime.witness_material_acquisition import record_witness_material_acquisition


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from compiled_material_invocation import (  # noqa: E402
    MaterialImplementationFunction,
    material_acquisition_result_reference,
    reference_occurrences_across,
)


ENV = Path("/usr/bin/env")
IMPLEMENTATION = Path("/usr/games/stockfish")
EXACT_MATERIAL = (
    b"uci\nisready\nposition startpos\nmoves e2e4\ngo depth 1\nquit\n",
    b"uci\nisready\nposition startpos moves e2e4\ngo depth 1\nquit\n",
)


@pytest.fixture(scope="module")
def game_protocol_witness_observation():
    if not ENV.is_file() or not IMPLEMENTATION.is_file():
        pytest.skip("the external game implementation function is unavailable")

    ledger = EventLedger()
    sources = tuple(
        record_witness_material_acquisition(
            ledger,
            locality_identity="game-protocol-material-witness-source",
            exact_bytes=material,
            source_boundary=f"game protocol source occurrence {position}",
        )
        for position, material in enumerate(EXACT_MATERIAL)
    )
    references = tuple(
        material_acquisition_result_reference(ledger, source.identity) for source in sources
    )
    function = MaterialImplementationFunction(
        identity="material-witness-game-protocol-0",
        invocation=(str(ENV), "-i", str(IMPLEMENTATION)),
    )
    invocations = reference_occurrences_across(
        references,
        boundary_identity="game-protocol-material-witness-invocation",
        implementation_functions=(function,),
        max_workers=1,
        time_limit_second_count=5.0,
        material_byte_count_limit=1048576,
    )[0]
    results = tuple(
        record_witness_material_acquisition(
            ledger,
            locality_identity="game-protocol-material-witness-result",
            exact_bytes=invocation.stdout_bytes or b"",
            source_boundary=f"external game stdout occurrence {position}",
            provenance_occurrence_references=(sources[position].identity,),
        )
        for position, invocation in enumerate(invocations)
    )
    return ledger, sources, references, function, invocations, results


def test_each_exact_command_stream_reaches_the_input_boundary(
    game_protocol_witness_observation,
):
    _, sources, references, function, invocations, _ = (
        game_protocol_witness_observation
    )

    assert tuple(source.exact_material for source in sources) == EXACT_MATERIAL
    assert tuple(reference.exact_material for reference in references) == EXACT_MATERIAL
    assert tuple(invocation.exact_material for invocation in invocations) == (
        EXACT_MATERIAL
    )
    assert tuple(invocation.source_reference for invocation in invocations) == (
        references
    )
    assert all(invocation.implementation_function == function for invocation in invocations)
    assert tuple(
        invocation.input_boundary_accepted_byte_count
        for invocation in invocations
    ) == tuple(len(material) for material in EXACT_MATERIAL)


def test_one_changed_turn_boundary_produces_a_distinct_external_result(
    game_protocol_witness_observation,
):
    _, _, _, _, invocations, _ = game_protocol_witness_observation
    first, second = invocations

    assert all(invocation.returned for invocation in invocations)
    assert all(invocation.returncode == 0 for invocation in invocations)
    assert all(invocation.stderr_bytes == b"" for invocation in invocations)
    assert b"Unknown command: 'moves e2e4'." in (first.stdout_bytes or b"")
    assert b"Unknown command: 'moves e2e4'." not in (second.stdout_bytes or b"")
    assert b"\nbestmove " in (first.stdout_bytes or b"")
    assert b"\nbestmove " in (second.stdout_bytes or b"")
    assert first.stdout_bytes != second.stdout_bytes
    assert first.coordinates != second.coordinates
    assert first.return_coordinates[:2] == second.return_coordinates[:2]
    assert first.return_coordinates[3:] == second.return_coordinates[3:]


def test_external_results_enter_seed_as_exact_provenanced_material(
    game_protocol_witness_observation,
):
    _, sources, _, _, invocations, results = game_protocol_witness_observation

    assert tuple(result.exact_material for result in results) == tuple(
        invocation.stdout_bytes for invocation in invocations
    )
    assert tuple(
        result.material["provenance_occurrence_references"] for result in results
    ) == tuple([source.identity] for source in sources)
