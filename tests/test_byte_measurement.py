from io import StringIO
import hashlib
import json

import pytest

from seed_runtime.byte_measurement import (
    BYTE_PAIR_MEASUREMENT_RECORDED_KIND,
    BYTE_PAIR_APPLICABILITY_RECORDED_KIND,
    BYTE_PAIR_MEASUREMENT_CONVENTION,
    BYTE_PAIR_RESULT_COORDINATES,
    BYTE_MEASUREMENT_RECORDED_KIND,
    BYTE_MEASUREMENT_CONVENTION,
    BYTE_RESULT_COORDINATES,
    BYTE_MEASUREMENT_RULE,
    ByteMeasurementError,
    RESPONSIBILITY_UNRECOVERED,
    SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY,
    _measure_byte_counts_through,
    _identity,
    _pair_input_applicability,
    get_recorded_pair_input_applicability,
    assertions_of_recorded_byte_measurement,
    assertions_of_recorded_adjacent_byte_pair_measurement,
    input_applicability_of_recorded_adjacent_byte_pair_measurement,
    measure_byte_counts,
    record_byte_count_layer,
    record_adjacent_byte_pair_count_layer,
)
from seed_runtime.events import EventLedger
from seed_runtime.event import Event
from seed_runtime.operator_console import run_persistent_operator_console
from seed_runtime.production_evidence import (
    PRODUCTION_EVIDENCE_KIND,
    production_commitment,
)


def _ledger(text="猫\n狗\n"):
    ledger = EventLedger()
    run_persistent_operator_console(
        ledger=ledger,
        workspace_id="w",
        session_id="source",
        input_stream=StringIO(text + "exit\n"),
        output_stream=StringIO(),
    )
    return ledger


def _byte_source(ledger):
    return record_byte_count_layer(
        ledger,
        workspace_id="w",
        source_session_ids=("source",),
        recording_session_id="byte-measurement",
    )


def test_exact_bytes_supply_the_measured_subjects_without_whitespace():
    measured = measure_byte_counts(
        _ledger(), workspace_id="w", source_session_ids=("source",)
    )
    counts = {item.byte_hex: item for item in measured.counts}

    # UTF-8 猫 = e7 8c ab and 狗 = e7 8b 97.  No character boundary is used or
    # claimed; these are the exact bytes Seed captured.
    assert counts["e7"].total_count == 2
    assert counts["8c"].total_count == 1
    assert counts["ab"].total_count == 1
    assert counts["8b"].total_count == 1
    assert counts["97"].total_count == 1
    assert counts["0a"].total_count == 2
    assert all(item.occurrences_examined == 2 for item in measured.counts)


def test_the_complete_declared_sessions_supply_the_population():
    measured = measure_byte_counts(
        _ledger("a\nb\n"), workspace_id="w", source_session_ids=("source",)
    )
    assert len(measured.source_material) == 2
    assert all(
        set(item) == {"ingress_occurrence_id", "raw_material_event_id"}
        for item in measured.source_material
    )
    assert measured.completeness_boundary.commitment


def test_count_and_recurrence_are_distinct_results():
    event = record_byte_count_layer(
        _ledger("ab\n"),
        workspace_id="w",
        source_session_ids=("source",),
        recording_session_id="measurement",
    )
    by_byte = {}
    for assertion in event.payload["assertions"]:
        byte_hex = assertion["assertion_subject"].get("byte_hex")
        if byte_hex is not None:
            by_byte.setdefault(byte_hex, []).append(assertion)

    assert [item["result"] for item in by_byte["61"]] == ["count"]
    assert by_byte["61"][0]["dimensions"]["content"]["total_count"] == 1
    # The newline occurs once too. No positive singleton is called recurrence.
    assert [item["result"] for item in by_byte["0a"]] == ["count"]


def test_recurrence_exists_only_above_one():
    event = record_byte_count_layer(
        _ledger("aa\n"),
        workspace_id="w",
        source_session_ids=("source",),
        recording_session_id="measurement",
    )
    results = [
        item["result"]
        for item in event.payload["assertions"]
        if item["assertion_subject"].get("byte_hex") == "61"
    ]
    assert results == ["count", "recurrence"]


