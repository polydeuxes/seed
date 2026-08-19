from copy import deepcopy
from collections import Counter
import ast
import json
import re
from tests.binary_input import binary_input
from io import BytesIO, StringIO
from pathlib import Path

from tests.representation_admission import admit_representation

from seed_runtime.byte_measurement import (
    BYTE_MEASUREMENT_RECORDED_KIND,
    BYTE_MEASUREMENT_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND,
    BYTE_MEASUREMENT_RESPONSIBLE_ACT_EVIDENCE_KIND,
    ASSERTION_LOCALITY_MOVEMENT_RESPONSIBILITY_ASSIGNMENT_KIND,
    BYTE_MEASUREMENT_RESPONSIBILITY,
    BYTE_MEASUREMENT_RULE,
    BYTE_PAIR_INPUT_ROLE,
    BYTE_PAIR_MEASUREMENT_RECORDED_KIND,
    BYTE_PAIR_MEASUREMENT_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND,
    BYTE_PAIR_RESPONSIBLE_ACT_EVIDENCE_KIND,
    BYTE_PAIR_MEASUREMENT_RESPONSIBILITY,
    BYTE_PAIR_MEASUREMENT_RULE,
    MEASURED_ASSERTION_RESPONSIBILITY,
    SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY,
    EVENT_KIND_RESPONSIBILITIES as BYTE_EVENT_KIND_RESPONSIBILITIES,
    _identity,
    _validate_moved_byte_assertion,
    assertions_of_recorded_byte_measurement,
    assertions_of_recorded_byte_position_pair_measurement,
    get_recorded_pair_input_applicability,
    get_byte_position_pair_measurement_responsibility_assignment,
    record_byte_measurement_responsibility_assignment,
    record_byte_position_pair_count_layer,
    record_byte_measurement_responsible_act_evidence,
    record_byte_measurement_result,
)
from seed_runtime.events import CORRUPTED, EventLedger
from seed_runtime.comparison_of_recorded_byte_pair_measurements import (
    record_recorded_pair_measurement_comparison_responsibility_assignment,
    record_recorded_pair_measurement_comparison_applicability_act_evidence,
    record_recorded_pair_measurement_comparison_applicability_result,
    record_recorded_pair_measurement_comparison_act_evidence,
    record_recorded_pair_measurement_comparison_result,
)
from seed_runtime.comparison_of_ordered_relation_path_with_recorded_pair_findings import (
    EVENT_KIND_RESPONSIBILITIES as PATH_FINDING_COMPARISON_EVENT_KIND_RESPONSIBILITIES,
    COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_RESPONSIBILITY_ASSIGNMENT_KIND,
    COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_APPLICABILITY_ACT_EVIDENCE_KIND,
    COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_APPLICABILITY_RESULT_KIND,
    COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_COMPARE_ACT_EVIDENCE_KIND,
    COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_RESULT_KIND,
)
from seed_runtime.candidate_standing_from_exact_result_assertions import (
    record_complete_candidate_standing,
)
from seed_runtime.identities import new_identity
from seed_runtime.material_ingest import ingest_material
from seed_runtime.measurement_of_recurrent_byte_pair_occurrence_position import (
    EVENT_KIND_RESPONSIBILITIES as PAIR_OCCURRENCE_EVENT_KIND_RESPONSIBILITIES,
    RECORDED_EVIDENCE_OF_ACT_OCCURRENCE_OF_MEASUREMENT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_KIND,
    RECORDING_OCCURRENCE_OF_RESULT_OF_MEASUREMENT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_KIND,
    RECORDED_RESPONSIBILITY_ASSIGNMENT_OF_MEASUREMENT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_KIND,
    RESPONSIBILITY_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_MEASUREMENT,
    RULE_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_MEASUREMENT,
    measure_positions_for_recurrent_byte_pair_assertions,
    measure_positions_of_recurrent_byte_pair_occurrences,
    references_to_recorded_recurrent_byte_pair_occurrence_positions,
    record_responsibility_assignment_for_measurement_of_recurrent_byte_pair_occurrence_position,
    record_evidence_of_act_occurrence_for_measurement_of_recurrent_byte_pair_occurrence_position,
    record_result_of_measurement_of_recurrent_byte_pair_occurrence_position,
)
from seed_runtime.measurement_of_shared_position_of_byte_pair_occurrences import (
    MEASUREMENT_RULE as SHARED_POSITION_MEASUREMENT_RULE,
    RESPONSIBILITY as SHARED_POSITION_MEASUREMENT_RESPONSIBILITY,
    SHARED_POSITION_ASSERTION_RESPONSIBILITY,
    SHARED_POSITION_MEASUREMENT_RESULT_KIND,
    record_shared_position_responsibility_assignment,
    record_shared_position_applicability_act_evidence,
    record_shared_position_applicability_result,
    record_shared_position_measurement_act_evidence,
    record_shared_position_measurement_result,
)
from seed_runtime.operator_console import run_persistent_operator_console
from seed_runtime.operator_locality_standing import (
    read_operator_locality_standing,
    read_operator_locality_standing_through,
)
from seed_runtime.operator_command import AddressedOperatorCommand, OperatorCommandFrame
from seed_runtime.operator_checkpoint import (
    EVENT_KIND_RESPONSIBILITIES as CHECKPOINT_EVENT_KIND_RESPONSIBILITIES,
    STANDING_BOUNDARY_REFERENCE_ACT_EVIDENCE_KIND,
    STANDING_BOUNDARY_REFERENCE_RECORDED_KIND,
    STANDING_BOUNDARY_REFERENCE_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND,
    record_standing_boundary_reference_responsibility_assignment,
    record_standing_boundary_reference_responsible_act_evidence,
    record_standing_boundary_reference_result,
)
from seed_runtime.operator_representation import (
    EXACT_SOURCE_MATERIAL_REPRESENTATION_RULE,
    EVENT_KIND_RESPONSIBILITIES as REPRESENTATION_EVENT_KIND_RESPONSIBILITIES,
    REPRESENTATION_ACT_EVIDENCE_KIND,
    REPRESENTATION_EMISSION_INPUT_ROLE,
    REPRESENTATION_LOCALITY_EVIDENCE_KIND,
    REPRESENTATION_RECORDED_KIND,
    REPRESENTATION_RESPONSIBILITY,
    emit_operator_representation_material,
    record_operator_representation,
)
from seed_runtime.operator_representation_admission import (
    EVENT_KIND_RESPONSIBILITIES as REPRESENTATION_ADMISSION_EVENT_KIND_RESPONSIBILITIES,
    REPRESENTATION_CANDIDATE_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND,
    REPRESENTATION_CANDIDATE_ACT_EVIDENCE_KIND,
    REPRESENTATION_CANDIDATE_RECORDED_KIND,
    EXACT_MATERIAL_REPRESENTATION_ADMISSION_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND,
    EXACT_MATERIAL_REPRESENTATION_ADMISSION_ACT_EVIDENCE_KIND,
    EXACT_MATERIAL_REPRESENTATION_ADMISSION_RECORDED_KIND,
    exact_material_representation_rule_is_applicable_to_boundary_rule,
)
from seed_runtime.operator_egress import EXACT_MATERIAL_WRITE_BOUNDARY_RULE
from seed_runtime.operator_representation_applicability import (
    EVENT_KIND_RESPONSIBILITIES as REPRESENTATION_APPLICABILITY_EVENT_KIND_RESPONSIBILITIES,
    REPRESENTATION_EMISSION_APPLICABILITY_ACT_EVIDENCE_KIND,
    REPRESENTATION_EMISSION_APPLICABILITY_RECORDED_KIND,
)
from seed_runtime.operator_material_acquisition import (
    EVENT_KIND_RESPONSIBILITIES as ACQUIRE_EVENT_KIND_RESPONSIBILITIES,
    OPERATOR_MATERIAL_ACQUIRE_ACT_EVIDENCE_KIND,
    OPERATOR_MATERIAL_ACQUIRE_LOCALITY_RELATION_OCCURRENCE_KIND,
    OPERATOR_MATERIAL_ACQUIRE_RECORDED_KIND,
    OPERATOR_MATERIAL_ACQUIRE_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND,
    record_operator_material_acquire_responsibility_assignment,
    record_operator_material_acquire_responsible_act_evidence,
    record_operator_material_acquire_result,
    read_operator_material_acquire_locality_relation_requirements,
)
from seed_runtime.operator_system_locality import (
    EVENT_KIND_RESPONSIBILITIES as SYSTEM_LOCALITY_EVENT_KIND_RESPONSIBILITIES,
    OPERATOR_SYSTEM_LOCALITY_ACT_EVIDENCE_KIND,
    OPERATOR_SYSTEM_LOCALITY_RECORDED_KIND,
    OPERATOR_SYSTEM_LOCALITY_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND,
    record_operator_system_locality_responsibility_assignment,
    record_operator_system_locality_act_evidence,
    record_operator_system_locality_result,
)
from seed_runtime.operator_material_boundary import OperatorBoundaryMaterial
from seed_runtime.operator_standing_continuation import (
    EVENT_KIND_RESPONSIBILITIES as CONTINUATION_EVENT_KIND_RESPONSIBILITIES,
    STANDING_LOCALITY_CONTINUATION_ACT_EVIDENCE_KIND,
    STANDING_LOCALITY_CONTINUATION_RECORDED_KIND,
    STANDING_LOCALITY_CONTINUATION_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND,
    record_standing_locality_continuation_responsibility_assignment,
    record_standing_locality_continuation_responsible_act_evidence,
    record_standing_locality_continuation_result,
)
from seed_runtime.standing_boundary_locality import (
    EVENT_KIND_RESPONSIBILITIES as BOUNDARY_LOCALITY_EVENT_KIND_RESPONSIBILITIES,
    RECORDED_STANDING_BOUNDARY_LOCALITY_ACT_EVIDENCE_KIND,
    RECORDED_STANDING_BOUNDARY_LOCALITY_RECORDED_KIND,
    RECORDED_STANDING_BOUNDARY_LOCALITY_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND,
    record_recorded_standing_boundary_locality_responsibility_assignment,
    record_recorded_standing_boundary_locality_responsible_act_evidence,
    record_recorded_standing_boundary_locality_result,
)
from seed_runtime.occurrence_position_measurement import (
    EVENT_KIND_RESPONSIBILITIES as POSITION_EVENT_KIND_RESPONSIBILITIES,
    MEASURED_ASSERTION_RESPONSIBILITY as POSITION_ASSERTION_RESPONSIBILITY,
    OCCURRENCE_POSITION_ACT_EVIDENCE_KIND,
    OCCURRENCE_POSITION_MEASUREMENT_RULE,
    OCCURRENCE_POSITION_RECORDED_KIND,
    OCCURRENCE_POSITION_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND,
    OCCURRENCE_POSITION_RESPONSIBILITY,
    get_occurrence_position_measurement_responsibility_assignment,
    measure_occurrence_position,
    record_occurrence_position_measurement_responsibility_assignment,
    record_occurrence_position_measurement_responsible_act_evidence,
    record_occurrence_position_measurement_result,
)
from seed_runtime.measurement_of_position_coordinates_of_byte_pair_occurrences import (
    record_byte_pair_occurrence_position_measurement_responsibility_assignment,
    record_byte_pair_occurrence_position_measurement_act_evidence,
    record_byte_pair_occurrence_position_measurement_result,
)
from seed_runtime.evidence_of_yield_relation import (
    OCCURRENCE_BOUNDARIES_OF_YIELD_RELATION,
    read_requirements_of_evidence_carried_by_result_occurrence,
    read_requirements_of_yield_relation,
)


def _record_byte_measurement(
    ledger, *, source_localities, recording_locality_identity
):
    assignment = record_byte_measurement_responsibility_assignment(
        ledger,
        source_localities=source_localities,
        recording_locality_identity=recording_locality_identity,
        locality_standing=read_operator_locality_standing(
            ledger, locality_identity=recording_locality_identity
        ),
    )
    act_evidence = record_byte_measurement_responsible_act_evidence(
        ledger,
        responsibility_assignment_event_identity=assignment.identity,
        responsibility_assignment_standing=read_operator_locality_standing(
            ledger, locality_identity=recording_locality_identity
        ),
    )
    return record_byte_measurement_result(
        ledger,
        responsible_act_evidence_event_identity=act_evidence.identity,
    )


GRAMMAR = Path(__file__).resolve().parents[1] / "book_of_seed/witness_grammar.json"
RUNTIME = Path(__file__).resolve().parents[1] / "seed_runtime"

EXACT = "exact"
INAPPLICABLE = "inapplicable"
UNKNOWN = "Unknown"
MISSING = "missing"
CONTRADICTION = "contradiction"


class _IntegrityAdversaryLedger(EventLedger):
    def __init__(self):
        super().__init__()
        self._corrupted_identities: set[str] = set()

    def mark_corrupted(self, event_identity: str) -> None:
        self._corrupted_identities.add(event_identity)

    def integrity_of(self, event_identity: str) -> str:
        if event_identity in self._corrupted_identities:
            return CORRUPTED
        return super().integrity_of(event_identity)


def _clause(clause_identity: str) -> dict:
    return json.loads(GRAMMAR.read_text(encoding="utf-8"))["clause_coordinates"][clause_identity]


def _coordinate_identities(coordinates: list[object]) -> tuple[str, ...]:
    return tuple(
        coordinate["identity"] if type(coordinate) is dict else coordinate
        for coordinate in coordinates
    )


def _witness_grammar() -> dict:
    return json.loads(GRAMMAR.read_text(encoding="utf-8"))["witness"]


def _assert_structured_relation_identities_name_their_exact_relation(value):
    if isinstance(value, dict):
        relation = value.get("relation")
        addresses = tuple(
            value[coordinate]
            for coordinate in ("identity", "subject")
            if coordinate in value
        )
        if relation is not None and addresses:
            assert type(relation) is str and relation
            for address in addresses:
                assert type(address) is str and address
                assert (
                    f"_{relation.casefold()}_"
                    in f"_{address.casefold()}_"
                ), f"{address} does not name its exact {relation} relation"
        for carried in value.values():
            _assert_structured_relation_identities_name_their_exact_relation(
                carried
            )
    elif isinstance(value, list):
        for carried in value:
            _assert_structured_relation_identities_name_their_exact_relation(
                carried
            )


def test_every_grammar_representation_composite_preserves_material_order():
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))
    assert grammar["composite"] == {
        "material_order": "preserved",
        "requires": ["exact_material", "exact_order", "exact_path"],
        "relations": {
            "of": {
                "from": "second_subject",
                "to": "first_subject",
                "coordinate": "of",
                "requires": [
                    "first_subject",
                    "second_subject",
                    "exact_order",
                ],
            }
        },
    }

    ordered: dict[frozenset[tuple[str, int]], set[tuple[str, ...]]] = {}
    structured_relations: list[dict] = []

    def carries_relation(value, expected):
        if isinstance(value, dict):
            if "relation" in value and (
                expected is None or value.get("relation") == expected
            ):
                assert value.get("first_subject")
                assert value.get("second_subject")
                return True
            return any(carries_relation(nested, expected) for nested in value.values())
        if isinstance(value, list):
            return any(carries_relation(nested, expected) for nested in value)
        return False

    def visit(value, parent=None):
        if isinstance(value, dict):
            if "relation" in value:
                assert value.get("first_subject")
                assert value.get("second_subject")
                structured_relations.append(value)
            for key, carried in value.items():
                if "_of_" in key:
                    assert carries_relation(carried, "of")
                visit(carried, value)
        elif isinstance(value, list):
            for carried in value:
                visit(carried, value)
        elif isinstance(value, str):
            words = tuple(re.findall(r"[A-Za-z]+", value.lower()))
            if len(words) > 1:
                material = frozenset(Counter(words).items())
                ordered.setdefault(material, set()).add(words)
            if "_of_" in value:
                assert parent is not None
                assert carries_relation(parent, "of")

    visit(grammar)
    _assert_structured_relation_identities_name_their_exact_relation(grammar)
    reordered = {
        words: orders for words, orders in ordered.items() if len(orders) > 1
    }
    assert reordered == {}
    assert structured_relations
    assert any(relation["relation"] == "of" for relation in structured_relations)
    serialized = GRAMMAR.read_text(encoding="utf-8")
    assert '"Evidence_occurrence"' not in serialized
    assert '"occurrence_Evidence"' not in serialized


def test_explicit_but_wrong_relation_cannot_satisfy_a_structured_grammar_address():
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))
    assert grammar["clause_coordinates"]["01.Standing.B"]["standing_not_established"][1] == {
        "subject": "same_subject",
        "coordinates": ["material_with_same_name"],
    }
    relation_subject = next(
        coordinates
        for coordinates in grammar["clause_coordinates"]["01.Source.C"][
            "test_subjects"
        ]
        if coordinates.get("subject")
        == "measurement_result_input_to_second_measurement"
    )
    mutations = (
        grammar["clause_coordinates"]["01.Standing.B"]["standing_not_established"][3],
        relation_subject,
    )
    assert mutations[0]["identity"] == "Authority_supports_exact_Act"
    assert mutations[1]["subject"] == (
        "measurement_result_input_to_second_measurement"
    )

    for structured_relation in mutations:
        changed = json.loads(json.dumps(grammar))
        target = (
            changed["clause_coordinates"]["01.Standing.B"]["standing_not_established"][3]
            if "identity" in structured_relation
            else next(
                coordinates
                for coordinates in changed["clause_coordinates"]["01.Source.C"][
                    "test_subjects"
                ]
                if coordinates.get("subject")
                == "measurement_result_input_to_second_measurement"
            )
        )
        target["relation"] = "dances_with"
        try:
            _assert_structured_relation_identities_name_their_exact_relation(changed)
        except AssertionError as error:
            assert "does not name its exact" in str(error)
        else:
            raise AssertionError("wrong explicit relation escaped exact address")


def _content_locality_witness(
    content: dict, *, locality, occurrence_identity: str
) -> str:
    if locality is None:
        return MISSING
    return (
        EXACT
        if locality.identity == occurrence_identity and locality.material == content
        else MISSING
    )


def _assertion_locality_witness(bundle: dict, *, occurrence_identity: str) -> str:
    requirements = _assertion_locality_requirements(
        bundle, occurrence_identity=occurrence_identity
    )
    return EXACT if all(requirements.values()) else MISSING


def _assertion_locality_requirements(
    bundle: dict, *, occurrence_identity: str
) -> dict[str, bool]:
    assertion = bundle["source_assertion"]
    event = bundle["event"]
    carried = [
        item
        for item in event.material.get("assertions", [])
        if item.get("dimensions", {}).get("identity") == assertion.assertion_identity
    ]
    exact_relation = carried == [assertion.material]
    exact_occurrence = (
        event.identity == occurrence_identity
        == assertion.recorded_occurrence_identity
    )
    intact = bundle["ledger"].integrity_of(event.identity) != CORRUPTED
    return {
        "exact_relation": exact_relation,
        "occurrence_witness": exact_occurrence,
        "intact_evidence": intact,
    }


def _source_assertion():
    witness = _byte_measurement_witness()
    return witness["source_assertion"]


def _byte_measurement_witness() -> dict:
    ledger = _IntegrityAdversaryLedger()
    run_persistent_operator_console(
        ledger=ledger,
        locality_identity="source",
        input_stream=binary_input("ta\n"),
        output_stream=StringIO(),
    )
    measurement = _record_byte_measurement(
        ledger,
        source_localities=("source",),
        recording_locality_identity="byte-measurement",
    )
    assertion = next(
        item
        for item in assertions_of_recorded_byte_measurement(ledger, measurement.identity)
        if item.result == "exact_source_material_set"
    )
    return {
        "ledger": ledger,
        "event": measurement,
        "source_assertion": assertion,
        "act_evidence": ledger.get(measurement.material["responsible_act_evidence_identity"]),
        "evidence_of_yield_relation": ledger.get(measurement.material["evidence_of_yield_relation_identity"]),
    }


def _recorded_applicability() -> dict:
    # RecordedByteAssertion deliberately carries no ledger handle. Recreate the
    # live witness so every relation can be checked through its own occurrences.
    ledger = _IntegrityAdversaryLedger()
    run_persistent_operator_console(
        ledger=ledger,
        locality_identity="source",
        input_stream=binary_input("ta\n"),
        output_stream=StringIO(),
    )
    byte_measurement = _record_byte_measurement(
        ledger,
        source_localities=("source",),
        recording_locality_identity="byte-measurement",
    )
    pair_measurement = record_byte_position_pair_count_layer(
        ledger,
        source_measurement_event_identity=byte_measurement.identity,
        recording_locality_identity="measurement",
    )
    event = ledger.get(pair_measurement.material["input_applicability_event_identity"])
    read = get_recorded_pair_input_applicability(ledger, event.identity)
    movement = ledger.get(read["input_movement_event_identity"])
    return {
        "ledger": ledger,
        "applicability": read,
        "event": event,
        "act_evidence": ledger.get(event.material["responsible_act_evidence_identity"]),
        "evidence_of_yield_relation": ledger.get(event.material["evidence_of_yield_relation_identity"]),
        "movement": movement,
        "movement_act_evidence": ledger.get(
            movement.material["responsible_act_evidence_identity"]
        ),
        "movement_evidence_of_yield_relation": ledger.get(
            movement.material["evidence_of_yield_relation_identity"]
        ),
        "pair_event": pair_measurement,
        "pair_act_evidence": ledger.get(
            pair_measurement.material["responsible_act_evidence_identity"]
        ),
        "pair_evidence_of_yield_relation": ledger.get(
            pair_measurement.material["evidence_of_yield_relation_identity"]
        ),
    }


def _assertion_locality_movement_yield_witness() -> dict:
    source = _recorded_applicability()
    return {
        "ledger": source["ledger"],
        "event": source["movement"],
        "act_evidence": source["movement_act_evidence"],
        "evidence_of_yield_relation": source["movement_evidence_of_yield_relation"],
        "recorded_result_occurrence_coordinate": "movement_act_occurrence_identity",
        "act_evidence_occurrence_coordinate": "movement_act_occurrence_identity",
    }


def _emission_witness() -> dict:
    ledger = _IntegrityAdversaryLedger()
    source = ingest_material(
        ledger,
        locality_identity="emission",
        exact_bytes=b"emission",
        source_role="operator",
        source_boundary="exact source boundary",
    )
    representation = record_operator_representation(
        ledger,
        locality_identity="emission",
        locality_standing=read_operator_locality_standing(
            ledger, locality_identity="emission"
        ),
        source_occurrence_reference=source.identity,
    )
    admission, applicability, standing, boundary = admit_representation(ledger, representation)
    emit_operator_representation_material(
        ledger,
        representation=representation,
        admission_result_event_identity=admission.identity,
        applicability_result_event_identity=applicability.identity,
        locality_standing=standing,
        output_boundary=boundary,
    )
    event = ledger.get(representation["emitted_event_identity"])
    return {
        "ledger": ledger,
        "event": event,
        "attempt": ledger.get(representation["emission_attempt_event_identity"]),
        "attempt_locality_evidence": ledger.get(
            representation["emission_attempt_locality_evidence_identity"]
        ),
        "act_evidence": ledger.get(
            event.material["responsible_act_evidence_identity"]
        ),
        "locality_evidence": ledger.get(event.material["locality_evidence_identity"]),
        "evidence_of_yield_relation": ledger.get(event.material["evidence_of_yield_relation_identity"]),
    }


def _failed_boundary_yield_witness() -> dict:
    class PartialOutput(BytesIO):
        def write(self, value):
            super().write(value[:-1])
            return len(value) - 1

    ledger = _IntegrityAdversaryLedger()
    source = ingest_material(
        ledger,
        locality_identity="failed-emission",
        exact_bytes=b"failed-emission",
        source_role="operator",
        source_boundary="exact source boundary",
    )
    representation = record_operator_representation(
        ledger,
        locality_identity="failed-emission",
        locality_standing=read_operator_locality_standing(
            ledger, locality_identity="failed-emission"
        ),
        source_occurrence_reference=source.identity,
    )
    partial_output = PartialOutput()
    admission, applicability, standing, boundary = admit_representation(
        ledger, representation, output_stream=partial_output
    )
    try:
        emit_operator_representation_material(
            ledger,
            representation=representation,
            admission_result_event_identity=admission.identity,
            applicability_result_event_identity=applicability.identity,
            locality_standing=standing,
            output_boundary=boundary,
        )
    except ValueError:
        pass
    event = ledger.get(representation["boundary_failure_event_identity"])
    return _yield_bundle(ledger, event)


def _repeated_emission_attempt_witness() -> tuple[dict, dict]:
    ledger = _IntegrityAdversaryLedger()
    source = ingest_material(
        ledger,
        locality_identity="repeated-emission-attempt",
        exact_bytes=b"repeated-emission-attempt",
        source_role="operator",
        source_boundary="exact source boundary",
    )
    representation = record_operator_representation(
        ledger,
        locality_identity="repeated-emission-attempt",
        locality_standing=read_operator_locality_standing(
            ledger, locality_identity="repeated-emission-attempt"
        ),
        source_occurrence_reference=source.identity,
    )
    admission, applicability, standing, boundary = admit_representation(ledger, representation)
    emit_operator_representation_material(
        ledger,
        representation=representation,
        admission_result_event_identity=admission.identity,
        applicability_result_event_identity=applicability.identity,
        locality_standing=standing,
        output_boundary=boundary,
    )
    first_attempt = ledger.get(representation["emission_attempt_event_identity"])
    first_evidence = ledger.get(
        representation["emission_attempt_locality_evidence_identity"]
    )
    first_event = ledger.get(representation["emitted_event_identity"])
    first_act_evidence = ledger.get(
        first_event.material["responsible_act_evidence_identity"]
    )
    first_locality_evidence = ledger.get(
        first_event.material["locality_evidence_identity"]
    )
    first_evidence_of_yield_relation = ledger.get(first_event.material["evidence_of_yield_relation_identity"])
    admission, applicability, standing, second_boundary = admit_representation(
        ledger,
        representation,
        boundary_identity="second-emission-boundary",
    )
    emit_operator_representation_material(
        ledger,
        representation=representation,
        admission_result_event_identity=admission.identity,
        applicability_result_event_identity=applicability.identity,
        locality_standing=standing,
        output_boundary=second_boundary,
    )
    second_attempt = ledger.get(representation["emission_attempt_event_identity"])
    second_evidence = ledger.get(
        representation["emission_attempt_locality_evidence_identity"]
    )
    second_event = ledger.get(representation["emitted_event_identity"])
    second_act_evidence = ledger.get(
        second_event.material["responsible_act_evidence_identity"]
    )
    second_locality_evidence = ledger.get(
        second_event.material["locality_evidence_identity"]
    )
    second_evidence_of_yield_relation = ledger.get(second_event.material["evidence_of_yield_relation_identity"])
    return (
        {
            "ledger": ledger,
            "attempt": first_attempt,
            "attempt_locality_evidence": first_evidence,
            "event": first_event,
            "act_evidence": first_act_evidence,
            "locality_evidence": first_locality_evidence,
            "evidence_of_yield_relation": first_evidence_of_yield_relation,
        },
        {
            "ledger": ledger,
            "attempt": second_attempt,
            "attempt_locality_evidence": second_evidence,
            "event": second_event,
            "act_evidence": second_act_evidence,
            "locality_evidence": second_locality_evidence,
            "evidence_of_yield_relation": second_evidence_of_yield_relation,
        },
    )


def _representation_candidate_admission_yield_witnesses() -> dict[str, dict]:
    ledger = _IntegrityAdversaryLedger()
    source = ingest_material(
        ledger,
        locality_identity="representation-admission",
        exact_bytes=b"representation-admission",
        source_role="operator",
        source_boundary="exact source boundary",
    )
    representation = record_operator_representation(
        ledger,
        locality_identity="representation-admission",
        locality_standing=read_operator_locality_standing(
            ledger, locality_identity="representation-admission"
        ),
        source_occurrence_reference=source.identity,
    )
    admission, applicability, _standing, _boundary = admit_representation(ledger, representation)
    candidate = ledger.get(
        admission.material["candidate_reference"]["recorded_occurrence_identity"]
    )
    applicability_bundle = _yield_bundle(ledger, applicability)
    applicability_bundle["recorded_result_occurrence_coordinate"] = (
        "applicability_act_occurrence_identity"
    )
    applicability_bundle["act_evidence_occurrence_coordinate"] = (
        "applicability_act_occurrence_identity"
    )
    return {
        "representation_candidate": _yield_bundle(ledger, candidate),
        "representation_admission": _yield_bundle(ledger, admission),
        "representation_emission_applicability": applicability_bundle,
    }


def _representation_candidate_yield_witness() -> dict:
    return _representation_candidate_admission_yield_witnesses()[
        "representation_candidate"
    ]


def _representation_admission_yield_witness() -> dict:
    return _representation_candidate_admission_yield_witnesses()[
        "representation_admission"
    ]


def _representation_emission_applicability_yield_witness() -> dict:
    return _representation_candidate_admission_yield_witnesses()[
        "representation_emission_applicability"
    ]


def _complete_candidate_standing_yield_witnesses() -> dict[str, dict]:
    ledger = _IntegrityAdversaryLedger()
    result = record_complete_candidate_standing(
        ledger,
        recording_locality_identity="complete-candidate-standing-yield",
        source_append_boundary=ledger.append_boundary(),
    )
    applicability = ledger.get(
        result.material["applicability_result_event_identity"]
    )
    return {
        "complete_candidate_standing_applicability": _yield_bundle(
            ledger, applicability
        ),
        "complete_candidate_standing": _yield_bundle(ledger, result),
    }


def _complete_candidate_standing_applicability_yield_witness() -> dict:
    return _complete_candidate_standing_yield_witnesses()[
        "complete_candidate_standing_applicability"
    ]


def _complete_candidate_standing_yield_witness() -> dict:
    return _complete_candidate_standing_yield_witnesses()[
        "complete_candidate_standing"
    ]


