"""Earlier preserved material remains referenceable by later occurrences.

The Book uses "remembering" for preservation of source coordinates or
standing for later lawful reconstruction (`05.Source.A`).  **This module does
not establish a Remembering Responsibility, Act, Standing, occurrence, or
kind.**  In active law that word is capitalised only at sentence starts and is
lowercase mid-sentence -- "sensing is not remembering, remembering is not
current read" -- and the section heading is lowercase.  The capital is
orthographic.

What this module demonstrates is narrow and structural:

    earlier events remain preserved and unchanged
    a later session read can reference them
    a later representation Act carries those references

That is the substrate later input support would require. It is **not** input support,
participation, admission, a finding, or new Standing, none of which are
demonstrated here. `01.Kinds` keeps applicable, admitted, and input distinct,
and carrying an event id as Evidence establishes none of them.

Two further limits.  Only representation representation_events were inspected; the other
operator event kinds are also later occurrences and are not shown to reference
the whole past.  And `#2350` left open whether
`read_operator_session_standing` is a lawful constitutional read
occurrence -- executing it proves the substrate exists, not that the read
is lawful.

This module also does not test that Seed's exact Act conditions change over time.  No
measurement act exists in the runtime, so there is no case where a later
material access reaches material it previously could not.

Run standalone to inspect the reference lists:

    python -m tests.test_preserved_material_later_referenceable
"""

from __future__ import annotations

import json
from io import StringIO

import pytest

from seed_runtime.events import EventLedger
from seed_runtime.operator_session_standing import (
    read_operator_session_standing,
)
from seed_runtime.operator_console import run_persistent_operator_console

RECORDED = "operator.representation.recorded"


def _payload_snapshot(events) -> dict[str, str]:
    return {
        event.id: json.dumps(event.payload, sort_keys=True, default=str)
        for event in events
    }


@pytest.fixture(scope="module")
def ledger() -> EventLedger:
    """Three operator materials delivered in sequence, from an empty ledger."""
    led = EventLedger()
    run_persistent_operator_console(
        ledger=led,
        workspace_id="w",
        session_id="s",
        input_stream=StringIO("first\nsecond\nthird\nexit\n"),
        output_stream=StringIO(),
    )
    return led


def test_later_representations_retain_references_to_earlier_preserved_material(
    ledger,
):
    """Each representation Act's as-of boundary reaches further back than the last.

    Reference, not participation of each referenced event.  The representation Act
    has as input the read; what it carries forward is the exact occurrence
    that read was taken through.  `#2372` established that the boundary
    fixes the input prefix exactly, so an enumeration of that prefix adds
    no distinction to it.
    """
    events = ledger.list()
    positions = {event.id: index for index, event in enumerate(events)}
    representation_events = [e for e in events if e.kind == RECORDED]
    assert len(representation_events) >= 3
    boundaries = [
        e.payload["session_standing_as_of_event_id"] for e in representation_events
    ]
    # The first representation Act's read was empty.  Recording that absence is
    # itself preserved source coordinates, not an absent occurrence.
    assert boundaries[0] is None
    # Every later boundary reaches strictly further into the session.
    for earlier, later in zip(boundaries[1:], boundaries[2:]):
        assert positions[later] > positions[earlier]
    # The last representation Act's boundary still stands after the first recorded event.
    assert positions[boundaries[-1]] > positions[events[0].id]


def test_later_reference_does_not_alter_earlier_events(ledger):
    """Referencing preserved material leaves that material byte-identical."""
    before = _payload_snapshot(ledger.list())
    read_operator_session_standing(ledger, workspace_id="w", session_id="s")
    after = _payload_snapshot(
        e for e in ledger.list() if e.id in before
    )
    assert after == before


def test_representation_appends_nothing(ledger):
    """Read reads; it does not record.

    `06.Events:20` holds that event recording is not required for every
    constitutional occurrence.  This read reads without appending.
    """
    count_before = len(ledger.list())
    read_operator_session_standing(ledger, workspace_id="w", session_id="s")
    assert len(ledger.list()) == count_before


def test_each_representation_act_is_appended_after_every_event_it_references(ledger):
    """Narrow by intent: an ordering finding about the ledger, nothing more.

    This says nothing about findings or Standing.  A representation Act is
    not a finding, and its own recorded authority is "representation Act occurrence
    only; establishes no Selection, support relation, result relation, or response treatment".
    """
    events = ledger.list()
    representation_events = [e for e in events if e.kind == RECORDED]
    positions = {event.id: index for index, event in enumerate(events)}
    # Each representation Act appears after the occurrence its boundary names.
    for representation_event in representation_events:
        boundary = representation_event.payload["session_standing_as_of_event_id"]
        if boundary is not None:
            assert positions[boundary] < positions[representation_event.id]


def test_no_act_condition_change_is_claimed_here(ledger):
    """Guard against this module being read as more than it is.

    Only one kind of Act with participating inputs runs in this session.  If a second
    measurement or finding act is added later, this assertion should fail and
    be replaced by a real Act-condition-change test.
    """
    observed_operator_event_kinds = {
        e.kind for e in ledger.list() if e.kind.startswith("operator.")
    }
    assert observed_operator_event_kinds == {
        "operator.representation.recorded",
        "operator.representation.emission_attempted",
        "operator.representation.emission_act_evidenced",
        "operator.representation.emission_carriage_evidenced",
        "operator.yield.evidence_recorded",
        "operator.representation.emitted",
        "operator.ingress.raw_material_captured",
        "operator.ingress.decoder_outcome_recorded",
        "operator.ingress.ingress_occurred",
    }


def render_evidence_growth() -> str:
    led = EventLedger()
    run_persistent_operator_console(
        ledger=led,
        workspace_id="w",
        session_id="s",
        input_stream=StringIO("first\nsecond\nthird\nexit\n"),
        output_stream=StringIO(),
    )
    lines = ["representation Act -> the occurrence its Standing was taken through", ""]
    for event in (e for e in led.list() if e.kind == RECORDED):
        lines.append(
            f"  {event.id}  as_of="
            f"{event.payload['session_standing_as_of_event_id']}"
        )
    return "\n".join(lines)


if __name__ == "__main__":  # pragma: no cover - inspection entry point
    print(render_evidence_growth())
