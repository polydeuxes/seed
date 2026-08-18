from tests.binary_input import binary_input
from collections import Counter as ExactCounter
from copy import deepcopy
from io import StringIO
import hashlib
import json

import pytest

from seed_runtime.byte_measurement import (
    BYTE_PAIR_MEASUREMENT_RECORDED_KIND,
    BYTE_PAIR_APPLICABILITY_RECORDED_KIND,
    BYTE_PAIR_RESULT_COORDINATES,
    BYTE_MEASUREMENT_RECORDED_KIND,
    BYTE_MEASUREMENT_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND,
    BYTE_MEASUREMENT_RESPONSIBLE_ACT_EVIDENCE_KIND,
    BYTE_RESULT_COORDINATES,
    BYTE_MEASUREMENT_RULE,
    BYTE_PAIR_MEASUREMENT_RULE,
    ByteMeasurementError,
    RESPONSIBILITY_UNESTABLISHED,
    SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY,
    _measure_byte_counts_through,
    _record_byte_measurement_result_from_carried_act_evidence,
    _identity,
    _pair_assertion_identity,
    _pair_input_applicability,
    get_recorded_pair_input_applicability,
    get_byte_measurement_responsibility_assignment,
    assertions_of_recorded_byte_measurement,
    assertions_of_recorded_byte_position_pair_measurement,
    input_applicability_of_recorded_byte_position_pair_measurement,
    measure_byte_counts,
    record_byte_measurement_responsibility_assignment,
    record_byte_measurement_responsible_act_evidence,
    record_byte_measurement_result,
    record_byte_position_pair_count_layer,
)
from seed_runtime.events import CORRUPTED, EventLedger, SQLiteEventLedger
from seed_runtime.event import Event
from seed_runtime.operator_console import run_persistent_operator_console
from seed_runtime.operator_locality_standing import (
    _carry_byte_measurement_assignment_into_standing,
    read_operator_locality_standing,
)
from seed_runtime.evidence_of_yield_relation import RECORDED_EVIDENCE_OF_YIELD_RELATION_KIND
from seed_runtime.material_ingest import (
    MATERIAL_INGEST_OCCURRED_KIND,
    ingest_material,
)


def _record_byte_measurement(
    ledger, *, source_localities, recording_locality_identity
):
    assignment = record_byte_measurement_responsibility_assignment(
        ledger,
        source_localities=source_localities,
        recording_locality_identity=recording_locality_identity,
        locality_standing=read_operator_locality_standing(
            ledger, locality_identity=recording_locality_identity
        ),
    )
    act_evidence = record_byte_measurement_responsible_act_evidence(
        ledger,
        responsibility_assignment_event_identity=assignment.identity,
        responsibility_assignment_standing=read_operator_locality_standing(
            ledger, locality_identity=recording_locality_identity
        ),
    )
    return record_byte_measurement_result(
        ledger,
        responsible_act_evidence_event_identity=act_evidence.identity,
    )


def _record_byte_measurement_assignment_and_act(
    ledger, *, source_localities, recording_locality_identity
):
    assignment = record_byte_measurement_responsibility_assignment(
        ledger,
        source_localities=source_localities,
        recording_locality_identity=recording_locality_identity,
        locality_standing=read_operator_locality_standing(
            ledger, locality_identity=recording_locality_identity
        ),
    )
    act = record_byte_measurement_responsible_act_evidence(
        ledger,
        responsibility_assignment_event_identity=assignment.identity,
        responsibility_assignment_standing=read_operator_locality_standing(
            ledger, locality_identity=recording_locality_identity
        ),
    )
    return assignment, act


@pytest.mark.parametrize(
    ("result", "content"),
    (
        (
            "count",
            {"input_count": 17, "occurrences_carrying": 3, "count": 8},
        ),
        ("recurrence", {"recurrence_established": True}),
    ),
)
def test_fixed_pair_identity_shape_equals_the_general_canonical_identity(
    result, content
):
    representation = (0, 255)
    scope = {"source_localities": ["source-λ", "source-2"]}
    subject = {
        "representation": list(representation),
        "measurement_rule": BYTE_PAIR_MEASUREMENT_RULE,
    }

    assert _pair_assertion_identity(
        result=result,
        representation=representation,
        canonical_scope=json.dumps(
            scope, ensure_ascii=False, sort_keys=True, separators=(",", ":")
        ),
        content=content,
    ) == _identity(result=result, subject=subject, scope=scope, content=content)


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


def _ledger(text="猫\n狗\n"):
    ledger = EventLedger()
    run_persistent_operator_console(
        ledger=ledger,
        locality_identity="source",
        input_stream=binary_input(text + ""),
        output_stream=StringIO(),
    )
    return ledger


def _byte_source(ledger):
    return _record_byte_measurement(
        ledger,
        source_localities=("source",),
        recording_locality_identity="byte-measurement",
    )


def test_responsible_act_evidence_is_observable_before_yield_and_result():
    ledger = _ledger("a\n")

    assignment, act_evidence = _record_byte_measurement_assignment_and_act(
        ledger,
        source_localities=("source",),
        recording_locality_identity="measurement",
    )

    assert act_evidence.kind == BYTE_MEASUREMENT_RESPONSIBLE_ACT_EVIDENCE_KIND
    assert ledger.list_locality("measurement") == [assignment, act_evidence]
    assert act_evidence.material["source_localities"] == ["source"]
    assert act_evidence.material["responsibility_assignment_reference"][
        "recorded_occurrence_identity"
    ] == assignment.identity

    result = record_byte_measurement_result(
        ledger,
        responsible_act_evidence_event_identity=act_evidence.identity,
    )
    events = ledger.list_locality("measurement")
    assert [event.kind for event in events] == [
        BYTE_MEASUREMENT_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND,
        BYTE_MEASUREMENT_RESPONSIBLE_ACT_EVIDENCE_KIND,
        RECORDED_EVIDENCE_OF_YIELD_RELATION_KIND,
        BYTE_MEASUREMENT_RECORDED_KIND,
    ]
    assert result.material["responsible_act_evidence_identity"] == act_evidence.identity
    assert result.material["evidence_of_yield_relation_identity"] == events[2].identity
    assert ledger.occurrences_in_append_order(
        (assignment.identity, act_evidence.identity, events[2].identity, result.identity),
        locality_identity="measurement",
    ) == events


