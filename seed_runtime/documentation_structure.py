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
class DocumentationHeadingRecord:
    level: int
    text: str
    line_number: int


@dataclass(frozen=True)
class DocumentationLinkRecord:
    source_path: str
    raw_target: str
    is_relative: bool
    points_under_docs: bool


@dataclass(frozen=True)
class DocumentationStructureRecord:
    path: str
    front_matter_present: bool
    front_matter_keys: tuple[str, ...]
    heading_present: bool
    title_heading: str | None
    heading_outline: tuple[DocumentationHeadingRecord, ...]
    has_section_headings: bool
    max_heading_depth: int
    skipped_heading_level_present: bool
    duplicate_heading_texts: tuple[str, ...]
    link_observations: tuple[DocumentationLinkRecord, ...]
    structure_status: str

    def to_json_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["front_matter_keys"] = list(self.front_matter_keys)
        data["heading_outline"] = [asdict(heading) for heading in self.heading_outline]
        data["duplicate_heading_texts"] = list(self.duplicate_heading_texts)
        data["link_observations"] = [asdict(link) for link in self.link_observations]
        return data


@dataclass(frozen=True)
class DocumentationStructureReport:
    documents: tuple[DocumentationStructureRecord, ...]
    summary: dict[str, int]
    boundary: dict[str, bool]

    def to_json_dict(self) -> dict[str, Any]:
        return {
            "documents": [document.to_json_dict() for document in self.documents],
            "summary": dict(self.summary),
            "boundary": dict(self.boundary),
        }


def observe_documentation_structure(repo_root: Path) -> DocumentationStructureReport:
    """Observe structural metadata for allowlisted top-level docs/*.md files."""

    docs_dir = repo_root / "docs"
    documents = tuple(
        observe_markdown_document(path, repo_root)
        for path in sorted(docs_dir.glob("*.md"))
        if path.is_file()
    )
    summary = {
        "total_documents": len(documents),
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
    }
    return DocumentationStructureReport(documents, summary, dict(BOUNDARY))


def observe_markdown_document(path: Path, repo_root: Path | None = None) -> DocumentationStructureRecord:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    front_matter_present, keys = _front_matter(lines)
    heading_outline = tuple(_heading_outline(lines))
    source_path = _relative_path(path, repo_root)
    link_observations = tuple(_link_observations(lines, path, source_path, repo_root))
    title_heading = _first_h1(heading_outline)
    heading_present = title_heading is not None
    return DocumentationStructureRecord(
        path=source_path,
        front_matter_present=front_matter_present,
        front_matter_keys=tuple(keys),
        heading_present=heading_present,
        title_heading=title_heading,
        heading_outline=heading_outline,
        has_section_headings=any(heading.level > 1 for heading in heading_outline),
        max_heading_depth=max((heading.level for heading in heading_outline), default=0),
        skipped_heading_level_present=_skipped_heading_level_present(heading_outline),
        duplicate_heading_texts=tuple(_duplicate_heading_texts(heading_outline)),
        link_observations=link_observations,
        structure_status=_structure_status(front_matter_present, heading_present),
    )


def documentation_structure_json(report: DocumentationStructureReport) -> dict[str, Any]:
    return report.to_json_dict()


def format_documentation_structure(report: DocumentationStructureReport) -> str:
    summary = report.summary
    lines = [
        "Documentation Structure",
        "",
        f"Total documents: {summary['total_documents']}",
        f"With YAML front matter: {summary['front_matter_present']}",
        f"Missing YAML front matter: {summary['front_matter_missing']}",
        f"With H1 heading: {summary['heading_present']}",
        f"Missing H1 heading: {summary['heading_missing']}",
        f"Internal docs links: {summary['internal_doc_link_count']}",
        f"External links: {summary['external_link_count']}",
        f"Broken local docs links: {summary['broken_local_doc_link_count']}",
        "",
        f"Boundary: {BOUNDARY_TEXT}",
    ]
    incomplete = [d for d in report.documents if d.structure_status != "complete"]
    if incomplete:
        lines.extend(["", "Incomplete documents:"])
        for document in incomplete:
            lines.append(f"- {document.path}: {document.structure_status}")
    return "\n".join(lines)


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
_INLINE_LINK_RE = re.compile(r"(?<!!)\[[^\]\n]+\]\(([^)\s]+)(?:\s+[^)]*)?\)")
_REFERENCE_LINK_RE = re.compile(r"^\s{0,3}\[[^\]\n]+\]:\s*(\S+)")
_SCHEME_RE = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*:")


def _heading_outline(lines: list[str]) -> list[DocumentationHeadingRecord]:
    headings: list[DocumentationHeadingRecord] = []
    for line_number, line in enumerate(lines, start=1):
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
    lines: list[str], path: Path, source_path: str, repo_root: Path | None
) -> list[DocumentationLinkRecord]:
    links: list[DocumentationLinkRecord] = []
    for line in lines:
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
    resolved = _resolved_local_target(link.raw_target, repo_root / link.source_path, repo_root)
    return resolved is not None and not resolved.exists()


def _resolved_local_target(target: str, source_path: Path, repo_root: Path) -> Path | None:
    target_path = target.split("#", 1)[0].split("?", 1)[0]
    if not target_path:
        return source_path.resolve()
    return (source_path.parent / target_path).resolve()
