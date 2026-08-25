"""One exact operator-material boundary occurrence and its exact result."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from seed_runtime.event import Event
from seed_runtime.events import CORRUPTED, EventLedger
from seed_runtime.identities import new_identity
from seed_runtime.material_source import (
    MATERIAL_RESULT_UNKNOWN,
    _append_exact_material_result_occurrence,
)
from seed_runtime.operator_material_boundary import OperatorBoundaryMaterial
from seed_runtime.yield_relation import (
    RECORDED_YIELD_RELATION_EVENT,
    _record_yield_relation,
    read_requirements_of_yield_relation,
)


OPERATOR_MATERIAL_SOURCE_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND = (
    "operator.material.source_responsibility_assignment_recorded"
)
OPERATOR_MATERIAL_SOURCE_ACT_OCCURRENCE_EVENT = (
    "operator.material.source_act_occurrence_recorded"
)
OPERATOR_MATERIAL_SOURCE_RECORDED_KIND = "operator.material.source_recorded"
OPERATOR_MATERIAL_SOURCE_LOCALITY_RELATION_OCCURRENCE_KIND = (
    "operator.material.source_recorded"
)
OPERATOR_MATERIAL_SOURCE_RESULT_KIND = "exact operator material boundary result"
OPERATOR_MATERIAL_SOURCE_ACT = "Preserve one exact operator material boundary result"
OPERATOR_MATERIAL_SOURCE_RESPONSIBILITY = (
    "preserve one exact material result supplied at one operator boundary"
)
OPERATOR_MATERIAL_SOURCE_BOOK_CLAUSE = "01.Source.G"
EVENT_KIND_RESPONSIBILITIES = {
    OPERATOR_MATERIAL_SOURCE_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND: (
        "01.Source.G"
    ),
    OPERATOR_MATERIAL_SOURCE_ACT_OCCURRENCE_EVENT: "02.Acts.A",
    OPERATOR_MATERIAL_SOURCE_RECORDED_KIND: "01.Source.G",
}


class OperatorMaterialSourceError(ValueError):
    """One operator-material boundary occurrence is not exact."""


def _require_identity(value: Any, message: str) -> str:
    if type(value) is not str or not value:
        raise OperatorMaterialSourceError(message)
    return value


def _source_standing_reference(
    ledger: EventLedger,
    *,
    locality_identity: str,
    locality_standing: dict[str, Any],
    responsibility_event_identity: str | None = None,
) -> dict[str, str | None]:
    _require_identity(
        locality_identity,
        "operator material source requires one exact Locality",
    )
    if type(locality_standing) is not dict:
        raise OperatorMaterialSourceError(
            "operator material source requires exact Locality Standing"
        )
    if locality_standing.get("locality_identity") != locality_identity:
        raise OperatorMaterialSourceError(
            "operator material source has a different Standing Locality"
        )
    standing_boundary = locality_standing.get("through_event_occurrence_identity")
    if responsibility_event_identity is None:
        latest = ledger.latest_locality_event(locality_identity)
        prior_event_identity = latest.identity if latest is not None else None
    else:
        try:
            earlier = ledger.prior_locality_event(
                responsibility_event_identity, locality_identity
            )
        except ValueError as error:
            raise OperatorMaterialSourceError(
                "operator material source requires its exact current Standing boundary"
            ) from error
        prior_event_identity = earlier.identity if earlier is not None else None
    if standing_boundary != prior_event_identity:
        raise OperatorMaterialSourceError(
            "operator material source requires its exact current Standing boundary"
        )
    if standing_boundary is not None:
        _require_identity(
            standing_boundary,
            "operator material source requires one exact Standing boundary",
        )
        boundary_event = ledger.get(standing_boundary)
        if (
            boundary_event is None
            or boundary_event.locality_identity != locality_identity
            or ledger.integrity_of(boundary_event.identity) == CORRUPTED
        ):
            raise OperatorMaterialSourceError(
                "operator material source requires its exact current Standing boundary"
            )
    return {
        "locality_identity": locality_identity,
        "standing_boundary_event_identity": standing_boundary,
    }


def _scope(
    *,
    scope_identity: str,
    source_standing_reference: dict[str, str | None],
    result_boundary_identity: str,
) -> dict[str, str | None]:
    return {
        "scope_identity": scope_identity,
        **deepcopy(source_standing_reference),
        "result_boundary_identity": result_boundary_identity,
    }


def _assignment_material(
    *,
    assignment_identity: str,
    assignment_subject_identity: str,
    source_act_identity: str,
    act_occurrence_identity: str,
    scope_identity: str,
    result_boundary_identity: str,
    source_standing_reference: dict[str, str | None],
) -> dict[str, Any]:
    return {
        "assignment_identity": assignment_identity,
        "assignment_subject_identity": assignment_subject_identity,
        "book_clause_identity": OPERATOR_MATERIAL_SOURCE_BOOK_CLAUSE,
        "responsible_boundary": "this Seed",
        "responsibility": OPERATOR_MATERIAL_SOURCE_RESPONSIBILITY,
        "source_act_identity": source_act_identity,
        "act_occurrence_identity": act_occurrence_identity,
        "result_boundary_identity": result_boundary_identity,
        "source_standing_reference": deepcopy(source_standing_reference),
        "scope": _scope(
            scope_identity=scope_identity,
            source_standing_reference=source_standing_reference,
            result_boundary_identity=result_boundary_identity,
        ),
        "standing_boundary_occurrence_reference": source_standing_reference[
            "standing_boundary_event_identity"
        ],
        "unknown": [
            "operator boundary material: Unknown"
        ],
    }


def _assignment_reference(assignment: Event) -> dict[str, str]:
    return {
        "recorded_occurrence_identity": assignment.identity,
        "assignment_identity": assignment.material["assignment_identity"],
        "assignment_subject_identity": assignment.material[
            "assignment_subject_identity"
        ],
        "book_clause_identity": assignment.material["book_clause_identity"],
        "scope_identity": assignment.material["scope"]["scope_identity"],
        "result_boundary_identity": assignment.material[
            "result_boundary_identity"
        ],
    }


def _act_occurrence_material(assignment: Event) -> dict[str, Any]:
    material = assignment.material
    return {
        "source_act_identity": material["source_act_identity"],
        "act_occurrence_identity": material["act_occurrence_identity"],
        "act": OPERATOR_MATERIAL_SOURCE_ACT,
        "responsibility": OPERATOR_MATERIAL_SOURCE_RESPONSIBILITY,
        "responsible_boundary": "this Seed",
        "responsibility_assignment_reference": _assignment_reference(assignment),
        "source_standing_reference": deepcopy(
            material["source_standing_reference"]
        ),
        "scope": deepcopy(material["scope"]),
        "result_boundary_identity": material["result_boundary_identity"],
    }


def _result_material(
    act_occurrence: Event,
    *,
    boundary_material: OperatorBoundaryMaterial,
    recorded_result_event_identity: str,
) -> dict[str, Any]:
    material = act_occurrence.material
    exact_material_subject = {
        "recorded_occurrence_identity": recorded_result_event_identity,
        "coordinate": "exact_material",
    }
    return {
        "result_identity": material["result_boundary_identity"],
        "source_act_identity": material["source_act_identity"],
        "act_occurrence_identity": material["act_occurrence_identity"],
        "exact_act": OPERATOR_MATERIAL_SOURCE_ACT,
        "responsibility": OPERATOR_MATERIAL_SOURCE_RESPONSIBILITY,
        "responsible_boundary": "this Seed",
        "responsibility_assignment_reference": deepcopy(
            material["responsibility_assignment_reference"]
        ),
        "source_standing_reference": deepcopy(
            material["source_standing_reference"]
        ),
        "scope": deepcopy(material["scope"]),
        "source_boundary": boundary_material.material_boundary,
        "locality_relation": {
            "first_subject": exact_material_subject,
            "relation": "locality",
            "second_subject": "this Seed",
            "relation_occurrence_identity": recorded_result_event_identity,
        },
        "locality_relation_occurrence_identity": recorded_result_event_identity,
        "known_loss": list(boundary_material.known_loss),
        "standing": "preserved",
        "unknown": list(MATERIAL_RESULT_UNKNOWN),
    }


def _recorded_result_material(
    result_material: dict[str, Any],
    *,
    act_occurrence_event_identity: str | None = None,
    yield_relation_identity: str | None = None,
) -> dict[str, Any]:
    recorded = {
        "result_identity": result_material["result_identity"],
        "source_act_identity": result_material["source_act_identity"],
        "act_occurrence_identity": result_material["act_occurrence_identity"],
        "exact_act": result_material["exact_act"],
        "responsibility": result_material["responsibility"],
        "responsible_boundary": result_material["responsible_boundary"],
        "responsibility_assignment_reference": result_material[
            "responsibility_assignment_reference"
        ],
        "source_standing_reference": result_material[
            "source_standing_reference"
        ],
        "scope": result_material["scope"],
        "source_boundary": result_material["source_boundary"],
        "locality_relation": result_material["locality_relation"],
        "locality_relation_occurrence_identity": result_material[
            "locality_relation_occurrence_identity"
        ],
        "known_loss": result_material["known_loss"],
        "standing": result_material["standing"],
        "unknown": result_material["unknown"],
        "source_role": "this operator",
        "provenance_occurrence_references": [],
        "dimensions": {
            "identity": result_material["result_identity"],
            "source_provenance": result_material["source_boundary"],
            "responsibility": result_material["responsibility"],
            "scope_locality": (
                "locality:"
                + result_material["source_standing_reference"][
                    "locality_identity"
                ]
            ),
            "occurrence_preservation": (
                "exact operator material material source occurrence recorded"
            ),
        },
    }
    if act_occurrence_event_identity is not None:
        recorded["act_occurrence_event_identity"] = (
            act_occurrence_event_identity
        )
    if yield_relation_identity is not None:
        recorded["yield_relation_identity"] = (
            yield_relation_identity
        )
    return recorded


def record_operator_material_source_responsibility_assignment(
    ledger: EventLedger,
    *,
    locality_identity: str,
    locality_standing: dict[str, Any],
) -> Event:
    """Assign Responsibility for exactly one later boundary occurrence."""

    if not isinstance(ledger, EventLedger):
        raise TypeError("operator material source requires one EventLedger")
    source_reference = _source_standing_reference(
        ledger,
        locality_identity=locality_identity,
        locality_standing=locality_standing,
    )
    return _record_operator_material_source_responsibility_assignment(
        ledger,
        locality_identity=locality_identity,
        source_reference=source_reference,
    )


def _record_operator_material_source_responsibility_assignment_from_standing(
    ledger: EventLedger,
    *,
    locality_identity: str,
    locality_standing: dict[str, Any],
) -> Event:
    source_reference = _source_standing_reference(
        ledger,
        locality_identity=locality_identity,
        locality_standing=locality_standing,
    )
    return _record_operator_material_source_responsibility_assignment(
        ledger,
        locality_identity=locality_identity,
        source_reference=source_reference,
    )


def _record_operator_material_source_responsibility_assignment(
    ledger: EventLedger,
    *,
    locality_identity: str,
    source_reference: dict[str, str | None],
) -> Event:
    assignment_identity = new_identity("operator_material_source_assignment")
    assignment_subject_identity = new_identity(
        "operator_material_source_assignment_subject"
    )
    source_act_identity = new_identity("operator_material_source_act")
    act_occurrence_identity = new_identity(
        "operator_material_source_act_occurrence"
    )
    scope_identity = new_identity("operator_material_source_scope")
    result_boundary_identity = new_identity(
        "operator_material_source_result_boundary"
    )
    return ledger.append(
        OPERATOR_MATERIAL_SOURCE_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND,
        _assignment_material(
            assignment_identity=assignment_identity,
            assignment_subject_identity=assignment_subject_identity,
            source_act_identity=source_act_identity,
            act_occurrence_identity=act_occurrence_identity,
            scope_identity=scope_identity,
            result_boundary_identity=result_boundary_identity,
            source_standing_reference=source_reference,
        ),
        locality_identity=locality_identity,
    )


def get_operator_material_source_responsibility_assignment(
    ledger: EventLedger, assignment_event_identity: str
) -> Event:
    """Read one intact Book-backed assignment occurrence."""

    _require_identity(
        assignment_event_identity,
        "operator material source requires one assignment occurrence",
    )
    assignment = ledger.get(assignment_event_identity)
    if (
        assignment is None
        or assignment.kind
        != OPERATOR_MATERIAL_SOURCE_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND
        or type(assignment.locality_identity) is not str
        or not assignment.locality_identity
        or assignment.exact_material is not None
        or ledger.integrity_of(assignment.identity) == CORRUPTED
    ):
        raise OperatorMaterialSourceError(
            "operator material source assignment is absent or corrupted"
        )
    material = assignment.material
    source_reference = material.get("source_standing_reference")
    scope = material.get("scope")
    identities = (
        material.get("assignment_identity"),
        material.get("assignment_subject_identity"),
        material.get("source_act_identity"),
        material.get("act_occurrence_identity"),
        scope.get("scope_identity") if type(scope) is dict else None,
        material.get("result_boundary_identity"),
    )
    if (
        type(source_reference) is not dict
        or source_reference.get("locality_identity") != assignment.locality_identity
        or any(type(identity) is not str or not identity for identity in identities)
        or len(set(identities)) != len(identities)
    ):
        raise OperatorMaterialSourceError(
            "operator material source assignment coordinates are not exact"
        )
    exact_source_reference = _source_standing_reference(
        ledger,
        locality_identity=assignment.locality_identity,
        locality_standing={
            "locality_identity": assignment.locality_identity,
            "through_event_occurrence_identity": source_reference.get(
                "standing_boundary_event_identity"
            ),
        },
        responsibility_event_identity=assignment.identity,
    )
    exact_assignment_material = _assignment_material(
        assignment_identity=identities[0],
        assignment_subject_identity=identities[1],
        source_act_identity=identities[2],
        act_occurrence_identity=identities[3],
        scope_identity=identities[4],
        result_boundary_identity=identities[5],
        source_standing_reference=exact_source_reference,
    )
    if material != exact_assignment_material:
        raise OperatorMaterialSourceError(
            "operator material source assignment is not exact"
        )
    return assignment


def record_operator_material_source_act_occurrence(
    ledger: EventLedger,
    *,
    responsibility_assignment_event_identity: str,
    responsibility_assignment_standing: dict[str, Any],
) -> Event:
    """Record the distinct Act occurrence from its carried assignment."""

    assignment = get_operator_material_source_responsibility_assignment(
        ledger, responsibility_assignment_event_identity
    )
    return _record_operator_material_source_act_occurrence(
        ledger,
        assignment=assignment,
        responsibility_assignment_standing=responsibility_assignment_standing,
    )


def _record_operator_material_source_act_occurrence_from_assignment(
    ledger: EventLedger,
    *,
    responsibility_assignment: Event,
    responsibility_assignment_standing: dict[str, Any],
) -> Event:
    if (
        type(responsibility_assignment) is not Event
        or responsibility_assignment.kind
        != OPERATOR_MATERIAL_SOURCE_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND
        or responsibility_assignment.exact_material is not None
        or type(responsibility_assignment_standing) is not dict
        or responsibility_assignment_standing.get(
            "through_event_occurrence_identity"
        )
        != responsibility_assignment.identity
    ):
        raise OperatorMaterialSourceError(
            "operator material source Act requires its recorded assignment"
        )
    return _record_operator_material_source_act_occurrence(
        ledger,
        assignment=responsibility_assignment,
        responsibility_assignment_standing=responsibility_assignment_standing,
    )


def _record_operator_material_source_act_occurrence(
    ledger: EventLedger,
    *,
    assignment: Event,
    responsibility_assignment_standing: dict[str, Any],
) -> Event:
    if type(responsibility_assignment_standing) is not dict:
        raise OperatorMaterialSourceError(
            "operator material source Act requires assignment Standing"
        )
    carried = responsibility_assignment_standing.get(
        "responsibility_assignment_occurrences"
    )
    if (
        responsibility_assignment_standing.get("locality_identity")
        != assignment.locality_identity
        or type(carried) is not dict
        or carried.get(assignment.identity, object()) is not None
    ):
        raise OperatorMaterialSourceError(
            "operator material source Act requires its exact carried assignment"
        )
    return ledger.append(
        OPERATOR_MATERIAL_SOURCE_ACT_OCCURRENCE_EVENT,
        _act_occurrence_material(assignment),
        locality_identity=assignment.locality_identity,
    )


def get_operator_material_source_act_occurrence(
    ledger: EventLedger, act_occurrence_event_identity: str
) -> Event:
    """Read one exact source Act occurrence occurrence."""

    _require_identity(
        act_occurrence_event_identity,
        "operator material source result requires one Act occurrence occurrence",
    )
    act_occurrence = ledger.get(act_occurrence_event_identity)
    if (
        act_occurrence is None
        or act_occurrence.kind != OPERATOR_MATERIAL_SOURCE_ACT_OCCURRENCE_EVENT
        or type(act_occurrence.locality_identity) is not str
        or not act_occurrence.locality_identity
        or act_occurrence.exact_material is not None
        or ledger.integrity_of(act_occurrence.identity) == CORRUPTED
    ):
        raise OperatorMaterialSourceError(
            "operator material source requires intact Act occurrence"
        )
    reference = act_occurrence.material.get("responsibility_assignment_reference")
    if type(reference) is not dict:
        raise OperatorMaterialSourceError(
            "operator material source Act carries no assignment"
        )
    assignment = get_operator_material_source_responsibility_assignment(
        ledger, reference.get("recorded_occurrence_identity")
    )
    if (
        assignment.locality_identity != act_occurrence.locality_identity
        or reference != _assignment_reference(assignment)
        or act_occurrence.material != _act_occurrence_material(assignment)
    ):
        raise OperatorMaterialSourceError(
            "operator material source Act occurrence is not exact"
        )
    try:
        ledger.occurrences_in_append_order(
            (assignment.identity, act_occurrence.identity),
            locality_identity=act_occurrence.locality_identity,
        )
    except ValueError as error:
        raise OperatorMaterialSourceError(
            "operator material source Act requires its prior assignment"
        ) from error
    return act_occurrence


def record_operator_material_source_result(
    ledger: EventLedger,
    *,
    act_occurrence_event_identity: str,
    boundary_material: OperatorBoundaryMaterial,
) -> Event:
    """Record one exact nonempty boundary result and its Yield."""

    act_occurrence = get_operator_material_source_act_occurrence(
        ledger, act_occurrence_event_identity
    )
    return _record_operator_material_source_result(
        ledger,
        act_occurrence=act_occurrence,
        boundary_material=boundary_material,
    )


def _record_operator_material_source_result(
    ledger: EventLedger,
    *,
    act_occurrence: Event,
    boundary_material: OperatorBoundaryMaterial,
) -> Event:
    if not isinstance(boundary_material, OperatorBoundaryMaterial):
        raise TypeError("operator material source requires exact boundary material")
    if boundary_material.eof:
        raise OperatorMaterialSourceError(
            "an empty operator boundary establishes no material result"
        )
    act_occurrence_identity = act_occurrence.material["act_occurrence_identity"]
    for prior_yield in ledger.iter_locality_kind(
        act_occurrence.locality_identity, RECORDED_YIELD_RELATION_EVENT
    ):
        if (
            prior_yield.material.get("act_occurrence_event_identity")
            == act_occurrence.identity
            or prior_yield.material.get("dimensions", {}).get(
                "act_occurrence_identity"
            )
            == act_occurrence_identity
        ):
            raise OperatorMaterialSourceError(
                "operator material source Act already carries a Yield"
            )
    recorded_result_event_identity = ledger.allocate_event_identity()
    result_material = _result_material(
        act_occurrence,
        boundary_material=boundary_material,
        recorded_result_event_identity=recorded_result_event_identity,
    )
    yield_relation = _record_yield_relation(
        ledger,
        locality_identity=act_occurrence.locality_identity,
        exact_act="Preserve one exact operator material boundary result",
        act_occurrence_identity=act_occurrence_identity,
        act_occurrence_event_identity=act_occurrence.identity,
        result_kind=OPERATOR_MATERIAL_SOURCE_RESULT_KIND,
        result_identity=result_material["result_identity"],
        result_content=result_material,
        responsibility=OPERATOR_MATERIAL_SOURCE_RESPONSIBILITY,
        occurrence_boundary="operator_material_source",
        responsible_boundary="this Seed",
        result_exact_material=boundary_material.exact_bytes,
    )
    return _append_exact_material_result_occurrence(
        ledger,
        result_event=Event(
            identity=recorded_result_event_identity,
            kind=OPERATOR_MATERIAL_SOURCE_RECORDED_KIND,
            material=_recorded_result_material(
                result_material,
                act_occurrence_event_identity=act_occurrence.identity,
                yield_relation_identity=(
                    yield_relation.identity
                ),
            ),
            exact_material=boundary_material.exact_bytes,
            locality_identity=act_occurrence.locality_identity,
        ),
    )


def read_operator_material_source_locality_relation_requirements(
    ledger: EventLedger,
    *,
    recorded_result_event_identity: str,
) -> dict[str, bool]:
    """Read the exact material-to-this-Seed Locality relation in O1."""

    result = ledger.get(recorded_result_event_identity)
    if result is None or result.kind != OPERATOR_MATERIAL_SOURCE_RECORDED_KIND:
        return {
            "exact_relation": False,
            "occurrence_witness": False,
            "intact_occurrence": False,
        }
    relation = result.material.get("locality_relation")
    exact_material_subject = {
        "recorded_occurrence_identity": result.identity,
        "coordinate": "exact_material",
    }
    yield_relation = ledger.get(result.material.get("locality_relation_occurrence_identity"))
    relation_is_result_occurrence = bool(
        yield_relation is not None
        and yield_relation.identity == result.identity
        and yield_relation.kind == result.kind
        and yield_relation.locality_identity == result.locality_identity
        and yield_relation.material == result.material
        and yield_relation.exact_material == result.exact_material
    )
    existing_o1_physiology = False
    try:
        act_occurrence = get_operator_material_source_act_occurrence(
            ledger,
            result.material.get("act_occurrence_event_identity"),
        )
        yield_relation = ledger.get(
            result.material.get("yield_relation_identity")
        )
        yield_dimensions = (
            yield_relation.material.get("dimensions", {})
            if yield_relation is not None
            else {}
        )
        existing_o1_physiology = bool(
            yield_relation is not None
            and yield_relation.kind == RECORDED_YIELD_RELATION_EVENT
            and yield_relation.locality_identity == result.locality_identity
            and yield_relation.exact_material == result.exact_material
            and yield_relation.material.get("act_occurrence_event_identity")
            == act_occurrence.identity
            and yield_relation.material.get("result_identity")
            == result.material.get("result_identity")
            and yield_dimensions.get("exact_act") == OPERATOR_MATERIAL_SOURCE_ACT
            and yield_dimensions.get("act_occurrence_identity")
            == result.material.get("act_occurrence_identity")
            and yield_dimensions.get("responsibility")
            == OPERATOR_MATERIAL_SOURCE_RESPONSIBILITY
            and yield_dimensions.get("responsible_boundary") == "this Seed"
            and act_occurrence.locality_identity == result.locality_identity
            and result.material.get("responsible_boundary") == "this Seed"
            and type(result.material.get("source_boundary")) is str
            and bool(result.material["source_boundary"])
            and ledger.integrity_of(act_occurrence.identity) != CORRUPTED
            and ledger.integrity_of(yield_relation.identity) != CORRUPTED
        )
    except (TypeError, ValueError):
        existing_o1_physiology = False
    return {
        "exact_relation": bool(
            type(relation) is dict
            and relation.get("first_subject") == exact_material_subject
            and relation.get("relation") == "locality"
            and relation.get("second_subject") == "this Seed"
            and type(result.exact_material) is bytes
            and bool(result.exact_material)
        ),
        "occurrence_witness": bool(
            type(relation) is dict
            and relation.get("relation_occurrence_identity") == result.identity
        ),
        "intact_occurrence": bool(
            relation_is_result_occurrence
            and existing_o1_physiology
            and ledger.integrity_of(result.identity) != CORRUPTED
        ),
    }


def get_recorded_operator_material_source(
    ledger: EventLedger, result_event_identity: str
) -> dict[str, Any]:
    """Read one exact boundary result through its exact Act and Yield."""

    _require_identity(
        result_event_identity,
        "operator material source read requires one result occurrence",
    )
    result = ledger.get(result_event_identity)
    if (
        result is None
        or result.kind != OPERATOR_MATERIAL_SOURCE_RECORDED_KIND
        or type(result.locality_identity) is not str
        or not result.locality_identity
        or type(result.exact_material) is not bytes
        or not result.exact_material
        or ledger.integrity_of(result.identity) == CORRUPTED
    ):
        raise OperatorMaterialSourceError(
            "operator material source result is absent or corrupted"
        )
    act_occurrence = get_operator_material_source_act_occurrence(
        ledger, result.material.get("act_occurrence_event_identity")
    )
    boundary = OperatorBoundaryMaterial(
        exact_bytes=result.exact_material,
        eof=False,
        material_boundary=result.material.get("source_boundary"),
        known_loss=tuple(result.material.get("known_loss", ())),
    )
    act_result_material = _result_material(
        act_occurrence,
        boundary_material=boundary,
        recorded_result_event_identity=result.identity,
    )
    exact_recorded_material = _recorded_result_material(
        act_result_material,
        act_occurrence_event_identity=act_occurrence.identity,
        yield_relation_identity=result.material.get("yield_relation_identity"),
    )
    if (
        result.locality_identity != act_occurrence.locality_identity
        or result.material != exact_recorded_material
    ):
        raise OperatorMaterialSourceError(
            "operator material source result coordinates are not exact"
        )
    requirements = read_requirements_of_yield_relation(
        ledger,
        recorded_result_event_identity=result.identity,
        yield_relation_event_identity=result.material["yield_relation_identity"],
        act_occurrence_event_identity=act_occurrence.identity,
    )
    if not all(requirements.values()):
        raise OperatorMaterialSourceError(
            "operator material source carries no exact Yield relation"
        )
    locality_requirements = (
        read_operator_material_source_locality_relation_requirements(
            ledger,
            recorded_result_event_identity=result.identity,
        )
    )
    if not all(locality_requirements.values()):
        raise OperatorMaterialSourceError(
            "operator material source carries no exact Locality relation"
        )
    return deepcopy(result.material)