def _recorded_pair_measurement_comparison_yield_witnesses() -> dict[str, dict]:
    ledger = _IntegrityAdversaryLedger()
    locality_identity = "recorded-pair-comparison-yield"
    earlier_source = ingest_material(
        ledger,
        locality_identity=locality_identity,
        exact_bytes=b"abab",
        source_role="system",
        source_boundary="earlier supplied occurrence",
    )
    earlier_measurement = _record_byte_measurement(
        ledger,
        source_localities=(locality_identity,),
        recording_locality_identity=locality_identity,
    )
    earlier_pair = record_byte_position_pair_count_layer(
        ledger,
        source_measurement_event_identity=earlier_measurement.identity,
        recording_locality_identity=locality_identity,
    )
    ingest_material(
        ledger,
        locality_identity=locality_identity,
        exact_bytes=b"abac",
        source_role="system",
        source_boundary="later supplied occurrence",
        provenance_occurrence_references=(earlier_source.identity,),
    )
    later_measurement = _record_byte_measurement(
        ledger,
        source_localities=(locality_identity,),
        recording_locality_identity=locality_identity,
    )
    later_pair = record_byte_position_pair_count_layer(
        ledger,
        source_measurement_event_identity=later_measurement.identity,
        recording_locality_identity=locality_identity,
    )
    standing = read_operator_locality_standing(
        ledger, locality_identity=locality_identity
    )
    assignment = (
        record_recorded_pair_measurement_comparison_responsibility_assignment(
            ledger,
            earlier_result_event_identity=earlier_pair.identity,
            later_result_event_identity=later_pair.identity,
            locality_standing=standing,
        )
    )
    applicability_act = (
        record_recorded_pair_measurement_comparison_applicability_act_evidence(
            ledger,
            responsibility_assignment_event_identity=assignment.identity,
            locality_standing=read_operator_locality_standing(
                ledger, locality_identity=locality_identity
            ),
        )
    )
    applicability = (
        record_recorded_pair_measurement_comparison_applicability_result(
            ledger,
            responsible_act_evidence_event_identity=applicability_act.identity,
        )
    )
    comparison_act = record_recorded_pair_measurement_comparison_act_evidence(
        ledger,
        responsibility_assignment_event_identity=assignment.identity,
        applicability_result_event_identity=applicability.identity,
        locality_standing=read_operator_locality_standing(
            ledger, locality_identity=locality_identity
        ),
    )
    comparison = record_recorded_pair_measurement_comparison_result(
        ledger, responsible_act_evidence_event_identity=comparison_act.identity
    )
    return {
        "recorded_pair_measurement_comparison_applicability": _yield_bundle(
            ledger, applicability
        ),
        "recorded_pair_measurement_comparison": _yield_bundle(ledger, comparison),
    }


def _recorded_pair_measurement_comparison_applicability_yield_witness() -> dict:
    return _recorded_pair_measurement_comparison_yield_witnesses()[
        "recorded_pair_measurement_comparison_applicability"
    ]


def _recorded_pair_measurement_comparison_yield_witness() -> dict:
    return _recorded_pair_measurement_comparison_yield_witnesses()[
        "recorded_pair_measurement_comparison"
    ]


def _ordered_relation_path_pair_finding_comparison_yield_witnesses() -> dict[str, dict]:
    from tests.test_comparison_of_ordered_relation_path_with_recorded_pair_findings import (
        _inputs,
        _record_comparison,
    )

    ledger, _earlier_source, _added, comparison, path = _inputs(
        ledger=_IntegrityAdversaryLedger()
    )
    _assignment, applicability, _act, result = _record_comparison(
        ledger, comparison, path
    )
    applicability_witness = _yield_bundle(ledger, applicability)
    applicability_witness["recorded_result_occurrence_coordinate"] = (
        "applicability_act_occurrence_identity"
    )
    applicability_witness["act_evidence_occurrence_coordinate"] = (
        "applicability_act_occurrence_identity"
    )
    return {
        "comparison_of_ordered_relation_path_with_recorded_pair_findings_applicability": applicability_witness,
        "comparison_of_ordered_relation_path_with_recorded_pair_findings_compare": _yield_bundle(
            ledger, result
        ),
    }


def _ordered_relation_path_pair_finding_comparison_applicability_yield_witness() -> dict:
    return _ordered_relation_path_pair_finding_comparison_yield_witnesses()[
        "comparison_of_ordered_relation_path_with_recorded_pair_findings_applicability"
    ]


def _ordered_relation_path_pair_finding_comparison_yield_witness() -> dict:
    return _ordered_relation_path_pair_finding_comparison_yield_witnesses()[
        "comparison_of_ordered_relation_path_with_recorded_pair_findings_compare"
    ]


def _addressed_byte_occurrence_reference_determination_yield_witnesses() -> dict[
    str, dict
]:
    from tests.test_addressed_byte_occurrence_reference_determination import (
        _record,
    )

    ledger = _IntegrityAdversaryLedger()
    recorded = _record(ledger)
    applicability = _yield_bundle(ledger, recorded["applicability"])
    applicability["recorded_result_occurrence_coordinate"] = (
        "applicability_act_occurrence_identity"
    )
    applicability["act_evidence_occurrence_coordinate"] = (
        "applicability_act_occurrence_identity"
    )
    determination = _yield_bundle(ledger, recorded["result"])
    determination["recorded_result_occurrence_coordinate"] = (
        "determination_act_occurrence_identity"
    )
    determination["act_evidence_occurrence_coordinate"] = (
        "determination_act_occurrence_identity"
    )
    return {
        "addressed_byte_occurrence_reference_determination_applicability": applicability,
        "addressed_byte_occurrence_reference_determination": determination,
    }


def _addressed_byte_occurrence_reference_determination_applicability_yield_witness() -> dict:
    return _addressed_byte_occurrence_reference_determination_yield_witnesses()[
        "addressed_byte_occurrence_reference_determination_applicability"
    ]


def _addressed_byte_occurrence_reference_determination_yield_witness() -> dict:
    return _addressed_byte_occurrence_reference_determination_yield_witnesses()[
        "addressed_byte_occurrence_reference_determination"
    ]


def _representation_witness() -> dict:
    ledger = _IntegrityAdversaryLedger()
    representation = record_operator_representation(
        ledger,
        locality_identity="representation",
        locality_standing={"through_event_occurrence_identity": None},
    )
    event = ledger.get(representation["representation_event_identity"])
    return {
        "ledger": ledger,
        "event": event,
        "act_evidence": ledger.get(event.material["responsible_act_evidence_identity"]),
        "locality_evidence": ledger.get(event.material["locality_evidence_identity"]),
        "evidence_of_yield_relation": ledger.get(event.material["evidence_of_yield_relation_identity"]),
    }


def _sourced_representation_witness() -> dict:
    ledger = _IntegrityAdversaryLedger()
    source = ingest_material(
        ledger,
        locality_identity="representation-source",
        exact_bytes=b"source material",
        source_role="operator",
        source_boundary="exact source boundary",
    )
    representation = record_operator_representation(
        ledger,
        locality_identity="representation-source",
        locality_standing=read_operator_locality_standing(
            ledger, locality_identity="representation-source"
        ),
        source_occurrence_reference=source.identity,
    )
    event = ledger.get(representation["representation_event_identity"])
    return {
        "ledger": ledger,
        "source": source,
        "event": event,
        "act_evidence": ledger.get(event.material["responsible_act_evidence_identity"]),
        "locality_evidence": ledger.get(event.material["locality_evidence_identity"]),
        "evidence_of_yield_relation": ledger.get(event.material["evidence_of_yield_relation_identity"]),
    }


def _repeated_representation_witness() -> tuple[dict, dict]:
    ledger = _IntegrityAdversaryLedger()

    def record() -> dict:
        representation = record_operator_representation(
            ledger,
            locality_identity="repeated-representation",
            locality_standing={"through_event_occurrence_identity": None},
        )
        event = ledger.get(representation["representation_event_identity"])
        return {
            "ledger": ledger,
            "event": event,
            "act_evidence": ledger.get(
                event.material["responsible_act_evidence_identity"]
            ),
            "locality_evidence": ledger.get(
                event.material["locality_evidence_identity"]
            ),
            "evidence_of_yield_relation": ledger.get(event.material["evidence_of_yield_relation_identity"]),
        }

    return record(), record()


def _occurrence_position_yield_witness() -> dict:
    ledger = _IntegrityAdversaryLedger()
    ledger.append("test.occurrence", {"material": "a"}, locality_identity="source")
    ledger.append("test.occurrence", {"material": "b"}, locality_identity="source")
    finding = measure_occurrence_position(
        ledger,
        source_locality_identity="source",
    )
    assignment = record_occurrence_position_measurement_responsibility_assignment(
        ledger,
        recording_locality_identity="measurement",
        finding=finding,
        locality_standing=read_operator_locality_standing(
            ledger, locality_identity="measurement"
        ),
    )
    act_evidence = record_occurrence_position_measurement_responsible_act_evidence(
        ledger,
        responsibility_assignment_event_identity=assignment.identity,
        responsibility_assignment_standing=read_operator_locality_standing(
            ledger, locality_identity="measurement"
        ),
    )
    event = record_occurrence_position_measurement_result(
        ledger,
        responsible_act_evidence_event_identity=act_evidence.identity,
    )
    return _yield_bundle(ledger, event)


def _byte_pair_occurrence_position_yield_witness() -> dict:
    ledger = _IntegrityAdversaryLedger()
    locality = "byte-pair-occurrence-position"
    source = ingest_material(
        ledger,
        locality_identity=locality,
        exact_bytes=b"abc",
        source_role="exact material",
        source_boundary="exact material boundary",
    )
    assignment = record_byte_pair_occurrence_position_measurement_responsibility_assignment(
        ledger,
        source_ingest_occurrence_identity=source.identity,
        locality_standing=read_operator_locality_standing(
            ledger, locality_identity=locality
        ),
    )
    act = record_byte_pair_occurrence_position_measurement_act_evidence(
        ledger,
        responsibility_assignment_event_identity=assignment.identity,
        responsibility_assignment_standing=read_operator_locality_standing(
            ledger, locality_identity=locality
        ),
    )
    event = record_byte_pair_occurrence_position_measurement_result(
        ledger,
        responsible_act_evidence_event_identity=act.identity,
    )
    return _yield_bundle(ledger, event)


def _pair_occurrence_yield_witness() -> dict:
    ledger = _IntegrityAdversaryLedger()
    locality = "pair-occurrence"
    ingest_material(
        ledger,
        locality_identity=locality,
        exact_bytes=b"abxxab",
        source_role="premise material",
        source_boundary="exact premise boundary",
    )
    byte = _record_byte_measurement(
        ledger,
        source_localities=(locality,),
        recording_locality_identity=locality,
    )
    pair = record_byte_position_pair_count_layer(
        ledger,
        source_measurement_event_identity=byte.identity,
        recording_locality_identity=locality,
    )
    recurrence = next(
        assertion
        for assertion in assertions_of_recorded_byte_position_pair_measurement(
            ledger, pair.identity
        )
        if assertion.result == "recurrence"
        and assertion.representation == (ord("a"), ord("b"))
    )
    source = ingest_material(
        ledger,
        locality_identity=locality,
        exact_bytes=b"ba---ab",
        source_role="later material",
        source_boundary="exact later boundary",
    )
    finding = measure_positions_of_recurrent_byte_pair_occurrences(
        ledger,
        pair_measurement_occurrence_identity=pair.identity,
        recurrence_assertion_identity=recurrence.assertion_identity,
        source_ingest_occurrence_identity=source.identity,
        occurrence_limit=16,
    )
    assignment = record_responsibility_assignment_for_measurement_of_recurrent_byte_pair_occurrence_position(
        ledger,
        finding=finding,
        locality_standing=read_operator_locality_standing(
            ledger, locality_identity=locality
        ),
    )
    act_evidence = record_evidence_of_act_occurrence_for_measurement_of_recurrent_byte_pair_occurrence_position(
        ledger,
        responsibility_assignment_event_identity=assignment.identity,
        responsibility_assignment_standing=read_operator_locality_standing(
            ledger, locality_identity=locality
        ),
    )
    event = record_result_of_measurement_of_recurrent_byte_pair_occurrence_position(
        ledger,
        responsible_act_evidence_event_identity=act_evidence.identity,
    )
    return _yield_bundle(ledger, event)


def _shared_position_yield_witnesses() -> dict[str, dict]:
    ledger = _IntegrityAdversaryLedger()
    locality = "shared-position"
    ingest_material(
        ledger,
        locality_identity=locality,
        exact_bytes=b"abxxabbcxxbc",
        source_role="premise material",
        source_boundary="exact premise boundary",
    )
    byte = _record_byte_measurement(
        ledger,
        source_localities=(locality,),
        recording_locality_identity=locality,
    )
    pair = record_byte_position_pair_count_layer(
        ledger,
        source_measurement_event_identity=byte.identity,
        recording_locality_identity=locality,
    )
    recurrences = {
        assertion.representation: assertion.assertion_identity
        for assertion in assertions_of_recorded_byte_position_pair_measurement(
            ledger, pair.identity
        )
        if assertion.result == "recurrence"
        and assertion.representation
        in {(ord("a"), ord("b")), (ord("b"), ord("c"))}
    }
    source = ingest_material(
        ledger,
        locality_identity=locality,
        exact_bytes=b"abc",
        source_role="later material",
        source_boundary="exact later boundary",
    )
    findings = measure_positions_for_recurrent_byte_pair_assertions(
        ledger,
        pair_measurement_occurrence_identity=pair.identity,
        recurrence_assertion_identities=(
            recurrences[(ord("a"), ord("b"))],
            recurrences[(ord("b"), ord("c"))],
        ),
        source_ingest_occurrence_identity=source.identity,
        occurrence_limit=8,
        through=ledger.append_boundary(),
    )
    results = []
    for finding in findings:
        assignment = record_responsibility_assignment_for_measurement_of_recurrent_byte_pair_occurrence_position(
            ledger,
            finding=finding,
            locality_standing=read_operator_locality_standing(
                ledger, locality_identity=locality
            ),
        )
        act = record_evidence_of_act_occurrence_for_measurement_of_recurrent_byte_pair_occurrence_position(
            ledger,
            responsibility_assignment_event_identity=assignment.identity,
            responsibility_assignment_standing=read_operator_locality_standing(
                ledger, locality_identity=locality
            ),
        )
        results.append(
            record_result_of_measurement_of_recurrent_byte_pair_occurrence_position(
                ledger,
                responsible_act_evidence_event_identity=act.identity,
            )
        )
    references = tuple(
        reference
        for result in results
        for reference in references_to_recorded_recurrent_byte_pair_occurrence_positions(
            ledger,
            result_occurrence_identity=result.identity,
        )
    )
    first = next(reference for reference in references if reference.exact_pair == b"ab")
    second = next(reference for reference in references if reference.exact_pair == b"bc")
    assignment = record_shared_position_responsibility_assignment(
        ledger,
        first_result_occurrence_identity=first.recorded_occurrence_identity,
        first_assertion_identity=first.assertion_identity,
        second_result_occurrence_identity=second.recorded_occurrence_identity,
        second_assertion_identity=second.assertion_identity,
        locality_standing=read_operator_locality_standing(
            ledger, locality_identity=locality
        ),
    )
    applicability_act = record_shared_position_applicability_act_evidence(
        ledger,
        assignment_event_identity=assignment.identity,
        locality_standing=read_operator_locality_standing(
            ledger, locality_identity=locality
        ),
    )
    applicability = record_shared_position_applicability_result(
        ledger,
        applicability_act_evidence_event_identity=applicability_act.identity,
    )
    measurement_act = record_shared_position_measurement_act_evidence(
        ledger,
        applicability_result_event_identity=applicability.identity,
        locality_standing=read_operator_locality_standing(
            ledger, locality_identity=locality
        ),
    )
    measurement = record_shared_position_measurement_result(
        ledger,
        measurement_act_evidence_event_identity=measurement_act.identity,
    )
    applicability_witness = _yield_bundle(ledger, applicability)
    applicability_witness["recorded_result_occurrence_coordinate"] = (
        "applicability_act_occurrence_identity"
    )
    applicability_witness["act_evidence_occurrence_coordinate"] = (
        "applicability_act_occurrence_identity"
    )
    return {
        "shared_pair_position_applicability": applicability_witness,
        "shared_pair_position_measurement": _yield_bundle(ledger, measurement),
    }


def _shared_position_applicability_yield_witness() -> dict:
    return _shared_position_yield_witnesses()[
        "shared_pair_position_applicability"
    ]


def _shared_position_measurement_yield_witness() -> dict:
    return _shared_position_yield_witnesses()["shared_pair_position_measurement"]


def _standing_locality_continuation_yield_witness() -> dict:
    ledger = _IntegrityAdversaryLedger()
    representation = record_operator_representation(
        ledger,
        locality_identity="standing-continuation-source",
        locality_standing={"through_event_occurrence_identity": None},
    )
    assignment = record_standing_locality_continuation_responsibility_assignment(
        ledger,
        source_locality_identity="standing-continuation-source",
        addressed_representation_event_identity=representation[
            "representation_event_identity"
        ],
    )
    assignment_standing = read_operator_locality_standing(
        ledger, locality_identity=assignment.locality_identity
    )
    act_evidence = record_standing_locality_continuation_responsible_act_evidence(
        ledger,
        responsibility_assignment_event_identity=assignment.identity,
        responsibility_assignment_standing=assignment_standing,
    )
    event = record_standing_locality_continuation_result(
        ledger,
        responsible_act_evidence_event_identity=act_evidence.identity,
    )
    return _yield_bundle(ledger, event)


def _operator_material_acquire_yield_witness() -> dict:
    ledger = _IntegrityAdversaryLedger()
    locality_identity = "operator-material-acquire"
    standing = read_operator_locality_standing(
        ledger, locality_identity=locality_identity
    )
    representation = record_operator_representation(
        ledger,
        locality_identity=locality_identity,
        locality_standing=standing,
    )
    standing = read_operator_locality_standing(
        ledger, locality_identity=locality_identity
    )
    assignment = record_operator_material_acquire_responsibility_assignment(
        ledger,
        locality_identity=locality_identity,
        addressed_representation_event_identity=representation[
            "representation_event_identity"
        ],
        locality_standing=standing,
    )
    assignment_standing = read_operator_locality_standing(
        ledger, locality_identity=locality_identity
    )
    act_evidence = record_operator_material_acquire_responsible_act_evidence(
        ledger,
        responsibility_assignment_event_identity=assignment.identity,
        responsibility_assignment_standing=assignment_standing,
    )
    event = record_operator_material_acquire_result(
        ledger,
        responsible_act_evidence_event_identity=act_evidence.identity,
        boundary_material=OperatorBoundaryMaterial(
            exact_bytes=b"\x00\xffoperator material",
            eof=False,
            material_boundary="fixture byte boundary",
            known_loss=("earlier material is not available",),
        ),
    )
    return _yield_bundle(ledger, event)


def _operator_material_acquire_locality_witness(bundle: dict) -> str:
    requirements = read_operator_material_acquire_locality_relation_requirements(
        bundle["ledger"],
        recorded_result_event_identity=bundle["event"].identity,
    )
    return EXACT if all(requirements.values()) else MISSING


def _operator_material_acquire_locality_fidelity_findings() -> dict[str, str]:
    exact = _operator_material_acquire_yield_witness()

    relation_missing = _operator_material_acquire_yield_witness()
    relation_missing["event"].material["locality_relation"]["relation"] = (
        "another relation"
    )

    alternate = _operator_material_acquire_yield_witness()
    different_occurrence = _operator_material_acquire_yield_witness()
    different_occurrence["event"].material["locality_relation"][
        "relation_occurrence_identity"
    ] = alternate["event"].identity

    evidence_not_intact = _operator_material_acquire_yield_witness()
    evidence_not_intact["ledger"].mark_corrupted(
        evidence_not_intact["event"].identity
    )

    different_relation_occurrence = _operator_material_acquire_yield_witness()
    different_relation_occurrence["ledger"].append(
        "unrelated.locality.fixture",
        {
            "first_subject": "another exact material",
            "relation": "locality",
            "second_subject": "another bounded subject",
            "relation_occurrence_identity": alternate["event"].identity,
        },
        locality_identity=different_relation_occurrence["event"].locality_identity,
    )

    return {
        "exact": _operator_material_acquire_locality_witness(exact),
        "relation_missing": _operator_material_acquire_locality_witness(
            relation_missing
        ),
        "different_occurrence": _operator_material_acquire_locality_witness(
            different_occurrence
        ),
        "evidence_not_intact": _operator_material_acquire_locality_witness(
            evidence_not_intact
        ),
        "different_relation_occurrence": (
            _operator_material_acquire_locality_witness(
                different_relation_occurrence
            )
        ),
    }


def _standing_boundary_reference_yield_witness() -> dict:
    ledger = _IntegrityAdversaryLedger()
    locality_identity = "standing-boundary-reference"
    standing = read_operator_locality_standing(
        ledger, locality_identity=locality_identity
    )
    representation = record_operator_representation(
        ledger,
        locality_identity=locality_identity,
        locality_standing=standing,
    )
    standing = read_operator_locality_standing(
        ledger, locality_identity=locality_identity
    )
    addressed = AddressedOperatorCommand(
        command_identity=new_identity("operator_command"),
        locality_identity=locality_identity,
        addressed_at_representation_event_identity=representation[
            "representation_event_identity"
        ],
        frame=OperatorCommandFrame(
            exact_bytes=b"/checkpoint\n",
            name=b"checkpoint",
            arguments=b"",
        ),
    )
    assignment = record_standing_boundary_reference_responsibility_assignment(
        ledger,
        addressed_command=addressed,
        locality_standing=standing,
    )
    assignment_standing = read_operator_locality_standing(
        ledger, locality_identity=locality_identity
    )
    act = record_standing_boundary_reference_responsible_act_evidence(
        ledger,
        responsibility_assignment_event_identity=assignment.identity,
        responsibility_assignment_standing=assignment_standing,
    )
    event = record_standing_boundary_reference_result(
        ledger, responsible_act_evidence_event_identity=act.identity
    )
    return _yield_bundle(ledger, event)


def _operator_system_locality_yield_witness() -> dict:
    ledger = _IntegrityAdversaryLedger()
    locality_identity = "operator-invocation-locality"
    command = ingest_material(
        ledger,
        locality_identity=locality_identity,
        exact_bytes=b"!pytest\n",
        source_role="operator",
        source_boundary="operator boundary",
    )
    assignment = record_operator_system_locality_responsibility_assignment(
        ledger,
        operator_material_occurrence_reference=command.identity,
        operator_locality_standing=read_operator_locality_standing(
            ledger, locality_identity=locality_identity
        ),
    )
    act = record_operator_system_locality_act_evidence(
        ledger,
        responsibility_assignment_event_identity=assignment.identity,
        responsibility_assignment_standing=read_operator_locality_standing(
            ledger, locality_identity=assignment.locality_identity
        ),
    )
    event = record_operator_system_locality_result(
        ledger, responsible_act_evidence_event_identity=act.identity
    )
    return _yield_bundle(ledger, event)


def _recorded_standing_boundary_locality_yield_witness() -> dict:
    ledger = _IntegrityAdversaryLedger()
    locality_identity = "recorded-standing-boundary-locality"
    standing = read_operator_locality_standing(
        ledger, locality_identity=locality_identity
    )
    representation = record_operator_representation(
        ledger,
        locality_identity=locality_identity,
        locality_standing=standing,
    )
    standing = read_operator_locality_standing(
        ledger, locality_identity=locality_identity
    )
    addressed = AddressedOperatorCommand(
        command_identity=new_identity("operator_command"),
        locality_identity=locality_identity,
        addressed_at_representation_event_identity=representation[
            "representation_event_identity"
        ],
        frame=OperatorCommandFrame(
            exact_bytes=b"/checkpoint\n",
            name=b"checkpoint",
            arguments=b"",
        ),
    )
    anchor_assignment = record_standing_boundary_reference_responsibility_assignment(
        ledger,
        addressed_command=addressed,
        locality_standing=standing,
    )
    anchor_act = record_standing_boundary_reference_responsible_act_evidence(
        ledger,
        responsibility_assignment_event_identity=anchor_assignment.identity,
        responsibility_assignment_standing=read_operator_locality_standing(
            ledger, locality_identity=locality_identity
        ),
    )
    record_standing_boundary_reference_result(
        ledger, responsible_act_evidence_event_identity=anchor_act.identity
    )
    relation_assignment = (
        record_recorded_standing_boundary_locality_responsibility_assignment(
            ledger,
            source_locality_standing=read_operator_locality_standing(
                ledger, locality_identity=locality_identity
            ),
        )
    )
    relation_act = (
        record_recorded_standing_boundary_locality_responsible_act_evidence(
            ledger,
            responsibility_assignment_event_identity=relation_assignment.identity,
            responsibility_assignment_standing=read_operator_locality_standing(
                ledger, locality_identity=relation_assignment.locality_identity
            ),
        )
    )
    event = record_recorded_standing_boundary_locality_result(
        ledger,
        responsible_act_evidence_event_identity=relation_act.identity,
    )
    return _yield_bundle(ledger, event)


def _yield_bundle(ledger, event) -> dict:
    act_evidence_identity = event.material.get("responsible_act_evidence_identity")
    locality_evidence_identity = event.material.get("locality_evidence_identity")
    return {
        "ledger": ledger,
        "event": event,
        "act_evidence": (
            ledger.get(act_evidence_identity) if isinstance(act_evidence_identity, str) else None
        ),
        "evidence_of_yield_relation": ledger.get(event.material["evidence_of_yield_relation_identity"]),
        "locality_evidence": (
            ledger.get(locality_evidence_identity)
            if isinstance(locality_evidence_identity, str)
            else None
        ),
    }


def _material_ingest_yield_witness() -> dict:
    ledger = _IntegrityAdversaryLedger()
    event = ingest_material(
        ledger,
        locality_identity="material-ingest-yield",
        exact_bytes=b"\x00\xffmaterial\n",
        source_role="system",
        source_boundary="supplied byte boundary",
    )
    return _yield_bundle(ledger, event)


