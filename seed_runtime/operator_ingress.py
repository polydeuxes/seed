"""One-attempt bounded operator-ingress representation handling and projection."""

from __future__ import annotations

from typing import TextIO

from seed_runtime.events import EventLedger
from seed_runtime.ids import new_id
from seed_runtime.operator_ingress_representation import (
    CapturedOperatorMaterial,
    examine_text_representation,
)


# Who supplied the material an occurrence preserves. Not the production occurrence of the
# recording occurrence, which is this Seed in both directions, and not authorship
# — an operator who supplies a book did not write it. `#2490` records why this
# has to exist before Seed preserves what it emitted: without it a later
# measurement over "preserved material" cannot decline to have as input Seed's own
# output, and Seed's account of a fire becomes material saying a fire occurred.
OPERATOR_ORIGIN = "operator"
SEED_ORIGIN = "this Seed"


def _dimensions(
    *, identity, content, standing, source, responsibility, authority, scope, occurrence
):
    return {
        "identity": identity,
        "content": content,
        "standing": standing,
        "source_provenance": source,
        "responsibility": responsibility,
        "authority": authority,
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


def project_operator_ingress_events(attempts, event, *, ledger=None) -> None:
    """Dispatch one operator-ingress event into the dedicated current view.

    ``attempts`` is the per-attempt projection mapping and is the whole of what
    this read has as input. It reads no entity, normalized Assertion, alias, relationship, or
    result condition, so nothing here requires a whole-workspace projection to exist.
    """
    if not event.kind.startswith("operator.ingress."):
        return
    subject_by_kind = {
        "operator.ingress.raw_material_captured": "raw_initial_material",
        "operator.ingress.ingress_occurred": "preserved_ingress",
        "operator.ingress.stopping_occurred": "interaction_closure",
    }
    supported_kinds = {
        *subject_by_kind,
        "operator.ingress.representation_examined",
    }
    if event.kind not in supported_kinds:
        raise ValueError(f"unsupported operator-ingress event: {event.kind}")
    attempt = event.payload["attempt_ref"]
    view = attempts.setdefault(
        attempt,
        {
            "event_ids": [],
            "dimensional_standing": {},
            "current_standing": {
                subject: None
                for subject in (
                    "raw_initial_material",
                    "preserved_ingress",
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
        "provenance_occurrence_refs": list(
            event.payload.get("provenance_occurrence_refs", ())
        ),
    }
    if event.kind == "operator.ingress.representation_examined":
        view["representation_examinations"][event.payload["material_role"]] = {
            "examination_event_id": event.id,
            "capture_event_id": event.payload["capture_event_id"],
            "stream_encoding_metadata": event.payload["stream_encoding_metadata"],
            "decoder_mechanism": event.payload["decoder_mechanism"],
            "decoder_mechanism_selection": event.payload["decoder_mechanism_selection"],
            "decoder_outcome": event.payload["decoder_outcome"],
            "decoder_succeeded": event.payload["decoder_succeeded"],
            "decoder_failure": event.payload["decoder_failure"],
        }
        view["last_event_kind"] = event.kind
        return
    subject = subject_by_kind[event.kind]
    dimensions = dict(event.payload["dimensions"])
    if subject == "preserved_ingress":
        dimensions["standing"] = "preserved"
    view["current_standing"][subject] = {
        "subject_ref": dimensions["identity"],
        "dimensions": dimensions,
        "evidence_event_id": event.id,
    }
    if event.kind == "operator.ingress.ingress_occurred" and all(
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
    view["last_event_kind"] = event.kind
    for key in ("known_loss", "unknowns", "conflicts"):
        view[key] = sorted(set((*view[key], *event.payload.get(key, ()))))
    for key in ("closed", "response_kind"):
        if key in event.payload:
            view[key] = event.payload[key]


def _capture_representation(
    *,
    ledger,
    workspace,
    session,
    attempt,
    material_role,
    captured_material: CapturedOperatorMaterial,
    provenance_occurrence_refs=(),
):
    capture = captured_material
    capture_ref = new_id("operator_material")
    captured = _record(
        ledger,
        "operator.ingress.raw_material_captured",
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
        stream_encoding_metadata=capture.stream_encoding_metadata,
        capture_boundary=capture.capture_boundary,
        byte_material_origin=capture.byte_material_origin,
        known_loss=list(capture.known_loss),
        provenance_occurrence_refs=list(provenance_occurrence_refs),
    )
    examination = examine_text_representation(capture)
    examination_event = _record(
        ledger,
        "operator.ingress.representation_examined",
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
        stream_encoding_metadata=capture.stream_encoding_metadata,
        decoder_mechanism=examination.mechanism,
        decoder_mechanism_selection=examination.mechanism_selection,
        decoder_outcome=examination.outcome,
        decoder_succeeded=examination.succeeded,
        decoder_failure=examination.failure,
        known_loss=list(capture.known_loss),
        unknowns=["true source-relative encoding Unknown"],
        provenance_occurrence_refs=[captured.id],
    )
    return capture, examination, captured, examination_event


def _project_attempt(*, events, ledger, attempt):
    """Project one attempt from exactly the occurrences it recorded.

    The whole-workspace replay this replaces rebuilt every entity, normalized Assertion,
    alias, relationship, and index in order to return one bounded attempt, and
    it did so once per attempt, so occurrence *j* was replayed by every later
    attempt. The work here is constant in the number of earlier attempts.

    Refusals the returned projection depends on are unchanged: the addressable
    material is still formed through `form_operator_ingress_addressable_material`,
    which consults the ledger for this attempt's exact provenance occurrences and refuses a
    foreign, incomplete, or unrecorded occurrence. What is no longer performed is
    the replay of unrelated historical events, which no clause makes this
    responsibility's to perform.
    """

    attempts: dict[str, dict] = {}
    for event in events:
        project_operator_ingress_events(attempts, event, ledger=ledger)
    return attempts[attempt]


def run_operator_ingress_attempt(
    *,
    ledger: EventLedger,
    workspace_id: str,
    session_id: str,
    captured_ingress: CapturedOperatorMaterial,
    output_stream: TextIO,
    session_standing: dict[str, object] | None = None,
) -> dict[str, object]:
    """Capture, examine, and project one bounded non-EOF ingress attempt.

    ``session_standing`` is already-projected Standing from this session's
    earlier recorded events.  It is carried on the returned projection for
    the Presentation to expose; it is not recorded, interpreted, or used to
    alter this attempt's own occurrence handling.

    The occurrence names no Presentation.  A relation between this preserved
    material and any preserved Presentation is its own bounded Assertion with
    its own participants, production occurrence, occurrence, and Evidence; it does not live
    inside one participant's record, and no such relation is established
    here.
    """
    if captured_ingress.eof:
        raise ValueError("captured_ingress must be non-EOF")

    attempt = new_id("operator_ingress_attempt")
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
    if not ingress_examination.succeeded:
        # The material occurred. Its text representation did not.
        #
        # Until now no ingress occurrence was recorded at all when the decoder
        # refused the bytes, so material Seed had captured exactly, and could
        # recover exactly, was absent from its own history because one later
        # examination of it failed. Capture and examination were already
        # recorded either way; only the occurrence was gated.
        #
        # The interaction still closes here. That is a separate consequence and
        # is unchanged: what the console can render is not what Seed preserves.
        unrepresented_event = _record(
            ledger,
            "operator.ingress.ingress_occurred",
            workspace_id,
            session_id,
            attempt,
            _dimensions(
                identity=attempt,
                content=f"exact material, {len(captured_ingress.exact_bytes)} bytes",
                standing="occurred",
                source=ingress_examination_event.id,
                responsibility="operator-ingress",
                authority="occurrence-only; represented relation Unknown",
                scope=f"workspace:{workspace_id};session:{session_id}",
                occurrence="exact material preserved; no text representation available",
            ),
            material_origin=OPERATOR_ORIGIN,
            text_representation={
                "available": False,
                "decoder_outcome": ingress_examination.outcome,
                "decoder_mechanism": ingress_examination.mechanism,
            },
            ingress_kind="unrepresented",
            byte_count=len(captured_ingress.exact_bytes),
            raw_material_event_id=ingress_capture.id,
            representation_examination_event_id=ingress_examination_event.id,
            known_loss=list(captured_ingress.known_loss),
            unknowns=[
                "what these bytes represent remains Unknown",
                "whether any decoder represents them remains Unknown",
            ],
            provenance_occurrence_refs=[
                ingress_capture.id,
                ingress_examination_event.id,
            ],
        )
        stop_event = _record(
            ledger,
            "operator.ingress.stopping_occurred",
            workspace_id,
            session_id,
            attempt,
            _dimensions(
                identity=f"stop:{ingress_examination_event.id}",
                content=ingress_examination.outcome,
                standing="closed",
                source=ingress_examination_event.id,
                responsibility="competent-local-stopping",
                authority="closes only this interaction",
                scope=f"attempt:{attempt}",
                occurrence="separate stopping act recorded",
            ),
            closed=True,
            response_kind=ingress_examination.outcome,
            provenance_occurrence_refs=[ingress_examination_event.id],
        )
        projection = _project_attempt(
            events=(
                ingress_capture,
                ingress_examination_event,
                unrepresented_event,
                stop_event,
            ),
            ledger=ledger,
            attempt=attempt,
        )
        output_stream.write(
            f"Decoder outcome {ingress_examination.outcome}: captured material did not "
            f"decode under {ingress_examination.mechanism}.\n"
        )
        output_stream.flush()
        if session_standing is not None:
            projection["session_standing"] = session_standing
        return projection
    raw_ingress = ingress_examination.represented_text
    ingress_kind = "empty" if raw_ingress in {"\n", "\r\n"} else "text"
    ingress_content = raw_ingress.removesuffix("\n").removesuffix("\r")
    ingress_event = _record(
        ledger,
        "operator.ingress.ingress_occurred",
        workspace_id,
        session_id,
        attempt,
        _dimensions(
            identity=attempt,
            content=ingress_content,
            standing="occurred",
            source=ingress_examination_event.id,
            responsibility="operator-ingress",
            authority="occurrence-only; represented relation Unknown",
            scope=f"workspace:{workspace_id};session:{session_id}",
            occurrence=(
                "strictly decoded text preserves capture/examination provenance"
            ),
        ),
        material_origin=OPERATOR_ORIGIN,
        text_representation={
            "available": True,
            "decoder_outcome": ingress_examination.outcome,
            "decoder_mechanism": ingress_examination.mechanism,
        },
        raw_input=raw_ingress,
        ingress_kind=ingress_kind,
        decoded_text=ingress_examination.represented_text,
        raw_material_event_id=ingress_capture.id,
        representation_examination_event_id=ingress_examination_event.id,
        known_loss=list(captured_ingress.known_loss),
        provenance_occurrence_refs=[
            ingress_capture.id,
            ingress_examination_event.id,
        ],
    )
    projection = _project_attempt(
        events=(ingress_capture, ingress_examination_event, ingress_event),
        ledger=ledger,
        attempt=attempt,
    )
    if session_standing is not None:
        projection["session_standing"] = session_standing
    return projection
