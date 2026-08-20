from copy import deepcopy

import pytest

import seed_runtime.occurrence_position_measurement as position_measurement
from seed_runtime.events import CORRUPTED, EventLedger, SQLiteEventLedger
from seed_runtime.occurrence_position_measurement import (
    OCCURRENCE_POSITION_ACT_EVIDENCE_KIND,
    OCCURRENCE_POSITION_MEASUREMENT_RULE,
    OCCURRENCE_POSITION_RECORDED_KIND,
    OCCURRENCE_POSITION_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND,
    OCCURRENCE_POSITION_RESULT_COORDINATES,
    MEASURED_ASSERTION_RESPONSIBILITY,
    OccurrencePositionFinding,
    get_occurrence_position_measurement_responsibility_assignment,
    get_recorded_occurrence_position_measurement,
    measure_occurrence_position,
    record_occurrence_position_measurement_responsibility_assignment,
    record_occurrence_position_measurement_responsible_act_evidence,
    record_occurrence_position_measurement_result,
)
from seed_runtime.operator_locality_standing import read_operator_locality_standing
from seed_runtime.evidence_of_yield_relation import (
    RECORDED_EVIDENCE_OF_YIELD_RELATION_KIND,
    read_requirements_of_yield_relation,
)


class IntegrityLedger(EventLedger):
    def __init__(self):
        super().__init__()
        self.corrupted = set()

    def integrity_of(self, event_identity):
        if event_identity in self.corrupted:
            return CORRUPTED
        return super().integrity_of(event_identity)


class StringSubclass(str):
    pass


class OccurrencePositionFindingSubclass(OccurrencePositionFinding):
    pass


def occurrence_road():
    ledger = IntegrityLedger()
    first = ledger.append("test.occurrence", {"material": "a"}, locality_identity="a")
    ledger.append("test.occurrence", {"material": "x"}, locality_identity="b")
    second = ledger.append("test.occurrence", {"material": "b"}, locality_identity="a")
    third = ledger.append("test.occurrence", {"material": "c"}, locality_identity="a")
    boundary = ledger.append_boundary()
    return ledger, (first, second, third), boundary


def _standing(ledger, locality="measurement"):
    return read_operator_locality_standing(
        ledger, locality_identity=locality
    )


def _record_assignment(ledger, finding, locality="measurement"):
    return record_occurrence_position_measurement_responsibility_assignment(
        ledger,
        recording_locality_identity=locality,
        finding=finding,
        locality_standing=_standing(ledger, locality),
    )


def _record_act(ledger, finding, locality="measurement"):
    assignment = _record_assignment(ledger, finding, locality)
    act = record_occurrence_position_measurement_responsible_act_evidence(
        ledger,
        responsibility_assignment_event_identity=assignment.identity,
        responsibility_assignment_standing=_standing(ledger, locality),
    )
    return assignment, act


def recorded_road():
    ledger, occurrences, boundary = occurrence_road()
    finding = measure_occurrence_position(
        ledger,
        source_locality_identity="a",
        through=boundary,
    )
    _assignment, act_evidence = _record_act(ledger, finding)
    recorded = record_occurrence_position_measurement_result(
        ledger,
        responsible_act_evidence_event_identity=act_evidence.identity,
    )
    return ledger, occurrences, boundary, finding, recorded


def test_exact_locality_occurrences_receive_exact_positions():
    ledger, occurrences, boundary = occurrence_road()

    finding = measure_occurrence_position(
        ledger,
        source_locality_identity="a",
        through=boundary,
    )

    assert finding.occurrences == tuple(
        (event.identity, position)
        for position, event in enumerate(occurrences)
    )
    assert finding.source_locality_identity == "a"
    assert finding.completeness_boundary == boundary


def test_another_locality_does_not_enter_the_position_measurement():
    ledger, occurrences, boundary = occurrence_road()

    finding = measure_occurrence_position(
        ledger,
        source_locality_identity="a",
        through=boundary,
    )

    assert [identity for identity, _position in finding.occurrences] == [
        event.identity for event in occurrences
    ]


