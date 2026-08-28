#!/usr/bin/env python3
"""Investigate exact recurrent material pairs without assigning meaning."""

from __future__ import annotations

from dataclasses import dataclass

from compiled_format_invocation import (
    ExactPositionMaterialReference,
    ExactPositionPairMaterialReference,
)
from compiled_material_invocation import MaterialAcquisitionResultReference
from seed_runtime.byte_measurement import (
    BYTE_PAIR_MEASUREMENT_RECORDED_KIND,
    assertions_of_recorded_byte_position_pair_measurement,
    get_byte_position_pair_measurement_subject_to_act_binding,
)
from seed_runtime.events import EventLedger


@dataclass(frozen=True, slots=True)
class ExactReferenceToRecurrentMaterialPair:
    recorded_occurrence_identity: str
    recurrence_result_position: int
    count_result_position: int
    locality_identity: str
    source_occurrence_identities: tuple[str, ...]
    completeness_boundary_identity: str
    exact_material: bytes

    def __post_init__(self) -> None:
        if (
            type(self.recorded_occurrence_identity) is not str
            or not self.recorded_occurrence_identity
            or type(self.recurrence_result_position) is not int
            or self.recurrence_result_position < 0
            or type(self.count_result_position) is not int
            or self.count_result_position < 0
            or self.recurrence_result_position == self.count_result_position
            or type(self.locality_identity) is not str
            or not self.locality_identity
            or type(self.source_occurrence_identities) is not tuple
            or not self.source_occurrence_identities
            or len(set(self.source_occurrence_identities))
            != len(self.source_occurrence_identities)
            or any(
                type(identity) is not str or not identity
                for identity in self.source_occurrence_identities
            )
            or type(self.completeness_boundary_identity) is not str
            or not self.completeness_boundary_identity
            or type(self.exact_material) is not bytes
            or len(self.exact_material) != 2
        ):
            raise TypeError(
                "recurrent pair requires its exact yielded Assertion reference"
            )

    @property
    def pair_identity(self) -> tuple[str, int]:
        return (
            self.recorded_occurrence_identity,
            self.recurrence_result_position,
        )


def exact_references_to_recurrent_material_pairs(
    ledger: EventLedger,
    measurement_occurrence_identity: str,
) -> tuple[ExactReferenceToRecurrentMaterialPair, ...]:
    """Read pair subjects whose exact Measurement established recurrence."""

    if not isinstance(ledger, EventLedger):
        raise TypeError("recurrent pair references require one EventLedger")
    event = ledger.get(measurement_occurrence_identity)
    if event is None or event.kind != BYTE_PAIR_MEASUREMENT_RECORDED_KIND:
        raise ValueError("recurrent pair references require one pair Measurement")
    assertions = assertions_of_recorded_byte_position_pair_measurement(
        ledger, measurement_occurrence_identity
    )
    reference = event.material["subject_to_act_binding_reference"]
    assignment = get_byte_position_pair_measurement_subject_to_act_binding(
        ledger, reference["recorded_occurrence_identity"]
    ).material
    source_occurrence_identities = tuple(
        reference["material_acquisition_result_occurrence_identity"]
        for reference in assignment["source_occurrence_references"]
    )
    completeness_boundary_identity = event.material["completeness_boundary"][
        "identity"
    ]
    found = []
    for assertion in assertions or ():
        if assertion.result != "recurrence" or assertion.content is None:
            continue
        support = assertion.support_assertion_references
        if (
            len(support) != 1
            or support[0].get("recorded_occurrence_identity") != event.identity
            or type(support[0].get("assertion_position")) is not int
            or support[0]["assertion_position"] < 0
        ):
            raise ValueError("recurrent pair carries no exact count Assertion support")
        found.append(
            ExactReferenceToRecurrentMaterialPair(
                recorded_occurrence_identity=event.identity,
                recurrence_result_position=assertion.assertion_position,
                count_result_position=support[0]["assertion_position"],
                locality_identity=event.locality_identity,
                source_occurrence_identities=source_occurrence_identities,
                completeness_boundary_identity=completeness_boundary_identity,
                exact_material=bytes(assertion.content),
            )
        )
    return tuple(found)


