"""Minimized read-only inquiry-note orientation probe.

Inquiry notes are stored outside the event ledger so operator prose remains
preserved evidence for this probe only. Rendering reads projected state but never
mutates it, appends events, calls providers, executes tools, or creates facts,
goals, tool needs, decisions, proposals, or plans.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
import json
from pathlib import Path
import re
from typing import Any, Iterable

from seed_runtime.ids import new_id
from seed_runtime.source_navigation import build_source_navigation
from seed_runtime.state import State

NOTE_SOURCE = "scripts.seed_local --record-inquiry-note"
AUTHORITY_BOUNDARY = (
    "This orientation is read-only. The inquiry note is preserved operator prose, "
    "not a fact, claim, goal, tool need, requirement, capability, decision, "
    "proposal, plan, authorization, command, or runtime instruction. Matches are "
    "deterministic lexical overlaps only and do not assert importance, "
    "do not assert ownership, "
    "intent, concern, recommended action, or next safe move."
)
UNCERTAINTY_WITH_MATCHES = (
    "Related material may be incomplete or incidental; lexical overlap is not "
    "semantic interpretation and does not establish operator intent."
)
UNCERTAINTY_WITHOUT_MATCHES = (
    "No deterministic related material was found in already projected read models; "
    "this absence does not prove the note is unrelated to existing work."
)
_TOKEN_RE = re.compile(r"[A-Za-z0-9_./:-]+")
_MIN_TOKEN_LENGTH = 3
_MAX_RELATED_ITEMS = 10


@dataclass(frozen=True)
class InquiryNoteRecord:
    note_id: str
    raw_note: str
    recorded_at: str
    source: str = NOTE_SOURCE
    workspace_id: str | None = None
    session_id: str | None = None


@dataclass(frozen=True)
class RelatedMaterial:
    material_type: str
    label: str
    surface: str
    support: str
    why_related: str
    surface_family: str


@dataclass(frozen=True)
class InquiryOrientationView:
    note: InquiryNoteRecord
    related_material: list[RelatedMaterial] = field(default_factory=list)
    uncertainty: str = UNCERTAINTY_WITHOUT_MATCHES
    authority_boundary: str = AUTHORITY_BOUNDARY


@dataclass(frozen=True)
class _InquiryOrientationCompositionRequest:
    """Implementation-local handoff from preserved inquiry note to orientation composition."""

    note: InquiryNoteRecord
    note_tokens: set[str]


@dataclass(frozen=True)
class _InquiryOrientationEvidence:
    """Implementation-local evidence collected for inquiry orientation composition."""

    related_material: list[RelatedMaterial]


@dataclass(frozen=True)
class _InquiryOrientationSelectedMaterial:
    """Implementation-local selected material with preserved supports for answer composition."""

    related_material: list[RelatedMaterial]
    support: list[str]


@dataclass(frozen=True)
class _InquiryOrientationAnswer:
    """Implementation-local answer composition before inquiry orientation rendering."""

    answer: list[RelatedMaterial]
    reason: str
    support: list[str]
    boundary: str
    limitations: str


def record_inquiry_note(
    store_path: Path,
    raw_note: str,
    *,
    workspace_id: str | None = None,
    session_id: str | None = None,
    recorded_at: datetime | None = None,
) -> InquiryNoteRecord:
    """Append one raw inquiry note to the isolated JSONL probe store."""

    if raw_note == "" or raw_note.strip() == "":
        raise ValueError("inquiry note must be non-empty")
    timestamp = (recorded_at or datetime.now(timezone.utc)).astimezone(timezone.utc)
    record = InquiryNoteRecord(
        note_id=new_id("inq"),
        raw_note=raw_note,
        recorded_at=timestamp.isoformat().replace("+00:00", "Z"),
        workspace_id=workspace_id,
        session_id=session_id,
    )
    store_path.parent.mkdir(parents=True, exist_ok=True)
    with store_path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(_record_to_json(record), sort_keys=True) + "\n")
    return record


def load_inquiry_notes(store_path: Path) -> list[InquiryNoteRecord]:
    """Load preserved inquiry notes from the isolated JSONL probe store."""

    if not store_path.exists():
        return []
    records: list[InquiryNoteRecord] = []
    with store_path.open("r", encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                records.append(InquiryNoteRecord(**json.loads(line)))
    return records


def select_inquiry_note(
    store_path: Path, note_id: str | None = None
) -> InquiryNoteRecord | None:
    """Return the requested note, or the latest note when no id is supplied."""

    records = load_inquiry_notes(store_path)
    if note_id is None:
        return records[-1] if records else None
    for record in records:
        if record.note_id == note_id:
            return record
    return None


def build_inquiry_orientation(
    state: State, note: InquiryNoteRecord
) -> InquiryOrientationView:
    """Build a bounded read-only orientation view for a preserved inquiry note."""

    request = _prepare_inquiry_orientation_composition(note)
    answer = _compose_inquiry_orientation_answer(state, request)
    return InquiryOrientationView(
        note=note,
        related_material=answer.answer,
        uncertainty=answer.limitations,
        authority_boundary=answer.boundary,
    )


def _prepare_inquiry_orientation_composition(
    note: InquiryNoteRecord,
) -> _InquiryOrientationCompositionRequest:
    """Prepare preserved inquiry material for bounded orientation composition."""

    return _InquiryOrientationCompositionRequest(
        note=note,
        note_tokens=_note_tokens(note.raw_note),
    )


def _compose_inquiry_orientation_answer(
    state: State, request: _InquiryOrientationCompositionRequest
) -> _InquiryOrientationAnswer:
    """Compose inquiry orientation answer material without rendering or transport changes."""

    evidence = _collect_inquiry_orientation_evidence(state, request)
    selected_material = _prepare_inquiry_orientation_selected_material(evidence)
    return _prepare_inquiry_orientation_answer(selected_material)


def _prepare_inquiry_orientation_answer(
    selected_material: _InquiryOrientationSelectedMaterial,
) -> _InquiryOrientationAnswer:
    """Prepare the implementation-local answer artifact from selected material."""

    return _InquiryOrientationAnswer(
        answer=selected_material.related_material,
        reason=_select_inquiry_orientation_reason(selected_material),
        support=selected_material.support,
        boundary=_select_inquiry_orientation_authority_boundary(selected_material),
        limitations=_select_inquiry_orientation_limitations(selected_material),
    )


def _select_inquiry_orientation_reason(
    selected_material: _InquiryOrientationSelectedMaterial,
) -> str:
    """Select reason text for the selected inquiry-orientation material."""

    return (
        "deterministic lexical overlaps against projected fact supports and "
        "source-navigation matches"
    )


def _select_inquiry_orientation_authority_boundary(
    selected_material: _InquiryOrientationSelectedMaterial,
) -> str:
    """Select authority-boundary text for the selected inquiry-orientation material."""

    return AUTHORITY_BOUNDARY


def _select_inquiry_orientation_limitations(
    selected_material: _InquiryOrientationSelectedMaterial,
) -> str:
    """Select uncertainty text from whether related material was selected."""

    return (
        UNCERTAINTY_WITH_MATCHES
        if selected_material.related_material
        else UNCERTAINTY_WITHOUT_MATCHES
    )


def _prepare_inquiry_orientation_selected_material(
    evidence: _InquiryOrientationEvidence,
) -> _InquiryOrientationSelectedMaterial:
    """Prepare selected related material and preserve its support strings."""

    related = evidence.related_material
    return _InquiryOrientationSelectedMaterial(
        related_material=related,
        support=[item.support for item in related],
    )


def _collect_inquiry_orientation_evidence(
    state: State, request: _InquiryOrientationCompositionRequest
) -> _InquiryOrientationEvidence:
    """Collect repository evidence before composing the inquiry orientation answer."""

    related = _dedupe_related(
        [
            *_fact_matches(state, request.note_tokens),
            *_source_navigation_matches(state, request.note_tokens),
        ]
    )[:_MAX_RELATED_ITEMS]
    return _InquiryOrientationEvidence(related_material=related)


def format_inquiry_orientation(view: InquiryOrientationView) -> str:
    """Render the required V1 text sections."""

    lines = [
        "Inquiry note:",
        f"  {view.note.raw_note}",
        "",
        "Potentially related material:",
    ]
    if view.related_material:
        for item in view.related_material:
            lines.append(f"  - [{item.material_type}] {item.label}: {item.surface}")
            lines.append("")
            lines.append("    surface family:")
            lines.append(f"      {item.surface_family}")
    else:
        lines.append(
            "  No deterministic related material found in projected read models."
        )
    lines.extend(["", "Support / why related:"])
    if view.related_material:
        for item in view.related_material:
            lines.append(f"  - {item.why_related}; support: {item.support}")
    else:
        lines.append("  No supportable lexical overlap was found.")
    lines.extend(
        [
            "",
            "Uncertainty:",
            f"  {view.uncertainty}",
            "",
            "Authority boundary:",
            f"  {view.authority_boundary}",
        ]
    )
    return "\n".join(lines)


def _record_to_json(record: InquiryNoteRecord) -> dict[str, Any]:
    return {
        "note_id": record.note_id,
        "raw_note": record.raw_note,
        "recorded_at": record.recorded_at,
        "source": record.source,
        "workspace_id": record.workspace_id,
        "session_id": record.session_id,
    }


def _note_tokens(raw_note: str) -> set[str]:
    return {
        token.lower()
        for token in _TOKEN_RE.findall(raw_note)
        if len(token) >= _MIN_TOKEN_LENGTH
    }


def _overlap(tokens: set[str], surfaces: Iterable[str]) -> set[str]:
    material_tokens: set[str] = set()
    for surface in surfaces:
        material_tokens.update(_note_tokens(surface))
    return tokens & material_tokens


def _fact_matches(state: State, tokens: set[str]) -> list[RelatedMaterial]:
    matches: list[RelatedMaterial] = []
    for support in state.fact_supports:
        value = str(support.value)
        overlaps = _overlap(
            tokens,
            [
                support.subject,
                support.predicate,
                value,
                support.dimensions.get("path", ""),
            ],
        )
        if not overlaps:
            continue
        surface = f"{support.subject} {support.predicate} {value}"
        matches.append(
            RelatedMaterial(
                material_type="projected fact support",
                label=support.subject,
                surface=surface,
                support=(
                    f"fact support subject={support.subject!r} predicate={support.predicate!r} "
                    f"path={support.dimensions.get('path')!r}"
                ),
                why_related=f"case-normalized token overlap: {', '.join(sorted(overlaps))}",
                surface_family="fact support",
            )
        )
    return matches


def _source_navigation_matches(state: State, tokens: set[str]) -> list[RelatedMaterial]:
    matches: list[RelatedMaterial] = []
    for token in sorted(tokens):
        view = build_source_navigation(state, token)
        for row in [*view.definitions, *view.imports]:
            matches.append(
                RelatedMaterial(
                    material_type=f"source navigation {row.predicate}",
                    label=row.value,
                    surface=f"{row.value} ({row.path or 'no path'})",
                    support=f"source-navigation support={row.representative_support_id}",
                    why_related=f"source-navigation lexical match for token: {token}",
                    surface_family="source navigation",
                )
            )
    return matches


def _dedupe_related(items: Iterable[RelatedMaterial]) -> list[RelatedMaterial]:
    seen: set[tuple[str, str, str]] = set()
    deduped: list[RelatedMaterial] = []
    for item in sorted(
        items, key=lambda i: (i.material_type, i.label, i.surface, i.support)
    ):
        key = (item.material_type, item.label, item.support)
        if key in seen:
            continue
        seen.add(key)
        deduped.append(item)
    return deduped
