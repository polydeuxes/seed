"""Record one complete Candidate Standing over exact result Assertions."""

from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from typing import Any

from seed_runtime.event import Event
from seed_runtime.events import CORRUPTED, EventLedger, EventLedgerBoundary
from seed_runtime.evidence_of_yield_relation import (
    _record_evidence_of_yield_relation,
    read_requirements_of_yield_relation,
)
from seed_runtime.identities import new_identity
from seed_runtime.measurement_of_position_coordinates_of_byte_pair_occurrences import (
    BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND,
    _recorded_position_assertion_coordinates_for_locality_movement,
    references_to_recorded_position_coordinates_of_byte_pair_occurrences,
)


CANDIDATE_STANDING_RESPONSIBILITY_ASSIGNMENT_KIND = (
    "operator.candidate_standing.responsibility_assignment_recorded"
)
CANDIDATE_STANDING_APPLICABILITY_ACT_EVIDENCE_KIND = (
    "operator.candidate_standing.applicability_act_evidenced"
)
CANDIDATE_STANDING_APPLICABILITY_RESULT_KIND = (
    "operator.candidate_standing.applicability_recorded"
)
CANDIDATE_STANDING_ACT_EVIDENCE_KIND = (
    "operator.candidate_standing.act_evidenced"
)
CANDIDATE_STANDING_RESULT_KIND = "operator.candidate_standing.recorded"

BOOK_CLAUSE = "01.Source.E.1"
ONE_SOURCE_CANDIDATE_RESPONSIBILITY = (
    "determine Applicability and record one Candidate for each exact source "
    "Assertion through one exact ledger boundary"
)
ORDERED_PAIR_CANDIDATE_RESPONSIBILITY = (
    "determine Applicability and record one Candidate for each distinct ordered "
    "source Assertion pair through one exact ledger boundary"
)
_CANDIDATE_RESPONSIBILITIES = frozenset(
    (
        ONE_SOURCE_CANDIDATE_RESPONSIBILITY,
        ORDERED_PAIR_CANDIDATE_RESPONSIBILITY,
    )
)
APPLICABILITY_ACT = (
    "determine Applicability of every exact source Assertion carried through the "
    "exact source ledger boundary"
)
ONE_SOURCE_CANDIDATE_ACT = (
    "record one Candidate for each exact source Assertion in event order"
)
ORDERED_PAIR_CANDIDATE_ACT = (
    "record one Candidate for each distinct ordered source Assertion pair in source "
    "event order"
)
APPLICABILITY_RESULT_NAME = (
    "Applicability result for exact Candidate Standing source Assertions"
)
CANDIDATE_RESULT_NAME = "complete Candidate Standing result"
CANDIDATE_ASSERTION_RESPONSIBILITY = (
    "preserve this Candidate Assertion's carried Standing coordinates"
)

EVENT_KIND_RESPONSIBILITIES = {
    CANDIDATE_STANDING_RESPONSIBILITY_ASSIGNMENT_KIND: "01.Source.E.1",
    CANDIDATE_STANDING_APPLICABILITY_ACT_EVIDENCE_KIND: "02.Acts.A",
    CANDIDATE_STANDING_APPLICABILITY_RESULT_KIND: "01.Standing.E.1",
    CANDIDATE_STANDING_ACT_EVIDENCE_KIND: "02.Acts.A",
    CANDIDATE_STANDING_RESULT_KIND: "01.Source.E.1",
}
ASSERTION_RESPONSIBILITIES = {
    CANDIDATE_ASSERTION_RESPONSIBILITY: "01.Standing.D.1",
}

_SOURCE_STANDING_COORDINATES = (
    "measurement_occurrences",
    "comparison_result_occurrences",
    "candidate_result_occurrences",
)
_SOURCE_ASSERTION_COORDINATES = (
    "source_Assertion_reference",
    "source_Locality",
    "source_Standing_boundary",
    "Evidence",
    "Authority",
    "Scope",
    "limits",
    "Unknown",
)


def _identity(value: Any, message: str) -> str:
    if type(value) is not str or not value:
        raise ValueError(message)
    return value


def _candidate_responsibility(value: Any) -> str:
    if value not in _CANDIDATE_RESPONSIBILITIES:
        raise ValueError("Candidate Standing requires one exact Responsibility")
    return value


def _candidate_act_for_responsibility(responsibility: str) -> str:
    exact = _candidate_responsibility(responsibility)
    if exact == ONE_SOURCE_CANDIDATE_RESPONSIBILITY:
        return ONE_SOURCE_CANDIDATE_ACT
    return ORDERED_PAIR_CANDIDATE_ACT


