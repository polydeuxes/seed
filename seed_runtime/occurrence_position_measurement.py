from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from typing import Any

from seed_runtime.event import Event
from seed_runtime.events import CORRUPTED, EventLedger, EventLedgerBoundary
from seed_runtime.identities import new_identity
from seed_runtime.evidence_of_yield_relation import (
    RECORDED_EVIDENCE_OF_YIELD_RELATION_KIND,
    _record_evidence_of_yield_relation,
    read_requirements_of_yield_relation,
)

OCCURRENCE_POSITION_RECORDED_KIND = (
    "operator.measurement.locality_occurrence_position_recorded"
)
OCCURRENCE_POSITION_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND = (
    "operator.measurement.locality_occurrence_position_responsibility_assignment_recorded"
)
OCCURRENCE_POSITION_ACT_EVIDENCE_KIND = (
    "operator.measurement.locality_occurrence_position_act_evidenced"
)
OCCURRENCE_POSITION_RESULT_KIND = "occurrence position Measurement result"
OCCURRENCE_POSITION_ACT = "occurrence position Measurement"
OCCURRENCE_POSITION_RESPONSIBILITY = (
    "establish each occurrence position within one exact Locality and boundary"
)
OCCURRENCE_POSITION_MEASUREMENT_RULE = (
    "preserve each exact occurrence in one exact Locality with its source-order "
    "position coordinate through one completeness boundary"
)
OCCURRENCE_POSITION_AUTHORITY = "bounded repository authority"
MEASURED_ASSERTION_RESPONSIBILITY = (
    "preserve this measured Assertion's carried Standing coordinates"
)
OCCURRENCE_POSITION_RESULT_COORDINATES = frozenset(
    {
        "result_identity",
        "addressed_act_identity",
        "act_occurrence_identity",
        "exact_act",
        "responsibility",
        "responsible_boundary",
        "responsibility_assignment_evidence",
        "responsibility_assignment_reference",
        "measurement_rule",
        "source_localities",
        "completeness_boundary",
        "assertions",
    }
)
EVENT_KIND_RESPONSIBILITIES = {
    OCCURRENCE_POSITION_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND: "01.Source.D",
    OCCURRENCE_POSITION_RECORDED_KIND: "01.Source.D",
    OCCURRENCE_POSITION_ACT_EVIDENCE_KIND: "02.Acts.A",
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
    assignment: Event,
    assertions: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "result_identity": assignment.material["measurement_result_identity"],
        "addressed_act_identity": assignment.material["measurement_act_identity"],
        "act_occurrence_identity": assignment.material["act_occurrence_identity"],
        "exact_act": OCCURRENCE_POSITION_ACT,
        "responsibility": OCCURRENCE_POSITION_RESPONSIBILITY,
        "responsible_boundary": "this Seed",
        "responsibility_assignment_evidence": _responsibility_assignment(finding),
        "responsibility_assignment_reference": _assignment_reference(assignment),
        "measurement_rule": OCCURRENCE_POSITION_MEASUREMENT_RULE,
        "source_localities": [finding.source_locality_identity],
        "completeness_boundary": {
            "identity": finding.completeness_boundary.identity,
        },
        "assertions": assertions,
    }


def _responsibility_assignment(
    finding: OccurrencePositionFinding,
) -> dict[str, Any]:
    return {
        "responsible_boundary": "this Seed",
        "source_occurrence_references": [
            {"occurrence_identity": identity}
            for identity, _position in finding.occurrences
        ],
        "completeness_boundary": finding.completeness_boundary.identity,
        "determination": OCCURRENCE_POSITION_MEASUREMENT_RULE,
    }


def _assignment_reference(assignment: Event) -> dict[str, str]:
    return {
        "recorded_occurrence_identity": assignment.identity,
        "assignment_identity": assignment.material["assignment_identity"],
        "assignment_subject_identity": assignment.material[
            "assignment_subject_identity"
        ],
        "book_clause_identity": assignment.material["book_clause_identity"],
        "result_boundary_identity": assignment.material[
            "result_boundary_identity"
        ],
    }


