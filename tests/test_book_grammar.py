import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
GRAMMAR = ROOT / "book_of_seed/witness_grammar.json"
CHAPTERS = ROOT / "book_of_seed/chapters"
BOOK_README = ROOT / "book_of_seed/README.md"
BOOK_ADMISSION = ROOT / "book_of_seed/book_admission.txt"


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


RESPONSIBILITY_COORDINATES = (
    (
        "Required branches",
        (
            ("Responsible boundary", "responsible_boundary"),
            ("Subject or material addressed", "subject_or_material_addressed"),
            ("Exact responsible act", "exact_responsible_act"),
            ("Authority", "authority"),
            ("Evidence", "evidence"),
            ("Scope and locality", "scope_and_locality"),
        ),
    ),
    (
        "Input branches",
        (
            ("Input source", "input_source"),
            ("Provenance", "provenance"),
        ),
    ),
    (
        "Support-relation branches",
        (("Support relation", "support_relation"),),
    ),
    (
        "Act-occurrence and non-occurrence branches",
        (
            ("Act occurrence", "act_occurrence"),
            (
                "Absence-of-act-occurrence finding",
                "absence_of_act_occurrence_finding",
            ),
            (
                "Occurrence or non-occurrence evidence",
                "occurrence_or_nonoccurrence_evidence",
            ),
        ),
    ),
    (
        "Result branches",
        (
            ("Occurrence-result Evidence", "occurrence_result_evidence"),
            ("Result", "result"),
        ),
    ),
    (
        "Standing branches",
        (
            ("Standing responsible boundary", "standing_responsible_boundary"),
            ("Standing occurrence", "standing_occurrence"),
            ("Standing-occurrence evidence", "standing_occurrence_evidence"),
            ("Standing", "standing"),
        ),
    ),
    (
        "Preservation, standing, and neighboring branches",
        (
            ("Preservation record", "preservation_record"),
            (
                "Separate Authorization standing",
                "separate_authorization_standing",
            ),
            (
                "Applicability and admission standing",
                "applicability_and_admission_standing",
            ),
            ("Lawful Stopping", "lawful_stopping"),
        ),
    ),
)


def _book_responsibility_heading_tree():
    groups = []
    current = None
    inside = False
    for line in BOOK_README.read_text(encoding="utf-8").splitlines():
        if line == "## Responsibility":
            assert not inside
            inside = True
            continue
        if inside and line.startswith("## "):
            break
        if not inside:
            continue
        if line.startswith("### "):
            current = [line[4:], []]
            groups.append(current)
        elif line.startswith("#### "):
            assert current is not None
            current[1].append(line[5:])
    assert inside
    return tuple((group, tuple(coordinates)) for group, coordinates in groups)


def test_book_responsibility_and_witness_grammar_share_exact_coordinates():
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))
    responsibility = grammar["responsibility"]
    expected_headings = tuple(
        (group, tuple(subject for subject, _ in coordinates))
        for group, coordinates in RESPONSIBILITY_COORDINATES
    )
    grammar_coordinates = tuple(
        (
            group["subject"],
            tuple(
                (coordinate["subject"], coordinate["coordinate"])
                for coordinate in group["coordinates"]
            ),
        )
        for group in responsibility["coordinates"]
    )

    assert responsibility["book_material_reference"] == "this_Book"
    assert responsibility["subject"] == "Responsibility"
    assert _book_responsibility_heading_tree() == expected_headings
    assert grammar_coordinates == RESPONSIBILITY_COORDINATES
    coordinates = [
        coordinate
        for _, group_coordinates in grammar_coordinates
        for _, coordinate in group_coordinates
    ]
    assert len(coordinates) == len(set(coordinates))


def _book_admission_words():
    words = []
    for line in BOOK_ADMISSION.read_text(encoding="utf-8").splitlines():
        material = line.strip()
        if not material or material.startswith("#"):
            continue
        assert " " not in material
        words.append(material)
    assert len(words) == len(set(words))
    return tuple(words)


def _resolve_grammar_coordinate(grammar, reference):
    coordinate = grammar
    for exact_key in reference:
        assert type(exact_key) is str
        assert type(coordinate) is dict
        assert exact_key in coordinate
        coordinate = coordinate[exact_key]
    return coordinate


