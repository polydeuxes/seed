#!/usr/bin/env python3

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from dataclasses import InitVar, dataclass, field
from typing import Hashable
import os
import selectors
import subprocess
import time

from seed_runtime.events import EventLedger
from seed_runtime.material_ingest import MATERIAL_INGEST_OCCURRED_KIND
from seed_runtime.evidence_of_yield_relation import read_requirements_of_yield_relation

from material_admission import (
    AdmissionOccurrence,
    AdmissionResultReference,
    admission_occurrence,
)

MaterialInvocationCoordinates = tuple[
    float,
    int | None,
    bool,
    bool,
    bool,
    bool,
    int | None,
    bytes | None,
    bytes | None,
]
MaterialInvocationReturnCoordinates = tuple[
    float,
    int | None,
    bool,
    bool,
    bool,
    bool,
    int | None,
]
from compiled_format_invocation import (
    AddedPositionOccurrence,
    ExactMaterialResultReference,
    RemovedPositionOccurrence,
)


@dataclass(frozen=True, slots=True)
class MaterialImplementationFunction:
    identity: str
    invocation: tuple[str, ...]

    def __post_init__(self) -> None:
        if type(self.identity) is not str or not self.identity:
            raise TypeError("one exact implementation function identity is required")
        if (
            type(self.invocation) is not tuple
            or not self.invocation
            or any(type(part) is not str or not part for part in self.invocation)
        ):
            raise TypeError("one exact implementation function invocation is required")


@dataclass(frozen=True, slots=True)
class IngestResultReference:
    recorded_occurrence_identity: str
    locality_identity: str
    act_occurrence_identity: str
    result_identity: str
    evidence_of_yield_relation_identity: str
    exact_material: bytes

    def __post_init__(self) -> None:
        coordinates = (
            self.recorded_occurrence_identity,
            self.locality_identity,
            self.act_occurrence_identity,
            self.result_identity,
            self.evidence_of_yield_relation_identity,
        )
        if any(
            type(coordinate) is not str or not coordinate
            for coordinate in coordinates
        ):
            raise TypeError("Ingest result requires exact occurrence coordinates")
        if type(self.exact_material) is not bytes:
            raise TypeError("Ingest result requires exact material")


@dataclass(frozen=True, slots=True)
class MaterialInvocationResultReference:
    invocation_occurrence: "MaterialInvocationOccurrence"

    def __post_init__(self) -> None:
        if not isinstance(self.invocation_occurrence, MaterialInvocationOccurrence):
            raise TypeError("invocation result requires its exact Act occurrence")

    @property
    def act_occurrence_identity(self) -> tuple[str, str, int]:
        return self.invocation_occurrence.occurrence_identity

    @property
    def result_identity(self) -> tuple[str, str, int, str]:
        return (*self.act_occurrence_identity, "result")

    @property
    def coordinates(
        self,
    ) -> MaterialInvocationCoordinates:
        return self.invocation_occurrence.coordinates


@dataclass(frozen=True, slots=True)
class MaterialAddedCompareOccurrence:
    boundary_identity: str
    occurrence_position: int
    addition_occurrence: AddedPositionOccurrence
    source_invocation: "MaterialInvocationOccurrence"
    result_invocation: "MaterialInvocationOccurrence"

    def __post_init__(self) -> None:
        if type(self.boundary_identity) is not str or not self.boundary_identity:
            raise TypeError("one exact boundary identity is required")
        if type(self.occurrence_position) is not int or self.occurrence_position < 0:
            raise TypeError("one exact Compare occurrence position is required")
        if not isinstance(self.addition_occurrence, AddedPositionOccurrence):
            raise TypeError("Compare requires one exact addition Act occurrence")
        if not isinstance(
            self.source_invocation, MaterialInvocationOccurrence
        ) or not isinstance(self.result_invocation, MaterialInvocationOccurrence):
            raise TypeError("Compare requires exact invocation occurrences")
        if (
            self.source_invocation.implementation_function
            != self.result_invocation.implementation_function
        ):
            raise ValueError("Compare cannot cross implementation functions")
        if (
            self.source_invocation.time_limit_second_count
            != self.result_invocation.time_limit_second_count
        ):
            raise ValueError("Compare cannot cross time limits")
        if self.source_invocation.source_reference != (
            self.addition_occurrence.source_reference
        ):
            raise ValueError("Compare source differs from its addition Act")
        if self.result_invocation.source_reference != (
            self.addition_occurrence.result_reference
        ):
            raise ValueError("Compare result differs from its addition Act")

    @property
    def occurrence_identity(self) -> tuple[str, str, int]:
        return (
            self.boundary_identity,
            self.source_invocation.implementation_function_identity,
            self.occurrence_position,
        )

    @property
    def implementation_function_identity(self) -> str:
        return self.source_invocation.implementation_function_identity

    @property
    def added_position_act_occurrence_identity(self) -> tuple[str, int]:
        return self.addition_occurrence.act_occurrence_identity

    @property
    def source_coordinates(
        self,
    ) -> MaterialInvocationCoordinates:
        return self.source_invocation.coordinates

    @property
    def result_coordinates(
        self,
    ) -> MaterialInvocationCoordinates:
        return self.result_invocation.coordinates

    @property
    def distinction(self) -> bool:
        return self.source_coordinates != self.result_coordinates


@dataclass(frozen=True, slots=True)
class MaterialAddedReturnCompareOccurrence(MaterialAddedCompareOccurrence):
    @property
    def source_coordinates(self) -> MaterialInvocationReturnCoordinates:
        return self.source_invocation.return_coordinates

    @property
    def result_coordinates(self) -> MaterialInvocationReturnCoordinates:
        return self.result_invocation.return_coordinates


@dataclass(frozen=True, slots=True)
class MaterialRemovedCompareOccurrence:
    boundary_identity: str
    occurrence_position: int
    removal_occurrence: RemovedPositionOccurrence
    source_invocation: "MaterialInvocationOccurrence"
    result_invocation: "MaterialInvocationOccurrence"

    def __post_init__(self) -> None:
        if type(self.boundary_identity) is not str or not self.boundary_identity:
            raise TypeError("one exact boundary identity is required")
        if type(self.occurrence_position) is not int or self.occurrence_position < 0:
            raise TypeError("one exact Compare occurrence position is required")
        if not isinstance(self.removal_occurrence, RemovedPositionOccurrence):
            raise TypeError("Compare requires one exact removal Act occurrence")
        if not isinstance(
            self.source_invocation, MaterialInvocationOccurrence
        ) or not isinstance(self.result_invocation, MaterialInvocationOccurrence):
            raise TypeError("Compare requires exact invocation occurrences")
        if (
            self.source_invocation.implementation_function
            != self.result_invocation.implementation_function
        ):
            raise ValueError("Compare cannot cross implementation functions")
        if (
            self.source_invocation.time_limit_second_count
            != self.result_invocation.time_limit_second_count
        ):
            raise ValueError("Compare cannot cross time limits")
        if (
            self.source_invocation.material_byte_count_limit
            != self.result_invocation.material_byte_count_limit
        ):
            raise ValueError("Compare cannot cross material byte-count limits")
        if self.source_invocation.source_reference != (
            self.removal_occurrence.source_reference
        ):
            raise ValueError("Compare source differs from its removal Act")
        if self.result_invocation.source_reference != (
            self.removal_occurrence.result_reference
        ):
            raise ValueError("Compare result differs from its removal Act")

    @property
    def occurrence_identity(self) -> tuple[str, str, int]:
        return (
            self.boundary_identity,
            self.source_invocation.implementation_function_identity,
            self.occurrence_position,
        )

    @property
    def implementation_function_identity(self) -> str:
        return self.source_invocation.implementation_function_identity

    @property
    def removed_position_act_occurrence_identity(self) -> tuple[str, int]:
        return self.removal_occurrence.act_occurrence_identity

    @property
    def removed_position_result_reference(self) -> ExactMaterialResultReference:
        return self.removal_occurrence.result_reference

    @property
    def source_coordinates(self) -> MaterialInvocationCoordinates:
        return self.source_invocation.coordinates

    @property
    def result_coordinates(self) -> MaterialInvocationCoordinates:
        return self.result_invocation.coordinates

    @property
    def distinction(self) -> bool:
        return self.source_coordinates != self.result_coordinates


