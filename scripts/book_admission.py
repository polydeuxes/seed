"""Admission carried by this Book's active constitutional material."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / "book_of_seed"


def scan_active_line(line: str) -> str:
    scanned = re.sub(r"\]\([^)]*\)", "]()", line)
    return re.sub(r"[_-]+", " ", scanned)


def book_proper_files() -> tuple[Path, ...]:
    """Return this Book's active prose, excluding its witness grammar."""

    chapters = tuple((BOOK / "chapters").glob("*.md"))
    return chapters + (BOOK / "README.md", BOOK / "concordance.md")


def book_proper_words() -> dict[str, list[tuple[str, int]]]:
    found: dict[str, list[tuple[str, int]]] = {}
    for path in book_proper_files():
        relative = path.relative_to(ROOT).as_posix()
        for number, line in enumerate(
            path.read_text(encoding="utf-8").split("\n"), start=1
        ):
            for word in re.findall(r"[A-Za-z]+", scan_active_line(line).lower()):
                found.setdefault(word, []).append((relative, number))
    return found


def book_admission() -> set[str]:
    """Return exactly the words carried by this Book's active prose."""

    return set(book_proper_words())


def witness_grammar_words() -> set[str]:
    return {
        word
        for line in (BOOK / "grammar.json").read_text(encoding="utf-8").split("\n")
        for word in re.findall(r"[A-Za-z]+", scan_active_line(line).lower())
    }
