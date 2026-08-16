import json
from pathlib import Path
import re

import pytest


ROOT = Path(__file__).resolve().parents[1]
GRAMMAR = ROOT / "book_of_seed/grammar.json"
CHAPTERS = ROOT / "book_of_seed/chapters"


def _active_book() -> str:
    return "\n".join(
        path.read_text(encoding="utf-8") for path in sorted(CHAPTERS.glob("*.md"))
    )


def _book_clause_identities() -> set[bytes]:
    return {
        identity
        for path in sorted(CHAPTERS.glob("*.md"))
        for identity in re.findall(
            rb"^### ([0-9]+\.[A-Za-z]+\.[A-Za-z0-9.]+) ",
            path.read_bytes(),
            re.M,
        )
    }


def _machine_clause_identities() -> set[bytes]:
    return set(
        re.findall(
            rb'^    "([0-9]+\.[A-Za-z]+\.[A-Za-z0-9.]+)": \{$',
            GRAMMAR.read_bytes(),
            re.M,
        )
    )


def _assert_relation_clauses(grammar: dict, active_book: str) -> None:
    for relation, coordinates in grammar["relations"].items():
        clause = coordinates["book_clause"]
        assert relation
        assert active_book.count(f"### {clause} ") == 1


def _machine_strings(value, path=()):
    if isinstance(value, dict):
        for key, nested in value.items():
            yield from _machine_strings(nested, (*path, key))
    elif isinstance(value, list):
        for position, nested in enumerate(value):
            yield from _machine_strings(nested, (*path, position))
    elif isinstance(value, str):
        yield path, value


@pytest.mark.subject("standing_responsibility_path")
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
            "branch_value_by_completion_without_responsible_occurrence_and_Evidence",
        ],
    }


@pytest.mark.subject("content_locality_occurrence_distinction")
def test_machine_witness_discriminates_content_locality_and_occurrence():
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))

    assert grammar["witness"]["discriminators"] == [
        "content",
        "locality",
        "occurrence",
    ]


@pytest.mark.subject("yield_relation_identity")
def test_machine_yield_relation_preserves_occurrence_and_result_identity():
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))

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


@pytest.mark.subject("machine_clause_witness_responsibility")
def test_machine_clauses_name_one_book_witness_or_responsibility():
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))

    assert grammar["clauses"]
    active_book = _active_book()
    for clause_identity, clause in grammar["clauses"].items():
        assert clause["subject"]
        assert ("responsibility" in clause) or (
            clause["witness"]
            in {"deterministic_tests", "unestablished"}
        )
        assert active_book.count(f"### {clause_identity} ") == 1


@pytest.mark.subject("relation_book_clause_reference")
def test_machine_relations_name_one_book_clause():
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))

    _assert_relation_clauses(grammar, _active_book())


@pytest.mark.subject("this_machine_root_reference")
def test_this_occurs_only_as_exact_machine_roots():
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))
    uses = [
        (path, value)
        for path, value in _machine_strings(grammar)
        if "this" in value.lower().split("_")
    ]

    assert uses == [
        (("book_material_reference",), "this_Book"),
        (("root_references", 0, "reference"), "this_Witness"),
        (
            ("root_references", 1, "reference"),
            "this_book_material_acquisition_witness",
        ),
        (("root_references", 2, "reference"), "this_Grammar"),
        (("root_references", 3, "reference"), "this_Book"),
        (("root_references", 4, "reference"), "this_Seed"),
        (("root_references", 5, "reference"), "this_Rosetta"),
        (("root_references", 6, "reference"), "this_Fidelity"),
        (("machine_grammar", "subject"), "this_Grammar"),
        (("machine_grammar", "book_material_reference"), "this_Book"),
        (
            ("machine_grammar", "represented_relation", "first_subject"),
            "this_Grammar",
        ),
        (
            ("machine_grammar", "represented_relation", "second_subject"),
            "this_Book",
        ),
        (("clauses", "01.Source.C", "subject"), "this_Fidelity"),
        (
            ("clauses", "01.Source.C", "comparison", "first_subject"),
            "this_Witness",
        ),
        (
            ("clauses", "01.Source.C", "comparison", "second_subject"),
            "this_Grammar",
        ),
        (
            ("clauses", "01.Source.C", "comparison", "addressed_subject"),
            "this_Seed",
        ),
        (
            ("clauses", "01.Source.C", "comparison", "result"),
            "this_Fidelity",
        ),
        (
            (
                "clauses",
                "01.Source.C",
                "test_subject_relation",
                "second_subject",
            ),
            "this_Fidelity",
        ),
        (
            (
                "clauses",
                "01.Source.C",
                "test_subject_relation",
                "first_subject_distinct_from",
            ),
            "this_Witness",
        ),
        (
            ("clauses", "01.Source.C", "test_subjects", 0, "subject"),
            "this_book_material_acquisition_witness",
        ),
        (
            (
                "clauses",
                "01.Source.C",
                "test_subjects",
                0,
                "material_reference",
            ),
            "this_Book",
        ),
        (("clauses", "01.Source.C", "comparison_order", 0), "this_Witness"),
        (("clauses", "01.Source.C", "comparison_order", 2), "this_Grammar"),
        (("clauses", "01.Source.C", "comparison_order", 3), "this_Fidelity"),
        (("clauses", "01.Source.C", "representation_order", 0), "this_Fidelity"),
        (
            ("clauses", "06.Locality.B", "subject"),
            "this_Seed_bears_Standing_Locality_continuation_Responsibility",
        ),
    ]