def test_exact_byte_assignment_enters_standing_and_owns_distinct_lifecycle_identities():
    ledger = _ledger("a\n")
    assignment = record_byte_measurement_responsibility_assignment(
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

    assert assignment.kind == BYTE_MEASUREMENT_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND
    assert standing["responsibility_assignment_occurrences"] == {
        assignment.identity: None
    }
    assert "standing" not in assignment.material
    act = record_byte_measurement_responsible_act_evidence(
        ledger,
        responsibility_assignment_event_identity=assignment.identity,
        responsibility_assignment_standing=standing,
    )
    result = record_byte_measurement_result(
        ledger, responsible_act_evidence_event_identity=act.identity
    )
    yield_evidence = ledger.get(result.material["evidence_of_yield_relation_identity"])
    identities = {
        assignment.identity,
        assignment.material["assignment_identity"],
        assignment.material["assignment_subject_identity"],
        assignment.material["measurement_act_identity"],
        assignment.material["act_occurrence_identity"],
        assignment.material["measurement_result_identity"],
        act.identity,
        yield_evidence.identity,
        result.identity,
    }
    assert len(identities) == 9
    assert result.material["responsibility_assignment_reference"] == {
        "recorded_occurrence_identity": assignment.identity,
        "assignment_identity": assignment.material["assignment_identity"],
        "assignment_subject_identity": assignment.material[
            "assignment_subject_identity"
        ],
    }
    assert "responsibility_assignment_evidence" not in act.material
    assert "responsibility_assignment_evidence" not in result.material


def test_stale_and_shaped_standing_cannot_authorize_exact_byte_act():
    ledger = _ledger("a\n")
    stale = read_operator_locality_standing(
        ledger, locality_identity="measurement"
    )
    assignment = record_byte_measurement_responsibility_assignment(
        ledger,
        source_localities=("source",),
        recording_locality_identity="measurement",
        locality_standing=stale,
    )
    shaped = deepcopy(
        read_operator_locality_standing(ledger, locality_identity="measurement")
    )
    shaped["responsibility_assignment_occurrences"] = {
        "same-shaped-assignment": None
    }

    for standing in (stale, shaped):
        with pytest.raises(
            ByteMeasurementError, match="exact current Locality Standing"
        ):
            record_byte_measurement_responsible_act_evidence(
                ledger,
                responsibility_assignment_event_identity=assignment.identity,
                responsibility_assignment_standing=standing,
            )


def test_corrupted_exact_byte_assignment_cannot_authorize_an_act():
    ledger = _ledger("a\n")
    assignment = record_byte_measurement_responsibility_assignment(
        ledger,
        source_localities=("source",),
        recording_locality_identity="measurement",
        locality_standing=read_operator_locality_standing(
            ledger, locality_identity="measurement"
        ),
    )
    assignment.material["responsibility"] = "corrupted Responsibility"

    with pytest.raises(ByteMeasurementError, match="coordinates are not exact"):
        get_byte_measurement_responsibility_assignment(
            ledger, assignment.identity
        )


def test_assignment_read_refuses_corrupted_unrelated_prior_standing_carrier():
    ledger = IntegrityCountingLedger()
    ingest_material(
        ledger,
        locality_identity="measurement",
        exact_bytes=b"ab",
        source_role="test source",
        source_boundary="test boundary",
    )
    first = _record_byte_measurement(
        ledger,
        source_localities=("measurement",),
        recording_locality_identity="measurement",
    )
    second = record_byte_measurement_responsibility_assignment(
        ledger,
        source_localities=("measurement",),
        recording_locality_identity="measurement",
        locality_standing=read_operator_locality_standing(
            ledger, locality_identity="measurement"
        ),
    )
    ledger.corrupted.add(first.identity)

    with pytest.raises(ByteMeasurementError):
        get_byte_measurement_responsibility_assignment(ledger, second.identity)


def test_operator_replay_uses_exact_context_while_public_assignment_reads_reconstruct(
    monkeypatch,
):
    from seed_runtime import operator_locality_standing as standing_module

    ledger = IntegrityCountingLedger()
    ingest_material(
        ledger,
        locality_identity="measurement",
        exact_bytes=b"ab",
        source_role="test source",
        source_boundary="test boundary",
    )
    first = _record_byte_measurement(
        ledger,
        source_localities=("measurement",),
        recording_locality_identity="measurement",
    )
    second = record_byte_measurement_responsibility_assignment(
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
    assert standing["responsibility_assignment_occurrences"][second.identity] is None
    with pytest.raises(AssertionError, match="nested operator Standing replay"):
        get_byte_measurement_responsibility_assignment(ledger, second.identity)

    monkeypatch.setattr(
        standing_module,
        "read_operator_locality_standing_through",
        original_read_through,
    )
    assert get_byte_measurement_responsibility_assignment(
        ledger, second.identity
    ) == second
    ledger.corrupted.add(first.identity)
    with pytest.raises(ByteMeasurementError):
        get_byte_measurement_responsibility_assignment(ledger, second.identity)


def test_assignment_act_and_result_survive_distinct_sqlite_restarts(tmp_path):
    path = tmp_path / "byte-assignment-restart.sqlite"
    ledger = SQLiteEventLedger(path)
    ingest_material(
        ledger,
        locality_identity="source",
        exact_bytes=b"durable",
        source_role="operator",
        source_boundary="durable boundary",
    )
    assignment = record_byte_measurement_responsibility_assignment(
        ledger,
        source_localities=("source",),
        recording_locality_identity="measurement",
        locality_standing=read_operator_locality_standing(
            ledger, locality_identity="measurement"
        ),
    )
    ledger.close()

    ledger = SQLiteEventLedger(path)
    assert get_byte_measurement_responsibility_assignment(
        ledger, assignment.identity
    ).identity == assignment.identity
    act = record_byte_measurement_responsible_act_evidence(
        ledger,
        responsibility_assignment_event_identity=assignment.identity,
        responsibility_assignment_standing=read_operator_locality_standing(
            ledger, locality_identity="measurement"
        ),
    )
    ledger.close()

    ledger = SQLiteEventLedger(path)
    result = record_byte_measurement_result(
        ledger, responsible_act_evidence_event_identity=act.identity
    )
    ledger.close()

    ledger = SQLiteEventLedger(path)
    assert assertions_of_recorded_byte_measurement(ledger, result.identity)
    ledger.close()


def test_console_exact_byte_same_call_path_does_not_use_public_standing_gate(
    monkeypatch,
):
    from seed_runtime import byte_measurement

    def forbidden(*args, **kwargs):
        raise AssertionError("console byte lifecycle must use carried Standing")

    monkeypatch.setattr(
        byte_measurement,
        "_require_current_byte_measurement_standing",
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
        output_stream=StringIO(),
    )
    assert any(
        event.kind == BYTE_MEASUREMENT_RECORDED_KIND
        for event in ledger.list_locality("source")
    )


def test_call_local_assignment_carry_requires_the_exact_assignment_at_tip():
    ledger = _ledger("a\n")
    standing = read_operator_locality_standing(
        ledger, locality_identity="measurement"
    )
    prior_boundary = standing["through_event_occurrence_identity"]
    assignment = record_byte_measurement_responsibility_assignment(
        ledger,
        source_localities=("source",),
        recording_locality_identity="measurement",
        locality_standing=standing,
    )
    ingest_material(
        ledger,
        locality_identity="unrelated",
        exact_bytes=b"later",
        source_role="test source",
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
    ledger = _ledger("a\n")
    assignment, act = _record_byte_measurement_assignment_and_act(
        ledger,
        source_localities=("source",),
        recording_locality_identity="measurement",
    )
    standing = read_operator_locality_standing(
        ledger, locality_identity="measurement"
    )
    ingest_material(
        ledger,
        locality_identity="unrelated",
        exact_bytes=b"later",
        source_role="test source",
        source_boundary="after act",
    )

    with pytest.raises(
        ByteMeasurementError, match="exact carried lifecycle occurrences"
    ):
        _record_byte_measurement_result_from_carried_act_evidence(
            ledger,
            responsible_act_evidence=act,
            responsibility_assignment=assignment,
            locality_standing=standing,
        )


def test_reopened_public_result_refuses_an_act_already_consumed(tmp_path):
    path = tmp_path / "byte-consumed-act.sqlite"
    ledger = SQLiteEventLedger(path)
    ingest_material(
        ledger,
        locality_identity="source",
        exact_bytes=b"a",
        source_role="test source",
        source_boundary="durable source",
    )
    _assignment, act = _record_byte_measurement_assignment_and_act(
        ledger,
        source_localities=("source",),
        recording_locality_identity="measurement",
    )
    record_byte_measurement_result(
        ledger, responsible_act_evidence_event_identity=act.identity
    )
    ledger.close()

    ledger = SQLiteEventLedger(path)
    with pytest.raises(ByteMeasurementError, match="already has a Yield or result"):
        record_byte_measurement_result(
            ledger, responsible_act_evidence_event_identity=act.identity
        )
    ledger.close()


def test_old_unassigned_exact_byte_act_api_is_not_accepted():
    ledger = _ledger("a\n")
    with pytest.raises(TypeError):
        record_byte_measurement_responsible_act_evidence(
            ledger,
            source_localities=("source",),
            recording_locality_identity="measurement",
        )


def test_two_stages_traverse_byte_counts_once(monkeypatch):
    from seed_runtime import byte_measurement

    ledger = _ledger("ab\n")
    calls = []
    original = byte_measurement._measure_byte_counts_through

    def count(*args, **kwargs):
        calls.append(kwargs["boundary"].identity)
        return original(*args, **kwargs)

    monkeypatch.setattr(byte_measurement, "_measure_byte_counts_through", count)
    assignment, act_evidence = _record_byte_measurement_assignment_and_act(
        ledger,
        source_localities=("source",),
        recording_locality_identity="measurement",
    )
    assert calls == []

    record_byte_measurement_result(
        ledger,
        responsible_act_evidence_event_identity=act_evidence.identity,
    )
    assert calls == [
        assignment.material["completeness_boundary_identity"]
    ]


def test_each_exact_ingest_is_counted_once_without_losing_zero_occurrence_material(
    monkeypatch,
):
    from seed_runtime import byte_measurement

    ledger = EventLedger()
    materials = (
        b'{"function":"unobserved","occurrence_count":0}',
        b'{"function":"observed","occurrence_count":2}',
    )
    ingests = tuple(
        ingest_material(
            ledger,
            locality_identity="measurement-sidecar",
            exact_bytes=material,
            source_role="implementation function Measurement",
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
    assert tuple(ingest.exact_material for ingest in ingests) == materials
    assert b'"occurrence_count":0' in ingests[0].exact_material
    expected_totals = ExactCounter(b"".join(materials))
    expected_carrying = {
        value: sum(value in material for material in materials)
        for value in expected_totals
    }
    assert {
        item.representation: (item.occurrences_carrying, item.count)
        for item in measured.counts
    } == {
        value: (expected_carrying[value], count)
        for value, count in expected_totals.items()
    }


def test_each_replay_validates_each_exact_ingest_and_reads_independently():
    ledger = IntegrityCountingLedger()
    materials = (
        b'{"function":"unobserved","occurrence_count":0}',
        b'{"function":"observed","occurrence_count":2}',
    )
    ingests = tuple(
        ingest_material(
            ledger,
            locality_identity="measurement-sidecar",
            exact_bytes=material,
            source_role="implementation function Measurement",
            source_boundary=f"sidecar-{position}",
        )
        for position, material in enumerate(materials)
    )
    _assignment, act_evidence = _record_byte_measurement_assignment_and_act(
        ledger,
        source_localities=("measurement-sidecar",),
        recording_locality_identity="measurement-sidecar",
    )
    ledger.integrity_calls.clear()

    result = record_byte_measurement_result(
        ledger,
        responsible_act_evidence_event_identity=act_evidence.identity,
    )

    after_result = [ledger.integrity_calls[ingest.identity] for ingest in ingests]
    assert all(count > 0 for count in after_result)
    assert tuple(ingest.exact_material for ingest in ingests) == materials

    assert assertions_of_recorded_byte_measurement(ledger, result.identity)
    after_read = [ledger.integrity_calls[ingest.identity] for ingest in ingests]
    assert all(after > before for after, before in zip(after_read, after_result))

    ledger.corrupted.add(ingests[0].identity)
    with pytest.raises(ByteMeasurementError, match="not an intact Ingest"):
        assertions_of_recorded_byte_measurement(ledger, result.identity)


def test_yield_resolves_the_exact_act_evidence_after_reopen(tmp_path):
    path = str(tmp_path / "measurement.sqlite")
    ledger = SQLiteEventLedger(path)
    ingest_material(
        ledger,
        locality_identity="source",
        exact_bytes=b"durable",
        source_role="operator",
        source_boundary="durable boundary",
    )
    assignment, act_evidence = _record_byte_measurement_assignment_and_act(
        ledger,
        source_localities=("source",),
        recording_locality_identity="measurement",
    )
    act_evidence_identity = act_evidence.identity
    assignment_identity = assignment.identity
    ledger.close()

    ledger = SQLiteEventLedger(path)
    try:
        result = record_byte_measurement_result(
            ledger,
            responsible_act_evidence_event_identity=act_evidence_identity,
        )
        assert result.material["responsible_act_evidence_identity"] == (
            act_evidence_identity
        )
        assert result.material["responsibility_assignment_reference"][
            "recorded_occurrence_identity"
        ] == assignment_identity
        assert assertions_of_recorded_byte_measurement(ledger, result.identity)
    finally:
        ledger.close()


def test_material_appended_after_act_evidence_cannot_enter_its_result():
    ledger = _ledger("a")
    _assignment, act_evidence = _record_byte_measurement_assignment_and_act(
        ledger,
        source_localities=("source",),
        recording_locality_identity="measurement",
    )
    ingest_material(
        ledger,
        locality_identity="source",
        exact_bytes=b"b",
        source_role="operator",
        source_boundary="later boundary",
    )

    result = record_byte_measurement_result(
        ledger,
        responsible_act_evidence_event_identity=act_evidence.identity,
    )
    counts = {
        item.representation: item.material["dimensions"]["content"]["count"]
        for item in assertions_of_recorded_byte_measurement(ledger, result.identity)
        if item.result == "count"
    }
    assert counts == {97: 1}


def test_one_responsible_act_occurrence_cannot_yield_twice(monkeypatch):
    from seed_runtime import byte_measurement

    ledger = _ledger("a\n")
    _assignment, act_evidence = _record_byte_measurement_assignment_and_act(
        ledger,
        source_localities=("source",),
        recording_locality_identity="measurement",
    )
    record_byte_measurement_result(
        ledger,
        responsible_act_evidence_event_identity=act_evidence.identity,
    )
    event_count = len(ledger.list())

    def forbidden(*args, **kwargs):
        raise AssertionError("a consumed Act occurrence must not be measured again")

    monkeypatch.setattr(byte_measurement, "_measure_byte_counts_through", forbidden)

    with pytest.raises(ByteMeasurementError, match="already has a Yield or result"):
        record_byte_measurement_result(
            ledger,
            responsible_act_evidence_event_identity=act_evidence.identity,
        )
    assert len(ledger.list()) == event_count


@pytest.mark.parametrize("identity", ("missing", None))
def test_yield_refuses_missing_responsible_act_evidence(identity):
    with pytest.raises(ByteMeasurementError, match="exact responsible Act Evidence"):
        record_byte_measurement_result(
            EventLedger(),
            responsible_act_evidence_event_identity=identity,
        )


def test_yield_refuses_a_different_occurrence_kind():
    ledger = _ledger("a\n")
    wrong = next(event for event in ledger.list() if event.locality_identity == "source")

    with pytest.raises(ByteMeasurementError, match="exact responsible Act Evidence"):
        record_byte_measurement_result(
            ledger,
            responsible_act_evidence_event_identity=wrong.identity,
        )


def test_exact_bytes_supply_the_measured_subjects_without_whitespace():
    measured = measure_byte_counts(
        _ledger(), source_localities=("source",)
    )
    counts = {item.representation: item for item in measured.counts}

    # UTF-8 猫 = e7 8c ab and 狗 = e7 8b 97.  No character boundary is used or
    # asserted; these are the exact bytes Seed recorded.
    assert counts[231].count == 2
    assert counts[140].count == 1
    assert counts[171].count == 1
    assert counts[139].count == 1
    assert counts[151].count == 1
    assert counts[10].count == 2
    assert len(measured.source_material) == 2


def test_the_complete_declared_localities_supply_the_inputs():
    measured = measure_byte_counts(
        _ledger("a\nb\n"), source_localities=("source",)
    )
    assert len(measured.source_material) == 2
    assert all(
        set(item) == {"ingest_occurrence_identity"}
        for item in measured.source_material
    )
    assert measured.completeness_boundary.identity


def test_count_and_recurrence_are_distinct_results():
    event = _record_byte_measurement(
        _ledger("ab\n"),
        source_localities=("source",),
        recording_locality_identity="measurement",
    )
    by_byte = {}
    for assertion in event.material["assertions"]:
        representation = assertion["assertion_subject"].get("representation")
        if representation is not None:
            by_byte.setdefault(representation, []).append(assertion)

    assert [item["result"] for item in by_byte[97]] == ["count"]
    assert by_byte[97][0]["dimensions"]["content"]["count"] == 1
    # The newline occurs once too. No positive singleton is called recurrence.
    assert [item["result"] for item in by_byte[10]] == ["count"]


def test_recurrence_exists_only_above_one():
    event = _record_byte_measurement(
        _ledger("aa\n"),
        source_localities=("source",),
        recording_locality_identity="measurement",
    )
    results = [
        item["result"]
        for item in event.material["assertions"]
        if item["assertion_subject"].get("representation") == 97
    ]
    assert results == ["count", "recurrence"]


def test_the_rule_is_mechanics_not_an_unchecked_callable():
    event = _record_byte_measurement(
        _ledger("the cat\n"),
        source_localities=("source",),
        recording_locality_identity="measurement",
    )
    assert event.material["measurement_rule"] == BYTE_MEASUREMENT_RULE
    assert event.kind == BYTE_MEASUREMENT_RECORDED_KIND
    assert "zebra" not in str(event.material)


def test_recorded_results_replay_the_complete_bounded_source_read():
    ledger = _ledger("猫\n狗\n")
    event = _record_byte_measurement(
        ledger,
        source_localities=("source",),
        recording_locality_identity="measurement",
    )
    read = assertions_of_recorded_byte_measurement(ledger, event.identity)
    assert read
    assert all(item.recorded_occurrence_identity == event.identity for item in read)
    evidence = ledger.get(event.material["evidence_of_yield_relation_identity"])
    assert evidence.kind == RECORDED_EVIDENCE_OF_YIELD_RELATION_KIND
    assert evidence.material["dimensions"]["act_occurrence_identity"] == event.material[
        "act_occurrence_identity"
    ]
    assert evidence.material["coordinates_of_carried_result"] == [
        "result_identity",
        "dimensions",
        "exact_act",
        "downstream_act_identity",
        "act_occurrence_identity",
        "responsibility",
        "responsible_boundary",
        "responsibility_assignment_reference",
        "measurement_rule",
        "source_localities",
        "completeness_boundary",
        "assertions",
    ]
    assert "occurrence_preservation" not in evidence.material["coordinates_of_carried_result"]

    count = next(
        item
        for item in read
        if item.representation == 231 and item.result == "count"
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
    assert count.material["dimensions"]["authority"] == "unestablished"
    assert count.material["dimensions"]["evidence_scope"]
    assert count.material["unknown"]
    assert count.material["conflicts"] == "Unknown"
    assert count.material["limits"]
    assert count.support_assertion_references == (
        {
            "recorded_occurrence_identity": event.identity,
            "assertion_identity": event.material["assertions"][0]["dimensions"]["identity"],
        },
    )

    detached_material = count.material
    detached_material["dimensions"]["standing"] = "unsupported"
    assert "standing" not in count.material["dimensions"]

    detached_references = count.support_assertion_references
    detached_references[0]["assertion_identity"] = "unsupported"
    assert count.support_assertion_references[0]["assertion_identity"] != "unsupported"

    # Read preserves exact durable JSON kinds. It does not protect the
    # result by transmuting lists to tuples or dicts to proxy objects.
    represented = Event(
        identity="re-represented",
        kind="test.representation",
        material=count.material,
    )
    assert type(represented.material) is dict
    assert type(represented.material["assertion_scope"]["source_localities"]) is list


def test_a_self_consistent_truncated_source_assertion_is_refused():
    ledger = _ledger("a\nb\n")
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
    evidence = ledger.get(event.material["evidence_of_yield_relation_identity"])
    evidence.material["result"] = {
        name: event.material[name]
        for name in evidence.material["coordinates_of_carried_result"]
    }
    with pytest.raises(ByteMeasurementError, match="complete bounded source read"):
        assertions_of_recorded_byte_measurement(ledger, event.identity)


def test_recording_occurrence_evidence_is_validated_exactly():
    ledger = _ledger("a\n")
    event = _record_byte_measurement(
        ledger,
        source_localities=("source",),
        recording_locality_identity="measurement",
    )
    event.material["occurrence_preservation"] = "something else"
    with pytest.raises(ByteMeasurementError, match="recording-occurrence Evidence"):
        assertions_of_recorded_byte_measurement(ledger, event.identity)


def test_ingest_after_the_measurement_boundary_cannot_enter_the_measurement():
    ledger = EventLedger()
    ingest_material(
        ledger,
        locality_identity="source",
        exact_bytes=b"a",
        source_role="operator",
        source_boundary="first boundary",
    )
    boundary = ledger.append_boundary()
    ingest_material(
        ledger,
        locality_identity="source",
        exact_bytes=b"b",
        source_role="system",
        source_boundary="second boundary",
    )
    measured = _measure_byte_counts_through(
        ledger,
        localities=("source",),
        boundary=boundary,
    )
    assert {item.representation: item.count for item in measured.counts} == {97: 1}


def test_a_missing_declared_locality_is_refused():
    with pytest.raises(ByteMeasurementError, match="absent"):
        measure_byte_counts(
            _ledger(), source_localities=("missing",)
        )


def test_ingest_must_match_its_exact_byte_coordinates():
    ledger = _ledger("a\n")
    ingest = next(
        ledger.iter_locality_kind("source", MATERIAL_INGEST_OCCURRED_KIND)
    )
    object.__setattr__(ingest, "exact_material", None)
    with pytest.raises(ByteMeasurementError, match="carries no exact bytes"):
        measure_byte_counts(
            ledger, source_localities=("source",)
        )


def test_repeated_locality_coordinate_does_not_repeat_one_ingest():
    ledger = _ledger("a\n")
    once = measure_byte_counts(
        ledger, source_localities=("source",)
    )
    repeated = measure_byte_counts(
        ledger, source_localities=("source", "source")
    )
    assert repeated == once


def test_every_overlapping_byte_position_pair_is_measured():
    ledger = _ledger("tatatata\n")
    source = _byte_source(ledger)
    event = record_byte_position_pair_count_layer(
        ledger,
        source_measurement_event_identity=source.identity,
        recording_locality_identity="measurement",
    )
    counts = {
        tuple(item["assertion_subject"]["representation"]): item["dimensions"]["content"]
        for item in event.material["assertions"]
        if item["result"] == "count"
    }

    assert counts[(116, 97)]["count"] == 4
    assert counts[(97, 116)]["count"] == 3
    assert counts[(97, 10)]["count"] == 1


def test_byte_position_pair_results_follow_first_observed_pair_positions():
    ledger = _ledger("tatatata\n")
    source = _byte_source(ledger)
    event = record_byte_position_pair_count_layer(
        ledger,
        source_measurement_event_identity=source.identity,
        recording_locality_identity="measurement",
    )

    assert [
        tuple(assertion["assertion_subject"]["representation"])
        for assertion in event.material["assertions"]
        if assertion["result"] == "count"
    ] == [(116, 97), (97, 116), (97, 10)]


def test_position_pairs_never_cross_ingest_boundaries():
    ledger = _ledger("a\nb\n")
    source = _byte_source(ledger)
    event = record_byte_position_pair_count_layer(
        ledger,
        source_measurement_event_identity=source.identity,
        recording_locality_identity="measurement",
    )
    counts = {
        tuple(item["assertion_subject"]["representation"]): item["dimensions"]["content"][
            "count"
        ]
        for item in event.material["assertions"]
        if item["result"] == "count"
    }

    assert counts == {(97, 10): 1, (98, 10): 1}
    assert (10, 98) not in counts


def test_position_pair_measurement_remains_byte_not_character_based():
    ledger = _ledger("猫\n")
    source = _byte_source(ledger)
    event = record_byte_position_pair_count_layer(
        ledger,
        source_measurement_event_identity=source.identity,
        recording_locality_identity="measurement",
    )
    counts = {
        tuple(item["assertion_subject"]["representation"])
        for item in event.material["assertions"]
        if item["result"] == "count"
    }

    # UTF-8 bytes e7 8c ab plus the recorded newline. These are ordered byte pairs,
    # not a Assertion that any pair is a character.
    assert counts == {(231, 140), (140, 171), (171, 10)}


def test_pair_count_and_recurrence_are_separate_results():
    ledger = _ledger("tatatata\n")
    source = _byte_source(ledger)
    event = record_byte_position_pair_count_layer(
        ledger,
        source_measurement_event_identity=source.identity,
        recording_locality_identity="measurement",
    )
    assert event.kind == BYTE_PAIR_MEASUREMENT_RECORDED_KIND
    by_pair = {}
    for assertion in event.material["assertions"]:
        representation = assertion["assertion_subject"].get("representation")
        if representation is not None:
            by_pair.setdefault(tuple(representation), []).append(assertion)

    assert [item["result"] for item in by_pair[(116, 97)]] == ["count", "recurrence"]
    assert [item["result"] for item in by_pair[(97, 10)]] == ["count"]
    assert by_pair[(116, 97)][1]["input_support"]["local_assertion_references"] == [
        by_pair[(116, 97)][0]["dimensions"]["identity"]
    ]
    moved_reference = by_pair[(116, 97)][0]["input_support"]["assertion_references"][0]
    original = next(
        item
        for item in assertions_of_recorded_byte_measurement(ledger, source.identity)
        if item.result == "exact_source_material_set"
    )
    assert moved_reference["assertion_identity"] == original.assertion_identity
    assert moved_reference["recorded_occurrence_identity"] == original.recorded_occurrence_identity
    assert event.material["source_movement_event_identity"] != original.recorded_occurrence_identity
    applicability = input_applicability_of_recorded_byte_position_pair_measurement(
        ledger, event.identity
    )
    assert applicability["dimensions"]["standing"] == "applicable"
    assert applicability["input_assertion_reference"] == event.material["source_assertion_reference"]
    assert applicability["result_boundary"]
    assert applicability["downstream_act"] == "declared byte-position-pair Measurement"
    assert applicability["measurement_locality"] == "measurement"
    assert applicability["input_unknown"]
    assert applicability["input_limits"]
    assert applicability["conflicts"] == []
    assert applicability["input_standing"] == {
        "recorded_measurement_result_occurrence_identity": source.identity,
        "assertion_identity": original.assertion_identity,
        "locality_movement_result_occurrence_identity": event.material[
            "source_movement_event_identity"
        ],
    }
    assert applicability["coordinate_treatment"]["support_relation_standing"] == {
        "carried": False,
        "treatment": "not established by Applicability",
    }


def test_recorded_pair_results_replay_the_complete_bounded_source_read():
    ledger = _ledger("tatatata\n")
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
    assert {item.representation for item in read if item.representation} == {
        (116, 97),
        (97, 116),
        (97, 10),
    }
    count = next(
        item
        for item in read
        if item.representation == (116, 97) and item.result == "count"
    )
    detached = count.material
    detached["dimensions"]["standing"] = "unsupported"
    assert "standing" not in count.material["dimensions"]
    assert count.support_assertion_references[0]["recorded_occurrence_identity"] == source.identity
    movement = ledger.get(event.material["source_movement_event_identity"])
    assert movement.material["source_assertion_reference"]["recorded_occurrence_identity"] == source.identity
    assert movement.material["assertion_identity"] == count.support_assertion_references[0]["assertion_identity"]
    assert movement.material["source_locality"] == "byte-measurement"
    assert movement.material["destination_locality"] == "measurement"
    assert movement.material["movement_act_identity"] != movement.material[
        "movement_act_occurrence_identity"
    ]
    act_evidence = ledger.get(movement.material["responsible_act_evidence_identity"])
    assert act_evidence.material["movement_act_identity"] == movement.material[
        "movement_act_identity"
    ]
    assert act_evidence.material["movement_act_occurrence_identity"] == movement.material[
        "movement_act_occurrence_identity"
    ]
    assert "dimensions" not in movement.material


def test_pair_validation_refuses_a_self_consistent_truncated_result_inputs():
    ledger = _ledger("tatatata\n")
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
        if assertion["dimensions"]["identity"]
        != recurrence["dimensions"]["identity"]
    ]
    evidence = ledger.get(event.material["evidence_of_yield_relation_identity"])
    evidence.material["result"] = {
        name: value
        for name, value in event.material.items()
        if name in BYTE_PAIR_RESULT_COORDINATES
    }

    with pytest.raises(ByteMeasurementError, match="recurrence boundary"):
        assertions_of_recorded_byte_position_pair_measurement(ledger, event.identity)


@pytest.mark.parametrize(
    "representation",
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
def test_pair_validation_requires_one_exact_ordered_representation(representation):
    ledger = _ledger("ta\n")
    source = _byte_source(ledger)
    event = record_byte_position_pair_count_layer(
        ledger,
        source_measurement_event_identity=source.identity,
        recording_locality_identity="measurement",
    )
    assertion = event.material["assertions"][0]
    assertion["assertion_subject"]["representation"] = representation
    assertion["dimensions"]["identity"] = _identity(
        result=assertion["result"],
        subject=assertion["assertion_subject"],
        scope=assertion["assertion_scope"],
        content=assertion["dimensions"]["content"],
    )
    evidence = ledger.get(event.material["evidence_of_yield_relation_identity"])
    evidence.material["result"] = {
        name: event.material[name]
        for name in evidence.material["coordinates_of_carried_result"]
    }

    with pytest.raises(ByteMeasurementError, match="unlawful pair Assertion"):
        assertions_of_recorded_byte_position_pair_measurement(ledger, event.identity)


def test_pair_validation_does_not_perform_the_pair_measurement_again(monkeypatch):
    ledger = _ledger("tatatata\n")
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
    ledger = _ledger("tatatata\n")
    source = _byte_source(ledger)
    event = record_byte_position_pair_count_layer(
        ledger,
        source_measurement_event_identity=source.identity,
        recording_locality_identity="measurement",
    )
    event.material["input_applicability"]["result_boundary"] = "some other use"
    evidence = ledger.get(event.material["evidence_of_yield_relation_identity"])
    evidence.material["result"] = {
        name: event.material[name]
        for name in evidence.material["coordinates_of_carried_result"]
    }

    with pytest.raises(ByteMeasurementError, match="historical input Applicability"):
        assertions_of_recorded_byte_position_pair_measurement(ledger, event.identity)


def test_zero_measured_pairs_is_a_lawful_exact_result():
    ledger = _ledger("\n")
    source = _byte_source(ledger)
    event = record_byte_position_pair_count_layer(
        ledger,
        source_measurement_event_identity=source.identity,
        recording_locality_identity="measurement",
    )

    assert event.material["assertions"] == []
    assert assertions_of_recorded_byte_position_pair_measurement(ledger, event.identity) == ()


def test_applicability_identity_is_bound_to_one_exact_downstream_act():
    ledger = _ledger("ta\n")
    source_event = _byte_source(ledger)
    source = next(
        item
        for item in assertions_of_recorded_byte_measurement(ledger, source_event.identity)
        if item.result == "exact_source_material_set"
    )
    first = _pair_input_applicability(
        ledger,
        source,
        downstream_act_identity="pair-act-1",
        applicability_act_identity="applicability-act-1",
        applicability_act_occurrence_identity="applicability-occurrence-1",
        measurement_locality_identity="byte-measurement",
    )
    second = _pair_input_applicability(
        ledger,
        source,
        downstream_act_identity="pair-act-2",
        applicability_act_identity="applicability-act-2",
        applicability_act_occurrence_identity="applicability-occurrence-2",
        measurement_locality_identity="byte-measurement",
    )

    assert first["dimensions"]["identity"] != second["dimensions"]["identity"]
    assert first["responsibility"]
    assert first["responsibility"] != first["assigned_by_responsibility"]
    assert first["downstream_act_identity"] == "pair-act-1"
    assert first["downstream_act_occurrence_identity"] is None


def test_pair_applicability_reads_exact_result_standing_instead_of_scalar():
    ledger = _ledger("ta\n")
    source_event = _byte_source(ledger)
    source = next(
        item
        for item in assertions_of_recorded_byte_measurement(ledger, source_event.identity)
        if item.result == "exact_source_material_set"
    )
    detached = source.material
    detached["dimensions"]["standing"] = "reported"
    detached_source = type(source)(
        assertion_identity=source.assertion_identity,
        recorded_occurrence_identity=source.recorded_occurrence_identity,
        representation=source.representation,
        result=source.result,
        _material_json=json.dumps(detached),
        _support_assertion_refs_json="[]",
    )
    applicable = _pair_input_applicability(
        ledger,
        detached_source,
        downstream_act_identity="pair-act-exact-standing",
        applicability_act_identity="applicability-act-exact-standing",
        applicability_act_occurrence_identity="applicability-occurrence-exact-standing",
        measurement_locality_identity="byte-measurement",
    )

    assert applicable["dimensions"]["standing"] == "applicable"
    assert applicable["conflicts"] == []
    assert applicable["input_standing"] == {
        "recorded_measurement_result_occurrence_identity": source.recorded_occurrence_identity,
        "assertion_identity": source.assertion_identity,
        "locality_movement_result_occurrence_identity": None,
    }
    assert applicable["input_assertion_reference"] == source.reference
    assert applicable["downstream_act_occurrence_identity"] is None


def test_seed_native_measurement_and_result_assertions_keep_distinct_responsibilities():
    ledger = _ledger("ta\n")
    source = _byte_source(ledger)
    result = record_byte_position_pair_count_layer(
        ledger,
        source_measurement_event_identity=source.identity,
        recording_locality_identity="measurement",
    )
    applicability = get_recorded_pair_input_applicability(
        ledger, result.material["input_applicability_event_identity"]
    )

    assert result.material["responsible_boundary"] == (
        SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY
    )
    assert applicability["responsible_boundary"] == (
        SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY
    )
    assert source.material["responsibility"] != result.material["responsibility"]
    assert source.material["responsible_boundary"] == (
        SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY
    )
    for assertion in result.material["assertions"]:
        assert assertion["dimensions"]["responsibility"] != result.material["responsibility"]


def test_seed_native_responsibility_is_earned_from_preserved_occurrences():
    ledger = _ledger("ta\n")
    source = _byte_source(ledger)
    assignment = get_byte_measurement_responsibility_assignment(
        ledger,
        source.material["responsibility_assignment_reference"][
            "recorded_occurrence_identity"
        ],
    ).material
    source_set = next(
        assertion
        for assertion in source.material["assertions"]
        if assertion["result"] == "exact_source_material_set"
    )

    assert assignment["responsible_boundary"] == "this Seed"
    assert assignment["source_occurrence_references"] == source_set["dimensions"][
        "content"
    ]["source_material"]
    assert assignment["completeness_boundary_identity"] == source.material[
        "completeness_boundary"
    ]["identity"]
    evidence_of_yield_relation = ledger.get(source.material["evidence_of_yield_relation_identity"])
    assert evidence_of_yield_relation.material["dimensions"]["responsible_boundary"] == (
        "this Seed"
    )


def test_locality_movement_assignment_is_earned_from_the_exact_source():
    ledger = _ledger("ta\n")
    source = _byte_source(ledger)
    pair = record_byte_position_pair_count_layer(
        ledger,
        source_measurement_event_identity=source.identity,
        recording_locality_identity="measurement",
    )
    movement = ledger.get(pair.material["source_movement_event_identity"])
    assignment = movement.material["responsibility_assignment_evidence"]

    assert assignment == {
        "responsible_boundary": "this Seed",
        "standing": "assigned",
        "source_assertion_reference": movement.material["source_assertion_reference"],
        "source_locality": "byte-measurement",
        "destination_locality": "measurement",
        "determination": "the exact preserved Assertion available in another Locality",
    }


def test_pair_act_identity_is_not_its_occurrence_identity():
    ledger = _ledger("ta\n")
    source = _byte_source(ledger)
    result = record_byte_position_pair_count_layer(
        ledger,
        source_measurement_event_identity=source.identity,
        recording_locality_identity="measurement",
    )

    assert result.material["downstream_act_identity"] != result.material["act_occurrence_identity"]
    assert result.material["input_applicability"]["downstream_act_identity"] == (
        result.material["downstream_act_identity"]
    )
    assert result.material["input_applicability"]["downstream_act_occurrence_identity"] is None


def test_pair_validation_refuses_more_carrying_occurrences_than_total_pairs():
    ledger = _ledger("ta\n")
    source = _byte_source(ledger)
    event = record_byte_position_pair_count_layer(
        ledger,
        source_measurement_event_identity=source.identity,
        recording_locality_identity="measurement",
    )
    count = next(
        assertion
        for assertion in event.material["assertions"]
        if assertion["assertion_subject"]["representation"] == [116, 97]
    )
    count["dimensions"]["content"] = {
        "input_count": 2,
        "occurrences_carrying": 2,
        "count": 1,
    }
    count["dimensions"]["identity"] = _identity(
        result="count",
        subject=count["assertion_subject"],
        scope=count["assertion_scope"],
        content=count["dimensions"]["content"],
    )
    evidence = ledger.get(event.material["evidence_of_yield_relation_identity"])
    evidence.material["result"] = {
        name: event.material[name]
        for name in evidence.material["coordinates_of_carried_result"]
    }

    with pytest.raises(ByteMeasurementError, match="unlawful pair count"):
        assertions_of_recorded_byte_position_pair_measurement(ledger, event.identity)


def test_pair_validation_refuses_missing_count_content_without_leaking_shape_errors():
    ledger = _ledger("ta\n")
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
    count["dimensions"]["identity"] = _identity(
        result="count",
        subject=count["assertion_subject"],
        scope=count["assertion_scope"],
        content=count["dimensions"]["content"],
    )
    evidence = ledger.get(event.material["evidence_of_yield_relation_identity"])
    evidence.material["result"] = {
        name: event.material[name]
        for name in evidence.material["coordinates_of_carried_result"]
    }

    with pytest.raises(ByteMeasurementError, match="unlawful pair count"):
        assertions_of_recorded_byte_position_pair_measurement(ledger, event.identity)


def test_byte_result_reader_refuses_changed_yield_result_identity():
    ledger = _ledger("ta\n")
    event = _byte_source(ledger)
    assert assertions_of_recorded_byte_measurement(ledger, event.identity)
    evidence = ledger.get(event.material["evidence_of_yield_relation_identity"])
    evidence.material["result_identity"] = "crossed-byte-result"

    with pytest.raises(ByteMeasurementError, match="byte Measurement yield Evidence"):
        assertions_of_recorded_byte_measurement(ledger, event.identity)


def test_pair_applicability_reader_refuses_changed_yield_result_identity():
    ledger = _ledger("ta\n")
    source = _byte_source(ledger)
    pair = record_byte_position_pair_count_layer(
        ledger,
        source_measurement_event_identity=source.identity,
        recording_locality_identity="measurement",
    )
    applicability_identity = pair.material["input_applicability_event_identity"]
    applicability = ledger.get(applicability_identity)
    assert get_recorded_pair_input_applicability(ledger, applicability.identity)
    evidence = ledger.get(
        applicability.material["evidence_of_yield_relation_identity"]
    )
    evidence.material["result_identity"] = "crossed-applicability-result"

    with pytest.raises(ByteMeasurementError, match="Applicability yield Evidence"):
        get_recorded_pair_input_applicability(ledger, applicability.identity)


def test_pair_applicability_reader_revalidates_exact_input_standing(monkeypatch):
    ledger = _ledger("ta\n")
    source = _byte_source(ledger)
    pair = record_byte_position_pair_count_layer(
        ledger,
        source_measurement_event_identity=source.identity,
        recording_locality_identity="measurement",
    )

    def refuse_detached_standing(*_args, **_kwargs):
        raise ByteMeasurementError("detached input Standing")

    monkeypatch.setattr(
        "seed_runtime.byte_measurement._recorded_input_assertion_standing",
        refuse_detached_standing,
    )
    with pytest.raises(ByteMeasurementError, match="detached input Standing"):
        get_recorded_pair_input_applicability(
            ledger, pair.material["input_applicability_event_identity"]
        )


def test_pair_result_reader_refuses_changed_yield_result_identity():
    ledger = _ledger("ta\n")
    source = _byte_source(ledger)
    pair = record_byte_position_pair_count_layer(
        ledger,
        source_measurement_event_identity=source.identity,
        recording_locality_identity="measurement",
    )
    assert assertions_of_recorded_byte_position_pair_measurement(
        ledger, pair.identity
    )
    evidence = ledger.get(pair.material["evidence_of_yield_relation_identity"])
    evidence.material["result_identity"] = "crossed-pair-result"

    with pytest.raises(
        ByteMeasurementError, match="byte-position-pair yield Evidence"
    ):
        assertions_of_recorded_byte_position_pair_measurement(ledger, pair.identity)


FIDELITY_SUBJECTS = {
    "act_evidence_responsibility_boundary_occurrence_authority_scope": (
        test_responsible_act_evidence_is_observable_before_yield_and_result,
        test_exact_byte_assignment_enters_standing_and_owns_distinct_lifecycle_identities,
        test_stale_and_shaped_standing_cannot_authorize_exact_byte_act,
        test_corrupted_exact_byte_assignment_cannot_authorize_an_act,
        test_assignment_read_refuses_corrupted_unrelated_prior_standing_carrier,
        test_operator_replay_uses_exact_context_while_public_assignment_reads_reconstruct,
        test_call_local_assignment_carry_requires_the_exact_assignment_at_tip,
        test_console_exact_byte_same_call_path_does_not_use_public_standing_gate,
        test_old_unassigned_exact_byte_act_api_is_not_accepted,
        test_one_responsible_act_occurrence_cannot_yield_twice,
        test_reopened_public_result_refuses_an_act_already_consumed,
        test_yield_refuses_missing_responsible_act_evidence,
        test_seed_native_measurement_and_result_assertions_keep_distinct_responsibilities,
        test_seed_native_responsibility_is_earned_from_preserved_occurrences,
    ),
    "exact_act_occurrence": (
        test_pair_act_identity_is_not_its_occurrence_identity,
    ),
    "yield_result_occurrence_evidence": (
        test_assignment_act_and_result_survive_distinct_sqlite_restarts,
        test_call_local_result_requires_the_exact_act_at_tip,
        test_yield_resolves_the_exact_act_evidence_after_reopen,
        test_material_appended_after_act_evidence_cannot_enter_its_result,
        test_yield_refuses_a_different_occurrence_kind,
    ),
    "declared_measurement_result": (
        test_fixed_pair_identity_shape_equals_the_general_canonical_identity,
        test_two_stages_traverse_byte_counts_once,
        test_each_exact_ingest_is_counted_once_without_losing_zero_occurrence_material,
        test_each_replay_validates_each_exact_ingest_and_reads_independently,
        test_exact_bytes_supply_the_measured_subjects_without_whitespace,
        test_the_complete_declared_localities_supply_the_inputs,
        test_recurrence_exists_only_above_one,
        test_the_rule_is_mechanics_not_an_unchecked_callable,
        test_recorded_results_replay_the_complete_bounded_source_read,
        test_a_self_consistent_truncated_source_assertion_is_refused,
        test_recording_occurrence_evidence_is_validated_exactly,
        test_ingest_after_the_measurement_boundary_cannot_enter_the_measurement,
        test_a_missing_declared_locality_is_refused,
        test_ingest_must_match_its_exact_byte_coordinates,
        test_repeated_locality_coordinate_does_not_repeat_one_ingest,
        test_every_overlapping_byte_position_pair_is_measured,
        test_byte_position_pair_results_follow_first_observed_pair_positions,
        test_position_pairs_never_cross_ingest_boundaries,
        test_position_pair_measurement_remains_byte_not_character_based,
        test_recorded_pair_results_replay_the_complete_bounded_source_read,
        test_pair_validation_refuses_a_self_consistent_truncated_result_inputs,
        test_pair_validation_does_not_perform_the_pair_measurement_again,
        test_zero_measured_pairs_is_a_lawful_exact_result,
        test_pair_validation_refuses_more_carrying_occurrences_than_total_pairs,
        test_pair_validation_refuses_missing_count_content_without_leaking_shape_errors,
        test_byte_result_reader_refuses_changed_yield_result_identity,
        test_pair_result_reader_refuses_changed_yield_result_identity,
    ),
    "measurement_result_distinctions": (
        test_count_and_recurrence_are_distinct_results,
        test_pair_count_and_recurrence_are_separate_results,
    ),
    "applicability_determination": (
        test_pair_validation_refuses_unsupported_input_applicability,
        test_applicability_identity_is_bound_to_one_exact_downstream_act,
        test_pair_applicability_reads_exact_result_standing_instead_of_scalar,
        test_pair_applicability_reader_refuses_changed_yield_result_identity,
        test_pair_applicability_reader_revalidates_exact_input_standing,
    ),
    "one_exact_movement_assertion": (
        test_locality_movement_assignment_is_earned_from_the_exact_source,
    ),
    "representation_source_coordinates": (
        test_pair_validation_requires_one_exact_ordered_representation,
    ),
}