def test_a_later_occurrence_does_not_revise_the_bounded_positions():
    ledger, _occurrences, boundary = occurrence_road()
    before = measure_occurrence_position(
        ledger,
        source_locality_identity="a",
        through=boundary,
    )

    ledger.append("test.occurrence", {"material": "later"}, locality_identity="a")

    assert measure_occurrence_position(
        ledger,
        source_locality_identity="a",
        through=boundary,
    ) == before
    assert len(
        measure_occurrence_position(
            ledger,
            source_locality_identity="a",
        ).occurrences
    ) == len(before.occurrences) + 1


def test_supplied_reversal_cannot_replace_the_ledger_measurement():
    ledger, occurrences, boundary = occurrence_road()
    reversed_finding = OccurrencePositionFinding(
        source_locality_identity="a",
        completeness_boundary=boundary,
        occurrences=tuple(
            (event.identity, position)
            for position, event in enumerate(reversed(occurrences))
        ),
    )

    with pytest.raises(
        ValueError,
        match="differs from the exact boundary",
    ):
        record_occurrence_position_measurement_responsibility_assignment(
            ledger,
            recording_locality_identity="measurement",
            finding=reversed_finding,
            locality_standing=_standing(ledger),
        )


def test_subclass_finding_cannot_replace_the_exact_measurement_type():
    ledger, occurrences, boundary = occurrence_road()
    subclass_finding = OccurrencePositionFindingSubclass(
        source_locality_identity="a",
        completeness_boundary=boundary,
        occurrences=tuple(
            (event.identity, position)
            for position, event in enumerate(occurrences)
        ),
    )

    with pytest.raises(TypeError, match="one exact finding"):
        record_occurrence_position_measurement_responsibility_assignment(
            ledger,
            recording_locality_identity="measurement",
            finding=subclass_finding,
            locality_standing=_standing(ledger),
        )


def test_corrupted_source_cannot_enter_act_evidence_after_measurement():
    ledger, occurrences, boundary = occurrence_road()
    finding = measure_occurrence_position(
        ledger,
        source_locality_identity="a",
        through=boundary,
    )
    ledger.corrupted.add(occurrences[1].identity)

    with pytest.raises(ValueError, match="requires intact occurrences"):
        record_occurrence_position_measurement_responsibility_assignment(
            ledger,
            recording_locality_identity="measurement",
            finding=finding,
            locality_standing=_standing(ledger),
        )


def test_recorded_position_measurement_has_exact_act_and_evidence_of_yield_relation():
    ledger, _occurrences, _boundary, finding, recorded = recorded_road()
    act_evidence = ledger.get(recorded.material["responsible_act_evidence_identity"])
    evidence_of_yield_relation = ledger.get(recorded.material["evidence_of_yield_relation_identity"])

    assert recorded.kind == OCCURRENCE_POSITION_RECORDED_KIND
    assert act_evidence.kind == OCCURRENCE_POSITION_ACT_EVIDENCE_KIND
    assert act_evidence.material["act_occurrence_identity"] == recorded.material[
        "act_occurrence_identity"
    ]
    assert act_evidence.material["responsibility_assignment_evidence"] == (
        recorded.material["responsibility_assignment_evidence"]
    )
    assert act_evidence.material["authority"] == "bounded repository authority"
    assert read_requirements_of_yield_relation(
        ledger,
        recorded_result_event_identity=recorded.identity,
        evidence_of_yield_relation_event_identity=evidence_of_yield_relation.identity,
        responsible_act_evidence_event_identity=act_evidence.identity,
    ) == {
        "exact_relation": True,
        "occurrence_witness": True,
        "intact_evidence": True,
    }
    assert get_recorded_occurrence_position_measurement(
        ledger,
        recorded.identity,
    ) == finding


def test_assignment_act_yield_and_result_keep_distinct_exact_identities():
    ledger, _occurrences, _boundary, _finding, recorded = recorded_road()
    reference = recorded.material["responsibility_assignment_reference"]
    assignment = get_occurrence_position_measurement_responsibility_assignment(
        ledger, reference["recorded_occurrence_identity"]
    )
    act_evidence = ledger.get(recorded.material["responsible_act_evidence_identity"])
    yielded = ledger.get(recorded.material["evidence_of_yield_relation_identity"])

    assert assignment.kind == (
        OCCURRENCE_POSITION_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND
    )
    assert reference == {
        "recorded_occurrence_identity": assignment.identity,
        "assignment_identity": assignment.material["assignment_identity"],
        "assignment_subject_identity": assignment.material[
            "assignment_subject_identity"
        ],
    }
    assert "standing" not in recorded.material[
        "responsibility_assignment_evidence"
    ]
    assert assignment.identity in _standing(ledger)[
        "responsibility_assignment_occurrences"
    ]
    assert len(
        {
            assignment.material["assignment_identity"],
            assignment.material["assignment_subject_identity"],
            assignment.material["measurement_act_identity"],
            assignment.material["act_occurrence_identity"],
            assignment.material["measurement_result_identity"],
            assignment.identity,
            act_evidence.identity,
            yielded.identity,
            recorded.identity,
        }
    ) == 9


