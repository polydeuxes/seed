"""Recorded represented-source recovery and attributed meaning-relation consumption."""

from __future__ import annotations

from typing import Any

from seed_runtime.events import EventLedger
from seed_runtime.ids import new_id

SOURCE_RECOVERED_KIND = "operator.presentation.source_recovered"
MEANING_RELATION_KIND = "operator.presentation.meaning_relation_established"

# Unknowns the Book positively establishes at this exact position; Operator
# Authority for the proposition is carried separately as unresolved prose in
# the queryable authority separation, never as a runtime branch value.
_RELATION_UNKNOWNS = (
    "operator intent Unknown",
    "operator selection occurrence Unknown",
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


def _require(condition: bool, failure: str) -> None:
    if not condition:
        raise ValueError(f"source recovery preconditions unmet: {failure}")


def _validated_event(ledger, event_id, kind, workspace_id, session_id, name):
    event = ledger.get(event_id) if event_id is not None else None
    _require(event is not None, f"{name} event not recorded")
    _require(event.kind == kind, f"{name} evidence is not a {kind} event")
    _require(
        event.workspace_id == workspace_id and event.session_id == session_id,
        f"{name} event belongs to another workspace or session",
    )
    return event


def run_operator_source_recovery_and_meaning_relation(
    ledger: EventLedger,
    *,
    workspace_id: str,
    session_id: str,
    identification_event_id: str,
) -> dict[str, Any]:
    """Recover the exact represented source for the identified alternative,
    then consume its attributed developer-supplied meaning testimony, as two
    distinct recorded results of one responsible occurrence.

    Everything consumed comes from recorded testimony: the identification
    result, its comparison, and the enclosing Presentation formation payload
    -- which is the Evidence that exact C formed exact alternative A
    representing exact source identity G with attributed meaning M.  Each
    alternative's empty upstream ``representation.evidence_event_ids`` means
    only that no separately recorded developer-source event exists; it is
    not reinterpreted, and no such event is synthesized.

    Recovery establishes represented-source identity through preserved
    lineage only.  The meaning relation consumes attributed testimony; it
    derives nothing from operator ingress, response text, rendered labels,
    recurrence, or lexical similarity, and establishes no operator intent,
    selection, authorization, goal Standing, or treatment.
    """
    scope = f"workspace:{workspace_id};session:{session_id}"
    identification_event = _validated_event(
        ledger,
        identification_event_id,
        "operator.exchange.identification_occurred",
        workspace_id,
        session_id,
        "identification",
    )
    identified = identification_event.payload["identified_alternative"]
    _require(
        identification_event.payload["basis"] == "identified"
        and identified is not None,
        "identification did not identify a presented alternative",
    )
    comparison_event = _validated_event(
        ledger,
        identification_event.payload["comparison_event_id"],
        "operator.exchange.comparison_occurred",
        workspace_id,
        session_id,
        "comparison",
    )
    presentation_ref = identification_event.payload["presentation_ref"]
    _require(
        comparison_event.payload["presentation_ref"] == presentation_ref,
        "comparison and identification concern different presentations",
    )
    response_attempt_ref = identification_event.payload["response_attempt_ref"]
    _require(
        comparison_event.payload["response_attempt_ref"] == response_attempt_ref,
        "comparison and identification concern different attempts",
    )
    _require(
        comparison_event.payload["comparison_ref"]
        == identification_event.payload["comparison_ref"],
        "identification does not consume this exact comparison",
    )
    matched_coordinate = comparison_event.payload["matched_coordinate"]
    _require(
        matched_coordinate is not None,
        "comparison recorded no coordinate match",
    )
    formed_event = _validated_event(
        ledger,
        identification_event.payload["presentation_formed_event_id"],
        "operator.presentation.formed",
        workspace_id,
        session_id,
        "formation",
    )
    _require(
        formed_event.payload["presentation_ref"] == presentation_ref,
        "formation event does not record this exact presentation",
    )
    _require(
        comparison_event.payload["presentation_formed_event_id"] == formed_event.id,
        "comparison does not record this exact formation occurrence",
    )
    emitted_event = _validated_event(
        ledger,
        comparison_event.payload["presentation_emitted_event_id"],
        "operator.presentation.emitted",
        workspace_id,
        session_id,
        "emission",
    )
    _require(
        emitted_event.payload["presentation_ref"] == presentation_ref
        and emitted_event.payload["formed_event_id"] == formed_event.id,
        "emission event does not record this exact presentation chain",
    )
    response_ingress_event_id = comparison_event.payload["response_ingress_event_id"]
    response_capture_event_id = comparison_event.payload["response_capture_event_id"]
    ingress_event = _validated_event(
        ledger,
        response_ingress_event_id,
        "operator.ingress.ingress_occurred",
        workspace_id,
        session_id,
        "response ingress",
    )
    capture_event = _validated_event(
        ledger,
        response_capture_event_id,
        "operator.ingress.raw_material_captured",
        workspace_id,
        session_id,
        "response capture",
    )
    _require(
        ingress_event.payload["attempt_ref"] == response_attempt_ref,
        "ingress and comparison concern different attempts",
    )
    _require(
        ingress_event.payload["raw_material_event_id"] == capture_event.id,
        "ingress does not record this exact capture occurrence",
    )
    _require(
        capture_event.payload["attempt_ref"] == response_attempt_ref,
        "capture and ingress belong to different attempts",
    )
    _require(
        ingress_event.payload.get("produced_after_presentation_ref")
        == presentation_ref
        and ingress_event.payload.get("produced_after_presentation_formed_event_id")
        == formed_event.id
        and ingress_event.payload.get("produced_after_presentation_emitted_event_id")
        == emitted_event.id,
        "ingress does not record production after this exact presentation chain",
    )
    _require(
        comparison_event.payload["compared_representation"]
        == ingress_event.payload["dimensions"]["content"],
        "comparison did not consume the recorded ingress representation",
    )

    # The recorded formation payload is the sole source of the exact A -> G
    # representation relation; the identification's carried alternative must
    # agree with it on every shared coordinate.
    alternatives_by_id = {
        alternative["alternative_id"]: alternative
        for alternative in formed_event.payload["alternatives"]
    }
    recorded_alternative = alternatives_by_id.get(identified["alternative_id"])
    _require(
        recorded_alternative is not None,
        "identified alternative does not belong to the recorded presentation",
    )
    for key in ("role", "response_coordinate", "rendered_label"):
        _require(
            recorded_alternative[key] == identified[key],
            f"identified alternative disagrees with recorded {key}",
        )
    _require(
        recorded_alternative["response_coordinate"] == matched_coordinate,
        "matched coordinate does not belong to the identified alternative",
    )
    _require(
        formed_event.payload["coordinate_bindings"].get(matched_coordinate)
        == recorded_alternative["alternative_id"],
        "recorded binding does not bind the matched coordinate to this "
        "alternative",
    )
    represented_source = recorded_alternative["represented_source"]
    _require(
        bool(represented_source.get("identity")),
        "recorded alternative carries no exact represented-source identity",
    )
    _require(
        represented_source.get("attribution") == "developer-supplied",
        "represented source is not attributed developer-supplied testimony",
    )
    _require(
        bool(represented_source.get("meaning")),
        "formation records no attributed meaning testimony for this source",
    )
    representation = recorded_alternative["representation"]

    recovery_ref = new_id("operator_source_recovery")
    recovery_event = ledger.append(
        SOURCE_RECOVERED_KIND,
        workspace_id,
        {
            "attempt_ref": response_attempt_ref,
            "recovery_ref": recovery_ref,
            "presentation_ref": presentation_ref,
            "presentation_formed_event_id": formed_event.id,
            "presentation_emitted_event_id": emitted_event.id,
            "comparison_event_id": comparison_event.id,
            "identification_event_id": identification_event.id,
            "response_attempt_ref": response_attempt_ref,
            "response_ingress_event_id": response_ingress_event_id,
            "response_capture_event_id": response_capture_event_id,
            "alternative": {
                "alternative_id": recorded_alternative["alternative_id"],
                "role": recorded_alternative["role"],
                "response_coordinate": recorded_alternative["response_coordinate"],
            },
            # Source identity only: recovery does not carry the meaning, so
            # recovered identity cannot masquerade as established meaning.
            "source": {
                "identity": represented_source["identity"],
                "kind": represented_source["kind"],
                "attribution": represented_source["attribution"],
                "reference": represented_source["reference"],
            },
            "representation": dict(representation),
            "purpose": (
                "recover the exact represented source for the identified "
                "alternative within the exact presentation"
            ),
            "dimensions": _dimensions(
                identity=recovery_ref,
                content=f"source recovered: {represented_source['identity']}",
                standing="source-recovered",
                source=identification_event.id,
                responsibility="bounded-represented-source-recovery",
                authority=(
                    "recovers represented-source identity through preserved "
                    "representation lineage only; establishes no meaning, "
                    "intent, selection, authorization, goal, or treatment"
                ),
                scope=f"{scope};exchange:{presentation_ref}->{response_attempt_ref}",
                occurrence="source-recovery occurrence durably recorded",
            ),
            "known_loss": list(representation["known_loss"]),
            "unknowns": [],
            "conflicts": [],
            "lineage": [
                formed_event.id,
                emitted_event.id,
                capture_event.id,
                ingress_event.id,
                comparison_event.id,
                identification_event.id,
            ],
            "mutates_cluster": False,
        },
        session_id=session_id,
    )

    relation_ref = new_id("operator_meaning_relation")
    proposition = represented_source["meaning"]
    relation_event = ledger.append(
        MEANING_RELATION_KIND,
        workspace_id,
        {
            "attempt_ref": response_attempt_ref,
            "relation_ref": relation_ref,
            "source_recovery_event_id": recovery_event.id,
            "recovery_ref": recovery_ref,
            "presentation_ref": presentation_ref,
            "presentation_formed_event_id": formed_event.id,
            "comparison_event_id": comparison_event.id,
            "identification_event_id": identification_event.id,
            "alternative_id": recorded_alternative["alternative_id"],
            "source_identity": represented_source["identity"],
            "proposition": proposition,
            "source_attribution": represented_source["attribution"],
            "source_reference": represented_source["reference"],
            "representation_purpose": representation["purpose"],
            "representation_scope": representation["scope"],
            "warrant_basis": (
                "attributed developer-supplied meaning testimony preserved "
                "by the recorded formation occurrence"
            ),
            # Structural four-way separation: standing, supported claims,
            # Evidence, and Scope are coordinates, with testimony alongside
            # rather than as the only representation.
            "authority_separation": {
                "source_authority": {
                    "standing": "bounded",
                    "supports": ["source-supplied-with-attributed-meaning"],
                    "evidence_event_ids": [formed_event.id],
                    "scope": {
                        "source_identity": represented_source["identity"],
                        "proposition": proposition,
                    },
                    "testimony": (
                        "authoritative only that this source was supplied "
                        "with this attributed meaning"
                    ),
                },
                "response_comparison_authority": {
                    "standing": "bounded",
                    "supports": ["response-matched-coordinate-within-presentation"],
                    "evidence_event_ids": [comparison_event.id],
                    "scope": {
                        "presentation_ref": presentation_ref,
                        "response_attempt_ref": response_attempt_ref,
                    },
                    "testimony": (
                        "bounds only the recorded match or no-match within "
                        "the exact presentation"
                    ),
                },
                "meaning_warrant": {
                    "standing": "established",
                    "supports": ["source-expresses-proposition"],
                    "evidence_event_ids": [formed_event.id, recovery_event.id],
                    "scope": {
                        "source_identity": represented_source["identity"],
                        "proposition": proposition,
                    },
                    "testimony": (
                        "preserved attributed testimony plus the recovered "
                        "exact source support the bounded relation that the "
                        "source expresses the proposition"
                    ),
                },
                "operator_authority": {
                    "standing": "unresolved",
                    "supports": [],
                    "evidence_event_ids": [],
                    "scope": {"proposition": proposition},
                    "testimony": (
                        "unresolved for this proposition; not established by "
                        "production, match, identification, or this relation"
                    ),
                },
            },
            "purpose": (
                "consume attributed developer-supplied meaning testimony for "
                "the recovered source"
            ),
            "dimensions": _dimensions(
                identity=relation_ref,
                content=(
                    f"{represented_source['identity']} expresses the "
                    "attributed proposition"
                ),
                standing="meaning-relation-established",
                source=recovery_event.id,
                responsibility="bounded-meaning-relation-consumption",
                authority=(
                    "bounded to: the recovered source expresses its attributed "
                    "developer-supplied proposition; establishes no operator "
                    "intent, selection, authorization, goal standing, or "
                    "treatment"
                ),
                scope=f"{scope};exchange:{presentation_ref}->{response_attempt_ref}",
                occurrence="meaning-relation occurrence durably recorded",
            ),
            "known_loss": [],
            "unknowns": list(_RELATION_UNKNOWNS),
            "conflicts": [],
            "lineage": [
                recovery_event.id,
                formed_event.id,
                identification_event.id,
            ],
            "mutates_cluster": False,
        },
        session_id=session_id,
    )
    return {
        "source_recovery": {
            "recovery_ref": recovery_ref,
            "event_id": recovery_event.id,
            "source_identity": represented_source["identity"],
            "alternative_id": recorded_alternative["alternative_id"],
        },
        "meaning_relation": {
            "relation_ref": relation_ref,
            "event_id": relation_event.id,
            "source_identity": represented_source["identity"],
            "proposition": proposition,
        },
    }
