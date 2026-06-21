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
