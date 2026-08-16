"""Measure ordered pairs at exact positions."""

from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Iterable, Sequence

from seed_runtime.events import CORRUPTED, EventLedger, EventLedgerBoundary
from seed_runtime.event import Event
from seed_runtime.identities import new_identity
from seed_runtime.yield_evidence import _record_yield_evidence
from seed_runtime.preserved_material_measurement import (
    INGEST_OCCURRED_KIND,
    MEASUREMENT_RECORDED_KIND,
    DeclaredMeasurement,
    MeasurementFinding,
    RepresentationCount,
    PreservedMaterialMeasurementError,
    measurement_input_occurrences,
    measure_position_representations,
)
from seed_runtime.operator_representation import (
    REPRESENTATION_EMITTED_KIND,
    REPRESENTATION_EMISSION_LOCALITY_EVIDENCE_KIND,
)

EQUIVALENCE_RULE = "byte-for-byte equality; no normalization"

MEASURED_POSITION: dict[str, int] = {"difference": 1}
POSITION_PAIR_MEASUREMENT_RECORDED_KIND = (
    "operator.measurement.position_pair_measurement_recorded"
)
POSITION_PAIR_MEASUREMENT_ACT_EVIDENCE_KIND = (
    "operator.measurement.position_pair_measurement_act_evidenced"
)
POSITION_PAIR_MEASUREMENT_LOCALITY_EVIDENCE_KIND = (
    "operator.measurement.position_pair_measurement_locality_evidenced"
)
POSITION_PAIR_MEASUREMENT_COMPARE_RECORDED_KIND = (
    "operator.measurement.position_pair_measurement_compare_recorded"
)
POSITION_PAIR_MEASUREMENT_COMPARE_ACT_EVIDENCE_KIND = (
    "operator.measurement.position_pair_measurement_compare_act_evidenced"
)
POSITION_PAIR_MEASUREMENT_COMPARE_LOCALITY_EVIDENCE_KIND = (
    "operator.measurement.position_pair_measurement_compare_locality_evidenced"
)
EVENT_KIND_RESPONSIBILITIES = {
    POSITION_PAIR_MEASUREMENT_RECORDED_KIND: "02.Acts.A",
    POSITION_PAIR_MEASUREMENT_ACT_EVIDENCE_KIND: "02.Acts.A",
    POSITION_PAIR_MEASUREMENT_LOCALITY_EVIDENCE_KIND: "06.Standing.B",
    POSITION_PAIR_MEASUREMENT_COMPARE_RECORDED_KIND: "02.Acts.A",
    POSITION_PAIR_MEASUREMENT_COMPARE_ACT_EVIDENCE_KIND: "02.Acts.A",
    POSITION_PAIR_MEASUREMENT_COMPARE_LOCALITY_EVIDENCE_KIND: "06.Standing.B",
}
POSITION_PAIR_MEASUREMENT_RESPONSIBILITY = (
    "establish one position before and one position after every exact occurrence "
    "of each ordered pair read from one exact finding"
)
PAIR_FINDING_PARTICIPATION_ROLE = "read ordered-pair finding"
SOURCE_OCCURRENCE_PARTICIPATION_ROLE = "exact preserved source occurrence"
EMISSION_LOCALITY_PARTICIPATION_ROLE = "exact emission Locality Evidence"
EMISSION_OCCURRENCE_PARTICIPATION_ROLE = "exact emission occurrence"
MEASUREMENT_COMPARE_INPUT_ROLE = "exact recorded position-pair measurements"
POSITION_PAIR_MEASUREMENT_COMPARE_RESPONSIBILITY = (
    "compare exact recorded position-pair measurements without identifying "
    "equal representations as equal occurrences or relations"
)


@dataclass(frozen=True)
class PositionPair:
    """Two representations in exact order."""

    first: str
    second: str

    def __post_init__(self) -> None:
        if not isinstance(self.first, str) or not isinstance(self.second, str):
            raise PreservedMaterialMeasurementError("a pair is a pair of representations")
        if not self.first or not self.second:
            raise PreservedMaterialMeasurementError("a pair's representations must be exact")

    def __str__(self) -> str:  # pragma: no cover - representation only
        return f"{self.first!r} -> {self.second!r}"


@dataclass(frozen=True)
class PositionedRepresentationOccurrence:
    """One exact representation position inside one preserved occurrence."""

    source_occurrence_identity: str
    position: int
    representation: str

    @property
    def identity(self) -> tuple[str, int]:
        return (self.source_occurrence_identity, self.position)


@dataclass(frozen=True)
class ExactPositionPairOccurrence:
    """One exact occurrence of an already-read ordered position pair."""

    pair: PositionPair
    first: PositionedRepresentationOccurrence
    second: PositionedRepresentationOccurrence

    def __post_init__(self) -> None:
        if self.first.source_occurrence_identity != self.second.source_occurrence_identity:
            raise PreservedMaterialMeasurementError(
                "a position pair occurrence cannot cross source occurrences"
            )
        if self.second.position != self.first.position + 1:
            raise PreservedMaterialMeasurementError(
                "a position pair occurrence requires the second position to equal the first position plus one"
            )
        if (
            self.first.representation != self.pair.first
            or self.second.representation != self.pair.second
        ):
            raise PreservedMaterialMeasurementError(
                "a position pair occurrence must carry its exact ordered pair"
            )

    @property
    def identity(self) -> tuple[str, int, int]:
        return (
            self.first.source_occurrence_identity,
            self.first.position,
            self.second.position,
        )


