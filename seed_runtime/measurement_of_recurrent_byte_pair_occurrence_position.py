"""Measure where one yielded recurrent byte-pair subject occurs.

This declared Measurement carries two distinct occurrence references:

* the recurrence Assertion yielded by an earlier byte-pair Measurement; and
* one later exact material result in the same Locality.

Ordering and distance are views over the two measured positions.  The result
carries neither a caller-supplied sign nor a grammatical meaning.
"""

from __future__ import annotations

from typing import Any, NamedTuple

from seed_runtime.byte_measurement import (
    BYTE_PAIR_MEASUREMENT_RECORDED_KIND,
    _validated_recorded_byte_position_pair_measurement,
)
from seed_runtime.event import Event
from seed_runtime.events import CORRUPTED, EventLedger, EventLedgerBoundary
from seed_runtime.material_source import (
    exact_material_result_bytes,
    read_exact_material_result,
)
from seed_runtime.yield_relation import (
    RECORDED_YIELD_RELATION_EVENT,
    _record_yield_relation,
    read_requirements_of_yield_relation,
)


RECORDING_OCCURRENCE_OF_RESULT_OF_MEASUREMENT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_KIND = (
    "operator.measurement_of_recurrent_byte_pair_occurrence_position."
    "recording_occurrence_of_result"
)
RECORDED_ACT_OCCURRENCE_OF_MEASUREMENT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_EVENT = (
    "operator.measurement_of_recurrent_byte_pair_occurrence_position."
    "act_occurrence_recorded"
)
RECORDED_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_MEASUREMENT_SUBJECT_TO_ACT_BINDING_KIND = (
    "operator.measurement_of_recurrent_byte_pair_occurrence_position."
    "subject_to_act_binding_recorded"
)
RESULT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_MEASUREMENT_KIND = (
    "result of exact Measurement of recurrent byte-pair occurrence position"
)
ACT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_MEASUREMENT = (
    "declared Measurement of byte-pair occurrence position"
)
RULE_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_MEASUREMENT = (
    "each ordered occurrence of the exact Yield-carried byte pair in one exact "
    "material result within one completeness boundary and occurrence count boundary"
)
SCOPE_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_MEASUREMENT = (
    "exact Yield-carried pair Assertion and exact later material result only"
)
MEASUREMENT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_BOUNDARY = (
    "measurement_of_recurrent_byte_pair_occurrence_position"
)
RESULT_COORDINATES_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_MEASUREMENT = frozenset(
    {
        "result_identity",
        "dimensions",
        "exact_act",
        "addressed_act_identity",
        "act_occurrence_identity",
        "subject_to_act_binding_reference",
        "measurement_rule",
        "source_localities",
        "completeness_boundary",
        "pair_assertion_reference",
        "source_material_result_occurrence_identity",
        "occurrence_count_boundary",
        "available_occurrence_count",
        "known_loss",
        "assertions",
    }
)
EVENT_KIND_BOOK_CLAUSES = {
    RECORDED_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_MEASUREMENT_SUBJECT_TO_ACT_BINDING_KIND: "01.Source.D",
    RECORDING_OCCURRENCE_OF_RESULT_OF_MEASUREMENT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_KIND: "01.Source.D",
    RECORDED_ACT_OCCURRENCE_OF_MEASUREMENT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_EVENT: "02.Acts.A",
}


def _exact_measurement_occurrence_coordinates(
    ledger: EventLedger, event_identity: str
) -> dict[str, str]:
    event = ledger.get(event_identity)
    if (
        event is None
        or event.kind != BYTE_PAIR_MEASUREMENT_RECORDED_KIND
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise ValueError(
            "pair occurrence binding carries no intact pair Measurement"
        )
    return {
        "recorded_occurrence_identity": event.identity,
        "result_identity": event.material["result_identity"],
        "act_occurrence_identity": event.material["act_occurrence_identity"],
        "act_occurrence_event_identity": event.material[
            "act_occurrence_event_identity"
        ],
        "yield_relation_identity": event.material[
            "yield_relation_identity"
        ],
    }


def _exact_material_result_availability_coordinates(
    ledger: EventLedger, event_identity: str
) -> dict[str, Any]:
    event = read_exact_material_result(ledger, event_identity)
    dimensions = event.material["dimensions"]
    occurrence = {
        "subject_reference": dimensions["identity"],
        "result_occurrence_identity": event.identity,
        "source_role": event.material["source_role"],
    }
    return occurrence


class ReferenceToRecordedRecurrentBytePair(NamedTuple):
    """Exact address of one recurrence Assertion and its count support."""

    recorded_occurrence_identity: str
    recurrence_assertion_position: int
    count_assertion_position: int
    locality_identity: str
    source_occurrence_identities: tuple[str, ...]
    completeness_boundary_identity: str
    exact_material: bytes

    @property
    def assertion_reference(self) -> dict[str, Any]:
        return {
            "recorded_occurrence_identity": self.recorded_occurrence_identity,
            "assertion_position": self.recurrence_assertion_position,
        }


class FindingOfRecurrentBytePairOccurrencePositions(NamedTuple):
    """Bounded ordered position findings for one exact pair subject."""

    pair_reference: ReferenceToRecordedRecurrentBytePair
    source_material_result_occurrence_identity: str
    source_locality_identity: str
    completeness_boundary: EventLedgerBoundary
    occurrence_count_boundary: int
    available_occurrence_count: int
    occurrences: tuple[tuple[int, int], ...]


class ReferenceToRecordedRecurrentBytePairOccurrencePosition(NamedTuple):
    """Immutable address of one exact yielded pair-position Assertion."""

    recorded_occurrence_identity: str
    assertion_position: int
    pair_measurement_occurrence_identity: str
    recurrence_assertion_position: int
    count_assertion_position: int
    source_material_result_occurrence_identity: str
    locality_identity: str
    completeness_boundary_identity: str
    exact_pair: bytes
    first_position: int
    second_position: int

    @property
    def assertion_address(self) -> int:
        return self.assertion_position

    @property
    def assertion_reference(self) -> dict[str, Any]:
        return {
            "recorded_occurrence_identity": self.recorded_occurrence_identity,
            "assertion_position": self.assertion_position,
        }

def _validate_pair_reference(reference: ReferenceToRecordedRecurrentBytePair) -> None:
    if type(reference) is not ReferenceToRecordedRecurrentBytePair:
        raise TypeError("recurrent pair reference requires one exact reference")
    strings = (
        reference.recorded_occurrence_identity,
        reference.locality_identity,
        reference.completeness_boundary_identity,
    )
    if any(type(value) is not str or not value for value in strings):
        raise ValueError("recurrent pair reference requires exact identities")
    if (
        type(reference.recurrence_assertion_position) is not int
        or reference.recurrence_assertion_position < 0
        or type(reference.count_assertion_position) is not int
        or reference.count_assertion_position < 0
    ):
        raise ValueError("recurrent pair reference requires exact Assertion positions")
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
        type(finding.source_material_result_occurrence_identity) is not str
        or not finding.source_material_result_occurrence_identity
        or type(finding.source_locality_identity) is not str
        or not finding.source_locality_identity
        or not isinstance(finding.completeness_boundary, EventLedgerBoundary)
    ):
        raise ValueError("pair occurrence finding requires exact source coordinates")
    if type(finding.occurrence_count_boundary) is not int or finding.occurrence_count_boundary <= 0:
        raise ValueError("pair occurrence finding requires a positive exact count boundary")
    if (
        type(finding.available_occurrence_count) is not int
        or finding.available_occurrence_count < 0
        or finding.available_occurrence_count < len(finding.occurrences)
        or len(finding.occurrences) > finding.occurrence_count_boundary
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
    recurrence_assertion_position: int,
) -> ReferenceToRecordedRecurrentBytePair:
    """Resolve one recurrence Assertion through its exact Measurement Yield."""

    return _references_to_recorded_recurrent_byte_pairs(
        ledger,
        measurement_occurrence_identity=measurement_occurrence_identity,
        recurrence_assertion_positions=(recurrence_assertion_position,),
    )[0]


