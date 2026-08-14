"""Recorded formation and emission of bounded operator representations.

A Representation carries exact formed content from current session Standing.
It may also carry alternatives whose source relations remain separately
bounded.
"""

from __future__ import annotations

from typing import Any, TextIO

from seed_runtime.events import EventLedger
from seed_runtime.ids import new_id

REPRESENTATION_FORMED_KIND = "operator.representation.formed"
from seed_runtime.operator_ingress import SEED_ORIGIN

REPRESENTATION_EMISSION_ATTEMPTED_KIND = "operator.representation.emission_attempted"
REPRESENTATION_EMITTED_KIND = "operator.representation.emitted"
REPRESENTATION_EMISSION_OUTCOME_KIND = "operator.representation.emission_outcome_recorded"

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


def form_operator_representation(
    ledger: EventLedger,
    *,
    workspace_id: str,
    session_id: str,
    session_standing: dict[str, Any],
    alternative_sources: tuple[dict[str, Any], ...] = (),
) -> dict[str, Any]:
    """Form one exact bounded Representation and record its formation occurrence.

    The Representation is bounded by the supplied projected session Standing.
    No alternatives are supplied by default; ``alternative_sources`` must be
    supplied by a caller with support for the eligibility and participation
    relations those alternatives carry.  Formation neither invents sources
    nor strengthens their standing, and no alternative's represented relation is derived
    from ingress material.  This module records what a Representation carries;
    it does not classify the resulting combination as a shape.

    Formation is not emission: the returned Representation carries no emission
    occurrence until :func:`emit_operator_representation` records one.
    """
    representation_id = new_id("operator_representation")
    scope = f"workspace:{workspace_id};session:{session_id}"
    alternatives = []
    coordinate_bindings: dict[str, str] = {}
    for position, source in enumerate(alternative_sources, start=1):
        alternative_id = new_id("represented_alternative")
        coordinate = str(position)
        alternatives.append(
            {
                "alternative_id": alternative_id,
                "role": source["role"],
                "response_coordinate": coordinate,
                "rendered_label": source["rendered_label"],
                "represented_source": dict(source["represented_source"]),
                # Each A-to-G representation relation preserves its own
                # boundary; Representation-level coordinates do not transfer
                # to it by identity.
                "representation": {
                    "formation_result": source["representation_result_boundary"],
                    "scope": scope,
                    "provenance": source["represented_source"]["reference"],
                    # No separately recorded source-evidence events exist
                    # for a developer-supplied source; empty is absence of
                    # record, not negative standing and not Unknown.
                    "evidence_event_ids": [],
                    "known_loss": [
                        "rendered label compresses represented candidate "
                        "represented relation"
                    ],
                    "unknowns": [],
                    "conflicts": [],
                },
            }
        )
        coordinate_bindings[coordinate] = alternative_id
    formation_result = "bounded representation of current session Standing"
    content = "bounded Representation of current session Standing"
    occurrence = "Representation formation durably recorded"
    known_loss: list[str] = []
    if alternatives:
        content = (
            "bounded Representation of current session Standing with "
            f"{len(alternatives)} represented alternatives"
        )
        occurrence = (
            f"{len(alternatives)} alternatives, roles, response-coordinate "
            "bindings, and represented provenance occurrences durably recorded"
        )
        formation_result += " with bounded alternatives and preserved source roles"
        known_loss.append(
            "rendered label compresses represented candidate relation"
        )
    # The latest recorded exchange finding, exposed exactly as recorded;
    # formation neither strengthens nor reinterprets it.
    prior_exchange_finding = session_standing.get("latest_exchange_finding")
    # The reconstructed source relation is exposed only when it belongs to the
    # exact latest finding's identification.
    represented_relation = None
    latest_relation = session_standing.get("latest_represented_relation")
    if (
        prior_exchange_finding is not None
        and latest_relation is not None
        and latest_relation["identification_event_id"]
        == prior_exchange_finding["identification"]["event_id"]
    ):
        represented_relation = latest_relation
    formed_event = ledger.append(
        REPRESENTATION_FORMED_KIND,
        workspace_id,
        {
            "attempt_ref": None,
            "representation_ref": representation_id,
            "dimensions": _dimensions(
                identity=representation_id,
                content=content,
                standing="formed",
                source=session_standing["as_of_event_id"],
                responsibility="bounded-representation-formation",
                authority=(
                    "formation occurrence only; establishes no Selection, "
                    "input support, or response treatment"
                ),
                scope=scope,
                occurrence=occurrence,
            ),
            "formation_result": formation_result,
            "alternatives": alternatives,
            "coordinate_bindings": coordinate_bindings,
            "session_standing_as_of_event_id": session_standing["as_of_event_id"],
            "prior_exchange_finding": prior_exchange_finding,
            "represented_relation": represented_relation,
            "known_loss": known_loss,
            "unknowns": [],
            "conflicts": [],
            "mutates_cluster": False,
        },
        session_id=session_id,
    )
    return {
        "representation_id": representation_id,
        "workspace_id": workspace_id,
        "session_id": session_id,
        "formation_result": formation_result,
        "alternatives": alternatives,
        "coordinate_bindings": coordinate_bindings,
        "formed_event_id": formed_event.id,
        "emission_attempt_event_id": None,
        "emission_outcome_event_id": None,
        "emitted_event_id": None,
        "session_standing_as_of_event_id": session_standing["as_of_event_id"],
        "prior_exchange_finding": prior_exchange_finding,
        "represented_relation": represented_relation,
        "known_loss": known_loss,
        "unknowns": [],
        "conflicts": [],
    }


