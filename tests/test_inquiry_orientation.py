from __future__ import annotations

from datetime import datetime, timezone

from seed_runtime.events import EventLedger
from seed_runtime.facts import Fact
from seed_runtime.inquiry_orientation import (
    AUTHORITY_BOUNDARY,
    build_inquiry_orientation,
    format_inquiry_orientation,
    load_inquiry_notes,
    record_inquiry_note,
)
from seed_runtime.models import utc_now
from seed_runtime.serialization import to_plain
from seed_runtime.state import StateProjector


def _state_with_example_host_fact():
    ledger = EventLedger()
    fact = Fact(
        id="fact_example_host_runtime",
        subject_id="example_host",
        predicate="runtime",
        value="prometheus-node-exporter",
        observed_at=utc_now(),
        evidence_ids=["evd_example_host"],
    )
    ledger.append("fact.observed", "ws", {"fact": to_plain(fact)})
    return ledger, StateProjector(ledger).project("ws")


def test_record_inquiry_note_preserves_raw_note_and_minimal_provenance(tmp_path):
    raw_note = "example_host keeps showing up first and that feels wrong"
    recorded_at = datetime(2026, 6, 16, 1, 2, 3, tzinfo=timezone.utc)

    record = record_inquiry_note(
        tmp_path / "probe.jsonl",
        raw_note,
        workspace_id="ws",
        session_id="sess",
        recorded_at=recorded_at,
    )

    loaded = load_inquiry_notes(tmp_path / "probe.jsonl")
    assert loaded == [record]
    assert record.note_id.startswith("inq_")
    assert record.raw_note == raw_note
    assert record.recorded_at == "2026-06-16T01:02:03Z"
    assert record.source == "scripts.seed_local --record-inquiry-note"
    assert record.workspace_id == "ws"
    assert record.session_id == "sess"


def test_inquiry_note_is_not_projected_into_runtime_state(tmp_path):
    ledger, before = _state_with_example_host_fact()

    record_inquiry_note(tmp_path / "probe.jsonl", "example_host feels wrong")
    after = StateProjector(ledger).project("ws")

    assert set(after.facts) == set(before.facts)
    assert after.observed_facts == before.observed_facts
    assert after.inferred_facts == before.inferred_facts
    assert after.goals == before.goals == {}
    assert after.tool_needs == before.tool_needs == {}
    assert after.execution_authorizations == before.execution_authorizations == {}
    assert after.execution_proposals == before.execution_proposals == {}
    assert after.pending_actions == before.pending_actions == {}
    assert after.action_plans == before.action_plans == {}
    assert after.handoff_plans == before.handoff_plans == {}
    assert after.tools == before.tools == {}


def test_orientation_output_includes_required_sections_and_supported_match(tmp_path):
    _ledger, state = _state_with_example_host_fact()
    note = record_inquiry_note(
        tmp_path / "probe.jsonl",
        "example_host keeps showing up first and that feels wrong",
        recorded_at=datetime(2026, 6, 16, tzinfo=timezone.utc),
    )

    output = format_inquiry_orientation(build_inquiry_orientation(state, note))

    assert "Inquiry note:\n  example_host keeps showing up first and that feels wrong" in output
    assert "Potentially related material:" in output
    assert "example_host runtime prometheus-node-exporter" in output
    assert "Support / why related:" in output
    assert "case-normalized token overlap: example_host" in output
    assert "Uncertainty:" in output
    assert "Authority boundary:" in output
    assert AUTHORITY_BOUNDARY in output
    assert "next safe move" in output  # only as a negated authority boundary phrase


def test_orientation_explicitly_renders_absent_related_material(tmp_path):
    _ledger, state = _state_with_example_host_fact()
    note = record_inquiry_note(
        tmp_path / "probe.jsonl",
        "unmatched prose only",
        recorded_at=datetime(2026, 6, 16, tzinfo=timezone.utc),
    )

    output = format_inquiry_orientation(build_inquiry_orientation(state, note))

    assert "No deterministic related material found" in output
    assert "No supportable lexical overlap was found." in output
    assert "Uncertainty:" in output
    assert "Authority boundary:" in output


def test_orientation_helper_does_not_mutate_state_or_create_actions(tmp_path):
    _ledger, state = _state_with_example_host_fact()
    before = (
        dict(state.facts),
        dict(state.goals),
        dict(state.tool_needs),
        dict(state.execution_proposals),
        dict(state.pending_actions),
        dict(state.action_plans),
    )
    note = record_inquiry_note(
        tmp_path / "probe.jsonl",
        "example_host wrong",
        recorded_at=datetime(2026, 6, 16, tzinfo=timezone.utc),
    )

    view = build_inquiry_orientation(state, note)

    assert (
        dict(state.facts),
        dict(state.goals),
        dict(state.tool_needs),
        dict(state.execution_proposals),
        dict(state.pending_actions),
        dict(state.action_plans),
    ) == before
    assert view.related_material
    assert state.tool_needs == {}
    assert state.execution_proposals == {}
    assert state.pending_actions == {}
    assert state.action_plans == {}


def test_state_summary_and_source_navigation_matches_do_not_assert_importance_or_ownership(tmp_path):
    _ledger, state = _state_with_example_host_fact()
    note = record_inquiry_note(
        tmp_path / "probe.jsonl",
        "example_host first owner",
        recorded_at=datetime(2026, 6, 16, tzinfo=timezone.utc),
    )

    output = format_inquiry_orientation(build_inquiry_orientation(state, note))

    assert "importance" in output
    assert "ownership" in output
    assert "assert importance" in output
    assert "assert ownership" in output
    assert "owner:" not in output.lower()
    assert "most important" not in output.lower()
