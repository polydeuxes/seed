"""Determine pair-position Assertions carrying one addressed byte coordinate.

This D.2 lifecycle consumes one exact recorded direct pair-position Measurement
and one exact source-byte position-coordinate reference.  It preserves every
Assertion reference carrying that exact coordinate and no other Assertion; it
establishes no recurrence, shared position, represented relation, or other
relation.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from seed_runtime.event import Event
from seed_runtime.events import CORRUPTED, EventLedger
from seed_runtime.evidence_of_yield_relation import (
    RECORDED_EVIDENCE_OF_YIELD_RELATION_KIND,
    _record_evidence_of_yield_relation,
    read_requirements_of_yield_relation,
)
from seed_runtime.identities import new_identity
from seed_runtime.measurement_of_position_coordinates_of_byte_pair_occurrences import (
    BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND,
    ReferenceToRecordedPositionOfBytePairOccurrence,
    references_to_recorded_byte_pair_occurrences_carrying_addressed_source_position_coordinate,
)


RESPONSIBILITY_ASSIGNMENT_KIND = (
    "operator.addressed_byte_occurrence_reference_determination."
    "responsibility_assignment_recorded"
)
APPLICABILITY_ACT_EVIDENCE_KIND = (
    "operator.addressed_byte_occurrence_reference_determination."
    "applicability_act_evidenced"
)
APPLICABILITY_RESULT_KIND = (
    "operator.addressed_byte_occurrence_reference_determination."
    "applicability_recorded"
)
DETERMINATION_ACT_EVIDENCE_KIND = (
    "operator.addressed_byte_occurrence_reference_determination."
    "determination_measurement_act_evidenced"
)
DETERMINATION_RESULT_KIND = (
    "operator.addressed_byte_occurrence_reference_determination."
    "determination_measurement_recorded"
)

BOOK_CLAUSE = "01.Source.D.2"
RESPONSIBILITY = (
    "determine every exact pair-occurrence position Assertion reference carrying "
    "one addressed source-byte position-coordinate reference and no other "
    "Assertion reference"
)
APPLICABILITY_ACT = "addressed byte occurrence reference determination Applicability"
DETERMINATION_ACT = (
    "declared Measurement of exact pair-occurrence position Assertion "
    "references carrying one addressed source-byte position-coordinate reference"
)
APPLICABILITY_YIELD_RESULT_KIND = (
    "addressed byte occurrence reference determination Applicability result"
)
DETERMINATION_YIELD_RESULT_KIND = (
    "result of declared Measurement of exact pair-occurrence position "
    "Assertion references carrying one addressed source-byte position-coordinate "
    "reference"
)
APPLICABILITY_BOUNDARY = (
    "addressed_byte_occurrence_reference_determination_applicability"
)
DETERMINATION_BOUNDARY = "addressed_byte_occurrence_reference_determination"
DETERMINATION_RULE = (
    "every exact pair-occurrence position Assertion reference carrying the "
    "addressed source-byte position-coordinate reference and no other Assertion "
    "reference, in source occurrence order"
)
LIMITS = [
    "bounded to one exact direct pair-position Measurement result, source "
    "occurrence, Locality, completeness boundary, and addressed coordinate",
    "establishes no recurrence, shared position relation, represented relation, "
    "or other relation",
]
UNKNOWN = [
    "what the addressed byte occurrence represents: Unknown",
    "what each carried Assertion reference represents: Unknown",
]

EVENT_KIND_RESPONSIBILITIES = {
    RESPONSIBILITY_ASSIGNMENT_KIND: "01.Source.D.2",
    APPLICABILITY_ACT_EVIDENCE_KIND: "02.Acts.A",
    APPLICABILITY_RESULT_KIND: "01.Standing.E.1",
    DETERMINATION_ACT_EVIDENCE_KIND: "02.Acts.A",
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
        "responsible_act_evidence_identity": event.material[
            "responsible_act_evidence_identity"
        ],
        "evidence_of_yield_relation_identity": event.material[
            "evidence_of_yield_relation_identity"
        ],
    }


def _determination_result_reference(event: Event) -> dict[str, str]:
    """Carry the exact identities of one validated D.2 Measurement result."""

    return {
        "recorded_occurrence_identity": event.identity,
        "result_identity": event.material["result_identity"],
        "act_occurrence_identity": event.material[
            "determination_act_occurrence_identity"
        ],
        "responsible_act_evidence_identity": event.material[
            "responsible_act_evidence_identity"
        ],
        "evidence_of_yield_relation_identity": event.material[
            "evidence_of_yield_relation_identity"
        ],
    }


def _assignment_reference(event: Event) -> dict[str, str]:
    return {
        "recorded_occurrence_identity": event.identity,
        "assignment_identity": event.material["assignment_identity"],
        "assignment_subject_identity": event.material[
            "assignment_subject_identity"
        ],
    }


def _applicability_result_reference(event: Event) -> dict[str, str]:
    return {
        "recorded_occurrence_identity": event.identity,
        "result_identity": event.material["result_identity"],
        "applicability_act_occurrence_identity": event.material[
            "applicability_act_occurrence_identity"
        ],
        "responsible_act_evidence_identity": event.material[
            "responsible_act_evidence_identity"
        ],
        "evidence_of_yield_relation_identity": event.material[
            "evidence_of_yield_relation_identity"
        ],
    }


def _references_carrying_addressed_coordinate(
    ledger: EventLedger,
    *,
    result_event_identity: str,
    coordinate_reference: dict[str, Any],
) -> tuple[ReferenceToRecordedPositionOfBytePairOccurrence, ...]:
    try:
        return references_to_recorded_byte_pair_occurrences_carrying_addressed_source_position_coordinate(
            ledger,
            result_event_identity,
            coordinate_reference,
        )
    except (TypeError, ValueError) as error:
        raise AddressedByteOccurrenceReferenceDeterminationError(
            "determination requires one exact addressed direct result coordinate"
        ) from error


def _source(
    ledger: EventLedger,
    *,
    result_event_identity: str,
    coordinate_reference: dict[str, Any],
) -> tuple[Event, tuple[ReferenceToRecordedPositionOfBytePairOccurrence, ...]]:
    references = _references_carrying_addressed_coordinate(
        ledger,
        result_event_identity=result_event_identity,
        coordinate_reference=coordinate_reference,
    )
    event = ledger.get(result_event_identity)
    if (
        event is None
        or event.kind != BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND
        or event.exact_material is not None
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise AddressedByteOccurrenceReferenceDeterminationError(
            "determination requires one intact direct result"
        )
    return event, references


def _scope(
    *,
    source_result: Event,
    coordinate_reference: dict[str, Any],
    standing_boundary_identity: str,
) -> dict[str, str]:
    return {
        "locality_identity": source_result.locality_identity,
        "source_ingest_occurrence_identity": coordinate_reference[
            "source_ingest_occurrence_identity"
        ],
        "completeness_boundary_identity": coordinate_reference[
            "completeness_boundary_identity"
        ],
        "standing_boundary_identity": standing_boundary_identity,
    }


def _authority() -> dict[str, str]:
    return {
        "source": "this Book",
        "book_clause_identity": BOOK_CLAUSE,
        "authority_limit": "bounded",
        "act": DETERMINATION_ACT,
        "negative_authority": (
            "establish no recurrence, shared position relation, represented "
            "relation or other relation"
        ),
    }


def _standing_carries_source(
    ledger: EventLedger,
    *,
    standing: dict[str, Any],
    source_result: Event,
    required_boundary_identity: str,
) -> None:
    measurements = standing.get("measurement_occurrences") if type(standing) is dict else None
    through = standing.get("through_event_occurrence_identity") if type(standing) is dict else None
    if (
        type(standing) is not dict
        or standing.get("locality_identity") != source_result.locality_identity
        or type(measurements) is not dict
        or measurements.get(source_result.identity) != _direct_result_reference(source_result)
        or type(through) is not str
        or not through
        or type(required_boundary_identity) is not str
        or not required_boundary_identity
    ):
        raise AddressedByteOccurrenceReferenceDeterminationError(
            "current Standing carries no exact addressed direct result"
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
            "current Standing boundary carries no addressed direct result"
        ) from error
    if tuple(event.identity for event in read) != ordered:
        raise AddressedByteOccurrenceReferenceDeterminationError(
            "current Standing boundary carries no addressed direct result"
        )


def _current_standing(
    ledger: EventLedger,
    *,
    source_result: Event,
    locality_standing: dict[str, Any],
) -> dict[str, Any]:
    from seed_runtime.operator_locality_standing import read_operator_locality_standing

    current = read_operator_locality_standing(
        ledger, locality_identity=source_result.locality_identity
    )
    if locality_standing != current:
        raise AddressedByteOccurrenceReferenceDeterminationError(
            "determination requires exact current Standing"
        )
    boundary = current.get("through_event_occurrence_identity")
    _standing_carries_source(
        ledger,
        standing=current,
        source_result=source_result,
        required_boundary_identity=boundary,
    )
    boundary_event = ledger.get(boundary)
    if (
        boundary_event is None
        or ledger.integrity_of(boundary_event.identity) == CORRUPTED
        or ledger.append_boundary_through_occurrence(boundary_event.identity)
        != ledger.append_boundary()
    ):
        raise AddressedByteOccurrenceReferenceDeterminationError(
            "determination requires Standing at the append tip"
        )
    return current


def _require_unchanged_stored_event(
    ledger: EventLedger,
    *,
    event: Event,
    kind: str,
    material: dict[str, Any],
    message: str,
) -> None:
    if (
        type(event) is not Event
        or ledger.get(event.identity) != event
        or event.kind != kind
        or event.exact_material is not None
        or ledger.integrity_of(event.identity) == CORRUPTED
        or event.material != material
    ):
        raise AddressedByteOccurrenceReferenceDeterminationError(message)


def _require_stage_at_append_tip(
    ledger: EventLedger, *, event: Event | None, message: str
) -> None:
    if (
        event is None
        or ledger.get(event.identity) != event
        or ledger.integrity_of(event.identity) == CORRUPTED
        or ledger.append_boundary_through_occurrence(event.identity)
        != ledger.append_boundary()
    ):
        raise AddressedByteOccurrenceReferenceDeterminationError(message)


_IDENTITY_COORDINATES = (
    "assignment_identity",
    "assignment_subject_identity",
    "applicability_act_identity",
    "applicability_act_occurrence_identity",
    "applicability_result_identity",
    "determination_act_identity",
    "determination_act_occurrence_identity",
    "determination_result_identity",
)


def _assignment_material(
    *,
    source_result: Event,
    coordinate_reference: dict[str, Any],
    standing_boundary_identity: str,
    identities: dict[str, str],
) -> dict[str, Any]:
    return {
        "assignment_identity": identities["assignment_identity"],
        "assignment_subject_identity": identities["assignment_subject_identity"],
        "applicability_act_identity": identities["applicability_act_identity"],
        "applicability_act_occurrence_identity": identities[
            "applicability_act_occurrence_identity"
        ],
        "applicability_result_identity": identities[
            "applicability_result_identity"
        ],
        "determination_act_identity": identities["determination_act_identity"],
        "determination_act_occurrence_identity": identities[
            "determination_act_occurrence_identity"
        ],
        "determination_result_identity": identities[
            "determination_result_identity"
        ],
        "book_clause_identity": BOOK_CLAUSE,
        "responsibility": RESPONSIBILITY,
        "responsible_boundary": "this Seed",
        "direct_pair_position_result_reference": _direct_result_reference(
            source_result
        ),
        "addressed_source_byte_position_coordinate_reference": deepcopy(
            coordinate_reference
        ),
        "determination_rule": DETERMINATION_RULE,
        "standing_boundary_identity": standing_boundary_identity,
        "scope": _scope(
            source_result=source_result,
            coordinate_reference=coordinate_reference,
            standing_boundary_identity=standing_boundary_identity,
        ),
        "authority": _authority(),
        "limits": list(LIMITS),
        "unknown": list(UNKNOWN),
    }


def record_addressed_byte_occurrence_reference_determination_responsibility_assignment(
    ledger: EventLedger,
    *,
    direct_result_event_identity: str,
    addressed_source_byte_position_coordinate_reference: dict[str, Any],
    locality_standing: dict[str, Any],
) -> Event:
    """Assign one exact addressed source coordinate carried by current Standing."""

    if not isinstance(ledger, EventLedger):
        raise TypeError("determination assignment requires one EventLedger")
    source_result, _references = _source(
        ledger,
        result_event_identity=_identity(
            direct_result_event_identity,
            "determination assignment requires one direct result",
        ),
        coordinate_reference=addressed_source_byte_position_coordinate_reference,
    )
    current = _current_standing(
        ledger, source_result=source_result, locality_standing=locality_standing
    )
    identities = {
        "assignment_identity": new_identity(
            "addressed_byte_occurrence_reference_assignment"
        ),
        "assignment_subject_identity": new_identity(
            "addressed_byte_occurrence_reference_assignment_subject"
        ),
        "applicability_act_identity": new_identity(
            "addressed_byte_occurrence_reference_applicability_act"
        ),
        "applicability_act_occurrence_identity": new_identity(
            "addressed_byte_occurrence_reference_applicability_act_occurrence"
        ),
        "applicability_result_identity": new_identity(
            "addressed_byte_occurrence_reference_applicability_result"
        ),
        "determination_act_identity": new_identity(
            "addressed_byte_occurrence_reference_determination_measurement_act"
        ),
        "determination_act_occurrence_identity": new_identity(
            "addressed_byte_occurrence_reference_determination_measurement_act_occurrence"
        ),
        "determination_result_identity": new_identity(
            "addressed_byte_occurrence_reference_determination_measurement_result"
        ),
    }
    if len(set(identities.values())) != len(identities):
        raise AddressedByteOccurrenceReferenceDeterminationError(
            "determination lifecycle identities collapsed"
        )
    source_material = deepcopy(source_result.material)
    source_read, _references_read = _source(
        ledger,
        result_event_identity=source_result.identity,
        coordinate_reference=addressed_source_byte_position_coordinate_reference,
    )
    _require_unchanged_stored_event(
        ledger,
        event=source_result,
        kind=BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND,
        material=source_material,
        message="determination assignment requires an intact exact source",
    )
    if source_read != source_result:
        raise AddressedByteOccurrenceReferenceDeterminationError(
            "determination assignment requires an intact exact source"
        )
    _require_stage_at_append_tip(
        ledger,
        event=ledger.get(current["through_event_occurrence_identity"]),
        message="determination assignment Standing left the append tip",
    )
    return ledger.append(
        RESPONSIBILITY_ASSIGNMENT_KIND,
        _assignment_material(
            source_result=source_result,
            coordinate_reference=(
                addressed_source_byte_position_coordinate_reference
            ),
            standing_boundary_identity=current[
                "through_event_occurrence_identity"
            ],
            identities=identities,
        ),
        locality_identity=source_result.locality_identity,
    )


def _read_assignment(
    ledger: EventLedger,
    event_identity: str,
    *,
    prior_standing: dict[str, Any] | None = None,
) -> tuple[
    Event,
    Event,
    tuple[ReferenceToRecordedPositionOfBytePairOccurrence, ...],
]:
    event = ledger.get(event_identity)
    if (
        event is None
        or event.kind != RESPONSIBILITY_ASSIGNMENT_KIND
        or event.exact_material is not None
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise AddressedByteOccurrenceReferenceDeterminationError(
            "determination assignment is absent or corrupted"
        )
    material = event.material
    source_reference = material.get("direct_pair_position_result_reference")
    coordinate_reference = material.get(
        "addressed_source_byte_position_coordinate_reference"
    )
    source_identity = (
        source_reference.get("recorded_occurrence_identity")
        if type(source_reference) is dict
        else None
    )
    source_result, references = _source(
        ledger,
        result_event_identity=source_identity,
        coordinate_reference=coordinate_reference,
    )
    identities = {key: material.get(key) for key in _IDENTITY_COORDINATES}
    standing_boundary = material.get("standing_boundary_identity")
    if (
        event.locality_identity != source_result.locality_identity
        or any(type(value) is not str or not value for value in identities.values())
        or len(set(identities.values())) != len(identities)
        or type(standing_boundary) is not str
        or not standing_boundary
        or material
        != _assignment_material(
            source_result=source_result,
            coordinate_reference=coordinate_reference,
            standing_boundary_identity=standing_boundary,
            identities=identities,
        )
    ):
        raise AddressedByteOccurrenceReferenceDeterminationError(
            "determination assignment coordinates are not exact"
        )
    if prior_standing is None:
        from seed_runtime.operator_locality_standing import (
            read_operator_locality_standing_through,
        )

        prior_standing = read_operator_locality_standing_through(
            ledger,
            locality_identity=source_result.locality_identity,
            through_event_occurrence_identity=standing_boundary,
        )
    _standing_carries_source(
        ledger,
        standing=prior_standing,
        source_result=source_result,
        required_boundary_identity=standing_boundary,
    )
    try:
        ledger.occurrences_in_append_order(
            (standing_boundary, event.identity),
            locality_identity=event.locality_identity,
        )
    except ValueError as error:
        raise AddressedByteOccurrenceReferenceDeterminationError(
            "determination assignment has false Standing boundary order"
        ) from error
    return event, source_result, references


def get_addressed_byte_occurrence_reference_determination_responsibility_assignment(
    ledger: EventLedger, event_identity: str
) -> Event:
    return _read_assignment(ledger, event_identity)[0]


def _require_stage_standing(
    ledger: EventLedger,
    *,
    standing: dict[str, Any],
    source_result: Event,
    assignment: Event,
    applicability_result: Event | None = None,
) -> None:
    current = _current_standing(
        ledger, source_result=source_result, locality_standing=standing
    )
    assignments = current.get("responsibility_assignment_occurrences")
    applicability = current.get("applicability_result_occurrences")
    required_tip = assignment.identity
    if applicability_result is not None:
        required_tip = applicability_result.identity
    if (
        type(assignments) is not dict
        or assignments.get(assignment.identity, object()) is not None
        or current.get("through_event_occurrence_identity") != required_tip
        or (
            applicability_result is not None
            and (
                type(applicability) is not dict
                or applicability.get(applicability_result.identity, object())
                is not None
            )
        )
    ):
        raise AddressedByteOccurrenceReferenceDeterminationError(
            "current Standing carries no exact determination stage"
        )


def _refuse_existing_act(
    ledger: EventLedger,
    *,
    assignment: Event,
    kind: str,
    occurrence_coordinate: str,
) -> None:
    occurrence_identity = assignment.material[occurrence_coordinate]
    for event in ledger.iter_locality_kind(assignment.locality_identity, kind):
        if (
            event.material.get(occurrence_coordinate) == occurrence_identity
            or event.material.get("responsibility_assignment_reference")
            == _assignment_reference(assignment)
        ):
            raise AddressedByteOccurrenceReferenceDeterminationError(
                "determination assignment already carries this Act"
            )


def _applicability_act_material(
    *, assignment: Event, source_result: Event
) -> dict[str, Any]:
    return {
        "applicability_act_identity": assignment.material[
            "applicability_act_identity"
        ],
        "applicability_act_occurrence_identity": assignment.material[
            "applicability_act_occurrence_identity"
        ],
        "act": APPLICABILITY_ACT,
        "responsibility": RESPONSIBILITY,
        "responsible_boundary": "this Seed",
        "responsibility_assignment_reference": _assignment_reference(assignment),
        "direct_pair_position_result_reference": _direct_result_reference(
            source_result
        ),
        "addressed_source_byte_position_coordinate_reference": deepcopy(
            assignment.material[
                "addressed_source_byte_position_coordinate_reference"
            ]
        ),
        "determination_rule": DETERMINATION_RULE,
        "downstream_act_identity": assignment.material[
            "determination_act_identity"
        ],
        "scope": deepcopy(assignment.material["scope"]),
        "authority": deepcopy(assignment.material["authority"]),
        "evidence_scope": "Evidence for this exact Applicability Act occurrence",
        "limits": list(assignment.material["limits"]),
        "unknown": list(assignment.material["unknown"]),
    }


def record_addressed_byte_occurrence_reference_determination_applicability_act_evidence(
    ledger: EventLedger,
    *,
    responsibility_assignment_event_identity: str,
    responsibility_assignment_standing: dict[str, Any],
) -> Event:
    assignment, source_result, _references = _read_assignment(
        ledger, responsibility_assignment_event_identity
    )
    _require_stage_standing(
        ledger,
        standing=responsibility_assignment_standing,
        source_result=source_result,
        assignment=assignment,
    )
    assignment_material = deepcopy(assignment.material)
    source_material = deepcopy(source_result.material)
    _refuse_existing_act(
        ledger,
        assignment=assignment,
        kind=APPLICABILITY_ACT_EVIDENCE_KIND,
        occurrence_coordinate="applicability_act_occurrence_identity",
    )
    source_read, _references_read = _source(
        ledger,
        result_event_identity=source_result.identity,
        coordinate_reference=assignment.material[
            "addressed_source_byte_position_coordinate_reference"
        ],
    )
    _require_unchanged_stored_event(
        ledger,
        event=source_result,
        kind=BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND,
        material=source_material,
        message="Applicability Act requires an intact exact source",
    )
    _require_unchanged_stored_event(
        ledger,
        event=assignment,
        kind=RESPONSIBILITY_ASSIGNMENT_KIND,
        material=assignment_material,
        message="Applicability Act requires an intact exact assignment",
    )
    if source_read != source_result:
        raise AddressedByteOccurrenceReferenceDeterminationError(
            "Applicability Act requires an intact exact source"
        )
    _require_stage_at_append_tip(
        ledger,
        event=assignment,
        message="Applicability Act assignment left the append tip",
    )
    return ledger.append(
        APPLICABILITY_ACT_EVIDENCE_KIND,
        _applicability_act_material(
            assignment=assignment, source_result=source_result
        ),
        locality_identity=assignment.locality_identity,
    )


def _read_applicability_act(
    ledger: EventLedger,
    event_identity: str,
    *,
    prior_standing: dict[str, Any] | None = None,
) -> tuple[
    Event,
    Event,
    Event,
    tuple[ReferenceToRecordedPositionOfBytePairOccurrence, ...],
]:
    event = ledger.get(event_identity)
    if (
        event is None
        or event.kind != APPLICABILITY_ACT_EVIDENCE_KIND
        or event.exact_material is not None
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise AddressedByteOccurrenceReferenceDeterminationError(
            "determination Applicability Act Evidence is absent or corrupted"
        )
    reference = event.material.get("responsibility_assignment_reference")
    assignment_identity = (
        reference.get("recorded_occurrence_identity")
        if type(reference) is dict
        else None
    )
    assignment, source_result, references = _read_assignment(
        ledger, assignment_identity, prior_standing=prior_standing
    )
    if (
        reference != _assignment_reference(assignment)
        or event.locality_identity != assignment.locality_identity
        or event.material
        != _applicability_act_material(
            assignment=assignment, source_result=source_result
        )
    ):
        raise AddressedByteOccurrenceReferenceDeterminationError(
            "determination Applicability Act Evidence is not exact"
        )
    try:
        ledger.occurrences_in_append_order(
            (assignment.identity, event.identity),
            locality_identity=event.locality_identity,
        )
    except ValueError as error:
        raise AddressedByteOccurrenceReferenceDeterminationError(
            "determination Applicability Act order is false"
        ) from error
    return event, assignment, source_result, references


def get_addressed_byte_occurrence_reference_determination_applicability_act_evidence(
    ledger: EventLedger, event_identity: str
) -> Event:
    return _read_applicability_act(ledger, event_identity)[0]


def _applicability_finding(
    *, assignment: Event, source_result: Event
) -> dict[str, Any]:
    coordinate = assignment.material[
        "addressed_source_byte_position_coordinate_reference"
    ]
    return {
        "first_subject": {
            "direct_pair_position_result_reference": _direct_result_reference(
                source_result
            ),
            "addressed_source_byte_position_coordinate_reference": deepcopy(
                coordinate
            ),
        },
        "relation": "applicable_to",
        "second_subject": {
            "exact_act": DETERMINATION_ACT,
            "act_identity": assignment.material["determination_act_identity"],
            "act_occurrence_identity": assignment.material[
                "determination_act_occurrence_identity"
            ],
            "result_identity": assignment.material[
                "determination_result_identity"
            ],
        },
        "source_ingest_occurrence_identity": coordinate[
            "source_ingest_occurrence_identity"
        ],
        "locality_identity": coordinate["locality_identity"],
        "completeness_boundary_identity": coordinate[
            "completeness_boundary_identity"
        ],
        "responsibility_assignment_reference": _assignment_reference(assignment),
    }


def _applicability_result_material(
    *, act: Event, assignment: Event, source_result: Event
) -> dict[str, Any]:
    return {
        "result_identity": assignment.material["applicability_result_identity"],
        "exact_act": APPLICABILITY_ACT,
        "applicability_act_identity": assignment.material[
            "applicability_act_identity"
        ],
        "applicability_act_occurrence_identity": assignment.material[
            "applicability_act_occurrence_identity"
        ],
        "downstream_act_identity": assignment.material[
            "determination_act_identity"
        ],
        "downstream_act_occurrence_identity": assignment.material[
            "determination_act_occurrence_identity"
        ],
        "responsibility": RESPONSIBILITY,
        "responsible_boundary": "this Seed",
        "responsibility_assignment_reference": _assignment_reference(assignment),
        "direct_pair_position_result_reference": _direct_result_reference(
            source_result
        ),
        "addressed_source_byte_position_coordinate_reference": deepcopy(
            assignment.material[
                "addressed_source_byte_position_coordinate_reference"
            ]
        ),
        "determination_rule": DETERMINATION_RULE,
        "applicability_finding": _applicability_finding(
            assignment=assignment, source_result=source_result
        ),
        "scope": deepcopy(assignment.material["scope"]),
        "authority": deepcopy(assignment.material["authority"]),
        "limits": list(assignment.material["limits"]),
        "unknown": list(assignment.material["unknown"]),
    }


def _refuse_existing_result(
    ledger: EventLedger,
    *,
    act: Event,
    result_kind: str,
    occurrence_coordinate: str,
) -> None:
    occurrence_identity = act.material[occurrence_coordinate]
    for event in ledger.iter_locality_kind(
        act.locality_identity, RECORDED_EVIDENCE_OF_YIELD_RELATION_KIND
    ):
        if (
            event.material.get("responsible_act_evidence_identity") == act.identity
            or event.material.get("dimensions", {}).get("act_occurrence_identity")
            == occurrence_identity
        ):
            raise AddressedByteOccurrenceReferenceDeterminationError(
                "determination Act already carries a Yield"
            )
    for event in ledger.iter_locality_kind(act.locality_identity, result_kind):
        if (
            event.material.get("responsible_act_evidence_identity") == act.identity
            or event.material.get(occurrence_coordinate) == occurrence_identity
        ):
            raise AddressedByteOccurrenceReferenceDeterminationError(
                "determination Act already carries a result"
            )


def _prepare_result_yield(
    ledger: EventLedger,
    *,
    act: Event,
    occurrence_coordinate: str,
    result_event_kind: str,
) -> None:
    _refuse_existing_result(
        ledger,
        act=act,
        result_kind=result_event_kind,
        occurrence_coordinate=occurrence_coordinate,
    )
    if ledger.append_boundary_through_occurrence(act.identity) != ledger.append_boundary():
        raise AddressedByteOccurrenceReferenceDeterminationError(
            "determination result requires its exact Act at the append tip"
        )


def _require_yield_at_append_tip(ledger: EventLedger, evidence: Event) -> None:
    if (
        ledger.get(evidence.identity) != evidence
        or evidence.kind != RECORDED_EVIDENCE_OF_YIELD_RELATION_KIND
        or ledger.integrity_of(evidence.identity) == CORRUPTED
        or ledger.append_boundary_through_occurrence(evidence.identity)
        != ledger.append_boundary()
    ):
        raise AddressedByteOccurrenceReferenceDeterminationError(
            "determination result requires exact Yield Evidence at the append tip"
        )


def _record_applicability_yield_evidence(
    ledger: EventLedger,
    *,
    act: Event,
    material: dict[str, Any],
) -> Event:
    return _record_evidence_of_yield_relation(
        ledger,
        locality_identity=act.locality_identity,
        exact_act=APPLICABILITY_ACT,
        act_occurrence_identity=act.material[
            "applicability_act_occurrence_identity"
        ],
        responsible_act_evidence_identity=act.identity,
        result_kind=APPLICABILITY_YIELD_RESULT_KIND,
        result_identity=material["result_identity"],
        result_content=material,
        responsibility=RESPONSIBILITY,
        occurrence_boundary=(
            "addressed_byte_occurrence_reference_determination_applicability"
        ),
        responsible_boundary="this Seed",
        responsible_act_occurrence_coordinate=(
            "applicability_act_occurrence_identity"
        ),
    )


def _record_determination_yield_evidence(
    ledger: EventLedger,
    *,
    act: Event,
    material: dict[str, Any],
) -> Event:
    return _record_evidence_of_yield_relation(
        ledger,
        locality_identity=act.locality_identity,
        exact_act=DETERMINATION_ACT,
        act_occurrence_identity=act.material[
            "determination_act_occurrence_identity"
        ],
        responsible_act_evidence_identity=act.identity,
        result_kind=DETERMINATION_YIELD_RESULT_KIND,
        result_identity=material["result_identity"],
        result_content=material,
        responsibility=RESPONSIBILITY,
        occurrence_boundary="addressed_byte_occurrence_reference_determination",
        responsible_boundary="this Seed",
        responsible_act_occurrence_coordinate=(
            "determination_act_occurrence_identity"
        ),
    )


def _recorded_applicability_result_material(
    material: dict[str, Any], *, act: Event, evidence: Event
) -> dict[str, Any]:
    return {
        "result_identity": material["result_identity"],
        "exact_act": material["exact_act"],
        "applicability_act_identity": material["applicability_act_identity"],
        "applicability_act_occurrence_identity": material[
            "applicability_act_occurrence_identity"
        ],
        "downstream_act_identity": material["downstream_act_identity"],
        "downstream_act_occurrence_identity": material[
            "downstream_act_occurrence_identity"
        ],
        "responsibility": material["responsibility"],
        "responsible_boundary": material["responsible_boundary"],
        "responsibility_assignment_reference": deepcopy(
            material["responsibility_assignment_reference"]
        ),
        "direct_pair_position_result_reference": deepcopy(
            material["direct_pair_position_result_reference"]
        ),
        "addressed_source_byte_position_coordinate_reference": deepcopy(
            material["addressed_source_byte_position_coordinate_reference"]
        ),
        "determination_rule": material["determination_rule"],
        "applicability_finding": deepcopy(material["applicability_finding"]),
        "scope": deepcopy(material["scope"]),
        "authority": deepcopy(material["authority"]),
        "limits": list(material["limits"]),
        "unknown": list(material["unknown"]),
        "responsible_act_evidence_identity": act.identity,
        "evidence_of_yield_relation_identity": evidence.identity,
    }


def record_addressed_byte_occurrence_reference_determination_applicability_result(
    ledger: EventLedger,
    *,
    applicability_act_evidence_event_identity: str,
) -> Event:
    act, assignment, source_result, _references = _read_applicability_act(
        ledger, applicability_act_evidence_event_identity
    )
    material = _applicability_result_material(
        act=act, assignment=assignment, source_result=source_result
    )
    act_material = deepcopy(act.material)
    assignment_material = deepcopy(assignment.material)
    source_material = deepcopy(source_result.material)
    _prepare_result_yield(
        ledger,
        act=act,
        occurrence_coordinate="applicability_act_occurrence_identity",
        result_event_kind=APPLICABILITY_RESULT_KIND,
    )
    act_read, assignment_read, source_read, _references_read = (
        _read_applicability_act(ledger, act.identity)
    )
    for stored, read, kind, material_read, message in (
        (
            act,
            act_read,
            APPLICABILITY_ACT_EVIDENCE_KIND,
            act_material,
            "Applicability Yield requires an intact exact Act",
        ),
        (
            assignment,
            assignment_read,
            RESPONSIBILITY_ASSIGNMENT_KIND,
            assignment_material,
            "Applicability Yield requires an intact exact assignment",
        ),
        (
            source_result,
            source_read,
            BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND,
            source_material,
            "Applicability Yield requires an intact exact source",
        ),
    ):
        _require_unchanged_stored_event(
            ledger,
            event=stored,
            kind=kind,
            material=material_read,
            message=message,
        )
        if read != stored:
            raise AddressedByteOccurrenceReferenceDeterminationError(message)
    _require_stage_at_append_tip(
        ledger, event=act, message="Applicability Act left the append tip"
    )
    evidence = _record_applicability_yield_evidence(
        ledger,
        act=act,
        material=material,
    )
    act_read, assignment_read, source_read, _references_read = (
        _read_applicability_act(ledger, act.identity)
    )
    if (act_read, assignment_read, source_read) != (
        act,
        assignment,
        source_result,
    ):
        raise AddressedByteOccurrenceReferenceDeterminationError(
            "Applicability result requires an intact exact stage"
        )
    for stored, kind, material_read, message in (
        (
            act,
            APPLICABILITY_ACT_EVIDENCE_KIND,
            act_material,
            "Applicability result requires an intact exact Act",
        ),
        (
            assignment,
            RESPONSIBILITY_ASSIGNMENT_KIND,
            assignment_material,
            "Applicability result requires an intact exact assignment",
        ),
        (
            source_result,
            BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND,
            source_material,
            "Applicability result requires an intact exact source",
        ),
    ):
        _require_unchanged_stored_event(
            ledger,
            event=stored,
            kind=kind,
            material=material_read,
            message=message,
        )
    _require_yield_at_append_tip(ledger, evidence)
    return ledger.append(
        APPLICABILITY_RESULT_KIND,
        _recorded_applicability_result_material(
            material, act=act, evidence=evidence
        ),
        locality_identity=act.locality_identity,
    )


def _require_yield(
    ledger: EventLedger,
    *,
    event: Event,
    act: Event,
    occurrence_coordinate: str,
    occurrence_boundary: str,
    result_kind: str,
) -> None:
    evidence_identity = event.material.get("evidence_of_yield_relation_identity")
    evidence = ledger.get(evidence_identity)
    try:
        requirements = read_requirements_of_yield_relation(
            ledger,
            recorded_result_event_identity=event.identity,
            evidence_of_yield_relation_event_identity=evidence_identity,
            responsible_act_evidence_event_identity=act.identity,
            recorded_result_occurrence_coordinate=occurrence_coordinate,
            responsible_act_occurrence_coordinate=occurrence_coordinate,
        )
    except (TypeError, ValueError):
        requirements = {}
    if (
        evidence is None
        or evidence.kind != RECORDED_EVIDENCE_OF_YIELD_RELATION_KIND
        or evidence.locality_identity != event.locality_identity
        or ledger.integrity_of(evidence.identity) == CORRUPTED
        or evidence.material.get("occurrence_boundary") != occurrence_boundary
        or evidence.material.get("result_kind") != result_kind
        or not all(requirements.values())
    ):
        raise AddressedByteOccurrenceReferenceDeterminationError(
            "determination result carries no exact Yield"
        )
    try:
        ordered = ledger.occurrences_in_append_order(
            (act.identity, evidence.identity, event.identity),
            locality_identity=event.locality_identity,
        )
    except ValueError as error:
        raise AddressedByteOccurrenceReferenceDeterminationError(
            "determination result occurrence order is false"
        ) from error
    if tuple(item.identity for item in ordered) != (
        act.identity,
        evidence.identity,
        event.identity,
    ):
        raise AddressedByteOccurrenceReferenceDeterminationError(
            "determination result occurrence order is false"
        )


def _read_applicability_result(
    ledger: EventLedger,
    event_identity: str,
    *,
    prior_standing: dict[str, Any] | None = None,
) -> tuple[
    Event,
    Event,
    Event,
    Event,
    tuple[ReferenceToRecordedPositionOfBytePairOccurrence, ...],
]:
    event = ledger.get(event_identity)
    if (
        event is None
        or event.kind != APPLICABILITY_RESULT_KIND
        or event.exact_material is not None
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise AddressedByteOccurrenceReferenceDeterminationError(
            "determination Applicability result is absent or corrupted"
        )
    act, assignment, source_result, references = _read_applicability_act(
        ledger,
        event.material.get("responsible_act_evidence_identity"),
        prior_standing=prior_standing,
    )
    expected = {
        **_applicability_result_material(
            act=act, assignment=assignment, source_result=source_result
        ),
        "responsible_act_evidence_identity": act.identity,
        "evidence_of_yield_relation_identity": event.material.get(
            "evidence_of_yield_relation_identity"
        ),
    }
    if event.locality_identity != act.locality_identity or event.material != expected:
        raise AddressedByteOccurrenceReferenceDeterminationError(
            "determination Applicability result coordinates are not exact"
        )
    _require_yield(
        ledger,
        event=event,
        act=act,
        occurrence_coordinate="applicability_act_occurrence_identity",
        occurrence_boundary=APPLICABILITY_BOUNDARY,
        result_kind=APPLICABILITY_YIELD_RESULT_KIND,
    )
    return event, act, assignment, source_result, references


def get_recorded_addressed_byte_occurrence_reference_determination_applicability(
    ledger: EventLedger, event_identity: str
) -> dict[str, Any]:
    return deepcopy(_read_applicability_result(ledger, event_identity)[0].material)


def _determination_act_material(
    *, assignment: Event, source_result: Event, applicability_result: Event
) -> dict[str, Any]:
    return {
        "determination_act_identity": assignment.material[
            "determination_act_identity"
        ],
        "determination_act_occurrence_identity": assignment.material[
            "determination_act_occurrence_identity"
        ],
        "act": DETERMINATION_ACT,
        "responsibility": RESPONSIBILITY,
        "responsible_boundary": "this Seed",
        "responsibility_assignment_reference": _assignment_reference(assignment),
        "applicability_result_reference": _applicability_result_reference(
            applicability_result
        ),
        "direct_pair_position_result_reference": _direct_result_reference(
            source_result
        ),
        "addressed_source_byte_position_coordinate_reference": deepcopy(
            assignment.material[
                "addressed_source_byte_position_coordinate_reference"
            ]
        ),
        "determination_rule": DETERMINATION_RULE,
        "result_identity": assignment.material["determination_result_identity"],
        "scope": deepcopy(assignment.material["scope"]),
        "authority": deepcopy(assignment.material["authority"]),
        "evidence_scope": "Evidence for this exact declared Measurement Act occurrence",
        "limits": list(assignment.material["limits"]),
        "unknown": list(assignment.material["unknown"]),
    }


def record_addressed_byte_occurrence_reference_determination_act_evidence(
    ledger: EventLedger,
    *,
    applicability_result_event_identity: str,
    applicability_standing: dict[str, Any],
) -> Event:
    applicability, app_act, assignment, source_result, _references = (
        _read_applicability_result(ledger, applicability_result_event_identity)
    )
    _require_stage_standing(
        ledger,
        standing=applicability_standing,
        source_result=source_result,
        assignment=assignment,
        applicability_result=applicability,
    )
    applicability_material = deepcopy(applicability.material)
    app_act_material = deepcopy(app_act.material)
    assignment_material = deepcopy(assignment.material)
    source_material = deepcopy(source_result.material)
    _refuse_existing_act(
        ledger,
        assignment=assignment,
        kind=DETERMINATION_ACT_EVIDENCE_KIND,
        occurrence_coordinate="determination_act_occurrence_identity",
    )
    (
        applicability_read,
        app_act_read,
        assignment_read,
        source_read,
        _references_read,
    ) = _read_applicability_result(ledger, applicability.identity)
    for stored, read, kind, material_read, message in (
        (
            applicability,
            applicability_read,
            APPLICABILITY_RESULT_KIND,
            applicability_material,
            "determination Measurement Act requires an intact exact Applicability",
        ),
        (
            app_act,
            app_act_read,
            APPLICABILITY_ACT_EVIDENCE_KIND,
            app_act_material,
            "determination Measurement Act requires an intact exact Applicability Act",
        ),
        (
            assignment,
            assignment_read,
            RESPONSIBILITY_ASSIGNMENT_KIND,
            assignment_material,
            "determination Measurement Act requires an intact exact assignment",
        ),
        (
            source_result,
            source_read,
            BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND,
            source_material,
            "determination Measurement Act requires an intact exact source",
        ),
    ):
        _require_unchanged_stored_event(
            ledger,
            event=stored,
            kind=kind,
            material=material_read,
            message=message,
        )
        if read != stored:
            raise AddressedByteOccurrenceReferenceDeterminationError(message)
    _require_stage_at_append_tip(
        ledger,
        event=applicability,
        message="determination Measurement Applicability left the append tip",
    )
    return ledger.append(
        DETERMINATION_ACT_EVIDENCE_KIND,
        _determination_act_material(
            assignment=assignment,
            source_result=source_result,
            applicability_result=applicability,
        ),
        locality_identity=assignment.locality_identity,
    )


def _read_determination_act(
    ledger: EventLedger,
    event_identity: str,
    *,
    prior_standing: dict[str, Any] | None = None,
) -> tuple[
    Event,
    Event,
    Event,
    Event,
    tuple[ReferenceToRecordedPositionOfBytePairOccurrence, ...],
]:
    event = ledger.get(event_identity)
    if (
        event is None
        or event.kind != DETERMINATION_ACT_EVIDENCE_KIND
        or event.exact_material is not None
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise AddressedByteOccurrenceReferenceDeterminationError(
            "determination Act Evidence is absent or corrupted"
        )
    applicability_reference = event.material.get("applicability_result_reference")
    applicability_identity = (
        applicability_reference.get("recorded_occurrence_identity")
        if type(applicability_reference) is dict
        else None
    )
    applicability, _app_act, assignment, source_result, references = (
        _read_applicability_result(
            ledger, applicability_identity, prior_standing=prior_standing
        )
    )
    if (
        applicability_reference != _applicability_result_reference(applicability)
        or event.locality_identity != assignment.locality_identity
        or event.material
        != _determination_act_material(
            assignment=assignment,
            source_result=source_result,
            applicability_result=applicability,
        )
    ):
        raise AddressedByteOccurrenceReferenceDeterminationError(
            "determination Act Evidence coordinates are not exact"
        )
    try:
        ledger.occurrences_in_append_order(
            (applicability.identity, event.identity),
            locality_identity=event.locality_identity,
        )
    except ValueError as error:
        raise AddressedByteOccurrenceReferenceDeterminationError(
            "determination Act order is false"
        ) from error
    return event, applicability, assignment, source_result, references


def get_addressed_byte_occurrence_reference_determination_act_evidence(
    ledger: EventLedger, event_identity: str
) -> Event:
    return _read_determination_act(ledger, event_identity)[0]


def _determination_result_material(
    *,
    act: Event,
    applicability: Event,
    assignment: Event,
    source_result: Event,
    references: tuple[ReferenceToRecordedPositionOfBytePairOccurrence, ...],
) -> dict[str, Any]:
    return {
        "result_identity": assignment.material["determination_result_identity"],
        "exact_act": DETERMINATION_ACT,
        "determination_act_identity": assignment.material[
            "determination_act_identity"
        ],
        "determination_act_occurrence_identity": assignment.material[
            "determination_act_occurrence_identity"
        ],
        "responsibility": RESPONSIBILITY,
        "responsible_boundary": "this Seed",
        "responsibility_assignment_reference": _assignment_reference(assignment),
        "applicability_result_reference": _applicability_result_reference(
            applicability
        ),
        "direct_pair_position_result_reference": _direct_result_reference(
            source_result
        ),
        "addressed_source_byte_position_coordinate_reference": deepcopy(
            assignment.material[
                "addressed_source_byte_position_coordinate_reference"
            ]
        ),
        "determination_rule": DETERMINATION_RULE,
        "completeness_boundary": {
            "identity": assignment.material["scope"][
                "completeness_boundary_identity"
            ]
        },
        "ordered_assertion_references": [
            reference.assertion_reference for reference in references
        ],
        "limits": list(assignment.material["limits"]),
        "unknown": list(assignment.material["unknown"]),
    }


def _recorded_determination_result_material(
    material: dict[str, Any], *, act: Event, evidence: Event
) -> dict[str, Any]:
    return {
        "result_identity": material["result_identity"],
        "exact_act": material["exact_act"],
        "determination_act_identity": material["determination_act_identity"],
        "determination_act_occurrence_identity": material[
            "determination_act_occurrence_identity"
        ],
        "responsibility": material["responsibility"],
        "responsible_boundary": material["responsible_boundary"],
        "responsibility_assignment_reference": deepcopy(
            material["responsibility_assignment_reference"]
        ),
        "applicability_result_reference": deepcopy(
            material["applicability_result_reference"]
        ),
        "direct_pair_position_result_reference": deepcopy(
            material["direct_pair_position_result_reference"]
        ),
        "addressed_source_byte_position_coordinate_reference": deepcopy(
            material["addressed_source_byte_position_coordinate_reference"]
        ),
        "determination_rule": material["determination_rule"],
        "completeness_boundary": deepcopy(material["completeness_boundary"]),
        "ordered_assertion_references": deepcopy(
            material["ordered_assertion_references"]
        ),
        "limits": list(material["limits"]),
        "unknown": list(material["unknown"]),
        "responsible_act_evidence_identity": act.identity,
        "evidence_of_yield_relation_identity": evidence.identity,
    }


def record_addressed_byte_occurrence_reference_determination_result(
    ledger: EventLedger,
    *,
    determination_act_evidence_event_identity: str,
) -> Event:
    act, applicability, assignment, source_result, references = (
        _read_determination_act(
            ledger, determination_act_evidence_event_identity
        )
    )
    material = _determination_result_material(
        act=act,
        applicability=applicability,
        assignment=assignment,
        source_result=source_result,
        references=references,
    )
    act_material = deepcopy(act.material)
    applicability_material = deepcopy(applicability.material)
    assignment_material = deepcopy(assignment.material)
    source_material = deepcopy(source_result.material)
    _prepare_result_yield(
        ledger,
        act=act,
        occurrence_coordinate="determination_act_occurrence_identity",
        result_event_kind=DETERMINATION_RESULT_KIND,
    )
    (
        act_read,
        applicability_read,
        assignment_read,
        source_read,
        _references_read,
    ) = _read_determination_act(ledger, act.identity)
    for stored, read, kind, material_read, message in (
        (
            act,
            act_read,
            DETERMINATION_ACT_EVIDENCE_KIND,
            act_material,
            "determination Measurement Yield requires an intact exact Act",
        ),
        (
            applicability,
            applicability_read,
            APPLICABILITY_RESULT_KIND,
            applicability_material,
            "determination Measurement Yield requires an intact exact Applicability",
        ),
        (
            assignment,
            assignment_read,
            RESPONSIBILITY_ASSIGNMENT_KIND,
            assignment_material,
            "determination Measurement Yield requires an intact exact assignment",
        ),
        (
            source_result,
            source_read,
            BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND,
            source_material,
            "determination Measurement Yield requires an intact exact source",
        ),
    ):
        _require_unchanged_stored_event(
            ledger,
            event=stored,
            kind=kind,
            material=material_read,
            message=message,
        )
        if read != stored:
            raise AddressedByteOccurrenceReferenceDeterminationError(message)
    _require_stage_at_append_tip(
        ledger,
        event=act,
        message="determination Measurement Act left the append tip",
    )
    evidence = _record_determination_yield_evidence(
        ledger,
        act=act,
        material=material,
    )
    (
        act_read,
        applicability_read,
        assignment_read,
        source_read,
        _references_read,
    ) = _read_determination_act(ledger, act.identity)
    if (act_read, applicability_read, assignment_read, source_read) != (
        act,
        applicability,
        assignment,
        source_result,
    ):
        raise AddressedByteOccurrenceReferenceDeterminationError(
            "determination Measurement result requires an intact exact stage"
        )
    for stored, kind, material_read, message in (
        (
            act,
            DETERMINATION_ACT_EVIDENCE_KIND,
            act_material,
            "determination Measurement result requires an intact exact Act",
        ),
        (
            applicability,
            APPLICABILITY_RESULT_KIND,
            applicability_material,
            "determination Measurement result requires an intact exact Applicability",
        ),
        (
            assignment,
            RESPONSIBILITY_ASSIGNMENT_KIND,
            assignment_material,
            "determination Measurement result requires an intact exact assignment",
        ),
        (
            source_result,
            BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND,
            source_material,
            "determination Measurement result requires an intact exact source",
        ),
    ):
        _require_unchanged_stored_event(
            ledger,
            event=stored,
            kind=kind,
            material=material_read,
            message=message,
        )
    _require_yield_at_append_tip(ledger, evidence)
    return ledger.append(
        DETERMINATION_RESULT_KIND,
        _recorded_determination_result_material(
            material, act=act, evidence=evidence
        ),
        locality_identity=act.locality_identity,
    )


def _read_determination_result(
    ledger: EventLedger,
    event_identity: str,
    *,
    prior_standing: dict[str, Any] | None = None,
) -> tuple[
    Event,
    Event,
    Event,
    Event,
    Event,
    tuple[ReferenceToRecordedPositionOfBytePairOccurrence, ...],
]:
    event = ledger.get(event_identity)
    if (
        event is None
        or event.kind != DETERMINATION_RESULT_KIND
        or event.exact_material is not None
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise AddressedByteOccurrenceReferenceDeterminationError(
            "determination result is absent or corrupted"
        )
    act, applicability, assignment, source_result, references = (
        _read_determination_act(
            ledger,
            event.material.get("responsible_act_evidence_identity"),
            prior_standing=prior_standing,
        )
    )
    expected = {
        **_determination_result_material(
            act=act,
            applicability=applicability,
            assignment=assignment,
            source_result=source_result,
            references=references,
        ),
        "responsible_act_evidence_identity": act.identity,
        "evidence_of_yield_relation_identity": event.material.get(
            "evidence_of_yield_relation_identity"
        ),
    }
    if event.locality_identity != act.locality_identity or event.material != expected:
        raise AddressedByteOccurrenceReferenceDeterminationError(
            "determination result coordinates are not exact"
        )
    _require_yield(
        ledger,
        event=event,
        act=act,
        occurrence_coordinate="determination_act_occurrence_identity",
        occurrence_boundary=DETERMINATION_BOUNDARY,
        result_kind=DETERMINATION_YIELD_RESULT_KIND,
    )
    return event, act, applicability, assignment, source_result, references


def get_recorded_addressed_byte_occurrence_reference_determination(
    ledger: EventLedger, event_identity: str
) -> dict[str, Any]:
    return deepcopy(_read_determination_result(ledger, event_identity)[0].material)


def _record_addressed_byte_occurrence_reference_determination_lifecycle_from_carried_standing(
    ledger: EventLedger,
    *,
    direct_result_event_identity: str,
    addressed_source_byte_position_coordinate_reference: dict[str, Any],
    locality_standing: dict[str, Any],
) -> tuple[dict[str, Any], Event]:
    """Record one D.2 lifecycle while carrying its exact stage readings."""

    from seed_runtime.operator_locality_standing import (
        _exact_standing_additions,
        _record_distinct,
    )

    if not isinstance(ledger, EventLedger):
        raise TypeError("determination lifecycle requires one EventLedger")
    standing = deepcopy(locality_standing)
    locality_identity = standing.get("locality_identity")
    boundary = standing.get("through_event_occurrence_identity")
    source_result, references = _source(
        ledger,
        result_event_identity=_identity(
            direct_result_event_identity,
            "determination lifecycle requires one direct result",
        ),
        coordinate_reference=(
            addressed_source_byte_position_coordinate_reference
        ),
    )
    _standing_carries_source(
        ledger,
        standing=standing,
        source_result=source_result,
        required_boundary_identity=boundary,
    )
    _require_stage_at_append_tip(
        ledger,
        event=ledger.get(boundary),
        message="determination assignment Standing left the append tip",
    )
    source_material = deepcopy(source_result.material)
    identities = {
        name: new_identity(prefix)
        for name, prefix in (
            (
                "assignment_identity",
                "addressed_byte_occurrence_reference_assignment",
            ),
            (
                "assignment_subject_identity",
                "addressed_byte_occurrence_reference_assignment_subject",
            ),
            (
                "applicability_act_identity",
                "addressed_byte_occurrence_reference_applicability_act",
            ),
            (
                "applicability_act_occurrence_identity",
                "addressed_byte_occurrence_reference_applicability_act_occurrence",
            ),
            (
                "applicability_result_identity",
                "addressed_byte_occurrence_reference_applicability_result",
            ),
            (
                "determination_act_identity",
                "addressed_byte_occurrence_reference_determination_measurement_act",
            ),
            (
                "determination_act_occurrence_identity",
                "addressed_byte_occurrence_reference_determination_measurement_act_occurrence",
            ),
            (
                "determination_result_identity",
                "addressed_byte_occurrence_reference_determination_measurement_result",
            ),
        )
    }
    if len(set(identities.values())) != len(identities):
        raise AddressedByteOccurrenceReferenceDeterminationError(
            "determination lifecycle identities collapsed"
        )

    exact_stage_material: list[tuple[Event, str, dict[str, Any]]] = [
        (
            source_result,
            BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND,
            source_material,
        )
    ]

    def require_intact() -> None:
        for event, kind, material in exact_stage_material:
            _require_unchanged_stored_event(
                ledger,
                event=event,
                kind=kind,
                material=material,
                message="determination requires each carried stage intact",
            )

    def require_prior_at_tip(event: Event) -> None:
        require_intact()
        _require_stage_at_append_tip(
            ledger,
            event=event,
            message="determination carried stage left the append tip",
        )

    def carry(event: Event, *, prior: str) -> None:
        assignments = standing.get("responsibility_assignment_occurrences")
        applicability_results = standing.get("applicability_result_occurrences")
        measurements = standing.get("measurement_occurrences")
        count = standing.get("event_count")
        if (
            type(assignments) is not dict
            or type(applicability_results) is not dict
            or type(measurements) is not dict
            or type(count) is not int
            or standing.get("through_event_occurrence_identity") != prior
            or event.locality_identity != locality_identity
            or ledger.get(event.identity) != event
            or ledger.integrity_of(event.identity) == CORRUPTED
            or ledger.append_boundary_through_occurrence(event.identity)
            != ledger.append_boundary()
        ):
            raise AddressedByteOccurrenceReferenceDeterminationError(
                "produced determination occurrence is not exact"
            )
        if event.kind == RESPONSIBILITY_ASSIGNMENT_KIND:
            lawful = (
                event.material.get("standing_boundary_identity") == prior
                and event.identity not in assignments
            )
        elif event.kind == APPLICABILITY_ACT_EVIDENCE_KIND:
            lawful = (
                event.material["responsibility_assignment_reference"][
                    "recorded_occurrence_identity"
                ]
                == prior
                and prior in assignments
            )
        elif event.kind == APPLICABILITY_RESULT_KIND:
            lawful = (
                event.material.get("responsible_act_evidence_identity") == prior
                and event.material["responsibility_assignment_reference"][
                    "recorded_occurrence_identity"
                ]
                in assignments
                and event.identity not in applicability_results
            )
        elif event.kind == DETERMINATION_ACT_EVIDENCE_KIND:
            lawful = (
                event.material["applicability_result_reference"][
                    "recorded_occurrence_identity"
                ]
                == prior
                and prior in applicability_results
            )
        elif event.kind == DETERMINATION_RESULT_KIND:
            lawful = (
                event.material.get("responsible_act_evidence_identity") == prior
                and event.identity not in measurements
            )
        else:
            lawful = False
        if not lawful:
            raise AddressedByteOccurrenceReferenceDeterminationError(
                "produced determination occurrence has false Standing"
            )
        additions = _exact_standing_additions(
            standing,
            event,
            error_message="produced determination Standing is not exact",
        )
        if event.kind == RESPONSIBILITY_ASSIGNMENT_KIND:
            assignments[event.identity] = None
        elif event.kind == APPLICABILITY_RESULT_KIND:
            applicability_results[event.identity] = None
        elif event.kind == DETERMINATION_RESULT_KIND:
            measurements[event.identity] = _determination_result_reference(event)
        for key, values in additions.items():
            for value in values:
                _record_distinct(standing[key], value)
        standing["through_event_occurrence_identity"] = event.identity
        standing["event_count"] = count + 1

    assignment_material = _assignment_material(
        source_result=source_result,
        coordinate_reference=(
            addressed_source_byte_position_coordinate_reference
        ),
        standing_boundary_identity=boundary,
        identities=identities,
    )
    require_prior_at_tip(ledger.get(boundary))
    assignment = ledger.append(
        RESPONSIBILITY_ASSIGNMENT_KIND,
        _assignment_material(
            source_result=source_result,
            coordinate_reference=(
                addressed_source_byte_position_coordinate_reference
            ),
            standing_boundary_identity=boundary,
            identities=identities,
        ),
        locality_identity=locality_identity,
    )
    exact_stage_material.append(
        (
            assignment,
            RESPONSIBILITY_ASSIGNMENT_KIND,
            assignment_material,
        )
    )
    require_intact()
    carry(assignment, prior=boundary)

    _refuse_existing_act(
        ledger,
        assignment=assignment,
        kind=APPLICABILITY_ACT_EVIDENCE_KIND,
        occurrence_coordinate="applicability_act_occurrence_identity",
    )
    applicability_act_material = _applicability_act_material(
        assignment=assignment, source_result=source_result
    )
    require_prior_at_tip(assignment)
    applicability_act = ledger.append(
        APPLICABILITY_ACT_EVIDENCE_KIND,
        _applicability_act_material(
            assignment=assignment,
            source_result=source_result,
        ),
        locality_identity=locality_identity,
    )
    exact_stage_material.append(
        (
            applicability_act,
            APPLICABILITY_ACT_EVIDENCE_KIND,
            applicability_act_material,
        )
    )
    require_intact()
    carry(applicability_act, prior=assignment.identity)

    applicability_material = _applicability_result_material(
        act=applicability_act,
        assignment=assignment,
        source_result=source_result,
    )
    _prepare_result_yield(
        ledger,
        act=applicability_act,
        occurrence_coordinate="applicability_act_occurrence_identity",
        result_event_kind=APPLICABILITY_RESULT_KIND,
    )
    require_prior_at_tip(applicability_act)
    applicability_evidence = _record_applicability_yield_evidence(
        ledger,
        act=applicability_act,
        material=applicability_material,
    )
    exact_stage_material.append(
        (
            applicability_evidence,
            RECORDED_EVIDENCE_OF_YIELD_RELATION_KIND,
            deepcopy(applicability_evidence.material),
        )
    )
    require_intact()
    _require_yield_at_append_tip(ledger, applicability_evidence)
    applicability_recorded = _recorded_applicability_result_material(
        applicability_material,
        act=applicability_act,
        evidence=applicability_evidence,
    )
    applicability = ledger.append(
        APPLICABILITY_RESULT_KIND,
        _recorded_applicability_result_material(
            applicability_material,
            act=applicability_act,
            evidence=applicability_evidence,
        ),
        locality_identity=locality_identity,
    )
    exact_stage_material.append(
        (applicability, APPLICABILITY_RESULT_KIND, applicability_recorded)
    )
    require_intact()
    carry(applicability, prior=applicability_act.identity)

    _refuse_existing_act(
        ledger,
        assignment=assignment,
        kind=DETERMINATION_ACT_EVIDENCE_KIND,
        occurrence_coordinate="determination_act_occurrence_identity",
    )
    act_material = _determination_act_material(
        assignment=assignment,
        source_result=source_result,
        applicability_result=applicability,
    )
    require_prior_at_tip(applicability)
    act = ledger.append(
        DETERMINATION_ACT_EVIDENCE_KIND,
        _determination_act_material(
            assignment=assignment,
            source_result=source_result,
            applicability_result=applicability,
        ),
        locality_identity=locality_identity,
    )
    exact_stage_material.append(
        (act, DETERMINATION_ACT_EVIDENCE_KIND, act_material)
    )
    require_intact()
    carry(act, prior=applicability.identity)

    result_material = _determination_result_material(
        act=act,
        applicability=applicability,
        assignment=assignment,
        source_result=source_result,
        references=references,
    )
    _prepare_result_yield(
        ledger,
        act=act,
        occurrence_coordinate="determination_act_occurrence_identity",
        result_event_kind=DETERMINATION_RESULT_KIND,
    )
    require_prior_at_tip(act)
    evidence = _record_determination_yield_evidence(
        ledger,
        act=act,
        material=result_material,
    )
    exact_stage_material.append(
        (
            evidence,
            RECORDED_EVIDENCE_OF_YIELD_RELATION_KIND,
            deepcopy(evidence.material),
        )
    )
    require_intact()
    _require_yield_at_append_tip(ledger, evidence)
    result_recorded = _recorded_determination_result_material(
        result_material,
        act=act,
        evidence=evidence,
    )
    result = ledger.append(
        DETERMINATION_RESULT_KIND,
        _recorded_determination_result_material(
            result_material,
            act=act,
            evidence=evidence,
        ),
        locality_identity=locality_identity,
    )
    exact_stage_material.append(
        (result, DETERMINATION_RESULT_KIND, result_recorded)
    )
    require_intact()
    carry(result, prior=act.identity)
    return standing, result
