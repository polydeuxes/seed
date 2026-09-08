"""One operator destination Locality related to one operator Locality."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from seed_runtime.event import Event
from seed_runtime.events import CORRUPTED, EventLedger
from seed_runtime.material_source import read_exact_material_result
from seed_runtime.operator_material_source import (
    OPERATOR_MATERIAL_SOURCE_RECORDED_KIND,
)


OPERATOR_DESTINATION_LOCALITY_ACT_OCCURRENCE_EVENT = (
    "operator.destination_locality_act_occurrence_recorded"
)
OPERATOR_DESTINATION_LOCALITY_RECORDED_KIND = "operator.destination_locality_recorded"
OPERATOR_DESTINATION_LOCALITY_ACT = "Locality"
EVENT_KIND_BOOK_CLAUSES = {
    OPERATOR_DESTINATION_LOCALITY_ACT_OCCURRENCE_EVENT: "02.Acts.A",
    OPERATOR_DESTINATION_LOCALITY_RECORDED_KIND: "06.Locality.A",
}


class OperatorDestinationLocalityError(ValueError):
    """One operator destination Locality boundary is absent or incoherent."""


def _identity(value: Any, message: str) -> str:
    if type(value) is not str or not value:
        raise OperatorDestinationLocalityError(message)
    return value


def _command_event(ledger: EventLedger, event_identity: str) -> Event:
    event = ledger.get(
        _identity(event_identity, "destination Locality requires one operator occurrence")
    )
    if (
        event is None
        or event.kind != OPERATOR_MATERIAL_SOURCE_RECORDED_KIND
        or type(event.exact_material) is not bytes
        or not event.exact_material.startswith(b"!")
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise OperatorDestinationLocalityError(
            "destination Locality requires one intact operator material occurrence"
        )
    try:
        read_exact_material_result(ledger, event.identity)
    except (TypeError, ValueError) as error:
        raise OperatorDestinationLocalityError(
            "destination Locality requires one intact operator material occurrence"
        ) from error
    return event


def _act_material(
    *,
    command: Event,
    through_event_occurrence_identity: str,
) -> dict[str, Any]:
    return {
        "act": OPERATOR_DESTINATION_LOCALITY_ACT,
        "operator_material_occurrence_reference": command.identity,
        "operator_through_event_occurrence_identity": (
            through_event_occurrence_identity
        ),
    }


def _source_cut_event(
    ledger: EventLedger,
    *,
    command: Event,
    through_event_occurrence_identity: str,
) -> Event:
    boundary = ledger.get(through_event_occurrence_identity)
    if (
        boundary is None
        or boundary.locality_identity != command.locality_identity
        or ledger.integrity_of(boundary.identity) == CORRUPTED
    ):
        raise OperatorDestinationLocalityError(
            "destination Locality Act requires an intact source cut"
        )
    ordered = (
        (command.identity,)
        if command.identity == boundary.identity
        else (command.identity, boundary.identity)
    )
    try:
        ledger.occurrence_identities_in_append_order(ordered)
    except (TypeError, ValueError) as error:
        raise OperatorDestinationLocalityError(
            "destination Locality Act requires its operator occurrence at or before the source cut"
        ) from error
    return boundary


def record_operator_destination_locality_act_occurrence(
    ledger: EventLedger,
    *,
    operator_material_occurrence_reference: str,
    current_coordinates: dict[str, Any],
) -> Event:
    """Record a Locality Act over exact current operator coordinates."""

    command = _command_event(ledger, operator_material_occurrence_reference)
    exact_results = (
        current_coordinates.get("exact_result_occurrences")
        if type(current_coordinates) is dict
        else None
    )
    boundary_identity = (
        current_coordinates.get("through_event_occurrence_identity")
        if type(current_coordinates) is dict
        else None
    )
    if (
        type(exact_results) is not dict
        or type(exact_results.get(command.identity)) is not dict
        or current_coordinates.get("locality_identity")
        != command.locality_identity
        or type(boundary_identity) is not str
        or not boundary_identity
    ):
        raise OperatorDestinationLocalityError(
            "destination Locality Act requires exact current operator material coordinates"
        )
    _source_cut_event(
        ledger,
        command=command,
        through_event_occurrence_identity=boundary_identity,
    )
    for act in ledger.list_events():
        if (
            act.kind == OPERATOR_DESTINATION_LOCALITY_ACT_OCCURRENCE_EVENT
            and act.material.get("operator_material_occurrence_reference")
            == command.identity
        ):
            raise OperatorDestinationLocalityError(
                "operator material occurrence already has a destination Locality Act"
            )
    destination_locality_identity = ledger.mint_identity(
        "operator_destination_locality"
    )
    return ledger.append(
        OPERATOR_DESTINATION_LOCALITY_ACT_OCCURRENCE_EVENT,
        _act_material(
            command=command,
            through_event_occurrence_identity=boundary_identity,
        ),
        locality_identity=destination_locality_identity,
    )


def get_operator_destination_locality_act_occurrence(
    ledger: EventLedger, event_identity: str
) -> Event:
    event = ledger.get(
        _identity(event_identity, "destination Locality requires Act occurrence")
    )
    if (
        event is None
        or event.kind != OPERATOR_DESTINATION_LOCALITY_ACT_OCCURRENCE_EVENT
        or event.exact_material is not None
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise OperatorDestinationLocalityError(
            "destination Locality Act occurrence is absent or corrupted"
        )
    material = event.material
    command = _command_event(
        ledger, material.get("operator_material_occurrence_reference")
    )
    if type(event.locality_identity) is not str or not event.locality_identity:
        raise OperatorDestinationLocalityError(
            "destination Locality Act coordinates are not exact"
        )
    exact_act_material = _act_material(
        command=command,
        through_event_occurrence_identity=material.get(
            "operator_through_event_occurrence_identity"
        ),
    )
    boundary = _source_cut_event(
        ledger,
        command=command,
        through_event_occurrence_identity=material.get(
            "operator_through_event_occurrence_identity"
        ),
    )
    if (
        material != exact_act_material
    ):
        raise OperatorDestinationLocalityError(
            "destination Locality Act occurrence is not exact"
        )
    ordered = (
        (command.identity, event.identity)
        if command.identity == boundary.identity
        else (command.identity, boundary.identity, event.identity)
    )
    try:
        ledger.occurrence_identities_in_append_order(ordered)
    except (TypeError, ValueError) as error:
        raise OperatorDestinationLocalityError(
            "destination Locality Act does not follow current material coordinates"
        ) from error
    return event


def _result_material(ledger: EventLedger, act: Event) -> dict[str, Any]:
    material = act.material
    command = _command_event(
        ledger, material["operator_material_occurrence_reference"]
    )
    return {
        "operator_material_occurrence_reference": material[
            "operator_material_occurrence_reference"
        ],
        "operator_locality_identity": command.locality_identity,
    }


def _refuse_second_result(ledger: EventLedger, act: Event) -> None:
    for result in ledger.iter_locality_kind(
        act.locality_identity, OPERATOR_DESTINATION_LOCALITY_RECORDED_KIND
    ):
        if result.material.get("act_occurrence_event_identity") == act.identity:
            raise OperatorDestinationLocalityError(
                "one destination Locality Act occurrence cannot address two results"
            )


def _recorded_result_material(
    result: dict[str, Any],
    *,
    act_occurrence_event_identity: str,
) -> dict[str, Any]:
    return {
        "act_occurrence_event_identity": act_occurrence_event_identity,
    }


def record_operator_destination_locality_result(
    ledger: EventLedger, *, act_occurrence_event_identity: str
) -> Event:
    act = get_operator_destination_locality_act_occurrence(
        ledger, act_occurrence_event_identity
    )
    _refuse_second_result(ledger, act)
    result = _result_material(ledger, act)
    return ledger.append(
        OPERATOR_DESTINATION_LOCALITY_RECORDED_KIND,
        _recorded_result_material(
            result,
            act_occurrence_event_identity=act.identity,
        ),
        locality_identity=act.locality_identity,
    )


def get_recorded_operator_destination_locality(
    ledger: EventLedger, event_identity: str
) -> dict[str, Any]:
    event = ledger.get(
        _identity(event_identity, "destination Locality requires one result")
    )
    if (
        event is None
        or event.kind != OPERATOR_DESTINATION_LOCALITY_RECORDED_KIND
        or event.exact_material is not None
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise OperatorDestinationLocalityError(
            "destination Locality result is absent or corrupted"
        )
    act = get_operator_destination_locality_act_occurrence(
        ledger, event.material.get("act_occurrence_event_identity")
    )
    result = _result_material(ledger, act)
    exact_result_material = _recorded_result_material(
        result,
        act_occurrence_event_identity=act.identity,
    )
    if (
        event.locality_identity != act.locality_identity
        or event.material != exact_result_material
    ):
        raise OperatorDestinationLocalityError("destination Locality result is not exact")
    try:
        ledger.occurrences_in_append_order(
            (act.identity, event.identity),
            locality_identity=event.locality_identity,
        )
    except ValueError as error:
        raise OperatorDestinationLocalityError(
            "destination Locality result requires its Act occurrence"
        ) from error
    return {
        **deepcopy(event.material),
        "operator_material_occurrence_reference": result[
            "operator_material_occurrence_reference"
        ],
        "operator_locality_identity": result["operator_locality_identity"],
        "destination_locality_identity": event.locality_identity,
    }


def operator_destination_locality_occurrence_references(
    ledger: EventLedger, event_identity: str
) -> tuple[str, str]:
    event = ledger.get(event_identity)
    result = get_recorded_operator_destination_locality(ledger, event_identity)
    identities = (
        result["act_occurrence_event_identity"],
        event.identity,
    )
    ledger.occurrences_in_append_order(
        identities, locality_identity=event.locality_identity
    )
    return identities
