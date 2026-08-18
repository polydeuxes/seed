from __future__ import annotations

import hashlib
import json

import pytest

import seed_runtime.measurement_of_position_coordinates_of_byte_pair_occurrences as direct_position_module
import seed_runtime.measurement_of_shared_position_of_byte_pair_occurrences as shared_position_module
from seed_runtime.byte_measurement import (
    assertions_of_recorded_byte_position_pair_measurement,
    record_byte_measurement_responsible_act_evidence,
    record_byte_measurement_result,
    record_byte_position_pair_count_layer,
)
from seed_runtime.events import EventLedger, SQLiteEventLedger
from seed_runtime.material_ingest import ingest_material
from seed_runtime.measurement_of_recurrent_byte_pair_occurrence_position import (
    measure_positions_for_recurrent_byte_pair_assertions,
    record_responsibility_assignment_for_measurement_of_recurrent_byte_pair_occurrence_position,
    record_evidence_of_act_occurrence_for_measurement_of_recurrent_byte_pair_occurrence_position,
    record_result_of_measurement_of_recurrent_byte_pair_occurrence_position,
    references_to_recorded_recurrent_byte_pair_occurrence_positions,
)
from seed_runtime.measurement_of_position_coordinates_of_byte_pair_occurrences import (
    record_byte_pair_occurrence_position_measurement_responsibility_assignment,
    record_byte_pair_occurrence_position_measurement_act_evidence,
    record_byte_pair_occurrence_position_measurement_result,
    references_to_recorded_position_coordinates_of_byte_pair_occurrences,
)
from seed_runtime.measurement_of_shared_position_of_byte_pair_occurrences import (
    SHARED_POSITION_APPLICABILITY_RESULT_KIND,
    SHARED_POSITION_MEASUREMENT_RESULT_KIND,
    SharedPairPositionError,
    get_shared_position_responsibility_assignment,
    get_shared_position_applicability_act_evidence,
    get_recorded_shared_position_applicability,
    get_shared_position_measurement_act_evidence,
    get_recorded_shared_position_measurement,
    record_shared_position_applicability_act_evidence,
    record_shared_position_applicability_result,
    record_shared_position_measurement_act_evidence,
    record_shared_position_measurement_result,
    record_shared_position_responsibility_assignment,
)
from seed_runtime.operator_locality_standing import (
    advance_operator_locality_standing,
    read_operator_locality_standing,
)
from seed_runtime.operator_representation import (
    read_operator_representation,
    record_operator_representation,
)


def _standing(ledger: EventLedger, locality: str):
    return read_operator_locality_standing(
        ledger, locality_identity=locality
    )


def _fixture(*, current: bytes = b"abc", ledger=None):
    if ledger is None:
        ledger = EventLedger()
    locality = "shared-pair-position"
    ingest_material(
        ledger,
        locality_identity=locality,
        exact_bytes=b"abxxabbcxxbc",
        source_role="premise material",
        source_boundary="exact premise boundary",
    )
    byte_act = record_byte_measurement_responsible_act_evidence(
        ledger,
        source_localities=(locality,),
        recording_locality_identity=locality,
    )
    byte_result = record_byte_measurement_result(
        ledger,
        responsible_act_evidence_event_identity=byte_act.identity,
    )
    pair_result = record_byte_position_pair_count_layer(
        ledger,
        source_measurement_event_identity=byte_result.identity,
        recording_locality_identity=locality,
    )
    pair_assertions = assertions_of_recorded_byte_position_pair_measurement(
        ledger, pair_result.identity
    )
    recurrence_by_pair = {
        assertion.representation: assertion.assertion_identity
        for assertion in pair_assertions or ()
        if assertion.result == "recurrence"
        and assertion.representation in {(ord("a"), ord("b")), (ord("b"), ord("c"))}
    }
    assert set(recurrence_by_pair) == {
        (ord("a"), ord("b")),
        (ord("b"), ord("c")),
    }
    source = ingest_material(
        ledger,
        locality_identity=locality,
        exact_bytes=current,
        source_role="later exact material",
        source_boundary="later exact material boundary",
    )
    findings = measure_positions_for_recurrent_byte_pair_assertions(
        ledger,
        pair_measurement_occurrence_identity=pair_result.identity,
        recurrence_assertion_identities=(
            recurrence_by_pair[(ord("a"), ord("b"))],
            recurrence_by_pair[(ord("b"), ord("c"))],
        ),
        source_ingest_occurrence_identity=source.identity,
        occurrence_limit=16,
        through=ledger.append_boundary(),
    )
    results = []
    for finding in findings:
        assignment = record_responsibility_assignment_for_measurement_of_recurrent_byte_pair_occurrence_position(
            ledger,
            finding=finding,
            locality_standing=_standing(ledger, locality),
        )
        act = record_evidence_of_act_occurrence_for_measurement_of_recurrent_byte_pair_occurrence_position(
            ledger,
            responsibility_assignment_event_identity=assignment.identity,
            responsibility_assignment_standing=_standing(ledger, locality),
        )
        results.append(
            record_result_of_measurement_of_recurrent_byte_pair_occurrence_position(
                ledger,
                responsible_act_evidence_event_identity=act.identity,
            )
        )
    references = tuple(
        reference
        for result in results
        for reference in references_to_recorded_recurrent_byte_pair_occurrence_positions(
            ledger,
            result_occurrence_identity=result.identity,
        )
    )
    first = next(reference for reference in references if reference.exact_pair == b"ab")
    second_candidates = tuple(
        reference for reference in references if reference.exact_pair == b"bc"
    )
    second = (
        second_candidates[0]
        if current == b"abc"
        else max(second_candidates, key=lambda reference: reference.first_position)
    )
    return ledger, locality, source, first, second