@dataclass(frozen=True, slots=True)
class ExactSubjectOfRecurrentMaterialPair:
    reference_to_recurrent_material_pair: ExactReferenceToRecurrentMaterialPair
    premise_occurrences_of_material_pair: tuple[ExactPositionPairMaterialReference, ...]

    def __post_init__(self) -> None:
        if (
            type(self.reference_to_recurrent_material_pair)
            is not ExactReferenceToRecurrentMaterialPair
            or type(self.premise_occurrences_of_material_pair) is not tuple
            or len(self.premise_occurrences_of_material_pair) < 2
            or any(
                type(occurrence) is not ExactPositionPairMaterialReference
                for occurrence in self.premise_occurrences_of_material_pair
            )
        ):
            raise TypeError("pair subject requires one exact reference and occurrences")
        if len(
            {
                occurrence.occurrence_identity
                for occurrence in self.premise_occurrences_of_material_pair
            }
        ) != len(self.premise_occurrences_of_material_pair):
            raise ValueError("pair premise occurrence entered twice")
        expected = self.reference_to_recurrent_material_pair.exact_material
        if any(
            occurrence.locality_identity
            != self.reference_to_recurrent_material_pair.locality_identity
            or occurrence.exact_material != expected
            for occurrence in self.premise_occurrences_of_material_pair
        ):
            raise ValueError("pair premise differs from its exact yielded subject")

    @property
    def pair_identity(self) -> tuple[str, str]:
        return self.reference_to_recurrent_material_pair.pair_identity


@dataclass(frozen=True, slots=True)
class ExactOccurrenceOfMaterialPair:
    subject_of_recurrent_material_pair: ExactSubjectOfRecurrentMaterialPair
    first_occurrence_reference: ExactPositionMaterialReference
    second_occurrence_reference: ExactPositionMaterialReference

    def __post_init__(self) -> None:
        if (
            type(self.subject_of_recurrent_material_pair) is not ExactSubjectOfRecurrentMaterialPair
            or type(self.first_occurrence_reference)
            is not ExactPositionMaterialReference
            or type(self.second_occurrence_reference)
            is not ExactPositionMaterialReference
        ):
            raise TypeError(
                "pair occurrence requires its exact subject and positions"
            )
        first = self.first_occurrence_reference
        second = self.second_occurrence_reference
        if (
            first.source_reference != second.source_reference
            or first.locality_identity
            != self.subject_of_recurrent_material_pair
            .reference_to_recurrent_material_pair.locality_identity
            or first.exact_material
            != self.subject_of_recurrent_material_pair
            .reference_to_recurrent_material_pair.exact_material[:1]
            or second.exact_material
            != self.subject_of_recurrent_material_pair
            .reference_to_recurrent_material_pair.exact_material[1:]
        ):
            raise ValueError("pair occurrence differs from its exact participants")
        if first.position == second.position:
            raise ValueError("pair participants require distinct exact positions")

    @property
    def pair_identity(self):
        return self.subject_of_recurrent_material_pair.pair_identity

    @property
    def locality_identity(self) -> str:
        return self.first_occurrence_reference.locality_identity

    @property
    def direction(self) -> str:
        return (
            "after"
            if self.second_occurrence_reference.position
            > self.first_occurrence_reference.position
            else "before"
        )

    @property
    def displacement(self) -> int:
        return abs(
            self.second_occurrence_reference.position
            - self.first_occurrence_reference.position
        )

    @property
    def occurrence_identity(self):
        return (
            self.first_occurrence_reference.source_reference,
            self.first_occurrence_reference.position,
            self.second_occurrence_reference.position,
        )