def _assert_word_coordinates_resolve(grammar):
    for word, coordinates in grammar["words"].items():
        assert set(coordinates) == {"coordinates"}
        assert word in _book_admission_words()
        exact_coordinates = coordinates["coordinates"]
        assert type(exact_coordinates) is list
        assert exact_coordinates
        coordinate_pairs = []
        for exact_coordinate in exact_coordinates:
            assert set(exact_coordinate) == {
                "grammar_coordinate_reference",
                "relation_coordinate_reference",
            }
            coordinate_pair = tuple(
                tuple(exact_coordinate[coordinate])
                for coordinate in (
                    "grammar_coordinate_reference",
                    "relation_coordinate_reference",
                )
            )
            for reference in coordinate_pair:
                assert _resolve_grammar_coordinate(grammar, reference)
            coordinate_pairs.append(coordinate_pair)
        assert len(set(coordinate_pairs)) == len(coordinate_pairs)


def _positive_relation_coordinates(material, path=(), standing_not_established=False):
    if isinstance(material, dict):
        if isinstance(material.get("relation"), str) and not standing_not_established:
            yield material["relation"], path
        for coordinate, nested in material.items():
            yield from _positive_relation_coordinates(
                nested,
                (*path, coordinate),
                standing_not_established
                or coordinate == "standing_not_established",
            )
    elif isinstance(material, list):
        for position, nested in enumerate(material):
            yield from _positive_relation_coordinates(
                nested,
                (*path, position),
                standing_not_established,
            )


def test_declared_book_word_source_and_relation_coordinates_resolve():
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))

    assert grammar["words"] == {
        "of": {
            "coordinates": [
                {
                    "grammar_coordinate_reference": ["composite"],
                    "relation_coordinate_reference": [
                        "composite",
                        "relations",
                        "of",
                    ],
                }
            ]
        },
        "participation": {
            "coordinates": [
                {
                    "grammar_coordinate_reference": [
                        "clause_coordinates",
                        "01.Standing.E.1",
                    ],
                    "relation_coordinate_reference": ["relations", "participation"],
                }
            ]
        },
        "yield": {
            "coordinates": [
                {
                    "grammar_coordinate_reference": [
                        "clause_coordinates",
                        "02.Acts.A",
                    ],
                    "relation_coordinate_reference": ["relations", "yield"],
                }
            ]
        },
        "locality": {
            "coordinates": [
                {
                    "grammar_coordinate_reference": [
                        "clause_coordinates",
                        "06.Locality.A",
                    ],
                    "relation_coordinate_reference": ["relations", "locality"],
                }
            ]
        },
        "bears": {
            "coordinates": [
                {
                    "grammar_coordinate_reference": [
                        "clause_coordinates",
                        "01.Standing.D.2",
                    ],
                    "relation_coordinate_reference": [
                        "clause_coordinates",
                        "01.Standing.D.2",
                        "Applicability_considered_with_respect_to",
                    ],
                },
                {
                    "grammar_coordinate_reference": [
                        "clause_coordinates",
                        "06.Locality.B",
                    ],
                    "relation_coordinate_reference": [
                        "clause_coordinates",
                        "06.Locality.B",
                        "subject",
                    ],
                },
            ]
        },
        "comparison": {
            "coordinates": [
                {
                    "grammar_coordinate_reference": [
                        "clause_coordinates",
                        "01.Source.C",
                    ],
                    "relation_coordinate_reference": [
                        "clause_coordinates",
                        "01.Source.C",
                        "comparison",
                    ],
                }
            ]
        },
        "represents": {
            "coordinates": [
                {
                    "grammar_coordinate_reference": ["witness_grammar"],
                    "relation_coordinate_reference": [
                        "witness_grammar",
                        "represented_relation",
                    ],
                }
            ]
        },
        "carries": {
            "coordinates": [
                {
                    "grammar_coordinate_reference": [
                        "clause_coordinates",
                        "01.Source.D",
                    ],
                    "relation_coordinate_reference": [
                        "clause_coordinates",
                        "01.Source.D",
                        "result_carries",
                    ],
                },
                {
                    "grammar_coordinate_reference": [
                        "clause_coordinates",
                        "01.Standing.E.1",
                    ],
                    "relation_coordinate_reference": [
                        "clause_coordinates",
                        "01.Standing.E.1",
                        "Assertion_coordinates",
                    ],
                },
                {
                    "grammar_coordinate_reference": [
                        "clause_coordinates",
                        "04.Compare.B",
                    ],
                    "relation_coordinate_reference": [
                        "clause_coordinates",
                        "04.Compare.B",
                        "comparison_rule",
                    ],
                },
            ]
        },
        "supports": {
            "coordinates": [
                {
                    "grammar_coordinate_reference": [
                        "clause_coordinates",
                        "06.Locality.D",
                    ],
                    "relation_coordinate_reference": [
                        "clause_coordinates",
                        "06.Locality.D",
                        "authority",
                    ],
                }
            ]
        },
    }
    _assert_word_coordinates_resolve(grammar)


