import ast
import json
import re
from io import StringIO
from pathlib import Path

from seed_runtime.byte_measurement import (
    BYTE_PAIR_INPUT_ROLE,
    _identity,
    _validate_moved_byte_assertion,
    assertions_of_recorded_byte_measurement,
    get_recorded_pair_input_applicability,
    record_adjacent_byte_pair_count_layer,
    record_byte_count_layer,
)
from seed_runtime.events import CORRUPTED, EventLedger
from seed_runtime.operator_console import run_persistent_operator_console
from seed_runtime.operator_representation import (
    REPRESENTATION_EMISSION_INPUT_ROLE,
    emit_operator_representation,
    record_operator_representation,
)
from seed_runtime.yield_evidence import YIELD_LIVE_BOUNDARIES, yield_commitment


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
        self._corrupted_ids: set[str] = set()

    def mark_corrupted(self, event_id: str) -> None:
        self._corrupted_ids.add(event_id)

    def integrity_of(self, event_id: str) -> str:
        if event_id in self._corrupted_ids:
            return CORRUPTED
        return super().integrity_of(event_id)


def _clause(clause_id: str) -> dict:
    return json.loads(GRAMMAR.read_text(encoding="utf-8"))["clauses"][clause_id]


def _witness_grammar() -> dict:
    return json.loads(GRAMMAR.read_text(encoding="utf-8"))["implementation_witness"]


def test_live_runtime_carries_no_retired_collective_vocabulary():
    runtime = Path(__file__).resolve().parents[1] / "seed_runtime"
    retired = "popu" + "lation"
    found = [path for path in runtime.glob("*.py") if retired in path.read_text().lower()]
    assert found == []


def _digest_only_witness(digest: str) -> dict[str, str]:
    assert isinstance(digest, str) and len(digest) == 64
    return {
        "digest": EXACT,
        "content_reconstruction": MISSING,
        "occurrence": MISSING,
        "provenance": MISSING,
        "Standing": MISSING,
        "Evidence": MISSING,
    }


def _content_carriage_witness(
    content: dict, *, carriage, occurrence_id: str
) -> str:
    if carriage is None:
        return MISSING
    return (
        EXACT
        if carriage.id == occurrence_id and carriage.payload == content
        else MISSING
    )


def _assertion_carriage_witness(bundle: dict, *, occurrence_id: str) -> str:
    requirements = _assertion_carriage_requirements(
        bundle, occurrence_id=occurrence_id
    )
    return EXACT if all(requirements.values()) else MISSING


def _assertion_carriage_requirements(
    bundle: dict, *, occurrence_id: str
) -> dict[str, bool]:
    assertion = bundle["source_assertion"]
    carrier = bundle["carrier"]
    carried = [
        item
        for item in carrier.payload.get("assertions", [])
        if item.get("dimensions", {}).get("identity") == assertion.assertion_id
    ]
    exact_relation = carried == [assertion.payload]
    exact_occurrence = (
        carrier.id == occurrence_id
        == assertion.recorded_occurrence_id
    )
    intact = bundle["ledger"].integrity_of(carrier.id) != CORRUPTED
    return {
        "exact_relation": exact_relation,
        "occurrence_witness": exact_occurrence,
        "intact_evidence": intact,
    }


def _representation_digest_witness(
    representation: dict, *, convention: str, digest: str
) -> str:
    return (
        EXACT
        if yield_commitment(convention, representation) == digest
        else MISSING
    )


def _recorded_digest_witness(
    representation: dict,
    *,
    convention: str,
    digest: str,
    digest_carriage,
    digest_occurrence_id: str,
) -> str:
    if digest_carriage is None:
        return MISSING
    mechanically_matches = (
        yield_commitment(convention, representation) == digest
    )
    exact_carriage = (
        digest_carriage.id == digest_occurrence_id
        and digest_carriage.payload.get("yield_commitment") == digest
    )
    return EXACT if mechanically_matches and exact_carriage else MISSING


def _source_assertion():
    road = _byte_measurement_road()
    return road["source_assertion"]


def _byte_measurement_road() -> dict:
    ledger = _IntegrityAdversaryLedger()
    run_persistent_operator_console(
        ledger=ledger,
        workspace_id="w",
        session_id="source",
        input_stream=StringIO("ta\nexit\n"),
        output_stream=StringIO(),
    )
    measurement = record_byte_count_layer(
        ledger,
        workspace_id="w",
        source_session_ids=("source",),
        recording_session_id="byte-measurement",
    )
    assertion = next(
        item
        for item in assertions_of_recorded_byte_measurement(ledger, measurement.id)
        if item.result == "exact_source_material_set"
    )
    return {
        "ledger": ledger,
        "carrier": measurement,
        "source_assertion": assertion,
        "act_evidence": ledger.get(measurement.payload["responsible_act_evidence_id"]),
        "content_evidence": ledger.get(measurement.payload["yield_evidence_id"]),
    }


def _recorded_applicability() -> dict:
    # RecordedByteAssertion deliberately carries no ledger handle. Recreate the
    # live road so every relation can be checked through its own occurrences.
    ledger = _IntegrityAdversaryLedger()
    run_persistent_operator_console(
        ledger=ledger,
        workspace_id="w",
        session_id="source",
        input_stream=StringIO("ta\nexit\n"),
        output_stream=StringIO(),
    )
    byte_measurement = record_byte_count_layer(
        ledger,
        workspace_id="w",
        source_session_ids=("source",),
        recording_session_id="byte-measurement",
    )
    pair_measurement = record_adjacent_byte_pair_count_layer(
        ledger,
        source_measurement_event_id=byte_measurement.id,
        workspace_id="w",
        recording_session_id="measurement",
    )
    carrier = ledger.get(pair_measurement.payload["input_applicability_event_id"])
    recovered = get_recorded_pair_input_applicability(ledger, carrier.id)
    movement = ledger.get(recovered["input_movement_event_id"])
    return {
        "ledger": ledger,
        "applicability": recovered,
        "carrier": carrier,
        "act_evidence": ledger.get(carrier.payload["responsible_act_evidence_id"]),
        "content_evidence": ledger.get(carrier.payload["yield_evidence_id"]),
        "movement": movement,
        "movement_act_evidence": ledger.get(
            movement.payload["movement_act_evidence_event_id"]
        ),
        "pair_carrier": pair_measurement,
        "pair_act_evidence": ledger.get(
            pair_measurement.payload["responsible_act_evidence_id"]
        ),
        "pair_content_evidence": ledger.get(
            pair_measurement.payload["yield_evidence_id"]
        ),
    }


def _emission_road() -> dict:
    ledger = _IntegrityAdversaryLedger()
    representation = record_operator_representation(
        ledger,
        workspace_id="w",
        session_id="emission",
        session_standing={"as_of_event_id": None},
    )
    emit_operator_representation(
        ledger,
        representation=representation,
        output_stream=StringIO(),
    )
    carrier = ledger.get(representation["emitted_event_id"])
    return {
        "ledger": ledger,
        "carrier": carrier,
        "attempt": ledger.get(representation["emission_attempt_event_id"]),
        "attempt_carriage_evidence": ledger.get(
            representation["emission_attempt_carriage_evidence_id"]
        ),
        "act_evidence": ledger.get(
            carrier.payload["responsible_act_evidence_id"]
        ),
        "carriage_evidence": ledger.get(carrier.payload["carriage_evidence_id"]),
        "content_evidence": ledger.get(carrier.payload["yield_evidence_id"]),
    }


def _repeated_emission_attempt_road() -> tuple[dict, dict]:
    ledger = _IntegrityAdversaryLedger()
    representation = record_operator_representation(
        ledger,
        workspace_id="w",
        session_id="repeated-emission-attempt",
        session_standing={"as_of_event_id": None},
    )
    emit_operator_representation(
        ledger,
        representation=representation,
        output_stream=StringIO(),
    )
    first_attempt = ledger.get(representation["emission_attempt_event_id"])
    first_evidence = ledger.get(
        representation["emission_attempt_carriage_evidence_id"]
    )
    first_carrier = ledger.get(representation["emitted_event_id"])
    first_act_evidence = ledger.get(
        first_carrier.payload["responsible_act_evidence_id"]
    )
    first_carriage_evidence = ledger.get(
        first_carrier.payload["carriage_evidence_id"]
    )
    first_yield_evidence = ledger.get(first_carrier.payload["yield_evidence_id"])
    emit_operator_representation(
        ledger,
        representation=representation,
        output_stream=StringIO(),
    )
    second_attempt = ledger.get(representation["emission_attempt_event_id"])
    second_evidence = ledger.get(
        representation["emission_attempt_carriage_evidence_id"]
    )
    second_carrier = ledger.get(representation["emitted_event_id"])
    second_act_evidence = ledger.get(
        second_carrier.payload["responsible_act_evidence_id"]
    )
    second_carriage_evidence = ledger.get(
        second_carrier.payload["carriage_evidence_id"]
    )
    second_yield_evidence = ledger.get(second_carrier.payload["yield_evidence_id"])
    return (
        {
            "ledger": ledger,
            "attempt": first_attempt,
            "attempt_carriage_evidence": first_evidence,
            "carrier": first_carrier,
            "act_evidence": first_act_evidence,
            "carriage_evidence": first_carriage_evidence,
            "content_evidence": first_yield_evidence,
        },
        {
            "ledger": ledger,
            "attempt": second_attempt,
            "attempt_carriage_evidence": second_evidence,
            "carrier": second_carrier,
            "act_evidence": second_act_evidence,
            "carriage_evidence": second_carriage_evidence,
            "content_evidence": second_yield_evidence,
        },
    )


