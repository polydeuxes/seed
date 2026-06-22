"""Read-only structural observation for repository Markdown documentation."""

from __future__ import annotations

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
class DocumentationStructureRecord:
    path: str
    front_matter_present: bool
    front_matter_keys: tuple[str, ...]
    heading_present: bool
    title_heading: str | None
    structure_status: str

    def to_json_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["front_matter_keys"] = list(self.front_matter_keys)
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
    }
    return DocumentationStructureReport(documents, summary, dict(BOUNDARY))


def observe_markdown_document(path: Path, repo_root: Path | None = None) -> DocumentationStructureRecord:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    front_matter_present, keys = _front_matter(lines)
    title_heading = _first_h1(lines)
    heading_present = title_heading is not None
    return DocumentationStructureRecord(
        path=_relative_path(path, repo_root),
        front_matter_present=front_matter_present,
        front_matter_keys=tuple(keys),
        heading_present=heading_present,
        title_heading=title_heading,
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


def _first_h1(lines: list[str]) -> str | None:
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    return None


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
