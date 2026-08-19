"""Exact system-attributed material supplied by one operator invocation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from seed_runtime.event import Event
from seed_runtime.events import CORRUPTED, EventLedger
from seed_runtime.material_acquisition import read_exact_material_acquisition_result
from seed_runtime.material_ingest import MATERIAL_INGEST_OCCURRED_KIND, ingest_material
from seed_runtime.operator_system_locality import (
    get_recorded_operator_system_locality,
)


@dataclass(frozen=True, slots=True)
class SuppliedSystemMaterialOccurrence:
    exact_bytes: bytes
    source_boundary: str
    egress: bool
    known_loss: tuple[str, ...] = ()
    provenance_occurrence_positions: tuple[int, ...] = ()

    def __post_init__(self) -> None:
        if type(self.exact_bytes) is not bytes:
            raise TypeError("exact material required")
        if type(self.source_boundary) is not str or not self.source_boundary:
            raise TypeError("exact source boundary required")
        if type(self.egress) is not bool:
            raise TypeError("exact egress distinction required")
        if type(self.known_loss) is not tuple or any(
            type(item) is not str for item in self.known_loss
        ):
            raise TypeError("exact known loss required")
        if (
            type(self.provenance_occurrence_positions) is not tuple
            or len(set(self.provenance_occurrence_positions))
            != len(self.provenance_occurrence_positions)
            or any(
                type(position) is not int or position < 0
                for position in self.provenance_occurrence_positions
            )
        ):
            raise TypeError("exact prior supplied occurrence positions required")


SuppliedSystemMaterialConsumer = Callable[
    [SuppliedSystemMaterialOccurrence], None
]
OperatorInvocationProvider = Callable[
    [bytes, SuppliedSystemMaterialConsumer], None
]


def ingest_supplied_invocation_occurrence(
    ledger: EventLedger,
    *,
    operator_invocation_locality_result_event_identity: str,
    command_occurrence_reference: str,
    supplied: SuppliedSystemMaterialOccurrence,
    prior_supplied_occurrence_references: tuple[str, ...] = (),
) -> Event:
    """Ingest one exact system occurrence in its invocation Locality."""

    if type(supplied) is not SuppliedSystemMaterialOccurrence:
        raise TypeError("exact supplied material required")
    if (
        type(prior_supplied_occurrence_references) is not tuple
        or len(set(prior_supplied_occurrence_references))
        != len(prior_supplied_occurrence_references)
        or any(
            type(reference) is not str or not reference
            for reference in prior_supplied_occurrence_references
        )
        or any(
            position >= len(prior_supplied_occurrence_references)
            for position in supplied.provenance_occurrence_positions
        )
    ):
        raise ValueError("exact prior supplied occurrence references required")
    relation = get_recorded_operator_system_locality(
        ledger, operator_invocation_locality_result_event_identity
    )
    command_occurrence = (
        ledger.get(command_occurrence_reference)
        if type(command_occurrence_reference) is str
        else None
    )
    if (
        command_occurrence is None
        or command_occurrence.identity
        != relation["operator_material_occurrence_reference"]
        or command_occurrence.locality_identity
        != relation["operator_locality_identity"]
        or command_occurrence.material.get("source_role") != "operator"
        or type(command_occurrence.exact_material) is not bytes
        or not command_occurrence.exact_material.startswith(b"!")
        or ledger.integrity_of(command_occurrence.identity) == CORRUPTED
    ):
        raise ValueError("exact operator occurrence required")
    try:
        read_exact_material_acquisition_result(ledger, command_occurrence.identity)
    except (TypeError, ValueError) as error:
        raise ValueError("exact operator occurrence required") from error
    prior_occurrences = tuple(
        ledger.get(reference) for reference in prior_supplied_occurrence_references
    )
    if any(
        occurrence is None
        or occurrence.kind != MATERIAL_INGEST_OCCURRED_KIND
        or occurrence.locality_identity != relation["destination_locality_identity"]
        or occurrence.material.get("source_role") != "system"
        or occurrence.material.get("provenance_occurrence_references")[:2]
        != [
            command_occurrence.identity,
            operator_invocation_locality_result_event_identity,
        ]
        or ledger.integrity_of(occurrence.identity) == CORRUPTED
        for occurrence in prior_occurrences
    ):
        raise ValueError("exact prior supplied occurrence references required")
    if prior_occurrences:
        try:
            ordered = ledger.occurrences_in_append_order(
                prior_supplied_occurrence_references,
                locality_identity=relation["destination_locality_identity"],
            )
        except (TypeError, ValueError) as error:
            raise ValueError(
                "exact prior supplied occurrence references required"
            ) from error
        if tuple(occurrence.identity for occurrence in ordered) != (
            prior_supplied_occurrence_references
        ):
            raise ValueError("exact prior supplied occurrence references required")
    return ingest_material(
        ledger,
        locality_identity=relation["destination_locality_identity"],
        exact_bytes=supplied.exact_bytes,
        source_role="system",
        source_boundary=supplied.source_boundary,
        known_loss=supplied.known_loss,
        provenance_occurrence_references=(
            command_occurrence.identity,
            operator_invocation_locality_result_event_identity,
            *(
                prior_supplied_occurrence_references[position]
                for position in supplied.provenance_occurrence_positions
            ),
        ),
    )
