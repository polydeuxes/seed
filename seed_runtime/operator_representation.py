"""Record and emit bounded Representations."""

from __future__ import annotations

from typing import Any, TextIO

from seed_runtime.events import CORRUPTED, EventLedger
from seed_runtime.identities import new_identity
from seed_runtime.yield_evidence import (
    _record_yield_evidence,
    read_yield_edge_requirements,
)

REPRESENTATION_RECORDED_KIND = "operator.representation.recorded"

REPRESENTATION_EMISSION_ATTEMPT_KIND = "operator.representation.emission_attempt_recorded"
REPRESENTATION_EMITTED_KIND = "operator.representation.emitted"
REPRESENTATION_EMISSION_OUTCOME_KIND = "operator.representation.emission_outcome_recorded"
REPRESENTATION_EMISSION_OUTCOME_ACT_EVIDENCE_KIND = (
    "operator.representation.emission_outcome_act_evidenced"
)
REPRESENTATION_ACT_EVIDENCE_KIND = "operator.representation.act_evidenced"
REPRESENTATION_LOCALITY_EVIDENCE_KIND = (
    "operator.representation.locality_evidenced"
)
REPRESENTATION_RESPONSIBILITY = (
    "yield one bounded Representation from the exact carried Locality coordinates"
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
REPRESENTATION_EMISSION_INPUT_ROLE = "exact bounded Representation"
REPRESENTATION_EMISSION_RESPONSIBILITY = (
    "write one exact Representation to its declared text-stream boundary"
)
REPRESENTATION_EMISSION_OUTCOME_RESULT_KIND = "Representation emission boundary result"
REPRESENTATION_EMISSION_OUTCOME_RESPONSIBILITY = (
    "preserve one exact failed Representation emission boundary call"
)
EVENT_KIND_RESPONSIBILITIES = {
    REPRESENTATION_RECORDED_KIND: "02.Acts.A",
    REPRESENTATION_EMISSION_ATTEMPT_KIND: "02.Acts.A",
    REPRESENTATION_EMITTED_KIND: "02.Acts.A",
    REPRESENTATION_ACT_EVIDENCE_KIND: "02.Acts.A",
    REPRESENTATION_LOCALITY_EVIDENCE_KIND: "06.Standing.B",
    REPRESENTATION_EMISSION_ACT_EVIDENCE_KIND: "02.Acts.A",
    REPRESENTATION_EMISSION_LOCALITY_EVIDENCE_KIND: "06.Standing.B",
    REPRESENTATION_EMISSION_ATTEMPT_LOCALITY_EVIDENCE_KIND: "06.Standing.B",
    REPRESENTATION_EMISSION_OUTCOME_KIND: "02.Acts.A",
    REPRESENTATION_EMISSION_OUTCOME_ACT_EVIDENCE_KIND: "02.Acts.A",
}

def _dimensions(
    *, identity, content, source, responsibility, authority, scope, occurrence,
    evidence_scope=None,
):
    dimensions = {
        "identity": identity,
        "content": content,
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
    locality_identity: str,
    locality_standing: dict[str, Any],
    alternative_sources: tuple[dict[str, Any], ...] = (),
) -> dict[str, Any]:
    """Record one exact bounded Representation and its Act occurrence."""
    representation_identity = new_identity("operator_representation")
    representation_act_identity = new_identity("operator_representation_act")
    act_occurrence_identity = new_identity("operator_representation_act_occurrence")
    scope = f"locality:{locality_identity}"
    alternative_material = []
    coordinate_binding: dict[str, str] = {}
    for position, source in enumerate(alternative_sources, start=1):
        alternative_identity = new_identity("represented_alternative")
        coordinate = str(position)
        alternative_material.append(
            {
                "alternative_identity": alternative_identity,
                "role": source["role"],
                "response_coordinate": coordinate,
                "label": source["label"],
                "represented_source": dict(source["represented_source"]),
                # Each A-to-G representation relation preserves its own
                # boundary; Representation-level coordinates do not transfer
                # to it by identity.
                "representation": {
                    "representation_result": source["representation_result_boundary"],
                    "scope": scope,
                    "provenance": source["represented_source"]["reference"],
                    "known_loss": [
                        "label compresses represented candidate "
                        "represented relation"
                    ],
                    "unknowns": [],
                    "conflicts": [],
                },
            }
        )
        coordinate_binding[coordinate] = alternative_identity
    representation_result = "bounded representation of current Locality Standing"
    content = "bounded Representation of current Locality Standing"
    occurrence = "Representation Act durably recorded"
    known_loss: list[str] = []
    if alternative_material:
        content = (
            "bounded Representation of current Locality Standing with "
            f"alternative material count {len(alternative_material)}"
        )
        occurrence = (
            f"alternative material count {len(alternative_material)}; roles, "
            "response-coordinate binding, and represented provenance occurrences "
            "durably recorded"
        )
        representation_result += " with bounded alternative material and preserved source roles"
        known_loss.append(
            "label compresses represented candidate relation"
        )
    result_material = {
        "representation_reference": representation_identity,
        "representation_act_identity": representation_act_identity,
        "act_occurrence_identity": act_occurrence_identity,
        "representation_result": representation_result,
        "alternative_material": alternative_material,
        "coordinate_binding": coordinate_binding,
        "locality_standing_as_of_event_identity": locality_standing["as_of_event_identity"],
        "known_loss": known_loss,
        "unknowns": [],
        "conflicts": [],
    }
    result_material["emission_text"] = _emission_text(result_material)
    responsible_act_evidence = ledger.append(
        REPRESENTATION_ACT_EVIDENCE_KIND,
        {
            "representation_act_identity": representation_act_identity,
            "act_occurrence_identity": act_occurrence_identity,
            "act": "bounded Representation Act",
            "responsibility": REPRESENTATION_RESPONSIBILITY,
            "responsible_boundary": "this Seed",
            "authority": "unestablished",
            "evidence_scope": (
                "Evidence for this exact Representation Act occurrence only"
            ),
        },
        locality_identity=locality_identity,
    )
    yield_evidence = _record_yield_evidence(
        ledger,
        locality_identity=locality_identity,
        exact_act="bounded Representation Act",
        act_occurrence_identity=act_occurrence_identity,
        result_kind="bounded Representation",
        result_identity=representation_identity,
        result_content=result_material,
        responsibility=REPRESENTATION_RESPONSIBILITY,
        live_boundary="representation_result",
        responsible_boundary="this Seed",
    )
    locality_evidence = ledger.append(
        REPRESENTATION_LOCALITY_EVIDENCE_KIND,
        {
            "act_occurrence_identity": act_occurrence_identity,
            "content_kind": "bounded Representation",
            "carried_content": result_material,
            "authority": "unestablished",
            "evidence_scope": (
                "Evidence only for this exact Representation-to-occurrence Locality"
            ),
        },
        locality_identity=locality_identity,
    )
    representation_event = ledger.append(
        REPRESENTATION_RECORDED_KIND,
        {
            "attempt_reference": None,
            **result_material,
            "dimensions": _dimensions(
                identity=act_occurrence_identity,
                content=content,
                source=locality_standing["as_of_event_identity"],
                responsibility=REPRESENTATION_RESPONSIBILITY,
                authority="unestablished",
                evidence_scope=(
                    "representation Act occurrence only; establishes no input "
                    "support or response treatment"
                ),
                scope=scope,
                occurrence=occurrence,
            ),
            "responsible_act_evidence_identity": responsible_act_evidence.identity,
            "yield_evidence_identity": yield_evidence.identity,
            "locality_evidence_identity": locality_evidence.identity,
        },
        locality_identity=locality_identity,
    )
    return {
        "representation_identity": representation_identity,
        "representation_act_identity": representation_act_identity,
        "act_occurrence_identity": act_occurrence_identity,
        "locality_identity": locality_identity,
        "representation_result": representation_result,
        "alternative_material": alternative_material,
        "coordinate_binding": coordinate_binding,
        "representation_event_identity": representation_event.identity,
        "emission_attempt_event_identity": None,
        "emission_attempt_locality_evidence_identity": None,
        "emission_outcome_event_identity": None,
        "emitted_event_identity": None,
        "locality_standing_as_of_event_identity": locality_standing["as_of_event_identity"],
        "emission_text": result_material["emission_text"],
        "known_loss": known_loss,
        "unknowns": [],
        "conflicts": [],
    }


def _emission_text(representation: dict[str, Any]) -> str:
    representation_identity = representation.get("representation_identity")
    if representation_identity is None:
        representation_identity = representation["representation_reference"]
    lines = [f"Bounded Representation {representation_identity}"]
    if representation["alternative_material"]:
        lines.append("Respond with exactly one token:")
    for alternative in representation["alternative_material"]:
        lines.append(
            f"  {alternative['response_coordinate']}. {alternative['label']}"
            f"  [{alternative['role']}]"
        )
    return "\n".join(lines) + "\n"


def read_operator_representation(
    ledger: EventLedger, representation_event_identity: str
) -> dict[str, Any]:
    event = ledger.get(representation_event_identity)
    if event is None or event.kind != REPRESENTATION_RECORDED_KIND:
        raise ValueError("the addressed occurrence is not a recorded Representation")
    material = event.material
    act_evidence = ledger.get(material.get("responsible_act_evidence_identity"))
    locality_evidence = ledger.get(material.get("locality_evidence_identity"))
    yield_evidence_identity = material.get("yield_evidence_identity")
    if (
        ledger.integrity_of(event.identity) == CORRUPTED
        or act_evidence is None
        or act_evidence.kind != REPRESENTATION_ACT_EVIDENCE_KIND
        or locality_evidence is None
        or locality_evidence.kind != REPRESENTATION_LOCALITY_EVIDENCE_KIND
        or ledger.integrity_of(locality_evidence.identity) == CORRUPTED
    ):
        raise ValueError("the recorded Representation Evidence is not exact")
    requirements = read_yield_edge_requirements(
        ledger,
        recorded_result_event_identity=event.identity,
        result_evidence_event_identity=yield_evidence_identity,
        responsible_act_evidence_event_identity=act_evidence.identity,
    )
    if not all(requirements.values()):
        raise ValueError("the recorded Representation Yield is not exact")
    exact_result = ledger.get(yield_evidence_identity).material.get("result")
    if (
        type(exact_result) is not dict
        or locality_evidence.material.get("carried_content") != exact_result
        or locality_evidence.material.get("act_occurrence_identity")
        != material.get("act_occurrence_identity")
        or act_evidence.material.get("act_occurrence_identity")
        != material.get("act_occurrence_identity")
        or act_evidence.material.get("representation_act_identity")
        != material.get("representation_act_identity")
        or event.locality_identity != locality_evidence.locality_identity
        or event.locality_identity != act_evidence.locality_identity
    ):
        raise ValueError("the recorded Representation coordinates are not exact")
    return {
        "representation_identity": material["representation_reference"],
        "representation_act_identity": material["representation_act_identity"],
        "act_occurrence_identity": material["act_occurrence_identity"],
        "locality_identity": event.locality_identity,
        "representation_result": material["representation_result"],
        "alternative_material": material["alternative_material"],
        "coordinate_binding": material["coordinate_binding"],
        "representation_event_identity": event.identity,
        "emission_text": material["emission_text"],
    }


def emit_operator_representation(
    ledger: EventLedger,
    *,
    representation: dict[str, Any],
    output_stream: TextIO,
) -> dict[str, Any]:
    """Write the Representation to the output stream and record the emission.

    Emission evidences only that the exact Representation was written to this boundary;
    effects beyond that output boundary require separate Evidence.
    """
    recorded = read_operator_representation(
        ledger, representation.get("representation_event_identity")
    )
    for coordinate in (
        "representation_identity",
        "representation_event_identity",
        "locality_identity",
        "emission_text",
    ):
        if representation.get(coordinate) != recorded[coordinate]:
            raise ValueError(
                "the supplied Representation disagrees with its recorded occurrence"
            )
    emitted_representation = recorded["emission_text"]
    emission_act_identity = new_identity("operator_representation_emission_act")
    scope = f"locality:{representation['locality_identity']}"
    attempt_event = ledger.append(
        REPRESENTATION_EMISSION_ATTEMPT_KIND,
        {
            "representation_reference": representation["representation_identity"],
            "representation_event_identity": representation["representation_event_identity"],
            "emission_act_identity": emission_act_identity,
            "dimensions": _dimensions(
                identity=f"emission-attempt:{representation['representation_identity']}",
                content="exact text prepared for the declared output boundary",
                source=representation["representation_event_identity"],
                responsibility=REPRESENTATION_EMISSION_RESPONSIBILITY,
                authority="unestablished",
                evidence_scope=(
                    "attempt occurrence only; establishes no output-boundary "
                    "acceptance or downstream effect"
                ),
                scope=scope,
                occurrence="emission attempt durably recorded before output",
            ),
            "representation": emitted_representation,
            "representation_kind": "text",
            "output_boundary": "text_stream_write",
            "known_loss": [],
            "unknowns": [
                "output-boundary acceptance remains Unknown until an outcome is recorded",
                "effects beyond the output boundary remain Unknown",
            ],
            "conflicts": [],
            "provenance_occurrence_references": [representation["representation_event_identity"]],
        },
        locality_identity=representation["locality_identity"],
    )
    representation["emission_attempt_event_identity"] = attempt_event.identity
    attempt_locality_evidence = ledger.append(
        REPRESENTATION_EMISSION_ATTEMPT_LOCALITY_EVIDENCE_KIND,
        {
            "representation_reference": representation["representation_identity"],
            "attempt_event_identity": attempt_event.identity,
            "content_kind": "text",
            "carried_content": emitted_representation,
            "authority": "unestablished",
            "evidence_scope": (
                "Evidence only for the exact text-to-emission-attempt Locality"
            ),
        },
        locality_identity=representation["locality_identity"],
    )
    representation["emission_attempt_locality_evidence_identity"] = (
        attempt_locality_evidence.identity
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
            attempt_event_identity=attempt_event.identity,
            scope=scope,
            boundary="text_stream_write",
            written=None,
            error=error,
        )
        representation["emission_outcome_event_identity"] = failed_event.identity
        raise

    if type(written) is not int or written != len(emitted_representation):
        failed_event = _record_emission_failure_outcome(
            ledger,
            representation=representation,
            attempt_event_identity=attempt_event.identity,
            scope=scope,
            boundary="text_stream_write",
            written=written,
            error=None,
        )
        representation["emission_outcome_event_identity"] = failed_event.identity
        raise ValueError("output boundary did not accept the exact representation")

    act_occurrence_identity = new_identity("operator_representation_emission_occurrence")
    locality_relation = {
        "first_subject": representation["representation_identity"],
        "second_subject": act_occurrence_identity,
        "relation_occurrence_identity": new_identity(
            "operator_representation_emission_locality_occurrence"
        ),
    }
    boundary_result = {
        "boundary": "text_stream_write",
        "accepted_representation": emitted_representation,
        "accepted_representation_kind": "text",
        "accepted_count": written,
    }
    result_content = {"result": boundary_result}
    result_material = {
        "emission_act_identity": emission_act_identity,
        "act_occurrence_identity": act_occurrence_identity,
        "representation_reference": representation["representation_identity"],
        "representation_event_identity": representation["representation_event_identity"],
        "input_role": REPRESENTATION_EMISSION_INPUT_ROLE,
        "locality_relation": locality_relation,
        "boundary_result": boundary_result,
        **result_content,
    }
    responsible_act_evidence = ledger.append(
        REPRESENTATION_EMISSION_ACT_EVIDENCE_KIND,
        {
            "emission_act_identity": emission_act_identity,
            "act_occurrence_identity": act_occurrence_identity,
            "act": "exact bounded Representation emission",
            "responsibility": REPRESENTATION_EMISSION_RESPONSIBILITY,
            "responsible_boundary": "this Seed",
            "representation_reference": representation["representation_identity"],
            "representation_event_identity": representation["representation_event_identity"],
            "input_role": REPRESENTATION_EMISSION_INPUT_ROLE,
            "authority": "unestablished",
            "evidence_scope": (
                "Evidence for this exact emission Act occurrence and "
                "the Representation participating in its exact input role only"
            ),
        },
        locality_identity=representation["locality_identity"],
    )
    locality_evidence = ledger.append(
        REPRESENTATION_EMISSION_LOCALITY_EVIDENCE_KIND,
        {
            "act_occurrence_identity": act_occurrence_identity,
            "representation_reference": representation["representation_identity"],
            "representation_event_identity": representation["representation_event_identity"],
            "locality_relation": locality_relation,
            "content_kind": "text",
            "carried_content": emitted_representation,
            "authority": "unestablished",
            "evidence_scope": (
                "Evidence only for the exact text-to-emission-occurrence Locality"
            ),
        },
        locality_identity=representation["locality_identity"],
    )
    yield_evidence = _record_yield_evidence(
        ledger,
        locality_identity=representation["locality_identity"],
        exact_act="exact bounded Representation emission",
        act_occurrence_identity=act_occurrence_identity,
        result_kind="text-stream boundary result",
        result_identity=f"emission-boundary-result:{act_occurrence_identity}",
        result_content=result_content,
        responsibility=REPRESENTATION_EMISSION_RESPONSIBILITY,
        live_boundary="successful_emission",
        responsible_boundary="this Seed",
    )
    emitted_event = ledger.append(
        REPRESENTATION_EMITTED_KIND,
        {
            "attempt_reference": attempt_event.identity,
            **result_material,
            "dimensions": _dimensions(
                identity=act_occurrence_identity,
                content="exact Representation written to console output stream",
                source=representation["representation_event_identity"],
                responsibility=REPRESENTATION_EMISSION_RESPONSIBILITY,
                authority="unestablished",
                evidence_scope=(
                    "emission occurrence only; effects beyond the output "
                    "boundary require separate Evidence"
                ),
                scope=scope,
                occurrence="emission occurrence durably recorded",
            ),
            "emitted_representation": emitted_representation,
            "emitted_representation_kind": "text",
            "output_boundary": "text_stream_write",
            "write_count": written,
            "responsible_act_evidence_identity": responsible_act_evidence.identity,
            "locality_evidence_identity": locality_evidence.identity,
            "yield_evidence_identity": yield_evidence.identity,
            "known_loss": [],
            "unknowns": [],
            "conflicts": [],
            "provenance_occurrence_references": [
                representation["representation_event_identity"],
                attempt_event.identity,
            ],
        },
        locality_identity=representation["locality_identity"],
    )
    representation["emission_outcome_event_identity"] = emitted_event.identity
    representation["emitted_event_identity"] = emitted_event.identity
    try:
        output_stream.flush()
    except Exception as error:
        failed_event = _record_emission_failure_outcome(
            ledger,
            representation=representation,
            attempt_event_identity=attempt_event.identity,
            scope=scope,
            boundary="text_stream_flush",
            written=written,
            error=error,
            emitted_event_identity=emitted_event.identity,
        )
        representation["emission_outcome_event_identity"] = failed_event.identity
        raise
    return representation


def _record_emission_failure_outcome(
    ledger: EventLedger,
    *,
    representation: dict[str, Any],
    attempt_event_identity: str,
    scope: str,
    boundary: str,
    written: Any,
    error: Exception | None,
    emitted_event_identity: str | None = None,
):
    """Preserve the bounded failure without inferring downstream state."""
    if type(written) is int and written >= 0:
        write_count: int | None = written
    else:
        write_count = None
    unknowns = ["effects beyond the output boundary remain Unknown"]
    if boundary == "text_stream_write" and write_count is None:
        unknowns.insert(
            0,
            "output-boundary acceptance remains Unknown because write reported no count",
        )
    act_identity = new_identity("operator_representation_emission_outcome_act")
    act_occurrence_identity = new_identity(
        "operator_representation_emission_outcome_act_occurrence"
    )
    result_identity = new_identity("operator_representation_emission_outcome_result")
    result_material = {
            "result_identity": result_identity,
            "downstream_act_identity": act_identity,
            "act_occurrence_identity": act_occurrence_identity,
            "attempt_reference": attempt_event_identity,
            "representation_reference": representation["representation_identity"],
            "representation_event_identity": representation["representation_event_identity"],
            "emitted_event_identity": emitted_event_identity,
            "dimensions": _dimensions(
                identity=f"emission-outcome:{attempt_event_identity}:{boundary}",
                content=f"{boundary} did not complete the emission call",
                source=attempt_event_identity,
                responsibility=REPRESENTATION_EMISSION_RESPONSIBILITY,
                authority="unestablished",
                evidence_scope=(
                    "failure occurrence only; establishes no downstream effect "
                    "and no acceptance beyond the reported write result"
                ),
                scope=scope,
                occurrence="emission failure durably recorded",
            ),
            "boundary": boundary,
            "write_count": write_count,
            "error": repr(error) if error is not None else None,
            "known_loss": [],
            "unknowns": unknowns,
            "conflicts": [],
            "provenance_occurrence_references": [
                representation["representation_event_identity"],
                attempt_event_identity,
                *([emitted_event_identity] if emitted_event_identity is not None else []),
            ],
        }
    act_evidence = ledger.append(
        REPRESENTATION_EMISSION_OUTCOME_ACT_EVIDENCE_KIND,
        {
            "downstream_act_identity": act_identity,
            "act_occurrence_identity": act_occurrence_identity,
            "act": "failed Representation emission boundary call",
            "responsibility": REPRESENTATION_EMISSION_OUTCOME_RESPONSIBILITY,
            "responsible_boundary": "this Seed",
            "authority": "unestablished",
            "evidence_scope": (
                "this exact failed Representation emission boundary call only"
            ),
        },
        locality_identity=representation["locality_identity"],
    )
    yield_evidence = _record_yield_evidence(
        ledger,
        locality_identity=representation["locality_identity"],
        exact_act="failed Representation emission boundary call",
        act_occurrence_identity=act_occurrence_identity,
        result_kind=REPRESENTATION_EMISSION_OUTCOME_RESULT_KIND,
        result_identity=result_identity,
        result_content=result_material,
        responsibility=REPRESENTATION_EMISSION_OUTCOME_RESPONSIBILITY,
        live_boundary="failed_emission_outcome",
        responsible_boundary="this Seed",
        recorded_result_coordinates={key: (key,) for key in result_material},
    )
    return ledger.append(
        REPRESENTATION_EMISSION_OUTCOME_KIND,
        {
            **result_material,
            "responsible_act_evidence_identity": act_evidence.identity,
            "yield_evidence_identity": yield_evidence.identity,
        },
        locality_identity=representation["locality_identity"],
    )
