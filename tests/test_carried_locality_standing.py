"""Advancing locality Standing matches replaying it at every occurrence boundary.

The console rebuilt Locality Standing before every interaction, so each later
interaction reread occurrence *j*.
`#2376` established that advancing a prior Standing over only the occurrences
after its boundary yields exactly the replayed result across 1,077 prefix
pairs. The console now carries its Standing forward instead.

**The guard is equivalence, not speed.** Every advance below is compared
against replay from zero through the same boundary. Timing is asserted nowhere;
`test_the_console_never_replays_the_session` pins the architecture directly.

The advance takes over its prior rather than copying it. Standing grows with the
locality, so a copy per advance would cost the locality event count every time and
reinstate the quadratic this replaced. That contract is exercised here so it
cannot be softened by accident.
"""

from __future__ import annotations

from copy import deepcopy
from tests.binary_input import binary_input
from io import BytesIO, StringIO

import pytest


from seed_runtime.events import EventLedger, SQLiteEventLedger
from seed_runtime.operator_locality_standing import (
    _record_distinct,
    advance_operator_locality_standing,
    read_operator_locality_standing,
    read_operator_locality_standing_through,
)
from seed_runtime.operator_console import run_persistent_operator_console
from seed_runtime.operator_material_acquisition import (
    OPERATOR_MATERIAL_ACQUIRE_RECORDED_KIND,
)
from seed_runtime.witness_material_acquisition import WITNESS_MATERIAL_ACQUISITION_RECORDED_KIND
from seed_runtime.witness_material_acquisition import record_witness_material_acquisition
from seed_runtime.material_acquisition import MaterialAcquisitionError
from seed_runtime.measurement_of_position_coordinates_of_byte_pair_occurrences import (
    BYTE_PAIR_OCCURRENCE_POSITION_ASSIGNMENT_KIND,
    BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND,
    references_to_recorded_position_coordinates_of_byte_pair_occurrences,
)
from seed_runtime.byte_measurement import (
    BYTE_MEASUREMENT_RECORDED_KIND,
    BYTE_MEASUREMENT_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND,
    assertions_of_recorded_byte_position_pair_measurement,
    record_byte_measurement_responsibility_assignment,
    record_byte_measurement_act_occurrence,
    record_byte_measurement_result,
    record_byte_position_pair_count_layer,
)
from seed_runtime.declared_measurement_responsibilities import (
    ExactByteOccurrenceMeasurementSubject,
    PositionCoordinateMeasurementSubject,
    _discover_byte_measurements,
    _discover_direct_measurements,
    _record_byte_measurement,
    _record_direct_measurement,
    _record_declared_measurements_from_carried_bounded_locality_replay,
    record_declared_measurements_from_current_bounded_locality_replay,
)
from seed_runtime.supplied_invocation_material import (
    SuppliedWitnessMaterialOccurrence,
)
from tests.operator_material_acquisition_test_witness import (
    record_operator_material_occurrence,
)

MATERIALS = (
    "alpha\nbeta\ngamma\n",
    "alpha\n\n\nbeta\n",
    "ünïcode ✓\nnaïve\n",
    'def greet(name):\n    return "Hello " + name\n',
    "only\n",
    "",
)


def _console(material, ledger=None):
    ledger = ledger if ledger is not None else EventLedger()
    output = StringIO()
    run_persistent_operator_console(
        ledger=ledger,
        locality_identity="s",
        input_stream=binary_input(material),
        output_stream=output,
    )
    return ledger, output.getvalue()


def _replay(events):
    ledger = EventLedger()
    ledger.extend(events)
    return read_operator_locality_standing(ledger, locality_identity="s")


def test_operator_acquisition_records_exact_byte_pair_occurrence_position_result():
    ledger, _output = _console("2+2=5\n")
    results = tuple(
        event
        for event in ledger.list()
        if event.kind == BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND
    )

    assert len(results) == 1
    references = (
        references_to_recorded_position_coordinates_of_byte_pair_occurrences(
            ledger, results[0].identity
        )
    )
    assert tuple(
        (reference.exact_pair, reference.first_position, reference.second_position)
        for reference in references
    ) == (
        (b"2+", 0, 1),
        (b"+2", 1, 2),
        (b"2=", 2, 3),
        (b"=5", 3, 4),
        (b"5\n", 4, 5),
    )


def test_declared_measurement_assignments_share_one_responsible_boundary():
    ledger = EventLedger()
    record_operator_material_occurrence(
        ledger,
        locality_identity="s",
        exact=b"first\n",
        source_boundary="first operator boundary",
    )
    record_operator_material_occurrence(
        ledger,
        locality_identity="s",
        exact=b"second\n",
        source_boundary="second operator boundary",
    )
    responsible_replay = read_operator_locality_standing(
        ledger, locality_identity="s"
    )
    responsible_boundary = responsible_replay[
        "through_event_occurrence_identity"
    ]

    recorded = record_declared_measurements_from_current_bounded_locality_replay(
        ledger,
        locality_identity="s",
    )
    assignments = tuple(
        event
        for event in ledger.list_locality("s")
        if event.kind
        in {
            BYTE_PAIR_OCCURRENCE_POSITION_ASSIGNMENT_KIND,
            BYTE_MEASUREMENT_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND,
        }
    )

    assert len(assignments) == 3
    assert {
        assignment.material["standing_boundary_identity"]
        for assignment in assignments
    } == {responsible_boundary}
    responsible_completeness_boundary = ledger.append_boundary_through_occurrence(
        responsible_boundary
    ).identity
    assert {
        assignment.material["completeness_boundary_identity"]
        for assignment in assignments
        if assignment.kind
        == BYTE_MEASUREMENT_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND
    } == {responsible_completeness_boundary}
    assert tuple(result.kind for result in recorded.result_occurrences) == (
        BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND,
        BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND,
        BYTE_MEASUREMENT_RECORDED_KIND,
    )
    assert recorded.bounded_locality_replay == read_operator_locality_standing(
        ledger, locality_identity="s"
    )


