"""Read-only structural observation for repository Markdown documentation."""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

BOUNDARY_TEXT = (
    "read only; observes document structure only; no prose interpretation; "
    "no claim extraction; no authority inference; no shape inference; "
    "no event ledger writes; no repository mutation"
)

BOUNDARY = {
    "read_only": True,
    "interprets_prose": False,
    "infers_claims": False,
    "infers_authority": False,
    "infers_shapes": False,
    "writes_event_ledger": False,
    "mutates_repository": False,
}

HUMAN_LIST_LIMIT = 20
_LINK_PATTERN = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")


@dataclass(frozen=True)
class DocumentationStructureOptions:
    document: str | None = None
    missing_front_matter: bool = False
    missing_trailing_newline: bool = False
    empty_sections: bool = False
    include_sections: bool = False
    include_links: bool = False
    include_code_fences: bool = False
    limit: int | None = None
    top: int | None = None
    summary_only: bool = False


@dataclass(frozen=True)
class DocumentationSection:
    level: int
    heading: str
    start_line: int
    end_line: int
    empty: bool

    def to_json_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class DocumentationLink:
    line: int
    target: str
    local_document: bool

    def to_json_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class DocumentationCodeFence:
    start_line: int
    end_line: int | None
    fence: str
    info: str
    closed: bool

    def to_json_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class DocumentationStructureRecord:
    path: str
    front_matter_present: bool
    front_matter_keys: tuple[str, ...]
    heading_present: bool
    title_heading: str | None
    structure_status: str
    line_count: int
    byte_count: int
    blank_line_count: int
    has_trailing_newline: bool
    section_count: int
    empty_section_count: int
    link_count: int
    code_fence_count: int
    sections: tuple[DocumentationSection, ...] = ()
    links: tuple[DocumentationLink, ...] = ()
    code_fences: tuple[DocumentationCodeFence, ...] = ()

    def to_json_dict(
        self,
        *,
        include_sections: bool = False,
        include_links: bool = False,
        include_code_fences: bool = False,
    ) -> dict[str, Any]:
        data = asdict(self)
        data["front_matter_keys"] = list(self.front_matter_keys)
        data.pop("sections")
        data.pop("links")
        data.pop("code_fences")
        if include_sections:
            data["sections"] = [section.to_json_dict() for section in self.sections]
        if include_links:
            data["links"] = [link.to_json_dict() for link in self.links]
        if include_code_fences:
            data["code_fences"] = [fence.to_json_dict() for fence in self.code_fences]
        return data


@dataclass(frozen=True)
class DocumentationStructureReport:
    documents: tuple[DocumentationStructureRecord, ...]
    summary: dict[str, int]
    boundary: dict[str, bool]
    options: DocumentationStructureOptions = DocumentationStructureOptions()

    def to_json_dict(self) -> dict[str, Any]:
        documents = (
            []
            if self.options.summary_only
            else [
                document.to_json_dict(
                    include_sections=self.options.include_sections,
                    include_links=self.options.include_links,
                    include_code_fences=self.options.include_code_fences,
                )
                for document in self.documents
            ]
        )
        return {
            "documents": documents,
            "summary": dict(self.summary),
            "boundary": dict(self.boundary),
        }


def observe_documentation_structure(
    repo_root: Path, options: DocumentationStructureOptions | None = None
) -> DocumentationStructureReport:
    """Observe structural metadata for allowlisted top-level docs/*.md files."""

    options = options or DocumentationStructureOptions()
    paths = _documentation_paths(repo_root, options.document)
    observed = tuple(observe_markdown_document(path, repo_root) for path in paths)
    selected = _select_documents(observed, options)
    summary = _summary(observed, selected)
    return DocumentationStructureReport(selected, summary, dict(BOUNDARY), options)


def observe_markdown_document(
    path: Path, repo_root: Path | None = None
) -> DocumentationStructureRecord:
    raw = path.read_bytes()
    text = raw.decode("utf-8")
    lines = text.splitlines()
    front_matter_present, keys = _front_matter(lines)
    headings = _headings(lines)
    title_heading = next((heading for level, heading, _line in headings if level == 1), None)
    sections = tuple(_sections(lines, headings))
    links = tuple(_links(lines))
    code_fences = tuple(_code_fences(lines))
    heading_present = title_heading is not None
    return DocumentationStructureRecord(
        path=_relative_path(path, repo_root),
        front_matter_present=front_matter_present,
        front_matter_keys=tuple(keys),
        heading_present=heading_present,
        title_heading=title_heading,
        structure_status=_structure_status(front_matter_present, heading_present),
        line_count=len(lines),
        byte_count=len(raw),
        blank_line_count=sum(not line.strip() for line in lines),
        has_trailing_newline=raw.endswith(b"\n"),
        section_count=len(sections),
        empty_section_count=sum(section.empty for section in sections),
        link_count=len(links),
        code_fence_count=len(code_fences),
        sections=sections,
        links=links,
        code_fences=code_fences,
    )


