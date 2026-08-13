from io import StringIO

import pytest

from seed_runtime.byte_measurement import (
    BYTE_MEASUREMENT_RECORDED_KIND,
    BYTE_MEASUREMENT_CONVENTION,
    BYTE_RESULT_COORDINATES,
    BYTE_MEASUREMENT_RULE,
    ByteMeasurementError,
    RESPONSIBILITY_UNRECOVERED,
    _measure_byte_counts_through,
    assertions_of_recorded_byte_measurement,
    measure_byte_counts,
    record_byte_count_layer,
)
from seed_runtime.events import EventLedger
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
