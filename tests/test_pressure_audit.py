import importlib.util
import json
import sys
from pathlib import Path

from seed_runtime.capability_needs import CapabilityNeedEntry
from seed_runtime.consumer_dependency_audit import ConsumerAudit, ConsumerAuditItem
from seed_runtime.diagnostic_shape_audit import (
    DiagnosticShapeAuditRow,
    DiagnosticShapeAuditSummary,
)
from seed_runtime.ownership_discrepancies import OwnershipDiscrepancyRow
from seed_runtime.pressure_audit import (
    _PressureItemCandidate,
    _admitted_pressure_items,
    _capability_pressure_evidence,
    _consumer_predicate_pressures,
    _diagnostic_shape_audit_root,
    _diagnostic_shape_audit_summary,
    _diagnostic_shape_pressure_evidence,
    _diagnostic_shape_pressure_score,
    _display_collection_evidence,
    _display_mapping_evidence,
    _display_scalar_evidence,
    _format_pressure_item_section,
    _fragile_predicate_pressure_evidence,
    _orphaned_predicate_pressure_evidence,
    _ownership_pressure,
    _ownership_pressure_evidence,
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


def test_diagnostic_shape_audit_summary_is_owned_by_local_helper(monkeypatch, tmp_path):
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    (repo_root / "scripts").mkdir()
    (repo_root / "scripts" / "seed_local.py").write_text("# local cli\n")
    rows = [
        DiagnosticShapeAuditRow("example", "supports_json", True, False, "mismatch"),
        DiagnosticShapeAuditRow("example", "uses_repo_files", True, None, "unknown"),
        DiagnosticShapeAuditRow("stable", "supports_json", True, True, "consistent"),
    ]
    calls = []

    def fake_shape_audit(repo_root=None):
        calls.append(repo_root)
        return rows

    monkeypatch.setattr(
        "seed_runtime.pressure_audit.build_diagnostic_shape_audit", fake_shape_audit
    )

    summary = _diagnostic_shape_audit_summary(repo_root)

    assert calls == [repo_root]
    assert summary == DiagnosticShapeAuditSummary(
        diagnostics_audited=2,
        consistent=1,
        warnings=0,
        mismatches=1,
        unknown=1,
    )


def test_diagnostic_shape_pressure_score_is_owned_by_local_helper():
    summary = DiagnosticShapeAuditSummary(
        diagnostics_audited=9,
        consistent=4,
        warnings=2,
        mismatches=1,
        unknown=2,
    )

    assert _diagnostic_shape_pressure_score(summary) == 5


def test_diagnostic_shape_pressure_evidence_is_owned_by_local_helper():
    summary = DiagnosticShapeAuditSummary(
        diagnostics_audited=7,
        consistent=3,
        warnings=2,
        mismatches=1,
        unknown=1,
    )

    assert _diagnostic_shape_pressure_evidence(summary) == {
        "mismatches": 1,
        "warnings": 2,
        "unknowns": 1,
    }


def test_diagnostic_shape_audit_root_is_owned_by_local_helper(tmp_path):
    repo_root = tmp_path / "repo"
    repo_root.mkdir()

    assert _diagnostic_shape_audit_root(repo_root) is None

    (repo_root / "scripts").mkdir()
    (repo_root / "scripts" / "seed_local.py").write_text("# local cli\n")

    assert _diagnostic_shape_audit_root(repo_root) == repo_root


def test_ownership_pressure_evidence_is_owned_by_local_helper():
    rows = [
        _ownership_row(),
        _ownership_row("svc-b", kind="storage", conflict="multiple_candidates"),
        _ownership_row("svc-c", conflict="owner_not_observed"),
    ]

    assert _ownership_pressure_evidence(rows) == {
        "service ambiguities": 2,
        "storage ambiguities": 1,
        "conflict counts": {
            "multiple_candidates": 1,
            "owner_not_observed": 2,
        },
        "dominant conflict": "owner_not_observed",
    }


def test_capability_pressure_evidence_is_owned_by_local_helper():
    entries = [
        CapabilityNeedEntry(
            capability="container_inventory",
            subjects={"svc-b", "svc-a"},
            diagnostics={"ownership_discrepancies"},
        ),
        CapabilityNeedEntry(
            capability="listener_process_inventory",
            subjects={"svc-a"},
            diagnostics={"listener_endpoint_reachability"},
        ),
    ]

    assert _capability_pressure_evidence(entries) == {
        "capability need frequency": {
            "container_inventory": 2,
            "listener_process_inventory": 1,
        },
        "affected subjects": ["svc-a", "svc-b"],
        "affected diagnostics": [
            "listener_endpoint_reachability",
            "ownership_discrepancies",
        ],
    }


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


def test_orphaned_predicate_pressure_evidence_is_owned_by_local_helper():
    items = [
        ConsumerAuditItem("unused_predicate", "observation_predicate", ()),
        ConsumerAuditItem("another_unused", "observation_predicate", ()),
    ]

    assert _orphaned_predicate_pressure_evidence(items) == {
        "orphan count": 2,
        "predicates": ["unused_predicate", "another_unused"],
    }


def test_fragile_predicate_pressure_evidence_is_owned_by_local_helper():
    items = [
        ConsumerAuditItem(
            "single_predicate", "observation_predicate", ("seed_runtime/state.py",)
        ),
        ConsumerAuditItem(
            "another_single", "observation_predicate", ("seed_runtime/cli.py",)
        ),
    ]

    assert _fragile_predicate_pressure_evidence(items) == {
        "single-consumer predicates": 2,
        "predicates": ["single_predicate", "another_single"],
    }


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


def test_pressure_item_section_formatting_is_owned_by_local_helper():
    item = _PressureItemCandidate(
        category="Example",
        score=7,
        evidence={"count": 2, "labels": ["alpha", "beta"]},
        reason="Example reason.",
        recommended_command="seed --example",
    ).to_pressure_item()

    assert _format_pressure_item_section(3, item) == [
        "3. Example",
        "",
        "Score: 7",
        "",
        "Evidence:",
        "  count: 2",
        "  labels: alpha, beta",
        "",
        "Reason: Example reason.",
        "Recommended inspection: seed --example",
        "",
    ]


def test_mapping_evidence_display_is_owned_by_local_helper():
    assert _display_mapping_evidence({"alpha": 1, "beta": "two"}) == "alpha=1, beta=two"
    assert _display_mapping_evidence({}) == "none"


def test_collection_evidence_display_is_owned_by_local_helper():
    assert _display_collection_evidence(["alpha", 2, "gamma"]) == "alpha, 2, gamma"
    assert _display_collection_evidence(()) == "none"


def test_scalar_evidence_display_is_owned_by_local_helper():
    assert _display_scalar_evidence("alpha") == "alpha"
    assert _display_scalar_evidence(3) == "3"
    assert _display_scalar_evidence(None) == "None"


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
