"""Read-only implementation-backed trait-to-concern characterization."""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import asdict, dataclass, fields
from typing import Any, Literal

from seed_runtime.diagnostic_inventory import DiagnosticInventoryEntry, DIAGNOSTIC_INVENTORY
from seed_runtime.operational_surface_inventory import OperationalSurface
from seed_runtime.projected_state_consumers import BOUNDARY, ProjectedConsumerRow
from seed_runtime.question_surface_inventory import QuestionSurfaceInventoryRow

Concern = Literal[
    "evidence_source",
    "operational_boundary",
    "dispatchability",
    "implementation_capability",
    "unclassified",
]

CONCERN_BY_TRAIT: dict[str, Concern] = {
    "uses_projected_state": "evidence_source",
    "uses_repo_files": "evidence_source",
    "uses_static_inventory": "evidence_source",
    "uses_live_observation": "evidence_source",
    "uses_event_ledger": "evidence_source",
    "uses_runtime_input": "evidence_source",
    "reads_diagnostic_facts": "evidence_source",
    "evidence": "evidence_source",
    "read_only": "operational_boundary",
    "records": "operational_boundary",
    "supports_record": "operational_boundary",
    "record_scope": "operational_boundary",
    "writes_event_ledger": "operational_boundary",
    "mutates_cluster": "operational_boundary",
    "executes_observation": "operational_boundary",
    "permission_creation": "operational_boundary",
    "provider_acquisition": "operational_boundary",
    "bounded_status": "dispatchability",
    "dispatch_surface": "dispatchability",
    "required_surface_args": "dispatchability",
    "supports_json": "implementation_capability",
    "json_support": "implementation_capability",
    "json_capable": "implementation_capability",
    "registered": "implementation_capability",
    "category": "implementation_capability",
    "consumer_kind": "implementation_capability",
    "emits_diagnostic_facts": "implementation_capability",
    "emits_cluster_facts": "implementation_capability",
}

SURFACE_FIELDS: dict[str, set[str]] = {
    "--diagnostic-inventory": {field.name for field in fields(DiagnosticInventoryEntry)},
    "--projected-state-consumers": {field.name for field in fields(ProjectedConsumerRow)} | set(BOUNDARY),
    "--question-surface-inventory": {field.name for field in fields(QuestionSurfaceInventoryRow)},
    "--operational-surface-inventory": {field.name for field in fields(OperationalSurface)},
}

MEANING_BY_TRAIT: dict[str, str] = {
    "uses_projected_state": "declares whether a surface consumes projected state",
    "uses_repo_files": "declares whether a surface reads repository files or repository inventory evidence",
    "uses_static_inventory": "declares whether a surface consumes static registry or inventory row data",
    "uses_live_observation": "declares whether a surface depends on existing live observation collection evidence",
    "uses_event_ledger": "declares whether a surface depends on event-ledger evidence",
    "uses_runtime_input": "declares whether a surface depends on runtime inquiry input",
    "reads_diagnostic_facts": "declares whether a surface reads diagnostic facts",
    "evidence": "names the implementation evidence source for a discovered operational surface",
    "read_only": "declares a no-mutation operational boundary",
    "records": "declares whether the visibility surface records facts during this run",
    "supports_record": "declares whether a surface has a record-capable mode",
    "record_scope": "declares the subject scope used when recording is supported",
    "writes_event_ledger": "declares whether a surface appends to the event ledger",
    "mutates_cluster": "declares whether a surface mutates cluster truth/state",
    "executes_observation": "declares whether a surface executes observation collection",
    "permission_creation": "declares whether a surface creates permission state",
    "provider_acquisition": "declares whether a surface acquires or invokes providers",
    "bounded_status": "declares bounded ask dispatch eligibility for a question family",
    "dispatch_surface": "declares the implementation dispatch surface for bounded ask",
    "required_surface_args": "declares required arguments for dispatchable bounded surfaces",
    "supports_json": "declares whether a diagnostic surface supports JSON output",
    "json_support": "declares whether a question surface supports JSON output",
    "json_capable": "declares whether an operational CLI surface has JSON-capable visibility",
    "registered": "declares whether a discovered operational surface is registered in diagnostic inventory",
    "category": "declares the discovered operational surface category",
    "consumer_kind": "declares the implementation-backed consumer kind",
    "emits_diagnostic_facts": "declares whether a surface emits diagnostic facts",
    "emits_cluster_facts": "declares whether a surface emits cluster facts",
}

@dataclass(frozen=True)
class ImplementationTraitCharacterizationRow:
    trait: str
    concern: Concern
    exposed_by: tuple[str, ...]
    implementation_meaning: str
    implementation_reason: str

    def to_json_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["exposed_by"] = list(self.exposed_by)
        return data


def build_implementation_trait_characterization() -> tuple[ImplementationTraitCharacterizationRow, ...]:
    exposure: dict[str, list[str]] = defaultdict(list)
    for surface, traits in SURFACE_FIELDS.items():
        for trait in traits:
            exposure[trait].append(surface)

    rows: list[ImplementationTraitCharacterizationRow] = []
    for trait in sorted(exposure):
        concern = CONCERN_BY_TRAIT.get(trait, "unclassified")
        exposed_by = tuple(sorted(exposure[trait]))
        if concern == "unclassified":
            reason = "trait is exposed by the current inventories, but no implementation-backed concern mapping declares it"
            meaning = "unclassified exposed implementation trait"
        else:
            reason = f"trait is declared by {', '.join(exposed_by)} and mapped by the implementation trait concern registry"
            meaning = MEANING_BY_TRAIT[trait]
        rows.append(ImplementationTraitCharacterizationRow(trait, concern, exposed_by, meaning, reason))
    return tuple(rows)


def implementation_trait_characterization_json(rows: tuple[ImplementationTraitCharacterizationRow, ...] | None = None) -> dict[str, Any]:
    rows = rows or build_implementation_trait_characterization()
    return {
        "concern_counts": dict(sorted(Counter(row.concern for row in rows).items())),
        "items": [row.to_json_dict() for row in rows],
    }


def format_implementation_trait_characterization(rows: tuple[ImplementationTraitCharacterizationRow, ...] | None = None) -> str:
    rows = rows or build_implementation_trait_characterization()
    counts = Counter(row.concern for row in rows)
    lines = ["Implementation Trait Characterization", ""]
    lines.append("concern_counts: " + ", ".join(f"{k}={v}" for k, v in sorted(counts.items())))
    lines.append("")
    for row in rows:
        lines.append(row.trait)
        lines.append(f"  concern: {row.concern}")
        lines.append(f"  exposed_by: {', '.join(row.exposed_by)}")
        lines.append(f"  implementation_meaning: {row.implementation_meaning}")
        lines.append(f"  implementation_reason: {row.implementation_reason}")
    return "\n".join(lines)