def test_act_requires_current_standing_that_carries_its_assignment():
    ledger, _occurrences, boundary = occurrence_road()
    finding = measure_occurrence_position(
        ledger, source_locality_identity="a", through=boundary
    )
    before_assignment = _standing(ledger)
    assignment = record_occurrence_position_measurement_responsibility_assignment(
        ledger,
        recording_locality_identity="measurement",
        finding=finding,
        locality_standing=before_assignment,
    )
    before = ledger.append_boundary()

    with pytest.raises(ValueError, match="exact current Locality Standing"):
        record_occurrence_position_measurement_responsible_act_evidence(
            ledger,
            responsibility_assignment_event_identity=assignment.identity,
            responsibility_assignment_standing=before_assignment,
        )

    assert ledger.append_boundary() == before
    assert record_occurrence_position_measurement_responsible_act_evidence(
        ledger,
        responsibility_assignment_event_identity=assignment.identity,
        responsibility_assignment_standing=_standing(ledger),
    ).kind == OCCURRENCE_POSITION_ACT_EVIDENCE_KIND


def test_assignment_refuses_stale_current_standing_without_appending():
    ledger, _occurrences, boundary = occurrence_road()
    finding = measure_occurrence_position(
        ledger, source_locality_identity="a", through=boundary
    )
    stale = _standing(ledger)
    _record_assignment(ledger, finding)
    before = ledger.append_boundary()

    with pytest.raises(ValueError, match="exact current Locality Standing"):
        record_occurrence_position_measurement_responsibility_assignment(
            ledger,
            recording_locality_identity="measurement",
            finding=finding,
            locality_standing=stale,
        )

    assert ledger.append_boundary() == before


def test_one_assignment_cannot_record_two_act_occurrences():
    ledger, _occurrences, boundary = occurrence_road()
    finding = measure_occurrence_position(
        ledger, source_locality_identity="a", through=boundary
    )
    assignment, _act = _record_act(ledger, finding)
    before = ledger.append_boundary()

    with pytest.raises(ValueError, match="already carries an Act"):
        record_occurrence_position_measurement_responsible_act_evidence(
            ledger,
            responsibility_assignment_event_identity=assignment.identity,
            responsibility_assignment_standing=_standing(ledger),
        )

    assert ledger.append_boundary() == before


def test_recording_and_reading_do_not_reconstruct_complete_result_material(
    monkeypatch,
):
    ledger, _occurrences, boundary = occurrence_road()
    finding = measure_occurrence_position(
        ledger,
        source_locality_identity="a",
        through=boundary,
    )
    participation = position_measurement._occurrence_position_participation
    position_assertions = position_measurement._position_assertions
    participation_calls = []
    assertion_calls = []

    def counted_participation(*args, **kwargs):
        participation_calls.append(None)
        return participation(*args, **kwargs)

    def counted_position_assertions(*args, **kwargs):
        assertion_calls.append(None)
        return position_assertions(*args, **kwargs)

    monkeypatch.setattr(
        position_measurement,
        "_occurrence_position_participation",
        counted_participation,
    )
    monkeypatch.setattr(
        position_measurement,
        "_position_assertions",
        counted_position_assertions,
    )

    assignment, act_evidence = _record_act(ledger, finding)
    recorded = record_occurrence_position_measurement_result(
        ledger,
        responsible_act_evidence_event_identity=act_evidence.identity,
    )
    yielded = ledger.get(recorded.material["evidence_of_yield_relation_identity"])
    assert get_recorded_occurrence_position_measurement(
        ledger,
        recorded.identity,
    ) == finding

    assert len(participation_calls) == 3
    assert len(assertion_calls) == 2
    assert act_evidence.material["participation"]
    assert "participation" not in recorded.material
    assert yielded.material["result"]["assertions"] == recorded.material[
        "assertions"
    ]
    assert yielded.material["result"]["assertions"] is not recorded.material[
        "assertions"
    ]


