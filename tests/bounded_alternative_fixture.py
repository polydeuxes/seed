"""Explicit bounded alternatives for Representation tests."""

from typing import Any

BOUNDED_ALTERNATIVE_FIXTURE_SOURCES = (
    {
        "role": "representation-navigation",
        "label": "Show preserved Ingest",
        "representation_result_boundary": "represent navigation to preserved Ingest",
        "represented_source": {
            "identity": "source:operator-ingest-navigation",
            "kind": "operator-ingest-navigation",
            "source_role": "developer-supplied",
            "represented_result": "navigate to preserved operator Ingest",
            "reference": "seed_runtime.operator_ingest_view",
        },
    },
    {
        "role": "representation-navigation",
        "label": "Show current Standing",
        "representation_result_boundary": (
            "represent navigation to the current Standing Standing representation"
        ),
        "represented_source": {
            "identity": "source:operator-ingest-standing-navigation",
            "kind": "operator-ingest-standing-navigation",
            "source_role": "developer-supplied",
            "represented_result": "navigate to the current Standing Standing representation",
            "reference": (
                "seed_runtime.operator_ingest_view.format_operator_ingest_view"
            ),
        },
    },
    {
        "role": "representation-navigation",
        "label": "Show recorded comparison",
        "representation_result_boundary": "represent navigation to recorded comparison",
        "represented_source": {
            "identity": "source:operator-comparison-navigation",
            "kind": "operator-comparison-navigation",
            "source_role": "developer-supplied",
            "represented_result": "navigate to the recorded operator comparison",
            "reference": "tests.bounded_alternative_fixture",
        },
    },
)
