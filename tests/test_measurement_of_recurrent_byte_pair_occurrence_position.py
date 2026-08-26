from __future__ import annotations

from copy import deepcopy
import json

import pytest

import seed_runtime.measurement_of_recurrent_byte_pair_occurrence_position as pair_occurrence_measurement
import seed_runtime.operator_locality_standing as operator_standing
from seed_runtime.byte_measurement import (
    record_byte_measurement_subject_to_act_binding,
    assertions_of_recorded_byte_position_pair_measurement,
    record_byte_measurement_act_occurrence,
    record_byte_measurement_result,
    record_byte_position_pair_count_layer,
)
from seed_runtime.events import EventLedger, EventLedgerBoundary, SQLiteEventLedger
from tests.operator_material_source_test_witness import (
    record_operator_material_occurrence,
)
from seed_runtime.measurement_of_recurrent_byte_pair_occurrence_position import (
    RECORDED_RESPONSIBILITY_ASSIGNMENT_OF_MEASUREMENT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_KIND,
    RECORDED_ACT_OCCURRENCE_OF_MEASUREMENT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_EVENT,
    RECORDING_OCCURRENCE_OF_RESULT_OF_MEASUREMENT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_KIND,
    get_responsibility_assignment_for_measurement_of_recurrent_byte_pair_occurrence_position,
    get_recorded_result_of_measurement_of_recurrent_byte_pair_occurrence_position,
    measure_positions_of_recurrent_byte_pair_occurrences,
    measure_positions_for_recurrent_byte_pair_assertions,
    references_to_recorded_recurrent_byte_pair_occurrence_positions,
    record_responsibility_assignment_for_measurement_of_recurrent_byte_pair_occurrence_position,
    record_act_occurrence_for_measurement_of_recurrent_byte_pair_occurrence_position,
    record_result_of_measurement_of_recurrent_byte_pair_occurrence_position,
)
from seed_runtime.operator_locality_standing import (
    _operator_standing_replay_validation,
    _operator_standing_validation_context,
    _set_operator_standing_validation_context,
    read_operator_locality_standing,
)
from seed_runtime.occurrence_position_measurement import (
    measure_occurrence_position,
    record_occurrence_position_measurement_responsibility_assignment,
)
from seed_runtime.yield_relation import read_requirements_of_yield_relation


def _fixture(
    *,
    current: bytes = b"ba---ab",
    premise: bytes = b"abxxab",
    ledger=None,
):
    ledger = ledger or EventLedger()
    locality = "pair-occurrence-measurement"
    record_operator_material_occurrence(
        ledger,
        locality_identity=locality,
        exact=premise,
        source_boundary="exact premise boundary",
    )
    byte_assignment = record_byte_measurement_subject_to_act_binding(
        ledger,
        source_localities=(locality,),
        recording_locality_identity=locality,
        current_coordinates=read_operator_locality_standing(
            ledger, locality_identity=locality
        ),
    )
    byte_act = record_byte_measurement_act_occurrence(
        ledger,
        subject_to_act_binding_event_identity=byte_assignment.identity,
        current_coordinates=read_operator_locality_standing(
            ledger, locality_identity=locality
        ),
    )
    byte = record_byte_measurement_result(
        ledger,
        act_occurrence_event_identity=byte_act.identity,
    )
    pair = record_byte_position_pair_count_layer(
        ledger,
        source_measurement_event_identity=byte.identity,
        recording_locality_identity=locality,
    )
    pair_assertions = assertions_of_recorded_byte_position_pair_measurement(
        ledger, pair.identity
    )
    recurrence = next(
        assertion
        for assertion in pair_assertions or ()
        if assertion.result == "recurrence"
        and assertion.content == (ord("a"), ord("b"))
    )
    source = record_operator_material_occurrence(
        ledger,
        locality_identity=locality,
        exact=current,
        source_boundary="later exact material boundary",
    )
    finding = measure_positions_of_recurrent_byte_pair_occurrences(
        ledger,
        pair_measurement_occurrence_identity=pair.identity,
        recurrence_assertion_position=recurrence.assertion_position,
        source_material_result_occurrence_identity=source.identity,
        occurrence_count_boundary=16,
    )
    return ledger, locality, pair, recurrence, source, finding


def _record(ledger, locality, finding):
    assignment = record_responsibility_assignment_for_measurement_of_recurrent_byte_pair_occurrence_position(
        ledger,
        finding=finding,
        locality_standing=read_operator_locality_standing(
            ledger, locality_identity=locality
        ),
    )
    act = record_act_occurrence_for_measurement_of_recurrent_byte_pair_occurrence_position(
        ledger,
        responsibility_assignment_event_identity=assignment.identity,
        responsibility_assignment_standing=read_operator_locality_standing(
            ledger, locality_identity=locality
        ),
    )
    result = record_result_of_measurement_of_recurrent_byte_pair_occurrence_position(
        ledger,
        act_occurrence_event_identity=act.identity,
    )
    return act, result


