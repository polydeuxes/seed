from __future__ import annotations

import sys
from pathlib import Path

import pytest


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from observe_cross_surface_rule_consequence import observe  # noqa: E402


@pytest.fixture(scope="module")
def observation() -> dict:
    return observe()


def _rule_result(finding: dict, first_conflicts: bool, second_conflicts: bool) -> dict:
    return next(
        rule_finding
        for rule_finding in finding["rule_findings"]
        if rule_finding["rule"]
        == {
            "same_first_changed_second_conflicts": first_conflicts,
            "changed_first_same_second_conflicts": second_conflicts,
        }
    )


def _extension_pattern(group: dict, first_conflicts: bool, second_conflicts: bool):
    return tuple(
        _rule_result(finding, first_conflicts, second_conflicts)["extension_count"]
        for finding in group["shared_relation_findings"]
    )


def test_every_rule_begins_later_work_with_the_same_two_exact_relations(
    observation: dict,
):
    assert observation["initial_shared_relation_count"] == 2
    assert all(
        len(group["shared_relation_findings"]) == 2
        for group in observation["consequence_groups"]
    )


def test_unchanged_material_keeps_all_directional_rules_compatible(
    observation: dict,
):
    unchanged = observation["consequence_groups"][0]

    for finding in unchanged["shared_relation_findings"]:
        for first_conflicts, second_conflicts in (
            (False, True),
            (True, False),
            (True, True),
        ):
            result = _rule_result(finding, first_conflicts, second_conflicts)
            assert result["compatible_count"] == 1
            assert result["extension_count"] == 0


def test_each_directional_repetition_distinguishes_the_answering_rule(
    observation: dict,
):
    same_first = observation["consequence_groups"][1]
    same_second = observation["consequence_groups"][2]

    assert sorted(_extension_pattern(same_first, False, True)) == [0, 1]
    assert sorted(_extension_pattern(same_first, True, False)) == [0, 1]
    assert _extension_pattern(same_first, True, True) == (0, 0)

    assert sorted(_extension_pattern(same_second, False, True)) == [0, 1]
    assert sorted(_extension_pattern(same_second, True, False)) == [0, 1]
    assert _extension_pattern(same_second, True, True) == (0, 0)


def test_both_directional_repetitions_leave_only_unrestricted_growth(
    observation: dict,
):
    both = observation["consequence_groups"][3]

    assert _extension_pattern(both, False, False) == (120, 120)
    assert _extension_pattern(both, False, True) == (0, 0)
    assert _extension_pattern(both, True, False) == (0, 0)
    assert _extension_pattern(both, True, True) == (0, 0)
