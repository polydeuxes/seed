from tests.binary_input import binary_input
from collections import Counter as ExactCounter
from copy import deepcopy

import pytest

import seed_runtime.operator_locality_standing as operator_standing_module
from seed_runtime.byte_measurement import (
    BYTE_PAIR_MEASUREMENT_RECORDED_KIND,
    BYTE_PAIR_APPLICABILITY_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
    BYTE_PAIR_MEASUREMENT_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
    BYTE_PAIR_APPLICABILITY_RECORDED_KIND,
    BYTE_PAIR_RESULT_COORDINATES,
    BYTE_MEASUREMENT_RECORDED_KIND,
    BYTE_MEASUREMENT_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
    BYTE_MEASUREMENT_RESPONSIBLE_ACT_OCCURRENCE_EVENT,
    ASSERTION_LOCALITY_MOVEMENT_SUBJECT_TO_ACT_BINDING_KIND,
    BYTE_RESULT_COORDINATES,
    BYTE_MEASUREMENT_RULE,
    BYTE_PAIR_MEASUREMENT_RULE,
    ByteMeasurementError,
    _measure_byte_counts_through,
    _record_assertion_locality_movement_act_from_current_coordinates,
    _record_assertion_locality_movement_result_from_current_coordinates,
    _record_byte_measurement_result_from_carried_act_occurrence,
    _record_movement_binding_from_current_coordinates,
    _validate_moved_byte_assertion,
    get_byte_position_pair_measurement_subject_to_act_binding,
    get_recorded_pair_input_applicability,
    get_byte_measurement_subject_to_act_binding,
    get_assertion_locality_movement_subject_to_act_binding,
    assertions_of_recorded_byte_measurement,
    assertions_of_recorded_byte_position_pair_measurement,
    input_applicability_of_recorded_byte_position_pair_measurement,
    measure_byte_counts,
    record_byte_measurement_subject_to_act_binding,
    record_byte_measurement_act_occurrence,
    record_byte_measurement_result,
    record_assertion_locality_movement_subject_to_act_binding,
    record_assertion_locality_movement_act_occurrence,
    record_assertion_locality_movement_result,
    move_recorded_byte_assertion_to_locality,
    move_recorded_byte_assertions_to_locality,
    record_byte_position_pair_count_layer,
)
from seed_runtime.events import CORRUPTED, EventLedger, SQLiteEventLedger
from seed_runtime.event import Event
from seed_runtime.operator_console import run_persistent_operator_console
from seed_runtime.operator_locality_standing import (
    _carry_assertion_locality_movement_act_into_standing,
    _carry_assertion_locality_movement_binding_into_current_coordinates,
    _carry_assertion_locality_movement_result_into_standing,
    _carry_byte_measurement_assignment_into_standing,
    advance_operator_locality_standing,
    read_operator_locality_standing,
    read_operator_locality_standing_through,
)
from seed_runtime.yield_relation import RECORDED_YIELD_RELATION_EVENT
from seed_runtime.material_source import (
    iter_exact_material_results,
)
from tests.operator_material_source_test_witness import (
    record_operator_material_occurrence,
)


def _record_operator_material_source(
    ledger,
    *,
    locality_identity,
    exact_bytes,
    source_boundary,
):
    return record_operator_material_occurrence(
        ledger,
        exact=exact_bytes,
        locality_identity=locality_identity,
        source_boundary=source_boundary,
    )


def _record_byte_measurement(
    ledger, *, source_localities, recording_locality_identity
):
    assignment = record_byte_measurement_subject_to_act_binding(
        ledger,
        source_localities=source_localities,
        recording_locality_identity=recording_locality_identity,
        locality_standing=read_operator_locality_standing(
            ledger, locality_identity=recording_locality_identity
        ),
    )
    act_occurrence = record_byte_measurement_act_occurrence(
        ledger,
        responsibility_assignment_event_identity=assignment.identity,
        responsibility_assignment_standing=read_operator_locality_standing(
            ledger, locality_identity=recording_locality_identity
        ),
    )
    return record_byte_measurement_result(
        ledger,
        act_occurrence_event_identity=act_occurrence.identity,
    )


def _record_byte_measurement_assignment_and_act(
    ledger, *, source_localities, recording_locality_identity
):
    assignment = record_byte_measurement_subject_to_act_binding(
        ledger,
        source_localities=source_localities,
        recording_locality_identity=recording_locality_identity,
        locality_standing=read_operator_locality_standing(
            ledger, locality_identity=recording_locality_identity
        ),
    )
    act = record_byte_measurement_act_occurrence(
        ledger,
        responsibility_assignment_event_identity=assignment.identity,
        responsibility_assignment_standing=read_operator_locality_standing(
            ledger, locality_identity=recording_locality_identity
        ),
    )
    return assignment, act


class IntegrityCountingLedger(EventLedger):
    def __init__(self):
        super().__init__()
        self.integrity_calls = ExactCounter()
        self.corrupted = set()

    def integrity_of(self, event_identity):
        self.integrity_calls[event_identity] += 1
        if event_identity in self.corrupted:
            return CORRUPTED
        return super().integrity_of(event_identity)


class YieldCallbackLedger(EventLedger):
    def __init__(self):
        super().__init__()
        self.callback_boundary = None
        self.callback_recorded = False

    def append(self, kind, material, **kwargs):
        event = super().append(kind, material, **kwargs)
        if (
            not self.callback_recorded
            and self.callback_boundary is not None
            and kind == RECORDED_YIELD_RELATION_EVENT
            and material.get("occurrence_boundary") == self.callback_boundary
        ):
            self.callback_recorded = True
            super().append(
                "test.unrelated_callback",
                {"unknown": ["unrelated append after Yield"]},
                locality_identity="unrelated",
            )
        return event


def _ledger(exact_material: bytes):
    if type(exact_material) is not bytes:
        raise TypeError("byte Measurement fixture requires exact bytes")
    ledger = EventLedger()
    for position, exact in enumerate(exact_material.splitlines(keepends=True)):
        _record_operator_material_source(
            ledger,
            locality_identity="source",
            exact_bytes=exact,
            source_boundary=f"fixture operator material {position}",
        )
    return ledger


def _byte_source(ledger):
    return _record_byte_measurement(
        ledger,
        source_localities=("source",),
        recording_locality_identity="byte-measurement",
    )


def _movement_source(ledger):
    result = _byte_source(ledger)
    source = next(
        assertion
        for assertion in assertions_of_recorded_byte_measurement(
            ledger, result.identity
        )
        if assertion.result == "exact_source_material_set"
    )
    return result, source


def _movement_carry_phase(ledger, phase):
    source_result, source = _movement_source(ledger)
    source_event = ledger.get(source.recorded_occurrence_identity)
    source_standing = read_operator_locality_standing(
        ledger, locality_identity=source_result.locality_identity
    )
    destination_standing = read_operator_locality_standing(
        ledger, locality_identity="movement-carry"
    )
    assignment = _record_movement_binding_from_current_coordinates(
        ledger,
        source=source,
        source_event=source_event,
        source_coordinates=source_standing,
        destination_locality="movement-carry",
        destination_coordinates=destination_standing,
    )
    state = {
        "phase": phase,
        "source_result": source_result,
        "source": source,
        "source_event": source_event,
        "source_standing": source_standing,
        "destination_standing": destination_standing,
        "assignment": assignment,
        "event": assignment,
    }
    if phase == "assignment":
        return state
    destination_standing = (
        _carry_assertion_locality_movement_binding_into_current_coordinates(
            ledger,
            destination_standing,
            assignment,
            source=source,
            source_event=source_event,
            source_standing=source_standing,
        )
    )
    act = _record_assertion_locality_movement_act_from_current_coordinates(
        ledger,
        binding=assignment,
        destination_coordinates=destination_standing,
    )
    state.update(
        destination_coordinates=destination_standing,
        act=act,
        event=act,
    )
    if phase == "act":
        return state
    destination_standing = _carry_assertion_locality_movement_act_into_standing(
        ledger,
        destination_standing,
        act,
        responsibility_assignment=assignment,
    )
    movement = _record_assertion_locality_movement_result_from_current_coordinates(
        ledger,
        act=act,
        binding=assignment,
    )
    state.update(
        destination_coordinates=destination_standing,
        movement=movement,
        event=movement,
    )
    return state


def _carry_movement_phase(
    ledger,
    state,
    *,
    source=None,
    responsibility_assignment=None,
):
    source = state["source"] if source is None else source
    responsibility_assignment = (
        state["assignment"]
        if responsibility_assignment is None
        else responsibility_assignment
    )
    if state["phase"] == "assignment":
        return _carry_assertion_locality_movement_binding_into_current_coordinates(
            ledger,
            state["destination_standing"],
            state["assignment"],
            source=source,
            source_event=state["source_event"],
            source_standing=state["source_standing"],
        )
    if state["phase"] == "act":
        return _carry_assertion_locality_movement_act_into_standing(
            ledger,
            state["destination_standing"],
            state["act"],
            responsibility_assignment=responsibility_assignment,
        )
    return _carry_assertion_locality_movement_result_into_standing(
        ledger,
        state["destination_standing"],
        state["movement"],
        act_occurrence=state["act"],
        responsibility_assignment=responsibility_assignment,
        source=source,
    )


def test_act_occurrence_is_observable_before_yield_and_result():
    ledger = _ledger(b"a\n")

    assignment, act_occurrence = _record_byte_measurement_assignment_and_act(
        ledger,
        source_localities=("source",),
        recording_locality_identity="measurement",
    )

    assert act_occurrence.kind == BYTE_MEASUREMENT_RESPONSIBLE_ACT_OCCURRENCE_EVENT
    assert ledger.list_locality("measurement") == [assignment, act_occurrence]
    assert act_occurrence.material["source_localities"] == ["source"]
    assert act_occurrence.material["subject_to_act_binding_reference"][
        "recorded_occurrence_identity"
    ] == assignment.identity

    result = record_byte_measurement_result(
        ledger,
        act_occurrence_event_identity=act_occurrence.identity,
    )
    events = ledger.list_locality("measurement")
    assert [event.kind for event in events] == [
        BYTE_MEASUREMENT_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
        BYTE_MEASUREMENT_RESPONSIBLE_ACT_OCCURRENCE_EVENT,
        RECORDED_YIELD_RELATION_EVENT,
        BYTE_MEASUREMENT_RECORDED_KIND,
    ]
    assert result.material["act_occurrence_event_identity"] == act_occurrence.identity
    assert result.material["yield_relation_identity"] == events[2].identity
    assert ledger.occurrences_in_append_order(
        (assignment.identity, act_occurrence.identity, events[2].identity, result.identity),
        locality_identity="measurement",
    ) == events


