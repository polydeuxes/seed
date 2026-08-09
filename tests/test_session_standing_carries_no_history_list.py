"""Session Standing states the occurrence it consumed through, not the list of them.

`consumed_event_ids` enumerated every applicable session occurrence in append
order. `#2374` established that after `#2373` removed its last consumer it had
no reader at all -- not the runtime, not the rendered View, not the Presentation
path -- and that `project_operator_session_standing` never read it either. It
was initialised, appended to, and returned, and never consulted.

A value the producing act does not consult is a by-product of the fold rather
than part of it. `05.Evidence:19` separately refuses copied identifiers the
standing of verified provenance, and `06.Representations:18` conditions the
inventory View shape on a contract this never asserted.

`as_of_event_id` and `event_count` remain. `#2374` measured that the boundary
locates the applicable suffix exactly at every step of a session, so nothing
that wanted to continue from this Standing needs the prefix enumerated.
"""

from __future__ import annotations

from io import StringIO

import pytest

from seed_runtime.events import EventLedger
from seed_runtime.operator_ingress_view import format_operator_ingress_view
from seed_runtime.operator_session_standing import project_operator_session_standing
from scripts import seed_local

EMITTED = "operator.presentation.emitted"


def _console(material):
    ledger = EventLedger()
    output = StringIO()
    seed_local.run_persistent_operator_console(
        ledger=ledger,
        workspace_id="w",
        session_id="s",
        input_stream=StringIO(material),
        output_stream=output,
    )
    return ledger, output.getvalue()


def _standing(ledger):
    return project_operator_session_standing(ledger, workspace_id="w", session_id="s")


@pytest.fixture(scope="module")
def session():
    return _console("alpha\n\nünïcode\ndef f(x):\nexit\n")


# --------------------------------------------------------------------------
# 4. No such coordinate remains.
# --------------------------------------------------------------------------


def test_session_standing_carries_no_history_list(session):
    ledger, _ = session
    assert "consumed_event_ids" not in _standing(ledger)


def test_no_coordinate_grows_one_entry_per_occurrence(session):
    """Guards against the list returning under another name.

    Every remaining collection is keyed by a subject the session recorded, so
    none of them holds an entry per consumed occurrence.
    """
    ledger, _ = session
    standing = _standing(ledger)
    applicable = standing["event_count"]
    for coordinate, value in standing.items():
        if isinstance(value, (list, dict)):
            assert len(value) < applicable, coordinate


# --------------------------------------------------------------------------
# 1. Session Standing otherwise projects identically.
# --------------------------------------------------------------------------


def test_every_other_coordinate_is_unchanged(session):
    """The removal is one key; the rest of the projection is untouched."""
    ledger, _ = session
    standing = _standing(ledger)
    assert set(standing) == {
        "workspace_id",
        "session_id",
        "as_of_event_id",
        "event_count",
        "attempts",
        "preserved_ingress_occurrences",
        "interaction_closures",
        "presentations",
        "comparisons",
        "identifications",
        "latest_exchange_finding",
        "source_recoveries",
        "meaning_relations",
        "latest_source_recovery",
        "latest_meaning_relation",
        "goal_applicabilities",
        "goal_admissions",
        "goal_consumptions",
        "goal_standings",
        "latest_interaction_goal_standing",
        "recorded_relation_standings",
        "known_loss",
        "unknowns",
        "conflicts",
    }


def test_the_boundary_and_the_count_still_agree_with_the_session(session):
    ledger, _ = session
    standing = _standing(ledger)
    applicable = [
        event
        for event in ledger.list("w")
        if event.session_id == "s"
        and event.kind.split(".")[1]
        in {"ingress", "presentation", "exchange", "interaction"}
    ]
    assert standing["event_count"] == len(applicable)
    assert standing["as_of_event_id"] == applicable[-1].id


def test_projection_remains_deterministic(session):
    ledger, _ = session
    assert _standing(ledger) == _standing(ledger)


def test_a_session_with_no_recorded_occurrence_states_absence():
    """A bare ledger, not a console run -- `exit` still forms and emits C0."""
    standing = _standing(EventLedger())
    assert standing["as_of_event_id"] is None
    assert standing["event_count"] == 0


# --------------------------------------------------------------------------
# 2. Presentation order remains recoverable from `presentations`.
# --------------------------------------------------------------------------


def test_emission_order_is_recoverable_from_presentations_alone(session):
    """The claim the removed comment attributed to the list."""
    ledger, _ = session
    events = ledger.list("w")
    positions = {event.id: index for index, event in enumerate(events)}
    projected = [
        entry["emitted_event_id"]
        for entry in _standing(ledger)["presentations"].values()
        if entry["emitted_event_id"] is not None
    ]
    recorded = [event.id for event in events if event.kind == EMITTED]
    assert projected == recorded
    assert [positions[i] for i in projected] == sorted(positions[i] for i in projected)


def test_no_presentation_is_named_current(session):
    ledger, _ = session
    standing = _standing(ledger)
    assert not any("current" in key for key in standing["presentations"])
    assert "current_presentation" not in standing


# --------------------------------------------------------------------------
# 3. The live View and Presentation paths are unchanged.
# --------------------------------------------------------------------------


def test_the_rendered_view_still_states_the_boundary():
    """Rendered from a real attempt carrying real Standing."""
    from seed_runtime.operator_ingress import run_operator_ingress_attempt
    from seed_runtime.operator_ingress_representation import capture_stdin_material

    ledger = EventLedger()
    run_operator_ingress_attempt(
        ledger=ledger,
        workspace_id="w",
        session_id="s",
        captured_ingress=capture_stdin_material(StringIO("earlier\n")),
        output_stream=StringIO(),
    )
    projection = run_operator_ingress_attempt(
        ledger=ledger,
        workspace_id="w",
        session_id="s",
        captured_ingress=capture_stdin_material(StringIO("later\n")),
        output_stream=StringIO(),
        session_standing=_standing(ledger),
    )
    rendered = format_operator_ingress_view(projection)
    assert "Session Standing" in rendered
    assert "as of event" in rendered


def test_the_console_output_is_unchanged(session):
    _, output = session
    assert output.count("Bounded Presentation") == 5


def test_presentations_still_record_their_own_boundary(session):
    ledger, _ = session
    for entry in _standing(ledger)["presentations"].values():
        assert "session_standing_as_of_event_id" in entry
