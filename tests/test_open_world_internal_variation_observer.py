from pathlib import Path
import sys


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from observe_open_world_internal_variation import (  # noqa: E402
    _surface_classes,
    _variation_positions,
)


def _variation(materials: tuple[str, ...]):
    starts = tuple(range(len(materials) * 2))
    productions = tuple(
        (material, (2 * position, 2 * position + 1))
        for position, material in enumerate(materials)
    )
    scalar_materials = []
    variation_positions, recorded_productions = _variation_positions(
        surface=(-1, -1),
        starts=starts,
        recurrent_productions=productions,
        scalar_materials=scalar_materials,
        scalar_indexes_by_value={},
    )
    return variation_positions, recorded_productions, scalar_materials


def test_source_population_establishes_zero_one_or_many_varying_positions():
    no_variation, productions, _materials = _variation(("ab", "cd"))
    assert no_variation == ()
    assert productions == ()

    one_variation, _productions, _materials = _variation(("ab", "ac"))
    assert tuple(
        finding["coordinate_class_number"] for finding in one_variation
    ) == (1,)

    two_variations, productions, scalar_materials = _variation(
        ("ab", "ac", "db", "dc")
    )
    assert tuple(
        finding["coordinate_class_number"] for finding in two_variations
    ) == (0, 1)
    assert tuple(
        finding["source_coordinate_positions"] for finding in two_variations
    ) == ([0], [1])
    assert tuple(
        finding["recurrent_substitution_frame_count"]
        for finding in two_variations
    ) == (2, 2)
    assert len(productions) == 4
    assert len(scalar_materials) == 4


def test_repeated_coordinate_is_one_exact_coordinate_class():
    assert _surface_classes((-1, -1, 0)) == ((0, 2), (1,))