@dataclass(frozen=True, slots=True)
class MaterialInvocationOccurrence:
    boundary_identity: str
    invocation_position: int
    exact_material: bytes
    implementation_function: MaterialImplementationFunction
    returned: bool
    returncode: int | None
    stdout_bytes: bytes | None
    stderr_bytes: bytes | None
    source_reference: Hashable | None = None
    time_limit_second_count: float = 30.0
    material_byte_count_limit: int | None = None
    time_limit_reached: bool = False
    stdout_byte_count_limit_reached: bool = False
    stderr_byte_count_limit_reached: bool = False

    def __post_init__(self) -> None:
        if type(self.boundary_identity) is not str or not self.boundary_identity:
            raise TypeError("one exact boundary identity is required")
        if type(self.invocation_position) is not int or self.invocation_position < 0:
            raise TypeError("one exact invocation position is required")
        if type(self.exact_material) is not bytes:
            raise TypeError("implementation function material must be exact bytes")
        if not isinstance(
            self.implementation_function, MaterialImplementationFunction
        ):
            raise TypeError("one exact implementation function is required")
        if type(self.returned) is not bool:
            raise TypeError("returned coordinate must be exact")
        if (
            type(self.time_limit_second_count) is not float
            or self.time_limit_second_count <= 0
        ):
            raise TypeError("one exact positive time limit second count is required")
        if self.material_byte_count_limit is not None and (
            type(self.material_byte_count_limit) is not int
            or self.material_byte_count_limit < 1
        ):
            raise TypeError("one exact positive material byte count limit is required")
        limit_coordinates = (
            self.time_limit_reached,
            self.stdout_byte_count_limit_reached,
            self.stderr_byte_count_limit_reached,
        )
        if any(type(coordinate) is not bool for coordinate in limit_coordinates):
            raise TypeError("invocation limit coordinates must be exact")
        if (
            self.material_byte_count_limit is None
            and (
                self.stdout_byte_count_limit_reached
                or self.stderr_byte_count_limit_reached
            )
        ):
            raise ValueError("material limit cannot be reached without its exact count")
        if self.returned and any(limit_coordinates):
            raise ValueError("a returned invocation cannot have reached a limit")
        if self.stdout_byte_count_limit_reached and (
            type(self.stdout_bytes) is not bytes
            or len(self.stdout_bytes) != self.material_byte_count_limit
        ):
            raise ValueError("stdout material does not preserve its exact bounded prefix")
        if self.stderr_byte_count_limit_reached and (
            type(self.stderr_bytes) is not bytes
            or len(self.stderr_bytes) != self.material_byte_count_limit
        ):
            raise ValueError("stderr material does not preserve its exact bounded prefix")
        if self.returned:
            if type(self.returncode) is not int:
                raise TypeError("a returned invocation requires its exact return code")
            if type(self.stdout_bytes) is not bytes or type(self.stderr_bytes) is not bytes:
                raise TypeError("returned material must be exact bytes")
        elif self.returncode is not None:
            raise ValueError("an invocation that did not return has no return code")
        elif self.stdout_bytes is not None and type(self.stdout_bytes) is not bytes:
            raise TypeError("available output material must be exact bytes")
        elif self.stderr_bytes is not None and type(self.stderr_bytes) is not bytes:
            raise TypeError("available error material must be exact bytes")
        if self.source_reference is not None:
            source_material = getattr(self.source_reference, "exact_material", None)
            if type(source_material) is not bytes:
                raise TypeError("source material requires its exact reference")
            if source_material != self.exact_material:
                raise ValueError("invocation material differs from its exact source")

    @property
    def occurrence_identity(self) -> tuple[str, str, int]:
        return (
            self.boundary_identity,
            self.implementation_function_identity,
            self.invocation_position,
        )

    @property
    def implementation_function_identity(self) -> str:
        return self.implementation_function.identity

    @property
    def coordinates(
        self,
    ) -> MaterialInvocationCoordinates:
        return (
            self.time_limit_second_count,
            self.material_byte_count_limit,
            self.returned,
            self.time_limit_reached,
            self.stdout_byte_count_limit_reached,
            self.stderr_byte_count_limit_reached,
            self.returncode,
            self.stdout_bytes,
            self.stderr_bytes,
        )

    @property
    def return_coordinates(self) -> MaterialInvocationReturnCoordinates:
        return (
            self.time_limit_second_count,
            self.material_byte_count_limit,
            self.returned,
            self.time_limit_reached,
            self.stdout_byte_count_limit_reached,
            self.stderr_byte_count_limit_reached,
            self.returncode,
        )

    @property
    def result_identity(self) -> tuple[str, str, int, str]:
        return (*self.occurrence_identity, "result")

    @property
    def result_reference(self) -> MaterialInvocationResultReference:
        return MaterialInvocationResultReference(invocation_occurrence=self)


@dataclass(frozen=True, slots=True)
class MaterialReferenceCompareOccurrence:
    boundary_identity: str
    occurrence_position: int
    first_invocation: MaterialInvocationOccurrence
    second_invocation: MaterialInvocationOccurrence

    def __post_init__(self) -> None:
        if type(self.boundary_identity) is not str or not self.boundary_identity:
            raise TypeError("one exact Compare boundary identity is required")
        if type(self.occurrence_position) is not int or self.occurrence_position < 0:
            raise TypeError("one exact Compare occurrence position is required")
        if not isinstance(
            self.first_invocation, MaterialInvocationOccurrence
        ) or not isinstance(self.second_invocation, MaterialInvocationOccurrence):
            raise TypeError("Compare requires exact invocation occurrences")
        if (
            self.first_invocation.implementation_function
            != self.second_invocation.implementation_function
        ):
            raise ValueError("Compare cannot cross implementation functions")
        if self.first_invocation.source_reference is None or (
            self.second_invocation.source_reference is None
        ):
            raise ValueError("Compare requires exact source references")
        if (
            self.first_invocation.source_reference
            == self.second_invocation.source_reference
        ):
            raise ValueError("one exact material reference cannot compare with itself")
        if (
            getattr(self.first_invocation.source_reference, "locality_identity", None)
            != getattr(
                self.second_invocation.source_reference,
                "locality_identity",
                None,
            )
        ):
            raise ValueError("Compare material crossed Localities")

    @property
    def implementation_function_identity(self) -> str:
        return self.first_invocation.implementation_function_identity

    @property
    def first_reference(self):
        return self.first_invocation.source_reference

    @property
    def second_reference(self):
        return self.second_invocation.source_reference

    @property
    def occurrence_identity(self) -> tuple[str, str, int]:
        return (
            self.boundary_identity,
            self.implementation_function_identity,
            self.occurrence_position,
        )

    @property
    def result_identity(self) -> tuple[str, str, int, str]:
        return (*self.occurrence_identity, "result")

    @property
    def distinction(self) -> bool:
        return self.first_invocation.coordinates != self.second_invocation.coordinates


