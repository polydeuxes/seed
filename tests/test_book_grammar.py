"""Exact Book and Witness coordinates."""

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
        "carried_coordinates",
    }
    assert {word for word in retired if word in material} == set()


def test_machine_grammar_addresses_current_coordinates_without_retired_objects():
    grammar = _grammar()

    assert set(grammar) == {"book_coordinates"}
    assert grammar["book_coordinates"]["01.Current.G"] == {
        "subject": "this_Seed",
        "when": "no_exact_coordinate_is_established_for_this_Seed",
        "current_coordinates": [],
    }

def test_no_current_coordinates_exist_without_one_established_coordinate():
    active_book = _active_book()
    assert active_book.count(
        "When no exact coordinate is established for this Seed, no current\n"
        "coordinates are established for this Seed."
    ) == 2
    assert "S0" not in active_book


def test_applicability_remains_separate_from_the_governed_act():
    grammar = _grammar()
    boundary = grammar["book_coordinates"]["01.Current.E.1"]
    assert boundary["subject"] == "subject_to_Act_binding"
    assert boundary["Applicability"] == {
        "exact_Act": "Applicability",
        "Act_occurrence": {
            "subject": "subject_to_Act_binding",
            "addressed_Act": "exact_Act",
            "Locality": "06.Locality.A.Locality",
        },
        "result": {
            "Act_occurrence": "Applicability_Act_occurrence",
            "Applicability": ["applicable", "inapplicable"],
        },
    }
    current = (CHAPTERS / "01_current_coordinates.md").read_text(encoding="utf-8")
    assert "exact coordinates of that Applicability Act occurrence" in current
    assert "exact coordinates of one Applicability result occurrence" in current

    for reference in ("04.Compare.A", "04.Compare.B"):
        compare = grammar["book_coordinates"][reference]
        assert compare["Applicability"] == "Applicability_result"
        assert compare["Yield"] == "02.Acts.A.Yield"

def test_compare_clause_addresses_its_exact_subjects_and_act():
    compare = _grammar()["book_coordinates"]["04.Compare"]

    assert compare["subject"] == "exact_Compare_subjects"
    assert compare["exact_Act"] == "Compare"
    assert "its exact\nsubjects, exact Compare Act, and Locality" in (
        CHAPTERS / "08_compare.md"
    ).read_text(encoding="utf-8")


def test_addressed_position_coordinates_preserve_the_bounded_subjects():
    measurement = _grammar()["book_coordinates"]["01.Source.D.2"]
    chapter = (
        CHAPTERS / "07_measurement.md"
    ).read_text(encoding="utf-8")

    assert measurement["current_coordinates"] == (
        "exact_byte_pair_position_Measurement_result"
    )
    assert measurement["subjects"] == (
        "exhaustive_bounded_source_byte_position_references"
    )
    assert "The bounded subjects are exhaustive." in chapter


def test_declared_measurement_does_not_infer_yield_from_its_result():
    measurement = _grammar()["book_coordinates"]["01.Source.D"]
    assert measurement["coordinates"] == [
        "exact_material_result",
        "Locality",
    ]
    assert "Yield" not in measurement
    acts = (
        CHAPTERS / "03_acts_and_occurrences.md"
    ).read_text(encoding="utf-8")
    assert (
        "One Act occurrence and one result occurrence have no Yield relation"
        in acts
    )


def test_positional_coordinates_name_their_exact_basis():
    coordinates = _grammar()["book_coordinates"]

    assert coordinates["01.Current.A.1"]["occurrence_order"] == (
        "result_occurrence_is_boundary_or_before_boundary_in_same_"
        "Locality_occurrence_order"
    )
    assert coordinates["01.Current.D.2"]["current_coordinates"] == (
        "exact_subject_through_exact_occurrence_boundary"
    )
    assert "occurrence_order" not in coordinates["01.Current.D.2"]
    assert coordinates["04.Compare.A"]["occurrence_order"] == [
        "earlier_result_occurrence_before_later_result_occurrence_in_same_Locality",
        "later_ordered_source_occurrence_references_are_earlier_ordered_source_"
        "occurrence_references_and_one_added_exact_occurrence",
    ]
    assert coordinates["06.Locality.B"]["prior_through_boundary"] == (
        "exact_earlier_boundary_in_same_Locality_occurrence_order"
    )