def _assignment(ledger, locality, first, second):
    return record_shared_position_responsibility_assignment(
        ledger,
        first_result_occurrence_identity=first.recorded_occurrence_identity,
        first_assertion_identity=first.assertion_identity,
        second_result_occurrence_identity=second.recorded_occurrence_identity,
        second_assertion_identity=second.assertion_identity,
        locality_standing=_standing(ledger, locality),
    )


def _record_path(ledger, locality, first, second):
    assignment = _assignment(ledger, locality, first, second)
    applicability_act = record_shared_position_applicability_act_evidence(
        ledger,
        assignment_event_identity=assignment.identity,
        locality_standing=_standing(ledger, locality),
    )
    applicability = record_shared_position_applicability_result(
        ledger,
        applicability_act_evidence_event_identity=applicability_act.identity,
    )
    measurement_act = record_shared_position_measurement_act_evidence(
        ledger,
        applicability_result_event_identity=applicability.identity,
        locality_standing=_standing(ledger, locality),
    )
    result = record_shared_position_measurement_result(
        ledger,
        measurement_act_evidence_event_identity=measurement_act.identity,
    )
    return assignment, applicability_act, applicability, measurement_act, result


def _position_coordinate_reference(reference, role):
    position = (
        reference.first_position if role == "first" else reference.second_position
    )
    exact_material = (
        reference.exact_pair[:1] if role == "first" else reference.exact_pair[1:]
    )
    coordinates = {
        "source_ingest_occurrence_identity": (
            reference.source_ingest_occurrence_identity
        ),
        "locality_identity": reference.locality_identity,
        "completeness_boundary_identity": (
            reference.completeness_boundary_identity
        ),
        "position": position,
        "exact_material": list(exact_material),
    }
    return {
        "identity": "source-byte-position-coordinate:"
        + hashlib.sha256(
            json.dumps(
                coordinates, sort_keys=True, separators=(",", ":")
            ).encode("utf-8")
        ).hexdigest(),
        **coordinates,
    }


