import json
from pathlib import Path
import re

import pytest

from scripts.fill_witness_grammar import (
    fill_fidelity_occurrence_kinds,
    fill_witness_grammar,
)


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


def _witness_clause_identities() -> set[bytes]:
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


def _witness_strings(value, path=()):
    if isinstance(value, dict):
        for key, nested in value.items():
            yield from _witness_strings(nested, (*path, key))
    elif isinstance(value, list):
        for position, nested in enumerate(value):
            yield from _witness_strings(nested, (*path, position))
    elif isinstance(value, str):
        yield path, value


def test_witness_readable_grammar_traverses_responsibility_from_standing():
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


def test_witness_discriminates_content_locality_and_occurrence():
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))

    assert grammar["witness"]["discriminators"] == [
        "content",
        "locality",
        "occurrence",
    ]


def test_witness_yield_relation_preserves_occurrence_and_result_identity():
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


def _assert_recorded_occurrence_kind_families(grammar):
    allowed = {
        ("event_occurrence",),
        ("Assertion_occurrence",),
        ("Fidelity_occurrence",),
    }
    for clause in grammar["clauses"].values():
        kinds = clause["recorded_occurrence_kind"]
        assert type(kinds) is list
        assert tuple(kinds) in allowed
        assert ("responsibility" in clause) == (
            kinds != ["Fidelity_occurrence"]
        )


def test_witness_clauses_separate_recovered_grammar_from_recorded_occurrence_kind():
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))

    assert grammar["clauses"]
    active_book = _active_book()
    for clause_identity, clause in grammar["clauses"].items():
        assert clause["subject"]
        assert clause["grammar"] == "established"
        assert not (
            clause.get("witness") == "unestablished"
        )
        assert active_book.count(f"### {clause_identity} ") == 1
    _assert_recorded_occurrence_kind_families(grammar)


def test_recorded_occurrence_kind_families_refuse_wrong_shape_or_crossing():
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))

    def assert_refused(identity, value, *, remove_responsibility=False):
        changed = json.loads(json.dumps(grammar))
        changed["clauses"][identity]["recorded_occurrence_kind"] = value
        if remove_responsibility:
            changed["clauses"][identity].pop("responsibility", None)
        try:
            _assert_recorded_occurrence_kind_families(changed)
        except (AssertionError, TypeError):
            return
        raise AssertionError("wrong recorded-occurrence kind family escaped")

    assert_refused("01.Source.B", None)
    assert_refused("01.Source.B", "event_occurrence")
    assert_refused("01.Source.B", ["event_occurrence", "Assertion_occurrence"])
    assert_refused("01.Source.B", ["unknown_occurrence"])
    assert_refused("01.Source.B", [])
    assert_refused("01.Source.A", ["Fidelity_occurrence"])
    assert_refused(
        "01.Source.A",
        ["event_occurrence"],
        remove_responsibility=True,
    )


def test_witness_relations_name_one_book_clause():
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))

    _assert_relation_clauses(grammar, _active_book())


def test_this_occurs_only_as_exact_witness_roots():
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))
    uses = [
        (path, value)
        for path, value in _witness_strings(grammar)
        if "this" in value.lower().split("_")
    ]

    roots = {
        coordinates["reference"] for coordinates in grammar["root_references"]
    }
    this_seed_responsibility = (
        "this_Seed_bears_Standing_Locality_continuation_Responsibility"
    )
    assert all(
        value in roots or value == this_seed_responsibility
        for _, value in uses
    )
    root_uses = [
        (path, value)
        for path, value in uses
        if path[0] in {"book_material_reference", "root_references", "witness_grammar"}
    ]
    assert root_uses == [
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
        (("witness_grammar", "subject"), "this_Grammar"),
        (("witness_grammar", "book_material_reference"), "this_Book"),
        (
            ("witness_grammar", "represented_relation", "first_subject"),
            "this_Grammar",
        ),
        (
            ("witness_grammar", "represented_relation", "second_subject"),
            "this_Book",
        ),
    ]
    assert (
        ("clauses", "06.Locality.B", "subject"),
        this_seed_responsibility,
    ) in uses
    assert (
        ("clauses", "01.Source.C", "test_subjects", 0, "subject"),
        "event_standing_grammar_responsibility",
    ) not in uses


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


