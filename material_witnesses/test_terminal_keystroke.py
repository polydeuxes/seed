"""Interrogate one opaque PTY/readline boundary with exact material.

This is the `dfcfcac0` experiment restored outside Seed Fidelity.  The fixed
subprocess is an operator-owned material witness.  Its result is not a Seed
Measurement or Admission occurrence.
"""

from __future__ import annotations

from pathlib import Path
import sys
import tempfile
from io import StringIO

import pytest

from seed_runtime.events import EventLedger
from seed_runtime.byte_measurement import (
    BYTE_MEASUREMENT_RECORDED_KIND,
    BYTE_PAIR_MEASUREMENT_RECORDED_KIND,
    assertions_of_recorded_byte_measurement,
    assertions_of_recorded_byte_position_pair_measurement,
    record_byte_measurement_responsibility_assignment,
    record_byte_measurement_responsible_act_evidence,
    record_byte_measurement_result,
    record_byte_position_pair_count_layer,
)
from seed_runtime.comparison_of_recorded_byte_pair_measurements import (
    RECORDED_PAIR_MEASUREMENT_COMPARISON_RESULT_KIND,
    get_recorded_pair_measurement_comparison,
)
from seed_runtime.witness_material_acquisition import WITNESS_MATERIAL_ACQUISITION_RECORDED_KIND, record_witness_material_acquisition
from seed_runtime.occurrence_position_measurement import (
    OCCURRENCE_POSITION_RECORDED_KIND,
)
from seed_runtime.measurement_of_position_coordinates_of_byte_pair_occurrences import (
    BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND,
)
from seed_runtime.operator_console import run_persistent_operator_console
from seed_runtime.operator_locality_standing import read_operator_locality_standing
from seed_runtime.operator_representation import (
    REPRESENTATION_RECORDED_KIND,
    emit_operator_representation_material,
    read_operator_representation,
    record_operator_representation,
)
from seed_runtime.operator_representation_admission import (
    EXACT_MATERIAL_REPRESENTATION_ADMISSION_RECORDED_KIND,
    REPRESENTATION_CANDIDATE_RECORDED_KIND,
    get_recorded_exact_material_representation_admission,
    get_recorded_representation_candidate,
)
from seed_runtime.operator_invocation_locality import OPERATOR_INVOCATION_LOCALITY_RECORDED_KIND
from seed_runtime.supplied_invocation_material import SuppliedWitnessMaterialOccurrence


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from compiled_material_invocation import (  # noqa: E402
    MaterialImplementationFunction,
    material_acquisition_result_reference,
    invocation_occurrence,
    reference_occurrences_across,
)
from tests.binary_input import binary_input  # noqa: E402
from tests.representation_admission import admit_representation  # noqa: E402


EXACT_MATERIAL = (
    b"printf 012x\x7f3\rexit\r",
    b"printf 0123\rexit\r",
)
IMPLEMENTATION_FUNCTION = MaterialImplementationFunction(
    identity="material-witness-pty-readline-0",
    invocation=(
        "/usr/bin/env",
        "-i",
        "TERM=dumb",
        "HOME=/tmp",
        "PS1=",
        "PS2=",
        "/usr/bin/script",
        "-qefc",
        "/bin/bash --noprofile --norc -i",
        "/dev/null",
    ),
)


@pytest.fixture(scope="module")
def terminal_witness_observation():
    required = tuple(
        Path(path) for path in ("/usr/bin/env", "/usr/bin/script", "/bin/bash")
    )
    if any(not path.is_file() for path in required):
        pytest.skip("opaque PTY implementation function is unavailable")

    ledger = EventLedger()
    acquisition_results = tuple(
        record_witness_material_acquisition(
            ledger,
            locality_identity="terminal-material-witness-source",
            exact_bytes=material,
            source_boundary=f"terminal-material-witness-source-{position}",
        )
        for position, material in enumerate(EXACT_MATERIAL)
    )
    references = tuple(
        material_acquisition_result_reference(ledger, occurrence.identity) for occurrence in acquisition_results
    )
    invocations = reference_occurrences_across(
        references,
        boundary_identity="terminal-material-witness-invocation",
        implementation_functions=(IMPLEMENTATION_FUNCTION,),
        max_workers=1,
        time_limit_second_count=2.0,
        material_byte_count_limit=65536,
    )[0]
    result_acquisition_results = tuple(
        record_witness_material_acquisition(
            ledger,
            locality_identity="terminal-material-witness-result",
            exact_bytes=occurrence.stdout_bytes or b"",
            source_boundary=f"external PTY stdout occurrence {position}",
            provenance_occurrence_references=(acquisition_results[position].identity,),
        )
        for position, occurrence in enumerate(invocations)
    )
    return ledger, acquisition_results, references, invocations, result_acquisition_results