def _references_to_recorded_recurrent_byte_pairs(
    ledger: EventLedger,
    *,
    measurement_occurrence_identity: str,
    recurrence_assertion_positions: tuple[int, ...],
    prior_coordinates: dict[str, Any] | None = None,
) -> tuple[ReferenceToRecordedRecurrentBytePair, ...]:
    """Resolve every exact subject from one independently validated result read."""

    if not isinstance(ledger, EventLedger):
        raise TypeError("recurrent pair reference requires one EventLedger")
    if (
        type(measurement_occurrence_identity) is not str
        or not measurement_occurrence_identity
        or type(recurrence_assertion_positions) is not tuple
        or not recurrence_assertion_positions
        or any(
            type(position) is not int or position < 0
            for position in recurrence_assertion_positions
        )
    ):
        raise ValueError("recurrent pair reference requires exact Assertion positions")
    if len(set(recurrence_assertion_positions)) != len(
        recurrence_assertion_positions
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
    reading = (
        _validated_recorded_byte_position_pair_measurement(
            ledger,
            event.identity,
            findings_only=True,
            prior_coordinates=prior_coordinates,
        )
        if prior_coordinates is not None
        else _validated_recorded_byte_position_pair_measurement(
            ledger, event.identity, findings_only=True
        )
    )
    findings = reading.results if reading is not None else None
    findings_by_position = {
        finding.assertion_position: finding for finding in findings or ()
    }
    binding = reading.binding.material if reading is not None else None
    sources = (
        binding.get("source_occurrence_references")
        if isinstance(binding, dict)
        else None
    )
    boundary = event.material.get("completeness_boundary")
    if (
        type(sources) is not list
        or not sources
        or any(
            type(reference) is not dict
            or set(reference) != {"material_result_occurrence_identity"}
            or type(reference["material_result_occurrence_identity"]) is not str
            or not reference["material_result_occurrence_identity"]
            for reference in sources
        )
        or type(boundary) is not dict
        or set(boundary) != {"identity"}
        or type(boundary["identity"]) is not str
        or not boundary["identity"]
    ):
        raise ValueError("the recurrent pair carries no exact source boundary")
    source_occurrence_identities = tuple(
        reference["material_result_occurrence_identity"] for reference in sources
    )
    found = []
    for recurrence_assertion_position in recurrence_assertion_positions:
        recurrence = findings_by_position.get(recurrence_assertion_position)
        if (
            recurrence is None
            or recurrence.result != "recurrence"
            or recurrence.exact_pair is None
        ):
            raise ValueError(
                "the addressed pair Assertion does not establish recurrence"
            )
        support = recurrence._local_support_assertion_positions
        if (
            len(support) != 1
            or type(support[0]) is not int
            or support[0] < 0
        ):
            raise ValueError(
                "the recurrent pair carries no exact count Assertion support"
            )
        count = findings_by_position.get(support[0])
        if (
            count is None
            or count.result != "count"
            or count.exact_pair != recurrence.exact_pair
        ):
            raise ValueError(
                "the recurrent pair count support carries another exact Assertion reference"
            )
        reference = ReferenceToRecordedRecurrentBytePair(
            recorded_occurrence_identity=event.identity,
            recurrence_assertion_position=recurrence.assertion_position,
            count_assertion_position=count.assertion_position,
            locality_identity=event.locality_identity,
            source_occurrence_identities=source_occurrence_identities,
            completeness_boundary_identity=boundary["identity"],
            exact_material=bytes(recurrence.exact_pair),
        )
        _validate_pair_reference(reference)
        found.append(reference)
    return tuple(found)


def _exact_material_result(ledger: EventLedger, event_identity: str) -> Event:
    try:
        return read_exact_material_result(ledger, event_identity)
    except (TypeError, ValueError) as error:
        raise ValueError(
            "pair occurrence Measurement requires one intact material result"
        ) from error


def _measurement_source_position_coordinates(
    ledger: EventLedger,
    *,
    pair_references: tuple[ReferenceToRecordedRecurrentBytePair, ...],
    source_material_result_occurrence_identity: str,
    boundary: EventLedgerBoundary,
) -> tuple[Event, tuple[tuple[int, ...], ...]]:
    if not pair_references:
        raise ValueError("pair occurrence Measurement requires one pair subject")
    source = _exact_material_result(ledger, source_material_result_occurrence_identity)
    pair_measurement_identity = pair_references[0].recorded_occurrence_identity
    if any(
        reference.recorded_occurrence_identity != pair_measurement_identity
        or reference.locality_identity != source.locality_identity
        for reference in pair_references
    ):
        raise ValueError("pair subject and measured source have distinct Localities")
    ledger.occurrences_in_append_order(
        (pair_measurement_identity, source.identity),
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
        pair_measurement_identity not in bounded_identities
        or source.identity not in bounded_identities
    ):
        raise ValueError("pair occurrence source falls outside its exact boundary")
    exact = exact_material_result_bytes(source)
    position_coordinates = [[] for _ in range(256)]
    for position, value in enumerate(exact):
        position_coordinates[value].append(position)
    return source, tuple(
        tuple(coordinates) for coordinates in position_coordinates
    )


def _finding_from_source_position_coordinates(
    *,
    pair_reference: ReferenceToRecordedRecurrentBytePair,
    source: Event,
    position_coordinates: tuple[tuple[int, ...], ...],
    boundary: EventLedgerBoundary,
    occurrence_count_boundary: int,
) -> FindingOfRecurrentBytePairOccurrencePositions:
    first_byte, second_byte = pair_reference.exact_material
    first_position_coordinates = position_coordinates[first_byte]
    second_position_coordinates = position_coordinates[second_byte]
    overlap = (
        len(first_position_coordinates) if first_byte == second_byte else 0
    )
    available = (
        len(first_position_coordinates) * len(second_position_coordinates)
        - overlap
    )
    found = []
    for first_position in first_position_coordinates:
        for second_position in second_position_coordinates:
            if first_position == second_position:
                continue
            if len(found) == occurrence_count_boundary:
                break
            found.append((first_position, second_position))
        if len(found) == occurrence_count_boundary:
            break
    finding = FindingOfRecurrentBytePairOccurrencePositions(
        pair_reference=pair_reference,
        source_material_result_occurrence_identity=source.identity,
        source_locality_identity=source.locality_identity,
        completeness_boundary=boundary,
        occurrence_count_boundary=occurrence_count_boundary,
        available_occurrence_count=available,
        occurrences=tuple(found),
    )
    _validate_finding(finding)
    return finding


def _measure_through(
    ledger: EventLedger,
    *,
    pair_reference: ReferenceToRecordedRecurrentBytePair,
    source_material_result_occurrence_identity: str,
    boundary: EventLedgerBoundary,
    occurrence_count_boundary: int,
) -> FindingOfRecurrentBytePairOccurrencePositions:
    source, position_coordinates = _measurement_source_position_coordinates(
        ledger,
        pair_references=(pair_reference,),
        source_material_result_occurrence_identity=source_material_result_occurrence_identity,
        boundary=boundary,
    )
    return _finding_from_source_position_coordinates(
        pair_reference=pair_reference,
        source=source,
        position_coordinates=position_coordinates,
        boundary=boundary,
        occurrence_count_boundary=occurrence_count_boundary,
    )


def measure_positions_of_recurrent_byte_pair_occurrences(
    ledger: EventLedger,
    *,
    pair_measurement_occurrence_identity: str,
    recurrence_assertion_position: int,
    source_material_result_occurrence_identity: str,
    occurrence_count_boundary: int,
    through: EventLedgerBoundary | None = None,
) -> FindingOfRecurrentBytePairOccurrencePositions:
    """Measure one yielded pair subject in one later exact material result."""

    if type(occurrence_count_boundary) is not int or occurrence_count_boundary <= 0:
        raise ValueError("pair occurrence Measurement requires a positive exact count boundary")
    pair_reference = reference_to_recorded_recurrent_byte_pair(
        ledger,
        measurement_occurrence_identity=pair_measurement_occurrence_identity,
        recurrence_assertion_position=recurrence_assertion_position,
    )
    return _measure_through(
        ledger,
        pair_reference=pair_reference,
        source_material_result_occurrence_identity=source_material_result_occurrence_identity,
        boundary=through or ledger.append_boundary(),
        occurrence_count_boundary=occurrence_count_boundary,
    )


def measure_positions_for_recurrent_byte_pair_assertions(
    ledger: EventLedger,
    *,
    pair_measurement_occurrence_identity: str,
    recurrence_assertion_positions: tuple[int, ...],
    source_material_result_occurrence_identity: str,
    occurrence_count_boundary: int,
    through: EventLedgerBoundary,
) -> tuple[FindingOfRecurrentBytePairOccurrencePositions, ...]:
    """Measure same-boundary pair subjects after one exact pair-result read."""

    if type(through) is not EventLedgerBoundary:
        raise TypeError(
            "Measurement of same-boundary pair subjects requires one exact boundary"
        )
    if type(occurrence_count_boundary) is not int or occurrence_count_boundary <= 0:
        raise ValueError("pair occurrence Measurement requires a positive exact count boundary")
    references = _references_to_recorded_recurrent_byte_pairs(
        ledger,
        measurement_occurrence_identity=pair_measurement_occurrence_identity,
        recurrence_assertion_positions=recurrence_assertion_positions,
    )
    source, position_coordinates = _measurement_source_position_coordinates(
        ledger,
        pair_references=references,
        source_material_result_occurrence_identity=source_material_result_occurrence_identity,
        boundary=through,
    )
    return tuple(
        _finding_from_source_position_coordinates(
            pair_reference=reference,
            source=source,
            position_coordinates=position_coordinates,
            boundary=through,
            occurrence_count_boundary=occurrence_count_boundary,
        )
        for reference in references
    )


def _binding_reference(binding: Event) -> dict[str, Any]:
    return {
        "recorded_occurrence_identity": binding.identity,
        "book_clause_identity": binding.material["book_clause_identity"],
        "exact_act_identity": binding.material["exact_act_identity"],
        "subject_reference": binding.material["subject_reference"],
        "result_boundary_identity": binding.material[
            "result_boundary_identity"
        ],
    }


def _binding_material(
    finding: FindingOfRecurrentBytePairOccurrencePositions,
    *,
    exact_act_identity: str,
    act_occurrence_identity: str,
    measurement_result_identity: str,
    through_event_occurrence_identity: str,
) -> dict[str, Any]:
    subject_reference = {
        "pair_assertion_reference": finding.pair_reference.assertion_reference,
        "source_material_result_occurrence_identity": (
            finding.source_material_result_occurrence_identity
        ),
    }
    return {
        "exact_act_identity": exact_act_identity,
        "subject_reference": subject_reference,
        "act_occurrence_identity": act_occurrence_identity,
        "measurement_result_identity": measurement_result_identity,
        "result_boundary_identity": measurement_result_identity,
        "book_clause_identity": "01.Source.D",
        "pair_assertion_reference": finding.pair_reference.assertion_reference,
        "source_material_result_occurrence_identity": (
            finding.source_material_result_occurrence_identity
        ),
        "source_locality_identity": finding.source_locality_identity,
        "completeness_boundary_identity": finding.completeness_boundary.identity,
        "occurrence_count_boundary": finding.occurrence_count_boundary,
        "through_event_occurrence_identity": through_event_occurrence_identity,
        "scope": {
            "source_locality_identity": finding.source_locality_identity,
            "completeness_boundary_identity": (
                finding.completeness_boundary.identity
            ),
            "occurrence_count_boundary": finding.occurrence_count_boundary,
        },
        "unknown": [],
    }


def _require_current_binding_coordinates(
    ledger: EventLedger,
    *,
    finding: FindingOfRecurrentBytePairOccurrencePositions,
    current_coordinates: dict[str, Any],
    required_binding_identity: str | None = None,
) -> str:
    if type(current_coordinates) is not dict:
        raise ValueError(
            "pair occurrence Measurement requires exact current coordinates"
        )
    from seed_runtime.operator_current_coordinates import (
        read_operator_current_coordinates,
    )
    from seed_runtime.material_source import (
        read_material_locality_relation_requirements,
    )

    current = read_operator_current_coordinates(
        ledger, locality_identity=finding.source_locality_identity
    )
    measurements = current_coordinates.get("measurement_occurrences")
    material_results = current_coordinates.get("material_result_occurrences")
    bindings = current_coordinates.get("subject_to_act_binding_occurrences")
    boundary = current_coordinates.get("through_event_occurrence_identity")
    source_has_exact_locality = all(
        read_material_locality_relation_requirements(
            ledger,
            recorded_result_event_identity=(
                finding.source_material_result_occurrence_identity
            ),
        ).values()
    )
    if (
        current_coordinates != current
        or current_coordinates.get("locality_identity")
        != finding.source_locality_identity
        or type(boundary) is not str
        or not boundary
        or type(measurements) is not dict
        or finding.pair_reference.recorded_occurrence_identity not in measurements
        or type(material_results) is not list
        or not any(
            type(occurrence) is dict
            and occurrence.get("result_occurrence_identity")
            == finding.source_material_result_occurrence_identity
            for occurrence in material_results
        )
        or not source_has_exact_locality
        or (
            required_binding_identity is not None
            and (
                type(bindings) is not dict
                or bindings.get(required_binding_identity, object()) is not None
            )
        )
    ):
        raise ValueError(
            "pair occurrence Measurement requires exact current coordinates"
        )
    return boundary


def record_recurrent_byte_pair_occurrence_position_measurement_subject_to_act_binding(
    ledger: EventLedger,
    *,
    finding: FindingOfRecurrentBytePairOccurrencePositions,
    current_coordinates: dict[str, Any],
) -> Event:
    """Record one exact subject-to-Act binding."""

    _validate_exact_finding_of_measurement(ledger, finding)
    through_event_occurrence_identity = _require_current_binding_coordinates(
        ledger, finding=finding, current_coordinates=current_coordinates
    )
    identities = {
        "exact_act_identity": ledger.mint_identity(
            "act_of_measurement_of_recurrent_byte_pair_occurrence_position"
        ),
        "act_occurrence_identity": ledger.mint_identity(
            "act_occurrence_of_measurement_of_recurrent_byte_pair_occurrence_position"
        ),
        "measurement_result_identity": ledger.mint_identity(
            "result_of_measurement_of_recurrent_byte_pair_occurrence_position"
        ),
    }
    if len(set(identities.values())) != len(identities):
        raise ValueError("pair occurrence Measurement lifecycle identities collapsed")
    return ledger.append(
        RECORDED_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_MEASUREMENT_SUBJECT_TO_ACT_BINDING_KIND,
        _binding_material(
            finding,
            through_event_occurrence_identity=through_event_occurrence_identity,
            **identities,
        ),
        locality_identity=finding.source_locality_identity,
    )


def _read_recurrent_byte_pair_occurrence_position_measurement_binding(
    ledger: EventLedger,
    binding_event_identity: str,
    *,
    prior_coordinates: dict[str, Any] | None = None,
) -> tuple[Event, FindingOfRecurrentBytePairOccurrencePositions]:
    if type(binding_event_identity) is not str or not binding_event_identity:
        raise ValueError("pair occurrence Measurement requires one exact binding")
    binding = ledger.get(binding_event_identity)
    if (
        binding is None
        or binding.kind
        != RECORDED_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_MEASUREMENT_SUBJECT_TO_ACT_BINDING_KIND
        or type(binding.locality_identity) is not str
        or not binding.locality_identity
        or ledger.integrity_of(binding.identity) == CORRUPTED
    ):
        raise ValueError("pair occurrence binding is absent or corrupted")
    material = binding.material
    identities = {
        coordinate: material.get(coordinate)
        for coordinate in (
            "exact_act_identity",
            "act_occurrence_identity",
            "measurement_result_identity",
        )
    }
    pair_reference = material.get("pair_assertion_reference")
    if (
        any(type(identity) is not str or not identity for identity in identities.values())
        or len(set(identities.values())) != len(identities)
        or type(pair_reference) is not dict
        or set(pair_reference)
        != {"recorded_occurrence_identity", "assertion_position"}
        or type(pair_reference["recorded_occurrence_identity"]) is not str
        or not pair_reference["recorded_occurrence_identity"]
        or type(pair_reference["assertion_position"]) is not int
        or pair_reference["assertion_position"] < 0
        or type(material.get("source_material_result_occurrence_identity")) is not str
        or not material["source_material_result_occurrence_identity"]
        or type(material.get("completeness_boundary_identity")) is not str
        or not material["completeness_boundary_identity"]
        or type(material.get("occurrence_count_boundary")) is not int
        or material["occurrence_count_boundary"] <= 0
        or type(material.get("through_event_occurrence_identity")) is not str
        or not material["through_event_occurrence_identity"]
    ):
        raise ValueError("pair occurrence binding carries malformed coordinates")
    through_event_occurrence_identity = material[
        "through_event_occurrence_identity"
    ]
    if prior_coordinates is None:
        from seed_runtime.operator_current_coordinates import (
            _operator_current_coordinate_validation_context,
        )

        prior_coordinates = _operator_current_coordinate_validation_context(
            ledger, locality_identity=binding.locality_identity
        )
        if prior_coordinates is None:
            from seed_runtime.operator_current_coordinates import (
                read_operator_current_coordinates_through,
            )

            prior_coordinates = read_operator_current_coordinates_through(
                ledger,
                locality_identity=binding.locality_identity,
                through_event_occurrence_identity=through_event_occurrence_identity,
            )
    pair_validation_coordinates = (
        prior_coordinates
        if type(prior_coordinates.get("subject_to_act_binding_occurrences"))
        is dict
        else None
    )
    pair_subject = _references_to_recorded_recurrent_byte_pairs(
        ledger,
        measurement_occurrence_identity=pair_reference[
            "recorded_occurrence_identity"
        ],
        recurrence_assertion_positions=(pair_reference["assertion_position"],),
        prior_coordinates=pair_validation_coordinates,
    )[0]
    finding = _measure_through(
        ledger,
        pair_reference=pair_subject,
        source_material_result_occurrence_identity=material[
            "source_material_result_occurrence_identity"
        ],
        boundary=EventLedgerBoundary(material["completeness_boundary_identity"]),
        occurrence_count_boundary=material["occurrence_count_boundary"],
    )
    expected = _binding_material(
        finding,
        through_event_occurrence_identity=material[
            "through_event_occurrence_identity"
        ],
        **identities,
    )
    if (
        binding.locality_identity != finding.source_locality_identity
        or material != expected
    ):
        raise ValueError("pair occurrence binding coordinates are not exact")
    measurements = prior_coordinates.get("measurement_occurrences")
    material_results = prior_coordinates.get("material_result_occurrences")
    carried_bindings = prior_coordinates.get(
        "subject_to_act_binding_occurrences"
    )
    prior_boundary_identity = prior_coordinates.get(
        "through_event_occurrence_identity"
    )
    # Every current-coordinate read crosses at least one ledger read. Bind the two
    # addressed inputs to their intact occurrence coordinates instead of
    # trusting shaped membership, whether the carrier came from the bounded
    # replay context or one family-private same-call reading.
    pair_occurrence_identity = (
        finding.pair_reference.recorded_occurrence_identity
    )
    exact_measurement_occurrence = (
        _exact_measurement_occurrence_coordinates(
            ledger, pair_occurrence_identity
        )
    )
    exact_material_result_occurrence = _exact_material_result_availability_coordinates(
        ledger, finding.source_material_result_occurrence_identity
    )
    from seed_runtime.material_source import (
        read_material_locality_relation_requirements,
    )
    source_has_exact_locality = all(
        read_material_locality_relation_requirements(
            ledger,
            recorded_result_event_identity=(
                finding.source_material_result_occurrence_identity
            ),
        ).values()
    )
    carried_material_result_occurrences = (
        [
            occurrence
            for occurrence in material_results
            if type(occurrence) is dict
            and occurrence.get("result_occurrence_identity")
            == finding.source_material_result_occurrence_identity
        ]
        if type(material_results) is list
        else []
    )
    if (
        type(measurements) is not dict
        or measurements.get(pair_occurrence_identity, object())
        != exact_measurement_occurrence
        or carried_material_result_occurrences != [exact_material_result_occurrence]
        or not source_has_exact_locality
    ):
        raise ValueError(
            "pair occurrence binding has no exact prior coordinates"
        )
    boundary_is_exact = (
        prior_boundary_identity == through_event_occurrence_identity
    )
    binding_is_carried_later = bool(
        type(prior_boundary_identity) is str
        and prior_boundary_identity
        and type(carried_bindings) is dict
        and carried_bindings.get(binding.identity, object()) is None
    )
    if (
        prior_coordinates.get("locality_identity") != binding.locality_identity
        or not (boundary_is_exact or binding_is_carried_later)
        or type(measurements) is not dict
        or finding.pair_reference.recorded_occurrence_identity not in measurements
        or type(material_results) is not list
        or not any(
            type(occurrence) is dict
            and occurrence.get("result_occurrence_identity")
            == finding.source_material_result_occurrence_identity
            for occurrence in material_results
        )
        or not source_has_exact_locality
    ):
        raise ValueError("pair occurrence binding has no exact prior coordinates")
    order = (
        (through_event_occurrence_identity, binding.identity)
        if boundary_is_exact or prior_boundary_identity == binding.identity
        else (
            through_event_occurrence_identity,
            binding.identity,
            prior_boundary_identity,
        )
    )
    try:
        ledger.occurrences_in_append_order(
            order,
            locality_identity=binding.locality_identity,
        )
    except ValueError as error:
        raise ValueError("pair occurrence binding order is false") from error
    return binding, finding


def get_recurrent_byte_pair_occurrence_position_measurement_subject_to_act_binding(
    ledger: EventLedger, binding_event_identity: str
) -> Event:
    return _read_recurrent_byte_pair_occurrence_position_measurement_binding(
        ledger, binding_event_identity
    )[0]


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
                    finding.source_material_result_occurrence_identity
                )
            },
            "role": "exact material result input",
            "act_occurrence_identity": act_occurrence_identity,
            "applicability": "applicable",
        },
    ]


