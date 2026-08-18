from copy import deepcopy

import pytest

from seed_runtime.candidate_standing_from_exact_result_assertions import (
    BOOK_CLAUSE,
    ONE_SOURCE_CANDIDATE_ACT,
    ONE_SOURCE_CANDIDATE_RESPONSIBILITY,
    ORDERED_PAIR_CANDIDATE_ACT,
    ORDERED_PAIR_CANDIDATE_RESPONSIBILITY,
    boundaries_of_recorded_candidate_standing,
    exact_source_assertion_materials_from_ordered_pair_candidate,
    exact_source_assertion_materials_from_every_ordered_pair_candidate,
    get_recorded_candidate_standing_applicability,
    get_recorded_candidate_standing,
    record_complete_candidate_standing,
    record_complete_ordered_pair_candidate_standing,
    record_one_source_and_ordered_pair_candidate_standings,
    source_assertion_references_for_candidate_standing,
)
from seed_runtime.events import EventLedger, SQLiteEventLedger
from seed_runtime.material_ingest import ingest_material
from seed_runtime.operator_locality_standing import (
    read_operator_locality_standing,
)
from tests.test_operator_locality_standing import _record_byte_measurement


def _source(ledger, *, locality="source", exact_bytes=b"ab"):
    ingest_material(
        ledger,
        locality_identity=locality,
        exact_bytes=exact_bytes,
        source_role="exact supplied material",
        source_boundary="candidate source boundary",
    )
    return _record_byte_measurement(
        ledger,
        source_localities=(locality,),
        recording_locality_identity=locality,
    )


def test_exact_source_assertion_coordinates_expose_every_result_assertion_in_event_order():
    ledger = EventLedger()
    first = _source(ledger, locality="first", exact_bytes=b"ab")
    second = _source(ledger, locality="second", exact_bytes=b"c")
    boundary = ledger.append_boundary()

    references = source_assertion_references_for_candidate_standing(
        ledger, source_append_boundary=boundary
    )

    first_references = tuple(
        reference
        for reference in references
        if reference["recorded_result_occurrence_identity"] == first.identity
    )
    second_references = tuple(
        reference
        for reference in references
        if reference["recorded_result_occurrence_identity"] == second.identity
    )
    assert tuple(reference["assertion_coordinate"] for reference in first_references) == (
        "result",
        "assertions/0",
        "assertions/1",
        "assertions/2",
    )
    assert tuple(reference["assertion_coordinate"] for reference in second_references) == (
        "result",
        "assertions/0",
        "assertions/1",
    )
    assert tuple(references) == first_references + second_references


def test_source_boundary_excludes_every_later_result_assertion():
    ledger = EventLedger()
    first = _source(ledger, locality="first")
    boundary = ledger.append_boundary()
    second = _source(ledger, locality="second")

    references = source_assertion_references_for_candidate_standing(
        ledger, source_append_boundary=boundary
    )

    assert {reference["recorded_result_occurrence_identity"] for reference in references} == {
        first.identity
    }
    assert second.identity not in {
        reference["recorded_result_occurrence_identity"] for reference in references
    }


