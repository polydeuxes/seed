from copy import deepcopy

import pytest

import seed_runtime.measurement_of_position_coordinates_of_byte_pair_occurrences as direct_position_module
import seed_runtime.operator_current_coordinates as standing_module
from seed_runtime.yield_relation import _record_yield_relation
from seed_runtime.yield_relation import (
    RECORDED_YIELD_RELATION_EVENT,
)
from seed_runtime.byte_measurement import (
    ASSERTION_LOCALITY_MOVEMENT_ACT_OCCURRENCE_EVENT,
    ASSERTION_LOCALITY_MOVEMENT_KIND,
    ASSERTION_LOCALITY_MOVEMENT_SUBJECT_TO_ACT_BINDING_KIND,
    ByteMeasurementError,
)
from seed_runtime.events import EventLedger, SQLiteEventLedger
from tests.operator_material_source_test_witness import (
    record_operator_material_occurrence,
)
from seed_runtime.measurement_of_position_coordinates_of_byte_pair_occurrences import (
    BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND,
    RESULT_KIND,
    _recorded_position_assertions_for_locality_movement,
    _recorded_position_assertion_at_position_for_locality_movement,
    record_byte_pair_occurrence_position_measurement_act_occurrence,
    record_byte_pair_occurrence_position_measurement_subject_to_act_binding,
    get_byte_pair_occurrence_position_measurement_act_occurrence,
    get_byte_pair_occurrence_position_measurement_subject_to_act_binding,
    get_recorded_byte_pair_occurrence_position_measurement,
    measure_position_coordinates_of_byte_pair_occurrences,
    move_recorded_position_assertion_to_locality,
    record_byte_pair_occurrence_position_measurement_act_occurrence,
    record_byte_pair_occurrence_position_measurement_subject_to_act_binding,
    record_byte_pair_occurrence_position_measurement_result,
    read_unbound_position_coordinate_measurement_material_results_through,
    references_to_addressed_recorded_position_coordinates_of_byte_pair_occurrences,
    references_to_recorded_byte_pair_occurrences_carrying_addressed_source_position_coordinate,
    references_to_recorded_position_coordinates_of_byte_pair_occurrences,
)


class MovementSourceChangeLedger(EventLedger):
    def __init__(self):
        super().__init__()
        self.source_event_identity = None
        self.trigger_kind = None
        self.changed = False

    def append(
        self,
        kind,
        material=None,
        *,
        exact_material=None,
        locality_identity=None,
    ):
        event = super().append(
            kind,
            material,
            exact_material=exact_material,
            locality_identity=locality_identity,
        )
        if (
            not self.changed
            and kind == self.trigger_kind
            and type(self.source_event_identity) is str
        ):
            self.changed = True
            source = self.get(self.source_event_identity)
            source.material["result_identity"] = (
                "changed after movement occurrence"
            )
        return event
from seed_runtime.operator_current_coordinates import (
    _carry_byte_pair_occurrence_position_measurement_result_into_current_coordinates,
    read_operator_current_coordinates,
)


def _standing(ledger, locality):
    return read_operator_current_coordinates(ledger, locality_identity=locality)


def _source(ledger, exact=b"2+2=5\n", locality="position-occurrence-position"):
    return record_operator_material_occurrence(
        ledger,
        locality_identity=locality,
        exact=exact,
        source_boundary="exact supplied material boundary",
    )


def _record(ledger, exact=b"2+2=5\n", locality="position-occurrence-position"):
    source = _source(ledger, exact, locality)
    assignment = record_byte_pair_occurrence_position_measurement_subject_to_act_binding(
        ledger,
        source_material_result_occurrence_identity=source.identity,
        current_coordinates=_standing(ledger, locality),
    )
    act = record_byte_pair_occurrence_position_measurement_act_occurrence(
        ledger,
        binding_event_identity=assignment.identity,
        binding_current_coordinates=_standing(ledger, locality),
    )
    result = record_byte_pair_occurrence_position_measurement_result(
        ledger,
        act_occurrence_event_identity=act.identity,
    )
    return source, assignment, act, result


def test_each_input_pair_has_first_and_second_exact_position_coordinates():
    ledger = EventLedger()
    source = _source(ledger)

    finding = measure_position_coordinates_of_byte_pair_occurrences(
        ledger,
        source_material_result_occurrence_identity=source.identity,
    )

    assert finding.occurrences == (
        (b"2+", 0, 1),
        (b"+2", 1, 2),
        (b"2=", 2, 3),
        (b"=5", 3, 4),
        (b"5\n", 4, 5),
    )
    assert finding.source_material_result_occurrence_identity == source.identity
    assert finding.completeness_boundary == (
        ledger.append_boundary_through_occurrence(source.identity)
    )