def test_exact_byte_assignment_enters_standing_and_owns_distinct_lifecycle_identities():
    ledger = _ledger(b"a\n")
    assignment = record_byte_measurement_subject_to_act_binding(
        ledger,
        source_localities=("source",),
        recording_locality_identity="measurement",
        locality_standing=read_operator_locality_standing(
            ledger, locality_identity="measurement"
        ),
    )
    standing = read_operator_locality_standing(
        ledger, locality_identity="measurement"
    )

    assert assignment.kind == BYTE_MEASUREMENT_SUBJECT_TO_ACT_BINDING_RECORDED_KIND
    assert standing["subject_to_act_binding_occurrences"].get(
        assignment.identity, object()
    ) is None
    assert "standing" not in assignment.material
    act = record_byte_measurement_act_occurrence(
        ledger,
        responsibility_assignment_event_identity=assignment.identity,
        responsibility_assignment_standing=standing,
    )
    result = record_byte_measurement_result(
        ledger, act_occurrence_event_identity=act.identity
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
    assert result.material["subject_to_act_binding_reference"] == {
        "recorded_occurrence_identity": assignment.identity,
        "book_clause_identity": assignment.material["book_clause_identity"],
        "exact_act_identity": assignment.material["exact_act_identity"],
        "subject_reference": assignment.material["subject_reference"],
        "result_boundary_identity": assignment.material[
            "result_boundary_identity"
        ],
    }
    assert "responsibility_assignment" not in act.material
    assert "responsibility_assignment" not in result.material


def test_stale_and_shaped_coordinates_cannot_carry_exact_byte_act():
    ledger = _ledger(b"a\n")
    stale = read_operator_locality_standing(
        ledger, locality_identity="measurement"
    )
    assignment = record_byte_measurement_subject_to_act_binding(
        ledger,
        source_localities=("source",),
        recording_locality_identity="measurement",
        locality_standing=stale,
    )
    shaped = deepcopy(
        read_operator_locality_standing(ledger, locality_identity="measurement")
    )
    shaped["subject_to_act_binding_occurrences"] = {
        "same-shaped-assignment": None
    }

    for coordinates in (stale, shaped):
        with pytest.raises(
            ByteMeasurementError, match="exact current Locality coordinates"
        ):
            record_byte_measurement_act_occurrence(
                ledger,
                responsibility_assignment_event_identity=assignment.identity,
                responsibility_assignment_standing=coordinates,
            )


def test_assignment_read_refuses_corrupted_unrelated_prior_standing_carrier():
    ledger = IntegrityCountingLedger()
    _record_operator_material_source(
        ledger,
        locality_identity="measurement",
        exact_bytes=b"ab",
        source_boundary="test boundary",
    )
    first = _record_byte_measurement(
        ledger,
        source_localities=("measurement",),
        recording_locality_identity="measurement",
    )
    second = record_byte_measurement_subject_to_act_binding(
        ledger,
        source_localities=("measurement",),
        recording_locality_identity="measurement",
        locality_standing=read_operator_locality_standing(
            ledger, locality_identity="measurement"
        ),
    )
    ledger.corrupted.add(first.identity)

    with pytest.raises(ByteMeasurementError):
        get_byte_measurement_subject_to_act_binding(ledger, second.identity)


def test_operator_replay_uses_exact_context_while_public_assignment_reads_reconstruct(
    monkeypatch,
):
    from seed_runtime import operator_locality_standing as standing_module

    ledger = IntegrityCountingLedger()
    _record_operator_material_source(
        ledger,
        locality_identity="measurement",
        exact_bytes=b"ab",
        source_boundary="test boundary",
    )
    first = _record_byte_measurement(
        ledger,
        source_localities=("measurement",),
        recording_locality_identity="measurement",
    )
    second = record_byte_measurement_subject_to_act_binding(
        ledger,
        source_localities=("measurement",),
        recording_locality_identity="measurement",
        locality_standing=read_operator_locality_standing(
            ledger, locality_identity="measurement"
        ),
    )
    original_read_through = (
        standing_module.read_operator_locality_standing_through
    )

    def refuse_nested_replay(*_args, **_kwargs):
        raise AssertionError("nested operator Standing replay")

    monkeypatch.setattr(
        standing_module,
        "read_operator_locality_standing_through",
        refuse_nested_replay,
    )
    standing = read_operator_locality_standing(
        ledger, locality_identity="measurement"
    )
    assert standing["measurement_occurrences"][first.identity]
    assert standing["subject_to_act_binding_occurrences"][second.identity] is None
    with pytest.raises(AssertionError, match="nested operator Standing replay"):
        get_byte_measurement_subject_to_act_binding(ledger, second.identity)

    monkeypatch.setattr(
        standing_module,
        "read_operator_locality_standing_through",
        original_read_through,
    )
    assert get_byte_measurement_subject_to_act_binding(
        ledger, second.identity
    ) == second
    ledger.corrupted.add(first.identity)
    with pytest.raises(ByteMeasurementError):
        get_byte_measurement_subject_to_act_binding(ledger, second.identity)


def test_equal_copied_replay_accumulators_cannot_satisfy_public_assignment_read():
    from seed_runtime.operator_locality_standing import (
        _operator_standing_replay_validation,
        _set_operator_standing_validation_context,
    )

    ledger = IntegrityCountingLedger()
    _record_operator_material_source(
        ledger,
        locality_identity="measurement",
        exact_bytes=b"ab",
        source_boundary="test boundary",
    )
    first = _record_byte_measurement(
        ledger,
        source_localities=("measurement",),
        recording_locality_identity="measurement",
    )
    second = record_byte_measurement_subject_to_act_binding(
        ledger,
        source_localities=("measurement",),
        recording_locality_identity="measurement",
        locality_standing=read_operator_locality_standing(
            ledger, locality_identity="measurement"
        ),
    )
    exact = read_operator_locality_standing(
        ledger, locality_identity="measurement"
    )
    copied_measurements = deepcopy(exact["measurement_occurrences"])
    copied_acquisition_results = deepcopy(exact["material_acquisition_result_occurrences"])
    copied_assignments = deepcopy(exact["subject_to_act_binding_occurrences"])
    assert copied_measurements == exact["measurement_occurrences"]
    assert copied_measurements is not exact["measurement_occurrences"]
    assert copied_acquisition_results == exact["material_acquisition_result_occurrences"]
    assert copied_acquisition_results is not exact["material_acquisition_result_occurrences"]
    assert copied_assignments == exact["subject_to_act_binding_occurrences"]
    assert copied_assignments is not exact["subject_to_act_binding_occurrences"]
    ledger.corrupted.add(first.identity)

    @_operator_standing_replay_validation
    def read_from_forged_accumulators():
        with pytest.raises(ValueError, match="exact accumulators"):
            _set_operator_standing_validation_context(
                ledger,
                locality_identity="measurement",
                through_event_occurrence_identity=exact[
                    "through_event_occurrence_identity"
                ],
                measurement_occurrences=copied_measurements,
                material_acquisition_result_occurrences=copied_acquisition_results,
                subject_to_act_binding_occurrences=copied_assignments,
            )
        return get_byte_measurement_subject_to_act_binding(
            ledger, second.identity
        )

    with pytest.raises(ByteMeasurementError):
        read_from_forged_accumulators()


def test_assignment_act_and_result_survive_distinct_sqlite_restarts(tmp_path):
    path = tmp_path / "byte-assignment-restart.sqlite"
    ledger = SQLiteEventLedger(path)
    _record_operator_material_source(
        ledger,
        locality_identity="source",
        exact_bytes=b"durable",
        source_boundary="durable boundary",
    )
    assignment = record_byte_measurement_subject_to_act_binding(
        ledger,
        source_localities=("source",),
        recording_locality_identity="measurement",
        locality_standing=read_operator_locality_standing(
            ledger, locality_identity="measurement"
        ),
    )
    ledger.close()

    ledger = SQLiteEventLedger(path)
    assert get_byte_measurement_subject_to_act_binding(
        ledger, assignment.identity
    ).identity == assignment.identity
    act = record_byte_measurement_act_occurrence(
        ledger,
        responsibility_assignment_event_identity=assignment.identity,
        responsibility_assignment_standing=read_operator_locality_standing(
            ledger, locality_identity="measurement"
        ),
    )
    ledger.close()

    ledger = SQLiteEventLedger(path)
    result = record_byte_measurement_result(
        ledger, act_occurrence_event_identity=act.identity
    )
    ledger.close()

    ledger = SQLiteEventLedger(path)
    assert assertions_of_recorded_byte_measurement(ledger, result.identity)
    ledger.close()


def test_console_exact_byte_same_call_path_does_not_reread_current_coordinates(
    monkeypatch,
):
    from seed_runtime import byte_measurement

    def forbidden(*args, **kwargs):
        raise AssertionError("console byte lifecycle must use carried coordinates")

    monkeypatch.setattr(
        byte_measurement,
        "_require_current_byte_measurement_coordinates",
        forbidden,
    )
    monkeypatch.setattr(
        byte_measurement,
        "_require_byte_measurement_act_without_result",
        forbidden,
    )
    ledger = EventLedger()
    run_persistent_operator_console(
        ledger=ledger,
        locality_identity="source",
        input_stream=binary_input("a\n"),
    )
    assert any(
        event.kind == BYTE_MEASUREMENT_RECORDED_KIND
        for event in ledger.list_locality("source")
    )


def test_call_local_assignment_carry_requires_the_exact_assignment_at_tip():
    ledger = _ledger(b"a\n")
    standing = read_operator_locality_standing(
        ledger, locality_identity="measurement"
    )
    prior_boundary = standing["through_event_occurrence_identity"]
    assignment = record_byte_measurement_subject_to_act_binding(
        ledger,
        source_localities=("source",),
        recording_locality_identity="measurement",
        locality_standing=standing,
    )
    _record_operator_material_source(
        ledger,
        locality_identity="unrelated",
        exact_bytes=b"later",
        source_boundary="after assignment",
    )

    with pytest.raises(ValueError, match="must follow carried Standing"):
        _carry_byte_measurement_assignment_into_standing(
            ledger,
            standing,
            assignment,
            prior_through_event_occurrence_identity=prior_boundary,
        )


def test_call_local_result_requires_the_exact_act_at_tip():
    ledger = _ledger(b"a\n")
    assignment, act = _record_byte_measurement_assignment_and_act(
        ledger,
        source_localities=("source",),
        recording_locality_identity="measurement",
    )
    standing = read_operator_locality_standing(
        ledger, locality_identity="measurement"
    )
    _record_operator_material_source(
        ledger,
        locality_identity="unrelated",
        exact_bytes=b"later",
        source_boundary="after act",
    )

    with pytest.raises(
        ByteMeasurementError, match="exact carried lifecycle occurrences"
    ):
        _record_byte_measurement_result_from_carried_act_occurrence(
            ledger,
            act_occurrence=act,
            responsibility_assignment=assignment,
            locality_standing=standing,
        )


def test_call_local_result_rechecks_act_tip_after_source_callback(monkeypatch):
    from seed_runtime import byte_measurement

    ledger = _ledger(b"a\n")
    assignment, act = _record_byte_measurement_assignment_and_act(
        ledger,
        source_localities=("source",),
        recording_locality_identity="measurement",
    )
    standing = read_operator_locality_standing(
        ledger, locality_identity="measurement"
    )
    original = byte_measurement._material_result_bytes
    callback_recorded = False

    def record_public_result_during_source_read(ledger, acquisition_result):
        nonlocal callback_recorded
        if not callback_recorded:
            callback_recorded = True
            record_byte_measurement_result(
                ledger, act_occurrence_event_identity=act.identity
            )
        return original(ledger, acquisition_result)

    monkeypatch.setattr(
        byte_measurement,
        "_material_result_bytes",
        record_public_result_during_source_read,
    )
    with pytest.raises(ByteMeasurementError, match="Act at the append tip"):
        _record_byte_measurement_result_from_carried_act_occurrence(
            ledger,
            act_occurrence=act,
            responsibility_assignment=assignment,
            locality_standing=standing,
        )

    assert sum(
            event.kind == BYTE_MEASUREMENT_RECORDED_KIND
            and event.material.get("act_occurrence_event_identity") == act.identity
        for event in ledger.list()
    ) == 1
    assert sum(
        event.kind == RECORDED_YIELD_RELATION_EVENT
        and event.material.get("act_occurrence_event_identity") == act.identity
        for event in ledger.list()
    ) == 1


def test_reopened_public_result_refuses_an_act_already_consumed(tmp_path):
    path = tmp_path / "byte-consumed-act.sqlite"
    ledger = SQLiteEventLedger(path)
    _record_operator_material_source(
        ledger,
        locality_identity="source",
        exact_bytes=b"a",
        source_boundary="durable source",
    )
    _assignment, act = _record_byte_measurement_assignment_and_act(
        ledger,
        source_localities=("source",),
        recording_locality_identity="measurement",
    )
    record_byte_measurement_result(
        ledger, act_occurrence_event_identity=act.identity
    )
    ledger.close()

    ledger = SQLiteEventLedger(path)
    with pytest.raises(ByteMeasurementError, match="already has a Yield or result"):
        record_byte_measurement_result(
            ledger, act_occurrence_event_identity=act.identity
        )
    ledger.close()


def test_old_unassigned_exact_byte_act_api_is_not_accepted():
    ledger = _ledger(b"a\n")
    with pytest.raises(TypeError):
        record_byte_measurement_act_occurrence(
            ledger,
            source_localities=("source",),
            recording_locality_identity="measurement",
        )


def test_two_stages_traverse_byte_counts_once(monkeypatch):
    from seed_runtime import byte_measurement

    ledger = _ledger(b"ab\n")
    calls = []
    original = byte_measurement._measure_byte_counts_through

    def count(*args, **kwargs):
        calls.append(kwargs["boundary"].identity)
        return original(*args, **kwargs)

    monkeypatch.setattr(byte_measurement, "_measure_byte_counts_through", count)
    assignment, act_occurrence = _record_byte_measurement_assignment_and_act(
        ledger,
        source_localities=("source",),
        recording_locality_identity="measurement",
    )
    assert calls == []

    record_byte_measurement_result(
        ledger,
        act_occurrence_event_identity=act_occurrence.identity,
    )
    assert calls == [
        assignment.material["completeness_boundary_identity"]
    ]


def test_each_exact_material_acquisition_is_counted_once_without_losing_zero_occurrence_material(
    monkeypatch,
):
    from seed_runtime import byte_measurement

    ledger = EventLedger()
    materials = (
        b'{"function":"unobserved","occurrence_count":0}',
        b'{"function":"observed","occurrence_count":2}',
    )
    acquisition_results = tuple(
        _record_operator_material_source(
            ledger,
            locality_identity="measurement-sidecar",
            exact_bytes=material,
            source_boundary=f"sidecar-{position}",
        )
        for position, material in enumerate(materials)
    )
    counted_material = []

    def counted(exact):
        counted_material.append(exact)
        return ExactCounter(exact)

    monkeypatch.setattr(byte_measurement, "Counter", counted)

    measured = measure_byte_counts(
        ledger,
        source_localities=("measurement-sidecar",),
    )

    assert counted_material == list(materials)
    assert tuple(acquisition_result.exact_material for acquisition_result in acquisition_results) == materials
    assert b'"occurrence_count":0' in acquisition_results[0].exact_material
    expected_totals = ExactCounter(b"".join(materials))
    expected_carrying = {
        value: sum(value in material for material in materials)
        for value in expected_totals
    }
    assert {
        item.content: (item.occurrences_carrying, item.count)
        for item in measured.counts
    } == {
        value: (expected_carrying[value], count)
        for value, count in expected_totals.items()
    }


def test_each_replay_validates_each_exact_material_acquisition_and_reads_independently():
    ledger = IntegrityCountingLedger()
    materials = (
        b'{"function":"unobserved","occurrence_count":0}',
        b'{"function":"observed","occurrence_count":2}',
    )
    acquisition_results = tuple(
        _record_operator_material_source(
            ledger,
            locality_identity="measurement-sidecar",
            exact_bytes=material,
            source_boundary=f"sidecar-{position}",
        )
        for position, material in enumerate(materials)
    )
    _assignment, act_occurrence = _record_byte_measurement_assignment_and_act(
        ledger,
        source_localities=("measurement-sidecar",),
        recording_locality_identity="measurement-sidecar",
    )
    ledger.integrity_calls.clear()

    result = record_byte_measurement_result(
        ledger,
        act_occurrence_event_identity=act_occurrence.identity,
    )

    after_result = [ledger.integrity_calls[acquisition_result.identity] for acquisition_result in acquisition_results]
    assert all(count > 0 for count in after_result)
    assert tuple(acquisition_result.exact_material for acquisition_result in acquisition_results) == materials

    assert assertions_of_recorded_byte_measurement(ledger, result.identity)
    after_read = [ledger.integrity_calls[acquisition_result.identity] for acquisition_result in acquisition_results]
    assert all(after > before for after, before in zip(after_read, after_result))

    ledger.corrupted.add(acquisition_results[0].identity)
    with pytest.raises(ByteMeasurementError, match="without intact physiology"):
        assertions_of_recorded_byte_measurement(ledger, result.identity)


def test_yield_resolves_the_exact_act_occurrence_after_reopen(tmp_path):
    path = str(tmp_path / "measurement.sqlite")
    ledger = SQLiteEventLedger(path)
    _record_operator_material_source(
        ledger,
        locality_identity="source",
        exact_bytes=b"durable",
        source_boundary="durable boundary",
    )
    assignment, act_occurrence = _record_byte_measurement_assignment_and_act(
        ledger,
        source_localities=("source",),
        recording_locality_identity="measurement",
    )
    act_occurrence_identity = act_occurrence.identity
    assignment_identity = assignment.identity
    ledger.close()

    ledger = SQLiteEventLedger(path)
    try:
        result = record_byte_measurement_result(
            ledger,
            act_occurrence_event_identity=act_occurrence_identity,
        )
        assert result.material["act_occurrence_event_identity"] == (
            act_occurrence_identity
        )
        assert result.material["subject_to_act_binding_reference"][
            "recorded_occurrence_identity"
        ] == assignment_identity
        assert assertions_of_recorded_byte_measurement(ledger, result.identity)
    finally:
        ledger.close()


def test_material_appended_after_act_occurrence_cannot_enter_its_result():
    ledger = _ledger(b"a")
    _assignment, act_occurrence = _record_byte_measurement_assignment_and_act(
        ledger,
        source_localities=("source",),
        recording_locality_identity="measurement",
    )
    _record_operator_material_source(
        ledger,
        locality_identity="source",
        exact_bytes=b"b",
        source_boundary="later boundary",
    )

    result = record_byte_measurement_result(
        ledger,
        act_occurrence_event_identity=act_occurrence.identity,
    )
    counts = {
        item.content: item.material["dimensions"]["content"]["count"]
        for item in assertions_of_recorded_byte_measurement(ledger, result.identity)
        if item.result == "count"
    }
    assert counts == {97: 1}


def test_one_responsible_act_occurrence_cannot_yield_twice(monkeypatch):
    from seed_runtime import byte_measurement

    ledger = _ledger(b"a\n")
    _assignment, act_occurrence = _record_byte_measurement_assignment_and_act(
        ledger,
        source_localities=("source",),
        recording_locality_identity="measurement",
    )
    record_byte_measurement_result(
        ledger,
        act_occurrence_event_identity=act_occurrence.identity,
    )
    event_count = len(ledger.list())

    def forbidden(*args, **kwargs):
        raise AssertionError("a consumed Act occurrence must not be measured again")

    monkeypatch.setattr(byte_measurement, "_measure_byte_counts_through", forbidden)

    with pytest.raises(ByteMeasurementError, match="already has a Yield or result"):
        record_byte_measurement_result(
            ledger,
            act_occurrence_event_identity=act_occurrence.identity,
        )
    assert len(ledger.list()) == event_count


@pytest.mark.parametrize("identity", ("missing", None))
def test_yield_refuses_missing_act_occurrence(identity):
    with pytest.raises(ByteMeasurementError, match="exact responsible Act occurrence"):
        record_byte_measurement_result(
            EventLedger(),
            act_occurrence_event_identity=identity,
        )


def test_yield_refuses_a_different_occurrence_kind():
    ledger = _ledger(b"a\n")
    wrong = next(event for event in ledger.list() if event.locality_identity == "source")

    with pytest.raises(ByteMeasurementError, match="exact responsible Act occurrence"):
        record_byte_measurement_result(
            ledger,
            act_occurrence_event_identity=wrong.identity,
        )


def test_opaque_bytes_supply_the_measured_subjects_without_whitespace():
    ledger = EventLedger()
    _record_operator_material_source(
        ledger,
        locality_identity="source",
        exact_bytes=b"\xe7\x8c\xab\n",
        source_boundary="opaque byte fixture",
    )
    measured = measure_byte_counts(
        ledger, source_localities=("source",)
    )
    counts = {item.content: item for item in measured.counts}

    # No character encoding or character boundary is supplied or asserted.
    assert counts[231].count == 1
    assert counts[140].count == 1
    assert counts[171].count == 1
    assert counts[10].count == 1
    assert len(measured.source_material) == 1


def test_the_complete_declared_localities_supply_the_inputs():
    measured = measure_byte_counts(
        _ledger(b"a\nb\n"), source_localities=("source",)
    )
    assert len(measured.source_material) == 2
    assert all(
        set(item) == {"material_acquisition_occurrence_identity"}
        for item in measured.source_material
    )
    assert measured.completeness_boundary.identity


def test_count_and_recurrence_are_distinct_results():
    event = _record_byte_measurement(
        _ledger(b"ab\n"),
        source_localities=("source",),
        recording_locality_identity="measurement",
    )
    by_byte = {}
    for assertion in event.material["assertions"]:
        content = assertion["assertion_subject"].get("content")
        if content is not None:
            by_byte.setdefault(content, []).append(assertion)

    assert [item["result"] for item in by_byte[97]] == ["count"]
    assert by_byte[97][0]["dimensions"]["content"]["count"] == 1
    # The newline occurs once too. No positive singleton is called recurrence.
    assert [item["result"] for item in by_byte[10]] == ["count"]


def test_recurrence_exists_only_above_one():
    event = _record_byte_measurement(
        _ledger(b"aa\n"),
        source_localities=("source",),
        recording_locality_identity="measurement",
    )
    results = [
        item["result"]
        for item in event.material["assertions"]
        if item["assertion_subject"].get("content") == 97
    ]
    assert results == ["count", "recurrence"]


def test_the_rule_is_mechanics_not_an_unchecked_callable():
    event = _record_byte_measurement(
        _ledger(b"the cat\n"),
        source_localities=("source",),
        recording_locality_identity="measurement",
    )
    assert event.material["measurement_rule"] == BYTE_MEASUREMENT_RULE
    assert event.kind == BYTE_MEASUREMENT_RECORDED_KIND
    assert "zebra" not in str(event.material)


def test_recorded_results_replay_the_complete_bounded_source_read():
    ledger = _ledger(b"a\na\n")
    event = _record_byte_measurement(
        ledger,
        source_localities=("source",),
        recording_locality_identity="measurement",
    )
    read = assertions_of_recorded_byte_measurement(ledger, event.identity)
    assert read
    assert all(item.recorded_occurrence_identity == event.identity for item in read)
    yield_relation = ledger.get(event.material["yield_relation_identity"])
    assert yield_relation.kind == RECORDED_YIELD_RELATION_EVENT
    assert yield_relation.material["dimensions"]["act_occurrence_identity"] == event.material[
        "act_occurrence_identity"
    ]
    assert yield_relation.material["coordinates_of_carried_result"] == [
        "result_identity",
        "dimensions",
        "exact_act",
        "addressed_act_identity",
        "act_occurrence_identity",
        "subject_to_act_binding_reference",
        "measurement_rule",
        "source_localities",
        "completeness_boundary",
        "assertions",
    ]
    assert "occurrence_preservation" not in yield_relation.material["coordinates_of_carried_result"]

    count = next(
        item
        for item in read
        if item.content == 97 and item.result == "count"
    )
    assert count.material["dimensions"]["content"] == {
        "input_count": 2,
        "occurrences_carrying": 2,
        "count": 2,
    }
    assert count.material["assertion_scope"] == {
        "source_localities": ["source"],
    }
    assert count.material["dimensions"]["source_provenance"]
    assert count.material["unknown"]
    assert count.material["conflicts"] == "Unknown"
    assert count.support_assertion_references == (
        {
            "recorded_occurrence_identity": event.identity,
            "assertion_position": event.material["assertions"][0]["dimensions"]["position"],
        },
    )

    detached_material = count.material
    detached_material["dimensions"]["standing"] = "unsupported"
    assert "standing" not in count.material["dimensions"]

    detached_references = count.support_assertion_references
    detached_references[0]["assertion_position"] = None
    assert count.support_assertion_references[0]["assertion_position"] is not None

    # Read preserves exact durable JSON kinds. It does not protect the
    # result by transmuting lists to tuples or dicts to proxy objects.
    represented = Event(
        identity="re-represented",
        kind="test.content",
        material=count.material,
    )
    assert type(represented.material) is dict
    assert type(represented.material["assertion_scope"]["source_localities"]) is list


def test_a_self_consistent_truncated_source_assertion_is_refused():
    ledger = _ledger(b"a\nb\n")
    event = _record_byte_measurement(
        ledger,
        source_localities=("source",),
        recording_locality_identity="measurement",
    )
    assertions = event.material["assertions"]
    source = assertions[0]
    source["dimensions"]["content"]["source_material"] = source["dimensions"][
        "content"
    ]["source_material"][:1]
    yield_relation = ledger.get(event.material["yield_relation_identity"])
    yield_relation.material["result"] = {
        name: event.material[name]
        for name in yield_relation.material["coordinates_of_carried_result"]
    }
    with pytest.raises(ByteMeasurementError, match="complete bounded source read"):
        assertions_of_recorded_byte_measurement(ledger, event.identity)


def test_changed_plain_byte_assertion_address_is_refused():
    ledger = _ledger(b"a\n")
    event = _record_byte_measurement(
        ledger,
        source_localities=("source",),
        recording_locality_identity="measurement",
    )
    leaf_assertion = next(
        assertion
        for assertion in reversed(event.material["assertions"])
        if assertion["result"] == "count"
    )
    leaf_assertion["dimensions"]["identity"] = (
        "crossed-plain-byte-assertion-address"
    )
    yield_relation = ledger.get(event.material["yield_relation_identity"])
    yield_relation.material["result"] = {
        name: event.material[name]
        for name in yield_relation.material["coordinates_of_carried_result"]
    }

    with pytest.raises(ByteMeasurementError, match="complete bounded source read"):
        assertions_of_recorded_byte_measurement(ledger, event.identity)


def test_recording_occurrence_is_validated_exactly():
    ledger = _ledger(b"a\n")
    event = _record_byte_measurement(
        ledger,
        source_localities=("source",),
        recording_locality_identity="measurement",
    )
    event.material["occurrence_preservation"] = "something else"
    with pytest.raises(ByteMeasurementError, match="exact Measurement and Yield relation"):
        assertions_of_recorded_byte_measurement(ledger, event.identity)


def test_material_acquisition_after_the_measurement_boundary_cannot_enter_the_measurement():
    ledger = EventLedger()
    _record_operator_material_source(
        ledger,
        locality_identity="source",
        exact_bytes=b"a",
        source_boundary="first boundary",
    )
    boundary = ledger.append_boundary()
    _record_operator_material_source(
        ledger,
        locality_identity="source",
        exact_bytes=b"b",
        source_boundary="second boundary",
    )
    measured = _measure_byte_counts_through(
        ledger,
        localities=("source",),
        boundary=boundary,
    )
    assert {item.content: item.count for item in measured.counts} == {97: 1}


def test_a_missing_declared_locality_is_refused():
    with pytest.raises(ByteMeasurementError, match="absent"):
        measure_byte_counts(
            EventLedger(), source_localities=("missing",)
        )


def test_acquisition_result_must_match_its_exact_byte_coordinates():
    ledger = _ledger(b"a\n")
    acquisition_result = next(iter_exact_material_results(ledger, "source"))
    object.__setattr__(acquisition_result, "exact_material", None)
    with pytest.raises(ByteMeasurementError, match="without intact physiology"):
        measure_byte_counts(
            ledger, source_localities=("source",)
        )


def test_repeated_locality_coordinate_does_not_repeat_one_acquire():
    ledger = _ledger(b"a\n")
    once = measure_byte_counts(
        ledger, source_localities=("source",)
    )
    repeated = measure_byte_counts(
        ledger, source_localities=("source", "source")
    )
    assert repeated == once


def test_every_overlapping_byte_position_pair_is_measured():
    ledger = _ledger(b"tatatata\n")
    source = _byte_source(ledger)
    event = record_byte_position_pair_count_layer(
        ledger,
        source_measurement_event_identity=source.identity,
        recording_locality_identity="measurement",
    )
    counts = {
            tuple(item["assertion_subject"]["content"]): item["dimensions"]["content"]
        for item in event.material["assertions"]
        if item["result"] == "count"
    }

    assert counts[(116, 97)]["count"] == 4
    assert counts[(97, 116)]["count"] == 3
    assert counts[(97, 10)]["count"] == 1


def test_byte_position_pair_results_follow_first_observed_pair_positions():
    ledger = _ledger(b"tatatata\n")
    source = _byte_source(ledger)
    event = record_byte_position_pair_count_layer(
        ledger,
        source_measurement_event_identity=source.identity,
        recording_locality_identity="measurement",
    )

    assert [
        tuple(assertion["assertion_subject"]["content"])
        for assertion in event.material["assertions"]
        if assertion["result"] == "count"
    ] == [(116, 97), (97, 116), (97, 10)]


def test_position_pairs_never_cross_material_acquisition_boundaries():
    ledger = _ledger(b"a\nb\n")
    source = _byte_source(ledger)
    event = record_byte_position_pair_count_layer(
        ledger,
        source_measurement_event_identity=source.identity,
        recording_locality_identity="measurement",
    )
    counts = {
        tuple(item["assertion_subject"]["content"]): item["dimensions"]["content"][
            "count"
        ]
        for item in event.material["assertions"]
        if item["result"] == "count"
    }

    assert counts == {(97, 10): 1, (98, 10): 1}
    assert (10, 98) not in counts


def test_position_pair_measurement_uses_exact_opaque_bytes():
    ledger = EventLedger()
    _record_operator_material_source(
        ledger,
        locality_identity="source",
        exact_bytes=b"\xe7\x8c\xab\n",
        source_boundary="opaque pair fixture",
    )
    source = _byte_source(ledger)
    event = record_byte_position_pair_count_layer(
        ledger,
        source_measurement_event_identity=source.identity,
        recording_locality_identity="measurement",
    )
    counts = {
        tuple(item["assertion_subject"]["content"])
        for item in event.material["assertions"]
        if item["result"] == "count"
    }

    # The recorded material supplies ordered byte pairs and no character claim.
    assert counts == {(231, 140), (140, 171), (171, 10)}


def test_pair_count_and_recurrence_are_separate_results():
    ledger = _ledger(b"tatatata\n")
    source = _byte_source(ledger)
    event = record_byte_position_pair_count_layer(
        ledger,
        source_measurement_event_identity=source.identity,
        recording_locality_identity="measurement",
    )
    assert event.kind == BYTE_PAIR_MEASUREMENT_RECORDED_KIND
    by_pair = {}
    for assertion in event.material["assertions"]:
        content = assertion["assertion_subject"].get("content")
        if content is not None:
            by_pair.setdefault(tuple(content), []).append(assertion)

    assert [item["result"] for item in by_pair[(116, 97)]] == ["count", "recurrence"]
    assert [item["result"] for item in by_pair[(97, 10)]] == ["count"]
    assert by_pair[(116, 97)][1]["input_support"]["local_assertion_references"] == [
        by_pair[(116, 97)][0]["dimensions"]["position"]
    ]
    moved_reference = by_pair[(116, 97)][0]["input_support"]["assertion_references"][0]
    original = next(
        item
        for item in assertions_of_recorded_byte_measurement(ledger, source.identity)
        if item.result == "exact_source_material_set"
    )
    assert moved_reference["assertion_position"] == original.assertion_position
    assert moved_reference["recorded_occurrence_identity"] == original.recorded_occurrence_identity
    assert event.material["source_movement_event_identity"] != original.recorded_occurrence_identity
    applicability = input_applicability_of_recorded_byte_position_pair_measurement(
        ledger, event.identity
    )
    assert applicability["dimensions"]["applicability"] == "applicable"
    assert applicability["input_assertion_reference"] == event.material["source_assertion_reference"]
    assert applicability["result_boundary"]
    assert applicability["addressed_act"] == "declared byte-position-pair Measurement"
    assert applicability["measurement_locality"] == "measurement"
    assert applicability["input_unknown"] == []
    assert applicability["input_coordinates"] == {
        "recorded_measurement_result_occurrence_identity": source.identity,
        "assertion_position": original.assertion_position,
        "locality_movement_result_occurrence_identity": event.material[
            "source_movement_event_identity"
        ],
    }


def test_recorded_pair_results_replay_the_complete_bounded_source_read():
    ledger = _ledger(b"tatatata\n")
    source = _byte_source(ledger)
    event = record_byte_position_pair_count_layer(
        ledger,
        source_measurement_event_identity=source.identity,
        recording_locality_identity="measurement",
    )

    read = assertions_of_recorded_byte_position_pair_measurement(
        ledger, event.identity
    )
    assert read
    assert all(item.recorded_occurrence_identity == event.identity for item in read)
    assert {item.content for item in read if item.content} == {
        (116, 97),
        (97, 116),
        (97, 10),
    }
    count = next(
        item
        for item in read
        if item.content == (116, 97) and item.result == "count"
    )
    detached = count.material
    detached["dimensions"]["standing"] = "unsupported"
    assert "standing" not in count.material["dimensions"]
    assert count.support_assertion_references[0]["recorded_occurrence_identity"] == source.identity
    movement = ledger.get(event.material["source_movement_event_identity"])
    assert movement.material["source_assertion_reference"]["recorded_occurrence_identity"] == source.identity
    assert movement.material["source_assertion_reference"] == (
        count.support_assertion_references[0]
    )
    assert movement.material["source_locality"] == "byte-measurement"
    assert movement.material["destination_locality"] == "measurement"
    assert movement.material["movement_act_identity"] != movement.material[
        "movement_act_occurrence_identity"
    ]
    act_occurrence = ledger.get(movement.material["act_occurrence_event_identity"])
    assert act_occurrence.material["movement_act_identity"] == movement.material[
        "movement_act_identity"
    ]
    assert act_occurrence.material["movement_act_occurrence_identity"] == movement.material[
        "movement_act_occurrence_identity"
    ]
    assert "dimensions" not in movement.material


def test_same_locality_pair_result_replays_without_recording_more_work():
    ledger = EventLedger()
    _record_operator_material_source(
        ledger,
        locality_identity="source",
        exact_bytes=b"tatatata\n",
        source_boundary="exact same-locality source",
    )
    source = _record_byte_measurement(
        ledger,
        source_localities=("source",),
        recording_locality_identity="source",
    )
    pair = record_byte_position_pair_count_layer(
        ledger,
        source_measurement_event_identity=source.identity,
        recording_locality_identity="source",
    )
    recorded_count = len(ledger.list())
    assert assertions_of_recorded_byte_position_pair_measurement(
        ledger, pair.identity
    )
    assert len(ledger.list()) == recorded_count


def test_pair_validation_refuses_a_self_consistent_truncated_result_inputs():
    ledger = _ledger(b"tatatata\n")
    source = _byte_source(ledger)
    event = record_byte_position_pair_count_layer(
        ledger,
        source_measurement_event_identity=source.identity,
        recording_locality_identity="measurement",
    )
    recurrence = next(
        assertion
        for assertion in event.material["assertions"]
        if assertion["result"] == "recurrence"
    )
    event.material["assertions"] = [
        assertion
        for assertion in event.material["assertions"]
        if assertion["dimensions"]["position"]
        != recurrence["dimensions"]["position"]
    ]
    yield_relation = ledger.get(event.material["yield_relation_identity"])
    yield_relation.material["result"] = {
        name: value
        for name, value in event.material.items()
        if name in BYTE_PAIR_RESULT_COORDINATES
    }

    with pytest.raises(ByteMeasurementError, match="unlawful pair Assertion"):
        assertions_of_recorded_byte_position_pair_measurement(ledger, event.identity)


def test_changed_pair_assertion_address_is_refused():
    ledger = _ledger(b"ta\n")
    source = _byte_source(ledger)
    event = record_byte_position_pair_count_layer(
        ledger,
        source_measurement_event_identity=source.identity,
        recording_locality_identity="measurement",
    )
    event.material["assertions"][0]["dimensions"]["identity"] = (
        "crossed-byte-pair-assertion-address"
    )
    yield_relation = ledger.get(event.material["yield_relation_identity"])
    yield_relation.material["result"] = {
        name: event.material[name]
        for name in yield_relation.material["coordinates_of_carried_result"]
    }

    with pytest.raises(ByteMeasurementError, match="unlawful pair Assertion"):
        assertions_of_recorded_byte_position_pair_measurement(ledger, event.identity)


@pytest.mark.parametrize(
    "content",
    (
        [116],
        [116, 256],
        [116, "97"],
        "7461",
        (116, 97),
        [116, 97, 10],
        [True, 97],
    ),
)
def test_pair_validation_requires_one_exact_ordered_content(content):
    ledger = _ledger(b"ta\n")
    source = _byte_source(ledger)
    event = record_byte_position_pair_count_layer(
        ledger,
        source_measurement_event_identity=source.identity,
        recording_locality_identity="measurement",
    )
    assertion = event.material["assertions"][0]
    assertion["assertion_subject"]["content"] = content
    yield_relation = ledger.get(event.material["yield_relation_identity"])
    yield_relation.material["result"] = {
        name: event.material[name]
        for name in yield_relation.material["coordinates_of_carried_result"]
    }

    with pytest.raises(ByteMeasurementError, match="unlawful pair Assertion"):
        assertions_of_recorded_byte_position_pair_measurement(ledger, event.identity)


def test_pair_validation_does_not_perform_the_pair_measurement_again(monkeypatch):
    ledger = _ledger(b"tatatata\n")
    source = _byte_source(ledger)
    event = record_byte_position_pair_count_layer(
        ledger,
        source_measurement_event_identity=source.identity,
        recording_locality_identity="measurement",
    )

    def forbidden(*args, **kwargs):
        raise AssertionError("the pair Measurement occurred again")

    monkeypatch.setattr(
        "seed_runtime.byte_measurement._measure_byte_position_pair_counts_through",
        forbidden,
    )
    monkeypatch.setattr(
        "seed_runtime.byte_measurement._pair_input_applicability", forbidden
    )
    assert assertions_of_recorded_byte_position_pair_measurement(ledger, event.identity)


def test_pair_validation_refuses_unsupported_input_applicability():
    ledger = _ledger(b"tatatata\n")
    source = _byte_source(ledger)
    event = record_byte_position_pair_count_layer(
        ledger,
        source_measurement_event_identity=source.identity,
        recording_locality_identity="measurement",
    )
    event.material["input_applicability"]["result_boundary"] = "some other use"
    yield_relation = ledger.get(event.material["yield_relation_identity"])
    yield_relation.material["result"] = {
        name: event.material[name]
        for name in yield_relation.material["coordinates_of_carried_result"]
    }

    with pytest.raises(ByteMeasurementError, match="Applicability result is not exact"):
        assertions_of_recorded_byte_position_pair_measurement(ledger, event.identity)


def test_zero_measured_pairs_is_a_lawful_exact_result():
    ledger = _ledger(b"\n")
    source = _byte_source(ledger)
    event = record_byte_position_pair_count_layer(
        ledger,
        source_measurement_event_identity=source.identity,
        recording_locality_identity="measurement",
    )

    assert event.material["assertions"] == []
    assert assertions_of_recorded_byte_position_pair_measurement(ledger, event.identity) == ()


def test_applicability_identity_is_bound_to_one_exact_addressed_act():
    ledger = _ledger(b"ta\n")
    source_event = _byte_source(ledger)
    first_result = record_byte_position_pair_count_layer(
        ledger,
        source_measurement_event_identity=source_event.identity,
        recording_locality_identity="byte-measurement",
    )
    second_result = record_byte_position_pair_count_layer(
        ledger,
        source_measurement_event_identity=source_event.identity,
        recording_locality_identity="byte-measurement",
    )
    first = input_applicability_of_recorded_byte_position_pair_measurement(
        ledger, first_result.identity
    )
    second = input_applicability_of_recorded_byte_position_pair_measurement(
        ledger, second_result.identity
    )
    first_assignment = ledger.get(
        first["subject_to_act_binding_reference"][
            "recorded_occurrence_identity"
        ],
    )

    assert first["dimensions"]["identity"] != second["dimensions"]["identity"]
    assert first["dimensions"]["identity"] == first_assignment.material[
        "applicability_result_identity"
    ]
    assert first_assignment.kind == (
        BYTE_PAIR_APPLICABILITY_SUBJECT_TO_ACT_BINDING_RECORDED_KIND
    )
    assert "assignment_identity" not in first["subject_to_act_binding_reference"]
    assert "assignment_subject_identity" not in first["subject_to_act_binding_reference"]
    assert first["addressed_act_identity"] == first_assignment.material[
        "addressed_act_identity"
    ]
    assert first["addressed_act_occurrence_identity"] is None


def test_pair_subject_to_act_bindings_are_distinct_and_share_the_addressed_act():
    ledger = _ledger(b"tata\n")
    source = _byte_source(ledger)
    result = record_byte_position_pair_count_layer(
        ledger,
        source_measurement_event_identity=source.identity,
        recording_locality_identity="measurement",
    )
    assignment = get_byte_position_pair_measurement_subject_to_act_binding(
        ledger,
        result.material["subject_to_act_binding_reference"][
            "recorded_occurrence_identity"
        ],
    )
    applicability = ledger.get(result.material["input_applicability_event_identity"])
    applicability_act = ledger.get(
        applicability.material["act_occurrence_event_identity"]
    )
    measurement_act = ledger.get(result.material["act_occurrence_event_identity"])
    standing = read_operator_locality_standing_through(
        ledger,
        locality_identity="measurement",
        through_event_occurrence_identity=assignment.identity,
    )

    assert standing["subject_to_act_binding_occurrences"].get(
        assignment.identity, object()
    ) is None
    applicability_binding = ledger.get(
        applicability_act.material["subject_to_act_binding_reference"][
            "recorded_occurrence_identity"
        ]
    )
    assert applicability_binding.kind == (
        BYTE_PAIR_APPLICABILITY_SUBJECT_TO_ACT_BINDING_RECORDED_KIND
    )
    assert assignment.kind == BYTE_PAIR_MEASUREMENT_SUBJECT_TO_ACT_BINDING_RECORDED_KIND
    assert applicability_binding.identity != assignment.identity
    assert assignment.material["subject_reference"] == applicability_binding.material[
        "source_assertion_reference"
    ]
    assert assignment.material["through_event_occurrence_identity"] == (
        applicability_binding.identity
    )
    assert applicability_binding.material["addressed_act_identity"] == (
        assignment.material["exact_act_identity"]
    )
    assert applicability_act.material["subject_to_act_binding_reference"] != (
        result.material["subject_to_act_binding_reference"]
    )
    assert measurement_act.material["subject_to_act_binding_reference"] == (
        result.material["subject_to_act_binding_reference"]
    )


@pytest.mark.parametrize(
    ("boundary", "message"),
    (
        ("byte_pair_applicability", "Applicability result requires its exact Yield"),
        ("byte_pair_measurement", "Measurement result requires its exact Yield"),
    ),
)
def test_pair_result_refuses_an_append_between_yield_and_result(boundary, message):
    ledger = YieldCallbackLedger()
    run_persistent_operator_console(
        ledger=ledger,
        locality_identity="source",
        input_stream=binary_input("tata\n"),
    )
    source = _byte_source(ledger)
    recorded_before = sum(
        event.kind == BYTE_PAIR_MEASUREMENT_RECORDED_KIND
        for event in ledger.list()
    )
    ledger.callback_boundary = boundary

    with pytest.raises(ByteMeasurementError, match=message):
        record_byte_position_pair_count_layer(
            ledger,
            source_measurement_event_identity=source.identity,
            recording_locality_identity="measurement",
        )

    assert ledger.callback_recorded is True
    assert sum(
        event.kind == BYTE_PAIR_MEASUREMENT_RECORDED_KIND
        for event in ledger.list()
    ) == recorded_before


def test_pair_call_local_lifecycle_refuses_forged_assignment_and_repeated_acts():
    from seed_runtime import byte_measurement
    from seed_runtime.operator_locality_standing import (
        _carry_pair_applicability_act_into_standing,
        _carry_pair_applicability_binding_into_standing,
        _carry_pair_applicability_result_into_standing,
        _carry_pair_measurement_act_into_standing,
        _carry_pair_measurement_binding_into_standing,
    )

    ledger = _ledger(b"tata\n")
    source_event = _byte_source(ledger)
    source, scope, content = byte_measurement._prepare_pair_source(
        ledger,
        source_measurement_event_identity=source_event.identity,
        measurement_locality_identity="byte-measurement",
    )
    standing = read_operator_locality_standing(
        ledger, locality_identity="byte-measurement"
    )
    boundary = byte_measurement._require_carried_pair_measurement_standing_at_tip(
        ledger,
        source=source,
        recording_locality_identity="byte-measurement",
        locality_standing=standing,
    )
    identities = byte_measurement._new_pair_lifecycle_identities(ledger)
    applicability_binding = byte_measurement._append_pair_applicability_binding(
        ledger,
        source=source,
        scope=scope,
        content=content,
        recording_locality_identity="byte-measurement",
        through_event_occurrence_identity=boundary,
        identities=identities,
    )
    standing = _carry_pair_applicability_binding_into_standing(
        ledger,
        standing,
        applicability_binding,
        source,
        prior_through_event_occurrence_identity=boundary,
    )
    measurement_binding = byte_measurement._append_pair_measurement_binding(
        ledger,
        source=source,
        scope=scope,
        content=content,
        recording_locality_identity="byte-measurement",
        through_event_occurrence_identity=applicability_binding.identity,
        identities=identities,
    )
    standing = _carry_pair_measurement_binding_into_standing(
        ledger,
        standing,
        measurement_binding,
        source,
        prior_through_event_occurrence_identity=applicability_binding.identity,
    )
    forged = deepcopy(applicability_binding)
    forged.material["addressed_act_identity"] = "forged-measurement-act"
    event_count = len(ledger.list())
    with pytest.raises(ByteMeasurementError, match="binding is not exact"):
        byte_measurement._record_pair_input_applicability_act_from_carried_assignment(
            ledger,
            assignment=forged,
            source=source,
            responsibility_assignment_standing=standing,
        )
    assert len(ledger.list()) == event_count

    applicability = byte_measurement._pair_input_applicability(
        ledger,
        source,
        assignment=applicability_binding,
        measurement_locality_identity="byte-measurement",
    )
    applicability_act = (
        byte_measurement._record_pair_input_applicability_act_from_carried_assignment(
            ledger,
            assignment=applicability_binding,
            source=source,
            responsibility_assignment_standing=standing,
        )
    )
    standing = _carry_pair_applicability_act_into_standing(
        ledger,
        standing,
        applicability_act,
        assignment=applicability_binding,
        source=source,
        prior_through_event_occurrence_identity=measurement_binding.identity,
    )
    unchanged = deepcopy(standing)
    with pytest.raises(ValueError, match="order is not exact"):
        _carry_pair_applicability_act_into_standing(
            ledger,
            standing,
            applicability_act,
            assignment=applicability_binding,
            source=source,
            prior_through_event_occurrence_identity=applicability_act.identity,
        )
    assert standing == unchanged

    applicability_event = (
        byte_measurement._record_pair_input_applicability_result_from_carried_act(
            ledger,
            assignment=applicability_binding,
            source=source,
            applicability_act_occurrence=applicability_act,
            applicability_assertion=applicability,
        )
    )
    standing = _carry_pair_applicability_result_into_standing(
        ledger,
        standing,
        applicability_event,
        assignment=applicability_binding,
        source=source,
        applicability_act_occurrence=applicability_act,
        prior_through_event_occurrence_identity=applicability_act.identity,
    )
    measurement_act = byte_measurement._record_pair_measurement_act_from_carried_applicability(
        ledger,
        assignment=measurement_binding,
        source=source,
        applicability_event=applicability_event,
        locality_standing=standing,
    )
    standing = _carry_pair_measurement_act_into_standing(
        ledger,
        standing,
        measurement_act,
        assignment=measurement_binding,
        source=source,
        applicability_event=applicability_event,
        applicability_act_occurrence=applicability_act,
        prior_through_event_occurrence_identity=applicability_event.identity,
    )
    unchanged = deepcopy(standing)
    with pytest.raises(ValueError, match="order is not exact"):
        _carry_pair_measurement_act_into_standing(
            ledger,
            standing,
            measurement_act,
            assignment=measurement_binding,
            source=source,
            applicability_event=applicability_event,
            applicability_act_occurrence=applicability_act,
            prior_through_event_occurrence_identity=measurement_act.identity,
        )
    assert standing == unchanged


def test_pair_result_is_derived_from_source_without_a_measured_carrier_argument():
    import inspect
    from seed_runtime import byte_measurement

    assert "measured" not in inspect.signature(
        byte_measurement._record_pair_measurement_result_from_carried_act
    ).parameters
    ledger = _ledger(b"abab\n")
    source = _byte_source(ledger)
    result = record_byte_position_pair_count_layer(
        ledger,
        source_measurement_event_identity=source.identity,
        recording_locality_identity="measurement",
    )
    counts = {
        tuple(assertion["assertion_subject"]["content"]): assertion[
            "dimensions"
        ]["content"]["count"]
        for assertion in result.material["assertions"]
        if assertion["result"] == "count"
    }
    assert counts[(97, 98)] == 2


def test_pair_result_rechecks_measurement_act_tip_after_source_callback(monkeypatch):
    from seed_runtime import byte_measurement

    ledger = _ledger(b"abab\n")
    source = _byte_source(ledger)
    recorded_before = sum(
        event.kind == BYTE_PAIR_MEASUREMENT_RECORDED_KIND
        for event in ledger.list()
    )
    original = byte_measurement._material_result_bytes
    callback_recorded = False

    def append_during_pair_measurement(ledger, acquisition_result):
        nonlocal callback_recorded
        events = ledger.list()
        tip = events[-1] if events else None
        if (
            not callback_recorded
            and tip is not None
            and tip.kind
            == "operator.measurement.byte_position_pair_act_occurrenced"
        ):
            callback_recorded = True
            ledger.append(
                "test.unrelated_pair_measurement_callback",
                {"unknown": ["unrelated append during pair Measurement"]},
                locality_identity="unrelated",
            )
        return original(ledger, acquisition_result)

    monkeypatch.setattr(
        byte_measurement, "_material_result_bytes", append_during_pair_measurement
    )
    with pytest.raises((ByteMeasurementError, ValueError)):
        record_byte_position_pair_count_layer(
            ledger,
            source_measurement_event_identity=source.identity,
            recording_locality_identity="measurement",
        )

    assert callback_recorded is True
    assert sum(
        event.kind == BYTE_PAIR_MEASUREMENT_RECORDED_KIND
        for event in ledger.list()
    ) == recorded_before


def test_pair_applicability_reads_exact_input_coordinates():
    ledger = _ledger(b"ta\n")
    source_event = _byte_source(ledger)
    source = next(
        item
        for item in assertions_of_recorded_byte_measurement(ledger, source_event.identity)
        if item.result == "exact_source_material_set"
    )
    result = record_byte_position_pair_count_layer(
        ledger,
        source_measurement_event_identity=source_event.identity,
        recording_locality_identity="byte-measurement",
    )
    applicable = input_applicability_of_recorded_byte_position_pair_measurement(
        ledger, result.identity
    )

    assert applicable["dimensions"]["applicability"] == "applicable"
    assert applicable["input_coordinates"] == {
        "recorded_measurement_result_occurrence_identity": source.recorded_occurrence_identity,
            "assertion_position": source.assertion_position,
        "locality_movement_result_occurrence_identity": None,
    }
    assert applicable["input_assertion_reference"] == source.reference
    assert applicable["addressed_act_occurrence_identity"] is None


def test_byte_measurement_binding_carries_its_exact_source_occurrences():
    ledger = _ledger(b"ta\n")
    source = _byte_source(ledger)
    assignment = get_byte_measurement_subject_to_act_binding(
        ledger,
        source.material["subject_to_act_binding_reference"][
            "recorded_occurrence_identity"
        ],
    ).material
    source_set = next(
        assertion
        for assertion in source.material["assertions"]
        if assertion["result"] == "exact_source_material_set"
    )

    assert assignment["source_occurrence_references"] == source_set["dimensions"][
        "content"
    ]["source_material"]
    assert assignment["completeness_boundary_identity"] == source.material[
        "completeness_boundary"
    ]["identity"]
def test_locality_movement_assignment_is_earned_from_the_exact_source():
    ledger = _ledger(b"ta\n")
    source = _byte_source(ledger)
    pair = record_byte_position_pair_count_layer(
        ledger,
        source_measurement_event_identity=source.identity,
        recording_locality_identity="measurement",
    )
    movement = ledger.get(pair.material["source_movement_event_identity"])
    reference = movement.material["subject_to_act_binding_reference"]
    assignment = get_assertion_locality_movement_subject_to_act_binding(
        ledger, reference["recorded_occurrence_identity"]
    )
    standing = read_operator_locality_standing(
        ledger, locality_identity="measurement"
    )

    assert assignment.kind == (
        ASSERTION_LOCALITY_MOVEMENT_SUBJECT_TO_ACT_BINDING_KIND
    )
    assert reference == {
        "recorded_occurrence_identity": assignment.identity,
        "book_clause_identity": assignment.material["book_clause_identity"],
        "result_boundary_identity": assignment.material[
            "result_boundary_identity"
        ],
    }
    assert assignment.material["source_assertion_reference"] == (
        movement.material["source_assertion_reference"]
    )
    assert assignment.material["source_locality"] == "byte-measurement"
    assert assignment.material["destination_locality"] == "measurement"
    assert standing["subject_to_act_binding_occurrences"][assignment.identity] is None
    assert "standing" not in assignment.material
    assert "responsibility_assignment" not in movement.material


def test_movement_assignment_owns_distinct_lifecycle_identities_and_enters_destination_standing():
    ledger = _ledger(b"ta\n")
    source_result, source = _movement_source(ledger)
    assignment = record_assertion_locality_movement_subject_to_act_binding(
        ledger,
        source=source,
        destination_locality="movement",
        source_current_coordinates=read_operator_locality_standing(
            ledger, locality_identity=source_result.locality_identity
        ),
        destination_current_coordinates=read_operator_locality_standing(
            ledger, locality_identity="movement"
        ),
    )
    identities = {
        assignment.identity,
        *(
            assignment.material[coordinate]
            for coordinate in (
                "movement_act_identity",
                "movement_act_occurrence_identity",
                "movement_result_identity",
            )
        ),
    }
    standing = read_operator_locality_standing(
        ledger, locality_identity="movement"
    )

    assert len(identities) == 4
    assert standing["subject_to_act_binding_occurrences"] == {
        assignment.identity: None
    }
    assert assignment.material["source_through_event_occurrence_identity"] == (
        source_result.identity
    )


def test_movement_assignment_refuses_stale_or_shaped_source_standing():
    ledger = _ledger(b"ta\n")
    source_result, source = _movement_source(ledger)
    stale = read_operator_locality_standing(
        ledger, locality_identity=source_result.locality_identity
    )
    shaped = deepcopy(stale)
    shaped["measurement_occurrences"] = {
        source_result.identity: {"recorded_occurrence_identity": source_result.identity}
    }
    _record_operator_material_source(
        ledger,
        locality_identity=source_result.locality_identity,
        exact_bytes=b"later",
        source_boundary="after source Standing",
    )
    destination = read_operator_locality_standing(
        ledger, locality_identity="movement"
    )

    for standing in (stale, shaped):
        with pytest.raises(ByteMeasurementError, match="current source coordinates"):
            record_assertion_locality_movement_subject_to_act_binding(
                ledger,
                source=source,
                destination_locality="movement",
                source_current_coordinates=standing,
                destination_current_coordinates=destination,
            )


def test_movement_act_requires_current_destination_standing_carrying_assignment():
    ledger = _ledger(b"ta\n")
    source_result, source = _movement_source(ledger)
    stale_destination = read_operator_locality_standing(
        ledger, locality_identity="movement"
    )
    assignment = record_assertion_locality_movement_subject_to_act_binding(
        ledger,
        source=source,
        destination_locality="movement",
        source_current_coordinates=read_operator_locality_standing(
            ledger, locality_identity=source_result.locality_identity
        ),
        destination_current_coordinates=stale_destination,
    )
    shaped = deepcopy(
        read_operator_locality_standing(ledger, locality_identity="movement")
    )
    shaped["subject_to_act_binding_occurrences"] = {
        "same-shaped-assignment": None
    }

    for standing in (stale_destination, shaped):
        with pytest.raises(
            ByteMeasurementError, match="current destination coordinates"
        ):
            record_assertion_locality_movement_act_occurrence(
                ledger,
                subject_to_act_binding_event_identity=assignment.identity,
                current_coordinates=standing,
            )


def test_movement_lifecycle_refuses_duplicate_act_and_result():
    ledger = _ledger(b"ta\n")
    source_result, source = _movement_source(ledger)
    assignment = record_assertion_locality_movement_subject_to_act_binding(
        ledger,
        source=source,
        destination_locality="movement",
        source_current_coordinates=read_operator_locality_standing(
            ledger, locality_identity=source_result.locality_identity
        ),
        destination_current_coordinates=read_operator_locality_standing(
            ledger, locality_identity="movement"
        ),
    )
    standing = read_operator_locality_standing(
        ledger, locality_identity="movement"
    )
    act = record_assertion_locality_movement_act_occurrence(
        ledger,
        subject_to_act_binding_event_identity=assignment.identity,
        current_coordinates=standing,
    )
    with pytest.raises(ByteMeasurementError, match="already carries an Act"):
        record_assertion_locality_movement_act_occurrence(
            ledger,
            subject_to_act_binding_event_identity=assignment.identity,
            current_coordinates=read_operator_locality_standing(
                ledger, locality_identity="movement"
            ),
        )
    movement = record_assertion_locality_movement_result(
        ledger, act_occurrence_event_identity=act.identity
    )
    assert _validate_moved_byte_assertion(ledger, movement.identity)
    with pytest.raises(ByteMeasurementError, match="already carries a Yield or result"):
        record_assertion_locality_movement_result(
            ledger, act_occurrence_event_identity=act.identity
        )


def test_movement_act_refuses_standing_before_a_later_destination_tip():
    ledger = _ledger(b"ta\n")
    source_result, source = _movement_source(ledger)
    assignment = record_assertion_locality_movement_subject_to_act_binding(
        ledger,
        source=source,
        destination_locality="movement",
        source_current_coordinates=read_operator_locality_standing(
            ledger, locality_identity=source_result.locality_identity
        ),
        destination_current_coordinates=read_operator_locality_standing(
            ledger, locality_identity="movement"
        ),
    )
    stale = read_operator_locality_standing(
        ledger, locality_identity="movement"
    )
    _record_operator_material_source(
        ledger,
        locality_identity="movement",
        exact_bytes=b"later",
        source_boundary="after assignment",
    )
    with pytest.raises(ByteMeasurementError, match="current destination coordinates"):
        record_assertion_locality_movement_act_occurrence(
            ledger,
            subject_to_act_binding_event_identity=assignment.identity,
            current_coordinates=stale,
        )


def test_movement_assignment_and_lifecycle_survive_sqlite_restarts(tmp_path):
    path = tmp_path / "movement-assignment.sqlite"
    ledger = SQLiteEventLedger(path)
    _record_operator_material_source(
        ledger,
        locality_identity="source",
        exact_bytes=b"ta",
        source_boundary="durable source",
    )
    source_result = _record_byte_measurement(
        ledger,
        source_localities=("source",),
        recording_locality_identity="source-measurement",
    )
    source = next(
        assertion
        for assertion in assertions_of_recorded_byte_measurement(
            ledger, source_result.identity
        )
        if assertion.result == "exact_source_material_set"
    )
    assignment = record_assertion_locality_movement_subject_to_act_binding(
        ledger,
        source=source,
        destination_locality="movement",
        source_current_coordinates=read_operator_locality_standing(
            ledger, locality_identity="source-measurement"
        ),
        destination_current_coordinates=read_operator_locality_standing(
            ledger, locality_identity="movement"
        ),
    )
    ledger.close()

    ledger = SQLiteEventLedger(path)
    assert get_assertion_locality_movement_subject_to_act_binding(
        ledger, assignment.identity
    ) == assignment
    act = record_assertion_locality_movement_act_occurrence(
        ledger,
        subject_to_act_binding_event_identity=assignment.identity,
        current_coordinates=read_operator_locality_standing(
            ledger, locality_identity="movement"
        ),
    )
    ledger.close()

    ledger = SQLiteEventLedger(path)
    movement = record_assertion_locality_movement_result(
        ledger, act_occurrence_event_identity=act.identity
    )
    ledger.close()

    ledger = SQLiteEventLedger(path)
    assert _validate_moved_byte_assertion(ledger, movement.identity)
    ledger.close()


def test_movement_assignment_reader_refuses_corrupted_source_carrier():
    ledger = IntegrityCountingLedger()
    _record_operator_material_source(
        ledger,
        locality_identity="source",
        exact_bytes=b"ta",
        source_boundary="source",
    )
    source_result = _record_byte_measurement(
        ledger,
        source_localities=("source",),
        recording_locality_identity="source-measurement",
    )
    source = next(
        assertion
        for assertion in assertions_of_recorded_byte_measurement(
            ledger, source_result.identity
        )
        if assertion.result == "exact_source_material_set"
    )
    assignment = record_assertion_locality_movement_subject_to_act_binding(
        ledger,
        source=source,
        destination_locality="movement",
        source_current_coordinates=read_operator_locality_standing(
            ledger, locality_identity="source-measurement"
        ),
        destination_current_coordinates=read_operator_locality_standing(
            ledger, locality_identity="movement"
        ),
    )
    ledger.corrupted.add(source_result.identity)

    with pytest.raises(ByteMeasurementError):
        get_assertion_locality_movement_subject_to_act_binding(
            ledger, assignment.identity
        )


@pytest.mark.parametrize(
    ("coordinate", "changed"),
    (
        ("result_kind", "another result kind"),
        ("occurrence_boundary", "another occurrence boundary"),
    ),
)
def test_movement_reader_refuses_crossed_yield_boundary_or_result_kind(
    coordinate, changed
):
    ledger = _ledger(b"ta\n")
    _source_result, source = _movement_source(ledger)
    moved = move_recorded_byte_assertion_to_locality(
        ledger, source=source, destination_locality="movement"
    )
    movement = ledger.get(moved.locality_movement_event_identity)
    yield_relation = ledger.get(
        movement.material["yield_relation_identity"]
    )
    yield_relation.material[coordinate] = changed

    with pytest.raises(ByteMeasurementError, match="Yield relation is not exact"):
        _validate_moved_byte_assertion(ledger, movement.identity)


def test_movement_carried_standing_equals_replay_and_same_locality_is_noop():
    ledger = _ledger(b"ta\n")
    source_result, source = _movement_source(ledger)
    prior = read_operator_locality_standing(
        ledger, locality_identity="movement"
    )
    assignment = record_assertion_locality_movement_subject_to_act_binding(
        ledger,
        source=source,
        destination_locality="movement",
        source_current_coordinates=read_operator_locality_standing(
            ledger, locality_identity=source_result.locality_identity
        ),
        destination_current_coordinates=deepcopy(prior),
    )
    carried = advance_operator_locality_standing(
        ledger,
        (assignment.identity,),
        locality_identity="movement",
        prior=prior,
    )
    assert carried == read_operator_locality_standing(
        ledger, locality_identity="movement"
    )
    act = record_assertion_locality_movement_act_occurrence(
        ledger,
        subject_to_act_binding_event_identity=assignment.identity,
        current_coordinates=carried,
    )
    movement = record_assertion_locality_movement_result(
        ledger, act_occurrence_event_identity=act.identity
    )
    carried = advance_operator_locality_standing(
        ledger,
        (
            act.identity,
            movement.material["yield_relation_identity"],
            movement.identity,
        ),
        locality_identity="movement",
        prior=carried,
    )
    assert carried == read_operator_locality_standing(
        ledger, locality_identity="movement"
    )

    event_count = len(ledger.list())
    same = move_recorded_byte_assertion_to_locality(
        ledger,
        source=source,
        destination_locality=source_result.locality_identity,
    )
    assert same == source
    assert len(ledger.list()) == event_count


def test_bounded_movement_batch_carries_each_assignment_before_its_act():
    ledger = _ledger(b"ta\n")
    source_result = _byte_source(ledger)
    sources = tuple(
        assertion
        for assertion in assertions_of_recorded_byte_measurement(
            ledger, source_result.identity
        )
        if assertion.result == "count"
    )

    moved = move_recorded_byte_assertions_to_locality(
        ledger,
        sources=sources,
        destination_locality="movement-batch",
    )
    standing = read_operator_locality_standing(
        ledger, locality_identity="movement-batch"
    )
    movements = tuple(
        ledger.get(assertion.locality_movement_event_identity)
        for assertion in moved
    )
    assignments = tuple(
        ledger.get(
            movement.material["subject_to_act_binding_reference"][
                "recorded_occurrence_identity"
            ]
        )
        for movement in movements
    )

    assert tuple(assertion.assertion_position for assertion in moved) == tuple(
        assertion.assertion_position for assertion in sources
    )
    assert all(
        standing["subject_to_act_binding_occurrences"].get(
            assignment.identity, object()
        )
        is None
        for assignment in assignments
    )
    assert standing["through_event_occurrence_identity"] == movements[-1].identity
    assert all(
        _validate_moved_byte_assertion(ledger, movement.identity) == assertion
        for movement, assertion in zip(movements, moved, strict=True)
    )


@pytest.mark.parametrize("phase", ("assignment", "act", "result"))
def test_movement_batch_carry_phases_refuse_a_later_append_tip_without_mutation(
    phase,
):
    ledger = _ledger(b"ta\n")
    state = _movement_carry_phase(ledger, phase)
    before = deepcopy(state["destination_standing"])
    _record_operator_material_source(
        ledger,
        locality_identity="movement-carry",
        exact_bytes=b"later",
        source_boundary="after carried movement phase",
    )

    with pytest.raises(ValueError, match="Standing is not exact"):
        _carry_movement_phase(ledger, state)

    assert state["destination_standing"] == before


@pytest.mark.parametrize("phase", ("assignment", "act", "result"))
def test_movement_batch_carry_phases_refuse_corruption_without_partial_standing(
    phase,
):
    ledger = _ledger(b"ta\n")
    state = _movement_carry_phase(ledger, phase)
    before = deepcopy(state["destination_standing"])
    state["event"].material["unknown"] = ["changed after append"]

    with pytest.raises(ValueError, match="Standing is not exact"):
        _carry_movement_phase(ledger, state)

    assert state["destination_standing"] == before


@pytest.mark.parametrize("phase", ("assignment", "act", "result"))
def test_movement_batch_carry_phases_refuse_substituted_lifecycle_inputs(phase):
    ledger = _ledger(b"ta\n")
    state = _movement_carry_phase(ledger, phase)
    before = deepcopy(state["destination_standing"])
    if phase in ("assignment", "result"):
        substitute_source = next(
            assertion
            for assertion in assertions_of_recorded_byte_measurement(
                ledger, state["source_result"].identity
            )
            if assertion.assertion_position != state["source"].assertion_position
        )
        call = lambda: _carry_movement_phase(
            ledger, state, source=substitute_source
        )
    else:
        substitute_assignment = deepcopy(state["assignment"])
        substitute_assignment.material["movement_act_identity"] = (
            "substituted-movement-Act"
        )
        call = lambda: _carry_movement_phase(
            ledger,
            state,
            responsibility_assignment=substitute_assignment,
        )

    with pytest.raises(ValueError, match="Standing is not exact"):
        call()

    assert state["destination_standing"] == before


def test_movement_batch_exact_carry_equals_public_replay():
    ledger = _ledger(b"ta\n")
    state = _movement_carry_phase(ledger, "result")

    carried, exact = _carry_movement_phase(ledger, state)

    assert carried == read_operator_locality_standing(
        ledger, locality_identity="movement-carry"
    )
    assert exact == _validate_moved_byte_assertion(
        ledger, state["movement"].identity
    )


def test_movement_batch_does_not_reenter_public_readers_and_reopens_exactly(
    tmp_path, monkeypatch
):
    import seed_runtime.byte_measurement as byte_measurement_module
    import seed_runtime.operator_locality_standing as standing_module

    path = tmp_path / "movement-batch-carry.sqlite"
    ledger = SQLiteEventLedger(path)
    _record_operator_material_source(
        ledger,
        locality_identity="source",
        exact_bytes=b"ta",
        source_boundary="durable source",
    )
    source_result = _record_byte_measurement(
        ledger,
        source_localities=("source",),
        recording_locality_identity="source-measurement",
    )
    sources = tuple(
        assertion
        for assertion in assertions_of_recorded_byte_measurement(
            ledger, source_result.identity
        )
        if assertion.result == "count"
    )

    def refuse_public_movement_read(*_args, **_kwargs):
        raise AssertionError("same-call movement re-entered a public reader")

    reader_names = (
        "_read_assertion_locality_movement_subject_to_act_binding",
        "_read_assertion_locality_movement_act_occurrence",
        "_validate_moved_byte_assertion",
    )
    for module in (byte_measurement_module, standing_module):
        for name in reader_names:
            monkeypatch.setattr(module, name, refuse_public_movement_read)

    moved = move_recorded_byte_assertions_to_locality(
        ledger,
        sources=sources,
        destination_locality="movement-batch",
    )
    movement_identities = tuple(
        assertion.locality_movement_event_identity for assertion in moved
    )
    ledger.close()
    monkeypatch.undo()

    reopened = SQLiteEventLedger(path)
    try:
        assert tuple(
            _validate_moved_byte_assertion(reopened, identity)
            for identity in movement_identities
        ) == moved
        assert read_operator_locality_standing(
            reopened, locality_identity="movement-batch"
        )["through_event_occurrence_identity"] == movement_identities[-1]
    finally:
        reopened.close()


def test_pair_act_identity_is_not_its_occurrence_identity():
    ledger = _ledger(b"ta\n")
    source = _byte_source(ledger)
    result = record_byte_position_pair_count_layer(
        ledger,
        source_measurement_event_identity=source.identity,
        recording_locality_identity="measurement",
    )

    assert result.material["addressed_act_identity"] != result.material["act_occurrence_identity"]
    assert result.material["input_applicability"]["addressed_act_identity"] == (
        result.material["addressed_act_identity"]
    )
    assert result.material["input_applicability"]["addressed_act_occurrence_identity"] is None


def test_pair_validation_refuses_more_carrying_occurrences_than_total_pairs():
    ledger = _ledger(b"ta\n")
    source = _byte_source(ledger)
    event = record_byte_position_pair_count_layer(
        ledger,
        source_measurement_event_identity=source.identity,
        recording_locality_identity="measurement",
    )
    count = next(
        assertion
        for assertion in event.material["assertions"]
        if assertion["assertion_subject"]["content"] == [116, 97]
    )
    count["dimensions"]["content"] = {
        "input_count": 2,
        "occurrences_carrying": 2,
        "count": 1,
    }
    yield_relation = ledger.get(event.material["yield_relation_identity"])
    yield_relation.material["result"] = {
        name: event.material[name]
        for name in yield_relation.material["coordinates_of_carried_result"]
    }

    with pytest.raises(ByteMeasurementError, match="unlawful pair count"):
        assertions_of_recorded_byte_position_pair_measurement(ledger, event.identity)


def test_pair_validation_refuses_missing_count_content_without_leaking_shape_errors():
    ledger = _ledger(b"ta\n")
    source = _byte_source(ledger)
    event = record_byte_position_pair_count_layer(
        ledger,
        source_measurement_event_identity=source.identity,
        recording_locality_identity="measurement",
    )
    count = next(
        assertion
        for assertion in event.material["assertions"]
        if assertion["result"] == "count"
    )
    count["dimensions"]["content"].pop("occurrences_carrying")
    yield_relation = ledger.get(event.material["yield_relation_identity"])
    yield_relation.material["result"] = {
        name: event.material[name]
        for name in yield_relation.material["coordinates_of_carried_result"]
    }

    with pytest.raises(ByteMeasurementError, match="unlawful pair count"):
        assertions_of_recorded_byte_position_pair_measurement(ledger, event.identity)


def test_byte_result_reader_refuses_changed_yield_result_identity():
    ledger = _ledger(b"ta\n")
    event = _byte_source(ledger)
    assert assertions_of_recorded_byte_measurement(ledger, event.identity)
    yield_relation = ledger.get(event.material["yield_relation_identity"])
    yield_relation.material["result_identity"] = "crossed-byte-result"

    with pytest.raises(ByteMeasurementError, match="byte Measurement Yield relation"):
        assertions_of_recorded_byte_measurement(ledger, event.identity)


def test_pair_applicability_reader_refuses_changed_yield_result_identity():
    ledger = _ledger(b"ta\n")
    source = _byte_source(ledger)
    pair = record_byte_position_pair_count_layer(
        ledger,
        source_measurement_event_identity=source.identity,
        recording_locality_identity="measurement",
    )
    applicability_identity = pair.material["input_applicability_event_identity"]
    applicability = ledger.get(applicability_identity)
    assert get_recorded_pair_input_applicability(ledger, applicability.identity)
    yield_relation = ledger.get(
        applicability.material["yield_relation_identity"]
    )
    yield_relation.material["result_identity"] = "crossed-applicability-result"

    with pytest.raises(ByteMeasurementError, match="Applicability result is not exact"):
        get_recorded_pair_input_applicability(ledger, applicability.identity)


def test_pair_applicability_reader_revalidates_exact_input_coordinates(monkeypatch):
    ledger = _ledger(b"ta\n")
    source = _byte_source(ledger)
    pair = record_byte_position_pair_count_layer(
        ledger,
        source_measurement_event_identity=source.identity,
        recording_locality_identity="measurement",
    )

    def refuse_detached_coordinates(*_args, **_kwargs):
        raise ByteMeasurementError("detached input coordinates")

    monkeypatch.setattr(
        "seed_runtime.byte_measurement.assertions_of_recorded_byte_measurement",
        refuse_detached_coordinates,
    )
    with pytest.raises(ByteMeasurementError, match="detached input coordinates"):
        get_recorded_pair_input_applicability(
            ledger, pair.material["input_applicability_event_identity"]
        )


def test_pair_result_reader_refuses_changed_yield_result_identity():
    ledger = _ledger(b"ta\n")
    source = _byte_source(ledger)
    pair = record_byte_position_pair_count_layer(
        ledger,
        source_measurement_event_identity=source.identity,
        recording_locality_identity="measurement",
    )
    assert assertions_of_recorded_byte_position_pair_measurement(
        ledger, pair.identity
    )
    yield_relation = ledger.get(pair.material["yield_relation_identity"])
    yield_relation.material["result_identity"] = "crossed-pair-result"

    with pytest.raises(
        ByteMeasurementError, match="byte-position-pair Yield relation"
    ):
        assertions_of_recorded_byte_position_pair_measurement(ledger, pair.identity)




FIDELITY_DISTINCTIONS = {
    ("book_coordinates", "01.Source.D", "result"): (
        test_two_stages_traverse_byte_counts_once,
        test_each_exact_material_acquisition_is_counted_once_without_losing_zero_occurrence_material,
        test_each_replay_validates_each_exact_material_acquisition_and_reads_independently,
        test_opaque_bytes_supply_the_measured_subjects_without_whitespace,
        test_the_complete_declared_localities_supply_the_inputs,
        test_recurrence_exists_only_above_one,
        test_the_rule_is_mechanics_not_an_unchecked_callable,
        test_recorded_results_replay_the_complete_bounded_source_read,
        test_a_self_consistent_truncated_source_assertion_is_refused,
        test_recording_occurrence_is_validated_exactly,
        test_material_acquisition_after_the_measurement_boundary_cannot_enter_the_measurement,
        test_a_missing_declared_locality_is_refused,
        test_acquisition_result_must_match_its_exact_byte_coordinates,
        test_repeated_locality_coordinate_does_not_repeat_one_acquire,
        test_every_overlapping_byte_position_pair_is_measured,
        test_byte_position_pair_results_follow_first_observed_pair_positions,
        test_position_pairs_never_cross_material_acquisition_boundaries,
        test_position_pair_measurement_uses_exact_opaque_bytes,
        test_recorded_pair_results_replay_the_complete_bounded_source_read,
    test_same_locality_pair_result_replays_without_recording_more_work,
        test_pair_validation_refuses_a_self_consistent_truncated_result_inputs,
        test_pair_result_is_derived_from_source_without_a_measured_carrier_argument,
        test_pair_validation_does_not_perform_the_pair_measurement_again,
        test_zero_measured_pairs_is_a_lawful_exact_result,
        test_pair_validation_refuses_more_carrying_occurrences_than_total_pairs,
        test_pair_validation_refuses_missing_count_content_without_leaking_shape_errors,
        test_byte_result_reader_refuses_changed_yield_result_identity,
        test_pair_result_reader_refuses_changed_yield_result_identity,
    ),
    ("book_coordinates", "01.Current.E.1", "Applicability", "result"): (
        test_pair_validation_refuses_unsupported_input_applicability,
        test_applicability_identity_is_bound_to_one_exact_addressed_act,
        test_pair_applicability_reads_exact_input_coordinates,
        test_pair_applicability_reader_refuses_changed_yield_result_identity,
        test_pair_applicability_reader_revalidates_exact_input_coordinates,
    ),
    ("book_coordinates", "01.Source.A", "subject"): (
        test_pair_validation_requires_one_exact_ordered_content,
    ),
}