def test_the_rule_is_mechanics_not_an_unchecked_callable():
    event = record_byte_count_layer(
        _ledger("the cat\n"),
        workspace_id="w",
        source_session_ids=("source",),
        recording_session_id="measurement",
    )
    assert event.payload["measurement_rule"] == BYTE_MEASUREMENT_RULE
    assert event.kind == BYTE_MEASUREMENT_RECORDED_KIND
    assert "zebra" not in str(event.payload)


def test_recorded_results_replay_the_complete_bounded_source_read():
    ledger = _ledger("猫\n狗\n")
    event = record_byte_count_layer(
        ledger,
        workspace_id="w",
        source_session_ids=("source",),
        recording_session_id="measurement",
    )
    recovered = assertions_of_recorded_byte_measurement(ledger, event.id)
    assert recovered
    assert all(item.recorded_occurrence_id == event.id for item in recovered)
    evidence = ledger.get(event.payload["production_evidence_id"])
    assert evidence.kind == PRODUCTION_EVIDENCE_KIND
    assert event.payload["producer"] == RESPONSIBILITY_UNRECOVERED
    assert evidence.payload["dimensions"]["producer"] == RESPONSIBILITY_UNRECOVERED
    assert "occurrence_preservation" not in evidence.payload["production_coordinates"]

    count = next(
        item
        for item in recovered
        if item.byte_hex == "e7" and item.result == "count"
    )
    assert count.payload["dimensions"]["content"] == {
        "occurrences_examined": 2,
        "occurrences_carrying": 2,
        "total_count": 2,
    }
    assert count.payload["assertion_scope"] == {
        "workspace_id": "w",
        "source_session_ids": ["source"],
    }
    assert count.payload["dimensions"]["source_provenance"]
    assert count.payload["dimensions"]["authority_warrant"]
    assert count.payload["unknowns"]
    assert count.payload["forbidden_inferences"]
    assert count.support_assertion_refs == (
        {
            "recorded_occurrence_id": event.id,
            "assertion_id": event.payload["assertions"][0]["dimensions"]["identity"],
        },
    )

    detached_payload = count.payload
    detached_payload["dimensions"]["standing"] = "invented"
    assert count.payload["dimensions"]["standing"] == "measured"

    detached_refs = count.support_assertion_refs
    detached_refs[0]["assertion_id"] = "invented"
    assert count.support_assertion_refs[0]["assertion_id"] != "invented"

    # Recovery preserves exact durable JSON kinds. It does not protect the
    # result by transmuting lists to tuples or dicts to proxy objects.
    represented = Event(
        id="re-presented",
        kind="test.representation",
        workspace_id="w",
        payload=count.payload,
    )
    assert type(represented.payload) is dict
    assert type(represented.payload["assertion_scope"]["source_session_ids"]) is list


def test_a_self_consistent_truncated_source_claim_is_refused():
    ledger = _ledger("a\nb\n")
    event = record_byte_count_layer(
        ledger,
        workspace_id="w",
        source_session_ids=("source",),
        recording_session_id="measurement",
    )
    assertions = event.payload["assertions"]
    source = assertions[0]
    source["dimensions"]["content"]["source_material"] = source["dimensions"][
        "content"
    ]["source_material"][:1]
    evidence = ledger.get(event.payload["production_evidence_id"])
    evidence.payload["production_commitment"] = production_commitment(
        BYTE_MEASUREMENT_CONVENTION,
        {name: event.payload[name] for name in BYTE_RESULT_COORDINATES},
    )
    with pytest.raises(ByteMeasurementError, match="complete bounded source read"):
        assertions_of_recorded_byte_measurement(ledger, event.id)


def test_recording_occurrence_testimony_is_recovered_exactly():
    ledger = _ledger("a\n")
    event = record_byte_count_layer(
        ledger,
        workspace_id="w",
        source_session_ids=("source",),
        recording_session_id="measurement",
    )
    event.payload["occurrence_preservation"] = "something else"
    with pytest.raises(ByteMeasurementError, match="recording-occurrence testimony"):
        assertions_of_recorded_byte_measurement(ledger, event.id)