@dataclass(frozen=True, slots=True)
class MaterialAdmissionOccurrence:
    admission_occurrence: AdmissionOccurrence
    invocation_result_references: tuple[MaterialInvocationResultReference, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.admission_occurrence, AdmissionOccurrence):
            raise TypeError("material Admission requires its exact Act occurrence")
        if (
            type(self.invocation_result_references) is not tuple
            or not self.invocation_result_references
            or any(
                not isinstance(reference, MaterialInvocationResultReference)
                for reference in self.invocation_result_references
            )
        ):
            raise TypeError("material Admission requires exact invocation results")
        invocation_occurrences = tuple(
            reference.invocation_occurrence
            for reference in self.invocation_result_references
        )
        implementation_functions = {
            occurrence.implementation_function
            for occurrence in invocation_occurrences
        }
        if len(implementation_functions) != 1:
            raise ValueError("one material Admission cannot cross implementation functions")
        if len(
            {
                occurrence.time_limit_second_count
                for occurrence in invocation_occurrences
            }
        ) != 1:
            raise ValueError("one material Admission cannot cross time limits")
        source_material = tuple(
            occurrence.source_reference for occurrence in invocation_occurrences
        )
        if any(source is None for source in source_material):
            raise ValueError("material Admission requires exact source references")
        if source_material != self.admission_occurrence.source_material:
            raise ValueError("material Admission source differs from its invocations")
        same_coordinates = {}
        for occurrence in invocation_occurrences:
            same_coordinates.setdefault(occurrence.coordinates, []).append(
                occurrence.source_reference
            )
        admitted_material = tuple(
            tuple(material) for material in same_coordinates.values()
        )
        if admitted_material != self.admission_occurrence.admitted_material:
            raise ValueError("material Admission differs from its invocation results")

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
class _MaterialFunctionsAdmissionReading:
    occurrence_rows: tuple[tuple[MaterialInvocationOccurrence, ...], ...]
    source_material: tuple[Hashable, ...] = field(init=False)
    admitted_material: tuple[tuple[Hashable, ...], ...] = field(init=False)
    invocation_result_references: tuple[
        MaterialInvocationResultReference, ...
    ] = field(init=False)

    def __post_init__(self) -> None:
        if type(self.occurrence_rows) is not tuple or not self.occurrence_rows:
            raise TypeError(
                "material functions Admission requires exact invocation tuples"
            )
        if any(
            type(row) is not tuple
            or not row
            or any(
                not isinstance(occurrence, MaterialInvocationOccurrence)
                for occurrence in row
            )
            for row in self.occurrence_rows
        ):
            raise TypeError(
                "material functions Admission requires exact invocation tuples"
            )
        identities = tuple(
            row[0].implementation_function_identity for row in self.occurrence_rows
        )
        if len(set(identities)) != len(identities) or any(
            any(
                occurrence.implementation_function_identity != identity
                for occurrence in row
            )
            for identity, row in zip(identities, self.occurrence_rows)
        ):
            raise ValueError(
                "each material functions tuple requires one exact function"
            )
        for row in self.occurrence_rows:
            implementation_function = row[0].implementation_function
            if any(
                occurrence.implementation_function != implementation_function
                for occurrence in row[1:]
            ):
                raise ValueError(
                    "one implementation identity names different functions"
                )
        source_rows = tuple(
            tuple(occurrence.source_reference for occurrence in row)
            for row in self.occurrence_rows
        )
        if any(source is None for row in source_rows for source in row):
            raise ValueError("material functions Admission requires exact source references")
        source_material = source_rows[0]
        if any(row != source_material for row in source_rows[1:]):
            raise ValueError("material functions require the same exact material")
        same_coordinates = {}
        for position, source in enumerate(source_material):
            coordinates = tuple(
                (identity, row[position].coordinates)
                for identity, row in zip(identities, self.occurrence_rows)
            )
            same_coordinates.setdefault(coordinates, []).append(source)
        admitted_material = tuple(
            tuple(material) for material in same_coordinates.values()
        )
        object.__setattr__(self, "source_material", source_material)
        object.__setattr__(self, "admitted_material", admitted_material)
        object.__setattr__(
            self,
            "invocation_result_references",
            tuple(
                occurrence.result_reference
                for row in self.occurrence_rows
                for occurrence in row
            ),
        )


def _material_functions_admission_reading(
    occurrence_rows: tuple[tuple[MaterialInvocationOccurrence, ...], ...],
) -> _MaterialFunctionsAdmissionReading:
    return _MaterialFunctionsAdmissionReading(occurrence_rows)


@dataclass(frozen=True, slots=True)
class MaterialFunctionsAdmissionOccurrence:
    admission_occurrence: AdmissionOccurrence
    invocation_result_references: tuple[MaterialInvocationResultReference, ...]
    _reading: InitVar[_MaterialFunctionsAdmissionReading | None] = None

    def __post_init__(
        self,
        _reading: _MaterialFunctionsAdmissionReading | None,
    ) -> None:
        if not isinstance(self.admission_occurrence, AdmissionOccurrence):
            raise TypeError("material functions Admission requires its exact Act occurrence")
        if (
            type(self.invocation_result_references) is not tuple
            or not self.invocation_result_references
            or any(
                not isinstance(reference, MaterialInvocationResultReference)
                for reference in self.invocation_result_references
            )
        ):
            raise TypeError("material functions Admission requires exact invocation results")
        if _reading is None:
            rows = {}
            for reference in self.invocation_result_references:
                occurrence = reference.invocation_occurrence
                rows.setdefault(
                    occurrence.implementation_function_identity,
                    [],
                ).append(occurrence)
            reading = _material_functions_admission_reading(
                tuple(tuple(row) for row in rows.values())
            )
        elif type(_reading) is not _MaterialFunctionsAdmissionReading:
            raise TypeError(
                "material functions Admission reading must be exact"
            )
        else:
            reading = _reading
        if reading.invocation_result_references != self.invocation_result_references:
            raise ValueError(
                "material functions Admission reading differs from its invocation results"
            )
        if reading.source_material != self.admission_occurrence.source_material:
            raise ValueError("material functions Admission source differs from its invocations")
        if reading.admitted_material != self.admission_occurrence.admitted_material:
            raise ValueError("material functions Admission differs from its invocation results")

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
class MaterialReturnAdmissionOccurrence:
    admission_occurrence: AdmissionOccurrence
    invocation_result_references: tuple[MaterialInvocationResultReference, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.admission_occurrence, AdmissionOccurrence):
            raise TypeError("return Admission requires its exact Act occurrence")
        if (
            type(self.invocation_result_references) is not tuple
            or not self.invocation_result_references
            or any(
                not isinstance(reference, MaterialInvocationResultReference)
                for reference in self.invocation_result_references
            )
        ):
            raise TypeError("return Admission requires exact invocation results")
        invocation_occurrences = tuple(
            reference.invocation_occurrence
            for reference in self.invocation_result_references
        )
        if len(
            {
                occurrence.implementation_function
                for occurrence in invocation_occurrences
            }
        ) != 1:
            raise ValueError("one return Admission cannot cross implementation functions")
        source_material = tuple(
            occurrence.source_reference for occurrence in invocation_occurrences
        )
        if any(source is None for source in source_material):
            raise ValueError("return Admission requires exact source references")
        if source_material != self.admission_occurrence.source_material:
            raise ValueError("return Admission source differs from its invocations")
        same_coordinates = {}
        for occurrence in invocation_occurrences:
            same_coordinates.setdefault(occurrence.return_coordinates, []).append(
                occurrence.source_reference
            )
        admitted_material = tuple(
            tuple(material) for material in same_coordinates.values()
        )
        if admitted_material != self.admission_occurrence.admitted_material:
            raise ValueError("return Admission differs from its invocation results")

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
class MaterialLocalityAdmissionOccurrence:
    locality_identity: str
    material_admission: MaterialAdmissionOccurrence

    def __post_init__(self) -> None:
        if type(self.locality_identity) is not str or not self.locality_identity:
            raise TypeError("material Admission requires one exact Locality")
        if not isinstance(self.material_admission, MaterialAdmissionOccurrence):
            raise TypeError("material Locality requires one exact Admission occurrence")
        if any(
            getattr(material, "locality_identity", None) != self.locality_identity
            for material in self.material_admission.source_material
        ):
            raise ValueError("material Admission crossed Localities")

    @property
    def act_occurrence_identity(self) -> tuple[str, int]:
        return self.material_admission.act_occurrence_identity

    @property
    def result_identity(self) -> tuple[str, int, str]:
        return self.material_admission.result_identity

    @property
    def source_material(self):
        return self.material_admission.source_material

    @property
    def admitted_material(self):
        return self.material_admission.admitted_material

    @property
    def result_reference(self) -> AdmissionResultReference:
        return self.material_admission.result_reference