def test_exact_yielded_pair_relations_compose_at_one_shared_position():
    ledger, locality, source, first, second = _fixture()
    assignment, _applicability_act, applicability, _measurement_act, result = (
        _record_path(ledger, locality, first, second)
    )
    applicability_reading = get_recorded_shared_position_applicability(
        ledger, applicability.identity
    )
    assert applicability.kind == SHARED_POSITION_APPLICABILITY_RESULT_KIND
    assert applicability_reading["applicability"] == "applicable"
    shared_reference = _position_coordinate_reference(first, "second")
    assert applicability_reading["dimensions"]["content"] == {
        "first_relation_second_position_coordinate_reference": shared_reference,
        "second_relation_first_position_coordinate_reference": (
            _position_coordinate_reference(second, "first")
        ),
        "shared_position_coordinate_reference": shared_reference,
    }

    reading = get_recorded_shared_position_measurement(ledger, result.identity)

    assert result.kind == SHARED_POSITION_MEASUREMENT_RESULT_KIND
    assert "standing" not in reading["dimensions"]
    assert "standing" not in reading["responsibility_assignment_evidence"]
    assert reading["responsibility_assignment_reference"] == {
        "recorded_occurrence_identity": assignment.identity,
        "assignment_identity": assignment.material["assignment_identity"],
        "assignment_subject_identity": assignment.material[
            "assignment_subject_identity"
        ],
    }
    assert assignment.identity in _standing(ledger, locality)[
        "responsibility_assignment_occurrences"
    ]
    assert len(reading["assertions"]) == 1
    assertion = reading["assertions"][0]
    assert assertion["result"] == "ordered_relation_path"
    assert "standing" not in assertion["dimensions"]
    content = assertion["dimensions"]["content"]
    assert content["shared_position_coordinate_reference"] == shared_reference
    assert content["source_ingest_occurrence_identity"] == source.identity
    assert assertion["assertion_subject"][
        "first_position_assertion_reference"
    ] == first.assertion_reference
    assert assertion["assertion_subject"][
        "second_position_assertion_reference"
    ] == second.assertion_reference
    assert assertion["input_support"]["assertion_references"] == [
        first.assertion_reference,
        second.assertion_reference,
    ]
    assert reading["authority"] == {
        "source": "this Book",
        "book_clause_identity": "01.Source.D",
        "authority_limit": "bounded",
        "act": (
            "determine one exact shared position-coordinate reference and Yield "
            "one ordered relation path"
        ),
        "negative_authority": (
            "establish no represented relation and no emission"
        ),
    }
    assert reading["authority"] != reading["scope"]
    assert result.exact_material is None
    assert result.identity in _standing(ledger, locality)["measurement_occurrences"]


def test_direct_position_coordinate_assertions_compose_without_recurrence_support(
    monkeypatch,
):
    ledger = EventLedger()
    locality = "direct-pair-position"
    source = ingest_material(
        ledger,
        locality_identity=locality,
        exact_bytes=b"2+2=5\n",
        source_role="exact material",
        source_boundary="exact material boundary",
    )
    direct_assignment = (
        record_byte_pair_occurrence_position_measurement_responsibility_assignment(
            ledger,
            source_ingest_occurrence_identity=source.identity,
            locality_standing=_standing(ledger, locality),
        )
    )
    direct_act = record_byte_pair_occurrence_position_measurement_act_evidence(
        ledger,
        responsibility_assignment_event_identity=direct_assignment.identity,
        responsibility_assignment_standing=_standing(ledger, locality),
    )
    direct_result = record_byte_pair_occurrence_position_measurement_result(
        ledger,
        responsible_act_evidence_event_identity=direct_act.identity,
    )
    references = (
        references_to_recorded_position_coordinates_of_byte_pair_occurrences(
            ledger, direct_result.identity
        )
    )
    first = next(reference for reference in references if reference.exact_pair == b"2+")
    second = next(reference for reference in references if reference.exact_pair == b"+2")
    result_reads = []
    original = direct_position_module._read_result

    def read_once(*args, **kwargs):
        result_reads.append(args[1])
        return original(*args, **kwargs)

    monkeypatch.setattr(direct_position_module, "_read_result", read_once)

    def full_population_is_not_needed(*_args, **_kwargs):
        raise AssertionError("shared position read the full direct reference population")

    monkeypatch.setattr(
        shared_position_module,
        "references_to_recorded_position_coordinates_of_byte_pair_occurrences",
        full_population_is_not_needed,
    )

    assignment, _applicability_act, _applicability, _measurement_act, result = (
        _record_path(ledger, locality, first, second)
    )
    assert result_reads
    assert set(result_reads) == {direct_result.identity}
    reading = get_recorded_shared_position_measurement(ledger, result.identity)

    assert reading["assertions"][0]["dimensions"]["content"][
        "shared_position_coordinate_reference"
    ] == _position_coordinate_reference(first, "second")
    assert assignment.material["first_position_assertion"][
        "support_assertion_references"
    ] == []
    assert assignment.material["second_position_assertion"][
        "support_assertion_references"
    ] == []