@dataclass(frozen=True)
class PositionPairMeasurement:
    """One position before and after one exact pair occurrence."""

    before_occurrence: PositionedRepresentationOccurrence | None
    pair_occurrence: ExactPositionPairOccurrence
    after_occurrence: PositionedRepresentationOccurrence | None
    source_occurrence_identity: str
    exact_order: tuple[int, ...]
    evidence: dict[str, object]

    def __post_init__(self) -> None:
        source_identity = self.source_occurrence_identity
        if not isinstance(source_identity, str) or not source_identity:
            raise PreservedMaterialMeasurementError(
                "a position-pair measurement requires one exact source occurrence"
            )
        if self.pair_occurrence.first.source_occurrence_identity != source_identity:
            raise PreservedMaterialMeasurementError(
                "the pair occurrence is outside the measured source occurrence"
            )
        expected_order = []
        if self.before_occurrence is not None:
            if (
                self.before_occurrence.source_occurrence_identity != source_identity
                or self.before_occurrence.position
                != self.pair_occurrence.first.position - 1
            ):
                raise PreservedMaterialMeasurementError(
                    "the before occurrence is not one position before the pair"
                )
            expected_order.append(self.before_occurrence.position)
        expected_order.extend(
            (
                self.pair_occurrence.first.position,
                self.pair_occurrence.second.position,
            )
        )
        if self.after_occurrence is not None:
            if (
                self.after_occurrence.source_occurrence_identity != source_identity
                or self.after_occurrence.position
                != self.pair_occurrence.second.position + 1
            ):
                raise PreservedMaterialMeasurementError(
                    "the after occurrence is not one position after the pair"
                )
            expected_order.append(self.after_occurrence.position)
        if self.exact_order != tuple(expected_order):
            raise PreservedMaterialMeasurementError(
                "the carried order does not match the exact measured positions"
            )
        evidence = self.evidence
        finding_identity = evidence.get("position_pair_evidence_event_identity")
        evidence_identities = evidence.get("evidence_occurrence_references")
        text = evidence.get("exact_representation")
        if (
            evidence.get("source_occurrence_identity") != source_identity
            or not isinstance(finding_identity, str)
            or not finding_identity
            or evidence_identities != [finding_identity, source_identity]
            or evidence.get("source_kind")
            not in {
                INGEST_OCCURRED_KIND,
                REPRESENTATION_EMITTED_KIND,
            }
            or not isinstance(evidence.get("locality_identity"), str)
            or not isinstance(text, str)
        ):
            raise PreservedMaterialMeasurementError(
                "the position-pair measurement does not preserve its exact Evidence"
            )
        positions = _positions(text)
        carried = (
            *((self.before_occurrence,) if self.before_occurrence is not None else ()),
            self.pair_occurrence.first,
            self.pair_occurrence.second,
            *((self.after_occurrence,) if self.after_occurrence is not None else ()),
        )
        if any(
            occurrence.position >= len(positions)
            or positions[occurrence.position] != occurrence.representation
            for occurrence in carried
        ):
            raise PreservedMaterialMeasurementError(
                "the measured occurrences do not match the carried source Evidence"
            )

    @property
    def identity(self) -> tuple[str, str, int, int]:
        return (
            self.evidence["position_pair_evidence_event_identity"],
            self.source_occurrence_identity,
            self.pair_occurrence.first.position,
            self.pair_occurrence.second.position,
        )

    @property
    def complete_coordinates(self) -> dict[str, object] | None:
        """Return the neutral coordinates only when both outer positions exist."""

        if self.before_occurrence is None or self.after_occurrence is None:
            return None
        return {
            "identity": {
                "position_pair_evidence_event_identity": self.evidence["position_pair_evidence_event_identity"],
                "source_occurrence_identity": self.source_occurrence_identity,
                "exact_order": list(self.exact_order),
            },
            "before_occurrence": {
                "occurrence": list(self.before_occurrence.identity),
                "representation": self.before_occurrence.representation,
            },
            "pair_occurrence": {
                "occurrence": list(self.pair_occurrence.identity),
                "ordered_pair": [
                    self.pair_occurrence.pair.first,
                    self.pair_occurrence.pair.second,
                ],
            },
            "after_occurrence": {
                "occurrence": list(self.after_occurrence.identity),
                "representation": self.after_occurrence.representation,
            },
            "evidence": dict(self.evidence),
        }



def _position_pairs_from_event(event: Event | None) -> list[PositionPair]:
    if event is None or event.kind != MEASUREMENT_RECORDED_KIND:
        raise PreservedMaterialMeasurementError(
            "pairs must be read from a recorded measurement finding"
        )
    first = event.material.get("relative_representation")
    if not isinstance(first, str) or not first:
        raise PreservedMaterialMeasurementError(
            "the recorded finding does not name the representation it measured after"
        )
    return [
        PositionPair(first=first, second=item["representation"])
        for item in event.material["representation_counts"]
    ]


def _is_established_after_measurement(event: Event) -> bool:

    relative = event.material.get("relative_representation")
    return (
        event.kind == MEASUREMENT_RECORDED_KIND
        and event.material.get("equivalence_rule") == EQUIVALENCE_RULE
        and event.material.get("measurement_distinction") == "position difference"
        and isinstance(relative, str)
        and bool(relative)
        and event.material.get("measured_position") == MEASURED_POSITION
    )


def position_pairs_from_finding(ledger: EventLedger, finding_event_identity: str) -> list[PositionPair]:
    """Read pairs out of a recorded finding rather than taking them from a caller.

    The recorded finding names one relative representation and the representations
    measured after it. Every representation is returned; none is filtered by count
    or share. Which of them prove reproducible is what the
    measurement measures, not something decided here.
    """

    return _position_pairs_from_event(ledger.get(finding_event_identity))


def _positions(text: str) -> Sequence[str]:
    """Whitespace-delimited positions.

    A reader-supplied resolution, recorded as such. `#2391` established that
    the discrimination survives character n-grams too, so this rule is not
    load-bearing; it is legible.
    """

    return text.split()


