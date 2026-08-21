"""Measure first and second position coordinates of each byte-pair occurrence.

The exact source material acquisition result bounds the population.  The Measurement records
first and second byte values with their position coordinates; it establishes no
recurrence, represented relation, character, word, or meaning.
"""

from __future__ import annotations

import hashlib
import json
from contextlib import contextmanager
from contextvars import ContextVar
from copy import deepcopy
from typing import TYPE_CHECKING, Any, Iterator, NamedTuple

if TYPE_CHECKING:
    from seed_runtime.byte_measurement import (
        RecordedAssertionCarriedByLocalityMovement,
    )

from seed_runtime.event import Event
from seed_runtime.events import CORRUPTED, EventLedger, EventLedgerBoundary
from seed_runtime.evidence_of_yield_relation import (
    RECORDED_EVIDENCE_OF_YIELD_RELATION_KIND,
    _record_evidence_of_yield_relation,
    read_requirements_of_yield_relation,
)
from seed_runtime.identities import new_identity
from seed_runtime.material_acquisition import (
    acquired_material_bytes,
    read_exact_material_acquisition_result,
)


BYTE_PAIR_OCCURRENCE_POSITION_ASSIGNMENT_KIND = (
    "operator.measurement_of_position_coordinates_of_byte_pair_occurrences."
    "responsibility_assignment_recorded"
)
BYTE_PAIR_OCCURRENCE_POSITION_ACT_EVIDENCE_KIND = (
    "operator.measurement_of_position_coordinates_of_byte_pair_occurrences."
    "evidence_of_act_occurrence_recorded"
)
BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND = (
    "operator.measurement_of_position_coordinates_of_byte_pair_occurrences."
    "recording_occurrence_of_result"
)
RESULT_KIND = "result of Measurement of position coordinates of byte-pair occurrences"


class _PositionResultReadingContext(NamedTuple):
    ledger: EventLedger
    result_event_identity: str
    reading: tuple[
        Event,
        "FindingOfPositionCoordinatesOfBytePairOccurrences",
        dict[str, Any],
    ]
    result_snapshot: Event
    prefix_snapshot: tuple[Event, ...]


_POSITION_RESULT_READING_CONTEXT: ContextVar[
    _PositionResultReadingContext | None
] = ContextVar("position_result_reading_context", default=None)


def _require_carried_position_measurement_source_unchanged() -> None:
    """Refuse a changed exact prefix before one continuation becomes visible."""

    context = _POSITION_RESULT_READING_CONTEXT.get()
    if context is None:
        return
    if any(
        context.ledger.get(expected.identity) != expected
        or context.ledger.integrity_of(expected.identity) == CORRUPTED
        for expected in context.prefix_snapshot
    ):
        raise ValueError(
            "byte-pair position-coordinate source changed during its bounded continuation"
        )


EXACT_ACT = "Measurement of position coordinates of byte-pair occurrences"
RESPONSIBILITY = (
    "Measurement of the position coordinates of each exact byte-pair occurrence "
    "within one exact material acquisition result"
)
MEASUREMENT_RULE = (
    "each exact byte-pair occurrence with its first position and second position "
    "in source occurrence order within one exact material acquisition result"
)
AUTHORITY = "bounded repository authority"
ASSERTION_RESPONSIBILITY = (
    "preserve this measured Assertion's carried Standing coordinates"
)

EVENT_KIND_RESPONSIBILITIES = {
    BYTE_PAIR_OCCURRENCE_POSITION_ASSIGNMENT_KIND: "01.Source.D",
    BYTE_PAIR_OCCURRENCE_POSITION_ACT_EVIDENCE_KIND: "02.Acts.A",
    BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND: "01.Source.D",
}
class FindingOfPositionCoordinatesOfBytePairOccurrences(NamedTuple):
    source_material_acquisition_occurrence_identity: str
    source_locality_identity: str
    completeness_boundary: EventLedgerBoundary
    exact_material: bytes

    @property
    def occurrences(self) -> tuple[tuple[bytes, int, int], ...]:
        return tuple(
            (
                self.exact_material[position : position + 2],
                position,
                position + 1,
            )
            for position in range(len(self.exact_material) - 1)
        )


class UnassignedPositionCoordinateMeasurementAcquisitionReading(NamedTuple):
    """Exact material acquisition coordinates read before this Measurement assignment.

    This bounded runtime read preserves exact source coordinates beside the
    absence of this Measurement Responsibility's assignment or result through B. It
    establishes no Locality relation, required assignment subject or
    coordinates, Responsibility assignment, Applicability, Act, or Standing.
    """

    source_material_acquisition_occurrence_identity: str
    source_result_identity: str
    source_locality_identity: str
    source_completeness_boundary_identity: str
    bounded_locality_replay_through_event_occurrence_identity: str
    bounded_locality_replay_append_boundary_identity: str
    responsible_act_evidence_identity: str
    evidence_of_yield_relation_identity: str
    source_role: str
    source_boundary: str
    exact_material: bytes
    known_loss: tuple[str, ...]
    unknown: tuple[str, ...]
    provenance_occurrence_references: tuple[str, ...]


class ReferenceToRecordedPositionOfBytePairOccurrence(
    NamedTuple
):
    recorded_occurrence_identity: str
    assertion_identity: str
    source_material_acquisition_occurrence_identity: str
    locality_identity: str
    completeness_boundary_identity: str
    exact_pair: bytes
    first_position: int
    second_position: int

    @property
    def assertion_reference(self) -> dict[str, str]:
        return {
            "recorded_occurrence_identity": self.recorded_occurrence_identity,
            "assertion_identity": self.assertion_identity,
        }

    @property
    def first_position_coordinate_reference(self) -> dict[str, Any]:
        return _source_position_coordinate_reference(
            source_material_acquisition_occurrence_identity=(
                self.source_material_acquisition_occurrence_identity
            ),
            source_locality_identity=self.locality_identity,
            completeness_boundary_identity=(
                self.completeness_boundary_identity
            ),
            position=self.first_position,
            exact_material=self.exact_pair[:1],
        )

    @property
    def second_position_coordinate_reference(self) -> dict[str, Any]:
        return _source_position_coordinate_reference(
            source_material_acquisition_occurrence_identity=(
                self.source_material_acquisition_occurrence_identity
            ),
            source_locality_identity=self.locality_identity,
            completeness_boundary_identity=(
                self.completeness_boundary_identity
            ),
            position=self.second_position,
            exact_material=self.exact_pair[1:],
        )


def _exact_string_list(value: Any, *, coordinate: str) -> tuple[str, ...]:
    if type(value) is not list or any(type(item) is not str for item in value):
        raise ValueError(f"exact material acquisition assignment subject has malformed {coordinate}")
    return tuple(value)


def _has_exact_material_locality_to_this_seed(
    ledger: EventLedger, source_identity: str
) -> bool:
    """Whether exact source acquisition supplies the Locality prerequisite."""

    from seed_runtime.material_acquisition import (
        read_material_acquisition_locality_relation_requirements,
    )

    return all(
        read_material_acquisition_locality_relation_requirements(
            ledger,
            recorded_result_event_identity=source_identity,
        ).values()
    )


def _material_acquisition_identities_with_exact_locality_from_bounded_replay(
    bounded_locality_replay: dict[str, Any],
) -> tuple[str, ...]:
    """Resolve exact acquisition sources already validated into bounded replay."""

    acquisitions = bounded_locality_replay.get(
        "material_acquisition_result_occurrences"
    )
    locality_occurrences = bounded_locality_replay.get(
        "material_locality_relation_occurrences"
    )
    if type(acquisitions) is not list or type(locality_occurrences) is not dict:
        raise ValueError(
            "declared Measurement source resolution requires exact bounded "
            "Locality replay"
        )
    identities: list[str] = []
    for occurrence in acquisitions:
        if (
            type(occurrence) is not dict
            or type(occurrence.get("result_occurrence_identity")) is not str
            or not occurrence["result_occurrence_identity"]
        ):
            raise ValueError(
                "bounded Locality replay contains a malformed material acquisition result"
            )
        source_identity = occurrence["result_occurrence_identity"]
        locality_coordinates = locality_occurrences.get(source_identity)
        if locality_coordinates is None:
            continue
        exact_relation = {
            "first_subject": {
                "recorded_occurrence_identity": source_identity,
                "coordinate": "exact_material",
            },
            "relation": "locality",
            "second_subject": "this Seed",
            "relation_occurrence_identity": source_identity,
        }
        if (
            type(locality_coordinates) is not dict
            or locality_coordinates.get("locality_relation") != exact_relation
        ):
            raise ValueError(
                "bounded Locality replay contains malformed material-to-this-Seed "
                "Locality coordinates"
            )
        identities.append(source_identity)
    return tuple(identities)