def test_raw_material_appended_after_the_boundary_cannot_enter_the_read():
    ledger = EventLedger()
    ingress = ledger.append(
        "operator.ingress.ingress_occurred",
        "w",
        {"raw_material_event_id": "not-yet-present"},
        session_id="source",
    )
    boundary = ledger.capture_boundary()
    raw = ledger.append(
        "operator.ingress.raw_material_captured",
        "w",
        {"exact_bytes_hex": "61", "byte_count": 1},
        session_id="source",
    )
    ingress.payload["raw_material_event_id"] = raw.id
    with pytest.raises(ByteMeasurementError, match="not intact raw material"):
        _measure_byte_counts_through(
            ledger,
            workspace_id="w",
            sessions=("source",),
            boundary=boundary,
        )


def test_a_missing_declared_session_is_refused():
    with pytest.raises(ByteMeasurementError, match="absent"):
        measure_byte_counts(
            _ledger(), workspace_id="w", source_session_ids=("missing",)
        )


def test_raw_material_must_match_its_exact_byte_coordinates():
    ledger = _ledger("a\n")
    ingress = next(
        ledger.iter_session_kind(
            "w", "source", "operator.ingress.ingress_occurred"
        )
    )
    raw = ledger.get(ingress.payload["raw_material_event_id"])
    raw.payload["exact_bytes_hex"] = "not hex"
    with pytest.raises(ByteMeasurementError, match="malformed"):
        measure_byte_counts(
            ledger, workspace_id="w", source_session_ids=("source",)
        )


def test_one_raw_occurrence_cannot_be_counted_through_two_ingress_references():
    ledger = _ledger("a\n")
    ingress = next(
        ledger.iter_session_kind(
            "w", "source", "operator.ingress.ingress_occurred"
        )
    )
    ledger.append(
        "operator.ingress.ingress_occurred",
        "w",
        {"raw_material_event_id": ingress.payload["raw_material_event_id"]},
        session_id="source",
    )

    with pytest.raises(ByteMeasurementError, match="cannot enter.*twice"):
        measure_byte_counts(
            ledger, workspace_id="w", source_session_ids=("source",)
        )


def test_every_overlapping_adjacent_byte_pair_is_measured():
    ledger = _ledger("tatatata\n")
    source = _byte_source(ledger)
    event = record_adjacent_byte_pair_count_layer(
        ledger,
        source_measurement_event_id=source.id,
        workspace_id="w",
        recording_session_id="measurement",
    )
    counts = {
        item["assertion_subject"]["pair_hex"]: item["dimensions"]["content"]
        for item in event.payload["assertions"]
        if item["result"] == "count"
    }

    assert counts["7461"]["total_count"] == 4  # ta
    assert counts["6174"]["total_count"] == 3  # at
    assert counts["610a"]["total_count"] == 1  # a + capture newline


def test_adjacent_pairs_never_cross_ingress_capture_boundaries():
    ledger = _ledger("a\nb\n")
    source = _byte_source(ledger)
    event = record_adjacent_byte_pair_count_layer(
        ledger,
        source_measurement_event_id=source.id,
        workspace_id="w",
        recording_session_id="measurement",
    )
    counts = {
        item["assertion_subject"]["pair_hex"]: item["dimensions"]["content"][
            "total_count"
        ]
        for item in event.payload["assertions"]
        if item["result"] == "count"
    }

    assert counts == {"610a": 1, "620a": 1}
    assert "0a62" not in counts


def test_adjacent_pair_measurement_remains_byte_not_character_based():
    ledger = _ledger("猫\n")
    source = _byte_source(ledger)
    event = record_adjacent_byte_pair_count_layer(
        ledger,
        source_measurement_event_id=source.id,
        workspace_id="w",
        recording_session_id="measurement",
    )
    counts = {
        item["assertion_subject"]["pair_hex"]
        for item in event.payload["assertions"]
        if item["result"] == "count"
    }

    # UTF-8 bytes e7 8c ab plus the captured newline. These are adjacent bytes,
    # not a claim that any pair is a character.
    assert counts == {"e78c", "8cab", "ab0a"}


