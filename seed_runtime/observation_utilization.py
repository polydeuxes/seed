"""Implementation-backed observation predicate utilization audit."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from seed_runtime.observation_inventory import build_observation_inventory


@dataclass(frozen=True)
class ObservationUtilizationRow:
    predicate: str
    providers: tuple[str, ...]
    collected: bool
    projected: bool
    read_model: bool
    diagnostic_consumed: bool
    first_loss: str

    @property
    def provider_count(self) -> int:
        return len(self.providers)

    def to_json_dict(self) -> dict[str, Any]:
        return {
            "predicate": self.predicate,
            "provider_count": self.provider_count,
            "providers": list(self.providers),
            "collected": self.collected,
            "projected": self.projected,
            "read_model": self.read_model,
            "diagnostic_consumed": self.diagnostic_consumed,
            "first_loss": self.first_loss,
        }


@dataclass(frozen=True)
class ObservationUtilizationAudit:
    predicates: tuple[ObservationUtilizationRow, ...]
    metadata: dict[str, str]

    @property
    def summary(self) -> dict[str, int]:
        return {
            "predicates_discovered": len(self.predicates),
            "projected_predicates": sum(row.projected for row in self.predicates),
            "read_model_predicates": sum(row.read_model for row in self.predicates),
            "diagnostic_consumed_predicates": sum(
                row.diagnostic_consumed for row in self.predicates
            ),
            "unused_predicates": sum(row.first_loss == "unused" for row in self.predicates),
            "collected_only_predicates": sum(
                row.collected
                and not row.projected
                and not row.read_model
                and not row.diagnostic_consumed
                for row in self.predicates
            ),
            "projected_but_never_read_predicates": sum(
                row.projected and not row.read_model for row in self.predicates
            ),
            "read_model_but_never_consumed_predicates": sum(
                row.read_model and not row.diagnostic_consumed for row in self.predicates
            ),
        }

    def to_json_dict(self) -> dict[str, Any]:
        return {
            "summary": self.summary,
            "predicates": [row.to_json_dict() for row in self.predicates],
            "metadata": dict(self.metadata),
        }


PROJECTED_PATHS = (
    "seed_runtime/state.py",
    "seed_runtime/relationship_catalog.py",
    "seed_runtime/inference_rules.py",
    "seed_runtime/fact_support_aggregation.py",
    "relationship_catalog/core.json",
    "inference_catalog/core.json",
    "predicate_catalog/core.json",
)
READ_MODEL_PATHS = (
    "seed_runtime/state_views.py",
    "seed_runtime/context_views.py",
    "seed_runtime/state_summary_views.py",
)
DIAGNOSTIC_PATHS = (
    "seed_runtime/ownership_discrepancies.py",
    "seed_runtime/classification_coverage.py",
    "seed_runtime/capability_needs.py",
    "seed_runtime/knowledge_reachability.py",
)


def build_observation_utilization_audit(
    root: str | Path | None = None,
    *,
    provider_filter: str | None = None,
    predicate_filter: str | None = None,
) -> ObservationUtilizationAudit:
    repo_root = Path(root) if root is not None else Path(__file__).resolve().parents[1]
    inventory = build_observation_inventory(
        repo_root, provider_filter=provider_filter, predicate_filter=predicate_filter
    )
    projected_source = _read_sources(repo_root, PROJECTED_PATHS)
    read_model_source = _read_sources(repo_root, READ_MODEL_PATHS)
    diagnostic_source = _read_sources(repo_root, DIAGNOSTIC_PATHS)
    rows = []
    generic_read_model = _has_generic_predicate_read_model(read_model_source)
    for predicate in inventory.predicates:
        projected = _mentions_predicate(projected_source, predicate.predicate)
        read_model = _mentions_predicate(read_model_source, predicate.predicate) or (
            projected and generic_read_model
        )
        diagnostic = _mentions_predicate(diagnostic_source, predicate.predicate)
        rows.append(
            ObservationUtilizationRow(
                predicate=predicate.predicate,
                providers=predicate.providers,
                collected=True,
                projected=projected,
                read_model=read_model,
                diagnostic_consumed=diagnostic,
                first_loss=_first_loss(projected, read_model, diagnostic),
            )
        )
    return ObservationUtilizationAudit(
        predicates=tuple(sorted(rows, key=lambda row: row.predicate)),
        metadata={
            "observation_discovery": inventory.metadata.get(
                "predicates_discovered_from", "observation inventory"
            ),
            "projected_evidence": ", ".join(PROJECTED_PATHS),
            "read_model_evidence": ", ".join(READ_MODEL_PATHS),
            "generic_read_model_evidence": "read-model code that iterates projected facts and renders fact.predicate applies to projected predicates",
            "diagnostic_evidence": ", ".join(DIAGNOSTIC_PATHS),
        },
    )


def observation_utilization_json(audit: ObservationUtilizationAudit) -> dict[str, Any]:
    return audit.to_json_dict()


def format_observation_utilization(audit: ObservationUtilizationAudit) -> str:
    lines = [
        "Observation Utilization Audit",
        "",
        f"Predicates discovered: {audit.summary['predicates_discovered']}",
        f"Projected predicates: {audit.summary['projected_predicates']}",
        f"Read-model predicates: {audit.summary['read_model_predicates']}",
        f"Diagnostic-consumed predicates: {audit.summary['diagnostic_consumed_predicates']}",
        f"Unused predicates: {audit.summary['unused_predicates']}",
        "",
        "Predicate | Providers | Collected | Projected | Read Model | Diagnostic | First Loss",
    ]
    for row in audit.predicates:
        lines.append(
            " | ".join(
                [
                    row.predicate,
                    str(row.provider_count),
                    _yes_no(row.collected),
                    _yes_no(row.projected),
                    _yes_no(row.read_model),
                    _yes_no(row.diagnostic_consumed),
                    row.first_loss,
                ]
            )
        )
    dead_zones = [row for row in audit.predicates if row.first_loss != "none"]
    lines.extend(["", "Dead-zone visibility"])
    if not dead_zones:
        lines.append("none")
    else:
        for row in dead_zones:
            lines.append(f"{row.predicate}: {row.first_loss}")
    return "\n".join(lines)


def _read_sources(root: Path, paths: tuple[str, ...]) -> dict[str, str]:
    return {path: _read(root / path) for path in paths}


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def _has_generic_predicate_read_model(sources: dict[str, str]) -> bool:
    return any("fact.predicate" in source and "state.facts" in source for source in sources.values())


def _mentions_predicate(sources: dict[str, str], predicate: str) -> bool:
    needle_json = json.dumps(predicate)
    needle_single = repr(predicate)
    return any(needle_json in source or needle_single in source for source in sources.values())


def _first_loss(projected: bool, read_model: bool, diagnostic: bool) -> str:
    if not projected and not read_model and not diagnostic:
        return "unused"
    if not projected:
        return "projection_loss"
    if not read_model:
        return "read_model_loss"
    if not diagnostic:
        return "diagnostic_loss"
    return "none"


def _yes_no(value: bool) -> str:
    return "yes" if value else "no"
