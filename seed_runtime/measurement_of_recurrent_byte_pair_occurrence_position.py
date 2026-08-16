"""Measure where one yielded recurrent byte-pair subject occurs.

This is a declared Measurement result, not a Candidate, Admission, or Standing
movement.  Its inputs remain two distinct occurrence references:

* the recurrence Assertion yielded by an earlier byte-pair Measurement; and
* one later exact Ingest result in the same Locality.

Ordering and distance are views over the two measured positions.  They are not
stored as caller-supplied signs or grammatical meanings.
"""

from __future__ import annotations

import hashlib
from typing import Any, NamedTuple

from seed_runtime.byte_measurement import (
    BYTE_PAIR_MEASUREMENT_RECORDED_KIND,
    SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY,
    assertions_of_recorded_byte_position_pair_measurement,
)
from seed_runtime.event import Event
from seed_runtime.events import CORRUPTED, EventLedger, EventLedgerBoundary
from seed_runtime.identities import new_identity
from seed_runtime.material_ingest import (
    MATERIAL_INGEST_OCCURRED_KIND,
    ingested_material_bytes,
)
from seed_runtime.evidence_of_yield_relation import (
    RECORDED_EVIDENCE_OF_YIELD_RELATION_KIND,
    _record_evidence_of_yield_relation,
    read_requirements_of_yield_relation,
)


RECORDING_OCCURRENCE_OF_RESULT_OF_MEASUREMENT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_KIND = (
    "operator.measurement_of_recurrent_byte_pair_occurrence_position."
    "recording_occurrence_of_result"
)
RECORDED_EVIDENCE_OF_ACT_OCCURRENCE_OF_MEASUREMENT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_KIND = (
    "operator.measurement_of_recurrent_byte_pair_occurrence_position."
    "evidence_of_act_occurrence_recorded"
)
RESULT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_MEASUREMENT_KIND = (
    "result of exact Measurement of recurrent byte-pair occurrence position"
)
ACT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_MEASUREMENT = (
    "declared Measurement of recurrent byte-pair occurrence position"
)
RESPONSIBILITY_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_MEASUREMENT = (
    "Measurement of each exact ordered position for one recurrent byte pair "
    "in one exact material result"
)
RULE_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_MEASUREMENT = (
    "each ordered occurrence of the exact Yield-carried byte pair in one exact "
    "Ingest result through one completeness boundary and occurrence limit"
)
AUTHORITY_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_MEASUREMENT = "bounded repository authority"
EVIDENCE_SCOPE_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_MEASUREMENT = (
    "exact Yield-carried pair Assertion and exact later Ingest result only"
)
MEASUREMENT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_BOUNDARY = (
    "measurement_of_recurrent_byte_pair_occurrence_position"
)
RESPONSIBILITY_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_ASSERTION = (
    "preserve this measured Assertion's carried Standing coordinates"
)
RESULT_COORDINATES_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_MEASUREMENT = frozenset(
    {
        "result_identity",
        "dimensions",
        "exact_act",
        "downstream_act_identity",
        "act_occurrence_identity",
        "responsibility",
        "responsible_boundary",
        "responsibility_assignment_evidence",
        "measurement_rule",
        "source_localities",
        "completeness_boundary",
        "pair_assertion_reference",
        "source_ingest_occurrence_identity",
        "occurrence_limit",
        "available_occurrence_count",
        "known_loss",
        "assertions",
    }
)
EVENT_KIND_RESPONSIBILITIES = {
    RECORDING_OCCURRENCE_OF_RESULT_OF_MEASUREMENT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_KIND: "01.Source.D",
    RECORDED_EVIDENCE_OF_ACT_OCCURRENCE_OF_MEASUREMENT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_KIND: "02.Acts.A",
}


class ReferenceToRecordedRecurrentBytePair(NamedTuple):
    """Exact address of one recurrence Assertion and its count support."""

    recorded_occurrence_identity: str
    recurrence_assertion_identity: str
    count_assertion_identity: str
    locality_identity: str
    source_occurrence_identities: tuple[str, ...]
    completeness_boundary_identity: str
    exact_material: bytes

    @property
    def assertion_reference(self) -> dict[str, str]:
        return {
            "recorded_occurrence_identity": self.recorded_occurrence_identity,
            "assertion_identity": self.recurrence_assertion_identity,
        }