def _material_of_act_occurrence(
    finding: FindingOfRecurrentBytePairOccurrencePositions,
    *,
    binding: Event,
) -> dict[str, Any]:
    act_identity = binding.material["exact_act_identity"]
    act_occurrence_identity = binding.material["act_occurrence_identity"]
    return {
        "addressed_act_identity": act_identity,
        "act_occurrence_identity": act_occurrence_identity,
        "act": ACT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_MEASUREMENT,
        "subject_to_act_binding_reference": _binding_reference(
            binding
        ),
        "measurement_rule": RULE_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_MEASUREMENT,
        "source_localities": [finding.source_locality_identity],
        "completeness_boundary": {
            "identity": finding.completeness_boundary.identity,
        },
        "pair_assertion_reference": finding.pair_reference.assertion_reference,
        "source_material_result_occurrence_identity": (
            finding.source_material_result_occurrence_identity
        ),
        "occurrence_count_boundary": finding.occurrence_count_boundary,
        "participation": _participation_in_measurement(
            finding,
            act_occurrence_identity=act_occurrence_identity,
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
        recurrence_assertion_position=(
            finding.pair_reference.recurrence_assertion_position
        ),
    )
    exact = _measure_through(
        ledger,
        pair_reference=pair_reference,
        source_material_result_occurrence_identity=finding.source_material_result_occurrence_identity,
        boundary=finding.completeness_boundary,
        occurrence_count_boundary=finding.occurrence_count_boundary,
    )
    if exact != finding:
        raise ValueError("pair occurrence finding differs from its exact inputs")


def record_act_occurrence_for_measurement_of_recurrent_byte_pair_occurrence_position(
    ledger: EventLedger,
    *,
    subject_to_act_binding_event_identity: str,
    current_coordinates: dict[str, Any],
) -> Event:
    """Record the responsible Measurement Act before its Yield and result."""

    binding, finding = _read_recurrent_byte_pair_occurrence_position_measurement_binding(
        ledger, subject_to_act_binding_event_identity
    )
    _require_current_binding_coordinates(
        ledger,
        finding=finding,
        current_coordinates=current_coordinates,
        required_binding_identity=binding.identity,
    )
    for event in ledger.iter_locality_kind(
        binding.locality_identity,
        RECORDED_ACT_OCCURRENCE_OF_MEASUREMENT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_EVENT,
    ):
        if (
            event.material.get("subject_to_act_binding_reference")
            == _binding_reference(binding)
            or event.material.get("act_occurrence_identity")
            == binding.material["act_occurrence_identity"]
        ):
            raise ValueError("pair occurrence binding already carries an Act")
    return ledger.append(
        RECORDED_ACT_OCCURRENCE_OF_MEASUREMENT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_EVENT,
        _material_of_act_occurrence(
            finding,
            binding=binding,
        ),
        locality_identity=binding.locality_identity,
    )


def _finding_of_measurement_from_act_occurrence(
    ledger: EventLedger,
    act_occurrence: Event,
    *,
    prior_coordinates: dict[str, Any] | None = None,
) -> tuple[Event, FindingOfRecurrentBytePairOccurrencePositions]:
    material = act_occurrence.material
    binding_reference = material.get("subject_to_act_binding_reference")
    if (
        type(binding_reference) is not dict
        or set(binding_reference)
        != {
            "recorded_occurrence_identity",
            "book_clause_identity",
            "exact_act_identity",
            "subject_reference",
            "result_boundary_identity",
        }
    ):
        raise ValueError("pair occurrence Act occurrence carries malformed coordinates")
    binding, finding = _read_recurrent_byte_pair_occurrence_position_measurement_binding(
        ledger,
        binding_reference.get("recorded_occurrence_identity"),
        prior_coordinates=prior_coordinates,
    )
    expected = _material_of_act_occurrence(
        finding, binding=binding
    )
    if (
        act_occurrence.locality_identity != binding.locality_identity
        or binding_reference != _binding_reference(binding)
        or material != expected
    ):
        raise ValueError("pair occurrence Act occurrence carries no exact binding")
    return binding, finding


def _position_assertions_of_measurement(finding: FindingOfRecurrentBytePairOccurrencePositions) -> list[dict[str, Any]]:
    scope = {"source_localities": [finding.source_locality_identity]}
    subject = {
        "pair_assertion_reference": finding.pair_reference.assertion_reference,
        "source_material_result_occurrence_identity": (
            finding.source_material_result_occurrence_identity
        ),
        "measurement_rule": RULE_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_MEASUREMENT,
    }
    assertions = []
    for assertion_position, (first_position, second_position) in enumerate(
        finding.occurrences
    ):
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
                    "position": assertion_position,
                    "content": content,
                    "source_provenance": (
                        "the exact Yield-carried pair Assertion and later material result"
                    ),
                },
                "result": "position",
                "assertion_subject": subject,
                "assertion_scope": scope,
                "input_support": {
                    "assertion_references": [
                        finding.pair_reference.assertion_reference
                    ],
                    "occurrence_references": [
                        finding.source_material_result_occurrence_identity
                    ],
                    "local_assertion_references": [],
                },
                "conflicts": "Unknown",
                "unknown": [],
            }
        )
    return assertions