def _representation_road() -> dict:
    ledger = _IntegrityAdversaryLedger()
    representation = record_operator_representation(
        ledger,
        workspace_id="w",
        session_id="representation",
        session_standing={"as_of_event_id": None},
    )
    carrier = ledger.get(representation["representation_event_id"])
    return {
        "ledger": ledger,
        "carrier": carrier,
        "act_evidence": ledger.get(carrier.payload["responsible_act_evidence_id"]),
        "carriage_evidence": ledger.get(carrier.payload["carriage_evidence_id"]),
        "content_evidence": ledger.get(carrier.payload["yield_evidence_id"]),
    }


def _repeated_representation_road() -> tuple[dict, dict]:
    ledger = _IntegrityAdversaryLedger()

    def record() -> dict:
        representation = record_operator_representation(
            ledger,
            workspace_id="w",
            session_id="repeated-representation",
            session_standing={"as_of_event_id": None},
        )
        carrier = ledger.get(representation["representation_event_id"])
        return {
            "ledger": ledger,
            "carrier": carrier,
            "act_evidence": ledger.get(
                carrier.payload["responsible_act_evidence_id"]
            ),
            "carriage_evidence": ledger.get(
                carrier.payload["carriage_evidence_id"]
            ),
            "content_evidence": ledger.get(carrier.payload["yield_evidence_id"]),
        }

    return record(), record()


def _assertion_witness(bundle: dict) -> dict[str, str]:
    assertion = bundle["source_assertion"]
    carrier = bundle["carrier"]
    content_evidence = bundle["content_evidence"]
    payload = assertion.payload
    dimensions = payload["dimensions"]
    expected_identity = _identity(
        result=payload["result"],
        subject=payload["assertion_subject"],
        scope=payload["assertion_scope"],
        content=dimensions["content"],
    )
    carried_assertion = next(
        (
            item
            for item in carrier.payload["assertions"]
            if item["dimensions"]["identity"] == assertion.assertion_id
        ),
        None,
    )
    evidence_edge = (
        assertion.recorded_occurrence_id == carrier.id
        and carried_assertion == payload
        and content_evidence is not None
        and carrier.payload.get("yield_evidence_id") == content_evidence.id
        and "assertions" in content_evidence.payload.get("yield_coordinates", [])
    )
    return {
        "identity": (
            EXACT if dimensions.get("identity") == expected_identity else CONTRADICTION
        ),
        # Evidence remains on the occurrence/result edge. It is recovered
        # through the exact carriage, not copied from support_basis.
        "Evidence": EXACT if evidence_edge else MISSING,
        "provenance": EXACT if dimensions.get("source_provenance") else MISSING,
        "Scope": EXACT if payload.get("assertion_scope") else MISSING,
        "Authority": EXACT if dimensions.get("authority") else MISSING,
        "conflicts": UNKNOWN if payload.get("conflicts") == "Unknown" else MISSING,
        "limits": EXACT if payload.get("forbidden_inferences") else MISSING,
        "Unknowns": EXACT if payload.get("unknowns") else MISSING,
        "Standing": EXACT if dimensions.get("standing") else MISSING,
    }


