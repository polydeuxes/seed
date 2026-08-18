import json
from pathlib import Path
import re


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
        "standing_not_established": [
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
            "same_result_content_identifies_one_result"
        ]
        is False
    )


def _assert_recorded_occurrence_kind_families(grammar):
    allowed = {
        (),
        ("event_occurrence",),
        ("Assertion_occurrence",),
    }
    for clause in grammar["clauses"].values():
        kinds = clause["recorded_occurrence_kind"]
        assert type(kinds) is list
        assert tuple(kinds) in allowed
        assert ("responsibility" in clause) == bool(kinds)


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
    assert_refused("01.Source.A", [])
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
    roots = {
        coordinates["reference"]: coordinates
        for coordinates in grammar["root_references"]
    }
    assert all(
        coordinates["first_subject"] == "this"
        and coordinates["relation"] == "identifies"
        and coordinates["second_subject"]
        for coordinates in roots.values()
    )

    unresolved = []

    def visit(value, path=(), parent=None):
        if isinstance(value, dict):
            for key, nested in value.items():
                visit(nested, (*path, key), value)
        elif isinstance(value, list):
            for position, nested in enumerate(value):
                visit(nested, (*path, position), value)
        elif (
            isinstance(value, str)
            and value.startswith("this_")
            and value not in roots
        ):
            if not (
                isinstance(parent, dict)
                and value in {parent.get("identity"), parent.get("subject")}
                and parent.get("first_subject") in roots
                and parent.get("relation")
                and parent.get("second_subject")
            ):
                unresolved.append((path, value))

    visit(grammar)
    assert unresolved == []


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
            "first_subject": "this",
            "relation": "identifies",
            "second_subject": "Witness",
        },
        {
            "reference": "this_book_material_acquisition_witness",
            "coordinate": "book_material_acquisition_witness_subject",
            "first_subject": "this",
            "relation": "identifies",
            "second_subject": "book_material_acquisition_witness",
        },
        {
            "reference": "this_Grammar",
            "coordinate": "witness_grammar",
            "first_subject": "this",
            "relation": "identifies",
            "second_subject": "Grammar",
        },
        {
            "reference": "this_Book",
            "coordinate": "book_material",
            "first_subject": "this",
            "relation": "identifies",
            "second_subject": "Book",
        },
        {
            "reference": "this_Seed",
            "coordinate": "seed_subject",
            "first_subject": "this",
            "relation": "identifies",
            "second_subject": "Seed",
        },
        {
            "reference": "this_Rosetta",
            "coordinate": "rosetta_reference",
            "first_subject": "this",
            "relation": "identifies",
            "second_subject": "Rosetta",
        },
        {
            "reference": "this_Fidelity",
            "coordinate": "bounded_Fidelity_finding",
            "first_subject": "this",
            "relation": "identifies",
            "second_subject": "Fidelity",
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
        "identifies_book": False,
    }


def test_clauses_without_recorded_occurrence_kind_remain_absent_in_book_order():
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))
    declarations = tuple(
        (identity, clause["recorded_occurrence_kind"])
        for identity, clause in grammar["clauses"].items()
        if clause["recorded_occurrence_kind"] == []
    )

    assert declarations == (
        ("01.Source.B", []),
        ("01.Source.C", []),
        ("01.Source.D.1", []),
        ("01.Source.F", []),
        ("01.Standing.A", []),
        ("01.Standing.B", []),
        ("01.Standing.C", []),
        ("01.Standing.D", []),
        ("01.Standing.D.2", []),
        ("01.Standing.F", []),
        ("05.Recording.A", []),
        ("05.Recording.C", []),
        ("05.Source.A", []),
        ("08.Authority.A", []),
        ("08.Authority.B", []),
        ("08.Authority.C", []),
    )
    assert all(
        "responsibility" not in grammar["clauses"][identity]
        for identity, _recorded_occurrence_kind in declarations
    )