def render_operator_representation(representation: dict[str, Any]) -> str:
    """Render the bounded Representation for the console output stream.

    Rendering exposes tokens, labels, and roles.  A rendered label is not the
    represented candidate's full represented relation; that represented relation stays preserved in the
    recorded formation payload.
    """
    lines = [f"Bounded Representation {representation['representation_id']}"]
    finding = representation.get("prior_exchange_finding")
    if finding is not None:
        identification = finding["identification"]
        comparison = finding["comparison"]
        if identification["identified_alternative"] is not None:
            alternative = identification["identified_alternative"]
            lines.append(
                "Prior exchange: alternative "
                f"{alternative['response_coordinate']} "
                f"({alternative['rendered_label']}) corresponds to the "
                f"captured material within {comparison['representation_ref']}. "
                "Operator intent and selection remain Unknown."
            )
        elif comparison["matched_coordinate"] is not None:
            # A matched coordinate whose binding failed is not a no-match;
            # the two recorded results stay distinguishable here.
            lines.append(
                "Prior exchange: coordinate "
                f"{comparison['matched_coordinate']} matched within "
                f"{comparison['representation_ref']}, but no represented "
                "alternative was lawfully identified "
                f"({identification['basis']})."
            )
        else:
            lines.append(
                "Prior exchange: no coordinate match within "
                f"{comparison['representation_ref']}; response represented relation and "
                "requested treatment remain Unknown."
            )
    relation = representation.get("represented_relation")
    if relation is not None:
        lines.append(
            f"Reconstructed source {relation['source_identity']} expresses: "
            f"\"{relation['proposition']}\" "
            f"({relation['source_role']}). Operator intent and "
            "selection remain Unknown; Operator Authority for this "
            "proposition remains unresolved."
        )
    if representation["alternatives"]:
        lines.append("Respond with exactly one token:")
    for alternative in representation["alternatives"]:
        lines.append(
            f"  {alternative['response_coordinate']}. {alternative['rendered_label']}"
            f"  [{alternative['role']}]"
        )
    return "\n".join(lines) + "\n"


