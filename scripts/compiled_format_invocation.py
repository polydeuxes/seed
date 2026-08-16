#!/usr/bin/env python3

from __future__ import annotations

import ast
from dataclasses import dataclass
import io
import json
import plistlib
import tomllib
from typing import Callable, Hashable, Protocol, runtime_checkable
import xml.etree.ElementTree

from seed_runtime.byte_measurement import (
    ASSERTION_LOCALITY_MOVEMENT_KIND,
    BYTE_MEASUREMENT_RECORDED_KIND,
    BYTE_PAIR_MEASUREMENT_RECORDED_KIND,
    assertions_of_recorded_byte_measurement,
    assertions_of_recorded_byte_position_pair_measurement,
    move_recorded_byte_assertion_to_locality,
)
from seed_runtime.events import EventLedger

from material_admission import (
    AdmissionOccurrence,
    AdmissionResultReference,
    admission_occurrence,
)


@dataclass(frozen=True)
class CompiledImplementationFunction:
    identity: str
    invocation: Callable[[bytes], object]

    def __post_init__(self) -> None:
        if type(self.identity) is not str or not self.identity:
            raise TypeError("one exact implementation function identity is required")
        if not callable(self.invocation):
            raise TypeError("one exact implementation function is required")


@runtime_checkable
class ExactMaterialCoordinates(Protocol):
    exact_material: bytes


@dataclass(frozen=True, slots=True)
class ExactMaterialReference:
    recorded_occurrence_identity: str
    assertion_identity: str
    locality_identity: str
    exact_material: bytes
    locality_movement_event_identity: str | None = None

    def __post_init__(self) -> None:
        if (
            type(self.recorded_occurrence_identity) is not str
            or not self.recorded_occurrence_identity
            or type(self.assertion_identity) is not str
            or not self.assertion_identity
            or type(self.locality_identity) is not str
            or not self.locality_identity
            or type(self.exact_material) is not bytes
            or (
                self.locality_movement_event_identity is not None
                and (
                    type(self.locality_movement_event_identity) is not str
                    or not self.locality_movement_event_identity
                )
            )
        ):
            raise TypeError("exact material requires its occurrence-bound Assertion reference")


@dataclass(frozen=True, slots=True)
class ExactPositionMaterialReference:
    source_reference: ExactMaterialCoordinates
    position: int
    exact_material: bytes

    def __post_init__(self) -> None:
        if not _is_exact_material_coordinates(self.source_reference):
            raise TypeError("position material requires its exact source reference")
        if type(getattr(self.source_reference, "locality_identity", None)) is not str:
            raise TypeError("position material requires its exact source Locality")
        if (
            type(self.position) is not int
            or self.position < 0
            or self.position >= len(self.source_reference.exact_material)
        ):
            raise ValueError("position material requires one exact source position")
        if (
            type(self.exact_material) is not bytes
            or len(self.exact_material) != 1
            or self.source_reference.exact_material[
                self.position : self.position + 1
            ]
            != self.exact_material
        ):
            raise ValueError("position material differs from its exact source")

    @property
    def locality_identity(self) -> str:
        return self.source_reference.locality_identity

    @property
    def occurrence_identity(self):
        return (self.source_reference, self.position)

    @property
    def first_position(self) -> int:
        return self.position

    @property
    def last_position(self) -> int:
        return self.position


@dataclass(frozen=True, slots=True)
class ExactPositionPairMaterialReference:
    first_reference: ExactPositionMaterialReference | ExactPositionPairMaterialReference
    second_reference: ExactPositionMaterialReference | ExactPositionPairMaterialReference
    exact_material: bytes

    def __post_init__(self) -> None:
        if not isinstance(
            self.first_reference,
            (ExactPositionMaterialReference, ExactPositionPairMaterialReference),
        ) or not isinstance(
            self.second_reference,
            (ExactPositionMaterialReference, ExactPositionPairMaterialReference),
        ):
            raise TypeError("position pair requires exact position material")
        if self.first_reference.source_reference != self.second_reference.source_reference:
            raise ValueError("position pair cannot cross source material")
        if self.second_reference.first_position != self.first_reference.last_position + 1:
            raise ValueError("position pair does not preserve exact source order")
        if self.exact_material != (
            self.first_reference.exact_material + self.second_reference.exact_material
        ):
            raise ValueError("position pair differs from its exact source material")

    @property
    def source_reference(self):
        return self.first_reference.source_reference

    @property
    def locality_identity(self) -> str:
        return self.first_reference.locality_identity

    @property
    def first_position(self) -> int:
        return self.first_reference.first_position

    @property
    def last_position(self) -> int:
        return self.second_reference.last_position

    @property
    def occurrence_identity(self):
        return (
            self.source_reference,
            self.first_position,
            self.last_position,
        )


def exact_position_material_references(
    source_reference: ExactMaterialCoordinates,
) -> tuple[ExactPositionMaterialReference, ...]:
    if not _is_exact_material_coordinates(source_reference):
        raise TypeError("position material requires one exact source reference")
    if type(getattr(source_reference, "locality_identity", None)) is not str:
        raise TypeError("position material requires one exact source Locality")
    return tuple(
        ExactPositionMaterialReference(
            source_reference=source_reference,
            position=position,
            exact_material=source_reference.exact_material[position : position + 1],
        )
        for position in range(len(source_reference.exact_material))
    )


def exact_position_pair_material_references(
    position_references: tuple[
        ExactPositionMaterialReference | ExactPositionPairMaterialReference, ...
    ],
) -> tuple[ExactPositionPairMaterialReference, ...]:
    if type(position_references) is not tuple or any(
        not isinstance(
            reference,
            (ExactPositionMaterialReference, ExactPositionPairMaterialReference),
        )
        for reference in position_references
    ):
        raise TypeError("position pairs require exact position material")
    by_first_position = {}
    for reference in position_references:
        by_first_position.setdefault(reference.first_position, []).append(reference)
    return tuple(
        ExactPositionPairMaterialReference(
            first_reference=first,
            second_reference=second,
            exact_material=first.exact_material + second.exact_material,
        )
        for first in position_references
        for second in by_first_position.get(first.last_position + 1, ())
        if first.source_reference == second.source_reference
    )


def exact_byte_material_references(
    ledger: EventLedger, measurement_occurrence_identity: str
) -> tuple[ExactMaterialReference, ...]:
    if not isinstance(ledger, EventLedger):
        raise TypeError("exact byte material references require one EventLedger")
    event = ledger.get(measurement_occurrence_identity)
    if event is None or event.kind != BYTE_MEASUREMENT_RECORDED_KIND:
        raise ValueError("exact byte material references require one Measurement occurrence")
    assertions = assertions_of_recorded_byte_measurement(
        ledger, measurement_occurrence_identity
    )
    return tuple(
        ExactMaterialReference(
            recorded_occurrence_identity=assertion.recorded_occurrence_identity,
            assertion_identity=assertion.assertion_identity,
            locality_identity=event.locality_identity,
            exact_material=bytes((assertion.representation,)),
        )
        for assertion in assertions or ()
        if assertion.result == "count" and assertion.representation is not None
    )


def moved_exact_byte_material_references(
    ledger: EventLedger,
    measurement_occurrence_identity: str,
    *,
    destination_locality: str,
) -> tuple[ExactMaterialReference, ...]:
    if not isinstance(ledger, EventLedger):
        raise TypeError("moved exact byte references require one EventLedger")
    if type(destination_locality) is not str or not destination_locality:
        raise TypeError("moved exact byte references require one destination Locality")
    event = ledger.get(measurement_occurrence_identity)
    if event is None or event.kind != BYTE_MEASUREMENT_RECORDED_KIND:
        raise ValueError("moved exact byte references require one Measurement occurrence")
    assertions = assertions_of_recorded_byte_measurement(
        ledger, measurement_occurrence_identity
    )
    found = []
    for assertion in assertions or ():
        if assertion.result != "count" or assertion.representation is None:
            continue
        moved = move_recorded_byte_assertion_to_locality(
            ledger,
            source=assertion,
            destination_locality=destination_locality,
        )
        movement_identity = moved.locality_movement_event_identity
        if event.locality_identity == destination_locality:
            if movement_identity is not None:
                raise ValueError("same-Locality material acquired a movement")
        else:
            movement = ledger.get(movement_identity)
            if (
                movement is None
                or movement.kind != ASSERTION_LOCALITY_MOVEMENT_KIND
                or movement.locality_identity != destination_locality
                or movement.material.get("source_assertion_reference")
                != moved.reference
                or movement.material.get("destination_locality")
                != destination_locality
            ):
                raise ValueError("byte material movement is not exact")
        found.append(
            ExactMaterialReference(
                recorded_occurrence_identity=moved.recorded_occurrence_identity,
                assertion_identity=moved.assertion_identity,
                locality_identity=destination_locality,
                exact_material=bytes((moved.representation,)),
                locality_movement_event_identity=(
                    movement_identity
                ),
            )
        )
    return tuple(found)


def exact_byte_pair_material_references(
    ledger: EventLedger, measurement_occurrence_identity: str
) -> tuple[ExactMaterialReference, ...]:
    if not isinstance(ledger, EventLedger):
        raise TypeError("exact byte-pair material references require one EventLedger")
    event = ledger.get(measurement_occurrence_identity)
    if event is None or event.kind != BYTE_PAIR_MEASUREMENT_RECORDED_KIND:
        raise ValueError("exact byte-pair material references require one Measurement occurrence")
    assertions = assertions_of_recorded_byte_position_pair_measurement(
        ledger, measurement_occurrence_identity
    )
    return tuple(
        ExactMaterialReference(
            recorded_occurrence_identity=assertion.recorded_occurrence_identity,
            assertion_identity=assertion.assertion_identity,
            locality_identity=event.locality_identity,
            exact_material=bytes(assertion.representation),
        )
        for assertion in assertions or ()
        if assertion.result == "count" and assertion.representation is not None
    )