@dataclass(frozen=True, slots=True)
class ExactPositionPremiseOfRecurrentMaterialPair:
    boundary_identity: str
    subject_of_recurrent_material_pair: ExactSubjectOfRecurrentMaterialPair
    occurrences_supporting_position_premise: tuple[ExactOccurrenceOfMaterialPair, ...]

    def __post_init__(self) -> None:
        if (
            type(self.boundary_identity) is not str
            or not self.boundary_identity
            or type(self.subject_of_recurrent_material_pair)
            is not ExactSubjectOfRecurrentMaterialPair
            or type(self.occurrences_supporting_position_premise) is not tuple
            or len(self.occurrences_supporting_position_premise) < 2
            or any(
                type(occurrence) is not ExactOccurrenceOfMaterialPair
                for occurrence in self.occurrences_supporting_position_premise
            )
        ):
            raise TypeError(
                "position premise of pair requires exact supporting occurrences"
            )
        if any(
            occurrence.subject_of_recurrent_material_pair != self.subject_of_recurrent_material_pair
            for occurrence in self.occurrences_supporting_position_premise
        ):
            raise ValueError(
                "position premise of pair has a different exact subject"
            )
        if len(
            {
                occurrence.occurrence_identity
                for occurrence in self.occurrences_supporting_position_premise
            }
        ) != len(self.occurrences_supporting_position_premise):
            raise ValueError("pair occurrence entered position premise twice")
        expected = tuple(
            (
                occurrence.first_occurrence_reference,
                occurrence.second_occurrence_reference,
            )
            for occurrence in self.occurrences_supporting_position_premise
        )
        carried = tuple(
            (reference.first_reference, reference.second_reference)
            for reference in (
                self.subject_of_recurrent_material_pair
                .premise_occurrences_of_material_pair
            )
        )
        if expected != carried:
            raise ValueError(
                "position premise of pair differs from its exact occurrence support"
            )

    @property
    def pair_identity(self):
        return self.subject_of_recurrent_material_pair.pair_identity

    @property
    def locality_identity(self) -> str:
        return (
            self.subject_of_recurrent_material_pair
            .reference_to_recurrent_material_pair.locality_identity
        )

    @property
    def relations_of_positions(self) -> tuple[tuple[str, int], ...]:
        found = []
        for occurrence in self.occurrences_supporting_position_premise:
            relation = (occurrence.direction, occurrence.displacement)
            if relation not in found:
                found.append(relation)
        return tuple(found)


@dataclass(frozen=True, slots=True)
class ExactCompareOccurrenceOfMaterialPair:
    boundary_identity: str
    occurrence_position: int
    position_premise_of_recurrent_material_pair: (
        ExactPositionPremiseOfRecurrentMaterialPair
    )
    current_occurrence_of_material_pair: ExactOccurrenceOfMaterialPair

    def __post_init__(self) -> None:
        if (
            type(self.boundary_identity) is not str
            or not self.boundary_identity
            or type(self.occurrence_position) is not int
            or self.occurrence_position < 0
            or type(self.position_premise_of_recurrent_material_pair)
            is not ExactPositionPremiseOfRecurrentMaterialPair
            or type(self.current_occurrence_of_material_pair) is not ExactOccurrenceOfMaterialPair
        ):
            raise TypeError("Compare requires exact pair occurrences and boundary")
        if (
            self.position_premise_of_recurrent_material_pair.pair_identity
            != self.current_occurrence_of_material_pair.pair_identity
            or self.position_premise_of_recurrent_material_pair.locality_identity
            != self.current_occurrence_of_material_pair.locality_identity
        ):
            raise ValueError("Compare cannot cross pair identities or Localities")
        current_source_identity = (
            self.current_occurrence_of_material_pair.first_occurrence_reference.source_reference
            .recorded_occurrence_identity
        )
        premise_source_identities = (
            self.position_premise_of_recurrent_material_pair
            .subject_of_recurrent_material_pair.reference_to_recurrent_material_pair
            .source_occurrence_identities
        )
        if current_source_identity in premise_source_identities:
            raise ValueError(
                "Compare requires material outside position premise support"
            )
        if (
            self.boundary_identity
            == self.position_premise_of_recurrent_material_pair.boundary_identity
        ):
            raise ValueError("position premise and Compare require distinct boundaries")

    @property
    def occurrence_identity(self) -> tuple[str, int]:
        return self.boundary_identity, self.occurrence_position

    @property
    def distinction(self) -> bool:
        return (
            self.current_occurrence_of_material_pair.direction,
            self.current_occurrence_of_material_pair.displacement,
        ) not in (
            self.position_premise_of_recurrent_material_pair
            .relations_of_positions
        )

    @property
    def matching_support_occurrence_identities(
        self,
    ) -> tuple[tuple[MaterialAcquisitionResultReference, int, int], ...]:
        current_relation = (
            self.current_occurrence_of_material_pair.direction,
            self.current_occurrence_of_material_pair.displacement,
        )
        return tuple(
            occurrence.occurrence_identity
            for occurrence in (
                self.position_premise_of_recurrent_material_pair
                .occurrences_supporting_position_premise
            )
            if (occurrence.direction, occurrence.displacement) == current_relation
        )