def test_pair_count_and_recurrence_are_separate_results():
    ledger = _ledger("tatatata\n")
    source = _byte_source(ledger)
    event = record_adjacent_byte_pair_count_layer(
        ledger,
        source_measurement_event_id=source.id,
        workspace_id="w",
        recording_session_id="measurement",
    )
    assert event.kind == BYTE_PAIR_MEASUREMENT_RECORDED_KIND
    by_pair = {}
    for assertion in event.payload["assertions"]:
        pair_hex = assertion["assertion_subject"].get("pair_hex")
        if pair_hex is not None:
            by_pair.setdefault(pair_hex, []).append(assertion)

    assert [item["result"] for item in by_pair["7461"]] == ["count", "recurrence"]
    assert [item["result"] for item in by_pair["610a"]] == ["count"]
    assert by_pair["7461"][1]["support_basis"]["local_assertion_ids"] == [
        by_pair["7461"][0]["dimensions"]["identity"]
    ]
    assert by_pair["7461"][0]["support_basis"]["assertion_refs"] == [
        next(
            item.reference
            for item in assertions_of_recorded_byte_measurement(ledger, source.id)
            if item.result == "exact_source_material_set"
        )
    ]
    applicability = input_applicability_of_recorded_adjacent_byte_pair_measurement(
        ledger, event.id
    )
    assert applicability["dimensions"]["standing"] == "applicable"
    assert applicability["input_assertion_ref"] == event.payload["source_assertion_ref"]
    assert applicability["purpose"]
    assert applicability["target_act"] == "declared adjacent-byte-pair Measurement"
    assert applicability["consumer_context"] == {
        "workspace_id": "w",
        "measurement_session_id": "measurement",
    }
    assert applicability["input_unknowns"]
    assert applicability["input_limits"]
    assert applicability["conflicts"] == []


def test_recorded_pair_results_replay_the_complete_bounded_source_read():
    ledger = _ledger("tatatata\n")
    source = _byte_source(ledger)
    event = record_adjacent_byte_pair_count_layer(
        ledger,
        source_measurement_event_id=source.id,
        workspace_id="w",
        recording_session_id="measurement",
    )

    recovered = assertions_of_recorded_adjacent_byte_pair_measurement(
        ledger, event.id
    )
    assert recovered
    assert all(item.recorded_occurrence_id == event.id for item in recovered)
    assert {item.pair_hex for item in recovered if item.pair_hex} == {
        "7461",
        "6174",
        "610a",
    }
    count = next(item for item in recovered if item.pair_hex == "7461" and item.result == "count")
    detached = count.payload
    detached["dimensions"]["standing"] = "invented"
    assert count.payload["dimensions"]["standing"] == "measured"
    assert count.support_assertion_refs[0]["recorded_occurrence_id"] == source.id


def test_pair_recovery_refuses_a_self_consistent_truncated_result_population():
    ledger = _ledger("tatatata\n")
    source = _byte_source(ledger)
    event = record_adjacent_byte_pair_count_layer(
        ledger,
        source_measurement_event_id=source.id,
        workspace_id="w",
        recording_session_id="measurement",
    )
    event.payload["assertions"] = event.payload["assertions"][:-1]
    evidence = ledger.get(event.payload["production_evidence_id"])
    evidence.payload["production_commitment"] = production_commitment(
        BYTE_PAIR_MEASUREMENT_CONVENTION,
        {name: event.payload[name] for name in BYTE_PAIR_RESULT_COORDINATES},
    )
    act_evidence = ledger.get(event.payload["responsible_act_evidence_id"])
    act_evidence.payload["result_commitment"] = evidence.payload[
        "production_commitment"
    ]

    with pytest.raises(ByteMeasurementError, match="recurrence boundary"):
        assertions_of_recorded_adjacent_byte_pair_measurement(ledger, event.id)