def _assignment_material(
    finding: OccurrencePositionFinding,
    *,
    standing_boundary_identity: str | None,
    assignment_identity: str,
    assignment_subject_identity: str,
    measurement_act_identity: str,
    act_occurrence_identity: str,
    measurement_result_identity: str,
) -> dict[str, Any]:
    return {
        "assignment_identity": assignment_identity,
        "assignment_subject_identity": assignment_subject_identity,
        "measurement_act_identity": measurement_act_identity,
        "act_occurrence_identity": act_occurrence_identity,
        "measurement_result_identity": measurement_result_identity,
        "result_boundary_identity": measurement_result_identity,
        "book_clause_identity": "01.Source.D",
        "responsibility": OCCURRENCE_POSITION_RESPONSIBILITY,
        "responsible_boundary": "this Seed",
        "responsibility_assignment_evidence": _responsibility_assignment(finding),
        "measurement_rule": OCCURRENCE_POSITION_MEASUREMENT_RULE,
        "source_locality_identity": finding.source_locality_identity,
        "completeness_boundary_identity": finding.completeness_boundary.identity,
        "standing_boundary_identity": standing_boundary_identity,
        "scope": {
            "recording_standing_boundary_identity": standing_boundary_identity,
            "source_locality_identity": finding.source_locality_identity,
            "completeness_boundary_identity": finding.completeness_boundary.identity,
        },
        "limits": [
            "assignment is bounded to this exact Locality and completeness boundary"
        ],
        "unknown": ["Participation and represented relation: Unknown"],
    }


def _canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def _position_assertion_identity(
    *,
    subject: dict[str, Any],
    scope: dict[str, Any],
    content: dict[str, Any],
) -> str:
    coordinates = {
        "result": "position",
        "subject": subject,
        "scope": scope,
        "content": content,
    }
    return "assertion_" + hashlib.sha256(
        _canonical(coordinates).encode("utf-8")
    ).hexdigest()


def _position_assertions(
    finding: OccurrencePositionFinding,
) -> list[dict[str, Any]]:
    assertions = []
    for occurrence_identity, position in finding.occurrences:
        scope = {"source_localities": [finding.source_locality_identity]}
        boundary = {"identity": finding.completeness_boundary.identity}
        subject = {
            "occurrence_identity": occurrence_identity,
            "measurement_rule": OCCURRENCE_POSITION_MEASUREMENT_RULE,
        }
        content = {
            "position": position,
            "completeness_boundary": boundary,
        }
        assertions.append(
            {
                "dimensions": {
                    "identity": _position_assertion_identity(
                        subject=subject,
                        scope=scope,
                        content=content,
                    ),
                    "content": content,
                    "source_provenance": (
                        "complete exact Locality through one boundary"
                    ),
                    "responsibility": MEASURED_ASSERTION_RESPONSIBILITY,
                    "evidence_scope": (
                        "exact occurrence position Measurement Evidence"
                    ),
                },
                "subject_kind": "assertion",
                "responsible_boundary": "this recorded assertion",
                "result": "position",
                "assertion_subject": subject,
                "assertion_scope": scope,
                "input_support": {
                    "occurrence_references": [occurrence_identity],
                    "local_assertion_references": [],
                },
                "conflicts": "Unknown",
                "unknown": [
                    "what this occurrence participates in or represents: Unknown"
                ],
                "limits": [
                    "exact occurrence position bounded by source Locality and "
                    "completeness boundary"
                ],
            }
        )
    return assertions


def _occurrence_position_participation(
    finding: OccurrencePositionFinding,
    *,
    act_occurrence_identity: str,
) -> list[dict[str, str]]:
    return [
        {
            "subject_reference": identity,
            "role": "exact occurrence",
            "act_occurrence_identity": act_occurrence_identity,
        }
        for identity, _position in finding.occurrences
    ]


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


