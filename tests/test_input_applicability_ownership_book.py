import json
from pathlib import Path


GRAMMAR = Path(__file__).resolve().parents[1] / "book_of_seed/grammar.json"


def _clause() -> dict:
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))
    return grammar["clauses"]["01.Standing.E.1"]


def test_applicability_binds_input_to_one_exact_act():
    clause = _clause()

    assert clause["subject"] == "input_to_exact_Act_relation"
    assert clause["responsibility"] == {
        "default": "exact_Act_Responsibility",
        "override": "explicitly_assigned_responsible_occurrence",
    }
    assert set(clause["must_precede"]) == {
        "participation",
        "consumption",
        "reliance",
    }
    assert {"input_identity", "exact_Act", "Scope", "locality", "Authority"} <= set(
        clause["coordinates"]
    )


def test_applicability_has_four_standings_and_preserves_exclusion():
    clause = _clause()

    assert clause["standings"] == [
        "applicable",
        "inapplicable",
        "conflicting",
        "Unknown",
    ]
    assert clause["excluded_input"] == {
        "may_participate": False,
        "may_support_result": False,
        "establishes_Act_nonoccurrence": False,
        "establishes_Act_prohibition": False,
    }


def test_composite_occurrence_keeps_results_distinct_and_recoverable():
    clause = _clause()

    assert set(clause["same_occurrence_may_establish"]) == {
        "Applicability",
        "Act_occurrence_or_nonoccurrence",
        "output_Standing",
    }
    assert clause["independently_recoverable"] is True
    assert ["Applicability", "Act_occurrence"] in clause["distinct_from"]
    assert ["Act_occurrence", "output_Standing"] in clause["distinct_from"]
    assert ["output_Standing", "downstream_Applicability"] in clause["distinct_from"]


def test_persistent_standing_does_not_create_an_act():
    clause = _clause()

    assert clause["persistent_Standing"] == {
        "requires_later_consumption": False,
        "establishes_new_Act": False,
    }