def exact_subjects_of_recurrent_adjacent_material_pairs(
    source_references: tuple[
        MaterialAcquisitionResultReference, ...
    ],
    pair_references: tuple[ExactReferenceToRecurrentMaterialPair, ...],
) -> tuple[ExactSubjectOfRecurrentMaterialPair, ...]:
    """Return yielded pair subjects with two resolved premise occurrences."""

    if (
        type(source_references) is not tuple
        or not source_references
        or any(
            type(reference) is not MaterialAcquisitionResultReference
            for reference in source_references
        )
    ):
        raise TypeError("pair subjects require exact source references")
    if len(set(source_references)) != len(source_references):
        raise ValueError("source reference entered pair investigation twice")
    if (
        type(pair_references) is not tuple
        or not pair_references
        or any(
            type(reference) is not ExactReferenceToRecurrentMaterialPair
            for reference in pair_references
        )
    ):
        raise TypeError("pair subjects require exact yielded pair references")
    by_material = {}
    for reference in pair_references:
        if reference.exact_material in by_material:
            raise ValueError("material entered yielded pair subjects twice")
        by_material[reference.exact_material] = reference
    locality = pair_references[0].locality_identity
    if any(reference.locality_identity != locality for reference in pair_references):
        raise ValueError("yielded pair subjects have distinct Localities")
    source_occurrence_identities = {
        reference.recorded_occurrence_identity for reference in source_references
    }
    if any(
        set(reference.source_occurrence_identities) != source_occurrence_identities
        for reference in pair_references
    ):
        raise ValueError("pair premises differ from the yielded source occurrences")

    premises: dict[bytes, list[ExactPositionPairMaterialReference]] = {}
    for source in source_references:
        exact = source.exact_material
        if source.locality_identity != locality:
            raise ValueError("pair source differs from its exact Locality material")
        for position in range(len(exact) - 1):
            material = exact[position : position + 2]
            if material not in by_material:
                continue
            found = premises.setdefault(material, [])
            if len(found) >= 2:
                continue
            first = ExactPositionMaterialReference(source, position, material[:1])
            second = ExactPositionMaterialReference(source, position + 1, material[1:])
            found.append(ExactPositionPairMaterialReference(first, second, material))
    return tuple(
        ExactSubjectOfRecurrentMaterialPair(
            reference_to_recurrent_material_pair=by_material[material],
            premise_occurrences_of_material_pair=tuple(found),
        )
        for material, found in premises.items()
        if len(found) >= 2
    )