def test_pair_recovery_does_not_perform_the_pair_measurement_again(monkeypatch):
    ledger = _ledger("tatatata\n")
    source = _byte_source(ledger)
    event = record_adjacent_byte_pair_count_layer(
        ledger,
        source_measurement_event_id=source.id,
        workspace_id="w",
        recording_session_id="measurement",
    )

    def forbidden(*args, **kwargs):
        raise AssertionError("recovery performed the pair Measurement again")

    monkeypatch.setattr(
        "seed_runtime.byte_measurement._measure_adjacent_byte_pair_counts_through",
        forbidden,
    )
    monkeypatch.setattr(
        "seed_runtime.byte_measurement._pair_input_applicability", forbidden
    )
    assert assertions_of_recorded_adjacent_byte_pair_measurement(ledger, event.id)


def test_pair_recovery_refuses_invented_input_applicability():
    ledger = _ledger("tatatata\n")
    source = _byte_source(ledger)
    event = record_adjacent_byte_pair_count_layer(
        ledger,
        source_measurement_event_id=source.id,
        workspace_id="w",
        recording_session_id="measurement",
    )
    event.payload["input_applicability"]["purpose"] = "some other use"
    evidence = ledger.get(event.payload["production_evidence_id"])
    evidence.payload["production_commitment"] = production_commitment(
        BYTE_PAIR_MEASUREMENT_CONVENTION,
        {name: event.payload[name] for name in BYTE_PAIR_RESULT_COORDINATES},
    )
    act_evidence = ledger.get(event.payload["responsible_act_evidence_id"])
    act_evidence.payload["result_commitment"] = evidence.payload[
        "production_commitment"
    ]

    with pytest.raises(ByteMeasurementError, match="historical input Applicability"):
        assertions_of_recorded_adjacent_byte_pair_measurement(ledger, event.id)


def test_zero_observed_pairs_is_a_lawful_recoverable_result():
    ledger = _ledger("\n")
    source = _byte_source(ledger)
    event = record_adjacent_byte_pair_count_layer(
        ledger,
        source_measurement_event_id=source.id,
        workspace_id="w",
        recording_session_id="measurement",
    )

    assert event.payload["assertions"] == []
    assert assertions_of_recorded_adjacent_byte_pair_measurement(ledger, event.id) == ()


def test_applicability_identity_is_bound_to_one_exact_act_occurrence():
    ledger = _ledger("ta\n")
    source_event = _byte_source(ledger)
    source = next(
        item
        for item in assertions_of_recorded_byte_measurement(ledger, source_event.id)
        if item.result == "exact_source_material_set"
    )
    first = _pair_input_applicability(
        source,
        target_act_id="pair-act-1",
        consumer_workspace_id="w",
        measurement_session_id="measurement",
    )
    second = _pair_input_applicability(
        source,
        target_act_id="pair-act-2",
        consumer_workspace_id="w",
        measurement_session_id="measurement",
    )

    assert first["dimensions"]["identity"] != second["dimensions"]["identity"]
    assert first["responsibility"]
    assert first["target_act_id"] == "pair-act-1"
    assert first["target_act_occurrence_id"] is None


def test_pair_applicability_has_real_non_applicable_and_unknown_outcomes():
    ledger = _ledger("ta\n")
    source_event = _byte_source(ledger)
    source = next(
        item
        for item in assertions_of_recorded_byte_measurement(ledger, source_event.id)
        if item.result == "exact_source_material_set"
    )
    inapplicable = _pair_input_applicability(
        source,
        target_act_id="pair-act-other-workspace",
        consumer_workspace_id="other",
        measurement_session_id="measurement",
    )
    carried = source.payload
    carried["dimensions"]["authority_warrant"] = "unrecognized"
    unknown_source = type(source)(
        assertion_id=source.assertion_id,
        recorded_occurrence_id=source.recorded_occurrence_id,
        byte_hex=source.byte_hex,
        result=source.result,
        _payload_json=json.dumps(carried),
        _support_assertion_refs_json="[]",
    )
    unknown = _pair_input_applicability(
        unknown_source,
        target_act_id="pair-act-unknown-authority",
        consumer_workspace_id="w",
        measurement_session_id="measurement",
    )

    assert inapplicable["dimensions"]["standing"] == "inapplicable"
    assert unknown["dimensions"]["standing"] == "Unknown"
    assert unknown["unknowns"][-1] == unknown["determination_basis"]