def test_distinct_direct_results_resolve_only_their_addressed_assertions(
    monkeypatch,
):
    ledger = EventLedger()
    locality = "distinct-direct-pair-position"
    source = ingest_material(
        ledger,
        locality_identity=locality,
        exact_bytes=b"2+2=5\n",
        source_role="exact material",
        source_boundary="exact material boundary",
    )
    results = []
    references = []
    for exact_pair in (b"2+", b"+2"):
        direct_assignment = (
            record_byte_pair_occurrence_position_measurement_responsibility_assignment(
                ledger,
                source_ingest_occurrence_identity=source.identity,
                locality_standing=_standing(ledger, locality),
            )
        )
        direct_act = record_byte_pair_occurrence_position_measurement_act_evidence(
            ledger,
            responsibility_assignment_event_identity=direct_assignment.identity,
            responsibility_assignment_standing=_standing(ledger, locality),
        )
        direct_result = record_byte_pair_occurrence_position_measurement_result(
            ledger,
            responsible_act_evidence_event_identity=direct_act.identity,
        )
        results.append(direct_result)
        references.append(
            next(
                reference
                for reference in references_to_recorded_position_coordinates_of_byte_pair_occurrences(
                    ledger, direct_result.identity
                )
                if reference.exact_pair == exact_pair
            )
        )

    def full_population_is_not_needed(*_args, **_kwargs):
        raise AssertionError("shared position read the full direct reference population")

    monkeypatch.setattr(
        shared_position_module,
        "references_to_recorded_position_coordinates_of_byte_pair_occurrences",
        full_population_is_not_needed,
    )

    _assignment_event, _applicability_act, _applicability, _measurement_act, result = (
        _record_path(ledger, locality, references[0], references[1])
    )
    reading = get_recorded_shared_position_measurement(ledger, result.identity)

    assert {reference.recorded_occurrence_identity for reference in references} == {
        direct_result.identity for direct_result in results
    }
    assert reading["assertions"][0]["dimensions"]["content"][
        "shared_position_coordinate_reference"
    ] == _position_coordinate_reference(references[0], "second")


def test_later_direct_lifecycle_reads_use_assignment_carried_exact_coordinates(
    monkeypatch,
):
    ledger = EventLedger()
    locality = "carried-direct-pair-position"
    source = ingest_material(
        ledger,
        locality_identity=locality,
        exact_bytes=b"2+2=5\n",
        source_role="exact material",
        source_boundary="exact material boundary",
    )
    direct_assignment = (
        record_byte_pair_occurrence_position_measurement_responsibility_assignment(
            ledger,
            source_ingest_occurrence_identity=source.identity,
            locality_standing=_standing(ledger, locality),
        )
    )
    direct_act = record_byte_pair_occurrence_position_measurement_act_evidence(
        ledger,
        responsibility_assignment_event_identity=direct_assignment.identity,
        responsibility_assignment_standing=_standing(ledger, locality),
    )
    direct_result = record_byte_pair_occurrence_position_measurement_result(
        ledger,
        responsible_act_evidence_event_identity=direct_act.identity,
    )
    direct_references = (
        references_to_recorded_position_coordinates_of_byte_pair_occurrences(
            ledger, direct_result.identity
        )
    )
    first = next(
        reference for reference in direct_references if reference.exact_pair == b"2+"
    )
    second = next(
        reference for reference in direct_references if reference.exact_pair == b"+2"
    )
    assignment = _assignment(ledger, locality, first, second)

    original = (
        shared_position_module.references_to_addressed_recorded_position_coordinates_of_byte_pair_occurrences
    )

    def assertion_scan_is_not_needed(*args, **kwargs):
        if kwargs.get("exact_coordinates") is None:
            raise AssertionError("later lifecycle read scanned assertion identities")
        return original(*args, **kwargs)

    monkeypatch.setattr(
        shared_position_module,
        "references_to_addressed_recorded_position_coordinates_of_byte_pair_occurrences",
        assertion_scan_is_not_needed,
    )
    applicability_act = record_shared_position_applicability_act_evidence(
        ledger,
        assignment_event_identity=assignment.identity,
        locality_standing=_standing(ledger, locality),
    )
    applicability = record_shared_position_applicability_result(
        ledger,
        applicability_act_evidence_event_identity=applicability_act.identity,
    )
    measurement_act = record_shared_position_measurement_act_evidence(
        ledger,
        applicability_result_event_identity=applicability.identity,
        locality_standing=_standing(ledger, locality),
    )
    result = record_shared_position_measurement_result(
        ledger,
        measurement_act_evidence_event_identity=measurement_act.identity,
    )

    assert get_recorded_shared_position_measurement(ledger, result.identity)[
        "assertions"
    ][0]["dimensions"]["content"][
        "shared_position_coordinate_reference"
    ] == _position_coordinate_reference(first, "second")


