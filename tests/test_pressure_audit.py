import importlib.util
import json
import sys
from pathlib import Path

from seed_runtime.consumer_dependency_audit import ConsumerAudit, ConsumerAuditItem
from seed_runtime.diagnostic_shape_audit import DiagnosticShapeAuditRow
from seed_runtime.ownership_discrepancies import OwnershipDiscrepancyRow
from seed_runtime.pressure_audit import (
    _PressureItemCandidate,
    _admitted_pressure_items,
    _consumer_predicate_pressures,
    _ownership_pressure,
    build_pressure_audit,
    format_pressure_audit,
)
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


def test_pressure_item_candidate_converts_to_public_pressure_item_shape():
    candidate = _PressureItemCandidate(
        category="Example",
        score=3,
        evidence={"count": 3},
        reason="Example reason.",
        recommended_command="seed --example",
    )

    item = candidate.to_pressure_item()

    assert item.to_json_dict() == {
        "category": "Example",
        "score": 3,
        "evidence": {"count": 3},
        "reason": "Example reason.",
        "recommended_command": "seed --example",
    }


def test_admitted_pressure_items_filter_convert_and_order_candidates():
    admitted = _admitted_pressure_items(
        _PressureItemCandidate(
            category="Beta",
            score=3,
            evidence={"count": 3},
            reason="Beta reason.",
            recommended_command="seed --beta",
        ),
        None,
        _PressureItemCandidate(
            category="Alpha",
            score=3,
            evidence={"count": 3},
            reason="Alpha reason.",
            recommended_command="seed --alpha",
        ),
        _PressureItemCandidate(
            category="Zero",
            score=0,
            evidence={"count": 0},
            reason="Zero reason.",
            recommended_command="seed --zero",
        ),
        _PressureItemCandidate(
            category="Gamma",
            score=1,
            evidence={"count": 1},
            reason="Gamma reason.",
            recommended_command="seed --gamma",
        ),
    )

    assert [item.category for item in admitted] == ["Alpha", "Beta", "Gamma"]
    assert [item.score for item in admitted] == [3, 3, 1]
    assert all(item.recommended_command.startswith("seed --") for item in admitted)


def test_ownership_pressure_candidate_preserves_public_item_fields(monkeypatch):
    monkeypatch.setattr(
        "seed_runtime.pressure_audit.build_ownership_discrepancies",
        lambda state: [_ownership_row(), _ownership_row("svc-b")],
    )

    candidate = _ownership_pressure(State(workspace_id="ws"))

    assert candidate is not None
    item = candidate.to_pressure_item()
    assert item.category == "Ownership Attribution"
    assert item.score == 2
    assert item.evidence == {
        "service ambiguities": 2,
        "storage ambiguities": 0,
        "conflict counts": {"owner_not_observed": 2},
        "dominant conflict": "owner_not_observed",
    }
    assert item.reason == (
        "Ownership discrepancy audit reports 2 unresolved ownership row(s)."
    )
    assert item.recommended_command == "seed --ownership-discrepancies"


def test_consumer_predicate_pressures_builds_predicate_candidates_from_one_audit(
    monkeypatch,
):
    calls = []
    audit = ConsumerAudit(
        items=(
            ConsumerAuditItem("unused_predicate", "observation_predicate", ()),
            ConsumerAuditItem(
                "single_predicate", "observation_predicate", ("seed_runtime/state.py",)
            ),
            ConsumerAuditItem("non_predicate", "other", ()),
        ),
        metadata={},
    )

    def fake_consumer_audit(root):
        calls.append(root)
        return audit

    monkeypatch.setattr(
        "seed_runtime.pressure_audit.build_consumer_audit", fake_consumer_audit
    )

    orphaned, fragile = _consumer_predicate_pressures(ROOT)

    assert calls == [ROOT]
    assert orphaned is not None
    assert orphaned.category == "Orphaned Predicates"
    assert orphaned.evidence == {
        "orphan count": 1,
        "predicates": ["unused_predicate"],
    }
    assert fragile is not None
    assert fragile.category == "Fragile Predicates"
    assert fragile.evidence == {
        "single-consumer predicates": 1,
        "predicates": ["single_predicate"],
    }


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
