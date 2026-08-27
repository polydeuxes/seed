"""An exact relation establishes one ordered occurrence path."""

from __future__ import annotations

import sys
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from observe_inward_story_flows import (  # noqa: E402
    _adjacent_story_pairs,
    _artifact_order_controls,
    _edge_forms,
    _shared_internal_edge_forms,
    _story_neighbors,
    _story_occurrences,
)


def _source(source_number: int, identities: list[str]) -> dict:
    return {
        "source_number": source_number,
        "walk_identity_sha256s": identities,
        "walk_addresses": [
            [position, position + 1] for position in range(len(identities))
        ],
    }


def test_enforced_edges_follow_refusal_and_remain_distinct_from_unbound_edges():
    enforced, unbound = _edge_forms(
        {
            "coordinate_control_findings": [
                {
                    "first_walk_identity_sha256": "a",
                    "later_walk_identity_sha256": "b",
                    "refused": True,
                },
                {
                    "first_walk_identity_sha256": "b",
                    "later_walk_identity_sha256": "c",
                    "refused": False,
                },
            ],
            "unbound_transitions": [
                {
                    "first_walk_identity_sha256": "c",
                    "later_walk_identity_sha256": "d",
                }
            ],
        }
    )

    assert enforced == {("a", "b")}
    assert unbound == {("c", "d")}


def test_maximal_enforced_walks_become_opaque_story_occurrences():
    source = _source(0, ["a", "b", "c", "d"])
    stories = _story_occurrences(
        [source],
        {("a", "b"), ("b", "c")},
    )

    assert len(stories) == 1
    assert stories[0]["walk_identity_sha256s"] == ["a", "b", "c"]
    assert stories[0]["first_walk_position"] == 0
    assert stories[0]["later_walk_position"] == 3
    assert _story_neighbors(stories, [source]) == [
        {
            "source_number": 0,
            "story_identity_sha256": stories[0]["story_identity_sha256"],
            "preceding_walk": None,
            "later_walk": {
                "walk_identity_sha256": "d",
                "walk_address": [3, 4],
            },
        }
    ]


def test_separate_sources_do_not_create_story_to_story_adjacency():
    sources = [
        _source(0, ["a", "b", "c"]),
        _source(1, ["a", "b", "c"]),
    ]
    stories = _story_occurrences(sources, {("a", "b"), ("b", "c")})

    assert len(stories) == 2
    assert _adjacent_story_pairs(stories) == []
    assert _shared_internal_edge_forms(stories) == {("a", "b"), ("b", "c")}
    assert _artifact_order_controls(stories) == {
        "artifact_story_order_count": 2,
        "artifact_order_creates_source_transition": False,
        "reversed_artifact_order_creates_source_transition": False,
    }


def test_two_maximal_stories_in_one_source_are_detected_as_adjacent():
    source = _source(0, ["a", "b", "c", "d", "e", "f"])
    stories = _story_occurrences(
        [source],
        {("a", "b"), ("b", "c"), ("d", "e"), ("e", "f")},
    )

    assert [story["walk_identity_sha256s"] for story in stories] == [
        ["a", "b", "c"],
        ["d", "e", "f"],
    ]
    assert _adjacent_story_pairs(stories) == [
        {
            "source_number": 0,
            "first_story_identity_sha256": stories[0]["story_identity_sha256"],
            "later_story_identity_sha256": stories[1]["story_identity_sha256"],
        }
    ]
