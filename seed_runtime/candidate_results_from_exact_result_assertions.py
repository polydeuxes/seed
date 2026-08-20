"""Yield one exact Candidate result for each subject owed by one Responsibility."""

from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from typing import Any, Iterator, NamedTuple

from seed_runtime.event import Event
from seed_runtime.events import CORRUPTED, EventLedger, EventLedgerBoundary
from seed_runtime.identities import new_identity
from seed_runtime.measurement_of_position_coordinates_of_byte_pair_occurrences import (
    BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND,
    _recorded_position_assertion_coordinates_for_locality_movement,
    references_to_recorded_position_coordinates_of_byte_pair_occurrences,
)


# EventLedger currently requires one storage-routing value. Every Candidate
# coordinate shares this bounded stream; the value establishes no occurrence
# classification.
CANDIDATE_OCCURRENCE_STREAM = "operator.candidate.occurred"

BOOK_CLAUSE = "01.Source.E.1"
ONE_SOURCE_CANDIDATE_RESPONSIBILITY = (
    "record one Candidate for each exact source Assertion through one exact boundary"
)
ORDERED_PAIR_CANDIDATE_RESPONSIBILITY = (
    "record one Candidate for each distinct ordered source Assertion pair through "
    "one exact boundary"
)
_CANDIDATE_RESPONSIBILITIES = frozenset(
    (ONE_SOURCE_CANDIDATE_RESPONSIBILITY, ORDERED_PAIR_CANDIDATE_RESPONSIBILITY)
)
APPLICABILITY_ACT = (
    "Applicability of one required Candidate subject to one Candidate Act"
)
ONE_SOURCE_CANDIDATE_ACT = "record one Candidate for one exact source Assertion"
ORDERED_PAIR_CANDIDATE_ACT = (
    "record one Candidate for one exact ordered source Assertion pair"
)
EVENT_KIND_RESPONSIBILITIES = {
    CANDIDATE_OCCURRENCE_STREAM: "01.Source.E.1",
}
_SOURCE_REPLAY_COORDINATES = (
    "measurement_occurrences",
    "comparison_result_occurrences",
    "candidate_result_occurrences",
)


class CandidateResponsibilityProgress(NamedTuple):
    required_candidate_addresses: tuple[str, ...]
    recorded_candidate_result_occurrences: tuple[str, ...]
    owed_candidate_addresses: tuple[str, ...]


class YieldedCandidateResult(NamedTuple):
    result_occurrence: Event
    progress: CandidateResponsibilityProgress


def _address(value: Any, message: str) -> str:
    if type(value) is not str or not value:
        raise ValueError(message)
    return value


def _candidate_responsibility(value: Any) -> str:
    if value not in _CANDIDATE_RESPONSIBILITIES:
        raise ValueError("Candidate production requires one exact Responsibility")
    return value


def _candidate_act_for_responsibility(responsibility: str) -> str:
    exact = _candidate_responsibility(responsibility)
    if exact == ONE_SOURCE_CANDIDATE_RESPONSIBILITY:
        return ONE_SOURCE_CANDIDATE_ACT
    return ORDERED_PAIR_CANDIDATE_ACT


