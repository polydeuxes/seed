"""One exact recorded-boundary Preservation Act and Locality relation."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from seed_runtime.event import Event
from seed_runtime.events import CORRUPTED, EventLedger
from seed_runtime.material_source import read_exact_material_result
from seed_runtime.operator_checkpoint import (
    get_operator_checkpoint_material_occurrence,
    is_operator_checkpoint_material,
)
from seed_runtime.operator_material_source import OPERATOR_MATERIAL_SOURCE_RECORDED_KIND
RECORDED_BOUNDARY_LOCALITY_ACT_OCCURRENCE_EVENT = (
    "operator.recorded_boundary_locality_act_occurrence_recorded"
)
RECORDED_BOUNDARY_LOCALITY_RECORDED_KIND = (
    "operator.recorded_boundary_locality_recorded"
)
RECORDED_BOUNDARY_LOCALITY_ACT = (
    "Preservation"
)
EVENT_KIND_BOOK_CLAUSES = {
    RECORDED_BOUNDARY_LOCALITY_ACT_OCCURRENCE_EVENT: "02.Acts.A",
    RECORDED_BOUNDARY_LOCALITY_RECORDED_KIND: "06.Locality.A",
}


class RecordedBoundaryLocalityError(ValueError):
    """Exact recorded-boundary Locality coordinates are required."""


def _require_identity(value: Any, message: str) -> str:
    if type(value) is not str or not value:
        raise RecordedBoundaryLocalityError(message)
    return value


def _through_occurrence_reference(
    ledger: EventLedger, checkpoint_occurrence_identity: str
) -> dict[str, str]:
    checkpoint = get_operator_checkpoint_material_occurrence(
        ledger, checkpoint_occurrence_identity
    )
    return {
        "recorded_occurrence_identity": checkpoint.identity,
    }


def _resolve_one_carried_reference(
    ledger: EventLedger,
    *,
    source_current_coordinates: dict[str, Any],
) -> dict[str, str]:
    if type(source_current_coordinates) is not dict:
        raise RecordedBoundaryLocalityError(
            "recorded boundary Locality requires exact source current coordinates"
        )
    source_locality = _require_identity(
        source_current_coordinates.get("locality_identity"),
        "recorded boundary Locality requires one source Locality",
    )
    material_results = source_current_coordinates.get("material_result_occurrences")
    relations = source_current_coordinates.get(
        "recorded_boundary_locality_relations"
    )
    if type(material_results) is not list or type(relations) is not dict:
        raise RecordedBoundaryLocalityError(
            "recorded boundary Locality requires exact current-coordinate identities"
        )
    checkpoint_occurrences = []
    for coordinate in material_results:
        if type(coordinate) is not dict:
            raise RecordedBoundaryLocalityError(
                "recorded boundary Locality requires exact material result coordinates"
            )
        occurrence_identity = _require_identity(
            coordinate.get("result_occurrence_identity"),
            "recorded boundary Locality requires exact material result coordinates",
        )
        if coordinate != {
            "subject_reference": occurrence_identity,
            "result_occurrence_identity": occurrence_identity,
        }:
            raise RecordedBoundaryLocalityError(
                "recorded boundary Locality requires exact material result coordinates"
            )
        try:
            event = read_exact_material_result(ledger, occurrence_identity)
        except (TypeError, ValueError) as error:
            raise RecordedBoundaryLocalityError(
                "recorded boundary Locality requires intact material result coordinates; "
                "one is absent or corrupted"
            ) from error
        if event.locality_identity != source_locality:
            raise RecordedBoundaryLocalityError(
                "recorded boundary Locality material has a different Locality"
            )
        if (
            event.kind == OPERATOR_MATERIAL_SOURCE_RECORDED_KIND
            and is_operator_checkpoint_material(event.exact_material)
        ):
            get_operator_checkpoint_material_occurrence(ledger, event.identity)
            checkpoint_occurrences.append(event.identity)
    carried_occurrences = [
        *checkpoint_occurrences,
        *(identity for identity, value in relations.items() if value is None),
    ]
    if len(carried_occurrences) != len(checkpoint_occurrences) + len(relations):
        raise RecordedBoundaryLocalityError(
            "recorded boundary Locality carriers are not exact"
        )
    if len(carried_occurrences) != 1:
        raise RecordedBoundaryLocalityError(
            "recorded boundary Locality requires exactly one current boundary reference"
        )
    event_identity = carried_occurrences[0]
    event = ledger.get(event_identity)
    if event is None or event.locality_identity != source_locality:
        raise RecordedBoundaryLocalityError(
            "recorded boundary Locality names a different current occurrence"
        )
    if event_identity in checkpoint_occurrences:
        return _through_occurrence_reference(ledger, event_identity)
    relation = get_recorded_boundary_locality(ledger, event_identity)
    return deepcopy(relation["through_occurrence_boundary_reference"])


def _act_material(
    *,
    through_occurrence_boundary_reference: dict[str, str],
) -> dict[str, Any]:
    return {
        "act": RECORDED_BOUNDARY_LOCALITY_ACT,
        "subject_reference": deepcopy(through_occurrence_boundary_reference),
    }


def _result_material(act: Event) -> dict[str, Any]:
    material = act.material
    return {
        "through_occurrence_boundary_reference": deepcopy(
            material["subject_reference"]
        ),
        "destination_locality_identity": act.locality_identity,
    }


def _recorded_result_material(
    *, act_occurrence_event_identity: str,
) -> dict[str, Any]:
    return {
        "act_occurrence_event_identity": act_occurrence_event_identity,
    }


def record_recorded_boundary_locality_act_occurrence(
    ledger: EventLedger,
    *,
    source_current_coordinates: dict[str, Any],
) -> Event:
    """Record Preservation from one exact source boundary."""

    if not isinstance(ledger, EventLedger):
        raise TypeError("recorded boundary Locality requires one EventLedger")
    carried_reference = _resolve_one_carried_reference(
        ledger, source_current_coordinates=source_current_coordinates
    )
    destination = ledger.mint_identity("recorded_boundary_locality")
    if ledger.has_locality(destination):
        raise RecordedBoundaryLocalityError(
            "recorded boundary Locality requires one unused destination Locality"
        )
    return ledger.append(
        RECORDED_BOUNDARY_LOCALITY_ACT_OCCURRENCE_EVENT,
        _act_material(
            through_occurrence_boundary_reference=carried_reference,
        ),
        locality_identity=destination,
    )


def get_recorded_boundary_locality_act_occurrence(
    ledger: EventLedger, event_identity: str
) -> Event:
    _require_identity(event_identity, "recorded boundary relation requires Act occurrence")
    event = ledger.get(event_identity)
    if (
        event is None
        or event.kind != RECORDED_BOUNDARY_LOCALITY_ACT_OCCURRENCE_EVENT
        or event.exact_material is not None
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise RecordedBoundaryLocalityError(
            "recorded boundary relation Act occurrence is absent or corrupted"
    )
    material = event.material
    reference = material.get("subject_reference")
    if (
        type(reference) is not dict
        or type(event.locality_identity) is not str
    ):
        raise RecordedBoundaryLocalityError(
            "recorded boundary relation Act occurrence requires exact coordinates"
        )
    expected_reference = _through_occurrence_reference(
        ledger, reference.get("recorded_occurrence_identity")
    )
    expected = _act_material(
        through_occurrence_boundary_reference=expected_reference,
    )
    if material != expected:
        raise RecordedBoundaryLocalityError(
            "recorded boundary relation Act occurrence is not exact"
        )
    subject_identity = expected_reference["recorded_occurrence_identity"]
    try:
        ledger.occurrence_identities_in_append_order(
            (subject_identity, event.identity)
        )
    except ValueError as error:
        raise RecordedBoundaryLocalityError(
            "recorded boundary relation Act requires its prior subject"
        ) from error
    return event


def record_recorded_boundary_locality_result(
    ledger: EventLedger,
    *, act_occurrence_event_identity: str,
) -> Event:
    act = get_recorded_boundary_locality_act_occurrence(
        ledger, act_occurrence_event_identity
    )
    for result in ledger.iter_locality_kind(
        act.locality_identity, RECORDED_BOUNDARY_LOCALITY_RECORDED_KIND
    ):
        if result.material.get("act_occurrence_event_identity") == act.identity:
            raise RecordedBoundaryLocalityError(
                "one recorded boundary Locality Act occurrence cannot address two results"
            )
    result_material = _result_material(act)
    return ledger.append(
        RECORDED_BOUNDARY_LOCALITY_RECORDED_KIND,
        _recorded_result_material(
            act_occurrence_event_identity=act.identity,
        ),
        locality_identity=act.locality_identity,
    )


def get_recorded_boundary_locality(
    ledger: EventLedger, event_identity: str
) -> dict[str, Any]:
    _require_identity(event_identity, "recorded boundary relation requires result")
    event = ledger.get(event_identity)
    if (
        event is None
        or event.kind != RECORDED_BOUNDARY_LOCALITY_RECORDED_KIND
        or event.exact_material is not None
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise RecordedBoundaryLocalityError(
            "recorded boundary relation result is absent or corrupted"
        )
    act = get_recorded_boundary_locality_act_occurrence(
        ledger, event.material.get("act_occurrence_event_identity")
    )
    expected_result = _result_material(act)
    expected = _recorded_result_material(
        act_occurrence_event_identity=act.identity,
    )
    if event.locality_identity != act.locality_identity or event.material != expected:
        raise RecordedBoundaryLocalityError(
            "recorded boundary relation result coordinates are not exact"
        )
    try:
        ledger.occurrences_in_append_order(
            (act.identity, event.identity),
            locality_identity=event.locality_identity,
        )
    except ValueError as error:
        raise RecordedBoundaryLocalityError(
            "recorded boundary Locality result requires its Act occurrence"
        ) from error
    return {
        **deepcopy(event.material),
        "through_occurrence_boundary_reference": deepcopy(
            expected_result["through_occurrence_boundary_reference"]
        ),
        "destination_locality_identity": event.locality_identity,
    }