def test_exact_unbound_material_results_are_read_through_frozen_b():
    ledger = EventLedger()
    first = _source(ledger, b"ab", locality="s")
    first_boundary = ledger.append_boundary_through_occurrence(first.identity)
    second = _source(ledger, b"cd", locality="s")
    tip_before_read = ledger.append_boundary()

    through_first = read_unbound_position_coordinate_measurement_material_results_through(
        ledger,
        locality_identity="s",
        through_event_occurrence_identity=first.identity,
    )
    through_second = read_unbound_position_coordinate_measurement_material_results_through(
        ledger,
        locality_identity="s",
        through_event_occurrence_identity=second.identity,
    )

    assert ledger.append_boundary() == tip_before_read
    assert tuple(
        subject.source_material_result_occurrence_identity for subject in through_first
    ) == (first.identity,)
    assert tuple(
        subject.source_material_result_occurrence_identity for subject in through_second
    ) == (first.identity, second.identity)
    first_source = through_first[0]
    assert first_source.source_result_identity == first.material["result_identity"]
    assert first_source.source_locality_identity == "s"
    assert (
        first_source.source_completeness_boundary_identity
        == first_boundary.identity
    )
    assert (
        first_source.bounded_locality_replay_through_event_occurrence_identity
        == first.identity
    )
    assert (
        first_source.bounded_locality_replay_append_boundary_identity
        == first_boundary.identity
    )
    assert first_source.act_occurrence_identity == first.material[
        "act_occurrence_identity"
    ]
    assert first_source.yield_relation_identity == first.material[
        "yield_relation_identity"
    ]
    assert first_source.source_boundary == "exact supplied material boundary"
    assert first_source.exact_material == b"ab"
    assert first_source.known_loss == ()
    assert first_source.source_occurrence_references == ()
    assert "locality_relation" not in first_source._fields


def test_later_assignment_does_not_change_an_earlier_subject_read():
    ledger = EventLedger()
    first = _source(ledger, b"ab", locality="s")
    second = _source(ledger, b"cd", locality="s")
    through_sources = read_unbound_position_coordinate_measurement_material_results_through(
        ledger,
        locality_identity="s",
        through_event_occurrence_identity=second.identity,
    )
    assignment = record_byte_pair_occurrence_position_measurement_subject_to_act_binding(
        ledger,
        source_material_result_occurrence_identity=first.identity,
        current_coordinates=_standing(ledger, "s"),
    )
    tip_after_assignment = ledger.append_boundary()

    same_earlier_read = (
        read_unbound_position_coordinate_measurement_material_results_through(
            ledger,
            locality_identity="s",
            through_event_occurrence_identity=second.identity,
        )
    )
    through_assignment = (
        read_unbound_position_coordinate_measurement_material_results_through(
            ledger,
            locality_identity="s",
            through_event_occurrence_identity=assignment.identity,
        )
    )

    assert ledger.append_boundary() == tip_after_assignment
    assert same_earlier_read == through_sources
    assert tuple(
        subject.source_material_result_occurrence_identity for subject in through_assignment
    ) == (second.identity,)


def test_direct_recorder_refuses_a_subject_with_an_assignment_already_recorded():
    ledger = EventLedger()
    source = _source(ledger, locality="s")
    record_byte_pair_occurrence_position_measurement_subject_to_act_binding(
        ledger,
        source_material_result_occurrence_identity=source.identity,
        current_coordinates=_standing(ledger, "s"),
    )
    boundary = ledger.append_boundary()

    with pytest.raises(ValueError, match="one exact current unbound material result"):
        record_byte_pair_occurrence_position_measurement_subject_to_act_binding(
            ledger,
            source_material_result_occurrence_identity=source.identity,
            current_coordinates=_standing(ledger, "s"),
        )

    assert ledger.append_boundary() == boundary


def test_unbound_material_result_read_survives_sqlite_restart(tmp_path):
    path = tmp_path / "position-coordinate-assignment-subjects.sqlite"
    ledger = SQLiteEventLedger(path)
    first = _source(ledger, b"ab", locality="s")
    second = _source(ledger, b"cd", locality="s")
    before = read_unbound_position_coordinate_measurement_material_results_through(
        ledger,
        locality_identity="s",
        through_event_occurrence_identity=second.identity,
    )
    boundary = ledger.append_boundary()
    second_identity = second.identity
    ledger.close()

    reopened = SQLiteEventLedger(path)
    try:
        after = read_unbound_position_coordinate_measurement_material_results_through(
            reopened,
            locality_identity="s",
            through_event_occurrence_identity=second_identity,
        )
        assert after == before
        assert reopened.append_boundary() == boundary
        assert tuple(
            subject.source_material_result_occurrence_identity for subject in after
        ) == (first.identity, second.identity)
    finally:
        reopened.close()