def _material_of_result_of_measurement(
    finding: FindingOfRecurrentBytePairOccurrencePositions,
    *,
    binding: Event,
) -> dict[str, Any]:
    known_loss = (
        ["pair occurrences beyond the exact occurrence count boundary are not carried"]
        if finding.available_occurrence_count > len(finding.occurrences)
        else []
    )
    return {
        "result_identity": binding.material["measurement_result_identity"],
        "dimensions": {
            "identity": "recurrent-byte-pair-occurrence-position-measurement",
            "content": "exact ordered pair occurrence position Assertions",
            "source_provenance": (
                "one recurrence Assertion carried by Yield relation and one later "
                "exact material result"
            ),
        },
        "exact_act": ACT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_MEASUREMENT,
        "addressed_act_identity": binding.material["exact_act_identity"],
        "act_occurrence_identity": binding.material["act_occurrence_identity"],
        "subject_to_act_binding_reference": _binding_reference(
            binding
        ),
        "measurement_rule": RULE_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_MEASUREMENT,
        "source_localities": [finding.source_locality_identity],
        "completeness_boundary": {
            "identity": finding.completeness_boundary.identity,
        },
        "pair_assertion_reference": finding.pair_reference.assertion_reference,
        "source_material_result_occurrence_identity": (
            finding.source_material_result_occurrence_identity
        ),
        "occurrence_count_boundary": finding.occurrence_count_boundary,
        "available_occurrence_count": finding.available_occurrence_count,
        "known_loss": known_loss,
        "assertions": _position_assertions_of_measurement(finding),
    }


