from scripts.observe_acquisition_distinction import observe


def test_equal_material_does_not_collapse_exact_source_occurrences():
    finding = observe()

    assert finding["equal_material_has_one_private_reference"] is True
    assert finding["equal_material_retains_two_exact_source_occurrences"] is True
    assert finding["two_occurrences_double_each_byte_count"] is True


def test_private_material_reference_is_not_a_source_occurrence_coordinate():
    finding = observe()
    two = finding["two_source_occurrences"]

    assert two["private_exact_material_reference_is_carried_by_source_occurrence"] is False
    assert two["distinct_result_identity_count"] == 2
    assert two["distinct_Responsibility_assignment_count"] == 2
    assert two["distinct_Act_occurrence_count"] == 2
    assert two["distinct_Yield_count"] == 2
    assert two["Measurement_result_carried_in_current_Standing"] is True
