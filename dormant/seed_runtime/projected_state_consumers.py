"""Read-only inventory of surfaces and their evidence-source consumption."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Literal

from seed_runtime.diagnostic_inventory import DIAGNOSTIC_INVENTORY

ConsumerKind = Literal[
    "diagnostic",
    "inquiry",
    "inventory",
    "runtime",
    "observation",
    "projection",
    "unknown",
]

BOUNDARY: dict[str, bool] = {
    "read_only": True,
    "records": False,
    "writes_event_ledger": False,
    "mutates_cluster": False,
    "executes_observation": False,
    "provider_acquisition": False,
    "permission_creation": False,
}

STATIC_INVENTORY_SURFACES = frozenset(
    {
        "diagnostic_inventory",
        "question_surface_inventory",
        "diagnostic_shape_audit",
        "projection_shape",
        "projected_state_consumers",
        "operational_surface_inventory",
    }
)

INQUIRY_SURFACES = frozenset(
    {
        "question_surface_inventory",
        "inquiry_artifacts",
        "investigation_path",
        "reasoning_path",
        "selection_path",
    }
)

OBSERVATION_SURFACES = frozenset(
    {
        "repository_state_observation",
        "observation_utilization",
        "observation_domains",
        "observation_permission",
    }
)

PROJECTION_SURFACES = frozenset(
    {
        "projection_shape",
        "current_facts_cache_debug",
        "graph_issue_summary",
    }
)

RUNTIME_INPUT_SURFACES = frozenset({"inquiry_artifacts"})
LIVE_OBSERVATION_SURFACES = frozenset({"repository_state_observation"})
EVENT_LEDGER_SURFACES = frozenset({"history_brief", "snapshot_policy_audit"})


@dataclass(frozen=True)
class ProjectedConsumerRow:
    surface: str
    cli_flags: tuple[str, ...]
    consumer_kind: ConsumerKind
    uses_projected_state: bool
    uses_repo_files: bool
    uses_static_inventory: bool
    uses_live_observation: bool
    uses_event_ledger: bool
    uses_runtime_input: bool
    boundary: dict[str, bool]
    notes: tuple[str, ...]

    def to_json_dict(self) -> dict[str, object]:
        data = asdict(self)
        data["cli_flags"] = list(self.cli_flags)
        data["notes"] = list(self.notes)
        data["boundary"] = dict(self.boundary)
        return data


def _kind_for(surface: str) -> ConsumerKind:
    if surface in STATIC_INVENTORY_SURFACES:
        return "inventory"
    if surface in INQUIRY_SURFACES:
        return "inquiry"
    if surface in OBSERVATION_SURFACES:
        return "observation"
    if surface in PROJECTION_SURFACES:
        return "projection"
    return "diagnostic"


def _notes_for(
    *,
    surface: str,
    uses_projected_state: bool,
    uses_repo_files: bool,
    uses_static_inventory: bool,
    uses_live_observation: bool,
    uses_event_ledger: bool,
    uses_runtime_input: bool,
) -> tuple[str, ...]:
    notes: list[str] = []
    if uses_projected_state:
        notes.append("projected-state use is declared by diagnostic inventory")
    if uses_repo_files:
        notes.append("repository-file use is declared by diagnostic inventory")
    if uses_static_inventory:
        notes.append("static inventory use is backed by registry/row data")
    if uses_live_observation:
        notes.append("live observation use is limited to existing observation collection surface evidence")
    if uses_event_ledger:
        notes.append("event-ledger use is marked only for existing history/policy audit surfaces")
    if uses_runtime_input:
        notes.append("runtime-input use is marked only for existing inquiry/runtime input surfaces")
    if not notes:
        notes.append("no source class is declared by current implementation evidence")
    if surface == "projected_state_consumers":
        notes.append("this surface classifies existing registry evidence only; it does not infer consumers")
    return tuple(notes)


def build_projected_state_consumers() -> tuple[ProjectedConsumerRow, ...]:
    """Return deterministic source-consumer rows from existing registries."""

    rows: list[ProjectedConsumerRow] = []
    for entry in DIAGNOSTIC_INVENTORY:
        uses_static_inventory = entry.name in STATIC_INVENTORY_SURFACES
        uses_live_observation = entry.name in LIVE_OBSERVATION_SURFACES
        uses_event_ledger = entry.name in EVENT_LEDGER_SURFACES
        uses_runtime_input = entry.name in RUNTIME_INPUT_SURFACES
        rows.append(
            ProjectedConsumerRow(
                surface=entry.name,
                cli_flags=entry.cli_flags,
                consumer_kind=_kind_for(entry.name),
                uses_projected_state=entry.uses_projected_state,
                uses_repo_files=entry.uses_repo_files,
                uses_static_inventory=uses_static_inventory,
                uses_live_observation=uses_live_observation,
                uses_event_ledger=uses_event_ledger,
                uses_runtime_input=uses_runtime_input,
                boundary=dict(BOUNDARY),
                notes=_notes_for(
                    surface=entry.name,
                    uses_projected_state=entry.uses_projected_state,
                    uses_repo_files=entry.uses_repo_files,
                    uses_static_inventory=uses_static_inventory,
                    uses_live_observation=uses_live_observation,
                    uses_event_ledger=uses_event_ledger,
                    uses_runtime_input=uses_runtime_input,
                ),
            )
        )
    return tuple(sorted(rows, key=lambda row: row.surface))


def projected_state_consumers_json(
    rows: tuple[ProjectedConsumerRow, ...] | None = None,
) -> list[dict[str, object]]:
    return [row.to_json_dict() for row in (rows or build_projected_state_consumers())]


def format_projected_state_consumers(
    rows: tuple[ProjectedConsumerRow, ...] | None = None,
) -> str:
    rows = rows or build_projected_state_consumers()
    lines = ["Projected State Consumers", ""]
    for row in rows:
        sources = [
            name
            for name, enabled in (
                ("projected_state", row.uses_projected_state),
                ("repo_files", row.uses_repo_files),
                ("static_inventory", row.uses_static_inventory),
                ("live_observation", row.uses_live_observation),
                ("event_ledger", row.uses_event_ledger),
                ("runtime_input", row.uses_runtime_input),
            )
            if enabled
        ]
        lines.append(row.surface)
        lines.append(f"  kind: {row.consumer_kind}")
        lines.append(f"  sources: {', '.join(sources) if sources else 'none_declared'}")
        lines.append("  boundary: read_only/no_record/no_mutation")
    return "\n".join(lines)
