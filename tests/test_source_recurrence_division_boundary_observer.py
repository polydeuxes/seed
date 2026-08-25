from scripts.observe_cross_surface_structure import SOURCE_GROUPS
from scripts.observe_source_recurrence_division_boundary import observe_sources


def test_live_recurrence_shape_does_not_supply_source_division():
    finding = observe_sources((b"a+aa+a", b"a+aa-a"))

    positive, changed = finding["sources"]
    assert positive["exact_material_result_count"] == 1
    assert positive["largest_exact_material_coordinate_count"] == 3
    assert positive["exact_material_results"][0]["occurrence_positions"] == [0, 3]
    assert changed["exact_material_result_count"] == 0


def test_bootstrap_sources_have_different_exact_material_findings():
    finding = observe_sources(SOURCE_GROUPS[0])

    assert [
        source["exact_material_result_count"] for source in finding["sources"]
    ] == [0, 128, 24, 1]
    assert [
        source["largest_exact_material_coordinate_count"]
        for source in finding["sources"]
    ] == [0, 19, 14, 3]
