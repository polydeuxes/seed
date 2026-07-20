import json

import scripts.seed_local as seed_local
from seed_runtime.component_audit import build_component_audit, format_component_audit
from seed_runtime.diagnostic_inventory import DIAGNOSTIC_INVENTORY
from seed_runtime.diagnostic_shape_audit import build_diagnostic_shape_audit


def test_component_audit_renders(capsys):
    assert seed_local.main(["--component-audit", "selection_path"]) == 0
    out = capsys.readouterr().out
    assert "Component Audit" in out
    assert "selection_path" in out
    assert "Boundary:" in out


def test_component_audit_json_is_valid(capsys):
    assert seed_local.main(["--component-audit", "selection_path", "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["component"] == "selection_path"
    assert payload["boundary"] == {
        "read_only": True,
        "writes_event_ledger": False,
        "mutates_cluster": False,
    }


def test_component_audit_surfaces_definitions_references_and_tests():
    audit = build_component_audit("selection_path")
    assert audit.definitions
    assert any("selection_path" in path for path in audit.definitions)
    assert audit.references
    assert any(path.startswith("tests/") for path in audit.tests)


def test_component_audit_surfaces_consumers_or_absence_and_graph_absence():
    audit = build_component_audit("selection_path")
    assert isinstance(audit.consumers, tuple)
    assert audit.operational_graph["observed"] in {True, False}
    text = format_component_audit(audit)
    assert "Consumers:" in text
    assert "Operational Graph:" in text


def test_component_audit_weak_evidence_is_unknown(tmp_path):
    (tmp_path / "README.md").write_text("unrelated repository\n")
    audit = build_component_audit("not_a_real_component", tmp_path)
    assert audit.status == "unknown"


def test_component_audit_emits_no_lifecycle_recommendation():
    text = format_component_audit(build_component_audit("selection_path"))
    lowered = text.lower()
    forbidden = ["recommend deletion", "recommend removal", "recommend replacement", "recommend reconnection", "recommend redesign", "deprecate this"]
    assert not any(term in lowered for term in forbidden)


def test_component_audit_does_not_write_event_ledger_or_mutate_cluster():
    audit = build_component_audit("selection_path")
    assert audit.boundary["writes_event_ledger"] is False
    assert audit.boundary["mutates_cluster"] is False


def test_component_audit_registered_in_diagnostic_inventory_and_shape_audit():
    entry = next(e for e in DIAGNOSTIC_INVENTORY if e.name == "component_audit")
    assert entry.supports_json is True
    assert entry.supports_record is False
    assert entry.writes_event_ledger is False
    assert entry.mutates_cluster is False
    rows = [r for r in build_diagnostic_shape_audit() if r.diagnostic == "component_audit"]
    assert rows
    assert {row.field for row in rows} >= {"supports_json", "writes_event_ledger", "mutates_cluster"}
