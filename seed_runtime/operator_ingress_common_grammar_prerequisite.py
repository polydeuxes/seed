"""One-attempt bounded operator-ingress representation handling and historical projection."""

from __future__ import annotations

from typing import BinaryIO, TextIO

from seed_runtime.events import EventLedger
from seed_runtime.ids import new_id
from seed_runtime.operator_ingress_representation import (
    CapturedOperatorMaterial,
    capture_stdin_material,
    examine_text_representation,
)
from seed_runtime.state import StateProjector


def _dimensions(
    *, identity, content, standing, source, responsibility, authority, scope, occurrence
):
    return {
        "identity": identity,
        "content": content,
        "standing": standing,
        "source_provenance": source,
        "responsibility": responsibility,
        "authority_warrant": authority,
        "scope_locality": scope,
        "occurrence_preservation": occurrence,
    }


def _record(ledger, kind, workspace, session, attempt, dimensions, **extra):
    return ledger.append(
        kind,
        workspace,
        {
            "attempt_ref": attempt,
            "dimensions": dimensions,
            "mutates_cluster": False,
            **extra,
        },
        session_id=session,
    )


def project_operator_ingress_common_grammar_events(
    state, event, *, ledger=None
) -> None:
    """Dispatch one operator-ingress common-grammar event into the dedicated current view."""
    if not event.kind.startswith("operator.ingress.common_grammar."):
        return
    attempt = event.payload["attempt_ref"]
    view = state.operator_ingress_common_grammar_attempts.setdefault(
        attempt,
        {
            "event_ids": [],
            "dimensional_standing": {},
            "current_standing": {
                subject: None
                for subject in (
                    "raw_initial_material",
                    "raw_response_material",
                    "preserved_ingress",
                    "produced_probe",
                    "alternative_representations",
                    "presentation",
                    "response",
                    "binding_finding",
                    "alternative_selection",
                    "source_recovery",
                    "source_role_testimony",
                    "potential_goal_standing",
                    "presentation_eligibility",
                    "meaning_relation",
                    "bounded_operator_goal_establishment_applicability",
                    "interaction_closure",
                )
            },
            "known_loss": [],
            "unknowns": [],
            "conflicts": [],
            "representation_examinations": {},
        },
    )
    view["event_ids"].append(event.id)
    # Occurrences are evidence in their own right.  Keep each complete
    # eight-dimensional description rather than replacing it with the tail event.
    view["dimensional_standing"][event.id] = {
        "event_kind": event.kind,
        "subject_ref": event.payload["dimensions"]["identity"],
        "dimensions": event.payload["dimensions"],
        "lineage": list(event.payload.get("lineage", ())),
    }
    if event.kind == "operator.ingress.common_grammar.representation_examined":
        view["representation_examinations"][event.payload["material_role"]] = {
            "examination_event_id": event.id,
            "capture_event_id": event.payload["capture_event_id"],
            "encoding_testimony": event.payload["encoding_testimony"],
            "decoder_mechanism": event.payload["decoder_mechanism"],
            "decoder_mechanism_selection": event.payload["decoder_mechanism_selection"],
            "decoder_outcome": event.payload["decoder_outcome"],
            "decoder_succeeded": event.payload["decoder_succeeded"],
            "decoder_failure": event.payload["decoder_failure"],
        }
        view["last_event_kind"] = event.kind
        return
    subject_by_kind = {
        "operator.ingress.common_grammar.ingress_occurred": "preserved_ingress",
        "operator.ingress.common_grammar.initial_eof_occurred": "preserved_ingress",
        "operator.ingress.common_grammar.probe_produced": "produced_probe",
        "operator.ingress.common_grammar.alternatives_represented": "alternative_representations",
        "operator.ingress.common_grammar.presentation_occurred": "presentation",
        "operator.ingress.common_grammar.response_captured": "response",
        "operator.ingress.common_grammar.response_eof_occurred": "response",
        "operator.ingress.common_grammar.binding_completed": "binding_finding",
        "operator.ingress.common_grammar.unsupported_finding": "binding_finding",
        "operator.ingress.common_grammar.alternative_selected": "alternative_selection",
        "operator.ingress.common_grammar.source_recovered": "source_recovery",
        "operator.ingress.common_grammar.source_recovery_refused": "source_recovery",
        "operator.ingress.common_grammar.potential_goal_standing_examined": "potential_goal_standing",
        "operator.ingress.common_grammar.presentation_eligibility_examined": "presentation_eligibility",
        "operator.ingress.common_grammar.meaning_relation_warranted": "meaning_relation",
        "operator.ingress.common_grammar.meaning_relation_refused": "meaning_relation",
        "operator.ingress.common_grammar.bounded_operator_goal_establishment_applicability_examined": "bounded_operator_goal_establishment_applicability",
        "operator.ingress.common_grammar.bounded_operator_goal_establishment_applicability_refused": "bounded_operator_goal_establishment_applicability",
        "operator.ingress.common_grammar.stopping_occurred": "interaction_closure",
    }
    subject = (
        "raw_initial_material"
        if event.kind == "operator.ingress.common_grammar.raw_material_captured"
        and event.payload["material_role"] == "initial_ingress"
        else (
            "raw_response_material"
            if event.kind == "operator.ingress.common_grammar.raw_material_captured"
            else subject_by_kind[event.kind]
        )
    )
    dimensions = dict(event.payload["dimensions"])
    if subject == "preserved_ingress":
        dimensions["standing"] = "preserved"
    view["current_standing"][subject] = {
        "subject_ref": dimensions["identity"],
        "dimensions": dimensions,
        "evidence_event_id": event.id,
    }
    if event.kind == "operator.ingress.common_grammar.ingress_occurred" and all(
        key in event.payload
        for key in (
            "decoded_text",
            "raw_material_event_id",
            "representation_examination_event_id",
        )
    ):
        from seed_runtime.operator_ingress_addressable_material import (
            form_operator_ingress_addressable_material,
        )

        if ledger is not None:
            view["addressable_operator_material"] = (
                form_operator_ingress_addressable_material(
                    ingress_occurrence=event, ledger=ledger
                ).to_json_dict()
            )
    if subject == "response" and view["current_standing"]["presentation"]:
        view["current_standing"]["presentation"]["dimensions"]["standing"] = "consumed"
    if subject == "binding_finding" and view["current_standing"]["response"]:
        view["current_standing"]["response"]["dimensions"]["standing"] = "consumed"
    view["last_event_kind"] = event.kind
    for key in ("known_loss", "unknowns", "conflicts"):
        view[key] = sorted(set((*view[key], *event.payload.get(key, ()))))
    for key in (
        "choice_set_ref",
        "presentation_ref",
        "capture_ref",
        "binding_id",
        "selected_presented_alternative_ref",
        "recovered_source_ref",
        "recovered_source_role",
        "recovered_source_proposition",
        "source_role_testimony_ref",
        "standing_subject",
        "standing_relation",
        "standing_result",
        "upstream_standing_occurrence_id",
        "presentation_purpose_id",
        "eligibility_relation",
        "eligibility_result",
        "relation_ref",
        "relation_assertion",
        "meaning_testimony_ref",
        "constitutive_convention_ref",
        "meaning_relation_warrant_occurrence_id",
        "consumer_ref",
        "purpose_ref",
        "condition_examined",
        "condition_evidence",
        "applicability",
        "applicability_reason",
        "closed",
        "response_kind",
    ):
        if key in event.payload:
            view[key] = event.payload[key]
    if event.kind == "operator.ingress.common_grammar.potential_goal_standing_examined":
        view["current_standing"]["source_role_testimony"] = {
            "subject_ref": event.payload.get("source_role_testimony_ref"),
            "testimony": event.payload.get("source_role_testimony"),
            "evidence_event_id": event.id,
        }