def _byte_measurement_result_has_exact_standing(ledger, event) -> bool:
    if (
        event is None
        or event.kind != BYTE_MEASUREMENT_RECORDED_KIND
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        return False
    try:
        assertions_of_recorded_byte_measurement(ledger, event.identity)
        standing = read_operator_locality_standing(
            ledger, locality_identity=event.locality_identity
        )
    except (TypeError, ValueError):
        return False
    return standing.get("measurement_occurrences", {}).get(event.identity) == {
        "recorded_occurrence_identity": event.identity,
        "result_identity": event.material.get("result_identity"),
        "act_occurrence_identity": event.material.get("act_occurrence_identity"),
        "responsible_act_evidence_identity": event.material.get(
            "responsible_act_evidence_identity"
        ),
        "evidence_of_yield_relation_identity": event.material.get(
            "evidence_of_yield_relation_identity"
        ),
    }


def _assertion_witness(bundle: dict) -> dict[str, str]:
    ledger = bundle["ledger"]
    assertion = bundle["source_assertion"]
    event = bundle["event"]
    evidence_of_yield_relation = bundle["evidence_of_yield_relation"]
    material = assertion.material
    dimensions = material["dimensions"]
    expected_identity = _identity(
        result=material["result"],
        subject=material["assertion_subject"],
        scope=material["assertion_scope"],
        content=dimensions["content"],
    )
    carried_assertion = next(
        (
            item
            for item in event.material["assertions"]
            if item["dimensions"]["identity"] == assertion.assertion_identity
        ),
        None,
    )
    evidence_relation = (
        assertion.recorded_occurrence_identity == event.identity
        and carried_assertion == material
        and evidence_of_yield_relation is not None
        and event.material.get("evidence_of_yield_relation_identity") == evidence_of_yield_relation.identity
        and "assertions" in evidence_of_yield_relation.material.get("coordinates_of_carried_result", [])
    )
    return {
        "identity": (
            EXACT if dimensions.get("identity") == expected_identity else CONTRADICTION
        ),
        "Evidence": EXACT if evidence_relation else MISSING,
        "provenance": EXACT if dimensions.get("source_provenance") else MISSING,
        "Scope": EXACT if material.get("assertion_scope") else MISSING,
        "Authority": EXACT if dimensions.get("authority") else MISSING,
        "conflicts": UNKNOWN if material.get("conflicts") == "Unknown" else MISSING,
        "limits": EXACT if material.get("limits") else MISSING,
        "Unknown": EXACT if material.get("unknown") else MISSING,
        "Standing": (
            EXACT
            if evidence_relation
            and _byte_measurement_result_has_exact_standing(ledger, event)
            else MISSING
        ),
    }


def _applicability_witness(bundle: dict) -> dict[str, str]:
    applicability = bundle["applicability"]
    event = bundle["event"]
    act_evidence = bundle["act_evidence"]
    evidence_of_yield_relation = bundle["evidence_of_yield_relation"]
    content = applicability["dimensions"]["content"]
    treatment = applicability["coordinate_treatment"]
    input_relation = (
        act_evidence is not None
        and event.material.get("input_assertion_reference")
        == applicability.get("input_assertion_reference")
        == act_evidence.material.get("input_assertion_reference")
    )
    act_relation = (
        act_evidence is not None
        and event.material.get("addressed_act_identity")
        == applicability.get("addressed_act_identity")
        == act_evidence.material.get("addressed_act_identity")
    )
    occurrence_relation = (
        act_evidence is not None
        and event.material.get("applicability_act_occurrence_identity")
        == applicability.get("applicability_act_occurrence_identity")
        == act_evidence.material.get("applicability_act_occurrence_identity")
    )
    carried_result = (
        evidence_of_yield_relation is not None
        and event.material.get("evidence_of_yield_relation_identity") == evidence_of_yield_relation.identity
        and event.material["dimensions"].get("standing")
        == applicability["dimensions"].get("standing")
    )
    return {
        "input_identity": EXACT if input_relation else MISSING,
        "exact_Act": EXACT if act_relation else MISSING,
        "subject": EXACT if content.get("addressed_act") else MISSING,
        "result_boundary": EXACT if applicability.get("result_boundary") else MISSING,
        "Scope": EXACT if applicability.get("scope_locality") else MISSING,
        "locality": EXACT if applicability.get("measurement_locality") else MISSING,
        "Authority": EXACT if applicability["dimensions"].get("authority") else MISSING,
        # The relation subjects already carry the exact input role and the
        # exact addressed-Act role; no extra participant noun is supplied.
        "participants_and_roles": EXACT if input_relation and act_relation else MISSING,
        "provenance": (
            EXACT
            if applicability["dimensions"].get("source_provenance")
            else MISSING
        ),
        "Standing": (
            EXACT if carried_result else MISSING
        ),
        "support_relation_Standing": (
            INAPPLICABLE
            if treatment.get("support_relation_standing", {}).get("treatment")
            == "not established by Applicability"
            else MISSING
        ),
        "current_Standing": (
            INAPPLICABLE
            if treatment.get("current_Standing", {}).get("treatment")
            == "not required for this historical bounded source material"
            else MISSING
        ),
        "occurrence_identity": (
            EXACT if occurrence_relation else MISSING
        ),
        "known_loss": (
            UNKNOWN
            if treatment.get("known_loss", {}).get("treatment")
            == "not represented by input"
            else MISSING
        ),
        "conflicts": EXACT if "conflicts" in applicability else MISSING,
        "Unknown": EXACT if applicability.get("unknown") else MISSING,
        "negative_Authority": (
            EXACT if treatment.get("negative_authority") else MISSING
        ),
    }


def _occurrence_result_witness(bundle: dict) -> str:
    requirements = _occurrence_result_requirements(bundle)
    return EXACT if all(requirements.values()) else MISSING


def _occurrences_of_result_under_pressure(bundle: dict):
    ledger = bundle["ledger"]
    evidence_of_yield_relation = bundle["evidence_of_yield_relation"]
    responsible_act_evidence = bundle.get("act_evidence")

    def record_if_supplied_representation_changed(event):
        if event is None:
            return None
        recorded = ledger.get(event.identity)
        if recorded == event:
            return event.identity
        recorded = deepcopy(event)
        object.__setattr__(
            recorded, "identity", new_identity("yield_relation_pressure")
        )
        ledger.append_many([recorded])
        return recorded.identity

    responsible_act_evidence_identity = record_if_supplied_representation_changed(
        responsible_act_evidence
    )
    if (
        evidence_of_yield_relation is not None
        and responsible_act_evidence is not None
        and responsible_act_evidence_identity is not None
        and responsible_act_evidence_identity != responsible_act_evidence.identity
        and evidence_of_yield_relation.material.get("responsible_act_evidence_identity")
        == responsible_act_evidence.identity
    ):
        evidence_of_yield_relation = deepcopy(evidence_of_yield_relation)
        evidence_of_yield_relation.material["responsible_act_evidence_identity"] = (
            responsible_act_evidence_identity
        )
    evidence_of_yield_relation_identity = record_if_supplied_representation_changed(evidence_of_yield_relation)

    event = deepcopy(bundle["event"])
    if (
        evidence_of_yield_relation is not None
        and evidence_of_yield_relation_identity != evidence_of_yield_relation.identity
        and event.material.get("evidence_of_yield_relation_identity") == evidence_of_yield_relation.identity
    ):
        event.material["evidence_of_yield_relation_identity"] = evidence_of_yield_relation_identity
    if (
        responsible_act_evidence is not None
        and responsible_act_evidence_identity != responsible_act_evidence.identity
        and event.material.get("responsible_act_evidence_identity")
        == responsible_act_evidence.identity
    ):
        event.material["responsible_act_evidence_identity"] = (
            responsible_act_evidence_identity
        )
    event_identity = record_if_supplied_representation_changed(event)

    return (
        ledger,
        event_identity,
        evidence_of_yield_relation_identity,
        responsible_act_evidence_identity,
    )


def _occurrence_result_requirements(bundle: dict) -> dict[str, bool]:
    (
        ledger,
        event_identity,
        evidence_of_yield_relation_identity,
        responsible_act_evidence_identity,
    ) = _occurrences_of_result_under_pressure(bundle)

    return read_requirements_of_yield_relation(
        ledger,
        recorded_result_event_identity=event_identity,
        evidence_of_yield_relation_event_identity=evidence_of_yield_relation_identity,
        responsible_act_evidence_event_identity=responsible_act_evidence_identity,
        recorded_result_occurrence_coordinate=bundle.get(
            "recorded_result_occurrence_coordinate", "act_occurrence_identity"
        ),
        responsible_act_occurrence_coordinate=bundle.get(
            "act_evidence_occurrence_coordinate", "act_occurrence_identity"
        ),
    )


def _evidence_carried_by_result_occurrence_witness(bundle: dict) -> str:
    requirements = _evidence_carried_by_result_occurrence_requirements(bundle)
    return EXACT if all(requirements.values()) else MISSING


def _evidence_carried_by_result_occurrence_requirements(
    bundle: dict,
) -> dict[str, bool]:
    (
        ledger,
        event_identity,
        evidence_of_yield_relation_identity,
        _responsible_act_evidence_identity,
    ) = _occurrences_of_result_under_pressure(bundle)
    return read_requirements_of_evidence_carried_by_result_occurrence(
        ledger,
        recorded_result_event_identity=event_identity,
        evidence_of_yield_relation_event_identity=(
            evidence_of_yield_relation_identity
        ),
        recorded_result_occurrence_coordinate=bundle.get(
            "recorded_result_occurrence_coordinate", "act_occurrence_identity"
        ),
    )


def _emission_locality_witness(bundle: dict) -> str:
    requirements = _emission_locality_requirements(bundle)
    return EXACT if all(requirements.values()) else MISSING


def _emission_locality_requirements(bundle: dict) -> dict[str, bool]:
    event = bundle["event"]
    evidence = bundle["locality_evidence"]
    if evidence is None:
        return {
            "exact_relation": False,
            "occurrence_witness": False,
            "intact_evidence": False,
        }
    event_relation = event.material.get("locality_relation")
    evidence_relation = evidence.material.get("locality_relation")
    exact_relation = bool(
        isinstance(event_relation, dict)
        and isinstance(evidence_relation, dict)
        and event_relation.get("first_subject")
        == evidence_relation.get("first_subject")
        == event.material.get("representation_reference")
        == evidence.material.get("representation_reference")
        and event_relation.get("second_subject")
        == evidence_relation.get("second_subject")
        == event.material.get("act_occurrence_identity")
        == evidence.material.get("act_occurrence_identity")
        and event.material.get("representation_event_identity")
        == evidence.material.get("representation_event_identity")
        and type(event.exact_material) is bytes
        and event.exact_material == evidence.exact_material
    )
    exact_occurrence = bool(
        isinstance(event_relation, dict)
        and isinstance(evidence_relation, dict)
        and event_relation.get("relation_occurrence_identity")
        == evidence_relation.get("relation_occurrence_identity")
    )
    evidence_is_carried = event.material.get("locality_evidence_identity") == evidence.identity
    return {
        "exact_relation": exact_relation and evidence_is_carried,
        "occurrence_witness": exact_occurrence,
        "intact_evidence": (
            bundle["ledger"].integrity_of(evidence.identity) != CORRUPTED
        ),
    }


def _emission_attempt_locality_witness(bundle: dict) -> str:
    requirements = _emission_attempt_locality_requirements(bundle)
    return EXACT if all(requirements.values()) else MISSING


def _emission_attempt_locality_requirements(bundle: dict) -> dict[str, bool]:
    attempt = bundle["attempt"]
    evidence = bundle["attempt_locality_evidence"]
    if evidence is None:
        return {
            "exact_relation": False,
            "occurrence_witness": False,
            "intact_evidence": False,
        }
    exact_relation = (
        type(attempt.exact_material) is bytes
        and attempt.exact_material == evidence.exact_material
    )
    exact_occurrence = attempt.identity == evidence.material.get("attempt_event_identity")
    exact_subject = (
        attempt.material.get("representation_reference")
        == evidence.material.get("representation_reference")
    )
    return {
        "exact_relation": exact_relation and exact_subject,
        "occurrence_witness": exact_occurrence,
        "intact_evidence": (
            bundle["ledger"].integrity_of(evidence.identity) != CORRUPTED
        ),
    }


def _emission_participation_witness(bundle: dict) -> str:
    requirements = _emission_participation_requirements(bundle)
    return EXACT if all(requirements.values()) else MISSING


def _emission_participation_requirements(bundle: dict) -> dict[str, bool]:
    event = bundle["event"]
    evidence = bundle["act_evidence"]
    if evidence is None:
        return {
            "exact_relation": False,
            "occurrence_witness": False,
            "intact_evidence": False,
        }
    exact_relation = (
        event.material.get("representation_reference")
        == evidence.material.get("representation_reference")
        and event.material.get("input_role")
        == evidence.material.get("input_role")
        == REPRESENTATION_EMISSION_INPUT_ROLE
    )
    exact_occurrence = (
        event.material.get("act_occurrence_identity")
        == evidence.material.get("act_occurrence_identity")
    )
    evidence_is_carried = (
        event.material.get("responsible_act_evidence_identity") == evidence.identity
    )
    return {
        "exact_relation": exact_relation and evidence_is_carried,
        "occurrence_witness": exact_occurrence,
        "intact_evidence": (
            bundle["ledger"].integrity_of(evidence.identity) != CORRUPTED
        ),
    }


def _representation_locality_witness(bundle: dict) -> str:
    requirements = _representation_locality_requirements(bundle)
    return EXACT if all(requirements.values()) else MISSING


def _representation_locality_requirements(bundle: dict) -> dict[str, bool]:
    event = bundle["event"]
    evidence = bundle["locality_evidence"]
    if evidence is None:
        return {
            "exact_relation": False,
            "occurrence_witness": False,
            "intact_evidence": False,
        }
    content = evidence.material.get("carried_content")
    exact_content = isinstance(content, dict) and all(
        event.material.get(key) == value for key, value in content.items()
    )
    exact_occurrence = (
        event.material.get("act_occurrence_identity")
        == evidence.material.get("act_occurrence_identity")
    )
    evidence_is_carried = event.material.get("locality_evidence_identity") == evidence.identity
    return {
        "exact_relation": exact_content and evidence_is_carried,
        "occurrence_witness": exact_occurrence,
        "intact_evidence": (
            bundle["ledger"].integrity_of(evidence.identity) != CORRUPTED
        ),
    }


def _relation_fidelity_findings() -> dict[str, dict[str, str]]:
    locality = _byte_measurement_witness()
    alternate_locality = _byte_measurement_witness()
    corrupted_locality = _byte_measurement_witness()
    corrupted_locality["ledger"].mark_corrupted(corrupted_locality["event"].identity)
    missing_locality = dict(locality)
    missing_event = deepcopy(locality["event"])
    missing_event.material["assertions"] = [
        item
        for item in missing_event.material["assertions"]
        if item["dimensions"]["identity"]
        != locality["source_assertion"].assertion_identity
    ]
    missing_locality["event"] = missing_event
    unrelated_locality = dict(locality)
    unrelated_event = deepcopy(locality["event"])
    unrelated_event.material["evidence_of_yield_relation_identity"] = "other-yield-evidence"
    unrelated_locality["event"] = unrelated_event

    participation = _recorded_applicability()
    alternate_participation = _recorded_applicability()
    corrupted_participation = _recorded_applicability()
    corrupted_participation["ledger"].mark_corrupted(
        corrupted_participation["pair_act_evidence"].identity
    )
    missing_participation = dict(participation)
    missing_participation_evidence = deepcopy(participation[
        "pair_act_evidence"
    ])
    missing_participation_evidence.material["input_role"] = "different-role"
    missing_participation["pair_act_evidence"] = missing_participation_evidence
    wrong_participation = dict(participation)
    wrong_participation_evidence = deepcopy(participation[
        "pair_act_evidence"
    ])
    wrong_participation_evidence.material["act_occurrence_identity"] = (
        alternate_participation["pair_event"].material["act_occurrence_identity"]
    )
    wrong_participation["pair_act_evidence"] = wrong_participation_evidence
    unrelated_participation = dict(participation)
    unrelated_participation_event = deepcopy(participation["pair_event"])
    unrelated_participation_event.material["evidence_of_yield_relation_identity"] = (
        "other-yield-evidence"
    )
    unrelated_participation["pair_event"] = unrelated_participation_event

    exact_yield = _byte_measurement_witness()
    alternate_yield = _byte_measurement_witness()
    corrupted_yield = _byte_measurement_witness()
    corrupted_yield["ledger"].mark_corrupted(
        corrupted_yield["evidence_of_yield_relation"].identity
    )
    missing_yield = dict(exact_yield)
    missing_yield_event = deepcopy(exact_yield["event"])
    missing_yield_event.material["evidence_of_yield_relation_identity"] = (
        "missing-yield-evidence"
    )
    missing_yield["event"] = missing_yield_event
    wrong_yield = dict(exact_yield)
    wrong_yield_act_evidence = deepcopy(exact_yield["act_evidence"])
    wrong_evidence_of_yield_relation = deepcopy(exact_yield["evidence_of_yield_relation"])
    alternate_yield_occurrence = alternate_yield["event"].material[
        "act_occurrence_identity"
    ]
    wrong_yield_act_evidence.material["act_occurrence_identity"] = (
        alternate_yield_occurrence
    )
    wrong_evidence_of_yield_relation.material["dimensions"]["act_occurrence_identity"] = (
        alternate_yield_occurrence
    )
    wrong_yield["act_evidence"] = wrong_yield_act_evidence
    wrong_yield["evidence_of_yield_relation"] = wrong_evidence_of_yield_relation
    unrelated_yield = dict(exact_yield)
    unrelated_yield_event = deepcopy(exact_yield["event"])
    unrelated_yield_event.material["occurrence_preservation"] = (
        "different neighboring locality coordinate"
    )
    unrelated_yield["event"] = unrelated_yield_event

    return {
        "locality": {
            "exact": _assertion_locality_witness(
                locality,
                occurrence_identity=locality["event"].identity,
            ),
            "relation_missing": _assertion_locality_witness(
                missing_locality,
                occurrence_identity=locality["event"].identity,
            ),
            "different_occurrence": _assertion_locality_witness(
                locality,
                occurrence_identity=alternate_locality["event"].identity,
            ),
            "evidence_not_intact": _assertion_locality_witness(
                corrupted_locality,
                occurrence_identity=corrupted_locality["event"].identity,
            ),
            "different_relation_occurrence": _assertion_locality_witness(
                unrelated_locality,
                occurrence_identity=locality["event"].identity,
            ),
        },
        "participation": {
            "exact": _participation_witness(
                participation, role=BYTE_PAIR_INPUT_ROLE
            ),
            "relation_missing": _participation_witness(
                missing_participation, role=BYTE_PAIR_INPUT_ROLE
            ),
            "different_occurrence": _participation_witness(
                wrong_participation, role=BYTE_PAIR_INPUT_ROLE
            ),
            "evidence_not_intact": _participation_witness(
                corrupted_participation, role=BYTE_PAIR_INPUT_ROLE
            ),
            "different_relation_occurrence": _participation_witness(
                unrelated_participation, role=BYTE_PAIR_INPUT_ROLE
            ),
        },
        "yield": {
            "exact": _occurrence_result_witness(exact_yield),
            "relation_missing": _occurrence_result_witness(missing_yield),
            "different_occurrence": _occurrence_result_witness(wrong_yield),
            "evidence_not_intact": _occurrence_result_witness(corrupted_yield),
            "different_relation_occurrence": _occurrence_result_witness(unrelated_yield),
        },
        "carried_by": {
            "exact": _evidence_carried_by_result_occurrence_witness(
                exact_yield
            ),
            "relation_missing": (
                _evidence_carried_by_result_occurrence_witness(missing_yield)
            ),
            "different_occurrence": (
                _evidence_carried_by_result_occurrence_witness(wrong_yield)
            ),
            "evidence_not_intact": (
                _evidence_carried_by_result_occurrence_witness(
                    corrupted_yield
                )
            ),
            "different_relation_occurrence": (
                _evidence_carried_by_result_occurrence_witness(
                    unrelated_yield
                )
            ),
        },
    }


def _successful_emission_requirement_bundles() -> dict[str, dict[str, dict]]:
    emission, alternate = _repeated_emission_attempt_witness()

    missing_locality = dict(emission)
    missing_locality_evidence = deepcopy(emission["locality_evidence"])
    object.__setattr__(
        missing_locality_evidence, "exact_material", b"different material"
    )
    missing_locality["locality_evidence"] = missing_locality_evidence
    wrong_locality = dict(emission)
    wrong_locality_evidence = deepcopy(emission["locality_evidence"])
    wrong_locality_evidence.material["locality_relation"][
        "relation_occurrence_identity"
    ] = alternate["locality_evidence"].material["locality_relation"][
        "relation_occurrence_identity"
    ]
    wrong_locality["locality_evidence"] = wrong_locality_evidence
    unrelated_locality = dict(emission)
    unrelated_locality_event = deepcopy(emission["event"])
    unrelated_locality_event.material["evidence_of_yield_relation_identity"] = "other-yield-evidence"
    unrelated_locality["event"] = unrelated_locality_event
    corrupted_locality = _emission_witness()
    corrupted_locality["ledger"].mark_corrupted(
        corrupted_locality["locality_evidence"].identity
    )

    missing_participation = dict(emission)
    missing_act_evidence = deepcopy(emission["act_evidence"])
    missing_act_evidence.material["input_role"] = "different-role"
    missing_participation["act_evidence"] = missing_act_evidence
    wrong_participation = dict(emission)
    wrong_participation_event = deepcopy(emission["event"])
    wrong_participation_event.material["responsible_act_evidence_identity"] = alternate[
        "act_evidence"
    ].identity
    wrong_participation["event"] = wrong_participation_event
    wrong_participation["act_evidence"] = alternate["act_evidence"]
    unrelated_participation = dict(emission)
    unrelated_participation_event = deepcopy(emission["event"])
    unrelated_participation_event.material["locality_evidence_identity"] = (
        "other-locality-evidence"
    )
    unrelated_participation["event"] = unrelated_participation_event
    corrupted_participation = _emission_witness()
    corrupted_participation["ledger"].mark_corrupted(
        corrupted_participation["act_evidence"].identity
    )

    missing_yield = dict(emission)
    missing_yield_event = deepcopy(emission["event"])
    missing_yield_event.material["evidence_of_yield_relation_identity"] = (
        "missing-yield-evidence"
    )
    missing_yield["event"] = missing_yield_event
    wrong_yield = dict(emission)
    wrong_yield_event = deepcopy(emission["event"])
    wrong_yield_event.material["responsible_act_evidence_identity"] = alternate[
        "act_evidence"
    ].identity
    wrong_yield_event.material["evidence_of_yield_relation_identity"] = alternate[
        "evidence_of_yield_relation"
    ].identity
    wrong_yield_event.material["result_identity"] = alternate[
        "event"
    ].material["result_identity"]
    wrong_yield["event"] = wrong_yield_event
    wrong_yield["act_evidence"] = alternate["act_evidence"]
    wrong_yield["evidence_of_yield_relation"] = alternate["evidence_of_yield_relation"]
    unrelated_yield = dict(emission)
    unrelated_yield_event = deepcopy(emission["event"])
    unrelated_yield_event.material["input_role"] = "other-role"
    unrelated_yield["event"] = unrelated_yield_event
    corrupted_yield = _emission_witness()
    corrupted_yield["ledger"].mark_corrupted(
        corrupted_yield["evidence_of_yield_relation"].identity
    )
    return {
        "locality": {
            "exact": emission,
            "relation_missing": missing_locality,
            "different_occurrence": wrong_locality,
            "evidence_not_intact": corrupted_locality,
            "different_relation_occurrence": unrelated_locality,
        },
        "participation": {
            "exact": emission,
            "relation_missing": missing_participation,
            "different_occurrence": wrong_participation,
            "evidence_not_intact": corrupted_participation,
            "different_relation_occurrence": unrelated_participation,
        },
        "yield": {
            "exact": emission,
            "relation_missing": missing_yield,
            "different_occurrence": wrong_yield,
            "evidence_not_intact": corrupted_yield,
            "different_relation_occurrence": unrelated_yield,
        },
        "carried_by": {
            "exact": emission,
            "relation_missing": missing_yield,
            "different_occurrence": wrong_yield,
            "evidence_not_intact": corrupted_yield,
            "different_relation_occurrence": unrelated_yield,
        },
    }


def _emission_relation_fidelity_findings() -> dict[str, dict[str, str]]:
    bundles = _successful_emission_requirement_bundles()
    witnesses = {
        "locality": _emission_locality_witness,
        "participation": _emission_participation_witness,
        "yield": _occurrence_result_witness,
        "carried_by": _evidence_carried_by_result_occurrence_witness,
    }
    return {
        relation: {
            treatment: witnesses[relation](bundle)
            for treatment, bundle in relation_bundles.items()
        }
        for relation, relation_bundles in bundles.items()
    }


def _yield_requirement_bundles(
    exact: dict,
    alternate: dict,
    corrupted: dict,
    *,
    unrelated_value,
) -> dict[str, dict]:
    missing = dict(exact)
    missing_event = deepcopy(exact["event"])
    missing_event.material["evidence_of_yield_relation_identity"] = "missing-yield-evidence"
    missing["event"] = missing_event

    different_occurrence = dict(exact)
    wrong_act_evidence = (
        deepcopy(exact["act_evidence"])
        if exact.get("act_evidence") is not None
        else None
    )
    wrong_evidence_of_yield_relation = deepcopy(exact["evidence_of_yield_relation"])
    recorded_result_occurrence_coordinate = exact.get(
        "recorded_result_occurrence_coordinate", "act_occurrence_identity"
    )
    act_evidence_occurrence_coordinate = exact.get(
        "act_evidence_occurrence_coordinate", "act_occurrence_identity"
    )
    alternate_occurrence = alternate["event"].material[
        recorded_result_occurrence_coordinate
    ]
    if wrong_act_evidence is not None:
        wrong_act_evidence.material[act_evidence_occurrence_coordinate] = (
            alternate_occurrence
        )
    wrong_evidence_of_yield_relation.material["dimensions"]["act_occurrence_identity"] = (
        alternate_occurrence
    )
    if wrong_act_evidence is not None:
        different_occurrence["act_evidence"] = wrong_act_evidence
    different_occurrence["evidence_of_yield_relation"] = wrong_evidence_of_yield_relation

    unrelated = dict(exact)
    unrelated_event = deepcopy(exact["event"])
    object.__setattr__(unrelated_event, "identity", unrelated_value)
    unrelated["event"] = unrelated_event

    corrupted["ledger"].mark_corrupted(corrupted["evidence_of_yield_relation"].identity)
    return {
        "exact": exact,
        "relation_missing": missing,
        "different_occurrence": different_occurrence,
        "evidence_not_intact": corrupted,
        "different_relation_occurrence": unrelated,
    }


def _byte_pair_yield_requirement_bundles() -> dict[str, dict[str, dict]]:
    applicability = _recorded_applicability()
    alternate_applicability = _recorded_applicability()
    corrupted_applicability = _recorded_applicability()
    for bundle in (
        applicability,
        alternate_applicability,
        corrupted_applicability,
    ):
        bundle["recorded_result_occurrence_coordinate"] = (
            "applicability_act_occurrence_identity"
        )
        bundle["act_evidence_occurrence_coordinate"] = (
            "applicability_act_occurrence_identity"
        )

    pair = {
        "ledger": applicability["ledger"],
        "event": applicability["pair_event"],
        "act_evidence": applicability["pair_act_evidence"],
        "evidence_of_yield_relation": applicability["pair_evidence_of_yield_relation"],
    }
    alternate_pair = {
        "ledger": alternate_applicability["ledger"],
        "event": alternate_applicability["pair_event"],
        "act_evidence": alternate_applicability["pair_act_evidence"],
        "evidence_of_yield_relation": alternate_applicability["pair_evidence_of_yield_relation"],
    }
    corrupted_pair_source = _recorded_applicability()
    corrupted_pair = {
        "ledger": corrupted_pair_source["ledger"],
        "event": corrupted_pair_source["pair_event"],
        "act_evidence": corrupted_pair_source["pair_act_evidence"],
        "evidence_of_yield_relation": corrupted_pair_source["pair_evidence_of_yield_relation"],
    }

    return {
        "byte_pair_applicability": _yield_requirement_bundles(
            applicability,
            alternate_applicability,
            corrupted_applicability,
            unrelated_value=alternate_applicability["event"].identity,
        ),
        "byte_pair_measurement": _yield_requirement_bundles(
            pair,
            alternate_pair,
            corrupted_pair,
            unrelated_value=alternate_pair["event"].identity,
        ),
    }


def _remaining_yield_requirement_bundles() -> dict[str, dict[str, dict]]:
    witnesses = {
        "complete_candidate_standing_applicability": (
            _complete_candidate_standing_applicability_yield_witness
        ),
        "complete_candidate_standing": (
            _complete_candidate_standing_yield_witness
        ),
        "representation_candidate": _representation_candidate_yield_witness,
        "representation_admission": _representation_admission_yield_witness,
        "representation_emission_applicability": (
            _representation_emission_applicability_yield_witness
        ),
        "assertion_locality_movement": _assertion_locality_movement_yield_witness,
        "occurrence_position_measurement": _occurrence_position_yield_witness,
        "byte_pair_occurrence_position_measurement": (
            _byte_pair_occurrence_position_yield_witness
        ),
        "measurement_of_recurrent_byte_pair_occurrence_position": _pair_occurrence_yield_witness,
        "shared_pair_position_applicability": (
            _shared_position_applicability_yield_witness
        ),
        "shared_pair_position_measurement": (
            _shared_position_measurement_yield_witness
        ),
        "recorded_pair_measurement_comparison_applicability": (
            _recorded_pair_measurement_comparison_applicability_yield_witness
        ),
        "recorded_pair_measurement_comparison": (
            _recorded_pair_measurement_comparison_yield_witness
        ),
        "comparison_of_ordered_relation_path_with_recorded_pair_findings_applicability": (
            _ordered_relation_path_pair_finding_comparison_applicability_yield_witness
        ),
        "comparison_of_ordered_relation_path_with_recorded_pair_findings_compare": (
            _ordered_relation_path_pair_finding_comparison_yield_witness
        ),
        "addressed_byte_occurrence_reference_determination_applicability": (
            _addressed_byte_occurrence_reference_determination_applicability_yield_witness
        ),
        "addressed_byte_occurrence_reference_determination": (
            _addressed_byte_occurrence_reference_determination_yield_witness
        ),
        "failed_boundary": _failed_boundary_yield_witness,
        "material_ingest": _material_ingest_yield_witness,
        "operator_material_acquire": _operator_material_acquire_yield_witness,
        "operator_invocation_locality_relation": (
            _operator_system_locality_yield_witness
        ),
        "standing_boundary_reference": _standing_boundary_reference_yield_witness,
        "recorded_standing_boundary_locality_relation": (
            _recorded_standing_boundary_locality_yield_witness
        ),
        "standing_locality_continuation": (
            _standing_locality_continuation_yield_witness
        ),
    }
    boundaries = {}
    for boundary, witness in witnesses.items():
        exact = witness()
        alternate = witness()
        corrupted = witness()
        boundaries[boundary] = _yield_requirement_bundles(
            exact,
            alternate,
            corrupted,
            unrelated_value=alternate["event"].identity,
        )
    return boundaries


def _additional_relation_occurrence_fidelity_findings() -> dict[
    tuple[str, str], dict[str, str]
]:
    representation, alternate_representation = _repeated_representation_witness()
    missing_representation_locality = dict(representation)
    missing_representation_locality_evidence = deepcopy(representation[
        "locality_evidence"
    ])
    missing_representation_locality_evidence.material["carried_content"][
        "representation_result"
    ] = "different result"
    missing_representation_locality[
        "locality_evidence"
    ] = missing_representation_locality_evidence
    wrong_representation_locality = dict(representation)
    wrong_representation_locality_evidence = deepcopy(representation[
        "locality_evidence"
    ])
    wrong_representation_locality_evidence.material["act_occurrence_identity"] = (
        alternate_representation["event"].material["act_occurrence_identity"]
    )
    wrong_representation_locality[
        "locality_evidence"
    ] = wrong_representation_locality_evidence
    corrupted_representation_locality = _representation_witness()
    corrupted_representation_locality["ledger"].mark_corrupted(
        corrupted_representation_locality["locality_evidence"].identity
    )
    unrelated_representation_locality = dict(representation)
    unrelated_representation_event = deepcopy(representation["event"])
    unrelated_representation_event.material["evidence_of_yield_relation_identity"] = "other-yield"
    unrelated_representation_locality["event"] = unrelated_representation_event

    missing_representation_yield = dict(representation)
    missing_representation_yield_event = deepcopy(representation["event"])
    missing_representation_yield_event.material["evidence_of_yield_relation_identity"] = (
        "missing-yield-evidence"
    )
    missing_representation_yield["event"] = missing_representation_yield_event
    wrong_representation_yield = dict(representation)
    wrong_representation_act_evidence = deepcopy(representation["act_evidence"])
    wrong_representation_evidence_of_yield_relation = deepcopy(representation[
        "evidence_of_yield_relation"
    ])
    alternate_occurrence = alternate_representation["event"].material[
        "act_occurrence_identity"
    ]
    wrong_representation_act_evidence.material["act_occurrence_identity"] = (
        alternate_occurrence
    )
    wrong_representation_evidence_of_yield_relation.material["dimensions"][
        "act_occurrence_identity"
    ] = alternate_occurrence
    wrong_representation_yield["act_evidence"] = wrong_representation_act_evidence
    wrong_representation_yield[
        "evidence_of_yield_relation"
    ] = wrong_representation_evidence_of_yield_relation
    corrupted_representation_yield = _representation_witness()
    corrupted_representation_yield["ledger"].mark_corrupted(
        corrupted_representation_yield["evidence_of_yield_relation"].identity
    )
    unrelated_representation_yield = dict(representation)
    unrelated_representation_yield_event = deepcopy(representation["event"])
    unrelated_representation_yield_event.material["locality_evidence_identity"] = (
        "other-locality"
    )
    unrelated_representation_yield["event"] = unrelated_representation_yield_event

    attempt, alternate_attempt = _repeated_emission_attempt_witness()
    missing_attempt = dict(attempt)
    changed_relation_material = dict(attempt["attempt_locality_evidence"].material)
    changed_relation_material["carried_content"] = "different carried content"
    missing_attempt["attempt_locality_evidence"] = attempt["ledger"].append(
        attempt["attempt_locality_evidence"].kind,
        changed_relation_material,
        locality_identity="repeated-emission-attempt",
    )
    wrong_attempt = dict(attempt)
    wrong_attempt["attempt_locality_evidence"] = alternate_attempt[
        "attempt_locality_evidence"
    ]
    corrupted_attempt, _ = _repeated_emission_attempt_witness()
    corrupted_attempt["ledger"].mark_corrupted(
        corrupted_attempt["attempt_locality_evidence"].identity
    )
    unrelated_attempt = dict(attempt)
    unrelated_attempt_event = deepcopy(attempt["attempt"])
    unrelated_attempt_event.material["evidence_of_yield_relation_identity"] = "unrelated-yield"
    unrelated_attempt["attempt"] = unrelated_attempt_event

    return {
        ("locality", "representation_result"): {
            "exact": _representation_locality_witness(representation),
            "relation_missing": _representation_locality_witness(
                missing_representation_locality
            ),
            "different_occurrence": _representation_locality_witness(
                wrong_representation_locality
            ),
            "evidence_not_intact": _representation_locality_witness(
                corrupted_representation_locality
            ),
            "different_relation_occurrence": _representation_locality_witness(
                unrelated_representation_locality
            ),
        },
        ("yield", "representation_result"): {
            "exact": _occurrence_result_witness(representation),
            "relation_missing": _occurrence_result_witness(
                missing_representation_yield
            ),
            "different_occurrence": _occurrence_result_witness(
                wrong_representation_yield
            ),
            "evidence_not_intact": _occurrence_result_witness(
                corrupted_representation_yield
            ),
            "different_relation_occurrence": _occurrence_result_witness(
                unrelated_representation_yield
            ),
        },
        ("locality", "emission_attempt"): {
            "exact": _emission_attempt_locality_witness(attempt),
            "relation_missing": _emission_attempt_locality_witness(missing_attempt),
            "different_occurrence": _emission_attempt_locality_witness(wrong_attempt),
            "evidence_not_intact": _emission_attempt_locality_witness(
                corrupted_attempt
            ),
            "different_relation_occurrence": _emission_attempt_locality_witness(
                unrelated_attempt
            ),
        },
    }


def _relation_occurrence_fidelity_findings() -> dict[
    tuple[str, str], dict[str, str]
]:
    byte_pair_yield_bundles = _byte_pair_yield_requirement_bundles()
    remaining_yield_bundles = _remaining_yield_requirement_bundles()
    primary_boundaries = {
        "locality": "byte_measurement",
        "participation": "byte_pair_measurement",
        "yield": "byte_measurement",
        "carried_by": "byte_measurement",
    }
    registered = {
        (relation, primary_boundaries[relation]): findings
        for relation, findings in _relation_fidelity_findings().items()
    }
    registered.update(
        {
            (relation, "successful_emission"): findings
            for relation, findings in _emission_relation_fidelity_findings().items()
        }
    )
    registered.update(_additional_relation_occurrence_fidelity_findings())
    registered[("locality", "assertion_movement")] = _locality_fidelity_findings()
    registered[("locality", "operator_material_acquisition")] = (
        _operator_material_acquire_locality_fidelity_findings()
    )
    registered.update(
        {
            ("yield", boundary): {
                case: _occurrence_result_witness(bundle)
                for case, bundle in cases.items()
            }
            for boundary, cases in byte_pair_yield_bundles.items()
        }
    )
    registered.update(
        {
            ("carried_by", boundary): {
                case: _evidence_carried_by_result_occurrence_witness(bundle)
                for case, bundle in cases.items()
            }
            for boundary, cases in byte_pair_yield_bundles.items()
        }
    )
    registered.update(
        {
            ("yield", boundary): {
                case: _occurrence_result_witness(bundle)
                for case, bundle in cases.items()
            }
            for boundary, cases in remaining_yield_bundles.items()
        }
    )
    registered.update(
        {
            ("carried_by", boundary): {
                case: _evidence_carried_by_result_occurrence_witness(bundle)
                for case, bundle in cases.items()
            }
            for boundary, cases in remaining_yield_bundles.items()
        }
    )
    return registered


def test_primary_relation_measurements_preserve_their_occurrence_boundaries():
    registered = _relation_occurrence_fidelity_findings()

    assert ("locality", "byte_measurement") in registered
    assert ("participation", "byte_pair_measurement") in registered
    assert ("yield", "byte_measurement") in registered
    assert ("carried_by", "byte_measurement") in registered
    assert ("locality", "assertion_movement") in registered


def _relation_witness_specs() -> dict[str, dict]:
    requirements = {
        "exact_relation": "relation_missing",
        "occurrence_witness": "different_occurrence",
        "intact_evidence": "evidence_not_intact",
    }
    return {
        "locality": {
            "from": "first_subject",
            "to": "second_subject",
            "requires": requirements,
        },
        "participation": {
            "from": "subject",
            "to": "Act_occurrence",
            "coordinate": "role",
            "requires": requirements,
        },
        "yield": {
            "from": "Act_occurrence",
            "to": "result",
            "preserves": ["Act_occurrence_identity", "result_identity"],
            "requires": requirements,
        },
        "carried_by": {
            "from": {
                "identity": "Evidence_of_Yield_relation",
                "first_subject": "Evidence",
                "relation": "of",
                "second_subject": "Yield_relation",
            },
            "to": {
                "identity": "recording_occurrence_of_result",
                "first_subject": "recording_occurrence",
                "relation": "of",
                "second_subject": "result",
            },
            "coordinate": {
                "identity": "evidence_of_yield_relation_identity",
                "first_subject": "Evidence",
                "relation": "of",
                "second_subject": "Yield_relation",
            },
            "occurrence_coordinate": "recorded_result_event_identity",
            "requires": requirements,
        },
    }


def _assert_relation_anatomy(grammar: dict, specs: dict[str, dict]) -> None:
    assert set(specs) == set(grammar["relations"])
    relation_families = grammar["witness"]["relation_witness_coordinates"][
        "families"
    ]
    for relation, declared in grammar["relations"].items():
        witnessed = specs[relation]
        declared_anatomy = {
            key: value
            for key, value in declared.items()
            if key not in {"book_clause", "requires"}
        }
        witnessed_anatomy = {
            key: value for key, value in witnessed.items() if key != "requires"
        }
        assert witnessed_anatomy == declared_anatomy
        assert list(witnessed["requires"]) == declared["requires"]
        assert declared["requires"] == relation_families[relation]


def _act_occurrence_witness(bundle: dict) -> dict[str, str]:
    event = bundle["event"]
    act_evidence = bundle["act_evidence"]
    byte_assignment = (
        _byte_measurement_assignment_from_reference(bundle)
        if event.kind == BYTE_MEASUREMENT_RECORDED_KIND
        else None
    )
    pair_assignment = (
        _pair_measurement_assignment_from_reference(bundle)
        if event.kind == BYTE_PAIR_MEASUREMENT_RECORDED_KIND
        else None
    )
    assignment = (
        event.material.get("responsibility_assignment_reference")
        if event.kind in {
            BYTE_MEASUREMENT_RECORDED_KIND,
            BYTE_PAIR_MEASUREMENT_RECORDED_KIND,
        }
        else event.material["responsibility_assignment_evidence"]
    )
    joined = (
        act_evidence is not None
        and event.material["addressed_act_identity"]
        == act_evidence.material["addressed_act_identity"]
        and event.material["act_occurrence_identity"]
        == act_evidence.material["act_occurrence_identity"]
        and event.material["responsibility"]
        == act_evidence.material["responsibility"]
        and event.material["responsible_boundary"]
        == act_evidence.material["responsible_boundary"]
        and assignment
        == act_evidence.material.get(
            "responsibility_assignment_reference"
            if event.kind in {
                BYTE_MEASUREMENT_RECORDED_KIND,
                BYTE_PAIR_MEASUREMENT_RECORDED_KIND,
            }
            else "responsibility_assignment_evidence"
        )
    )
    assignment_standing = bool(
        joined
        and _responsibility_assignment_standing_is_exact(bundle)
    )
    return {
        "Responsibility": EXACT if joined else MISSING,
        "Responsibility_assignment_Standing": (
            EXACT if assignment_standing else MISSING
        ),
        "responsible_boundary": EXACT if joined else MISSING,
        "exact_Act": EXACT if joined else MISSING,
        "Act_occurrence": EXACT if joined else MISSING,
        "Evidence_of_Act_occurrence": (
            EXACT
            if joined
            and event.material["responsible_act_evidence_identity"] == act_evidence.identity
            else MISSING
        ),
        "Authority": (
            EXACT if joined and act_evidence.material.get("authority") else MISSING
        ),
        "Scope": (
            EXACT
            if event.locality_identity is not None
            and (
                byte_assignment.material.get("completeness_boundary_identity")
                if byte_assignment is not None
                else assignment.get("completeness_boundary")
            )
            else MISSING
        ),
        "limits": (
            EXACT if event.material["dimensions"].get("authority") else MISSING
        ),
    }


def _byte_measurement_assignment_from_reference(bundle: dict):
    reference = bundle["event"].material.get(
        "responsibility_assignment_reference"
    )
    if type(reference) is not dict:
        return None
    assignment = bundle["ledger"].get(
        reference.get("recorded_occurrence_identity")
    )
    if assignment is None:
        return None
    try:
        standing = read_operator_locality_standing_through(
            bundle["ledger"],
            locality_identity=assignment.locality_identity,
            through_event_occurrence_identity=assignment.identity,
        )
    except (TypeError, ValueError):
        return None
    if (
        assignment.kind
        != BYTE_MEASUREMENT_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND
        or reference
        != {
            "recorded_occurrence_identity": assignment.identity,
            "assignment_identity": assignment.material["assignment_identity"],
            "assignment_subject_identity": assignment.material[
                "assignment_subject_identity"
            ],
        }
        or standing.get("responsibility_assignment_occurrences", {}).get(
            assignment.identity, object()
        )
        is not None
    ):
        return None
    return assignment


def _pair_measurement_assignment_from_reference(bundle: dict):
    reference = bundle["event"].material.get(
        "responsibility_assignment_reference"
    )
    if type(reference) is not dict:
        return None
    try:
        assignment = get_byte_position_pair_measurement_responsibility_assignment(
            bundle["ledger"], reference.get("recorded_occurrence_identity")
        )
        standing = read_operator_locality_standing_through(
            bundle["ledger"],
            locality_identity=assignment.locality_identity,
            through_event_occurrence_identity=assignment.identity,
        )
    except (TypeError, ValueError):
        return None
    if (
        assignment.kind
        != BYTE_PAIR_MEASUREMENT_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND
        or reference
        != {
            "recorded_occurrence_identity": assignment.identity,
            "assignment_identity": assignment.material["assignment_identity"],
            "assignment_subject_identity": assignment.material[
                "assignment_subject_identity"
            ],
        }
        or standing.get("responsibility_assignment_occurrences", {}).get(
            assignment.identity, object()
        )
        is not None
    ):
        return None
    return assignment


def _occurrence_position_assignment_reference_is_exact(bundle: dict) -> bool:
    event = bundle["event"]
    reference = event.material.get("responsibility_assignment_reference")
    if type(reference) is not dict:
        return False
    try:
        assignment = get_occurrence_position_measurement_responsibility_assignment(
            bundle["ledger"], reference.get("recorded_occurrence_identity")
        )
        standing = read_operator_locality_standing_through(
            bundle["ledger"],
            locality_identity=assignment.locality_identity,
            through_event_occurrence_identity=assignment.identity,
        )
    except (TypeError, ValueError):
        return False
    return bool(
        assignment.kind
        == OCCURRENCE_POSITION_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND
        and reference
        == {
            "recorded_occurrence_identity": assignment.identity,
            "assignment_identity": assignment.material["assignment_identity"],
            "assignment_subject_identity": assignment.material[
                "assignment_subject_identity"
            ],
        }
        and standing.get("responsibility_assignment_occurrences", {}).get(
            assignment.identity, object()
        )
        is None
    )


def _pair_occurrence_assignment_from_reference(bundle: dict):
    reference = bundle["event"].material.get(
        "responsibility_assignment_reference"
    )
    if type(reference) is not dict:
        return None
    assignment = bundle["ledger"].get(
        reference.get("recorded_occurrence_identity")
    )
    if assignment is None:
        return None
    try:
        standing = read_operator_locality_standing_through(
            bundle["ledger"],
            locality_identity=assignment.locality_identity,
            through_event_occurrence_identity=assignment.identity,
        )
    except (TypeError, ValueError):
        return None
    if (
        assignment.kind
        != RECORDED_RESPONSIBILITY_ASSIGNMENT_OF_MEASUREMENT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_KIND
        or reference
        != {
            "recorded_occurrence_identity": assignment.identity,
            "assignment_identity": assignment.material["assignment_identity"],
            "assignment_subject_identity": assignment.material[
                "assignment_subject_identity"
            ],
        }
        or standing.get("responsibility_assignment_occurrences", {}).get(
            assignment.identity, object()
        )
        is not None
    ):
        return None
    return assignment


def _pair_occurrence_assignment_reference_is_exact(bundle: dict) -> bool:
    return _pair_occurrence_assignment_from_reference(bundle) is not None


def _responsibility_assignment_standing_is_exact(bundle: dict) -> bool:
    event = bundle["event"]
    assignment = event.material.get("responsibility_assignment_evidence")
    if event.kind == BYTE_MEASUREMENT_RECORDED_KIND:
        return _byte_measurement_assignment_from_reference(bundle) is not None
    if event.kind == BYTE_PAIR_MEASUREMENT_RECORDED_KIND:
        return _pair_measurement_assignment_from_reference(bundle) is not None
    if event.kind == OCCURRENCE_POSITION_RECORDED_KIND:
        return _occurrence_position_assignment_reference_is_exact(bundle)
    if (
        event.kind
        == RECORDING_OCCURRENCE_OF_RESULT_OF_MEASUREMENT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_KIND
    ):
        return _pair_occurrence_assignment_reference_is_exact(bundle)
    return assignment.get("standing") == "assigned"


def _measurement_result_witness(bundle: dict) -> dict[str, str]:
    event = bundle["event"]
    material = event.material
    expected = {
        BYTE_MEASUREMENT_RECORDED_KIND: (
            BYTE_MEASUREMENT_RESPONSIBILITY,
            BYTE_MEASUREMENT_RULE,
            True,
            {"exact_source_material_set", "count", "recurrence"},
            "ingest_occurrence_identity",
        ),
        BYTE_PAIR_MEASUREMENT_RECORDED_KIND: (
            BYTE_PAIR_MEASUREMENT_RESPONSIBILITY,
            BYTE_PAIR_MEASUREMENT_RULE,
            False,
            {"count", "recurrence"},
            "ingest_occurrence_identity",
        ),
        OCCURRENCE_POSITION_RECORDED_KIND: (
            OCCURRENCE_POSITION_RESPONSIBILITY,
            OCCURRENCE_POSITION_MEASUREMENT_RULE,
            False,
            {"position"},
            "occurrence_identity",
        ),
        RECORDING_OCCURRENCE_OF_RESULT_OF_MEASUREMENT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_KIND: (
            RESPONSIBILITY_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_MEASUREMENT,
            RULE_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_MEASUREMENT,
            False,
            {"position"},
            "occurrence_identity",
        ),
        SHARED_POSITION_MEASUREMENT_RESULT_KIND: (
            SHARED_POSITION_MEASUREMENT_RESPONSIBILITY,
            SHARED_POSITION_MEASUREMENT_RULE,
            False,
            {"ordered_relation_path"},
            "occurrence_identity",
        ),
    }.get(event.kind)
    if expected is None:
        return {
            coordinate: MISSING
            for coordinate in _clause("01.Source.D")["responsibility"][
                "coordinates"
            ]
        }
    (
        expected_responsibility,
        expected_rule,
        carries_source_set,
        allowed_results,
        source_reference_coordinate,
    ) = expected
    byte_assignment = None
    byte_assignment_occurrence = None
    pair_assignment = None
    pair_occurrence_assignment = None
    if (
        event.kind
        == RECORDING_OCCURRENCE_OF_RESULT_OF_MEASUREMENT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_KIND
    ):
        assignment = material.get("responsibility_assignment_reference")
        pair_occurrence_assignment = _pair_occurrence_assignment_from_reference(
            bundle
        )
    elif event.kind == BYTE_MEASUREMENT_RECORDED_KIND:
        assignment = material.get("responsibility_assignment_reference")
        if type(assignment) is dict:
            byte_assignment_occurrence = bundle["ledger"].get(
                assignment.get("recorded_occurrence_identity")
            )
        byte_assignment = _byte_measurement_assignment_from_reference(bundle)
    elif event.kind == BYTE_PAIR_MEASUREMENT_RECORDED_KIND:
        assignment = material.get("responsibility_assignment_reference")
        pair_assignment = _pair_measurement_assignment_from_reference(bundle)
    else:
        assignment = material.get("responsibility_assignment_evidence")
    localities = material.get("source_localities")
    boundary = material.get("completeness_boundary")
    assertions = material.get("assertions")
    expected_scope = (
        {"source_localities": localities}
        if isinstance(localities, list) and localities
        else None
    )
    assertion_results = (
        [item.get("result") for item in assertions]
        if isinstance(assertions, list)
        and all(isinstance(item, dict) for item in assertions)
        else None
    )
    position_assertions_are_exact = bool(
        event.kind != OCCURRENCE_POSITION_RECORDED_KIND
        or (
            isinstance(assertions, list)
            and all(
                item.get("result") == "position"
                and item.get("input_support", {}).get(
                    "occurrence_references"
                )
                == [
                    item.get("assertion_subject", {}).get(
                        "occurrence_identity"
                    )
                ]
                and item.get("dimensions", {}).get("content")
                == {
                    "position": position,
                    "completeness_boundary": boundary,
                }
                for position, item in enumerate(assertions)
            )
        )
    )
    pair_occurrence_assertions_are_exact = bool(
        event.kind != RECORDING_OCCURRENCE_OF_RESULT_OF_MEASUREMENT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_KIND
        or (
            isinstance(assertions, list)
            and all(
                item.get("result") == "position"
                and set(item.get("dimensions", {}).get("content", {}))
                == {
                    "first_position",
                    "second_position",
                    "completeness_boundary",
                }
                and item.get("assertion_subject", {}).get(
                    "pair_assertion_reference"
                )
                == material.get("pair_assertion_reference")
                and item.get("assertion_subject", {}).get(
                    "source_ingest_occurrence_identity"
                )
                == material.get("source_ingest_occurrence_identity")
                for item in assertions
            )
        )
    )
    carried_assertions_are_exact = bool(
        assertion_results is not None
        and position_assertions_are_exact
        and pair_occurrence_assertions_are_exact
        and all(
            item.get("assertion_subject", {}).get("measurement_rule")
            == expected_rule
            and item.get("assertion_scope") == expected_scope
            and item.get("dimensions", {}).get("responsibility")
            == (
                SHARED_POSITION_ASSERTION_RESPONSIBILITY
                if event.kind == SHARED_POSITION_MEASUREMENT_RESULT_KIND
                else MEASURED_ASSERTION_RESPONSIBILITY
            )
            for item in assertions
        )
        and set(assertion_results) <= allowed_results
        and (
            assertion_results[:1] == ["exact_source_material_set"]
            if carries_source_set
            else "exact_source_material_set" not in assertion_results
        )
    )
    expected_assignment_coordinates = {
        "responsible_boundary",
        "source_occurrence_references",
        "completeness_boundary",
        "determination",
    }
    if event.kind not in {
        BYTE_MEASUREMENT_RECORDED_KIND,
        OCCURRENCE_POSITION_RECORDED_KIND,
        RECORDING_OCCURRENCE_OF_RESULT_OF_MEASUREMENT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_KIND,
    }:
        expected_assignment_coordinates.add("standing")
    if (
        byte_assignment is not None
        or pair_assignment is not None
        or pair_occurrence_assignment is not None
    ):
        assignment_is_exact = bool(
            isinstance(assignment, dict)
            and set(assignment)
            == {
                "recorded_occurrence_identity",
                "assignment_identity",
                "assignment_subject_identity",
            }
        )
    else:
        assignment_is_exact = bool(
            isinstance(assignment, dict)
            and set(assignment) == expected_assignment_coordinates
            and assignment["responsible_boundary"]
            == SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY
            and _responsibility_assignment_standing_is_exact(bundle)
            and isinstance(assignment["source_occurrence_references"], list)
            and assignment["source_occurrence_references"]
            and all(
                isinstance(reference, dict)
                and set(reference) == {source_reference_coordinate}
                and isinstance(reference[source_reference_coordinate], str)
                and reference[source_reference_coordinate]
                for reference in assignment["source_occurrence_references"]
            )
            and isinstance(assignment["determination"], str)
            and assignment["determination"]
            and (
                event.kind != OCCURRENCE_POSITION_RECORDED_KIND
                or (
                    isinstance(assertions, list)
                    and assignment["source_occurrence_references"]
                    == [
                        {
                            "occurrence_identity": item.get(
                                "assertion_subject", {}
                            ).get("occurrence_identity")
                        }
                        for item in assertions
                        if isinstance(item, dict)
                    ]
                )
            )
        )
    return {
        "responsibility": (
            EXACT
            if material.get("responsibility") == expected_responsibility
            else MISSING
        ),
        "responsible_boundary": (
            EXACT
            if material.get("responsible_boundary")
            == SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY
            else MISSING
        ),
        "responsibility_assignment_evidence": (
            EXACT if assignment_is_exact else MISSING
        ),
        "measurement_rule": (
            EXACT if material.get("measurement_rule") == expected_rule else MISSING
        ),
        "source_localities": (
            EXACT
            if isinstance(localities, list)
            and localities
            and len(localities) == len(set(localities))
            and all(isinstance(locality, str) and locality for locality in localities)
            else MISSING
        ),
        "completeness_boundary": (
            EXACT
            if isinstance(boundary, dict)
            and set(boundary) == {"identity"}
            and isinstance(boundary["identity"], str)
            and boundary["identity"]
            and isinstance(assignment, dict)
            and (
                (
                    byte_assignment_occurrence
                    or pair_assignment
                    or pair_occurrence_assignment
                ).material.get("completeness_boundary_identity")
                == boundary["identity"]
                if byte_assignment_occurrence is not None
                or pair_assignment is not None
                or pair_occurrence_assignment is not None
                else assignment.get("completeness_boundary")
                == boundary["identity"]
            )
            else MISSING
        ),
        "assertions": EXACT if carried_assertions_are_exact else MISSING,
    }


def _measurement_result_distinctions(bundle: dict) -> dict[tuple[str, str], bool]:
    event = bundle["event"]
    material = event.material
    assertions = material.get("assertions")
    assertion_responsibilities = (
        {
            item.get("dimensions", {}).get("responsibility")
            for item in assertions
            if isinstance(item, dict)
        }
        if isinstance(assertions, list)
        else set()
    )
    return {
        ("Measurement_result", "exact_Act_occurrence"): (
            material.get("result_identity")
            != material.get("act_occurrence_identity")
        ),
        ("Measurement_occurrence", "recording_occurrence"): (
            material.get("act_occurrence_identity") != event.identity
        ),
        (
            "Measurement_Responsibility",
            "Assertion_Standing_coordinate_Responsibility",
        ): (
            bool(assertion_responsibilities)
            and assertion_responsibilities
            == {
                SHARED_POSITION_ASSERTION_RESPONSIBILITY
                if event.kind == SHARED_POSITION_MEASUREMENT_RESULT_KIND
                else MEASURED_ASSERTION_RESPONSIBILITY
            }
            and material.get("responsibility") not in assertion_responsibilities
        ),
    }


def _representation_source_witness(bundle: dict) -> dict[str, str]:
    event = bundle["event"]
    material = event.material
    dimensions = material.get("dimensions")
    dimensions = dimensions if isinstance(dimensions, dict) else {}
    source_reference = material.get("source_occurrence_reference")
    source = (
        bundle["ledger"].get(source_reference)
        if isinstance(source_reference, str)
        else None
    )
    standing_boundary = material.get("locality_standing_through_event_occurrence_identity")
    standing_boundary_event = (
        bundle["ledger"].get(standing_boundary)
        if isinstance(standing_boundary, str)
        else None
    )
    try:
        if source_reference != standing_boundary:
            bundle["ledger"].occurrences_in_append_order(
                (source_reference, standing_boundary),
                locality_identity=event.locality_identity,
            )
        bundle["ledger"].occurrences_in_append_order(
            (standing_boundary, event.identity),
            locality_identity=event.locality_identity,
        )
        standing_boundary_is_exact = True
    except (TypeError, ValueError):
        standing_boundary_is_exact = False
    return {
        "responsibility": (
            EXACT
            if dimensions.get("responsibility") == REPRESENTATION_RESPONSIBILITY
            else MISSING
        ),
        "representation_rule": (
            EXACT
            if material.get("representation_rule")
            == EXACT_SOURCE_MATERIAL_REPRESENTATION_RULE
            else MISSING
        ),
        "source_occurrence_reference": (
            EXACT
            if source is not None
            and bundle["ledger"].integrity_of(source.identity) != CORRUPTED
            and source.locality_identity == event.locality_identity
            and source.exact_material == event.exact_material
            else MISSING
        ),
        "locality_standing_through_event_occurrence_identity": (
            EXACT
            if standing_boundary_is_exact
            and standing_boundary_event is not None
            and bundle["ledger"].integrity_of(standing_boundary) != CORRUPTED
            else MISSING
        ),
        "source_provenance": (
            EXACT
            if dimensions.get("source_provenance")
            == material.get("locality_standing_through_event_occurrence_identity")
            else MISSING
        ),
        "scope_locality": (
            EXACT
            if dimensions.get("scope_locality")
            == f"locality:{event.locality_identity}"
            else MISSING
        ),
        "authority": (
            EXACT if dimensions.get("authority") == "unestablished" else MISSING
        ),
        "known_loss": (
            EXACT if isinstance(material.get("known_loss"), list) else MISSING
        ),
        "conflicts": (
            EXACT if isinstance(material.get("conflicts"), list) else MISSING
        ),
        "unknown": (
            EXACT if isinstance(material.get("unknown"), list) else MISSING
        ),
    }


def _representation_source_distinctions(
    bundle: dict,
) -> dict[tuple[str, str], bool]:
    event = bundle["event"]
    material = event.material
    return {
        ("Representation_result", "exact_Act_occurrence"): (
            material.get("result_identity")
            != material.get("act_occurrence_identity")
        ),
        ("Representation_source_coordinates", "Locality_relation"): (
            material.get("source_occurrence_reference")
            != material.get("locality_evidence_identity")
        ),
    }


def _representation_act_evidence_witness(bundle: dict) -> bool:
    event = bundle["event"]
    evidence = bundle["act_evidence"]
    return bool(
        evidence is not None
        and evidence.kind == REPRESENTATION_ACT_EVIDENCE_KIND
        and bundle["ledger"].integrity_of(evidence.identity) != CORRUPTED
        and event.material.get("responsible_act_evidence_identity") == evidence.identity
        and event.material.get("representation_act_identity")
        == evidence.material.get("representation_act_identity")
        and event.material.get("act_occurrence_identity")
        == evidence.material.get("act_occurrence_identity")
        and event.material.get("dimensions", {}).get("responsibility")
        == evidence.material.get("responsibility")
        == REPRESENTATION_RESPONSIBILITY
    )


def _locality_requirements(bundle: dict) -> dict[str, bool]:
    ledger = bundle["ledger"]
    movement = bundle["movement"]
    act_evidence = bundle["movement_act_evidence"]
    relation = movement.material.get("locality_relation")
    evidence_relation = (
        act_evidence.material.get("locality_relation")
        if act_evidence is not None
        else None
    )
    return {
        "exact_relation": bool(
            isinstance(relation, dict)
            and isinstance(evidence_relation, dict)
            and relation.get("first_subject")
            == evidence_relation.get("first_subject")
            == movement.material.get("source_assertion_reference")
            and relation.get("second_subject")
            == evidence_relation.get("second_subject")
            == movement.material.get("destination_locality")
        ),
        "occurrence_witness": bool(
            isinstance(relation, dict)
            and isinstance(evidence_relation, dict)
            and relation.get("relation_occurrence_identity")
            == evidence_relation.get("relation_occurrence_identity")
            == movement.material.get("movement_act_occurrence_identity")
        ),
        "intact_evidence": bool(
            act_evidence is not None
            and movement.material.get("responsible_act_evidence_identity")
            == act_evidence.identity
            and ledger.integrity_of(act_evidence.identity) != CORRUPTED
        ),
    }


def _locality_witness(bundle: dict) -> str:
    return EXACT if all(_locality_requirements(bundle).values()) else MISSING


def _movement_coordinate_witness(bundle: dict) -> dict[str, str]:
    ledger = bundle["ledger"]
    movement = bundle["movement"]
    act_evidence = bundle["movement_act_evidence"]
    source_reference = movement.material.get("source_assertion_reference")
    try:
        source = _validate_moved_byte_assertion(ledger, movement.identity)
    except ValueError:
        source = None
    source_event = (
        ledger.get(source.recorded_occurrence_identity)
        if source is not None
        else None
    )
    source_material = source.material if source is not None else {}
    source_dimensions = source_material.get("dimensions", {})
    assignment_reference = movement.material.get(
        "responsibility_assignment_reference"
    )
    assignment = (
        ledger.get(assignment_reference.get("recorded_occurrence_identity"))
        if type(assignment_reference) is dict
        else None
    )
    try:
        assignment_standing = read_operator_locality_standing_through(
            ledger,
            locality_identity=movement.locality_identity,
            through_event_occurrence_identity=(
                assignment.identity if assignment is not None else None
            ),
        )
    except (TypeError, ValueError):
        assignment_standing = {}
    exact_assignment_standing = bool(
        assignment is not None
        and assignment.kind
        == ASSERTION_LOCALITY_MOVEMENT_RESPONSIBILITY_ASSIGNMENT_KIND
        and assignment_reference
        == {
            "recorded_occurrence_identity": assignment.identity,
            "assignment_identity": assignment.material["assignment_identity"],
            "assignment_subject_identity": assignment.material[
                "assignment_subject_identity"
            ],
        }
        and assignment_standing.get(
            "responsibility_assignment_occurrences", {}
        ).get(assignment.identity, object())
        is None
    )
    preserved = movement.material.get("preserved_coordinates")
    exact_preserved = preserved == [
        "Evidence",
        "Authority",
        "Scope",
        "Unknown",
        "limits",
        "Standing",
    ]
    evidence_requirements = read_requirements_of_yield_relation(
        ledger,
        recorded_result_event_identity=movement.identity,
        evidence_of_yield_relation_event_identity=movement.material.get(
            "evidence_of_yield_relation_identity"
        ),
        responsible_act_evidence_event_identity=movement.material.get(
            "responsible_act_evidence_identity"
        ),
        recorded_result_occurrence_coordinate=(
            "movement_act_occurrence_identity"
        ),
        responsible_act_occurrence_coordinate=(
            "movement_act_occurrence_identity"
        ),
    )
    intact_act_evidence = (
        act_evidence is not None
        and ledger.integrity_of(act_evidence.identity) != CORRUPTED
        and movement.material.get("responsible_act_evidence_identity")
        == act_evidence.identity
    )
    exact_source = (
        source is not None
        and movement.material.get("assertion_identity")
        == source.assertion_identity
        and source_reference == source.reference
    )
    return {
        "subject": EXACT if exact_source else MISSING,
        "source_coordinates": (
            EXACT
            if exact_source
            and source_event is not None
            and movement.material.get("source_locality")
            == source_event.locality_identity
            else MISSING
        ),
        "destination_coordinates": (
            EXACT
            if movement.material.get("destination_locality")
            == movement.locality_identity
            and act_evidence is not None
            and act_evidence.material.get("destination_locality")
            == movement.locality_identity
            else MISSING
        ),
        "exact_Act": (
            EXACT
            if intact_act_evidence
            and movement.material.get("movement_act_identity")
            == act_evidence.material.get("movement_act_identity")
            and movement.material.get("movement_act_identity")
            != movement.material.get("movement_act_occurrence_identity")
            else MISSING
        ),
        "Act_occurrence": (
            EXACT
            if intact_act_evidence
            and movement.material.get("movement_act_occurrence_identity")
            == act_evidence.material.get("movement_act_occurrence_identity")
            == movement.material.get("locality_relation", {}).get(
                "relation_occurrence_identity"
            )
            else MISSING
        ),
        "Evidence": (
            EXACT
            if intact_act_evidence and all(evidence_requirements.values())
            else MISSING
        ),
        "Authority": (
            EXACT
            if exact_preserved
            and movement.material.get("authority")
            == source_dimensions.get("authority")
            and act_evidence is not None
            and act_evidence.material.get("authority")
            == source_dimensions.get("authority")
            and "authority" in source_dimensions
            else MISSING
        ),
        "Scope": (
            EXACT
            if exact_preserved
            and isinstance(source_material.get("assertion_scope"), dict)
            and movement.material.get("movement_scope")
            == (
                "Locality movement bounded to this exact Assertion; establishes no "
                "different identity or Standing"
            )
            else MISSING
        ),
        "limits": (
            EXACT
            if exact_preserved and isinstance(source_material.get("limits"), list)
            else MISSING
        ),
        "Unknown": (
            EXACT
            if exact_preserved and isinstance(source_material.get("unknown"), list)
            else MISSING
        ),
        "Standing": (
            EXACT
            if exact_preserved
            and exact_source
            and exact_assignment_standing
            and _byte_measurement_result_has_exact_standing(ledger, source_event)
            else MISSING
        ),
    }


def _locality_fidelity_findings() -> dict[str, str]:
    exact = _recorded_applicability()

    relation_missing = _recorded_applicability()
    relation_missing["movement"].material["locality_relation"]["second_subject"] = (
        "another bounded subject"
    )

    different_occurrence = _recorded_applicability()
    source_occurrence = different_occurrence["ledger"].get(
        different_occurrence["movement"].material["source_assertion_reference"][
            "recorded_occurrence_identity"
        ]
    )
    different_occurrence["movement_act_evidence"].material["locality_relation"][
        "relation_occurrence_identity"
    ] = source_occurrence.identity

    evidence_not_intact = _recorded_applicability()
    evidence_not_intact["ledger"].mark_corrupted(
        evidence_not_intact["movement_act_evidence"].identity
    )

    occurrence_of_different_relation = _recorded_applicability()
    occurrence_of_different_relation["movement"].material["movement_scope"] = "another description"

    return {
        "exact": _locality_witness(exact),
        "relation_missing": _locality_witness(relation_missing),
        "different_occurrence": _locality_witness(different_occurrence),
        "evidence_not_intact": _locality_witness(evidence_not_intact),
        "different_relation_occurrence": _locality_witness(occurrence_of_different_relation),
    }


def _participation_witness(bundle: dict, *, role: str) -> str:
    requirements = _participation_requirements(bundle, role=role)
    return EXACT if all(requirements.values()) else MISSING


def _participation_requirements(bundle: dict, *, role: str) -> dict[str, bool]:
    applicability = bundle["applicability"]
    pair = bundle["pair_event"]
    act_evidence = bundle["pair_act_evidence"]
    if act_evidence is None:
        return {
            "exact_relation": False,
            "occurrence_witness": False,
            "intact_evidence": False,
        }
    exact_subject = (
        applicability["input_assertion_reference"]
        == pair.material["source_assertion_reference"]
        == act_evidence.material["input_assertion_reference"]
    )
    exact_role = (
        role
        == applicability["input_role"]
        == pair.material["input_role"]
        == act_evidence.material["input_role"]
    )
    exact_occurrence = (
        pair.material["act_occurrence_identity"]
        == act_evidence.material["act_occurrence_identity"]
    )
    applicable_to_act = (
        applicability["dimensions"]["standing"] == "applicable"
        and applicability["addressed_act_identity"] == pair.material["addressed_act_identity"]
        and applicability["dimensions"]["identity"]
        == act_evidence.material["input_applicability_identity"]
    )
    return {
        "exact_relation": exact_subject and exact_role and applicable_to_act,
        "occurrence_witness": exact_occurrence,
        "intact_evidence": (
            bundle["ledger"].integrity_of(act_evidence.identity) != CORRUPTED
        ),
    }


def test_witness_discriminates_content_locality_and_occurrence():
    grammar = _witness_grammar()
    ledger = EventLedger()
    content = {"a": 1, "b": 2}

    first = ledger.append("test.locality", dict(content), locality_identity="s")
    second = ledger.append("test.locality", dict(content), locality_identity="t")
    assert first.material == second.material
    assert first.locality_identity != second.locality_identity

    changed_content = ledger.append(
        "test.locality", {"a": 1, "b": 3}, locality_identity="s"
    )
    repeated = ledger.append("test.locality", dict(content), locality_identity="s")
    assert first.material != changed_content.material
    assert first.locality_identity == changed_content.locality_identity
    assert first.identity != changed_content.identity

    assert first.material == repeated.material
    assert first.locality_identity == repeated.locality_identity
    assert first.identity != repeated.identity

    assert grammar["distinctions"] == ["content", "locality", "occurrence"]
    assert grammar["distinct_from"] == [
        ["content", "locality"],
        ["content", "occurrence"],
        ["locality", "occurrence"],
    ]


def _assert_ordered_fidelity_representation(fidelity: dict) -> None:
    test_subjects = fidelity["test_subjects"]
    assert {**fidelity, "test_subjects": "declared_test_subjects"} == {
        "subject": "this_Fidelity",
        "book_material_reference": "01.Source.C",
        "grammar": "established",
        "recorded_occurrence_kind": [],
        "comparison": {
            "first_subject": "this_Witness",
            "relation": "comparison",
            "second_subject": "this_Grammar",
            "addressed_subject": "this_Seed",
            "boundary": "deterministic_tests",
            "result": "this_Fidelity",
        },
        "test_subject_relation": {
            "first_subject": "test_subject",
            "relation": "witness_for",
            "second_subject": "this_Fidelity",
            "first_subject_distinct_from": "this_Witness",
        },
        "test_subjects": "declared_test_subjects",
        "preserves": [
            "Evidence",
            "provenance",
            "Authority",
            "Scope",
            "conflicts",
            "Unknown",
            "erasure",
            "unsupported_coordinates",
            "mutation",
            "Authority_relocation",
        ],
        "comparison_order": [
            "this_Witness",
            "deterministic_tests",
            "this_Grammar",
            "this_Fidelity",
        ],
        "representation_order": [
            "this_Fidelity",
            "exact_relation",
            "supporting_measurements",
        ],
        "standing_not_established": [
            "Standing_beyond_test_boundary",
            "correction_Authority",
        ],
    }
    assert len(test_subjects) == 229
    assert len({coordinates["subject"] for coordinates in test_subjects}) == 229
    assert test_subjects[0] == {
        "subject": "event_standing_grammar_responsibility"
    }
    assert test_subjects[-1] == {
        "subject": "fidelity_witness_subject_completeness"
    }
    by_subject = {
        coordinates["subject"]: coordinates for coordinates in test_subjects
    }
    assert by_subject["this_book_material_acquisition_witness"] == {
        "subject": "this_book_material_acquisition_witness",
        "material_reference": "this_Book",
    }
    assert by_subject["separate_admission_material_relation_order"] == {
        "subject": "separate_admission_material_relation_order",
        "material_reference": "this_separate_admission_material",
    }
    assert by_subject["book_separate_admission_material_Admission_distinction"] == {
        "subject": "book_separate_admission_material_Admission_distinction",
        "first_material_reference": "this_Book",
        "second_material_reference": "this_separate_admission_material",
    }
    assert fidelity["comparison"]["first_subject"] != fidelity["comparison"][
        "second_subject"
    ]
    assert fidelity["comparison"]["boundary"] not in {
        fidelity["comparison"]["first_subject"],
        fidelity["comparison"]["second_subject"],
        fidelity["comparison"]["addressed_subject"],
        fidelity["comparison"]["result"],
    }
    assert fidelity["comparison_order"] != fidelity["representation_order"]


def test_fidelity_is_bounded_witness_grammar_comparison_for_this_seed():
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))

    _assert_ordered_fidelity_representation(grammar["clause_coordinates"]["01.Source.C"])


