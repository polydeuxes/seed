"""Measure exact bytes across complete bounded material result occurrences.

This is the first source boundary that does not receive its measured
subjects from a caller.  The subjects are the literal byte values carried by
the exact material linked from every material result occurrence in the declared
Localities through one recorded ledger boundary.

One byte value receives one count result position.  Recurrence is a separate
result position and exists only where the total count exceeds one.  The same byte
material establishes no character, word, position pair, grammar, or represented
relation.
"""

from __future__ import annotations


from collections import Counter
from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Iterable

from seed_runtime.events import CORRUPTED, EventLedger, EventLedgerBoundary
from seed_runtime.event import Event
from seed_runtime.yield_relation import (
    RECORDED_YIELD_RELATION_EVENT,
    _record_yield_relation,
    read_requirements_of_yield_relation,
)
from seed_runtime.material_source import (
    MaterialSourceError,
    exact_material_result_bytes,
    iter_exact_material_results,
)

BYTE_MEASUREMENT_RECORDED_KIND = "operator.measurement.byte_counts_recorded"
BYTE_MEASUREMENT_RESULT_KIND = "exact byte-count Measurement results"
BYTE_PAIR_MEASUREMENT_RECORDED_KIND = (
    "operator.measurement.byte_position_pair_counts_recorded"
)
BYTE_PAIR_APPLICABILITY_SUBJECT_TO_ACT_BINDING_RECORDED_KIND = (
    "operator.measurement.byte_position_pair_applicability_subject_to_act_binding_recorded"
)
BYTE_PAIR_MEASUREMENT_SUBJECT_TO_ACT_BINDING_RECORDED_KIND = (
    "operator.measurement.byte_position_pair_measurement_subject_to_act_binding_recorded"
)
BYTE_OCCURRENCE_PRESERVATION = "exact byte Measurement result"
BYTE_PAIR_OCCURRENCE_PRESERVATION = "exact byte-position-pair Measurement result"
BYTE_RESULT_COORDINATES = frozenset(
    {
        "result_identity",
        "dimensions",
        "exact_act",
        "addressed_act_identity",
        "act_occurrence_identity",
        "subject_to_act_binding_reference",
        "source_localities",
        "completeness_boundary",
        "result_positions",
    }
)
BYTE_MEASUREMENT_ACT_OCCURRENCE_EVENT = (
    "operator.measurement.byte_act_occurrenced"
)
BYTE_MEASUREMENT_SUBJECT_TO_ACT_BINDING_RECORDED_KIND = (
    "operator.measurement.byte_subject_to_act_binding_recorded"
)
BYTE_PAIR_RESULT_COORDINATES = BYTE_RESULT_COORDINATES - {
    "subject_to_act_binding_reference",
} | {
    "addressed_act_identity",
    "act_occurrence_identity",
    "source_result_position_reference",
    "source_movement_event_identity",
    "input_applicability",
    "input_applicability_event_identity",
    "subject_to_act_binding_reference",
}
BYTE_PAIR_RESULT_COORDINATES_WITHOUT_APPLICABILITY = BYTE_RESULT_COORDINATES - {
    "subject_to_act_binding_reference",
} | {
    "addressed_act_identity",
    "act_occurrence_identity",
    "source_result_position_reference",
    "source_movement_event_identity",
}
BYTE_PAIR_MEASUREMENT_ACT_OCCURRENCE_EVENT = (
    "operator.measurement.byte_position_pair_act_occurrenced"
)
BYTE_PAIR_APPLICABILITY_RECORDED_KIND = (
    "operator.measurement.byte_position_pair_input_applicability_recorded"
)
BYTE_PAIR_APPLICABILITY_RESULT_KIND = "byte-position-pair input Applicability result"
BYTE_PAIR_APPLICABILITY_RESULT_COORDINATES = frozenset(
    {
        "result_identity",
        "dimensions",
        "exact_act",
        "subject_to_act_binding_reference",
        "applicability_act_identity",
        "applicability_act_occurrence_identity",
        "addressed_act_identity",
        "input_result_position_reference",
        "input_movement_event_identity",
        "applicability",
    }
)
BYTE_PAIR_APPLICABILITY_ACT_OCCURRENCE_EVENT = (
    "operator.measurement.byte_position_pair_applicability_act_occurrence_recorded"
)
RESULT_POSITION_LOCALITY_MOVEMENT_KIND = "operator.result_position.locality_movement_recorded"
RESULT_POSITION_LOCALITY_MOVEMENT_SUBJECT_TO_ACT_BINDING_KIND = (
    "operator.result_position.locality_movement_subject_to_act_binding_recorded"
)
RESULT_POSITION_LOCALITY_MOVEMENT_ACT_OCCURRENCE_EVENT = (
    "operator.result_position.locality_movement_act_occurrence_recorded"
)
RESULT_POSITION_LOCALITY_MOVEMENT_RESULT_KIND = "result-position Locality movement result"
EVENT_KIND_BOOK_CLAUSES = {
    BYTE_MEASUREMENT_SUBJECT_TO_ACT_BINDING_RECORDED_KIND: "01.Source.D",
    BYTE_MEASUREMENT_RECORDED_KIND: "01.Source.D",
    BYTE_PAIR_MEASUREMENT_RECORDED_KIND: "01.Source.D",
    BYTE_PAIR_APPLICABILITY_SUBJECT_TO_ACT_BINDING_RECORDED_KIND: "01.Current.E.1",
    BYTE_PAIR_MEASUREMENT_SUBJECT_TO_ACT_BINDING_RECORDED_KIND: "01.Source.D",
    BYTE_MEASUREMENT_ACT_OCCURRENCE_EVENT: "02.Acts.A",
    BYTE_PAIR_MEASUREMENT_ACT_OCCURRENCE_EVENT: "02.Acts.A",
    BYTE_PAIR_APPLICABILITY_RECORDED_KIND: "01.Current.E.1",
    BYTE_PAIR_APPLICABILITY_ACT_OCCURRENCE_EVENT: "02.Acts.A",
    RESULT_POSITION_LOCALITY_MOVEMENT_SUBJECT_TO_ACT_BINDING_KIND: "03.Movement.A",
    RESULT_POSITION_LOCALITY_MOVEMENT_ACT_OCCURRENCE_EVENT: "02.Acts.A",
    RESULT_POSITION_LOCALITY_MOVEMENT_KIND: "03.Movement.A",
}
BYTE_PAIR_RESULT_BOUNDARY = (
    "establish exact count of byte-pair occurrences in source order within the exact "
    "bounded source material"
)
class ByteMeasurementError(ValueError):
    """The exact byte Measurement could not be performed as declared."""


def _require_exact_result_yield(
    ledger: EventLedger,
    event: Any,
    yield_relation: Any,
    act_occurrence: Any,
    *,
    result_name: str,
    occurrence_coordinate: str = "act_occurrence_identity",
) -> None:
    requirements = read_requirements_of_yield_relation(
        ledger,
        recorded_result_event_identity=event.identity,
        yield_relation_event_identity=yield_relation.identity,
        act_occurrence_event_identity=act_occurrence.identity,
        recorded_result_occurrence_coordinate=occurrence_coordinate,
        yielding_act_occurrence_coordinate=occurrence_coordinate,
    )
    if not all(requirements.values()):
        raise ByteMeasurementError(
            f"{event.identity} names no exact {result_name} Yield relation"
        )


def _yield_immediately_precedes_result(
    ledger: EventLedger, yield_relation: Event, result: Event
) -> bool:
    try:
        prefix = ledger.list(
            through=ledger.append_boundary_through_occurrence(result.identity)
        )
    except (TypeError, ValueError):
        return False
    return len(prefix) >= 2 and prefix[-2] == yield_relation and prefix[-1] == result


@dataclass(frozen=True)
class MeasuredByteCount:
    content: int
    occurrences_carrying: int
    count: int


@dataclass(frozen=True)
class MeasuredByteInputs:
    source_localities: tuple[str, ...]
    completeness_boundary: EventLedgerBoundary
    source_material: tuple[dict[str, str], ...]
    counts: tuple[MeasuredByteCount, ...]


@dataclass(frozen=True)
class MeasuredBytePairCount:
    content: tuple[int, int]
    occurrences_carrying: int
    count: int


@dataclass(frozen=True)
class MeasuredBytePairInputs:
    source_localities: tuple[str, ...]
    completeness_boundary: EventLedgerBoundary
    source_material: tuple[dict[str, str], ...]
    source_result_position_reference: dict[str, str]
    source_movement_event_identity: str | None
    input_applicability: dict[str, Any]
    addressed_act_identity: str
    act_occurrence_identity: str
    counts: tuple[MeasuredBytePairCount, ...]


def _byte_result_position_reference(source: dict[str, Any]) -> dict[str, Any]:
    return {
        "recorded_occurrence_identity": source["recorded_occurrence_identity"],
        "result_position": source["result_position"],
    }


def _byte_result_position_movement_identity(source: dict[str, Any]) -> str | None:
    return source.get("locality_movement_event_identity")


@dataclass(frozen=True)
class RecordedBytePairResultPosition:
    result_position: int
    recorded_occurrence_identity: str
    content: tuple[int, int] | None
    result: str
    _material: dict[str, Any]
    _referenced_result_position_references: tuple[dict[str, Any], ...]

    @property
    def material(self) -> dict[str, Any]:
        return deepcopy(self._material)

    @property
    def referenced_result_position_references(self) -> tuple[dict[str, Any], ...]:
        return deepcopy(self._referenced_result_position_references)

    @property
    def reference(self) -> dict[str, Any]:
        return {
            "recorded_occurrence_identity": self.recorded_occurrence_identity,
            "result_position": self.result_position,
        }


@dataclass(frozen=True)
class _RecordedBytePairFinding:
    result_position: int
    recorded_occurrence_identity: str
    exact_pair: tuple[int, int]
    result: str
    _content_coordinates: tuple[int, int, int] | bool
    _referenced_result_positions: tuple[int, ...]

    @property
    def content(self) -> dict[str, int | bool]:
        if self.result == "recurrence":
            return {"recurrence_established": self._content_coordinates}
        input_count, occurrences_carrying, count = self._content_coordinates
        return {
            "input_count": input_count,
            "occurrences_carrying": occurrences_carrying,
            "count": count,
        }

    @property
    def reference(self) -> dict[str, Any]:
        return {
            "recorded_occurrence_identity": self.recorded_occurrence_identity,
            "result_position": self.result_position,
        }


@dataclass(frozen=True)
class _RecordedBytePairMeasurementReading:
    results: tuple[RecordedBytePairResultPosition, ...] | tuple[_RecordedBytePairFinding, ...]
    binding: Event | None
    source: dict[str, Any]


def _recorded_input_result_position_coordinates(
    ledger: EventLedger,
    source: dict[str, Any],
    *,
    measurement_locality_identity: str,
    prior_coordinates: dict[str, Any] | None = None,
) -> tuple[dict[str, Any], dict[str, str | None]]:
    """Resolve the exact occurrences carrying one proposed input."""

    if type(source) is not dict or set(source) != {
        "recorded_occurrence_identity",
        "result_position",
        "locality_movement_event_identity",
    }:
        raise ByteMeasurementError(
            "byte-position-pair Applicability requires one exact result position"
        )
    movement_identity = _byte_result_position_movement_identity(source)
    if movement_identity is None:
        source_event = ledger.get(source["recorded_occurrence_identity"])
        exact = _byte_result_position(
            ledger,
            source["recorded_occurrence_identity"],
            source["result_position"],
            prior_coordinates=prior_coordinates,
        )
        if (
            source_event is None
            or source_event.locality_identity != measurement_locality_identity
        ):
            exact = None
    else:
        exact = _validate_moved_result_position(
            ledger,
            movement_identity,
            prior_destination_coordinates=prior_coordinates,
        )
        movement = ledger.get(movement_identity)
        if (
            movement is None
            or movement.locality_identity != measurement_locality_identity
        ):
            exact = None
    result_position = None
    if exact is not None:
        _event, result_position, _localities = _read_byte_result_position(
            ledger,
            exact,
            prior_coordinates=prior_coordinates,
        )
    if (
        exact is None
        or result_position is None
        or result_position["result"] != "exact_source_material_set"
        or _byte_result_position_reference(exact)
        != _byte_result_position_reference(source)
        or _byte_result_position_movement_identity(exact) != movement_identity
    ):
        raise ByteMeasurementError(
            "byte-position-pair Applicability requires exact input coordinates"
        )
    return exact, {
        "recorded_measurement_result_occurrence_identity": (
            exact["recorded_occurrence_identity"]
        ),
        "result_position": exact["result_position"],
        "locality_movement_result_occurrence_identity": (
            _byte_result_position_movement_identity(exact)
        ),
    }