def _recorded_position_coordinate_measurement_sources_from_bounded_replay(
    ledger: EventLedger,
    bounded_locality_replay: dict[str, Any],
) -> set[str]:
    """Resolve sources from prior occurrences already validated by replay."""

    recorded_sources: set[str] = set()
    occurrence_populations = (
        (
            bounded_locality_replay["responsibility_assignment_occurrences"],
            BYTE_PAIR_OCCURRENCE_POSITION_ASSIGNMENT_KIND,
        ),
        (
            bounded_locality_replay["measurement_occurrences"],
            BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND,
        ),
    )
    for occurrence_identities, expected_kind in occurrence_populations:
        for occurrence_identity in occurrence_identities:
            event = ledger.get(occurrence_identity)
            if event is None or event.kind != expected_kind:
                continue
            if ledger.integrity_of(event.identity) == CORRUPTED:
                raise ValueError(
                    "bounded Locality replay contains a corrupted position-coordinate "
                    "Measurement occurrence"
                )
            source_identity = event.material.get(
                "source_material_acquisition_occurrence_identity"
            )
            if type(source_identity) is not str or not source_identity:
                raise ValueError(
                    "bounded Locality replay contains a malformed position-coordinate "
                    "Measurement occurrence"
                )
            recorded_sources.add(source_identity)
    return recorded_sources


def _unassigned_position_coordinate_measurement_acquisition_results_from_bounded_locality_replay(
    ledger: EventLedger,
    bounded_locality_replay: dict[str, Any],
    *,
    locality_identity: str,
) -> tuple[UnassignedPositionCoordinateMeasurementAcquisitionReading, ...]:
    if (
        not isinstance(ledger, EventLedger)
        or type(locality_identity) is not str
        or not locality_identity
        or type(bounded_locality_replay) is not dict
        or bounded_locality_replay.get("locality_identity") != locality_identity
        or type(bounded_locality_replay.get("material_acquisition_result_occurrences")) is not list
        or type(
            bounded_locality_replay.get("responsibility_assignment_occurrences")
        )
        is not dict
        or type(bounded_locality_replay.get("measurement_occurrences")) is not dict
    ):
        raise ValueError(
            "position-coordinate source read requires exact bounded Locality replay"
        )
    replay_through = bounded_locality_replay.get(
        "through_event_occurrence_identity"
    )
    replay_event = (
        ledger.get(replay_through)
        if type(replay_through) is str and replay_through
        else None
    )
    if (
        replay_event is None
        or replay_event.locality_identity != locality_identity
        or ledger.integrity_of(replay_event.identity) == CORRUPTED
    ):
        raise ValueError(
            "position-coordinate source read requires one exact replay boundary"
        )
    replay_boundary = ledger.append_boundary_through_occurrence(replay_through)

    recorded_sources = (
        _recorded_position_coordinate_measurement_sources_from_bounded_replay(
            ledger, bounded_locality_replay
        )
    )
    exact_operator_locality_sources = set(
        _material_acquisition_identities_with_exact_locality_from_bounded_replay(
            bounded_locality_replay
        )
    )

    sources: list[UnassignedPositionCoordinateMeasurementAcquisitionReading] = []
    for occurrence in bounded_locality_replay["material_acquisition_result_occurrences"]:
        if (
            type(occurrence) is not dict
            or type(occurrence.get("result_occurrence_identity")) is not str
            or not occurrence["result_occurrence_identity"]
        ):
            raise ValueError(
                "bounded Locality replay contains a malformed material acquisition result"
            )
        source_identity = occurrence["result_occurrence_identity"]
        if source_identity in recorded_sources:
            continue
        if source_identity not in exact_operator_locality_sources:
            # Availability through B is not the exact material-to-this-Seed
            # Locality occurrence and Evidence required by 01.Source.D.
            continue
        source = ledger.get(source_identity)
        if source is None or source.locality_identity != locality_identity:
            raise ValueError(
                "bounded Locality replay contains an absent material acquisition result"
            )
        if not all(
            type(source.material.get(key)) is str and source.material[key]
            for key in (
                "responsible_act_evidence_identity",
                "evidence_of_yield_relation_identity",
            )
        ):
            # Preserved legacy material is not an exact result of the material acquisition
            # Act/Yield physiology required by this assignment subject.
            continue
        source = read_exact_material_acquisition_result(ledger, source_identity)
        material = source.material
        exact_coordinates = {
            key: material.get(key)
            for key in (
                "result_identity",
                "responsible_act_evidence_identity",
                "evidence_of_yield_relation_identity",
                "source_role",
                "source_boundary",
            )
        }
        if any(
            type(value) is not str or not value
            for value in exact_coordinates.values()
        ):
            raise ValueError("exact material acquisition assignment subject coordinates are malformed")
        sources.append(
            UnassignedPositionCoordinateMeasurementAcquisitionReading(
                source_material_acquisition_occurrence_identity=source.identity,
                source_result_identity=exact_coordinates["result_identity"],
                source_locality_identity=source.locality_identity,
                source_completeness_boundary_identity=(
                    ledger.append_boundary_through_occurrence(source.identity).identity
                ),
                bounded_locality_replay_through_event_occurrence_identity=(
                    replay_through
                ),
                bounded_locality_replay_append_boundary_identity=(
                    replay_boundary.identity
                ),
                responsible_act_evidence_identity=exact_coordinates[
                    "responsible_act_evidence_identity"
                ],
                evidence_of_yield_relation_identity=exact_coordinates[
                    "evidence_of_yield_relation_identity"
                ],
                source_role=exact_coordinates["source_role"],
                source_boundary=exact_coordinates["source_boundary"],
                exact_material=acquired_material_bytes(source),
                known_loss=_exact_string_list(
                    material.get("known_loss"), coordinate="known_loss"
                ),
                unknown=_exact_string_list(
                    material.get("unknown"), coordinate="unknown"
                ),
                provenance_occurrence_references=_exact_string_list(
                    material.get("provenance_occurrence_references"),
                    coordinate="provenance_occurrence_references",
                ),
            )
        )
    return tuple(sources)


def read_unassigned_position_coordinate_measurement_acquisition_results_through(
    ledger: EventLedger,
    *,
    locality_identity: str,
    through_event_occurrence_identity: str,
) -> tuple[UnassignedPositionCoordinateMeasurementAcquisitionReading, ...]:
    """Read exact unassigned material acquisition results for this Measurement through B.

    The non-recording read establishes neither an exact Locality
    relation nor that any returned source is a subject of this Measurement's
    Responsibility assignment.
    """

    from seed_runtime.operator_locality_standing import (
        read_operator_locality_standing_through,
    )

    bounded_locality_replay = read_operator_locality_standing_through(
        ledger,
        locality_identity=locality_identity,
        through_event_occurrence_identity=through_event_occurrence_identity,
    )
    return _unassigned_position_coordinate_measurement_acquisition_results_from_bounded_locality_replay(
        ledger,
        bounded_locality_replay,
        locality_identity=locality_identity,
    )

def _validate_finding(
    finding: FindingOfPositionCoordinatesOfBytePairOccurrences,
) -> None:
    if type(finding) is not FindingOfPositionCoordinatesOfBytePairOccurrences:
        raise TypeError("byte-pair position-coordinate Measurement requires one exact finding")
    if (
        type(finding.source_material_acquisition_occurrence_identity) is not str
        or not finding.source_material_acquisition_occurrence_identity
        or type(finding.source_locality_identity) is not str
        or not finding.source_locality_identity
        or type(finding.completeness_boundary) is not EventLedgerBoundary
        or type(finding.exact_material) is not bytes
    ):
        raise ValueError("byte-pair position-coordinate finding carries no exact source")


def _measure_through(
    ledger: EventLedger,
    *,
    source_material_acquisition_occurrence_identity: str,
    boundary: EventLedgerBoundary,
) -> FindingOfPositionCoordinatesOfBytePairOccurrences:
    source = read_exact_material_acquisition_result(ledger, source_material_acquisition_occurrence_identity)
    exact_boundary = ledger.append_boundary_through_occurrence(source.identity)
    if type(boundary) is not EventLedgerBoundary or boundary != exact_boundary:
        raise ValueError(
            "byte-pair position-coordinate Measurement requires the exact source boundary"
        )
    exact = acquired_material_bytes(source)
    finding = FindingOfPositionCoordinatesOfBytePairOccurrences(
        source_material_acquisition_occurrence_identity=source.identity,
        source_locality_identity=source.locality_identity,
        completeness_boundary=boundary,
        exact_material=exact,
    )
    _validate_finding(finding)
    return finding