def test_recording_order_does_not_change_each_assignment_responsible_boundary(
    monkeypatch,
):
    from seed_runtime import declared_measurement_responsibilities

    monkeypatch.setattr(
        declared_measurement_responsibilities,
        "DECLARED_MEASUREMENT_RESPONSIBILITIES",
        tuple(
            reversed(
                declared_measurement_responsibilities.DECLARED_MEASUREMENT_RESPONSIBILITIES
            )
        ),
    )
    ledger = EventLedger()
    record_operator_material_occurrence(
        ledger,
        locality_identity="s",
        exact=b"material\n",
        source_boundary="operator boundary",
    )
    responsible_boundary = read_operator_locality_standing(
        ledger, locality_identity="s"
    )["through_event_occurrence_identity"]

    recorded = record_declared_measurements_from_current_bounded_locality_replay(
        ledger,
        locality_identity="s",
    )
    assignments = tuple(
        event
        for event in ledger.list_locality("s")
        if event.kind
        in {
            BYTE_PAIR_OCCURRENCE_POSITION_ASSIGNMENT_KIND,
            BYTE_MEASUREMENT_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND,
        }
    )

    assert tuple(result.kind for result in recorded.result_occurrences) == (
        BYTE_MEASUREMENT_RECORDED_KIND,
        BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND,
    )
    assert {
        assignment.material["standing_boundary_identity"]
        for assignment in assignments
    } == {responsible_boundary}


def test_supplied_witness_acquisition_records_declared_measurements_from_locality():
    ledger = EventLedger()

    def provide(_command, supply):
        supply(
            SuppliedWitnessMaterialOccurrence(
                b"4\n",
                "invocation output occurrence 0",
            )
        )
        supply(
            SuppliedWitnessMaterialOccurrence(
                b"",
                "invocation completion",
            )
        )

    run_persistent_operator_console(
        ledger=ledger,
        locality_identity="s",
        input_stream=binary_input(b"!calculator 2+2\n"),
        output_stream=StringIO(),
        raw_output_stream=BytesIO(),
        operator_invocation_provider=provide,
    )
    invocation_locality = next(
        event.material["destination_locality_identity"]
        for event in ledger.list()
        if event.kind == "operator.invocation_locality_recorded"
    )
    supplied = tuple(
        event
        for event in ledger.list()
        if event.kind == WITNESS_MATERIAL_ACQUISITION_RECORDED_KIND
        and event.locality_identity == invocation_locality
    )
    results = tuple(
        event
        for event in ledger.list()
        if event.kind == BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND
        and event.locality_identity == invocation_locality
    )

    assert tuple(event.exact_material for event in supplied) == (b"4\n", b"")
    assert len(results) == len(supplied)
    standing = read_operator_locality_standing(
        ledger, locality_identity=invocation_locality
    )
    assert tuple(
        occurrence["result_occurrence_identity"]
        for occurrence in standing["material_acquisition_result_occurrences"]
    ) == tuple(event.identity for event in supplied)
    assert standing["material_locality_relation_occurrences"] == {
        event.identity: {"locality_relation": event.material["locality_relation"]}
        for event in supplied
    }
    assert {result.identity for result in results}.issubset(
        set(standing["measurement_occurrences"])
    )


def test_witness_acquisitions_enter_declared_measurement_through_locality():
    ledger = EventLedger()
    first = record_witness_material_acquisition(
        ledger,
        locality_identity="s",
        exact_bytes=b"first\n",
        source_boundary="first exact boundary",
    )
    second = record_witness_material_acquisition(
        ledger,
        locality_identity="s",
        exact_bytes=b"second\n",
        source_boundary="second exact boundary",
    )

    recorded = record_declared_measurements_from_current_bounded_locality_replay(
        ledger,
        locality_identity="s",
    )

    assert tuple(
        occurrence["result_occurrence_identity"]
        for occurrence in recorded.bounded_locality_replay[
            "material_acquisition_result_occurrences"
        ]
    ) == (first.identity, second.identity)
    assert len(recorded.result_occurrences) == 3
    assert recorded.bounded_locality_replay[
        "material_locality_relation_occurrences"
    ] == {
        event.identity: {"locality_relation": event.material["locality_relation"]}
        for event in (first, second)
    }
    assert recorded.bounded_locality_replay == read_operator_locality_standing(
        ledger, locality_identity="s"
    )

    boundary = ledger.append_boundary()
    again = record_declared_measurements_from_current_bounded_locality_replay(
        ledger,
        locality_identity="s",
    )
    assert again.result_occurrences == ()
    assert ledger.append_boundary() == boundary


def test_witness_locality_exposes_declared_measurement_subjects():
    ledger = EventLedger()
    first = record_witness_material_acquisition(
        ledger,
        locality_identity="s",
        exact_bytes=b"first\n",
        source_boundary="first exact boundary",
    )
    second = record_witness_material_acquisition(
        ledger,
        locality_identity="s",
        exact_bytes=b"second\n",
        source_boundary="second exact boundary",
    )
    standing = read_operator_locality_standing(ledger, locality_identity="s")

    position_subjects = _discover_direct_measurements(ledger, standing, "s")
    byte_subjects = _discover_byte_measurements(ledger, standing, "s")

    assert tuple(
        subject.source_material_acquisition_occurrence_identity
        for subject in position_subjects
    ) == (first.identity, second.identity)
    assert len(byte_subjects) == 1
    assert byte_subjects[0].source_material_acquisition_occurrence_identities == (
        first.identity,
        second.identity,
    )
    boundary = ledger.append_boundary()
    with pytest.raises(
        ValueError, match="exact-byte Measurement requires its exact subject"
    ):
        _record_byte_measurement(ledger, standing, standing, "s", None)
    with pytest.raises(
        ValueError, match="position-coordinate Measurement requires its exact subject"
    ):
        _record_direct_measurement(ledger, standing, standing, "s", None)
    assert ledger.append_boundary() == boundary