def test_exact_material_reaches_the_external_function_unchanged(
    terminal_witness_observation,
):
    _, acquisition_results, references, invocations, _ = terminal_witness_observation

    assert tuple(occurrence.exact_material for occurrence in acquisition_results) == EXACT_MATERIAL
    assert tuple(reference.exact_material for reference in references) == EXACT_MATERIAL
    assert tuple(occurrence.exact_material for occurrence in invocations) == EXACT_MATERIAL
    assert tuple(
        occurrence.input_boundary_accepted_byte_count
        for occurrence in invocations
    ) == tuple(len(material) for material in EXACT_MATERIAL)
    assert tuple(occurrence.source_reference for occurrence in invocations) == references


def test_the_external_result_preserves_every_bounded_process_coordinate(
    terminal_witness_observation,
):
    _, _, _, invocations, _ = terminal_witness_observation

    for occurrence in invocations:
        assert occurrence.result_reference.coordinates == occurrence.coordinates
        assert occurrence.stdout_bytes is None or type(occurrence.stdout_bytes) is bytes
        assert occurrence.stderr_bytes is None or type(occurrence.stderr_bytes) is bytes


def test_one_exact_del_byte_changes_the_external_result(
    terminal_witness_observation,
):
    _, _, references, invocations, _ = terminal_witness_observation

    assert EXACT_MATERIAL[0] == b"printf 012x" + bytes((127,)) + b"3\rexit\r"
    assert tuple(
        occurrence.input_boundary_accepted_byte_count
        for occurrence in invocations
    ) == tuple(len(material) for material in EXACT_MATERIAL)
    assert invocations[0].return_coordinates[:2] == (
        invocations[1].return_coordinates[:2]
    )
    assert invocations[0].return_coordinates[3:] == (
        invocations[1].return_coordinates[3:]
    )
    assert invocations[0].return_coordinates != invocations[1].return_coordinates
    assert invocations[0].stdout_bytes != invocations[1].stdout_bytes
    assert invocations[0].coordinates != invocations[1].coordinates
    assert references[0].result_identity != references[1].result_identity


def test_external_results_enter_seed_only_as_exact_provenanced_material(
    terminal_witness_observation,
):
    _, source_acquisition_results, _, invocations, result_acquisition_results = terminal_witness_observation

    assert tuple(occurrence.exact_material for occurrence in result_acquisition_results) == tuple(
        invocation.stdout_bytes or b"" for invocation in invocations
    )
    assert tuple(
        occurrence.material["provenance_occurrence_references"]
        for occurrence in result_acquisition_results
    ) == tuple([source.identity] for source in source_acquisition_results)


