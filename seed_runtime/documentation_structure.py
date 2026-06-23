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


@dataclass(frozen=True)
class DocumentationStructureFilters:
    missing_front_matter: bool = False
    missing_trailing_newline: bool = False
    empty_sections: bool = False
    include_links: bool = False
    include_code_fences: bool = False
    include_sections: bool = False


@dataclass(frozen=True)
class DocumentationHeadingRecord:
    level: int
    text: str
    line_number: int


@dataclass(frozen=True)
class DocumentationSectionRecord:
    heading_text: str
    heading_level: int
    start_line: int
    end_line: int
    child_section_count: int
    parent_heading_path: tuple[str, ...]


@dataclass(frozen=True)
class DocumentationLinkRecord:
    source_path: str
    raw_target: str
    is_relative: bool
    points_under_docs: bool


@dataclass(frozen=True)
class DocumentationCodeBlockRecord:
    fence_type: str
    info_string: str | None
    language: str | None
    start_line: int
    end_line: int | None
    closed: bool


@dataclass(frozen=True)
class DocumentationStructureRecord:
    path: str
    line_count: int
    byte_count: int
    blank_line_count: int
    nonblank_line_count: int
    empty_document: bool
    has_trailing_newline: bool
    front_matter_present: bool
    front_matter_keys: tuple[str, ...]
    heading_present: bool
    title_heading: str | None
    heading_outline: tuple[DocumentationHeadingRecord, ...]
    has_section_headings: bool
    max_heading_depth: int
    skipped_heading_level_present: bool
    duplicate_heading_texts: tuple[str, ...]
    sections: tuple[DocumentationSectionRecord, ...]
    section_count: int
    max_section_depth: int
    empty_section_count: int
    link_observations: tuple[DocumentationLinkRecord, ...]
    code_block_observations: tuple[DocumentationCodeBlockRecord, ...]
    structure_status: str

    def to_json_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["front_matter_keys"] = list(self.front_matter_keys)
        data["heading_outline"] = [asdict(heading) for heading in self.heading_outline]
        data["duplicate_heading_texts"] = list(self.duplicate_heading_texts)
        data["sections"] = [
            {**asdict(section), "parent_heading_path": list(section.parent_heading_path)}
            for section in self.sections
        ]
        data["link_observations"] = [asdict(link) for link in self.link_observations]
        data["code_block_observations"] = [
            asdict(code_block) for code_block in self.code_block_observations
        ]
        return data


@dataclass(frozen=True)
class DocumentationStructureReport:
    documents: tuple[DocumentationStructureRecord, ...]
    summary: dict[str, Any]
    boundary: dict[str, bool]

    def to_json_dict(self) -> dict[str, Any]:
        return {
            "documents": [document.to_json_dict() for document in self.documents],
            "summary": dict(self.summary),
            "boundary": dict(self.boundary),
        }


def observe_documentation_structure(
    repo_root: Path, filters: DocumentationStructureFilters | None = None
) -> DocumentationStructureReport:
    """Observe structural metadata for allowlisted top-level docs/*.md files."""

    docs_dir = repo_root / "docs"
    documents = tuple(
        observe_markdown_document(path, repo_root)
        for path in sorted(docs_dir.glob("*.md"))
        if path.is_file()
    )
    documents = _filter_documents(documents, filters)
    return DocumentationStructureReport(
        documents, _summary(documents, repo_root), dict(BOUNDARY)
    )


def _filter_documents(
    documents: tuple[DocumentationStructureRecord, ...],
    filters: DocumentationStructureFilters | None,
) -> tuple[DocumentationStructureRecord, ...]:
    if filters is None:
        return documents
    filtered = documents
    if filters.missing_front_matter:
        filtered = tuple(d for d in filtered if not d.front_matter_present)
    if filters.missing_trailing_newline:
        filtered = tuple(d for d in filtered if not d.has_trailing_newline)
    if filters.empty_sections:
        filtered = tuple(d for d in filtered if d.empty_section_count > 0)
    return filtered