def _event(
    ledger: EventLedger,
    event_identity: Any,
    *,
    kind: str,
    message: str,
) -> Event:
    event = ledger.get(_identity(event_identity, message))
    if (
        event is None
        or event.kind != kind
        or event.exact_material is not None
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise ValueError(message)
    return event


def _canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def _boundary(ledger: EventLedger, identity: Any) -> EventLedgerBoundary:
    exact = EventLedgerBoundary(
        _identity(identity, "Candidate Standing requires one exact source boundary")
    )
    ledger.list(through=exact)
    return exact


def _assertion_identity(assertion: Any, message: str) -> str:
    if type(assertion) is not dict:
        raise ValueError(message)
    dimensions = assertion.get("dimensions")
    identity = (
        dimensions.get("identity") if type(dimensions) is dict else None
    )
    if type(identity) is not str or not identity:
        identity = assertion.get("identity")
    return _identity(identity, message)


def _source_assertion_reference(
    event: Event,
    *,
    standing_coordinate: str,
    assertion_coordinate: str,
    assertion_identity: str,
    source_assertion_coordinates: dict[str, Any],
    source_standing_through_event_occurrence_identity: str,
) -> dict[str, Any]:
    return {
        "recorded_result_occurrence_identity": event.identity,
        "recorded_result_occurrence_kind": event.kind,
        "assertion_identity": assertion_identity,
        "assertion_coordinate": assertion_coordinate,
        "source_locality_identity": event.locality_identity,
        "source_standing_coordinate": standing_coordinate,
        "source_standing_through_event_occurrence_identity": (
            source_standing_through_event_occurrence_identity
        ),
        "source_assertion_coordinates": deepcopy(source_assertion_coordinates),
    }


def _source_coordinates(event: Event, assertion: dict[str, Any] | None) -> dict[str, Any]:
    """Carry source coordinates without assigning them to Production."""

    if assertion is None:
        return {
            "Evidence": event.material.get("evidence_of_yield_relation_identity"),
            "Authority": deepcopy(event.material.get("authority")),
            "Scope": deepcopy(event.material.get("scope")),
            "limits": deepcopy(event.material.get("limits")),
            "Unknown": deepcopy(event.material.get("unknown")),
        }
    dimensions = assertion.get("dimensions")
    return {
        "Evidence": deepcopy(
            dimensions.get("evidence_scope")
            if type(dimensions) is dict
            else assertion.get("evidence_scope")
        ),
        "Authority": deepcopy(
            dimensions.get("authority")
            if type(dimensions) is dict
            else assertion.get("authority")
        ),
        "Scope": deepcopy(assertion.get("assertion_scope")),
        "limits": deepcopy(assertion.get("limits")),
        "Unknown": deepcopy(assertion.get("unknown")),
    }


def _references_carried_by_result(
    ledger: EventLedger,
    event: Event,
    *,
    standing_coordinate: str,
    source_standing_through_event_occurrence_identity: str,
) -> list[dict[str, Any]]:
    material = event.material
    references = []
    result_identity = material.get("result_identity")
    if type(result_identity) is str and result_identity:
        references.append(
            _source_assertion_reference(
                event,
                standing_coordinate=standing_coordinate,
                assertion_coordinate="result",
                assertion_identity=result_identity,
                source_assertion_coordinates=_source_coordinates(event, None),
                source_standing_through_event_occurrence_identity=(
                    source_standing_through_event_occurrence_identity
                ),
            )
        )

    assertions = material.get("assertions")
    if type(assertions) is list:
        for position, assertion in enumerate(assertions):
            references.append(
                _source_assertion_reference(
                    event,
                    standing_coordinate=standing_coordinate,
                    assertion_coordinate=f"assertions/{position}",
                    assertion_identity=_assertion_identity(
                        assertion,
                        "Candidate Standing requires exact Assertions carried by a result",
                    ),
                    source_assertion_coordinates=_source_coordinates(
                        event, assertion
                    ),
                    source_standing_through_event_occurrence_identity=(
                        source_standing_through_event_occurrence_identity
                    ),
                )
            )
    elif type(assertions) is dict:
        try:
            assertion_identity = _assertion_identity(
                assertions,
                "Candidate Standing requires exact Assertions carried by a result",
            )
        except ValueError:
            assertion_identity = None
        if assertion_identity is not None:
            references.append(
                _source_assertion_reference(
                    event,
                    standing_coordinate=standing_coordinate,
                    assertion_coordinate="assertions",
                    assertion_identity=assertion_identity,
                    source_assertion_coordinates=_source_coordinates(
                        event, assertions
                    ),
                    source_standing_through_event_occurrence_identity=(
                        source_standing_through_event_occurrence_identity
                    ),
                )
            )
    elif assertions is not None:
        raise ValueError(
            "Candidate Standing requires exact Assertions carried by a result"
        )

    if event.kind == BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND:
        for position, reference in enumerate(
            references_to_recorded_position_coordinates_of_byte_pair_occurrences(
                ledger, event.identity
            )
        ):
            references.append(
                _source_assertion_reference(
                    event,
                    standing_coordinate=standing_coordinate,
                    assertion_coordinate=f"position_assertions/{position}",
                    assertion_identity=reference.assertion_identity,
                    source_assertion_coordinates=(
                        _recorded_position_assertion_coordinates_for_locality_movement(
                            ledger,
                            result_event_identity=event.identity,
                            assertion_identity=reference.assertion_identity,
                        )
                    ),
                    source_standing_through_event_occurrence_identity=(
                        source_standing_through_event_occurrence_identity
                    ),
                )
            )

    finding = material.get("finding")
    if finding is not None:
        references.append(
            _source_assertion_reference(
                event,
                standing_coordinate=standing_coordinate,
                assertion_coordinate="finding",
                assertion_identity=_assertion_identity(
                    finding,
                    "Candidate Standing requires one exact finding Assertion",
                ),
                source_assertion_coordinates=_source_coordinates(event, finding),
                source_standing_through_event_occurrence_identity=(
                    source_standing_through_event_occurrence_identity
                ),
            )
        )

    if event.kind == CANDIDATE_STANDING_RESULT_KIND:
        candidate_assertions = material.get("candidate_assertions")
        if type(candidate_assertions) is not list:
            raise ValueError(
                "Candidate Standing requires exact Candidate Assertions carried by a result"
            )
        for position, assertion in enumerate(candidate_assertions):
            references.append(
                _source_assertion_reference(
                    event,
                    standing_coordinate=standing_coordinate,
                    assertion_coordinate=f"candidate_assertions/{position}",
                    assertion_identity=_assertion_identity(
                        assertion,
                        "Candidate Standing requires exact Candidate Assertions carried by a result",
                    ),
                    source_assertion_coordinates=_source_coordinates(
                        event, assertion
                    ),
                    source_standing_through_event_occurrence_identity=(
                        source_standing_through_event_occurrence_identity
                    ),
                )
            )
    return references


def _source_assertion_references_through(
    ledger: EventLedger, boundary: EventLedgerBoundary
) -> list[dict[str, str]]:
    """Read the exact source Assertion coordinates through one ledger boundary."""

    events = ledger.list(through=boundary)
    positions = {event.identity: position for position, event in enumerate(events)}
    locality_events: dict[str, list[str]] = {}
    for event in events:
        locality_events.setdefault(event.locality_identity, []).append(event.identity)

    # The import is local because Locality Standing imports this module to
    # validate and carry the resulting Candidate Standing occurrences.
    from seed_runtime.operator_locality_standing import (
        advance_operator_locality_standing,
    )

    ordered: list[tuple[int, int, dict[str, str]]] = []
    for locality_identity, event_identities in locality_events.items():
        standing = advance_operator_locality_standing(
            ledger,
            event_identities,
            locality_identity=locality_identity,
        )
        standing_boundary_identity = standing.get(
            "through_event_occurrence_identity"
        )
        if standing_boundary_identity is None:
            continue
        _identity(
            standing_boundary_identity,
            "Candidate Standing requires one exact source Standing boundary",
        )
        for standing_coordinate in _SOURCE_STANDING_COORDINATES:
            result_occurrences = standing.get(standing_coordinate)
            if type(result_occurrences) is not dict:
                raise ValueError(
                    "Candidate Standing requires exact result Assertion Standing"
                )
            for result_occurrence_identity in result_occurrences:
                event = ledger.get(result_occurrence_identity)
                position = positions.get(result_occurrence_identity)
                if (
                    event is None
                    or position is None
                    or event.locality_identity != locality_identity
                    or ledger.integrity_of(event.identity) == CORRUPTED
                ):
                    raise ValueError(
                        "Candidate Standing requires intact source result occurrences"
                    )
                for assertion_position, reference in enumerate(
                    _references_carried_by_result(
                        ledger,
                        event,
                        standing_coordinate=standing_coordinate,
                        source_standing_through_event_occurrence_identity=(
                            standing_boundary_identity
                        ),
                    )
                ):
                    ordered.append((position, assertion_position, reference))

    ordered.sort(key=lambda item: (item[0], item[1]))
    references = []
    seen = set()
    for _event_position, _assertion_position, reference in ordered:
        key = (
            reference["recorded_result_occurrence_identity"],
            reference["assertion_identity"],
        )
        if key in seen:
            continue
        seen.add(key)
        references.append(reference)
    return references


def source_assertion_references_for_candidate_standing(
    ledger: EventLedger, *, source_append_boundary: EventLedgerBoundary
) -> tuple[dict[str, str], ...]:
    """Read every exact source Assertion through the supplied boundary."""

    if not isinstance(ledger, EventLedger):
        raise TypeError("Candidate Standing requires one EventLedger")
    if not isinstance(source_append_boundary, EventLedgerBoundary):
        raise TypeError("Candidate Standing requires one exact source boundary")
    return tuple(
        deepcopy(reference)
        for reference in _source_assertion_references_through(
            ledger, _boundary(ledger, source_append_boundary.identity)
        )
    )


def _authority(responsibility: str) -> dict[str, Any]:
    exact_responsibility = _candidate_responsibility(responsibility)
    return {
        "source": "this Book",
        "book_clause_identity": BOOK_CLAUSE,
        "responsible_boundary": "this Seed",
        "scope": exact_responsibility,
        "standing_not_established": [
            "represented relation",
            "Admission",
            "Applicability to another Act",
            "Participation in another Act",
            "source Assertion movement",
        ],
    }


def _assignment_reference(assignment: Event) -> dict[str, str]:
    return {
        "recorded_occurrence_identity": assignment.identity,
        "assignment_subject_identity": assignment.material[
            "assignment_subject_identity"
        ],
    }


def _assignment_material(
    *,
    assignment_subject_identity: str,
    applicability_act_identity: str,
    applicability_act_occurrence_identity: str,
    applicability_result_identity: str,
    candidate_act_identity: str,
    candidate_act_occurrence_identity: str,
    candidate_result_identity: str,
    scope_identity: str,
    recording_locality_identity: str,
    prior_recording_occurrence_identity: str | None,
    source_append_boundary_identity: str,
    source_assertion_references: list[dict[str, str]],
    responsibility: str,
) -> dict[str, Any]:
    exact_responsibility = _candidate_responsibility(responsibility)
    exact_candidate_act = _candidate_act_for_responsibility(exact_responsibility)
    return {
        "assignment_subject_identity": assignment_subject_identity,
        "book_clause_identity": BOOK_CLAUSE,
        "responsibility": exact_responsibility,
        "responsible_boundary": "this Seed",
        "applicability_act_identity": applicability_act_identity,
        "applicability_act_occurrence_identity": (
            applicability_act_occurrence_identity
        ),
        "applicability_result_identity": applicability_result_identity,
        "candidate_act_identity": candidate_act_identity,
        "candidate_act": exact_candidate_act,
        "candidate_act_occurrence_identity": candidate_act_occurrence_identity,
        "candidate_result_identity": candidate_result_identity,
        "source_ledger_boundary_identity": source_append_boundary_identity,
        "source_assertion_references": deepcopy(source_assertion_references),
        "prior_recording_occurrence_identity": prior_recording_occurrence_identity,
        "scope": {
            "identity": scope_identity,
            "recording_locality_identity": recording_locality_identity,
            "source_ledger_boundary_identity": source_append_boundary_identity,
        },
        "authority": _authority(exact_responsibility),
        "limits": [
            "the complete result is bounded to the exact source ledger boundary"
        ],
        "unknown": [
            "what each Candidate represents or may participate in: Unknown"
        ],
    }


def _latest_locality_occurrence_identity(
    ledger: EventLedger, locality_identity: str
) -> str | None:
    events = ledger.list_locality(locality_identity)
    return events[-1].identity if events else None


def _require_latest_in_locality(ledger: EventLedger, event: Event, message: str) -> None:
    if _latest_locality_occurrence_identity(ledger, event.locality_identity) != event.identity:
        raise ValueError(message)


def _record_candidate_standing_responsibility_assignment(
    ledger: EventLedger,
    *,
    source_append_boundary: EventLedgerBoundary,
    recording_locality_identity: str,
    responsibility: str,
) -> Event:
    if not isinstance(ledger, EventLedger):
        raise TypeError("Candidate Standing requires one EventLedger")
    if type(recording_locality_identity) is not str or not recording_locality_identity:
        raise ValueError("Candidate Standing requires one exact recording Locality")
    boundary = _boundary(ledger, source_append_boundary.identity)
    exact_responsibility = _candidate_responsibility(responsibility)
    references = _source_assertion_references_through(ledger, boundary)
    for recorded in ledger.iter_locality_kind(
        recording_locality_identity,
        CANDIDATE_STANDING_RESPONSIBILITY_ASSIGNMENT_KIND,
    ):
        if (
            recorded.material.get("source_ledger_boundary_identity")
            == boundary.identity
            and recorded.material.get("responsibility") == exact_responsibility
        ):
            raise ValueError(
                "Candidate Standing already carries one assignment for this exact source boundary"
            )
    prior = _latest_locality_occurrence_identity(ledger, recording_locality_identity)
    return ledger.append(
        CANDIDATE_STANDING_RESPONSIBILITY_ASSIGNMENT_KIND,
        _assignment_material(
            assignment_subject_identity=new_identity(
                "candidate_standing_assignment_subject"
            ),
            applicability_act_identity=new_identity(
                "candidate_standing_applicability_act"
            ),
            applicability_act_occurrence_identity=new_identity(
                "candidate_standing_applicability_act_occurrence"
            ),
            applicability_result_identity=new_identity(
                "candidate_standing_applicability_result"
            ),
            candidate_act_identity=new_identity("candidate_standing_act"),
            candidate_act_occurrence_identity=new_identity(
                "candidate_standing_act_occurrence"
            ),
            candidate_result_identity=new_identity("candidate_standing_result"),
            scope_identity=new_identity("candidate_standing_scope"),
            recording_locality_identity=recording_locality_identity,
            prior_recording_occurrence_identity=prior,
            source_append_boundary_identity=boundary.identity,
            source_assertion_references=references,
            responsibility=exact_responsibility,
        ),
        locality_identity=recording_locality_identity,
    )


def record_one_source_candidate_standing_responsibility_assignment(
    ledger: EventLedger,
    *,
    source_append_boundary: EventLedgerBoundary,
    recording_locality_identity: str,
) -> Event:
    return _record_candidate_standing_responsibility_assignment(
        ledger,
        source_append_boundary=source_append_boundary,
        recording_locality_identity=recording_locality_identity,
        responsibility=ONE_SOURCE_CANDIDATE_RESPONSIBILITY,
    )


def record_ordered_pair_candidate_standing_responsibility_assignment(
    ledger: EventLedger,
    *,
    source_append_boundary: EventLedgerBoundary,
    recording_locality_identity: str,
) -> Event:
    return _record_candidate_standing_responsibility_assignment(
        ledger,
        source_append_boundary=source_append_boundary,
        recording_locality_identity=recording_locality_identity,
        responsibility=ORDERED_PAIR_CANDIDATE_RESPONSIBILITY,
    )


def _read_assignment(ledger: EventLedger, event_identity: Any) -> Event:
    assignment = _event(
        ledger,
        event_identity,
        kind=CANDIDATE_STANDING_RESPONSIBILITY_ASSIGNMENT_KIND,
        message="Candidate Standing requires one exact Responsibility assignment",
    )
    material = assignment.material
    boundary = _boundary(
        ledger, material.get("source_ledger_boundary_identity")
    )
    references = _source_assertion_references_through(ledger, boundary)
    exact_responsibility = _candidate_responsibility(material.get("responsibility"))
    identities = (
        "assignment_subject_identity",
        "applicability_act_identity",
        "applicability_act_occurrence_identity",
        "applicability_result_identity",
        "candidate_act_identity",
        "candidate_act_occurrence_identity",
        "candidate_result_identity",
    )
    exact_identities = {
        key: _identity(
            material.get(key),
            "Candidate Standing assignment requires exact lifecycle identities",
        )
        for key in identities
    }
    scope = material.get("scope")
    prior = material.get("prior_recording_occurrence_identity")
    if prior is not None and (type(prior) is not str or not prior):
        raise ValueError(
            "Candidate Standing assignment requires one exact prior recording occurrence"
        )
    expected = _assignment_material(
        **exact_identities,
        scope_identity=_identity(
            scope.get("identity") if type(scope) is dict else None,
            "Candidate Standing assignment requires one exact Scope",
        ),
        recording_locality_identity=assignment.locality_identity,
        prior_recording_occurrence_identity=prior,
        source_append_boundary_identity=boundary.identity,
        source_assertion_references=references,
        responsibility=exact_responsibility,
    )
    if material != expected:
        raise ValueError("Candidate Standing Responsibility assignment is not exact")
    if prior is not None:
        ordered = ledger.occurrences_in_append_order(
            (prior, assignment.identity),
            locality_identity=assignment.locality_identity,
        )
        if ordered[-1].identity != assignment.identity:
            raise ValueError("Candidate Standing assignment order is not exact")
    return assignment


def get_candidate_standing_responsibility_assignment(
    ledger: EventLedger, event_identity: str
) -> dict[str, Any]:
    return deepcopy(_read_assignment(ledger, event_identity).material)


def _applicability_act_material(assignment: Event) -> dict[str, Any]:
    references = assignment.material["source_assertion_references"]
    return {
        "applicability_act_identity": assignment.material[
            "applicability_act_identity"
        ],
        "act_occurrence_identity": assignment.material[
            "applicability_act_occurrence_identity"
        ],
        "act": APPLICABILITY_ACT,
        "responsibility": assignment.material["responsibility"],
        "responsible_boundary": "this Seed",
        "responsibility_assignment_reference": _assignment_reference(assignment),
        "source_ledger_boundary_identity": assignment.material[
            "source_ledger_boundary_identity"
        ],
        "candidate_act": assignment.material["candidate_act"],
        "input_relations": [
            {
                "source_assertion_reference": deepcopy(reference),
                "relation": "input_to",
                "role": "input",
                "candidate_act_identity": assignment.material[
                    "candidate_act_identity"
                ],
            }
            for reference in references
        ],
        "scope": deepcopy(assignment.material["scope"]),
        "authority": deepcopy(assignment.material["authority"]),
        "evidence_scope": "exact Candidate Standing source Assertions",
        "limits": list(assignment.material["limits"]),
        "unknown": list(assignment.material["unknown"]),
    }


def record_candidate_standing_applicability_act_evidence(
    ledger: EventLedger, *, responsibility_assignment_event_identity: str
) -> Event:
    assignment = _read_assignment(
        ledger, responsibility_assignment_event_identity
    )
    _require_latest_in_locality(
        ledger,
        assignment,
        "Candidate Standing Applicability requires its assignment current in the recording Locality",
    )
    return ledger.append(
        CANDIDATE_STANDING_APPLICABILITY_ACT_EVIDENCE_KIND,
        _applicability_act_material(assignment),
        locality_identity=assignment.locality_identity,
    )


def _read_applicability_act(
    ledger: EventLedger, event_identity: Any
) -> tuple[Event, Event]:
    act = _event(
        ledger,
        event_identity,
        kind=CANDIDATE_STANDING_APPLICABILITY_ACT_EVIDENCE_KIND,
        message="Candidate Standing requires exact Applicability Act Evidence",
    )
    reference = act.material.get("responsibility_assignment_reference")
    assignment = _read_assignment(
        ledger,
        reference.get("recorded_occurrence_identity")
        if type(reference) is dict
        else None,
    )
    if (
        act.locality_identity != assignment.locality_identity
        or act.material != _applicability_act_material(assignment)
    ):
        raise ValueError("Candidate Standing Applicability Act Evidence is not exact")
    ledger.occurrences_in_append_order(
        (assignment.identity, act.identity),
        locality_identity=assignment.locality_identity,
    )
    return act, assignment


def get_candidate_standing_applicability_act_evidence(
    ledger: EventLedger, event_identity: str
) -> dict[str, Any]:
    return deepcopy(_read_applicability_act(ledger, event_identity)[0].material)


def _applicability_result_material(
    act: Event, assignment: Event, *, evidence_identity: str | None = None
) -> dict[str, Any]:
    return {
        "result_identity": assignment.material["applicability_result_identity"],
        "applicability_act_identity": assignment.material[
            "applicability_act_identity"
        ],
        "act_occurrence_identity": assignment.material[
            "applicability_act_occurrence_identity"
        ],
        "exact_act": APPLICABILITY_ACT,
        "responsibility": assignment.material["responsibility"],
        "responsible_boundary": "this Seed",
        "responsibility_assignment_reference": _assignment_reference(assignment),
        "source_ledger_boundary_identity": assignment.material[
            "source_ledger_boundary_identity"
        ],
        "candidate_act": assignment.material["candidate_act"],
        "applicability_findings": [
            {
                "source_assertion_reference": deepcopy(reference),
                "candidate_act_identity": assignment.material[
                    "candidate_act_identity"
                ],
                "relation": "input_to",
                "role": "input",
                "finding": "applicable",
            }
            for reference in assignment.material["source_assertion_references"]
        ],
        "scope": deepcopy(assignment.material["scope"]),
        "authority": deepcopy(assignment.material["authority"]),
        "evidence_scope": "exact Candidate Act",
        "limits": list(assignment.material["limits"]),
        "unknown": list(assignment.material["unknown"]),
        "responsible_act_evidence_identity": act.identity,
        "evidence_of_yield_relation_identity": evidence_identity,
    }


def record_candidate_standing_applicability_result(
    ledger: EventLedger, *, responsible_act_evidence_event_identity: str
) -> Event:
    act, assignment = _read_applicability_act(
        ledger, responsible_act_evidence_event_identity
    )
    _require_latest_in_locality(
        ledger,
        act,
        "Candidate Standing Applicability result requires its Act current in the recording Locality",
    )
    result = _applicability_result_material(act, assignment)
    evidence = _record_evidence_of_yield_relation(
        ledger,
        locality_identity=act.locality_identity,
        exact_act=APPLICABILITY_ACT,
        act_occurrence_identity=act.material["act_occurrence_identity"],
        responsible_act_evidence_identity=act.identity,
        result_kind=APPLICABILITY_RESULT_NAME,
        result_identity=result["result_identity"],
        result_content={
            key: value
            for key, value in result.items()
            if key
            not in {
                "responsible_act_evidence_identity",
                "evidence_of_yield_relation_identity",
            }
        },
        responsibility=assignment.material["responsibility"],
        occurrence_boundary="complete_candidate_standing_applicability",
        responsible_boundary="this Seed",
    )
    return ledger.append(
        CANDIDATE_STANDING_APPLICABILITY_RESULT_KIND,
        _applicability_result_material(
            act, assignment, evidence_identity=evidence.identity
        ),
        locality_identity=act.locality_identity,
    )


def _read_applicability_result(
    ledger: EventLedger, event_identity: Any
) -> tuple[Event, Event, Event]:
    event = _event(
        ledger,
        event_identity,
        kind=CANDIDATE_STANDING_APPLICABILITY_RESULT_KIND,
        message="Candidate Standing requires one exact Applicability result",
    )
    act, assignment = _read_applicability_act(
        ledger, event.material.get("responsible_act_evidence_identity")
    )
    evidence_identity = event.material.get("evidence_of_yield_relation_identity")
    exact_evidence_identity = _identity(
            evidence_identity,
            "Candidate Standing Applicability requires exact Yield Evidence",
        )
    if event.material != _applicability_result_material(
        act, assignment, evidence_identity=exact_evidence_identity
    ) or not all(
        read_requirements_of_yield_relation(
            ledger,
            recorded_result_event_identity=event.identity,
            evidence_of_yield_relation_event_identity=evidence_identity,
            responsible_act_evidence_event_identity=act.identity,
        ).values()
    ):
        raise ValueError("Candidate Standing Applicability result is not exact")
    ledger.occurrences_in_append_order(
        (act.identity, evidence_identity, event.identity),
        locality_identity=event.locality_identity,
    )
    return event, act, assignment


def get_recorded_candidate_standing_applicability(
    ledger: EventLedger, event_identity: str
) -> dict[str, Any]:
    return deepcopy(_read_applicability_result(ledger, event_identity)[0].material)


def _candidate_act_material(
    assignment: Event, applicability: Event
) -> dict[str, Any]:
    references = assignment.material["source_assertion_references"]
    return {
        "candidate_act_identity": assignment.material["candidate_act_identity"],
        "act_occurrence_identity": assignment.material[
            "candidate_act_occurrence_identity"
        ],
        "act": assignment.material["candidate_act"],
        "responsibility": assignment.material["responsibility"],
        "responsible_boundary": "this Seed",
        "responsibility_assignment_reference": _assignment_reference(assignment),
        "applicability_result_event_identity": applicability.identity,
        "source_ledger_boundary_identity": assignment.material[
            "source_ledger_boundary_identity"
        ],
        "participation": [
            {
                "source_assertion_reference": deepcopy(reference),
                "role": "input",
                "act_occurrence_identity": assignment.material[
                    "candidate_act_occurrence_identity"
                ],
            }
            for reference in references
        ],
        "scope": deepcopy(assignment.material["scope"]),
        "authority": deepcopy(assignment.material["authority"]),
        "evidence_scope": "exact Candidate Act",
        "limits": list(assignment.material["limits"]),
        "unknown": list(assignment.material["unknown"]),
    }


def record_candidate_standing_act_evidence(
    ledger: EventLedger, *, applicability_result_event_identity: str
) -> Event:
    applicability, _applicability_act, assignment = (
        _read_applicability_result(ledger, applicability_result_event_identity)
    )
    _require_latest_in_locality(
        ledger,
        applicability,
        "Candidate Standing Act requires Applicability current in the recording Locality",
    )
    return ledger.append(
        CANDIDATE_STANDING_ACT_EVIDENCE_KIND,
        _candidate_act_material(assignment, applicability),
        locality_identity=assignment.locality_identity,
    )


def _read_candidate_act(
    ledger: EventLedger, event_identity: Any
) -> tuple[Event, Event, Event]:
    act = _event(
        ledger,
        event_identity,
        kind=CANDIDATE_STANDING_ACT_EVIDENCE_KIND,
        message="Candidate Standing requires exact Act Evidence",
    )
    applicability, _applicability_act, assignment = (
        _read_applicability_result(
            ledger, act.material.get("applicability_result_event_identity")
        )
    )
    if (
        act.locality_identity != assignment.locality_identity
        or act.material != _candidate_act_material(assignment, applicability)
    ):
        raise ValueError("Candidate Standing Act Evidence is not exact")
    ledger.occurrences_in_append_order(
        (applicability.identity, act.identity),
        locality_identity=act.locality_identity,
    )
    return act, applicability, assignment


def get_candidate_standing_act_evidence(
    ledger: EventLedger, event_identity: str
) -> dict[str, Any]:
    return deepcopy(_read_candidate_act(ledger, event_identity)[0].material)


def _unary_candidate_identity(
    assignment: Event, reference: dict[str, str], position: int
) -> str:
    coordinates = {
        "source_ledger_boundary_identity": assignment.material[
            "source_ledger_boundary_identity"
        ],
        "responsibility": assignment.material["responsibility"],
        "candidate_act": assignment.material["candidate_act"],
        "source_assertion_reference": reference,
        "position": position,
    }
    return "candidate_" + hashlib.sha256(
        _canonical(coordinates).encode("utf-8")
    ).hexdigest()


def _ordered_pair_candidate_identity(
    assignment: Event,
    first_reference: dict[str, str],
    second_reference: dict[str, str],
    position: int,
) -> str:
    coordinates = {
        "source_ledger_boundary_identity": assignment.material[
            "source_ledger_boundary_identity"
        ],
        "responsibility": assignment.material["responsibility"],
        "candidate_act": assignment.material["candidate_act"],
        "first_source_assertion_reference": first_reference,
        "second_source_assertion_reference": second_reference,
        "position": position,
    }
    return "candidate_" + hashlib.sha256(
        _canonical(coordinates).encode("utf-8")
    ).hexdigest()


def _unary_candidates(assignment: Event) -> list[dict[str, Any]]:
    return [
        {
            "dimensions": {
                "identity": _unary_candidate_identity(
                    assignment, reference, position
                ),
                "content": {
                    "position": position,
                    "source_assertion_reference": deepcopy(reference),
                    "source_ledger_boundary_identity": assignment.material[
                        "source_ledger_boundary_identity"
                    ],
                    "candidate_act": assignment.material["candidate_act"],
                },
                "source_provenance": "exact source Assertion reference",
                "responsibility": CANDIDATE_ASSERTION_RESPONSIBILITY,
                "authority": deepcopy(assignment.material["authority"]),
                "evidence_scope": "exact Candidate Standing Act Evidence",
            },
            "subject_kind": "assertion",
            "responsible_boundary": "this recorded assertion",
            "result": "candidate",
            "assertion_subject": {
                "source_assertion_reference": deepcopy(reference),
            },
            "assertion_scope": deepcopy(assignment.material["scope"]),
            "represented_relation": "Unknown",
            "conflicts": "Unknown",
            "unknown": ["what this Candidate represents: Unknown"],
            "limits": [
                "Candidate Standing establishes no represented relation",
                "source Assertion coordinates are carried by exact reference",
            ],
        }
        for position, reference in enumerate(
            assignment.material["source_assertion_references"]
        )
    ]


def _ordered_pair_candidates(assignment: Event) -> list[dict[str, Any]]:
    references = assignment.material["source_assertion_references"]
    ordered_pairs = (
        (first_reference, second_reference)
        for first_position, first_reference in enumerate(references)
        for second_position, second_reference in enumerate(references)
        if first_position != second_position
    )
    return [
        {
            "dimensions": {
                "identity": _ordered_pair_candidate_identity(
                    assignment,
                    first_reference,
                    second_reference,
                    position,
                ),
                "content": {
                    "position": position,
                    "first_source_assertion_reference": deepcopy(
                        first_reference
                    ),
                    "second_source_assertion_reference": deepcopy(
                        second_reference
                    ),
                    "source_ledger_boundary_identity": assignment.material[
                        "source_ledger_boundary_identity"
                    ],
                    "candidate_act": assignment.material["candidate_act"],
                },
                "source_provenance": "exact source Assertion references",
                "responsibility": CANDIDATE_ASSERTION_RESPONSIBILITY,
                "authority": deepcopy(assignment.material["authority"]),
                "evidence_scope": "exact Candidate Standing Act Evidence",
            },
            "subject_kind": "assertion",
            "responsible_boundary": "this recorded assertion",
            "result": "candidate",
            "assertion_subject": {
                "first_source_assertion_reference": deepcopy(first_reference),
                "second_source_assertion_reference": deepcopy(
                    second_reference
                ),
            },
            "assertion_scope": deepcopy(assignment.material["scope"]),
            "represented_relation": "Unknown",
            "conflicts": "Unknown",
            "unknown": ["what this Candidate represents: Unknown"],
            "limits": [
                "Candidate Standing establishes no represented relation",
                "source Assertion coordinates are carried by exact references",
            ],
        }
        for position, (first_reference, second_reference) in enumerate(
            ordered_pairs
        )
    ]


def _candidates(assignment: Event) -> list[dict[str, Any]]:
    if (
        _candidate_responsibility(assignment.material.get("responsibility"))
        == ONE_SOURCE_CANDIDATE_RESPONSIBILITY
    ):
        return _unary_candidates(assignment)
    return _ordered_pair_candidates(assignment)


def _required_candidate_count(assignment: Event) -> int:
    source_count = len(assignment.material["source_assertion_references"])
    if (
        _candidate_responsibility(assignment.material.get("responsibility"))
        == ONE_SOURCE_CANDIDATE_RESPONSIBILITY
    ):
        return source_count
    return source_count * (source_count - 1)


def _candidate_result_material(
    act: Event,
    assignment: Event,
    applicability: Event,
    *,
    evidence_identity: str | None = None,
) -> dict[str, Any]:
    candidates = _candidates(assignment)
    return {
        "result_identity": assignment.material["candidate_result_identity"],
        "candidate_act_identity": assignment.material["candidate_act_identity"],
        "act_occurrence_identity": assignment.material[
            "candidate_act_occurrence_identity"
        ],
        "exact_act": assignment.material["candidate_act"],
        "responsibility": assignment.material["responsibility"],
        "responsible_boundary": "this Seed",
        "responsibility_assignment_reference": _assignment_reference(assignment),
        "applicability_result_event_identity": applicability.identity,
        "source_ledger_boundary_identity": assignment.material[
            "source_ledger_boundary_identity"
        ],
        "source_assertion_references": deepcopy(
            assignment.material["source_assertion_references"]
        ),
        "candidate_assertions": candidates,
        "completeness": {
            "required_candidate_count": _required_candidate_count(assignment),
            "recorded_candidate_count": len(candidates),
            "partial": False,
        },
        "participation": deepcopy(act.material["participation"]),
        "scope": deepcopy(assignment.material["scope"]),
        "authority": deepcopy(assignment.material["authority"]),
        "limits": list(assignment.material["limits"]),
        "unknown": list(assignment.material["unknown"]),
        "responsible_act_evidence_identity": act.identity,
        "evidence_of_yield_relation_identity": evidence_identity,
    }


def record_candidate_standing_result(
    ledger: EventLedger, *, responsible_act_evidence_event_identity: str
) -> Event:
    act, applicability, assignment = _read_candidate_act(
        ledger, responsible_act_evidence_event_identity
    )
    _require_latest_in_locality(
        ledger,
        act,
        "Candidate Standing result requires its Act current in the recording Locality",
    )
    result = _candidate_result_material(act, assignment, applicability)
    evidence = _record_evidence_of_yield_relation(
        ledger,
        locality_identity=act.locality_identity,
        exact_act=assignment.material["candidate_act"],
        act_occurrence_identity=act.material["act_occurrence_identity"],
        responsible_act_evidence_identity=act.identity,
        result_kind=CANDIDATE_RESULT_NAME,
        result_identity=result["result_identity"],
        result_content={
            key: value
            for key, value in result.items()
            if key
            not in {
                "responsible_act_evidence_identity",
                "evidence_of_yield_relation_identity",
            }
        },
        responsibility=assignment.material["responsibility"],
        occurrence_boundary="complete_candidate_standing",
        responsible_boundary="this Seed",
    )
    return ledger.append(
        CANDIDATE_STANDING_RESULT_KIND,
        _candidate_result_material(
            act,
            assignment,
            applicability,
            evidence_identity=evidence.identity,
        ),
        locality_identity=act.locality_identity,
    )


def _read_candidate_result(
    ledger: EventLedger, event_identity: Any
) -> tuple[Event, Event, Event, Event]:
    event = _event(
        ledger,
        event_identity,
        kind=CANDIDATE_STANDING_RESULT_KIND,
        message="Candidate Standing requires one exact complete result",
    )
    act, applicability, assignment = _read_candidate_act(
        ledger, event.material.get("responsible_act_evidence_identity")
    )
    evidence_identity = event.material.get("evidence_of_yield_relation_identity")
    exact_evidence_identity = _identity(
            evidence_identity,
            "Candidate Standing requires exact Yield Evidence",
        )
    if event.material != _candidate_result_material(
        act,
        assignment,
        applicability,
        evidence_identity=exact_evidence_identity,
    ) or not all(
        read_requirements_of_yield_relation(
            ledger,
            recorded_result_event_identity=event.identity,
            evidence_of_yield_relation_event_identity=evidence_identity,
            responsible_act_evidence_event_identity=act.identity,
        ).values()
    ):
        raise ValueError("Candidate Standing result is not complete and exact")
    ledger.occurrences_in_append_order(
        (act.identity, evidence_identity, event.identity),
        locality_identity=event.locality_identity,
    )
    return event, act, applicability, assignment


def get_recorded_candidate_standing(
    ledger: EventLedger, event_identity: str
) -> dict[str, Any]:
    """Replay its exact sources and owed Candidates before returning Standing."""

    return deepcopy(_read_candidate_result(ledger, event_identity)[0].material)


def _exact_source_assertion_material(
    ledger: EventLedger, reference: dict[str, Any]
) -> dict[str, Any]:
    if type(reference) is not dict:
        raise ValueError("Candidate requires one exact source Assertion reference")
    event = ledger.get(reference.get("recorded_result_occurrence_identity"))
    if (
        event is None
        or event.kind != reference.get("recorded_result_occurrence_kind")
        or event.locality_identity != reference.get("source_locality_identity")
        or event.exact_material is not None
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise ValueError("Candidate source Assertion occurrence is not intact")

    coordinate = reference.get("assertion_coordinate")
    assertion: dict[str, Any]
    if coordinate == "result":
        assertion = event.material
        assertion_identity = event.material.get("result_identity")
        source_coordinates = _source_coordinates(event, None)
    elif type(coordinate) is str and coordinate.startswith("assertions/"):
        assertions = event.material.get("assertions")
        try:
            position = int(coordinate.removeprefix("assertions/"))
            assertion = assertions[position]
        except (TypeError, ValueError, IndexError) as error:
            raise ValueError(
                "Candidate source Assertion coordinate is not exact"
            ) from error
        assertion_identity = _assertion_identity(
            assertion, "Candidate source Assertion requires one exact identity"
        )
        source_coordinates = _source_coordinates(event, assertion)
    elif coordinate == "assertions":
        assertion = event.material.get("assertions")
        assertion_identity = _assertion_identity(
            assertion, "Candidate source Assertion requires one exact identity"
        )
        source_coordinates = _source_coordinates(event, assertion)
    elif type(coordinate) is str and coordinate.startswith("position_assertions/"):
        assertion = _recorded_position_assertion_coordinates_for_locality_movement(
            ledger,
            result_event_identity=event.identity,
            assertion_identity=reference.get("assertion_identity"),
        )
        assertion_identity = _assertion_identity(
            assertion, "Candidate source Assertion requires one exact identity"
        )
        source_coordinates = _source_coordinates(event, assertion)
    elif coordinate == "finding":
        assertion = event.material.get("finding")
        assertion_identity = _assertion_identity(
            assertion, "Candidate source Assertion requires one exact identity"
        )
        source_coordinates = _source_coordinates(event, assertion)
    elif type(coordinate) is str and coordinate.startswith("candidate_assertions/"):
        candidates = event.material.get("candidate_assertions")
        try:
            position = int(coordinate.removeprefix("candidate_assertions/"))
            assertion = candidates[position]
        except (TypeError, ValueError, IndexError) as error:
            raise ValueError(
                "Candidate source Assertion coordinate is not exact"
            ) from error
        assertion_identity = _assertion_identity(
            assertion, "Candidate source Assertion requires one exact identity"
        )
        source_coordinates = _source_coordinates(event, assertion)
    else:
        raise ValueError("Candidate source Assertion coordinate is not exact")

    if (
        assertion_identity != reference.get("assertion_identity")
        or source_coordinates != reference.get("source_assertion_coordinates")
    ):
        raise ValueError("Candidate source Assertion coordinates are not exact")
    return deepcopy(assertion)


def exact_source_assertion_materials_from_ordered_pair_candidate(
    ledger: EventLedger,
    *,
    candidate_standing_result_event_identity: str,
    candidate_assertion_identity: str,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Read both exact lower Assertions without moving or relating them."""

    result, _act, _applicability, _assignment = _read_candidate_result(
        ledger, candidate_standing_result_event_identity
    )
    matches = tuple(
        candidate
        for candidate in result.material["candidate_assertions"]
        if _assertion_identity(
            candidate, "ordered-pair Candidate requires one exact identity"
        )
        == candidate_assertion_identity
    )
    if len(matches) != 1:
        raise ValueError("ordered-pair Candidate identity is not exact")
    return _exact_source_assertion_materials_from_ordered_pair_candidate(
        ledger, matches[0]
    )


def _exact_source_assertion_materials_from_ordered_pair_candidate(
    ledger: EventLedger, candidate: dict[str, Any]
) -> tuple[dict[str, Any], dict[str, Any]]:
    subject = candidate.get("assertion_subject")
    if type(subject) is not dict or set(subject) != {
        "first_source_assertion_reference",
        "second_source_assertion_reference",
    }:
        raise ValueError("Candidate is not one exact ordered source Assertion pair")
    return (
        _exact_source_assertion_material(
            ledger, subject["first_source_assertion_reference"]
        ),
        _exact_source_assertion_material(
            ledger, subject["second_source_assertion_reference"]
        ),
    )


def exact_source_assertion_materials_from_every_ordered_pair_candidate(
    ledger: EventLedger,
    *,
    candidate_standing_result_event_identity: str,
) -> tuple[tuple[str, dict[str, Any], dict[str, Any]], ...]:
    """Read every ordered Candidate and both exact lower Assertions in order."""

    result, _act, _applicability, assignment = _read_candidate_result(
        ledger, candidate_standing_result_event_identity
    )
    if (
        assignment.material["responsibility"]
        != ORDERED_PAIR_CANDIDATE_RESPONSIBILITY
    ):
        raise ValueError("Candidate Standing is not the exact ordered-pair result")
    return tuple(
        (
            _assertion_identity(
                candidate, "ordered-pair Candidate requires one exact identity"
            ),
            *_exact_source_assertion_materials_from_ordered_pair_candidate(
                ledger, candidate
            ),
        )
        for candidate in result.material["candidate_assertions"]
    )


def _exact_representation_paths(
    material: Any, path: tuple[str | int, ...] = ()
) -> tuple[dict[str, Any], ...]:
    paths: list[dict[str, Any]] = []
    if type(material) is dict:
        carried = material.items()
    elif type(material) is list:
        carried = enumerate(material)
    else:
        return ()
    for coordinate, value in carried:
        exact_path = (*path, coordinate)
        paths.append(
            {
                "path": list(exact_path),
                "material": deepcopy(value),
            }
        )
        paths.extend(_exact_representation_paths(value, exact_path))
    return tuple(paths)


def exact_representation_paths_from_every_ordered_pair_candidate(
    ledger: EventLedger,
    *,
    candidate_standing_result_event_identity: str,
) -> tuple[
    tuple[
        str,
        tuple[dict[str, Any], ...],
        tuple[dict[str, Any], ...],
    ],
    ...,
]:
    """Read every nested representation path without assigning it grammar."""

    return tuple(
        (
            candidate_identity,
            _exact_representation_paths(first),
            _exact_representation_paths(second),
        )
        for candidate_identity, first, second in (
            exact_source_assertion_materials_from_every_ordered_pair_candidate(
                ledger,
                candidate_standing_result_event_identity=(
                    candidate_standing_result_event_identity
                ),
            )
        )
    )


def _exact_source_assertion_coordinates(
    reference: dict[str, Any],
) -> tuple[dict[str, Any], ...]:
    carried = reference.get("source_assertion_coordinates")
    if type(carried) is not dict or set(carried) != {
        "Evidence",
        "Authority",
        "Scope",
        "limits",
        "Unknown",
    }:
        raise ValueError("Candidate source Assertion coordinates are not exact")
    materials = {
        "source_Assertion_reference": deepcopy(reference),
        "source_Locality": reference.get("source_locality_identity"),
        "source_Standing_boundary": reference.get(
            "source_standing_through_event_occurrence_identity"
        ),
        **deepcopy(carried),
    }
    if (
        type(materials["source_Locality"]) is not str
        or not materials["source_Locality"]
        or type(materials["source_Standing_boundary"]) is not str
        or not materials["source_Standing_boundary"]
    ):
        raise ValueError("Candidate source Assertion coordinates are not exact")
    return tuple(
        {
            "grammar_coordinate_reference": [
                "clause_coordinates",
                BOOK_CLAUSE,
                "source_Assertion_coordinates",
                "coordinates",
                position,
            ],
            "coordinate": coordinate,
            "material": materials[coordinate],
        }
        for position, coordinate in enumerate(_SOURCE_ASSERTION_COORDINATES)
    )


def exact_source_assertion_coordinates_from_every_ordered_pair_candidate(
    ledger: EventLedger,
    *,
    candidate_standing_result_event_identity: str,
) -> tuple[
    tuple[
        str,
        tuple[dict[str, Any], ...],
        tuple[dict[str, Any], ...],
    ],
    ...,
]:
    """Read only the source coordinates explicitly carried by Book grammar."""

    result, _act, _applicability, assignment = _read_candidate_result(
        ledger, candidate_standing_result_event_identity
    )
    if (
        assignment.material["responsibility"]
        != ORDERED_PAIR_CANDIDATE_RESPONSIBILITY
    ):
        raise ValueError("Candidate Standing is not the exact ordered-pair result")
    coordinates = []
    for candidate in result.material["candidate_assertions"]:
        subject = candidate.get("assertion_subject")
        if type(subject) is not dict or set(subject) != {
            "first_source_assertion_reference",
            "second_source_assertion_reference",
        }:
            raise ValueError(
                "Candidate is not one exact ordered source Assertion pair"
            )
        coordinates.append(
            (
                _assertion_identity(
                    candidate,
                    "ordered-pair Candidate requires one exact identity",
                ),
                _exact_source_assertion_coordinates(
                    subject["first_source_assertion_reference"]
                ),
                _exact_source_assertion_coordinates(
                    subject["second_source_assertion_reference"]
                ),
            )
        )
    return tuple(coordinates)


def represented_relation_coordinates_from_every_ordered_pair_candidate(
    ledger: EventLedger,
    *,
    candidate_standing_result_event_identity: str,
) -> tuple[
    tuple[
        str,
        dict[str, Any],
        dict[str, Any],
        dict[str, Any],
    ],
    ...,
]:
    """Read every ordered Candidate relation coordinate without filling it."""

    result, _act, _applicability, assignment = _read_candidate_result(
        ledger, candidate_standing_result_event_identity
    )
    if (
        assignment.material["responsibility"]
        != ORDERED_PAIR_CANDIDATE_RESPONSIBILITY
    ):
        raise ValueError("Candidate Standing is not the exact ordered-pair result")
    coordinates = []
    for candidate in result.material["candidate_assertions"]:
        subject = candidate.get("assertion_subject")
        if type(subject) is not dict or set(subject) != {
            "first_source_assertion_reference",
            "second_source_assertion_reference",
        }:
            raise ValueError(
                "Candidate is not one exact ordered source Assertion pair"
            )
        represented_relation = candidate.get("represented_relation")
        if represented_relation != "Unknown":
            raise ValueError("Candidate represented relation is not Unknown")
        coordinates.append(
            (
                _assertion_identity(
                    candidate,
                    "ordered-pair Candidate requires one exact identity",
                ),
                deepcopy(subject["first_source_assertion_reference"]),
                deepcopy(subject["second_source_assertion_reference"]),
                {
                    "grammar_coordinate_reference": [
                        "clause_coordinates",
                        BOOK_CLAUSE,
                        "ordered_pair_candidate_responsibility",
                        "represented_relation",
                    ],
                    "coordinate": "represented_relation",
                    "material": represented_relation,
                },
            )
        )
    return tuple(coordinates)


def boundaries_of_recorded_candidate_standing(
    ledger: EventLedger, event_identity: str
) -> dict[str, EventLedgerBoundary]:
    """Read the distinct frozen-source and later-result append boundaries."""

    event, _act, _applicability, assignment = _read_candidate_result(
        ledger, event_identity
    )
    return {
        "source_ledger_boundary": _boundary(
            ledger, assignment.material["source_ledger_boundary_identity"]
        ),
        "candidate_result_ledger_boundary": (
            ledger.append_boundary_through_occurrence(event.identity)
        ),
    }


def record_complete_candidate_standing(
    ledger: EventLedger,
    *,
    recording_locality_identity: str,
    source_append_boundary: EventLedgerBoundary | None = None,
) -> Event:
    """Record one Candidate for each source Assertion through the boundary."""

    boundary = source_append_boundary or ledger.append_boundary()
    assignment = record_one_source_candidate_standing_responsibility_assignment(
        ledger,
        source_append_boundary=boundary,
        recording_locality_identity=recording_locality_identity,
    )
    applicability_act = record_candidate_standing_applicability_act_evidence(
        ledger,
        responsibility_assignment_event_identity=assignment.identity,
    )
    applicability = record_candidate_standing_applicability_result(
        ledger,
        responsible_act_evidence_event_identity=applicability_act.identity,
    )
    act = record_candidate_standing_act_evidence(
        ledger,
        applicability_result_event_identity=applicability.identity,
    )
    return record_candidate_standing_result(
        ledger,
        responsible_act_evidence_event_identity=act.identity,
    )


def record_complete_ordered_pair_candidate_standing(
    ledger: EventLedger,
    *,
    recording_locality_identity: str,
    source_append_boundary: EventLedgerBoundary | None = None,
) -> Event:
    """Record every ordered pair Candidate owed by the frozen source surface."""

    boundary = source_append_boundary or ledger.append_boundary()
    assignment = record_ordered_pair_candidate_standing_responsibility_assignment(
        ledger,
        source_append_boundary=boundary,
        recording_locality_identity=recording_locality_identity,
    )
    applicability_act = record_candidate_standing_applicability_act_evidence(
        ledger,
        responsibility_assignment_event_identity=assignment.identity,
    )
    applicability = record_candidate_standing_applicability_result(
        ledger,
        responsible_act_evidence_event_identity=applicability_act.identity,
    )
    act = record_candidate_standing_act_evidence(
        ledger,
        applicability_result_event_identity=applicability.identity,
    )
    return record_candidate_standing_result(
        ledger,
        responsible_act_evidence_event_identity=act.identity,
    )


def record_one_source_and_ordered_pair_candidate_standings(
    ledger: EventLedger,
    *,
    one_source_recording_locality_identity: str,
    ordered_pair_recording_locality_identity: str,
    source_append_boundary: EventLedgerBoundary | None = None,
) -> tuple[Event, Event]:
    """Record both exact Candidate Responsibilities through one frozen boundary."""

    boundary = source_append_boundary or ledger.append_boundary()
    one_source_result = record_complete_candidate_standing(
        ledger,
        recording_locality_identity=one_source_recording_locality_identity,
        source_append_boundary=boundary,
    )
    ordered_pair_result = record_complete_ordered_pair_candidate_standing(
        ledger,
        recording_locality_identity=ordered_pair_recording_locality_identity,
        source_append_boundary=boundary,
    )
    return one_source_result, ordered_pair_result