def measure_position_coordinates_of_byte_pair_occurrences(
    ledger: EventLedger,
    *,
    source_material_acquisition_occurrence_identity: str,
) -> FindingOfPositionCoordinatesOfBytePairOccurrences:
    """Measure each exact byte-pair window in one material acquisition result."""

    if not isinstance(ledger, EventLedger):
        raise TypeError("byte-pair position-coordinate Measurement requires one EventLedger")
    if (
        type(source_material_acquisition_occurrence_identity) is not str
        or not source_material_acquisition_occurrence_identity
    ):
        raise ValueError("byte-pair position-coordinate Measurement requires one material acquisition result")
    return _measure_through(
        ledger,
        source_material_acquisition_occurrence_identity=source_material_acquisition_occurrence_identity,
        boundary=ledger.append_boundary_through_occurrence(
            source_material_acquisition_occurrence_identity
        ),
    )


def _assignment_reference(assignment: Event) -> dict[str, str]:
    return {
        "recorded_occurrence_identity": assignment.identity,
        "assignment_identity": assignment.material["assignment_identity"],
        "assignment_subject_identity": assignment.material[
            "assignment_subject_identity"
        ],
    }


def _input_relation(
    finding: FindingOfPositionCoordinatesOfBytePairOccurrences,
    *,
    measurement_act_identity: str,
    act_occurrence_identity: str,
) -> dict[str, Any]:
    return {
        "first_subject": {
            "recorded_occurrence_identity": (
                finding.source_material_acquisition_occurrence_identity
            )
        },
        "relation": "input_to",
        "second_subject": {
            "exact_act": EXACT_ACT,
            "measurement_act_identity": measurement_act_identity,
            "act_occurrence_identity": act_occurrence_identity,
        },
        "through": (
            "one intact exact operator material acquisition result with its exact "
            "material-to-this-Seed Locality occurrence and Evidence"
        ),
    }


def _assignment_material(
    finding: FindingOfPositionCoordinatesOfBytePairOccurrences,
    *,
    standing_boundary_identity: str,
    assignment_identity: str,
    assignment_subject_identity: str,
    measurement_act_identity: str,
    act_occurrence_identity: str,
    measurement_result_identity: str,
) -> dict[str, Any]:
    input_relation = _input_relation(
        finding,
        measurement_act_identity=measurement_act_identity,
        act_occurrence_identity=act_occurrence_identity,
    )
    return {
        "assignment_identity": assignment_identity,
        "assignment_subject_identity": assignment_subject_identity,
        "measurement_act_identity": measurement_act_identity,
        "act_occurrence_identity": act_occurrence_identity,
        "measurement_result_identity": measurement_result_identity,
        "book_clause_identity": "01.Source.D",
        "responsibility": RESPONSIBILITY,
        "responsible_boundary": "this Seed",
        "source_material_acquisition_occurrence_identity": (
            finding.source_material_acquisition_occurrence_identity
        ),
        "source_locality_identity": finding.source_locality_identity,
        "completeness_boundary_identity": finding.completeness_boundary.identity,
        "standing_boundary_identity": standing_boundary_identity,
        "input_relation": input_relation,
        "measurement_rule": MEASUREMENT_RULE,
        "scope": {
            "source_material_acquisition_occurrence_identity": (
                finding.source_material_acquisition_occurrence_identity
            ),
            "source_locality_identity": finding.source_locality_identity,
            "completeness_boundary_identity": (
                finding.completeness_boundary.identity
            ),
            "recording_standing_boundary_identity": standing_boundary_identity,
        },
        "authority": AUTHORITY,
        "limits": [
            "assignment is bounded to this exact material acquisition result and source boundary"
        ],
        "unknown": [
            "Participation or representation of each measured byte pair: Unknown"
        ],
    }


def _require_current_standing(
    ledger: EventLedger,
    *,
    locality_identity: str,
    locality_standing: dict[str, Any],
    source_material_acquisition_occurrence_identity: str | None = None,
    assignment_identity: str | None = None,
) -> str:
    """Validate a carried replay at the current event in its Locality."""

    if type(locality_standing) is not dict:
        raise ValueError(
            "byte-pair position-coordinate Measurement requires current Locality Standing"
        )
    boundary = locality_standing.get("through_event_occurrence_identity")
    acquisition_results = locality_standing.get("material_acquisition_result_occurrences")
    assignments = locality_standing.get("responsibility_assignment_occurrences")
    carried_acquisition_results = {
        occurrence.get("result_occurrence_identity")
        for occurrence in acquisition_results or ()
        if type(occurrence) is dict
    }
    source_has_exact_locality = bool(
        source_material_acquisition_occurrence_identity is None
        or _has_exact_material_locality_to_this_seed(
            ledger, source_material_acquisition_occurrence_identity
        )
    )
    if (
        locality_standing.get("locality_identity") != locality_identity
        or type(boundary) is not str
        or not boundary
        or (
            source_material_acquisition_occurrence_identity is not None
            and (
                source_material_acquisition_occurrence_identity
                not in carried_acquisition_results
                or not source_has_exact_locality
            )
        )
        or (
            assignment_identity is not None
            and (
                type(assignments) is not dict
                or assignments.get(assignment_identity, object()) is not None
            )
        )
    ):
        raise ValueError(
            "byte-pair position-coordinate Measurement requires current Locality Standing"
        )
    boundary_event = ledger.get(boundary)
    locality_events = (
        ledger.list_locality(locality_identity)
        if boundary_event is not None
        else ()
    )
    if (
        boundary_event is None
        or boundary_event.locality_identity != locality_identity
        or ledger.integrity_of(boundary) == CORRUPTED
        or not locality_events
        or locality_events[-1].identity != boundary
    ):
        raise ValueError(
            "byte-pair position-coordinate Measurement requires current Locality Standing"
        )
    return boundary


def _require_exact_responsibility_boundary(
    ledger: EventLedger,
    *,
    locality_identity: str,
    responsibility_boundary_identity: str,
    source_material_acquisition_occurrence_identity: str,
) -> str:
    """Validate the exact earlier boundary that supplies this assignment subject."""

    if (
        type(responsibility_boundary_identity) is not str
        or not responsibility_boundary_identity
    ):
        raise ValueError(
            "byte-pair position-coordinate assignment requires one exact "
            "responsible boundary"
        )
    boundary_event = ledger.get(responsibility_boundary_identity)
    try:
        boundary = ledger.append_boundary_through_occurrence(
            responsibility_boundary_identity
        )
        order = (source_material_acquisition_occurrence_identity,)
        if (
            source_material_acquisition_occurrence_identity
            != responsibility_boundary_identity
        ):
            order = (
                source_material_acquisition_occurrence_identity,
                responsibility_boundary_identity,
            )
        ledger.occurrences_in_append_order(order, locality_identity=locality_identity)
    except ValueError as error:
        raise ValueError(
            "byte-pair position-coordinate assignment requires one exact "
            "responsible boundary"
        ) from error
    if (
        boundary_event is None
        or boundary_event.locality_identity != locality_identity
        or ledger.integrity_of(boundary_event.identity) == CORRUPTED
        or not _has_exact_material_locality_to_this_seed(
            ledger, source_material_acquisition_occurrence_identity
        )
    ):
        raise ValueError(
            "byte-pair position-coordinate assignment requires one exact "
            "responsible boundary"
        )
    source = read_exact_material_acquisition_result(
        ledger, source_material_acquisition_occurrence_identity
    )
    if not any(
        event.identity == source.identity
        for event in ledger.iter_locality_kind(
            locality_identity,
            source.kind,
            through=boundary,
        )
    ):
        raise ValueError(
            "byte-pair position-coordinate assignment requires one exact "
            "responsible boundary"
        )
    return responsibility_boundary_identity


def _record_byte_pair_occurrence_position_measurement_responsibility_assignment(
    ledger: EventLedger,
    *,
    source_material_acquisition_occurrence_identity: str,
    locality_standing: dict[str, Any],
) -> Event:
    finding = measure_position_coordinates_of_byte_pair_occurrences(
        ledger,
        source_material_acquisition_occurrence_identity=source_material_acquisition_occurrence_identity,
    )
    return _record_byte_pair_occurrence_position_measurement_responsibility_assignment_from_finding(
        ledger,
        finding=finding,
        locality_standing=locality_standing,
    )