def test_later_source_boundary_carries_prior_candidate_result_assertions(tmp_path):
    database = str(tmp_path / "recursive-candidate-standing.sqlite")
    ledger = SQLiteEventLedger(database)
    _source(ledger, exact_bytes=b"a")
    first_result = record_complete_candidate_standing(
        ledger,
        recording_locality_identity="first-candidate-standing",
        source_append_boundary=ledger.append_boundary(),
    )
    first_standing = get_recorded_candidate_standing(
        ledger, first_result.identity
    )
    later_source_boundary = ledger.append_boundary()

    later_references = source_assertion_references_for_candidate_standing(
        ledger, source_append_boundary=later_source_boundary
    )
    prior_candidate_identities = {
        candidate["dimensions"]["identity"]
        for candidate in first_standing["candidate_assertions"]
    }
    carried_prior_candidate_references = tuple(
        reference
        for reference in later_references
        if reference["recorded_result_occurrence_identity"] == first_result.identity
    )

    assert carried_prior_candidate_references[0]["assertion_identity"] == (
        first_standing["result_identity"]
    )
    assert {
        reference["assertion_identity"]
        for reference in carried_prior_candidate_references[1:]
    } == prior_candidate_identities
    assert all(
        reference["source_standing_coordinate"] == "candidate_result_occurrences"
        and reference["source_locality_identity"] == "first-candidate-standing"
        for reference in carried_prior_candidate_references
    )

    later_result = record_complete_candidate_standing(
        ledger,
        recording_locality_identity="later-candidate-standing",
        source_append_boundary=later_source_boundary,
    )
    expected = get_recorded_candidate_standing(ledger, later_result.identity)
    ledger.close()

    reopened = SQLiteEventLedger(database)
    assert get_recorded_candidate_standing(reopened, later_result.identity) == expected
    assert prior_candidate_identities <= {
        candidate["assertion_subject"]["source_assertion_reference"][
            "assertion_identity"
        ]
        for candidate in expected["candidate_assertions"]
    }


def test_complete_candidate_standing_owes_one_neutral_row_per_source_assertion():
    ledger = EventLedger()
    _source(ledger)
    source_boundary = ledger.append_boundary()
    source_references = source_assertion_references_for_candidate_standing(
        ledger, source_append_boundary=source_boundary
    )

    result = record_complete_candidate_standing(
        ledger,
        recording_locality_identity="candidate-production",
        source_append_boundary=source_boundary,
    )
    standing = get_recorded_candidate_standing(ledger, result.identity)
    applicability = get_recorded_candidate_standing_applicability(
        ledger, standing["applicability_result_event_identity"]
    )

    assert standing["responsibility"] == ONE_SOURCE_CANDIDATE_RESPONSIBILITY
    assert standing["exact_act"] == ONE_SOURCE_CANDIDATE_ACT
    assert tuple(standing["source_assertion_references"]) == source_references
    assert len(standing["candidate_assertions"]) == len(source_references)
    assert tuple(
        candidate["assertion_subject"]["source_assertion_reference"]
        for candidate in standing["candidate_assertions"]
    ) == source_references
    assert all(
        candidate["represented_relation"] == "Unknown"
        for candidate in standing["candidate_assertions"]
    )
    assert all(
        relation["role"] == "input"
        for relation in standing["participation"]
    )
    assert all(
        finding["relation"] == "input_to" and finding["role"] == "input"
        for finding in applicability["applicability_findings"]
    )
    assert all(
        set(candidate)
        == {
            "dimensions",
            "subject_kind",
            "responsible_boundary",
            "result",
            "assertion_subject",
            "assertion_scope",
            "represented_relation",
            "conflicts",
            "unknown",
            "limits",
        }
        for candidate in standing["candidate_assertions"]
    )
    assert standing["completeness"] == {
        "required_candidate_count": len(source_references),
        "recorded_candidate_count": len(source_references),
        "partial": False,
    }
    locality_standing = read_operator_locality_standing(
        ledger, locality_identity="candidate-production"
    )
    assert locality_standing["candidate_result_occurrences"] == {
        result.identity: None
    }
    assert locality_standing["comparison_result_occurrences"] == {}
    assert locality_standing["assertion_locality_movement_occurrences"] == {}


