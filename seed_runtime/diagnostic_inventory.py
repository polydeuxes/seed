"""Registry-backed visibility for operational diagnostic CLI surfaces."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Literal

RecordScope = Literal["none", "diagnostic_run"]


@dataclass(frozen=True)
class DiagnosticInventoryEntry:
    """Operational shape declaration for one diagnostic/test-like CLI surface."""

    name: str
    cli_flags: tuple[str, ...]
    uses_projected_state: bool
    uses_repo_files: bool
    supports_json: bool
    supports_record: bool
    record_scope: RecordScope
    emits_diagnostic_facts: bool
    emits_cluster_facts: bool
    writes_event_ledger: bool
    mutates_cluster: bool
    reads_diagnostic_facts: bool
    description: str

    def to_json_dict(self) -> dict[str, object]:
        data = asdict(self)
        data["cli_flags"] = list(self.cli_flags)
        return data


DIAGNOSTIC_INVENTORY: tuple[DiagnosticInventoryEntry, ...] = (
    DiagnosticInventoryEntry(
        name="classification_coverage",
        cli_flags=("--classification-coverage",),
        uses_projected_state=True,
        uses_repo_files=False,
        supports_json=False,
        supports_record=True,
        record_scope="diagnostic_run",
        emits_diagnostic_facts=True,
        emits_cluster_facts=False,
        writes_event_ledger=True,
        mutates_cluster=False,
        reads_diagnostic_facts=False,
        description="Reports projected entity classification coverage and unknown contributors.",
    ),
    DiagnosticInventoryEntry(
        name="graph_issue_summary",
        cli_flags=("--graph-issue-summary",),
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
        description="Reports grouped projected graph validation issues.",
    ),
    DiagnosticInventoryEntry(
        name="knowledge_reachability",
        cli_flags=(
            "--knowledge-reachability-audit",
            "--knowledge-reachability-audit-json",
        ),
        uses_projected_state=True,
        uses_repo_files=True,
        supports_json=True,
        supports_record=False,
        record_scope="none",
        emits_diagnostic_facts=False,
        emits_cluster_facts=False,
        writes_event_ledger=False,
        mutates_cluster=False,
        reads_diagnostic_facts=False,
        description="Audits knowledge reachability across projected, repository, inquiry, and rendered surfaces.",
    ),
    DiagnosticInventoryEntry(
        name="ownership_discrepancies",
        cli_flags=("--ownership-discrepancies",),
        uses_projected_state=True,
        uses_repo_files=False,
        supports_json=True,
        supports_record=True,
        record_scope="diagnostic_run",
        emits_diagnostic_facts=True,
        emits_cluster_facts=False,
        writes_event_ledger=True,
        mutates_cluster=False,
        reads_diagnostic_facts=False,
        description="Reports storage/service ownership candidates, conflicts, and capability needs.",
    ),
    DiagnosticInventoryEntry(
        name="audit_snapshot",
        cli_flags=("--audit-snapshot",),
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
        description="Saves local operational audit output and best-effort git metadata under .audit/seed/ without recording facts.",
    ),
    DiagnosticInventoryEntry(
        name="audit_snapshots",
        cli_flags=("--audit-snapshots",),
        uses_projected_state=False,
        uses_repo_files=False,
        supports_json=False,
        supports_record=False,
        record_scope="none",
        emits_diagnostic_facts=False,
        emits_cluster_facts=False,
        writes_event_ledger=False,
        mutates_cluster=False,
        reads_diagnostic_facts=False,
        description="Lists local operational audit snapshot artifacts from .audit/seed/.",
    ),
    DiagnosticInventoryEntry(
        name="audit_compare",
        cli_flags=("--audit-compare",),
        uses_projected_state=False,
        uses_repo_files=False,
        supports_json=True,
        supports_record=False,
        record_scope="none",
        emits_diagnostic_facts=False,
        emits_cluster_facts=False,
        writes_event_ledger=False,
        mutates_cluster=False,
        reads_diagnostic_facts=False,
        description="Compares two local operational audit snapshots without recording facts.",
    ),
    DiagnosticInventoryEntry(
        name="operational_surface_inventory",
        cli_flags=("--operational-surface-inventory",),
        uses_projected_state=False,
        uses_repo_files=False,
        supports_json=True,
        supports_record=False,
        record_scope="none",
        emits_diagnostic_facts=False,
        emits_cluster_facts=False,
        writes_event_ledger=False,
        mutates_cluster=False,
        reads_diagnostic_facts=False,
        description="Discovers operational CLI surfaces from argparse implementation evidence without recording facts or mutating cluster state.",
    ),
    DiagnosticInventoryEntry(
        name="visibility_coverage_audit",
        cli_flags=("--visibility-coverage-audit",),
        uses_projected_state=False,
        uses_repo_files=False,
        supports_json=True,
        supports_record=False,
        record_scope="none",
        emits_diagnostic_facts=False,
        emits_cluster_facts=False,
        writes_event_ledger=False,
        mutates_cluster=False,
        reads_diagnostic_facts=False,
        description="Compares implementation-discovered operational surfaces with diagnostic inventory visibility without recording facts or mutating cluster state.",
    ),
    DiagnosticInventoryEntry(
        name="operational_surface_classification_audit",
        cli_flags=("--operational-surface-classification-audit",),
        uses_projected_state=False,
        uses_repo_files=False,
        supports_json=True,
        supports_record=False,
        record_scope="none",
        emits_diagnostic_facts=False,
        emits_cluster_facts=False,
        writes_event_ledger=False,
        mutates_cluster=False,
        reads_diagnostic_facts=False,
        description="Classifies discovered CLI elements into primary surfaces, filters, modifiers, debug, manual-input, legacy, or unknown without recording facts or mutating cluster state.",
    ),
    DiagnosticInventoryEntry(
        name="consumer_audit",
        cli_flags=("--consumer-audit",),
        uses_projected_state=False,
        uses_repo_files=True,
        supports_json=True,
        supports_record=False,
        record_scope="none",
        emits_diagnostic_facts=False,
        emits_cluster_facts=False,
        writes_event_ledger=False,
        mutates_cluster=False,
        reads_diagnostic_facts=False,
        description="Audits implementation-backed consumers of observation predicates and diagnostic surfaces without recording facts.",
    ),
    DiagnosticInventoryEntry(
        name="emitter_consumer_audit",
        cli_flags=("--emitter-consumer-audit",),
        uses_projected_state=False,
        uses_repo_files=True,
        supports_json=True,
        supports_record=False,
        record_scope="none",
        emits_diagnostic_facts=False,
        emits_cluster_facts=False,
        writes_event_ledger=False,
        mutates_cluster=False,
        reads_diagnostic_facts=False,
        description="Audits implementation-backed emitted outputs and their visible consumers without recording facts or mutating cluster state.",
    ),
    DiagnosticInventoryEntry(
        name="observation_utilization",
        cli_flags=("--observation-utilization",),
        uses_projected_state=False,
        uses_repo_files=True,
        supports_json=True,
        supports_record=False,
        record_scope="none",
        emits_diagnostic_facts=False,
        emits_cluster_facts=False,
        writes_event_ledger=False,
        mutates_cluster=False,
        reads_diagnostic_facts=False,
        description=(
            "Audits implementation source participation of observation predicates "
            "across projection, read-model, and diagnostic surfaces without "
            "loading projected state."
        ),
    ),
    DiagnosticInventoryEntry(
        name="capability_needs",
        cli_flags=("--capability-needs",),
        uses_projected_state=True,
        uses_repo_files=False,
        supports_json=True,
        supports_record=False,
        record_scope="none",
        emits_diagnostic_facts=False,
        emits_cluster_facts=False,
        writes_event_ledger=False,
        mutates_cluster=False,
        reads_diagnostic_facts=True,
        description="Reads recorded diagnostic facts and reports capability needs by subject.",
    ),
    DiagnosticInventoryEntry(
        name="investigation_path",
        cli_flags=("--investigation-path",),
        uses_projected_state=False,
        uses_repo_files=False,
        supports_json=True,
        supports_record=False,
        record_scope="none",
        emits_diagnostic_facts=False,
        emits_cluster_facts=False,
        writes_event_ledger=False,
        mutates_cluster=False,
        reads_diagnostic_facts=False,
        description="Exposes evidence-backed read-only investigation paths across existing diagnostic surfaces without planning, recording, event ledger writes, or cluster mutation.",
    ),
    DiagnosticInventoryEntry(
        name="ops_brief",
        cli_flags=("--ops-brief",),
        uses_projected_state=True,
        uses_repo_files=True,
        supports_json=True,
        supports_record=False,
        record_scope="none",
        emits_diagnostic_facts=False,
        emits_cluster_facts=False,
        writes_event_ledger=False,
        mutates_cluster=False,
        reads_diagnostic_facts=True,
        description="Aggregates existing operational visibility surfaces into a read-only triage brief.",
    ),
    DiagnosticInventoryEntry(
        name="current_facts_cache_debug",
        cli_flags=("--current-facts-cache-debug",),
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
        description="Reports read-only current-facts cache and timing phases without recording facts or mutating cluster state.",
    ),
    DiagnosticInventoryEntry(
        name="impact_audit",
        cli_flags=("--impact-audit",),
        uses_projected_state=False,
        uses_repo_files=False,
        supports_json=True,
        supports_record=False,
        record_scope="none",
        emits_diagnostic_facts=False,
        emits_cluster_facts=False,
        writes_event_ledger=False,
        mutates_cluster=False,
        reads_diagnostic_facts=False,
        description="Compares existing operational audit snapshots, reports snapshot coverage, and classifies observable outcome impact without recording facts.",
    ),
    DiagnosticInventoryEntry(
        name="pressure_audit",
        cli_flags=("--pressure-audit",),
        uses_projected_state=True,
        uses_repo_files=True,
        supports_json=True,
        supports_record=False,
        record_scope="none",
        emits_diagnostic_facts=False,
        emits_cluster_facts=False,
        writes_event_ledger=False,
        mutates_cluster=False,
        reads_diagnostic_facts=True,
        description="Ranks operational pressure from existing visibility surfaces without recording facts or mutating cluster state.",
    ),
    DiagnosticInventoryEntry(
        name="correlation_audit",
        cli_flags=("--correlation-audit",),
        uses_projected_state=True,
        uses_repo_files=True,
        supports_json=True,
        supports_record=False,
        record_scope="none",
        emits_diagnostic_facts=False,
        emits_cluster_facts=False,
        writes_event_ledger=False,
        mutates_cluster=False,
        reads_diagnostic_facts=True,
        description="Correlates existing evidence, consumers, and pressure surfaces to expose suspected operational disconnects without recording facts.",
    ),
    DiagnosticInventoryEntry(
        name="privilege_discovery",
        cli_flags=("--privilege-discovery",),
        uses_projected_state=True,
        uses_repo_files=False,
        supports_json=True,
        supports_record=False,
        record_scope="none",
        emits_diagnostic_facts=False,
        emits_cluster_facts=False,
        writes_event_ledger=False,
        mutates_cluster=False,
        reads_diagnostic_facts=True,
        description="Explains privilege boundaries for current capability needs without privileged actions, fact recording, or cluster mutation.",
    ),
)


def diagnostic_inventory_json(
    entries: tuple[DiagnosticInventoryEntry, ...] = DIAGNOSTIC_INVENTORY,
) -> list[dict[str, object]]:
    return [entry.to_json_dict() for entry in entries]


def format_diagnostic_inventory(
    entries: tuple[DiagnosticInventoryEntry, ...] = DIAGNOSTIC_INVENTORY,
) -> str:
    headers = [
        "Diagnostic",
        "CLI Flag",
        "Uses State",
        "Uses Repo Files",
        "JSON",
        "Record",
        "Record Scope",
        "Emits Facts",
        "Mutates Cluster",
        "Notes",
    ]
    rows = [
        [
            entry.name,
            ", ".join(entry.cli_flags),
            _yes_no(entry.uses_projected_state),
            _yes_no(entry.uses_repo_files),
            _yes_no(entry.supports_json),
            _yes_no(entry.supports_record),
            entry.record_scope,
            _emits_facts_label(entry),
            _yes_no(entry.mutates_cluster),
            _notes(entry),
        ]
        for entry in entries
    ]
    widths = [
        max(len(row[index]) for row in [headers, *rows])
        for index in range(len(headers))
    ]
    rendered = [_render_row(headers, widths)]
    rendered.extend(_render_row(row, widths) for row in rows)
    return "\n".join(rendered)


def _render_row(row: list[str], widths: list[int]) -> str:
    return " | ".join(value.ljust(widths[index]) for index, value in enumerate(row))


def _yes_no(value: bool) -> str:
    return "yes" if value else "no"


def _emits_facts_label(entry: DiagnosticInventoryEntry) -> str:
    if entry.emits_diagnostic_facts and entry.emits_cluster_facts:
        return "diagnostic and cluster facts"
    if entry.emits_diagnostic_facts:
        return "diagnostic facts"
    if entry.emits_cluster_facts:
        return "cluster facts"
    return "no"


def _notes(entry: DiagnosticInventoryEntry) -> str:
    notes = [entry.description]
    if entry.supports_record:
        notes.append("recorded subjects use diagnostic_run:<id>")
    if entry.writes_event_ledger:
        notes.append("writes_event_ledger=true")
    if entry.reads_diagnostic_facts:
        notes.append("reads_diagnostic_facts=true")
    return " ".join(notes)
