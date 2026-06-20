import json

import scripts.seed_local as seed_local
from seed_runtime.diagnostic_inventory import DiagnosticInventoryEntry
from seed_runtime.diagnostic_shape_audit import (
    DiagnosticImplementationSpec,
    build_diagnostic_shape_audit,
    diagnostic_shape_audit_json,
    format_diagnostic_shape_audit,
    summarize_diagnostic_shape_audit,
)


def _row(rows, diagnostic, field):
    return next(row for row in rows if row.diagnostic == diagnostic and row.field == field)


def _entry(**overrides):
    data = dict(
        name="synthetic",
        cli_flags=("--synthetic",),
        uses_projected_state=True,
        uses_repo_files=False,
        supports_json=False,
        supports_record=False,
        record_scope="none",
        emits_diagnostic_facts=False,
        emits_cluster_facts=False,
        writes_event_ledger=False,
        mutates_cluster=False,
        reads_diagnostic_facts=False,
        description="Synthetic fixture.",
    )
    data.update(overrides)
    return DiagnosticInventoryEntry(**data)


def test_matching_registry_declarations_report_consistent_for_current_diagnostics():
    rows = build_diagnostic_shape_audit()

    assert _row(rows, "ownership_discrepancies", "supports_json").status == "consistent"
    assert _row(rows, "knowledge_reachability", "uses_repo_files").status == "consistent"
    assert _row(rows, "capability_needs", "reads_diagnostic_facts").status == "consistent"


def test_mismatched_fixture_reports_mismatch(tmp_path):
    (tmp_path / "scripts").mkdir()
    (tmp_path / "scripts" / "seed_local.py").write_text("", encoding="utf-8")
    (tmp_path / "synthetic.py").write_text("def build_synthetic(state):\n    return []\n", encoding="utf-8")
    rows = build_diagnostic_shape_audit(
        (_entry(supports_json=True),),
        implementation_specs={
            "synthetic": DiagnosticImplementationSpec(
                name="synthetic",
                module_path="synthetic.py",
                build_function="build_synthetic",
                json_function="synthetic_json",
                cli_flags=("--synthetic",),
            )
        },
        repo_root=tmp_path,
    )

    assert _row(rows, "synthetic", "supports_json").status == "mismatch"


def test_record_enabled_diagnostics_validate_diagnostic_run_scoping():
    rows = build_diagnostic_shape_audit()

    assert _row(rows, "classification_coverage", "record_scope").observed == "diagnostic_run"
    assert _row(rows, "classification_coverage", "record_scope").status == "consistent"
    assert _row(rows, "ownership_discrepancies", "record_scope").observed == "diagnostic_run"
    assert _row(rows, "ownership_discrepancies", "record_scope").status == "consistent"


def test_json_capable_diagnostics_validate_json_support():
    rows = build_diagnostic_shape_audit()

    for diagnostic in ["ownership_discrepancies", "capability_needs", "knowledge_reachability"]:
        row = _row(rows, diagnostic, "supports_json")
        assert row.observed is True
        assert row.status == "consistent"


def test_capability_needs_validates_diagnostic_fact_reads():
    row = _row(build_diagnostic_shape_audit(), "capability_needs", "reads_diagnostic_facts")

    assert row.observed is True
    assert row.status == "consistent"


def test_knowledge_reachability_validates_repo_file_usage():
    row = _row(build_diagnostic_shape_audit(), "knowledge_reachability", "uses_repo_files")

    assert row.observed is True
    assert row.status == "consistent"


def test_cli_diagnostic_shape_audit_json_emits_valid_json(capsys):
    assert seed_local.main(["--diagnostic-shape-audit", "--json"]) == 0

    payload = json.loads(capsys.readouterr().out)

    assert isinstance(payload, list)
    assert {"diagnostic", "field", "declared", "observed", "status"} <= set(payload[0])
    assert any(item["diagnostic"] == "ownership_discrepancies" for item in payload)


def test_summary_counts_are_correct_for_fixture(tmp_path):
    (tmp_path / "scripts").mkdir()
    (tmp_path / "scripts" / "seed_local.py").write_text("", encoding="utf-8")
    rows = build_diagnostic_shape_audit(
        (_entry(supports_record=False, supports_json=True, uses_projected_state=False),),
        implementation_specs={"synthetic": DiagnosticImplementationSpec(name="synthetic", module_path="missing.py")},
        repo_root=tmp_path,
    )

    summary = summarize_diagnostic_shape_audit(rows)
    assert summary.diagnostics_audited == 1
    assert summary.consistent == sum(row.status == "consistent" for row in rows)
    assert summary.mismatches == sum(row.status == "mismatch" for row in rows)
    assert summary.unknown == 0
    assert "Diagnostics audited: 1" in format_diagnostic_shape_audit(rows)
    assert diagnostic_shape_audit_json(rows)[0]["diagnostic"] == "synthetic"
