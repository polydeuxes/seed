import json

from scripts import seed_local
from seed_runtime.emitter_attribution_audit import build_emitter_attribution_audit
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
