import importlib.util
import json
import sys
from pathlib import Path

from seed_runtime.consumer_dependency_audit import ConsumerAudit, ConsumerAuditItem
from seed_runtime.diagnostic_shape_audit import DiagnosticShapeAuditRow
from seed_runtime.ownership_discrepancies import OwnershipDiscrepancyRow
from seed_runtime.pressure_audit import build_pressure_audit, format_pressure_audit
from seed_runtime.state import State

ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "seed_local.py"


def load_seed_local():
    spec = importlib.util.spec_from_file_location("seed_local_pressure", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def _ownership_row(subject="svc-a", kind="service", conflict="owner_not_observed"):
    return OwnershipDiscrepancyRow(
        subject=subject,
        kind=kind,
        candidate_owner="node-a",
        confidence=0.5,
        evidence_count=1,
        conflict=conflict,
        reason="ambiguous",
        evidence=[],
    )


def test_pressure_audit_renders_json_and_evidence_backed_ranking(monkeypatch, capsys):
    seed_local = load_seed_local()
    monkeypatch.setattr(
        seed_local,
        "build_pressure_audit",
        lambda state, repo_root=None: build_pressure_audit(state, repo_root=repo_root),
    )
    monkeypatch.setattr(
        "seed_runtime.pressure_audit.build_ownership_discrepancies",
        lambda state: [_ownership_row(), _ownership_row("svc-b")],
    )
    monkeypatch.setattr(
        "seed_runtime.pressure_audit.build_capability_needs", lambda state: []
    )
    monkeypatch.setattr(
        "seed_runtime.pressure_audit.build_diagnostic_shape_audit",
        lambda repo_root=None: [],
    )
    monkeypatch.setattr(
        "seed_runtime.pressure_audit.build_consumer_audit",
        lambda root: ConsumerAudit(items=(), metadata={}),
    )

    assert seed_local.main(["--pressure-audit"]) == 0
    output = capsys.readouterr().out
    assert "Pressure Audit" in output
    assert "1. Ownership Attribution" in output
    assert "Score: 2" in output
    assert "service ambiguities: 2" in output
    assert "Recommended inspection: seed --ownership-discrepancies" in output

    assert seed_local.main(["--pressure-audit", "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["pressures"][0]["category"] == "Ownership Attribution"
    assert payload["pressures"][0]["score"] == 2
    assert payload["pressures"][0]["evidence"]["service ambiguities"] == 2
    assert (
        payload["pressures"][0]["recommended_command"]
        == "seed --ownership-discrepancies"
    )


def test_pressure_categories_appear_from_existing_surface_evidence(monkeypatch):
    class Need:
        capability = "container_inventory"
        subjects = {"svc-a", "svc-b"}
        diagnostics = {"ownership_discrepancies"}
        needed_evidence = {"container_inventory"}

    consumer = ConsumerAudit(
        items=(
            ConsumerAuditItem("unused_predicate", "observation_predicate", ()),
            ConsumerAuditItem(
                "single_predicate", "observation_predicate", ("seed_runtime/state.py",)
            ),
        ),
        metadata={},
    )
    shape_rows = [
        DiagnosticShapeAuditRow("example", "supports_json", True, False, "mismatch"),
        DiagnosticShapeAuditRow("example", "uses_repo_files", True, None, "unknown"),
    ]
    monkeypatch.setattr(
        "seed_runtime.pressure_audit.build_ownership_discrepancies",
        lambda state: [_ownership_row()],
    )
    monkeypatch.setattr(
        "seed_runtime.pressure_audit.build_capability_needs", lambda state: [Need()]
    )
    monkeypatch.setattr(
        "seed_runtime.pressure_audit.build_consumer_audit", lambda root: consumer
    )
    monkeypatch.setattr(
        "seed_runtime.pressure_audit.build_diagnostic_shape_audit",
        lambda repo_root=None: shape_rows,
    )

    audit = build_pressure_audit(State(workspace_id="ws"), repo_root=ROOT)
    categories = {item.category: item for item in audit.pressures}
    assert categories["Diagnostic Shape"].evidence["mismatches"] == 1
    assert categories["Diagnostic Shape"].evidence["unknowns"] == 1
    assert (
        categories["Ownership Attribution"].evidence["dominant conflict"]
        == "owner_not_observed"
    )
    assert categories["Capability"].evidence["capability need frequency"] == {
        "container_inventory": 2
    }
    assert categories["Orphaned Predicates"].evidence["orphan count"] == 1
    assert categories["Fragile Predicates"].evidence["single-consumer predicates"] == 1
    assert all(
        item.recommended_command.startswith("seed --") for item in audit.pressures
    )


def test_pressure_audit_empty_state_is_sane_and_read_only(monkeypatch, tmp_path):
    db = tmp_path / "seed.sqlite"
    seed_local = load_seed_local()
    monkeypatch.setattr(
        "seed_runtime.pressure_audit.build_ownership_discrepancies", lambda state: []
    )
    monkeypatch.setattr(
        "seed_runtime.pressure_audit.build_capability_needs", lambda state: []
    )
    monkeypatch.setattr(
        "seed_runtime.pressure_audit.build_diagnostic_shape_audit",
        lambda repo_root=None: [],
    )
    monkeypatch.setattr(
        "seed_runtime.pressure_audit.build_consumer_audit",
        lambda root: ConsumerAudit(items=(), metadata={}),
    )

    assert seed_local.main(["--db", str(db), "--pressure-audit"]) == 0
    rendered = format_pressure_audit(
        build_pressure_audit(State(workspace_id="ws"), repo_root=tmp_path)
    )
    assert "pressures identified: 0" in rendered
    ledger = seed_local.SQLiteEventLedger(str(db))
    try:
        assert ledger.list_events(seed_local.DEFAULT_WORKSPACE) == []
    finally:
        ledger.close()
