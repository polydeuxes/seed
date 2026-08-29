"""Determine exact pair-position result references at one addressed byte coordinate."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from seed_runtime.event import Event
from seed_runtime.events import CORRUPTED, EventLedger
from seed_runtime.measurement_of_position_coordinates_of_byte_pair_occurrences import (
    BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND,
    ReferenceToRecordedPositionOfBytePairOccurrence,
    references_to_recorded_byte_pair_occurrences_carrying_addressed_source_position_coordinate,
)


DETERMINATION_ACT_OCCURRENCE_EVENT = (
    "operator.addressed_byte_occurrence_reference_determination."
    "determination_measurement_act_occurrence_recorded"
)
DETERMINATION_RESULT_KIND = (
    "operator.addressed_byte_occurrence_reference_determination."
    "determination_measurement_recorded"
)
BOOK_CLAUSE = "01.Source.D.2"
DETERMINATION_ACT = (
    "declared Measurement of exact pair-occurrence result-position "
    "references with one addressed source-byte position-coordinate reference"
)
EVENT_KIND_BOOK_CLAUSES = {
    DETERMINATION_ACT_OCCURRENCE_EVENT: "02.Acts.A",
    DETERMINATION_RESULT_KIND: "01.Source.D.2",
}


class AddressedByteOccurrenceReferenceDeterminationError(ValueError):
    """An addressed byte-occurrence determination coordinate is not exact."""


def _identity(value: Any, message: str) -> str:
    if type(value) is not str or not value:
        raise AddressedByteOccurrenceReferenceDeterminationError(message)
    return value


def _direct_result_reference(event: Event) -> dict[str, str]:
    return {
        "recorded_occurrence_identity": event.identity,
        "result_identity": event.material["result_identity"],
        "act_occurrence_identity": event.material["act_occurrence_identity"],
        "act_occurrence_event_identity": event.material[
            "act_occurrence_event_identity"
        ],
    }


def _determination_result_reference(event: Event) -> dict[str, str]:
    return {
        "recorded_occurrence_identity": event.identity,
        "result_identity": event.material["result_identity"],
        "act_occurrence_identity": event.material[
            "determination_act_occurrence_identity"
        ],
        "act_occurrence_event_identity": event.material[
            "act_occurrence_event_identity"
        ],
    }


def _source(
    ledger: EventLedger,
    *,
    result_event_identity: str,
    coordinate_reference: dict[str, Any],
    current_coordinates: dict[str, Any] | None = None,
) -> tuple[Event, tuple[ReferenceToRecordedPositionOfBytePairOccurrence, ...]]:
    try:
        references = references_to_recorded_byte_pair_occurrences_carrying_addressed_source_position_coordinate(
            ledger,
            result_event_identity,
            coordinate_reference,
            prior_coordinates=current_coordinates,
        )
    except (AttributeError, TypeError, ValueError) as error:
        raise AddressedByteOccurrenceReferenceDeterminationError(
            "determination has no exact addressed direct-result coordinate"
        ) from error
    event = ledger.get(result_event_identity)
    if (
        event is None
        or event.kind != BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND
        or event.exact_material is not None
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise AddressedByteOccurrenceReferenceDeterminationError(
            "determination has no intact direct result"
        )
    return event, references


def _current_coordinates_carry_source(
    ledger: EventLedger,
    *,
    current_coordinates: dict[str, Any],
    source_result: Event,
    required_boundary_identity: str,
) -> None:
    measurements = (
        current_coordinates.get("measurement_occurrences")
        if type(current_coordinates) is dict
        else None
    )
    through = (
        current_coordinates.get("through_event_occurrence_identity")
        if type(current_coordinates) is dict
        else None
    )
    if (
        type(current_coordinates) is not dict
        or current_coordinates.get("locality_identity")
        != source_result.locality_identity
        or type(measurements) is not dict
        or measurements.get(source_result.identity)
        != _direct_result_reference(source_result)
        or type(through) is not str
        or type(required_boundary_identity) is not str
    ):
        raise AddressedByteOccurrenceReferenceDeterminationError(
            "no exact addressed direct result is current"
        )
    ordered = tuple(
        dict.fromkeys((source_result.identity, required_boundary_identity, through))
    )
    try:
        read = ledger.occurrences_in_append_order(
            ordered, locality_identity=source_result.locality_identity
        )
    except (TypeError, ValueError) as error:
        raise AddressedByteOccurrenceReferenceDeterminationError(
            "addressed direct result is not established through the boundary"
        ) from error
    if tuple(event.identity for event in read) != ordered:
        raise AddressedByteOccurrenceReferenceDeterminationError(
            "addressed direct result is not established through the boundary"
        )


def _require_exact_current_coordinates(
    ledger: EventLedger,
    *,
    source_result: Event,
    current_coordinates: dict[str, Any],
) -> dict[str, Any]:
    if type(current_coordinates) is not dict:
        raise AddressedByteOccurrenceReferenceDeterminationError(
            "determination has no exact current coordinates"
        )
    boundary = current_coordinates.get("through_event_occurrence_identity")
    _current_coordinates_carry_source(
        ledger,
        current_coordinates=current_coordinates,
        source_result=source_result,
        required_boundary_identity=boundary,
    )
    event = ledger.get(boundary)
    if (
        event is None
        or ledger.integrity_of(event.identity) == CORRUPTED
        or event.locality_identity != source_result.locality_identity
        or ledger.append_boundary_through_occurrence(event.identity)
        != ledger.append_boundary()
    ):
        raise AddressedByteOccurrenceReferenceDeterminationError(
            "determination current coordinates do not reach the append boundary"
        )
    return current_coordinates


def _at_append_tip(ledger: EventLedger, event: Event | None) -> bool:
    return (
        event is not None
        and ledger.get(event.identity) == event
        and ledger.integrity_of(event.identity) != CORRUPTED
        and ledger.append_boundary_through_occurrence(event.identity)
        == ledger.append_boundary()
    )


def _mint_identities(ledger: EventLedger) -> dict[str, str]:
    identities = {
        "determination_act_identity": ledger.mint_identity(
            "addressed_byte_occurrence_reference_determination_measurement_act"
        ),
        "determination_act_occurrence_identity": ledger.mint_identity(
            "addressed_byte_occurrence_reference_determination_measurement_act_occurrence"
        ),
        "determination_result_identity": ledger.mint_identity(
            "addressed_byte_occurrence_reference_determination_measurement_result"
        ),
    }
    if len(set(identities.values())) != 3:
        raise AddressedByteOccurrenceReferenceDeterminationError(
            "determination lifecycle identities collapsed"
        )
    return identities


def _act_material(
    *,
    source: Event,
    coordinate: dict[str, Any],
    boundary: str,
    identities: dict[str, str],
) -> dict[str, Any]:
    subject = {
        "direct_pair_position_result_reference": _direct_result_reference(source),
        "addressed_source_byte_position_coordinate_reference": deepcopy(coordinate),
    }
    return {
        "determination_act_identity": identities["determination_act_identity"],
        "determination_act_occurrence_identity": identities[
            "determination_act_occurrence_identity"
        ],
        "determination_result_identity": identities[
            "determination_result_identity"
        ],
        "act": DETERMINATION_ACT,
        "subject_reference": subject,
        "direct_pair_position_result_reference": deepcopy(
            subject["direct_pair_position_result_reference"]
        ),
        "addressed_source_byte_position_coordinate_reference": deepcopy(coordinate),
        "through_event_occurrence_identity": boundary,
    }


def record_addressed_byte_occurrence_reference_determination_act_occurrence(
    ledger: EventLedger,
    *,
    direct_result_event_identity: str,
    addressed_source_byte_position_coordinate_reference: dict[str, Any],
    current_coordinates: dict[str, Any],
) -> Event:
    if not isinstance(ledger, EventLedger):
        raise TypeError("determination Act needs one EventLedger")
    source, references = _source(
        ledger,
        result_event_identity=_identity(
            direct_result_event_identity, "determination Act has no direct result"
        ),
        coordinate_reference=addressed_source_byte_position_coordinate_reference,
        current_coordinates=current_coordinates,
    )
    current = _require_exact_current_coordinates(
        ledger, source_result=source, current_coordinates=current_coordinates
    )
    boundary = current["through_event_occurrence_identity"]
    source_material = deepcopy(source.material)
    identities = _mint_identities(ledger)
    source_read, references_read = _source(
        ledger,
        result_event_identity=source.identity,
        coordinate_reference=addressed_source_byte_position_coordinate_reference,
        current_coordinates=current_coordinates,
    )
    if (
        source_read != source
        or source.material != source_material
        or references_read != references
        or not _at_append_tip(ledger, ledger.get(boundary))
    ):
        raise AddressedByteOccurrenceReferenceDeterminationError(
            "determination source changed before its Act occurrence"
        )
    return ledger.append(
        DETERMINATION_ACT_OCCURRENCE_EVENT,
        _act_material(
            source=source,
            coordinate=addressed_source_byte_position_coordinate_reference,
            boundary=boundary,
            identities=identities,
        ),
        locality_identity=source.locality_identity,
    )


def _read_determination_act(
    ledger: EventLedger,
    event_identity: str,
    *,
    prior_coordinates: dict[str, Any] | None = None,
) -> tuple[
    Event,
    Event,
    tuple[ReferenceToRecordedPositionOfBytePairOccurrence, ...],
]:
    act = ledger.get(event_identity)
    if (
        act is None
        or act.kind != DETERMINATION_ACT_OCCURRENCE_EVENT
        or act.exact_material is not None
        or ledger.integrity_of(act.identity) == CORRUPTED
    ):
        raise AddressedByteOccurrenceReferenceDeterminationError(
            "determination Act occurrence is absent or corrupted"
        )
    reference = act.material.get("direct_pair_position_result_reference")
    source_identity = (
        reference.get("recorded_occurrence_identity")
        if type(reference) is dict
        else None
    )
    coordinate = act.material.get(
        "addressed_source_byte_position_coordinate_reference"
    )
    boundary = act.material.get("through_event_occurrence_identity")
    if prior_coordinates is None:
        from seed_runtime.operator_current_coordinates import (
            read_operator_current_coordinates_through,
        )

        try:
            prior_coordinates = read_operator_current_coordinates_through(
                ledger,
                locality_identity=act.locality_identity,
                through_event_occurrence_identity=boundary,
            )
        except (AttributeError, TypeError, ValueError) as error:
            raise AddressedByteOccurrenceReferenceDeterminationError(
                "determination Act has no exact prior coordinates"
            ) from error
    source, references = _source(
        ledger,
        result_event_identity=source_identity,
        coordinate_reference=coordinate,
        current_coordinates=prior_coordinates,
    )
    _current_coordinates_carry_source(
        ledger,
        current_coordinates=prior_coordinates,
        source_result=source,
        required_boundary_identity=boundary,
    )
    identities = {
        key: act.material.get(key)
        for key in (
            "determination_act_identity",
            "determination_act_occurrence_identity",
            "determination_result_identity",
        )
    }
    expected = _act_material(
        source=source,
        coordinate=coordinate,
        boundary=boundary,
        identities=identities,
    )
    try:
        ordered = ledger.occurrences_in_append_order(
            (boundary, act.identity), locality_identity=act.locality_identity
        )
    except (TypeError, ValueError) as error:
        raise AddressedByteOccurrenceReferenceDeterminationError(
            "determination Act order is false"
        ) from error
    if (
        any(type(value) is not str or not value for value in identities.values())
        or len(set(identities.values())) != 3
        or act.locality_identity != source.locality_identity
        or act.material != expected
        or tuple(event.identity for event in ordered) != (boundary, act.identity)
    ):
        raise AddressedByteOccurrenceReferenceDeterminationError(
            "determination Act occurrence coordinates are not exact"
        )
    return act, source, references


def get_addressed_byte_occurrence_reference_determination_act_occurrence(
    ledger: EventLedger, event_identity: str
) -> Event:
    return _read_determination_act(ledger, event_identity)[0]


def _result_material(
    *,
    act: Event,
    source: Event,
    references: tuple[ReferenceToRecordedPositionOfBytePairOccurrence, ...],
) -> dict[str, Any]:
    coordinate = act.material[
        "addressed_source_byte_position_coordinate_reference"
    ]
    return {
        "result_identity": act.material["determination_result_identity"],
        "exact_act": DETERMINATION_ACT,
        "determination_act_identity": act.material["determination_act_identity"],
        "determination_act_occurrence_identity": act.material[
            "determination_act_occurrence_identity"
        ],
        "direct_pair_position_result_reference": _direct_result_reference(source),
        "addressed_source_byte_position_coordinate_reference": deepcopy(coordinate),
        "completeness_boundary": {
            "identity": coordinate["completeness_boundary_identity"]
        },
        "ordered_result_position_references": [
            deepcopy(reference.result_position_reference) for reference in references
        ],
        "act_occurrence_event_identity": act.identity,
    }


def record_addressed_byte_occurrence_reference_determination_result(
    ledger: EventLedger,
    *,
    determination_act_occurrence_event_identity: str,
    current_coordinates: dict[str, Any] | None = None,
) -> Event:
    act, source, references = _read_determination_act(
        ledger,
        determination_act_occurrence_event_identity,
        prior_coordinates=current_coordinates,
    )
    act_material = deepcopy(act.material)
    source_material = deepcopy(source.material)
    matches = tuple(
        event
        for event in ledger.iter_locality_kind(
            act.locality_identity, DETERMINATION_RESULT_KIND
        )
        if event.material.get("act_occurrence_event_identity") == act.identity
        or event.material.get("determination_act_occurrence_identity")
        == act.material["determination_act_occurrence_identity"]
    )
    if matches:
        raise AddressedByteOccurrenceReferenceDeterminationError(
            "a result is already recorded for determination Act"
        )
    act_read, source_read, references_read = _read_determination_act(
        ledger,
        act.identity,
        prior_coordinates=current_coordinates,
    )
    if (
        act_read != act
        or act.material != act_material
        or source_read != source
        or source.material != source_material
        or references_read != references
        or not _at_append_tip(ledger, act)
    ):
        raise AddressedByteOccurrenceReferenceDeterminationError(
            "determination coordinates changed before its result occurrence"
        )
    return ledger.append(
        DETERMINATION_RESULT_KIND,
        _result_material(act=act, source=source, references=references),
        locality_identity=act.locality_identity,
    )


def _read_determination_result(
    ledger: EventLedger,
    event_identity: str,
    *,
    prior_coordinates: dict[str, Any] | None = None,
) -> tuple[
    Event,
    Event,
    Event,
    tuple[ReferenceToRecordedPositionOfBytePairOccurrence, ...],
]:
    result = ledger.get(event_identity)
    if (
        result is None
        or result.kind != DETERMINATION_RESULT_KIND
        or result.exact_material is not None
        or ledger.integrity_of(result.identity) == CORRUPTED
    ):
        raise AddressedByteOccurrenceReferenceDeterminationError(
            "determination result is absent or corrupted"
        )
    act, source, references = _read_determination_act(
        ledger,
        result.material.get("act_occurrence_event_identity"),
        prior_coordinates=prior_coordinates,
    )
    expected = _result_material(act=act, source=source, references=references)
    matches = tuple(
        event
        for event in ledger.iter_locality_kind(
            result.locality_identity, DETERMINATION_RESULT_KIND
        )
        if event.material.get("act_occurrence_event_identity") == act.identity
    )
    try:
        ordered = ledger.occurrences_in_append_order(
            (act.identity, result.identity), locality_identity=result.locality_identity
        )
    except (TypeError, ValueError) as error:
        raise AddressedByteOccurrenceReferenceDeterminationError(
            "determination result occurrence order is false"
        ) from error
    if (
        result.locality_identity != act.locality_identity
        or result.material != expected
        or tuple(event.identity for event in ordered)
        != (act.identity, result.identity)
        or len(matches) != 1
        or matches[0].identity != result.identity
    ):
        raise AddressedByteOccurrenceReferenceDeterminationError(
            "determination result coordinates are not exact"
        )
    return result, act, source, references


def get_recorded_addressed_byte_occurrence_reference_determination(
    ledger: EventLedger, event_identity: str
) -> dict[str, Any]:
    return deepcopy(_read_determination_result(ledger, event_identity)[0].material)


def _record_addressed_byte_occurrence_reference_determination_lifecycle_from_carried_current_coordinates(
    ledger: EventLedger,
    *,
    direct_result_event_identity: str,
    addressed_source_byte_position_coordinate_reference: dict[str, Any],
    current_coordinates: dict[str, Any],
    mutate_current_coordinates: bool = False,
) -> tuple[dict[str, Any], Event]:
    if not isinstance(ledger, EventLedger):
        raise TypeError("determination lifecycle needs one EventLedger")
    current = (
        current_coordinates
        if mutate_current_coordinates
        else deepcopy(current_coordinates)
    )
    locality = current.get("locality_identity")
    prior = current.get("through_event_occurrence_identity")
    count = current.get("event_count")
    measurements = current.get("measurement_occurrences")
    if type(count) is not int or type(measurements) is not dict:
        raise AddressedByteOccurrenceReferenceDeterminationError(
            "determination lifecycle has no exact current coordinates"
        )
    act = record_addressed_byte_occurrence_reference_determination_act_occurrence(
        ledger,
        direct_result_event_identity=direct_result_event_identity,
        addressed_source_byte_position_coordinate_reference=(
            addressed_source_byte_position_coordinate_reference
        ),
        current_coordinates=current,
    )
    if (
        current.get("through_event_occurrence_identity") != prior
        or act.locality_identity != locality
        or not _at_append_tip(ledger, act)
    ):
        raise AddressedByteOccurrenceReferenceDeterminationError(
            "produced determination Act is not exact"
        )
    current["through_event_occurrence_identity"] = act.identity
    current["event_count"] = count + 1
    result = record_addressed_byte_occurrence_reference_determination_result(
        ledger,
        determination_act_occurrence_event_identity=act.identity,
        current_coordinates=current,
    )
    if result.identity in measurements or not _at_append_tip(ledger, result):
        raise AddressedByteOccurrenceReferenceDeterminationError(
            "produced determination result is not exact"
        )
    measurements[result.identity] = _determination_result_reference(result)
    current["through_event_occurrence_identity"] = result.identity
    current["event_count"] = count + 2
    return current, result
