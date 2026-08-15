#!/usr/bin/env python3

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from typing import Hashable
import subprocess

from seed_runtime.events import EventLedger
from seed_runtime.material_ingest import MATERIAL_INGEST_OCCURRED_KIND
from seed_runtime.yield_evidence import read_yield_relation_requirements

from material_admission import (
    AdmissionOccurrence,
    AdmissionResultReference,
    admission_occurrence,
)
from compiled_format_invocation import AddedPositionOccurrence


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
    yield_evidence_identity: str
    exact_material: bytes

    def __post_init__(self) -> None:
        coordinates = (
            self.recorded_occurrence_identity,
            self.locality_identity,
            self.act_occurrence_identity,
            self.result_identity,
            self.yield_evidence_identity,
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
    def coordinates(self) -> tuple[int, bytes, bytes]:
        return self.invocation_occurrence.coordinates


@dataclass(frozen=True, slots=True)
class StdoutMaterialReference:
    invocation_occurrence: "MaterialInvocationOccurrence"

    def __post_init__(self) -> None:
        if not isinstance(self.invocation_occurrence, MaterialInvocationOccurrence):
            raise TypeError("stdout material requires its exact invocation occurrence")

    @property
    def act_occurrence_identity(self) -> tuple[str, str, int]:
        return self.invocation_occurrence.occurrence_identity

    @property
    def result_identity(self) -> tuple[str, str, int, str]:
        return (*self.act_occurrence_identity, "stdout")

    @property
    def exact_material(self) -> bytes:
        return self.invocation_occurrence.stdout_bytes


@dataclass(frozen=True, slots=True)
class IngestedStdoutOccurrence:
    boundary_identity: str
    occurrence_position: int
    stdout_reference: StdoutMaterialReference
    ingest_reference: IngestResultReference

    def __post_init__(self) -> None:
        if type(self.boundary_identity) is not str or not self.boundary_identity:
            raise TypeError("one exact boundary identity is required")
        if type(self.occurrence_position) is not int or self.occurrence_position < 0:
            raise TypeError("one exact occurrence position is required")
        if not isinstance(self.stdout_reference, StdoutMaterialReference):
            raise TypeError("Ingest crossing requires exact stdout material")
        if not isinstance(self.ingest_reference, IngestResultReference):
            raise TypeError("Ingest crossing requires one exact Ingest result")
        if self.stdout_reference.exact_material != self.ingest_reference.exact_material:
            raise ValueError("Ingest material differs from exact stdout material")

    @property
    def occurrence_identity(self) -> tuple[str, int]:
        return (self.boundary_identity, self.occurrence_position)


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
    def distinction(self) -> bool:
        return self.source_invocation.coordinates != self.result_invocation.coordinates


@dataclass(frozen=True, slots=True)
class MaterialInvocationOccurrence:
    boundary_identity: str
    invocation_position: int
    exact_material: bytes
    implementation_function: MaterialImplementationFunction
    returncode: int
    stdout_bytes: bytes
    stderr_bytes: bytes
    source_reference: Hashable | None = None

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
        if type(self.returncode) is not int:
            raise TypeError("return code must be exact")
        if type(self.stdout_bytes) is not bytes or type(self.stderr_bytes) is not bytes:
            raise TypeError("returned material must be exact bytes")
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
    def coordinates(self) -> tuple[int, bytes, bytes]:
        return (self.returncode, self.stdout_bytes, self.stderr_bytes)

    @property
    def result_identity(self) -> tuple[str, str, int, str]:
        return (*self.occurrence_identity, "result")

    @property
    def result_reference(self) -> MaterialInvocationResultReference:
        return MaterialInvocationResultReference(invocation_occurrence=self)

    @property
    def stdout_reference(self) -> StdoutMaterialReference:
        return StdoutMaterialReference(invocation_occurrence=self)


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
    requirements = read_yield_relation_requirements(
        ledger,
        recorded_result_event_identity=event.identity,
        result_evidence_event_identity=event.material.get("yield_evidence_identity"),
        responsible_act_evidence_event_identity=event.material.get(
            "responsible_act_evidence_identity"
        ),
    )
    if not all(requirements.values()):
        raise ValueError("Ingest result reference requires its exact Yield Evidence")
    return IngestResultReference(
        recorded_occurrence_identity=event.identity,
        locality_identity=event.locality_identity,
        act_occurrence_identity=event.material["act_occurrence_identity"],
        result_identity=event.material["result_identity"],
        yield_evidence_identity=event.material["yield_evidence_identity"],
        exact_material=event.exact_material,
    )


def invocation_occurrence(
    exact_material: bytes,
    implementation_function: MaterialImplementationFunction,
    *,
    boundary_identity: str,
    invocation_position: int = 0,
    source_reference: Hashable | None = None,
) -> MaterialInvocationOccurrence:
    if type(exact_material) is not bytes:
        raise TypeError("implementation function material must be exact bytes")
    if not isinstance(implementation_function, MaterialImplementationFunction):
        raise TypeError("one material implementation function is required")
    completed = subprocess.run(
        implementation_function.invocation,
        input=exact_material,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        timeout=30,
    )
    return MaterialInvocationOccurrence(
        boundary_identity=boundary_identity,
        invocation_position=invocation_position,
        exact_material=exact_material,
        implementation_function=implementation_function,
        returncode=completed.returncode,
        stdout_bytes=completed.stdout,
        stderr_bytes=completed.stderr,
        source_reference=source_reference,
    )


def occurrences_across(
    exact_materials: tuple[bytes, ...],
    *,
    boundary_identity: str,
    implementation_functions: tuple[
        MaterialImplementationFunction, ...
    ] = MATERIAL_IMPLEMENTATION_FUNCTIONS,
) -> tuple[tuple[MaterialInvocationOccurrence, ...], ...]:
    return _occurrences_across(
        exact_materials,
        boundary_identity=boundary_identity,
        implementation_functions=implementation_functions,
    )


def reference_occurrences_across(
    references: tuple[Hashable, ...],
    *,
    boundary_identity: str,
    implementation_functions: tuple[
        MaterialImplementationFunction, ...
    ] = MATERIAL_IMPLEMENTATION_FUNCTIONS,
    max_workers: int = 16,
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
    )


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


def _occurrences_across(
    exact_materials: tuple[bytes, ...],
    *,
    boundary_identity: str,
    implementation_functions: tuple[MaterialImplementationFunction, ...],
    source_references: tuple[Hashable, ...] | None = None,
    max_workers: int = 16,
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
                MaterialAddedCompareOccurrence(
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