def test_same_pair_material_at_distinct_positions_remains_distinct_occurrences():
    ledger = EventLedger()
    source = _source(ledger, b"aaa")

    finding = measure_position_coordinates_of_byte_pair_occurrences(
        ledger,
        source_material_result_occurrence_identity=source.identity,
    )

    assert finding.occurrences == ((b"aa", 0, 1), (b"aa", 1, 2))


@pytest.mark.parametrize("exact", (b"x",))
def test_material_without_a_byte_pair_yields_an_exact_empty_result(exact):
    ledger = EventLedger()
    _source_event, _assignment, _act, result = _record(ledger, exact)

    finding = get_recorded_byte_pair_occurrence_position_measurement(
        ledger, result.identity
    )

    assert finding.occurrences == ()
    assert result.material["assertions"]["occurrences"] == 0


def test_empty_witness_material_locality_can_acquire_an_empty_measurement_assignment():
    from seed_runtime.witness_material_source import (
        record_witness_material_source,
    )

    ledger = EventLedger()
    source = record_witness_material_source(
        ledger,
        locality_identity="position-occurrence-position",
        exact_bytes=b"",
        source_boundary="empty Witness boundary",
    )
    finding = measure_position_coordinates_of_byte_pair_occurrences(
        ledger,
        source_material_result_occurrence_identity=source.identity,
    )
    assert finding.occurrences == ()
    assignment = record_byte_pair_occurrence_position_measurement_subject_to_act_binding(
        ledger,
        source_material_result_occurrence_identity=source.identity,
        current_coordinates=_standing(
            ledger, "position-occurrence-position"
        ),
    )
    assert assignment.material[
        "source_material_result_occurrence_identity"
    ] == source.identity


def test_assignment_act_yield_and_result_enter_current_standing():
    ledger = EventLedger()
    source = _source(ledger)
    locality = source.locality_identity
    assignment = record_byte_pair_occurrence_position_measurement_subject_to_act_binding(
        ledger,
        source_material_result_occurrence_identity=source.identity,
        current_coordinates=_standing(ledger, locality),
    )
    assert assignment.identity in _standing(
        ledger, locality
    )["subject_to_act_binding_occurrences"]

    act = record_byte_pair_occurrence_position_measurement_act_occurrence(
        ledger,
        binding_event_identity=assignment.identity,
        binding_current_coordinates=_standing(ledger, locality),
    )
    result = record_byte_pair_occurrence_position_measurement_result(
        ledger,
        act_occurrence_event_identity=act.identity,
    )
    standing = _standing(ledger, locality)

    assert get_byte_pair_occurrence_position_measurement_subject_to_act_binding(
        ledger, assignment.identity
    ) == assignment
    assert get_byte_pair_occurrence_position_measurement_act_occurrence(
        ledger, act.identity
    ) == act
    assert result.identity in standing["measurement_occurrences"]
    assert result.material["yield_relation_identity"] == (
        standing["measurement_occurrences"][result.identity][
            "yield_relation_identity"
        ]
    )


def test_act_requires_current_coordinates_that_carry_exact_binding():
    ledger = EventLedger()
    source = _source(ledger)
    locality = source.locality_identity
    before_binding = _standing(ledger, locality)
    binding = record_byte_pair_occurrence_position_measurement_subject_to_act_binding(
        ledger,
        source_material_result_occurrence_identity=source.identity,
        current_coordinates=before_binding,
    )
    assert set(binding.material) == {
        "subject_reference",
        "exact_act_identity",
        "act_occurrence_identity",
        "measurement_result_identity",
        "result_boundary_identity",
        "book_clause_identity",
        "source_material_result_occurrence_identity",
        "source_locality_identity",
        "completeness_boundary_identity",
        "through_event_occurrence_identity",
        "input_relation",
    }

    with pytest.raises(ValueError, match="exact current coordinates"):
        record_byte_pair_occurrence_position_measurement_act_occurrence(
            ledger,
            binding_event_identity=binding.identity,
            binding_current_coordinates=before_binding,
        )


def test_one_assignment_records_one_act_and_one_result():
    ledger = EventLedger()
    _source_event, assignment, act, _result = _record(ledger)

    with pytest.raises(ValueError, match="already carries an Act"):
        record_byte_pair_occurrence_position_measurement_act_occurrence(
            ledger,
            binding_event_identity=assignment.identity,
            binding_current_coordinates=_standing(
                ledger, assignment.locality_identity
            ),
        )
    with pytest.raises(ValueError, match="already carries a Yield"):
        record_byte_pair_occurrence_position_measurement_result(
            ledger,
            act_occurrence_event_identity=act.identity,
        )


