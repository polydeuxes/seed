"""Deterministic session-local Standing projection over preserved ingress events."""

from __future__ import annotations

from typing import Any

from seed_runtime.events import EventLedger

_SUBJECT_BY_KIND = {
    "operator.ingress.raw_material_captured": "raw_initial_material",
    "operator.ingress.ingress_occurred": "preserved_ingress",
    "operator.ingress.stopping_occurred": "interaction_closure",
}
_PRESENTATION_FORMED_KIND = "operator.presentation.formed"
_PRESENTATION_EMITTED_KIND = "operator.presentation.emitted"
_COMPARISON_KIND = "operator.exchange.comparison_occurred"
_IDENTIFICATION_KIND = "operator.exchange.identification_occurred"
_SUPPORTED_KINDS = {
    *_SUBJECT_BY_KIND,
    "operator.ingress.representation_examined",
    _PRESENTATION_FORMED_KIND,
    _PRESENTATION_EMITTED_KIND,
    _COMPARISON_KIND,
    _IDENTIFICATION_KIND,
}


def project_operator_session_standing(
    ledger: EventLedger, *, workspace_id: str, session_id: str
) -> dict[str, Any]:
    """Project bounded session-local Standing from already-recorded events.

    Consumes only ``operator.ingress.*`` and ``operator.presentation.*``
    events stamped with this exact workspace and session, in append order.  The result is fully recomputable
    from the ledger and is not itself recorded: it exposes only standings,
    limits, and Unknowns the session's events already carry.  An empty
    coordinate is absence of record, not negative standing and not Unknown.
    Meaning candidates are never produced here; each preserved ingress keeps
    the authority its own event recorded.
    """
    attempts: dict[str, dict[str, Any]] = {}
    preserved_ingress_occurrences: list[dict[str, Any]] = []
    interaction_closures: list[dict[str, Any]] = []
    presentations: dict[str, dict[str, Any]] = {}
    current_presentation_id: str | None = None
    comparisons: dict[str, dict[str, Any]] = {}
    identifications: dict[str, dict[str, Any]] = {}
    latest_exchange_finding: dict[str, Any] | None = None
    known_loss: set[str] = set()
    unknowns: set[str] = set()
    conflicts: set[str] = set()
    as_of_event_id: str | None = None
    consumed_event_ids: list[str] = []
    event_count = 0

    for event in ledger.list(workspace_id):
        if event.session_id != session_id:
            continue
        if not (
            event.kind.startswith("operator.ingress.")
            or event.kind.startswith("operator.presentation.")
            or event.kind.startswith("operator.exchange.")
        ):
            continue
        if event.kind not in _SUPPORTED_KINDS:
            raise ValueError(f"unsupported operator-ingress event: {event.kind}")
        event_count += 1
        as_of_event_id = event.id
        consumed_event_ids.append(event.id)
        for key, collected in (
            ("known_loss", known_loss),
            ("unknowns", unknowns),
            ("conflicts", conflicts),
        ):
            collected.update(event.payload.get(key, ()))
        if event.kind == _PRESENTATION_FORMED_KIND:
            payload = event.payload
            presentations[payload["presentation_ref"]] = {
                "presentation_id": payload["presentation_ref"],
                "formed_event_id": event.id,
                "emitted_event_id": None,
                "purpose": payload["purpose"],
                "alternatives": payload["alternatives"],
                "coordinate_bindings": payload["coordinate_bindings"],
                "session_standing_as_of_event_id": payload[
                    "session_standing_as_of_event_id"
                ],
                "session_standing_evidence_ids": payload[
                    "session_standing_evidence_ids"
                ],
                "prior_exchange_finding": payload.get("prior_exchange_finding"),
                "scope": payload["dimensions"]["scope_locality"],
                "provenance": payload["dimensions"]["source_provenance"],
                "known_loss": payload["known_loss"],
                "unknowns": payload["unknowns"],
                "conflicts": payload["conflicts"],
            }
            continue
        if event.kind == _PRESENTATION_EMITTED_KIND:
            presentation_ref = event.payload["presentation_ref"]
            if presentation_ref not in presentations:
                raise ValueError(
                    "presentation emission without recorded formation: "
                    f"{presentation_ref}"
                )
            presentations[presentation_ref]["emitted_event_id"] = event.id
            current_presentation_id = presentation_ref
            continue
        if event.kind == _COMPARISON_KIND:
            payload = event.payload
            comparisons[payload["comparison_ref"]] = {
                "comparison_ref": payload["comparison_ref"],
                "event_id": event.id,
                "presentation_ref": payload["presentation_ref"],
                "response_attempt_ref": payload["response_attempt_ref"],
                "compared_representation": payload["compared_representation"],
                "coordinate_set": payload["coordinate_set"],
                "matched_coordinate": payload["matched_coordinate"],
                "outcome": payload["outcome"],
                "unknowns": payload["unknowns"],
            }
            continue
        if event.kind == _IDENTIFICATION_KIND:
            payload = event.payload
            identification = {
                "identification_ref": payload["identification_ref"],
                "event_id": event.id,
                "comparison_ref": payload["comparison_ref"],
                "comparison_event_id": payload["comparison_event_id"],
                "presentation_ref": payload["presentation_ref"],
                "response_attempt_ref": payload["response_attempt_ref"],
                "identified_alternative": payload["identified_alternative"],
                "basis": payload["basis"],
                "outcome": payload["outcome"],
            }
            identifications[payload["identification_ref"]] = identification
            comparison = comparisons.get(payload["comparison_ref"])
            if comparison is None:
                raise ValueError(
                    "identification without recorded comparison: "
                    f"{payload['comparison_ref']}"
                )
            # The most recent complete exchange finding, exactly as recorded.
            latest_exchange_finding = {
                "comparison": comparison,
                "identification": identification,
            }
            continue
        attempt_ref = event.payload["attempt_ref"]
        attempt = attempts.setdefault(
            attempt_ref,
            {"event_ids": [], "preserved_ingress": None, "interaction_closure": None},
        )
        attempt["event_ids"].append(event.id)
        if event.kind == "operator.ingress.ingress_occurred":
            occurrence = {
                "attempt_ref": attempt_ref,
                "subject_ref": event.payload["dimensions"]["identity"],
                "standing": "preserved",
                "authority_warrant": event.payload["dimensions"]["authority_warrant"],
                "evidence_event_id": event.id,
            }
            attempt["preserved_ingress"] = occurrence
            preserved_ingress_occurrences.append(occurrence)
        elif event.kind == "operator.ingress.stopping_occurred":
            closure = {
                "attempt_ref": attempt_ref,
                "response_kind": event.payload.get("response_kind"),
                "evidence_event_id": event.id,
            }
            attempt["interaction_closure"] = closure
            interaction_closures.append(closure)

    return {
        "workspace_id": workspace_id,
        "session_id": session_id,
        "as_of_event_id": as_of_event_id,
        "event_count": event_count,
        # Exact append-order inventory of every session event this
        # projection consumed, including Presentation formation and
        # emission Evidence.
        "consumed_event_ids": consumed_event_ids,
        "attempts": attempts,
        "preserved_ingress_occurrences": preserved_ingress_occurrences,
        "interaction_closures": interaction_closures,
        "presentations": presentations,
        # The most recently emitted Presentation, complete with alternatives
        # and bindings, so a later occurrence can consume its exact
        # coordinates.  None means no emission is recorded in this session.
        "current_presentation": (
            presentations[current_presentation_id]
            if current_presentation_id is not None
            else None
        ),
        # Exactly the relation standings recorded by session events.  No
        # current event kind records one, so this stays empty until a
        # responsible occurrence does; emptiness is absence of record only.
        "comparisons": comparisons,
        "identifications": identifications,
        "latest_exchange_finding": latest_exchange_finding,
        "recorded_relation_standings": [],
        "known_loss": sorted(known_loss),
        "unknowns": sorted(unknowns),
        "conflicts": sorted(conflicts),
    }
