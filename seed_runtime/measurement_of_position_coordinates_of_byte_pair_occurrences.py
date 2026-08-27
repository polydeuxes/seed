"""Measure first and second position coordinates of each byte-pair occurrence.

The exact source material result bounds the addressed occurrences. The Measurement records
first and second byte values with their position coordinates; it establishes no
recurrence, represented relation, character, word, or meaning.
"""

from __future__ import annotations

from copy import deepcopy
from typing import TYPE_CHECKING, Any, Iterator, NamedTuple

if TYPE_CHECKING:
    from seed_runtime.byte_measurement import (
        RecordedAssertionCarriedByLocalityMovement,
    )

from seed_runtime.event import Event
from seed_runtime.events import CORRUPTED, EventLedger, EventLedgerBoundary
from seed_runtime.yield_relation import (
    RECORDED_YIELD_RELATION_EVENT,
    _record_yield_relation,
    read_requirements_of_yield_relation,
)
from seed_runtime.material_source import (
    exact_material_result_bytes,
    read_exact_material_result,
)


BYTE_PAIR_OCCURRENCE_POSITION_SUBJECT_TO_ACT_BINDING_RECORDED_KIND = (
    "operator.measurement_of_position_coordinates_of_byte_pair_occurrences."
    "subject_to_act_binding_recorded"
)
BYTE_PAIR_OCCURRENCE_POSITION_ACT_OCCURRENCE_EVENT = (
    "operator.measurement_of_position_coordinates_of_byte_pair_occurrences."
    "act_occurrence_recorded"
)
BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND = (
    "operator.measurement_of_position_coordinates_of_byte_pair_occurrences."
    "recording_occurrence_of_result"
)
RESULT_KIND = "result of Measurement of position coordinates of byte-pair occurrences"


EXACT_ACT = "Measurement of position coordinates of byte-pair occurrences"

EVENT_KIND_BOOK_CLAUSES = {
    BYTE_PAIR_OCCURRENCE_POSITION_SUBJECT_TO_ACT_BINDING_RECORDED_KIND: "01.Source.D",
    BYTE_PAIR_OCCURRENCE_POSITION_ACT_OCCURRENCE_EVENT: "02.Acts.A",
    BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND: "01.Source.D",
}
class FindingOfPositionCoordinatesOfBytePairOccurrences(NamedTuple):
    source_material_result_occurrence_identity: str
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


class UnboundPositionCoordinateMeasurementMaterialResultReading(NamedTuple):
    """Exact material-result coordinates read before this Measurement binding.

    This bounded runtime read preserves exact source coordinates beside the
    absence of this Measurement's binding or result through B. It establishes
    no Locality relation, subject-to-Act binding, Applicability, or Act.
    """

    source_material_result_occurrence_identity: str
    source_result_identity: str
    source_locality_identity: str
    source_completeness_boundary_identity: str
    bounded_locality_replay_through_event_occurrence_identity: str
    bounded_locality_replay_append_boundary_identity: str
    act_occurrence_identity: str
    yield_relation_identity: str
    source_boundary: str
    exact_material: bytes
    source_occurrence_references: tuple[str, ...]


