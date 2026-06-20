"""Read-only operational impact audit from existing audit snapshots."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

from seed_runtime.audit_snapshots import compare_audit_snapshots

ImpactResult = Literal["improved", "regressed", "unchanged", "unknown"]


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
        }


@dataclass(frozen=True)
class ImpactAudit:
    snapshots: dict[str, dict[str, str]]
    metrics: list[ImpactMetric]
    overall: ImpactResult
    missing: list[str]

    def to_json_dict(self) -> dict[str, Any]:
        return {
            "snapshots": self.snapshots,
            "metrics": [m.to_json_dict() for m in self.metrics],
            "overall": self.overall,
            "missing": self.missing,
        }


def build_impact_audit(repo_root: Path) -> ImpactAudit:
    metrics: list[ImpactMetric] = []
    missing: list[str] = []
    snapshots: dict[str, dict[str, str]] = {}

    try:
        ownership = compare_audit_snapshots(repo_root, "previous", "latest", kind="ownership_discrepancies")
        snapshots["ownership_discrepancies"] = ownership.get("snapshots", {})
        before = len(ownership.get("removed_rows", [])) + _changed_from_count(ownership)
        after = len(ownership.get("added_rows", [])) + _changed_to_count(ownership)
        # The total unresolved row count is the stable common rows plus added/removed.
        common = _common_changed_keys(ownership)
        before = len(common) + len(ownership.get("removed_rows", []))
        after = len(common) + len(ownership.get("added_rows", []))
        metrics.append(_metric("Ownership", "unresolved_ownership_rows", before, after, "lower_is_better"))

        before_needs, after_needs = _capability_need_counts_from_ownership_diff(ownership)
        metrics.append(_metric("Capabilities", "capability_pressure", before_needs, after_needs, "lower_is_better"))

        before_ambiguous, after_ambiguous = _ambiguous_counts_from_ownership_diff(ownership)
        metrics.append(_metric("Ownership", "ambiguity_counts", before_ambiguous, after_ambiguous, "lower_is_better"))
    except FileNotFoundError as exc:
        missing.append(str(exc))

    try:
        observation = compare_audit_snapshots(repo_root, "previous", "latest", kind="observation_inventory")
        snapshots["observation_inventory"] = observation.get("snapshots", {})
        changes = observation.get("summary_changes", {})
        for key in ("orphaned_predicates", "unused_predicates", "fragile_predicates"):
            if key in changes:
                metrics.append(_metric("Diagnostics", key, changes[key].get("from"), changes[key].get("to"), "lower_is_better"))
        pred_added = len(observation.get("predicates", {}).get("added", []))
        pred_removed = len(observation.get("predicates", {}).get("removed", []))
        metrics.append(_metric("Diagnostics", "observable_predicates", pred_removed, pred_added, "higher_is_better", note="added minus removed predicates"))
    except FileNotFoundError as exc:
        missing.append(str(exc))

    return ImpactAudit(snapshots=snapshots, metrics=metrics, overall=_overall(metrics, missing), missing=missing)


def impact_audit_json(audit: ImpactAudit) -> dict[str, Any]:
    return audit.to_json_dict()


def format_impact_audit(audit: ImpactAudit) -> str:
    lines = ["Operational Impact Audit", "", f"Overall: {audit.overall}", ""]
    if audit.snapshots:
        lines.append("Comparisons:")
        for kind, refs in audit.snapshots.items():
            lines.append(f"  {kind}: {refs.get('previous', '-')} -> {refs.get('latest', '-')}")
        lines.append("")
    if audit.metrics:
        lines.append("Outcomes:")
        for metric in audit.metrics:
            lines.extend([
                f"  {metric.area} / {metric.metric}:",
                f"    before: {_value(metric.before)}",
                f"    after: {_value(metric.after)}",
                f"    result: {metric.result}",
                f"    delta: {_value(metric.delta)}",
            ])
            if metric.note:
                lines.append(f"    note: {metric.note}")
    else:
        lines.append("Outcomes: unavailable")
    if audit.missing:
        lines.extend(["", "Missing comparison data:"])
        lines.extend(f"  - {m}" for m in audit.missing)
    return "\n".join(lines)


def _metric(area: str, name: str, before: Any, after: Any, direction: Literal["lower_is_better", "higher_is_better"], note: str = "") -> ImpactMetric:
    b = _int_or_none(before); a = _int_or_none(after)
    delta = None if b is None or a is None else a - b
    if delta is None:
        result: ImpactResult = "unknown"
    elif delta == 0:
        result = "unchanged"
    elif (delta < 0 and direction == "lower_is_better") or (delta > 0 and direction == "higher_is_better"):
        result = "improved"
    else:
        result = "regressed"
    return ImpactMetric(area, name, b, a, delta, result, direction, note)


def _overall(metrics: list[ImpactMetric], missing: list[str]) -> ImpactResult:
    results = {m.result for m in metrics}
    if "regressed" in results:
        return "regressed"
    if "improved" in results:
        return "improved"
    if metrics and results <= {"unchanged"}:
        return "unchanged"
    return "unknown"


def _value(value: int | None) -> str:
    return "unknown" if value is None else str(value)

def _int_or_none(value: Any) -> int | None:
    return value if isinstance(value, int) and not isinstance(value, bool) else None

def _common_changed_keys(diff: dict[str, Any]) -> set[str]:
    keys = set()
    for changes in diff.get("changes", {}).values():
        for change in changes:
            if "key" in change:
                keys.add(str(change["key"]))
    return keys

def _changed_from_count(diff: dict[str, Any]) -> int:
    return len(_common_changed_keys(diff))

def _changed_to_count(diff: dict[str, Any]) -> int:
    return len(_common_changed_keys(diff))

def _capability_need_counts_from_ownership_diff(diff: dict[str, Any]) -> tuple[int, int]:
    before = sum(len(r.get("capability_needs", []) or []) for r in diff.get("removed_rows", []))
    after = sum(len(r.get("capability_needs", []) or []) for r in diff.get("added_rows", []))
    for change in diff.get("changes", {}).get("capability_needs", []):
        before += len(change.get("removed", []))
        after += len(change.get("added", []))
    return before, after

def _ambiguous_counts_from_ownership_diff(diff: dict[str, Any]) -> tuple[int, int]:
    before = sum(1 for r in diff.get("removed_rows", []) if _is_ambiguous(r))
    after = sum(1 for r in diff.get("added_rows", []) if _is_ambiguous(r))
    for change in diff.get("changes", {}).get("conflict", []):
        before += 1 if _conflict_is_ambiguous(change.get("from")) else 0
        after += 1 if _conflict_is_ambiguous(change.get("to")) else 0
    return before, after

def _is_ambiguous(row: dict[str, Any]) -> bool:
    return _conflict_is_ambiguous(row.get("conflict"))

def _conflict_is_ambiguous(conflict: Any) -> bool:
    return conflict in {"ambiguous", "ambiguous_owner", "conflicting_owners", "insufficient_evidence", "missing_owner", "owner_not_observed"}