def _applicability_witness(bundle: dict) -> dict[str, str]:
    applicability = bundle["applicability"]
    carrier = bundle["carrier"]
    act_evidence = bundle["act_evidence"]
    content_evidence = bundle["content_evidence"]
    content = applicability["dimensions"]["content"]
    treatment = applicability["coordinate_treatment"]
    input_edge = (
        act_evidence is not None
        and carrier.payload.get("input_assertion_ref")
        == applicability.get("input_assertion_ref")
        == act_evidence.payload.get("input_assertion_ref")
    )
    act_edge = (
        act_evidence is not None
        and carrier.payload.get("target_act_id")
        == applicability.get("target_act_id")
        == act_evidence.payload.get("target_act_id")
    )
    occurrence_edge = (
        act_evidence is not None
        and carrier.payload.get("applicability_act_occurrence_id")
        == applicability.get("applicability_act_occurrence_id")
        == act_evidence.payload.get("applicability_act_occurrence_id")
    )
    carried_result = (
        content_evidence is not None
        and carrier.payload.get("yield_evidence_id") == content_evidence.id
        and carrier.payload["dimensions"].get("standing")
        == applicability["dimensions"].get("standing")
    )
    return {
        "input_identity": EXACT if input_edge else MISSING,
        "exact_Act": EXACT if act_edge else MISSING,
        "subject": EXACT if content.get("target_act") else MISSING,
        "result_boundary": EXACT if applicability.get("result_boundary") else MISSING,
        "Scope": EXACT if applicability.get("scope_locality") else MISSING,
        "locality": EXACT if applicability.get("act_context") else MISSING,
        "Authority": EXACT if applicability["dimensions"].get("authority") else MISSING,
        # The relation endpoints already identify the exact input role and the
        # exact addressed-Act role; no extra participant noun is supplied.
        "participants_and_roles": EXACT if input_edge and act_edge else MISSING,
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
            EXACT if occurrence_edge else MISSING
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
    carrier = bundle["carrier"]
    act_evidence = bundle["act_evidence"]
    content_evidence = bundle["content_evidence"]
    if act_evidence is None or content_evidence is None:
        return {
            "exact_relation": False,
            "occurrence_witness": False,
            "intact_evidence": False,
        }
    carrier_occurrence_coordinate = bundle.get(
        "carrier_occurrence_coordinate", "act_occurrence_id"
    )
    act_evidence_occurrence_coordinate = bundle.get(
        "act_evidence_occurrence_coordinate", "act_occurrence_id"
    )
    same_occurrence = carrier.payload.get(carrier_occurrence_coordinate) == (
        act_evidence.payload.get(act_evidence_occurrence_coordinate)
    ) == content_evidence.payload.get("dimensions", {}).get("act_occurrence_id")
    yield_coordinates = content_evidence.payload.get("yield_coordinates")
    if not isinstance(yield_coordinates, list) or not all(
        isinstance(key, str) and key in carrier.payload for key in yield_coordinates
    ):
        return {
            "exact_relation": False,
            "occurrence_witness": same_occurrence,
            "intact_evidence": (
                bundle["ledger"].integrity_of(act_evidence.id) != CORRUPTED
                and bundle["ledger"].integrity_of(content_evidence.id)
                != CORRUPTED
            ),
        }
    actual_result = {key: carrier.payload[key] for key in yield_coordinates}
    actual_commitment = yield_commitment(
        content_evidence.payload.get("yield_convention"), actual_result
    )
    same_result = (
        act_evidence.payload.get("result_commitment")
        == content_evidence.payload.get("yield_commitment")
        == actual_commitment
    )
    evidence_is_carried = (
        carrier.payload.get("responsible_act_evidence_id") == act_evidence.id
        and carrier.payload.get("yield_evidence_id") == content_evidence.id
    )
    return {
        "exact_relation": same_result and evidence_is_carried,
        "occurrence_witness": same_occurrence,
        "intact_evidence": (
            bundle["ledger"].integrity_of(act_evidence.id) != CORRUPTED
            and bundle["ledger"].integrity_of(content_evidence.id) != CORRUPTED
        ),
    }


def _emission_carriage_witness(bundle: dict) -> str:
    requirements = _emission_carriage_requirements(bundle)
    return EXACT if all(requirements.values()) else MISSING


def _emission_carriage_requirements(bundle: dict) -> dict[str, bool]:
    carrier = bundle["carrier"]
    evidence = bundle["carriage_evidence"]
    if evidence is None:
        return {
            "exact_relation": False,
            "occurrence_witness": False,
            "intact_evidence": False,
        }
    exact_relation = (
        carrier.payload.get("emitted_representation")
        == evidence.payload.get("carried_content")
    )
    exact_occurrence = (
        carrier.payload.get("act_occurrence_id")
        == evidence.payload.get("act_occurrence_id")
    )
    evidence_is_carried = carrier.payload.get("carriage_evidence_id") == evidence.id
    return {
        "exact_relation": exact_relation and evidence_is_carried,
        "occurrence_witness": exact_occurrence,
        "intact_evidence": (
            bundle["ledger"].integrity_of(evidence.id) != CORRUPTED
        ),
    }


def _emission_attempt_carriage_witness(bundle: dict) -> str:
    requirements = _emission_attempt_carriage_requirements(bundle)
    return EXACT if all(requirements.values()) else MISSING


def _emission_attempt_carriage_requirements(bundle: dict) -> dict[str, bool]:
    attempt = bundle["attempt"]
    evidence = bundle["attempt_carriage_evidence"]
    if evidence is None:
        return {
            "exact_relation": False,
            "occurrence_witness": False,
            "intact_evidence": False,
        }
    exact_relation = (
        attempt.payload.get("attempted_representation")
        == evidence.payload.get("carried_content")
    )
    exact_occurrence = attempt.id == evidence.payload.get("attempt_event_id")
    exact_subject = (
        attempt.payload.get("representation_ref")
        == evidence.payload.get("representation_ref")
    )
    return {
        "exact_relation": exact_relation and exact_subject,
        "occurrence_witness": exact_occurrence,
        "intact_evidence": (
            bundle["ledger"].integrity_of(evidence.id) != CORRUPTED
        ),
    }


def _emission_participation_witness(bundle: dict) -> str:
    requirements = _emission_participation_requirements(bundle)
    return EXACT if all(requirements.values()) else MISSING


def _emission_participation_requirements(bundle: dict) -> dict[str, bool]:
    carrier = bundle["carrier"]
    evidence = bundle["act_evidence"]
    if evidence is None:
        return {
            "exact_relation": False,
            "occurrence_witness": False,
            "intact_evidence": False,
        }
    exact_relation = (
        carrier.payload.get("representation_ref")
        == evidence.payload.get("representation_ref")
        and carrier.payload.get("input_role")
        == evidence.payload.get("input_role")
        == REPRESENTATION_EMISSION_INPUT_ROLE
    )
    exact_occurrence = (
        carrier.payload.get("act_occurrence_id")
        == evidence.payload.get("act_occurrence_id")
    )
    evidence_is_carried = (
        carrier.payload.get("responsible_act_evidence_id") == evidence.id
    )
    return {
        "exact_relation": exact_relation and evidence_is_carried,
        "occurrence_witness": exact_occurrence,
        "intact_evidence": (
            bundle["ledger"].integrity_of(evidence.id) != CORRUPTED
        ),
    }


def _representation_carriage_witness(bundle: dict) -> str:
    requirements = _representation_carriage_requirements(bundle)
    return EXACT if all(requirements.values()) else MISSING


def _representation_carriage_requirements(bundle: dict) -> dict[str, bool]:
    carrier = bundle["carrier"]
    evidence = bundle["carriage_evidence"]
    if evidence is None:
        return {
            "exact_relation": False,
            "occurrence_witness": False,
            "intact_evidence": False,
        }
    content = evidence.payload.get("carried_content")
    exact_content = isinstance(content, dict) and all(
        carrier.payload.get(key) == value for key, value in content.items()
    )
    exact_occurrence = (
        carrier.payload.get("act_occurrence_id")
        == evidence.payload.get("act_occurrence_id")
    )
    evidence_is_carried = carrier.payload.get("carriage_evidence_id") == evidence.id
    return {
        "exact_relation": exact_content and evidence_is_carried,
        "occurrence_witness": exact_occurrence,
        "intact_evidence": (
            bundle["ledger"].integrity_of(evidence.id) != CORRUPTED
        ),
    }


def _structural_edge_fidelity_cases() -> dict[str, dict[str, str]]:
    carriage = _byte_measurement_road()
    alternate_carriage = _byte_measurement_road()
    corrupted_carriage = _byte_measurement_road()
    corrupted_carriage["ledger"].mark_corrupted(corrupted_carriage["carrier"].id)
    missing_carriage = dict(carriage)
    missing_carrier = carriage["carrier"].model_copy(deep=True)
    missing_carrier.payload["assertions"] = [
        item
        for item in missing_carrier.payload["assertions"]
        if item["dimensions"]["identity"]
        != carriage["source_assertion"].assertion_id
    ]
    missing_carriage["carrier"] = missing_carrier
    unrelated_carriage = dict(carriage)
    unrelated_carrier = carriage["carrier"].model_copy(deep=True)
    unrelated_carrier.payload["yield_evidence_id"] = "other-yield-evidence"
    unrelated_carriage["carrier"] = unrelated_carrier

    participation = _recorded_applicability()
    alternate_participation = _recorded_applicability()
    corrupted_participation = _recorded_applicability()
    corrupted_participation["ledger"].mark_corrupted(
        corrupted_participation["pair_act_evidence"].id
    )
    missing_participation = dict(participation)
    missing_participation_evidence = participation[
        "pair_act_evidence"
    ].model_copy(deep=True)
    missing_participation_evidence.payload["input_role"] = "different-role"
    missing_participation["pair_act_evidence"] = missing_participation_evidence
    wrong_participation = dict(participation)
    wrong_participation_evidence = participation[
        "pair_act_evidence"
    ].model_copy(deep=True)
    wrong_participation_evidence.payload["act_occurrence_id"] = (
        alternate_participation["pair_carrier"].payload["act_occurrence_id"]
    )
    wrong_participation["pair_act_evidence"] = wrong_participation_evidence
    unrelated_participation = dict(participation)
    unrelated_participation_carrier = participation["pair_carrier"].model_copy(
        deep=True
    )
    unrelated_participation_carrier.payload["yield_evidence_id"] = (
        "other-yield-evidence"
    )
    unrelated_participation["pair_carrier"] = unrelated_participation_carrier

    yielded = _byte_measurement_road()
    alternate_yield = _byte_measurement_road()
    corrupted_yield = _byte_measurement_road()
    corrupted_yield["ledger"].mark_corrupted(
        corrupted_yield["content_evidence"].id
    )
    missing_yield = dict(yielded)
    missing_yield_carrier = yielded["carrier"].model_copy(deep=True)
    missing_yield_carrier.payload["measurement_rule"] = "different-rule"
    missing_yield["carrier"] = missing_yield_carrier
    wrong_yield = dict(yielded)
    wrong_yield_act_evidence = yielded["act_evidence"].model_copy(deep=True)
    wrong_yield_content_evidence = yielded["content_evidence"].model_copy(deep=True)
    alternate_yield_occurrence = alternate_yield["carrier"].payload[
        "act_occurrence_id"
    ]
    wrong_yield_act_evidence.payload["act_occurrence_id"] = (
        alternate_yield_occurrence
    )
    wrong_yield_content_evidence.payload["dimensions"]["act_occurrence_id"] = (
        alternate_yield_occurrence
    )
    wrong_yield["act_evidence"] = wrong_yield_act_evidence
    wrong_yield["content_evidence"] = wrong_yield_content_evidence
    unrelated_yield = dict(yielded)
    unrelated_yield_carrier = yielded["carrier"].model_copy(deep=True)
    unrelated_yield_carrier.payload["occurrence_preservation"] = (
        "changed neighboring carriage coordinate"
    )
    unrelated_yield["carrier"] = unrelated_yield_carrier

    return {
        "carriage": {
            "exact": _assertion_carriage_witness(
                carriage,
                occurrence_id=carriage["carrier"].id,
            ),
            "edge_missing": _assertion_carriage_witness(
                missing_carriage,
                occurrence_id=carriage["carrier"].id,
            ),
            "wrong_occurrence": _assertion_carriage_witness(
                carriage,
                occurrence_id=alternate_carriage["carrier"].id,
            ),
            "corrupted_evidence": _assertion_carriage_witness(
                corrupted_carriage,
                occurrence_id=corrupted_carriage["carrier"].id,
            ),
            "unrelated_change": _assertion_carriage_witness(
                unrelated_carriage,
                occurrence_id=carriage["carrier"].id,
            ),
        },
        "participation": {
            "exact": _participation_witness(
                participation, role=BYTE_PAIR_INPUT_ROLE
            ),
            "edge_missing": _participation_witness(
                missing_participation, role=BYTE_PAIR_INPUT_ROLE
            ),
            "wrong_occurrence": _participation_witness(
                wrong_participation, role=BYTE_PAIR_INPUT_ROLE
            ),
            "corrupted_evidence": _participation_witness(
                corrupted_participation, role=BYTE_PAIR_INPUT_ROLE
            ),
            "unrelated_change": _participation_witness(
                unrelated_participation, role=BYTE_PAIR_INPUT_ROLE
            ),
        },
        "yield": {
            "exact": _occurrence_result_witness(yielded),
            "edge_missing": _occurrence_result_witness(missing_yield),
            "wrong_occurrence": _occurrence_result_witness(wrong_yield),
            "corrupted_evidence": _occurrence_result_witness(corrupted_yield),
            "unrelated_change": _occurrence_result_witness(unrelated_yield),
        },
    }


def _successful_emission_requirement_bundles() -> dict[str, dict[str, dict]]:
    emission, alternate = _repeated_emission_attempt_road()

    missing_carriage = dict(emission)
    missing_carriage_evidence = emission["carriage_evidence"].model_copy(deep=True)
    missing_carriage_evidence.payload["carried_content"] = "different content"
    missing_carriage["carriage_evidence"] = missing_carriage_evidence
    wrong_carriage = dict(emission)
    wrong_carriage_carrier = emission["carrier"].model_copy(deep=True)
    wrong_carriage_carrier.payload["carriage_evidence_id"] = alternate[
        "carriage_evidence"
    ].id
    wrong_carriage["carrier"] = wrong_carriage_carrier
    wrong_carriage["carriage_evidence"] = alternate["carriage_evidence"]
    unrelated_carriage = dict(emission)
    unrelated_carriage_carrier = emission["carrier"].model_copy(deep=True)
    unrelated_carriage_carrier.payload["yield_evidence_id"] = "other-yield-evidence"
    unrelated_carriage["carrier"] = unrelated_carriage_carrier
    corrupted_carriage = _emission_road()
    corrupted_carriage["ledger"].mark_corrupted(
        corrupted_carriage["carriage_evidence"].id
    )

    missing_participation = dict(emission)
    missing_act_evidence = emission["act_evidence"].model_copy(deep=True)
    missing_act_evidence.payload["input_role"] = "different-role"
    missing_participation["act_evidence"] = missing_act_evidence
    wrong_participation = dict(emission)
    wrong_participation_carrier = emission["carrier"].model_copy(deep=True)
    wrong_participation_carrier.payload["responsible_act_evidence_id"] = alternate[
        "act_evidence"
    ].id
    wrong_participation["carrier"] = wrong_participation_carrier
    wrong_participation["act_evidence"] = alternate["act_evidence"]
    unrelated_participation = dict(emission)
    unrelated_participation_carrier = emission["carrier"].model_copy(deep=True)
    unrelated_participation_carrier.payload["carriage_evidence_id"] = (
        "other-carriage-evidence"
    )
    unrelated_participation["carrier"] = unrelated_participation_carrier
    corrupted_participation = _emission_road()
    corrupted_participation["ledger"].mark_corrupted(
        corrupted_participation["act_evidence"].id
    )

    missing_yield = dict(emission)
    missing_yield_carrier = emission["carrier"].model_copy(deep=True)
    missing_yield_carrier.payload["yielded_result"]["accepted_length"] += 1
    missing_yield["carrier"] = missing_yield_carrier
    wrong_yield = dict(emission)
    wrong_yield_carrier = emission["carrier"].model_copy(deep=True)
    wrong_yield_carrier.payload["responsible_act_evidence_id"] = alternate[
        "act_evidence"
    ].id
    wrong_yield_carrier.payload["yield_evidence_id"] = alternate[
        "content_evidence"
    ].id
    wrong_yield["carrier"] = wrong_yield_carrier
    wrong_yield["act_evidence"] = alternate["act_evidence"]
    wrong_yield["content_evidence"] = alternate["content_evidence"]
    unrelated_yield = dict(emission)
    unrelated_yield_carrier = emission["carrier"].model_copy(deep=True)
    unrelated_yield_carrier.payload["input_role"] = "other-role"
    unrelated_yield["carrier"] = unrelated_yield_carrier
    corrupted_yield = _emission_road()
    corrupted_yield["ledger"].mark_corrupted(
        corrupted_yield["content_evidence"].id
    )
    return {
        "carriage": {
            "exact": emission,
            "edge_missing": missing_carriage,
            "wrong_occurrence": wrong_carriage,
            "corrupted_evidence": corrupted_carriage,
            "unrelated_change": unrelated_carriage,
        },
        "participation": {
            "exact": emission,
            "edge_missing": missing_participation,
            "wrong_occurrence": wrong_participation,
            "corrupted_evidence": corrupted_participation,
            "unrelated_change": unrelated_participation,
        },
        "yield": {
            "exact": emission,
            "edge_missing": missing_yield,
            "wrong_occurrence": wrong_yield,
            "corrupted_evidence": corrupted_yield,
            "unrelated_change": unrelated_yield,
        },
    }


def _emission_structural_edge_fidelity_cases() -> dict[str, dict[str, str]]:
    bundles = _successful_emission_requirement_bundles()
    witnesses = {
        "carriage": _emission_carriage_witness,
        "participation": _emission_participation_witness,
        "yield": _occurrence_result_witness,
    }
    return {
        edge: {case: witnesses[edge](bundle) for case, bundle in cases.items()}
        for edge, cases in bundles.items()
    }


def _yield_requirement_bundles(
    exact: dict,
    alternate: dict,
    corrupted: dict,
    *,
    unrelated_value,
) -> dict[str, dict]:
    missing = dict(exact)
    missing_carrier = exact["carrier"].model_copy(deep=True)
    yielded_coordinates = exact["content_evidence"].payload["yield_coordinates"]
    missing_coordinate = next(
        coordinate
        for coordinate in yielded_coordinates
        if coordinate != "act_occurrence_id"
    )
    missing_carrier.payload.pop(missing_coordinate)
    missing["carrier"] = missing_carrier

    wrong_occurrence = dict(exact)
    wrong_act_evidence = exact["act_evidence"].model_copy(deep=True)
    wrong_content_evidence = exact["content_evidence"].model_copy(deep=True)
    carrier_occurrence_coordinate = exact.get(
        "carrier_occurrence_coordinate", "act_occurrence_id"
    )
    act_evidence_occurrence_coordinate = exact.get(
        "act_evidence_occurrence_coordinate", "act_occurrence_id"
    )
    alternate_occurrence = alternate["carrier"].payload[
        carrier_occurrence_coordinate
    ]
    wrong_act_evidence.payload[act_evidence_occurrence_coordinate] = (
        alternate_occurrence
    )
    wrong_content_evidence.payload["dimensions"]["act_occurrence_id"] = (
        alternate_occurrence
    )
    wrong_occurrence["act_evidence"] = wrong_act_evidence
    wrong_occurrence["content_evidence"] = wrong_content_evidence

    unrelated = dict(exact)
    unrelated_carrier = exact["carrier"].model_copy(
        deep=True, update={"id": unrelated_value}
    )
    unrelated["carrier"] = unrelated_carrier

    corrupted["ledger"].mark_corrupted(corrupted["content_evidence"].id)
    return {
        "exact": exact,
        "edge_missing": missing,
        "wrong_occurrence": wrong_occurrence,
        "corrupted_evidence": corrupted,
        "unrelated_change": unrelated,
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
        bundle["carrier_occurrence_coordinate"] = (
            "applicability_act_occurrence_id"
        )
        bundle["act_evidence_occurrence_coordinate"] = (
            "applicability_act_occurrence_id"
        )

    pair = {
        "ledger": applicability["ledger"],
        "carrier": applicability["pair_carrier"],
        "act_evidence": applicability["pair_act_evidence"],
        "content_evidence": applicability["pair_content_evidence"],
    }
    alternate_pair = {
        "ledger": alternate_applicability["ledger"],
        "carrier": alternate_applicability["pair_carrier"],
        "act_evidence": alternate_applicability["pair_act_evidence"],
        "content_evidence": alternate_applicability["pair_content_evidence"],
    }
    corrupted_pair_source = _recorded_applicability()
    corrupted_pair = {
        "ledger": corrupted_pair_source["ledger"],
        "carrier": corrupted_pair_source["pair_carrier"],
        "act_evidence": corrupted_pair_source["pair_act_evidence"],
        "content_evidence": corrupted_pair_source["pair_content_evidence"],
    }

    return {
        "byte_pair_applicability": _yield_requirement_bundles(
            applicability,
            alternate_applicability,
            corrupted_applicability,
            unrelated_value=alternate_applicability["carrier"].id,
        ),
        "byte_pair_measurement": _yield_requirement_bundles(
            pair,
            alternate_pair,
            corrupted_pair,
            unrelated_value=alternate_pair["carrier"].id,
        ),
    }
def _additional_live_structural_edge_fidelity_cases() -> dict[
    tuple[str, str], dict[str, str]
]:
    representation, alternate_representation = _repeated_representation_road()
    missing_representation_carriage = dict(representation)
    missing_representation_carriage_evidence = representation[
        "carriage_evidence"
    ].model_copy(deep=True)
    missing_representation_carriage_evidence.payload["carried_content"][
        "representation_result"
    ] = "different result"
    missing_representation_carriage[
        "carriage_evidence"
    ] = missing_representation_carriage_evidence
    wrong_representation_carriage = dict(representation)
    wrong_representation_carriage_evidence = representation[
        "carriage_evidence"
    ].model_copy(deep=True)
    wrong_representation_carriage_evidence.payload["act_occurrence_id"] = (
        alternate_representation["carrier"].payload["act_occurrence_id"]
    )
    wrong_representation_carriage[
        "carriage_evidence"
    ] = wrong_representation_carriage_evidence
    corrupted_representation_carriage = _representation_road()
    corrupted_representation_carriage["ledger"].mark_corrupted(
        corrupted_representation_carriage["carriage_evidence"].id
    )
    unrelated_representation_carriage = dict(representation)
    unrelated_representation_carrier = representation["carrier"].model_copy(deep=True)
    unrelated_representation_carrier.payload["yield_evidence_id"] = "other-yield"
    unrelated_representation_carriage["carrier"] = unrelated_representation_carrier

    missing_representation_yield = dict(representation)
    missing_representation_yield_carrier = representation["carrier"].model_copy(
        deep=True
    )
    missing_representation_yield_carrier.payload["representation_result"] = (
        "different result"
    )
    missing_representation_yield["carrier"] = missing_representation_yield_carrier
    wrong_representation_yield = dict(representation)
    wrong_representation_act_evidence = representation["act_evidence"].model_copy(
        deep=True
    )
    wrong_representation_content_evidence = representation[
        "content_evidence"
    ].model_copy(deep=True)
    alternate_occurrence = alternate_representation["carrier"].payload[
        "act_occurrence_id"
    ]
    wrong_representation_act_evidence.payload["act_occurrence_id"] = (
        alternate_occurrence
    )
    wrong_representation_content_evidence.payload["dimensions"][
        "act_occurrence_id"
    ] = alternate_occurrence
    wrong_representation_yield["act_evidence"] = wrong_representation_act_evidence
    wrong_representation_yield[
        "content_evidence"
    ] = wrong_representation_content_evidence
    corrupted_representation_yield = _representation_road()
    corrupted_representation_yield["ledger"].mark_corrupted(
        corrupted_representation_yield["content_evidence"].id
    )
    unrelated_representation_yield = dict(representation)
    unrelated_representation_yield_carrier = representation["carrier"].model_copy(
        deep=True
    )
    unrelated_representation_yield_carrier.payload["carriage_evidence_id"] = (
        "other-carriage"
    )
    unrelated_representation_yield["carrier"] = unrelated_representation_yield_carrier

    attempt, alternate_attempt = _repeated_emission_attempt_road()
    missing_attempt = dict(attempt)
    changed_relation_payload = dict(attempt["attempt_carriage_evidence"].payload)
    changed_relation_payload["carried_content"] = "different carried content"
    missing_attempt["attempt_carriage_evidence"] = attempt["ledger"].append(
        attempt["attempt_carriage_evidence"].kind,
        "w",
        changed_relation_payload,
        session_id="repeated-emission-attempt",
    )
    wrong_attempt = dict(attempt)
    wrong_attempt["attempt_carriage_evidence"] = alternate_attempt[
        "attempt_carriage_evidence"
    ]
    corrupted_attempt, _ = _repeated_emission_attempt_road()
    corrupted_attempt["ledger"].mark_corrupted(
        corrupted_attempt["attempt_carriage_evidence"].id
    )
    unrelated_attempt = dict(attempt)
    unrelated_attempt_event = attempt["attempt"].model_copy(deep=True)
    unrelated_attempt_event.payload["yield_evidence_id"] = "unrelated-yield"
    unrelated_attempt["attempt"] = unrelated_attempt_event

    return {
        ("carriage", "representation_result"): {
            "exact": _representation_carriage_witness(representation),
            "edge_missing": _representation_carriage_witness(
                missing_representation_carriage
            ),
            "wrong_occurrence": _representation_carriage_witness(
                wrong_representation_carriage
            ),
            "corrupted_evidence": _representation_carriage_witness(
                corrupted_representation_carriage
            ),
            "unrelated_change": _representation_carriage_witness(
                unrelated_representation_carriage
            ),
        },
        ("yield", "representation_result"): {
            "exact": _occurrence_result_witness(representation),
            "edge_missing": _occurrence_result_witness(
                missing_representation_yield
            ),
            "wrong_occurrence": _occurrence_result_witness(
                wrong_representation_yield
            ),
            "corrupted_evidence": _occurrence_result_witness(
                corrupted_representation_yield
            ),
            "unrelated_change": _occurrence_result_witness(
                unrelated_representation_yield
            ),
        },
        ("carriage", "emission_attempt"): {
            "exact": _emission_attempt_carriage_witness(attempt),
            "edge_missing": _emission_attempt_carriage_witness(missing_attempt),
            "wrong_occurrence": _emission_attempt_carriage_witness(wrong_attempt),
            "corrupted_evidence": _emission_attempt_carriage_witness(
                corrupted_attempt
            ),
            "unrelated_change": _emission_attempt_carriage_witness(
                unrelated_attempt
            ),
        },
    }


def _live_structural_edge_fidelity_cases() -> dict[
    tuple[str, str], dict[str, str]
]:
    registered = {
        (edge, "byte_measurement"): cases
        for edge, cases in _structural_edge_fidelity_cases().items()
    }
    registered.update(
        {
            (edge, "successful_emission"): cases
            for edge, cases in _emission_structural_edge_fidelity_cases().items()
        }
    )
    registered.update(_additional_live_structural_edge_fidelity_cases())
    registered.update(
        {
            ("yield", boundary): {
                case: _occurrence_result_witness(bundle)
                for case, bundle in cases.items()
            }
            for boundary, cases in _byte_pair_yield_requirement_bundles().items()
        }
    )
    return registered


def _structural_edge_implementation_specs() -> dict[str, dict]:
    requirements = {
        "exact_relation": "edge_missing",
        "occurrence_witness": "wrong_occurrence",
        "intact_evidence": "corrupted_evidence",
    }
    return {
        "carriage": {
            "from": "content",
            "to": "occurrence",
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
            "requires": requirements,
        },
    }


def _assert_structural_edge_anatomy(grammar: dict, specs: dict[str, dict]) -> None:
    assert set(specs) == set(grammar["structural_edges"])
    relation_families = grammar["implementation_witness"]["relation_audit"][
        "families"
    ]
    for edge, declared in grammar["structural_edges"].items():
        witnessed = specs[edge]
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
        assert declared["requires"] == relation_families[edge]


def _act_occurrence_witness(bundle: dict) -> dict[str, str]:
    carrier = bundle["carrier"]
    act_evidence = bundle["act_evidence"]
    joined = (
        act_evidence is not None
        and carrier.payload["target_act_id"]
        == act_evidence.payload["target_act_id"]
        and carrier.payload["act_occurrence_id"]
        == act_evidence.payload["act_occurrence_id"]
        and carrier.payload["responsibility"]
        == act_evidence.payload["responsibility"]
        and carrier.payload["responsible_boundary"]
        == act_evidence.payload["responsible_boundary"]
    )
    assignment = carrier.payload["responsibility_assignment_evidence"]
    return {
        "Responsibility": EXACT if joined else MISSING,
        "responsible_boundary": EXACT if joined else MISSING,
        "exact_Act": EXACT if joined else MISSING,
        "Act_occurrence": EXACT if joined else MISSING,
        "occurrence_Evidence": (
            EXACT
            if joined
            and carrier.payload["responsible_act_evidence_id"] == act_evidence.id
            else MISSING
        ),
        "Authority": (
            EXACT if joined and act_evidence.payload.get("authority") else MISSING
        ),
        "Scope": (
            EXACT
            if assignment.get("workspace_id") == carrier.workspace_id
            and assignment.get("completeness_boundary")
            else MISSING
        ),
        "limits": (
            EXACT if carrier.payload["dimensions"].get("authority") else MISSING
        ),
    }


def _movement_witness(bundle: dict) -> dict[str, str]:
    ledger = bundle["ledger"]
    movement = bundle["movement"]
    act_evidence = bundle["movement_act_evidence"]
    moved = _validate_moved_byte_assertion(ledger, movement.id)
    source = moved.reference if moved is not None else None
    source_event = ledger.get(source["recorded_occurrence_id"]) if source else None
    occurrence_edge = (
        act_evidence is not None
        and movement.payload["movement_act_occurrence_id"]
        == act_evidence.payload["movement_act_occurrence_id"]
    )
    movement_act_edge = (
        act_evidence is not None
        and movement.payload["movement_act_id"]
        == act_evidence.payload["movement_act_id"]
    )
    return {
        "workspace": (
            EXACT if movement.workspace_id == source_event.workspace_id else MISSING
        ),
        "source_Assertion_reference": (
            EXACT if movement.payload["source_assertion_ref"] == source else MISSING
        ),
        "source_locality": (
            EXACT if movement.payload["source_locality"] == source_event.session_id else MISSING
        ),
        "destination_locality": (
            EXACT if movement.payload["target_locality"] == movement.session_id else MISSING
        ),
        "movement_Act": (
            EXACT if movement_act_edge else MISSING
        ),
        "movement_occurrence": EXACT if occurrence_edge else MISSING,
        "movement_Evidence": (
            EXACT
            if act_evidence is not None
            and movement.payload["movement_act_evidence_event_id"] == act_evidence.id
            else MISSING
        ),
        "movement_Authority": (
            EXACT if movement.payload.get("authority") else MISSING
        ),
        "Assertion_identity": (
            EXACT if movement.payload["assertion_id"] == moved.assertion_id else MISSING
        ),
        "original_occurrence": (
            EXACT
            if moved.recorded_occurrence_id == source["recorded_occurrence_id"]
            else MISSING
        ),
        "Assertion_Evidence": (
            EXACT
            if "Evidence" in movement.payload["surviving_coordinates"]
            else MISSING
        ),
        "Assertion_Authority": (
            EXACT
            if "Authority" in movement.payload["surviving_coordinates"]
            else MISSING
        ),
        **{
            coordinate: (
                EXACT
                if coordinate in movement.payload["surviving_coordinates"]
                else MISSING
            )
            for coordinate in ("Standing", "Scope", "Unknowns", "limits")
        },
    }


def _participation_witness(bundle: dict, *, role: str) -> str:
    requirements = _participation_requirements(bundle, role=role)
    return EXACT if all(requirements.values()) else MISSING


def _participation_requirements(bundle: dict, *, role: str) -> dict[str, bool]:
    applicability = bundle["applicability"]
    pair = bundle["pair_carrier"]
    act_evidence = bundle["pair_act_evidence"]
    if act_evidence is None:
        return {
            "exact_relation": False,
            "occurrence_witness": False,
            "intact_evidence": False,
        }
    exact_subject = (
        applicability["input_assertion_ref"]
        == pair.payload["source_assertion_ref"]
        == act_evidence.payload["input_assertion_ref"]
    )
    exact_role = (
        role
        == applicability["input_role"]
        == pair.payload["input_role"]
        == act_evidence.payload["input_role"]
    )
    exact_occurrence = (
        pair.payload["act_occurrence_id"]
        == act_evidence.payload["act_occurrence_id"]
    )
    applicable_to_act = (
        applicability["dimensions"]["standing"] == "applicable"
        and applicability["target_act_id"] == pair.payload["target_act_id"]
        and applicability["dimensions"]["identity"]
        == act_evidence.payload["input_applicability_identity"]
    )
    return {
        "exact_relation": exact_subject and exact_role and applicable_to_act,
        "occurrence_witness": exact_occurrence,
        "intact_evidence": (
            bundle["ledger"].integrity_of(act_evidence.id) != CORRUPTED
        ),
    }


def test_implementation_witness_discriminates_content_carriage_and_digest():
    grammar = _witness_grammar()
    ledger = EventLedger()
    content = {"a": 1, "b": 2}

    first = ledger.append("test.carriage", "w", dict(content), session_id="s")
    second = ledger.append("test.carriage", "w", dict(content), session_id="s")
    assert first.payload == second.payload
    assert first.id != second.id
    assert yield_commitment("test", first.payload) == yield_commitment(
        "test", second.payload
    )

    first_json = '{"a":1,"b":2}'
    second_json = '{\n  "b": 2,\n  "a": 1\n}'
    assert first_json != second_json
    assert json.loads(first_json) == json.loads(second_json)
    assert yield_commitment(
        "test", json.loads(first_json)
    ) == yield_commitment("test", json.loads(second_json))

    changed_content = {"a": 1, "b": 3}
    assert yield_commitment("test", content) != yield_commitment(
        "test", changed_content
    )

    assert grammar["discriminators"] == ["content", "carriage", "digest"]
    assert grammar["non_equivalence"] == [
        ["content", "carriage"],
        ["content", "digest"],
        ["carriage", "digest"],
    ]


def test_fidelity_is_this_seeds_bounded_machine_comparison():
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))

    assert grammar["fidelity"] == {
        "book_clause": "01.Source.C",
        "subject": "this_Seed",
        "expectation": "machine_grammar",
        "comparison": "deterministic_tests",
        "witness": "live_implementation",
        "result": "bounded_Fidelity_finding",
        "does_not_establish": "global_certification",
    }


