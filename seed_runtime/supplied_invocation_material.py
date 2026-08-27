"""Exact material supplied by this Witness through one operator invocation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from seed_runtime.event import Event
from seed_runtime.events import CORRUPTED, EventLedger
from seed_runtime.material_source import read_exact_material_result
from seed_runtime.operator_material_source import (
    OPERATOR_MATERIAL_SOURCE_RECORDED_KIND,
)
from seed_runtime.witness_material_source import WITNESS_MATERIAL_SOURCE_RECORDED_KIND, record_witness_material_source
from seed_runtime.operator_invocation_locality import (
    get_recorded_operator_invocation_locality,
)


@dataclass(frozen=True, slots=True)
class SuppliedWitnessReadOccurrence:
    exact_bytes: bytes
    source_boundary: str
    invocation_position: int

    def __post_init__(self) -> None:
        if type(self.exact_bytes) is not bytes or not self.exact_bytes:
            raise TypeError("exact nonempty read material required")
        if type(self.source_boundary) is not str or not self.source_boundary:
            raise TypeError("exact read source boundary required")
        if (
            type(self.invocation_position) is not int
            or self.invocation_position < 0
        ):
            raise TypeError("exact invocation read position required")


@dataclass(frozen=True, slots=True)
class SuppliedWitnessMaterialOccurrence:
    exact_bytes: bytes
    source_boundary: str
    known_loss: tuple[str, ...] = ()
    source_occurrence_positions: tuple[int, ...] = ()
    read_occurrences: tuple[SuppliedWitnessReadOccurrence, ...] = ()

    def __post_init__(self) -> None:
        if type(self.exact_bytes) is not bytes:
            raise TypeError("exact material required")
        if type(self.source_boundary) is not str or not self.source_boundary:
            raise TypeError("exact source boundary required")
        if type(self.known_loss) is not tuple or any(
            type(item) is not str for item in self.known_loss
        ):
            raise TypeError("exact known loss required")
        if (
            type(self.source_occurrence_positions) is not tuple
            or len(set(self.source_occurrence_positions))
            != len(self.source_occurrence_positions)
            or any(
                type(position) is not int or position < 0
                for position in self.source_occurrence_positions
            )
        ):
            raise TypeError("exact prior supplied occurrence positions required")
        if (
            type(self.read_occurrences) is not tuple
            or any(
                type(occurrence) is not SuppliedWitnessReadOccurrence
                for occurrence in self.read_occurrences
            )
            or len(
                {
                    occurrence.source_boundary
                    for occurrence in self.read_occurrences
                }
            )
            != len(self.read_occurrences)
            or len(
                {
                    occurrence.invocation_position
                    for occurrence in self.read_occurrences
                }
            )
            != len(self.read_occurrences)
            or (
                self.read_occurrences
                and b"".join(
                    occurrence.exact_bytes
                    for occurrence in self.read_occurrences
                )
                != self.exact_bytes
            )
        ):
            raise TypeError("exact supplied read occurrences required")


SuppliedWitnessMaterialConsumer = Callable[
    [SuppliedWitnessMaterialOccurrence], None
]
OperatorInvocationProvider = Callable[
    [bytes, SuppliedWitnessMaterialConsumer], None
]


def _read_occurrence_coordinates(
    occurrences: tuple[SuppliedWitnessReadOccurrence, ...],
) -> tuple[dict[str, object], ...]:
    coordinates = []
    start = 0
    for occurrence in occurrences:
        end = start + len(occurrence.exact_bytes)
        coordinates.append(
            {
                "source_boundary": occurrence.source_boundary,
                "invocation_position": occurrence.invocation_position,
                "start_position": start,
                "end_position": end,
            }
        )
        start = end
    return tuple(coordinates)


def record_supplied_witness_material_source(
    ledger: EventLedger,
    *,
    operator_invocation_locality_result_event_identity: str,
    command_occurrence_reference: str,
    supplied: SuppliedWitnessMaterialOccurrence,
    prior_supplied_occurrence_references: tuple[str, ...] = (),
) -> Event:
    """Record one exact occurrence supplied by this Witness in its Locality."""

    if type(supplied) is not SuppliedWitnessMaterialOccurrence:
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
            for position in supplied.source_occurrence_positions
        )
    ):
        raise ValueError("exact prior supplied occurrence references required")
    relation = get_recorded_operator_invocation_locality(
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
        or command_occurrence.kind != OPERATOR_MATERIAL_SOURCE_RECORDED_KIND
        or command_occurrence.locality_identity
        != relation["operator_locality_identity"]
        or type(command_occurrence.exact_material) is not bytes
        or not command_occurrence.exact_material.startswith(b"!")
        or ledger.integrity_of(command_occurrence.identity) == CORRUPTED
    ):
        raise ValueError("exact operator occurrence required")
    try:
        read_exact_material_result(ledger, command_occurrence.identity)
    except (TypeError, ValueError) as error:
        raise ValueError("exact operator occurrence required") from error
    prior_occurrences = tuple(
        ledger.get(reference) for reference in prior_supplied_occurrence_references
    )
    if any(
        occurrence is None
        or occurrence.kind != WITNESS_MATERIAL_SOURCE_RECORDED_KIND
        or occurrence.locality_identity != relation["destination_locality_identity"]
        or occurrence.material.get("source_occurrence_references")[:2]
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
    return record_witness_material_source(
        ledger,
        locality_identity=relation["destination_locality_identity"],
        exact_bytes=supplied.exact_bytes,
        source_boundary=supplied.source_boundary,
        known_loss=supplied.known_loss,
        source_occurrence_references=(
            command_occurrence.identity,
            operator_invocation_locality_result_event_identity,
            *(
                prior_supplied_occurrence_references[position]
                for position in supplied.source_occurrence_positions
            ),
        ),
        read_occurrences=_read_occurrence_coordinates(supplied.read_occurrences),
    )