def record_result_of_measurement_of_recurrent_byte_pair_occurrence_position(
    ledger: EventLedger,
    *,
    act_occurrence_event_identity: str,
) -> Event:
    """Record the Yield and result for one exact pair occurrence Measurement."""

    if (
        type(act_occurrence_event_identity) is not str
        or not act_occurrence_event_identity
    ):
        raise ValueError("pair occurrence result requires exact Act occurrence")
    act_occurrence = ledger.get(act_occurrence_event_identity)
    if (
        act_occurrence is None
        or act_occurrence.kind != RECORDED_ACT_OCCURRENCE_OF_MEASUREMENT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_EVENT
        or type(act_occurrence.locality_identity) is not str
        or not act_occurrence.locality_identity
        or ledger.integrity_of(act_occurrence.identity) == CORRUPTED
    ):
        raise ValueError("pair occurrence result requires intact Act occurrence")
    binding, finding = _finding_of_measurement_from_act_occurrence(
        ledger, act_occurrence
    )
    expected_act = _material_of_act_occurrence(
        finding, binding=binding
    )
    if act_occurrence.material != expected_act:
        raise ValueError(
            "pair occurrence result differs from its exact Act occurrence"
        )
    act_occurrence_identity = act_occurrence.material["act_occurrence_identity"]
    for event in ledger.list_locality(act_occurrence.locality_identity):
        if event.kind in {
            RECORDED_YIELD_RELATION_EVENT,
            RECORDING_OCCURRENCE_OF_RESULT_OF_MEASUREMENT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_KIND,
        } and (
            event.material.get("act_occurrence_identity")
            == act_occurrence.identity
            or event.material.get("act_occurrence_identity")
            == act_occurrence_identity
            or event.material.get("dimensions", {}).get("act_occurrence_identity")
            == act_occurrence_identity
        ):
            raise ValueError("pair occurrence Measurement Act already has a result")
    result = _material_of_result_of_measurement(
        finding, binding=binding
    )
    yield_relation = _record_yield_relation(
        ledger,
        locality_identity=act_occurrence.locality_identity,
        exact_act=ACT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_MEASUREMENT,
        act_occurrence_identity=act_occurrence_identity,
        act_occurrence_event_identity=act_occurrence.identity,
        result_kind=RESULT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_MEASUREMENT_KIND,
        result_identity=result["result_identity"],
        result_content=result,
        occurrence_boundary="measurement_of_recurrent_byte_pair_occurrence_position",
    )
    return ledger.append(
        RECORDING_OCCURRENCE_OF_RESULT_OF_MEASUREMENT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_KIND,
        {
            "result_identity": result["result_identity"],
            "dimensions": result["dimensions"],
            "exact_act": result["exact_act"],
            "addressed_act_identity": result["addressed_act_identity"],
            "act_occurrence_identity": result["act_occurrence_identity"],
            "subject_to_act_binding_reference": result[
                "subject_to_act_binding_reference"
            ],
            "measurement_rule": result["measurement_rule"],
            "source_localities": result["source_localities"],
            "completeness_boundary": result["completeness_boundary"],
            "pair_assertion_reference": result["pair_assertion_reference"],
            "source_material_result_occurrence_identity": result[
                "source_material_result_occurrence_identity"
            ],
            "occurrence_count_boundary": result["occurrence_count_boundary"],
            "available_occurrence_count": result[
                "available_occurrence_count"
            ],
            "known_loss": result["known_loss"],
            "assertions": result["assertions"],
            "act_occurrence_event_identity": act_occurrence.identity,
            "yield_relation_identity": yield_relation.identity,
        },
        locality_identity=act_occurrence.locality_identity,
    )