def test_act_evidence_is_observed_before_yield_without_reconstructing_finding(
    monkeypatch,
):
    ledger, _occurrences, boundary = occurrence_road()
    finding = measure_occurrence_position(
        ledger,
        source_locality_identity="a",
        through=boundary,
    )
    measurements = []

    def counted_measure(*args, **kwargs):
        measurements.append((args, kwargs))
        raise AssertionError("an exact finding must not be reconstructed")

    monkeypatch.setattr(
        position_measurement,
        "measure_occurrence_position",
        counted_measure,
    )

    assignment, act_evidence = _record_act(ledger, finding)

    assert [
        event.kind for event in ledger.list_locality("measurement")
    ] == [
        OCCURRENCE_POSITION_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND,
        OCCURRENCE_POSITION_ACT_EVIDENCE_KIND,
    ]
    assert "result_identity" not in act_evidence.material
    assert "occurrences" not in act_evidence.material
    assert all(
        "position" not in item
        for item in act_evidence.material["participation"]
    )
    observed = ledger.append(
        "test.act_evidence_observed",
        {"act_evidence_identity": act_evidence.identity},
        locality_identity="measurement",
    )

    recorded = record_occurrence_position_measurement_result(
        ledger,
        responsible_act_evidence_event_identity=act_evidence.identity,
    )

    events = ledger.list_locality("measurement")
    assert [event.kind for event in events] == [
        OCCURRENCE_POSITION_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND,
        OCCURRENCE_POSITION_ACT_EVIDENCE_KIND,
        observed.kind,
        RECORDED_EVIDENCE_OF_YIELD_RELATION_KIND,
        OCCURRENCE_POSITION_RECORDED_KIND,
    ]
    assert recorded.material["responsible_act_evidence_identity"] == (
        act_evidence.identity
    )
    assert get_recorded_occurrence_position_measurement(
        ledger,
        recorded.identity,
    ) == finding
    assert measurements == []


@pytest.mark.parametrize(
    "act_evidence_identity",
    (None, "", "absent_act_evidence", StringSubclass("absent_act_evidence")),
)
def test_result_refuses_arbitrary_act_evidence_identity_without_appending(
    act_evidence_identity,
):
    ledger, _occurrences, boundary = occurrence_road()
    finding = measure_occurrence_position(
        ledger,
        source_locality_identity="a",
        through=boundary,
    )
    before = ledger.append_boundary()

    with pytest.raises(ValueError, match="Act Evidence"):
        record_occurrence_position_measurement_result(
            ledger,
            responsible_act_evidence_event_identity=act_evidence_identity,
        )

    assert ledger.append_boundary() == before


def test_result_refuses_substituted_assignment_without_appending_yield():
    ledger, _occurrences, boundary = occurrence_road()
    finding = measure_occurrence_position(
        ledger,
        source_locality_identity="a",
        through=boundary,
    )
    _assignment, act_evidence = _record_act(ledger, finding)
    act_evidence.material["responsibility_assignment_reference"][
        "recorded_occurrence_identity"
    ] = "substituted-assignment"
    before = ledger.append_boundary()

    with pytest.raises(ValueError, match="exact intact Act Evidence"):
        record_occurrence_position_measurement_result(
            ledger,
            responsible_act_evidence_event_identity=act_evidence.identity,
        )

    assert ledger.append_boundary() == before


def test_result_refuses_wrong_kind_and_corrupted_act_evidence():
    ledger, _occurrences, boundary = occurrence_road()
    finding = measure_occurrence_position(
        ledger,
        source_locality_identity="a",
        through=boundary,
    )
    wrong_kind = ledger.append(
        "test.not_act_evidence",
        {},
        locality_identity="measurement",
    )
    _assignment, act_evidence = _record_act(ledger, finding)

    with pytest.raises(ValueError, match="exact intact Act Evidence"):
        record_occurrence_position_measurement_result(
            ledger,
            responsible_act_evidence_event_identity=wrong_kind.identity,
        )

    ledger.corrupted.add(act_evidence.identity)
    with pytest.raises(ValueError, match="exact intact Act Evidence"):
        record_occurrence_position_measurement_result(
            ledger,
            responsible_act_evidence_event_identity=act_evidence.identity,
        )