def test_source_and_candidate_result_boundaries_and_localities_stay_distinct():
    ledger = EventLedger()
    _source(ledger, locality="source")
    source_boundary = ledger.append_boundary()
    result = record_complete_candidate_standing(
        ledger,
        recording_locality_identity="candidate-production",
        source_append_boundary=source_boundary,
    )

    boundaries = boundaries_of_recorded_candidate_standing(
        ledger, result.identity
    )
    standing = get_recorded_candidate_standing(ledger, result.identity)

    assert boundaries["source_ledger_boundary"] == source_boundary
    assert (
        boundaries["candidate_result_ledger_boundary"]
        == ledger.append_boundary_through_occurrence(result.identity)
    )
    assert (
        boundaries["source_ledger_boundary"]
        != boundaries["candidate_result_ledger_boundary"]
    )
    assert result.locality_identity == "candidate-production"
    assert {
        reference["source_locality_identity"]
        for reference in standing["source_assertion_references"]
    } == {"source"}
    assert all(
        candidate["assertion_scope"]["recording_locality_identity"]
        == "candidate-production"
        for candidate in standing["candidate_assertions"]
    )
    assert all(
        candidate["dimensions"]["authority"]
        != candidate["assertion_subject"]["source_assertion_reference"][
            "source_assertion_coordinates"
        ]["Authority"]
        for candidate in standing["candidate_assertions"]
    )


def test_ordered_pair_candidate_standing_owes_both_orders_without_self_pairs():
    ledger = EventLedger()
    _source(ledger, exact_bytes=b"a")
    source_boundary = ledger.append_boundary()
    source_references = source_assertion_references_for_candidate_standing(
        ledger, source_append_boundary=source_boundary
    )

    result = record_complete_ordered_pair_candidate_standing(
        ledger,
        recording_locality_identity="ordered-pair-candidate-standing",
        source_append_boundary=source_boundary,
    )
    standing = get_recorded_candidate_standing(ledger, result.identity)
    expected = tuple(
        (first, second)
        for first_position, first in enumerate(source_references)
        for second_position, second in enumerate(source_references)
        if first_position != second_position
    )
    recorded = tuple(
        (
            candidate["assertion_subject"][
                "first_source_assertion_reference"
            ],
            candidate["assertion_subject"][
                "second_source_assertion_reference"
            ],
        )
        for candidate in standing["candidate_assertions"]
    )

    assert standing["responsibility"] == ORDERED_PAIR_CANDIDATE_RESPONSIBILITY
    assert standing["exact_act"] == ORDERED_PAIR_CANDIDATE_ACT
    assert recorded == expected
    assert standing["completeness"] == {
        "required_candidate_count": len(expected),
        "recorded_candidate_count": len(expected),
        "partial": False,
    }
    assert all(first != second for first, second in recorded)
    assert all(
        candidate["represented_relation"] == "Unknown"
        for candidate in standing["candidate_assertions"]
    )


def test_ordered_pair_candidate_reads_both_exact_lower_assertions_without_an_append(
    tmp_path,
):
    database = str(tmp_path / "ordered-pair-source-material.sqlite")
    ledger = SQLiteEventLedger(database)
    _source(ledger, exact_bytes=b"a")
    result = record_complete_ordered_pair_candidate_standing(
        ledger,
        recording_locality_identity="ordered-pair-candidates",
        source_append_boundary=ledger.append_boundary(),
    )
    standing = get_recorded_candidate_standing(ledger, result.identity)
    candidate = standing["candidate_assertions"][0]
    candidate_identity = candidate["dimensions"]["identity"]
    first_reference = candidate["assertion_subject"][
        "first_source_assertion_reference"
    ]
    second_reference = candidate["assertion_subject"][
        "second_source_assertion_reference"
    ]
    boundary_before_read = ledger.append_boundary()

    first, second = exact_source_assertion_materials_from_ordered_pair_candidate(
        ledger,
        candidate_standing_result_event_identity=result.identity,
        candidate_assertion_identity=candidate_identity,
    )

    assert first["result_identity"] == first_reference["assertion_identity"]
    assert second["dimensions"]["identity"] == second_reference["assertion_identity"]
    assert ledger.append_boundary() == boundary_before_read
    ledger.close()

    reopened = SQLiteEventLedger(database)
    assert exact_source_assertion_materials_from_ordered_pair_candidate(
        reopened,
        candidate_standing_result_event_identity=result.identity,
        candidate_assertion_identity=candidate_identity,
    ) == (first, second)


