"""Read-only visibility into implementation-selected comparison references."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from seed_runtime.impact_audit import build_impact_audit
from seed_runtime.snapshot_policy_audit import build_snapshot_policy_audit


@dataclass(frozen=True)
class _ReferenceChoicePayload:
    selected_reference: dict[str, Any]


@dataclass(frozen=True)
class _ComparisonLineagePayload:
    selection_rationale: list[str]
    alternative_references: list[dict[str, Any]]
    limitations: list[str]


@dataclass(frozen=True)
class ReferenceSelection:
    domain: str
    question: str
    selected_reference: dict[str, Any]
    selection_rationale: list[str]
    alternative_references: list[dict[str, Any]]
    authority_boundary: dict[str, Any]
    limitations: list[str]
    writes_event_ledger: bool = False
    mutates_cluster: bool = False

    def to_json_dict(self) -> dict[str, Any]:
        return {
            "domain": self.domain,
            "question": self.question,
            "selected_reference": self.selected_reference,
            "selection_rationale": self.selection_rationale,
            "alternative_references": self.alternative_references,
            "authority_boundary": self.authority_boundary,
            "limitations": self.limitations,
            "writes_event_ledger": self.writes_event_ledger,
            "mutates_cluster": self.mutates_cluster,
        }


def build_reference_selection(repo_root: Path, domain: str) -> ReferenceSelection:
    if domain != "history":
        return _reference_selection_from_payloads(
            domain=domain,
            question="unknown",
            choice=_ReferenceChoicePayload(selected_reference={"status": "unknown"}),
            lineage=_ComparisonLineagePayload(
                selection_rationale=["unsupported reference-selection domain"],
                alternative_references=[
                    {
                        "reference": "unknown",
                        "reason": "implementation does not currently expose candidate alternatives for this domain",
                    }
                ],
                limitations=["only the history domain is currently implementation-backed"],
            ),
        )
    return _build_history_reference_selection(repo_root)


def _reference_selection_from_payloads(
    *,
    domain: str,
    question: str,
    choice: _ReferenceChoicePayload,
    lineage: _ComparisonLineagePayload,
) -> ReferenceSelection:
    return ReferenceSelection(
        domain=domain,
        question=question,
        selected_reference=choice.selected_reference,
        selection_rationale=lineage.selection_rationale,
        alternative_references=lineage.alternative_references,
        authority_boundary=_authority_boundary(),
        limitations=lineage.limitations,
    )


def reference_selection_json(selection: ReferenceSelection) -> dict[str, Any]:
    return selection.to_json_dict()


def format_reference_selection(selection: ReferenceSelection) -> str:
    lines = [
        "Reference Selection",
        "",
        "Domain:",
        f"  {selection.domain}",
        "",
        "Question:",
        f"  {selection.question}",
        "",
        "Selected Reference:",
    ]
    lines.extend(_format_mapping(selection.selected_reference))
    lines.extend(["", "Selection Rationale:"])
    lines.extend(_format_list(selection.selection_rationale))
    lines.extend(["", "Alternative References:"])
    if selection.alternative_references:
        for row in selection.alternative_references:
            lines.append(f"  - {row.get('reference', 'unknown')}")
            if row.get("reason"):
                lines.append(f"    reason: {row['reason']}")
            if row.get("authority"):
                lines.append(f"    authority: {row['authority']}")
    else:
        lines.append("  - unknown")
        lines.append(
            "    reason: implementation does not currently expose candidate alternatives"
        )
    lines.extend(["", "Authority Boundary:"])
    lines.extend(_format_mapping(selection.authority_boundary))
    lines.extend(["", "Known Limitations:"])
    lines.extend(_format_list(selection.limitations))
    return "\n".join(lines)


def _build_history_reference_selection(repo_root: Path) -> ReferenceSelection:
    impact = build_impact_audit(repo_root)
    policy = build_snapshot_policy_audit(repo_root)
    comparable = [
        {"snapshot_kind": kind, **pair}
        for kind, pair in sorted(impact.snapshots.items())
    ]
    if comparable:
        selected = {
            "reference": "previous comparable snapshot",
            "status": "selected",
            "comparable_snapshot_pairs": comparable,
        }
        rationale = [
            "impact_audit compares the latest comparable snapshot pair for each supported snapshot kind",
            "history_brief builds historical comparison from impact_audit and snapshot_policy_audit outputs",
        ]
    else:
        selected = {
            "reference": "unknown",
            "status": "unavailable",
            "reason": "no supported snapshot kind currently has a comparable snapshot pair",
        }
        rationale = [
            "history comparison requires at least two comparable snapshots for a supported snapshot kind"
        ]
    alternatives = _history_alternatives(policy)
    limitations = [
        "visibility only; does not create accepted baselines or expectations",
        "candidate alternatives are limited to existing snapshot-policy and repository-observation evidence",
        "no baseline storage, lifecycle, registry, persistence, runtime behavior, or policy is introduced",
    ]
    if not alternatives:
        alternatives = [
            {
                "reference": "unknown",
                "reason": "implementation does not currently expose candidate alternatives",
            }
        ]
    return _reference_selection_from_payloads(
        domain="history",
        question="historical comparison",
        choice=_ReferenceChoicePayload(selected_reference=selected),
        lineage=_ComparisonLineagePayload(
            selection_rationale=rationale,
            alternative_references=alternatives,
            limitations=limitations,
        ),
    )


def _history_alternatives(policy) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for kind in policy.snapshot_kinds:
        if kind.latest_snapshot:
            rows.append(
                {
                    "reference": f"latest {kind.kind} snapshot",
                    "authority": "candidate reference",
                    "reason": "snapshot_policy_audit exposes a latest snapshot, but latest-only evidence is not a historical comparison pair",
                }
            )
    if policy.repository_context.repository_status_available:
        rows.append(
            {
                "reference": "repository-context-constrained snapshot",
                "authority": "candidate reference",
                "reason": "repository_observation exposes repository context that can constrain interpretation without becoming a baseline",
            }
        )
    return rows


def _authority_boundary() -> dict[str, Any]:
    return {
        "selected_authority": "implementation-selected reference",
        "candidate_reference": "alternative only when exposed by implementation evidence",
        "accepted_reference": False,
        "expectation_bearing_reference": False,
        "read_only": True,
        "recording": "none",
        "writes_event_ledger": False,
        "mutates_cluster": False,
    }


def _format_mapping(mapping: dict[str, Any]) -> list[str]:
    if not mapping:
        return ["  unknown"]
    lines = []
    for key, value in mapping.items():
        if isinstance(value, list):
            lines.append(f"  {key}: {value if value else 'none'}")
        else:
            lines.append(f"  {key}: {value}")
    return lines


def _format_list(items: list[str]) -> list[str]:
    return [f"  - {item}" for item in items] if items else ["  - unknown"]
