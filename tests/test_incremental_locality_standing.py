"""Advancing locality Standing equals replaying it, at every occurrence boundary.

The console projected locality Standing from the first event of the locality
before every interaction, so occurrence *j* was reprojected by every later one.
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

FIDELITY_SUBJECT = "current_Locality_Standing"

from seed_runtime.events import EventLedger, SQLiteEventLedger
from seed_runtime.operator_locality_standing import (
    advance_operator_locality_standing,
    read_operator_locality_standing,
)
from seed_runtime.operator_console import run_persistent_operator_console
from seed_runtime.material_ingest import MATERIAL_INGEST_OCCURRED_KIND
from seed_runtime.material_ingest import ingest_material
from seed_runtime.byte_measurement import (
    record_byte_measurement_responsible_act_evidence,
    record_byte_measurement_result,
)
from seed_runtime.supplied_invocation_material import (
    SuppliedSystemMaterialOccurrence,
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


def _ingress_event(index, *, unknown):
    """One recorded ingest occurrence carrying distinct Unknown."""
    ledger = EventLedger()
    return ledger.append(
        MATERIAL_INGEST_OCCURRED_KIND,
        {
            "dimensions": {
                "identity": f"material_{index}",
                "authority": "unestablished",
                "content": "00",
            },
            "source_role": "operator",
            "unknown": list(unknown),
        },
        locality_identity="s",
    )


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
    """Two Representation occurrences, then three ingest occurrences, repeating."""
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
                MATERIAL_INGEST_OCCURRED_KIND,
                {
                    "dimensions": {
                        "identity": "first",
                        "authority": "unestablished",
                    },
                    "source_role": "operator",
                },
                locality_identity="s",
            )
            second = ledger.append(
                MATERIAL_INGEST_OCCURRED_KIND,
                {
                    "dimensions": {
                        "identity": "second",
                        "authority": "unestablished",
                    },
                    "source_role": "operator",
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
        MATERIAL_INGEST_OCCURRED_KIND,
        {
            "dimensions": {
                "identity": "elsewhere",
                "authority": "unestablished",
            },
            "source_role": "operator",
        },
        locality_identity="elsewhere",
    )

    with pytest.raises(ValueError, match="not in this Locality"):
        advance_operator_locality_standing(
            ledger,
            (event.identity,),
            locality_identity="s",
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
    from seed_runtime import operator_console

    original = operator_console.read_operator_locality_standing

    def record(ledger, **kwargs):
        calls.append(len(ledger.list_locality(kwargs["locality_identity"])))
        return original(ledger, **kwargs)

    monkeypatch.setattr(operator_console, "read_operator_locality_standing", record)
    _console("alpha\nbeta\ngamma\ndelta\n")
    assert calls == [0]


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
    # One identity for Ingest or the separately observable byte Measurement
    # Act Evidence, two for its Yield/result, three for occurrence-position
    # Measurement, four for a record-only Representation, six for the distinct
    # pair-input Applicability and pair Measurement lifecycles, and all ten
    # exact identities for a successful raw Representation lifecycle. No call
    # grows with the ledger.
    assert set(sizes) <= {1, 2, 3, 4, 6, 10}, sizes


def test_fresh_pair_measurement_is_not_reread_when_it_enters_standing(monkeypatch):
    from seed_runtime import byte_measurement, operator_console

    ledger = EventLedger()
    ingest_material(
        ledger,
        locality_identity="s",
        exact_bytes=b"abab",
        source_role="material witness",
        source_boundary="exact pair material",
    )
    measurement_act = record_byte_measurement_responsible_act_evidence(
        ledger,
        source_localities=("s",),
        recording_locality_identity="s",
    )
    measurement = record_byte_measurement_result(
        ledger,
        responsible_act_evidence_event_identity=measurement_act.identity,
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
    assert reads == [pair_measurement.identity]
    with pytest.raises(ValueError, match="follow its carried Act and Yield"):
        operator_console._carry_recorded_pair_measurement_into_standing(
            dict(standing),
            pair_measurement,
            prior_through_event_occurrence_identity="crossed-boundary",
        )
    with pytest.raises(ValueError, match="Standing is not exact"):
        operator_console._carry_recorded_pair_measurement_into_standing(
            standing,
            pair_measurement,
            prior_through_event_occurrence_identity=pair_measurement.identity,
        )


def test_fresh_pair_measurement_is_not_reread_to_address_its_representation(
    monkeypatch,
):
    from seed_runtime import byte_measurement, operator_console
    from seed_runtime.operator_representation import (
        _record_operator_representation_from_recorded_pair_measurement,
        record_operator_representation,
    )

    ledger = EventLedger()
    ingest_material(
        ledger,
        locality_identity="s",
        exact_bytes=b"abab",
        source_role="material witness",
        source_boundary="exact pair material",
    )
    measurement_act = record_byte_measurement_responsible_act_evidence(
        ledger,
        source_localities=("s",),
        recording_locality_identity="s",
    )
    measurement = record_byte_measurement_result(
        ledger,
        responsible_act_evidence_event_identity=measurement_act.identity,
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
    later_boundary = ingest_material(
        ledger,
        locality_identity="s",
        exact_bytes=b"later material",
        source_role="material witness",
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
        _record_operator_material_acquire_responsible_act_evidence_from_assignment,
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
    ingest_material(
        ledger,
        locality_identity="s",
        exact_bytes=b"abab",
        source_role="material witness",
        source_boundary="exact pair material",
    )
    measurement_act = record_byte_measurement_responsible_act_evidence(
        ledger,
        source_localities=("s",),
        recording_locality_identity="s",
    )
    measurement = record_byte_measurement_result(
        ledger,
        responsible_act_evidence_event_identity=measurement_act.identity,
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
    act_evidence = (
        _record_operator_material_acquire_responsible_act_evidence_from_assignment(
            ledger,
            responsibility_assignment=assignment,
            responsibility_assignment_standing=standing,
        )
    )
    standing = _carry_operator_material_acquisition_occurrence_into_standing(
        standing,
        act_evidence,
        prior_through_event_occurrence_identity=assignment.identity,
    )
    assert representation_reads == []
    acquired = record_operator_material_acquire_result(
        ledger,
        responsible_act_evidence_event_identity=act_evidence.identity,
        boundary_material=OperatorBoundaryMaterial(
            exact_bytes=b"next material",
            eof=False,
            material_boundary="next boundary",
            known_loss=(),
        ),
    )
    unchanged = deepcopy(standing)
    malformed = deepcopy(acquired)
    malformed.material["unknown"] = "not exact"
    with pytest.raises(ValueError, match="Standing is not exact"):
        _carry_operator_material_acquisition_occurrence_into_standing(
            standing,
            malformed,
            prior_through_event_occurrence_identity=act_evidence.identity,
        )
    assert standing == unchanged
    standing = _carry_operator_material_acquisition_occurrence_into_standing(
        standing,
        acquired,
        prior_through_event_occurrence_identity=act_evidence.identity,
    )

    assert representation_reads == [representation["representation_event_identity"]]
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
def test_each_console_road_leaves_incremental_standing_equal_to_replay(
    monkeypatch, material, raw, existing_locality
):
    from seed_runtime import operator_console

    ledger = EventLedger()
    if existing_locality:
        ledger.append(
            MATERIAL_INGEST_OCCURRED_KIND,
            {
                "dimensions": {
                    "identity": "existing-material",
                    "authority": "unestablished",
                },
                "source_role": "operator",
                "unknown": [],
            },
            exact_material=b"existing material",
            locality_identity="existing",
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
    for locality_identity, incremental in observed.items():
        assert incremental == read_operator_locality_standing(
            ledger, locality_identity=locality_identity
        )


@pytest.mark.parametrize("failure", ("write", "flush"))
def test_a_failed_console_emission_advances_every_recorded_occurrence(
    monkeypatch, failure
):
    from seed_runtime import operator_console

    class FailedBoundary(BytesIO):
        def write(self, value):
            if failure == "write":
                super().write(value[:-1])
                return len(value) - 1
            return super().write(value)

        def flush(self):
            if failure == "flush":
                raise OSError("flush failed")
            return super().flush()

    ledger = EventLedger()
    observed = []
    original = operator_console._advance_over_representation

    def record(ledger, standing, representation):
        advanced = original(ledger, standing, representation)
        observed.append(advanced)
        return advanced

    monkeypatch.setattr(operator_console, "_advance_over_representation", record)
    error = ValueError if failure == "write" else OSError
    with pytest.raises(error):
        run_persistent_operator_console(
            ledger=ledger,
            locality_identity="s",
            input_stream=binary_input(b"!ls\n"),
            output_stream=StringIO(),
            raw_output_stream=FailedBoundary(),
            operator_invocation_provider=lambda _command, supply: supply(
                SuppliedSystemMaterialOccurrence(
                    b"exact raw material\n",
                    "invocation output occurrence 0",
                    True,
                )
            ),
        )

    system_locality_identity = next(
        event.locality_identity
        for event in ledger.list()
        if event.kind == "operator.invocation_locality_recorded"
    )
    assert observed[-1] == read_operator_locality_standing(
        ledger, locality_identity=system_locality_identity
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
    before = len(prior["ingest_occurrences"])
    prefix.extend(events[5:])
    advanced = _advance(events[5:], prior=prior, ledger=prefix)
    assert advanced["ingest_occurrences"] is prior["ingest_occurrences"]
    assert len(prior["ingest_occurrences"]) >= before


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
        "ingest_occurrences",
        "measurement_occurrences",
        "exact_result_occurrences",
        "operator_material_acquire_act_occurrences",
        "recorded_standing_boundary_references",
        "recorded_standing_boundary_locality_relations",
        "known_loss",
        "unknown",
        "conflicts",
    ):
        assert advanced[coordinate] is prior[coordinate], coordinate


def test_a_growing_unknown_set_does_not_reintroduce_per_advance_copying():
    """Distinct Unknown per occurrence, which acquisition would yield."""
    standing = _advance([])
    held = standing["unknown"]
    for index in range(200):
        event = _ingress_event(index, unknown=[f"unknown {index}"])
        standing = _advance([event], prior=standing)
        # The same sequence throughout: never rebuilt, never re-sorted into a
        # new object, however many distinct values accumulate.
        assert standing["unknown"] is held
    assert len(standing["unknown"]) == 200
    assert standing["unknown"] == sorted(standing["unknown"])
    assert len(set(standing["unknown"])) == 200


def test_repeated_values_are_recorded_once():
    standing = _advance([])
    for index in range(5):
        standing = _advance(
            [_ingress_event(index, unknown=["one repeated unknown"])],
            prior=standing,
        )
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
    assert kinds.count(MATERIAL_INGEST_OCCURRED_KIND) == 2
    assert kinds.count("operator.representation.recorded") == 5
    assert kinds.count("operator.representation.emitted") == 0
    assert output == ""
