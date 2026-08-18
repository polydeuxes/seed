from __future__ import annotations

from copy import deepcopy
import json

import pytest
from tests.representation_admission import admit_representation

import seed_runtime.measurement_of_recurrent_byte_pair_occurrence_position as pair_occurrence_measurement
from seed_runtime.byte_measurement import (
    record_byte_measurement_responsibility_assignment,
    assertions_of_recorded_byte_position_pair_measurement,
    record_byte_measurement_responsible_act_evidence,
    record_byte_measurement_result,
    record_byte_position_pair_count_layer,
)
from seed_runtime.events import EventLedger, EventLedgerBoundary, SQLiteEventLedger
from seed_runtime.material_ingest import ingest_material
from seed_runtime.measurement_of_recurrent_byte_pair_occurrence_position import (
    RECORDED_RESPONSIBILITY_ASSIGNMENT_OF_MEASUREMENT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_KIND,
    RECORDED_EVIDENCE_OF_ACT_OCCURRENCE_OF_MEASUREMENT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_KIND,
    RECORDING_OCCURRENCE_OF_RESULT_OF_MEASUREMENT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_KIND,
    get_responsibility_assignment_for_measurement_of_recurrent_byte_pair_occurrence_position,
    get_recorded_result_of_measurement_of_recurrent_byte_pair_occurrence_position,
    measure_positions_of_recurrent_byte_pair_occurrences,
    measure_positions_for_recurrent_byte_pair_assertions,
    references_to_recorded_recurrent_byte_pair_occurrence_positions,
    record_responsibility_assignment_for_measurement_of_recurrent_byte_pair_occurrence_position,
    record_evidence_of_act_occurrence_for_measurement_of_recurrent_byte_pair_occurrence_position,
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
from seed_runtime.operator_representation import (
    emit_operator_representation_material,
    read_operator_representation,
    record_operator_representation,
)
from seed_runtime.evidence_of_yield_relation import read_requirements_of_yield_relation
from seed_runtime.operator_representation_admission import RepresentationAdmissionError


def _fixture(
    *,
    current: bytes = b"ba---ab",
    premise: bytes = b"abxxab",
    ledger=None,
):
    ledger = ledger or EventLedger()
    locality = "pair-occurrence-measurement"
    ingest_material(
        ledger,
        locality_identity=locality,
        exact_bytes=premise,
        source_role="premise material",
        source_boundary="exact premise boundary",
    )
    byte_assignment = record_byte_measurement_responsibility_assignment(
        ledger,
        source_localities=(locality,),
        recording_locality_identity=locality,
        locality_standing=read_operator_locality_standing(
            ledger, locality_identity=locality
        ),
    )
    byte_act = record_byte_measurement_responsible_act_evidence(
        ledger,
        responsibility_assignment_event_identity=byte_assignment.identity,
        responsibility_assignment_standing=read_operator_locality_standing(
            ledger, locality_identity=locality
        ),
    )
    byte = record_byte_measurement_result(
        ledger,
        responsible_act_evidence_event_identity=byte_act.identity,
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
        and assertion.representation == (ord("a"), ord("b"))
    )
    source = ingest_material(
        ledger,
        locality_identity=locality,
        exact_bytes=current,
        source_role="operator material",
        source_boundary="later exact material boundary",
    )
    finding = measure_positions_of_recurrent_byte_pair_occurrences(
        ledger,
        pair_measurement_occurrence_identity=pair.identity,
        recurrence_assertion_identity=recurrence.assertion_identity,
        source_ingest_occurrence_identity=source.identity,
        occurrence_limit=16,
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
    act = record_evidence_of_act_occurrence_for_measurement_of_recurrent_byte_pair_occurrence_position(
        ledger,
        responsibility_assignment_event_identity=assignment.identity,
        responsibility_assignment_standing=read_operator_locality_standing(
            ledger, locality_identity=locality
        ),
    )
    result = record_result_of_measurement_of_recurrent_byte_pair_occurrence_position(
        ledger,
        responsible_act_evidence_event_identity=act.identity,
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

    assert act.kind == RECORDED_EVIDENCE_OF_ACT_OCCURRENCE_OF_MEASUREMENT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_KIND
    assert result.kind == RECORDING_OCCURRENCE_OF_RESULT_OF_MEASUREMENT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_KIND
    assert read == finding
    assert result.exact_material is None
    requirements = read_requirements_of_yield_relation(
        ledger,
        recorded_result_event_identity=result.identity,
        evidence_of_yield_relation_event_identity=result.material["evidence_of_yield_relation_identity"],
        responsible_act_evidence_event_identity=act.identity,
    )
    assert requirements == {
        "exact_relation": True,
        "occurrence_witness": True,
        "intact_evidence": True,
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
    standing = read_operator_locality_standing(
        ledger, locality_identity=locality
    )

    assert assignment.kind == RECORDED_RESPONSIBILITY_ASSIGNMENT_OF_MEASUREMENT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_KIND
    assert get_responsibility_assignment_for_measurement_of_recurrent_byte_pair_occurrence_position(
        ledger, assignment.identity
    ) == assignment
    assert standing["responsibility_assignment_occurrences"][assignment.identity] is None
    assert "standing" not in assignment.material

    act = record_evidence_of_act_occurrence_for_measurement_of_recurrent_byte_pair_occurrence_position(
        ledger,
        responsibility_assignment_event_identity=assignment.identity,
        responsibility_assignment_standing=standing,
    )
    result = record_result_of_measurement_of_recurrent_byte_pair_occurrence_position(
        ledger,
        responsible_act_evidence_event_identity=act.identity,
    )
    evidence = ledger.get(result.material["evidence_of_yield_relation_identity"])
    identities = {
        assignment.identity,
        assignment.material["assignment_identity"],
        assignment.material["assignment_subject_identity"],
        assignment.material["measurement_act_identity"],
        assignment.material["act_occurrence_identity"],
        assignment.material["measurement_result_identity"],
        act.identity,
        evidence.identity,
        result.identity,
    }
    assert len(identities) == 9
    assert act.material["responsibility_assignment_reference"] == {
        "recorded_occurrence_identity": assignment.identity,
        "assignment_identity": assignment.material["assignment_identity"],
        "assignment_subject_identity": assignment.material[
            "assignment_subject_identity"
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
        record_evidence_of_act_occurrence_for_measurement_of_recurrent_byte_pair_occurrence_position(
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
    shaped["responsibility_assignment_occurrences"] = {
        "same-shape-assignment": None
    }

    with pytest.raises(ValueError, match="exact current Locality Standing"):
        record_evidence_of_act_occurrence_for_measurement_of_recurrent_byte_pair_occurrence_position(
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
    assignment.material["occurrence_limit"] += 1

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
    standing = read_operator_locality_standing(
        ledger, locality_identity=locality
    )

    @_operator_standing_replay_validation
    def outer():
        with pytest.raises(ValueError, match="exact accumulators"):
            _set_operator_standing_validation_context(
                ledger,
                locality_identity=locality,
                through_event_occurrence_identity=standing[
                    "through_event_occurrence_identity"
                ],
                measurement_occurrences=standing["measurement_occurrences"],
                ingest_occurrences=standing["ingest_occurrences"],
                responsibility_assignment_occurrences=standing[
                    "responsibility_assignment_occurrences"
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
            ingest_occurrences=standing["ingest_occurrences"],
            responsibility_assignment_occurrences={
                **standing["responsibility_assignment_occurrences"],
                assignment.identity: None,
            },
        )
        return get_responsibility_assignment_for_measurement_of_recurrent_byte_pair_occurrence_position(
            ledger, assignment.identity
        )

    with pytest.raises(ValueError, match="exact accumulators"):
        read_from_false_earlier_context()


@pytest.mark.parametrize("forged_coordinate", ["measurement", "ingest"])
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
    def read_from_context(measurements, ingests):
        _set_operator_standing_validation_context(
            ledger,
            locality_identity=locality,
            through_event_occurrence_identity=assignment.material[
                "standing_boundary_identity"
            ],
            measurement_occurrences=measurements,
            ingest_occurrences=ingests,
            responsibility_assignment_occurrences=standing[
                "responsibility_assignment_occurrences"
            ],
        )
        return get_responsibility_assignment_for_measurement_of_recurrent_byte_pair_occurrence_position(
            ledger, assignment.identity
        )

    measurements = deepcopy(standing["measurement_occurrences"])
    ingests = deepcopy(standing["ingest_occurrences"])
    coordinate = (
        measurements[pair.identity]
        if forged_coordinate == "measurement"
        else next(
            occurrence
            for occurrence in ingests
            if occurrence.get("evidence_event_identity") == source.identity
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
        read_from_context(measurements, ingests)


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
    act = record_evidence_of_act_occurrence_for_measurement_of_recurrent_byte_pair_occurrence_position(
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
        responsible_act_evidence_event_identity=act.identity,
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
        reference.assertion_identity for reference in references
    ) == tuple(
        assertion["dimensions"]["identity"]
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
            reference.recurrence_assertion_identity,
            reference.count_assertion_identity,
            reference.source_ingest_occurrence_identity,
            reference.locality_identity,
            reference.completeness_boundary_identity,
            reference.exact_pair,
        )
        for reference in references
    } == {
        (
            result.identity,
            pair.identity,
            recurrence.assertion_identity,
            recurrence.support_assertion_references[0]["assertion_identity"],
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
            "assertion_identity": reference.assertion_identity,
        }
        for reference in references
    )


def test_same_boundary_pair_subjects_have_one_pair_result_read(monkeypatch):
    ledger, _locality, pair, _recurrence, source, _finding = _fixture(
        premise=b"abxxabyybayyba",
        current=b"ba---abxx--yy",
    )
    pair_assertions = assertions_of_recorded_byte_position_pair_measurement(
        ledger, pair.identity
    )
    recurrence_identities = tuple(
        assertion.assertion_identity
        for assertion in pair_assertions or ()
        if assertion.result == "recurrence"
    )
    assert len(recurrence_identities) > 1
    through = ledger.append_boundary()
    expected = tuple(
        measure_positions_of_recurrent_byte_pair_occurrences(
            ledger,
            pair_measurement_occurrence_identity=pair.identity,
            recurrence_assertion_identity=identity,
            source_ingest_occurrence_identity=source.identity,
            occurrence_limit=16,
            through=through,
        )
        for identity in recurrence_identities
    )
    pair_result_read_count = 0
    source_read_count = 0
    order_read_count = 0
    boundary_read_count = 0
    pair_result_read = (
        pair_occurrence_measurement._findings_of_recorded_byte_position_pair_measurement
    )
    source_read = pair_occurrence_measurement._exact_ingest_event
    order_read = ledger.occurrences_in_append_order
    boundary_read = ledger.list_locality

    def witness_pair_result_read(ledger, event_identity):
        nonlocal pair_result_read_count
        pair_result_read_count += 1
        return pair_result_read(ledger, event_identity)

    def witness_source_read(ledger, event_identity):
        nonlocal source_read_count
        source_read_count += 1
        return source_read(ledger, event_identity)

    def witness_order_read(event_identities, *, locality_identity):
        nonlocal order_read_count
        order_read_count += 1
        return order_read(
            event_identities, locality_identity=locality_identity
        )

    def witness_boundary_read(locality_identity, *, through=None):
        nonlocal boundary_read_count
        boundary_read_count += 1
        return boundary_read(locality_identity, through=through)

    monkeypatch.setattr(
        pair_occurrence_measurement,
        "_findings_of_recorded_byte_position_pair_measurement",
        witness_pair_result_read,
    )
    monkeypatch.setattr(
        pair_occurrence_measurement, "_exact_ingest_event", witness_source_read
    )
    monkeypatch.setattr(
        ledger, "occurrences_in_append_order", witness_order_read
    )
    monkeypatch.setattr(ledger, "list_locality", witness_boundary_read)
    pair_result_read(ledger, pair.identity)
    exact_pair_read_order_count = order_read_count
    exact_pair_read_boundary_count = boundary_read_count
    pair_result_read_count = 0
    source_read_count = 0
    order_read_count = 0
    boundary_read_count = 0
    measured = measure_positions_for_recurrent_byte_pair_assertions(
        ledger,
        pair_measurement_occurrence_identity=pair.identity,
        recurrence_assertion_identities=recurrence_identities,
        source_ingest_occurrence_identity=source.identity,
        occurrence_limit=16,
        through=through,
    )

    assert measured == expected
    assert pair_result_read_count == 1
    assert source_read_count == 1
    assert order_read_count == exact_pair_read_order_count + 1
    assert boundary_read_count == exact_pair_read_boundary_count + 1
    assert tuple(
        finding.pair_reference.recurrence_assertion_identity
        for finding in measured
    ) == recurrence_identities
    assert {
        (
            finding.source_ingest_occurrence_identity,
            finding.source_locality_identity,
            finding.completeness_boundary.identity,
            finding.occurrence_limit,
        )
        for finding in measured
    } == {(source.identity, source.locality_identity, through.identity, 16)}


def test_one_same_boundary_pair_subject_set_requires_exact_distinct_recurrence_subjects():
    ledger, _locality, pair, recurrence, source, _finding = _fixture()
    through = ledger.append_boundary()

    class TupleSubclass(tuple):
        pass

    class BoundarySubclass(EventLedgerBoundary):
        pass

    for supplied in ([recurrence.assertion_identity], TupleSubclass((recurrence.assertion_identity,))):
        with pytest.raises(ValueError, match="exact occurrence identities"):
            measure_positions_for_recurrent_byte_pair_assertions(
                ledger,
                pair_measurement_occurrence_identity=pair.identity,
                recurrence_assertion_identities=supplied,
                source_ingest_occurrence_identity=source.identity,
                occurrence_limit=16,
                through=through,
            )
    with pytest.raises(ValueError, match="entered one result twice"):
        measure_positions_for_recurrent_byte_pair_assertions(
            ledger,
            pair_measurement_occurrence_identity=pair.identity,
            recurrence_assertion_identities=(
                recurrence.assertion_identity,
                recurrence.assertion_identity,
            ),
            source_ingest_occurrence_identity=source.identity,
            occurrence_limit=16,
            through=through,
        )
    count_identity = recurrence.support_assertion_references[0][
        "assertion_identity"
    ]
    with pytest.raises(ValueError, match="does not establish recurrence"):
        measure_positions_for_recurrent_byte_pair_assertions(
            ledger,
            pair_measurement_occurrence_identity=pair.identity,
            recurrence_assertion_identities=(count_identity,),
            source_ingest_occurrence_identity=source.identity,
            occurrence_limit=16,
            through=through,
        )
    with pytest.raises(TypeError, match="one exact boundary"):
        measure_positions_for_recurrent_byte_pair_assertions(
            ledger,
            pair_measurement_occurrence_identity=pair.identity,
            recurrence_assertion_identities=(recurrence.assertion_identity,),
            source_ingest_occurrence_identity=source.identity,
            occurrence_limit=16,
            through=BoundarySubclass(through.identity),
        )
    with pytest.raises(ValueError, match="outside its exact boundary"):
        measure_positions_for_recurrent_byte_pair_assertions(
            ledger,
            pair_measurement_occurrence_identity=pair.identity,
            recurrence_assertion_identities=(recurrence.assertion_identity,),
            source_ingest_occurrence_identity=source.identity,
            occurrence_limit=16,
            through=ledger.append_boundary_through_occurrence(pair.identity),
        )


def test_same_boundary_pair_subjects_keep_each_result_evidence_distinct():
    ledger, locality, pair, _recurrence, source, _finding = _fixture(
        premise=b"abxxabyybayyba",
        current=b"ba---abxx--yy",
    )
    recurrence_identities = tuple(
        assertion.assertion_identity
        for assertion in assertions_of_recorded_byte_position_pair_measurement(
            ledger, pair.identity
        ) or ()
        if assertion.result == "recurrence"
    )
    findings = measure_positions_for_recurrent_byte_pair_assertions(
        ledger,
        pair_measurement_occurrence_identity=pair.identity,
        recurrence_assertion_identities=recurrence_identities,
        source_ingest_occurrence_identity=source.identity,
        occurrence_limit=16,
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


def test_act_evidence_has_inputs_and_responsibility_but_no_result_finding():
    ledger, locality, _pair, _recurrence, _source, finding = _fixture()
    assignment = record_responsibility_assignment_for_measurement_of_recurrent_byte_pair_occurrence_position(
        ledger,
        finding=finding,
        locality_standing=read_operator_locality_standing(
            ledger, locality_identity=locality
        ),
    )
    act = record_evidence_of_act_occurrence_for_measurement_of_recurrent_byte_pair_occurrence_position(
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


def test_occurrence_limit_is_explicit_and_preserves_exact_known_loss():
    ledger, locality, pair, recurrence, source, _finding = _fixture()
    finding = measure_positions_of_recurrent_byte_pair_occurrences(
        ledger,
        pair_measurement_occurrence_identity=pair.identity,
        recurrence_assertion_identity=recurrence.assertion_identity,
        source_ingest_occurrence_identity=source.identity,
        occurrence_limit=2,
    )
    _act, result = _record(ledger, locality, finding)

    assert finding.occurrences == ((1, 0), (1, 6))
    assert finding.available_occurrence_count == 4
    assert result.material["occurrence_limit"] == 2
    assert result.material["known_loss"] == [
        "pair occurrences beyond the exact occurrence limit are not carried"
    ]


def test_measurement_result_does_not_promote_across_the_three_later_crossings():
    ledger, locality, _pair, _recurrence, _source, finding = _fixture()
    _act, result = _record(ledger, locality, finding)

    serialized = json.dumps(result.material).lower()
    assert all(
        word not in serialized
        for word in (
            "candidate",
            "participant",
            "admitted_material",
            "admission_result",
            "standing_movement",
            "represented_relation",
        )
    )
    assert result.identity not in read_operator_locality_standing(
        ledger, locality_identity=locality
    )["exact_result_occurrences"]


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
        "responsible_act_evidence_identity": act.identity,
        "evidence_of_yield_relation_identity": result.material["evidence_of_yield_relation_identity"],
    }
    representation = record_operator_representation(
        ledger,
        locality_identity=locality,
        locality_standing=standing,
        source_occurrence_reference=result.identity,
    )
    assert read_operator_representation(
        ledger, representation["representation_event_identity"]
    )["source_occurrence_reference"] == result.identity
    with pytest.raises(RepresentationAdmissionError, match="without exact material"):
        admit_representation(ledger, representation)


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


def test_same_bytes_cannot_substitute_another_ingest_occurrence():
    ledger, locality, _pair, _recurrence, _source, finding = _fixture()
    substitute = ingest_material(
        ledger,
        locality_identity=locality,
        exact_bytes=b"ba---ab",
        source_role="same bytes at another occurrence",
        source_boundary="another exact boundary",
    )
    substituted = finding._replace(
        source_ingest_occurrence_identity=substitute.identity
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
    other = ingest_material(
        ledger,
        locality_identity="other-locality",
        exact_bytes=b"ba---ab",
        source_role="other",
        source_boundary="other",
    )
    with pytest.raises(ValueError, match="distinct Localities"):
        measure_positions_of_recurrent_byte_pair_occurrences(
            ledger,
            pair_measurement_occurrence_identity=pair.identity,
            recurrence_assertion_identity=recurrence.assertion_identity,
            source_ingest_occurrence_identity=other.identity,
            occurrence_limit=16,
        )
    boundary_before_source = ledger.append_boundary_through_occurrence(pair.identity)
    with pytest.raises(ValueError, match="outside its exact boundary"):
        measure_positions_of_recurrent_byte_pair_occurrences(
            ledger,
            pair_measurement_occurrence_identity=pair.identity,
            recurrence_assertion_identity=recurrence.assertion_identity,
            source_ingest_occurrence_identity=source.identity,
            occurrence_limit=16,
            through=boundary_before_source,
        )


def test_count_assertion_cannot_impersonate_recurrence_and_result_is_single_use():
    ledger, locality, pair, recurrence, source, finding = _fixture()
    count_identity = recurrence.support_assertion_references[0][
        "assertion_identity"
    ]
    with pytest.raises(ValueError, match="does not establish recurrence"):
        measure_positions_of_recurrent_byte_pair_occurrences(
            ledger,
            pair_measurement_occurrence_identity=pair.identity,
            recurrence_assertion_identity=count_identity,
            source_ingest_occurrence_identity=source.identity,
            occurrence_limit=16,
        )
    act, _result = _record(ledger, locality, finding)
    with pytest.raises(ValueError, match="already has a result"):
        record_result_of_measurement_of_recurrent_byte_pair_occurrence_position(
            ledger,
            responsible_act_evidence_event_identity=act.identity,
        )


def test_unrelated_later_material_does_not_move_the_measured_boundary():
    ledger, locality, _pair, _recurrence, _source, finding = _fixture()
    ingest_material(
        ledger,
        locality_identity=locality,
        exact_bytes=b"abababab",
        source_role="later unrelated material",
        source_boundary="later boundary",
    )
    _act, result = _record(ledger, locality, finding)

    assert get_recorded_result_of_measurement_of_recurrent_byte_pair_occurrence_position(ledger, result.identity) == finding


def test_occurrence_position_yield_cannot_impersonate_measurement_of_pair_occurrence_position_yield():
    ledger, locality, _pair, _recurrence, _source, finding = _fixture()
    _act, result = _record(ledger, locality, finding)
    evidence = ledger.get(result.material["evidence_of_yield_relation_identity"])
    evidence.material["occurrence_boundary"] = "occurrence_position_measurement"

    with pytest.raises(ValueError, match="no exact Evidence of Yield relation"):
        get_recorded_result_of_measurement_of_recurrent_byte_pair_occurrence_position(
            ledger, result.identity
        )


@pytest.mark.parametrize(
    "crossing",
    ("act_evidence", "evidence_of_yield_relation", "recorded_result", "pair_subject"),
)
def test_each_measurement_of_pair_occurrence_position_crossing_refuses_its_own_corruption(
    crossing,
):
    ledger, locality, pair, _recurrence, _source, finding = _fixture()
    act, result = _record(ledger, locality, finding)

    if crossing == "act_evidence":
        act.material["occurrence_limit"] += 1
    elif crossing == "evidence_of_yield_relation":
        evidence = ledger.get(result.material["evidence_of_yield_relation_identity"])
        evidence.material["result"]["occurrence_limit"] += 1
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


FIDELITY_SUBJECTS = {
    "assertion_standing_coordinates": (
        test_exact_assignment_enters_current_standing_and_owns_distinct_lifecycle_identities,
        test_stale_standing_cannot_authorize_the_assigned_measurement_act,
        test_shaped_standing_without_the_exact_assignment_cannot_authorize_the_act,
        test_corrupted_assignment_occurrence_cannot_authorize_the_act,
        test_assignment_read_refuses_a_corrupted_unrelated_prior_standing_carrier,
        test_replay_validation_context_refuses_unbound_accumulators_and_clears,
        test_replay_context_before_the_recorded_assignment_boundary_is_refused,
        test_replay_context_refuses_forged_exact_boundary_input_coordinates,
        test_assignment_act_and_result_survive_distinct_durable_restarts,
        test_measurement_result_does_not_promote_across_the_three_later_crossings,
        test_pair_occurrence_result_enters_standing_as_one_exact_measurement_reference,
        test_measured_scalar_cannot_impersonate_pair_occurrence_result_standing,
    ),
    "act_evidence_responsibility_boundary_occurrence_authority_scope": (
        test_act_evidence_has_inputs_and_responsibility_but_no_result_finding,
    ),
    "yield_result_occurrence_evidence": (
        test_pair_occurrence_measurement_yield_preserves_the_exact_finding,
        test_occurrence_position_yield_cannot_impersonate_measurement_of_pair_occurrence_position_yield,
    ),
    "declared_measurement_result": (
        test_pair_occurrence_measurement_finds_exact_positions_without_a_sign,
        test_each_pair_position_assertion_has_one_exact_occurrence_bound_reference,
        test_same_boundary_pair_subjects_have_one_pair_result_read,
        test_one_same_boundary_pair_subject_set_requires_exact_distinct_recurrence_subjects,
        test_same_boundary_pair_subjects_keep_each_result_evidence_distinct,
        test_occurrence_limit_is_explicit_and_preserves_exact_known_loss,
        test_same_bytes_cannot_substitute_another_ingest_occurrence,
        test_count_assertion_cannot_impersonate_recurrence_and_result_is_single_use,
        test_unrelated_later_material_does_not_move_the_measured_boundary,
    ),
    "locality_relation_coordinates": (
        test_distinct_locality_and_pre_source_boundary_are_refused,
    ),
    "representation_source_coordinates": (
        test_each_measurement_of_pair_occurrence_position_crossing_refuses_its_own_corruption,
    ),
}