def test_seed_measures_source_and_result_pair_findings_independently(
    terminal_witness_observation,
):
    _, _, _, invocations, _ = terminal_witness_observation
    ledger = EventLedger()
    localities = (
        "terminal-pair-source-locality",
        "terminal-pair-result-locality",
    )
    materials = (
        EXACT_MATERIAL,
        tuple(invocation.stdout_bytes or b"" for invocation in invocations),
    )
    findings = []

    for locality_identity, exact_materials in zip(localities, materials):
        for position, exact_material in enumerate(exact_materials):
            record_witness_material_acquisition(
                ledger,
                locality_identity=locality_identity,
                exact_bytes=exact_material,
                source_boundary=f"terminal pair occurrence {position}",
            )
        byte_assignment = record_byte_measurement_responsibility_assignment(
            ledger,
            source_localities=(locality_identity,),
            recording_locality_identity=locality_identity,
            locality_standing=read_operator_locality_standing(
                ledger, locality_identity=locality_identity
            ),
        )
        byte_act = record_byte_measurement_responsible_act_evidence(
            ledger,
            responsibility_assignment_event_identity=byte_assignment.identity,
            responsibility_assignment_standing=read_operator_locality_standing(
                ledger, locality_identity=locality_identity
            ),
        )
        byte_result = record_byte_measurement_result(
            ledger,
            responsible_act_evidence_event_identity=byte_act.identity,
        )
        pair_result = record_byte_position_pair_count_layer(
            ledger,
            source_measurement_event_identity=byte_result.identity,
            recording_locality_identity=locality_identity,
        )
        assertions = assertions_of_recorded_byte_position_pair_measurement(
            ledger, pair_result.identity
        )
        findings.append(
            {
                (
                    assertion.result,
                    assertion.representation,
                ): assertion.material["dimensions"]["content"]
                for assertion in assertions
            }
        )
        standing = read_operator_locality_standing(
            ledger, locality_identity=locality_identity
        )
        assert byte_result.identity in standing["measurement_occurrences"]
        assert pair_result.identity in standing["measurement_occurrences"]

    source_findings, result_findings = findings
    assert len(source_findings) == 34
    assert len(result_findings) == 45
    assert source_findings != result_findings
    assert set(source_findings) - set(result_findings) == {
        ("count", (120, 127)),
        ("count", (127, 51)),
        ("count", (13, 101)),
        ("recurrence", (13, 101)),
    }
    assert set(result_findings) - set(source_findings) == {
        ("count", (10, 101)),
        ("count", (10, 112)),
        ("count", (10, 48)),
        ("count", (120, 8)),
        ("count", (13, 10)),
        ("count", (32, 8)),
        ("count", (51, 101)),
        ("count", (8, 32)),
        ("count", (8, 51)),
        ("recurrence", (10, 101)),
        ("recurrence", (10, 112)),
        ("recurrence", (10, 48)),
        ("recurrence", (13, 10)),
        ("recurrence", (50, 51)),
        ("recurrence", (51, 101)),
    }


def test_one_exact_witness_result_crosses_the_operator_emission_road(
    terminal_witness_observation,
):
    ledger, _, _, _, result_acquisition_results = terminal_witness_observation
    source = result_acquisition_results[0]
    representation = record_operator_representation(
        ledger,
        locality_identity=source.locality_identity,
        locality_standing=read_operator_locality_standing(
            ledger, locality_identity=source.locality_identity
        ),
        source_occurrence_reference=source.identity,
    )

    with tempfile.TemporaryFile(mode="w+b") as output:
        admission, applicability, standing, boundary = admit_representation(
            ledger,
            representation,
            boundary_identity="terminal-material-witness-output",
            operator_locality_identity="terminal-material-witness-operator",
            output_stream=output,
        )
        emitted = emit_operator_representation_material(
            ledger,
            representation=representation,
            admission_result_event_identity=admission.identity,
            applicability_result_event_identity=applicability.identity,
            locality_standing=standing,
            output_boundary=boundary,
        )
        output.seek(0)
        exact_output = output.read()

    assert exact_output == source.exact_material
    assert ledger.get(emitted["emitted_event_identity"]).exact_material == (
        source.exact_material
    )


