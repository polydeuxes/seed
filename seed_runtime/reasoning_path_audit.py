"""Read-only evidence-backed derivation paths for operational conclusions."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from seed_runtime.capability_needs import build_capability_needs
from seed_runtime.operational_story import build_operational_story
from seed_runtime.ownership_discrepancies import (
    build_ownership_discrepancies,
    diagnostic_capability_need_records,
)
from seed_runtime.pressure_audit import build_pressure_audit
from seed_runtime.privilege_discovery import build_privilege_discovery
from seed_runtime.state import State
from seed_runtime.typed_unknowns import (
    TypedUnknownRecord,
    preserve_typed_unknown,
    typed_unknowns_to_public_dicts,
)


@dataclass(frozen=True)
class _DerivedConclusionPayload:
    """Implementation-local derived conclusions separated from their lineage."""

    intermediate_conclusions: list[dict[str, Any]]
    derived_conclusions: list[dict[str, Any]]


@dataclass(frozen=True)
class _DerivationSupportingEvidencePayload:
    """Implementation-local supporting evidence for derived conclusions."""

    evidence: list[dict[str, Any]]


@dataclass(frozen=True)
class _DerivationLineagePayload:
    """Implementation-local derivation path consumers and limitations."""

    consumers: list[dict[str, Any]]
    story_impact: list[dict[str, Any]]
    unknowns: list[TypedUnknownRecord]


@dataclass(frozen=True)
class ReasoningPathAudit:
    domain: str
    subject: str
    evidence: list[dict[str, Any]] = field(default_factory=list)
    intermediate_conclusions: list[dict[str, Any]] = field(default_factory=list)
    derived_conclusions: list[dict[str, Any]] = field(default_factory=list)
    consumers: list[dict[str, Any]] = field(default_factory=list)
    story_impact: list[dict[str, Any]] = field(default_factory=list)
    unknowns: list[dict[str, str]] = field(default_factory=list)
    boundary: dict[str, bool | str] = field(
        default_factory=lambda: {
            "mode": "read_only_reasoning_audit",
            "records_facts": False,
            "writes_event_ledger": False,
            "mutates_cluster": False,
        }
    )

    def to_json_dict(self) -> dict[str, Any]:
        return {
            "domain": self.domain,
            "subject": self.subject,
            "evidence": self.evidence,
            "intermediate_conclusions": self.intermediate_conclusions,
            "derived_conclusions": self.derived_conclusions,
            "consumers": self.consumers,
            "story_impact": self.story_impact,
            "unknowns": self.unknowns,
            "boundary": self.boundary,
        }


def build_reasoning_path_audit(
    state: State,
    domain: str,
    subject: str,
    *,
    repo_root: str | Path | None = None,
) -> ReasoningPathAudit:
    """Build a derivation path only from implemented diagnostic surfaces."""

    root = (
        Path(repo_root)
        if repo_root is not None
        else Path(__file__).resolve().parents[1]
    )
    consumers: list[dict[str, Any]] = []
    story_impact: list[dict[str, Any]] = []

    rows = build_ownership_discrepancies(state)
    needs = build_capability_needs(state)
    pressure = build_pressure_audit(state, repo_root=root)
    privilege = build_privilege_discovery(state)
    story = build_operational_story(state, repo_root=root)

    relevant_rows = _reasoning_path_relevant_ownership_rows(rows, subject)
    supporting_evidence_payload = _reasoning_path_supporting_evidence_payload(
        relevant_rows
    )

    intermediate = _reasoning_path_intermediate_conclusions(relevant_rows)
    derived = _reasoning_path_derived_capability_conclusions(relevant_rows, subject)

    consumers.extend(_reasoning_path_capability_need_consumers(needs, subject))
    for need in needs:
        if _matches(subject, need.capability, *need.subjects, *need.diagnostics):
            if not any(d.get("surface") == "capability_needs" for d in derived):
                derived.append(
                    {
                        "conclusion": f"{need.capability} capability need",
                        "surface": "capability_needs",
                        "subjects": sorted(need.subjects),
                        "needed_evidence": sorted(need.needed_evidence),
                    }
                )

    for item in pressure.pressures:
        text = f"{item.category} {item.reason} {item.evidence}"
        if subject.lower() in text.lower() or domain.lower() in item.category.lower():
            consumers.append(
                {
                    "surface": "pressure_audit",
                    "reason": item.reason,
                    "category": item.category,
                    "score": item.score,
                }
            )
    for cap in privilege.capabilities:
        if _matches(subject, cap.name):
            consumers.append(
                {
                    "surface": "privilege_discovery",
                    "reason": "explains access boundary for the derived capability need",
                    "access_level": cap.access_level,
                    "pressure": cap.pressure,
                }
            )
    if (
        subject.lower() in str(story.to_json_dict()).lower()
        or domain.lower() in story.focus.lower()
    ):
        story_impact.append(
            {
                "surface": "operational_story",
                "focus": story.focus,
                "pressure": story.pressure,
                "reason": "operational story includes this subject, domain, or derived pressure",
            }
        )
        consumers.append(
            {
                "surface": "operational_story",
                "reason": "composes current focus and investigation path from pressure and capability surfaces",
            }
        )

    unknowns: list[TypedUnknownRecord] = []
    if not (
        supporting_evidence_payload.evidence
        or intermediate
        or derived
        or consumers
        or story_impact
    ):
        unknowns.append(
            preserve_typed_unknown(
                unknown_type="Evidence Gap",
                area="derivation",
                reason="no derivation evidence currently available",
            )
        )
    conclusion_payload = _DerivedConclusionPayload(
        intermediate_conclusions=intermediate,
        derived_conclusions=derived,
    )
    lineage_payload = _DerivationLineagePayload(
        consumers=_dedupe(consumers),
        story_impact=story_impact,
        unknowns=unknowns,
    )
    return _reasoning_path_from_payloads(
        domain,
        subject,
        conclusions=conclusion_payload,
        supporting_evidence=supporting_evidence_payload,
        lineage=lineage_payload,
    )


def _reasoning_path_capability_need_consumers(
    needs: list[Any], subject: str
) -> list[dict[str, Any]]:
    """Preserve capability-needs consumers for a reasoning-path subject."""

    return [
        {
            "surface": "capability_needs",
            "reason": "reports derived diagnostic capability need",
            "subjects": sorted(need.subjects),
            "diagnostics": sorted(need.diagnostics),
        }
        for need in needs
        if _matches(subject, need.capability, *need.subjects, *need.diagnostics)
    ]


def _reasoning_path_relevant_ownership_rows(
    rows: list[Any], subject: str
) -> list[Any]:
    """Select ownership rows relevant to a reasoning-path subject."""

    return [
        row
        for row in rows
        if _matches(subject, row.subject, row.conflict)
        or any(
            _matches(
                subject, rec.get("candidate_capability"), rec.get("diagnostic_conflict")
            )
            for rec in diagnostic_capability_need_records(row)
        )
    ]


def _reasoning_path_intermediate_conclusions(
    relevant_rows: list[Any],
) -> list[dict[str, Any]]:
    """Derive implementation-local intermediate conclusions from selected rows."""

    return [
        {
            "conclusion": "ownership attribution incomplete",
            "surface": "ownership_discrepancies",
            "subject": row.subject,
            "reason": row.conflict,
        }
        for row in relevant_rows
        if row.conflict
    ]


def _reasoning_path_derived_capability_conclusions(
    relevant_rows: list[Any], subject: str
) -> list[dict[str, Any]]:
    """Derive capability conclusions from selected ownership rows."""

    derived: list[dict[str, Any]] = []
    for row in relevant_rows:
        for rec in diagnostic_capability_need_records(row):
            if _matches(
                subject,
                rec.get("candidate_capability"),
                rec.get("diagnostic_conflict"),
                row.subject,
            ):
                derived.append(
                    {
                        "conclusion": f"{rec['candidate_capability']} capability need",
                        "surface": "capability_needs",
                        "subject": row.subject,
                        "needed_evidence": rec.get("needed_evidence"),
                        "source_conflict": rec.get("diagnostic_conflict"),
                    }
                )
    return derived


def _reasoning_path_supporting_evidence_payload(
    relevant_rows: list[Any],
) -> _DerivationSupportingEvidencePayload:
    """Build implementation-local supporting evidence from selected source rows."""

    return _DerivationSupportingEvidencePayload(
        evidence=[
            {
                "surface": "ownership_discrepancies",
                "subject": row.subject,
                "finding": row.conflict or "ownership_candidate",
                "reason": row.reason,
                "evidence_count": row.evidence_count,
            }
            for row in relevant_rows
        ]
    )


def _reasoning_path_from_payloads(
    domain: str,
    subject: str,
    *,
    conclusions: _DerivedConclusionPayload,
    supporting_evidence: _DerivationSupportingEvidencePayload,
    lineage: _DerivationLineagePayload,
) -> ReasoningPathAudit:
    return ReasoningPathAudit(
        domain,
        subject,
        supporting_evidence.evidence,
        conclusions.intermediate_conclusions,
        conclusions.derived_conclusions,
        lineage.consumers,
        lineage.story_impact,
        typed_unknowns_to_public_dicts(lineage.unknowns),
    )


def reasoning_path_audit_json(audit: ReasoningPathAudit) -> dict[str, Any]:
    return audit.to_json_dict()


def format_reasoning_path_audit(audit: ReasoningPathAudit) -> str:
    title = "Reasoning Path" if not audit.unknowns else "Reasoning Path Incomplete"
    lines = [
        title,
        "",
        "Subject:",
        f"  {audit.subject}",
        "",
        "Domain:",
        f"  {audit.domain}",
    ]
    for heading, values in (
        ("Observed Evidence", audit.evidence),
        ("Intermediate Conclusions", audit.intermediate_conclusions),
        ("Derived Conclusions", audit.derived_conclusions),
        ("Consumers", audit.consumers),
        ("Story Impact", audit.story_impact),
    ):
        lines.extend(["", f"{heading}:"])
        lines.extend(_items(values))
    if audit.unknowns:
        lines.extend(["", "Unknowns:"])
        lines.extend(f"  - {u['area']}: {u['reason']}" for u in audit.unknowns)
    lines.extend(
        [
            "",
            "Boundary:",
            "  read-only; no recording, event ledger writes, or cluster mutation",
        ]
    )
    return "\n".join(lines)


def _matches(needle: str, *values: object) -> bool:
    n = needle.lower()
    return any(
        n == str(v).lower() or n in str(v).lower() for v in values if v is not None
    )


def _items(values: list[dict[str, Any]]) -> list[str]:
    if not values:
        return ["  none observed"]
    return ["  - " + "; ".join(f"{k}={v}" for k, v in item.items()) for item in values]


def _dedupe(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen = set()
    out = []
    for item in items:
        key = tuple(sorted((k, str(v)) for k, v in item.items()))
        if key not in seen:
            seen.add(key)
            out.append(item)
    return out