def _summary(
    documents: tuple[DocumentationStructureRecord, ...], repo_root: Path
) -> dict[str, Any]:
    return {
        "total_documents": len(documents),
        "total_lines": sum(d.line_count for d in documents),
        "total_bytes": sum(d.byte_count for d in documents),
        "blank_line_count": sum(d.blank_line_count for d in documents),
        "nonblank_line_count": sum(d.nonblank_line_count for d in documents),
        "empty_document_count": sum(d.empty_document for d in documents),
        "documents_without_trailing_newline": sum(
            not d.has_trailing_newline for d in documents
        ),
        "front_matter_present": sum(d.front_matter_present for d in documents),
        "front_matter_missing": sum(not d.front_matter_present for d in documents),
        "heading_present": sum(d.heading_present for d in documents),
        "heading_missing": sum(not d.heading_present for d in documents),
        "internal_doc_link_count": sum(
            link.points_under_docs for d in documents for link in d.link_observations
        ),
        "external_link_count": sum(
            not link.is_relative for d in documents for link in d.link_observations
        ),
        "broken_local_doc_link_count": sum(
            _local_doc_link_is_broken(link, repo_root)
            for d in documents
            for link in d.link_observations
        ),
        "code_block_count": sum(len(d.code_block_observations) for d in documents),
        "unclosed_code_block_count": sum(
            not code_block.closed
            for d in documents
            for code_block in d.code_block_observations
        ),
        "code_block_languages": sorted(
            {
                code_block.language
                for d in documents
                for code_block in d.code_block_observations
                if code_block.language is not None
            }
        ),
        "section_count": sum(d.section_count for d in documents),
        "max_section_depth": max((d.max_section_depth for d in documents), default=0),
        "empty_section_count": sum(d.empty_section_count for d in documents),
    }

def observe_markdown_document(
    path: Path, repo_root: Path | None = None
) -> DocumentationStructureRecord:
    raw_bytes = path.read_bytes()
    text = raw_bytes.decode("utf-8")
    lines = text.splitlines()
    metrics = _document_metrics(raw_bytes, lines)
    front_matter_present, keys = _front_matter(lines)
    code_block_observations = tuple(_code_block_observations(lines))
    code_content_lines = _code_content_line_numbers(code_block_observations, len(lines))
    heading_outline = tuple(_heading_outline(lines, code_content_lines))
    sections = tuple(_section_inventory(heading_outline, lines, code_content_lines))
    source_path = _relative_path(path, repo_root)
    link_observations = tuple(
        _link_observations(lines, path, source_path, repo_root, code_content_lines)
    )
    title_heading = _first_h1(heading_outline)
    heading_present = title_heading is not None
    return DocumentationStructureRecord(
        path=source_path,
        line_count=metrics["line_count"],
        byte_count=metrics["byte_count"],
        blank_line_count=metrics["blank_line_count"],
        nonblank_line_count=metrics["nonblank_line_count"],
        empty_document=metrics["empty_document"],
        has_trailing_newline=metrics["has_trailing_newline"],
        front_matter_present=front_matter_present,
        front_matter_keys=tuple(keys),
        heading_present=heading_present,
        title_heading=title_heading,
        heading_outline=heading_outline,
        has_section_headings=any(heading.level > 1 for heading in heading_outline),
        max_heading_depth=max((heading.level for heading in heading_outline), default=0),
        skipped_heading_level_present=_skipped_heading_level_present(heading_outline),
        duplicate_heading_texts=tuple(_duplicate_heading_texts(heading_outline)),
        sections=sections,
        section_count=len(sections),
        max_section_depth=max(
            (len(section.parent_heading_path) + 1 for section in sections), default=0
        ),
        empty_section_count=sum(
            _section_is_empty(section, lines, code_content_lines)
            for section in sections
        ),
        link_observations=link_observations,
        code_block_observations=code_block_observations,
        structure_status=_structure_status(front_matter_present, heading_present),
    )


def _document_metrics(raw_bytes: bytes, lines: list[str]) -> dict[str, int | bool]:
    blank_line_count = sum(not line.strip() for line in lines)
    return {
        "line_count": len(lines),
        "byte_count": len(raw_bytes),
        "blank_line_count": blank_line_count,
        "nonblank_line_count": len(lines) - blank_line_count,
        "empty_document": len(raw_bytes) == 0,
        "has_trailing_newline": raw_bytes.endswith(b"\n"),
    }