def test_every_structural_edge_has_live_fidelity_cases():
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))
    cases = _structural_edge_fidelity_cases()
    specs = _structural_edge_implementation_specs()
    expected = grammar["implementation_witness"]["fidelity_cases"]

    _assert_structural_edge_anatomy(grammar, specs)
    assert set(cases) == set(grammar["structural_edges"])
    assert all(set(edge_cases) == set(expected) for edge_cases in cases.values())
    assert cases == {
        edge: expected for edge in grammar["structural_edges"]
    }
    for edge, spec in specs.items():
        for adversary in spec["requires"].values():
            assert cases[edge][adversary] == MISSING


def test_emission_instantiates_every_structural_edge_at_its_boundary():
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))
    cases = _emission_structural_edge_fidelity_cases()
    expected = grammar["implementation_witness"]["fidelity_cases"]

    assert set(cases) == set(grammar["structural_edges"])
    assert cases == {edge: expected for edge in grammar["structural_edges"]}


def test_every_registered_live_edge_instantiation_obeys_the_full_fidelity_matrix():
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))
    expected = grammar["implementation_witness"]["fidelity_cases"]
    registered = _live_structural_edge_fidelity_cases()

    assert registered
    assert {edge for edge, _boundary in registered} == set(
        grammar["structural_edges"]
    )
    assert all(cases == expected for cases in registered.values())
    assert ("carriage", "representation_result") in registered
    assert ("carriage", "emission_attempt") in registered


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
            declared.append(boundary.value)

    assert len(declared) == len(set(declared))
    assert set(declared) == set(YIELD_LIVE_BOUNDARIES)


