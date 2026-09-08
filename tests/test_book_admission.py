"""Book distinctions."""

from __future__ import annotations

import ast
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
from tests.test_runtime_witness_grammar import (
    _authored_event_material_strings,
    _runtime_trees,
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


def test_lexical_admission_has_one_test_reader():
    readers = set()
    for path in sorted((ROOT / "tests").glob("test_*.py")):
        tree = ast.parse(
            path.read_text(encoding="utf-8"),
            filename=str(path),
        )
        reads_admission = any(
            (
                isinstance(node, ast.ImportFrom)
                and node.module == "scripts.book_admission"
                and any(
                    name.name in {"BOOK_ADMISSION", "book_admission"}
                    for name in node.names
                )
            )
            or (
                isinstance(node, ast.Constant)
                and node.value == "book_admission.txt"
            )
            for node in ast.walk(tree)
        )
        if reads_admission:
            readers.add(path.relative_to(ROOT).as_posix())

    assert readers == {"tests/test_book_admission.py"}


def test_rosetta_translates_warrant_to_exact_references():
    rosetta_warrant = {
        word
        for word in _admission_entries(ROSETTA_ADMISSION)
        if word.startswith("warrant")
    }
    assert rosetta_warrant == {"warrant"}
    translations = (
        ROOT / "rosetta" / "standing_and_responsibility.md"
    ).read_text(encoding="utf-8")
    assert (
        "Warrant        exact source and occurrence references for one Assertion "
        "or result; composite only, no new relation by identity"
    ) in translations


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
    translations = (
        ROOT / "rosetta" / "standing_and_responsibility.md"
    ).read_text(encoding="utf-8")
    assert (
        "These forms compress one exact Act occurrence plus a bounded failure "
        "Assertion\nor result and exact source and occurrence references."
    ) in translations


def test_clause_coordinate_tokens_require_explicit_curation():
    assert "g" in book_admission()

    uncurated_coordinate_words = set(
        re.findall(
            r"[A-Za-z]+",
            scan_active_line("01.Source.Uncuratedcoordinate").lower(),
        )
    ) - book_admission()

    assert uncurated_coordinate_words == {"uncuratedcoordinate"}


def test_current_coordinates_require_an_exact_occurrence_boundary():
    chapter = (BOOK / "chapters" / "01_current_coordinates.md").read_text(
        encoding="utf-8"
    )
    assert (
        "For an exact subject, its exact current coordinates through an exact\n"
        "occurrence boundary are its exact coordinates whose occurrences\n"
        "are in a Locality through that boundary."
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
    assert rosetta_composite == {"composite"}


def test_book_distinction_words_are_admitted():
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


def test_book_admission_contains_only_book_distinction_words():
    unused = sorted(book_admission() - set(book_proper_words()))
    assert not unused, (
        "\nBook admission contains words absent from active Book material: "
        + ", ".join(unused)
    )


def _unadmitted_test_module_prose(
    material: str,
    *,
    book_words: set[str],
    explanation_words: set[str],
) -> dict[str, list[str]]:
    absent: dict[str, list[str]] = {}
    paragraphs = re.split(r"\n\s*\n", material.strip())
    registers = (
        ("distinction", paragraphs[0], book_words),
        ("explanation", "\n".join(paragraphs[1:]), explanation_words),
    )
    for register, prose, admitted in registers:
        words = {
            word
            for word in re.findall(
                r"[A-Za-z]+",
                scan_active_line(prose).lower(),
            )
        }
        unadmitted = sorted(words - admitted)
        if unadmitted:
            absent[register] = unadmitted
    return absent


def test_test_module_distinction_words_are_admitted():
    book_words = book_admission()
    explanation_words = book_words | set(_admission_entries(ROSETTA_ADMISSION))
    absent: dict[str, dict[str, list[str]]] = {}
    missing: list[str] = []
    for path in sorted((ROOT / "tests").glob("test_*.py")):
        tree = ast.parse(
            path.read_text(encoding="utf-8"),
            filename=str(path),
        )
        material = ast.get_docstring(tree, clean=False)
        if material is None:
            missing.append(path.relative_to(ROOT).as_posix())
            continue
        unadmitted = _unadmitted_test_module_prose(
            material,
            book_words=book_words,
            explanation_words=explanation_words,
        )
        if unadmitted:
            absent[path.relative_to(ROOT).as_posix()] = unadmitted

    report = "\n".join(
        f"  {path} [{register}]: {', '.join(words)}"
        for path, registers in absent.items()
        for register, words in registers.items()
    )
    assert not missing and not absent, (
        "\nTest modules without a Distinction:\n  "
        + "\n  ".join(missing)
        + "\nTest distinction or explanation has words absent from its admission:\n"
        + report
    )


def test_rosetta_word_enters_explanation_but_not_distinction():
    book_words = book_admission()
    explanation_words = book_words | set(_admission_entries(ROSETTA_ADMISSION))

    assert _unadmitted_test_module_prose(
        "Validation.\n\nExact coordinates.",
        book_words=book_words,
        explanation_words=explanation_words,
    ) == {"distinction": ["validation"]}
    assert _unadmitted_test_module_prose(
        "Exact coordinates.\n\nValidation.",
        book_words=book_words,
        explanation_words=explanation_words,
    ) == {}


def _unadmitted_authored_event_material(path: Path, tree: ast.Module):
    admitted = book_admission()
    violations = set()
    for source, line, value in _authored_event_material_strings(path, tree):
        for word in re.findall(r"[A-Za-z]+", scan_active_line(value).lower()):
            if word not in admitted:
                violations.add((source, line, word, value))
    return sorted(violations)


def test_seed_authored_event_material_values_have_lexical_admission():
    violations = []
    for path, tree in _runtime_trees():
        violations.extend(_unadmitted_authored_event_material(path, tree))
    assert violations == [], "\n" + "\n".join(
        f"{path}:{line} [{word}] {value}"
        for path, line, word, value in violations
    )


def test_authored_value_admission_refuses_an_unadmitted_word_without_naming_it():
    tree = ast.parse(
        'ledger.append(SOME_KIND, {"standing": "invented"})'
    )
    assert _unadmitted_authored_event_material(Path("external.py"), tree) == [
        ("external.py", 1, "invented", "invented")
    ]


def test_authored_value_admission_reads_a_local_material_function():
    tree = ast.parse(
        'def material():\n    return {"standing": "invented"}\n'
        'ledger.append(SOME_KIND, material())'
    )
    assert _unadmitted_authored_event_material(Path("external.py"), tree) == [
        ("external.py", 2, "invented", "invented")
    ]


def test_authored_value_admission_reads_local_material_function_arguments():
    tree = ast.parse(
        'def material(*, standing):\n    return {"standing": standing}\n'
        'ledger.append(SOME_KIND, {"dimensions": material(standing="invented")})'
    )
    assert _unadmitted_authored_event_material(Path("external.py"), tree) == [
        ("external.py", 3, "invented", "invented")
    ]


def test_supplied_material_is_not_seed_authored_language():
    tree = ast.parse(
        'ledger.append(SOME_KIND, {"standing": operator_material})'
    )
    assert _unadmitted_authored_event_material(Path("external.py"), tree) == []


def test_witness_grammar_distinction_words_are_admitted():
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
