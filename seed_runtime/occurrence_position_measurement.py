from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from seed_runtime.event import Event
from seed_runtime.events import CORRUPTED, EventLedger, EventLedgerBoundary

OCCURRENCE_POSITION_RECORDED_KIND = (
    "operator.measurement.locality_occurrence_position_recorded"
)
OCCURRENCE_POSITION_ACT_OCCURRENCE_EVENT = (
    "operator.measurement.locality_occurrence_position_act_occurrence_recorded"
)
OCCURRENCE_POSITION_RESULT_KIND = "occurrence position Measurement result"
OCCURRENCE_POSITION_ACT = "occurrence position Measurement"
OCCURRENCE_POSITION_RESULT_COORDINATES = frozenset(
    {
        "completeness_boundary",
        "result_positions",
    }
)
EVENT_KIND_BOOK_CLAUSES = {
    OCCURRENCE_POSITION_RECORDED_KIND: "01.Source.D",
    OCCURRENCE_POSITION_ACT_OCCURRENCE_EVENT: "02.Acts.A",
}


@dataclass(frozen=True)
class OccurrencePositionFinding:
    """Exact occurrence positions within one Locality and append boundary."""

    source_locality_identity: str
    completeness_boundary: EventLedgerBoundary
    occurrences: tuple[tuple[str, int], ...]

    def __post_init__(self) -> None:
        if not isinstance(self.source_locality_identity, str) or not (
            self.source_locality_identity
        ):
            raise ValueError(
                "one exact source Locality is required"
            )
        if not isinstance(self.completeness_boundary, EventLedgerBoundary):
            raise ValueError(
                "one exact append boundary is required"
            )
        identities = []
        for expected_position, occurrence in enumerate(self.occurrences):
            if (
                type(occurrence) is not tuple
                or len(occurrence) != 2
                or not isinstance(occurrence[0], str)
                or not occurrence[0]
                or type(occurrence[1]) is not int
                or occurrence[1] != expected_position
            ):
                raise ValueError(
                    "each exact occurrence requires its measured position"
                )
            identities.append(occurrence[0])
        if len(set(identities)) != len(identities):
            raise ValueError(
                "one occurrence cannot occupy more than one measured position"
            )

def measure_occurrence_position(
    ledger: EventLedger,
    *,
    source_locality_identity: str,
    through: EventLedgerBoundary | None = None,
) -> OccurrencePositionFinding:
    """Measure every occurrence position in one Locality through one boundary."""

    if not isinstance(ledger, EventLedger):
        raise TypeError("occurrence position Measurement requires one EventLedger")
    if not isinstance(source_locality_identity, str) or not source_locality_identity:
        raise ValueError(
            "one exact source Locality is required"
        )
    boundary = through or ledger.append_boundary()
    return _measure_occurrence_position_through(
        ledger,
        source_locality_identity=source_locality_identity,
        boundary=boundary,
    )


def _measure_occurrence_position_through(
    ledger: EventLedger,
    *,
    source_locality_identity: str,
    boundary: EventLedgerBoundary,
) -> OccurrencePositionFinding:
    occurrences = ledger.list_locality(
        source_locality_identity,
        through=boundary,
    )
    if any(ledger.integrity_of(event.identity) == CORRUPTED for event in occurrences):
        raise ValueError(
            "occurrence position Measurement requires intact occurrences"
        )
    return OccurrencePositionFinding(
        source_locality_identity=source_locality_identity,
        completeness_boundary=boundary,
        occurrences=tuple(
            (event.identity, position)
            for position, event in enumerate(occurrences)
        ),
    )


def _occurrence_position_result_material(
    finding: OccurrencePositionFinding,
    *,
    result_positions: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "completeness_boundary": {
            "identity": finding.completeness_boundary.identity,
        },
        "result_positions": result_positions,
    }


