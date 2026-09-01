"""Exact source position and order: distinctions."""

from scripts.observe_source_position_path_discrimination import observe


def test_exact_paths_address_only_the_next_consecutive_coordinate():
    finding = observe()

    for layout in finding["layouts"].values():
        assert (
            layout["exact_next_coordinate_answer_count"]
            < layout["any_later_coordinate_answer_count"]
        )


def test_acquisition_packaging_changes_the_current_recurrence_results():
    finding = observe()
    assert finding["same_ordered_material_in_every_layout"] is True

    layouts = finding["layouts"]
    assert layouts["one_acquisition"]["distinct_exact_material_result_count"] == 143
    assert layouts["four_acquisitions"]["distinct_exact_material_result_count"] == 153
    assert (
        layouts["seventeen_byte_acquisitions"][
            "distinct_exact_material_result_count"
        ]
        == 8
    )
