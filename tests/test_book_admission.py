"""Book admission."""

from __future__ import annotations

import json
import re
from pathlib import Path

from scripts.book_admission import (
    BOOK,
    BOOK_ADMISSION,
    ROOT,
    book_admission,
    book_proper_files,
    book_proper_words,
    witness_addresses,
    scan_active_line,
    witness_grammar_words,
)

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
    assert "book_of_seed/witness_grammar.json" not in files
    assert (BOOK / "witness_grammar.json").is_file()
    assert not (BOOK / "grammar.json").exists()


def test_admitted_material_reference_subjects_resolve_relative_markdown_links():
    grammar = json.loads(
        (BOOK / "witness_grammar.json").read_text(encoding="utf-8")
    )
    declared_references = {
        (reference["subject"], reference["coordinate"])
        for reference in witness_addresses()
    }
    subjects = (
        (BOOK, "this_Book", "book_material", book_admission()),
        (
            ROOT / "rosetta",
            "this_separate_admission_material",
            "separate_admission_material_reference",
            set(_admission_entries(ROSETTA_ADMISSION)),
        ),
    )
    missing: list[tuple[str, str, str]] = []
    for root, subject, coordinate, admission in subjects:
        subject_words = set(
            re.findall(r"[A-Za-z]+", scan_active_line(subject).lower())
        )
        assert (subject, coordinate) in declared_references
        assert subject_words <= admission
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


def test_book_and_rosetta_admission_material_are_distinct():
    modal_compressions = {
        "may",
        "sufficient",
        "possible",
        "allowed",
        "capable",
    }
    rosetta_admission = set(_admission_entries(ROSETTA_ADMISSION))
    assert BOOK_ADMISSION == ROOT / "book_of_seed" / "book_admission.txt"
    assert ROSETTA_ADMISSION != BOOK_ADMISSION
    assert not BOOK_ADMISSION.is_symlink()
    assert not ROSETTA_ADMISSION.is_symlink()
    assert modal_compressions.isdisjoint(book_admission())
    assert modal_compressions <= rosetta_admission
    assert not {
        word
        for word in book_admission()
        if word.startswith("implement") or word.startswith("machine")
    }
    assert {"implementation", "machine"} <= set(
        _admission_entries(ROSETTA_ADMISSION)
    )


def test_rosetta_admits_composite_support_relation_terms():
    rosetta_warrant = {
        word
        for word in _admission_entries(ROSETTA_ADMISSION)
        if word.startswith("warrant")
    }
    assert rosetta_warrant == {"warrant", "warranted", "warranting", "warrants"}
    roots = (ROOT / "rosetta" / "roots.md").read_text(encoding="utf-8")
    assert (
        "Warrant        exact support relation from Evidence + Authority + Scope "
        "+ preserved limits to one Assertion or assignment; composite only, no "
        "new relation by identity"
    ) in roots


def test_failure_is_book_material_and_performative_forms_are_rosetta_composites():
    book_failure = {
        word for word in book_admission() if word.startswith("fail")
    }
    rosetta_failure = {
        word
        for word in _admission_entries(ROSETTA_ADMISSION)
        if word.startswith("fail")
    }
    assert book_failure == {"failure"}
    assert rosetta_failure == {"fail", "failed", "failure", "fails"}
    roots = (ROOT / "rosetta" / "roots.md").read_text(encoding="utf-8")
    assert (
        "These forms compress one exact Act occurrence plus a bounded failure "
        "Assertion\nor result, Evidence, Authority, Scope, and preserved limits."
    ) in roots


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


def test_standing_requires_the_exact_support_relation():
    chapter = (BOOK / "chapters" / "01_constitutional_standing.md").read_text(
        encoding="utf-8"
    )
    assert (
        "Standing for one exact subject requires an exact Responsibility, Act\n"
        "occurrence, Yield, Authority, Scope, limits, and result for that subject."
    ) in chapter


def test_composite_is_communication_in_rosetta_not_active_book_grammar():
    book_composite = {
        word for word in book_admission() if word.startswith("composite")
    }
    rosetta_composite = {
        word
        for word in _admission_entries(ROSETTA_ADMISSION)
        if word.startswith("composite")
    }
    assert book_composite == set()
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
        "\nActive Book material carries words absent from Book admission:\n"
        + report
    )


def test_book_admission_carries_no_unused_words():
    unused = sorted(book_admission() - set(book_proper_words()))
    assert not unused, (
        "\nBook admission carries words absent from active Book material: "
        + ", ".join(unused)
    )


def test_witness_grammar_words_in_book_admission():
    assert witness_grammar_words() <= book_admission()
    grammar = json.loads(
        (BOOK / "witness_grammar.json").read_text(encoding="utf-8")
    )

    def contains_host_boolean(value: object) -> bool:
        if type(value) is bool:
            return True
        if type(value) is dict:
            return any(contains_host_boolean(nested) for nested in value.values())
        if type(value) is list:
            return any(contains_host_boolean(nested) for nested in value)
        return False

    assert not contains_host_boolean(grammar)


PYTEST_ADMISSION = (
    test_book_proper_scope_excludes_rosetta,
    test_admitted_material_reference_subjects_resolve_relative_markdown_links,
    test_book_and_rosetta_admission_material_are_distinct,
    test_rosetta_admits_composite_support_relation_terms,
    test_failure_is_book_material_and_performative_forms_are_rosetta_composites,
    test_clause_coordinate_tokens_require_explicit_curation,
    test_standing_requires_the_exact_support_relation,
    test_composite_is_communication_in_rosetta_not_active_book_grammar,
    test_book_proper_is_within_book_admission,
    test_book_admission_carries_no_unused_words,
    test_witness_grammar_words_in_book_admission,
)