def documentation_structure_json(report: DocumentationStructureReport) -> dict[str, Any]:
    return report.to_json_dict()


def format_documentation_structure(report: DocumentationStructureReport) -> str:
    summary = report.summary
    lines = [
        "Documentation Structure",
        "",
        f"Total documents: {summary['total_documents']}",
        f"Selected documents: {summary['selected_documents']}",
        f"With YAML front matter: {summary['front_matter_present']}",
        f"Missing YAML front matter: {summary['front_matter_missing']}",
        f"With H1 heading: {summary['heading_present']}",
        f"Missing H1 heading: {summary['heading_missing']}",
        f"Missing trailing newline: {summary['missing_trailing_newline']}",
        f"Empty sections: {summary['empty_sections']}",
        f"Links: {summary['links']}",
        f"Code fences: {summary['code_fences']}",
        "",
        f"Boundary: {BOUNDARY_TEXT}",
    ]
    if report.options.summary_only:
        return "\n".join(lines)
    _append_document_lists(lines, report)
    return "\n".join(lines)


def _append_document_lists(lines: list[str], report: DocumentationStructureReport) -> None:
    documents = report.documents
    incomplete = [d for d in documents if d.structure_status != "complete"]
    if incomplete:
        lines.extend(["", "Incomplete documents:"])
        for document in incomplete[:HUMAN_LIST_LIMIT]:
            lines.append(f"- {document.path}: {document.structure_status}")
        if len(incomplete) > HUMAN_LIST_LIMIT:
            lines.append(f"... {len(incomplete) - HUMAN_LIST_LIMIT} more")
    if report.options.include_sections:
        lines.extend(["", "Section detail:"])
        for document in documents[:HUMAN_LIST_LIMIT]:
            lines.append(f"- {document.path}: {document.section_count} sections, {document.empty_section_count} empty")
    if report.options.include_links:
        lines.extend(["", "Link detail:"])
        for document in documents[:HUMAN_LIST_LIMIT]:
            lines.append(f"- {document.path}: {document.link_count} links")
    if report.options.include_code_fences:
        lines.extend(["", "Code fence detail:"])
        for document in documents[:HUMAN_LIST_LIMIT]:
            unclosed = sum(not fence.closed for fence in document.code_fences)
            lines.append(f"- {document.path}: {document.code_fence_count} code fences, {unclosed} unclosed")


def _documentation_paths(repo_root: Path, document: str | None) -> tuple[Path, ...]:
    docs_dir = repo_root / "docs"
    if document is None:
        return tuple(path for path in sorted(docs_dir.glob("*.md")) if path.is_file())
    path = _validated_document_path(repo_root, document)
    if not path.is_file():
        raise ValueError(f"documentation document not found: {document}")
    return (path,)


def _validated_document_path(repo_root: Path, document: str) -> Path:
    requested = Path(document)
    if requested.is_absolute() or ".." in requested.parts:
        raise ValueError("--document must be a repository-relative docs/*.md path")
    if (
        len(requested.parts) != 2
        or requested.parts[0] != "docs"
        or requested.suffix != ".md"
    ):
        raise ValueError("--document must be a repository-relative docs/*.md path")
    return repo_root / requested


def _select_documents(
    documents: tuple[DocumentationStructureRecord, ...], options: DocumentationStructureOptions
) -> tuple[DocumentationStructureRecord, ...]:
    selected = list(documents)
    if options.missing_front_matter:
        selected = [document for document in selected if not document.front_matter_present]
    if options.missing_trailing_newline:
        selected = [document for document in selected if not document.has_trailing_newline]
    if options.empty_sections:
        selected = [document for document in selected if document.empty_section_count > 0]
    if options.top is not None:
        selected = sorted(selected, key=_issue_score, reverse=True)[: options.top]
    if options.limit is not None:
        selected = selected[: options.limit]
    return tuple(selected)


