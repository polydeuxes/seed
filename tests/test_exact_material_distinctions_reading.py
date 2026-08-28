"""Exact material occurrences establish Distinctions."""

from scripts.exact_material_distinctions_reading import (
    exact_material_distinctions_reading,
)


def test_two_material_occurrences_have_established_result_readings():
    materials = (b"ab\n", b"ac\n")

    reading = exact_material_distinctions_reading(
        materials,
        locality_identity="test-exact-material-Distinctions-reading",
    )

    assert tuple(
        result["exact_material"]
        for _identity, result in reading["material_results"]
    ) == materials
    assert len(reading["byte_measurement_result_positions"]) == 2
    assert len(reading["pair_measurement_result_positions"]) == 2
    assert len(reading["pair_compare_applicability_results"]) == 1
    assert len(reading["pair_compare_results"]) == 1
    path_applicability = reading["path_compare_applicability_results"]
    assert len(path_applicability) == 2
    assert sorted(
        result["applicability"] for _identity, result in path_applicability
    ) == ["applicable", "inapplicable"]
    assert len(reading["path_compare_results"]) == 1
    assert len(reading["distinction_measurement_results"]) == 1

    path_result_identity = reading["path_compare_results"][0][0]
    distinction = reading["distinction_measurement_results"][0][1]
    assert distinction["source_result_occurrence_identity"] == path_result_identity
    assert distinction["completeness_boundary"] == {
        "source_result_occurrence_identity": path_result_identity,
        "distinction_count": len(distinction["findings"]),
    }