def _recorded_result_of_recurrent_pair_position_measurement_reading(
    ledger: EventLedger,
    event_identity: str,
    *,
    prior_coordinates: dict[str, Any] | None = None,
) -> tuple[Event, FindingOfRecurrentBytePairOccurrencePositions]:
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
        "act_occurrence_identity",
        "act_occurrence_event_identity",
        "yield_relation_identity",
    }:
        raise ValueError("pair occurrence result carries malformed coordinates")
    act_occurrence_event_identity = material.get("act_occurrence_event_identity")
    act_occurrence = (
        ledger.get(act_occurrence_event_identity)
        if type(act_occurrence_event_identity) is str
        else None
    )
    if (
        act_occurrence is None
        or act_occurrence.kind != RECORDED_ACT_OCCURRENCE_OF_MEASUREMENT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_EVENT
        or act_occurrence.locality_identity != event.locality_identity
        or ledger.integrity_of(act_occurrence.identity) == CORRUPTED
    ):
        raise ValueError("pair occurrence result carries no exact Act occurrence")
    binding, finding = _finding_of_measurement_from_act_occurrence(
        ledger, act_occurrence, prior_coordinates=prior_coordinates
    )
    expected_act = _material_of_act_occurrence(
        finding, binding=binding
    )
    if act_occurrence.material != expected_act:
        raise ValueError(
            "pair occurrence result differs from its exact Act occurrence"
        )
    result = _material_of_result_of_measurement(
        finding, binding=binding
    )
    carried = {
        key: value
        for key, value in material.items()
        if key
        not in {
            "act_occurrence_event_identity",
            "yield_relation_identity",
        }
    }
    if carried != result:
        raise ValueError("pair occurrence result differs from its exact finding")
    requirements = read_requirements_of_yield_relation(
        ledger,
        recorded_result_event_identity=event.identity,
        yield_relation_event_identity=material.get("yield_relation_identity"),
        act_occurrence_event_identity=act_occurrence.identity,
    )
    yield_relation = ledger.get(material.get("yield_relation_identity"))
    if (
        not all(requirements.values())
        or yield_relation is None
        or yield_relation.material.get("occurrence_boundary")
        != MEASUREMENT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_BOUNDARY
        or yield_relation.material.get("result_kind")
        != RESULT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_MEASUREMENT_KIND
    ):
        raise ValueError("pair occurrence result carries no exact Yield relation")
    return event, finding