def test_console_naturally_decomposes_each_supplied_terminal_witness_occurrence():
    ledger = EventLedger()
    command = b"!witness terminal\n"
    observations = tuple(
        invocation_occurrence(
            exact_material,
            IMPLEMENTATION_FUNCTION,
            boundary_identity="terminal-console-material-witness",
            invocation_position=position,
            time_limit_second_count=2.0,
            material_byte_count_limit=65536,
        )
        for position, exact_material in enumerate(EXACT_MATERIAL)
    )

    def provider(exact_command, supply):
        assert exact_command == command
        supply(
            SuppliedWitnessMaterialOccurrence(
                exact_bytes=IMPLEMENTATION_FUNCTION.identity.encode("ascii"),
                source_boundary="terminal witness implementation function reference",
                egress=False,
            )
        )
        for position, (exact_source, observation) in enumerate(
            zip(EXACT_MATERIAL, observations)
        ):
            supply(
                SuppliedWitnessMaterialOccurrence(
                    exact_bytes=exact_source,
                    source_boundary=f"terminal witness source occurrence {position}",
                    egress=False,
                )
            )
            supply(
                SuppliedWitnessMaterialOccurrence(
                    exact_bytes=observation.stdout_bytes or b"",
                    source_boundary=f"terminal witness stdout occurrence {position}",
                    egress=True,
                    provenance_occurrence_positions=(0, 1 + position * 2),
                )
            )

    with tempfile.TemporaryFile(mode="w+b") as raw_output:
        run_persistent_operator_console(
            ledger=ledger,
            locality_identity="terminal-witness-operator-locality",
            input_stream=binary_input(command),
            output_stream=StringIO(),
            raw_output_stream=raw_output,
            operator_invocation_provider=provider,
        )
        raw_output.seek(0)
        emitted_material = raw_output.read()

    relation = next(
        event
        for event in ledger.list()
        if event.kind == OPERATOR_INVOCATION_LOCALITY_RECORDED_KIND
    )
    invocation_locality = relation.material["destination_locality_identity"]
    witness_events = ledger.list_locality(invocation_locality)
    acquisition_results = tuple(
        event for event in witness_events if event.kind == WITNESS_MATERIAL_ACQUISITION_RECORDED_KIND
    )
    measurements = tuple(
        event for event in witness_events if event.kind == BYTE_MEASUREMENT_RECORDED_KIND
    )
    pair_measurements = tuple(
        event
        for event in witness_events
        if event.kind == BYTE_PAIR_MEASUREMENT_RECORDED_KIND
    )
    position_measurements = tuple(
        event
        for event in witness_events
        if event.kind == OCCURRENCE_POSITION_RECORDED_KIND
    )
    direct_position_measurements = tuple(
        event
        for event in witness_events
        if event.kind == BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND
    )
    emissions = tuple(
        event
        for event in witness_events
        if event.kind == "operator.representation.emitted"
    )
    comparisons = tuple(
        event
        for event in witness_events
        if event.kind == RECORDED_PAIR_MEASUREMENT_COMPARISON_RESULT_KIND
    )
    representations = tuple(
        event for event in witness_events if event.kind == REPRESENTATION_RECORDED_KIND
    )
    candidates = tuple(
        event
        for event in witness_events
        if event.kind == REPRESENTATION_CANDIDATE_RECORDED_KIND
    )
    admissions = tuple(
        event
        for event in witness_events
        if event.kind == EXACT_MATERIAL_REPRESENTATION_ADMISSION_RECORDED_KIND
    )

    expected_supplied = tuple(
        (
            IMPLEMENTATION_FUNCTION.identity.encode("ascii"),
            *(
                material
                for position in range(len(EXACT_MATERIAL))
                for material in (
                    EXACT_MATERIAL[position],
                    observations[position].stdout_bytes or b"",
                )
            ),
        )
    )
    expected_emitted = tuple(
        observation.stdout_bytes or b"" for observation in observations
    )
    assert tuple(event.exact_material for event in acquisition_results) == expected_supplied
    assert tuple(
        event.material["provenance_occurrence_references"][-2:]
        for event in acquisition_results[2::2]
    ) == tuple(
        [acquisition_results[0].identity, acquisition_results[1 + position * 2].identity]
        for position in range(len(EXACT_MATERIAL))
    )
    assert len(measurements) == len(acquisition_results) == 5
    assert len(direct_position_measurements) == len(acquisition_results) == 5
    assert len(pair_measurements) == len(EXACT_MATERIAL) * 2 == 4
    assert len(position_measurements) == len(acquisition_results) == 5
    for position, measurement in enumerate(measurements):
        assertions = assertions_of_recorded_byte_measurement(
            ledger, measurement.identity
        )
        source_set = next(
            assertion
            for assertion in assertions
            if assertion.result == "exact_source_material_set"
        )
        assert source_set.material["dimensions"]["content"]["source_material"] == [
            {"material_acquisition_occurrence_identity": event.identity}
            for event in acquisition_results[: position + 1]
        ]
    assert tuple(event.exact_material for event in emissions) == expected_emitted
    assert emitted_material == b"".join(expected_emitted)

    assert len(comparisons) == len(EXACT_MATERIAL) == 2
    for position, comparison in enumerate(comparisons):
        recorded = get_recorded_pair_measurement_comparison(
            ledger, comparison.identity
        )
        assignment = ledger.get(
            recorded["responsibility_assignment_reference"][
                "recorded_occurrence_identity"
            ]
        )
        assert assignment is not None
        assert assignment.material["earlier_measurement_reference"][
            "recorded_occurrence_identity"
        ] == pair_measurements[position * 2].identity
        assert assignment.material["later_measurement_reference"][
            "recorded_occurrence_identity"
        ] == pair_measurements[1 + position * 2].identity
        assert assignment.material["added_occurrence_reference"] == acquisition_results[
            2 + position * 2
        ].identity
        assert assignment.material[
            "operator_invocation_locality_relation_event_identity"
        ] == relation.identity
        assert assignment.material["destination_operator_locality_identity"] == (
            "terminal-witness-operator-locality"
        )
        assert assignment.material[
            "added_occurrence_provenance_references"
        ] == acquisition_results[2 + position * 2].material[
            "provenance_occurrence_references"
        ]
        assert recorded["findings"]["conflicting_findings"]
        assert recorded["findings"]["unknown_findings"] == []
        assert "cause" not in recorded
        assert "meaning" not in recorded

    comparison_identities = {comparison.identity for comparison in comparisons}
    comparison_representations = tuple(
        read_operator_representation(ledger, representation.identity)
        for representation in representations
        if representation.material["source_occurrence_reference"]
        in comparison_identities
    )
    assert len(comparison_representations) == len(comparisons)
    assert {
        representation["source_occurrence_reference"]
        for representation in comparison_representations
    } == comparison_identities
    assert all(
        representation["exact_material"] is None
        and "representation_rule" not in representation
        for representation in comparison_representations
    )

    comparison_representation_identities = {
        representation["representation_event_identity"]
        for representation in comparison_representations
    }
    comparison_candidates = tuple(
        get_recorded_representation_candidate(ledger, candidate.identity)
        for candidate in candidates
        if candidate.material["representation_reference"][
            "representation_event_identity"
        ]
        in comparison_representation_identities
    )
    assert len(comparison_candidates) == len(comparisons)
    assert all(
        candidate["destination_operator_locality_identity"]
        == "terminal-witness-operator-locality"
        and "representation_rule" not in candidate["representation_reference"]
        for candidate in comparison_candidates
    )
    admitted_candidate_identities = {
        get_recorded_exact_material_representation_admission(
            ledger, admission.identity
        )["candidate_reference"]["recorded_occurrence_identity"]
        for admission in admissions
    }
    assert admitted_candidate_identities.isdisjoint(
        candidate.identity
        for candidate in candidates
        if candidate.material["representation_reference"][
            "representation_event_identity"
        ]
        in comparison_representation_identities
    )

    standing = read_operator_locality_standing(
        ledger, locality_identity=invocation_locality
    )
    assert set(standing["measurement_occurrences"]) == {
        *(measurement.identity for measurement in measurements),
        *(measurement.identity for measurement in pair_measurements),
        *(measurement.identity for measurement in position_measurements),
        *(measurement.identity for measurement in direct_position_measurements),
    }
    assert set(standing["comparison_result_occurrences"]) == {
        comparison.identity for comparison in comparisons
    }
    assert comparison_representation_identities <= {
        representation["representation_event_identity"]
        for representation in standing["representations"].values()
    }
    assert {
        candidate.identity
        for candidate in candidates
        if candidate.material["representation_reference"][
            "representation_event_identity"
        ]
        in comparison_representation_identities
    } <= set(standing["candidate_result_occurrences"])