def _record_byte_pair_occurrence_position_measurement_responsibility_assignment_from_finding(
    ledger: EventLedger,
    *,
    finding: FindingOfPositionCoordinatesOfBytePairOccurrences,
    locality_standing: dict[str, Any],
) -> Event:
    _validate_finding(finding)
    standing_boundary_identity = _require_current_standing(
        ledger,
        locality_identity=finding.source_locality_identity,
        locality_standing=locality_standing,
        source_material_acquisition_occurrence_identity=(
            finding.source_material_acquisition_occurrence_identity
        ),
    )
    # This runtime refusal prevents malformed or already-recorded sources from
    # crossing the public recorder.  Membership establishes neither the
    # missing exact Locality relation nor the required assignment subject and
    # coordinates.
    current_sources = (
        _unassigned_position_coordinate_measurement_acquisition_results_from_bounded_locality_replay(
            ledger,
            locality_standing,
            locality_identity=finding.source_locality_identity,
        )
    )
    if finding.source_material_acquisition_occurrence_identity not in {
        source.source_material_acquisition_occurrence_identity for source in current_sources
    }:
        raise ValueError(
            "byte-pair position-coordinate assignment requires one exact current unassigned material acquisition result"
        )
    global_recording_boundary = ledger.append_boundary()
    identities = {
        "assignment_identity": new_identity(
            "byte_pair_occurrence_position_assignment"
        ),
        "assignment_subject_identity": new_identity(
            "byte_pair_occurrence_position_assignment_subject"
        ),
        "measurement_act_identity": new_identity(
            "byte_pair_occurrence_position_measurement_act"
        ),
        "act_occurrence_identity": new_identity(
            "byte_pair_occurrence_position_measurement_act_occurrence"
        ),
        "measurement_result_identity": new_identity(
            "byte_pair_occurrence_position_measurement_result"
        ),
    }
    if len(set(identities.values())) != len(identities):
        raise ValueError("byte-pair position-coordinate Measurement identities collapsed")
    if ledger.append_boundary() != global_recording_boundary:
        raise ValueError(
            "byte-pair position-coordinate global recording boundary changed before assignment"
        )
    return ledger.append(
        BYTE_PAIR_OCCURRENCE_POSITION_ASSIGNMENT_KIND,
        _assignment_material(
            finding,
            standing_boundary_identity=standing_boundary_identity,
            **identities,
        ),
        locality_identity=finding.source_locality_identity,
    )


def _record_byte_pair_occurrence_position_measurement_responsibility_assignment_from_carried_finding(
    ledger: EventLedger,
    *,
    finding: FindingOfPositionCoordinatesOfBytePairOccurrences,
    locality_standing: dict[str, Any],
) -> Event:
    """Assign one finding produced beside the exact carried replay boundary."""

    return _record_byte_pair_occurrence_position_measurement_responsibility_assignment_from_finding(
        ledger,
        finding=finding,
        locality_standing=locality_standing,
    )


def _record_byte_pair_occurrence_position_measurement_responsibility_assignment_from_responsibility_boundary(
    ledger: EventLedger,
    *,
    finding: FindingOfPositionCoordinatesOfBytePairOccurrences,
    responsibility_boundary_identity: str,
) -> Event:
    """Record one assignment preserving its exact earlier responsible boundary."""

    global_recording_boundary = ledger.append_boundary()
    _validate_finding(finding)
    standing_boundary_identity = _require_exact_responsibility_boundary(
        ledger,
        locality_identity=finding.source_locality_identity,
        responsibility_boundary_identity=responsibility_boundary_identity,
        source_material_acquisition_occurrence_identity=(
            finding.source_material_acquisition_occurrence_identity
        ),
    )
    if any(
        event.material.get("source_material_acquisition_occurrence_identity")
        == finding.source_material_acquisition_occurrence_identity
        for kind in (
            BYTE_PAIR_OCCURRENCE_POSITION_ASSIGNMENT_KIND,
            BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND,
        )
        for event in ledger.iter_locality_kind(
            finding.source_locality_identity,
            kind,
        )
    ):
        raise ValueError(
            "byte-pair position-coordinate assignment requires one exact "
            "unassigned subject at its responsibility boundary"
        )
    identities = {
        "assignment_identity": new_identity(
            "byte_pair_occurrence_position_assignment"
        ),
        "assignment_subject_identity": new_identity(
            "byte_pair_occurrence_position_assignment_subject"
        ),
        "measurement_act_identity": new_identity(
            "byte_pair_occurrence_position_measurement_act"
        ),
        "act_occurrence_identity": new_identity(
            "byte_pair_occurrence_position_measurement_act_occurrence"
        ),
        "measurement_result_identity": new_identity(
            "byte_pair_occurrence_position_measurement_result"
        ),
    }
    if len(set(identities.values())) != len(identities):
        raise ValueError(
            "byte-pair position-coordinate Measurement identities collapsed"
        )
    if ledger.append_boundary() != global_recording_boundary:
        raise ValueError(
            "byte-pair position-coordinate global recording boundary changed "
            "before assignment"
        )
    return ledger.append(
        BYTE_PAIR_OCCURRENCE_POSITION_ASSIGNMENT_KIND,
        _assignment_material(
            finding,
            standing_boundary_identity=standing_boundary_identity,
            **identities,
        ),
        locality_identity=finding.source_locality_identity,
    )


def record_byte_pair_occurrence_position_measurement_responsibility_assignment(
    ledger: EventLedger,
    *,
    source_material_acquisition_occurrence_identity: str,
    locality_standing: dict[str, Any],
) -> Event:
    """Assign the exact source result to this declared Measurement."""

    return _record_byte_pair_occurrence_position_measurement_responsibility_assignment(
        ledger,
        source_material_acquisition_occurrence_identity=source_material_acquisition_occurrence_identity,
        locality_standing=locality_standing,
    )


def _read_assignment(
    ledger: EventLedger, assignment_event_identity: str
) -> tuple[Event, FindingOfPositionCoordinatesOfBytePairOccurrences]:
    assignment = ledger.get(assignment_event_identity)
    if (
        assignment is None
        or assignment.kind != BYTE_PAIR_OCCURRENCE_POSITION_ASSIGNMENT_KIND
        or type(assignment.locality_identity) is not str
        or not assignment.locality_identity
        or assignment.exact_material is not None
        or ledger.integrity_of(assignment.identity) == CORRUPTED
    ):
        raise ValueError("byte-pair position-coordinate assignment is absent or corrupted")
    material = assignment.material
    identities = {
        key: material.get(key)
        for key in (
            "assignment_identity",
            "assignment_subject_identity",
            "measurement_act_identity",
            "act_occurrence_identity",
            "measurement_result_identity",
        )
    }
    source_identity = material.get("source_material_acquisition_occurrence_identity")
    boundary_identity = material.get("completeness_boundary_identity")
    standing_boundary_identity = material.get("standing_boundary_identity")
    if (
        any(type(value) is not str or not value for value in identities.values())
        or len(set(identities.values())) != len(identities)
        or any(
            type(value) is not str or not value
            for value in (
                source_identity,
                boundary_identity,
                standing_boundary_identity,
            )
        )
    ):
        raise ValueError("byte-pair position-coordinate assignment coordinates are not exact")
    try:
        finding = _measure_through(
            ledger,
            source_material_acquisition_occurrence_identity=source_identity,
            boundary=EventLedgerBoundary(boundary_identity),
        )
    except (TypeError, ValueError) as error:
        raise ValueError(
            "byte-pair position-coordinate assignment coordinates are not exact"
        ) from error
    if (
        assignment.locality_identity != finding.source_locality_identity
        or material
        != _assignment_material(
            finding,
            standing_boundary_identity=standing_boundary_identity,
            **identities,
        )
    ):
        raise ValueError("byte-pair position-coordinate assignment coordinates are not exact")
    from seed_runtime.operator_locality_standing import (
        read_operator_locality_standing_through,
    )

    try:
        prior = read_operator_locality_standing_through(
            ledger,
            locality_identity=finding.source_locality_identity,
            through_event_occurrence_identity=standing_boundary_identity,
        )
        ledger.occurrences_in_append_order(
            (standing_boundary_identity, assignment.identity),
            locality_identity=finding.source_locality_identity,
        )
    except (TypeError, ValueError) as error:
        raise ValueError(
            "byte-pair position-coordinate assignment has no exact prior Standing"
        ) from error
    if not any(
        type(occurrence) is dict
        and occurrence.get("result_occurrence_identity") == source_identity
        for occurrence in prior.get("material_acquisition_result_occurrences", ())
    ):
        raise ValueError(
            "byte-pair position-coordinate assignment has no exact prior Standing"
        )
    return assignment, finding