def test_exact_byte_measurement_refuses_a_raw_witness_acquisition_result_set():
    ledger = EventLedger()
    first = record_witness_material_acquisition(
        ledger,
        locality_identity="s",
        exact_bytes=b"first\n",
        source_boundary="first exact boundary",
    )
    record_witness_material_acquisition(
        ledger,
        locality_identity="s",
        exact_bytes=b"second\n",
        source_boundary="second exact boundary",
    )
    standing = read_operator_locality_standing(ledger, locality_identity="s")
    incomplete = ExactByteOccurrenceMeasurementSubject((first.identity,))
    boundary = ledger.append_boundary()

    with pytest.raises(
        ValueError,
        match="differs from the current acquisition-result set",
    ):
        _record_byte_measurement(ledger, standing, standing, "s", incomplete)

    assert ledger.append_boundary() == boundary


def test_bounded_replay_exposes_assignments_after_witness_locality():
    ledger = EventLedger()
    record_witness_material_acquisition(
        ledger,
        locality_identity="s",
        exact_bytes=b"Hello, how are you\n",
        source_boundary="operator material occurrence",
    )
    before = read_operator_locality_standing(ledger, locality_identity="s")
    assert before["responsibility_assignment_occurrences"] == {}

    recorded = record_declared_measurements_from_current_bounded_locality_replay(
        ledger,
        locality_identity="s",
    )
    assignments = tuple(
        event
        for event in ledger.list()
        if event.kind
        in {
            BYTE_PAIR_OCCURRENCE_POSITION_ASSIGNMENT_KIND,
            BYTE_MEASUREMENT_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND,
        }
    )

    assert len(assignments) == 2
    assert len(recorded.result_occurrences) == 2
    assert set(recorded.bounded_locality_replay["responsibility_assignment_occurrences"]) == {
        assignment.identity for assignment in assignments
    }
    assert recorded.bounded_locality_replay == read_operator_locality_standing(
        ledger, locality_identity="s"
    )


def test_declared_measurements_refuse_a_material_acquisition_without_exact_yield():
    ledger = EventLedger()
    source = ledger.append(
        WITNESS_MATERIAL_ACQUISITION_RECORDED_KIND,
        {
            "dimensions": {
                "identity": "preserved material",
            },
            "source_role": "this Witness",
            "unknown": [],
        },
        exact_material=b"preserved material",
        locality_identity="s",
    )

    with pytest.raises(
        MaterialAcquisitionError,
        match="Witness material-acquisition result is absent or corrupted",
    ):
        record_declared_measurements_from_current_bounded_locality_replay(
            ledger,
            locality_identity="s",
        )

    assert not tuple(
        event
        for event in ledger.list()
        if event.kind
        in {
            BYTE_MEASUREMENT_RECORDED_KIND,
            BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND,
        }
    )
    assert ledger.get(source.identity) == source


def test_carried_declaration_records_witness_measurements_after_another_locality_append():
    ledger = EventLedger()
    record_witness_material_acquisition(
        ledger,
        locality_identity="s",
        exact_bytes=b"pin\n",
        source_boundary="exact pin boundary",
    )
    standing = read_operator_locality_standing(ledger, locality_identity="s")
    foreign = ledger.append(
        "test.occurrence",
        {"unknown": []},
        locality_identity="another-locality",
    )

    recorded = _record_declared_measurements_from_carried_bounded_locality_replay(
        ledger,
        standing,
        locality_identity="s",
    )

    assert len(recorded.result_occurrences) == 2
    event_identities = tuple(event.identity for event in ledger.list())
    assert event_identities.index(foreign.identity) < event_identities.index(
        recorded.result_occurrences[-1].identity
    )


def test_carried_declaration_refuses_replay_before_the_current_boundary():
    ledger = EventLedger()
    record_witness_material_acquisition(
        ledger,
        locality_identity="s",
        exact_bytes=b"pin\n",
        source_boundary="exact pin boundary",
    )
    standing = read_operator_locality_standing(ledger, locality_identity="s")
    later = ledger.append(
        "test.occurrence",
        {"unknown": []},
        locality_identity="s",
    )

    with pytest.raises(ValueError, match="current bounded Locality replay boundary"):
        _record_declared_measurements_from_carried_bounded_locality_replay(
            ledger,
            standing,
            locality_identity="s",
        )

    assert (
        ledger.append_boundary_through_occurrence(later.identity)
        == ledger.append_boundary()
    )


def test_witness_material_measurements_remain_exhausted_after_sqlite_reopen(tmp_path):
    path = str(tmp_path / "standing-declarations.sqlite")
    ledger = SQLiteEventLedger(path)
    try:
        record_witness_material_acquisition(
            ledger,
            locality_identity="s",
            exact_bytes=b"2+2=5\n",
            source_boundary="exact claim boundary",
        )
        first = record_declared_measurements_from_current_bounded_locality_replay(
            ledger,
            locality_identity="s",
        )
        assert len(first.result_occurrences) == 2
        boundary = ledger.append_boundary()
    finally:
        ledger.close()

    reopened = SQLiteEventLedger(path)
    try:
        second = record_declared_measurements_from_current_bounded_locality_replay(
            reopened,
            locality_identity="s",
        )
        assert second.result_occurrences == ()
        assert reopened.append_boundary() == boundary
        assert second.bounded_locality_replay == read_operator_locality_standing(
            reopened, locality_identity="s"
        )
    finally:
        reopened.close()


def _advance(events, prior=None, *, ledger=None):
    if ledger is None:
        ledger = EventLedger()
        ledger.extend(events)
    return advance_operator_locality_standing(
        ledger,
        (event.identity for event in events),
        locality_identity="s",
        prior=prior,
    )