def test_negative_pair_applicability_is_recorded_and_the_target_act_does_not_occur():
    ledger = _ledger("ta\n")
    source = _byte_source(ledger)

    result = record_adjacent_byte_pair_count_layer(
        ledger,
        source_measurement_event_id=source.id,
        workspace_id="other",
        recording_session_id="measurement",
    )

    assert result.kind == BYTE_PAIR_APPLICABILITY_RECORDED_KIND
    recovered = get_recorded_pair_input_applicability(ledger, result.id)
    assert recovered["dimensions"]["standing"] == "inapplicable"
    assert recovered["target_act_occurrence_id"] is None
    assert recovered["dimensions"]["source_provenance"] == (
        "not consumed across the workspace boundary"
    )
    assert recovered["scope_locality"] == {
        "consumer_workspace_id": "other",
        "measurement_session_id": "measurement",
    }
    for coordinate in (
        "input_standing",
        "input_authority",
        "input_unknowns",
        "input_limits",
    ):
        assert recovered[coordinate]["carried"] is False
    assert recovered["coordinate_treatment"]["negative_authority"]["carried"] is False
    assert (
        result.payload["target_act_outcome"]
        == "not established by this Applicability claim"
    )
    assert not any(
        event.kind == BYTE_PAIR_MEASUREMENT_RECORDED_KIND
        for event in ledger.list_session("other", "measurement")
    )


def test_seed_native_measurement_and_result_assertions_keep_distinct_responsibilities():
    ledger = _ledger("ta\n")
    source = _byte_source(ledger)
    result = record_adjacent_byte_pair_count_layer(
        ledger,
        source_measurement_event_id=source.id,
        workspace_id="w",
        recording_session_id="measurement",
    )
    applicability = get_recorded_pair_input_applicability(
        ledger, result.payload["input_applicability_event_id"]
    )

    assert result.payload["responsible_boundary"] == (
        SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY
    )
    assert applicability["responsible_boundary"] == (
        SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY
    )
    assert result.payload["producer"] == RESPONSIBILITY_UNRECOVERED
    for assertion in result.payload["assertions"]:
        assert assertion["dimensions"]["responsibility"] != result.payload["responsibility"]


def test_pair_act_identity_is_not_its_occurrence_identity():
    ledger = _ledger("ta\n")
    source = _byte_source(ledger)
    result = record_adjacent_byte_pair_count_layer(
        ledger,
        source_measurement_event_id=source.id,
        workspace_id="w",
        recording_session_id="measurement",
    )

    assert result.payload["target_act_id"] != result.payload["act_occurrence_id"]
    assert result.payload["input_applicability"]["target_act_id"] == (
        result.payload["target_act_id"]
    )
    assert result.payload["input_applicability"]["target_act_occurrence_id"] is None


def test_pair_recovery_refuses_more_carrying_occurrences_than_total_pairs():
    ledger = _ledger("ta\n")
    source = _byte_source(ledger)
    event = record_adjacent_byte_pair_count_layer(
        ledger,
        source_measurement_event_id=source.id,
        workspace_id="w",
        recording_session_id="measurement",
    )
    count = next(
        assertion
        for assertion in event.payload["assertions"]
        if assertion["assertion_subject"]["pair_hex"] == "7461"
    )
    count["dimensions"]["content"] = {
        "occurrences_examined": 2,
        "occurrences_carrying": 2,
        "total_count": 1,
    }
    count["dimensions"]["identity"] = _identity(
        result="count",
        subject=count["assertion_subject"],
        scope=count["assertion_scope"],
        content=count["dimensions"]["content"],
    )
    commitment = production_commitment(
        BYTE_PAIR_MEASUREMENT_CONVENTION,
        {name: event.payload[name] for name in BYTE_PAIR_RESULT_COORDINATES},
    )
    ledger.get(event.payload["production_evidence_id"]).payload[
        "production_commitment"
    ] = commitment
    ledger.get(event.payload["responsible_act_evidence_id"]).payload[
        "result_commitment"
    ] = commitment

    with pytest.raises(ByteMeasurementError, match="unlawful pair count"):
        assertions_of_recorded_adjacent_byte_pair_measurement(ledger, event.id)