def _measure_position_pair_measurements(
    occurrences: Iterable[Event],
    pairs: Iterable[PositionPair],
    *,
    position_pair_evidence_event_identity: str,
) -> tuple[PositionPairMeasurement, ...]:
    """Extend every exact pair occurrence one position before and after.

    Pair values select what is measured; they do not assert the resulting
    coordinates. Every measurement is identified by its preserved source
    occurrence and exact positions. Boundary absence is retained as absence,
    rather than dropping the pair occurrence or filling a position.
    """

    bounded_pairs = tuple(dict.fromkeys(pairs))
    measurements: list[PositionPairMeasurement] = []
    for source in occurrences:
        if source.kind == INGEST_OCCURRED_KIND:
            text = source.material.get("represented_material")
        elif source.kind == REPRESENTATION_EMITTED_KIND:
            text = source.material.get("emitted_representation")
        else:
            raise PreservedMaterialMeasurementError(
                f"the source occurrence does not carry represented material: {source.kind}"
            )
        if not isinstance(text, str):
            raise PreservedMaterialMeasurementError(
                f"{source.identity} carries no represented material"
            )
        positions = _positions(text)
        for pair in bounded_pairs:
            for at in range(len(positions) - 1):
                if positions[at] != pair.first or positions[at + 1] != pair.second:
                    continue
                pair_first = PositionedRepresentationOccurrence(
                    source.identity, at, positions[at]
                )
                pair_second = PositionedRepresentationOccurrence(
                    source.identity, at + 1, positions[at + 1]
                )
                before = (
                    PositionedRepresentationOccurrence(
                        source.identity, at - 1, positions[at - 1]
                    )
                    if at > 0
                    else None
                )
                after = (
                    PositionedRepresentationOccurrence(
                        source.identity, at + 2, positions[at + 2]
                    )
                    if at + 2 < len(positions)
                    else None
                )
                exact_order = tuple(
                    position
                    for position in (
                        before.position if before is not None else None,
                        pair_first.position,
                        pair_second.position,
                        after.position if after is not None else None,
                    )
                    if position is not None
                )
                measurements.append(
                    PositionPairMeasurement(
                        before_occurrence=before,
                        pair_occurrence=ExactPositionPairOccurrence(
                            pair=pair,
                            first=pair_first,
                            second=pair_second,
                        ),
                        after_occurrence=after,
                        source_occurrence_identity=source.identity,
                        exact_order=exact_order,
                        evidence={
                            "source_occurrence_identity": source.identity,
                            "position_pair_evidence_event_identity": position_pair_evidence_event_identity,
                            "evidence_occurrence_references": [
                                position_pair_evidence_event_identity,
                                source.identity,
                            ],
                            "source_kind": source.kind,
                            "locality_identity": source.locality_identity,
                            "exact_representation": text,
                        },
                    )
                )
    return tuple(measurements)


def measure_emitted_representation_position_pair(
    ledger: EventLedger,
    *,
    emission_event_identity: str,
) -> tuple[PositionPairMeasurement, ...]:
    """Measure exact position pairs in material carried by one emission occurrence.

    The emission occurrence is admitted only through its exact Locality
    Evidence. Matching text or an emission-shaped event does not establish the
    content-to-occurrence relation.
    """

    emission = ledger.get(emission_event_identity)
    if (
        emission is None
        or emission.kind != REPRESENTATION_EMITTED_KIND
        or ledger.integrity_of(emission_event_identity) == CORRUPTED
    ):
        raise PreservedMaterialMeasurementError(
            "emitted-representation position pair requires one intact emission occurrence"
        )
    text = emission.material.get("emitted_representation")
    locality_identity = emission.material.get("locality_evidence_identity")
    locality = ledger.get(locality_identity) if isinstance(locality_identity, str) else None
    if (
        not isinstance(text, str)
        or locality is None
        or locality.kind != REPRESENTATION_EMISSION_LOCALITY_EVIDENCE_KIND
        or ledger.integrity_of(locality.identity) == CORRUPTED
        or locality.locality_identity != emission.locality_identity
        or locality.material.get("act_occurrence_identity")
        != emission.material.get("act_occurrence_identity")
        or locality.material.get("content_kind") != "text"
        or locality.material.get("carried_content") != text
    ):
        raise PreservedMaterialMeasurementError(
            "the emission does not preserve exact Locality Evidence for its representation"
        )
    positions = _positions(text)
    pairs = tuple(
        dict.fromkeys(
            PositionPair(positions[index], positions[index + 1])
            for index in range(len(positions) - 1)
        )
    )
    return _measure_position_pair_measurements(
        (emission,),
        pairs,
        position_pair_evidence_event_identity=locality.identity,
    )


def compare_emitted_representation_position_pair(
    ledger: EventLedger,
    *,
    emission_event_identities: Iterable[str],
) -> dict[str, object]:
    """Compare exact positional measurements from distinct emissions."""

    identities = tuple(emission_event_identities)
    if (
        len(identities) < 2
        or any(not isinstance(identity, str) or not identity for identity in identities)
        or len(set(identities)) != len(identities)
    ):
        raise PreservedMaterialMeasurementError(
            "emission position pair Compare requires at least two distinct exact emission occurrences"
        )
    measurements = tuple(
        measurement
        for identity in identities
        for measurement in measure_emitted_representation_position_pair(
            ledger,
            emission_event_identity=identity,
        )
    )
    return compare_position_pair_measurements(measurements)


def record_emitted_representation_position_pair(
    ledger: EventLedger,
    *,
    emission_event_identity: str,
) -> Event:
    """Preserve exact position pairs measured through one emission Locality."""

    emission = ledger.get(emission_event_identity)
    measurements = measure_emitted_representation_position_pair(
        ledger,
        emission_event_identity=emission_event_identity,
    )
    assert emission is not None
    locality_identity = emission.material["locality_evidence_identity"]
    return _record_position_pair_measurement_result(
        ledger,
        locality_identity=emission.locality_identity,
        position_pair_evidence_event_identity=locality_identity,
        source_identities=(emission.identity,),
        measurements=measurements,
        applicable_inputs=[
            {
                "input_reference": locality_identity,
                "role": EMISSION_LOCALITY_PARTICIPATION_ROLE,
                "standing": "applicable",
            },
            {
                "input_reference": emission.identity,
                "role": EMISSION_OCCURRENCE_PARTICIPATION_ROLE,
                "standing": "applicable",
            },
        ],
    )


