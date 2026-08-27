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
from seed_runtime.yield_relation import (
    read_requirements_of_yield_relation,
)


OPERATOR_DESTINATION_LOCALITY_SUBJECT_TO_ACT_BINDING_RECORDED_KIND = (
    "operator.destination_locality_subject_to_act_binding_recorded"
)
OPERATOR_DESTINATION_LOCALITY_ACT_OCCURRENCE_EVENT = (
    "operator.destination_locality_act_occurrence_recorded"
)
OPERATOR_DESTINATION_LOCALITY_RECORDED_KIND = "operator.destination_locality_recorded"
OPERATOR_DESTINATION_LOCALITY_BOOK_CLAUSE = "06.Locality.D"
OPERATOR_DESTINATION_LOCALITY_ACT = (
    "Establish one direct operator destination Locality relation"
)
EVENT_KIND_BOOK_CLAUSES = {
    OPERATOR_DESTINATION_LOCALITY_SUBJECT_TO_ACT_BINDING_RECORDED_KIND: (
        "06.Locality.D"
    ),
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
    requirements = read_requirements_of_yield_relation(
        ledger,
        recorded_result_event_identity=event.identity,
        yield_relation_event_identity=event.material.get(
            "yield_relation_identity"
        ),
        act_occurrence_event_identity=event.material.get(
            "act_occurrence_event_identity"
        ),
    )
    if not all(requirements.values()):
        raise OperatorDestinationLocalityError(
            "operator command occurrence has no exact Yield"
        )
    return event


def _binding_material(
    *,
    command: Event,
    through_event_occurrence_identity: str,
    operator_destination_locality_act_identity: str,
    act_occurrence_identity: str,
    result_identity: str,
    destination_locality_identity: str,
) -> dict[str, Any]:
    return {
        "book_clause_identity": OPERATOR_DESTINATION_LOCALITY_BOOK_CLAUSE,
        "exact_act": OPERATOR_DESTINATION_LOCALITY_ACT,
        "operator_destination_locality_act_identity": (
            operator_destination_locality_act_identity
        ),
        "act_occurrence_identity": act_occurrence_identity,
        "result_boundary_identity": result_identity,
        "operator_material_occurrence_reference": command.identity,
        "operator_material_result_identity": command.material["result_identity"],
        "operator_locality_identity": command.locality_identity,
        "operator_through_event_occurrence_identity": (
            through_event_occurrence_identity
        ),
        "destination_locality_identity": destination_locality_identity,
    }


def record_operator_destination_locality_subject_to_act_binding(
    ledger: EventLedger,
    *,
    operator_material_occurrence_reference: str,
    current_coordinates: dict[str, Any],
) -> Event:
    """Bind one destination Locality relation to its exact Act."""

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
            "destination Locality binding requires exact current operator material coordinates"
        )
    for binding in ledger.list_events():
        if (
            binding.kind
            == OPERATOR_DESTINATION_LOCALITY_SUBJECT_TO_ACT_BINDING_RECORDED_KIND
            and binding.material.get("operator_material_occurrence_reference")
            == command.identity
        ):
            raise OperatorDestinationLocalityError(
                "operator material occurrence already has a destination Locality binding"
            )
    identities = {
        "operator_destination_locality_act_identity": ledger.mint_identity(
            "operator_destination_locality_act"
        ),
        "act_occurrence_identity": ledger.mint_identity(
            "operator_destination_locality_act_occurrence"
        ),
        "result_identity": ledger.mint_identity("operator_destination_locality_result"),
        "destination_locality_identity": ledger.mint_identity(
            "operator_destination_locality"
        ),
    }
    if len(set(identities.values())) != len(identities):
        raise OperatorDestinationLocalityError("destination Locality identities are compressed")
    return ledger.append(
        OPERATOR_DESTINATION_LOCALITY_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
        _binding_material(
            command=command,
            through_event_occurrence_identity=boundary_identity,
            **identities,
        ),
        locality_identity=identities["destination_locality_identity"],
    )


