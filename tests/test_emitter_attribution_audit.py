import json

from scripts import seed_local
from seed_runtime.emitter_attribution_audit import (
    ClassifiedEvidence,
    build_emitter_attribution_audit,
    _classify_unknown_emitter_attribution,
    _collect_emitter_attribution_implementation_evidence,
)
from seed_runtime.events import EventLedger


def test_emitter_attribution_audit_renders(capsys):
    assert seed_local.main(["--emitter-attribution-audit"]) == 0
    out = capsys.readouterr().out
    assert "Emitter Attribution Audit" in out
    assert "Reason:" in out


def test_emitter_attribution_audit_json_valid(capsys):
    assert seed_local.main(["--emitter-attribution-audit", "--json"]) == 0
    data = json.loads(capsys.readouterr().out)
    assert "items" in data
    assert "summary" in data
    assert data["items"][0]["event"]


def test_attributed_emitters_are_reported():
    audit = build_emitter_attribution_audit()
    assert any(
        item.status == "attributed" and item.emitter != "unknown"
        for item in audit.items
    )


def test_unknown_emitters_are_reported():
    audit = build_emitter_attribution_audit()
    assert any(item.emitter == "unknown" for item in audit.items)


def test_discovery_gap_explanations_appear_for_consumed_literal_without_emit(tmp_path):
    runtime = tmp_path / "seed_runtime"
    scripts = tmp_path / "scripts"
    runtime.mkdir()
    scripts.mkdir()
    (runtime / "state.py").write_text(
        'def consume(event):\n    return event.kind == "gap.event"\n'
    )
    audit = build_emitter_attribution_audit(tmp_path)
    item = next(item for item in audit.items if item.event == "gap.event")
    assert item.status == "discovery_gap"
    assert "no direct emit call" in item.reason


def test_workflow_events_appear_when_implementation_evidence_exists(tmp_path):
    runtime = tmp_path / "seed_runtime"
    scripts = tmp_path / "scripts"
    runtime.mkdir()
    scripts.mkdir()
    (runtime / "state.py").write_text(
        'def consume(event):\n    return event.kind == "pending_action.completed"\n'
    )
    (runtime / "pending_actions.py").write_text(
        'from seed_runtime.events import Event\ndef helper(kind):\n    return Event(kind=kind, subject="s", predicate="p", object="o")\n'
    )
    audit = build_emitter_attribution_audit(tmp_path)
    item = next(
        item for item in audit.items if item.event == "pending_action.completed"
    )
    assert item.status == "dynamic"
    assert "workflow event" in item.reason


def test_empty_state_builder_is_sane(tmp_path):
    (tmp_path / "seed_runtime").mkdir()
    (tmp_path / "scripts").mkdir()
    audit = build_emitter_attribution_audit(tmp_path)
    assert audit.items == ()
    assert audit.summary["items_scanned"] == 0


def test_emitter_attribution_audit_does_not_write_event_ledger_or_mutate_cluster():
    ledger = EventLedger()
    before = ledger.list_events()
    audit = build_emitter_attribution_audit()
    after = ledger.list_events()
    assert before == after == []
    assert audit.metadata["discovery"]


def test_attribution_excludes_rendered_messages_from_default_counts():
    audit = build_emitter_attribution_audit()
    events = {item.event for item in audit.items}
    assert (
        "No deterministic related material found in projected read models."
        not in events
    )
    assert "No supportable lexical overlap was found." not in events
    assert (
        "Guardrail: diagnostic only; no ownership facts are inferred or written."
        not in events
    )
    assert all(item.emission_type == "domain_emission" for item in audit.items)
    assert audit.summary["attributed"] == sum(
        item.status == "attributed" and item.emission_type == "domain_emission"
        for item in audit.items
    )


def test_action_plan_events_remain_attributed():
    audit = build_emitter_attribution_audit()
    item = next(item for item in audit.items if item.event == "action_plan.created")
    assert item.status == "attributed"
    assert item.emitter == "action_plan"
    assert item.emission_type == "domain_emission"