def _require_carried_byte_pair_occurrence_position_assignment(
    ledger: EventLedger,
    *,
    responsibility_assignment: Event,
    finding: FindingOfPositionCoordinatesOfBytePairOccurrences,
) -> None:
    if (
        type(responsibility_assignment) is not Event
        or type(finding) is not FindingOfPositionCoordinatesOfBytePairOccurrences
        or responsibility_assignment.kind
        != BYTE_PAIR_OCCURRENCE_POSITION_ASSIGNMENT_KIND
        or responsibility_assignment.exact_material is not None
        or responsibility_assignment.locality_identity
        != finding.source_locality_identity
        or ledger.integrity_of(responsibility_assignment.identity) == CORRUPTED
    ):
        raise ValueError(
            "byte-pair position-coordinate Measurement requires its exact carried assignment"
        )
    material = responsibility_assignment.material
    identity_coordinates = {
        coordinate: material.get(coordinate)
        for coordinate in (
            "assignment_identity",
            "assignment_subject_identity",
            "measurement_act_identity",
            "act_occurrence_identity",
            "measurement_result_identity",
        )
    }
    standing_boundary_identity = material.get("standing_boundary_identity")
    if (
        any(
            type(identity) is not str or not identity
            for identity in identity_coordinates.values()
        )
        or len(set(identity_coordinates.values())) != len(identity_coordinates)
        or material
        != _assignment_material(
            finding,
            standing_boundary_identity=standing_boundary_identity,
            **identity_coordinates,
        )
    ):
        raise ValueError(
            "byte-pair position-coordinate Measurement requires its exact carried assignment"
        )


def get_byte_pair_occurrence_position_measurement_responsibility_assignment(
    ledger: EventLedger, assignment_event_identity: str
) -> Event:
    assignment, _finding = _read_assignment(ledger, assignment_event_identity)
    return assignment


def _participation(
    finding: FindingOfPositionCoordinatesOfBytePairOccurrences,
    *,
    act_occurrence_identity: str,
) -> dict[str, str]:
    return {
        "subject_reference": finding.source_material_acquisition_occurrence_identity,
        "role": "input",
        "act_occurrence_identity": act_occurrence_identity,
    }


def _act_material(
    finding: FindingOfPositionCoordinatesOfBytePairOccurrences,
    assignment: Event,
) -> dict[str, Any]:
    return {
        "addressed_act_identity": assignment.material["measurement_act_identity"],
        "act_occurrence_identity": assignment.material["act_occurrence_identity"],
        "act": EXACT_ACT,
        "responsibility": RESPONSIBILITY,
        "responsible_boundary": "this Seed",
        "responsibility_assignment_reference": _assignment_reference(assignment),
        "input_relation": assignment.material["input_relation"],
        "participation": _participation(
            finding,
            act_occurrence_identity=assignment.material["act_occurrence_identity"],
        ),
        "authority": AUTHORITY,
        "evidence_scope": (
            "Evidence bounded to this exact byte-pair position-coordinate Measurement occurrence"
        ),
    }


def _record_byte_pair_occurrence_position_measurement_act_evidence(
    ledger: EventLedger,
    *,
    responsibility_assignment_event_identity: str,
    responsibility_assignment_standing: dict[str, Any],
) -> Event:
    assignment, finding = _read_assignment(
        ledger, responsibility_assignment_event_identity
    )
    _require_current_standing(
        ledger,
        locality_identity=assignment.locality_identity,
        locality_standing=responsibility_assignment_standing,
        assignment_identity=assignment.identity,
    )
    for prior in ledger.iter_locality_kind(
        assignment.locality_identity, BYTE_PAIR_OCCURRENCE_POSITION_ACT_EVIDENCE_KIND
    ):
        if (
            prior.material.get("responsibility_assignment_reference")
            == _assignment_reference(assignment)
            or prior.material.get("act_occurrence_identity")
            == assignment.material["act_occurrence_identity"]
        ):
            raise ValueError("byte-pair position-coordinate assignment already carries an Act")
    return ledger.append(
        BYTE_PAIR_OCCURRENCE_POSITION_ACT_EVIDENCE_KIND,
        _act_material(finding, assignment),
        locality_identity=assignment.locality_identity,
    )


def record_byte_pair_occurrence_position_measurement_act_evidence(
    ledger: EventLedger,
    *,
    responsibility_assignment_event_identity: str,
    responsibility_assignment_standing: dict[str, Any],
) -> Event:
    return _record_byte_pair_occurrence_position_measurement_act_evidence(
        ledger,
        responsibility_assignment_event_identity=(
            responsibility_assignment_event_identity
        ),
        responsibility_assignment_standing=responsibility_assignment_standing,
    )


def _record_byte_pair_occurrence_position_measurement_act_evidence_from_carried_assignment(
    ledger: EventLedger,
    *,
    responsibility_assignment: Event,
    finding: FindingOfPositionCoordinatesOfBytePairOccurrences,
    responsibility_assignment_standing: dict[str, Any],
) -> Event:
    """Record the Act beside its just-carried exact assignment and finding."""

    _require_carried_byte_pair_occurrence_position_assignment(
        ledger,
        responsibility_assignment=responsibility_assignment,
        finding=finding,
    )
    _require_current_standing(
        ledger,
        locality_identity=responsibility_assignment.locality_identity,
        locality_standing=responsibility_assignment_standing,
        assignment_identity=responsibility_assignment.identity,
    )
    for prior in ledger.iter_locality_kind(
        responsibility_assignment.locality_identity,
        BYTE_PAIR_OCCURRENCE_POSITION_ACT_EVIDENCE_KIND,
    ):
        if (
            prior.material.get("responsibility_assignment_reference")
            == _assignment_reference(responsibility_assignment)
            or prior.material.get("act_occurrence_identity")
            == responsibility_assignment.material["act_occurrence_identity"]
        ):
            raise ValueError("byte-pair position-coordinate assignment already carries an Act")
    return ledger.append(
        BYTE_PAIR_OCCURRENCE_POSITION_ACT_EVIDENCE_KIND,
        _act_material(finding, responsibility_assignment),
        locality_identity=responsibility_assignment.locality_identity,
    )


def _read_act(
    ledger: EventLedger, act_evidence_event_identity: str
) -> tuple[
    Event,
    Event,
    FindingOfPositionCoordinatesOfBytePairOccurrences,
]:
    act = ledger.get(act_evidence_event_identity)
    if (
        act is None
        or act.kind != BYTE_PAIR_OCCURRENCE_POSITION_ACT_EVIDENCE_KIND
        or act.exact_material is not None
        or ledger.integrity_of(act.identity) == CORRUPTED
    ):
        raise ValueError("byte-pair position-coordinate result requires intact Act Evidence")
    reference = act.material.get("responsibility_assignment_reference")
    try:
        assignment, finding = _read_assignment(
            ledger,
            reference.get("recorded_occurrence_identity")
            if type(reference) is dict
            else "",
        )
    except (TypeError, ValueError) as error:
        raise ValueError(
            "byte-pair position-coordinate result requires intact Act Evidence"
        ) from error
    if (
        act.locality_identity != assignment.locality_identity
        or reference != _assignment_reference(assignment)
        or act.material != _act_material(finding, assignment)
    ):
        raise ValueError("byte-pair position-coordinate result requires intact Act Evidence")
    try:
        ledger.occurrences_in_append_order(
            (assignment.identity, act.identity),
            locality_identity=assignment.locality_identity,
        )
    except ValueError as error:
        raise ValueError(
            "byte-pair position-coordinate Act requires its prior assignment"
        ) from error
    return act, assignment, finding


def get_byte_pair_occurrence_position_measurement_act_evidence(
    ledger: EventLedger, act_evidence_event_identity: str
) -> Event:
    act, _assignment, _finding = _read_act(ledger, act_evidence_event_identity)
    return act


def _canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def _source_position_coordinate_reference(
    *,
    source_material_acquisition_occurrence_identity: str,
    source_locality_identity: str,
    completeness_boundary_identity: str,
    position: int,
    exact_material: bytes,
) -> dict[str, Any]:
    coordinates = {
        "source_material_acquisition_occurrence_identity": source_material_acquisition_occurrence_identity,
        "locality_identity": source_locality_identity,
        "completeness_boundary_identity": completeness_boundary_identity,
        "position": position,
        "exact_material": list(exact_material),
    }
    return {
        "identity": "source-byte-position-coordinate:"
        + hashlib.sha256(_canonical(coordinates).encode("utf-8")).hexdigest(),
        **coordinates,
    }


