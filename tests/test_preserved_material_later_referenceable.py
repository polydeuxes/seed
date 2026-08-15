"""Earlier preserved material remains referenceable by later occurrences.

The Book uses "remembering" for preservation of source coordinates or
standing for later lawful read (`05.Source.A`).  **This module does
not establish a Remembering Responsibility, Act, Standing, occurrence, or
kind.**  In active law that word is capitalised only at sentence starts and is
lowercase mid-sentence -- "sensing is not remembering, remembering is not
current read" -- and the section heading is lowercase.  The capital is
orthographic.

What this module demonstrates is narrow:

    earlier events remain preserved and preserved
    a later locality read can reference them
    a later representation Act carries those references

That is the substrate later input support would require. It is **not** input support,
participation, admission, a finding, or new Standing, none of which are
demonstrated here. `01.Kinds` keeps applicable, admitted, and input distinct,
and carrying an event identity as Evidence establishes none of them.

Two further limits.  Only representation representation_events were inspected; the other
operator event kinds are also later occurrences and are not shown to reference
the whole past.  And `#2350` left open whether
`read_operator_locality_standing` is a lawful constitutional read
occurrence -- executing it proves the substrate exists, not that the read
is lawful.

This module also does not test that Seed's exact Act conditions revision over time.  No
measurement act exists in the runtime, so there is no case where a later
material access reaches material it previously could not.

Run standalone to inspect the reference lists:

    python -m tests.test_preserved_material_later_referenceable
"""

from __future__ import annotations

import json
from tests.binary_input import binary_input
from io import StringIO

import pytest

from seed_runtime.events import EventLedger
from seed_runtime.operator_locality_standing import (
    read_operator_locality_standing,
)
from seed_runtime.operator_console import run_persistent_operator_console

RECORDED = "operator.representation.recorded"


def _material_snapshot(events) -> dict[str, str]:
    return {
        event.identity: json.dumps(event.material, sort_keys=True, default=str)
        for event in events
    }


@pytest.fixture(scope="module")
def ledger() -> EventLedger:
    """Three operator materials delivered in sequence, from an empty ledger."""
    led = EventLedger()
    run_persistent_operator_console(
        ledger=led,
        locality_identity="s",
        input_stream=binary_input("first\nsecond\nthird\n"),
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
    positions = {event.identity: index for index, event in enumerate(events)}
    representation_events = [e for e in events if e.kind == RECORDED]
    assert len(representation_events) >= 3
    boundaries = [
        e.material["locality_standing_as_of_event_identity"] for e in representation_events
    ]
    # The first representation Act's read was empty.  Recording that absence is
    # itself preserved source coordinates, not an absent occurrence.
    assert boundaries[0] is None
    # Every later boundary reaches strictly further into the locality.
    for earlier, later in zip(boundaries[1:], boundaries[2:]):
        assert positions[later] > positions[earlier]
    # The last representation Act's boundary still stands after the first recorded event.
    assert positions[boundaries[-1]] > positions[events[0].identity]


def test_later_reference_does_not_alter_earlier_events(ledger):
    """Referencing preserved material leaves that material byte-identical."""
    before = _material_snapshot(ledger.list())
    read_operator_locality_standing(ledger, locality_identity="s")
    after = _material_snapshot(
        e for e in ledger.list() if e.identity in before
    )
    assert after == before


def test_representation_appends_nothing(ledger):
    """Read reads; it does not record.

    `06.Events:20` holds that event recording is not required for every
    constitutional occurrence.  This read reads without appending.
    """
    count_before = len(ledger.list())
    read_operator_locality_standing(ledger, locality_identity="s")
    assert len(ledger.list()) == count_before


def test_each_representation_act_is_appended_after_every_event_it_references(ledger):
    """Narrow by intent: an ordering finding about the ledger, nothing more.

    This says nothing about findings or Standing.  A representation Act is
    not a finding, and its own recorded authority is "representation Act occurrence
    only; establishes no input support, result relation, or response treatment".
    """
    events = ledger.list()
    representation_events = [e for e in events if e.kind == RECORDED]
    positions = {event.identity: index for index, event in enumerate(events)}
    # Each representation Act appears after the occurrence its boundary names.
    for representation_event in representation_events:
        boundary = representation_event.material["locality_standing_as_of_event_identity"]
        if boundary is not None:
            assert positions[boundary] < positions[representation_event.identity]


def test_no_act_condition_change_is_claimed_here(ledger):
    """Guard against this module being read as more than it is.

    Only one kind of Act with participating inputs runs in this locality.  If a second
    measurement or finding act is added later, this assertion should fail and
    be replaced by a real Act-condition-revision test.
    """
    event_kinds = {
        e.kind
        for e in ledger.list()
        if e.kind.startswith(("material.", "operator."))
    }
    assert event_kinds == {
        "material.ingest.act_evidenced",
        "material.ingest.occurred",
        "operator.representation.recorded",
        "operator.representation.act_evidenced",
        "operator.representation.locality_evidenced",
        "operator.representation.emission_attempt_recorded",
        "operator.representation.emission_attempt_locality_evidenced",
        "operator.representation.emission_act_evidenced",
        "operator.representation.emission_locality_evidenced",
        "operator.yield.evidence_recorded",
        "operator.representation.emitted",
    }


def represent_evidence_growth() -> str:
    led = EventLedger()
    run_persistent_operator_console(
        ledger=led,
        locality_identity="s",
        input_stream=binary_input("first\nsecond\nthird\n"),
        output_stream=StringIO(),
    )
    lines = ["representation Act -> the occurrence its Standing was taken through", ""]
    for event in (e for e in led.list() if e.kind == RECORDED):
        lines.append(
            f"  {event.identity}  as_of="
            f"{event.material['locality_standing_as_of_event_identity']}"
        )
    return "\n".join(lines)


if __name__ == "__main__":  # pragma: no cover - inspection entry point
    print(represent_evidence_growth())