# --------------------------------------------------------------------------
# Equivalence, at every occurrence boundary.
# --------------------------------------------------------------------------


@pytest.mark.parametrize("material", MATERIALS)
def test_advancing_one_occurrence_at_a_time_equals_replay(material):
    ledger, _ = _console(material)
    events = ledger.list()
    standing = _advance([])
    prefix = EventLedger()
    for index in range(len(events)):
        prefix.extend((events[index],))
        standing = _advance(
            [events[index]], prior=standing, ledger=prefix
        )
        assert standing == _replay(events[: index + 1])


def test_advancing_in_the_console_s_own_groupings_equals_replay():
    """Two Representation occurrences, then three acquisition_result occurrences, repeating."""
    ledger, _ = _console("alpha\nbeta\ngamma\n")
    events = ledger.list()
    standing = _advance([])
    prefix = EventLedger()
    input = 0
    for size in (2, 3, 2, 3, 2, 3, 2):
        batch = events[input : input + size]
        if not batch:
            break
        prefix.extend(batch)
        standing = _advance(batch, prior=standing, ledger=prefix)
        input += len(batch)
        assert standing == _replay(events[:input])


def test_an_advance_over_no_occurrences_changes_nothing():
    ledger, _ = _console("alpha\n")
    events = ledger.list()
    standing = _advance(events)
    assert _advance([], prior=standing) == _replay(events)


def test_replay_still_works_and_agrees_with_a_single_advance():
    for material in MATERIALS:
        ledger, _ = _console(material)
        events = ledger.list()
        assert _advance(events) == _replay(events)
        assert read_operator_locality_standing(
            ledger, locality_identity="s"
        ) == _replay(events)


def test_an_advance_refuses_reversed_exact_occurrences(tmp_path):
    ledgers = (
        EventLedger(),
        SQLiteEventLedger(str(tmp_path / "reversed.sqlite")),
    )
    try:
        for ledger in ledgers:
            first = ledger.append(
                WITNESS_MATERIAL_ACQUISITION_RECORDED_KIND,
                {
                    "dimensions": {
                        "identity": "first",
                    },
                    "source_role": "this Witness",
                },
                locality_identity="s",
            )
            second = ledger.append(
                WITNESS_MATERIAL_ACQUISITION_RECORDED_KIND,
                {
                    "dimensions": {
                        "identity": "second",
                    },
                    "source_role": "this Witness",
                },
                locality_identity="s",
            )

            with pytest.raises(ValueError, match="not in append order"):
                advance_operator_locality_standing(
                    ledger,
                    (second.identity, first.identity),
                    locality_identity="s",
                )
    finally:
        ledgers[1].close()


def test_an_advance_refuses_an_occurrence_from_another_locality():
    ledger = EventLedger()
    event = ledger.append(
        WITNESS_MATERIAL_ACQUISITION_RECORDED_KIND,
        {
            "dimensions": {
                "identity": "elsewhere",
            },
            "source_role": "this Witness",
        },
        locality_identity="elsewhere",
    )

    with pytest.raises(ValueError, match="not in this Locality"):
        advance_operator_locality_standing(
            ledger,
            (event.identity,),
            locality_identity="s",
        )


def test_input_boundary_cannot_append_an_occurrence_during_acquisition():
    ledger = EventLedger()

    class AppendingInput:
        def readline(self):
            record_witness_material_acquisition(
                ledger,
                locality_identity="s",
                exact_bytes=b"outside acquisition",
                source_boundary="inside input boundary invocation",
            )
            return b"addressed material\n"

    with pytest.raises(ValueError, match="before its result"):
        run_persistent_operator_console(
            ledger=ledger,
            locality_identity="s",
            input_stream=AppendingInput(),
            output_stream=StringIO(),
        )

    assert all(
        event.kind != OPERATOR_MATERIAL_ACQUIRE_RECORDED_KIND
        for event in ledger.list()
    )


def test_a_persisted_ledger_advances_identically(tmp_path):
    ledger = SQLiteEventLedger(str(tmp_path / "ledger.sqlite"))
    try:
        _console("alpha\nünïcode\n", ledger=ledger)
        events = ledger.list()
        standing = _advance([])
        prefix = EventLedger()
        for index in range(len(events)):
            prefix.extend((events[index],))
            standing = _advance(
                [events[index]], prior=standing, ledger=prefix
            )
        assert standing == _replay(events)
    finally:
        ledger.close()


# --------------------------------------------------------------------------
# The architecture, pinned directly rather than by timing.
# --------------------------------------------------------------------------


def test_the_console_never_replays_the_locality(monkeypatch):
    """One read from nothing recorded, for C0. No replay after that."""
    calls = []
    from seed_runtime import operator_console, operator_locality_standing

    original = operator_locality_standing.read_operator_locality_standing

    def record(ledger, **kwargs):
        calls.append(len(ledger.list_locality(kwargs["locality_identity"])))
        return original(ledger, **kwargs)

    monkeypatch.setattr(
        operator_locality_standing, "read_operator_locality_standing", record
    )
    monkeypatch.setattr(operator_console, "read_operator_locality_standing", record)
    _console("alpha\nbeta\ngamma\ndelta\n")
    assert calls == [0]


def test_incremental_advance_does_not_reconstruct_its_prior_boundary(monkeypatch):
    """A validated prior replay remains the validation input while it advances."""

    from seed_runtime import operator_locality_standing

    ledger = EventLedger()
    record_operator_material_occurrence(
        ledger,
        locality_identity="s",
        exact=b"alpha\n",
        source_boundary="exact operator boundary",
    )
    prior = read_operator_locality_standing(ledger, locality_identity="s")
    assignment = record_byte_measurement_responsibility_assignment(
        ledger,
        source_localities=("s",),
        recording_locality_identity="s",
        locality_standing=prior,
    )

    def refuse(*_args, **_kwargs):
        raise AssertionError("incremental advance reconstructed its prior boundary")

    monkeypatch.setattr(
        operator_locality_standing,
        "read_operator_locality_standing_through",
        refuse,
    )
    advanced = advance_operator_locality_standing(
        ledger,
        (assignment.identity,),
        locality_identity="s",
        prior=prior,
    )
    assert advanced["through_event_occurrence_identity"] == assignment.identity