def _occurrence_position_act_evidence_material(
    finding: OccurrencePositionFinding,
    *,
    assignment: Event,
    participation: list[dict[str, str]],
) -> dict[str, Any]:
    return {
        "addressed_act_identity": assignment.material["measurement_act_identity"],
        "act_occurrence_identity": assignment.material["act_occurrence_identity"],
        "act": OCCURRENCE_POSITION_ACT,
        "responsibility": OCCURRENCE_POSITION_RESPONSIBILITY,
        "responsible_boundary": "this Seed",
        "responsibility_assignment_evidence": _responsibility_assignment(finding),
        "responsibility_assignment_reference": _assignment_reference(assignment),
        "evidence_scope": (
            "Evidence bounded to this exact occurrence position Measurement "
            "occurrence"
        ),
        "source_locality_identity": finding.source_locality_identity,
        "participation": participation,
    }


def _require_current_locality_standing(
    ledger: EventLedger,
    *,
    locality_identity: str,
    locality_standing: dict[str, Any],
    required_assignment_identity: str | None = None,
) -> str | None:
    if type(locality_standing) is not dict:
        raise ValueError(
            "occurrence position Measurement requires exact current Locality Standing"
        )
    # Imported here because the Standing reader imports this module's event
    # contract. Recording is runtime work after both modules are initialized.
    from seed_runtime.operator_locality_standing import (
        read_operator_locality_standing,
    )

    current = read_operator_locality_standing(
        ledger, locality_identity=locality_identity
    )
    carried = locality_standing.get("responsibility_assignment_occurrences")
    if (
        locality_standing != current
        or locality_standing.get("locality_identity") != locality_identity
        or (
            required_assignment_identity is not None
            and (
                type(carried) is not dict
                or carried.get(required_assignment_identity, object()) is not None
            )
        )
    ):
        raise ValueError(
            "occurrence position Measurement requires exact current Locality Standing"
        )
    boundary = locality_standing.get("through_event_occurrence_identity")
    if boundary is not None and (type(boundary) is not str or not boundary):
        raise ValueError(
            "occurrence position Measurement requires exact current Locality Standing"
        )
    return boundary


def _require_carried_locality_standing_at_tip(
    ledger: EventLedger,
    *,
    locality_identity: str,
    locality_standing: dict[str, Any],
    required_assignment_identity: str | None = None,
) -> str | None:
    """Validate same-call carried Standing without replaying its Locality."""

    if type(locality_standing) is not dict:
        raise ValueError(
            "occurrence position Measurement requires exact current Locality Standing"
        )
    boundary = locality_standing.get("through_event_occurrence_identity")
    carried = locality_standing.get("responsibility_assignment_occurrences")
    if (
        locality_standing.get("locality_identity") != locality_identity
        or boundary is None
        or type(boundary) is not str
        or not boundary
        or (
            required_assignment_identity is not None
            and (
                type(carried) is not dict
                or carried.get(required_assignment_identity, object()) is not None
            )
        )
    ):
        raise ValueError(
            "occurrence position Measurement requires exact current Locality Standing"
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
            "occurrence position Measurement requires exact current Locality Standing"
        )
    return boundary


def _record_occurrence_position_measurement_responsibility_assignment(
    ledger: EventLedger,
    *,
    recording_locality_identity: str,
    finding: OccurrencePositionFinding,
    locality_standing: dict[str, Any],
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
                "occurrence position Measurement requires exact current Locality Standing"
            )
    else:
        _exact_occurrence_position_finding(ledger, finding)
    require_standing = (
        _require_carried_locality_standing_at_tip
        if carried
        else _require_current_locality_standing
    )
    standing_boundary_identity = require_standing(
        ledger,
        locality_identity=recording_locality_identity,
        locality_standing=locality_standing,
    )
    if (
        carried
        and (
            not finding.occurrences
            or finding.occurrences[-1][0] != standing_boundary_identity
        )
    ):
        raise ValueError(
            "occurrence position Measurement requires exact current Locality Standing"
        )
    identities = {
        "assignment_identity": new_identity(
            "occurrence_position_measurement_assignment"
        ),
        "assignment_subject_identity": new_identity(
            "occurrence_position_measurement_assignment_subject"
        ),
        "measurement_act_identity": new_identity(
            "occurrence_position_measurement_act"
        ),
        "act_occurrence_identity": new_identity(
            "occurrence_position_measurement_occurrence"
        ),
        "measurement_result_identity": new_identity(
            "occurrence_position_measurement_result"
        ),
    }
    if len(set(identities.values())) != len(identities):
        raise ValueError("occurrence position Measurement identities collapsed")
    return ledger.append(
        OCCURRENCE_POSITION_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND,
        _assignment_material(
            finding,
            standing_boundary_identity=standing_boundary_identity,
            **identities,
        ),
        locality_identity=recording_locality_identity,
    )