def test_carried_result_skips_history_scan_only_at_its_exact_act_tip(monkeypatch):
    ledger = EventLedger()
    source = _source(ledger)
    locality = source.locality_identity
    finding = measure_position_coordinates_of_byte_pair_occurrences(
        ledger,
        source_material_result_occurrence_identity=source.identity,
    )
    assignment = record_byte_pair_occurrence_position_measurement_subject_to_act_binding(
        ledger,
        source_material_result_occurrence_identity=source.identity,
        current_coordinates=_standing(ledger, locality),
    )
    act = record_byte_pair_occurrence_position_measurement_act_occurrence(
        ledger,
        binding_event_identity=assignment.identity,
        binding_current_coordinates=_standing(ledger, locality),
    )

    def history_scan_is_not_available(*_args, **_kwargs):
        raise AssertionError(
            "carried result scanned prior Yield or result occurrences"
        )

    monkeypatch.setattr(ledger, "iter_locality_kind", history_scan_is_not_available)
    result = (
        direct_position_module._record_byte_pair_occurrence_position_measurement_result_from_carried_act_occurrence(
            ledger,
            act_occurrence=act,
            binding=assignment,
            finding=finding,
        )
    )
    assert result.kind == BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND

    with pytest.raises(ValueError, match="intact Act occurrence"):
        (
            direct_position_module._record_byte_pair_occurrence_position_measurement_result_from_carried_act_occurrence(
                ledger,
                act_occurrence=act,
                binding=assignment,
                finding=finding,
            )
        )


def test_result_refuses_changed_assertion_coordinates():
    ledger = EventLedger()
    _source_event, _assignment, _act, result = _record(ledger)
    result.material["assertions"]["dimensions"]["content"][
        "second_position"
    ] = "position"

    with pytest.raises(ValueError, match="coordinates are not exact"):
        get_recorded_byte_pair_occurrence_position_measurement(ledger, result.identity)


def test_references_preserve_every_exact_pair_occurrence():
    ledger = EventLedger()
    source, _assignment, _act, result = _record(ledger, b"aaa")

    references = (
        references_to_recorded_position_coordinates_of_byte_pair_occurrences(
            ledger, result.identity
        )
    )

    assert tuple(
        (reference.exact_pair, reference.first_position, reference.second_position)
        for reference in references
    ) == ((b"aa", 0, 1), (b"aa", 1, 2))
    assert tuple(reference.assertion_position for reference in references) == (0, 1)
    assert (
        references[0].second_position_coordinate_reference
        == references[1].first_position_coordinate_reference
    )
    assert references[0].first_position_coordinate_reference["position"] == 0
    assert references[0].second_position_coordinate_reference["position"] == 1
    assert all(
        reference.source_material_result_occurrence_identity == source.identity
        and reference.recorded_occurrence_identity == result.identity
        for reference in references
    )


def test_one_bounded_position_assertion_result_coordinates_equals_each_addressed_read():
    ledger = EventLedger()
    _source_event, _assignment, _act, result = _record(ledger, b"abcdef")
    references = (
        references_to_recorded_position_coordinates_of_byte_pair_occurrences(
            ledger, result.identity
        )
    )

    assertions = tuple(
        _recorded_position_assertions_for_locality_movement(
            ledger,
            result_event_identity=result.identity,
        )
    )

    assert assertions == tuple(
        _recorded_position_assertion_at_position_for_locality_movement(
            ledger,
            result_event_identity=result.identity,
            assertion_position=reference.assertion_position,
        )
        for reference in references
    )
    assert tuple(
        assertion["dimensions"]["position"] for assertion in assertions
    ) == tuple(reference.assertion_position for reference in references)
    assert all(
        set(assertion)
        == {
            "dimensions",
            "result",
            "assertion_subject",
            "conflicts",
        }
        for assertion in assertions
    )


def test_bounded_position_assertion_result_coordinates_reads_once_in_source_order(
    monkeypatch,
):
    ledger = EventLedger()
    _source_event, _assignment, _act, result = _record(ledger, b"abcdef")
    result_reads = 0
    original_result_read = direct_position_module._read_result

    def counted_result_read(*args, **kwargs):
        nonlocal result_reads
        result_reads += 1
        return original_result_read(*args, **kwargs)

    monkeypatch.setattr(direct_position_module, "_read_result", counted_result_read)

    assertions = tuple(
        _recorded_position_assertions_for_locality_movement(
            ledger,
            result_event_identity=result.identity,
        )
    )

    assert len(assertions) == 5
    assert result_reads == 1
    assert tuple(item["dimensions"]["position"] for item in assertions) == tuple(
        range(5)
    )