def test_declared_measurement_discovery_uses_validated_replay_coordinates(
    monkeypatch,
):
    """Discovery does not reconstruct lifecycles already validated into replay."""

    from seed_runtime import (
        measurement_of_position_coordinates_of_byte_pair_occurrences as position_measurement,
        operator_material_acquisition,
    )

    ledger, _output = _console("alpha\nbeta\n")
    replay = read_operator_locality_standing(ledger, locality_identity="s")

    def refuse(*_args, **_kwargs):
        raise AssertionError("declared Measurement reconstructed prior physiology")

    monkeypatch.setattr(position_measurement, "_read_assignment", refuse)
    monkeypatch.setattr(position_measurement, "_read_result", refuse)
    monkeypatch.setattr(
        operator_material_acquisition,
        "read_operator_material_acquire_locality_relation_requirements",
        refuse,
    )

    assert _discover_direct_measurements(ledger, replay, "s") == ()
    assert _discover_byte_measurements(ledger, replay, "s") == ()


def test_the_console_measures_each_occurrence_population_once(monkeypatch):
    """The same-call assignment, Act, and result consume one exact finding."""

    from seed_runtime import occurrence_position_measurement

    calls = []
    original = occurrence_position_measurement._measure_occurrence_position_through

    def record(*args, **kwargs):
        calls.append(kwargs["boundary"])
        return original(*args, **kwargs)

    monkeypatch.setattr(
        occurrence_position_measurement,
        "_measure_occurrence_position_through",
        record,
    )
    _console("alpha\n")
    assert len(calls) == 1


def test_each_advance_reads_only_what_an_act_just_recorded(monkeypatch):
    """Guards against a ledger scan reappearing on the continuation path."""
    from seed_runtime import operator_console

    sizes = []
    original = operator_console.advance_operator_locality_standing

    def record(ledger, event_identities, **kwargs):
        event_identities = list(event_identities)
        sizes.append(len(event_identities))
        return original(ledger, event_identities, **kwargs)

    monkeypatch.setattr(operator_console, "advance_operator_locality_standing", record)
    _console("alpha\nbeta\ngamma\ndelta\n")
    # One identity for material acquisition or the separately observable byte Measurement
    # Act occurrence, two for its Yield/result, three for occurrence-position
    # Measurement, four for a record-only Representation, six for the distinct
    # pair-input Applicability and pair Measurement lifecycles, and all ten
    # exact identities for a successful raw Representation lifecycle. No call
    # grows with the ledger.
    assert set(sizes) <= {1, 2, 3, 4, 6, 10}, sizes


def test_fresh_pair_measurement_is_not_reread_when_it_enters_standing(monkeypatch):
    from seed_runtime import byte_measurement, operator_console

    ledger = EventLedger()
    record_operator_material_occurrence(
        ledger,
        locality_identity="s",
        exact=b"abab",
        source_boundary="exact pair material",
    )
    measurement_assignment = record_byte_measurement_responsibility_assignment(
        ledger,
        source_localities=("s",),
        recording_locality_identity="s",
        locality_standing=read_operator_locality_standing(
            ledger, locality_identity="s"
        ),
    )
    measurement_act = record_byte_measurement_act_occurrence(
        ledger,
        responsibility_assignment_event_identity=measurement_assignment.identity,
        responsibility_assignment_standing=read_operator_locality_standing(
            ledger, locality_identity="s"
        ),
    )
    measurement = record_byte_measurement_result(
        ledger,
        act_occurrence_event_identity=measurement_act.identity,
    )
    standing = read_operator_locality_standing(ledger, locality_identity="s")
    reads = []
    original = byte_measurement._read_recorded_byte_position_pair_measurement

    def record(*args, **kwargs):
        reads.append(args[1])
        return original(*args, **kwargs)

    monkeypatch.setattr(
        byte_measurement,
        "_read_recorded_byte_position_pair_measurement",
        record,
    )
    standing, pair_measurement = operator_console._record_pair_measurement(
        ledger,
        standing,
        byte_measurement_event_identity=measurement.identity,
        locality_identity="s",
    )

    assert reads == []
    assert pair_measurement.identity in standing["measurement_occurrences"]
    assert standing == read_operator_locality_standing(
        ledger, locality_identity="s"
    )
    assert reads == []
    assert assertions_of_recorded_byte_position_pair_measurement(
        ledger, pair_measurement.identity
    )
    assert reads == [pair_measurement.identity]
    assert not hasattr(
        operator_console, "_carry_recorded_pair_measurement_into_standing"
    )


def test_corrupted_pair_assignment_refusal_leaves_carried_standing_unchanged():
    ledger = EventLedger()
    record_operator_material_occurrence(
        ledger,
        locality_identity="s",
        exact=b"abab",
        source_boundary="exact pair material",
    )
    measurement_assignment = record_byte_measurement_responsibility_assignment(
        ledger,
        source_localities=("s",),
        recording_locality_identity="s",
        locality_standing=read_operator_locality_standing(
            ledger, locality_identity="s"
        ),
    )
    measurement_act = record_byte_measurement_act_occurrence(
        ledger,
        responsibility_assignment_event_identity=measurement_assignment.identity,
        responsibility_assignment_standing=read_operator_locality_standing(
            ledger, locality_identity="s"
        ),
    )
    measurement = record_byte_measurement_result(
        ledger, act_occurrence_event_identity=measurement_act.identity
    )
    pair = record_byte_position_pair_count_layer(
        ledger,
        source_measurement_event_identity=measurement.identity,
        recording_locality_identity="s",
    )
    assignment = ledger.get(
        pair.material["responsibility_assignment_reference"][
            "recorded_occurrence_identity"
        ]
    )
    prior = read_operator_locality_standing_through(
        ledger,
        locality_identity="s",
        through_event_occurrence_identity=assignment.material[
            "standing_boundary_identity"
        ],
    )
    unchanged = deepcopy(prior)
    assignment.material["unknown"] = ["forged-partial-standing"]

    with pytest.raises(ValueError, match="assignment coordinates are not exact"):
        advance_operator_locality_standing(
            ledger,
            [assignment.identity],
            locality_identity="s",
            prior=prior,
        )

    assert prior == unchanged