@dataclass(frozen=True, slots=True)
class ExactMaterialResultReference:
    act_occurrence_identity: tuple[str, int]
    result_identity: tuple[str, int, str]
    locality_identity: str
    exact_material: bytes
    source_admission_result_reference: AdmissionResultReference | None = None
    source_admitted_material_position: int | None = None
    added_admission_result_reference: AdmissionResultReference | None = None
    added_admitted_material_position: int | None = None
    admitted_material_act_occurrence_count_limit: int | None = None

    def __post_init__(self) -> None:
        if (
            type(self.act_occurrence_identity) is not tuple
            or len(self.act_occurrence_identity) != 2
            or type(self.act_occurrence_identity[0]) is not str
            or type(self.act_occurrence_identity[1]) is not int
            or type(self.result_identity) is not tuple
            or len(self.result_identity) != 3
            or self.result_identity[:2] != self.act_occurrence_identity
            or self.result_identity[2] != "result"
            or type(self.locality_identity) is not str
            or not self.locality_identity
            or type(self.exact_material) is not bytes
        ):
            raise TypeError("exact material result requires its Act occurrence and result identity")
        admission_coordinates = (
            self.source_admission_result_reference,
            self.source_admitted_material_position,
            self.added_admission_result_reference,
            self.added_admitted_material_position,
            self.admitted_material_act_occurrence_count_limit,
        )
        if any(coordinate is not None for coordinate in admission_coordinates):
            if not isinstance(
                self.source_admission_result_reference, AdmissionResultReference
            ) or not isinstance(
                self.added_admission_result_reference, AdmissionResultReference
            ):
                raise TypeError("material result requires its exact Admission results")
            if (
                type(self.source_admitted_material_position) is not int
                or self.source_admitted_material_position < 0
                or self.source_admitted_material_position
                >= len(self.source_admission_result_reference.admitted_material)
                or type(self.added_admitted_material_position) is not int
                or self.added_admitted_material_position < 0
                or self.added_admitted_material_position
                >= len(self.added_admission_result_reference.admitted_material)
            ):
                raise TypeError("material result requires its exact admitted positions")
            if (
                type(self.admitted_material_act_occurrence_count_limit) is not int
                or self.admitted_material_act_occurrence_count_limit < 1
            ):
                raise TypeError("material result requires its exact Act occurrence count limit")

    def __hash__(self) -> int:
        return hash(self.result_identity)


def _is_exact_material_coordinates(material: object) -> bool:
    from compiled_material_invocation import IngestResultReference

    return isinstance(
        material,
        (
            ExactMaterialReference,
            ExactMaterialResultReference,
            ExactPositionMaterialReference,
            ExactPositionPairMaterialReference,
            IngestResultReference,
        ),
    )


@dataclass(frozen=True, slots=True)
class CompiledInvocationResultReference:
    invocation_occurrence: "CompiledInvocationOccurrence"

    def __post_init__(self) -> None:
        if not isinstance(self.invocation_occurrence, CompiledInvocationOccurrence):
            raise TypeError("invocation result requires its exact Act occurrence")

    @property
    def act_occurrence_identity(self) -> tuple[str, str, int]:
        return self.invocation_occurrence.occurrence_identity

    @property
    def result_identity(self) -> tuple[str, str, int, str]:
        return (*self.act_occurrence_identity, "result")

    @property
    def coordinates(self) -> bool:
        return self.invocation_occurrence.returned


@dataclass(frozen=True, slots=True)
class AddedPositionOccurrence:
    boundary_identity: str
    locality_identity: str
    occurrence_position: int
    source_reference: ExactMaterialCoordinates
    position: int
    added_reference: ExactMaterialCoordinates
    result_material: bytes
    source_admission_result_reference: AdmissionResultReference | None = None
    source_admitted_material_position: int | None = None
    added_admission_result_reference: AdmissionResultReference | None = None
    added_admitted_material_position: int | None = None
    admitted_material_act_occurrence_count_limit: int | None = None

    def __post_init__(self) -> None:
        if type(self.boundary_identity) is not str or not self.boundary_identity:
            raise TypeError("one exact boundary identity is required")
        if type(self.locality_identity) is not str or not self.locality_identity:
            raise TypeError("addition Act requires one exact Locality")
        if type(self.occurrence_position) is not int or self.occurrence_position < 0:
            raise TypeError("one exact Act occurrence position is required")
        if not _is_exact_material_coordinates(self.source_reference):
            raise TypeError("source material requires its exact reference")
        if not _is_exact_material_coordinates(self.added_reference):
            raise TypeError("added material requires its exact reference")
        source_locality = getattr(self.source_reference, "locality_identity", None)
        added_locality = getattr(self.added_reference, "locality_identity", None)
        if (
            source_locality != self.locality_identity
            or added_locality != self.locality_identity
        ):
            raise ValueError("addition Act material crossed Localities")
        if len(self.added_reference.exact_material) != 1:
            raise ValueError("added material must be exactly one byte")
        if not preserves_original_order(
            source_material=self.source_reference.exact_material,
            result_material=self.result_material,
            added_position=self.position,
        ):
            raise ValueError("result material does not preserve its exact source order")
        if self.result_material[self.position : self.position + 1] != self.added_material:
            raise ValueError("result material does not carry the exact added material")
        admission_coordinates = (
            self.source_admission_result_reference,
            self.source_admitted_material_position,
            self.added_admission_result_reference,
            self.added_admitted_material_position,
            self.admitted_material_act_occurrence_count_limit,
        )
        if any(coordinate is not None for coordinate in admission_coordinates):
            if not isinstance(
                self.source_admission_result_reference, AdmissionResultReference
            ) or not isinstance(
                self.added_admission_result_reference, AdmissionResultReference
            ):
                raise TypeError("addition Act requires its exact Admission results")
            if (
                type(self.source_admitted_material_position) is not int
                or self.source_admitted_material_position < 0
                or self.source_admitted_material_position
                >= len(self.source_admission_result_reference.admitted_material)
                or type(self.added_admitted_material_position) is not int
                or self.added_admitted_material_position < 0
                or self.added_admitted_material_position
                >= len(self.added_admission_result_reference.admitted_material)
            ):
                raise TypeError("addition Act requires its exact admitted positions")
            if (
                type(self.admitted_material_act_occurrence_count_limit) is not int
                or self.admitted_material_act_occurrence_count_limit < 1
            ):
                raise TypeError("addition Act requires its exact occurrence count limit")
            source_admitted_material = (
                self.source_admission_result_reference.admitted_material[
                    self.source_admitted_material_position
                ]
            )
            added_admitted_material = (
                self.added_admission_result_reference.admitted_material[
                    self.added_admitted_material_position
                ]
            )
            if (
                self.source_reference not in source_admitted_material
                or self.added_reference not in added_admitted_material
            ):
                raise ValueError("addition Act material differs from its Admissions")

    def __hash__(self) -> int:
        return hash(self.act_occurrence_identity)

    @property
    def act_identity(self) -> tuple[str, str]:
        return (self.boundary_identity, "add exact material at exact position")

    @property
    def act_occurrence_identity(self) -> tuple[str, int]:
        return (self.boundary_identity, self.occurrence_position)

    @property
    def result_identity(self) -> tuple[str, int, str]:
        return (self.boundary_identity, self.occurrence_position, "result")

    @property
    def result_reference(self) -> ExactMaterialResultReference:
        return ExactMaterialResultReference(
            act_occurrence_identity=self.act_occurrence_identity,
            result_identity=self.result_identity,
            locality_identity=self.locality_identity,
            exact_material=self.result_material,
            source_admission_result_reference=self.source_admission_result_reference,
            source_admitted_material_position=self.source_admitted_material_position,
            added_admission_result_reference=self.added_admission_result_reference,
            added_admitted_material_position=self.added_admitted_material_position,
            admitted_material_act_occurrence_count_limit=(
                self.admitted_material_act_occurrence_count_limit
            ),
        )

    @property
    def source_material(self) -> bytes:
        return self.source_reference.exact_material

    @property
    def added_material(self) -> bytes:
        return self.added_reference.exact_material


@dataclass(frozen=True, slots=True)
class RemovedPositionOccurrence:
    boundary_identity: str
    locality_identity: str
    occurrence_position: int
    source_reference: ExactMaterialReference
    position: int
    removed_reference: ExactMaterialReference
    result_material: bytes

    def __post_init__(self) -> None:
        if type(self.boundary_identity) is not str or not self.boundary_identity:
            raise TypeError("one exact boundary identity is required")
        if type(self.locality_identity) is not str or not self.locality_identity:
            raise TypeError("removal Act requires one exact Locality")
        if type(self.occurrence_position) is not int or self.occurrence_position < 0:
            raise TypeError("one exact Act occurrence position is required")
        if not isinstance(self.source_reference, ExactMaterialReference):
            raise TypeError("source material requires its exact reference")
        if not isinstance(self.removed_reference, ExactMaterialReference):
            raise TypeError("removed material requires its exact reference")
        if (
            self.source_reference.locality_identity != self.locality_identity
            or self.removed_reference.locality_identity != self.locality_identity
        ):
            raise ValueError("removal Act material crossed Localities")
        if len(self.removed_reference.exact_material) != 1:
            raise ValueError("removed material must be exactly one byte")
        if (
            type(self.position) is not int
            or self.position < 0
            or self.position >= len(self.source_material)
            or self.source_material[self.position : self.position + 1]
            != self.removed_material
            or self.result_material
            != self.source_material[: self.position]
            + self.source_material[self.position + 1 :]
        ):
            raise ValueError("result material does not preserve the exact removal")

    @property
    def act_identity(self) -> tuple[str, str]:
        return (self.boundary_identity, "remove exact material at exact position")

    @property
    def act_occurrence_identity(self) -> tuple[str, int]:
        return (self.boundary_identity, self.occurrence_position)

    @property
    def result_identity(self) -> tuple[str, int, str]:
        return (self.boundary_identity, self.occurrence_position, "result")

    @property
    def result_reference(self) -> ExactMaterialResultReference:
        return ExactMaterialResultReference(
            act_occurrence_identity=self.act_occurrence_identity,
            result_identity=self.result_identity,
            locality_identity=self.locality_identity,
            exact_material=self.result_material,
        )

    @property
    def source_material(self) -> bytes:
        return self.source_reference.exact_material

    @property
    def removed_material(self) -> bytes:
        return self.removed_reference.exact_material


