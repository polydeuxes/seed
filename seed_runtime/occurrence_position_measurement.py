from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from seed_runtime.event import Event
from seed_runtime.events import CORRUPTED, EventLedger, EventLedgerBoundary
from seed_runtime.identities import new_identity
from seed_runtime.yield_evidence import (
    _record_yield_evidence,
    read_yield_relation_requirements,
)

OCCURRENCE_POSITION_RECORDED_KIND = (
    "operator.measurement.locality_occurrence_position_recorded"
)
OCCURRENCE_POSITION_ACT_EVIDENCE_KIND = (
    "operator.measurement.locality_occurrence_position_act_evidenced"
)
OCCURRENCE_POSITION_RESULT_KIND = "occurrence position Measurement result"
OCCURRENCE_POSITION_ACT = "occurrence position Measurement"
OCCURRENCE_POSITION_RESPONSIBILITY = (
    "establish each occurrence position within one exact Locality and boundary"
)
OCCURRENCE_POSITION_AUTHORITY = "bounded repository authority"
EVENT_KIND_RESPONSIBILITIES = {
    OCCURRENCE_POSITION_RECORDED_KIND: "02.Acts.A",
    OCCURRENCE_POSITION_ACT_EVIDENCE_KIND: "02.Acts.A",
}


class OccurrencePositionMeasurementError(Exception):
    pass


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
            raise OccurrencePositionMeasurementError(
                "one exact source Locality is required"
            )
        if not isinstance(self.completeness_boundary, EventLedgerBoundary):
            raise OccurrencePositionMeasurementError(
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
                raise OccurrencePositionMeasurementError(
                    "each exact occurrence requires its measured position"
                )
            identities.append(occurrence[0])
        if len(set(identities)) != len(identities):
            raise OccurrencePositionMeasurementError(
                "one occurrence cannot occupy more than one measured position"
            )

    def to_json_dict(self) -> dict[str, Any]:
        return {
            "source_locality_identity": self.source_locality_identity,
            "completeness_boundary": {
                "identity": self.completeness_boundary.identity,
            },
            "occurrences": [
                {"identity": identity, "position": position}
                for identity, position in self.occurrences
            ],
        }


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
        raise OccurrencePositionMeasurementError(
            "one exact source Locality is required"
        )
    boundary = through or ledger.append_boundary()
    occurrences = ledger.list_locality(
        source_locality_identity,
        through=boundary,
    )
    if any(ledger.integrity_of(event.identity) == CORRUPTED for event in occurrences):
        raise OccurrencePositionMeasurementError(
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
    result_identity: str,
    act_identity: str,
    act_occurrence_identity: str,
) -> dict[str, Any]:
    assignment = {
        "standing": "assigned",
        "responsibility": OCCURRENCE_POSITION_RESPONSIBILITY,
        "responsible_boundary": "this Seed",
        "completeness_boundary": finding.completeness_boundary.identity,
    }
    participation = [
        {
            "subject_reference": identity,
            "role": "exact occurrence",
            "act_occurrence_identity": act_occurrence_identity,
        }
        for identity, _position in finding.occurrences
    ]
    return {
        "result_identity": result_identity,
        "downstream_act_identity": act_identity,
        "act_occurrence_identity": act_occurrence_identity,
        "exact_act": OCCURRENCE_POSITION_ACT,
        "responsibility": OCCURRENCE_POSITION_RESPONSIBILITY,
        "responsible_boundary": "this Seed",
        "responsibility_assignment_evidence": assignment,
        "authority": OCCURRENCE_POSITION_AUTHORITY,
        "participation": participation,
        **finding.to_json_dict(),
        "limits": [
            "occurrence position does not establish causation or another relation",
        ],
    }


def record_occurrence_position_measurement(
    ledger: EventLedger,
    *,
    recording_locality_identity: str,
    finding: OccurrencePositionFinding,
) -> Event:
    """Record one exact occurrence-position Measurement and its Yield."""

    exact = measure_occurrence_position(
        ledger,
        source_locality_identity=finding.source_locality_identity,
        through=finding.completeness_boundary,
    )
    if finding != exact:
        raise OccurrencePositionMeasurementError(
            "the supplied occurrence position finding differs from the exact boundary"
        )

    act_identity = new_identity("occurrence_position_measurement_act")
    act_occurrence_identity = new_identity(
        "occurrence_position_measurement_occurrence"
    )
    result_identity = new_identity("occurrence_position_measurement_result")
    result_material = _occurrence_position_result_material(
        finding,
        result_identity=result_identity,
        act_identity=act_identity,
        act_occurrence_identity=act_occurrence_identity,
    )
    act_evidence = ledger.append(
        OCCURRENCE_POSITION_ACT_EVIDENCE_KIND,
        {
            "downstream_act_identity": act_identity,
            "act_occurrence_identity": act_occurrence_identity,
            "act": OCCURRENCE_POSITION_ACT,
            "responsibility": OCCURRENCE_POSITION_RESPONSIBILITY,
            "responsible_boundary": "this Seed",
            "responsibility_assignment_evidence": result_material[
                "responsibility_assignment_evidence"
            ],
            "authority": OCCURRENCE_POSITION_AUTHORITY,
            "evidence_scope": (
                "Evidence for this exact occurrence position Measurement "
                "occurrence and result"
            ),
            "participation": result_material["participation"],
        },
        locality_identity=recording_locality_identity,
    )
    yield_evidence = _record_yield_evidence(
        ledger,
        locality_identity=recording_locality_identity,
        exact_act=OCCURRENCE_POSITION_ACT,
        act_occurrence_identity=act_occurrence_identity,
        responsible_act_evidence_identity=act_evidence.identity,
        result_kind=OCCURRENCE_POSITION_RESULT_KIND,
        result_identity=result_identity,
        result_content=result_material,
        responsibility=OCCURRENCE_POSITION_RESPONSIBILITY,
        live_boundary="occurrence_position_measurement",
        responsible_boundary="this Seed",
    )
    recorded_material = {
        "result_identity": result_material["result_identity"],
        "downstream_act_identity": result_material["downstream_act_identity"],
        "act_occurrence_identity": result_material["act_occurrence_identity"],
        "exact_act": result_material["exact_act"],
        "responsibility": result_material["responsibility"],
        "responsible_boundary": result_material["responsible_boundary"],
        "responsibility_assignment_evidence": result_material[
            "responsibility_assignment_evidence"
        ],
        "authority": result_material["authority"],
        "participation": result_material["participation"],
        "source_locality_identity": result_material["source_locality_identity"],
        "completeness_boundary": result_material["completeness_boundary"],
        "occurrences": result_material["occurrences"],
        "limits": result_material["limits"],
        "responsible_act_evidence_identity": act_evidence.identity,
        "yield_evidence_identity": yield_evidence.identity,
    }
    return ledger.append(
        OCCURRENCE_POSITION_RECORDED_KIND,
        recorded_material,
        locality_identity=recording_locality_identity,
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
        raise OccurrencePositionMeasurementError(
            "the occurrence position Measurement result is absent or corrupted"
        )
    material = event.material
    source_locality_identity = material.get("source_locality_identity")
    boundary = material.get("completeness_boundary")
    occurrences = material.get("occurrences")
    if (
        not isinstance(source_locality_identity, str)
        or not source_locality_identity
        or type(boundary) is not dict
        or set(boundary) != {"identity"}
        or not isinstance(boundary["identity"], str)
        or type(occurrences) is not list
    ):
        raise OccurrencePositionMeasurementError(
            "the occurrence position Measurement carries malformed coordinates"
        )
    try:
        finding = OccurrencePositionFinding(
            source_locality_identity=source_locality_identity,
            completeness_boundary=EventLedgerBoundary(boundary["identity"]),
            occurrences=tuple(
                (item["identity"], item["position"])
                for item in occurrences
                if type(item) is dict and set(item) == {"identity", "position"}
            ),
        )
    except (KeyError, TypeError, OccurrencePositionMeasurementError) as error:
        raise OccurrencePositionMeasurementError(
            "the occurrence position Measurement carries malformed occurrences"
        ) from error
    if len(finding.occurrences) != len(occurrences):
        raise OccurrencePositionMeasurementError(
            "the occurrence position Measurement carries malformed occurrences"
        )

    act_evidence_identity = material.get("responsible_act_evidence_identity")
    yield_evidence_identity = material.get("yield_evidence_identity")
    act_evidence = (
        ledger.get(act_evidence_identity)
        if isinstance(act_evidence_identity, str)
        else None
    )
    result_material = _occurrence_position_result_material(
        finding,
        result_identity=material.get("result_identity"),
        act_identity=material.get("downstream_act_identity"),
        act_occurrence_identity=material.get("act_occurrence_identity"),
    )
    expected_act_evidence = {
        "downstream_act_identity": material.get("downstream_act_identity"),
        "act_occurrence_identity": material.get("act_occurrence_identity"),
        "act": OCCURRENCE_POSITION_ACT,
        "responsibility": OCCURRENCE_POSITION_RESPONSIBILITY,
        "responsible_boundary": "this Seed",
        "responsibility_assignment_evidence": result_material[
            "responsibility_assignment_evidence"
        ],
        "authority": OCCURRENCE_POSITION_AUTHORITY,
        "evidence_scope": (
            "Evidence for this exact occurrence position Measurement occurrence "
            "and result"
        ),
        "participation": result_material["participation"],
    }
    if (
        act_evidence is None
        or act_evidence.kind != OCCURRENCE_POSITION_ACT_EVIDENCE_KIND
        or act_evidence.locality_identity != event.locality_identity
        or ledger.integrity_of(act_evidence.identity) == CORRUPTED
        or act_evidence.material != expected_act_evidence
    ):
        raise OccurrencePositionMeasurementError(
            "the occurrence position Measurement carries no exact Act Evidence"
        )
    requirements = read_yield_relation_requirements(
        ledger,
        recorded_result_event_identity=event.identity,
        result_evidence_event_identity=(
            yield_evidence_identity
            if isinstance(yield_evidence_identity, str)
            else None
        ),
        responsible_act_evidence_event_identity=act_evidence.identity,
    )
    if not all(requirements.values()):
        raise OccurrencePositionMeasurementError(
            "the occurrence position Measurement carries no exact Yield Evidence"
        )
    carried = {
        key: value
        for key, value in material.items()
        if key
        not in {
            "responsible_act_evidence_identity",
            "yield_evidence_identity",
        }
    }
    if carried != result_material:
        raise OccurrencePositionMeasurementError(
            "the occurrence position Measurement result differs from its coordinates"
        )
    exact = measure_occurrence_position(
        ledger,
        source_locality_identity=finding.source_locality_identity,
        through=finding.completeness_boundary,
    )
    if finding != exact:
        raise OccurrencePositionMeasurementError(
            "the occurrence position Measurement differs from its exact boundary"
        )
    return finding
