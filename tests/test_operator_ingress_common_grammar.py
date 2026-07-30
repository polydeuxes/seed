from io import BytesIO, StringIO
from dataclasses import replace
from pathlib import Path
import subprocess
import sys

import pytest

from seed_runtime.closed_choice_selection_binding import (
    ClosedChoiceOption,
    ClosedChoiceSelectionBindingError,
    OperatorSelectionTokenCapture,
    PresentedClosedChoiceSet,
    bind_closed_choice_selection,
)
from seed_runtime.bounded_operator_goal_establishment import (
    BoundedOperatorGoalEstablishmentError,
    establish_bounded_operator_goal_from_closed_choice,
)
from seed_runtime.events import EventLedger, SQLiteEventLedger
from seed_runtime.operator_ingress_common_grammar_prerequisite import (
    APPLICATION_SOURCE_MEANING_CONVENTION,
    RENDERING_KNOWN_LOSS,
    SOURCE_MEANING_CONVENTIONS,
    SOURCE_MEANING_TESTIMONIES,
    _dimensions,
    _examine_meaning_relation_for_bounded_operator_goal_establishment,
    _record,
    _recordable_binding_testimony,
    _recordable_presented_options,
    _representation_fingerprint,
    _warrant_source_meaning_relation,
    common_grammar_choice_set,
    common_grammar_representation_lineages,
    _recover_represented_source,
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


def _rewarrant(ledger, recovery, *, testimony=None, convention=None):
    return _warrant_source_meaning_relation(
        ledger=ledger,
        workspace_id="w",
        session_id="s",
        attempt_ref=recovery.payload["attempt_ref"],
        source_recovery=recovery,
        testimony=testimony,
        convention=convention,
    )


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


# Disconnected downstream helper-contract witnesses
# This fixture exercises bounded helper contracts directly. It does not represent
# an active operator-ingress production road.


def _record_preconsumption_probe_fixture(
    *, ledger=None, token="1", attempt="attempt:helper"
):
    """Disconnected helper-contract testimony, not the active production road."""
    ledger = ledger or EventLedger()
    presentation_ref = "presentation:helper"
    choice = common_grammar_choice_set(presentation_ref)
    representation_ref = "representation:helper"
    rows = common_grammar_representation_lineages(choice, representation_ref)
    payload = [vars(row) for row in rows]

    def dims(identity, standing, responsibility):
        return _dimensions(
            identity=identity,
            content="bounded fixture",
            standing=standing,
            source="test fixture",
            responsibility=responsibility,
            authority="local contract only",
            scope=f"attempt:{attempt}",
            occurrence="direct bounded fixture occurrence",
        )

    represented = _record(
        ledger,
        "operator.ingress.common_grammar.alternatives_represented",
        "w",
        "s",
        attempt,
        dims(
            representation_ref,
            "preserved-before-selection",
            "responsible-alternative-representation",
        ),
        choice_set_ref=choice.choice_set_ref,
        presentation_ref=presentation_ref,
        choice_set_fingerprint=choice.exact_choice_set_fingerprint,
        representations=payload,
        representation_evidence_fingerprint=_representation_fingerprint(payload),
        known_loss=list(RENDERING_KNOWN_LOSS),
        lineage=[],
    )
    presented = _record(
        ledger,
        "operator.ingress.common_grammar.presentation_occurred",
        "w",
        "s",
        attempt,
        dims(presentation_ref, "presented", "presentation"),
        choice_set_ref=choice.choice_set_ref,
        presentation_ref=presentation_ref,
        choice_set_fingerprint=choice.exact_choice_set_fingerprint,
        lineage=[represented.id],
    )
    capture_ref = "capture:helper"
    response = _record(
        ledger,
        "operator.ingress.common_grammar.response_captured",
        "w",
        "s",
        attempt,
        dims(capture_ref, "captured", "response-capture"),
        raw_input=token + "\n",
        response_kind="token",
        choice_set_ref=choice.choice_set_ref,
        presentation_ref=presentation_ref,
        capture_ref=capture_ref,
        choice_set_fingerprint=choice.exact_choice_set_fingerprint,
        lineage=[presented.id],
    )
    capture = OperatorSelectionTokenCapture(
        capture_ref, choice.choice_set_ref, token, provenance=(response.id,)
    )
    binding = bind_closed_choice_selection(choice, capture)
    return ledger, choice, capture, binding, represented, presented, response


def _record_consumed_probe_fixture(*, ledger=None, token="1", attempt="attempt:helper"):
    """Disconnected consumed testimony, not the active production road."""
    fixture = _record_preconsumption_probe_fixture(
        ledger=ledger, token=token, attempt=attempt
    )
    ledger, choice, capture, binding, represented, presented, response = fixture

    def dims(identity, standing, responsibility):
        return _dimensions(
            identity=identity,
            content="bounded fixture",
            standing=standing,
            source="test fixture",
            responsibility=responsibility,
            authority="local contract only",
            scope=f"attempt:{attempt}",
            occurrence="direct bounded fixture occurrence",
        )

    binding_event = _record(
        ledger,
        "operator.ingress.common_grammar.binding_completed",
        "w",
        "s",
        attempt,
        dims(binding.binding_id, "bound", "exact-set-binding"),
        binding_id=binding.binding_id,
        binding_testimony=_recordable_binding_testimony(binding),
        capture_ref=capture.capture_ref,
        choice_set_ref=choice.choice_set_ref,
        presented_options=_recordable_presented_options(choice),
        selected_presented_alternative_ref=binding.selected_presented_alternative_ref,
        response_kind="token",
        unknowns=[],
        choice_set_fingerprint=choice.exact_choice_set_fingerprint,
        lineage=[response.id, presented.id],
    )
    selected = _record(
        ledger,
        "operator.ingress.common_grammar.alternative_selected",
        "w",
        "s",
        attempt,
        dims(
            binding.selected_presented_alternative_ref,
            "selected",
            "presented-alternative-selection",
        ),
        selected_presented_alternative_ref=binding.selected_presented_alternative_ref,
        binding_id=binding.binding_id,
        lineage=[binding_event.id],
    )
    return (
        *fixture,
        binding_event,
        selected,
    )


def _record_source_recovery_fixture(*, token="1"):
    """Disconnected recovery testimony, not the active production road."""
    fixture = _record_consumed_probe_fixture(token=token)
    ledger, choice, _, binding, represented, presented, _, binding_event, selected = (
        fixture
    )
    recovered, refusal = _recover_represented_source(
        binding,
        choice,
        represented,
        ledger=ledger,
        workspace_id="w",
        attempt_ref="attempt:helper",
        presentation_occurrence=presented,
        selection_occurrence=selected,
    )
    assert refusal is None
    recovery = _record(
        ledger,
        "operator.ingress.common_grammar.source_recovered",
        "w",
        "s",
        "attempt:helper",
        _dimensions(
            identity=f"source-recovery:{selected.id}",
            content=recovered.represented_source_ref,
            standing="recovered",
            source=represented.id,
            responsibility="represented-source-recovery",
            authority="recovery only",
            scope="attempt:helper",
            occurrence="direct bounded fixture occurrence",
        ),
        recovered_source_ref=recovered.represented_source_ref,
        recovered_source_role=recovered.represented_source_role,
        recovered_source_proposition=recovered.proposition_assertion,
        selected_presented_alternative_ref=recovered.presented_alternative_ref,
        representation_occurrence_id=represented.id,
        binding_occurrence_id=binding_event.id,
        known_loss=list(recovered.representation_known_loss),
        lineage=[represented.id, presented.id, binding_event.id, selected.id],
    )
    return fixture, recovery


def test_direct_representation_and_source_recovery_preserve_exact_distinctions():
    fixture, recovery = _record_source_recovery_fixture()
    _, choice, _, _, represented, presented, response, binding_event, selected = fixture
    row = represented.payload["representations"][0]
    assert (
        len(
            {
                "1",
                row["presented_alternative_ref"],
                row["represented_source_ref"],
                row["rendered_label"],
                row["proposition_assertion"],
            }
        )
        == 5
    )
    assert row["rendered_label"] != row["proposition_assertion"]
    assert row["exact_choice_set_fingerprint"] == choice.exact_choice_set_fingerprint
    assert (
        row["producer_occurrence_ref"] == represented.payload["dimensions"]["identity"]
    )
    assert recovery.payload["lineage"] == [
        represented.id,
        presented.id,
        binding_event.id,
        selected.id,
    ]
    assert response.id in binding_event.payload["lineage"]
    assert tuple(recovery.payload["known_loss"]) == row["known_loss"]


@pytest.mark.parametrize(
    "change,reason",
    [
        ({"testimony_id": "wrong"}, "meaning_testimony_identity_mismatch"),
        ({"source_ref": "source:wrong"}, "meaning_testimony_identity_mismatch"),
        ({"source_role": "wrong"}, "source_role_mismatch"),
        ({"proposition": "changed"}, "proposition_mismatch"),
        (
            {"relation_assertion": "identifies"},
            "meaning_testimony_relation_not_expresses",
        ),
        (
            {"attributed_supplier": ""},
            "meaning_testimony_attribution_absent_or_mismatched",
        ),
        (
            {"producer_declaration_ref": ""},
            "meaning_testimony_declaration_reference_absent",
        ),
        ({"provenance": ()}, "meaning_testimony_provenance_absent"),
        (
            {"declared_application_purpose": "wrong"},
            "meaning_testimony_purpose_mismatch",
        ),
        ({"scope": "wrong"}, "meaning_testimony_scope_mismatch"),
        ({"unknowns": ("unknown",)}, "meaning_testimony_unknown"),
        ({"conflicts": ("conflict",)}, "meaning_testimony_conflicting"),
    ],
)
def test_direct_meaning_testimony_refusal_surface(change, reason):
    fixture, recovery = _record_source_recovery_fixture()
    testimony = replace(
        SOURCE_MEANING_TESTIMONIES[recovery.payload["recovered_source_ref"]], **change
    )
    assert (
        _rewarrant(
            fixture[0],
            recovery,
            testimony=testimony,
            convention=APPLICATION_SOURCE_MEANING_CONVENTION,
        ).payload["refusal_reason"]
        == reason
    )


@pytest.mark.parametrize(
    "change,reason",
    [
        ({"convention_id": "wrong"}, "constitutive_convention_identity_mismatch"),
        (
            {"attribution": ""},
            "constitutive_convention_attribution_absent_or_mismatched",
        ),
        ({"applicable_authority": ()}, "constitutive_convention_authority_absent"),
        (
            {"permitted_testimony_kind": "Other"},
            "constitutive_convention_testimony_form_not_permitted",
        ),
        (
            {"permitted_relation_form": "represents"},
            "constitutive_convention_does_not_permit_expresses",
        ),
        ({"purpose": ""}, "constitutive_convention_purpose_mismatch"),
        ({"scope": ""}, "constitutive_convention_scope_mismatch"),
        ({"unknowns": ("unknown",)}, "constitutive_convention_unknown"),
        ({"conflicts": ("conflict",)}, "constitutive_convention_conflicting"),
    ],
)
def test_direct_constitutive_convention_refusal_surface(change, reason):
    fixture, recovery = _record_source_recovery_fixture()
    testimony = SOURCE_MEANING_TESTIMONIES[recovery.payload["recovered_source_ref"]]
    assert (
        _rewarrant(
            fixture[0],
            recovery,
            testimony=testimony,
            convention=replace(APPLICATION_SOURCE_MEANING_CONVENTION, **change),
        ).payload["refusal_reason"]
        == reason
    )


def test_direct_exact_meaning_warrant_and_missing_inputs_are_distinct():
    fixture, recovery = _record_source_recovery_fixture()
    testimony = SOURCE_MEANING_TESTIMONIES[recovery.payload["recovered_source_ref"]]
    warranted = _rewarrant(
        fixture[0],
        recovery,
        testimony=testimony,
        convention=SOURCE_MEANING_CONVENTIONS[testimony.source_ref],
    )
    assert (
        warranted.kind.endswith("meaning_relation_warranted")
        and warranted.payload["source_recovery_occurrence_id"] == recovery.id
    )
    fixture, recovery = _record_source_recovery_fixture()
    missing = _rewarrant(
        fixture[0],
        recovery,
        testimony=None,
        convention=APPLICATION_SOURCE_MEANING_CONVENTION,
    )
    assert (
        missing.payload["refusal_reason"] == "missing_meaning_testimony"
        and "remains Unknown" in missing.payload["unknowns"][0]
    )
    fixture, recovery = _record_source_recovery_fixture()
    testimony = SOURCE_MEANING_TESTIMONIES[recovery.payload["recovered_source_ref"]]
    assert (
        _rewarrant(fixture[0], recovery, testimony=testimony, convention=None).payload[
            "refusal_reason"
        ]
        == "missing_constitutive_convention"
    )


def test_direct_meaning_warrant_rejects_forgery_duplicates_and_upstream_uncertainty():
    fixture, recovery = _record_source_recovery_fixture()
    other = SOURCE_MEANING_TESTIMONIES["source:operator-common-grammar-local-stop:v1"]
    assert (
        _rewarrant(
            fixture[0],
            recovery,
            testimony=other,
            convention=APPLICATION_SOURCE_MEANING_CONVENTION,
        ).payload["refusal_reason"]
        == "source_identity_mismatch"
    )
    fixture, recovery = _record_source_recovery_fixture()
    forged = recovery.model_copy(deep=True)
    forged.payload["recovered_source_proposition"] = "forged"
    exact = SOURCE_MEANING_TESTIMONIES[recovery.payload["recovered_source_ref"]]
    assert (
        _rewarrant(
            fixture[0],
            forged,
            testimony=exact,
            convention=APPLICATION_SOURCE_MEANING_CONVENTION,
        ).payload["refusal_reason"]
        == "supplied_source_recovery_is_not_recorded_occurrence"
    )
    fixture, recovery = _record_source_recovery_fixture()
    fixture[0].extend([recovery.model_copy(update={"id": "event:duplicate"})])
    exact = SOURCE_MEANING_TESTIMONIES[recovery.payload["recovered_source_ref"]]
    assert (
        _rewarrant(
            fixture[0],
            recovery,
            testimony=exact,
            convention=APPLICATION_SOURCE_MEANING_CONVENTION,
        ).payload["refusal_reason"]
        == "multiple_source_recovery_occurrences"
    )
    for field, reason in (
        ("unknowns", "upstream_representation_unknown"),
        ("conflicts", "upstream_representation_conflicting"),
    ):
        fixture, recovery = _record_source_recovery_fixture()
        fixture[4].payload[field] = [field]
        exact = SOURCE_MEANING_TESTIMONIES[recovery.payload["recovered_source_ref"]]
        assert (
            _rewarrant(
                fixture[0],
                recovery,
                testimony=exact,
                convention=APPLICATION_SOURCE_MEANING_CONVENTION,
            ).payload["refusal_reason"]
            == reason
        )


@pytest.mark.parametrize(
    "mutation,reason",
    [
        (lambda f: None, "no_recorded_representation_occurrence"),
        (lambda f: f[4].payload.__setitem__("attempt_ref", "wrong"), "wrong_attempt"),
        (
            lambda f: f[4].payload.__setitem__("presentation_ref", "wrong"),
            "wrong_presentation",
        ),
        (
            lambda f: f[4].payload.__setitem__("choice_set_ref", "wrong"),
            "wrong_choice_set",
        ),
        (
            lambda f: f[4].payload.__setitem__("choice_set_fingerprint", "wrong"),
            "wrong_set_fingerprint",
        ),
        (
            lambda f: f[4]
            .payload["representations"][0]
            .__setitem__("proposition_assertion", "forged"),
            "forged_relation_payload",
        ),
    ],
)
def test_direct_source_recovery_checks_exact_representation(mutation, reason):
    fixture = _record_consumed_probe_fixture()
    mutation(fixture)
    occurrence = (
        None if reason == "no_recorded_representation_occurrence" else fixture[4]
    )
    recovered, refusal = _recover_represented_source(
        fixture[3],
        fixture[1],
        occurrence,
        ledger=fixture[0],
        workspace_id="w",
        attempt_ref="attempt:helper",
        presentation_occurrence=fixture[5],
        selection_occurrence=fixture[8],
    )
    assert recovered is None and refusal == reason


@pytest.mark.parametrize(
    "field,value,reason",
    [
        ("binding_id", "wrong", "binding_id_mismatch"),
        ("choice_set_ref", "wrong", "binding_choice_set_mismatch"),
        ("choice_set_fingerprint", "wrong", "binding_set_fingerprint_mismatch"),
        ("presented_options", [], "binding_presented_options_mismatch"),
        (
            "selected_presented_alternative_ref",
            "wrong",
            "binding_selected_alternative_mismatch",
        ),
        ("binding_testimony", {}, "recorded_binding_payload_mismatch"),
        ("lineage", [], "binding_lineage_mismatch"),
    ],
)
def test_direct_source_recovery_checks_exact_recorded_binding(field, value, reason):
    fixture = _record_consumed_probe_fixture()
    fixture[7].payload[field] = value
    recovered, refusal = _recover_represented_source(
        fixture[3],
        fixture[1],
        fixture[4],
        ledger=fixture[0],
        workspace_id="w",
        attempt_ref="attempt:helper",
        presentation_occurrence=fixture[5],
        selection_occurrence=fixture[8],
    )
    assert recovered is None and refusal == reason


@pytest.mark.parametrize(
    "binding_count,reason",
    [
        (0, "no_recorded_binding_occurrence"),
        (2, "multiple_recorded_binding_occurrences"),
    ],
)
def test_direct_source_recovery_requires_one_recorded_binding(binding_count, reason):
    fixture = _record_consumed_probe_fixture()
    source = fixture[0].list_events("w")
    ledger = EventLedger()
    ledger.extend(
        event
        for event in source
        if event.kind != "operator.ingress.common_grammar.binding_completed"
    )
    if binding_count == 2:
        ledger.extend(
            [fixture[7], fixture[7].model_copy(update={"id": "evt:duplicate"})]
        )

    recovered, refusal = _recover_represented_source(
        fixture[3],
        fixture[1],
        fixture[4],
        ledger=ledger,
        workspace_id="w",
        attempt_ref="attempt:helper",
        presentation_occurrence=fixture[5],
        selection_occurrence=fixture[8],
    )
    assert recovered is None and refusal == reason


def test_direct_source_recovery_checks_selected_occurrence_separately():
    fixture = _record_consumed_probe_fixture()
    mismatched_selection = fixture[8].model_copy(deep=True)
    mismatched_selection.payload["binding_id"] = "binding:wrong"

    recovered, refusal = _recover_represented_source(
        fixture[3],
        fixture[1],
        fixture[4],
        ledger=fixture[0],
        workspace_id="w",
        attempt_ref="attempt:helper",
        presentation_occurrence=fixture[5],
        selection_occurrence=mismatched_selection,
    )
    assert recovered is None
    assert refusal == "selected_alternative_occurrence_mismatch"


def test_direct_meaning_warrant_requires_exact_recorded_source_recovery():
    fixture, recovery = _record_source_recovery_fixture()
    ledger = EventLedger()
    ledger.extend(
        event for event in fixture[0].list_events("w") if event.id != recovery.id
    )
    testimony = SOURCE_MEANING_TESTIMONIES[recovery.payload["recovered_source_ref"]]

    result = _rewarrant(
        ledger,
        recovery,
        testimony=testimony,
        convention=SOURCE_MEANING_CONVENTIONS[testimony.source_ref],
    )

    assert result.kind.endswith("meaning_relation_refused")
    assert result.payload["refusal_reason"] == (
        "no_exact_recorded_source_recovery_occurrence"
    )
    result_text = str(result.model_dump()).lower()
    for unclaimed in (
        "meaning relation warranted",
        "proposition false",
        "applicability",
        "admission",
        "goal establishment",
    ):
        assert unclaimed not in result_text


def _record_meaning_warrant_fixture():
    """Disconnected warrant testimony, not the active production road."""
    fixture, recovery = _record_source_recovery_fixture()
    testimony = SOURCE_MEANING_TESTIMONIES[recovery.payload["recovered_source_ref"]]
    warrant = _rewarrant(
        fixture[0],
        recovery,
        testimony=testimony,
        convention=SOURCE_MEANING_CONVENTIONS[testimony.source_ref],
    )
    assert warrant.kind.endswith("meaning_relation_warranted")
    return fixture[0], warrant


def test_exact_recorded_meaning_warrant_allows_only_applicability_examination():
    ledger, warrant = _record_meaning_warrant_fixture()
    result = _examine_meaning_relation_for_bounded_operator_goal_establishment(
        ledger=ledger,
        workspace_id="w",
        session_id="s",
        attempt_ref="attempt:helper",
        meaning_relation=warrant,
    )
    assert result.kind.endswith("applicability_examined")
    assert result.payload["applicability"] == "unknown"
    assert result.payload["unknowns"] == ["consumer-local admission evidence is absent"]
    assert "inapplicable" not in str(result.model_dump()).lower()
    assert not any(
        marker in event.kind
        for event in ledger.list_events("w")
        for marker in ("admission", "goal_established")
    )


@pytest.mark.parametrize("supplied", ["unrecorded-copy", None])
def test_meaning_warrant_consumer_refuses_nonexact_or_missing_warrant(supplied):
    if supplied == "unrecorded-copy":
        ledger, warrant = _record_meaning_warrant_fixture()
        supplied_event = warrant.model_copy(update={"id": "evt:unrecorded-copy"})
    else:
        ledger, supplied_event = EventLedger(), None

    result = _examine_meaning_relation_for_bounded_operator_goal_establishment(
        ledger=ledger,
        workspace_id="w",
        session_id="s",
        attempt_ref="attempt:helper",
        meaning_relation=supplied_event,
    )
    assert result.kind.endswith("applicability_refused")
    assert result.payload["refusal_reason"] == (
        "supplied_meaning_relation_is_not_exact_recorded_warrant"
    )
    assert result.payload["applicability"] == "unknown"
    assert not any(
        marker in event.kind
        for event in ledger.list_events("w")
        for marker in ("admission", "goal_established")
    )


def test_direct_capture_validation_uses_preconsumption_fixture():
    fixture = _record_preconsumption_probe_fixture()
    ledger, choice, capture = fixture[:3]
    assert (
        validate_capture_for_probe(
            ledger=ledger,
            workspace_id="w",
            attempt_ref="attempt:helper",
            choice_set=choice,
            capture=capture,
        ).binding_state
        == "bound"
    )
    altered = PresentedClosedChoiceSet(
        choice.choice_set_ref,
        choice.prompt,
        (ClosedChoiceOption("1", "different", "Different"), *choice.options[1:]),
        choice.presentation_ref,
    )
    for candidate_choice, candidate_capture, message in (
        (
            common_grammar_choice_set("presentation:wrong"),
            capture,
            "presentation/set identity or fingerprint mismatch",
        ),
        (
            replace(choice, choice_set_ref="choice-set:wrong"),
            capture,
            "presentation/set identity or fingerprint mismatch",
        ),
        (
            choice,
            replace(capture, choice_set_ref="wrong"),
            "presentation/set identity or fingerprint mismatch",
        ),
        (altered, capture, "presentation/set identity or fingerprint mismatch"),
        (
            choice,
            replace(capture, capture_ref="other"),
            "capture is not the current recorded occurrence",
        ),
        (
            choice,
            replace(capture, captured_token="2"),
            "capture is not the current recorded occurrence",
        ),
    ):
        with pytest.raises(ClosedChoiceSelectionBindingError, match=message):
            validate_capture_for_probe(
                ledger=ledger,
                workspace_id="w",
                attempt_ref="attempt:helper",
                choice_set=candidate_choice,
                capture=candidate_capture,
            )


def test_consumed_capture_refusal_and_durable_replay(tmp_path):
    fixture = _record_consumed_probe_fixture()
    ledger, choice, capture = fixture[:3]
    with pytest.raises(ClosedChoiceSelectionBindingError, match="already consumed"):
        validate_capture_for_probe(
            ledger=ledger,
            workspace_id="w",
            attempt_ref="attempt:helper",
            choice_set=choice,
            capture=capture,
        )
    path = tmp_path / "helper-replay.db"
    durable = SQLiteEventLedger(str(path))
    durable_fixture = _record_consumed_probe_fixture(ledger=durable)
    durable.close()
    reopened = SQLiteEventLedger(str(path))
    with pytest.raises(ClosedChoiceSelectionBindingError, match="already consumed"):
        validate_capture_for_probe(
            ledger=reopened,
            workspace_id="w",
            attempt_ref="attempt:helper",
            choice_set=durable_fixture[1],
            capture=durable_fixture[2],
        )
    reopened.close()


def test_direct_closed_choice_binding_is_not_positive_boge_admission():
    choice = PresentedClosedChoiceSet(
        "choice:bare",
        "Choose",
        (ClosedChoiceOption("1", "alternative:bare", "Bare"),),
        "presentation:bare",
    )
    capture = OperatorSelectionTokenCapture("capture:bare", "choice:bare", "1")
    binding = bind_closed_choice_selection(choice, capture)
    with pytest.raises(
        BoundedOperatorGoalEstablishmentError,
        match="closed-choice bounded-goal establishment is unavailable",
    ):
        establish_bounded_operator_goal_from_closed_choice(binding)