def _capture_representation(
    *,
    ledger,
    workspace,
    session,
    attempt,
    material_role,
    captured_material=None,
    input_stream=None,
    lineage=(),
):
    if (captured_material is None) == (input_stream is None):
        raise ValueError("supply exactly one of captured_material or input_stream")
    capture = (
        captured_material
        if captured_material is not None
        else capture_stdin_material(input_stream)
    )
    capture_ref = new_id("operator_material")
    captured = _record(
        ledger,
        "operator.ingress.common_grammar.raw_material_captured",
        workspace,
        session,
        attempt,
        _dimensions(
            identity=capture_ref,
            content=capture.exact_bytes.hex(),
            standing="captured",
            source=capture.capture_boundary,
            responsibility="competent-raw-material-capture",
            authority="occurrence evidence only",
            scope=f"workspace:{workspace};session:{session};role:{material_role}",
            occurrence="exact boundary bytes durably preserved as hexadecimal",
        ),
        material_role=material_role,
        exact_bytes_hex=capture.exact_bytes.hex(),
        byte_count=len(capture.exact_bytes),
        eof=capture.eof,
        delimiter_hex=capture.delimiter_hex,
        encoding_testimony=capture.encoding_testimony,
        capture_boundary=capture.capture_boundary,
        byte_material_origin=capture.byte_material_origin,
        known_loss=list(capture.known_loss),
        lineage=list(lineage),
    )
    examination = examine_text_representation(capture)
    if examination is None:
        return capture, None, captured, None
    examination_event = _record(
        ledger,
        "operator.ingress.common_grammar.representation_examined",
        workspace,
        session,
        attempt,
        _dimensions(
            identity=f"representation-examination:{captured.id}",
            content="strict decoder examination",
            # Preserve the particular decoder occurrence here as well as in the
            # examination payload.  A shared ``not-decodable`` standing would
            # collapse an unavailable mechanism and bytes rejected by an
            # available mechanism back into the Boolean boundary this record is
            # intended to repair.
            standing=examination.outcome,
            source=captured.id,
            responsibility="bounded-representation-evidence-production",
            authority="decoder outcome evidence only",
            scope=f"captured-occurrence:{capture_ref}",
            occurrence="decoder examination durably recorded",
        ),
        material_role=material_role,
        capture_event_id=captured.id,
        encoding_testimony=capture.encoding_testimony,
        decoder_mechanism=examination.mechanism,
        decoder_mechanism_selection=examination.mechanism_selection,
        decoder_outcome=examination.outcome,
        decoder_succeeded=examination.succeeded,
        decoder_failure=examination.failure,
        known_loss=list(capture.known_loss),
        unknowns=["true source-relative encoding Unknown"],
        lineage=[captured.id],
    )
    return capture, examination, captured, examination_event


