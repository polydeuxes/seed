from copy import deepcopy

import pytest

from seed_runtime.events import CORRUPTED, EventLedger, SQLiteEventLedger
from seed_runtime.occurrence_position_measurement import (
    OCCURRENCE_POSITION_ACT_EVIDENCE_KIND,
    OCCURRENCE_POSITION_RECORDED_KIND,
    OccurrencePositionFinding,
    get_recorded_occurrence_position_measurement,
    measure_occurrence_position,
    record_occurrence_position_measurement,
)
from seed_runtime.yield_evidence import read_yield_relation_requirements


class IntegrityLedger(EventLedger):
    def __init__(self):
        super().__init__()
        self.corrupted = set()

    def integrity_of(self, event_identity):
        if event_identity in self.corrupted:
            return CORRUPTED
        return super().integrity_of(event_identity)


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
    recorded = record_occurrence_position_measurement(
        ledger,
        recording_locality_identity="measurement",
        finding=finding,
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
        record_occurrence_position_measurement(
            ledger,
            recording_locality_identity="measurement",
            finding=reversed_finding,
        )


def test_recorded_position_measurement_has_exact_act_and_yield_evidence():
    ledger, _occurrences, _boundary, finding, recorded = recorded_road()
    act_evidence = ledger.get(recorded.material["responsible_act_evidence_identity"])
    yield_evidence = ledger.get(recorded.material["yield_evidence_identity"])

    assert recorded.kind == OCCURRENCE_POSITION_RECORDED_KIND
    assert act_evidence.kind == OCCURRENCE_POSITION_ACT_EVIDENCE_KIND
    assert act_evidence.material["act_occurrence_identity"] == recorded.material[
        "act_occurrence_identity"
    ]
    assert act_evidence.material["responsibility_assignment_evidence"] == (
        recorded.material["responsibility_assignment_evidence"]
    )
    assert act_evidence.material["authority"] == "bounded repository authority"
    assert read_yield_relation_requirements(
        ledger,
        recorded_result_event_identity=recorded.identity,
        result_evidence_event_identity=yield_evidence.identity,
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


def test_position_finding_establishes_no_stronger_relation():
    _ledger, _occurrences, _boundary, _finding, recorded = recorded_road()

    assert "first_subject" not in recorded.material
    assert "second_subject" not in recorded.material
    assert recorded.material["limits"] == [
        "occurrence position does not establish causation or another relation"
    ]


def test_changed_position_is_not_certified_by_unchanged_evidence():
    ledger, _occurrences, _boundary, _finding, recorded = recorded_road()
    recorded.material["occurrences"][0]["position"] = 1

    with pytest.raises(ValueError):
        get_recorded_occurrence_position_measurement(ledger, recorded.identity)


def test_corrupted_input_act_or_yield_evidence_is_refused():
    for coordinate in (
        "input",
        "responsible_act_evidence_identity",
        "yield_evidence_identity",
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
    recorded = record_occurrence_position_measurement(
        ledger,
        recording_locality_identity="measurement",
        finding=finding,
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
    recorded = record_occurrence_position_measurement(
        ledger,
        recording_locality_identity="measurement",
        finding=measure_occurrence_position(
            ledger,
            source_locality_identity="a",
        ),
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
