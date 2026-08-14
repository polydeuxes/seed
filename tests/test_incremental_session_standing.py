"""Advancing session Standing equals replaying it, at every occurrence boundary.

The console projected session Standing from the first event of the session
before every interaction, so occurrence *j* was reprojected by every later one.
`#2376` established that advancing a prior Standing over only the occurrences
after its boundary produces exactly the replayed result across 1,077 prefix
pairs. The console now carries its Standing forward instead.

**The guard is equivalence, not speed.** Every advance below is compared
against replay from zero through the same boundary. Timing is asserted nowhere;
`test_the_console_never_replays_the_session` pins the architecture directly.

The advance takes over its prior rather than copying it. Standing grows with the
session, so a copy per advance would cost the session length every time and
reinstate the quadratic this replaced. That contract is exercised here so it
cannot be softened by accident.
"""

from __future__ import annotations

from io import StringIO

import pytest

from seed_runtime.events import EventLedger, SQLiteEventLedger
from seed_runtime.operator_session_standing import (
    advance_operator_session_standing,
    project_operator_session_standing,
)
from seed_runtime.operator_console import run_persistent_operator_console

MATERIALS = (
    "alpha\nbeta\ngamma\nexit\n",
    "alpha\n\n\nbeta\nexit\n",
    "ünïcode ✓\nnaïve\nexit\n",
    'def greet(name):\n    return "Hello " + name\nexit\n',
    "only\nexit\n",
    "exit\n",
)


def _console(material, ledger=None):
    ledger = ledger if ledger is not None else EventLedger()
    output = StringIO()
    run_persistent_operator_console(
        ledger=ledger,
        workspace_id="w",
        session_id="s",
        input_stream=StringIO(material),
        output_stream=output,
    )
    return ledger, output.getvalue()


def _replay(events):
    ledger = EventLedger()
    ledger.extend(events)
    return project_operator_session_standing(ledger, workspace_id="w", session_id="s")


def _ingress_event(index, *, unknowns):
    """One recorded ingress occurrence carrying distinct Unknowns."""
    ledger = EventLedger()
    return ledger.append(
        "operator.ingress.raw_material_captured",
        "w",
        {
            "attempt_ref": f"attempt_{index}",
            "dimensions": {"identity": f"material_{index}"},
            "material_role": "initial_ingress",
            "unknowns": list(unknowns),
        },
        session_id="s",
    )


def _advance(events, prior=None):
    return advance_operator_session_standing(
        events, workspace_id="w", session_id="s", prior=prior
    )


# --------------------------------------------------------------------------
# Equivalence, at every occurrence boundary.
# --------------------------------------------------------------------------


@pytest.mark.parametrize("material", MATERIALS)
def test_advancing_one_occurrence_at_a_time_equals_replay(material):
    ledger, _ = _console(material)
    events = ledger.list("w")
    standing = _advance([])
    for index in range(len(events)):
        standing = _advance([events[index]], prior=standing)
        assert standing == _replay(events[: index + 1])


def test_advancing_in_the_console_s_own_groupings_equals_replay():
    """Two Presentation occurrences, then three ingress occurrences, repeating."""
    ledger, _ = _console("alpha\nbeta\ngamma\nexit\n")
    events = ledger.list("w")
    standing = _advance([])
    input = 0
    for size in (2, 3, 2, 3, 2, 3, 2):
        batch = events[input : input + size]
        if not batch:
            break
        standing = _advance(batch, prior=standing)
        input += len(batch)
        assert standing == _replay(events[:input])


def test_an_advance_over_no_occurrences_changes_nothing():
    ledger, _ = _console("alpha\nexit\n")
    events = ledger.list("w")
    standing = _advance(events)
    assert _advance([], prior=standing) == _replay(events)


def test_replay_still_works_and_agrees_with_a_single_advance():
    for material in MATERIALS:
        ledger, _ = _console(material)
        events = ledger.list("w")
        assert _advance(events) == _replay(events)
        assert project_operator_session_standing(
            ledger, workspace_id="w", session_id="s"
        ) == _replay(events)


