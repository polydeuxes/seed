from io import BytesIO, StringIO
from pathlib import Path
import subprocess
import sys

import pytest

from seed_runtime.events import EventLedger, SQLiteEventLedger
from seed_runtime.operator_ingress_common_grammar_prerequisite import (
    run_operator_ingress_common_grammar_probe_attempt,
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


def test_historical_presentation_eligibility_event_still_projects():
    """Historical projection compatibility witness, not current producer reachability or uptake."""
    ledger = EventLedger()
    historical = ledger.append(
        "operator.ingress.common_grammar.presentation_eligibility_examined",
        "w",
        {
            "attempt_ref": "attempt:historical",
            "dimensions": {
                "identity": "presentation-eligibility:historical",
                "content": "historical eligibility payload",
                "standing": "eligible",
            },
            "presentation_purpose_id": "purpose:historical",
            "eligibility_relation": "is eligible for exact presentation purpose",
            "eligibility_result": "eligible",
            "mutates_cluster": False,
        },
        session_id="s",
    )

    view = (
        StateProjector(ledger)
        .project("w")
        .operator_ingress_common_grammar_attempts["attempt:historical"]
    )
    projected = view["current_standing"]["presentation_eligibility"]
    assert projected["evidence_event_id"] == historical.id
    assert projected["dimensions"] == historical.payload["dimensions"]
    assert view["presentation_purpose_id"] == "purpose:historical"
    assert view["eligibility_relation"] == "is eligible for exact presentation purpose"
    assert view["eligibility_result"] == "eligible"


def test_historical_potential_goal_standing_event_still_projects():
    """Historical projection compatibility witness, not producer reachability or authority."""
    ledger = EventLedger()
    historical = ledger.append(
        "operator.ingress.common_grammar.potential_goal_standing_examined",
        "w",
        {
            "attempt_ref": "attempt:historical-standing",
            "dimensions": {
                "identity": "bounded-potential-goal-standing:historical",
                "content": "historical standing payload",
                "standing": "established",
            },
            "standing_subject": "source:historical",
            "standing_relation": "has bounded potential-goal standing",
            "standing_result": "established",
            "source_role_testimony_ref": "testimony:historical",
            "source_role_testimony": {"attributed_role": "historical-role"},
            "mutates_cluster": False,
        },
        session_id="s",
    )

    view = (
        StateProjector(ledger)
        .project("w")
        .operator_ingress_common_grammar_attempts["attempt:historical-standing"]
    )
    projected = view["current_standing"]["potential_goal_standing"]
    assert projected["evidence_event_id"] == historical.id
    assert projected["dimensions"] == historical.payload["dimensions"]
    assert view["standing_result"] == "established"
    assert view["current_standing"]["source_role_testimony"] == {
        "subject_ref": "testimony:historical",
        "testimony": {"attributed_role": "historical-role"},
        "evidence_event_id": historical.id,
    }


def test_initial_eof_records_eof_and_separate_stop_without_probe():
    ledger, view, output = run_attempt("")
    assert [event.kind for event in ledger.list_events("w")] == [
        "operator.ingress.common_grammar.raw_material_captured",
        "operator.ingress.common_grammar.initial_eof_occurred",
        "operator.ingress.common_grammar.stopping_occurred",
    ]
    assert view["representation_examinations"] == {}
    assert view["closed"] is True
    assert (
        view["current_standing"]["interaction_closure"]["dimensions"]["standing"]
        == "closed"
    )
    assert output == "Operator-ingress common-grammar interaction stopped locally.\n"
    stop = ledger.list_events("w")[-1]
    assert stop.payload["dimensions"]["authority_warrant"] == (
        "closes only this interaction"
    )


@pytest.mark.parametrize(
    ("material", "ingress_kind", "content"),
    [
        (b"Exact ingress \xc3\xa9\r\n", "text", "Exact ingress \xe9"),
        (b"\n", "empty", ""),
    ],
)
def test_decoded_non_eof_ingress_returns_after_preservation_and_projection(
    material, ingress_kind, content
):
    ledger = EventLedger()
    output = StringIO()
    captured = capture_stdin_material(BytesIO(material))

    class ResponseInputMustNotBeRead:
        def readline(self):
            pytest.fail("decoded ingress must not trigger a response read")

    view = run_operator_ingress_common_grammar_probe_attempt(
        ledger=ledger,
        workspace_id="w",
        session_id="s",
        captured_ingress=captured,
        response_input_stream=ResponseInputMustNotBeRead(),
        output_stream=output,
    )

    events = ledger.list_events("w")
    assert [event.kind for event in events] == [
        "operator.ingress.common_grammar.raw_material_captured",
        "operator.ingress.common_grammar.representation_examined",
        "operator.ingress.common_grammar.ingress_occurred",
    ]
    capture, examination, ingress = events
    assert capture.payload["exact_bytes_hex"] == material.hex()
    assert examination.payload["lineage"] == [capture.id]
    assert examination.payload["decoder_outcome"] == "decoded"
    assert ingress.payload["ingress_kind"] == ingress_kind
    assert ingress.payload["raw_input"] == material.decode()
    assert ingress.payload["decoded_text"] == material.decode()
    assert ingress.payload["lineage"] == [capture.id, examination.id]
    assert ingress.payload["dimensions"]["content"] == content
    assert ingress.payload["dimensions"]["authority_warrant"] == (
        "occurrence-only; meaning Unknown"
    )
    assert view["event_ids"] == [event.id for event in events]
    assert view["last_event_kind"] == ingress.kind
    assert view["current_standing"]["preserved_ingress"] == {
        "subject_ref": ingress.payload["attempt_ref"],
        "dimensions": {
            **ingress.payload["dimensions"],
            "standing": "preserved",
        },
        "evidence_event_id": ingress.id,
    }
    assert (
        view["representation_examinations"]["initial_ingress"]["examination_event_id"]
        == examination.id
    )
    assert view["known_loss"] == list(captured.known_loss)
    assert view["unknowns"] == []
    assert view["current_standing"]["interaction_closure"] is None
    assert "addressable_operator_material" in view
    assert output.getvalue() == ""


def test_console_recurs_after_each_quiescent_non_eof_attempt():
    ledger, output = run_console(b"first ingress\nsecond ingress\nexit\n")
    events = ledger.list_events("console-w")
    assert [event.kind for event in events] == [
        kind
        for _ in range(2)
        for kind in (
            "operator.ingress.common_grammar.raw_material_captured",
            "operator.ingress.common_grammar.representation_examined",
            "operator.ingress.common_grammar.ingress_occurred",
        )
    ]
    assert [
        event.payload["decoded_text"]
        for event in events
        if event.kind == "operator.ingress.common_grammar.ingress_occurred"
    ] == ["first ingress\n", "second ingress\n"]
    assert (
        len(
            StateProjector(ledger)
            .project("console-w")
            .operator_ingress_common_grammar_attempts
        )
        == 2
    )
    assert output == "Seed console: `exit` exits.\n"


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
        action.dest == "operator_ingress_common_grammar" for action in parser._actions
    )