def test_ordered_pair_source_material_read_refuses_one_source_candidate():
    ledger = EventLedger()
    _source(ledger, exact_bytes=b"a")
    result = record_complete_candidate_standing(
        ledger,
        recording_locality_identity="one-source-candidates",
        source_append_boundary=ledger.append_boundary(),
    )
    standing = get_recorded_candidate_standing(ledger, result.identity)

    with pytest.raises(ValueError, match="not one exact ordered"):
        exact_source_assertion_materials_from_ordered_pair_candidate(
            ledger,
            candidate_standing_result_event_identity=result.identity,
            candidate_assertion_identity=(
                standing["candidate_assertions"][0]["dimensions"]["identity"]
            ),
        )


def test_every_ordered_pair_candidate_reads_both_sources_after_one_result_read(
    monkeypatch,
):
    import seed_runtime.candidate_standing_from_exact_result_assertions as candidate_runtime

    ledger = EventLedger()
    _source(ledger, exact_bytes=b"a")
    result = record_complete_ordered_pair_candidate_standing(
        ledger,
        recording_locality_identity="ordered-pair-candidates",
        source_append_boundary=ledger.append_boundary(),
    )
    standing = get_recorded_candidate_standing(ledger, result.identity)
    exact_read = candidate_runtime._read_candidate_result
    result_reads = 0

    def counted_read(*args, **coordinates):
        nonlocal result_reads
        result_reads += 1
        return exact_read(*args, **coordinates)

    monkeypatch.setattr(candidate_runtime, "_read_candidate_result", counted_read)
    boundary_before_read = ledger.append_boundary()
    readings = exact_source_assertion_materials_from_every_ordered_pair_candidate(
        ledger,
        candidate_standing_result_event_identity=result.identity,
    )

    assert result_reads == 1
    assert tuple(reading[0] for reading in readings) == tuple(
        candidate["dimensions"]["identity"]
        for candidate in standing["candidate_assertions"]
    )
    assert tuple(
        (
            first["result_identity"]
            if "result_identity" in first
            else first["dimensions"]["identity"],
            second["result_identity"]
            if "result_identity" in second
            else second["dimensions"]["identity"],
        )
        for _candidate_identity, first, second in readings
    ) == tuple(
        (
            candidate["assertion_subject"][
                "first_source_assertion_reference"
            ]["assertion_identity"],
            candidate["assertion_subject"][
                "second_source_assertion_reference"
            ]["assertion_identity"],
        )
        for candidate in standing["candidate_assertions"]
    )
    assert ledger.append_boundary() == boundary_before_read


def test_both_exact_candidate_responsibilities_use_one_source_boundary():
    ledger = EventLedger()
    _source(ledger, exact_bytes=b"a")
    source_boundary = ledger.append_boundary()

    one_source_result, ordered_pair_result = (
        record_one_source_and_ordered_pair_candidate_standings(
            ledger,
            one_source_recording_locality_identity="one-source-candidates",
            ordered_pair_recording_locality_identity="ordered-pair-candidates",
            source_append_boundary=source_boundary,
        )
    )
    one_source = get_recorded_candidate_standing(
        ledger, one_source_result.identity
    )
    ordered_pair = get_recorded_candidate_standing(
        ledger, ordered_pair_result.identity
    )

    assert one_source["responsibility"] == ONE_SOURCE_CANDIDATE_RESPONSIBILITY
    assert ordered_pair["responsibility"] == (
        ORDERED_PAIR_CANDIDATE_RESPONSIBILITY
    )
    assert one_source["source_ledger_boundary_identity"] == source_boundary.identity
    assert ordered_pair["source_ledger_boundary_identity"] == source_boundary.identity
    assert one_source_result.locality_identity == "one-source-candidates"
    assert ordered_pair_result.locality_identity == "ordered-pair-candidates"
    assert all(
        candidate["represented_relation"] == "Unknown"
        for standing in (one_source, ordered_pair)
        for candidate in standing["candidate_assertions"]
    )


