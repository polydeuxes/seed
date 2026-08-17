"""Continue one exact prior Locality Standing boundary at another Locality.

This boundary establishes one direct Locality relation and bounded
availability only.  It does not copy the prior Locality's occurrences or
Standing accumulators, make any carried subject applicable to another Act,
establish priority, or follow another continuation transitively.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from seed_runtime.event import Event
from seed_runtime.events import CORRUPTED, EventLedger
from seed_runtime.identities import new_identity
from seed_runtime.operator_representation import read_operator_representation
from seed_runtime.evidence_of_yield_relation import (
    RECORDED_EVIDENCE_OF_YIELD_RELATION_KIND,
    _record_evidence_of_yield_relation,
    read_requirements_of_yield_relation,
)


STANDING_LOCALITY_CONTINUATION_ACT_EVIDENCE_KIND = (
    "operator.standing.locality_continuation_act_evidenced"
)
STANDING_LOCALITY_CONTINUATION_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND = (
    "operator.standing.locality_continuation_responsibility_assignment_recorded"
)
STANDING_LOCALITY_CONTINUATION_RECORDED_KIND = (
    "operator.standing.locality_continuation_recorded"
)
STANDING_LOCALITY_CONTINUATION_RESULT_KIND = (
    "Standing Locality continuation result"
)
STANDING_LOCALITY_CONTINUATION_ACT = "Standing Locality continuation"
STANDING_LOCALITY_CONTINUATION_RESPONSIBILITY = (
    "preserve availability of one exact prior Locality Standing boundary at one other "
    "exact Locality without revising its carried subjects"
)
STANDING_LOCALITY_CONTINUATION_INPUT_ROLE = (
    "exact prior Locality Standing boundary"
)
EVENT_KIND_RESPONSIBILITIES = {
    STANDING_LOCALITY_CONTINUATION_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND: (
        "06.Locality.B"
    ),
    STANDING_LOCALITY_CONTINUATION_ACT_EVIDENCE_KIND: "02.Acts.A",
    STANDING_LOCALITY_CONTINUATION_RECORDED_KIND: "06.Locality.A",
}
STANDING_LOCALITY_CONTINUATION_ASSIGNMENT_BOOK_CLAUSE = "06.Locality.B"


class StandingLocalityContinuationError(ValueError):
    """One exact Standing Locality continuation could not be established."""


def _require_identity(value: Any, message: str) -> str:
    if type(value) is not str or not value:
        raise StandingLocalityContinuationError(message)
    return value


def _source_standing_reference(
    ledger: EventLedger,
    *,
    source_locality_identity: str,
    addressed_representation_event_identity: str,
) -> dict[str, str | None]:
    """Resolve the exact source boundary represented by one intact occurrence."""

    _require_identity(
        source_locality_identity,
        "Standing Locality continuation requires one exact source Locality",
    )
    _require_identity(
        addressed_representation_event_identity,
        "Standing Locality continuation requires one addressed Representation",
    )
    try:
        representation = read_operator_representation(
            ledger, addressed_representation_event_identity
        )
    except ValueError as error:
        raise StandingLocalityContinuationError(
            "Standing Locality continuation requires one intact addressed Representation"
        ) from error
    if representation["locality_identity"] != source_locality_identity:
        raise StandingLocalityContinuationError(
            "Standing Locality continuation has a different source Locality"
        )

    representation_event = ledger.get(addressed_representation_event_identity)
    if (
        representation_event is None
        or "locality_standing_through_event_occurrence_identity"
        not in representation_event.material
    ):
        raise StandingLocalityContinuationError(
            "the addressed Representation carries no exact source boundary"
        )
    source_boundary = representation_event.material[
        "locality_standing_through_event_occurrence_identity"
    ]
    if source_boundary is not None and (
        type(source_boundary) is not str or not source_boundary
    ):
        raise StandingLocalityContinuationError(
            "Standing Locality continuation requires one exact source boundary"
        )
    occurrences = ledger.list_locality(source_locality_identity)
    positions = {event.identity: position for position, event in enumerate(occurrences)}
    representation_position = positions.get(addressed_representation_event_identity)
    if representation_position is None:
        raise StandingLocalityContinuationError(
            "the addressed Representation is absent from its source Locality"
        )
    if source_boundary is not None:
        boundary_event = ledger.get(source_boundary)
        boundary_position = positions.get(source_boundary)
        if (
            boundary_event is None
            or boundary_event.locality_identity != source_locality_identity
            or boundary_position is None
            or boundary_position >= representation_position
            or ledger.integrity_of(boundary_event.identity) == CORRUPTED
        ):
            raise StandingLocalityContinuationError(
                "Standing Locality continuation requires its exact prior source boundary"
            )
    return {
        "source_locality_identity": source_locality_identity,
        "source_standing_through_event_occurrence_identity": source_boundary,
        "addressed_representation_event_identity": (
            addressed_representation_event_identity
        ),
    }


def _participation(
    source_standing_reference: dict[str, str | None],
    *,
    act_occurrence_identity: str,
) -> dict[str, Any]:
    return {
        "subject_reference": deepcopy(source_standing_reference),
        "role": STANDING_LOCALITY_CONTINUATION_INPUT_ROLE,
        "act_occurrence_identity": act_occurrence_identity,
    }


def _assignment_material(
    *,
    assignment_identity: str,
    assignment_subject_identity: str,
    result_boundary_identity: str,
    source_standing_reference: dict[str, str | None],
    destination_locality_identity: str,
) -> dict[str, Any]:
    addressed_representation = source_standing_reference[
        "addressed_representation_event_identity"
    ]
    return {
        "assignment_identity": assignment_identity,
        "assignment_subject_identity": assignment_subject_identity,
        "book_clause_identity": (
            STANDING_LOCALITY_CONTINUATION_ASSIGNMENT_BOOK_CLAUSE
        ),
        "responsible_boundary": "this Seed",
        "responsibility": STANDING_LOCALITY_CONTINUATION_RESPONSIBILITY,
        "source_standing_reference": deepcopy(source_standing_reference),
        "destination_locality_identity": destination_locality_identity,
        "evidence_occurrence_reference": addressed_representation,
        "authority": {
            "source": "active Book",
            "book_clause_identity": (
                STANDING_LOCALITY_CONTINUATION_ASSIGNMENT_BOOK_CLAUSE
            ),
            "standing": "bounded",
        },
        "scope": {
            "source_locality_identity": source_standing_reference[
                "source_locality_identity"
            ],
            "source_standing_through_event_occurrence_identity": source_standing_reference[
                "source_standing_through_event_occurrence_identity"
            ],
            "addressed_representation_event_identity": addressed_representation,
            "destination_locality_identity": destination_locality_identity,
        },
        "result_boundary_identity": result_boundary_identity,
        "standing": "assigned",
        "limits": [
            "this assignment is bounded to one direct occurrence and result boundary",
            "availability at this Locality is not Applicability or Participation",
        ],
        "unknown": [
            "Applicability of every carried subject to another Act remains Unknown"
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
        "result_boundary_identity": assignment.material[
            "result_boundary_identity"
        ],
    }


def _act_evidence_material(
    *,
    continuation_act_identity: str,
    act_occurrence_identity: str,
    locality_relation_occurrence_identity: str,
    responsibility_assignment_reference: dict[str, str],
    source_standing_reference: dict[str, str | None],
    destination_locality_identity: str,
) -> dict[str, Any]:
    return {
        "continuation_act_identity": continuation_act_identity,
        "act_occurrence_identity": act_occurrence_identity,
        "locality_relation_occurrence_identity": (
            locality_relation_occurrence_identity
        ),
        "act": STANDING_LOCALITY_CONTINUATION_ACT,
        "responsibility": STANDING_LOCALITY_CONTINUATION_RESPONSIBILITY,
        "responsible_boundary": "this Seed",
        "responsibility_assignment_reference": dict(
            responsibility_assignment_reference
        ),
        "source_standing_reference": deepcopy(source_standing_reference),
        "destination_locality_identity": destination_locality_identity,
        "participation": _participation(
            source_standing_reference,
            act_occurrence_identity=act_occurrence_identity,
        ),
        "authority": "unestablished",
        "evidence_scope": (
            "Evidence bounded to this exact direct Standing Locality continuation "
            "occurrence"
        ),
    }


def _result_material(
    *,
    result_identity: str,
    continuation_act_identity: str,
    act_occurrence_identity: str,
    locality_relation_occurrence_identity: str,
    responsibility_assignment_reference: dict[str, str],
    source_standing_reference: dict[str, str | None],
    destination_locality_identity: str,
) -> dict[str, Any]:
    participation = _participation(
        source_standing_reference,
        act_occurrence_identity=act_occurrence_identity,
    )
    return {
        "result_identity": result_identity,
        "continuation_act_identity": continuation_act_identity,
        "act_occurrence_identity": act_occurrence_identity,
        "locality_relation_occurrence_identity": (
            locality_relation_occurrence_identity
        ),
        "exact_act": STANDING_LOCALITY_CONTINUATION_ACT,
        "responsibility": STANDING_LOCALITY_CONTINUATION_RESPONSIBILITY,
        "responsible_boundary": "this Seed",
        "responsibility_assignment_reference": dict(
            responsibility_assignment_reference
        ),
        "source_standing_reference": deepcopy(source_standing_reference),
        "destination_locality_identity": destination_locality_identity,
        "participation": participation,
        "locality_relation": {
            "first_subject": deepcopy(source_standing_reference),
            "second_subject": destination_locality_identity,
            "relation_occurrence_identity": locality_relation_occurrence_identity,
        },
        "standing": "preserved",
        "authority": "unestablished",
        "unknown": [
            "Applicability of every carried subject to another Act remains Unknown"
        ],
        "limits": [
            "availability at this exact Locality is not Applicability or Participation",
            "this direct Locality relation carries no other Locality relation",
        ],
    }


def _recorded_result_material(
    result_material: dict[str, Any],
    *,
    responsible_act_evidence_identity: str,
    evidence_of_yield_relation_identity: str,
) -> dict[str, Any]:
    """Carry every result coordinate at one literal durable address."""

    return {
        "result_identity": result_material["result_identity"],
        "continuation_act_identity": result_material[
            "continuation_act_identity"
        ],
        "act_occurrence_identity": result_material["act_occurrence_identity"],
        "locality_relation_occurrence_identity": result_material[
            "locality_relation_occurrence_identity"
        ],
        "exact_act": result_material["exact_act"],
        "responsibility": result_material["responsibility"],
        "responsible_boundary": result_material["responsible_boundary"],
        "responsibility_assignment_reference": result_material[
            "responsibility_assignment_reference"
        ],
        "source_standing_reference": result_material[
            "source_standing_reference"
        ],
        "destination_locality_identity": result_material[
            "destination_locality_identity"
        ],
        "participation": result_material["participation"],
        "locality_relation": result_material["locality_relation"],
        "standing": result_material["standing"],
        "authority": result_material["authority"],
        "unknown": result_material["unknown"],
        "limits": result_material["limits"],
        "responsible_act_evidence_identity": responsible_act_evidence_identity,
        "evidence_of_yield_relation_identity": evidence_of_yield_relation_identity,
    }


def record_standing_locality_continuation_responsibility_assignment(
    ledger: EventLedger,
    *,
    source_locality_identity: str,
    addressed_representation_event_identity: str,
) -> Event:
    """Record one bounded assignment at one fresh destination Locality."""

    if not isinstance(ledger, EventLedger):
        raise TypeError("Standing Locality continuation requires one EventLedger")
    source_reference = _source_standing_reference(
        ledger,
        source_locality_identity=source_locality_identity,
        addressed_representation_event_identity=(
            addressed_representation_event_identity
        ),
    )
    destination_locality_identity = new_identity("standing_locality")
    if ledger.has_locality(destination_locality_identity):
        raise StandingLocalityContinuationError(
            "Standing Locality continuation requires one fresh destination Locality"
        )
    assignment_identity = new_identity(
        "standing_locality_continuation_responsibility_assignment"
    )
    assignment_subject_identity = new_identity(
        "standing_locality_continuation_responsibility_subject"
    )
    result_boundary_identity = new_identity(
        "standing_locality_continuation_result_boundary"
    )
    return ledger.append(
        STANDING_LOCALITY_CONTINUATION_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND,
        _assignment_material(
            assignment_identity=assignment_identity,
            assignment_subject_identity=assignment_subject_identity,
            result_boundary_identity=result_boundary_identity,
            source_standing_reference=source_reference,
            destination_locality_identity=destination_locality_identity,
        ),
        locality_identity=destination_locality_identity,
    )


def record_standing_locality_continuation_responsible_act_evidence(
    ledger: EventLedger,
    *,
    responsibility_assignment_event_identity: str,
    responsibility_assignment_standing: dict[str, Any],
) -> Event:
    """Record one Act from one exact prior carried assignment Standing."""

    if not isinstance(ledger, EventLedger):
        raise TypeError("Standing Locality continuation requires one EventLedger")
    assignment = get_standing_locality_continuation_responsibility_assignment(
        ledger, responsibility_assignment_event_identity
    )
    if type(responsibility_assignment_standing) is not dict:
        raise StandingLocalityContinuationError(
            "Standing Locality continuation Act requires carried assignment Standing"
        )
    assignment_occurrences = responsibility_assignment_standing.get(
        "responsibility_assignment_occurrences"
    )
    if (
        responsibility_assignment_standing.get("locality_identity")
        != assignment.locality_identity
        or type(assignment_occurrences) is not dict
        or assignment.identity not in assignment_occurrences
        or assignment_occurrences[assignment.identity] is not None
    ):
        raise StandingLocalityContinuationError(
            "Standing Locality continuation Act requires its exact prior carried assignment"
        )
    standing_boundary = responsibility_assignment_standing.get(
        "through_event_occurrence_identity"
    )
    standing_boundary_event = ledger.get(standing_boundary)
    if (
        type(standing_boundary) is not str
        or not standing_boundary
        or standing_boundary_event is None
        or standing_boundary_event.locality_identity != assignment.locality_identity
    ):
        raise StandingLocalityContinuationError(
            "Standing Locality continuation Act requires one exact assignment Standing boundary"
        )
    if standing_boundary != assignment.identity:
        try:
            ledger.occurrences_in_append_order(
                (assignment.identity, standing_boundary),
                locality_identity=assignment.locality_identity,
            )
        except ValueError as error:
            raise StandingLocalityContinuationError(
                "Standing Locality continuation Act requires a prior assignment occurrence"
            ) from error

    source_reference = assignment.material["source_standing_reference"]
    destination_locality_identity = assignment.locality_identity
    continuation_act_identity = new_identity("standing_locality_continuation_act")
    act_occurrence_identity = new_identity(
        "standing_locality_continuation_occurrence"
    )
    locality_relation_occurrence_identity = new_identity(
        "standing_locality_continuation_relation_occurrence"
    )
    return ledger.append(
        STANDING_LOCALITY_CONTINUATION_ACT_EVIDENCE_KIND,
        _act_evidence_material(
            continuation_act_identity=continuation_act_identity,
            act_occurrence_identity=act_occurrence_identity,
            locality_relation_occurrence_identity=(
                locality_relation_occurrence_identity
            ),
            responsibility_assignment_reference=_assignment_reference(assignment),
            source_standing_reference=source_reference,
            destination_locality_identity=destination_locality_identity,
        ),
        locality_identity=destination_locality_identity,
    )


def _validated_act_evidence(
    ledger: EventLedger, responsible_act_evidence_event_identity: str
) -> Event:
    _require_identity(
        responsible_act_evidence_event_identity,
        "Standing Locality continuation result requires one exact Act Evidence identity",
    )
    act_evidence = ledger.get(responsible_act_evidence_event_identity)
    if (
        act_evidence is None
        or act_evidence.kind != STANDING_LOCALITY_CONTINUATION_ACT_EVIDENCE_KIND
        or type(act_evidence.locality_identity) is not str
        or not act_evidence.locality_identity
        or act_evidence.exact_material is not None
        or ledger.integrity_of(act_evidence.identity) == CORRUPTED
    ):
        raise StandingLocalityContinuationError(
            "Standing Locality continuation result requires intact Act Evidence"
        )
    material = act_evidence.material
    source_reference = material.get("source_standing_reference")
    if type(source_reference) is not dict:
        raise StandingLocalityContinuationError(
            "Standing Locality continuation Act Evidence carries no exact source boundary"
        )
    expected_reference = _source_standing_reference(
        ledger,
        source_locality_identity=source_reference.get("source_locality_identity"),
        addressed_representation_event_identity=source_reference.get(
            "addressed_representation_event_identity"
        ),
    )
    if source_reference != expected_reference:
        raise StandingLocalityContinuationError(
            "Standing Locality continuation Act Evidence carries another source boundary"
        )
    continuation_act_identity = material.get("continuation_act_identity")
    act_occurrence_identity = material.get("act_occurrence_identity")
    locality_relation_occurrence_identity = material.get(
        "locality_relation_occurrence_identity"
    )
    assignment_reference = material.get("responsibility_assignment_reference")
    if type(assignment_reference) is not dict:
        raise StandingLocalityContinuationError(
            "Standing Locality continuation Act Evidence carries no exact Responsibility assignment"
        )
    assignment = get_standing_locality_continuation_responsibility_assignment(
        ledger, assignment_reference.get("recorded_occurrence_identity")
    )
    if (
        type(continuation_act_identity) is not str
        or not continuation_act_identity
        or type(act_occurrence_identity) is not str
        or not act_occurrence_identity
        or continuation_act_identity == act_occurrence_identity
        or type(locality_relation_occurrence_identity) is not str
        or not locality_relation_occurrence_identity
        or locality_relation_occurrence_identity
        in {continuation_act_identity, act_occurrence_identity}
        or len(
            {
                assignment.identity,
                assignment.material["assignment_identity"],
                assignment.material["assignment_subject_identity"],
                assignment.material["result_boundary_identity"],
                continuation_act_identity,
                act_occurrence_identity,
                locality_relation_occurrence_identity,
            }
        )
        != 7
        or assignment_reference != _assignment_reference(assignment)
        or assignment.locality_identity != act_evidence.locality_identity
        or assignment.material["responsibility"]
        != STANDING_LOCALITY_CONTINUATION_RESPONSIBILITY
        or assignment.material["responsible_boundary"] != "this Seed"
        or assignment.material["source_standing_reference"] != expected_reference
        or assignment.material["destination_locality_identity"]
        != act_evidence.locality_identity
        or material.get("destination_locality_identity")
        != act_evidence.locality_identity
        or material
        != _act_evidence_material(
            continuation_act_identity=continuation_act_identity,
            act_occurrence_identity=act_occurrence_identity,
            locality_relation_occurrence_identity=(
                locality_relation_occurrence_identity
            ),
            responsibility_assignment_reference=assignment_reference,
            source_standing_reference=expected_reference,
            destination_locality_identity=act_evidence.locality_identity,
        )
    ):
        raise StandingLocalityContinuationError(
            "Standing Locality continuation Act Evidence is not exact"
        )
    return act_evidence


def record_standing_locality_continuation_result(
    ledger: EventLedger,
    *,
    responsible_act_evidence_event_identity: str,
) -> Event:
    """Record the Yield and direct Locality relation for one evidenced Act."""

    act_evidence = _validated_act_evidence(
        ledger, responsible_act_evidence_event_identity
    )
    material = act_evidence.material
    locality_identity = act_evidence.locality_identity
    act_occurrence_identity = material["act_occurrence_identity"]
    for prior_yield in ledger.iter_locality_kind(
        locality_identity, RECORDED_EVIDENCE_OF_YIELD_RELATION_KIND
    ):
        dimensions = prior_yield.material.get("dimensions")
        if (
            prior_yield.material.get("responsible_act_evidence_identity")
            == act_evidence.identity
            or (
                type(dimensions) is dict
                and dimensions.get("act_occurrence_identity")
                == act_occurrence_identity
            )
        ):
            raise StandingLocalityContinuationError(
                "the Standing Locality continuation Act already carries a Yield"
            )
    for prior_result in ledger.iter_locality_kind(
        locality_identity, STANDING_LOCALITY_CONTINUATION_RECORDED_KIND
    ):
        if (
            prior_result.material.get("responsible_act_evidence_identity")
            == act_evidence.identity
            or prior_result.material.get("act_occurrence_identity")
            == act_occurrence_identity
        ):
            raise StandingLocalityContinuationError(
                "the Standing Locality continuation Act already carries a result"
            )

    result_identity = material["responsibility_assignment_reference"][
        "result_boundary_identity"
    ]
    result_material = _result_material(
        result_identity=result_identity,
        continuation_act_identity=material["continuation_act_identity"],
        act_occurrence_identity=act_occurrence_identity,
        locality_relation_occurrence_identity=material[
            "locality_relation_occurrence_identity"
        ],
        responsibility_assignment_reference=material[
            "responsibility_assignment_reference"
        ],
        source_standing_reference=material["source_standing_reference"],
        destination_locality_identity=locality_identity,
    )
    evidence_of_yield_relation = _record_evidence_of_yield_relation(
        ledger,
        locality_identity=locality_identity,
        exact_act=STANDING_LOCALITY_CONTINUATION_ACT,
        act_occurrence_identity=act_occurrence_identity,
        responsible_act_evidence_identity=act_evidence.identity,
        result_kind=STANDING_LOCALITY_CONTINUATION_RESULT_KIND,
        result_identity=result_identity,
        result_content=result_material,
        responsibility=STANDING_LOCALITY_CONTINUATION_RESPONSIBILITY,
        live_boundary="standing_locality_continuation",
        responsible_boundary="this Seed",
    )
    return ledger.append(
        STANDING_LOCALITY_CONTINUATION_RECORDED_KIND,
        _recorded_result_material(
            result_material,
            responsible_act_evidence_identity=act_evidence.identity,
            evidence_of_yield_relation_identity=evidence_of_yield_relation.identity,
        ),
        locality_identity=locality_identity,
    )


def get_recorded_standing_locality_continuation(
    ledger: EventLedger, recorded_result_event_identity: str
) -> dict[str, Any]:
    """Read one direct continuation relation through its exact Evidence."""

    _require_identity(
        recorded_result_event_identity,
        "Standing Locality continuation read requires one exact result occurrence",
    )
    event = ledger.get(recorded_result_event_identity)
    if (
        event is None
        or event.kind != STANDING_LOCALITY_CONTINUATION_RECORDED_KIND
        or type(event.locality_identity) is not str
        or not event.locality_identity
        or event.exact_material is not None
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise StandingLocalityContinuationError(
            "the Standing Locality continuation result is absent or corrupted"
        )
    act_evidence = _validated_act_evidence(
        ledger, event.material.get("responsible_act_evidence_identity")
    )
    result_identity = event.material.get("result_identity")
    expected = _result_material(
        result_identity=result_identity,
        continuation_act_identity=act_evidence.material[
            "continuation_act_identity"
        ],
        act_occurrence_identity=act_evidence.material["act_occurrence_identity"],
        locality_relation_occurrence_identity=act_evidence.material[
            "locality_relation_occurrence_identity"
        ],
        responsibility_assignment_reference=act_evidence.material[
            "responsibility_assignment_reference"
        ],
        source_standing_reference=act_evidence.material[
            "source_standing_reference"
        ],
        destination_locality_identity=event.locality_identity,
    )
    expected_event_material = _recorded_result_material(
        expected,
        responsible_act_evidence_identity=act_evidence.identity,
        evidence_of_yield_relation_identity=event.material.get("evidence_of_yield_relation_identity"),
    )
    if (
        type(result_identity) is not str
        or not result_identity
        or act_evidence.locality_identity != event.locality_identity
        or event.material != expected_event_material
    ):
        raise StandingLocalityContinuationError(
            "the Standing Locality continuation result coordinates are not exact"
        )
    requirements = read_requirements_of_yield_relation(
        ledger,
        recorded_result_event_identity=event.identity,
        evidence_of_yield_relation_event_identity=event.material["evidence_of_yield_relation_identity"],
        responsible_act_evidence_event_identity=act_evidence.identity,
    )
    if not all(requirements.values()):
        raise StandingLocalityContinuationError(
            "the Standing Locality continuation carries no exact Evidence of Yield relation"
        )
    return deepcopy(event.material)


def get_standing_locality_continuation_responsibility_assignment(
    ledger: EventLedger, recorded_assignment_event_identity: str
) -> Event:
    """Read one Book-bounded Responsibility assignment Standing occurrence."""

    _require_identity(
        recorded_assignment_event_identity,
        "Standing Locality continuation requires one exact Responsibility assignment occurrence",
    )
    assignment = ledger.get(recorded_assignment_event_identity)
    if (
        assignment is None
        or assignment.kind
        != STANDING_LOCALITY_CONTINUATION_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND
        or type(assignment.locality_identity) is not str
        or not assignment.locality_identity
        or assignment.exact_material is not None
        or ledger.integrity_of(assignment.identity) == CORRUPTED
    ):
        raise StandingLocalityContinuationError(
            "the Standing Locality continuation Responsibility assignment is absent or corrupted"
        )
    material = assignment.material
    source_reference = material.get("source_standing_reference")
    if type(source_reference) is not dict:
        raise StandingLocalityContinuationError(
            "the Responsibility assignment carries no exact source boundary"
        )
    expected_reference = _source_standing_reference(
        ledger,
        source_locality_identity=source_reference.get("source_locality_identity"),
        addressed_representation_event_identity=source_reference.get(
            "addressed_representation_event_identity"
        ),
    )
    assignment_identity = material.get("assignment_identity")
    assignment_subject_identity = material.get("assignment_subject_identity")
    result_boundary_identity = material.get("result_boundary_identity")
    if (
        type(assignment_identity) is not str
        or not assignment_identity
        or type(assignment_subject_identity) is not str
        or not assignment_subject_identity
        or type(result_boundary_identity) is not str
        or not result_boundary_identity
        or len(
            {
                assignment_identity,
                assignment_subject_identity,
                result_boundary_identity,
            }
        )
        != 3
        or source_reference != expected_reference
        or material
        != _assignment_material(
            assignment_identity=assignment_identity,
            assignment_subject_identity=assignment_subject_identity,
            result_boundary_identity=result_boundary_identity,
            source_standing_reference=expected_reference,
            destination_locality_identity=assignment.locality_identity,
        )
    ):
        raise StandingLocalityContinuationError(
            "the Standing Locality continuation Responsibility assignment is not exact"
        )
    return assignment
