import json
from pathlib import Path

import pytest

from seed_runtime.book_projection import (
    BookProjectionError,
    machine_book_coordinates,
    project_book,
)


ROOT = Path(__file__).resolve().parents[1]
GRAMMAR = ROOT / "book_of_seed/grammar.json"
CHAPTERS = ROOT / "book_of_seed/chapters"


def _active_book() -> str:
    return "\n".join(
        path.read_text(encoding="utf-8") for path in sorted(CHAPTERS.glob("*.md"))
    )


def _assert_structural_edge_clauses(grammar: dict, active_book: str) -> None:
    for edge, coordinates in grammar["structural_edges"].items():
        clause = coordinates["book_clause"]
        assert edge
        assert active_book.count(f"### {clause} ") == 1


def test_machine_readable_grammar_traverses_responsibility_from_standing():
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))

    assert grammar["version"] == 3
    assert grammar["spine"] == {
        "root": "Standing",
        "path": [
            "Standing",
            "Responsibility",
            "exact_Act",
            "Act_occurrence",
            "result",
            "Standing",
        ],
        "responsibility_assignment_subject": (
            "responsible_boundary_bears_Responsibility"
        ),
        "assignment_requires": "current_Standing",
        "does_not_establish": [
            "Responsibility_by_identity",
            "Responsibility_occurrence",
            "result_Standing_revision",
        ],
    }
    assert grammar["implementation_witness"]["discriminators"] == [
        "content",
        "locality",
        "digest",
    ]
    assert grammar["clauses"]
    active_book = _active_book()
    _assert_structural_edge_clauses(grammar, active_book)
    assert active_book.count(f"### {grammar['fidelity']['book_clause']} ") == 1
    for clause_id, clause in grammar["clauses"].items():
        assert clause["subject"]
        assert clause["responsibility"]
        assert active_book.count(f"### {clause_id} ") == 1


def test_missing_structural_edge_clause_is_detected():
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))
    active_book = _active_book()
    locality_clause = grammar["structural_edges"]["locality"]["book_clause"]
    broken_book = active_book.replace(
        f"### {locality_clause} ", "### 01.Missing.A ", 1
    )

    try:
        _assert_structural_edge_clauses(grammar, broken_book)
    except AssertionError:
        pass
    else:
        raise AssertionError("missing Locality clause escaped the grammar audit")


def test_machine_grammar_matches_the_ordered_chapter_representation():
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))

    assert machine_book_coordinates(CHAPTERS) == grammar["book_representation"][
        "chapters"
    ]


def test_every_chapter_sentence_has_an_exact_order_and_bounded_standing():
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))
    projection = project_book(CHAPTERS)
    admitted = set(grammar["book_representation"]["sentence_standings"])
    kinds = set(grammar["book_representation"]["sentence_kinds"])

    for chapter in projection:
        assert [sentence.sentence_number for sentence in chapter.sentences] == list(
            range(1, len(chapter.sentences) + 1)
        )
        assert {sentence.standing for sentence in chapter.sentences} <= admitted
        assert {sentence.kind for sentence in chapter.sentences} <= kinds
        assert all(sentence.text for sentence in chapter.sentences)


def test_sentence_standing_follows_the_machine_rules():
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))
    rules = grammar["book_representation"]["standing_rules"]

    for chapter in project_book(CHAPTERS):
        for sentence in chapter.sentences:
            if rules["unresolved_text"] in sentence.text:
                expected = rules["unresolved_standing"]
            else:
                expected = rules["sections"].get(
                    sentence.section, rules["default"]
                )
            assert sentence.standing == expected


def test_chapter_reordering_changes_the_machine_comparison(tmp_path):
    copied = tmp_path / "chapters"
    copied.mkdir()
    paths = sorted(CHAPTERS.glob("*.md"))
    for path in paths:
        target = copied / path.name
        target.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")
    first = copied / paths[0].name
    second = copied / paths[1].name
    first_material = first.read_text(encoding="utf-8")
    second_material = second.read_text(encoding="utf-8")
    first.write_text(second_material, encoding="utf-8")
    second.write_text(first_material, encoding="utf-8")

    assert machine_book_coordinates(copied) != machine_book_coordinates(CHAPTERS)


def test_sentence_reordering_changes_the_machine_comparison(tmp_path):
    copied = tmp_path / "chapters"
    copied.mkdir()
    for path in CHAPTERS.glob("*.md"):
        (copied / path.name).write_text(
            path.read_text(encoding="utf-8"), encoding="utf-8"
        )
    first = copied / "01-source-coordinates-and-grammar.md"
    material = first.read_text(encoding="utf-8")
    left = (
        "A supplied representation may become Seed-addressable without becoming "
        "Evidence, applicable input, adopted law, truth, or native grammar."
    )
    right = (
        "Equal content under another source or occurrence does not establish "
        "equal identity or Standing."
    )
    assert f"{left} {right}" in material
    first.write_text(
        material.replace(f"{left} {right}", f"{right} {left}", 1),
        encoding="utf-8",
    )

    actual = machine_book_coordinates(copied)
    expected = machine_book_coordinates(CHAPTERS)
    assert actual[0]["sentence_count"] == expected[0]["sentence_count"]
    assert actual[0]["ordered_sentence_digest"] != expected[0][
        "ordered_sentence_digest"
    ]


def test_missing_chapter_position_is_refused(tmp_path):
    copied = tmp_path / "chapters"
    copied.mkdir()
    for path in CHAPTERS.glob("*.md"):
        if not path.name.startswith("02-"):
            (copied / path.name).write_text(
                path.read_text(encoding="utf-8"), encoding="utf-8"
            )

    with pytest.raises(BookProjectionError, match="chapter order must be contiguous"):
        project_book(copied)