def test_bounded_position_assertion_result_coordinates_refuses_changed_result():
    ledger = EventLedger()
    _source_event, _assignment, _act, result = _record(ledger, b"abcdef")
    unchanged = tuple(
        _recorded_position_assertions_for_locality_movement(
            ledger,
            result_event_identity=result.identity,
        )
    )
    result.material["result_identity"] = (
        "changed before the bounded Assertion read"
    )

    with pytest.raises(ValueError, match="coordinates are not exact"):
        _recorded_position_assertions_for_locality_movement(
            ledger,
            result_event_identity=result.identity,
        )

    assert len(unchanged) == 5


def test_addressed_references_use_requested_result_local_positions():
    ledger = EventLedger()
    _source_event, _assignment, _act, result = _record(ledger, b"abcdef")
    all_references = (
        references_to_recorded_position_coordinates_of_byte_pair_occurrences(
            ledger, result.identity
        )
    )
    addressed = (
        references_to_addressed_recorded_position_coordinates_of_byte_pair_occurrences(
            ledger,
            result.identity,
            (
                all_references[0].assertion_position,
                all_references[1].assertion_position,
            ),
        )
    )

    assert addressed == all_references[:2]


def test_full_reference_reader_does_not_construct_the_occurrence_tuple(
    monkeypatch,
):
    ledger = EventLedger()
    _source_event, _assignment, _act, result = _record(ledger, b"abcdef")

    def occurrence_tuple_is_not_needed(_finding):
        raise AssertionError("full reference read constructed the occurrence tuple")

    monkeypatch.setattr(
        direct_position_module.FindingOfPositionCoordinatesOfBytePairOccurrences,
        "occurrences",
        property(occurrence_tuple_is_not_needed),
    )

    references = (
        references_to_recorded_position_coordinates_of_byte_pair_occurrences(
            ledger, result.identity
        )
    )
    assert tuple(reference.exact_pair for reference in references) == (
        b"ab",
        b"bc",
        b"cd",
        b"de",
        b"ef",
    )


def test_exact_addressed_source_position_reads_only_its_carried_pair_references(
    monkeypatch,
):
    ledger = EventLedger()
    _source_event, _assignment, _act, result = _record(ledger)
    all_references = (
        references_to_recorded_position_coordinates_of_byte_pair_occurrences(
            ledger, result.identity
        )
    )
    addressed_position = all_references[2].second_position_coordinate_reference
    assert addressed_position == all_references[3].first_position_coordinate_reference
    calls = []
    original = direct_position_module._recorded_position_reference

    def counted(*args, **kwargs):
        calls.append(kwargs["first_position"])
        return original(*args, **kwargs)

    def full_position_read_is_not_needed(*_args, **_kwargs):
        raise AssertionError("addressed source position read every position")

    monkeypatch.setattr(
        direct_position_module, "_recorded_position_reference", counted
    )
    monkeypatch.setattr(
        direct_position_module,
        "references_to_recorded_position_coordinates_of_byte_pair_occurrences",
        full_position_read_is_not_needed,
    )
    monkeypatch.setattr(
        direct_position_module,
        "references_to_addressed_recorded_position_coordinates_of_byte_pair_occurrences",
        full_position_read_is_not_needed,
    )

    references = (
        references_to_recorded_byte_pair_occurrences_carrying_addressed_source_position_coordinate(
            ledger, result.identity, addressed_position
        )
    )

    assert tuple(
        (reference.exact_pair, reference.first_position, reference.second_position)
        for reference in references
    ) == ((b"2=", 2, 3), (b"=5", 3, 4))
    assert all(
        addressed_position
        in (
            reference.first_position_coordinate_reference,
            reference.second_position_coordinate_reference,
        )
        for reference in references
    )
    assert calls == [2, 3]


@pytest.mark.parametrize(
    ("exact", "position", "expected"),
    (
        (b"abc", 0, ((b"ab", 0, 1),)),
        (b"abc", 2, ((b"bc", 1, 2),)),
        (b"x", 0, ()),
    ),
)
def test_addressed_source_position_preserves_exact_boundaries(
    exact, position, expected
):
    ledger = EventLedger()
    _source_event, _assignment, _act, result = _record(ledger, exact)
    finding = get_recorded_byte_pair_occurrence_position_measurement(
        ledger, result.identity
    )
    coordinate = direct_position_module._source_position_coordinate_reference(
        source_material_result_occurrence_identity=(
            finding.source_material_result_occurrence_identity
        ),
        source_locality_identity=finding.source_locality_identity,
        completeness_boundary_identity=finding.completeness_boundary.identity,
        position=position,
        exact_material=exact[position : position + 1],
    )

    references = (
        references_to_recorded_byte_pair_occurrences_carrying_addressed_source_position_coordinate(
            ledger, result.identity, coordinate
        )
    )

    assert tuple(
        (reference.exact_pair, reference.first_position, reference.second_position)
        for reference in references
    ) == expected