def test_one_measurement_act_cannot_yield_two_results():
    ledger, _occurrences, boundary = occurrence_road()
    finding = measure_occurrence_position(
        ledger,
        source_locality_identity="a",
        through=boundary,
    )
    _assignment, act_evidence = _record_act(ledger, finding)
    record_occurrence_position_measurement_result(
        ledger,
        responsible_act_evidence_event_identity=act_evidence.identity,
    )
    before = ledger.append_boundary()

    with pytest.raises(ValueError, match="already carries a Yield"):
        record_occurrence_position_measurement_result(
            ledger,
            responsible_act_evidence_event_identity=act_evidence.identity,
        )

    assert ledger.append_boundary() == before


def test_carried_result_skips_history_scan_only_at_its_exact_act_tip(monkeypatch):
    ledger, _occurrences, boundary = occurrence_road()
    finding = measure_occurrence_position(
        ledger,
        source_locality_identity="a",
        through=boundary,
    )
    assignment, act_evidence = _record_act(ledger, finding, locality="a")

    def history_scan_is_not_available(*_args, **_kwargs):
        raise AssertionError(
            "same-call result scanned prior Yield or result occurrences"
        )

    monkeypatch.setattr(ledger, "iter_locality_kind", history_scan_is_not_available)
    recorded = (
        position_measurement._record_occurrence_position_measurement_result_from_carried_act_evidence(
            ledger,
            responsible_act_evidence=act_evidence,
            responsibility_assignment=assignment,
            finding=finding,
        )
    )
    assert recorded.kind == OCCURRENCE_POSITION_RECORDED_KIND

    with pytest.raises(ValueError, match="exact intact Act Evidence"):
        (
            position_measurement._record_occurrence_position_measurement_result_from_carried_act_evidence(
                ledger,
                responsible_act_evidence=act_evidence,
                responsibility_assignment=assignment,
                finding=finding,
            )
        )


def test_position_finding_establishes_no_stronger_relation():
    _ledger, _occurrences, _boundary, _finding, recorded = recorded_road()

    assert "first_subject" not in recorded.material
    assert "second_subject" not in recorded.material
    assert "causation" not in recorded.material
    assert all(
        assertion["limits"]
        == [
            "exact occurrence position bounded by source Locality and "
            "completeness boundary"
        ]
        for assertion in recorded.material["assertions"]
    )


def test_changed_position_is_not_certified_by_unchanged_evidence():
    ledger, _occurrences, _boundary, _finding, recorded = recorded_road()
    recorded.material["assertions"][0]["dimensions"]["content"]["position"] = 1

    with pytest.raises(ValueError):
        get_recorded_occurrence_position_measurement(ledger, recorded.identity)


def test_result_carries_one_ordered_assertion_per_exact_position():
    ledger, occurrences, boundary, _finding, recorded = recorded_road()

    assert set(recorded.material) == OCCURRENCE_POSITION_RESULT_COORDINATES | {
        "responsible_act_evidence_identity",
        "evidence_of_yield_relation_identity",
    }
    assert recorded.material["measurement_rule"] == (
        OCCURRENCE_POSITION_MEASUREMENT_RULE
    )
    assert recorded.material["source_localities"] == ["a"]
    assert recorded.material["completeness_boundary"] == {
        "identity": boundary.identity
    }
    assertions = recorded.material["assertions"]
    assert len(assertions) == len(occurrences)
    assert [
        (
            item["assertion_subject"]["occurrence_identity"],
            item["dimensions"]["content"]["position"],
        )
        for item in assertions
    ] == [(event.identity, position) for position, event in enumerate(occurrences)]
    assert len({item["dimensions"]["identity"] for item in assertions}) == len(
        assertions
    )
    assert {
        item["dimensions"]["responsibility"] for item in assertions
    } == {MEASURED_ASSERTION_RESPONSIBILITY}
    assert all("standing" not in item["dimensions"] for item in assertions)
    assert _standing(ledger)["measurement_occurrences"][recorded.identity] == {
        "recorded_occurrence_identity": recorded.identity,
        "result_identity": recorded.material["result_identity"],
        "act_occurrence_identity": recorded.material["act_occurrence_identity"],
        "responsible_act_evidence_identity": recorded.material[
            "responsible_act_evidence_identity"
        ],
        "evidence_of_yield_relation_identity": recorded.material[
            "evidence_of_yield_relation_identity"
        ],
    }
    assert all(
        item["assertion_scope"] == {"source_localities": ["a"]}
        and item["result"] == "position"
        and item["assertion_subject"]["measurement_rule"]
        == OCCURRENCE_POSITION_MEASUREMENT_RULE
        for item in assertions
    )