def test_pair_occurrence_measurement_finds_exact_positions_without_a_sign():
    ledger, locality, _pair, _recurrence, _source, finding = _fixture()

    assert finding.occurrences == ((1, 0), (1, 6), (5, 0), (5, 6))
    assert finding.available_occurrence_count == 4
    assert {
        "before" if second < first else "after"
        for first, second in finding.occurrences
    } == {"before", "after"}
    assert {abs(second - first) for first, second in finding.occurrences} == {
        1,
        5,
    }


def test_pair_occurrence_measurement_yield_preserves_the_exact_finding():
    ledger, locality, _pair, _recurrence, _source, finding = _fixture()

    act, result = _record(ledger, locality, finding)
    read = get_recorded_result_of_measurement_of_recurrent_byte_pair_occurrence_position(ledger, result.identity)

    assert act.kind == RECORDED_ACT_OCCURRENCE_OF_MEASUREMENT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_EVENT
    assert result.kind == RECORDING_OCCURRENCE_OF_RESULT_OF_MEASUREMENT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_KIND
    assert read == finding
    assert result.exact_material is None
    requirements = read_requirements_of_yield_relation(
        ledger,
        recorded_result_event_identity=result.identity,
        yield_relation_event_identity=result.material["yield_relation_identity"],
        act_occurrence_event_identity=act.identity,
    )
    assert requirements == {
        "exact_relation": True,
        "occurrence_witness": True,
        "intact_occurrence": True,
    }
    assert all(
        set(assertion["dimensions"]["content"])
        == {"first_position", "second_position", "completeness_boundary"}
        for assertion in result.material["assertions"]
    )
    assert "standing" not in result.material["dimensions"]
    assert all(
        "standing" not in assertion["dimensions"]
        for assertion in result.material["assertions"]
    )
    serialized = json.dumps(result.material).lower()
    assert "direction" not in serialized
    assert "displacement" not in serialized


def test_exact_assignment_enters_current_standing_and_owns_distinct_lifecycle_identities():
    ledger, locality, _pair, _recurrence, _source, finding = _fixture()
    assignment = record_responsibility_assignment_for_measurement_of_recurrent_byte_pair_occurrence_position(
        ledger,
        finding=finding,
        locality_standing=read_operator_locality_standing(
            ledger, locality_identity=locality
        ),
    )
    current_coordinates = read_operator_locality_standing(
        ledger, locality_identity=locality
    )

    assert assignment.kind == RECORDED_RESPONSIBILITY_ASSIGNMENT_OF_MEASUREMENT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_KIND
    assert get_responsibility_assignment_for_measurement_of_recurrent_byte_pair_occurrence_position(
        ledger, assignment.identity
    ) == assignment
    assert current_coordinates["subject_to_act_binding_occurrences"][
        assignment.identity
    ] is None
    assert "standing" not in assignment.material

    act = record_act_occurrence_for_measurement_of_recurrent_byte_pair_occurrence_position(
        ledger,
        responsibility_assignment_event_identity=assignment.identity,
        responsibility_assignment_standing=current_coordinates,
    )
    result = record_result_of_measurement_of_recurrent_byte_pair_occurrence_position(
        ledger,
        act_occurrence_event_identity=act.identity,
    )
    yield_relation = ledger.get(result.material["yield_relation_identity"])
    identities = {
        assignment.identity,
        assignment.material["measurement_act_identity"],
        assignment.material["act_occurrence_identity"],
        assignment.material["measurement_result_identity"],
        act.identity,
        yield_relation.identity,
        result.identity,
    }
    assert len(identities) == 7
    assert act.material["responsibility_assignment_reference"] == {
        "recorded_occurrence_identity": assignment.identity,
        "book_clause_identity": assignment.material["book_clause_identity"],
        "exact_act_identity": assignment.material["exact_act_identity"],
        "subject_reference": assignment.material["subject_reference"],
        "result_boundary_identity": assignment.material[
            "result_boundary_identity"
        ],
    }
    assert result.material["responsibility_assignment_reference"] == act.material[
        "responsibility_assignment_reference"
    ]