def _read_recorded_result_of_measurement_of_recurrent_byte_pair_occurrence_position(
    ledger: EventLedger,
    event_identity: str,
    *,
    prior_coordinates: dict[str, Any] | None = None,
) -> FindingOfRecurrentBytePairOccurrencePositions:
    return _recorded_result_of_recurrent_pair_position_measurement_reading(
        ledger,
        event_identity,
        prior_coordinates=prior_coordinates,
    )[1]


def get_recorded_result_of_measurement_of_recurrent_byte_pair_occurrence_position(
    ledger: EventLedger,
    event_identity: str,
) -> FindingOfRecurrentBytePairOccurrencePositions:
    """Read one pair-occurrence result through its exact Act and Yield."""

    return _read_recorded_result_of_measurement_of_recurrent_byte_pair_occurrence_position(
        ledger, event_identity
    )


def _references_from_recorded_recurrent_pair_position_result(
    event: Event,
    finding: FindingOfRecurrentBytePairOccurrencePositions,
    *,
    assertion_positions: tuple[int, ...] | None = None,
) -> tuple[ReferenceToRecordedRecurrentBytePairOccurrencePosition, ...]:
    assertions = event.material["assertions"]
    if len(assertions) != len(finding.occurrences):
        raise ValueError("pair-position result carries a different Assertion population")
    references = []
    for assertion_position, (assertion, (first_position, second_position)) in enumerate(
        zip(assertions, finding.occurrences)
    ):
        if assertion.get("dimensions", {}).get("position") != assertion_position:
            raise ValueError("pair-position result carries no exact Assertion position")
        references.append(
            ReferenceToRecordedRecurrentBytePairOccurrencePosition(
                recorded_occurrence_identity=event.identity,
                assertion_position=assertion_position,
                pair_measurement_occurrence_identity=(
                    finding.pair_reference.recorded_occurrence_identity
                ),
                recurrence_assertion_position=(
                    finding.pair_reference.recurrence_assertion_position
                ),
                count_assertion_position=(
                    finding.pair_reference.count_assertion_position
                ),
                source_material_result_occurrence_identity=(
                    finding.source_material_result_occurrence_identity
                ),
                locality_identity=finding.source_locality_identity,
                completeness_boundary_identity=(
                    finding.completeness_boundary.identity
                ),
                exact_pair=finding.pair_reference.exact_material,
                first_position=first_position,
                second_position=second_position,
            )
        )
    if assertion_positions is None:
        return tuple(references)
    if (
        type(assertion_positions) is not tuple
        or any(type(position) is not int or position < 0 for position in assertion_positions)
        or len(set(assertion_positions)) != len(assertion_positions)
    ):
        raise ValueError("pair-position references require exact Assertion positions")
    by_position = {reference.assertion_position: reference for reference in references}
    if any(position not in by_position for position in assertion_positions):
        raise ValueError("pair-position result carries no addressed Assertion")
    return tuple(by_position[position] for position in assertion_positions)