ASPELL_US = MaterialImplementationFunction(
    identity="aspell-en-US",
    invocation=("aspell", "--lang=en_US", "pipe"),
)
ASPELL_GB = MaterialImplementationFunction(
    identity="aspell-en-GB",
    invocation=("aspell", "--lang=en_GB", "pipe"),
)
ENCHANT_US = MaterialImplementationFunction(
    identity="enchant-en-US",
    invocation=("enchant-2", "-a", "-d", "en_US"),
)
ENCHANT_GB = MaterialImplementationFunction(
    identity="enchant-en-GB",
    invocation=("enchant-2", "-a", "-d", "en_GB"),
)
MATERIAL_IMPLEMENTATION_FUNCTIONS = (
    ASPELL_US,
    ASPELL_GB,
    ENCHANT_US,
    ENCHANT_GB,
)


def ingest_result_reference(
    ledger: EventLedger, recorded_occurrence_identity: str
) -> IngestResultReference:
    if not isinstance(ledger, EventLedger):
        raise TypeError("Ingest result reference requires one EventLedger")
    event = ledger.get(recorded_occurrence_identity)
    if event is None or event.kind != MATERIAL_INGEST_OCCURRED_KIND:
        raise ValueError("Ingest result reference requires one Ingest occurrence")
    requirements = read_requirements_of_yield_relation(
        ledger,
        recorded_result_event_identity=event.identity,
        evidence_of_yield_relation_event_identity=event.material.get("evidence_of_yield_relation_identity"),
        responsible_act_evidence_event_identity=event.material.get(
            "responsible_act_evidence_identity"
        ),
    )
    if not all(requirements.values()):
        raise ValueError("Ingest result reference requires its exact Evidence of Yield relation")
    return IngestResultReference(
        recorded_occurrence_identity=event.identity,
        locality_identity=event.locality_identity,
        act_occurrence_identity=event.material["act_occurrence_identity"],
        result_identity=event.material["result_identity"],
        evidence_of_yield_relation_identity=event.material["evidence_of_yield_relation_identity"],
        exact_material=event.exact_material,
    )


def invocation_occurrence(
    exact_material: bytes,
    implementation_function: MaterialImplementationFunction,
    *,
    boundary_identity: str,
    invocation_position: int = 0,
    source_reference: Hashable | None = None,
    time_limit_second_count: float = 30.0,
    material_byte_count_limit: int | None = None,
) -> MaterialInvocationOccurrence:
    if type(exact_material) is not bytes:
        raise TypeError("implementation function material must be exact bytes")
    if not isinstance(implementation_function, MaterialImplementationFunction):
        raise TypeError("one material implementation function is required")
    if (
        type(time_limit_second_count) is not float
        or time_limit_second_count <= 0
    ):
        raise TypeError("one exact positive time limit second count is required")
    if material_byte_count_limit is not None and (
        type(material_byte_count_limit) is not int
        or material_byte_count_limit < 1
    ):
        raise TypeError("one exact positive material byte count limit is required")
    if material_byte_count_limit is not None:
        return _byte_bounded_invocation_occurrence(
            exact_material,
            implementation_function,
            boundary_identity=boundary_identity,
            invocation_position=invocation_position,
            source_reference=source_reference,
            time_limit_second_count=time_limit_second_count,
            material_byte_count_limit=material_byte_count_limit,
        )
    try:
        completed = subprocess.run(
            implementation_function.invocation,
            input=exact_material,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            timeout=time_limit_second_count,
        )
    except subprocess.TimeoutExpired as occurrence:
        return MaterialInvocationOccurrence(
            boundary_identity=boundary_identity,
            invocation_position=invocation_position,
            exact_material=exact_material,
            implementation_function=implementation_function,
            returned=False,
            returncode=None,
            stdout_bytes=occurrence.stdout,
            stderr_bytes=occurrence.stderr,
            source_reference=source_reference,
            time_limit_second_count=time_limit_second_count,
            time_limit_reached=True,
        )
    return MaterialInvocationOccurrence(
        boundary_identity=boundary_identity,
        invocation_position=invocation_position,
        exact_material=exact_material,
        implementation_function=implementation_function,
        returned=True,
        returncode=completed.returncode,
        stdout_bytes=completed.stdout,
        stderr_bytes=completed.stderr,
        source_reference=source_reference,
        time_limit_second_count=time_limit_second_count,
    )


