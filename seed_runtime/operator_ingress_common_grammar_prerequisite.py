"""One-attempt bounded operator-ingress common-grammar interaction for unknown operator common grammar."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from typing import BinaryIO, TextIO

from seed_runtime.closed_choice_selection_binding import (
    ClosedChoiceOption,
    ClosedChoiceSelectionBindingError,
    OperatorSelectionTokenCapture,
    PresentedClosedChoiceSet,
    bind_closed_choice_selection,
)
from seed_runtime.events import EventLedger
from seed_runtime.ids import new_id
from seed_runtime.operator_ingress_representation import (
    CapturedOperatorMaterial,
    capture_stdin_material,
    examine_text_representation,
)
from seed_runtime.state import StateProjector

CHOICE_SET_REF = "operator-ingress-common-grammar:v1:two-alternative"
PROMPT = "Select one alternative by its exact token:"
OPTIONS = (
    ClosedChoiceOption(
        "1",
        "common-grammar-acquisition",
        "Select bounded common-grammar acquisition alternative.",
    ),
    ClosedChoiceOption("2", "local-stop", "Select local stopping alternative."),
)

SOURCE_PROPOSITIONS = {
    "source:operator-common-grammar-potential-goal:v1": (
        "potential-goal candidate",
        "establish richer shared grammar with the operator",
    ),
    "source:operator-common-grammar-local-stop:v1": (
        "local-stop",
        "establish no such goal and stop locally",
    ),
}
ALTERNATIVE_SOURCES = {
    "common-grammar-acquisition": "source:operator-common-grammar-potential-goal:v1",
    "local-stop": "source:operator-common-grammar-local-stop:v1",
}


def _representation_fingerprint(representations: object) -> str:
    encoded = json.dumps(
        representations, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode()
    return "operator-ingress-representations:" + hashlib.sha256(encoded).hexdigest()


@dataclass(frozen=True)
class AlternativeSourceRepresentation:
    presented_alternative_ref: str
    represented_source_ref: str
    represented_source_role: str
    representation_purpose: str
    choice_set_ref: str
    exact_choice_set_fingerprint: str
    presentation_ref: str
    rendered_label: str
    rendered_detail: str
    proposition_assertion: str
    representation_relation: str
    exact_set_participation: str
    source_attribution: str
    producer_occurrence_ref: str
    authority_limits: tuple[str, ...]
    provenance: tuple[str, ...]
    scope: str
    known_loss: tuple[str, ...] = ()
    unknowns: tuple[str, ...] = ()
    conflicts: tuple[str, ...] = ()


@dataclass(frozen=True)
class RecoveredRepresentedSource:
    presented_alternative_ref: str
    represented_source_ref: str
    represented_source_role: str
    proposition_assertion: str
    representation_provenance: tuple[str, ...]
    representation_scope: str
    representation_known_loss: tuple[str, ...]
    representation_occurrence_id: str


def common_grammar_representation_lineages(
    choice_set: PresentedClosedChoiceSet,
    producer_occurrence_ref: str,
) -> tuple[AlternativeSourceRepresentation, ...]:
    """Preserve the application-owned row-to-source assertions for this probe."""
    return tuple(
        AlternativeSourceRepresentation(
            option.presented_alternative_ref,
            ALTERNATIVE_SOURCES[option.presented_alternative_ref],
            SOURCE_PROPOSITIONS[ALTERNATIVE_SOURCES[option.presented_alternative_ref]][
                0
            ],
            "represent an application-owned bounded common-grammar source",
            choice_set.choice_set_ref,
            choice_set.exact_choice_set_fingerprint,
            choice_set.presentation_ref,
            option.presented_label,
            option.presented_detail,
            SOURCE_PROPOSITIONS[ALTERNATIVE_SOURCES[option.presented_alternative_ref]][
                1
            ],
            "presented_alternative_represents_application_owned_source",
            "member_of_exact_presented_choice_set",
            "application-owned common-grammar prerequisite source",
            producer_occurrence_ref,
            (
                "no meaning warrant",
                "no goal, stopping, acquisition, or action authority",
            ),
            (
                "seed_runtime.operator_ingress_common_grammar:alternative-source-lineage:v1",
            ),
            f"presentation:{choice_set.presentation_ref};choice-set:{choice_set.choice_set_ref}",
        )
        for option in choice_set.options
    )


def _recover_represented_source(
    binding, choice_set, occurrence, *, attempt_ref, presentation_occurrence
):
    """Recover from one earlier durable representation occurrence, never constants."""
    selected = binding.selected_presented_alternative_ref
    checks = (
        (occurrence is None, "no_recorded_representation_occurrence"),
        (
            occurrence is not None
            and occurrence.payload.get("attempt_ref") != attempt_ref,
            "wrong_attempt",
        ),
        (
            occurrence is not None
            and occurrence.payload.get("presentation_ref")
            != choice_set.presentation_ref,
            "wrong_presentation",
        ),
        (
            occurrence is not None
            and occurrence.payload.get("choice_set_ref") != choice_set.choice_set_ref,
            "wrong_choice_set",
        ),
        (
            occurrence is not None
            and occurrence.payload.get("choice_set_fingerprint")
            != choice_set.exact_choice_set_fingerprint,
            "wrong_set_fingerprint",
        ),
        (presentation_occurrence is None, "no_recorded_presentation_occurrence"),
        (
            presentation_occurrence is not None
            and presentation_occurrence.payload.get("attempt_ref") != attempt_ref,
            "wrong_presentation_attempt",
        ),
        (
            presentation_occurrence is not None
            and presentation_occurrence.payload.get("presentation_ref")
            != choice_set.presentation_ref,
            "wrong_presentation_occurrence",
        ),
        (
            presentation_occurrence is not None
            and presentation_occurrence.payload.get("choice_set_fingerprint")
            != choice_set.exact_choice_set_fingerprint,
            "presentation_fingerprint_mismatch",
        ),
        (
            binding.binding_state != "bound" or not selected,
            "no_selected_presented_alternative",
        ),
        (bool(binding.unknown_selection_evidence), "selection_evidence_unknown"),
        (
            bool(binding.conflicting_selection_evidence),
            "selection_evidence_conflicting",
        ),
    )
    for failed, reason in checks:
        if failed:
            return None, reason
    lineage = occurrence.payload.get("representations", ())
    if occurrence.payload.get(
        "representation_evidence_fingerprint"
    ) != _representation_fingerprint(lineage):
        return None, "forged_relation_payload"
    matches = [
        item for item in lineage if item.get("presented_alternative_ref") == selected
    ]
    if len(matches) != 1:
        return None, "selected_alternative_not_preserved"
    item = matches[0]
    required = {
        "represented_source_ref",
        "represented_source_role",
        "proposition_assertion",
        "representation_relation",
        "exact_set_participation",
        "rendered_label",
        "rendered_detail",
        "source_attribution",
        "producer_occurrence_ref",
        "provenance",
        "scope",
        "authority_limits",
        "known_loss",
        "unknowns",
        "conflicts",
    }
    if not required.issubset(item):
        return None, "representation_evidence_missing"
    if item["producer_occurrence_ref"] != occurrence.payload["dimensions"]["identity"]:
        return None, "forged_relation_payload"
    if (
        item["representation_relation"]
        != "presented_alternative_represents_application_owned_source"
    ):
        return None, "representation_relation_missing_or_conflicting"
    if item["exact_set_participation"] != "member_of_exact_presented_choice_set":
        return None, "exact_set_participation_missing_or_conflicting"
    if item["unknowns"]:
        return None, "representation_evidence_unknown"
    if item["conflicts"]:
        return None, "representation_evidence_conflicting"
    option = next(
        (o for o in choice_set.options if o.presented_alternative_ref == selected), None
    )
    if option is None:
        return None, "wrong_alternative_identity"
    if (
        item["rendered_label"] != option.presented_label
        or item["rendered_detail"] != option.presented_detail
    ):
        return None, "rendered_content_mismatch"
    return (
        RecoveredRepresentedSource(
            selected,
            item["represented_source_ref"],
            item["represented_source_role"],
            item["proposition_assertion"],
            tuple(item["provenance"]),
            item["scope"],
            tuple(item["known_loss"]),
            occurrence.id,
        ),
        None,
    )


def common_grammar_choice_set(presentation_ref: str) -> PresentedClosedChoiceSet:
    """Return the application-owned probe; callers can supply identity, not semantics."""
    return PresentedClosedChoiceSet(
        choice_set_ref=CHOICE_SET_REF,
        prompt=PROMPT,
        options=OPTIONS,
        presentation_ref=presentation_ref,
        provenance=("seed_runtime.operator_ingress_common_grammar:v1",),
    )


def render_probe(choice_set: PresentedClosedChoiceSet) -> str:
    return "\n".join(
        (
            choice_set.prompt,
            *(f"{o.token}. {o.presented_label}" for o in choice_set.options),
        )
    )


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


def project_operator_ingress_common_grammar_events(state, event) -> None:
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
        "closed",
        "response_kind",
    ):
        if key in event.payload:
            view[key] = event.payload[key]


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
            ingress_examination.represented_text if ingress_examination else None
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
    StateProjector(ledger).project(workspace_id)
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

    presentation_ref = f"presentation:{ingress.id}"
    choice_set = common_grammar_choice_set(presentation_ref)
    produced = _record(
        ledger,
        "operator.ingress.common_grammar.probe_produced",
        workspace_id,
        session_id,
        attempt,
        _dimensions(
            identity=CHOICE_SET_REF,
            content=render_probe(choice_set),
            standing="produced",
            source="application-owned probe v1",
            responsibility="probe-production",
            authority="invites only exact local token selection",
            scope=f"attempt:{attempt}",
            occurrence="versioned representation preserved",
        ),
        choice_set_ref=CHOICE_SET_REF,
        presentation_ref=presentation_ref,
        choice_set_fingerprint=choice_set.exact_choice_set_fingerprint,
        lineage=[ingress.id],
    )
    representation_ref = new_id("operator_ingress_representation")
    representations = common_grammar_representation_lineages(
        choice_set, representation_ref
    )
    representation_payload = [asdict(item) for item in representations]
    representation_event = _record(
        ledger,
        "operator.ingress.common_grammar.alternatives_represented",
        workspace_id,
        session_id,
        attempt,
        _dimensions(
            identity=representation_ref,
            content="application-owned alternatives represent carried sources",
            standing="preserved-before-selection",
            source="application-owned common-grammar prerequisite sources",
            responsibility="responsible-alternative-representation",
            authority="representation testimony only; no meaning warrant",
            scope=f"attempt:{attempt};presentation:{presentation_ref}",
            occurrence="exact representation relations and set participation durably preserved",
        ),
        choice_set_ref=choice_set.choice_set_ref,
        presentation_ref=presentation_ref,
        choice_set_fingerprint=choice_set.exact_choice_set_fingerprint,
        representations=representation_payload,
        representation_evidence_fingerprint=_representation_fingerprint(
            representation_payload
        ),
        lineage=[produced.id],
    )
    rendered = render_probe(choice_set)
    output_stream.write(rendered + "\n")
    output_stream.flush()
    presented = _record(
        ledger,
        "operator.ingress.common_grammar.presentation_occurred",
        workspace_id,
        session_id,
        attempt,
        _dimensions(
            identity=presentation_ref,
            content=rendered,
            standing="presented",
            source="real-shell-stdout",
            responsibility="presentation",
            authority="no acquisition or stopping authority",
            scope=f"attempt:{attempt}",
            occurrence="stdout emission recorded",
        ),
        choice_set_ref=CHOICE_SET_REF,
        presentation_ref=presentation_ref,
        choice_set_fingerprint=choice_set.exact_choice_set_fingerprint,
        lineage=[produced.id, representation_event.id],
    )
    (
        captured_response,
        response_examination,
        response_capture,
        response_examination_event,
    ) = _capture_representation(
        ledger=ledger,
        workspace=workspace_id,
        session=session_id,
        attempt=attempt,
        input_stream=response_input_stream,
        material_role="enum_response",
        lineage=(presented.id,),
    )
    raw_response = (
        response_examination.represented_text or "" if response_examination else ""
    )
    response_kind = (
        "eof"
        if captured_response.eof
        else "empty" if raw_response in {"\n", "\r\n"} else "token"
    )
    token = (
        ""
        if response_kind == "eof"
        else raw_response.removesuffix("\n").removesuffix("\r")
    )
    if response_kind == "eof":
        eof = _record(
            ledger,
            "operator.ingress.common_grammar.response_eof_occurred",
            workspace_id,
            session_id,
            attempt,
            _dimensions(
                identity=f"response-eof:{presented.id}",
                content=None,
                standing="occurred",
                source="real-shell-stdin",
                responsibility="response-occurrence",
                authority="EOF occurrence only; not a token or binding input",
                scope=f"attempt:{attempt}",
                occurrence="response EOF evidence preserved",
            ),
            raw_input=raw_response,
            response_kind="eof",
            presentation_ref=presentation_ref,
            raw_material_event_id=response_capture.id,
            lineage=[presented.id, response_capture.id],
        )
        _record(
            ledger,
            "operator.ingress.common_grammar.stopping_occurred",
            workspace_id,
            session_id,
            attempt,
            _dimensions(
                identity=f"stop:{eof.id}",
                content="response EOF",
                standing="closed",
                source=eof.id,
                responsibility="competent-local-stopping",
                authority="closes only this interaction",
                scope=f"attempt:{attempt}",
                occurrence="separate stopping act recorded",
            ),
            closed=True,
            response_kind="eof",
            lineage=[eof.id],
        )
        state = StateProjector(ledger).project(workspace_id)
        output_stream.write(
            "Operator-ingress common-grammar interaction stopped locally.\n"
        )
        output_stream.flush()
        return state.operator_ingress_common_grammar_attempts[attempt]

    if response_examination is not None and not response_examination.succeeded:
        _record(
            ledger,
            "operator.ingress.common_grammar.stopping_occurred",
            workspace_id,
            session_id,
            attempt,
            _dimensions(
                identity=f"stop:{response_examination_event.id}",
                content="response representation insufficiency",
                standing="closed",
                source=response_examination_event.id,
                responsibility="competent-local-stopping",
                authority="closes only this interaction",
                scope=f"attempt:{attempt}",
                occurrence="separate stopping act recorded",
            ),
            closed=True,
            response_kind="representation_insufficient",
            lineage=[response_examination_event.id],
        )
        state = StateProjector(ledger).project(workspace_id)
        output_stream.write(
            "Representation insufficient: captured response did not decode under the selected decoder mechanism.\n"
        )
        output_stream.flush()
        return state.operator_ingress_common_grammar_attempts[attempt]

    capture_ref = f"capture:{presented.id}"
    response = _record(
        ledger,
        "operator.ingress.common_grammar.response_captured",
        workspace_id,
        session_id,
        attempt,
        _dimensions(
            identity=capture_ref,
            content=None if response_kind == "eof" else token,
            standing="captured",
            source=response_examination_event.id,
            responsibility="response-capture",
            authority="occurrence-only; meaning and intent Unknown until binding",
            scope=f"choice-set:{CHOICE_SET_REF}",
            occurrence="strictly decoded text preserves capture/examination lineage",
        ),
        raw_input=raw_response,
        response_kind=response_kind,
        choice_set_ref=CHOICE_SET_REF,
        presentation_ref=presentation_ref,
        capture_ref=capture_ref,
        choice_set_fingerprint=choice_set.exact_choice_set_fingerprint,
        lineage=[presented.id, response_capture.id, response_examination_event.id],
        raw_material_event_id=response_capture.id,
        representation_examination_event_id=response_examination_event.id,
    )
    capture = OperatorSelectionTokenCapture(
        capture_ref, CHOICE_SET_REF, token, provenance=(response.id,)
    )
    binding = validate_capture_for_probe(
        ledger=ledger,
        workspace_id=workspace_id,
        attempt_ref=attempt,
        choice_set=choice_set,
        capture=capture,
    )
    unknowns = (
        ()
        if binding.binding_state == "bound"
        else (
            "response meaning Unknown",
            "operator intent Unknown",
            "requested alternative Unknown",
        )
    )
    finding_kind = (
        "binding_completed"
        if binding.binding_state == "bound"
        else "unsupported_finding"
    )
    binding_event = _record(
        ledger,
        f"operator.ingress.common_grammar.{finding_kind}",
        workspace_id,
        session_id,
        attempt,
        _dimensions(
            identity=binding.binding_id,
            content=token,
            standing=binding.binding_state,
            source=f"capture:{capture_ref};presentation:{presentation_ref}",
            responsibility="exact-set-binding",
            authority="binding only; no acquisition authority",
            scope=f"exact-choice-set:{CHOICE_SET_REF}",
            occurrence="binding finding recorded",
        ),
        binding_id=binding.binding_id,
        capture_ref=capture_ref,
        choice_set_ref=CHOICE_SET_REF,
        response_kind=response_kind,
        unknowns=list(unknowns),
        choice_set_fingerprint=choice_set.exact_choice_set_fingerprint,
        lineage=[response.id, presented.id],
    )
    if binding.binding_state == "bound":
        alternative = binding.selected_presented_alternative_ref
        selection = _record(
            ledger,
            "operator.ingress.common_grammar.alternative_selected",
            workspace_id,
            session_id,
            attempt,
            _dimensions(
                identity=alternative,
                content=token,
                standing="selected",
                source=binding_event.id,
                responsibility="presented-alternative-selection",
                authority="selection only; acquisition not authorized or begun",
                scope=f"attempt:{attempt}",
                occurrence="selection event recorded",
            ),
            selected_presented_alternative_ref=alternative,
            binding_id=binding.binding_id,
            lineage=[binding_event.id],
        )
        representation_occurrences = [
            event
            for event in ledger.list_events(workspace_id)
            if event.kind == "operator.ingress.common_grammar.alternatives_represented"
            and event.payload.get("attempt_ref") == attempt
        ]
        recorded_representation = (
            representation_occurrences[0]
            if len(representation_occurrences) == 1
            else None
        )
        recovered, refusal_reason = _recover_represented_source(
            binding,
            choice_set,
            recorded_representation,
            attempt_ref=attempt,
            presentation_occurrence=presented,
        )
        if recovered is None:
            _record(
                ledger,
                "operator.ingress.common_grammar.source_recovery_refused",
                workspace_id,
                session_id,
                attempt,
                _dimensions(
                    identity=f"source-recovery-refusal:{selection.id}",
                    content=refusal_reason,
                    standing="refused",
                    source=selection.id,
                    responsibility="represented-source-recovery",
                    authority="refusal only; establishes no source or proposition standing",
                    scope=f"attempt:{attempt}",
                    occurrence="bounded source-recovery refusal durably recorded",
                ),
                refusal_reason=refusal_reason,
                selected_presented_alternative_ref=alternative,
                lineage=[presented.id, binding_event.id, selection.id],
            )
            result = f"Source recovery refused: {refusal_reason}."
        else:
            _record(
                ledger,
                "operator.ingress.common_grammar.source_recovered",
                workspace_id,
                session_id,
                attempt,
                _dimensions(
                    identity=recovered.represented_source_ref,
                    content=recovered.proposition_assertion,
                    standing="recovered",
                    source=";".join(recovered.representation_provenance),
                    responsibility="alternative-source-lineage-recovery",
                    authority="source identity recovery only; no meaning warrant, goal, acquisition, or stop",
                    scope=recovered.representation_scope,
                    occurrence="separate responsible source-recovery occurrence recorded",
                ),
                selected_presented_alternative_ref=alternative,
                recovered_source_ref=recovered.represented_source_ref,
                recovered_source_role=recovered.represented_source_role,
                recovered_source_proposition=recovered.proposition_assertion,
                choice_set_fingerprint=choice_set.exact_choice_set_fingerprint,
                presentation_ref=presentation_ref,
                known_loss=list(recovered.representation_known_loss),
                representation_occurrence_id=recovered.representation_occurrence_id,
                lineage=[
                    recovered.representation_occurrence_id,
                    presented.id,
                    binding_event.id,
                    selection.id,
                ],
            )
            if recovered.represented_source_role == "local-stop":
                result = (
                    "Local-stop source recovered; bounded stop was not established."
                )
            else:
                result = "Potential-goal source recovered; bounded goal was not established and acquisition was not authorized or begun."
    else:
        result = "Unsupported response: exact token 1 or 2 required."
    state = StateProjector(ledger).project(workspace_id)
    output_stream.write(result + "\n")
    output_stream.flush()
    return state.operator_ingress_common_grammar_attempts[attempt]


def validate_capture_for_probe(
    *,
    ledger: EventLedger,
    workspace_id: str,
    attempt_ref: str,
    choice_set: PresentedClosedChoiceSet,
    capture: OperatorSelectionTokenCapture,
    unsupported_selection_evidence: tuple[str, ...] = (),
):
    """Validate production identity/currentness and consume one recorded capture."""
    events = [
        event
        for event in ledger.list_events(workspace_id)
        if event.payload.get("attempt_ref") == attempt_ref
    ]
    presentations = [
        event
        for event in events
        if event.kind == "operator.ingress.common_grammar.presentation_occurred"
    ]
    captures = [
        event
        for event in events
        if event.kind == "operator.ingress.common_grammar.response_captured"
    ]
    if not presentations or not captures:
        raise ClosedChoiceSelectionBindingError(
            "communication probe lacks recorded presentation or capture evidence"
        )
    presentation = presentations[-1]
    recorded_capture = captures[-1]
    fingerprint = choice_set.exact_choice_set_fingerprint
    if (
        choice_set.choice_set_ref != CHOICE_SET_REF
        or choice_set.presentation_ref != presentation.payload.get("presentation_ref")
        or capture.choice_set_ref != presentation.payload.get("choice_set_ref")
        or fingerprint != presentation.payload.get("choice_set_fingerprint")
    ):
        raise ClosedChoiceSelectionBindingError(
            "communication probe presentation/set identity or fingerprint mismatch"
        )
    if (
        capture.capture_ref != recorded_capture.payload.get("capture_ref")
        or capture.choice_set_ref != recorded_capture.payload.get("choice_set_ref")
        or capture.captured_token
        != (
            ""
            if recorded_capture.payload.get("response_kind") == "eof"
            else recorded_capture.payload.get("raw_input", "")
            .removesuffix("\n")
            .removesuffix("\r")
        )
    ):
        raise ClosedChoiceSelectionBindingError(
            "communication probe capture is not the current recorded occurrence"
        )
    if any(
        event.kind
        in {
            "operator.ingress.common_grammar.binding_completed",
            "operator.ingress.common_grammar.unsupported_finding",
        }
        and event.payload.get("capture_ref") == capture.capture_ref
        for event in events
    ):
        raise ClosedChoiceSelectionBindingError(
            "communication probe response capture was already consumed"
        )
    return bind_closed_choice_selection(
        choice_set,
        capture,
        unsupported_selection_evidence=unsupported_selection_evidence,
    )