def test_byte_pair_yield_adversaries_change_one_requirement_each():
    expected = {
        "exact": (True, True, True),
        "edge_missing": (False, True, True),
        "wrong_occurrence": (True, False, True),
        "corrupted_evidence": (True, True, False),
        "unrelated_change": (True, True, True),
    }
    boundaries = _byte_pair_yield_requirement_bundles()

    assert {
        boundary: {
            case: tuple(_occurrence_result_requirements(bundle).values())
            for case, bundle in cases.items()
        }
        for boundary, cases in boundaries.items()
    } == {boundary: expected for boundary in boundaries}


def test_emission_attempt_carriage_adversaries_change_one_requirement_each():
    exact, alternate = _repeated_emission_attempt_road()
    wrong_occurrence = dict(exact)
    wrong_occurrence["attempt_carriage_evidence"] = alternate[
        "attempt_carriage_evidence"
    ]

    missing_relation = dict(exact)
    changed = dict(exact["attempt_carriage_evidence"].payload)
    changed["carried_content"] = "different carried content"
    missing_relation["attempt_carriage_evidence"] = exact["ledger"].append(
        exact["attempt_carriage_evidence"].kind,
        "w",
        changed,
        session_id="repeated-emission-attempt",
    )

    corrupted, _ = _repeated_emission_attempt_road()
    corrupted["ledger"].mark_corrupted(
        corrupted["attempt_carriage_evidence"].id
    )

    unrelated = dict(exact)
    unrelated_attempt = exact["attempt"].model_copy(deep=True)
    unrelated_attempt.payload["yield_evidence_id"] = "unrelated-yield"
    unrelated["attempt"] = unrelated_attempt

    assert _emission_attempt_carriage_requirements(exact) == {
        "exact_relation": True,
        "occurrence_witness": True,
        "intact_evidence": True,
    }
    assert _emission_attempt_carriage_requirements(missing_relation) == {
        "exact_relation": False,
        "occurrence_witness": True,
        "intact_evidence": True,
    }
    assert _emission_attempt_carriage_requirements(wrong_occurrence) == {
        "exact_relation": True,
        "occurrence_witness": False,
        "intact_evidence": True,
    }
    assert _emission_attempt_carriage_requirements(corrupted) == {
        "exact_relation": True,
        "occurrence_witness": True,
        "intact_evidence": False,
    }
    assert _emission_attempt_carriage_requirements(unrelated) == {
        "exact_relation": True,
        "occurrence_witness": True,
        "intact_evidence": True,
    }


