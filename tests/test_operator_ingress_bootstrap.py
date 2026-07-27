from io import BytesIO, StringIO
from pathlib import Path
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
from seed_runtime.operator_ingress_common_grammar_prerequisite import (
    CHOICE_SET_REF,
    bootstrap_choice_set,
    run_operator_ingress_common_grammar_probe_attempt,
    validate_capture_for_probe,
)
from seed_runtime.operator_ingress_representation import (
    CapturedOperatorMaterial,
    capture_stdin_material,
)
from seed_runtime.state import StateProjector
from scripts import seed_local


def run_attempt(text, ledger=None, session="s"):
    ledger = ledger or EventLedger()
    output = StringIO()
    input_stream = StringIO(text)
    captured_ingress = capture_stdin_material(input_stream)
    view = run_operator_ingress_common_grammar_probe_attempt(
        ledger=ledger,
        workspace_id="w",
        session_id=session,
        captured_ingress=captured_ingress,
        response_input_stream=input_stream,
        output_stream=output,
    )
    return ledger, view, output.getvalue()


@pytest.mark.parametrize(
    "token,treatment",
    [("1", "common-grammar-acquisition"), ("2", "local-stop")],
)
def test_exact_treatments_select_without_acquisition_or_bounded_stop(token, treatment):
    ledger, view, output = run_attempt(f"do something exactly\n{token}\n")
    assert view["selected_treatment"] == treatment
    assert view.get("closed") is None
    kinds = [event.kind for event in ledger.list_events("w")]
    assert "operator.bootstrap.treatment_selected" in kinds
    assert "operator.bootstrap.stopping_occurred" not in kinds
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
    assert (
        view["current_standing"]["binding_finding"]["dimensions"]["standing"]
        == "unsupported"
    )
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
    assert not any(
        event.kind == "operator.bootstrap.stopping_occurred"
        for event in ledger.list_events()
    )


def test_eof_is_distinct_from_empty_response():
    eof_ledger, eof, _ = run_attempt("hello\n")
    _, empty, _ = run_attempt("hello\n\n", session="empty")
    assert eof["response_kind"] == "eof"
    assert empty["response_kind"] == "empty"
    eof_kinds = [event.kind for event in eof_ledger.list_events("w")]
    assert "operator.bootstrap.response_eof_occurred" in eof_kinds
    assert "operator.bootstrap.stopping_occurred" in eof_kinds
    assert "operator.bootstrap.response_captured" not in eof_kinds
    assert "operator.bootstrap.binding_completed" not in eof_kinds
    assert "operator.bootstrap.unsupported_finding" not in eof_kinds
    assert "capture_ref" not in eof
    assert "binding_id" not in eof


def test_initial_eof_records_eof_and_separate_stop_without_probe():
    ledger, view, output = run_attempt("")
    assert [event.kind for event in ledger.list_events("w")] == [
        "operator.bootstrap.raw_material_captured",
        "operator.bootstrap.initial_eof_occurred",
        "operator.bootstrap.stopping_occurred",
    ]
    assert view["representation_examinations"] == {}
    assert view["closed"] is True
    assert (
        view["current_standing"]["interaction_closure"]["dimensions"]["standing"]
        == "closed"
    )
    assert "selected_treatment" not in view
    assert output == "Bootstrap stopped locally.\n"
    stop = ledger.list_events("w")[-1]
    assert stop.payload["dimensions"]["authority_warrant"] == (
        "closes only this interaction"
    )


