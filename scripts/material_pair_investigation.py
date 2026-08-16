#!/usr/bin/env python3
"""Investigate exact recurrent material pairs without assigning meaning."""

from __future__ import annotations

from dataclasses import dataclass

from compiled_format_invocation import (
    ExactPositionMaterialReference,
    ExactPositionPairMaterialReference,
)
from compiled_material_invocation import IngestResultReference
from seed_runtime.byte_measurement import (
    BYTE_PAIR_MEASUREMENT_RECORDED_KIND,
    assertions_of_recorded_byte_position_pair_measurement,
)
from seed_runtime.events import EventLedger


@dataclass(frozen=True, slots=True)
class ExactRecurrentMaterialPairReference:
    recorded_occurrence_identity: str
    recurrence_assertion_identity: str
    count_assertion_identity: str
    locality_identity: str
    source_occurrence_identities: tuple[str, ...]
    completeness_boundary_identity: str
    exact_material: bytes

    def __post_init__(self) -> None:
        if (
            type(self.recorded_occurrence_identity) is not str
            or not self.recorded_occurrence_identity
            or type(self.recurrence_assertion_identity) is not str
            or not self.recurrence_assertion_identity
            or type(self.count_assertion_identity) is not str
            or not self.count_assertion_identity
            or self.recurrence_assertion_identity == self.count_assertion_identity
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
    def pair_identity(self) -> tuple[str, str]:
        return (
            self.recorded_occurrence_identity,
            self.recurrence_assertion_identity,
        )


def exact_recurrent_material_pair_references(
    ledger: EventLedger,
    measurement_occurrence_identity: str,
) -> tuple[ExactRecurrentMaterialPairReference, ...]:
    """Read pair subjects whose exact Measurement established recurrence."""

    if not isinstance(ledger, EventLedger):
        raise TypeError("recurrent pair references require one EventLedger")
    event = ledger.get(measurement_occurrence_identity)
    if event is None or event.kind != BYTE_PAIR_MEASUREMENT_RECORDED_KIND:
        raise ValueError("recurrent pair references require one pair Measurement")
    assertions = assertions_of_recorded_byte_position_pair_measurement(
        ledger, measurement_occurrence_identity
    )
    assignment = event.material["responsibility_assignment_evidence"]
    source_occurrence_identities = tuple(
        reference["ingest_occurrence_identity"]
        for reference in assignment["source_occurrence_references"]
    )
    completeness_boundary_identity = event.material["completeness_boundary"][
        "identity"
    ]
    found = []
    for assertion in assertions or ():
        if assertion.result != "recurrence" or assertion.representation is None:
            continue
        support = assertion.support_assertion_references
        if (
            len(support) != 1
            or support[0].get("recorded_occurrence_identity") != event.identity
            or type(support[0].get("assertion_identity")) is not str
        ):
            raise ValueError("recurrent pair carries no exact count Assertion support")
        found.append(
            ExactRecurrentMaterialPairReference(
                recorded_occurrence_identity=event.identity,
                recurrence_assertion_identity=assertion.assertion_identity,
                count_assertion_identity=support[0]["assertion_identity"],
                locality_identity=event.locality_identity,
                source_occurrence_identities=source_occurrence_identities,
                completeness_boundary_identity=completeness_boundary_identity,
                exact_material=bytes(assertion.representation),
            )
        )
    return tuple(sorted(found, key=lambda reference: reference.exact_material))


@dataclass(frozen=True, slots=True)
class ExactMaterialPairCandidate:
    pair_reference: ExactRecurrentMaterialPairReference
    premise_occurrences: tuple[ExactPositionPairMaterialReference, ...]

    def __post_init__(self) -> None:
        if (
            type(self.pair_reference) is not ExactRecurrentMaterialPairReference
            or type(self.premise_occurrences) is not tuple
            or len(self.premise_occurrences) < 2
            or any(
                type(occurrence) is not ExactPositionPairMaterialReference
                for occurrence in self.premise_occurrences
            )
        ):
            raise TypeError("pair candidate requires one exact subject and occurrences")
        if len(
            {occurrence.occurrence_identity for occurrence in self.premise_occurrences}
        ) != len(self.premise_occurrences):
            raise ValueError("pair premise occurrence entered twice")
        expected = self.pair_reference.exact_material
        if any(
            occurrence.locality_identity != self.pair_reference.locality_identity
            or occurrence.exact_material != expected
            for occurrence in self.premise_occurrences
        ):
            raise ValueError("pair premise differs from its exact yielded subject")

    @property
    def pair_identity(self) -> tuple[str, str]:
        return self.pair_reference.pair_identity


@dataclass(frozen=True, slots=True)
class ExactMaterialPairOccurrence:
    pair_candidate: ExactMaterialPairCandidate
    first_occurrence_reference: ExactPositionMaterialReference
    second_occurrence_reference: ExactPositionMaterialReference

    def __post_init__(self) -> None:
        if (
            type(self.pair_candidate) is not ExactMaterialPairCandidate
            or type(self.first_occurrence_reference)
            is not ExactPositionMaterialReference
            or type(self.second_occurrence_reference)
            is not ExactPositionMaterialReference
        ):
            raise TypeError(
                "pair occurrence requires its exact candidate and positions"
            )
        first = self.first_occurrence_reference
        second = self.second_occurrence_reference
        if (
            first.source_reference != second.source_reference
            or first.locality_identity
            != self.pair_candidate.pair_reference.locality_identity
            or first.exact_material
            != self.pair_candidate.pair_reference.exact_material[:1]
            or second.exact_material
            != self.pair_candidate.pair_reference.exact_material[1:]
        ):
            raise ValueError("pair occurrence differs from its exact participants")
        if first.position == second.position:
            raise ValueError("pair participants require distinct exact positions")

    @property
    def pair_identity(self):
        return self.pair_candidate.pair_identity

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
class ExactMaterialPairCompareOccurrence:
    boundary_identity: str
    occurrence_position: int
    premise_occurrence: ExactMaterialPairOccurrence
    current_occurrence: ExactMaterialPairOccurrence

    def __post_init__(self) -> None:
        if (
            type(self.boundary_identity) is not str
            or not self.boundary_identity
            or type(self.occurrence_position) is not int
            or self.occurrence_position < 0
            or type(self.premise_occurrence) is not ExactMaterialPairOccurrence
            or type(self.current_occurrence) is not ExactMaterialPairOccurrence
        ):
            raise TypeError("Compare requires exact pair occurrences and boundary")
        if (
            self.premise_occurrence.pair_identity
            != self.current_occurrence.pair_identity
            or self.premise_occurrence.locality_identity
            != self.current_occurrence.locality_identity
        ):
            raise ValueError("Compare cannot cross pair identities or Localities")
        if (
            self.premise_occurrence.occurrence_identity
            == self.current_occurrence.occurrence_identity
        ):
            raise ValueError("Compare requires distinct pair occurrences")

    @property
    def occurrence_identity(self) -> tuple[str, int]:
        return self.boundary_identity, self.occurrence_position

    @property
    def distinction(self) -> bool:
        return (
            self.premise_occurrence.direction,
            self.premise_occurrence.displacement,
        ) != (
            self.current_occurrence.direction,
            self.current_occurrence.displacement,
        )


def recurrent_adjacent_pair_candidates(
    source_references: tuple[
        IngestResultReference, ...
    ],
    pair_references: tuple[ExactRecurrentMaterialPairReference, ...],
) -> tuple[ExactMaterialPairCandidate, ...]:
    """Return pairs with at least two exact adjacent premise occurrences."""

    if (
        type(source_references) is not tuple
        or not source_references
        or any(
            type(reference) is not IngestResultReference
            for reference in source_references
        )
    ):
        raise TypeError("pair candidates require exact source references")
    if len(set(source_references)) != len(source_references):
        raise ValueError("source reference entered pair investigation twice")
    if (
        type(pair_references) is not tuple
        or not pair_references
        or any(
            type(reference) is not ExactRecurrentMaterialPairReference
            for reference in pair_references
        )
    ):
        raise TypeError("pair candidates require exact yielded pair references")
    by_material = {}
    for reference in pair_references:
        if reference.exact_material in by_material:
            raise ValueError("material entered yielded pair subjects twice")
        by_material[reference.exact_material] = reference
    locality = pair_references[0].locality_identity
    if any(reference.locality_identity != locality for reference in pair_references):
        raise ValueError("yielded pair subjects crossed Localities")
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
        ExactMaterialPairCandidate(
            pair_reference=by_material[material],
            premise_occurrences=tuple(found),
        )
        for material, found in sorted(premises.items())
        if len(found) >= 2
    )