@dataclass(frozen=True, slots=True)
class CompiledInvocationOccurrence:
    boundary_identity: str
    invocation_position: int
    exact_material: bytes
    implementation_function: CompiledImplementationFunction
    returned: bool
    source_coordinate: (
        ExactMaterialCoordinates
        | AddedPositionOccurrence
        | RemovedPositionOccurrence
        | None
    ) = None

    def __post_init__(self) -> None:
        if type(self.boundary_identity) is not str or not self.boundary_identity:
            raise TypeError("one exact boundary identity is required")
        if type(self.invocation_position) is not int or self.invocation_position < 0:
            raise TypeError("one exact invocation position is required")
        if type(self.exact_material) is not bytes:
            raise TypeError("implementation function material must be exact bytes")
        if not isinstance(
            self.implementation_function, CompiledImplementationFunction
        ):
            raise TypeError("one exact compiled implementation function is required")
        if type(self.returned) is not bool:
            raise TypeError("returned coordinate must be exact")
        if self.source_coordinate is not None:
            if _is_exact_material_coordinates(self.source_coordinate):
                source_material = self.source_coordinate.exact_material
            elif isinstance(
                self.source_coordinate,
                (AddedPositionOccurrence, RemovedPositionOccurrence),
            ):
                source_material = self.source_coordinate.result_material
            else:
                raise TypeError("source material requires its exact reference")
            if source_material != self.exact_material:
                raise ValueError("invocation material differs from its exact source")

    @property
    def implementation_function_identity(self) -> str:
        return self.implementation_function.identity

    @property
    def result_identity(self) -> tuple[str, str, int, str]:
        return (*self.occurrence_identity, "result")

    @property
    def result_reference(self) -> CompiledInvocationResultReference:
        return CompiledInvocationResultReference(invocation_occurrence=self)

    @property
    def occurrence_identity(self) -> tuple[str, str, int]:
        return (
            self.boundary_identity,
            self.implementation_function_identity,
            self.invocation_position,
        )

    @property
    def source_material(self) -> bytes | None:
        if _is_exact_material_coordinates(self.source_coordinate):
            return self.source_coordinate.exact_material
        if isinstance(self.source_coordinate, AddedPositionOccurrence):
            return self.source_coordinate.source_material
        if isinstance(self.source_coordinate, RemovedPositionOccurrence):
            return self.source_coordinate.source_material
        return None

    @property
    def added_position(self) -> int | None:
        return (
            self.source_coordinate.position
            if isinstance(self.source_coordinate, AddedPositionOccurrence)
            else None
        )

    @property
    def added_material(self) -> bytes | None:
        return (
            self.source_coordinate.added_material
            if isinstance(self.source_coordinate, AddedPositionOccurrence)
            else None
        )


@dataclass(frozen=True, slots=True)
class AddedPositionCompareOccurrence:
    boundary_identity: str
    occurrence_position: int
    implementation_function_identity: str
    added_position_act_occurrence_identity: tuple[str, int]
    source_invocation_occurrence_identity: tuple[str, str, int]
    result_invocation_occurrence_identity: tuple[str, str, int]
    source_returned: bool
    result_returned: bool

    @property
    def occurrence_identity(self) -> tuple[str, str, int]:
        return (
            self.boundary_identity,
            self.implementation_function_identity,
            self.occurrence_position,
        )

    @property
    def distinction(self) -> bool:
        return self.source_returned != self.result_returned

    @property
    def source_coordinates(self) -> bool:
        return self.source_returned

    @property
    def result_coordinates(self) -> bool:
        return self.result_returned


@dataclass(frozen=True, slots=True)
class AddedPositionPairCompareOccurrence:
    boundary_identity: str
    occurrence_position: int
    source_reference: ExactMaterialReference | ExactMaterialResultReference
    added_reference: ExactMaterialReference
    first_position: int
    second_position: int
    first_added_position_act_occurrence_identity: tuple[str, int]
    second_added_position_act_occurrence_identity: tuple[str, int]
    first_compare_occurrence_identities: tuple[tuple[str, str, int], ...]
    second_compare_occurrence_identities: tuple[tuple[str, str, int], ...]
    first_returned_coordinates: tuple[tuple[str, bool, bool], ...]
    second_returned_coordinates: tuple[tuple[str, bool, bool], ...]

    @property
    def occurrence_identity(self) -> tuple[str, int]:
        return (self.boundary_identity, self.occurrence_position)

    @property
    def distinction(self) -> bool:
        return self.first_returned_coordinates != self.second_returned_coordinates


@dataclass(frozen=True, slots=True)
class RemovedPositionCompareOccurrence:
    boundary_identity: str
    occurrence_position: int
    implementation_function_identity: str
    removed_position_act_occurrence_identity: tuple[str, int]
    source_invocation_occurrence_identity: tuple[str, str, int]
    result_invocation_occurrence_identity: tuple[str, str, int]
    source_returned: bool
    result_returned: bool

    @property
    def occurrence_identity(self) -> tuple[str, str, int]:
        return (
            self.boundary_identity,
            self.implementation_function_identity,
            self.occurrence_position,
        )

    @property
    def distinction(self) -> bool:
        return self.source_returned != self.result_returned


@dataclass(frozen=True, slots=True)
class AddedPositionAdmissionOccurrence:
    admission_occurrence: AdmissionOccurrence
    addition_occurrences: tuple[AddedPositionOccurrence, ...]
    comparison_occurrences: tuple[tuple[object, ...], ...]

    def __post_init__(self) -> None:
        if not isinstance(self.admission_occurrence, AdmissionOccurrence):
            raise TypeError("addition Admission requires its exact Act occurrence")
        admitted = admit_added_position_occurrences(
            self.addition_occurrences,
            self.comparison_occurrences,
        )
        if self.admission_occurrence.source_material != self.addition_occurrences:
            raise ValueError("addition Admission source differs from its Act occurrences")
        if self.admission_occurrence.admitted_material != admitted:
            raise ValueError("addition Admission differs from its Compare occurrences")

    @property
    def source_material(self):
        return self.admission_occurrence.source_material

    @property
    def admitted_material(self):
        return self.admission_occurrence.admitted_material

    @property
    def act_occurrence_identity(self) -> tuple[str, int]:
        return self.admission_occurrence.act_occurrence_identity

    @property
    def result_identity(self) -> tuple[str, int, str]:
        return self.admission_occurrence.result_identity

    @property
    def result_reference(self) -> AdmissionResultReference:
        return AdmissionResultReference(admission_occurrence=self)


@dataclass(frozen=True, slots=True)
class CompiledAdmissionOccurrence:
    admission_occurrence: AdmissionOccurrence
    invocation_result_references: tuple[CompiledInvocationResultReference, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.admission_occurrence, AdmissionOccurrence):
            raise TypeError("compiled Admission requires its exact Act occurrence")
        if (
            type(self.invocation_result_references) is not tuple
            or not self.invocation_result_references
            or any(
                not isinstance(reference, CompiledInvocationResultReference)
                for reference in self.invocation_result_references
            )
        ):
            raise TypeError("compiled Admission requires exact invocation results")
        invocations = tuple(
            reference.invocation_occurrence
            for reference in self.invocation_result_references
        )
        rows = {}
        functions = {}
        for invocation in invocations:
            identity = invocation.implementation_function_identity
            function = functions.setdefault(identity, invocation.implementation_function)
            if function != invocation.implementation_function:
                raise ValueError("one implementation identity names different functions")
            rows.setdefault(identity, []).append(invocation)
        source_rows = tuple(
            tuple(invocation.source_coordinate for invocation in row)
            for row in rows.values()
        )
        if any(source is None for row in source_rows for source in row):
            raise ValueError("compiled Admission requires exact source references")
        source_material = source_rows[0]
        if any(row != source_material for row in source_rows[1:]):
            raise ValueError("compiled Admission rows require the same exact material")
        if source_material != self.admission_occurrence.source_material:
            raise ValueError("compiled Admission source differs from its invocations")
        same_coordinates = {}
        for position, source in enumerate(source_material):
            coordinates = tuple(
                (identity, row[position].returned)
                for identity, row in rows.items()
            )
            same_coordinates.setdefault(coordinates, []).append(source)
        admitted = tuple(tuple(material) for material in same_coordinates.values())
        if admitted != self.admission_occurrence.admitted_material:
            raise ValueError("compiled Admission differs from its invocation results")

    @property
    def source_material(self):
        return self.admission_occurrence.source_material

    @property
    def admitted_material(self):
        return self.admission_occurrence.admitted_material

    @property
    def act_occurrence_identity(self) -> tuple[str, int]:
        return self.admission_occurrence.act_occurrence_identity

    @property
    def result_identity(self) -> tuple[str, int, str]:
        return self.admission_occurrence.result_identity

    @property
    def result_reference(self) -> AdmissionResultReference:
        return AdmissionResultReference(admission_occurrence=self)


