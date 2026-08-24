from pathlib import Path
import sys


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from observe_inward_occurrence_surfaces import _surface  # noqa: E402


def test_scalar_values_do_not_choose_an_occurrence_coordinate_surface():
    coordinate_materials = {}
    first_exact, first_surface, *_ = _surface(
        {"alpha": "first", "beta": 1}, coordinate_materials
    )
    second_exact, second_surface, *_ = _surface(
        {"alpha": "second", "beta": 2}, coordinate_materials
    )

    assert first_surface == second_surface
    assert first_exact == second_exact


def test_immediate_container_count_does_not_change_coordinate_surface():
    coordinate_materials = {}
    first_exact, first_surface, *_ = _surface(
        {"alpha": ["first"]}, coordinate_materials
    )
    second_exact, second_surface, *_ = _surface(
        {"alpha": ["first", "second"]}, coordinate_materials
    )

    assert first_surface == second_surface
    assert first_exact != second_exact


def test_coordinate_material_changes_the_surface():
    coordinate_materials = {}
    _first_exact, first_surface, *_ = _surface(
        {"alpha": "same"}, coordinate_materials
    )
    _second_exact, second_surface, *_ = _surface(
        {"beta": "same"}, coordinate_materials
    )

    assert first_surface != second_surface
