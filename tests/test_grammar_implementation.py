import json
from io import StringIO
from pathlib import Path

from seed_runtime.byte_measurement import (
    _identity,
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


def _content_carriage_witness(
    content: dict, *, carriage, carriage_occurrence_id: str
) -> str:
    if carriage is None:
        return MISSING
    return (
        EXACT
        if carriage.id == carriage_occurrence_id and carriage.payload == content
        else MISSING
    )


def _representation_digest_witness(
    representation: dict, *, convention: str, digest: str
) -> str:
    return (
        EXACT
        if production_commitment(convention, representation) == digest
        else MISSING
    )


def _recorded_digest_witness(
    representation: dict,
    *,
    convention: str,
    digest: str,
    digest_carriage,
    digest_carriage_occurrence_id: str,
) -> str:
    if digest_carriage is None:
        return MISSING
    mechanically_matches = (
        production_commitment(convention, representation) == digest
    )
    exact_carriage = (
        digest_carriage.id == digest_carriage_occurrence_id
        and digest_carriage.payload.get("production_commitment") == digest
    )
    return EXACT if mechanically_matches and exact_carriage else MISSING


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
        and carrier.payload.get("production_evidence_id") == content_evidence.id
        and "assertions" in content_evidence.payload.get("production_coordinates", [])
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
        # The relation endpoints already identify the exact input role and the
        # exact addressed-Act role; no extra participant noun is invented.
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


def test_content_and_carriage_endpoints_do_not_establish_carriage_relation():
    ledger = EventLedger()
    content = {"subject": "x", "standing": "Unknown"}
    carriage = ledger.append("test.carriage", "w", dict(content), session_id="s")

    assert (
        _content_carriage_witness(
            content, carriage=carriage, carriage_occurrence_id=carriage.id
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
            carriage_occurrence_id=carriage.id,
        )
        == MISSING
    )


def test_representation_and_digest_endpoints_do_not_establish_commitment_relation():
    representation = {"subject": "x", "standing": "Unknown"}
    digest = production_commitment("test", representation)

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
        for coordinate in evidence.payload["production_coordinates"]
    }
    digest = evidence.payload["production_commitment"]
    convention = evidence.payload["production_convention"]

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
            digest_carriage_occurrence_id=evidence.id,
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
            digest_carriage_occurrence_id=evidence.id,
        )
        == MISSING
    )


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
            "content_to_carriage": ["exact_relation", "occurrence_witness"],
            "input_to_Act": ["exact_relation", "occurrence_witness"],
            "Act_occurrence_to_result": [
                "exact_relation",
                "occurrence_witness",
            ],
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


def test_occurrence_and_result_endpoints_do_not_establish_their_relation():
    bundle = _byte_measurement_road()
    assert _occurrence_result_witness(bundle) == EXACT

    carrier = bundle["carrier"]
    assert carrier.payload["act_occurrence_id"]
    assert carrier.payload["assertions"]
    bundle["content_evidence"] = None
    assert _occurrence_result_witness(bundle) == MISSING
