"""Implementation-backed knowledge reachability audit."""

from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass, asdict
import time
from pathlib import Path
import json
import re
from typing import Any, Callable, Iterable, Iterator

from seed_runtime.events import EventLedger
from seed_runtime.inquiry_orientation import (
    InquiryNoteRecord,
    build_inquiry_orientation,
    format_inquiry_orientation,
)
from seed_runtime.state import State, StateProjector

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
DEFAULT_SOURCE_BUDGETS = {
    "default seeds": None,
    "event payloads": 200,
    "projected state": 200,
    "docs/": 50,
    "seed_runtime/": 50,
    "source-navigation terms": 100,
}


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
    timings: dict[str, float]
    candidate_counts: dict[str, int]
    algorithmic_counters: dict[str, int] | None = None
    candidate_sources: dict[str, int] | None = None
    scan_counts: dict[str, int] | None = None
    cache: dict[str, str] | None = None
    indexes: dict[str, float] | None = None
    truncated: bool = False
    reason: str | None = None
    limit: int | None = DEFAULT_AUDIT_LIMIT
    max_seconds: float | None = DEFAULT_MAX_SECONDS

    @property
    def timing(self) -> dict[str, float]:
        return self.timings

    @property
    def candidates(self) -> dict[str, int]:
        return self.candidate_counts


@dataclass(frozen=True)
class KnowledgeReachabilityAuditResult:
    rows: list[KnowledgeReachabilityRow]
    metadata: KnowledgeReachabilityMetadata


@dataclass
class _ReachabilityTimer:
    progress: Callable[[str], None] | None = None
    timings: dict[str, float] | None = None

    def __post_init__(self) -> None:
        if self.timings is None:
            self.timings = {}
        self._total_start = time.monotonic()

    @contextmanager
    def phase(self, name: str, **start_fields: Any) -> Iterator[Callable[..., None]]:
        self.emit("start", name, **start_fields)
        start = time.monotonic()
        end_fields: dict[str, Any] = {}

        def add_fields(**fields: Any) -> None:
            end_fields.update(fields)

        try:
            yield add_fields
        finally:
            elapsed = time.monotonic() - start
            assert self.timings is not None
            self.timings[name] = elapsed
            self.emit("end", name, elapsed=elapsed, **end_fields)

    def progress_message(
        self, name: str, current: int, total: int, **fields: Any
    ) -> None:
        elapsed = time.monotonic() - self._total_start
        self.emit(
            "progress", name, prefix=f"{current}/{total}", elapsed=elapsed, **fields
        )

    def total(self) -> float:
        return time.monotonic() - self._total_start

    def emit(
        self,
        event: str,
        phase: str,
        *,
        elapsed: float | None = None,
        prefix: str | None = None,
        **fields: Any,
    ) -> None:
        if self.progress is None:
            return
        pieces = [f"[reachability] {event} {phase}"]
        if prefix:
            pieces.append(prefix)
        if elapsed is not None:
            pieces.append(
                f"{elapsed:.2f}s" if event == "end" else f"elapsed={elapsed:.2f}s"
            )
        pieces.extend(
            f"{key}={value}" for key, value in fields.items() if value is not None
        )
        self.progress(" ".join(pieces))


@dataclass(frozen=True)
class _CandidateDiscovery:
    candidates: dict[str, str]
    source_counts: dict[str, int]
    scan_counts: dict[str, int]
    raw_seen: int
    used: int
    truncated: bool