def test_attribution_include_rendered_classifies_guardrail_messages(capsys):
    assert seed_local.main(["--emitter-attribution-audit", "--include-rendered"]) == 0
    out = capsys.readouterr().out
    assert (
        "Guardrail: diagnostic only; no ownership facts are inferred or written." in out
    )
    assert "Emission type: guardrail_text" in out


def test_attribution_json_reports_domain_classification(capsys):
    assert seed_local.main(["--emitter-attribution-audit", "--json"]) == 0
    data = json.loads(capsys.readouterr().out)
    assert {item["emission_type"] for item in data["items"]} == {"domain_emission"}


def test_direct_append_literal_attributes_unknown_emitter_candidate(tmp_path):
    runtime = tmp_path / "seed_runtime"
    scripts = tmp_path / "scripts"
    runtime.mkdir()
    scripts.mkdir()
    (runtime / "workflow.py").write_text(
        'def emit(self):\n    self._require_ledger().append("workflow.done", "s", {})\n',
        encoding="utf-8",
    )
    (runtime / "state.py").write_text(
        'def consume(event):\n    return event.kind == "workflow.done"\n',
        encoding="utf-8",
    )

    audit = build_emitter_attribution_audit(tmp_path)
    item = next(item for item in audit.items if item.event == "workflow.done")

    assert item.status == "attributed"
    assert item.confidence == "high"
    assert item.emitter == "workflow"
    assert item.attribution_evidence[0].category == "direct_emitter"


def test_dynamic_construction_does_not_override_direct_emitter_evidence(tmp_path):
    runtime = tmp_path / "seed_runtime"
    scripts = tmp_path / "scripts"
    runtime.mkdir()
    scripts.mkdir()
    (runtime / "action_plans.py").write_text(
        "from seed_runtime.events import Event\n"
        "def emit(self, kind):\n"
        '    Event(kind=kind, subject="s", predicate="p", object="o")\n'
        '    self._require_ledger().append("action_plan.accepted", "s", {})\n',
        encoding="utf-8",
    )
    (runtime / "state.py").write_text(
        'def consume(event):\n    return event.kind == "action_plan.accepted"\n',
        encoding="utf-8",
    )

    audit = build_emitter_attribution_audit(tmp_path)
    item = next(item for item in audit.items if item.event == "action_plan.accepted")

    assert item.status == "attributed"
    assert item.confidence == "high"
    assert any(e.category == "direct_emitter" for e in item.attribution_evidence)
    assert any(e.category == "event_constructor" for e in item.supporting_references)


def test_action_plan_lifecycle_events_are_attributed_from_direct_evidence():
    audit = build_emitter_attribution_audit()

    for event in (
        "action_plan.accepted",
        "action_plan.approved",
        "action_plan.rejected",
        "action_plan.superseded",
    ):
        item = next(item for item in audit.items if item.event == event)
        assert item.status == "attributed"
        assert item.emitter == "action_plan"
        assert item.confidence == "high"
        assert any(e.category == "direct_emitter" for e in item.attribution_evidence)
        assert item.supporting_references


def test_attribution_json_distinguishes_driving_evidence_from_references(capsys):
    assert seed_local.main(["--emitter-attribution-audit", "--json"]) == 0
    data = json.loads(capsys.readouterr().out)
    item = next(i for i in data["items"] if i["event"] == "action_plan.accepted")

    assert item["confidence"] == "high"
    assert item["attribution_evidence"]
    assert item["attribution_evidence"][0]["category"] == "direct_emitter"
    assert "supporting_references" in item