def _added_position_comparisons_by_occurrence(
    occurrences: tuple[AddedPositionOccurrence, ...],
    comparisons: tuple[tuple[object, ...], ...],
) -> tuple[
    dict[tuple[str, int], AddedPositionOccurrence],
    dict[tuple[str, int], tuple[object, ...]],
]:
    if type(occurrences) is not tuple or not occurrences:
        raise TypeError("Admission requires exact addition Act occurrences")
    if type(comparisons) is not tuple or not comparisons:
        raise TypeError("Admission requires exact Compare occurrence tuples")

    occurrence_by_identity: dict[tuple[str, int], AddedPositionOccurrence] = {}
    for occurrence in occurrences:
        if not isinstance(occurrence, AddedPositionOccurrence):
            raise TypeError("Admission requires exact addition Act occurrences")
        identity = occurrence.act_occurrence_identity
        if identity in occurrence_by_identity:
            raise ValueError("addition Act occurrence entered Admission twice")
        occurrence_by_identity[identity] = occurrence

    expected_identities = frozenset(occurrence_by_identity)
    comparisons_by_occurrence: dict[
        tuple[str, int], list[object]
    ] = {
        identity: [] for identity in occurrence_by_identity
    }
    implementation_function_identities = set()
    for row in comparisons:
        if type(row) is not tuple or not row:
            raise TypeError("Admission requires exact Compare occurrence tuples")
        implementation_function_identity = row[0].implementation_function_identity
        if implementation_function_identity in implementation_function_identities:
            raise ValueError("implementation function entered Admission twice")
        implementation_function_identities.add(implementation_function_identity)

        comparison_by_identity = {}
        for comparison in row:
            from compiled_material_invocation import MaterialAddedCompareOccurrence

            if not isinstance(
                comparison,
                (AddedPositionCompareOccurrence, MaterialAddedCompareOccurrence),
            ):
                raise TypeError("Admission requires exact addition Compare occurrences")
            if (
                comparison.implementation_function_identity
                != implementation_function_identity
            ):
                raise ValueError("one Compare tuple crossed implementation functions")
            identity = comparison.added_position_act_occurrence_identity
            if identity in comparison_by_identity:
                raise ValueError("addition Act occurrence entered one Compare tuple twice")
            try:
                hash(comparison.source_coordinates)
                hash(comparison.result_coordinates)
            except TypeError as error:
                raise TypeError("Compare coordinates must be exact") from error
            comparison_by_identity[identity] = comparison

        if frozenset(comparison_by_identity) != expected_identities:
            raise ValueError("Compare tuple does not carry every addition Act occurrence")
        for identity in occurrence_by_identity:
            comparison = comparison_by_identity[identity]
            comparisons_by_occurrence[identity].append(comparison)

    return occurrence_by_identity, {
        identity: tuple(found)
        for identity, found in comparisons_by_occurrence.items()
    }


def admit_added_position_occurrences(
    occurrences: tuple[AddedPositionOccurrence, ...],
    comparisons: tuple[tuple[object, ...], ...],
) -> tuple[tuple[AddedPositionOccurrence, ...], ...]:
    occurrence_by_identity, comparisons_by_occurrence = (
        _added_position_comparisons_by_occurrence(occurrences, comparisons)
    )

    same_coordinates: dict[
        tuple[tuple[str, Hashable, Hashable], ...], list[AddedPositionOccurrence]
    ] = {}
    for identity, occurrence in occurrence_by_identity.items():
        coordinates = tuple(
            (
                comparison.implementation_function_identity,
                comparison.source_coordinates,
                comparison.result_coordinates,
            )
            for comparison in comparisons_by_occurrence[identity]
        )
        same_coordinates.setdefault(coordinates, []).append(occurrence)
    return tuple(tuple(found) for found in same_coordinates.values())


def added_position_admission_occurrence(
    occurrences: tuple[AddedPositionOccurrence, ...],
    comparisons: tuple[tuple[object, ...], ...],
    *,
    boundary_identity: str,
    occurrence_position: int = 0,
) -> AddedPositionAdmissionOccurrence:
    admitted = admit_added_position_occurrences(occurrences, comparisons)
    admission = admission_occurrence(
        admitted,
        boundary_identity=boundary_identity,
        occurrence_position=occurrence_position,
        source_material=occurrences,
    )
    return AddedPositionAdmissionOccurrence(
        admission_occurrence=admission,
        addition_occurrences=occurrences,
        comparison_occurrences=comparisons,
    )


def added_position_admission_occurrences(
    occurrences: tuple[AddedPositionOccurrence, ...],
    comparisons: tuple[tuple[object, ...], ...],
    *,
    boundary_identity: str,
) -> tuple[AddedPositionAdmissionOccurrence, ...]:
    if type(comparisons) is not tuple or not comparisons:
        raise TypeError("Admission requires exact Compare occurrence tuples")
    comparison_sets = tuple((row,) for row in comparisons) + (comparisons,)
    return tuple(
        added_position_admission_occurrence(
            occurrences,
            comparison_set,
            boundary_identity=boundary_identity,
            occurrence_position=position,
        )
        for position, comparison_set in enumerate(comparison_sets)
    )


def compare_added_position_pairs(
    occurrences: tuple[AddedPositionOccurrence, ...],
    comparisons: tuple[tuple[AddedPositionCompareOccurrence, ...], ...],
    *,
    boundary_identity: str,
) -> tuple[AddedPositionPairCompareOccurrence, ...]:
    if type(boundary_identity) is not str or not boundary_identity:
        raise TypeError("one exact boundary identity is required")
    occurrence_by_identity, comparisons_by_occurrence = (
        _added_position_comparisons_by_occurrence(occurrences, comparisons)
    )
    same_material = {}
    for occurrence in occurrence_by_identity.values():
        same_material.setdefault(
            (occurrence.source_reference, occurrence.added_reference), []
        ).append(occurrence)

    found = []
    for material_at_positions in same_material.values():
        for first_offset, first in enumerate(material_at_positions):
            for second in material_at_positions[first_offset + 1 :]:
                first_comparisons = comparisons_by_occurrence[
                    first.act_occurrence_identity
                ]
                second_comparisons = comparisons_by_occurrence[
                    second.act_occurrence_identity
                ]
                found.append(
                    AddedPositionPairCompareOccurrence(
                        boundary_identity=boundary_identity,
                        occurrence_position=len(found),
                        source_reference=first.source_reference,
                        added_reference=first.added_reference,
                        first_position=first.position,
                        second_position=second.position,
                        first_added_position_act_occurrence_identity=(
                            first.act_occurrence_identity
                        ),
                        second_added_position_act_occurrence_identity=(
                            second.act_occurrence_identity
                        ),
                        first_compare_occurrence_identities=tuple(
                            comparison.occurrence_identity
                            for comparison in first_comparisons
                        ),
                        second_compare_occurrence_identities=tuple(
                            comparison.occurrence_identity
                            for comparison in second_comparisons
                        ),
                        first_returned_coordinates=tuple(
                            (
                                comparison.implementation_function_identity,
                                comparison.source_returned,
                                comparison.result_returned,
                            )
                            for comparison in first_comparisons
                        ),
                        second_returned_coordinates=tuple(
                            (
                                comparison.implementation_function_identity,
                                comparison.source_returned,
                                comparison.result_returned,
                            )
                            for comparison in second_comparisons
                        ),
                    )
                )
    return tuple(found)


def _a(material: bytes):
    return json.loads(material)


def _b(material: bytes):
    return tomllib.load(io.BytesIO(material))


def _c(material: bytes):
    return xml.etree.ElementTree.fromstring(material)


def _d(material: bytes):
    return ast.parse(material)


def _e(material: bytes):
    return plistlib.loads(material)


COMPILED_IMPLEMENTATION_FUNCTIONS = tuple(
    CompiledImplementationFunction(identity=f"compiled-{index}", invocation=invocation)
    for index, invocation in enumerate((_a, _b, _c, _d, _e))
)


def compiled_invocation(
    exact_material: bytes,
    implementation_function: CompiledImplementationFunction,
    *,
    boundary_identity: str,
    invocation_position: int = 0,
    source_coordinate: (
        ExactMaterialCoordinates
        | AddedPositionOccurrence
        | RemovedPositionOccurrence
        | None
    ) = None,
) -> CompiledInvocationOccurrence:
    if type(exact_material) is not bytes:
        raise TypeError("implementation function material must be exact bytes")
    if not isinstance(implementation_function, CompiledImplementationFunction):
        raise TypeError("one compiled implementation function is required")
    if type(boundary_identity) is not str or not boundary_identity:
        raise TypeError("one exact boundary identity is required")
    if type(invocation_position) is not int or invocation_position < 0:
        raise TypeError("one exact invocation position is required")
    try:
        implementation_function.invocation(exact_material)
    except Exception:
        returned = False
    else:
        returned = True
    return CompiledInvocationOccurrence(
        boundary_identity=boundary_identity,
        invocation_position=invocation_position,
        exact_material=exact_material,
        implementation_function=implementation_function,
        returned=returned,
        source_coordinate=source_coordinate,
    )