def _occurrence_position_act_occurrence_material(
    finding: OccurrencePositionFinding,
    *,
    through_event_occurrence_identity: str | None,
) -> dict[str, Any]:
    return {
        "act": OCCURRENCE_POSITION_ACT,
        "subject_reference": {
            "source_occurrence_references": [
                {"occurrence_identity": identity}
                for identity, _position in finding.occurrences
            ],
        },
        "source_locality_identity": finding.source_locality_identity,
        "completeness_boundary_identity": finding.completeness_boundary.identity,
        "through_event_occurrence_identity": through_event_occurrence_identity,
    }


def _position_results(
    finding: OccurrencePositionFinding,
) -> list[dict[str, Any]]:
    result_positions = []
    for occurrence_identity, position in finding.occurrences:
        boundary = {"identity": finding.completeness_boundary.identity}
        subject = {"occurrence_identity": occurrence_identity}
        content = {
            "position": position,
            "completeness_boundary": boundary,
        }
        result_positions.append(
            {
                "dimensions": {
                    "identity": occurrence_identity,
                    "content": content,
                },
                "result": "position",
                "subject": subject,
            }
        )
    return result_positions


def _exact_occurrence_position_finding(
    ledger: EventLedger,
    finding: OccurrencePositionFinding,
) -> None:
    if not isinstance(ledger, EventLedger):
        raise TypeError("occurrence position Measurement requires one EventLedger")
    if type(finding) is not OccurrencePositionFinding:
        raise TypeError(
            "occurrence position recording requires one exact finding"
        )
    source_occurrences = ledger.list_locality(
        finding.source_locality_identity,
        through=finding.completeness_boundary,
    )
    if len(source_occurrences) != len(finding.occurrences):
        raise ValueError(
            "the supplied occurrence position finding differs from the exact boundary"
        )
    for position, occurrence in enumerate(source_occurrences):
        if ledger.integrity_of(occurrence.identity) == CORRUPTED:
            raise ValueError(
                "occurrence position Measurement requires intact occurrences"
            )
        if finding.occurrences[position] != (occurrence.identity, position):
            raise ValueError(
                "the supplied occurrence position finding differs from the exact boundary"
            )


def _require_current_coordinates(
    ledger: EventLedger,
    *,
    locality_identity: str,
    current_coordinates: dict[str, Any],
) -> str | None:
    if type(current_coordinates) is not dict:
        raise ValueError(
            "occurrence position Measurement requires exact current coordinates"
        )
    # Imported here because the current-coordinate reader imports this module's event
    # contract. Recording is runtime work after both modules are initialized.
    from seed_runtime.operator_current_coordinates import (
        read_operator_current_coordinates,
    )

    current = read_operator_current_coordinates(
        ledger, locality_identity=locality_identity
    )
    if (
        current_coordinates != current
        or current_coordinates.get("locality_identity") != locality_identity
    ):
        raise ValueError(
            "occurrence position Measurement requires exact current coordinates"
        )
    boundary = current_coordinates.get("through_event_occurrence_identity")
    if boundary is not None and (type(boundary) is not str or not boundary):
        raise ValueError(
            "occurrence position Measurement requires exact current coordinates"
        )
    return boundary


def _require_carried_current_coordinates_at_append_boundary(
    ledger: EventLedger,
    *,
    locality_identity: str,
    current_coordinates: dict[str, Any],
) -> str | None:
    """Read same-call coordinates at the current append boundary."""

    if type(current_coordinates) is not dict:
        raise ValueError(
            "occurrence position Measurement requires exact current coordinates"
        )
    boundary = current_coordinates.get("through_event_occurrence_identity")
    if (
        current_coordinates.get("locality_identity") != locality_identity
        or boundary is None
        or type(boundary) is not str
        or not boundary
    ):
        raise ValueError(
            "occurrence position Measurement requires exact current coordinates"
        )
    event = ledger.get(boundary)
    if (
        event is None
        or event.locality_identity != locality_identity
        or ledger.integrity_of(boundary) == CORRUPTED
        or ledger.append_boundary_through_occurrence(boundary)
        != ledger.append_boundary()
    ):
        raise ValueError(
            "occurrence position Measurement requires exact current coordinates"
        )
    return boundary


