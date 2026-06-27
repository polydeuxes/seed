"""Read-only navigation over preserved repository source facts.

This module projects only existing ``imports`` and ``defines`` facts from a
projected :class:`seed_runtime.state.State`. It does not inspect files, parse
source, ingest observations, or infer behavior/reachability/ownership.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Literal

from seed_runtime.facts import FactSupport
from seed_runtime.state import State

SOURCE_PREDICATES = frozenset({"defines", "imports"})
BOUNDED_ROW_LIMIT = 10
DEFINITION_NON_CLAIMS = (
    "definition evidence only; no call, behavior, capability ownership, or runtime reachability claims",
    "uses projected source facts only; does not inspect repository files or parse source during lookup",
)
DEPENDENCY_NON_CLAIMS = (
    "import dependency evidence only; no runtime behavior, runtime reachability, ownership authority, call graph usage, import execution, or module load success claims",
    "uses projected source import facts only; does not inspect repository files, parse source during lookup, or validate dependency correctness",
)
SUPPORT_NON_CLAIMS = (
    "support evidence summary only; no truth, runtime behavior, runtime reachability, ownership authority, call graph usage, import execution, module load success, dependency correctness, or semantic relevance claims",
    "uses existing projected source fact/support evidence only; does not inspect repository files, parse source during lookup, or infer beyond source navigation matches",
)


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
class RepositoryArtifactDefinitionExplanation:
    """Definition visibility for one repository artifact query."""

    query: str
    status: Literal["defined", "unknown"]
    definition_kind: str
    definition_value: str | None
    source_path: str | None
    representative_fact_id: str | None
    representative_support_id: str | None
    boundary: tuple[str, ...]

    def to_json_dict(self) -> dict[str, object]:
        data = asdict(self)
        data["boundary"] = list(self.boundary)
        return data


@dataclass(frozen=True)
class RepositoryArtifactDependencyMention:
    """One preserved import/dependency mention for a repository artifact query."""

    query: str
    status: Literal["mentioned"]
    dependency_value: str
    source_path: str | None
    representative_fact_id: str | None
    representative_support_id: str | None
    support_count: int
    boundary: tuple[str, ...]

    def to_json_dict(self) -> dict[str, object]:
        data = asdict(self)
        data["boundary"] = list(self.boundary)
        return data


@dataclass(frozen=True)
class RepositoryArtifactDependencyExplanation:
    """Dependency visibility for one repository artifact query."""

    query: str
    status: Literal["mentioned", "unknown"]
    dependencies: list[RepositoryArtifactDependencyMention]
    boundary: tuple[str, ...]

    def to_json_dict(self) -> dict[str, object]:
        return {
            "query": self.query,
            "status": self.status,
            "dependencies": [item.to_json_dict() for item in self.dependencies],
            "boundary": list(self.boundary),
        }


@dataclass(frozen=True)
class RepositoryArtifactSupportExplanation:
    """Support-evidence visibility for one repository artifact query."""

    query: str
    status: Literal["supported", "unsupported"]
    definition_support_count: int
    dependency_support_count: int
    total_support_count: int
    representative_definition_fact_id: str | None
    representative_definition_support_id: str | None
    representative_dependency_fact_id: str | None
    representative_dependency_support_id: str | None
    source_paths: tuple[str, ...]
    boundary: tuple[str, ...]

    def to_json_dict(self) -> dict[str, object]:
        data = asdict(self)
        data["source_paths"] = list(self.source_paths)
        data["boundary"] = list(self.boundary)
        return data


@dataclass(frozen=True)
class SourceNavigationView:
    """Bounded read-only source navigation projection for one query."""

    query: str
    definitions: list[SourceNavigationRow] = field(default_factory=list)
    imports: list[SourceNavigationRow] = field(default_factory=list)
    repository_artifact_definition: RepositoryArtifactDefinitionExplanation | None = (
        None
    )
    repository_artifact_dependencies: RepositoryArtifactDependencyExplanation | None = (
        None
    )
    repository_artifact_support: RepositoryArtifactSupportExplanation | None = None


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
    definitions = sorted(
        [row for row in matched if row.predicate == "defines"], key=_row_sort_key
    )
    imports = sorted(
        [row for row in matched if row.predicate == "imports"], key=_row_sort_key
    )
    bounded = any(
        normalized_query == row.subject or normalized_query == row.path
        for row in definitions + imports
    )
    dependency_mentions = sorted(
        [row for row in rows if _dependency_mentions(row, normalized_query)],
        key=_row_sort_key,
    )
    return SourceNavigationView(
        query=normalized_query,
        definitions=definitions,
        imports=imports,
        repository_artifact_definition=_definition_explanation(
            normalized_query,
            definitions,
            bounded=bounded,
        ),
        repository_artifact_dependencies=_dependency_explanation(
            normalized_query,
            dependency_mentions,
            bounded=bounded,
        ),
        repository_artifact_support=_support_explanation(
            normalized_query,
            definitions,
            dependency_mentions,
        ),
    )


def format_source_navigation(view: SourceNavigationView) -> str:
    """Render a deterministic operator-facing source navigation view."""

    lines = ["Source Navigation", "", f"query: {view.query}", ""]
    bounded = _is_path_or_module_lookup(view)
    if view.repository_artifact_definition is not None:
        lines.extend(
            _format_definition_explanation(view.repository_artifact_definition)
        )
        lines.append("")
    if view.repository_artifact_dependencies is not None:
        lines.extend(
            _format_dependency_explanation(view.repository_artifact_dependencies)
        )
        lines.append("")
    if view.repository_artifact_support is not None:
        lines.extend(_format_support_explanation(view.repository_artifact_support))
        lines.append("")
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


def _dependency_mentions(row: SourceNavigationRow, query: str) -> bool:
    if row.predicate != "imports":
        return False
    return query == row.value or query == _final_segment(row.value)


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


def source_navigation_json(view: SourceNavigationView) -> dict[str, object]:
    """Return stable JSON for source navigation visibility."""

    return {
        "query": view.query,
        "repository_artifact_definition": (
            view.repository_artifact_definition.to_json_dict()
            if view.repository_artifact_definition is not None
            else None
        ),
        "repository_artifact_dependencies": (
            view.repository_artifact_dependencies.to_json_dict()
            if view.repository_artifact_dependencies is not None
            else None
        ),
        "repository_artifact_support": (
            view.repository_artifact_support.to_json_dict()
            if view.repository_artifact_support is not None
            else None
        ),
        "definitions": [_row_json(row) for row in view.definitions],
        "imports": [_row_json(row) for row in view.imports],
    }


def _row_json(row: SourceNavigationRow) -> dict[str, object]:
    return {
        "subject": row.subject,
        "predicate": row.predicate,
        "value": row.value,
        "path": row.path,
        "support_count": row.support_count,
        "representative_fact_id": row.representative_fact_id,
        "representative_support_id": row.representative_support_id,
    }


def _definition_explanation(
    query: str, definitions: list[SourceNavigationRow], *, bounded: bool
) -> RepositoryArtifactDefinitionExplanation:
    if not definitions:
        return RepositoryArtifactDefinitionExplanation(
            query=query,
            status="unknown",
            definition_kind="unknown",
            definition_value=None,
            source_path=None,
            representative_fact_id=None,
            representative_support_id=None,
            boundary=DEFINITION_NON_CLAIMS,
        )
    row = definitions[0]
    return RepositoryArtifactDefinitionExplanation(
        query=query,
        status="defined",
        definition_kind="unknown",
        definition_value=row.value,
        source_path=row.path,
        representative_fact_id=None if bounded else row.representative_fact_id,
        representative_support_id=None if bounded else row.representative_support_id,
        boundary=DEFINITION_NON_CLAIMS,
    )


def _dependency_explanation(
    query: str, mentions: list[SourceNavigationRow], *, bounded: bool
) -> RepositoryArtifactDependencyExplanation:
    dependencies = [
        RepositoryArtifactDependencyMention(
            query=query,
            status="mentioned",
            dependency_value=row.value,
            source_path=row.path,
            representative_fact_id=None if bounded else row.representative_fact_id,
            representative_support_id=(
                None if bounded else row.representative_support_id
            ),
            support_count=row.support_count,
            boundary=DEPENDENCY_NON_CLAIMS,
        )
        for row in mentions
    ]
    return RepositoryArtifactDependencyExplanation(
        query=query,
        status="mentioned" if dependencies else "unknown",
        dependencies=dependencies,
        boundary=DEPENDENCY_NON_CLAIMS,
    )


def _support_explanation(
    query: str,
    definitions: list[SourceNavigationRow],
    dependency_mentions: list[SourceNavigationRow],
) -> RepositoryArtifactSupportExplanation:
    definition_support_count = sum(row.support_count for row in definitions)
    dependency_support_count = sum(row.support_count for row in dependency_mentions)
    definition_row = definitions[0] if definitions else None
    dependency_row = dependency_mentions[0] if dependency_mentions else None
    source_paths = tuple(
        sorted(
            {
                row.path
                for row in [*definitions, *dependency_mentions]
                if row.path is not None
            }
        )
    )
    total_support_count = definition_support_count + dependency_support_count
    return RepositoryArtifactSupportExplanation(
        query=query,
        status="supported" if total_support_count else "unsupported",
        definition_support_count=definition_support_count,
        dependency_support_count=dependency_support_count,
        total_support_count=total_support_count,
        representative_definition_fact_id=(
            definition_row.representative_fact_id
            if definition_row is not None
            else None
        ),
        representative_definition_support_id=(
            definition_row.representative_support_id
            if definition_row is not None
            else None
        ),
        representative_dependency_fact_id=(
            dependency_row.representative_fact_id
            if dependency_row is not None
            else None
        ),
        representative_dependency_support_id=(
            dependency_row.representative_support_id
            if dependency_row is not None
            else None
        ),
        source_paths=source_paths,
        boundary=SUPPORT_NON_CLAIMS,
    )


def _format_dependency_explanation(
    explanation: RepositoryArtifactDependencyExplanation,
) -> list[str]:
    lines = [
        "Repository Artifact Dependencies:",
        f"  query: {explanation.query}",
        f"  status: {explanation.status}",
    ]
    if explanation.dependencies:
        lines.append("  preserved import mentions:")
        for item in explanation.dependencies:
            lines.extend(
                [
                    f"    - dependency value: {item.dependency_value}",
                    "      source path: "
                    + (item.source_path if item.source_path is not None else "unknown"),
                    f"      support facts: {item.support_count}",
                    "      representative source fact: "
                    + (
                        item.representative_fact_id
                        if item.representative_fact_id is not None
                        else "unknown"
                    ),
                    "      representative source support: "
                    + (
                        item.representative_support_id
                        if item.representative_support_id is not None
                        else "unknown"
                    ),
                ]
            )
    else:
        lines.append("  preserved import mentions: none")
    lines.append("  boundary:")
    lines.extend(f"    - {item}" for item in explanation.boundary)
    return lines


def _format_definition_explanation(
    explanation: RepositoryArtifactDefinitionExplanation,
) -> list[str]:
    lines = [
        "Repository Artifact Definition:",
        f"  query: {explanation.query}",
        f"  status: {explanation.status}",
        f"  definition kind: {explanation.definition_kind}",
        "  definition value: "
        + (
            explanation.definition_value
            if explanation.definition_value is not None
            else "unknown"
        ),
        "  source path: "
        + (
            explanation.source_path
            if explanation.source_path is not None
            else "unknown"
        ),
        "  representative source fact: "
        + (
            explanation.representative_fact_id
            if explanation.representative_fact_id is not None
            else "unknown"
        ),
        "  representative source support: "
        + (
            explanation.representative_support_id
            if explanation.representative_support_id is not None
            else "unknown"
        ),
        "  boundary:",
    ]
    lines.extend(f"    - {item}" for item in explanation.boundary)
    return lines


def _format_support_explanation(
    explanation: RepositoryArtifactSupportExplanation,
) -> list[str]:
    lines = [
        "Repository Artifact Support:",
        f"  query: {explanation.query}",
        f"  status: {explanation.status}",
        f"  definition support facts: {explanation.definition_support_count}",
        f"  dependency support facts: {explanation.dependency_support_count}",
        f"  total support facts: {explanation.total_support_count}",
        "  representative definition source fact: "
        + (
            explanation.representative_definition_fact_id
            if explanation.representative_definition_fact_id is not None
            else "unknown"
        ),
        "  representative definition source support: "
        + (
            explanation.representative_definition_support_id
            if explanation.representative_definition_support_id is not None
            else "unknown"
        ),
        "  representative dependency source fact: "
        + (
            explanation.representative_dependency_fact_id
            if explanation.representative_dependency_fact_id is not None
            else "unknown"
        ),
        "  representative dependency source support: "
        + (
            explanation.representative_dependency_support_id
            if explanation.representative_dependency_support_id is not None
            else "unknown"
        ),
        "  source paths represented:",
    ]
    if explanation.source_paths:
        lines.extend(f"    - {path}" for path in explanation.source_paths)
    else:
        lines.append("    - none")
    lines.append("  boundary:")
    lines.extend(f"    - {item}" for item in explanation.boundary)
    return lines