def _assertion_coordinates(
    finding: FindingOfPositionCoordinatesOfBytePairOccurrences,
    *,
    exact_pair: bytes,
    first_position: int,
    second_position: int,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, int]]:
    subject = {
        "source_material_acquisition_occurrence_identity": (
            finding.source_material_acquisition_occurrence_identity
        ),
        "exact_pair": list(exact_pair),
        "measurement_rule": MEASUREMENT_RULE,
    }
    scope = {
        "source_locality_identity": finding.source_locality_identity,
        "source_material_acquisition_occurrence_identity": (
            finding.source_material_acquisition_occurrence_identity
        ),
        "completeness_boundary_identity": finding.completeness_boundary.identity,
    }
    content = {
        "first_position": first_position,
        "second_position": second_position,
        "first_position_coordinate_reference": (
            _source_position_coordinate_reference(
                source_material_acquisition_occurrence_identity=(
                    finding.source_material_acquisition_occurrence_identity
                ),
                source_locality_identity=finding.source_locality_identity,
                completeness_boundary_identity=(
                    finding.completeness_boundary.identity
                ),
                position=first_position,
                exact_material=exact_pair[:1],
            )
        ),
        "second_position_coordinate_reference": (
            _source_position_coordinate_reference(
                source_material_acquisition_occurrence_identity=(
                    finding.source_material_acquisition_occurrence_identity
                ),
                source_locality_identity=finding.source_locality_identity,
                completeness_boundary_identity=(
                    finding.completeness_boundary.identity
                ),
                position=second_position,
                exact_material=exact_pair[1:],
            )
        ),
    }
    return subject, scope, content


def _assertion(
    finding: FindingOfPositionCoordinatesOfBytePairOccurrences,
    *,
    exact_pair: bytes,
    first_position: int,
    second_position: int,
) -> dict[str, Any]:
    subject, scope, content = _assertion_coordinates(
        finding,
        exact_pair=exact_pair,
        first_position=first_position,
        second_position=second_position,
    )
    assertion_identity = _assertion_identity(
        finding,
        exact_pair=exact_pair,
        first_position=first_position,
        second_position=second_position,
    )
    return {
        "dimensions": {
            "identity": assertion_identity,
            "content": content,
            "source_provenance": "one exact material acquisition occurrence and source boundary",
            "responsibility": ASSERTION_RESPONSIBILITY,
            "authority": "unestablished",
            "evidence_scope": (
                "exact byte-pair position-coordinate Measurement Evidence"
            ),
        },
        "subject_kind": "assertion",
        "responsible_boundary": "this recorded assertion",
        "result": "position",
        "assertion_subject": subject,
        "assertion_scope": scope,
        "input_support": {
            "occurrence_references": [finding.source_material_acquisition_occurrence_identity],
            "local_assertion_references": [],
        },
        "conflicts": "Unknown",
        "unknown": [
            "Participation or representation of this byte pair: Unknown"
        ],
        "limits": [
            "first and second position coordinates bounded by one exact material acquisition result "
            "and source boundary"
        ],
    }


def _assertion_identity(
    finding: FindingOfPositionCoordinatesOfBytePairOccurrences,
    *,
    exact_pair: bytes,
    first_position: int,
    second_position: int,
) -> str:
    subject, scope, content = _assertion_coordinates(
        finding,
        exact_pair=exact_pair,
        first_position=first_position,
        second_position=second_position,
    )
    identity_material = {
        "result": "position",
        "subject": subject,
        "scope": scope,
        "content": content,
    }
    return "byte-pair-occurrence-position:" + hashlib.sha256(
        _canonical(identity_material).encode("utf-8")
    ).hexdigest()


def _assertion_population(
    finding: FindingOfPositionCoordinatesOfBytePairOccurrences,
) -> dict[str, Any]:
    return {
        "result": "position",
        "measurement_rule": MEASUREMENT_RULE,
        "source_material_acquisition_occurrence_identity": (
            finding.source_material_acquisition_occurrence_identity
        ),
        "source_locality_identity": finding.source_locality_identity,
        "completeness_boundary_identity": finding.completeness_boundary.identity,
        "occurrences": max(0, len(finding.exact_material) - 1),
        "dimensions": {
            "content": {
                "exact_pair": "material at first_position through second_position",
                "first_position": "position",
                "second_position": "position of the second byte occurrence",
                "first_position_coordinate_reference": (
                    "exact source-byte position-coordinate reference"
                ),
                "second_position_coordinate_reference": (
                    "exact source-byte position-coordinate reference"
                ),
            },
            "responsibility": ASSERTION_RESPONSIBILITY,
            "authority": "unestablished",
        },
        "unknown": [
            "Participation or representation of each measured byte pair: Unknown"
        ],
    }


def _result_material(
    finding: FindingOfPositionCoordinatesOfBytePairOccurrences,
    assignment: Event,
) -> dict[str, Any]:
    return {
        "result_identity": assignment.material["measurement_result_identity"],
        "addressed_act_identity": assignment.material["measurement_act_identity"],
        "act_occurrence_identity": assignment.material["act_occurrence_identity"],
        "exact_act": EXACT_ACT,
        "responsibility": RESPONSIBILITY,
        "responsible_boundary": "this Seed",
        "responsibility_assignment_reference": _assignment_reference(assignment),
        "input_relation": assignment.material["input_relation"],
        "measurement_rule": MEASUREMENT_RULE,
        "source_localities": [finding.source_locality_identity],
        "source_material_acquisition_occurrence_identity": (
            finding.source_material_acquisition_occurrence_identity
        ),
        "completeness_boundary": {
            "identity": finding.completeness_boundary.identity
        },
        "assertions": _assertion_population(finding),
        "unknown": [
            "Participation or representation of each measured byte pair: Unknown"
        ],
    }


def _refuse_existing_byte_pair_occurrence_position_measurement_result(
    ledger: EventLedger,
    *,
    act: Event,
    act_occurrence_identity: str,
) -> None:
    for prior_yield in ledger.iter_locality_kind(
        act.locality_identity, RECORDED_EVIDENCE_OF_YIELD_RELATION_KIND
    ):
        dimensions = prior_yield.material.get("dimensions")
        if (
            prior_yield.material.get("responsible_act_evidence_identity")
            == act.identity
            or (
                type(dimensions) is dict
                and dimensions.get("act_occurrence_identity")
                == act_occurrence_identity
            )
        ):
            raise ValueError(
                "byte-pair position-coordinate Act already carries a Yield"
            )
    for prior_result in ledger.iter_locality_kind(
        act.locality_identity, BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND
    ):
        if (
            prior_result.material.get("responsible_act_evidence_identity")
            == act.identity
            or prior_result.material.get("act_occurrence_identity")
            == act_occurrence_identity
        ):
            raise ValueError(
                "byte-pair position-coordinate Act already carries a result"
            )


def _record_byte_pair_occurrence_position_measurement_result(
    ledger: EventLedger,
    *,
    act: Event,
    assignment: Event,
    finding: FindingOfPositionCoordinatesOfBytePairOccurrences,
) -> Event:
    result = _result_material(finding, assignment)
    evidence = _record_evidence_of_yield_relation(
        ledger,
        locality_identity=act.locality_identity,
        exact_act=EXACT_ACT,
        act_occurrence_identity=assignment.material["act_occurrence_identity"],
        responsible_act_evidence_identity=act.identity,
        result_kind=RESULT_KIND,
        result_identity=result["result_identity"],
        result_content=result,
        responsibility=RESPONSIBILITY,
        occurrence_boundary="byte_pair_occurrence_position_measurement",
        responsible_boundary="this Seed",
    )
    return ledger.append(
        BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND,
        {
            "result_identity": result["result_identity"],
            "addressed_act_identity": result["addressed_act_identity"],
            "act_occurrence_identity": result["act_occurrence_identity"],
            "exact_act": result["exact_act"],
            "responsibility": result["responsibility"],
            "responsible_boundary": result["responsible_boundary"],
            "responsibility_assignment_reference": result[
                "responsibility_assignment_reference"
            ],
            "input_relation": result["input_relation"],
            "measurement_rule": result["measurement_rule"],
            "source_localities": result["source_localities"],
            "source_material_acquisition_occurrence_identity": result[
                "source_material_acquisition_occurrence_identity"
            ],
            "completeness_boundary": result["completeness_boundary"],
            "assertions": result["assertions"],
            "unknown": result["unknown"],
            "responsible_act_evidence_identity": act.identity,
            "evidence_of_yield_relation_identity": evidence.identity,
        },
        locality_identity=act.locality_identity,
    )