def _byte_bounded_invocation_occurrence(
    exact_material,
    implementation_function,
    *,
    boundary_identity,
    invocation_position,
    source_reference,
    time_limit_second_count,
    material_byte_count_limit,
):
    streams = selectors.DefaultSelector()
    process = subprocess.Popen(
        implementation_function.invocation,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        bufsize=0,
    )
    input_position = 0
    stdout = bytearray()
    stderr = bytearray()
    time_limit_reached = False
    stdout_limit_reached = False
    stderr_limit_reached = False

    def end_process() -> None:
        if process.poll() is None:
            try:
                process.kill()
            except ProcessLookupError:
                pass

    for stream in (process.stdin, process.stdout, process.stderr):
        os.set_blocking(stream.fileno(), False)
    streams.register(process.stdin, selectors.EVENT_WRITE, "stdin")
    streams.register(process.stdout, selectors.EVENT_READ, "stdout")
    streams.register(process.stderr, selectors.EVENT_READ, "stderr")
    deadline = time.monotonic() + time_limit_second_count
    try:
        while streams.get_map():
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                time_limit_reached = True
                end_process()
                if process.stdin in tuple(
                    key.fileobj for key in streams.get_map().values()
                ):
                    streams.unregister(process.stdin)
                    process.stdin.close()
                remaining = 0.05
            for key, _ in streams.select(min(remaining, 0.05)):
                stream = key.fileobj
                if key.data == "stdin":
                    try:
                        count = os.write(
                            stream.fileno(), exact_material[input_position:]
                        )
                    except BrokenPipeError:
                        count = 0
                        input_position = len(exact_material)
                    else:
                        input_position += count
                    if input_position == len(exact_material):
                        streams.unregister(stream)
                        stream.close()
                    continue
                try:
                    found = os.read(stream.fileno(), 65536)
                except BlockingIOError:
                    continue
                if not found:
                    streams.unregister(stream)
                    stream.close()
                    continue
                material = stdout if key.data == "stdout" else stderr
                available = material_byte_count_limit - len(material)
                material.extend(found[:available])
                if len(found) > available:
                    if key.data == "stdout":
                        stdout_limit_reached = True
                    else:
                        stderr_limit_reached = True
                    end_process()
            if process.poll() is not None and len(streams.get_map()) == 1:
                remaining_stream = next(iter(streams.get_map().values())).fileobj
                if remaining_stream is process.stdin:
                    streams.unregister(remaining_stream)
                    remaining_stream.close()
    except BaseException:
        end_process()
        raise
    finally:
        streams.close()
        for stream in (process.stdin, process.stdout, process.stderr):
            if not stream.closed:
                stream.close()
        process.wait()
    returned = not (
        time_limit_reached or stdout_limit_reached or stderr_limit_reached
    )
    return MaterialInvocationOccurrence(
        boundary_identity=boundary_identity,
        invocation_position=invocation_position,
        exact_material=exact_material,
        implementation_function=implementation_function,
        returned=returned,
        returncode=process.returncode if returned else None,
        stdout_bytes=bytes(stdout),
        stderr_bytes=bytes(stderr),
        source_reference=source_reference,
        time_limit_second_count=time_limit_second_count,
        material_byte_count_limit=material_byte_count_limit,
        time_limit_reached=time_limit_reached,
        stdout_byte_count_limit_reached=stdout_limit_reached,
        stderr_byte_count_limit_reached=stderr_limit_reached,
    )


def occurrences_across(
    exact_materials: tuple[bytes, ...],
    *,
    boundary_identity: str,
    implementation_functions: tuple[
        MaterialImplementationFunction, ...
    ] = MATERIAL_IMPLEMENTATION_FUNCTIONS,
    time_limit_second_count: float = 30.0,
    material_byte_count_limit: int | None = None,
) -> tuple[tuple[MaterialInvocationOccurrence, ...], ...]:
    return _occurrences_across(
        exact_materials,
        boundary_identity=boundary_identity,
        implementation_functions=implementation_functions,
        time_limit_second_count=time_limit_second_count,
        material_byte_count_limit=material_byte_count_limit,
    )


def reference_occurrences_across(
    references: tuple[Hashable, ...],
    *,
    boundary_identity: str,
    implementation_functions: tuple[
        MaterialImplementationFunction, ...
    ] = MATERIAL_IMPLEMENTATION_FUNCTIONS,
    max_workers: int = 16,
    time_limit_second_count: float = 30.0,
    material_byte_count_limit: int | None = None,
) -> tuple[tuple[MaterialInvocationOccurrence, ...], ...]:
    if type(references) is not tuple or any(
        type(getattr(reference, "exact_material", None)) is not bytes
        for reference in references
    ):
        raise TypeError("implementation function inputs require exact references")
    return _occurrences_across(
        tuple(reference.exact_material for reference in references),
        boundary_identity=boundary_identity,
        implementation_functions=implementation_functions,
        source_references=references,
        max_workers=max_workers,
        time_limit_second_count=time_limit_second_count,
        material_byte_count_limit=material_byte_count_limit,
    )


def compare_material_reference_invocations(
    invocation_rows: tuple[tuple[MaterialInvocationOccurrence, ...], ...],
    reference_pairs: tuple[tuple[Hashable, Hashable], ...],
    *,
    boundary_identity: str,
) -> tuple[tuple[MaterialReferenceCompareOccurrence, ...], ...]:
    if (
        type(invocation_rows) is not tuple
        or not invocation_rows
        or any(
            type(row) is not tuple
            or not row
            or any(
                not isinstance(occurrence, MaterialInvocationOccurrence)
                for occurrence in row
            )
            for row in invocation_rows
        )
    ):
        raise TypeError("Compare requires exact invocation tuples")
    if (
        type(reference_pairs) is not tuple
        or not reference_pairs
        or any(
            type(pair) is not tuple
            or len(pair) != 2
            or any(
                type(getattr(reference, "exact_material", None)) is not bytes
                for reference in pair
            )
            for pair in reference_pairs
        )
    ):
        raise TypeError("Compare requires exact material reference pairs")
    if type(boundary_identity) is not str or not boundary_identity:
        raise TypeError("one exact Compare boundary identity is required")
    if any(first == second for first, second in reference_pairs):
        raise ValueError("one exact material reference cannot compare with itself")
    if len(set(reference_pairs)) != len(reference_pairs):
        raise ValueError("one exact material pair entered Compare twice")
    source_rows = tuple(
        tuple(occurrence.source_reference for occurrence in row)
        for row in invocation_rows
    )
    if any(source is None for row in source_rows for source in row):
        raise ValueError("Compare requires exact source references")
    sources = source_rows[0]
    if any(row != sources for row in source_rows[1:]):
        raise ValueError("Compare invocation tuples crossed their sources")
    by_source_position = {source: position for position, source in enumerate(sources)}
    if len(by_source_position) != len(sources):
        raise ValueError("one exact material reference entered invocation twice")
    if any(
        first not in by_source_position or second not in by_source_position
        for first, second in reference_pairs
    ):
        raise ValueError("Compare reference is absent from its invocation boundary")
    found = []
    for row in invocation_rows:
        implementation_function = row[0].implementation_function
        if any(
            occurrence.implementation_function != implementation_function
            for occurrence in row
        ):
            raise ValueError("Compare tuple crossed implementation functions")
        found.append(
            tuple(
                MaterialReferenceCompareOccurrence(
                    boundary_identity=boundary_identity,
                    occurrence_position=position,
                    first_invocation=row[by_source_position[first]],
                    second_invocation=row[by_source_position[second]],
                )
                for position, (first, second) in enumerate(reference_pairs)
            )
        )
    return tuple(found)


def admit_invocation_occurrences(
    occurrences: tuple[MaterialInvocationOccurrence, ...],
    *,
    boundary_identity: str,
    occurrence_position: int = 0,
) -> MaterialAdmissionOccurrence:
    if type(occurrences) is not tuple or not occurrences:
        raise TypeError("material Admission requires exact invocation occurrences")
    if any(
        not isinstance(occurrence, MaterialInvocationOccurrence)
        for occurrence in occurrences
    ):
        raise TypeError("material Admission requires exact invocation occurrences")
    same_coordinates = {}
    for occurrence in occurrences:
        if occurrence.source_reference is None:
            raise ValueError("material Admission requires exact source references")
        same_coordinates.setdefault(occurrence.coordinates, []).append(
            occurrence.source_reference
        )
    admission = admission_occurrence(
        tuple(tuple(material) for material in same_coordinates.values()),
        boundary_identity=boundary_identity,
        occurrence_position=occurrence_position,
        source_material=tuple(
            occurrence.source_reference for occurrence in occurrences
        ),
    )
    return MaterialAdmissionOccurrence(
        admission_occurrence=admission,
        invocation_result_references=tuple(
            occurrence.result_reference for occurrence in occurrences
        ),
    )