def test_fidelity_refuses_collapsed_subjects_tests_as_subject_and_inverted_order():
    fidelity = json.loads(GRAMMAR.read_text(encoding="utf-8"))["clause_coordinates"][
        "01.Source.C"
    ]

    collapsed_direction = deepcopy(fidelity)
    collapsed_direction["comparison"]["second_subject"] = collapsed_direction[
        "comparison"
    ]["first_subject"]
    try:
        _assert_ordered_fidelity_representation(collapsed_direction)
    except AssertionError:
        pass
    else:
        raise AssertionError("collapsed Fidelity direction escaped comparison")

    tests_as_subject = deepcopy(fidelity)
    tests_as_subject["comparison"]["first_subject"] = "deterministic_tests"
    try:
        _assert_ordered_fidelity_representation(tests_as_subject)
    except AssertionError:
        pass
    else:
        raise AssertionError("Fidelity tests escaped as a compared subject")

    measurements_first = deepcopy(fidelity)
    measurements_first["representation_order"] = [
        "supporting_measurements",
        "exact_relation",
        "this_Fidelity",
    ]
    try:
        _assert_ordered_fidelity_representation(measurements_first)
    except AssertionError:
        pass
    else:
        raise AssertionError("inverted Fidelity Representation order escaped")


def test_each_fidelity_test_subject_names_one_exact_witness_grammar_coordinate():
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))
    test_subjects = grammar["clause_coordinates"]["01.Source.C"]["test_subjects"]
    missing = []

    for test_subject in test_subjects:
        reference = test_subject.get("grammar_coordinate_reference")
        if reference is None:
            missing.append(test_subject["subject"])
            continue
        coordinate = reference
        assert type(coordinate) is list
        assert len(coordinate) >= 3
        assert coordinate[0] == "clause_coordinates"
        clause_identity = coordinate[1]
        clause = grammar["clause_coordinates"][clause_identity]
        assert clause["book_material_reference"] == clause_identity

        carried = grammar
        for part in coordinate:
            carried = carried[
                part["identity"] if type(part) is dict else part
            ]
        assert carried is not None

    assert missing == []