def test_ordered_pair_candidate_standing_refuses_one_omitted_owed_candidate():
    ledger = EventLedger()
    _source(ledger, exact_bytes=b"a")
    result = record_complete_ordered_pair_candidate_standing(
        ledger,
        recording_locality_identity="ordered-pair-candidate-standing",
        source_append_boundary=ledger.append_boundary(),
    )
    ledger.get(result.identity).material["candidate_assertions"].pop()

    with pytest.raises(ValueError, match="not complete and exact"):
        get_recorded_candidate_standing(ledger, result.identity)


@pytest.mark.parametrize("change", ("missing", "extra", "reordered"))
def test_replay_refuses_rows_different_from_the_exact_source_and_act(change):
    ledger = EventLedger()
    _source(ledger)
    result = record_complete_candidate_standing(
        ledger,
        recording_locality_identity="candidate-production",
        source_append_boundary=ledger.append_boundary(),
    )
    material = ledger.get(result.identity).material
    candidates = material["candidate_assertions"]
    if change == "missing":
        candidates.pop()
    elif change == "extra":
        candidates.append(deepcopy(candidates[-1]))
    else:
        candidates[0], candidates[1] = candidates[1], candidates[0]

    with pytest.raises(ValueError, match="not complete and exact"):
        get_recorded_candidate_standing(ledger, result.identity)


def test_replay_requires_each_source_result_occurrence_intact():
    ledger = EventLedger()
    source = _source(ledger)
    result = record_complete_candidate_standing(
        ledger,
        recording_locality_identity="candidate-production",
        source_append_boundary=ledger.append_boundary(),
    )
    source.material["unknown"] = ["changed after Candidate result"]

    with pytest.raises(ValueError):
        get_recorded_candidate_standing(ledger, result.identity)


@pytest.mark.parametrize(
    "record_complete",
    (record_complete_candidate_standing, record_complete_ordered_pair_candidate_standing),
)
def test_empty_source_surface_records_one_complete_empty_candidate_standing(
    record_complete,
):
    ledger = EventLedger()
    result = record_complete(
        ledger,
        recording_locality_identity="candidate-production",
        source_append_boundary=ledger.append_boundary(),
    )

    standing = get_recorded_candidate_standing(ledger, result.identity)
    assert standing["source_assertion_references"] == []
    assert standing["candidate_assertions"] == []
    assert standing["completeness"] == {
        "required_candidate_count": 0,
        "recorded_candidate_count": 0,
        "partial": False,
    }


@pytest.mark.parametrize(
    "record_complete",
    (record_complete_candidate_standing, record_complete_ordered_pair_candidate_standing),
)
def test_complete_candidate_standing_replays_after_sqlite_restart(
    tmp_path, record_complete
):
    database = str(tmp_path / "candidate-standing.sqlite")
    ledger = SQLiteEventLedger(database)
    _source(ledger)
    source_boundary = ledger.append_boundary()
    result = record_complete(
        ledger,
        recording_locality_identity="candidate-production",
        source_append_boundary=source_boundary,
    )
    expected = get_recorded_candidate_standing(ledger, result.identity)
    ledger.close()

    reopened = SQLiteEventLedger(database)
    assert get_recorded_candidate_standing(reopened, result.identity) == expected
    boundaries = boundaries_of_recorded_candidate_standing(
        reopened, result.identity
    )
    assert boundaries["source_ledger_boundary"] == source_boundary
    assert (
        boundaries["candidate_result_ledger_boundary"]
        == reopened.append_boundary_through_occurrence(result.identity)
    )