def record_byte_pair_occurrence_position_measurement_result(
    ledger: EventLedger,
    *,
    responsible_act_evidence_event_identity: str,
) -> Event:
    act, assignment, finding = _read_act(
        ledger, responsible_act_evidence_event_identity
    )
    _refuse_existing_byte_pair_occurrence_position_measurement_result(
        ledger,
        act=act,
        act_occurrence_identity=assignment.material["act_occurrence_identity"],
    )
    return _record_byte_pair_occurrence_position_measurement_result(
        ledger,
        act=act,
        assignment=assignment,
        finding=finding,
    )


def _record_byte_pair_occurrence_position_measurement_result_from_carried_act_evidence(
    ledger: EventLedger,
    *,
    responsible_act_evidence: Event,
    responsibility_assignment: Event,
    finding: FindingOfPositionCoordinatesOfBytePairOccurrences,
) -> Event:
    """Record the result beside its just-produced exact Act Evidence."""

    _require_carried_byte_pair_occurrence_position_assignment(
        ledger,
        responsibility_assignment=responsibility_assignment,
        finding=finding,
    )
    if (
        type(responsible_act_evidence) is not Event
        or responsible_act_evidence.kind
        != BYTE_PAIR_OCCURRENCE_POSITION_ACT_EVIDENCE_KIND
        or responsible_act_evidence.exact_material is not None
        or responsible_act_evidence.locality_identity
        != responsibility_assignment.locality_identity
        or ledger.integrity_of(responsible_act_evidence.identity) == CORRUPTED
        or responsible_act_evidence.material
        != _act_material(finding, responsibility_assignment)
        or ledger.append_boundary_through_occurrence(
            responsible_act_evidence.identity
        )
        != ledger.append_boundary()
    ):
        raise ValueError(
            "byte-pair position-coordinate result requires intact Act Evidence"
        )
    return _record_byte_pair_occurrence_position_measurement_result(
        ledger,
        act=responsible_act_evidence,
        assignment=responsibility_assignment,
        finding=finding,
    )