class FindingOfRecurrentBytePairOccurrencePositions(NamedTuple):
    """Bounded ordered position findings for one exact pair subject."""

    pair_reference: ReferenceToRecordedRecurrentBytePair
    source_ingest_occurrence_identity: str
    source_locality_identity: str
    completeness_boundary: EventLedgerBoundary
    occurrence_limit: int
    available_occurrence_count: int
    occurrences: tuple[tuple[int, int], ...]

def _validate_pair_reference(reference: ReferenceToRecordedRecurrentBytePair) -> None:
    if type(reference) is not ReferenceToRecordedRecurrentBytePair:
        raise TypeError("recurrent pair reference requires one exact reference")
    strings = (
        reference.recorded_occurrence_identity,
        reference.recurrence_assertion_identity,
        reference.count_assertion_identity,
        reference.locality_identity,
        reference.completeness_boundary_identity,
    )
    if any(type(value) is not str or not value for value in strings):
        raise ValueError("recurrent pair reference requires exact identities")
    if (
        type(reference.source_occurrence_identities) is not tuple
        or not reference.source_occurrence_identities
        or len(set(reference.source_occurrence_identities))
        != len(reference.source_occurrence_identities)
        or any(
            type(identity) is not str or not identity
            for identity in reference.source_occurrence_identities
        )
    ):
        raise ValueError("recurrent pair reference requires distinct source occurrences")
    if type(reference.exact_material) is not bytes or len(reference.exact_material) != 2:
        raise ValueError("recurrent pair reference requires exactly two bytes")


def _validate_finding(finding: FindingOfRecurrentBytePairOccurrencePositions) -> None:
    if type(finding) is not FindingOfRecurrentBytePairOccurrencePositions:
        raise TypeError("pair occurrence finding requires one exact finding")
    _validate_pair_reference(finding.pair_reference)
    if (
        type(finding.source_ingest_occurrence_identity) is not str
        or not finding.source_ingest_occurrence_identity
        or type(finding.source_locality_identity) is not str
        or not finding.source_locality_identity
        or not isinstance(finding.completeness_boundary, EventLedgerBoundary)
    ):
        raise ValueError("pair occurrence finding requires exact source coordinates")
    if type(finding.occurrence_limit) is not int or finding.occurrence_limit <= 0:
        raise ValueError("pair occurrence finding requires a positive exact limit")
    if (
        type(finding.available_occurrence_count) is not int
        or finding.available_occurrence_count < 0
        or finding.available_occurrence_count < len(finding.occurrences)
        or len(finding.occurrences) > finding.occurrence_limit
    ):
        raise ValueError("pair occurrence finding carries an impossible count")
    if type(finding.occurrences) is not tuple:
        raise TypeError("pair occurrences require one exact tuple")
    seen = set()
    for occurrence in finding.occurrences:
        if (
            type(occurrence) is not tuple
            or len(occurrence) != 2
            or any(type(position) is not int or position < 0 for position in occurrence)
            or occurrence[0] == occurrence[1]
            or occurrence in seen
        ):
            raise ValueError("each pair occurrence requires two distinct positions")
        seen.add(occurrence)


def reference_to_recorded_recurrent_byte_pair(
    ledger: EventLedger,
    *,
    measurement_occurrence_identity: str,
    recurrence_assertion_identity: str,
) -> ReferenceToRecordedRecurrentBytePair:
    """Resolve one recurrence Assertion through its exact Measurement Yield."""

    return _references_to_recorded_recurrent_byte_pairs(
        ledger,
        measurement_occurrence_identity=measurement_occurrence_identity,
        recurrence_assertion_identities=(recurrence_assertion_identity,),
    )[0]


