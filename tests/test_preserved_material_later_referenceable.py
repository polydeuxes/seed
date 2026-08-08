"""Earlier preserved material remains referenceable by later occurrences.

The Book uses "remembering" for preservation of sufficient testimony or
standing for later lawful recovery (`05.Testimony:109`).  **This module does
not establish a Remembering Responsibility, Act, Standing, occurrence, or
kind.**  In active law that word is capitalised only at sentence starts and is
lowercase mid-sentence -- "sensing is not remembering, remembering is not
current projection" -- and the section heading is lowercase.  The capital is
orthographic.

What this module demonstrates is narrow and structural:

    earlier events remain preserved and unchanged
    a later session projection can reference them
    a later presentation formation carries those references

That is the substrate later Uptake would require.  It is **not** Uptake,
consumption, admission, a finding, or new Standing, none of which are
demonstrated here.  `01.Uptake` keeps applicable, admitted, and consumed as
distinct standings, and carrying an event id as evidence establishes none of
them.

Two further limits.  Only presentation formations were inspected; the other
operator event kinds are also later occurrences and are not shown to reference
the whole past.  And `#2350` left open whether
`project_operator_session_standing` is a lawful constitutional projection
occurrence -- executing it proves the substrate exists, not that the projection
is lawful.

This module also does not test that Seed's *capability* changes over time.  No
measurement act exists in the runtime, so there is no case where a later
capability reaches material it previously could not.

Run standalone to inspect the reference lists:

    python -m tests.test_preserved_material_later_referenceable
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


def test_later_formations_retain_references_to_earlier_preserved_material(
    ledger,
):
    """Each formation's evidence list includes every earlier event id.

    References, not consumption of each referenced event.  The formation
    consumes the projection; what it carries forward is that projection's
    ordered list of event ids.
    """
    formations = [e for e in ledger.list() if e.kind == FORMED]
    assert len(formations) >= 3
    evidence = [e.payload["session_standing_evidence_ids"] for e in formations]
    # The first formation's projection was empty.  Recording that emptiness is
    # itself preserved testimony, not an absent occurrence.
    assert evidence[0] == []
    # Every later evidence list strictly extends the one before it.
    for earlier, later in zip(evidence, evidence[1:]):
        assert later[: len(earlier)] == earlier
        assert len(later) > len(earlier)
    # The very first recorded event is still cited by the last formation.
    assert ledger.list()[0].id in evidence[-1]


def test_later_reference_does_not_alter_earlier_events(ledger):
    """Referencing preserved material leaves that material byte-identical."""
    before = _payload_snapshot(ledger.list())
    project_operator_session_standing(ledger, workspace_id="w", session_id="s")
    after = _payload_snapshot(
        e for e in ledger.list() if e.id in before
    )
    assert after == before


def test_projection_appends_nothing(ledger):
    """Projection reads; it does not record.

    `06.Events:20` holds that event recording is not required for every
    constitutional occurrence.  This projection reads without appending.
    """
    count_before = len(ledger.list())
    project_operator_session_standing(ledger, workspace_id="w", session_id="s")
    assert len(ledger.list()) == count_before


def test_each_formation_is_appended_after_every_event_it_references(ledger):
    """Narrow by intent: an ordering fact about the ledger, nothing more.

    This says nothing about findings or Standing.  A presentation formation is
    not a finding, and its own recorded authority is "formation occurrence
    only; establishes no selection, warrant, goal, or response treatment".
    """
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
    observed_operator_event_kinds = {
        e.kind for e in ledger.list() if e.kind.startswith("operator.")
    }
    assert observed_operator_event_kinds == {
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
    lines = ["formation -> earlier event ids referenced", ""]
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
