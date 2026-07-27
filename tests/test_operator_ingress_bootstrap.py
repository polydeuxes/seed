from io import StringIO
import subprocess
import sys

import pytest

from seed_runtime.bounded_operator_goal_establishment import (
    BoundedOperatorGoalEstablishmentError,
    establish_bounded_operator_goal_from_closed_choice,
)
from seed_runtime.closed_choice_selection_binding import (
    ClosedChoiceOption,
    ClosedChoiceSelectionBindingError,
    OperatorSelectionTokenCapture,
    PresentedClosedChoiceSet,
)
from seed_runtime.events import EventLedger, SQLiteEventLedger
from seed_runtime.operator_ingress_bootstrap import (
    CHOICE_SET_REF,
    bootstrap_choice_set,
    run_operator_ingress_bootstrap,
    validate_capture_for_probe,
)
from seed_runtime.state import StateProjector


def run_attempt(text, ledger=None, session="s"):
    ledger = ledger or EventLedger()
    output = StringIO()
    view = run_operator_ingress_bootstrap(
        ledger=ledger,
        workspace_id="w",
        session_id=session,
        input_stream=StringIO(text),
        output_stream=output,
    )
    return ledger, view, output.getvalue()


@pytest.mark.parametrize(
    "token,treatment,closed",
    [("1", "common-grammar-acquisition", None), ("2", "local-stop", True)],
)
def test_exact_treatments_select_without_acquisition_and_stop_is_separate(
    token, treatment, closed
):
    ledger, view, output = run_attempt(f"do something exactly\n{token}\n")
    assert view["selected_treatment"] == treatment
    assert view.get("closed") is closed
    kinds = [event.kind for event in ledger.list_events("w")]
    assert "operator.bootstrap.treatment_selected" in kinds
    assert ("operator.bootstrap.stopping_occurred" in kinds) is (token == "2")
    assert not any(
        any(
            word in event.kind
            for word in ("demand", "acquisition", "interpretation", "cluster")
        )
        for event in ledger.list_events("w")
    )
    assert "1. Select bounded common-grammar acquisition treatment." in output


@pytest.mark.parametrize(
    "token", ["", " ", "1 ", " 1", "ONE", "Acquisition", "01", "2 "]
)
def test_near_matches_and_empty_are_unsupported_with_semantic_unknowns(token):
    ledger, view, output = run_attempt(f"hello\n{token}\n")
    assert view["standing"] == "unsupported"
    assert view["unknowns"] == [
        "operator intent Unknown",
        "requested treatment Unknown",
        "response meaning Unknown",
    ]
    assert "Unsupported response" in output
    assert not any(
        event.kind == "operator.bootstrap.treatment_selected"
        for event in ledger.list_events()
    )


def test_eof_is_distinct_from_empty_response():
    _, eof, _ = run_attempt("hello\n")
    _, empty, _ = run_attempt("hello\n\n", session="empty")
    assert eof["response_kind"] == "eof"
    assert empty["response_kind"] == "empty"


def test_initial_eof_records_eof_and_separate_stop_without_probe():
    ledger, view, output = run_attempt("")
    assert [event.kind for event in ledger.list_events("w")] == [
        "operator.bootstrap.initial_eof_occurred",
        "operator.bootstrap.stopping_occurred",
    ]
    assert view["closed"] is True
    assert view["standing"] == "closed"
    assert "selected_treatment" not in view
    assert output == "Bootstrap stopped locally.\n"


def test_exact_ingress_preservation_all_dimensions_and_durable_replay(tmp_path):
    path = tmp_path / "events.db"
    ledger, view, _ = run_attempt(
        "  Mixed CASE ingress  \n2\n", SQLiteEventLedger(str(path))
    )
    ingress = ledger.list_events("w")[0]
    assert ingress.payload["raw_input"] == "  Mixed CASE ingress  \n"
    assert ingress.payload["known_loss"] == [
        "terminal framing outside captured line is not preserved"
    ]
    assert len(view["dimensional_standing"]) == 7
    assert all(
        set(item["dimensions"])
        == {
            "identity",
            "content",
            "standing",
            "source_provenance",
            "responsibility",
            "authority_warrant",
            "scope_locality",
            "occurrence_preservation",
        }
        for item in view["dimensional_standing"].values()
    )
    assert all(
        item["lineage"] for item in list(view["dimensional_standing"].values())[1:]
    )
    attempt_ref = ingress.payload["attempt_ref"]
    ledger.close()
    reopened = SQLiteEventLedger(str(path))
    replayed = (
        StateProjector(reopened).project("w").operator_ingress_bootstraps[attempt_ref]
    )
    assert replayed == view
    assert all(
        event.payload["mutates_cluster"] is False for event in reopened.list_events("w")
    )


def _recorded_probe_inputs(ledger):
    events = ledger.list_events("w")
    ingress = events[0]
    response = next(
        e for e in events if e.kind == "operator.bootstrap.response_captured"
    )
    choice = bootstrap_choice_set(response.payload["presentation_ref"])
    capture = OperatorSelectionTokenCapture(
        response.payload["capture_ref"], CHOICE_SET_REF, "1"
    )
    return ingress.payload["attempt_ref"], choice, capture