def compiled_invocations(
    exact_materials: tuple[bytes, ...],
    *,
    boundary_identity: str,
    implementation_functions: tuple[CompiledImplementationFunction, ...] = COMPILED_IMPLEMENTATION_FUNCTIONS,
) -> tuple[tuple[CompiledInvocationOccurrence, ...], ...]:
    if type(exact_materials) is not tuple or not all(
        type(material) is bytes for material in exact_materials
    ):
        raise TypeError("implementation function inputs must be one exact tuple of bytes")
    if type(implementation_functions) is not tuple or not implementation_functions:
        raise TypeError("compiled implementation functions must be one nonempty tuple")
    if type(boundary_identity) is not str or not boundary_identity:
        raise TypeError("one exact boundary identity is required")
    if not all(
        isinstance(implementation_function, CompiledImplementationFunction)
        for implementation_function in implementation_functions
    ):
        raise TypeError("compiled implementation functions must be exact")
    return _compiled_invocations(
        exact_materials,
        boundary_identity=boundary_identity,
        implementation_functions=implementation_functions,
    )


def compiled_reference_invocations(
    references: tuple[ExactMaterialCoordinates, ...],
    *,
    boundary_identity: str,
    implementation_functions: tuple[
        CompiledImplementationFunction, ...
    ] = COMPILED_IMPLEMENTATION_FUNCTIONS,
) -> tuple[tuple[CompiledInvocationOccurrence, ...], ...]:
    if type(references) is not tuple or not all(
        _is_exact_material_coordinates(reference) for reference in references
    ):
        raise TypeError("implementation function inputs must carry exact references")
    if type(boundary_identity) is not str or not boundary_identity:
        raise TypeError("one exact boundary identity is required")
    if type(implementation_functions) is not tuple or not implementation_functions:
        raise TypeError("compiled implementation functions must be one nonempty tuple")
    if not all(
        isinstance(implementation_function, CompiledImplementationFunction)
        for implementation_function in implementation_functions
    ):
        raise TypeError("compiled implementation functions must be exact")
    return _compiled_invocations(
        tuple(reference.exact_material for reference in references),
        boundary_identity=boundary_identity,
        implementation_functions=implementation_functions,
        source_coordinates=references,
    )


def _compiled_invocations(
    exact_materials: tuple[bytes, ...],
    *,
    boundary_identity: str,
    implementation_functions: tuple[CompiledImplementationFunction, ...],
    source_coordinates: tuple[
        ExactMaterialCoordinates
        | AddedPositionOccurrence
        | RemovedPositionOccurrence,
        ...,
    ] | None = None,
) -> tuple[tuple[CompiledInvocationOccurrence, ...], ...]:
    identities = tuple(
        implementation_function.identity
        for implementation_function in implementation_functions
    )
    if len(set(identities)) != len(identities):
        raise ValueError("implementation function identities must be distinct")
    found = []
    for implementation_function in implementation_functions:
        occurrences = []
        for invocation_position, material in enumerate(exact_materials):
            try:
                implementation_function.invocation(material)
            except Exception:
                returned = False
            else:
                returned = True
            occurrences.append(
                CompiledInvocationOccurrence(
                    boundary_identity=boundary_identity,
                    invocation_position=invocation_position,
                    exact_material=material,
                    implementation_function=implementation_function,
                    returned=returned,
                    source_coordinate=(
                        source_coordinates[invocation_position]
                        if source_coordinates is not None
                        else None
                    ),
                )
            )
        found.append(tuple(occurrences))
    return tuple(found)


def admit_compiled_invocation_occurrences(
    occurrences: tuple[CompiledInvocationOccurrence, ...],
    *,
    boundary_identity: str,
    occurrence_position: int = 0,
) -> CompiledAdmissionOccurrence:
    return admit_compiled_invocation_rows(
        (occurrences,),
        boundary_identity=boundary_identity,
        occurrence_position=occurrence_position,
    )


def admit_compiled_invocation_rows(
    occurrence_rows: tuple[tuple[CompiledInvocationOccurrence, ...], ...],
    *,
    boundary_identity: str,
    occurrence_position: int = 0,
) -> CompiledAdmissionOccurrence:
    if type(occurrence_rows) is not tuple or not occurrence_rows:
        raise TypeError("compiled Admission requires exact invocation tuples")
    if any(
        type(row) is not tuple
        or not row
        or any(
            not isinstance(occurrence, CompiledInvocationOccurrence)
            for occurrence in row
        )
        for row in occurrence_rows
    ):
        raise TypeError("compiled Admission requires exact invocation tuples")
    identities = tuple(
        row[0].implementation_function_identity for row in occurrence_rows
    )
    if len(set(identities)) != len(identities) or any(
        any(
            occurrence.implementation_function_identity != identity
            for occurrence in row
        )
        for identity, row in zip(identities, occurrence_rows)
    ):
        raise ValueError("each compiled Admission tuple requires one exact function")
    source_rows = tuple(
        tuple(occurrence.source_coordinate for occurrence in row)
        for row in occurrence_rows
    )
    if any(source is None for row in source_rows for source in row):
        raise ValueError("compiled Admission requires exact source references")
    source_material = source_rows[0]
    if any(row != source_material for row in source_rows[1:]):
        raise ValueError("compiled Admission tuples require the same exact material")
    same_coordinates = {}
    for position, source in enumerate(source_material):
        coordinates = tuple(
            (identity, row[position].returned)
            for identity, row in zip(identities, occurrence_rows)
        )
        same_coordinates.setdefault(coordinates, []).append(source)
    flattened = tuple(
        occurrence for row in occurrence_rows for occurrence in row
    )
    admission = admission_occurrence(
        tuple(tuple(material) for material in same_coordinates.values()),
        boundary_identity=boundary_identity,
        occurrence_position=occurrence_position,
        source_material=source_material,
    )
    return CompiledAdmissionOccurrence(
        admission_occurrence=admission,
        invocation_result_references=tuple(
            occurrence.result_reference for occurrence in flattened
        ),
    )


def preserves_original_order(
    *,
    source_material: bytes,
    result_material: bytes,
    added_position: int,
) -> bool:
    if (
        type(source_material) is not bytes
        or type(result_material) is not bytes
        or type(added_position) is not int
        or added_position < 0
        or added_position >= len(result_material)
        or len(result_material) != len(source_material) + 1
    ):
        return False
    return (
        result_material[:added_position]
        + result_material[added_position + 1 :]
        == source_material
    )


def added_position_occurrences(
    source_material: tuple[ExactMaterialCoordinates, ...],
    added_material: tuple[ExactMaterialCoordinates, ...],
    *,
    boundary_identity: str,
) -> tuple[AddedPositionOccurrence, ...]:
    if type(source_material) is not tuple or not all(
        _is_exact_material_coordinates(material)
        for material in source_material
    ):
        raise TypeError("source material must carry exact references")
    if type(added_material) is not tuple or not all(
        _is_exact_material_coordinates(material)
        and type(material.exact_material) is bytes
        and len(material.exact_material) == 1
        for material in added_material
    ):
        raise TypeError("added material must carry exact one-byte references")
    if type(boundary_identity) is not str or not boundary_identity:
        raise TypeError("one exact boundary identity is required")
    return tuple(
        AddedPositionOccurrence(
            boundary_identity=boundary_identity,
            locality_identity=source.locality_identity,
            occurrence_position=occurrence_position,
            source_reference=source,
            position=position,
            added_reference=added,
            result_material=bytes(
                (
                    *source.exact_material[:position],
                    *added.exact_material,
                    *source.exact_material[position:],
                )
            ),
        )
        for occurrence_position, (source, position, added) in enumerate(
            (source, position, added)
            for source in source_material
            for position in range(len(source.exact_material) + 1)
            for added in added_material
        )
    )


def admission_added_position_occurrences(
    admission_result_reference: AdmissionResultReference,
    *,
    boundary_identity: str,
    admitted_material_act_occurrence_count_limit: int,
) -> tuple[AddedPositionOccurrence, ...]:
    if not isinstance(admission_result_reference, AdmissionResultReference):
        raise TypeError("addition Acts require one exact Admission result")
    if type(boundary_identity) is not str or not boundary_identity:
        raise TypeError("one exact boundary identity is required")
    if (
        type(admitted_material_act_occurrence_count_limit) is not int
        or admitted_material_act_occurrence_count_limit < 1
    ):
        raise TypeError("one exact positive Act occurrence count limit is required")
    found = []
    for admitted_position, admitted_material in enumerate(
        admission_result_reference.admitted_material
    ):
        if any(
            not _is_exact_material_coordinates(material)
            or len(material.exact_material) != 1
            for material in admitted_material
        ):
            raise TypeError("addition Acts require exact one-byte admitted material")
        locality_identities = {
            getattr(material, "locality_identity", None)
            for material in admitted_material
        }
        if None in locality_identities:
            raise TypeError("addition Acts require exact material Localities")
        if len(locality_identities) != 1:
            raise ValueError("one admitted material tuple crossed Localities")
        occurrence_count = sum(
            (len(source.exact_material) + 1) * len(admitted_material)
            for source in admitted_material
        )
        if occurrence_count > admitted_material_act_occurrence_count_limit:
            continue
        for source in admitted_material:
            for position in range(len(source.exact_material) + 1):
                for added in admitted_material:
                    found.append(
                        AddedPositionOccurrence(
                            boundary_identity=boundary_identity,
                            locality_identity=source.locality_identity,
                            occurrence_position=len(found),
                            source_reference=source,
                            position=position,
                            added_reference=added,
                            result_material=(
                                source.exact_material[:position]
                                + added.exact_material
                                + source.exact_material[position:]
                            ),
                            source_admission_result_reference=(
                                admission_result_reference
                            ),
                            source_admitted_material_position=admitted_position,
                            added_admission_result_reference=(
                                admission_result_reference
                            ),
                            added_admitted_material_position=admitted_position,
                            admitted_material_act_occurrence_count_limit=(
                                admitted_material_act_occurrence_count_limit
                            ),
                        )
                    )
    return tuple(found)