def test_fresh_pair_measurement_is_not_reread_to_address_its_representation(
    monkeypatch,
):
    from seed_runtime import byte_measurement, operator_console
    from seed_runtime.operator_representation import (
        _record_operator_representation_from_recorded_pair_measurement,
        record_operator_representation,
    )

    ledger = EventLedger()
    record_operator_material_occurrence(
        ledger,
        locality_identity="s",
        exact=b"abab",
        source_boundary="exact pair material",
    )
    measurement_assignment = record_byte_measurement_responsibility_assignment(
        ledger,
        source_localities=("s",),
        recording_locality_identity="s",
        locality_standing=read_operator_locality_standing(
            ledger, locality_identity="s"
        ),
    )
    measurement_act = record_byte_measurement_act_occurrence(
        ledger,
        responsibility_assignment_event_identity=measurement_assignment.identity,
        responsibility_assignment_standing=read_operator_locality_standing(
            ledger, locality_identity="s"
        ),
    )
    measurement = record_byte_measurement_result(
        ledger,
        act_occurrence_event_identity=measurement_act.identity,
    )
    standing = read_operator_locality_standing(ledger, locality_identity="s")
    standing, pair_measurement = operator_console._record_pair_measurement(
        ledger,
        standing,
        byte_measurement_event_identity=measurement.identity,
        locality_identity="s",
    )
    reads = []
    original = byte_measurement._read_recorded_byte_position_pair_measurement

    def record(*args, **kwargs):
        reads.append(args[1])
        return original(*args, **kwargs)

    monkeypatch.setattr(
        byte_measurement,
        "_read_recorded_byte_position_pair_measurement",
        record,
    )
    later_boundary = record_witness_material_acquisition(
        ledger,
        locality_identity="s",
        exact_bytes=b"later material",
        source_boundary="later exact boundary",
    )
    standing = _advance([later_boundary], prior=standing, ledger=ledger)
    representation = (
        _record_operator_representation_from_recorded_pair_measurement(
            ledger,
            locality_identity="s",
            locality_standing=standing,
            pair_measurement=pair_measurement,
            carried_standing_boundary=later_boundary,
        )
    )

    assert reads == []
    assert representation["source_occurrence_reference"] == pair_measurement.identity
    independently_validated = record_operator_representation(
        ledger,
        locality_identity="s",
        locality_standing=standing,
        source_occurrence_reference=pair_measurement.identity,
    )
    assert reads == [pair_measurement.identity]
    assert independently_validated["source_occurrence_reference"] == (
        pair_measurement.identity
    )
    with pytest.raises(ValueError, match="just-carried Standing boundary"):
        _record_operator_representation_from_recorded_pair_measurement(
            ledger,
            locality_identity="s",
            locality_standing={
                **standing,
                "through_event_occurrence_identity": measurement.identity,
            },
            pair_measurement=pair_measurement,
        )


