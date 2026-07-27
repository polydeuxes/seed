from io import StringIO
import subprocess
import sys

import pytest

from seed_runtime.bounded_operator_goal_establishment import (
    BoundedOperatorGoalEstablishmentError,
    establish_bounded_operator_goal_from_closed_choice,
)
from seed_runtime.closed_choice_selection_binding import (
    ClosedChoiceSelectionBindingError,
    OperatorSelectionTokenCapture,
)
from seed_runtime.events import EventLedger, SQLiteEventLedger
from seed_runtime.diagnostic_inventory import DIAGNOSTIC_INVENTORY
from seed_runtime.diagnostic_shape_audit import build_diagnostic_shape_audit
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


def test_exact_ingress_preservation_all_dimensions_and_durable_replay(tmp_path):
    path = tmp_path / "events.db"
    ledger, view, _ = run_attempt(
        "  Mixed CASE ingress  \n1\n", SQLiteEventLedger(str(path))
    )
    ingress = ledger.list_events("w")[0]
    assert ingress.payload["raw_input"] == "  Mixed CASE ingress  \n"
    assert ingress.payload["known_loss"] == [
        "terminal framing outside captured line is not preserved"
    ]
    assert set(view["dimensions"]) == {
        "identity",
        "content",
        "standing",
        "source_provenance",
        "responsibility",
        "authority_warrant",
        "scope_locality",
        "occurrence_preservation",
    }
    ledger.close()
    reopened = SQLiteEventLedger(str(path))
    replayed = (
        StateProjector(reopened)
        .project("w")
        .operator_ingress_bootstraps["operator-bootstrap:s"]
    )
    assert replayed == view
    assert all(
        event.payload["mutates_cluster"] is False for event in reopened.list_events("w")
    )


def test_probe_identity_replay_guards_and_boge_refusal():
    choice = bootstrap_choice_set("presentation:1")
    capture = OperatorSelectionTokenCapture("capture:1", CHOICE_SET_REF, "1")
    binding = validate_capture_for_probe(choice, capture, "presentation:1")
    with pytest.raises(ClosedChoiceSelectionBindingError):
        validate_capture_for_probe(choice, capture, "presentation:wrong")
    with pytest.raises(ClosedChoiceSelectionBindingError):
        validate_capture_for_probe(choice, capture, "presentation:1", ("capture:1",))
    with pytest.raises(BoundedOperatorGoalEstablishmentError):
        establish_bounded_operator_goal_from_closed_choice(binding)


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


def test_bootstrap_probe_is_visible_and_shape_audited():
    entry = next(
        item
        for item in DIAGNOSTIC_INVENTORY
        if item.name == "operator_ingress_bootstrap"
    )
    assert entry.cli_flags == ("--operator-ingress-bootstrap",)
    assert entry.writes_event_ledger is True
    assert entry.mutates_cluster is False
    rows = [
        row for row in build_diagnostic_shape_audit() if row.diagnostic == entry.name
    ]
    assert len(rows) == 9
    assert not [row for row in rows if row.status == "mismatch"]
