"""Read-only audit snapshot policy visibility."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Literal

from seed_runtime.audit_snapshots import SUPPORTED_KINDS, audit_root
from seed_runtime.impact_audit import build_impact_audit
from seed_runtime.repository_observation import (
    RepositoryObservation,
    observe_repository,
)

Recommendation = Literal[
    "snapshot_recommended",
    "snapshot_optional",
    "snapshot_not_needed",
    "insufficient_change",
    "unknown",
]
SnapshotStatus = Literal["healthy", "single_snapshot", "unsnapshotted", "unknown_kind"]


@dataclass(frozen=True)
class SnapshotKindPolicy:
    kind: str
    latest_snapshot: str | None
    latest_snapshot_age_seconds: int | None
    snapshot_count: int
    comparison_available: bool
    comparison_usefulness: str
    status: SnapshotStatus
    recommendation: Recommendation
    reason: str

    def to_json_dict(self) -> dict[str, Any]:
        return {
            "kind": self.kind,
            "latest_snapshot": self.latest_snapshot,
            "latest_snapshot_age_seconds": self.latest_snapshot_age_seconds,
            "snapshot_count": self.snapshot_count,
            "comparison_available": self.comparison_available,
            "comparison_usefulness": self.comparison_usefulness,
            "status": self.status,
            "recommendation": self.recommendation,
            "reason": self.reason,
        }


@dataclass(frozen=True)
class SnapshotConstrainedSurface:
    surface: str
    dependent_on: tuple[str, ...]
    snapshot_health: str
    reason: str

    def to_json_dict(self) -> dict[str, Any]:
        return {
            "surface": self.surface,
            "dependent_on": list(self.dependent_on),
            "snapshot_health": self.snapshot_health,
            "reason": self.reason,
        }


@dataclass(frozen=True)
class SnapshotPolicyAudit:
    repository_context: RepositoryObservation
    repository_context_health: str
    repository_context_reason: str
    snapshot_kinds: list[SnapshotKindPolicy]
    comparison_availability: list[dict[str, Any]]
    recommendations: list[dict[str, str]]
    operational_surfaces: list[SnapshotConstrainedSurface]
    writes_event_ledger: bool = False
    mutates_cluster: bool = False

    def to_json_dict(self) -> dict[str, Any]:
        return {
            "repository_context": self.repository_context.to_json_dict(),
            "repository_context_health": self.repository_context_health,
            "repository_context_reason": self.repository_context_reason,
            "snapshot_kinds": [k.to_json_dict() for k in self.snapshot_kinds],
            "comparison_availability": self.comparison_availability,
            "recommendations": self.recommendations,
            "operational_surfaces": [
                s.to_json_dict() for s in self.operational_surfaces
            ],
            "writes_event_ledger": self.writes_event_ledger,
            "mutates_cluster": self.mutates_cluster,
        }


_MISSING_CANDIDATES: tuple[tuple[str, str], ...] = (
    ("capability_needs", "impact_audit cannot compare capability pressure"),
)


def build_snapshot_policy_audit(
    repo_root: Path, *, now: datetime | None = None
) -> SnapshotPolicyAudit:
    root = Path(repo_root)
    clock = now or datetime.now(timezone.utc)
    kinds = [_kind_policy(root, kind, clock) for kind in sorted(SUPPORTED_KINDS)]
    kinds.extend(
        _missing_kind_policy(kind, reason) for kind, reason in _MISSING_CANDIDATES
    )

    impact = build_impact_audit(root)
    comparison_availability = [
        {
            "surface": row.surface,
            "snapshot_kind": row.snapshot_kind,
            "comparison_available": row.comparison_data,
            "status": row.status,
            "metrics": list(row.metrics),
            "note": row.note,
        }
        for row in impact.coverage
    ]
    repository_context = observe_repository(root)
    repository_health, repository_reason = _repository_context_health(
        repository_context
    )
    surfaces = _operational_surfaces(comparison_availability)
    recommendations = [
        {"kind": row.kind, "recommendation": row.recommendation, "reason": row.reason}
        for row in kinds
    ]
    return SnapshotPolicyAudit(
        repository_context,
        repository_health,
        repository_reason,
        kinds,
        comparison_availability,
        recommendations,
        surfaces,
    )


def snapshot_policy_audit_json(audit: SnapshotPolicyAudit) -> dict[str, Any]:
    return audit.to_json_dict()


def format_snapshot_policy_audit(audit: SnapshotPolicyAudit) -> str:
    lines = [
        "Snapshot Policy Audit",
        "",
        "Repository Context:",
        f"  health: {audit.repository_context_health}",
        f"  reason: {audit.repository_context_reason}",
        f"  status available: {'yes' if audit.repository_context.repository_status_available else 'no'}",
        f"  vcs: {audit.repository_context.repository_vcs or 'unknown'}",
        f"  latest repository state: {audit.repository_context.repository_head_commit or 'unknown'}",
        f"  branch: {audit.repository_context.repository_branch or 'unknown'}",
        f"  status: {_repository_status_label(audit.repository_context)}",
        "",
        "Snapshot Kinds:",
    ]
    if not audit.snapshot_kinds:
        lines.append("  none")
    for row in audit.snapshot_kinds:
        lines.extend(
            [
                f"  {row.kind}:",
                f"    latest snapshot: {row.latest_snapshot or 'none'}",
                f"    latest snapshot age seconds: {_value(row.latest_snapshot_age_seconds)}",
                f"    snapshot count: {row.snapshot_count}",
                f"    comparison available: {'yes' if row.comparison_available else 'no'}",
                f"    comparison usefulness: {row.comparison_usefulness}",
                f"    status: {row.status}",
                f"    recommendation: {row.recommendation}",
                f"    reason: {row.reason}",
            ]
        )
    lines.extend(["", "Comparison Availability:"])
    if not audit.comparison_availability:
        lines.append("  none")
    for row in audit.comparison_availability:
        lines.append(f"  {row['surface']}: {row['status']}")
        lines.append(f"    snapshot kind: {row.get('snapshot_kind') or 'none'}")
        lines.append(
            f"    comparison available: {'yes' if row.get('comparison_available') else 'no'}"
        )
        if row.get("note"):
            lines.append(f"    note: {row['note']}")
    lines.extend(["", "Operational Surfaces:"])
    if not audit.operational_surfaces:
        lines.append("  none")
    for surface in audit.operational_surfaces:
        lines.append(f"  {surface.surface}:")
        lines.append(f"    dependent on: {', '.join(surface.dependent_on) or 'none'}")
        lines.append(f"    snapshot health: {surface.snapshot_health}")
        lines.append(f"    reason: {surface.reason}")
    lines.extend(["", "Recommendations:"])
    for row in audit.recommendations:
        lines.append(f"  {row['kind']}: {row['recommendation']} - {row['reason']}")
    return "\n".join(lines)


def _kind_policy(repo_root: Path, kind: str, now: datetime) -> SnapshotKindPolicy:
    dirs = _snapshot_dirs(repo_root, kind)
    latest = dirs[-1] if dirs else None
    age = _snapshot_age_seconds(latest, now) if latest else None
    if len(dirs) >= 2:
        status: SnapshotStatus = "healthy"
        useful = "historical comparison is available"
        rec: Recommendation = "snapshot_optional"
        reason = "existing snapshots can compare recent history; take another snapshot when new operational change should be preserved"
    elif len(dirs) == 1:
        status = "single_snapshot"
        useful = "baseline exists but no before/after comparison is possible"
        rec = "snapshot_recommended"
        reason = "one more snapshot would enable comparison"
    else:
        status = "unsnapshotted"
        useful = "no baseline exists"
        rec = "snapshot_recommended"
        reason = "first snapshot would establish a baseline"
    return SnapshotKindPolicy(
        kind,
        latest.name if latest else None,
        age,
        len(dirs),
        len(dirs) >= 2,
        useful,
        status,
        rec,
        reason,
    )


def _missing_kind_policy(kind: str, reason: str) -> SnapshotKindPolicy:
    return SnapshotKindPolicy(
        kind,
        None,
        None,
        0,
        False,
        "not supported by audit snapshot storage",
        "unsnapshotted",
        "unknown",
        reason,
    )


def _snapshot_dirs(repo_root: Path, kind: str) -> list[Path]:
    root = audit_root(repo_root)
    if not root.exists():
        return []
    return sorted(
        p for p in root.iterdir() if p.is_dir() and (p / f"{kind}.json").exists()
    )


def _snapshot_age_seconds(directory: Path, now: datetime) -> int | None:
    metadata_path = directory / "metadata.json"
    try:
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        created = str(metadata.get("created_at") or "").replace("Z", "+00:00")
        created_at = datetime.fromisoformat(created)
        if created_at.tzinfo is None:
            created_at = created_at.replace(tzinfo=timezone.utc)
        return max(0, int((now - created_at).total_seconds()))
    except (OSError, ValueError, TypeError, json.JSONDecodeError):
        return None


def _operational_surfaces(
    rows: list[dict[str, Any]],
) -> list[SnapshotConstrainedSurface]:
    by_surface = {str(row["surface"]): row for row in rows}
    deps = ("ownership_discrepancies", "observation_inventory")
    healthy = [d for d in deps if by_surface.get(d, {}).get("comparison_available")]
    if len(healthy) == len(deps):
        health = "healthy"
        reason = "all story snapshot-backed dependencies are comparable"
    elif healthy:
        health = "partial"
        reason = "some story outcomes are comparable and some are not"
    else:
        health = "constrained"
        reason = (
            "story historical context lacks comparable snapshot-backed dependencies"
        )
    return [SnapshotConstrainedSurface("operational_story", deps, health, reason)]


def _value(value: int | None) -> str:
    return "unknown" if value is None else str(value)


def _repository_context_health(observation: RepositoryObservation) -> tuple[str, str]:
    if not observation.repository_status_available:
        return (
            "missing",
            observation.reason or "repository-state evidence is unavailable",
        )
    if observation.repository_head_commit and observation.repository_dirty is False:
        return "healthy", "repository-state evidence is complete and clean"
    return "partial", "repository-state evidence is available but working tree is dirty or incomplete"


def _repository_status_label(observation: RepositoryObservation) -> str:
    if not observation.repository_status_available:
        return "unknown"
    return "dirty" if observation.repository_dirty else "clean"