def test_successful_emission_adversaries_change_one_requirement_each():
    bundles = _successful_emission_requirement_bundles()
    requirement_witnesses = {
        "carriage": _emission_carriage_requirements,
        "participation": _emission_participation_requirements,
        "yield": _occurrence_result_requirements,
    }
    expected = {
        "exact": {
            "exact_relation": True,
            "occurrence_witness": True,
            "intact_evidence": True,
        },
        "edge_missing": {
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
        "unrelated_change": {
            "exact_relation": True,
            "occurrence_witness": True,
            "intact_evidence": True,
        },
    }

    assert {
        edge: {
            case: requirement_witnesses[edge](bundle)
            for case, bundle in cases.items()
        }
        for edge, cases in bundles.items()
    } == {edge: expected for edge in bundles}


def test_representation_result_adversaries_change_one_requirement_each():
    exact, alternate = _repeated_representation_road()

    missing_carriage = dict(exact)
    missing_carriage_evidence = exact["carriage_evidence"].model_copy(deep=True)
    missing_carriage_evidence.payload["carried_content"][
        "representation_result"
    ] = "different result"
    missing_carriage["carriage_evidence"] = missing_carriage_evidence
    wrong_carriage = dict(exact)
    wrong_carriage_evidence = exact["carriage_evidence"].model_copy(deep=True)
    wrong_carriage_evidence.payload["act_occurrence_id"] = alternate[
        "carrier"
    ].payload["act_occurrence_id"]
    wrong_carriage["carriage_evidence"] = wrong_carriage_evidence
    corrupted_carriage = _representation_road()
    corrupted_carriage["ledger"].mark_corrupted(
        corrupted_carriage["carriage_evidence"].id
    )
    unrelated_carriage = dict(exact)
    unrelated_carrier = exact["carrier"].model_copy(deep=True)
    unrelated_carrier.payload["yield_evidence_id"] = "different-yield-evidence"
    unrelated_carriage["carrier"] = unrelated_carrier

    missing_yield = dict(exact)
    missing_yield_carrier = exact["carrier"].model_copy(deep=True)
    missing_yield_carrier.payload["representation_result"] = "different result"
    missing_yield["carrier"] = missing_yield_carrier
    wrong_yield = dict(exact)
    wrong_act_evidence = exact["act_evidence"].model_copy(deep=True)
    wrong_content_evidence = exact["content_evidence"].model_copy(deep=True)
    alternate_occurrence = alternate["carrier"].payload["act_occurrence_id"]
    wrong_act_evidence.payload["act_occurrence_id"] = alternate_occurrence
    wrong_content_evidence.payload["dimensions"]["act_occurrence_id"] = (
        alternate_occurrence
    )
    wrong_yield["act_evidence"] = wrong_act_evidence
    wrong_yield["content_evidence"] = wrong_content_evidence
    corrupted_yield = _representation_road()
    corrupted_yield["ledger"].mark_corrupted(
        corrupted_yield["content_evidence"].id
    )
    unrelated_yield = dict(exact)
    unrelated_yield_carrier = exact["carrier"].model_copy(deep=True)
    unrelated_yield_carrier.payload["carriage_evidence_id"] = "different-carriage"
    unrelated_yield["carrier"] = unrelated_yield_carrier

    expected = {
        "exact": (True, True, True),
        "edge_missing": (False, True, True),
        "wrong_occurrence": (True, False, True),
        "corrupted_evidence": (True, True, False),
        "unrelated_change": (True, True, True),
    }
    bundles = {
        "carriage": {
            "exact": exact,
            "edge_missing": missing_carriage,
            "wrong_occurrence": wrong_carriage,
            "corrupted_evidence": corrupted_carriage,
            "unrelated_change": unrelated_carriage,
        },
        "yield": {
            "exact": exact,
            "edge_missing": missing_yield,
            "wrong_occurrence": wrong_yield,
            "corrupted_evidence": corrupted_yield,
            "unrelated_change": unrelated_yield,
        },
    }
    witnesses = {
        "carriage": _representation_carriage_requirements,
        "yield": _occurrence_result_requirements,
    }

    assert {
        edge: {
            case: tuple(witnesses[edge](bundle).values())
            for case, bundle in cases.items()
        }
        for edge, cases in bundles.items()
    } == {edge: expected for edge in bundles}


def test_byte_measurement_adversaries_change_one_requirement_each():
    carriage = _byte_measurement_road()
    alternate_carriage = _byte_measurement_road()
    missing_carriage = dict(carriage)
    missing_carrier = carriage["carrier"].model_copy(deep=True)
    missing_carrier.payload["assertions"] = []
    missing_carriage["carrier"] = missing_carrier
    corrupted_carriage = _byte_measurement_road()
    corrupted_carriage["ledger"].mark_corrupted(corrupted_carriage["carrier"].id)
    unrelated_carriage = dict(carriage)
    unrelated_carrier = carriage["carrier"].model_copy(deep=True)
    unrelated_carrier.payload["yield_evidence_id"] = "different-yield-evidence"
    unrelated_carriage["carrier"] = unrelated_carrier

    participation = _recorded_applicability()
    alternate_participation = _recorded_applicability()
    missing_participation = dict(participation)
    missing_participation_evidence = participation[
        "pair_act_evidence"
    ].model_copy(deep=True)
    missing_participation_evidence.payload["input_role"] = "different-role"
    missing_participation["pair_act_evidence"] = missing_participation_evidence
    wrong_participation = dict(participation)
    wrong_participation_evidence = participation[
        "pair_act_evidence"
    ].model_copy(deep=True)
    wrong_participation_evidence.payload["act_occurrence_id"] = (
        alternate_participation["pair_carrier"].payload["act_occurrence_id"]
    )
    wrong_participation["pair_act_evidence"] = wrong_participation_evidence
    corrupted_participation = _recorded_applicability()
    corrupted_participation["ledger"].mark_corrupted(
        corrupted_participation["pair_act_evidence"].id
    )
    unrelated_participation = dict(participation)
    unrelated_pair = participation["pair_carrier"].model_copy(deep=True)
    unrelated_pair.payload["yield_evidence_id"] = "different-yield-evidence"
    unrelated_participation["pair_carrier"] = unrelated_pair

    yielded = _byte_measurement_road()
    alternate_yield = _byte_measurement_road()
    missing_yield = dict(yielded)
    missing_yield_carrier = yielded["carrier"].model_copy(deep=True)
    missing_yield_carrier.payload["measurement_rule"] = "different-rule"
    missing_yield["carrier"] = missing_yield_carrier
    wrong_yield = dict(yielded)
    wrong_act_evidence = yielded["act_evidence"].model_copy(deep=True)
    wrong_content_evidence = yielded["content_evidence"].model_copy(deep=True)
    alternate_occurrence = alternate_yield["carrier"].payload["act_occurrence_id"]
    wrong_act_evidence.payload["act_occurrence_id"] = alternate_occurrence
    wrong_content_evidence.payload["dimensions"]["act_occurrence_id"] = (
        alternate_occurrence
    )
    wrong_yield["act_evidence"] = wrong_act_evidence
    wrong_yield["content_evidence"] = wrong_content_evidence
    corrupted_yield = _byte_measurement_road()
    corrupted_yield["ledger"].mark_corrupted(
        corrupted_yield["content_evidence"].id
    )
    unrelated_yield = dict(yielded)
    unrelated_yield_carrier = yielded["carrier"].model_copy(deep=True)
    unrelated_yield_carrier.payload["occurrence_preservation"] = "different"
    unrelated_yield["carrier"] = unrelated_yield_carrier

    expected = {
        "exact": (True, True, True),
        "edge_missing": (False, True, True),
        "wrong_occurrence": (True, False, True),
        "corrupted_evidence": (True, True, False),
        "unrelated_change": (True, True, True),
    }
    actual = {
        "carriage": {
            "exact": _assertion_carriage_requirements(
                carriage, occurrence_id=carriage["carrier"].id
            ),
            "edge_missing": _assertion_carriage_requirements(
                missing_carriage, occurrence_id=carriage["carrier"].id
            ),
            "wrong_occurrence": _assertion_carriage_requirements(
                carriage, occurrence_id=alternate_carriage["carrier"].id
            ),
            "corrupted_evidence": _assertion_carriage_requirements(
                corrupted_carriage,
                occurrence_id=corrupted_carriage["carrier"].id,
            ),
            "unrelated_change": _assertion_carriage_requirements(
                unrelated_carriage, occurrence_id=carriage["carrier"].id
            ),
        },
        "participation": {
            case: _participation_requirements(bundle, role=BYTE_PAIR_INPUT_ROLE)
            for case, bundle in {
                "exact": participation,
                "edge_missing": missing_participation,
                "wrong_occurrence": wrong_participation,
                "corrupted_evidence": corrupted_participation,
                "unrelated_change": unrelated_participation,
            }.items()
        },
        "yield": {
            case: _occurrence_result_requirements(bundle)
            for case, bundle in {
                "exact": yielded,
                "edge_missing": missing_yield,
                "wrong_occurrence": wrong_yield,
                "corrupted_evidence": corrupted_yield,
                "unrelated_change": unrelated_yield,
            }.items()
        },
    }

    assert {
        edge: {case: tuple(requirements.values()) for case, requirements in cases.items()}
        for edge, cases in actual.items()
    } == {edge: expected for edge in actual}


def test_attempt_and_success_have_distinct_carriages_for_the_same_text():
    emission = _emission_road()
    alternate = _emission_road()
    wrong_attempt = dict(emission)
    wrong_attempt["attempt_carriage_evidence"] = alternate[
        "attempt_carriage_evidence"
    ]
    success_evidence_in_attempt_slot = dict(emission)
    success_evidence_in_attempt_slot["attempt_carriage_evidence"] = emission[
        "carriage_evidence"
    ]

    assert emission["attempt"].payload["attempted_representation"] == emission[
        "carrier"
    ].payload["emitted_representation"]
    assert _emission_attempt_carriage_witness(emission) == EXACT
    assert _emission_attempt_carriage_witness(wrong_attempt) == MISSING
    assert (
        _emission_attempt_carriage_witness(success_evidence_in_attempt_slot)
        == MISSING
    )


def test_representation_act_has_an_exact_yield_edge_without_asserting_participation():
    representation = _representation_road()
    alternate = _representation_road()
    missing = dict(representation)
    missing["content_evidence"] = None
    wrong_occurrence = dict(representation)
    wrong_occurrence["content_evidence"] = alternate["content_evidence"]
    missing_carriage = dict(representation)
    missing_carriage["carriage_evidence"] = None
    wrong_carriage = dict(representation)
    wrong_carriage["carriage_evidence"] = alternate["carriage_evidence"]

    assert _representation_carriage_witness(representation) == EXACT
    assert _representation_carriage_witness(missing_carriage) == MISSING
    assert _representation_carriage_witness(wrong_carriage) == MISSING
    assert _occurrence_result_witness(representation) == EXACT
    assert _occurrence_result_witness(missing) == MISSING
    assert _occurrence_result_witness(wrong_occurrence) == MISSING
    assert "input_role" not in representation["carrier"].payload


def test_changed_structural_edge_anatomy_is_detected():
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))
    grammar["structural_edges"]["yield"]["from"] = "result"

    try:
        _assert_structural_edge_anatomy(
            grammar, _structural_edge_implementation_specs()
        )
    except AssertionError:
        pass
    else:
        raise AssertionError("reversed Yield anatomy escaped implementation Fidelity")


