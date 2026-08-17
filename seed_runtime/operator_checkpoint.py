"""Operator shorthand for recording one exact Standing-boundary reference."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from typing import Any

from seed_runtime.event import Event
from seed_runtime.events import CORRUPTED, EventLedger
from seed_runtime.identities import new_identity
from seed_runtime.operator_command import AddressedOperatorCommand
from seed_runtime.operator_representation import read_operator_representation
from seed_runtime.evidence_of_yield_relation import (
    RECORDED_EVIDENCE_OF_YIELD_RELATION_KIND,
    _record_evidence_of_yield_relation,
    read_requirements_of_yield_relation,
)


STANDING_BOUNDARY_REFERENCE_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND = (
    "operator.standing_boundary_reference_responsibility_assignment_recorded"
)
STANDING_BOUNDARY_REFERENCE_ACT_EVIDENCE_KIND = (
    "operator.standing_boundary_reference_act_evidenced"
)
STANDING_BOUNDARY_REFERENCE_RECORDED_KIND = (
    "operator.standing_boundary_reference_recorded"
)
STANDING_BOUNDARY_REFERENCE_RESULT_KIND = "recorded Standing boundary reference result"
STANDING_BOUNDARY_REFERENCE_ACT = "Record one exact Standing boundary reference"
STANDING_BOUNDARY_REFERENCE_RESPONSIBILITY = (
    "record one exact addressed Representation and its exact Standing boundary "
    "in one durable bounded record"
)
STANDING_BOUNDARY_REFERENCE_BOOK_CLAUSE = "05.Recording.D"
EVENT_KIND_RESPONSIBILITIES = {
    STANDING_BOUNDARY_REFERENCE_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND: (
        "05.Recording.D"
    ),
    STANDING_BOUNDARY_REFERENCE_ACT_EVIDENCE_KIND: "02.Acts.A",
    STANDING_BOUNDARY_REFERENCE_RECORDED_KIND: "05.Recording.D",
}


class OperatorCheckpointError(ValueError):
    """One exact Standing-boundary reference could not be recorded."""


@dataclass(frozen=True)
class OperatorCheckpointRequest:
    pass


def request_operator_checkpoint(
    addressed: AddressedOperatorCommand,
) -> OperatorCheckpointRequest:
    if not isinstance(addressed, AddressedOperatorCommand):
        raise TypeError("checkpoint control requires one addressed command")
    if addressed.frame.exact_bytes not in {
        b"/checkpoint",
        b"/checkpoint\n",
        b"/checkpoint\r\n",
    }:
        raise ValueError("/checkpoint accepts no material")
    return OperatorCheckpointRequest()


def _require_identity(value: Any, message: str) -> str:
    if type(value) is not str or not value:
        raise OperatorCheckpointError(message)
    return value


def _source_reference(
    ledger: EventLedger,
    *,
    addressed_command: AddressedOperatorCommand,
    locality_standing: dict[str, Any],
) -> dict[str, str | None]:
    if not isinstance(addressed_command, AddressedOperatorCommand):
        raise TypeError("checkpoint requires one addressed command")
    if type(locality_standing) is not dict:
        raise OperatorCheckpointError("checkpoint requires exact Locality Standing")
    locality_identity = addressed_command.locality_identity
    representation_identity = (
        addressed_command.addressed_at_representation_event_identity
    )
    _require_identity(locality_identity, "checkpoint requires one exact Locality")
    _require_identity(
        representation_identity,
        "checkpoint requires one addressed Representation",
    )
    if locality_standing.get("locality_identity") != locality_identity:
        raise OperatorCheckpointError("checkpoint has a different Standing Locality")
    if locality_standing.get("through_event_occurrence_identity") != representation_identity:
        raise OperatorCheckpointError(
            "checkpoint requires the exact addressed Representation Standing"
        )
    try:
        representation = read_operator_representation(
            ledger, representation_identity
        )
    except ValueError as error:
        raise OperatorCheckpointError(
            "checkpoint requires one intact addressed Representation"
        ) from error
    representation_event = ledger.get(representation_identity)
    if (
        representation["locality_identity"] != locality_identity
        or representation_event is None
        or ledger.integrity_of(representation_identity) == CORRUPTED
        or "locality_standing_through_event_occurrence_identity"
        not in representation_event.material
    ):
        raise OperatorCheckpointError(
            "checkpoint has a different Representation Locality"
        )
    boundary = representation_event.material[
        "locality_standing_through_event_occurrence_identity"
    ]
    if boundary is not None:
        _require_identity(
            boundary,
            "checkpoint requires one exact Standing boundary",
        )
        occurrences = ledger.list_locality(locality_identity)
        positions = {event.identity: index for index, event in enumerate(occurrences)}
        boundary_event = ledger.get(boundary)
        if (
            boundary_event is None
            or boundary_event.locality_identity != locality_identity
            or positions.get(boundary, len(occurrences))
            >= positions.get(representation_identity, -1)
            or ledger.integrity_of(boundary) == CORRUPTED
        ):
            raise OperatorCheckpointError(
                "checkpoint requires its intact exact Standing boundary"
            )
    return {
        "source_locality_identity": locality_identity,
        "addressed_representation_event_identity": representation_identity,
        "standing_boundary_event_identity": boundary,
    }


def _authority() -> dict[str, str]:
    return {
        "source": "active Book",
        "book_clause_identity": STANDING_BOUNDARY_REFERENCE_BOOK_CLAUSE,
        "standing": "bounded",
        "limit": "bounded to this exact record",
    }


def _assignment_material(
    *,
    assignment_identity: str,
    assignment_subject_identity: str,
    recording_act_identity: str,
    act_occurrence_identity: str,
    result_identity: str,
    scope_identity: str,
    source_reference: dict[str, str | None],
) -> dict[str, Any]:
    return {
        "assignment_identity": assignment_identity,
        "assignment_subject_identity": assignment_subject_identity,
        "book_clause_identity": STANDING_BOUNDARY_REFERENCE_BOOK_CLAUSE,
        "responsibility": STANDING_BOUNDARY_REFERENCE_RESPONSIBILITY,
        "responsible_boundary": "this Seed",
        "recording_act_identity": recording_act_identity,
        "act_occurrence_identity": act_occurrence_identity,
        "result_identity": result_identity,
        "source_reference": deepcopy(source_reference),
        "scope": {
            "scope_identity": scope_identity,
            **deepcopy(source_reference),
        },
        "evidence_occurrence_reference": source_reference[
            "addressed_representation_event_identity"
        ],
        "authority": _authority(),
        "limits": [
            "record existence establishes no represented relation or Standing revision",
            "this record establishes no movement or Locality relation",
        ],
        "unknown": [
            "Applicability of the recorded boundary to another Act remains Unknown"
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


def _act_material(assignment: Event) -> dict[str, Any]:
    return {
        "recording_act_identity": assignment.material["recording_act_identity"],
        "act_occurrence_identity": assignment.material["act_occurrence_identity"],
        "act": STANDING_BOUNDARY_REFERENCE_ACT,
        "responsibility": STANDING_BOUNDARY_REFERENCE_RESPONSIBILITY,
        "responsible_boundary": "this Seed",
        "responsibility_assignment_reference": _assignment_reference(assignment),
        "source_reference": deepcopy(assignment.material["source_reference"]),
        "scope": deepcopy(assignment.material["scope"]),
        "result_identity": assignment.material["result_identity"],
        "authority": _authority(),
        "evidence_scope": "Evidence bounded to this exact record occurrence",
    }


def _result_material(act_evidence: Event) -> dict[str, Any]:
    return {
        "result_identity": act_evidence.material["result_identity"],
        "recording_act_identity": act_evidence.material["recording_act_identity"],
        "act_occurrence_identity": act_evidence.material["act_occurrence_identity"],
        "exact_act": STANDING_BOUNDARY_REFERENCE_ACT,
        "responsibility": STANDING_BOUNDARY_REFERENCE_RESPONSIBILITY,
        "responsible_boundary": "this Seed",
        "responsibility_assignment_reference": deepcopy(
            act_evidence.material["responsibility_assignment_reference"]
        ),
        "source_reference": deepcopy(act_evidence.material["source_reference"]),
        "scope": deepcopy(act_evidence.material["scope"]),
        "authority": _authority(),
        "standing": "recorded",
        "limits": [
            "record existence establishes no represented relation or Standing revision",
            "this record establishes no movement or Locality relation",
        ],
        "unknown": [
            "Applicability of the recorded boundary to another Act remains Unknown"
        ],
    }


def _recorded_result_material(
    result_material: dict[str, Any],
    *,
    responsible_act_evidence_identity: str,
    evidence_of_yield_relation_identity: str,
) -> dict[str, Any]:
    return {
        "result_identity": result_material["result_identity"],
        "recording_act_identity": result_material["recording_act_identity"],
        "act_occurrence_identity": result_material["act_occurrence_identity"],
        "exact_act": result_material["exact_act"],
        "responsibility": result_material["responsibility"],
        "responsible_boundary": result_material["responsible_boundary"],
        "responsibility_assignment_reference": deepcopy(
            result_material["responsibility_assignment_reference"]
        ),
        "source_reference": deepcopy(result_material["source_reference"]),
        "scope": deepcopy(result_material["scope"]),
        "authority": deepcopy(result_material["authority"]),
        "standing": result_material["standing"],
        "limits": list(result_material["limits"]),
        "unknown": list(result_material["unknown"]),
        "responsible_act_evidence_identity": responsible_act_evidence_identity,
        "evidence_of_yield_relation_identity": evidence_of_yield_relation_identity,
    }


def record_standing_boundary_reference_responsibility_assignment(
    ledger: EventLedger,
    *,
    addressed_command: AddressedOperatorCommand,
    locality_standing: dict[str, Any],
) -> Event:
    """Assign one exact addressed Representation boundary record in this Locality."""

    if not isinstance(ledger, EventLedger):
        raise TypeError("checkpoint requires one EventLedger")
    source_reference = _source_reference(
        ledger,
        addressed_command=addressed_command,
        locality_standing=locality_standing,
    )
    identities = {
        "assignment_identity": new_identity("standing_boundary_reference_assignment"),
        "assignment_subject_identity": new_identity(
            "standing_boundary_reference_assignment_subject"
        ),
        "recording_act_identity": new_identity(
            "standing_boundary_reference_recording_act"
        ),
        "act_occurrence_identity": new_identity(
            "standing_boundary_reference_act_occurrence"
        ),
        "result_identity": new_identity("standing_boundary_reference_result"),
        "scope_identity": new_identity("standing_boundary_reference_scope"),
    }
    return ledger.append(
        STANDING_BOUNDARY_REFERENCE_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND,
        _assignment_material(source_reference=source_reference, **identities),
        locality_identity=addressed_command.locality_identity,
    )


def get_standing_boundary_reference_responsibility_assignment(
    ledger: EventLedger, event_identity: str
) -> Event:
    _require_identity(event_identity, "checkpoint requires one assignment occurrence")
    event = ledger.get(event_identity)
    if (
        event is None
        or event.kind
        != STANDING_BOUNDARY_REFERENCE_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND
        or type(event.locality_identity) is not str
        or event.exact_material is not None
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise OperatorCheckpointError("checkpoint assignment is absent or corrupted")
    material = event.material
    source_reference = material.get("source_reference")
    scope = material.get("scope")
    identities = (
        material.get("assignment_identity"),
        material.get("assignment_subject_identity"),
        material.get("recording_act_identity"),
        material.get("act_occurrence_identity"),
        material.get("result_identity"),
        scope.get("scope_identity") if type(scope) is dict else None,
    )
    if any(type(value) is not str or not value for value in identities) or len(
        set(identities)
    ) != len(identities):
        raise OperatorCheckpointError("checkpoint assignment identities are not exact")
    if type(source_reference) is not dict:
        raise OperatorCheckpointError("checkpoint assignment carries no source reference")
    representation = ledger.get(
        source_reference.get("addressed_representation_event_identity")
    )
    if (
        representation is None
        or representation.locality_identity != event.locality_identity
        or ledger.integrity_of(representation.identity) == CORRUPTED
    ):
        raise OperatorCheckpointError("checkpoint assignment carries no Representation")
    try:
        read_operator_representation(ledger, representation.identity)
    except ValueError as error:
        raise OperatorCheckpointError(
            "checkpoint assignment carries no intact Representation"
        ) from error
    boundary = representation.material.get(
        "locality_standing_through_event_occurrence_identity"
    )
    if boundary is not None:
        boundary_event = ledger.get(boundary)
        positions = {
            occurrence.identity: index
            for index, occurrence in enumerate(
                ledger.list_locality(event.locality_identity)
            )
        }
        if (
            boundary_event is None
            or boundary_event.locality_identity != event.locality_identity
            or positions.get(boundary, len(positions))
            >= positions.get(representation.identity, -1)
            or ledger.integrity_of(boundary) == CORRUPTED
        ):
            raise OperatorCheckpointError(
                "checkpoint assignment carries no intact exact Standing boundary"
            )
    expected_source = {
        "source_locality_identity": event.locality_identity,
        "addressed_representation_event_identity": representation.identity,
        "standing_boundary_event_identity": boundary,
    }
    expected = _assignment_material(
        assignment_identity=identities[0],
        assignment_subject_identity=identities[1],
        recording_act_identity=identities[2],
        act_occurrence_identity=identities[3],
        result_identity=identities[4],
        scope_identity=identities[5],
        source_reference=expected_source,
    )
    if source_reference != expected_source or material != expected:
        raise OperatorCheckpointError("checkpoint assignment is not exact")
    return event


def record_standing_boundary_reference_responsible_act_evidence(
    ledger: EventLedger,
    *,
    responsibility_assignment_event_identity: str,
    responsibility_assignment_standing: dict[str, Any],
) -> Event:
    assignment = get_standing_boundary_reference_responsibility_assignment(
        ledger, responsibility_assignment_event_identity
    )
    if type(responsibility_assignment_standing) is not dict:
        raise OperatorCheckpointError("checkpoint Act requires assignment Standing")
    carried = responsibility_assignment_standing.get(
        "responsibility_assignment_occurrences"
    )
    if (
        responsibility_assignment_standing.get("locality_identity")
        != assignment.locality_identity
        or type(carried) is not dict
        or carried.get(assignment.identity, object()) is not None
    ):
        raise OperatorCheckpointError("checkpoint Act requires its carried assignment")
    return ledger.append(
        STANDING_BOUNDARY_REFERENCE_ACT_EVIDENCE_KIND,
        _act_material(assignment),
        locality_identity=assignment.locality_identity,
    )


def get_standing_boundary_reference_act_evidence(
    ledger: EventLedger, event_identity: str
) -> Event:
    _require_identity(event_identity, "checkpoint requires one Act Evidence occurrence")
    event = ledger.get(event_identity)
    if (
        event is None
        or event.kind != STANDING_BOUNDARY_REFERENCE_ACT_EVIDENCE_KIND
        or event.exact_material is not None
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise OperatorCheckpointError("checkpoint Act Evidence is absent or corrupted")
    reference = event.material.get("responsibility_assignment_reference")
    if type(reference) is not dict:
        raise OperatorCheckpointError("checkpoint Act carries no assignment")
    assignment = get_standing_boundary_reference_responsibility_assignment(
        ledger, reference.get("recorded_occurrence_identity")
    )
    if (
        assignment.locality_identity != event.locality_identity
        or reference != _assignment_reference(assignment)
        or event.material != _act_material(assignment)
    ):
        raise OperatorCheckpointError("checkpoint Act Evidence is not exact")
    try:
        ledger.occurrences_in_append_order(
            (assignment.identity, event.identity),
            locality_identity=event.locality_identity,
        )
    except ValueError as error:
        raise OperatorCheckpointError("checkpoint Act requires its prior assignment") from error
    return event


def record_standing_boundary_reference_result(
    ledger: EventLedger,
    *,
    responsible_act_evidence_event_identity: str,
) -> Event:
    act_evidence = get_standing_boundary_reference_act_evidence(
        ledger, responsible_act_evidence_event_identity
    )
    for evidence in ledger.iter_locality_kind(
        act_evidence.locality_identity, RECORDED_EVIDENCE_OF_YIELD_RELATION_KIND
    ):
        if evidence.material.get("responsible_act_evidence_identity") == act_evidence.identity:
            raise OperatorCheckpointError("checkpoint Act already carries a Yield")
    result_material = _result_material(act_evidence)
    evidence = _record_evidence_of_yield_relation(
        ledger,
        locality_identity=act_evidence.locality_identity,
        exact_act=STANDING_BOUNDARY_REFERENCE_ACT,
        act_occurrence_identity=act_evidence.material["act_occurrence_identity"],
        responsible_act_evidence_identity=act_evidence.identity,
        result_kind=STANDING_BOUNDARY_REFERENCE_RESULT_KIND,
        result_identity=result_material["result_identity"],
        result_content=result_material,
        responsibility=STANDING_BOUNDARY_REFERENCE_RESPONSIBILITY,
        live_boundary="standing_boundary_reference",
        responsible_boundary="this Seed",
    )
    return ledger.append(
        STANDING_BOUNDARY_REFERENCE_RECORDED_KIND,
        _recorded_result_material(
            result_material,
            responsible_act_evidence_identity=act_evidence.identity,
            evidence_of_yield_relation_identity=evidence.identity,
        ),
        locality_identity=act_evidence.locality_identity,
    )


def get_recorded_standing_boundary_reference(
    ledger: EventLedger, event_identity: str
) -> dict[str, Any]:
    _require_identity(event_identity, "checkpoint requires one recorded result")
    event = ledger.get(event_identity)
    if (
        event is None
        or event.kind != STANDING_BOUNDARY_REFERENCE_RECORDED_KIND
        or event.exact_material is not None
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise OperatorCheckpointError("checkpoint record is absent or corrupted")
    act = get_standing_boundary_reference_act_evidence(
        ledger, event.material.get("responsible_act_evidence_identity")
    )
    expected_result = _result_material(act)
    expected = _recorded_result_material(
        expected_result,
        responsible_act_evidence_identity=act.identity,
        evidence_of_yield_relation_identity=event.material.get("evidence_of_yield_relation_identity"),
    )
    if event.locality_identity != act.locality_identity or event.material != expected:
        raise OperatorCheckpointError("checkpoint record coordinates are not exact")
    requirements = read_requirements_of_yield_relation(
        ledger,
        recorded_result_event_identity=event.identity,
        evidence_of_yield_relation_event_identity=event.material["evidence_of_yield_relation_identity"],
        responsible_act_evidence_event_identity=act.identity,
    )
    if not all(requirements.values()):
        raise OperatorCheckpointError("checkpoint record carries no exact Yield")
    return deepcopy(event.material)
