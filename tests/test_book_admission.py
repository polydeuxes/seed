"""Book admission."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / "book_of_seed"
BOOK_ADMISSION = BOOK / "book_admission.txt"
ROSETTA_ADMISSION = ROOT / "rosetta" / "rosetta_admission.txt"


def scan_active_line(line: str) -> str:
    scanned = re.sub(r"\]\([^)]*\)", "]()", line)
    return re.sub(r"[_-]+", " ", scanned)


def book_proper_files() -> list[Path]:
    files = sorted((BOOK / "chapters").glob("*.md"))
    for extra in ("README.md", "concordance.md", "grammar.json"):
        candidate = BOOK / extra
        if candidate.exists():
            files.append(candidate)
    return files


def _admission_entries(path: Path = BOOK_ADMISSION) -> dict[str, str]:
    entries: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").split("\n"):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        divided = line.split("#", 1)
        word = divided[0]
        reason = divided[1] if len(divided) == 2 else ""
        entries[word.strip()] = reason.strip()
    return entries


def book_admission() -> set[str]:
    return set(_admission_entries())


def book_proper_words() -> dict[str, list[tuple[str, int]]]:
    found: dict[str, list[tuple[str, int]]] = {}
    for path in book_proper_files():
        rel = path.relative_to(ROOT).as_posix()
        for number, line in enumerate(path.read_text().split("\n"), start=1):
            for word in re.findall(r"[A-Za-z]+", scan_active_line(line).lower()):
                found.setdefault(word, []).append((rel, number))
    return found


def machine_grammar_words() -> set[str]:
    return {
        word
        for line in (BOOK / "grammar.json").read_text().split("\n")
        for word in re.findall(r"[A-Za-z]+", scan_active_line(line).lower())
    }


def test_book_proper_scope_excludes_rosetta():
    files = {path.relative_to(ROOT).as_posix() for path in book_proper_files()}
    assert any(path.startswith("book_of_seed/chapters/") for path in files)
    assert not any("/rosetta/" in path or path.startswith("rosetta/") for path in files)


def test_book_and_rosetta_file_addresses_use_underscores_not_hyphens():
    roots = (BOOK, ROOT / "rosetta")
    hyphenated = {
        path.relative_to(ROOT).as_posix()
        for root in roots
        for path in root.rglob("*")
        if path.is_file() and "-" in path.name
    }

    assert hyphenated == set()


def test_book_and_rosetta_relative_markdown_links_resolve():
    markdown = tuple(
        path
        for root in (BOOK, ROOT / "rosetta")
        for path in root.rglob("*.md")
    )
    missing: list[tuple[str, str]] = []
    for path in markdown:
        for target in re.findall(
            r"\]\(([^)#]+)(?:#[^)]+)?\)", path.read_text(encoding="utf-8")
        ):
            if "://" in target:
                continue
            if not (path.parent / target).is_file():
                missing.append((path.relative_to(ROOT).as_posix(), target))

    assert missing == []


def test_book_has_its_own_admission_and_points_to_rosetta():
    assert BOOK_ADMISSION == ROOT / "book_of_seed" / "book_admission.txt"
    assert ROSETTA_ADMISSION != BOOK_ADMISSION
    assert not BOOK_ADMISSION.is_symlink()
    assert not ROSETTA_ADMISSION.is_symlink()
    assert (
        "# Rosetta admission: ../rosetta/rosetta_admission.txt"
        in BOOK_ADMISSION.read_text(encoding="utf-8").splitlines()
    )
    assert set(_admission_entries(BOOK_ADMISSION)) < set(
        _admission_entries(ROSETTA_ADMISSION)
    )


def test_warrant_admission_is_broad_in_rosetta_and_singular_in_book():
    book_warrant = {
        word
        for word in _admission_entries(BOOK_ADMISSION)
        if word.startswith("warrant")
    }
    rosetta_warrant = {
        word
        for word in _admission_entries(ROSETTA_ADMISSION)
        if word.startswith("warrant")
    }
    assert book_warrant == {"warrant"}
    assert rosetta_warrant == {"warrant", "warranted", "warranting", "warrants"}


def test_clause_coordinate_tokens_require_explicit_curation():
    assert "g" in book_admission()
    assert "g" in _admission_entries(ROSETTA_ADMISSION)

    uncurated_coordinate_words = set(
        re.findall(
            r"[A-Za-z]+",
            scan_active_line("01.Source.Uncuratedcoordinate").lower(),
        )
    ) - book_admission()

    assert uncurated_coordinate_words == {"uncuratedcoordinate"}


def test_warrant_remains_lowercase_and_bounded_to_the_three_standing_sentences():
    chapter = (BOOK / "chapters" / "02_constitutional_standing.md").read_text(
        encoding="utf-8"
    )
    paragraph = next(
        paragraph
        for paragraph in chapter.split("\n\n")
        if "warrant" in paragraph.lower()
    )

    assert "Warrant" not in paragraph
    assert paragraph == (
        "Preserved material does not warrant an Assertion it carries. "
        "This use of warrant is a composite. "
            "Standing carried by this Seed requires warrant through its Evidence, "
            "Authority, Scope, and preserved limits."
    )


def test_composite_admission_is_broad_in_rosetta_and_singular_in_book():
    book_composite = {
        word
        for word in _admission_entries(BOOK_ADMISSION)
        if word.startswith("composite")
    }
    rosetta_composite = {
        word
        for word in _admission_entries(ROSETTA_ADMISSION)
        if word.startswith("composite")
    }
    assert book_composite == {"composite"}
    assert rosetta_composite == {"composite", "composites"}


def test_book_proper_is_within_book_admission():
    unadmitted = {
        word: places
        for word, places in book_proper_words().items()
        if word not in book_admission()
    }
    report = "\n".join(
        f"  {word} -- {places[0][0]}:{places[0][1]}"
        + (f" and {len(places) - 1} more" if len(places) > 1 else "")
        for word, places in sorted(unadmitted.items())
    )
    assert not unadmitted, (
        "\nActive law carries vocabulary the lexicon does not admit.\n"
            "Remove it or request curation; automated agents must not amend Book admission:\n"
        + report
    )


def test_book_admission_carries_no_unused_words():
    unused = sorted(book_admission() - set(book_proper_words()))
    assert not unused, (
        "\nBook admission carries words active law no longer carries: "
        + ", ".join(unused)
    )


def test_book_admission_and_machine_grammar_match():
    assert book_admission() == machine_grammar_words()