def exact_occurrences_of_material_pair(
    subject_of_recurrent_material_pair: ExactSubjectOfRecurrentMaterialPair,
    source_reference: MaterialAcquisitionResultReference,
) -> tuple[ExactOccurrenceOfMaterialPair, ...]:
    """Enumerate every ordered occurrence of one evidenced pair in one source."""

    if type(subject_of_recurrent_material_pair) is not ExactSubjectOfRecurrentMaterialPair:
        raise TypeError("pair occurrences require one exact subject")
    if type(source_reference) is not MaterialAcquisitionResultReference:
        raise TypeError("pair occurrences require one exact source reference")
    exact = source_reference.exact_material
    if (
        source_reference.locality_identity
        != subject_of_recurrent_material_pair.reference_to_recurrent_material_pair.locality_identity
    ):
        raise ValueError("pair occurrence source has a different Locality")
    exact_pair_material = (
        subject_of_recurrent_material_pair
        .reference_to_recurrent_material_pair.exact_material
    )
    first_material = exact_pair_material[:1]
    second_material = exact_pair_material[1:]
    first_positions = tuple(
        position
        for position, material in enumerate(exact)
        if bytes((material,)) == first_material
    )
    second_positions = tuple(
        position
        for position, material in enumerate(exact)
        if bytes((material,)) == second_material
    )
    found = []
    for first_position in first_positions:
        for second_position in second_positions:
            if first_position == second_position:
                continue
            found.append(
                ExactOccurrenceOfMaterialPair(
                    subject_of_recurrent_material_pair=subject_of_recurrent_material_pair,
                    first_occurrence_reference=ExactPositionMaterialReference(
                        source_reference, first_position, first_material
                    ),
                    second_occurrence_reference=ExactPositionMaterialReference(
                        source_reference, second_position, second_material
                    ),
                )
            )
    return tuple(found)


def exact_position_premise_of_recurrent_material_pair(
    subject_of_recurrent_material_pair: ExactSubjectOfRecurrentMaterialPair,
    *,
    boundary_identity: str,
) -> ExactPositionPremiseOfRecurrentMaterialPair:
    """Carry exact recurrent-pair position support at one boundary."""

    if type(subject_of_recurrent_material_pair) is not ExactSubjectOfRecurrentMaterialPair:
        raise TypeError("position premise of pair requires one exact subject")
    occurrences_supporting_position_premise = tuple(
        ExactOccurrenceOfMaterialPair(
            subject_of_recurrent_material_pair=subject_of_recurrent_material_pair,
            first_occurrence_reference=reference.first_reference,
            second_occurrence_reference=reference.second_reference,
        )
        for reference in subject_of_recurrent_material_pair.premise_occurrences_of_material_pair
    )
    return ExactPositionPremiseOfRecurrentMaterialPair(
        boundary_identity=boundary_identity,
        subject_of_recurrent_material_pair=subject_of_recurrent_material_pair,
        occurrences_supporting_position_premise=occurrences_supporting_position_premise,
    )


def compare_occurrences_of_material_pair(
    position_premise_of_recurrent_material_pair: (
        ExactPositionPremiseOfRecurrentMaterialPair
    ),
    current_occurrences: tuple[ExactOccurrenceOfMaterialPair, ...],
    *,
    boundary_identity: str,
) -> tuple[ExactCompareOccurrenceOfMaterialPair, ...]:
    """Compare current coordinates with one exact bounded position premise."""

    if (
        type(position_premise_of_recurrent_material_pair)
        is not ExactPositionPremiseOfRecurrentMaterialPair
        or type(current_occurrences) is not tuple
        or not current_occurrences
        or any(
            type(occurrence) is not ExactOccurrenceOfMaterialPair
            for occurrence in current_occurrences
        )
    ):
        raise TypeError("Compare requires exact pair occurrences")
    return tuple(
        ExactCompareOccurrenceOfMaterialPair(
            boundary_identity=boundary_identity,
            occurrence_position=position,
            position_premise_of_recurrent_material_pair=(
                position_premise_of_recurrent_material_pair
            ),
            current_occurrence_of_material_pair=current,
        )
        for position, current in enumerate(current_occurrences)
    )
