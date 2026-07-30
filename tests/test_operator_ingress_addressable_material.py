from io import BytesIO, StringIO

import pytest

from seed_runtime.events import EventLedger, SQLiteEventLedger
from seed_runtime.operator_ingress_addressable_material import (
    AUTHORITY_LIMITS,
    UNKNOWNS,
    OperatorIngressAddressableMaterial,
    OperatorIngressAddressableMaterialError,
    form_operator_ingress_addressable_material,
)
from seed_runtime.operator_ingress_common_grammar_prerequisite import (
    run_operator_ingress_common_grammar_probe_attempt,
)
from seed_runtime.operator_ingress_representation import capture_stdin_material
from seed_runtime.state import StateProjector


class _UnreadableResponse:
    def readline(self):
        pytest.fail("addressable-material formation must not read a second input")


def _run(material: bytes, *, ledger=None):
    ledger = ledger or EventLedger()
    output = StringIO()
    view = run_operator_ingress_common_grammar_probe_attempt(
        ledger=ledger,
        workspace_id="w",
        session_id="s",
        captured_ingress=capture_stdin_material(BytesIO(material)),
        response_input_stream=_UnreadableResponse(),
        output_stream=output,
    )
    projected = view.get("addressable_operator_material")
    artifact = (
        OperatorIngressAddressableMaterial.from_json_dict(projected)
        if projected is not None
        else None
    )
    return ledger, view, artifact, output.getvalue()


@pytest.mark.parametrize(
    ("material", "text", "ingress_kind", "content"),
    [
        (b" exact \r\n", " exact \r\n", "text", " exact "),
        (b"\n", "\n", "empty", ""),
        (b"\r\n", "\r\n", "empty", ""),
    ],
)
def test_decoded_ingress_forms_exact_bounded_addressable_material(
    material, text, ingress_kind, content
):
    ledger, view, artifact, output = _run(material)
    raw, examination, ingress = ledger.list_events("w")
    assert artifact is not None
    assert artifact.ingress_event_ref == ingress.id
    assert artifact.raw_material_event_ref == raw.id
    assert artifact.representation_examination_event_ref == examination.id
    assert ingress.payload["raw_input"] == text
    assert ingress.payload["decoded_text"] == text
    assert ingress.payload["dimensions"]["content"] == content
    assert ingress.payload["ingress_kind"] == ingress_kind
    assert ingress.payload["decoded_text"] != ingress.payload["dimensions"]["content"]
    assert artifact.exact_operator_material.material_ref == ingress.id
    assert artifact.exact_operator_material.exact_text == text
    assert artifact.exact_operator_material.provenance == (
        raw.id,
        examination.id,
        ingress.id,
    )
    span = artifact.exact_operator_material.source_spans[0]
    assert (span.source_ref, span.start, span.end, span.exact_text) == (
        ingress.id,
        0,
        len(text),
        text,
    )
    assert artifact.provenance == (raw.id, examination.id, ingress.id)
    assert artifact.source_role == (
        "operator-origin material at the preserved ingress boundary"
    )
    assert artifact.unknowns == UNKNOWNS
    assert artifact.authority_limits == AUTHORITY_LIMITS
    assert artifact.read_only is True
    assert artifact.writes_event_ledger is False
    assert artifact.mutates_state is False
    assert artifact.mutates_cluster is False
    assert view["addressable_operator_material"] == artifact.to_json_dict()
    assert output == ""
    assert [event.kind for event in ledger.list_events("w")] == [
        "operator.ingress.common_grammar.raw_material_captured",
        "operator.ingress.common_grammar.representation_examined",
        "operator.ingress.common_grammar.ingress_occurred",
    ]


def test_active_formation_does_not_call_interpretation_producer(monkeypatch):
    import seed_runtime.contextual_interpretation_warrant_set as interpretation

    monkeypatch.setattr(
        interpretation,
        "produce_contextual_interpretation_warrant_set",
        lambda **kwargs: pytest.fail(
            "interpretation production must remain disconnected"
        ),
    )
    _, _, artifact, _ = _run(b"material\n")
    assert artifact is not None


