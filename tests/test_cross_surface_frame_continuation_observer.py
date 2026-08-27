"""A separate relation is established by exact material."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from observe_cross_surface_frame_continuation import observe  # noqa: E402


@pytest.fixture(scope="module")
def observed_groups() -> list[dict]:
    return observe()["groups"]


def _continuation_counts(group: dict) -> tuple[int, ...]:
    return tuple(
        relation["continuation_count"]
        for relation in group["frame_relation_continuations"]
    )


def _greatest_mapping_counts(group: dict) -> tuple[int, ...]:
    return tuple(
        relation["greatest_complete_mapping_count"]
        for relation in group["frame_relation_continuations"]
    )


def test_larger_structure_discriminates_two_exact_frame_relations(
    observed_groups: list[dict],
):
    groups = observed_groups

    assert tuple(group["frame_relation_count"] for group in groups) == (
        2,
        2,
        2,
        2,
    )
    assert _continuation_counts(groups[0]) == (2, 0)
    assert _greatest_mapping_counts(groups[0]) == (8, 0)
    assert _continuation_counts(groups[1]) == (0, 0)
    assert _continuation_counts(groups[2]) == (0, 2)
    assert _greatest_mapping_counts(groups[2]) == (0, 8)


def test_both_relations_continue_when_both_larger_structures_answer(
    observed_groups: list[dict],
):
    group = observed_groups[3]

    assert _continuation_counts(group) == (2, 2)
    assert _greatest_mapping_counts(group) == (8, 8)
    assert all(
        continuation["added_mapping_count"] == 5
        for relation in group["frame_relation_continuations"]
        for continuation in relation["continuations"]
    )