@pytest.mark.parametrize(
    "change",
    (
        lambda coordinate: coordinate.update(position=True),
        lambda coordinate: coordinate.update(position=-1),
        lambda coordinate: coordinate.update(exact_material=[0]),
        lambda coordinate: coordinate.update(locality_identity="another-locality"),
        lambda coordinate: coordinate.update(
            completeness_boundary_identity="another-boundary"
        ),
        lambda coordinate: coordinate.update(
            source_material_result_occurrence_identity="another-result"
        ),
    ),
)
def test_addressed_source_position_refuses_a_changed_coordinate(change):
    ledger = EventLedger()
    _source_event, _assignment, _act, result = _record(ledger, b"aaa")
    reference = references_to_recorded_position_coordinates_of_byte_pair_occurrences(
        ledger, result.identity
    )[0]
    coordinate = deepcopy(reference.second_position_coordinate_reference)
    change(coordinate)

    with pytest.raises(ValueError, match="addressed source position"):
        references_to_recorded_byte_pair_occurrences_carrying_addressed_source_position_coordinate(
            ledger, result.identity, coordinate
        )


def test_equal_byte_material_at_distinct_positions_has_distinct_coordinates():
    ledger = EventLedger()
    _source_event, _assignment, _act, result = _record(ledger, b"aaa")
    references = references_to_recorded_position_coordinates_of_byte_pair_occurrences(
        ledger, result.identity
    )
    first_a = references[0].first_position_coordinate_reference
    second_a = references[0].second_position_coordinate_reference

    assert first_a["exact_material"] == second_a["exact_material"]
    assert (first_a["position"], second_a["position"]) == (0, 1)
    assert (
        references_to_recorded_byte_pair_occurrences_carrying_addressed_source_position_coordinate(
            ledger, result.identity, second_a
        )
        == references
    )


def test_addressed_source_position_from_another_exact_result_is_refused():
    ledger = EventLedger()
    _first_source, _first_assignment, _first_act, first_result = _record(
        ledger, b"abc", "first-address-locality"
    )
    _second_source, _second_assignment, _second_act, second_result = _record(
        ledger, b"abc", "second-address-locality"
    )
    other_coordinate = (
        references_to_recorded_position_coordinates_of_byte_pair_occurrences(
            ledger, second_result.identity
        )[0].first_position_coordinate_reference
    )

    with pytest.raises(ValueError, match="exact recorded coordinate"):
        references_to_recorded_byte_pair_occurrences_carrying_addressed_source_position_coordinate(
            ledger, first_result.identity, other_coordinate
        )


@pytest.mark.parametrize(
    ("occurrence_boundary", "result_kind"),
    (
        ("byte_measurement", RESULT_KIND),
        ("byte_pair_occurrence_position_measurement", "another result kind"),
    ),
)
def test_result_refuses_an_intact_yield_from_another_exact_family(
    occurrence_boundary,
    result_kind,
):
    ledger = EventLedger()
    source = _source(ledger)
    assignment = record_byte_pair_occurrence_position_measurement_subject_to_act_binding(
        ledger,
        source_material_result_occurrence_identity=source.identity,
        current_coordinates=_standing(ledger, source.locality_identity),
    )
    act = record_byte_pair_occurrence_position_measurement_act_occurrence(
        ledger,
        binding_event_identity=assignment.identity,
        binding_current_coordinates=_standing(
            ledger, source.locality_identity
        ),
    )
    act_read, assignment_read, finding = direct_position_module._read_act(
        ledger, act.identity
    )
    result_material = direct_position_module._result_material(
        finding, assignment_read
    )
    yield_relation = _record_yield_relation(
        ledger,
        locality_identity=act.locality_identity,
        exact_act=direct_position_module.EXACT_ACT,
        act_occurrence_identity=assignment.material["act_occurrence_identity"],
        act_occurrence_event_identity=act_read.identity,
        result_kind=result_kind,
        result_identity=result_material["result_identity"],
        result_content=result_material,
        occurrence_boundary=occurrence_boundary,
    )
    result = ledger.append(
        BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND,
        {
            **result_material,
            "act_occurrence_event_identity": act.identity,
            "yield_relation_identity": yield_relation.identity,
        },
        locality_identity=act.locality_identity,
    )

    with pytest.raises(ValueError, match="exact Yield"):
        get_recorded_byte_pair_occurrence_position_measurement(ledger, result.identity)


