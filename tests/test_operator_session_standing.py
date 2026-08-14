from copy import deepcopy
from io import StringIO

from seed_runtime.events import EventLedger
from seed_runtime.operator_ingress import run_operator_ingress_attempt
from seed_runtime.operator_ingress_representation import capture_stdin_material
from seed_runtime.operator_console import run_persistent_operator_console
from seed_runtime.operator_session_standing import project_operator_session_standing


def _attempt(ledger, text, *, workspace="w", session="s", session_standing=None):
    return run_operator_ingress_attempt(
        ledger=ledger,
        workspace_id=workspace,
        session_id=session,
        captured_ingress=capture_stdin_material(StringIO(text)),
        output_stream=StringIO(),
        session_standing=session_standing,
    )


def _standing(ledger, *, workspace="w", session="s"):
    return project_operator_session_standing(
        ledger, workspace_id=workspace, session_id=session
    )


def test_events_from_different_sessions_cannot_influence_one_another():
    ledger = EventLedger()
    first = _attempt(ledger, "first session material\n", session="s1")
    second = _attempt(ledger, "second session material\n", session="s2")

    standing_one = _standing(ledger, session="s1")
    standing_two = _standing(ledger, session="s2")

    assert standing_one["session_id"] == "s1"
    assert standing_two["session_id"] == "s2"
    one_subjects = {
        occurrence["subject_ref"]
        for occurrence in standing_one["preserved_ingress_occurrences"]
    }
    two_subjects = {
        occurrence["subject_ref"]
        for occurrence in standing_two["preserved_ingress_occurrences"]
    }
    assert one_subjects == {first["current_standing"]["preserved_ingress"]["subject_ref"]}
    assert two_subjects == {second["current_standing"]["preserved_ingress"]["subject_ref"]}
    assert not set(standing_one["attempts"]) & set(standing_two["attempts"])
    assert not {e for a in standing_one["attempts"].values() for e in a["event_ids"]} & {
        e for a in standing_two["attempts"].values() for e in a["event_ids"]
    }


def test_next_attempt_consumes_standing_from_earlier_same_session_events():
    ledger = EventLedger()
    first = _attempt(ledger, "earlier material\n")

    standing = _standing(ledger)
    second = _attempt(ledger, "later material\n", session_standing=standing)

    assert second["session_standing"] is standing
    inherited = second["session_standing"]["preserved_ingress_occurrences"]
    assert [occurrence["subject_ref"] for occurrence in inherited] == [
        first["current_standing"]["preserved_ingress"]["subject_ref"]
    ]
    assert first["current_standing"]["preserved_ingress"]["subject_ref"] == (
        inherited[0]["subject_ref"]
    )


def test_projection_is_deterministic_regardless_of_unrelated_ledger_events():
    ledger = EventLedger()
    _attempt(ledger, "session material\n")
    before = _standing(ledger)

    ledger.append("unrelated.kind", "w", {"noise": True}, session_id="s")
    ledger.append("unrelated.kind", "other-workspace", {}, session_id="s")
    _attempt(ledger, "other session material\n", session="elsewhere")
    after = _standing(ledger)

    assert after == before
    assert _standing(ledger) == after


def test_unknown_conflict_and_absence_remain_distinct():
    ledger = EventLedger()
    _attempt(ledger, "material\n")

    standing = _standing(ledger)

    # Unknowns are only what session events positively carry.
    assert standing["unknowns"] == ["true source-relative encoding Unknown"]
    # No session event records a conflict or a relation standing; both stay
    # empty rather than being promoted to Unknown or to a negative Assertion.
    assert standing["conflicts"] == []
    assert standing["recorded_relation_standings"] == []
    assert "relation" not in " ".join(standing["unknowns"])
    next_attempt = _attempt(ledger, "next\n", session_standing=standing)
    assert next_attempt["session_standing"]["recorded_relation_standings"] == []


def test_one_attempt_behavior_unchanged_without_earlier_session_history():
    baseline_ledger = EventLedger()
    baseline = _attempt(baseline_ledger, "solo material\n")
    assert "session_standing" not in baseline

    # The console passes Standing containing C0 to the first interaction,
    # and its interaction output is a bounded Presentation, not the View.
    input_stream = StringIO("solo material\nexit\n")
    output_stream = StringIO()
    console_ledger = EventLedger()
    run_persistent_operator_console(
        ledger=console_ledger,
        workspace_id="w",
        session_id="s",
        input_stream=input_stream,
        output_stream=output_stream,
    )
    rendered = output_stream.getvalue()
    assert "Bounded Presentation" in rendered
    assert "Session Standing" not in rendered


def test_console_supplies_prior_session_standing_to_later_interactions():
    input_stream = StringIO("first material\nsecond material\nexit\n")
    output_stream = StringIO()
    ledger = EventLedger()

    run_persistent_operator_console(
        ledger=ledger,
        workspace_id="w",
        session_id="s",
        input_stream=input_stream,
        output_stream=output_stream,
    )

    rendered = output_stream.getvalue()
    assert rendered.count("Bounded Presentation") == 3
    standing = _standing(ledger)
    assert len(standing["presentations"]) == 3
    first_id, second_id, third_id = list(standing["presentations"])
    assert list(standing["presentations"])[-1] == third_id
    # The later Presentation's recorded formation input Standing taken
    # through a strictly later occurrence than the first one's.
    positions = {event.id: index for index, event in enumerate(ledger.list("w"))}
    first_presentation = standing["presentations"][first_id]
    assert first_presentation["session_standing_as_of_event_id"] is None
    later_boundary = positions[
        standing["presentations"][third_id]["session_standing_as_of_event_id"]
    ]
    # The first Presentation's own formation and emission occurrences fall
    # inside the prefix the later formation input.
    assert positions[first_presentation["formed_event_id"]] < later_boundary
    assert positions[first_presentation["emitted_event_id"]] < later_boundary


def test_projection_does_not_mutate_ledger_or_synthesize_events():
    ledger = EventLedger()
    _attempt(ledger, "material\n")
    events_before = deepcopy(ledger.list("w"))

    _standing(ledger)

    assert ledger.list("w") == events_before
