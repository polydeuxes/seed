from copy import deepcopy

import pytest

from seed_runtime.candidate_standing_from_exact_result_assertions import (
    BOOK_CLAUSE,
    CANDIDATE_RULE,
    SOURCE_RULE,
    boundaries_of_recorded_candidate_standing,
    get_recorded_candidate_standing,
    record_complete_candidate_standing,
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


def test_source_rule_exposes_every_result_assertion_in_event_order():
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

    assert standing["source_rule"] == SOURCE_RULE
    assert standing["candidate_rule"] == CANDIDATE_RULE
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


@pytest.mark.parametrize("change", ("missing", "extra", "reordered"))
def test_replay_refuses_rows_different_from_the_source_and_candidate_rules(change):
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


def test_empty_source_surface_records_one_complete_empty_candidate_standing():
    ledger = EventLedger()
    result = record_complete_candidate_standing(
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


def test_complete_candidate_standing_replays_after_sqlite_restart(tmp_path):
    database = str(tmp_path / "candidate-standing.sqlite")
    ledger = SQLiteEventLedger(database)
    _source(ledger)
    source_boundary = ledger.append_boundary()
    result = record_complete_candidate_standing(
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


def test_machine_grammar_names_the_exact_first_source_and_candidate_rules():
    import json

    with open("book_of_seed/grammar.json", encoding="utf-8") as source:
        clause = json.load(source)["clause_coordinates"][BOOK_CLAUSE]

    assert clause["source_rule"]["identity"] == SOURCE_RULE.replace(" ", "_")
    assert clause["candidate_rule"]["identity"] == CANDIDATE_RULE.replace(" ", "_")


FIDELITY_SUBJECTS = {
    "complete_candidate_standing_source_coordinates": (
        test_source_rule_exposes_every_result_assertion_in_event_order,
        test_source_boundary_excludes_every_later_result_assertion,
        test_source_and_candidate_result_boundaries_and_localities_stay_distinct,
        test_replay_requires_each_source_result_occurrence_intact,
    ),
    "complete_candidate_standing_coordinate_order": (
        test_complete_candidate_standing_owes_one_neutral_row_per_source_assertion,
        test_replay_refuses_rows_different_from_the_source_and_candidate_rules,
        test_empty_source_surface_records_one_complete_empty_candidate_standing,
        test_complete_candidate_standing_replays_after_sqlite_restart,
    ),
    "complete_candidate_standing_grammar_coordinates": (
        test_machine_grammar_names_the_exact_first_source_and_candidate_rules,
    ),
}