def test_content_and_carriage_endpoints_do_not_establish_carriage_relation():
    ledger = EventLedger()
    content = {"subject": "x", "standing": "Unknown"}
    carriage = ledger.append("test.carriage", "w", dict(content), session_id="s")

    assert (
        _content_carriage_witness(
            content, carriage=carriage, occurrence_id=carriage.id
        )
        == EXACT
    )
    second_carriage = ledger.append(
        "test.carriage", "w", dict(content), session_id="s"
    )
    assert content
    assert second_carriage.payload == carriage.payload
    assert second_carriage.id != carriage.id
    assert (
        _content_carriage_witness(
            content,
            carriage=second_carriage,
            occurrence_id=carriage.id,
        )
        == MISSING
    )


def test_representation_and_digest_endpoints_do_not_establish_commitment_relation():
    representation = {"subject": "x", "standing": "Unknown"}
    digest = yield_commitment("test", representation)

    assert (
        _representation_digest_witness(
            representation, convention="test", digest=digest
        )
        == EXACT
    )
    changed_representation = {"subject": "x", "standing": "measured"}
    assert changed_representation
    assert digest
    assert (
        _representation_digest_witness(
            changed_representation, convention="test", digest=digest
        )
        == MISSING
    )


def test_digest_recomputation_is_not_a_recorded_digest_occurrence():
    bundle = _byte_measurement_road()
    evidence = bundle["content_evidence"]
    carrier = bundle["carrier"]
    represented = {
        coordinate: carrier.payload[coordinate]
        for coordinate in evidence.payload["yield_coordinates"]
    }
    digest = evidence.payload["yield_commitment"]
    convention = evidence.payload["yield_convention"]

    assert (
        _representation_digest_witness(
            represented, convention=convention, digest=digest
        )
        == EXACT
    )
    assert (
        _recorded_digest_witness(
            represented,
            convention=convention,
            digest=digest,
            digest_carriage=evidence,
            digest_occurrence_id=evidence.id,
        )
        == EXACT
    )
    other_carriage = bundle["act_evidence"]
    assert (
        _recorded_digest_witness(
            represented,
            convention=convention,
            digest=digest,
            digest_carriage=other_carriage,
            digest_occurrence_id=evidence.id,
        )
        == MISSING
    )


def test_a_digest_alone_witnesses_no_content_carriage_or_standing():
    grammar = _witness_grammar()
    digest = yield_commitment("test", {"a": 1})
    witness = _digest_only_witness(digest)

    assert witness == {
        "digest": EXACT,
        **{name: MISSING for name in grammar["digest_does_not_establish"]},
    }


def test_assertion_clause_is_checked_against_a_live_byte_assertion():
    clause = _clause("01.Standing.D.1")
    witness = _assertion_witness(_byte_measurement_road())

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


def test_asserted_content_identity_includes_scope_but_not_carriage():
    ledger = EventLedger()
    for session_id in ("source-one", "source-two"):
        run_persistent_operator_console(
            ledger=ledger,
            workspace_id="w",
            session_id=session_id,
            input_stream=StringIO("t\nexit\n"),
            output_stream=StringIO(),
        )

    first = record_byte_count_layer(
        ledger,
        workspace_id="w",
        source_session_ids=("source-one",),
        recording_session_id="measurement-one",
    )
    repeated = record_byte_count_layer(
        ledger,
        workspace_id="w",
        source_session_ids=("source-one",),
        recording_session_id="measurement-two",
    )
    other_scope = record_byte_count_layer(
        ledger,
        workspace_id="w",
        source_session_ids=("source-two",),
        recording_session_id="measurement-three",
    )

    def count_assertion(event):
        return next(
            assertion
            for assertion in event.payload["assertions"]
            if assertion["result"] == "count"
            and assertion["assertion_subject"].get("byte_hex") == "74"
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
    assert first.id != repeated.id
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
        "subject_taxonomy_closed": False,
        "preserves_subject_identity": True,
        "distinct_from": [
            "subject",
            "carriage",
            "Applicability",
            "Admission",
            "participation",
            "input_to_result_support",
        ],
    }
    assert applicability["input_role"] == BYTE_PAIR_INPUT_ROLE
    assert applicability["target_act_occurrence_id"] is None


def test_participation_requires_exact_subject_role_and_act_occurrence():
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))
    bundle = _recorded_applicability()

    assert grammar["structural_edges"]["participation"] == {
        "book_clause": "01.Standing.E.1",
        "from": "subject",
        "to": "Act_occurrence",
        "coordinate": "role",
        "requires": ["exact_relation", "occurrence_witness", "intact_evidence"],
    }
    assert _participation_witness(bundle, role=BYTE_PAIR_INPUT_ROLE) == EXACT
    assert _participation_witness(bundle, role="some other role") == MISSING

    assert bundle["applicability"]["dimensions"]["standing"] == "applicable"
    assert bundle["pair_carrier"].payload["act_occurrence_id"]
    bundle["pair_act_evidence"] = None
    assert _participation_witness(bundle, role=BYTE_PAIR_INPUT_ROLE) == MISSING