def test_book_word_coordinate_siren_refuses_a_missing_source_or_relation():
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))
    for coordinate in (
        "grammar_coordinate_reference",
        "relation_coordinate_reference",
    ):
        changed = json.loads(json.dumps(grammar))
        changed["words"]["of"]["coordinates"][0][coordinate] = [
            "missing_coordinate"
        ]
        try:
            _assert_word_coordinates_resolve(changed)
        except AssertionError:
            continue
        raise AssertionError(f"missing {coordinate} escaped")


def test_every_admitted_book_word_has_explicit_source_and_relation_coordinates():
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))
    admitted = set(_book_admission_words())
    declared = set(grammar["words"])

    unexpected = sorted(declared - admitted)
    missing = sorted(admitted - declared)
    assert unexpected == []
    assert missing == [], (
        "\nBook words without explicit Witness Grammar source and relation "
        "coordinates:\n  " + "\n  ".join(missing)
    )


def test_every_exact_positive_relation_occurrence_has_a_declared_coordinate_pair():
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))
    declared_relation_coordinates = {
        word: {
            tuple(exact_coordinate["relation_coordinate_reference"])
            for exact_coordinate in coordinates["coordinates"]
        }
        for word, coordinates in grammar["words"].items()
    }
    missing = [
        (word, path)
        for word, path in _positive_relation_coordinates(grammar)
        if word in declared_relation_coordinates
        and path not in declared_relation_coordinates[word]
    ]

    assert missing == [], (
        "\nExact positive Witness Grammar relation occurrences without a "
        "declared word coordinate pair:\n  "
        + "\n  ".join(
            f"{word}: " + " -> ".join(str(coordinate) for coordinate in path)
            for word, path in missing
        )
    )


def test_witness_discriminates_content_locality_and_occurrence():
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))

    assert grammar["witness"]["distinctions"] == [
        "content",
        "locality",
        "occurrence",
    ]
    assert grammar["witness"]["distinct_from"] == [
        ["content", "locality"],
        ["content", "occurrence"],
        ["locality", "occurrence"],
    ]


def test_source_measurement_declarations_require_one_current_standing_pin():
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))
    source = grammar["clause_coordinates"]["01.Source.D"]
    seed_subject = next(
        reference["reference"]
        for reference in grammar["source_references"]
        if reference["coordinate"] == "seed_subject"
    )

    assert source["responsibility"]["responsible_boundary"] == seed_subject
    assert source["standing_emission_declarations"] == [
        {
            "order": 0,
            "book_clause": "01.Source.D",
            "measurement": {
                "identity": (
                    "measurement_of_position_coordinates_of_byte_pair_occurrences"
                ),
                "first_subject": "position_coordinates",
                "relation": "of",
                "second_subject": "byte_pair_occurrences",
            },
            "subject": "exact_Ingest_result",
            "requires": ["current_Standing", "exact_subject"],
            "standing_not_established": [
                "Responsibility_assignment_by_subject_presence",
                "Applicability_by_subject_presence",
                "Act_by_subject_presence",
            ],
        },
        {
            "order": 1,
            "book_clause": "01.Source.D",
            "measurement": {
                "identity": "measurement_of_exact_byte_occurrences",
                "first_subject": "exact_byte_occurrences",
                "relation": "of",
                "second_subject": "exact_Ingest_source_set",
            },
            "subject": "exact_Ingest_source_set",
            "requires": ["current_Standing", "exact_subject"],
            "standing_not_established": [
                "Responsibility_assignment_by_subject_presence",
                "Applicability_by_subject_presence",
                "Act_by_subject_presence",
            ],
        },
    ]
    assert (
        "Recording one declared Responsibility assignment in declared order "
        "requires one exact current Standing boundary"
    ) in _active_book()


