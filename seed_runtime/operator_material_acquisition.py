"""One exact operator-material boundary occurrence and its raw result."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from seed_runtime.event import Event
from seed_runtime.events import CORRUPTED, EventLedger
from seed_runtime.identities import new_identity
from seed_runtime.material_ingest import MATERIAL_RESULT_UNKNOWNS
from seed_runtime.operator_material_boundary import OperatorBoundaryMaterial
from seed_runtime.operator_representation import read_operator_representation
from seed_runtime.evidence_of_yield_relation import (
    RECORDED_EVIDENCE_OF_YIELD_RELATION_KIND,
    _record_evidence_of_yield_relation,
    read_requirements_of_yield_relation,
)


OPERATOR_MATERIAL_ACQUIRE_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND = (
    "operator.material.acquire_responsibility_assignment_recorded"
)
OPERATOR_MATERIAL_ACQUIRE_ACT_EVIDENCE_KIND = (
    "operator.material.acquire_act_evidenced"
)
OPERATOR_MATERIAL_ACQUIRE_RECORDED_KIND = "operator.material.acquire_recorded"
OPERATOR_MATERIAL_ACQUIRE_RESULT_KIND = "exact operator material boundary result"
OPERATOR_MATERIAL_ACQUIRE_ACT = "Acquire one exact operator material boundary result"
OPERATOR_MATERIAL_ACQUIRE_RESPONSIBILITY = (
    "preserve one exact material result supplied at one operator boundary"
)
OPERATOR_MATERIAL_ACQUIRE_BOOK_CLAUSE = "01.Source.G"
EVENT_KIND_RESPONSIBILITIES = {
    OPERATOR_MATERIAL_ACQUIRE_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND: (
        "01.Source.G"
    ),
    OPERATOR_MATERIAL_ACQUIRE_ACT_EVIDENCE_KIND: "02.Acts.A",
    OPERATOR_MATERIAL_ACQUIRE_RECORDED_KIND: "01.Source.G",
}


class OperatorMaterialAcquireError(ValueError):
    """One operator-material boundary occurrence is not exact."""


def _require_identity(value: Any, message: str) -> str:
    if type(value) is not str or not value:
        raise OperatorMaterialAcquireError(message)
    return value


def _source_standing_reference(
    ledger: EventLedger,
    *,
    locality_identity: str,
    addressed_representation_event_identity: str,
    locality_standing: dict[str, Any],
) -> dict[str, str]:
    _require_identity(
        locality_identity,
        "operator material acquire requires one exact Locality",
    )
    _require_identity(
        addressed_representation_event_identity,
        "operator material acquire requires one addressed Representation",
    )
    if type(locality_standing) is not dict:
        raise OperatorMaterialAcquireError(
            "operator material acquire requires exact Locality Standing"
        )
    if locality_standing.get("locality_identity") != locality_identity:
        raise OperatorMaterialAcquireError(
            "operator material acquire crossed its Locality Standing"
        )
    standing_boundary = locality_standing.get("as_of_event_identity")
    _require_identity(
        standing_boundary,
        "operator material acquire requires one exact Standing boundary",
    )
    try:
        representation = read_operator_representation(
            ledger, addressed_representation_event_identity
        )
    except ValueError as error:
        raise OperatorMaterialAcquireError(
            "operator material acquire requires one intact addressed Representation"
        ) from error
    if representation["locality_identity"] != locality_identity:
        raise OperatorMaterialAcquireError(
            "operator material acquire crossed its addressed Representation Locality"
        )
    ordered_identities = (
        (addressed_representation_event_identity,)
        if addressed_representation_event_identity == standing_boundary
        else (addressed_representation_event_identity, standing_boundary)
    )
    try:
        boundary_event = ledger.occurrences_in_append_order(
            ordered_identities,
            locality_identity=locality_identity,
        )[-1]
    except ValueError as error:
        raise OperatorMaterialAcquireError(
            "operator material acquire requires its exact current Standing boundary"
        ) from error
    if ledger.integrity_of(boundary_event.identity) == CORRUPTED:
        raise OperatorMaterialAcquireError(
            "operator material acquire requires its exact current Standing boundary"
        )
    return {
        "locality_identity": locality_identity,
        "locality_standing_as_of_event_identity": standing_boundary,
        "addressed_representation_event_identity": (
            addressed_representation_event_identity
        ),
    }


def _authority() -> dict[str, str]:
    return {
        "source": "active Book",
        "book_clause_identity": OPERATOR_MATERIAL_ACQUIRE_BOOK_CLAUSE,
        "standing": "bounded",
        "limit": "preservation of this exact boundary result only",
    }


def _scope(
    *,
    scope_identity: str,
    source_standing_reference: dict[str, str],
    result_boundary_identity: str,
) -> dict[str, str]:
    return {
        "scope_identity": scope_identity,
        **deepcopy(source_standing_reference),
        "result_boundary_identity": result_boundary_identity,
    }


def _assignment_material(
    *,
    assignment_identity: str,
    assignment_subject_identity: str,
    acquire_act_identity: str,
    act_occurrence_identity: str,
    scope_identity: str,
    result_boundary_identity: str,
    source_standing_reference: dict[str, str],
) -> dict[str, Any]:
    return {
        "assignment_identity": assignment_identity,
        "assignment_subject_identity": assignment_subject_identity,
        "book_clause_identity": OPERATOR_MATERIAL_ACQUIRE_BOOK_CLAUSE,
        "responsible_boundary": "this Seed",
        "responsibility": OPERATOR_MATERIAL_ACQUIRE_RESPONSIBILITY,
        "acquire_act_identity": acquire_act_identity,
        "act_occurrence_identity": act_occurrence_identity,
        "result_boundary_identity": result_boundary_identity,
        "source_standing_reference": deepcopy(source_standing_reference),
        "scope": _scope(
            scope_identity=scope_identity,
            source_standing_reference=source_standing_reference,
            result_boundary_identity=result_boundary_identity,
        ),
        "evidence_occurrence_reference": source_standing_reference[
            "addressed_representation_event_identity"
        ],
        "authority": _authority(),
        "standing": "assigned",
        "limits": [
            "this assignment is bounded to one exact boundary occurrence",
            (
                "preserved material establishes no represented relation or "
                "Authority for another Act"
            ),
        ],
        "unknowns": [
            "what exact material the operator boundary supplies remains Unknown"
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


def _act_evidence_material(assignment: Event) -> dict[str, Any]:
    material = assignment.material
    return {
        "acquire_act_identity": material["acquire_act_identity"],
        "act_occurrence_identity": material["act_occurrence_identity"],
        "act": OPERATOR_MATERIAL_ACQUIRE_ACT,
        "responsibility": OPERATOR_MATERIAL_ACQUIRE_RESPONSIBILITY,
        "responsible_boundary": "this Seed",
        "responsibility_assignment_reference": _assignment_reference(assignment),
        "source_standing_reference": deepcopy(
            material["source_standing_reference"]
        ),
        "scope": deepcopy(material["scope"]),
        "result_boundary_identity": material["result_boundary_identity"],
        "authority": _authority(),
        "evidence_scope": (
            "Evidence for this exact operator material boundary occurrence only"
        ),
    }


def _result_material(
    act_evidence: Event,
    *,
    boundary_material: OperatorBoundaryMaterial,
) -> dict[str, Any]:
    material = act_evidence.material
    return {
        "result_identity": material["result_boundary_identity"],
        "acquire_act_identity": material["acquire_act_identity"],
        "act_occurrence_identity": material["act_occurrence_identity"],
        "exact_act": OPERATOR_MATERIAL_ACQUIRE_ACT,
        "responsibility": OPERATOR_MATERIAL_ACQUIRE_RESPONSIBILITY,
        "responsible_boundary": "this Seed",
        "responsibility_assignment_reference": deepcopy(
            material["responsibility_assignment_reference"]
        ),
        "source_standing_reference": deepcopy(
            material["source_standing_reference"]
        ),
        "scope": deepcopy(material["scope"]),
        "source_boundary": boundary_material.material_boundary,
        "known_loss": list(boundary_material.known_loss),
        "authority": _authority(),
        "standing": "preserved",
        "limits": [
            "exact material establishes no represented relation",
            "this result establishes no other boundary occurrence",
        ],
        "unknowns": list(MATERIAL_RESULT_UNKNOWNS),
    }


def _recorded_result_material(
    result_material: dict[str, Any],
    *,
    responsible_act_evidence_identity: str,
    evidence_of_yield_relation_identity: str,
) -> dict[str, Any]:
    return {
        "result_identity": result_material["result_identity"],
        "acquire_act_identity": result_material["acquire_act_identity"],
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
        "known_loss": result_material["known_loss"],
        "authority": result_material["authority"],
        "standing": result_material["standing"],
        "limits": result_material["limits"],
        "unknowns": result_material["unknowns"],
        "responsible_act_evidence_identity": responsible_act_evidence_identity,
        "evidence_of_yield_relation_identity": evidence_of_yield_relation_identity,
    }


def record_operator_material_acquire_responsibility_assignment(
    ledger: EventLedger,
    *,
    locality_identity: str,
    addressed_representation_event_identity: str,
    locality_standing: dict[str, Any],
) -> Event:
    """Assign Responsibility for exactly one later boundary occurrence."""

    if not isinstance(ledger, EventLedger):
        raise TypeError("operator material acquire requires one EventLedger")
    source_reference = _source_standing_reference(
        ledger,
        locality_identity=locality_identity,
        addressed_representation_event_identity=(
            addressed_representation_event_identity
        ),
        locality_standing=locality_standing,
    )
    assignment_identity = new_identity("operator_material_acquire_assignment")
    assignment_subject_identity = new_identity(
        "operator_material_acquire_assignment_subject"
    )
    acquire_act_identity = new_identity("operator_material_acquire_act")
    act_occurrence_identity = new_identity(
        "operator_material_acquire_act_occurrence"
    )
    scope_identity = new_identity("operator_material_acquire_scope")
    result_boundary_identity = new_identity(
        "operator_material_acquire_result_boundary"
    )
    return ledger.append(
        OPERATOR_MATERIAL_ACQUIRE_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND,
        _assignment_material(
            assignment_identity=assignment_identity,
            assignment_subject_identity=assignment_subject_identity,
            acquire_act_identity=acquire_act_identity,
            act_occurrence_identity=act_occurrence_identity,
            scope_identity=scope_identity,
            result_boundary_identity=result_boundary_identity,
            source_standing_reference=source_reference,
        ),
        locality_identity=locality_identity,
    )


def get_operator_material_acquire_responsibility_assignment(
    ledger: EventLedger, assignment_event_identity: str
) -> Event:
    """Read one intact Book-backed assignment occurrence."""

    _require_identity(
        assignment_event_identity,
        "operator material acquire requires one assignment occurrence",
    )
    assignment = ledger.get(assignment_event_identity)
    if (
        assignment is None
        or assignment.kind
        != OPERATOR_MATERIAL_ACQUIRE_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND
        or type(assignment.locality_identity) is not str
        or not assignment.locality_identity
        or assignment.exact_material is not None
        or ledger.integrity_of(assignment.identity) == CORRUPTED
    ):
        raise OperatorMaterialAcquireError(
            "operator material acquire assignment is absent or corrupted"
        )
    material = assignment.material
    source_reference = material.get("source_standing_reference")
    scope = material.get("scope")
    identities = (
        material.get("assignment_identity"),
        material.get("assignment_subject_identity"),
        material.get("acquire_act_identity"),
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
        raise OperatorMaterialAcquireError(
            "operator material acquire assignment coordinates are not exact"
        )
    expected_source = _source_standing_reference(
        ledger,
        locality_identity=assignment.locality_identity,
        addressed_representation_event_identity=source_reference.get(
            "addressed_representation_event_identity"
        ),
        locality_standing={
            "locality_identity": assignment.locality_identity,
            "as_of_event_identity": source_reference.get(
                "locality_standing_as_of_event_identity"
            ),
        },
    )
    expected = _assignment_material(
        assignment_identity=identities[0],
        assignment_subject_identity=identities[1],
        acquire_act_identity=identities[2],
        act_occurrence_identity=identities[3],
        scope_identity=identities[4],
        result_boundary_identity=identities[5],
        source_standing_reference=expected_source,
    )
    if material != expected:
        raise OperatorMaterialAcquireError(
            "operator material acquire assignment is not exact"
        )
    return assignment


def record_operator_material_acquire_responsible_act_evidence(
    ledger: EventLedger,
    *,
    responsibility_assignment_event_identity: str,
    responsibility_assignment_standing: dict[str, Any],
) -> Event:
    """Record the distinct Act occurrence from its carried assignment."""

    assignment = get_operator_material_acquire_responsibility_assignment(
        ledger, responsibility_assignment_event_identity
    )
    if type(responsibility_assignment_standing) is not dict:
        raise OperatorMaterialAcquireError(
            "operator material acquire Act requires assignment Standing"
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
        raise OperatorMaterialAcquireError(
            "operator material acquire Act requires its exact carried assignment"
        )
    return ledger.append(
        OPERATOR_MATERIAL_ACQUIRE_ACT_EVIDENCE_KIND,
        _act_evidence_material(assignment),
        locality_identity=assignment.locality_identity,
    )


def get_operator_material_acquire_act_evidence(
    ledger: EventLedger, act_evidence_event_identity: str
) -> Event:
    """Read one exact acquire Act Evidence occurrence."""

    _require_identity(
        act_evidence_event_identity,
        "operator material acquire result requires one Act Evidence occurrence",
    )
    act_evidence = ledger.get(act_evidence_event_identity)
    if (
        act_evidence is None
        or act_evidence.kind != OPERATOR_MATERIAL_ACQUIRE_ACT_EVIDENCE_KIND
        or type(act_evidence.locality_identity) is not str
        or not act_evidence.locality_identity
        or act_evidence.exact_material is not None
        or ledger.integrity_of(act_evidence.identity) == CORRUPTED
    ):
        raise OperatorMaterialAcquireError(
            "operator material acquire requires intact Act Evidence"
        )
    reference = act_evidence.material.get("responsibility_assignment_reference")
    if type(reference) is not dict:
        raise OperatorMaterialAcquireError(
            "operator material acquire Act carries no assignment"
        )
    assignment = get_operator_material_acquire_responsibility_assignment(
        ledger, reference.get("recorded_occurrence_identity")
    )
    if (
        assignment.locality_identity != act_evidence.locality_identity
        or reference != _assignment_reference(assignment)
        or act_evidence.material != _act_evidence_material(assignment)
    ):
        raise OperatorMaterialAcquireError(
            "operator material acquire Act Evidence is not exact"
        )
    try:
        ledger.occurrences_in_append_order(
            (assignment.identity, act_evidence.identity),
            locality_identity=act_evidence.locality_identity,
        )
    except ValueError as error:
        raise OperatorMaterialAcquireError(
            "operator material acquire Act requires its prior assignment"
        ) from error
    return act_evidence


def record_operator_material_acquire_result(
    ledger: EventLedger,
    *,
    responsible_act_evidence_event_identity: str,
    boundary_material: OperatorBoundaryMaterial,
) -> Event:
    """Record one exact nonempty boundary result and its Yield."""

    if not isinstance(boundary_material, OperatorBoundaryMaterial):
        raise TypeError("operator material acquire requires exact boundary material")
    if boundary_material.eof:
        raise OperatorMaterialAcquireError(
            "an empty operator boundary establishes no acquire result"
        )
    act_evidence = get_operator_material_acquire_act_evidence(
        ledger, responsible_act_evidence_event_identity
    )
    act_occurrence_identity = act_evidence.material["act_occurrence_identity"]
    for prior_yield in ledger.iter_locality_kind(
        act_evidence.locality_identity, RECORDED_EVIDENCE_OF_YIELD_RELATION_KIND
    ):
        if (
            prior_yield.material.get("responsible_act_evidence_identity")
            == act_evidence.identity
            or prior_yield.material.get("dimensions", {}).get(
                "act_occurrence_identity"
            )
            == act_occurrence_identity
        ):
            raise OperatorMaterialAcquireError(
                "operator material acquire Act already carries a Yield"
            )
    result_material = _result_material(
        act_evidence, boundary_material=boundary_material
    )
    evidence_of_yield_relation = _record_evidence_of_yield_relation(
        ledger,
        locality_identity=act_evidence.locality_identity,
        exact_act=OPERATOR_MATERIAL_ACQUIRE_ACT,
        act_occurrence_identity=act_occurrence_identity,
        responsible_act_evidence_identity=act_evidence.identity,
        result_kind=OPERATOR_MATERIAL_ACQUIRE_RESULT_KIND,
        result_identity=result_material["result_identity"],
        result_content=result_material,
        responsibility=OPERATOR_MATERIAL_ACQUIRE_RESPONSIBILITY,
        live_boundary="operator_material_acquire",
        responsible_boundary="this Seed",
        result_exact_material=boundary_material.exact_bytes,
    )
    return ledger.append(
        OPERATOR_MATERIAL_ACQUIRE_RECORDED_KIND,
        _recorded_result_material(
            result_material,
            responsible_act_evidence_identity=act_evidence.identity,
            evidence_of_yield_relation_identity=evidence_of_yield_relation.identity,
        ),
        exact_material=boundary_material.exact_bytes,
        locality_identity=act_evidence.locality_identity,
    )


def get_recorded_operator_material_acquire(
    ledger: EventLedger, result_event_identity: str
) -> dict[str, Any]:
    """Read one raw boundary result through its exact Act and Yield."""

    _require_identity(
        result_event_identity,
        "operator material acquire read requires one result occurrence",
    )
    result = ledger.get(result_event_identity)
    if (
        result is None
        or result.kind != OPERATOR_MATERIAL_ACQUIRE_RECORDED_KIND
        or type(result.locality_identity) is not str
        or not result.locality_identity
        or type(result.exact_material) is not bytes
        or not result.exact_material
        or ledger.integrity_of(result.identity) == CORRUPTED
    ):
        raise OperatorMaterialAcquireError(
            "operator material acquire result is absent or corrupted"
        )
    act_evidence = get_operator_material_acquire_act_evidence(
        ledger, result.material.get("responsible_act_evidence_identity")
    )
    boundary = OperatorBoundaryMaterial(
        exact_bytes=result.exact_material,
        eof=False,
        material_boundary=result.material.get("source_boundary"),
        known_loss=tuple(result.material.get("known_loss", ())),
    )
    expected_result = _result_material(act_evidence, boundary_material=boundary)
    expected = _recorded_result_material(
        expected_result,
        responsible_act_evidence_identity=act_evidence.identity,
        evidence_of_yield_relation_identity=result.material.get("evidence_of_yield_relation_identity"),
    )
    if (
        result.locality_identity != act_evidence.locality_identity
        or result.material != expected
    ):
        raise OperatorMaterialAcquireError(
            "operator material acquire result coordinates are not exact"
        )
    requirements = read_requirements_of_yield_relation(
        ledger,
        recorded_result_event_identity=result.identity,
        evidence_of_yield_relation_event_identity=result.material["evidence_of_yield_relation_identity"],
        responsible_act_evidence_event_identity=act_evidence.identity,
    )
    if not all(requirements.values()):
        raise OperatorMaterialAcquireError(
            "operator material acquire carries no exact Evidence of Yield relation"
        )
    return deepcopy(result.material)