def test_private_recorders_require_the_exact_carried_boundary(monkeypatch):
    ledger = EventLedger()
    source = _source(ledger)
    locality = source.locality_identity
    carried_source = _standing(ledger, locality)

    def coordinate_replay_is_not_available(*_args, **_kwargs):
        raise AssertionError("carried recorder reconstructed current coordinates")

    monkeypatch.setattr(
        standing_module,
        "read_operator_current_coordinates",
        coordinate_replay_is_not_available,
    )
    assignment = (
        record_byte_pair_occurrence_position_measurement_subject_to_act_binding(
            ledger,
            source_material_result_occurrence_identity=source.identity,
            current_coordinates=carried_source,
        )
    )
    carried_assignment = deepcopy(carried_source)
    carried_assignment["subject_to_act_binding_occurrences"][
        assignment.identity
    ] = None
    carried_assignment["through_event_occurrence_identity"] = assignment.identity
    carried_assignment["event_count"] += 1

    act = record_byte_pair_occurrence_position_measurement_act_occurrence(
        ledger,
        binding_event_identity=assignment.identity,
        binding_current_coordinates=carried_assignment,
    )

    assert get_byte_pair_occurrence_position_measurement_act_occurrence(
        ledger, act.identity
    ) == act

    stale_source = deepcopy(carried_source)
    stale_source["material_result_occurrences"] = []
    with pytest.raises(ValueError, match="exact current coordinates"):
        record_byte_pair_occurrence_position_measurement_subject_to_act_binding(
            ledger,
            source_material_result_occurrence_identity=source.identity,
            current_coordinates=stale_source,
        )


def test_assignment_act_and_result_survive_separate_restarts(tmp_path):
    path = tmp_path / "position-occurrence-position.sqlite"
    ledger = SQLiteEventLedger(path)
    source = _source(ledger)
    locality = source.locality_identity
    assignment = record_byte_pair_occurrence_position_measurement_subject_to_act_binding(
        ledger,
        source_material_result_occurrence_identity=source.identity,
        current_coordinates=_standing(ledger, locality),
    )
    assignment_identity = assignment.identity
    ledger.close()

    ledger = SQLiteEventLedger(path)
    assignment = get_byte_pair_occurrence_position_measurement_subject_to_act_binding(
        ledger, assignment_identity
    )
    act = record_byte_pair_occurrence_position_measurement_act_occurrence(
        ledger,
        binding_event_identity=assignment.identity,
        binding_current_coordinates=_standing(ledger, locality),
    )
    act_identity = act.identity
    ledger.close()

    ledger = SQLiteEventLedger(path)
    try:
        result = record_byte_pair_occurrence_position_measurement_result(
            ledger,
            act_occurrence_event_identity=act_identity,
        )
        assert get_recorded_byte_pair_occurrence_position_measurement(
            ledger, result.identity
        ).occurrences[0] == (b"2+", 0, 1)
    finally:
        ledger.close()


def test_reopened_public_result_refuses_a_second_yield(tmp_path):
    path = tmp_path / "position-occurrence-position-duplicate.sqlite"
    ledger = SQLiteEventLedger(path)
    _source_event, _assignment, act, _result = _record(ledger)
    act_identity = act.identity
    ledger.close()

    reopened = SQLiteEventLedger(path)
    try:
        before = reopened.append_boundary()
        with pytest.raises(ValueError, match="already carries a Yield"):
            record_byte_pair_occurrence_position_measurement_result(
                reopened,
                act_occurrence_event_identity=act_identity,
            )
        assert reopened.append_boundary() == before
    finally:
        reopened.close()


def test_same_call_result_carry_equals_full_standing_replay():
    ledger = EventLedger()
    source = _source(ledger)
    locality = source.locality_identity
    assignment = record_byte_pair_occurrence_position_measurement_subject_to_act_binding(
        ledger,
        source_material_result_occurrence_identity=source.identity,
        current_coordinates=_standing(ledger, locality),
    )
    act = record_byte_pair_occurrence_position_measurement_act_occurrence(
        ledger,
        binding_event_identity=assignment.identity,
        binding_current_coordinates=_standing(ledger, locality),
    )
    before_result = _standing(ledger, locality)
    result = record_byte_pair_occurrence_position_measurement_result(
        ledger,
        act_occurrence_event_identity=act.identity,
    )

    carried = _carry_byte_pair_occurrence_position_measurement_result_into_current_coordinates(
        ledger,
        before_result,
        result,
        prior_through_event_occurrence_identity=act.identity,
    )

    assert carried == _standing(ledger, locality)


