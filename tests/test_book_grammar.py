import json
from pathlib import Path


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
