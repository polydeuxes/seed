from copy import deepcopy
import inspect

import pytest

from seed_runtime.candidate_results_from_exact_result_assertions import (
    APPLICABILITY_ACT,
    CANDIDATE_OCCURRENCE_STREAM,
    ONE_SOURCE_CANDIDATE_ACT,
    ORDERED_PAIR_CANDIDATE_ACT,
    candidate_assertion_from_result,
    candidate_responsibility_progress,
    get_candidate_act,
    get_candidate_applicability_act,
    get_candidate_applicability_result,
    get_candidate_participation,
    get_candidate_responsibility,
    get_candidate_yield_relation,
    get_recorded_candidate_result,
    record_one_owed_candidate_result,
    record_one_source_candidate_responsibility,
    record_ordered_pair_candidate_responsibility,
    source_assertion_references_through_boundary,
    yield_candidate_results,
)
from seed_runtime.events import EventLedger, SQLiteEventLedger
from seed_runtime.operator_locality_standing import read_operator_locality_standing
from tests.operator_material_acquisition_test_witness import (
    record_operator_material_occurrence,
)
from tests.test_operator_locality_standing import _record_byte_measurement


def _source(ledger, *, locality="source", exact_bytes=b"ab"):
    record_operator_material_occurrence(
        ledger,
        locality_identity=locality,
        exact=exact_bytes,
        source_boundary="candidate source boundary",
    )
    return _record_byte_measurement(
        ledger,
        source_localities=(locality,),
        recording_locality_identity=locality,
    )


def _one_source_responsibility(ledger, *, locality="candidate"):
    _source(ledger)
    boundary = ledger.append_boundary()
    return record_one_source_candidate_responsibility(
        ledger,
        source_append_boundary=boundary,
        recording_locality_identity=locality,
    )


def test_source_read_preserves_every_exact_assertion_coordinate_in_order():
    ledger = EventLedger()
    result = _source(ledger)

    references = source_assertion_references_through_boundary(
        ledger, source_append_boundary=ledger.append_boundary()
    )

    assert tuple(
        reference["recorded_result_occurrence_identity"] for reference in references
    ) == (result.identity,) * 4
    assert tuple(reference["assertion_coordinate"] for reference in references) == (
        "result",
        "assertions/0",
        "assertions/1",
        "assertions/2",
    )


def test_one_candidate_yields_while_its_responsibility_still_owes_subjects():
    ledger = EventLedger()
    responsibility = _one_source_responsibility(ledger)

    yielded = record_one_owed_candidate_result(
        ledger, responsibility_event_identity=responsibility.identity
    )

    assert yielded is not None
    assert len(yielded.progress.required_candidate_addresses) == 4
    assert yielded.progress.recorded_candidate_result_occurrences == (
        yielded.result_occurrence.identity,
    )
    assert len(yielded.progress.owed_candidate_addresses) == 3
    material = get_recorded_candidate_result(
        ledger, yielded.result_occurrence.identity
    )
    assert "candidate_assertion" in material
    assert "candidate_assertions" not in material
    assert "required_candidate_count" not in material
    assert "recorded_candidate_count" not in material
    assert "partial" not in material


def test_another_responsibility_can_begin_before_the_first_is_exhausted():
    ledger = EventLedger()
    _source(ledger)
    source_boundary = ledger.append_boundary()
    first = record_one_source_candidate_responsibility(
        ledger,
        source_append_boundary=source_boundary,
        recording_locality_identity="first candidate road",
    )
    first_yield = record_one_owed_candidate_result(
        ledger, responsibility_event_identity=first.identity
    )
    assert first_yield is not None
    assert first_yield.progress.owed_candidate_addresses

    second = record_one_source_candidate_responsibility(
        ledger,
        source_append_boundary=source_boundary,
        recording_locality_identity="second candidate road",
    )
    second_yield = record_one_owed_candidate_result(
        ledger, responsibility_event_identity=second.identity
    )

    assert second_yield is not None
    assert first_yield.progress.owed_candidate_addresses
    assert second_yield.progress.owed_candidate_addresses


def test_resuming_one_responsibility_exhausts_every_owed_subject_once():
    ledger = EventLedger()
    responsibility = _one_source_responsibility(ledger)
    first = record_one_owed_candidate_result(
        ledger, responsibility_event_identity=responsibility.identity
    )
    assert first is not None

    later = tuple(
        yield_candidate_results(
            ledger, responsibility_event_identity=responsibility.identity
        )
    )
    final = candidate_responsibility_progress(
        ledger, responsibility_event_identity=responsibility.identity
    )

    assert len(later) == 3
    assert final.owed_candidate_addresses == ()
    assert len(final.recorded_candidate_result_occurrences) == 4
    assert len(set(final.recorded_candidate_result_occurrences)) == 4
    assert record_one_owed_candidate_result(
        ledger, responsibility_event_identity=responsibility.identity
    ) is None


def test_each_subject_has_its_own_applicability_participation_act_yield_and_result():
    ledger = EventLedger()
    responsibility = _one_source_responsibility(ledger)
    yielded = record_one_owed_candidate_result(
        ledger, responsibility_event_identity=responsibility.identity
    )
    assert yielded is not None

    result = get_recorded_candidate_result(ledger, yielded.result_occurrence.identity)
    applicability = get_candidate_applicability_result(
        ledger, result["applicability_result_occurrence_identity"]
    )
    applicability_act = next(
        event
        for event in ledger.iter_locality_kind("candidate", CANDIDATE_OCCURRENCE_STREAM)
        if event.material.get("applicability_result_identity")
        == applicability["result_identity"]
        and event.material.get("act") == APPLICABILITY_ACT
    )
    participation = get_candidate_participation(
        ledger, result["participation_relation_occurrence_identity"]
    )
    candidate_act = next(
        event
        for event in ledger.iter_locality_kind("candidate", CANDIDATE_OCCURRENCE_STREAM)
        if event.material.get("candidate_result_identity") == result["result_identity"]
        and event.material.get("act") == ONE_SOURCE_CANDIDATE_ACT
    )

    get_candidate_responsibility(ledger, responsibility.identity)
    get_candidate_applicability_act(ledger, applicability_act.identity)
    get_candidate_act(ledger, candidate_act.identity)
    get_candidate_yield_relation(
        ledger, applicability["yield_relation_occurrence_identity"]
    )
    get_candidate_yield_relation(ledger, result["yield_relation_occurrence_identity"])
    assert participation["first_subject"] == result["required_subject"]
    assert participation["second_subject"] == {
        "Act_occurrence": result["act_occurrence_identity"]
    }