def _pair_input_applicability(
    ledger: EventLedger,
    source: dict[str, Any],
    *,
    binding: Event,
    measurement_locality_identity: str,
    prior_coordinates: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Determine this source result position's use by this exact pair Measurement."""

    source, input_coordinates = _recorded_input_result_position_coordinates(
        ledger,
        source,
        measurement_locality_identity=measurement_locality_identity,
        prior_coordinates=prior_coordinates,
    )
    return _pair_input_applicability_from_exact_source(
        source,
        binding=binding,
        measurement_locality_identity=measurement_locality_identity,
        input_coordinates=input_coordinates,
    )


def _pair_input_applicability_from_exact_source(
    source: dict[str, Any],
    *,
    binding: Event,
    measurement_locality_identity: str,
    input_coordinates: dict[str, str | None] | None = None,
) -> dict[str, Any]:
    """Build Applicability from one validated exact source carrier."""

    if input_coordinates is None:
        input_coordinates = {
            "recorded_measurement_result_occurrence_identity": (
                source["recorded_occurrence_identity"]
            ),
            "result_position": source["result_position"],
            "locality_movement_result_occurrence_identity": (
                _byte_result_position_movement_identity(source)
            ),
        }
    reference = _byte_result_position_reference(source)
    movement_identity = _byte_result_position_movement_identity(source)
    content = {
        "input_result_position_reference": reference,
        "input_movement_event_identity": movement_identity,
        "addressed_act_identity": binding.material["addressed_act_identity"],
        "addressed_act": "declared byte-position-pair Measurement",
        "subject_to_act_binding_reference": (
            _pair_subject_to_act_binding_reference(binding)
        ),
        "applicability_act_identity": binding.material["exact_act_identity"],
        "applicability_act_occurrence_identity": binding.material[
            "applicability_act_occurrence_identity"
        ],
        "result_boundary": BYTE_PAIR_RESULT_BOUNDARY,
    }
    applicability = "applicable"
    identity = binding.material["applicability_result_identity"]
    return {
        "dimensions": {
            "identity": identity,
            "content": content,
            "applicability": applicability,
        },
        "result": "input_applicability",
        "input_result_position_reference": reference,
        "input_movement_event_identity": movement_identity,
        "addressed_act_identity": binding.material["addressed_act_identity"],
        "addressed_act_occurrence_identity": None,
        "subject_to_act_binding_reference": (
            _pair_subject_to_act_binding_reference(binding)
        ),
        "applicability_act_identity": binding.material["exact_act_identity"],
        "applicability_act_occurrence_identity": binding.material[
            "applicability_act_occurrence_identity"
        ],
        "addressed_act": "declared byte-position-pair Measurement",
        "result_boundary": BYTE_PAIR_RESULT_BOUNDARY,
        "measurement_locality": measurement_locality_identity,
        "input_coordinates": input_coordinates,
    }


def _material_result_bytes(ledger: EventLedger, occurrence) -> bytes:
    if ledger.integrity_of(occurrence.identity) == CORRUPTED:
        raise ByteMeasurementError(
            f"{occurrence.identity} is not an intact material result occurrence"
        )
    try:
        return exact_material_result_bytes(occurrence)
    except MaterialSourceError as exc:
        raise ByteMeasurementError(str(exc)) from exc


def _exact_material_results(
    ledger: EventLedger,
    locality_identity: str,
    *,
    through: EventLedgerBoundary,
):
    try:
        yield from iter_exact_material_results(
            ledger,
            locality_identity,
            through=through,
        )
    except MaterialSourceError as exc:
        raise ByteMeasurementError(
            "source carries a material result without intact physiology"
        ) from exc


def measure_byte_counts(
    ledger: EventLedger,
    *,
    source_localities: Iterable[str],
) -> MeasuredByteInputs:
    """Count every exact byte in every declared Locality through one boundary."""

    localities = tuple(dict.fromkeys(source_localities))
    if not localities or any(not isinstance(item, str) or not item for item in localities):
        raise ByteMeasurementError(
            "byte Measurement requires exact declared source Localities"
        )
    boundary = ledger.append_boundary()
    return _measure_byte_counts_through(
        ledger,
        localities=localities,
        boundary=boundary,
    )


def _measure_byte_counts_through(
    ledger: EventLedger,
    *,
    localities: tuple[str, ...],
    boundary: EventLedgerBoundary,
) -> MeasuredByteInputs:
    missing = [
        locality
        for locality in localities
        if not ledger.has_locality(locality, through=boundary)
    ]
    if missing:
        raise ByteMeasurementError(
            "declared source Localities are absent through the Measurement boundary: "
            + ", ".join(missing)
        )

    source_material: list[dict[str, str]] = []
    seen_material: set[str] = set()
    carrying = [0] * 256
    totals = [0] * 256
    for locality in localities:
        for material_result in _exact_material_results(
            ledger, locality, through=boundary
        ):
            exact = _material_result_bytes(ledger, material_result)
            if material_result.identity in seen_material:
                raise ByteMeasurementError(
                    "one material result occurrence cannot enter a byte Measurement twice"
                )
            seen_material.add(material_result.identity)
            source_material.append({"material_result_occurrence_identity": material_result.identity})
            for value, count in Counter(exact).items():
                carrying[value] += 1
                totals[value] += count
    if not source_material:
        raise ByteMeasurementError(
            "declared source Localities contain no material_result through the Measurement boundary"
        )
    counts = tuple(
        MeasuredByteCount(
            content=value,
            occurrences_carrying=carrying[value],
            count=totals[value],
        )
        for value in range(256)
        if totals[value] > 0
    )
    return MeasuredByteInputs(
        source_localities=localities,
        completeness_boundary=boundary,
        source_material=tuple(source_material),
        counts=counts,
    )


def _prepare_pair_source(
    ledger: EventLedger,
    *,
    source_measurement_event_identity: str,
    measurement_locality_identity: str,
    prior_coordinates: dict[str, Any] | None = None,
) -> tuple[dict[str, Any], tuple[str, ...], dict[str, Any]]:
    """Read one source before its act-local Applicability determination."""

    if (
        not isinstance(measurement_locality_identity, str)
        or not measurement_locality_identity
    ):
        raise ByteMeasurementError(
            "byte-position-pair Measurement requires an exact Act Locality"
        )
    read = _result_positions_of_recorded_byte_measurement(
        ledger,
        source_measurement_event_identity,
        prior_coordinates=prior_coordinates,
    )
    if read is None:
        raise ByteMeasurementError("byte-position-pair Measurement requires a source")
    source = next(
        (
            item
            for item in read
            if item["result"] == "exact_source_material_set"
        ),
        None,
    )
    if source is None:
        raise ByteMeasurementError(
            "byte-position-pair Measurement requires an exact source-material-set result position"
        )
    source = _byte_result_position(
        ledger,
        source_measurement_event_identity,
        source["dimensions"]["position"],
        prior_coordinates=prior_coordinates,
    )
    if source is None:
        raise ByteMeasurementError(
            "byte-position-pair Measurement requires exact source coordinates"
        )
    source = _move_byte_result_position_to_locality(
        ledger,
        source=source,
        destination_locality=measurement_locality_identity,
    )
    _event, material, source_localities = _read_byte_result_position(
        ledger,
        source,
        prior_coordinates=prior_coordinates,
    )
    content = material["dimensions"]["content"]
    return source, source_localities, content


def _movement_binding_reference(binding: Event) -> dict[str, str]:
    return {
        "recorded_occurrence_identity": binding.identity,
        "book_clause_identity": binding.material["book_clause_identity"],
    }


def _source_result_position_reference(
    source: dict[str, Any],
) -> dict[str, Any]:
    return _byte_result_position_reference(source)


def _source_result_position_coordinates(
    ledger: EventLedger,
    source: dict[str, Any],
) -> dict[str, Any]:
    source_event = ledger.get(source["recorded_occurrence_identity"])
    if source_event is None:
        raise ByteMeasurementError("result position movement source cannot be read")
    if source_event.kind == BYTE_MEASUREMENT_RECORDED_KIND:
        _event, material, _localities = _read_byte_result_position(ledger, source)
        return material

    from seed_runtime.measurement_of_position_coordinates_of_byte_pair_occurrences import (
        BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND,
        _recorded_position_result_content_at_position_for_locality_movement,
    )

    if source_event.kind == BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND:
        return _recorded_position_result_content_at_position_for_locality_movement(
            ledger,
            result_event_identity=source_event.identity,
            result_position=source["result_position"],
        )

    from seed_runtime.comparison_of_shared_position_measurement_with_recorded_pair_findings import (
        COMPARISON_OF_SHARED_POSITION_MEASUREMENT_WITH_RECORDED_PAIR_FINDINGS_RESULT_KIND,
        _recorded_shared_position_comparison_finding_result_content_for_locality_movement,
    )

    if (
        source_event.kind
        == COMPARISON_OF_SHARED_POSITION_MEASUREMENT_WITH_RECORDED_PAIR_FINDINGS_RESULT_KIND
    ):
        return _recorded_shared_position_comparison_finding_result_content_for_locality_movement(
            ledger,
            result_event_identity=source_event.identity,
            result_position=source["result_position"],
        )
    raise ByteMeasurementError("result position movement source cannot be read")


def _source_result_position_from_reference(
    ledger: EventLedger, reference: Any
) -> tuple[dict[str, Any], Event]:
    if type(reference) is not dict or "recorded_occurrence_identity" not in reference:
        raise ByteMeasurementError("result position movement carries no exact source")
    source_event = ledger.get(reference["recorded_occurrence_identity"])
    if source_event is None or source_event.locality_identity is None:
        raise ByteMeasurementError("result position movement source cannot be read")
    if source_event.kind == BYTE_MEASUREMENT_RECORDED_KIND:
        if (
            set(reference)
            != {"recorded_occurrence_identity", "result_position"}
            or type(reference["result_position"]) is not int
            or reference["result_position"] < 0
        ):
            raise ByteMeasurementError("result position movement carries no exact source")
        source = _byte_result_position(
            ledger,
            source_event.identity,
            reference["result_position"],
        )
        if source is not None:
            return source, source_event

    from seed_runtime.measurement_of_position_coordinates_of_byte_pair_occurrences import (
        BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND,
        _recorded_position_result_content_at_position_for_locality_movement,
    )

    if source_event.kind == BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND:
        if set(reference) != {
            "recorded_occurrence_identity",
            "result_position",
        } or type(reference["result_position"]) is not int:
            raise ByteMeasurementError("result position movement carries no exact source")
        try:
            coordinates = _recorded_position_result_content_at_position_for_locality_movement(
                ledger,
                result_event_identity=source_event.identity,
                result_position=reference["result_position"],
            )
        except ValueError:
            pass
        else:
            return {
                **deepcopy(reference),
                "locality_movement_event_identity": None,
            }, source_event

    from seed_runtime.comparison_of_shared_position_measurement_with_recorded_pair_findings import (
        COMPARISON_OF_SHARED_POSITION_MEASUREMENT_WITH_RECORDED_PAIR_FINDINGS_RESULT_KIND,
        _recorded_shared_position_comparison_finding_result_content_for_locality_movement,
    )

    if (
        source_event.kind
        == COMPARISON_OF_SHARED_POSITION_MEASUREMENT_WITH_RECORDED_PAIR_FINDINGS_RESULT_KIND
    ):
        if set(reference) != {
            "recorded_occurrence_identity",
            "result_position",
        } or type(reference["result_position"]) is not int:
            raise ByteMeasurementError("result position movement carries no exact source")
        try:
            coordinates = _recorded_shared_position_comparison_finding_result_content_for_locality_movement(
                ledger,
                result_event_identity=source_event.identity,
                result_position=reference["result_position"],
            )
        except ValueError:
            pass
        else:
            return {
                **deepcopy(reference),
                "locality_movement_event_identity": None,
            }, source_event
    raise ByteMeasurementError("result position movement source cannot be read")


def _source_measurement_current_coordinates(source_event: Event) -> dict[str, str]:
    coordinates = {
        "recorded_occurrence_identity": source_event.identity,
        "result_identity": source_event.material["result_identity"],
        "act_occurrence_identity": source_event.material["act_occurrence_identity"],
        "act_occurrence_event_identity": source_event.material[
            "act_occurrence_event_identity"
        ],
    }
    yield_relation_identity = source_event.material.get("yield_relation_identity")
    if type(yield_relation_identity) is str and yield_relation_identity:
        coordinates["yield_relation_identity"] = yield_relation_identity
    return coordinates


def _source_result_position_is_carried(
    source_event: Event, current_coordinates: dict[str, Any]
) -> bool:
    from seed_runtime.comparison_of_shared_position_measurement_with_recorded_pair_findings import (
        COMPARISON_OF_SHARED_POSITION_MEASUREMENT_WITH_RECORDED_PAIR_FINDINGS_RESULT_KIND,
    )

    if (
        source_event.kind
        == COMPARISON_OF_SHARED_POSITION_MEASUREMENT_WITH_RECORDED_PAIR_FINDINGS_RESULT_KIND
    ):
        return (
            current_coordinates.get("comparison_result_occurrences", {}).get(
                source_event.identity, object()
            )
            is None
        )
    return current_coordinates.get("measurement_occurrences", {}).get(
        source_event.identity
    ) == _source_measurement_current_coordinates(source_event)


def _require_current_movement_source_coordinates(
    ledger: EventLedger,
    *,
    source_event: Event,
    current_coordinates: dict[str, Any],
) -> str:
    from seed_runtime.operator_current_coordinates import read_operator_current_coordinates

    current = read_operator_current_coordinates(
        ledger, locality_identity=source_event.locality_identity
    )
    boundary = current_coordinates.get("through_event_occurrence_identity")
    if (
        current_coordinates != current
        or type(boundary) is not str
        or not boundary
        or not _source_result_position_is_carried(source_event, current_coordinates)
    ):
        raise ByteMeasurementError(
            "result position movement binding requires exact current source coordinates"
        )
    return boundary


def _require_current_movement_destination_coordinates(
    ledger: EventLedger,
    *,
    destination_locality: str,
    current_coordinates: dict[str, Any],
    binding_identity: str | None = None,
) -> str | None:
    from seed_runtime.operator_current_coordinates import read_operator_current_coordinates

    current = read_operator_current_coordinates(
        ledger, locality_identity=destination_locality
    )
    boundary = current_coordinates.get("through_event_occurrence_identity")
    bindings = current_coordinates.get("subject_to_act_binding_occurrences")
    if (
        current_coordinates != current
        or current_coordinates.get("locality_identity") != destination_locality
        or (boundary is not None and (type(boundary) is not str or not boundary))
        or (
            binding_identity is not None
            and (
                type(bindings) is not dict
                or bindings.get(binding_identity, object()) is not None
            )
        )
    ):
        raise ByteMeasurementError(
            "result position movement requires exact current destination coordinates"
        )
    return boundary


def _movement_binding_material(
    *,
    source: dict[str, Any],
    source_result_position_coordinates: dict[str, Any],
    source_event: Event,
    source_locality: str,
    destination_locality: str,
    source_through_event_occurrence_identity: str,
    destination_through_event_occurrence_identity: str | None,
    movement_act_identity: str,
    movement_act_occurrence_identity: str,
    movement_result_identity: str,
) -> dict[str, Any]:
    return {
        "movement_act_identity": movement_act_identity,
        "movement_act_occurrence_identity": movement_act_occurrence_identity,
        "movement_result_identity": movement_result_identity,
        "book_clause_identity": "03.Movement.A",
        "source_result_position_reference": _source_result_position_reference(source),
        "source_result_position_coordinates": deepcopy(source_result_position_coordinates),
        "source_locality": source_locality,
        "destination_locality": destination_locality,
        "source_through_event_occurrence_identity": source_through_event_occurrence_identity,
        "destination_through_event_occurrence_identity": (
            destination_through_event_occurrence_identity
        ),
        "determination": (
            "exact addressed result content in another Locality"
        ),
    }


def _require_exact_movement_binding_and_source(
    ledger: EventLedger, binding: Event
) -> tuple[dict[str, Any], Event]:
    if (
        type(binding) is not Event
        or binding.kind
        != RESULT_POSITION_LOCALITY_MOVEMENT_SUBJECT_TO_ACT_BINDING_KIND
        or binding.locality_identity is None
        or ledger.get(binding.identity) != binding
        or ledger.integrity_of(binding.identity) == CORRUPTED
    ):
        raise ByteMeasurementError(
            "result position movement requires an exact subject-to-Act binding"
        )
    source, source_event = _source_result_position_from_reference(
        ledger, binding.material.get("source_result_position_reference")
    )
    identity_coordinates = (
        "movement_act_identity",
        "movement_act_occurrence_identity",
        "movement_result_identity",
    )
    identities = {
        coordinate: binding.material.get(coordinate)
        for coordinate in identity_coordinates
    }
    source_boundary = binding.material.get("source_through_event_occurrence_identity")
    destination_boundary = binding.material.get(
        "destination_through_event_occurrence_identity"
    )
    if (
        type(source_boundary) is not str
        or not source_boundary
        or any(
            type(identity) is not str or not identity
            for identity in identities.values()
        )
        or len(set(identities.values())) != len(identities)
        or binding.material
        != _movement_binding_material(
            source=source,
            source_result_position_coordinates=_source_result_position_coordinates(ledger, source),
            source_event=source_event,
            source_locality=source_event.locality_identity,
            destination_locality=binding.locality_identity,
            source_through_event_occurrence_identity=source_boundary,
            destination_through_event_occurrence_identity=destination_boundary,
            **identities,
        )
    ):
        raise ByteMeasurementError(
            "result position movement requires an exact source and binding"
        )
    return source, source_event


def record_result_position_locality_movement_subject_to_act_binding(
    ledger: EventLedger,
    *,
    source: dict[str, Any],
    destination_locality: str,
    source_current_coordinates: dict[str, Any],
    destination_current_coordinates: dict[str, Any],
) -> Event:
    """Record the exact subject-to-Act binding for one result position movement."""

    if type(destination_locality) is not str or not destination_locality:
        raise ByteMeasurementError("result position movement requires a destination Locality")
    exact_source, source_event = _source_result_position_from_reference(
        ledger, _byte_result_position_reference(source)
    )
    if exact_source != source:
        raise ByteMeasurementError("result position movement requires its exact source")
    if source_event.locality_identity == destination_locality:
        raise ByteMeasurementError("same-Locality result position requires no movement")
    source_boundary = _require_current_movement_source_coordinates(
        ledger,
        source_event=source_event,
        current_coordinates=source_current_coordinates,
    )
    destination_boundary = _require_current_movement_destination_coordinates(
        ledger,
        destination_locality=destination_locality,
        current_coordinates=destination_current_coordinates,
    )
    identities = {
        "movement_act_identity": ledger.mint_identity("result_position_locality_movement_act"),
        "movement_act_occurrence_identity": ledger.mint_identity(
            "result_position_locality_movement_occurrence"
        ),
        "movement_result_identity": ledger.mint_identity(
            "result_position_locality_movement_result"
        ),
    }
    if len(set(identities.values())) != len(identities):
        raise ByteMeasurementError("result position movement lifecycle identities collapsed")
    return ledger.append(
        RESULT_POSITION_LOCALITY_MOVEMENT_SUBJECT_TO_ACT_BINDING_KIND,
        _movement_binding_material(
            source=source,
            source_result_position_coordinates=_source_result_position_coordinates(ledger, source),
            source_event=source_event,
            source_locality=source_event.locality_identity,
            destination_locality=destination_locality,
            source_through_event_occurrence_identity=source_boundary,
            destination_through_event_occurrence_identity=destination_boundary,
            **identities,
        ),
        locality_identity=destination_locality,
    )


def _read_result_position_locality_movement_subject_to_act_binding(
    ledger: EventLedger,
    binding_event_identity: str,
    *,
    prior_destination_coordinates: dict[str, Any] | None = None,
) -> tuple[Event, dict[str, Any], Event]:
    binding = ledger.get(binding_event_identity)
    if (
        binding is None
        or binding.kind
        != RESULT_POSITION_LOCALITY_MOVEMENT_SUBJECT_TO_ACT_BINDING_KIND
        or binding.locality_identity is None
        or ledger.integrity_of(binding.identity) == CORRUPTED
    ):
        raise ByteMeasurementError(
            "result position movement binding is absent or corrupted"
        )
    material = binding.material
    source, source_event = _source_result_position_from_reference(
        ledger, material.get("source_result_position_reference")
    )
    identities = {
        coordinate: material.get(coordinate)
        for coordinate in (
            "movement_act_identity",
            "movement_act_occurrence_identity",
            "movement_result_identity",
        )
    }
    source_boundary = material.get("source_through_event_occurrence_identity")
    destination_boundary = material.get("destination_through_event_occurrence_identity")
    if (
        any(type(identity) is not str or not identity for identity in identities.values())
        or len(set(identities.values())) != len(identities)
        or type(source_boundary) is not str
        or not source_boundary
        or (
            destination_boundary is not None
            and (type(destination_boundary) is not str or not destination_boundary)
        )
    ):
        raise ByteMeasurementError(
            "result position movement binding carries malformed coordinates"
        )
    expected = _movement_binding_material(
        source=source,
        source_result_position_coordinates=_source_result_position_coordinates(ledger, source),
        source_event=source_event,
        source_locality=source_event.locality_identity,
        destination_locality=binding.locality_identity,
        source_through_event_occurrence_identity=source_boundary,
        destination_through_event_occurrence_identity=destination_boundary,
        **identities,
    )
    if material != expected:
        raise ByteMeasurementError(
            "result position movement binding coordinates are not exact"
        )
    from seed_runtime.operator_current_coordinates import (
        read_operator_current_coordinates_through,
    )

    try:
        source_coordinates = read_operator_current_coordinates_through(
            ledger,
            locality_identity=source_event.locality_identity,
            through_event_occurrence_identity=source_boundary,
        )
        if prior_destination_coordinates is None:
            prior_destination_coordinates = read_operator_current_coordinates_through(
                ledger,
                locality_identity=binding.locality_identity,
                through_event_occurrence_identity=destination_boundary,
            )
    except (TypeError, ValueError) as error:
        raise ByteMeasurementError(
            "result position movement binding has no exact current coordinates"
        ) from error
    if not _source_result_position_is_carried(source_event, source_coordinates):
        raise ByteMeasurementError(
            "result position movement binding has no exact source coordinates"
        )
    prior_destination_boundary = prior_destination_coordinates.get(
        "through_event_occurrence_identity"
    )
    carried_bindings = prior_destination_coordinates.get(
        "subject_to_act_binding_occurrences"
    )
    destination_boundary_is_exact = prior_destination_boundary == destination_boundary
    binding_is_carried_later = bool(
        type(prior_destination_boundary) is str
        and prior_destination_boundary
        and type(carried_bindings) is dict
        and carried_bindings.get(binding.identity, object()) is None
    )
    if (
        prior_destination_coordinates.get("locality_identity")
        != binding.locality_identity
        or not (destination_boundary_is_exact or binding_is_carried_later)
    ):
        raise ByteMeasurementError(
            "result position movement binding has no exact destination coordinates"
        )
    order = (binding.identity,)
    if destination_boundary is not None:
        order = (destination_boundary, binding.identity)
    if binding_is_carried_later and prior_destination_boundary != binding.identity:
        order = (*order, prior_destination_boundary)
    try:
        ledger.occurrences_in_append_order(
            order, locality_identity=binding.locality_identity
        )
    except ValueError as error:
        raise ByteMeasurementError(
            "result position movement binding order is false"
        ) from error
    return binding, source, source_event


def get_result_position_locality_movement_subject_to_act_binding(
    ledger: EventLedger, binding_event_identity: str
) -> Event:
    return _read_result_position_locality_movement_subject_to_act_binding(
        ledger, binding_event_identity
    )[0]


def _movement_act_material(binding: Event) -> dict[str, Any]:
    return {
        "act": "result-position Locality movement",
        "subject_to_act_binding_reference": _movement_binding_reference(
            binding
        ),
        "movement_act_identity": binding.material["movement_act_identity"],
        "movement_act_occurrence_identity": binding.material[
            "movement_act_occurrence_identity"
        ],
        "source_result_position_reference": binding.material[
            "source_result_position_reference"
        ],
        "source_locality": binding.material["source_locality"],
        "destination_locality": binding.locality_identity,
        "locality_relation": {
            "first_subject": binding.material["source_result_position_reference"],
            "second_subject": binding.locality_identity,
            "relation_occurrence_identity": binding.material[
                "movement_act_occurrence_identity"
            ],
        },
    }


def record_result_position_locality_movement_act_occurrence(
    ledger: EventLedger,
    *,
    subject_to_act_binding_event_identity: str,
    current_coordinates: dict[str, Any],
) -> Event:
    binding, _source, _source_event = (
        _read_result_position_locality_movement_subject_to_act_binding(
            ledger, subject_to_act_binding_event_identity
        )
    )
    _require_current_movement_destination_coordinates(
        ledger,
        destination_locality=binding.locality_identity,
        current_coordinates=current_coordinates,
        binding_identity=binding.identity,
    )
    for prior in ledger.iter_locality_kind(
        binding.locality_identity,
        RESULT_POSITION_LOCALITY_MOVEMENT_ACT_OCCURRENCE_EVENT,
    ):
        if prior.material.get("subject_to_act_binding_reference") == (
            _movement_binding_reference(binding)
        ):
            raise ByteMeasurementError(
                "result position movement binding carries one Act"
            )
    return ledger.append(
        RESULT_POSITION_LOCALITY_MOVEMENT_ACT_OCCURRENCE_EVENT,
        _movement_act_material(binding),
        locality_identity=binding.locality_identity,
    )


def _record_result_position_locality_movement_act_from_current_coordinates(
    ledger: EventLedger,
    *,
    binding: Event,
    destination_coordinates: dict[str, Any],
) -> Event:
    try:
        _require_exact_movement_binding_and_source(ledger, binding)
    except (ByteMeasurementError, TypeError, ValueError) as error:
        raise ByteMeasurementError(
            "result position movement Act requires an exact source and binding"
        ) from error
    if (
        binding.kind
        != RESULT_POSITION_LOCALITY_MOVEMENT_SUBJECT_TO_ACT_BINDING_KIND
        or ledger.get(binding.identity) != binding
        or ledger.integrity_of(binding.identity) == CORRUPTED
        or destination_coordinates.get("locality_identity")
        != binding.locality_identity
        or destination_coordinates.get("through_event_occurrence_identity")
        != binding.identity
        or destination_coordinates.get(
            "subject_to_act_binding_occurrences", {}
        ).get(binding.identity, object())
        is not None
        or ledger.append_boundary_through_occurrence(binding.identity)
        != ledger.append_boundary()
    ):
        raise ByteMeasurementError(
            "result position movement Act requires exact carried binding coordinates"
        )
    return ledger.append(
        RESULT_POSITION_LOCALITY_MOVEMENT_ACT_OCCURRENCE_EVENT,
        _movement_act_material(binding),
        locality_identity=binding.locality_identity,
    )


def _read_result_position_locality_movement_act_occurrence(
    ledger: EventLedger,
    act_occurrence_event_identity: str,
    *,
    prior_destination_coordinates: dict[str, Any] | None = None,
) -> tuple[Event, Event, dict[str, Any]]:
    act = ledger.get(act_occurrence_event_identity)
    if (
        act is None
        or act.kind != RESULT_POSITION_LOCALITY_MOVEMENT_ACT_OCCURRENCE_EVENT
        or ledger.integrity_of(act.identity) == CORRUPTED
    ):
        raise ByteMeasurementError("result position movement Act occurrence is absent or corrupted")
    reference = act.material.get("subject_to_act_binding_reference")
    if type(reference) is not dict:
        raise ByteMeasurementError("result position movement Act carries no exact binding")
    binding, source, _source_event = (
        _read_result_position_locality_movement_subject_to_act_binding(
            ledger,
            reference.get("recorded_occurrence_identity"),
            prior_destination_coordinates=prior_destination_coordinates,
        )
    )
    if (
        reference != _movement_binding_reference(binding)
        or act.locality_identity != binding.locality_identity
        or act.material != _movement_act_material(binding)
    ):
        raise ByteMeasurementError("result position movement Act occurrence is not exact")
    try:
        ledger.occurrences_in_append_order(
            (binding.identity, act.identity),
            locality_identity=binding.locality_identity,
        )
    except ValueError as error:
        raise ByteMeasurementError("result position movement Act order is false") from error
    return act, binding, source


def _movement_result_material(
    binding: Event,
) -> dict[str, Any]:
    return {
        "result_identity": binding.material["movement_result_identity"],
        "movement_act_identity": binding.material["movement_act_identity"],
        "movement_act_occurrence_identity": binding.material[
            "movement_act_occurrence_identity"
        ],
        "subject_to_act_binding_reference": _movement_binding_reference(
            binding
        ),
        "source_result_position_reference": binding.material[
            "source_result_position_reference"
        ],
        "source_result_position_coordinates": binding.material[
            "source_result_position_coordinates"
        ],
        "source_locality": binding.material["source_locality"],
        "destination_locality": binding.locality_identity,
        "locality_relation": {
            "first_subject": binding.material["source_result_position_reference"],
            "second_subject": binding.locality_identity,
            "relation_occurrence_identity": binding.material[
                "movement_act_occurrence_identity"
            ],
        },
    }


def record_result_position_locality_movement_result(
    ledger: EventLedger, *, act_occurrence_event_identity: str
) -> Event:
    act, binding, _source = _read_result_position_locality_movement_act_occurrence(
        ledger, act_occurrence_event_identity
    )
    for prior in ledger.iter_locality_kind(
        binding.locality_identity, RESULT_POSITION_LOCALITY_MOVEMENT_KIND
    ):
        if prior.material.get("act_occurrence_event_identity") == act.identity:
            raise ByteMeasurementError(
                "result position movement Act has one result"
            )
    return _append_result_position_locality_movement_result(
        ledger, act=act, binding=binding
    )


def _append_result_position_locality_movement_result(
    ledger: EventLedger, *, act: Event, binding: Event
) -> Event:
    _require_exact_movement_binding_and_source(ledger, binding)
    if (
        ledger.get(act.identity) != act
        or ledger.integrity_of(act.identity) == CORRUPTED
        or act.material != _movement_act_material(binding)
        or ledger.append_boundary_through_occurrence(act.identity)
        != ledger.append_boundary()
    ):
        raise ByteMeasurementError(
            "result position movement result requires its exact source and Act"
        )
    return ledger.append(
        RESULT_POSITION_LOCALITY_MOVEMENT_KIND,
        {
            **_movement_result_material(binding),
            "act_occurrence_event_identity": act.identity,
        },
        locality_identity=binding.locality_identity,
    )


def _record_result_position_locality_movement_result_from_current_coordinates(
    ledger: EventLedger,
    *,
    act: Event,
    binding: Event,
    destination_coordinates: dict[str, Any] | None = None,
) -> Event:
    if destination_coordinates is not None:
        try:
            _require_exact_movement_binding_and_source(ledger, binding)
        except (ByteMeasurementError, TypeError, ValueError) as error:
            raise ByteMeasurementError(
                "result position movement result requires an exact source and Act"
            ) from error
        if act.material != _movement_act_material(binding):
            raise ByteMeasurementError(
                "result position movement result requires an exact source and Act"
            )
    if (
        ledger.get(act.identity) != act
        or act.kind != RESULT_POSITION_LOCALITY_MOVEMENT_ACT_OCCURRENCE_EVENT
        or ledger.integrity_of(act.identity) == CORRUPTED
        or act.locality_identity != binding.locality_identity
        or act.material != _movement_act_material(binding)
        or ledger.append_boundary_through_occurrence(act.identity)
        != ledger.append_boundary()
    ):
        raise ByteMeasurementError(
            "result position movement result requires its exact carried Act at the current append boundary"
        )
    return _append_result_position_locality_movement_result(
        ledger, act=act, binding=binding
    )


def _move_byte_result_position_to_locality(
    ledger: EventLedger,
    *,
    source: dict[str, Any],
    destination_locality: str,
) -> dict[str, Any]:
    """Preserve one result position movement without copying the result position."""

    source_event = ledger.get(source["recorded_occurrence_identity"])
    if source_event is None:
        raise ByteMeasurementError("result position locality movement requires its source")
    if source_event.locality_identity == destination_locality:
        return source
    from seed_runtime.operator_current_coordinates import read_operator_current_coordinates

    binding = record_result_position_locality_movement_subject_to_act_binding(
        ledger,
        source=source,
        destination_locality=destination_locality,
        source_current_coordinates=read_operator_current_coordinates(
            ledger, locality_identity=source_event.locality_identity
        ),
        destination_current_coordinates=read_operator_current_coordinates(
            ledger, locality_identity=destination_locality
        ),
    )
    act = record_result_position_locality_movement_act_occurrence(
        ledger,
        subject_to_act_binding_event_identity=binding.identity,
        current_coordinates=read_operator_current_coordinates(
            ledger, locality_identity=destination_locality
        ),
    )
    movement = record_result_position_locality_movement_result(
        ledger, act_occurrence_event_identity=act.identity
    )
    exact = _validate_moved_result_position(ledger, movement.identity)
    if exact is None:
        raise ByteMeasurementError("result position locality movement is absent")
    return exact


def move_recorded_byte_result_position_to_locality(
    ledger: EventLedger,
    *,
    source: dict[str, Any],
    destination_locality: str,
) -> dict[str, Any]:
    return _move_byte_result_position_to_locality(
        ledger,
        source=source,
        destination_locality=destination_locality,
    )


def _move_result_position_reference_to_locality(
    ledger: EventLedger,
    *,
    source_result_position_reference: dict[str, str],
    destination_locality: str,
) -> dict[str, Any]:
    """Carry one exact supported result position through one 03.Movement.A occurrence."""

    source, source_event = _source_result_position_from_reference(
        ledger, source_result_position_reference
    )
    if source_event.kind == BYTE_MEASUREMENT_RECORDED_KIND:
        raise ByteMeasurementError(
            "this movement road requires a position or shared-position Compare result position"
        )
    if source_event.locality_identity == destination_locality:
        raise ByteMeasurementError("same-Locality result position requires no movement")
    from seed_runtime.operator_current_coordinates import (
        _carry_result_position_locality_movement_act_into_current_coordinates,
        _carry_result_position_locality_movement_binding_into_current_coordinates,
        _carry_result_position_locality_movement_result_into_current_coordinates,
        read_operator_current_coordinates,
    )

    source_coordinates = read_operator_current_coordinates(
        ledger, locality_identity=source_event.locality_identity
    )
    _require_current_movement_source_coordinates(
        ledger, source_event=source_event, current_coordinates=source_coordinates
    )
    destination_coordinates = read_operator_current_coordinates(
        ledger, locality_identity=destination_locality
    )
    _require_current_movement_destination_coordinates(
        ledger,
        destination_locality=destination_locality,
        current_coordinates=destination_coordinates,
    )
    binding = _record_movement_binding_from_current_coordinates(
        ledger,
        source=source,
        source_event=source_event,
        source_coordinates=source_coordinates,
        destination_locality=destination_locality,
        destination_coordinates=destination_coordinates,
    )
    destination_coordinates = (
        _carry_result_position_locality_movement_binding_into_current_coordinates(
            ledger,
            destination_coordinates,
            binding,
            source=source,
            source_event=source_event,
            source_current_coordinates=source_coordinates,
        )
    )
    act = _record_result_position_locality_movement_act_from_current_coordinates(
        ledger,
        binding=binding,
        destination_coordinates=destination_coordinates,
    )
    destination_coordinates = _carry_result_position_locality_movement_act_into_current_coordinates(
        ledger,
        destination_coordinates,
        act,
        binding=binding,
    )
    movement = _record_result_position_locality_movement_result_from_current_coordinates(
        ledger,
        act=act,
        binding=binding,
        destination_coordinates=destination_coordinates,
    )
    _destination_coordinates, carried = (
        _carry_result_position_locality_movement_result_into_current_coordinates(
            ledger,
            destination_coordinates,
            movement,
            act_occurrence=act,
            binding=binding,
            source=source,
        )
    )
    if type(carried) is not dict:
        raise ByteMeasurementError(
            "result-position Locality movement has no exact result"
        )
    return carried


def _record_movement_binding_from_current_coordinates(
    ledger: EventLedger,
    *,
    source: dict[str, Any],
    source_event: Event,
    source_coordinates: dict[str, Any],
    destination_locality: str,
    destination_coordinates: dict[str, Any],
) -> Event:
    source_boundary = source_coordinates.get("through_event_occurrence_identity")
    destination_boundary = destination_coordinates.get(
        "through_event_occurrence_identity"
    )
    if (
        source_coordinates.get("locality_identity") != source_event.locality_identity
        or type(source_boundary) is not str
        or not source_boundary
        or not _source_result_position_is_carried(source_event, source_coordinates)
        or destination_coordinates.get("locality_identity") != destination_locality
        or (
            destination_boundary is not None
            and (
                type(destination_boundary) is not str
                or not destination_boundary
            )
        )
    ):
        raise ByteMeasurementError(
            "result position movement binding requires exact current source and destination coordinates"
    )
    identities = {
        "movement_act_identity": ledger.mint_identity("result_position_locality_movement_act"),
        "movement_act_occurrence_identity": ledger.mint_identity(
            "result_position_locality_movement_occurrence"
        ),
        "movement_result_identity": ledger.mint_identity(
            "result_position_locality_movement_result"
        ),
    }
    if len(set(identities.values())) != len(identities):
        raise ByteMeasurementError("result position movement lifecycle identities collapsed")
    return ledger.append(
        RESULT_POSITION_LOCALITY_MOVEMENT_SUBJECT_TO_ACT_BINDING_KIND,
        _movement_binding_material(
            source=source,
            source_result_position_coordinates=_source_result_position_coordinates(ledger, source),
            source_event=source_event,
            source_locality=source_event.locality_identity,
            destination_locality=destination_locality,
            source_through_event_occurrence_identity=source_boundary,
            destination_through_event_occurrence_identity=destination_boundary,
            **identities,
        ),
        locality_identity=destination_locality,
    )


def move_recorded_byte_result_positions_to_locality(
    ledger: EventLedger,
    *,
    sources: tuple[dict[str, Any], ...],
    destination_locality: str,
) -> tuple[dict[str, Any], ...]:
    """Move one exact result's result positions in one bounded same-call lifecycle."""

    if not sources:
        return ()
    source_event_identity = sources[0]["recorded_occurrence_identity"]
    if any(
        source["recorded_occurrence_identity"] != source_event_identity
        for source in sources
    ):
        raise ByteMeasurementError(
            "bounded result position movement requires one exact source result"
        )
    source_event = ledger.get(source_event_identity)
    if source_event is None or source_event.locality_identity is None:
        raise ByteMeasurementError("result position locality movement requires its source")
    if source_event.locality_identity == destination_locality:
        return sources
    exact_sources = {
        source["result_position"]: _byte_result_position(
            ledger,
            source_event_identity,
            source["result_position"],
        )
        for source in sources
    }
    if any(
        exact_sources.get(source["result_position"]) != source
        for source in sources
    ):
        raise ByteMeasurementError(
            "bounded result position movement requires each exact source result position"
        )
    from seed_runtime.operator_current_coordinates import (
        _carry_result_position_locality_movement_act_into_current_coordinates,
        _carry_result_position_locality_movement_binding_into_current_coordinates,
        _carry_result_position_locality_movement_result_into_current_coordinates,
        read_operator_current_coordinates,
    )

    source_coordinates = read_operator_current_coordinates(
        ledger, locality_identity=source_event.locality_identity
    )
    _require_current_movement_source_coordinates(
        ledger, source_event=source_event, current_coordinates=source_coordinates
    )
    destination_coordinates = read_operator_current_coordinates(
        ledger, locality_identity=destination_locality
    )
    _require_current_movement_destination_coordinates(
        ledger,
        destination_locality=destination_locality,
        current_coordinates=destination_coordinates,
    )
    moved = []
    for source in sources:
        binding = _record_movement_binding_from_current_coordinates(
            ledger,
            source=source,
            source_event=source_event,
            source_coordinates=source_coordinates,
            destination_locality=destination_locality,
            destination_coordinates=destination_coordinates,
        )
        destination_coordinates = (
            _carry_result_position_locality_movement_binding_into_current_coordinates(
                ledger,
                destination_coordinates,
                binding,
                source=source,
                source_event=source_event,
                source_current_coordinates=source_coordinates,
            )
        )
        act = _record_result_position_locality_movement_act_from_current_coordinates(
            ledger,
            binding=binding,
            destination_coordinates=destination_coordinates,
        )
        destination_coordinates = _carry_result_position_locality_movement_act_into_current_coordinates(
            ledger,
            destination_coordinates,
            act,
            binding=binding,
        )
        movement = _record_result_position_locality_movement_result_from_current_coordinates(
            ledger,
            act=act,
            binding=binding,
            destination_coordinates=destination_coordinates,
        )
        destination_coordinates, exact = (
            _carry_result_position_locality_movement_result_into_current_coordinates(
                ledger,
                destination_coordinates,
                movement,
                act_occurrence=act,
                binding=binding,
                source=source,
            )
        )
        moved.append(exact)
    return tuple(moved)


def _result_position_addressed_by_locality_movement_result(
    *,
    movement: Event,
    binding: Event,
    source: dict[str, Any],
) -> dict[str, Any]:
    """Carry the source result position with one exact movement result."""

    if (
        movement.material.get("subject_to_act_binding_reference")
        != _movement_binding_reference(binding)
        or binding.material.get("source_result_position_reference")
        != _source_result_position_reference(source)
        or movement.material.get("source_result_position_reference")
        != _source_result_position_reference(source)
    ):
        raise ByteMeasurementError(
            "result position locality movement carries no exact source"
        )
    return {
        **_byte_result_position_reference(source),
        "locality_movement_event_identity": movement.identity,
    }


def _validate_moved_result_position(
    ledger: EventLedger,
    movement_event_identity: str,
    *,
    prior_destination_coordinates: dict[str, Any] | None = None,
) -> dict[str, Any] | None:
    movement = ledger.get(movement_event_identity)
    if movement is None or movement.kind != RESULT_POSITION_LOCALITY_MOVEMENT_KIND:
        return None
    if ledger.integrity_of(movement.identity) == CORRUPTED:
        raise ByteMeasurementError("result position locality movement is corrupted")
    act_occurrence, binding, source = (
        _read_result_position_locality_movement_act_occurrence(
            ledger,
            movement.material.get("act_occurrence_event_identity"),
            prior_destination_coordinates=prior_destination_coordinates,
        )
    )
    if (
        movement.locality_identity != binding.locality_identity
        or movement.material.get("subject_to_act_binding_reference")
        != _movement_binding_reference(binding)
    ):
        raise ByteMeasurementError(
            "result position locality movement carries no exact binding"
        )
    expected = {
        **_movement_result_material(binding),
        "act_occurrence_event_identity": act_occurrence.identity,
    }
    if movement.material != expected:
        raise ByteMeasurementError("result position locality movement is not exact")
    try:
        ordered = ledger.occurrences_in_append_order(
            (act_occurrence.identity, movement.identity),
            locality_identity=movement.locality_identity,
        )
    except ValueError as error:
        raise ByteMeasurementError(
            "result position movement result does not follow its Act"
        ) from error
    if [occurrence.identity for occurrence in ordered] != [
        act_occurrence.identity,
        movement.identity,
    ]:
        raise ByteMeasurementError(
            "result position movement result does not follow its Act"
        )
    results = tuple(
        candidate
        for candidate in ledger.iter_locality_kind(
            movement.locality_identity,
            RESULT_POSITION_LOCALITY_MOVEMENT_KIND,
        )
        if candidate.material.get("act_occurrence_event_identity")
        == act_occurrence.identity
    )
    if len(results) != 1 or results[0].identity != movement.identity:
        raise ByteMeasurementError(
            "result position movement Act has no single exact result"
        )
    return _result_position_addressed_by_locality_movement_result(
        movement=movement,
        binding=binding,
        source=source,
    )


def _measure_byte_position_pair_counts_through(
    ledger: EventLedger,
    *,
    localities: tuple[str, ...],
    boundary: EventLedgerBoundary,
    source_result_position_reference: dict[str, str],
    source_movement_event_identity: str | None,
    input_applicability: dict[str, Any],
    addressed_act_identity: str,
    act_occurrence_identity: str,
) -> MeasuredBytePairInputs:
    missing = [
        locality
        for locality in localities
        if not ledger.has_locality(locality, through=boundary)
    ]
    if missing:
        raise ByteMeasurementError(
            "declared source Localities are absent through the Measurement boundary: "
            + ", ".join(missing)
        )

    source_material: list[dict[str, str]] = []
    seen_material: set[str] = set()
    totals: dict[bytes, int] = {}
    carrying: dict[bytes, int] = {}
    for locality in localities:
        for material_result in _exact_material_results(
            ledger, locality, through=boundary
        ):
            if ledger.integrity_of(material_result.identity) == CORRUPTED:
                raise ByteMeasurementError(
                    "corrupted material_result cannot participate in byte-position-pair Measurement"
                )
            exact = _material_result_bytes(ledger, material_result)
            if material_result.identity in seen_material:
                raise ByteMeasurementError(
                    "one material result occurrence cannot enter a pair Measurement twice"
                )
            seen_material.add(material_result.identity)
            source_material.append({"material_result_occurrence_identity": material_result.identity})
            seen: set[bytes] = set()
            for index in range(len(exact) - 1):
                pair = exact[index : index + 2]
                totals[pair] = totals.get(pair, 0) + 1
                seen.add(pair)
            for pair in seen:
                carrying[pair] = carrying.get(pair, 0) + 1
    if not source_material:
        raise ByteMeasurementError(
            "declared source Localities contain no material_result through the Measurement boundary"
        )
    counts = tuple(
        MeasuredBytePairCount(
            content=(pair[0], pair[1]),
            occurrences_carrying=carrying[pair],
            count=totals[pair],
        )
        for pair in totals
    )
    return MeasuredBytePairInputs(
        source_localities=localities,
        completeness_boundary=boundary,
        source_material=tuple(source_material),
        source_result_position_reference=source_result_position_reference,
        source_movement_event_identity=source_movement_event_identity,
        input_applicability=input_applicability,
        addressed_act_identity=addressed_act_identity,
        act_occurrence_identity=act_occurrence_identity,
        counts=counts,
    )


def _result_positions(measured: MeasuredByteInputs) -> list[dict[str, Any]]:
    source_subject = {
        "source_occurrence_references": [
            dict(reference) for reference in measured.source_material
        ],
    }
    source_content = {
        "source_material": list(measured.source_material),
        "completeness_boundary": {
            "identity": measured.completeness_boundary.identity
        },
    }
    results: list[dict[str, Any]] = [
        {
            "dimensions": {
                "position": 0,
                "content": source_content,
            },
            "result": "exact_source_material_set",
            "subject": source_subject,
        }
    ]

    def result_position(
        *,
        result: str,
        item: MeasuredByteCount,
        content: dict[str, Any],
        referenced_result_positions: list[int],
    ):
        subject = {"content": item.content}
        position = len(results)
        return {
            "dimensions": {
                "position": position,
                "content": content,
            },
            "result": result,
            "subject": subject,
            "referenced_result_positions": referenced_result_positions,
        }

    for item in measured.counts:
        count_content = {
            "input_count": len(measured.source_material),
            "occurrences_carrying": item.occurrences_carrying,
            "count": item.count,
        }
        count = result_position(
            result="count",
            item=item,
            content=count_content,
            referenced_result_positions=[0],
        )
        results.append(count)
        if item.count > 1:
            results.append(
                result_position(
                    result="recurrence",
                    item=item,
                    content={"recurrence_established": True},
                    referenced_result_positions=[count["dimensions"]["position"]],
                )
            )
    return results


def _byte_measurement_source_material(
    ledger: EventLedger,
    *,
    localities: tuple[str, ...],
    boundary: EventLedgerBoundary,
) -> tuple[dict[str, str], ...]:
    missing = [
        locality
        for locality in localities
        if not ledger.has_locality(locality, through=boundary)
    ]
    if missing:
        raise ByteMeasurementError(
            "declared source Localities are absent through the Measurement boundary: "
            + ", ".join(missing)
        )
    source_material = []
    seen_material = set()
    for locality in localities:
        for material_result in _exact_material_results(
            ledger, locality, through=boundary
        ):
            _material_result_bytes(ledger, material_result)
            if material_result.identity in seen_material:
                raise ByteMeasurementError(
                    "one material result occurrence cannot enter a byte Measurement twice"
                )
            seen_material.add(material_result.identity)
            source_material.append(
                {"material_result_occurrence_identity": material_result.identity}
            )
    if not source_material:
        raise ByteMeasurementError(
            "declared source Localities contain no exact material result with "
            "an exact Locality through the Measurement boundary"
        )
    return tuple(source_material)


def _byte_measurement_binding_reference(binding: Event) -> dict[str, Any]:
    return {
        "recorded_occurrence_identity": binding.identity,
        "book_clause_identity": binding.material["book_clause_identity"],
        "exact_act_identity": binding.material["exact_act_identity"],
        "subject_reference": deepcopy(binding.material["subject_reference"]),
    }


def _byte_measurement_binding_material(
    *,
    source_localities: tuple[str, ...],
    source_material: tuple[dict[str, str], ...],
    completeness_boundary_identity: str,
    through_event_occurrence_identity: str | None,
    exact_act_identity: str,
    act_occurrence_identity: str,
    measurement_result_identity: str,
) -> dict[str, Any]:
    return {
        "subject_reference": {
            "source_occurrence_references": [
                dict(reference) for reference in source_material
            ],
        },
        "exact_act_identity": exact_act_identity,
        "act_occurrence_identity": act_occurrence_identity,
        "measurement_result_identity": measurement_result_identity,
        "book_clause_identity": "01.Source.D",
        "source_localities": list(source_localities),
        "completeness_boundary_identity": completeness_boundary_identity,
        "through_event_occurrence_identity": through_event_occurrence_identity,
    }


def _require_current_byte_measurement_coordinates(
    ledger: EventLedger,
    *,
    recording_locality_identity: str,
    current_coordinates: dict[str, Any],
    required_binding_occurrence_identity: str | None = None,
) -> str | None:
    if type(current_coordinates) is not dict:
        raise ByteMeasurementError(
            "byte Measurement requires exact current Locality coordinates"
        )
    from seed_runtime.operator_current_coordinates import (
        read_operator_current_coordinates,
    )

    current = read_operator_current_coordinates(
        ledger, locality_identity=recording_locality_identity
    )
    bindings = current_coordinates.get("subject_to_act_binding_occurrences")
    boundary = current_coordinates.get("through_event_occurrence_identity")
    if (
        current_coordinates != current
        or current_coordinates.get("locality_identity")
        != recording_locality_identity
        or (boundary is not None and (type(boundary) is not str or not boundary))
        or (
            required_binding_occurrence_identity is not None
            and (
                type(bindings) is not dict
                or bindings.get(required_binding_occurrence_identity, object())
                is not None
            )
        )
    ):
        raise ByteMeasurementError(
            "byte Measurement requires exact current Locality coordinates"
        )
    return boundary


def _require_carried_byte_measurement_coordinates_at_current_boundary(
    ledger: EventLedger,
    *,
    recording_locality_identity: str,
    current_coordinates: dict[str, Any],
    required_binding_occurrence_identity: str | None = None,
) -> str:
    if type(current_coordinates) is not dict:
        raise ByteMeasurementError(
            "byte Measurement requires exact current Locality coordinates"
        )
    boundary = current_coordinates.get("through_event_occurrence_identity")
    bindings = current_coordinates.get("subject_to_act_binding_occurrences")
    if (
        current_coordinates.get("locality_identity")
        != recording_locality_identity
        or type(boundary) is not str
        or not boundary
        or (
            required_binding_occurrence_identity is not None
            and (
                type(bindings) is not dict
                or bindings.get(required_binding_occurrence_identity, object())
                is not None
            )
        )
    ):
        raise ByteMeasurementError(
            "byte Measurement requires exact current Locality coordinates"
        )
    event = ledger.get(boundary)
    locality_events = (
        ledger.list_locality(recording_locality_identity)
        if event is not None
        else ()
    )
    if (
        event is None
        or event.locality_identity != recording_locality_identity
        or ledger.integrity_of(boundary) == CORRUPTED
        or not locality_events
        or locality_events[-1].identity != boundary
    ):
        raise ByteMeasurementError(
            "byte Measurement requires exact current Locality coordinates"
        )
    return boundary


def _require_exact_byte_measurement_through_occurrence(
    ledger: EventLedger,
    *,
    source_localities: tuple[str, ...],
    recording_locality_identity: str,
    through_event_occurrence_identity: str,
) -> tuple[str, tuple[dict[str, str], ...]]:
    """Validate one earlier boundary carrying the exact source occurrences."""

    if (
        type(through_event_occurrence_identity) is not str
        or not through_event_occurrence_identity
    ):
        raise ByteMeasurementError(
            "byte Measurement requires one exact through-occurrence boundary"
        )
    boundary_event = ledger.get(through_event_occurrence_identity)
    try:
        boundary = ledger.append_boundary_through_occurrence(
            through_event_occurrence_identity
        )
        source_material = _byte_measurement_source_material(
            ledger,
            localities=source_localities,
            boundary=boundary,
        )
    except (TypeError, ValueError) as error:
        raise ByteMeasurementError(
            "byte Measurement requires one exact through-occurrence boundary"
        ) from error
    if (
        boundary_event is None
        or boundary_event.locality_identity != recording_locality_identity
        or ledger.integrity_of(boundary_event.identity) == CORRUPTED
    ):
        raise ByteMeasurementError(
            "byte Measurement requires one exact through-occurrence boundary"
        )
    return through_event_occurrence_identity, source_material


def _prepare_byte_measurement_subject_to_act_binding(
    ledger: EventLedger,
    *,
    source_localities: Iterable[str],
    recording_locality_identity: str,
) -> tuple[tuple[str, ...], EventLedgerBoundary, tuple[dict[str, str], ...]]:
    if (
        type(recording_locality_identity) is not str
        or not recording_locality_identity
    ):
        raise ByteMeasurementError(
            "byte Measurement recording requires an exact Locality"
        )
    localities = tuple(dict.fromkeys(source_localities))
    if (
        not localities
        or any(type(locality) is not str or not locality for locality in localities)
    ):
        raise ByteMeasurementError(
            "byte Measurement requires exact declared source Localities"
        )
    boundary = ledger.append_boundary()
    source_material = _byte_measurement_source_material(
        ledger, localities=localities, boundary=boundary
    )
    return localities, boundary, source_material


def _append_byte_measurement_subject_to_act_binding(
    ledger: EventLedger,
    *,
    source_localities: tuple[str, ...],
    source_material: tuple[dict[str, str], ...],
    completeness_boundary_identity: str,
    through_event_occurrence_identity: str | None,
    recording_locality_identity: str,
) -> Event:
    identities = {
        "exact_act_identity": ledger.mint_identity("byte_measurement_act"),
        "act_occurrence_identity": ledger.mint_identity(
            "byte_measurement_occurrence"
        ),
        "measurement_result_identity": ledger.mint_identity(
            "byte_measurement_result"
        ),
    }
    if len(set(identities.values())) != len(identities):
        raise ByteMeasurementError(
            "byte Measurement lifecycle identities collapsed"
        )
    return ledger.append(
        BYTE_MEASUREMENT_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
        _byte_measurement_binding_material(
            source_localities=source_localities,
            source_material=source_material,
            completeness_boundary_identity=completeness_boundary_identity,
            through_event_occurrence_identity=through_event_occurrence_identity,
            **identities,
        ),
        locality_identity=recording_locality_identity,
    )


def record_byte_measurement_subject_to_act_binding(
    ledger: EventLedger,
    *,
    source_localities: Iterable[str],
    recording_locality_identity: str,
    current_coordinates: dict[str, Any],
) -> Event:
    """Record one exact-byte Measurement subject-to-Act binding."""

    localities, boundary, source_material = (
        _prepare_byte_measurement_subject_to_act_binding(
            ledger,
            source_localities=source_localities,
            recording_locality_identity=recording_locality_identity,
        )
    )
    through_event_occurrence_identity = _require_current_byte_measurement_coordinates(
        ledger,
        recording_locality_identity=recording_locality_identity,
        current_coordinates=current_coordinates,
    )
    if ledger.append_boundary() != boundary:
        raise ByteMeasurementError(
            "byte Measurement current coordinates changed before binding recording"
        )
    return _append_byte_measurement_subject_to_act_binding(
        ledger,
        source_localities=localities,
        source_material=source_material,
        completeness_boundary_identity=boundary.identity,
        through_event_occurrence_identity=through_event_occurrence_identity,
        recording_locality_identity=recording_locality_identity,
    )


def _record_byte_measurement_subject_to_act_binding_from_current_coordinates(
    ledger: EventLedger,
    *,
    source_localities: Iterable[str],
    recording_locality_identity: str,
    current_coordinates: dict[str, Any],
) -> Event:
    localities, boundary, source_material = (
        _prepare_byte_measurement_subject_to_act_binding(
            ledger,
            source_localities=source_localities,
            recording_locality_identity=recording_locality_identity,
        )
    )
    through_event_occurrence_identity = (
        _require_carried_byte_measurement_coordinates_at_current_boundary(
            ledger,
            recording_locality_identity=recording_locality_identity,
            current_coordinates=current_coordinates,
        )
    )
    if ledger.append_boundary() != boundary:
        raise ByteMeasurementError(
            "byte Measurement current coordinates changed before binding recording"
        )
    return _append_byte_measurement_subject_to_act_binding(
        ledger,
        source_localities=localities,
        source_material=source_material,
        completeness_boundary_identity=boundary.identity,
        through_event_occurrence_identity=through_event_occurrence_identity,
        recording_locality_identity=recording_locality_identity,
    )


def _record_byte_measurement_subject_to_act_binding_from_through_event_occurrence(
    ledger: EventLedger,
    *,
    source_localities: Iterable[str],
    recording_locality_identity: str,
    through_event_occurrence_identity: str,
) -> Event:
    """Record one binding through an exact earlier occurrence."""

    localities = tuple(dict.fromkeys(source_localities))
    through_event_occurrence_identity, through_occurrence_source_material = (
        _require_exact_byte_measurement_through_occurrence(
            ledger,
            source_localities=localities,
            recording_locality_identity=recording_locality_identity,
            through_event_occurrence_identity=through_event_occurrence_identity,
        )
    )
    current_localities, boundary, current_source_material = (
        _prepare_byte_measurement_subject_to_act_binding(
            ledger,
            source_localities=localities,
            recording_locality_identity=recording_locality_identity,
        )
    )
    if (
        current_localities != localities
        or current_source_material != through_occurrence_source_material
    ):
        raise ByteMeasurementError(
            "byte Measurement source material changed after its through-occurrence boundary"
        )
    if ledger.append_boundary() != boundary:
        raise ByteMeasurementError(
            "byte Measurement current coordinates changed before binding recording"
        )
    through_occurrence_boundary = (
        ledger.append_boundary_through_occurrence(through_event_occurrence_identity)
    )
    return _append_byte_measurement_subject_to_act_binding(
        ledger,
        source_localities=localities,
        source_material=current_source_material,
        completeness_boundary_identity=through_occurrence_boundary.identity,
        through_event_occurrence_identity=through_event_occurrence_identity,
        recording_locality_identity=recording_locality_identity,
    )


def _read_byte_measurement_subject_to_act_binding(
    ledger: EventLedger,
    binding_event_identity: str,
    *,
    prior_coordinates: dict[str, Any] | None = None,
) -> tuple[Event, tuple[str, ...], EventLedgerBoundary, tuple[dict[str, str], ...]]:
    if type(binding_event_identity) is not str or not binding_event_identity:
        raise ByteMeasurementError(
            "byte Measurement requires one exact subject-to-Act binding"
        )
    binding = ledger.get(binding_event_identity)
    if (
        binding is None
        or binding.kind
        != BYTE_MEASUREMENT_SUBJECT_TO_ACT_BINDING_RECORDED_KIND
        or type(binding.locality_identity) is not str
        or not binding.locality_identity
        or ledger.integrity_of(binding.identity) == CORRUPTED
    ):
        raise ByteMeasurementError(
            "byte Measurement subject-to-Act binding is absent or corrupted"
        )
    material = binding.material
    identities = {
        coordinate: material.get(coordinate)
        for coordinate in (
            "exact_act_identity",
            "act_occurrence_identity",
            "measurement_result_identity",
        )
    }
    localities_value = material.get("source_localities")
    completeness_boundary_identity = material.get(
        "completeness_boundary_identity"
    )
    through_event_occurrence_identity = material.get("through_event_occurrence_identity")
    if (
        any(type(identity) is not str or not identity for identity in identities.values())
        or len(set(identities.values())) != len(identities)
        or type(localities_value) is not list
        or not localities_value
        or any(type(locality) is not str or not locality for locality in localities_value)
        or len(set(localities_value)) != len(localities_value)
        or type(completeness_boundary_identity) is not str
        or not completeness_boundary_identity
        or (
            through_event_occurrence_identity is not None
            and (
                type(through_event_occurrence_identity) is not str
                or not through_event_occurrence_identity
            )
        )
    ):
        raise ByteMeasurementError(
            "byte Measurement subject-to-Act binding carries malformed coordinates"
        )
    localities = tuple(localities_value)
    boundary = EventLedgerBoundary(completeness_boundary_identity)
    source_material = _byte_measurement_source_material(
        ledger, localities=localities, boundary=boundary
    )
    expected = _byte_measurement_binding_material(
        source_localities=localities,
        source_material=source_material,
        completeness_boundary_identity=completeness_boundary_identity,
        through_event_occurrence_identity=through_event_occurrence_identity,
        **identities,
    )
    if material != expected:
        raise ByteMeasurementError(
            "byte Measurement subject-to-Act binding coordinates are not exact"
        )
    if prior_coordinates is None:
        from seed_runtime.operator_current_coordinates import (
            read_operator_current_coordinates_through,
        )

        try:
            prior_coordinates = read_operator_current_coordinates_through(
                ledger,
                locality_identity=binding.locality_identity,
                through_event_occurrence_identity=through_event_occurrence_identity,
            )
        except (TypeError, ValueError) as error:
            raise ByteMeasurementError(
                "byte Measurement binding has no exact prior coordinates"
            ) from error
    carried_bindings = prior_coordinates.get(
        "subject_to_act_binding_occurrences"
    )
    prior_boundary_identity = prior_coordinates.get(
        "through_event_occurrence_identity"
    )
    boundary_is_exact = prior_boundary_identity == through_event_occurrence_identity
    binding_is_carried_later = bool(
        type(prior_boundary_identity) is str
        and prior_boundary_identity
        and type(carried_bindings) is dict
        and carried_bindings.get(binding.identity, object()) is None
    )
    recording_boundary_precedes_binding = bool(
        type(prior_boundary_identity) is str
        and prior_boundary_identity
        and prior_boundary_identity != through_event_occurrence_identity
        and not binding_is_carried_later
    )
    if (
        prior_coordinates.get("locality_identity") != binding.locality_identity
        or not (
            boundary_is_exact
            or binding_is_carried_later
            or recording_boundary_precedes_binding
        )
    ):
        raise ByteMeasurementError(
            "byte Measurement binding has no exact prior coordinates"
        )
    if boundary_is_exact:
        order = (binding.identity,)
        if through_event_occurrence_identity is not None:
            order = (through_event_occurrence_identity, binding.identity)
    elif prior_boundary_identity == binding.identity:
        order = (binding.identity,)
    elif recording_boundary_precedes_binding:
        order = (
            through_event_occurrence_identity,
            prior_boundary_identity,
            binding.identity,
        )
    else:
        order = (binding.identity, prior_boundary_identity)
        if through_event_occurrence_identity is not None:
            order = (
                through_event_occurrence_identity,
                binding.identity,
                prior_boundary_identity,
            )
    try:
        ledger.occurrences_in_append_order(
            order, locality_identity=binding.locality_identity
        )
    except ValueError as error:
        raise ByteMeasurementError(
            "byte Measurement binding order is false"
        ) from error
    return binding, localities, boundary, source_material


def get_byte_measurement_subject_to_act_binding(
    ledger: EventLedger, binding_event_identity: str
) -> Event:
    return _read_byte_measurement_subject_to_act_binding(
        ledger, binding_event_identity
    )[0]


def _byte_measurement_act_occurrence_material(
    binding: Event,
) -> dict[str, Any]:
    return {
        "addressed_act_identity": binding.material["exact_act_identity"],
        "act_occurrence_identity": binding.material[
            "act_occurrence_identity"
        ],
        "act": "declared exact-byte Measurement",
        "subject_to_act_binding_reference": (
            _byte_measurement_binding_reference(binding)
        ),
        "source_localities": list(binding.material["source_localities"]),
    }


def _append_byte_measurement_act_occurrence(
    ledger: EventLedger,
    *,
    binding: Event,
) -> Event:
    for prior_act in ledger.iter_locality_kind(
        binding.locality_identity,
        BYTE_MEASUREMENT_ACT_OCCURRENCE_EVENT,
    ):
        if (
            prior_act.material.get("subject_to_act_binding_reference")
            == _byte_measurement_binding_reference(binding)
            or prior_act.material.get("act_occurrence_identity")
            == binding.material["act_occurrence_identity"]
        ):
            raise ByteMeasurementError(
                "byte Measurement binding carries one Act"
            )
    return ledger.append(
        BYTE_MEASUREMENT_ACT_OCCURRENCE_EVENT,
        _byte_measurement_act_occurrence_material(binding),
        locality_identity=binding.locality_identity,
    )


def record_byte_measurement_act_occurrence(
    ledger: EventLedger,
    *,
    subject_to_act_binding_event_identity: str,
    current_coordinates: dict[str, Any],
) -> Event:
    """Record one exact byte Measurement Act occurrence from its binding."""

    binding, _localities, _boundary, _source_material = (
        _read_byte_measurement_subject_to_act_binding(
            ledger, subject_to_act_binding_event_identity
        )
    )
    _require_current_byte_measurement_coordinates(
        ledger,
        recording_locality_identity=binding.locality_identity,
        current_coordinates=current_coordinates,
        required_binding_occurrence_identity=binding.identity,
    )
    return _append_byte_measurement_act_occurrence(
        ledger,
        binding=binding,
    )


def _record_byte_measurement_act_occurrence_from_current_coordinates(
    ledger: EventLedger,
    *,
    subject_to_act_binding: Event,
    current_coordinates: dict[str, Any],
) -> Event:
    if (
        type(subject_to_act_binding) is not Event
        or subject_to_act_binding.kind
        != BYTE_MEASUREMENT_SUBJECT_TO_ACT_BINDING_RECORDED_KIND
        or ledger.integrity_of(subject_to_act_binding.identity) == CORRUPTED
    ):
        raise ByteMeasurementError(
            "byte Measurement requires its exact binding in current coordinates"
        )
    exact_binding, _localities, _boundary, _source_material = (
        _read_byte_measurement_subject_to_act_binding(
            ledger,
            subject_to_act_binding.identity,
            prior_coordinates=current_coordinates,
        )
    )
    if exact_binding != subject_to_act_binding:
        raise ByteMeasurementError(
            "byte Measurement requires its exact binding in current coordinates"
        )
    _require_carried_byte_measurement_coordinates_at_current_boundary(
        ledger,
        recording_locality_identity=subject_to_act_binding.locality_identity,
        current_coordinates=current_coordinates,
        required_binding_occurrence_identity=subject_to_act_binding.identity,
    )
    return _append_byte_measurement_act_occurrence(
        ledger,
        binding=subject_to_act_binding,
    )


def _measurement_of_act_occurrence(
    ledger: EventLedger,
    act_occurrence_event_identity: str,
    *,
    prior_coordinates: dict[str, Any] | None = None,
) -> tuple[Any, Event, MeasuredByteInputs]:
    event = ledger.get(act_occurrence_event_identity)
    if (
        event is None
        or event.kind != BYTE_MEASUREMENT_ACT_OCCURRENCE_EVENT
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise ByteMeasurementError(
            "byte Measurement result requires one exact Act occurrence"
        )
    material = event.material
    binding_reference = material.get("subject_to_act_binding_reference")
    if (
        type(binding_reference) is not dict
        or set(binding_reference)
            != {
                "recorded_occurrence_identity",
                "book_clause_identity",
                "exact_act_identity",
                "subject_reference",
            }
        or type(event.locality_identity) is not str
        or not event.locality_identity
    ):
        raise ByteMeasurementError(
            "byte Measurement Act occurrence carries malformed coordinates"
        )
    binding, localities, boundary, _source_material = (
        _read_byte_measurement_subject_to_act_binding(
            ledger,
            binding_reference.get("recorded_occurrence_identity"),
            prior_coordinates=prior_coordinates,
        )
    )
    measured = _measure_byte_counts_through(
        ledger,
        localities=localities,
        boundary=boundary,
    )
    expected = _byte_measurement_act_occurrence_material(binding)
    if (
        binding_reference
        != _byte_measurement_binding_reference(binding)
        or event.locality_identity != binding.locality_identity
        or material != expected
    ):
        raise ByteMeasurementError(
            "byte Measurement Act occurrence is not exact"
        )
    return event, binding, measured


def _require_byte_measurement_act_without_result(
    ledger: EventLedger, act_occurrence: Event
) -> None:
    for event in ledger.iter_locality_kind(
        act_occurrence.locality_identity,
        BYTE_MEASUREMENT_RECORDED_KIND,
    ):
        if (
            event.material.get("act_occurrence_event_identity")
            == act_occurrence.identity
        ):
            raise ByteMeasurementError(
                "byte Measurement Act occurrence has one result"
            )


def _record_byte_measurement_result_from_exact_inputs(
    ledger: EventLedger,
    *,
    act_occurrence: Event,
    binding: Event,
    measured: MeasuredByteInputs,
) -> Event:
    result_identity = binding.material["measurement_result_identity"]
    result_material = {
        "result_identity": result_identity,
        "dimensions": {
                "identity": "byte-count-measurement-occurrence",
                "content": (
                    "exact source material, byte count, and same content"
                ),
        },
        "exact_act": "declared exact-byte Measurement",
        "addressed_act_identity": act_occurrence.material[
            "addressed_act_identity"
        ],
        "act_occurrence_identity": act_occurrence.material[
            "act_occurrence_identity"
        ],
        "subject_to_act_binding_reference": (
            _byte_measurement_binding_reference(binding)
        ),
        "source_localities": list(measured.source_localities),
        "completeness_boundary": {
            "identity": measured.completeness_boundary.identity
        },
        "result_positions": _result_positions(measured),
    }
    return ledger.append(
        BYTE_MEASUREMENT_RECORDED_KIND,
        {
            **result_material,
            "act_occurrence_event_identity": act_occurrence.identity,
            "occurrence_preservation": BYTE_OCCURRENCE_PRESERVATION,
        },
        locality_identity=act_occurrence.locality_identity,
    )


def record_byte_measurement_result(
    ledger: EventLedger,
    *,
    act_occurrence_event_identity: str,
    current_coordinates: dict[str, Any] | None = None,
):
    """Record the result of one exact recorded byte Measurement Act."""

    supplied = ledger.get(act_occurrence_event_identity)
    if (
        supplied is None
        or supplied.kind != BYTE_MEASUREMENT_ACT_OCCURRENCE_EVENT
        or ledger.integrity_of(supplied.identity) == CORRUPTED
    ):
        raise ByteMeasurementError(
            "byte Measurement result requires one exact Act occurrence"
        )
    _require_byte_measurement_act_without_result(ledger, supplied)

    act_occurrence, binding, measured = (
        _measurement_of_act_occurrence(
            ledger,
            supplied.identity,
            prior_coordinates=current_coordinates,
        )
    )

    return _record_byte_measurement_result_from_exact_inputs(
        ledger,
        act_occurrence=act_occurrence,
        binding=binding,
        measured=measured,
    )


def _record_byte_measurement_result_from_current_coordinates(
    ledger: EventLedger,
    *,
    act_occurrence: Event,
    subject_to_act_binding: Event,
    current_coordinates: dict[str, Any],
) -> Event:
    if (
        type(act_occurrence) is not Event
        or type(subject_to_act_binding) is not Event
        or ledger.get(act_occurrence.identity)
        != act_occurrence
        or act_occurrence.kind
        != BYTE_MEASUREMENT_ACT_OCCURRENCE_EVENT
        or ledger.integrity_of(act_occurrence.identity) == CORRUPTED
        or ledger.append_boundary_through_occurrence(
            act_occurrence.identity
        )
        != ledger.append_boundary()
    ):
        raise ByteMeasurementError(
            "byte Measurement result requires exact lifecycle occurrences in current coordinates"
        )
    exact_act, exact_binding, measured = (
        _measurement_of_act_occurrence(
            ledger,
            act_occurrence.identity,
            prior_coordinates=current_coordinates,
        )
    )
    if (
        exact_act != act_occurrence
        or exact_binding != subject_to_act_binding
    ):
        raise ByteMeasurementError(
            "byte Measurement result requires exact lifecycle occurrences in current coordinates"
        )
    if (
        ledger.get(act_occurrence.identity) != act_occurrence
        or ledger.integrity_of(act_occurrence.identity) == CORRUPTED
        or ledger.append_boundary_through_occurrence(
            act_occurrence.identity
        )
        != ledger.append_boundary()
    ):
        raise ByteMeasurementError(
            "byte Measurement result requires its exact Act at the current append boundary"
        )
    return _record_byte_measurement_result_from_exact_inputs(
        ledger,
        act_occurrence=act_occurrence,
        binding=subject_to_act_binding,
        measured=measured,
    )


def _result_positions_of_recorded_byte_measurement(
    ledger: EventLedger,
    event_identity: str,
    *,
    prior_coordinates: dict[str, Any] | None = None,
) -> tuple[dict[str, Any], ...] | None:
    event = ledger.get(event_identity)
    if event is None:
        return None
    if event.kind != BYTE_MEASUREMENT_RECORDED_KIND:
        raise ByteMeasurementError(f"{event_identity} is not a byte Measurement occurrence")
    if ledger.integrity_of(event_identity) == CORRUPTED:
        raise ByteMeasurementError("a corrupted occurrence cannot return byte results")
    material = event.material
    if set(material) != BYTE_RESULT_COORDINATES | {
        "act_occurrence_identity",
        "act_occurrence_event_identity",
        "occurrence_preservation",
    }:
        raise ByteMeasurementError(
            f"{event_identity} does not carry the exact byte result and recording surfaces"
        )
    if (
        material.get("occurrence_preservation") != BYTE_OCCURRENCE_PRESERVATION
        or material.get("exact_act") != "declared exact-byte Measurement"
        or not isinstance(material.get("addressed_act_identity"), str)
        or not material["addressed_act_identity"]
        or not isinstance(material.get("act_occurrence_identity"), str)
        or not material["act_occurrence_identity"]
        or material["addressed_act_identity"] == material["act_occurrence_identity"]
        or material.get("dimensions")
        != {
                "identity": "byte-count-measurement-occurrence",
                "content": "exact source material, byte count, and same content",
        }
    ):
        raise ByteMeasurementError(
            f"{event_identity} does not preserve its exact Measurement result"
        )
    act_occurrence_event_identity = material.get("act_occurrence_event_identity")
    act_occurrence = ledger.get(act_occurrence_event_identity) if isinstance(act_occurrence_event_identity, str) else None
    expected_act_occurrence = {
        "addressed_act_identity": material["addressed_act_identity"],
        "act_occurrence_identity": material["act_occurrence_identity"],
        "act": "declared exact-byte Measurement",
        "subject_to_act_binding_reference": material[
            "subject_to_act_binding_reference"
        ],
        "source_localities": material["source_localities"],
    }
    if (
        act_occurrence is None
        or act_occurrence.kind != BYTE_MEASUREMENT_ACT_OCCURRENCE_EVENT
        or act_occurrence.locality_identity != event.locality_identity
        or ledger.integrity_of(act_occurrence.identity) == CORRUPTED
        or act_occurrence.material != expected_act_occurrence
    ):
        raise ByteMeasurementError(
            f"{event_identity} names no exact byte Measurement Act occurrence"
        )
    _validated_act, binding, measured = (
        _measurement_of_act_occurrence(
            ledger,
            act_occurrence.identity,
            prior_coordinates=prior_coordinates,
        )
    )
    try:
        ordered = ledger.occurrences_in_append_order(
            (act_occurrence.identity, event.identity),
            locality_identity=event.locality_identity,
        )
    except (TypeError, ValueError) as error:
        raise ByteMeasurementError(
            f"{event_identity} does not follow its exact byte Measurement Act"
        ) from error
    results = tuple(
        candidate
        for candidate in ledger.iter_locality_kind(
            event.locality_identity,
            BYTE_MEASUREMENT_RECORDED_KIND,
        )
        if candidate.material.get("act_occurrence_event_identity")
        == act_occurrence.identity
    )
    if (
        tuple(item.identity for item in ordered)
        != (act_occurrence.identity, event.identity)
        or len(results) != 1
        or results[0].identity != event.identity
    ):
        raise ByteMeasurementError(
            f"{event_identity} is not the single exact byte Measurement result"
        )
    boundary_value = material.get("completeness_boundary")
    localities_value = material.get("source_localities")
    if (
        not isinstance(boundary_value, dict)
        or set(boundary_value) != {"identity"}
        or not isinstance(boundary_value["identity"], str)
        or not isinstance(localities_value, list)
        or not localities_value
        or any(not isinstance(item, str) or not item for item in localities_value)
        or len(set(localities_value)) != len(localities_value)
    ):
        raise ByteMeasurementError(
            f"{event_identity} does not carry the exact byte Measurement boundary"
        )
    if (
        material.get("subject_to_act_binding_reference")
        != _byte_measurement_binding_reference(binding)
        or material.get("result_identity")
        != binding.material["measurement_result_identity"]
        or material.get("addressed_act_identity")
        != binding.material["exact_act_identity"]
        or material.get("act_occurrence_identity")
        != binding.material["act_occurrence_identity"]
        or measured.completeness_boundary.identity != boundary_value["identity"]
        or list(measured.source_localities) != localities_value
    ):
        raise ByteMeasurementError(
            f"{event_identity} does not establish its Seed-native Measurement boundary"
        )
    recorded_result_positions = material.get("result_positions")
    if type(recorded_result_positions) is not list:
        raise ByteMeasurementError(
            f"{event_identity} does not carry the results of its complete bounded source read"
        )
    try:
        expected = _result_positions(measured)
    except (KeyError, TypeError, ByteMeasurementError) as error:
        raise ByteMeasurementError(
            f"{event_identity} does not carry the results of its complete bounded source read"
        ) from error
    if recorded_result_positions != expected:
        raise ByteMeasurementError(
            f"{event_identity} does not carry the results of its complete bounded source read"
        )
    return tuple(deepcopy(result_position) for result_position in expected)


def result_positions_of_recorded_byte_measurement(
    ledger: EventLedger,
    event_identity: str,
    *,
    prior_coordinates: dict[str, Any] | None = None,
) -> tuple[dict[str, Any], ...] | None:
    """Read the exact byte results after replaying their bounded source read."""

    return _result_positions_of_recorded_byte_measurement(
        ledger,
        event_identity,
        prior_coordinates=prior_coordinates,
    )


def _byte_result_position(
    ledger: EventLedger,
    event_identity: str,
    result_position: int,
    *,
    prior_coordinates: dict[str, Any] | None = None,
) -> dict[str, Any] | None:
    """Resolve one exact result occurrence and result-local position."""

    result_positions = _result_positions_of_recorded_byte_measurement(
        ledger,
        event_identity,
        prior_coordinates=prior_coordinates,
    )
    if result_positions is None:
        return None
    addressed_content = next(
        (
            item
            for item in result_positions
            if item["dimensions"]["position"] == result_position
        ),
        None,
    )
    if addressed_content is None:
        return None
    return {
        "recorded_occurrence_identity": event_identity,
        "result_position": result_position,
        "locality_movement_event_identity": None,
    }


def _read_byte_result_position(
    ledger: EventLedger,
    source: dict[str, Any],
    *,
    prior_coordinates: dict[str, Any] | None = None,
) -> tuple[Event, dict[str, Any], tuple[str, ...]]:
    reference = _byte_result_position_reference(source)
    event = ledger.get(reference["recorded_occurrence_identity"])
    source_coordinates = (
        prior_coordinates
        if event is not None
        and prior_coordinates is not None
        and prior_coordinates.get("locality_identity") == event.locality_identity
        else None
    )
    result_positions = _result_positions_of_recorded_byte_measurement(
        ledger,
        reference["recorded_occurrence_identity"],
        prior_coordinates=source_coordinates,
    )
    result_position = next(
        (
            item
            for item in result_positions or ()
            if item["dimensions"]["position"] == reference["result_position"]
        ),
        None,
    )
    if event is None or result_position is None:
        raise ByteMeasurementError("byte result position is absent")
    return event, result_position, tuple(event.material["source_localities"])


def _pair_result_positions(measured: MeasuredBytePairInputs) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []

    def result_position(
        *,
        result: str,
        item: MeasuredBytePairCount,
        content: dict[str, Any],
        referenced_result_positions: list[int],
        referenced_result_position_references: list[dict[str, Any]],
    ) -> dict[str, Any]:
        subject = {"content": list(item.content)}
        position = len(results)
        return {
            "dimensions": {
                "position": position,
                "content": content,
            },
            "result": result,
            "subject": subject,
            "referenced_result_position_references": (
                referenced_result_position_references
            ),
            "referenced_result_positions": referenced_result_positions,
        }

    for item in measured.counts:
        count = result_position(
            result="count",
            item=item,
            content={
                "input_count": len(measured.source_material),
                "occurrences_carrying": item.occurrences_carrying,
                "count": item.count,
            },
            referenced_result_positions=[],
            referenced_result_position_references=[
                measured.source_result_position_reference
            ],
        )
        results.append(count)
        if item.count > 1:
            results.append(
                result_position(
                    result="recurrence",
                    item=item,
                    content={"recurrence_established": True},
                    referenced_result_positions=[count["dimensions"]["position"]],
                    referenced_result_position_references=[],
                )
            )
    return results


def _pair_subject_to_act_binding_reference(binding: Event) -> dict[str, Any]:
    return {
        "recorded_occurrence_identity": binding.identity,
        "book_clause_identity": binding.material["book_clause_identity"],
        "exact_act_identity": binding.material["exact_act_identity"],
        "subject_reference": deepcopy(binding.material["subject_reference"]),
    }


def _pair_binding_source_coordinates(
    *,
    source: dict[str, Any],
    source_localities: tuple[str, ...],
    content: dict[str, Any],
    recording_locality_identity: str,
    through_event_occurrence_identity: str,
) -> dict[str, Any]:
    return {
        "source_movement_event_identity": _byte_result_position_movement_identity(source),
        "source_localities": list(source_localities),
        "source_occurrence_references": list(content["source_material"]),
        "completeness_boundary_identity": content["completeness_boundary"][
            "identity"
        ],
        "through_event_occurrence_identity": through_event_occurrence_identity,
        "recording_locality_identity": recording_locality_identity,
    }


def _pair_applicability_binding_material(
    *,
    source: dict[str, Any],
    source_localities: tuple[str, ...],
    content: dict[str, Any],
    recording_locality_identity: str,
    through_event_occurrence_identity: str,
    exact_act_identity: str,
    applicability_act_occurrence_identity: str,
    applicability_result_identity: str,
    measurement_act_identity: str,
) -> dict[str, Any]:
    return {
        **_pair_binding_source_coordinates(
            source=source,
            source_localities=source_localities,
            content=content,
            recording_locality_identity=recording_locality_identity,
            through_event_occurrence_identity=through_event_occurrence_identity,
        ),
        "source_result_position_reference": _byte_result_position_reference(source),
        "subject_reference": {
            "input_result_position_reference": _byte_result_position_reference(source),
            "input_movement_event_identity": _byte_result_position_movement_identity(source),
            "addressed_act_identity": measurement_act_identity,
        },
        "exact_act_identity": exact_act_identity,
        "applicability_act_occurrence_identity": (
            applicability_act_occurrence_identity
        ),
        "applicability_result_identity": applicability_result_identity,
        "addressed_act_identity": measurement_act_identity,
        "book_clause_identity": "01.Current.E.1",
    }


def _pair_measurement_binding_material(
    *,
    source: dict[str, Any],
    source_localities: tuple[str, ...],
    content: dict[str, Any],
    recording_locality_identity: str,
    through_event_occurrence_identity: str,
    exact_act_identity: str,
    measurement_act_occurrence_identity: str,
    measurement_result_identity: str,
) -> dict[str, Any]:
    return {
        **_pair_binding_source_coordinates(
            source=source,
            source_localities=source_localities,
            content=content,
            recording_locality_identity=recording_locality_identity,
            through_event_occurrence_identity=through_event_occurrence_identity,
        ),
        "subject_reference": _byte_result_position_reference(source),
        "exact_act_identity": exact_act_identity,
        "measurement_act_occurrence_identity": measurement_act_occurrence_identity,
        "measurement_result_identity": measurement_result_identity,
        "book_clause_identity": "01.Source.D",
    }


def _pair_binding_source_reference(binding: Event) -> Any:
    if binding.kind == BYTE_PAIR_MEASUREMENT_SUBJECT_TO_ACT_BINDING_RECORDED_KIND:
        return binding.material.get("subject_reference")
    return binding.material.get("source_result_position_reference")


def _require_exact_pair_subject_to_act_binding_event(
    ledger: EventLedger,
    binding: Event,
    source: dict[str, Any],
    *,
    prior_coordinates: dict[str, Any] | None = None,
) -> None:
    """Validate one recorded subject-to-Act binding against its exact source."""

    if (
        type(binding) is not Event
        or type(source) is not dict
        or ledger.get(binding.identity) != binding
        or binding.kind not in {
            BYTE_PAIR_APPLICABILITY_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
            BYTE_PAIR_MEASUREMENT_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
        }
        or binding.locality_identity is None
        or ledger.integrity_of(binding.identity) == CORRUPTED
    ):
        raise ByteMeasurementError(
            "byte-position-pair subject-to-Act binding is not exact"
        )
    material = binding.material
    identity_keys = (
        (
            "exact_act_identity",
            "applicability_act_occurrence_identity",
            "applicability_result_identity",
            "addressed_act_identity",
        )
        if binding.kind == BYTE_PAIR_APPLICABILITY_SUBJECT_TO_ACT_BINDING_RECORDED_KIND
        else (
            "exact_act_identity",
            "measurement_act_occurrence_identity",
            "measurement_result_identity",
        )
    )
    identities = {key: material.get(key) for key in identity_keys}
    boundary = material.get("through_event_occurrence_identity")
    _source_event, source_material, source_localities = _read_byte_result_position(
        ledger,
        source,
        prior_coordinates=prior_coordinates,
    )
    common = dict(
        source=source,
        source_localities=source_localities,
        content=source_material["dimensions"]["content"],
        recording_locality_identity=binding.locality_identity,
        through_event_occurrence_identity=boundary,
    )
    if binding.kind == BYTE_PAIR_APPLICABILITY_SUBJECT_TO_ACT_BINDING_RECORDED_KIND:
        exact_material = _pair_applicability_binding_material(
            **common,
            exact_act_identity=identities["exact_act_identity"],
            applicability_act_occurrence_identity=identities[
                "applicability_act_occurrence_identity"
            ],
            applicability_result_identity=identities[
                "applicability_result_identity"
            ],
            measurement_act_identity=identities["addressed_act_identity"],
        )
    else:
        exact_material = _pair_measurement_binding_material(
            **common,
            exact_act_identity=identities["exact_act_identity"],
            measurement_act_occurrence_identity=identities[
                "measurement_act_occurrence_identity"
            ],
            measurement_result_identity=identities["measurement_result_identity"],
        )
    if (
        _byte_result_position_reference(source) != _pair_binding_source_reference(binding)
        or _byte_result_position_movement_identity(source)
        != material.get("source_movement_event_identity")
        or type(boundary) is not str
        or not boundary
        or any(type(value) is not str or not value for value in identities.values())
        or len(set(identities.values())) != len(identities)
        or material != exact_material
    ):
        raise ByteMeasurementError(
            "byte-position-pair subject-to-Act binding coordinates are not exact"
        )


def _pair_source_is_carried(
    source: dict[str, Any],
    current_coordinates: dict[str, Any],
    *,
    binding_identity: str | None = None,
) -> bool:
    bindings = current_coordinates.get("subject_to_act_binding_occurrences")
    if binding_identity is not None:
        return (
            type(bindings) is dict
            and bindings.get(binding_identity, object()) is None
        )
    movement_identity = _byte_result_position_movement_identity(source)
    if movement_identity is not None:
        movements = current_coordinates.get(
            "result_position_locality_movement_occurrences"
        )
        return (
            type(movements) is dict
            and movement_identity in movements
        )
    carried = current_coordinates.get("measurement_occurrences")
    return (
        type(carried) is dict
        and source["recorded_occurrence_identity"] in carried
    )


def _require_carried_pair_measurement_at_current_append_boundary(
    ledger: EventLedger,
    *,
    source: dict[str, Any],
    recording_locality_identity: str,
    current_coordinates: dict[str, Any],
    required_binding_identity: str | None = None,
    required_applicability_identity: str | None = None,
) -> str:
    boundary = current_coordinates.get("through_event_occurrence_identity")
    bindings = current_coordinates.get("subject_to_act_binding_occurrences")
    applicability = current_coordinates.get("applicability_result_occurrences")
    event = ledger.get(boundary) if type(boundary) is str else None
    if (
        current_coordinates.get("locality_identity") != recording_locality_identity
        or type(boundary) is not str
        or not boundary
        or event is None
        or event.locality_identity != recording_locality_identity
        or ledger.integrity_of(boundary) == CORRUPTED
        or ledger.append_boundary_through_occurrence(boundary)
        != ledger.append_boundary()
        or not _pair_source_is_carried(
            source,
            current_coordinates,
            binding_identity=required_binding_identity,
        )
        or (
            required_binding_identity is not None
            and (
                type(bindings) is not dict
                or bindings.get(required_binding_identity, object()) is not None
            )
        )
        or (
            required_applicability_identity is not None
            and (
                type(applicability) is not dict
                or applicability.get(required_applicability_identity, object())
                is not None
            )
        )
    ):
        raise ByteMeasurementError(
            "byte-position-pair Measurement requires exact carried coordinates at the current append boundary"
        )
    return boundary


def _new_pair_lifecycle_identities(ledger: EventLedger) -> dict[str, str]:
    identities = {
        "applicability_act_identity": ledger.mint_identity("byte_pair_applicability_act"),
        "applicability_act_occurrence_identity": ledger.mint_identity(
            "byte_pair_applicability_occurrence"
        ),
        "applicability_result_identity": ledger.mint_identity(
            "byte_pair_applicability_result"
        ),
        "measurement_act_identity": ledger.mint_identity(
            "byte_position_pair_measurement_act"
        ),
        "measurement_act_occurrence_identity": ledger.mint_identity(
            "byte_position_pair_measurement_occurrence"
        ),
        "measurement_result_identity": ledger.mint_identity(
            "byte_position_pair_measurement_result"
        ),
    }
    if len(set(identities.values())) != len(identities):
        raise ByteMeasurementError(
            "byte-position-pair Measurement lifecycle identities collapsed"
        )
    return identities


def _new_pair_measurement_identities_without_applicability(
    ledger: EventLedger,
) -> dict[str, str]:
    identities = {
        "measurement_act_identity": ledger.mint_identity(
            "byte_position_pair_measurement_act"
        ),
        "measurement_act_occurrence_identity": ledger.mint_identity(
            "byte_position_pair_measurement_occurrence"
        ),
        "measurement_result_identity": ledger.mint_identity(
            "byte_position_pair_measurement_result"
        ),
    }
    if len(set(identities.values())) != 3:
        raise ByteMeasurementError(
            "byte-position-pair Measurement identities collapsed"
        )
    return identities


def _append_pair_applicability_binding(
    ledger: EventLedger,
    *,
    source: dict[str, Any],
    source_localities: tuple[str, ...],
    content: dict[str, Any],
    recording_locality_identity: str,
    through_event_occurrence_identity: str,
    identities: dict[str, str],
) -> Event:
    return ledger.append(
        BYTE_PAIR_APPLICABILITY_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
        _pair_applicability_binding_material(
            source=source,
            source_localities=source_localities,
            content=content,
            recording_locality_identity=recording_locality_identity,
            through_event_occurrence_identity=through_event_occurrence_identity,
            exact_act_identity=identities["applicability_act_identity"],
            applicability_act_occurrence_identity=identities[
                "applicability_act_occurrence_identity"
            ],
            applicability_result_identity=identities["applicability_result_identity"],
            measurement_act_identity=identities["measurement_act_identity"],
        ),
        locality_identity=recording_locality_identity,
    )


def _append_pair_measurement_binding(
    ledger: EventLedger,
    *,
    source: dict[str, Any],
    source_localities: tuple[str, ...],
    content: dict[str, Any],
    recording_locality_identity: str,
    through_event_occurrence_identity: str,
    identities: dict[str, str],
) -> Event:
    return ledger.append(
        BYTE_PAIR_MEASUREMENT_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
        _pair_measurement_binding_material(
            source=source,
            source_localities=source_localities,
            content=content,
            recording_locality_identity=recording_locality_identity,
            through_event_occurrence_identity=through_event_occurrence_identity,
            exact_act_identity=identities["measurement_act_identity"],
            measurement_act_occurrence_identity=identities[
                "measurement_act_occurrence_identity"
            ],
            measurement_result_identity=identities["measurement_result_identity"],
        ),
        locality_identity=recording_locality_identity,
    )


def _prior_coordinates_for_pair_subject_to_act_binding(
    ledger: EventLedger,
    *,
    binding: Event,
    boundary: str,
) -> dict[str, Any]:
    from seed_runtime.operator_current_coordinates import (
        read_operator_current_coordinates_through,
    )

    try:
        return read_operator_current_coordinates_through(
            ledger,
            locality_identity=binding.locality_identity,
            through_event_occurrence_identity=boundary,
        )
    except (TypeError, ValueError) as error:
        raise ByteMeasurementError(
            "byte-position-pair subject-to-Act binding has no exact prior coordinates"
        ) from error


def _read_pair_subject_to_act_binding(
    ledger: EventLedger,
    binding_event_identity: str,
    *,
    binding_kind: str,
    prior_coordinates: dict[str, Any] | None = None,
) -> tuple[Event, dict[str, Any], tuple[str, ...], dict[str, Any]]:
    binding = ledger.get(binding_event_identity)
    if (
        binding is None
        or binding.kind != binding_kind
        or binding.locality_identity is None
        or ledger.integrity_of(binding.identity) == CORRUPTED
    ):
        raise ByteMeasurementError(
            "byte-position-pair subject-to-Act binding is absent or corrupted"
        )
    material = binding.material
    reference = _pair_binding_source_reference(binding)
    movement_identity = material.get("source_movement_event_identity")
    boundary = material.get("through_event_occurrence_identity")
    if type(boundary) is not str or not boundary:
        raise ByteMeasurementError(
            "byte-position-pair Measurement binding carries no through-occurrence boundary"
        )
    if movement_identity is None:
        if prior_coordinates is None:
            prior_coordinates = _prior_coordinates_for_pair_subject_to_act_binding(
                ledger, binding=binding, boundary=boundary
            )
        source = (
            _byte_result_position(
                ledger,
                reference.get("recorded_occurrence_identity"),
                reference.get("result_position"),
                prior_coordinates=prior_coordinates,
            )
            if type(reference) is dict
            else None
        )
    elif type(movement_identity) is str and movement_identity:
        source = _validate_moved_result_position(
            ledger,
            movement_identity,
            prior_destination_coordinates=coordinates,
        )
    else:
        source = None
    if (
        source is None
        or _byte_result_position_reference(source) != reference
        or _byte_result_position_movement_identity(source) != movement_identity
    ):
        raise ByteMeasurementError(
            "byte-position-pair subject-to-Act binding carries no exact source"
        )
    _source_event, source_material, source_localities = _read_byte_result_position(
        ledger, source, prior_coordinates=prior_coordinates
    )
    content = source_material["dimensions"]["content"]
    _require_exact_pair_subject_to_act_binding_event(
        ledger,
        binding,
        source,
        prior_coordinates=prior_coordinates,
    )
    if prior_coordinates is None:
        prior_coordinates = _prior_coordinates_for_pair_subject_to_act_binding(
            ledger, binding=binding, boundary=boundary
        )
    through_occurrence = prior_coordinates.get("through_event_occurrence_identity")
    bindings = prior_coordinates.get("subject_to_act_binding_occurrences")
    boundary_is_exact = through_occurrence == boundary
    binding_is_carried = bool(
        type(bindings) is dict
        and bindings.get(binding.identity, object()) is None
    )
    if (
        prior_coordinates.get("locality_identity") != binding.locality_identity
        or not _pair_source_is_carried(
            source,
            prior_coordinates,
            binding_identity=(binding.identity if binding_is_carried else None),
        )
        or not (boundary_is_exact or binding_is_carried)
    ):
        raise ByteMeasurementError(
            "byte-position-pair subject-to-Act binding has no exact prior coordinates"
        )
    order = (boundary, binding.identity)
    if binding_is_carried and through_occurrence != binding.identity:
        order = (*order, through_occurrence)
    try:
        ledger.occurrences_in_append_order(
            tuple(dict.fromkeys(order)),
            locality_identity=binding.locality_identity,
        )
    except ValueError as error:
        raise ByteMeasurementError(
            "byte-position-pair subject-to-Act binding order is false"
        ) from error
    return binding, source, source_localities, content


def _read_pair_measurement_subject_to_act_binding(
    ledger: EventLedger,
    binding_event_identity: str,
    *,
    prior_coordinates: dict[str, Any] | None = None,
) -> tuple[Event, dict[str, Any], tuple[str, ...], dict[str, Any]]:
    return _read_pair_subject_to_act_binding(
        ledger,
        binding_event_identity,
        binding_kind=BYTE_PAIR_MEASUREMENT_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
        prior_coordinates=prior_coordinates,
    )


def _read_pair_applicability_subject_to_act_binding(
    ledger: EventLedger,
    binding_event_identity: str,
    *,
    prior_coordinates: dict[str, Any] | None = None,
) -> tuple[Event, dict[str, Any], tuple[str, ...], dict[str, Any]]:
    return _read_pair_subject_to_act_binding(
        ledger,
        binding_event_identity,
        binding_kind=BYTE_PAIR_APPLICABILITY_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
        prior_coordinates=prior_coordinates,
    )


def get_byte_position_pair_measurement_subject_to_act_binding(
    ledger: EventLedger, binding_event_identity: str
) -> Event:
    return _read_pair_measurement_subject_to_act_binding(
        ledger, binding_event_identity
    )[0]


def _pair_applicability_act_material(
    applicability_binding: Event, source: dict[str, Any]
) -> dict[str, Any]:
    return {
        "applicability_act_identity": applicability_binding.material[
            "exact_act_identity"
        ],
        "applicability_act_occurrence_identity": applicability_binding.material[
            "applicability_act_occurrence_identity"
        ],
        "act": "input Applicability",
        "subject_to_act_binding_reference": (
            _pair_subject_to_act_binding_reference(applicability_binding)
        ),
        "input_result_position_reference": _byte_result_position_reference(source),
        "input_movement_event_identity": _byte_result_position_movement_identity(source),
        "addressed_act_identity": applicability_binding.material[
            "addressed_act_identity"
        ],
    }


def _require_exact_pair_applicability_act_event(
    ledger: EventLedger,
    event: Event,
    *,
    binding: Event,
    source: dict[str, Any],
    prior_coordinates: dict[str, Any] | None = None,
) -> None:
    _require_exact_pair_subject_to_act_binding_event(
        ledger,
        binding,
        source,
        prior_coordinates=prior_coordinates,
    )
    if (
        type(event) is not Event
        or ledger.get(event.identity) != event
        or event.kind != BYTE_PAIR_APPLICABILITY_ACT_OCCURRENCE_EVENT
        or event.locality_identity != binding.locality_identity
        or ledger.integrity_of(event.identity) == CORRUPTED
        or event.material != _pair_applicability_act_material(binding, source)
    ):
        raise ByteMeasurementError("pair Applicability Act occurrence is not exact")


def _record_pair_input_applicability_act_from_carried_binding(
    ledger: EventLedger,
    *,
    binding: Event,
    source: dict[str, Any],
    current_coordinates: dict[str, Any],
) -> Event:
    _require_exact_pair_subject_to_act_binding_event(
        ledger,
        binding,
        source,
        prior_coordinates=current_coordinates,
    )
    _require_carried_pair_measurement_at_current_append_boundary(
        ledger,
        source=source,
        recording_locality_identity=binding.locality_identity,
        current_coordinates=current_coordinates,
        required_binding_identity=binding.identity,
    )
    return ledger.append(
        BYTE_PAIR_APPLICABILITY_ACT_OCCURRENCE_EVENT,
        _pair_applicability_act_material(binding, source),
        locality_identity=binding.locality_identity,
    )


def _pair_applicability_result_material(
    binding: Event,
    source: dict[str, Any],
    applicability_result: dict[str, Any],
) -> dict[str, Any]:
    return {
        "result_identity": binding.material["applicability_result_identity"],
        "dimensions": {
            "identity": applicability_result["dimensions"]["identity"],
            "content": "exact subject-to-Act binding Applicability",
            "applicability": applicability_result["dimensions"]["applicability"],
        },
        "exact_act": "input Applicability",
        "subject_to_act_binding_reference": (
            _pair_subject_to_act_binding_reference(binding)
        ),
        "applicability_act_identity": applicability_result["applicability_act_identity"],
        "applicability_act_occurrence_identity": applicability_result[
            "applicability_act_occurrence_identity"
        ],
        "addressed_act_identity": applicability_result["addressed_act_identity"],
        "input_result_position_reference": _byte_result_position_reference(source),
        "input_movement_event_identity": _byte_result_position_movement_identity(source),
        "applicability": applicability_result,
    }


def _require_exact_pair_applicability_result_event(
    ledger: EventLedger,
    event: Event,
    *,
    binding: Event,
    source: dict[str, Any],
    applicability_act_occurrence: Event,
    prior_coordinates: dict[str, Any] | None = None,
) -> dict[str, Any]:
    _require_exact_pair_applicability_act_event(
        ledger,
        applicability_act_occurrence,
        binding=binding,
        source=source,
        prior_coordinates=prior_coordinates,
    )
    expected_applicability = _pair_input_applicability_from_exact_source(
        source,
        binding=binding,
        measurement_locality_identity=binding.locality_identity,
    )
    expected_material = {
        **_pair_applicability_result_material(
            binding, source, expected_applicability
        ),
        "act_occurrence_event_identity": applicability_act_occurrence.identity,
    }
    try:
        ordered = ledger.occurrences_in_append_order(
            (applicability_act_occurrence.identity, event.identity),
            locality_identity=event.locality_identity,
        )
    except (TypeError, ValueError) as error:
        raise ByteMeasurementError(
            "pair Applicability result does not follow its Act"
        ) from error
    results = tuple(
        candidate
        for candidate in ledger.iter_locality_kind(
            event.locality_identity,
            BYTE_PAIR_APPLICABILITY_RECORDED_KIND,
        )
        if candidate.material.get("act_occurrence_event_identity")
        == applicability_act_occurrence.identity
    )
    if (
        type(event) is not Event
        or ledger.get(event.identity) != event
        or event.kind != BYTE_PAIR_APPLICABILITY_RECORDED_KIND
        or event.locality_identity != binding.locality_identity
        or ledger.integrity_of(event.identity) == CORRUPTED
        or event.material != expected_material
        or tuple(item.identity for item in ordered)
        != (applicability_act_occurrence.identity, event.identity)
        or len(results) != 1
        or results[0].identity != event.identity
    ):
        raise ByteMeasurementError("pair Applicability result is not exact")
    return expected_applicability


def _record_pair_input_applicability_result_from_carried_act(
    ledger: EventLedger,
    *,
    binding: Event,
    source: dict[str, Any],
    applicability_act_occurrence: Event,
    applicability_result: dict[str, Any],
    current_coordinates: dict[str, Any],
) -> Event:
    _require_exact_pair_applicability_act_event(
        ledger,
        applicability_act_occurrence,
        binding=binding,
        source=source,
        prior_coordinates=current_coordinates,
    )
    expected_applicability = _pair_input_applicability_from_exact_source(
        source,
        binding=binding,
        measurement_locality_identity=binding.locality_identity,
    )
    if (
        applicability_result != expected_applicability
        or ledger.append_boundary_through_occurrence(
            applicability_act_occurrence.identity
        )
        != ledger.append_boundary()
    ):
        raise ByteMeasurementError(
            "pair Applicability result requires its exact Act at the current append boundary"
        )
    recorded_material = {
        **_pair_applicability_result_material(
            binding, source, applicability_result
        ),
        "act_occurrence_event_identity": applicability_act_occurrence.identity,
    }
    return ledger.append(
        BYTE_PAIR_APPLICABILITY_RECORDED_KIND,
        recorded_material,
        locality_identity=binding.locality_identity,
    )


def _read_pair_applicability_act_occurrence(
    ledger: EventLedger,
    event_identity: str,
    *,
    prior_coordinates: dict[str, Any] | None = None,
) -> tuple[Event, Event, dict[str, Any]]:
    event = ledger.get(event_identity)
    if (
        event is None
        or event.kind != BYTE_PAIR_APPLICABILITY_ACT_OCCURRENCE_EVENT
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise ByteMeasurementError(
            "pair Applicability Act occurrence is absent or corrupted"
        )
    reference = event.material.get("subject_to_act_binding_reference")
    binding, source, _source_localities, _content = (
        _read_pair_applicability_subject_to_act_binding(
            ledger,
            reference.get("recorded_occurrence_identity")
            if type(reference) is dict
            else None,
            prior_coordinates=prior_coordinates,
        )
    )
    if (
        reference != _pair_subject_to_act_binding_reference(binding)
        or event.locality_identity != binding.locality_identity
        or event.material != _pair_applicability_act_material(binding, source)
    ):
        raise ByteMeasurementError("pair Applicability Act occurrence is not exact")
    try:
        ledger.occurrences_in_append_order(
            (binding.identity, event.identity),
            locality_identity=binding.locality_identity,
        )
    except ValueError as error:
        raise ByteMeasurementError(
            "pair Applicability Act does not follow its binding"
        ) from error
    return event, binding, source


def _read_recorded_pair_input_applicability(
    ledger: EventLedger,
    event_identity: str,
    *,
    prior_coordinates: dict[str, Any] | None = None,
) -> dict[str, Any] | None:
    """Read one historical input Applicability result without redetermining it."""

    event = ledger.get(event_identity)
    if event is None:
        return None
    if event.kind != BYTE_PAIR_APPLICABILITY_RECORDED_KIND:
        raise ByteMeasurementError(f"{event_identity} is not pair-input Applicability")
    if ledger.integrity_of(event.identity) == CORRUPTED:
        raise ByteMeasurementError("corrupted Applicability cannot be read")
    material = event.material
    if set(material) != BYTE_PAIR_APPLICABILITY_RESULT_COORDINATES | {
        "act_occurrence_event_identity",
    }:
        raise ByteMeasurementError(
            f"{event_identity} does not carry the exact Applicability result surface"
        )
    binding_reference = material.get("subject_to_act_binding_reference")
    binding, source, _source_localities, _content = (
        _read_pair_applicability_subject_to_act_binding(
            ledger,
            binding_reference.get("recorded_occurrence_identity")
            if type(binding_reference) is dict
            else None,
            prior_coordinates=prior_coordinates,
        )
    )
    act_occurrence = ledger.get(material.get("act_occurrence_event_identity"))
    if (
        binding_reference
        != _pair_subject_to_act_binding_reference(binding)
        or event.locality_identity != binding.locality_identity
        or material.get("result_identity")
        != binding.material["applicability_result_identity"]
        or act_occurrence is None
    ):
        raise ByteMeasurementError(
            f"{event_identity} carries no exact pair Measurement binding"
        )
    applicability = _require_exact_pair_applicability_result_event(
        ledger,
        event,
        binding=binding,
        source=source,
        applicability_act_occurrence=act_occurrence,
        prior_coordinates=prior_coordinates,
    )
    return deepcopy(applicability)


def get_recorded_pair_input_applicability(
    ledger: EventLedger, event_identity: str
) -> dict[str, Any] | None:
    return _read_recorded_pair_input_applicability(
        ledger, event_identity
    )


def _pair_applicability_binding_of_result(
    ledger: EventLedger,
    applicability_event: Event,
    *,
    source: dict[str, Any],
    prior_coordinates: dict[str, Any] | None = None,
) -> Event:
    reference = applicability_event.material.get("subject_to_act_binding_reference")
    binding, applicability_source, _source_localities, _content = (
        _read_pair_applicability_subject_to_act_binding(
            ledger,
            reference.get("recorded_occurrence_identity")
            if type(reference) is dict
            else None,
            prior_coordinates=prior_coordinates,
        )
    )
    if (
        reference != _pair_subject_to_act_binding_reference(binding)
        or _byte_result_position_reference(applicability_source)
        != _byte_result_position_reference(source)
    ):
        raise ByteMeasurementError(
            "pair Applicability result addresses another subject-to-Act binding"
        )
    return binding


def _pair_measurement_act_material(
    binding: Event,
    source: dict[str, Any],
    applicability_event: Event,
) -> dict[str, Any]:
    return {
        "addressed_act_identity": binding.material["exact_act_identity"],
        "act_occurrence_identity": binding.material[
            "measurement_act_occurrence_identity"
        ],
        "act": "declared byte-position-pair Measurement",
        "subject_to_act_binding_reference": (
            _pair_subject_to_act_binding_reference(binding)
        ),
        "result_boundary": BYTE_PAIR_RESULT_BOUNDARY,
        "input_applicability_identity": applicability_event.material["dimensions"][
            "identity"
        ],
        "input_applicability_event_identity": applicability_event.identity,
        "input_result_position_reference": _byte_result_position_reference(source),
    }


def _require_exact_pair_measurement_act_event(
    ledger: EventLedger,
    event: Event,
    *,
    binding: Event,
    applicability_binding: Event,
    source: dict[str, Any],
    applicability_event: Event,
    applicability_act_occurrence: Event,
    prior_coordinates: dict[str, Any] | None = None,
) -> None:
    _require_exact_pair_applicability_result_event(
        ledger,
        applicability_event,
        binding=applicability_binding,
        source=source,
        applicability_act_occurrence=applicability_act_occurrence,
        prior_coordinates=prior_coordinates,
    )
    if (
        type(event) is not Event
        or ledger.get(event.identity) != event
        or event.kind != BYTE_PAIR_MEASUREMENT_ACT_OCCURRENCE_EVENT
        or event.locality_identity != binding.locality_identity
        or ledger.integrity_of(event.identity) == CORRUPTED
        or event.material
        != _pair_measurement_act_material(binding, source, applicability_event)
    ):
        raise ByteMeasurementError("pair Measurement Act occurrence is not exact")


def _record_pair_measurement_act_from_carried_applicability(
    ledger: EventLedger,
    *,
    binding: Event,
    source: dict[str, Any],
    applicability_event: Event,
    current_coordinates: dict[str, Any],
) -> Event:
    applicability_act_occurrence = ledger.get(
        applicability_event.material.get("act_occurrence_event_identity")
    )
    if (
        applicability_act_occurrence is None
        or applicability_act_occurrence.kind
        != BYTE_PAIR_APPLICABILITY_ACT_OCCURRENCE_EVENT
    ):
        raise ByteMeasurementError(
            "pair Measurement Act requires exact recorded binding and Applicability"
        )
    applicability_reference = applicability_event.material.get(
        "subject_to_act_binding_reference"
    )
    applicability_binding, applicability_source, _source_localities, _content = (
        _read_pair_applicability_subject_to_act_binding(
            ledger,
            applicability_reference.get("recorded_occurrence_identity")
            if type(applicability_reference) is dict
            else None,
            prior_coordinates=current_coordinates,
        )
    )
    if _byte_result_position_reference(
        applicability_source
    ) != _byte_result_position_reference(source):
        raise ByteMeasurementError(
            "pair Measurement Act Applicability addresses another source"
        )
    _require_exact_pair_applicability_result_event(
        ledger,
        applicability_event,
        binding=applicability_binding,
        source=source,
        applicability_act_occurrence=applicability_act_occurrence,
        prior_coordinates=current_coordinates,
    )
    _require_carried_pair_measurement_at_current_append_boundary(
        ledger,
        source=source,
        recording_locality_identity=binding.locality_identity,
        current_coordinates=current_coordinates,
        required_binding_identity=binding.identity,
        required_applicability_identity=applicability_event.identity,
    )
    if (
        current_coordinates["through_event_occurrence_identity"]
        != applicability_event.identity
        or applicability_event.material["dimensions"]["applicability"] != "applicable"
    ):
        raise ByteMeasurementError(
            "pair Measurement Act requires exact applicable coordinates at the current append boundary"
        )
    return ledger.append(
        BYTE_PAIR_MEASUREMENT_ACT_OCCURRENCE_EVENT,
        _pair_measurement_act_material(binding, source, applicability_event),
        locality_identity=binding.locality_identity,
    )


def _read_pair_measurement_act_occurrence(
    ledger: EventLedger,
    event_identity: str,
    *,
    prior_coordinates: dict[str, Any] | None = None,
) -> tuple[Event, Event | None, dict[str, Any], Event | None]:
    event = ledger.get(event_identity)
    if (
        event is None
        or event.kind != BYTE_PAIR_MEASUREMENT_ACT_OCCURRENCE_EVENT
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise ByteMeasurementError(
            "pair Measurement Act occurrence is absent or corrupted"
        )
    if "subject_to_act_binding_reference" not in event.material:
        source, _source_localities, _content = _pair_source_from_act_without_applicability(
            ledger, event, prior_coordinates=prior_coordinates
        )
        return event, None, source, None
    reference = event.material.get("subject_to_act_binding_reference")
    binding, source, _source_localities, _content = (
        _read_pair_measurement_subject_to_act_binding(
            ledger,
            reference.get("recorded_occurrence_identity")
            if type(reference) is dict
            else None,
            prior_coordinates=prior_coordinates,
        )
    )
    applicability = ledger.get(
        event.material.get("input_applicability_event_identity")
    )
    applicability_act = (
        ledger.get(applicability.material.get("act_occurrence_event_identity"))
        if applicability is not None
        else None
    )
    applicability_reference = (
        applicability.material.get("subject_to_act_binding_reference")
        if applicability is not None
        else None
    )
    applicability_binding = None
    applicability_source = None
    if type(applicability_reference) is dict:
        applicability_binding, applicability_source, _source_localities, _content = (
            _read_pair_applicability_subject_to_act_binding(
                ledger,
                applicability_reference.get("recorded_occurrence_identity"),
                prior_coordinates=prior_coordinates,
            )
        )
    applicability_material = None
    if (
        applicability is not None
        and applicability_act is not None
        and applicability_binding is not None
        and applicability_source is not None
    ):
        applicability_material = _require_exact_pair_applicability_result_event(
            ledger,
            applicability,
            binding=applicability_binding,
            source=applicability_source,
            applicability_act_occurrence=applicability_act,
            prior_coordinates=prior_coordinates,
        )
    if (
        reference != _pair_subject_to_act_binding_reference(binding)
        or applicability is None
        or applicability_material != applicability.material.get("applicability")
        or _byte_result_position_reference(applicability_source)
        != _byte_result_position_reference(source)
        or applicability.material.get("dimensions", {}).get("applicability")
        != "applicable"
        or event.locality_identity != binding.locality_identity
        or event.material
        != _pair_measurement_act_material(binding, source, applicability)
    ):
        raise ByteMeasurementError("pair Measurement Act occurrence is not exact")
    try:
        ledger.occurrences_in_append_order(
            (
                applicability_binding.identity,
                binding.identity,
                applicability.identity,
                event.identity,
            ),
            locality_identity=binding.locality_identity,
        )
    except ValueError as error:
        raise ByteMeasurementError(
            "pair Measurement Act does not follow exact Applicability"
        ) from error
    return event, binding, source, applicability


def _pair_measurement_result_material(
    measured: MeasuredBytePairInputs,
    *,
    binding: Event,
    applicability_event: Event,
) -> dict[str, Any]:
    return {
        "result_identity": binding.material["measurement_result_identity"],
        "dimensions": {
            "identity": "byte-position-pair-count-measurement-occurrence",
            "content": "byte-position-pair count and same content",
        },
        "exact_act": "declared byte-position-pair Measurement",
        "addressed_act_identity": binding.material["exact_act_identity"],
        "act_occurrence_identity": binding.material[
            "measurement_act_occurrence_identity"
        ],
        "subject_to_act_binding_reference": (
            _pair_subject_to_act_binding_reference(binding)
        ),
        "source_result_position_reference": measured.source_result_position_reference,
        "source_movement_event_identity": measured.source_movement_event_identity,
        "input_applicability": measured.input_applicability,
        "input_applicability_event_identity": applicability_event.identity,
        "source_localities": list(measured.source_localities),
        "completeness_boundary": {
            "identity": measured.completeness_boundary.identity
        },
        "result_positions": _pair_result_positions(measured),
    }


def _record_pair_measurement_result_from_carried_act(
    ledger: EventLedger,
    *,
    act_occurrence: Event,
    binding: Event,
    source: dict[str, Any],
    applicability_event: Event,
    applicability_act_occurrence: Event,
    current_coordinates: dict[str, Any],
) -> Event:
    applicability_binding = _pair_applicability_binding_of_result(
        ledger,
        applicability_event,
        source=source,
        prior_coordinates=current_coordinates,
    )
    _require_exact_pair_measurement_act_event(
        ledger,
        act_occurrence,
        binding=binding,
        applicability_binding=applicability_binding,
        source=source,
        applicability_event=applicability_event,
        applicability_act_occurrence=applicability_act_occurrence,
        prior_coordinates=current_coordinates,
    )
    _require_carried_pair_measurement_at_current_append_boundary(
        ledger,
        source=source,
        recording_locality_identity=binding.locality_identity,
        current_coordinates=current_coordinates,
        required_binding_identity=binding.identity,
        required_applicability_identity=applicability_event.identity,
    )
    if (
        act_occurrence.kind != BYTE_PAIR_MEASUREMENT_ACT_OCCURRENCE_EVENT
        or ledger.integrity_of(act_occurrence.identity) == CORRUPTED
        or act_occurrence.material
        != _pair_measurement_act_material(
            binding,
            source,
            applicability_event,
        )
        or ledger.append_boundary_through_occurrence(
            act_occurrence.identity
        )
        != ledger.append_boundary()
    ):
        raise ByteMeasurementError(
            "pair Measurement result requires its exact Act at the current append boundary"
        )
    _source_event, source_material, source_localities = _read_byte_result_position(
        ledger, source, prior_coordinates=current_coordinates
    )
    content = source_material["dimensions"]["content"]
    measured = _measure_byte_position_pair_counts_through(
        ledger,
        localities=source_localities,
        boundary=EventLedgerBoundary(content["completeness_boundary"]["identity"]),
        source_result_position_reference=_byte_result_position_reference(source),
        source_movement_event_identity=_byte_result_position_movement_identity(source),
        input_applicability=applicability_event.material["applicability"],
        addressed_act_identity=binding.material["exact_act_identity"],
        act_occurrence_identity=binding.material[
            "measurement_act_occurrence_identity"
        ],
    )
    if (
        ledger.get(act_occurrence.identity) != act_occurrence
        or ledger.integrity_of(act_occurrence.identity) == CORRUPTED
        or ledger.append_boundary_through_occurrence(
            act_occurrence.identity
        )
        != ledger.append_boundary()
    ):
        raise ByteMeasurementError(
            "pair Measurement result requires its exact Act at the current append boundary"
        )
    recorded_material = {
        **_pair_measurement_result_material(
            measured,
            binding=binding,
            applicability_event=applicability_event,
        ),
        "act_occurrence_event_identity": act_occurrence.identity,
        "occurrence_preservation": BYTE_PAIR_OCCURRENCE_PRESERVATION,
    }
    return ledger.append(
        BYTE_PAIR_MEASUREMENT_RECORDED_KIND,
        recorded_material,
        locality_identity=binding.locality_identity,
    )


def _require_exact_pair_measurement_result_event(
    ledger: EventLedger,
    event: Event,
    *,
    act_occurrence: Event,
    binding: Event,
    source: dict[str, Any],
    applicability_event: Event,
    applicability_act_occurrence: Event,
    prior_coordinates: dict[str, Any] | None = None,
) -> None:
    applicability_binding = _pair_applicability_binding_of_result(
        ledger,
        applicability_event,
        source=source,
        prior_coordinates=prior_coordinates,
    )
    _require_exact_pair_measurement_act_event(
        ledger,
        act_occurrence,
        binding=binding,
        applicability_binding=applicability_binding,
        source=source,
        applicability_event=applicability_event,
        applicability_act_occurrence=applicability_act_occurrence,
        prior_coordinates=prior_coordinates,
    )
    _source_event, source_material, source_localities = _read_byte_result_position(
        ledger, source, prior_coordinates=prior_coordinates
    )
    content = source_material["dimensions"]["content"]
    measured = _measure_byte_position_pair_counts_through(
        ledger,
        localities=source_localities,
        boundary=EventLedgerBoundary(content["completeness_boundary"]["identity"]),
        source_result_position_reference=_byte_result_position_reference(source),
        source_movement_event_identity=_byte_result_position_movement_identity(source),
        input_applicability=applicability_event.material["applicability"],
        addressed_act_identity=binding.material["exact_act_identity"],
        act_occurrence_identity=binding.material[
            "measurement_act_occurrence_identity"
        ],
    )
    expected = {
        **_pair_measurement_result_material(
            measured,
            binding=binding,
            applicability_event=applicability_event,
        ),
        "act_occurrence_event_identity": act_occurrence.identity,
        "occurrence_preservation": BYTE_PAIR_OCCURRENCE_PRESERVATION,
    }
    try:
        ordered = ledger.occurrences_in_append_order(
            (act_occurrence.identity, event.identity),
            locality_identity=event.locality_identity,
        )
    except (TypeError, ValueError) as error:
        raise ByteMeasurementError(
            "pair Measurement result does not follow its Act"
        ) from error
    results = tuple(
        candidate
        for candidate in ledger.iter_locality_kind(
            event.locality_identity,
            BYTE_PAIR_MEASUREMENT_RECORDED_KIND,
        )
        if candidate.material.get("act_occurrence_event_identity")
        == act_occurrence.identity
    )
    if (
        type(event) is not Event
        or ledger.get(event.identity) != event
        or event.kind != BYTE_PAIR_MEASUREMENT_RECORDED_KIND
        or event.locality_identity != binding.locality_identity
        or ledger.integrity_of(event.identity) == CORRUPTED
        or event.material != expected
        or tuple(item.identity for item in ordered)
        != (act_occurrence.identity, event.identity)
        or len(results) != 1
        or results[0].identity != event.identity
    ):
        raise ByteMeasurementError(
            "pair Measurement result is not exact"
        )


def _pair_measurement_act_material_without_applicability(
    *,
    source: dict[str, Any],
    source_localities: tuple[str, ...],
    content: dict[str, Any],
    through_event_occurrence_identity: str,
    identities: dict[str, str],
) -> dict[str, Any]:
    return {
        "addressed_act_identity": identities["measurement_act_identity"],
        "act_occurrence_identity": identities[
            "measurement_act_occurrence_identity"
        ],
        "measurement_result_identity": identities["measurement_result_identity"],
        "act": "declared byte-position-pair Measurement",
        "subject_reference": _byte_result_position_reference(source),
        "source_result_position_reference": _byte_result_position_reference(source),
        "source_movement_event_identity": _byte_result_position_movement_identity(
            source
        ),
        "source_localities": list(source_localities),
        "completeness_boundary_identity": content["completeness_boundary"][
            "identity"
        ],
        "result_boundary": BYTE_PAIR_RESULT_BOUNDARY,
        "through_event_occurrence_identity": through_event_occurrence_identity,
    }


def _pair_source_from_act_without_applicability(
    ledger: EventLedger,
    act_occurrence: Event,
    *,
    prior_coordinates: dict[str, Any] | None = None,
) -> tuple[dict[str, Any], tuple[str, ...], dict[str, Any]]:
    reference = act_occurrence.material.get("source_result_position_reference")
    movement_identity = act_occurrence.material.get(
        "source_movement_event_identity"
    )
    boundary = act_occurrence.material.get("through_event_occurrence_identity")
    if type(reference) is not dict or type(boundary) is not str or not boundary:
        raise ByteMeasurementError(
            "pair Measurement Act carries no exact source result position"
        )
    coordinates = prior_coordinates
    if (
        type(coordinates) is not dict
        or coordinates.get("locality_identity") != act_occurrence.locality_identity
    ):
        from seed_runtime.operator_current_coordinates import (
            read_operator_current_coordinates_through,
        )

        try:
            coordinates = read_operator_current_coordinates_through(
                ledger,
                locality_identity=act_occurrence.locality_identity,
                through_event_occurrence_identity=boundary,
            )
        except (TypeError, ValueError) as error:
            raise ByteMeasurementError(
                "pair Measurement Act has no exact prior coordinates"
            ) from error
    if movement_identity is None:
        source = _byte_result_position(
            ledger,
            reference.get("recorded_occurrence_identity"),
            reference.get("result_position"),
            prior_coordinates=coordinates,
        )
    elif type(movement_identity) is str and movement_identity:
        source = _validate_moved_result_position(ledger, movement_identity)
    else:
        source = None
    if (
        source is None
        or _byte_result_position_reference(source) != reference
        or _byte_result_position_movement_identity(source) != movement_identity
        or not _pair_source_is_carried(source, coordinates)
    ):
        raise ByteMeasurementError(
            "pair Measurement Act carries another source result position"
        )
    _source_event, source_material, source_localities = _read_byte_result_position(
        ledger, source, prior_coordinates=coordinates
    )
    dimensions = source_material.get("dimensions")
    content = dimensions.get("content") if type(dimensions) is dict else None
    if (
        source_material.get("result") != "exact_source_material_set"
        or type(content) is not dict
        or type(content.get("completeness_boundary")) is not dict
    ):
        raise ByteMeasurementError(
            "pair Measurement Act carries no exact source result position"
        )
    identities = {
        "measurement_act_identity": act_occurrence.material.get(
            "addressed_act_identity"
        ),
        "measurement_act_occurrence_identity": act_occurrence.material.get(
            "act_occurrence_identity"
        ),
        "measurement_result_identity": act_occurrence.material.get(
            "measurement_result_identity"
        ),
    }
    expected = _pair_measurement_act_material_without_applicability(
        source=source,
        source_localities=source_localities,
        content=content,
        through_event_occurrence_identity=boundary,
        identities=identities,
    )
    anchor = movement_identity or source["recorded_occurrence_identity"]
    ordered_identities = tuple(dict.fromkeys((anchor, boundary, act_occurrence.identity)))
    try:
        ordered = ledger.occurrences_in_append_order(
            ordered_identities,
            locality_identity=act_occurrence.locality_identity,
        )
    except (TypeError, ValueError) as error:
        raise ByteMeasurementError(
            "pair Measurement Act occurrence order is false"
        ) from error
    if (
        any(type(value) is not str or not value for value in identities.values())
        or len(set(identities.values())) != 3
        or act_occurrence.material != expected
        or tuple(event.identity for event in ordered) != ordered_identities
    ):
        raise ByteMeasurementError(
            "pair Measurement Act occurrence coordinates are not exact"
        )
    return source, source_localities, content


def _record_pair_measurement_act_without_applicability(
    ledger: EventLedger,
    *,
    source: dict[str, Any],
    source_localities: tuple[str, ...],
    content: dict[str, Any],
    recording_locality_identity: str,
    current_coordinates: dict[str, Any],
) -> Event:
    boundary = _require_carried_pair_measurement_at_current_append_boundary(
        ledger,
        source=source,
        recording_locality_identity=recording_locality_identity,
        current_coordinates=current_coordinates,
    )
    identities = _new_pair_measurement_identities_without_applicability(ledger)
    source_material = deepcopy(content)
    source_read_event, content_read, localities_read = _read_byte_result_position(
        ledger, source, prior_coordinates=current_coordinates
    )
    boundary_event = ledger.get(boundary)
    if (
        _byte_result_position_reference(source)
        != {
            "recorded_occurrence_identity": source_read_event.identity,
            "result_position": source["result_position"],
        }
        or content_read["dimensions"]["content"] != source_material
        or localities_read != source_localities
        or boundary_event is None
        or ledger.integrity_of(boundary_event.identity) == CORRUPTED
        or ledger.append_boundary_through_occurrence(boundary_event.identity)
        != ledger.append_boundary()
    ):
        raise ByteMeasurementError(
            "pair Measurement source changed before its Act occurrence"
        )
    return ledger.append(
        BYTE_PAIR_MEASUREMENT_ACT_OCCURRENCE_EVENT,
        _pair_measurement_act_material_without_applicability(
            source=source,
            source_localities=source_localities,
            content=content,
            through_event_occurrence_identity=boundary,
            identities=identities,
        ),
        locality_identity=recording_locality_identity,
    )


def _pair_measurement_result_material_without_applicability(
    measured: MeasuredBytePairInputs,
    *,
    act_occurrence: Event,
) -> dict[str, Any]:
    return {
        "result_identity": act_occurrence.material["measurement_result_identity"],
        "dimensions": {
            "identity": "byte-position-pair-count-measurement-occurrence",
            "content": "byte-position-pair count and same content",
        },
        "exact_act": "declared byte-position-pair Measurement",
        "addressed_act_identity": act_occurrence.material[
            "addressed_act_identity"
        ],
        "act_occurrence_identity": act_occurrence.material[
            "act_occurrence_identity"
        ],
        "source_result_position_reference": measured.source_result_position_reference,
        "source_movement_event_identity": measured.source_movement_event_identity,
        "source_localities": list(measured.source_localities),
        "completeness_boundary": {
            "identity": measured.completeness_boundary.identity
        },
        "result_positions": _pair_result_positions(measured),
        "act_occurrence_event_identity": act_occurrence.identity,
        "occurrence_preservation": BYTE_PAIR_OCCURRENCE_PRESERVATION,
    }


def _record_pair_measurement_result_without_applicability(
    ledger: EventLedger,
    *,
    act_occurrence: Event,
    current_coordinates: dict[str, Any],
) -> Event:
    source, source_localities, content = _pair_source_from_act_without_applicability(
        ledger, act_occurrence, prior_coordinates=current_coordinates
    )
    existing = tuple(
        event
        for event in ledger.iter_locality_kind(
            act_occurrence.locality_identity,
            BYTE_PAIR_MEASUREMENT_RECORDED_KIND,
        )
        if event.material.get("act_occurrence_event_identity")
        == act_occurrence.identity
        or event.material.get("act_occurrence_identity")
        == act_occurrence.material["act_occurrence_identity"]
    )
    if existing:
        raise ByteMeasurementError(
            "one pair Measurement Act cannot record a second result"
        )
    measured = _measure_byte_position_pair_counts_through(
        ledger,
        localities=source_localities,
        boundary=EventLedgerBoundary(content["completeness_boundary"]["identity"]),
        source_result_position_reference=_byte_result_position_reference(source),
        source_movement_event_identity=_byte_result_position_movement_identity(source),
        input_applicability={},
        addressed_act_identity=act_occurrence.material["addressed_act_identity"],
        act_occurrence_identity=act_occurrence.material["act_occurrence_identity"],
    )
    act_material = deepcopy(act_occurrence.material)
    source_read, localities_read, content_read = _pair_source_from_act_without_applicability(
        ledger, act_occurrence, prior_coordinates=current_coordinates
    )
    if (
        act_occurrence.material != act_material
        or source_read != source
        or localities_read != source_localities
        or content_read != content
        or ledger.append_boundary_through_occurrence(act_occurrence.identity)
        != ledger.append_boundary()
    ):
        raise ByteMeasurementError(
            "pair Measurement coordinates changed before its result occurrence"
        )
    return ledger.append(
        BYTE_PAIR_MEASUREMENT_RECORDED_KIND,
        _pair_measurement_result_material_without_applicability(
            measured, act_occurrence=act_occurrence
        ),
        locality_identity=act_occurrence.locality_identity,
    )


def _record_byte_position_pair_count_layer_from_carried_current_coordinates(
    ledger: EventLedger,
    *,
    source: dict[str, Any],
    source_localities: tuple[str, ...],
    content: dict[str, Any],
    recording_locality_identity: str,
    current_coordinates: dict[str, Any],
) -> tuple[Event, dict[str, Any]]:
    from seed_runtime.operator_current_coordinates import (
        advance_operator_current_coordinates,
    )

    prior = current_coordinates["through_event_occurrence_identity"]
    act_occurrence = _record_pair_measurement_act_without_applicability(
        ledger,
        source=source,
        source_localities=source_localities,
        content=content,
        recording_locality_identity=recording_locality_identity,
        current_coordinates=current_coordinates,
    )
    current_coordinates = advance_operator_current_coordinates(
        ledger,
        (act_occurrence.identity,),
        locality_identity=recording_locality_identity,
        prior=current_coordinates,
    )
    if current_coordinates["through_event_occurrence_identity"] != act_occurrence.identity:
        raise ByteMeasurementError(
            "pair Measurement Act did not advance exact current coordinates"
        )
    result = _record_pair_measurement_result_without_applicability(
        ledger,
        act_occurrence=act_occurrence,
        current_coordinates=current_coordinates,
    )
    current_coordinates = advance_operator_current_coordinates(
        ledger,
        (result.identity,),
        locality_identity=recording_locality_identity,
        prior=current_coordinates,
    )
    if (
        prior == result.identity
        or current_coordinates["through_event_occurrence_identity"] != result.identity
    ):
        raise ByteMeasurementError(
            "pair Measurement result did not advance exact current coordinates"
        )
    return result, current_coordinates


def _record_byte_position_pair_count_layer_from_current_coordinates(
    ledger: EventLedger,
    *,
    source_measurement_event_identity: str,
    recording_locality_identity: str,
    current_coordinates: dict[str, Any],
) -> tuple[Event, dict[str, Any]]:
    source, source_localities, content = _prepare_pair_source(
        ledger,
        source_measurement_event_identity=source_measurement_event_identity,
        measurement_locality_identity=recording_locality_identity,
        prior_coordinates=current_coordinates,
    )
    _require_carried_pair_measurement_at_current_append_boundary(
        ledger,
        source=source,
        recording_locality_identity=recording_locality_identity,
        current_coordinates=current_coordinates,
    )
    return _record_byte_position_pair_count_layer_from_carried_current_coordinates(
        ledger,
        source=source,
        source_localities=source_localities,
        content=content,
        recording_locality_identity=recording_locality_identity,
        current_coordinates=current_coordinates,
    )


def record_byte_position_pair_count_layer(
    ledger: EventLedger,
    *,
    source_measurement_event_identity: str,
    recording_locality_identity: str,
):
    """Record exact byte-position-pair counts without crossing append boundaries."""

    if not isinstance(recording_locality_identity, str) or not recording_locality_identity:
        raise ByteMeasurementError(
            "byte-position-pair Measurement recording requires an exact Locality"
        )
    source, source_localities, content = _prepare_pair_source(
        ledger,
        source_measurement_event_identity=source_measurement_event_identity,
        measurement_locality_identity=recording_locality_identity,
    )
    from seed_runtime.operator_current_coordinates import read_operator_current_coordinates

    current_coordinates = read_operator_current_coordinates(
        ledger, locality_identity=recording_locality_identity
    )
    result, _current_coordinates = _record_byte_position_pair_count_layer_from_carried_current_coordinates(
        ledger,
        source=source,
        source_localities=source_localities,
        content=content,
        recording_locality_identity=recording_locality_identity,
        current_coordinates=current_coordinates,
    )
    return result


def _validated_recorded_byte_position_pair_measurement(
    ledger: EventLedger,
    event_identity: str,
    *,
    findings_only: bool,
    prior_coordinates: dict[str, Any] | None = None,
) -> _RecordedBytePairMeasurementReading | None:
    """Validate one exact pair result and return its requested reading surface."""

    event = ledger.get(event_identity)
    if event is None:
        return None
    if event.kind != BYTE_PAIR_MEASUREMENT_RECORDED_KIND:
        raise ByteMeasurementError(
            f"{event_identity} is not a byte-position-pair Measurement occurrence"
        )
    if ledger.integrity_of(event_identity) == CORRUPTED:
        raise ByteMeasurementError("a corrupted occurrence cannot return pair results")
    material = event.material
    has_no_applicability = "subject_to_act_binding_reference" not in material
    exact_surface = (
        BYTE_PAIR_RESULT_COORDINATES_WITHOUT_APPLICABILITY
        if has_no_applicability
        else BYTE_PAIR_RESULT_COORDINATES
    ) | {
        "act_occurrence_identity",
        "act_occurrence_event_identity",
        "occurrence_preservation",
    }
    if set(material) != exact_surface:
        raise ByteMeasurementError(
            f"{event_identity} does not carry the exact pair result and recording surfaces"
        )
    binding_reference = material.get("subject_to_act_binding_reference")
    act_occurrence_identity = material.get("act_occurrence_identity")
    act_occurrence_event_identity = material.get("act_occurrence_event_identity")
    act_occurrence, binding, source, applicability_event = (
        _read_pair_measurement_act_occurrence(
            ledger,
            act_occurrence_event_identity,
            prior_coordinates=prior_coordinates,
        )
    )
    if has_no_applicability:
        if (
            binding is not None
            or applicability_event is not None
            or event.locality_identity != act_occurrence.locality_identity
            or material.get("result_identity")
            != act_occurrence.material["measurement_result_identity"]
            or material.get("source_result_position_reference")
            != _byte_result_position_reference(source)
            or material.get("source_movement_event_identity")
            != _byte_result_position_movement_identity(source)
        ):
            raise ByteMeasurementError(
                f"{event_identity} carries no exact pair Measurement without Applicability"
            )
    elif (
        binding is None
        or applicability_event is None
        or binding_reference != _pair_subject_to_act_binding_reference(binding)
        or event.locality_identity != binding.locality_identity
        or material.get("result_identity")
        != binding.material["measurement_result_identity"]
        or material.get("source_result_position_reference")
        != _byte_result_position_reference(source)
        or material.get("source_movement_event_identity")
        != _byte_result_position_movement_identity(source)
        or material.get("input_applicability_event_identity")
        != applicability_event.identity
    ):
        raise ByteMeasurementError(
            f"{event_identity} carries no exact pair Measurement binding"
        )
    expected_dimensions = {
        "identity": "byte-position-pair-count-measurement-occurrence",
        "content": "byte-position-pair count and same content",
    }
    if (
        material.get("occurrence_preservation") != BYTE_PAIR_OCCURRENCE_PRESERVATION
        or material.get("exact_act") != "declared byte-position-pair Measurement"
        or not isinstance(material.get("addressed_act_identity"), str)
        or not material["addressed_act_identity"]
        or not isinstance(material.get("act_occurrence_identity"), str)
        or not material["act_occurrence_identity"]
        or material["addressed_act_identity"] == material["act_occurrence_identity"]
        or material.get("dimensions") != expected_dimensions
    ):
        raise ByteMeasurementError(
            f"{event_identity} does not preserve its exact pair Measurement result position"
        )
    if not has_no_applicability:
        carried_applicability = material.get("input_applicability")
        applicability_dimensions = (
            carried_applicability.get("dimensions")
            if isinstance(carried_applicability, dict)
            else None
        )
        applicability_identity = (
            applicability_dimensions.get("identity")
            if isinstance(applicability_dimensions, dict)
            else None
        )
        if not isinstance(applicability_identity, str) or not applicability_identity:
            raise ByteMeasurementError(
                f"{event_identity} carries no exact input Applicability"
            )
        if (
            binding is None
            or applicability_event is None
            or act_occurrence.material
            != _pair_measurement_act_material(binding, source, applicability_event)
        ):
            raise ByteMeasurementError(
                f"{event_identity} names no exact responsible pair Measurement Act occurrence"
            )
    try:
        ordered = ledger.occurrences_in_append_order(
            (act_occurrence.identity, event.identity),
            locality_identity=event.locality_identity,
        )
    except (TypeError, ValueError) as error:
        raise ByteMeasurementError(
            f"{event_identity} does not follow its pair Measurement Act"
        ) from error
    results = tuple(
        candidate
        for candidate in ledger.iter_locality_kind(
            event.locality_identity,
            BYTE_PAIR_MEASUREMENT_RECORDED_KIND,
        )
        if candidate.material.get("act_occurrence_event_identity")
        == act_occurrence.identity
    )
    if (
        tuple(item.identity for item in ordered)
        != (act_occurrence.identity, event.identity)
        or len(results) != 1
        or results[0].identity != event.identity
    ):
        raise ByteMeasurementError(
            f"{event_identity} is not the single exact pair Measurement result"
        )
    boundary_value = material.get("completeness_boundary")
    localities_value = material.get("source_localities")
    if (
        not isinstance(boundary_value, dict)
        or set(boundary_value) != {"identity"}
        or not isinstance(boundary_value["identity"], str)
        or not isinstance(localities_value, list)
        or not localities_value
        or any(not isinstance(item, str) or not item for item in localities_value)
        or len(set(localities_value)) != len(localities_value)
    ):
        raise ByteMeasurementError(
            f"{event_identity} does not carry the exact pair Measurement boundary"
        )
    source_reference = material.get("source_result_position_reference")
    if (
        not isinstance(source_reference, dict)
        or set(source_reference)
        != {"recorded_occurrence_identity", "result_position"}
        or not isinstance(source_reference["recorded_occurrence_identity"], str)
        or not source_reference["recorded_occurrence_identity"]
        or type(source_reference["result_position"]) is not int
        or source_reference["result_position"] < 0
    ):
        raise ByteMeasurementError(f"{event_identity} carries no exact source result position")
    if (
        _byte_result_position_reference(source) != source_reference
        or event.locality_identity is None
    ):
        raise ByteMeasurementError(
            f"{event_identity} does not carry its exact input source result position"
        )
    _source_event, source_material, source_localities = _read_byte_result_position(
        ledger, source, prior_coordinates=prior_coordinates
    )
    source_content = source_material["dimensions"]["content"]
    if (
        localities_value != list(source_localities)
        or boundary_value != source_content["completeness_boundary"]
        or (
            binding is not None
            and binding.material.get("source_localities") != localities_value
        )
        or (
            binding is not None
            and binding.material.get("completeness_boundary_identity")
            != boundary_value["identity"]
        )
    ):
        raise ByteMeasurementError(
            f"{event_identity} does not carry its exact input source boundary"
        )
    if not has_no_applicability:
        applicability_event_identity = material.get(
            "input_applicability_event_identity"
        )
        if (
            applicability_event is None
            or applicability_event_identity != applicability_event.identity
            or applicability_event.material.get("applicability")
            != material.get("input_applicability")
        ):
            raise ByteMeasurementError(
                f"{event_identity} does not name its exact recorded input Applicability"
            )
    result_positions = material.get("result_positions")
    if not isinstance(result_positions, list):
        raise ByteMeasurementError(f"{event_identity} carries no pair result result positions")
    by_pair: dict[tuple[int, int], dict[str, dict[str, Any]]] = {}
    exact_keys = {
        "dimensions",
        "result",
        "subject",
        "referenced_result_position_references",
        "referenced_result_positions",
    }
    for position, result_position in enumerate(result_positions):
        if not isinstance(result_position, dict) or set(result_position) != exact_keys:
            raise ByteMeasurementError(f"{event_identity} carries a malformed pair result position")
        subject = result_position.get("subject")
        result = result_position.get("result")
        dimensions = result_position.get("dimensions")
        exact_pair = (
            subject.get("content") if isinstance(subject, dict) else None
        )
        if (
            type(exact_pair) is not list
            or len(exact_pair) != 2
            or any(
                type(value) is not int or not 0 <= value <= 255
                for value in exact_pair
            )
            or subject
            != {
                "content": exact_pair,
            }
            or result not in {"count", "recurrence"}
            or not isinstance(dimensions, dict)
            or set(dimensions)
                != {
                    "position",
                    "content",
                }
            or dimensions.get("position") != position
        ):
            raise ByteMeasurementError(f"{event_identity} carries an unlawful pair result position")
        content = dimensions.get("content")
        content_shape_is_exact = (
            result == "recurrence"
            and content == {"recurrence_established": True}
        ) or (
            result == "count"
            and type(content) is dict
            and set(content) == {"input_count", "occurrences_carrying", "count"}
            and all(type(value) is int for value in content.values())
        )
        if not content_shape_is_exact:
            raise ByteMeasurementError(
                f"{event_identity} carries unlawful pair {result}"
            )
        group = by_pair.setdefault(tuple(exact_pair), {})
        if result in group:
            raise ByteMeasurementError(f"{event_identity} duplicates one pair result")
        group[result] = result_position
    for group in by_pair.values():
        count = group.get("count")
        if count is None:
            raise ByteMeasurementError(f"{event_identity} carries recurrence without count")
        count_content = count["dimensions"]["content"]
        if (
            not isinstance(count_content, dict)
            or set(count_content)
            != {"input_count", "occurrences_carrying", "count"}
            or any(type(value) is not int or value <= 0 for value in count_content.values())
            or count_content["occurrences_carrying"] > count_content["input_count"]
            or count_content["occurrences_carrying"] > count_content["count"]
            or count["referenced_result_position_references"] != [source_reference]
            or count["referenced_result_positions"] != []
        ):
            raise ByteMeasurementError(f"{event_identity} carries an unlawful pair count")
        recurrence = group.get("recurrence")
        if (recurrence is not None) != (count_content["count"] > 1):
            raise ByteMeasurementError(f"{event_identity} carries the wrong recurrence boundary")
        if recurrence is not None and (
            recurrence["dimensions"]["content"] != {"recurrence_established": True}
            or recurrence["referenced_result_position_references"] != []
            or recurrence["referenced_result_positions"]
            != [count["dimensions"]["position"]]
        ):
            raise ByteMeasurementError(
                f"{event_identity} carries an unlawful recurrence result position reference"
            )
    validated_results = []
    for result_position in result_positions:
        if findings_only:
            content = result_position["dimensions"]["content"]
            content_coordinates: tuple[int, int, int] | bool
            if result_position["result"] == "recurrence":
                content_coordinates = content["recurrence_established"]
            else:
                content_coordinates = (
                    content["input_count"],
                    content["occurrences_carrying"],
                    content["count"],
                )
            validated_results.append(
                _RecordedBytePairFinding(
                    result_position=result_position["dimensions"]["position"],
                    recorded_occurrence_identity=event.identity,
                    exact_pair=tuple(
                        result_position["subject"]["content"]
                    ),
                    result=result_position["result"],
                    _content_coordinates=content_coordinates,
                    _referenced_result_positions=tuple(
                        result_position["referenced_result_positions"]
                    ),
                )
            )
            continue
        referenced_result_position_references = list(
            result_position["referenced_result_position_references"]
        )
        referenced_result_position_references.extend(
            {
                "recorded_occurrence_identity": event.identity,
                "result_position": local_position,
            }
            for local_position in result_position["referenced_result_positions"]
        )
        validated_results.append(RecordedBytePairResultPosition(
            result_position=result_position["dimensions"]["position"],
            recorded_occurrence_identity=event.identity,
            content=tuple(result_position["subject"]["content"]),
            result=result_position["result"],
            _material=deepcopy(result_position),
            _referenced_result_position_references=tuple(
                deepcopy(referenced_result_position_references)
            ),
        ))
    return _RecordedBytePairMeasurementReading(
        results=tuple(validated_results),
        binding=binding,
        source=source,
    )


def _read_recorded_byte_position_pair_measurement(
    ledger: EventLedger,
    event_identity: str,
    *,
    findings_only: bool,
    prior_coordinates: dict[str, Any] | None = None,
) -> tuple[RecordedBytePairResultPosition, ...] | tuple[_RecordedBytePairFinding, ...] | None:
    reading = _validated_recorded_byte_position_pair_measurement(
        ledger,
        event_identity,
        findings_only=findings_only,
        prior_coordinates=prior_coordinates,
    )
    return reading.results if reading is not None else None


def result_positions_of_recorded_byte_position_pair_measurement(
    ledger: EventLedger,
    event_identity: str,
    *,
    prior_coordinates: dict[str, Any] | None = None,
) -> tuple[RecordedBytePairResultPosition, ...] | None:
    """Read the exact pair result without performing Measurement again."""

    reading = _read_recorded_byte_position_pair_measurement(
        ledger,
        event_identity,
        findings_only=False,
        prior_coordinates=prior_coordinates,
    )
    return reading


def _findings_of_recorded_byte_position_pair_measurement(
    ledger: EventLedger,
    event_identity: str,
    *,
    prior_coordinates: dict[str, Any] | None = None,
) -> tuple[_RecordedBytePairFinding, ...] | None:
    """Read only exact finding coordinates after the same full validation."""

    reading = _read_recorded_byte_position_pair_measurement(
        ledger,
        event_identity,
        findings_only=True,
        prior_coordinates=prior_coordinates,
    )
    return reading


def byte_position_pair_measurement_occurrence_references(
    ledger: EventLedger, event_identity: str
) -> tuple[str, ...]:
    """Return the exact ordered occurrences preceding one pair result."""

    result_positions = result_positions_of_recorded_byte_position_pair_measurement(
        ledger, event_identity
    )
    if type(result_positions) is not tuple:
        raise ByteMeasurementError("pair Measurement result is absent")
    result = ledger.get(event_identity)
    assert result is not None
    if "input_applicability_event_identity" not in result.material:
        references = (
            result.material["act_occurrence_event_identity"],
            result.identity,
        )
        ordered = ledger.occurrences_in_append_order(
            references, locality_identity=result.locality_identity
        )
        if tuple(event.identity for event in ordered) != references:
            raise ByteMeasurementError(
                "pair Measurement occurrences are not ordered"
            )
        return references
    applicability_identity = result.material["input_applicability_event_identity"]
    applicability = ledger.get(applicability_identity)
    if applicability is None:
        raise ByteMeasurementError(
            "pair Measurement carries no exact Applicability result"
        )
    get_recorded_pair_input_applicability(ledger, applicability.identity)
    references = (
        applicability.material["act_occurrence_identity"],
        applicability.material["yield_relation_identity"],
        applicability.identity,
        result.material["act_occurrence_identity"],
        result.material["yield_relation_identity"],
        result.identity,
    )
    ordered = ledger.occurrences_in_append_order(
        references, locality_identity=result.locality_identity
    )
    if tuple(event.identity for event in ordered) != references:
        raise ByteMeasurementError(
            "pair Applicability and Measurement occurrences are not ordered"
        )
    return references


def input_applicability_of_recorded_byte_position_pair_measurement(
    ledger: EventLedger, event_identity: str
) -> dict[str, Any] | None:
    """Validate the exact input-to-Act Applicability result position."""

    read = result_positions_of_recorded_byte_position_pair_measurement(ledger, event_identity)
    if read is None:
        return None
    event = ledger.get(event_identity)
    return deepcopy(event.material.get("input_applicability"))
