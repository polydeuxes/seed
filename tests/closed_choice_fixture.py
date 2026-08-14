"""Explicit non-result-directed closed-choice fixture for exchange mechanics."""

from typing import Any

CLOSED_CHOICE_FIXTURE_SOURCES = (
    {
        "role": "presentation-navigation",
        "rendered_label": "Show preserved ingress",
        "representation_result_boundary": "represent navigation to preserved ingress",
        "represented_source": {
            "identity": "source:operator-ingress-navigation",
            "kind": "operator-ingress-navigation",
            "source_role": "developer-supplied",
            "represented_result": "navigate to preserved operator ingress",
            "reference": "seed_runtime.operator_ingress_view",
        },
    },
    {
        "role": "presentation-navigation",
        "rendered_label": "Show current Standing",
        "representation_result_boundary": (
            "represent navigation to the current Standing View"
        ),
        "represented_source": {
            "identity": "source:operator-ingress-view-navigation",
            "kind": "operator-ingress-view-navigation",
            "source_role": "developer-supplied",
            "represented_result": "navigate to the current Standing View",
            "reference": (
                "seed_runtime.operator_ingress_view.format_operator_ingress_view"
            ),
        },
    },
    {
        "role": "presentation-navigation",
        "rendered_label": "Show recorded exchange",
        "representation_result_boundary": "represent navigation to recorded exchange",
        "represented_source": {
            "identity": "source:operator-exchange-navigation",
            "kind": "operator-exchange-navigation",
            "source_role": "developer-supplied",
            "represented_result": "navigate to the recorded operator exchange",
            "reference": "seed_runtime.operator_response_comparison",
        },
    },
)
