"""One attempt projects from its own occurrences, not from a whole-workspace rebuild.

`run_operator_ingress_attempt` used to reach its result through
`StateProjector.project(workspace_id)`: build a fresh whole-workspace
projection, rebuild every entity, Fact, alias, relationship and index, then
return one bounded attempt out of it. Doing that once per attempt made
occurrence *j* replay for every later attempt.

The projection it needs was already bounded. `project_operator_ingress_events`
consumes only the per-attempt mapping -- no entity, Fact, alias, relationship,
or goal -- so the attempt can be projected from exactly the three occurrences it
recorded.

**The guard is equivalence, not speed.** The central tests here compare the
bounded projection against the whole-workspace one it replaces. Timing is not
asserted anywhere; `test_live_ingress_does_not_rebuild_the_workspace` pins the
architecture directly instead.

What is deliberately no longer performed is the replay of unrelated historical
events. The refusals this result depends on are local to the attempt and its
lineage, and they are exercised below.
"""

from __future__ import annotations

import tempfile
from io import StringIO
from pathlib import Path

import pytest

from seed_runtime import operator_ingress
from seed_runtime.events import EventLedger, SQLiteEventLedger
from seed_runtime.operator_ingress import run_operator_ingress_attempt
from seed_runtime.operator_ingress_addressable_material import (
    OperatorIngressAddressableMaterialError,
)
from seed_runtime.operator_ingress_representation import capture_stdin_material
from seed_runtime.state import StateProjector

MATERIALS = (
    "the cat jumped the fence\n",
    "\n",
    "   \n",
    "\ttabbed\n",
    "ünïcode ✓\n",
    "def greet(name):\n",
)
OCCURRED = "operator.ingress.ingress_occurred"


class UndecodableByteStream:
    """A byte stream whose material the selected decoder rejects."""

    def readline(self) -> bytes:
        return b"\xff\xfe\n"


def _attempt(ledger, material, **kwargs):
    return run_operator_ingress_attempt(
        ledger=ledger,
        workspace_id="w",
        session_id="s",
        captured_ingress=capture_stdin_material(StringIO(material)),
        output_stream=StringIO(),
        **kwargs,
    )


def _whole_workspace(ledger, attempt):
    return StateProjector(ledger).project("w").operator_ingress_attempts[attempt]


# --------------------------------------------------------------------------
# Equivalence with the whole-workspace projection it replaces.
# --------------------------------------------------------------------------


def test_bounded_projection_equals_the_whole_workspace_projection():
    """Every attempt, across representative material, must project identically."""
    ledger = EventLedger()
    bounded = [_attempt(ledger, material) for material in MATERIALS]
    for projection in bounded:
        attempt = projection["current_standing"]["preserved_ingress"]["subject_ref"]
        assert projection == _whole_workspace(ledger, attempt)


def test_equivalence_holds_for_the_earliest_attempt_after_many_later_ones():
    """The attempt most exposed to the removed replay is the first one."""
    ledger = EventLedger()
    first = _attempt(ledger, "first material\n")
    for index in range(8):
        _attempt(ledger, f"later material {index}\n")
    attempt = first["current_standing"]["preserved_ingress"]["subject_ref"]
    assert first == _whole_workspace(ledger, attempt)


def test_stop_path_projection_equals_the_whole_workspace_projection():
    """Decoder refusal must project identically through the bounded path."""
    ledger = EventLedger()
    _attempt(ledger, "earlier material\n")
    projection = run_operator_ingress_attempt(
        ledger=ledger,
        workspace_id="w",
        session_id="s",
        captured_ingress=capture_stdin_material(UndecodableByteStream()),
        output_stream=StringIO(),
    )
    assert projection["closed"] is True
    stop = next(
        event
        for event in ledger.list_events("w")
        if event.kind == "operator.ingress.stopping_occurred"
    )
    attempt = stop.payload["attempt_ref"]
    assert projection == _whole_workspace(ledger, attempt)


def test_session_standing_is_still_carried_through():
    ledger = EventLedger()
    standing = {"preserved_ingress_occurrences": []}
    projection = _attempt(ledger, "material\n", session_standing=standing)
    assert projection["session_standing"] is standing


# --------------------------------------------------------------------------
# The refusals this result depends on are local, and they still fire.
# --------------------------------------------------------------------------


