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
OCCURRENCE_POSITION_ACT_EVIDENCE_KIND = (
    "operator.measurement.locality_occurrence_position_act_evidenced"
)
OCCURRENCE_POSITION_RESULT_KIND = "occurrence position Measurement result"
OCCURRENCE_POSITION_ACT = "occurrence position Measurement"
OCCURRENCE_POSITION_RESPONSIBILITY = (
    "establish each occurrence position within one exact Locality and boundary"
)
OCCURRENCE_POSITION_MEASUREMENT_RULE = (
    "each exact occurrence in one exact Locality; position equal to its order "
    "through one completeness boundary"
)
OCCURRENCE_POSITION_AUTHORITY = "bounded repository authority"
MEASURED_ASSERTION_RESPONSIBILITY = (
    "preserve Standing coordinates carried by this measured Assertion"
)
OCCURRENCE_POSITION_RESULT_COORDINATES = frozenset(
    {
        "result_identity",
        "downstream_act_identity",
        "act_occurrence_identity",
        "exact_act",
        "responsibility",
        "responsible_boundary",
        "responsibility_assignment_evidence",
        "measurement_rule",
        "source_localities",
        "completeness_boundary",
        "assertions",
    }
)
EVENT_KIND_RESPONSIBILITIES = {
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
    result_identity: str,
    act_identity: str,
    act_occurrence_identity: str,
    assertions: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "result_identity": result_identity,
        "downstream_act_identity": act_identity,
        "act_occurrence_identity": act_occurrence_identity,
        "exact_act": OCCURRENCE_POSITION_ACT,
        "responsibility": OCCURRENCE_POSITION_RESPONSIBILITY,
        "responsible_boundary": "this Seed",
        "responsibility_assignment_evidence": _responsibility_assignment(finding),
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
        "standing": "assigned",
        "responsible_boundary": "this Seed",
        "source_occurrence_references": [
            {"occurrence_identity": identity}
            for identity, _position in finding.occurrences
        ],
        "completeness_boundary": finding.completeness_boundary.identity,
        "determination": OCCURRENCE_POSITION_MEASUREMENT_RULE,
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
                    "standing": "measured",
                    "source_provenance": (
                        "complete exact Locality through one boundary"
                    ),
                    "responsibility": MEASURED_ASSERTION_RESPONSIBILITY,
                    "authority": "unestablished",
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
                    "what this occurrence participates in or represents remains Unknown"
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
    act_identity: str,
    act_occurrence_identity: str,
    participation: list[dict[str, str]],
) -> dict[str, Any]:
    return {
        "downstream_act_identity": act_identity,
        "act_occurrence_identity": act_occurrence_identity,
        "act": OCCURRENCE_POSITION_ACT,
        "responsibility": OCCURRENCE_POSITION_RESPONSIBILITY,
        "responsible_boundary": "this Seed",
        "responsibility_assignment_evidence": _responsibility_assignment(finding),
        "authority": OCCURRENCE_POSITION_AUTHORITY,
        "evidence_scope": (
            "Evidence bounded to this exact occurrence position Measurement "
            "occurrence"
        ),
        "source_locality_identity": finding.source_locality_identity,
        "participation": participation,
    }


def record_occurrence_position_measurement_responsible_act_evidence(
    ledger: EventLedger,
    *,
    recording_locality_identity: str,
    finding: OccurrencePositionFinding,
) -> Event:
    """Record the responsible Act Evidence before its Yield and result."""

    if type(recording_locality_identity) is not str or not recording_locality_identity:
        raise ValueError("occurrence position recording requires one exact Locality")
    _exact_occurrence_position_finding(ledger, finding)

    act_identity = new_identity("occurrence_position_measurement_act")
    act_occurrence_identity = new_identity(
        "occurrence_position_measurement_occurrence"
    )
    participation = _occurrence_position_participation(
        finding,
        act_occurrence_identity=act_occurrence_identity,
    )
    return ledger.append(
        OCCURRENCE_POSITION_ACT_EVIDENCE_KIND,
        _occurrence_position_act_evidence_material(
            finding,
            act_identity=act_identity,
            act_occurrence_identity=act_occurrence_identity,
            participation=participation,
        ),
        locality_identity=recording_locality_identity,
    )