def record_occurrence_position_measurement_responsibility_assignment(
    ledger: EventLedger,
    *,
    recording_locality_identity: str,
    finding: OccurrencePositionFinding,
    locality_standing: dict[str, Any],
) -> Event:
    """Record one exact Book-backed Responsibility assignment occurrence."""

    return _record_occurrence_position_measurement_responsibility_assignment(
        ledger,
        recording_locality_identity=recording_locality_identity,
        finding=finding,
        locality_standing=locality_standing,
        carried=False,
    )


def _record_occurrence_position_measurement_responsibility_assignment_from_carried_standing(
    ledger: EventLedger,
    *,
    recording_locality_identity: str,
    finding: OccurrencePositionFinding,
    locality_standing: dict[str, Any],
) -> Event:
    """Assign a finding produced beside the exact carried Standing at the tip."""

    return _record_occurrence_position_measurement_responsibility_assignment(
        ledger,
        recording_locality_identity=recording_locality_identity,
        finding=finding,
        locality_standing=locality_standing,
        carried=True,
    )


def _read_occurrence_position_measurement_responsibility_assignment(
    ledger: EventLedger,
    assignment_event_identity: str,
) -> tuple[Event, OccurrencePositionFinding]:
    if type(assignment_event_identity) is not str or not assignment_event_identity:
        raise ValueError(
            "occurrence position Measurement requires one assignment occurrence"
        )
    assignment = ledger.get(assignment_event_identity)
    if (
        assignment is None
        or assignment.kind
        != OCCURRENCE_POSITION_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND
        or type(assignment.locality_identity) is not str
        or not assignment.locality_identity
        or assignment.exact_material is not None
        or ledger.integrity_of(assignment.identity) == CORRUPTED
    ):
        raise ValueError(
            "occurrence position Measurement assignment is absent or corrupted"
        )
    material = assignment.material
    identities = {
        coordinate: material.get(coordinate)
        for coordinate in (
            "assignment_identity",
            "assignment_subject_identity",
            "measurement_act_identity",
            "act_occurrence_identity",
            "measurement_result_identity",
        )
    }
    source_locality_identity = material.get("source_locality_identity")
    completeness_boundary_identity = material.get(
        "completeness_boundary_identity"
    )
    standing_boundary_identity = material.get("standing_boundary_identity")
    if (
        any(type(value) is not str or not value for value in identities.values())
        or len(set(identities.values())) != len(identities)
        or type(source_locality_identity) is not str
        or not source_locality_identity
        or type(completeness_boundary_identity) is not str
        or not completeness_boundary_identity
        or (
            standing_boundary_identity is not None
            and (
                type(standing_boundary_identity) is not str
                or not standing_boundary_identity
            )
        )
    ):
        raise ValueError(
            "occurrence position Measurement assignment coordinates are not exact"
        )
    try:
        finding = _measure_occurrence_position_through(
            ledger,
            source_locality_identity=source_locality_identity,
            boundary=EventLedgerBoundary(completeness_boundary_identity),
        )
    except (TypeError, ValueError) as error:
        raise ValueError(
            "occurrence position Measurement assignment coordinates are not exact"
        ) from error
    if material != _assignment_material(
        finding,
        standing_boundary_identity=standing_boundary_identity,
        **identities,
    ):
        raise ValueError(
            "occurrence position Measurement assignment coordinates are not exact"
        )
    if standing_boundary_identity is not None:
        boundary = ledger.get(standing_boundary_identity)
        if (
            boundary is None
            or boundary.locality_identity != assignment.locality_identity
            or ledger.integrity_of(boundary.identity) == CORRUPTED
        ):
            raise ValueError(
                "occurrence position Measurement assignment has no exact Standing boundary"
            )
        try:
            ledger.occurrences_in_append_order(
                (standing_boundary_identity, assignment.identity),
                locality_identity=assignment.locality_identity,
            )
        except ValueError as error:
            raise ValueError(
                "occurrence position Measurement assignment has false occurrence order"
            ) from error
    return assignment, finding