def test_book_and_witness_grammar_have_the_same_clauses():
    assert _book_clause_identities() == _witness_clause_identities()


def test_witness_clauses_address_their_exact_book_material():
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))

    assert grammar["book_material_reference"] == "this_Book"
    assert tuple(
        (identity, clause["book_material_reference"])
        for identity, clause in grammar["clauses"].items()
    ) == tuple((identity, identity) for identity in grammar["clauses"])


def test_witness_root_references_remain_distinct_and_in_declared_order():
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
        {"reference": "this_Grammar", "coordinate": "witness_grammar"},
        {"reference": "this_Book", "coordinate": "book_material"},
        {"reference": "this_Seed", "coordinate": "seed_subject"},
        {"reference": "this_Rosetta", "coordinate": "rosetta_reference"},
        {
            "reference": "this_Fidelity",
            "coordinate": "bounded_Fidelity_finding",
        },
    ]


def test_witness_grammar_represents_the_book_without_identity_equality():
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))

    assert grammar["witness_grammar"] == {
        "subject": "this_Grammar",
        "book_material_reference": "this_Book",
        "represented_relation": {
            "first_subject": "this_Grammar",
            "relation": "represents",
            "second_subject": "this_Book",
        },
        "equal_identity": False,
    }


FIDELITY_ONLY_CLAUSE_IDENTITIES = (
    "01.Source.B",
    "01.Source.C",
    "01.Source.D.1",
    "01.Source.E",
    "01.Source.F",
    "01.Standing.A",
    "01.Standing.B",
    "01.Standing.C",
    "01.Standing.D",
    "01.Standing.D.2",
    "01.Standing.E",
    "01.Standing.F",
    "05.Recording.A",
    "05.Recording.B",
    "05.Recording.C",
    "05.Source.A",
    "08.Authority.A",
    "08.Authority.B",
    "08.Authority.C",
)


@pytest.mark.parametrize(
    "clause_identity",
    FIDELITY_ONLY_CLAUSE_IDENTITIES,
    ids=FIDELITY_ONLY_CLAUSE_IDENTITIES,
)
def test_fidelity_only_clause_has_exact_book_grammar_and_fidelity_occurrence(
    clause_identity,
):
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))
    clause = grammar["clauses"][clause_identity]

    assert clause["book_material_reference"] == clause_identity
    assert clause["grammar"] == "established"
    assert clause["recorded_occurrence_kind"] == ["Fidelity_occurrence"]
    assert "responsibility" not in clause
    assert _active_book().count(f"### {clause_identity} ") == 1


def test_fidelity_occurrence_kind_filler_is_exact_and_idempotent():
    current = GRAMMAR.read_bytes()
    unchanged, missing = fill_witness_grammar(current)
    assert unchanged == current
    assert missing == ()

    one_blank = current.replace(
        b'      "recorded_occurrence_kind": ["Fidelity_occurrence"],',
        b'      "recorded_occurrence_kind": [],',
        1,
    )
    filled_occurrences, missing = fill_fidelity_occurrence_kinds(one_blank)
    filled, remaining = fill_witness_grammar(one_blank)
    assert filled_occurrences == current
    assert filled == current
    assert missing == (FIDELITY_ONLY_CLAUSE_IDENTITIES[0],)
    assert remaining == missing


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


def test_public_export_does_not_establish_standing():
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))

    assert grammar["clauses"]["01.Standing.C"]["does_not_establish"][-1] == (
        "Standing_by_public_export"
    )


def test_applicability_requires_more_than_usefulness_agreement_or_availability():
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))
    clause = grammar["clauses"]["01.Standing.E.1"]

    assert clause["does_not_establish"] == [
        "Applicability_by_usefulness",
        "Applicability_by_agreement",
        "Applicability_by_availability",
    ]


