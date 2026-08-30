"""An exact subject boundary: separate results."""

from pathlib import Path
import sys


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from observe_open_world_consequence_asymmetry import (  # noqa: E402
    _frame_substitution_edge_coordinates,
    _immediate_outer_context_population,
    _source_carried_joint_frames,
)
from report_open_world_consequence_asymmetry import _effect_counts  # noqa: E402


def test_joint_frame_requires_a_complete_source_carried_substitution_square():
    complete = _source_carried_joint_frames(
        ((0, 2), (0, 3), (1, 2), (1, 3)), 0, 1
    )
    assert len(complete) == 1
    assert complete[0]["complete_substitution_square_count"] == 1
    assert len(complete[0]["cell_population"]) == 4

    assert _source_carried_joint_frames(
        ((0, 2), (0, 3), (1, 2)), 0, 1
    ) == ()


def test_fixed_other_classes_remain_part_of_the_joint_frame_boundary():
    frames = _source_carried_joint_frames(
        (
            (0, 9, 2),
            (0, 9, 3),
            (1, 9, 2),
            (1, 9, 3),
            (0, 8, 2),
            (0, 8, 3),
            (1, 8, 2),
            (1, 8, 3),
        ),
        0,
        2,
    )
    assert tuple(
        frame["fixed_coordinate_material_indexes"] for frame in frames
    ) == ([8], [9])


def test_immediate_consequence_preserves_left_right_and_joint_populations():
    population = _immediate_outer_context_population(
        "xabryabz", coordinate_count=2, starts=(1, 5)
    )
    assert population["_left_values"] == {"x", "y"}
    assert population["_right_values"] == {"r", "z"}
    assert population["_joint_values"] == {("x", "r"), ("y", "z")}


def test_each_coordinate_gets_its_own_substitution_edges():
    frame = _source_carried_joint_frames(
        ((0, 2), (0, 3), (1, 2), (1, 3)), 0, 1
    )[0]
    first_edges, second_edges = _frame_substitution_edge_coordinates(frame)
    assert len(first_edges) == 2
    assert len(second_edges) == 2
    assert {edge[0] for edge in first_edges} == {2, 3}
    assert {edge[0] for edge in second_edges} == {0, 1}


def test_controlled_square_compares_two_edges_for_each_coordinate():
    # Cell order is x0y0, x0y1, x1y0, x1y1.
    assert _effect_counts(["a", "a", "b", "b"], (0, 1, 2, 3)) == (2, 0)
    assert _effect_counts(["a", "b", "a", "b"], (0, 1, 2, 3)) == (0, 2)
    assert _effect_counts(["a", "b", "c", "d"], (0, 1, 2, 3)) == (2, 2)
