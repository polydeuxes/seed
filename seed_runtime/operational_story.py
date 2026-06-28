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
    investigation_path: list[dict[str, str | int]]
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


@dataclass(frozen=True)
class _OperationalStoryAnswerPayload:
    """Implementation-local bounded answer material for the story surface."""

    focus: str
    pressure: dict[str, Any]
    capabilities: list[dict[str, Any]]
    constraints: list[dict[str, Any]]
    correlation_gaps: list[dict[str, Any]]
    impact: dict[str, Any]
    recent_changes: list[str]
    observed_outcomes: list[str]


@dataclass(frozen=True)
class _OperationalStoryLimitationsPayload:
    """Implementation-local incompleteness and unavailable authority material."""

    unknowns: list[dict[str, str]]


@dataclass(frozen=True)
class _OperationalStoryReasoningPayload:
    """Implementation-local reason material explaining the story answer."""

    investigation_path: list[dict[str, str | int]]


@dataclass(frozen=True)
class _OperationalStorySupportingEvidencePayload:
    """Implementation-local implementation evidence supporting story reasons."""

    supporting_evidence: list[str]


@dataclass(frozen=True)
class _OperationalStoryBoundaryPayload:
    """Implementation-local authority boundary limiting story conclusions."""

    boundary: dict[str, bool | str]


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

    (
        answer_payload,
        reasoning_payload,
        supporting_evidence_payload,
        boundary_payload,
        limitations_payload,
    ) = (
        _compose_operational_story_payloads(
            primary=primary,
            capability_needs=capability_needs,
            privilege_capabilities=privilege.capabilities,
            correlation_findings=correlation.findings,
            impact_metrics=impact.metrics,
            impact_overall=impact.overall,
            impact_missing=impact.missing,
            investigation_surfaces=investigation.surfaces,
            has_pressures=bool(pressure_audit.pressures),
        )
    )

    return OperationalStory(
        focus=answer_payload.focus,
        pressure=answer_payload.pressure,
        supporting_evidence=supporting_evidence_payload.supporting_evidence,
        capabilities=answer_payload.capabilities,
        constraints=answer_payload.constraints,
        correlation_gaps=answer_payload.correlation_gaps,
        impact=answer_payload.impact,
        recent_changes=answer_payload.recent_changes,
        observed_outcomes=answer_payload.observed_outcomes,
        investigation_path=reasoning_payload.investigation_path,
        unknowns=limitations_payload.unknowns,
        boundary=boundary_payload.boundary,
    )


def _compose_operational_story_payloads(
    *,
    primary: PressureItem | None,
    capability_needs: list[CapabilityNeedEntry],
    privilege_capabilities: tuple[PrivilegeDiscoveryCapability, ...],
    correlation_findings: tuple[CorrelationFinding, ...],
    impact_metrics: list[ImpactMetric],
    impact_overall: str,
    impact_missing: list[str],
    investigation_surfaces,
    has_pressures: bool,
) -> tuple[
    _OperationalStoryAnswerPayload,
    _OperationalStoryReasoningPayload,
    _OperationalStorySupportingEvidencePayload,
    _OperationalStoryBoundaryPayload,
    _OperationalStoryLimitationsPayload,
]:
    """Separate answer, reason, support, authority boundary, and limitations."""

    unknowns: list[dict[str, str]] = []
    if not has_pressures:
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
    if impact_overall == "unknown":
        unknowns.append(
            {"area": "impact", "reason": _impact_unknown_reason(impact_metrics)}
        )

    answer = _OperationalStoryAnswerPayload(
        focus=_focus(primary),
        pressure=_pressure(primary),
        capabilities=[_capability(entry) for entry in capability_needs],
        constraints=[_constraint(cap) for cap in privilege_capabilities],
        correlation_gaps=[_correlation(finding) for finding in correlation_findings],
        impact={
            "overall": impact_overall,
            "missing": list(impact_missing),
            "metrics": [_metric(m) for m in impact_metrics],
        },
        recent_changes=_recent_changes(impact_metrics),
        observed_outcomes=_observed_outcomes(impact_metrics),
    )
    reasoning = _OperationalStoryReasoningPayload(
        investigation_path=[
            {"surface": step.name, "reason": step.reason, "order": step.order}
            for step in investigation_surfaces
        ],
    )
    supporting_evidence = _OperationalStorySupportingEvidencePayload(
        supporting_evidence=_supporting_evidence(primary),
    )
    boundary = _OperationalStoryBoundaryPayload(
        boundary={
            "mode": "read_only_view",
            "records_facts": False,
            "writes_event_ledger": False,
            "mutates_cluster": False,
        },
    )
    limitations = _OperationalStoryLimitationsPayload(unknowns=unknowns)
    return answer, reasoning, supporting_evidence, boundary, limitations


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
            [f"{s['surface']}: {s['reason']}" for s in story.investigation_path],
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
    return (
        primary.category.lower() if primary else "no current pressure focus identified"
    )


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
            f"{m.metric} is {m.availability}: {m.note}" for m in unavailable[:3]
        )
    return "no comparable impact metrics are currently available"


def _domain_for(primary: PressureItem | None) -> str:
    if primary is None:
        return "operational"
    category = primary.category.lower()
    reason = primary.reason.lower()
    if "ownership" in category or "ownership" in reason:
        return "ownership"
    if "capability" in category or "capability" in reason:
        return "capability"
    if "consumer" in category or "consumer" in reason or "orphaned" in category:
        return "consumer"
    if "correlation" in category or "correlation" in reason:
        return "correlation"
    if "pressure" in category or "pressure" in reason:
        return "pressure"
    return "operational"


def _bullets(values: list[str], empty: str) -> list[str]:
    return [f"  - {value}" for value in values] if values else [f"  {empty}"]