def admission_result_added_position_occurrences(
    source_admission_result_reference: AdmissionResultReference,
    added_admission_result_reference: AdmissionResultReference,
    *,
    boundary_identity: str,
    admitted_material_act_occurrence_count_limit: int,
) -> tuple[AddedPositionOccurrence, ...]:
    if not isinstance(
        source_admission_result_reference, AdmissionResultReference
    ) or not isinstance(added_admission_result_reference, AdmissionResultReference):
        raise TypeError("addition Acts require exact Admission results")
    if type(boundary_identity) is not str or not boundary_identity:
        raise TypeError("one exact boundary identity is required")
    if (
        type(admitted_material_act_occurrence_count_limit) is not int
        or admitted_material_act_occurrence_count_limit < 1
    ):
        raise TypeError("one exact positive Act occurrence count limit is required")
    found = []
    for source_admitted_position, source_admitted_material in enumerate(
        source_admission_result_reference.admitted_material
    ):
        if any(
            not _is_exact_material_coordinates(material)
            for material in source_admitted_material
        ):
            raise TypeError("addition Acts require exact admitted source material")
        source_locality_identities = {
            getattr(material, "locality_identity", None)
            for material in source_admitted_material
        }
        if None in source_locality_identities:
            raise TypeError("addition Acts require exact source material Localities")
        if len(source_locality_identities) != 1:
            raise ValueError("one admitted source material tuple crossed Localities")
        for added_admitted_position, added_admitted_material in enumerate(
            added_admission_result_reference.admitted_material
        ):
            if any(
                not _is_exact_material_coordinates(material)
                or len(material.exact_material) != 1
                for material in added_admitted_material
            ):
                raise TypeError(
                    "addition Acts require exact one-byte admitted added material"
                )
            added_locality_identities = {
                getattr(material, "locality_identity", None)
                for material in added_admitted_material
            }
            if None in added_locality_identities:
                raise TypeError(
                    "addition Acts require exact added material Localities"
                )
            if len(added_locality_identities) != 1:
                raise ValueError("one admitted added material tuple crossed Localities")
            if source_locality_identities != added_locality_identities:
                raise ValueError("addition Act Admissions crossed Localities")
            occurrence_count = sum(
                (len(source.exact_material) + 1) * len(added_admitted_material)
                for source in source_admitted_material
            )
            if occurrence_count > admitted_material_act_occurrence_count_limit:
                continue
            for source in source_admitted_material:
                for position in range(len(source.exact_material) + 1):
                    for added in added_admitted_material:
                        found.append(
                            AddedPositionOccurrence(
                                boundary_identity=boundary_identity,
                                locality_identity=source.locality_identity,
                                occurrence_position=len(found),
                                source_reference=source,
                                position=position,
                                added_reference=added,
                                result_material=(
                                    source.exact_material[:position]
                                    + added.exact_material
                                    + source.exact_material[position:]
                                ),
                                source_admission_result_reference=(
                                    source_admission_result_reference
                                ),
                                source_admitted_material_position=(
                                    source_admitted_position
                                ),
                                added_admission_result_reference=(
                                    added_admission_result_reference
                                ),
                                added_admitted_material_position=(
                                    added_admitted_position
                                ),
                                admitted_material_act_occurrence_count_limit=(
                                    admitted_material_act_occurrence_count_limit
                                ),
                            )
                        )
    return tuple(found)


def added_position_invocations(
    occurrences: tuple[AddedPositionOccurrence, ...],
    *,
    boundary_identity: str,
    implementation_functions: tuple[CompiledImplementationFunction, ...] = COMPILED_IMPLEMENTATION_FUNCTIONS,
) -> tuple[tuple[CompiledInvocationOccurrence, ...], ...]:
    if type(occurrences) is not tuple:
        raise TypeError("added-position occurrences must be one exact tuple")
    if type(boundary_identity) is not str or not boundary_identity:
        raise TypeError("one exact boundary identity is required")
    exact_material = []
    for occurrence_position, occurrence in enumerate(occurrences):
        if not isinstance(occurrence, AddedPositionOccurrence):
            raise TypeError("added-position material requires its exact Act occurrence")
        source = occurrence.source_material
        position = occurrence.position
        added = occurrence.added_material
        material = occurrence.result_material
        if (
            occurrence.occurrence_position != occurrence_position
            or type(added) is not bytes
            or len(added) != 1
            or type(material) is not bytes
            or not preserves_original_order(
                source_material=source,
                result_material=material,
                added_position=position,
            )
            or material[position : position + 1] != added
        ):
            raise ValueError("result material does not preserve its exact source order")
        exact_material.append(material)
    if type(implementation_functions) is not tuple or not implementation_functions:
        raise TypeError("compiled implementation functions must be one nonempty tuple")
    if not all(
        isinstance(implementation_function, CompiledImplementationFunction)
        for implementation_function in implementation_functions
    ):
        raise TypeError("compiled implementation functions must be exact")
    return _compiled_invocations(
        tuple(exact_material),
        boundary_identity=boundary_identity,
        implementation_functions=implementation_functions,
        source_coordinates=occurrences,
    )


def removed_position_occurrences(
    source_material: tuple[ExactMaterialReference, ...],
    removed_material: tuple[ExactMaterialReference, ...],
    *,
    boundary_identity: str,
) -> tuple[RemovedPositionOccurrence, ...]:
    if type(source_material) is not tuple or not all(
        isinstance(material, ExactMaterialReference) for material in source_material
    ):
        raise TypeError("source material must carry exact references")
    if type(removed_material) is not tuple or not all(
        isinstance(material, ExactMaterialReference)
        and len(material.exact_material) == 1
        for material in removed_material
    ):
        raise TypeError("removed material must carry exact one-byte references")
    if type(boundary_identity) is not str or not boundary_identity:
        raise TypeError("one exact boundary identity is required")
    exact_coordinates = tuple(
        (source, position, removed)
        for source in source_material
        for position in range(len(source.exact_material))
        for removed in removed_material
        if source.exact_material[position : position + 1]
        == removed.exact_material
    )
    return tuple(
        RemovedPositionOccurrence(
            boundary_identity=boundary_identity,
            locality_identity=source.locality_identity,
            occurrence_position=occurrence_position,
            source_reference=source,
            position=position,
            removed_reference=removed,
            result_material=(
                source.exact_material[:position]
                + source.exact_material[position + 1 :]
            ),
        )
        for occurrence_position, (source, position, removed) in enumerate(
            exact_coordinates
        )
    )


def removed_position_invocations(
    occurrences: tuple[RemovedPositionOccurrence, ...],
    *,
    boundary_identity: str,
    implementation_functions: tuple[
        CompiledImplementationFunction, ...
    ] = COMPILED_IMPLEMENTATION_FUNCTIONS,
) -> tuple[tuple[CompiledInvocationOccurrence, ...], ...]:
    if type(occurrences) is not tuple or not all(
        isinstance(occurrence, RemovedPositionOccurrence)
        for occurrence in occurrences
    ):
        raise TypeError("removed-position material requires exact Act occurrences")
    if any(
        occurrence.occurrence_position != position
        for position, occurrence in enumerate(occurrences)
    ):
        raise ValueError("removed-position Act occurrence positions must remain exact")
    if type(boundary_identity) is not str or not boundary_identity:
        raise TypeError("one exact boundary identity is required")
    if type(implementation_functions) is not tuple or not implementation_functions:
        raise TypeError("compiled implementation functions must be one nonempty tuple")
    if not all(
        isinstance(implementation_function, CompiledImplementationFunction)
        for implementation_function in implementation_functions
    ):
        raise TypeError("compiled implementation functions must be exact")
    return _compiled_invocations(
        tuple(occurrence.result_material for occurrence in occurrences),
        boundary_identity=boundary_identity,
        implementation_functions=implementation_functions,
        source_coordinates=occurrences,
    )


def compare_added_position_invocations(
    source_invocations: tuple[tuple[CompiledInvocationOccurrence, ...], ...],
    result_invocations: tuple[tuple[CompiledInvocationOccurrence, ...], ...],
    *,
    boundary_identity: str,
) -> tuple[tuple[AddedPositionCompareOccurrence, ...], ...]:
    if type(source_invocations) is not tuple or type(result_invocations) is not tuple:
        raise TypeError("Compare inputs must be exact invocation tuples")
    if len(source_invocations) != len(result_invocations):
        raise ValueError("Compare inputs require the same implementation functions")
    if type(boundary_identity) is not str or not boundary_identity:
        raise TypeError("one exact boundary identity is required")
    compared = []
    comparison_position = 0
    for source_row, result_row in zip(source_invocations, result_invocations):
        if not source_row or not result_row:
            raise ValueError("Compare inputs require invocation occurrences")
        implementation_function_identity = source_row[0].implementation_function_identity
        if (
            any(
                occurrence.implementation_function_identity
                != implementation_function_identity
                for occurrence in source_row
            )
            or any(
                occurrence.implementation_function_identity
                != implementation_function_identity
                for occurrence in result_row
            )
        ):
            raise ValueError("Compare inputs require the same implementation function")
        source_by_reference = {}
        for source_invocation in source_row:
            reference = source_invocation.source_coordinate
            if not _is_exact_material_coordinates(reference):
                raise ValueError("source invocation requires its exact material reference")
            if reference in source_by_reference:
                raise ValueError("source material reference entered Compare twice")
            source_by_reference[reference] = source_invocation
        row = []
        for result_invocation in result_row:
            addition = result_invocation.source_coordinate
            if not isinstance(addition, AddedPositionOccurrence):
                raise ValueError("result invocation requires its exact addition occurrence")
            source_invocation = source_by_reference.get(addition.source_reference)
            if source_invocation is None:
                raise ValueError("addition occurrence has no exact source invocation")
            if (
                source_invocation.exact_material != addition.source_material
                or result_invocation.exact_material != addition.result_material
            ):
                raise ValueError("invocation material differs from the addition occurrence")
            row.append(
                AddedPositionCompareOccurrence(
                    boundary_identity=boundary_identity,
                    occurrence_position=comparison_position,
                    implementation_function_identity=implementation_function_identity,
                    added_position_act_occurrence_identity=(
                        addition.act_occurrence_identity
                    ),
                    source_invocation_occurrence_identity=(
                        source_invocation.occurrence_identity
                    ),
                    result_invocation_occurrence_identity=(
                        result_invocation.occurrence_identity
                    ),
                    source_returned=source_invocation.returned,
                    result_returned=result_invocation.returned,
                )
            )
            comparison_position += 1
        compared.append(tuple(row))
    return tuple(compared)


