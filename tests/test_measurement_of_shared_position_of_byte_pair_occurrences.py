from __future__ import annotations

from copy import deepcopy
from functools import lru_cache

import pytest

import seed_runtime.measurement_of_position_coordinates_of_byte_pair_occurrences as direct_position_module
import seed_runtime.measurement_of_recurrent_byte_pair_occurrence_position as recurrent_position_module
import seed_runtime.measurement_of_shared_position_of_byte_pair_occurrences as shared_position_module
import seed_runtime.operator_current_coordinates as operator_current_coordinates_module
from seed_runtime.addressed_byte_occurrence_reference_determination import (
    record_addressed_byte_occurrence_reference_determination_act_occurrence,
    record_addressed_byte_occurrence_reference_determination_applicability_act_occurrence,
    record_addressed_byte_occurrence_reference_determination_applicability_result,
    record_addressed_byte_occurrence_reference_determination_subject_to_act_binding,
    record_addressed_byte_occurrence_reference_determination_result,
)
from seed_runtime.byte_measurement import (
    record_byte_measurement_subject_to_act_binding,
    assertions_of_recorded_byte_position_pair_measurement,
    record_byte_measurement_act_occurrence,
    record_byte_measurement_result,
    record_byte_position_pair_count_layer,
)
from seed_runtime.events import EventLedger, SQLiteEventLedger
from tests.operator_material_source_test_witness import (
    record_operator_material_occurrence,
)
from seed_runtime.witness_material_source import record_witness_material_source
from seed_runtime.measurement_of_recurrent_byte_pair_occurrence_position import (
    measure_positions_for_recurrent_byte_pair_assertions,
    record_recurrent_byte_pair_occurrence_position_measurement_subject_to_act_binding,
    record_act_occurrence_for_measurement_of_recurrent_byte_pair_occurrence_position,
    record_result_of_measurement_of_recurrent_byte_pair_occurrence_position,
    references_to_recorded_recurrent_byte_pair_occurrence_positions,
)
from seed_runtime.measurement_of_position_coordinates_of_byte_pair_occurrences import (
    _source_position_coordinate_reference,
    record_byte_pair_occurrence_position_measurement_subject_to_act_binding,
    record_byte_pair_occurrence_position_measurement_act_occurrence,
    record_byte_pair_occurrence_position_measurement_result,
    references_to_recorded_position_coordinates_of_byte_pair_occurrences,
)
from seed_runtime.measurement_of_shared_position_of_byte_pair_occurrences import (
    SHARED_POSITION_APPLICABILITY_ACT_OCCURRENCE_EVENT,
    SHARED_POSITION_APPLICABILITY_RESULT_KIND,
    SHARED_POSITION_MEASUREMENT_ACT_OCCURRENCE_EVENT,
    SHARED_POSITION_MEASUREMENT_RESULT_KIND,
    SHARED_POSITION_MEASUREMENT_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
    SharedPairPositionError,
    get_shared_position_subject_to_act_binding,
    get_shared_position_applicability_act_occurrence,
    get_recorded_shared_position_applicability,
    get_shared_position_measurement_act_occurrence,
    get_recorded_shared_position_measurement,
    ordered_relation_path_assertion_adjacent_to_input_position_assertion_coordinates,
    ordered_source_position_coordinates_adjacent_to_ordered_relation_path_assertion,
    record_shared_position_applicability_act_occurrence,
    record_shared_position_applicability_result,
    record_shared_position_measurement_act_occurrence,
    record_shared_position_measurement_result,
    record_shared_position_subject_to_act_binding,
    record_shared_position_subject_to_act_binding_from_addressed_byte_occurrence_reference_determination_result,
)
from seed_runtime.operator_current_coordinates import (
    advance_operator_current_coordinates,
    read_operator_current_coordinates,
)


def _current_coordinates(ledger: EventLedger, locality: str):
    return read_operator_current_coordinates(
        ledger, locality_identity=locality
    )


def _direct_d2(
    ledger: EventLedger,
    *,
    locality: str,
    exact: bytes = b"2+2=5\n",
    position: int = 1,
):
    source = record_operator_material_occurrence(
        ledger,
        locality_identity=locality,
        exact=exact,
        source_boundary="exact material boundary",
    )
    direct_assignment = (
        record_byte_pair_occurrence_position_measurement_subject_to_act_binding(
            ledger,
            source_material_result_occurrence_identity=source.identity,
            current_coordinates=_current_coordinates(ledger, locality),
        )
    )
    direct_act = record_byte_pair_occurrence_position_measurement_act_occurrence(
        ledger,
        binding_event_identity=direct_assignment.identity,
        binding_current_coordinates=_current_coordinates(ledger, locality),
    )
    direct_result = record_byte_pair_occurrence_position_measurement_result(
        ledger,
        act_occurrence_event_identity=direct_act.identity,
    )
    coordinate = _source_position_coordinate_reference(
        source_material_result_occurrence_identity=source.identity,
        source_locality_identity=locality,
        completeness_boundary_identity=(
            ledger.append_boundary_through_occurrence(source.identity).identity
        ),
        position=position,
        exact_material=exact[position : position + 1],
    )
    determination_binding = record_addressed_byte_occurrence_reference_determination_subject_to_act_binding(
        ledger,
        direct_result_event_identity=direct_result.identity,
        addressed_source_byte_position_coordinate_reference=coordinate,
        current_coordinates=_current_coordinates(ledger, locality),
    )
    applicability_act = record_addressed_byte_occurrence_reference_determination_applicability_act_occurrence(
        ledger,
        binding_event_identity=determination_binding.identity,
        binding_current_coordinates=_current_coordinates(ledger, locality),
    )
    applicability = record_addressed_byte_occurrence_reference_determination_applicability_result(
        ledger,
        applicability_act_occurrence_event_identity=applicability_act.identity,
    )
    determination_act = record_addressed_byte_occurrence_reference_determination_act_occurrence(
        ledger,
        applicability_result_event_identity=applicability.identity,
        current_coordinates=_current_coordinates(ledger, locality),
    )
    determination_result = record_addressed_byte_occurrence_reference_determination_result(
        ledger,
        determination_act_occurrence_event_identity=determination_act.identity,
    )
    return source, direct_result, determination_result


