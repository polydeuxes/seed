"""Recorded formation and emission of bounded closed-choice Presentations."""

from __future__ import annotations

from typing import Any, TextIO

from seed_runtime.events import EventLedger
from seed_runtime.ids import new_id

PRESENTATION_FORMED_KIND = "operator.presentation.formed"
PRESENTATION_EMITTED_KIND = "operator.presentation.emitted"

# Developer-supplied sources, attributed and bounded.  Their meanings are the
# Book's exact wording and are never derived from operator ingress material.
_CANDIDATE_SOURCE_REFERENCE = (
    "book_of_seed/03-goals-and-advancement/"
    "operator-ingress-common-grammar-prerequisite.md"
)
_DEVELOPER_SUPPLIED_SOURCES = (
    {
        "role": "potential-goal",
        "rendered_label": "Establish richer shared grammar with the Operator",
        "representation_purpose": (
            "represent the developer-supplied potential-goal candidate "
            "for bounded presentation"
        ),
        "represented_source": {
            # Stable exact identity of source candidate G, held apart from
            # its kind, meaning text, and reference so later recovery
            # identifies the candidate rather than a description of it.
            "identity": "source:developer-supplied-grammar-acquisition-candidate",
            "kind": "developer-supplied-potential-goal-candidate",
            "attribution": "developer-supplied",
            "meaning": "establish richer shared grammar with the operator",
            "reference": _CANDIDATE_SOURCE_REFERENCE,
        },
        # The exact developer-supplied treatment relation: this alternative
        # may be consumed by the exact interaction-goal Consumer.  Neither
        # the role string nor the rendered label carries this relation.
        "consumer_treatment": {
            # Stable treatment kind, distinct from the per-formation
            # instantiated relation identity added at formation.
            "treatment_kind": "bounded-interaction-goal-establishment",
            "identity": (
                "treatment:developer-supplied-interaction-goal-establishment"
            ),
            "consumer_purpose": (
                "determine whether the validated potential-goal relation "
                "bears on establishing the current bounded interaction goal"
            ),
            "treatment": (
                "consume the warranted meaning relation to establish "
                "bounded interaction-goal standing"
            ),
            "attribution": "developer-supplied",
            "authority_boundary": (
                "covers only bounded interaction-goal establishment for "
                "this exact source and proposition within the forming "
                "session; establishes no operator intent, selection, or "
                "downstream authorization"
            ),
            "provenance": _CANDIDATE_SOURCE_REFERENCE,
        },
    },
    {
        "role": "presentation-navigation",
        "rendered_label": "Show current Standing",
        "representation_purpose": (
            "represent navigation to the current Standing View"
        ),
        "represented_source": {
            "identity": "source:operator-ingress-view-navigation",
            "kind": "operator-ingress-view-navigation",
            "attribution": "developer-supplied",
            "meaning": "navigate to the current Standing View",
            "reference": (
                "seed_runtime.operator_ingress_view.format_operator_ingress_view"
            ),
        },
    },
    {
        "role": "local-stop",
        "rendered_label": "Establish no such goal and stop locally",
        "representation_purpose": (
            "represent the developer-supplied local-stop treatment"
        ),
        "represented_source": {
            "identity": "source:developer-supplied-local-stop-treatment",
            "kind": "developer-supplied-local-stop-treatment",
            "attribution": "developer-supplied",
            "meaning": "establish no such goal and stop locally",
            "reference": _CANDIDATE_SOURCE_REFERENCE,
        },
    },
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


def form_operator_presentation(
    ledger: EventLedger,
    *,
    workspace_id: str,
    session_id: str,
    session_standing: dict[str, Any],
) -> dict[str, Any]:
    """Form one exact bounded Presentation and record its formation occurrence.

    The presented alternatives represent developer-supplied sources under
    explicit roles; formation neither invents sources nor strengthens their
    standing, and no alternative's meaning is derived from ingress material.
    Formation is not emission: the returned Presentation carries no emission
    occurrence until :func:`emit_operator_presentation` records one.
    """
    presentation_id = new_id("operator_presentation")
    scope = f"workspace:{workspace_id};session:{session_id}"
    alternatives = []
    coordinate_bindings: dict[str, str] = {}
    for position, source in enumerate(_DEVELOPER_SUPPLIED_SOURCES, start=1):
        alternative_id = new_id("presented_alternative")
        coordinate = str(position)
        source_treatment = source.get("consumer_treatment")
        consumer_treatment = None
        if source_treatment is not None:
            consumer_treatment = {
                **source_treatment,
                "relation_identity": f"treatment-relation:{alternative_id}",
                "alternative_id": alternative_id,
                "source_identity": source["represented_source"]["identity"],
                "proposition": source["represented_source"]["meaning"],
                "scope": scope,
                # Structural Consumer Authority: standing, supported Acts,
                # Evidence, and Scope as coordinates.  The empty Evidence
                # list means the enclosing formation occurrence is the
                # Evidence, per the established convention.
                "consumer_authority": {
                    "standing": "bounded",
                    "supports": [
                        "admit-exact-meaning-relation",
                        "consume-exact-admitted-relation",
                        "establish-bounded-interaction-goal-standing",
                    ],
                    "evidence_event_ids": [],
                    "scope": {
                        "alternative_id": alternative_id,
                        "source_identity": source["represented_source"][
                            "identity"
                        ],
                        "proposition": source["represented_source"]["meaning"],
                        "consumer_purpose": source_treatment[
                            "consumer_purpose"
                        ],
                        "session_scope": scope,
                    },
                },
                "known_loss": [],
                "unknowns": [],
                "conflicts": [],
            }
        alternatives.append(
            {
                "alternative_id": alternative_id,
                "role": source["role"],
                "response_coordinate": coordinate,
                "rendered_label": source["rendered_label"],
                "represented_source": dict(source["represented_source"]),
                # None means no treatment relation is preserved for this
                # alternative and this exact Consumer; it is not global
                # inapplicability to every Consumer.
                "consumer_treatment": consumer_treatment,
                # Each A-to-G representation relation preserves its own
                # boundary; Presentation-level coordinates do not transfer
                # to it automatically.
                "representation": {
                    "purpose": source["representation_purpose"],
                    "scope": scope,
                    "provenance": source["represented_source"]["reference"],
                    # No separately recorded source-evidence events exist
                    # for a developer-supplied source; empty is absence of
                    # record, not negative standing and not Unknown.
                    "evidence_event_ids": [],
                    "known_loss": [
                        "rendered label compresses represented candidate "
                        "meaning"
                    ],
                    "unknowns": [],
                    "conflicts": [],
                },
            }
        )
        coordinate_bindings[coordinate] = alternative_id
    # The exact inventory of session events this formation consumed,
    # including any prior Presentation formation and emission Evidence.
    standing_evidence_ids = list(session_standing["consumed_event_ids"])
    # The latest recorded exchange finding, exposed exactly as recorded;
    # formation neither strengthens nor reinterprets it.
    prior_exchange_finding = session_standing.get("latest_exchange_finding")
    # The recovered source relation is exposed only when it belongs to the
    # exact latest finding's identification.
    recovered_meaning_relation = None
    latest_relation = session_standing.get("latest_meaning_relation")
    if (
        prior_exchange_finding is not None
        and latest_relation is not None
        and latest_relation["identification_event_id"]
        == prior_exchange_finding["identification"]["event_id"]
    ):
        recovered_meaning_relation = latest_relation
    # The validated current interaction-goal Standing, exposed exactly.
    current_interaction_goal = session_standing.get(
        "latest_interaction_goal_standing"
    )
    formed_event = ledger.append(
        PRESENTATION_FORMED_KIND,
        workspace_id,
        {
            "attempt_ref": None,
            "presentation_ref": presentation_id,
            "dimensions": _dimensions(
                identity=presentation_id,
                content=(
                    "bounded closed-choice presentation with "
                    f"{len(alternatives)} role-tagged alternatives"
                ),
                standing="formed",
                source=session_standing["as_of_event_id"],
                responsibility="bounded-presentation-formation",
                authority=(
                    "formation occurrence only; establishes no selection, "
                    "warrant, goal, or response treatment"
                ),
                scope=scope,
                occurrence=(
                    "alternatives, roles, token bindings, and represented-source "
                    "lineage durably recorded"
                ),
            ),
            "purpose": (
                "present developer-supplied bounded alternatives in the "
                "current session Standing context"
            ),
            "alternatives": alternatives,
            "coordinate_bindings": coordinate_bindings,
            "session_standing_as_of_event_id": session_standing["as_of_event_id"],
            "session_standing_evidence_ids": standing_evidence_ids,
            "prior_exchange_finding": prior_exchange_finding,
            "recovered_meaning_relation": recovered_meaning_relation,
            "current_interaction_goal": current_interaction_goal,
            "known_loss": [
                "rendered label compresses represented candidate meaning"
            ],
            "unknowns": [],
            "conflicts": [],
            "mutates_cluster": False,
        },
        session_id=session_id,
    )
    return {
        "presentation_id": presentation_id,
        "workspace_id": workspace_id,
        "session_id": session_id,
        "purpose": (
            "present developer-supplied bounded alternatives in the "
            "current session Standing context"
        ),
        "alternatives": alternatives,
        "coordinate_bindings": coordinate_bindings,
        "formed_event_id": formed_event.id,
        "emitted_event_id": None,
        "session_standing_as_of_event_id": session_standing["as_of_event_id"],
        "session_standing_evidence_ids": standing_evidence_ids,
        "prior_exchange_finding": prior_exchange_finding,
        "recovered_meaning_relation": recovered_meaning_relation,
        "current_interaction_goal": current_interaction_goal,
        "known_loss": ["rendered label compresses represented candidate meaning"],
        "unknowns": [],
        "conflicts": [],
    }


def render_operator_presentation(presentation: dict[str, Any]) -> str:
    """Render the bounded Presentation for the console output stream.

    Rendering exposes tokens, labels, and roles.  A rendered label is not the
    represented candidate's full meaning; that meaning stays preserved in the
    recorded formation payload.
    """
    lines = [f"Bounded Presentation {presentation['presentation_id']}"]
    finding = presentation.get("prior_exchange_finding")
    if finding is not None:
        identification = finding["identification"]
        comparison = finding["comparison"]
        if identification["identified_alternative"] is not None:
            alternative = identification["identified_alternative"]
            lines.append(
                "Prior exchange: alternative "
                f"{alternative['response_coordinate']} "
                f"({alternative['rendered_label']}) corresponds to the "
                f"captured material within {comparison['presentation_ref']}. "
                "Operator intent and selection remain Unknown."
            )
        elif comparison["matched_coordinate"] is not None:
            # A matched coordinate whose binding failed is not a no-match;
            # the two recorded results stay distinguishable here.
            lines.append(
                "Prior exchange: coordinate "
                f"{comparison['matched_coordinate']} matched within "
                f"{comparison['presentation_ref']}, but no presented "
                "alternative was lawfully identified "
                f"({identification['basis']})."
            )
        else:
            lines.append(
                "Prior exchange: no coordinate match within "
                f"{comparison['presentation_ref']}; response meaning and "
                "requested treatment remain Unknown."
            )
    relation = presentation.get("recovered_meaning_relation")
    if relation is not None:
        lines.append(
            f"Recovered source {relation['source_identity']} expresses: "
            f"\"{relation['proposition']}\" "
            f"({relation['source_attribution']}). Operator intent and "
            "selection remain Unknown; Operator Authority for this "
            "proposition remains unresolved."
        )
    goal = presentation.get("current_interaction_goal")
    if goal is not None:
        lines.extend(
            (
                f"Current bounded interaction goal: \"{goal['proposition']}\"",
                f"  Source: {goal['source_identity']}",
                "  Applicability: established for this exact Consumer purpose",
                "  Admission: established",
                "  Consumption: occurred",
                "  Operator intent remains Unknown. Operator Selection "
                "remains Unknown.",
                "  Operator Authority for the proposition remains "
                "unresolved. No Learning Standing is established by this "
                "path.",
            )
        )
    lines.append("Respond with exactly one token:")
    for alternative in presentation["alternatives"]:
        lines.append(
            f"  {alternative['response_coordinate']}. {alternative['rendered_label']}"
            f"  [{alternative['role']}]"
        )
    return "\n".join(lines) + "\n"


def emit_operator_presentation(
    ledger: EventLedger,
    *,
    presentation: dict[str, Any],
    output_stream: TextIO,
) -> dict[str, Any]:
    """Write the Presentation to the output stream and record the emission.

    Emission evidences only that the rendering was written to this boundary;
    external realization remains separately evidenced.
    """
    output_stream.write(render_operator_presentation(presentation))
    output_stream.flush()
    emitted_event = ledger.append(
        PRESENTATION_EMITTED_KIND,
        presentation["workspace_id"],
        {
            "attempt_ref": None,
            "presentation_ref": presentation["presentation_id"],
            "formed_event_id": presentation["formed_event_id"],
            "dimensions": _dimensions(
                identity=f"emission:{presentation['presentation_id']}",
                content="presentation rendering written to console output stream",
                standing="emitted",
                source=presentation["formed_event_id"],
                responsibility="bounded-presentation-emission",
                authority=(
                    "emission occurrence only; external realization separately "
                    "evidenced"
                ),
                scope=(
                    f"workspace:{presentation['workspace_id']};"
                    f"session:{presentation['session_id']}"
                ),
                occurrence="emission occurrence durably recorded",
            ),
            "known_loss": [],
            "unknowns": [],
            "conflicts": [],
            "lineage": [presentation["formed_event_id"]],
            "mutates_cluster": False,
        },
        session_id=presentation["session_id"],
    )
    presentation["emitted_event_id"] = emitted_event.id
    return presentation
