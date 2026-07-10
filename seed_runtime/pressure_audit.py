"""Read-only operational pressure audit aggregated from existing visibility surfaces."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from seed_runtime.capability_needs import CapabilityNeedEntry, build_capability_needs
from seed_runtime.consumer_dependency_audit import ConsumerAudit, build_consumer_audit
from seed_runtime.diagnostic_shape_audit import (
    DiagnosticShapeAuditSummary,
    build_diagnostic_shape_audit,
    summarize_diagnostic_shape_audit,
)
from seed_runtime.ownership_discrepancies import build_ownership_discrepancies
from seed_runtime.state import State


@dataclass(frozen=True)
class PressureItem:
    category: str
    score: int
    evidence: dict[str, Any]
    reason: str
    recommended_command: str

    def to_json_dict(self) -> dict[str, Any]:
        return {
            "category": self.category,
            "score": self.score,
            "evidence": self.evidence,
            "reason": self.reason,
            "recommended_command": self.recommended_command,
        }


@dataclass(frozen=True)
class _PressureItemCandidate:
    category: str
    score: int
    evidence: dict[str, Any]
    reason: str
    recommended_command: str

    def to_pressure_item(self) -> PressureItem:
        return PressureItem(
            category=self.category,
            score=self.score,
            evidence=self.evidence,
            reason=self.reason,
            recommended_command=self.recommended_command,
        )


@dataclass(frozen=True)
class PressureAudit:
    pressures: tuple[PressureItem, ...]

    def to_json_dict(self) -> dict[str, Any]:
        return {"pressures": [item.to_json_dict() for item in self.pressures]}


def build_pressure_audit(
    state: State, *, repo_root: str | Path | None = None
) -> PressureAudit:
    """Rank operational pressure without planning, recording, or mutating state."""

    root = (
        Path(repo_root)
        if repo_root is not None
        else Path(__file__).resolve().parents[1]
    )
    return PressureAudit(
        pressures=_admitted_pressure_items(
            _diagnostic_shape_pressure(root),
            _ownership_pressure(state),
            _capability_pressure(state),
            *_consumer_predicate_pressures(root),
        )
    )


def pressure_audit_json(audit: PressureAudit) -> dict[str, Any]:
    return audit.to_json_dict()


def _admitted_pressure_items(
    *candidates: _PressureItemCandidate | None,
) -> tuple[PressureItem, ...]:
    items = [
        candidate.to_pressure_item()
        for candidate in candidates
        if candidate is not None and candidate.score > 0
    ]
    return tuple(sorted(items, key=lambda item: (-item.score, item.category)))


def format_pressure_audit(audit: PressureAudit) -> str:
    lines = ["Pressure Audit", ""]
    if not audit.pressures:
        lines.extend(
            [
                "No operational pressure identified by the current audit inputs.",
                "",
                "Summary:",
                "  pressures identified: 0",
            ]
        )
        return "\n".join(lines)
    for index, item in enumerate(audit.pressures, start=1):
        lines.extend(_format_pressure_item_section(index, item))
    lines.append("Summary:")
    lines.append(f"  pressures identified: {len(audit.pressures)}")
    return "\n".join(lines).rstrip()


def _format_pressure_item_section(index: int, item: PressureItem) -> list[str]:
    lines = [
        f"{index}. {item.category}",
        "",
        f"Score: {item.score}",
        "",
        "Evidence:",
    ]
    for key, value in item.evidence.items():
        lines.append(f"  {key}: {_display_evidence(value)}")
    lines.extend(
        [
            "",
            f"Reason: {item.reason}",
            f"Recommended inspection: {item.recommended_command}",
            "",
        ]
    )
    return lines


def _diagnostic_shape_pressure(root: Path) -> _PressureItemCandidate | None:
    summary = _diagnostic_shape_audit_summary(root)
    score = summary.mismatches + summary.warnings + summary.unknown
    if score <= 0:
        return None
    return _PressureItemCandidate(
        category="Diagnostic Shape",
        score=score,
        evidence=_diagnostic_shape_pressure_evidence(summary),
        reason=(
            "Diagnostic shape audit found visibility-contract rows that are not consistent."
        ),
        recommended_command="seed --diagnostic-shape-audit --mismatches",
    )


def _diagnostic_shape_audit_root(root: Path) -> Path | None:
    return root if (root / "scripts" / "seed_local.py").exists() else None


def _diagnostic_shape_audit_summary(root: Path) -> DiagnosticShapeAuditSummary:
    return summarize_diagnostic_shape_audit(
        build_diagnostic_shape_audit(repo_root=_diagnostic_shape_audit_root(root))
    )


def _diagnostic_shape_pressure_evidence(
    summary: DiagnosticShapeAuditSummary,
) -> dict[str, int]:
    return {
        "mismatches": summary.mismatches,
        "warnings": summary.warnings,
        "unknowns": summary.unknown,
    }


def _ownership_pressure(state: State) -> _PressureItemCandidate | None:
    rows = [row for row in build_ownership_discrepancies(state) if row.conflict]
    score = len(rows)
    if score <= 0:
        return None
    return _PressureItemCandidate(
        category="Ownership Attribution",
        score=score,
        evidence=_ownership_pressure_evidence(rows),
        reason=f"Ownership discrepancy audit reports {score} unresolved ownership row(s).",
        recommended_command="seed --ownership-discrepancies",
    )


def _ownership_pressure_evidence(rows: list[Any]) -> dict[str, Any]:
    conflict_counts = Counter(str(row.conflict) for row in rows)
    kind_counts = Counter(row.kind for row in rows)
    dominant = conflict_counts.most_common(1)[0][0] if conflict_counts else "none"
    return {
        "service ambiguities": kind_counts["service"],
        "storage ambiguities": kind_counts["storage"],
        "conflict counts": dict(sorted(conflict_counts.items())),
        "dominant conflict": dominant,
    }


def _capability_pressure(state: State) -> _PressureItemCandidate | None:
    entries = build_capability_needs(state)
    score = sum(len(entry.subjects) for entry in entries)
    if score <= 0:
        return None
    top = entries[0]
    return _PressureItemCandidate(
        category="Capability",
        score=score,
        evidence=_capability_pressure_evidence(entries),
        reason=(
            f"Capability needs audit reports missing observation capability across {score} subject occurrence(s); "
            f"top need is {top.capability}."
        ),
        recommended_command="seed --capability-needs",
    )


def _capability_pressure_evidence(
    entries: list[CapabilityNeedEntry],
) -> dict[str, Any]:
    return {
        "capability need frequency": {
            entry.capability: len(entry.subjects) for entry in entries
        },
        "affected subjects": sorted(
            {subject for entry in entries for subject in entry.subjects}
        ),
        "affected diagnostics": sorted(
            {diag for entry in entries for diag in entry.diagnostics}
        ),
    }


def _consumer_predicate_pressures(
    root: Path,
) -> tuple[_PressureItemCandidate | None, _PressureItemCandidate | None]:
    audit = build_consumer_audit(root)
    return (
        _orphaned_predicate_pressure(audit),
        _fragile_predicate_pressure(audit),
    )


def _orphaned_predicate_pressure(
    audit: ConsumerAudit,
) -> _PressureItemCandidate | None:
    items = [
        item
        for item in audit.items
        if item.kind == "observation_predicate" and item.orphaned
    ]
    if not items:
        return None
    return _PressureItemCandidate(
        category="Orphaned Predicates",
        score=len(items),
        evidence=_orphaned_predicate_pressure_evidence(items),
        reason="Consumer audit found observation predicates with no implementation consumers.",
        recommended_command="seed --consumer-audit",
    )


def _orphaned_predicate_pressure_evidence(
    items: list[Any],
) -> dict[str, Any]:
    return {
        "orphan count": len(items),
        "predicates": [item.item for item in items],
    }


def _fragile_predicate_pressure(
    audit: ConsumerAudit,
) -> _PressureItemCandidate | None:
    items = [
        item
        for item in audit.items
        if item.kind == "observation_predicate" and item.consumer_count == 1
    ]
    if not items:
        return None
    return _PressureItemCandidate(
        category="Fragile Predicates",
        score=len(items),
        evidence=_fragile_predicate_pressure_evidence(items),
        reason="Consumer audit found observation predicates with a single implementation consumer.",
        recommended_command="seed --consumer-audit",
    )


def _fragile_predicate_pressure_evidence(
    items: list[Any],
) -> dict[str, Any]:
    return {
        "single-consumer predicates": len(items),
        "predicates": [item.item for item in items],
    }


def _display_evidence(value: Any) -> str:
    if isinstance(value, dict):
        return _display_mapping_evidence(value)
    if isinstance(value, (list, tuple, set)):
        return _display_collection_evidence(value)
    return _display_scalar_evidence(value)


def _display_mapping_evidence(value: dict[Any, Any]) -> str:
    return ", ".join(f"{key}={val}" for key, val in value.items()) or "none"


def _display_collection_evidence(value: list[Any] | tuple[Any, ...] | set[Any]) -> str:
    return ", ".join(str(item) for item in value) or "none"


def _display_scalar_evidence(value: Any) -> str:
    return str(value)