def test_witness_yield_relation_preserves_occurrence_and_result_coordinates():
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))

    assert grammar["relations"]["yield"]["preserves"] == [
        "Act_occurrence_identity",
        "result_identity",
    ]
    assert "standing_not_established" not in grammar["relations"]["yield"]


def _assert_recorded_occurrence_kind_families(grammar):
    allowed = {
        (),
        ("event_occurrence",),
        ("Assertion_occurrence",),
    }
    for clause in grammar["clause_coordinates"].values():
        kinds = clause["recorded_occurrence_kind"]
        assert type(kinds) is list
        assert tuple(kinds) in allowed
        assert ("responsibility" in clause) == bool(kinds)


def test_witness_clauses_separate_recovered_grammar_from_recorded_occurrence_kind():
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))

    assert grammar["clause_coordinates"]
    active_book = _active_book()
    for clause_identity, clause in grammar["clause_coordinates"].items():
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
        changed["clause_coordinates"][identity]["recorded_occurrence_kind"] = value
        if remove_responsibility:
            changed["clause_coordinates"][identity].pop("responsibility", None)
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


def test_this_occurs_only_as_exact_witness_sources():
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))
    sources = {
        coordinates["reference"]: coordinates
        for coordinates in grammar["source_references"]
    }
    assert all(
        set(coordinates) == {"reference", "coordinate"}
        and coordinates["coordinate"]
        for coordinates in sources.values()
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
            and value not in sources
        ):
            if not (
                isinstance(parent, dict)
                and value in {parent.get("identity"), parent.get("subject")}
                and parent.get("first_subject") in sources
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
        for identity, clause in grammar["clause_coordinates"].items()
    ) == tuple((identity, identity) for identity in grammar["clause_coordinates"])


def test_witness_source_references_remain_distinct_and_in_declared_order():
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))

    assert grammar["source_references"] == [
        {
            "reference": "this_Witness",
            "coordinate": "witness",
        },
        {
            "reference": "this_book_material_acquisition_witness",
            "coordinate": "book_material_acquisition_witness_subject",
        },
        {
            "reference": "this_Grammar",
            "coordinate": "witness_grammar",
        },
        {
            "reference": "this_Book",
            "coordinate": "book_material",
        },
        {
            "reference": "this_Seed",
            "coordinate": "seed_subject",
        },
        {
            "reference": "this_separate_admission_material",
            "coordinate": "separate_admission_material_reference",
        },
        {
            "reference": "this_Fidelity",
            "coordinate": "bounded_Fidelity_finding",
        },
    ]


def test_witness_grammar_represents_the_book_from_its_exact_reference():
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))

    assert grammar["witness_grammar"] == {
        "subject": "this_Grammar",
        "book_material_reference": "this_Book",
        "represented_relation": {
            "first_subject": "this_Grammar",
            "relation": "represents",
            "second_subject": "this_Book",
        },
    }
    source_relation = grammar["clause_coordinates"]["01.Source.F"]
    assert source_relation["recorded_occurrence_kind"] == []
    assert source_relation["assertion"] == {
        "first_subject": "X",
        "relation": "exact_relation",
        "second_subject": "Y",
    }


def test_clauses_without_recorded_occurrence_kind_remain_absent_in_book_order():
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))
    declarations = tuple(
        (identity, clause["recorded_occurrence_kind"])
        for identity, clause in grammar["clause_coordinates"].items()
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
        "responsibility" not in grammar["clause_coordinates"][identity]
        for identity, _recorded_occurrence_kind in declarations
    )


def test_supporting_finding_standing_not_established_participation_by_identity():
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))
    clause = grammar["clause_coordinates"]["08.Authority.B"]

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

    assert grammar["clause_coordinates"]["01.Standing.C"]["standing_not_established"][-1] == (
        "Standing_by_public_export"
    )


