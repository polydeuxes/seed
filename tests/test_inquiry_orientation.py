from __future__ import annotations

from datetime import datetime, timezone

from seed_runtime.events import EventLedger
from seed_runtime.facts import Fact
from seed_runtime.inquiry_orientation import (
    AUTHORITY_BOUNDARY,
    _InquiryOrientationAnswer,
    _InquiryOrientationCompositionRequest,
    _InquiryOrientationEvidence,
    _InquiryOrientationSelectedMaterial,
    _collect_inquiry_orientation_evidence,
    _compose_inquiry_orientation_answer,
    _prepare_inquiry_orientation_composition,
    _prepare_inquiry_orientation_selected_material,
    _select_inquiry_orientation_limitations,
    _select_inquiry_orientation_reason,
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

    assert (
        "Inquiry note:\n  example_host keeps showing up first and that feels wrong"
        in output
    )
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


def test_state_summary_and_source_navigation_matches_do_not_assert_importance_or_ownership(
    tmp_path,
):
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


def _state_with_example_source_navigation_fact():
    ledger = EventLedger()
    fact = Fact(
        id="fact_example_source_define",
        subject_id="seed_runtime.example",
        predicate="defines",
        value="seed_runtime.example.examplesurface",
        dimensions={"path": "seed_runtime/example.py"},
        observed_at=utc_now(),
        evidence_ids=["evd_example_source_define"],
    )
    ledger.append("fact.observed", "ws", {"fact": to_plain(fact)})
    return ledger, StateProjector(ledger).project("ws")


def test_fact_support_surface_family_renders_without_changing_match(tmp_path):
    _ledger, state = _state_with_example_host_fact()
    note = record_inquiry_note(
        tmp_path / "probe.jsonl",
        "example_host keeps showing up first",
        recorded_at=datetime(2026, 6, 16, tzinfo=timezone.utc),
    )

    view = build_inquiry_orientation(state, note)
    output = format_inquiry_orientation(view)

    assert [
        (item.material_type, item.label, item.surface, item.support)
        for item in view.related_material
    ] == [
        (
            "projected fact support",
            "example_host",
            "example_host runtime prometheus-node-exporter",
            "fact support subject='example_host' predicate='runtime' path=None",
        )
    ]
    assert view.related_material[0].surface_family == "fact support"
    assert "surface family:\n      fact support" in output


def test_source_navigation_surface_family_renders_without_changing_match(tmp_path):
    _ledger, state = _state_with_example_source_navigation_fact()
    note = record_inquiry_note(
        tmp_path / "probe.jsonl",
        "examplesurface source lookup",
        recorded_at=datetime(2026, 6, 16, tzinfo=timezone.utc),
    )

    view = build_inquiry_orientation(state, note)
    output = format_inquiry_orientation(view)

    source_matches = [
        item
        for item in view.related_material
        if item.material_type == "source navigation defines"
    ]
    assert [
        (item.material_type, item.label, item.surface, item.support)
        for item in source_matches
    ] == [
        (
            "source navigation defines",
            "seed_runtime.example.examplesurface",
            "seed_runtime.example.examplesurface (seed_runtime/example.py)",
            "source-navigation support=seed_runtime.example|defines|seed_runtime.example.examplesurface|path=seed_runtime/example.py",
        )
    ]
    assert source_matches[0].surface_family == "source navigation"
    assert "surface family:\n      source navigation" in output


def test_surface_family_labels_preserve_ranking_and_retrieval_scope(tmp_path):
    _ledger, state = _state_with_example_source_navigation_fact()
    note = record_inquiry_note(
        tmp_path / "probe.jsonl",
        "seed_runtime.example examplesurface",
        recorded_at=datetime(2026, 6, 16, tzinfo=timezone.utc),
    )

    view = build_inquiry_orientation(state, note)

    assert [(item.material_type, item.label) for item in view.related_material] == [
        ("projected fact support", "seed_runtime.example"),
        ("source navigation defines", "seed_runtime.example.examplesurface"),
    ]
    assert len(view.related_material) == 2
    assert {item.surface_family for item in view.related_material} == {
        "fact support",
        "source navigation",
    }


def test_surface_family_labels_do_not_add_authority_claims(tmp_path):
    _ledger, state = _state_with_example_source_navigation_fact()
    note = record_inquiry_note(
        tmp_path / "probe.jsonl",
        "examplesurface",
        recorded_at=datetime(2026, 6, 16, tzinfo=timezone.utc),
    )

    view = build_inquiry_orientation(state, note)
    output = format_inquiry_orientation(view).lower()

    assert "surface family:" in output
    for item in view.related_material:
        label = item.surface_family.lower()
        assert "importance" not in label
        assert "intent" not in label
        assert "concern" not in label
        assert "action" not in label
        assert "recommend" not in label
    assert "recommended action" in output  # only in the negated authority boundary
    assert "next safe move" in output  # only in the negated authority boundary


def test_inquiry_orientation_composition_request_separates_note_from_rendering(tmp_path):
    _ledger, state = _state_with_example_host_fact()
    note = record_inquiry_note(
        tmp_path / "probe.jsonl",
        "example_host keeps showing up first",
        recorded_at=datetime(2026, 6, 16, tzinfo=timezone.utc),
    )

    request = _prepare_inquiry_orientation_composition(note)
    evidence = _collect_inquiry_orientation_evidence(state, request)
    selected_material = _prepare_inquiry_orientation_selected_material(evidence)
    answer = _compose_inquiry_orientation_answer(state, request)
    view = build_inquiry_orientation(state, note)
    output = format_inquiry_orientation(view)

    assert isinstance(request, _InquiryOrientationCompositionRequest)
    assert isinstance(evidence, _InquiryOrientationEvidence)
    assert isinstance(selected_material, _InquiryOrientationSelectedMaterial)
    assert isinstance(answer, _InquiryOrientationAnswer)
    assert request.note == note
    assert request.note_tokens == {"example_host", "keeps", "showing", "first"}
    assert evidence.related_material == selected_material.related_material
    assert selected_material.related_material == answer.answer == view.related_material
    assert answer.boundary == view.authority_boundary == AUTHORITY_BOUNDARY
    assert answer.limitations == view.uncertainty
    assert selected_material.support == [item.support for item in view.related_material]
    assert answer.support == selected_material.support
    assert answer.limitations == _select_inquiry_orientation_limitations(
        selected_material
    )
    assert answer.reason == _select_inquiry_orientation_reason(selected_material)
    assert "deterministic lexical overlaps" in answer.reason
    assert "Inquiry note:" in output
    assert "raw_note" not in request.__dataclass_fields__
    assert "recorded_at" not in request.__dataclass_fields__
    assert "workspace_id" not in request.__dataclass_fields__
    assert "answer" not in evidence.__dataclass_fields__
    assert "reason" not in evidence.__dataclass_fields__
    assert "boundary" not in evidence.__dataclass_fields__
    assert "limitations" not in evidence.__dataclass_fields__
    assert "note" not in selected_material.__dataclass_fields__
    assert "reason" not in selected_material.__dataclass_fields__
    assert "boundary" not in selected_material.__dataclass_fields__
    assert "limitations" not in selected_material.__dataclass_fields__
    assert "Inquiry note" not in answer.__dataclass_fields__
    assert "related_material" not in answer.__dataclass_fields__
    assert "uncertainty" not in answer.__dataclass_fields__
    assert "authority_boundary" not in answer.__dataclass_fields__


def test_selected_material_limitations_are_owned_before_answer_construction(tmp_path):
    _ledger, state = _state_with_example_host_fact()
    matched_note = record_inquiry_note(
        tmp_path / "probe.jsonl",
        "example_host keeps showing up first",
        recorded_at=datetime(2026, 6, 16, tzinfo=timezone.utc),
    )
    unmatched_note = record_inquiry_note(
        tmp_path / "probe.jsonl",
        "unmatched prose only",
        recorded_at=datetime(2026, 6, 17, tzinfo=timezone.utc),
    )

    matched_request = _prepare_inquiry_orientation_composition(matched_note)
    matched_material = _prepare_inquiry_orientation_selected_material(
        _collect_inquiry_orientation_evidence(state, matched_request)
    )
    unmatched_request = _prepare_inquiry_orientation_composition(unmatched_note)
    unmatched_material = _prepare_inquiry_orientation_selected_material(
        _collect_inquiry_orientation_evidence(state, unmatched_request)
    )

    assert _select_inquiry_orientation_limitations(matched_material) == (
        "Related material may be incomplete or incidental; lexical overlap is not "
        "semantic interpretation and does not establish operator intent."
    )
    assert _select_inquiry_orientation_limitations(unmatched_material) == (
        "No deterministic related material was found in already projected read models; "
        "this absence does not prove the note is unrelated to existing work."
    )
    assert _compose_inquiry_orientation_answer(
        state, matched_request
    ).limitations == _select_inquiry_orientation_limitations(matched_material)
    assert _compose_inquiry_orientation_answer(
        state, unmatched_request
    ).limitations == _select_inquiry_orientation_limitations(unmatched_material)
    assert "answer" not in matched_material.__dataclass_fields__
    assert "boundary" not in matched_material.__dataclass_fields__
    assert "reason" not in matched_material.__dataclass_fields__


def test_selected_material_reason_is_owned_before_answer_construction(tmp_path):
    _ledger, state = _state_with_example_source_navigation_fact()
    note = record_inquiry_note(
        tmp_path / "probe.jsonl",
        "seed_runtime.example examplesurface",
        recorded_at=datetime(2026, 6, 18, tzinfo=timezone.utc),
    )

    request = _prepare_inquiry_orientation_composition(note)
    selected_material = _prepare_inquiry_orientation_selected_material(
        _collect_inquiry_orientation_evidence(state, request)
    )
    reason = _select_inquiry_orientation_reason(selected_material)
    answer = _compose_inquiry_orientation_answer(state, request)

    assert reason == (
        "deterministic lexical overlaps against projected fact supports and "
        "source-navigation matches"
    )
    assert answer.reason == reason
    assert selected_material.related_material == answer.answer
    assert selected_material.support == answer.support
    assert "boundary" not in selected_material.__dataclass_fields__
    assert "limitations" not in selected_material.__dataclass_fields__
    assert "reason" not in selected_material.__dataclass_fields__