def _record_occurrence_position_measurement_act_occurrence(
    ledger: EventLedger,
    *,
    recording_locality_identity: str,
    finding: OccurrencePositionFinding,
    current_coordinates: dict[str, Any],
    carried: bool,
) -> Event:
    if type(recording_locality_identity) is not str or not recording_locality_identity:
        raise ValueError("occurrence position recording requires one exact Locality")
    if carried:
        if (
            type(finding) is not OccurrencePositionFinding
            or finding.source_locality_identity != recording_locality_identity
            or finding.completeness_boundary != ledger.append_boundary()
        ):
            raise ValueError(
                "occurrence position Measurement requires exact current coordinates"
            )
    else:
        _exact_occurrence_position_finding(ledger, finding)
    require_coordinates = (
        _require_carried_current_coordinates_at_append_boundary
        if carried
        else _require_current_coordinates
    )
    through_event_occurrence_identity = require_coordinates(
        ledger,
        locality_identity=recording_locality_identity,
        current_coordinates=current_coordinates,
    )
    if (
        carried
        and (
            not finding.occurrences
            or finding.occurrences[-1][0] != through_event_occurrence_identity
        )
    ):
        raise ValueError(
            "occurrence position Measurement requires exact current coordinates"
        )
    return ledger.append(
        OCCURRENCE_POSITION_ACT_OCCURRENCE_EVENT,
        _occurrence_position_act_occurrence_material(
            finding,
            through_event_occurrence_identity=through_event_occurrence_identity,
        ),
        locality_identity=recording_locality_identity,
    )


def record_occurrence_position_measurement_act_occurrence(
    ledger: EventLedger,
    *,
    recording_locality_identity: str,
    finding: OccurrencePositionFinding,
    current_coordinates: dict[str, Any],
) -> Event:
    """Record the Measurement Act with its exact binding coordinates."""

    return _record_occurrence_position_measurement_act_occurrence(
        ledger,
        recording_locality_identity=recording_locality_identity,
        finding=finding,
        current_coordinates=current_coordinates,
        carried=False,
    )


def _record_occurrence_position_measurement_act_occurrence_from_current_coordinates(
    ledger: EventLedger,
    *,
    recording_locality_identity: str,
    finding: OccurrencePositionFinding,
    current_coordinates: dict[str, Any],
) -> Event:
    """Record the Act from a finding produced from same-call coordinates."""

    return _record_occurrence_position_measurement_act_occurrence(
        ledger,
        recording_locality_identity=recording_locality_identity,
        finding=finding,
        current_coordinates=current_coordinates,
        carried=True,
    )


