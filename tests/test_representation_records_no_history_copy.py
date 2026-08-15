"""A representation records the occurrence its Standing was taken through, not the prefix.

`locality_standing_evidence_ids` copied locality Standing's whole append-order
event-reference copy into every `operator.representation.recorded` payload, beside
`locality_standing_as_of_event_id`, which already names that occurrence.

`#2372` established that the copy was exactly derivable from the boundary
across 67 representation_events, that its only non-test reader passed it straight through,
that no clause requires it, and that its durable growth converged on x4 per
doubling -- an extrapolated 29 billion identifiers for one corpus file.

`05.Evidence:19` refuses a copied causation identifier the standing of verified
provenance, and `05.Source.A` states copied provenance references do not turn
source labels into established Standing. A longer list was never stronger Evidence than
a shorter one.

These tests pin the removal and the boundary that remains.
"""

from __future__ import annotations

from tests.binary_input import binary_input
from io import StringIO

import pytest

from seed_runtime.events import EventLedger
from seed_runtime.operator_locality_standing import read_operator_locality_standing
from seed_runtime.operator_console import run_persistent_operator_console

RECORDED = "operator.representation.recorded"
FAMILIES = (
    "material.ingest.",
    "operator.representation.",
    "operator.locality.",
    "operator.interaction.",
)


def _console(material):
    ledger = EventLedger()
    output = StringIO()
    run_persistent_operator_console(
        ledger=ledger,
        locality_id="s",
        input_stream=binary_input(material),
        output_stream=output,
    )
    return ledger, output.getvalue()


def _standing(ledger):
    return read_operator_locality_standing(ledger, locality_id="s")


@pytest.fixture(scope="module")
def locality():
    return _console("alpha\n\nünïcode\ndef f(x):\n")


# --------------------------------------------------------------------------
# No history copy is durably recorded.
# --------------------------------------------------------------------------


def test_no_representation_act_records_a_history_copy(locality):
    ledger, _ = locality
    for event in ledger.list():
        assert "locality_standing_evidence_ids" not in event.payload


def test_no_projected_representation_exposes_one(locality):
    ledger, _ = locality
    for representation in _standing(ledger)["representations"].values():
        assert "locality_standing_evidence_ids" not in representation


def test_recorded_payload_size_does_not_grow_with_locality_event_count():
    """The defect being removed: each representation Act carried every prior event id."""
    sizes = []
    for lines in (5, 10, 20):
        ledger, _ = _console("material\n" * lines + "")
        representation_events = [e for e in ledger.list() if e.kind == RECORDED]
        sizes.append(len(str(representation_events[-1].payload)) - len(str(representation_events[0].payload)))
    # Payload size differs between first and last representation Act only by the
    # boundary identifier, not by a copy that grows with the locality.
    assert max(sizes) < 200, sizes


# --------------------------------------------------------------------------
# The boundary that remains still fixes the input prefix.
# --------------------------------------------------------------------------


def test_the_first_representation_act_records_absence_of_a_prior_occurrence(locality):
    """Recorded absence, not absence of participation."""
    ledger, _ = locality
    first = next(e for e in ledger.list() if e.kind == RECORDED)
    assert "locality_standing_as_of_event_id" in first.payload
    assert first.payload["locality_standing_as_of_event_id"] is None


def test_each_boundary_reaches_strictly_further_than_the_last(locality):
    ledger, _ = locality
    events = ledger.list()
    positions = {event.id: index for index, event in enumerate(events)}
    boundaries = [
        e.payload["locality_standing_as_of_event_id"]
        for e in events
        if e.kind == RECORDED
    ]
    assert boundaries[0] is None
    later = [positions[b] for b in boundaries[1:]]
    assert later == sorted(later)
    assert len(set(later)) == len(later)


def test_the_boundary_still_determines_the_participating_prefix(locality):
    """What the removed list enumerated is addressable from what remains."""
    ledger, _ = locality
    events = ledger.list()

    def prefix_through(boundary):
        if boundary is None:
            return []
        collected = []
        for event in events:
            if event.locality_id != "s":
                continue
            if not any(event.kind.startswith(family) for family in FAMILIES):
                continue
            collected.append(event.id)
            if event.id == boundary:
                break
        return collected

    for representation_event in (e for e in events if e.kind == RECORDED):
        boundary = representation_event.payload["locality_standing_as_of_event_id"]
        input = prefix_through(boundary)
        assert (input and input[-1] == boundary) or boundary is None


def test_every_boundary_precedes_the_representation_act_that_records_it(locality):
    ledger, _ = locality
    events = ledger.list()
    positions = {event.id: index for index, event in enumerate(events)}
    for representation_event in (e for e in events if e.kind == RECORDED):
        boundary = representation_event.payload["locality_standing_as_of_event_id"]
        if boundary is not None:
            assert positions[boundary] < positions[representation_event.id]


# --------------------------------------------------------------------------
# Nothing else about the locality different.
# --------------------------------------------------------------------------


def test_the_locality_still_projects_deterministically(locality):
    ledger, _ = locality
    assert _standing(ledger) == _standing(ledger)


def test_the_console_still_presents_every_interaction(locality):
    _, output = locality
    assert output.count("Bounded Representation") == 5


def test_standing_still_records_its_participation_boundary(locality):
    """Removed from the Representation, and the boundary remains on the read."""
    ledger, _ = locality
    standing = _standing(ledger)
    assert standing["as_of_event_id"] is not None
    assert standing["event_count"] > 0
    assert "input_event_ids" not in standing