def test_stale_standing_cannot_authorize_the_assigned_measurement_act():
    ledger, locality, _pair, _recurrence, _source, finding = _fixture()
    stale = read_operator_locality_standing(
        ledger, locality_identity=locality
    )
    assignment = record_responsibility_assignment_for_measurement_of_recurrent_byte_pair_occurrence_position(
        ledger,
        finding=finding,
        locality_standing=stale,
    )

    with pytest.raises(ValueError, match="exact current Locality Standing"):
        record_act_occurrence_for_measurement_of_recurrent_byte_pair_occurrence_position(
            ledger,
            responsibility_assignment_event_identity=assignment.identity,
            responsibility_assignment_standing=stale,
        )


def test_shaped_standing_without_the_exact_assignment_cannot_authorize_the_act():
    ledger, locality, _pair, _recurrence, _source, finding = _fixture()
    assignment = record_responsibility_assignment_for_measurement_of_recurrent_byte_pair_occurrence_position(
        ledger,
        finding=finding,
        locality_standing=read_operator_locality_standing(
            ledger, locality_identity=locality
        ),
    )
    shaped = deepcopy(
        read_operator_locality_standing(ledger, locality_identity=locality)
    )
    shaped["subject_to_act_binding_occurrences"] = {
        "same-shape-assignment": None
    }

    with pytest.raises(ValueError, match="exact current Locality Standing"):
        record_act_occurrence_for_measurement_of_recurrent_byte_pair_occurrence_position(
            ledger,
            responsibility_assignment_event_identity=assignment.identity,
            responsibility_assignment_standing=shaped,
        )


def test_corrupted_assignment_occurrence_cannot_authorize_the_act():
    ledger, locality, _pair, _recurrence, _source, finding = _fixture()
    assignment = record_responsibility_assignment_for_measurement_of_recurrent_byte_pair_occurrence_position(
        ledger,
        finding=finding,
        locality_standing=read_operator_locality_standing(
            ledger, locality_identity=locality
        ),
    )
    assignment.material["occurrence_count_boundary"] += 1

    with pytest.raises(ValueError, match="coordinates are not exact"):
        get_responsibility_assignment_for_measurement_of_recurrent_byte_pair_occurrence_position(
            ledger, assignment.identity
        )


def test_assignment_read_refuses_a_corrupted_unrelated_prior_standing_carrier():
    ledger, locality, _pair, _recurrence, _source, finding = _fixture()
    occurrence_finding = measure_occurrence_position(
        ledger, source_locality_identity=locality
    )
    unrelated = record_occurrence_position_measurement_responsibility_assignment(
        ledger,
        recording_locality_identity=locality,
        finding=occurrence_finding,
        locality_standing=read_operator_locality_standing(
            ledger, locality_identity=locality
        ),
    )
    assignment = record_responsibility_assignment_for_measurement_of_recurrent_byte_pair_occurrence_position(
        ledger,
        finding=finding,
        locality_standing=read_operator_locality_standing(
            ledger, locality_identity=locality
        ),
    )
    unrelated.material["responsibility"] = "corrupted unrelated Responsibility"

    with pytest.raises(ValueError, match="coordinates are not exact"):
        read_operator_locality_standing(ledger, locality_identity=locality)
    with pytest.raises(ValueError, match="coordinates are not exact"):
        get_responsibility_assignment_for_measurement_of_recurrent_byte_pair_occurrence_position(
            ledger, assignment.identity
        )


def test_replay_validation_context_refuses_unbound_accumulators_and_clears():
    ledger, locality, _pair, _recurrence, _source, _finding = _fixture()
    current_coordinates = read_operator_locality_standing(
        ledger, locality_identity=locality
    )

    @_operator_standing_replay_validation
    def outer():
        with pytest.raises(ValueError, match="exact accumulators"):
            _set_operator_standing_validation_context(
                ledger,
                locality_identity=locality,
                through_event_occurrence_identity=current_coordinates[
                    "through_event_occurrence_identity"
                ],
                measurement_occurrences=current_coordinates["measurement_occurrences"],
                material_result_occurrences=current_coordinates["material_result_occurrences"],
                subject_to_act_binding_occurrences=current_coordinates[
                    "subject_to_act_binding_occurrences"
                ],
            )
        assert _operator_standing_validation_context(
            ledger, locality_identity=locality
        ) is None
        raise RuntimeError("exercise replay-context cleanup")

    with pytest.raises(RuntimeError, match="cleanup"):
        outer()
    assert _operator_standing_validation_context(
        ledger, locality_identity=locality
    ) is None


