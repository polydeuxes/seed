import json
from io import StringIO
from pathlib import Path

from seed_runtime.byte_measurement import (
    assertions_of_recorded_byte_measurement,
    get_recorded_pair_input_applicability,
    record_adjacent_byte_pair_count_layer,
    record_byte_count_layer,
)
from seed_runtime.events import EventLedger
from seed_runtime.operator_console import run_persistent_operator_console
from seed_runtime.production_evidence import production_commitment


GRAMMAR = Path(__file__).resolve().parents[1] / "book_of_seed/grammar.json"

EXACT = "exact"
INAPPLICABLE = "inapplicable"
UNKNOWN = "Unknown"
MISSING = "missing"
CONTRADICTION = "contradiction"


def _clause(clause_id: str) -> dict:
    return json.loads(GRAMMAR.read_text(encoding="utf-8"))["clauses"][clause_id]


def _witness_grammar() -> dict:
    return json.loads(GRAMMAR.read_text(encoding="utf-8"))["implementation_witness"]


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


def _source_assertion():
    road = _byte_measurement_road()
    return road["source_assertion"]


def _byte_measurement_road() -> dict:
    ledger = EventLedger()
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
        "content_evidence": ledger.get(measurement.payload["production_evidence_id"]),
    }


def _recorded_applicability() -> dict:
    # RecordedByteAssertion deliberately carries no ledger handle. Recreate the
    # live road so every relation can be checked through its own occurrences.
    ledger = EventLedger()
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
    return {
        "applicability": recovered,
        "carrier": carrier,
        "act_evidence": ledger.get(carrier.payload["responsible_act_evidence_id"]),
        "content_evidence": ledger.get(carrier.payload["production_evidence_id"]),
    }


def _assertion_witness(assertion) -> dict[str, str]:
    payload = assertion.payload
    dimensions = payload["dimensions"]
    return {
        # Runtime identity commits to result, subject, Scope, and content.  The
        # grammar currently names asserted content alone.  The audit exposes
        # the disagreement; it does not choose which side should change.
        "identity": CONTRADICTION,
        # support_basis is not silently promoted into Evidence.
        "Evidence": MISSING,
        "provenance": EXACT if dimensions.get("source_provenance") else MISSING,
        "Scope": EXACT if payload.get("assertion_scope") else MISSING,
        "Authority": EXACT if dimensions.get("authority") else MISSING,
        "conflicts": MISSING,
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
        and carrier.payload.get("production_evidence_id") == content_evidence.id
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
        "participants_and_roles": MISSING,
        "provenance": (
            EXACT
            if applicability["dimensions"].get("source_provenance")
            else MISSING
        ),
        "Standing": (
            EXACT if carried_result else MISSING
        ),
        # Applicability explicitly establishes no input-to-result support
        # relation, but the runtime carries no coordinate saying so.
        "support_relation_Standing": MISSING,
        "currentness": (
            INAPPLICABLE
            if treatment.get("currentness", {}).get("treatment")
            == "not required for this historical bounded population"
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
    carrier = bundle["carrier"]
    act_evidence = bundle["act_evidence"]
    content_evidence = bundle["content_evidence"]
    if act_evidence is None or content_evidence is None:
        return MISSING
    same_occurrence = carrier.payload.get("act_occurrence_id") == (
        act_evidence.payload.get("act_occurrence_id")
    )
    same_result = act_evidence.payload.get("result_commitment") == (
        content_evidence.payload.get("production_commitment")
    )
    evidence_is_carried = (
        carrier.payload.get("responsible_act_evidence_id") == act_evidence.id
        and carrier.payload.get("production_evidence_id") == content_evidence.id
    )
    return EXACT if same_occurrence and same_result and evidence_is_carried else MISSING


def test_implementation_witness_discriminates_content_carriage_and_digest():
    grammar = _witness_grammar()
    ledger = EventLedger()
    content = {"a": 1, "b": 2}

    first = ledger.append("test.carriage", "w", dict(content), session_id="s")
    second = ledger.append("test.carriage", "w", dict(content), session_id="s")
    assert first.payload == second.payload
    assert first.id != second.id
    assert production_commitment("test", first.payload) == production_commitment(
        "test", second.payload
    )

    first_json = '{"a":1,"b":2}'
    second_json = '{\n  "b": 2,\n  "a": 1\n}'
    assert first_json != second_json
    assert json.loads(first_json) == json.loads(second_json)
    assert production_commitment(
        "test", json.loads(first_json)
    ) == production_commitment("test", json.loads(second_json))

    changed_content = {"a": 1, "b": 3}
    assert production_commitment("test", content) != production_commitment(
        "test", changed_content
    )

    assert grammar["discriminators"] == ["content", "carriage", "digest"]
    assert grammar["non_equivalence"] == [
        ["content", "carriage"],
        ["content", "digest"],
        ["carriage", "digest"],
    ]


def test_a_digest_alone_witnesses_no_content_carriage_or_standing():
    grammar = _witness_grammar()
    digest = production_commitment("test", {"a": 1})
    witness = _digest_only_witness(digest)

    assert witness == {
        "digest": EXACT,
        **{name: MISSING for name in grammar["digest_does_not_establish"]},
    }


def test_assertion_clause_is_checked_against_a_live_byte_assertion():
    clause = _clause("01.Standing.D.1")
    witness = _assertion_witness(_source_assertion())

    assert set(witness) == {"identity", *clause["responsibility"]["coordinates"]}
    assert witness == {
        "identity": CONTRADICTION,
        "Evidence": MISSING,
        "provenance": EXACT,
        "Scope": EXACT,
        "Authority": EXACT,
        "conflicts": MISSING,
        "limits": EXACT,
        "Unknowns": EXACT,
        "Standing": EXACT,
    }


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
        "participants_and_roles": MISSING,
        "provenance": EXACT,
        "Standing": EXACT,
        "support_relation_Standing": MISSING,
        "currentness": INAPPLICABLE,
        "occurrence_identity": EXACT,
        "known_loss": UNKNOWN,
        "conflicts": EXACT,
        "Unknowns": EXACT,
        "negative_Authority": EXACT,
    }


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
        "requires": ["exact_relation", "occurrence_witness"],
        "families": [
            "content_to_carriage",
            "input_to_Act",
            "Act_occurrence_to_result",
            "representation_to_digest",
        ],
    }
    assert witness["input_identity"] == MISSING
    assert witness["exact_Act"] == MISSING
    assert witness["occurrence_identity"] == MISSING


def test_occurrence_and_result_endpoints_do_not_establish_their_relation():
    bundle = _byte_measurement_road()
    assert _occurrence_result_witness(bundle) == EXACT

    carrier = bundle["carrier"]
    assert carrier.payload["act_occurrence_id"]
    assert carrier.payload["assertions"]
    bundle["content_evidence"] = None
    assert _occurrence_result_witness(bundle) == MISSING
