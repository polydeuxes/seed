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
        attempt, {"event_ids": [], "known_loss": [], "unknowns": [], "conflicts": []}
    )
    view["event_ids"].append(event.id)
    view["dimensions"] = event.payload["dimensions"]
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
    attempt = f"operator-bootstrap:{session_id}"
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
        "operator.bootstrap.ingress_occurred",
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
    )
    capture = OperatorSelectionTokenCapture(
        capture_ref, CHOICE_SET_REF, token, provenance=(response.id,)
    )
    binding = bind_closed_choice_selection(
        choice_set,
        capture,
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
    choice_set, capture, expected_presentation_ref: str, seen_capture_refs=()
):
    """Goal-local admission seam for identity and replay checks."""
    if (
        choice_set.choice_set_ref != CHOICE_SET_REF
        or choice_set.presentation_ref != expected_presentation_ref
    ):
        raise ClosedChoiceSelectionBindingError(
            "communication probe presentation/set identity mismatch"
        )
    if capture.capture_ref in seen_capture_refs:
        raise ClosedChoiceSelectionBindingError(
            "communication probe response capture was already replayed"
        )
    return bind_closed_choice_selection(choice_set, capture)