def test_exact_ingress_preservation_all_dimensions_and_durable_replay(tmp_path):
    path = tmp_path / "events.db"
    ledger, view, _ = run_attempt(
        "  Mixed CASE ingress  \n2\n", SQLiteEventLedger(str(path))
    )
    ingress = next(
        e
        for e in ledger.list_events("w")
        if e.kind == "operator.bootstrap.ingress_occurred"
    )
    assert ingress.payload["raw_input"] == "  Mixed CASE ingress  \n"
    assert ingress.payload["known_loss"] == [
        "original transport bytes and prior decoder behavior are unavailable"
    ]
    assert len(view["dimensional_standing"]) == 10
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
    assert (
        view["current_standing"]["presentation"]["dimensions"]["standing"] == "consumed"
    )
    assert view["current_standing"]["response"]["dimensions"]["standing"] == "consumed"
    assert (
        view["current_standing"]["binding_finding"]["dimensions"]["standing"] == "bound"
    )
    assert (
        view["current_standing"]["presentation"]["dimensions"]["standing"] == "consumed"
    )
    assert (
        view["current_standing"]["raw_response_material"]["dimensions"]["standing"]
        == "captured"
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


@pytest.mark.parametrize(
    "text,present,response,binding,treatment,closure",
    [
        ("hello\n1\n", "consumed", "consumed", "bound", "selected", None),
        ("hello\nwat\n", "consumed", "consumed", "unsupported", None, None),
        ("hello\n2\n", "consumed", "consumed", "bound", "selected", None),
        ("", None, None, None, None, "closed"),
        ("hello\n", "consumed", "occurred", None, None, "closed"),
    ],
)
def test_subject_local_current_standing_is_asymmetric(
    text, present, response, binding, treatment, closure
):
    _, view, _ = run_attempt(text)

    def standing(subject):
        current = view["current_standing"][subject]
        return current and current["dimensions"]["standing"]

    assert standing("preserved_ingress") == "preserved"
    assert standing("presentation") == present
    assert standing("response") == response
    assert standing("binding_finding") == binding
    assert standing("treatment_selection") == treatment
    assert standing("interaction_closure") == closure


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


class _RawStdin:
    def __init__(self, material: bytes, encoding="utf-8"):
        self.buffer = BytesIO(material)
        self.encoding = encoding


def run_raw(material: bytes, *, ledger=None):
    ledger = ledger or EventLedger()
    output = StringIO()
    input_stream = _RawStdin(material)
    captured_ingress = capture_stdin_material(input_stream)
    view = run_operator_ingress_common_grammar_probe_attempt(
        ledger=ledger,
        workspace_id="raw-w",
        session_id="raw-s",
        captured_ingress=captured_ingress,
        response_input_stream=input_stream,
        output_stream=output,
    )
    return ledger, view, output.getvalue()


def run_console(material: bytes):
    ledger = EventLedger()
    output = StringIO()
    seed_local.run_persistent_operator_console(
        ledger=ledger,
        workspace_id="console-w",
        session_id="console-s",
        input_stream=_RawStdin(material),
        output_stream=output,
    )
    return ledger, output.getvalue()


def test_bare_seed_enters_persistent_console_and_announces_exit():
    completed = subprocess.run(
        [sys.executable, "scripts/seed_local.py"],
        input=b"exit\n",
        capture_output=True,
        check=True,
    )
    assert completed.stdout == b"Seed console: `exit` exits.\n"
    assert completed.returncode == 0


def test_console_passes_its_capture_unchanged_to_the_bounded_attempt(monkeypatch):
    supplied = _RawStdin(b"ordinary ingress\r\n2\nexit\n")
    received = []

    def bounded_attempt(**kwargs):
        received.append(kwargs)
        # Response ownership remains inside the bounded attempt.
        assert kwargs["response_input_stream"].buffer.readline() == b"2\n"

    monkeypatch.setattr(
        seed_local,
        "run_operator_ingress_common_grammar_probe_attempt",
        bounded_attempt,
    )
    seed_local.run_persistent_operator_console(
        ledger=EventLedger(),
        workspace_id="w",
        session_id="s",
        input_stream=supplied,
        output_stream=StringIO(),
    )

    assert len(received) == 1
    capture = received[0]["captured_ingress"]
    assert capture.exact_bytes == b"ordinary ingress\r\n"
    assert capture.delimiter_hex == "0d0a"
    assert capture.capture_boundary == "stdin.buffer.readline"
    assert capture.byte_material_origin == "direct_boundary_observation"
    assert received[0]["response_input_stream"] is supplied


def test_existing_capture_provenance_is_recorded_without_reinference():
    capture = CapturedOperatorMaterial(
        exact_bytes=b"captured elsewhere\n",
        eof=False,
        delimiter_hex="0a",
        capture_boundary="explicit-test-boundary",
        byte_material_origin="explicit-test-origin",
        encoding_testimony="utf-8",
        known_loss=("explicit-test-loss",),
    )
    ledger = EventLedger()
    run_operator_ingress_common_grammar_probe_attempt(
        ledger=ledger,
        workspace_id="w",
        session_id="s",
        captured_ingress=capture,
        response_input_stream=BytesIO(b"2\n"),
        output_stream=StringIO(),
    )
    recorded = ledger.list_events("w")[0].payload
    assert recorded["capture_boundary"] == capture.capture_boundary
    assert recorded["byte_material_origin"] == capture.byte_material_origin
    assert recorded["exact_bytes_hex"] == capture.exact_bytes.hex()
    assert recorded["known_loss"] == list(capture.known_loss)


def test_parser_has_no_alternate_operator_ingress_controller():
    parser = seed_local.build_parser()
    assert not any(
        action.dest == "operator_ingress_bootstrap" for action in parser._actions
    )


def test_console_runs_multiple_bounded_interactions_after_local_stop_and_unsupported():
    ledger, output = run_console(b"first ingress\n2\nsecond ingress\nnot-a-token\nexit\n")
    attempts = StateProjector(ledger).project("console-w").operator_ingress_bootstraps
    assert len(attempts) == 2
    assert {view.get("selected_treatment") for view in attempts.values()} == {
        "local-stop",
        None,
    }
    assert any(
        view.get("current_standing", {})
        .get("binding_finding", {})
        .get("dimensions", {})
        .get("standing")
        == "unsupported"
        for view in attempts.values()
    )
    assert output.count("Select one treatment by its exact token:") == 2
    assert "Local-stop treatment selected; bounded stop was not established." in output
    assert "Unsupported response" in output


def test_outer_exit_is_not_operator_ingress_and_capture_keeps_provenance():
    ledger, _ = run_console(b"\xff\nexit\n")
    events = ledger.list_events("console-w")
    captures = [
        event
        for event in events
        if event.kind == "operator.bootstrap.raw_material_captured"
    ]
    assert len(captures) == 1
    assert captures[0].payload["exact_bytes_hex"] == "ff0a"
    assert captures[0].payload["capture_boundary"] == "stdin.buffer.readline"
    assert captures[0].payload["byte_material_origin"] == "direct_boundary_observation"
    assert b"exit\n".hex() not in str([event.payload for event in events])


def test_stdin_buffer_capture_preserves_exact_boundary_bytes_and_decoder_testimony(
    tmp_path,
):
    path = tmp_path / "raw.db"
    ledger, view, _ = run_raw("é\r\n2\n".encode(), ledger=SQLiteEventLedger(str(path)))
    raw, examination = ledger.list_events("raw-w")[:2]
    assert raw.payload["exact_bytes_hex"] == "é\r\n".encode().hex()
    assert raw.payload["delimiter_hex"] == "0d0a"
    assert raw.payload["capture_boundary"] == "stdin.buffer.readline"
    assert raw.payload["byte_material_origin"] == "direct_boundary_observation"
    assert raw.payload["encoding_testimony"] == "utf-8"
    assert examination.kind == "operator.bootstrap.representation_examined"
    assert examination.payload["decoder_mechanism"] == "utf-8"
    assert examination.payload["decoder_succeeded"] is True
    assert examination.payload["decoder_failure"] is None
    projected = view["representation_examinations"]["initial_ingress"]
    assert projected["decoder_succeeded"] is True
    assert "admission" not in projected
    assert "competency" not in str(projected).lower()
    ledger.close()
    replay = StateProjector(SQLiteEventLedger(str(path))).project("raw-w")
    assert (
        replay.operator_ingress_bootstraps[
            next(iter(replay.operator_ingress_bootstraps))
        ]
        == view
    )


def test_stringio_capture_identifies_text_reencoding_and_preserves_known_loss():
    ledger, _, _ = run_attempt("hello\n2\n")
    raw = ledger.list_events("w")[0]
    assert raw.payload["exact_bytes_hex"] == b"hello\n".hex()
    assert (
        raw.payload["byte_material_origin"]
        == "text_reencoding_after_prior_decoding"
    )
    assert raw.payload["encoding_testimony"] is None
    assert raw.payload["capture_boundary"] == "text-stream adapter after prior decoding"
    assert raw.payload["known_loss"] == [
        "original transport bytes and prior decoder behavior are unavailable"
    ]
    examination = ledger.list_events("w")[1]
    assert examination.payload["decoder_mechanism"] == "utf-8"
    assert (
        examination.payload["decoder_mechanism_selection"]
        == "implementation_utf8_fallback"
    )
    assert examination.payload["decoder_outcome"] == "decoded"


def test_decoder_success_does_not_claim_admission_interpretation_or_competency():
    ledger, view, _ = run_raw(b"ASCII\n2\n")
    examination = ledger.list_events("raw-w")[1]
    assert examination.payload["decoder_succeeded"] is True
    forbidden = ("admission", "admitted", "interpretation", "competency")
    assert not any(word in str(examination.payload).lower() for word in forbidden)
    assert not any(
        word in str(view["representation_examinations"]).lower() for word in forbidden
    )


def test_production_operator_ingress_contains_no_pesc_identifier_or_payload():
    forbidden = "pe" + "sc"
    production = Path("seed_runtime/operator_ingress_common_grammar_prerequisite.py").read_text()
    production += Path("seed_runtime/operator_ingress_representation.py").read_text()
    assert forbidden not in production.lower()


def test_production_and_event_payloads_do_not_claim_source_relative_original_bytes():
    forbidden = "original_transport" + "_bytes"
    production = Path("seed_runtime/operator_ingress_common_grammar_prerequisite.py").read_text()
    production += Path("seed_runtime/operator_ingress_representation.py").read_text()
    assert forbidden not in production

    ledgers = (run_raw(b"hello\n2\n")[0], run_attempt("hello\n2\n")[0])
    for ledger in ledgers:
        assert forbidden not in str(
            [event.payload for event in ledger.list_events()]
        )


def test_invalid_initial_bytes_are_preserved_without_replacement_and_stop_before_enum():
    ledger, view, output = run_raw(b"\xff\n1\n")
    assert output == (
        "Representation insufficient: captured material did not decode under "
        "the selected decoder mechanism.\n"
    )
    events = ledger.list_events("raw-w")
    assert events[0].payload["exact_bytes_hex"] == "ff0a"
    assert events[1].payload["decoder_succeeded"] is False
    assert "\ufffd" not in str([event.payload for event in events])
    assert not any(
        e.kind
        in {
            "operator.bootstrap.probe_produced",
            "operator.bootstrap.presentation_occurred",
            "operator.bootstrap.response_captured",
            "operator.bootstrap.binding_completed",
        }
        for e in events
    )
    assert (
        view["representation_examinations"]["initial_ingress"]["decoder_succeeded"]
        is False
    )


def test_invalid_enum_bytes_stop_before_token_capture_or_binding():
    ledger, _, output = run_raw(b"hello\n\xff\n")
    assert "Select one treatment" in output
    assert output.endswith(
        "Representation insufficient: captured response did not decode under the selected decoder mechanism.\n"
    )
    events = ledger.list_events("raw-w")
    assert not any(
        e.kind
        in {
            "operator.bootstrap.response_captured",
            "operator.bootstrap.binding_completed",
            "operator.bootstrap.unsupported_finding",
        }
        for e in events
    )
    assert not any(
        any(term in e.kind for term in ("demand", "acquisition", "boge", "cluster"))
        for e in events
    )


def test_empty_material_and_eof_have_distinct_raw_evidence():
    empty_ledger, _, _ = run_raw(b"\n2\n")
    eof_ledger, _, _ = run_raw(b"")
    empty = empty_ledger.list_events("raw-w")[0].payload
    eof = eof_ledger.list_events("raw-w")[0].payload
    assert (empty["exact_bytes_hex"], empty["eof"], empty["delimiter_hex"]) == (
        "0a",
        False,
        "0a",
    )
    assert (eof["exact_bytes_hex"], eof["eof"], eof["delimiter_hex"]) == (
        "",
        True,
        None,
    )


def test_initial_and_response_eof_do_not_claim_representation_examination():
    initial_ledger, initial_view, _ = run_raw(b"")
    response_ledger, response_view, _ = run_raw(b"hello\n")
    assert not any(
        event.kind == "operator.bootstrap.representation_examined"
        for event in initial_ledger.list_events("raw-w")
    )
    response_examinations = [
        event
        for event in response_ledger.list_events("raw-w")
        if event.kind == "operator.bootstrap.representation_examined"
    ]
    assert [event.payload["material_role"] for event in response_examinations] == [
        "initial_ingress"
    ]
    assert initial_view["representation_examinations"] == {}
    assert "enum_response" not in response_view["representation_examinations"]
    eof_event = next(
        event
        for event in response_ledger.list_events("raw-w")
        if event.kind == "operator.bootstrap.response_eof_occurred"
    )
    raw_response = next(
        event
        for event in response_ledger.list_events("raw-w")
        if event.kind == "operator.bootstrap.raw_material_captured"
        and event.payload["material_role"] == "enum_response"
    )
    assert raw_response.id in eof_event.payload["lineage"]


def test_decoder_outcomes_and_selection_sources_remain_distinct():
    unavailable_ledger, _, _ = run_operator_with_stream(
        _RawStdin(b"hello\n", "x-no-such-codec")
    )
    rejected_ledger, _, _ = run_raw(b"\xff\n")
    success_ledger, _, _ = run_raw(b"hello\n2\n")
    unavailable = unavailable_ledger.list_events("raw-w")[1].payload
    rejected = rejected_ledger.list_events("raw-w")[1].payload
    success = success_ledger.list_events("raw-w")[1].payload
    assert unavailable["decoder_outcome"] == "decoder_unavailable"
    assert unavailable["decoder_mechanism_selection"] == "stream_encoding_testimony"
    assert unavailable["decoder_failure"].startswith("LookupError:")
    assert rejected["decoder_outcome"] == "bytes_rejected"
    assert rejected["decoder_failure"].startswith("UnicodeDecodeError:")
    assert success["decoder_outcome"] == "decoded"
    assert success["decoder_failure"] is None

    for ledger, expected in (
        (unavailable_ledger, "decoder_unavailable"),
        (rejected_ledger, "bytes_rejected"),
        (success_ledger, "decoded"),
    ):
        examination = ledger.list_events("raw-w")[1]
        assert examination.payload["dimensions"]["standing"] == expected


def run_operator_with_stream(stream):
    ledger = EventLedger()
    output = StringIO()
    captured_ingress = capture_stdin_material(stream)
    view = run_operator_ingress_common_grammar_probe_attempt(
        ledger=ledger,
        workspace_id="raw-w",
        session_id="raw-s",
        captured_ingress=captured_ingress,
        response_input_stream=stream,
        output_stream=output,
    )
    return ledger, view, output.getvalue()


def test_utf8_fallback_is_implementation_selected_and_direct_bytesio_is_exact():
    ledger, _, _ = run_operator_with_stream(BytesIO(b"\xc3\xa9\n2\n"))
    raw, examination = ledger.list_events("raw-w")[:2]
    assert raw.payload["exact_bytes_hex"] == b"\xc3\xa9\n".hex()
    assert raw.payload["byte_material_origin"] == "direct_boundary_observation"
    assert (
        raw.payload["capture_boundary"]
        == "binary-stream.readline (bytes observed directly)"
    )
    assert raw.payload["encoding_testimony"] is None
    assert examination.payload["decoder_mechanism"] == "utf-8"
    assert (
        examination.payload["decoder_mechanism_selection"]
        == "implementation_utf8_fallback"
    )


def test_representation_evidence_produces_no_broader_standing():
    ledger, view, _ = run_raw(b"hello\n2\n")
    evidence = str(
        [
            event.payload
            for event in ledger.list_events("raw-w")
            if event.kind
            in {
                "operator.bootstrap.raw_material_captured",
                "operator.bootstrap.representation_examined",
            }
        ]
        + [view["representation_examinations"]]
    ).lower()
    assert not any(
        word in evidence
        for word in (
            "admission",
            "interpretation",
            "grammar",
            "competency",
            "demand",
            "boge",
        )
    )
