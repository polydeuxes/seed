"""Project the ordered chapter representation of the Book.

The Markdown chapters and ``grammar.json`` are two representations of the
Book.  This module gives deterministic tests a mechanical comparison boundary:
it addresses each chapter statement by chapter, section, clause, and position,
then commits to that exact ordered projection.  It does not make either file
the Book by identity.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from pathlib import Path
import re


_CHAPTER_NAME = re.compile(r"^(?P<number>[0-9]{2})-(?P<name>.+)\.md$")
_CLAUSE_HEADING = re.compile(
    r"^(?P<clause>[0-9]+\.[A-Za-z]+\.[A-Z](?:\.[0-9]+)?)\s+—\s+.+$"
)


class BookProjectionError(ValueError):
    """The chapter representation cannot be addressed from exact material."""


@dataclass(frozen=True)
class BookSentence:
    """One exact ordered statement in a Markdown chapter representation."""

    chapter_number: int
    chapter_path: str
    chapter_title: str
    sentence_number: int
    section: str
    clause: str | None
    kind: str
    standing: str
    text: str

    @property
    def commitment(self) -> str:
        encoded = json.dumps(
            asdict(self), sort_keys=True, separators=(",", ":"), ensure_ascii=False
        ).encode("utf-8")
        return sha256(encoded).hexdigest()


@dataclass(frozen=True)
class BookChapter:
    """One ordered chapter and the statements its representation carries."""

    number: int
    path: str
    title: str
    clauses: tuple[str, ...]
    sentences: tuple[BookSentence, ...]

    @property
    def ordered_sentence_digest(self) -> str:
        encoded = json.dumps(
            [sentence.commitment for sentence in self.sentences],
            separators=(",", ":"),
        ).encode("ascii")
        return sha256(encoded).hexdigest()

    def machine_coordinates(self) -> dict[str, object]:
        return {
            "number": self.number,
            "path": self.path,
            "title": self.title,
            "clause_order": list(self.clauses),
            "sentence_count": len(self.sentences),
            "ordered_sentence_digest": self.ordered_sentence_digest,
        }


def _sentence_standing(section: str, text: str) -> str:
    if "[UNRESOLVED]" in text:
        return "Unknown"
    if section == "Related chapters":
        return "navigation_only"
    if section == "Representative repository anchors":
        return "implementation_reference"
    if section == "Counterexamples or failure modes":
        return "counterexample"
    if section == "Core question":
        return "question"
    return "represented"


def _split_sentences(paragraph: str) -> tuple[str, ...]:
    """Split prose at exact sentence punctuation outside inline code.

    Markdown paragraphs may wrap across lines.  Backtick-delimited
    implementation names can themselves contain punctuation, so punctuation
    inside inline code does not end a sentence.
    """

    material = " ".join(paragraph.split())
    if not material:
        return ()
    results: list[str] = []
    start = 0
    in_code = False
    index = 0
    while index < len(material):
        character = material[index]
        if character == "`":
            in_code = not in_code
        elif (
            not in_code
            and character in ".!?"
            and (index + 1 == len(material) or material[index + 1].isspace())
        ):
            results.append(material[start : index + 1].strip())
            index += 1
            while index < len(material) and material[index].isspace():
                index += 1
            start = index
            continue
        index += 1
    remainder = material[start:].strip()
    if remainder:
        results.append(remainder)
    return tuple(results)


def _project_chapter(path: Path, *, root: Path) -> BookChapter:
    match = _CHAPTER_NAME.fullmatch(path.name)
    if match is None:
        raise BookProjectionError(f"chapter has no ordered filename: {path.name}")
    number = int(match.group("number"))
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or not lines[0].startswith("# "):
        raise BookProjectionError(f"chapter has no exact title: {path.name}")
    title = lines[0][2:].strip()
    if not title:
        raise BookProjectionError(f"chapter has an empty title: {path.name}")

    relative_path = path.relative_to(root).as_posix()
    section = "chapter"
    clause: str | None = None
    clauses: list[str] = []
    sentence_fields: list[tuple[str, str | None, str, str]] = []
    paragraph: list[str] = []
    in_fence = False

    def append_text(text: str, kind: str) -> None:
        for sentence in _split_sentences(text):
            sentence_fields.append((section, clause, kind, sentence))

    def flush_paragraph() -> None:
        if paragraph:
            append_text(" ".join(paragraph), "prose")
            paragraph.clear()

    for line in lines[1:]:
        stripped = line.strip()
        if stripped.startswith("```"):
            flush_paragraph()
            in_fence = not in_fence
            continue
        if in_fence:
            if stripped:
                append_text(stripped, "grammar_expression")
            continue
        if stripped.startswith("## ") and not stripped.startswith("### "):
            flush_paragraph()
            section = stripped[3:].strip()
            clause = None
            continue
        if stripped.startswith("### "):
            flush_paragraph()
            heading = stripped[4:].strip()
            clause_match = _CLAUSE_HEADING.fullmatch(heading)
            clause = clause_match.group("clause") if clause_match else None
            section = heading
            if clause is not None:
                if clause in clauses:
                    raise BookProjectionError(
                        f"chapter repeats clause {clause}: {path.name}"
                    )
                clauses.append(clause)
            continue
        if stripped.startswith("- "):
            flush_paragraph()
            append_text(stripped[2:].strip(), "list_statement")
            continue
        if not stripped:
            flush_paragraph()
            continue
        paragraph.append(stripped)
    flush_paragraph()

    sentences = tuple(
        BookSentence(
            chapter_number=number,
            chapter_path=relative_path,
            chapter_title=title,
            sentence_number=index,
            section=statement_section,
            clause=statement_clause,
            kind=kind,
            standing=_sentence_standing(statement_section, text),
            text=text,
        )
        for index, (statement_section, statement_clause, kind, text) in enumerate(
            sentence_fields, start=1
        )
    )
    if not sentences:
        raise BookProjectionError(f"chapter carries no statements: {path.name}")
    return BookChapter(
        number=number,
        path=relative_path,
        title=title,
        clauses=tuple(clauses),
        sentences=sentences,
    )


def project_book(chapters_directory: str | Path) -> tuple[BookChapter, ...]:
    """Project every chapter in exact filename order."""

    chapters_path = Path(chapters_directory)
    paths = sorted(chapters_path.glob("*.md"))
    chapters = tuple(
        _project_chapter(path, root=chapters_path.parent) for path in paths
    )
    expected = tuple(range(1, len(chapters) + 1))
    observed = tuple(chapter.number for chapter in chapters)
    if observed != expected:
        raise BookProjectionError(
            f"chapter order must be contiguous: expected {expected}, observed {observed}"
        )
    return chapters


def machine_book_coordinates(chapters_directory: str | Path) -> list[dict[str, object]]:
    """Return the exact chapter coordinates compared with ``grammar.json``."""

    return [chapter.machine_coordinates() for chapter in project_book(chapters_directory)]
