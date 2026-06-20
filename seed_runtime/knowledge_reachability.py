"""Implementation-backed knowledge reachability audit."""

from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
import json
import re
from typing import Any, Iterable

from seed_runtime.events import EventLedger
from seed_runtime.inquiry_orientation import (
    InquiryNoteRecord,
    build_inquiry_orientation,
    format_inquiry_orientation,
)
from seed_runtime.source_navigation import (
    build_source_navigation,
    format_source_navigation,
)
from seed_runtime.state import State, StateProjector
from seed_runtime.state_summary_views import state_summary
from seed_runtime.state_views import build_fact_view, build_observation_view

_TOKEN_RE = re.compile(r"[A-Za-z][A-Za-z0-9_./:-]{2,}")
DEFAULT_SEEDS = [
    "node115",
    "prometheus",
    "localhost:9090",
    "relationship",
    "ownership",
    "storage topology",
    "source navigation",
    "current work position",
    "active edge",
    "lens",
    "continuation",
    "inquiry orientation",
    "state build",
    "projection cache",
    "shared storage candidates",
]
FAMILIES = (
    "runtime",
    "relationships",
    "ownership",
    "projection",
    "repository",
    "inquiry",
)
STAGES = ("Preserved", "Projected", "Read Model", "Inquiry Orientation", "Rendered")


@dataclass(frozen=True)
class KnowledgeReachabilityRow:
    family: str
    candidate: str
    preserved: bool
    projected: bool
    read_model: bool
    inquiry_orientation: bool
    rendered: bool
    first_loss: str


def build_knowledge_reachability_audit(
    ledger: EventLedger,
    workspace_id: str,
    *,
    family: str | None = None,
    subject: str | None = None,
    repo_root: Path | None = None,
) -> list[KnowledgeReachabilityRow]:
    state = StateProjector(ledger).project(workspace_id)
    events = ledger.list_events(workspace_id)
    candidates = _discover_candidates(events, state, repo_root or Path.cwd())
    if subject:
        candidates = {subject: _family_for_candidate(subject)}
    rows = []
    for candidate in sorted(candidates):
        candidate_family = candidates[candidate]
        if family and candidate_family != family:
            continue
        flags = _candidate_flags(candidate, events, state)
        rows.append(
            KnowledgeReachabilityRow(
                candidate_family, candidate, *flags, _first_loss(flags)
            )
        )
    return rows


def format_knowledge_reachability_table(rows: list[KnowledgeReachabilityRow]) -> str:
    headers = ["Family", "Candidate", *STAGES, "First Loss"]
    body = [
        [
            r.family,
            r.candidate,
            *[_yes(getattr(r, _attr(h))) for h in STAGES],
            r.first_loss,
        ]
        for r in rows
    ]
    widths = [len(h) for h in headers]
    for row in body:
        widths = [max(width, len(cell)) for width, cell in zip(widths, row)]

    def fmt(row: list[str]) -> str:
        return " | ".join(cell.ljust(widths[i]) for i, cell in enumerate(row))

    return "\n".join(
        [fmt(headers), fmt(["-" * w for w in widths]), *[fmt(row) for row in body]]
    )


def knowledge_reachability_json(
    rows: list[KnowledgeReachabilityRow],
) -> list[dict[str, Any]]:
    return [asdict(row) for row in rows]


def _candidate_flags(
    candidate: str, events: list[Any], state: State
) -> tuple[bool, bool, bool, bool, bool]:
    preserved = _contains(
        candidate,
        [item for event in events for item in (_json(event.payload), event.kind)],
    )
    projected_surfaces = _projected_surfaces(state)
    projected = _contains(candidate, projected_surfaces)
    read_surfaces = _read_model_surfaces(state, candidate)
    read_model = _contains(candidate, read_surfaces)
    note = InquiryNoteRecord(
        note_id="audit", raw_note=candidate, recorded_at="1970-01-01T00:00:00Z"
    )
    orientation = format_inquiry_orientation(build_inquiry_orientation(state, note))
    inquiry = (
        _contains(candidate, [orientation])
        and "No deterministic related material" not in orientation
    )
    rendered = _contains(candidate, read_surfaces + ([orientation] if inquiry else []))
    return preserved, projected, read_model, inquiry, rendered


