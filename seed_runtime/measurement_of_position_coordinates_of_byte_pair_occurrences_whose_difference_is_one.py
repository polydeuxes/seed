"""Measure every byte-pair occurrence whose position difference is one.

The exact source Ingest result bounds the population.  The Measurement records
the two byte values and their two position coordinates; it establishes no recurrence,
represented relation, character, word, or meaning.
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


POSITION_DIFFERENCE_ONE_ASSIGNMENT_KIND = (
    "operator.measurement_of_position_coordinates_of_byte_pair_occurrences_whose_"
    "difference_is_one.responsibility_assignment_recorded"
)
POSITION_DIFFERENCE_ONE_ACT_EVIDENCE_KIND = (
    "operator.measurement_of_position_coordinates_of_byte_pair_occurrences_whose_"
    "difference_is_one.evidence_of_act_occurrence_recorded"
)
POSITION_DIFFERENCE_ONE_RESULT_KIND = (
    "operator.measurement_of_position_coordinates_of_byte_pair_occurrences_whose_"
    "difference_is_one.recording_occurrence_of_result"
)
RESULT_KIND = (
    "result of Measurement of position coordinates of byte-pair occurrences whose "
    "difference is one"
)
EXACT_ACT = (
    "Measurement of position coordinates of byte-pair occurrences whose difference is one"
)
RESPONSIBILITY = (
    "Measurement of each exact byte-pair occurrence whose position-coordinate "
    "difference is one within one exact Ingest result"
)
MEASUREMENT_RULE = (
    "each exact byte pair at first position and second position whose difference is one "
    "within one exact Ingest result"
)
AUTHORITY = "bounded repository authority"
ASSERTION_RESPONSIBILITY = (
    "preserve carried Standing coordinates of this measured Assertion"
)

EVENT_KIND_RESPONSIBILITIES = {
    POSITION_DIFFERENCE_ONE_ASSIGNMENT_KIND: "01.Source.D",
    POSITION_DIFFERENCE_ONE_ACT_EVIDENCE_KIND: "02.Acts.A",
    POSITION_DIFFERENCE_ONE_RESULT_KIND: "01.Source.D",
}
ASSERTION_RESPONSIBILITIES = {
    "position of exact byte-pair occurrence whose difference is one": "01.Source.D",
}


class FindingOfPositionCoordinatesOfBytePairOccurrencesWhoseDifferenceIsOne(NamedTuple):
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


class ReferenceToRecordedPositionOfBytePairOccurrenceWhoseDifferenceIsOne(
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


def _validate_finding(
    finding: FindingOfPositionCoordinatesOfBytePairOccurrencesWhoseDifferenceIsOne,
) -> None:
    if type(finding) is not FindingOfPositionCoordinatesOfBytePairOccurrencesWhoseDifferenceIsOne:
        raise TypeError("position-difference Measurement requires one exact finding")
    if (
        type(finding.source_ingest_occurrence_identity) is not str
        or not finding.source_ingest_occurrence_identity
        or type(finding.source_locality_identity) is not str
        or not finding.source_locality_identity
        or type(finding.completeness_boundary) is not EventLedgerBoundary
        or type(finding.exact_material) is not bytes
    ):
        raise ValueError("position-difference finding carries no exact source")


def _measure_through(
    ledger: EventLedger,
    *,
    source_ingest_occurrence_identity: str,
    boundary: EventLedgerBoundary,
) -> FindingOfPositionCoordinatesOfBytePairOccurrencesWhoseDifferenceIsOne:
    source = read_exact_ingest_result(ledger, source_ingest_occurrence_identity)
    exact_boundary = ledger.append_boundary_through_occurrence(source.identity)
    if type(boundary) is not EventLedgerBoundary or boundary != exact_boundary:
        raise ValueError(
            "position-difference Measurement requires the exact source boundary"
        )
    exact = ingested_material_bytes(source)
    finding = FindingOfPositionCoordinatesOfBytePairOccurrencesWhoseDifferenceIsOne(
        source_ingest_occurrence_identity=source.identity,
        source_locality_identity=source.locality_identity,
        completeness_boundary=boundary,
        exact_material=exact,
    )
    _validate_finding(finding)
    return finding


def measure_position_coordinates_of_byte_pair_occurrences_whose_difference_is_one(
    ledger: EventLedger,
    *,
    source_ingest_occurrence_identity: str,
) -> FindingOfPositionCoordinatesOfBytePairOccurrencesWhoseDifferenceIsOne:
    """Measure every exact two-position window in one Ingest result."""

    if not isinstance(ledger, EventLedger):
        raise TypeError("position-difference Measurement requires one EventLedger")
    if (
        type(source_ingest_occurrence_identity) is not str
        or not source_ingest_occurrence_identity
    ):
        raise ValueError("position-difference Measurement requires one Ingest result")
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


def _input_applicability(
    finding: FindingOfPositionCoordinatesOfBytePairOccurrencesWhoseDifferenceIsOne,
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
        "standing": "applicable",
        "through": (
            "one intact exact Ingest result carried by current Locality Standing"
        ),
    }


def _assignment_material(
    finding: FindingOfPositionCoordinatesOfBytePairOccurrencesWhoseDifferenceIsOne,
    *,
    standing_boundary_identity: str,
    assignment_identity: str,
    assignment_subject_identity: str,
    measurement_act_identity: str,
    act_occurrence_identity: str,
    measurement_result_identity: str,
) -> dict[str, Any]:
    applicability = _input_applicability(
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
        "input_applicability": applicability,
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
            "position-difference Measurement requires current Locality Standing"
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
            "position-difference Measurement requires current Locality Standing"
        )
    return boundary


def record_position_difference_one_measurement_responsibility_assignment(
    ledger: EventLedger,
    *,
    source_ingest_occurrence_identity: str,
    locality_standing: dict[str, Any],
) -> Event:
    """Assign the exact source result to this declared Measurement."""

    finding = measure_position_coordinates_of_byte_pair_occurrences_whose_difference_is_one(
        ledger,
        source_ingest_occurrence_identity=source_ingest_occurrence_identity,
    )
    standing_boundary_identity = _require_current_standing(
        ledger,
        locality_identity=finding.source_locality_identity,
        locality_standing=locality_standing,
        source_ingest_occurrence_identity=source_ingest_occurrence_identity,
    )
    identities = {
        "assignment_identity": new_identity(
            "byte_pair_position_difference_one_assignment"
        ),
        "assignment_subject_identity": new_identity(
            "byte_pair_position_difference_one_assignment_subject"
        ),
        "measurement_act_identity": new_identity(
            "byte_pair_position_difference_one_measurement_act"
        ),
        "act_occurrence_identity": new_identity(
            "byte_pair_position_difference_one_measurement_act_occurrence"
        ),
        "measurement_result_identity": new_identity(
            "byte_pair_position_difference_one_measurement_result"
        ),
    }
    if len(set(identities.values())) != len(identities):
        raise ValueError("position-difference Measurement identities collapsed")
    return ledger.append(
        POSITION_DIFFERENCE_ONE_ASSIGNMENT_KIND,
        _assignment_material(
            finding,
            standing_boundary_identity=standing_boundary_identity,
            **identities,
        ),
        locality_identity=finding.source_locality_identity,
    )


def _read_assignment(
    ledger: EventLedger, assignment_event_identity: str
) -> tuple[Event, FindingOfPositionCoordinatesOfBytePairOccurrencesWhoseDifferenceIsOne]:
    assignment = ledger.get(assignment_event_identity)
    if (
        assignment is None
        or assignment.kind != POSITION_DIFFERENCE_ONE_ASSIGNMENT_KIND
        or type(assignment.locality_identity) is not str
        or not assignment.locality_identity
        or assignment.exact_material is not None
        or ledger.integrity_of(assignment.identity) == CORRUPTED
    ):
        raise ValueError("position-difference assignment is absent or corrupted")
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
        raise ValueError("position-difference assignment coordinates are not exact")
    try:
        finding = _measure_through(
            ledger,
            source_ingest_occurrence_identity=source_identity,
            boundary=EventLedgerBoundary(boundary_identity),
        )
    except (TypeError, ValueError) as error:
        raise ValueError(
            "position-difference assignment coordinates are not exact"
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
        raise ValueError("position-difference assignment coordinates are not exact")
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
            "position-difference assignment has no exact prior Standing"
        ) from error
    if not any(
        type(occurrence) is dict
        and occurrence.get("evidence_event_identity") == source_identity
        for occurrence in prior.get("ingest_occurrences", ())
    ):
        raise ValueError(
            "position-difference assignment has no exact prior Standing"
        )
    return assignment, finding


def get_position_difference_one_measurement_responsibility_assignment(
    ledger: EventLedger, assignment_event_identity: str
) -> Event:
    assignment, _finding = _read_assignment(ledger, assignment_event_identity)
    return assignment


def _participation(
    finding: FindingOfPositionCoordinatesOfBytePairOccurrencesWhoseDifferenceIsOne,
    *,
    act_occurrence_identity: str,
) -> dict[str, str]:
    return {
        "subject_reference": finding.source_ingest_occurrence_identity,
        "role": "input",
        "act_occurrence_identity": act_occurrence_identity,
    }


def _act_material(
    finding: FindingOfPositionCoordinatesOfBytePairOccurrencesWhoseDifferenceIsOne,
    assignment: Event,
) -> dict[str, Any]:
    return {
        "downstream_act_identity": assignment.material["measurement_act_identity"],
        "act_occurrence_identity": assignment.material["act_occurrence_identity"],
        "act": EXACT_ACT,
        "responsibility": RESPONSIBILITY,
        "responsible_boundary": "this Seed",
        "responsibility_assignment_reference": _assignment_reference(assignment),
        "input_applicability": assignment.material["input_applicability"],
        "participation": _participation(
            finding,
            act_occurrence_identity=assignment.material["act_occurrence_identity"],
        ),
        "authority": AUTHORITY,
        "evidence_scope": (
            "Evidence bounded to this exact position-difference Measurement occurrence"
        ),
    }


def record_position_difference_one_measurement_act_evidence(
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
        assignment.locality_identity, POSITION_DIFFERENCE_ONE_ACT_EVIDENCE_KIND
    ):
        if (
            prior.material.get("responsibility_assignment_reference")
            == _assignment_reference(assignment)
            or prior.material.get("act_occurrence_identity")
            == assignment.material["act_occurrence_identity"]
        ):
            raise ValueError("position-difference assignment already carries an Act")
    return ledger.append(
        POSITION_DIFFERENCE_ONE_ACT_EVIDENCE_KIND,
        _act_material(finding, assignment),
        locality_identity=assignment.locality_identity,
    )


def _read_act(
    ledger: EventLedger, act_evidence_event_identity: str
) -> tuple[
    Event,
    Event,
    FindingOfPositionCoordinatesOfBytePairOccurrencesWhoseDifferenceIsOne,
]:
    act = ledger.get(act_evidence_event_identity)
    if (
        act is None
        or act.kind != POSITION_DIFFERENCE_ONE_ACT_EVIDENCE_KIND
        or act.exact_material is not None
        or ledger.integrity_of(act.identity) == CORRUPTED
    ):
        raise ValueError("position-difference result requires intact Act Evidence")
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
            "position-difference result requires intact Act Evidence"
        ) from error
    if (
        act.locality_identity != assignment.locality_identity
        or reference != _assignment_reference(assignment)
        or act.material != _act_material(finding, assignment)
    ):
        raise ValueError("position-difference result requires intact Act Evidence")
    try:
        ledger.occurrences_in_append_order(
            (assignment.identity, act.identity),
            locality_identity=assignment.locality_identity,
        )
    except ValueError as error:
        raise ValueError(
            "position-difference Act requires its prior assignment"
        ) from error
    return act, assignment, finding


def get_position_difference_one_measurement_act_evidence(
    ledger: EventLedger, act_evidence_event_identity: str
) -> Event:
    act, _assignment, _finding = _read_act(ledger, act_evidence_event_identity)
    return act


def _canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def _assertion(
    finding: FindingOfPositionCoordinatesOfBytePairOccurrencesWhoseDifferenceIsOne,
    *,
    exact_pair: bytes,
    first_position: int,
    second_position: int,
) -> dict[str, Any]:
    scope = {
        "source_locality_identity": finding.source_locality_identity,
        "source_ingest_occurrence_identity": (
            finding.source_ingest_occurrence_identity
        ),
        "completeness_boundary_identity": finding.completeness_boundary.identity,
    }
    subject = {
        "source_ingest_occurrence_identity": (
            finding.source_ingest_occurrence_identity
        ),
        "exact_pair": list(exact_pair),
        "measurement_rule": MEASUREMENT_RULE,
    }
    content = {
        "first_position": first_position,
        "second_position": second_position,
    }
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
            "standing": "measured",
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
            "two position coordinates bounded by one exact Ingest result and source boundary"
        ],
    }


def _assertion_identity(
    finding: FindingOfPositionCoordinatesOfBytePairOccurrencesWhoseDifferenceIsOne,
    *,
    exact_pair: bytes,
    first_position: int,
    second_position: int,
) -> str:
    identity_material = {
        "result": "position",
        "subject": {
            "source_ingest_occurrence_identity": (
                finding.source_ingest_occurrence_identity
            ),
            "exact_pair": list(exact_pair),
            "measurement_rule": MEASUREMENT_RULE,
        },
        "scope": {
            "source_locality_identity": finding.source_locality_identity,
            "source_ingest_occurrence_identity": (
                finding.source_ingest_occurrence_identity
            ),
            "completeness_boundary_identity": finding.completeness_boundary.identity,
        },
        "content": {
            "first_position": first_position,
            "second_position": second_position,
        },
    }
    return "byte-pair-position-difference-one:" + hashlib.sha256(
        _canonical(identity_material).encode("utf-8")
    ).hexdigest()


def _assertion_population(
    finding: FindingOfPositionCoordinatesOfBytePairOccurrencesWhoseDifferenceIsOne,
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
                "second_position": "difference from first_position is one",
            },
            "responsibility": ASSERTION_RESPONSIBILITY,
            "standing": "measured",
            "authority": "unestablished",
        },
        "unknown": [
            "Participation or representation of each measured byte pair remains Unknown"
        ],
    }


def _result_material(
    finding: FindingOfPositionCoordinatesOfBytePairOccurrencesWhoseDifferenceIsOne,
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
        "input_applicability": assignment.material["input_applicability"],
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


def record_position_difference_one_measurement_result(
    ledger: EventLedger,
    *,
    responsible_act_evidence_event_identity: str,
) -> Event:
    act, assignment, finding = _read_act(
        ledger, responsible_act_evidence_event_identity
    )
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
                == assignment.material["act_occurrence_identity"]
            )
        ):
            raise ValueError("position-difference Act already carries a Yield")
    for prior_result in ledger.iter_locality_kind(
        act.locality_identity, POSITION_DIFFERENCE_ONE_RESULT_KIND
    ):
        if (
            prior_result.material.get("responsible_act_evidence_identity")
            == act.identity
            or prior_result.material.get("act_occurrence_identity")
            == assignment.material["act_occurrence_identity"]
        ):
            raise ValueError("position-difference Act already carries a result")
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
        live_boundary="byte_pair_position_coordinate_difference_one_measurement",
        responsible_boundary="this Seed",
    )
    return ledger.append(
        POSITION_DIFFERENCE_ONE_RESULT_KIND,
        {
            **result,
            "responsible_act_evidence_identity": act.identity,
            "evidence_of_yield_relation_identity": evidence.identity,
        },
        locality_identity=act.locality_identity,
    )


def _read_result(
    ledger: EventLedger, result_event_identity: str
) -> tuple[
    Event,
    FindingOfPositionCoordinatesOfBytePairOccurrencesWhoseDifferenceIsOne,
    dict[str, Any],
]:
    event = ledger.get(result_event_identity)
    if (
        event is None
        or event.kind != POSITION_DIFFERENCE_ONE_RESULT_KIND
        or event.exact_material is not None
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise ValueError("position-difference result is absent or corrupted")
    try:
        act, assignment, finding = _read_act(
            ledger, event.material.get("responsible_act_evidence_identity")
        )
    except (TypeError, ValueError) as error:
        raise ValueError("position-difference result carries no exact Act") from error
    expected = {
        **_result_material(finding, assignment),
        "responsible_act_evidence_identity": act.identity,
        "evidence_of_yield_relation_identity": event.material.get(
            "evidence_of_yield_relation_identity"
        ),
    }
    if event.locality_identity != act.locality_identity or event.material != expected:
        raise ValueError("position-difference result coordinates are not exact")
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
        raise ValueError("position-difference result carries no exact Yield") from error
    if (
        not all(requirements.values())
        or evidence is None
        or evidence.kind != RECORDED_EVIDENCE_OF_YIELD_RELATION_KIND
        or ledger.integrity_of(evidence.identity) == CORRUPTED
    ):
        raise ValueError("position-difference result carries no exact Yield")
    try:
        ordered = ledger.occurrences_in_append_order(
            (act.identity, evidence.identity, event.identity),
            locality_identity=event.locality_identity,
        )
    except ValueError as error:
        raise ValueError("position-difference result has false occurrence order") from error
    if tuple(item.identity for item in ordered) != (
        act.identity,
        evidence.identity,
        event.identity,
    ):
        raise ValueError("position-difference result has false occurrence order")
    return event, finding, expected["assertions"]


def get_recorded_position_difference_one_measurement(
    ledger: EventLedger, result_event_identity: str
) -> FindingOfPositionCoordinatesOfBytePairOccurrencesWhoseDifferenceIsOne:
    _event, finding, _assertions_read = _read_result(ledger, result_event_identity)
    return finding


def _recorded_position_reference(
    event: Event,
    finding: FindingOfPositionCoordinatesOfBytePairOccurrencesWhoseDifferenceIsOne,
    *,
    exact_pair: bytes,
    first_position: int,
    second_position: int,
) -> ReferenceToRecordedPositionOfBytePairOccurrenceWhoseDifferenceIsOne:
    return ReferenceToRecordedPositionOfBytePairOccurrenceWhoseDifferenceIsOne(
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


def _references_to_recorded_position_coordinates_for_assertion_identities(
    ledger: EventLedger,
    result_event_identity: str,
    assertion_identities: tuple[str, ...],
) -> tuple[
    ReferenceToRecordedPositionOfBytePairOccurrenceWhoseDifferenceIsOne, ...
]:
    """Resolve exact addressed Assertions with one bounded result read."""

    if (
        type(assertion_identities) is not tuple
        or not assertion_identities
        or any(type(identity) is not str or not identity for identity in assertion_identities)
        or len(set(assertion_identities)) != len(assertion_identities)
    ):
        raise ValueError("position references require distinct Assertion identities")
    event, finding, _assertion_population_read = _read_result(
        ledger, result_event_identity
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
    if set(resolved) != requested:
        raise ValueError("position result carries no addressed Assertion")
    return tuple(resolved[identity] for identity in assertion_identities)


def references_to_recorded_position_coordinates_of_byte_pair_occurrences_whose_difference_is_one(
    ledger: EventLedger, result_event_identity: str
) -> tuple[
    ReferenceToRecordedPositionOfBytePairOccurrenceWhoseDifferenceIsOne, ...
]:
    event, finding, _assertion_population_read = _read_result(
        ledger, result_event_identity
    )
    return tuple(
        _recorded_position_reference(
            event,
            finding,
            exact_pair=exact_pair,
            first_position=first_position,
            second_position=second_position,
        )
        for exact_pair, first_position, second_position in finding.occurrences
    )
