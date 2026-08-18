"""Preserve one exact recorded Standing-boundary result at one new Locality."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from seed_runtime.event import Event
from seed_runtime.events import CORRUPTED, EventLedger
from seed_runtime.identities import new_identity
from seed_runtime.operator_checkpoint import get_recorded_standing_boundary_reference
from seed_runtime.evidence_of_yield_relation import (
    RECORDED_EVIDENCE_OF_YIELD_RELATION_KIND,
    _record_evidence_of_yield_relation,
    read_requirements_of_yield_relation,
)


RECORDED_STANDING_BOUNDARY_LOCALITY_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND = (
    "operator.recorded_standing_boundary_locality_responsibility_assignment_recorded"
)
RECORDED_STANDING_BOUNDARY_LOCALITY_ACT_EVIDENCE_KIND = (
    "operator.recorded_standing_boundary_locality_act_evidenced"
)
RECORDED_STANDING_BOUNDARY_LOCALITY_RECORDED_KIND = (
    "operator.recorded_standing_boundary_locality_recorded"
)
RECORDED_STANDING_BOUNDARY_LOCALITY_RESULT_KIND = (
    "recorded Standing boundary Locality relation result"
)
RECORDED_STANDING_BOUNDARY_LOCALITY_ACT = (
    "Preserve one exact recorded Standing boundary result at one new Locality"
)
RECORDED_STANDING_BOUNDARY_LOCALITY_RESPONSIBILITY = (
    "preserve one direct Locality relation from one exact recorded Standing "
    "boundary result at one new Locality"
)
RECORDED_STANDING_BOUNDARY_LOCALITY_BOOK_CLAUSE = "06.Locality.C"
EVENT_KIND_RESPONSIBILITIES = {
    RECORDED_STANDING_BOUNDARY_LOCALITY_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND: (
        "06.Locality.C"
    ),
    RECORDED_STANDING_BOUNDARY_LOCALITY_ACT_EVIDENCE_KIND: "02.Acts.A",
    RECORDED_STANDING_BOUNDARY_LOCALITY_RECORDED_KIND: "06.Locality.A",
}


class RecordedStandingBoundaryLocalityError(ValueError):
    """One exact recorded-boundary Locality relation is not established."""


def _require_identity(value: Any, message: str) -> str:
    if type(value) is not str or not value:
        raise RecordedStandingBoundaryLocalityError(message)
    return value


def _anchor_reference(ledger: EventLedger, anchor_event_identity: str) -> dict[str, str]:
    recorded = get_recorded_standing_boundary_reference(
        ledger, anchor_event_identity
    )
    return {
        "recorded_occurrence_identity": anchor_event_identity,
        "result_identity": recorded["result_identity"],
    }


def _resolve_one_carried_anchor(
    ledger: EventLedger,
    *,
    source_locality_standing: dict[str, Any],
) -> dict[str, str]:
    if type(source_locality_standing) is not dict:
        raise RecordedStandingBoundaryLocalityError(
            "recorded Standing boundary Locality requires exact source Standing"
        )
    source_locality = _require_identity(
        source_locality_standing.get("locality_identity"),
        "recorded Standing boundary Locality requires one source Locality",
    )
    anchors = source_locality_standing.get(
        "recorded_standing_boundary_references"
    )
    relations = source_locality_standing.get(
        "recorded_standing_boundary_locality_relations"
    )
    if type(anchors) is not dict or type(relations) is not dict:
        raise RecordedStandingBoundaryLocalityError(
            "recorded Standing boundary Locality requires exact carried identities"
        )
    candidates = [
        *(('anchor', identity) for identity, value in anchors.items() if value is None),
        *(('relation', identity) for identity, value in relations.items() if value is None),
    ]
    if len(candidates) != len(anchors) + len(relations):
        raise RecordedStandingBoundaryLocalityError(
            "recorded Standing boundary Locality carriers are not exact"
        )
    if len(candidates) != 1:
        raise RecordedStandingBoundaryLocalityError(
            "recorded Standing boundary Locality requires exactly one carried reference"
        )
    kind, event_identity = candidates[0]
    event = ledger.get(event_identity)
    if event is None or event.locality_identity != source_locality:
        raise RecordedStandingBoundaryLocalityError(
            "recorded Standing boundary Locality names a different carried occurrence"
        )
    if kind == "anchor":
        return _anchor_reference(ledger, event_identity)
    relation = get_recorded_standing_boundary_locality(
        ledger, event_identity
    )
    return deepcopy(relation["standing_boundary_reference"])


def _authority() -> dict[str, str]:
    return {
        "source": "active Book",
        "book_clause_identity": RECORDED_STANDING_BOUNDARY_LOCALITY_BOOK_CLAUSE,
        "standing": "bounded",
        "limit": "bounded to this exact direct Locality relation",
    }


def _assignment_material(
    *,
    assignment_identity: str,
    assignment_subject_identity: str,
    locality_act_identity: str,
    act_occurrence_identity: str,
    locality_relation_occurrence_identity: str,
    result_identity: str,
    scope_identity: str,
    standing_boundary_reference: dict[str, str],
    destination_locality_identity: str,
) -> dict[str, Any]:
    return {
        "assignment_identity": assignment_identity,
        "assignment_subject_identity": assignment_subject_identity,
        "book_clause_identity": RECORDED_STANDING_BOUNDARY_LOCALITY_BOOK_CLAUSE,
        "responsibility": RECORDED_STANDING_BOUNDARY_LOCALITY_RESPONSIBILITY,
        "responsible_boundary": "this Seed",
        "locality_act_identity": locality_act_identity,
        "act_occurrence_identity": act_occurrence_identity,
        "locality_relation_occurrence_identity": locality_relation_occurrence_identity,
        "result_identity": result_identity,
        "standing_boundary_reference": deepcopy(standing_boundary_reference),
        "destination_locality_identity": destination_locality_identity,
        "scope": {
            "scope_identity": scope_identity,
            "standing_boundary_reference": deepcopy(standing_boundary_reference),
            "destination_locality_identity": destination_locality_identity,
        },
        "evidence_occurrence_reference": standing_boundary_reference[
            "recorded_occurrence_identity"
        ],
        "authority": _authority(),
        "limits": [
            "this assignment is bounded to one direct Locality relation",
            "the relation carries no addressed Standing",
        ],
        "unknown": [
            "Applicability of the recorded boundary to another Act: Unknown"
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
        "result_identity": assignment.material["result_identity"],
    }


def _participation(
    standing_boundary_reference: dict[str, str], act_occurrence_identity: str
) -> dict[str, Any]:
    return {
        "subject_reference": deepcopy(standing_boundary_reference),
        "role": "exact recorded Standing boundary result",
        "act_occurrence_identity": act_occurrence_identity,
    }


def _act_material(assignment: Event) -> dict[str, Any]:
    material = assignment.material
    return {
        "locality_act_identity": material["locality_act_identity"],
        "act_occurrence_identity": material["act_occurrence_identity"],
        "locality_relation_occurrence_identity": material[
            "locality_relation_occurrence_identity"
        ],
        "act": RECORDED_STANDING_BOUNDARY_LOCALITY_ACT,
        "responsibility": RECORDED_STANDING_BOUNDARY_LOCALITY_RESPONSIBILITY,
        "responsible_boundary": "this Seed",
        "responsibility_assignment_reference": _assignment_reference(assignment),
        "standing_boundary_reference": deepcopy(
            material["standing_boundary_reference"]
        ),
        "destination_locality_identity": assignment.locality_identity,
        "scope": deepcopy(material["scope"]),
        "result_identity": material["result_identity"],
        "participation": _participation(
            material["standing_boundary_reference"],
            material["act_occurrence_identity"],
        ),
        "authority": _authority(),
        "evidence_scope": "Evidence bounded to this exact direct Locality relation",
    }


def _result_material(act: Event) -> dict[str, Any]:
    material = act.material
    return {
        "result_identity": material["result_identity"],
        "locality_act_identity": material["locality_act_identity"],
        "act_occurrence_identity": material["act_occurrence_identity"],
        "locality_relation_occurrence_identity": material[
            "locality_relation_occurrence_identity"
        ],
        "exact_act": RECORDED_STANDING_BOUNDARY_LOCALITY_ACT,
        "responsibility": RECORDED_STANDING_BOUNDARY_LOCALITY_RESPONSIBILITY,
        "responsible_boundary": "this Seed",
        "responsibility_assignment_reference": deepcopy(
            material["responsibility_assignment_reference"]
        ),
        "standing_boundary_reference": deepcopy(
            material["standing_boundary_reference"]
        ),
        "destination_locality_identity": act.locality_identity,
        "scope": deepcopy(material["scope"]),
        "participation": deepcopy(material["participation"]),
        "locality_relation": {
            "first_subject": deepcopy(material["standing_boundary_reference"]),
            "second_subject": act.locality_identity,
            "relation_occurrence_identity": material[
                "locality_relation_occurrence_identity"
            ],
        },
        "authority": _authority(),
        "standing": "preserved",
        "limits": [
            "this direct Locality relation carries no other Locality relation",
            "the relation carries no addressed Standing",
            "the relation establishes no Compare",
        ],
        "unknown": [
            "Applicability of the recorded boundary to another Act: Unknown"
        ],
    }


def _recorded_result_material(
    result_material: dict[str, Any],
    *, responsible_act_evidence_identity: str,
    evidence_of_yield_relation_identity: str,
) -> dict[str, Any]:
    return {
        "result_identity": result_material["result_identity"],
        "locality_act_identity": result_material["locality_act_identity"],
        "act_occurrence_identity": result_material["act_occurrence_identity"],
        "locality_relation_occurrence_identity": result_material[
            "locality_relation_occurrence_identity"
        ],
        "exact_act": result_material["exact_act"],
        "responsibility": result_material["responsibility"],
        "responsible_boundary": result_material["responsible_boundary"],
        "responsibility_assignment_reference": deepcopy(
            result_material["responsibility_assignment_reference"]
        ),
        "standing_boundary_reference": deepcopy(
            result_material["standing_boundary_reference"]
        ),
        "destination_locality_identity": result_material[
            "destination_locality_identity"
        ],
        "scope": deepcopy(result_material["scope"]),
        "participation": deepcopy(result_material["participation"]),
        "locality_relation": deepcopy(result_material["locality_relation"]),
        "authority": deepcopy(result_material["authority"]),
        "standing": result_material["standing"],
        "limits": list(result_material["limits"]),
        "unknown": list(result_material["unknown"]),
        "responsible_act_evidence_identity": responsible_act_evidence_identity,
        "evidence_of_yield_relation_identity": evidence_of_yield_relation_identity,
    }


def record_recorded_standing_boundary_locality_responsibility_assignment(
    ledger: EventLedger,
    *,
    source_locality_standing: dict[str, Any],
) -> Event:
    """Assign one direct relation from exactly one carried recorded result."""

    if not isinstance(ledger, EventLedger):
        raise TypeError("recorded Standing boundary Locality requires one EventLedger")
    anchor = _resolve_one_carried_anchor(
        ledger, source_locality_standing=source_locality_standing
    )
    destination = new_identity("recorded_standing_boundary_locality")
    if ledger.has_locality(destination):
        raise RecordedStandingBoundaryLocalityError(
            "recorded Standing boundary Locality requires one fresh Locality"
        )
    identities = {
        "assignment_identity": new_identity(
            "recorded_standing_boundary_locality_assignment"
        ),
        "assignment_subject_identity": new_identity(
            "recorded_standing_boundary_locality_assignment_subject"
        ),
        "locality_act_identity": new_identity(
            "recorded_standing_boundary_locality_act"
        ),
        "act_occurrence_identity": new_identity(
            "recorded_standing_boundary_locality_act_occurrence"
        ),
        "locality_relation_occurrence_identity": new_identity(
            "recorded_standing_boundary_locality_relation_occurrence"
        ),
        "result_identity": new_identity(
            "recorded_standing_boundary_locality_result"
        ),
        "scope_identity": new_identity(
            "recorded_standing_boundary_locality_scope"
        ),
    }
    return ledger.append(
        RECORDED_STANDING_BOUNDARY_LOCALITY_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND,
        _assignment_material(
            standing_boundary_reference=anchor,
            destination_locality_identity=destination,
            **identities,
        ),
        locality_identity=destination,
    )


def get_recorded_standing_boundary_locality_responsibility_assignment(
    ledger: EventLedger, event_identity: str
) -> Event:
    _require_identity(event_identity, "recorded boundary relation requires assignment")
    event = ledger.get(event_identity)
    if (
        event is None
        or event.kind
        != RECORDED_STANDING_BOUNDARY_LOCALITY_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND
        or type(event.locality_identity) is not str
        or event.exact_material is not None
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise RecordedStandingBoundaryLocalityError(
            "recorded boundary relation assignment is absent or corrupted"
        )
    material = event.material
    anchor = material.get("standing_boundary_reference")
    scope = material.get("scope")
    identities = (
        material.get("assignment_identity"),
        material.get("assignment_subject_identity"),
        material.get("locality_act_identity"),
        material.get("act_occurrence_identity"),
        material.get("locality_relation_occurrence_identity"),
        material.get("result_identity"),
        scope.get("scope_identity") if type(scope) is dict else None,
    )
    if (
        type(anchor) is not dict
        or any(type(value) is not str or not value for value in identities)
        or len(set(identities)) != len(identities)
    ):
        raise RecordedStandingBoundaryLocalityError(
            "recorded boundary relation assignment identities are not exact"
        )
    expected_anchor = _anchor_reference(
        ledger, anchor.get("recorded_occurrence_identity")
    )
    expected = _assignment_material(
        assignment_identity=identities[0],
        assignment_subject_identity=identities[1],
        locality_act_identity=identities[2],
        act_occurrence_identity=identities[3],
        locality_relation_occurrence_identity=identities[4],
        result_identity=identities[5],
        scope_identity=identities[6],
        standing_boundary_reference=expected_anchor,
        destination_locality_identity=event.locality_identity,
    )
    if material != expected:
        raise RecordedStandingBoundaryLocalityError(
            "recorded boundary relation assignment is not exact"
        )
    return event


def record_recorded_standing_boundary_locality_responsible_act_evidence(
    ledger: EventLedger,
    *, responsibility_assignment_event_identity: str,
    responsibility_assignment_standing: dict[str, Any],
) -> Event:
    assignment = get_recorded_standing_boundary_locality_responsibility_assignment(
        ledger, responsibility_assignment_event_identity
    )
    if type(responsibility_assignment_standing) is not dict:
        raise RecordedStandingBoundaryLocalityError(
            "recorded boundary relation Act requires assignment Standing"
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
        raise RecordedStandingBoundaryLocalityError(
            "recorded boundary relation Act requires its carried assignment"
        )
    return ledger.append(
        RECORDED_STANDING_BOUNDARY_LOCALITY_ACT_EVIDENCE_KIND,
        _act_material(assignment),
        locality_identity=assignment.locality_identity,
    )


def get_recorded_standing_boundary_locality_act_evidence(
    ledger: EventLedger, event_identity: str
) -> Event:
    _require_identity(event_identity, "recorded boundary relation requires Act Evidence")
    event = ledger.get(event_identity)
    if (
        event is None
        or event.kind != RECORDED_STANDING_BOUNDARY_LOCALITY_ACT_EVIDENCE_KIND
        or event.exact_material is not None
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise RecordedStandingBoundaryLocalityError(
            "recorded boundary relation Act Evidence is absent or corrupted"
        )
    reference = event.material.get("responsibility_assignment_reference")
    if type(reference) is not dict:
        raise RecordedStandingBoundaryLocalityError(
            "recorded boundary relation Act carries no assignment"
        )
    assignment = get_recorded_standing_boundary_locality_responsibility_assignment(
        ledger, reference.get("recorded_occurrence_identity")
    )
    if (
        assignment.locality_identity != event.locality_identity
        or reference != _assignment_reference(assignment)
        or event.material != _act_material(assignment)
    ):
        raise RecordedStandingBoundaryLocalityError(
            "recorded boundary relation Act Evidence is not exact"
        )
    try:
        ledger.occurrences_in_append_order(
            (assignment.identity, event.identity),
            locality_identity=event.locality_identity,
        )
    except ValueError as error:
        raise RecordedStandingBoundaryLocalityError(
            "recorded boundary relation Act requires its prior assignment"
        ) from error
    return event


def record_recorded_standing_boundary_locality_result(
    ledger: EventLedger,
    *, responsible_act_evidence_event_identity: str,
) -> Event:
    act = get_recorded_standing_boundary_locality_act_evidence(
        ledger, responsible_act_evidence_event_identity
    )
    for evidence in ledger.iter_locality_kind(act.locality_identity, RECORDED_EVIDENCE_OF_YIELD_RELATION_KIND):
        if evidence.material.get("responsible_act_evidence_identity") == act.identity:
            raise RecordedStandingBoundaryLocalityError(
                "recorded boundary relation Act already carries a Yield"
            )
    result_material = _result_material(act)
    evidence = _record_evidence_of_yield_relation(
        ledger,
        locality_identity=act.locality_identity,
        exact_act=RECORDED_STANDING_BOUNDARY_LOCALITY_ACT,
        act_occurrence_identity=act.material["act_occurrence_identity"],
        responsible_act_evidence_identity=act.identity,
        result_kind=RECORDED_STANDING_BOUNDARY_LOCALITY_RESULT_KIND,
        result_identity=result_material["result_identity"],
        result_content=result_material,
        responsibility=RECORDED_STANDING_BOUNDARY_LOCALITY_RESPONSIBILITY,
        occurrence_boundary="recorded_standing_boundary_locality_relation",
        responsible_boundary="this Seed",
    )
    return ledger.append(
        RECORDED_STANDING_BOUNDARY_LOCALITY_RECORDED_KIND,
        _recorded_result_material(
            result_material,
            responsible_act_evidence_identity=act.identity,
            evidence_of_yield_relation_identity=evidence.identity,
        ),
        locality_identity=act.locality_identity,
    )


def get_recorded_standing_boundary_locality(
    ledger: EventLedger, event_identity: str
) -> dict[str, Any]:
    _require_identity(event_identity, "recorded boundary relation requires result")
    event = ledger.get(event_identity)
    if (
        event is None
        or event.kind != RECORDED_STANDING_BOUNDARY_LOCALITY_RECORDED_KIND
        or event.exact_material is not None
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise RecordedStandingBoundaryLocalityError(
            "recorded boundary relation result is absent or corrupted"
        )
    act = get_recorded_standing_boundary_locality_act_evidence(
        ledger, event.material.get("responsible_act_evidence_identity")
    )
    expected_result = _result_material(act)
    expected = _recorded_result_material(
        expected_result,
        responsible_act_evidence_identity=act.identity,
        evidence_of_yield_relation_identity=event.material.get("evidence_of_yield_relation_identity"),
    )
    if event.locality_identity != act.locality_identity or event.material != expected:
        raise RecordedStandingBoundaryLocalityError(
            "recorded boundary relation result coordinates are not exact"
        )
    requirements = read_requirements_of_yield_relation(
        ledger,
        recorded_result_event_identity=event.identity,
        evidence_of_yield_relation_event_identity=event.material["evidence_of_yield_relation_identity"],
        responsible_act_evidence_event_identity=act.identity,
    )
    if not all(requirements.values()):
        raise RecordedStandingBoundaryLocalityError(
            "recorded boundary relation result carries no exact Yield"
        )
    return deepcopy(event.material)
