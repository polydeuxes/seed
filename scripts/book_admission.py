"""Independent Book admission and the material it bounds."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / "book_of_seed"
BOOK_ADMISSION = BOOK / "book_admission.txt"


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
    """Read the independently curated words admitted to this Book."""

    return {
        line.split("#", 1)[0].strip()
        for line in BOOK_ADMISSION.read_text(encoding="utf-8").splitlines()
        if line.split("#", 1)[0].strip()
    }


def witness_grammar_words() -> set[str]:
    return {
        word
        for line in (BOOK / "witness_grammar.json")
        .read_text(encoding="utf-8")
        .split("\n")
        for word in re.findall(r"[A-Za-z]+", scan_active_line(line).lower())
    }
