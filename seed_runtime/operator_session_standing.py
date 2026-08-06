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
    "operator.interaction.goal_applicability_established",
    "operator.interaction.goal_admission_established",
    "operator.interaction.goal_consumption_occurred",
    "operator.interaction.goal_standing_established",
}


CONSUMER_PURPOSE = (
    "determine whether the validated potential-goal relation bears on "
    "establishing the current bounded interaction goal"
)

_GOAL_APPLICABILITY_KIND = "operator.interaction.goal_applicability_established"
_GOAL_ADMISSION_KIND = "operator.interaction.goal_admission_established"
_GOAL_CONSUMPTION_KIND = "operator.interaction.goal_consumption_occurred"
_GOAL_STANDING_KIND = "operator.interaction.goal_standing_established"


def determine_goal_applicability(
    relation: dict[str, Any],
    recovery: dict[str, Any],
    treatment: dict[str, Any] | None,
    *,
    scope: str,
) -> tuple[str, str]:
    """Derive the only lawful Applicability finding, structurally.

    The determination consumes the alternative's role, the exact
    developer-supplied treatment relation, the structural Authority
    coordinates of the validated meaning relation, and Scope agreement.
    It never inspects the proposition's wording.
    """
    role = recovery["alternative"]["role"]
    if role != "potential-goal":
        return "inapplicable", "role-not-potential-goal"
    if treatment is None:
        return "inapplicable", "no-consumer-treatment-relation"
    if (
        treatment["consumer_purpose"] != CONSUMER_PURPOSE
        or treatment["alternative_id"] != recovery["alternative"]["alternative_id"]
        or treatment["source_identity"] != relation["source_identity"]
        or treatment["proposition"] != relation["proposition"]
        or treatment["attribution"] != "developer-supplied"
    ):
        return "inapplicable", "treatment-disagreement"
    if treatment["scope"] != scope or relation["representation_scope"] != scope:
        return "inapplicable", "scope-mismatch"
    if treatment.get("treatment_kind") != "bounded-interaction-goal-establishment":
        return "inapplicable", "treatment-kind-mismatch"
    authority = treatment.get("consumer_authority")
    if authority is None or (
        authority.get("standing") != "bounded"
        or authority.get("supports")
        != [
            "admit-exact-meaning-relation",
            "consume-exact-admitted-relation",
            "establish-bounded-interaction-goal-standing",
        ]
        or authority.get("scope")
        != {
            "alternative_id": treatment["alternative_id"],
            "source_identity": treatment["source_identity"],
            "proposition": treatment["proposition"],
            "consumer_purpose": treatment["consumer_purpose"],
            "session_scope": treatment["scope"],
        }
    ):
        return "inapplicable", "consumer-authority-not-established"
    if treatment.get("conflicts"):
        return "inapplicable", "treatment-conflicted"
    separation = relation["authority_separation"]
    if (
        separation["meaning_warrant"]["standing"] != "established"
        or separation["source_authority"]["standing"] != "bounded"
        or separation["response_comparison_authority"]["standing"] != "bounded"
    ):
        return "inapplicable", "authority-coordinates-not-established"
    return "applicable", "structural-agreement"



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
    scope = f"workspace:{workspace_id};session:{session_id}"
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
    goal_applicabilities: dict[str, dict[str, Any]] = {}
    goal_identities: dict[str, str] = {}
    goal_admissions: dict[str, dict[str, Any]] = {}
    goal_consumptions: dict[str, dict[str, Any]] = {}
    goal_standings: dict[str, dict[str, Any]] = {}
    latest_interaction_goal_standing: dict[str, Any] | None = None
    known_loss: set[str] = set()
    unknowns: set[str] = set()
    conflicts: set[str] = set()
    as_of_event_id: str | None = None
    consumed_event_ids: list[str] = []
    event_count = 0

    def register_goal_identity(identity: str, coordinate: str) -> None:
        existing = goal_identities.get(identity)
        if existing is not None:
            raise ValueError(
                f"duplicate goal identity {identity}: {existing} and {coordinate}"
            )
        goal_identities[identity] = coordinate

    for event in ledger.list(workspace_id):
        if event.session_id != session_id:
            continue
        if not (
            event.kind.startswith("operator.ingress.")
            or event.kind.startswith("operator.presentation.")
            or event.kind.startswith("operator.exchange.")
            or event.kind.startswith("operator.interaction.")
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
            if payload["presentation_ref"] in presentations:
                raise ValueError(
                    "duplicate presentation reference: "
                    f"{payload['presentation_ref']}"
                )
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
            if payload["comparison_ref"] in comparisons:
                raise ValueError(
                    "duplicate comparison reference: "
                    f"{payload['comparison_ref']}"
                )
            # The comparison result is re-derived from recorded C and R;
            # a carried result that contradicts the recorded ingress
            # content or C's recorded coordinates is refused.
            presentation = presentations.get(payload["presentation_ref"])
            if presentation is None or (
                payload["presentation_formed_event_id"]
                != presentation["formed_event_id"]
                or payload["presentation_emitted_event_id"]
                != presentation["emitted_event_id"]
                or presentation["emitted_event_id"] is None
            ):
                raise ValueError(
                    "comparison does not carry the recorded presentation "
                    "occurrence lineage"
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
                    "comparison's response evidence does not agree with a "
                    "recorded ingress occurrence"
                )
            if (
                preserved_response["produced_after_presentation_ref"]
                != payload["presentation_ref"]
                or preserved_response[
                    "produced_after_presentation_formed_event_id"
                ]
                != presentation["formed_event_id"]
                or preserved_response[
                    "produced_after_presentation_emitted_event_id"
                ]
                != presentation["emitted_event_id"]
            ):
                raise ValueError(
                    "recorded ingress was not produced after this exact "
                    "presentation"
                )
            expected_representation = preserved_response["content"]
            expected_coordinate_set = sorted(
                alternative["response_coordinate"]
                for alternative in presentation["alternatives"]
            )
            expected_match = (
                expected_representation
                if expected_representation in set(expected_coordinate_set)
                else None
            )
            expected_outcome = (
                f"match:{expected_match}"
                if expected_match is not None
                else "no-coordinate-match"
            )
            expected_unknowns = (
                [
                    "operator intent Unknown",
                    "operator selection occurrence Unknown",
                ]
                if expected_match is not None
                else [
                    "response meaning Unknown",
                    "operator intent Unknown",
                    "operator selection occurrence Unknown",
                    "requested treatment Unknown",
                ]
            )
            for field, expected in (
                ("compared_representation", expected_representation),
                ("coordinate_set", expected_coordinate_set),
                ("matched_coordinate", expected_match),
                ("outcome", expected_outcome),
                ("unknowns", expected_unknowns),
            ):
                if payload[field] != expected:
                    raise ValueError(
                        "comparison does not agree with the result derived "
                        f"from recorded testimony on {field}"
                    )
            comparisons[payload["comparison_ref"]] = {
                "comparison_ref": payload["comparison_ref"],
                "event_id": event.id,
                "presentation_ref": payload["presentation_ref"],
                "response_attempt_ref": payload["response_attempt_ref"],
                "response_ingress_event_id": payload["response_ingress_event_id"],
                "response_capture_event_id": payload["response_capture_event_id"],
                "compared_representation": expected_representation,
                "coordinate_set": expected_coordinate_set,
                "matched_coordinate": expected_match,
                "outcome": expected_outcome,
                "unknowns": expected_unknowns,
            }
            continue
        if event.kind == _IDENTIFICATION_KIND:
            payload = event.payload
            if payload["identification_ref"] in identifications:
                raise ValueError(
                    "duplicate identification reference: "
                    f"{payload['identification_ref']}"
                )
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
            # The only lawful identification result is re-derived from the
            # reconstructed comparison and C's recorded bindings; the
            # carried basis, outcome, and complete identified alternative
            # must equal that reconstruction.
            identification_presentation = presentations.get(
                identification["presentation_ref"]
            )
            if identification_presentation is None:
                raise ValueError(
                    "identification names an unrecorded presentation: "
                    f"{identification['presentation_ref']}"
                )
            matched = comparison["matched_coordinate"]
            expected_identified = None
            if matched is None:
                expected_basis = "no-coordinate-match"
            else:
                bound_alternative_id = identification_presentation[
                    "coordinate_bindings"
                ].get(matched)
                recorded_by_id = {
                    alternative["alternative_id"]: alternative
                    for alternative in identification_presentation["alternatives"]
                }
                if bound_alternative_id is None:
                    expected_basis = "binding-absent"
                elif bound_alternative_id not in recorded_by_id:
                    expected_basis = "binding-inapplicable"
                else:
                    expected_basis = "identified"
                    recorded = recorded_by_id[bound_alternative_id]
                    expected_identified = {
                        "alternative_id": recorded["alternative_id"],
                        "role": recorded["role"],
                        "response_coordinate": recorded["response_coordinate"],
                        "rendered_label": recorded["rendered_label"],
                    }
            expected_outcome = (
                "alternative-identified"
                if expected_identified is not None
                else "no-presented-alternative-identified"
            )
            if (
                identification["basis"] != expected_basis
                or identification["outcome"] != expected_outcome
                or identification["identified_alternative"] != expected_identified
            ):
                raise ValueError(
                    "identification does not agree with the result derived "
                    "from its recorded comparison and binding"
                )
            identification["identified_alternative"] = expected_identified
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
            if payload["recovery_ref"] in source_recoveries:
                raise ValueError(
                    f"duplicate recovery reference: {payload['recovery_ref']}"
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
            if payload["relation_ref"] in meaning_relations:
                raise ValueError(
                    f"duplicate relation reference: {payload['relation_ref']}"
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
        if event.kind == _GOAL_APPLICABILITY_KIND:
            payload = event.payload
            if payload["applicability_ref"] in goal_applicabilities:
                raise ValueError(
                    "duplicate applicability reference: "
                    f"{payload['applicability_ref']}"
                )
            relation = meaning_relations.get(payload["relation_ref"])
            if relation is None or relation["event_id"] != (
                payload["meaning_relation_event_id"]
            ):
                raise ValueError(
                    "goal applicability does not consume a recorded "
                    "meaning relation"
                )
            recovery = source_recoveries[relation["recovery_ref"]]
            presentation = presentations[relation["presentation_ref"]]
            recorded_alternative = next(
                alternative
                for alternative in presentation["alternatives"]
                if alternative["alternative_id"] == relation["alternative_id"]
            )
            treatment = recorded_alternative.get("consumer_treatment")
            derived_standing, derived_basis = determine_goal_applicability(
                relation, recovery, treatment, scope=scope
            )
            expected_determination_authority = {
                "standing": "bounded",
                "supports": ["determine-exact-goal-applicability"],
                "evidence_event_ids": [
                    relation["event_id"],
                    relation["presentation_formed_event_id"],
                ],
                "scope": {
                    "meaning_relation_event_id": relation["event_id"],
                    "alternative_id": relation["alternative_id"],
                    "source_identity": relation["source_identity"],
                    "proposition": relation["proposition"],
                    "consumer_purpose": CONSUMER_PURPOSE,
                    "session_scope": scope,
                },
            }
            expected_authority = None
            if derived_standing == "applicable":
                expected_authority = {
                    "identity": treatment["relation_identity"],
                    "kind": treatment["treatment_kind"],
                    "standing": "bounded",
                    "supports": list(
                        treatment["consumer_authority"]["supports"]
                    ),
                    "evidence_event_ids": [
                        relation["presentation_formed_event_id"]
                    ],
                    "scope": dict(treatment["consumer_authority"]["scope"]),
                    "boundary": treatment["authority_boundary"],
                    "attribution": treatment["attribution"],
                    "provenance": treatment["provenance"],
                }
            expected = {
                "consumer_purpose": CONSUMER_PURPOSE,
                "act": {
                    "act_ref": payload["act"]["act_ref"],
                    "act_kind": "determine-exact-goal-applicability",
                    "responsibility_ref": payload["responsibility_ref"],
                },
                "basis": {
                    "finding": derived_basis,
                    "responsibility_ref": payload["responsibility_ref"],
                    "authority_support": "determine-exact-goal-applicability",
                },
                "consumer_responsibility": {
                    "identity": payload["responsibility_ref"],
                    "consumer_identity": payload["consumer_ref"],
                    "purpose": CONSUMER_PURPOSE,
                    "scope": scope,
                    "determination_authority": expected_determination_authority,
                    "treatment_authority": expected_authority,
                    "evidence_event_ids": [
                        relation["event_id"],
                        relation["presentation_formed_event_id"],
                    ],
                },
                "known_loss": [],
                "unknowns": [
                    "operator intent Unknown",
                    "operator selection occurrence Unknown",
                ],
                "conflicts": [],
                "lineage": [
                    relation["event_id"],
                    relation["source_recovery_event_id"],
                    relation["presentation_formed_event_id"],
                ],
                "source_recovery_event_id": relation["source_recovery_event_id"],
                "presentation_ref": relation["presentation_ref"],
                "presentation_formed_event_id": relation[
                    "presentation_formed_event_id"
                ],
                "alternative": {
                    "alternative_id": recovery["alternative"]["alternative_id"],
                    "role": recovery["alternative"]["role"],
                },
                "source_identity": relation["source_identity"],
                "proposition": relation["proposition"],
                "consumer_scope": scope,
                "standing": derived_standing,
                "consumed_authority_coordinates": {
                    name: relation["authority_separation"][name]["standing"]
                    for name in (
                        "source_authority",
                        "response_comparison_authority",
                        "meaning_warrant",
                        "operator_authority",
                    )
                },
                "consumer_treatment": treatment,
                "evidence_event_ids": [
                    relation["event_id"],
                    relation["source_recovery_event_id"],
                    relation["presentation_formed_event_id"],
                ],
                "dimensions": {
                    **payload["dimensions"],
                    "identity": payload["applicability_ref"],
                    "standing": derived_standing,
                    "source_provenance": relation["event_id"],
                    "responsibility": payload["responsibility_ref"],
                    "scope_locality": scope,
                },
            }
            for field, value in expected.items():
                if payload[field] != value:
                    raise ValueError(
                        "goal applicability does not agree with the result "
                        f"derived from recorded testimony on {field}"
                    )
            register_goal_identity(payload["consumer_ref"], "Consumer")
            register_goal_identity(payload["responsibility_ref"], "Responsibility")
            register_goal_identity(payload["act"]["act_ref"], "Applicability Act")
            register_goal_identity(
                payload["applicability_ref"], "Applicability result"
            )
            goal_applicabilities[payload["applicability_ref"]] = {
                "applicability_ref": payload["applicability_ref"],
                "event_id": event.id,
                "consumer_ref": payload["consumer_ref"],
                "responsibility_ref": payload["responsibility_ref"],
                "relation_ref": payload["relation_ref"],
                "meaning_relation_event_id": payload["meaning_relation_event_id"],
                "treatment_authority": expected_authority,
                "determination_authority": expected_determination_authority,
                **expected,
            }
            continue
        if event.kind == _GOAL_ADMISSION_KIND:
            payload = event.payload
            if payload["admission_ref"] in goal_admissions:
                raise ValueError(
                    f"duplicate admission reference: {payload['admission_ref']}"
                )
            applicability = goal_applicabilities.get(payload["applicability_ref"])
            if applicability is None or (
                applicability["event_id"] != payload["applicability_event_id"]
                or applicability["standing"] != "applicable"
            ):
                raise ValueError(
                    "goal admission does not consume a recorded applicable "
                    "finding"
                )
            for field in (
                "consumer_ref",
                "consumer_purpose",
                "meaning_relation_event_id",
                "source_identity",
                "proposition",
                "consumer_scope",
            ):
                if payload[field] != applicability[field]:
                    raise ValueError(
                        "goal admission does not agree with its recorded "
                        f"applicability on {field}"
                    )
            if payload["alternative_id"] != (
                applicability["alternative"]["alternative_id"]
            ) or payload["standing"] != "admitted":
                raise ValueError(
                    "goal admission does not agree with its recorded "
                    "applicability on alternative or standing"
                )
            expected_admission = {
                "responsibility_ref": applicability["responsibility_ref"],
                "act": {
                    "act_ref": payload["act"]["act_ref"],
                    "act_kind": "admit-exact-meaning-relation",
                    "responsibility_ref": applicability["responsibility_ref"],
                },
                "basis": {
                    "applicable_finding_event_id": applicability["event_id"],
                    "responsibility_ref": applicability["responsibility_ref"],
                    "authority_support": "admit-exact-meaning-relation",
                },
                "evidence_event_ids": [
                    applicability["event_id"],
                    applicability["meaning_relation_event_id"],
                ],
                "lineage": [applicability["event_id"]],
                "known_loss": [],
                "unknowns": [
                    "operator intent Unknown",
                    "operator selection occurrence Unknown",
                ],
                "conflicts": [],
                "dimensions": {
                    **payload["dimensions"],
                    "identity": payload["admission_ref"],
                    "standing": "admitted",
                    "source_provenance": applicability["event_id"],
                    "responsibility": applicability["responsibility_ref"],
                    "scope_locality": scope,
                },
            }
            for field, value in expected_admission.items():
                if payload[field] != value:
                    raise ValueError(
                        "goal admission does not carry its recorded basis "
                        f"and boundary on {field}"
                    )
            register_goal_identity(payload["act"]["act_ref"], "Admission Act")
            register_goal_identity(payload["admission_ref"], "Admission result")
            goal_admissions[payload["admission_ref"]] = {
                "admission_ref": payload["admission_ref"],
                "event_id": event.id,
                "applicability_ref": payload["applicability_ref"],
                "applicability_event_id": payload["applicability_event_id"],
                "consumer_ref": payload["consumer_ref"],
                "consumer_purpose": payload["consumer_purpose"],
                "meaning_relation_event_id": payload["meaning_relation_event_id"],
                "alternative_id": payload["alternative_id"],
                "source_identity": payload["source_identity"],
                "proposition": payload["proposition"],
                "consumer_scope": payload["consumer_scope"],
                "standing": "admitted",
                "responsibility_ref": applicability["responsibility_ref"],
                "act": expected_admission["act"],
                "basis": expected_admission["basis"],
                "evidence_event_ids": expected_admission["evidence_event_ids"],
                "lineage": expected_admission["lineage"],
                "known_loss": expected_admission["known_loss"],
                "unknowns": expected_admission["unknowns"],
                "conflicts": expected_admission["conflicts"],
            }
            continue
        if event.kind == _GOAL_CONSUMPTION_KIND:
            payload = event.payload
            if payload["consumption_ref"] in goal_consumptions:
                raise ValueError(
                    "duplicate consumption reference: "
                    f"{payload['consumption_ref']}"
                )
            admission = goal_admissions.get(payload["admission_ref"])
            if admission is None or (
                admission["event_id"] != payload["admission_event_id"]
                or admission["applicability_event_id"]
                != payload["applicability_event_id"]
            ):
                raise ValueError(
                    "goal consumption does not consume a recorded admission"
                )
            for field in (
                "consumer_ref",
                "consumer_purpose",
                "meaning_relation_event_id",
                "alternative_id",
                "source_identity",
                "proposition",
                "consumer_scope",
            ):
                if payload[field] != admission[field]:
                    raise ValueError(
                        "goal consumption does not agree with its recorded "
                        f"admission on {field}"
                    )
            applicability = goal_applicabilities[admission["applicability_ref"]]
            expected_authority = applicability["treatment_authority"]
            if payload["treatment_authority"] != expected_authority:
                raise ValueError(
                    "goal consumption does not carry the recorded treatment "
                    "authority"
                )
            expected_consumption = {
                "responsibility_ref": applicability["responsibility_ref"],
                "act": {
                    "act_ref": payload["act"]["act_ref"],
                    "act_kind": "consume-exact-admitted-relation",
                    "responsibility_ref": applicability["responsibility_ref"],
                },
                "basis": {
                    "admission_event_id": admission["event_id"],
                    "responsibility_ref": applicability["responsibility_ref"],
                    "authority_support": "consume-exact-admitted-relation",
                },
                "evidence_event_ids": [
                    admission["event_id"],
                    admission["applicability_event_id"],
                    admission["meaning_relation_event_id"],
                ],
                "lineage": [
                    admission["event_id"],
                    admission["applicability_event_id"],
                    admission["meaning_relation_event_id"],
                ],
                "known_loss": [],
                "unknowns": [
                    "operator intent Unknown",
                    "operator selection occurrence Unknown",
                ],
                "conflicts": [],
                "dimensions": {
                    **payload["dimensions"],
                    "identity": payload["consumption_ref"],
                    "standing": "consumed",
                    "source_provenance": admission["event_id"],
                    "responsibility": applicability["responsibility_ref"],
                    "scope_locality": scope,
                },
            }
            for field, value in expected_consumption.items():
                if payload[field] != value:
                    raise ValueError(
                        "goal consumption does not carry its recorded basis "
                        f"and boundary on {field}"
                    )
            register_goal_identity(payload["act"]["act_ref"], "consumption Act")
            register_goal_identity(
                payload["consumption_ref"], "consumption occurrence/result"
            )
            goal_consumptions[payload["consumption_ref"]] = {
                "consumption_ref": payload["consumption_ref"],
                "event_id": event.id,
                "consumer_ref": applicability["consumer_ref"],
                "admission_ref": payload["admission_ref"],
                "admission_event_id": payload["admission_event_id"],
                "applicability_event_id": payload["applicability_event_id"],
                "consumer_ref": payload["consumer_ref"],
                "meaning_relation_event_id": payload["meaning_relation_event_id"],
                "alternative_id": payload["alternative_id"],
                "source_identity": payload["source_identity"],
                "proposition": payload["proposition"],
                "consumer_scope": payload["consumer_scope"],
                "responsibility_ref": applicability["responsibility_ref"],
                "treatment_authority": expected_authority,
                "act": expected_consumption["act"],
                "basis": expected_consumption["basis"],
                "evidence_event_ids": expected_consumption["evidence_event_ids"],
                "lineage": expected_consumption["lineage"],
                "known_loss": expected_consumption["known_loss"],
                "unknowns": expected_consumption["unknowns"],
                "conflicts": expected_consumption["conflicts"],
            }
            continue
        if event.kind == _GOAL_STANDING_KIND:
            payload = event.payload
            if payload["goal_standing_ref"] in goal_standings:
                raise ValueError(
                    "duplicate goal-standing reference: "
                    f"{payload['goal_standing_ref']}"
                )
            consumption = goal_consumptions.get(payload["consumption_ref"])
            if consumption is None or (
                consumption["event_id"] != payload["consumption_event_id"]
                or consumption["admission_event_id"]
                != payload["admission_event_id"]
                or consumption["applicability_event_id"]
                != payload["applicability_event_id"]
            ):
                raise ValueError(
                    "goal standing does not consume a recorded consumption "
                    "occurrence"
                )
            for field in (
                "consumer_ref",
                "meaning_relation_event_id",
                "alternative_id",
                "source_identity",
                "proposition",
            ):
                if payload[field] != consumption[field]:
                    raise ValueError(
                        "goal standing does not agree with its recorded "
                        f"consumption on {field}"
                    )
            expected_operator_authority = {
                "standing": "unresolved",
                "supports": [],
                "evidence_event_ids": [],
                "scope": {"proposition": consumption["proposition"]},
            }
            if payload["operator_authority"] != expected_operator_authority:
                raise ValueError(
                    "goal standing does not preserve the unresolved operator "
                    "authority boundary"
                )
            if payload["treatment_authority"] != consumption["treatment_authority"]:
                raise ValueError(
                    "goal standing does not carry the recorded treatment "
                    "authority"
                )
            goal_applicability = goal_applicabilities[
                goal_admissions[consumption["admission_ref"]][
                    "applicability_ref"
                ]
            ]
            goal_relation = meaning_relations[goal_applicability["relation_ref"]]
            expected_goal = {
                "source_recovery_event_id": goal_relation[
                    "source_recovery_event_id"
                ],
                "presentation_ref": goal_relation["presentation_ref"],
                "standing": (
                    "this exact bounded interaction proceeds under the "
                    "proposition as its current goal"
                ),
                "locality": "current bounded interaction",
                "consumer_scope": consumption["consumer_scope"],
                "responsibility_ref": consumption["responsibility_ref"],
                "act": {
                    "act_ref": payload["act"]["act_ref"],
                    "act_kind": "establish-bounded-interaction-goal-standing",
                    "responsibility_ref": consumption["responsibility_ref"],
                },
                "basis": {
                    "consumption_event_id": consumption["event_id"],
                    "responsibility_ref": consumption["responsibility_ref"],
                    "authority_support": (
                        "establish-bounded-interaction-goal-standing"
                    ),
                },
                "evidence_event_ids": [
                    consumption["event_id"],
                    consumption["admission_event_id"],
                    consumption["applicability_event_id"],
                    consumption["meaning_relation_event_id"],
                ],
                "lineage": [
                    consumption["event_id"],
                    consumption["admission_event_id"],
                    consumption["applicability_event_id"],
                    consumption["meaning_relation_event_id"],
                ],
                "known_loss": [],
                "unknowns": [
                    "operator intent Unknown",
                    "operator selection occurrence Unknown",
                ],
                "conflicts": [],
                "dimensions": {
                    **payload["dimensions"],
                    "identity": payload["goal_standing_ref"],
                    "standing": "interaction-goal-established",
                    "source_provenance": consumption["event_id"],
                    "responsibility": consumption["responsibility_ref"],
                    "scope_locality": scope,
                },
            }
            for field, value in expected_goal.items():
                if payload[field] != value:
                    raise ValueError(
                        "goal standing does not agree with the standing "
                        f"derived from recorded testimony on {field}"
                    )
            goal_standing = {
                "goal_standing_ref": payload["goal_standing_ref"],
                "event_id": event.id,
                "consumption_ref": payload["consumption_ref"],
                "consumption_event_id": payload["consumption_event_id"],
                "admission_event_id": payload["admission_event_id"],
                "applicability_event_id": payload["applicability_event_id"],
                "consumer_ref": payload["consumer_ref"],
                "meaning_relation_event_id": payload["meaning_relation_event_id"],
                "source_recovery_event_id": payload["source_recovery_event_id"],
                "presentation_ref": payload["presentation_ref"],
                "alternative_id": payload["alternative_id"],
                "source_identity": payload["source_identity"],
                "proposition": payload["proposition"],
                "standing": expected_goal["standing"],
                "responsibility_ref": consumption["responsibility_ref"],
                # The complete validated boundary, retained so the next
                # Consumer reads projected Standing rather than raw events.
                "consumer_responsibility": goal_applicability[
                    "consumer_responsibility"
                ],
                "treatment_authority": consumption["treatment_authority"],
                "operator_authority": expected_operator_authority,
                "consumer_scope": consumption["consumer_scope"],
                "locality": expected_goal["locality"],
                "act": expected_goal["act"],
                "bases": {
                    "applicability": goal_applicability["basis"],
                    "admission": goal_admissions[consumption["admission_ref"]][
                        "basis"
                    ],
                    "consumption": consumption["basis"],
                    "goal_standing": expected_goal["basis"],
                },
                "evidence_event_ids": expected_goal["evidence_event_ids"],
                "lineage": expected_goal["lineage"],
                "known_loss": expected_goal["known_loss"],
                "unknowns": expected_goal["unknowns"],
                "conflicts": expected_goal["conflicts"],
            }
            register_goal_identity(
                payload["act"]["act_ref"], "goal-establishment Act"
            )
            register_goal_identity(payload["goal_standing_ref"], "goal Standing")
            goal_standings[payload["goal_standing_ref"]] = goal_standing
            latest_interaction_goal_standing = goal_standing
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
                "content": event.payload["dimensions"]["content"],
                "produced_after_presentation_ref": event.payload.get(
                    "produced_after_presentation_ref"
                ),
                "produced_after_presentation_formed_event_id": event.payload.get(
                    "produced_after_presentation_formed_event_id"
                ),
                "produced_after_presentation_emitted_event_id": event.payload.get(
                    "produced_after_presentation_emitted_event_id"
                ),
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
        "goal_applicabilities": goal_applicabilities,
        "goal_admissions": goal_admissions,
        "goal_consumptions": goal_consumptions,
        "goal_standings": goal_standings,
        "latest_interaction_goal_standing": latest_interaction_goal_standing,
        "recorded_relation_standings": [],
        "known_loss": sorted(known_loss),
        "unknowns": sorted(unknowns),
        "conflicts": sorted(conflicts),
    }
