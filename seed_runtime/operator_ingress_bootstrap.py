"""One-attempt production bootstrap for unknown operator common grammar."""

from __future__ import annotations

from typing import TextIO

from seed_runtime.closed_choice_selection_binding import (
    ClosedChoiceOption,
    ClosedChoiceSelectionBindingError,
    OperatorSelectionTokenCapture,
    PresentedClosedChoiceSet,
    bind_closed_choice_selection,
)
from seed_runtime.events import EventLedger
from seed_runtime.ids import new_id
from seed_runtime.state import StateProjector

CHOICE_SET_REF = "operator-common-grammar-bootstrap:v1:two-treatment"
PROMPT = "Select one treatment by its exact token:"
OPTIONS = (
    ClosedChoiceOption(
        "1",
        "common-grammar-acquisition",
        "Select bounded common-grammar acquisition treatment.",
    ),
    ClosedChoiceOption("2", "local-stop", "Select local stopping treatment."),
)


def bootstrap_choice_set(presentation_ref: str) -> PresentedClosedChoiceSet:
    """Return the application-owned probe; callers can supply identity, not semantics."""
    return PresentedClosedChoiceSet(
        choice_set_ref=CHOICE_SET_REF,
        prompt=PROMPT,
        options=OPTIONS,
        presentation_ref=presentation_ref,
        provenance=("seed_runtime.operator_ingress_bootstrap:v1",),
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


def project_bootstrap_events(state, event) -> None:
    """Dispatch one bootstrap event into the dedicated current view."""
    if not event.kind.startswith("operator.bootstrap."):
        return
    attempt = event.payload["attempt_ref"]
    view = state.operator_ingress_bootstraps.setdefault(
        attempt,
        {
            "event_ids": [],
            "dimensional_standing": {},
            "known_loss": [],
            "unknowns": [],
            "conflicts": [],
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
    view["current_dimensions"] = event.payload["dimensions"]
    view["standing"] = event.payload["dimensions"]["standing"]
    view["last_event_kind"] = event.kind
    for key in ("known_loss", "unknowns", "conflicts"):
        view[key] = sorted(set((*view[key], *event.payload.get(key, ()))))
    for key in (
        "choice_set_ref",
        "presentation_ref",
        "capture_ref",
        "binding_id",
        "selected_treatment",
        "closed",
        "response_kind",
    ):
        if key in event.payload:
            view[key] = event.payload[key]


def run_operator_ingress_bootstrap(
    *,
    ledger: EventLedger,
    workspace_id: str,
    session_id: str,
    input_stream: TextIO,
    output_stream: TextIO,
) -> dict[str, object]:
    """Run exactly one ingress/probe/response attempt and stop."""
    attempt = new_id("operator_bootstrap_attempt")
    raw_ingress = input_stream.readline()
    ingress_kind = (
        "eof"
        if raw_ingress == ""
        else "empty" if raw_ingress in {"\n", "\r\n"} else "text"
    )
    ingress_content = (
        None
        if ingress_kind == "eof"
        else raw_ingress.removesuffix("\n").removesuffix("\r")
    )
    ingress = _record(
        ledger,
        (
            "operator.bootstrap.initial_eof_occurred"
            if ingress_kind == "eof"
            else "operator.bootstrap.ingress_occurred"
        ),
        workspace_id,
        session_id,
        attempt,
        _dimensions(
            identity=attempt,
            content=ingress_content,
            standing="occurred",
            source="real-shell-stdin",
            responsibility="operator-ingress",
            authority="occurrence-only; meaning Unknown",
            scope=f"workspace:{workspace_id};session:{session_id}",
            occurrence="exact raw input preserved",
        ),
        raw_input=raw_ingress,
        ingress_kind=ingress_kind,
        known_loss=["terminal framing outside captured line is not preserved"],
    )
    StateProjector(ledger).project(workspace_id)
    if ingress_kind == "eof":
        _record(
            ledger,
            "operator.bootstrap.stopping_occurred",
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
        output_stream.write("Bootstrap stopped locally.\n")
        output_stream.flush()
        return state.operator_ingress_bootstraps[attempt]

    presentation_ref = f"presentation:{ingress.id}"
    choice_set = bootstrap_choice_set(presentation_ref)
    _record(
        ledger,
        "operator.bootstrap.probe_produced",
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
    rendered = render_probe(choice_set)
    output_stream.write(rendered + "\n")
    output_stream.flush()
    presented = _record(
        ledger,
        "operator.bootstrap.presentation_occurred",
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
        lineage=[ingress.id],
    )
    raw_response = input_stream.readline()
    response_kind = (
        "eof"
        if raw_response == ""
        else "empty" if raw_response in {"\n", "\r\n"} else "token"
    )
    token = (
        ""
        if response_kind == "eof"
        else raw_response.removesuffix("\n").removesuffix("\r")
    )
    capture_ref = f"capture:{presented.id}"
    response = _record(
        ledger,
        "operator.bootstrap.response_captured",
        workspace_id,
        session_id,
        attempt,
        _dimensions(
            identity=capture_ref,
            content=None if response_kind == "eof" else token,
            standing="captured",
            source="real-shell-stdin",
            responsibility="response-capture",
            authority="occurrence-only; meaning and intent Unknown until binding",
            scope=f"choice-set:{CHOICE_SET_REF}",
            occurrence="exact raw response preserved",
        ),
        raw_input=raw_response,
        response_kind=response_kind,
        choice_set_ref=CHOICE_SET_REF,
        presentation_ref=presentation_ref,
        capture_ref=capture_ref,
        choice_set_fingerprint=choice_set.exact_choice_set_fingerprint,
        lineage=[presented.id],
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
        unsupported_selection_evidence=(
            ("EOF is not a selection token",) if response_kind == "eof" else ()
        ),
    )
    unknowns = (
        ()
        if binding.binding_state == "bound"
        else (
            "response meaning Unknown",
            "operator intent Unknown",
            "requested treatment Unknown",
        )
    )
    finding_kind = (
        "binding_completed"
        if binding.binding_state == "bound"
        else "unsupported_finding"
    )
    binding_event = _record(
        ledger,
        f"operator.bootstrap.{finding_kind}",
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
        treatment = binding.bound_option_ref
        selection = _record(
            ledger,
            "operator.bootstrap.treatment_selected",
            workspace_id,
            session_id,
            attempt,
            _dimensions(
                identity=treatment,
                content=token,
                standing="selected",
                source=binding_event.id,
                responsibility="treatment-selection",
                authority="selection only; acquisition not authorized or begun",
                scope=f"attempt:{attempt}",
                occurrence="selection event recorded",
            ),
            selected_treatment=treatment,
            binding_id=binding.binding_id,
            lineage=[binding_event.id],
        )
        if treatment == "local-stop":
            _record(
                ledger,
                "operator.bootstrap.stopping_occurred",
                workspace_id,
                session_id,
                attempt,
                _dimensions(
                    identity=f"stop:{selection.id}",
                    content="local stop",
                    standing="closed",
                    source=selection.id,
                    responsibility="competent-local-stopping",
                    authority="closes only this interaction",
                    scope=f"attempt:{attempt}",
                    occurrence="separate stopping act recorded",
                ),
                selected_treatment=treatment,
                closed=True,
                lineage=[selection.id],
            )
            result = "Bootstrap stopped locally."
        else:
            result = "Common-grammar acquisition treatment selected; acquisition was not authorized or begun."
    else:
        result = "Unsupported response: exact token 1 or 2 required."
    state = StateProjector(ledger).project(workspace_id)
    output_stream.write(result + "\n")
    output_stream.flush()
    return state.operator_ingress_bootstraps[attempt]


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
        if event.kind == "operator.bootstrap.presentation_occurred"
    ]
    captures = [
        event
        for event in events
        if event.kind == "operator.bootstrap.response_captured"
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
            "operator.bootstrap.binding_completed",
            "operator.bootstrap.unsupported_finding",
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
