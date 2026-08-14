"""A Presentation records the occurrence its Standing was taken through, not the prefix.

`session_standing_evidence_ids` copied session Standing's whole append-order
event inventory into every `operator.presentation.formed` payload, beside
`session_standing_as_of_event_id`, which already names that occurrence.

`#2372` established that the copy was exactly derivable from the boundary
across 67 formations, that its only non-test reader passed it straight through,
that no clause requires it, and that its durable growth converged on x4 per
doubling -- an extrapolated 29 billion identifiers for one corpus file.

`05.Evidence:19` refuses a copied causation identifier the standing of verified
provenance, and `05.Source.A` states copied provenance references do not turn
source labels into established Standing. A longer list was never stronger Evidence than
a shorter one.

These tests pin the removal and the boundary that remains.
"""

from __future__ import annotations

from io import StringIO

import pytest

from seed_runtime.events import EventLedger
from seed_runtime.operator_session_standing import read_operator_session_standing
from seed_runtime.operator_console import run_persistent_operator_console

FORMED = "operator.presentation.formed"
FAMILIES = (
    "operator.ingress.",
    "operator.presentation.",
    "operator.exchange.",
    "operator.interaction.",
)


def _console(material):
    ledger = EventLedger()
    output = StringIO()
    run_persistent_operator_console(
        ledger=ledger,
        workspace_id="w",
        session_id="s",
        input_stream=StringIO(material),
        output_stream=output,
    )
    return ledger, output.getvalue()


def _standing(ledger):
    return read_operator_session_standing(ledger, workspace_id="w", session_id="s")


@pytest.fixture(scope="module")
def session():
    return _console("alpha\n\nünïcode\ndef f(x):\nexit\n")


# --------------------------------------------------------------------------
# No history inventory is durably recorded.
# --------------------------------------------------------------------------


def test_no_formation_records_a_history_inventory(session):
    ledger, _ = session
    for event in ledger.list("w"):
        assert "session_standing_evidence_ids" not in event.payload


def test_no_projected_presentation_exposes_one(session):
    ledger, _ = session
    for presentation in _standing(ledger)["presentations"].values():
        assert "session_standing_evidence_ids" not in presentation


def test_recorded_payload_size_does_not_grow_with_session_length():
    """The defect being removed: each formation carried every prior event id."""
    sizes = []
    for lines in (5, 10, 20):
        ledger, _ = _console("material\n" * lines + "exit\n")
        formations = [e for e in ledger.list("w") if e.kind == FORMED]
        sizes.append(len(str(formations[-1].payload)) - len(str(formations[0].payload)))
    # Payload size differs between first and last formation only by the
    # boundary identifier, not by an inventory that grows with the session.
    assert max(sizes) < 200, sizes


# --------------------------------------------------------------------------
# The boundary that remains still fixes the input prefix.
# --------------------------------------------------------------------------


def test_the_first_formation_records_absence_of_a_prior_occurrence(session):
    """Recorded absence, not absence of participation."""
    ledger, _ = session
    first = next(e for e in ledger.list("w") if e.kind == FORMED)
    assert "session_standing_as_of_event_id" in first.payload
    assert first.payload["session_standing_as_of_event_id"] is None


def test_each_boundary_reaches_strictly_further_than_the_last(session):
    ledger, _ = session
    events = ledger.list("w")
    positions = {event.id: index for index, event in enumerate(events)}
    boundaries = [
        e.payload["session_standing_as_of_event_id"]
        for e in events
        if e.kind == FORMED
    ]
    assert boundaries[0] is None
    later = [positions[b] for b in boundaries[1:]]
    assert later == sorted(later)
    assert len(set(later)) == len(later)


def test_the_boundary_still_determines_the_consumed_prefix(session):
    """What the removed list enumerated is reconstructible from what remains."""
    ledger, _ = session
    events = ledger.list("w")

    def prefix_through(boundary):
        if boundary is None:
            return []
        collected = []
        for event in events:
            if event.session_id != "s":
                continue
            if not any(event.kind.startswith(family) for family in FAMILIES):
                continue
            collected.append(event.id)
            if event.id == boundary:
                break
        return collected

    for formation in (e for e in events if e.kind == FORMED):
        boundary = formation.payload["session_standing_as_of_event_id"]
        input = prefix_through(boundary)
        assert (input and input[-1] == boundary) or boundary is None


def test_every_boundary_precedes_the_formation_that_records_it(session):
    ledger, _ = session
    events = ledger.list("w")
    positions = {event.id: index for index, event in enumerate(events)}
    for formation in (e for e in events if e.kind == FORMED):
        boundary = formation.payload["session_standing_as_of_event_id"]
        if boundary is not None:
            assert positions[boundary] < positions[formation.id]


# --------------------------------------------------------------------------
# Nothing else about the session changed.
# --------------------------------------------------------------------------


def test_the_session_still_projects_deterministically(session):
    ledger, _ = session
    assert _standing(ledger) == _standing(ledger)


def test_the_console_still_presents_every_interaction(session):
    _, output = session
    assert output.count("Bounded Presentation") == 5


def test_standing_still_records_the_boundary_it_consumed_through(session):
    """Removed from the Presentation, and the boundary remains on the read."""
    ledger, _ = session
    standing = _standing(ledger)
    assert standing["as_of_event_id"] is not None
    assert standing["event_count"] > 0
    assert "input_event_ids" not in standing
