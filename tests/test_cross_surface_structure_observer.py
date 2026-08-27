"""An exact source relation establishes one ordered result."""

from __future__ import annotations

import json
import sys
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from observe_cross_surface_structure import (  # noqa: E402
    SOURCE_GROUPS,
    _observe_group,
)


def _only_relation_walk(group: dict) -> dict:
    assert len(group["frame_relation_walks"]) == 1
    return group["frame_relation_walks"][0]


def test_four_sources_connect_one_exact_renaming_through_reversed_endpoints():
    group = _observe_group(0, SOURCE_GROUPS[0])
    walk = _only_relation_walk(group)

    assert group["exact_endpoint_frame_relation_count"] == 1
    assert walk["compatible_renaming_count"] == 1
    assert walk["middle_walk_count"] == 1
    connected = walk["compatible_renamings"][0]
    assert len(connected["anchor_pairs"]) == 3
    assert len(connected["renaming"]["material_renaming"]) == 8
    assert connected["renaming"]["preserves_source_order"] is True


def test_each_missing_or_changed_relation_remains_visible():
    without_later_sources = _observe_group(1, SOURCE_GROUPS[1])
    changed_larger_surface = _observe_group(2, SOURCE_GROUPS[2])
    changed_reversed_endpoints = _observe_group(3, SOURCE_GROUPS[3])
    first_later_source_only = _observe_group(6, SOURCE_GROUPS[6])
    second_later_source_only = _observe_group(7, SOURCE_GROUPS[7])

    assert without_later_sources["exact_material_renaming_count"] > 1
    assert without_later_sources["frame_relation_walks"] == []

    changed_walk = _only_relation_walk(changed_larger_surface)
    assert changed_walk["compatible_renaming_count"] == 0
    assert changed_walk["middle_walk_count"] == 0

    assert changed_reversed_endpoints["frame_relation_walks"] == []
    assert first_later_source_only["frame_relation_walks"] == []
    assert second_later_source_only["frame_relation_walks"] == []


def test_source_order_and_human_gloss_do_not_choose_the_structural_result():
    reordered = _observe_group(4, SOURCE_GROUPS[4])
    changed_gloss = _observe_group(5, SOURCE_GROUPS[5])
    with_other_material = _observe_group(8, SOURCE_GROUPS[8])

    reordered_walk = _only_relation_walk(reordered)
    assert reordered_walk["compatible_renaming_count"] == 1
    assert reordered_walk["compatible_renamings"][0]["renaming"][
        "preserves_source_order"
    ] is False

    changed_walk = _only_relation_walk(changed_gloss)
    assert changed_walk["compatible_renaming_count"] == 1
    assert changed_walk["middle_walk_count"] == 1
    assert changed_walk["compatible_renamings"][0]["renaming"][
        "preserves_source_order"
    ] is True

    original = _only_relation_walk(_observe_group(0, SOURCE_GROUPS[0]))
    other_material_walk = _only_relation_walk(with_other_material)
    assert other_material_walk["compatible_renaming_count"] == 1
    assert other_material_walk["compatible_renamings"][0]["renaming"][
        "material_renaming"
    ] == original["compatible_renamings"][0]["renaming"]["material_renaming"]

    frozen = json.dumps(changed_gloss, sort_keys=True)
    assert "one plus" not in frozen
    assert "is equal to" not in frozen