@pytest.mark.subject("relation_book_clause_reference")
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


@pytest.mark.subject("book_machine_clause_identity_equality")
def test_book_and_machine_grammar_have_the_same_clauses():
    assert _book_clause_identities() == _machine_clause_identities()


@pytest.mark.subject("machine_clause_book_material_reference")
def test_machine_clauses_address_their_exact_book_material():
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))

    assert grammar["book_material_reference"] == "this_Book"
    assert tuple(
        (identity, clause["book_material_reference"])
        for identity, clause in grammar["clauses"].items()
    ) == tuple((identity, identity) for identity in grammar["clauses"])


@pytest.mark.subject("machine_root_reference_order")
def test_machine_root_references_remain_distinct_and_in_declared_order():
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))

    assert grammar["root_references"] == [
        {
            "reference": "this_Witness",
            "coordinate": "witness",
        },
        {
            "reference": "this_book_material_acquisition_witness",
            "coordinate": "book_material_acquisition_witness_subject",
        },
        {"reference": "this_Grammar", "coordinate": "machine_grammar"},
        {"reference": "this_Book", "coordinate": "book_material"},
        {"reference": "this_Seed", "coordinate": "seed_subject"},
        {"reference": "this_Rosetta", "coordinate": "rosetta_reference"},
        {
            "reference": "this_Fidelity",
            "coordinate": "bounded_Fidelity_finding",
        },
    ]


@pytest.mark.subject("machine_grammar_represents_book")
def test_machine_grammar_represents_the_book_without_identity_equality():
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))

    assert grammar["machine_grammar"] == {
        "subject": "this_Grammar",
        "book_material_reference": "this_Book",
        "represented_relation": {
            "first_subject": "this_Grammar",
            "relation": "represents",
            "second_subject": "this_Book",
        },
        "equal_identity": False,
    }


@pytest.mark.subject("unestablished_clause_witness_order")
def test_clauses_without_event_species_name_their_witness_in_book_order():
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))
    declarations = tuple(
        (identity, clause["witness"])
        for identity, clause in grammar["clauses"].items()
        if "witness" in clause
    )

    assert declarations == (
        ("01.Source.B", "unestablished"),
        ("01.Source.C", "unestablished"),
        ("01.Source.D.1", "unestablished"),
        ("01.Source.E", "unestablished"),
        ("01.Source.F", "unestablished"),
        ("01.Standing.A", "unestablished"),
        ("01.Standing.B", "unestablished"),
        ("01.Standing.C", "unestablished"),
        ("01.Standing.D", "unestablished"),
        ("01.Standing.D.2", "unestablished"),
        ("01.Standing.E", "unestablished"),
        ("01.Standing.F", "unestablished"),
        ("05.Recording.A", "unestablished"),
        ("05.Recording.B", "unestablished"),
        ("05.Recording.C", "unestablished"),
        ("05.Source.A", "unestablished"),
        ("08.Authority.A", "unestablished"),
        ("08.Authority.B", "unestablished"),
        ("08.Authority.C", "unestablished"),
    )
    assert all(
        "responsibility" not in grammar["clauses"][identity]
        for identity, _witness in declarations
    )


@pytest.mark.subject("supporting_finding_participation_distinction")
def test_supporting_finding_does_not_establish_participation_by_identity():
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))
    clause = grammar["clauses"]["08.Authority.B"]

    assert clause["supporting_findings"] == [
        "established_support_relation",
        "Applicability",
        "Admission",
    ]
    assert clause["does_not_establish"][0] == (
        "Participation_relation_by_supporting_finding_identity"
    )


@pytest.mark.subject("public_export_standing_distinction")
def test_public_export_does_not_establish_standing():
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))

    assert grammar["clauses"]["01.Standing.C"]["does_not_establish"][-1] == (
        "Standing_by_public_export"
    )


@pytest.mark.subject("applicability_usefulness_agreement_availability_distinction")
def test_applicability_requires_more_than_usefulness_agreement_or_availability():
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))
    clause = grammar["clauses"]["01.Standing.E.1"]

    assert clause["does_not_establish"] == [
        "Applicability_by_usefulness",
        "Applicability_by_agreement",
        "Applicability_by_availability",
    ]


@pytest.mark.subject("applicability_responsibility")
def test_applicability_responsibility_is_exact_act_or_assigned_occurrence():
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))

    assert grammar["clauses"]["01.Standing.E.1"]["responsibility"] == {
        "default": "exact_Act_Responsibility",
        "override": "assigned_responsible_occurrence",
    }
