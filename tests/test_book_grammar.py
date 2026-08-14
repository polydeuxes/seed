import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GRAMMAR = ROOT / "book_of_seed/grammar.json"
BOOK = ROOT / "book_of_seed/chapters/02-constitutional-standing.md"


def test_machine_readable_grammar_uses_responsibility_spine():
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))

    assert grammar["version"] == 2
    assert grammar["spine"] == "Responsibility"
    assert grammar["implementation_witness"]["discriminators"] == [
        "content",
        "carriage",
        "digest",
    ]
    assert grammar["clauses"]
    for clause_id, clause in grammar["clauses"].items():
        assert clause["subject"]
        assert clause["responsibility"]
        assert f"### {clause_id}" in BOOK.read_text(encoding="utf-8")
