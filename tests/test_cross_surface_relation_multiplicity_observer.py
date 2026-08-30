"""Bounded material: exact relation coordinates."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from observe_cross_surface_relation_multiplicity import observe  # noqa: E402


@pytest.fixture(scope="module")
def observed_groups() -> list[dict]:
    return observe()["groups"]


def _rule_counts(group: dict) -> dict[tuple[bool, bool], tuple[int, ...]]:
    return {
        (
            finding["rule"]["same_first_changed_second_conflicts"],
            finding["rule"]["changed_first_same_second_conflicts"],
        ): tuple(
            relation["continuation_count"]
            for relation in finding["relation_continuations"]
        )
        for finding in group["rule_findings"]
    }


def _orientation_counts(group: dict) -> dict[tuple[bool, bool], tuple[int, ...]]:
    return {
        (
            finding["rule"]["same_first_changed_second_conflicts"],
            finding["rule"]["changed_first_same_second_conflicts"],
        ): tuple(
            relation["orientation_count"]
            for relation in finding["relation_continuations"]
        )
        for finding in group["rule_findings"]
    }


def test_one_to_one_material_does_not_distinguish_three_directional_rules(
    observed_groups: list[dict],
):
    counts = _rule_counts(observed_groups[0])

    assert counts[(False, True)] == (2,)
    assert counts[(True, False)] == (2,)
    assert counts[(True, True)] == (2,)
    assert counts[(False, False)] == (240,)


def test_many_to_one_material_refuses_only_rules_that_forbid_its_orientation(
    observed_groups: list[dict],
):
    counts = _rule_counts(observed_groups[1])
    orientations = _orientation_counts(observed_groups[1])

    assert counts[(True, True)] == (0,)
    assert orientations[(True, True)] == (0,)
    assert counts[(True, False)] == (3,)
    assert counts[(False, True)] == (3,)
    assert orientations[(True, False)] == (1,)
    assert orientations[(False, True)] == (1,)


def test_unrestricted_pair_growth_adds_bridge_internal_continuations(
    observed_groups: list[dict],
):
    counts = _rule_counts(observed_groups[2])

    assert counts[(False, False)] == (4,)
    assert counts[(False, True)] == (0,)
    assert counts[(True, False)] == (0,)
    assert counts[(True, True)] == (0,)
