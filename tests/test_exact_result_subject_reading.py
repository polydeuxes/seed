"""Compare Measurement results establish exact Distinctions."""

from scripts.exact_result_subject_reading import (
    exact_bounded_result_subject_reading,
)


def test_exact_result_subjects_retain_material_and_result_coordinates():
    result = exact_bounded_result_subject_reading(
        (b"ab\n", b"ac\n"),
        locality_identity="test-exact-result-subject-reading",
    )
    reading = result["exact_reading"]
    sequences = result["result_subject_sequences"]

    assert len(sequences) == 1
    sequence = sequences[0]
    assert sequence["ordered_content"] == b"ac\n"
    assert sequence["ordered_positions"] == (0, 1, 2)

    ordered_material_identities = tuple(
        identity for identity, _result in reading["material_results"]
    )
    material_identities = set(ordered_material_identities)
    byte_measurement_identities = {
        identity
        for identity, _result in reading["byte_measurement_result_positions"]
    }
    pair_measurement_identities = {
        identity
        for identity, _result in reading["pair_measurement_result_positions"]
    }
    path_identities = {
        identity
        for identity, _result in reading[
            "ordered_relation_path_measurement_results"
        ]
    }
    pair_compare_identities = {
        identity for identity, _result in reading["pair_compare_results"]
    }
    path_compare_identities = {
        identity for identity, _result in reading["path_compare_results"]
    }
    distinction_identities = {
        identity
        for identity, _result in reading["distinction_measurement_results"]
    }

    assert sequence["path_source_material_result_occurrence_identity"] in (
        material_identities
    )
    assert sequence[
        "earlier_byte_measurement_result_occurrence_identity"
    ] in byte_measurement_identities
    assert sequence[
        "later_byte_measurement_result_occurrence_identity"
    ] in byte_measurement_identities
    assert sequence[
        "earlier_pair_measurement_result_occurrence_identity"
    ] in pair_measurement_identities
    assert sequence[
        "later_pair_measurement_result_occurrence_identity"
    ] in pair_measurement_identities
    assert sequence["ordered_path_measurement_result_reference"][0] in (
        path_identities
    )
    assert sequence["pair_compare_result_occurrence_identity"] in (
        pair_compare_identities
    )
    assert sequence["path_compare_result_occurrence_identity"] in (
        path_compare_identities
    )
    assert sequence["distinction_measurement_result_occurrence_identity"] in (
        distinction_identities
    )
    assert sequence["earlier_material_result_occurrence_identities"] == (
        ordered_material_identities[:1]
    )
    assert sequence["later_material_result_occurrence_identities"] == (
        ordered_material_identities
    )


def test_one_compare_result_occupies_multiple_later_compare_bindings():
    result = exact_bounded_result_subject_reading(
        (b"abcd", b"abce"),
        locality_identity="test-exact-result-subject-fan-out",
    )
    sequences = result["result_subject_sequences"]

    assert len(sequences) == 2
    assert len(
        {
            sequence["pair_compare_result_occurrence_identity"]
            for sequence in sequences
        }
    ) == 1
    assert len(
        {
            sequence["ordered_path_measurement_result_reference"]
            for sequence in sequences
        }
    ) == 2
    assert len(
        {
            sequence["path_compare_result_occurrence_identity"]
            for sequence in sequences
        }
    ) == 2
    assert len(
        {
            sequence["distinction_measurement_result_occurrence_identity"]
            for sequence in sequences
        }
    ) == 2
