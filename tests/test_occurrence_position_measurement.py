"""Exact position for each Locality occurrence is established by Measurement."""

from copy import deepcopy

import pytest

import seed_runtime.occurrence_position_measurement as position_measurement
from seed_runtime.events import CORRUPTED, EventLedger, SQLiteEventLedger
from seed_runtime.occurrence_position_measurement import (
    OCCURRENCE_POSITION_ACT_OCCURRENCE_EVENT,
    OCCURRENCE_POSITION_RECORDED_KIND,
    OCCURRENCE_POSITION_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
    OCCURRENCE_POSITION_RESULT_COORDINATES,
    OccurrencePositionFinding,
    get_occurrence_position_measurement_subject_to_act_binding,
    get_recorded_occurrence_position_measurement,
    measure_occurrence_position,
    record_occurrence_position_measurement_subject_to_act_binding,
    record_occurrence_position_measurement_act_occurrence,
    record_occurrence_position_measurement_result,
)
from seed_runtime.operator_current_coordinates import read_operator_current_coordinates
from seed_runtime.yield_relation import (
    RECORDED_YIELD_RELATION_EVENT,
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


def _current_coordinates(ledger, locality="measurement"):
    return read_operator_current_coordinates(
        ledger, locality_identity=locality
    )


def _record_binding(ledger, finding, locality="measurement"):
    return record_occurrence_position_measurement_subject_to_act_binding(
        ledger,
        recording_locality_identity=locality,
        finding=finding,
        current_coordinates=_current_coordinates(ledger, locality),
    )


def _record_act(ledger, finding, locality="measurement"):
    binding = _record_binding(ledger, finding, locality)
    act = record_occurrence_position_measurement_act_occurrence(
        ledger,
        binding_event_identity=binding.identity,
        current_coordinates=_current_coordinates(ledger, locality),
    )
    return binding, act


def recorded_road():
    ledger, occurrences, boundary = occurrence_road()
    finding = measure_occurrence_position(
        ledger,
        source_locality_identity="a",
        through=boundary,
    )
    _binding, act_occurrence = _record_act(ledger, finding)
    recorded = record_occurrence_position_measurement_result(
        ledger,
        act_occurrence_event_identity=act_occurrence.identity,
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
        record_occurrence_position_measurement_subject_to_act_binding(
            ledger,
            recording_locality_identity="measurement",
            finding=reversed_finding,
            current_coordinates=_current_coordinates(ledger),
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
        record_occurrence_position_measurement_subject_to_act_binding(
            ledger,
            recording_locality_identity="measurement",
            finding=subclass_finding,
            current_coordinates=_current_coordinates(ledger),
        )


def test_corrupted_source_cannot_enter_act_occurrence_after_measurement():
    ledger, occurrences, boundary = occurrence_road()
    finding = measure_occurrence_position(
        ledger,
        source_locality_identity="a",
        through=boundary,
    )
    ledger.corrupted.add(occurrences[1].identity)

    with pytest.raises(ValueError, match="requires intact occurrences"):
        record_occurrence_position_measurement_subject_to_act_binding(
            ledger,
            recording_locality_identity="measurement",
            finding=finding,
            current_coordinates=_current_coordinates(ledger),
        )


def test_recorded_position_measurement_has_exact_act_and_yield_relation():
    ledger, _occurrences, _boundary, finding, recorded = recorded_road()
    act_occurrence = ledger.get(recorded.material["act_occurrence_event_identity"])
    yield_relation = ledger.get(recorded.material["yield_relation_identity"])

    assert recorded.kind == OCCURRENCE_POSITION_RECORDED_KIND
    assert act_occurrence.kind == OCCURRENCE_POSITION_ACT_OCCURRENCE_EVENT
    assert act_occurrence.material["act_occurrence_identity"] == recorded.material[
        "act_occurrence_identity"
    ]
    assert read_requirements_of_yield_relation(
        ledger,
        recorded_result_event_identity=recorded.identity,
        yield_relation_event_identity=yield_relation.identity,
        act_occurrence_event_identity=act_occurrence.identity,
    ) == {
        "exact_relation": True,
        "occurrence_witness": True,
        "intact_occurrence": True,
    }
    assert get_recorded_occurrence_position_measurement(
        ledger,
        recorded.identity,
    ) == finding


def test_binding_act_yield_and_result_keep_distinct_exact_identities():
    ledger, _occurrences, _boundary, _finding, recorded = recorded_road()
    reference = recorded.material["subject_to_act_binding_reference"]
    binding = get_occurrence_position_measurement_subject_to_act_binding(
        ledger, reference["recorded_occurrence_identity"]
    )
    act_occurrence = ledger.get(recorded.material["act_occurrence_event_identity"])
    yielded = ledger.get(recorded.material["yield_relation_identity"])

    assert binding.kind == (
        OCCURRENCE_POSITION_SUBJECT_TO_ACT_BINDING_RECORDED_KIND
    )
    assert set(binding.material) == {
        "subject_reference",
        "exact_act_identity",
        "act_occurrence_identity",
        "measurement_result_identity",
        "book_clause_identity",
        "source_locality_identity",
        "completeness_boundary_identity",
        "through_event_occurrence_identity",
    }
    assert reference == {
        "recorded_occurrence_identity": binding.identity,
        "book_clause_identity": binding.material["book_clause_identity"],
        "exact_act_identity": binding.material["exact_act_identity"],
        "subject_reference": binding.material["subject_reference"],
    }
    assert binding.identity in _current_coordinates(ledger)[
        "subject_to_act_binding_occurrences"
    ]
    assert len(
        {
            binding.material["exact_act_identity"],
            binding.material["act_occurrence_identity"],
            binding.material["measurement_result_identity"],
            binding.identity,
            act_occurrence.identity,
            yielded.identity,
            recorded.identity,
        }
    ) == 7


def test_act_requires_current_coordinates_carrying_the_binding():
    ledger, _occurrences, boundary = occurrence_road()
    finding = measure_occurrence_position(
        ledger, source_locality_identity="a", through=boundary
    )
    before_binding = _current_coordinates(ledger)
    binding = record_occurrence_position_measurement_subject_to_act_binding(
        ledger,
        recording_locality_identity="measurement",
        finding=finding,
        current_coordinates=before_binding,
    )
    before = ledger.append_boundary()

    with pytest.raises(ValueError, match="exact current coordinates"):
        record_occurrence_position_measurement_act_occurrence(
            ledger,
            binding_event_identity=binding.identity,
            current_coordinates=before_binding,
        )

    assert ledger.append_boundary() == before
    assert record_occurrence_position_measurement_act_occurrence(
        ledger,
        binding_event_identity=binding.identity,
        current_coordinates=_current_coordinates(ledger),
    ).kind == OCCURRENCE_POSITION_ACT_OCCURRENCE_EVENT


def test_binding_refuses_stale_current_coordinates_without_appending():
    ledger, _occurrences, boundary = occurrence_road()
    finding = measure_occurrence_position(
        ledger, source_locality_identity="a", through=boundary
    )
    stale = _current_coordinates(ledger)
    _record_binding(ledger, finding)
    before = ledger.append_boundary()

    with pytest.raises(ValueError, match="exact current coordinates"):
        record_occurrence_position_measurement_subject_to_act_binding(
            ledger,
            recording_locality_identity="measurement",
            finding=finding,
            current_coordinates=stale,
        )

    assert ledger.append_boundary() == before


def test_one_binding_cannot_record_two_act_occurrences():
    ledger, _occurrences, boundary = occurrence_road()
    finding = measure_occurrence_position(
        ledger, source_locality_identity="a", through=boundary
    )
    binding, _act = _record_act(ledger, finding)
    before = ledger.append_boundary()

    with pytest.raises(ValueError, match="already carries an Act"):
        record_occurrence_position_measurement_act_occurrence(
            ledger,
            binding_event_identity=binding.identity,
            current_coordinates=_current_coordinates(ledger),
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
    position_results = position_measurement._position_results
    result_position_calls = []

    def counted_position_results(*args, **kwargs):
        result_position_calls.append(None)
        return position_results(*args, **kwargs)

    monkeypatch.setattr(
        position_measurement,
        "_position_results",
        counted_position_results,
    )

    binding, act_occurrence = _record_act(ledger, finding)
    recorded = record_occurrence_position_measurement_result(
        ledger,
        act_occurrence_event_identity=act_occurrence.identity,
    )
    yielded = ledger.get(recorded.material["yield_relation_identity"])
    assert get_recorded_occurrence_position_measurement(
        ledger,
        recorded.identity,
    ) == finding

    assert len(result_position_calls) == 2
    assert act_occurrence.material["subject_to_act_binding_reference"][
        "recorded_occurrence_identity"
    ] == binding.identity
    assert yielded.material["result"]["result_positions"] == recorded.material[
        "result_positions"
    ]
    assert yielded.material["result"]["result_positions"] is not recorded.material[
        "result_positions"
    ]


def test_act_occurrence_is_observed_before_yield_without_reconstructing_finding(
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

    binding, act_occurrence = _record_act(ledger, finding)

    assert [
        event.kind for event in ledger.list_locality("measurement")
    ] == [
        OCCURRENCE_POSITION_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
        OCCURRENCE_POSITION_ACT_OCCURRENCE_EVENT,
    ]
    assert "result_identity" not in act_occurrence.material
    assert "occurrences" not in act_occurrence.material
    assert act_occurrence.material["subject_to_act_binding_reference"][
        "recorded_occurrence_identity"
    ] == binding.identity
    observed = ledger.append(
        "test.act_occurrence_observed",
        {"act_occurrence_event_identity": act_occurrence.identity},
        locality_identity="measurement",
    )

    recorded = record_occurrence_position_measurement_result(
        ledger,
        act_occurrence_event_identity=act_occurrence.identity,
    )

    events = ledger.list_locality("measurement")
    assert [event.kind for event in events] == [
        OCCURRENCE_POSITION_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
        OCCURRENCE_POSITION_ACT_OCCURRENCE_EVENT,
        observed.kind,
        RECORDED_YIELD_RELATION_EVENT,
        OCCURRENCE_POSITION_RECORDED_KIND,
    ]
    assert recorded.material["act_occurrence_event_identity"] == (
        act_occurrence.identity
    )
    assert get_recorded_occurrence_position_measurement(
        ledger,
        recorded.identity,
    ) == finding
    assert measurements == []


@pytest.mark.parametrize(
    "act_occurrence_identity",
    (None, "", "absent_act_occurrence", StringSubclass("absent_act_occurrence")),
)
def test_result_refuses_arbitrary_act_occurrence_identity_without_appending(
    act_occurrence_identity,
):
    ledger, _occurrences, boundary = occurrence_road()
    finding = measure_occurrence_position(
        ledger,
        source_locality_identity="a",
        through=boundary,
    )
    before = ledger.append_boundary()

    with pytest.raises(ValueError, match="Act occurrence"):
        record_occurrence_position_measurement_result(
            ledger,
            act_occurrence_event_identity=act_occurrence_identity,
        )

    assert ledger.append_boundary() == before


def test_result_refuses_substituted_binding_without_appending_yield():
    ledger, _occurrences, boundary = occurrence_road()
    finding = measure_occurrence_position(
        ledger,
        source_locality_identity="a",
        through=boundary,
    )
    _binding, act_occurrence = _record_act(ledger, finding)
    act_occurrence.material["subject_to_act_binding_reference"][
        "recorded_occurrence_identity"
    ] = "substituted-binding"
    before = ledger.append_boundary()

    with pytest.raises(ValueError, match="exact intact Act occurrence"):
        record_occurrence_position_measurement_result(
            ledger,
            act_occurrence_event_identity=act_occurrence.identity,
        )

    assert ledger.append_boundary() == before


def test_result_refuses_wrong_kind_and_corrupted_act_occurrence():
    ledger, _occurrences, boundary = occurrence_road()
    finding = measure_occurrence_position(
        ledger,
        source_locality_identity="a",
        through=boundary,
    )
    wrong_kind = ledger.append(
        "test.not_act_occurrence",
        {},
        locality_identity="measurement",
    )
    _binding, act_occurrence = _record_act(ledger, finding)

    with pytest.raises(ValueError, match="exact intact Act occurrence"):
        record_occurrence_position_measurement_result(
            ledger,
            act_occurrence_event_identity=wrong_kind.identity,
        )

    ledger.corrupted.add(act_occurrence.identity)
    with pytest.raises(ValueError, match="exact intact Act occurrence"):
        record_occurrence_position_measurement_result(
            ledger,
            act_occurrence_event_identity=act_occurrence.identity,
        )


def test_one_measurement_act_cannot_yield_two_results():
    ledger, _occurrences, boundary = occurrence_road()
    finding = measure_occurrence_position(
        ledger,
        source_locality_identity="a",
        through=boundary,
    )
    _binding, act_occurrence = _record_act(ledger, finding)
    record_occurrence_position_measurement_result(
        ledger,
        act_occurrence_event_identity=act_occurrence.identity,
    )
    before = ledger.append_boundary()

    with pytest.raises(ValueError, match="already carries a Yield"):
        record_occurrence_position_measurement_result(
            ledger,
            act_occurrence_event_identity=act_occurrence.identity,
        )

    assert ledger.append_boundary() == before


def test_carried_result_skips_history_scan_only_at_its_exact_act_tip(monkeypatch):
    ledger, _occurrences, boundary = occurrence_road()
    finding = measure_occurrence_position(
        ledger,
        source_locality_identity="a",
        through=boundary,
    )
    binding, act_occurrence = _record_act(ledger, finding, locality="a")

    def history_scan_is_not_available(*_args, **_kwargs):
        raise AssertionError(
            "same-call result scanned prior Yield or result occurrences"
        )

    monkeypatch.setattr(ledger, "iter_locality_kind", history_scan_is_not_available)
    recorded = (
        position_measurement._record_occurrence_position_measurement_result_from_carried_act_occurrence(
            ledger,
            act_occurrence=act_occurrence,
            binding=binding,
            finding=finding,
        )
    )
    assert recorded.kind == OCCURRENCE_POSITION_RECORDED_KIND

    with pytest.raises(ValueError, match="exact intact Act occurrence"):
        (
            position_measurement._record_occurrence_position_measurement_result_from_carried_act_occurrence(
                ledger,
                act_occurrence=act_occurrence,
                binding=binding,
                finding=finding,
            )
        )


def test_changed_position_is_refused_by_the_unchanged_yield_relation():
    ledger, _occurrences, _boundary, _finding, recorded = recorded_road()
    recorded.material["result_positions"][0]["dimensions"]["content"]["position"] = 1

    with pytest.raises(ValueError):
        get_recorded_occurrence_position_measurement(ledger, recorded.identity)


def test_result_carries_one_ordered_result_position_per_exact_position():
    ledger, occurrences, boundary, _finding, recorded = recorded_road()

    assert set(recorded.material) == OCCURRENCE_POSITION_RESULT_COORDINATES | {
        "act_occurrence_identity",
        "act_occurrence_event_identity",
        "yield_relation_identity",
    }
    assert recorded.material["source_localities"] == ["a"]
    assert recorded.material["completeness_boundary"] == {
        "identity": boundary.identity
    }
    result_positions = recorded.material["result_positions"]
    assert len(result_positions) == len(occurrences)
    assert [
        (
            item["subject"]["occurrence_identity"],
            item["dimensions"]["content"]["position"],
        )
        for item in result_positions
    ] == [(event.identity, position) for position, event in enumerate(occurrences)]
    assert [item["dimensions"]["identity"] for item in result_positions] == [
        event.identity for event in occurrences
    ]
    assert _current_coordinates(ledger)["measurement_occurrences"][recorded.identity] == {
        "recorded_occurrence_identity": recorded.identity,
        "result_identity": recorded.material["result_identity"],
        "act_occurrence_event_identity": recorded.material["act_occurrence_event_identity"],
        "act_occurrence_identity": recorded.material[
            "act_occurrence_identity"
        ],
        "yield_relation_identity": recorded.material[
            "yield_relation_identity"
        ],
    }
    assert all(
        set(item)
        == {
            "dimensions",
            "result",
            "subject",
        }
        and item["result"] == "position"
        for item in result_positions
    )


@pytest.mark.parametrize(
    "mutate",
    (
        lambda result_positions: result_positions.pop(1),
        lambda result_positions: result_positions.reverse(),
        lambda result_positions: result_positions.__setitem__(1, deepcopy(result_positions[0])),
        lambda result_positions: result_positions[1]["subject"].__setitem__(
            "occurrence_identity", "substituted-occurrence"
        ),
        lambda result_positions: result_positions[1]["dimensions"]["content"].__setitem__(
            "position", 0
        ),
    ),
)
def test_missing_reordered_duplicated_or_substituted_result_positions_are_refused(mutate):
    ledger, _occurrences, _boundary, _finding, recorded = recorded_road()
    mutate(recorded.material["result_positions"])

    with pytest.raises(ValueError, match="malformed result positions"):
        get_recorded_occurrence_position_measurement(ledger, recorded.identity)


@pytest.mark.parametrize(
    "coordinate, value",
    (
        ("source_localities", ["b"]),
        ("completeness_boundary", {"identity": "another-boundary"}),
    ),
)
def test_wrong_result_boundary_coordinates_are_refused(coordinate, value):
    ledger, _occurrences, _boundary, _finding, recorded = recorded_road()
    recorded.material[coordinate] = value

    with pytest.raises(ValueError):
        get_recorded_occurrence_position_measurement(ledger, recorded.identity)


def test_corrupted_input_act_or_yield_relation_is_refused():
    for coordinate in (
        "input",
        "act_occurrence_event_identity",
        "yield_relation_identity",
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
    _binding, act_occurrence = _record_act(ledger, finding)
    recorded = record_occurrence_position_measurement_result(
        ledger,
        act_occurrence_event_identity=act_occurrence.identity,
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
    path = tmp_path / "occurrence-position.sqlite"
    ledger = SQLiteEventLedger(path)
    ledger.append("test.occurrence", {"material": "a"}, locality_identity="a")
    finding = measure_occurrence_position(
        ledger,
        source_locality_identity="a",
    )
    _binding, act_occurrence = _record_act(ledger, finding)
    recorded = record_occurrence_position_measurement_result(
        ledger,
        act_occurrence_event_identity=act_occurrence.identity,
    )
    carried = {
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

    reopened = SQLiteEventLedger(path)
    try:
        for prefix, identity in carried.items():
            prior_number = int(identity.rsplit("_", 1)[1])
            assert reopened.mint_identity(prefix) == f"{prefix}_{prior_number + 1:06d}"
    finally:
        reopened.close()


def test_binding_act_and_result_remain_exact_across_separate_restarts(tmp_path):
    path = tmp_path / "occurrence-position-restarts.sqlite"
    ledger = SQLiteEventLedger(path)
    first = ledger.append(
        "test.occurrence", {"material": "a"}, locality_identity="a"
    )
    finding = measure_occurrence_position(
        ledger, source_locality_identity="a"
    )
    binding = _record_binding(ledger, finding)
    binding_identity = binding.identity
    ledger.close()

    ledger = SQLiteEventLedger(path)
    binding = get_occurrence_position_measurement_subject_to_act_binding(
        ledger, binding_identity
    )
    act_occurrence = record_occurrence_position_measurement_act_occurrence(
        ledger,
        binding_event_identity=binding.identity,
        current_coordinates=_current_coordinates(ledger),
    )
    act_identity = act_occurrence.identity
    ledger.close()

    ledger = SQLiteEventLedger(path)
    try:
        recorded = record_occurrence_position_measurement_result(
            ledger,
            act_occurrence_event_identity=act_identity,
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
    _binding, act_occurrence = _record_act(ledger, finding)
    record_occurrence_position_measurement_result(
        ledger,
        act_occurrence_event_identity=act_occurrence.identity,
    )
    act_identity = act_occurrence.identity
    ledger.close()

    reopened = SQLiteEventLedger(path)
    try:
        before = reopened.append_boundary()
        with pytest.raises(ValueError, match="already carries a Yield"):
            record_occurrence_position_measurement_result(
                reopened,
                act_occurrence_event_identity=act_identity,
            )
        assert reopened.append_boundary() == before
    finally:
        reopened.close()




WITNESSED_BOOK_COORDINATES = {
    ("book_coordinates", "01.Source.D", "result"): (
        test_a_later_occurrence_does_not_revise_the_bounded_positions,
        test_supplied_reversal_cannot_replace_the_ledger_measurement,
        test_subclass_finding_cannot_replace_the_exact_measurement_type,
        test_recording_and_reading_do_not_reconstruct_complete_result_material,
        test_changed_position_is_refused_by_the_unchanged_yield_relation,
        test_missing_reordered_duplicated_or_substituted_result_positions_are_refused,
        test_wrong_result_boundary_coordinates_are_refused,
        test_wrong_boundary_is_refused_without_reconstructing_positions,
        test_durable_position_identities_are_not_reissued_after_reopen,
    ),
}