def record_occurrence_position_measurement_result(
    ledger: EventLedger,
    *,
    finding: OccurrencePositionFinding,
    responsible_act_evidence_event_identity: str,
) -> Event:
    """Record the Yield and result of one exact evidenced Measurement Act."""

    if (
        type(responsible_act_evidence_event_identity) is not str
        or not responsible_act_evidence_event_identity
    ):
        raise ValueError(
            "occurrence position result requires one exact Act Evidence identity"
        )
    if type(finding) is not OccurrencePositionFinding:
        raise TypeError(
            "occurrence position result requires the exact finding of its Act"
        )
    act_evidence = ledger.get(responsible_act_evidence_event_identity)
    if (
        act_evidence is None
        or act_evidence.kind != OCCURRENCE_POSITION_ACT_EVIDENCE_KIND
        or type(act_evidence.locality_identity) is not str
        or not act_evidence.locality_identity
        or ledger.integrity_of(act_evidence.identity) == CORRUPTED
    ):
        raise ValueError(
            "occurrence position result requires its exact intact Act Evidence"
        )
    act_identity = act_evidence.material.get("downstream_act_identity")
    act_occurrence_identity = act_evidence.material.get("act_occurrence_identity")
    if (
        type(act_identity) is not str
        or not act_identity
        or type(act_occurrence_identity) is not str
        or not act_occurrence_identity
        or act_identity == act_occurrence_identity
    ):
        raise ValueError(
            "occurrence position result requires its exact intact Act Evidence"
        )
    participation = _occurrence_position_participation(
        finding,
        act_occurrence_identity=act_occurrence_identity,
    )
    if act_evidence.material != _occurrence_position_act_evidence_material(
        finding,
        act_identity=act_identity,
        act_occurrence_identity=act_occurrence_identity,
        participation=participation,
    ):
        raise ValueError(
            "occurrence position result requires its exact intact Act Evidence"
        )
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

    result_identity = new_identity("occurrence_position_measurement_result")
    assertions = _position_assertions(finding)
    result_material = _occurrence_position_result_material(
        finding,
        result_identity=result_identity,
        act_identity=act_identity,
        act_occurrence_identity=act_occurrence_identity,
        assertions=assertions,
    )
    evidence_of_yield_relation = _record_evidence_of_yield_relation(
        ledger,
        locality_identity=act_evidence.locality_identity,
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
        or type(material.get("downstream_act_identity")) is not str
        or not material["downstream_act_identity"]
        or type(material.get("act_occurrence_identity")) is not str
        or not material["act_occurrence_identity"]
        or material["downstream_act_identity"]
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

    act_evidence_identity = material.get("responsible_act_evidence_identity")
    evidence_of_yield_relation_identity = material.get("evidence_of_yield_relation_identity")
    act_evidence = (
        ledger.get(act_evidence_identity)
        if isinstance(act_evidence_identity, str)
        else None
    )
    result_identity = material.get("result_identity")
    act_identity = material.get("downstream_act_identity")
    act_occurrence_identity = material.get("act_occurrence_identity")
    participation = _occurrence_position_participation(
        finding,
        act_occurrence_identity=act_occurrence_identity,
    )
    result_material = _occurrence_position_result_material(
        finding,
        result_identity=result_identity,
        act_identity=act_identity,
        act_occurrence_identity=act_occurrence_identity,
        assertions=assertions,
    )
    expected_act_evidence = _occurrence_position_act_evidence_material(
        finding,
        act_identity=act_identity,
        act_occurrence_identity=act_occurrence_identity,
        participation=participation,
    )
    if (
        act_evidence is None
        or act_evidence.kind != OCCURRENCE_POSITION_ACT_EVIDENCE_KIND
        or act_evidence.locality_identity != event.locality_identity
        or ledger.integrity_of(act_evidence.identity) == CORRUPTED
        or act_evidence.material != expected_act_evidence
    ):
        raise ValueError(
            "the occurrence position Measurement carries no exact Act Evidence"
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
