import json

from scripts import seed_local
from seed_runtime.emitter_consumer_audit import build_emitter_consumer_audit
from seed_runtime.events import EventLedger


def test_emitter_consumer_audit_renders(capsys):
    assert seed_local.main(["--emitter-consumer-audit"]) == 0
    out = capsys.readouterr().out
    assert "Emitter/Consumer Audit" in out
    assert "Status:" in out


def test_emitter_consumer_audit_json_valid(capsys):
    assert seed_local.main(["--emitter-consumer-audit", "--json"]) == 0
    data = json.loads(capsys.readouterr().out)
    assert "items" in data
    assert "summary" in data


def test_event_emitters_and_consumers_discovered():
    audit = build_emitter_consumer_audit()
    emitted = {output for item in audit.items for output in item.emits}
    assert "action_plan.created" in emitted
    action_item = next(item for item in audit.items if item.emitter == "action_plan")
    assert "projection builders" in action_item.consumers


def test_orphaned_and_consumed_outputs_reported():
    audit = build_emitter_consumer_audit()
    statuses = {item.status for item in audit.items}
    assert "consumed" in statuses
    assert "orphaned" in statuses or "partially_consumed" in statuses


def test_empty_state_builder_is_sane(tmp_path):
    (tmp_path / "seed_runtime").mkdir()
    (tmp_path / "scripts").mkdir()
    audit = build_emitter_consumer_audit(tmp_path)
    assert audit.items == ()
    assert audit.summary["items_scanned"] == 0


def test_emitter_consumer_audit_does_not_write_event_ledger_or_mutate_cluster():
    ledger = EventLedger()
    before = ledger.list_events()
    audit = build_emitter_consumer_audit()
    after = ledger.list_events()
    assert before == after == []
    assert audit.metadata["discovery"]