def test_replay_context_before_the_recorded_assignment_boundary_is_refused():
    ledger, locality, pair, _recurrence, _source, finding = _fixture()
    standing = read_operator_locality_standing(
        ledger, locality_identity=locality
    )
    assignment = record_responsibility_assignment_for_measurement_of_recurrent_byte_pair_occurrence_position(
        ledger,
        finding=finding,
        locality_standing=standing,
    )

    @_operator_standing_replay_validation
    def read_from_false_earlier_context():
        _set_operator_standing_validation_context(
            ledger,
            locality_identity=locality,
            through_event_occurrence_identity=pair.identity,
            measurement_occurrences=standing["measurement_occurrences"],
            material_result_occurrences=standing["material_result_occurrences"],
            subject_to_act_binding_occurrences={
                **standing["subject_to_act_binding_occurrences"],
                assignment.identity: None,
            },
        )
        return get_responsibility_assignment_for_measurement_of_recurrent_byte_pair_occurrence_position(
            ledger, assignment.identity
        )

    with pytest.raises(ValueError, match="exact accumulators"):
        read_from_false_earlier_context()


@pytest.mark.parametrize("forged_coordinate", ["measurement", "acquisition_result"])
@pytest.mark.parametrize("mutation", ["extra", "missing", "changed"])
def test_replay_context_refuses_forged_exact_boundary_input_coordinates(
    forged_coordinate, mutation,
):
    ledger, locality, pair, _recurrence, source, finding = _fixture()
    standing = read_operator_locality_standing(
        ledger, locality_identity=locality
    )
    assignment = record_responsibility_assignment_for_measurement_of_recurrent_byte_pair_occurrence_position(
        ledger,
        finding=finding,
        locality_standing=standing,
    )

    @_operator_standing_replay_validation
    def read_from_context(measurements, acquisition_results):
        _set_operator_standing_validation_context(
            ledger,
            locality_identity=locality,
            through_event_occurrence_identity=assignment.material[
                "standing_boundary_identity"
            ],
            measurement_occurrences=measurements,
            material_result_occurrences=acquisition_results,
            subject_to_act_binding_occurrences=standing[
                "subject_to_act_binding_occurrences"
            ],
        )
        return get_responsibility_assignment_for_measurement_of_recurrent_byte_pair_occurrence_position(
            ledger, assignment.identity
        )

    measurements = deepcopy(standing["measurement_occurrences"])
    acquisition_results = deepcopy(standing["material_result_occurrences"])
    coordinate = (
        measurements[pair.identity]
        if forged_coordinate == "measurement"
        else next(
            occurrence
            for occurrence in acquisition_results
                if occurrence.get("result_occurrence_identity") == source.identity
        )
    )
    key = (
        "result_identity"
        if forged_coordinate == "measurement"
        else "subject_reference"
    )
    if mutation == "extra":
        coordinate["forged"] = True
    elif mutation == "missing":
        coordinate.pop(key)
    else:
        coordinate[key] += "-forged"

    with pytest.raises(ValueError, match="exact accumulators"):
        read_from_context(measurements, acquisition_results)


def test_assignment_act_and_result_survive_distinct_durable_restarts(tmp_path):
    database = tmp_path / "recurrent-pair-position.sqlite"
    ledger = SQLiteEventLedger(database)
    ledger, locality, _pair, _recurrence, _source, finding = _fixture(
        ledger=ledger
    )
    assignment = record_responsibility_assignment_for_measurement_of_recurrent_byte_pair_occurrence_position(
        ledger,
        finding=finding,
        locality_standing=read_operator_locality_standing(
            ledger, locality_identity=locality
        ),
    )
    ledger.close()

    ledger = SQLiteEventLedger(database)
    assert get_responsibility_assignment_for_measurement_of_recurrent_byte_pair_occurrence_position(
        ledger, assignment.identity
    ).identity == assignment.identity
    act = record_act_occurrence_for_measurement_of_recurrent_byte_pair_occurrence_position(
        ledger,
        responsibility_assignment_event_identity=assignment.identity,
        responsibility_assignment_standing=read_operator_locality_standing(
            ledger, locality_identity=locality
        ),
    )
    ledger.close()

    ledger = SQLiteEventLedger(database)
    result = record_result_of_measurement_of_recurrent_byte_pair_occurrence_position(
        ledger,
        act_occurrence_event_identity=act.identity,
    )
    ledger.close()

    ledger = SQLiteEventLedger(database)
    assert get_recorded_result_of_measurement_of_recurrent_byte_pair_occurrence_position(
        ledger, result.identity
    ) == finding
    ledger.close()