def emit_operator_representation(
    ledger: EventLedger,
    *,
    representation: dict[str, Any],
    output_stream: TextIO,
) -> dict[str, Any]:
    """Write the Representation to the output stream and record the emission.

    Emission evidences only that the rendering was written to this boundary;
    effects beyond that output boundary require separate Evidence.
    """
    emitted_representation = render_operator_representation(representation)
    stream_encoding_metadata = getattr(output_stream, "encoding", None)
    if type(stream_encoding_metadata) is not str or not stream_encoding_metadata:
        stream_encoding_metadata = None
    scope = (
        f"workspace:{representation['workspace_id']};"
        f"session:{representation['session_id']}"
    )
    attempt_event = ledger.append(
        REPRESENTATION_EMISSION_ATTEMPTED_KIND,
        representation["workspace_id"],
        {
            "representation_ref": representation["representation_id"],
            "formed_event_id": representation["formed_event_id"],
            "dimensions": _dimensions(
                identity=f"emission-attempt:{representation['representation_id']}",
                content="exact text prepared for the declared output boundary",
                standing="attempt recorded; output-boundary outcome Unknown",
                source=representation["formed_event_id"],
                responsibility="bounded-representation-emission",
                authority=(
                    "attempt occurrence only; establishes no output-boundary "
                    "acceptance or downstream effect"
                ),
                scope=scope,
                occurrence="emission attempt durably recorded before output",
            ),
            "material_origin": SEED_ORIGIN,
            "attempted_representation": emitted_representation,
            "attempted_representation_kind": "text",
            "output_boundary": "text_stream_write",
            "stream_encoding_metadata": stream_encoding_metadata,
            "known_loss": [],
            "unknowns": [
                "output-boundary acceptance remains Unknown until an outcome is recorded",
                "effects beyond the output boundary remain Unknown",
            ],
            "conflicts": [],
            "provenance_occurrence_refs": [representation["formed_event_id"]],
            "mutates_cluster": False,
        },
        session_id=representation["session_id"],
    )
    representation["emission_attempt_event_id"] = attempt_event.id

    try:
        written = output_stream.write(emitted_representation)
    except Exception as error:
        failed_event = _record_emission_failure_outcome(
            ledger,
            representation=representation,
            attempt_event_id=attempt_event.id,
            scope=scope,
            stream_encoding_metadata=stream_encoding_metadata,
            phase="text_stream_write",
            written=None,
            error=error,
        )
        representation["emission_outcome_event_id"] = failed_event.id
        raise

    if type(written) is not int or written != len(emitted_representation):
        failed_event = _record_emission_failure_outcome(
            ledger,
            representation=representation,
            attempt_event_id=attempt_event.id,
            scope=scope,
            stream_encoding_metadata=stream_encoding_metadata,
            phase="text_stream_write",
            written=written,
            error=None,
        )
        representation["emission_outcome_event_id"] = failed_event.id
        raise ValueError("output boundary did not accept the exact representation")

    emitted_event = ledger.append(
        REPRESENTATION_EMITTED_KIND,
        representation["workspace_id"],
        {
            "attempt_ref": attempt_event.id,
            "representation_ref": representation["representation_id"],
            "formed_event_id": representation["formed_event_id"],
            "dimensions": _dimensions(
                identity=f"emission:{representation['representation_id']}",
                content="representation rendering written to console output stream",
                standing="emitted",
                source=representation["formed_event_id"],
                responsibility="bounded-representation-emission",
                authority=(
                    "emission occurrence only; effects beyond the output "
                    "boundary require separate Evidence"
                ),
                scope=scope,
                occurrence="emission occurrence durably recorded",
            ),
            "material_origin": SEED_ORIGIN,
            "emitted_representation": emitted_representation,
            "emitted_representation_kind": "text",
            "output_boundary": "text_stream_write",
            "stream_encoding_metadata": stream_encoding_metadata,
            "write_length": written,
            "known_loss": [],
            "unknowns": [],
            "conflicts": [],
            "provenance_occurrence_refs": [
                representation["formed_event_id"],
                attempt_event.id,
            ],
            "mutates_cluster": False,
        },
        session_id=representation["session_id"],
    )
    representation["emission_outcome_event_id"] = emitted_event.id
    representation["emitted_event_id"] = emitted_event.id
    try:
        output_stream.flush()
    except Exception as error:
        failed_event = _record_emission_failure_outcome(
            ledger,
            representation=representation,
            attempt_event_id=attempt_event.id,
            scope=scope,
            stream_encoding_metadata=stream_encoding_metadata,
            phase="text_stream_flush",
            written=written,
            error=error,
            emitted_event_id=emitted_event.id,
        )
        representation["emission_outcome_event_id"] = failed_event.id
        raise
    return representation


def _record_emission_failure_outcome(
    ledger: EventLedger,
    *,
    representation: dict[str, Any],
    attempt_event_id: str,
    scope: str,
    stream_encoding_metadata: str | None,
    phase: str,
    written: Any,
    error: Exception | None,
    emitted_event_id: str | None = None,
):
    """Preserve the bounded failure without inferring downstream state."""
    if type(written) is int and written >= 0:
        reported_write_length: int | None = written
    else:
        reported_write_length = None
    outcome = (
        "flush_failed_after_emission"
        if emitted_event_id is not None
        else "write_failed"
    )
    return ledger.append(
        REPRESENTATION_EMISSION_OUTCOME_KIND,
        representation["workspace_id"],
        {
            "attempt_ref": attempt_event_id,
            "representation_ref": representation["representation_id"],
            "formed_event_id": representation["formed_event_id"],
            "emitted_event_id": emitted_event_id,
            "dimensions": _dimensions(
                identity=f"emission-outcome:{attempt_event_id}:{phase}",
                content=f"{phase} did not complete the emission call",
                standing=outcome,
                source=attempt_event_id,
                responsibility="bounded-representation-emission",
                authority=(
                    "failure occurrence only; establishes no downstream effect "
                    "and no acceptance beyond the reported write result"
                ),
                scope=scope,
                occurrence="emission failure durably recorded",
            ),
            "failure_phase": phase,
            "outcome": outcome,
            "reported_write_length": reported_write_length,
            "expected_write_length": len(
                render_operator_representation(representation)
            ),
            "error_type": type(error).__name__ if error is not None else None,
            "error_message": str(error) if error is not None else None,
            "output_boundary": "text_stream_write",
            "stream_encoding_metadata": stream_encoding_metadata,
            "known_loss": [],
            "unknowns": ["effects beyond the output boundary remain Unknown"],
            "conflicts": [],
            "provenance_occurrence_refs": [
                representation["formed_event_id"],
                attempt_event_id,
                *([emitted_event_id] if emitted_event_id is not None else []),
            ],
            "mutates_cluster": False,
        },
        session_id=representation["session_id"],
    )