def test_refused_same_call_result_does_not_change_prior_current_coordinates():
    ledger = EventLedger()
    source = _source(ledger)
    locality = source.locality_identity
    binding = record_byte_pair_occurrence_position_measurement_subject_to_act_binding(
        ledger,
        source_material_result_occurrence_identity=source.identity,
        current_coordinates=_standing(ledger, locality),
    )
    act = record_byte_pair_occurrence_position_measurement_act_occurrence(
        ledger,
        binding_event_identity=binding.identity,
        binding_current_coordinates=_standing(ledger, locality),
    )
    prior = _standing(ledger, locality)
    unchanged = deepcopy(prior)
    result = record_byte_pair_occurrence_position_measurement_result(
        ledger,
        act_occurrence_event_identity=act.identity,
    )
    malformed = deepcopy(result)
    malformed.material["result_identity"] = "different"

    with pytest.raises(ValueError):
        _carry_byte_pair_occurrence_position_measurement_result_into_current_coordinates(
            ledger,
            prior,
            malformed,
            prior_through_event_occurrence_identity=act.identity,
        )

    assert prior == unchanged


def _assert_position_assertion_movement_requires_its_exact_source(
    trigger_kind, result_occurrences
):
    ledger = MovementSourceChangeLedger()
    _source_event, _assignment, _act, result = _record(
        ledger, exact=b"4\n", locality="calculator-result"
    )
    reference = references_to_recorded_position_coordinates_of_byte_pair_occurrences(
        ledger, result.identity
    )[0]
    ledger.source_event_identity = result.identity
    ledger.trigger_kind = trigger_kind

    with pytest.raises((ByteMeasurementError, ValueError)):
        move_recorded_position_assertion_to_locality(
            ledger,
            source_assertion_reference=reference.assertion_reference,
            destination_locality="calculator-relation-construction",
        )

    assert ledger.changed is True
    assert len(
        tuple(
            ledger.iter_locality_kind(
                "calculator-relation-construction",
                ASSERTION_LOCALITY_MOVEMENT_KIND,
            )
        )
    ) == result_occurrences


def test_position_assertion_movement_requires_its_exact_source_after_subject_to_act_binding():
    _assert_position_assertion_movement_requires_its_exact_source(
        ASSERTION_LOCALITY_MOVEMENT_SUBJECT_TO_ACT_BINDING_KIND,
        0,
    )


def test_position_assertion_movement_requires_its_exact_source_after_act_occurrence():
    _assert_position_assertion_movement_requires_its_exact_source(
        ASSERTION_LOCALITY_MOVEMENT_ACT_OCCURRENCE_EVENT,
        0,
    )


def test_position_assertion_movement_requires_its_exact_source_after_yield_relation():
    _assert_position_assertion_movement_requires_its_exact_source(
        RECORDED_YIELD_RELATION_EVENT,
        0,
    )


def test_position_assertion_movement_requires_its_exact_source_when_carrying_the_result_into_standing():
    _assert_position_assertion_movement_requires_its_exact_source(
        ASSERTION_LOCALITY_MOVEMENT_KIND,
        1,
    )


def test_result_carries_only_its_declared_measurement_coordinates():
    ledger = EventLedger()
    _source_event, assignment, _act, result = _record(ledger)

    assert result.kind == BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND
    assert set(result.material) == {
        "result_identity",
        "addressed_act_identity",
        "act_occurrence_identity",
        "exact_act",
        "subject_to_act_binding_reference",
        "input_relation",
        "source_localities",
        "source_material_result_occurrence_identity",
        "completeness_boundary",
        "assertions",
        "act_occurrence_event_identity",
        "yield_relation_identity",
    }
    assert "standing" not in assignment.material["input_relation"]
    assert "standing" not in result.material["assertions"]["dimensions"]




FIDELITY_DISTINCTIONS = {
    ("book_coordinates", "01.Source.D", "result"): (
        test_each_input_pair_has_first_and_second_exact_position_coordinates,
        test_same_pair_material_at_distinct_positions_remains_distinct_occurrences,
        test_material_without_a_byte_pair_yields_an_exact_empty_result,
        test_result_refuses_changed_assertion_coordinates,
        test_references_preserve_every_exact_pair_occurrence,
        test_addressed_references_use_requested_result_local_positions,
        test_full_reference_reader_does_not_construct_the_occurrence_tuple,
        test_exact_addressed_source_position_reads_only_its_carried_pair_references,
        test_addressed_source_position_preserves_exact_boundaries,
        test_addressed_source_position_refuses_a_changed_coordinate,
        test_equal_byte_material_at_distinct_positions_has_distinct_coordinates,
        test_addressed_source_position_from_another_exact_result_is_refused,
        test_result_carries_only_its_declared_measurement_coordinates,
    ),
}