def test_measured_scalar_cannot_impersonate_occurrence_position_standing():
    ledger, _occurrences, _boundary, _finding, recorded = recorded_road()
    recorded.material["assertions"][0]["dimensions"]["standing"] = "measured"

    with pytest.raises(ValueError, match="malformed Assertions"):
        get_recorded_occurrence_position_measurement(ledger, recorded.identity)


@pytest.mark.parametrize(
    "mutate",
    (
        lambda assertions: assertions.pop(1),
        lambda assertions: assertions.reverse(),
        lambda assertions: assertions.__setitem__(1, deepcopy(assertions[0])),
        lambda assertions: assertions[1]["assertion_subject"].__setitem__(
            "occurrence_identity", "substituted-occurrence"
        ),
        lambda assertions: assertions[1]["dimensions"]["content"].__setitem__(
            "position", 0
        ),
    ),
)
def test_missing_reordered_duplicated_or_substituted_assertions_are_refused(mutate):
    ledger, _occurrences, _boundary, _finding, recorded = recorded_road()
    mutate(recorded.material["assertions"])

    with pytest.raises(ValueError, match="malformed Assertions"):
        get_recorded_occurrence_position_measurement(ledger, recorded.identity)


@pytest.mark.parametrize(
    "coordinate, value",
    (
        ("measurement_rule", "another Measurement rule"),
        ("source_localities", ["b"]),
        ("completeness_boundary", {"identity": "another-boundary"}),
    ),
)
def test_wrong_result_boundary_coordinates_are_refused(coordinate, value):
    ledger, _occurrences, _boundary, _finding, recorded = recorded_road()
    recorded.material[coordinate] = value

    with pytest.raises(ValueError):
        get_recorded_occurrence_position_measurement(ledger, recorded.identity)


def test_corrupted_input_act_or_evidence_of_yield_relation_is_refused():
    for coordinate in (
        "input",
        "responsible_act_evidence_identity",
        "evidence_of_yield_relation_identity",
    ):
        ledger, occurrences, _boundary, _finding, recorded = recorded_road()
        corrupted_identity = (
            occurrences[0].identity
            if coordinate == "input"
            else recorded.material[coordinate]
        )
        ledger.corrupted.add(corrupted_identity)

        with pytest.raises(ValueError):
            get_recorded_occurrence_position_measurement(ledger, recorded.identity)


def test_wrong_boundary_is_refused_without_reconstructing_positions():
    ledger, _occurrences, _boundary, _finding, recorded = recorded_road()
    changed = deepcopy(recorded.material["completeness_boundary"])
    changed["identity"] = "not-a-boundary"
    recorded.material["completeness_boundary"] = changed

    with pytest.raises(ValueError):
        get_recorded_occurrence_position_measurement(ledger, recorded.identity)


def test_durable_locality_positions_read_through_their_exact_yield(tmp_path):
    ledger = SQLiteEventLedger(tmp_path / "occurrence-position.sqlite")
    first = ledger.append("test.occurrence", {"material": "a"}, locality_identity="a")
    ledger.append("test.occurrence", {"material": "x"}, locality_identity="b")
    second = ledger.append("test.occurrence", {"material": "b"}, locality_identity="a")
    finding = measure_occurrence_position(
        ledger,
        source_locality_identity="a",
    )
    _assignment, act_evidence = _record_act(ledger, finding)
    recorded = record_occurrence_position_measurement_result(
        ledger,
        responsible_act_evidence_event_identity=act_evidence.identity,
    )

    assert finding.occurrences == (
        (first.identity, 0),
        (second.identity, 1),
    )
    assert get_recorded_occurrence_position_measurement(
        ledger,
        recorded.identity,
    ) == finding