def admit_invocation_rows(
    occurrence_rows: tuple[tuple[MaterialInvocationOccurrence, ...], ...],
    *,
    boundary_identity: str,
    occurrence_position: int = 0,
) -> MaterialFunctionsAdmissionOccurrence:
    reading = _material_functions_admission_reading(occurrence_rows)
    admission = admission_occurrence(
        reading.admitted_material,
        boundary_identity=boundary_identity,
        occurrence_position=occurrence_position,
        source_material=reading.source_material,
    )
    return MaterialFunctionsAdmissionOccurrence(
        admission_occurrence=admission,
        invocation_result_references=reading.invocation_result_references,
        _reading=reading,
    )


def admit_invocation_return_occurrences(
    occurrences: tuple[MaterialInvocationOccurrence, ...],
    *,
    boundary_identity: str,
    occurrence_position: int = 0,
) -> MaterialReturnAdmissionOccurrence:
    if type(occurrences) is not tuple or not occurrences:
        raise TypeError("return Admission requires exact invocation occurrences")
    if any(
        not isinstance(occurrence, MaterialInvocationOccurrence)
        for occurrence in occurrences
    ):
        raise TypeError("return Admission requires exact invocation occurrences")
    same_coordinates = {}
    for occurrence in occurrences:
        if occurrence.source_reference is None:
            raise ValueError("return Admission requires exact source references")
        same_coordinates.setdefault(occurrence.return_coordinates, []).append(
            occurrence.source_reference
        )
    admission = admission_occurrence(
        tuple(tuple(material) for material in same_coordinates.values()),
        boundary_identity=boundary_identity,
        occurrence_position=occurrence_position,
        source_material=tuple(
            occurrence.source_reference for occurrence in occurrences
        ),
    )
    return MaterialReturnAdmissionOccurrence(
        admission_occurrence=admission,
        invocation_result_references=tuple(
            occurrence.result_reference for occurrence in occurrences
        ),
    )


def material_locality_admission_occurrences(
    occurrences: tuple[MaterialInvocationOccurrence, ...],
    *,
    boundary_identity: str,
) -> tuple[MaterialLocalityAdmissionOccurrence, ...]:
    if type(occurrences) is not tuple or not occurrences:
        raise TypeError("material Localities require exact invocation occurrences")
    if any(
        not isinstance(occurrence, MaterialInvocationOccurrence)
        for occurrence in occurrences
    ):
        raise TypeError("material Localities require exact invocation occurrences")
    if type(boundary_identity) is not str or not boundary_identity:
        raise TypeError("one exact boundary identity is required")
    by_locality = {}
    for occurrence in occurrences:
        locality_identity = getattr(
            occurrence.source_reference, "locality_identity", None
        )
        if type(locality_identity) is not str or not locality_identity:
            raise TypeError("material Admission requires its exact source Locality")
        by_locality.setdefault(locality_identity, []).append(occurrence)
    return tuple(
        MaterialLocalityAdmissionOccurrence(
            locality_identity=locality_identity,
            material_admission=admit_invocation_occurrences(
                tuple(locality_occurrences),
                boundary_identity=boundary_identity,
                occurrence_position=position,
            ),
        )
        for position, (locality_identity, locality_occurrences) in enumerate(
            by_locality.items()
        )
    )


def _occurrences_across(
    exact_materials: tuple[bytes, ...],
    *,
    boundary_identity: str,
    implementation_functions: tuple[MaterialImplementationFunction, ...],
    source_references: tuple[Hashable, ...] | None = None,
    max_workers: int = 16,
    time_limit_second_count: float = 30.0,
    material_byte_count_limit: int | None = None,
) -> tuple[tuple[MaterialInvocationOccurrence, ...], ...]:
    if type(exact_materials) is not tuple or any(
        type(material) is not bytes for material in exact_materials
    ):
        raise TypeError(
            "implementation function inputs must be one exact tuple of bytes"
        )
    if type(boundary_identity) is not str or not boundary_identity:
        raise TypeError("one exact boundary identity is required")
    if type(implementation_functions) is not tuple or not implementation_functions:
        raise TypeError("material implementation functions must be one nonempty tuple")
    if any(
        not isinstance(implementation_function, MaterialImplementationFunction)
        for implementation_function in implementation_functions
    ):
        raise TypeError("material implementation functions must be exact")
    implementation_function_identities = tuple(
        implementation_function.identity
        for implementation_function in implementation_functions
    )
    if len(set(implementation_function_identities)) != len(
        implementation_function_identities
    ):
        raise ValueError("implementation function identities must be distinct")
    if source_references is not None and len(source_references) != len(exact_materials):
        raise ValueError("each material requires its exact source reference")
    if type(max_workers) is not int or max_workers < 1:
        raise TypeError("invocation count must be one positive integer")
    if (
        type(time_limit_second_count) is not float
        or time_limit_second_count <= 0
    ):
        raise TypeError("one exact positive time limit second count is required")
    if not exact_materials:
        return tuple(() for _ in implementation_functions)
    calls = tuple(
        (
            material,
            implementation_function,
            invocation_position,
            source_references[invocation_position]
            if source_references is not None
            else None,
        )
        for implementation_function in implementation_functions
        for invocation_position, material in enumerate(exact_materials)
    )

    def invoke(call) -> MaterialInvocationOccurrence:
        material, implementation_function, position, source_reference = call
        return invocation_occurrence(
            material,
            implementation_function,
            boundary_identity=boundary_identity,
            invocation_position=position,
            source_reference=source_reference,
            time_limit_second_count=time_limit_second_count,
            material_byte_count_limit=material_byte_count_limit,
        )

    with ThreadPoolExecutor(max_workers=min(max_workers, len(calls))) as workers:
        occurrences = tuple(workers.map(invoke, calls))
    width = len(exact_materials)
    return tuple(
        occurrences[offset : offset + width]
        for offset in range(0, len(occurrences), width)
    )


def compare_added_material_invocations(
    additions: tuple[AddedPositionOccurrence, ...],
    source_invocations: tuple[tuple[MaterialInvocationOccurrence, ...], ...],
    result_invocations: tuple[tuple[MaterialInvocationOccurrence, ...], ...],
    *,
    boundary_identity: str,
) -> tuple[tuple[MaterialAddedCompareOccurrence, ...], ...]:
    return _compare_added_material_invocations(
        additions,
        source_invocations,
        result_invocations,
        boundary_identity=boundary_identity,
        compare_occurrence=MaterialAddedCompareOccurrence,
    )


def compare_added_material_return_invocations(
    additions: tuple[AddedPositionOccurrence, ...],
    source_invocations: tuple[tuple[MaterialInvocationOccurrence, ...], ...],
    result_invocations: tuple[tuple[MaterialInvocationOccurrence, ...], ...],
    *,
    boundary_identity: str,
) -> tuple[tuple[MaterialAddedReturnCompareOccurrence, ...], ...]:
    return _compare_added_material_invocations(
        additions,
        source_invocations,
        result_invocations,
        boundary_identity=boundary_identity,
        compare_occurrence=MaterialAddedReturnCompareOccurrence,
    )