def test_every_relation_has_exact_fidelity_findings():
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))
    findings = _relation_fidelity_findings()
    specs = _relation_witness_specs()
    expected = grammar["witness"]["fidelity_findings"]

    _assert_relation_anatomy(grammar, specs)
    assert set(findings) == set(grammar["relations"])
    assert all(
        set(relation_findings) == set(expected)
        for relation_findings in findings.values()
    )
    assert findings == {
        relation: expected for relation in grammar["relations"]
    }
    for relation, spec in specs.items():
        for adversary in spec["requires"].values():
            assert findings[relation][adversary] == MISSING


def test_emission_instantiates_each_relation_it_carries_at_its_boundary():
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))
    findings = _emission_relation_fidelity_findings()
    expected = grammar["witness"]["fidelity_findings"]

    assert set(findings) == set(grammar["relations"])
    assert findings == {relation: expected for relation in findings}


def test_every_registered_relation_occurrence_obeys_the_full_fidelity_matrix():
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))
    expected = grammar["witness"]["fidelity_findings"]
    registered = _relation_occurrence_fidelity_findings()

    assert registered
    assert {relation for relation, _boundary in registered} == set(
        grammar["relations"]
    )
    assert all(findings == expected for findings in registered.values())
    assert ("locality", "representation_result") in registered
    assert ("locality", "emission_attempt") in registered
    assert {
        boundary for relation, boundary in registered if relation == "yield"
    } == set(OCCURRENCE_BOUNDARIES_OF_YIELD_RELATION)


def test_every_evidence_of_yield_relation_site_declares_its_occurrence_boundary():
    declared: list[str] = []
    for path in sorted(RUNTIME.glob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            if not isinstance(node.func, ast.Name):
                continue
            if node.func.id != "_record_evidence_of_yield_relation":
                continue
            boundary = next(
                (keyword.value for keyword in node.keywords if keyword.arg == "occurrence_boundary"),
                None,
            )
            assert isinstance(boundary, ast.Constant), (
                f"{path.name}:{node.lineno} must declare one literal occurrence_boundary"
            )
            assert isinstance(boundary.value, str) and boundary.value
            responsible_act_evidence = next(
                (
                    keyword.value
                    for keyword in node.keywords
                    if keyword.arg == "responsible_act_evidence_identity"
                ),
                None,
            )
            assert responsible_act_evidence is not None, (
                f"{path.name}:{node.lineno} must name responsible Act Evidence"
            )
            declared.append(boundary.value)

    assert len(declared) == len(set(declared))
    assert set(declared) == set(OCCURRENCE_BOUNDARIES_OF_YIELD_RELATION)


def test_byte_pair_yield_adversaries_change_one_requirement_each():
    expected = {
        "exact": (True, True, True),
        "relation_missing": (False, True, True),
        "different_occurrence": (True, False, True),
        "evidence_not_intact": (True, True, False),
        "different_relation_occurrence": (True, True, True),
    }
    boundaries = _byte_pair_yield_requirement_bundles()

    assert {
        boundary: {
            case: tuple(_occurrence_result_requirements(bundle).values())
            for case, bundle in cases.items()
        }
        for boundary, cases in boundaries.items()
    } == {boundary: expected for boundary in boundaries}


def test_remaining_yield_adversaries_change_one_requirement_each():
    expected = {
        "exact": (True, True, True),
        "relation_missing": (False, True, True),
        "different_occurrence": (True, False, True),
        "evidence_not_intact": (True, True, False),
        "different_relation_occurrence": (True, True, True),
    }
    boundaries = _remaining_yield_requirement_bundles()

    assert {
        boundary: {
            case: tuple(_occurrence_result_requirements(bundle).values())
            for case, bundle in cases.items()
        }
        for boundary, cases in boundaries.items()
    } == {boundary: expected for boundary in boundaries}


def test_emission_attempt_locality_adversaries_change_one_requirement_each():
    exact, alternate = _repeated_emission_attempt_witness()
    different_occurrence = dict(exact)
    different_occurrence["attempt_locality_evidence"] = alternate[
        "attempt_locality_evidence"
    ]

    missing_relation = dict(exact)
    different = dict(exact["attempt_locality_evidence"].material)
    missing_relation["attempt_locality_evidence"] = exact["ledger"].append(
        exact["attempt_locality_evidence"].kind,
        different,
        locality_identity="repeated-emission-attempt",
    )

    corrupted, _ = _repeated_emission_attempt_witness()
    corrupted["ledger"].mark_corrupted(
        corrupted["attempt_locality_evidence"].identity
    )

    unrelated = dict(exact)
    unrelated_attempt = deepcopy(exact["attempt"])
    unrelated_attempt.material["evidence_of_yield_relation_identity"] = "unrelated-yield"
    unrelated["attempt"] = unrelated_attempt

    assert _emission_attempt_locality_requirements(exact) == {
        "exact_relation": True,
        "occurrence_witness": True,
        "intact_evidence": True,
    }
    assert _emission_attempt_locality_requirements(missing_relation) == {
        "exact_relation": False,
        "occurrence_witness": True,
        "intact_evidence": True,
    }
    assert _emission_attempt_locality_requirements(different_occurrence) == {
        "exact_relation": True,
        "occurrence_witness": False,
        "intact_evidence": True,
    }
    assert _emission_attempt_locality_requirements(corrupted) == {
        "exact_relation": True,
        "occurrence_witness": True,
        "intact_evidence": False,
    }
    assert _emission_attempt_locality_requirements(unrelated) == {
        "exact_relation": True,
        "occurrence_witness": True,
        "intact_evidence": True,
    }


def test_successful_emission_adversaries_change_one_requirement_each():
    bundles = _successful_emission_requirement_bundles()
    requirement_witnesses = {
        "locality": _emission_locality_requirements,
        "participation": _emission_participation_requirements,
        "yield": _occurrence_result_requirements,
        "carried_by": _evidence_carried_by_result_occurrence_requirements,
    }
    expected = {
        "exact": {
            "exact_relation": True,
            "occurrence_witness": True,
            "intact_evidence": True,
        },
        "relation_missing": {
            "exact_relation": False,
            "occurrence_witness": True,
            "intact_evidence": True,
        },
        "different_occurrence": {
            "exact_relation": True,
            "occurrence_witness": False,
            "intact_evidence": True,
        },
        "evidence_not_intact": {
            "exact_relation": True,
            "occurrence_witness": True,
            "intact_evidence": False,
        },
        "different_relation_occurrence": {
            "exact_relation": True,
            "occurrence_witness": True,
            "intact_evidence": True,
        },
    }

    assert {
        relation: {
            case: requirement_witnesses[relation](bundle)
            for case, bundle in cases.items()
        }
        for relation, cases in bundles.items()
    } == {relation: expected for relation in bundles}


def test_representation_result_adversaries_change_one_requirement_each():
    exact, alternate = _repeated_representation_witness()

    missing_locality = dict(exact)
    missing_locality_evidence = deepcopy(exact["locality_evidence"])
    missing_locality_evidence.material["carried_content"][
        "representation_result"
    ] = "different result"
    missing_locality["locality_evidence"] = missing_locality_evidence
    wrong_locality = dict(exact)
    wrong_locality_evidence = deepcopy(exact["locality_evidence"])
    wrong_locality_evidence.material["act_occurrence_identity"] = alternate[
        "event"
    ].material["act_occurrence_identity"]
    wrong_locality["locality_evidence"] = wrong_locality_evidence
    corrupted_locality = _representation_witness()
    corrupted_locality["ledger"].mark_corrupted(
        corrupted_locality["locality_evidence"].identity
    )
    unrelated_locality = dict(exact)
    unrelated_event = deepcopy(exact["event"])
    unrelated_event.material["evidence_of_yield_relation_identity"] = "different-yield-evidence"
    unrelated_locality["event"] = unrelated_event

    missing_yield = dict(exact)
    missing_yield_event = deepcopy(exact["event"])
    missing_yield_event.material["evidence_of_yield_relation_identity"] = "missing-yield-evidence"
    missing_yield["event"] = missing_yield_event
    wrong_yield = dict(exact)
    wrong_act_evidence = deepcopy(exact["act_evidence"])
    wrong_evidence_of_yield_relation = deepcopy(exact["evidence_of_yield_relation"])
    alternate_occurrence = alternate["event"].material["act_occurrence_identity"]
    wrong_act_evidence.material["act_occurrence_identity"] = alternate_occurrence
    wrong_evidence_of_yield_relation.material["dimensions"]["act_occurrence_identity"] = (
        alternate_occurrence
    )
    wrong_yield["act_evidence"] = wrong_act_evidence
    wrong_yield["evidence_of_yield_relation"] = wrong_evidence_of_yield_relation
    corrupted_yield = _representation_witness()
    corrupted_yield["ledger"].mark_corrupted(
        corrupted_yield["evidence_of_yield_relation"].identity
    )
    unrelated_yield = dict(exact)
    unrelated_yield_event = deepcopy(exact["event"])
    unrelated_yield_event.material["locality_evidence_identity"] = "different-locality"
    unrelated_yield["event"] = unrelated_yield_event

    expected = {
        "exact": (True, True, True),
        "relation_missing": (False, True, True),
        "different_occurrence": (True, False, True),
        "evidence_not_intact": (True, True, False),
        "different_relation_occurrence": (True, True, True),
    }
    bundles = {
        "locality": {
            "exact": exact,
            "relation_missing": missing_locality,
            "different_occurrence": wrong_locality,
            "evidence_not_intact": corrupted_locality,
            "different_relation_occurrence": unrelated_locality,
        },
        "yield": {
            "exact": exact,
            "relation_missing": missing_yield,
            "different_occurrence": wrong_yield,
            "evidence_not_intact": corrupted_yield,
            "different_relation_occurrence": unrelated_yield,
        },
        "carried_by": {
            "exact": exact,
            "relation_missing": missing_yield,
            "different_occurrence": wrong_yield,
            "evidence_not_intact": corrupted_yield,
            "different_relation_occurrence": unrelated_yield,
        },
    }
    witnesses = {
        "locality": _representation_locality_requirements,
        "yield": _occurrence_result_requirements,
        "carried_by": _evidence_carried_by_result_occurrence_requirements,
    }

    assert {
        relation: {
            case: tuple(witnesses[relation](bundle).values())
            for case, bundle in cases.items()
        }
        for relation, cases in bundles.items()
    } == {relation: expected for relation in bundles}


def test_byte_measurement_adversaries_change_one_requirement_each():
    locality = _byte_measurement_witness()
    alternate_locality = _byte_measurement_witness()
    missing_locality = dict(locality)
    missing_event = deepcopy(locality["event"])
    missing_event.material["assertions"] = []
    missing_locality["event"] = missing_event
    corrupted_locality = _byte_measurement_witness()
    corrupted_locality["ledger"].mark_corrupted(corrupted_locality["event"].identity)
    unrelated_locality = dict(locality)
    unrelated_event = deepcopy(locality["event"])
    unrelated_event.material["evidence_of_yield_relation_identity"] = "different-yield-evidence"
    unrelated_locality["event"] = unrelated_event

    participation = _recorded_applicability()
    alternate_participation = _recorded_applicability()
    missing_participation = dict(participation)
    missing_participation_evidence = deepcopy(participation[
        "pair_act_evidence"
    ])
    missing_participation_evidence.material["input_role"] = "different-role"
    missing_participation["pair_act_evidence"] = missing_participation_evidence
    wrong_participation = dict(participation)
    wrong_participation_evidence = deepcopy(participation[
        "pair_act_evidence"
    ])
    wrong_participation_evidence.material["act_occurrence_identity"] = (
        alternate_participation["pair_event"].material["act_occurrence_identity"]
    )
    wrong_participation["pair_act_evidence"] = wrong_participation_evidence
    corrupted_participation = _recorded_applicability()
    corrupted_participation["ledger"].mark_corrupted(
        corrupted_participation["pair_act_evidence"].identity
    )
    unrelated_participation = dict(participation)
    unrelated_pair = deepcopy(participation["pair_event"])
    unrelated_pair.material["evidence_of_yield_relation_identity"] = "different-yield-evidence"
    unrelated_participation["pair_event"] = unrelated_pair

    exact_yield = _byte_measurement_witness()
    alternate_yield = _byte_measurement_witness()
    missing_yield = dict(exact_yield)
    missing_yield_event = deepcopy(exact_yield["event"])
    missing_yield_event.material["evidence_of_yield_relation_identity"] = (
        "missing-yield-evidence"
    )
    missing_yield["event"] = missing_yield_event
    wrong_yield = dict(exact_yield)
    wrong_act_evidence = deepcopy(exact_yield["act_evidence"])
    wrong_evidence_of_yield_relation = deepcopy(exact_yield["evidence_of_yield_relation"])
    alternate_occurrence = alternate_yield["event"].material["act_occurrence_identity"]
    wrong_act_evidence.material["act_occurrence_identity"] = alternate_occurrence
    wrong_evidence_of_yield_relation.material["dimensions"]["act_occurrence_identity"] = (
        alternate_occurrence
    )
    wrong_yield["act_evidence"] = wrong_act_evidence
    wrong_yield["evidence_of_yield_relation"] = wrong_evidence_of_yield_relation
    corrupted_yield = _byte_measurement_witness()
    corrupted_yield["ledger"].mark_corrupted(
        corrupted_yield["evidence_of_yield_relation"].identity
    )
    unrelated_yield = dict(exact_yield)
    unrelated_yield_event = deepcopy(exact_yield["event"])
    unrelated_yield_event.material["occurrence_preservation"] = "different"
    unrelated_yield["event"] = unrelated_yield_event

    expected = {
        "exact": (True, True, True),
        "relation_missing": (False, True, True),
        "different_occurrence": (True, False, True),
        "evidence_not_intact": (True, True, False),
        "different_relation_occurrence": (True, True, True),
    }
    actual = {
        "locality": {
            "exact": _assertion_locality_requirements(
                locality, occurrence_identity=locality["event"].identity
            ),
            "relation_missing": _assertion_locality_requirements(
                missing_locality, occurrence_identity=locality["event"].identity
            ),
            "different_occurrence": _assertion_locality_requirements(
                locality, occurrence_identity=alternate_locality["event"].identity
            ),
            "evidence_not_intact": _assertion_locality_requirements(
                corrupted_locality,
                occurrence_identity=corrupted_locality["event"].identity,
            ),
            "different_relation_occurrence": _assertion_locality_requirements(
                unrelated_locality, occurrence_identity=locality["event"].identity
            ),
        },
        "participation": {
            case: _participation_requirements(bundle, role=BYTE_PAIR_INPUT_ROLE)
            for case, bundle in {
                "exact": participation,
                "relation_missing": missing_participation,
                "different_occurrence": wrong_participation,
                "evidence_not_intact": corrupted_participation,
                "different_relation_occurrence": unrelated_participation,
            }.items()
        },
        "yield": {
            case: _occurrence_result_requirements(bundle)
            for case, bundle in {
                "exact": exact_yield,
                "relation_missing": missing_yield,
                "different_occurrence": wrong_yield,
                "evidence_not_intact": corrupted_yield,
                "different_relation_occurrence": unrelated_yield,
            }.items()
        },
    }

    assert {
        relation: {case: tuple(requirements.values()) for case, requirements in cases.items()}
        for relation, cases in actual.items()
    } == {relation: expected for relation in actual}


def test_attempt_and_success_have_distinct_locality_relations_for_exact_material():
    emission = _emission_witness()
    alternate = _emission_witness()
    wrong_attempt = dict(emission)
    wrong_attempt["attempt_locality_evidence"] = alternate[
        "attempt_locality_evidence"
    ]
    success_evidence_in_attempt_slot = dict(emission)
    success_evidence_in_attempt_slot["attempt_locality_evidence"] = emission[
        "locality_evidence"
    ]

    assert emission["attempt"].exact_material == emission["event"].exact_material
    assert _emission_attempt_locality_witness(emission) == EXACT
    assert _emission_attempt_locality_witness(wrong_attempt) == MISSING
    assert (
        _emission_attempt_locality_witness(success_evidence_in_attempt_slot)
        == MISSING
    )


def test_successful_emission_locality_binds_the_exact_representation():
    exact = _emission_witness()
    different = dict(exact)
    evidence = deepcopy(exact["locality_evidence"])
    evidence.material["representation_reference"] = "another-representation"
    evidence.material["locality_relation"]["first_subject"] = (
        "another-representation"
    )
    different["locality_evidence"] = evidence

    assert _emission_locality_requirements(exact) == {
        "exact_relation": True,
        "occurrence_witness": True,
        "intact_evidence": True,
    }
    assert _emission_locality_requirements(different) == {
        "exact_relation": False,
        "occurrence_witness": True,
        "intact_evidence": True,
    }


def test_representation_act_has_an_exact_yield_relation_without_asserting_participation():
    representation = _representation_witness()
    alternate = _representation_witness()
    missing = dict(representation)
    missing["evidence_of_yield_relation"] = None
    different_occurrence = dict(representation)
    different_occurrence["evidence_of_yield_relation"] = alternate["evidence_of_yield_relation"]
    missing_locality = dict(representation)
    missing_locality["locality_evidence"] = None
    wrong_locality = dict(representation)
    wrong_locality["locality_evidence"] = alternate["locality_evidence"]

    assert _representation_locality_witness(representation) == EXACT
    assert _representation_locality_witness(missing_locality) == MISSING
    assert _representation_locality_witness(wrong_locality) == MISSING
    assert _occurrence_result_witness(representation) == EXACT
    assert _occurrence_result_witness(missing) == MISSING
    assert _occurrence_result_witness(different_occurrence) == MISSING
    assert "input_role" not in representation["event"].material


def test_changed_relation_anatomy_is_detected():
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))
    grammar["relations"]["yield"]["from"] = "result"

    try:
        _assert_relation_anatomy(
            grammar, _relation_witness_specs()
        )
    except AssertionError:
        pass
    else:
        raise AssertionError("reversed Yield anatomy escaped witness Fidelity")


def test_content_and_locality_subjects_do_not_establish_locality_relation():
    ledger = EventLedger()
    content = {"subject": "x", "standing": "Unknown"}
    locality = ledger.append("test.locality", dict(content), locality_identity="s")

    assert (
        _content_locality_witness(
            content, locality=locality, occurrence_identity=locality.identity
        )
        == EXACT
    )
    second_locality = ledger.append(
        "test.locality", dict(content), locality_identity="s"
    )
    assert content
    assert second_locality.material == locality.material
    assert second_locality.identity != locality.identity
    assert (
        _content_locality_witness(
            content,
            locality=second_locality,
            occurrence_identity=locality.identity,
        )
        == MISSING
    )


def test_assertion_clause_is_checked_against_a_live_byte_assertion():
    clause = _clause("01.Standing.D.1")
    witness = _assertion_witness(_byte_measurement_witness())

    assert set(witness) == {"identity", *clause["responsibility"]["coordinates"]}
    assert witness == {
        "identity": EXACT,
        "Evidence": EXACT,
        "provenance": EXACT,
        "Scope": EXACT,
        "Authority": EXACT,
        "conflicts": UNKNOWN,
        "limits": EXACT,
        "Unknown": EXACT,
        "Standing": EXACT,
    }