def _projected_surfaces(state: State) -> list[str]:
    surfaces: list[str] = []
    for fact in state.facts.values():
        surfaces.extend(
            [fact.subject_id, fact.predicate, _json(fact.value), _json(fact.dimensions)]
        )
    for support in state.fact_supports:
        surfaces.extend(
            [
                support.subject,
                support.predicate,
                _json(support.value),
                _json(support.dimensions),
            ]
        )
    for obs in state.observations.values():
        surfaces.extend([obs.subject, obs.predicate, _json(obs.value), obs.source_type])
    for entity in state.entities.values():
        surfaces.extend(
            [
                entity.id,
                entity.name,
                entity.kind,
                _json(entity.aliases),
                _json(entity.attributes),
            ]
        )
    for edge in [*state.relationships, *state.entity_relationships]:
        surfaces.append(_json(edge))
    return surfaces


def _read_model_surfaces(state: State, candidate: str) -> list[str]:
    fact_lines = [
        f"{v.subject} {v.predicate} {_json(v.object)} {_json(v.dimensions)}"
        for v in build_fact_view(state)
    ]
    obs_lines = [v.summary for v in build_observation_view(state)]
    nav_view = build_source_navigation(state, candidate)
    nav = (
        format_source_navigation(nav_view)
        if nav_view.definitions or nav_view.imports
        else ""
    )
    summary = _json(state_summary(state))
    return [*fact_lines, *obs_lines, nav, summary]


def _discover_candidates(
    events: list[Any], state: State, repo_root: Path
) -> dict[str, str]:
    found = {seed: _family_for_candidate(seed) for seed in DEFAULT_SEEDS}
    surfaces = [_json(event.payload) for event in events] + _projected_surfaces(state)
    for text in surfaces:
        for token in _TOKEN_RE.findall(text):
            if _useful_token(token):
                found.setdefault(token, _family_for_candidate(token))
    for path in (
        (repo_root / "docs").glob("**/*") if (repo_root / "docs").exists() else []
    ):
        if path.is_file():
            found.setdefault(str(path.relative_to(repo_root)), "repository")
            for token in _TOKEN_RE.findall(
                path.stem.replace("_", " ").replace("-", " ")
            ):
                if _useful_token(token):
                    found.setdefault(token.lower(), "repository")
    runtime_dir = repo_root / "seed_runtime"
    if runtime_dir.exists():
        for path in runtime_dir.glob("*.py"):
            found.setdefault(path.stem.replace("_", " "), "projection")
    return found


def _family_for_candidate(candidate: str) -> str:
    text = candidate.lower()
    if any(t in text for t in ("node", "localhost", "prometheus")):
        return "runtime"
    if "relationship" in text or "edge" in text:
        return "relationships"
    if "owner" in text or "ownership" in text:
        return "ownership"
    if any(t in text for t in ("projection", "state", "read model", "cache")):
        return "projection"
    if any(t in text for t in ("inquiry", "note", "orientation")):
        return "inquiry"
    return "repository"


def _first_loss(flags: tuple[bool, bool, bool, bool, bool]) -> str:
    seen = False
    for stage, present in zip(STAGES, flags):
        if seen and not present:
            return stage
        seen = seen or present
    return "none" if all(flags) else ("not present" if not any(flags) else "none")


def _contains(candidate: str, surfaces: Iterable[str]) -> bool:
    needle = candidate.lower()
    return any(needle in str(surface).lower() for surface in surfaces)


def _json(value: Any) -> str:
    try:
        return json.dumps(value, sort_keys=True, default=str)
    except TypeError:
        return str(value)


def _yes(value: bool) -> str:
    return "yes" if value else "no"


def _attr(header: str) -> str:
    return header.lower().replace(" ", "_")


def _useful_token(token: str) -> bool:
    return (
        len(token) >= 4
        and not token.isdigit()
        and token.lower() not in {"true", "false", "none", "null", "source", "value"}
    )
