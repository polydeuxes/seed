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
_SOURCE_RECOVERED_KIND = "operator.presentation.source_recovered"
_MEANING_RELATION_KIND = "operator.presentation.meaning_relation_established"
_SUPPORTED_KINDS = {
    *_SUBJECT_BY_KIND,
    "operator.ingress.representation_examined",
    _PRESENTATION_FORMED_KIND,
    _PRESENTATION_EMITTED_KIND,
    _COMPARISON_KIND,
    _IDENTIFICATION_KIND,
    _SOURCE_RECOVERED_KIND,
    _MEANING_RELATION_KIND,
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
    source_recoveries: dict[str, dict[str, Any]] = {}
    meaning_relations: dict[str, dict[str, Any]] = {}
    latest_source_recovery: dict[str, Any] | None = None
    latest_meaning_relation: dict[str, Any] | None = None
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
            if (
                event.payload["formed_event_id"]
                != presentations[presentation_ref]["formed_event_id"]
            ):
                raise ValueError(
                    "presentation emission does not name its recorded "
                    "formation occurrence"
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
                "response_ingress_event_id": payload["response_ingress_event_id"],
                "response_capture_event_id": payload["response_capture_event_id"],
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
            # The joined pair must agree on every shared coordinate; a
            # mismatched pair is structurally refused rather than composed.
            for identification_key, comparison_key in (
                ("comparison_event_id", "event_id"),
                ("presentation_ref", "presentation_ref"),
                ("response_attempt_ref", "response_attempt_ref"),
            ):
                if (
                    identification[identification_key]
                    != comparison[comparison_key]
                ):
                    raise ValueError(
                        "identification does not agree with its recorded "
                        f"comparison on {identification_key}"
                    )
            # An identified result must follow from the comparison finding
            # and the recorded binding; a forged basis is refused here.
            if identification["basis"] == "identified":
                identified_alternative = identification["identified_alternative"]
                matched = comparison["matched_coordinate"]
                identification_presentation = presentations.get(
                    identification["presentation_ref"]
                )
                if identification_presentation is None:
                    raise ValueError(
                        "identification names an unrecorded presentation: "
                        f"{identification['presentation_ref']}"
                    )
                if (
                    identified_alternative is None
                    or matched is None
                    or comparison["outcome"] != f"match:{matched}"
                    or identified_alternative["response_coordinate"] != matched
                    or identification_presentation["coordinate_bindings"].get(
                        matched
                    )
                    != identified_alternative["alternative_id"]
                ):
                    raise ValueError(
                        "identified result does not follow from its recorded "
                        "comparison finding and binding"
                    )
            elif identification["basis"] == "no-coordinate-match":
                if comparison["matched_coordinate"] is not None:
                    raise ValueError(
                        "no-coordinate-match identification contradicts a "
                        "recorded match"
                    )
            # The most recent complete exchange finding, exactly as recorded.
            latest_exchange_finding = {
                "comparison": comparison,
                "identification": identification,
            }
            continue
        if event.kind == _SOURCE_RECOVERED_KIND:
            payload = event.payload
            # A recovery is admitted into Standing only where the recorded
            # formation testimony and the recorded identification agree with
            # every coordinate it carries.
            presentation = presentations.get(payload["presentation_ref"])
            if presentation is None:
                raise ValueError(
                    "source recovery names an unrecorded presentation: "
                    f"{payload['presentation_ref']}"
                )
            recorded_alternative = next(
                (
                    alternative
                    for alternative in presentation["alternatives"]
                    if alternative["alternative_id"]
                    == payload["alternative"]["alternative_id"]
                ),
                None,
            )
            if recorded_alternative is None:
                raise ValueError(
                    "source recovery names an alternative outside its "
                    "recorded presentation"
                )
            recorded_source = recorded_alternative["represented_source"]
            for key in ("identity", "kind", "attribution", "reference"):
                if payload["source"][key] != recorded_source[key]:
                    raise ValueError(
                        "source recovery does not agree with recorded "
                        f"formation testimony on source {key}"
                    )
            for key in ("role", "response_coordinate"):
                if payload["alternative"][key] != recorded_alternative[key]:
                    raise ValueError(
                        "source recovery does not agree with recorded "
                        f"formation testimony on alternative {key}"
                    )
            if (
                payload["presentation_formed_event_id"]
                != presentation["formed_event_id"]
                or payload["presentation_emitted_event_id"]
                != presentation["emitted_event_id"]
            ):
                raise ValueError(
                    "source recovery does not carry the recorded "
                    "presentation occurrence lineage"
                )
            supporting_identification = next(
                (
                    identification
                    for identification in identifications.values()
                    if identification["event_id"]
                    == payload["identification_event_id"]
                ),
                None,
            )
            if supporting_identification is None or (
                supporting_identification["presentation_ref"]
                != payload["presentation_ref"]
                or supporting_identification["basis"] != "identified"
                or supporting_identification["outcome"]
                != "alternative-identified"
                or supporting_identification["identified_alternative"] is None
                or supporting_identification["identified_alternative"][
                    "alternative_id"
                ]
                != payload["alternative"]["alternative_id"]
                or supporting_identification["comparison_event_id"]
                != payload["comparison_event_id"]
                or supporting_identification["response_attempt_ref"]
                != payload["response_attempt_ref"]
            ):
                raise ValueError(
                    "source recovery does not agree with its recorded "
                    "identification"
                )
            # Re-prove Compare -> Identification -> A from the recorded
            # comparison: a match to the identified alternative's own
            # coordinate, bound to its identity by the recorded binding.
            supporting_comparison = comparisons.get(
                supporting_identification["comparison_ref"]
            )
            if supporting_comparison is None:
                raise ValueError(
                    "source recovery's identification has no recorded "
                    "comparison"
                )
            matched = supporting_comparison["matched_coordinate"]
            if (
                matched is None
                or supporting_comparison["outcome"] != f"match:{matched}"
                or recorded_alternative["response_coordinate"] != matched
                or presentation["coordinate_bindings"].get(matched)
                != payload["alternative"]["alternative_id"]
            ):
                raise ValueError(
                    "source recovery is not supported by a recorded match "
                    "bound to the identified alternative"
                )
            if (
                payload["response_ingress_event_id"]
                != supporting_comparison["response_ingress_event_id"]
                or payload["response_capture_event_id"]
                != supporting_comparison["response_capture_event_id"]
            ):
                raise ValueError(
                    "source recovery does not carry its comparison's "
                    "recorded response evidence"
                )
            response_attempt = attempts.get(payload["response_attempt_ref"])
            preserved_response = (
                response_attempt["preserved_ingress"] if response_attempt else None
            )
            if preserved_response is None or (
                preserved_response["evidence_event_id"]
                != payload["response_ingress_event_id"]
                or preserved_response["raw_material_event_id"]
                != payload["response_capture_event_id"]
            ):
                raise ValueError(
                    "source recovery's response evidence does not agree "
                    "with the recorded ingress occurrence"
                )
            if payload["representation"] != recorded_alternative["representation"]:
                raise ValueError(
                    "source recovery does not agree with recorded formation "
                    "testimony on the representation boundary"
                )
            recovery = {
                "recovery_ref": payload["recovery_ref"],
                "event_id": event.id,
                "presentation_ref": payload["presentation_ref"],
                "presentation_formed_event_id": payload[
                    "presentation_formed_event_id"
                ],
                "presentation_emitted_event_id": payload[
                    "presentation_emitted_event_id"
                ],
                "comparison_event_id": payload["comparison_event_id"],
                "identification_event_id": payload["identification_event_id"],
                "response_attempt_ref": payload["response_attempt_ref"],
                "response_ingress_event_id": payload["response_ingress_event_id"],
                "response_capture_event_id": payload["response_capture_event_id"],
                "alternative": payload["alternative"],
                "source": payload["source"],
                # The complete representation boundary, reconstructed from
                # the recorded formation testimony it was validated against.
                "representation": recorded_alternative["representation"],
            }
            source_recoveries[payload["recovery_ref"]] = recovery
            latest_source_recovery = recovery
            continue
        if event.kind == _MEANING_RELATION_KIND:
            payload = event.payload
            recovery_event_id = payload["source_recovery_event_id"]
            recovery = source_recoveries.get(payload["recovery_ref"])
            if recovery is None:
                raise ValueError(
                    "meaning relation without recorded source recovery: "
                    f"{payload['recovery_ref']}"
                )
            # The joined pair must agree on every shared coordinate; a
            # mismatched pair is structurally refused rather than composed.
            presentation = presentations.get(payload["presentation_ref"])
            if presentation is None:
                raise ValueError(
                    "meaning relation names an unrecorded presentation: "
                    f"{payload['presentation_ref']}"
                )
            recorded_alternative = next(
                (
                    alternative
                    for alternative in presentation["alternatives"]
                    if alternative["alternative_id"] == payload["alternative_id"]
                ),
                None,
            )
            if recorded_alternative is None:
                raise ValueError(
                    "meaning relation names an alternative outside its "
                    "recorded presentation"
                )
            recorded_source = recorded_alternative["represented_source"]
            recorded_representation = recorded_alternative["representation"]
            agreements = (
                (recovery_event_id, recovery["event_id"], "source_recovery_event_id"),
                (
                    payload["presentation_ref"],
                    recovery["presentation_ref"],
                    "presentation_ref",
                ),
                (
                    payload["presentation_formed_event_id"],
                    recovery["presentation_formed_event_id"],
                    "presentation_formed_event_id",
                ),
                (
                    payload["identification_event_id"],
                    recovery["identification_event_id"],
                    "identification_event_id",
                ),
                (
                    payload["alternative_id"],
                    recovery["alternative"]["alternative_id"],
                    "alternative_id",
                ),
                (
                    payload["source_identity"],
                    recovery["source"]["identity"],
                    "source_identity",
                ),
                (
                    payload["source_reference"],
                    recovery["source"]["reference"],
                    "source_reference",
                ),
                # The proposition and its attribution must equal the recorded
                # formation testimony exactly; a forged M is refused here.
                (payload["proposition"], recorded_source["meaning"], "proposition"),
                (
                    payload["source_attribution"],
                    recorded_source["attribution"],
                    "source_attribution",
                ),
                (
                    payload["representation_purpose"],
                    recorded_representation["purpose"],
                    "representation_purpose",
                ),
                (
                    payload["representation_scope"],
                    recorded_representation["scope"],
                    "representation_scope",
                ),
            )
            for supplied, recorded, coordinate in agreements:
                if supplied != recorded:
                    raise ValueError(
                        "meaning relation does not agree with its recorded "
                        f"source recovery on {coordinate}"
                    )
            # The structural Authority coordinates are reconstructed from
            # recorded testimony, and the carried separation must equal the
            # reconstruction -- a forged standing, support, Evidence, or
            # Scope is refused rather than exposed to a later consumer.
            reconstructed_separation = {
                "source_authority": {
                    "standing": "bounded",
                    "supports": ["source-supplied-with-attributed-meaning"],
                    "evidence_event_ids": [recovery["presentation_formed_event_id"]],
                    "scope": {
                        "source_identity": recovery["source"]["identity"],
                        "proposition": recorded_source["meaning"],
                    },
                },
                "response_comparison_authority": {
                    "standing": "bounded",
                    "supports": ["response-matched-coordinate-within-presentation"],
                    "evidence_event_ids": [recovery["comparison_event_id"]],
                    "scope": {
                        "presentation_ref": recovery["presentation_ref"],
                        "response_attempt_ref": recovery["response_attempt_ref"],
                    },
                },
                "meaning_warrant": {
                    "standing": "established",
                    "supports": ["source-expresses-proposition"],
                    "evidence_event_ids": [
                        recovery["presentation_formed_event_id"],
                        recovery["event_id"],
                    ],
                    "scope": {
                        "source_identity": recovery["source"]["identity"],
                        "proposition": recorded_source["meaning"],
                    },
                },
                "operator_authority": {
                    "standing": "unresolved",
                    "supports": [],
                    "evidence_event_ids": [],
                    "scope": {"proposition": recorded_source["meaning"]},
                },
            }
            carried_separation = payload["authority_separation"]
            if set(carried_separation) != set(reconstructed_separation):
                raise ValueError(
                    "meaning relation does not carry the four Authority "
                    "coordinates"
                )
            authority_separation = {}
            for name, reconstructed in reconstructed_separation.items():
                carried = carried_separation[name]
                for field, value in reconstructed.items():
                    if carried.get(field) != value:
                        raise ValueError(
                            "meaning relation does not agree with recorded "
                            f"testimony on {name}.{field}"
                        )
                authority_separation[name] = {
                    **reconstructed,
                    "testimony": carried.get("testimony"),
                }
            # The relation's remaining Standing coordinates are producer
            # invariants at this boundary; a forged loss, Unknown, or
            # conflict inventory is refused rather than exposed.
            reconstructed_relation_standing = {
                "warrant_basis": (
                    "attributed developer-supplied meaning testimony "
                    "preserved by the recorded formation occurrence"
                ),
                "known_loss": [],
                "unknowns": [
                    "operator intent Unknown",
                    "operator selection occurrence Unknown",
                ],
                "conflicts": [],
            }
            for field, value in reconstructed_relation_standing.items():
                if payload[field] != value:
                    raise ValueError(
                        "meaning relation does not agree with recorded "
                        f"testimony on {field}"
                    )
            relation = {
                "relation_ref": payload["relation_ref"],
                "event_id": event.id,
                "source_recovery_event_id": recovery_event_id,
                "recovery_ref": payload["recovery_ref"],
                "presentation_ref": payload["presentation_ref"],
                "presentation_formed_event_id": payload[
                    "presentation_formed_event_id"
                ],
                "identification_event_id": payload["identification_event_id"],
                "alternative_id": payload["alternative_id"],
                "source_identity": payload["source_identity"],
                "proposition": payload["proposition"],
                "source_attribution": payload["source_attribution"],
                "source_reference": payload["source_reference"],
                "representation_purpose": payload["representation_purpose"],
                "representation_scope": payload["representation_scope"],
                "warrant_basis": reconstructed_relation_standing["warrant_basis"],
                "authority_separation": authority_separation,
                "known_loss": reconstructed_relation_standing["known_loss"],
                "unknowns": reconstructed_relation_standing["unknowns"],
                "conflicts": reconstructed_relation_standing["conflicts"],
            }
            meaning_relations[payload["relation_ref"]] = relation
            latest_meaning_relation = relation
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
                "raw_material_event_id": event.payload["raw_material_event_id"],
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
        "source_recoveries": source_recoveries,
        "meaning_relations": meaning_relations,
        "latest_source_recovery": latest_source_recovery,
        "latest_meaning_relation": latest_meaning_relation,
        "recorded_relation_standings": [],
        "known_loss": sorted(known_loss),
        "unknowns": sorted(unknowns),
        "conflicts": sorted(conflicts),
    }
