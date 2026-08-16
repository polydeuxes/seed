from __future__ import annotations

from pathlib import Path
import sys

import pytest

from seed_runtime.byte_measurement import (
    assertions_of_recorded_byte_measurement,
    record_byte_count_layer,
)
from seed_runtime.events import EventLedger
from seed_runtime.material_ingest import ingest_material


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from compiled_format_invocation import ExactMaterialReference  # noqa: E402
from compiled_material_invocation import (  # noqa: E402
    MaterialImplementationFunction,
    admit_invocation_occurrences,
    ingest_result_reference,
    reference_occurrences_across,
)


def _measured_material():
    ledger = EventLedger()
    ingest_material(
        ledger,
        locality_identity="one-byte-material",
        exact_bytes=bytes(range(256)),
        source_role="fixture material",
        source_boundary="fixture-0",
    )
    measurement = record_byte_count_layer(
        ledger,
        source_locality_identities=("one-byte-material",),
        recording_locality_identity="one-byte-measurement",
    )
    assertions = assertions_of_recorded_byte_measurement(ledger, measurement.identity)
    references = tuple(
        sorted(
            (
                ExactMaterialReference(
                    recorded_occurrence_identity=assertion.recorded_occurrence_identity,
                    assertion_identity=assertion.assertion_identity,
                    exact_material=bytes((assertion.representation,)),
                )
                for assertion in assertions or ()
                if assertion.result == "count"
                and assertion.representation is not None
            ),
            key=lambda reference: reference.exact_material,
        )
    )
    return ledger, references


@pytest.fixture(scope="module")
def material_invocations():
    ledger, references = _measured_material()
    function = MaterialImplementationFunction(
        identity="compiled-0",
        invocation=(
            sys.executable,
            "-I",
            str(Path(__file__).with_name("compiled_tic_tac_toe.py")),
        ),
    )
    occurrences = reference_occurrences_across(
        references,
        boundary_identity="one-byte-compiled-material",
        implementation_functions=(function,),
    )[0]
    return ledger, references, occurrences


def test_every_measured_byte_reaches_the_compiled_function(material_invocations):
    _, references, occurrences = material_invocations

    assert len(references) == len(occurrences) == 256
    assert tuple(reference.exact_material for reference in references) == tuple(
        bytes((value,)) for value in range(256)
    )
    assert tuple(occurrence.source_reference for occurrence in occurrences) == references
    assert len({occurrence.occurrence_identity for occurrence in occurrences}) == 256
    assert all(occurrence.returned for occurrence in occurrences)


def test_compiled_function_establishes_distinct_raw_coordinates(
    material_invocations,
):
    _, references, occurrences = material_invocations
    admission = admit_invocation_occurrences(
        occurrences,
        boundary_identity="one-byte-compiled-material-admission",
    )

    assert admission.source_material == references
    assert len({occurrence.returncode for occurrence in occurrences}) > 1
    assert len(admission.admitted_material) > 1


def test_one_byte_material_crosses_the_return_code_boundary(material_invocations):
    _, _, occurrences = material_invocations

    assert any(
        first.returncode != second.returncode
        for position, first in enumerate(occurrences)
        for second in occurrences[position + 1 :]
    )


def test_each_returned_material_enters_a_fresh_locality(material_invocations):
    ledger, _, occurrences = material_invocations
    events = tuple(
        ingest_material(
            ledger,
            locality_identity=f"compiled-material-result-{position}",
            exact_bytes=occurrence.stdout_bytes,
            source_role="fixture material",
            source_boundary=f"fixture-result-{position}",
        )
        for position, occurrence in enumerate(occurrences)
    )
    references = tuple(
        ingest_result_reference(ledger, event.identity) for event in events
    )

    assert len({event.locality_identity for event in events}) == len(events)
    assert tuple(reference.exact_material for reference in references) == tuple(
        occurrence.stdout_bytes for occurrence in occurrences
    )
    assert len({reference.exact_material for reference in references}) < len(
        references
    )
    assert len({reference.result_identity for reference in references}) == len(
        references
    )
