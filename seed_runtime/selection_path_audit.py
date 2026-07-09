"""Read-only selection trace visibility for operational conclusions."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from seed_runtime.operational_story import build_operational_story
from seed_runtime.pressure_audit import PressureItem, build_pressure_audit
from seed_runtime.state import State
from seed_runtime.typed_unknowns import (
    TypedUnknownRecord,
    preserve_typed_unknown,
    typed_unknowns_to_public_dicts,
)


@dataclass(frozen=True)
class _SelectionResultPayload:
    selected: str


@dataclass(frozen=True)
class _SelectionReasonPayload:
    outcome: dict[str, Any]


@dataclass(frozen=True)
class _SelectionSupportingEvidencePayload:
    evidence: list[dict[str, Any]]


@dataclass(frozen=True)
class _SelectionCandidateSetPayload:
    candidates: list[dict[str, Any]]


@dataclass(frozen=True)
class _SelectionNonSelectedPayload:
    non_selected: list[dict[str, Any]]


@dataclass(frozen=True)
class _SelectionFactorPayload:
    selection_factors: list[str]


@dataclass(frozen=True)
class _SelectionUnknownPayload:
    unknowns: list[TypedUnknownRecord]


@dataclass(frozen=True)
class _SelectionLineagePayload:
    candidate_set: _SelectionCandidateSetPayload
    factors: _SelectionFactorPayload
    non_selected: _SelectionNonSelectedPayload
    unknowns: _SelectionUnknownPayload


@dataclass(frozen=True)
class _SelectionPathInputs:
    pressures: tuple[PressureItem, ...]
    focus: str


@dataclass(frozen=True)
class _SelectionPathPayloads:
    result: _SelectionResultPayload
    reason: _SelectionReasonPayload
    support: _SelectionSupportingEvidencePayload
    lineage: _SelectionLineagePayload


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

    root = _selection_path_repo_root(repo_root)
    normalized = _normalize_target(target)
    inputs = _selection_path_inputs(state, root)

    if _target_matches_focus_selection(normalized, inputs.focus):
        return _from_focus_selection(target, normalized, inputs.pressures, inputs.focus)

    if _target_matches_pressure_category(normalized, inputs.pressures):
        return _from_pressure_category_selection(target, inputs.pressures, inputs.focus)

    return _unsupported_target_selection(target, inputs.pressures)


def _selection_path_repo_root(repo_root: str | Path | None) -> Path:
    return (
        Path(repo_root)
        if repo_root is not None
        else Path(__file__).resolve().parents[1]
    )


def _selection_path_inputs(state: State, root: Path) -> _SelectionPathInputs:
    pressure = build_pressure_audit(state, repo_root=root)
    story = build_operational_story(state, repo_root=root)
    return _SelectionPathInputs(pressures=pressure.pressures, focus=story.focus)


def _unsupported_target_selection(
    target: str, pressures: tuple[PressureItem, ...]
) -> SelectionPathAudit:
    return _selection_path_from_payloads(
        target=target,
        result=_unsupported_target_result_payload(),
        reason=_unsupported_target_reason_payload(),
        support=_unsupported_target_supporting_evidence_payload(),
        lineage=_unsupported_target_lineage_payload(pressures),
    )


def _unsupported_target_lineage_payload(
    pressures: tuple[PressureItem, ...],
) -> _SelectionLineagePayload:
    return _SelectionLineagePayload(
        candidate_set=_candidate_set_from_pressures(pressures),
        factors=_unsupported_target_factor_payload(),
        non_selected=_unsupported_target_non_selected_payload(),
        unknowns=_unsupported_target_unknown_payload(),
    )


def _unsupported_target_result_payload() -> _SelectionResultPayload:
    return _SelectionResultPayload(selected="unknown")


def _unsupported_target_reason_payload() -> _SelectionReasonPayload:
    return _SelectionReasonPayload(
        outcome={
            "selected": "unknown",
            "reason": "target is not an implemented selection surface",
        }
    )


def _unsupported_target_supporting_evidence_payload() -> (
    _SelectionSupportingEvidencePayload
):
    return _SelectionSupportingEvidencePayload(evidence=[])


def _unsupported_target_factor_payload() -> _SelectionFactorPayload:
    return _SelectionFactorPayload(selection_factors=["unknown"])


def _unsupported_target_non_selected_payload() -> _SelectionNonSelectedPayload:
    return _SelectionNonSelectedPayload(non_selected=[])


def _unsupported_target_unknown_payload() -> _SelectionUnknownPayload:
    return _SelectionUnknownPayload(
        unknowns=[
            preserve_typed_unknown(
                unknown_type="Implementation Unknown",
                area="selection_logic",
                reason="no implementation-backed selection evidence discovered for target",
            )
        ]
    )


def _selection_path_from_payloads(
    *,
    target: str,
    result: _SelectionResultPayload,
    reason: _SelectionReasonPayload,
    support: _SelectionSupportingEvidencePayload,
    lineage: _SelectionLineagePayload,
) -> SelectionPathAudit:
    return _selection_path_from_payload_bundle(
        target=target,
        payloads=_SelectionPathPayloads(
            result=result,
            reason=reason,
            support=support,
            lineage=lineage,
        ),
    )


def _selection_path_from_payload_bundle(
    *, target: str, payloads: _SelectionPathPayloads
) -> SelectionPathAudit:
    return SelectionPathAudit(
        target=target,
        selected=payloads.result.selected,
        candidates=payloads.lineage.candidate_set.candidates,
        selection_factors=payloads.lineage.factors.selection_factors,
        non_selected=payloads.lineage.non_selected.non_selected,
        evidence=payloads.support.evidence,
        outcome=payloads.reason.outcome,
        unknowns=typed_unknowns_to_public_dicts(payloads.lineage.unknowns.unknowns),
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
    return _selection_path_from_payload_bundle(
        target=target,
        payloads=_pressure_selection_payloads(selected, pressures, focus),
    )


def _from_pressure_category_selection(
    target: str, pressures: tuple[PressureItem, ...], focus: str
) -> SelectionPathAudit:
    selected_item = _selected_pressure_item(pressures)
    return _from_pressure_selection(
        target,
        _pressure_category_selection_selected_name(selected_item, focus),
        pressures,
        focus,
    )


def _from_focus_selection(
    target: str, normalized_target: str, pressures: tuple[PressureItem, ...], focus: str
) -> SelectionPathAudit:
    selected_item = _selected_pressure_item(pressures)
    return _from_pressure_selection(
        target,
        _focus_selection_selected_name(normalized_target, selected_item, focus),
        pressures,
        focus,
    )


def _pressure_selection_payloads(
    selected: str, pressures: tuple[PressureItem, ...], focus: str
) -> _SelectionPathPayloads:
    selected_item = _selected_pressure_item(pressures)
    unknowns = _selection_unknowns_from_pressures(pressures)
    return _SelectionPathPayloads(
        result=_pressure_selection_result_payload(selected),
        reason=_pressure_selection_reason_payload(selected, focus),
        support=_pressure_selection_supporting_evidence_payload(selected_item),
        lineage=_pressure_selection_lineage_payload(pressures, selected_item, unknowns),
    )


def _pressure_selection_result_payload(selected: str) -> _SelectionResultPayload:
    return _SelectionResultPayload(selected=selected)


def _pressure_selection_reason_payload(
    selected: str, focus: str
) -> _SelectionReasonPayload:
    return _SelectionReasonPayload(
        outcome={
            "selected": selected,
            "focus": focus,
            "summary": f"{selected} selected",
        }
    )


def _pressure_selection_lineage_payload(
    pressures: tuple[PressureItem, ...],
    selected_item: PressureItem | None,
    unknowns: _SelectionUnknownPayload,
) -> _SelectionLineagePayload:
    return _SelectionLineagePayload(
        candidate_set=_candidate_set_from_pressures(pressures),
        factors=_selection_factors_from_pressures(pressures),
        non_selected=_non_selected_from_pressures(pressures, selected_item),
        unknowns=unknowns,
    )


def _pressure_selection_supporting_evidence_payload(
    selected_item: PressureItem | None,
) -> _SelectionSupportingEvidencePayload:
    return _SelectionSupportingEvidencePayload(
        evidence=[_evidence(selected_item)] if selected_item else []
    )


def _selected_pressure_item(pressures: tuple[PressureItem, ...]) -> PressureItem | None:
    return pressures[0] if pressures else None


def _target_matches_focus_selection(normalized_target: str, focus: str) -> bool:
    return normalized_target in {
        "current_focus",
        "primary_pressure",
    } or _matches_target(normalized_target, focus)


def _target_matches_pressure_category(
    normalized_target: str, pressures: tuple[PressureItem, ...]
) -> bool:
    return any(_matches_target(normalized_target, item.category) for item in pressures)


def _selection_unknowns_from_pressures(
    pressures: tuple[PressureItem, ...],
) -> _SelectionUnknownPayload:
    unknowns: list[TypedUnknownRecord] = []
    if not pressures:
        unknowns.append(
            preserve_typed_unknown(
                unknown_type="Evidence Gap",
                area="candidate_set",
                reason="no pressure candidates available from current audit inputs",
            )
        )
    return _SelectionUnknownPayload(unknowns=unknowns)


def _selection_factors_from_pressures(
    pressures: tuple[PressureItem, ...],
) -> _SelectionFactorPayload:
    return _SelectionFactorPayload(
        selection_factors=(
            ["pressure audit orders candidates by descending score, then category name"]
            if pressures
            else ["unknown"]
        )
    )


def _candidate_set_from_pressures(
    pressures: tuple[PressureItem, ...],
) -> _SelectionCandidateSetPayload:
    return _SelectionCandidateSetPayload(
        candidates=[
            _candidate(item, index) for index, item in enumerate(pressures, start=1)
        ]
    )


def _candidate(item: PressureItem, rank: int) -> dict[str, Any]:
    return {
        "candidate": item.category.lower(),
        "score": item.score,
        "rank": rank,
        "reason": item.reason,
        "evidence": item.evidence,
    }


def _non_selected_from_pressures(
    pressures: tuple[PressureItem, ...],
    selected_item: PressureItem | None,
) -> _SelectionNonSelectedPayload:
    return _SelectionNonSelectedPayload(
        non_selected=[
            _non_selected(item, selected_item)
            for item in _non_selected_pressure_candidates(pressures)
        ]
    )


def _non_selected_pressure_candidates(
    pressures: tuple[PressureItem, ...],
) -> tuple[PressureItem, ...]:
    return pressures[1:]


def _non_selected(
    item: PressureItem, selected_item: PressureItem | None
) -> dict[str, Any]:
    return {
        "candidate": item.category.lower(),
        "score": item.score,
        "reason": _non_selected_reason(item, selected_item),
    }


def _non_selected_reason(item: PressureItem, selected_item: PressureItem | None) -> str:
    if selected_item and item.score < selected_item.score:
        return "lower pressure score than selected candidate"
    if selected_item and item.score == selected_item.score:
        return "same pressure score; category name sorted after selected candidate"
    return "not selected because another candidate sorted earlier"


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


def _focus_selection_selected_name(
    normalized_target: str, selected_item: PressureItem | None, focus: str
) -> str:
    return (
        focus
        if normalized_target == "current_focus"
        else _selected_name(selected_item, focus)
    )


def _pressure_category_selection_selected_name(
    selected_item: PressureItem | None, focus: str
) -> str:
    return _selected_name(selected_item, focus)


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