def test_probe_identity_fingerprint_and_consumption_guards():
    ledger, _, _ = run_attempt("hello\n1\n")
    attempt, choice, capture = _recorded_probe_inputs(ledger)
    with pytest.raises(ClosedChoiceSelectionBindingError):
        validate_capture_for_probe(
            ledger=ledger,
            workspace_id="w",
            attempt_ref=attempt,
            choice_set=bootstrap_choice_set("presentation:wrong"),
            capture=capture,
        )
    wrong_set_capture = OperatorSelectionTokenCapture(
        capture.capture_ref, "goal-choice-set:wrong", capture.captured_token
    )
    with pytest.raises(ClosedChoiceSelectionBindingError):
        validate_capture_for_probe(
            ledger=ledger,
            workspace_id="w",
            attempt_ref=attempt,
            choice_set=choice,
            capture=wrong_set_capture,
        )
    altered = PresentedClosedChoiceSet(
        CHOICE_SET_REF,
        choice.prompt,
        (ClosedChoiceOption("1", "different", "Different"), *choice.options[1:]),
        choice.presentation_ref,
    )
    with pytest.raises(ClosedChoiceSelectionBindingError):
        validate_capture_for_probe(
            ledger=ledger,
            workspace_id="w",
            attempt_ref=attempt,
            choice_set=altered,
            capture=capture,
        )
    with pytest.raises(ClosedChoiceSelectionBindingError, match="already consumed"):
        validate_capture_for_probe(
            ledger=ledger,
            workspace_id="w",
            attempt_ref=attempt,
            choice_set=choice,
            capture=capture,
        )


def test_communication_binding_lacks_positive_boge_admission():
    ledger, view, _ = run_attempt("hello\n1\n")
    attempt, choice, capture = _recorded_probe_inputs(ledger)
    binding_event = next(
        e
        for e in ledger.list_events("w")
        if e.kind == "operator.bootstrap.binding_completed"
    )
    # Re-create the immutable binding only to exercise the downstream boundary;
    # production already consumed this capture and records the same binding identity.
    from seed_runtime.closed_choice_selection_binding import (
        bind_closed_choice_selection,
    )

    binding = bind_closed_choice_selection(choice, capture)
    assert (
        binding.binding_id == binding_event.payload["binding_id"] == view["binding_id"]
    )
    with pytest.raises(BoundedOperatorGoalEstablishmentError):
        establish_bounded_operator_goal_from_closed_choice(binding)


def test_two_durable_attempts_in_same_session_remain_distinct(tmp_path):
    path = tmp_path / "attempts.db"
    ledger = SQLiteEventLedger(str(path))
    _, first, _ = run_attempt("first\n1\n", ledger, session="same")
    _, second, _ = run_attempt("second\n2\n", ledger, session="same")
    attempt_refs = {e.payload["attempt_ref"] for e in ledger.list_events("w")}
    assert len(attempt_refs) == 2
    assert first["event_ids"] != second["event_ids"]
    ledger.close()
    reopened = SQLiteEventLedger(str(path))
    projection = StateProjector(reopened).project("w").operator_ingress_bootstraps
    assert set(projection) == attempt_refs
    assert {view["selected_treatment"] for view in projection.values()} == {
        "common-grammar-acquisition",
        "local-stop",
    }


def test_consumed_capture_replay_is_refused_after_durable_reconstruction(tmp_path):
    path = tmp_path / "replay.db"
    ledger, _, _ = run_attempt("hello\n1\n", SQLiteEventLedger(str(path)))
    attempt, choice, capture = _recorded_probe_inputs(ledger)
    ledger.close()
    reopened = SQLiteEventLedger(str(path))
    with pytest.raises(ClosedChoiceSelectionBindingError, match="already consumed"):
        validate_capture_for_probe(
            ledger=reopened,
            workspace_id="w",
            attempt_ref=attempt,
            choice_set=choice,
            capture=capture,
        )


def test_real_cli_reads_ingress_presents_stdout_and_persists(tmp_path):
    db = tmp_path / "cli.db"
    completed = subprocess.run(
        [
            sys.executable,
            "scripts/seed_local.py",
            "--operator-ingress-bootstrap",
            "--db",
            str(db),
            "--workspace",
            "cli-w",
            "--session",
            "cli-s",
        ],
        input="free form operator words\n2\n",
        text=True,
        capture_output=True,
        check=True,
    )
    assert completed.stdout.splitlines() == [
        "Select one treatment by its exact token:",
        "1. Select bounded common-grammar acquisition treatment.",
        "2. Select local stopping treatment.",
        "Bootstrap stopped locally.",
    ]
    ledger = SQLiteEventLedger(str(db))
    assert (
        ledger.list_events("cli-w")[0].payload["raw_input"]
        == "free form operator words\n"
    )
    assert (
        ledger.list_events("cli-w")[-1].kind == "operator.bootstrap.stopping_occurred"
    )