def compare_removed_material_invocations(
    removals: tuple[RemovedPositionOccurrence, ...],
    source_invocations: tuple[tuple[MaterialInvocationOccurrence, ...], ...],
    result_invocations: tuple[tuple[MaterialInvocationOccurrence, ...], ...],
    *,
    boundary_identity: str,
) -> tuple[tuple[MaterialRemovedCompareOccurrence, ...], ...]:
    if type(removals) is not tuple or not removals or any(
        not isinstance(removal, RemovedPositionOccurrence) for removal in removals
    ):
        raise TypeError("Compare requires exact removal Act occurrences")
    if (
        type(source_invocations) is not tuple
        or type(result_invocations) is not tuple
    ):
        raise TypeError("Compare requires exact invocation tuples")
    if len(source_invocations) != len(result_invocations):
        raise ValueError("Compare requires the same implementation functions")
    if type(boundary_identity) is not str or not boundary_identity:
        raise TypeError("one exact boundary identity is required")

    found = []
    occurrence_position = 0
    for source_row, result_row in zip(source_invocations, result_invocations):
        if (
            type(source_row) is not tuple
            or type(result_row) is not tuple
            or not source_row
            or not result_row
            or any(
                not isinstance(invocation, MaterialInvocationOccurrence)
                for invocation in (*source_row, *result_row)
            )
        ):
            raise TypeError("Compare requires exact invocation occurrences")
        implementation_function = source_row[0].implementation_function
        if any(
            invocation.implementation_function != implementation_function
            for invocation in (*source_row, *result_row)
        ):
            raise ValueError("Compare cannot cross implementation functions")
        source_by_reference = {
            invocation.source_reference: invocation for invocation in source_row
        }
        result_by_reference = {
            invocation.source_reference: invocation for invocation in result_row
        }
        if len(source_by_reference) != len(source_row):
            raise ValueError("source reference entered removal Compare twice")
        if len(result_by_reference) != len(result_row):
            raise ValueError("result reference entered removal Compare twice")

        row = []
        for removal in removals:
            source = source_by_reference.get(removal.source_reference)
            result = result_by_reference.get(removal.result_reference)
            if source is None or result is None:
                raise ValueError(
                    "Compare requires each exact removal source and result invocation"
                )
            row.append(
                MaterialRemovedCompareOccurrence(
                    boundary_identity=boundary_identity,
                    occurrence_position=occurrence_position,
                    removal_occurrence=removal,
                    source_invocation=source,
                    result_invocation=result,
                )
            )
            occurrence_position += 1
        found.append(tuple(row))
    return tuple(found)


def recurring_added_result_coordinates(
    comparisons: tuple[MaterialAddedCompareOccurrence, ...],
    addition: AddedPositionOccurrence,
    source_invocation: MaterialInvocationOccurrence,
) -> MaterialInvocationCoordinates | MaterialInvocationReturnCoordinates | None:
    if (
        type(comparisons) is not tuple
        or len(comparisons) < 2
        or any(
            not isinstance(comparison, MaterialAddedCompareOccurrence)
            for comparison in comparisons
        )
    ):
        raise TypeError("recurrence requires exact Compare occurrences")
    if not isinstance(addition, AddedPositionOccurrence) or not isinstance(
        source_invocation, MaterialInvocationOccurrence
    ):
        raise TypeError("recurrence requires one exact addition and source invocation")
    comparison_type = type(comparisons[0])
    if any(type(comparison) is not comparison_type for comparison in comparisons):
        raise TypeError("recurrence cannot cross Compare coordinates")
    if (
        addition.source_admission_result_reference is None
        or addition.added_admission_result_reference is None
    ):
        return None
    if source_invocation.source_reference != addition.source_reference:
        raise ValueError("source invocation differs from the addition Act")

    addition_coordinates = (
        addition.source_admission_result_reference.result_identity,
        addition.source_admitted_material_position,
        addition.added_admission_result_reference.result_identity,
        addition.added_admitted_material_position,
        addition.position,
        len(addition.source_material),
        len(addition.added_material),
    )
    source_coordinates = (
        source_invocation.return_coordinates
        if comparison_type is MaterialAddedReturnCompareOccurrence
        else source_invocation.coordinates
    )
    found = []
    occurrence_identities = set()
    for comparison in comparisons:
        prior = comparison.addition_occurrence
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
            and comparison.source_coordinates == source_coordinates
            and prior.act_occurrence_identity != addition.act_occurrence_identity
            and prior.result_material != addition.result_material
        ):
            found.append(comparison.result_coordinates)
            occurrence_identities.add(comparison.occurrence_identity)
    if len(occurrence_identities) < 2 or len(set(found)) != 1:
        return None
    return found[0]


def first_recurring_added_return_compare(
    additions: tuple[AddedPositionOccurrence, ...],
    source_invocations: tuple[MaterialInvocationOccurrence, ...],
    implementation_function: MaterialImplementationFunction,
    *,
    boundary_identity: str,
    act_occurrence_count_limit: int,
    invoke_later: bool = True,
) -> tuple[
    tuple[MaterialAddedReturnCompareOccurrence, ...],
    MaterialInvocationReturnCoordinates | None,
    MaterialAddedReturnCompareOccurrence | None,
]:
    if type(additions) is not tuple or not additions or any(
        not isinstance(addition, AddedPositionOccurrence) for addition in additions
    ):
        raise TypeError("recurrence requires exact addition Act occurrences")
    if type(source_invocations) is not tuple or not source_invocations or any(
        not isinstance(invocation, MaterialInvocationOccurrence)
        for invocation in source_invocations
    ):
        raise TypeError("recurrence requires exact source invocation occurrences")
    if not isinstance(implementation_function, MaterialImplementationFunction):
        raise TypeError("recurrence requires one exact implementation function")
    if type(boundary_identity) is not str or not boundary_identity:
        raise TypeError("one exact boundary identity is required")
    if (
        type(act_occurrence_count_limit) is not int
        or act_occurrence_count_limit < 1
    ):
        raise TypeError("one exact positive Act occurrence count limit is required")
    if type(invoke_later) is not bool:
        raise TypeError("later invocation control must be exact")
    source_by_reference = {
        invocation.source_reference: invocation for invocation in source_invocations
    }
    if len(source_by_reference) != len(source_invocations) or any(
        invocation.implementation_function != implementation_function
        for invocation in source_invocations
    ):
        raise ValueError("recurrence source invocations must be exact and distinct")
    if len(
        {invocation.return_coordinates for invocation in source_invocations}
    ) < 2:
        return (), None, None

    comparisons = []
    for addition in additions[:act_occurrence_count_limit]:
        source_invocation = source_by_reference.get(addition.source_reference)
        if source_invocation is None:
            raise ValueError("recurrence requires each exact source invocation")
        coordinates = (
            recurring_added_result_coordinates(
                tuple(comparisons),
                addition,
                source_invocation,
            )
            if len(comparisons) >= 2
            else None
        )
        if coordinates is not None and not invoke_later:
            return tuple(comparisons), coordinates, None
        result_invocation = invocation_occurrence(
            addition.result_material,
            implementation_function,
            boundary_identity=f"{boundary_identity}-invocation",
            invocation_position=len(comparisons),
            source_reference=addition.result_reference,
            time_limit_second_count=source_invocation.time_limit_second_count,
            material_byte_count_limit=source_invocation.material_byte_count_limit,
        )
        comparison = MaterialAddedReturnCompareOccurrence(
            boundary_identity=f"{boundary_identity}-compare",
            occurrence_position=len(comparisons),
            addition_occurrence=addition,
            source_invocation=source_invocation,
            result_invocation=result_invocation,
        )
        if coordinates is not None:
            return tuple(comparisons), coordinates, comparison
        comparisons.append(comparison)
    return tuple(comparisons), None, None