def documentation_structure_json(report: DocumentationStructureReport) -> dict[str, Any]:
    return report.to_json_dict()


def format_documentation_structure(
    report: DocumentationStructureReport,
    filters: DocumentationStructureFilters | None = None,
) -> str:
    summary = report.summary
    lines = [
        "Documentation Structure",
        "",
        f"Total documents: {summary['total_documents']}",
        f"Total lines: {summary['total_lines']}",
        f"Total bytes: {summary['total_bytes']}",
        f"Blank lines: {summary['blank_line_count']}",
        f"Nonblank lines: {summary['nonblank_line_count']}",
        f"Empty documents: {summary['empty_document_count']}",
        (
            "Documents without trailing newline: "
            f"{summary['documents_without_trailing_newline']}"
        ),
        f"With YAML front matter: {summary['front_matter_present']}",
        f"Missing YAML front matter: {summary['front_matter_missing']}",
        f"With H1 heading: {summary['heading_present']}",
        f"Missing H1 heading: {summary['heading_missing']}",
        f"Internal docs links: {summary['internal_doc_link_count']}",
        f"External links: {summary['external_link_count']}",
        f"Broken local docs links: {summary['broken_local_doc_link_count']}",
        f"Fenced code blocks: {summary['code_block_count']}",
        f"Unclosed fenced code blocks: {summary['unclosed_code_block_count']}",
        f"Fenced code block languages: {_format_languages(summary['code_block_languages'])}",
        f"Sections: {summary['section_count']}",
        f"Maximum section depth: {summary['max_section_depth']}",
        f"Empty sections: {summary['empty_section_count']}",
        "",
        f"Boundary: {BOUNDARY_TEXT}",
    ]
    incomplete = [d for d in report.documents if d.structure_status != "complete"]
    if incomplete:
        lines.extend(["", "Incomplete documents:"])
        for document in incomplete:
            lines.append(f"- {document.path}: {document.structure_status}")
    filters = filters or DocumentationStructureFilters()
    if (
        filters.missing_front_matter
        or filters.missing_trailing_newline
        or filters.empty_sections
    ):
        lines.extend(["", "Filtered documents:"])
        if report.documents:
            for document in report.documents:
                lines.append(f"- {document.path}: {document.structure_status}")
        else:
            lines.append("- none")
    if filters.include_sections or filters.empty_sections:
        lines.extend(_format_section_details(report))
    if filters.include_links:
        lines.extend(_format_link_details(report))
    if filters.include_code_fences:
        lines.extend(_format_code_fence_details(report))
    return "\n".join(lines)


def _format_section_details(report: DocumentationStructureReport) -> list[str]:
    lines = ["", "Sections:"]
    found = False
    for document in report.documents:
        for section in document.sections:
            found = True
            parent_path = " > ".join(section.parent_heading_path) or "none"
            lines.append(
                f"- {document.path}:{section.start_line}-{section.end_line} "
                f"level={section.heading_level} heading={section.heading_text!r} "
                f"children={section.child_section_count} parent={parent_path}"
            )
    if not found:
        lines.append("- none")
    return lines


def _format_link_details(report: DocumentationStructureReport) -> list[str]:
    lines = ["", "Links:"]
    found = False
    for document in report.documents:
        for link in document.link_observations:
            found = True
            lines.append(
                f"- {document.path}: target={link.raw_target} "
                f"relative={str(link.is_relative).lower()} "
                f"under_docs={str(link.points_under_docs).lower()}"
            )
    if not found:
        lines.append("- none")
    return lines


def _format_code_fence_details(report: DocumentationStructureReport) -> list[str]:
    lines = ["", "Code fences:"]
    found = False
    for document in report.documents:
        for block in document.code_block_observations:
            found = True
            end = block.end_line if block.end_line is not None else "open"
            language = block.language or "none"
            lines.append(
                f"- {document.path}:{block.start_line}-{end} "
                f"type={block.fence_type} language={language} "
                f"closed={str(block.closed).lower()}"
            )
    if not found:
        lines.append("- none")
    return lines


