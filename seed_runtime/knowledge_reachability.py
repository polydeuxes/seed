"""Implementation-backed knowledge reachability audit."""

from __future__ import annotations

from dataclasses import dataclass, asdict
import time
from pathlib import Path
import json
import re
from typing import Any, Callable, Iterable

from seed_runtime.events import EventLedger
from seed_runtime.inquiry_orientation import (
    InquiryNoteRecord,
    build_inquiry_orientation,
    format_inquiry_orientation,
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
DEFAULT_AUDIT_LIMIT = 500
DEFAULT_MAX_SECONDS = 60.0
PROGRESS_INTERVAL_SECONDS = 5.0


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


@dataclass(frozen=True)
class KnowledgeReachabilityMetadata:
    timing: dict[str, float]
    candidates: dict[str, int]
    truncated: bool = False
    reason: str | None = None
    limit: int | None = DEFAULT_AUDIT_LIMIT
    max_seconds: float | None = DEFAULT_MAX_SECONDS


@dataclass(frozen=True)
class KnowledgeReachabilityAuditResult:
    rows: list[KnowledgeReachabilityRow]
    metadata: KnowledgeReachabilityMetadata


@dataclass(frozen=True)
class _AuditIndexes:
    preserved_surfaces: list[str]
    projected_surfaces: list[str]
    read_model_surfaces: list[str]
    inquiry_surfaces: list[str]


def build_knowledge_reachability_audit(
    ledger: EventLedger,
    workspace_id: str,
    *,
    family: str | None = None,
    subject: str | None = None,
    repo_root: Path | None = None,
    limit: int | None = DEFAULT_AUDIT_LIMIT,
    all_candidates: bool = False,
    max_seconds: float | None = DEFAULT_MAX_SECONDS,
    progress: Callable[[str], None] | None = None,
    progress_interval_seconds: float = PROGRESS_INTERVAL_SECONDS,
) -> list[KnowledgeReachabilityRow]:
    return build_knowledge_reachability_audit_result(
        ledger,
        workspace_id,
        family=family,
        subject=subject,
        repo_root=repo_root,
        limit=limit,
        all_candidates=all_candidates,
        max_seconds=max_seconds,
        progress=progress,
        progress_interval_seconds=progress_interval_seconds,
    ).rows


def build_knowledge_reachability_audit_result(
    ledger: EventLedger,
    workspace_id: str,
    *,
    family: str | None = None,
    subject: str | None = None,
    repo_root: Path | None = None,
    limit: int | None = DEFAULT_AUDIT_LIMIT,
    all_candidates: bool = False,
    max_seconds: float | None = DEFAULT_MAX_SECONDS,
    progress: Callable[[str], None] | None = None,
    progress_interval_seconds: float = PROGRESS_INTERVAL_SECONDS,
) -> KnowledgeReachabilityAuditResult:
    timings: dict[str, float] = {}
    t0 = time.monotonic()
    state = StateProjector(ledger).project(workspace_id)
    events = ledger.list_events(workspace_id)
    timings["load state/cache"] = time.monotonic() - t0

    t0 = time.monotonic()
    candidates = _discover_candidates(events, state, repo_root or Path.cwd())
    if subject:
        candidates = {subject: _family_for_candidate(subject)}
    if family:
        candidates = {c: f for c, f in candidates.items() if f == family}
    discovered = len(candidates)
    sorted_candidates = sorted(candidates)
    skipped = 0
    truncated = False
    reason = None
    effective_limit = None if all_candidates or subject else limit
    if effective_limit is not None and len(sorted_candidates) > effective_limit:
        skipped = len(sorted_candidates) - effective_limit
        sorted_candidates = sorted_candidates[:effective_limit]
        truncated = True
        reason = "limit"
    timings["discover candidates"] = time.monotonic() - t0

    t0 = time.monotonic()
    indexes = _build_indexes(events, state)
    timings["build indexes"] = time.monotonic() - t0

    t0 = time.monotonic()
    deadline = time.monotonic() + max_seconds if max_seconds is not None else None
    next_progress = time.monotonic() + progress_interval_seconds
    rows: list[KnowledgeReachabilityRow] = []
    for idx, candidate in enumerate(sorted_candidates, start=1):
        now = time.monotonic()
        if deadline is not None and now >= deadline:
            skipped += len(sorted_candidates) - idx + 1
            truncated = True
            reason = "max_seconds"
            break
        if progress and now >= next_progress:
            progress(f"evaluated {idx - 1}/{len(sorted_candidates)} candidates...")
            next_progress = now + progress_interval_seconds
        flags = _candidate_flags_from_indexes(candidate, indexes)
        rows.append(
            KnowledgeReachabilityRow(
                candidates[candidate], candidate, *flags, _first_loss(flags)
            )
        )
    timings["evaluate candidates"] = time.monotonic() - t0
    timings["render"] = 0.0
    metadata = KnowledgeReachabilityMetadata(
        timing={k: round(v, 6) for k, v in timings.items()},
        candidates={
            "discovered": discovered,
            "evaluated": len(rows),
            "skipped": skipped,
        },
        truncated=truncated,
        reason=reason,
        limit=effective_limit,
        max_seconds=max_seconds,
    )
    return KnowledgeReachabilityAuditResult(rows, metadata)


def format_knowledge_reachability_table(
    rows: list[KnowledgeReachabilityRow],
    metadata: KnowledgeReachabilityMetadata | None = None,
) -> str:
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

    table = "\n".join(
        [fmt(headers), fmt(["-" * w for w in widths]), *[fmt(row) for row in body]]
    )
    if metadata is None:
        return table
    timing = "\n".join(
        f"  {name}: {seconds:.3f}s" for name, seconds in metadata.timing.items()
    )
    candidates = "\n".join(
        f"  {name}: {count}" for name, count in metadata.candidates.items()
    )
    guard = ""
    if metadata.truncated:
        guard = f"\nTruncated: true ({metadata.reason})"
    return f"Knowledge Reachability Audit\nTiming:\n{timing}\nCandidates:\n{candidates}{guard}\n\n{table}"


def knowledge_reachability_json(
    rows: list[KnowledgeReachabilityRow],
    metadata: KnowledgeReachabilityMetadata | None = None,
) -> list[dict[str, Any]] | dict[str, Any]:
    rendered = [asdict(row) for row in rows]
    if metadata is None:
        return rendered
    return {"metadata": asdict(metadata), "rows": rendered}


def _candidate_flags(
    candidate: str, events: list[Any], state: State
) -> tuple[bool, bool, bool, bool, bool]:
    return _candidate_flags_from_indexes(candidate, _build_indexes(events, state))


def _build_indexes(events: list[Any], state: State) -> _AuditIndexes:
    projected_surfaces = _projected_surfaces(state)
    read_surfaces = _read_model_surfaces(state)
    inquiry_surfaces = _inquiry_surfaces(state)
    return _AuditIndexes(
        preserved_surfaces=[
            item for event in events for item in (_json(event.payload), event.kind)
        ],
        projected_surfaces=projected_surfaces,
        read_model_surfaces=read_surfaces,
        inquiry_surfaces=inquiry_surfaces,
    )


def _candidate_flags_from_indexes(
    candidate: str, indexes: _AuditIndexes
) -> tuple[bool, bool, bool, bool, bool]:
    preserved = _contains(candidate, indexes.preserved_surfaces)
    projected = _contains(candidate, indexes.projected_surfaces)
    read_model = _contains(candidate, indexes.read_model_surfaces)
    inquiry = _contains(candidate, indexes.inquiry_surfaces)
    rendered = _contains(
        candidate, indexes.read_model_surfaces + indexes.inquiry_surfaces
    )
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


def _read_model_surfaces(state: State) -> list[str]:
    fact_lines = [
        f"{v.subject} {v.predicate} {_json(v.object)} {_json(v.dimensions)}"
        for v in build_fact_view(state)
    ]
    obs_lines = [v.summary for v in build_observation_view(state)]
    summary = _json(state_summary(state))
    return [*fact_lines, *obs_lines, summary]


def _inquiry_surfaces(state: State) -> list[str]:
    # Build inquiry orientation once so the audit is bounded and cache-aware.
    note = InquiryNoteRecord(
        note_id="audit",
        raw_note=" ".join(DEFAULT_SEEDS),
        recorded_at="1970-01-01T00:00:00Z",
    )
    orientation = format_inquiry_orientation(build_inquiry_orientation(state, note))
    return [] if "No deterministic related material" in orientation else [orientation]


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