def run_operator_ingress_common_grammar_probe_attempt(
    *,
    ledger: EventLedger,
    workspace_id: str,
    session_id: str,
    captured_ingress: CapturedOperatorMaterial,
    response_input_stream: TextIO | BinaryIO,
    output_stream: TextIO,
) -> dict[str, object]:
    """Run exactly one ingress/common-grammar-probe/response attempt and return."""
    attempt = new_id("operator_ingress_common_grammar_attempt")
    (
        captured_ingress,
        ingress_examination,
        ingress_capture,
        ingress_examination_event,
    ) = _capture_representation(
        ledger=ledger,
        workspace=workspace_id,
        session=session_id,
        attempt=attempt,
        captured_material=captured_ingress,
        material_role="initial_ingress",
    )
    raw_ingress = (
        ingress_examination.represented_text or "" if ingress_examination else ""
    )
    ingress_kind = (
        "eof"
        if captured_ingress.eof
        else "empty" if raw_ingress in {"\n", "\r\n"} else "text"
    )
    ingress_content = (
        None
        if ingress_kind == "eof"
        else raw_ingress.removesuffix("\n").removesuffix("\r")
    )
    if ingress_examination is not None and not ingress_examination.succeeded:
        _record(
            ledger,
            "operator.ingress.common_grammar.stopping_occurred",
            workspace_id,
            session_id,
            attempt,
            _dimensions(
                identity=f"stop:{ingress_examination_event.id}",
                content="representation insufficiency",
                standing="closed",
                source=ingress_examination_event.id,
                responsibility="competent-local-stopping",
                authority="closes only this interaction",
                scope=f"attempt:{attempt}",
                occurrence="separate stopping act recorded",
            ),
            closed=True,
            response_kind="representation_insufficient",
            lineage=[ingress_examination_event.id],
        )
        state = StateProjector(ledger).project(workspace_id)
        output_stream.write(
            "Representation insufficient: captured material did not decode under the selected decoder mechanism.\n"
        )
        output_stream.flush()
        return state.operator_ingress_common_grammar_attempts[attempt]
    ingress = _record(
        ledger,
        (
            "operator.ingress.common_grammar.initial_eof_occurred"
            if ingress_kind == "eof"
            else "operator.ingress.common_grammar.ingress_occurred"
        ),
        workspace_id,
        session_id,
        attempt,
        _dimensions(
            identity=attempt,
            content=ingress_content,
            standing="occurred",
            source=(
                ingress_capture.id
                if ingress_examination_event is None
                else ingress_examination_event.id
            ),
            responsibility="operator-ingress",
            authority="occurrence-only; meaning Unknown",
            scope=f"workspace:{workspace_id};session:{session_id}",
            occurrence=(
                "EOF occurrence preserves raw-capture lineage"
                if ingress_kind == "eof"
                else "strictly decoded text preserves capture/examination lineage"
            ),
        ),
        raw_input=raw_ingress,
        ingress_kind=ingress_kind,
        decoded_text=(
            ingress_examination.represented_text
            if ingress_examination is not None
            else None
        ),
        raw_material_event_id=ingress_capture.id,
        **(
            {"representation_examination_event_id": ingress_examination_event.id}
            if ingress_examination_event is not None
            else {}
        ),
        known_loss=list(captured_ingress.known_loss),
        lineage=[
            ingress_capture.id,
            *([ingress_examination_event.id] if ingress_examination_event else []),
        ],
    )
    state = StateProjector(ledger).project(workspace_id)
    if ingress_kind == "eof":
        _record(
            ledger,
            "operator.ingress.common_grammar.stopping_occurred",
            workspace_id,
            session_id,
            attempt,
            _dimensions(
                identity=f"stop:{ingress.id}",
                content="initial EOF",
                standing="closed",
                source=ingress.id,
                responsibility="competent-local-stopping",
                authority="closes only this interaction",
                scope=f"attempt:{attempt}",
                occurrence="separate stopping act recorded",
            ),
            closed=True,
            response_kind="initial_eof",
            lineage=[ingress.id],
        )
        state = StateProjector(ledger).project(workspace_id)
        output_stream.write(
            "Operator-ingress common-grammar interaction stopped locally.\n"
        )
        output_stream.flush()
        return state.operator_ingress_common_grammar_attempts[attempt]

    return state.operator_ingress_common_grammar_attempts[attempt]