def recurring_added_returned_coordinate(
    comparisons: tuple[AddedPositionCompareOccurrence, ...],
    additions: tuple[AddedPositionOccurrence, ...],
    addition: AddedPositionOccurrence,
    source_invocation: CompiledInvocationOccurrence,
) -> bool | None:
    if (
        type(comparisons) is not tuple
        or len(comparisons) < 2
        or any(
            not isinstance(comparison, AddedPositionCompareOccurrence)
            for comparison in comparisons
        )
    ):
        raise TypeError("recurrence requires exact Compare occurrences")
    if type(additions) is not tuple or any(
        not isinstance(found, AddedPositionOccurrence) for found in additions
    ):
        raise TypeError("recurrence requires exact addition Act occurrences")
    if not isinstance(addition, AddedPositionOccurrence) or not isinstance(
        source_invocation, CompiledInvocationOccurrence
    ):
        raise TypeError("recurrence requires one exact addition and source invocation")
    if (
        addition.source_admission_result_reference is None
        or addition.added_admission_result_reference is None
    ):
        return None
    if source_invocation.source_coordinate != addition.source_reference:
        raise ValueError("source invocation differs from the addition Act")
    addition_by_identity = {
        found.act_occurrence_identity: found for found in additions
    }
    if len(addition_by_identity) != len(additions):
        raise ValueError("addition Act occurrence entered recurrence twice")

    addition_coordinates = (
        addition.source_admission_result_reference.result_identity,
        addition.source_admitted_material_position,
        addition.added_admission_result_reference.result_identity,
        addition.added_admitted_material_position,
        addition.position,
        len(addition.source_material),
        len(addition.added_material),
    )
    found = []
    occurrence_identities = set()
    for comparison in comparisons:
        prior = addition_by_identity.get(
            comparison.added_position_act_occurrence_identity
        )
        if prior is None:
            raise ValueError("Compare occurrence has no exact addition Act occurrence")
        if (
            prior.source_admission_result_reference is None
            or prior.added_admission_result_reference is None
        ):
            continue
        prior_coordinates = (
            prior.source_admission_result_reference.result_identity,
            prior.source_admitted_material_position,
            prior.added_admission_result_reference.result_identity,
            prior.added_admitted_material_position,
            prior.position,
            len(prior.source_material),
            len(prior.added_material),
        )
        if (
            prior_coordinates == addition_coordinates
            and comparison.implementation_function_identity
            == source_invocation.implementation_function_identity
            and comparison.source_returned == source_invocation.returned
            and prior.act_occurrence_identity != addition.act_occurrence_identity
            and prior.result_material != addition.result_material
        ):
            found.append(comparison.result_returned)
            occurrence_identities.add(comparison.occurrence_identity)
    if len(occurrence_identities) < 2 or len(set(found)) != 1:
        return None
    return found[0]


def first_recurring_added_compare(
    additions: tuple[AddedPositionOccurrence, ...],
    source_invocations: tuple[CompiledInvocationOccurrence, ...],
    implementation_function: CompiledImplementationFunction,
    *,
    boundary_identity: str,
    act_occurrence_count_limit: int,
    invoke_later: bool = True,
) -> tuple[
    tuple[AddedPositionCompareOccurrence, ...],
    bool | None,
    AddedPositionCompareOccurrence | None,
]:
    if type(additions) is not tuple or not additions or any(
        not isinstance(addition, AddedPositionOccurrence) for addition in additions
    ):
        raise TypeError("recurrence requires exact addition Act occurrences")
    if type(source_invocations) is not tuple or not source_invocations or any(
        not isinstance(invocation, CompiledInvocationOccurrence)
        for invocation in source_invocations
    ):
        raise TypeError("recurrence requires exact source invocation occurrences")
    if not isinstance(implementation_function, CompiledImplementationFunction):
        raise TypeError("recurrence requires one exact implementation function")
    if type(boundary_identity) is not str or not boundary_identity:
        raise TypeError("one exact boundary identity is required")
    if (
        type(act_occurrence_count_limit) is not int
        or act_occurrence_count_limit < 1
    ):
        raise TypeError("one exact positive Act occurrence count limit is required")
    source_by_reference = {
        invocation.source_coordinate: invocation for invocation in source_invocations
    }
    if len(source_by_reference) != len(source_invocations) or any(
        invocation.implementation_function != implementation_function
        for invocation in source_invocations
    ):
        raise ValueError("recurrence source invocations must be exact and distinct")
    if len({invocation.returned for invocation in source_invocations}) < 2:
        return (), None, None

    comparisons = []
    for addition in additions[:act_occurrence_count_limit]:
        source_invocation = source_by_reference.get(addition.source_reference)
        if source_invocation is None:
            raise ValueError("recurrence requires each exact source invocation")
        coordinate = (
            recurring_added_returned_coordinate(
                tuple(comparisons),
                additions,
                addition,
                source_invocation,
            )
            if len(comparisons) >= 2
            else None
        )
        if coordinate is not None and not invoke_later:
            return tuple(comparisons), coordinate, None
        result_invocation = compiled_invocation(
            addition.result_material,
            implementation_function,
            boundary_identity=f"{boundary_identity}-invocation",
            invocation_position=len(comparisons),
            source_coordinate=addition,
        )
        comparison = AddedPositionCompareOccurrence(
            boundary_identity=f"{boundary_identity}-compare",
            occurrence_position=len(comparisons),
            implementation_function_identity=(
                implementation_function.identity
            ),
            added_position_act_occurrence_identity=(
                addition.act_occurrence_identity
            ),
            source_invocation_occurrence_identity=(
                source_invocation.occurrence_identity
            ),
            result_invocation_occurrence_identity=(
                result_invocation.occurrence_identity
            ),
            source_returned=source_invocation.returned,
            result_returned=result_invocation.returned,
        )
        if coordinate is not None:
            return tuple(comparisons), coordinate, comparison
        comparisons.append(comparison)
    return tuple(comparisons), None, None


def first_recurring_added_compare_across(
    additions: tuple[AddedPositionOccurrence, ...],
    source_invocation_rows: tuple[tuple[CompiledInvocationOccurrence, ...], ...],
    *,
    boundary_identity: str,
    act_occurrence_count_limit: int,
) -> tuple[
    tuple[tuple[AddedPositionCompareOccurrence, ...], ...],
    tuple[bool, ...] | None,
    tuple[AddedPositionCompareOccurrence, ...] | None,
]:
    if type(source_invocation_rows) is not tuple or not source_invocation_rows:
        raise TypeError("joint recurrence requires exact invocation rows")
    functions = tuple(row[0].implementation_function for row in source_invocation_rows if row)
    if len(functions) != len(source_invocation_rows) or len(
        {function.identity for function in functions}
    ) != len(functions):
        raise ValueError("joint recurrence requires distinct implementation functions")
    source_coordinates = tuple(
        tuple(invocation.source_coordinate for invocation in row)
        for row in source_invocation_rows
    )
    if any(row != source_coordinates[0] for row in source_coordinates[1:]):
        raise ValueError("joint recurrence requires one exact source sequence")
    results = tuple(
        first_recurring_added_compare(
            additions,
            row,
            function,
            boundary_identity=f"{boundary_identity}-{function.identity}",
            act_occurrence_count_limit=act_occurrence_count_limit,
        )
        for row, function in zip(source_invocation_rows, functions)
    )
    if any(later is None for _, _, later in results):
        return tuple(earlier for earlier, _, _ in results), None, None
    later_occurrences = tuple(later for _, _, later in results)
    if len({later.added_position_act_occurrence_identity for later in later_occurrences}) != 1:
        return tuple(earlier for earlier, _, _ in results), None, None
    coordinates = tuple(coordinate for _, coordinate, _ in results)
    return (
        tuple(earlier for earlier, _, _ in results),
        coordinates,
        later_occurrences,
    )