def test_supporting_finding_standing_not_established_participation_by_identity():
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))
    clause = grammar["clauses"]["08.Authority.B"]

    assert clause["supporting_findings"] == [
        "established_support_relation",
        "Applicability",
        "Admission",
    ]
    assert clause["standing_not_established"][0] == (
        "Participation_relation_by_supporting_finding_identity"
    )


def test_public_export_standing_not_established_standing():
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))

    assert grammar["clauses"]["01.Standing.C"]["standing_not_established"][-1] == (
        "Standing_by_public_export"
    )


def test_applicability_requires_more_than_usefulness_agreement_or_availability():
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))
    clause = grammar["clauses"]["01.Standing.E.1"]

    assert clause["standing_not_established"] == [
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
    identities = tuple(
        coordinate["identity"] if type(coordinate) is dict else coordinate
        for coordinate in required_coordinates
    )
    return all(
        (
            crossing[coordinate]["occurrence"]
            if type(crossing[coordinate]) is dict
            else crossing[coordinate]
        )
        != "unestablished"
        for coordinate in identities
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
        {
            "identity": "Evidence_of_Yield_relation",
            "first_subject": "Evidence",
            "relation": "of",
            "second_subject": "Yield_relation",
        },
        "result_occurrence",
        "Standing",
        "downstream_Act",
    ]
    complete_subjects = set()
    incomplete_subjects = set()
    required_identities = tuple(
        coordinate["identity"] if type(coordinate) is dict else coordinate
        for coordinate in required
    )
    for crossing in completeness["required_crossings"]:
        assert tuple(crossing) == ("subject", *required_identities)
        assert crossing["grammar"] == "established"
        assert crossing["grammar_reference"] in grammar["clauses"]
        target = (
            complete_subjects
            if _crossing_is_complete(required, crossing)
            else incomplete_subjects
        )
        target.add(crossing["subject"])
    assert complete_subjects == {
        "candidate",
        "emission_candidate_Admission_to_operator_Locality",
        "emission_input_Applicability",
    }
    assert incomplete_subjects == {
        "Admission",
    }


def test_generic_admission_grammar_precedes_each_concrete_lifecycle():
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
    assert admission["Evidence_of_Yield_relation"] == {
        "first_subject": "Evidence",
        "relation": "of",
        "second_subject": "Yield_relation",
        "occurrence": "unestablished",
    }
    assert admission["result_occurrence"] == "unestablished"
    assert admission["Standing"] == "unestablished"

    concrete = next(
        crossing
        for crossing in completeness["required_crossings"]
        if crossing["subject"]
        == "emission_candidate_Admission_to_operator_Locality"
    )
    assert concrete["responsible_boundary"] == "this_Seed"
    assert concrete["Act_Evidence"] == "Admission_Act_Evidence"
    assert concrete["Evidence_of_Yield_relation"] == {
        "first_subject": "Evidence",
        "relation": "of",
        "second_subject": "Yield_relation",
        "occurrence": "Admission_Evidence_of_Yield_relation",
    }
    assert concrete["result_occurrence"] == "Admission_result_occurrence"
    assert concrete["Standing"] == "Admission_Standing"


FIDELITY_SUBJECTS = {
    "standing_responsibility_path": (
        test_witness_readable_grammar_traverses_responsibility_from_standing,
    ),
    "public_export_standing_distinction": (
        test_public_export_standing_not_established_standing,
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
        test_supporting_finding_standing_not_established_participation_by_identity,
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
        test_generic_admission_grammar_precedes_each_concrete_lifecycle,
    ),
    "clause_grammar_recorded_occurrence_kind_distinction": (
        test_clauses_without_recorded_occurrence_kind_remain_absent_in_book_order,
    ),
    "witness_clause_book_material_reference": (
        test_witness_clauses_address_their_exact_book_material,
    ),
    "book_witness_clause_identity_distinction": (
        test_book_and_witness_grammar_have_the_same_clauses,
    ),
}
