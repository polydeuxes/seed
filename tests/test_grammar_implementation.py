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
from seed_runtime.events import EventLedger
from seed_runtime.operator_console import run_persistent_operator_console
from seed_runtime.yield_evidence import yield_commitment


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
    content: dict, *, carriage, carriage_occurrence_id: str
) -> str:
    if carriage is None:
        return MISSING
    return (
        EXACT
        if carriage.id == carriage_occurrence_id and carriage.payload == content
        else MISSING
    )


def _assertion_carriage_witness(bundle: dict, *, carriage_occurrence_id: str) -> str:
    assertion = bundle["source_assertion"]
    carrier = bundle["carrier"]
    carried = [
        item
        for item in carrier.payload.get("assertions", [])
        if item.get("dimensions", {}).get("identity") == assertion.assertion_id
    ]
    exact_relation = carried == [assertion.payload]
    exact_occurrence = (
        carrier.id == carriage_occurrence_id
        == assertion.recorded_occurrence_id
    )
    return EXACT if exact_relation and exact_occurrence else MISSING


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
    digest_carriage_occurrence_id: str,
) -> str:
    if digest_carriage is None:
        return MISSING
    mechanically_matches = (
        yield_commitment(convention, representation) == digest
    )
    exact_carriage = (
        digest_carriage.id == digest_carriage_occurrence_id
        and digest_carriage.payload.get("yield_commitment") == digest
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
        "content_evidence": ledger.get(measurement.payload["yield_evidence_id"]),
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
    carrier = bundle["carrier"]
    act_evidence = bundle["act_evidence"]
    content_evidence = bundle["content_evidence"]
    if act_evidence is None or content_evidence is None:
        return MISSING
    same_occurrence = carrier.payload.get("act_occurrence_id") == (
        act_evidence.payload.get("act_occurrence_id")
    ) == content_evidence.payload.get("dimensions", {}).get("act_occurrence_id")
    same_result = act_evidence.payload.get("result_commitment") == (
        content_evidence.payload.get("yield_commitment")
    )
    evidence_is_carried = (
        carrier.payload.get("responsible_act_evidence_id") == act_evidence.id
        and carrier.payload.get("yield_evidence_id") == content_evidence.id
    )
    return EXACT if same_occurrence and same_result and evidence_is_carried else MISSING


def _structural_edge_fidelity_cases() -> dict[str, dict[str, str]]:
    carriage = _byte_measurement_road()
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
    unrelated_carrier.payload["unrelated_test_coordinate"] = "ignored"
    unrelated_carriage["carrier"] = unrelated_carrier

    participation = _recorded_applicability()
    missing_participation = dict(participation)
    missing_participation["pair_act_evidence"] = None
    wrong_participation = dict(participation)
    participation_evidence = participation["pair_act_evidence"]
    wrong_participation_evidence = participation_evidence.model_copy(deep=True)
    wrong_participation_evidence.payload["act_occurrence_id"] = (
        "another_pair_measurement_occurrence"
    )
    wrong_participation["pair_act_evidence"] = wrong_participation_evidence
    unrelated_participation = dict(participation)
    unrelated_participation_evidence = participation_evidence.model_copy(deep=True)
    unrelated_participation_evidence.payload["unrelated_test_coordinate"] = "ignored"
    unrelated_participation["pair_act_evidence"] = unrelated_participation_evidence

    yielded = _byte_measurement_road()
    missing_yield = dict(yielded)
    missing_yield["content_evidence"] = None
    wrong_yield = dict(yielded)
    yield_evidence = yielded["content_evidence"]
    wrong_yield_evidence = yield_evidence.model_copy(deep=True)
    wrong_yield_evidence.payload["dimensions"]["act_occurrence_id"] = (
        "another_byte_measurement_occurrence"
    )
    wrong_yield["content_evidence"] = wrong_yield_evidence
    unrelated_yield = dict(yielded)
    unrelated_yield_evidence = yield_evidence.model_copy(deep=True)
    unrelated_yield_evidence.payload["unrelated_test_coordinate"] = "ignored"
    unrelated_yield["content_evidence"] = unrelated_yield_evidence

    return {
        "carriage": {
            "exact": _assertion_carriage_witness(
                carriage,
                carriage_occurrence_id=carriage["carrier"].id,
            ),
            "edge_missing": _assertion_carriage_witness(
                missing_carriage,
                carriage_occurrence_id=carriage["carrier"].id,
            ),
            "wrong_occurrence": _assertion_carriage_witness(
                carriage,
                carriage_occurrence_id="another_byte_measurement_carriage",
            ),
            "unrelated_change": _assertion_carriage_witness(
                unrelated_carriage,
                carriage_occurrence_id=carriage["carrier"].id,
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
            "unrelated_change": _participation_witness(
                unrelated_participation, role=BYTE_PAIR_INPUT_ROLE
            ),
        },
        "yield": {
            "exact": _occurrence_result_witness(yielded),
            "edge_missing": _occurrence_result_witness(missing_yield),
            "wrong_occurrence": _occurrence_result_witness(wrong_yield),
            "unrelated_change": _occurrence_result_witness(unrelated_yield),
        },
    }


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
        "original_carriage_occurrence": (
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
    applicability = bundle["applicability"]
    pair = bundle["pair_carrier"]
    act_evidence = bundle["pair_act_evidence"]
    if act_evidence is None:
        return MISSING
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
    return (
        EXACT
        if exact_subject and exact_role and exact_occurrence and applicable_to_act
        else MISSING
    )


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


def test_every_structural_edge_has_live_fidelity_cases():
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))
    cases = _structural_edge_fidelity_cases()
    expected = grammar["implementation_witness"]["fidelity_cases"]

    assert set(cases) == set(grammar["structural_edges"])
    assert all(set(edge_cases) == set(expected) for edge_cases in cases.values())
    assert cases == {
        edge: expected for edge in grammar["structural_edges"]
    }


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
        "from": "subject",
        "to": "Act_occurrence",
        "coordinate": "role",
        "requires": ["exact_relation", "occurrence_witness"],
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
            "carriage": ["exact_relation", "occurrence_witness"],
            "candidate_participation": ["exact_relation", "occurrence_witness"],
            "participation": ["exact_relation", "occurrence_witness"],
            "yield": ["exact_relation", "occurrence_witness"],
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


def test_runtime_uses_yield_for_the_occurrence_to_result_edge():
    retired = re.compile(
        r"\bproduc(?:e(?:d|s)?|ing|tion\w*|er\w*)\b",
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
