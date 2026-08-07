"""Explicit closed-choice fixture for exercising dormant exchange machinery.

These developer-authored sources were formerly injected into every
Presentation by ``form_operator_presentation``.  They are retained here as an
exact bounded test fixture so the dormant Compare, Identification,
source-recovery, meaning-relation, and interaction-goal machinery keeps its
coverage.  Supplying them is a caller's explicit act; nothing in the runtime
supplies them by default, and their presence in a fixture establishes no
Standing.
"""

from typing import Any

CANDIDATE_SOURCE_REFERENCE = (
    "book_of_seed/03-goals-and-advancement/"
    "operator-ingress-common-grammar-prerequisite.md"
)
CLOSED_CHOICE_FIXTURE_SOURCES = (
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
            "reference": CANDIDATE_SOURCE_REFERENCE,
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
            "provenance": CANDIDATE_SOURCE_REFERENCE,
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
            "reference": CANDIDATE_SOURCE_REFERENCE,
        },
    },
)