def get_operator_destination_locality_subject_to_act_binding(
    ledger: EventLedger, event_identity: str
) -> Event:
    event = ledger.get(
        _identity(event_identity, "destination Locality requires one binding")
    )
    if (
        event is None
        or event.kind
        != OPERATOR_DESTINATION_LOCALITY_SUBJECT_TO_ACT_BINDING_RECORDED_KIND
        or event.exact_material is not None
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise OperatorDestinationLocalityError(
            "destination Locality binding is absent or corrupted"
        )
    material = event.material
    command = _command_event(
        ledger, material.get("operator_material_occurrence_reference")
    )
    identity_coordinates = (
        "operator_destination_locality_act_identity",
        "act_occurrence_identity",
        "result_boundary_identity",
        "destination_locality_identity",
    )
    identities = tuple(material.get(key) for key in identity_coordinates)
    if (
        any(type(value) is not str or not value for value in identities)
        or len(set(identities)) != len(identities)
    ):
        raise OperatorDestinationLocalityError(
            "destination Locality binding identities are not exact"
        )
    exact_binding_material = _binding_material(
        command=command,
        through_event_occurrence_identity=material.get(
            "operator_through_event_occurrence_identity"
        ),
        operator_destination_locality_act_identity=identities[0],
        act_occurrence_identity=identities[1],
        result_identity=identities[2],
        destination_locality_identity=identities[3],
    )
    boundary = ledger.get(
        material.get("operator_through_event_occurrence_identity")
    )
    if (
        material != exact_binding_material
        or event.locality_identity
        != material.get("destination_locality_identity")
        or boundary is None
        or boundary.locality_identity != command.locality_identity
        or ledger.integrity_of(boundary.identity) == CORRUPTED
    ):
        raise OperatorDestinationLocalityError("destination Locality binding is not exact")
    ordered = (
        (command.identity,)
        if command.identity == boundary.identity
        else (command.identity, boundary.identity)
    )
    try:
        ledger.occurrences_in_append_order(
            ordered, locality_identity=command.locality_identity
        )
    except (TypeError, ValueError) as error:
        raise OperatorDestinationLocalityError(
            "destination Locality binding does not follow current material coordinates"
        ) from error
    return event


def _act_material(binding: Event) -> dict[str, Any]:
    material = binding.material
    return {
        "operator_destination_locality_act_identity": material[
            "operator_destination_locality_act_identity"
        ],
        "act_occurrence_identity": material["act_occurrence_identity"],
        "result_boundary_identity": material["result_boundary_identity"],
        "act": OPERATOR_DESTINATION_LOCALITY_ACT,
        "subject_to_act_binding_event_identity": binding.identity,
        "operator_material_occurrence_reference": material[
            "operator_material_occurrence_reference"
        ],
        "operator_locality_identity": material["operator_locality_identity"],
        "destination_locality_identity": material[
            "destination_locality_identity"
        ],
    }


def record_operator_destination_locality_act_occurrence(
    ledger: EventLedger,
    *,
    subject_to_act_binding_event_identity: str,
    current_coordinates: dict[str, Any],
) -> Event:
    binding = get_operator_destination_locality_subject_to_act_binding(
        ledger, subject_to_act_binding_event_identity
    )
    current_bindings = (
        current_coordinates.get(
            "subject_to_act_binding_occurrences"
        )
        if type(current_coordinates) is dict
        else None
    )
    if (
        type(current_bindings) is not dict
        or current_bindings.get(binding.identity, object()) is not None
        or current_coordinates.get("locality_identity")
        != binding.locality_identity
    ):
        raise OperatorDestinationLocalityError(
            "destination Locality Act requires its exact current binding"
        )
    return ledger.append(
        OPERATOR_DESTINATION_LOCALITY_ACT_OCCURRENCE_EVENT,
        _act_material(binding),
        locality_identity=binding.material["destination_locality_identity"],
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
    binding = get_operator_destination_locality_subject_to_act_binding(
        ledger, event.material.get("subject_to_act_binding_event_identity")
    )
    if (
        event.material != _act_material(binding)
        or event.locality_identity
        != binding.material.get("destination_locality_identity")
    ):
        raise OperatorDestinationLocalityError("destination Locality Act occurrence is not exact")
    try:
        ledger.occurrences_in_append_order(
            (binding.identity, event.identity),
            locality_identity=event.locality_identity,
        )
    except ValueError as error:
        raise OperatorDestinationLocalityError(
            "destination Locality Act requires its prior binding"
        ) from error
    return event


def _result_material(act: Event) -> dict[str, Any]:
    material = act.material
    return {
        "result_identity": material["result_boundary_identity"],
        "operator_destination_locality_act_identity": material[
            "operator_destination_locality_act_identity"
        ],
        "act_occurrence_identity": material["act_occurrence_identity"],
        "exact_act": OPERATOR_DESTINATION_LOCALITY_ACT,
        "subject_to_act_binding_event_identity": material[
            "subject_to_act_binding_event_identity"
        ],
        "operator_material_occurrence_reference": material[
            "operator_material_occurrence_reference"
        ],
        "operator_locality_identity": material["operator_locality_identity"],
        "destination_locality_identity": material[
            "destination_locality_identity"
        ],
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
        "result_identity": result["result_identity"],
        "operator_destination_locality_act_identity": result[
            "operator_destination_locality_act_identity"
        ],
        "act_occurrence_identity": result["act_occurrence_identity"],
        "exact_act": result["exact_act"],
        "subject_to_act_binding_event_identity": result[
            "subject_to_act_binding_event_identity"
        ],
        "operator_material_occurrence_reference": result[
            "operator_material_occurrence_reference"
        ],
        "operator_locality_identity": result["operator_locality_identity"],
        "destination_locality_identity": result[
            "destination_locality_identity"
        ],
        "act_occurrence_event_identity": act_occurrence_event_identity,
    }


def record_operator_destination_locality_result(
    ledger: EventLedger, *, act_occurrence_event_identity: str
) -> Event:
    act = get_operator_destination_locality_act_occurrence(
        ledger, act_occurrence_event_identity
    )
    _refuse_second_result(ledger, act)
    result = _result_material(act)
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
    result = _result_material(act)
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
    return deepcopy(event.material)


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