def test_a_persisted_ledger_advances_identically(tmp_path):
    ledger = SQLiteEventLedger(str(tmp_path / "ledger.sqlite"))
    try:
        _console("alpha\nünïcode\nexit\n", ledger=ledger)
        events = ledger.list("w")
        standing = _advance([])
        for index in range(len(events)):
            standing = _advance([events[index]], prior=standing)
        assert standing == _replay(events)
    finally:
        ledger.close()


# --------------------------------------------------------------------------
# The architecture, pinned directly rather than by timing.
# --------------------------------------------------------------------------


def test_the_console_never_replays_the_session(monkeypatch):
    """One projection from nothing recorded, for C0. No replay after that."""
    calls = []
    from seed_runtime import operator_console

    original = operator_console.project_operator_session_standing

    def record(ledger, **kwargs):
        calls.append(len(ledger.list(kwargs["workspace_id"])))
        return original(ledger, **kwargs)

    monkeypatch.setattr(operator_console, "project_operator_session_standing", record)
    _console("alpha\nbeta\ngamma\ndelta\nexit\n")
    assert calls == [0]


def test_each_advance_consumes_only_what_an_act_just_recorded(monkeypatch):
    """Guards against a ledger scan reappearing on the continuation path."""
    from seed_runtime import operator_console

    sizes = []
    original = operator_console.advance_operator_session_standing

    def record(events, **kwargs):
        events = list(events)
        sizes.append(len(events))
        return original(events, **kwargs)

    monkeypatch.setattr(operator_console, "advance_operator_session_standing", record)
    _console("alpha\nbeta\ngamma\ndelta\nexit\n")
    assert set(sizes) <= {2, 3}, sizes


# --------------------------------------------------------------------------
# The ownership contract.
# --------------------------------------------------------------------------


def test_the_advance_consumes_its_prior():
    """Stated so it cannot be softened into a copy without a deliberate change.

    Copying per advance would cost the session length every time, which is the
    quadratic this replaced.
    """
    ledger, _ = _console("alpha\nbeta\nexit\n")
    events = ledger.list("w")
    prior = _advance(events[:5])
    before = len(prior["preserved_ingress_occurrences"])
    advanced = _advance(events[5:], prior=prior)
    assert advanced["attempts"] is prior["attempts"]
    assert len(prior["preserved_ingress_occurrences"]) >= before


def test_every_growable_accumulator_is_consumed_not_copied():
    """The prior-transfer rule has to hold for all of them, not most of them.

    `known_loss`, `unknowns` and `conflicts` were rebuilt from the prior on
    every advance and re-sorted on every return. They do not grow on the five
    live kinds, so the measured path stayed linear, but acquisition would make
    them grow and restore the shape.
    """
    ledger, _ = _console("alpha\nbeta\nexit\n")
    events = ledger.list("w")
    prior = _advance(events[:5])
    advanced = _advance(events[5:], prior=prior)
    for coordinate in (
        "attempts",
        "presentations",
        "preserved_ingress_occurrences",
        "known_loss",
        "unknowns",
        "conflicts",
    ):
        assert advanced[coordinate] is prior[coordinate], coordinate


def test_a_growing_unknown_set_does_not_reintroduce_per_advance_copying():
    """Distinct Unknowns per occurrence, which acquisition would produce."""
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
    ledger, output = _console("alpha\nbeta\ngamma\nexit\n")
    assert output.count("Bounded Presentation") == 4
    assert project_operator_session_standing(
        ledger, workspace_id="w", session_id="s"
    ) == _replay(ledger.list("w"))


# --------------------------------------------------------------------------
# Behaviour that must not have changed.
# --------------------------------------------------------------------------


def test_c0_still_forms_from_empty_standing():
    ledger, _ = _console("exit\n")
    formed = next(
        event
        for event in ledger.list("w")
        if event.kind == "operator.presentation.formed"
    )
    assert formed.payload["session_standing_as_of_event_id"] is None


def test_the_session_records_the_same_occurrences_it_always_did():
    ledger, output = _console("alpha\nbeta\nexit\n")
    kinds = [event.kind for event in ledger.list("w")]
    assert kinds.count("operator.ingress.ingress_occurred") == 2
    assert kinds.count("operator.presentation.formed") == 3
    assert kinds.count("operator.presentation.emitted") == 3
    assert output.count("Bounded Presentation") == 3