def test_fresh_representation_is_carried_until_acquisition_crosses_input(monkeypatch):
    from seed_runtime import (
        byte_measurement,
        operator_console,
        operator_material_acquisition,
    )
    from seed_runtime.operator_material_acquisition import (
        _record_operator_material_acquire_responsibility_assignment_from_carried_representation,
        _record_operator_material_acquire_act_occurrence_from_assignment,
        record_operator_material_acquire_result,
    )
    from seed_runtime.operator_material_boundary import OperatorBoundaryMaterial
    from seed_runtime.operator_locality_standing import (
        _carry_operator_material_acquisition_occurrence_into_standing,
    )
    from seed_runtime.operator_representation import (
        _record_operator_representation_from_recorded_pair_measurement,
    )

    ledger = EventLedger()
    record_operator_material_occurrence(
        ledger,
        locality_identity="s",
        exact=b"abab",
        source_boundary="exact pair material",
    )
    measurement_assignment = record_byte_measurement_responsibility_assignment(
        ledger,
        source_localities=("s",),
        recording_locality_identity="s",
        locality_standing=read_operator_locality_standing(
            ledger, locality_identity="s"
        ),
    )
    measurement_act = record_byte_measurement_act_occurrence(
        ledger,
        responsibility_assignment_event_identity=measurement_assignment.identity,
        responsibility_assignment_standing=read_operator_locality_standing(
            ledger, locality_identity="s"
        ),
    )
    measurement = record_byte_measurement_result(
        ledger,
        act_occurrence_event_identity=measurement_act.identity,
    )
    standing = read_operator_locality_standing(ledger, locality_identity="s")
    standing, pair_measurement = operator_console._record_pair_measurement(
        ledger,
        standing,
        byte_measurement_event_identity=measurement.identity,
        locality_identity="s",
    )
    representation = (
        _record_operator_representation_from_recorded_pair_measurement(
            ledger,
            locality_identity="s",
            locality_standing=standing,
            pair_measurement=pair_measurement,
        )
    )
    standing = operator_console._advance_over_representation(
        ledger, standing, representation
    )
    representation_reads = []
    original = operator_material_acquisition.read_operator_representation

    def record(*args, **kwargs):
        representation_reads.append(args[1])
        return original(*args, **kwargs)

    monkeypatch.setattr(
        operator_material_acquisition,
        "read_operator_representation",
        record,
    )
    assignment = _record_operator_material_acquire_responsibility_assignment_from_carried_representation(
        ledger,
        locality_identity="s",
        representation=representation,
        locality_standing=standing,
    )
    standing = _carry_operator_material_acquisition_occurrence_into_standing(
        standing,
        assignment,
        prior_through_event_occurrence_identity=representation[
            "representation_event_identity"
        ],
    )
    act_occurrence = (
        _record_operator_material_acquire_act_occurrence_from_assignment(
            ledger,
            responsibility_assignment=assignment,
            responsibility_assignment_standing=standing,
        )
    )
    standing = _carry_operator_material_acquisition_occurrence_into_standing(
        standing,
        act_occurrence,
        prior_through_event_occurrence_identity=assignment.identity,
    )
    assert representation_reads == []
    acquired = record_operator_material_acquire_result(
        ledger,
        act_occurrence_event_identity=act_occurrence.identity,
        boundary_material=OperatorBoundaryMaterial(
            exact_bytes=b"next material",
            eof=False,
            material_boundary="next boundary",
            known_loss=(),
        ),
    )
    unchanged = deepcopy(standing)
    for malformed_unknown in ("not exact", [{}]):
        malformed = deepcopy(acquired)
        malformed.material["unknown"] = malformed_unknown
        with pytest.raises(ValueError, match="Standing is not exact"):
            _carry_operator_material_acquisition_occurrence_into_standing(
                standing,
                malformed,
                prior_through_event_occurrence_identity=act_occurrence.identity,
            )
        assert standing == unchanged
    standing = _carry_operator_material_acquisition_occurrence_into_standing(
        standing,
        acquired,
        prior_through_event_occurrence_identity=act_occurrence.identity,
    )

    assert representation_reads.count(
        representation["representation_event_identity"]
    ) == 1
    assert acquired.exact_material == b"next material"
    assert acquired.identity in standing["exact_result_occurrences"]
    with pytest.raises(
        operator_material_acquisition.OperatorMaterialAcquireError,
        match="carried Representation",
    ):
        _record_operator_material_acquire_responsibility_assignment_from_carried_representation(
            ledger,
            locality_identity="s",
            representation={
                **representation,
                "representation_event_identity": pair_measurement.identity,
            },
            locality_standing=standing,
        )


@pytest.mark.parametrize(
    ("material", "raw", "existing_locality"),
    (
        (b"", False, False),
        (b"record-only road\n", False, False),
        (b"\x00\xff raw road\n", True, False),
        (b"/locality\n", False, False),
        (b"/checkpoint\n", False, False),
        (b"/locality existing\n", False, True),
    ),
)
def test_each_console_road_leaves_carried_standing_matching_replay(
    monkeypatch, material, raw, existing_locality
):
    from seed_runtime import operator_console

    ledger = EventLedger()
    if existing_locality:
        record_witness_material_acquisition(
            ledger,
            locality_identity="existing",
            exact_bytes=b"existing material",
            source_boundary="existing exact material test boundary",
        )

    observed = {}
    original = operator_console._advance_over

    def record(ledger, standing, event_identities, *, locality_identity):
        advanced = original(
            ledger,
            standing,
            event_identities,
            locality_identity=locality_identity,
        )
        observed[locality_identity] = advanced
        return advanced

    monkeypatch.setattr(operator_console, "_advance_over", record)
    run_persistent_operator_console(
        ledger=ledger,
        locality_identity="s",
        input_stream=binary_input(material),
        output_stream=StringIO(),
        raw_output_stream=BytesIO() if raw else None,
    )

    assert observed
    for locality_identity, carried in observed.items():
        assert carried == read_operator_locality_standing(
            ledger, locality_identity=locality_identity
        )


def test_supplied_witness_material_does_not_invoke_the_raw_output_boundary(
    monkeypatch,
):
    from seed_runtime import operator_console

    class FailedBoundary(BytesIO):
        def write(self, value):
            pytest.fail(("unexpected raw output write", value))

        def flush(self):
            pytest.fail("unexpected raw output flush")

    ledger = EventLedger()
    observed = []
    original = operator_console._advance_over_representation

    def record(ledger, standing, representation):
        advanced = original(ledger, standing, representation)
        observed.append(advanced)
        return advanced

    monkeypatch.setattr(operator_console, "_advance_over_representation", record)
    run_persistent_operator_console(
        ledger=ledger,
        locality_identity="s",
        input_stream=binary_input(b"!ls\n"),
        output_stream=StringIO(),
        raw_output_stream=FailedBoundary(),
        operator_invocation_provider=lambda _command, supply: supply(
            SuppliedWitnessMaterialOccurrence(
                b"exact raw material\n",
                "invocation output occurrence 0",
            )
        ),
    )

    invocation_locality_identity = next(
        event.locality_identity
        for event in ledger.list()
        if event.kind == "operator.invocation_locality_recorded"
    )
    assert observed[-1] == read_operator_locality_standing(
        ledger, locality_identity=invocation_locality_identity
    )


# --------------------------------------------------------------------------
# The shared-accumulator contract.
# --------------------------------------------------------------------------


def test_the_advance_reads_its_prior():
    """Stated so it cannot be softened into a copy without a deliberate revision.

    Copying per advance would cost the locality event count every time, which is the
    quadratic this replaced.
    """
    ledger, _ = _console("alpha\nbeta\n")
    events = ledger.list()
    prefix = EventLedger()
    prefix.extend(events[:5])
    prior = _advance(events[:5], ledger=prefix)
    before = len(prior["material_acquisition_result_occurrences"])
    prefix.extend(events[5:])
    advanced = _advance(events[5:], prior=prior, ledger=prefix)
    assert advanced["material_acquisition_result_occurrences"] is prior["material_acquisition_result_occurrences"]
    assert len(prior["material_acquisition_result_occurrences"]) >= before