def test_asserted_content_identity_includes_scope_but_not_locality():
    ledger = EventLedger()
    for locality_identity in ("source-one", "source-two"):
        run_persistent_operator_console(
            ledger=ledger,
            locality_identity=locality_identity,
            input_stream=binary_input("t\n"),
            output_stream=StringIO(),
        )

    first = _record_byte_measurement(
        ledger,
        source_localities=("source-one",),
        recording_locality_identity="measurement-one",
    )
    repeated = _record_byte_measurement(
        ledger,
        source_localities=("source-one",),
        recording_locality_identity="measurement-two",
    )
    other_scope = _record_byte_measurement(
        ledger,
        source_localities=("source-two",),
        recording_locality_identity="measurement-three",
    )

    def count_assertion(event):
        return next(
            assertion
            for assertion in event.material["assertions"]
            if assertion["result"] == "count"
            and assertion["assertion_subject"].get("representation") == 116
        )

    first_assertion = count_assertion(first)
    repeated_assertion = count_assertion(repeated)
    other_scope_assertion = count_assertion(other_scope)
    assert first_assertion["dimensions"]["content"] == repeated_assertion[
        "dimensions"
    ]["content"]
    assert first_assertion["dimensions"]["identity"] == repeated_assertion[
        "dimensions"
    ]["identity"]
    assert first.identity != repeated.identity
    assert first_assertion["dimensions"]["content"] == other_scope_assertion[
        "dimensions"
    ]["content"]
    assert first_assertion["assertion_scope"] != other_scope_assertion[
        "assertion_scope"
    ]
    assert first_assertion["dimensions"]["identity"] != other_scope_assertion[
        "dimensions"
    ]["identity"]


def test_applicability_clause_is_checked_against_a_live_pair_determination():
    clause = _clause("01.Standing.E.1")
    witness = _applicability_witness(_recorded_applicability())

    assert set(witness) == set(clause["coordinates"])
    assert witness == {
        "input_identity": EXACT,
        "exact_Act": EXACT,
        "subject": EXACT,
        "result_boundary": EXACT,
        "Scope": EXACT,
        "locality": EXACT,
        "Authority": EXACT,
        "participants_and_roles": EXACT,
        "provenance": EXACT,
        "Standing": EXACT,
        "support_relation_Standing": INAPPLICABLE,
        "current_Standing": INAPPLICABLE,
        "occurrence_identity": EXACT,
        "known_loss": UNKNOWN,
        "conflicts": EXACT,
        "Unknown": EXACT,
        "negative_Authority": EXACT,
    }


def test_input_is_an_open_act_local_role_before_participation():
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))
    bundle = _recorded_applicability()
    applicability = bundle["applicability"]

    assert grammar["input_role"] == {
        "kind": "Act_local_role",
        "preserves": ["subject_identity"],
        "distinct_from": [
            "subject",
            "candidate",
            "locality",
            "Applicability",
            "Admission",
            "participation",
            "input_to_result_support",
        ],
    }
    assert applicability["input_role"] == BYTE_PAIR_INPUT_ROLE
    assert applicability["addressed_act_occurrence_identity"] is None


def _assert_role_distinctions(distinctions: dict) -> None:
    assert distinctions == {
        "distinct_coordinates": [
            "subject",
            "candidate",
            "Participation_relation",
        ],
        "ordered_coordinate_pair": [
            ["subject", "candidate"],
            ["candidate", "subject"],
            ["subject", "Participation_relation"],
            ["Participation_relation", "subject"],
            ["candidate", "Participation_relation"],
            ["Participation_relation", "candidate"],
        ],
        "candidate_coordinates": [
            "applicable_source_role",
            "Representation_Act_occurrence",
            "Scope",
            "Authority",
            "provenance",
            "Unknown",
        ],
        "Participation_relation_coordinates": {
            "book_clause": "01.Standing.E.1",
            "from": "subject",
            "to": "Act_occurrence",
            "coordinate": "role",
            "requires": [
                "exact_relation",
                "occurrence_witness",
                "intact_evidence",
            ],
        },
        "standing_not_established": [
            "candidate_by_subject_identity",
            "Participation_relation_by_subject_identity",
            "Participation_by_candidate_identity",
            {
                "first_subject": "ordered_coordinate_pair",
                "relation": "establishes",
                "second_subject": "relation",
                "standing": "not_established",
            },
        ],
    }
    assert len(distinctions["ordered_coordinate_pair"]) == 6
    assert {
        tuple(reversed(pair))
        for pair in distinctions["ordered_coordinate_pair"]
    } == {
        tuple(pair) for pair in distinctions["ordered_coordinate_pair"]
    }
    assert all(
        first != second
        for first, second in distinctions["ordered_coordinate_pair"]
    )
    assert distinctions["standing_not_established"][-1]["standing"] == (
        "not_established"
    )


def test_subject_candidate_and_participation_relation_are_distinguished_in_both_directions():
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))
    distinctions = grammar["role_distinctions"]

    _assert_role_distinctions(distinctions)
    assert distinctions["Participation_relation_coordinates"] == grammar[
        "relations"
    ]["participation"]


def test_role_distinctions_refuse_direction_collapse_and_identity_promotion():
    distinctions = json.loads(GRAMMAR.read_text(encoding="utf-8"))[
        "role_distinctions"
    ]

    collapsed_direction = deepcopy(distinctions)
    collapsed_direction["ordered_coordinate_pair"][1] = list(
        collapsed_direction["ordered_coordinate_pair"][0]
    )

    def assert_refused(changed: dict) -> None:
        try:
            _assert_role_distinctions(changed)
        except AssertionError:
            return
        raise AssertionError("compressed role distinction escaped comparison")

    assert_refused(collapsed_direction)

    missing_comparison = deepcopy(distinctions)
    missing_comparison["ordered_coordinate_pair"].pop()
    assert_refused(missing_comparison)

    promoted_by_identity = deepcopy(distinctions)
    promoted_by_identity["standing_not_established"][-1]["standing"] = "established"
    assert_refused(promoted_by_identity)

    compressed_coordinates = deepcopy(distinctions)
    compressed_coordinates["candidate_coordinates"] = list(
        compressed_coordinates["Participation_relation_coordinates"]
    )
    assert_refused(compressed_coordinates)


def test_candidate_clause_preserves_coordinates_without_promoting_the_subject():
    clause = _clause("01.Source.E")
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))

    assert clause == {
        "subject": "candidate",
        "book_material_reference": "01.Source.E",
        "grammar": "established",
        "recorded_occurrence_kind": ["event_occurrence"],
        "preserves": [
            "applicable_source_role",
            "Representation_Act_occurrence",
            "Scope",
            "Authority",
            "provenance",
            "Unknown",
        ],
        "standing_not_established": [
            "Act_occurrence_by_candidate_identity",
            "occurrence_result_relation_by_candidate_identity",
            "Participation_by_candidate_identity",
        ],
        "responsibility": {
            "responsible_boundary": "this_Seed",
            "assignment": "this_Book",
            "exact_Act": "preserve_exact_Representation_candidate",
            "result": "candidate_Standing",
        },
        "occurrence_coordinates": [
            "Representation_occurrence",
            "Representation_source_Standing_boundary",
            "assignment_Standing_boundary",
            "destination_operator_boundary",
            "destination_operator_boundary_rule",
            "destination_operator_Locality",
            "emission_Act",
            "Scope",
            "Authority",
            "limits",
        ],
    }
    assert grammar["role_distinctions"]["candidate_coordinates"] == clause[
        "preserves"
    ]


def test_cross_boundary_participation_preserves_scope_and_limits():
    clause = _clause("01.Source.B")

    assert clause == {
        "subject": {
            "identity": "supplied_material_Participation_in_exact_Act_with_input_role",
            "first_subject": "supplied_material",
            "relation": "Participation",
            "second_subject": "exact_Act",
            "role": "input",
        },
        "book_material_reference": "01.Source.B",
        "grammar": "established",
        "recorded_occurrence_kind": [],
        "coordinates": [
            "supplied_material",
            "input_role",
            "exact_Act",
            "Act_occurrence",
            "Participation_relation",
            "carried_Scope",
            "preserved_limits",
        ],
        "preserves": ["carried_Scope", "preserved_limits"],
        "coordinates_preserved_through": [
            "summarizing",
            "indexing",
            "citing",
            "comparing",
            "representing",
            "attaching",
        ],
        "standing_not_established": ["Authority_relocation"],
    }
    assert clause["preserves"] == clause["coordinates"][-2:]


def test_participation_relation_coordinates_match_the_role_distinction():
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))

    assert grammar["relations"]["participation"] == grammar[
        "role_distinctions"
    ]["Participation_relation_coordinates"]


def test_live_participation_is_not_source_b_by_relation_identity():
    clause = _clause("01.Source.B")
    emission = _emission_witness()

    assert _emission_participation_witness(emission) == EXACT
    assert not set(clause["preserves"]) <= set(emission["act_evidence"].material)
    assert "01.Source.B" not in REPRESENTATION_EVENT_KIND_RESPONSIBILITIES.values()


def test_candidate_coordinate_order_is_the_exact_book_order():
    clause = _clause("01.Source.E")
    source_book = (
        GRAMMAR.parent / "chapters" / "01_source_coordinates_and_grammar.md"
    ).read_text(encoding="utf-8")
    sentence = next(
        line
        for line in source_book.splitlines()
        if line.startswith("A candidate preserves every applicable source role")
    ).lower()
    phrases = tuple(
        coordinate.replace("_", " ").lower()
        for coordinate in clause["preserves"]
    )
    positions = tuple(sentence.index(phrase) for phrase in phrases)
    pairs_of_adjacent_positions = tuple(
        (positions[position], positions[position + 1])
        for position in range(len(positions) - 1)
    )

    assert all(
        first_position < second_position
        for first_position, second_position in pairs_of_adjacent_positions
    )


def test_participation_requires_exact_subject_role_and_act_occurrence():
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))
    bundle = _recorded_applicability()

    assert grammar["relations"]["participation"] == {
        "book_clause": "01.Standing.E.1",
        "from": "subject",
        "to": "Act_occurrence",
        "coordinate": "role",
        "requires": ["exact_relation", "occurrence_witness", "intact_evidence"],
    }
    assert _participation_witness(bundle, role=BYTE_PAIR_INPUT_ROLE) == EXACT
    assert _participation_witness(bundle, role="some other role") == MISSING

    assert bundle["applicability"]["dimensions"]["standing"] == "applicable"
    assert bundle["pair_event"].material["act_occurrence_identity"]
    bundle["pair_act_evidence"] = None
    assert _participation_witness(bundle, role=BYTE_PAIR_INPUT_ROLE) == MISSING


def test_unjoined_subjects_do_not_witness_an_input_to_act_relation():
    grammar = _witness_grammar()
    bundle = _recorded_applicability()
    bundle["act_evidence"] = None
    witness = _applicability_witness(bundle)

    assert bundle["applicability"]["input_assertion_reference"]
    assert bundle["applicability"]["addressed_act_identity"]
    assert bundle["applicability"]["applicability_act_occurrence_identity"]
    assert grammar["relation_witness_coordinates"] == {
        "standing_not_established": [
            {
                "first_subject": "subject_presence",
                "relation": "establishes",
                "second_subject": "relation",
                "standing": "not_established",
            }
        ],
        "families": {
            "candidate_participation": ["exact_relation", "occurrence_witness"],
            "participation": [
                "exact_relation",
                "occurrence_witness",
                "intact_evidence",
            ],
            "locality": [
                "exact_relation",
                "occurrence_witness",
                "intact_evidence",
            ],
                "yield": ["exact_relation", "occurrence_witness", "intact_evidence"],
                "carried_by": [
                    "exact_relation",
                    "occurrence_witness",
                    "intact_evidence",
                ],
            },
    }
    assert witness["input_identity"] == MISSING
    assert witness["exact_Act"] == MISSING
    assert witness["occurrence_identity"] == MISSING


def test_locality_relation_clause_is_checked_against_the_live_pair_witness():
    clause = _clause("06.Locality.A")
    bundle = _recorded_applicability()
    relation = bundle["movement"].material["locality_relation"]

    assert clause["identity"] == [
        "first_subject",
        "second_subject",
        "relation_occurrence",
    ]
    assert clause["requires"] == list(_locality_requirements(bundle))
    assert relation["first_subject"] == bundle["movement"].material[
        "source_assertion_reference"
    ]
    assert relation["second_subject"] == bundle["movement"].material[
        "destination_locality"
    ]
    assert _locality_witness(bundle) == EXACT


def test_locality_fans_out_orthogonal_adversaries_for_each_live_witness():
    exact = _recorded_applicability()

    relation_missing = _recorded_applicability()
    relation_missing["movement"].material["locality_relation"]["second_subject"] = (
        "another bounded subject"
    )

    different_occurrence = _recorded_applicability()
    source_occurrence = different_occurrence["ledger"].get(
        different_occurrence["movement"].material["source_assertion_reference"][
            "recorded_occurrence_identity"
        ]
    )
    different_occurrence["movement_act_evidence"].material["locality_relation"][
        "relation_occurrence_identity"
    ] = source_occurrence.identity

    evidence_not_intact = _recorded_applicability()
    evidence_not_intact["ledger"].mark_corrupted(
        evidence_not_intact["movement_act_evidence"].identity
    )

    occurrence_of_different_relation = _recorded_applicability()
    occurrence_of_different_relation["movement"].material["movement_scope"] = "another description"

    cases = {
        "exact": exact,
        "relation_missing": relation_missing,
        "different_occurrence": different_occurrence,
        "evidence_not_intact": evidence_not_intact,
        "different_relation_occurrence": occurrence_of_different_relation,
    }
    assert {name: _locality_witness(case) for name, case in cases.items()} == {
        "exact": EXACT,
        "relation_missing": MISSING,
        "different_occurrence": MISSING,
        "evidence_not_intact": MISSING,
        "different_relation_occurrence": EXACT,
    }
    assert _locality_requirements(relation_missing) == {
        "exact_relation": False,
        "occurrence_witness": True,
        "intact_evidence": True,
    }
    assert _locality_requirements(different_occurrence) == {
        "exact_relation": True,
        "occurrence_witness": False,
        "intact_evidence": True,
    }
    assert _locality_requirements(evidence_not_intact) == {
        "exact_relation": True,
        "occurrence_witness": True,
        "intact_evidence": False,
    }


def test_occurrence_and_result_subjects_do_not_establish_their_relation():
    bundle = _byte_measurement_witness()
    assert _clause("02.Acts.A")["occurrence_to_result"] == {
        "requires": "Evidence",
        "standing_not_established": [
            {
                "first_subject": "result_existence_by_identity",
                "relation": "establishes",
                "second_subject": "occurrence_to_result_relation",
                "standing": "not_established",
            }
        ],
    }
    assert _occurrence_result_witness(bundle) == EXACT

    event = bundle["event"]
    assert event.material["act_occurrence_identity"]
    assert event.material["assertions"]
    bundle["evidence_of_yield_relation"] = None
    assert _occurrence_result_witness(bundle) == MISSING


def test_yield_relation_read_has_no_result_reencoding_surface():
    bundle = _byte_measurement_witness()
    import seed_runtime.evidence_of_yield_relation as yield_module

    assert not hasattr(yield_module, "yield_commitment")
    assert _occurrence_result_requirements(bundle) == {
        "exact_relation": True,
        "occurrence_witness": True,
        "intact_evidence": True,
    }


def _live_yield_exact_bundles() -> dict[str, dict]:
    bundles = {
        "byte_measurement": _byte_measurement_witness(),
        "representation_result": _representation_witness(),
        "successful_emission": _successful_emission_requirement_bundles()[
            "yield"
        ]["exact"],
    }
    bundles.update(
        {
            boundary: cases["exact"]
            for boundary, cases in _byte_pair_yield_requirement_bundles().items()
        }
    )
    bundles.update(
        {
            boundary: cases["exact"]
            for boundary, cases in _remaining_yield_requirement_bundles().items()
        }
    )
    assert set(bundles) == set(OCCURRENCE_BOUNDARIES_OF_YIELD_RELATION)
    return bundles


def _different_preservable_value(value):
    if type(value) is bool:
        return not value
    if type(value) is int:
        return value + 1
    if type(value) is float:
        return value + 1.0
    if type(value) is str:
        return value + "-different"
    if type(value) is list:
        return [*value, None]
    if type(value) is dict:
        different = dict(value)
        coordinate = "different"
        while coordinate in different:
            coordinate += "-different"
        different[coordinate] = None
        return different
    if value is None:
        return "different"
    raise TypeError(f"unpreservable result coordinate: {type(value).__name__}")


def _change_one_carried_yield_coordinate(bundle: dict) -> dict:
    different = dict(bundle)
    event = deepcopy(bundle["event"])
    evidence = bundle["evidence_of_yield_relation"]
    occurrence_coordinate = bundle.get(
        "recorded_result_occurrence_coordinate", "act_occurrence_identity"
    )
    for coordinate in evidence.material["coordinates_of_carried_result"]:
        carried_at = evidence.material["coordinates_of_recorded_result"][coordinate]
        if carried_at == [occurrence_coordinate]:
            continue
        containing = event.material
        for part in carried_at[:-1]:
            containing = containing[part]
        containing[carried_at[-1]] = _different_preservable_value(
            containing[carried_at[-1]]
        )
        different["event"] = event
        return different
    raise AssertionError("the Yield result has no non-occurrence coordinate")


def test_every_live_recorded_yield_result_is_bound_to_its_exact_evidence_result():
    for boundary, exact in _live_yield_exact_bundles().items():
        assert _occurrence_result_requirements(exact) == {
            "exact_relation": True,
            "occurrence_witness": True,
            "intact_evidence": True,
        }, boundary

        changed_result = _change_one_carried_yield_coordinate(exact)
        assert _occurrence_result_requirements(changed_result) == {
            "exact_relation": False,
            "occurrence_witness": True,
            "intact_evidence": True,
        }, boundary

        missing_reference = dict(exact)
        missing_reference_event = deepcopy(exact["event"])
        missing_reference_event.material["evidence_of_yield_relation_identity"] = (
            "missing-yield-evidence"
        )
        missing_reference["event"] = missing_reference_event
        assert _occurrence_result_requirements(missing_reference) == {
            "exact_relation": False,
            "occurrence_witness": True,
            "intact_evidence": True,
        }, boundary

        missing_act_reference = dict(exact)
        missing_act_reference_event = deepcopy(exact["event"])
        missing_act_reference_event.material["responsible_act_evidence_identity"] = (
            "missing-act-evidence"
        )
        missing_act_reference["event"] = missing_act_reference_event
        assert _occurrence_result_requirements(missing_act_reference) == {
            "exact_relation": False,
            "occurrence_witness": True,
            "intact_evidence": True,
        }, boundary

        missing_result_identity = dict(exact)
        missing_result_identity_event = deepcopy(exact["event"])
        missing_result_identity_event.material.pop("result_identity")
        missing_result_identity["event"] = missing_result_identity_event
        assert _occurrence_result_requirements(missing_result_identity) == {
            "exact_relation": False,
            "occurrence_witness": True,
            "intact_evidence": True,
        }, boundary

        wrong_result_identity = dict(exact)
        wrong_result_identity_event = deepcopy(exact["event"])
        wrong_result_identity_event.material["result_identity"] = (
            "different result identity"
        )
        wrong_result_identity["event"] = wrong_result_identity_event
        assert _occurrence_result_requirements(wrong_result_identity) == {
            "exact_relation": False,
            "occurrence_witness": True,
            "intact_evidence": True,
        }, boundary

        wrong_evidence_result_identity = dict(exact)
        wrong_evidence_of_yield_relation = deepcopy(exact["evidence_of_yield_relation"])
        wrong_evidence_of_yield_relation.material["result_identity"] = (
            "different result identity"
        )
        wrong_evidence_result_identity["evidence_of_yield_relation"] = wrong_evidence_of_yield_relation
        assert _occurrence_result_requirements(wrong_evidence_result_identity) == {
            "exact_relation": False,
            "occurrence_witness": True,
            "intact_evidence": True,
        }, boundary

        wrong_yield_act_reference = dict(exact)
        wrong_evidence_of_yield_relation = deepcopy(exact["evidence_of_yield_relation"])
        wrong_evidence_of_yield_relation.material["responsible_act_evidence_identity"] = (
            "different-act-evidence"
        )
        wrong_yield_act_reference["evidence_of_yield_relation"] = wrong_evidence_of_yield_relation
        assert _occurrence_result_requirements(wrong_yield_act_reference) == {
            "exact_relation": False,
            "occurrence_witness": True,
            "intact_evidence": True,
        }, boundary

        wrong_act = dict(exact)
        wrong_act_evidence = deepcopy(exact["act_evidence"])
        wrong_act_evidence.material["act"] = "different Act"
        wrong_act["act_evidence"] = wrong_act_evidence
        assert _occurrence_result_requirements(wrong_act) == {
            "exact_relation": False,
            "occurrence_witness": True,
            "intact_evidence": True,
        }, boundary

        wrong_responsibility = dict(exact)
        wrong_responsibility_evidence = deepcopy(exact["act_evidence"])
        wrong_responsibility_evidence.material["responsibility"] = (
            "different Responsibility"
        )
        wrong_responsibility["act_evidence"] = wrong_responsibility_evidence
        assert _occurrence_result_requirements(wrong_responsibility) == {
            "exact_relation": False,
            "occurrence_witness": True,
            "intact_evidence": True,
        }, boundary

        wrong_boundary = dict(exact)
        wrong_boundary_evidence = deepcopy(exact["act_evidence"])
        wrong_boundary_evidence.material["responsible_boundary"] = (
            "different responsible boundary"
        )
        wrong_boundary["act_evidence"] = wrong_boundary_evidence
        assert _occurrence_result_requirements(wrong_boundary) == {
            "exact_relation": False,
            "occurrence_witness": True,
            "intact_evidence": True,
        }, boundary

        absent_act_evidence = dict(exact)
        absent_act_evidence["act_evidence"] = None
        assert _occurrence_result_requirements(absent_act_evidence) == {
            "exact_relation": False,
            "occurrence_witness": False,
            "intact_evidence": False,
        }, boundary

        exact["ledger"].mark_corrupted(exact["act_evidence"].identity)
        assert _occurrence_result_requirements(exact) == {
            "exact_relation": True,
            "occurrence_witness": True,
            "intact_evidence": False,
        }, boundary


def test_different_yield_occurrences_do_not_share_result_identity():
    factories = {
        "complete_candidate_standing_applicability": (
            _complete_candidate_standing_applicability_yield_witness
        ),
        "complete_candidate_standing": (
            _complete_candidate_standing_yield_witness
        ),
        "representation_candidate": _representation_candidate_yield_witness,
        "representation_admission": _representation_admission_yield_witness,
        "representation_emission_applicability": (
            _representation_emission_applicability_yield_witness
        ),
        "byte_measurement": _byte_measurement_witness,
        "representation_result": _representation_witness,
        "successful_emission": _emission_witness,
        "assertion_locality_movement": _assertion_locality_movement_yield_witness,
        "occurrence_position_measurement": _occurrence_position_yield_witness,
        "byte_pair_occurrence_position_measurement": (
            _byte_pair_occurrence_position_yield_witness
        ),
            "measurement_of_recurrent_byte_pair_occurrence_position": _pair_occurrence_yield_witness,
            "shared_pair_position_applicability": (
                _shared_position_applicability_yield_witness
            ),
            "shared_pair_position_measurement": (
                _shared_position_measurement_yield_witness
            ),
        "recorded_pair_measurement_comparison_applicability": (
            _recorded_pair_measurement_comparison_applicability_yield_witness
        ),
        "recorded_pair_measurement_comparison": (
            _recorded_pair_measurement_comparison_yield_witness
        ),
        "comparison_of_ordered_relation_path_with_recorded_pair_findings_applicability": (
            _ordered_relation_path_pair_finding_comparison_applicability_yield_witness
        ),
        "comparison_of_ordered_relation_path_with_recorded_pair_findings_compare": (
            _ordered_relation_path_pair_finding_comparison_yield_witness
        ),
        "addressed_byte_occurrence_reference_determination_applicability": (
            _addressed_byte_occurrence_reference_determination_applicability_yield_witness
        ),
        "addressed_byte_occurrence_reference_determination": (
            _addressed_byte_occurrence_reference_determination_yield_witness
        ),
        "failed_boundary": _failed_boundary_yield_witness,
        "material_ingest": _material_ingest_yield_witness,
        "operator_material_acquire": _operator_material_acquire_yield_witness,
        "operator_invocation_locality_relation": (
            _operator_system_locality_yield_witness
        ),
        "standing_boundary_reference": _standing_boundary_reference_yield_witness,
        "recorded_standing_boundary_locality_relation": (
            _recorded_standing_boundary_locality_yield_witness
        ),
        "standing_locality_continuation": (
            _standing_locality_continuation_yield_witness
        ),
    }
    pairs = {
        boundary: (factory(), factory())
        for boundary, factory in factories.items()
    }
    first_pair = _recorded_applicability()
    second_pair = _recorded_applicability()
    pairs["byte_pair_applicability"] = (first_pair, second_pair)
    pairs["byte_pair_measurement"] = (
        {"event": first_pair["pair_event"]},
        {"event": second_pair["pair_event"]},
    )

    assert set(pairs) == set(OCCURRENCE_BOUNDARIES_OF_YIELD_RELATION)
    for boundary, (first, second) in pairs.items():
        occurrence_coordinate = (
            "applicability_act_occurrence_identity"
            if boundary in {
                "byte_pair_applicability",
                "representation_emission_applicability",
                "shared_pair_position_applicability",
                "comparison_of_ordered_relation_path_with_recorded_pair_findings_applicability",
                "addressed_byte_occurrence_reference_determination_applicability",
            }
            else "movement_act_occurrence_identity"
            if boundary == "assertion_locality_movement"
            else "determination_act_occurrence_identity"
            if boundary == "addressed_byte_occurrence_reference_determination"
            else "act_occurrence_identity"
        )
        assert first["event"].material[occurrence_coordinate] != second[
            "event"
        ].material[occurrence_coordinate], boundary
        assert first["event"].material["result_identity"] != second[
            "event"
        ].material["result_identity"], boundary


def test_exact_act_clause_is_checked_against_live_byte_measurement():
    clause = _clause("02.Acts.A")
    bundle = _byte_measurement_witness()
    witness = _act_occurrence_witness(bundle)

    assert set(witness) == set(
        _coordinate_identities(clause["responsibility"]["coordinates"])
    )
    assert set(witness.values()) == {EXACT}
    assert bundle["event"].material["addressed_act_identity"] != bundle["event"].material[
        "act_occurrence_identity"
    ]
    assert _occurrence_result_witness(bundle) == EXACT
    assert {
        "first_subject": "emission_Act_occurrence",
        "relation": "Yield",
        "second_subject": "accepted_exact_Representation_result",
    } in clause["witness_relations"]


def test_representation_source_clause_is_checked_against_one_live_result():
    clause = _clause("01.Source.A")
    bundle = _sourced_representation_witness()
    witness = _representation_source_witness(bundle)
    distinctions = _representation_source_distinctions(bundle)

    assert set(witness) == set(
        _coordinate_identities(clause["responsibility"]["coordinates"])
    )
    assert set(witness.values()) == {EXACT}
    assert list(distinctions) == [
        tuple(distinction) for distinction in clause["distinct_from"]
    ]
    assert set(distinctions.values()) == {True}


def test_exact_source_material_rule_is_checked_against_one_live_representation():
    clause = _clause("01.Source.A")
    witness = _sourced_representation_witness()
    event = witness["event"]
    rule = clause["exact_material_representation_rule"]

    assert rule == {
        "first_subject": "Representation_exact_material",
        "relation": "preserves",
        "second_subject": {
            "first_subject": "exact_material",
            "relation": "of",
            "second_subject": "source_result",
        },
        "preserves": "source_result_occurrence",
        "standing_not_established": [
            "what_material_represents",
            "represented_relation",
        ],
    }
    assert event.material["representation_rule"] == (
        EXACT_SOURCE_MATERIAL_REPRESENTATION_RULE
    )
    assert event.exact_material == witness["source"].exact_material


def test_exact_material_admission_establishes_one_rule_relation():
    clause = _clause("01.Standing.E")["Admission_occurrence"]
    material = _representation_admission_yield_witness()["event"].material

    assert clause["rule_relation"] == {
        "first_subject": {
            "identity": "Representation_rule_preserve_exact_material_of_source_result",
            "first_subject": "Representation_rule",
            "relation": "preserve",
            "second_subject": {
                "first_subject": "exact_material",
                "relation": "of",
                "second_subject": "source_result",
            },
        },
        "relation": "applicable_to",
        "second_subject": "destination_boundary_rule_write_exact_material",
        "preserves": [
            "Representation_rule",
            "destination_boundary_rule",
        ],
        "standing_not_established": [
            "relation_by_write_function",
            "effects_beyond_boundary",
        ],
    }
    assert material["representation_rule_to_boundary_rule_relation"] == {
        "first_subject": EXACT_SOURCE_MATERIAL_REPRESENTATION_RULE,
        "relation": "applicable_to",
        "second_subject": EXACT_MATERIAL_WRITE_BOUNDARY_RULE,
    }
    assert exact_material_representation_rule_is_applicable_to_boundary_rule(
        EXACT_SOURCE_MATERIAL_REPRESENTATION_RULE,
        EXACT_MATERIAL_WRITE_BOUNDARY_RULE,
    )
    assert not exact_material_representation_rule_is_applicable_to_boundary_rule(
        EXACT_SOURCE_MATERIAL_REPRESENTATION_RULE,
        "render terminal cells",
    )


def test_representation_source_and_standing_boundary_remain_distinct_coordinates():
    ledger = _IntegrityAdversaryLedger()
    source = ingest_material(
        ledger,
        locality_identity="representation-source",
        exact_bytes=b"source material",
        source_role="operator",
        source_boundary="exact source boundary",
    )
    later = ingest_material(
        ledger,
        locality_identity="representation-source",
        exact_bytes=b"later material",
        source_role="operator",
        source_boundary="later source boundary",
    )
    representation = record_operator_representation(
        ledger,
        locality_identity="representation-source",
        locality_standing=read_operator_locality_standing(
            ledger, locality_identity="representation-source"
        ),
        source_occurrence_reference=source.identity,
    )
    event = ledger.get(representation["representation_event_identity"])
    bundle = {
        "ledger": ledger,
        "source": source,
        "event": event,
        "act_evidence": ledger.get(
            event.material["responsible_act_evidence_identity"]
        ),
        "locality_evidence": ledger.get(
            event.material["locality_evidence_identity"]
        ),
        "evidence_of_yield_relation": ledger.get(event.material["evidence_of_yield_relation_identity"]),
    }

    assert source.identity != later.identity
    assert event.material["locality_standing_through_event_occurrence_identity"] == later.identity
    assert set(_representation_source_witness(bundle).values()) == {EXACT}