def _build_fixture(
    *,
    current: bytes = b"abc",
    ledger=None,
    locality: str = "shared-pair-position",
):
    if ledger is None:
        ledger = EventLedger()
    record_operator_material_occurrence(
        ledger,
        locality_identity=locality,
        exact=b"abxxabbcxxbc",
        source_boundary="exact premise boundary",
    )
    byte_assignment = record_byte_measurement_subject_to_act_binding(
        ledger,
        source_localities=(locality,),
        recording_locality_identity=locality,
        current_coordinates=read_operator_current_coordinates(
            ledger, locality_identity=locality
        ),
    )
    byte_act = record_byte_measurement_act_occurrence(
        ledger,
        subject_to_act_binding_event_identity=byte_assignment.identity,
        current_coordinates=read_operator_current_coordinates(
            ledger, locality_identity=locality
        ),
    )
    byte_result = record_byte_measurement_result(
        ledger,
        act_occurrence_event_identity=byte_act.identity,
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
        assertion.content: assertion.assertion_position
        for assertion in pair_assertions or ()
        if assertion.result == "recurrence"
        and assertion.content in {(ord("a"), ord("b")), (ord("b"), ord("c"))}
    }
    assert set(recurrence_by_pair) == {
        (ord("a"), ord("b")),
        (ord("b"), ord("c")),
    }
    source = record_operator_material_occurrence(
        ledger,
        locality_identity=locality,
        exact=current,
        source_boundary="later exact material boundary",
    )
    findings = measure_positions_for_recurrent_byte_pair_assertions(
        ledger,
        pair_measurement_occurrence_identity=pair_result.identity,
        recurrence_assertion_positions=(
            recurrence_by_pair[(ord("a"), ord("b"))],
            recurrence_by_pair[(ord("b"), ord("c"))],
        ),
        source_material_result_occurrence_identity=source.identity,
        occurrence_count_boundary=16,
        through=ledger.append_boundary(),
    )
    results = []
    for finding in findings:
        binding = record_recurrent_byte_pair_occurrence_position_measurement_subject_to_act_binding(
            ledger,
            finding=finding,
            current_coordinates=_current_coordinates(ledger, locality),
        )
        act = record_act_occurrence_for_measurement_of_recurrent_byte_pair_occurrence_position(
            ledger,
            subject_to_act_binding_event_identity=binding.identity,
            current_coordinates=_current_coordinates(ledger, locality),
        )
        results.append(
            record_result_of_measurement_of_recurrent_byte_pair_occurrence_position(
                ledger,
                act_occurrence_event_identity=act.identity,
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


@lru_cache(maxsize=None)
def _in_memory_fixture_template(current: bytes, locality: str):
    return _build_fixture(current=current, locality=locality)


def _fixture(
    *,
    current: bytes = b"abc",
    ledger=None,
    locality: str = "shared-pair-position",
):
    if ledger is not None:
        return _build_fixture(current=current, ledger=ledger, locality=locality)
    return deepcopy(_in_memory_fixture_template(current, locality))


def _shared_binding(ledger, locality, first, second):
    return record_shared_position_subject_to_act_binding(
        ledger,
        first_result_occurrence_identity=first.recorded_occurrence_identity,
        first_assertion_address=first.assertion_address,
        second_result_occurrence_identity=second.recorded_occurrence_identity,
        second_assertion_address=second.assertion_address,
        current_coordinates=_current_coordinates(ledger, locality),
    )


def _recurrent_result_coordinates(ledger, reference):
    result = ledger.get(reference.recorded_occurrence_identity)
    act = ledger.get(result.material["act_occurrence_event_identity"])
    binding = ledger.get(
        act.material["subject_to_act_binding_reference"][
            "recorded_occurrence_identity"
        ]
    )
    pair = ledger.get(reference.pair_measurement_occurrence_identity)
    source = ledger.get(reference.source_material_result_occurrence_identity)
    yield_relation = ledger.get(
        result.material["yield_relation_identity"]
    )
    return {
        "result": result,
        "act": act,
        "binding": binding,
        "yield_relation": yield_relation,
        "pair": pair,
        "source": source,
    }


def _record_path(ledger, locality, first, second):
    binding = _shared_binding(ledger, locality, first, second)
    applicability_act = record_shared_position_applicability_act_occurrence(
        ledger,
        binding_event_identity=binding.identity,
        current_coordinates=_current_coordinates(ledger, locality),
    )
    applicability = record_shared_position_applicability_result(
        ledger,
        applicability_act_occurrence_event_identity=applicability_act.identity,
    )
    measurement_act = record_shared_position_measurement_act_occurrence(
        ledger,
        applicability_result_event_identity=applicability.identity,
        current_coordinates=_current_coordinates(ledger, locality),
    )
    result = record_shared_position_measurement_result(
        ledger,
        measurement_act_occurrence_event_identity=measurement_act.identity,
    )
    return binding, applicability_act, applicability, measurement_act, result


@pytest.fixture(scope="module")
def restarted_shared_path(tmp_path_factory):
    database = tmp_path_factory.mktemp("shared-position") / "shared-position.sqlite"
    ledger = SQLiteEventLedger(str(database))
    ledger, locality, _source, first, second = _fixture(ledger=ledger)
    binding, _applicability_act, _applicability, _measurement_act, result = (
        _record_path(ledger, locality, first, second)
    )
    result_identity = result.identity
    ledger.close()
    return {
        "database": database,
        "locality": locality,
        "binding": binding,
        "result_identity": result_identity,
    }


def _record_d2_shared_path(ledger, locality, determination_result):
    binding = record_shared_position_subject_to_act_binding_from_addressed_byte_occurrence_reference_determination_result(
        ledger,
        determination_result_event_identity=determination_result.identity,
        current_coordinates=_current_coordinates(ledger, locality),
    )
    applicability_act = record_shared_position_applicability_act_occurrence(
        ledger,
        binding_event_identity=binding.identity,
        current_coordinates=_current_coordinates(ledger, locality),
    )
    applicability = record_shared_position_applicability_result(
        ledger,
        applicability_act_occurrence_event_identity=applicability_act.identity,
    )
    measurement_act = record_shared_position_measurement_act_occurrence(
        ledger,
        applicability_result_event_identity=applicability.identity,
        current_coordinates=_current_coordinates(ledger, locality),
    )
    result = record_shared_position_measurement_result(
        ledger,
        measurement_act_occurrence_event_identity=measurement_act.identity,
    )
    return binding, applicability_act, applicability, measurement_act, result


def _position_coordinate_reference(reference, role):
    position = (
        reference.first_position if role == "first" else reference.second_position
    )
    exact_material = (
        reference.exact_pair[:1] if role == "first" else reference.exact_pair[1:]
    )
    return {
        "source_material_result_occurrence_identity": (
            reference.source_material_result_occurrence_identity
        ),
        "locality_identity": reference.locality_identity,
        "completeness_boundary_identity": (
            reference.completeness_boundary_identity
        ),
        "position": position,
        "exact_material": list(exact_material),
    }


def test_exact_yielded_pair_relations_compose_at_one_shared_position():
    ledger, locality, source, first, second = _fixture()
    binding, applicability_act, applicability, _measurement_act, result = (
        _record_path(ledger, locality, first, second)
    )
    assert applicability_act.material["addressed_act_identity"] == (
        binding.material["exact_act_identity"]
    )
    assert {
        relation["addressed_act_identity"]
        for relation in applicability_act.material["input_relations"]
    } == {binding.material["exact_act_identity"]}
    applicability_reading = get_recorded_shared_position_applicability(
        ledger, applicability.identity
    )
    assert applicability_reading["addressed_act_identity"] == (
        binding.material["exact_act_identity"]
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
    assert "responsibility_assignment" not in reading
    assert reading["subject_to_act_binding_reference"] == {
        "recorded_occurrence_identity": binding.identity,
        "book_clause_identity": binding.material["book_clause_identity"],
        "exact_act_identity": binding.material["exact_act_identity"],
        "subject_reference": binding.material["subject_reference"],
        "result_boundary_identity": binding.material[
            "measurement_result_identity"
        ],
    }
    assert binding.identity in _current_coordinates(ledger, locality)[
        "subject_to_act_binding_occurrences"
    ]
    assert len(reading["assertions"]) == 1
    assertion = reading["assertions"][0]
    assert assertion["result"] == "ordered_relation_path"
    assert "standing" not in assertion["dimensions"]
    content = assertion["dimensions"]["content"]
    assert content["shared_position_coordinate_reference"] == shared_reference
    assert content["source_material_result_occurrence_identity"] == source.identity
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
    assert result.exact_material is None
    assert result.identity in _current_coordinates(ledger, locality)["measurement_occurrences"]


def test_ordered_path_exposes_input_position_assertion_coordinates_without_carrying_their_pair_material():
    ledger, locality, _source, first, second = _fixture()
    _assignment_event, _applicability_act, _applicability, _measurement_act, result = (
        _record_path(ledger, locality, first, second)
    )
    boundary_before_read = ledger.append_boundary()

    path, first_coordinates, second_coordinates = (
        ordered_relation_path_assertion_adjacent_to_input_position_assertion_coordinates(
            ledger, result.identity
        )
    )
    reading = get_recorded_shared_position_measurement(ledger, result.identity)

    assert path == reading["assertions"][0]
    assert first_coordinates == reading["first_position_assertion"]
    assert second_coordinates == reading["second_position_assertion"]
    assert first_coordinates["exact_pair"] == list(first.exact_pair)
    assert second_coordinates["exact_pair"] == list(second.exact_pair)
    assert "exact_pair" not in path
    assert set(path["dimensions"]["content"]) == {
        "shared_position_coordinate_reference",
        "source_material_result_occurrence_identity",
        "completeness_boundary_identity",
    }
    assert ledger.append_boundary() == boundary_before_read

    first_coordinates["exact_pair"][0] = 255
    assert (
        ordered_relation_path_assertion_adjacent_to_input_position_assertion_coordinates(
            ledger, result.identity
        )[1]["exact_pair"]
        == list(first.exact_pair)
    )


def test_ordered_source_positions_are_adjacent_to_the_path_assertion():
    ledger, locality, _source, first, second = _fixture()
    _assignment_event, _applicability_act, _applicability, _measurement_act, result = (
        _record_path(ledger, locality, first, second)
    )
    boundary_before_read = ledger.append_boundary()

    path, positions = (
        ordered_source_position_coordinates_adjacent_to_ordered_relation_path_assertion(
            ledger, result.identity
        )
    )

    assert positions == (
        _position_coordinate_reference(first, "first"),
        _position_coordinate_reference(first, "second"),
        _position_coordinate_reference(second, "second"),
    )
    assert tuple(coordinate["position"] for coordinate in positions) == (
        first.first_position,
        first.second_position,
        second.second_position,
    )
    assert tuple(coordinate["exact_material"] for coordinate in positions) == (
        list(first.exact_pair[:1]),
        list(first.exact_pair[1:]),
        list(second.exact_pair[1:]),
    )
    assert "ordered_source_position_coordinates" not in path
    assert set(path["dimensions"]["content"]) == {
        "shared_position_coordinate_reference",
        "source_material_result_occurrence_identity",
        "completeness_boundary_identity",
    }
    assert ledger.append_boundary() == boundary_before_read


def test_two_recurrent_results_share_one_exact_current_standing_read(monkeypatch):
    ledger, locality, _source, first, second = _fixture()
    standing_reads = []
    original = operator_current_coordinates_module.read_operator_current_coordinates_through

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
        operator_current_coordinates_module,
        "read_operator_current_coordinates_through",
        witnessed,
    )
    inputs = shared_position_module._inputs(
        ledger,
        first_result_occurrence_identity=first.recorded_occurrence_identity,
        first_assertion_address=first.assertion_address,
        second_result_occurrence_identity=second.recorded_occurrence_identity,
        second_assertion_address=second.assertion_address,
    )
    second_binding = _recurrent_result_coordinates(
        ledger, second
    )["binding"]

    assert inputs.first == first
    assert inputs.second == second
    assert standing_reads == [
        (
            locality,
            second_binding.material["through_event_occurrence_identity"],
        )
    ]

    standing_reads.clear()
    references_to_recorded_recurrent_byte_pair_occurrence_positions(
        ledger,
        result_occurrence_identity=first.recorded_occurrence_identity,
    )
    references_to_recorded_recurrent_byte_pair_occurrence_positions(
        ledger,
        result_occurrence_identity=second.recorded_occurrence_identity,
    )
    assert len(standing_reads) == 2


def test_shared_binding_threads_explicit_prior_without_replay_or_ambient_override(
    monkeypatch,
):
    ledger, locality, _source, first, second = _fixture()
    prior_coordinates = _current_coordinates(ledger, locality)
    binding = record_shared_position_subject_to_act_binding(
        ledger,
        first_result_occurrence_identity=first.recorded_occurrence_identity,
        first_assertion_address=first.assertion_address,
        second_result_occurrence_identity=second.recorded_occurrence_identity,
        second_assertion_address=second.assertion_address,
        current_coordinates=prior_coordinates,
    )

    def replay_must_not_run(*_args, **_kwargs):
        raise AssertionError("explicit shared-position prior Standing was replayed")

    def ambient_must_not_override(*_args, **_kwargs):
        raise AssertionError("ambient Standing overrode an explicit carrier")

    monkeypatch.setattr(
        operator_current_coordinates_module,
        "read_operator_current_coordinates_through",
        replay_must_not_run,
    )
    monkeypatch.setattr(
        operator_current_coordinates_module,
        "_operator_current_coordinate_validation_context",
        ambient_must_not_override,
    )

    read_binding, inputs = shared_position_module._read_binding(
        ledger,
        binding.identity,
        prior_coordinates=prior_coordinates,
    )

    assert read_binding == binding
    assert inputs.first == first
    assert inputs.second == second


@pytest.mark.parametrize(
    "changed_prior",
    ("stale", "wrong locality", "substituted binding"),
)
def test_shared_binding_refuses_changed_explicit_prior_coordinates(changed_prior):
    ledger, locality, _source, first, second = _fixture()
    exact_prior = _current_coordinates(ledger, locality)
    binding = record_shared_position_subject_to_act_binding(
        ledger,
        first_result_occurrence_identity=first.recorded_occurrence_identity,
        first_assertion_address=first.assertion_address,
        second_result_occurrence_identity=second.recorded_occurrence_identity,
        second_assertion_address=second.assertion_address,
        current_coordinates=exact_prior,
    )
    changed_coordinates = deepcopy(exact_prior)
    if changed_prior == "stale":
        first_act = _recurrent_result_coordinates(ledger, first)["act"]
        changed_coordinates = operator_current_coordinates_module.read_operator_current_coordinates_through(
            ledger,
            locality_identity=locality,
            through_event_occurrence_identity=first_act.identity,
        )
    elif changed_prior == "wrong locality":
        changed_coordinates["locality_identity"] = "another-shared-position-locality"
    else:
        second_binding = _recurrent_result_coordinates(
            ledger, second
        )["binding"]
        del changed_coordinates["subject_to_act_binding_occurrences"][
            second_binding.identity
        ]
        changed_coordinates["subject_to_act_binding_occurrences"][
            "substituted-same-shaped-binding"
        ] = None

    with pytest.raises((SharedPairPositionError, ValueError)):
        shared_position_module._read_binding(
            ledger,
            binding.identity,
            prior_coordinates=changed_coordinates,
        )


def test_shared_binding_explicit_prior_revalidates_later_input_mutation():
    ledger, locality, _source, first, second = _fixture()
    exact_prior = _current_coordinates(ledger, locality)
    binding = record_shared_position_subject_to_act_binding(
        ledger,
        first_result_occurrence_identity=first.recorded_occurrence_identity,
        first_assertion_address=first.assertion_address,
        second_result_occurrence_identity=second.recorded_occurrence_identity,
        second_assertion_address=second.assertion_address,
        current_coordinates=exact_prior,
    )
    changed_result = _recurrent_result_coordinates(ledger, second)["result"]
    changed_result.material["known_loss"] = not changed_result.material["known_loss"]

    with pytest.raises((SharedPairPositionError, ValueError)):
        shared_position_module._read_binding(
            ledger,
            binding.identity,
            prior_coordinates=exact_prior,
        )


@pytest.mark.parametrize(
    "changed_occurrence",
    ("result", "act", "binding", "pair", "source"),
)
def test_recurrent_result_batch_revalidates_every_carried_occurrence_after_coordinate_read(
    monkeypatch, changed_occurrence
):
    ledger, _locality, _source, first, second = _fixture()
    changed = _recurrent_result_coordinates(ledger, first)[
        changed_occurrence
    ]
    original_material = deepcopy(changed.material)
    original = operator_current_coordinates_module.read_operator_current_coordinates_through
    changed_once = False

    def change_after_standing(*args, **kwargs):
        nonlocal changed_once
        current_coordinates = original(*args, **kwargs)
        if not changed_once:
            if changed_occurrence == "source":
                changed.material["source_role"] = "changed after Standing"
            elif changed_occurrence == "pair":
                changed.material["assertions"][0]["dimensions"][
                    "content"
                ] = {"changed_after_standing": True}
            else:
                changed.material["changed_after_standing"] = True
            changed_once = True
        return current_coordinates

    monkeypatch.setattr(
        operator_current_coordinates_module,
        "read_operator_current_coordinates_through",
        change_after_standing,
    )
    identities = {
        "first_result_occurrence_identity": first.recorded_occurrence_identity,
        "first_assertion_address": first.assertion_address,
        "second_result_occurrence_identity": second.recorded_occurrence_identity,
        "second_assertion_address": second.assertion_address,
    }
    with pytest.raises((SharedPairPositionError, ValueError)):
        shared_position_module._inputs(ledger, **identities)

    changed.material.clear()
    changed.material.update(original_material)
    assert shared_position_module._inputs(ledger, **identities).first == first


def test_recurrent_result_batch_keeps_its_historical_boundary_across_unrelated_append(
    monkeypatch,
):
    ledger, locality, _source, first, second = _fixture()
    original = operator_current_coordinates_module.read_operator_current_coordinates_through
    appended = False

    def append_after_standing(*args, **kwargs):
        nonlocal appended
        current_coordinates = original(*args, **kwargs)
        if not appended:
            ledger.append(
                "test.unrelated.recorded",
                {"source": "unrelated"},
                locality_identity=locality,
            )
            appended = True
        return current_coordinates

    monkeypatch.setattr(
        operator_current_coordinates_module,
        "read_operator_current_coordinates_through",
        append_after_standing,
    )
    inputs = shared_position_module._inputs(
        ledger,
        first_result_occurrence_identity=first.recorded_occurrence_identity,
        first_assertion_address=first.assertion_address,
        second_result_occurrence_identity=second.recorded_occurrence_identity,
        second_assertion_address=second.assertion_address,
    )

    assert inputs.first == first
    assert inputs.second == second
    assert appended is True


def test_recurrent_result_batch_requires_an_addressed_position_and_one_locality():
    ledger, _locality, _source, first, second = _fixture()
    first_result = ledger.get(first.recorded_occurrence_identity)
    first_unaddressed_position = len(first_result.material["assertions"])
    with pytest.raises((SharedPairPositionError, ValueError)):
        shared_position_module._inputs(
            ledger,
            first_result_occurrence_identity=first.recorded_occurrence_identity,
            first_assertion_address=first_unaddressed_position,
            second_result_occurrence_identity=second.recorded_occurrence_identity,
            second_assertion_address=second.assertion_address,
        )

    _ledger, _other_locality, _other_source, _other_first, other_second = (
        _fixture(ledger=ledger, locality="another-shared-pair-position")
    )
    with pytest.raises((SharedPairPositionError, ValueError)):
        shared_position_module._inputs(
            ledger,
            first_result_occurrence_identity=first.recorded_occurrence_identity,
            first_assertion_address=first.assertion_address,
            second_result_occurrence_identity=(
                other_second.recorded_occurrence_identity
            ),
            second_assertion_address=other_second.assertion_address,
        )


def test_recurrent_result_batch_refuses_through_occurrences_without_one_order():
    ledger, _locality, _source, first, second = _fixture()
    binding = _recurrent_result_coordinates(ledger, first)["binding"]
    binding.material["through_event_occurrence_identity"] = (
        second.recorded_occurrence_identity
    )

    with pytest.raises((SharedPairPositionError, ValueError)):
        shared_position_module._inputs(
            ledger,
            first_result_occurrence_identity=first.recorded_occurrence_identity,
            first_assertion_address=first.assertion_address,
            second_result_occurrence_identity=second.recorded_occurrence_identity,
            second_assertion_address=second.assertion_address,
        )


def test_direct_position_coordinate_assertions_compose_without_recurrence_support(
    monkeypatch,
):
    ledger = EventLedger()
    locality = "direct-pair-position"
    _source, direct_result, determination_result = _direct_d2(
        ledger, locality=locality
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

    binding = record_shared_position_subject_to_act_binding_from_addressed_byte_occurrence_reference_determination_result(
        ledger,
        determination_result_event_identity=determination_result.identity,
        current_coordinates=_current_coordinates(ledger, locality),
    )
    applicability_act = record_shared_position_applicability_act_occurrence(
        ledger,
        binding_event_identity=binding.identity,
        current_coordinates=_current_coordinates(ledger, locality),
    )
    applicability = record_shared_position_applicability_result(
        ledger,
        applicability_act_occurrence_event_identity=applicability_act.identity,
    )
    measurement_act = record_shared_position_measurement_act_occurrence(
        ledger,
        applicability_result_event_identity=applicability.identity,
        current_coordinates=_current_coordinates(ledger, locality),
    )
    result = record_shared_position_measurement_result(
        ledger,
        measurement_act_occurrence_event_identity=measurement_act.identity,
    )
    assert result_reads
    assert set(result_reads) == {direct_result.identity}
    reading = get_recorded_shared_position_measurement(ledger, result.identity)

    assert reading["assertions"][0]["dimensions"]["content"][
        "shared_position_coordinate_reference"
    ] == _position_coordinate_reference(first, "second")
    assert binding.material["first_position_assertion"][
        "support_assertion_references"
    ] == []
    assert binding.material["second_position_assertion"][
        "support_assertion_references"
    ] == []
    assert binding.material[
        shared_position_module.D2_RESULT_REFERENCE_COORDINATE
    ] == _current_coordinates(ledger, locality)["measurement_occurrences"][
        determination_result.identity
    ]


def test_shared_position_binding_refuses_raw_direct_result_inputs_atomically():
    ledger = EventLedger()
    locality = "raw-direct-pair-position"
    _source, direct_result, _determination_result = _direct_d2(
        ledger, locality=locality
    )
    references = references_to_recorded_position_coordinates_of_byte_pair_occurrences(
        ledger, direct_result.identity
    )
    first = next(reference for reference in references if reference.exact_pair == b"2+")
    second = next(reference for reference in references if reference.exact_pair == b"+2")
    before = len(ledger.list())

    with pytest.raises(SharedPairPositionError, match="require one D.2"):
        record_shared_position_subject_to_act_binding(
            ledger,
            first_result_occurrence_identity=direct_result.identity,
            first_assertion_address=first.assertion_address,
            second_result_occurrence_identity=direct_result.identity,
            second_assertion_address=second.assertion_address,
            current_coordinates=_current_coordinates(ledger, locality),
        )
    assert len(ledger.list()) == before


@pytest.mark.parametrize(
    ("exact", "position"),
    ((b"ab", 0), (b"ab", 1), (b"x", 0)),
)
def test_d2_result_without_exactly_two_references_cannot_assign_shared_position(
    exact, position
):
    ledger = EventLedger()
    locality = "insufficient-d2-pair-position"
    _source, _direct_result, determination_result = _direct_d2(
        ledger,
        locality=locality,
        exact=exact,
        position=position,
    )
    before = len(ledger.list())

    with pytest.raises(SharedPairPositionError, match="exactly two ordered"):
        record_shared_position_subject_to_act_binding_from_addressed_byte_occurrence_reference_determination_result(
            ledger,
            determination_result_event_identity=determination_result.identity,
            current_coordinates=_current_coordinates(ledger, locality),
        )
    assert len(ledger.list()) == before


def test_d2_repeated_material_keeps_two_source_ordered_assertion_addresses():
    ledger = EventLedger()
    locality = "repeated-d2-pair-position"
    _source, _direct_result, determination_result = _direct_d2(
        ledger,
        locality=locality,
        exact=b"aaa",
        position=1,
    )

    binding = record_shared_position_subject_to_act_binding_from_addressed_byte_occurrence_reference_determination_result(
        ledger,
        determination_result_event_identity=determination_result.identity,
        current_coordinates=_current_coordinates(ledger, locality),
    )

    first = binding.material["first_position_assertion"]
    second = binding.material["second_position_assertion"]
    assert first["exact_pair"] == second["exact_pair"] == [ord("a"), ord("a")]
    assert first["assertion_reference"] != second["assertion_reference"]
    assert (first["first_position"], second["first_position"]) == (0, 1)


def test_d2_shared_binding_requires_exact_current_coordinates_atomically():
    ledger = EventLedger()
    locality = "current-d2-pair-position"
    _source, _direct_result, determination_result = _direct_d2(
        ledger, locality=locality
    )
    stale = _current_coordinates(ledger, locality)
    record_witness_material_source(
        ledger,
        locality_identity=locality,
        exact_bytes=b"later",
        source_boundary="later material boundary",
    )
    before = len(ledger.list())
    with pytest.raises(SharedPairPositionError, match="current coordinates"):
        record_shared_position_subject_to_act_binding_from_addressed_byte_occurrence_reference_determination_result(
            ledger,
            determination_result_event_identity=determination_result.identity,
            current_coordinates=stale,
        )
    assert len(ledger.list()) == before

    changed_coordinates = deepcopy(_current_coordinates(ledger, locality))
    changed_coordinates["measurement_occurrences"][determination_result.identity][
        "result_identity"
    ] = "changed-result"
    with pytest.raises(SharedPairPositionError, match="current coordinates"):
        record_shared_position_subject_to_act_binding_from_addressed_byte_occurrence_reference_determination_result(
            ledger,
            determination_result_event_identity=determination_result.identity,
            current_coordinates=changed_coordinates,
        )
    assert len(ledger.list()) == before


def test_d2_result_corruption_invalidates_shared_binding_reader():
    ledger = EventLedger()
    locality = "corrupted-d2-pair-position"
    _source, _direct_result, determination_result = _direct_d2(
        ledger, locality=locality
    )
    binding = record_shared_position_subject_to_act_binding_from_addressed_byte_occurrence_reference_determination_result(
        ledger,
        determination_result_event_identity=determination_result.identity,
        current_coordinates=_current_coordinates(ledger, locality),
    )
    applicability_act = record_shared_position_applicability_act_occurrence(
        ledger,
        binding_event_identity=binding.identity,
        current_coordinates=_current_coordinates(ledger, locality),
    )

    determination_result.material["determination_rule"] = "changed rule"

    with pytest.raises(SharedPairPositionError):
        get_shared_position_subject_to_act_binding(ledger, binding.identity)
    with pytest.raises(SharedPairPositionError):
        get_shared_position_applicability_act_occurrence(
            ledger, applicability_act.identity
        )


@pytest.mark.parametrize("callback_kind", ("append", "mutate"))
def test_d2_shared_binding_revalidates_after_callback_atomically(
    monkeypatch, callback_kind
):
    ledger = EventLedger()
    locality = "callback-d2-pair-position"
    _source, _direct_result, determination_result = _direct_d2(
        ledger, locality=locality
    )
    current_coordinates = _current_coordinates(ledger, locality)
    coordinates_before = deepcopy(current_coordinates)
    original = shared_position_module._d2_result_inputs
    calls = 0

    def callback_after_read(*args, **kwargs):
        nonlocal calls
        reading = original(*args, **kwargs)
        calls += 1
        if calls == 3:
            if callback_kind == "append":
                ledger.append(
                    "test.callback.unrelated",
                    {"source": "callback"},
                    locality_identity=locality,
                )
            else:
                determination_result.material["determination_rule"] = (
                    "changed during callback"
                )
        return reading

    monkeypatch.setattr(
        shared_position_module,
        "_d2_result_inputs",
        callback_after_read,
    )
    before_assignments = len(
        tuple(ledger.iter_locality_kind(
            locality, SHARED_POSITION_MEASUREMENT_SUBJECT_TO_ACT_BINDING_RECORDED_KIND
        ))
    )

    with pytest.raises(SharedPairPositionError):
        record_shared_position_subject_to_act_binding_from_addressed_byte_occurrence_reference_determination_result(
            ledger,
            determination_result_event_identity=determination_result.identity,
            current_coordinates=current_coordinates,
        )

    assert current_coordinates == coordinates_before
    assert len(
        tuple(ledger.iter_locality_kind(
            locality, SHARED_POSITION_MEASUREMENT_SUBJECT_TO_ACT_BINDING_RECORDED_KIND
        ))
    ) == before_assignments


def test_later_direct_occurrence_read_requires_binding_carried_exact_coordinates(
    monkeypatch,
):
    ledger = EventLedger()
    locality = "carried-direct-pair-position"
    _source, direct_result, determination_result = _direct_d2(
        ledger, locality=locality
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
    binding = record_shared_position_subject_to_act_binding_from_addressed_byte_occurrence_reference_determination_result(
        ledger,
        determination_result_event_identity=determination_result.identity,
        current_coordinates=_current_coordinates(ledger, locality),
    )

    def raw_direct_resolver_is_not_needed(*_args, **_kwargs):
        raise AssertionError("D.2-derived binding reread raw direct inputs")

    monkeypatch.setattr(
        shared_position_module,
        "references_to_addressed_recorded_position_coordinates_of_byte_pair_occurrences",
        raw_direct_resolver_is_not_needed,
    )
    applicability_act = record_shared_position_applicability_act_occurrence(
        ledger,
        binding_event_identity=binding.identity,
        current_coordinates=_current_coordinates(ledger, locality),
    )
    applicability = record_shared_position_applicability_result(
        ledger,
        applicability_act_occurrence_event_identity=applicability_act.identity,
    )
    measurement_act = record_shared_position_measurement_act_occurrence(
        ledger,
        applicability_result_event_identity=applicability.identity,
        current_coordinates=_current_coordinates(ledger, locality),
    )
    result = record_shared_position_measurement_result(
        ledger,
        measurement_act_occurrence_event_identity=measurement_act.identity,
    )

    assert get_recorded_shared_position_measurement(ledger, result.identity)[
        "assertions"
    ][0]["dimensions"]["content"][
        "shared_position_coordinate_reference"
    ] == _position_coordinate_reference(first, "second")


def test_positions_that_do_not_meet_are_inapplicable_and_cannot_participate():
    ledger, locality, _source, first, second = _fixture(current=b"ab--bc")
    binding = _shared_binding(ledger, locality, first, second)
    act = record_shared_position_applicability_act_occurrence(
        ledger,
        binding_event_identity=binding.identity,
        current_coordinates=_current_coordinates(ledger, locality),
    )
    result = record_shared_position_applicability_result(
        ledger,
        applicability_act_occurrence_event_identity=act.identity,
    )

    assert get_recorded_shared_position_applicability(ledger, result.identity)[
        "applicability"
    ] == "inapplicable"
    with pytest.raises(SharedPairPositionError):
        record_shared_position_measurement_act_occurrence(
            ledger,
            applicability_result_event_identity=result.identity,
            current_coordinates=_current_coordinates(ledger, locality),
        )


def test_one_act_cannot_yield_two_shared_position_results():
    ledger, locality, _source, first, second = _fixture()
    binding = _shared_binding(ledger, locality, first, second)
    act = record_shared_position_applicability_act_occurrence(
        ledger,
        binding_event_identity=binding.identity,
        current_coordinates=_current_coordinates(ledger, locality),
    )
    record_shared_position_applicability_result(
        ledger,
        applicability_act_occurrence_event_identity=act.identity,
    )

    with pytest.raises(SharedPairPositionError):
        record_shared_position_applicability_result(
            ledger,
            applicability_act_occurrence_event_identity=act.identity,
        )


def test_aggregate_pair_findings_cannot_impersonate_occurrence_bound_positions():
    ledger, locality, _source, first, second = _fixture()

    with pytest.raises(ValueError):
        record_shared_position_subject_to_act_binding(
            ledger,
            first_result_occurrence_identity=(
                first.pair_measurement_occurrence_identity
            ),
            first_assertion_address=first.recurrence_assertion_position,
            second_result_occurrence_identity=(
                second.recorded_occurrence_identity
            ),
            second_assertion_address=second.assertion_address,
            current_coordinates=_current_coordinates(ledger, locality),
        )


def test_each_new_elevator_crossing_is_read_from_its_exact_occurrences():
    ledger, locality, _source, first, second = _fixture()
    binding, applicability_act, applicability, measurement_act, result = (
        _record_path(ledger, locality, first, second)
    )
    crossings = (
        (
            binding,
            lambda: get_shared_position_subject_to_act_binding(
                ledger, binding.identity
            ),
        ),
        (
            applicability_act,
            lambda: get_shared_position_applicability_act_occurrence(
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
            lambda: get_shared_position_measurement_act_occurrence(
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


def test_each_shared_position_occurrence_read_requires_exact_input_coordinates(
    monkeypatch,
):
    ledger, locality, _source, first, second = _fixture()
    binding = _shared_binding(ledger, locality, first, second)
    applicability_act = record_shared_position_applicability_act_occurrence(
        ledger,
        binding_event_identity=binding.identity,
        current_coordinates=_current_coordinates(ledger, locality),
    )
    applicability = record_shared_position_applicability_result(
        ledger,
        applicability_act_occurrence_event_identity=applicability_act.identity,
    )
    current_coordinates = _current_coordinates(ledger, locality)
    original = shared_position_module._inputs
    calls = []

    def counted(ledger, **identities):
        calls.append(tuple(identities.values()))
        return original(ledger, **identities)

    monkeypatch.setattr(shared_position_module, "_inputs", counted)
    expected_call = (
        first.recorded_occurrence_identity,
        first.assertion_address,
        second.recorded_occurrence_identity,
        second.assertion_address,
        current_coordinates,
    )
    independently_read_call = (*expected_call[:-1], None)

    measurement_act = record_shared_position_measurement_act_occurrence(
        ledger,
        applicability_result_event_identity=applicability.identity,
        current_coordinates=current_coordinates,
    )
    assert calls == [expected_call]

    result = record_shared_position_measurement_result(
        ledger,
        measurement_act_occurrence_event_identity=measurement_act.identity,
    )
    assert calls == [expected_call, independently_read_call]

    get_shared_position_measurement_act_occurrence(ledger, measurement_act.identity)
    assert calls == [expected_call, independently_read_call, independently_read_call]

    get_recorded_shared_position_measurement(ledger, result.identity)
    assert calls == [
        expected_call,
        independently_read_call,
        independently_read_call,
        independently_read_call,
    ]

    get_recorded_shared_position_measurement(ledger, result.identity)
    assert calls == [
        expected_call,
        independently_read_call,
        independently_read_call,
        independently_read_call,
        independently_read_call,
    ]


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
        yield_relation = ledger.get(event.material["yield_relation_identity"])
        assert yield_relation is not None
        result_identity = yield_relation.material["result_identity"]
        yield_relation.material["result_identity"] = "changed-result"
        with pytest.raises(SharedPairPositionError):
            read(ledger, event.identity)
        yield_relation.material["result_identity"] = result_identity


def test_shared_position_result_survives_sqlite_restart(restarted_shared_path):
    reopened = SQLiteEventLedger(str(restarted_shared_path["database"]))
    try:
        result_identity = restarted_shared_path["result_identity"]
        binding = restarted_shared_path["binding"]
        reading = get_recorded_shared_position_measurement(
            reopened, result_identity
        )

        assert reading["assertions"][0]["result"] == "ordered_relation_path"
        assert get_shared_position_subject_to_act_binding(
            reopened, binding.identity
        ) == binding.material
        assert result_identity in _current_coordinates(
            reopened, restarted_shared_path["locality"]
        )["measurement_occurrences"]
    finally:
        reopened.close()


def test_d2_derived_shared_position_provenance_survives_sqlite_restart(tmp_path):
    database = tmp_path / "d2-shared-position.sqlite"
    locality = "restarted-d2-shared-position"
    ledger = SQLiteEventLedger(str(database))
    _source, _direct_result, determination_result = _direct_d2(
        ledger, locality=locality
    )
    binding, _app_act, _applicability, _act, result = _record_d2_shared_path(
        ledger, locality, determination_result
    )
    binding_identity = binding.identity
    result_identity = result.identity
    determination_identity = determination_result.identity
    ledger.close()

    reopened = SQLiteEventLedger(str(database))
    binding_reading = get_shared_position_subject_to_act_binding(
        reopened, binding_identity
    )
    result_reading = get_recorded_shared_position_measurement(
        reopened, result_identity
    )

    assert binding_reading[
        shared_position_module.D2_RESULT_REFERENCE_COORDINATE
    ]["recorded_occurrence_identity"] == determination_identity
    assert result_reading["assertions"][0]["result"] == "ordered_relation_path"
    assert result_identity in _current_coordinates(reopened, locality)[
        "measurement_occurrences"
    ]
    reopened.close()


def test_one_complete_shared_measurement_reads_two_exact_bindings(
    monkeypatch,
):
    ledger, locality, _source, first, second = _fixture()
    binding, applicability_act, _applicability, _measurement_act, result = (
        _record_path(ledger, locality, first, second)
    )
    original = operator_current_coordinates_module._read_shared_position_binding
    calls = []

    def counted(*args, **kwargs):
        calls.append(args[1])
        return original(*args, **kwargs)

    monkeypatch.setattr(
        operator_current_coordinates_module,
        "_read_shared_position_binding",
        counted,
    )

    current_coordinates = _current_coordinates(ledger, locality)

    applicability_binding_identity = applicability_act.material[
        "subject_to_act_binding_reference"
    ]["recorded_occurrence_identity"]
    assert calls == [binding.identity, applicability_binding_identity]
    assert result.identity in current_coordinates["measurement_occurrences"]


_EXACT_OCCURRENCE_COORDINATES_REQUIRED_BY_CARRIED_STANDING = (
    ("input_result_occurrences", "result"),
    ("source_occurrences", "source"),
    ("pair_measurement_result_occurrences", "pair"),
    ("subject_to_act_binding_occurrences", "recurrent_binding"),
    ("act_occurrence_occurrences", "recurrent_act"),
    ("yield_relation_occurrences", "recurrent_yield"),
)


@pytest.mark.parametrize(
    ("reading_coordinate", "input_coordinate"),
    _EXACT_OCCURRENCE_COORDINATES_REQUIRED_BY_CARRIED_STANDING,
)
def test_current_coordinates_require_each_exact_occurrence_coordinate_intact(
    monkeypatch, reading_coordinate, input_coordinate
):
    ledger, locality, _source, first, second = _fixture()
    _record_path(ledger, locality, first, second)
    original = operator_current_coordinates_module._advance_shared_position_replay_reading
    changed = False

    def change_before_applicability(ledger, reading, event):
        nonlocal changed
        if (
            not changed
            and event.kind == SHARED_POSITION_APPLICABILITY_ACT_OCCURRENCE_EVENT
        ):
            recurrent = _recurrent_result_coordinates(ledger, first)
            identities = {
                "result": first.recorded_occurrence_identity,
                "source": first.source_material_result_occurrence_identity,
                "pair": first.pair_measurement_occurrence_identity,
                "recurrent_binding": recurrent["binding"].identity,
                "recurrent_act": recurrent["act"].identity,
                "recurrent_yield": recurrent["yield_relation"].identity,
            }
            target = next(
                occurrence
                for occurrence in getattr(reading, reading_coordinate)
                if occurrence.event.identity == identities[input_coordinate]
            )
            target.event.material["changed_between_shared_replay_occurrences"] = True
            changed = True
        return original(ledger, reading, event)

    monkeypatch.setattr(
        operator_current_coordinates_module,
        "_advance_shared_position_replay_reading",
        change_before_applicability,
    )

    with pytest.raises(SharedPairPositionError, match="intact"):
        _current_coordinates(ledger, locality)
    assert changed is True


def test_carried_coordinates_require_the_shared_binding_occurrence_intact(
    monkeypatch,
):
    ledger, locality, _source, first, second = _fixture()
    _record_path(ledger, locality, first, second)
    original = operator_current_coordinates_module._advance_shared_position_replay_reading
    changed = False

    def change_before_applicability(ledger, reading, event):
        nonlocal changed
        if (
            not changed
            and event.kind == SHARED_POSITION_APPLICABILITY_ACT_OCCURRENCE_EVENT
        ):
            reading.binding_occurrence.event.material[
                "changed_between_shared_replay_occurrences"
            ] = True
            changed = True
        return original(ledger, reading, event)

    monkeypatch.setattr(
        operator_current_coordinates_module,
        "_advance_shared_position_replay_reading",
        change_before_applicability,
    )

    with pytest.raises(SharedPairPositionError, match="intact"):
        _current_coordinates(ledger, locality)
    assert changed is True


_LATER_SHARED_OCCURRENCE_COORDINATES_REQUIRED_BY_CARRIED_STANDING = (
    (
        SHARED_POSITION_APPLICABILITY_RESULT_KIND,
        "applicability_act_occurrence",
    ),
    (
        SHARED_POSITION_MEASUREMENT_ACT_OCCURRENCE_EVENT,
        "applicability_result_occurrence",
    ),
    (
        SHARED_POSITION_MEASUREMENT_RESULT_KIND,
        "measurement_act_occurrence",
    ),
)


@pytest.mark.parametrize(
    ("occurrence_kind", "reading_coordinate"),
    _LATER_SHARED_OCCURRENCE_COORDINATES_REQUIRED_BY_CARRIED_STANDING,
)
def test_current_coordinates_require_each_later_shared_occurrence_intact(
    monkeypatch, occurrence_kind, reading_coordinate
):
    ledger, locality, _source, first, second = _fixture()
    _record_path(ledger, locality, first, second)
    original = operator_current_coordinates_module._advance_shared_position_replay_reading
    changed = False

    def change_before_next_occurrence(ledger, reading, event):
        nonlocal changed
        if not changed and event.kind == occurrence_kind:
            occurrence = getattr(reading, reading_coordinate)
            occurrence.event.material[
                "changed_between_shared_replay_occurrences"
            ] = True
            changed = True
        return original(ledger, reading, event)

    monkeypatch.setattr(
        operator_current_coordinates_module,
        "_advance_shared_position_replay_reading",
        change_before_next_occurrence,
    )

    with pytest.raises(SharedPairPositionError, match="intact"):
        _current_coordinates(ledger, locality)
    assert changed is True


def test_operator_replay_refuses_a_substituted_shared_binding(monkeypatch):
    ledger, locality, _source, first, second = _fixture()
    _record_path(ledger, locality, first, second)
    original = operator_current_coordinates_module._advance_shared_position_replay_reading
    substituted = False

    def substitute_before_applicability(ledger, reading, event):
        nonlocal substituted
        if not substituted:
            binding, inputs = reading.binding_reading
            reading.binding_reading = (deepcopy(binding), inputs)
            substituted = True
        return original(ledger, reading, event)

    monkeypatch.setattr(
        operator_current_coordinates_module,
        "_advance_shared_position_replay_reading",
        substitute_before_applicability,
    )

    with pytest.raises(SharedPairPositionError, match="substituted"):
        _current_coordinates(ledger, locality)


def test_operator_shared_replay_starts_fresh_after_exception(monkeypatch):
    ledger, locality, _source, first, second = _fixture()
    _shared_binding, _applicability_act, _applicability, _measurement_act, result = (
        _record_path(ledger, locality, first, second)
    )
    original = operator_current_coordinates_module._advance_shared_position_replay_reading
    interrupted = False

    def interrupt_once(ledger, reading, event):
        nonlocal interrupted
        if not interrupted:
            interrupted = True
            raise RuntimeError("interrupt shared replay")
        return original(ledger, reading, event)

    monkeypatch.setattr(
        operator_current_coordinates_module,
        "_advance_shared_position_replay_reading",
        interrupt_once,
    )

    with pytest.raises(RuntimeError, match="interrupt shared replay"):
        _current_coordinates(ledger, locality)
    assert result.identity in _current_coordinates(ledger, locality)["measurement_occurrences"]


def test_operator_replay_passes_prior_coordinates_to_d2_derived_shared_readers(
    monkeypatch,
):
    ledger = EventLedger()
    locality = "bounded-replay-d2-shared-position"
    _source, _direct_result, determination_result = _direct_d2(
        ledger, locality=locality
    )
    _record_d2_shared_path(ledger, locality, determination_result)
    import seed_runtime.operator_current_coordinates as standing_module
    original = standing_module._read_shared_position_binding
    calls = []

    monkeypatch.setattr(
        standing_module,
        "_read_shared_position_binding",
        lambda *args, **kwargs: (
            calls.append(kwargs.get("prior_coordinates")),
            original(*args, **kwargs),
        )[1],
    )

    replayed = read_operator_current_coordinates(
        ledger, locality_identity=locality
    )
    assert replayed["through_event_occurrence_identity"] == ledger.list_locality(
        locality
    )[-1].identity
    assert calls
    assert all(prior is not None for prior in calls)


def test_current_coordinates_match_replay_for_the_complete_elevator():
    ledger, locality, _source, first, second = _fixture()
    prior = _current_coordinates(ledger, locality)
    prior_count = len(ledger.list_locality(locality))
    _record_path(ledger, locality, first, second)
    later = tuple(
        event.identity for event in ledger.list_locality(locality)[prior_count:]
    )

    carried = advance_operator_current_coordinates(
        ledger,
        later,
        locality_identity=locality,
        prior=prior,
    )

    assert carried == _current_coordinates(ledger, locality)




FIDELITY_DISTINCTIONS = {
    ("book_coordinates", "01.Current.E.1", "Applicability", "result"): (
        test_positions_that_do_not_meet_are_inapplicable_and_cannot_participate,
    ),
    ("book_coordinates", "01.Source.D", "result"): (
        test_exact_yielded_pair_relations_compose_at_one_shared_position,
        test_direct_position_coordinate_assertions_compose_without_recurrence_support,
        test_d2_result_without_exactly_two_references_cannot_assign_shared_position,
        test_d2_repeated_material_keeps_two_source_ordered_assertion_addresses,
        test_aggregate_pair_findings_cannot_impersonate_occurrence_bound_positions,
        test_shared_position_result_survives_sqlite_restart,
        test_d2_derived_shared_position_provenance_survives_sqlite_restart,
        test_one_complete_shared_measurement_reads_two_exact_bindings,
        test_current_coordinates_require_each_exact_occurrence_coordinate_intact,
        test_carried_coordinates_require_the_shared_binding_occurrence_intact,
        test_current_coordinates_require_each_later_shared_occurrence_intact,
        test_operator_replay_refuses_a_substituted_shared_binding,
        test_operator_shared_replay_starts_fresh_after_exception,
        test_operator_replay_passes_prior_coordinates_to_d2_derived_shared_readers,
        test_current_coordinates_match_replay_for_the_complete_elevator,
    ),
}


WITNESS_MATERIAL_TESTS = (
    test_ordered_path_exposes_input_position_assertion_coordinates_without_carrying_their_pair_material,
    test_ordered_source_positions_are_adjacent_to_the_path_assertion,
)
