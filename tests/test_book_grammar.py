"""Exact active Book and Witness Grammar structure."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / "book_of_seed"
GRAMMAR = BOOK / "witness_grammar.json"
CHAPTERS = BOOK / "chapters"


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
            r"^### ([0-9]+\.[A-Za-z]+\.[A-Za-z0-9.]+) ",
            _active_book(),
            re.MULTILINE,
        )
    )


def test_book_and_witness_grammar_have_the_same_coordinates():
    assert set(_grammar()["book_coordinates"]) == _book_coordinates()


def test_witness_grammar_has_no_retired_scaffolding():
    material = GRAMMAR.read_text(encoding="utf-8").lower()
    retired = {
        "act_evidence",
        "evidence_of_yield",
        "intact_evidence",
        "unestablished",
        "responsibility_assignment",
        "represented_relation",
        "represents",
        "bears",
        "carried_by",
    }
    assert {word for word in retired if word in material} == set()


def test_current_standing_precedes_responsibility_without_assignment():
    assert _grammar()["standing"] == {
        "current": {
            "subject": "this_Seed",
            "coordinates": [],
        },
        "path": [
            "Standing",
            "Responsibility",
            "exact_Act",
            "Act_occurrence",
            "result",
        ],
        "later_Standing": {
            "requires": [
                "Responsibility",
                "exact_Act",
                "Act_occurrence",
                "Yield_relation",
                "result",
            ]
        },
    }


def test_empty_standing_is_only_the_first_current_standing():
    active_book = _active_book()
    assert active_book.count(
        "This Seed first current Standing carries no coordinates."
    ) == 2
    assert "S0" not in active_book
    assert "This Seed current Standing carries no coordinates." not in active_book


def test_applicability_required_admission_and_participation_remain_separate():
    grammar = _grammar()
    boundary = grammar["book_coordinates"]["01.Standing.E.1"]
    assert boundary["Applicability"] == {
        "Responsibility": "Applicability",
        "exact_Act": "Applicability",
        "result": "Applicability_result",
    }
    assert boundary["Admission"] == {
        "boundary": "required_Admission_boundary",
        "Responsibility": "Admission",
        "exact_Act": "Admission",
        "occurrence": "exact_Admission_occurrence",
    }
    assert boundary["Participation"] == {
        "relation": "participation",
        "occurrence": "exact_participation_relation_occurrence",
    }

    for reference in ("04.Compare.A", "04.Compare.B"):
        compare = grammar["book_coordinates"][reference]
        assert compare["input"] == [
            "Applicability_result",
            "participation_relation_occurrence",
        ]
        assert "Admission" not in compare
        assert "required_Admission" not in compare
        assert compare["relations"] == ["participation", "yield"]

    candidate_compare = grammar["book_coordinates"]["04.Compare.C"]
    assert candidate_compare["input"] == [
        "Applicability_result",
        "exact_Admission_occurrence",
        "participation_relation_occurrence",
    ]
    assert candidate_compare["Participation"] == {
        "subject": "Candidate",
        "role": "Candidate",
    }


def test_candidate_compare_uses_candidate_as_subject_and_sources_as_coordinates():
    candidate_compare = _grammar()["book_coordinates"]["04.Compare.C"]

    assert candidate_compare == {
        "subject": "Candidate",
        "Responsibility": "compare_Candidate_coordinates",
        "responsibility_source": (
            "current_Standing_carrying_exact_Candidate_result"
        ),
        "exact_Act": "Compare",
        "rule": "compare_first_and_second_source_Assertion_coordinates",
        "carried_coordinates": [
            "first_source_Assertion_reference",
            "second_source_Assertion_reference",
            "first_source_role",
            "second_source_role",
        ],
        "subject_boundary": "exact_Candidate_result",
        "input": [
            "Applicability_result",
            "exact_Admission_occurrence",
            "participation_relation_occurrence",
        ],
        "Participation": {
            "subject": "Candidate",
            "role": "Candidate",
        },
        "relations": ["participation", "yield"],
        "result": "Candidate_coordinate_Compare_result",
    }
    assert candidate_compare["subject"] not in candidate_compare[
        "carried_coordinates"
    ]
    assert candidate_compare["Participation"]["subject"] == candidate_compare[
        "subject"
    ]


def test_candidate_production_owns_completeness_without_a_result_barrier():
    grammar = _grammar()
    candidate = grammar["book_coordinates"]["01.Source.E.1"]
    standing = grammar["book_coordinates"]["01.Standing.D"]

    assert candidate == {
        "subject": "required_source_Assertion_or_ordered_source_Assertion_pair",
        "Responsibility": "exhaustive_Candidate_for_bounded_subject_set",
        "exact_Act": "Candidate",
        "input": [
            "Applicability_result",
            "participation_relation_occurrence",
        ],
        "required_Admission": (
            "exact_Admission_occurrence_prior_to_Participation"
        ),
        "completeness_boundary": "Responsibility_bounded_subject_set",
        "relations": ["participation", "yield"],
        "result_boundary": "Candidate_Act_occurrence_Yield_exact_Candidate_result",
        "later_Standing": "requires_no_bounded_subject_set_completion",
        "result": "exact_Candidate_result",
    }
    assert standing["responsibility_subject_set"] == (
        "exhaustive_bounded_subject_set"
    )
    assert standing["establishes_no"] == [
        "order_for_another_Responsibility",
        "Applicability_for_another_Responsibility",
        "completion_for_another_Responsibility",
    ]

    candidate_book = (
        CHAPTERS / "07_measurement_and_candidates.md"
    ).read_text(encoding="utf-8")
    standing_book = (
        CHAPTERS / "01_constitutional_standing.md"
    ).read_text(encoding="utf-8")
    compare_book = (CHAPTERS / "08_compare.md").read_text(encoding="utf-8")
    assert (
        "Each Responsibility is exhaustive for its bounded\n"
        "subject set."
    ) in candidate_book
    assert (
        "A Candidate result\n"
        "requires no completion of other required subjects under that Responsibility\n"
        "for later Standing."
    ) in candidate_book
    assert (
        "An exhaustive bounded subject set for one Responsibility establishes no order,\n"
        "Applicability, or completion for another Responsibility."
    ) in standing_book
    assert "one complete Candidate result" not in compare_book
    assert "every Candidate in the complete Candidate result" not in compare_book


def test_candidate_compare_book_refuses_source_participation_and_relation_promotion():
    compare = (CHAPTERS / "08_compare.md").read_text(encoding="utf-8")

    assert (
        "A source Assertion reference is no other Compare subject."
    ) in compare
    assert (
        "Candidate Participation, source references, shared coordinates, or a Compare\n"
        "result establishes no source Assertion relation and no later Standing."
    ) in compare


def test_responsibility_coordinates_are_anatomy_not_assignment():
    assert _grammar()["responsibility"] == {
        "subject": "Responsibility",
        "book_material_reference": "this_Book",
        "coordinates": [
            "responsible_boundary",
            "subject",
            "exact_Act",
            "Authority",
            "Scope",
            "Locality",
            "limits",
            "source",
            "provenance",
            "support_relations",
        ],
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
            "01.Standing.E.1",
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
            "08.Authority.A",
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


def test_witness_grammar_relation_population_is_empty():
    assert _grammar()["witness_grammar"] == {
        "subject": "this_Grammar",
        "book_material_reference": "this_Book",
        "relations": [],
    }


def test_each_book_coordinate_has_exact_responsibility_and_act():
    coordinates_by_reference = {
        reference: coordinates
        for reference, coordinates in _grammar()["book_coordinates"].items()
        if reference != "01.Standing.E.1"
    }
    incomplete = {
        reference: sorted(
            {"subject", "Responsibility", "exact_Act"} - set(coordinates)
        )
        for reference, coordinates in coordinates_by_reference.items()
        if {"subject", "Responsibility", "exact_Act"} - set(coordinates)
    }
    assert incomplete == {}


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
    references = _grammar()["source_references"]
    assert len(references) == len(
        {(reference["reference"], reference["coordinate"]) for reference in references}
    )
    assert {
        ("this_Book", "book_material"),
        ("this_Grammar", "grammar"),
        ("this_Seed", "seed_subject"),
        ("this_Witness", "witness"),
    } <= {
        (reference["reference"], reference["coordinate"])
        for reference in references
    }


def test_fidelity_preserves_the_book_material_witness_subject():
    assert _grammar()["book_coordinates"]["01.Source.C"] == {
        "subject": "Fidelity",
        "Responsibility": "compare_this_Seed_occurrence_with_this_Grammar",
        "exact_Act": "Compare",
        "test_subject": "this_book_material_acquisition_witness",
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


FIDELITY_SUBJECTS = {
    "active_book_witness_coordinate_population": (
        test_book_and_witness_grammar_have_the_same_coordinates,
    ),
    "retired_witness_scaffolding_refusal": (
        test_witness_grammar_has_no_retired_scaffolding,
    ),
    "standing_responsibility_direct_position": (
        test_current_standing_precedes_responsibility_without_assignment,
    ),
    "initial_empty_standing_boundary": (
        test_empty_standing_is_only_the_first_current_standing,
    ),
    "applicability_admission_participation_separation": (
        test_applicability_required_admission_and_participation_remain_separate,
    ),
    "candidate_compare_subject_coordinate_distinction": (
        test_candidate_compare_uses_candidate_as_subject_and_sources_as_coordinates,
        test_candidate_compare_book_refuses_source_participation_and_relation_promotion,
    ),
    "responsibility_exhaustion_without_completion_barrier": (
        test_candidate_production_owns_completeness_without_a_result_barrier,
    ),
    "responsibility_exact_anatomy": (
        test_responsibility_coordinates_are_anatomy_not_assignment,
    ),
    "direct_exact_relation_population": (test_exact_relations_are_direct,),
    "direct_yield_relation": (test_yield_has_no_interposed_node,),
    "witness_grammar_empty_relation_population": (
        test_witness_grammar_relation_population_is_empty,
    ),
    "book_coordinate_responsibility_act_completeness": (
        test_each_book_coordinate_has_exact_responsibility_and_act,
    ),
    "book_coordinate_relation_resolution": (
        test_declared_relation_references_resolve,
    ),
    "source_reference_exact_population": (test_source_references_are_exact_and_distinct,),
    "fidelity_book_material_witness_subject": (
        test_fidelity_preserves_the_book_material_witness_subject,
    ),
    "machine_grammar_host_boolean_refusal": (
        test_machine_grammar_contains_no_host_boolean,
    ),
}