def test_a_tampered_occurrence_carrying_a_genuine_identifier_still_refuses():
    """The adversarial case that a per-identifier cache would have bypassed."""
    ledger = EventLedger()
    _attempt(ledger, "material\n")
    occurrence = next(e for e in ledger.list_events("w") if e.kind == OCCURRED)
    foreign = occurrence.model_copy(update={"workspace_id": "elsewhere"})
    with pytest.raises(OperatorIngressAddressableMaterialError):
        operator_ingress.project_operator_ingress_events({}, foreign, ledger=ledger)


@pytest.mark.parametrize(
    "change",
    (
        {"raw_material_event_id": "evt_absent"},
        {"representation_examination_event_id": "evt_absent"},
        {"lineage": []},
        {"ingress_kind": "invented"},
        {"decoded_text": None},
        {"attempt_ref": "operator_ingress_attempt_absent"},
    ),
)
def test_broken_lineage_still_refuses(change):
    """The local validation surface, exercised one coordinate at a time."""
    ledger = EventLedger()
    _attempt(ledger, "material\n")
    occurrence = next(e for e in ledger.list_events("w") if e.kind == OCCURRED)
    broken = occurrence.model_copy(
        update={"payload": {**occurrence.payload, **change}}
    )
    with pytest.raises(Exception):
        operator_ingress.project_operator_ingress_events({}, broken, ledger=ledger)


def test_a_reversed_lineage_still_refuses():
    ledger = EventLedger()
    _attempt(ledger, "material\n")
    occurrence = next(e for e in ledger.list_events("w") if e.kind == OCCURRED)
    reversed_lineage = list(reversed(occurrence.payload["lineage"]))
    broken = occurrence.model_copy(
        update={"payload": {**occurrence.payload, "lineage": reversed_lineage}}
    )
    with pytest.raises(Exception):
        operator_ingress.project_operator_ingress_events({}, broken, ledger=ledger)


# --------------------------------------------------------------------------
# The architecture, pinned directly rather than by timing.
# --------------------------------------------------------------------------


def test_live_ingress_does_not_rebuild_the_workspace(monkeypatch):
    """A whole-workspace projection must not be built to return one attempt."""
    calls = []
    original = StateProjector.project

    def record(self, workspace_id, **kwargs):
        calls.append(workspace_id)
        return original(self, workspace_id, **kwargs)

    monkeypatch.setattr(StateProjector, "project", record)
    ledger = EventLedger()
    for material in MATERIALS:
        _attempt(ledger, material)
    assert calls == []


def test_one_attempt_projects_only_its_own_occurrences(monkeypatch):
    """Guards against `ledger.list_events(...)` reappearing inside the helper."""
    ledger = EventLedger()
    for index in range(5):
        _attempt(ledger, f"material {index}\n")

    projected = []
    original = operator_ingress.project_operator_ingress_events

    def record(attempts, event, *, ledger=None):
        projected.append(event.id)
        return original(attempts, event, ledger=ledger)

    monkeypatch.setattr(operator_ingress, "project_operator_ingress_events", record)
    _attempt(ledger, "one more\n")
    assert len(projected) == 3


def test_the_projection_reads_only_the_attempt_mapping():
    """`project_operator_ingress_events` consumes no whole-workspace projection."""
    ledger = EventLedger()
    _attempt(ledger, "material\n")
    occurrence = next(e for e in ledger.list_events("w") if e.kind == OCCURRED)
    attempts: dict = {}
    operator_ingress.project_operator_ingress_events(
        attempts, occurrence, ledger=ledger
    )
    assert list(attempts) == [occurrence.payload["attempt_ref"]]


# --------------------------------------------------------------------------
# Persisted ledgers.
# --------------------------------------------------------------------------


def test_a_persisted_ledger_projects_identically():
    """`SQLiteEventLedger.get` rebuilds an Event per call, so identity never holds.

    Any boundary that distinguishes a recorded occurrence must compare by value.
    """
    with tempfile.TemporaryDirectory() as directory:
        ledger = SQLiteEventLedger(str(Path(directory) / "ledger.sqlite"))
        try:
            for material in MATERIALS[:3]:
                projection = _attempt(ledger, material)
                attempt = projection["current_standing"]["preserved_ingress"][
                    "subject_ref"
                ]
                assert projection == _whole_workspace(ledger, attempt)
            occurrence = next(
                e for e in ledger.list_events("w") if e.kind == OCCURRED
            )
            assert ledger.get(occurrence.id) is not occurrence
            assert ledger.get(occurrence.id) == occurrence
        finally:
            ledger.close()