def test_positions_that_do_not_meet_are_inapplicable_and_cannot_participate():
    ledger, locality, _source, first, second = _fixture(current=b"ab--bc")
    assignment = _assignment(ledger, locality, first, second)
    act = record_shared_position_applicability_act_evidence(
        ledger,
        assignment_event_identity=assignment.identity,
        locality_standing=_standing(ledger, locality),
    )
    result = record_shared_position_applicability_result(
        ledger,
        applicability_act_evidence_event_identity=act.identity,
    )

    assert get_recorded_shared_position_applicability(ledger, result.identity)[
        "applicability"
    ] == "inapplicable"
    with pytest.raises(SharedPairPositionError):
        record_shared_position_measurement_act_evidence(
            ledger,
            applicability_result_event_identity=result.identity,
            locality_standing=_standing(ledger, locality),
        )


def test_one_act_cannot_yield_two_shared_position_results():
    ledger, locality, _source, first, second = _fixture()
    assignment = _assignment(ledger, locality, first, second)
    act = record_shared_position_applicability_act_evidence(
        ledger,
        assignment_event_identity=assignment.identity,
        locality_standing=_standing(ledger, locality),
    )
    record_shared_position_applicability_result(
        ledger,
        applicability_act_evidence_event_identity=act.identity,
    )

    with pytest.raises(SharedPairPositionError):
        record_shared_position_applicability_result(
            ledger,
            applicability_act_evidence_event_identity=act.identity,
        )


def test_aggregate_pair_findings_cannot_impersonate_occurrence_bound_positions():
    ledger, locality, _source, first, second = _fixture()

    with pytest.raises(ValueError):
        record_shared_position_responsibility_assignment(
            ledger,
            first_result_occurrence_identity=(
                first.pair_measurement_occurrence_identity
            ),
            first_assertion_identity=first.recurrence_assertion_identity,
            second_result_occurrence_identity=(
                second.recorded_occurrence_identity
            ),
            second_assertion_identity=second.assertion_identity,
            locality_standing=_standing(ledger, locality),
        )


def test_each_new_elevator_crossing_is_read_from_its_exact_occurrences():
    ledger, locality, _source, first, second = _fixture()
    assignment, applicability_act, applicability, measurement_act, result = (
        _record_path(ledger, locality, first, second)
    )
    crossings = (
        (
            assignment,
            lambda: get_shared_position_responsibility_assignment(
                ledger, assignment.identity
            ),
        ),
        (
            applicability_act,
            lambda: get_shared_position_applicability_act_evidence(
                ledger,
                applicability_act.identity,
            ),
        ),
        (
            applicability,
            lambda: get_recorded_shared_position_applicability(
                ledger, applicability.identity
            ),
        ),
        (
            measurement_act,
            lambda: get_shared_position_measurement_act_evidence(
                ledger, measurement_act.identity
            ),
        ),
        (
            result,
            lambda: get_recorded_shared_position_measurement(
                ledger, result.identity
            ),
        ),
    )
    for event, read in crossings:
        event.material["changed_after_recording"] = True
        with pytest.raises((SharedPairPositionError, ValueError)):
            read()
        del event.material["changed_after_recording"]


def test_each_shared_position_lifecycle_read_validates_inputs_once_without_cache(
    monkeypatch,
):
    ledger, locality, _source, first, second = _fixture()
    assignment = _assignment(ledger, locality, first, second)
    applicability_act = record_shared_position_applicability_act_evidence(
        ledger,
        assignment_event_identity=assignment.identity,
        locality_standing=_standing(ledger, locality),
    )
    applicability = record_shared_position_applicability_result(
        ledger,
        applicability_act_evidence_event_identity=applicability_act.identity,
    )
    standing = _standing(ledger, locality)
    original = shared_position_module._inputs
    calls = []

    def counted(ledger, **identities):
        calls.append(tuple(identities.values()))
        return original(ledger, **identities)

    monkeypatch.setattr(shared_position_module, "_inputs", counted)
    expected_call = (
        first.recorded_occurrence_identity,
        first.assertion_identity,
        second.recorded_occurrence_identity,
        second.assertion_identity,
    )

    measurement_act = record_shared_position_measurement_act_evidence(
        ledger,
        applicability_result_event_identity=applicability.identity,
        locality_standing=standing,
    )
    assert calls == [expected_call]

    result = record_shared_position_measurement_result(
        ledger,
        measurement_act_evidence_event_identity=measurement_act.identity,
    )
    assert calls == [expected_call] * 2

    get_shared_position_measurement_act_evidence(ledger, measurement_act.identity)
    assert calls == [expected_call] * 3

    get_recorded_shared_position_measurement(ledger, result.identity)
    assert calls == [expected_call] * 4

    get_recorded_shared_position_measurement(ledger, result.identity)
    assert calls == [expected_call] * 5


