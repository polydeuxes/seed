"""Read-only selection trace visibility for operational conclusions."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from seed_runtime.operational_story import build_operational_story
from seed_runtime.pressure_audit import PressureItem, build_pressure_audit
from seed_runtime.state import State


@dataclass(frozen=True)
class _SelectionResultPayload:
    selected: str
    outcome: dict[str, Any]


@dataclass(frozen=True)
class _SelectionLineagePayload:
    candidates: list[dict[str, Any]]
    selection_factors: list[str]
    non_selected: list[dict[str, Any]]
    evidence: list[dict[str, Any]]
    unknowns: list[dict[str, str]]


@dataclass(frozen=True)
class SelectionPathAudit:
    target: str
    selected: str
    candidates: list[dict[str, Any]] = field(default_factory=list)
    selection_factors: list[str] = field(default_factory=list)
    non_selected: list[dict[str, Any]] = field(default_factory=list)
    evidence: list[dict[str, Any]] = field(default_factory=list)
    outcome: dict[str, Any] = field(default_factory=dict)
    unknowns: list[dict[str, str]] = field(default_factory=list)
    boundary: dict[str, bool | str] = field(
        default_factory=lambda: {
            "mode": "read_only_selection_audit",
            "records_facts": False,
            "writes_event_ledger": False,
            "mutates_cluster": False,
        }
    )

    def to_json_dict(self) -> dict[str, Any]:
        return {
            "target": self.target,
            "selected": self.selected,
            "candidates": self.candidates,
            "selection_factors": self.selection_factors,
            "non_selected": self.non_selected,
            "evidence": self.evidence,
            "outcome": self.outcome,
            "unknowns": self.unknowns,
            "boundary": self.boundary,
        }


def build_selection_path_audit(
    state: State,
    target: str,
    *,
    repo_root: str | Path | None = None,
) -> SelectionPathAudit:
    """Explain implemented selection evidence without changing selection behavior."""

    root = (
        Path(repo_root)
        if repo_root is not None
        else Path(__file__).resolve().parents[1]
    )
    normalized = _normalize_target(target)
    pressure = build_pressure_audit(state, repo_root=root)
    story = build_operational_story(state, repo_root=root)

    if normalized in {"current_focus", "primary_pressure"} or _matches_target(
        normalized, story.focus
    ):
        selected_item = pressure.pressures[0] if pressure.pressures else None
        selected = (
            story.focus
            if normalized == "current_focus"
            else _selected_name(selected_item, story.focus)
        )
        return _from_pressure_selection(
            target, selected, pressure.pressures, story.focus
        )

    matching = [
        item
        for item in pressure.pressures
        if _matches_target(normalized, item.category)
    ]
    if matching:
        selected_item = pressure.pressures[0] if pressure.pressures else None
        return _from_pressure_selection(
            target,
            _selected_name(selected_item, story.focus),
            pressure.pressures,
            story.focus,
        )

    return _selection_path_from_payloads(
        target=target,
        result=_SelectionResultPayload(
            selected="unknown",
            outcome={
                "selected": "unknown",
                "reason": "target is not an implemented selection surface",
            },
        ),
        lineage=_SelectionLineagePayload(
            candidates=[
                _candidate(item, index)
                for index, item in enumerate(pressure.pressures, start=1)
            ],
            selection_factors=["unknown"],
            non_selected=[],
            evidence=[],
            unknowns=[
                {
                    "area": "selection_logic",
                    "reason": "no implementation-backed selection evidence discovered for target",
                }
            ],
        ),
    )


def _selection_path_from_payloads(
    *,
    target: str,
    result: _SelectionResultPayload,
    lineage: _SelectionLineagePayload,
) -> SelectionPathAudit:
    return SelectionPathAudit(
        target=target,
        selected=result.selected,
        candidates=lineage.candidates,
        selection_factors=lineage.selection_factors,
        non_selected=lineage.non_selected,
        evidence=lineage.evidence,
        outcome=result.outcome,
        unknowns=lineage.unknowns,
    )


def selection_path_audit_json(audit: SelectionPathAudit) -> dict[str, Any]:
    return audit.to_json_dict()


def format_selection_path_audit(audit: SelectionPathAudit) -> str:
    lines = [
        "Selection Path",
        "",
        "Target:",
        f"  {audit.target}",
        "",
        "Selected:",
        f"  {audit.selected}",
    ]
    lines.extend(["", "Candidate Set:"])
    lines.extend(_items(audit.candidates, lambda c: f"{c['candidate']} ({c['score']})"))
    lines.extend(["", "Selection Factors:"])
    lines.extend(_bullets(audit.selection_factors, "unknown"))
    lines.extend(["", "Non-selected Candidates:"])
    lines.extend(
        _items(audit.non_selected, lambda c: f"{c['candidate']}: {c['reason']}")
    )
    lines.extend(["", "Evidence:"])
    lines.extend(
        _items(audit.evidence, lambda e: "; ".join(f"{k}={v}" for k, v in e.items()))
    )
    if audit.unknowns:
        lines.extend(["", "Unknowns:"])
        lines.extend(f"  - {u['area']}: {u['reason']}" for u in audit.unknowns)
    lines.extend(
        [
            "",
            "Outcome:",
            f"  {audit.outcome.get('summary', audit.outcome.get('reason', 'unknown'))}",
        ]
    )
    lines.extend(
        [
            "",
            "Boundary:",
            "  read-only; no recording, event ledger writes, or cluster mutation",
        ]
    )
    return "\n".join(lines)


def _from_pressure_selection(
    target: str, selected: str, pressures: tuple[PressureItem, ...], focus: str
) -> SelectionPathAudit:
    selected_item = pressures[0] if pressures else None
    unknowns = []
    factors = (
        ["pressure audit orders candidates by descending score, then category name"]
        if pressures
        else ["unknown"]
    )
    if not pressures:
        unknowns.append(
            {
                "area": "candidate_set",
                "reason": "no pressure candidates available from current audit inputs",
            }
        )
    return _selection_path_from_payloads(
        target=target,
        result=_SelectionResultPayload(
            selected=selected,
            outcome={
                "selected": selected,
                "focus": focus,
                "summary": f"{selected} selected",
            },
        ),
        lineage=_SelectionLineagePayload(
            candidates=[
                _candidate(item, index)
                for index, item in enumerate(pressures, start=1)
            ],
            selection_factors=factors,
            non_selected=[
                _non_selected(item, selected_item) for item in pressures[1:]
            ],
            evidence=[_evidence(selected_item)] if selected_item else [],
            unknowns=unknowns,
        ),
    )


def _candidate(item: PressureItem, rank: int) -> dict[str, Any]:
    return {
        "candidate": item.category.lower(),
        "score": item.score,
        "rank": rank,
        "reason": item.reason,
        "evidence": item.evidence,
    }


def _non_selected(
    item: PressureItem, selected_item: PressureItem | None
) -> dict[str, Any]:
    reason = "not selected because another candidate sorted earlier"
    if selected_item and item.score < selected_item.score:
        reason = "lower pressure score than selected candidate"
    elif selected_item and item.score == selected_item.score:
        reason = "same pressure score; category name sorted after selected candidate"
    return {"candidate": item.category.lower(), "score": item.score, "reason": reason}


def _evidence(item: PressureItem | None) -> dict[str, Any]:
    if item is None:
        return {}
    return {
        "surface": "pressure_audit",
        "category": item.category,
        "score": item.score,
        "reason": item.reason,
        "evidence": item.evidence,
    }


def _selected_name(item: PressureItem | None, focus: str) -> str:
    return item.category.lower() if item else focus


def _normalize_target(target: str) -> str:
    return target.strip().lower().replace("-", "_").replace(" ", "_")


def _matches_target(target: str, value: str) -> bool:
    return _normalize_target(value) == target or target in _normalize_target(value)


def _bullets(values: list[str], empty: str) -> list[str]:
    return [f"  - {value}" for value in values] if values else [f"  {empty}"]


def _items(values: list[dict[str, Any]], render) -> list[str]:
    return (
        ["  none observed"]
        if not values
        else [f"  - {render(value)}" for value in values]
    )
