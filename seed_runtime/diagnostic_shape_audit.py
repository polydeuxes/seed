"""Static diagnostic shape self-audit."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

from seed_runtime.diagnostic_inventory import (
    DIAGNOSTIC_INVENTORY,
    DiagnosticInventoryEntry,
)

AuditStatus = Literal["consistent", "warning", "mismatch", "unknown"]
FILTERABLE_AUDIT_STATUSES: tuple[AuditStatus, ...] = (
    "consistent",
    "warning",
    "mismatch",
    "unknown",
)
AUDIT_FIELDS = (
    "supports_record",
    "supports_json",
    "record_scope",
    "emits_diagnostic_facts",
    "writes_event_ledger",
    "reads_diagnostic_facts",
    "uses_repo_files",
    "uses_projected_state",
    "mutates_cluster",
)


@dataclass(frozen=True)
class DiagnosticImplementationSpec:
    name: str
    module_path: str
    build_function: str | None = None
    format_function: str | None = None
    json_function: str | None = None
    record_function: str | None = None
    cli_flags: tuple[str, ...] = ()
    json_cli_flags: tuple[str, ...] = ()
    repo_file_markers: tuple[str, ...] = ()
    diagnostic_fact_read_markers: tuple[str, ...] = ()
    mutation_markers: tuple[str, ...] = (
        "subprocess.run",
        ".write_text(",
        "os.remove",
        "shutil.rmtree",
        "authorize_execution",
    )


@dataclass(frozen=True)
class DiagnosticShapeAuditRow:
    diagnostic: str
    field: str
    declared: bool | str
    observed: bool | str | None
    status: AuditStatus

    def to_json_dict(self) -> dict[str, Any]:
        return {
            "diagnostic": self.diagnostic,
            "field": self.field,
            "declared": _json_value(self.declared),
            "observed": _json_value(self.observed),
            "status": self.status,
        }


@dataclass(frozen=True)
class DiagnosticShapeAuditSummary:
    diagnostics_audited: int
    consistent: int
    warnings: int
    mismatches: int
    unknown: int


IMPLEMENTATION_SPECS: dict[str, DiagnosticImplementationSpec] = {
    "classification_coverage": DiagnosticImplementationSpec(
        name="classification_coverage",
        module_path="seed_runtime/classification_coverage.py",
        build_function="build_classification_coverage_diagnostic",
        format_function="format_classification_coverage",
        record_function="record_classification_coverage_diagnostic",
        cli_flags=("--classification-coverage",),
    ),
    "graph_issue_summary": DiagnosticImplementationSpec(
        name="graph_issue_summary",
        module_path="seed_runtime/state.py",
        cli_flags=("--graph-issue-summary",),
    ),
    "knowledge_reachability": DiagnosticImplementationSpec(
        name="knowledge_reachability",
        module_path="seed_runtime/knowledge_reachability.py",
        build_function="build_knowledge_reachability_audit_result",
        format_function="format_knowledge_reachability_table",
        json_function="knowledge_reachability_json",
        cli_flags=("--knowledge-reachability-audit",),
        json_cli_flags=("--knowledge-reachability-audit-json",),
        repo_file_markers=("repo_root", "repo_paths", "repository"),
    ),
    "ownership_discrepancies": DiagnosticImplementationSpec(
        name="ownership_discrepancies",
        module_path="seed_runtime/ownership_discrepancies.py",
        build_function="build_ownership_discrepancies",
        format_function="format_ownership_discrepancies",
        json_function="ownership_discrepancies_json",
        record_function="record_ownership_discrepancy_capability_needs",
        cli_flags=("--ownership-discrepancies",),
    ),
    "audit_snapshot": DiagnosticImplementationSpec(
        name="audit_snapshot",
        module_path="seed_runtime/audit_snapshots.py",
        build_function="create_audit_snapshot",
        cli_flags=("--audit-snapshot",),
        mutation_markers=("os.remove", "shutil.rmtree", "authorize_execution"),
    ),
    "audit_snapshots": DiagnosticImplementationSpec(
        name="audit_snapshots",
        module_path="seed_runtime/audit_snapshots.py",
        format_function="format_audit_snapshots",
        cli_flags=("--audit-snapshots",),
        mutation_markers=(
            ".write_text(",
            "subprocess.run",
            "os.remove",
            "shutil.rmtree",
            "authorize_execution",
        ),
    ),
    "audit_compare": DiagnosticImplementationSpec(
        name="audit_compare",
        module_path="seed_runtime/audit_snapshots.py",
        build_function="compare_audit_snapshots",
        format_function="format_audit_compare",
        cli_flags=("--audit-compare",),
        mutation_markers=(
            ".write_text(",
            "subprocess.run",
            "os.remove",
            "shutil.rmtree",
            "authorize_execution",
        ),
    ),
    "operational_surface_inventory": DiagnosticImplementationSpec(
        name="operational_surface_inventory",
        module_path="seed_runtime/operational_surface_inventory.py",
        build_function="build_operational_surface_inventory",
        format_function="format_operational_surface_inventory",
        json_function="operational_surface_inventory_json",
        cli_flags=("--operational-surface-inventory",),
    ),
    "visibility_coverage_audit": DiagnosticImplementationSpec(
        name="visibility_coverage_audit",
        module_path="seed_runtime/operational_surface_inventory.py",
        build_function="build_visibility_coverage_audit",
        format_function="format_visibility_coverage_audit",
        json_function="visibility_coverage_audit_json",
        cli_flags=("--visibility-coverage-audit",),
    ),
    "operational_surface_classification_audit": DiagnosticImplementationSpec(
        name="operational_surface_classification_audit",
        module_path="seed_runtime/operational_surface_inventory.py",
        build_function="build_operational_surface_classification_audit",
        format_function="format_operational_surface_classification_audit",
        json_function="operational_surface_classification_audit_json",
        cli_flags=("--operational-surface-classification-audit",),
    ),
    "consumer_audit": DiagnosticImplementationSpec(
        name="consumer_audit",
        module_path="seed_runtime/consumer_dependency_audit.py",
        build_function="build_consumer_audit",
        format_function="format_consumer_audit",
        json_function="consumer_audit_json",
        cli_flags=("--consumer-audit",),
        repo_file_markers=("CONSUMER_PATHS", "_read_sources"),
    ),
    "observation_utilization": DiagnosticImplementationSpec(
        name="observation_utilization",
        module_path="seed_runtime/observation_utilization.py",
        build_function="build_observation_utilization_audit",
        format_function="format_observation_utilization",
        json_function="observation_utilization_json",
        cli_flags=("--observation-utilization",),
        repo_file_markers=("PROJECTED_PATHS", "READ_MODEL_PATHS", "DIAGNOSTIC_PATHS"),
    ),
    "capability_needs": DiagnosticImplementationSpec(
        name="capability_needs",
        module_path="seed_runtime/capability_needs.py",
        build_function="build_capability_needs",
        format_function="format_capability_needs",
        json_function="capability_needs_json",
        cli_flags=("--capability-needs",),
        diagnostic_fact_read_markers=("diagnostic_run:", "diagnostic_capability_need"),
    ),
    "investigation_path": DiagnosticImplementationSpec(
        name="investigation_path",
        module_path="seed_runtime/investigation_path_audit.py",
        build_function="build_investigation_path_audit",
        format_function="format_investigation_path_audit",
        json_function="investigation_path_audit_json",
        cli_flags=("--investigation-path",),
    ),
    "ops_brief": DiagnosticImplementationSpec(
        name="ops_brief",
        module_path="seed_runtime/ops_brief.py",
        build_function="build_ops_brief",
        format_function="format_ops_brief",
        json_function="to_json_dict",
        cli_flags=("--ops-brief",),
        repo_file_markers=(
            "build_observation_inventory",
            "build_consumer_audit",
            "build_diagnostic_shape_audit",
            "list_audit_snapshots",
        ),
        diagnostic_fact_read_markers=("build_capability_needs",),
    ),
    "current_facts_cache_debug": DiagnosticImplementationSpec(
        name="current_facts_cache_debug",
        module_path="scripts/seed_local.py",
        build_function="_current_facts_timing_from_args",
        format_function="_format_current_facts_timing_report",
        cli_flags=("--current-facts-cache-debug",),
        mutation_markers=(
            "subprocess.run",
            ".write_text(",
            "os.remove",
            "shutil.rmtree",
            "authorize_execution",
            "ingest_observations",
        ),
    ),
    "impact_audit": DiagnosticImplementationSpec(
        name="impact_audit",
        module_path="seed_runtime/impact_audit.py",
        build_function="build_impact_audit",
        format_function="format_impact_audit",
        json_function="impact_audit_json",
        cli_flags=("--impact-audit",),
        mutation_markers=(
            ".write_text(",
            "subprocess.run",
            "os.remove",
            "shutil.rmtree",
            "authorize_execution",
        ),
    ),
    "pressure_audit": DiagnosticImplementationSpec(
        name="pressure_audit",
        module_path="seed_runtime/pressure_audit.py",
        build_function="build_pressure_audit",
        format_function="format_pressure_audit",
        json_function="pressure_audit_json",
        cli_flags=("--pressure-audit",),
        repo_file_markers=(
            "build_consumer_audit",
            "build_diagnostic_shape_audit",
        ),
        diagnostic_fact_read_markers=("build_capability_needs",),
    ),
    "correlation_audit": DiagnosticImplementationSpec(
        name="correlation_audit",
        module_path="seed_runtime/correlation_audit.py",
        build_function="build_correlation_audit",
        format_function="format_correlation_audit",
        json_function="correlation_audit_json",
        cli_flags=("--correlation-audit",),
        repo_file_markers=("build_consumer_audit",),
        diagnostic_fact_read_markers=("build_capability_needs",),
    ),
    "privilege_discovery": DiagnosticImplementationSpec(
        name="privilege_discovery",
        module_path="seed_runtime/privilege_discovery.py",
        build_function="build_privilege_discovery",
        format_function="format_privilege_discovery",
        json_function="privilege_discovery_json",
        cli_flags=("--privilege-discovery",),
        diagnostic_fact_read_markers=("build_capability_needs",),
    ),
}


def build_diagnostic_shape_audit(
    entries: tuple[DiagnosticInventoryEntry, ...] = DIAGNOSTIC_INVENTORY,
    *,
    implementation_specs: dict[
        str, DiagnosticImplementationSpec
    ] = IMPLEMENTATION_SPECS,
    repo_root: Path | None = None,
) -> list[DiagnosticShapeAuditRow]:
    root = repo_root or Path(__file__).resolve().parents[1]
    cli_source = _read(root / "scripts" / "seed_local.py")
    rows: list[DiagnosticShapeAuditRow] = []
    for entry in entries:
        spec = implementation_specs.get(entry.name)
        observed = _observe(entry, spec, root, cli_source) if spec else {}
        for field in AUDIT_FIELDS:
            declared = getattr(entry, field)
            value = observed.get(field)
            rows.append(
                DiagnosticShapeAuditRow(
                    diagnostic=entry.name,
                    field=field,
                    declared=declared,
                    observed=value,
                    status=_status(declared, value),
                )
            )
    return rows


def filter_diagnostic_shape_audit_rows(
    rows: list[DiagnosticShapeAuditRow], status: AuditStatus | None = None
) -> list[DiagnosticShapeAuditRow]:
    if status is None:
        return rows
    return [row for row in rows if row.status == status]


def diagnostic_shape_audit_json(
    rows: list[DiagnosticShapeAuditRow],
    *,
    status: AuditStatus | None = None,
) -> list[dict[str, Any]]:
    return [
        row.to_json_dict() for row in filter_diagnostic_shape_audit_rows(rows, status)
    ]


def summarize_diagnostic_shape_audit(
    rows: list[DiagnosticShapeAuditRow],
) -> DiagnosticShapeAuditSummary:
    diagnostics = {row.diagnostic for row in rows}
    return DiagnosticShapeAuditSummary(
        diagnostics_audited=len(diagnostics),
        consistent=sum(row.status == "consistent" for row in rows),
        warnings=sum(row.status == "warning" for row in rows),
        mismatches=sum(row.status == "mismatch" for row in rows),
        unknown=sum(row.status == "unknown" for row in rows),
    )


def format_diagnostic_shape_audit(
    rows: list[DiagnosticShapeAuditRow],
    *,
    status: AuditStatus | None = None,
) -> str:
    filtered_rows = filter_diagnostic_shape_audit_rows(rows, status)
    lines = ["Diagnostic Shape Audit", ""]
    if status is not None:
        lines.append(f"Filter: status={status}")
        lines.append("")
    if status is not None and not filtered_rows:
        lines.append(f"No diagnostic shape audit rows matched status={status}.")
    current = None
    for row in filtered_rows:
        if row.diagnostic != current:
            current = row.diagnostic
            lines.append(row.diagnostic)
        lines.extend(
            [
                f"  {row.field}",
                f"    declared: {_display(row.declared)}",
                f"    observed: {_display(row.observed)}",
                f"    status: {row.status}",
            ]
        )
    summary = summarize_diagnostic_shape_audit(rows)
    summary_lines = [
        "",
        f"Diagnostics audited: {summary.diagnostics_audited}",
        f"Consistent: {summary.consistent}",
        f"Warnings: {summary.warnings}",
        f"Mismatches: {summary.mismatches}",
        f"Unknown: {summary.unknown}",
    ]
    if status is not None:
        summary_lines.append(f"Filtered rows: {len(filtered_rows)}")
    lines.extend(summary_lines)
    return "\n".join(lines)


def _observe(
    entry: DiagnosticInventoryEntry,
    spec: DiagnosticImplementationSpec,
    root: Path,
    cli_source: str,
) -> dict[str, bool | str | None]:
    module_source = _read(root / spec.module_path)
    record_source = (
        _function_source(cli_source, spec.record_function)
        if spec.record_function
        else ""
    )
    implementation_source = _implementation_source(module_source, spec)
    cli_surface_source = _cli_surface_source(cli_source, spec.cli_flags)
    has_json_renderer = bool(spec.json_function and spec.json_function in module_source)
    has_direct_json_output = (
        "args.json_output" in cli_surface_source and "json.dumps" in cli_surface_source
    )
    has_json_path = (
        bool(
            spec.json_cli_flags
            and all(flag in cli_source for flag in spec.json_cli_flags)
        )
        or bool(has_json_renderer and "args.json_output" in cli_surface_source)
        or has_direct_json_output
    )
    record_scope = None
    if record_source:
        protected = (
            'subject="node115"',
            'subject="node116"',
            'subject="filesystem"',
            'subject="service"',
            'subject="host"',
        )
        if "diagnostic_run:" in record_source and not any(
            marker in record_source for marker in protected
        ):
            record_scope = "diagnostic_run"
        elif any(marker in record_source for marker in protected):
            record_scope = "cluster_subject"
    return {
        "supports_record": bool(
            spec.record_function and spec.record_function in cli_source
        ),
        "supports_json": bool(has_json_path),
        "record_scope": record_scope or "none",
        "emits_diagnostic_facts": "DevObservationSeed" in record_source
        and ("diagnostic_" in record_source or "record_facts" in record_source),
        "writes_event_ledger": "ingest_observations" in record_source
        and "EventLedger" in record_source,
        "reads_diagnostic_facts": (
            all(marker in module_source for marker in spec.diagnostic_fact_read_markers)
            if spec.diagnostic_fact_read_markers
            else False
        ),
        "uses_repo_files": (
            any(marker in module_source for marker in spec.repo_file_markers)
            if spec.repo_file_markers
            else False
        ),
        "uses_projected_state": "State" in implementation_source
        or "projected_state_from_args" in cli_surface_source,
        "mutates_cluster": any(
            marker in implementation_source for marker in spec.mutation_markers
        ),
    }


def _implementation_source(
    module_source: str, spec: DiagnosticImplementationSpec
) -> str:
    """Return the implementation slice owned by one diagnostic surface.

    The audit is intentionally static, but it must not attribute every marker in a
    shared module to every surface in that module.  Snapshot creation, listing,
    and comparison live together, so broad module scans confused local artifact
    writes with compare/list behavior.
    """
    parts = []
    for function_name in (
        spec.build_function,
        spec.format_function,
        spec.json_function,
        spec.record_function,
    ):
        if function_name:
            parts.append(_function_source(module_source, function_name))
    return "\n".join(part for part in parts if part) or module_source


def _cli_surface_source(cli_source: str, cli_flags: tuple[str, ...]) -> str:
    parts = []
    for flag in cli_flags:
        attr = flag.lstrip("-").replace("-", "_")
        marker = f"if args.{attr}"
        start = 0
        while True:
            start = cli_source.find(marker, start)
            if start < 0:
                break
            next_if = cli_source.find("\n    if args.", start + len(marker))
            parts.append(
                cli_source[start:] if next_if < 0 else cli_source[start:next_if]
            )
            start += len(marker)
    return "\n".join(parts)


def _status(declared: bool | str, observed: bool | str | None) -> AuditStatus:
    if observed is None:
        return "unknown"
    if declared == observed:
        return "consistent"
    if declared is False and observed in (None, "none"):
        return "consistent"
    return "mismatch"


def _function_source(source: str, function_name: str | None) -> str:
    if not function_name:
        return ""
    marker = f"def {function_name}("
    start = source.find(marker)
    if start < 0:
        return ""
    next_def = source.find("\ndef ", start + len(marker))
    return source[start:] if next_def < 0 else source[start:next_def]


def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


def _display(value: Any) -> str:
    if value is True:
        return "yes"
    if value is False:
        return "no"
    if value is None:
        return "unknown"
    return str(value)


def _json_value(value: Any) -> Any:
    if isinstance(value, bool) or value is None:
        return value
    return str(value)
