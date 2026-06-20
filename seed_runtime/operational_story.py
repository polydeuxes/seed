"""Read-only operational story view composed from existing visibility surfaces."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from seed_runtime.capability_needs import CapabilityNeedEntry, build_capability_needs
from seed_runtime.correlation_audit import CorrelationFinding, build_correlation_audit
from seed_runtime.impact_audit import ImpactMetric, build_impact_audit
from seed_runtime.investigation_path_audit import build_investigation_path_audit
from seed_runtime.pressure_audit import PressureItem, build_pressure_audit
from seed_runtime.privilege_discovery import (
    PrivilegeDiscoveryCapability,
    build_privilege_discovery,
)
from seed_runtime.state import State


@dataclass(frozen=True)
class OperationalStory:
    focus: str
    pressure: dict[str, Any]
    supporting_evidence: list[str]
    capabilities: list[dict[str, Any]]
    constraints: list[dict[str, Any]]
    correlation_gaps: list[dict[str, Any]]
    impact: dict[str, Any]
    recent_changes: list[str]
    observed_outcomes: list[str]
    investigation_path: list[dict[str, str]]
    unknowns: list[dict[str, str]]
    boundary: dict[str, bool | str]

    def to_json_dict(self) -> dict[str, Any]:
        return {
            "focus": self.focus,
            "pressure": self.pressure,
            "supporting_evidence": self.supporting_evidence,
            "capabilities": self.capabilities,
            "constraints": self.constraints,
            "correlation_gaps": self.correlation_gaps,
            "impact": self.impact,
            "recent_changes": self.recent_changes,
            "observed_outcomes": self.observed_outcomes,
            "investigation_path": self.investigation_path,
            "unknowns": self.unknowns,
            "boundary": self.boundary,
        }


def build_operational_story(
    state: State, *, repo_root: str | Path | None = None
) -> OperationalStory:
    """Compose current operational evidence without planning, recording, or mutation."""

    root = (
        Path(repo_root)
        if repo_root is not None
        else Path(__file__).resolve().parents[1]
    )
    pressure_audit = build_pressure_audit(state, repo_root=root)
    capability_needs = build_capability_needs(state)
    privilege = build_privilege_discovery(state)
    correlation = build_correlation_audit(state, repo_root=root)
    impact = build_impact_audit(root)
    primary = pressure_audit.pressures[0] if pressure_audit.pressures else None
    investigation = build_investigation_path_audit(_domain_for(primary))

    unknowns: list[dict[str, str]] = []
    if not pressure_audit.pressures:
        unknowns.append(
            {
                "area": "pressure",
                "reason": "no operational pressure identified by current audit inputs",
            }
        )
    if not capability_needs:
        unknowns.append(
            {
                "area": "capabilities",
                "reason": "no capability needs identified by current audit inputs",
            }
        )
    if impact.overall == "unknown":
        unknowns.append({"area": "impact", "reason": _impact_unknown_reason(impact.metrics)})

    return OperationalStory(
        focus=_focus(primary),
        pressure=_pressure(primary),
        supporting_evidence=_supporting_evidence(primary),
        capabilities=[_capability(entry) for entry in capability_needs],
        constraints=[_constraint(cap) for cap in privilege.capabilities],
        correlation_gaps=[
            _correlation(finding) for finding in correlation.findings
        ],
        impact={
            "overall": impact.overall,
            "missing": list(impact.missing),
            "metrics": [_metric(m) for m in impact.metrics],
        },
        recent_changes=_recent_changes(impact.metrics),
        observed_outcomes=_observed_outcomes(impact.metrics),
        investigation_path=[
            {"surface": step.name, "purpose": step.purpose}
            for step in investigation.surfaces
        ],
        unknowns=unknowns,
        boundary={
            "mode": "read_only_view",
            "records_facts": False,
            "writes_event_ledger": False,
            "mutates_cluster": False,
        },
    )


def operational_story_json(story: OperationalStory) -> dict[str, Any]:
    return story.to_json_dict()


def format_operational_story(story: OperationalStory) -> str:
    lines = [
        "Operational Story",
        "",
        "Current Focus:",
        f"  {story.focus}",
        "",
        "Primary Pressure:",
    ]
    lines.append(f"  {story.pressure.get('summary', 'none observed')}")
    lines.extend(["", "Supporting Evidence:"])
    lines.extend(_bullets(story.supporting_evidence, "none observed"))
    lines.extend(["", "Missing Capabilities:"])
    lines.extend(
        _bullets(
            [
                f"{c['capability']} ({c['subjects']} subject(s))"
                for c in story.capabilities
            ],
            "none observed",
        )
    )
    lines.extend(["", "Access Constraints:"])
    lines.extend(
        _bullets(
            [
                f"{c['capability']}: {c['access_level']} - {c['notes']}"
                for c in story.constraints
            ],
            "none observed",
        )
    )
    lines.extend(["", "Observed Correlation Gaps:"])
    lines.extend(
        _bullets(
            [
                f"{c['area']}: {c['assessment']} "
                f"(boundary: {c['candidate_boundary']})"
                for c in story.correlation_gaps
            ],
            "none observed",
        )
    )
    lines.extend(["", "Recent Changes:"])
    lines.extend(_bullets(story.recent_changes, "unknown"))
    lines.extend(["", "Observed Outcomes:"])
    lines.extend(_bullets(story.observed_outcomes, "unknown"))
    lines.extend(["", "Current Investigation Path:"])
    lines.extend(
        _bullets(
            [
                f"{s['surface']}: {s['purpose']}"
                for s in story.investigation_path
            ],
            "none available",
        )
    )
    if story.unknowns:
        lines.extend(["", "Unknowns:"])
        lines.extend(f"  - {u['area']}: {u['reason']}" for u in story.unknowns)
    lines.extend(
        [
            "",
            "Boundary:",
            "  read-only view; no recording, event ledger writes, cluster mutation, "
            "plans, or implementation advice",
        ]
    )
    return "\n".join(lines)


def _focus(primary: PressureItem | None) -> str:
    return primary.category.lower() if primary else "no current pressure focus identified"

def _pressure(primary: PressureItem | None) -> dict[str, Any]:
    if primary is None:
        return {"summary": "none observed", "score": 0, "evidence": {}}
    return {
        "category": primary.category,
        "score": primary.score,
        "summary": f"{primary.score} {primary.category.lower()} pressure point(s)",
        "reason": primary.reason,
        "evidence": primary.evidence,
    }

def _supporting_evidence(primary: PressureItem | None) -> list[str]:
    if primary is None:
        return []
    return [primary.reason, *[f"{k}: {v}" for k, v in primary.evidence.items()]]

def _capability(entry: CapabilityNeedEntry) -> dict[str, Any]:
    return {
        "capability": entry.capability,
        "subjects": len(entry.subjects),
        "diagnostics": sorted(entry.diagnostics),
        "needed_evidence": sorted(entry.needed_evidence),
    }

def _constraint(cap: PrivilegeDiscoveryCapability) -> dict[str, Any]:
    return {
        "capability": cap.name,
        "access_level": cap.access_level,
        "pressure": cap.pressure,
        "operational_benefit": cap.operational_benefit,
        "notes": cap.notes,
    }

def _correlation(finding: CorrelationFinding) -> dict[str, Any]:
    return {
        "area": finding.area,
        "assessment": finding.assessment,
        "candidate_boundary": finding.candidate_boundary,
        "evidence_present": finding.evidence_present,
        "observed_result": finding.observed_result,
    }

def _metric(metric: ImpactMetric) -> dict[str, Any]:
    return metric.to_json_dict()

def _recent_changes(metrics: list[ImpactMetric]) -> list[str]:
    return [
        f"{m.area}/{m.metric}: {m.before} -> {m.after}"
        for m in metrics
        if m.availability == "comparable"
    ]

def _observed_outcomes(metrics: list[ImpactMetric]) -> list[str]:
    return [f"{m.area}/{m.metric}: {m.result}" for m in metrics]

def _impact_unknown_reason(metrics: list[ImpactMetric]) -> str:
    unavailable = [m for m in metrics if m.availability != "comparable"]
    if unavailable:
        return "; ".join(
            f"{m.metric} is {m.availability}: {m.note}"
            for m in unavailable[:3]
        )
    return "no comparable impact metrics are currently available"

def _domain_for(primary: PressureItem | None) -> str:
    if primary and "ownership" in primary.category.lower():
        return "ownership"
    if primary and "capability" in primary.category.lower():
        return "capability"
    return "operational"

def _bullets(values: list[str], empty: str) -> list[str]:
    return [f"  - {value}" for value in values] if values else [f"  {empty}"]