def _code_block_observations(lines: list[str]) -> list[DocumentationCodeBlockRecord]:
    code_blocks: list[DocumentationCodeBlockRecord] = []
    open_fence: tuple[str, int, str | None, str | None, int] | None = None
    for line_number, line in enumerate(lines, start=1):
        match = _FENCE_RE.match(line)
        if match is None:
            continue
        fence = match.group(1)
        fence_char = fence[0]
        info_string = _normalize_info_string(match.group(2))
        if open_fence is None:
            open_fence = (
                fence_char,
                len(fence),
                info_string,
                _language(info_string),
                line_number,
            )
            continue
        open_char, open_length, open_info, open_language, start_line = open_fence
        if fence_char == open_char and len(fence) >= open_length:
            code_blocks.append(
                DocumentationCodeBlockRecord(
                    fence_type=_fence_type(open_char),
                    info_string=open_info,
                    language=open_language,
                    start_line=start_line,
                    end_line=line_number,
                    closed=True,
                )
            )
            open_fence = None
    if open_fence is not None:
        open_char, _open_length, open_info, open_language, start_line = open_fence
        code_blocks.append(
            DocumentationCodeBlockRecord(
                fence_type=_fence_type(open_char),
                info_string=open_info,
                language=open_language,
                start_line=start_line,
                end_line=None,
                closed=False,
            )
        )
    return code_blocks


def _normalize_info_string(raw_info: str) -> str | None:
    info = raw_info.strip()
    return info or None


def _language(info_string: str | None) -> str | None:
    if info_string is None:
        return None
    language = info_string.split(None, 1)[0].strip().lower()
    return language or None


def _fence_type(fence_char: str) -> str:
    return "backtick" if fence_char == "`" else "tilde"


def _code_content_line_numbers(
    code_blocks: tuple[DocumentationCodeBlockRecord, ...], line_count: int
) -> set[int]:
    line_numbers: set[int] = set()
    for block in code_blocks:
        end = block.end_line if block.end_line is not None else line_count + 1
        line_numbers.update(range(block.start_line + 1, end))
    return line_numbers


def _format_languages(languages: object) -> str:
    if not languages:
        return "none"
    return ", ".join(str(language) for language in languages)


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


_ATX_HEADING_RE = re.compile(r"^(#{1,6})(?:[ \t]+|$)(.*)$")
_FENCE_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
_INLINE_LINK_RE = re.compile(r"(?<!!)\[[^\]\n]+\]\(([^)\s]+)(?:\s+[^)]*)?\)")
_REFERENCE_LINK_RE = re.compile(r"^\s{0,3}\[[^\]\n]+\]:\s*(\S+)")
_SCHEME_RE = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*:")


def _heading_outline(
    lines: list[str], code_content_lines: set[int] | None = None
) -> list[DocumentationHeadingRecord]:
    headings: list[DocumentationHeadingRecord] = []
    code_content_lines = code_content_lines or set()
    for line_number, line in enumerate(lines, start=1):
        if line_number in code_content_lines:
            continue
        match = _ATX_HEADING_RE.match(line)
        if match is None:
            continue
        headings.append(
            DocumentationHeadingRecord(
                level=len(match.group(1)),
                text=match.group(2).strip(),
                line_number=line_number,
            )
        )
    return headings


def _section_inventory(
    headings: tuple[DocumentationHeadingRecord, ...],
    lines: list[str],
    code_content_lines: set[int] | None = None,
) -> list[DocumentationSectionRecord]:
    sections: list[DocumentationSectionRecord] = []
    child_counts = [0 for _heading in headings]
    parent_indexes: list[int | None] = []
    stack: list[tuple[int, int]] = []
    for index, heading in enumerate(headings):
        while stack and stack[-1][0] >= heading.level:
            stack.pop()
        parent_index = stack[-1][1] if stack else None
        parent_indexes.append(parent_index)
        if parent_index is not None:
            child_counts[parent_index] += 1
        stack.append((heading.level, index))

    parent_paths = [
        _parent_heading_path(index, headings, parent_indexes)
        for index, _heading in enumerate(headings)
    ]
    for index, heading in enumerate(headings):
        sections.append(
            DocumentationSectionRecord(
                heading_text=heading.text,
                heading_level=heading.level,
                start_line=heading.line_number,
                end_line=_section_end_line(index, headings, len(lines)),
                child_section_count=child_counts[index],
                parent_heading_path=parent_paths[index],
            )
        )
    return sections