def test_corrupted_shared_position_yield_relations_are_refused():
    ledger, locality, _source, first, second = _fixture()
    _assignment_event, _applicability_act, applicability, _measurement_act, result = (
        _record_path(ledger, locality, first, second)
    )
    crossings = (
        (applicability, get_recorded_shared_position_applicability),
        (result, get_recorded_shared_position_measurement),
    )

    for event, read in crossings:
        evidence = ledger.get(event.material["evidence_of_yield_relation_identity"])
        assert evidence is not None
        result_identity = evidence.material["result_identity"]
        evidence.material["result_identity"] = "crossed-result"
        with pytest.raises(SharedPairPositionError):
            read(ledger, event.identity)
        evidence.material["result_identity"] = result_identity


def test_shared_position_result_survives_sqlite_restart(tmp_path):
    database = tmp_path / "shared-position.sqlite"
    ledger = SQLiteEventLedger(str(database))
    ledger, locality, _source, first, second = _fixture(ledger=ledger)
    _assignment_event, _applicability_act, _applicability, _measurement_act, result = (
        _record_path(ledger, locality, first, second)
    )
    result_identity = result.identity
    ledger.close()

    reopened = SQLiteEventLedger(str(database))
    reading = get_recorded_shared_position_measurement(
        reopened, result_identity
    )

    assert reading["assertions"][0]["result"] == "ordered_relation_path"
    assert result_identity in _standing(reopened, locality)[
        "measurement_occurrences"
    ]
    reopened.close()


def test_incremental_standing_matches_replay_for_the_whole_new_elevator():
    ledger, locality, _source, first, second = _fixture()
    prior = _standing(ledger, locality)
    prior_count = len(ledger.list_locality(locality))
    _record_path(ledger, locality, first, second)
    later = tuple(
        event.identity for event in ledger.list_locality(locality)[prior_count:]
    )

    incremental = advance_operator_locality_standing(
        ledger,
        later,
        locality_identity=locality,
        prior=prior,
    )

    assert incremental == _standing(ledger, locality)


def test_structured_path_can_be_addressed_but_is_not_raw_emission_material():
    ledger, locality, _source, first, second = _fixture()
    _assignment_event, _applicability_act, _applicability, _measurement_act, result = (
        _record_path(ledger, locality, first, second)
    )
    representation = record_operator_representation(
        ledger,
        locality_identity=locality,
        locality_standing=_standing(ledger, locality),
        source_occurrence_reference=result.identity,
    )
    recorded = ledger.get(representation["representation_event_identity"])

    reading = read_operator_representation(ledger, recorded.identity)
    assert reading["representation_event_identity"] == recorded.identity
    assert reading["source_occurrence_reference"] == result.identity
    assert recorded.exact_material is None
    assert "representation_rule" not in recorded.material


FIDELITY_SUBJECTS = {
    "applicability_determination": (
        test_positions_that_do_not_meet_are_inapplicable_and_cannot_participate,
    ),
    "yield_result_occurrence_evidence": (
        test_one_act_cannot_yield_two_shared_position_results,
        test_each_new_elevator_crossing_is_read_from_its_exact_occurrences,
        test_each_shared_position_lifecycle_read_validates_inputs_once_without_cache,
        test_distinct_direct_results_resolve_only_their_addressed_assertions,
        test_later_direct_lifecycle_reads_use_assignment_carried_exact_coordinates,
        test_corrupted_shared_position_yield_relations_are_refused,
    ),
    "declared_measurement_result": (
        test_exact_yielded_pair_relations_compose_at_one_shared_position,
        test_direct_position_coordinate_assertions_compose_without_recurrence_support,
        test_aggregate_pair_findings_cannot_impersonate_occurrence_bound_positions,
        test_shared_position_result_survives_sqlite_restart,
        test_incremental_standing_matches_replay_for_the_whole_new_elevator,
    ),
    "representation_source_coordinates": (
        test_structured_path_can_be_addressed_but_is_not_raw_emission_material,
    ),
}
