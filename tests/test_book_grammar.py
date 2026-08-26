"""Exact active Book and Witness Grammar structure."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / "book_of_seed"
GRAMMAR = BOOK / "witness_grammar.json"
CHAPTERS = BOOK / "chapters"


def _addresses():
    import json

    return json.loads(
        (BOOK / "witness_addresses.json").read_text(encoding="utf-8")
    )["witness_addresses"]


def _grammar() -> dict:
    return json.loads(GRAMMAR.read_text(encoding="utf-8"))


def _active_book() -> str:
    return "\n".join(
        [
            (BOOK / "README.md").read_text(encoding="utf-8"),
            *(
                path.read_text(encoding="utf-8")
                for path in sorted(CHAPTERS.glob("*.md"))
            ),
        ]
    )


def _book_coordinates() -> set[str]:
    return set(
        re.findall(
            r"^### ([0-9]+\.[A-Za-z]+(?:\.[A-Za-z0-9.]+)?) ",
            _active_book(),
            re.MULTILINE,
        )
    )


def test_book_and_witness_grammar_have_the_same_coordinates():
    """Every identified clause has one machine coordinate."""

    assert set(_grammar()["book_coordinates"]) == _book_coordinates()


def test_witness_grammar_has_no_retired_scaffolding():
    material = GRAMMAR.read_text(encoding="utf-8").lower()
    retired = {
        "intact_occurrence",
        "unestablished",
        "responsibility_assignment",
        "represented_relation",
        "represents",
        "bears",
        "carried_by",
    }
    assert {word for word in retired if word in material} == set()


def test_machine_grammar_carries_current_coordinates_without_retired_objects():
    grammar = _grammar()

    assert set(grammar) == {"relations", "book_coordinates"}
    assert grammar["book_coordinates"]["01.Current.G"] == {
        "subject": "this_Seed",
        "current_coordinates": [],
    }

def test_empty_current_coordinates_are_only_the_first_current_coordinates():
    active_book = _active_book()
    assert active_book.count(
        "This Seed first carries no current coordinates."
    ) == 2
    assert "S0" not in active_book


def test_applicability_and_participation_remain_separate():
    grammar = _grammar()
    boundary = grammar["book_coordinates"]["01.Current.E.1"]
    assert boundary["Applicability"] == {
        "exact_Act": "Applicability",
        "result": "Applicability_result",
    }
    assert boundary["Participation"] == {
        "relation": "participation",
        "occurrence": "exact_participation_relation_occurrence",
    }

    for reference in ("04.Compare.A", "04.Compare.B"):
        compare = grammar["book_coordinates"][reference]
        assert compare["requires"] == [
            "Applicability_result",
            "participation_relation_occurrence",
        ]
        assert compare["relations"] == ["participation", "yield"]

def test_generic_compare_carries_its_exact_rule():
    generic_compare = _grammar()["book_coordinates"]["04.Compare"]

    assert generic_compare["rule"] == "exact_Compare_rule"
    assert "its exact subjects, rule, Scope, Locality" in (
        CHAPTERS / "08_compare.md"
    ).read_text(encoding="utf-8")


def test_addressed_position_coordinates_carry_the_bounded_subjects():
    measurement = _grammar()["book_coordinates"]["01.Source.D.2"]
    chapter = (
        CHAPTERS / "07_measurement.md"
    ).read_text(encoding="utf-8")

    assert measurement["requires_current_coordinates"] == (
        "exact_byte_pair_position_Measurement_result"
    )
    assert measurement["subjects"] == (
        "exhaustive_bounded_source_byte_position_references"
    )
    assert "The bounded subjects are exhaustive." in chapter


def test_subject_to_act_binding_is_direct_clause_coordinates():
    act = _grammar()["book_coordinates"]["02.Acts.A"]

    assert act == {
        "subject": "exact_subject",
        "exact_Act": "exact_Act",
        "rule": "exact_rule_where_required",
        "requires": [
            "Scope",
            "Locality",
            "required_relations",
        ],
        "relations": ["participation", "carriage", "yield"],
        "result": "exact_result",
    }


def test_exact_relations_are_direct():
    grammar = _grammar()
    assert set(grammar["relations"]) == {
        "participation",
        "carriage",
        "yield",
        "locality",
        "support",
    }
    expected = {
        "participation": (
            "exact_subject_and_role",
            "exact_Act_occurrence",
            "01.Current.E.1",
        ),
        "carriage": (
            "exact_content",
            "exact_Act_occurrence",
            "02.Acts.A",
        ),
        "yield": (
            "exact_Act_occurrence",
            "exact_result",
            "02.Acts.A",
        ),
        "locality": (
            "exact_subject",
            "exact_subject",
            "06.Locality.A",
        ),
        "support": (
            "exact_subject",
            "exact_input_to_Act_position",
            "08.Support.A",
        ),
    }
    for relation, (first, second, book_reference) in expected.items():
        coordinates = grammar["relations"][relation]
        assert coordinates["first_subject"] == first
        assert coordinates["relation"] == relation
        assert coordinates["second_subject"] == second
        assert coordinates["book_reference"] == book_reference
        assert "relation_occurrence" in coordinates["requires"]
        assert book_reference in grammar["book_coordinates"]


def test_yield_has_no_interposed_node():
    yield_relation = _grammar()["relations"]["yield"]
    assert yield_relation["first_subject"] == "exact_Act_occurrence"
    assert yield_relation["second_subject"] == "exact_result"
    assert yield_relation["relation"] == "yield"


def test_the_grammar_declares_no_block_for_itself():
    """An empty relation list distinguishes nothing from an absent one."""

    assert "witness_grammar" not in _grammar()
    assert any(
        address["subject"] == "this_Grammar"
        for address in _addresses()
    )

def test_only_clauses_naming_an_Act_project_one():
    """A clause that names no Act must not be given one.

    Demanding an exact_Act of every coordinate supplied Act names the Book
    never gave. The exact set is pinned positively instead.
    """

    coordinates = _grammar()["book_coordinates"]
    naming_no_Act = {
        reference
        for reference, body in coordinates.items()
        if "exact_Act" not in body
    }
    assert naming_no_Act == {
        "01.Source.I",
        "05.Recording.A",
        "05.Recording.C",
        "05.Provenance.A",
        "08.Support.A",
        "08.Scope.A",
        "07.Emission.C",
        "07.Emission.D",
        "01.Current.G",
        "01.Current.A",
        "01.Current.A.1",
        "01.Current.D",
        "01.Current.D.1",
        "01.Current.D.2",
        "01.Current.E",
        "01.Current.E.1",
    }

    for reference, body in coordinates.items():
        assert "subject" in body or "subjects" in body, reference


def test_declared_relation_references_resolve():
    grammar = _grammar()
    unresolved = {
        reference: sorted(
            relation
            for relation in coordinates.get("relations", [])
            if relation not in grammar["relations"]
        )
        for reference, coordinates in grammar["book_coordinates"].items()
        if any(
            relation not in grammar["relations"]
            for relation in coordinates.get("relations", [])
        )
    }
    assert unresolved == {}


def test_source_references_are_exact_and_distinct():
    references = _addresses()
    assert len(references) == len(
        {(reference["subject"], reference["coordinate"]) for reference in references}
    )
    assert {
        ("this_Book", "book_material"),
        ("this_Grammar", "grammar"),
        ("this_Seed", "seed_subject"),
        ("this_Witness", "witness"),
    } <= {
        (reference["subject"], reference["coordinate"])
        for reference in references
    }


def test_fidelity_preserves_the_book_material_witness_subject():
    assert _grammar()["book_coordinates"]["01.Source.C"] == {
        "exact_Act": "Compare",
        "subjects": [
            "this_Seed_exact_occurrence",
            "this_Grammar",
            "this_book_material_witness",
        ],
        "carried_coordinates": [
            "exact_declared_distinction",
            "source",
            "provenance",
            "Scope",
            "Locality",
            "conflicts",
            "loss",
            "Unknown",
        ],
    }

def test_machine_grammar_contains_no_host_boolean():
    def contains_boolean(value: object) -> bool:
        if type(value) is bool:
            return True
        if isinstance(value, dict):
            return any(contains_boolean(nested) for nested in value.values())
        if isinstance(value, list):
            return any(contains_boolean(nested) for nested in value)
        return False

    assert not contains_boolean(_grammar())
