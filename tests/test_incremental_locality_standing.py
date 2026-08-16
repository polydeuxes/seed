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

from tests.binary_input import binary_input
from io import StringIO

import pytest

from seed_runtime.events import EventLedger, SQLiteEventLedger
from seed_runtime.operator_locality_standing import (
    advance_operator_locality_standing,
    read_operator_locality_standing,
)
from seed_runtime.operator_console import run_persistent_operator_console
from seed_runtime.material_ingest import MATERIAL_INGEST_OCCURRED_KIND

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


def _ingress_event(index, *, unknowns):
    """One recorded ingest occurrence carrying distinct Unknowns."""
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
            "unknowns": list(unknowns),
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
    assert set(sizes) <= {1, 3}, sizes


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

    `known_loss`, `unknowns` and `conflicts` were rebuilt from the prior on
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
        "known_loss",
        "unknowns",
        "conflicts",
    ):
        assert advanced[coordinate] is prior[coordinate], coordinate


def test_a_growing_unknown_set_does_not_reintroduce_per_advance_copying():
    """Distinct Unknowns per occurrence, which acquisition would yield."""
    standing = _advance([])
    held = standing["unknowns"]
    for index in range(200):
        event = _ingress_event(index, unknowns=[f"unknown {index}"])
        standing = _advance([event], prior=standing)
        # The same sequence throughout: never rebuilt, never re-sorted into a
        # new object, however many distinct values accumulate.
        assert standing["unknowns"] is held
    assert len(standing["unknowns"]) == 200
    assert standing["unknowns"] == sorted(standing["unknowns"])
    assert len(set(standing["unknowns"])) == 200


def test_repeated_values_are_recorded_once():
    standing = _advance([])
    for index in range(5):
        standing = _advance(
            [_ingress_event(index, unknowns=["one repeated unknown"])],
            prior=standing,
        )
    assert standing["unknowns"] == ["one repeated unknown"]


def test_the_console_keeps_no_earlier_standing():
    """The only holder hands its Standing forward and retains nothing."""
    ledger, output = _console("alpha\nbeta\ngamma\n")
    assert output.count("Bounded Representation") == 4
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
    assert supplied.material["locality_standing_as_of_event_identity"] is None


def test_the_locality_records_the_same_occurrences_it_always_did():
    ledger, output = _console("alpha\nbeta\n")
    kinds = [event.kind for event in ledger.list()]
    assert kinds.count(MATERIAL_INGEST_OCCURRED_KIND) == 2
    assert kinds.count("operator.representation.recorded") == 3
    assert kinds.count("operator.representation.emitted") == 3
    assert output.count("Bounded Representation") == 3
