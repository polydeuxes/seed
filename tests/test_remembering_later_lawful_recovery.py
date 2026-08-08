"""Remembering: preserved material stays available for later lawful recovery.

`05.Testimony:109` -- "Remembering is preservation of sufficient testimony or
standing for later lawful recovery."

This module tests the temporal invariant that makes bootstrap tractable: an act
occurring late may consume material preserved early, and doing so produces new
occurrences rather than altering the old ones.  Seed is not limited to what it
could establish at the moment material arrived.

What this module does NOT test, stated plainly because the distinction is the
whole point: it does not test that Seed's *capability* changes over time.  No
measurement act exists in the runtime yet, so there is no M2-becomes-available
case to exercise.  What is tested is the surrounding law -- that later
consumption of earlier material is lawful, additive, and non-destructive --
which is what any future capability change would rely on.

Run standalone to inspect the evidence lists:

    python -m tests.test_remembering_later_lawful_recovery
"""

from __future__ import annotations

import json
import sys
from io import StringIO
from pathlib import Path

import pytest

from seed_runtime.events import EventLedger
from seed_runtime.operator_session_standing import (
    project_operator_session_standing,
)

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import seed_local  # noqa: E402

FORMED = "operator.presentation.formed"


def _payload_snapshot(events) -> dict[str, str]:
    return {
        event.id: json.dumps(event.payload, sort_keys=True, default=str)
        for event in events
    }


@pytest.fixture(scope="module")
def ledger() -> EventLedger:
    """Three operator materials delivered in sequence, from an empty ledger."""
    led = EventLedger()
    seed_local.run_persistent_operator_console(
        ledger=led,
        workspace_id="w",
        session_id="s",
        input_stream=StringIO("first\nsecond\nthird\nexit\n"),
        output_stream=StringIO(),
    )
    return led


def test_later_occurrences_consume_earlier_preserved_material(ledger):
    """Each formation's evidence includes every earlier event, cumulatively.

    This is the property that makes a growing capability useful: the material
    from the first interaction is still being consumed at the last one.
    """
    formations = [e for e in ledger.list() if e.kind == FORMED]
    assert len(formations) >= 3
    evidence = [e.payload["session_standing_evidence_ids"] for e in formations]
    # The first formation consumes empty Standing; that is still consumption.
    assert evidence[0] == []
    # Every later evidence list strictly extends the one before it.
    for earlier, later in zip(evidence, evidence[1:]):
        assert later[: len(earlier)] == earlier
        assert len(later) > len(earlier)
    # The very first recorded event is still cited by the last formation.
    assert ledger.list()[0].id in evidence[-1]


def test_later_consumption_does_not_alter_earlier_events(ledger):
    """Consuming preserved material leaves that material byte-identical."""
    before = _payload_snapshot(ledger.list())
    project_operator_session_standing(ledger, workspace_id="w", session_id="s")
    after = _payload_snapshot(
        e for e in ledger.list() if e.id in before
    )
    assert after == before


def test_projection_appends_nothing(ledger):
    """Projection reads; it does not record.

    `06.Events:20` holds that event recording is not required for every
    constitutional occurrence, and projection here consumes without emitting.
    """
    count_before = len(ledger.list())
    project_operator_session_standing(ledger, workspace_id="w", session_id="s")
    assert len(ledger.list()) == count_before


def test_a_later_finding_is_a_new_event_not_an_edit(ledger):
    """New standing arrives as new occurrences appended after the old ones."""
    events = ledger.list()
    formations = [e for e in events if e.kind == FORMED]
    positions = {event.id: index for index, event in enumerate(events)}
    # Each formation appears after every event it cites as evidence.
    for formation in formations:
        for cited in formation.payload["session_standing_evidence_ids"]:
            assert positions[cited] < positions[formation.id]


def test_no_capability_change_is_claimed_here(ledger):
    """Guard against this module being read as more than it is.

    Only one kind of consuming act runs in this session.  If a second
    measurement or finding act is added later, this assertion should fail and
    be replaced by a real capability-change test.
    """
    consuming_kinds = {
        e.kind for e in ledger.list() if e.kind.startswith("operator.")
    }
    assert consuming_kinds == {
        "operator.presentation.formed",
        "operator.presentation.emitted",
        "operator.ingress.raw_material_captured",
        "operator.ingress.representation_examined",
        "operator.ingress.ingress_occurred",
    }


def render_evidence_growth() -> str:
    led = EventLedger()
    seed_local.run_persistent_operator_console(
        ledger=led,
        workspace_id="w",
        session_id="s",
        input_stream=StringIO("first\nsecond\nthird\nexit\n"),
        output_stream=StringIO(),
    )
    lines = ["formation -> evidence consumed", ""]
    for event in (e for e in led.list() if e.kind == FORMED):
        cited = event.payload["session_standing_evidence_ids"]
        lines.append(
            f"  {event.id}  as_of="
            f"{event.payload['session_standing_as_of_event_id']}  "
            f"n={len(cited)}  {cited}"
        )
    return "\n".join(lines)


if __name__ == "__main__":  # pragma: no cover - inspection entry point
    print(render_evidence_growth())
