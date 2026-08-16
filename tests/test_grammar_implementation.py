from copy import deepcopy
import ast
import json
import re
from tests.binary_input import binary_input
from io import BytesIO, StringIO
from pathlib import Path

from seed_runtime.byte_measurement import (
    BYTE_PAIR_INPUT_ROLE,
    _identity,
    _validate_moved_byte_assertion,
    assertions_of_recorded_byte_measurement,
    get_recorded_pair_input_applicability,
    record_byte_position_pair_count_layer,
    record_byte_count_layer,
)
from seed_runtime.events import CORRUPTED, EventLedger
from seed_runtime.identities import new_identity
from seed_runtime.material_ingest import ingest_material
from seed_runtime.operator_console import run_persistent_operator_console
from seed_runtime.operator_command import AddressedOperatorCommand, OperatorCommandFrame
from seed_runtime.operator_checkpoint import (
    ADDRESSED_REPRESENTATION_LOCALITY_EVIDENCE_KIND,
    open_operator_checkpoint,
)
from tests.material_fixture_console import run_material_fixture_console
from seed_runtime.operator_representation import (
    REPRESENTATION_EMISSION_INPUT_ROLE,
    emit_operator_representation,
    record_operator_representation,
)
from seed_runtime.occurrence_position_measurement import (
    measure_occurrence_position,
    record_occurrence_position_measurement,
)
from seed_runtime.yield_evidence import YIELD_LIVE_BOUNDARIES
from seed_runtime.yield_evidence import read_yield_relation_requirements


GRAMMAR = Path(__file__).resolve().parents[1] / "book_of_seed/grammar.json"
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
    return json.loads(GRAMMAR.read_text(encoding="utf-8"))["clauses"][clause_identity]