def measure_position_pairs_from_finding(
    ledger: EventLedger,
    *,
    finding_event_identity: str,
    occurrences: Iterable[Event],
) -> tuple[PositionPairMeasurement, ...]:
    """Measure only position pairs read from one recorded finding."""

    finding = ledger.get(finding_event_identity)
    if finding is None or ledger.integrity_of(finding_event_identity) == CORRUPTED:
        raise PreservedMaterialMeasurementError(
            "position pairs require one intact recorded finding"
        )
    if not _is_established_after_measurement(finding):
        raise PreservedMaterialMeasurementError(
            "position-pair measurements require an exact recorded position difference of one"
        )
    material = tuple(occurrences)
    recorded_occurrences = measurement_input_occurrences(finding.material)
    if tuple(event.identity for event in material) != recorded_occurrences:
        raise PreservedMaterialMeasurementError(
            "the supplied source occurrences differ from the finding's exact Evidence"
        )
    for event in material:
        recorded = ledger.get(event.identity)
        if (
            recorded is None
            or recorded.kind != INGEST_OCCURRED_KIND
            or recorded.locality_identity != finding.locality_identity
            or recorded.locality_identity != event.locality_identity
            or recorded.material != event.material
        ):
            raise PreservedMaterialMeasurementError(
                "the finding's source-occurrence Evidence does not read"
            )
    pairs = _position_pairs_from_event(finding)
    return _measure_position_pair_measurements(
        material,
        pairs,
        position_pair_evidence_event_identity=finding_event_identity,
    )


def compare_position_pair_measurements(
    measurements: Iterable[PositionPairMeasurement],
) -> dict[str, object]:
    """Report only distinctions that survive exact occurrence counterexamples.

    Representation equality is counted for comparison but never used as
    occurrence identity. The result reports only measured differences.
    """

    bounded = tuple(measurements)
    if not all(isinstance(item, PositionPairMeasurement) for item in bounded):
        raise PreservedMaterialMeasurementError(
            "position-pair measurement Compare requires exact bounded measurements"
        )
    identities = [measurement.identity for measurement in bounded]
    if len(set(identities)) != len(identities):
        raise PreservedMaterialMeasurementError(
            "the same exact position-pair measurement was supplied more than once"
        )
    complete = tuple(
        coordinates
        for measurement in bounded
        if (coordinates := measurement.complete_coordinates) is not None
    )
    representation_coordinates: dict[
        tuple[str, tuple[str, str], str], list[dict[str, object]]
    ] = {}
    pair_coordinates: dict[tuple[str, str], list[dict[str, object]]] = {}
    endpoint_coordinates: dict[tuple[str, str], list[dict[str, object]]] = {}
    for coordinates in complete:
        before = coordinates["before_occurrence"]["representation"]
        pair = tuple(coordinates["pair_occurrence"]["ordered_pair"])
        after = coordinates["after_occurrence"]["representation"]
        representation_coordinates.setdefault((before, pair, after), []).append(
            coordinates
        )
        pair_coordinates.setdefault(pair, []).append(coordinates)
        endpoint_coordinates.setdefault((before, after), []).append(coordinates)

    return {
        "measurement_count": len(bounded),
        "complete_measurement_count": len(complete),
        "boundary_measurement_count": len(bounded) - len(complete),
        "distinct_complete_occurrence_count": len(
            {
                (
                    coordinates["identity"]["position_pair_evidence_event_identity"],
                    coordinates["identity"]["source_occurrence_identity"],
                    tuple(coordinates["identity"]["exact_order"]),
                )
                for coordinates in complete
            }
        ),
        "distinct_representation_coordinate_count": len(representation_coordinates),
        "counterexamples": {
            "equal_representation_coordinates_distinct_occurrence_count": sum(
                len(occurrences) > 1
                for occurrences in representation_coordinates.values()
            ),
            "equal_ordered_pair_distinct_endpoint_representation_count": sum(
                len(
                    {
                        (
                            coordinates["before_occurrence"]["representation"],
                            coordinates["after_occurrence"]["representation"],
                        )
                        for coordinates in occurrences
                    }
                )
                > 1
                for occurrences in pair_coordinates.values()
            ),
            "equal_endpoint_representations_distinct_ordered_pair_count": sum(
                len(
                    {
                        tuple(coordinates["pair_occurrence"]["ordered_pair"])
                        for coordinates in occurrences
                    }
                )
                > 1
                for occurrences in endpoint_coordinates.values()
            ),
        },
        "distinct_position_pair_coordinates": [
            {
                "before_present": before_present,
                "after_present": after_present,
                "exact_order_difference": list(differences),
            }
            for before_present, after_present, differences in sorted(
                {
                    (
                        measurement.before_occurrence is not None,
                        measurement.after_occurrence is not None,
                        tuple(
                            later - earlier
                            for earlier, later in zip(
                                measurement.exact_order,
                                measurement.exact_order[1:],
                            )
                        ),
                    )
                    for measurement in bounded
                }
            )
        ],
    }


def _position_pair_measurement_material(
    measurement: PositionPairMeasurement,
) -> dict[str, object]:
    def positioned(
        occurrence: PositionedRepresentationOccurrence | None,
    ) -> dict[str, object] | None:
        if occurrence is None:
            return None
        return {
            "source_occurrence_identity": occurrence.source_occurrence_identity,
            "position": occurrence.position,
            "representation": occurrence.representation,
        }

    return {
        "before_occurrence": positioned(measurement.before_occurrence),
        "pair_occurrence": {
            "ordered_pair": [
                measurement.pair_occurrence.pair.first,
                measurement.pair_occurrence.pair.second,
            ],
            "first": positioned(measurement.pair_occurrence.first),
            "second": positioned(measurement.pair_occurrence.second),
        },
        "after_occurrence": positioned(measurement.after_occurrence),
        "source_occurrence_identity": measurement.source_occurrence_identity,
        "exact_order": list(measurement.exact_order),
        "evidence": dict(measurement.evidence),
    }


