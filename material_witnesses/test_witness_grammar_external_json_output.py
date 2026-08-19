"""Carry exact Witness Grammar bytes through one external JSON result boundary.

The external function occurrence remains Witness Material.  Its exact stdout
enters Seed only through a later Ingest Act and then becomes exact material for
one Seed-native byte Measurement.  Neither road establishes JSON structure,
word positions, or relation Standing.
"""

from __future__ import annotations

from pathlib import Path
import sys

import pytest

from seed_runtime.byte_measurement import (
    BYTE_MEASUREMENT_RECORDED_KIND,
)
from seed_runtime.events import EventLedger
from seed_runtime.material_ingest import (
    MATERIAL_INGEST_OCCURRED_KIND,
    ingest_material,
    read_exact_ingest_result,
)
from seed_runtime.measurement_of_position_coordinates_of_byte_pair_occurrences import (
    BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND,
    references_to_recorded_position_coordinates_of_byte_pair_occurrences,
)
from seed_runtime.standing_measurement_declarations import (
    record_declared_measurements_from_current_standing,
)


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from compiled_material_invocation import (  # noqa: E402
    MaterialImplementationFunction,
    ingest_result_reference,
    reference_occurrences_across,
)


WITNESS_GRAMMAR = ROOT / "book_of_seed" / "witness_grammar.json"
SOURCE_LOCALITY = "witness-grammar-external-json-source"
RESULT_LOCALITY = "witness-grammar-external-json-result"
EXTERNAL_JSON_FUNCTION = MaterialImplementationFunction(
    identity="material-witness-cpython-json-tool-compact",
    invocation=(sys.executable, "-m", "json.tool", "--compact"),
)
EXTERNAL_JSON_KNOWN_LOSS = (
    "source byte positions and source lexical formatting are not preserved",
)


@pytest.fixture(scope="module")
def witness_grammar_external_json_observation():
    ledger = EventLedger()
    exact_source = WITNESS_GRAMMAR.read_bytes()
    source = ingest_material(
        ledger,
        locality_identity=SOURCE_LOCALITY,
        exact_bytes=exact_source,
        source_role="Witness Grammar material",
        source_boundary="exact Witness Grammar file bytes",
    )
    source_reference = ingest_result_reference(ledger, source.identity)

    before_external_invocation = ledger.append_boundary()
    invocation = reference_occurrences_across(
        (source_reference,),
        boundary_identity="witness-grammar-external-json-invocation",
        implementation_functions=(EXTERNAL_JSON_FUNCTION,),
        max_workers=1,
        time_limit_second_count=5.0,
        material_byte_count_limit=262144,
    )[0][0]
    after_external_invocation = ledger.append_boundary()

    if (
        not invocation.returned
        or invocation.returncode != 0
        or type(invocation.stdout_bytes) is not bytes
        or type(invocation.stderr_bytes) is not bytes
    ):
        pytest.fail("external JSON witness did not return exact result material")

    result = ingest_material(
        ledger,
        locality_identity=RESULT_LOCALITY,
        exact_bytes=invocation.stdout_bytes,
        source_role="external JSON result material",
        source_boundary="external JSON stdout occurrence 0",
        known_loss=EXTERNAL_JSON_KNOWN_LOSS,
        provenance_occurrence_references=(source.identity,),
    )
    declared_measurements = record_declared_measurements_from_current_standing(
        ledger,
        locality_identity=RESULT_LOCALITY,
    )
    position_measurement = next(
        event
        for event in declared_measurements.result_occurrences
        if event.kind == BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND
    )
    byte_measurement = next(
        event
        for event in declared_measurements.result_occurrences
        if event.kind == BYTE_MEASUREMENT_RECORDED_KIND
    )
    return {
        "ledger": ledger,
        "exact_source": exact_source,
        "source": source,
        "source_reference": source_reference,
        "before_external_invocation": before_external_invocation,
        "after_external_invocation": after_external_invocation,
        "invocation": invocation,
        "result": result,
        "declared_measurements": declared_measurements,
        "position_measurement": position_measurement,
        "byte_measurement": byte_measurement,
    }


def test_exact_witness_grammar_ingest_result_reaches_the_external_json_function(
    witness_grammar_external_json_observation,
):
    observation = witness_grammar_external_json_observation
    source = observation["source"]
    source_reference = observation["source_reference"]
    invocation = observation["invocation"]

    assert read_exact_ingest_result(
        observation["ledger"], source.identity
    ) == source
    assert source_reference.recorded_occurrence_identity == source.identity
    assert source_reference.exact_material == observation["exact_source"]
    assert invocation.source_reference == source_reference
    assert invocation.exact_material == observation["exact_source"]
    assert invocation.implementation_function == EXTERNAL_JSON_FUNCTION
    assert invocation.input_boundary_accepted_byte_count == len(
        observation["exact_source"]
    )


def test_external_json_invocation_appends_no_seed_occurrence(
    witness_grammar_external_json_observation,
):
    observation = witness_grammar_external_json_observation

    assert observation["before_external_invocation"] == observation[
        "after_external_invocation"
    ]


def test_external_json_output_enters_seed_only_as_exact_provenanced_material(
    witness_grammar_external_json_observation,
):
    observation = witness_grammar_external_json_observation
    ledger = observation["ledger"]
    source = observation["source"]
    invocation = observation["invocation"]
    result = observation["result"]

    assert result.kind == MATERIAL_INGEST_OCCURRED_KIND
    assert read_exact_ingest_result(ledger, result.identity) == result
    assert result.exact_material == invocation.stdout_bytes
    assert result.material["provenance_occurrence_references"] == [
        source.identity
    ]
    assert result.material["known_loss"] == list(EXTERNAL_JSON_KNOWN_LOSS)
    assert result.material["unknown"] == [
        "represented_relation",
        "source_relation",
    ]
    assert "implementation_function_identity" not in result.material
    assert "external_invocation_occurrence_identity" not in result.material


def test_seed_native_byte_measurement_reads_only_the_external_output_ingest_result(
    witness_grammar_external_json_observation,
):
    observation = witness_grammar_external_json_observation
    measurement = observation["byte_measurement"]

    assert measurement.kind == BYTE_MEASUREMENT_RECORDED_KIND
    assert measurement.locality_identity == RESULT_LOCALITY
    assert measurement.material["source_localities"] == [RESULT_LOCALITY]
    assert measurement.material["assertions"]
    assert all(
        assertion["assertion_scope"]["source_localities"]
        == [RESULT_LOCALITY]
        for assertion in measurement.material["assertions"]
    )


def test_seed_native_position_measurement_records_every_external_output_byte_pair_occurrence(
    witness_grammar_external_json_observation,
):
    observation = witness_grammar_external_json_observation
    ledger = observation["ledger"]
    result = observation["result"]
    measurement = observation["position_measurement"]
    references = (
        references_to_recorded_position_coordinates_of_byte_pair_occurrences(
            ledger, measurement.identity
        )
    )

    assert measurement.locality_identity == RESULT_LOCALITY
    assert measurement.material["source_ingest_occurrence_identity"] == (
        result.identity
    )
    assert measurement.material["assertions"]["occurrences"] == max(
        len(result.exact_material) - 1,
        0,
    )
    assert len(references) == max(len(result.exact_material) - 1, 0)
    assert tuple(reference.first_position for reference in references) == tuple(
        range(len(references))
    )
    assert tuple(reference.second_position for reference in references) == tuple(
        range(1, len(references) + 1)
    )
    assert all(
        reference.exact_pair
        == result.exact_material[
            reference.first_position : reference.second_position + 1
        ]
        for reference in references
    )
