#!/usr/bin/env python3
"""Read exact results that occupy later subject positions."""

from __future__ import annotations

from typing import Any

from scripts.exact_material_distinctions_reading import (
    exact_bounded_material_distinctions_reading,
)


def _results_by_occurrence(
    reading: dict[str, tuple[tuple[str, Any], ...]],
    surface: str,
) -> dict[str, Any]:
    results = reading.get(surface)
    if type(results) is not tuple:
        raise ValueError(f"{surface} is not one exact result population")
    by_occurrence = dict(results)
    if len(by_occurrence) != len(results):
        raise ValueError(f"{surface} repeats one result occurrence")
    return by_occurrence


def _occurrence_identity(reference: Any, *, coordinate: str) -> str:
    identity = (
        reference.get("recorded_occurrence_identity")
        if type(reference) is dict
        else None
    )
    if type(identity) is not str or not identity:
        raise ValueError(f"{coordinate} has no exact result occurrence")
    return identity


def _result_position_reference(
    reference: Any,
    *,
    coordinate: str,
) -> tuple[str, int]:
    identity = _occurrence_identity(reference, coordinate=coordinate)
    position = reference.get("result_position")
    if type(position) is not int or position < 0:
        raise ValueError(f"{coordinate} has no exact result position")
    return identity, position


def _pair_measurement_byte_result(
    pair_result_positions: Any,
) -> str:
    if type(pair_result_positions) is not tuple or not pair_result_positions:
        raise ValueError("pair Measurement has no exact result positions")
    references = pair_result_positions[0].referenced_result_position_references
    if len(references) != 1:
        raise ValueError("pair Measurement has no exact byte Measurement result")
    return _occurrence_identity(
        references[0],
        coordinate="pair Measurement byte-result reference",
    )


def _byte_measurement_material_results(
    byte_result_positions: Any,
) -> tuple[str, ...]:
    if type(byte_result_positions) is not tuple or not byte_result_positions:
        raise ValueError("byte Measurement has no exact result positions")
    subject = byte_result_positions[0].get("subject")
    references = (
        subject.get("source_occurrence_references")
        if type(subject) is dict
        else None
    )
    if type(references) is not list or not references:
        raise ValueError("byte Measurement has no exact material-result subjects")
    identities = tuple(
        reference.get("material_result_occurrence_identity")
        if type(reference) is dict
        else None
        for reference in references
    )
    if any(type(identity) is not str or not identity for identity in identities):
        raise ValueError("byte Measurement has malformed material-result subjects")
    return identities


