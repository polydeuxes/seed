"""One operator invocation Locality related to one operator Locality."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from seed_runtime.event import Event
from seed_runtime.events import CORRUPTED, EventLedger
from seed_runtime.identities import new_identity
from seed_runtime.material_source import read_exact_material_result
from seed_runtime.yield_relation import (
    RECORDED_YIELD_RELATION_EVENT,
    _record_yield_relation,
    read_requirements_of_yield_relation,
)


OPERATOR_INVOCATION_LOCALITY_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND = (
    "operator.invocation_locality_responsibility_assignment_recorded"
)
OPERATOR_INVOCATION_LOCALITY_ACT_OCCURRENCE_EVENT = (
    "operator.invocation_locality_act_occurrence_recorded"
)
OPERATOR_INVOCATION_LOCALITY_RECORDED_KIND = "operator.invocation_locality_recorded"
OPERATOR_INVOCATION_LOCALITY_BOOK_CLAUSE = "06.Locality.D"
OPERATOR_INVOCATION_LOCALITY_ACT = (
    "Establish one direct operator invocation Locality relation"
)
OPERATOR_INVOCATION_LOCALITY_RESULT_KIND = (
    "operator invocation Locality relation result"
)

EVENT_KIND_RESPONSIBILITIES = {
    OPERATOR_INVOCATION_LOCALITY_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND: (
        "06.Locality.D"
    ),
    OPERATOR_INVOCATION_LOCALITY_ACT_OCCURRENCE_EVENT: "02.Acts.A",
    OPERATOR_INVOCATION_LOCALITY_RECORDED_KIND: "06.Locality.A",
}


class OperatorInvocationLocalityError(ValueError):
    """One operator invocation Locality boundary is absent or incoherent."""


def _identity(value: Any, message: str) -> str:
    if type(value) is not str or not value:
        raise OperatorInvocationLocalityError(message)
    return value


def _command_event(ledger: EventLedger, event_identity: str) -> Event:
    event = ledger.get(
        _identity(event_identity, "invocation Locality requires one operator occurrence")
    )
    if (
        event is None
        or event.material.get("source_role") != "this operator"
        or type(event.exact_material) is not bytes
        or not event.exact_material.startswith(b"!")
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise OperatorInvocationLocalityError(
            "invocation Locality requires one intact operator material occurrence"
        )
    try:
        read_exact_material_result(ledger, event.identity)
    except (TypeError, ValueError) as error:
        raise OperatorInvocationLocalityError(
            "invocation Locality requires one intact operator material occurrence"
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
        raise OperatorInvocationLocalityError(
            "operator command occurrence carries no exact Yield"
        )
    return event


def _assignment_material(
    *,
    command: Event,
    standing_boundary_identity: str,
    operator_invocation_locality_act_identity: str,
    act_occurrence_identity: str,
    relation_occurrence_identity: str,
    result_identity: str,
    destination_locality_identity: str,
) -> dict[str, Any]:
    return {
        "book_clause_identity": OPERATOR_INVOCATION_LOCALITY_BOOK_CLAUSE,
        "exact_act": OPERATOR_INVOCATION_LOCALITY_ACT,
        "operator_invocation_locality_act_identity": (
            operator_invocation_locality_act_identity
        ),
        "act_occurrence_identity": act_occurrence_identity,
        "relation_occurrence_identity": relation_occurrence_identity,
        "result_boundary_identity": result_identity,
        "operator_material_occurrence_reference": command.identity,
        "operator_material_result_identity": command.material["result_identity"],
        "operator_locality_identity": command.locality_identity,
        "operator_standing_boundary_identity": standing_boundary_identity,
        "destination_locality_identity": destination_locality_identity,
        "scope": {
            "operator_locality_identity": command.locality_identity,
            "destination_locality_identity": destination_locality_identity,
            "operator_material_occurrence_reference": command.identity,
        },
        "unknown": [],
    }


def record_operator_invocation_locality_responsibility_assignment(
    ledger: EventLedger,
    *,
    operator_material_occurrence_reference: str,
    operator_locality_standing: dict[str, Any],
) -> Event:
    """Assign one invocation Locality from one exact operator occurrence."""

    command = _command_event(ledger, operator_material_occurrence_reference)
    carried = (
        operator_locality_standing.get("exact_result_occurrences")
        if type(operator_locality_standing) is dict
        else None
    )
    boundary_identity = (
        operator_locality_standing.get("through_event_occurrence_identity")
        if type(operator_locality_standing) is dict
        else None
    )
    if (
        type(carried) is not dict
        or type(carried.get(command.identity)) is not dict
        or operator_locality_standing.get("locality_identity")
        != command.locality_identity
        or type(boundary_identity) is not str
        or not boundary_identity
    ):
        raise OperatorInvocationLocalityError(
            "invocation Locality assignment requires exact operator material Standing"
        )
    for assignment in ledger.list_events():
        if (
            assignment.kind
            == OPERATOR_INVOCATION_LOCALITY_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND
            and assignment.material.get("operator_material_occurrence_reference")
            == command.identity
        ):
            raise OperatorInvocationLocalityError(
                "operator material occurrence already carries an invocation Locality assignment"
            )
    identities = {
        "operator_invocation_locality_act_identity": new_identity(
            "operator_invocation_locality_act"
        ),
        "act_occurrence_identity": new_identity(
            "operator_invocation_locality_act_occurrence"
        ),
        "relation_occurrence_identity": new_identity(
            "operator_invocation_locality_relation_occurrence"
        ),
        "result_identity": new_identity("operator_invocation_locality_result"),
        "destination_locality_identity": new_identity(
            "operator_invocation_locality"
        ),
    }
    if len(set(identities.values())) != len(identities):
        raise OperatorInvocationLocalityError("invocation Locality identities are compressed")
    return ledger.append(
        OPERATOR_INVOCATION_LOCALITY_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND,
        _assignment_material(
            command=command,
            standing_boundary_identity=boundary_identity,
            **identities,
        ),
        locality_identity=identities["destination_locality_identity"],
    )


def get_operator_invocation_locality_responsibility_assignment(
    ledger: EventLedger, event_identity: str
) -> Event:
    event = ledger.get(
        _identity(event_identity, "invocation Locality requires one assignment")
    )
    if (
        event is None
        or event.kind
        != OPERATOR_INVOCATION_LOCALITY_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND
        or event.exact_material is not None
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise OperatorInvocationLocalityError(
            "invocation Locality assignment is absent or corrupted"
        )
    material = event.material
    command = _command_event(
        ledger, material.get("operator_material_occurrence_reference")
    )
    identity_coordinates = (
        "operator_invocation_locality_act_identity",
        "act_occurrence_identity",
        "relation_occurrence_identity",
        "result_boundary_identity",
        "destination_locality_identity",
    )
    identities = tuple(material.get(key) for key in identity_coordinates)
    if (
        any(type(value) is not str or not value for value in identities)
        or len(set(identities)) != len(identities)
    ):
        raise OperatorInvocationLocalityError(
            "invocation Locality assignment identities are not exact"
        )
    exact_assignment_material = _assignment_material(
        command=command,
        standing_boundary_identity=material.get(
            "operator_standing_boundary_identity"
        ),
        operator_invocation_locality_act_identity=identities[0],
        act_occurrence_identity=identities[1],
        relation_occurrence_identity=identities[2],
        result_identity=identities[3],
        destination_locality_identity=identities[4],
    )
    boundary = ledger.get(material.get("operator_standing_boundary_identity"))
    if (
        material != exact_assignment_material
        or event.locality_identity
        != material.get("destination_locality_identity")
        or boundary is None
        or boundary.locality_identity != command.locality_identity
        or ledger.integrity_of(boundary.identity) == CORRUPTED
    ):
        raise OperatorInvocationLocalityError("invocation Locality assignment is not exact")
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
        raise OperatorInvocationLocalityError(
            "invocation Locality assignment does not follow material Standing"
        ) from error
    return event


def _act_material(assignment: Event) -> dict[str, Any]:
    material = assignment.material
    return {
        "operator_invocation_locality_act_identity": material[
            "operator_invocation_locality_act_identity"
        ],
        "act_occurrence_identity": material["act_occurrence_identity"],
        "result_boundary_identity": material["result_boundary_identity"],
        "act": OPERATOR_INVOCATION_LOCALITY_ACT,
        "responsibility_assignment_event_identity": assignment.identity,
        "operator_material_occurrence_reference": material[
            "operator_material_occurrence_reference"
        ],
        "operator_locality_identity": material["operator_locality_identity"],
        "destination_locality_identity": material[
            "destination_locality_identity"
        ],
        "relation_occurrence_identity": material[
            "relation_occurrence_identity"
        ],
        "scope": deepcopy(material["scope"]),
    }


def record_operator_invocation_locality_act_occurrence(
    ledger: EventLedger,
    *,
    responsibility_assignment_event_identity: str,
    responsibility_assignment_standing: dict[str, Any],
) -> Event:
    assignment = get_operator_invocation_locality_responsibility_assignment(
        ledger, responsibility_assignment_event_identity
    )
    carried = (
        responsibility_assignment_standing.get(
            "subject_to_act_binding_occurrences"
        )
        if type(responsibility_assignment_standing) is dict
        else None
    )
    if (
        type(carried) is not dict
        or carried.get(assignment.identity, object()) is not None
        or responsibility_assignment_standing.get("locality_identity")
        != assignment.locality_identity
    ):
        raise OperatorInvocationLocalityError(
            "invocation Locality Act requires its carried assignment"
        )
    return ledger.append(
        OPERATOR_INVOCATION_LOCALITY_ACT_OCCURRENCE_EVENT,
        _act_material(assignment),
        locality_identity=assignment.material["destination_locality_identity"],
    )


def get_operator_invocation_locality_act_occurrence(
    ledger: EventLedger, event_identity: str
) -> Event:
    event = ledger.get(
        _identity(event_identity, "invocation Locality requires Act occurrence")
    )
    if (
        event is None
        or event.kind != OPERATOR_INVOCATION_LOCALITY_ACT_OCCURRENCE_EVENT
        or event.exact_material is not None
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise OperatorInvocationLocalityError(
            "invocation Locality Act occurrence is absent or corrupted"
        )
    assignment = get_operator_invocation_locality_responsibility_assignment(
        ledger, event.material.get("responsibility_assignment_event_identity")
    )
    if (
        event.material != _act_material(assignment)
        or event.locality_identity
        != assignment.material.get("destination_locality_identity")
    ):
        raise OperatorInvocationLocalityError("invocation Locality Act occurrence is not exact")
    try:
        ledger.occurrences_in_append_order(
            (assignment.identity, event.identity),
            locality_identity=event.locality_identity,
        )
    except ValueError as error:
        raise OperatorInvocationLocalityError(
            "invocation Locality Act requires its prior assignment"
        ) from error
    return event


def _result_material(act: Event) -> dict[str, Any]:
    material = act.material
    relation = {
        "first_subject": material["operator_locality_identity"],
        "second_subject": material["destination_locality_identity"],
        "relation_occurrence_identity": material["relation_occurrence_identity"],
    }
    return {
        "result_identity": material["result_boundary_identity"],
        "operator_invocation_locality_act_identity": material[
            "operator_invocation_locality_act_identity"
        ],
        "act_occurrence_identity": material["act_occurrence_identity"],
        "exact_act": OPERATOR_INVOCATION_LOCALITY_ACT,
        "responsibility_assignment_event_identity": material[
            "responsibility_assignment_event_identity"
        ],
        "operator_material_occurrence_reference": material[
            "operator_material_occurrence_reference"
        ],
        "operator_locality_identity": material["operator_locality_identity"],
        "destination_locality_identity": material[
            "destination_locality_identity"
        ],
        "relation_occurrence_identity": material["relation_occurrence_identity"],
        "locality_relation": relation,
        "scope": deepcopy(material["scope"]),
        "known_loss": [],
        "conflicts": [],
        "unknown": [],
    }


def _refuse_second_yield(ledger: EventLedger, act: Event) -> None:
    for yield_relation in ledger.iter_locality_kind(
        act.locality_identity, RECORDED_YIELD_RELATION_EVENT
    ):
        if yield_relation.material.get("act_occurrence_event_identity") == act.identity:
            raise OperatorInvocationLocalityError(
                "invocation Locality Act already carries a Yield"
            )


def _recorded_result_material(
    result: dict[str, Any],
    *,
    act_occurrence_event_identity: str,
    yield_relation_identity: str,
) -> dict[str, Any]:
    return {
        "result_identity": result["result_identity"],
        "operator_invocation_locality_act_identity": result[
            "operator_invocation_locality_act_identity"
        ],
        "act_occurrence_identity": result["act_occurrence_identity"],
        "exact_act": result["exact_act"],
        "responsibility_assignment_event_identity": result[
            "responsibility_assignment_event_identity"
        ],
        "operator_material_occurrence_reference": result[
            "operator_material_occurrence_reference"
        ],
        "operator_locality_identity": result["operator_locality_identity"],
        "destination_locality_identity": result[
            "destination_locality_identity"
        ],
        "relation_occurrence_identity": result[
            "relation_occurrence_identity"
        ],
        "locality_relation": deepcopy(result["locality_relation"]),
        "scope": deepcopy(result["scope"]),
        "known_loss": list(result["known_loss"]),
        "conflicts": list(result["conflicts"]),
        "unknown": list(result["unknown"]),
        "act_occurrence_event_identity": act_occurrence_event_identity,
        "yield_relation_identity": (
            yield_relation_identity
        ),
    }


def record_operator_invocation_locality_result(
    ledger: EventLedger, *, act_occurrence_event_identity: str
) -> Event:
    act = get_operator_invocation_locality_act_occurrence(
        ledger, act_occurrence_event_identity
    )
    _refuse_second_yield(ledger, act)
    result = _result_material(act)
    yield_relation = _record_yield_relation(
        ledger,
        locality_identity=act.locality_identity,
        exact_act=OPERATOR_INVOCATION_LOCALITY_ACT,
        act_occurrence_identity=act.material["act_occurrence_identity"],
        act_occurrence_event_identity=act.identity,
        result_kind=OPERATOR_INVOCATION_LOCALITY_RESULT_KIND,
        result_identity=result["result_identity"],
        result_content=result,
        occurrence_boundary="operator_invocation_locality_relation",
    )
    return ledger.append(
        OPERATOR_INVOCATION_LOCALITY_RECORDED_KIND,
        _recorded_result_material(
            result,
            act_occurrence_event_identity=act.identity,
            yield_relation_identity=yield_relation.identity,
        ),
        locality_identity=act.locality_identity,
    )


def get_recorded_operator_invocation_locality(
    ledger: EventLedger, event_identity: str
) -> dict[str, Any]:
    event = ledger.get(
        _identity(event_identity, "invocation Locality requires one result")
    )
    if (
        event is None
        or event.kind != OPERATOR_INVOCATION_LOCALITY_RECORDED_KIND
        or event.exact_material is not None
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise OperatorInvocationLocalityError(
            "invocation Locality result is absent or corrupted"
        )
    act = get_operator_invocation_locality_act_occurrence(
        ledger, event.material.get("act_occurrence_event_identity")
    )
    result = _result_material(act)
    exact_result_material = _recorded_result_material(
        result,
        act_occurrence_event_identity=act.identity,
        yield_relation_identity=event.material.get(
            "yield_relation_identity"
        ),
    )
    if (
        event.locality_identity != act.locality_identity
        or event.material != exact_result_material
    ):
        raise OperatorInvocationLocalityError("invocation Locality result is not exact")
    requirements = read_requirements_of_yield_relation(
        ledger,
        recorded_result_event_identity=event.identity,
        yield_relation_event_identity=event.material[
            "yield_relation_identity"
        ],
        act_occurrence_event_identity=act.identity,
    )
    if not all(requirements.values()):
        raise OperatorInvocationLocalityError("invocation Locality result carries no exact Yield")
    return deepcopy(event.material)


def operator_invocation_locality_occurrence_references(
    ledger: EventLedger, event_identity: str
) -> tuple[str, str, str]:
    event = ledger.get(event_identity)
    result = get_recorded_operator_invocation_locality(ledger, event_identity)
    identities = (
        result["act_occurrence_event_identity"],
        result["yield_relation_identity"],
        event.identity,
    )
    ledger.occurrences_in_append_order(
        identities, locality_identity=event.locality_identity
    )
    return identities