def test_each_pair_position_assertion_has_one_exact_occurrence_bound_reference():
    ledger, locality, pair, recurrence, source, finding = _fixture()
    _act, result = _record(ledger, locality, finding)

    references = references_to_recorded_recurrent_byte_pair_occurrence_positions(
        ledger,
        result_occurrence_identity=result.identity,
    )

    assert tuple(
        reference.assertion_position for reference in references
    ) == tuple(
        assertion["dimensions"]["position"]
        for assertion in result.material["assertions"]
    )
    assert tuple(
        (reference.first_position, reference.second_position)
        for reference in references
    ) == finding.occurrences
    assert {
        (
            reference.recorded_occurrence_identity,
            reference.pair_measurement_occurrence_identity,
            reference.recurrence_assertion_position,
            reference.count_assertion_position,
            reference.source_material_result_occurrence_identity,
            reference.locality_identity,
            reference.completeness_boundary_identity,
            reference.exact_pair,
        )
        for reference in references
    } == {
        (
            result.identity,
            pair.identity,
            recurrence.assertion_position,
            recurrence.support_assertion_references[0]["assertion_position"],
            source.identity,
            locality,
            finding.completeness_boundary.identity,
            b"ab",
        )
    }
    assert all(
        reference.assertion_reference
        == {
            "recorded_occurrence_identity": result.identity,
            "assertion_position": reference.assertion_position,
        }
        for reference in references
    )


def test_assignment_read_threads_one_exact_standing_to_pair_validation(monkeypatch):
    ledger, locality, pair, _recurrence, _source, finding = _fixture()
    prior_standing = read_operator_locality_standing(
        ledger, locality_identity=locality
    )
    assignment = record_responsibility_assignment_for_measurement_of_recurrent_byte_pair_occurrence_position(
        ledger,
        finding=finding,
        locality_standing=prior_standing,
    )
    pair_reads = []
    original = (
        pair_occurrence_measurement._validated_recorded_byte_position_pair_measurement
    )

    def witnessed(
        ledger,
        event_identity,
        *,
        findings_only,
        prior_standing=None,
    ):
        pair_reads.append((event_identity, prior_standing))
        return original(
            ledger,
            event_identity,
            findings_only=findings_only,
            prior_standing=prior_standing,
        )

    monkeypatch.setattr(
        pair_occurrence_measurement,
        "_validated_recorded_byte_position_pair_measurement",
        witnessed,
    )

    ambient_standing = deepcopy(prior_standing)

    def ambient_must_not_override_explicit_standing(*_args, **_kwargs):
        return ambient_standing

    monkeypatch.setattr(
        operator_standing,
        "_operator_standing_validation_context",
        ambient_must_not_override_explicit_standing,
    )
    read_assignment, read_finding = pair_occurrence_measurement._read_responsibility_assignment_for_measurement_of_recurrent_byte_pair_occurrence_position(
        ledger,
        assignment.identity,
        prior_standing=prior_standing,
    )

    assert read_assignment == assignment
    assert read_finding == finding
    assert pair_reads == [(pair.identity, prior_standing)]
    assert _operator_standing_validation_context(
        ledger, locality_identity=locality
    ) is None


@pytest.mark.parametrize("changed_input", ("measurement", "acquisition_result"))
def test_explicit_prior_standing_binds_each_exact_input_occurrence(changed_input):
    ledger, locality, pair, _recurrence, source, finding = _fixture()
    prior_standing = read_operator_locality_standing(
        ledger, locality_identity=locality
    )
    assignment = record_responsibility_assignment_for_measurement_of_recurrent_byte_pair_occurrence_position(
        ledger,
        finding=finding,
        locality_standing=prior_standing,
    )
    forged = deepcopy(prior_standing)
    if changed_input == "measurement":
        forged["measurement_occurrences"][pair.identity][
            "result_identity"
        ] = "substituted-result"
    else:
        carried = next(
            occurrence
            for occurrence in forged["material_result_occurrences"]
            if occurrence["result_occurrence_identity"] == source.identity
        )
        carried["result_identity"] = "substituted-result"

    with pytest.raises(ValueError, match="no exact prior Standing"):
        pair_occurrence_measurement._read_responsibility_assignment_for_measurement_of_recurrent_byte_pair_occurrence_position(
            ledger,
            assignment.identity,
            prior_standing=forged,
        )


def test_assignment_pair_handoff_still_refuses_later_pair_corruption():
    ledger, locality, pair, _recurrence, _source, finding = _fixture()
    prior_standing = read_operator_locality_standing(
        ledger, locality_identity=locality
    )
    assignment = record_responsibility_assignment_for_measurement_of_recurrent_byte_pair_occurrence_position(
        ledger,
        finding=finding,
        locality_standing=prior_standing,
    )
    pair.material["assertions"][0]["dimensions"]["content"] = {
        "crossed": True
    }

    with pytest.raises(ValueError):
        pair_occurrence_measurement._read_responsibility_assignment_for_measurement_of_recurrent_byte_pair_occurrence_position(
            ledger,
            assignment.identity,
            prior_standing=prior_standing,
        )