def _record_position_pair_measurement_result(
    ledger: EventLedger,
    *,
    locality_identity: str,
    position_pair_evidence_event_identity: str,
    source_identities: tuple[str, ...],
    measurements: tuple[PositionPairMeasurement, ...],
    applicable_inputs: list[dict[str, str]],
) -> Event:
    act_identity = new_identity("position_pair_measurement_measurement_act")
    act_occurrence_identity = new_identity("position_pair_measurement_measurement_occurrence")
    result_identity = f"position-pair-measurement-result:{act_occurrence_identity}"
    result_material = {
        "result_identity": result_identity,
        "position_pair_evidence_event_identity": position_pair_evidence_event_identity,
        "source_occurrence_references": list(source_identities),
        "measurements": [
            _position_pair_measurement_material(measurement)
            for measurement in measurements
        ],
    }
    participation = [
        {
            "subject_reference": item["input_reference"],
            "role": item["role"],
            "act_occurrence_identity": act_occurrence_identity,
        }
        for item in applicable_inputs
    ]
    act_evidence = ledger.append(
        POSITION_PAIR_MEASUREMENT_ACT_EVIDENCE_KIND,
        {
            "downstream_act_identity": act_identity,
            "act_occurrence_identity": act_occurrence_identity,
            "act": "exact position-pair measurement Measurement",
            "responsibility": POSITION_PAIR_MEASUREMENT_RESPONSIBILITY,
            "responsible_boundary": "this Seed",
            "input_applicability": applicable_inputs,
            "participation": participation,
            "authority": "unestablished",
            "evidence_scope": "this exact bounded Measurement occurrence only",
        },
        locality_identity=locality_identity,
    )
    yield_evidence = _record_yield_evidence(
        ledger,
        locality_identity=locality_identity,
        exact_act="exact position-pair measurement Measurement",
        act_occurrence_identity=act_occurrence_identity,
        responsible_act_evidence_identity=act_evidence.identity,
        result_kind="exact position-pair measurements",
        result_identity=result_identity,
        result_content=result_material,
        responsibility=POSITION_PAIR_MEASUREMENT_RESPONSIBILITY,
        live_boundary="position_pair_measurement",
        responsible_boundary="this Seed",
    )
    locality_evidence = ledger.append(
        POSITION_PAIR_MEASUREMENT_LOCALITY_EVIDENCE_KIND,
        {
            "act_occurrence_identity": act_occurrence_identity,
            "content_kind": "exact position-pair measurements",
            "carried_content": result_material,
            "authority": "unestablished",
            "evidence_scope": "this exact result-to-occurrence Locality only",
        },
        locality_identity=locality_identity,
    )
    return ledger.append(
        POSITION_PAIR_MEASUREMENT_RECORDED_KIND,
        {
            **result_material,
            "dimensions": {
                "identity": act_occurrence_identity,
                "content": "exact position-pair measurements",
                "source_provenance": [position_pair_evidence_event_identity, *source_identities],
                "responsibility": POSITION_PAIR_MEASUREMENT_RESPONSIBILITY,
                "responsible_boundary": "this Seed",
                "authority": "unestablished",
                "evidence_scope": (
                    "measurement Evidence only; establishes no represented relation "
                    "or Standing beyond this result"
                ),
                "scope_locality": f"locality:{locality_identity}",
                "occurrence_preservation": "one exact position-pair measurement Measurement occurrence recorded",
            },
            "downstream_act_identity": act_identity,
            "act_occurrence_identity": act_occurrence_identity,
            "responsible_act_evidence_identity": act_evidence.identity,
            "participation": participation,
            "yield_evidence_identity": yield_evidence.identity,
            "locality_evidence_identity": locality_evidence.identity,
            "known_loss": [],
            "unknowns": [
                "represented relation of any carried Representation remains Unknown"
            ],
            "conflicts": [],
        },
        locality_identity=locality_identity,
    )


def record_position_pair_measurements(
    ledger: EventLedger,
    *,
    locality_identity: str,
    finding_event_identity: str,
) -> Event:
    """Preserve one exact bounded position-pair measurement Measurement result."""

    finding = ledger.get(finding_event_identity)
    if (
        finding is None
        or finding.locality_identity != locality_identity
    ):
        raise PreservedMaterialMeasurementError(
            "the read pair finding is outside this Measurement locality"
        )
    source_identities = measurement_input_occurrences(finding.material)
    source_occurrences = []
    for source_identity in source_identities:
        source = ledger.get(source_identity) if isinstance(source_identity, str) else None
        if source is None:
            raise PreservedMaterialMeasurementError(
                "the read pair finding names an absent source occurrence"
            )
        source_occurrences.append(source)
    measurements = measure_position_pairs_from_finding(
        ledger,
        finding_event_identity=finding_event_identity,
        occurrences=source_occurrences,
    )
    applicable_inputs = [
        {
            "input_reference": finding_event_identity,
            "role": PAIR_FINDING_PARTICIPATION_ROLE,
            "standing": "applicable",
        },
        *[
            {
                "input_reference": source_identity,
                "role": SOURCE_OCCURRENCE_PARTICIPATION_ROLE,
                "standing": "applicable",
            }
            for source_identity in source_identities
        ],
    ]
    return _record_position_pair_measurement_result(
        ledger,
        locality_identity=locality_identity,
        position_pair_evidence_event_identity=finding_event_identity,
        source_identities=tuple(source_identities),
        measurements=measurements,
        applicable_inputs=applicable_inputs,
    )


def _position_pair_measurement_from_material(
    value: object,
) -> PositionPairMeasurement:
    if not isinstance(value, dict):
        raise PreservedMaterialMeasurementError(
            "a recorded position-pair measurement is not an exact coordinate mapping"
        )

    def positioned(item: object) -> PositionedRepresentationOccurrence | None:
        if item is None:
            return None
        if not isinstance(item, dict):
            raise PreservedMaterialMeasurementError(
                "a recorded position is not an exact coordinate mapping"
            )
        source_identity = item.get("source_occurrence_identity")
        position = item.get("position")
        representation = item.get("representation")
        if (
            not isinstance(source_identity, str)
            or not source_identity
            or not isinstance(position, int)
            or isinstance(position, bool)
            or position < 0
            or not isinstance(representation, str)
            or not representation
        ):
            raise PreservedMaterialMeasurementError(
                "a recorded position carries malformed coordinates"
            )
        return PositionedRepresentationOccurrence(
            source_identity,
            position,
            representation,
        )

    pair_value = value.get("pair_occurrence")
    if not isinstance(pair_value, dict):
        raise PreservedMaterialMeasurementError(
            "a recorded position-pair measurement carries no exact pair occurrence"
        )
    ordered_pair = pair_value.get("ordered_pair")
    if (
        not isinstance(ordered_pair, list)
        or len(ordered_pair) != 2
        or not all(isinstance(item, str) and item for item in ordered_pair)
    ):
        raise PreservedMaterialMeasurementError(
            "a recorded position-pair measurement carries no exact ordered pair"
        )
    pair_first = positioned(pair_value.get("first"))
    pair_second = positioned(pair_value.get("second"))
    if pair_first is None or pair_second is None:
        raise PreservedMaterialMeasurementError(
            "a recorded pair occurrence is missing one exact position"
        )
    source_identity = value.get("source_occurrence_identity")
    exact_order = value.get("exact_order")
    evidence = value.get("evidence")
    if (
        not isinstance(source_identity, str)
        or not source_identity
        or not isinstance(exact_order, list)
        or not all(
            isinstance(position, int)
            and not isinstance(position, bool)
            and position >= 0
            for position in exact_order
        )
        or not isinstance(evidence, dict)
    ):
        raise PreservedMaterialMeasurementError(
            "a recorded position-pair measurement carries malformed bounds"
        )
    return PositionPairMeasurement(
        before_occurrence=positioned(value.get("before_occurrence")),
        pair_occurrence=ExactPositionPairOccurrence(
            PositionPair(*ordered_pair),
            pair_first,
            pair_second,
        ),
        after_occurrence=positioned(value.get("after_occurrence")),
        source_occurrence_identity=source_identity,
        exact_order=tuple(exact_order),
        evidence=evidence,
    )


