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


def test_rendered_fallback_and_guardrail_strings_are_excluded_by_default():
    audit = build_emitter_consumer_audit()
    emitted = {output for item in audit.items for output in item.emits}
    assert (
        "No deterministic related material found in projected read models."
        not in emitted
    )
    assert "No supportable lexical overlap was found." not in emitted
    assert (
        "Guardrail: diagnostic only; no ownership facts are inferred or written."
        not in emitted
    )
    assert all(item.emission_type == "domain_emission" for item in audit.items)


def test_pending_action_events_remain_visible_as_domain_emissions():
    audit = build_emitter_consumer_audit()
    emitted = {output for item in audit.items for output in item.emits}
    assert "pending_action.completed" in emitted
    assert "pending_action.approved" in emitted
    assert all(item.emission_type == "domain_emission" for item in audit.items)


def test_emitter_consumer_include_rendered_classifies_rendered_strings(capsys):
    assert seed_local.main(["--emitter-consumer-audit", "--include-rendered"]) == 0
    out = capsys.readouterr().out
    assert (
        "Guardrail: diagnostic only; no ownership facts are inferred or written." in out
    )
    assert "Emission type: guardrail_text" in out


def test_emitter_consumer_json_reports_domain_classification(capsys):
    assert seed_local.main(["--emitter-consumer-audit", "--json"]) == 0
    data = json.loads(capsys.readouterr().out)
    assert {item["emission_type"] for item in data["items"]} == {"domain_emission"}


def test_scan_result_collection_preserves_outputs_evidence_gating_and_read_only(tmp_path):
    runtime = tmp_path / "seed_runtime"
    scripts = tmp_path / "scripts"
    runtime.mkdir()
    scripts.mkdir()
    (runtime / "producer.py").write_text(
        "def produce(ledger):\n"
        "    ledger.append('slice.visible')\n"
        "    lines = []\n"
        "    lines.append('Guardrail: visible only with rendered strings.')\n",
        encoding="utf-8",
    )
    (runtime / "consumer.py").write_text(
        "def consume(event):\n"
        "    if event.kind == 'slice.visible':\n"
        "        return True\n",
        encoding="utf-8",
    )

    ledger = EventLedger()
    before = ledger.list_events()
    audit = build_emitter_consumer_audit(tmp_path)
    after = ledger.list_events()

    emitted = {output for item in audit.items for output in item.emits}
    visible = next(item for item in audit.items if item.emits == ("slice.visible",))
    assert before == after == []
    assert "slice.visible" in emitted
    assert "Guardrail: visible only with rendered strings." not in emitted
    assert visible.consumers == ("diagnostics and audits",)
    assert visible.evidence == ("seed_runtime/producer.py:2",)
    assert visible.emission_type == "domain_emission"

    rendered_audit = build_emitter_consumer_audit(tmp_path, include_rendered=True)
    rendered = next(
        item
        for item in rendered_audit.items
        if item.emits == ("Guardrail: visible only with rendered strings.",)
    )
    assert rendered.emission_type == "guardrail_text"


def test_relationship_status_derivation_preserves_statuses_summary_json_and_text(tmp_path):
    runtime = tmp_path / "seed_runtime"
    scripts = tmp_path / "scripts"
    runtime.mkdir()
    scripts.mkdir()
    (runtime / "producer.py").write_text(
        "def produce(ledger):\n"
        "    ledger.append_many('slice.consumed')\n"
        "    ledger.append_many('slice.orphaned')\n"
        "    ledger.append_many('slice.partial_one')\n"
        "    ledger.append_many('slice.partial_two')\n",
        encoding="utf-8",
    )
    (runtime / "consumer.py").write_text(
        "def consume(event):\n"
        "    if event.kind in {'slice.consumed', 'slice.partial_one'}:\n"
        "        return True\n"
        "    if event.kind == 'slice.unknown_consumer_only':\n"
        "        return True\n",
        encoding="utf-8",
    )

    audit = build_emitter_consumer_audit(tmp_path)
    producer = next(item for item in audit.items if item.emitter == "producer")
    unknown = next(item for item in audit.items if item.emitter == "unknown")

    assert producer.status == "partially_consumed"
    assert unknown.status == "unknown"
    assert audit.summary["partially_consumed"] == 1
    assert audit.summary["unknown"] == 1
    assert producer.to_json_dict()["status"] == "partially_consumed"
    text = seed_local.format_emitter_consumer_audit(audit)
    assert "Status: partially_consumed" in text
    assert "Status: unknown" in text

    (runtime / "producer.py").write_text(
        "def produce(ledger):\n"
        "    ledger.append('slice.consumed')\n",
        encoding="utf-8",
    )
    (runtime / "orphan.py").write_text(
        "def produce(ledger):\n"
        "    ledger.append('slice.orphaned')\n",
        encoding="utf-8",
    )
    consumed_or_orphaned = build_emitter_consumer_audit(tmp_path)
    statuses = {item.emits[0]: item.status for item in consumed_or_orphaned.items}
    assert statuses["slice.consumed"] == "consumed"
    assert statuses["slice.orphaned"] == "orphaned"


def test_unknown_emitter_rows_preserve_consumers_order_shape_text_and_read_only(tmp_path):
    runtime = tmp_path / "seed_runtime"
    scripts = tmp_path / "scripts"
    runtime.mkdir()
    scripts.mkdir()
    (runtime / "consumer.py").write_text(
        "def consume(event):\n"
        "    if event.kind == 'slice.missing_b':\n"
        "        return True\n"
        "    if event.kind == 'slice.missing_a':\n"
        "        return True\n",
        encoding="utf-8",
    )

    ledger = EventLedger()
    before = ledger.list_events()
    audit = build_emitter_consumer_audit(tmp_path)
    after = ledger.list_events()
    unknown_rows = [item for item in audit.items if item.emitter == "unknown"]

    assert before == after == []
    assert [row.emits for row in unknown_rows] == [
        ("slice.missing_a",),
        ("slice.missing_b",),
    ]
    assert all(row.status == "unknown" for row in unknown_rows)
    assert all(row.consumers == ("diagnostics and audits",) for row in unknown_rows)
    json_rows = [row.to_json_dict() for row in unknown_rows]
    assert json_rows == [
        {
            "emitter": "unknown",
            "emits": ["slice.missing_a"],
            "consumers": ["diagnostics and audits"],
            "status": "unknown",
            "evidence": [],
            "emission_type": "domain_emission",
        },
        {
            "emitter": "unknown",
            "emits": ["slice.missing_b"],
            "consumers": ["diagnostics and audits"],
            "status": "unknown",
            "evidence": [],
            "emission_type": "domain_emission",
        },
    ]
    text = seed_local.format_emitter_consumer_audit(audit)
    assert "Emitter: unknown" in text
    assert "slice.missing_a" in text
    assert "slice.missing_b" in text
    assert "Status: unknown" in text