def test_representation_result_act_and_locality_species_keep_their_clauses():
    assert REPRESENTATION_EVENT_KIND_RESPONSIBILITIES[
        REPRESENTATION_RECORDED_KIND
    ] == "01.Source.A"
    assert REPRESENTATION_EVENT_KIND_RESPONSIBILITIES[
        REPRESENTATION_ACT_EVIDENCE_KIND
    ] == "02.Acts.A"
    assert REPRESENTATION_EVENT_KIND_RESPONSIBILITIES[
        REPRESENTATION_LOCALITY_EVIDENCE_KIND
    ] == "06.Locality.A"


def test_candidate_and_admission_species_keep_their_distinct_clauses():
    assert REPRESENTATION_ADMISSION_EVENT_KIND_RESPONSIBILITIES == {
        REPRESENTATION_CANDIDATE_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND: "01.Source.E",
        REPRESENTATION_CANDIDATE_ACT_EVIDENCE_KIND: "02.Acts.A",
        REPRESENTATION_CANDIDATE_RECORDED_KIND: "01.Source.E",
        EXACT_MATERIAL_REPRESENTATION_ADMISSION_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND: "01.Standing.E",
        EXACT_MATERIAL_REPRESENTATION_ADMISSION_ACT_EVIDENCE_KIND: "02.Acts.A",
        EXACT_MATERIAL_REPRESENTATION_ADMISSION_RECORDED_KIND: "01.Standing.E",
    }


def test_emission_applicability_species_keep_act_and_result_clauses_distinct():
    assert REPRESENTATION_APPLICABILITY_EVENT_KIND_RESPONSIBILITIES == {
        REPRESENTATION_EMISSION_APPLICABILITY_ACT_EVIDENCE_KIND: "02.Acts.A",
        REPRESENTATION_EMISSION_APPLICABILITY_RECORDED_KIND: "01.Standing.E.1",
    }


def test_emission_applicability_witnesses_every_declared_coordinate():
    clause = _clause("01.Standing.E.1")[
        "emission_input_Applicability_occurrence"
    ]
    material = _representation_emission_applicability_yield_witness()[
        "event"
    ].material
    witness = {
        "Admission_result_occurrence": material[
            "admission_result_event_identity"
        ],
        "Representation_occurrence": material["representation_reference"][
            "representation_event_identity"
        ],
        "input_identity": material["input_identity"],
        "input_role": material["input_role"],
        "emission_Act": material["addressed_act_identity"],
        "emission_Act_occurrence": material[
            "addressed_act_occurrence_identity"
        ],
        "emission_result_boundary": material[
            "addressed_result_boundary_identity"
        ],
        "Standing_boundary": material["standing_boundary_identity"],
        "destination_operator_boundary": material[
            "destination_operator_boundary_identity"
        ],
        "destination_operator_boundary_rule": material[
            "destination_operator_boundary_rule"
        ],
        "destination_operator_Locality": material[
            "destination_operator_locality_identity"
        ],
        "Scope": material["scope"],
        "Authority": material["authority"],
        "provenance": material["provenance_occurrence_references"],
        "known_loss": material["known_loss"],
        "conflicts": material["conflicts"],
        "Unknown": material["unknown"],
        "negative_Authority": material["negative_authority"],
    }

    assert tuple(witness) == tuple(clause["coordinates"])
    assert all(
        value is not None
        and (type(value) not in {str, dict} or bool(value))
        for value in witness.values()
    )
    assert material["standing"] == "applicable"
    assert material["support_relation_standing"] == "admitted"


def test_assertion_movement_result_names_and_witnesses_its_witness_clause():
    clause = _clause("03.Movement.A")
    bundle = _recorded_applicability()
    witness = _movement_coordinate_witness(bundle)

    assert BYTE_EVENT_KIND_RESPONSIBILITIES[
        bundle["movement"].kind
    ] == "03.Movement.A"
    assert BYTE_EVENT_KIND_RESPONSIBILITIES[
        ASSERTION_LOCALITY_MOVEMENT_RESPONSIBILITY_ASSIGNMENT_KIND
    ] == "03.Movement.A"
    assert set(witness) == set(clause["responsibility"]["coordinates"])
    assert set(witness.values()) == {EXACT}
    assert bundle["movement"].identity != bundle["movement"].material[
        "movement_act_occurrence_identity"
    ]


def test_assertion_movement_standing_carries_the_exact_grammar_coordinates():
    clause = _clause("03.Movement.A")
    bundle = _recorded_applicability()
    standing = read_operator_locality_standing(
        bundle["ledger"], locality_identity=bundle["movement"].locality_identity
    )
    coordinates = standing["assertion_locality_movement_occurrences"][
        bundle["movement"].identity
    ]

    grammar_coordinates = clause["destination_Standing_coordinates"][
        "assertion_locality_movement_occurrences"
    ]["carries"]
    assert set(coordinates) == {
        coordinate["identity"] if type(coordinate) is dict else coordinate
        for coordinate in grammar_coordinates
    }
    assert coordinates["source_assertion_reference"] == bundle[
        "movement"
    ].material["source_assertion_reference"]


def test_assertion_movement_coordinates_refuse_crossing_or_loss():
    adversaries = {
        "subject": lambda bundle: bundle["movement"].material.__setitem__(
            "assertion_identity", "another Assertion"
        ),
        "source_coordinates": lambda bundle: bundle["movement"].material.__setitem__(
            "source_locality", "another Locality"
        ),
        "destination_coordinates": lambda bundle: bundle[
            "movement"
        ].material.__setitem__("destination_locality", "another Locality"),
        "exact_Act": lambda bundle: bundle["movement"].material.__setitem__(
            "movement_act_identity",
            bundle["movement"].material["movement_act_occurrence_identity"],
        ),
        "Act_occurrence": lambda bundle: bundle["movement"].material[
            "locality_relation"
        ].__setitem__("relation_occurrence_identity", "another occurrence"),
        "Evidence": lambda bundle: bundle["ledger"].mark_corrupted(
            bundle["movement_act_evidence"].identity
        ),
        "Authority": lambda bundle: bundle["movement"].material.__setitem__(
            "authority", "another Authority"
        ),
        "Scope": lambda bundle: bundle["movement"].material.__setitem__(
            "movement_scope", "another Scope"
        ),
        "limits": lambda bundle: bundle["movement"].material[
            "preserved_coordinates"
        ].remove("limits"),
        "Unknown": lambda bundle: bundle["movement"].material[
            "preserved_coordinates"
        ].remove("Unknown"),
        "Standing": lambda bundle: bundle["movement"].material[
            "preserved_coordinates"
        ].remove("Standing"),
    }

    for coordinate, cross in adversaries.items():
        bundle = _recorded_applicability()
        cross(bundle)
        assert _movement_coordinate_witness(bundle)[coordinate] == MISSING


def test_standing_locality_continuation_stages_keep_distinct_clause_coordinates():
    assert CONTINUATION_EVENT_KIND_RESPONSIBILITIES[
        STANDING_LOCALITY_CONTINUATION_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND
    ] == "06.Locality.B"
    assert CONTINUATION_EVENT_KIND_RESPONSIBILITIES[
        STANDING_LOCALITY_CONTINUATION_ACT_EVIDENCE_KIND
    ] == "02.Acts.A"
    assert CONTINUATION_EVENT_KIND_RESPONSIBILITIES[
        STANDING_LOCALITY_CONTINUATION_RECORDED_KIND
    ] == "06.Locality.A"


def test_operator_material_acquire_stages_keep_distinct_clause_coordinates():
    clause = _clause("01.Source.G")
    assert clause["no_material_boundary"] == {
        "standing_not_established": [
            {
                "first_subject": "boundary_supplies_no_material",
                "relation": "establishes",
                "second_subject": "material_result",
                "standing": "not_established",
            },
            {
                "first_subject": "boundary_supplies_no_material",
                "relation": "establishes",
                "second_subject": "Yield",
                "standing": "not_established",
            },
            {
                "first_subject": "boundary_supplies_no_material",
                "relation": "establishes",
                "second_subject": "completion",
                "standing": "not_established",
            },
        ]
    }
    assert ACQUIRE_EVENT_KIND_RESPONSIBILITIES[
        OPERATOR_MATERIAL_ACQUIRE_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND
    ] == "01.Source.G"
    assert ACQUIRE_EVENT_KIND_RESPONSIBILITIES[
        OPERATOR_MATERIAL_ACQUIRE_ACT_EVIDENCE_KIND
    ] == "02.Acts.A"
    assert ACQUIRE_EVENT_KIND_RESPONSIBILITIES[
        OPERATOR_MATERIAL_ACQUIRE_RECORDED_KIND
    ] == "01.Source.G"
    assert OPERATOR_MATERIAL_ACQUIRE_LOCALITY_RELATION_OCCURRENCE_KIND == (
        OPERATOR_MATERIAL_ACQUIRE_RECORDED_KIND
    )
    locality_relation = next(
        coordinate
        for coordinate in clause["responsibility"]["coordinates"]
        if type(coordinate) is dict
        and coordinate.get("identity")
        == "operator_material_to_this_Seed_Locality_relation"
    )
    assert locality_relation == {
        "identity": "operator_material_to_this_Seed_Locality_relation",
        "assignment": {
            "standing_not_established": [
                {
                    "first_subject": "Unknown",
                    "relation": "locality",
                    "second_subject": "this_Seed",
                    "relation_occurrence": "Unknown",
                    "Evidence": "Unknown",
                }
            ]
        },
        "result": {
            "first_subject": {
                "recorded_occurrence": "operator_material_result_occurrence",
                "coordinate": "exact_material",
            },
            "relation": "locality",
            "second_subject": "this_Seed",
            "relation_occurrence": "operator_material_result_occurrence",
            "Evidence": {
                "occurrence": "operator_material_result_occurrence",
                "requires": [
                    "Responsibility_assignment",
                    "operator_boundary",
                    "Act_occurrence",
                    "Act_Evidence",
                    "Yield",
                    "exact_material_result",
                ],
                "self_reference_alone": "establishes_no_Evidence",
            },
        },
    }


def test_standing_boundary_reference_stages_keep_distinct_clause_coordinates():
    assert CHECKPOINT_EVENT_KIND_RESPONSIBILITIES[
        STANDING_BOUNDARY_REFERENCE_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND
    ] == "05.Recording.D"
    assert CHECKPOINT_EVENT_KIND_RESPONSIBILITIES[
        STANDING_BOUNDARY_REFERENCE_ACT_EVIDENCE_KIND
    ] == "02.Acts.A"
    assert CHECKPOINT_EVENT_KIND_RESPONSIBILITIES[
        STANDING_BOUNDARY_REFERENCE_RECORDED_KIND
    ] == "05.Recording.D"


def test_recorded_boundary_locality_stages_keep_distinct_clause_coordinates():
    assert BOUNDARY_LOCALITY_EVENT_KIND_RESPONSIBILITIES[
        RECORDED_STANDING_BOUNDARY_LOCALITY_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND
    ] == "06.Locality.C"
    assert BOUNDARY_LOCALITY_EVENT_KIND_RESPONSIBILITIES[
        RECORDED_STANDING_BOUNDARY_LOCALITY_ACT_EVIDENCE_KIND
    ] == "02.Acts.A"
    assert BOUNDARY_LOCALITY_EVENT_KIND_RESPONSIBILITIES[
        RECORDED_STANDING_BOUNDARY_LOCALITY_RECORDED_KIND
    ] == "06.Locality.A"


def test_operator_system_locality_stages_keep_distinct_witness_clauses():
    assert SYSTEM_LOCALITY_EVENT_KIND_RESPONSIBILITIES[
        OPERATOR_SYSTEM_LOCALITY_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND
    ] == "06.Locality.D"
    assert SYSTEM_LOCALITY_EVENT_KIND_RESPONSIBILITIES[
        OPERATOR_SYSTEM_LOCALITY_ACT_EVIDENCE_KIND
    ] == "02.Acts.A"
    assert SYSTEM_LOCALITY_EVENT_KIND_RESPONSIBILITIES[
        OPERATOR_SYSTEM_LOCALITY_RECORDED_KIND
    ] == "06.Locality.A"


def test_representation_source_act_and_locality_witnesses_do_not_absorb_each_other():
    source_missing = _sourced_representation_witness()
    for material in (
        source_missing["event"].material,
        source_missing["evidence_of_yield_relation"].material["result"],
        source_missing["locality_evidence"].material["carried_content"],
    ):
        material["source_occurrence_reference"] = None

    source_witness = _representation_source_witness(source_missing)
    assert source_witness["source_occurrence_reference"] == MISSING
    assert source_witness["locality_standing_through_event_occurrence_identity"] == MISSING
    assert _representation_act_evidence_witness(source_missing)
    assert _representation_locality_witness(source_missing) == EXACT

    act_missing = _sourced_representation_witness()
    act_missing["act_evidence"] = None

    assert set(_representation_source_witness(act_missing).values()) == {EXACT}
    assert not _representation_act_evidence_witness(act_missing)
    assert _representation_locality_witness(act_missing) == EXACT

    locality_missing = _sourced_representation_witness()
    locality_missing["locality_evidence"] = None

    assert set(_representation_source_witness(locality_missing).values()) == {EXACT}
    assert _representation_act_evidence_witness(locality_missing)
    assert _representation_locality_witness(locality_missing) == MISSING


def test_representation_source_distinction_adversaries_collapse_one_boundary_each():
    result_is_act = _sourced_representation_witness()
    result_is_act["event"].material["result_identity"] = result_is_act[
        "event"
    ].material["act_occurrence_identity"]
    assert _representation_source_distinctions(result_is_act) == {
        ("Representation_result", "exact_Act_occurrence"): False,
        ("Representation_source_coordinates", "Locality_relation"): True,
    }

    source_is_locality = _sourced_representation_witness()
    source_is_locality["event"].material["locality_evidence_identity"] = (
        source_is_locality["event"].material["source_occurrence_reference"]
    )
    assert _representation_source_distinctions(source_is_locality) == {
        ("Representation_result", "exact_Act_occurrence"): True,
        ("Representation_source_coordinates", "Locality_relation"): False,
    }


def test_representation_source_coordinate_adversaries_preserve_exact_dependencies():
    mutations = {
        "responsibility": lambda material: material["dimensions"].__setitem__(
            "responsibility", REPRESENTATION_EMISSION_INPUT_ROLE
        ),
        "source_provenance": lambda material: material["dimensions"].__setitem__(
            "source_provenance", "different provenance"
        ),
        "scope_locality": lambda material: material["dimensions"].__setitem__(
            "scope_locality", "different locality"
        ),
        "authority": lambda material: material["dimensions"].__setitem__(
            "authority", "different authority"
        ),
        "known_loss": lambda material: material.__setitem__("known_loss", None),
        "conflicts": lambda material: material.__setitem__("conflicts", None),
        "unknown": lambda material: material.__setitem__("unknown", None),
    }

    for changed, mutate in mutations.items():
        bundle = _sourced_representation_witness()
        mutate(bundle["event"].material)
        witness = _representation_source_witness(bundle)
        expected_missing = {changed}

        assert {
            coordinate
            for coordinate, standing in witness.items()
            if standing == MISSING
        } == expected_missing


def test_measurement_result_clause_is_checked_against_live_byte_pair_and_position_results():
    clause = _clause("01.Source.D")
    byte = _byte_measurement_witness()
    pair_bundle = _recorded_applicability()
    pair = {
        "event": pair_bundle["pair_event"],
        "ledger": pair_bundle["ledger"],
    }
    position = _occurrence_position_yield_witness()
    pair_occurrence = _pair_occurrence_yield_witness()
    shared_position = _shared_position_measurement_yield_witness()

    assert clause["findings"] == [
        "count",
        "recurrence",
        "position",
        "ordered_relation_path",
    ]
    for bundle in (byte, pair, position, pair_occurrence):
        witness = _measurement_result_witness(bundle)
        distinctions = _measurement_result_distinctions(bundle)

        assert set(witness) == set(clause["responsibility"]["coordinates"])
        assert set(witness.values()) == {EXACT}
        assert list(distinctions) == [
            tuple(distinction) for distinction in clause["distinct_from"]
        ]
        assert set(distinctions.values()) == {True}

    shared_witness = _measurement_result_witness(shared_position)
    assert shared_witness == {
        coordinate: (
            MISSING
            if coordinate == "responsibility_assignment_evidence"
            else EXACT
        )
        for coordinate in clause["responsibility"]["coordinates"]
    }


def test_standing_measurement_declarations_match_the_curated_runtime_order():
    from seed_runtime.standing_measurement_declarations import (
        STANDING_MEASUREMENT_DECLARATIONS,
    )

    declared = _clause("01.Source.D")["standing_emission_declarations"]

    assert tuple(
        (
            coordinate["order"],
            coordinate["book_clause"],
            coordinate["measurement"]["identity"],
        )
        for coordinate in declared
    ) == tuple(
        (
            declaration.order,
            declaration.book_clause_identity,
            measurement,
        )
        for declaration, measurement in zip(
            STANDING_MEASUREMENT_DECLARATIONS,
            (
                "measurement_of_position_coordinates_of_byte_pair_occurrences",
                "measurement_of_exact_byte_occurrences",
            ),
            strict=True,
        )
    )
    assert _clause("01.Source.D")["declared_measurements"][
        "measurement_of_exact_byte_occurrences"
    ] == {
        "measurement": {
            "subject": {
                "first_subject": "exact_byte_occurrences",
                "relation": "of",
                "second_subject": "exact_Ingest_source_set",
            },
            "findings": ["count", "recurrence"],
        },
        "input_subject": "exact_Ingest_source_set",
        "bounded_by": ["source_localities", "completeness_boundary"],
        "standing_not_established": ["represented_relation"],
    }


def test_each_declared_measurement_names_its_finding_and_responsible_occurrence():
    assert _clause("02.Acts.A")["declared_Measurement_finding_occurrence_pair"] == {
        "first_subject": "exact_declared_Measurement_Act_occurrence",
        "relation": "establishes",
        "second_subject": "finding",
        "finding": "declared_Measurement_result_finding",
        "responsible_occurrence_reference": "exact_declared_Measurement_Act_occurrence",
        "evidence_reference": {
            "first_subject": "Evidence",
            "relation": "of",
            "second_subject": ["Act_occurrence", "Yield_relation"],
        },
        "result_boundary": "exact_result_boundary",
    }

    clause = _clause("01.Source.D")
    assert clause["recorded_occurrence_kind"] == ["event_occurrence"]
    assert "assertions" in clause["responsibility"]["coordinates"]
    for declared in clause["declared_measurements"].values():
        measurement = declared["measurement"]
        finding_coordinates = tuple(
            coordinate
            for key in ("finding", "findings")
            for coordinate in (
                [measurement[key]]
                if key in measurement and isinstance(measurement[key], str)
                else measurement.get(key, [])
            )
        )
        assert finding_coordinates
        assert all(type(coordinate) is str and coordinate for coordinate in finding_coordinates)
        assert declared.get("standing_not_established")


def test_measurement_result_pronoun_is_an_exact_machine_reference():
    assert _clause("01.Source.D")["result_carries"] == {
        "first_subject": "result",
        "relation": "carries",
        "second_subject": "findings",
        "bounded_by": ["declared_rule", "declared_boundary"],
    }
    assert _clause("01.Source.D")["it_reference"] == {
        "reference": "it",
        "coordinate": "result",
    }


def test_addressed_byte_occurrence_reference_determination_keeps_exact_bounds():
    clause = _clause("01.Source.D.2")

    assert clause["subject"] == (
        "addressed_byte_occurrence_reference_determination"
    )
    assert clause["responsibility"] == {
        "kind": "addressed_byte_occurrence_reference_determination_Measurement_result_boundary",
        "responsible_boundary": "this_Seed",
        "assignment": "exact_Responsibility_assignment_occurrence",
        "Act": "declared_Measurement",
        "result": "declared_Measurement_result",
        "coordinates": [
            "responsibility_assignment_reference",
            "assignment_current_Standing",
            "direct_pair_position_result_reference",
            "addressed_source_byte_position_coordinate_reference",
            "Applicability_Act_occurrence",
            "Applicability_Act_Evidence",
            {
                "identity": "Applicability_Evidence_of_Yield_relation",
                "first_subject": "Applicability_Evidence",
                "relation": "of",
                "second_subject": "Applicability_Yield_relation",
            },
            "Applicability_result_occurrence",
            "determination_Act_occurrence",
            "determination_Act_Evidence",
            {
                "identity": "determination_Evidence_of_Yield_relation",
                "first_subject": "determination_Evidence",
                "relation": "of",
                "second_subject": "determination_Yield_relation",
            },
            "determination_result_occurrence",
            "Locality",
            "completeness_boundary",
            "Scope",
            "Authority",
            "limits",
            "Unknown",
        ],
    }
    assert clause["determination"] == {
        "addressed_coordinate_reference_occurrences": [
            {
                "first_subject": "first_position_coordinate_reference",
                "relation": "of",
                "second_subject": "addressed_byte_occurrence",
            },
            {
                "first_subject": "second_position_coordinate_reference",
                "relation": "of",
                "second_subject": "addressed_byte_occurrence",
            },
        ],
        "carries": "every_exact_pair_position_Assertion_reference_with_one_addressed_coordinate",
        "standing_not_established": "each_pair_position_Assertion_reference_with_no_addressed_coordinate",
        "order": "source_occurrence_order",
        "lawful_no_reference_result": {
            "when": {
                "standing_not_established": [
                    {
                        "first_subject": "first_position_coordinate_reference",
                        "relation": "of",
                        "second_subject": "addressed_byte_occurrence",
                    },
                    {
                        "first_subject": "second_position_coordinate_reference",
                        "relation": "of",
                        "second_subject": "addressed_byte_occurrence",
                    },
                ]
            },
            "carried_pair_position_Assertion_references": [],
        },
    }
    assert clause["occurrence_order"] == [
        "Responsibility_assignment_occurrence",
        "assignment_current_Standing",
        "Applicability_Act_occurrence",
        "Applicability_Act_Evidence",
        {
            "identity": "Applicability_Evidence_of_Yield_relation",
            "first_subject": "Applicability_Evidence",
            "relation": "of",
            "second_subject": "Applicability_Yield_relation",
        },
        "Applicability_result_occurrence",
        "determination_Act_occurrence",
        "determination_Act_Evidence",
        {
            "identity": "determination_Evidence_of_Yield_relation",
            "first_subject": "determination_Evidence",
            "relation": "of",
            "second_subject": "determination_Yield_relation",
        },
        "determination_result_occurrence",
    ]
    assert clause["distinct_from"] == [
        ["Applicability_Act_occurrence", "determination_Act_occurrence"],
        ["Applicability_Act_Evidence", "determination_Act_Evidence"],
        {
            "first_subject": {
                "identity": "Applicability_Evidence_of_Yield_relation",
                "first_subject": "Applicability_Evidence",
                "relation": "of",
                "second_subject": "Applicability_Yield_relation",
            },
            "relation": "distinct_from",
            "second_subject": {
                "identity": "determination_Evidence_of_Yield_relation",
                "first_subject": "determination_Evidence",
                "relation": "of",
                "second_subject": "determination_Yield_relation",
            },
        },
        ["Applicability_result_occurrence", "determination_result_occurrence"],
    ]
    assert clause["unsupported_coordinates"]["standing_not_established"] == [
        "addressed_occurrence_by_scalar_byte",
        "addressed_occurrence_by_scalar_position",
        "recurrence",
        "shared_position_relation",
        "Participation_beyond_exact_Act",
        "represented_relation",
        "other_relation",
    ]
    registered = _relation_occurrence_fidelity_findings()
    assert (
        "yield",
        "addressed_byte_occurrence_reference_determination_applicability",
    ) in registered
    assert (
        "yield",
        "addressed_byte_occurrence_reference_determination",
    ) in registered


def test_pair_occurrence_measurement_is_structured_in_the_grammar_representation():
    declared = _clause("01.Source.D")["declared_measurements"][
        "measurement_of_recurrent_byte_pair_occurrence_position"
    ]
    result_witness = _pair_occurrence_yield_witness()
    material = result_witness["event"].material

    assert declared == {
        "measurement": {
            "subject": {
                "first_subject": "occurrence",
                "relation": "of",
                "second_subject": "recurrent_byte_pair",
            },
            "finding": "position",
        },
        "witness": {
            "event_occurrences": [
                {
                    "first_subject": "Evidence",
                    "relation": "of",
                    "second_subject": "Act_occurrence",
                    "recording": "recorded",
                },
                {
                    "first_subject": "Evidence",
                    "relation": "of",
                    "second_subject": "Yield_relation",
                    "recording": "recorded",
                },
                {
                    "first_subject": "recording_occurrence",
                    "relation": "of",
                    "second_subject": "result",
                },
            ],
            "yield_relation": {
                "first_subject": "result",
                "relation": "of",
                "second_subject": "Act_occurrence",
                "from": "Act_occurrence",
                "to": "result",
            },
            "evidence_carried_by_result_occurrence_relation": {
                "first_subject": {
                    "identity": "Evidence_of_Yield_relation",
                    "first_subject": "Evidence",
                    "relation": "of",
                    "second_subject": "Yield_relation",
                },
                "relation": "carried_by",
                "second_subject": {
                    "identity": "recording_occurrence_of_result",
                    "first_subject": "recording_occurrence",
                    "relation": "of",
                    "second_subject": "result",
                },
            },
            "input_references": [
                "pair_assertion_reference",
                "source_ingest_occurrence_identity",
            ],
            "result_coordinates": [
                "dimensions",
                "available_occurrence_count",
                "known_loss",
            ],
            "determination": "measurement_rule",
            "recurrent_subject": {
                "first_subject": "recurrence_Assertion",
                "relation": "carried_by",
                "second_subject": {
                    "first_subject": "Evidence",
                    "relation": "of",
                    "second_subject": "Yield_relation",
                },
            },
        },
        "input_subject": {
            "first_subject": "recurrence_Assertion",
            "relation": "carried_by",
            "second_subject": {
                "first_subject": "Evidence",
                "relation": "of",
                "second_subject": "Yield_relation",
            },
        },
        "input_material": "later_exact_Ingest_result",
        "findings": ["first_position", "second_position"],
        "order_and_position_difference_read_from": [
            "first_position",
            "second_position",
        ],
        "bounded_by": [
            "Locality",
            "completeness_boundary",
            "occurrence_limit",
        ],
        "standing_not_established": [
            "Candidate",
            "Admission",
            "Standing_movement",
            "represented_relation",
        ],
    }


    assert material["pair_assertion_reference"]
    assert material["source_ingest_occurrence_identity"]
    assert material["occurrence_limit"]
    assert all(
        set(assertion["dimensions"]["content"])
        == {"first_position", "second_position", "completeness_boundary"}
        for assertion in material["assertions"]
    )
    grammar_witness = declared["witness"]
    assert set(grammar_witness["input_references"]) <= set(material)
    result_coordinate_identities = {
        coordinate["identity"] if type(coordinate) is dict else coordinate
        for coordinate in grammar_witness["result_coordinates"]
    }
    assert result_coordinate_identities <= set(material)
    assert grammar_witness["determination"] in material
    evidence_occurrence = grammar_witness["event_occurrences"][0]
    evidence_occurrence_name = "_".join(
        (
            evidence_occurrence["first_subject"],
            evidence_occurrence["relation"],
            evidence_occurrence["second_subject"],
            evidence_occurrence["recording"],
        )
    ).lower()
    assert result_witness["act_evidence"].kind.endswith(evidence_occurrence_name)
    evidence_of_yield_relation = grammar_witness["event_occurrences"][1]
    evidence_of_yield_relation_name = "_".join(
        (
            evidence_of_yield_relation["first_subject"],
            evidence_of_yield_relation["relation"],
            evidence_of_yield_relation["second_subject"],
            evidence_of_yield_relation["recording"],
        )
    ).lower()
    assert result_witness["evidence_of_yield_relation"].kind.endswith(
        evidence_of_yield_relation_name
    )
    yield_relation = grammar_witness["yield_relation"]
    assert yield_relation == {
        "first_subject": "result",
        "relation": "of",
        "second_subject": "Act_occurrence",
        "from": "Act_occurrence",
        "to": "result",
    }
    recording_occurrence_of_result = grammar_witness["event_occurrences"][2]
    recording_occurrence_of_result_name = "_".join(
        (
            recording_occurrence_of_result["first_subject"],
            recording_occurrence_of_result["relation"],
            recording_occurrence_of_result["second_subject"],
        )
    ).lower()
    assert result_witness["event"].kind.endswith(recording_occurrence_of_result_name)
    assert grammar_witness["evidence_carried_by_result_occurrence_relation"] == {
        "first_subject": {
            "identity": "Evidence_of_Yield_relation",
            "first_subject": "Evidence",
            "relation": "of",
            "second_subject": "Yield_relation",
        },
        "relation": "carried_by",
        "second_subject": {
            "identity": "recording_occurrence_of_result",
            "first_subject": "recording_occurrence",
            "relation": "of",
            "second_subject": "result",
        },
    }
    assert material["evidence_of_yield_relation_identity"] == result_witness[
        "evidence_of_yield_relation"
    ].identity
    assert not {
        "candidate",
        "admission",
        "standing_movement",
        "represented_relation",
    } & set(material)


def test_byte_pair_occurrence_position_measurement_is_structured_in_grammar():
    declared = _clause("01.Source.D")["declared_measurements"][
        "measurement_of_position_coordinates_of_byte_pair_occurrences"
    ]
    bundle = _byte_pair_occurrence_position_yield_witness()
    material = bundle["event"].material
    act_material = bundle["act_evidence"].material

    assert declared["measurement"] == {
        "subject": {
            "first_subject": "position",
            "relation": "of",
            "second_subject": {
                "identity": "occurrences_of_byte_pair",
                "first_subject": "occurrences",
                "relation": "of",
                "second_subject": "byte_pair",
            },
        },
        "finding": "position",
    }
    assert declared["witness"]["input_reference"] in material
    assert material[declared["witness"]["input_reference"]] == (
        act_material["participation"]["subject_reference"]
    )
    assert declared["witness"]["input_relation"] == {
        "first_subject": "exact_Ingest_result",
        "relation": "input_to",
        "second_subject": "exact_Act",
    }
    assert material["assertions"]["dimensions"]["content"] == {
        "exact_pair": "material at first_position through second_position",
        "first_position": "position",
        "second_position": "position of the second byte occurrence",
        "first_position_coordinate_reference": (
            "exact source-byte position-coordinate reference"
        ),
        "second_position_coordinate_reference": (
            "exact source-byte position-coordinate reference"
        ),
    }
    assert material["assertions"]["occurrences"] == 2