def test_unjoined_endpoints_do_not_witness_an_input_to_act_relation():
    grammar = _witness_grammar()
    bundle = _recorded_applicability()
    bundle["act_evidence"] = None
    witness = _applicability_witness(bundle)

    assert bundle["applicability"]["input_assertion_ref"]
    assert bundle["applicability"]["target_act_id"]
    assert bundle["applicability"]["applicability_act_occurrence_id"]
    assert grammar["relation_audit"] == {
        "endpoint_presence_establishes_relation": False,
        "families": {
            "carriage": ["exact_relation", "occurrence_witness", "intact_evidence"],
            "candidate_participation": ["exact_relation", "occurrence_witness"],
            "participation": ["exact_relation", "occurrence_witness", "intact_evidence"],
            "yield": ["exact_relation", "occurrence_witness", "intact_evidence"],
            "representation_mechanically_matches_digest": [
                "mechanical_recomputation"
            ],
            "representation_digest_carried_by_occurrence": [
                "exact_relation",
                "occurrence_witness",
            ],
        },
    }
    assert witness["input_identity"] == MISSING
    assert witness["exact_Act"] == MISSING
    assert witness["occurrence_identity"] == MISSING


def test_locality_movement_clause_is_checked_against_the_live_pair_road():
    clause = _clause("06.Standing.B")
    bundle = _recorded_applicability()
    witness = _movement_witness(bundle)
    expected_coordinates = {
        *clause["responsibility"]["coordinates"],
        *clause["preserves"],
    }

    assert set(witness) == expected_coordinates
    assert set(witness.values()) == {EXACT}
    movement = bundle["movement"]
    assert "dimensions" not in movement.payload
    assert movement.workspace_id == bundle["ledger"].get(
        movement.payload["source_assertion_ref"]["recorded_occurrence_id"]
    ).workspace_id
    assert clause["result"] == "availability_at_destination_locality"


def test_movement_endpoints_do_not_replace_movement_occurrence_evidence():
    bundle = _recorded_applicability()
    movement = bundle["movement"]
    assert movement.payload["source_assertion_ref"]
    assert movement.payload["target_locality"]
    bundle["movement_act_evidence"] = None
    witness = _movement_witness(bundle)

    assert witness["source_Assertion_reference"] == EXACT
    assert witness["destination_locality"] == EXACT
    assert witness["movement_Act"] == MISSING
    assert witness["movement_occurrence"] == MISSING
    assert witness["movement_Evidence"] == MISSING


def test_occurrence_and_result_endpoints_do_not_establish_their_relation():
    bundle = _byte_measurement_road()
    assert _occurrence_result_witness(bundle) == EXACT

    carrier = bundle["carrier"]
    assert carrier.payload["act_occurrence_id"]
    assert carrier.payload["assertions"]
    bundle["content_evidence"] = None
    assert _occurrence_result_witness(bundle) == MISSING


def test_exact_act_clause_is_checked_against_live_byte_measurement():
    clause = _clause("02.Acts.A")
    bundle = _byte_measurement_road()
    witness = _act_occurrence_witness(bundle)

    assert set(witness) == set(clause["responsibility"]["coordinates"])
    assert set(witness.values()) == {EXACT}
    assert bundle["carrier"].payload["target_act_id"] != bundle["carrier"].payload[
        "act_occurrence_id"
    ]
    assert _occurrence_result_witness(bundle) == EXACT


def test_act_and_occurrence_ids_do_not_establish_their_relation():
    bundle = _byte_measurement_road()
    carrier = bundle["carrier"]
    assert carrier.payload["target_act_id"]
    assert carrier.payload["act_occurrence_id"]
    bundle["act_evidence"] = None
    witness = _act_occurrence_witness(bundle)

    assert witness["exact_Act"] == MISSING
    assert witness["Act_occurrence"] == MISSING
    assert witness["occurrence_Evidence"] == MISSING


def test_runtime_uses_yield_only_for_the_occurrence_to_result_edge():
    retired = re.compile(
        r"\b(?:produc(?:e(?:d|s)?|ing|tion\w*|er\w*)|reyield\w*)\b",
        re.IGNORECASE,
    )
    runtime_root = GRAMMAR.parents[1] / "seed_runtime"
    contaminated = {
        path.relative_to(GRAMMAR.parents[1]).as_posix(): [
            (line_number, line.rstrip())
            for line_number, line in enumerate(
                path.read_text(encoding="utf-8").splitlines(), start=1
            )
            if retired.search(line)
        ]
        for path in runtime_root.glob("*.py")
    }

    assert {path: hits for path, hits in contaminated.items() if hits} == {}


def test_runtime_has_no_formation_layer():
    retired = "forma" + "tion"
    runtime_root = GRAMMAR.parents[1] / "seed_runtime"
    contaminated = [
        path.relative_to(GRAMMAR.parents[1]).as_posix()
        for path in runtime_root.glob("*.py")
        if retired in path.read_text(encoding="utf-8").casefold()
    ]

    assert contaminated == []


def test_runtime_has_no_execution_layer():
    retired = re.compile(r"\bexecutions?\b|execution[-_]", re.IGNORECASE)
    runtime_root = GRAMMAR.parents[1] / "seed_runtime"
    contaminated = {
        path.relative_to(GRAMMAR.parents[1]).as_posix(): [
            (line_number, line.rstrip())
            for line_number, line in enumerate(
                path.read_text(encoding="utf-8").splitlines(), start=1
            )
            if retired.search(line)
        ]
        for path in runtime_root.glob("*.py")
    }

    assert {path: hits for path, hits in contaminated.items() if hits} == {}


def test_runtime_has_no_unsupported_coordinate_abstraction():
    retired = re.compile(
        r"\bin" + r"vent(?:s|ed|ing|ion|ions)?\b|in"
        + r"vent(?:s|ed|ing|ion|ions)?[-_]",
        re.IGNORECASE,
    )
    runtime_root = GRAMMAR.parents[1] / "seed_runtime"
    contaminated = {
        path.relative_to(GRAMMAR.parents[1]).as_posix(): [
            (line_number, line.rstrip())
            for line_number, line in enumerate(
                path.read_text(encoding="utf-8").splitlines(), start=1
            )
            if retired.search(line)
        ]
        for path in runtime_root.glob("*.py")
    }

    assert {path: hits for path, hits in contaminated.items() if hits} == {}


def test_runtime_has_no_inventory_abstraction():
    retired = re.compile(r"\binventor(?:y|ies)\b|inventory[-_]", re.IGNORECASE)
    runtime_root = GRAMMAR.parents[1] / "seed_runtime"
    contaminated = {
        path.relative_to(GRAMMAR.parents[1]).as_posix(): [
            (line_number, line.rstrip())
            for line_number, line in enumerate(
                path.read_text(encoding="utf-8").splitlines(), start=1
            )
            if retired.search(line)
        ]
        for path in runtime_root.glob("*.py")
    }

    assert {path: hits for path, hits in contaminated.items() if hits} == {}


def test_runtime_does_not_reuse_fidelity_as_a_result_kind():
    retired = re.compile(r"\bfidelity\w*\b|fidelity[-_]", re.IGNORECASE)
    runtime_root = GRAMMAR.parents[1] / "seed_runtime"
    contaminated = {
        path.relative_to(GRAMMAR.parents[1]).as_posix(): [
            (line_number, line.rstrip())
            for line_number, line in enumerate(
                path.read_text(encoding="utf-8").splitlines(), start=1
            )
            if retired.search(line)
        ]
        for path in runtime_root.glob("*.py")
    }

    assert {path: hits for path, hits in contaminated.items() if hits} == {}


def test_runtime_has_no_view_abstraction():
    retired = re.compile(r"\bviews?\b|view[-_]", re.IGNORECASE)
    runtime_root = GRAMMAR.parents[1] / "seed_runtime"
    contaminated = {
        path.relative_to(GRAMMAR.parents[1]).as_posix(): [
            (line_number, line.rstrip())
            for line_number, line in enumerate(
                path.read_text(encoding="utf-8").splitlines(), start=1
            )
            if retired.search(line)
        ]
        for path in runtime_root.glob("*.py")
    }

    assert {path: hits for path, hits in contaminated.items() if hits} == {}


def test_runtime_reserves_warrant_for_the_seed_standing_declaration():
    retired = re.compile(r"\bwarrant\w*\b|warrant[-_]", re.IGNORECASE)
    runtime_root = GRAMMAR.parents[1] / "seed_runtime"
    contaminated = {
        path.relative_to(GRAMMAR.parents[1]).as_posix(): [
            (line_number, line.rstrip())
            for line_number, line in enumerate(
                path.read_text(encoding="utf-8").splitlines(), start=1
            )
            if retired.search(line)
        ]
        for path in runtime_root.glob("*.py")
    }

    assert {path: hits for path, hits in contaminated.items() if hits} == {}


def test_runtime_has_no_examination_species():
    retired = re.compile(r"\bexaminations?\b|examination[-_]", re.IGNORECASE)
    runtime_root = GRAMMAR.parents[1] / "seed_runtime"
    contaminated = {
        path.relative_to(GRAMMAR.parents[1]).as_posix(): [
            (line_number, line.rstrip())
            for line_number, line in enumerate(
                path.read_text(encoding="utf-8").splitlines(), start=1
            )
            if retired.search(line)
        ]
        for path in runtime_root.glob("*.py")
    }

    assert {path: hits for path, hits in contaminated.items() if hits} == {}
