"""Process-local repetition around bounded operator ingress and Representation."""

from __future__ import annotations

from typing import TextIO

from seed_runtime.events import EventLedger
from seed_runtime.operator_ingress import run_operator_ingress_attempt
from seed_runtime.operator_ingress_representation import capture_stdin_material
from seed_runtime.operator_representation import (
    emit_operator_representation,
    record_operator_representation,
)
from seed_runtime.operator_session_standing import (
    advance_operator_session_standing,
    read_operator_session_standing,
)


def _is_console_exit(material: bytes, encoding: str | None) -> bool:
    command = material.removesuffix(b"\n").removesuffix(b"\r")
    try:
        return command == "exit".encode(encoding or "utf-8", errors="strict")
    except LookupError:
        return False


def _advance_over(ledger, standing, event_ids, *, workspace_id, session_id):
    """Advance carried Standing over occurrences a responsible act just recorded.

    The identifiers come from the act that recorded them, so nothing here
    searches the ledger for what happened; the events are retrieved by exact
    identifier.
    """

    return advance_operator_session_standing(
        [ledger.get(event_id) for event_id in event_ids],
        workspace_id=workspace_id,
        session_id=session_id,
        prior=standing,
    )


def run_persistent_operator_console(
    *,
    ledger: EventLedger,
    workspace_id: str,
    session_id: str,
    input_stream: TextIO,
    output_stream: TextIO,
    process_boundary_escape: bool = True,
) -> None:
    """Repeat bounded operator interactions within this process."""
    # A console that declined to install the escape does not announce it.
    if process_boundary_escape:
        output_stream.write("Seed console: `exit` exits.\n")
        output_stream.flush()
    # Standing is carried through the session rather than re-projected before
    # each interaction. Each responsible act returns the occurrences it
    # recorded, so the console advances over exactly those occurrences.
    session_standing = read_operator_session_standing(
        ledger, workspace_id=workspace_id, session_id=session_id
    )
    representation = record_operator_representation(
        ledger,
        workspace_id=workspace_id,
        session_id=session_id,
        session_standing=session_standing,
    )
    representation = emit_operator_representation(
        ledger, representation=representation, output_stream=output_stream
    )
    session_standing = _advance_over(
        ledger,
        session_standing,
        (
            representation["representation_event_id"],
            representation["emission_attempt_event_id"],
            representation["emitted_event_id"],
        ),
        workspace_id=workspace_id,
        session_id=session_id,
    )
    while True:
        captured_ingress = capture_stdin_material(input_stream)
        # `exit` is a surrounding process escape, not operator ingress. The
        # switch is bootstrap scaffolding for non-interactive acquisition:
        # without the escape installed, exact material named `exit` is
        # preserved and termination comes from EOF.
        if captured_ingress.eof:
            return
        if process_boundary_escape and _is_console_exit(
            captured_ingress.exact_bytes, captured_ingress.stream_encoding_metadata
        ):
            return
        # No Representation is attached to this capture. Selecting one by
        # recency would assert a relation no occurrence determined.
        attempt_view = run_operator_ingress_attempt(
            ledger=ledger,
            workspace_id=workspace_id,
            session_id=session_id,
            captured_ingress=captured_ingress,
            output_stream=output_stream,
            session_standing=(
                session_standing if session_standing["event_count"] else None
            ),
        )
        session_standing = _advance_over(
            ledger,
            session_standing,
            attempt_view["event_ids"],
            workspace_id=workspace_id,
            session_id=session_id,
        )
        if attempt_view["current_standing"]["preserved_ingress"] is not None:
            # The yielded Representation is preserved independently. No Compare
            # or Identification is inferred merely from temporal proximity.
            representation = record_operator_representation(
                ledger,
                workspace_id=workspace_id,
                session_id=session_id,
                session_standing=session_standing,
            )
            representation = emit_operator_representation(
                ledger, representation=representation, output_stream=output_stream
            )
            session_standing = _advance_over(
                ledger,
                session_standing,
                (
                    representation["representation_event_id"],
                    representation["emission_attempt_event_id"],
                    representation["emitted_event_id"],
                ),
                workspace_id=workspace_id,
                session_id=session_id,
            )