@pytest.mark.parametrize("material", [b"", b"\xff\n"])
def test_eof_and_representation_insufficiency_form_no_addressable_material(material):
    ledger = EventLedger()
    output = StringIO()
    view = run_operator_ingress_common_grammar_probe_attempt(
        ledger=ledger,
        workspace_id="w",
        session_id="s",
        captured_ingress=capture_stdin_material(BytesIO(material)),
        response_input_stream=_UnreadableResponse(),
        output_stream=output,
    )
    assert "addressable_operator_material" not in view


def test_producer_refuses_forged_foreign_incomplete_and_invalid_occurrences():
    ledger, _, _, _ = _run(b"material\n")
    ingress = ledger.list_events("w")[-1]

    def changed(**payload_changes):
        payload = {**ingress.payload, **payload_changes}
        return ingress.model_copy(update={"payload": payload})

    refused = (
        ingress.model_copy(update={"id": "evt:forged"}),
        ingress.model_copy(update={"workspace_id": "foreign"}),
        changed(raw_material_event_id=None),
        changed(lineage=[]),
        changed(ingress_kind="eof"),
        changed(decoded_text=None),
        changed(
            dimensions={
                **ingress.payload["dimensions"],
                "authority_warrant": "meaning known",
            }
        ),
    )
    for occurrence in refused:
        with pytest.raises(OperatorIngressAddressableMaterialError):
            form_operator_ingress_addressable_material(
                ingress_occurrence=occurrence, ledger=ledger
            )

    raw, examination, _ = ledger.list_events("w")
    response_raw = raw.model_copy(
        update={
            "id": "evt:response",
            "payload": {**raw.payload, "material_role": "response"},
        }
    )
    response_ledger = EventLedger()
    response_ledger.extend((response_raw, examination, ingress))
    with pytest.raises(OperatorIngressAddressableMaterialError):
        form_operator_ingress_addressable_material(
            ingress_occurrence=ingress, ledger=response_ledger
        )

    failed = examination.model_copy(
        update={
            "payload": {
                **examination.payload,
                "decoder_succeeded": False,
                "decoder_outcome": "bytes_rejected",
            }
        }
    )
    failed_ledger = EventLedger()
    failed_ledger.extend((raw, failed, ingress))
    with pytest.raises(OperatorIngressAddressableMaterialError):
        form_operator_ingress_addressable_material(
            ingress_occurrence=ingress, ledger=failed_ledger
        )


def test_sqlite_replay_reconstructs_identical_material(tmp_path):
    path = tmp_path / "events.db"
    ledger = SQLiteEventLedger(str(path))
    _, view, artifact, _ = _run("é\n".encode(), ledger=ledger)
    ledger.close()
    replay_ledger = SQLiteEventLedger(str(path))
    replay = StateProjector(replay_ledger).project("w")
    replay_view = replay.operator_ingress_common_grammar_attempts[
        next(iter(replay.operator_ingress_common_grammar_attempts))
    ]
    assert replay_view == view
    assert (
        OperatorIngressAddressableMaterial.from_json_dict(
            replay_view["addressable_operator_material"]
        )
        == artifact
    )
    replayed_artifact = OperatorIngressAddressableMaterial.from_json_dict(
        replay_view["addressable_operator_material"]
    )
    assert artifact.exact_operator_material.exact_text == "é\n"
    assert replayed_artifact.exact_operator_material.exact_text == "é\n"
    replay_ledger.close()


def test_historical_incomplete_ingress_replays_without_inventing_material():
    ledger = EventLedger()
    historical = ledger.append(
        "operator.ingress.common_grammar.ingress_occurred",
        "w",
        {
            "attempt_ref": "attempt:historical",
            "dimensions": {
                "identity": "attempt:historical",
                "content": "historical",
                "standing": "occurred",
            },
            "ingress_kind": "text",
            "mutates_cluster": False,
        },
        session_id="s",
    )
    view = (
        StateProjector(ledger)
        .project("w")
        .operator_ingress_common_grammar_attempts["attempt:historical"]
    )
    assert (
        view["current_standing"]["preserved_ingress"]["evidence_event_id"]
        == historical.id
    )
    assert "addressable_operator_material" not in view
