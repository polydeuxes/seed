"""Book admission."""

from __future__ import annotations

import json
import re
from pathlib import Path

from scripts.book_admission import (
    BOOK,
    ROOT,
    book_admission,
    book_proper_files,
    book_proper_words,
    scan_active_line,
    witness_grammar_words,
)

BOOK_ADMISSION = BOOK / "book_admission.txt"
ROSETTA_ADMISSION = ROOT / "rosetta" / "rosetta_admission.txt"


def _admission_entries(path: Path) -> dict[str, str]:
    entries: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").split("\n"):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        divided = line.split("#", 1)
        word = divided[0]
        reason = divided[1] if len(divided) == 2 else ""
        entries[word.strip()] = reason.strip()
    return entries


def test_book_proper_scope_excludes_rosetta():
    files = {path.relative_to(ROOT).as_posix() for path in book_proper_files()}
    assert any(path.startswith("book_of_seed/chapters/") for path in files)
    assert not any("/rosetta/" in path or path.startswith("rosetta/") for path in files)
    assert "book_of_seed/grammar.json" not in files


def test_admitted_material_reference_subjects_resolve_relative_markdown_links():
    grammar = json.loads((BOOK / "grammar.json").read_text(encoding="utf-8"))
    declared_references = {
        (reference["reference"], reference["coordinate"])
        for reference in grammar["root_references"]
    }
    subjects = (
        (BOOK, "this_Book", "book_material"),
        (ROOT / "rosetta", "this_Rosetta", "rosetta_reference"),
    )
    missing: list[tuple[str, str, str]] = []
    for root, subject, coordinate in subjects:
        subject_words = set(
            re.findall(r"[A-Za-z]+", scan_active_line(subject).lower())
        )
        assert (subject, coordinate) in declared_references
        assert subject_words <= book_admission()
        for path in root.rglob("*.md"):
            for target in re.findall(
                r"\]\(([^)#]+)(?:#[^)]+)?\)", path.read_text(encoding="utf-8")
            ):
                if "://" in target:
                    continue
                if not (path.parent / target).is_file():
                    missing.append(
                        (subject, path.relative_to(ROOT).as_posix(), target)
                    )

    assert missing == []


def test_book_has_no_separate_admission_authority():
    assert BOOK_ADMISSION == ROOT / "book_of_seed" / "book_admission.txt"
    assert ROSETTA_ADMISSION != BOOK_ADMISSION
    assert not BOOK_ADMISSION.exists()
    assert not ROSETTA_ADMISSION.is_symlink()


def test_warrant_admission_is_broad_in_rosetta_and_singular_in_book():
    book_warrant = {word for word in book_admission() if word.startswith("warrant")}
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
        word for word in book_admission() if word.startswith("composite")
    }
    rosetta_composite = {
        word
        for word in _admission_entries(ROSETTA_ADMISSION)
        if word.startswith("composite")
    }
    assert book_composite == {"composite"}
    assert rosetta_composite == {"composite", "composites"}


def test_book_proper_is_within_book_admission():
    assert book_admission() == set(book_proper_words())


def test_book_admission_carries_no_unused_words():
    assert book_admission() - set(book_proper_words()) == set()


def test_witness_grammar_words_in_book_admission():
    assert witness_grammar_words() <= book_admission()


FIDELITY_SUBJECTS = {
    "warrant_standing_boundary": (
        test_warrant_remains_lowercase_and_bounded_to_the_three_standing_sentences,
    ),
    "active_book_scope": (test_book_proper_scope_excludes_rosetta,),
    "admitted_material_reference_relative_resolution": (
        test_admitted_material_reference_subjects_resolve_relative_markdown_links,
    ),
    "book_rosetta_admission_distinction": (
        test_book_has_no_separate_admission_authority,
    ),
    "book_rosetta_warrant_admission_distinction": (
        test_warrant_admission_is_broad_in_rosetta_and_singular_in_book,
    ),
    "clause_coordinate_word_admission": (
        test_clause_coordinate_tokens_require_explicit_curation,
    ),
    "book_rosetta_composite_admission_distinction": (
        test_composite_admission_is_broad_in_rosetta_and_singular_in_book,
    ),
    "active_book_within_book_admission": (
        test_book_proper_is_within_book_admission,
    ),
    "book_admission_active_law_use": (
        test_book_admission_carries_no_unused_words,
    ),
    "witness_grammar_words_in_book_admission": (
        test_witness_grammar_words_in_book_admission,
    ),
}
