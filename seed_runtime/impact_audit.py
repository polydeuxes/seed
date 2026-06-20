"""Read-only operational impact audit from existing audit snapshots."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

from seed_runtime.audit_snapshots import (
    SUPPORTED_KINDS,
    audit_root,
    compare_audit_snapshots,
)

ImpactResult = Literal["improved", "regressed", "unchanged", "unknown"]
CoverageStatus = Literal["comparable", "not_snapshotted", "no_comparison_data"]


@dataclass(frozen=True)
class ImpactMetric:
    area: str
    metric: str
    before: int | None
    after: int | None
    delta: int | None
    result: ImpactResult
    direction: Literal["lower_is_better", "higher_is_better"]
    note: str = ""
    snapshot_kind: str | None = None
    availability: CoverageStatus = "comparable"

    def to_json_dict(self) -> dict[str, Any]:
        return {
            "area": self.area,
            "metric": self.metric,
            "before": self.before,
            "after": self.after,
            "delta": self.delta,
            "result": self.result,
            "direction": self.direction,
            "note": self.note,
            "snapshot_kind": self.snapshot_kind,
            "availability": self.availability,
        }


@dataclass(frozen=True)
class SnapshotCoverage:
    surface: str
    snapshot_kind: str | None
    supports_snapshots: bool
    comparison_data: bool
    status: CoverageStatus
    metrics: tuple[str, ...]
    note: str = ""

    def to_json_dict(self) -> dict[str, Any]:
        return {
            "surface": self.surface,
            "snapshot_kind": self.snapshot_kind,
            "supports_snapshots": self.supports_snapshots,
            "comparison_data": self.comparison_data,
            "status": self.status,
            "metrics": list(self.metrics),
            "note": self.note,
        }


@dataclass(frozen=True)
class ImpactAudit:
    snapshots: dict[str, dict[str, str]]
    metrics: list[ImpactMetric]
    overall: ImpactResult
    missing: list[str]
    coverage: list[SnapshotCoverage]

    def to_json_dict(self) -> dict[str, Any]:
        return {
            "snapshots": self.snapshots,
            "metrics": [m.to_json_dict() for m in self.metrics],
            "overall": self.overall,
            "missing": self.missing,
            "snapshot_coverage": [c.to_json_dict() for c in self.coverage],
        }


_SURFACE_METRICS: tuple[tuple[str, str | None, tuple[str, ...], str], ...] = (
    (
        "ownership_discrepancies",
        "ownership_discrepancies",
        ("unresolved_ownership_rows", "ambiguity_counts"),
        "Snapshot payload contains ownership rows.",
    ),
    (
        "observation_inventory",
        "observation_inventory",
        ("observable_predicates",),
        "Snapshot payload contains predicate inventory.",
    ),
    (
        "capability_needs",
        None,
        ("capability_pressure",),
        "No audit snapshot kind currently stores capability-needs output.",
    ),
    (
        "pressure_audit",
        None,
        (),
        "Future candidate; current impact metrics do not compare pressure-audit scores.",
    ),
    (
        "ops_brief",
        None,
        (),
        "Future candidate; aggregate brief is not currently snapshotted.",
    ),
    (
        "correlation_audit",
        None,
        (),
        "Future candidate; current impact metrics do not require it.",
    ),
    (
        "privilege_discovery",
        None,
        (),
        "Future candidate; current impact metrics do not require it.",
    ),
)


def build_impact_audit(repo_root: Path) -> ImpactAudit:
    metrics: list[ImpactMetric] = []
    missing: list[str] = []
    snapshots: dict[str, dict[str, str]] = {}
    coverage = _build_snapshot_coverage(repo_root)

    ownership_pair = _snapshot_payload_pair(repo_root, "ownership_discrepancies")
    if ownership_pair is None:
        missing.append("need at least two ownership_discrepancies snapshots")
        metrics.append(
            _unavailable_metric(
                "Ownership",
                "unresolved_ownership_rows",
                "lower_is_better",
                "ownership_discrepancies",
                "no_comparison_data",
            )
        )
        metrics.append(
            _unavailable_metric(
                "Ownership",
                "ambiguity_counts",
                "lower_is_better",
                "ownership_discrepancies",
                "no_comparison_data",
            )
        )
    else:
        previous_id, latest_id, before_rows, after_rows = ownership_pair
        snapshots["ownership_discrepancies"] = {
            "previous": previous_id,
            "latest": latest_id,
        }
        metrics.append(
            _metric(
                "Ownership",
                "unresolved_ownership_rows",
                len(before_rows),
                len(after_rows),
                "lower_is_better",
                snapshot_kind="ownership_discrepancies",
            )
        )
        metrics.append(
            _metric(
                "Ownership",
                "ambiguity_counts",
                _count_ambiguous_rows(before_rows),
                _count_ambiguous_rows(after_rows),
                "lower_is_better",
                snapshot_kind="ownership_discrepancies",
            )
        )

    metrics.append(
        _unavailable_metric(
            "Capabilities",
            "capability_pressure",
            "lower_is_better",
            None,
            "not_snapshotted",
            "capability_needs/pressure_audit comparison data is not snapshotted; missing evidence is not reported as zero",
        )
    )

    observation_pair = _snapshot_payload_pair(repo_root, "observation_inventory")
    if observation_pair is None:
        missing.append("need at least two observation_inventory snapshots")
        metrics.append(
            _unavailable_metric(
                "Diagnostics",
                "observable_predicates",
                "higher_is_better",
                "observation_inventory",
                "no_comparison_data",
            )
        )
    else:
        previous_id, latest_id, before_payload, after_payload = observation_pair
        snapshots["observation_inventory"] = {
            "previous": previous_id,
            "latest": latest_id,
        }
        metrics.append(
            _metric(
                "Diagnostics",
                "observable_predicates",
                _predicate_count(before_payload),
                _predicate_count(after_payload),
                "higher_is_better",
                note="total predicates in observation_inventory snapshots",
                snapshot_kind="observation_inventory",
            )
        )
        try:
            observation = compare_audit_snapshots(
                repo_root, "previous", "latest", kind="observation_inventory"
            )
            changes = observation.get("summary_changes", {})
            for key in (
                "orphaned_predicates",
                "unused_predicates",
                "fragile_predicates",
            ):
                if key in changes:
                    metrics.append(
                        _metric(
                            "Diagnostics",
                            key,
                            changes[key].get("from"),
                            changes[key].get("to"),
                            "lower_is_better",
                            snapshot_kind="observation_inventory",
                        )
                    )
        except FileNotFoundError:
            pass

    return ImpactAudit(
        snapshots=snapshots,
        metrics=metrics,
        overall=_overall(metrics),
        missing=missing,
        coverage=coverage,
    )


def impact_audit_json(audit: ImpactAudit) -> dict[str, Any]:
    return audit.to_json_dict()


def format_impact_audit(audit: ImpactAudit) -> str:
    lines = ["Operational Impact Audit", "", f"Overall: {audit.overall}", ""]
    if audit.snapshots:
        lines.append("Comparisons:")
        for kind, refs in audit.snapshots.items():
            lines.append(
                f"  {kind}: {refs.get('previous', '-')} -> {refs.get('latest', '-')}"
            )
        lines.append("")
    lines.append("Snapshot Coverage:")
    for row in audit.coverage:
        lines.append(f"  {row.surface}: {row.status}")
        lines.append(f"    snapshots: {'yes' if row.supports_snapshots else 'no'}")
        lines.append(f"    comparison data: {'yes' if row.comparison_data else 'no'}")
        if row.metrics:
            lines.append(f"    metrics: {', '.join(row.metrics)}")
        if row.note:
            lines.append(f"    note: {row.note}")
    lines.append("")
    if audit.metrics:
        lines.append("Outcomes:")
        for metric in audit.metrics:
            lines.extend(
                [
                    f"  {metric.area} / {metric.metric}:",
                    f"    availability: {metric.availability}",
                    f"    before: {_value(metric.before, metric.availability)}",
                    f"    after: {_value(metric.after, metric.availability)}",
                    f"    result: {metric.result}",
                    f"    delta: {_value(metric.delta, metric.availability)}",
                ]
            )
            if metric.snapshot_kind:
                lines.append(f"    snapshot_kind: {metric.snapshot_kind}")
            if metric.note:
                lines.append(f"    note: {metric.note}")
    else:
        lines.append("Outcomes: unavailable")
    if audit.missing:
        lines.extend(["", "Missing comparison data:"])
        lines.extend(f"  - {m}" for m in audit.missing)
    return "\n".join(lines)


def _metric(
    area: str,
    name: str,
    before: Any,
    after: Any,
    direction: Literal["lower_is_better", "higher_is_better"],
    note: str = "",
    snapshot_kind: str | None = None,
) -> ImpactMetric:
    b = _int_or_none(before)
    a = _int_or_none(after)
    delta = None if b is None or a is None else a - b
    if delta is None:
        result: ImpactResult = "unknown"
    elif delta == 0:
        result = "unchanged"
    elif (delta < 0 and direction == "lower_is_better") or (
        delta > 0 and direction == "higher_is_better"
    ):
        result = "improved"
    else:
        result = "regressed"
    return ImpactMetric(
        area, name, b, a, delta, result, direction, note, snapshot_kind, "comparable"
    )


def _unavailable_metric(
    area: str,
    name: str,
    direction: Literal["lower_is_better", "higher_is_better"],
    snapshot_kind: str | None,
    availability: CoverageStatus,
    note: str = "",
) -> ImpactMetric:
    return ImpactMetric(
        area,
        name,
        None,
        None,
        None,
        "unknown",
        direction,
        note or availability,
        snapshot_kind,
        availability,
    )


def _overall(metrics: list[ImpactMetric]) -> ImpactResult:
    comparable = [m for m in metrics if m.availability == "comparable"]
    results = {m.result for m in comparable}
    if "regressed" in results:
        return "regressed"
    if "improved" in results:
        return "improved"
    if comparable and results <= {"unchanged"}:
        return "unchanged"
    return "unknown"


def _value(value: int | None, availability: CoverageStatus = "comparable") -> str:
    if value is None:
        return "unknown" if availability == "comparable" else availability
    return str(value)


def _int_or_none(value: Any) -> int | None:
    return value if isinstance(value, int) and not isinstance(value, bool) else None


def _snapshot_payload_pair(
    repo_root: Path, kind: str
) -> tuple[str, str, Any, Any] | None:
    dirs = _snapshot_dirs(repo_root, kind)
    if len(dirs) < 2:
        return None
    previous, latest = dirs[-2], dirs[-1]
    left = _read_json(previous / f"{kind}.json")
    right = _read_json(latest / f"{kind}.json")
    if left is None or right is None:
        return None
    return previous.name, latest.name, left, right


def _snapshot_dirs(repo_root: Path, kind: str) -> list[Path]:
    root = audit_root(repo_root)
    if not root.exists():
        return []
    return sorted(
        p for p in root.iterdir() if p.is_dir() and (p / f"{kind}.json").exists()
    )


def _read_json(path: Path) -> Any | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return None


def _predicate_count(payload: dict[str, Any]) -> int | None:
    summary_count = (
        payload.get("summary", {}).get("predicate_count")
        if isinstance(payload, dict)
        else None
    )
    if isinstance(summary_count, int) and not isinstance(summary_count, bool):
        return summary_count
    predicates = payload.get("predicates") if isinstance(payload, dict) else None
    return len(predicates) if isinstance(predicates, list) else None


def _count_ambiguous_rows(rows: list[dict[str, Any]]) -> int:
    return sum(1 for row in rows if _is_ambiguous(row))


def _is_ambiguous(row: dict[str, Any]) -> bool:
    return _conflict_is_ambiguous(row.get("conflict"))


def _conflict_is_ambiguous(conflict: Any) -> bool:
    return conflict in {
        "ambiguous",
        "ambiguous_owner",
        "conflicting_owners",
        "multiple_candidate_owners",
        "insufficient_evidence",
        "missing_owner",
        "owner_not_observed",
    }


def _build_snapshot_coverage(repo_root: Path) -> list[SnapshotCoverage]:
    rows: list[SnapshotCoverage] = []
    for surface, snapshot_kind, metrics, note in _SURFACE_METRICS:
        supports = bool(snapshot_kind and snapshot_kind in SUPPORTED_KINDS)
        comparison = bool(
            snapshot_kind and len(_snapshot_dirs(repo_root, snapshot_kind)) >= 2
        )
        if comparison:
            status: CoverageStatus = "comparable"
        elif supports:
            status = "no_comparison_data"
        else:
            status = "not_snapshotted"
        rows.append(
            SnapshotCoverage(
                surface, snapshot_kind, supports, comparison, status, metrics, note
            )
        )
    return rows
