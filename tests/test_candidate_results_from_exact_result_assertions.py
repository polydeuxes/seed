from copy import deepcopy
import inspect

import pytest

import seed_runtime.candidate_results_from_exact_result_assertions as candidate_module
from seed_runtime.candidate_results_from_exact_result_assertions import (
    ACT_BOOK_CLAUSE,
    APPLICABILITY_ACT,
    APPLICABILITY_BOOK_CLAUSE,
    APPLICABILITY_RESPONSIBILITY,
    BOOK_CLAUSE,
    CANDIDATE_OCCURRENCE_STREAM,
    ONE_SOURCE_CANDIDATE_ACT,
    ORDERED_PAIR_CANDIDATE_ACT,
    boundaries_of_recorded_candidate_result,
    candidate_assertion_from_result,
    candidate_results_by_required_subject,
    get_candidate_act,
    get_candidate_applicability_act,
    get_candidate_applicability_responsibility,
    get_candidate_applicability_result,
    get_candidate_participation,
    get_candidate_responsibility,
    get_candidate_yield_relation,
    get_recorded_candidate_result,
    record_one_candidate_result,
    record_one_source_candidate_responsibility,
    record_ordered_pair_candidate_responsibility,
    required_subjects_for_candidate_responsibility,
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


def test_one_candidate_yields_while_required_subjects_remain_unrecorded():
    ledger = EventLedger()
    responsibility = _one_source_responsibility(ledger)

    yielded = record_one_candidate_result(
        ledger, responsibility_event_identity=responsibility.identity
    )

    assert yielded is not None
    required = required_subjects_for_candidate_responsibility(
        ledger, responsibility_event_identity=responsibility.identity
    )
    recorded = candidate_results_by_required_subject(
        ledger, responsibility_event_identity=responsibility.identity
    )
    assert len(required) == 4
    assert recorded == (
        (
            yielded.material["required_subject"][
                "required_subject_address"
            ],
            yielded.identity,
        ),
    )
    assert len(required) - len(recorded) == 3
    material = get_recorded_candidate_result(
        ledger, yielded.identity
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
    first_yield = record_one_candidate_result(
        ledger, responsibility_event_identity=first.identity
    )
    assert first_yield is not None
    assert len(candidate_results_by_required_subject(
        ledger, responsibility_event_identity=first.identity
    )) == 1

    second = record_one_source_candidate_responsibility(
        ledger,
        source_append_boundary=source_boundary,
        recording_locality_identity="second candidate road",
    )
    second_yield = record_one_candidate_result(
        ledger, responsibility_event_identity=second.identity
    )

    assert second_yield is not None
    assert len(candidate_results_by_required_subject(
        ledger, responsibility_event_identity=first.identity
    )) == 1
    assert len(candidate_results_by_required_subject(
        ledger, responsibility_event_identity=second.identity
    )) == 1


def test_resuming_one_responsibility_records_every_required_subject_once():
    ledger = EventLedger()
    responsibility = _one_source_responsibility(ledger)
    first = record_one_candidate_result(
        ledger, responsibility_event_identity=responsibility.identity
    )
    assert first is not None

    later = tuple(
        yield_candidate_results(
            ledger, responsibility_event_identity=responsibility.identity
        )
    )
    required = required_subjects_for_candidate_responsibility(
        ledger, responsibility_event_identity=responsibility.identity
    )
    recorded = candidate_results_by_required_subject(
        ledger, responsibility_event_identity=responsibility.identity
    )

    assert len(later) == 3
    assert len(recorded) == len(required)
    result_occurrences = tuple(result for _subject, result in recorded)
    assert len(result_occurrences) == 4
    assert len(set(result_occurrences)) == 4
    assert record_one_candidate_result(
        ledger, responsibility_event_identity=responsibility.identity
    ) is None


def test_each_subject_has_its_own_applicability_participation_act_yield_and_result():
    ledger = EventLedger()
    responsibility = _one_source_responsibility(ledger)
    yielded = record_one_candidate_result(
        ledger, responsibility_event_identity=responsibility.identity
    )
    assert yielded is not None

    result = get_recorded_candidate_result(ledger, yielded.identity)
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
    applicability_responsibility = next(
        event
        for event in ledger.iter_locality_kind(
            "candidate", CANDIDATE_OCCURRENCE_STREAM
        )
        if event.material.get("responsibility") == APPLICABILITY_RESPONSIBILITY
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
    get_candidate_applicability_responsibility(
        ledger, applicability_responsibility.identity
    )
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
    assert applicability_act.material["responsibility"] == (
        APPLICABILITY_RESPONSIBILITY
    )
    assert candidate_act.material["responsibility"] != APPLICABILITY_RESPONSIBILITY
    assert applicability_act.material["authority"] != candidate_act.material[
        "authority"
    ]
    assert applicability_act.material["scope"] != candidate_act.material["scope"]
    assert set(result["required_subject"]) == {
        "required_subject_address",
        "position",
        "role",
        "source_assertion_references",
    }
    assert result["required_subject"]["required_subject_address"] != result[
        "candidate_assertion"
    ]["subject_address"]


def test_shared_storage_stream_preserves_each_occurrence_book_coordinate():
    ledger = EventLedger()
    responsibility = _one_source_responsibility(ledger)
    yielded = record_one_candidate_result(
        ledger, responsibility_event_identity=responsibility.identity
    )
    assert yielded is not None

    events = tuple(
        ledger.iter_locality_kind("candidate", CANDIDATE_OCCURRENCE_STREAM)
    )
    assert len(events) == 9
    for event in events:
        material = event.material
        if material.get("relation") == "yield":
            assert material["book_reference"] == ACT_BOOK_CLAUSE
        elif (
            material.get("responsibility") == APPLICABILITY_RESPONSIBILITY
            or material.get("act") == APPLICABILITY_ACT
            or material.get("exact_act") == APPLICABILITY_ACT
            or material.get("relation") == "participation"
        ):
            assert material["book_reference"] == APPLICABILITY_BOOK_CLAUSE
        else:
            assert material["book_reference"] == BOOK_CLAUSE


def test_generator_rereads_required_subjects_and_results_after_yielding_control():
    ledger = EventLedger()
    responsibility = _one_source_responsibility(ledger)
    generated = yield_candidate_results(
        ledger, responsibility_event_identity=responsibility.identity
    )

    first = next(generated)
    interleaved = record_one_candidate_result(
        ledger, responsibility_event_identity=responsibility.identity
    )
    assert interleaved is not None
    resumed = next(generated)
    completed = tuple(generated)

    result_subjects = tuple(
        subject
        for subject, _result in candidate_results_by_required_subject(
            ledger, responsibility_event_identity=responsibility.identity
        )
    )
    assert len(result_subjects) == len(set(result_subjects)) == 4
    assert first.identity != interleaved.identity
    assert resumed.identity != interleaved.identity
    assert len(completed) == 1


def test_second_result_for_one_required_subject_is_refused_before_append():
    ledger = EventLedger()
    responsibility = _one_source_responsibility(ledger)
    yielded = record_one_candidate_result(
        ledger, responsibility_event_identity=responsibility.identity
    )
    assert yielded is not None
    exact_responsibility = candidate_module._read_responsibility(
        ledger, responsibility.identity
    )
    subject = candidate_module._required_subjects(exact_responsibility)[0]
    boundary = ledger.append_boundary()

    with pytest.raises(
        ValueError,
        match="already has a result for this required subject",
    ):
        candidate_module._record_candidate_result_for_subject(
            ledger, exact_responsibility, subject
        )

    assert ledger.append_boundary() == boundary


def test_candidate_result_preserves_distinct_source_result_boundaries_and_localities():
    ledger = EventLedger()
    responsibility = _one_source_responsibility(
        ledger, locality="candidate locality"
    )
    yielded = record_one_candidate_result(
        ledger, responsibility_event_identity=responsibility.identity
    )
    assert yielded is not None

    result = get_recorded_candidate_result(ledger, yielded.identity)
    boundaries = boundaries_of_recorded_candidate_result(
        ledger, yielded.identity
    )
    source_reference = result["required_subject"][
        "source_assertion_references"
    ][0]

    assert boundaries["source_ledger_boundary"] != boundaries[
        "candidate_result_ledger_boundary"
    ]
    assert source_reference["source_locality_identity"] == "source"
    assert yielded.locality_identity == "candidate locality"
    assert result["candidate_assertion"]["Authority"] == result["authority"]
    assert result["candidate_assertion"]["Authority"] != source_reference[
        "source_assertion_coordinates"
    ]["Authority"]


def test_yielded_candidate_is_an_exact_subject_read_at_a_later_source_boundary():
    ledger = EventLedger()
    responsibility = _one_source_responsibility(ledger)
    yielded = record_one_candidate_result(
        ledger, responsibility_event_identity=responsibility.identity
    )
    assert yielded is not None
    later_boundary = ledger.append_boundary()

    references = source_assertion_references_through_boundary(
        ledger, source_append_boundary=later_boundary
    )
    candidate_references = tuple(
        reference
        for reference in references
        if reference["recorded_result_occurrence_identity"]
        == yielded.identity
    )
    assert tuple(
        reference["assertion_coordinate"] for reference in candidate_references
    ) == ("result", "candidate_assertion")
    assert candidate_references[1]["assertion_identity"] == (
        yielded.material["candidate_assertion"]["subject_address"]
    )


def test_ordered_pair_responsibility_requires_each_distinct_ordered_pair():
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

    required_subjects = required_subjects_for_candidate_responsibility(
        ledger, responsibility_event_identity=responsibility.identity
    )
    assert len(required_subjects) == len(references) * (
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
            for reference in item.material["required_subject"][
                "source_assertion_references"
            ]
        )
        for item in yielded
    )
    assert all(first != second for first, second in pairs)
    assert len(pairs) == len(set(pairs))
    assert all(
        item.material["exact_act"] == ORDERED_PAIR_CANDIDATE_ACT
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
    required_before = required_subjects_for_candidate_responsibility(
        ledger, responsibility_event_identity=responsibility.identity
    )

    _source(ledger, locality="later", exact_bytes=b"bc")
    required_after = required_subjects_for_candidate_responsibility(
        ledger, responsibility_event_identity=responsibility.identity
    )

    assert required_after == required_before


def test_candidate_result_is_available_to_bounded_replay_without_positive_standing():
    ledger = EventLedger()
    responsibility = _one_source_responsibility(ledger)
    yielded = record_one_candidate_result(
        ledger, responsibility_event_identity=responsibility.identity
    )
    assert yielded is not None

    replay = read_operator_locality_standing(
        ledger, locality_identity="candidate"
    )

    assert yielded.identity in replay["candidate_result_occurrences"]
    result = get_recorded_candidate_result(ledger, yielded.identity)
    assert "standing" not in result
    assert "standing_occurrence_identity" not in result
    assert "standing_responsibility_reference" not in result


def test_candidate_assertion_is_independently_readable_from_one_result():
    ledger = EventLedger()
    responsibility = _one_source_responsibility(ledger)
    yielded = record_one_candidate_result(
        ledger, responsibility_event_identity=responsibility.identity
    )
    assert yielded is not None

    assertion = candidate_assertion_from_result(
        ledger, candidate_result_event_identity=yielded.identity
    )

    assert assertion == yielded.material["candidate_assertion"]
    assert assertion["relation"] == "Unknown"


def test_record_one_candidate_accepts_no_caller_subject_choice():
    parameters = inspect.signature(
        record_one_candidate_result
    ).parameters
    assert tuple(parameters) == ("ledger", "responsibility_event_identity")


def test_sqlite_reopen_preserves_unrecorded_work_and_resumes_it(tmp_path):
    database = str(tmp_path / "candidate.sqlite")
    ledger = SQLiteEventLedger(database)
    responsibility = _one_source_responsibility(ledger)
    first = record_one_candidate_result(
        ledger, responsibility_event_identity=responsibility.identity
    )
    assert first is not None
    before_required = required_subjects_for_candidate_responsibility(
        ledger, responsibility_event_identity=responsibility.identity
    )
    before_recorded = candidate_results_by_required_subject(
        ledger, responsibility_event_identity=responsibility.identity
    )
    ledger.close()

    reopened = SQLiteEventLedger(database)
    after_required = required_subjects_for_candidate_responsibility(
        reopened, responsibility_event_identity=responsibility.identity
    )
    after_recorded = candidate_results_by_required_subject(
        reopened, responsibility_event_identity=responsibility.identity
    )
    assert after_required == before_required
    assert after_recorded == before_recorded
    resumed = tuple(
        yield_candidate_results(
            reopened, responsibility_event_identity=responsibility.identity
        )
    )
    assert len(resumed) == len(before_required) - len(before_recorded)
    assert len(candidate_results_by_required_subject(
        reopened, responsibility_event_identity=responsibility.identity
    )) == len(before_required)


def test_changed_candidate_result_is_refused():
    ledger = EventLedger()
    responsibility = _one_source_responsibility(ledger)
    yielded = record_one_candidate_result(
        ledger, responsibility_event_identity=responsibility.identity
    )
    assert yielded is not None
    original = deepcopy(yielded.material["candidate_assertion"])
    yielded.material["candidate_assertion"]["relation"] = "same"

    with pytest.raises(ValueError, match="Candidate result is not exact"):
        get_recorded_candidate_result(ledger, yielded.identity)

    assert original["relation"] == "Unknown"