def _parent_heading_path(
    index: int,
    headings: tuple[DocumentationHeadingRecord, ...],
    parent_indexes: list[int | None],
) -> tuple[str, ...]:
    path: list[str] = []
    parent_index = parent_indexes[index]
    while parent_index is not None:
        path.append(headings[parent_index].text)
        parent_index = parent_indexes[parent_index]
    return tuple(reversed(path))


def _section_end_line(
    index: int, headings: tuple[DocumentationHeadingRecord, ...], line_count: int
) -> int:
    heading = headings[index]
    for later_heading in headings[index + 1 :]:
        if later_heading.level <= heading.level:
            return later_heading.line_number - 1
    return line_count


def _section_is_empty(
    section: DocumentationSectionRecord,
    lines: list[str],
    code_content_lines: set[int] | None = None,
) -> bool:
    code_content_lines = code_content_lines or set()
    for line_number in range(section.start_line + 1, section.end_line + 1):
        if line_number in code_content_lines:
            continue
        line = lines[line_number - 1]
        if _ATX_HEADING_RE.match(line):
            continue
        if line.strip():
            return False
    return True


def _first_h1(headings: tuple[DocumentationHeadingRecord, ...]) -> str | None:
    for heading in headings:
        if heading.level == 1:
            return heading.text
    return None


def _skipped_heading_level_present(
    headings: tuple[DocumentationHeadingRecord, ...],
) -> bool:
    previous_level = 0
    for heading in headings:
        if heading.level > previous_level + 1:
            return True
        previous_level = heading.level
    return False


def _duplicate_heading_texts(
    headings: tuple[DocumentationHeadingRecord, ...],
) -> list[str]:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for heading in headings:
        if heading.text in seen:
            duplicates.add(heading.text)
        seen.add(heading.text)
    return sorted(duplicates)


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


def _link_observations(
    lines: list[str],
    path: Path,
    source_path: str,
    repo_root: Path | None,
    code_content_lines: set[int] | None = None,
) -> list[DocumentationLinkRecord]:
    links: list[DocumentationLinkRecord] = []
    code_content_lines = code_content_lines or set()
    for line_number, line in enumerate(lines, start=1):
        if line_number in code_content_lines:
            continue
        for target in _markdown_link_targets(line):
            raw_target = _normalize_link_target(target)
            if not raw_target:
                continue
            links.append(
                DocumentationLinkRecord(
                    source_path=source_path,
                    raw_target=raw_target,
                    is_relative=_is_relative_link(raw_target),
                    points_under_docs=_points_under_docs(raw_target, path, repo_root),
                )
            )
    return links


def _markdown_link_targets(line: str) -> list[str]:
    return [
        *(match.group(1) for match in _INLINE_LINK_RE.finditer(line)),
        *(match.group(1) for match in _REFERENCE_LINK_RE.finditer(line)),
    ]


def _normalize_link_target(target: str) -> str:
    return target.strip().strip("<>")


def _is_relative_link(target: str) -> bool:
    return not (target.startswith(("/", "#", "//")) or _SCHEME_RE.match(target))


def _points_under_docs(target: str, source_path: Path, repo_root: Path | None) -> bool:
    if not _is_relative_link(target) or repo_root is None:
        return False
    resolved = _resolved_local_target(target, source_path, repo_root)
    if resolved is None:
        return False
    try:
        resolved.relative_to(repo_root / "docs")
    except ValueError:
        return False
    return True


def _local_doc_link_is_broken(link: DocumentationLinkRecord, repo_root: Path) -> bool:
    if not link.is_relative or not link.points_under_docs:
        return False
    resolved = _resolved_local_target(
        link.raw_target, repo_root / link.source_path, repo_root
    )
    return resolved is not None and not resolved.exists()


def _resolved_local_target(
    target: str, source_path: Path, repo_root: Path
) -> Path | None:
    target_path = target.split("#", 1)[0].split("?", 1)[0]
    if not target_path:
        return source_path.resolve()
    return (source_path.parent / target_path).resolve()