def _witness_grammar() -> dict:
    return json.loads(GRAMMAR.read_text(encoding="utf-8"))["implementation_witness"]


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
    measurement = record_byte_count_layer(
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
        "content_evidence": ledger.get(measurement.material["yield_evidence_identity"]),
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
    byte_measurement = record_byte_count_layer(
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
        "content_evidence": ledger.get(event.material["yield_evidence_identity"]),
        "movement": movement,
        "movement_act_evidence": ledger.get(
            movement.material["responsible_act_evidence_identity"]
        ),
        "movement_content_evidence": ledger.get(
            movement.material["yield_evidence_identity"]
        ),
        "pair_event": pair_measurement,
        "pair_act_evidence": ledger.get(
            pair_measurement.material["responsible_act_evidence_identity"]
        ),
        "pair_content_evidence": ledger.get(
            pair_measurement.material["yield_evidence_identity"]
        ),
    }


def _assertion_locality_movement_yield_witness() -> dict:
    source = _recorded_applicability()
    return {
        "ledger": source["ledger"],
        "event": source["movement"],
        "act_evidence": source["movement_act_evidence"],
        "content_evidence": source["movement_content_evidence"],
        "recorded_result_occurrence_coordinate": "movement_act_occurrence_identity",
        "act_evidence_occurrence_coordinate": "movement_act_occurrence_identity",
    }


def _emission_witness() -> dict:
    ledger = _IntegrityAdversaryLedger()
    representation = record_operator_representation(
        ledger,
        locality_identity="emission",
        locality_standing={"as_of_event_identity": None},
    )
    emit_operator_representation(
        ledger,
        representation=representation,
        output_stream=StringIO(),
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
        "content_evidence": ledger.get(event.material["yield_evidence_identity"]),
    }


def _failed_emission_yield_witness() -> dict:
    class PartialOutput(StringIO):
        def write(self, value):
            super().write(value[:-1])
            return len(value) - 1

    ledger = _IntegrityAdversaryLedger()
    representation = record_operator_representation(
        ledger,
        locality_identity="failed-emission",
        locality_standing={"as_of_event_identity": None},
    )
    try:
        emit_operator_representation(
            ledger,
            representation=representation,
            output_stream=PartialOutput(),
        )
    except ValueError:
        pass
    event = ledger.get(representation["emission_failure_event_identity"])
    return _yield_bundle(ledger, event)


def _repeated_emission_attempt_witness() -> tuple[dict, dict]:
    ledger = _IntegrityAdversaryLedger()
    representation = record_operator_representation(
        ledger,
        locality_identity="repeated-emission-attempt",
        locality_standing={"as_of_event_identity": None},
    )
    emit_operator_representation(
        ledger,
        representation=representation,
        output_stream=StringIO(),
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
    first_yield_evidence = ledger.get(first_event.material["yield_evidence_identity"])
    emit_operator_representation(
        ledger,
        representation=representation,
        output_stream=StringIO(),
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
    second_yield_evidence = ledger.get(second_event.material["yield_evidence_identity"])
    return (
        {
            "ledger": ledger,
            "attempt": first_attempt,
            "attempt_locality_evidence": first_evidence,
            "event": first_event,
            "act_evidence": first_act_evidence,
            "locality_evidence": first_locality_evidence,
            "content_evidence": first_yield_evidence,
        },
        {
            "ledger": ledger,
            "attempt": second_attempt,
            "attempt_locality_evidence": second_evidence,
            "event": second_event,
            "act_evidence": second_act_evidence,
            "locality_evidence": second_locality_evidence,
            "content_evidence": second_yield_evidence,
        },
    )


def _representation_witness() -> dict:
    ledger = _IntegrityAdversaryLedger()
    representation = record_operator_representation(
        ledger,
        locality_identity="representation",
        locality_standing={"as_of_event_identity": None},
    )
    event = ledger.get(representation["representation_event_identity"])
    return {
        "ledger": ledger,
        "event": event,
        "act_evidence": ledger.get(event.material["responsible_act_evidence_identity"]),
        "locality_evidence": ledger.get(event.material["locality_evidence_identity"]),
        "content_evidence": ledger.get(event.material["yield_evidence_identity"]),
    }


def _repeated_representation_witness() -> tuple[dict, dict]:
    ledger = _IntegrityAdversaryLedger()

    def record() -> dict:
        representation = record_operator_representation(
            ledger,
            locality_identity="repeated-representation",
            locality_standing={"as_of_event_identity": None},
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
            "content_evidence": ledger.get(event.material["yield_evidence_identity"]),
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
    event = record_occurrence_position_measurement(
        ledger,
        recording_locality_identity="measurement",
        finding=finding,
    )
    return _yield_bundle(ledger, event)


def _checkpoint_locality_witnesses() -> tuple[dict, dict]:
    ledger = _IntegrityAdversaryLedger()

    def record(locality_identity: str) -> dict:
        representation = record_operator_representation(
            ledger,
            locality_identity=locality_identity,
            locality_standing={"as_of_event_identity": None},
        )
        addressed = AddressedOperatorCommand(
            command_identity=new_identity("operator_command"),
            locality_identity=locality_identity,
            addressed_at_representation_event_identity=representation[
                "representation_event_identity"
            ],
            frame=OperatorCommandFrame(
                exact_bytes=b"/checkpoint material\n",
                name=b"checkpoint",
                arguments=b"material",
            ),
        )
        checkpoint_result = open_operator_checkpoint(ledger, addressed)
        evidence = ledger.get(checkpoint_result.locality_evidence_event_identity)
        checkpoint = ledger.get(
            addressed.addressed_at_representation_event_identity
        )
        return {
            "ledger": ledger,
            "event": evidence,
            "addressed": addressed,
            "checkpoint": checkpoint,
        }

    return record("checkpoint-witness-one"), record("checkpoint-witness-two")


def _checkpoint_locality_requirements(bundle: dict) -> dict[str, bool]:
    event = bundle["event"]
    addressed = bundle["addressed"]
    checkpoint = bundle["checkpoint"]
    if addressed is None or checkpoint is None:
        return {
            "exact_relation": False,
            "occurrence_witness": False,
            "intact_evidence": False,
        }
    exact_relation = (
        event.material.get("first_subject") == addressed.command_identity
        and event.material.get("second_subject") == checkpoint.identity
    )
    occurrence_witness = (
        addressed.addressed_at_representation_event_identity == checkpoint.identity
        and checkpoint.kind == "operator.representation.recorded"
        and addressed.locality_identity == checkpoint.locality_identity
        and event.locality_identity != checkpoint.locality_identity
    )
    return {
        "exact_relation": exact_relation,
        "occurrence_witness": occurrence_witness,
        "intact_evidence": all(
            bundle["ledger"].integrity_of(item.identity) != CORRUPTED
            for item in (event, checkpoint)
        ),
    }


def _checkpoint_locality_cases() -> dict[str, str]:
    exact, alternate = _checkpoint_locality_witnesses()
    missing = dict(exact)
    missing["event"] = deepcopy(exact["event"])
    missing["event"].material["second_subject"] = "missing-checkpoint"
    wrong_occurrence = dict(exact)
    wrong_occurrence["checkpoint"] = alternate["checkpoint"]
    corrupted, _ = _checkpoint_locality_witnesses()
    corrupted["ledger"].mark_corrupted(corrupted["event"].identity)
    unrelated = dict(exact)
    unrelated["addressed"] = AddressedOperatorCommand(
        command_identity=exact["addressed"].command_identity,
        locality_identity=exact["addressed"].locality_identity,
        addressed_at_representation_event_identity=(
            exact["addressed"].addressed_at_representation_event_identity
        ),
        frame=OperatorCommandFrame(
            exact_bytes=b"/checkpoint other\n",
            name=b"checkpoint",
            arguments=b"other",
        ),
    )

    def witness(bundle: dict) -> str:
        return EXACT if all(_checkpoint_locality_requirements(bundle).values()) else MISSING

    return {
        "exact": witness(exact),
        "relation_missing": witness(missing),
        "wrong_occurrence": witness(wrong_occurrence),
        "corrupted_evidence": witness(corrupted),
        "unrelated_occurrence": witness(unrelated),
    }


def _yield_bundle(ledger, event) -> dict:
    act_evidence_identity = event.material.get("responsible_act_evidence_identity")
    locality_evidence_identity = event.material.get("locality_evidence_identity")
    return {
        "ledger": ledger,
        "event": event,
        "act_evidence": (
            ledger.get(act_evidence_identity) if isinstance(act_evidence_identity, str) else None
        ),
        "content_evidence": ledger.get(event.material["yield_evidence_identity"]),
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


def _assertion_witness(bundle: dict) -> dict[str, str]:
    assertion = bundle["source_assertion"]
    event = bundle["event"]
    content_evidence = bundle["content_evidence"]
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
        and content_evidence is not None
        and event.material.get("yield_evidence_identity") == content_evidence.identity
        and "assertions" in content_evidence.material.get("yield_coordinates", [])
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
        "Unknowns": EXACT if material.get("unknowns") else MISSING,
        "Standing": EXACT if dimensions.get("standing") else MISSING,
    }


def _applicability_witness(bundle: dict) -> dict[str, str]:
    applicability = bundle["applicability"]
    event = bundle["event"]
    act_evidence = bundle["act_evidence"]
    content_evidence = bundle["content_evidence"]
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
        and event.material.get("downstream_act_identity")
        == applicability.get("downstream_act_identity")
        == act_evidence.material.get("downstream_act_identity")
    )
    occurrence_relation = (
        act_evidence is not None
        and event.material.get("applicability_act_occurrence_identity")
        == applicability.get("applicability_act_occurrence_identity")
        == act_evidence.material.get("applicability_act_occurrence_identity")
    )
    carried_result = (
        content_evidence is not None
        and event.material.get("yield_evidence_identity") == content_evidence.identity
        and event.material["dimensions"].get("standing")
        == applicability["dimensions"].get("standing")
    )
    return {
        "input_identity": EXACT if input_relation else MISSING,
        "exact_Act": EXACT if act_relation else MISSING,
        "subject": EXACT if content.get("downstream_act") else MISSING,
        "result_boundary": EXACT if applicability.get("result_boundary") else MISSING,
        "Scope": EXACT if applicability.get("scope_locality") else MISSING,
        "locality": EXACT if applicability.get("measurement_locality") else MISSING,
        "Authority": EXACT if applicability["dimensions"].get("authority") else MISSING,
        # The relation endpoints already identify the exact input role and the
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
        "currentness": (
            INAPPLICABLE
            if treatment.get("currentness", {}).get("treatment")
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
        "Unknowns": EXACT if applicability.get("unknowns") else MISSING,
        "negative_Authority": (
            EXACT if treatment.get("negative_authority") else MISSING
        ),
    }


def _occurrence_result_witness(bundle: dict) -> str:
    requirements = _occurrence_result_requirements(bundle)
    return EXACT if all(requirements.values()) else MISSING


def _occurrence_result_requirements(bundle: dict) -> dict[str, bool]:
    ledger = bundle["ledger"]
    result_evidence = bundle["content_evidence"]
    responsible_act_evidence = bundle.get("act_evidence")

    def record_if_supplied_representation_changed(event):
        if event is None:
            return None
        stored = ledger.get(event.identity)
        if stored == event:
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
        result_evidence is not None
        and responsible_act_evidence is not None
        and responsible_act_evidence_identity is not None
        and responsible_act_evidence_identity != responsible_act_evidence.identity
        and result_evidence.material.get("responsible_act_evidence_identity")
        == responsible_act_evidence.identity
    ):
        result_evidence = deepcopy(result_evidence)
        result_evidence.material["responsible_act_evidence_identity"] = (
            responsible_act_evidence_identity
        )
    result_evidence_identity = record_if_supplied_representation_changed(result_evidence)

    event = deepcopy(bundle["event"])
    if (
        result_evidence is not None
        and result_evidence_identity != result_evidence.identity
        and event.material.get("yield_evidence_identity") == result_evidence.identity
    ):
        event.material["yield_evidence_identity"] = result_evidence_identity
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

    return read_yield_relation_requirements(
        ledger,
        recorded_result_event_identity=event_identity,
        result_evidence_event_identity=result_evidence_identity,
        responsible_act_evidence_event_identity=responsible_act_evidence_identity,
        recorded_result_occurrence_coordinate=bundle.get(
            "recorded_result_occurrence_coordinate", "act_occurrence_identity"
        ),
        responsible_act_occurrence_coordinate=bundle.get(
            "act_evidence_occurrence_coordinate", "act_occurrence_identity"
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
        and event.material.get("emitted_representation")
        == evidence.material.get("carried_content")
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
        attempt.material.get("representation")
        == evidence.material.get("carried_content")
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


def _relation_fidelity_cases() -> dict[str, dict[str, str]]:
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
    unrelated_event.material["yield_evidence_identity"] = "other-yield-evidence"
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
    unrelated_participation_event.material["yield_evidence_identity"] = (
        "other-yield-evidence"
    )
    unrelated_participation["pair_event"] = unrelated_participation_event

    exact_yield = _byte_measurement_witness()
    alternate_yield = _byte_measurement_witness()
    corrupted_yield = _byte_measurement_witness()
    corrupted_yield["ledger"].mark_corrupted(
        corrupted_yield["content_evidence"].identity
    )
    missing_yield = dict(exact_yield)
    missing_yield_event = deepcopy(exact_yield["event"])
    missing_yield_event.material["yield_evidence_identity"] = (
        "missing-yield-evidence"
    )
    missing_yield["event"] = missing_yield_event
    wrong_yield = dict(exact_yield)
    wrong_yield_act_evidence = deepcopy(exact_yield["act_evidence"])
    wrong_yield_content_evidence = deepcopy(exact_yield["content_evidence"])
    alternate_yield_occurrence = alternate_yield["event"].material[
        "act_occurrence_identity"
    ]
    wrong_yield_act_evidence.material["act_occurrence_identity"] = (
        alternate_yield_occurrence
    )
    wrong_yield_content_evidence.material["dimensions"]["act_occurrence_identity"] = (
        alternate_yield_occurrence
    )
    wrong_yield["act_evidence"] = wrong_yield_act_evidence
    wrong_yield["content_evidence"] = wrong_yield_content_evidence
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
            "wrong_occurrence": _assertion_locality_witness(
                locality,
                occurrence_identity=alternate_locality["event"].identity,
            ),
            "corrupted_evidence": _assertion_locality_witness(
                corrupted_locality,
                occurrence_identity=corrupted_locality["event"].identity,
            ),
            "unrelated_occurrence": _assertion_locality_witness(
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
            "wrong_occurrence": _participation_witness(
                wrong_participation, role=BYTE_PAIR_INPUT_ROLE
            ),
            "corrupted_evidence": _participation_witness(
                corrupted_participation, role=BYTE_PAIR_INPUT_ROLE
            ),
            "unrelated_occurrence": _participation_witness(
                unrelated_participation, role=BYTE_PAIR_INPUT_ROLE
            ),
        },
        "yield": {
            "exact": _occurrence_result_witness(exact_yield),
            "relation_missing": _occurrence_result_witness(missing_yield),
            "wrong_occurrence": _occurrence_result_witness(wrong_yield),
            "corrupted_evidence": _occurrence_result_witness(corrupted_yield),
            "unrelated_occurrence": _occurrence_result_witness(unrelated_yield),
        },
    }


def _successful_emission_requirement_bundles() -> dict[str, dict[str, dict]]:
    emission, alternate = _repeated_emission_attempt_witness()

    missing_locality = dict(emission)
    missing_locality_evidence = deepcopy(emission["locality_evidence"])
    missing_locality_evidence.material["carried_content"] = "different content"
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
    unrelated_locality_event.material["yield_evidence_identity"] = "other-yield-evidence"
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
    missing_yield_event.material["yield_evidence_identity"] = (
        "missing-yield-evidence"
    )
    missing_yield["event"] = missing_yield_event
    wrong_yield = dict(emission)
    wrong_yield_event = deepcopy(emission["event"])
    wrong_yield_event.material["responsible_act_evidence_identity"] = alternate[
        "act_evidence"
    ].identity
    wrong_yield_event.material["yield_evidence_identity"] = alternate[
        "content_evidence"
    ].identity
    wrong_yield_event.material["result_identity"] = alternate[
        "event"
    ].material["result_identity"]
    wrong_yield["event"] = wrong_yield_event
    wrong_yield["act_evidence"] = alternate["act_evidence"]
    wrong_yield["content_evidence"] = alternate["content_evidence"]
    unrelated_yield = dict(emission)
    unrelated_yield_event = deepcopy(emission["event"])
    unrelated_yield_event.material["input_role"] = "other-role"
    unrelated_yield["event"] = unrelated_yield_event
    corrupted_yield = _emission_witness()
    corrupted_yield["ledger"].mark_corrupted(
        corrupted_yield["content_evidence"].identity
    )
    return {
        "locality": {
            "exact": emission,
            "relation_missing": missing_locality,
            "wrong_occurrence": wrong_locality,
            "corrupted_evidence": corrupted_locality,
            "unrelated_occurrence": unrelated_locality,
        },
        "participation": {
            "exact": emission,
            "relation_missing": missing_participation,
            "wrong_occurrence": wrong_participation,
            "corrupted_evidence": corrupted_participation,
            "unrelated_occurrence": unrelated_participation,
        },
        "yield": {
            "exact": emission,
            "relation_missing": missing_yield,
            "wrong_occurrence": wrong_yield,
            "corrupted_evidence": corrupted_yield,
            "unrelated_occurrence": unrelated_yield,
        },
    }


def _emission_relation_fidelity_cases() -> dict[str, dict[str, str]]:
    bundles = _successful_emission_requirement_bundles()
    witnesses = {
        "locality": _emission_locality_witness,
        "participation": _emission_participation_witness,
        "yield": _occurrence_result_witness,
    }
    return {
        relation: {case: witnesses[relation](bundle) for case, bundle in cases.items()}
        for relation, cases in bundles.items()
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
    missing_event.material["yield_evidence_identity"] = "missing-yield-evidence"
    missing["event"] = missing_event

    wrong_occurrence = dict(exact)
    wrong_act_evidence = (
        deepcopy(exact["act_evidence"])
        if exact.get("act_evidence") is not None
        else None
    )
    wrong_content_evidence = deepcopy(exact["content_evidence"])
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
    wrong_content_evidence.material["dimensions"]["act_occurrence_identity"] = (
        alternate_occurrence
    )
    if wrong_act_evidence is not None:
        wrong_occurrence["act_evidence"] = wrong_act_evidence
    wrong_occurrence["content_evidence"] = wrong_content_evidence

    unrelated = dict(exact)
    unrelated_event = deepcopy(exact["event"])
    object.__setattr__(unrelated_event, "identity", unrelated_value)
    unrelated["event"] = unrelated_event

    corrupted["ledger"].mark_corrupted(corrupted["content_evidence"].identity)
    return {
        "exact": exact,
        "relation_missing": missing,
        "wrong_occurrence": wrong_occurrence,
        "corrupted_evidence": corrupted,
        "unrelated_occurrence": unrelated,
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
        "content_evidence": applicability["pair_content_evidence"],
    }
    alternate_pair = {
        "ledger": alternate_applicability["ledger"],
        "event": alternate_applicability["pair_event"],
        "act_evidence": alternate_applicability["pair_act_evidence"],
        "content_evidence": alternate_applicability["pair_content_evidence"],
    }
    corrupted_pair_source = _recorded_applicability()
    corrupted_pair = {
        "ledger": corrupted_pair_source["ledger"],
        "event": corrupted_pair_source["pair_event"],
        "act_evidence": corrupted_pair_source["pair_act_evidence"],
        "content_evidence": corrupted_pair_source["pair_content_evidence"],
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
        "assertion_locality_movement": _assertion_locality_movement_yield_witness,
        "occurrence_position_measurement": _occurrence_position_yield_witness,
        "failed_emission": _failed_emission_yield_witness,
        "material_ingest": _material_ingest_yield_witness,
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


def _additional_live_relation_fidelity_cases() -> dict[
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
    unrelated_representation_event.material["yield_evidence_identity"] = "other-yield"
    unrelated_representation_locality["event"] = unrelated_representation_event

    missing_representation_yield = dict(representation)
    missing_representation_yield_event = deepcopy(representation["event"])
    missing_representation_yield_event.material["yield_evidence_identity"] = (
        "missing-yield-evidence"
    )
    missing_representation_yield["event"] = missing_representation_yield_event
    wrong_representation_yield = dict(representation)
    wrong_representation_act_evidence = deepcopy(representation["act_evidence"])
    wrong_representation_content_evidence = deepcopy(representation[
        "content_evidence"
    ])
    alternate_occurrence = alternate_representation["event"].material[
        "act_occurrence_identity"
    ]
    wrong_representation_act_evidence.material["act_occurrence_identity"] = (
        alternate_occurrence
    )
    wrong_representation_content_evidence.material["dimensions"][
        "act_occurrence_identity"
    ] = alternate_occurrence
    wrong_representation_yield["act_evidence"] = wrong_representation_act_evidence
    wrong_representation_yield[
        "content_evidence"
    ] = wrong_representation_content_evidence
    corrupted_representation_yield = _representation_witness()
    corrupted_representation_yield["ledger"].mark_corrupted(
        corrupted_representation_yield["content_evidence"].identity
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
    unrelated_attempt_event.material["yield_evidence_identity"] = "unrelated-yield"
    unrelated_attempt["attempt"] = unrelated_attempt_event

    return {
        ("locality", "representation_result"): {
            "exact": _representation_locality_witness(representation),
            "relation_missing": _representation_locality_witness(
                missing_representation_locality
            ),
            "wrong_occurrence": _representation_locality_witness(
                wrong_representation_locality
            ),
            "corrupted_evidence": _representation_locality_witness(
                corrupted_representation_locality
            ),
            "unrelated_occurrence": _representation_locality_witness(
                unrelated_representation_locality
            ),
        },
        ("yield", "representation_result"): {
            "exact": _occurrence_result_witness(representation),
            "relation_missing": _occurrence_result_witness(
                missing_representation_yield
            ),
            "wrong_occurrence": _occurrence_result_witness(
                wrong_representation_yield
            ),
            "corrupted_evidence": _occurrence_result_witness(
                corrupted_representation_yield
            ),
            "unrelated_occurrence": _occurrence_result_witness(
                unrelated_representation_yield
            ),
        },
        ("locality", "emission_attempt"): {
            "exact": _emission_attempt_locality_witness(attempt),
            "relation_missing": _emission_attempt_locality_witness(missing_attempt),
            "wrong_occurrence": _emission_attempt_locality_witness(wrong_attempt),
            "corrupted_evidence": _emission_attempt_locality_witness(
                corrupted_attempt
            ),
            "unrelated_occurrence": _emission_attempt_locality_witness(
                unrelated_attempt
            ),
        },
    }


def _live_relation_fidelity_cases() -> dict[
    tuple[str, str], dict[str, str]
]:
    primary_boundaries = {
        "locality": "byte_measurement",
        "participation": "byte_pair_measurement",
        "yield": "byte_measurement",
    }
    registered = {
        (relation, primary_boundaries[relation]): cases
        for relation, cases in _relation_fidelity_cases().items()
    }
    registered.update(
        {
            (relation, "successful_emission"): cases
            for relation, cases in _emission_relation_fidelity_cases().items()
        }
    )
    registered.update(_additional_live_relation_fidelity_cases())
    registered[("locality", "assertion_movement")] = _locality_fidelity_cases()
    registered[("locality", "operator_checkpoint")] = (
        _checkpoint_locality_cases()
    )
    registered.update(
        {
            ("yield", boundary): {
                case: _occurrence_result_witness(bundle)
                for case, bundle in cases.items()
            }
            for boundary, cases in _byte_pair_yield_requirement_bundles().items()
        }
    )
    registered.update(
        {
            ("yield", boundary): {
                case: _occurrence_result_witness(bundle)
                for case, bundle in cases.items()
            }
            for boundary, cases in _remaining_yield_requirement_bundles().items()
        }
    )
    return registered


def test_primary_relation_measurements_preserve_their_live_boundaries():
    registered = _live_relation_fidelity_cases()

    assert ("locality", "byte_measurement") in registered
    assert ("participation", "byte_pair_measurement") in registered
    assert ("yield", "byte_measurement") in registered
    assert ("locality", "assertion_movement") in registered


def _relation_implementation_specs() -> dict[str, dict]:
    requirements = {
        "exact_relation": "relation_missing",
        "occurrence_witness": "wrong_occurrence",
        "intact_evidence": "corrupted_evidence",
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
            "equal_result_content_establishes_identity": False,
            "requires": requirements,
        },
    }


def _assert_relation_anatomy(grammar: dict, specs: dict[str, dict]) -> None:
    assert set(specs) == set(grammar["relations"])
    relation_families = grammar["implementation_witness"]["relation_audit"][
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
    assignment = event.material["responsibility_assignment_evidence"]
    joined = (
        act_evidence is not None
        and event.material["downstream_act_identity"]
        == act_evidence.material["downstream_act_identity"]
        and event.material["act_occurrence_identity"]
        == act_evidence.material["act_occurrence_identity"]
        and event.material["responsibility"]
        == act_evidence.material["responsibility"]
        and event.material["responsible_boundary"]
        == act_evidence.material["responsible_boundary"]
        and assignment
        == act_evidence.material.get("responsibility_assignment_evidence")
    )
    return {
        "Responsibility": EXACT if joined else MISSING,
        "Responsibility_assignment_Standing": (
            EXACT if joined and assignment.get("standing") == "assigned" else MISSING
        ),
        "responsible_boundary": EXACT if joined else MISSING,
        "exact_Act": EXACT if joined else MISSING,
        "Act_occurrence": EXACT if joined else MISSING,
        "occurrence_Evidence": (
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
            and assignment.get("completeness_boundary")
            else MISSING
        ),
        "limits": (
            EXACT if event.material["dimensions"].get("authority") else MISSING
        ),
    }


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


def _locality_fidelity_cases() -> dict[str, str]:
    exact = _recorded_applicability()

    relation_missing = _recorded_applicability()
    relation_missing["movement"].material["locality_relation"]["second_subject"] = (
        "another bounded subject"
    )

    wrong_occurrence = _recorded_applicability()
    source_occurrence = wrong_occurrence["ledger"].get(
        wrong_occurrence["movement"].material["source_assertion_reference"][
            "recorded_occurrence_identity"
        ]
    )
    wrong_occurrence["movement_act_evidence"].material["locality_relation"][
        "relation_occurrence_identity"
    ] = source_occurrence.identity

    corrupted_evidence = _recorded_applicability()
    corrupted_evidence["ledger"].mark_corrupted(
        corrupted_evidence["movement_act_evidence"].identity
    )

    unrelated_occurrence = _recorded_applicability()
    unrelated_occurrence["movement"].material["movement_scope"] = "another description"

    return {
        "exact": _locality_witness(exact),
        "relation_missing": _locality_witness(relation_missing),
        "wrong_occurrence": _locality_witness(wrong_occurrence),
        "corrupted_evidence": _locality_witness(corrupted_evidence),
        "unrelated_occurrence": _locality_witness(unrelated_occurrence),
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
        and applicability["downstream_act_identity"] == pair.material["downstream_act_identity"]
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


def test_implementation_witness_discriminates_content_and_locality():
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
    assert first.material != changed_content.material
    assert first.locality_identity == changed_content.locality_identity

    assert grammar["discriminators"] == ["content", "locality"]
    assert grammar["non_equivalence"] == [
        ["content", "locality"],
    ]


def test_fidelity_is_this_seeds_bounded_machine_comparison():
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))

    assert grammar["fidelity"] == {
        "book_clause": "01.Source.C",
        "subject": "this_Seed",
        "grammar": "machine_grammar",
        "comparison": "deterministic_tests",
        "witness": "live_implementation",
        "result": "bounded_Fidelity_finding",
        "does_not_establish": "global_certification",
    }


def test_every_relation_has_live_fidelity_cases():
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))
    cases = _relation_fidelity_cases()
    specs = _relation_implementation_specs()
    expected = grammar["implementation_witness"]["fidelity_cases"]

    _assert_relation_anatomy(grammar, specs)
    assert set(cases) == set(grammar["relations"])
    assert all(set(relation_cases) == set(expected) for relation_cases in cases.values())
    assert cases == {
        relation: expected for relation in grammar["relations"]
    }
    for relation, spec in specs.items():
        for adversary in spec["requires"].values():
            assert cases[relation][adversary] == MISSING


def test_emission_instantiates_each_relation_it_carries_at_its_boundary():
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))
    cases = _emission_relation_fidelity_cases()
    expected = grammar["implementation_witness"]["fidelity_cases"]

    assert set(cases) == {"locality", "participation", "yield"}
    assert set(cases) == set(grammar["relations"])
    assert cases == {relation: expected for relation in cases}


def test_every_registered_live_relation_instantiation_obeys_the_full_fidelity_matrix():
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))
    expected = grammar["implementation_witness"]["fidelity_cases"]
    registered = _live_relation_fidelity_cases()

    assert registered
    assert {relation for relation, _boundary in registered} == set(
        grammar["relations"]
    )
    assert all(cases == expected for cases in registered.values())
    assert ("locality", "representation_result") in registered
    assert ("locality", "emission_attempt") in registered
    assert {
        boundary for relation, boundary in registered if relation == "yield"
    } == set(YIELD_LIVE_BOUNDARIES)


def test_every_yield_evidence_site_declares_its_live_boundary():
    declared: list[str] = []
    for path in sorted(RUNTIME.glob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            if not isinstance(node.func, ast.Name):
                continue
            if node.func.id != "_record_yield_evidence":
                continue
            boundary = next(
                (keyword.value for keyword in node.keywords if keyword.arg == "live_boundary"),
                None,
            )
            assert isinstance(boundary, ast.Constant), (
                f"{path.name}:{node.lineno} must declare one literal live_boundary"
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
    assert set(declared) == set(YIELD_LIVE_BOUNDARIES)


def test_byte_pair_yield_adversaries_change_one_requirement_each():
    expected = {
        "exact": (True, True, True),
        "relation_missing": (False, True, True),
        "wrong_occurrence": (True, False, True),
        "corrupted_evidence": (True, True, False),
        "unrelated_occurrence": (True, True, True),
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
        "wrong_occurrence": (True, False, True),
        "corrupted_evidence": (True, True, False),
        "unrelated_occurrence": (True, True, True),
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
    wrong_occurrence = dict(exact)
    wrong_occurrence["attempt_locality_evidence"] = alternate[
        "attempt_locality_evidence"
    ]

    missing_relation = dict(exact)
    different = dict(exact["attempt_locality_evidence"].material)
    different["carried_content"] = "different carried content"
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
    unrelated_attempt.material["yield_evidence_identity"] = "unrelated-yield"
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
    assert _emission_attempt_locality_requirements(wrong_occurrence) == {
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
        "wrong_occurrence": {
            "exact_relation": True,
            "occurrence_witness": False,
            "intact_evidence": True,
        },
        "corrupted_evidence": {
            "exact_relation": True,
            "occurrence_witness": True,
            "intact_evidence": False,
        },
        "unrelated_occurrence": {
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
    unrelated_event.material["yield_evidence_identity"] = "different-yield-evidence"
    unrelated_locality["event"] = unrelated_event

    missing_yield = dict(exact)
    missing_yield_event = deepcopy(exact["event"])
    missing_yield_event.material["yield_evidence_identity"] = "missing-yield-evidence"
    missing_yield["event"] = missing_yield_event
    wrong_yield = dict(exact)
    wrong_act_evidence = deepcopy(exact["act_evidence"])
    wrong_content_evidence = deepcopy(exact["content_evidence"])
    alternate_occurrence = alternate["event"].material["act_occurrence_identity"]
    wrong_act_evidence.material["act_occurrence_identity"] = alternate_occurrence
    wrong_content_evidence.material["dimensions"]["act_occurrence_identity"] = (
        alternate_occurrence
    )
    wrong_yield["act_evidence"] = wrong_act_evidence
    wrong_yield["content_evidence"] = wrong_content_evidence
    corrupted_yield = _representation_witness()
    corrupted_yield["ledger"].mark_corrupted(
        corrupted_yield["content_evidence"].identity
    )
    unrelated_yield = dict(exact)
    unrelated_yield_event = deepcopy(exact["event"])
    unrelated_yield_event.material["locality_evidence_identity"] = "different-locality"
    unrelated_yield["event"] = unrelated_yield_event

    expected = {
        "exact": (True, True, True),
        "relation_missing": (False, True, True),
        "wrong_occurrence": (True, False, True),
        "corrupted_evidence": (True, True, False),
        "unrelated_occurrence": (True, True, True),
    }
    bundles = {
        "locality": {
            "exact": exact,
            "relation_missing": missing_locality,
            "wrong_occurrence": wrong_locality,
            "corrupted_evidence": corrupted_locality,
            "unrelated_occurrence": unrelated_locality,
        },
        "yield": {
            "exact": exact,
            "relation_missing": missing_yield,
            "wrong_occurrence": wrong_yield,
            "corrupted_evidence": corrupted_yield,
            "unrelated_occurrence": unrelated_yield,
        },
    }
    witnesses = {
        "locality": _representation_locality_requirements,
        "yield": _occurrence_result_requirements,
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
    unrelated_event.material["yield_evidence_identity"] = "different-yield-evidence"
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
    unrelated_pair.material["yield_evidence_identity"] = "different-yield-evidence"
    unrelated_participation["pair_event"] = unrelated_pair

    exact_yield = _byte_measurement_witness()
    alternate_yield = _byte_measurement_witness()
    missing_yield = dict(exact_yield)
    missing_yield_event = deepcopy(exact_yield["event"])
    missing_yield_event.material["yield_evidence_identity"] = (
        "missing-yield-evidence"
    )
    missing_yield["event"] = missing_yield_event
    wrong_yield = dict(exact_yield)
    wrong_act_evidence = deepcopy(exact_yield["act_evidence"])
    wrong_content_evidence = deepcopy(exact_yield["content_evidence"])
    alternate_occurrence = alternate_yield["event"].material["act_occurrence_identity"]
    wrong_act_evidence.material["act_occurrence_identity"] = alternate_occurrence
    wrong_content_evidence.material["dimensions"]["act_occurrence_identity"] = (
        alternate_occurrence
    )
    wrong_yield["act_evidence"] = wrong_act_evidence
    wrong_yield["content_evidence"] = wrong_content_evidence
    corrupted_yield = _byte_measurement_witness()
    corrupted_yield["ledger"].mark_corrupted(
        corrupted_yield["content_evidence"].identity
    )
    unrelated_yield = dict(exact_yield)
    unrelated_yield_event = deepcopy(exact_yield["event"])
    unrelated_yield_event.material["occurrence_preservation"] = "different"
    unrelated_yield["event"] = unrelated_yield_event

    expected = {
        "exact": (True, True, True),
        "relation_missing": (False, True, True),
        "wrong_occurrence": (True, False, True),
        "corrupted_evidence": (True, True, False),
        "unrelated_occurrence": (True, True, True),
    }
    actual = {
        "locality": {
            "exact": _assertion_locality_requirements(
                locality, occurrence_identity=locality["event"].identity
            ),
            "relation_missing": _assertion_locality_requirements(
                missing_locality, occurrence_identity=locality["event"].identity
            ),
            "wrong_occurrence": _assertion_locality_requirements(
                locality, occurrence_identity=alternate_locality["event"].identity
            ),
            "corrupted_evidence": _assertion_locality_requirements(
                corrupted_locality,
                occurrence_identity=corrupted_locality["event"].identity,
            ),
            "unrelated_occurrence": _assertion_locality_requirements(
                unrelated_locality, occurrence_identity=locality["event"].identity
            ),
        },
        "participation": {
            case: _participation_requirements(bundle, role=BYTE_PAIR_INPUT_ROLE)
            for case, bundle in {
                "exact": participation,
                "relation_missing": missing_participation,
                "wrong_occurrence": wrong_participation,
                "corrupted_evidence": corrupted_participation,
                "unrelated_occurrence": unrelated_participation,
            }.items()
        },
        "yield": {
            case: _occurrence_result_requirements(bundle)
            for case, bundle in {
                "exact": exact_yield,
                "relation_missing": missing_yield,
                "wrong_occurrence": wrong_yield,
                "corrupted_evidence": corrupted_yield,
                "unrelated_occurrence": unrelated_yield,
            }.items()
        },
    }

    assert {
        relation: {case: tuple(requirements.values()) for case, requirements in cases.items()}
        for relation, cases in actual.items()
    } == {relation: expected for relation in actual}


def test_attempt_and_success_have_distinct_locality_relations_for_the_same_text():
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

    assert emission["attempt"].material["representation"] == emission[
        "event"
    ].material["emitted_representation"]
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
    missing["content_evidence"] = None
    wrong_occurrence = dict(representation)
    wrong_occurrence["content_evidence"] = alternate["content_evidence"]
    missing_locality = dict(representation)
    missing_locality["locality_evidence"] = None
    wrong_locality = dict(representation)
    wrong_locality["locality_evidence"] = alternate["locality_evidence"]

    assert _representation_locality_witness(representation) == EXACT
    assert _representation_locality_witness(missing_locality) == MISSING
    assert _representation_locality_witness(wrong_locality) == MISSING
    assert _occurrence_result_witness(representation) == EXACT
    assert _occurrence_result_witness(missing) == MISSING
    assert _occurrence_result_witness(wrong_occurrence) == MISSING
    assert "input_role" not in representation["event"].material


def test_changed_relation_anatomy_is_detected():
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))
    grammar["relations"]["yield"]["from"] = "result"

    try:
        _assert_relation_anatomy(
            grammar, _relation_implementation_specs()
        )
    except AssertionError:
        pass
    else:
        raise AssertionError("reversed Yield anatomy escaped implementation Fidelity")


def test_content_and_locality_endpoints_do_not_establish_locality_relation():
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
        "Unknowns": EXACT,
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

    first = record_byte_count_layer(
        ledger,
        source_localities=("source-one",),
        recording_locality_identity="measurement-one",
    )
    repeated = record_byte_count_layer(
        ledger,
        source_localities=("source-one",),
        recording_locality_identity="measurement-two",
    )
    other_scope = record_byte_count_layer(
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
        "currentness": INAPPLICABLE,
        "occurrence_identity": EXACT,
        "known_loss": UNKNOWN,
        "conflicts": EXACT,
        "Unknowns": EXACT,
        "negative_Authority": EXACT,
    }


def test_input_is_an_open_act_local_role_before_participation():
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))
    bundle = _recorded_applicability()
    applicability = bundle["applicability"]

    assert grammar["input_role"] == {
        "kind": "Act_local_role",
        "preserves_subject_identity": True,
        "distinct_from": [
            "subject",
            "locality",
            "Applicability",
            "Admission",
            "participation",
            "input_to_result_support",
        ],
    }
    assert applicability["input_role"] == BYTE_PAIR_INPUT_ROLE
    assert applicability["downstream_act_occurrence_identity"] is None


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


def test_unjoined_endpoints_do_not_witness_an_input_to_act_relation():
    grammar = _witness_grammar()
    bundle = _recorded_applicability()
    bundle["act_evidence"] = None
    witness = _applicability_witness(bundle)

    assert bundle["applicability"]["input_assertion_reference"]
    assert bundle["applicability"]["downstream_act_identity"]
    assert bundle["applicability"]["applicability_act_occurrence_identity"]
    assert grammar["relation_audit"] == {
        "endpoint_presence_establishes_relation": False,
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

    wrong_occurrence = _recorded_applicability()
    source_occurrence = wrong_occurrence["ledger"].get(
        wrong_occurrence["movement"].material["source_assertion_reference"][
            "recorded_occurrence_identity"
        ]
    )
    wrong_occurrence["movement_act_evidence"].material["locality_relation"][
        "relation_occurrence_identity"
    ] = source_occurrence.identity

    corrupted_evidence = _recorded_applicability()
    corrupted_evidence["ledger"].mark_corrupted(
        corrupted_evidence["movement_act_evidence"].identity
    )

    unrelated_occurrence = _recorded_applicability()
    unrelated_occurrence["movement"].material["movement_scope"] = "another description"

    cases = {
        "exact": exact,
        "relation_missing": relation_missing,
        "wrong_occurrence": wrong_occurrence,
        "corrupted_evidence": corrupted_evidence,
        "unrelated_occurrence": unrelated_occurrence,
    }
    assert {name: _locality_witness(case) for name, case in cases.items()} == {
        "exact": EXACT,
        "relation_missing": MISSING,
        "wrong_occurrence": MISSING,
        "corrupted_evidence": MISSING,
        "unrelated_occurrence": EXACT,
    }
    assert _locality_requirements(relation_missing) == {
        "exact_relation": False,
        "occurrence_witness": True,
        "intact_evidence": True,
    }
    assert _locality_requirements(wrong_occurrence) == {
        "exact_relation": True,
        "occurrence_witness": False,
        "intact_evidence": True,
    }
    assert _locality_requirements(corrupted_evidence) == {
        "exact_relation": True,
        "occurrence_witness": True,
        "intact_evidence": False,
    }


def test_occurrence_and_result_endpoints_do_not_establish_their_relation():
    bundle = _byte_measurement_witness()
    assert _occurrence_result_witness(bundle) == EXACT

    event = bundle["event"]
    assert event.material["act_occurrence_identity"]
    assert event.material["assertions"]
    bundle["content_evidence"] = None
    assert _occurrence_result_witness(bundle) == MISSING


def test_yield_relation_read_has_no_result_reencoding_surface():
    bundle = _byte_measurement_witness()
    import seed_runtime.yield_evidence as yield_module

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
    assert set(bundles) == set(YIELD_LIVE_BOUNDARIES)
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
    evidence = bundle["content_evidence"]
    occurrence_coordinate = bundle.get(
        "recorded_result_occurrence_coordinate", "act_occurrence_identity"
    )
    for coordinate in evidence.material["yield_coordinates"]:
        carried_at = evidence.material["recorded_result_coordinates"][coordinate]
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
        missing_reference_event.material["yield_evidence_identity"] = (
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
        wrong_result_evidence = deepcopy(exact["content_evidence"])
        wrong_result_evidence.material["result_identity"] = (
            "different result identity"
        )
        wrong_evidence_result_identity["content_evidence"] = wrong_result_evidence
        assert _occurrence_result_requirements(wrong_evidence_result_identity) == {
            "exact_relation": False,
            "occurrence_witness": True,
            "intact_evidence": True,
        }, boundary

        wrong_yield_act_reference = dict(exact)
        wrong_yield_evidence = deepcopy(exact["content_evidence"])
        wrong_yield_evidence.material["responsible_act_evidence_identity"] = (
            "different-act-evidence"
        )
        wrong_yield_act_reference["content_evidence"] = wrong_yield_evidence
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


def test_unrelated_yield_occurrences_do_not_share_result_identity():
    factories = {
        "byte_measurement": _byte_measurement_witness,
        "representation_result": _representation_witness,
        "successful_emission": _emission_witness,
        "assertion_locality_movement": _assertion_locality_movement_yield_witness,
        "occurrence_position_measurement": _occurrence_position_yield_witness,
        "failed_emission": _failed_emission_yield_witness,
        "material_ingest": _material_ingest_yield_witness,
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

    assert set(pairs) == set(YIELD_LIVE_BOUNDARIES)
    for boundary, (first, second) in pairs.items():
        occurrence_coordinate = (
            "applicability_act_occurrence_identity"
            if boundary == "byte_pair_applicability"
            else "movement_act_occurrence_identity"
            if boundary == "assertion_locality_movement"
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

    assert set(witness) == set(clause["responsibility"]["coordinates"])
    assert set(witness.values()) == {EXACT}
    assert bundle["event"].material["downstream_act_identity"] != bundle["event"].material[
        "act_occurrence_identity"
    ]
    assert _occurrence_result_witness(bundle) == EXACT


def test_act_and_occurrence_identities_do_not_establish_their_relation():
    bundle = _byte_measurement_witness()
    event = bundle["event"]
    assert event.material["downstream_act_identity"]
    assert event.material["act_occurrence_identity"]
    bundle["act_evidence"] = None
    witness = _act_occurrence_witness(bundle)

    assert witness["exact_Act"] == MISSING
    assert witness["Act_occurrence"] == MISSING
    assert witness["occurrence_Evidence"] == MISSING


def test_responsibility_coordinates_do_not_establish_assignment_standing():
    bundle = _byte_measurement_witness()
    assignment = dict(
        bundle["event"].material["responsibility_assignment_evidence"]
    )
    assignment.pop("standing")
    bundle["event"].material["responsibility_assignment_evidence"] = assignment
    bundle["act_evidence"].material["responsibility_assignment_evidence"] = dict(
        assignment
    )

    witness = _act_occurrence_witness(bundle)
    assert witness["Responsibility"] == EXACT
    assert witness["responsible_boundary"] == EXACT
    assert witness["Responsibility_assignment_Standing"] == MISSING


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
    "operator.addressed_representation.locality_evidenced": "operator_checkpoint",
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
    registered = _live_relation_fidelity_cases()
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
# or a dedicated one. grammar.json requires exact_relation, occurrence_witness,
# and intact_evidence, and names no species for them.
RELATION_EVIDENCE = {
    "_checkpoint_locality_requirements": (
        "locality",
        "a command-to-checkpoint locality-evidence occurrence",
    ),
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
    checkpoint, _ = _checkpoint_locality_witnesses()

    return {
        "_checkpoint_locality_requirements": _checkpoint_locality_requirements(
            checkpoint
        ),
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
    }


def test_every_live_relation_witness_names_its_relation_and_its_evidence():
    """Runtime discovery equated with the registry, for all three relations."""

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
    """Each relation grammar.json declares has a live witness."""

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
