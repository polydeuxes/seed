"""Read exact adjacency-pair occurrences from displacement-one findings.

An **adjacency pair** is two representations, one recorded as occupying the
position after the other. Nothing more.

`#2391` validated thirteen such pairs from preserved material without a reader
naming any representation, occupant, or delimiter.

**The pairs are not supplied.** :func:`adjacency_pairs_from_finding` reads them out of a
recorded measurement finding, so what this round measures relative to comes
from the previous round's Evidence rather than from the caller. Every exact
pair occurrence retains that finding and its source occurrence.

Nothing here establishes represented relation, grammatical kind, relation, or
truth. A pair is an exact displacement-one adjacency.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Iterable, Sequence

from seed_runtime.events import CORRUPTED, EventLedger, EventLedgerBoundary
from seed_runtime.event import Event
from seed_runtime.ids import new_id
from seed_runtime.yield_evidence import _record_yield_evidence, yield_commitment
from seed_runtime.preserved_material_measurement import (
    INGEST_OCCURRED_KIND,
    MEASUREMENT_RECORDED_KIND,
    DeclaredMeasurement,
    MeasurementFinding,
    MEASUREMENT_CONVENTION,
    Occupancy,
    PreservedMaterialMeasurementError,
    measure_occupancy,
)
from seed_runtime.operator_representation import (
    REPRESENTATION_EMITTED_KIND,
    REPRESENTATION_EMISSION_LOCALITY_EVIDENCE_KIND,
)

EQUIVALENCE_RULE = "byte-for-byte equality; no normalization"

# Where each distinction measures, stated as coordinates rather than left in the
# indexing.  A measurement that does not say where it looked cannot be compared
# with one that looked elsewhere, and a coordinate that is never written down
# cannot be measured to have never varied.
#
#   anchored_on   which preserved representation the position is taken from
#   direction     which side of it
#   displacement  how many positions away
#
# This describes the displacement-one acquisition retained here.
MEASURED_POSITIONS: dict[str, dict[str, object]] = {
    "after": {"anchored_on": "the representation", "direction": "after", "displacement": 1},
}
ADJACENCY_PAIR_MEASUREMENT_RECORDED_KIND = (
    "operator.measurement.adjacency_pair_measurement_recorded"
)
ADJACENCY_PAIR_MEASUREMENT_ACT_EVIDENCE_KIND = (
    "operator.measurement.adjacency_pair_measurement_act_evidenced"
)
ADJACENCY_PAIR_MEASUREMENT_LOCALITY_EVIDENCE_KIND = (
    "operator.measurement.adjacency_pair_measurement_locality_evidenced"
)
ADJACENCY_PAIR_MEASUREMENT_CONVENTION = "adjacency_pair_measurement"
ADJACENCY_PAIR_MEASUREMENT_COMPARE_RECORDED_KIND = (
    "operator.measurement.adjacency_pair_measurement_compare_recorded"
)
ADJACENCY_PAIR_MEASUREMENT_COMPARE_ACT_EVIDENCE_KIND = (
    "operator.measurement.adjacency_pair_measurement_compare_act_evidenced"
)
ADJACENCY_PAIR_MEASUREMENT_COMPARE_LOCALITY_EVIDENCE_KIND = (
    "operator.measurement.adjacency_pair_measurement_compare_locality_evidenced"
)
EVENT_KIND_RESPONSIBILITIES = {
    ADJACENCY_PAIR_MEASUREMENT_RECORDED_KIND: "02.Acts.A",
    ADJACENCY_PAIR_MEASUREMENT_ACT_EVIDENCE_KIND: "02.Acts.A",
    ADJACENCY_PAIR_MEASUREMENT_LOCALITY_EVIDENCE_KIND: "06.Standing.B",
    ADJACENCY_PAIR_MEASUREMENT_COMPARE_RECORDED_KIND: "02.Acts.A",
    ADJACENCY_PAIR_MEASUREMENT_COMPARE_ACT_EVIDENCE_KIND: "02.Acts.A",
    ADJACENCY_PAIR_MEASUREMENT_COMPARE_LOCALITY_EVIDENCE_KIND: "06.Standing.B",
}
ADJACENCY_PAIR_MEASUREMENT_COMPARE_CONVENTION = (
    "adjacency_pair_measurement_compare"
)
ADJACENCY_PAIR_MEASUREMENT_RESPONSIBILITY = (
    "measure one adjacent position on each side of every exact occurrence of "
    "each ordered pair read from one exact finding"
)
PAIR_FINDING_PARTICIPATION_ROLE = "read ordered-pair finding"
SOURCE_OCCURRENCE_PARTICIPATION_ROLE = "exact preserved source occurrence"
EMISSION_LOCALITY_PARTICIPATION_ROLE = "exact emission Locality Evidence"
EMISSION_OCCURRENCE_PARTICIPATION_ROLE = "exact emission occurrence"
MEASUREMENT_COMPARE_INPUT_ROLE = "exact recorded adjacency-pair measurements"
ADJACENCY_PAIR_MEASUREMENT_COMPARE_RESPONSIBILITY = (
    "compare exact recorded adjacency-pair measurements without identifying "
    "equal representations as equal occurrences or relations"
)


@dataclass(frozen=True)
class AdjacencyPair:
    """An ordered pair of representations whose adjacency was found reproducible.

    The name describes the measured arrangement and nothing else. It is not a
    constitutional kind, and it asserts nothing about either representation or
    about any relation between them.
    """

    left: str
    right: str

    def __post_init__(self) -> None:
        if not isinstance(self.left, str) or not isinstance(self.right, str):
            raise PreservedMaterialMeasurementError("a pair is a pair of representations")
        if not self.left or not self.right:
            raise PreservedMaterialMeasurementError("a pair's representations must be exact")

    def __str__(self) -> str:  # pragma: no cover - representation only
        return f"{self.left!r} -> {self.right!r}"


@dataclass(frozen=True)
class PositionedRepresentationOccurrence:
    """One exact representation position inside one preserved occurrence."""

    source_occurrence_id: str
    position: int
    representation: str

    @property
    def identity(self) -> tuple[str, int]:
        return (self.source_occurrence_id, self.position)


@dataclass(frozen=True)
class ExactAdjacencyPairOccurrence:
    """One exact occurrence of an already-read ordered adjacency pair."""

    pair: AdjacencyPair
    left: PositionedRepresentationOccurrence
    right: PositionedRepresentationOccurrence

    def __post_init__(self) -> None:
        if self.left.source_occurrence_id != self.right.source_occurrence_id:
            raise PreservedMaterialMeasurementError(
                "an adjacency pair occurrence cannot cross source occurrences"
            )
        if self.right.position != self.left.position + 1:
            raise PreservedMaterialMeasurementError(
                "an adjacency pair occurrence requires exact displacement-one order"
            )
        if (
            self.left.representation != self.pair.left
            or self.right.representation != self.pair.right
        ):
            raise PreservedMaterialMeasurementError(
                "an adjacency pair occurrence must carry its exact ordered pair"
            )

    @property
    def identity(self) -> tuple[str, int, int]:
        return (
            self.left.source_occurrence_id,
            self.left.position,
            self.right.position,
        )


@dataclass(frozen=True)
class AdjacencyPairMeasurement:
    """One bounded position on each side of one exact pair occurrence.

    The representations are carried measurements. They are not classified as
    relation words, and equal representations do not identify equal relations.
    """

    left_occurrence: PositionedRepresentationOccurrence | None
    pair_occurrence: ExactAdjacencyPairOccurrence
    right_occurrence: PositionedRepresentationOccurrence | None
    source_occurrence_id: str
    exact_order: tuple[int, ...]
    evidence: dict[str, object]

    def __post_init__(self) -> None:
        source_id = self.source_occurrence_id
        if not isinstance(source_id, str) or not source_id:
            raise PreservedMaterialMeasurementError(
                "an adjacency-pair measurement requires one exact source occurrence"
            )
        if self.pair_occurrence.left.source_occurrence_id != source_id:
            raise PreservedMaterialMeasurementError(
                "the pair occurrence is outside the measured source occurrence"
            )
        expected_order = []
        if self.left_occurrence is not None:
            if (
                self.left_occurrence.source_occurrence_id != source_id
                or self.left_occurrence.position
                != self.pair_occurrence.left.position - 1
            ):
                raise PreservedMaterialMeasurementError(
                    "the left occurrence is not exactly adjacent to the pair"
                )
            expected_order.append(self.left_occurrence.position)
        expected_order.extend(
            (
                self.pair_occurrence.left.position,
                self.pair_occurrence.right.position,
            )
        )
        if self.right_occurrence is not None:
            if (
                self.right_occurrence.source_occurrence_id != source_id
                or self.right_occurrence.position
                != self.pair_occurrence.right.position + 1
            ):
                raise PreservedMaterialMeasurementError(
                    "the right occurrence is not exactly adjacent to the pair"
                )
            expected_order.append(self.right_occurrence.position)
        if self.exact_order != tuple(expected_order):
            raise PreservedMaterialMeasurementError(
                "the carried order does not match the exact measured positions"
            )
        evidence = self.evidence
        finding_id = evidence.get("adjacency_evidence_event_id")
        evidence_ids = evidence.get("evidence_occurrence_ids")
        text = evidence.get("exact_representation")
        if (
            evidence.get("source_occurrence_id") != source_id
            or not isinstance(finding_id, str)
            or not finding_id
            or evidence_ids != [finding_id, source_id]
            or evidence.get("source_kind")
            not in {
                INGEST_OCCURRED_KIND,
                REPRESENTATION_EMITTED_KIND,
            }
            or not isinstance(evidence.get("locality_id"), str)
            or not isinstance(text, str)
        ):
            raise PreservedMaterialMeasurementError(
                "the adjacency-pair measurement does not preserve its exact Evidence"
            )
        positions = _positions(text)
        carried = (
            *((self.left_occurrence,) if self.left_occurrence is not None else ()),
            self.pair_occurrence.left,
            self.pair_occurrence.right,
            *((self.right_occurrence,) if self.right_occurrence is not None else ()),
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
            self.evidence["adjacency_evidence_event_id"],
            self.source_occurrence_id,
            self.pair_occurrence.left.position,
            self.pair_occurrence.right.position,
        )

    @property
    def fully_bounded_coordinates(self) -> dict[str, object] | None:
        """Return the neutral coordinates only when both outer positions exist."""

        if self.left_occurrence is None or self.right_occurrence is None:
            return None
        return {
            "identity": {
                "adjacency_evidence_event_id": self.evidence["adjacency_evidence_event_id"],
                "source_occurrence_id": self.source_occurrence_id,
                "positions": list(self.exact_order),
            },
            "left_occurrence": {
                "occurrence": list(self.left_occurrence.identity),
                "representation": self.left_occurrence.representation,
            },
            "pair_occurrence": {
                "occurrence": list(self.pair_occurrence.identity),
                "ordered_pair": [
                    self.pair_occurrence.pair.left,
                    self.pair_occurrence.pair.right,
                ],
            },
            "right_occurrence": {
                "occurrence": list(self.right_occurrence.identity),
                "representation": self.right_occurrence.representation,
            },
            "evidence": dict(self.evidence),
        }



def _adjacency_pairs_from_event(event: Event | None) -> list[AdjacencyPair]:
    if event is None or event.kind != MEASUREMENT_RECORDED_KIND:
        raise PreservedMaterialMeasurementError(
            "pairs must be read from a recorded measurement finding"
        )
    left = event.payload.get("measured_left_representation")
    if not isinstance(left, str) or not left:
        raise PreservedMaterialMeasurementError(
            "the recorded finding does not name the representation it measured after"
        )
    return [
        AdjacencyPair(left=left, right=occupancy["representation"])
        for occupancy in event.payload["occupancies"]
    ]


def _is_established_after_measurement(event: Event) -> bool:
    """Whether a record carries the exact established displacement-1 distinction."""

    left = event.payload.get("measured_left_representation")
    return (
        event.kind == MEASUREMENT_RECORDED_KIND
        and event.payload.get("convention") == MEASUREMENT_CONVENTION
        and event.payload.get("equivalence_rule") == EQUIVALENCE_RULE
        and event.payload.get("measurement_distinction") == "after"
        and isinstance(left, str)
        and bool(left)
        and event.payload.get("measured_relative_to") == [left]
        and event.payload.get("measured_position") == MEASURED_POSITIONS["after"]
    )


def adjacency_pairs_from_finding(ledger: EventLedger, finding_event_id: str) -> list[AdjacencyPair]:
    """Read pairs out of a recorded finding rather than taking them from a caller.

    The recorded finding names a left representation and the occupancies
    measured after it. Every occupancy is returned; none is filtered by count,
    share, or a threshold. Which of them prove reproducible is what the
    measurement measures, not something decided here.
    """

    return _adjacency_pairs_from_event(ledger.get(finding_event_id))


def _positions(text: str) -> Sequence[str]:
    """Whitespace-delimited positions.

    A reader-supplied resolution, recorded as such. `#2391` established that
    the discrimination survives character n-grams too, so this rule is not
    load-bearing; it is legible.
    """

    return text.split()


def _measure_adjacency_pair_measurements(
    occurrences: Iterable[Event],
    pairs: Iterable[AdjacencyPair],
    *,
    adjacency_evidence_event_id: str,
) -> tuple[AdjacencyPairMeasurement, ...]:
    """Extend every exact pair occurrence one position in each direction.

    Pair values select what is measured; they do not classify the resulting
    coordinates. Every measurement is identified by its preserved source
    occurrence and exact positions. Boundary absence is retained as absence,
    rather than dropping the pair occurrence or filling a position.
    """

    bounded_pairs = tuple(dict.fromkeys(pairs))
    measurements: list[AdjacencyPairMeasurement] = []
    for source in occurrences:
        if source.kind == INGEST_OCCURRED_KIND:
            text = source.payload.get("represented_material")
        elif source.kind == REPRESENTATION_EMITTED_KIND:
            text = source.payload.get("emitted_representation")
        else:
            raise PreservedMaterialMeasurementError(
                f"the source occurrence does not carry represented material: {source.kind}"
            )
        if not isinstance(text, str):
            raise PreservedMaterialMeasurementError(
                f"{source.id} carries no represented material"
            )
        positions = _positions(text)
        for pair in bounded_pairs:
            for at in range(len(positions) - 1):
                if positions[at] != pair.left or positions[at + 1] != pair.right:
                    continue
                pair_left = PositionedRepresentationOccurrence(
                    source.id, at, positions[at]
                )
                pair_right = PositionedRepresentationOccurrence(
                    source.id, at + 1, positions[at + 1]
                )
                left = (
                    PositionedRepresentationOccurrence(
                        source.id, at - 1, positions[at - 1]
                    )
                    if at > 0
                    else None
                )
                right = (
                    PositionedRepresentationOccurrence(
                        source.id, at + 2, positions[at + 2]
                    )
                    if at + 2 < len(positions)
                    else None
                )
                exact_order = tuple(
                    position
                    for position in (
                        left.position if left is not None else None,
                        pair_left.position,
                        pair_right.position,
                        right.position if right is not None else None,
                    )
                    if position is not None
                )
                measurements.append(
                    AdjacencyPairMeasurement(
                        left_occurrence=left,
                        pair_occurrence=ExactAdjacencyPairOccurrence(
                            pair=pair,
                            left=pair_left,
                            right=pair_right,
                        ),
                        right_occurrence=right,
                        source_occurrence_id=source.id,
                        exact_order=exact_order,
                        evidence={
                            "source_occurrence_id": source.id,
                            "adjacency_evidence_event_id": adjacency_evidence_event_id,
                            "evidence_occurrence_ids": [
                                adjacency_evidence_event_id,
                                source.id,
                            ],
                            "source_kind": source.kind,
                            "locality_id": source.locality_id,
                            "exact_representation": text,
                        },
                    )
                )
    return tuple(measurements)


def measure_emitted_representation_adjacency(
    ledger: EventLedger,
    *,
    emission_event_id: str,
) -> tuple[AdjacencyPairMeasurement, ...]:
    """Measure exact adjacency in text carried by one emission occurrence.

    The emission occurrence is admitted only through its exact Locality
    Evidence. Matching text or an emission-shaped event does not establish the
    content-to-occurrence relation.
    """

    emission = ledger.get(emission_event_id)
    if (
        emission is None
        or emission.kind != REPRESENTATION_EMITTED_KIND
        or ledger.integrity_of(emission_event_id) == CORRUPTED
    ):
        raise PreservedMaterialMeasurementError(
            "emitted-representation adjacency requires one intact emission occurrence"
        )
    text = emission.payload.get("emitted_representation")
    locality_id = emission.payload.get("locality_evidence_id")
    locality = ledger.get(locality_id) if isinstance(locality_id, str) else None
    if (
        not isinstance(text, str)
        or locality is None
        or locality.kind != REPRESENTATION_EMISSION_LOCALITY_EVIDENCE_KIND
        or ledger.integrity_of(locality.id) == CORRUPTED
        or locality.locality_id != emission.locality_id
        or locality.payload.get("act_occurrence_id")
        != emission.payload.get("act_occurrence_id")
        or locality.payload.get("content_kind") != "text"
        or locality.payload.get("carried_content") != text
    ):
        raise PreservedMaterialMeasurementError(
            "the emission does not preserve exact Locality Evidence for its representation"
        )
    positions = _positions(text)
    pairs = tuple(
        dict.fromkeys(
            AdjacencyPair(positions[index], positions[index + 1])
            for index in range(len(positions) - 1)
        )
    )
    return _measure_adjacency_pair_measurements(
        (emission,),
        pairs,
        adjacency_evidence_event_id=locality.id,
    )


def compare_emitted_representation_adjacency(
    ledger: EventLedger,
    *,
    emission_event_ids: Iterable[str],
) -> dict[str, object]:
    """Compare exact positional measurements from distinct emissions."""

    identities = tuple(emission_event_ids)
    if (
        len(identities) < 2
        or any(not isinstance(identity, str) or not identity for identity in identities)
        or len(set(identities)) != len(identities)
    ):
        raise PreservedMaterialMeasurementError(
            "emission adjacency Compare requires at least two distinct exact emission occurrences"
        )
    measurements = tuple(
        measurement
        for identity in identities
        for measurement in measure_emitted_representation_adjacency(
            ledger,
            emission_event_id=identity,
        )
    )
    return compare_adjacency_pair_measurements(measurements)


def record_emitted_representation_adjacency(
    ledger: EventLedger,
    *,
    emission_event_id: str,
) -> Event:
    """Preserve exact adjacency measured through one emission Locality."""

    emission = ledger.get(emission_event_id)
    measurements = measure_emitted_representation_adjacency(
        ledger,
        emission_event_id=emission_event_id,
    )
    assert emission is not None
    locality_id = emission.payload["locality_evidence_id"]
    return _record_adjacency_pair_measurement_result(
        ledger,
        locality_id=emission.locality_id,
        adjacency_evidence_event_id=locality_id,
        source_ids=(emission.id,),
        measurements=measurements,
        applicable_inputs=[
            {
                "input_reference": locality_id,
                "role": EMISSION_LOCALITY_PARTICIPATION_ROLE,
                "standing": "applicable",
            },
            {
                "input_reference": emission.id,
                "role": EMISSION_OCCURRENCE_PARTICIPATION_ROLE,
                "standing": "applicable",
            },
        ],
    )


def measure_adjacency_pairs_from_finding(
    ledger: EventLedger,
    *,
    finding_event_id: str,
    occurrences: Iterable[Event],
) -> tuple[AdjacencyPairMeasurement, ...]:
    """Measure only adjacency pairs read from one recorded finding."""

    finding = ledger.get(finding_event_id)
    if finding is None or ledger.integrity_of(finding_event_id) == CORRUPTED:
        raise PreservedMaterialMeasurementError(
            "adjacency pairs require one intact recorded finding"
        )
    if not _is_established_after_measurement(finding):
        raise PreservedMaterialMeasurementError(
            "adjacency-pair measurements require an exact recorded displacement-one finding"
        )
    material = tuple(occurrences)
    recorded_ids = finding.payload.get("input_event_ids")
    if (
        not isinstance(recorded_ids, list)
        or not all(isinstance(value, str) and value for value in recorded_ids)
        or tuple(event.id for event in material) != tuple(recorded_ids)
    ):
        raise PreservedMaterialMeasurementError(
            "the supplied source occurrences differ from the finding's exact Evidence"
        )
    for event in material:
        recorded = ledger.get(event.id)
        if (
            recorded is None
            or recorded.kind != INGEST_OCCURRED_KIND
            or recorded.locality_id != finding.locality_id
            or recorded.locality_id != event.locality_id
            or recorded.payload != event.payload
        ):
            raise PreservedMaterialMeasurementError(
                "the finding's source-occurrence Evidence does not read"
            )
    pairs = _adjacency_pairs_from_event(finding)
    return _measure_adjacency_pair_measurements(
        material,
        pairs,
        adjacency_evidence_event_id=finding_event_id,
    )


def compare_adjacency_pair_measurements(
    measurements: Iterable[AdjacencyPairMeasurement],
) -> dict[str, object]:
    """Report only distinctions that survive exact occurrence counterexamples.

    Representation equality is counted for comparison but never used as
    occurrence identity. The result reports only measured differences.
    """

    bounded = tuple(measurements)
    if not all(isinstance(item, AdjacencyPairMeasurement) for item in bounded):
        raise PreservedMaterialMeasurementError(
            "adjacency-pair measurement Compare requires exact bounded measurements"
        )
    identities = [measurement.identity for measurement in bounded]
    if len(set(identities)) != len(identities):
        raise PreservedMaterialMeasurementError(
            "the same exact adjacency-pair measurement was supplied more than once"
        )
    complete = tuple(
        coordinates
        for measurement in bounded
        if (coordinates := measurement.fully_bounded_coordinates) is not None
    )
    representation_groups: dict[
        tuple[str, tuple[str, str], str], list[dict[str, object]]
    ] = {}
    pair_groups: dict[tuple[str, str], list[dict[str, object]]] = {}
    outer_groups: dict[tuple[str, str], list[dict[str, object]]] = {}
    for coordinates in complete:
        left = coordinates["left_occurrence"]["representation"]
        pair = tuple(coordinates["pair_occurrence"]["ordered_pair"])
        right = coordinates["right_occurrence"]["representation"]
        representation_groups.setdefault((left, pair, right), []).append(coordinates)
        pair_groups.setdefault(pair, []).append(coordinates)
        outer_groups.setdefault((left, right), []).append(coordinates)

    return {
        "measurement_count": len(bounded),
        "fully_bounded_measurement_count": len(complete),
        "boundary_measurement_count": len(bounded) - len(complete),
        "distinct_fully_bounded_occurrences": len(
            {
                (
                    coordinates["identity"]["adjacency_evidence_event_id"],
                    coordinates["identity"]["source_occurrence_id"],
                    tuple(coordinates["identity"]["positions"]),
                )
                for coordinates in complete
            }
        ),
        "distinct_representation_triples": len(representation_groups),
        "counterexamples": {
            "representation_triple_groups_with_multiple_occurrences": sum(
                len(group) > 1 for group in representation_groups.values()
            ),
            "ordered_pair_groups_with_multiple_endpoint_representations": sum(
                len(
                    {
                        (
                            coordinates["left_occurrence"]["representation"],
                            coordinates["right_occurrence"]["representation"],
                        )
                        for coordinates in group
                    }
                )
                > 1
                for group in pair_groups.values()
            ),
            "endpoint_groups_with_multiple_ordered_pairs": sum(
                len(
                    {
                        tuple(coordinates["pair_occurrence"]["ordered_pair"])
                        for coordinates in group
                    }
                )
                > 1
                for group in outer_groups.values()
            ),
        },
        "distinct_adjacency_coordinates": [
            {
                "left_present": left_present,
                "right_present": right_present,
                "ordered_displacements": list(displacements),
            }
            for left_present, right_present, displacements in sorted(
                {
                    (
                        measurement.left_occurrence is not None,
                        measurement.right_occurrence is not None,
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


def _adjacency_pair_measurement_payload(
    measurement: AdjacencyPairMeasurement,
) -> dict[str, object]:
    def positioned(
        occurrence: PositionedRepresentationOccurrence | None,
    ) -> dict[str, object] | None:
        if occurrence is None:
            return None
        return {
            "source_occurrence_id": occurrence.source_occurrence_id,
            "position": occurrence.position,
            "representation": occurrence.representation,
        }

    return {
        "left_occurrence": positioned(measurement.left_occurrence),
        "pair_occurrence": {
            "ordered_pair": [
                measurement.pair_occurrence.pair.left,
                measurement.pair_occurrence.pair.right,
            ],
            "left": positioned(measurement.pair_occurrence.left),
            "right": positioned(measurement.pair_occurrence.right),
        },
        "right_occurrence": positioned(measurement.right_occurrence),
        "source_occurrence_id": measurement.source_occurrence_id,
        "exact_order": list(measurement.exact_order),
        "evidence": dict(measurement.evidence),
    }


def _record_adjacency_pair_measurement_result(
    ledger: EventLedger,
    *,
    locality_id: str,
    adjacency_evidence_event_id: str,
    source_ids: tuple[str, ...],
    measurements: tuple[AdjacencyPairMeasurement, ...],
    applicable_inputs: list[dict[str, str]],
) -> Event:
    act_id = new_id("adjacency_pair_measurement_measurement_act")
    act_occurrence_id = new_id("adjacency_pair_measurement_measurement_occurrence")
    result_payload = {
        "adjacency_evidence_event_id": adjacency_evidence_event_id,
        "source_occurrence_ids": list(source_ids),
        "measurements": [
            _adjacency_pair_measurement_payload(measurement)
            for measurement in measurements
        ],
    }
    participation = [
        {
            "subject_reference": item["input_reference"],
            "role": item["role"],
            "act_occurrence_id": act_occurrence_id,
        }
        for item in applicable_inputs
    ]
    act_evidence = ledger.append(
        ADJACENCY_PAIR_MEASUREMENT_ACT_EVIDENCE_KIND,
        {
            "downstream_act_id": act_id,
            "act_occurrence_id": act_occurrence_id,
            "act": "exact adjacency-pair measurement Measurement",
            "responsibility": ADJACENCY_PAIR_MEASUREMENT_RESPONSIBILITY,
            "responsible_boundary": "this Seed",
            "input_applicability": applicable_inputs,
            "participation": participation,
            "result_commitment": yield_commitment(
                ADJACENCY_PAIR_MEASUREMENT_CONVENTION, result_payload
            ),
            "authority": "unestablished",
            "evidence_scope": "this exact bounded Measurement occurrence only",
        },
        locality_id=locality_id,
    )
    yield_evidence = _record_yield_evidence(
        ledger,
        locality_id=locality_id,
        convention=ADJACENCY_PAIR_MEASUREMENT_CONVENTION,
        yielding_act="exact adjacency-pair measurement Measurement",
        act_occurrence_id=act_occurrence_id,
        yielded_result_kind="exact adjacency-pair measurements",
        result_identity=f"adjacency-pair-measurement-result:{act_occurrence_id}",
        yielded_content=result_payload,
        responsibility=ADJACENCY_PAIR_MEASUREMENT_RESPONSIBILITY,
        live_boundary="adjacency_pair_measurement",
        responsible_boundary="this Seed",
    )
    locality_evidence = ledger.append(
        ADJACENCY_PAIR_MEASUREMENT_LOCALITY_EVIDENCE_KIND,
        {
            "act_occurrence_id": act_occurrence_id,
            "content_kind": "exact adjacency-pair measurements",
            "carried_content": result_payload,
            "authority": "unestablished",
            "evidence_scope": "this exact result-to-occurrence Locality only",
        },
        locality_id=locality_id,
    )
    return ledger.append(
        ADJACENCY_PAIR_MEASUREMENT_RECORDED_KIND,
        {
            **result_payload,
            "dimensions": {
                "identity": act_occurrence_id,
                "content": "exact adjacency-pair measurements",
                "source_provenance": [adjacency_evidence_event_id, *source_ids],
                "responsibility": ADJACENCY_PAIR_MEASUREMENT_RESPONSIBILITY,
                "responsible_boundary": "this Seed",
                "authority": "unestablished",
                "evidence_scope": (
                    "measurement Evidence only; establishes no classification, "
                    "represented relation, or Standing beyond this result"
                ),
                "scope_locality": f"locality:{locality_id}",
                "occurrence_preservation": "one exact adjacency-pair measurement Measurement occurrence recorded",
            },
            "downstream_act_id": act_id,
            "act_occurrence_id": act_occurrence_id,
            "responsible_act_evidence_id": act_evidence.id,
            "participation": participation,
            "yield_evidence_id": yield_evidence.id,
            "locality_evidence_id": locality_evidence.id,
            "known_loss": [],
            "unknowns": ["what any carried representation means remains Unknown"],
            "conflicts": [],
        },
        locality_id=locality_id,
    )


def record_adjacency_pair_measurements(
    ledger: EventLedger,
    *,
    locality_id: str,
    finding_event_id: str,
) -> Event:
    """Preserve one exact bounded adjacency-pair measurement Measurement result."""

    finding = ledger.get(finding_event_id)
    if (
        finding is None
        or finding.locality_id != locality_id
    ):
        raise PreservedMaterialMeasurementError(
            "the read pair finding is outside this Measurement locality"
        )
    source_ids = finding.payload.get("input_event_ids")
    if not isinstance(source_ids, list):
        raise PreservedMaterialMeasurementError(
            "the read pair finding carries no exact source occurrences"
        )
    source_occurrences = []
    for source_id in source_ids:
        source = ledger.get(source_id) if isinstance(source_id, str) else None
        if source is None:
            raise PreservedMaterialMeasurementError(
                "the read pair finding names an absent source occurrence"
            )
        source_occurrences.append(source)
    measurements = measure_adjacency_pairs_from_finding(
        ledger,
        finding_event_id=finding_event_id,
        occurrences=source_occurrences,
    )
    applicable_inputs = [
        {
            "input_reference": finding_event_id,
            "role": PAIR_FINDING_PARTICIPATION_ROLE,
            "standing": "applicable",
        },
        *[
            {
                "input_reference": source_id,
                "role": SOURCE_OCCURRENCE_PARTICIPATION_ROLE,
                "standing": "applicable",
            }
            for source_id in source_ids
        ],
    ]
    return _record_adjacency_pair_measurement_result(
        ledger,
        locality_id=locality_id,
        adjacency_evidence_event_id=finding_event_id,
        source_ids=tuple(source_ids),
        measurements=measurements,
        applicable_inputs=applicable_inputs,
    )


def _adjacency_pair_measurement_from_payload(
    value: object,
) -> AdjacencyPairMeasurement:
    if not isinstance(value, dict):
        raise PreservedMaterialMeasurementError(
            "a recorded adjacency-pair measurement is not an exact coordinate mapping"
        )

    def positioned(item: object) -> PositionedRepresentationOccurrence | None:
        if item is None:
            return None
        if not isinstance(item, dict):
            raise PreservedMaterialMeasurementError(
                "a recorded position is not an exact coordinate mapping"
            )
        source_id = item.get("source_occurrence_id")
        position = item.get("position")
        representation = item.get("representation")
        if (
            not isinstance(source_id, str)
            or not source_id
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
            source_id,
            position,
            representation,
        )

    pair_value = value.get("pair_occurrence")
    if not isinstance(pair_value, dict):
        raise PreservedMaterialMeasurementError(
            "a recorded adjacency-pair measurement carries no exact pair occurrence"
        )
    ordered_pair = pair_value.get("ordered_pair")
    if (
        not isinstance(ordered_pair, list)
        or len(ordered_pair) != 2
        or not all(isinstance(item, str) and item for item in ordered_pair)
    ):
        raise PreservedMaterialMeasurementError(
            "a recorded adjacency-pair measurement carries no exact ordered pair"
        )
    pair_left = positioned(pair_value.get("left"))
    pair_right = positioned(pair_value.get("right"))
    if pair_left is None or pair_right is None:
        raise PreservedMaterialMeasurementError(
            "a recorded pair occurrence is missing one exact position"
        )
    source_id = value.get("source_occurrence_id")
    exact_order = value.get("exact_order")
    evidence = value.get("evidence")
    if (
        not isinstance(source_id, str)
        or not source_id
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
            "a recorded adjacency-pair measurement carries malformed bounds"
        )
    return AdjacencyPairMeasurement(
        left_occurrence=positioned(value.get("left_occurrence")),
        pair_occurrence=ExactAdjacencyPairOccurrence(
            AdjacencyPair(*ordered_pair),
            pair_left,
            pair_right,
        ),
        right_occurrence=positioned(value.get("right_occurrence")),
        source_occurrence_id=source_id,
        exact_order=tuple(exact_order),
        evidence=evidence,
    )


def get_recorded_adjacency_pair_measurements(
    ledger: EventLedger,
    event_id: str,
) -> tuple[AdjacencyPairMeasurement, ...] | None:
    """Read an exact recorded result without repeating its Measurement."""

    event = ledger.get(event_id)
    if event is None:
        return None
    if (
        event.kind != ADJACENCY_PAIR_MEASUREMENT_RECORDED_KIND
        or ledger.integrity_of(event_id) == CORRUPTED
    ):
        raise PreservedMaterialMeasurementError(
            "the adjacency-pair measurement result event is absent or corrupted"
        )
    adjacency_evidence_id = event.payload.get("adjacency_evidence_event_id")
    source_ids = event.payload.get("source_occurrence_ids")
    carried_measurements = event.payload.get("measurements")
    if (
        not isinstance(adjacency_evidence_id, str)
        or not adjacency_evidence_id
        or not isinstance(source_ids, list)
        or not all(isinstance(value, str) and value for value in source_ids)
        or not isinstance(carried_measurements, list)
    ):
        raise PreservedMaterialMeasurementError(
            "the adjacency-pair measurement result carries malformed result coordinates"
        )
    result_payload = {
        "adjacency_evidence_event_id": adjacency_evidence_id,
        "source_occurrence_ids": source_ids,
        "measurements": carried_measurements,
    }
    act_evidence_id = event.payload.get("responsible_act_evidence_id")
    yield_evidence_id = event.payload.get("yield_evidence_id")
    locality_evidence_id = event.payload.get("locality_evidence_id")
    if not all(
        isinstance(value, str) and value
        for value in (act_evidence_id, yield_evidence_id, locality_evidence_id)
    ):
        raise PreservedMaterialMeasurementError(
            "the adjacency-pair measurement result carries malformed Evidence references"
        )
    act_evidence = ledger.get(act_evidence_id)
    yield_evidence = ledger.get(yield_evidence_id)
    locality_evidence = ledger.get(locality_evidence_id)
    if (
        act_evidence is None
        or act_evidence.kind != ADJACENCY_PAIR_MEASUREMENT_ACT_EVIDENCE_KIND
        or yield_evidence is None
        or yield_evidence.kind != "operator.yield.evidence_recorded"
        or locality_evidence is None
        or locality_evidence.kind != ADJACENCY_PAIR_MEASUREMENT_LOCALITY_EVIDENCE_KIND
    ):
        raise PreservedMaterialMeasurementError(
            "the adjacency-pair measurement result carries incomplete edge Evidence"
        )
    act_occurrence_id = event.payload.get("act_occurrence_id")
    downstream_act_id = event.payload.get("downstream_act_id")
    commitment = yield_commitment(ADJACENCY_PAIR_MEASUREMENT_CONVENTION, result_payload)
    if (
        not isinstance(act_occurrence_id, str)
        or not isinstance(downstream_act_id, str)
        or act_evidence.payload.get("downstream_act_id") != downstream_act_id
        or act_evidence.payload.get("act_occurrence_id") != act_occurrence_id
        or yield_evidence.payload.get("dimensions", {}).get("act_occurrence_id")
        != act_occurrence_id
        or locality_evidence.payload.get("act_occurrence_id")
        != act_occurrence_id
        or act_evidence.payload.get("result_commitment") != commitment
        or yield_evidence.payload.get("yield_commitment") != commitment
        or yield_evidence.payload.get("yield_convention")
        != ADJACENCY_PAIR_MEASUREMENT_CONVENTION
        or locality_evidence.payload.get("carried_content") != result_payload
    ):
        raise PreservedMaterialMeasurementError(
            "the adjacency-pair measurement edge Evidence concerns different coordinates"
        )
    anchor = ledger.get(adjacency_evidence_id)
    sources: dict[str, Event] = {}
    source_texts: dict[str, str] = {}
    if anchor is not None and _is_established_after_measurement(anchor):
        expected_inputs = [
            {
                "input_reference": adjacency_evidence_id,
                "role": PAIR_FINDING_PARTICIPATION_ROLE,
                "standing": "applicable",
            },
            *[
                {
                    "input_reference": source_id,
                    "role": SOURCE_OCCURRENCE_PARTICIPATION_ROLE,
                    "standing": "applicable",
                }
                for source_id in source_ids
            ],
        ]
        if (
            ledger.integrity_of(adjacency_evidence_id) == CORRUPTED
            or anchor.locality_id != event.locality_id
            or anchor.payload.get("input_event_ids") != source_ids
        ):
            raise PreservedMaterialMeasurementError(
                "the adjacency-pair measurement pair-finding Evidence does not read"
            )
        for source_id in source_ids:
            source = ledger.get(source_id)
            text = source.payload.get("represented_material") if source is not None else None
            if (
                source is None
                or source.kind != INGEST_OCCURRED_KIND
                or ledger.integrity_of(source_id) == CORRUPTED
                or source.locality_id != event.locality_id
                or not isinstance(text, str)
            ):
                raise PreservedMaterialMeasurementError(
                    "the adjacency-pair measurement source Evidence does not read"
                )
            sources[source_id] = source
            source_texts[source_id] = text
    elif (
        anchor is not None
        and anchor.kind == REPRESENTATION_EMISSION_LOCALITY_EVIDENCE_KIND
        and ledger.integrity_of(anchor.id) != CORRUPTED
        and len(source_ids) == 1
    ):
        source = ledger.get(source_ids[0])
        text = source.payload.get("emitted_representation") if source is not None else None
        if (
            source is None
            or source.kind != REPRESENTATION_EMITTED_KIND
            or ledger.integrity_of(source.id) == CORRUPTED
            or source.locality_id != event.locality_id
            or source.payload.get("locality_evidence_id") != anchor.id
            or anchor.payload.get("act_occurrence_id")
            != source.payload.get("act_occurrence_id")
            or anchor.payload.get("content_kind") != "text"
            or anchor.payload.get("carried_content") != text
            or not isinstance(text, str)
        ):
            raise PreservedMaterialMeasurementError(
                "the emitted-representation Locality Evidence does not read"
            )
        sources[source.id] = source
        source_texts[source.id] = text
        expected_inputs = [
            {
                "input_reference": anchor.id,
                "role": EMISSION_LOCALITY_PARTICIPATION_ROLE,
                "standing": "applicable",
            },
            {
                "input_reference": source.id,
                "role": EMISSION_OCCURRENCE_PARTICIPATION_ROLE,
                "standing": "applicable",
            },
        ]
    else:
        raise PreservedMaterialMeasurementError(
            "the adjacency-pair measurement Evidence anchor does not read"
        )
    expected_participation = [
        {
            "subject_reference": item["input_reference"],
            "role": item["role"],
            "act_occurrence_id": act_occurrence_id,
        }
        for item in expected_inputs
    ]
    if (
        act_evidence.payload.get("input_applicability") != expected_inputs
        or act_evidence.payload.get("participation") != expected_participation
        or event.payload.get("participation") != expected_participation
    ):
        raise PreservedMaterialMeasurementError(
            "the adjacency-pair measurement Act Evidence concerns different inputs or Participation coordinates"
        )
    measurements = tuple(
        _adjacency_pair_measurement_from_payload(value)
        for value in carried_measurements
    )
    if any(
        measurement.evidence.get("adjacency_evidence_event_id") != adjacency_evidence_id
        or measurement.source_occurrence_id not in sources
        or measurement.evidence.get("exact_representation")
        != source_texts[measurement.source_occurrence_id]
        or measurement.evidence.get("locality_id") != event.locality_id
        for measurement in measurements
    ):
        raise PreservedMaterialMeasurementError(
            "a carried adjacency-pair measurement names different Evidence"
        )
    return measurements


def record_adjacency_pair_measurement_compare(
    ledger: EventLedger,
    *,
    locality_id: str,
    measurement_event_ids: Iterable[str],
) -> Event:
    """Compare exact durable measurement results and preserve the bounded result."""

    input_ids = tuple(measurement_event_ids)
    if (
        len(input_ids) < 2
        or any(not isinstance(value, str) or not value for value in input_ids)
        or len(set(input_ids)) != len(input_ids)
    ):
        raise PreservedMaterialMeasurementError(
            "measurement Compare requires at least two distinct recorded measurement occurrences"
        )
    measurements: list[AdjacencyPairMeasurement] = []
    for event_id in input_ids:
        event = ledger.get(event_id)
        read = get_recorded_adjacency_pair_measurements(ledger, event_id)
        if (
            event is None
            or read is None
            or event.locality_id != locality_id
        ):
            raise PreservedMaterialMeasurementError(
                "an measurement Compare input does not read in this locality"
            )
        measurements.extend(read)
    compared = compare_adjacency_pair_measurements(measurements)
    act_id = new_id("adjacency_pair_measurement_compare_act")
    act_occurrence_id = new_id("adjacency_pair_measurement_compare_occurrence")
    result_payload = {
        "measurement_event_ids": list(input_ids),
        "comparison": compared,
    }
    participation = [
        {
            "subject_reference": event_id,
            "role": MEASUREMENT_COMPARE_INPUT_ROLE,
            "act_occurrence_id": act_occurrence_id,
        }
        for event_id in input_ids
    ]
    act_evidence = ledger.append(
        ADJACENCY_PAIR_MEASUREMENT_COMPARE_ACT_EVIDENCE_KIND,
        {
            "downstream_act_id": act_id,
            "act_occurrence_id": act_occurrence_id,
            "act": "Compare exact adjacency-pair measurement results",
            "responsibility": ADJACENCY_PAIR_MEASUREMENT_COMPARE_RESPONSIBILITY,
            "responsible_boundary": "this Seed",
            "authority": "unestablished",
            "evidence_scope": (
                "Evidence concerning this exact Compare occurrence, its exact "
                "participants, and its exact result commitment"
            ),
            "participation": participation,
            "result_commitment": yield_commitment(
                ADJACENCY_PAIR_MEASUREMENT_COMPARE_CONVENTION,
                result_payload,
            ),
        },
        locality_id=locality_id,
    )
    yield_evidence = _record_yield_evidence(
        ledger,
        locality_id=locality_id,
        convention=ADJACENCY_PAIR_MEASUREMENT_COMPARE_CONVENTION,
        yielding_act="Compare exact adjacency-pair measurement results",
        act_occurrence_id=act_occurrence_id,
        yielded_result_kind="bounded adjacency-pair measurement comparison",
        result_identity=f"adjacency-pair-measurement-compare:{act_occurrence_id}",
        yielded_content=result_payload,
        responsibility=ADJACENCY_PAIR_MEASUREMENT_COMPARE_RESPONSIBILITY,
        live_boundary="adjacency_pair_measurement_compare",
        responsible_boundary="this Seed",
    )
    locality_evidence = ledger.append(
        ADJACENCY_PAIR_MEASUREMENT_COMPARE_LOCALITY_EVIDENCE_KIND,
        {
            "act_occurrence_id": act_occurrence_id,
            "carried_content": result_payload,
        },
        locality_id=locality_id,
    )
    return ledger.append(
        ADJACENCY_PAIR_MEASUREMENT_COMPARE_RECORDED_KIND,
        {
            **result_payload,
            "downstream_act_id": act_id,
            "act_occurrence_id": act_occurrence_id,
            "responsibility": ADJACENCY_PAIR_MEASUREMENT_COMPARE_RESPONSIBILITY,
            "responsible_boundary": "this Seed",
            "participation": participation,
            "responsible_act_evidence_id": act_evidence.id,
            "yield_evidence_id": yield_evidence.id,
            "locality_evidence_id": locality_evidence.id,
            "unknowns": [
                "whether any repeated source arrangement represents a grammar distinction remains Unknown"
            ],
        },
        locality_id=locality_id,
    )


def get_recorded_adjacency_pair_measurement_compare(
    ledger: EventLedger,
    event_id: str,
) -> dict[str, object] | None:
    """Read one durable Compare result without repeating the Compare."""

    event = ledger.get(event_id)
    if event is None:
        return None
    if (
        event.kind != ADJACENCY_PAIR_MEASUREMENT_COMPARE_RECORDED_KIND
        or ledger.integrity_of(event_id) == CORRUPTED
    ):
        raise PreservedMaterialMeasurementError(
            "the recorded measurement Compare is absent or corrupted"
        )
    input_ids = event.payload.get("measurement_event_ids")
    compared = event.payload.get("comparison")
    if (
        not isinstance(input_ids, list)
        or len(input_ids) < 2
        or len(set(input_ids)) != len(input_ids)
        or not all(isinstance(value, str) and value for value in input_ids)
        or not isinstance(compared, dict)
    ):
        raise PreservedMaterialMeasurementError(
            "the recorded measurement Compare carries malformed coordinates"
        )
    result_payload = {
        "measurement_event_ids": input_ids,
        "comparison": compared,
    }
    act_evidence = ledger.get(event.payload.get("responsible_act_evidence_id"))
    yield_evidence = ledger.get(event.payload.get("yield_evidence_id"))
    locality_evidence = ledger.get(event.payload.get("locality_evidence_id"))
    evidence = (act_evidence, yield_evidence, locality_evidence)
    if any(
        item is None or ledger.integrity_of(item.id) == CORRUPTED
        for item in evidence
    ):
        raise PreservedMaterialMeasurementError(
            "the recorded measurement Compare carries absent or corrupted edge Evidence"
        )
    assert act_evidence is not None
    assert yield_evidence is not None
    assert locality_evidence is not None
    act_occurrence_id = event.payload.get("act_occurrence_id")
    commitment = yield_commitment(
        ADJACENCY_PAIR_MEASUREMENT_COMPARE_CONVENTION,
        result_payload,
    )
    expected_participation = [
        {
            "subject_reference": input_id,
            "role": MEASUREMENT_COMPARE_INPUT_ROLE,
            "act_occurrence_id": act_occurrence_id,
        }
        for input_id in input_ids
    ]
    if (
        act_evidence.kind != ADJACENCY_PAIR_MEASUREMENT_COMPARE_ACT_EVIDENCE_KIND
        or locality_evidence.kind
        != ADJACENCY_PAIR_MEASUREMENT_COMPARE_LOCALITY_EVIDENCE_KIND
        or yield_evidence.kind != "operator.yield.evidence_recorded"
        or act_evidence.payload.get("act_occurrence_id") != act_occurrence_id
        or yield_evidence.payload.get("dimensions", {}).get("act_occurrence_id")
        != act_occurrence_id
        or locality_evidence.payload.get("act_occurrence_id") != act_occurrence_id
        or act_evidence.payload.get("result_commitment") != commitment
        or act_evidence.payload.get("authority") != "unestablished"
        or act_evidence.payload.get("evidence_scope")
        != (
            "Evidence concerning this exact Compare occurrence, its exact "
            "participants, and its exact result commitment"
        )
        or yield_evidence.payload.get("yield_commitment") != commitment
        or yield_evidence.payload.get("yield_convention")
        != ADJACENCY_PAIR_MEASUREMENT_COMPARE_CONVENTION
        or locality_evidence.payload.get("carried_content") != result_payload
        or act_evidence.payload.get("participation") != expected_participation
        or event.payload.get("participation") != expected_participation
    ):
        raise PreservedMaterialMeasurementError(
            "the recorded measurement Compare edge Evidence concerns different coordinates"
        )
    for input_id in input_ids:
        event = ledger.get(input_id)
        if (
            event is None
            or ledger.integrity_of(input_id) == CORRUPTED
            or event.locality_id != event.locality_id
            or get_recorded_adjacency_pair_measurements(ledger, input_id) is None
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
            for token in _positions(event.payload.get("represented_material"))
        }
        everywhere = seen if everywhere is None else (everywhere & seen)
    offered = {
        token
        for event in material
        for token in _positions(event.payload.get("represented_material"))
    }
    if everywhere is not None:
        offered &= everywhere
    return sorted(offered)


def enumerate_displacements(
    occurrences: Iterable[Event], representation: str, *, direction: str = "after"
) -> list[int]:
    """Every positional displacement at which this material has a position.

    Nothing is preferred and nothing is chosen. An occurrence carrying the
    representation at index *i* has a position at displacement *d* whenever the
    occurrence extends that far, so the displacements returned are a finding about
    how far the material reaches from where the representation sits.

    A displacement absent here is absent because no occurrence reaches it, not
    because it was judged uninteresting. `#2397` recorded that a coordinate
    measured with one value is not thereby an instruction to vary it; this does
    not vary it either, it reports what the material makes measurable.
    """

    if direction not in ("after", "before"):
        raise PreservedMaterialMeasurementError(
            "a displacement is measured before or after, and nothing else"
        )
    reachable: set[int] = set()
    for event in occurrences:
        parts = _positions(event.payload.get("represented_material"))
        for index, part in enumerate(parts):
            if part != representation:
                continue
            span = len(parts) - 1 - index if direction == "after" else index
            reachable.update(range(1, span + 1))
    return sorted(reachable)


def measure_at_displacement(
    occurrences: Iterable[Event],
    representation: str,
    *,
    displacement: int,
    direction: str = "after",
    counting_scope: str,
    premise_event_id: str | None = None,
) -> MeasurementFinding:
    """Count what occupies one stated displacement from one representation.

    The displacement is a parameter of the measurement rather than a constant
    of the code, and it is recorded on the finding, so a later survey measures
    the value actually used instead of a value the indexing hid.
    """

    if displacement < 1:
        raise PreservedMaterialMeasurementError(
            "a displacement is at least one position away"
        )
    step = displacement if direction == "after" else -displacement

    def occupant_of(text: str) -> str | None:
        parts = _positions(text)
        for index, part in enumerate(parts):
            if part != representation:
                continue
            at = index + step
            if 0 <= at < len(parts):
                return parts[at]
        return None

    return measure_occupancy(
        occurrences,
        declared=DeclaredMeasurement(
            representation_measured=(
                f"the representation {displacement} position(s) {direction} "
                f"{representation!r}"
            ),
            equivalence_rule=EQUIVALENCE_RULE,
            counting_scope=counting_scope,
            premise_event_id=premise_event_id,
            measured_after=representation,
            distinction=direction,
            relative_to=(representation,),
            measured_position={
                "anchored_on": "the representation",
                "direction": direction,
                "displacement": displacement,
            },
        ),
        occupant_of=occupant_of,
    )


def measure_after(
    occurrences: Iterable[Event],
    representation: str,
    *,
    counting_scope: str,
    premise_event_id: str | None = None,
) -> MeasurementFinding:
    """Count what occupies the position immediately after a representation.

    One displacement of the family :func:`measure_at_displacement` covers, kept
    because the continuation and its tests name it. It carries no privilege;
    `#2403` records that no displacement is preferred.
    """

    return measure_at_displacement(
        occurrences,
        representation,
        displacement=1,
        direction="after",
        counting_scope=counting_scope,
        premise_event_id=premise_event_id,
    )
