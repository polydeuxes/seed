"""Read-only navigation over preserved repository source facts.

This module projects only existing ``imports`` and ``defines`` facts from a
projected :class:`seed_runtime.state.State`. It does not inspect files, parse
source, ingest observations, or infer behavior/reachability/ownership.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

from seed_runtime.facts import FactSupport
from seed_runtime.state import State

SOURCE_PREDICATES = frozenset({"defines", "imports"})
BOUNDED_ROW_LIMIT = 10


@dataclass(frozen=True)
class SourceNavigationRow:
    """One source-fact support row suitable for operator navigation."""

    subject: str
    predicate: Literal["defines", "imports"]
    value: str
    path: str | None
    support_count: int
    representative_fact_id: str | None
    representative_support_id: str


@dataclass(frozen=True)
class SourceNavigationView:
    """Bounded read-only source navigation projection for one query."""

    query: str
    definitions: list[SourceNavigationRow] = field(default_factory=list)
    imports: list[SourceNavigationRow] = field(default_factory=list)


def build_source_navigation(state: State, query: str) -> SourceNavigationView:
    """Return source navigation rows for ``query`` from preserved facts only.

    Matching is intentionally syntactic over the support projection:
    * short symbols match the final dotted segment of definition values;
    * qualified symbols match exact definition values;
    * modules match support subjects;
    * paths match the preserved ``path`` dimension.
    """

    normalized_query = query.strip()
    rows = [_row_from_support(support) for support in state.fact_supports]
    matched = [row for row in rows if _matches(row, normalized_query)]
    return SourceNavigationView(
        query=normalized_query,
        definitions=sorted(
            [row for row in matched if row.predicate == "defines"], key=_row_sort_key
        ),
        imports=sorted(
            [row for row in matched if row.predicate == "imports"], key=_row_sort_key
        ),
    )


def format_source_navigation(view: SourceNavigationView) -> str:
    """Render a deterministic operator-facing source navigation view."""

    lines = ["Source Navigation", "", f"query: {view.query}", ""]
    bounded = _is_path_or_module_lookup(view)
    if view.definitions:
        lines.append(_section_heading("Definitions", view.definitions, bounded=bounded))
        lines.extend(
            _format_rows(view.definitions, include_module=True, bounded=bounded)
        )
        lines.append("")
    if view.imports:
        lines.append(_section_heading("Imports", view.imports, bounded=bounded))
        lines.extend(_format_rows(view.imports, include_module=False, bounded=bounded))
        lines.append("")
    if bounded and (view.definitions or view.imports):
        lines.extend(_format_support_summary(view.definitions + view.imports))
    if not view.definitions and not view.imports:
        lines.append("No source facts matched.")
    return "\n".join(lines).rstrip()


def _row_from_support(support: FactSupport) -> SourceNavigationRow:
    predicate = support.predicate
    if predicate not in SOURCE_PREDICATES:
        # Kept defensive; callers filter via _matches before exposing rows.
        predicate = str(predicate)
    return SourceNavigationRow(
        subject=support.subject,
        predicate=predicate,  # type: ignore[arg-type]
        value=str(support.value),
        path=support.dimensions.get("path"),
        support_count=len(support.supporting_fact_ids),
        representative_fact_id=(
            sorted(support.supporting_fact_ids)[0]
            if support.supporting_fact_ids
            else None
        ),
        representative_support_id=_support_identity(support),
    )


def _matches(row: SourceNavigationRow, query: str) -> bool:
    if row.predicate not in SOURCE_PREDICATES:
        return False
    if query == row.subject or query == row.path:
        return True
    if row.predicate == "defines":
        return query == row.value or query == _final_segment(row.value)
    return False


def _final_segment(value: str) -> str:
    return value.rsplit(".", 1)[-1]


def _support_identity(support: FactSupport) -> str:
    path = support.dimensions.get("path", "")
    return f"{support.subject}|{support.predicate}|{support.value}|path={path}"


def _row_sort_key(row: SourceNavigationRow) -> tuple[Any, ...]:
    return (row.path or "", row.subject, row.value, row.representative_support_id)


def _is_path_or_module_lookup(view: SourceNavigationView) -> bool:
    rows = view.definitions + view.imports
    return any(view.query == row.subject or view.query == row.path for row in rows)


def _section_heading(
    label: str, rows: list[SourceNavigationRow], *, bounded: bool
) -> str:
    if not bounded:
        return f"{label}:"
    shown = min(len(rows), BOUNDED_ROW_LIMIT)
    return f"{label}: {len(rows)} total, showing {shown}"


def _format_support_summary(rows: list[SourceNavigationRow]) -> list[str]:
    support_facts = sum(row.support_count for row in rows)
    return [
        "Support:",
        f"  support facts: {support_facts}",
        "  representative fact/support: available in exact symbol lookup",
    ]


def _format_rows(
    rows: list[SourceNavigationRow], *, include_module: bool, bounded: bool
) -> list[str]:
    lines: list[str] = []
    visible_rows = rows[:BOUNDED_ROW_LIMIT] if bounded else rows
    for row in visible_rows:
        lines.append(f"  {row.value}")
        if bounded:
            continue
        if include_module:
            lines.append(f"    module: {row.subject}")
        lines.append(f"    path: {row.path or '(none)'}")
        lines.append(f"    support facts: {row.support_count}")
        if row.representative_fact_id:
            lines.append(f"    representative fact: {row.representative_fact_id}")
        lines.append(f"    representative support: {row.representative_support_id}")
    return lines