def test_public_assignment_read_still_reconstructs_prior_standing(monkeypatch):
    ledger, locality, _pair, _recurrence, _source, finding = _fixture()
    prior_standing = read_operator_locality_standing(
        ledger, locality_identity=locality
    )
    assignment = record_responsibility_assignment_for_measurement_of_recurrent_byte_pair_occurrence_position(
        ledger,
        finding=finding,
        locality_standing=prior_standing,
    )
    standing_reads = []
    original = operator_standing.read_operator_locality_standing_through

    def witnessed(
        ledger,
        *,
        locality_identity,
        through_event_occurrence_identity,
    ):
        standing_reads.append(
            (locality_identity, through_event_occurrence_identity)
        )
        return original(
            ledger,
            locality_identity=locality_identity,
            through_event_occurrence_identity=through_event_occurrence_identity,
        )

    monkeypatch.setattr(
        operator_standing, "read_operator_locality_standing_through", witnessed
    )

    assert get_responsibility_assignment_for_measurement_of_recurrent_byte_pair_occurrence_position(
        ledger, assignment.identity
    ) == assignment
    assert (
        locality,
        assignment.material["standing_boundary_identity"],
    ) in standing_reads
    assert all(
        (
            read_locality == locality
            and type(read_boundary) is str
            and read_boundary
        )
        for read_locality, read_boundary in standing_reads
    )


def test_one_same_boundary_pair_subject_set_requires_exact_distinct_recurrence_subjects():
    ledger, _locality, pair, recurrence, source, _finding = _fixture()
    through = ledger.append_boundary()

    class TupleSubclass(tuple):
        pass

    class BoundarySubclass(EventLedgerBoundary):
        pass

    for supplied in ([recurrence.assertion_position], TupleSubclass((recurrence.assertion_position,))):
        with pytest.raises(ValueError, match="exact Assertion positions"):
            measure_positions_for_recurrent_byte_pair_assertions(
                ledger,
                pair_measurement_occurrence_identity=pair.identity,
                recurrence_assertion_positions=supplied,
                source_material_result_occurrence_identity=source.identity,
                occurrence_count_boundary=16,
                through=through,
            )
    with pytest.raises(ValueError, match="entered one result twice"):
        measure_positions_for_recurrent_byte_pair_assertions(
            ledger,
            pair_measurement_occurrence_identity=pair.identity,
            recurrence_assertion_positions=(
                recurrence.assertion_position,
                recurrence.assertion_position,
            ),
            source_material_result_occurrence_identity=source.identity,
            occurrence_count_boundary=16,
            through=through,
        )
    count_position = recurrence.support_assertion_references[0][
        "assertion_position"
    ]
    with pytest.raises(ValueError, match="does not establish recurrence"):
        measure_positions_for_recurrent_byte_pair_assertions(
            ledger,
            pair_measurement_occurrence_identity=pair.identity,
            recurrence_assertion_positions=(count_position,),
            source_material_result_occurrence_identity=source.identity,
            occurrence_count_boundary=16,
            through=through,
        )
    with pytest.raises(TypeError, match="one exact boundary"):
        measure_positions_for_recurrent_byte_pair_assertions(
            ledger,
            pair_measurement_occurrence_identity=pair.identity,
            recurrence_assertion_positions=(recurrence.assertion_position,),
            source_material_result_occurrence_identity=source.identity,
            occurrence_count_boundary=16,
            through=BoundarySubclass(through.identity),
        )
    with pytest.raises(ValueError, match="outside its exact boundary"):
        measure_positions_for_recurrent_byte_pair_assertions(
            ledger,
            pair_measurement_occurrence_identity=pair.identity,
            recurrence_assertion_positions=(recurrence.assertion_position,),
            source_material_result_occurrence_identity=source.identity,
            occurrence_count_boundary=16,
            through=ledger.append_boundary_through_occurrence(pair.identity),
        )


def test_same_boundary_pair_subjects_keep_each_yield_relation_distinct():
    ledger, locality, pair, _recurrence, source, _finding = _fixture(
        premise=b"abxxabyybayyba",
        current=b"ba---abxx--yy",
    )
    recurrence_positions = tuple(
        assertion.assertion_position
        for assertion in assertions_of_recorded_byte_position_pair_measurement(
            ledger, pair.identity
        ) or ()
        if assertion.result == "recurrence"
    )
    findings = measure_positions_for_recurrent_byte_pair_assertions(
        ledger,
        pair_measurement_occurrence_identity=pair.identity,
        recurrence_assertion_positions=recurrence_positions,
        source_material_result_occurrence_identity=source.identity,
        occurrence_count_boundary=16,
        through=ledger.append_boundary(),
    )
    results = tuple(_record(ledger, locality, finding)[1] for finding in findings)

    results[-1].material["assertions"][0]["dimensions"]["content"][
        "first_position"
    ] += 1
    assert (
        get_recorded_result_of_measurement_of_recurrent_byte_pair_occurrence_position(
            ledger, results[0].identity
        )
        == findings[0]
    )
    with pytest.raises(ValueError):
        get_recorded_result_of_measurement_of_recurrent_byte_pair_occurrence_position(
            ledger, results[-1].identity
        )