def test_applicability_responsibility_is_exact_act_or_assigned_occurrence():
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))

    assert grammar["clauses"]["01.Standing.E.1"]["responsibility"] == {
        "default": "exact_Act_Responsibility",
        "override": "assigned_responsible_occurrence",
    }


def _crossing_is_complete(required_coordinates, crossing):
    return all(
        crossing[coordinate] != "unestablished"
        for coordinate in required_coordinates
    )


def test_witness_completeness_separates_grammar_from_live_crossing():
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))
    completeness = grammar["completeness"]
    required = completeness["required_coordinates"]

    assert required == [
        "grammar",
        "grammar_reference",
        "responsible_boundary",
        "responsibility_assignment",
        "Act_Evidence",
        "Evidence_of_Yield_relation",
        "result_occurrence",
        "Standing",
        "downstream_Act",
    ]
    for crossing in completeness["required_crossings"]:
        assert tuple(crossing) == ("subject", *required)
        assert crossing["grammar"] == "established"
        assert crossing["grammar_reference"] in grammar["clauses"]
        assert not _crossing_is_complete(required, crossing)


def test_emission_admission_grammar_is_established_before_its_lifecycle():
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))
    completeness = grammar["completeness"]
    admission = next(
        crossing
        for crossing in completeness["required_crossings"]
        if crossing["subject"] == "Admission"
    )

    assert admission["grammar"] == "established"
    assert admission["grammar_reference"] == "01.Standing.E"
    assert admission["responsible_boundary"] == (
        "Representation_emission_Responsibility"
    )
    assert admission["responsibility_assignment"] == "this_Book"
    assert admission["downstream_Act"] == "Representation_emission_Act"
    assert admission["Act_Evidence"] == "unestablished"
    assert admission["Evidence_of_Yield_relation"] == "unestablished"
    assert admission["result_occurrence"] == "unestablished"
    assert admission["Standing"] == "unestablished"


FIDELITY_SUBJECTS = {
    "standing_responsibility_path": (
        test_witness_readable_grammar_traverses_responsibility_from_standing,
    ),
    "public_export_standing_distinction": (
        test_public_export_does_not_establish_standing,
    ),
    "applicability_responsibility": (
        test_applicability_responsibility_is_exact_act_or_assigned_occurrence,
    ),
    "witness_clause_grammar_recorded_occurrence_kind": (
        test_witness_clauses_separate_recovered_grammar_from_recorded_occurrence_kind,
        test_recorded_occurrence_kind_families_refuse_wrong_shape_or_crossing,
    ),
    "yield_relation_identity": (
        test_witness_yield_relation_preserves_occurrence_and_result_identity,
    ),
    "relation_book_clause_reference": (
        test_witness_relations_name_one_book_clause,
        test_missing_relation_clause_is_detected,
    ),
    "supporting_finding_participation_distinction": (
        test_supporting_finding_does_not_establish_participation_by_identity,
    ),
    "applicability_usefulness_agreement_availability_distinction": (
        test_applicability_requires_more_than_usefulness_agreement_or_availability,
    ),
    "content_locality_occurrence_distinction": (
        test_witness_discriminates_content_locality_and_occurrence,
    ),
    "witness_root_reference": (test_this_occurs_only_as_exact_witness_roots,),
    "witness_root_reference_order": (
        test_witness_root_references_remain_distinct_and_in_declared_order,
    ),
    "witness_grammar_represents_book": (
        test_witness_grammar_represents_the_book_without_identity_equality,
    ),
    "witness_grammar_completeness": (
        test_witness_completeness_separates_grammar_from_live_crossing,
        test_emission_admission_grammar_is_established_before_its_lifecycle,
    ),
    "clause_grammar_recorded_occurrence_kind_distinction": (
        test_fidelity_only_clause_has_exact_book_grammar_and_fidelity_occurrence,
        test_fidelity_occurrence_kind_filler_is_exact_and_idempotent,
    ),
    "witness_clause_book_material_reference": (
        test_witness_clauses_address_their_exact_book_material,
    ),
    "book_witness_clause_identity_equality": (
        test_book_and_witness_grammar_have_the_same_clauses,
    ),
}