def test_unknown_emitter_classification_preserves_returned_fields():
    direct = (ClassifiedEvidence("direct_emitter", "seed_runtime/workflow.py:2"),)
    indirect = (ClassifiedEvidence("indirect_emitter", "seed_runtime/pending_actions.py:4"),)
    diagnostic = (ClassifiedEvidence("diagnostic_reference", "seed_runtime/audit.py:5"),)
    string_ref = (ClassifiedEvidence("string_reference", "seed_runtime/other.py:6"),)
    dynamic = (ClassifiedEvidence("event_constructor", "seed_runtime/events.py:7"),)

    attributed = _classify_unknown_emitter_attribution("workflow.done", direct, dynamic)
    assert attributed.status == "attributed"
    assert attributed.reason.startswith("direct emitter evidence")
    assert attributed.emitter == "workflow"
    assert attributed.confidence == "high"
    assert attributed.attribution_evidence == direct
    assert attributed.supporting_references == dynamic

    workflow_dynamic_with_refs = _classify_unknown_emitter_attribution(
        "pending_action.completed", diagnostic, dynamic
    )
    assert workflow_dynamic_with_refs.status == "dynamic"
    assert workflow_dynamic_with_refs.reason.startswith("workflow event")
    assert workflow_dynamic_with_refs.emitter == "unknown"
    assert workflow_dynamic_with_refs.confidence == "low"
    assert workflow_dynamic_with_refs.attribution_evidence == dynamic
    assert workflow_dynamic_with_refs.supporting_references == diagnostic

    indirect_result = _classify_unknown_emitter_attribution(
        "custom.event", indirect + string_ref, dynamic
    )
    assert indirect_result.status == "indirect"
    assert indirect_result.reason.startswith("event is visible through workflow helper")
    assert indirect_result.emitter == "unknown"
    assert indirect_result.confidence == "medium"
    assert indirect_result.attribution_evidence == indirect
    assert indirect_result.supporting_references == string_ref + dynamic

    discovery_gap = _classify_unknown_emitter_attribution("custom.event", string_ref, ())
    assert discovery_gap.status == "discovery_gap"
    assert discovery_gap.reason.startswith("event literal is present")
    assert discovery_gap.emitter == "unknown"
    assert discovery_gap.confidence == "low"
    assert discovery_gap.attribution_evidence == ()
    assert discovery_gap.supporting_references == string_ref

    workflow_dynamic_only = _classify_unknown_emitter_attribution(
        "action_plan.created", (), dynamic
    )
    assert workflow_dynamic_only.status == "dynamic"
    assert workflow_dynamic_only.attribution_evidence == dynamic
    assert workflow_dynamic_only.supporting_references == ()

    missing = _classify_unknown_emitter_attribution("custom.event", (), ())
    assert missing.status == "missing"
    assert missing.reason.startswith("event is consumed")
    assert missing.emitter == "unknown"
    assert missing.confidence == "none"
    assert missing.attribution_evidence == ()
    assert missing.supporting_references == ()



def test_implementation_evidence_collection_preserves_sources_and_ordering(tmp_path):
    runtime = tmp_path / "seed_runtime"
    runtime.mkdir()
    (runtime / "alpha.py").write_text(
        'from seed_runtime.events import Event\n'
        'def dynamic(kind):\n'
        '    Event(kind=kind, subject="s", predicate="p", object="o")\n'
        'def direct(self):\n'
        '    self._require_ledger().append("alpha.created", "s", {})\n'
        'def literal(event):\n'
        '    return event.kind == "alpha.created"\n',
        encoding="utf-8",
    )
    (runtime / "zeta.py").write_text(
        'def dynamic_append(self, kind):\n'
        '    self._require_ledger().append(kind, "s", {})\n'
        'def literal():\n'
        '    return "zeta.reference"\n',
        encoding="utf-8",
    )
    evidence = _collect_emitter_attribution_implementation_evidence(tmp_path)

    alpha_refs = evidence.literal_references["alpha.created"]
    assert [(e.category, e.location) for e in alpha_refs] == sorted(
        (e.category, e.location) for e in alpha_refs
    )
    assert ("direct_emitter", "seed_runtime/alpha.py:5") in [
        (e.category, e.location) for e in alpha_refs
    ]
    assert any(e.category == "string_reference" for e in alpha_refs)
    assert evidence.literal_references["zeta.reference"] == (
        ClassifiedEvidence("string_reference", "seed_runtime/zeta.py:4"),
    )
    assert evidence.dynamic_event_construction == tuple(
        sorted(evidence.dynamic_event_construction, key=lambda e: (e.category, e.location))
    )
    assert evidence.dynamic_event_construction == (
        ClassifiedEvidence("event_constructor", "seed_runtime/alpha.py:3"),
        ClassifiedEvidence("event_constructor", "seed_runtime/zeta.py:2"),
    )