def test_measurement_result_carriers_and_responsible_act_evidence_name_their_own_clauses():
    assert {
        BYTE_EVENT_KIND_RESPONSIBILITIES[
            BYTE_MEASUREMENT_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND
        ],
        BYTE_EVENT_KIND_RESPONSIBILITIES[BYTE_MEASUREMENT_RECORDED_KIND],
        BYTE_EVENT_KIND_RESPONSIBILITIES[BYTE_PAIR_MEASUREMENT_RECORDED_KIND],
        POSITION_EVENT_KIND_RESPONSIBILITIES[
            OCCURRENCE_POSITION_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND
        ],
        POSITION_EVENT_KIND_RESPONSIBILITIES[OCCURRENCE_POSITION_RECORDED_KIND],
        PAIR_OCCURRENCE_EVENT_KIND_RESPONSIBILITIES[
            RECORDED_RESPONSIBILITY_ASSIGNMENT_OF_MEASUREMENT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_KIND
        ],
        PAIR_OCCURRENCE_EVENT_KIND_RESPONSIBILITIES[
            RECORDING_OCCURRENCE_OF_RESULT_OF_MEASUREMENT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_KIND
        ],
    } == {"01.Source.D"}
    assert {
        BYTE_EVENT_KIND_RESPONSIBILITIES[
            BYTE_MEASUREMENT_RESPONSIBLE_ACT_EVIDENCE_KIND
        ],
        BYTE_EVENT_KIND_RESPONSIBILITIES[
            BYTE_PAIR_RESPONSIBLE_ACT_EVIDENCE_KIND
        ],
        POSITION_EVENT_KIND_RESPONSIBILITIES[
            OCCURRENCE_POSITION_ACT_EVIDENCE_KIND
        ],
        PAIR_OCCURRENCE_EVENT_KIND_RESPONSIBILITIES[
            RECORDED_EVIDENCE_OF_ACT_OCCURRENCE_OF_MEASUREMENT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_KIND
        ],
    } == {"02.Acts.A"}


def test_position_result_act_and_assertion_responsibilities_do_not_absorb_each_other():
    act_without_result = _occurrence_position_yield_witness()
    act_evidence_material = deepcopy(act_without_result["act_evidence"].material)
    assert {
        item["dimensions"]["responsibility"]
        for item in act_without_result["event"].material["assertions"]
    } == {POSITION_ASSERTION_RESPONSIBILITY}
    assert (
        act_without_result["event"].material["responsibility"]
        != POSITION_ASSERTION_RESPONSIBILITY
    )
    act_without_result["event"].material["assertions"][0]["dimensions"][
        "responsibility"
    ] = OCCURRENCE_POSITION_RESPONSIBILITY

    assert act_without_result["act_evidence"].material == act_evidence_material
    assert POSITION_EVENT_KIND_RESPONSIBILITIES[
        OCCURRENCE_POSITION_ACT_EVIDENCE_KIND
    ] == "02.Acts.A"
    assert _measurement_result_witness(act_without_result)["assertions"] == MISSING

    result_without_act = _occurrence_position_yield_witness()
    result_without_act["act_evidence"] = None
    assert set(_measurement_result_witness(result_without_act).values()) == {EXACT}
    assert POSITION_EVENT_KIND_RESPONSIBILITIES[
        OCCURRENCE_POSITION_RECORDED_KIND
    ] == "01.Source.D"


def test_measurement_result_and_exact_act_clauses_do_not_absorb_each_other():
    act_without_result = _byte_measurement_witness()
    act_without_result["event"].material["assertions"] = []

    assert set(_act_occurrence_witness(act_without_result).values()) == {EXACT}
    assert _measurement_result_witness(act_without_result) == {
        "responsibility": EXACT,
        "responsible_boundary": EXACT,
        "responsibility_assignment_evidence": EXACT,
        "measurement_rule": EXACT,
        "source_localities": EXACT,
        "completeness_boundary": EXACT,
        "assertions": MISSING,
    }

    result_without_act_evidence = _byte_measurement_witness()
    result_without_act_evidence["act_evidence"] = None

    assert set(
        _measurement_result_witness(result_without_act_evidence).values()
    ) == {EXACT}
    act_witness = _act_occurrence_witness(result_without_act_evidence)
    assert act_witness["exact_Act"] == MISSING
    assert act_witness["Act_occurrence"] == MISSING
    assert act_witness["Evidence_of_Act_occurrence"] == MISSING


def test_shared_position_measurement_decomposes_material_non_establishment():
    declared = _clause("01.Source.D")["declared_measurements"][
        "measurement_of_shared_position_of_byte_pair_occurrences"
    ]

    assert declared["standing_not_established"][0] == {
        "first_subject": "input_pair_occurrences",
        "relation": "establish",
        "second_subject": {
            "first_subject": "material",
            "relation": "of",
            "second_subject": "input_pair_occurrences",
        },
        "standing": "not_established",
    }


def test_ordered_relation_path_and_pair_findings_keep_each_responsibility_clause_distinct():
    declared = _clause("04.Compare.B")
    assert declared["subject"] == {
        "identity": "bounded_comparison_of_ordered_relation_path_with_recorded_pair_findings",
        "first_subject": "bounded_comparison",
        "relation": "of",
        "second_subject": {
            "first_subject": "ordered_relation_path",
            "relation": "with",
            "second_subject": "recorded_pair_findings",
        },
    }
    assert PATH_FINDING_COMPARISON_EVENT_KIND_RESPONSIBILITIES == {
        COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_RESPONSIBILITY_ASSIGNMENT_KIND: "04.Compare.B",
        COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_APPLICABILITY_ACT_EVIDENCE_KIND: "02.Acts.A",
        COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_APPLICABILITY_RESULT_KIND: "01.Standing.E.1",
        COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_COMPARE_ACT_EVIDENCE_KIND: "02.Acts.A",
        COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_RESULT_KIND: "04.Compare.B",
    }
    assert declared["standing_not_established"] == [
        "source_relation",
        "recurrence",
        "represented_relation",
        "composite_material",
    ]


def test_measurement_result_distinction_adversaries_collapse_one_boundary_each():
    mutations = {
        ("Measurement_result", "exact_Act_occurrence"): lambda bundle: bundle[
            "event"
        ].material.__setitem__(
            "result_identity",
            bundle["event"].material["act_occurrence_identity"],
        ),
        ("Measurement_occurrence", "recording_occurrence"): lambda bundle: (
            object.__setattr__(
                bundle["event"],
                "identity",
                bundle["event"].material["act_occurrence_identity"],
            )
        ),
        (
            "Measurement_Responsibility",
            "Assertion_Standing_coordinate_Responsibility",
        ): lambda bundle: [
            item["dimensions"].__setitem__(
                "responsibility", bundle["event"].material["responsibility"]
            )
            for item in bundle["event"].material["assertions"]
        ],
    }

    for collapsed, mutate in mutations.items():
        bundle = _byte_measurement_witness()
        mutate(bundle)
        distinctions = _measurement_result_distinctions(bundle)

        assert distinctions[collapsed] is False
        assert all(
            preserved
            for distinction, preserved in distinctions.items()
            if distinction != collapsed
        )


def test_measurement_result_adversaries_change_the_declared_coordinate_only():
    mutations = {
        "responsibility": lambda material: material.__setitem__(
            "responsibility", BYTE_PAIR_MEASUREMENT_RESPONSIBILITY
        ),
        "responsible_boundary": lambda material: material.__setitem__(
            "responsible_boundary", "a different boundary"
        ),
        "responsibility_assignment_evidence": lambda material: material[
            "responsibility_assignment_reference"
        ].__setitem__("assignment_identity", "a different assignment"),
        "measurement_rule": lambda material: material.__setitem__(
            "measurement_rule", BYTE_PAIR_MEASUREMENT_RULE
        ),
        "completeness_boundary": lambda material: material[
            "completeness_boundary"
        ].__setitem__("identity", "a different boundary"),
        "assertions": lambda material: material["assertions"][0][
            "assertion_subject"
        ].__setitem__("measurement_rule", BYTE_PAIR_MEASUREMENT_RULE),
    }

    for changed, mutate in mutations.items():
        bundle = _byte_measurement_witness()
        mutate(bundle["event"].material)
        witness = _measurement_result_witness(bundle)

        assert witness[changed] == MISSING
        assert all(
            standing == EXACT
            for coordinate, standing in witness.items()
            if coordinate != changed
        )


def test_act_and_occurrence_identities_do_not_establish_their_relation():
    bundle = _byte_measurement_witness()
    event = bundle["event"]
    assert event.material["addressed_act_identity"]
    assert event.material["act_occurrence_identity"]
    bundle["act_evidence"] = None
    witness = _act_occurrence_witness(bundle)

    assert witness["exact_Act"] == MISSING
    assert witness["Act_occurrence"] == MISSING
    assert witness["Evidence_of_Act_occurrence"] == MISSING


def test_responsibility_coordinates_do_not_establish_assignment_standing():
    bundle = _byte_measurement_witness()
    assignment_reference = dict(
        bundle["event"].material["responsibility_assignment_reference"]
    )
    assignment_reference["recorded_occurrence_identity"] = "same-shaped-missing"
    bundle["event"].material["responsibility_assignment_reference"] = (
        assignment_reference
    )
    bundle["act_evidence"].material["responsibility_assignment_reference"] = dict(
        assignment_reference
    )

    witness = _act_occurrence_witness(bundle)
    assert witness["Responsibility"] == EXACT
    assert witness["responsible_boundary"] == EXACT
    assert witness["Responsibility_assignment_Standing"] == MISSING


def test_occurrence_position_assignment_standing_refuses_a_corrupted_prior_carrier():
    ledger = _IntegrityAdversaryLedger()
    ingest_material(
        ledger,
        locality_identity="source",
        exact_bytes=b"ab",
        source_role="test source",
        source_boundary="test boundary",
    )
    prior_result = _record_byte_measurement(
        ledger,
        source_localities=("source",),
        recording_locality_identity="measurement",
    )
    second_assignment = record_byte_measurement_responsibility_assignment(
        ledger,
        source_localities=("source",),
        recording_locality_identity="measurement",
        locality_standing=read_operator_locality_standing(
            ledger, locality_identity="measurement"
        ),
    )
    record_byte_measurement_responsible_act_evidence(
        ledger,
        responsibility_assignment_event_identity=second_assignment.identity,
        responsibility_assignment_standing=read_operator_locality_standing(
            ledger, locality_identity="measurement"
        ),
    )
    finding = measure_occurrence_position(
        ledger, source_locality_identity="source"
    )
    assignment = record_occurrence_position_measurement_responsibility_assignment(
        ledger,
        recording_locality_identity="measurement",
        finding=finding,
        locality_standing=read_operator_locality_standing(
            ledger, locality_identity="measurement"
        ),
    )
    position_act = record_occurrence_position_measurement_responsible_act_evidence(
        ledger,
        responsibility_assignment_event_identity=assignment.identity,
        responsibility_assignment_standing=read_operator_locality_standing(
            ledger, locality_identity="measurement"
        ),
    )
    position_result = record_occurrence_position_measurement_result(
        ledger,
        responsible_act_evidence_event_identity=position_act.identity,
    )
    bundle = _yield_bundle(ledger, position_result)
    ledger.mark_corrupted(prior_result.identity)

    assert not _responsibility_assignment_standing_is_exact(bundle)
    assert _measurement_result_witness(bundle)[
        "responsibility_assignment_evidence"
    ] == MISSING


def test_runtime_authority_does_not_carry_evidence_scope_prose():
    contaminated = {}
    pattern = re.compile(
        r'"authority"\s*:\s*(?:"[^"\n]*(?:Evidence|evidence|evidences)|'
        r'\([^)]{0,400}(?:Evidence|evidence|evidences))',
        re.MULTILINE,
    )
    for path in sorted(RUNTIME.glob("*.py")):
        matches = [match.group(0) for match in pattern.finditer(path.read_text())]
        if matches:
            contaminated[path.name] = matches

    assert contaminated == {}


def test_each_dimensions_call_separates_authority_from_its_evidence_scope():
    """Every call through the shared dimensions bottleneck is checked."""

    dimensions_calls = []
    for path in sorted(RUNTIME.glob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if not (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Name)
                and node.func.id == "_dimensions"
            ):
                continue
            keywords = {item.arg: item.value for item in node.keywords}
            dimensions_calls.append((path.name, node.lineno))
            authority = keywords.get("authority")
            assert isinstance(authority, ast.Constant), (path, node.lineno)
            assert authority.value == "unestablished", (path, node.lineno)
            assert "evidence_scope" in keywords, (path, node.lineno)

    assert dimensions_calls


LOCALITY_BOUNDARY_BY_KIND = {
    "operator.representation.locality_evidenced": "representation_result",
    "operator.representation.emission_attempt_locality_evidenced": (
        "emission_attempt"
    ),
    "operator.representation.emission_locality_evidenced": (
        "successful_emission"
    ),
}
LOCALITY_BOUNDARIES_EVIDENCED_BY_OCCURRENCE = {
    "byte_measurement",
    "assertion_movement",
    "operator_material_acquisition",
}


def _declared_kind_constants(family: str) -> dict[str, list[str]]:
    """Every module-level kind constant naming this relation, found by read code.

    Discovery from the runtime, as with Yield: the registry above is not
    asked what exists, the runtime is. A boundary that stops declaring itself,
    or a new one that never registers, both surface here.
    """

    found: dict[str, list[str]] = {}
    for path in sorted(RUNTIME.glob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in tree.body:
            if not isinstance(node, ast.Assign):
                continue
            if not isinstance(node.value, ast.Constant):
                continue
            if not isinstance(node.value.value, str):
                continue
            for target in node.targets:
                if not isinstance(target, ast.Name):
                    continue
                if family not in target.id:
                    continue
                found.setdefault(node.value.value, []).append(path.name)
    return found


def test_every_locality_evidence_kind_is_declared_once_and_registered():
    """The Yield discovery pattern, applied to the second relation."""

    discovered = _declared_kind_constants("LOCALITY_EVIDENCE_KIND")

    duplicated = {
        kind: modules for kind, modules in discovered.items() if len(modules) > 1
    }
    assert not duplicated, (
        "\nOne locality kind, declared by more than one module. The writer and "
        "the reader then hold separate contracts that drift silently:\n"
        + "\n".join(f"  {kind} -- {', '.join(m)}" for kind, m in duplicated.items())
    )

    assert set(discovered) == set(LOCALITY_BOUNDARY_BY_KIND), (
        "\nLive locality boundaries and the registry disagree.\n"
        f"  only live:     {sorted(set(discovered) - set(LOCALITY_BOUNDARY_BY_KIND))}\n"
        f"  only registry: {sorted(set(LOCALITY_BOUNDARY_BY_KIND) - set(discovered))}"
    )
    registered = _relation_occurrence_fidelity_findings()
    assert {
        boundary for relation, boundary in registered if relation == "locality"
    } == (
        set(LOCALITY_BOUNDARY_BY_KIND.values())
        | LOCALITY_BOUNDARIES_EVIDENCED_BY_OCCURRENCE
    )


# Every module recording a `scope_locality` dimension. 06.Locality.A makes
# locality a coordinate in its own right, and 01.Standing.E.1 enumerates Scope
# and locality separately among the coordinates Applicability is determined
# for. This compound field carries both in one string. A regression boundary,
# not approval.
SCOPE_LOCALITY_COMPOUND_SITES = 21


def test_no_new_site_compounds_scope_with_locality():
    """The count of sites compounding Scope with locality may fall, never rise."""

    sites = sum(
        path.read_text(encoding="utf-8").count("scope_locality")
        for path in sorted(RUNTIME.glob("*.py"))
    )
    assert sites <= SCOPE_LOCALITY_COMPOUND_SITES, (
        f"\n{sites} sites compound Scope with locality, up from "
        f"{SCOPE_LOCALITY_COMPOUND_SITES}. 06.Locality.A carries locality as "
        "its own coordinate; a new site glues it to Scope again."
    )


# Every live relation witness, and where its Evidence comes from.
#
# A dedicated Evidence event species is not what establishes a relation: Evidence
# may be the event occurrence itself, a responsible Act evidence occurrence,
# or a dedicated one. witness_grammar.json requires exact_relation,
# occurrence_witness,
# and intact_evidence, and names no species for them.
RELATION_EVIDENCE = {
    "_locality_requirements": (
        "locality",
        "the responsible movement Evidence occurrence",
    ),
    "_assertion_locality_requirements": ("locality", "the event occurrence itself"),
    "_emission_locality_requirements": ("locality", "a locality-evidence occurrence"),
    "_emission_attempt_locality_requirements": (
        "locality",
        "an emission-attempt locality-evidence occurrence",
    ),
    "_representation_locality_requirements": (
        "locality",
        "a representation locality-evidence occurrence",
    ),
    "_emission_participation_requirements": (
        "participation",
        "the responsible emission Act evidence occurrence",
    ),
    "_participation_requirements": (
        "participation",
        "the responsible pair Act evidence occurrence",
    ),
    "_occurrence_result_requirements": ("yield", "a Yield-evidence occurrence"),
    "_evidence_carried_by_result_occurrence_requirements": (
        "carried_by",
        "the exact Evidence occurrence carried by the result recording occurrence",
    ),
}


def _requirement_witnesses() -> set[str]:
    """Every live relation reader present in this module."""

    return {
        name
        for name, value in globals().items()
        if name.startswith("_")
        and name.endswith("_requirements")
        and callable(value)
    }


def _relation_coordinates_from_live_witnesses() -> dict[str, dict[str, bool]]:
    byte_measurement = _byte_measurement_witness()
    emission = _emission_witness()
    representation = _representation_witness()
    applicability = _recorded_applicability()
    return {
        "_locality_requirements": _locality_requirements(applicability),
        "_assertion_locality_requirements": _assertion_locality_requirements(
            byte_measurement,
            occurrence_identity=byte_measurement["event"].identity,
        ),
        "_emission_locality_requirements": _emission_locality_requirements(emission),
        "_emission_attempt_locality_requirements": (
            _emission_attempt_locality_requirements(emission)
        ),
        "_representation_locality_requirements": (
            _representation_locality_requirements(representation)
        ),
        "_emission_participation_requirements": (
            _emission_participation_requirements(emission)
        ),
        "_participation_requirements": _participation_requirements(
            applicability,
            role=BYTE_PAIR_INPUT_ROLE,
        ),
        "_occurrence_result_requirements": _occurrence_result_requirements(
            byte_measurement
        ),
        "_evidence_carried_by_result_occurrence_requirements": (
            _evidence_carried_by_result_occurrence_requirements(
                byte_measurement
            )
        ),
    }


def test_every_live_relation_witness_names_its_relation_and_its_evidence():
    """Runtime discovery equated with the registry, for every relation."""

    assert _requirement_witnesses() == set(RELATION_EVIDENCE), (
        "\nLive relation witnesses and the registry disagree.\n"
        f"  only live:     {sorted(_requirement_witnesses() - set(RELATION_EVIDENCE))}\n"
        f"  only registry: {sorted(set(RELATION_EVIDENCE) - _requirement_witnesses())}"
    )

    relations = json.loads(GRAMMAR.read_text(encoding="utf-8"))["relations"]
    for witness, (relation, evidence) in RELATION_EVIDENCE.items():
        assert relation in relations, f"{witness} names {relation}, which is not a relation"
        assert evidence, witness


def test_each_relation_has_a_live_witness():
    """Each relation Witness Grammar declares has a live witness."""

    relations = json.loads(GRAMMAR.read_text(encoding="utf-8"))["relations"]
    witnessed = {relation for relation, _ in RELATION_EVIDENCE.values()}
    assert witnessed == set(relations)


def test_every_live_relation_witness_returns_its_relation_required_coordinates():
    """The vector each witness reports is the one its relation declares."""

    relations = json.loads(GRAMMAR.read_text(encoding="utf-8"))["relations"]
    reported = _relation_coordinates_from_live_witnesses()
    assert set(reported) == _requirement_witnesses() == set(RELATION_EVIDENCE)

    for witness, requirements in reported.items():
        relation, _ = RELATION_EVIDENCE[witness]
        required = set(relations[relation]["requires"])
        assert set(requirements) == required, (
            f"{witness} witnesses {relation}, which requires {sorted(required)}; "
            f"it reports {sorted(requirements)}"
        )
        assert all(requirements.values()), witness


FIDELITY_SUBJECTS = {
    "addressed_byte_occurrence_reference_determination": (
        test_addressed_byte_occurrence_reference_determination_keeps_exact_bounds,
    ),
    "assertion_standing_coordinates": (
        test_assertion_clause_is_checked_against_a_live_byte_assertion,
    ),
    "asserted_content_scope_locality_distinction": (
        test_asserted_content_identity_includes_scope_but_not_locality,
    ),
    "responsibility_assignment_standing_distinction": (
        test_responsibility_coordinates_do_not_establish_assignment_standing,
        test_occurrence_position_assignment_standing_refuses_a_corrupted_prior_carrier,
    ),
    "scope_locality_distinction": (test_no_new_site_compounds_scope_with_locality,),
    "exact_act_occurrence": (
        test_exact_act_clause_is_checked_against_live_byte_measurement,
    ),
    "exact_act_occurrence_relation": (
        test_act_and_occurrence_identities_do_not_establish_their_relation,
    ),
    "measurement_result_exact_act_clause_distinction": (
        test_measurement_result_and_exact_act_clauses_do_not_absorb_each_other,
    ),
    "measurement_result_act_evidence_clause_distinction": (
        test_measurement_result_carriers_and_responsible_act_evidence_name_their_own_clauses,
    ),
    "position_result_act_assertion_responsibility_distinction": (
        test_position_result_act_and_assertion_responsibilities_do_not_absorb_each_other,
    ),
    "evidence_of_yield_relation_boundary": (
        test_every_evidence_of_yield_relation_site_declares_its_occurrence_boundary,
    ),
    "yield_relation_required_coordinates": (
        test_byte_pair_yield_adversaries_change_one_requirement_each,
        test_remaining_yield_adversaries_change_one_requirement_each,
    ),
    "yield_subject_presence_relation_distinction": (
        test_occurrence_and_result_subjects_do_not_establish_their_relation,
    ),
    "yield_relation_result_identity": (
        test_yield_relation_read_has_no_result_reencoding_surface,
    ),
    "yield_relation_exact_evidence_result": (
        test_every_live_recorded_yield_result_is_bound_to_its_exact_evidence_result,
    ),
    "different_yield_result_identity": (
        test_different_yield_occurrences_do_not_share_result_identity,
    ),
    "declared_measurement_result": (
        test_measurement_result_clause_is_checked_against_live_byte_pair_and_position_results,
        test_standing_measurement_declarations_match_the_curated_runtime_order,
        test_each_declared_measurement_names_its_finding_and_responsible_occurrence,
        test_shared_position_measurement_decomposes_material_non_establishment,
        test_byte_pair_occurrence_position_measurement_is_structured_in_grammar,
    ),
    "it_result_reference": (
        test_measurement_result_pronoun_is_an_exact_machine_reference,
    ),
    "recurrent_byte_pair_occurrence_position_measurement": (
        test_pair_occurrence_measurement_is_structured_in_the_grammar_representation,
    ),
    "measurement_result_distinctions": (
        test_measurement_result_distinction_adversaries_collapse_one_boundary_each,
    ),
    "measurement_result_coordinates": (
        test_measurement_result_adversaries_change_the_declared_coordinate_only,
    ),
    "byte_measurement_relation": (
        test_byte_measurement_adversaries_change_one_requirement_each,
    ),
    "relation_occurrence_boundary": (
        test_primary_relation_measurements_preserve_their_occurrence_boundaries,
    ),
    "relation_required_coordinates": (
        test_changed_relation_anatomy_is_detected,
        test_explicit_but_wrong_relation_cannot_satisfy_a_structured_grammar_address,
        test_ordered_relation_path_and_pair_findings_keep_each_responsibility_clause_distinct,
    ),
    "relation_witness_evidence": (
        test_every_live_relation_witness_names_its_relation_and_its_evidence,
    ),
    "relation_occurrence_witness": (test_each_relation_has_a_live_witness,),
    "relation_witness_required_coordinates": (
        test_every_live_relation_witness_returns_its_relation_required_coordinates,
    ),
    "representation_yield_participation_distinction": (
        test_representation_act_has_an_exact_yield_relation_without_asserting_participation,
    ),
    "emission_relation_instantiation": (
        test_emission_instantiates_each_relation_it_carries_at_its_boundary,
    ),
    "successful_emission_relation": (
        test_successful_emission_adversaries_change_one_requirement_each,
    ),
    "representation_result_relation": (
        test_representation_result_adversaries_change_one_requirement_each,
    ),
    "applicability_determination": (
        test_applicability_clause_is_checked_against_a_live_pair_determination,
        test_emission_applicability_witnesses_every_declared_coordinate,
    ),
    "input_role_participation_distinction": (
        test_input_is_an_open_act_local_role_before_participation,
    ),
    "candidate_participation_distinction": (
        test_subject_candidate_and_participation_relation_are_distinguished_in_both_directions,
    ),
    "candidate_role_distinction": (
        test_role_distinctions_refuse_direction_collapse_and_identity_promotion,
    ),
    "candidate_source_coordinates": (
        test_candidate_clause_preserves_coordinates_without_promoting_the_subject,
    ),
    "cross_boundary_participation_scope_limits": (
        test_cross_boundary_participation_preserves_scope_and_limits,
    ),
    "participation_source_boundary_distinction": (
        test_live_participation_is_not_source_b_by_relation_identity,
    ),
    "candidate_coordinate_order": (
        test_candidate_coordinate_order_is_the_exact_book_order,
    ),
    "participation_relation_coordinates": (
        test_participation_relation_coordinates_match_the_role_distinction,
        test_participation_requires_exact_subject_role_and_act_occurrence,
    ),
    "input_act_relation_occurrence": (
        test_unjoined_subjects_do_not_witness_an_input_to_act_relation,
    ),
    "one_exact_movement_assertion": (
        test_assertion_movement_result_names_and_witnesses_its_witness_clause,
    ),
    "assertion_locality_movement_standing_coordinates": (
        test_assertion_movement_standing_carries_the_exact_grammar_coordinates,
    ),
    "movement_coordinate_distinction": (
        test_assertion_movement_coordinates_refuse_crossing_or_loss,
    ),
    "standing_boundary_reference_responsibility_clause_coordinates": (
        test_standing_boundary_reference_stages_keep_distinct_clause_coordinates,
    ),
    "locality_relation_coordinates": (
        test_locality_relation_clause_is_checked_against_the_live_pair_witness,
    ),
    "locality_relation_distinctions": (
        test_locality_fans_out_orthogonal_adversaries_for_each_live_witness,
    ),
    "locality_subject_presence_relation_distinction": (
        test_content_and_locality_subjects_do_not_establish_locality_relation,
    ),
    "emission_attempt_locality_relation": (
        test_emission_attempt_locality_adversaries_change_one_requirement_each,
    ),
    "emission_locality_distinction": (
        test_attempt_and_success_have_distinct_locality_relations_for_exact_material,
    ),
    "successful_emission_locality_relation": (
        test_successful_emission_locality_binds_the_exact_representation,
    ),
    "locality_relation_occurrence_evidence": (
        test_every_locality_evidence_kind_is_declared_once_and_registered,
    ),
    "standing_locality_continuation_responsibility_clause_coordinates": (
        test_standing_locality_continuation_stages_keep_distinct_clause_coordinates,
    ),
    "recorded_boundary_locality_responsibility_clause_coordinates": (
        test_recorded_boundary_locality_stages_keep_distinct_clause_coordinates,
    ),
    "Responsibility_assignment_of_operator_invocation_Locality_relation": (
        test_operator_system_locality_stages_keep_distinct_witness_clauses,
    ),
    "operator_material_acquisition_responsibility_clause_coordinates": (
        test_operator_material_acquire_stages_keep_distinct_clause_coordinates,
    ),
    "authority_evidence_scope_distinction": (
        test_runtime_authority_does_not_carry_evidence_scope_prose,
        test_each_dimensions_call_separates_authority_from_its_evidence_scope,
    ),
    "representation_source_coordinates": (
        test_representation_source_clause_is_checked_against_one_live_result,
        test_exact_source_material_rule_is_checked_against_one_live_representation,
        test_representation_source_coordinate_adversaries_preserve_exact_dependencies,
    ),
    "emission_candidate_Admission_to_operator_Locality": (
        test_exact_material_admission_establishes_one_rule_relation,
    ),
    "representation_source_standing_boundary_distinction": (
        test_representation_source_and_standing_boundary_remain_distinct_coordinates,
    ),
    "representation_result_act_locality_clause_distinction": (
        test_representation_result_act_and_locality_species_keep_their_clauses,
        test_candidate_and_admission_species_keep_their_distinct_clauses,
        test_emission_applicability_species_keep_act_and_result_clauses_distinct,
    ),
    "representation_source_act_locality_distinction": (
        test_representation_source_act_and_locality_witnesses_do_not_absorb_each_other,
        test_representation_source_distinction_adversaries_collapse_one_boundary_each,
    ),
    "composite_material_order": (
        test_every_grammar_representation_composite_preserves_material_order,
    ),
    "content_locality_occurrence_distinction": (
        test_witness_discriminates_content_locality_and_occurrence,
    ),
    "relation_fidelity_findings": (test_every_relation_has_exact_fidelity_findings,),
    "relation_occurrence_fidelity_findings": (
        test_every_registered_relation_occurrence_obeys_the_full_fidelity_matrix,
    ),
    "bounded_fidelity_comparison": (
        test_fidelity_is_bounded_witness_grammar_comparison_for_this_seed,
        test_fidelity_refuses_collapsed_subjects_tests_as_subject_and_inverted_order,
        test_each_fidelity_test_subject_names_one_exact_witness_grammar_coordinate,
    ),
}
