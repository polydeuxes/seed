import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GRAMMAR = ROOT / "book_of_seed/grammar.json"
CHAPTERS = ROOT / "book_of_seed/chapters"


def _active_book() -> str:
    return "\n".join(
        path.read_text(encoding="utf-8") for path in sorted(CHAPTERS.glob("*.md"))
    )


def _assert_relation_clauses(grammar: dict, active_book: str) -> None:
    for relation, coordinates in grammar["relations"].items():
        clause = coordinates["book_clause"]
        assert relation
        assert active_book.count(f"### {clause} ") == 1


def test_machine_readable_grammar_traverses_responsibility_from_standing():
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))

    assert grammar["standing"] == {
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
    ]
    assert grammar["relations"]["yield"]["preserves"] == [
        "Act_occurrence_identity",
        "result_identity",
    ]
    assert (
        grammar["relations"]["yield"][
            "equal_result_content_establishes_identity"
        ]
        is False
    )
    assert grammar["clauses"]
    active_book = _active_book()
    _assert_relation_clauses(grammar, active_book)
    assert active_book.count(f"### {grammar['fidelity']['book_clause']} ") == 1
    for clause_identity, clause in grammar["clauses"].items():
        assert clause["subject"]
        assert clause["responsibility"]
        assert active_book.count(f"### {clause_identity} ") == 1


def test_missing_relation_clause_is_detected():
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))
    active_book = _active_book()
    locality_clause = grammar["relations"]["locality"]["book_clause"]
    broken_book = active_book.replace(
        f"### {locality_clause} ", "### 01.Missing.A ", 1
    )

    try:
        _assert_relation_clauses(grammar, broken_book)
    except AssertionError:
        pass
    else:
        raise AssertionError("missing Locality clause escaped the grammar audit")


def test_ingest_occurrence_and_yield_identity_remain_distinct():
    chapter = (CHAPTERS / "14-representation-emission-and-locality.md").read_text(
        encoding="utf-8"
    )

    assert (
        "Each Ingest occurrence has one distinct result identity."
        in chapter
    )
    assert (
        "Equal material content does not identify either occurrence, result, or "
        "Yield relation."
        in chapter
    )