def get_occurrence_position_measurement_responsibility_assignment(
    ledger: EventLedger,
    assignment_event_identity: str,
) -> Event:
    """Read one intact occurrence-position Responsibility assignment."""

    assignment, _finding = (
        _read_occurrence_position_measurement_responsibility_assignment(
            ledger, assignment_event_identity
        )
    )
    return assignment


def _record_occurrence_position_measurement_responsible_act_evidence(
    ledger: EventLedger,
    *,
    responsibility_assignment_event_identity: str,
    responsibility_assignment_standing: dict[str, Any],
    carried: bool,
) -> Event:
    assignment, finding = (
        _read_occurrence_position_measurement_responsibility_assignment(
            ledger, responsibility_assignment_event_identity
        )
    )
    require_standing = (
        _require_carried_locality_standing_at_tip
        if carried
        else _require_current_locality_standing
    )
    require_standing(
        ledger,
        locality_identity=assignment.locality_identity,
        locality_standing=responsibility_assignment_standing,
        required_assignment_identity=assignment.identity,
    )
    for prior_act in ledger.iter_locality_kind(
        assignment.locality_identity,
        OCCURRENCE_POSITION_ACT_EVIDENCE_KIND,
    ):
        if (
            prior_act.material.get("responsibility_assignment_reference")
            == _assignment_reference(assignment)
            or prior_act.material.get("act_occurrence_identity")
            == assignment.material["act_occurrence_identity"]
        ):
            raise ValueError(
                "the occurrence position Responsibility assignment already carries an Act"
            )
    participation = _occurrence_position_participation(
        finding,
        act_occurrence_identity=assignment.material["act_occurrence_identity"],
    )
    return ledger.append(
        OCCURRENCE_POSITION_ACT_EVIDENCE_KIND,
        _occurrence_position_act_evidence_material(
            finding,
            assignment=assignment,
            participation=participation,
        ),
        locality_identity=assignment.locality_identity,
    )


def record_occurrence_position_measurement_responsible_act_evidence(
    ledger: EventLedger,
    *,
    responsibility_assignment_event_identity: str,
    responsibility_assignment_standing: dict[str, Any],
) -> Event:
    """Record the responsible Act Evidence before its Yield and result."""

    return _record_occurrence_position_measurement_responsible_act_evidence(
        ledger,
        responsibility_assignment_event_identity=(
            responsibility_assignment_event_identity
        ),
        responsibility_assignment_standing=responsibility_assignment_standing,
        carried=False,
    )


def _require_carried_occurrence_position_assignment(
    ledger: EventLedger,
    *,
    responsibility_assignment: Event,
    finding: OccurrencePositionFinding,
) -> None:
    if (
        type(responsibility_assignment) is not Event
        or type(finding) is not OccurrencePositionFinding
        or responsibility_assignment.kind
        != OCCURRENCE_POSITION_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND
        or responsibility_assignment.exact_material is not None
        or responsibility_assignment.locality_identity
        != finding.source_locality_identity
        or ledger.integrity_of(responsibility_assignment.identity) == CORRUPTED
    ):
        raise ValueError(
            "occurrence position Measurement requires its exact carried assignment"
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
            "occurrence position Measurement requires its exact carried assignment"
        )


