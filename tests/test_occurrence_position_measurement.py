from copy import deepcopy

import pytest

import seed_runtime.occurrence_position_measurement as position_measurement
from seed_runtime.events import CORRUPTED, EventLedger, SQLiteEventLedger
from seed_runtime.occurrence_position_measurement import (
    OCCURRENCE_POSITION_ACT_EVIDENCE_KIND,
    OCCURRENCE_POSITION_MEASUREMENT_RULE,
    OCCURRENCE_POSITION_RECORDED_KIND,
    OCCURRENCE_POSITION_RESULT_COORDINATES,
    MEASURED_ASSERTION_RESPONSIBILITY,
    OccurrencePositionFinding,
    get_recorded_occurrence_position_measurement,
    measure_occurrence_position,
    record_occurrence_position_measurement_responsible_act_evidence,
    record_occurrence_position_measurement_result,
)
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


def recorded_road():
    ledger, occurrences, boundary = occurrence_road()
    finding = measure_occurrence_position(
        ledger,
        source_locality_identity="a",
        through=boundary,
    )
    act_evidence = record_occurrence_position_measurement_responsible_act_evidence(
        ledger,
        recording_locality_identity="measurement",
        finding=finding,
    )
    recorded = record_occurrence_position_measurement_result(
        ledger,
        finding=finding,
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
        record_occurrence_position_measurement_responsible_act_evidence(
            ledger,
            recording_locality_identity="measurement",
            finding=reversed_finding,
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
        record_occurrence_position_measurement_responsible_act_evidence(
            ledger,
            recording_locality_identity="measurement",
            finding=subclass_finding,
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
        record_occurrence_position_measurement_responsible_act_evidence(
            ledger,
            recording_locality_identity="measurement",
            finding=finding,
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

    act_evidence = record_occurrence_position_measurement_responsible_act_evidence(
        ledger,
        recording_locality_identity="measurement",
        finding=finding,
    )
    recorded = record_occurrence_position_measurement_result(
        ledger,
        finding=finding,
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

    act_evidence = record_occurrence_position_measurement_responsible_act_evidence(
        ledger,
        recording_locality_identity="measurement",
        finding=finding,
    )

    assert [
        event.kind for event in ledger.list_locality("measurement")
    ] == [OCCURRENCE_POSITION_ACT_EVIDENCE_KIND]
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
        finding=finding,
        responsible_act_evidence_event_identity=act_evidence.identity,
    )

    events = ledger.list_locality("measurement")
    assert [event.kind for event in events] == [
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
            finding=finding,
            responsible_act_evidence_event_identity=act_evidence_identity,
        )

    assert ledger.append_boundary() == before


def test_result_refuses_substituted_finding_without_appending_yield():
    ledger, _occurrences, boundary = occurrence_road()
    finding = measure_occurrence_position(
        ledger,
        source_locality_identity="a",
        through=boundary,
    )
    other_finding = measure_occurrence_position(
        ledger,
        source_locality_identity="b",
        through=boundary,
    )
    act_evidence = record_occurrence_position_measurement_responsible_act_evidence(
        ledger,
        recording_locality_identity="measurement",
        finding=finding,
    )
    before = ledger.append_boundary()

    with pytest.raises(ValueError, match="exact intact Act Evidence"):
        record_occurrence_position_measurement_result(
            ledger,
            finding=other_finding,
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
    act_evidence = record_occurrence_position_measurement_responsible_act_evidence(
        ledger,
        recording_locality_identity="measurement",
        finding=finding,
    )

    with pytest.raises(ValueError, match="exact intact Act Evidence"):
        record_occurrence_position_measurement_result(
            ledger,
            finding=finding,
            responsible_act_evidence_event_identity=wrong_kind.identity,
        )

    ledger.corrupted.add(act_evidence.identity)
    with pytest.raises(ValueError, match="exact intact Act Evidence"):
        record_occurrence_position_measurement_result(
            ledger,
            finding=finding,
            responsible_act_evidence_event_identity=act_evidence.identity,
        )


def test_one_measurement_act_cannot_yield_two_results():
    ledger, _occurrences, boundary = occurrence_road()
    finding = measure_occurrence_position(
        ledger,
        source_locality_identity="a",
        through=boundary,
    )
    act_evidence = record_occurrence_position_measurement_responsible_act_evidence(
        ledger,
        recording_locality_identity="measurement",
        finding=finding,
    )
    record_occurrence_position_measurement_result(
        ledger,
        finding=finding,
        responsible_act_evidence_event_identity=act_evidence.identity,
    )
    before = ledger.append_boundary()

    with pytest.raises(ValueError, match="already carries a Yield"):
        record_occurrence_position_measurement_result(
            ledger,
            finding=finding,
            responsible_act_evidence_event_identity=act_evidence.identity,
        )

    assert ledger.append_boundary() == before


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
    _ledger, occurrences, boundary, _finding, recorded = recorded_road()

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
    assert all(
        item["assertion_scope"] == {"source_localities": ["a"]}
        and item["result"] == "position"
        and item["assertion_subject"]["measurement_rule"]
        == OCCURRENCE_POSITION_MEASUREMENT_RULE
        for item in assertions
    )


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
    act_evidence = record_occurrence_position_measurement_responsible_act_evidence(
        ledger,
        recording_locality_identity="measurement",
        finding=finding,
    )
    recorded = record_occurrence_position_measurement_result(
        ledger,
        finding=finding,
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
    act_evidence = record_occurrence_position_measurement_responsible_act_evidence(
        ledger,
        recording_locality_identity="measurement",
        finding=finding,
    )
    recorded = record_occurrence_position_measurement_result(
        ledger,
        finding=finding,
        responsible_act_evidence_event_identity=act_evidence.identity,
    )
    carried = {
        "occurrence_position_measurement_act": recorded.material[
            "downstream_act_identity"
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


FIDELITY_SUBJECTS = {
    "act_evidence_responsibility_boundary_occurrence_authority_scope": (
        test_corrupted_source_cannot_enter_act_evidence_after_measurement,
        test_act_evidence_is_observed_before_yield_without_reconstructing_finding,
        test_result_refuses_arbitrary_act_evidence_identity_without_appending,
        test_result_refuses_wrong_kind_and_corrupted_act_evidence,
    ),
    "yield_result_occurrence_evidence": (
        test_recorded_position_measurement_has_exact_act_and_evidence_of_yield_relation,
        test_result_refuses_substituted_finding_without_appending_yield,
        test_one_measurement_act_cannot_yield_two_results,
        test_corrupted_input_act_or_evidence_of_yield_relation_is_refused,
        test_durable_locality_positions_read_through_their_exact_yield,
    ),
    "declared_measurement_result": (
        test_a_later_occurrence_does_not_revise_the_bounded_positions,
        test_supplied_reversal_cannot_replace_the_ledger_measurement,
        test_subclass_finding_cannot_replace_the_exact_measurement_type,
        test_recording_and_reading_do_not_reconstruct_complete_result_material,
        test_position_finding_establishes_no_stronger_relation,
        test_changed_position_is_not_certified_by_unchanged_evidence,
        test_result_carries_one_ordered_assertion_per_exact_position,
        test_missing_reordered_duplicated_or_substituted_assertions_are_refused,
        test_wrong_result_boundary_coordinates_are_refused,
        test_wrong_boundary_is_refused_without_reconstructing_positions,
        test_durable_position_identities_are_not_reissued_after_reopen,
    ),
    "locality_relation_coordinates": (
        test_exact_locality_occurrences_receive_exact_positions,
        test_another_locality_does_not_enter_the_position_measurement,
    ),
}