def get_recorded_position_pair_measurements(
    ledger: EventLedger,
    event_identity: str,
) -> tuple[PositionPairMeasurement, ...] | None:
    """Read an exact recorded result without repeating its Measurement."""

    event = ledger.get(event_identity)
    if event is None:
        return None
    if (
        event.kind != POSITION_PAIR_MEASUREMENT_RECORDED_KIND
        or ledger.integrity_of(event_identity) == CORRUPTED
    ):
        raise PreservedMaterialMeasurementError(
            "the position-pair measurement result event is absent or corrupted"
        )
    position_pair_evidence_identity = event.material.get("position_pair_evidence_event_identity")
    source_identities = event.material.get("source_occurrence_references")
    carried_measurements = event.material.get("measurements")
    if (
        not isinstance(position_pair_evidence_identity, str)
        or not position_pair_evidence_identity
        or not isinstance(source_identities, list)
        or not all(isinstance(value, str) and value for value in source_identities)
        or not isinstance(carried_measurements, list)
    ):
        raise PreservedMaterialMeasurementError(
            "the position-pair measurement result carries malformed result coordinates"
        )
    result_material = {
        "result_identity": event.material.get("result_identity"),
        "position_pair_evidence_event_identity": position_pair_evidence_identity,
        "source_occurrence_references": source_identities,
        "measurements": carried_measurements,
    }
    act_evidence_identity = event.material.get("responsible_act_evidence_identity")
    yield_evidence_identity = event.material.get("yield_evidence_identity")
    locality_evidence_identity = event.material.get("locality_evidence_identity")
    if not all(
        isinstance(value, str) and value
        for value in (act_evidence_identity, yield_evidence_identity, locality_evidence_identity)
    ):
        raise PreservedMaterialMeasurementError(
            "the position-pair measurement result carries malformed Evidence references"
        )
    act_evidence = ledger.get(act_evidence_identity)
    yield_evidence = ledger.get(yield_evidence_identity)
    locality_evidence = ledger.get(locality_evidence_identity)
    if (
        act_evidence is None
        or act_evidence.kind != POSITION_PAIR_MEASUREMENT_ACT_EVIDENCE_KIND
        or yield_evidence is None
        or yield_evidence.kind != "operator.yield.evidence_recorded"
        or locality_evidence is None
        or locality_evidence.kind != POSITION_PAIR_MEASUREMENT_LOCALITY_EVIDENCE_KIND
    ):
        raise PreservedMaterialMeasurementError(
            "the position-pair measurement result carries incomplete relation Evidence"
        )
    act_occurrence_identity = event.material.get("act_occurrence_identity")
    downstream_act_identity = event.material.get("downstream_act_identity")
    if (
        not isinstance(act_occurrence_identity, str)
        or not isinstance(downstream_act_identity, str)
        or act_evidence.material.get("downstream_act_identity") != downstream_act_identity
        or act_evidence.material.get("act_occurrence_identity") != act_occurrence_identity
        or yield_evidence.material.get("dimensions", {}).get("act_occurrence_identity")
        != act_occurrence_identity
        or locality_evidence.material.get("act_occurrence_identity")
        != act_occurrence_identity
        or locality_evidence.material.get("carried_content") != result_material
    ):
        raise PreservedMaterialMeasurementError(
            "the position-pair measurement relation Evidence carries different coordinates"
        )
    anchor = ledger.get(position_pair_evidence_identity)
    sources: dict[str, Event] = {}
    source_texts: dict[str, str] = {}
    if anchor is not None and _is_established_after_measurement(anchor):
        expected_inputs = [
            {
                "input_reference": position_pair_evidence_identity,
                "role": PAIR_FINDING_PARTICIPATION_ROLE,
                "standing": "applicable",
            },
            *[
                {
                    "input_reference": source_identity,
                    "role": SOURCE_OCCURRENCE_PARTICIPATION_ROLE,
                    "standing": "applicable",
                }
                for source_identity in source_identities
            ],
        ]
        if (
            ledger.integrity_of(position_pair_evidence_identity) == CORRUPTED
            or anchor.locality_identity != event.locality_identity
            or measurement_input_occurrences(anchor.material)
            != tuple(source_identities)
        ):
            raise PreservedMaterialMeasurementError(
                "the position-pair measurement pair-finding Evidence does not read"
            )
        for source_identity in source_identities:
            source = ledger.get(source_identity)
            text = source.material.get("represented_material") if source is not None else None
            if (
                source is None
                or source.kind != INGEST_OCCURRED_KIND
                or ledger.integrity_of(source_identity) == CORRUPTED
                or source.locality_identity != event.locality_identity
                or not isinstance(text, str)
            ):
                raise PreservedMaterialMeasurementError(
                    "the position-pair measurement source Evidence does not read"
                )
            sources[source_identity] = source
            source_texts[source_identity] = text
    elif (
        anchor is not None
        and anchor.kind == REPRESENTATION_EMISSION_LOCALITY_EVIDENCE_KIND
        and ledger.integrity_of(anchor.identity) != CORRUPTED
        and len(source_identities) == 1
    ):
        source = ledger.get(source_identities[0])
        text = source.material.get("emitted_representation") if source is not None else None
        if (
            source is None
            or source.kind != REPRESENTATION_EMITTED_KIND
            or ledger.integrity_of(source.identity) == CORRUPTED
            or source.locality_identity != event.locality_identity
            or source.material.get("locality_evidence_identity") != anchor.identity
            or anchor.material.get("act_occurrence_identity")
            != source.material.get("act_occurrence_identity")
            or anchor.material.get("content_kind") != "text"
            or anchor.material.get("carried_content") != text
            or not isinstance(text, str)
        ):
            raise PreservedMaterialMeasurementError(
                "the emitted-representation Locality Evidence does not read"
            )
        sources[source.identity] = source
        source_texts[source.identity] = text
        expected_inputs = [
            {
                "input_reference": anchor.identity,
                "role": EMISSION_LOCALITY_PARTICIPATION_ROLE,
                "standing": "applicable",
            },
            {
                "input_reference": source.identity,
                "role": EMISSION_OCCURRENCE_PARTICIPATION_ROLE,
                "standing": "applicable",
            },
        ]
    else:
        raise PreservedMaterialMeasurementError(
            "the position-pair measurement Evidence anchor does not read"
        )
    expected_participation = [
        {
            "subject_reference": item["input_reference"],
            "role": item["role"],
            "act_occurrence_identity": act_occurrence_identity,
        }
        for item in expected_inputs
    ]
    if (
        act_evidence.material.get("input_applicability") != expected_inputs
        or act_evidence.material.get("participation") != expected_participation
        or event.material.get("participation") != expected_participation
    ):
        raise PreservedMaterialMeasurementError(
            "the position-pair measurement Act Evidence carries different inputs or Participation coordinates"
        )
    measurements = tuple(
        _position_pair_measurement_from_material(value)
        for value in carried_measurements
    )
    if any(
        measurement.evidence.get("position_pair_evidence_event_identity") != position_pair_evidence_identity
        or measurement.source_occurrence_identity not in sources
        or measurement.evidence.get("exact_representation")
        != source_texts[measurement.source_occurrence_identity]
        or measurement.evidence.get("locality_identity") != event.locality_identity
        for measurement in measurements
    ):
        raise PreservedMaterialMeasurementError(
            "a carried position-pair measurement names different Evidence"
        )
    return measurements


