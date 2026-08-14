import json
from pathlib import Path


GRAMMAR = Path(__file__).resolve().parents[1] / "book_of_seed/grammar.json"


def _clause() -> dict:
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))
    return grammar["clauses"]["01.Standing.D.1"]


def test_assertion_fidelity_responsibility_has_exact_coordinates():
    clause = _clause()

    assert clause["subject"] == "Assertion"
    assert clause["identity"] == ["asserted_content"]
    assert clause["responsibility"] == {
        "kind": "fidelity",
        "addressed": "Standing",
        "coordinates": [
            "Evidence",
            "provenance",
            "Scope",
            "Authority",
            "conflicts",
            "limits",
            "Unknowns",
            "Standing",
        ],
    }
    assert set(clause["distinct_from"]) == {
        "establishing_Act",
        "establishing_occurrence",
        "recording_occurrence",
    }


def test_assertion_fidelity_does_not_manufacture_movement():
    clause = _clause()

    assert set(clause["does_not_establish"]) == {
        "another_Act",
        "Standing_revision",
        "Stop",
    }
    assert clause["identity_change"] == {
        "when": "asserted_content_changes",
        "result": "different_Assertion",
    }
    assert clause["Unknown"]["requires_elimination"] is False