def _event(
    ledger: EventLedger,
    event_address: Any,
    *,
    message: str,
) -> Event:
    event = ledger.get(_address(event_address, message))
    if (
        event is None
        or event.kind != CANDIDATE_OCCURRENCE_STREAM
        or event.exact_material is not None
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise ValueError(message)
    return event


def _canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def _boundary(ledger: EventLedger, address: Any) -> EventLedgerBoundary:
    exact = EventLedgerBoundary(
        _address(address, "Candidate production requires one exact source boundary")
    )
    ledger.list(through=exact)
    return exact


def _assertion_address(assertion: Any, message: str) -> str:
    if type(assertion) is not dict:
        raise ValueError(message)
    dimensions = assertion.get("dimensions")
    address = dimensions.get("identity") if type(dimensions) is dict else None
    if type(address) is not str or not address:
        address = assertion.get("identity")
    if type(address) is not str or not address:
        address = assertion.get("subject_address")
    return _address(address, message)


def _source_assertion_reference(
    event: Event,
    *,
    replay_coordinate: str,
    assertion_coordinate: str,
    assertion_address: str,
    source_assertion_coordinates: dict[str, Any],
    source_replay_through_event_occurrence_address: str,
) -> dict[str, Any]:
    return {
        "recorded_result_occurrence_identity": event.identity,
        "assertion_identity": assertion_address,
        "assertion_coordinate": assertion_coordinate,
        "source_locality_identity": event.locality_identity,
        "source_replay_coordinate": replay_coordinate,
        "source_replay_through_event_occurrence_identity": (
            source_replay_through_event_occurrence_address
        ),
        "source_assertion_coordinates": deepcopy(source_assertion_coordinates),
    }


def _source_coordinates(event: Event, assertion: dict[str, Any] | None) -> dict[str, Any]:
    if assertion is None:
        return {
            "Yield": event.material.get("yield_relation_occurrence_identity"),
            "Authority": deepcopy(event.material.get("authority")),
            "Scope": deepcopy(event.material.get("scope")),
            "limits": deepcopy(event.material.get("limits")),
            "Unknown": deepcopy(event.material.get("unknown")),
        }
    dimensions = assertion.get("dimensions")
    return {
        "Authority": deepcopy(
            dimensions.get("authority")
            if type(dimensions) is dict
            else assertion.get("Authority")
        ),
        "Scope": deepcopy(
            assertion.get("assertion_scope")
            if "assertion_scope" in assertion
            else assertion.get("Scope")
        ),
        "limits": deepcopy(assertion.get("limits")),
        "Unknown": deepcopy(assertion.get("unknown")),
    }


def _references_carried_by_result(
    ledger: EventLedger,
    event: Event,
    *,
    replay_coordinate: str,
    source_replay_through_event_occurrence_address: str,
) -> list[dict[str, Any]]:
    material = event.material
    references: list[dict[str, Any]] = []
    result_address = material.get("result_identity")
    if type(result_address) is str and result_address:
        references.append(
            _source_assertion_reference(
                event,
                replay_coordinate=replay_coordinate,
                assertion_coordinate="result",
                assertion_address=result_address,
                source_assertion_coordinates=_source_coordinates(event, None),
                source_replay_through_event_occurrence_address=(
                    source_replay_through_event_occurrence_address
                ),
            )
        )

    assertions = material.get("assertions")
    if type(assertions) is list:
        for position, assertion in enumerate(assertions):
            references.append(
                _source_assertion_reference(
                    event,
                    replay_coordinate=replay_coordinate,
                    assertion_coordinate=f"assertions/{position}",
                    assertion_address=_assertion_address(
                        assertion,
                        "Candidate production requires exact Assertions carried by a result",
                    ),
                    source_assertion_coordinates=_source_coordinates(event, assertion),
                    source_replay_through_event_occurrence_address=(
                        source_replay_through_event_occurrence_address
                    ),
                )
            )
    elif type(assertions) is dict:
        references.append(
            _source_assertion_reference(
                event,
                replay_coordinate=replay_coordinate,
                assertion_coordinate="assertions",
                assertion_address=_assertion_address(
                    assertions,
                    "Candidate production requires one exact Assertion carried by a result",
                ),
                source_assertion_coordinates=_source_coordinates(event, assertions),
                source_replay_through_event_occurrence_address=(
                    source_replay_through_event_occurrence_address
                ),
            )
        )
    elif assertions is not None:
        raise ValueError("Candidate production requires exact result Assertions")

    if event.kind == BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND:
        for position, reference in enumerate(
            references_to_recorded_position_coordinates_of_byte_pair_occurrences(
                ledger, event.identity
            )
        ):
            assertion = _recorded_position_assertion_coordinates_for_locality_movement(
                ledger,
                result_event_identity=event.identity,
                assertion_identity=reference.assertion_identity,
            )
            references.append(
                _source_assertion_reference(
                    event,
                    replay_coordinate=replay_coordinate,
                    assertion_coordinate=f"position_assertions/{position}",
                    assertion_address=reference.assertion_identity,
                    source_assertion_coordinates=_source_coordinates(event, assertion),
                    source_replay_through_event_occurrence_address=(
                        source_replay_through_event_occurrence_address
                    ),
                )
            )

    finding = material.get("finding")
    if finding is not None:
        references.append(
            _source_assertion_reference(
                event,
                replay_coordinate=replay_coordinate,
                assertion_coordinate="finding",
                assertion_address=_assertion_address(
                    finding,
                    "Candidate production requires one exact finding Assertion",
                ),
                source_assertion_coordinates=_source_coordinates(event, finding),
                source_replay_through_event_occurrence_address=(
                    source_replay_through_event_occurrence_address
                ),
            )
        )

    if (
        event.kind == CANDIDATE_OCCURRENCE_STREAM
        and type(event.material.get("candidate_assertion")) is dict
    ):
        assertion = material.get("candidate_assertion")
        references.append(
            _source_assertion_reference(
                event,
                replay_coordinate=replay_coordinate,
                assertion_coordinate="candidate_assertion",
                assertion_address=_assertion_address(
                    assertion,
                    "Candidate result requires one exact Candidate Assertion",
                ),
                source_assertion_coordinates=_source_coordinates(event, assertion),
                source_replay_through_event_occurrence_address=(
                    source_replay_through_event_occurrence_address
                ),
            )
        )
    return references


def _source_assertion_references_through(
    ledger: EventLedger, boundary: EventLedgerBoundary
) -> list[dict[str, Any]]:
    events = ledger.list(through=boundary)
    positions = {event.identity: position for position, event in enumerate(events)}
    locality_events: dict[str, list[str]] = {}
    for event in events:
        locality_events.setdefault(event.locality_identity, []).append(event.identity)

    from seed_runtime.operator_locality_standing import advance_operator_locality_standing

    ordered: list[tuple[int, int, dict[str, Any]]] = []
    for locality_address, event_addresses in locality_events.items():
        replay = advance_operator_locality_standing(
            ledger, event_addresses, locality_identity=locality_address
        )
        replay_boundary = replay.get("through_event_occurrence_identity")
        if replay_boundary is None:
            continue
        exact_replay_boundary = _address(
            replay_boundary,
            "Candidate production requires one exact bounded replay boundary",
        )
        for replay_coordinate in _SOURCE_REPLAY_COORDINATES:
            occurrences = replay.get(replay_coordinate)
            if type(occurrences) is not dict:
                raise ValueError("Candidate production requires exact result occurrences")
            for occurrence_address in occurrences:
                event = ledger.get(occurrence_address)
                position = positions.get(occurrence_address)
                if (
                    event is None
                    or position is None
                    or event.locality_identity != locality_address
                    or ledger.integrity_of(event.identity) == CORRUPTED
                ):
                    raise ValueError("Candidate production requires intact source results")
                for assertion_position, reference in enumerate(
                    _references_carried_by_result(
                        ledger,
                        event,
                        replay_coordinate=replay_coordinate,
                        source_replay_through_event_occurrence_address=(
                            exact_replay_boundary
                        ),
                    )
                ):
                    ordered.append((position, assertion_position, reference))

    ordered.sort(key=lambda item: (item[0], item[1]))
    references: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()
    for _event_position, _assertion_position, reference in ordered:
        key = (
            reference["recorded_result_occurrence_identity"],
            reference["assertion_identity"],
        )
        if key not in seen:
            seen.add(key)
            references.append(reference)
    return references


def source_assertion_references_through_boundary(
    ledger: EventLedger, *, source_append_boundary: EventLedgerBoundary
) -> tuple[dict[str, Any], ...]:
    """Read every exact source Assertion through one frozen boundary."""

    if not isinstance(ledger, EventLedger):
        raise TypeError("Candidate production requires one EventLedger")
    if not isinstance(source_append_boundary, EventLedgerBoundary):
        raise TypeError("Candidate production requires one exact source boundary")
    return tuple(
        deepcopy(reference)
        for reference in _source_assertion_references_through(
            ledger, _boundary(ledger, source_append_boundary.identity)
        )
    )


def _authority(responsibility: str) -> dict[str, Any]:
    return {
        "source": "this Book",
        "book_clause_identity": BOOK_CLAUSE,
        "responsible_boundary": "this Seed",
        "scope": _candidate_responsibility(responsibility),
    }


def _responsibility_reference(responsibility: Event) -> dict[str, str]:
    return {
        "recorded_occurrence_identity": responsibility.identity,
        "responsibility_subject_identity": responsibility.material[
            "responsibility_subject_identity"
        ],
    }


def _required_subject_address(
    responsibility: Event,
    *,
    position: int,
    role: str,
    references: list[dict[str, Any]],
) -> str:
    coordinates = {
        "responsibility_reference": _responsibility_reference(responsibility),
        "source_ledger_boundary_identity": responsibility.material[
            "source_ledger_boundary_identity"
        ],
        "position": position,
        "role": role,
        "source_assertion_references": references,
    }
    return "candidate_" + hashlib.sha256(
        _canonical(coordinates).encode("utf-8")
    ).hexdigest()


def _required_subjects(responsibility: Event) -> tuple[dict[str, Any], ...]:
    references = responsibility.material["source_assertion_references"]
    exact_responsibility = responsibility.material["responsibility"]
    subjects: list[dict[str, Any]] = []
    if exact_responsibility == ONE_SOURCE_CANDIDATE_RESPONSIBILITY:
        for position, reference in enumerate(references):
            subject_references = [deepcopy(reference)]
            role = "source Assertion"
            subjects.append(
                {
                    "candidate_address": _required_subject_address(
                        responsibility,
                        position=position,
                        role=role,
                        references=subject_references,
                    ),
                    "position": position,
                    "role": role,
                    "source_assertion_references": subject_references,
                }
            )
        return tuple(subjects)

    position = 0
    for first_position, first in enumerate(references):
        for second_position, second in enumerate(references):
            if first_position == second_position:
                continue
            subject_references = [deepcopy(first), deepcopy(second)]
            role = "ordered source Assertion pair"
            subjects.append(
                {
                    "candidate_address": _required_subject_address(
                        responsibility,
                        position=position,
                        role=role,
                        references=subject_references,
                    ),
                    "position": position,
                    "role": role,
                    "source_assertion_references": subject_references,
                }
            )
            position += 1
    return tuple(subjects)


def _responsibility_material(
    *,
    responsibility_subject_address: str,
    source_boundary: EventLedgerBoundary,
    source_references: list[dict[str, Any]],
    responsibility: str,
    recording_locality: str,
    scope_address: str,
) -> dict[str, Any]:
    return {
        "responsibility_subject_identity": responsibility_subject_address,
        "book_clause_identity": BOOK_CLAUSE,
        "responsibility": responsibility,
        "responsible_boundary": "this Seed",
        "candidate_act": _candidate_act_for_responsibility(responsibility),
        "source_ledger_boundary_identity": source_boundary.identity,
        "source_assertion_references": deepcopy(source_references),
        "scope": {
            "identity": scope_address,
            "recording_locality_identity": recording_locality,
            "source_ledger_boundary_identity": source_boundary.identity,
        },
        "authority": _authority(responsibility),
        "limits": [
            "Each Responsibility is exhaustive for its bounded subject set"
        ],
        "unknown": ["each Candidate relation: Unknown"],
    }


def _record_candidate_responsibility(
    ledger: EventLedger,
    *,
    source_append_boundary: EventLedgerBoundary,
    recording_locality_identity: str,
    responsibility: str,
) -> Event:
    if not isinstance(ledger, EventLedger):
        raise TypeError("Candidate production requires one EventLedger")
    if type(recording_locality_identity) is not str or not recording_locality_identity:
        raise ValueError("Candidate production requires one recording Locality")
    boundary = _boundary(ledger, source_append_boundary.identity)
    exact_responsibility = _candidate_responsibility(responsibility)
    references = _source_assertion_references_through(ledger, boundary)
    for recorded in ledger.iter_locality_kind(
        recording_locality_identity, CANDIDATE_OCCURRENCE_STREAM
    ):
        if (
            "responsibility_subject_identity" in recorded.material
            and recorded.material.get("source_ledger_boundary_identity")
            == boundary.identity
            and recorded.material.get("responsibility") == exact_responsibility
        ):
            raise ValueError(
                "Candidate Responsibility already exists for this source boundary"
            )
    return ledger.append(
        CANDIDATE_OCCURRENCE_STREAM,
        _responsibility_material(
            responsibility_subject_address=new_identity(
                "candidate_responsibility_subject"
            ),
            source_boundary=boundary,
            source_references=references,
            responsibility=exact_responsibility,
            recording_locality=recording_locality_identity,
            scope_address=new_identity("candidate_responsibility_scope"),
        ),
        locality_identity=recording_locality_identity,
    )


def record_one_source_candidate_responsibility(
    ledger: EventLedger,
    *,
    source_append_boundary: EventLedgerBoundary,
    recording_locality_identity: str,
) -> Event:
    return _record_candidate_responsibility(
        ledger,
        source_append_boundary=source_append_boundary,
        recording_locality_identity=recording_locality_identity,
        responsibility=ONE_SOURCE_CANDIDATE_RESPONSIBILITY,
    )


def record_ordered_pair_candidate_responsibility(
    ledger: EventLedger,
    *,
    source_append_boundary: EventLedgerBoundary,
    recording_locality_identity: str,
) -> Event:
    return _record_candidate_responsibility(
        ledger,
        source_append_boundary=source_append_boundary,
        recording_locality_identity=recording_locality_identity,
        responsibility=ORDERED_PAIR_CANDIDATE_RESPONSIBILITY,
    )


def _read_responsibility(ledger: EventLedger, event_address: Any) -> Event:
    event = _event(
        ledger,
        event_address,
        message="Candidate production requires one exact Responsibility",
    )
    material = event.material
    boundary = _boundary(ledger, material.get("source_ledger_boundary_identity"))
    responsibility = _candidate_responsibility(material.get("responsibility"))
    references = _source_assertion_references_through(ledger, boundary)
    scope = material.get("scope")
    expected = _responsibility_material(
        responsibility_subject_address=_address(
            material.get("responsibility_subject_identity"),
            "Candidate Responsibility requires one subject address",
        ),
        source_boundary=boundary,
        source_references=references,
        responsibility=responsibility,
        recording_locality=event.locality_identity,
        scope_address=_address(
            scope.get("identity") if type(scope) is dict else None,
            "Candidate Responsibility requires one Scope address",
        ),
    )
    if material != expected:
        raise ValueError("Candidate Responsibility is not exact")
    return event


def get_candidate_responsibility(
    ledger: EventLedger, event_identity: str
) -> dict[str, Any]:
    return deepcopy(_read_responsibility(ledger, event_identity).material)


def _lifecycle_addresses() -> dict[str, str]:
    return {
        "applicability_act_identity": new_identity("candidate_applicability_act"),
        "applicability_act_occurrence_identity": new_identity(
            "candidate_applicability_act_occurrence"
        ),
        "applicability_result_identity": new_identity(
            "candidate_applicability_result"
        ),
        "candidate_act_identity": new_identity("candidate_act"),
        "candidate_act_occurrence_identity": new_identity(
            "candidate_act_occurrence"
        ),
        "candidate_result_identity": new_identity("candidate_result"),
    }


def _applicability_act_material(
    responsibility: Event,
    subject: dict[str, Any],
    addresses: dict[str, str],
) -> dict[str, Any]:
    return {
        "applicability_act_identity": addresses["applicability_act_identity"],
        "applicability_act_occurrence_identity": addresses[
            "applicability_act_occurrence_identity"
        ],
        "applicability_result_identity": addresses["applicability_result_identity"],
        "candidate_act_identity": addresses["candidate_act_identity"],
        "candidate_act_occurrence_identity": addresses[
            "candidate_act_occurrence_identity"
        ],
        "candidate_result_identity": addresses["candidate_result_identity"],
        "act": APPLICABILITY_ACT,
        "responsibility": responsibility.material["responsibility"],
        "responsible_boundary": "this Seed",
        "responsibility_reference": _responsibility_reference(responsibility),
        "required_subject": deepcopy(subject),
        "candidate_act": responsibility.material["candidate_act"],
        "scope": deepcopy(responsibility.material["scope"]),
        "authority": deepcopy(responsibility.material["authority"]),
        "limits": list(responsibility.material["limits"]),
        "unknown": list(responsibility.material["unknown"]),
    }


def _yield_relation_material(
    responsibility: Event,
    *,
    act_occurrence_address: str,
    result_address: str,
    result_name: str,
) -> dict[str, Any]:
    return {
        "first_subject": {"Act_occurrence": act_occurrence_address},
        "relation": "yield",
        "second_subject": {"result": result_address, "name": result_name},
        "responsibility_reference": _responsibility_reference(responsibility),
        "authority": deepcopy(responsibility.material["authority"]),
        "scope": deepcopy(responsibility.material["scope"]),
        "limits": list(responsibility.material["limits"]),
        "unknown": list(responsibility.material["unknown"]),
    }


def _applicability_result_material(
    responsibility: Event,
    act: Event,
    yield_relation: Event,
) -> dict[str, Any]:
    return {
        "result_identity": act.material["applicability_result_identity"],
        "act_occurrence_identity": act.material[
            "applicability_act_occurrence_identity"
        ],
        "exact_act": APPLICABILITY_ACT,
        "responsibility": responsibility.material["responsibility"],
        "responsibility_reference": _responsibility_reference(responsibility),
        "required_subject": deepcopy(act.material["required_subject"]),
        "finding": "applicable",
        "candidate_act": responsibility.material["candidate_act"],
        "yield_relation_occurrence_identity": yield_relation.identity,
        "scope": deepcopy(responsibility.material["scope"]),
        "authority": deepcopy(responsibility.material["authority"]),
        "limits": list(responsibility.material["limits"]),
        "unknown": list(responsibility.material["unknown"]),
    }


def _participation_material(
    responsibility: Event, applicability: Event, act: Event
) -> dict[str, Any]:
    subject = applicability.material["required_subject"]
    return {
        "first_subject": deepcopy(subject),
        "relation": "participation",
        "role": subject["role"],
        "second_subject": {
            "Act_occurrence": act.material["candidate_act_occurrence_identity"]
        },
        "responsibility_reference": _responsibility_reference(responsibility),
        "applicability_result_occurrence_identity": applicability.identity,
        "authority": deepcopy(responsibility.material["authority"]),
        "scope": deepcopy(responsibility.material["scope"]),
        "limits": list(responsibility.material["limits"]),
        "unknown": list(responsibility.material["unknown"]),
    }


def _candidate_act_material(
    responsibility: Event,
    applicability: Event,
    applicability_act: Event,
    participation: Event,
) -> dict[str, Any]:
    return {
        "candidate_act_identity": applicability_act.material["candidate_act_identity"],
        "act_occurrence_identity": applicability_act.material[
            "candidate_act_occurrence_identity"
        ],
        "candidate_result_identity": applicability_act.material[
            "candidate_result_identity"
        ],
        "act": responsibility.material["candidate_act"],
        "responsibility": responsibility.material["responsibility"],
        "responsibility_reference": _responsibility_reference(responsibility),
        "required_subject": deepcopy(applicability.material["required_subject"]),
        "applicability_result_occurrence_identity": applicability.identity,
        "participation_relation_occurrence_identity": participation.identity,
        "scope": deepcopy(responsibility.material["scope"]),
        "authority": deepcopy(responsibility.material["authority"]),
        "limits": list(responsibility.material["limits"]),
        "unknown": list(responsibility.material["unknown"]),
    }


def _candidate_assertion(
    responsibility: Event, subject: dict[str, Any]
) -> dict[str, Any]:
    references = subject["source_assertion_references"]
    if len(references) == 1:
        content = {
            "position": subject["position"],
            "source_assertion_reference": deepcopy(references[0]),
            "source_role": "source Assertion",
        }
    else:
        content = {
            "position": subject["position"],
            "first_source_assertion_reference": deepcopy(references[0]),
            "second_source_assertion_reference": deepcopy(references[1]),
            "first_source_role": "first source Assertion",
            "second_source_role": "second source Assertion",
        }
    content["source_ledger_boundary_identity"] = responsibility.material[
        "source_ledger_boundary_identity"
    ]
    return {
        "subject_address": subject["candidate_address"],
        "content": content,
        "source": deepcopy(references),
        "provenance": "exact source Assertion reference",
        "Authority": deepcopy(responsibility.material["authority"]),
        "Scope": deepcopy(responsibility.material["scope"]),
        "Locality": responsibility.locality_identity,
        "responsible_boundary": "this recorded Assertion",
        "result": "Candidate",
        "relation": "Unknown",
        "conflicts": "Unknown",
        "unknown": ["Candidate relation: Unknown"],
        "limits": [
            "Candidate Act establishes no source Assertion relation",
            "source Assertion coordinates are carried by exact reference",
        ],
    }


def _candidate_result_material(
    responsibility: Event,
    act: Event,
    yield_relation: Event,
) -> dict[str, Any]:
    subject = act.material["required_subject"]
    return {
        "result_identity": act.material["candidate_result_identity"],
        "act_occurrence_identity": act.material["act_occurrence_identity"],
        "exact_act": responsibility.material["candidate_act"],
        "responsibility": responsibility.material["responsibility"],
        "responsibility_reference": _responsibility_reference(responsibility),
        "required_subject": deepcopy(subject),
        "candidate_assertion": _candidate_assertion(responsibility, subject),
        "applicability_result_occurrence_identity": act.material[
            "applicability_result_occurrence_identity"
        ],
        "participation_relation_occurrence_identity": act.material[
            "participation_relation_occurrence_identity"
        ],
        "yield_relation_occurrence_identity": yield_relation.identity,
        "scope": deepcopy(responsibility.material["scope"]),
        "authority": deepcopy(responsibility.material["authority"]),
        "limits": list(responsibility.material["limits"]),
        "unknown": list(responsibility.material["unknown"]),
    }


def _read_applicability_act(
    ledger: EventLedger, event_address: Any
) -> tuple[Event, Event]:
    event = _event(
        ledger,
        event_address,
        message="Candidate production requires one Applicability Act occurrence",
    )
    reference = event.material.get("responsibility_reference")
    responsibility = _read_responsibility(
        ledger,
        reference.get("recorded_occurrence_identity")
        if type(reference) is dict
        else None,
    )
    subject = event.material.get("required_subject")
    addresses = {
        key: _address(event.material.get(key), "Candidate lifecycle address is not exact")
        for key in (
            "applicability_act_identity",
            "applicability_act_occurrence_identity",
            "applicability_result_identity",
            "candidate_act_identity",
            "candidate_act_occurrence_identity",
            "candidate_result_identity",
        )
    }
    if (
        subject not in _required_subjects(responsibility)
        or event.locality_identity != responsibility.locality_identity
        or event.material != _applicability_act_material(
            responsibility, subject, addresses
        )
    ):
        raise ValueError("Candidate Applicability Act occurrence is not exact")
    return event, responsibility


def get_candidate_applicability_act(
    ledger: EventLedger, event_identity: str
) -> dict[str, Any]:
    return deepcopy(_read_applicability_act(ledger, event_identity)[0].material)


def _read_yield_relation(
    ledger: EventLedger,
    event_address: Any,
    *,
    responsibility: Event,
    act_occurrence_address: str,
    result_address: str,
    result_name: str,
) -> Event:
    event = _event(
        ledger,
        event_address,
        message="Candidate production requires one exact Yield relation occurrence",
    )
    if event.material != _yield_relation_material(
        responsibility,
        act_occurrence_address=act_occurrence_address,
        result_address=result_address,
        result_name=result_name,
    ):
        raise ValueError("Candidate Yield relation occurrence is not exact")
    return event


def get_candidate_yield_relation(
    ledger: EventLedger, event_identity: str
) -> dict[str, Any]:
    event = _event(
        ledger,
        event_identity,
        message="Candidate production requires one exact Yield relation occurrence",
    )
    return deepcopy(event.material)


def _read_applicability_result(
    ledger: EventLedger, event_address: Any
) -> tuple[Event, Event, Event]:
    event = _event(
        ledger,
        event_address,
        message="Candidate production requires one Applicability result",
    )
    reference = event.material.get("responsibility_reference")
    responsibility = _read_responsibility(
        ledger,
        reference.get("recorded_occurrence_identity")
        if type(reference) is dict
        else None,
    )
    applicability_acts = tuple(
        candidate
        for candidate in ledger.iter_locality_kind(
            event.locality_identity, CANDIDATE_OCCURRENCE_STREAM
        )
        if candidate.material.get("applicability_result_identity")
        == event.material.get("result_identity")
    )
    if len(applicability_acts) != 1:
        raise ValueError("Candidate Applicability result requires one exact Act")
    act, exact_responsibility = _read_applicability_act(
        ledger, applicability_acts[0].identity
    )
    if exact_responsibility.identity != responsibility.identity:
        raise ValueError("Candidate Applicability result crosses Responsibilities")
    yield_relation = _read_yield_relation(
        ledger,
        event.material.get("yield_relation_occurrence_identity"),
        responsibility=responsibility,
        act_occurrence_address=act.material["applicability_act_occurrence_identity"],
        result_address=act.material["applicability_result_identity"],
        result_name="Applicability result",
    )
    if event.material != _applicability_result_material(
        responsibility, act, yield_relation
    ):
        raise ValueError("Candidate Applicability result is not exact")
    ledger.occurrences_in_append_order(
        (act.identity, yield_relation.identity, event.identity),
        locality_identity=event.locality_identity,
    )
    return event, act, responsibility


def get_candidate_applicability_result(
    ledger: EventLedger, event_identity: str
) -> dict[str, Any]:
    return deepcopy(_read_applicability_result(ledger, event_identity)[0].material)


def _read_participation(
    ledger: EventLedger, event_address: Any
) -> tuple[Event, Event, Event, Event]:
    event = _event(
        ledger,
        event_address,
        message="Candidate production requires one Participation occurrence",
    )
    applicability, applicability_act, responsibility = _read_applicability_result(
        ledger, event.material.get("applicability_result_occurrence_identity")
    )
    if event.material != _participation_material(
        responsibility, applicability, applicability_act
    ):
        raise ValueError("Candidate Participation occurrence is not exact")
    ledger.occurrences_in_append_order(
        (applicability.identity, event.identity),
        locality_identity=event.locality_identity,
    )
    return event, applicability, applicability_act, responsibility


def get_candidate_participation(
    ledger: EventLedger, event_identity: str
) -> dict[str, Any]:
    return deepcopy(_read_participation(ledger, event_identity)[0].material)


def _read_candidate_act(
    ledger: EventLedger, event_address: Any
) -> tuple[Event, Event, Event, Event, Event]:
    event = _event(
        ledger,
        event_address,
        message="Candidate production requires one Candidate Act occurrence",
    )
    participation, applicability, applicability_act, responsibility = (
        _read_participation(
            ledger, event.material.get("participation_relation_occurrence_identity")
        )
    )
    if event.material != _candidate_act_material(
        responsibility, applicability, applicability_act, participation
    ):
        raise ValueError("Candidate Act occurrence is not exact")
    ledger.occurrences_in_append_order(
        (participation.identity, event.identity),
        locality_identity=event.locality_identity,
    )
    return event, participation, applicability, applicability_act, responsibility


def get_candidate_act(ledger: EventLedger, event_identity: str) -> dict[str, Any]:
    return deepcopy(_read_candidate_act(ledger, event_identity)[0].material)


def _read_candidate_result(
    ledger: EventLedger, event_address: Any
) -> tuple[Event, Event, Event]:
    event = _event(
        ledger,
        event_address,
        message="Candidate production requires one exact Candidate result",
    )
    candidate_acts = tuple(
        candidate
        for candidate in ledger.iter_locality_kind(
            event.locality_identity, CANDIDATE_OCCURRENCE_STREAM
        )
        if (
            candidate.material.get("act")
            in {ONE_SOURCE_CANDIDATE_ACT, ORDERED_PAIR_CANDIDATE_ACT}
            and candidate.material.get("candidate_result_identity")
            == event.material.get("result_identity")
        )
    )
    if len(candidate_acts) != 1:
        raise ValueError("Candidate result requires one exact Candidate Act")
    act, _participation, _applicability, _applicability_act, responsibility = (
        _read_candidate_act(ledger, candidate_acts[0].identity)
    )
    yield_relation = _read_yield_relation(
        ledger,
        event.material.get("yield_relation_occurrence_identity"),
        responsibility=responsibility,
        act_occurrence_address=act.material["act_occurrence_identity"],
        result_address=act.material["candidate_result_identity"],
        result_name="Candidate result",
    )
    if event.material != _candidate_result_material(
        responsibility, act, yield_relation
    ):
        raise ValueError("Candidate result is not exact")
    ledger.occurrences_in_append_order(
        (act.identity, yield_relation.identity, event.identity),
        locality_identity=event.locality_identity,
    )
    return event, act, responsibility


def get_recorded_candidate_result(
    ledger: EventLedger, event_identity: str
) -> dict[str, Any]:
    return deepcopy(_read_candidate_result(ledger, event_identity)[0].material)


def candidate_assertion_from_result(
    ledger: EventLedger, *, candidate_result_event_identity: str
) -> dict[str, Any]:
    return deepcopy(
        _read_candidate_result(ledger, candidate_result_event_identity)[0].material[
            "candidate_assertion"
        ]
    )


def candidate_responsibility_progress(
    ledger: EventLedger, *, responsibility_event_identity: str
) -> CandidateResponsibilityProgress:
    responsibility = _read_responsibility(ledger, responsibility_event_identity)
    required = _required_subjects(responsibility)
    required_addresses = tuple(subject["candidate_address"] for subject in required)
    recorded: list[tuple[str, str]] = []
    for event in ledger.iter_locality_kind(
        responsibility.locality_identity, CANDIDATE_OCCURRENCE_STREAM
    ):
        if type(event.material.get("candidate_assertion")) is not dict:
            continue
        result, _act, result_responsibility = _read_candidate_result(
            ledger, event.identity
        )
        if result_responsibility.identity != responsibility.identity:
            continue
        candidate_address = result.material["required_subject"]["candidate_address"]
        recorded.append((candidate_address, result.identity))
    recorded_addresses = tuple(address for address, _result in recorded)
    if len(recorded_addresses) != len(set(recorded_addresses)) or any(
        address not in required_addresses for address in recorded_addresses
    ):
        raise ValueError("Candidate Responsibility results cross its required subjects")
    recorded_set = set(recorded_addresses)
    return CandidateResponsibilityProgress(
        required_candidate_addresses=required_addresses,
        recorded_candidate_result_occurrences=tuple(
            result for _address_value, result in recorded
        ),
        owed_candidate_addresses=tuple(
            address for address in required_addresses if address not in recorded_set
        ),
    )


def _record_one_candidate_result(
    ledger: EventLedger, responsibility: Event, subject: dict[str, Any]
) -> Event:
    addresses = _lifecycle_addresses()
    with ledger.batched():
        applicability_act = ledger.append(
            CANDIDATE_OCCURRENCE_STREAM,
            _applicability_act_material(responsibility, subject, addresses),
            locality_identity=responsibility.locality_identity,
        )
        applicability_yield = ledger.append(
            CANDIDATE_OCCURRENCE_STREAM,
            _yield_relation_material(
                responsibility,
                act_occurrence_address=addresses[
                    "applicability_act_occurrence_identity"
                ],
                result_address=addresses["applicability_result_identity"],
                result_name="Applicability result",
            ),
            locality_identity=responsibility.locality_identity,
        )
        applicability = ledger.append(
            CANDIDATE_OCCURRENCE_STREAM,
            _applicability_result_material(
                responsibility, applicability_act, applicability_yield
            ),
            locality_identity=responsibility.locality_identity,
        )
        participation = ledger.append(
            CANDIDATE_OCCURRENCE_STREAM,
            _participation_material(
                responsibility, applicability, applicability_act
            ),
            locality_identity=responsibility.locality_identity,
        )
        candidate_act = ledger.append(
            CANDIDATE_OCCURRENCE_STREAM,
            _candidate_act_material(
                responsibility,
                applicability,
                applicability_act,
                participation,
            ),
            locality_identity=responsibility.locality_identity,
        )
        candidate_yield = ledger.append(
            CANDIDATE_OCCURRENCE_STREAM,
            _yield_relation_material(
                responsibility,
                act_occurrence_address=addresses["candidate_act_occurrence_identity"],
                result_address=addresses["candidate_result_identity"],
                result_name="Candidate result",
            ),
            locality_identity=responsibility.locality_identity,
        )
        result = ledger.append(
            CANDIDATE_OCCURRENCE_STREAM,
            _candidate_result_material(
                responsibility, candidate_act, candidate_yield
            ),
            locality_identity=responsibility.locality_identity,
        )
    return result


def record_one_owed_candidate_result(
    ledger: EventLedger, *, responsibility_event_identity: str
) -> YieldedCandidateResult | None:
    """Record one owed subject in source order, used only for durable serialization."""

    responsibility = _read_responsibility(ledger, responsibility_event_identity)
    progress = candidate_responsibility_progress(
        ledger, responsibility_event_identity=responsibility.identity
    )
    if not progress.owed_candidate_addresses:
        return None
    owed_address = progress.owed_candidate_addresses[0]
    subject = next(
        subject
        for subject in _required_subjects(responsibility)
        if subject["candidate_address"] == owed_address
    )
    result = _record_one_candidate_result(ledger, responsibility, subject)
    return YieldedCandidateResult(
        result_occurrence=result,
        progress=candidate_responsibility_progress(
            ledger, responsibility_event_identity=responsibility.identity
        ),
    )


def yield_candidate_results(
    ledger: EventLedger, *, responsibility_event_identity: str
) -> Iterator[YieldedCandidateResult]:
    """Yield control after each exact result while preserving every owed subject."""

    responsibility = _read_responsibility(ledger, responsibility_event_identity)
    required = _required_subjects(responsibility)
    initial = candidate_responsibility_progress(
        ledger, responsibility_event_identity=responsibility.identity
    )
    owed = set(initial.owed_candidate_addresses)
    owed_subjects = tuple(
        subject for subject in required if subject["candidate_address"] in owed
    )
    recorded = list(initial.recorded_candidate_result_occurrences)
    for position, subject in enumerate(owed_subjects):
        result = _record_one_candidate_result(ledger, responsibility, subject)
        recorded.append(result.identity)
        yield YieldedCandidateResult(
            result_occurrence=result,
            progress=CandidateResponsibilityProgress(
                required_candidate_addresses=initial.required_candidate_addresses,
                recorded_candidate_result_occurrences=tuple(recorded),
                owed_candidate_addresses=tuple(
                    later["candidate_address"]
                    for later in owed_subjects[position + 1 :]
                ),
            ),
        )


def record_one_source_and_ordered_pair_candidate_responsibilities(
    ledger: EventLedger,
    *,
    one_source_recording_locality_identity: str,
    ordered_pair_recording_locality_identity: str,
    source_append_boundary: EventLedgerBoundary | None = None,
) -> tuple[Event, Event]:
    """Record both Responsibilities through one frozen source boundary."""

    boundary = source_append_boundary or ledger.append_boundary()
    return (
        record_one_source_candidate_responsibility(
            ledger,
            source_append_boundary=boundary,
            recording_locality_identity=one_source_recording_locality_identity,
        ),
        record_ordered_pair_candidate_responsibility(
            ledger,
            source_append_boundary=boundary,
            recording_locality_identity=ordered_pair_recording_locality_identity,
        ),
    )


def boundaries_of_recorded_candidate_result(
    ledger: EventLedger, event_identity: str
) -> dict[str, EventLedgerBoundary]:
    event, _act, responsibility = _read_candidate_result(ledger, event_identity)
    return {
        "source_ledger_boundary": _boundary(
            ledger, responsibility.material["source_ledger_boundary_identity"]
        ),
        "candidate_result_ledger_boundary": ledger.append_boundary_through_occurrence(
            event.identity
        ),
    }