def exact_result_subject_sequences(
    reading: dict[str, tuple[tuple[str, Any], ...]],
) -> tuple[dict[str, Any], ...]:
    """Resolve exact result occurrences reused as later exact subjects."""

    material_results = _results_by_occurrence(reading, "material_results")
    byte_measurements = _results_by_occurrence(
        reading,
        "byte_measurement_result_positions",
    )
    pair_measurements = _results_by_occurrence(
        reading,
        "pair_measurement_result_positions",
    )
    shared_position_results = _results_by_occurrence(
        reading,
        "shared_position_measurement_results",
    )
    pair_comparisons = _results_by_occurrence(reading, "pair_compare_results")
    shared_position_comparisons = _results_by_occurrence(reading, "shared_position_compare_results")
    distinctions = _results_by_occurrence(
        reading,
        "distinction_measurement_results",
    )

    sequences = []
    for distinction_identity, distinction in distinctions.items():
        shared_position_comparison_identity = distinction.get(
            "source_result_occurrence_identity"
        )
        shared_position_comparison = shared_position_comparisons.get(shared_position_comparison_identity)
        finding = (
            shared_position_comparison.get("finding")
            if type(shared_position_comparison) is dict
            else None
        )
        subject = finding.get("subject") if type(finding) is dict else None
        if type(subject) is not dict:
            raise ValueError("Distinction source has no exact Compare subjects")

        shared_position_reference = subject.get(
            "shared_position_result_position_reference"
        )
        shared_position_identity, shared_position_result_position = _result_position_reference(
            shared_position_reference,
            coordinate="shared-position Measurement result reference",
        )
        shared_position_result = shared_position_results.get(shared_position_identity)
        if type(shared_position_result) is not dict or shared_position_result_position != 0:
            raise ValueError("Compare has no exact shared-position result subject")

        pair_comparison_reference = subject.get(
            "recorded_pair_comparison_result_reference"
        )
        pair_comparison_identity = _occurrence_identity(
            pair_comparison_reference,
            coordinate="pair Compare result reference",
        )
        pair_comparison = pair_comparisons.get(pair_comparison_identity)
        if type(pair_comparison) is not dict:
            raise ValueError("shared-position Compare has no exact pair Compare result subject")

        result_positions = shared_position_result.get("result_positions")
        shared_position_result_position_content = (
            result_positions[0]
            if type(result_positions) is list and len(result_positions) == 1
            else None
        )
        if type(shared_position_result_position_content) is not dict:
            raise ValueError("shared-position Measurement has no exact result position")
        shared_position_subject = shared_position_result_position_content["subject"]
        first_position_reference = _result_position_reference(
            shared_position_subject.get("first_position_result_reference"),
            coordinate="first position Measurement result reference",
        )
        second_position_reference = _result_position_reference(
            shared_position_subject.get("second_position_result_reference"),
            coordinate="second position Measurement result reference",
        )
        source_material_result_identity = shared_position_result_position_content["content"].get(
            "source_material_result_occurrence_identity"
        )
        if source_material_result_identity not in material_results:
            raise ValueError("shared-position result has no exact material-result source")

        pair_binding = pair_comparison.get("subject_to_act_binding_reference")
        pair_subject = (
            pair_binding.get("subject_reference")
            if type(pair_binding) is dict
            else pair_comparison.get("subject_reference")
        )
        if type(pair_subject) is not dict:
            raise ValueError("pair Compare has no exact Measurement subjects")
        earlier_pair_identity = _occurrence_identity(
            pair_subject.get("earlier_measurement_reference"),
            coordinate="earlier pair Measurement result reference",
        )
        later_pair_identity = _occurrence_identity(
            pair_subject.get("later_measurement_reference"),
            coordinate="later pair Measurement result reference",
        )
        if (
            earlier_pair_identity not in pair_measurements
            or later_pair_identity not in pair_measurements
        ):
            raise ValueError("pair Compare subjects are absent")

        earlier_byte_identity = _pair_measurement_byte_result(
            pair_measurements[earlier_pair_identity]
        )
        later_byte_identity = _pair_measurement_byte_result(
            pair_measurements[later_pair_identity]
        )
        if (
            earlier_byte_identity not in byte_measurements
            or later_byte_identity not in byte_measurements
        ):
            raise ValueError("pair Measurement byte-result subjects are absent")

        first_pair = shared_position_result["first_position_result"]["exact_pair"]
        second_pair = shared_position_result["second_position_result"]["exact_pair"]
        if (
            type(first_pair) is not list
            or len(first_pair) != 2
            or type(second_pair) is not list
            or len(second_pair) != 2
            or first_pair[1] != second_pair[0]
        ):
            raise ValueError("shared-position result has malformed exact content")

        sequences.append(
            {
                "source_material_result_occurrence_identity": (
                    source_material_result_identity
                ),
                "ordered_content": bytes(
                    (first_pair[0], first_pair[1], second_pair[1])
                ),
                "ordered_positions": (
                    shared_position_result["first_position_result"]["first_position"],
                    shared_position_result["first_position_result"]["second_position"],
                    shared_position_result["second_position_result"]["second_position"],
                ),
                "first_position_measurement_result_reference": (
                    first_position_reference
                ),
                "second_position_measurement_result_reference": (
                    second_position_reference
                ),
                "shared_position_measurement_result_reference": (
                    shared_position_identity,
                    shared_position_result_position,
                ),
                "earlier_pair_measurement_result_occurrence_identity": (
                    earlier_pair_identity
                ),
                "later_pair_measurement_result_occurrence_identity": (
                    later_pair_identity
                ),
                "earlier_byte_measurement_result_occurrence_identity": (
                    earlier_byte_identity
                ),
                "later_byte_measurement_result_occurrence_identity": (
                    later_byte_identity
                ),
                "earlier_material_result_occurrence_identities": (
                    _byte_measurement_material_results(
                        byte_measurements[earlier_byte_identity]
                    )
                ),
                "later_material_result_occurrence_identities": (
                    _byte_measurement_material_results(
                        byte_measurements[later_byte_identity]
                    )
                ),
                "pair_compare_result_occurrence_identity": (
                    pair_comparison_identity
                ),
                "shared_position_compare_result_occurrence_identity": (
                    shared_position_comparison_identity
                ),
                "distinction_measurement_result_occurrence_identity": (
                    distinction_identity
                ),
            }
        )
    return tuple(sequences)


def exact_bounded_result_subject_reading(
    materials: tuple[bytes, ...],
    *,
    locality_identity: str = "exact-result-subject-reading",
) -> dict[str, Any]:
    """Read exact result-to-later-subject sequences without adding an occurrence."""

    reading = exact_bounded_material_distinctions_reading(
        materials,
        locality_identity=locality_identity,
    )
    return {
        "exact_reading": reading,
        "result_subject_sequences": exact_result_subject_sequences(reading),
    }
