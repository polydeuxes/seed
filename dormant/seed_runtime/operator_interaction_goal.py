"""Applicability, Admission, consumption, and bounded interaction-goal Standing."""

from __future__ import annotations

from typing import Any

from seed_runtime.events import EventLedger
from seed_runtime.ids import new_id
from seed_runtime.operator_session_standing import (
    CONSUMER_PURPOSE,
    determine_goal_applicability,
    project_operator_session_standing,
)

GOAL_APPLICABILITY_KIND = "operator.interaction.goal_applicability_established"
GOAL_ADMISSION_KIND = "operator.interaction.goal_admission_established"
GOAL_CONSUMPTION_KIND = "operator.interaction.goal_consumption_occurred"
GOAL_STANDING_KIND = "operator.interaction.goal_standing_established"

_GOAL_UNKNOWNS = (
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


def run_interaction_goal_establishment(
    ledger: EventLedger,
    *,
    workspace_id: str,
    session_id: str,
) -> dict[str, Any]:
    """One occurrence-local Consumer Responsibility for one exact purpose:
    determine whether the validated potential-goal relation bears on
    establishing the current bounded interaction goal.

    Input arrives only through the validated session projection; there is
    no caller-supplied relation dictionary.  Applicability, Admission,
    consumption, and the resulting bounded goal Standing are four distinct
    recorded results.  An inapplicable relation proceeds no further, and a
    missing treatment relation means the exact goal-consumption gap is
    preserved rather than closed by role or label.

    The resulting Standing is only that this exact bounded interaction
    proceeds under the proposition as its current goal.  Operator intent
    and selection remain Unknown, Operator Authority for the proposition
    remains unresolved, and no learning, remembering, acquisition, or
    downstream treatment occurs here.
    """
    scope = f"workspace:{workspace_id};session:{session_id}"
    standing = project_operator_session_standing(
        ledger, workspace_id=workspace_id, session_id=session_id
    )
    relation = standing["latest_meaning_relation"]
    if relation is None:
        return {"outcome": "no-validated-meaning-relation"}
    recovery = standing["source_recoveries"][relation["recovery_ref"]]
    presentation = standing["presentations"][relation["presentation_ref"]]
    recorded_alternative = next(
        alternative
        for alternative in presentation["alternatives"]
        if alternative["alternative_id"] == relation["alternative_id"]
    )
    treatment = recorded_alternative.get("consumer_treatment")

    # Consumer, Responsibility, and Act carry distinct exact identities.
    consumer_ref = new_id("interaction_goal_consumer")
    responsibility_ref = new_id("interaction_goal_responsibility")
    applicability_standing, basis = determine_goal_applicability(
        relation, recovery, treatment, scope=scope
    )
    # The determination Authority warrants the Applicability finding itself,
    # applicable or not; the treatment Authority -- present only where the
    # recorded treatment relation covers this exact material -- warrants
    # Admission, consumption, and goal establishment, and its absence is
    # what prevents them.
    determination_authority = {
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
    treatment_authority = None
    if treatment is not None and applicability_standing == "applicable":
        treatment_authority = {
            "identity": treatment["relation_identity"],
            "kind": treatment["treatment_kind"],
            "standing": "bounded",
            "supports": list(treatment["consumer_authority"]["supports"]),
            "evidence_event_ids": [relation["presentation_formed_event_id"]],
            "scope": dict(treatment["consumer_authority"]["scope"]),
            "boundary": treatment["authority_boundary"],
            "attribution": treatment["attribution"],
            "provenance": treatment["provenance"],
        }
    consumer_responsibility = {
        "identity": responsibility_ref,
        "consumer_identity": consumer_ref,
        "purpose": CONSUMER_PURPOSE,
        "scope": scope,
        "determination_authority": determination_authority,
        "treatment_authority": treatment_authority,
        "evidence_event_ids": [
            relation["event_id"],
            relation["presentation_formed_event_id"],
        ],
    }
    applicability_ref = new_id("goal_applicability")
    applicability_event = ledger.append(
        GOAL_APPLICABILITY_KIND,
        workspace_id,
        {
            "attempt_ref": recovery["response_attempt_ref"],
            "applicability_ref": applicability_ref,
            "consumer_ref": consumer_ref,
            "responsibility_ref": responsibility_ref,
            "act": {
                "act_ref": new_id("goal_applicability_act"),
                "act_kind": "determine-exact-goal-applicability",
                "responsibility_ref": responsibility_ref,
            },
            "basis": {
                "finding": basis,
                "responsibility_ref": responsibility_ref,
                "authority_support": "determine-exact-goal-applicability",
            },
            "consumer_purpose": CONSUMER_PURPOSE,
            "consumer_responsibility": consumer_responsibility,
            "meaning_relation_event_id": relation["event_id"],
            "relation_ref": relation["relation_ref"],
            "source_recovery_event_id": relation["source_recovery_event_id"],
            "presentation_ref": relation["presentation_ref"],
            "presentation_formed_event_id": relation["presentation_formed_event_id"],
            "alternative": {
                "alternative_id": recovery["alternative"]["alternative_id"],
                "role": recovery["alternative"]["role"],
            },
            "source_identity": relation["source_identity"],
            "proposition": relation["proposition"],
            "consumer_scope": scope,
            "standing": applicability_standing,
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
            "dimensions": _dimensions(
                identity=applicability_ref,
                content=f"goal applicability: {applicability_standing} ({basis})",
                standing=applicability_standing,
                source=relation["event_id"],
                responsibility=responsibility_ref,
                authority=(
                    "determines only whether the validated relation bears on "
                    "this exact Consumer purpose and Scope; establishes no "
                    "admission, consumption, goal standing, operator intent, "
                    "or selection"
                ),
                scope=scope,
                occurrence="applicability determination durably recorded",
            ),
            "known_loss": [],
            "unknowns": list(_GOAL_UNKNOWNS),
            "conflicts": [],
            "lineage": [
                relation["event_id"],
                relation["source_recovery_event_id"],
                relation["presentation_formed_event_id"],
            ],
            "mutates_cluster": False,
        },
        session_id=session_id,
    )
    if applicability_standing != "applicable":
        return {
            "outcome": "inapplicable",
            "basis": basis,
            "consumer_ref": consumer_ref,
            "applicability": {
                "applicability_ref": applicability_ref,
                "event_id": applicability_event.id,
                "standing": applicability_standing,
            },
        }

    admission_ref = new_id("goal_admission")
    admission_event = ledger.append(
        GOAL_ADMISSION_KIND,
        workspace_id,
        {
            "attempt_ref": recovery["response_attempt_ref"],
            "admission_ref": admission_ref,
            "applicability_event_id": applicability_event.id,
            "applicability_ref": applicability_ref,
            "consumer_ref": consumer_ref,
            "consumer_purpose": CONSUMER_PURPOSE,
            "meaning_relation_event_id": relation["event_id"],
            "alternative_id": recovery["alternative"]["alternative_id"],
            "source_identity": relation["source_identity"],
            "proposition": relation["proposition"],
            "consumer_scope": scope,
            "standing": "admitted",
            "responsibility_ref": responsibility_ref,
            "act": {
                "act_ref": new_id("goal_admission_act"),
                "act_kind": "admit-exact-meaning-relation",
                "responsibility_ref": responsibility_ref,
            },
            # The explicit constitutional basis for this exact movement.
            "basis": {
                "applicable_finding_event_id": applicability_event.id,
                "responsibility_ref": responsibility_ref,
                "authority_support": "admit-exact-meaning-relation",
            },
            "evidence_event_ids": [applicability_event.id, relation["event_id"]],
            "dimensions": _dimensions(
                identity=admission_ref,
                content="applicable relation admitted for possible use",
                standing="admitted",
                source=applicability_event.id,
                responsibility=responsibility_ref,
                authority=(
                    "admits the applicable relation for possible use under "
                    "this exact Consumer purpose and Scope only; admission "
                    "is not consumption, operator intent, selection, or goal "
                    "standing"
                ),
                scope=scope,
                occurrence="admission durably recorded",
            ),
            "known_loss": [],
            "unknowns": list(_GOAL_UNKNOWNS),
            "conflicts": [],
            "lineage": [applicability_event.id],
            "mutates_cluster": False,
        },
        session_id=session_id,
    )

    consumption_ref = new_id("goal_consumption")
    consumption_event = ledger.append(
        GOAL_CONSUMPTION_KIND,
        workspace_id,
        {
            "attempt_ref": recovery["response_attempt_ref"],
            "consumption_ref": consumption_ref,
            "admission_event_id": admission_event.id,
            "admission_ref": admission_ref,
            "applicability_event_id": applicability_event.id,
            "consumer_ref": consumer_ref,
            "consumer_purpose": CONSUMER_PURPOSE,
            "meaning_relation_event_id": relation["event_id"],
            "alternative_id": recovery["alternative"]["alternative_id"],
            "source_identity": relation["source_identity"],
            "proposition": relation["proposition"],
            "consumer_scope": scope,
            "responsibility_ref": responsibility_ref,
            "act": {
                "act_ref": new_id("goal_consumption_act"),
                "act_kind": "consume-exact-admitted-relation",
                "responsibility_ref": responsibility_ref,
            },
            "basis": {
                "admission_event_id": admission_event.id,
                "responsibility_ref": responsibility_ref,
                "authority_support": "consume-exact-admitted-relation",
            },
            "treatment_authority": treatment_authority,
            "evidence_event_ids": [
                admission_event.id,
                applicability_event.id,
                relation["event_id"],
            ],
            "dimensions": _dimensions(
                identity=consumption_ref,
                content="admitted relation consumed by the exact Consumer",
                standing="consumed",
                source=admission_event.id,
                responsibility=responsibility_ref,
                authority=(
                    "consumes the admitted relation under the exact "
                    "developer-supplied treatment relation only; establishes "
                    "the bounded goal standing recorded separately and "
                    "nothing else"
                ),
                scope=scope,
                occurrence="consumption occurrence durably recorded",
            ),
            "known_loss": [],
            "unknowns": list(_GOAL_UNKNOWNS),
            "conflicts": [],
            "lineage": [
                admission_event.id,
                applicability_event.id,
                relation["event_id"],
            ],
            "mutates_cluster": False,
        },
        session_id=session_id,
    )

    goal_standing_ref = new_id("interaction_goal_standing")
    goal_event = ledger.append(
        GOAL_STANDING_KIND,
        workspace_id,
        {
            "attempt_ref": recovery["response_attempt_ref"],
            "goal_standing_ref": goal_standing_ref,
            "consumption_event_id": consumption_event.id,
            "consumption_ref": consumption_ref,
            "admission_event_id": admission_event.id,
            "applicability_event_id": applicability_event.id,
            "consumer_ref": consumer_ref,
            "meaning_relation_event_id": relation["event_id"],
            "source_recovery_event_id": relation["source_recovery_event_id"],
            "presentation_ref": relation["presentation_ref"],
            "alternative_id": recovery["alternative"]["alternative_id"],
            "source_identity": relation["source_identity"],
            "proposition": relation["proposition"],
            "standing": (
                "this exact bounded interaction proceeds under the "
                "proposition as its current goal"
            ),
            "responsibility_ref": responsibility_ref,
            "act": {
                "act_ref": new_id("goal_standing_act"),
                "act_kind": "establish-bounded-interaction-goal-standing",
                "responsibility_ref": responsibility_ref,
            },
            "basis": {
                "consumption_event_id": consumption_event.id,
                "responsibility_ref": responsibility_ref,
                "authority_support": (
                    "establish-bounded-interaction-goal-standing"
                ),
            },
            "treatment_authority": treatment_authority,
            "operator_authority": {
                "standing": "unresolved",
                "supports": [],
                "evidence_event_ids": [],
                "scope": {"proposition": relation["proposition"]},
            },
            "consumer_scope": scope,
            "locality": "current bounded interaction",
            "evidence_event_ids": [
                consumption_event.id,
                admission_event.id,
                applicability_event.id,
                relation["event_id"],
            ],
            "dimensions": _dimensions(
                identity=goal_standing_ref,
                content=(
                    "bounded interaction-goal standing established for the "
                    "attributed proposition"
                ),
                standing="interaction-goal-established",
                source=consumption_event.id,
                responsibility=responsibility_ref,
                authority=(
                    "bounds this exact interaction to proceed under the "
                    "proposition as its current goal; establishes no operator "
                    "intent, selection, authorization, universal "
                    "applicability, acquisition, learning, or remembering"
                ),
                scope=scope,
                occurrence="goal standing durably recorded",
            ),
            "known_loss": [],
            "unknowns": list(_GOAL_UNKNOWNS),
            "conflicts": [],
            "lineage": [
                consumption_event.id,
                admission_event.id,
                applicability_event.id,
                relation["event_id"],
            ],
            "mutates_cluster": False,
        },
        session_id=session_id,
    )
    return {
        "outcome": "goal-standing-established",
        "consumer_ref": consumer_ref,
        "applicability": {
            "applicability_ref": applicability_ref,
            "event_id": applicability_event.id,
            "standing": "applicable",
        },
        "admission": {
            "admission_ref": admission_ref,
            "event_id": admission_event.id,
        },
        "consumption": {
            "consumption_ref": consumption_ref,
            "event_id": consumption_event.id,
        },
        "goal_standing": {
            "goal_standing_ref": goal_standing_ref,
            "event_id": goal_event.id,
            "proposition": relation["proposition"],
        },
    }