def exact_pair_occurrences(
    pair_candidate: ExactMaterialPairCandidate,
    source_reference: IngestResultReference,
) -> tuple[ExactMaterialPairOccurrence, ...]:
    """Enumerate every ordered occurrence of one evidenced pair in one source."""

    if type(pair_candidate) is not ExactMaterialPairCandidate:
        raise TypeError("pair occurrences require one exact candidate")
    if type(source_reference) is not IngestResultReference:
        raise TypeError("pair occurrences require one exact source reference")
    exact = source_reference.exact_material
    if (
        source_reference.locality_identity
        != pair_candidate.pair_reference.locality_identity
    ):
        raise ValueError("pair occurrence source crossed its exact Locality")
    first_material = pair_candidate.pair_reference.exact_material[:1]
    second_material = pair_candidate.pair_reference.exact_material[1:]
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
                ExactMaterialPairOccurrence(
                    pair_candidate=pair_candidate,
                    first_occurrence_reference=ExactPositionMaterialReference(
                        source_reference, first_position, first_material
                    ),
                    second_occurrence_reference=ExactPositionMaterialReference(
                        source_reference, second_position, second_material
                    ),
                )
            )
    return tuple(found)


def compare_pair_occurrences(
    pair_candidate: ExactMaterialPairCandidate,
    current_occurrences: tuple[ExactMaterialPairOccurrence, ...],
    *,
    boundary_identity: str,
) -> tuple[ExactMaterialPairCompareOccurrence, ...]:
    """Compare current ordered coordinates with one exact premise occurrence."""

    if (
        type(pair_candidate) is not ExactMaterialPairCandidate
        or type(current_occurrences) is not tuple
        or not current_occurrences
        or any(
            type(occurrence) is not ExactMaterialPairOccurrence
            for occurrence in current_occurrences
        )
    ):
        raise TypeError("Compare requires exact pair occurrences")
    premise_reference = pair_candidate.premise_occurrences[0]
    premise = ExactMaterialPairOccurrence(
        pair_candidate=pair_candidate,
        first_occurrence_reference=premise_reference.first_reference,
        second_occurrence_reference=premise_reference.second_reference,
    )
    return tuple(
        ExactMaterialPairCompareOccurrence(
            boundary_identity=boundary_identity,
            occurrence_position=position,
            premise_occurrence=premise,
            current_occurrence=current,
        )
        for position, current in enumerate(current_occurrences)
    )
