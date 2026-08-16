"""Exact material supplied by one invocation boundary."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from seed_runtime.event import Event
from seed_runtime.events import CORRUPTED, EventLedger
from seed_runtime.material_ingest import (
    MATERIAL_INGEST_OCCURRED_KIND,
    ingest_material,
)


@dataclass(frozen=True, slots=True)
class SuppliedMaterialOccurrence:
    exact_bytes: bytes
    source_boundary: str
    known_loss: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if type(self.exact_bytes) is not bytes:
            raise TypeError("exact material required")
        if type(self.source_boundary) is not str or not self.source_boundary:
            raise TypeError("exact source boundary required")
        if type(self.known_loss) is not tuple or any(
            type(item) is not str for item in self.known_loss
        ):
            raise TypeError("exact known loss required")


@dataclass(frozen=True, slots=True)
class SuppliedInvocationMaterial:
    output_material: SuppliedMaterialOccurrence
    error_material: SuppliedMaterialOccurrence
    end_material: SuppliedMaterialOccurrence

    def __post_init__(self) -> None:
        occurrences = (
            self.output_material,
            self.error_material,
            self.end_material,
        )
        if any(
            type(occurrence) is not SuppliedMaterialOccurrence
            for occurrence in occurrences
        ):
            raise TypeError("exact supplied material required")
        boundaries = tuple(
            occurrence.source_boundary for occurrence in occurrences
        )
        if len(set(boundaries)) != len(boundaries):
            raise ValueError("distinct source boundary required")


SuppliedInvocationProvider = Callable[[bytes], SuppliedInvocationMaterial]


def ingest_supplied_invocation_material(
    ledger: EventLedger,
    *,
    locality_identity: str,
    command_occurrence_reference: str,
    supplied: SuppliedInvocationMaterial,
) -> tuple[Event, Event, Event]:
    """Ingest supplied output, error, and end material in exact order."""

    if type(supplied) is not SuppliedInvocationMaterial:
        raise TypeError("exact supplied material required")
    command_occurrence = (
        ledger.get(command_occurrence_reference)
        if type(command_occurrence_reference) is str
        else None
    )
    if (
        command_occurrence is None
        or command_occurrence.kind != MATERIAL_INGEST_OCCURRED_KIND
        or command_occurrence.locality_identity != locality_identity
        or command_occurrence.material.get("source_role") != "operator"
        or type(command_occurrence.exact_material) is not bytes
        or not command_occurrence.exact_material.startswith(b"!")
        or ledger.integrity_of(command_occurrence.identity) == CORRUPTED
    ):
        raise ValueError("exact operator occurrence required")
    return tuple(
        ingest_material(
            ledger,
            locality_identity=locality_identity,
            exact_bytes=occurrence.exact_bytes,
            source_role="system",
            source_boundary=occurrence.source_boundary,
            known_loss=occurrence.known_loss,
            provenance_occurrence_references=(command_occurrence.identity,),
        )
        for occurrence in (
            supplied.output_material,
            supplied.error_material,
            supplied.end_material,
        )
    )
