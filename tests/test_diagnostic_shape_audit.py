import json

import scripts.seed_local as seed_local
from seed_runtime.diagnostic_inventory import DiagnosticInventoryEntry
from seed_runtime.diagnostic_shape_audit import (
    DiagnosticImplementationSpec,
    DiagnosticShapeAuditRow,
    build_diagnostic_shape_audit,
    diagnostic_shape_audit_json,
    format_diagnostic_shape_audit,
    summarize_diagnostic_shape_audit,
)


def _row(rows, diagnostic, field):
    return next(
        row for row in rows if row.diagnostic == diagnostic and row.field == field
    )


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
    assert (
        _row(rows, "knowledge_reachability", "uses_repo_files").status == "consistent"
    )
    assert (
        _row(rows, "capability_needs", "reads_diagnostic_facts").status == "consistent"
    )
    assert (
        _row(rows, "observation_utilization", "uses_repo_files").status == "consistent"
    )
    assert _row(rows, "consumer_audit", "uses_repo_files").status == "consistent"


def test_mismatched_fixture_reports_mismatch(tmp_path):
    (tmp_path / "scripts").mkdir()
    (tmp_path / "scripts" / "seed_local.py").write_text("", encoding="utf-8")
    (tmp_path / "synthetic.py").write_text(
        "def build_synthetic(state):\n    return []\n", encoding="utf-8"
    )
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

    assert (
        _row(rows, "classification_coverage", "record_scope").observed
        == "diagnostic_run"
    )
    assert _row(rows, "classification_coverage", "record_scope").status == "consistent"
    assert (
        _row(rows, "ownership_discrepancies", "record_scope").observed
        == "diagnostic_run"
    )
    assert _row(rows, "ownership_discrepancies", "record_scope").status == "consistent"


def test_json_capable_diagnostics_validate_json_support():
    rows = build_diagnostic_shape_audit()

    for diagnostic in [
        "ownership_discrepancies",
        "capability_needs",
        "knowledge_reachability",
        "observation_utilization",
        "consumer_audit",
    ]:
        row = _row(rows, diagnostic, "supports_json")
        assert row.observed is True
        assert row.status == "consistent"


def test_capability_needs_validates_diagnostic_fact_reads():
    row = _row(
        build_diagnostic_shape_audit(), "capability_needs", "reads_diagnostic_facts"
    )

    assert row.observed is True
    assert row.status == "consistent"


def test_knowledge_reachability_validates_repo_file_usage():
    row = _row(
        build_diagnostic_shape_audit(), "knowledge_reachability", "uses_repo_files"
    )

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
        (
            _entry(
                supports_record=False, supports_json=True, uses_projected_state=False
            ),
        ),
        implementation_specs={
            "synthetic": DiagnosticImplementationSpec(
                name="synthetic", module_path="missing.py"
            )
        },
        repo_root=tmp_path,
    )

    summary = summarize_diagnostic_shape_audit(rows)
    assert summary.diagnostics_audited == 1
    assert summary.consistent == sum(row.status == "consistent" for row in rows)
    assert summary.mismatches == sum(row.status == "mismatch" for row in rows)
    assert summary.unknown == 0
    assert "Diagnostics audited: 1" in format_diagnostic_shape_audit(rows)
    assert diagnostic_shape_audit_json(rows)[0]["diagnostic"] == "synthetic"


def test_mismatch_filter_only_shows_mismatch_rows():
    rows = [
        _row_fixture("alpha", "supports_json", "consistent"),
        _row_fixture("alpha", "supports_record", "mismatch"),
        _row_fixture("beta", "record_scope", "mismatch"),
    ]

    output = format_diagnostic_shape_audit(rows, status="mismatch")

    assert "Filter: status=mismatch" in output
    assert "supports_record" in output
    assert "record_scope" in output
    assert "supports_json" not in output
    assert "status: consistent" not in output
    assert output.count("status: mismatch") == 2
    assert "Consistent: 1" in output
    assert "Mismatches: 2" in output
    assert "Filtered rows: 2" in output


def test_json_mismatch_filter_only_returns_mismatch_rows():
    rows = [
        _row_fixture("alpha", "supports_json", "consistent"),
        _row_fixture("alpha", "supports_record", "mismatch"),
    ]

    payload = diagnostic_shape_audit_json(rows, status="mismatch")

    assert [item["field"] for item in payload] == ["supports_record"]
    assert {item["status"] for item in payload} == {"mismatch"}


def test_warning_and_unknown_status_filters_work():
    rows = [
        _row_fixture("alpha", "supports_json", "warning"),
        _row_fixture("alpha", "supports_record", "unknown"),
        _row_fixture("alpha", "record_scope", "mismatch"),
    ]

    warning_output = format_diagnostic_shape_audit(rows, status="warning")
    unknown_payload = diagnostic_shape_audit_json(rows, status="unknown")

    assert "supports_json" in warning_output
    assert "supports_record" not in warning_output
    assert "Filtered rows: 1" in warning_output
    assert [item["field"] for item in unknown_payload] == ["supports_record"]
    assert unknown_payload[0]["status"] == "unknown"


def test_no_match_status_filter_output_is_sane():
    rows = [_row_fixture("alpha", "supports_json", "consistent")]

    output = format_diagnostic_shape_audit(rows, status="warning")

    assert "No diagnostic shape audit rows matched status=warning." in output
    assert "Diagnostics audited: 1" in output
    assert "Filtered rows: 0" in output


def test_default_diagnostic_shape_audit_output_is_unchanged_by_filter_support():
    rows = [_row_fixture("alpha", "supports_json", "consistent")]

    output = format_diagnostic_shape_audit(rows)

    assert "Filter:" not in output
    assert "Filtered rows:" not in output
    assert "supports_json" in output
    assert "status: consistent" in output


def test_cli_mismatches_filter_shows_only_mismatch_rows_and_filtered_count(capsys):
    assert seed_local.main(["--diagnostic-shape-audit", "--mismatches"]) == 0

    output = capsys.readouterr().out

    assert "Filter: status=mismatch" in output
    assert "Filtered rows:" in output
    assert "status: consistent" not in output
    assert "Diagnostics audited:" in output
    assert "Mismatches:" in output


def test_cli_json_mismatch_filter_only_returns_mismatch_rows(capsys):
    assert (
        seed_local.main(["--diagnostic-shape-audit", "--json", "--status", "mismatch"])
        == 0
    )

    payload = json.loads(capsys.readouterr().out)

    assert payload
    assert {item["status"] for item in payload} == {"mismatch"}


def _row_fixture(diagnostic, field, status):
    return DiagnosticShapeAuditRow(
        diagnostic=diagnostic,
        field=field,
        declared=True,
        observed=False if status == "mismatch" else True,
        status=status,
    )