def test_durable_position_identities_are_not_reissued_after_reopen(tmp_path):
    from seed_runtime.identities import _next_values, new_identity

    path = tmp_path / "occurrence-position.sqlite"
    ledger = SQLiteEventLedger(path)
    ledger.append("test.occurrence", {"material": "a"}, locality_identity="a")
    finding = measure_occurrence_position(
        ledger,
        source_locality_identity="a",
    )
    assignment, act_evidence = _record_act(ledger, finding)
    recorded = record_occurrence_position_measurement_result(
        ledger,
        responsible_act_evidence_event_identity=act_evidence.identity,
    )
    carried = {
        "occurrence_position_measurement_assignment": assignment.material[
            "assignment_identity"
        ],
        "occurrence_position_measurement_assignment_subject": assignment.material[
            "assignment_subject_identity"
        ],
        "occurrence_position_measurement_act": recorded.material[
            "addressed_act_identity"
        ],
        "occurrence_position_measurement_occurrence": recorded.material[
            "act_occurrence_identity"
        ],
        "occurrence_position_measurement_result": recorded.material[
            "result_identity"
        ],
    }
    ledger.close()

    _next_values.clear()
    reopened = SQLiteEventLedger(path)
    try:
        for prefix, identity in carried.items():
            prior_number = int(identity.rsplit("_", 1)[1])
            assert new_identity(prefix) == f"{prefix}_{prior_number + 1:06d}"
    finally:
        reopened.close()


def test_assignment_act_and_result_survive_separate_restarts(tmp_path):
    path = tmp_path / "occurrence-position-restarts.sqlite"
    ledger = SQLiteEventLedger(path)
    first = ledger.append(
        "test.occurrence", {"material": "a"}, locality_identity="a"
    )
    finding = measure_occurrence_position(
        ledger, source_locality_identity="a"
    )
    assignment = _record_assignment(ledger, finding)
    assignment_identity = assignment.identity
    ledger.close()

    ledger = SQLiteEventLedger(path)
    assignment = get_occurrence_position_measurement_responsibility_assignment(
        ledger, assignment_identity
    )
    act_evidence = record_occurrence_position_measurement_responsible_act_evidence(
        ledger,
        responsibility_assignment_event_identity=assignment.identity,
        responsibility_assignment_standing=_standing(ledger),
    )
    act_identity = act_evidence.identity
    ledger.close()

    ledger = SQLiteEventLedger(path)
    try:
        recorded = record_occurrence_position_measurement_result(
            ledger,
            responsible_act_evidence_event_identity=act_identity,
        )
        assert get_recorded_occurrence_position_measurement(
            ledger, recorded.identity
        ).occurrences == ((first.identity, 0),)
    finally:
        ledger.close()


def test_reopened_public_result_refuses_a_second_yield(tmp_path):
    path = tmp_path / "occurrence-position-duplicate.sqlite"
    ledger = SQLiteEventLedger(path)
    ledger.append("test.occurrence", {"material": "a"}, locality_identity="a")
    finding = measure_occurrence_position(ledger, source_locality_identity="a")
    _assignment, act_evidence = _record_act(ledger, finding)
    record_occurrence_position_measurement_result(
        ledger,
        responsible_act_evidence_event_identity=act_evidence.identity,
    )
    act_identity = act_evidence.identity
    ledger.close()

    reopened = SQLiteEventLedger(path)
    try:
        before = reopened.append_boundary()
        with pytest.raises(ValueError, match="already carries a Yield"):
            record_occurrence_position_measurement_result(
                reopened,
                responsible_act_evidence_event_identity=act_identity,
            )
        assert reopened.append_boundary() == before
    finally:
        reopened.close()


FIDELITY_DISTINCTIONS = {
    ("book_coordinates", "01.Source.D", "result"): (
        test_a_later_occurrence_does_not_revise_the_bounded_positions,
        test_supplied_reversal_cannot_replace_the_ledger_measurement,
        test_subclass_finding_cannot_replace_the_exact_measurement_type,
        test_recording_and_reading_do_not_reconstruct_complete_result_material,
        test_position_finding_establishes_no_stronger_relation,
        test_changed_position_is_not_certified_by_unchanged_evidence,
        test_missing_reordered_duplicated_or_substituted_assertions_are_refused,
        test_wrong_result_boundary_coordinates_are_refused,
        test_wrong_boundary_is_refused_without_reconstructing_positions,
        test_durable_position_identities_are_not_reissued_after_reopen,
    ),
}