def _recurrent_pair_position_result_lifecycle_boundary(
    ledger: EventLedger,
    result_occurrence_identity: str,
) -> tuple[str, str]:
    if type(result_occurrence_identity) is not str or not result_occurrence_identity:
        raise ValueError("pair-position references require one exact result occurrence")
    result = ledger.get(result_occurrence_identity)
    if (
        result is None
        or result.kind
        != RECORDING_OCCURRENCE_OF_RESULT_OF_MEASUREMENT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_KIND
        or type(result.locality_identity) is not str
        or not result.locality_identity
        or ledger.integrity_of(result.identity) == CORRUPTED
    ):
        raise ValueError("pair-position result is absent or corrupted")
    act_identity = result.material.get("act_occurrence_event_identity")
    act = ledger.get(act_identity) if type(act_identity) is str else None
    if (
        act is None
        or act.kind
        != RECORDED_ACT_OCCURRENCE_OF_MEASUREMENT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_EVENT
        or act.locality_identity != result.locality_identity
        or ledger.integrity_of(act.identity) == CORRUPTED
    ):
        raise ValueError("pair-position result carries no exact Act occurrence")
    binding_reference = act.material.get("subject_to_act_binding_reference")
    binding_identity = (
        binding_reference.get("recorded_occurrence_identity")
        if type(binding_reference) is dict
        else None
    )
    binding = (
        ledger.get(binding_identity)
        if type(binding_identity) is str
        else None
    )
    if (
        binding is None
        or binding.kind
        != RECORDED_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_MEASUREMENT_SUBJECT_TO_ACT_BINDING_KIND
        or binding.locality_identity != result.locality_identity
        or ledger.integrity_of(binding.identity) == CORRUPTED
    ):
        raise ValueError("pair-position result carries no exact binding")
    boundary_identity = binding.material.get(
        "through_event_occurrence_identity"
    )
    if type(boundary_identity) is not str or not boundary_identity:
        raise ValueError("pair-position binding carries no exact through-occurrence")
    try:
        ordered = tuple(
            dict.fromkeys(
                (
                    boundary_identity,
                    binding.identity,
                    act.identity,
                    result.identity,
                )
            )
        )
        resolved = ledger.occurrences_in_append_order(
            ordered,
            locality_identity=result.locality_identity,
        )
    except (TypeError, ValueError) as error:
        raise ValueError("pair-position result lifecycle order is false") from error
    if tuple(event.identity for event in resolved) != ordered:
        raise ValueError("pair-position result lifecycle order is false")
    return boundary_identity, result.locality_identity


def _references_to_addressed_recorded_recurrent_pair_position_results(
    ledger: EventLedger,
    *,
    result_and_assertion_positions: tuple[
        tuple[str, int], tuple[str, int]
    ],
    prior_coordinates: dict[str, Any] | None = None,
) -> tuple[
    ReferenceToRecordedRecurrentBytePairOccurrencePosition,
    ReferenceToRecordedRecurrentBytePairOccurrencePosition,
]:
    """Address two distinct results through one exact current-coordinate read."""

    if not isinstance(ledger, EventLedger):
        raise TypeError("pair-position references require one EventLedger")
    if (
        type(result_and_assertion_positions) is not tuple
        or len(result_and_assertion_positions) != 2
        or any(
            type(address) is not tuple
            or len(address) != 2
            or type(address[0]) is not str
            or not address[0]
            or type(address[1]) is not int
            or address[1] < 0
            for address in result_and_assertion_positions
        )
        or result_and_assertion_positions[0][0]
        == result_and_assertion_positions[1][0]
    ):
        raise ValueError("two distinct pair-position results must be addressed")
    lifecycle_boundaries = tuple(
        _recurrent_pair_position_result_lifecycle_boundary(
            ledger, result_identity
        )
        for result_identity, _assertion_position in result_and_assertion_positions
    )
    localities = tuple(locality for _boundary, locality in lifecycle_boundaries)
    if localities[0] != localities[1]:
        raise ValueError("addressed pair-position results require one exact Locality")
    boundaries = tuple(boundary for boundary, _locality in lifecycle_boundaries)
    if boundaries[0] == boundaries[1]:
        later_boundary = boundaries[0]
    else:
        later_boundary = None
        for ordered_boundaries in (boundaries, tuple(reversed(boundaries))):
            try:
                resolved = ledger.occurrences_in_append_order(
                    ordered_boundaries,
                    locality_identity=localities[0],
                )
            except (TypeError, ValueError):
                continue
            if tuple(event.identity for event in resolved) == ordered_boundaries:
                later_boundary = ordered_boundaries[1]
                break
        if later_boundary is None:
            raise ValueError(
                "addressed pair-position through-occurrences cannot be ordered in one Locality"
            )
    if prior_coordinates is None:
        from seed_runtime.operator_current_coordinates import (
            read_operator_current_coordinates_through,
        )

        prior_coordinates = read_operator_current_coordinates_through(
            ledger,
            locality_identity=localities[0],
            through_event_occurrence_identity=later_boundary,
        )
    elif type(prior_coordinates) is not dict:
        raise ValueError("addressed pair-position results require exact prior coordinates")
    addressed = []
    for result_identity, assertion_position in result_and_assertion_positions:
        event, finding = (
            _recorded_result_of_recurrent_pair_position_measurement_reading(
                ledger,
                result_identity,
                prior_coordinates=prior_coordinates,
            )
        )
        addressed.append(
            _references_from_recorded_recurrent_pair_position_result(
                event,
                finding,
                assertion_positions=(assertion_position,),
            )[0]
        )
    return addressed[0], addressed[1]


def references_to_recorded_recurrent_byte_pair_occurrence_positions(
    ledger: EventLedger,
    *,
    result_occurrence_identity: str,
) -> tuple[ReferenceToRecordedRecurrentBytePairOccurrencePosition, ...]:
    """Read one intact result and address each exact position Assertion once."""

    if not isinstance(ledger, EventLedger):
        raise TypeError("pair-position references require one EventLedger")
    if (
        type(result_occurrence_identity) is not str
        or not result_occurrence_identity
    ):
        raise ValueError("pair-position references require one exact result occurrence")
    finding = (
        get_recorded_result_of_measurement_of_recurrent_byte_pair_occurrence_position(
            ledger, result_occurrence_identity
        )
    )
    event = ledger.get(result_occurrence_identity)
    if event is None:
        raise ValueError("pair-position result disappeared after validation")
    return _references_from_recorded_recurrent_pair_position_result(
        event, finding
    )
