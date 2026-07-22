from __future__ import annotations

import json

from seed_runtime.events import SQLiteEventLedger
from seed_runtime.rule_inventory import collect_rule_inventory
from seed_runtime.serialization import to_plain
from scripts import seed_local


def _entries_by_id():
    return {entry.id: entry for entry in collect_rule_inventory()}


def test_inventory_includes_predicate_catalog_entries():
    entries = _entries_by_id()

    assert "predicate.availability_status" in entries
    entry = entries["predicate.availability_status"]
    assert entry.category == "predicate_catalog"
    assert entry.source == "predicate_catalog/core.json"
    assert "current fact cardinality is single" in entry.then_effects
    assert entry.metadata["allowed_values"] == ["up", "down", "unknown"]


def test_inventory_includes_relationship_catalog_entries():
    entries = _entries_by_id()

    assert "relationship.monitored_by" in entries
    entry = entries["relationship.monitored_by"]
    assert entry.category == "relationship_catalog"
    assert entry.metadata["relationship_kind"] == "dependency"
    assert entry.metadata["derived_from_predicates"] == ["prometheus_instance"]
    assert "object is fixed to 'prometheus'" in entry.then_effects


def test_inventory_includes_inference_catalog_entries_if_present():
    entries = _entries_by_id()

    assert "inference.availability_down_health_degraded" in entries
    entry = entries["inference.availability_down_health_degraded"]
    assert entry.category == "inference_catalog"
    assert "fact predicate is 'availability_status'" in entry.if_conditions
    assert "infer predicate 'health_status'" in entry.then_effects


def test_inventory_output_is_deterministic_and_sorted():
    first = collect_rule_inventory()
    second = collect_rule_inventory()

    assert [entry.id for entry in first] == [entry.id for entry in second]
    assert [entry.category for entry in first] == sorted(entry.category for entry in first)
    assert json.dumps(to_plain(first), sort_keys=True) == json.dumps(
        to_plain(second), sort_keys=True
    )


def test_rules_cli_outputs_json_without_appending_ledger_events(tmp_path, capsys):
    db_path = tmp_path / "seed.sqlite"

    exit_code = seed_local.main(["--db", str(db_path), "--rules"])

    assert exit_code == 0
    payload = json.loads(capsys.readouterr().out)
    assert any(entry["id"] == "predicate.availability_status" for entry in payload)
    assert SQLiteEventLedger(str(db_path)).list("local") == []


def test_rules_cli_does_not_build_runtime_or_tool_executor(monkeypatch, capsys):

    exit_code = seed_local.main(["--rules"])

    assert exit_code == 0
    payload = json.loads(capsys.readouterr().out)
    assert any(entry["category"] == "capability_resolution" for entry in payload)