class ReferenceToRecordedPositionOfBytePairOccurrence(
    NamedTuple
):
    recorded_occurrence_identity: str
    assertion_position: int
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

    @property
    def first_position_coordinate_reference(self) -> dict[str, Any]:
        return _source_position_coordinate_reference(
            source_material_result_occurrence_identity=(
                self.source_material_result_occurrence_identity
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
            source_material_result_occurrence_identity=(
                self.source_material_result_occurrence_identity
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
        raise ValueError(f"exact material-result subject has malformed {coordinate}")
    return tuple(value)


def _has_exact_material_result_locality(
    ledger: EventLedger, source_identity: str
) -> bool:
    """Whether the exact material result carries the Locality prerequisite."""

    from seed_runtime.material_source import (
        read_material_result_locality_requirements,
    )

    return all(
        read_material_result_locality_requirements(
            ledger,
            recorded_result_event_identity=source_identity,
        ).values()
    )


def _material_result_identities_from_bounded_replay(
    bounded_locality_replay: dict[str, Any],
) -> tuple[str, ...]:
    """Resolve exact material results from one bounded current-coordinate read."""

    material_results = bounded_locality_replay.get("material_result_occurrences")
    if type(material_results) is not list:
        raise ValueError(
            "declared Measurement source resolution requires exact bounded "
            "Locality replay"
        )
    identities: list[str] = []
    for occurrence in material_results:
        if (
            type(occurrence) is not dict
            or type(occurrence.get("result_occurrence_identity")) is not str
            or not occurrence["result_occurrence_identity"]
        ):
            raise ValueError(
                "bounded Locality replay contains a malformed material result"
            )
        identities.append(occurrence["result_occurrence_identity"])
    return tuple(identities)


def _recorded_position_coordinate_measurement_sources_from_bounded_replay(
    ledger: EventLedger,
    bounded_locality_replay: dict[str, Any],
) -> set[str]:
    """Resolve sources from prior occurrences already validated by replay."""

    recorded_sources: set[str] = set()
    for occurrence_identity in bounded_locality_replay[
        "subject_to_act_binding_occurrences"
    ]:
        event = ledger.get(occurrence_identity)
        if (
            event is None
            or event.kind
            != BYTE_PAIR_OCCURRENCE_POSITION_SUBJECT_TO_ACT_BINDING_RECORDED_KIND
        ):
            continue
        if ledger.integrity_of(event.identity) == CORRUPTED:
            raise ValueError(
                "bounded Locality replay contains a corrupted position-coordinate "
                "Measurement occurrence"
            )
        source_identity = event.material.get(
            "source_material_result_occurrence_identity"
        )
        if type(source_identity) is not str or not source_identity:
            raise ValueError(
                "bounded Locality replay contains a malformed position-coordinate "
                "Measurement occurrence"
            )
        recorded_sources.add(source_identity)
    for occurrence_identity in bounded_locality_replay["measurement_occurrences"]:
        event = ledger.get(occurrence_identity)
        if (
            event is None
            or event.kind != BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND
        ):
            continue
        if ledger.integrity_of(event.identity) == CORRUPTED:
            raise ValueError(
                "bounded Locality replay contains a corrupted position-coordinate "
                "Measurement occurrence"
            )
        source_identity = event.material.get(
            "source_material_result_occurrence_identity"
        )
        if type(source_identity) is not str or not source_identity:
            raise ValueError(
                "bounded Locality replay contains a malformed position-coordinate "
                "Measurement occurrence"
            )
        recorded_sources.add(source_identity)
    return recorded_sources


def _unbound_position_coordinate_measurement_material_results_from_bounded_locality_replay(
    ledger: EventLedger,
    bounded_locality_replay: dict[str, Any],
    *,
    locality_identity: str,
) -> tuple[UnboundPositionCoordinateMeasurementMaterialResultReading, ...]:
    if (
        not isinstance(ledger, EventLedger)
        or type(locality_identity) is not str
        or not locality_identity
        or type(bounded_locality_replay) is not dict
        or bounded_locality_replay.get("locality_identity") != locality_identity
        or type(bounded_locality_replay.get("material_result_occurrences")) is not list
        or type(
            bounded_locality_replay.get("subject_to_act_binding_occurrences")
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
    sources: list[UnboundPositionCoordinateMeasurementMaterialResultReading] = []
    for occurrence in bounded_locality_replay["material_result_occurrences"]:
        if (
            type(occurrence) is not dict
            or type(occurrence.get("result_occurrence_identity")) is not str
            or not occurrence["result_occurrence_identity"]
        ):
            raise ValueError(
                "bounded Locality replay contains a malformed material result"
            )
        source_identity = occurrence["result_occurrence_identity"]
        if source_identity in recorded_sources:
            continue
        source = ledger.get(source_identity)
        if source is None or source.locality_identity != locality_identity:
            raise ValueError(
                "bounded Locality replay contains an absent material result"
            )
        if not all(
            type(source.material.get(key)) is str and source.material[key]
            for key in (
                "act_occurrence_identity",
                "yield_relation_identity",
            )
        ):
            # Preserved legacy material lacks the exact source Act/Yield
            # coordinates required by this binding subject.
            continue
        source = read_exact_material_result(ledger, source_identity)
        material = source.material
        exact_coordinates = {
            key: material.get(key)
            for key in (
                "result_identity",
                "act_occurrence_identity",
                "yield_relation_identity",
                "source_boundary",
            )
        }
        if any(
            type(value) is not str or not value
            for value in exact_coordinates.values()
        ):
            raise ValueError("exact material-result subject coordinates are malformed")
        sources.append(
            UnboundPositionCoordinateMeasurementMaterialResultReading(
                source_material_result_occurrence_identity=source.identity,
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
                act_occurrence_identity=exact_coordinates[
                    "act_occurrence_identity"
                ],
                yield_relation_identity=exact_coordinates[
                    "yield_relation_identity"
                ],
                source_boundary=exact_coordinates["source_boundary"],
                exact_material=exact_material_result_bytes(source),
                source_occurrence_references=_exact_string_list(
                    material.get("source_occurrence_references"),
                    coordinate="source_occurrence_references",
                ),
            )
        )
    return tuple(sources)


def read_unbound_position_coordinate_measurement_material_results_through(
    ledger: EventLedger,
    *,
    locality_identity: str,
    through_event_occurrence_identity: str,
) -> tuple[UnboundPositionCoordinateMeasurementMaterialResultReading, ...]:
    """Read exact unbound material results for this Measurement through B.

    The non-recording read establishes neither an exact Locality
    relation nor a subject-to-Act binding for any returned result.
    """

    from seed_runtime.operator_current_coordinates import (
        read_operator_current_coordinates_through,
    )

    bounded_locality_replay = read_operator_current_coordinates_through(
        ledger,
        locality_identity=locality_identity,
        through_event_occurrence_identity=through_event_occurrence_identity,
    )
    return _unbound_position_coordinate_measurement_material_results_from_bounded_locality_replay(
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
        type(finding.source_material_result_occurrence_identity) is not str
        or not finding.source_material_result_occurrence_identity
        or type(finding.source_locality_identity) is not str
        or not finding.source_locality_identity
        or type(finding.completeness_boundary) is not EventLedgerBoundary
        or type(finding.exact_material) is not bytes
    ):
        raise ValueError("byte-pair position-coordinate finding carries no exact source")


def _measure_through(
    ledger: EventLedger,
    *,
    source_material_result_occurrence_identity: str,
    boundary: EventLedgerBoundary,
) -> FindingOfPositionCoordinatesOfBytePairOccurrences:
    source = read_exact_material_result(ledger, source_material_result_occurrence_identity)
    exact_boundary = ledger.append_boundary_through_occurrence(source.identity)
    if type(boundary) is not EventLedgerBoundary or boundary != exact_boundary:
        raise ValueError(
            "byte-pair position-coordinate Measurement requires the exact source boundary"
        )
    exact = exact_material_result_bytes(source)
    finding = FindingOfPositionCoordinatesOfBytePairOccurrences(
        source_material_result_occurrence_identity=source.identity,
        source_locality_identity=source.locality_identity,
        completeness_boundary=boundary,
        exact_material=exact,
    )
    _validate_finding(finding)
    return finding


def measure_position_coordinates_of_byte_pair_occurrences(
    ledger: EventLedger,
    *,
    source_material_result_occurrence_identity: str,
) -> FindingOfPositionCoordinatesOfBytePairOccurrences:
    """Measure each exact byte-pair window in one material result."""

    if not isinstance(ledger, EventLedger):
        raise TypeError("byte-pair position-coordinate Measurement requires one EventLedger")
    if (
        type(source_material_result_occurrence_identity) is not str
        or not source_material_result_occurrence_identity
    ):
        raise ValueError("byte-pair position-coordinate Measurement requires one material result")
    return _measure_through(
        ledger,
        source_material_result_occurrence_identity=source_material_result_occurrence_identity,
        boundary=ledger.append_boundary_through_occurrence(
            source_material_result_occurrence_identity
        ),
    )


def _binding_reference(binding: Event) -> dict[str, Any]:
    return {
        "recorded_occurrence_identity": binding.identity,
        "book_clause_identity": binding.material["book_clause_identity"],
        "exact_act_identity": binding.material["exact_act_identity"],
        "subject_reference": deepcopy(binding.material["subject_reference"]),
        "result_boundary_identity": binding.material[
            "result_boundary_identity"
        ],
    }


def _binding_material(
    finding: FindingOfPositionCoordinatesOfBytePairOccurrences,
    *,
    through_event_occurrence_identity: str,
    exact_act_identity: str,
    act_occurrence_identity: str,
    measurement_result_identity: str,
) -> dict[str, Any]:
    return {
        "subject_reference": {
            "recorded_occurrence_identity": (
                finding.source_material_result_occurrence_identity
            )
        },
        "exact_act_identity": exact_act_identity,
        "act_occurrence_identity": act_occurrence_identity,
        "measurement_result_identity": measurement_result_identity,
        "result_boundary_identity": measurement_result_identity,
        "book_clause_identity": "01.Source.D",
        "source_material_result_occurrence_identity": (
            finding.source_material_result_occurrence_identity
        ),
        "source_locality_identity": finding.source_locality_identity,
        "completeness_boundary_identity": finding.completeness_boundary.identity,
        "through_event_occurrence_identity": through_event_occurrence_identity,
    }


def _require_current_coordinates(
    ledger: EventLedger,
    *,
    locality_identity: str,
    current_coordinates: dict[str, Any],
    source_material_result_occurrence_identity: str | None = None,
    binding_occurrence_identity: str | None = None,
) -> str:
    """Validate the exact current coordinates this Measurement reads.

    The source material result, Locality, and through occurrence are each
    validated against the ledger. Coordinates this Measurement does not read
    are not authenticated here.
    """

    if type(current_coordinates) is not dict:
        raise ValueError(
            "byte-pair position-coordinate Measurement requires exact current coordinates"
        )
    boundary = current_coordinates.get("through_event_occurrence_identity")
    material_results = current_coordinates.get("material_result_occurrences")
    bindings = current_coordinates.get("subject_to_act_binding_occurrences")
    carried_material_results = {
        occurrence.get("result_occurrence_identity")
        for occurrence in material_results or ()
        if type(occurrence) is dict
    }
    source_has_exact_locality = bool(
        source_material_result_occurrence_identity is None
        or _has_exact_material_result_locality(
            ledger, source_material_result_occurrence_identity
        )
    )
    if (
        current_coordinates.get("locality_identity") != locality_identity
        or type(boundary) is not str
        or not boundary
        or (
            source_material_result_occurrence_identity is not None
            and (
                source_material_result_occurrence_identity
                not in carried_material_results
                or not source_has_exact_locality
            )
        )
        or (
            binding_occurrence_identity is not None
            and (
                type(bindings) is not dict
                or bindings.get(binding_occurrence_identity, object()) is not None
            )
        )
    ):
        raise ValueError(
            "byte-pair position-coordinate Measurement requires exact current coordinates"
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
            "byte-pair position-coordinate Measurement requires exact current coordinates"
        )
    return boundary


def _require_exact_through_event_occurrence(
    ledger: EventLedger,
    *,
    locality_identity: str,
    through_event_occurrence_identity: str,
    source_material_result_occurrence_identity: str,
) -> str:
    """Validate the exact earlier boundary that supplies this binding subject."""

    if (
        type(through_event_occurrence_identity) is not str
        or not through_event_occurrence_identity
    ):
        raise ValueError(
            "byte-pair position-coordinate binding requires one exact "
            "through-occurrence boundary"
        )
    boundary_event = ledger.get(through_event_occurrence_identity)
    try:
        boundary = ledger.append_boundary_through_occurrence(
            through_event_occurrence_identity
        )
        order = (source_material_result_occurrence_identity,)
        if (
            source_material_result_occurrence_identity
            != through_event_occurrence_identity
        ):
            order = (
                source_material_result_occurrence_identity,
                through_event_occurrence_identity,
            )
        ledger.occurrences_in_append_order(order, locality_identity=locality_identity)
    except ValueError as error:
        raise ValueError(
            "byte-pair position-coordinate binding requires one exact "
            "through-occurrence boundary"
        ) from error
    if (
        boundary_event is None
        or boundary_event.locality_identity != locality_identity
        or ledger.integrity_of(boundary_event.identity) == CORRUPTED
        or not _has_exact_material_result_locality(
            ledger, source_material_result_occurrence_identity
        )
    ):
        raise ValueError(
            "byte-pair position-coordinate binding requires one exact "
            "through-occurrence boundary"
        )
    return through_event_occurrence_identity


def _record_byte_pair_occurrence_position_measurement_subject_to_act_binding(
    ledger: EventLedger,
    *,
    source_material_result_occurrence_identity: str,
    current_coordinates: dict[str, Any],
) -> Event:
    finding = measure_position_coordinates_of_byte_pair_occurrences(
        ledger,
        source_material_result_occurrence_identity=source_material_result_occurrence_identity,
    )
    return _record_byte_pair_occurrence_position_measurement_subject_to_act_binding_from_finding(
        ledger,
        finding=finding,
        current_coordinates=current_coordinates,
    )


def _record_byte_pair_occurrence_position_measurement_subject_to_act_binding_from_finding(
    ledger: EventLedger,
    *,
    finding: FindingOfPositionCoordinatesOfBytePairOccurrences,
    current_coordinates: dict[str, Any],
) -> Event:
    _validate_finding(finding)
    through_event_occurrence_identity = _require_current_coordinates(
        ledger,
        locality_identity=finding.source_locality_identity,
        current_coordinates=current_coordinates,
        source_material_result_occurrence_identity=(
            finding.source_material_result_occurrence_identity
        ),
    )
    # This refusal prevents malformed or already-recorded sources from entering
    # the recorder. The occurrence identity alone establishes neither the exact
    # Locality relation nor the required binding subject and coordinates.
    current_sources = (
        _unbound_position_coordinate_measurement_material_results_from_bounded_locality_replay(
            ledger,
            current_coordinates,
            locality_identity=finding.source_locality_identity,
        )
    )
    if finding.source_material_result_occurrence_identity not in {
        source.source_material_result_occurrence_identity for source in current_sources
    }:
        raise ValueError(
            "byte-pair position-coordinate binding requires one exact current unbound material result"
        )
    global_recording_boundary = ledger.append_boundary()
    identities = {
        "exact_act_identity": ledger.mint_identity(
            "byte_pair_occurrence_position_measurement_act"
        ),
        "act_occurrence_identity": ledger.mint_identity(
            "byte_pair_occurrence_position_measurement_act_occurrence"
        ),
        "measurement_result_identity": ledger.mint_identity(
            "byte_pair_occurrence_position_measurement_result"
        ),
    }
    if len(set(identities.values())) != len(identities):
        raise ValueError("byte-pair position-coordinate Measurement identities collapsed")
    if ledger.append_boundary() != global_recording_boundary:
        raise ValueError(
            "byte-pair position-coordinate global recording boundary changed before binding"
        )
    return ledger.append(
        BYTE_PAIR_OCCURRENCE_POSITION_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
        _binding_material(
            finding,
            through_event_occurrence_identity=through_event_occurrence_identity,
            **identities,
        ),
        locality_identity=finding.source_locality_identity,
    )


def _record_byte_pair_occurrence_position_measurement_subject_to_act_binding_from_carried_finding(
    ledger: EventLedger,
    *,
    finding: FindingOfPositionCoordinatesOfBytePairOccurrences,
    current_coordinates: dict[str, Any],
) -> Event:
    """Bind one finding carried by the exact current coordinates."""

    return _record_byte_pair_occurrence_position_measurement_subject_to_act_binding_from_finding(
        ledger,
        finding=finding,
        current_coordinates=current_coordinates,
    )


def _record_byte_pair_occurrence_position_measurement_subject_to_act_binding_from_through_event_occurrence(
    ledger: EventLedger,
    *,
    finding: FindingOfPositionCoordinatesOfBytePairOccurrences,
    through_event_occurrence_identity: str,
) -> Event:
    """Record one binding through an exact earlier occurrence."""

    global_recording_boundary = ledger.append_boundary()
    _validate_finding(finding)
    through_event_occurrence_identity = _require_exact_through_event_occurrence(
        ledger,
        locality_identity=finding.source_locality_identity,
        through_event_occurrence_identity=through_event_occurrence_identity,
        source_material_result_occurrence_identity=(
            finding.source_material_result_occurrence_identity
        ),
    )
    if any(
        event.material.get("source_material_result_occurrence_identity")
        == finding.source_material_result_occurrence_identity
        for event in (
            *ledger.iter_locality_kind(
                finding.source_locality_identity,
                BYTE_PAIR_OCCURRENCE_POSITION_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
            ),
            *ledger.iter_locality_kind(
                finding.source_locality_identity,
                BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND,
            ),
        )
    ):
        raise ValueError(
            "byte-pair position-coordinate binding requires one exact "
            "unbound subject through the supplied occurrence"
        )
    identities = {
        "exact_act_identity": ledger.mint_identity(
            "byte_pair_occurrence_position_measurement_act"
        ),
        "act_occurrence_identity": ledger.mint_identity(
            "byte_pair_occurrence_position_measurement_act_occurrence"
        ),
        "measurement_result_identity": ledger.mint_identity(
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
            "before binding"
        )
    return ledger.append(
        BYTE_PAIR_OCCURRENCE_POSITION_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
        _binding_material(
            finding,
            through_event_occurrence_identity=through_event_occurrence_identity,
            **identities,
        ),
        locality_identity=finding.source_locality_identity,
    )


def record_byte_pair_occurrence_position_measurement_subject_to_act_binding(
    ledger: EventLedger,
    *,
    source_material_result_occurrence_identity: str,
    current_coordinates: dict[str, Any],
) -> Event:
    """Bind the exact source result to this declared Measurement."""

    return _record_byte_pair_occurrence_position_measurement_subject_to_act_binding(
        ledger,
        source_material_result_occurrence_identity=source_material_result_occurrence_identity,
        current_coordinates=current_coordinates,
    )


def _read_binding(
    ledger: EventLedger,
    binding_event_identity: str,
    *,
    prior_coordinates: dict[str, Any] | None = None,
) -> tuple[Event, FindingOfPositionCoordinatesOfBytePairOccurrences]:
    binding = ledger.get(binding_event_identity)
    if (
        binding is None
        or binding.kind != BYTE_PAIR_OCCURRENCE_POSITION_SUBJECT_TO_ACT_BINDING_RECORDED_KIND
        or type(binding.locality_identity) is not str
        or not binding.locality_identity
        or binding.exact_material is not None
        or ledger.integrity_of(binding.identity) == CORRUPTED
    ):
        raise ValueError("byte-pair position-coordinate binding is absent or corrupted")
    material = binding.material
    identities = {
        key: material.get(key)
        for key in (
            "exact_act_identity",
            "act_occurrence_identity",
            "measurement_result_identity",
        )
    }
    source_identity = material.get("source_material_result_occurrence_identity")
    boundary_identity = material.get("completeness_boundary_identity")
    through_event_occurrence_identity = material.get(
        "through_event_occurrence_identity"
    )
    if (
        any(type(value) is not str or not value for value in identities.values())
        or len(set(identities.values())) != len(identities)
        or any(
            type(value) is not str or not value
            for value in (
                source_identity,
                boundary_identity,
                through_event_occurrence_identity,
            )
        )
    ):
        raise ValueError("byte-pair position-coordinate binding coordinates are not exact")
    try:
        finding = _measure_through(
            ledger,
            source_material_result_occurrence_identity=source_identity,
            boundary=EventLedgerBoundary(boundary_identity),
        )
    except (TypeError, ValueError) as error:
        raise ValueError(
            "byte-pair position-coordinate binding coordinates are not exact"
        ) from error
    if (
        binding.locality_identity != finding.source_locality_identity
        or material
        != _binding_material(
            finding,
            through_event_occurrence_identity=through_event_occurrence_identity,
            **identities,
        )
    ):
        raise ValueError("byte-pair position-coordinate binding coordinates are not exact")
    try:
        if prior_coordinates is None:
            from seed_runtime.operator_current_coordinates import (
                read_operator_current_coordinates_through,
            )

            prior_coordinates = read_operator_current_coordinates_through(
                ledger,
                locality_identity=finding.source_locality_identity,
                through_event_occurrence_identity=through_event_occurrence_identity,
            )
        ledger.occurrences_in_append_order(
            (through_event_occurrence_identity, binding.identity),
            locality_identity=finding.source_locality_identity,
        )
    except (TypeError, ValueError) as error:
        raise ValueError(
            "byte-pair position-coordinate binding has no exact prior coordinates"
        ) from error
    if not any(
        type(occurrence) is dict
        and occurrence.get("result_occurrence_identity") == source_identity
        for occurrence in prior_coordinates.get("material_result_occurrences", ())
    ):
        raise ValueError(
            "byte-pair position-coordinate binding has no exact prior coordinates"
        )
    return binding, finding


def _require_carried_byte_pair_occurrence_position_subject_to_act_binding(
    ledger: EventLedger,
    *,
    binding: Event,
    finding: FindingOfPositionCoordinatesOfBytePairOccurrences,
) -> None:
    if (
        type(binding) is not Event
        or type(finding) is not FindingOfPositionCoordinatesOfBytePairOccurrences
        or binding.kind
        != BYTE_PAIR_OCCURRENCE_POSITION_SUBJECT_TO_ACT_BINDING_RECORDED_KIND
        or binding.exact_material is not None
        or binding.locality_identity
        != finding.source_locality_identity
        or ledger.integrity_of(binding.identity) == CORRUPTED
    ):
        raise ValueError(
            "byte-pair position-coordinate Measurement requires its exact carried binding"
        )
    material = binding.material
    identity_coordinates = {
        coordinate: material.get(coordinate)
        for coordinate in (
            "exact_act_identity",
            "act_occurrence_identity",
            "measurement_result_identity",
        )
    }
    through_event_occurrence_identity = material.get(
        "through_event_occurrence_identity"
    )
    if (
        any(
            type(identity) is not str or not identity
            for identity in identity_coordinates.values()
        )
        or len(set(identity_coordinates.values())) != len(identity_coordinates)
        or material
        != _binding_material(
            finding,
            through_event_occurrence_identity=through_event_occurrence_identity,
            **identity_coordinates,
        )
    ):
        raise ValueError(
            "byte-pair position-coordinate Measurement requires its exact carried binding"
        )


def get_byte_pair_occurrence_position_measurement_subject_to_act_binding(
    ledger: EventLedger,
    binding_event_identity: str,
    *,
    prior_coordinates: dict[str, Any] | None = None,
) -> Event:
    binding, _finding = _read_binding(
        ledger,
        binding_event_identity,
        prior_coordinates=prior_coordinates,
    )
    return binding


def _act_material(
    finding: FindingOfPositionCoordinatesOfBytePairOccurrences,
    binding: Event,
) -> dict[str, Any]:
    return {
        "addressed_act_identity": binding.material["exact_act_identity"],
        "act_occurrence_identity": binding.material["act_occurrence_identity"],
        "act": EXACT_ACT,
        "subject_to_act_binding_reference": _binding_reference(binding),
    }


def _record_byte_pair_occurrence_position_measurement_act_occurrence(
    ledger: EventLedger,
    *,
    binding_event_identity: str,
    binding_current_coordinates: dict[str, Any],
) -> Event:
    binding, finding = _read_binding(
        ledger, binding_event_identity
    )
    _require_current_coordinates(
        ledger,
        locality_identity=binding.locality_identity,
        current_coordinates=binding_current_coordinates,
        binding_occurrence_identity=binding.identity,
    )
    for prior in ledger.iter_locality_kind(
        binding.locality_identity, BYTE_PAIR_OCCURRENCE_POSITION_ACT_OCCURRENCE_EVENT
    ):
        if (
            prior.material.get("subject_to_act_binding_reference")
            == _binding_reference(binding)
            or prior.material.get("act_occurrence_identity")
            == binding.material["act_occurrence_identity"]
        ):
            raise ValueError("byte-pair position-coordinate binding already carries an Act")
    return ledger.append(
        BYTE_PAIR_OCCURRENCE_POSITION_ACT_OCCURRENCE_EVENT,
        _act_material(finding, binding),
        locality_identity=binding.locality_identity,
    )


def record_byte_pair_occurrence_position_measurement_act_occurrence(
    ledger: EventLedger,
    *,
    binding_event_identity: str,
    binding_current_coordinates: dict[str, Any],
) -> Event:
    return _record_byte_pair_occurrence_position_measurement_act_occurrence(
        ledger,
        binding_event_identity=(
            binding_event_identity
        ),
        binding_current_coordinates=binding_current_coordinates,
    )


def _record_byte_pair_occurrence_position_measurement_act_occurrence_from_carried_binding(
    ledger: EventLedger,
    *,
    binding: Event,
    finding: FindingOfPositionCoordinatesOfBytePairOccurrences,
    binding_current_coordinates: dict[str, Any],
) -> Event:
    """Record the Act beside its just-carried exact binding and finding."""

    _require_carried_byte_pair_occurrence_position_subject_to_act_binding(
        ledger,
        binding=binding,
        finding=finding,
    )
    _require_current_coordinates(
        ledger,
        locality_identity=binding.locality_identity,
        current_coordinates=binding_current_coordinates,
        binding_occurrence_identity=binding.identity,
    )
    for prior in ledger.iter_locality_kind(
        binding.locality_identity,
        BYTE_PAIR_OCCURRENCE_POSITION_ACT_OCCURRENCE_EVENT,
    ):
        if (
            prior.material.get("subject_to_act_binding_reference")
            == _binding_reference(binding)
            or prior.material.get("act_occurrence_identity")
            == binding.material["act_occurrence_identity"]
        ):
            raise ValueError("byte-pair position-coordinate binding already carries an Act")
    return ledger.append(
        BYTE_PAIR_OCCURRENCE_POSITION_ACT_OCCURRENCE_EVENT,
        _act_material(finding, binding),
        locality_identity=binding.locality_identity,
    )


def _read_act(
    ledger: EventLedger,
    act_occurrence_event_identity: str,
    *,
    prior_coordinates: dict[str, Any] | None = None,
) -> tuple[
    Event,
    Event,
    FindingOfPositionCoordinatesOfBytePairOccurrences,
]:
    act = ledger.get(act_occurrence_event_identity)
    if (
        act is None
        or act.kind != BYTE_PAIR_OCCURRENCE_POSITION_ACT_OCCURRENCE_EVENT
        or act.exact_material is not None
        or ledger.integrity_of(act.identity) == CORRUPTED
    ):
        raise ValueError("byte-pair position-coordinate result requires intact Act occurrence")
    reference = act.material.get("subject_to_act_binding_reference")
    try:
        binding, finding = _read_binding(
            ledger,
            reference.get("recorded_occurrence_identity")
            if type(reference) is dict
            else "",
            prior_coordinates=prior_coordinates,
        )
    except (TypeError, ValueError) as error:
        raise ValueError(
            "byte-pair position-coordinate result requires intact Act occurrence"
        ) from error
    if (
        act.locality_identity != binding.locality_identity
        or reference != _binding_reference(binding)
        or act.material != _act_material(finding, binding)
    ):
        raise ValueError("byte-pair position-coordinate result requires intact Act occurrence")
    try:
        ledger.occurrences_in_append_order(
            (binding.identity, act.identity),
            locality_identity=binding.locality_identity,
        )
    except ValueError as error:
        raise ValueError(
            "byte-pair position-coordinate Act requires its prior binding"
        ) from error
    return act, binding, finding


def get_byte_pair_occurrence_position_measurement_act_occurrence(
    ledger: EventLedger, act_occurrence_event_identity: str
) -> Event:
    act, _binding, _finding = _read_act(ledger, act_occurrence_event_identity)
    return act


def _source_position_coordinate_reference(
    *,
    source_material_result_occurrence_identity: str,
    source_locality_identity: str,
    completeness_boundary_identity: str,
    position: int,
    exact_material: bytes,
) -> dict[str, Any]:
    return {
        "source_material_result_occurrence_identity": source_material_result_occurrence_identity,
        "locality_identity": source_locality_identity,
        "completeness_boundary_identity": completeness_boundary_identity,
        "position": position,
        "exact_material": list(exact_material),
    }


def _assertion_coordinates(
    finding: FindingOfPositionCoordinatesOfBytePairOccurrences,
    *,
    exact_pair: bytes,
    first_position: int,
    second_position: int,
) -> tuple[dict[str, Any], dict[str, Any]]:
    subject = {
        "source_material_result_occurrence_identity": (
            finding.source_material_result_occurrence_identity
        ),
        "exact_pair": list(exact_pair),
    }
    content = {
        "first_position": first_position,
        "second_position": second_position,
        "first_position_coordinate_reference": (
            _source_position_coordinate_reference(
                source_material_result_occurrence_identity=(
                    finding.source_material_result_occurrence_identity
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
                source_material_result_occurrence_identity=(
                    finding.source_material_result_occurrence_identity
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
    return subject, content


def _assertion(
    finding: FindingOfPositionCoordinatesOfBytePairOccurrences,
    *,
    exact_pair: bytes,
    first_position: int,
    second_position: int,
) -> dict[str, Any]:
    subject, content = _assertion_coordinates(
        finding,
        exact_pair=exact_pair,
        first_position=first_position,
        second_position=second_position,
    )
    return {
        "dimensions": {
            "position": first_position,
            "content": content,
        },
        "result": "position",
        "assertion_subject": subject,
    }


def _assertion_result_coordinates(
    finding: FindingOfPositionCoordinatesOfBytePairOccurrences,
) -> dict[str, Any]:
    return {
        "result": "position",
        "source_material_result_occurrence_identity": (
            finding.source_material_result_occurrence_identity
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
        },
    }


def _result_material(
    finding: FindingOfPositionCoordinatesOfBytePairOccurrences,
    binding: Event,
) -> dict[str, Any]:
    return {
        "result_identity": binding.material["measurement_result_identity"],
        "addressed_act_identity": binding.material["exact_act_identity"],
        "act_occurrence_identity": binding.material["act_occurrence_identity"],
        "exact_act": EXACT_ACT,
        "subject_to_act_binding_reference": _binding_reference(binding),
        "source_localities": [finding.source_locality_identity],
        "source_material_result_occurrence_identity": (
            finding.source_material_result_occurrence_identity
        ),
        "completeness_boundary": {
            "identity": finding.completeness_boundary.identity
        },
        "assertions": _assertion_result_coordinates(finding),
    }


def _refuse_existing_byte_pair_occurrence_position_measurement_result(
    ledger: EventLedger,
    *,
    act: Event,
    act_occurrence_identity: str,
) -> None:
    for prior_yield in ledger.iter_locality_kind(
        act.locality_identity, RECORDED_YIELD_RELATION_EVENT
    ):
        dimensions = prior_yield.material.get("dimensions")
        if (
            prior_yield.material.get("act_occurrence_event_identity")
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
            prior_result.material.get("act_occurrence_event_identity")
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
    binding: Event,
    finding: FindingOfPositionCoordinatesOfBytePairOccurrences,
) -> Event:
    result = _result_material(finding, binding)
    yield_relation = _record_yield_relation(
        ledger,
        locality_identity=act.locality_identity,
        exact_act=EXACT_ACT,
        act_occurrence_identity=binding.material["act_occurrence_identity"],
        act_occurrence_event_identity=act.identity,
        result_kind=RESULT_KIND,
        result_identity=result["result_identity"],
        result_content=result,
        occurrence_boundary="byte_pair_occurrence_position_measurement",
    )
    return ledger.append(
        BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND,
        {
            "result_identity": result["result_identity"],
            "addressed_act_identity": result["addressed_act_identity"],
            "act_occurrence_identity": result["act_occurrence_identity"],
            "exact_act": result["exact_act"],
            "subject_to_act_binding_reference": result[
                "subject_to_act_binding_reference"
            ],
            "source_localities": result["source_localities"],
            "source_material_result_occurrence_identity": result[
                "source_material_result_occurrence_identity"
            ],
            "completeness_boundary": result["completeness_boundary"],
            "assertions": result["assertions"],
            "act_occurrence_event_identity": act.identity,
            "yield_relation_identity": yield_relation.identity,
        },
        locality_identity=act.locality_identity,
    )


def record_byte_pair_occurrence_position_measurement_result(
    ledger: EventLedger,
    *,
    act_occurrence_event_identity: str,
) -> Event:
    act, binding, finding = _read_act(
        ledger, act_occurrence_event_identity
    )
    _refuse_existing_byte_pair_occurrence_position_measurement_result(
        ledger,
        act=act,
        act_occurrence_identity=binding.material["act_occurrence_identity"],
    )
    return _record_byte_pair_occurrence_position_measurement_result(
        ledger,
        act=act,
        binding=binding,
        finding=finding,
    )


def _record_byte_pair_occurrence_position_measurement_result_from_carried_act_occurrence(
    ledger: EventLedger,
    *,
    act_occurrence: Event,
    binding: Event,
    finding: FindingOfPositionCoordinatesOfBytePairOccurrences,
) -> Event:
    """Record the result beside its just-produced exact Act occurrence."""

    _require_carried_byte_pair_occurrence_position_subject_to_act_binding(
        ledger,
        binding=binding,
        finding=finding,
    )
    if (
        type(act_occurrence) is not Event
        or act_occurrence.kind
        != BYTE_PAIR_OCCURRENCE_POSITION_ACT_OCCURRENCE_EVENT
        or act_occurrence.exact_material is not None
        or act_occurrence.locality_identity
        != binding.locality_identity
        or ledger.integrity_of(act_occurrence.identity) == CORRUPTED
        or act_occurrence.material
        != _act_material(finding, binding)
        or ledger.append_boundary_through_occurrence(
            act_occurrence.identity
        )
        != ledger.append_boundary()
    ):
        raise ValueError(
            "byte-pair position-coordinate result requires intact Act occurrence"
        )
    return _record_byte_pair_occurrence_position_measurement_result(
        ledger,
        act=act_occurrence,
        binding=binding,
        finding=finding,
    )


def _read_result(
    ledger: EventLedger,
    result_event_identity: str,
    *,
    prior_coordinates: dict[str, Any] | None = None,
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
        act, binding, finding = _read_act(
            ledger,
            event.material.get("act_occurrence_event_identity"),
            prior_coordinates=prior_coordinates,
        )
    except (TypeError, ValueError) as error:
        raise ValueError("byte-pair position-coordinate result carries no exact Act") from error
    expected = {
        **_result_material(finding, binding),
        "act_occurrence_event_identity": act.identity,
        "yield_relation_identity": event.material.get(
            "yield_relation_identity"
        ),
    }
    if event.locality_identity != act.locality_identity or event.material != expected:
        raise ValueError("byte-pair position-coordinate result coordinates are not exact")
    yield_relation_identity = event.material.get("yield_relation_identity")
    try:
        requirements = read_requirements_of_yield_relation(
            ledger,
            recorded_result_event_identity=event.identity,
            yield_relation_event_identity=yield_relation_identity,
            act_occurrence_event_identity=act.identity,
        )
        yield_relation = ledger.get(yield_relation_identity)
    except (TypeError, ValueError) as error:
        raise ValueError("byte-pair position-coordinate result carries no exact Yield") from error
    if (
        not all(requirements.values())
        or yield_relation is None
        or yield_relation.kind != RECORDED_YIELD_RELATION_EVENT
        or ledger.integrity_of(yield_relation.identity) == CORRUPTED
        or yield_relation.material.get("occurrence_boundary")
        != "byte_pair_occurrence_position_measurement"
        or yield_relation.material.get("result_kind") != RESULT_KIND
    ):
        raise ValueError("byte-pair position-coordinate result carries no exact Yield")
    try:
        ordered = ledger.occurrences_in_append_order(
            (act.identity, yield_relation.identity, event.identity),
            locality_identity=event.locality_identity,
        )
    except ValueError as error:
        raise ValueError("byte-pair position-coordinate result has false occurrence order") from error
    if tuple(item.identity for item in ordered) != (
        act.identity,
        yield_relation.identity,
        event.identity,
    ):
        raise ValueError("byte-pair position-coordinate result has false occurrence order")
    return event, finding, expected["assertions"]


def get_recorded_byte_pair_occurrence_position_measurement(
    ledger: EventLedger,
    result_event_identity: str,
    *,
    prior_coordinates: dict[str, Any] | None = None,
) -> FindingOfPositionCoordinatesOfBytePairOccurrences:
    _event, finding, _assertions_read = _read_result(
        ledger,
        result_event_identity,
        prior_coordinates=prior_coordinates,
    )
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
        assertion_position=first_position,
        source_material_result_occurrence_identity=(
            finding.source_material_result_occurrence_identity
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
    assertion_position: int,
    exact_pair: bytes,
    first_position: int,
    second_position: int,
) -> ReferenceToRecordedPositionOfBytePairOccurrence:
    if (
        type(assertion_position) is not int
        or assertion_position < 0
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
        or assertion_position != first_position
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
        "source_material_result_occurrence_identity",
        "locality_identity",
        "completeness_boundary_identity",
        "position",
        "exact_material",
    }
    if (
        type(position_coordinate_reference) is not dict
        or set(position_coordinate_reference) != coordinate_keys
        or type(position_coordinate_reference.get("source_material_result_occurrence_identity"))
        is not str
        or not position_coordinate_reference["source_material_result_occurrence_identity"]
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
            "addressed source position is outside the exact material result"
        )
    expected = _source_position_coordinate_reference(
        source_material_result_occurrence_identity=(
            finding.source_material_result_occurrence_identity
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
    *,
    prior_coordinates: dict[str, Any] | None = None,
) -> tuple[ReferenceToRecordedPositionOfBytePairOccurrence, ...]:
    """Read pair Assertions carrying one exact addressed source coordinate."""

    if not isinstance(ledger, EventLedger):
        raise TypeError("addressed source position requires one EventLedger")
    if type(result_event_identity) is not str or not result_event_identity:
        raise ValueError("addressed source position requires one result occurrence")
    event, finding, _assertion_result_coordinates_read = _read_result(
        ledger,
        result_event_identity,
        prior_coordinates=prior_coordinates,
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
    assertion_positions: tuple[int, ...],
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
        type(assertion_positions) is not tuple
        or not assertion_positions
        or any(type(position) is not int or position < 0 for position in assertion_positions)
        or len(set(assertion_positions)) != len(assertion_positions)
    ):
        raise ValueError("position references require distinct Assertion positions")
    if (
        exact_coordinates is not None
        and (
            type(exact_coordinates) is not tuple
            or len(exact_coordinates) != len(assertion_positions)
            or any(
                type(coordinates) is not tuple or len(coordinates) != 3
                for coordinates in exact_coordinates
            )
        )
    ):
        raise ValueError("position references require exact addressed coordinates")
    event, finding, _assertion_result_coordinates_read = _read_result(
        ledger, result_event_identity
    )
    if exact_coordinates is not None:
        return tuple(
            _reference_at_exact_coordinates(
                event,
                finding,
                assertion_position=assertion_position,
                exact_pair=coordinates[0],
                first_position=coordinates[1],
                second_position=coordinates[2],
            )
            for assertion_position, coordinates in zip(
                assertion_positions, exact_coordinates, strict=True
            )
        )
    references = []
    for first_position in assertion_positions:
        second_position = first_position + 1
        if second_position >= len(finding.exact_material):
            raise ValueError("position result carries no addressed Assertion")
        exact_pair = finding.exact_material[first_position : second_position + 1]
        references.append(
            _recorded_position_reference(
                event,
                finding,
                exact_pair=exact_pair,
                first_position=first_position,
                second_position=second_position,
            )
        )
    return tuple(references)


def references_to_recorded_position_coordinates_of_byte_pair_occurrences(
    ledger: EventLedger, result_event_identity: str
) -> tuple[
    ReferenceToRecordedPositionOfBytePairOccurrence, ...
]:
    event, finding, _assertion_result_coordinates_read = _read_result(
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
    ledger: EventLedger,
    result_event_identity: str,
    *,
    prior_coordinates: dict[str, Any] | None = None,
) -> Iterator[dict[str, Any]]:
    """Yield the exact bounded source-position subjects from one result read."""

    _event, finding, _assertion_result_coordinates_read = _read_result(
        ledger,
        result_event_identity,
        prior_coordinates=prior_coordinates,
    )
    for position, value in enumerate(finding.exact_material):
        yield _source_position_coordinate_reference(
            source_material_result_occurrence_identity=(
                finding.source_material_result_occurrence_identity
            ),
            source_locality_identity=finding.source_locality_identity,
            completeness_boundary_identity=finding.completeness_boundary.identity,
            position=position,
            exact_material=bytes((value,)),
        )


def _recorded_position_assertion_at_position_for_locality_movement(
    ledger: EventLedger,
    *,
    result_event_identity: str,
    assertion_position: int,
) -> dict[str, Any]:
    event, finding, _assertion_result_coordinates_read = _read_result(
        ledger, result_event_identity
    )
    if (
        type(assertion_position) is not int
        or assertion_position < 0
        or assertion_position + 1 >= len(finding.exact_material)
    ):
        raise ValueError(
            "position Assertion Locality movement requires exact source coordinates"
        )
    return _assertion(
        finding,
        exact_pair=finding.exact_material[assertion_position : assertion_position + 2],
        first_position=assertion_position,
        second_position=assertion_position + 1,
    )


def _recorded_position_assertions_for_locality_movement(
    ledger: EventLedger,
    *,
    result_event_identity: str,
) -> Iterator[dict[str, Any]]:
    """Yield every position Assertion after one exact bounded result read.

    The Assertions are reconstructed from the validated finding. Reading them
    records no movement and establishes no later relation.
    """

    _event, finding, _assertion_result_coordinates_read = _read_result(
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