def test_outer_exit_is_not_operator_ingress_and_capture_keeps_provenance():
    ledger, _ = run_console(b"\xff\nexit\n")
    events = ledger.list_events("console-w")
    captures = [
        event
        for event in events
        if event.kind == "operator.ingress.common_grammar.raw_material_captured"
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
    assert examination.kind == "operator.ingress.common_grammar.representation_examined"
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
        replay.operator_ingress_common_grammar_attempts[
            next(iter(replay.operator_ingress_common_grammar_attempts))
        ]
        == view
    )


def test_stringio_capture_identifies_text_reencoding_and_preserves_known_loss():
    ledger, _, _ = run_attempt("hello\n2\n")
    raw = ledger.list_events("w")[0]
    assert raw.payload["exact_bytes_hex"] == b"hello\n".hex()
    assert raw.payload["byte_material_origin"] == "text_reencoding_after_prior_decoding"
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
    production = Path(
        "seed_runtime/operator_ingress_common_grammar_prerequisite.py"
    ).read_text()
    production += Path("seed_runtime/operator_ingress_representation.py").read_text()
    assert forbidden not in production.lower()


def test_production_and_event_payloads_do_not_claim_source_relative_original_bytes():
    forbidden = "original_transport" + "_bytes"
    production = Path(
        "seed_runtime/operator_ingress_common_grammar_prerequisite.py"
    ).read_text()
    production += Path("seed_runtime/operator_ingress_representation.py").read_text()
    assert forbidden not in production

    ledgers = (run_raw(b"hello\n2\n")[0], run_attempt("hello\n2\n")[0])
    for ledger in ledgers:
        assert forbidden not in str([event.payload for event in ledger.list_events()])


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
            "operator.ingress.common_grammar.probe_produced",
            "operator.ingress.common_grammar.presentation_occurred",
            "operator.ingress.common_grammar.response_captured",
            "operator.ingress.common_grammar.binding_completed",
        }
        for e in events
    )
    assert (
        view["representation_examinations"]["initial_ingress"]["decoder_succeeded"]
        is False
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
                "operator.ingress.common_grammar.raw_material_captured",
                "operator.ingress.common_grammar.representation_examined",
            }
        ]
        + [view["representation_examinations"]]
    ).lower()
    assert not any(
        word in evidence
        for word in (
            "admission",
            "interpretation",
            "competency",
            "demand",
            "bounded-goal-applicability",
        )
    )