def test_applicability_requires_more_than_usefulness_agreement_or_availability():
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))
    clause = grammar["clause_coordinates"]["01.Standing.E.1"]

    assert clause["standing_not_established"] == [
        "Applicability_by_usefulness",
        "Applicability_by_agreement",
        "Applicability_by_availability",
    ]
    assert clause["Applicability_findings"] == [
        "applicable",
        "inapplicable",
        "conflicting",
        "Unknown",
    ]
    assert clause["emission_input_Applicability_occurrence"][
        "each_other_Applicability_finding"
    ] == {"requires": "separate_evidenced_determination"}
    assert clause["excluded_input"] == {
        "relation_findings": [
            {
                "first_subject": "excluded_input",
                "relation": "Participation",
                "second_subject": "exact_Act",
                "finding": "excluded",
            },
            {
                "first_subject": "excluded_input",
                "relation": "supports",
                "second_subject": "result",
                "finding": "excluded",
            },
        ],
        "standing_not_established": [
            {
                "first_subject": {
                    "first_subject": "exclusion",
                    "relation": "of",
                    "second_subject": "one_proposed_input",
                },
                "relation": "establishes",
                "second_subject": "Act_nonoccurrence",
                "standing": "not_established",
            },
            {
                "first_subject": {
                    "first_subject": "exclusion",
                    "relation": "of",
                    "second_subject": "one_proposed_input",
                },
                "relation": "establishes",
                "second_subject": "Act_prohibition",
                "standing": "not_established",
            },
        ],
    }
    assert clause["Assertion_coordinates"] == {
        "first_subject": "each_Assertion",
        "relation": "carries",
        "second_subject": "exact_coordinates",
    }
    assert clause["persistent_Standing"] == {
        "standing_not_established": [
            {
                "first_subject": "persistent_Standing",
                "relation": "supplies",
                "second_subject": "another_Act",
                "standing": "not_established",
            }
        ]
    }


def test_later_assertion_meets_current_standing_without_collapsed_boolean_claims():
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))
    clause = grammar["clause_coordinates"]["01.Standing.D.2"]

    assert clause["movement_preserves"] == [
        {
            "first_subject": "responsible_movement_occurrence",
            "relation": "preserves",
            "second_subject": "previously_established_coordinates",
        },
        {
            "first_subject": "responsible_movement_occurrence",
            "relation": "preserves",
            "second_subject": "Unknown",
        },
        {
            "first_subject": "responsible_movement_occurrence",
            "relation": "preserves",
            "second_subject": "exact_subject_coordinate",
        },
    ]

    assert clause["earlier_Assertions"] == {
        "preservation_relations": [
            {
                "first_subject": {
                    "first_subject": "preservation",
                    "relation": "of",
                    "second_subject": "earlier_Assertions",
                },
                "relation": "carries",
                "second_subject": "exact_reference",
            },
            {
                "first_subject": {
                    "first_subject": "preservation",
                    "relation": "of",
                    "second_subject": "earlier_Assertions",
                },
                "relation": "carries",
                "second_subject": "exact_coordinates",
            },
        ],
        "standing_not_established": [
            {
                "first_subject": {
                    "first_subject": "preservation",
                    "relation": "of",
                    "second_subject": "earlier_Assertions",
                },
                "relation": "establishes",
                "second_subject": "separate_Applicability_boundary_for_each_Assertion",
                "standing": "not_established",
            },
            {
                "first_subject": {
                    "first_subject": "preservation",
                    "relation": "of",
                    "second_subject": "earlier_Assertions",
                },
                "relation": "requires",
                "second_subject": {
                    "first_subject": "Compare",
                    "relation": "of",
                    "second_subject": {
                        "first_subject": "later_Assertion",
                        "relation": "with",
                        "second_subject": "each_earlier_Assertion",
                    },
                },
                "standing": "not_established",
            },
        ],
    }
    assert clause["Compare_result"] == {
        "subject_coordinates": [
            "comparison",
            "coordinate_distinction",
            "result_shape",
        ],
        "participation_in_another_Act": "unestablished",
    }