def compare_removed_position_invocations(
    source_invocations: tuple[tuple[CompiledInvocationOccurrence, ...], ...],
    result_invocations: tuple[tuple[CompiledInvocationOccurrence, ...], ...],
    *,
    boundary_identity: str,
) -> tuple[tuple[RemovedPositionCompareOccurrence, ...], ...]:
    if type(source_invocations) is not tuple or type(result_invocations) is not tuple:
        raise TypeError("Compare inputs must be exact invocation tuples")
    if len(source_invocations) != len(result_invocations):
        raise ValueError("Compare inputs require the same implementation functions")
    if type(boundary_identity) is not str or not boundary_identity:
        raise TypeError("one exact boundary identity is required")
    compared = []
    comparison_position = 0
    for source_row, result_row in zip(source_invocations, result_invocations):
        if not source_row or not result_row:
            raise ValueError("Compare inputs require invocation occurrences")
        implementation_function_identity = source_row[0].implementation_function_identity
        if (
            any(
                occurrence.implementation_function_identity
                != implementation_function_identity
                for occurrence in source_row
            )
            or any(
                occurrence.implementation_function_identity
                != implementation_function_identity
                for occurrence in result_row
            )
        ):
            raise ValueError("Compare inputs require the same implementation function")
        source_by_reference = {}
        for source_invocation in source_row:
            reference = source_invocation.source_coordinate
            if not isinstance(reference, ExactMaterialReference):
                raise ValueError("source invocation requires its exact material reference")
            if reference in source_by_reference:
                raise ValueError("source material reference entered Compare twice")
            source_by_reference[reference] = source_invocation
        row = []
        for result_invocation in result_row:
            removal = result_invocation.source_coordinate
            if not isinstance(removal, RemovedPositionOccurrence):
                raise ValueError("result invocation requires its exact removal occurrence")
            source_invocation = source_by_reference.get(removal.source_reference)
            if source_invocation is None:
                raise ValueError("removal occurrence has no exact source invocation")
            if (
                source_invocation.exact_material != removal.source_material
                or result_invocation.exact_material != removal.result_material
            ):
                raise ValueError("invocation material differs from the removal occurrence")
            row.append(
                RemovedPositionCompareOccurrence(
                    boundary_identity=boundary_identity,
                    occurrence_position=comparison_position,
                    implementation_function_identity=implementation_function_identity,
                    removed_position_act_occurrence_identity=(
                        removal.act_occurrence_identity
                    ),
                    source_invocation_occurrence_identity=(
                        source_invocation.occurrence_identity
                    ),
                    result_invocation_occurrence_identity=(
                        result_invocation.occurrence_identity
                    ),
                    source_returned=source_invocation.returned,
                    result_returned=result_invocation.returned,
                )
            )
            comparison_position += 1
        compared.append(tuple(row))
    return tuple(compared)


def recurring_removed_returned_coordinate(
    comparisons: tuple[RemovedPositionCompareOccurrence, ...],
    removals: tuple[RemovedPositionOccurrence, ...],
    removal: RemovedPositionOccurrence,
    source_invocation: CompiledInvocationOccurrence,
) -> bool | None:
    if type(comparisons) is not tuple or len(comparisons) < 2 or any(
        not isinstance(comparison, RemovedPositionCompareOccurrence)
        for comparison in comparisons
    ):
        raise TypeError("recurrence requires exact Compare occurrences")
    if type(removals) is not tuple or any(
        not isinstance(found, RemovedPositionOccurrence) for found in removals
    ):
        raise TypeError("recurrence requires exact removal Act occurrences")
    if not isinstance(removal, RemovedPositionOccurrence) or not isinstance(
        source_invocation, CompiledInvocationOccurrence
    ):
        raise TypeError("recurrence requires one exact removal and source invocation")
    if source_invocation.source_coordinate != removal.source_reference:
        raise ValueError("source invocation differs from the removal Act")
    removal_by_identity = {
        found.act_occurrence_identity: found for found in removals
    }
    if len(removal_by_identity) != len(removals):
        raise ValueError("removal Act occurrence entered recurrence twice")
    coordinates = (
        len(removal.source_material),
        removal.removed_material,
        removal.position,
        len(removal.source_material),
        len(removal.removed_material),
    )
    found = []
    occurrence_identities = set()
    for comparison in comparisons:
        prior = removal_by_identity.get(
            comparison.removed_position_act_occurrence_identity
        )
        if prior is None:
            raise ValueError("Compare occurrence has no exact removal Act occurrence")
        prior_coordinates = (
            len(prior.source_material),
            prior.removed_material,
            prior.position,
            len(prior.source_material),
            len(prior.removed_material),
        )
        if (
            prior_coordinates == coordinates
            and comparison.implementation_function_identity
            == source_invocation.implementation_function_identity
            and comparison.source_returned == source_invocation.returned
            and prior.act_occurrence_identity != removal.act_occurrence_identity
            and prior.result_material != removal.result_material
        ):
            found.append(comparison.result_returned)
            occurrence_identities.add(comparison.occurrence_identity)
    if len(occurrence_identities) < 2 or len(set(found)) != 1:
        return None
    return found[0]


def first_recurring_removed_compare(
    removals: tuple[RemovedPositionOccurrence, ...],
    source_invocations: tuple[CompiledInvocationOccurrence, ...],
    implementation_function: CompiledImplementationFunction,
    *,
    boundary_identity: str,
    act_occurrence_count_limit: int,
    invoke_later: bool = True,
) -> tuple[
    tuple[RemovedPositionCompareOccurrence, ...],
    bool | None,
    RemovedPositionCompareOccurrence | None,
]:
    if type(removals) is not tuple or not removals or any(
        not isinstance(removal, RemovedPositionOccurrence) for removal in removals
    ):
        raise TypeError("recurrence requires exact removal Act occurrences")
    if type(source_invocations) is not tuple or not source_invocations or any(
        not isinstance(invocation, CompiledInvocationOccurrence)
        for invocation in source_invocations
    ):
        raise TypeError("recurrence requires exact source invocation occurrences")
    if not isinstance(implementation_function, CompiledImplementationFunction):
        raise TypeError("recurrence requires one exact implementation function")
    if type(boundary_identity) is not str or not boundary_identity:
        raise TypeError("one exact boundary identity is required")
    if type(act_occurrence_count_limit) is not int or act_occurrence_count_limit < 1:
        raise TypeError("one exact positive Act occurrence count limit is required")
    if type(invoke_later) is not bool:
        raise TypeError("later invocation control must be exact")
    source_by_reference = {
        invocation.source_coordinate: invocation for invocation in source_invocations
    }
    if len(source_by_reference) != len(source_invocations) or any(
        invocation.implementation_function != implementation_function
        for invocation in source_invocations
    ):
        raise ValueError("recurrence source invocations must be exact and distinct")
    if len({invocation.returned for invocation in source_invocations}) < 2:
        return (), None, None
    comparisons = []
    for removal in removals[:act_occurrence_count_limit]:
        source_invocation = source_by_reference.get(removal.source_reference)
        if source_invocation is None:
            raise ValueError("recurrence requires each exact source invocation")
        coordinate = (
            recurring_removed_returned_coordinate(
                tuple(comparisons), removals, removal, source_invocation
            )
            if len(comparisons) >= 2
            else None
        )
        if coordinate is not None and not invoke_later:
            return tuple(comparisons), coordinate, None
        result_invocation = compiled_invocation(
            removal.result_material,
            implementation_function,
            boundary_identity=f"{boundary_identity}-invocation",
            invocation_position=len(comparisons),
            source_coordinate=removal,
        )
        comparison = RemovedPositionCompareOccurrence(
            boundary_identity=f"{boundary_identity}-compare",
            occurrence_position=len(comparisons),
            implementation_function_identity=implementation_function.identity,
            removed_position_act_occurrence_identity=removal.act_occurrence_identity,
            source_invocation_occurrence_identity=source_invocation.occurrence_identity,
            result_invocation_occurrence_identity=result_invocation.occurrence_identity,
            source_returned=source_invocation.returned,
            result_returned=result_invocation.returned,
        )
        if coordinate is not None:
            return tuple(comparisons), coordinate, comparison
        comparisons.append(comparison)
    return tuple(comparisons), None, None


def first_recurring_removed_compare_across(
    removals: tuple[RemovedPositionOccurrence, ...],
    source_invocation_rows: tuple[tuple[CompiledInvocationOccurrence, ...], ...],
    *,
    boundary_identity: str,
    act_occurrence_count_limit: int,
) -> tuple[
    tuple[tuple[RemovedPositionCompareOccurrence, ...], ...],
    tuple[bool, ...] | None,
    tuple[RemovedPositionCompareOccurrence, ...] | None,
]:
    if type(source_invocation_rows) is not tuple or not source_invocation_rows:
        raise TypeError("joint recurrence requires exact invocation rows")
    functions = tuple(
        row[0].implementation_function
        for row in source_invocation_rows
        if row
    )
    if len(functions) != len(source_invocation_rows) or len(
        {function.identity for function in functions}
    ) != len(functions):
        raise ValueError("joint recurrence requires distinct implementation functions")
    source_coordinates = tuple(
        tuple(invocation.source_coordinate for invocation in row)
        for row in source_invocation_rows
    )
    if any(row != source_coordinates[0] for row in source_coordinates[1:]):
        raise ValueError("joint recurrence requires one exact source sequence")
    results = tuple(
        first_recurring_removed_compare(
            removals,
            row,
            function,
            boundary_identity=f"{boundary_identity}-{function.identity}",
            act_occurrence_count_limit=act_occurrence_count_limit,
        )
        for row, function in zip(source_invocation_rows, functions)
    )
    if any(later is None for _, _, later in results):
        return tuple(earlier for earlier, _, _ in results), None, None
    later_occurrences = tuple(later for _, _, later in results)
    if len({later.removed_position_act_occurrence_identity for later in later_occurrences}) != 1:
        return tuple(earlier for earlier, _, _ in results), None, None
    coordinates = tuple(coordinate for _, coordinate, _ in results)
    return (
        tuple(earlier for earlier, _, _ in results),
        coordinates,
        later_occurrences,
    )