def _record_occurrence_position_measurement_responsible_act_evidence_from_carried_standing(
    ledger: EventLedger,
    *,
    responsibility_assignment: Event,
    finding: OccurrencePositionFinding,
    responsibility_assignment_standing: dict[str, Any],
) -> Event:
    """Record the Act beside its just-carried exact assignment occurrence."""

    _require_carried_occurrence_position_assignment(
        ledger,
        responsibility_assignment=responsibility_assignment,
        finding=finding,
    )
    _require_carried_locality_standing_at_tip(
        ledger,
        locality_identity=responsibility_assignment.locality_identity,
        locality_standing=responsibility_assignment_standing,
        required_assignment_identity=responsibility_assignment.identity,
    )
    for prior_act in ledger.iter_locality_kind(
        responsibility_assignment.locality_identity,
        OCCURRENCE_POSITION_ACT_EVIDENCE_KIND,
    ):
        if (
            prior_act.material.get("responsibility_assignment_reference")
            == _assignment_reference(responsibility_assignment)
            or prior_act.material.get("act_occurrence_identity")
            == responsibility_assignment.material["act_occurrence_identity"]
        ):
            raise ValueError(
                "the occurrence position Responsibility assignment already carries an Act"
            )
    participation = _occurrence_position_participation(
        finding,
        act_occurrence_identity=responsibility_assignment.material[
            "act_occurrence_identity"
        ],
    )
    return ledger.append(
        OCCURRENCE_POSITION_ACT_EVIDENCE_KIND,
        _occurrence_position_act_evidence_material(
            finding,
            assignment=responsibility_assignment,
            participation=participation,
        ),
        locality_identity=responsibility_assignment.locality_identity,
    )


def _read_occurrence_position_measurement_act_evidence(
    ledger: EventLedger,
    act_evidence_event_identity: str,
) -> tuple[Event, Event, OccurrencePositionFinding]:
    if type(act_evidence_event_identity) is not str or not act_evidence_event_identity:
        raise ValueError(
            "occurrence position result requires one exact Act Evidence identity"
        )
    act_evidence = ledger.get(act_evidence_event_identity)
    if (
        act_evidence is None
        or act_evidence.kind != OCCURRENCE_POSITION_ACT_EVIDENCE_KIND
        or type(act_evidence.locality_identity) is not str
        or not act_evidence.locality_identity
        or act_evidence.exact_material is not None
        or ledger.integrity_of(act_evidence.identity) == CORRUPTED
    ):
        raise ValueError(
            "occurrence position result requires its exact intact Act Evidence"
        )
    reference = act_evidence.material.get("responsibility_assignment_reference")
    if type(reference) is not dict:
        raise ValueError(
            "occurrence position result requires its exact intact Act Evidence"
        )
    try:
        assignment, finding = (
            _read_occurrence_position_measurement_responsibility_assignment(
                ledger, reference.get("recorded_occurrence_identity")
            )
        )
    except (TypeError, ValueError) as error:
        raise ValueError(
            "occurrence position result requires its exact intact Act Evidence"
        ) from error
    participation = _occurrence_position_participation(
        finding,
        act_occurrence_identity=assignment.material["act_occurrence_identity"],
    )
    if (
        assignment.locality_identity != act_evidence.locality_identity
        or reference != _assignment_reference(assignment)
        or act_evidence.material
        != _occurrence_position_act_evidence_material(
            finding,
            assignment=assignment,
            participation=participation,
        )
    ):
        raise ValueError(
            "occurrence position result requires its exact intact Act Evidence"
        )
    try:
        ledger.occurrences_in_append_order(
            (assignment.identity, act_evidence.identity),
            locality_identity=act_evidence.locality_identity,
        )
    except ValueError as error:
        raise ValueError(
            "occurrence position Act Evidence requires its prior assignment"
        ) from error
    return act_evidence, assignment, finding


def _refuse_existing_occurrence_position_measurement_result(
    ledger: EventLedger,
    *,
    act_evidence: Event,
    act_occurrence_identity: str,
) -> None:
    for prior_yield in ledger.iter_locality_kind(
        act_evidence.locality_identity,
        RECORDED_EVIDENCE_OF_YIELD_RELATION_KIND,
    ):
        dimensions = prior_yield.material.get("dimensions")
        if (
            prior_yield.material.get("responsible_act_evidence_identity")
            == act_evidence.identity
            or (
                type(dimensions) is dict
                and dimensions.get("act_occurrence_identity")
                == act_occurrence_identity
            )
        ):
            raise ValueError(
                "the occurrence position Measurement Act already carries a Yield"
            )
    for prior_result in ledger.iter_locality_kind(
        act_evidence.locality_identity,
        OCCURRENCE_POSITION_RECORDED_KIND,
    ):
        if (
            prior_result.material.get("responsible_act_evidence_identity")
            == act_evidence.identity
            or prior_result.material.get("act_occurrence_identity")
            == act_occurrence_identity
        ):
            raise ValueError(
                "the occurrence position Measurement Act already carries a result"
            )