def test_machine_grammar_names_the_exact_source_assertion_coordinates_and_one_source_candidate_responsibility():
    import json

    with open("book_of_seed/grammar.json", encoding="utf-8") as source:
        clause = json.load(source)["clause_coordinates"][BOOK_CLAUSE]

    assert clause["source_Assertion_coordinates"] == {
        "result_Assertions": [
            "exact_Measurement_result_Assertion",
            "exact_Compare_result_Assertion",
            "exact_Candidate_result_Assertion",
        ],
        "carried_Assertion_relation": {
            "first_subject": "each_exact_Assertion",
            "relation": "carried_by",
            "second_subject": "one_exact_result_Assertion",
        },
        "bounded_by": "exact_ledger_boundary",
        "order": "event_order",
        "coordinates": [
            "source_Assertion_reference",
            "source_Locality",
            "source_Standing_boundary",
            "Evidence",
            "Authority",
            "Scope",
            "limits",
            "Unknown",
        ],
    }
    coordinate = clause["one_source_candidate_responsibility"]
    assert coordinate["responsibility"] == (
        ONE_SOURCE_CANDIDATE_RESPONSIBILITY.replace(" ", "_")
    )
    assert coordinate["exact_Act"] == ONE_SOURCE_CANDIDATE_ACT.replace(" ", "_")
    assert coordinate["source_input_relation"] == {
        "first_subject": "exact_source_Assertion",
        "relation": "input_to",
        "second_subject": ONE_SOURCE_CANDIDATE_ACT.replace(" ", "_"),
        "role": "input",
    }
    assert coordinate["source_Participation"] == {
        "subject_reference": "exact_source_Assertion",
        "role": "input",
        "act": ONE_SOURCE_CANDIDATE_ACT.replace(" ", "_"),
        "act_occurrence": "exact_Candidate_Act_occurrence",
    }


def test_machine_grammar_names_the_exact_ordered_pair_candidate_responsibility():
    import json

    with open("book_of_seed/grammar.json", encoding="utf-8") as source:
        coordinate = json.load(source)["clause_coordinates"][BOOK_CLAUSE][
            "ordered_pair_candidate_responsibility"
        ]

    assert coordinate["exact_Act"] == ORDERED_PAIR_CANDIDATE_ACT.replace(" ", "_")
    assert coordinate["responsibility"] == (
        ORDERED_PAIR_CANDIDATE_RESPONSIBILITY.replace(" ", "_")
    )
    assert coordinate["source_pair"] == {
        "first_subject": "ordered_pair",
        "relation": "of",
        "second_subject": "distinct_exact_source_Assertions",
    }
    assert coordinate["candidate_source_roles"] == [
        "first_source_Assertion",
        "second_source_Assertion",
    ]
    assert coordinate["requires"] == "distinct_exact_source_Assertion_references"
    assert coordinate["order"] == [
        "first_source_event_order",
        "second_source_event_order",
    ]
    assert coordinate["represented_relation"] == "Unknown"


FIDELITY_SUBJECTS = {
    "complete_candidate_standing_source_coordinates": (
        test_exact_source_assertion_coordinates_expose_every_result_assertion_in_event_order,
        test_source_boundary_excludes_every_later_result_assertion,
        test_later_source_boundary_carries_prior_candidate_result_assertions,
        test_source_and_candidate_result_boundaries_and_localities_stay_distinct,
        test_replay_requires_each_source_result_occurrence_intact,
    ),
    "complete_candidate_standing_coordinate_order": (
        test_complete_candidate_standing_owes_one_neutral_row_per_source_assertion,
        test_ordered_pair_candidate_standing_owes_both_orders_without_self_pairs,
        test_ordered_pair_candidate_reads_both_exact_lower_assertions_without_an_append,
        test_ordered_pair_source_material_read_refuses_one_source_candidate,
        test_every_ordered_pair_candidate_reads_both_sources_after_one_result_read,
        test_both_exact_candidate_responsibilities_use_one_source_boundary,
        test_ordered_pair_candidate_standing_refuses_one_omitted_owed_candidate,
        test_replay_refuses_rows_different_from_the_exact_source_and_act,
        test_empty_source_surface_records_one_complete_empty_candidate_standing,
        test_complete_candidate_standing_replays_after_sqlite_restart,
    ),
    "one_source_candidate_standing_responsibility_coordinates": (
        test_machine_grammar_names_the_exact_source_assertion_coordinates_and_one_source_candidate_responsibility,
    ),
    "ordered_pair_candidate_standing_responsibility_coordinates": (
        test_machine_grammar_names_the_exact_ordered_pair_candidate_responsibility,
    ),
}
