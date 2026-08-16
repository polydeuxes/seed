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
        ],
    }
    assert grammar["implementation_witness"]["discriminators"] == [
        "content",
        "locality",
        "occurrence",
    ]
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
    assert grammar["clauses"]
    active_book = _active_book()
    _assert_relation_clauses(grammar, active_book)
    for clause_identity, clause in grammar["clauses"].items():
        assert clause["subject"]
        assert ("responsibility" in clause) or (
            clause["implementation_witness"]
            in {"deterministic_tests", "unestablished"}
        )
        assert active_book.count(f"### {clause_identity} ") == 1


def test_this_occurs_only_as_exact_machine_roots():
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))
    uses = [
        (path, value)
        for path, value in _machine_strings(grammar)
        if "this" in value.lower().split("_")
    ]

    assert uses == [
        (("book_material_reference",), "this_Book"),
        (("clauses", "01.Source.C", "subject"), "this_Seed"),
        (
            ("clauses", "06.Locality.B", "subject"),
            "this_Seed_bears_Standing_Locality_continuation_Responsibility",
        ),
    ]


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


def test_book_and_machine_grammar_have_the_same_clauses():
    assert _book_clause_identities() == _machine_clause_identities()


def test_machine_clauses_address_their_exact_book_material():
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))

    assert grammar["book_material_reference"] == "this_Book"
    assert tuple(
        (identity, clause["book_material_reference"])
        for identity, clause in grammar["clauses"].items()
    ) == tuple((identity, identity) for identity in grammar["clauses"])


def test_clauses_without_event_species_name_their_witness_in_book_order():
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))
    declarations = tuple(
        (identity, clause["implementation_witness"])
        for identity, clause in grammar["clauses"].items()
        if "implementation_witness" in clause
    )

    assert declarations == (
        ("01.Source.B", "unestablished"),
        ("01.Source.C", "deterministic_tests"),
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