def _summary(
    observed: tuple[DocumentationStructureRecord, ...], selected: tuple[DocumentationStructureRecord, ...]
) -> dict[str, int]:
    return {
        "total_documents": len(observed),
        "selected_documents": len(selected),
        "front_matter_present": sum(d.front_matter_present for d in selected),
        "front_matter_missing": sum(not d.front_matter_present for d in selected),
        "heading_present": sum(d.heading_present for d in selected),
        "heading_missing": sum(not d.heading_present for d in selected),
        "missing_trailing_newline": sum(not d.has_trailing_newline for d in selected),
        "empty_sections": sum(d.empty_section_count for d in selected),
        "links": sum(d.link_count for d in selected),
        "code_fences": sum(d.code_fence_count for d in selected),
    }


def _issue_score(document: DocumentationStructureRecord) -> int:
    return (
        int(not document.front_matter_present)
        + int(not document.heading_present)
        + int(not document.has_trailing_newline)
        + document.empty_section_count
        + sum(not fence.closed for fence in document.code_fences)
    )


def _front_matter(lines: list[str]) -> tuple[bool, list[str]]:
    if not lines or lines[0] != "---":
        return False, []
    try:
        closing_index = lines[1:].index("---") + 1
    except ValueError:
        return False, []
    keys: list[str] = []
    for line in lines[1:closing_index]:
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or ":" not in stripped:
            continue
        key = stripped.split(":", 1)[0].strip()
        if key:
            keys.append(key)
    return True, keys


def _headings(lines: list[str]) -> list[tuple[int, str, int]]:
    headings: list[tuple[int, str, int]] = []
    for index, line in enumerate(lines, start=1):
        stripped = line.lstrip()
        hashes = len(stripped) - len(stripped.lstrip("#"))
        if (
            1 <= hashes <= 6
            and stripped.startswith("#")
            and stripped[hashes : hashes + 1] == " "
        ):
            headings.append((hashes, stripped[hashes + 1 :].strip(), index))
    return headings


def _sections(lines: list[str], headings: list[tuple[int, str, int]]) -> list[DocumentationSection]:
    sections: list[DocumentationSection] = []
    for index, (level, heading, start_line) in enumerate(headings):
        end_line = len(lines)
        for next_level, _next_heading, next_line in headings[index + 1 :]:
            if next_level <= level:
                end_line = next_line - 1
                break
        body = lines[start_line:end_line]
        sections.append(
            DocumentationSection(
                level=level,
                heading=heading,
                start_line=start_line,
                end_line=end_line,
                empty=not any(line.strip() for line in body),
            )
        )
    return sections


def _links(lines: list[str]) -> list[DocumentationLink]:
    links: list[DocumentationLink] = []
    for line_number, line in enumerate(lines, start=1):
        for match in _LINK_PATTERN.finditer(line):
            target = match.group(1).strip()
            links.append(
                DocumentationLink(
                    line=line_number,
                    target=target,
                    local_document=target.startswith("docs/") or target.endswith(".md"),
                )
            )
    return links


def _code_fences(lines: list[str]) -> list[DocumentationCodeFence]:
    fences: list[DocumentationCodeFence] = []
    open_fence: tuple[str, str, int] | None = None
    for line_number, line in enumerate(lines, start=1):
        stripped = line.lstrip()
        if not (stripped.startswith("```") or stripped.startswith("~~~")):
            continue
        fence = stripped[:3]
        info = stripped[3:].strip()
        if open_fence is None:
            open_fence = (fence, info, line_number)
        elif stripped.startswith(open_fence[0]):
            start_fence, start_info, start_line = open_fence
            fences.append(
                DocumentationCodeFence(
                    start_line=start_line,
                    end_line=line_number,
                    fence=start_fence,
                    info=start_info,
                    closed=True,
                )
            )
            open_fence = None
    if open_fence is not None:
        start_fence, start_info, start_line = open_fence
        fences.append(
            DocumentationCodeFence(
                start_line=start_line,
                end_line=None,
                fence=start_fence,
                info=start_info,
                closed=False,
            )
        )
    return fences


def _structure_status(front_matter_present: bool, heading_present: bool) -> str:
    if front_matter_present and heading_present:
        return "complete"
    if not front_matter_present and not heading_present:
        return "missing_front_matter_and_heading"
    if not front_matter_present:
        return "missing_front_matter"
    return "missing_heading"


def _relative_path(path: Path, repo_root: Path | None) -> str:
    if repo_root is None:
        return path.as_posix()
    try:
        return path.relative_to(repo_root).as_posix()
    except ValueError:
        return path.as_posix()