def test_source_and_destination_coordinates_establish_no_occurrence_order():
    movement = _grammar()["book_coordinates"]["03.Movement.A"]
    chapter = (CHAPTERS / "10_movement.md").read_text(encoding="utf-8")

    assert movement["coordinates"] == [
        "exact_subject",
        "source_coordinates",
        "destination_coordinates",
        "Locality",
    ]
    assert (
        "Source and destination coordinates\n"
        "establish no earlier or later occurrence order."
    ) in chapter


def test_machine_grammar_has_no_generic_result_boundary():
    material = GRAMMAR.read_text(encoding="utf-8")

    assert "result_boundary" not in material


def test_subject_to_act_binding_is_direct_clause_coordinates():
    act = _grammar()["book_coordinates"]["02.Acts.A"]

    assert act["subject"] == "exact_subject"
    assert act["exact_Act"] == "exact_Act"
    assert act["Locality"] == "06.Locality.A.Locality"
    assert act["result"] == "exact_result"
    assert act["Yield"]["relation"] == "yield"


def test_exact_relations_are_direct():
    grammar = _grammar()
    expected = {
        "yield": (
            grammar["book_coordinates"]["02.Acts.A"]["Yield"],
            "exact_Act_occurrence",
            "exact_result",
            "02.Acts.A.Yield",
        ),
        "locality": (
            grammar["book_coordinates"]["06.Locality.A"]["Locality"],
            "exact_subject",
            "exact_subject",
            "06.Locality.A.Locality",
        ),
    }
    for relation, (coordinates, first, second, address) in expected.items():
        assert coordinates["first_subject"] == first
        assert coordinates["relation"] == relation
        assert coordinates["second_subject"] == second
        assert coordinates["relation_occurrence"] == "relation_occurrence"
        clause, coordinate = address.rsplit(".", 1)
        assert grammar["book_coordinates"][clause][coordinate] == coordinates


def test_yield_has_no_interposed_node():
    yield_relation = _grammar()["book_coordinates"]["02.Acts.A"]["Yield"]
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
        "05.Recording.C",
        "07.Emission.C",
        "07.Emission.D",
        "01.Current.G",
        "01.Current.A",
        "01.Current.A.1",
        "01.Current.D",
        "01.Current.D.1",
        "01.Current.D.2",
        "01.Current.E.1",
    }

    for reference, body in coordinates.items():
        assert "subject" in body or "subjects" in body, reference


def test_declared_relation_references_resolve():
    grammar = _grammar()
    coordinates = grammar["book_coordinates"]
    exact = {
        "Yield": "02.Acts.A.Yield",
        "Locality": "06.Locality.A.Locality",
    }
    unresolved = {
        reference: (name, value)
        for reference, body in coordinates.items()
        for name, value in body.items()
        if name in exact and type(value) is str and value != exact[name]
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


def test_result_positions_address_exact_source_occurrences_directly():
    assert _grammar()["book_coordinates"]["01.Current.D.1"] == {
        "subject": "exact_addressed_result_content",
        "coordinates": [
            "recorded_result_occurrence",
            "result_position",
            "source_occurrence_references",
            "Locality",
        ],
    }


def test_sources_and_emission_preserve_exact_boundaries_without_loss_staging():
    coordinates = _grammar()["book_coordinates"]

    assert coordinates["01.Source.H"]["coordinates"] == [
        "source_boundary",
        "source_occurrence_references",
        "Locality",
    ]
    assert coordinates["07.Emission.A"]["coordinates"] == [
        "exact_destination_boundary",
        "Locality",
    ]

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
