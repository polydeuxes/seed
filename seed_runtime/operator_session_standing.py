"""Deterministic session-local Standing projection over preserved ingress events."""

from __future__ import annotations

from typing import Any

from seed_runtime.events import EventLedger

_SUBJECT_BY_KIND = {
    "operator.ingress.raw_material_captured": "raw_initial_material",
    "operator.ingress.ingress_occurred": "preserved_ingress",
    "operator.ingress.stopping_occurred": "interaction_closure",
}
_SUPPORTED_KINDS = {
    *_SUBJECT_BY_KIND,
    "operator.ingress.representation_examined",
}


def project_operator_session_standing(
    ledger: EventLedger, *, workspace_id: str, session_id: str
) -> dict[str, Any]:
    """Project bounded session-local Standing from already-recorded events.

    Consumes only ``operator.ingress.*`` events stamped with this exact
    workspace and session, in append order.  The result is fully recomputable
    from the ledger and is not itself recorded: it exposes only standings,
    limits, and Unknowns the session's events already carry.  An empty
    coordinate is absence of record, not negative standing and not Unknown.
    Meaning candidates are never produced here; each preserved ingress keeps
    the authority its own event recorded.
    """
    attempts: dict[str, dict[str, Any]] = {}
    preserved_ingress_occurrences: list[dict[str, Any]] = []
    interaction_closures: list[dict[str, Any]] = []
    known_loss: set[str] = set()
    unknowns: set[str] = set()
    conflicts: set[str] = set()
    as_of_event_id: str | None = None
    event_count = 0

    for event in ledger.list(workspace_id):
        if event.session_id != session_id:
            continue
        if not event.kind.startswith("operator.ingress."):
            continue
        if event.kind not in _SUPPORTED_KINDS:
            raise ValueError(f"unsupported operator-ingress event: {event.kind}")
        event_count += 1
        as_of_event_id = event.id
        attempt_ref = event.payload["attempt_ref"]
        attempt = attempts.setdefault(
            attempt_ref,
            {"event_ids": [], "preserved_ingress": None, "interaction_closure": None},
        )
        attempt["event_ids"].append(event.id)
        for key, collected in (
            ("known_loss", known_loss),
            ("unknowns", unknowns),
            ("conflicts", conflicts),
        ):
            collected.update(event.payload.get(key, ()))
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
        "attempts": attempts,
        "preserved_ingress_occurrences": preserved_ingress_occurrences,
        "interaction_closures": interaction_closures,
        # Exactly the relation standings recorded by session events.  No
        # current event kind records one, so this stays empty until a
        # responsible occurrence does; emptiness is absence of record only.
        "recorded_relation_standings": [],
        "known_loss": sorted(known_loss),
        "unknowns": sorted(unknowns),
        "conflicts": sorted(conflicts),
    }
