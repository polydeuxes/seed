"""Recorded Representation Acts and emission of their bounded results.

A Representation carries exact content from current session Standing.
It may also carry alternatives whose source relations remain separately
bounded.
"""

from __future__ import annotations

from typing import Any, TextIO

from seed_runtime.events import EventLedger
from seed_runtime.ids import new_id
from seed_runtime.yield_evidence import _record_yield_evidence, yield_commitment

REPRESENTATION_RECORDED_KIND = "operator.representation.recorded"
from seed_runtime.operator_ingress import SEED_ORIGIN

REPRESENTATION_EMISSION_ATTEMPTED_KIND = "operator.representation.emission_attempted"
REPRESENTATION_EMITTED_KIND = "operator.representation.emitted"
REPRESENTATION_EMISSION_OUTCOME_KIND = "operator.representation.emission_outcome_recorded"
REPRESENTATION_ACT_EVIDENCE_KIND = "operator.representation.act_evidenced"
REPRESENTATION_LOCALITY_EVIDENCE_KIND = (
    "operator.representation.locality_evidenced"
)
REPRESENTATION_CONVENTION = "operator_representation_v1"
REPRESENTATION_RESPONSIBILITY = (
    "yield one bounded Representation from the exact carried session coordinates"
)
REPRESENTATION_EMISSION_ACT_EVIDENCE_KIND = (
    "operator.representation.emission_act_evidenced"
)
REPRESENTATION_EMISSION_LOCALITY_EVIDENCE_KIND = (
    "operator.representation.emission_locality_evidenced"
)
REPRESENTATION_EMISSION_ATTEMPT_LOCALITY_EVIDENCE_KIND = (
    "operator.representation.emission_attempt_locality_evidenced"
)
REPRESENTATION_EMISSION_CONVENTION = "operator_representation_emission_v1"
REPRESENTATION_EMISSION_INPUT_ROLE = "exact bounded Representation"
REPRESENTATION_EMISSION_RESPONSIBILITY = (
    "write one exact rendered Representation to its declared text-stream boundary"
)

def _dimensions(
    *, identity, content, standing, source, responsibility, authority, scope, occurrence,
    evidence_scope=None,
):
    dimensions = {
        "identity": identity,
        "content": content,
        "standing": standing,
        "source_provenance": source,
        "responsibility": responsibility,
        "authority": authority,
        "scope_locality": scope,
        "occurrence_preservation": occurrence,
    }
    if evidence_scope is not None:
        dimensions["evidence_scope"] = evidence_scope
    return dimensions


