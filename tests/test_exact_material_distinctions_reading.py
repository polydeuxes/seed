"""Compare Measurement results establish exact Distinctions."""

from scripts.exact_material_distinctions_reading import (
    exact_bounded_material_distinctions_reading,
    exact_bounded_material_result_content_reading,
    exact_material_distinctions_reading,
    exact_material_result_content_reading,
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
    assert "pair_compare_applicability_results" not in reading
    assert len(reading["pair_compare_results"]) == 1
    path_applicability = reading["shared_position_compare_applicability_results"]
    assert len(path_applicability) == 2
    assert sorted(
        result["applicability"] for _identity, result in path_applicability
    ) == ["applicable", "inapplicable"]
    assert len(reading["shared_position_compare_results"]) == 1
    assert len(reading["distinction_measurement_results"]) == 1

    comparison_result_identity = reading["shared_position_compare_results"][0][0]
    distinction = reading["distinction_measurement_results"][0][1]
    assert distinction["source_result_occurrence_identity"] == comparison_result_identity
    assert distinction["completeness_boundary"] == {
        "source_result_occurrence_identity": comparison_result_identity,
        "distinction_count": len(distinction["findings"]),
    }


def test_result_content_uses_source_positions_without_cross_reading_identities():
    reading = exact_material_result_content_reading(
        (b"ab\n", b"ac\n"),
        (b"ab\n", b"ax\n"),
    )

    material = reading["result_content"]["material_results"]
    assert material["same"] == (("material_result", 0),)
    assert tuple(coordinate for coordinate, _content in material["first"]) == (
        ("material_result", 1),
    )
    assert tuple(coordinate for coordinate, _content in material["second"]) == (
        ("material_result", 1),
    )
    assert material["first"][0][1]["exact_material"] == b"ac\n"
    assert material["second"][0][1]["exact_material"] == b"ax\n"

    pair_compare = reading["result_content"]["pair_compare_results"]
    assert pair_compare["same"] == ()
    assert pair_compare["first"][0][0] == (
        "pair_Compare_result",
        (0,),
        (0, 1),
    )
    assert pair_compare["second"][0][0] == (
        "pair_Compare_result",
        (0,),
        (0, 1),
    )


def test_exact_material_boundaries_do_not_add_delimiter_content():
    materials = (b"ab", b"cd")

    reading = exact_bounded_material_distinctions_reading(
        materials,
        locality_identity="test-exact-bounded-material-reading",
    )

    assert tuple(
        result["exact_material"]
        for _identity, result in reading["material_results"]
    ) == materials


def test_equal_complete_content_remains_exact_under_different_boundaries():
    first = (b"abcd",)
    second = (b"ab", b"cd")

    reading = exact_bounded_material_result_content_reading(first, second)

    assert b"".join(
        result["exact_material"]
        for _identity, result in reading["first_exact_reading"]["material_results"]
    ) == b"".join(
        result["exact_material"]
        for _identity, result in reading["second_exact_reading"]["material_results"]
    )
    assert len(reading["first_exact_reading"]["material_results"]) == 1
    assert len(reading["second_exact_reading"]["material_results"]) == 2


def test_ordered_path_reading_preserves_exact_content_and_source_occurrence():
    one_source = exact_bounded_material_distinctions_reading(
        (b"ATCATC",),
        locality_identity="test-one-source-ordered-shared_position-reading",
    )
    two_sources = exact_bounded_material_distinctions_reading(
        (b"ATC", b"ATC"),
        locality_identity="test-two-source-ordered-shared_position-reading",
    )

    def atc_paths(reading):
        return tuple(
            shared_position
            for _identity, shared_position in reading[
                "shared_position_measurement_results"
            ]
            if shared_position["first_position_result"]["exact_pair"] == [65, 84]
            and shared_position["second_position_result"]["exact_pair"] == [84, 67]
        )

    one_source_paths = atc_paths(one_source)
    two_source_paths = atc_paths(two_sources)

    assert tuple(
        shared_position["first_position_result"]["first_position"]
        for shared_position in one_source_paths
    ) == (0, 3)
    assert tuple(
        shared_position["first_position_result"]["first_position"]
        for shared_position in two_source_paths
    ) == (0, 0)
    assert len(
        {
            shared_position["result_positions"][0]["content"][
                "source_material_result_occurrence_identity"
            ]
            for shared_position in one_source_paths
        }
    ) == 1
    assert len(
        {
            shared_position["result_positions"][0]["content"][
                "source_material_result_occurrence_identity"
            ]
            for shared_position in two_source_paths
        }
    ) == 2
