"""Operator shorthand for recording one exact through-occurrence reference."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from typing import Any

from seed_runtime.event import Event
from seed_runtime.events import CORRUPTED, EventLedger
from seed_runtime.operator_command import AddressedOperatorCommand
from seed_runtime.yield_relation import (
    RECORDED_YIELD_RELATION_EVENT,
    _record_yield_relation,
    read_requirements_of_yield_relation,
)


THROUGH_OCCURRENCE_BOUNDARY_REFERENCE_SUBJECT_TO_ACT_BINDING_RECORDED_KIND = (
    "operator.through_occurrence_boundary_reference_subject_to_act_binding_recorded"
)
THROUGH_OCCURRENCE_BOUNDARY_REFERENCE_ACT_OCCURRENCE_EVENT = (
    "operator.through_occurrence_boundary_reference_act_occurrence_recorded"
)
THROUGH_OCCURRENCE_BOUNDARY_REFERENCE_RECORDED_KIND = (
    "operator.through_occurrence_boundary_reference_recorded"
)
THROUGH_OCCURRENCE_BOUNDARY_REFERENCE_RESULT_KIND = (
    "recorded through-occurrence boundary reference result"
)
THROUGH_OCCURRENCE_BOUNDARY_REFERENCE_ACT = (
    "Recording of one exact through-occurrence boundary reference"
)
THROUGH_OCCURRENCE_BOUNDARY_REFERENCE_BOOK_CLAUSE = "05.Recording.D"
EVENT_KIND_BOOK_CLAUSES = {
    THROUGH_OCCURRENCE_BOUNDARY_REFERENCE_SUBJECT_TO_ACT_BINDING_RECORDED_KIND: (
        "05.Recording.D"
    ),
    THROUGH_OCCURRENCE_BOUNDARY_REFERENCE_ACT_OCCURRENCE_EVENT: "02.Acts.A",
    THROUGH_OCCURRENCE_BOUNDARY_REFERENCE_RECORDED_KIND: "05.Recording.D",
}


class OperatorCheckpointError(ValueError):
    """One exact through-occurrence reference could not be recorded."""


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
    current_coordinates: dict[str, Any],
) -> dict[str, str | None]:
    if not isinstance(addressed_command, AddressedOperatorCommand):
        raise TypeError("checkpoint requires one addressed command")
    if type(current_coordinates) is not dict:
        raise OperatorCheckpointError("checkpoint requires exact current coordinates")
    locality_identity = addressed_command.locality_identity
    boundary_identity = (
        addressed_command.addressed_through_event_occurrence_identity
    )
    _require_identity(locality_identity, "checkpoint requires one exact Locality")
    _require_identity(
        boundary_identity,
        "checkpoint requires one addressed through-occurrence boundary",
    )
    if current_coordinates.get("locality_identity") != locality_identity:
        raise OperatorCheckpointError("checkpoint has a different Locality")
    if current_coordinates.get("through_event_occurrence_identity") != boundary_identity:
        raise OperatorCheckpointError(
            "checkpoint requires the exact addressed through-occurrence boundary"
        )
    boundary_event = ledger.get(boundary_identity)
    if (
        boundary_event is None
        or boundary_event.locality_identity != locality_identity
        or ledger.integrity_of(boundary_identity) == CORRUPTED
    ):
        raise OperatorCheckpointError(
            "checkpoint has no intact addressed through-occurrence boundary"
        )
    return {
        "source_locality_identity": locality_identity,
        "through_event_occurrence_identity": boundary_identity,
    }


def _binding_material(
    *,
    exact_act_identity: str,
    act_occurrence_identity: str,
    result_identity: str,
    source_reference: dict[str, str | None],
) -> dict[str, Any]:
    return {
        "book_clause_identity": THROUGH_OCCURRENCE_BOUNDARY_REFERENCE_BOOK_CLAUSE,
        "subject_reference": deepcopy(source_reference),
        "act": THROUGH_OCCURRENCE_BOUNDARY_REFERENCE_ACT,
        "exact_act_identity": exact_act_identity,
        "act_occurrence_identity": act_occurrence_identity,
        "result_identity": result_identity,
    }


def _binding_reference(binding: Event) -> dict[str, Any]:
    return {
        "recorded_occurrence_identity": binding.identity,
        "book_clause_identity": binding.material["book_clause_identity"],
        "exact_act_identity": binding.material["exact_act_identity"],
        "subject_reference": deepcopy(binding.material["subject_reference"]),
    }


def _act_material(binding: Event) -> dict[str, Any]:
    return {
        "exact_act_identity": binding.material["exact_act_identity"],
        "act_occurrence_identity": binding.material["act_occurrence_identity"],
        "act": THROUGH_OCCURRENCE_BOUNDARY_REFERENCE_ACT,
        "subject_to_act_binding_reference": _binding_reference(binding),
        "result_identity": binding.material["result_identity"],
    }


def _result_material(act_occurrence: Event) -> dict[str, Any]:
    return {
        "result_identity": act_occurrence.material["result_identity"],
        "exact_act_identity": act_occurrence.material["exact_act_identity"],
        "act_occurrence_identity": act_occurrence.material["act_occurrence_identity"],
        "exact_act": THROUGH_OCCURRENCE_BOUNDARY_REFERENCE_ACT,
        "subject_to_act_binding_reference": deepcopy(
            act_occurrence.material["subject_to_act_binding_reference"]
        ),
        "source_reference": deepcopy(
            act_occurrence.material["subject_to_act_binding_reference"][
                "subject_reference"
            ]
        ),
    }


def _recorded_result_material(
    result_material: dict[str, Any],
    *,
    act_occurrence_event_identity: str,
    yield_relation_identity: str,
) -> dict[str, Any]:
    return {
        "result_identity": result_material["result_identity"],
        "exact_act_identity": result_material["exact_act_identity"],
        "act_occurrence_identity": result_material["act_occurrence_identity"],
        "exact_act": result_material["exact_act"],
        "subject_to_act_binding_reference": deepcopy(
            result_material["subject_to_act_binding_reference"]
        ),
        "source_reference": deepcopy(result_material["source_reference"]),
        "act_occurrence_event_identity": act_occurrence_event_identity,
        "yield_relation_identity": yield_relation_identity,
    }


def record_through_occurrence_boundary_reference_subject_to_act_binding(
    ledger: EventLedger,
    *,
    addressed_command: AddressedOperatorCommand,
    current_coordinates: dict[str, Any],
) -> Event:
    """Bind one exact addressed boundary reference to its recording Act."""

    if not isinstance(ledger, EventLedger):
        raise TypeError("checkpoint requires one EventLedger")
    source_reference = _source_reference(
        ledger,
        addressed_command=addressed_command,
        current_coordinates=current_coordinates,
    )
    identities = {
        "exact_act_identity": ledger.mint_identity(
            "through_occurrence_boundary_reference_recording_act"
        ),
        "act_occurrence_identity": ledger.mint_identity(
            "through_occurrence_boundary_reference_act_occurrence"
        ),
        "result_identity": ledger.mint_identity(
            "through_occurrence_boundary_reference_result"
        ),
    }
    return ledger.append(
        THROUGH_OCCURRENCE_BOUNDARY_REFERENCE_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
        _binding_material(source_reference=source_reference, **identities),
        locality_identity=addressed_command.locality_identity,
    )


def get_through_occurrence_boundary_reference_subject_to_act_binding(
    ledger: EventLedger, event_identity: str
) -> Event:
    _require_identity(event_identity, "checkpoint requires one binding occurrence")
    event = ledger.get(event_identity)
    if (
        event is None
        or event.kind
        != THROUGH_OCCURRENCE_BOUNDARY_REFERENCE_SUBJECT_TO_ACT_BINDING_RECORDED_KIND
        or type(event.locality_identity) is not str
        or event.exact_material is not None
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise OperatorCheckpointError("checkpoint binding is absent or corrupted")
    material = event.material
    source_reference = material.get("subject_reference")
    identities = (
        material.get("exact_act_identity"),
        material.get("act_occurrence_identity"),
        material.get("result_identity"),
    )
    if any(type(value) is not str or not value for value in identities) or len(
        set(identities)
    ) != len(identities):
        raise OperatorCheckpointError("checkpoint binding identities are not exact")
    if type(source_reference) is not dict:
        raise OperatorCheckpointError("checkpoint binding carries no source reference")
    boundary = ledger.get(source_reference.get("through_event_occurrence_identity"))
    if (
        boundary is None
        or boundary.locality_identity != event.locality_identity
        or ledger.integrity_of(boundary.identity) == CORRUPTED
    ):
        raise OperatorCheckpointError(
            "checkpoint binding carries no intact addressed boundary"
        )
    expected_source = {
        "source_locality_identity": event.locality_identity,
        "through_event_occurrence_identity": boundary.identity,
    }
    expected = _binding_material(
        exact_act_identity=identities[0],
        act_occurrence_identity=identities[1],
        result_identity=identities[2],
        source_reference=expected_source,
    )
    if source_reference != expected_source or material != expected:
        raise OperatorCheckpointError("checkpoint binding is not exact")
    return event


def record_through_occurrence_boundary_reference_act_occurrence(
    ledger: EventLedger,
    *,
    subject_to_act_binding_event_identity: str,
    current_coordinates: dict[str, Any],
) -> Event:
    binding = get_through_occurrence_boundary_reference_subject_to_act_binding(
        ledger, subject_to_act_binding_event_identity
    )
    if type(current_coordinates) is not dict:
        raise OperatorCheckpointError("checkpoint Act requires current coordinates")
    carried = current_coordinates.get(
        "subject_to_act_binding_occurrences"
    )
    if (
        current_coordinates.get("locality_identity")
        != binding.locality_identity
        or type(carried) is not dict
        or carried.get(binding.identity, object()) is not None
    ):
        raise OperatorCheckpointError("checkpoint Act requires its carried binding")
    return ledger.append(
        THROUGH_OCCURRENCE_BOUNDARY_REFERENCE_ACT_OCCURRENCE_EVENT,
        _act_material(binding),
        locality_identity=binding.locality_identity,
    )


def get_through_occurrence_boundary_reference_act_occurrence(
    ledger: EventLedger, event_identity: str
) -> Event:
    _require_identity(event_identity, "checkpoint requires one Act occurrence occurrence")
    event = ledger.get(event_identity)
    if (
        event is None
        or event.kind != THROUGH_OCCURRENCE_BOUNDARY_REFERENCE_ACT_OCCURRENCE_EVENT
        or event.exact_material is not None
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise OperatorCheckpointError("checkpoint Act occurrence is absent or corrupted")
    reference = event.material.get("subject_to_act_binding_reference")
    if type(reference) is not dict:
        raise OperatorCheckpointError("checkpoint Act carries no binding")
    binding = get_through_occurrence_boundary_reference_subject_to_act_binding(
        ledger, reference.get("recorded_occurrence_identity")
    )
    if (
        binding.locality_identity != event.locality_identity
        or reference != _binding_reference(binding)
        or event.material != _act_material(binding)
    ):
        raise OperatorCheckpointError("checkpoint Act occurrence is not exact")
    try:
        ledger.occurrences_in_append_order(
            (binding.identity, event.identity),
            locality_identity=event.locality_identity,
        )
    except ValueError as error:
        raise OperatorCheckpointError("checkpoint Act requires its prior binding") from error
    return event


def record_through_occurrence_boundary_reference_result(
    ledger: EventLedger,
    *,
    act_occurrence_event_identity: str,
) -> Event:
    act_occurrence = get_through_occurrence_boundary_reference_act_occurrence(
        ledger, act_occurrence_event_identity
    )
    for yield_relation in ledger.iter_locality_kind(
        act_occurrence.locality_identity, RECORDED_YIELD_RELATION_EVENT
    ):
        if yield_relation.material.get("act_occurrence_event_identity") == act_occurrence.identity:
            raise OperatorCheckpointError("checkpoint Act already carries a Yield")
    result_material = _result_material(act_occurrence)
    yield_relation = _record_yield_relation(
        ledger,
        locality_identity=act_occurrence.locality_identity,
        exact_act=THROUGH_OCCURRENCE_BOUNDARY_REFERENCE_ACT,
        act_occurrence_identity=act_occurrence.material["act_occurrence_identity"],
        act_occurrence_event_identity=act_occurrence.identity,
        result_kind=THROUGH_OCCURRENCE_BOUNDARY_REFERENCE_RESULT_KIND,
        result_identity=result_material["result_identity"],
        result_content=result_material,
        occurrence_boundary="through_occurrence_boundary_reference",
    )
    return ledger.append(
        THROUGH_OCCURRENCE_BOUNDARY_REFERENCE_RECORDED_KIND,
        _recorded_result_material(
            result_material,
            act_occurrence_event_identity=act_occurrence.identity,
            yield_relation_identity=yield_relation.identity,
        ),
        locality_identity=act_occurrence.locality_identity,
    )


def get_recorded_through_occurrence_boundary_reference(
    ledger: EventLedger, event_identity: str
) -> dict[str, Any]:
    _require_identity(event_identity, "checkpoint requires one recorded result")
    event = ledger.get(event_identity)
    if (
        event is None
        or event.kind != THROUGH_OCCURRENCE_BOUNDARY_REFERENCE_RECORDED_KIND
        or event.exact_material is not None
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise OperatorCheckpointError("checkpoint record is absent or corrupted")
    act = get_through_occurrence_boundary_reference_act_occurrence(
        ledger, event.material.get("act_occurrence_event_identity")
    )
    expected_result = _result_material(act)
    expected = _recorded_result_material(
        expected_result,
        act_occurrence_event_identity=act.identity,
        yield_relation_identity=event.material.get("yield_relation_identity"),
    )
    if event.locality_identity != act.locality_identity or event.material != expected:
        raise OperatorCheckpointError("checkpoint record coordinates are not exact")
    requirements = read_requirements_of_yield_relation(
        ledger,
        recorded_result_event_identity=event.identity,
        yield_relation_event_identity=event.material["yield_relation_identity"],
        act_occurrence_event_identity=act.identity,
    )
    if not all(requirements.values()):
        raise OperatorCheckpointError("checkpoint record carries no exact Yield")
    return deepcopy(event.material)