def _read_occurrence_position_measurement_act_occurrence(
    ledger: EventLedger,
    act_occurrence_event_identity: str,
) -> tuple[Event, OccurrencePositionFinding]:
    if type(act_occurrence_event_identity) is not str or not act_occurrence_event_identity:
        raise ValueError(
            "occurrence position result requires one exact Act occurrence identity"
        )
    act_occurrence = ledger.get(act_occurrence_event_identity)
    if (
        act_occurrence is None
        or act_occurrence.kind != OCCURRENCE_POSITION_ACT_OCCURRENCE_EVENT
        or type(act_occurrence.locality_identity) is not str
        or not act_occurrence.locality_identity
        or act_occurrence.exact_material is not None
        or ledger.integrity_of(act_occurrence.identity) == CORRUPTED
    ):
        raise ValueError(
            "occurrence position result requires its exact intact Act occurrence"
        )
    material = act_occurrence.material
    source_locality_identity = material.get("source_locality_identity")
    completeness_boundary_identity = material.get(
        "completeness_boundary_identity"
    )
    through_event_occurrence_identity = material.get(
        "through_event_occurrence_identity"
    )
    if (
        type(source_locality_identity) is not str
        or not source_locality_identity
        or type(completeness_boundary_identity) is not str
        or not completeness_boundary_identity
        or (
            through_event_occurrence_identity is not None
            and (
                type(through_event_occurrence_identity) is not str
                or not through_event_occurrence_identity
            )
        )
    ):
        raise ValueError(
            "occurrence position Act coordinates are not exact"
        )
    try:
        finding = _measure_occurrence_position_through(
            ledger,
            source_locality_identity=source_locality_identity,
            boundary=EventLedgerBoundary(completeness_boundary_identity),
        )
    except (TypeError, ValueError) as error:
        raise ValueError(
            "occurrence position Act coordinates are not exact"
        ) from error
    if material != _occurrence_position_act_occurrence_material(
        finding,
        through_event_occurrence_identity=through_event_occurrence_identity,
    ):
        raise ValueError(
            "occurrence position Act coordinates are not exact"
        )
    if not ledger.append_boundary_precedes_occurrence(
        finding.completeness_boundary, act_occurrence.identity
    ):
        raise ValueError("occurrence position Act has false occurrence order")
    if through_event_occurrence_identity is not None:
        boundary = ledger.get(through_event_occurrence_identity)
        if (
            boundary is None
            or boundary.locality_identity != act_occurrence.locality_identity
            or ledger.integrity_of(boundary.identity) == CORRUPTED
        ):
            raise ValueError(
                "occurrence position Act has no exact through-occurrence boundary"
            )
        try:
            ledger.occurrences_in_append_order(
                (through_event_occurrence_identity, act_occurrence.identity),
                locality_identity=act_occurrence.locality_identity,
            )
        except ValueError as error:
            raise ValueError(
                "occurrence position Act has false occurrence order"
            ) from error
    return act_occurrence, finding


def _refuse_existing_occurrence_position_measurement_result(
    ledger: EventLedger,
    *,
    act_occurrence: Event,
) -> None:
    for prior_result in ledger.iter_locality_kind(
        act_occurrence.locality_identity,
        OCCURRENCE_POSITION_RECORDED_KIND,
    ):
        if (
            prior_result.material.get("act_occurrence_event_identity")
            == act_occurrence.identity
        ):
            raise ValueError(
                "the occurrence position Measurement Act already has a result"
            )


def _record_occurrence_position_measurement_result(
    ledger: EventLedger,
    *,
    act_occurrence: Event,
    finding: OccurrencePositionFinding,
) -> Event:
    result_positions = _position_results(finding)
    result_material = _occurrence_position_result_material(
        finding,
        result_positions=result_positions,
    )
    recorded_material = {
        "completeness_boundary": result_material["completeness_boundary"],
        "result_positions": result_material["result_positions"],
        "act_occurrence_event_identity": act_occurrence.identity,
    }
    return ledger.append(
        OCCURRENCE_POSITION_RECORDED_KIND,
        recorded_material,
        locality_identity=act_occurrence.locality_identity,
    )


def record_occurrence_position_measurement_result(
    ledger: EventLedger,
    *,
    act_occurrence_event_identity: str,
) -> Event:
    """Record the result of one exact recorded Measurement Act."""

    act_occurrence, finding = (
        _read_occurrence_position_measurement_act_occurrence(
            ledger, act_occurrence_event_identity
        )
    )
    _refuse_existing_occurrence_position_measurement_result(
        ledger,
        act_occurrence=act_occurrence,
    )
    return _record_occurrence_position_measurement_result(
        ledger,
        act_occurrence=act_occurrence,
        finding=finding,
    )