def _read_result(
    ledger: EventLedger, result_event_identity: str
) -> tuple[
    Event,
    FindingOfPositionCoordinatesOfBytePairOccurrences,
    dict[str, Any],
]:
    context = _POSITION_RESULT_READING_CONTEXT.get()
    if (
        context is not None
        and context.ledger is ledger
        and context.result_event_identity == result_event_identity
    ):
        if (
            ledger.get(context.result_snapshot.identity) != context.result_snapshot
            or ledger.integrity_of(context.result_snapshot.identity) == CORRUPTED
        ):
            raise ValueError(
                "byte-pair position-coordinate source changed during its bounded continuation"
            )
        event, finding, assertions = context.reading
        return event, finding, assertions
    event = ledger.get(result_event_identity)
    if (
        event is None
        or event.kind != BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND
        or event.exact_material is not None
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise ValueError("byte-pair position-coordinate result is absent or corrupted")
    try:
        act, assignment, finding = _read_act(
            ledger, event.material.get("responsible_act_evidence_identity")
        )
    except (TypeError, ValueError) as error:
        raise ValueError("byte-pair position-coordinate result carries no exact Act") from error
    expected = {
        **_result_material(finding, assignment),
        "responsible_act_evidence_identity": act.identity,
        "evidence_of_yield_relation_identity": event.material.get(
            "evidence_of_yield_relation_identity"
        ),
    }
    if event.locality_identity != act.locality_identity or event.material != expected:
        raise ValueError("byte-pair position-coordinate result coordinates are not exact")
    evidence_identity = event.material.get("evidence_of_yield_relation_identity")
    try:
        requirements = read_requirements_of_yield_relation(
            ledger,
            recorded_result_event_identity=event.identity,
            evidence_of_yield_relation_event_identity=evidence_identity,
            responsible_act_evidence_event_identity=act.identity,
        )
        evidence = ledger.get(evidence_identity)
    except (TypeError, ValueError) as error:
        raise ValueError("byte-pair position-coordinate result carries no exact Yield") from error
    if (
        not all(requirements.values())
        or evidence is None
        or evidence.kind != RECORDED_EVIDENCE_OF_YIELD_RELATION_KIND
        or ledger.integrity_of(evidence.identity) == CORRUPTED
        or evidence.material.get("occurrence_boundary")
        != "byte_pair_occurrence_position_measurement"
        or evidence.material.get("result_kind") != RESULT_KIND
    ):
        raise ValueError("byte-pair position-coordinate result carries no exact Yield")
    try:
        ordered = ledger.occurrences_in_append_order(
            (act.identity, evidence.identity, event.identity),
            locality_identity=event.locality_identity,
        )
    except ValueError as error:
        raise ValueError("byte-pair position-coordinate result has false occurrence order") from error
    if tuple(item.identity for item in ordered) != (
        act.identity,
        evidence.identity,
        event.identity,
    ):
        raise ValueError("byte-pair position-coordinate result has false occurrence order")
    return event, finding, expected["assertions"]


@contextmanager
def carried_position_measurement_result_reading(
    ledger: EventLedger, result_event_identity: str
) -> Iterator[None]:
    """Keep one validated direct-result reading through its bounded continuation."""

    if not isinstance(ledger, EventLedger):
        raise TypeError("position result continuation requires one EventLedger")
    reading = _read_result(ledger, result_event_identity)
    boundary = ledger.append_boundary_through_occurrence(result_event_identity)
    snapshot = tuple(deepcopy(event) for event in ledger.list(through=boundary))
    token = _POSITION_RESULT_READING_CONTEXT.set(
        _PositionResultReadingContext(
            ledger,
            result_event_identity,
            reading,
            deepcopy(reading[0]),
            snapshot,
        )
    )
    try:
        yield
    finally:
        try:
            _require_carried_position_measurement_source_unchanged()
        finally:
            _POSITION_RESULT_READING_CONTEXT.reset(token)


def get_recorded_byte_pair_occurrence_position_measurement(
    ledger: EventLedger, result_event_identity: str
) -> FindingOfPositionCoordinatesOfBytePairOccurrences:
    _event, finding, _assertions_read = _read_result(ledger, result_event_identity)
    return finding


def _recorded_position_reference(
    event: Event,
    finding: FindingOfPositionCoordinatesOfBytePairOccurrences,
    *,
    exact_pair: bytes,
    first_position: int,
    second_position: int,
) -> ReferenceToRecordedPositionOfBytePairOccurrence:
    return ReferenceToRecordedPositionOfBytePairOccurrence(
        recorded_occurrence_identity=event.identity,
        assertion_identity=_assertion_identity(
            finding,
            exact_pair=exact_pair,
            first_position=first_position,
            second_position=second_position,
        ),
        source_material_acquisition_occurrence_identity=(
            finding.source_material_acquisition_occurrence_identity
        ),
        locality_identity=finding.source_locality_identity,
        completeness_boundary_identity=finding.completeness_boundary.identity,
        exact_pair=exact_pair,
        first_position=first_position,
        second_position=second_position,
    )


def _reference_at_exact_coordinates(
    event: Event,
    finding: FindingOfPositionCoordinatesOfBytePairOccurrences,
    *,
    assertion_identity: str,
    exact_pair: bytes,
    first_position: int,
    second_position: int,
) -> ReferenceToRecordedPositionOfBytePairOccurrence:
    if (
        type(assertion_identity) is not str
        or not assertion_identity
        or type(exact_pair) is not bytes
        or len(exact_pair) != 2
        or type(first_position) is not int
        or first_position < 0
        or type(second_position) is not int
        or second_position != first_position + 1
    ):
        raise ValueError("position reference requires exact addressed coordinates")
    if (
        second_position >= len(finding.exact_material)
        or finding.exact_material[first_position : second_position + 1]
        != exact_pair
        or _assertion_identity(
            finding,
            exact_pair=exact_pair,
            first_position=first_position,
            second_position=second_position,
        )
        != assertion_identity
    ):
        raise ValueError("position result carries no addressed Assertion")
    return _recorded_position_reference(
        event,
        finding,
        exact_pair=exact_pair,
        first_position=first_position,
        second_position=second_position,
    )


def _position_of_exact_source_position_coordinate_reference(
    finding: FindingOfPositionCoordinatesOfBytePairOccurrences,
    position_coordinate_reference: dict[str, Any],
) -> int:
    coordinate_keys = {
        "identity",
        "source_material_acquisition_occurrence_identity",
        "locality_identity",
        "completeness_boundary_identity",
        "position",
        "exact_material",
    }
    if (
        type(position_coordinate_reference) is not dict
        or set(position_coordinate_reference) != coordinate_keys
        or type(position_coordinate_reference.get("identity")) is not str
        or not position_coordinate_reference["identity"]
        or type(position_coordinate_reference.get("source_material_acquisition_occurrence_identity"))
        is not str
        or not position_coordinate_reference["source_material_acquisition_occurrence_identity"]
        or type(position_coordinate_reference.get("locality_identity")) is not str
        or not position_coordinate_reference["locality_identity"]
        or type(
            position_coordinate_reference.get("completeness_boundary_identity")
        )
        is not str
        or not position_coordinate_reference["completeness_boundary_identity"]
        or type(position_coordinate_reference.get("position")) is not int
        or type(position_coordinate_reference.get("exact_material")) is not list
        or len(position_coordinate_reference["exact_material"]) != 1
        or type(position_coordinate_reference["exact_material"][0]) is not int
        or not 0 <= position_coordinate_reference["exact_material"][0] <= 255
    ):
        raise ValueError(
            "addressed source position requires one exact coordinate reference"
        )
    position = position_coordinate_reference["position"]
    if position < 0 or position >= len(finding.exact_material):
        raise ValueError(
            "addressed source position is outside the exact material acquisition result"
        )
    expected = _source_position_coordinate_reference(
        source_material_acquisition_occurrence_identity=(
            finding.source_material_acquisition_occurrence_identity
        ),
        source_locality_identity=finding.source_locality_identity,
        completeness_boundary_identity=finding.completeness_boundary.identity,
        position=position,
        exact_material=finding.exact_material[position : position + 1],
    )
    if position_coordinate_reference != expected:
        raise ValueError(
            "addressed source position is not the exact recorded coordinate"
        )
    return position


def references_to_recorded_byte_pair_occurrences_carrying_addressed_source_position_coordinate(
    ledger: EventLedger,
    result_event_identity: str,
    position_coordinate_reference: dict[str, Any],
) -> tuple[ReferenceToRecordedPositionOfBytePairOccurrence, ...]:
    """Read pair Assertions carrying one exact addressed source coordinate."""

    if not isinstance(ledger, EventLedger):
        raise TypeError("addressed source position requires one EventLedger")
    if type(result_event_identity) is not str or not result_event_identity:
        raise ValueError("addressed source position requires one result occurrence")
    event, finding, _assertion_population_read = _read_result(
        ledger, result_event_identity
    )
    position = _position_of_exact_source_position_coordinate_reference(
        finding, position_coordinate_reference
    )
    first_positions = []
    if position > 0:
        first_positions.append(position - 1)
    if position + 1 < len(finding.exact_material):
        first_positions.append(position)
    return tuple(
        _recorded_position_reference(
            event,
            finding,
            exact_pair=finding.exact_material[
                first_position : first_position + 2
            ],
            first_position=first_position,
            second_position=first_position + 1,
        )
        for first_position in first_positions
    )


def references_to_addressed_recorded_position_coordinates_of_byte_pair_occurrences(
    ledger: EventLedger,
    result_event_identity: str,
    assertion_identities: tuple[str, ...],
    *,
    exact_coordinates: tuple[tuple[bytes, int, int], ...] | None = None,
) -> tuple[
    ReferenceToRecordedPositionOfBytePairOccurrence, ...
]:
    """Resolve exact addressed Assertions with one bounded result read."""

    if not isinstance(ledger, EventLedger):
        raise TypeError("position references require one EventLedger")
    if type(result_event_identity) is not str or not result_event_identity:
        raise ValueError("position references require one result occurrence")
    if (
        type(assertion_identities) is not tuple
        or not assertion_identities
        or any(type(identity) is not str or not identity for identity in assertion_identities)
        or len(set(assertion_identities)) != len(assertion_identities)
    ):
        raise ValueError("position references require distinct Assertion identities")
    if (
        exact_coordinates is not None
        and (
            type(exact_coordinates) is not tuple
            or len(exact_coordinates) != len(assertion_identities)
            or any(
                type(coordinates) is not tuple or len(coordinates) != 3
                for coordinates in exact_coordinates
            )
        )
    ):
        raise ValueError("position references require exact addressed coordinates")
    event, finding, _assertion_population_read = _read_result(
        ledger, result_event_identity
    )
    if exact_coordinates is not None:
        return tuple(
            _reference_at_exact_coordinates(
                event,
                finding,
                assertion_identity=assertion_identity,
                exact_pair=coordinates[0],
                first_position=coordinates[1],
                second_position=coordinates[2],
            )
            for assertion_identity, coordinates in zip(
                assertion_identities, exact_coordinates, strict=True
            )
        )
    requested = set(assertion_identities)
    resolved = {}
    for first_position in range(len(finding.exact_material) - 1):
        second_position = first_position + 1
        exact_pair = finding.exact_material[first_position : second_position + 1]
        assertion_identity = _assertion_identity(
            finding,
            exact_pair=exact_pair,
            first_position=first_position,
            second_position=second_position,
        )
        if assertion_identity in requested:
            resolved[assertion_identity] = _recorded_position_reference(
                event,
                finding,
                exact_pair=exact_pair,
                first_position=first_position,
                second_position=second_position,
            )
            if len(resolved) == len(requested):
                break
    if set(resolved) != requested:
        raise ValueError("position result carries no addressed Assertion")
    return tuple(resolved[identity] for identity in assertion_identities)


def references_to_recorded_position_coordinates_of_byte_pair_occurrences(
    ledger: EventLedger, result_event_identity: str
) -> tuple[
    ReferenceToRecordedPositionOfBytePairOccurrence, ...
]:
    event, finding, _assertion_population_read = _read_result(
        ledger, result_event_identity
    )
    return tuple(
        _recorded_position_reference(
            event,
            finding,
            exact_pair=finding.exact_material[
                first_position : first_position + 2
            ],
            first_position=first_position,
            second_position=first_position + 1,
        )
        for first_position in range(len(finding.exact_material) - 1)
    )


def source_position_coordinate_references_of_recorded_position_measurement(
    ledger: EventLedger, result_event_identity: str
) -> Iterator[dict[str, Any]]:
    """Yield the exact bounded source-position subjects from one result read."""

    _event, finding, _assertion_population_read = _read_result(
        ledger, result_event_identity
    )
    for position, value in enumerate(finding.exact_material):
        yield _source_position_coordinate_reference(
            source_material_acquisition_occurrence_identity=(
                finding.source_material_acquisition_occurrence_identity
            ),
            source_locality_identity=finding.source_locality_identity,
            completeness_boundary_identity=finding.completeness_boundary.identity,
            position=position,
            exact_material=bytes((value,)),
        )


def _recorded_position_assertion_coordinates_for_locality_movement(
    ledger: EventLedger,
    *,
    result_event_identity: str,
    assertion_identity: str,
) -> dict[str, Any]:
    event, finding, _assertion_population_read = _read_result(
        ledger, result_event_identity
    )
    for first_position in range(len(finding.exact_material) - 1):
        second_position = first_position + 1
        exact_pair = finding.exact_material[first_position : second_position + 1]
        if (
            _assertion_identity(
                finding,
                exact_pair=exact_pair,
                first_position=first_position,
                second_position=second_position,
            )
            == assertion_identity
        ):
            return _assertion(
                finding,
                exact_pair=exact_pair,
                first_position=first_position,
                second_position=second_position,
            )
    raise ValueError(
        "position Assertion Locality movement requires exact source coordinates"
    )


def _recorded_position_assertion_coordinate_population_for_locality_movement(
    ledger: EventLedger,
    *,
    result_event_identity: str,
) -> Iterator[dict[str, Any]]:
    """Yield every position Assertion after one exact bounded result read.

    The population is reconstructed from the validated finding. Reading it
    records no movement and grants no later relation or Standing.
    """

    _event, finding, _assertion_population_read = _read_result(
        ledger, result_event_identity
    )
    return (
        _assertion(
            finding,
            exact_pair=finding.exact_material[
                first_position : first_position + 2
            ],
            first_position=first_position,
            second_position=first_position + 1,
        )
        for first_position in range(len(finding.exact_material) - 1)
    )


def move_recorded_position_assertion_to_locality(
    ledger: EventLedger,
    *,
    source_assertion_reference: dict[str, str],
    destination_locality: str,
) -> RecordedAssertionCarriedByLocalityMovement:
    """Carry one exact recorded position Assertion through 03.Movement.A."""

    from seed_runtime.byte_measurement import (
        _move_assertion_reference_to_locality,
    )

    return _move_assertion_reference_to_locality(
        ledger,
        source_assertion_reference=source_assertion_reference,
        destination_locality=destination_locality,
    )