def record_operator_representation(
    ledger: EventLedger,
    *,
    workspace_id: str,
    locality_id: str,
    locality_standing: dict[str, Any],
    alternative_sources: tuple[dict[str, Any], ...] = (),
) -> dict[str, Any]:
    """Record one exact bounded Representation and its exact Act occurrence.

    The Representation is bounded by the supplied projected session Standing.
    No alternatives are supplied by default; ``alternative_sources`` must be
    supplied by a caller with support for the eligibility and participation
    relations those alternatives carry.  Representation Act supplies no sources
    nor strengthens their standing, and no alternative's represented relation is derived
    from ingress material.  This module records what a Representation carries;
    it does not classify the resulting combination as a shape.

    Representation Act is not emission: the returned Representation carries no emission
    occurrence until :func:`emit_operator_representation` records one.
    """
    representation_id = new_id("operator_representation")
    representation_act_id = new_id("operator_representation_act")
    act_occurrence_id = new_id("operator_representation_act_occurrence")
    scope = f"workspace:{workspace_id};locality:{locality_id}"
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
                    "representation_result": source["representation_result_boundary"],
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
    representation_result = "bounded representation of current session Standing"
    content = "bounded Representation of current session Standing"
    occurrence = "Representation Act durably recorded"
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
        representation_result += " with bounded alternatives and preserved source roles"
        known_loss.append(
            "rendered label compresses represented candidate relation"
        )
    # The latest recorded exchange finding, exposed exactly as recorded;
    # representation Act neither strengthens nor reinterprets it.
    prior_exchange_finding = locality_standing.get("latest_exchange_finding")
    # The reconstructed source relation is exposed only when it belongs to the
    # exact latest finding's identification.
    represented_relation = None
    latest_relation = locality_standing.get("latest_represented_relation")
    if (
        prior_exchange_finding is not None
        and latest_relation is not None
        and latest_relation["identification_event_id"]
        == prior_exchange_finding["identification"]["event_id"]
    ):
        represented_relation = latest_relation
    result_payload = {
        "representation_ref": representation_id,
        "representation_act_id": representation_act_id,
        "act_occurrence_id": act_occurrence_id,
        "representation_result": representation_result,
        "alternatives": alternatives,
        "coordinate_bindings": coordinate_bindings,
        "locality_standing_as_of_event_id": locality_standing["as_of_event_id"],
        "prior_exchange_finding": prior_exchange_finding,
        "represented_relation": represented_relation,
        "known_loss": known_loss,
        "unknowns": [],
        "conflicts": [],
    }
    responsible_act_evidence = ledger.append(
        REPRESENTATION_ACT_EVIDENCE_KIND,
        workspace_id,
        {
            "representation_act_id": representation_act_id,
            "act_occurrence_id": act_occurrence_id,
            "act": "bounded Representation Act",
            "responsibility": REPRESENTATION_RESPONSIBILITY,
            "responsible_boundary": "this Seed",
            "result_commitment": yield_commitment(
                REPRESENTATION_CONVENTION, result_payload
            ),
            "standing": "occurred",
            "authority": "unestablished",
            "evidence_scope": (
                "Evidence concerning this exact Representation Act occurrence only"
            ),
        },
        locality_id=locality_id,
    )
    yield_evidence = _record_yield_evidence(
        ledger,
        workspace_id=workspace_id,
        locality_id=locality_id,
        convention=REPRESENTATION_CONVENTION,
        yielding_act="bounded Representation Act",
        act_occurrence_id=act_occurrence_id,
        yielded_result_kind="bounded Representation",
        result_identity=representation_id,
        yielded_content=result_payload,
        responsibility=REPRESENTATION_RESPONSIBILITY,
        live_boundary="representation_result",
        responsible_boundary="this Seed",
    )
    locality_evidence = ledger.append(
        REPRESENTATION_LOCALITY_EVIDENCE_KIND,
        workspace_id,
        {
            "act_occurrence_id": act_occurrence_id,
            "content_kind": "bounded Representation",
            "carried_content": result_payload,
            "standing": "carried",
            "authority": "unestablished",
            "evidence_scope": (
                "Evidence only for this exact Representation-to-occurrence Locality"
            ),
        },
        locality_id=locality_id,
    )
    representation_event = ledger.append(
        REPRESENTATION_RECORDED_KIND,
        workspace_id,
        {
            "attempt_ref": None,
            **result_payload,
            "dimensions": _dimensions(
                identity=act_occurrence_id,
                content=content,
                standing="recorded",
                source=locality_standing["as_of_event_id"],
                responsibility=REPRESENTATION_RESPONSIBILITY,
                authority="unestablished",
                evidence_scope=(
                    "representation Act occurrence only; establishes no Selection, "
                    "input support, or response treatment"
                ),
                scope=scope,
                occurrence=occurrence,
            ),
            "responsible_act_evidence_id": responsible_act_evidence.id,
            "yield_evidence_id": yield_evidence.id,
            "locality_evidence_id": locality_evidence.id,
            "mutates_cluster": False,
        },
        locality_id=locality_id,
    )
    return {
        "representation_id": representation_id,
        "representation_act_id": representation_act_id,
        "act_occurrence_id": act_occurrence_id,
        "workspace_id": workspace_id,
        "locality_id": locality_id,
        "representation_result": representation_result,
        "alternatives": alternatives,
        "coordinate_bindings": coordinate_bindings,
        "representation_event_id": representation_event.id,
        "emission_attempt_event_id": None,
        "emission_attempt_locality_evidence_id": None,
        "emission_outcome_event_id": None,
        "emitted_event_id": None,
        "locality_standing_as_of_event_id": locality_standing["as_of_event_id"],
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
    recorded representation payload.
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
    emission_act_id = new_id("operator_representation_emission_act")
    stream_encoding_metadata = getattr(output_stream, "encoding", None)
    if type(stream_encoding_metadata) is not str or not stream_encoding_metadata:
        stream_encoding_metadata = None
    scope = (
        f"workspace:{representation['workspace_id']};"
        f"locality:{representation['locality_id']}"
    )
    attempt_event = ledger.append(
        REPRESENTATION_EMISSION_ATTEMPTED_KIND,
        representation["workspace_id"],
        {
            "representation_ref": representation["representation_id"],
            "representation_event_id": representation["representation_event_id"],
            "emission_act_id": emission_act_id,
            "dimensions": _dimensions(
                identity=f"emission-attempt:{representation['representation_id']}",
                content="exact text prepared for the declared output boundary",
                standing="attempt recorded; output-boundary outcome Unknown",
                source=representation["representation_event_id"],
                responsibility=REPRESENTATION_EMISSION_RESPONSIBILITY,
                authority="unestablished",
                evidence_scope=(
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
            "provenance_occurrence_refs": [representation["representation_event_id"]],
            "mutates_cluster": False,
        },
        locality_id=representation["locality_id"],
    )
    representation["emission_attempt_event_id"] = attempt_event.id
    attempt_locality_evidence = ledger.append(
        REPRESENTATION_EMISSION_ATTEMPT_LOCALITY_EVIDENCE_KIND,
        representation["workspace_id"],
        {
            "representation_ref": representation["representation_id"],
            "attempt_event_id": attempt_event.id,
            "content_kind": "text",
            "carried_content": emitted_representation,
            "standing": "carried",
            "authority": "unestablished",
            "evidence_scope": (
                "Evidence only for the exact text-to-emission-attempt Locality"
            ),
        },
        locality_id=representation["locality_id"],
    )
    representation["emission_attempt_locality_evidence_id"] = (
        attempt_locality_evidence.id
    )

    # The attempt is durable before the output boundary sees anything. A
    # caller batching its appends is deferring commits, not this ordering:
    # an emission whose attempt was still uncommitted could reach the world
    # and leave no record that it was tried.
    ledger.flush()

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

    act_occurrence_id = new_id("operator_representation_emission_occurrence")
    boundary_result = {
        "boundary": "text_stream_write",
        "accepted_representation": emitted_representation,
        "accepted_representation_kind": "text",
        "accepted_length": written,
    }
    yielded_content = {"yielded_result": boundary_result}
    result_payload = {
        "emission_act_id": emission_act_id,
        "act_occurrence_id": act_occurrence_id,
        "representation_ref": representation["representation_id"],
        "representation_event_id": representation["representation_event_id"],
        "input_role": REPRESENTATION_EMISSION_INPUT_ROLE,
        "boundary_result": boundary_result,
        **yielded_content,
    }
    responsible_act_evidence = ledger.append(
        REPRESENTATION_EMISSION_ACT_EVIDENCE_KIND,
        representation["workspace_id"],
        {
            "emission_act_id": emission_act_id,
            "act_occurrence_id": act_occurrence_id,
            "act": "exact bounded Representation emission",
            "responsibility": REPRESENTATION_EMISSION_RESPONSIBILITY,
            "responsible_boundary": "this Seed",
            "representation_ref": representation["representation_id"],
            "representation_event_id": representation["representation_event_id"],
            "input_role": REPRESENTATION_EMISSION_INPUT_ROLE,
            "result_commitment": yield_commitment(
                REPRESENTATION_EMISSION_CONVENTION, yielded_content
            ),
            "standing": "occurred",
            "authority": "unestablished",
            "evidence_scope": (
                "Evidence concerning this exact emission Act occurrence and "
                "the Representation participating in its exact input role only"
            ),
        },
        locality_id=representation["locality_id"],
    )
    locality_evidence = ledger.append(
        REPRESENTATION_EMISSION_LOCALITY_EVIDENCE_KIND,
        representation["workspace_id"],
        {
            "act_occurrence_id": act_occurrence_id,
            "content_kind": "text",
            "carried_content": emitted_representation,
            "standing": "carried",
            "authority": "unestablished",
            "evidence_scope": (
                "Evidence only for the exact text-to-emission-occurrence Locality"
            ),
        },
        locality_id=representation["locality_id"],
    )
    yield_evidence = _record_yield_evidence(
        ledger,
        workspace_id=representation["workspace_id"],
        locality_id=representation["locality_id"],
        convention=REPRESENTATION_EMISSION_CONVENTION,
        yielding_act="exact bounded Representation emission",
        act_occurrence_id=act_occurrence_id,
        yielded_result_kind="text-stream boundary result",
        result_identity=f"emission-boundary-result:{act_occurrence_id}",
        yielded_content=yielded_content,
        responsibility=REPRESENTATION_EMISSION_RESPONSIBILITY,
        live_boundary="successful_emission",
        responsible_boundary="this Seed",
    )
    emitted_event = ledger.append(
        REPRESENTATION_EMITTED_KIND,
        representation["workspace_id"],
        {
            "attempt_ref": attempt_event.id,
            **result_payload,
            "dimensions": _dimensions(
                identity=act_occurrence_id,
                content="representation rendering written to console output stream",
                standing="emitted",
                source=representation["representation_event_id"],
                responsibility=REPRESENTATION_EMISSION_RESPONSIBILITY,
                authority="unestablished",
                evidence_scope=(
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
            "responsible_act_evidence_id": responsible_act_evidence.id,
            "locality_evidence_id": locality_evidence.id,
            "yield_evidence_id": yield_evidence.id,
            "known_loss": [],
            "unknowns": [],
            "conflicts": [],
            "provenance_occurrence_refs": [
                representation["representation_event_id"],
                attempt_event.id,
            ],
            "mutates_cluster": False,
        },
        locality_id=representation["locality_id"],
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
    unknowns = ["effects beyond the output boundary remain Unknown"]
    if phase == "text_stream_write" and reported_write_length is None:
        unknowns.insert(
            0,
            "output-boundary acceptance remains Unknown because write reported no length",
        )
    return ledger.append(
        REPRESENTATION_EMISSION_OUTCOME_KIND,
        representation["workspace_id"],
        {
            "attempt_ref": attempt_event_id,
            "representation_ref": representation["representation_id"],
            "representation_event_id": representation["representation_event_id"],
            "emitted_event_id": emitted_event_id,
            "dimensions": _dimensions(
                identity=f"emission-outcome:{attempt_event_id}:{phase}",
                content=f"{phase} did not complete the emission call",
                standing=outcome,
                source=attempt_event_id,
                responsibility=REPRESENTATION_EMISSION_RESPONSIBILITY,
                authority="unestablished",
                evidence_scope=(
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
            "unknowns": unknowns,
            "conflicts": [],
            "provenance_occurrence_refs": [
                representation["representation_event_id"],
                attempt_event_id,
                *([emitted_event_id] if emitted_event_id is not None else []),
            ],
            "mutates_cluster": False,
        },
        locality_id=representation["locality_id"],
    )