def test_applicability_responsibility_is_exact_act_or_assigned_occurrence():
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))

    assert grammar["clause_coordinates"]["01.Standing.E.1"]["responsibility"] == {
        "default": "exact_Act_Responsibility",
        "assignment": "assigned_responsible_occurrence",
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
        "addressed_Act",
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
        assert crossing["grammar_reference"] in grammar["clause_coordinates"]
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
    assert admission["addressed_Act"] == "Representation_emission_Act"
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


def test_addressed_byte_occurrence_reference_determination_is_constitutional():
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))
    clause = grammar["clause_coordinates"]["01.Source.D.2"]
    chapter = (CHAPTERS / "01_source_coordinates_and_grammar.md").read_text(
        encoding="utf-8"
    )
    material = chapter.split(
        "### 01.Source.D.2 — Addressed byte occurrence reference determination\n\n",
        1,
    )[1].split("\n\n### 01.Source.E", 1)[0]

    assert clause["book_material_reference"] == "01.Source.D.2"
    assert clause["recorded_occurrence_kind"] == ["event_occurrence"]
    assert clause["responsibility"]["responsible_boundary"] == "this_Seed"
    assert clause["occurrence_order"][2:6] == [
        "Applicability_Act_occurrence",
        "Applicability_Act_Evidence",
        {
            "identity": "Applicability_Evidence_of_Yield_relation",
            "first_subject": "Applicability_Evidence",
            "relation": "of",
            "second_subject": "Applicability_Yield_relation",
        },
        "Applicability_result_occurrence",
    ]
    assert clause["occurrence_order"][6:] == [
        "determination_Act_occurrence",
        "determination_Act_Evidence",
        {
            "identity": "determination_Evidence_of_Yield_relation",
            "first_subject": "determination_Evidence",
            "relation": "of",
            "second_subject": "determination_Yield_relation",
        },
        "determination_result_occurrence",
    ]
    assert clause["determination"]["order"] == "source_occurrence_order"
    assert clause["determination"]["lawful_no_reference_result"] == {
        "when": {
            "standing_not_established": [
                {
                    "first_subject": "first_position_coordinate_reference",
                    "relation": "of",
                    "second_subject": "addressed_byte_occurrence",
                },
                {
                    "first_subject": "second_position_coordinate_reference",
                    "relation": "of",
                    "second_subject": "addressed_byte_occurrence",
                },
            ]
        },
        "carried_pair_position_Assertion_references": [],
    }
    assert "every exact pair-occurrence position Assertion reference" in material
    assert "carries no Assertion reference" in material
    assert "carries Unknown for the represented relation" in material
    assert not {"selection", "equality", "math"} & set(material.casefold().split())


FIDELITY_SUBJECTS = {
    "addressed_byte_occurrence_reference_determination": (
        test_addressed_byte_occurrence_reference_determination_is_constitutional,
    ),
    "standing_responsibility_path": (
        test_witness_readable_grammar_traverses_responsibility_from_standing,
        test_source_measurement_declarations_require_one_current_standing_pin,
    ),
    "book_responsibility_witness_grammar_coordinate_distinction": (
        test_book_responsibility_and_witness_grammar_share_exact_coordinates,
    ),
    "book_words_source_relation_coordinates": (
        test_declared_book_word_source_and_relation_coordinates_resolve,
        test_book_word_coordinate_siren_refuses_a_missing_source_or_relation,
        test_every_admitted_book_word_has_explicit_source_and_relation_coordinates,
        test_every_exact_positive_relation_occurrence_has_a_declared_coordinate_pair,
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
        test_witness_yield_relation_preserves_occurrence_and_result_coordinates,
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
    "later_Assertion_current_Standing_boundary": (
        test_later_assertion_meets_current_standing_without_collapsed_boolean_claims,
    ),
    "content_locality_occurrence_distinction": (
        test_witness_discriminates_content_locality_and_occurrence,
    ),
    "witness_source_reference": (
        test_this_occurs_only_as_exact_witness_sources,
    ),
    "witness_source_reference_order": (
        test_witness_source_references_remain_distinct_and_in_declared_order,
    ),
    "witness_grammar_represents_book": (
        test_witness_grammar_represents_the_book_from_its_exact_reference,
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