def record_position_pair_measurement_compare(
    ledger: EventLedger,
    *,
    locality_identity: str,
    measurement_occurrence_references: Iterable[str],
) -> Event:
    """Compare exact durable measurement results and preserve the bounded result."""

    input_identities = tuple(measurement_occurrence_references)
    if (
        len(input_identities) < 2
        or any(not isinstance(value, str) or not value for value in input_identities)
        or len(set(input_identities)) != len(input_identities)
    ):
        raise PreservedMaterialMeasurementError(
            "measurement Compare requires at least two distinct recorded measurement occurrences"
        )
    measurements: list[PositionPairMeasurement] = []
    for event_identity in input_identities:
        event = ledger.get(event_identity)
        read = get_recorded_position_pair_measurements(ledger, event_identity)
        if (
            event is None
            or read is None
            or event.locality_identity != locality_identity
        ):
            raise PreservedMaterialMeasurementError(
                "an measurement Compare input does not read in this locality"
            )
        measurements.extend(read)
    compared = compare_position_pair_measurements(measurements)
    act_identity = new_identity("position_pair_measurement_compare_act")
    act_occurrence_identity = new_identity("position_pair_measurement_compare_occurrence")
    result_identity = f"position-pair-measurement-compare:{act_occurrence_identity}"
    result_material = {
        "result_identity": result_identity,
        "measurement_occurrence_references": list(input_identities),
        "comparison": compared,
    }
    participation = [
        {
            "subject_reference": event_identity,
            "role": MEASUREMENT_COMPARE_INPUT_ROLE,
            "act_occurrence_identity": act_occurrence_identity,
        }
        for event_identity in input_identities
    ]
    act_evidence = ledger.append(
        POSITION_PAIR_MEASUREMENT_COMPARE_ACT_EVIDENCE_KIND,
        {
            "downstream_act_identity": act_identity,
            "act_occurrence_identity": act_occurrence_identity,
            "act": "Compare exact position-pair measurement results",
            "responsibility": POSITION_PAIR_MEASUREMENT_COMPARE_RESPONSIBILITY,
            "responsible_boundary": "this Seed",
            "authority": "unestablished",
            "evidence_scope": (
                "Evidence for this exact Compare occurrence and its exact "
                "participants"
            ),
            "participation": participation,
        },
        locality_identity=locality_identity,
    )
    yield_evidence = _record_yield_evidence(
        ledger,
        locality_identity=locality_identity,
        exact_act="Compare exact position-pair measurement results",
        act_occurrence_identity=act_occurrence_identity,
        responsible_act_evidence_identity=act_evidence.identity,
        result_kind="bounded position-pair measurement comparison",
        result_identity=result_identity,
        result_content=result_material,
        responsibility=POSITION_PAIR_MEASUREMENT_COMPARE_RESPONSIBILITY,
        live_boundary="position_pair_measurement_compare",
        responsible_boundary="this Seed",
    )
    locality_evidence = ledger.append(
        POSITION_PAIR_MEASUREMENT_COMPARE_LOCALITY_EVIDENCE_KIND,
        {
            "act_occurrence_identity": act_occurrence_identity,
            "carried_content": result_material,
        },
        locality_identity=locality_identity,
    )
    return ledger.append(
        POSITION_PAIR_MEASUREMENT_COMPARE_RECORDED_KIND,
        {
            **result_material,
            "downstream_act_identity": act_identity,
            "act_occurrence_identity": act_occurrence_identity,
            "responsibility": POSITION_PAIR_MEASUREMENT_COMPARE_RESPONSIBILITY,
            "responsible_boundary": "this Seed",
            "participation": participation,
            "responsible_act_evidence_identity": act_evidence.identity,
            "yield_evidence_identity": yield_evidence.identity,
            "locality_evidence_identity": locality_evidence.identity,
            "unknowns": [
                "whether any repeated source material represents a grammar distinction remains Unknown"
            ],
        },
        locality_identity=locality_identity,
    )