def test_ordered_pair_responsibility_owes_each_distinct_ordered_pair():
    ledger = EventLedger()
    _source(ledger, exact_bytes=b"a")
    boundary = ledger.append_boundary()
    references = source_assertion_references_through_boundary(
        ledger, source_append_boundary=boundary
    )
    responsibility = record_ordered_pair_candidate_responsibility(
        ledger,
        source_append_boundary=boundary,
        recording_locality_identity="pairs",
    )

    progress = candidate_responsibility_progress(
        ledger, responsibility_event_identity=responsibility.identity
    )
    assert len(progress.required_candidate_addresses) == len(references) * (
        len(references) - 1
    )

    yielded = tuple(
        yield_candidate_results(
            ledger, responsibility_event_identity=responsibility.identity
        )
    )
    pairs = tuple(
        tuple(
            (
                reference["recorded_result_occurrence_identity"],
                reference["assertion_coordinate"],
            )
            for reference in item.result_occurrence.material["required_subject"][
                "source_assertion_references"
            ]
        )
        for item in yielded
    )
    assert all(first != second for first, second in pairs)
    assert len(pairs) == len(set(pairs))
    assert all(
        item.result_occurrence.material["exact_act"] == ORDERED_PAIR_CANDIDATE_ACT
        for item in yielded
    )


def test_source_boundary_is_frozen_when_later_sources_arrive():
    ledger = EventLedger()
    _source(ledger, locality="first", exact_bytes=b"a")
    boundary = ledger.append_boundary()
    responsibility = record_one_source_candidate_responsibility(
        ledger,
        source_append_boundary=boundary,
        recording_locality_identity="candidate",
    )
    required_before = candidate_responsibility_progress(
        ledger, responsibility_event_identity=responsibility.identity
    ).required_candidate_addresses

    _source(ledger, locality="later", exact_bytes=b"bc")
    required_after = candidate_responsibility_progress(
        ledger, responsibility_event_identity=responsibility.identity
    ).required_candidate_addresses

    assert required_after == required_before


def test_candidate_result_is_available_to_bounded_replay_without_positive_standing():
    ledger = EventLedger()
    responsibility = _one_source_responsibility(ledger)
    yielded = record_one_owed_candidate_result(
        ledger, responsibility_event_identity=responsibility.identity
    )
    assert yielded is not None

    replay = read_operator_locality_standing(
        ledger, locality_identity="candidate"
    )

    assert yielded.result_occurrence.identity in replay["candidate_result_occurrences"]
    result = get_recorded_candidate_result(ledger, yielded.result_occurrence.identity)
    assert "standing" not in result
    assert "standing_occurrence_identity" not in result
    assert "standing_responsibility_reference" not in result


def test_candidate_assertion_is_independently_readable_from_one_result():
    ledger = EventLedger()
    responsibility = _one_source_responsibility(ledger)
    yielded = record_one_owed_candidate_result(
        ledger, responsibility_event_identity=responsibility.identity
    )
    assert yielded is not None

    assertion = candidate_assertion_from_result(
        ledger, candidate_result_event_identity=yielded.result_occurrence.identity
    )

    assert assertion == yielded.result_occurrence.material["candidate_assertion"]
    assert assertion["relation"] == "Unknown"


def test_record_one_owed_candidate_accepts_no_caller_subject_choice():
    parameters = inspect.signature(record_one_owed_candidate_result).parameters
    assert tuple(parameters) == ("ledger", "responsibility_event_identity")


def test_sqlite_reopen_preserves_owed_work_and_resumes_it(tmp_path):
    database = str(tmp_path / "candidate.sqlite")
    ledger = SQLiteEventLedger(database)
    responsibility = _one_source_responsibility(ledger)
    first = record_one_owed_candidate_result(
        ledger, responsibility_event_identity=responsibility.identity
    )
    assert first is not None
    before = first.progress
    ledger.close()

    reopened = SQLiteEventLedger(database)
    after = candidate_responsibility_progress(
        reopened, responsibility_event_identity=responsibility.identity
    )
    assert after == before
    resumed = tuple(
        yield_candidate_results(
            reopened, responsibility_event_identity=responsibility.identity
        )
    )
    assert len(resumed) == len(before.owed_candidate_addresses)
    assert resumed[-1].progress.owed_candidate_addresses == ()


def test_changed_candidate_result_is_refused():
    ledger = EventLedger()
    responsibility = _one_source_responsibility(ledger)
    yielded = record_one_owed_candidate_result(
        ledger, responsibility_event_identity=responsibility.identity
    )
    assert yielded is not None
    original = deepcopy(yielded.result_occurrence.material["candidate_assertion"])
    yielded.result_occurrence.material["candidate_assertion"]["relation"] = "same"

    with pytest.raises(ValueError, match="Candidate result is not exact"):
        get_recorded_candidate_result(ledger, yielded.result_occurrence.identity)

    assert original["relation"] == "Unknown"