def test_act_occurrence_has_inputs_and_responsibility_but_no_result_finding():
    ledger, locality, _pair, _recurrence, _source, finding = _fixture()
    assignment = record_responsibility_assignment_for_measurement_of_recurrent_byte_pair_occurrence_position(
        ledger,
        finding=finding,
        locality_standing=read_operator_locality_standing(
            ledger, locality_identity=locality
        ),
    )
    act = record_act_occurrence_for_measurement_of_recurrent_byte_pair_occurrence_position(
        ledger,
        responsibility_assignment_event_identity=assignment.identity,
        responsibility_assignment_standing=read_operator_locality_standing(
            ledger, locality_identity=locality
        ),
    )

    assert {
        item["role"] for item in act.material["participation"]
    } == {
        "Yield-carried recurrent byte-pair subject",
        "exact material result input",
    }
    assert not {
        "assertions",
        "available_occurrence_count",
        "known_loss",
        "result_identity",
    } & set(act.material)


def test_occurrence_count_boundary_is_explicit_and_preserves_exact_known_loss():
    ledger, locality, pair, recurrence, source, _finding = _fixture()
    finding = measure_positions_of_recurrent_byte_pair_occurrences(
        ledger,
        pair_measurement_occurrence_identity=pair.identity,
        recurrence_assertion_position=recurrence.assertion_position,
        source_material_result_occurrence_identity=source.identity,
        occurrence_count_boundary=2,
    )
    _act, result = _record(ledger, locality, finding)

    assert finding.occurrences == ((1, 0), (1, 6))
    assert finding.available_occurrence_count == 4
    assert result.material["occurrence_count_boundary"] == 2
    assert result.material["known_loss"] == [
        "pair occurrences beyond the exact occurrence count boundary are not carried"
    ]


def test_pair_occurrence_result_enters_standing_as_one_exact_measurement_reference():
    ledger, locality, _pair, _recurrence, _source, finding = _fixture()
    act, result = _record(ledger, locality, finding)
    standing = read_operator_locality_standing(
        ledger, locality_identity=locality
    )

    assert standing["measurement_occurrences"][result.identity] == {
        "recorded_occurrence_identity": result.identity,
        "result_identity": result.material["result_identity"],
        "act_occurrence_identity": result.material["act_occurrence_identity"],
        "act_occurrence_event_identity": act.identity,
        "yield_relation_identity": result.material["yield_relation_identity"],
    }


@pytest.mark.parametrize("carrier", ("result", "assertion"))
def test_measured_scalar_cannot_impersonate_pair_occurrence_result_standing(carrier):
    ledger, locality, _pair, _recurrence, _source, finding = _fixture()
    _act, result = _record(ledger, locality, finding)
    dimensions = (
        result.material["dimensions"]
        if carrier == "result"
        else result.material["assertions"][0]["dimensions"]
    )
    dimensions["standing"] = "measured"

    with pytest.raises(ValueError, match="differs from its exact finding"):
        get_recorded_result_of_measurement_of_recurrent_byte_pair_occurrence_position(
            ledger, result.identity
        )


def test_same_bytes_cannot_substitute_another_material_result_occurrence():
    ledger, locality, _pair, _recurrence, _source, finding = _fixture()
    substitute = record_operator_material_occurrence(
        ledger,
        locality_identity=locality,
        exact=b"ba---ab",
        source_boundary="another exact boundary",
    )
    substituted = finding._replace(
        source_material_result_occurrence_identity=substitute.identity
    )

    with pytest.raises(ValueError, match="outside its exact boundary"):
        record_responsibility_assignment_for_measurement_of_recurrent_byte_pair_occurrence_position(
            ledger,
            finding=substituted,
            locality_standing=read_operator_locality_standing(
                ledger, locality_identity=locality
            ),
        )