def get_recorded_position_pair_measurement_compare(
    ledger: EventLedger,
    event_identity: str,
) -> dict[str, object] | None:
    """Read one durable Compare result without repeating the Compare."""

    event = ledger.get(event_identity)
    if event is None:
        return None
    if (
        event.kind != POSITION_PAIR_MEASUREMENT_COMPARE_RECORDED_KIND
        or ledger.integrity_of(event_identity) == CORRUPTED
    ):
        raise PreservedMaterialMeasurementError(
            "the recorded measurement Compare is absent or corrupted"
        )
    input_identities = event.material.get("measurement_occurrence_references")
    compared = event.material.get("comparison")
    if (
        not isinstance(input_identities, list)
        or len(input_identities) < 2
        or len(set(input_identities)) != len(input_identities)
        or not all(isinstance(value, str) and value for value in input_identities)
        or not isinstance(compared, dict)
    ):
        raise PreservedMaterialMeasurementError(
            "the recorded measurement Compare carries malformed coordinates"
        )
    result_material = {
        "result_identity": event.material.get("result_identity"),
        "measurement_occurrence_references": input_identities,
        "comparison": compared,
    }
    act_evidence = ledger.get(event.material.get("responsible_act_evidence_identity"))
    yield_evidence = ledger.get(event.material.get("yield_evidence_identity"))
    locality_evidence = ledger.get(event.material.get("locality_evidence_identity"))
    evidence = (act_evidence, yield_evidence, locality_evidence)
    if any(
        item is None or ledger.integrity_of(item.identity) == CORRUPTED
        for item in evidence
    ):
        raise PreservedMaterialMeasurementError(
            "the recorded measurement Compare carries absent or corrupted relation Evidence"
        )
    assert act_evidence is not None
    assert yield_evidence is not None
    assert locality_evidence is not None
    act_occurrence_identity = event.material.get("act_occurrence_identity")
    expected_participation = [
        {
            "subject_reference": input_identity,
            "role": MEASUREMENT_COMPARE_INPUT_ROLE,
            "act_occurrence_identity": act_occurrence_identity,
        }
        for input_identity in input_identities
    ]
    if (
        act_evidence.kind != POSITION_PAIR_MEASUREMENT_COMPARE_ACT_EVIDENCE_KIND
        or locality_evidence.kind
        != POSITION_PAIR_MEASUREMENT_COMPARE_LOCALITY_EVIDENCE_KIND
        or yield_evidence.kind != "operator.yield.evidence_recorded"
        or act_evidence.material.get("act_occurrence_identity") != act_occurrence_identity
        or yield_evidence.material.get("dimensions", {}).get("act_occurrence_identity")
        != act_occurrence_identity
        or locality_evidence.material.get("act_occurrence_identity") != act_occurrence_identity
        or act_evidence.material.get("authority") != "unestablished"
        or act_evidence.material.get("evidence_scope")
        != (
            "Evidence for this exact Compare occurrence and its exact "
            "participants"
        )
        or locality_evidence.material.get("carried_content") != result_material
        or act_evidence.material.get("participation") != expected_participation
        or event.material.get("participation") != expected_participation
    ):
        raise PreservedMaterialMeasurementError(
            "the recorded measurement Compare relation Evidence carries different coordinates"
        )
    for input_identity in input_identities:
        event = ledger.get(input_identity)
        if (
            event is None
            or ledger.integrity_of(input_identity) == CORRUPTED
            or event.locality_identity != event.locality_identity
            or get_recorded_position_pair_measurements(ledger, input_identity) is None
        ):
            raise PreservedMaterialMeasurementError(
                "a recorded measurement Compare input does not read"
            )
    return compared



def enumerate_representations(
    occurrences: Iterable[Event], *, present_in: Sequence[Sequence[Event]] = ()
) -> list[str]:
    """Every representation the material offers.

    No representation is named here and none is preferred. When ``present_in``
    is supplied, only representations measurable in *every* one of those scopes
    are returned -- a comparability requirement, so that a later measurement can
    measure the same distinction in each scope, not a judgement that the others are
    uninteresting.

    This is what removes the last supplied representation from the chain. The
    caller no longer says which representation to measure after; the material
    says which representations there are, and later measurements say which of
    them anything reproducible follows from.
    """

    material = list(occurrences)
    everywhere: set[str] | None = None
    for scope in present_in:
        seen = {
            token
            for event in scope
            for token in _positions(event.material.get("represented_material"))
        }
        everywhere = seen if everywhere is None else (everywhere & seen)
    offered = {
        token
        for event in material
        for token in _positions(event.material.get("represented_material"))
    }
    if everywhere is not None:
        offered &= everywhere
    return sorted(offered)


def enumerate_position_difference(
    occurrences: Iterable[Event], representation: str
) -> list[int]:
    differences: set[int] = set()
    for event in occurrences:
        parts = _positions(event.material.get("represented_material"))
        for index, part in enumerate(parts):
            if part != representation:
                continue
            differences.update(range(-index, 0))
            differences.update(range(1, len(parts) - index))
    return sorted(differences)


def measure_at_position_difference(
    occurrences: Iterable[Event],
    representation: str,
    *,
    difference: int,
    counting_scope: str,
) -> MeasurementFinding:
    if not isinstance(difference, int) or isinstance(difference, bool) or difference == 0:
        raise PreservedMaterialMeasurementError(
            "a position difference is a nonzero count"
        )

    def representation_at(text: str) -> str | None:
        parts = _positions(text)
        for index, part in enumerate(parts):
            if part != representation:
                continue
            at = index + difference
            if 0 <= at < len(parts):
                return parts[at]
        return None

    return measure_position_representations(
        occurrences,
        declared=DeclaredMeasurement(
            representation_measured=(
                f"the representation at position difference {difference} from "
                f"{representation!r}"
            ),
            equivalence_rule=EQUIVALENCE_RULE,
            counting_scope=counting_scope,
            relative_representation=representation,
            distinction="position difference",
            measured_position={"difference": difference},
        ),
        representation_at=representation_at,
    )


def measure_after(
    occurrences: Iterable[Event],
    representation: str,
    *,
    counting_scope: str,
) -> MeasurementFinding:
    return measure_at_position_difference(
        occurrences,
        representation,
        difference=1,
        counting_scope=counting_scope,
    )