def test_every_growable_accumulator_participates_without_copying():
    """The prior-transfer rule has to hold for all of them, not most of them.

    `known_loss`, `unknown` and `conflicts` were rebuilt from the prior on
    every advance and re-sorted on every return. They do not grow on the five
    live kinds, so the measured path stayed linear, but acquisition would make
    them grow and restore the shape.
    """
    ledger, _ = _console("alpha\nbeta\n")
    events = ledger.list()
    prefix = EventLedger()
    prefix.extend(events[:5])
    prior = _advance(events[:5], ledger=prefix)
    prefix.extend(events[5:])
    advanced = _advance(events[5:], prior=prior, ledger=prefix)
    for coordinate in (
        "representations",
        "material_acquisition_result_occurrences",
        "measurement_occurrences",
        "exact_result_occurrences",
        "operator_material_acquire_act_occurrences",
        "material_locality_relation_occurrences",
        "recorded_standing_boundary_references",
        "recorded_standing_boundary_locality_relations",
        "known_loss",
        "unknown",
        "conflicts",
    ):
        assert advanced[coordinate] is prior[coordinate], coordinate


def test_a_growing_unknown_set_does_not_reintroduce_per_advance_copying():
    """A growing carried Unknown population remains one exact sequence."""
    standing = _advance([])
    held = standing["unknown"]
    for index in range(200):
        _record_distinct(standing["unknown"], f"unknown {index}")
        standing = _advance([], prior=standing)
        # The same sequence throughout: never rebuilt, never re-sorted into a
        # new object, however many distinct values accumulate.
        assert standing["unknown"] is held
    assert len(standing["unknown"]) == 200
    assert standing["unknown"] == sorted(standing["unknown"])
    assert len(set(standing["unknown"])) == 200


def test_repeated_values_are_recorded_once():
    standing = _advance([])
    for _index in range(5):
        _record_distinct(standing["unknown"], "one repeated unknown")
        standing = _advance([], prior=standing)
    assert standing["unknown"] == ["one repeated unknown"]


def test_the_console_keeps_no_earlier_standing():
    """The only holder hands its Standing forward and retains nothing."""
    ledger, output = _console("alpha\nbeta\ngamma\n")
    assert output == ""
    assert read_operator_locality_standing(
        ledger, locality_identity="s"
    ) == _replay(ledger.list())


# --------------------------------------------------------------------------
# Behaviour that must not have different.
# --------------------------------------------------------------------------


def test_c0_still_forms_from_empty_standing():
    ledger, _ = _console("")
    supplied = next(
        event
        for event in ledger.list()
        if event.kind == "operator.representation.recorded"
    )
    assert supplied.material["locality_standing_through_event_occurrence_identity"] is None


def test_the_locality_records_only_responsible_representation_occurrences():
    ledger, output = _console("alpha\nbeta\n")
    kinds = [event.kind for event in ledger.list()]
    assert kinds.count(OPERATOR_MATERIAL_ACQUIRE_RECORDED_KIND) == 2
    assert kinds.count("operator.representation.recorded") == 5
    assert kinds.count("operator.representation.emitted") == 0
    assert output == ""


PYTEST_ADMISSION = (
    test_operator_acquisition_records_exact_byte_pair_occurrence_position_result,
    test_declared_measurement_assignments_share_one_responsible_boundary,
    test_recording_order_does_not_change_each_assignment_responsible_boundary,
    test_supplied_witness_acquisition_records_declared_measurements_from_locality,
    test_witness_acquisitions_enter_declared_measurement_through_locality,
    test_witness_locality_exposes_declared_measurement_subjects,
    test_exact_byte_measurement_refuses_a_raw_witness_acquisition_result_set,
    test_bounded_replay_exposes_assignments_after_witness_locality,
    test_declared_measurements_refuse_a_material_acquisition_without_exact_yield,
    test_carried_declaration_records_witness_measurements_after_another_locality_append,
    test_carried_declaration_refuses_replay_before_the_current_boundary,
    test_witness_material_measurements_remain_exhausted_after_sqlite_reopen,
    test_advancing_one_occurrence_at_a_time_equals_replay,
    test_advancing_in_the_console_s_own_groupings_equals_replay,
    test_an_advance_over_no_occurrences_changes_nothing,
    test_replay_still_works_and_agrees_with_a_single_advance,
    test_an_advance_refuses_reversed_exact_occurrences,
    test_an_advance_refuses_an_occurrence_from_another_locality,
    test_input_boundary_cannot_append_an_occurrence_during_acquisition,
    test_a_persisted_ledger_advances_identically,
    test_the_console_never_replays_the_locality,
    test_incremental_advance_does_not_reconstruct_its_prior_boundary,
    test_declared_measurement_discovery_uses_validated_replay_coordinates,
    test_the_console_measures_each_occurrence_population_once,
    test_each_advance_reads_only_what_an_act_just_recorded,
    test_fresh_pair_measurement_is_not_reread_when_it_enters_standing,
    test_corrupted_pair_assignment_refusal_leaves_carried_standing_unchanged,
    test_fresh_pair_measurement_is_not_reread_to_address_its_representation,
    test_fresh_representation_is_carried_until_acquisition_crosses_input,
    test_each_console_road_leaves_carried_standing_matching_replay,
    test_supplied_witness_material_does_not_invoke_the_raw_output_boundary,
    test_the_advance_reads_its_prior,
    test_every_growable_accumulator_participates_without_copying,
    test_a_growing_unknown_set_does_not_reintroduce_per_advance_copying,
    test_repeated_values_are_recorded_once,
    test_the_console_keeps_no_earlier_standing,
    test_c0_still_forms_from_empty_standing,
    test_the_locality_records_only_responsible_representation_occurrences,
)