def _record_occurrence_position_measurement_result(
    ledger: EventLedger,
    *,
    act_evidence: Event,
    assignment: Event,
    finding: OccurrencePositionFinding,
) -> Event:
    act_occurrence_identity = assignment.material["act_occurrence_identity"]

    assertions = _position_assertions(finding)
    result_material = _occurrence_position_result_material(
        finding,
        assignment=assignment,
        assertions=assertions,
    )
    evidence_of_yield_relation = _record_evidence_of_yield_relation(
        ledger,
        locality_identity=act_evidence.locality_identity,
        exact_act=OCCURRENCE_POSITION_ACT,
        act_occurrence_identity=act_occurrence_identity,
        responsible_act_evidence_identity=act_evidence.identity,
        result_kind=OCCURRENCE_POSITION_RESULT_KIND,
        result_identity=result_material["result_identity"],
        result_content=result_material,
        responsibility=OCCURRENCE_POSITION_RESPONSIBILITY,
        occurrence_boundary="occurrence_position_measurement",
        responsible_boundary="this Seed",
    )
    recorded_material = {
        "result_identity": result_material["result_identity"],
        "addressed_act_identity": result_material["addressed_act_identity"],
        "act_occurrence_identity": result_material["act_occurrence_identity"],
        "exact_act": result_material["exact_act"],
        "responsibility": result_material["responsibility"],
        "responsible_boundary": result_material["responsible_boundary"],
        "responsibility_assignment_evidence": result_material[
            "responsibility_assignment_evidence"
        ],
        "responsibility_assignment_reference": result_material[
            "responsibility_assignment_reference"
        ],
        "measurement_rule": result_material["measurement_rule"],
        "source_localities": result_material["source_localities"],
        "completeness_boundary": result_material["completeness_boundary"],
        "assertions": result_material["assertions"],
        "responsible_act_evidence_identity": act_evidence.identity,
        "evidence_of_yield_relation_identity": evidence_of_yield_relation.identity,
    }
    return ledger.append(
        OCCURRENCE_POSITION_RECORDED_KIND,
        recorded_material,
        locality_identity=act_evidence.locality_identity,
    )


def record_occurrence_position_measurement_result(
    ledger: EventLedger,
    *,
    responsible_act_evidence_event_identity: str,
) -> Event:
    """Record the Yield and result of one exact evidenced Measurement Act."""

    act_evidence, assignment, finding = (
        _read_occurrence_position_measurement_act_evidence(
            ledger, responsible_act_evidence_event_identity
        )
    )
    _refuse_existing_occurrence_position_measurement_result(
        ledger,
        act_evidence=act_evidence,
        act_occurrence_identity=assignment.material["act_occurrence_identity"],
    )
    return _record_occurrence_position_measurement_result(
        ledger,
        act_evidence=act_evidence,
        assignment=assignment,
        finding=finding,
    )


def _record_occurrence_position_measurement_result_from_carried_act_evidence(
    ledger: EventLedger,
    *,
    responsible_act_evidence: Event,
    responsibility_assignment: Event,
    finding: OccurrencePositionFinding,
) -> Event:
    """Record the result beside its just-produced exact Act Evidence."""

    _require_carried_occurrence_position_assignment(
        ledger,
        responsibility_assignment=responsibility_assignment,
        finding=finding,
    )
    participation = _occurrence_position_participation(
        finding,
        act_occurrence_identity=responsibility_assignment.material[
            "act_occurrence_identity"
        ],
    )
    if (
        type(responsible_act_evidence) is not Event
        or responsible_act_evidence.kind != OCCURRENCE_POSITION_ACT_EVIDENCE_KIND
        or responsible_act_evidence.exact_material is not None
        or responsible_act_evidence.locality_identity
        != responsibility_assignment.locality_identity
        or ledger.integrity_of(responsible_act_evidence.identity) == CORRUPTED
        or responsible_act_evidence.material
        != _occurrence_position_act_evidence_material(
            finding,
            assignment=responsibility_assignment,
            participation=participation,
        )
        or ledger.append_boundary_through_occurrence(
            responsible_act_evidence.identity
        )
        != ledger.append_boundary()
    ):
        raise ValueError(
            "occurrence position result requires its exact intact Act Evidence"
        )
    return _record_occurrence_position_measurement_result(
        ledger,
        act_evidence=responsible_act_evidence,
        assignment=responsibility_assignment,
        finding=finding,
    )