@dataclass(frozen=True)
class _AuditIndexes:
    preserved_terms: set[str]
    projected_terms: set[str]
    read_model_terms: set[str]
    inquiry_terms: set[str]


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
    timer = _ReachabilityTimer(progress)
    cache = {"state": "miss", "summary": "miss", "projection": "miss"}
    scan_counts: dict[str, int] = {}
    source_counts: dict[str, int] = {}
    index_timings: dict[str, float] = {}
    counters = _new_counters()

    with timer.phase("load_state", state_cache=cache["state"], evaluated=0):
        state = StateProjector(ledger).project(workspace_id)
        events = ledger.list_events(workspace_id)

    with timer.phase("discover_candidates") as finish_discovery:
        effective_limit = None if all_candidates or subject else limit
        discovery = _discover_candidates(
            events,
            state,
            repo_root or Path.cwd(),
            counters,
            limit=effective_limit,
            all_candidates=all_candidates,
            subject=subject,
        )
        candidates = discovery.candidates
        source_counts = discovery.source_counts
        scan_counts = discovery.scan_counts
        if subject:
            candidates = {subject: _family_for_candidate(subject)}
        if family:
            candidates = {c: f for c, f in candidates.items() if f == family}
        discovered = len(candidates)
        sorted_candidates = sorted(candidates)
        skipped = 0
        truncated = discovery.truncated
        reason = None
        if truncated:
            reason = "limit"
            skipped = max(0, discovery.raw_seen - len(sorted_candidates))
        if effective_limit is not None and len(sorted_candidates) > effective_limit:
            skipped = len(sorted_candidates) - effective_limit
            sorted_candidates = sorted_candidates[:effective_limit]
            truncated = True
            reason = "limit"
        finish_discovery(
            raw_seen=discovery.raw_seen,
            used=len(sorted_candidates),
            limit=effective_limit,
            truncated=truncated,
        )

    with timer.phase("build_indexes"):
        indexes = _build_indexes(
            events, state, timer=timer, index_timings=index_timings, counters=counters
        )

    with timer.phase("evaluate") as finish_evaluate:
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
                timer.progress_message("evaluate", idx - 1, len(sorted_candidates))
                next_progress = now + progress_interval_seconds
            flags = _candidate_flags_from_indexes(candidate, indexes, counters)
            rows.append(
                KnowledgeReachabilityRow(
                    candidates[candidate], candidate, *flags, _first_loss(flags)
                )
            )
        finish_evaluate(
            evaluated=len(rows), membership_checks=counters["membership_checks"]
        )

    with timer.phase("render"):
        pass
    assert timer.timings is not None
    timer.timings["total"] = timer.total()
    counters["candidate_count"] = len(rows)
    counters["raw_candidates_discovered"] = discovery.raw_seen
    counters["candidates_evaluated"] = len(rows)
    for key in sorted(counters):
        timer.emit("counter", key, value=counters[key])
    metadata = KnowledgeReachabilityMetadata(
        timings={k: round(v, 6) for k, v in timer.timings.items()},
        candidate_counts={
            "raw_seen": discovery.raw_seen,
            "used": len(sorted_candidates),
            "limit": effective_limit if effective_limit is not None else 0,
            "discovered": discovered,
            "raw_candidates_discovered": discovery.raw_seen,
            "capped": len(sorted_candidates),
            "candidates_evaluated": len(rows),
            "evaluated": len(rows),
            "skipped": skipped,
        },
        algorithmic_counters=dict(counters),
        candidate_sources=source_counts,
        scan_counts=scan_counts,
        cache=cache,
        indexes={k: round(v, 6) for k, v in index_timings.items()},
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
        f"  {name}: {seconds:.3f}s" for name, seconds in metadata.timings.items()
    )
    candidates = "\n".join(
        f"  {name}: {count}" for name, count in metadata.candidate_counts.items()
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
    metadata_payload = asdict(metadata)
    metadata_payload["timing"] = {
        **metadata.timings,
        "load state/cache": metadata.timings.get("load_state", 0.0),
    }
    metadata_payload["candidates"] = metadata.candidate_counts
    return {"metadata": metadata_payload, "rows": rendered}


def _candidate_flags(
    candidate: str, events: list[Any], state: State
) -> tuple[bool, bool, bool, bool, bool]:
    counters = _new_counters()
    return _candidate_flags_from_indexes(
        candidate, _build_indexes(events, state, counters=counters), counters
    )


def _build_indexes(
    events: list[Any],
    state: State,
    *,
    timer: _ReachabilityTimer | None = None,
    index_timings: dict[str, float] | None = None,
    counters: dict[str, int] | None = None,
) -> _AuditIndexes:
    local_timer = timer or _ReachabilityTimer(None)
    timings = index_timings if index_timings is not None else {}
    counters = counters if counters is not None else _new_counters()
    counters["state_projection_build_calls"] += 1
    with local_timer.phase("projected_entities"):
        counters["entity_projection_build_calls"] += 1
        projected_entities = _projected_entity_surfaces(state, counters)
    timings["projected_entities"] = (
        local_timer.timings.get("projected_entities", 0.0)
        if local_timer.timings
        else 0.0
    )
    with local_timer.phase("projected_facts"):
        projected_facts = _projected_fact_surfaces(state, counters)
    timings["projected_facts"] = (
        local_timer.timings.get("projected_facts", 0.0) if local_timer.timings else 0.0
    )
    with local_timer.phase("fact_support"):
        counters["fact_support_index_build_calls"] += 1
        fact_support = _fact_support_surfaces(state, counters)
    timings["fact_support"] = (
        local_timer.timings.get("fact_support", 0.0) if local_timer.timings else 0.0
    )
    with local_timer.phase(
        "source_navigation.index_from_fact_support"
    ) as finish_source_index:
        source_nav_terms = _source_navigation_terms_from_fact_support(state, counters)
        finish_source_index(
            supports_scanned=counters["fact_supports_scanned"],
            terms=len(source_nav_terms),
        )
    timings["source_navigation.index_from_fact_support"] = (
        local_timer.timings.get("source_navigation.index_from_fact_support", 0.0)
        if local_timer.timings
        else 0.0
    )
    with local_timer.phase("read_model"):
        read_surfaces = _read_model_surfaces(state, counters, local_timer)
    timings["read_model"] = (
        local_timer.timings.get("read_model", 0.0) if local_timer.timings else 0.0
    )
    with local_timer.phase("inquiry_orientation"):
        counters["orientation_build_calls"] += 1
        inquiry_surfaces = _inquiry_surfaces(state)
    timings["inquiry_orientation"] = (
        local_timer.timings.get("inquiry_orientation", 0.0)
        if local_timer.timings
        else 0.0
    )
    return _AuditIndexes(
        preserved_terms=_surface_terms(
            (item for event in events for item in (_json(event.payload), event.kind)),
            counters,
        ),
        projected_terms=_surface_terms(
            [*projected_entities, *projected_facts, *fact_support], counters
        ),
        read_model_terms=_surface_terms([*read_surfaces, *source_nav_terms], counters),
        inquiry_terms=_surface_terms(inquiry_surfaces, counters),
    )


def _candidate_flags_from_indexes(
    candidate: str, indexes: _AuditIndexes, counters: dict[str, int]
) -> tuple[bool, bool, bool, bool, bool]:
    preserved = _contains(candidate, indexes.preserved_terms, counters)
    projected = _contains(candidate, indexes.projected_terms, counters)
    read_model = _contains(candidate, indexes.read_model_terms, counters)
    inquiry = _contains(candidate, indexes.inquiry_terms, counters)
    rendered = read_model or inquiry
    counters["membership_checks"] += 1
    return preserved, projected, read_model, inquiry, rendered


def _projected_surfaces(
    state: State, counters: dict[str, int] | None = None
) -> list[str]:
    return [
        *_projected_fact_surfaces(state, counters),
        *_fact_support_surfaces(state, counters),
        *_projected_entity_surfaces(state, counters),
    ]


def _projected_fact_surfaces(
    state: State, counters: dict[str, int] | None = None
) -> list[str]:
    surfaces: list[str] = []
    if counters is not None:
        counters["facts_scanned"] += len(state.facts)
    for fact in state.facts.values():
        surfaces.extend(
            [fact.subject_id, fact.predicate, _json(fact.value), _json(fact.dimensions)]
        )
    return surfaces


def _fact_support_surfaces(
    state: State, counters: dict[str, int] | None = None
) -> list[str]:
    surfaces: list[str] = []
    if counters is not None:
        counters["fact_supports_scanned"] += len(state.fact_supports)
    for support in state.fact_supports:
        surfaces.extend(
            [
                support.subject,
                support.predicate,
                _json(support.value),
                _json(support.dimensions),
            ]
        )
    return surfaces


def _projected_entity_surfaces(
    state: State, counters: dict[str, int] | None = None
) -> list[str]:
    surfaces: list[str] = []
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


def _read_model_surfaces(
    state: State,
    counters: dict[str, int] | None = None,
    timer: _ReachabilityTimer | None = None,
) -> list[str]:
    if counters is not None:
        counters["read_model_build_calls"] += 1
    local_timer = timer or _ReachabilityTimer(None)
    surfaces: list[str] = []
    with local_timer.phase("read_model.current_facts") as finish:
        for fact in state.facts.values():
            surfaces.append(
                f"{fact.subject_id} {fact.predicate} {_json(fact.value)} "
                f"{_json(fact.dimensions)}"
            )
        finish(rows=len(state.facts))
    with local_timer.phase("read_model.fact_support") as finish:
        for support in state.fact_supports:
            surfaces.append(
                f"{support.subject} {support.predicate} {_json(support.value)} "
                f"{_json(support.dimensions)}"
            )
        finish(rows=len(state.fact_supports))
    with local_timer.phase("read_model.state_summary") as finish:
        surfaces.append(
            " ".join(
                [
                    f"entities {len(state.entities)}",
                    f"facts {len(state.facts)}",
                    f"observations {len(state.observations)}",
                    f"relationships {len(state.relationships)}",
                ]
            )
        )
        finish(rows=1)
    with local_timer.phase("read_model.inquiry_orientation") as finish:
        notes = getattr(state, "inquiry_notes", {})
        note_ids = [getattr(note, "note_id", str(note)) for note in notes.values()]
        surfaces.extend(note_ids)
        finish(rows=len(note_ids))
    return surfaces


def _inquiry_surfaces(state: State) -> list[str]:
    # Build inquiry orientation once so the audit is bounded and cache-aware.
    note = InquiryNoteRecord(
        note_id="audit",
        raw_note=" ".join(DEFAULT_SEEDS),
        recorded_at="1970-01-01T00:00:00Z",
    )
    orientation = format_inquiry_orientation(build_inquiry_orientation(state, note))
    return [] if "No deterministic related material" in orientation else [orientation]


def _new_counters() -> dict[str, int]:
    return {
        "candidate_count": 0,
        "raw_candidates_discovered": 0,
        "candidates_evaluated": 0,
        "facts_scanned": 0,
        "fact_supports_scanned": 0,
        "source_navigation_build_calls": 0,
        "source_navigation_query_calls": 0,
        "source_navigation_rows_scanned": 0,
        "orientation_build_calls": 0,
        "orientation_query_calls": 0,
        "docs_scanned": 0,
        "symbols_scanned": 0,
        "tokenizations": 0,
        "normalizations": 0,
        "membership_checks": 0,
        "state_projection_build_calls": 0,
        "entity_projection_build_calls": 0,
        "fact_support_index_build_calls": 0,
        "read_model_build_calls": 0,
    }


def _source_navigation_terms_from_fact_support(
    state: State, counters: dict[str, int]
) -> list[str]:
    counters["source_navigation_rows_scanned"] += len(state.fact_supports)
    terms: list[str] = []
    for support in state.fact_supports:
        if support.predicate not in {"defines", "imports"}:
            continue
        terms.extend(
            [
                support.subject,
                support.predicate,
                str(support.value),
                str(support.dimensions.get("path", "")),
                str(support.value).rsplit(".", 1)[-1],
            ]
        )
    return terms


def _surface_terms(
    surfaces: Iterable[str], counters: dict[str, int] | None = None
) -> set[str]:
    terms: set[str] = set()
    for surface in surfaces:
        text = str(surface).lower()
        if text:
            terms.add(text)
        if counters is not None:
            counters["tokenizations"] += 1
        tokens = [token.lower() for token in _TOKEN_RE.findall(text)]
        terms.update(tokens)
        for width in (2, 3, 4):
            terms.update(
                " ".join(tokens[index : index + width])
                for index in range(0, max(0, len(tokens) - width + 1))
            )
    return terms


def _discover_candidates(
    events: list[Any],
    state: State,
    repo_root: Path,
    counters: dict[str, int] | None = None,
    *,
    limit: int | None = DEFAULT_AUDIT_LIMIT,
    all_candidates: bool = False,
    subject: str | None = None,
) -> _CandidateDiscovery:
    found: dict[str, str] = {}
    source_counts = {
        "default seeds": 0,
        "event payloads": 0,
        "projected state": 0,
        "docs/": 0,
        "seed_runtime/": 0,
        "source-navigation terms": 0,
    }
    scan_counts = {
        "event payloads scanned": 0,
        "facts scanned": 0,
        "repo files scanned": 0,
        "symbols scanned": 0,
        "source-navigation terms scanned": 0,
    }
    raw_seen = 0
    truncated = False
    source_budgets = (
        {key: None for key in DEFAULT_SOURCE_BUDGETS} if all_candidates else DEFAULT_SOURCE_BUDGETS
    )

    if subject:
        found[subject] = _family_for_candidate(subject)
        return _CandidateDiscovery(found, source_counts, scan_counts, 1, 1, False)

    def globally_full() -> bool:
        return limit is not None and len(found) >= limit

    def source_full(source: str) -> bool:
        budget = source_budgets.get(source)
        return budget is not None and source_counts[source] >= budget

    def add(candidate: str, family: str, source: str) -> None:
        nonlocal raw_seen
        raw_seen += 1
        if globally_full() and candidate not in found:
            return
        if source_full(source) and candidate not in found:
            return
        before = len(found)
        found.setdefault(candidate, family)
        if len(found) > before:
            source_counts[source] += 1

    for seed in DEFAULT_SEEDS:
        add(seed, _family_for_candidate(seed), "default seeds")

    for event in events:
        if globally_full():
            truncated = True
            break
        if source_full("event payloads"):
            break
        scan_counts["event payloads scanned"] += 1
        if counters is not None:
            counters["tokenizations"] += 1
        for token in _TOKEN_RE.findall(_json(event.payload)):
            if _useful_token(token):
                add(token, _family_for_candidate(token), "event payloads")

    if not globally_full():
        projected_surfaces = _projected_surfaces(state)
        if counters is not None:
            counters["facts_scanned"] += len(state.facts)
            counters["fact_supports_scanned"] += len(state.fact_supports)
        scan_counts["facts scanned"] = len(state.facts) + len(state.fact_supports)
        for text in projected_surfaces:
            if globally_full() or source_full("projected state"):
                if globally_full():
                    truncated = True
                break
            if counters is not None:
                counters["tokenizations"] += 1
            for token in _TOKEN_RE.findall(text):
                if _useful_token(token):
                    add(token, _family_for_candidate(token), "projected state")

    if not globally_full():
        for term in _source_navigation_terms_from_fact_support(
            state, _new_counters()
        ):
            scan_counts["source-navigation terms scanned"] += 1
            if globally_full() or source_full("source-navigation terms"):
                if globally_full():
                    truncated = True
                break
            if _useful_token(term):
                add(term, "repository", "source-navigation terms")

    if not globally_full():
        for path in (
            (repo_root / "docs").glob("**/*") if (repo_root / "docs").exists() else []
        ):
            if globally_full() or source_full("docs/"):
                if globally_full():
                    truncated = True
                break
            if path.is_file():
                scan_counts["repo files scanned"] += 1
                if counters is not None:
                    counters["docs_scanned"] += 1
                add(str(path.relative_to(repo_root)), "repository", "docs/")
                if counters is not None:
                    counters["tokenizations"] += 1
                for token in _TOKEN_RE.findall(
                    path.stem.replace("_", " ").replace("-", " ")
                ):
                    scan_counts["symbols scanned"] += 1
                    if _useful_token(token):
                        add(token.lower(), "repository", "docs/")
    runtime_dir = repo_root / "seed_runtime"
    if not globally_full() and runtime_dir.exists():
        for path in runtime_dir.glob("*.py"):
            if globally_full() or source_full("seed_runtime/"):
                if globally_full():
                    truncated = True
                break
            scan_counts["repo files scanned"] += 1
            scan_counts["symbols scanned"] += 1
            if counters is not None:
                counters["symbols_scanned"] += 1
            add(path.stem.replace("_", " "), "projection", "seed_runtime/")
    return _CandidateDiscovery(
        found, source_counts, scan_counts, raw_seen, len(found), truncated
    )


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


def _contains(candidate: str, terms: set[str], counters: dict[str, int]) -> bool:
    counters["normalizations"] += 1
    counters["membership_checks"] += 1
    return candidate.lower() in terms


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