def recurring_added_result_coordinates_across(
    comparison_rows: tuple[tuple[MaterialAddedReturnCompareOccurrence, ...], ...],
    addition: AddedPositionOccurrence,
    source_invocations: tuple[MaterialInvocationOccurrence, ...],
) -> tuple[MaterialInvocationReturnCoordinates, ...] | None:
    if type(comparison_rows) is not tuple or len(comparison_rows) < 2 or any(
        type(row) is not tuple
        or len(row) < 2
        or any(
            not isinstance(comparison, MaterialAddedReturnCompareOccurrence)
            for comparison in row
        )
        for row in comparison_rows
    ):
        raise TypeError("full-function recurrence requires exact Compare tuples")
    if not isinstance(addition, AddedPositionOccurrence):
        raise TypeError("full-function recurrence requires one exact addition")
    if (
        type(source_invocations) is not tuple
        or len(source_invocations) != len(comparison_rows)
        or any(
            not isinstance(invocation, MaterialInvocationOccurrence)
            for invocation in source_invocations
        )
    ):
        raise TypeError("full-function recurrence requires exact source invocations")
    comparison_act_identities = tuple(
        tuple(
            comparison.addition_occurrence.act_occurrence_identity
            for comparison in row
        )
        for row in comparison_rows
    )
    if any(
        row != comparison_act_identities[0]
        for row in comparison_act_identities[1:]
    ):
        raise ValueError("full-function recurrence requires the same exact Acts")
    comparison_function_identities = tuple(
        row[0].implementation_function_identity for row in comparison_rows
    )
    source_function_identities = tuple(
        invocation.implementation_function_identity
        for invocation in source_invocations
    )
    if (
        len(set(comparison_function_identities)) != len(comparison_rows)
        or comparison_function_identities != source_function_identities
        or any(
            any(
                comparison.implementation_function_identity != identity
                for comparison in row
            )
            for identity, row in zip(comparison_function_identities, comparison_rows)
        )
    ):
        raise ValueError(
            "full-function recurrence requires different exact implementation functions"
        )
    if any(
        invocation.source_reference != addition.source_reference
        for invocation in source_invocations
    ):
        raise ValueError("full-function recurrence requires the exact source material")
    coordinates = tuple(
        recurring_added_result_coordinates(row, addition, source_invocation)
        for row, source_invocation in zip(comparison_rows, source_invocations)
    )
    if any(coordinate is None for coordinate in coordinates):
        return None
    return coordinates


def first_recurring_added_return_compare_across(
    additions: tuple[AddedPositionOccurrence, ...],
    source_invocation_rows: tuple[tuple[MaterialInvocationOccurrence, ...], ...],
    *,
    boundary_identity: str,
    act_occurrence_count_limit: int,
) -> tuple[
    tuple[tuple[MaterialAddedReturnCompareOccurrence, ...], ...],
    tuple[MaterialInvocationReturnCoordinates, ...] | None,
    tuple[MaterialAddedReturnCompareOccurrence, ...] | None,
]:
    if type(source_invocation_rows) is not tuple or len(source_invocation_rows) < 2:
        raise TypeError("full-function recurrence requires exact invocation tuples")
    row_lengths = {len(row) for row in source_invocation_rows}
    if len(row_lengths) != 1:
        raise ValueError("full-function recurrence requires one exact source sequence")
    functions = tuple(
        row[0].implementation_function for row in source_invocation_rows if row
    )
    if len(functions) != len(source_invocation_rows) or len(
        {function.identity for function in functions}
    ) != len(functions):
        raise ValueError(
            "full-function recurrence requires different implementation functions"
        )
    source_references = tuple(
        tuple(invocation.source_reference for invocation in row)
        for row in source_invocation_rows
    )
    if any(row != source_references[0] for row in source_references[1:]):
        raise ValueError("full-function recurrence requires one exact source sequence")
    source_by_function = tuple(
        {
            invocation.source_reference: invocation for invocation in row
        }
        for row in source_invocation_rows
    )
    if any(len(found) != len(row) for found, row in zip(source_by_function, source_invocation_rows)):
        raise ValueError("full-function recurrence requires distinct source occurrences")
    comparisons = tuple([] for _ in functions)
    for occurrence_position, addition in enumerate(
        additions[:act_occurrence_count_limit]
    ):
        source_invocations = tuple(
            found.get(addition.source_reference) for found in source_by_function
        )
        if any(invocation is None for invocation in source_invocations):
            raise ValueError("recurrence requires each exact source invocation")
        coordinates = (
            recurring_added_result_coordinates_across(
                tuple(tuple(row) for row in comparisons),
                addition,
                source_invocations,
            )
            if occurrence_position >= 2
            else None
        )
        later = []
        for row, function, source_invocation in zip(
            comparisons, functions, source_invocations
        ):
            result_invocation = invocation_occurrence(
                addition.result_material,
                function,
                boundary_identity=f"{boundary_identity}-{function.identity}-invocation",
                invocation_position=occurrence_position,
                source_reference=addition.result_reference,
                time_limit_second_count=source_invocation.time_limit_second_count,
                material_byte_count_limit=source_invocation.material_byte_count_limit,
            )
            comparison = MaterialAddedReturnCompareOccurrence(
                boundary_identity=f"{boundary_identity}-{function.identity}-compare",
                occurrence_position=occurrence_position,
                addition_occurrence=addition,
                source_invocation=source_invocation,
                result_invocation=result_invocation,
            )
            later.append(comparison)
            if coordinates is None:
                row.append(comparison)
        if coordinates is not None:
            return tuple(tuple(row) for row in comparisons), coordinates, tuple(later)
    return tuple(tuple(row) for row in comparisons), None, None


def _compare_added_material_invocations(
    additions,
    source_invocations,
    result_invocations,
    *,
    boundary_identity,
    compare_occurrence,
):
    if type(additions) is not tuple or not additions:
        raise TypeError("Compare requires exact addition Act occurrences")
    if len(source_invocations) != len(result_invocations):
        raise ValueError("Compare requires the same implementation functions")
    found = []
    position = 0
    for source_row, result_row in zip(source_invocations, result_invocations):
        if not source_row or not result_row:
            raise ValueError("Compare requires exact invocation occurrences")
        if source_row[0].implementation_function != result_row[0].implementation_function:
            raise ValueError("Compare cannot cross implementation functions")
        source_by_reference = {
            invocation.source_reference: invocation for invocation in source_row
        }
        result_by_reference = {
            invocation.source_reference: invocation for invocation in result_row
        }
        row = []
        for addition in additions:
            source = source_by_reference.get(addition.source_reference)
            result = result_by_reference.get(addition.result_reference)
            if source is None or result is None:
                raise ValueError("Compare requires each exact source and result invocation")
            row.append(
                compare_occurrence(
                    boundary_identity=boundary_identity,
                    occurrence_position=position,
                    addition_occurrence=addition,
                    source_invocation=source,
                    result_invocation=result,
                )
            )
            position += 1
        found.append(tuple(row))
    return tuple(found)