def _references_to_recorded_recurrent_byte_pairs(
    ledger: EventLedger,
    *,
    measurement_occurrence_identity: str,
    recurrence_assertion_identities: tuple[str, ...],
) -> tuple[ReferenceToRecordedRecurrentBytePair, ...]:
    """Resolve several subjects from one independently validated result read."""

    if not isinstance(ledger, EventLedger):
        raise TypeError("recurrent pair reference requires one EventLedger")
    if (
        type(measurement_occurrence_identity) is not str
        or not measurement_occurrence_identity
        or type(recurrence_assertion_identities) is not tuple
        or not recurrence_assertion_identities
        or any(
            type(identity) is not str or not identity
            for identity in recurrence_assertion_identities
        )
    ):
        raise ValueError("recurrent pair reference requires exact occurrence identities")
    if len(set(recurrence_assertion_identities)) != len(
        recurrence_assertion_identities
    ):
        raise ValueError("recurrent pair Assertion entered one result twice")
    event = ledger.get(measurement_occurrence_identity)
    if (
        event is None
        or event.kind != BYTE_PAIR_MEASUREMENT_RECORDED_KIND
        or type(event.locality_identity) is not str
        or not event.locality_identity
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise ValueError("recurrent pair reference requires one intact pair Measurement")
    assertions = assertions_of_recorded_byte_position_pair_measurement(
        ledger, event.identity
    )
    assertions_by_identity = {
        assertion.assertion_identity: assertion for assertion in assertions or ()
    }
    assignment = event.material.get("responsibility_assignment_evidence")
    sources = (
        assignment.get("source_occurrence_references")
        if isinstance(assignment, dict)
        else None
    )
    boundary = event.material.get("completeness_boundary")
    if (
        type(sources) is not list
        or not sources
        or any(
            type(reference) is not dict
            or set(reference) != {"ingest_occurrence_identity"}
            or type(reference["ingest_occurrence_identity"]) is not str
            or not reference["ingest_occurrence_identity"]
            for reference in sources
        )
        or type(boundary) is not dict
        or set(boundary) != {"identity"}
        or type(boundary["identity"]) is not str
        or not boundary["identity"]
    ):
        raise ValueError("the recurrent pair carries no exact source boundary")
    source_occurrence_identities = tuple(
        reference["ingest_occurrence_identity"] for reference in sources
    )
    found = []
    for recurrence_assertion_identity in recurrence_assertion_identities:
        recurrence = assertions_by_identity.get(recurrence_assertion_identity)
        if (
            recurrence is None
            or recurrence.result != "recurrence"
            or recurrence.representation is None
        ):
            raise ValueError(
                "the addressed pair Assertion does not establish recurrence"
            )
        support = recurrence.support_assertion_references
        if (
            len(support) != 1
            or support[0].get("recorded_occurrence_identity") != event.identity
            or type(support[0].get("assertion_identity")) is not str
        ):
            raise ValueError(
                "the recurrent pair carries no exact count Assertion support"
            )
        count = assertions_by_identity.get(support[0]["assertion_identity"])
        if (
            count is None
            or count.result != "count"
            or count.representation != recurrence.representation
        ):
            raise ValueError(
                "the recurrent pair count support identifies a different Assertion"
            )
        reference = ReferenceToRecordedRecurrentBytePair(
            recorded_occurrence_identity=event.identity,
            recurrence_assertion_identity=recurrence.assertion_identity,
            count_assertion_identity=count.assertion_identity,
            locality_identity=event.locality_identity,
            source_occurrence_identities=source_occurrence_identities,
            completeness_boundary_identity=boundary["identity"],
            exact_material=bytes(recurrence.representation),
        )
        _validate_pair_reference(reference)
        found.append(reference)
    return tuple(found)


def _exact_ingest_event(ledger: EventLedger, event_identity: str) -> Event:
    event = ledger.get(event_identity)
    if (
        event is None
        or event.kind != MATERIAL_INGEST_OCCURRED_KIND
        or type(event.locality_identity) is not str
        or not event.locality_identity
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise ValueError("pair occurrence Measurement requires one intact Ingest result")
    requirements = read_requirements_of_yield_relation(
        ledger,
        recorded_result_event_identity=event.identity,
        evidence_of_yield_relation_event_identity=event.material.get("evidence_of_yield_relation_identity"),
        responsible_act_evidence_event_identity=event.material.get(
            "responsible_act_evidence_identity"
        ),
    )
    if not all(requirements.values()):
        raise ValueError("pair occurrence Measurement requires exact Ingest Yield")
    ingested_material_bytes(event)
    return event


def _measure_through(
    ledger: EventLedger,
    *,
    pair_reference: ReferenceToRecordedRecurrentBytePair,
    source_ingest_occurrence_identity: str,
    boundary: EventLedgerBoundary,
    occurrence_limit: int,
) -> FindingOfRecurrentBytePairOccurrencePositions:
    source = _exact_ingest_event(ledger, source_ingest_occurrence_identity)
    if source.locality_identity != pair_reference.locality_identity:
        raise ValueError("pair subject and measured source have distinct Localities")
    ledger.occurrences_in_append_order(
        (pair_reference.recorded_occurrence_identity, source.identity),
        locality_identity=source.locality_identity,
    )
    bounded_identities = {
        event.identity
        for event in ledger.list_locality(
            source.locality_identity,
            through=boundary,
        )
    }
    if (
        pair_reference.recorded_occurrence_identity not in bounded_identities
        or source.identity not in bounded_identities
    ):
        raise ValueError("pair occurrence source falls outside its exact boundary")
    exact = ingested_material_bytes(source)
    first_byte, second_byte = pair_reference.exact_material
    first_positions = tuple(
        position for position, value in enumerate(exact) if value == first_byte
    )
    second_positions = tuple(
        position for position, value in enumerate(exact) if value == second_byte
    )
    overlap = len(first_positions) if first_byte == second_byte else 0
    available = len(first_positions) * len(second_positions) - overlap
    found = []
    for first_position in first_positions:
        for second_position in second_positions:
            if first_position == second_position:
                continue
            if len(found) == occurrence_limit:
                break
            found.append((first_position, second_position))
        if len(found) == occurrence_limit:
            break
    finding = FindingOfRecurrentBytePairOccurrencePositions(
        pair_reference=pair_reference,
        source_ingest_occurrence_identity=source.identity,
        source_locality_identity=source.locality_identity,
        completeness_boundary=boundary,
        occurrence_limit=occurrence_limit,
        available_occurrence_count=available,
        occurrences=tuple(found),
    )
    _validate_finding(finding)
    return finding


def measure_positions_of_recurrent_byte_pair_occurrences(
    ledger: EventLedger,
    *,
    pair_measurement_occurrence_identity: str,
    recurrence_assertion_identity: str,
    source_ingest_occurrence_identity: str,
    occurrence_limit: int,
    through: EventLedgerBoundary | None = None,
) -> FindingOfRecurrentBytePairOccurrencePositions:
    """Measure one yielded pair subject in one later exact Ingest result."""

    if type(occurrence_limit) is not int or occurrence_limit <= 0:
        raise ValueError("pair occurrence Measurement requires a positive exact limit")
    pair_reference = reference_to_recorded_recurrent_byte_pair(
        ledger,
        measurement_occurrence_identity=pair_measurement_occurrence_identity,
        recurrence_assertion_identity=recurrence_assertion_identity,
    )
    return _measure_through(
        ledger,
        pair_reference=pair_reference,
        source_ingest_occurrence_identity=source_ingest_occurrence_identity,
        boundary=through or ledger.append_boundary(),
        occurrence_limit=occurrence_limit,
    )


def measure_positions_for_recurrent_byte_pair_assertions(
    ledger: EventLedger,
    *,
    pair_measurement_occurrence_identity: str,
    recurrence_assertion_identities: tuple[str, ...],
    source_ingest_occurrence_identity: str,
    occurrence_limit: int,
    through: EventLedgerBoundary,
) -> tuple[FindingOfRecurrentBytePairOccurrencePositions, ...]:
    """Measure a same-boundary fan-out after one exact pair-result read."""

    if type(through) is not EventLedgerBoundary:
        raise TypeError("pair occurrence fan-out requires one exact boundary")
    if type(occurrence_limit) is not int or occurrence_limit <= 0:
        raise ValueError("pair occurrence Measurement requires a positive exact limit")
    references = _references_to_recorded_recurrent_byte_pairs(
        ledger,
        measurement_occurrence_identity=pair_measurement_occurrence_identity,
        recurrence_assertion_identities=recurrence_assertion_identities,
    )
    return tuple(
        _measure_through(
            ledger,
            pair_reference=reference,
            source_ingest_occurrence_identity=source_ingest_occurrence_identity,
            boundary=through,
            occurrence_limit=occurrence_limit,
        )
        for reference in references
    )


def _responsibility_assignment_of_measurement(finding: FindingOfRecurrentBytePairOccurrencePositions) -> dict[str, Any]:
    return {
        "responsible_boundary": SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY,
        "standing": "assigned",
        "source_occurrence_references": [
            {
                "occurrence_identity": (
                    finding.pair_reference.recorded_occurrence_identity
                )
            },
            {"occurrence_identity": finding.source_ingest_occurrence_identity},
        ],
        "completeness_boundary": finding.completeness_boundary.identity,
        "determination": RULE_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_MEASUREMENT,
    }


def _participation_in_measurement(
    finding: FindingOfRecurrentBytePairOccurrencePositions,
    *,
    act_occurrence_identity: str,
) -> list[dict[str, Any]]:
    return [
        {
            "subject_reference": finding.pair_reference.assertion_reference,
            "role": "Yield-carried recurrent byte-pair subject",
            "act_occurrence_identity": act_occurrence_identity,
            "applicability": "applicable",
        },
        {
            "subject_reference": {
                "recorded_occurrence_identity": (
                    finding.source_ingest_occurrence_identity
                )
            },
            "role": "exact material result input",
            "act_occurrence_identity": act_occurrence_identity,
            "applicability": "applicable",
        },
    ]


def _material_of_evidence_of_act_occurrence(
    finding: FindingOfRecurrentBytePairOccurrencePositions,
    *,
    act_identity: str,
    act_occurrence_identity: str,
) -> dict[str, Any]:
    return {
        "downstream_act_identity": act_identity,
        "act_occurrence_identity": act_occurrence_identity,
        "act": ACT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_MEASUREMENT,
        "responsibility": RESPONSIBILITY_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_MEASUREMENT,
        "responsible_boundary": SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY,
        "responsibility_assignment_evidence": _responsibility_assignment_of_measurement(finding),
        "measurement_rule": RULE_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_MEASUREMENT,
        "source_localities": [finding.source_locality_identity],
        "completeness_boundary": {
            "identity": finding.completeness_boundary.identity,
        },
        "pair_assertion_reference": finding.pair_reference.assertion_reference,
        "source_ingest_occurrence_identity": (
            finding.source_ingest_occurrence_identity
        ),
        "occurrence_limit": finding.occurrence_limit,
        "participation": _participation_in_measurement(
            finding,
            act_occurrence_identity=act_occurrence_identity,
        ),
        "authority": AUTHORITY_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_MEASUREMENT,
        "evidence_scope": (
            "Evidence for this exact bounded pair occurrence Measurement only"
        ),
    }


def _validate_exact_finding_of_measurement(
    ledger: EventLedger,
    finding: FindingOfRecurrentBytePairOccurrencePositions,
) -> None:
    _validate_finding(finding)
    pair_reference = reference_to_recorded_recurrent_byte_pair(
        ledger,
        measurement_occurrence_identity=(
            finding.pair_reference.recorded_occurrence_identity
        ),
        recurrence_assertion_identity=(
            finding.pair_reference.recurrence_assertion_identity
        ),
    )
    exact = _measure_through(
        ledger,
        pair_reference=pair_reference,
        source_ingest_occurrence_identity=finding.source_ingest_occurrence_identity,
        boundary=finding.completeness_boundary,
        occurrence_limit=finding.occurrence_limit,
    )
    if exact != finding:
        raise ValueError("pair occurrence finding differs from its exact inputs")


def record_evidence_of_act_occurrence_for_measurement_of_recurrent_byte_pair_occurrence_position(
    ledger: EventLedger,
    *,
    finding: FindingOfRecurrentBytePairOccurrencePositions,
    recording_locality_identity: str,
) -> Event:
    """Record the responsible Measurement Act before its Yield and result."""

    if (
        type(recording_locality_identity) is not str
        or not recording_locality_identity
        or recording_locality_identity != finding.source_locality_identity
    ):
        raise ValueError("pair occurrence Measurement requires its exact Locality")
    _validate_exact_finding_of_measurement(ledger, finding)
    act_identity = new_identity("act_of_measurement_of_recurrent_byte_pair_occurrence_position")
    act_occurrence_identity = new_identity("act_occurrence_of_measurement_of_recurrent_byte_pair_occurrence_position")
    return ledger.append(
        RECORDED_EVIDENCE_OF_ACT_OCCURRENCE_OF_MEASUREMENT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_KIND,
        _material_of_evidence_of_act_occurrence(
            finding,
            act_identity=act_identity,
            act_occurrence_identity=act_occurrence_identity,
        ),
        locality_identity=recording_locality_identity,
    )


def _finding_of_measurement_from_evidence_of_act_occurrence(
    ledger: EventLedger,
    act_evidence: Event,
) -> FindingOfRecurrentBytePairOccurrencePositions:
    material = act_evidence.material
    pair_reference = material.get("pair_assertion_reference")
    boundary = material.get("completeness_boundary")
    source_localities = material.get("source_localities")
    if (
        type(pair_reference) is not dict
        or set(pair_reference)
        != {"recorded_occurrence_identity", "assertion_identity"}
        or any(type(value) is not str or not value for value in pair_reference.values())
        or type(boundary) is not dict
        or set(boundary) != {"identity"}
        or type(boundary["identity"]) is not str
        or not boundary["identity"]
        or type(source_localities) is not list
        or len(source_localities) != 1
        or type(source_localities[0]) is not str
        or not source_localities[0]
        or type(material.get("source_ingest_occurrence_identity")) is not str
        or not material["source_ingest_occurrence_identity"]
        or type(material.get("occurrence_limit")) is not int
        or material["occurrence_limit"] <= 0
    ):
        raise ValueError("pair occurrence Act Evidence carries malformed coordinates")
    finding = measure_positions_of_recurrent_byte_pair_occurrences(
        ledger,
        pair_measurement_occurrence_identity=pair_reference[
            "recorded_occurrence_identity"
        ],
        recurrence_assertion_identity=pair_reference["assertion_identity"],
        source_ingest_occurrence_identity=material[
            "source_ingest_occurrence_identity"
        ],
        occurrence_limit=material["occurrence_limit"],
        through=EventLedgerBoundary(boundary["identity"]),
    )
    if finding.source_locality_identity != source_localities[0]:
        raise ValueError(
            "pair occurrence Act Evidence names a different source Locality"
        )
    return finding


def _identity_of_position_assertion(
    *,
    finding: FindingOfRecurrentBytePairOccurrencePositions,
    first_position: int,
    second_position: int,
) -> str:
    digest = hashlib.sha256()
    for coordinate in (
        finding.pair_reference.recorded_occurrence_identity,
        finding.pair_reference.recurrence_assertion_identity,
        finding.source_ingest_occurrence_identity,
        finding.source_locality_identity,
        finding.completeness_boundary.identity,
        str(first_position),
        str(second_position),
    ):
        encoded = coordinate.encode("utf-8")
        digest.update(len(encoded).to_bytes(8, "big"))
        digest.update(encoded)
    return "pair-occurrence-measurement:" + digest.hexdigest()


def _position_assertions_of_measurement(finding: FindingOfRecurrentBytePairOccurrencePositions) -> list[dict[str, Any]]:
    scope = {"source_localities": [finding.source_locality_identity]}
    subject = {
        "pair_assertion_reference": finding.pair_reference.assertion_reference,
        "source_ingest_occurrence_identity": (
            finding.source_ingest_occurrence_identity
        ),
        "measurement_rule": RULE_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_MEASUREMENT,
    }
    assertions = []
    for first_position, second_position in finding.occurrences:
        content = {
            "first_position": first_position,
            "second_position": second_position,
            "completeness_boundary": {
                "identity": finding.completeness_boundary.identity,
            },
        }
        assertions.append(
            {
                "dimensions": {
                    "identity": _identity_of_position_assertion(
                        finding=finding,
                        first_position=first_position,
                        second_position=second_position,
                    ),
                    "content": content,
                    "standing": "measured",
                    "source_provenance": (
                        "the exact Yield-carried pair Assertion and later Ingest result"
                    ),
                    "responsibility": RESPONSIBILITY_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_ASSERTION,
                    "authority": "unestablished",
                    "evidence_scope": EVIDENCE_SCOPE_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_MEASUREMENT,
                },
                "subject_kind": "assertion",
                "responsible_boundary": "this recorded assertion",
                "result": "position",
                "assertion_subject": subject,
                "assertion_scope": scope,
                "input_support": {
                    "assertion_references": [
                        finding.pair_reference.assertion_reference
                    ],
                    "occurrence_references": [
                        finding.source_ingest_occurrence_identity
                    ],
                    "local_assertion_references": [],
                },
                "conflicts": "Unknown",
                "unknowns": [
                    "what this ordered pair occurrence relation is remains Unknown"
                ],
                "limits": [
                    "position is bounded by the exact source result, completeness "
                    "boundary, and occurrence limit"
                ],
            }
        )
    return assertions


def _material_of_result_of_measurement(
    finding: FindingOfRecurrentBytePairOccurrencePositions,
    *,
    result_identity: str,
    act_identity: str,
    act_occurrence_identity: str,
) -> dict[str, Any]:
    known_loss = (
        ["pair occurrences beyond the exact occurrence limit are not carried"]
        if finding.available_occurrence_count > len(finding.occurrences)
        else []
    )
    return {
        "result_identity": result_identity,
        "dimensions": {
            "identity": "recurrent-byte-pair-occurrence-position-measurement",
            "content": "exact ordered pair occurrence position Assertions",
            "standing": "measured",
            "source_provenance": (
                "one recurrence Assertion carried by Evidence of Yield relation and one later "
                "exact Ingest result"
            ),
            "authority": "unestablished",
            "evidence_scope": EVIDENCE_SCOPE_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_MEASUREMENT,
        },
        "exact_act": ACT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_MEASUREMENT,
        "downstream_act_identity": act_identity,
        "act_occurrence_identity": act_occurrence_identity,
        "responsibility": RESPONSIBILITY_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_MEASUREMENT,
        "responsible_boundary": SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY,
        "responsibility_assignment_evidence": _responsibility_assignment_of_measurement(finding),
        "measurement_rule": RULE_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_MEASUREMENT,
        "source_localities": [finding.source_locality_identity],
        "completeness_boundary": {
            "identity": finding.completeness_boundary.identity,
        },
        "pair_assertion_reference": finding.pair_reference.assertion_reference,
        "source_ingest_occurrence_identity": (
            finding.source_ingest_occurrence_identity
        ),
        "occurrence_limit": finding.occurrence_limit,
        "available_occurrence_count": finding.available_occurrence_count,
        "known_loss": known_loss,
        "assertions": _position_assertions_of_measurement(finding),
    }


def record_result_of_measurement_of_recurrent_byte_pair_occurrence_position(
    ledger: EventLedger,
    *,
    responsible_act_evidence_event_identity: str,
) -> Event:
    """Record the Yield and result for one exact pair occurrence Measurement."""

    if (
        type(responsible_act_evidence_event_identity) is not str
        or not responsible_act_evidence_event_identity
    ):
        raise ValueError("pair occurrence result requires exact Act Evidence")
    act_evidence = ledger.get(responsible_act_evidence_event_identity)
    if (
        act_evidence is None
        or act_evidence.kind != RECORDED_EVIDENCE_OF_ACT_OCCURRENCE_OF_MEASUREMENT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_KIND
        or type(act_evidence.locality_identity) is not str
        or not act_evidence.locality_identity
        or ledger.integrity_of(act_evidence.identity) == CORRUPTED
    ):
        raise ValueError("pair occurrence result requires intact Act Evidence")
    finding = _finding_of_measurement_from_evidence_of_act_occurrence(ledger, act_evidence)
    expected_act = _material_of_evidence_of_act_occurrence(
        finding,
        act_identity=act_evidence.material.get("downstream_act_identity"),
        act_occurrence_identity=act_evidence.material.get("act_occurrence_identity"),
    )
    if act_evidence.material != expected_act:
        raise ValueError(
            "pair occurrence result differs from its exact Act Evidence"
        )
    act_occurrence_identity = act_evidence.material["act_occurrence_identity"]
    for event in ledger.list_locality(act_evidence.locality_identity):
        if event.kind in {
            RECORDED_EVIDENCE_OF_YIELD_RELATION_KIND,
            RECORDING_OCCURRENCE_OF_RESULT_OF_MEASUREMENT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_KIND,
        } and (
            event.material.get("responsible_act_evidence_identity")
            == act_evidence.identity
            or event.material.get("act_occurrence_identity")
            == act_occurrence_identity
            or event.material.get("dimensions", {}).get("act_occurrence_identity")
            == act_occurrence_identity
        ):
            raise ValueError("pair occurrence Measurement Act already has a result")
    result_identity = new_identity("result_of_measurement_of_recurrent_byte_pair_occurrence_position")
    result = _material_of_result_of_measurement(
        finding,
        result_identity=result_identity,
        act_identity=act_evidence.material["downstream_act_identity"],
        act_occurrence_identity=act_occurrence_identity,
    )
    evidence = _record_evidence_of_yield_relation(
        ledger,
        locality_identity=act_evidence.locality_identity,
        exact_act=ACT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_MEASUREMENT,
        act_occurrence_identity=act_occurrence_identity,
        responsible_act_evidence_identity=act_evidence.identity,
        result_kind=RESULT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_MEASUREMENT_KIND,
        result_identity=result_identity,
        result_content=result,
        responsibility=RESPONSIBILITY_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_MEASUREMENT,
        live_boundary="measurement_of_recurrent_byte_pair_occurrence_position",
        responsible_boundary=SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY,
    )
    return ledger.append(
        RECORDING_OCCURRENCE_OF_RESULT_OF_MEASUREMENT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_KIND,
        {
            "result_identity": result["result_identity"],
            "dimensions": result["dimensions"],
            "exact_act": result["exact_act"],
            "downstream_act_identity": result["downstream_act_identity"],
            "act_occurrence_identity": result["act_occurrence_identity"],
            "responsibility": result["responsibility"],
            "responsible_boundary": result["responsible_boundary"],
            "responsibility_assignment_evidence": result[
                "responsibility_assignment_evidence"
            ],
            "measurement_rule": result["measurement_rule"],
            "source_localities": result["source_localities"],
            "completeness_boundary": result["completeness_boundary"],
            "pair_assertion_reference": result["pair_assertion_reference"],
            "source_ingest_occurrence_identity": result[
                "source_ingest_occurrence_identity"
            ],
            "occurrence_limit": result["occurrence_limit"],
            "available_occurrence_count": result[
                "available_occurrence_count"
            ],
            "known_loss": result["known_loss"],
            "assertions": result["assertions"],
            "responsible_act_evidence_identity": act_evidence.identity,
            "evidence_of_yield_relation_identity": evidence.identity,
        },
        locality_identity=act_evidence.locality_identity,
    )


def get_recorded_result_of_measurement_of_recurrent_byte_pair_occurrence_position(
    ledger: EventLedger,
    event_identity: str,
) -> FindingOfRecurrentBytePairOccurrencePositions:
    """Read one pair-occurrence result through its exact Act and Yield."""

    event = ledger.get(event_identity)
    if (
        event is None
        or event.kind != RECORDING_OCCURRENCE_OF_RESULT_OF_MEASUREMENT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_KIND
        or type(event.locality_identity) is not str
        or not event.locality_identity
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise ValueError("pair occurrence Measurement result is absent or corrupted")
    material = event.material
    if set(material) != RESULT_COORDINATES_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_MEASUREMENT | {
        "responsible_act_evidence_identity",
        "evidence_of_yield_relation_identity",
    }:
        raise ValueError("pair occurrence result carries malformed coordinates")
    act_evidence_identity = material.get("responsible_act_evidence_identity")
    act_evidence = (
        ledger.get(act_evidence_identity)
        if type(act_evidence_identity) is str
        else None
    )
    if (
        act_evidence is None
        or act_evidence.kind != RECORDED_EVIDENCE_OF_ACT_OCCURRENCE_OF_MEASUREMENT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_KIND
        or act_evidence.locality_identity != event.locality_identity
        or ledger.integrity_of(act_evidence.identity) == CORRUPTED
    ):
        raise ValueError("pair occurrence result carries no exact Act Evidence")
    finding = _finding_of_measurement_from_evidence_of_act_occurrence(ledger, act_evidence)
    expected_act = _material_of_evidence_of_act_occurrence(
        finding,
        act_identity=material.get("downstream_act_identity"),
        act_occurrence_identity=material.get("act_occurrence_identity"),
    )
    if act_evidence.material != expected_act:
        raise ValueError(
            "pair occurrence result differs from its exact Act Evidence"
        )
    result = _material_of_result_of_measurement(
        finding,
        result_identity=material.get("result_identity"),
        act_identity=material.get("downstream_act_identity"),
        act_occurrence_identity=material.get("act_occurrence_identity"),
    )
    carried = {
        key: value
        for key, value in material.items()
        if key
        not in {"responsible_act_evidence_identity", "evidence_of_yield_relation_identity"}
    }
    if carried != result:
        raise ValueError("pair occurrence result differs from its exact finding")
    requirements = read_requirements_of_yield_relation(
        ledger,
        recorded_result_event_identity=event.identity,
        evidence_of_yield_relation_event_identity=material.get("evidence_of_yield_relation_identity"),
        responsible_act_evidence_event_identity=act_evidence.identity,
    )
    evidence_of_yield_relation = ledger.get(material.get("evidence_of_yield_relation_identity"))
    if (
        not all(requirements.values())
        or evidence_of_yield_relation is None
        or evidence_of_yield_relation.material.get("live_boundary")
        != MEASUREMENT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_BOUNDARY
        or evidence_of_yield_relation.material.get("result_kind")
        != RESULT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_MEASUREMENT_KIND
    ):
        raise ValueError("pair occurrence result carries no exact Evidence of Yield relation")
    return finding
