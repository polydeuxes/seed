"""One operator invocation Locality related to one operator Locality."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from seed_runtime.event import Event
from seed_runtime.events import CORRUPTED, EventLedger
from seed_runtime.identities import new_identity
from seed_runtime.material_acquisition import read_exact_material_acquisition_result
from seed_runtime.evidence_of_yield_relation import (
    RECORDED_EVIDENCE_OF_YIELD_RELATION_KIND,
    _record_evidence_of_yield_relation,
    read_requirements_of_yield_relation,
)


OPERATOR_SYSTEM_LOCALITY_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND = (
    "operator.invocation_locality_responsibility_assignment_recorded"
)
OPERATOR_SYSTEM_LOCALITY_ACT_EVIDENCE_KIND = (
    "operator.invocation_locality_act_evidenced"
)
OPERATOR_SYSTEM_LOCALITY_RECORDED_KIND = "operator.invocation_locality_recorded"
OPERATOR_SYSTEM_LOCALITY_BOOK_CLAUSE = "06.Locality.D"
OPERATOR_SYSTEM_LOCALITY_ACT = (
    "Establish one direct operator invocation Locality relation"
)
OPERATOR_SYSTEM_LOCALITY_RESPONSIBILITY = (
    "preserve one operator invocation Locality relation from one operator Locality"
)
OPERATOR_SYSTEM_LOCALITY_RESULT_KIND = (
    "operator invocation Locality relation result"
)

EVENT_KIND_RESPONSIBILITIES = {
    OPERATOR_SYSTEM_LOCALITY_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND: (
        "06.Locality.D"
    ),
    OPERATOR_SYSTEM_LOCALITY_ACT_EVIDENCE_KIND: "02.Acts.A",
    OPERATOR_SYSTEM_LOCALITY_RECORDED_KIND: "06.Locality.A",
}


class OperatorSystemLocalityError(ValueError):
    """One operator invocation Locality boundary is absent or incoherent."""


def _identity(value: Any, message: str) -> str:
    if type(value) is not str or not value:
        raise OperatorSystemLocalityError(message)
    return value


def _command_event(ledger: EventLedger, event_identity: str) -> Event:
    event = ledger.get(
        _identity(event_identity, "invocation Locality requires one operator occurrence")
    )
    if (
        event is None
        or event.material.get("source_role") != "operator"
        or type(event.exact_material) is not bytes
        or not event.exact_material.startswith(b"!")
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise OperatorSystemLocalityError(
            "invocation Locality requires one intact operator material occurrence"
        )
    try:
        read_exact_material_acquisition_result(ledger, event.identity)
    except (TypeError, ValueError) as error:
        raise OperatorSystemLocalityError(
            "invocation Locality requires one intact operator material occurrence"
        ) from error
    requirements = read_requirements_of_yield_relation(
        ledger,
        recorded_result_event_identity=event.identity,
        evidence_of_yield_relation_event_identity=event.material.get(
            "evidence_of_yield_relation_identity"
        ),
        responsible_act_evidence_event_identity=event.material.get(
            "responsible_act_evidence_identity"
        ),
    )
    if not all(requirements.values()):
        raise OperatorSystemLocalityError(
            "operator command occurrence carries no exact Yield"
        )
    return event


def _assignment_material(
    *,
    command: Event,
    standing_boundary_identity: str,
    assignment_identity: str,
    assignment_subject_identity: str,
    operator_invocation_locality_act_identity: str,
    act_occurrence_identity: str,
    relation_occurrence_identity: str,
    result_identity: str,
    destination_locality_identity: str,
    scope_identity: str,
) -> dict[str, Any]:
    return {
        "assignment_identity": assignment_identity,
        "assignment_subject_identity": assignment_subject_identity,
        "book_clause_identity": OPERATOR_SYSTEM_LOCALITY_BOOK_CLAUSE,
        "responsible_boundary": "this Seed",
        "responsibility": OPERATOR_SYSTEM_LOCALITY_RESPONSIBILITY,
        "exact_act": OPERATOR_SYSTEM_LOCALITY_ACT,
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
            "scope_identity": scope_identity,
            "operator_locality_identity": command.locality_identity,
            "destination_locality_identity": destination_locality_identity,
            "operator_material_occurrence_reference": command.identity,
        },
        "authority": {
            "standing": "operator Authority",
            "source_occurrence_reference": command.identity,
            "limit": "this exact operator material occurrence",
        },
        "limits": [
            "one operator material occurrence establishes one new destination Locality",
            "the relation carries no operator Standing into the destination Locality",
        ],
        "unknown": [],
    }


def record_operator_system_locality_responsibility_assignment(
    ledger: EventLedger,
    *,
    operator_material_occurrence_reference: str,
    operator_locality_standing: dict[str, Any],
) -> Event:
    """Assign one invocation Locality under one exact operator Authority."""

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
        or carried.get(command.identity, object()) is not None
        or operator_locality_standing.get("locality_identity")
        != command.locality_identity
        or type(boundary_identity) is not str
        or not boundary_identity
    ):
        raise OperatorSystemLocalityError(
            "invocation Locality assignment requires exact operator material Standing"
        )
    for assignment in ledger.list_events():
        if (
            assignment.kind
            == OPERATOR_SYSTEM_LOCALITY_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND
            and assignment.material.get("operator_material_occurrence_reference")
            == command.identity
        ):
            raise OperatorSystemLocalityError(
                "operator material occurrence already carries an invocation Locality assignment"
            )
    identities = {
        "assignment_identity": new_identity("operator_invocation_locality_assignment"),
        "assignment_subject_identity": new_identity(
            "operator_invocation_locality_assignment_subject"
        ),
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
        "scope_identity": new_identity("operator_invocation_locality_scope"),
    }
    if len(set(identities.values())) != len(identities):
        raise OperatorSystemLocalityError("invocation Locality identities are compressed")
    return ledger.append(
        OPERATOR_SYSTEM_LOCALITY_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND,
        _assignment_material(
            command=command,
            standing_boundary_identity=boundary_identity,
            **identities,
        ),
        locality_identity=identities["destination_locality_identity"],
    )


def get_operator_system_locality_responsibility_assignment(
    ledger: EventLedger, event_identity: str
) -> Event:
    event = ledger.get(
        _identity(event_identity, "invocation Locality requires one assignment")
    )
    if (
        event is None
        or event.kind
        != OPERATOR_SYSTEM_LOCALITY_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND
        or event.exact_material is not None
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise OperatorSystemLocalityError(
            "invocation Locality assignment is absent or corrupted"
        )
    material = event.material
    command = _command_event(
        ledger, material.get("operator_material_occurrence_reference")
    )
    identity_coordinates = (
        "assignment_identity",
        "assignment_subject_identity",
        "operator_invocation_locality_act_identity",
        "act_occurrence_identity",
        "relation_occurrence_identity",
        "result_boundary_identity",
        "destination_locality_identity",
    )
    identities = tuple(material.get(key) for key in identity_coordinates)
    scope = material.get("scope")
    scope_identity = scope.get("scope_identity") if type(scope) is dict else None
    if (
        any(type(value) is not str or not value for value in (*identities, scope_identity))
        or len(set((*identities, scope_identity))) != len((*identities, scope_identity))
    ):
        raise OperatorSystemLocalityError(
            "invocation Locality assignment identities are not exact"
        )
    exact_assignment_material = _assignment_material(
        command=command,
        standing_boundary_identity=material.get(
            "operator_standing_boundary_identity"
        ),
        assignment_identity=identities[0],
        assignment_subject_identity=identities[1],
        operator_invocation_locality_act_identity=identities[2],
        act_occurrence_identity=identities[3],
        relation_occurrence_identity=identities[4],
        result_identity=identities[5],
        destination_locality_identity=identities[6],
        scope_identity=scope_identity,
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
        raise OperatorSystemLocalityError("invocation Locality assignment is not exact")
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
        raise OperatorSystemLocalityError(
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
        "act": OPERATOR_SYSTEM_LOCALITY_ACT,
        "responsibility": OPERATOR_SYSTEM_LOCALITY_RESPONSIBILITY,
        "responsible_boundary": "this Seed",
        "responsibility_assignment_event_identity": assignment.identity,
        "assignment_identity": material["assignment_identity"],
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
        "authority": deepcopy(material["authority"]),
        "evidence_scope": "Evidence bounded to one direct operator invocation Locality relation",
    }


def record_operator_system_locality_act_evidence(
    ledger: EventLedger,
    *,
    responsibility_assignment_event_identity: str,
    responsibility_assignment_standing: dict[str, Any],
) -> Event:
    assignment = get_operator_system_locality_responsibility_assignment(
        ledger, responsibility_assignment_event_identity
    )
    carried = (
        responsibility_assignment_standing.get(
            "responsibility_assignment_occurrences"
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
        raise OperatorSystemLocalityError(
            "invocation Locality Act requires its carried assignment"
        )
    return ledger.append(
        OPERATOR_SYSTEM_LOCALITY_ACT_EVIDENCE_KIND,
        _act_material(assignment),
        locality_identity=assignment.material["destination_locality_identity"],
    )


def get_operator_system_locality_act_evidence(
    ledger: EventLedger, event_identity: str
) -> Event:
    event = ledger.get(
        _identity(event_identity, "invocation Locality requires Act Evidence")
    )
    if (
        event is None
        or event.kind != OPERATOR_SYSTEM_LOCALITY_ACT_EVIDENCE_KIND
        or event.exact_material is not None
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise OperatorSystemLocalityError(
            "invocation Locality Act Evidence is absent or corrupted"
        )
    assignment = get_operator_system_locality_responsibility_assignment(
        ledger, event.material.get("responsibility_assignment_event_identity")
    )
    if (
        event.material != _act_material(assignment)
        or event.locality_identity
        != assignment.material.get("destination_locality_identity")
    ):
        raise OperatorSystemLocalityError("invocation Locality Act Evidence is not exact")
    try:
        ledger.occurrences_in_append_order(
            (assignment.identity, event.identity),
            locality_identity=event.locality_identity,
        )
    except ValueError as error:
        raise OperatorSystemLocalityError(
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
        "exact_act": OPERATOR_SYSTEM_LOCALITY_ACT,
        "responsibility": OPERATOR_SYSTEM_LOCALITY_RESPONSIBILITY,
        "responsible_boundary": "this Seed",
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
        "authority": deepcopy(material["authority"]),
        "standing": "established",
        "known_loss": [],
        "conflicts": [],
        "unknown": [],
        "negative_authority": [
            "the relation carries no operator Standing into the destination Locality",
            "the relation establishes no enclosure or hierarchy",
        ],
    }


def _refuse_second_yield(ledger: EventLedger, act: Event) -> None:
    for evidence in ledger.iter_locality_kind(
        act.locality_identity, RECORDED_EVIDENCE_OF_YIELD_RELATION_KIND
    ):
        if evidence.material.get("responsible_act_evidence_identity") == act.identity:
            raise OperatorSystemLocalityError(
                "invocation Locality Act already carries a Yield"
            )


def _recorded_result_material(
    result: dict[str, Any],
    *,
    responsible_act_evidence_identity: str,
    evidence_of_yield_relation_identity: str,
) -> dict[str, Any]:
    return {
        "result_identity": result["result_identity"],
        "operator_invocation_locality_act_identity": result[
            "operator_invocation_locality_act_identity"
        ],
        "act_occurrence_identity": result["act_occurrence_identity"],
        "exact_act": result["exact_act"],
        "responsibility": result["responsibility"],
        "responsible_boundary": result["responsible_boundary"],
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
        "authority": deepcopy(result["authority"]),
        "standing": result["standing"],
        "known_loss": list(result["known_loss"]),
        "conflicts": list(result["conflicts"]),
        "unknown": list(result["unknown"]),
        "negative_authority": list(result["negative_authority"]),
        "responsible_act_evidence_identity": responsible_act_evidence_identity,
        "evidence_of_yield_relation_identity": (
            evidence_of_yield_relation_identity
        ),
    }


def record_operator_system_locality_result(
    ledger: EventLedger, *, responsible_act_evidence_event_identity: str
) -> Event:
    act = get_operator_system_locality_act_evidence(
        ledger, responsible_act_evidence_event_identity
    )
    _refuse_second_yield(ledger, act)
    result = _result_material(act)
    evidence = _record_evidence_of_yield_relation(
        ledger,
        locality_identity=act.locality_identity,
        exact_act=OPERATOR_SYSTEM_LOCALITY_ACT,
        act_occurrence_identity=act.material["act_occurrence_identity"],
        responsible_act_evidence_identity=act.identity,
        result_kind=OPERATOR_SYSTEM_LOCALITY_RESULT_KIND,
        result_identity=result["result_identity"],
        result_content=result,
        responsibility=OPERATOR_SYSTEM_LOCALITY_RESPONSIBILITY,
        occurrence_boundary="operator_invocation_locality_relation",
        responsible_boundary="this Seed",
    )
    return ledger.append(
        OPERATOR_SYSTEM_LOCALITY_RECORDED_KIND,
        _recorded_result_material(
            result,
            responsible_act_evidence_identity=act.identity,
            evidence_of_yield_relation_identity=evidence.identity,
        ),
        locality_identity=act.locality_identity,
    )


def get_recorded_operator_system_locality(
    ledger: EventLedger, event_identity: str
) -> dict[str, Any]:
    event = ledger.get(
        _identity(event_identity, "invocation Locality requires one result")
    )
    if (
        event is None
        or event.kind != OPERATOR_SYSTEM_LOCALITY_RECORDED_KIND
        or event.exact_material is not None
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise OperatorSystemLocalityError(
            "invocation Locality result is absent or corrupted"
        )
    act = get_operator_system_locality_act_evidence(
        ledger, event.material.get("responsible_act_evidence_identity")
    )
    result = _result_material(act)
    exact_result_material = _recorded_result_material(
        result,
        responsible_act_evidence_identity=act.identity,
        evidence_of_yield_relation_identity=event.material.get(
            "evidence_of_yield_relation_identity"
        ),
    )
    if (
        event.locality_identity != act.locality_identity
        or event.material != exact_result_material
    ):
        raise OperatorSystemLocalityError("invocation Locality result is not exact")
    requirements = read_requirements_of_yield_relation(
        ledger,
        recorded_result_event_identity=event.identity,
        evidence_of_yield_relation_event_identity=event.material[
            "evidence_of_yield_relation_identity"
        ],
        responsible_act_evidence_event_identity=act.identity,
    )
    if not all(requirements.values()):
        raise OperatorSystemLocalityError("invocation Locality result carries no exact Yield")
    return deepcopy(event.material)


def operator_system_locality_occurrence_references(
    ledger: EventLedger, event_identity: str
) -> tuple[str, str, str]:
    event = ledger.get(event_identity)
    result = get_recorded_operator_system_locality(ledger, event_identity)
    identities = (
        result["responsible_act_evidence_identity"],
        result["evidence_of_yield_relation_identity"],
        event.identity,
    )
    ledger.occurrences_in_append_order(
        identities, locality_identity=event.locality_identity
    )
    return identities
