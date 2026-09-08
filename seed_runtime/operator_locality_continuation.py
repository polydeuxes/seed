"""One exact source through-occurrence boundary at another Locality.

This boundary establishes one Locality relation and bounded
availability only.  It does not copy the source Locality's occurrences or
current coordinates, make any addressed subject applicable to another Act,
establish priority, or follow another continuation transitively.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from seed_runtime.event import Event
from seed_runtime.events import CORRUPTED, EventLedger
LOCALITY_CONTINUATION_ACT_OCCURRENCE_EVENT = (
    "operator.locality_continuation_act_occurrence_recorded"
)
LOCALITY_CONTINUATION_RECORDED_KIND = (
    "operator.locality_continuation_recorded"
)
LOCALITY_CONTINUATION_ACT = "Preservation"
EVENT_KIND_BOOK_CLAUSES = {
    LOCALITY_CONTINUATION_ACT_OCCURRENCE_EVENT: "02.Acts.A",
    LOCALITY_CONTINUATION_RECORDED_KIND: "06.Locality.A",
}


class LocalityContinuationError(ValueError):
    """One exact source-boundary Locality relation could not be established."""


def _require_identity(value: Any, message: str) -> str:
    if type(value) is not str or not value:
        raise LocalityContinuationError(message)
    return value


def _source_coordinate_reference(
    ledger: EventLedger,
    *,
    source_locality_identity: str,
    source_through_event_occurrence_identity: str,
) -> dict[str, str | None]:
    """Resolve one intact exact source occurrence boundary."""

    _require_identity(
        source_locality_identity,
        "Locality continuation requires one exact source Locality",
    )
    _require_identity(
        source_through_event_occurrence_identity,
        "Locality continuation requires one exact source occurrence boundary",
    )
    source_boundary = ledger.get(source_through_event_occurrence_identity)
    if (
        source_boundary is None
        or source_boundary.locality_identity != source_locality_identity
        or ledger.integrity_of(source_boundary.identity) == CORRUPTED
    ):
        raise LocalityContinuationError(
            "Locality continuation requires one intact source boundary"
        )
    occurrences = ledger.list_locality(source_locality_identity)
    positions = {event.identity: position for position, event in enumerate(occurrences)}
    if positions.get(source_through_event_occurrence_identity) is None:
        raise LocalityContinuationError(
            "the source occurrence boundary is absent from its source Locality"
        )
    return {
        "source_locality_identity": source_locality_identity,
        "source_through_event_occurrence_identity": (
            source_through_event_occurrence_identity
        ),
    }


def _act_occurrence_material(
    *,
    source_coordinate_reference: dict[str, str | None],
) -> dict[str, Any]:
    return {
        "act": LOCALITY_CONTINUATION_ACT,
        "source_coordinate_reference": deepcopy(source_coordinate_reference),
    }


def _result_material(
    *,
    source_coordinate_reference: dict[str, str | None],
    destination_locality_identity: str,
) -> dict[str, Any]:
    return {
        "source_coordinate_reference": deepcopy(source_coordinate_reference),
        "destination_locality_identity": destination_locality_identity,
    }


def _recorded_result_material(
    result_material: dict[str, Any],
    *,
    act_occurrence_event_identity: str,
) -> dict[str, Any]:
    """Record every result coordinate at one literal durable address."""

    return {
        "destination_locality_identity": result_material[
            "destination_locality_identity"
        ],
        "act_occurrence_event_identity": act_occurrence_event_identity,
    }


def record_locality_continuation_act_occurrence(
    ledger: EventLedger,
    *,
    source_locality_identity: str,
    source_through_event_occurrence_identity: str,
) -> Event:
    """Record an Act over an exact source cut in a fresh Locality."""

    if not isinstance(ledger, EventLedger):
        raise TypeError("Locality continuation requires one EventLedger")
    source_reference = _source_coordinate_reference(
        ledger,
        source_locality_identity=source_locality_identity,
        source_through_event_occurrence_identity=(
            source_through_event_occurrence_identity
        ),
    )
    destination_locality_identity = ledger.mint_identity(
        "locality_continuation_destination_locality"
    )
    if ledger.has_locality(destination_locality_identity):
        raise LocalityContinuationError(
            "Locality continuation requires one fresh destination Locality"
        )
    return ledger.append(
        LOCALITY_CONTINUATION_ACT_OCCURRENCE_EVENT,
        _act_occurrence_material(
            source_coordinate_reference=source_reference,
        ),
        locality_identity=destination_locality_identity,
    )


def _validated_act_occurrence(
    ledger: EventLedger, act_occurrence_event_identity: str
) -> Event:
    _require_identity(
        act_occurrence_event_identity,
        "Locality continuation result requires one exact Act occurrence identity",
    )
    act_occurrence = ledger.get(act_occurrence_event_identity)
    if (
        act_occurrence is None
        or act_occurrence.kind != LOCALITY_CONTINUATION_ACT_OCCURRENCE_EVENT
        or type(act_occurrence.locality_identity) is not str
        or not act_occurrence.locality_identity
        or act_occurrence.exact_material is not None
        or ledger.integrity_of(act_occurrence.identity) == CORRUPTED
    ):
        raise LocalityContinuationError(
            "Locality continuation result requires intact Act occurrence"
        )
    material = act_occurrence.material
    source_reference = material.get("source_coordinate_reference")
    if type(source_reference) is not dict:
        raise LocalityContinuationError(
            "Locality continuation Act occurrence requires one exact source boundary"
        )
    expected_reference = _source_coordinate_reference(
        ledger,
        source_locality_identity=source_reference.get("source_locality_identity"),
        source_through_event_occurrence_identity=source_reference.get(
            "source_through_event_occurrence_identity"
        ),
    )
    if source_reference != expected_reference:
        raise LocalityContinuationError(
            "Locality continuation Act occurrence names another source boundary"
        )
    if (
        material != _act_occurrence_material(
            source_coordinate_reference=expected_reference,
        )
    ):
        raise LocalityContinuationError(
            "Locality continuation Act occurrence is not exact"
        )
    try:
        ledger.occurrence_identities_in_append_order(
            (
                expected_reference["source_through_event_occurrence_identity"],
                act_occurrence.identity,
            )
        )
    except ValueError as error:
        raise LocalityContinuationError(
            "Locality continuation Act requires its prior source boundary"
        ) from error
    return act_occurrence


def record_locality_continuation_result(
    ledger: EventLedger,
    *,
    act_occurrence_event_identity: str,
) -> Event:
    """Record the Locality relation for one Act occurrence."""

    act_occurrence = _validated_act_occurrence(
        ledger, act_occurrence_event_identity
    )
    material = act_occurrence.material
    locality_identity = act_occurrence.locality_identity
    for prior_result in ledger.iter_locality_kind(
        locality_identity, LOCALITY_CONTINUATION_RECORDED_KIND
    ):
        if (
            prior_result.material.get("act_occurrence_event_identity")
            == act_occurrence.identity
        ):
            raise LocalityContinuationError(
                "one Locality continuation Act occurrence cannot address two results"
            )

    result_material = _result_material(
        source_coordinate_reference=material["source_coordinate_reference"],
        destination_locality_identity=locality_identity,
    )
    return ledger.append(
        LOCALITY_CONTINUATION_RECORDED_KIND,
        _recorded_result_material(
            result_material,
            act_occurrence_event_identity=act_occurrence.identity,
        ),
        locality_identity=locality_identity,
    )


def get_recorded_locality_continuation(
    ledger: EventLedger, recorded_result_event_identity: str
) -> dict[str, Any]:
    """Read one continuation relation through its exact occurrence."""

    _require_identity(
        recorded_result_event_identity,
        "Locality continuation read requires one exact result occurrence",
    )
    event = ledger.get(recorded_result_event_identity)
    if (
        event is None
        or event.kind != LOCALITY_CONTINUATION_RECORDED_KIND
        or type(event.locality_identity) is not str
        or not event.locality_identity
        or event.exact_material is not None
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise LocalityContinuationError(
            "the Locality continuation result is absent or corrupted"
        )
    act_occurrence = _validated_act_occurrence(
        ledger, event.material.get("act_occurrence_event_identity")
    )
    expected = _result_material(
        source_coordinate_reference=act_occurrence.material[
            "source_coordinate_reference"
        ],
        destination_locality_identity=event.locality_identity,
    )
    expected_event_material = _recorded_result_material(
        expected,
        act_occurrence_event_identity=act_occurrence.identity,
    )
    if (
        act_occurrence.locality_identity != event.locality_identity
        or event.material != expected_event_material
    ):
        raise LocalityContinuationError(
            "the Locality continuation result coordinates are not exact"
        )
    try:
        ledger.occurrences_in_append_order(
            (act_occurrence.identity, event.identity),
            locality_identity=event.locality_identity,
        )
    except ValueError as error:
        raise LocalityContinuationError(
            "the Locality continuation result requires its Act occurrence"
        ) from error
    return {
        **deepcopy(event.material),
        "source_coordinate_reference": deepcopy(
            expected["source_coordinate_reference"]
        ),
    }