def test_distinct_locality_and_pre_source_boundary_are_refused():
    ledger, _locality, pair, recurrence, source, _finding = _fixture()
    other = record_operator_material_occurrence(
        ledger,
        locality_identity="other-locality",
        exact=b"ba---ab",
        source_boundary="other",
    )
    with pytest.raises(ValueError, match="distinct Localities"):
        measure_positions_of_recurrent_byte_pair_occurrences(
            ledger,
            pair_measurement_occurrence_identity=pair.identity,
            recurrence_assertion_position=recurrence.assertion_position,
            source_material_result_occurrence_identity=other.identity,
            occurrence_count_boundary=16,
        )
    boundary_before_source = ledger.append_boundary_through_occurrence(pair.identity)
    with pytest.raises(ValueError, match="outside its exact boundary"):
        measure_positions_of_recurrent_byte_pair_occurrences(
            ledger,
            pair_measurement_occurrence_identity=pair.identity,
            recurrence_assertion_position=recurrence.assertion_position,
            source_material_result_occurrence_identity=source.identity,
            occurrence_count_boundary=16,
            through=boundary_before_source,
        )


def test_count_assertion_cannot_impersonate_recurrence_and_result_is_single_use():
    ledger, locality, pair, recurrence, source, finding = _fixture()
    count_position = recurrence.support_assertion_references[0][
        "assertion_position"
    ]
    with pytest.raises(ValueError, match="does not establish recurrence"):
        measure_positions_of_recurrent_byte_pair_occurrences(
            ledger,
            pair_measurement_occurrence_identity=pair.identity,
            recurrence_assertion_position=count_position,
            source_material_result_occurrence_identity=source.identity,
            occurrence_count_boundary=16,
        )
    act, _result = _record(ledger, locality, finding)
    with pytest.raises(ValueError, match="already has a result"):
        record_result_of_measurement_of_recurrent_byte_pair_occurrence_position(
            ledger,
            act_occurrence_event_identity=act.identity,
        )


def test_unrelated_later_material_does_not_move_the_measured_boundary():
    ledger, locality, _pair, _recurrence, _source, finding = _fixture()
    record_operator_material_occurrence(
        ledger,
        locality_identity=locality,
        exact=b"abababab",
        source_boundary="later boundary",
    )
    _act, result = _record(ledger, locality, finding)

    assert get_recorded_result_of_measurement_of_recurrent_byte_pair_occurrence_position(ledger, result.identity) == finding


def test_occurrence_position_yield_cannot_impersonate_measurement_of_pair_occurrence_position_yield():
    ledger, locality, _pair, _recurrence, _source, finding = _fixture()
    _act, result = _record(ledger, locality, finding)
    yield_relation = ledger.get(result.material["yield_relation_identity"])
    yield_relation.material["occurrence_boundary"] = "occurrence_position_measurement"

    with pytest.raises(ValueError, match="no exact Yield relation"):
        get_recorded_result_of_measurement_of_recurrent_byte_pair_occurrence_position(
            ledger, result.identity
        )


@pytest.mark.parametrize(
    "crossing",
    ("act_occurrence", "yield_relation", "recorded_result", "pair_subject"),
)
def test_each_measurement_of_pair_occurrence_position_crossing_refuses_its_own_corruption(
    crossing,
):
    ledger, locality, pair, _recurrence, _source, finding = _fixture()
    act, result = _record(ledger, locality, finding)

    if crossing == "act_occurrence":
        act.material["occurrence_count_boundary"] += 1
    elif crossing == "yield_relation":
        yield_relation = ledger.get(result.material["yield_relation_identity"])
        yield_relation.material["result"]["occurrence_count_boundary"] += 1
    elif crossing == "recorded_result":
        result.material["assertions"][0]["dimensions"]["content"][
            "first_position"
        ] += 1
    else:
        pair.material["assertions"][0]["dimensions"]["content"] = {
            "substituted": True
        }

    with pytest.raises(ValueError):
        get_recorded_result_of_measurement_of_recurrent_byte_pair_occurrence_position(
            ledger, result.identity
        )




FIDELITY_DISTINCTIONS = {
    ("book_coordinates", "01.Source.D", "result"): (
        test_pair_occurrence_measurement_finds_exact_positions_without_a_sign,
        test_each_pair_position_assertion_has_one_exact_occurrence_bound_reference,
        test_assignment_read_threads_one_exact_standing_to_pair_validation,
        test_assignment_pair_handoff_still_refuses_later_pair_corruption,
        test_public_assignment_read_still_reconstructs_prior_standing,
        test_one_same_boundary_pair_subject_set_requires_exact_distinct_recurrence_subjects,
        test_same_boundary_pair_subjects_keep_each_yield_relation_distinct,
        test_occurrence_count_boundary_is_explicit_and_preserves_exact_known_loss,
        test_same_bytes_cannot_substitute_another_material_result_occurrence,
        test_count_assertion_cannot_impersonate_recurrence_and_result_is_single_use,
        test_unrelated_later_material_does_not_move_the_measured_boundary,
    ),
    ("book_coordinates", "01.Source.A", "subject"): (
        test_each_measurement_of_pair_occurrence_position_crossing_refuses_its_own_corruption,
    ),
}