def get_recorded_occurrence_position_measurement(
    ledger: EventLedger,
    event_identity: str,
) -> OccurrencePositionFinding:
    """Read one recorded occurrence-position Measurement through its Evidence."""

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
        "responsible_act_evidence_identity",
        "evidence_of_yield_relation_identity",
    }:
        raise ValueError(
            "the occurrence position Measurement carries malformed coordinates"
        )
    source_localities = material.get("source_localities")
    boundary = material.get("completeness_boundary")
    if (
        material.get("exact_act") != OCCURRENCE_POSITION_ACT
        or material.get("responsibility") != OCCURRENCE_POSITION_RESPONSIBILITY
        or material.get("responsible_boundary") != "this Seed"
        or material.get("measurement_rule")
        != OCCURRENCE_POSITION_MEASUREMENT_RULE
        or type(source_localities) is not list
        or len(source_localities) != 1
        or type(source_localities[0]) is not str
        or not source_localities[0]
        or type(boundary) is not dict
        or set(boundary) != {"identity"}
        or type(boundary["identity"]) is not str
        or not boundary["identity"]
        or type(material.get("assertions")) is not list
        or type(material.get("result_identity")) is not str
        or not material["result_identity"]
        or type(material.get("addressed_act_identity")) is not str
        or not material["addressed_act_identity"]
        or type(material.get("act_occurrence_identity")) is not str
        or not material["act_occurrence_identity"]
        or material["addressed_act_identity"]
        == material["act_occurrence_identity"]
    ):
        raise ValueError(
            "the occurrence position Measurement carries malformed coordinates"
        )
    try:
        finding = _measure_occurrence_position_through(
            ledger,
            source_locality_identity=source_localities[0],
            boundary=EventLedgerBoundary(boundary["identity"]),
        )
    except (TypeError, ValueError) as error:
        raise ValueError(
            "the occurrence position Measurement carries malformed coordinates"
        ) from error
    assertions = _position_assertions(finding)
    if material["assertions"] != assertions:
        raise ValueError(
            "the occurrence position Measurement carries malformed Assertions"
        )

    evidence_of_yield_relation_identity = material.get(
        "evidence_of_yield_relation_identity"
    )
    try:
        act_evidence, assignment, assigned_finding = (
            _read_occurrence_position_measurement_act_evidence(
                ledger, material.get("responsible_act_evidence_identity")
            )
        )
    except (TypeError, ValueError) as error:
        raise ValueError(
            "the occurrence position Measurement carries no exact Act Evidence"
        ) from error
    if (
        act_evidence.locality_identity != event.locality_identity
        or assigned_finding != finding
        or material.get("responsibility_assignment_reference")
        != _assignment_reference(assignment)
    ):
        raise ValueError(
            "the occurrence position Measurement carries no exact Act Evidence"
        )
    result_material = _occurrence_position_result_material(
        assigned_finding,
        assignment=assignment,
        assertions=assertions,
    )
    requirements = read_requirements_of_yield_relation(
        ledger,
        recorded_result_event_identity=event.identity,
        evidence_of_yield_relation_event_identity=(
            evidence_of_yield_relation_identity
            if isinstance(evidence_of_yield_relation_identity, str)
            else None
        ),
        responsible_act_evidence_event_identity=act_evidence.identity,
    )
    if not all(requirements.values()):
        raise ValueError(
            "the occurrence position Measurement carries no exact Evidence of Yield relation"
        )
    carried = {
        key: value
        for key, value in material.items()
        if key
        not in {
            "responsible_act_evidence_identity",
            "evidence_of_yield_relation_identity",
        }
    }
    if carried != result_material:
        raise ValueError(
            "the occurrence position Measurement result differs from its coordinates"
        )
    return finding
