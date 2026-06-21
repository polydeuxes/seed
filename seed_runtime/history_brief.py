"""Read-only historical synthesis brief from existing visibility surfaces."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

from seed_runtime.impact_audit import ImpactAudit, ImpactMetric, build_impact_audit
from seed_runtime.repository_observation import RepositoryObservation
from seed_runtime.snapshot_policy_audit import SnapshotPolicyAudit, build_snapshot_policy_audit

ConfidenceLevel = Literal["high", "partial", "snapshot_constrained", "unknown"]


@dataclass(frozen=True)
class HistoryBrief:
    changes: list[dict[str, Any]]
    stable: list[dict[str, Any]]
    repository_context: dict[str, Any]
    historical_confidence: dict[str, Any]
    unsupported_conclusions: list[dict[str, str]]
    writes_event_ledger: bool = False
    mutates_cluster: bool = False

    def to_json_dict(self) -> dict[str, Any]:
        return {
            "changes": self.changes,
            "stable": self.stable,
            "repository_context": self.repository_context,
            "historical_confidence": self.historical_confidence,
            "unsupported_conclusions": self.unsupported_conclusions,
            "writes_event_ledger": self.writes_event_ledger,
            "mutates_cluster": self.mutates_cluster,
        }


def build_history_brief(repo_root: Path) -> HistoryBrief:
    """Build a synthesis from impact, snapshot-policy, and repository observation."""

    impact = build_impact_audit(repo_root)
    policy = build_snapshot_policy_audit(repo_root)
    changes = _changes(impact)
    stable = _stable(impact)
    unsupported = _unsupported(impact, policy)
    confidence = _confidence(impact, policy, unsupported)
    return HistoryBrief(
        changes=changes,
        stable=stable,
        repository_context=_repository_context(policy.repository_context, policy),
        historical_confidence=confidence,
        unsupported_conclusions=unsupported,
    )


def history_brief_json(brief: HistoryBrief) -> dict[str, Any]:
    return brief.to_json_dict()


def format_history_brief(brief: HistoryBrief) -> str:
    lines = [
        "History Brief",
        "",
        "Changes:",
        *_format_items(brief.changes),
        "",
        "Stability:",
        *_format_items(brief.stable),
        "",
        "Repository Context:",
    ]
    ctx = brief.repository_context
    lines.extend(
        [
            f"  health: {ctx.get('health', 'unknown')}",
            f"  state: {ctx.get('state', 'unknown')}",
            f"  vcs: {ctx.get('vcs') or 'unknown'}",
            f"  head commit: {ctx.get('head_commit') or 'unknown'}",
            f"  branch: {ctx.get('branch') or 'unknown'}",
            f"  reason: {ctx.get('reason') or 'none'}",
        ]
    )
    conf = brief.historical_confidence
    lines.extend(
        [
            "",
            "Historical Confidence:",
            f"  level: {conf.get('level', 'unknown')}",
            f"  comparison: {conf.get('comparison', 'unknown')}",
            f"  causation: {conf.get('causation', 'not proven')}",
            f"  reason: {conf.get('reason', 'unknown')}",
            "",
            "Unsupported Conclusions:",
            *_format_items(brief.unsupported_conclusions),
            "",
            "Boundary: correlation may be visible; causation is not proven by this brief.",
        ]
    )
    return "\n".join(lines)


def _changes(impact: ImpactAudit) -> list[dict[str, Any]]:
    rows = []
    for metric in impact.metrics:
        if metric.availability == "comparable" and metric.delta not in (None, 0):
            rows.append(_metric_summary(metric, "changed"))
    return rows


def _stable(impact: ImpactAudit) -> list[dict[str, Any]]:
    rows = []
    for metric in impact.metrics:
        if metric.availability == "comparable" and metric.delta == 0:
            rows.append(_metric_summary(metric, "unchanged"))
    return rows


def _metric_summary(metric: ImpactMetric, status: str) -> dict[str, Any]:
    return {
        "area": metric.area,
        "metric": metric.metric,
        "status": status,
        "before": metric.before,
        "after": metric.after,
        "delta": metric.delta,
        "result": metric.result,
        "evidence": metric.snapshot_kind or "impact_audit",
        "summary": f"{metric.metric} {status}: {metric.before} -> {metric.after} (delta {metric.delta})",
    }


def _repository_context(
    observation: RepositoryObservation, policy: SnapshotPolicyAudit
) -> dict[str, Any]:
    if not observation.repository_status_available:
        state = "repository context unavailable"
    elif observation.repository_dirty:
        state = "dirty repository"
    else:
        state = "clean repository"
    return {
        "health": policy.repository_context_health,
        "state": state,
        "vcs": observation.repository_vcs,
        "head_commit": observation.repository_head_commit,
        "branch": observation.repository_branch,
        "dirty": observation.repository_dirty,
        "status_available": observation.repository_status_available,
        "reason": policy.repository_context_reason,
    }


def _confidence(
    impact: ImpactAudit,
    policy: SnapshotPolicyAudit,
    unsupported: list[dict[str, str]],
) -> dict[str, Any]:
    comparable = sum(1 for row in impact.coverage if row.comparison_data)
    constrained = [row.surface for row in policy.operational_surfaces if row.snapshot_health != "healthy"]
    if comparable >= 2 and policy.repository_context_health == "healthy" and not constrained:
        level: ConfidenceLevel = "high"
        reason = "snapshot comparisons and clean repository context are available"
    elif comparable and policy.repository_context_health != "missing":
        level = "partial"
        reason = "some comparisons are available, with repository context present"
    elif comparable:
        level = "snapshot_constrained"
        reason = "comparison snapshots exist but repository context is missing"
    else:
        level = "unknown"
        reason = "insufficient comparison history"
    return {
        "level": level,
        "comparison": "available" if comparable else "insufficient comparison history",
        "snapshot_constrained_surfaces": constrained,
        "repository_context_health": policy.repository_context_health,
        "correlation": "visible when repository and operational state are both observed",
        "causation": "not proven",
        "reason": reason,
        "unsupported_count": len(unsupported),
    }


def _unsupported(
    impact: ImpactAudit, policy: SnapshotPolicyAudit) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for missing in impact.missing:
        rows.append({"conclusion": missing, "reason": "insufficient comparison history"})
    for metric in impact.metrics:
        if metric.availability != "comparable":
            rows.append(
                {
                    "conclusion": f"{metric.metric} change magnitude",
                    "reason": metric.note or metric.availability,
                }
            )
    if policy.repository_context_health == "missing":
        rows.append(
            {
                "conclusion": "repository-state comparison",
                "reason": policy.repository_context_reason,
            }
        )
    rows.append(
        {
            "conclusion": "causal link between repository change and operational change",
            "reason": "correlation may be visible, but causation is not proven by existing surfaces",
        }
    )
    return rows


def _format_items(items: list[dict[str, Any]]) -> list[str]:
    if not items:
        return ["  none"]
    return [f"  - {item.get('summary') or item.get('conclusion')}: {item.get('reason') or item.get('evidence', '')}" for item in items]
