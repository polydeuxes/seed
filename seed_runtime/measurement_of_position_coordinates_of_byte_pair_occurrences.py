"""Measure first and second position coordinates of each byte-pair occurrence.

The exact source Ingest result bounds the population.  The Measurement records
first and second byte values with their position coordinates; it establishes no
recurrence, represented relation, character, word, or meaning.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any, NamedTuple

from seed_runtime.event import Event
from seed_runtime.events import CORRUPTED, EventLedger, EventLedgerBoundary
from seed_runtime.evidence_of_yield_relation import (
    RECORDED_EVIDENCE_OF_YIELD_RELATION_KIND,
    _record_evidence_of_yield_relation,
    read_requirements_of_yield_relation,
)
from seed_runtime.identities import new_identity
from seed_runtime.material_ingest import (
    ingested_material_bytes,
    read_exact_ingest_result,
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
EXACT_ACT = "Measurement of position coordinates of byte-pair occurrences"
RESPONSIBILITY = (
    "Measurement of the position coordinates of each exact byte-pair occurrence "
    "within one exact Ingest result"
)
MEASUREMENT_RULE = (
    "each exact byte-pair occurrence with its first position and second position "
    "in source occurrence order within one exact Ingest result"
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
    source_ingest_occurrence_identity: str
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


class ReferenceToRecordedPositionOfBytePairOccurrence(
    NamedTuple
):
    recorded_occurrence_identity: str
    assertion_identity: str
    source_ingest_occurrence_identity: str
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
            source_ingest_occurrence_identity=(
                self.source_ingest_occurrence_identity
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
            source_ingest_occurrence_identity=(
                self.source_ingest_occurrence_identity
            ),
            source_locality_identity=self.locality_identity,
            completeness_boundary_identity=(
                self.completeness_boundary_identity
            ),
            position=self.second_position,
            exact_material=self.exact_pair[1:],
        )


def _validate_finding(
    finding: FindingOfPositionCoordinatesOfBytePairOccurrences,
) -> None:
    if type(finding) is not FindingOfPositionCoordinatesOfBytePairOccurrences:
        raise TypeError("byte-pair position-coordinate Measurement requires one exact finding")
    if (
        type(finding.source_ingest_occurrence_identity) is not str
        or not finding.source_ingest_occurrence_identity
        or type(finding.source_locality_identity) is not str
        or not finding.source_locality_identity
        or type(finding.completeness_boundary) is not EventLedgerBoundary
        or type(finding.exact_material) is not bytes
    ):
        raise ValueError("byte-pair position-coordinate finding carries no exact source")


def _measure_through(
    ledger: EventLedger,
    *,
    source_ingest_occurrence_identity: str,
    boundary: EventLedgerBoundary,
) -> FindingOfPositionCoordinatesOfBytePairOccurrences:
    source = read_exact_ingest_result(ledger, source_ingest_occurrence_identity)
    exact_boundary = ledger.append_boundary_through_occurrence(source.identity)
    if type(boundary) is not EventLedgerBoundary or boundary != exact_boundary:
        raise ValueError(
            "byte-pair position-coordinate Measurement requires the exact source boundary"
        )
    exact = ingested_material_bytes(source)
    finding = FindingOfPositionCoordinatesOfBytePairOccurrences(
        source_ingest_occurrence_identity=source.identity,
        source_locality_identity=source.locality_identity,
        completeness_boundary=boundary,
        exact_material=exact,
    )
    _validate_finding(finding)
    return finding


def measure_position_coordinates_of_byte_pair_occurrences(
    ledger: EventLedger,
    *,
    source_ingest_occurrence_identity: str,
) -> FindingOfPositionCoordinatesOfBytePairOccurrences:
    """Measure each exact byte-pair window in one Ingest result."""

    if not isinstance(ledger, EventLedger):
        raise TypeError("byte-pair position-coordinate Measurement requires one EventLedger")
    if (
        type(source_ingest_occurrence_identity) is not str
        or not source_ingest_occurrence_identity
    ):
        raise ValueError("byte-pair position-coordinate Measurement requires one Ingest result")
    return _measure_through(
        ledger,
        source_ingest_occurrence_identity=source_ingest_occurrence_identity,
        boundary=ledger.append_boundary_through_occurrence(
            source_ingest_occurrence_identity
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
                finding.source_ingest_occurrence_identity
            )
        },
        "relation": "input_to",
        "second_subject": {
            "exact_act": EXACT_ACT,
            "measurement_act_identity": measurement_act_identity,
            "act_occurrence_identity": act_occurrence_identity,
        },
        "through": (
            "one intact exact Ingest result carried by current Locality Standing"
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
        "source_ingest_occurrence_identity": (
            finding.source_ingest_occurrence_identity
        ),
        "source_locality_identity": finding.source_locality_identity,
        "completeness_boundary_identity": finding.completeness_boundary.identity,
        "standing_boundary_identity": standing_boundary_identity,
        "input_relation": input_relation,
        "measurement_rule": MEASUREMENT_RULE,
        "scope": {
            "source_ingest_occurrence_identity": (
                finding.source_ingest_occurrence_identity
            ),
            "source_locality_identity": finding.source_locality_identity,
            "completeness_boundary_identity": (
                finding.completeness_boundary.identity
            ),
            "recording_standing_boundary_identity": standing_boundary_identity,
        },
        "authority": AUTHORITY,
        "limits": [
            "assignment is bounded to this exact Ingest result and source boundary"
        ],
        "unknown": [
            "Participation or representation of each measured byte pair remains Unknown"
        ],
    }


def _require_current_standing(
    ledger: EventLedger,
    *,
    locality_identity: str,
    locality_standing: dict[str, Any],
    source_ingest_occurrence_identity: str | None = None,
    assignment_identity: str | None = None,
) -> str:
    from seed_runtime.operator_locality_standing import (
        read_operator_locality_standing,
    )

    if type(locality_standing) is not dict:
        raise ValueError(
            "byte-pair position-coordinate Measurement requires current Locality Standing"
        )
    current = read_operator_locality_standing(
        ledger, locality_identity=locality_identity
    )
    boundary = locality_standing.get("through_event_occurrence_identity")
    ingests = locality_standing.get("ingest_occurrences")
    assignments = locality_standing.get("responsibility_assignment_occurrences")
    carried_ingests = {
        occurrence.get("evidence_event_identity")
        for occurrence in ingests or ()
        if type(occurrence) is dict
    }
    if (
        locality_standing != current
        or locality_standing.get("locality_identity") != locality_identity
        or type(boundary) is not str
        or not boundary
        or (
            source_ingest_occurrence_identity is not None
            and source_ingest_occurrence_identity not in carried_ingests
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
    return boundary


def _require_carried_standing_at_tip(
    ledger: EventLedger,
    *,
    locality_identity: str,
    locality_standing: dict[str, Any],
    source_ingest_occurrence_identity: str | None = None,
    assignment_identity: str | None = None,
) -> str:
    """Validate a call-local Standing already advanced to the append tip."""

    if type(locality_standing) is not dict:
        raise ValueError(
            "byte-pair position-coordinate Measurement requires current Locality Standing"
        )
    boundary = locality_standing.get("through_event_occurrence_identity")
    ingests = locality_standing.get("ingest_occurrences")
    assignments = locality_standing.get("responsibility_assignment_occurrences")
    carried_ingests = {
        occurrence.get("evidence_event_identity")
        for occurrence in ingests or ()
        if type(occurrence) is dict
    }
    if (
        locality_standing.get("locality_identity") != locality_identity
        or type(boundary) is not str
        or not boundary
        or (
            source_ingest_occurrence_identity is not None
            and source_ingest_occurrence_identity not in carried_ingests
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
    if (
        boundary_event is None
        or boundary_event.locality_identity != locality_identity
        or ledger.integrity_of(boundary) == CORRUPTED
        or ledger.append_boundary_through_occurrence(boundary)
        != ledger.append_boundary()
    ):
        raise ValueError(
            "byte-pair position-coordinate Measurement requires current Locality Standing"
        )
    return boundary


def _record_byte_pair_occurrence_position_measurement_responsibility_assignment(
    ledger: EventLedger,
    *,
    source_ingest_occurrence_identity: str,
    locality_standing: dict[str, Any],
    carried: bool,
) -> Event:
    finding = measure_position_coordinates_of_byte_pair_occurrences(
        ledger,
        source_ingest_occurrence_identity=source_ingest_occurrence_identity,
    )
    return _record_byte_pair_occurrence_position_measurement_responsibility_assignment_from_finding(
        ledger,
        finding=finding,
        locality_standing=locality_standing,
        carried=carried,
    )


def _record_byte_pair_occurrence_position_measurement_responsibility_assignment_from_finding(
    ledger: EventLedger,
    *,
    finding: FindingOfPositionCoordinatesOfBytePairOccurrences,
    locality_standing: dict[str, Any],
    carried: bool,
) -> Event:
    _validate_finding(finding)
    require_standing = (
        _require_carried_standing_at_tip if carried else _require_current_standing
    )
    standing_boundary_identity = require_standing(
        ledger,
        locality_identity=finding.source_locality_identity,
        locality_standing=locality_standing,
        source_ingest_occurrence_identity=(
            finding.source_ingest_occurrence_identity
        ),
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
        raise ValueError("byte-pair position-coordinate Measurement identities collapsed")
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
    """Assign one finding produced beside the exact carried Standing at the tip."""

    return _record_byte_pair_occurrence_position_measurement_responsibility_assignment_from_finding(
        ledger,
        finding=finding,
        locality_standing=locality_standing,
        carried=True,
    )


def record_byte_pair_occurrence_position_measurement_responsibility_assignment(
    ledger: EventLedger,
    *,
    source_ingest_occurrence_identity: str,
    locality_standing: dict[str, Any],
) -> Event:
    """Assign the exact source result to this declared Measurement."""

    return _record_byte_pair_occurrence_position_measurement_responsibility_assignment(
        ledger,
        source_ingest_occurrence_identity=source_ingest_occurrence_identity,
        locality_standing=locality_standing,
        carried=False,
    )


def _record_byte_pair_occurrence_position_measurement_responsibility_assignment_from_carried_standing(
    ledger: EventLedger,
    *,
    source_ingest_occurrence_identity: str,
    locality_standing: dict[str, Any],
) -> Event:
    """Assign the exact source already carried at the current append tip."""

    return _record_byte_pair_occurrence_position_measurement_responsibility_assignment(
        ledger,
        source_ingest_occurrence_identity=source_ingest_occurrence_identity,
        locality_standing=locality_standing,
        carried=True,
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
    source_identity = material.get("source_ingest_occurrence_identity")
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
            source_ingest_occurrence_identity=source_identity,
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
        and occurrence.get("evidence_event_identity") == source_identity
        for occurrence in prior.get("ingest_occurrences", ())
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
        "subject_reference": finding.source_ingest_occurrence_identity,
        "role": "input",
        "act_occurrence_identity": act_occurrence_identity,
    }


def _act_material(
    finding: FindingOfPositionCoordinatesOfBytePairOccurrences,
    assignment: Event,
) -> dict[str, Any]:
    return {
        "downstream_act_identity": assignment.material["measurement_act_identity"],
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
    carried: bool,
) -> Event:
    assignment, finding = _read_assignment(
        ledger, responsibility_assignment_event_identity
    )
    require_standing = (
        _require_carried_standing_at_tip if carried else _require_current_standing
    )
    require_standing(
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
        carried=False,
    )


def _record_byte_pair_occurrence_position_measurement_act_evidence_from_carried_standing(
    ledger: EventLedger,
    *,
    responsibility_assignment_event_identity: str,
    responsibility_assignment_standing: dict[str, Any],
) -> Event:
    """Record the Act beside its just-carried exact assignment occurrence."""

    return _record_byte_pair_occurrence_position_measurement_act_evidence(
        ledger,
        responsibility_assignment_event_identity=(
            responsibility_assignment_event_identity
        ),
        responsibility_assignment_standing=responsibility_assignment_standing,
        carried=True,
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
    _require_carried_standing_at_tip(
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
    source_ingest_occurrence_identity: str,
    source_locality_identity: str,
    completeness_boundary_identity: str,
    position: int,
    exact_material: bytes,
) -> dict[str, Any]:
    coordinates = {
        "source_ingest_occurrence_identity": source_ingest_occurrence_identity,
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
        "source_ingest_occurrence_identity": (
            finding.source_ingest_occurrence_identity
        ),
        "exact_pair": list(exact_pair),
        "measurement_rule": MEASUREMENT_RULE,
    }
    scope = {
        "source_locality_identity": finding.source_locality_identity,
        "source_ingest_occurrence_identity": (
            finding.source_ingest_occurrence_identity
        ),
        "completeness_boundary_identity": finding.completeness_boundary.identity,
    }
    content = {
        "first_position": first_position,
        "second_position": second_position,
        "first_position_coordinate_reference": (
            _source_position_coordinate_reference(
                source_ingest_occurrence_identity=(
                    finding.source_ingest_occurrence_identity
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
                source_ingest_occurrence_identity=(
                    finding.source_ingest_occurrence_identity
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
            "source_provenance": "one exact Ingest occurrence and source boundary",
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
            "occurrence_references": [finding.source_ingest_occurrence_identity],
            "local_assertion_references": [],
        },
        "conflicts": "Unknown",
        "unknown": [
            "Participation or representation of this byte pair remains Unknown"
        ],
        "limits": [
            "first and second position coordinates bounded by one exact Ingest result "
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
        "source_ingest_occurrence_identity": (
            finding.source_ingest_occurrence_identity
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
            "Participation or representation of each measured byte pair remains Unknown"
        ],
    }


def _result_material(
    finding: FindingOfPositionCoordinatesOfBytePairOccurrences,
    assignment: Event,
) -> dict[str, Any]:
    return {
        "result_identity": assignment.material["measurement_result_identity"],
        "downstream_act_identity": assignment.material["measurement_act_identity"],
        "act_occurrence_identity": assignment.material["act_occurrence_identity"],
        "exact_act": EXACT_ACT,
        "responsibility": RESPONSIBILITY,
        "responsible_boundary": "this Seed",
        "responsibility_assignment_reference": _assignment_reference(assignment),
        "input_relation": assignment.material["input_relation"],
        "measurement_rule": MEASUREMENT_RULE,
        "source_localities": [finding.source_locality_identity],
        "source_ingest_occurrence_identity": (
            finding.source_ingest_occurrence_identity
        ),
        "completeness_boundary": {
            "identity": finding.completeness_boundary.identity
        },
        "assertions": _assertion_population(finding),
        "unknown": [
            "Participation or representation of each measured byte pair remains Unknown"
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
            "downstream_act_identity": result["downstream_act_identity"],
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
            "source_ingest_occurrence_identity": result[
                "source_ingest_occurrence_identity"
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
        source_ingest_occurrence_identity=(
            finding.source_ingest_occurrence_identity
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
