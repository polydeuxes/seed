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
from seed_runtime.yield_relation import (
    RECORDED_YIELD_RELATION_EVENT,
    _record_yield_relation,
    read_requirements_of_yield_relation,
)


STANDING_LOCALITY_CONTINUATION_ACT_OCCURRENCE_EVENT = (
    "operator.standing.locality_continuation_act_occurrence_recorded"
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
    "exact Locality"
)
STANDING_LOCALITY_CONTINUATION_INPUT_ROLE = (
    "exact prior Locality Standing boundary"
)
EVENT_KIND_RESPONSIBILITIES = {
    STANDING_LOCALITY_CONTINUATION_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND: (
        "06.Locality.B"
    ),
    STANDING_LOCALITY_CONTINUATION_ACT_OCCURRENCE_EVENT: "02.Acts.A",
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
    standing_boundary_event_identity: str,
) -> dict[str, str | None]:
    """Resolve one intact exact source Standing boundary."""

    _require_identity(
        source_locality_identity,
        "Standing Locality continuation requires one exact source Locality",
    )
    _require_identity(
        standing_boundary_event_identity,
        "Standing Locality continuation requires one exact Standing boundary",
    )
    source_boundary = ledger.get(standing_boundary_event_identity)
    if (
        source_boundary is None
        or source_boundary.locality_identity != source_locality_identity
        or ledger.integrity_of(source_boundary.identity) == CORRUPTED
    ):
        raise StandingLocalityContinuationError(
            "Standing Locality continuation requires one intact source boundary"
        )
    occurrences = ledger.list_locality(source_locality_identity)
    positions = {event.identity: position for position, event in enumerate(occurrences)}
    if positions.get(standing_boundary_event_identity) is None:
        raise StandingLocalityContinuationError(
            "the source Standing boundary is absent from its source Locality"
        )
    return {
        "source_locality_identity": source_locality_identity,
        "source_standing_through_event_occurrence_identity": (
            standing_boundary_event_identity
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
    standing_boundary = source_standing_reference[
        "source_standing_through_event_occurrence_identity"
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
        "standing_boundary_occurrence_reference": standing_boundary,
        "scope": {
            "source_locality_identity": source_standing_reference[
                "source_locality_identity"
            ],
            "source_standing_through_event_occurrence_identity": source_standing_reference[
                "source_standing_through_event_occurrence_identity"
            ],
            "destination_locality_identity": destination_locality_identity,
        },
        "result_boundary_identity": result_boundary_identity,
        "unknown": [
            "Applicability of every carried subject to another Act: Unknown"
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


def _act_occurrence_material(
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
        "unknown": [
            "Applicability of every carried subject to another Act: Unknown"
        ],
    }


def _recorded_result_material(
    result_material: dict[str, Any],
    *,
    act_occurrence_event_identity: str,
    yield_relation_identity: str,
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
        "unknown": result_material["unknown"],
        "act_occurrence_event_identity": act_occurrence_event_identity,
        "yield_relation_identity": yield_relation_identity,
    }


def record_standing_locality_continuation_responsibility_assignment(
    ledger: EventLedger,
    *,
    source_locality_identity: str,
    standing_boundary_event_identity: str,
) -> Event:
    """Record one bounded assignment at one fresh destination Locality."""

    if not isinstance(ledger, EventLedger):
        raise TypeError("Standing Locality continuation requires one EventLedger")
    source_reference = _source_standing_reference(
        ledger,
        source_locality_identity=source_locality_identity,
        standing_boundary_event_identity=standing_boundary_event_identity,
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


def record_standing_locality_continuation_act_occurrence(
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
        STANDING_LOCALITY_CONTINUATION_ACT_OCCURRENCE_EVENT,
        _act_occurrence_material(
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


def _validated_act_occurrence(
    ledger: EventLedger, act_occurrence_event_identity: str
) -> Event:
    _require_identity(
        act_occurrence_event_identity,
        "Standing Locality continuation result requires one exact Act occurrence identity",
    )
    act_occurrence = ledger.get(act_occurrence_event_identity)
    if (
        act_occurrence is None
        or act_occurrence.kind != STANDING_LOCALITY_CONTINUATION_ACT_OCCURRENCE_EVENT
        or type(act_occurrence.locality_identity) is not str
        or not act_occurrence.locality_identity
        or act_occurrence.exact_material is not None
        or ledger.integrity_of(act_occurrence.identity) == CORRUPTED
    ):
        raise StandingLocalityContinuationError(
            "Standing Locality continuation result requires intact Act occurrence"
        )
    material = act_occurrence.material
    source_reference = material.get("source_standing_reference")
    if type(source_reference) is not dict:
        raise StandingLocalityContinuationError(
            "Standing Locality continuation Act occurrence carries no exact source boundary"
        )
    expected_reference = _source_standing_reference(
        ledger,
        source_locality_identity=source_reference.get("source_locality_identity"),
        standing_boundary_event_identity=source_reference.get(
            "source_standing_through_event_occurrence_identity"
        ),
    )
    if source_reference != expected_reference:
        raise StandingLocalityContinuationError(
            "Standing Locality continuation Act occurrence carries another source boundary"
        )
    continuation_act_identity = material.get("continuation_act_identity")
    act_occurrence_identity = material.get("act_occurrence_identity")
    locality_relation_occurrence_identity = material.get(
        "locality_relation_occurrence_identity"
    )
    assignment_reference = material.get("responsibility_assignment_reference")
    if type(assignment_reference) is not dict:
        raise StandingLocalityContinuationError(
            "Standing Locality continuation Act occurrence carries no exact Responsibility assignment"
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
        or assignment.locality_identity != act_occurrence.locality_identity
        or assignment.material["responsibility"]
        != STANDING_LOCALITY_CONTINUATION_RESPONSIBILITY
        or assignment.material["responsible_boundary"] != "this Seed"
        or assignment.material["source_standing_reference"] != expected_reference
        or assignment.material["destination_locality_identity"]
        != act_occurrence.locality_identity
        or material.get("destination_locality_identity")
        != act_occurrence.locality_identity
        or material
        != _act_occurrence_material(
            continuation_act_identity=continuation_act_identity,
            act_occurrence_identity=act_occurrence_identity,
            locality_relation_occurrence_identity=(
                locality_relation_occurrence_identity
            ),
            responsibility_assignment_reference=assignment_reference,
            source_standing_reference=expected_reference,
            destination_locality_identity=act_occurrence.locality_identity,
        )
    ):
        raise StandingLocalityContinuationError(
            "Standing Locality continuation Act occurrence is not exact"
        )
    return act_occurrence


def record_standing_locality_continuation_result(
    ledger: EventLedger,
    *,
    act_occurrence_event_identity: str,
) -> Event:
    """Record the Yield and direct Locality relation for one recorded Act."""

    act_occurrence = _validated_act_occurrence(
        ledger, act_occurrence_event_identity
    )
    material = act_occurrence.material
    locality_identity = act_occurrence.locality_identity
    act_occurrence_identity = material["act_occurrence_identity"]
    for prior_yield in ledger.iter_locality_kind(
        locality_identity, RECORDED_YIELD_RELATION_EVENT
    ):
        dimensions = prior_yield.material.get("dimensions")
        if (
            prior_yield.material.get("act_occurrence_event_identity")
            == act_occurrence.identity
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
            prior_result.material.get("act_occurrence_event_identity")
            == act_occurrence.identity
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
    yield_relation = _record_yield_relation(
        ledger,
        locality_identity=locality_identity,
        exact_act=STANDING_LOCALITY_CONTINUATION_ACT,
        act_occurrence_identity=act_occurrence_identity,
        act_occurrence_event_identity=act_occurrence.identity,
        result_kind=STANDING_LOCALITY_CONTINUATION_RESULT_KIND,
        result_identity=result_identity,
        result_content=result_material,
        responsibility=STANDING_LOCALITY_CONTINUATION_RESPONSIBILITY,
        occurrence_boundary="standing_locality_continuation",
        responsible_boundary="this Seed",
    )
    return ledger.append(
        STANDING_LOCALITY_CONTINUATION_RECORDED_KIND,
        _recorded_result_material(
            result_material,
            act_occurrence_event_identity=act_occurrence.identity,
            yield_relation_identity=yield_relation.identity,
        ),
        locality_identity=locality_identity,
    )


def get_recorded_standing_locality_continuation(
    ledger: EventLedger, recorded_result_event_identity: str
) -> dict[str, Any]:
    """Read one direct continuation relation through its exact relation."""

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
    act_occurrence = _validated_act_occurrence(
        ledger, event.material.get("act_occurrence_event_identity")
    )
    result_identity = event.material.get("result_identity")
    expected = _result_material(
        result_identity=result_identity,
        continuation_act_identity=act_occurrence.material[
            "continuation_act_identity"
        ],
        act_occurrence_identity=act_occurrence.material["act_occurrence_identity"],
        locality_relation_occurrence_identity=act_occurrence.material[
            "locality_relation_occurrence_identity"
        ],
        responsibility_assignment_reference=act_occurrence.material[
            "responsibility_assignment_reference"
        ],
        source_standing_reference=act_occurrence.material[
            "source_standing_reference"
        ],
        destination_locality_identity=event.locality_identity,
    )
    expected_event_material = _recorded_result_material(
        expected,
        act_occurrence_event_identity=act_occurrence.identity,
        yield_relation_identity=event.material.get("yield_relation_identity"),
    )
    if (
        type(result_identity) is not str
        or not result_identity
        or act_occurrence.locality_identity != event.locality_identity
        or event.material != expected_event_material
    ):
        raise StandingLocalityContinuationError(
            "the Standing Locality continuation result coordinates are not exact"
        )
    requirements = read_requirements_of_yield_relation(
        ledger,
        recorded_result_event_identity=event.identity,
        yield_relation_event_identity=event.material["yield_relation_identity"],
        act_occurrence_event_identity=act_occurrence.identity,
    )
    if not all(requirements.values()):
        raise StandingLocalityContinuationError(
            "the Standing Locality continuation carries no exact Yield relation"
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
        standing_boundary_event_identity=source_reference.get(
            "source_standing_through_event_occurrence_identity"
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
