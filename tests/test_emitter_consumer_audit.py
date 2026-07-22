import json

from scripts import seed_local
from seed_runtime.diagnostic_inventory import DIAGNOSTIC_INVENTORY
from seed_runtime.diagnostic_shape_audit import build_diagnostic_shape_audit
from seed_runtime.emitter_consumer_audit import (
    EmitterConsumerItem,
    _assemble_emitter_consumer_audit,
    build_emitter_consumer_audit,
)
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
    assert statuses & {"consumed", "unknown"}


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


def test_scanned_emitted_item_rows_preserve_shape_status_evidence_text_and_unknowns(tmp_path):
    runtime = tmp_path / "seed_runtime"
    scripts = tmp_path / "scripts"
    runtime.mkdir()
    scripts.mkdir()
    (runtime / "producer.py").write_text(
        "def produce(ledger):\n"
        "    ledger.append('slice.scanned_a')\n"
        "    ledger.append('slice.scanned_b')\n"
        "    ledger.append('slice.scanned_orphan')\n",
        encoding="utf-8",
    )
    (runtime / "consumer.py").write_text(
        "def consume(event):\n"
        "    if event.kind == 'slice.scanned_a':\n"
        "        return True\n"
        "    if event.kind == 'slice.unknown_present':\n"
        "        return True\n",
        encoding="utf-8",
    )
    (scripts / "seed_local.py").write_text(
        "def consume(event):\n"
        "    if event.kind == 'slice.scanned_b':\n"
        "        return True\n",
        encoding="utf-8",
    )

    ledger = EventLedger()
    before = ledger.list_events()
    audit = build_emitter_consumer_audit(tmp_path)
    after = ledger.list_events()

    producer = next(item for item in audit.items if item.emitter == "producer")
    unknown = next(item for item in audit.items if item.emitter == "unknown")

    assert before == after == []
    assert producer.emits == (
        "slice.scanned_a",
        "slice.scanned_b",
        "slice.scanned_orphan",
    )
    assert producer.consumers == ("CLI surfaces", "diagnostics and audits")
    assert producer.status == "partially_consumed"
    assert producer.evidence == (
        "seed_runtime/producer.py:2",
        "seed_runtime/producer.py:3",
        "seed_runtime/producer.py:4",
    )
    assert producer.to_json_dict() == {
        "emitter": "producer",
        "emits": [
            "slice.scanned_a",
            "slice.scanned_b",
            "slice.scanned_orphan",
        ],
        "consumers": ["CLI surfaces", "diagnostics and audits"],
        "status": "partially_consumed",
        "evidence": [
            "seed_runtime/producer.py:2",
            "seed_runtime/producer.py:3",
            "seed_runtime/producer.py:4",
        ],
        "emission_type": "domain_emission",
    }
    assert unknown.emits == ("slice.unknown_present",)
    text = seed_local.format_emitter_consumer_audit(audit)
    assert "Emitter: producer" in text
    assert "slice.scanned_orphan" in text
    assert "Status: partially_consumed" in text
    assert "Emitter: unknown" in text


def test_final_audit_assembly_preserves_rows_sorting_metadata_public_outputs_and_visibility():
    scanned_rows = [
        EmitterConsumerItem(
            emitter="producer_z",
            emits=("slice.z",),
            consumers=("diagnostics and audits",),
            status="orphaned",
            evidence=("seed_runtime/producer_z.py:2",),
        ),
        EmitterConsumerItem(
            emitter="producer_a",
            emits=("slice.a",),
            consumers=("CLI surfaces",),
            status="consumed",
            evidence=("scripts/seed_local.py:3",),
        ),
    ]
    unknown_rows = [
        EmitterConsumerItem(
            emitter="unknown",
            emits=("slice.missing",),
            consumers=("read models",),
            status="unknown",
        )
    ]

    ledger = EventLedger()
    before = ledger.list_events()
    audit = _assemble_emitter_consumer_audit(
        scanned_rows, unknown_rows, include_rendered=True
    )
    after = ledger.list_events()

    assert before == after == []
    assert [item.emitter for item in audit.items] == [
        "producer_a",
        "producer_z",
        "unknown",
    ]
    assert audit.metadata == {
        "discovery": "AST scan of event ledger append literals, Event(...) kind literals, and event.kind comparisons; rendered strings are excluded unless include_rendered is true.",
        "include_rendered": True,
        "scope": ["seed_runtime", "scripts"],
    }
    assert audit.to_json_dict() == {
        "summary": {
            "items_scanned": 3,
            "consumed": 1,
            "orphaned": 1,
            "partially_consumed": 0,
            "unknown": 1,
        },
        "items": [item.to_json_dict() for item in audit.items],
        "metadata": audit.metadata,
    }
    text = seed_local.format_emitter_consumer_audit(audit)
    assert "Emitter/Consumer Audit" in text
    assert "Items scanned: 3" in text
    assert "Emitter: producer_a" in text
    assert "Emitter: unknown" in text

    inventory_entry = next(
        entry for entry in DIAGNOSTIC_INVENTORY if entry.name == "emitter_consumer_audit"
    )
    assert inventory_entry.cli_flags == ("--emitter-consumer-audit", "--include-rendered")
    assert inventory_entry.uses_repo_files is True
    assert inventory_entry.supports_json is True
    assert inventory_entry.supports_record is False
    assert inventory_entry.record_scope == "none"
    assert inventory_entry.writes_event_ledger is False
    assert inventory_entry.mutates_cluster is False

    shape_rows = build_diagnostic_shape_audit()
    shape_by_field = {
        row.field: row
        for row in shape_rows
        if row.diagnostic == "emitter_consumer_audit"
    }
    assert shape_by_field["supports_json"].status == "consistent"
    assert shape_by_field["uses_repo_files"].status == "consistent"
    assert shape_by_field["writes_event_ledger"].status == "consistent"
    assert shape_by_field["mutates_cluster"].status == "consistent"