def _record_occurrence_position_measurement_result_from_carried_act_occurrence(
    ledger: EventLedger,
    *,
    act_occurrence: Event,
    finding: OccurrencePositionFinding,
) -> Event:
    """Record the result from the just-produced exact Act occurrence."""

    if (
        type(act_occurrence) is not Event
        or act_occurrence.kind != OCCURRENCE_POSITION_ACT_OCCURRENCE_EVENT
        or act_occurrence.exact_material is not None
        or act_occurrence.locality_identity
        != finding.source_locality_identity
        or ledger.integrity_of(act_occurrence.identity) == CORRUPTED
        or act_occurrence.material
        != _occurrence_position_act_occurrence_material(
            finding,
            through_event_occurrence_identity=act_occurrence.material.get(
                "through_event_occurrence_identity"
            ),
        )
        or ledger.append_boundary_through_occurrence(
            act_occurrence.identity
        )
        != ledger.append_boundary()
    ):
        raise ValueError(
            "occurrence position result requires its exact intact Act occurrence"
        )
    return _record_occurrence_position_measurement_result(
        ledger,
        act_occurrence=act_occurrence,
        finding=finding,
    )


def get_recorded_occurrence_position_measurement(
    ledger: EventLedger,
    event_identity: str,
) -> OccurrencePositionFinding:
    """Read one recorded occurrence-position Measurement through its exact relation."""

    event = ledger.get(event_identity)
    if (
        event is None
        or event.kind != OCCURRENCE_POSITION_RECORDED_KIND
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise ValueError(
            "the occurrence position Measurement result is absent or corrupted"
        )
    material = event.material
    if set(material) != OCCURRENCE_POSITION_RESULT_COORDINATES | {
        "act_occurrence_event_identity",
    }:
        raise ValueError(
            "the occurrence position Measurement carries malformed coordinates"
        )
    boundary = material.get("completeness_boundary")
    if (
        type(boundary) is not dict
        or set(boundary) != {"identity"}
        or type(boundary["identity"]) is not str
        or not boundary["identity"]
        or type(material.get("result_positions")) is not list
    ):
        raise ValueError(
            "the occurrence position Measurement carries malformed coordinates"
        )
    try:
        act_occurrence, bound_finding = (
                _read_occurrence_position_measurement_act_occurrence(
                    ledger, material.get("act_occurrence_event_identity")
                )
        )
    except (TypeError, ValueError) as error:
        raise ValueError(
            "the occurrence position Measurement carries no exact Act occurrence"
        ) from error
    try:
        finding = _measure_occurrence_position_through(
            ledger,
            source_locality_identity=bound_finding.source_locality_identity,
            boundary=EventLedgerBoundary(boundary["identity"]),
        )
    except (TypeError, ValueError) as error:
        raise ValueError(
            "the occurrence position Measurement carries malformed coordinates"
        ) from error
    result_positions = _position_results(finding)
    if material["result_positions"] != result_positions:
        raise ValueError(
            "the occurrence position Measurement carries malformed result positions"
        )
    if (
        act_occurrence.locality_identity != event.locality_identity
        or bound_finding != finding
    ):
        raise ValueError(
            "the occurrence position Measurement carries no exact Act occurrence"
        )
    result_material = _occurrence_position_result_material(
        bound_finding,
        result_positions=result_positions,
    )
    try:
        ordered = ledger.occurrences_in_append_order(
            (act_occurrence.identity, event.identity),
            locality_identity=event.locality_identity,
        )
    except (TypeError, ValueError) as error:
        raise ValueError(
            "the occurrence position Measurement result does not follow its Act"
        ) from error
    results = tuple(
        candidate
        for candidate in ledger.iter_locality_kind(
            event.locality_identity,
            OCCURRENCE_POSITION_RECORDED_KIND,
        )
        if candidate.material.get("act_occurrence_event_identity")
        == act_occurrence.identity
    )
    if (
        tuple(item.identity for item in ordered)
        != (act_occurrence.identity, event.identity)
        or len(results) != 1
        or results[0].identity != event.identity
    ):
        raise ValueError(
            "the occurrence position Measurement result is not exact for its Act"
        )
    recorded_result_material = {
        key: value
        for key, value in material.items()
        if key != "act_occurrence_event_identity"
    }
    if recorded_result_material != result_material:
        raise ValueError(
            "the occurrence position Measurement result differs from its coordinates"
        )
    return finding
