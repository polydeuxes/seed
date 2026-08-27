"""Measure exact bytes across complete bounded material result occurrences.

This is the first source boundary that does not receive its measured
subjects from a caller.  The subjects are the literal byte values carried by
the exact material linked from every material result occurrence in the declared
Localities through one recorded ledger boundary.

One byte value receives one count Assertion.  Recurrence is a separate
Assertion and exists only where the total count exceeds one.  The same byte
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
BYTE_PAIR_MEASUREMENT_RESULT_KIND = "exact byte-position-pair count Measurement results"
BYTE_OCCURRENCE_PRESERVATION = (
    "byte Measurement results with Yield"
)
BYTE_PAIR_OCCURRENCE_PRESERVATION = (
    "byte-position-pair Measurement results with Yield"
)
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
        "assertions",
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
    "source_assertion_reference",
    "source_movement_event_identity",
    "input_applicability",
    "input_applicability_event_identity",
    "subject_to_act_binding_reference",
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
        "input_assertion_reference",
        "input_movement_event_identity",
        "applicability",
    }
)
BYTE_PAIR_APPLICABILITY_ACT_OCCURRENCE_EVENT = (
    "operator.measurement.byte_position_pair_applicability_act_occurrence_recorded"
)
ASSERTION_LOCALITY_MOVEMENT_KIND = "operator.assertion.locality_movement_recorded"
ASSERTION_LOCALITY_MOVEMENT_SUBJECT_TO_ACT_BINDING_KIND = (
    "operator.assertion.locality_movement_subject_to_act_binding_recorded"
)
ASSERTION_LOCALITY_MOVEMENT_ACT_OCCURRENCE_EVENT = (
    "operator.assertion.locality_movement_act_occurrence_recorded"
)
ASSERTION_LOCALITY_MOVEMENT_RESULT_KIND = "Assertion Locality movement result"
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
    ASSERTION_LOCALITY_MOVEMENT_SUBJECT_TO_ACT_BINDING_KIND: "03.Movement.A",
    ASSERTION_LOCALITY_MOVEMENT_ACT_OCCURRENCE_EVENT: "02.Acts.A",
    ASSERTION_LOCALITY_MOVEMENT_KIND: "03.Movement.A",
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
    source_assertion_reference: dict[str, str]
    source_movement_event_identity: str | None
    input_applicability: dict[str, Any]
    addressed_act_identity: str
    act_occurrence_identity: str
    counts: tuple[MeasuredBytePairCount, ...]


def _byte_result_position_reference(source: dict[str, Any]) -> dict[str, Any]:
    return {
        "recorded_occurrence_identity": source["recorded_occurrence_identity"],
        "assertion_position": source["assertion_position"],
    }


def _byte_result_position_movement_identity(source: dict[str, Any]) -> str | None:
    return source.get("locality_movement_event_identity")


@dataclass(frozen=True)
class RecordedBytePairAssertion:
    assertion_position: int
    recorded_occurrence_identity: str
    content: tuple[int, int] | None
    result: str
    _material: dict[str, Any]
    _referenced_assertions: tuple[dict[str, Any], ...]

    @property
    def material(self) -> dict[str, Any]:
        return deepcopy(self._material)

    @property
    def referenced_assertions(self) -> tuple[dict[str, Any], ...]:
        return deepcopy(self._referenced_assertions)

    @property
    def reference(self) -> dict[str, Any]:
        return {
            "recorded_occurrence_identity": self.recorded_occurrence_identity,
            "assertion_position": self.assertion_position,
        }


@dataclass(frozen=True)
class _RecordedBytePairFinding:
    assertion_position: int
    recorded_occurrence_identity: str
    exact_pair: tuple[int, int]
    result: str
    _content_coordinates: tuple[int, int, int] | bool
    _referenced_assertion_positions: tuple[int, ...]

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
            "assertion_position": self.assertion_position,
        }


@dataclass(frozen=True)
class _RecordedBytePairMeasurementReading:
    results: tuple[RecordedBytePairAssertion, ...] | tuple[_RecordedBytePairFinding, ...]
    binding: Event
    source: dict[str, Any]


def _recorded_input_assertion_coordinates(
    ledger: EventLedger,
    source: dict[str, Any],
    *,
    measurement_locality_identity: str,
    prior_coordinates: dict[str, Any] | None = None,
) -> tuple[dict[str, Any], dict[str, str | None]]:
    """Resolve the exact occurrences carrying one proposed input."""

    if type(source) is not dict or set(source) != {
        "recorded_occurrence_identity",
        "assertion_position",
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
            source["assertion_position"],
            prior_coordinates=prior_coordinates,
        )
        if (
            source_event is None
            or source_event.locality_identity != measurement_locality_identity
        ):
            exact = None
    else:
        exact = _validate_moved_byte_assertion(
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
    assertion = None
    if exact is not None:
        _event, assertion, _localities = _read_byte_result_position(
            ledger,
            exact,
            prior_coordinates=prior_coordinates,
        )
    if (
        exact is None
        or assertion is None
        or assertion["result"] != "exact_source_material_set"
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
        "assertion_position": exact["assertion_position"],
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
    """Determine this source Assertion's use by this exact pair Measurement."""

    source, input_coordinates = _recorded_input_assertion_coordinates(
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
    """Build Applicability from an already validated exact source carrier."""

    if input_coordinates is None:
        input_coordinates = {
            "recorded_measurement_result_occurrence_identity": (
                source["recorded_occurrence_identity"]
            ),
            "assertion_position": source["assertion_position"],
            "locality_movement_result_occurrence_identity": (
                _byte_result_position_movement_identity(source)
            ),
        }
    reference = _byte_result_position_reference(source)
    movement_identity = _byte_result_position_movement_identity(source)
    content = {
        "input_assertion_reference": reference,
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
        "input_assertion_reference": reference,
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
    read = _assertions_of_recorded_byte_measurement(
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
            "byte-position-pair Measurement requires an exact source-material-set Assertion"
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
    source = _move_byte_assertion_to_locality(
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


def _source_assertion_reference(
    source: dict[str, Any],
) -> dict[str, Any]:
    return _byte_result_position_reference(source)


def _source_assertion_coordinates(
    ledger: EventLedger,
    source: dict[str, Any],
) -> dict[str, Any]:
    source_event = ledger.get(source["recorded_occurrence_identity"])
    if source_event is None:
        raise ByteMeasurementError("Assertion movement source cannot be read")
    if source_event.kind == BYTE_MEASUREMENT_RECORDED_KIND:
        _event, material, _localities = _read_byte_result_position(ledger, source)
        return material

    from seed_runtime.measurement_of_position_coordinates_of_byte_pair_occurrences import (
        BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND,
        _recorded_position_assertion_at_position_for_locality_movement,
    )

    if source_event.kind == BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND:
        return _recorded_position_assertion_at_position_for_locality_movement(
            ledger,
            result_event_identity=source_event.identity,
            assertion_position=source["assertion_position"],
        )

    from seed_runtime.comparison_of_ordered_relation_path_with_recorded_pair_findings import (
        COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_RESULT_KIND,
        _recorded_path_comparison_finding_assertion_coordinates_for_locality_movement,
    )

    if (
        source_event.kind
        == COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_RESULT_KIND
    ):
        return _recorded_path_comparison_finding_assertion_coordinates_for_locality_movement(
            ledger,
            result_event_identity=source_event.identity,
            assertion_position=source["assertion_position"],
        )
    raise ByteMeasurementError("Assertion movement source cannot be read")


def _source_assertion_from_reference(
    ledger: EventLedger, reference: Any
) -> tuple[dict[str, Any], Event]:
    if type(reference) is not dict or "recorded_occurrence_identity" not in reference:
        raise ByteMeasurementError("Assertion movement carries no exact source")
    source_event = ledger.get(reference["recorded_occurrence_identity"])
    if source_event is None or source_event.locality_identity is None:
        raise ByteMeasurementError("Assertion movement source cannot be read")
    if source_event.kind == BYTE_MEASUREMENT_RECORDED_KIND:
        if (
            set(reference)
            != {"recorded_occurrence_identity", "assertion_position"}
            or type(reference["assertion_position"]) is not int
            or reference["assertion_position"] < 0
        ):
            raise ByteMeasurementError("Assertion movement carries no exact source")
        source = _byte_result_position(
            ledger,
            source_event.identity,
            reference["assertion_position"],
        )
        if source is not None:
            return source, source_event

    from seed_runtime.measurement_of_position_coordinates_of_byte_pair_occurrences import (
        BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND,
        _recorded_position_assertion_at_position_for_locality_movement,
    )

    if source_event.kind == BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND:
        if set(reference) != {
            "recorded_occurrence_identity",
            "assertion_position",
        } or type(reference["assertion_position"]) is not int:
            raise ByteMeasurementError("Assertion movement carries no exact source")
        try:
            coordinates = _recorded_position_assertion_at_position_for_locality_movement(
                ledger,
                result_event_identity=source_event.identity,
                assertion_position=reference["assertion_position"],
            )
        except ValueError:
            pass
        else:
            return {
                **deepcopy(reference),
                "locality_movement_event_identity": None,
            }, source_event

    from seed_runtime.comparison_of_ordered_relation_path_with_recorded_pair_findings import (
        COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_RESULT_KIND,
        _recorded_path_comparison_finding_assertion_coordinates_for_locality_movement,
    )

    if (
        source_event.kind
        == COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_RESULT_KIND
    ):
        if set(reference) != {
            "recorded_occurrence_identity",
            "assertion_position",
        } or type(reference["assertion_position"]) is not int:
            raise ByteMeasurementError("Assertion movement carries no exact source")
        try:
            coordinates = _recorded_path_comparison_finding_assertion_coordinates_for_locality_movement(
                ledger,
                result_event_identity=source_event.identity,
                assertion_position=reference["assertion_position"],
            )
        except ValueError:
            pass
        else:
            return {
                **deepcopy(reference),
                "locality_movement_event_identity": None,
            }, source_event
    raise ByteMeasurementError("Assertion movement source cannot be read")


def _source_measurement_current_coordinates(source_event: Event) -> dict[str, str]:
    return {
        "recorded_occurrence_identity": source_event.identity,
        "result_identity": source_event.material["result_identity"],
        "act_occurrence_identity": source_event.material["act_occurrence_identity"],
        "act_occurrence_event_identity": source_event.material[
            "act_occurrence_event_identity"
        ],
        "yield_relation_identity": source_event.material[
            "yield_relation_identity"
        ],
    }


def _source_assertion_is_carried(
    source_event: Event, current_coordinates: dict[str, Any]
) -> bool:
    from seed_runtime.comparison_of_ordered_relation_path_with_recorded_pair_findings import (
        COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_RESULT_KIND,
    )

    if (
        source_event.kind
        == COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_RESULT_KIND
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
        or not _source_assertion_is_carried(source_event, current_coordinates)
    ):
        raise ByteMeasurementError(
            "Assertion movement binding requires exact current source coordinates"
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
            "Assertion movement requires exact current destination coordinates"
        )
    return boundary


def _movement_binding_material(
    *,
    source: dict[str, Any],
    source_assertion_coordinates: dict[str, Any],
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
        "source_assertion_reference": _source_assertion_reference(source),
        "source_assertion_coordinates": deepcopy(source_assertion_coordinates),
        "source_locality": source_locality,
        "destination_locality": destination_locality,
        "source_through_event_occurrence_identity": source_through_event_occurrence_identity,
        "destination_through_event_occurrence_identity": (
            destination_through_event_occurrence_identity
        ),
        "determination": (
            "the exact Assertion at another Locality"
        ),
    }


def _require_exact_movement_binding_and_source(
    ledger: EventLedger, binding: Event
) -> tuple[dict[str, Any], Event]:
    if (
        type(binding) is not Event
        or binding.kind
        != ASSERTION_LOCALITY_MOVEMENT_SUBJECT_TO_ACT_BINDING_KIND
        or binding.locality_identity is None
        or ledger.get(binding.identity) != binding
        or ledger.integrity_of(binding.identity) == CORRUPTED
    ):
        raise ByteMeasurementError(
            "Assertion movement requires an exact subject-to-Act binding"
        )
    source, source_event = _source_assertion_from_reference(
        ledger, binding.material.get("source_assertion_reference")
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
            source_assertion_coordinates=_source_assertion_coordinates(ledger, source),
            source_event=source_event,
            source_locality=source_event.locality_identity,
            destination_locality=binding.locality_identity,
            source_through_event_occurrence_identity=source_boundary,
            destination_through_event_occurrence_identity=destination_boundary,
            **identities,
        )
    ):
        raise ByteMeasurementError(
            "Assertion movement requires an exact source and binding"
        )
    return source, source_event


def record_assertion_locality_movement_subject_to_act_binding(
    ledger: EventLedger,
    *,
    source: dict[str, Any],
    destination_locality: str,
    source_current_coordinates: dict[str, Any],
    destination_current_coordinates: dict[str, Any],
) -> Event:
    """Record the exact subject-to-Act binding for one Assertion movement."""

    if type(destination_locality) is not str or not destination_locality:
        raise ByteMeasurementError("Assertion movement requires a destination Locality")
    exact_source, source_event = _source_assertion_from_reference(
        ledger, _byte_result_position_reference(source)
    )
    if exact_source != source:
        raise ByteMeasurementError("Assertion movement requires its exact source")
    if source_event.locality_identity == destination_locality:
        raise ByteMeasurementError("same-Locality Assertion requires no movement")
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
        "movement_act_identity": ledger.mint_identity("assertion_locality_movement_act"),
        "movement_act_occurrence_identity": ledger.mint_identity(
            "assertion_locality_movement_occurrence"
        ),
        "movement_result_identity": ledger.mint_identity(
            "assertion_locality_movement_result"
        ),
    }
    if len(set(identities.values())) != len(identities):
        raise ByteMeasurementError("Assertion movement lifecycle identities collapsed")
    return ledger.append(
        ASSERTION_LOCALITY_MOVEMENT_SUBJECT_TO_ACT_BINDING_KIND,
        _movement_binding_material(
            source=source,
            source_assertion_coordinates=_source_assertion_coordinates(ledger, source),
            source_event=source_event,
            source_locality=source_event.locality_identity,
            destination_locality=destination_locality,
            source_through_event_occurrence_identity=source_boundary,
            destination_through_event_occurrence_identity=destination_boundary,
            **identities,
        ),
        locality_identity=destination_locality,
    )


def _read_assertion_locality_movement_subject_to_act_binding(
    ledger: EventLedger,
    binding_event_identity: str,
    *,
    prior_destination_coordinates: dict[str, Any] | None = None,
) -> tuple[Event, dict[str, Any], Event]:
    binding = ledger.get(binding_event_identity)
    if (
        binding is None
        or binding.kind
        != ASSERTION_LOCALITY_MOVEMENT_SUBJECT_TO_ACT_BINDING_KIND
        or binding.locality_identity is None
        or ledger.integrity_of(binding.identity) == CORRUPTED
    ):
        raise ByteMeasurementError(
            "Assertion movement binding is absent or corrupted"
        )
    material = binding.material
    source, source_event = _source_assertion_from_reference(
        ledger, material.get("source_assertion_reference")
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
            "Assertion movement binding carries malformed coordinates"
        )
    expected = _movement_binding_material(
        source=source,
        source_assertion_coordinates=_source_assertion_coordinates(ledger, source),
        source_event=source_event,
        source_locality=source_event.locality_identity,
        destination_locality=binding.locality_identity,
        source_through_event_occurrence_identity=source_boundary,
        destination_through_event_occurrence_identity=destination_boundary,
        **identities,
    )
    if material != expected:
        raise ByteMeasurementError(
            "Assertion movement binding coordinates are not exact"
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
            "Assertion movement binding has no exact current coordinates"
        ) from error
    if not _source_assertion_is_carried(source_event, source_coordinates):
        raise ByteMeasurementError(
            "Assertion movement binding has no exact source coordinates"
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
            "Assertion movement binding has no exact destination coordinates"
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
            "Assertion movement binding order is false"
        ) from error
    return binding, source, source_event


def get_assertion_locality_movement_subject_to_act_binding(
    ledger: EventLedger, binding_event_identity: str
) -> Event:
    return _read_assertion_locality_movement_subject_to_act_binding(
        ledger, binding_event_identity
    )[0]


def _movement_act_material(binding: Event) -> dict[str, Any]:
    return {
        "act": "Assertion Locality movement",
        "subject_to_act_binding_reference": _movement_binding_reference(
            binding
        ),
        "movement_act_identity": binding.material["movement_act_identity"],
        "movement_act_occurrence_identity": binding.material[
            "movement_act_occurrence_identity"
        ],
        "source_assertion_reference": binding.material[
            "source_assertion_reference"
        ],
        "source_locality": binding.material["source_locality"],
        "destination_locality": binding.locality_identity,
        "locality_relation": {
            "first_subject": binding.material["source_assertion_reference"],
            "second_subject": binding.locality_identity,
            "relation_occurrence_identity": binding.material[
                "movement_act_occurrence_identity"
            ],
        },
    }


def record_assertion_locality_movement_act_occurrence(
    ledger: EventLedger,
    *,
    subject_to_act_binding_event_identity: str,
    current_coordinates: dict[str, Any],
) -> Event:
    binding, _source, _source_event = (
        _read_assertion_locality_movement_subject_to_act_binding(
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
        ASSERTION_LOCALITY_MOVEMENT_ACT_OCCURRENCE_EVENT,
    ):
        if prior.material.get("subject_to_act_binding_reference") == (
            _movement_binding_reference(binding)
        ):
            raise ByteMeasurementError(
                "Assertion movement binding already carries an Act"
            )
    return ledger.append(
        ASSERTION_LOCALITY_MOVEMENT_ACT_OCCURRENCE_EVENT,
        _movement_act_material(binding),
        locality_identity=binding.locality_identity,
    )


def _record_assertion_locality_movement_act_from_current_coordinates(
    ledger: EventLedger,
    *,
    binding: Event,
    destination_coordinates: dict[str, Any],
) -> Event:
    try:
        _require_exact_movement_binding_and_source(ledger, binding)
    except (ByteMeasurementError, TypeError, ValueError) as error:
        raise ByteMeasurementError(
            "Assertion movement Act requires an exact source and binding"
        ) from error
    if (
        binding.kind
        != ASSERTION_LOCALITY_MOVEMENT_SUBJECT_TO_ACT_BINDING_KIND
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
            "Assertion movement Act requires exact carried binding coordinates"
        )
    return ledger.append(
        ASSERTION_LOCALITY_MOVEMENT_ACT_OCCURRENCE_EVENT,
        _movement_act_material(binding),
        locality_identity=binding.locality_identity,
    )


def _read_assertion_locality_movement_act_occurrence(
    ledger: EventLedger,
    act_occurrence_event_identity: str,
    *,
    prior_destination_coordinates: dict[str, Any] | None = None,
) -> tuple[Event, Event, dict[str, Any]]:
    act = ledger.get(act_occurrence_event_identity)
    if (
        act is None
        or act.kind != ASSERTION_LOCALITY_MOVEMENT_ACT_OCCURRENCE_EVENT
        or ledger.integrity_of(act.identity) == CORRUPTED
    ):
        raise ByteMeasurementError("Assertion movement Act occurrence is absent or corrupted")
    reference = act.material.get("subject_to_act_binding_reference")
    if type(reference) is not dict:
        raise ByteMeasurementError("Assertion movement Act carries no exact binding")
    binding, source, _source_event = (
        _read_assertion_locality_movement_subject_to_act_binding(
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
        raise ByteMeasurementError("Assertion movement Act occurrence is not exact")
    try:
        ledger.occurrences_in_append_order(
            (binding.identity, act.identity),
            locality_identity=binding.locality_identity,
        )
    except ValueError as error:
        raise ByteMeasurementError("Assertion movement Act order is false") from error
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
        "source_assertion_reference": binding.material[
            "source_assertion_reference"
        ],
        "source_assertion_coordinates": binding.material[
            "source_assertion_coordinates"
        ],
        "source_locality": binding.material["source_locality"],
        "destination_locality": binding.locality_identity,
        "locality_relation": {
            "first_subject": binding.material["source_assertion_reference"],
            "second_subject": binding.locality_identity,
            "relation_occurrence_identity": binding.material[
                "movement_act_occurrence_identity"
            ],
        },
    }


def record_assertion_locality_movement_result(
    ledger: EventLedger, *, act_occurrence_event_identity: str
) -> Event:
    act, binding, _source = _read_assertion_locality_movement_act_occurrence(
        ledger, act_occurrence_event_identity
    )
    for kind in (
        RECORDED_YIELD_RELATION_EVENT,
        ASSERTION_LOCALITY_MOVEMENT_KIND,
    ):
        for prior in ledger.iter_locality_kind(binding.locality_identity, kind):
            if prior.material.get("act_occurrence_event_identity") == act.identity:
                raise ByteMeasurementError(
                    "Assertion movement Act already carries a Yield or result"
                )
    return _append_assertion_locality_movement_result(
        ledger, act=act, binding=binding
    )


def _append_assertion_locality_movement_result(
    ledger: EventLedger, *, act: Event, binding: Event
) -> Event:
    result_material = _movement_result_material(binding)
    yield_relation = _record_yield_relation(
        ledger,
        locality_identity=binding.locality_identity,
        exact_act="Assertion Locality movement",
        act_occurrence_identity=binding.material[
            "movement_act_occurrence_identity"
        ],
        act_occurrence_event_identity=act.identity,
        result_kind=ASSERTION_LOCALITY_MOVEMENT_RESULT_KIND,
        result_identity=binding.material["movement_result_identity"],
        result_content=result_material,
        occurrence_boundary="assertion_locality_movement",
        yielding_act_occurrence_coordinate="movement_act_occurrence_identity",
        coordinates_of_recorded_result={key: (key,) for key in result_material},
    )
    _require_exact_movement_binding_and_source(ledger, binding)
    if (
        ledger.get(act.identity) != act
        or ledger.integrity_of(act.identity) == CORRUPTED
        or act.material != _movement_act_material(binding)
        or ledger.get(yield_relation.identity) != yield_relation
        or ledger.integrity_of(yield_relation.identity) == CORRUPTED
        or ledger.append_boundary_through_occurrence(yield_relation.identity)
        != ledger.append_boundary()
    ):
        raise ByteMeasurementError(
            "Assertion movement result requires exact source, Act, and Yield relation"
        )
    return ledger.append(
        ASSERTION_LOCALITY_MOVEMENT_KIND,
        {
            **_movement_result_material(binding),
            "act_occurrence_event_identity": act.identity,
            "yield_relation_identity": yield_relation.identity,
        },
        locality_identity=binding.locality_identity,
    )


def _record_assertion_locality_movement_result_from_current_coordinates(
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
                "Assertion movement result requires an exact source and Act"
            ) from error
        if act.material != _movement_act_material(binding):
            raise ByteMeasurementError(
                "Assertion movement result requires an exact source and Act"
            )
    if (
        ledger.get(act.identity) != act
        or act.kind != ASSERTION_LOCALITY_MOVEMENT_ACT_OCCURRENCE_EVENT
        or ledger.integrity_of(act.identity) == CORRUPTED
        or act.locality_identity != binding.locality_identity
        or act.material != _movement_act_material(binding)
        or ledger.append_boundary_through_occurrence(act.identity)
        != ledger.append_boundary()
    ):
        raise ByteMeasurementError(
            "Assertion movement result requires its exact carried Act at the current append boundary"
        )
    return _append_assertion_locality_movement_result(
        ledger, act=act, binding=binding
    )


def _move_byte_assertion_to_locality(
    ledger: EventLedger,
    *,
    source: dict[str, Any],
    destination_locality: str,
) -> dict[str, Any]:
    """Preserve one Assertion movement without copying the Assertion."""

    source_event = ledger.get(source["recorded_occurrence_identity"])
    if source_event is None:
        raise ByteMeasurementError("Assertion locality movement requires its source")
    if source_event.locality_identity == destination_locality:
        return source
    from seed_runtime.operator_current_coordinates import read_operator_current_coordinates

    binding = record_assertion_locality_movement_subject_to_act_binding(
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
    act = record_assertion_locality_movement_act_occurrence(
        ledger,
        subject_to_act_binding_event_identity=binding.identity,
        current_coordinates=read_operator_current_coordinates(
            ledger, locality_identity=destination_locality
        ),
    )
    movement = record_assertion_locality_movement_result(
        ledger, act_occurrence_event_identity=act.identity
    )
    exact = _validate_moved_byte_assertion(ledger, movement.identity)
    if exact is None:
        raise ByteMeasurementError("Assertion locality movement is absent")
    return exact


def move_recorded_byte_assertion_to_locality(
    ledger: EventLedger,
    *,
    source: dict[str, Any],
    destination_locality: str,
) -> dict[str, Any]:
    return _move_byte_assertion_to_locality(
        ledger,
        source=source,
        destination_locality=destination_locality,
    )


def _move_assertion_reference_to_locality(
    ledger: EventLedger,
    *,
    source_assertion_reference: dict[str, str],
    destination_locality: str,
) -> dict[str, Any]:
    """Carry one exact supported Assertion through one 03.Movement.A occurrence."""

    source, source_event = _source_assertion_from_reference(
        ledger, source_assertion_reference
    )
    if source_event.kind == BYTE_MEASUREMENT_RECORDED_KIND:
        raise ByteMeasurementError(
            "this movement road requires a position or path-comparison Assertion"
        )
    if source_event.locality_identity == destination_locality:
        raise ByteMeasurementError("same-Locality Assertion requires no movement")
    from seed_runtime.operator_current_coordinates import (
        _carry_assertion_locality_movement_act_into_current_coordinates,
        _carry_assertion_locality_movement_binding_into_current_coordinates,
        _carry_assertion_locality_movement_result_into_current_coordinates,
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
        _carry_assertion_locality_movement_binding_into_current_coordinates(
            ledger,
            destination_coordinates,
            binding,
            source=source,
            source_event=source_event,
            source_current_coordinates=source_coordinates,
        )
    )
    act = _record_assertion_locality_movement_act_from_current_coordinates(
        ledger,
        binding=binding,
        destination_coordinates=destination_coordinates,
    )
    destination_coordinates = _carry_assertion_locality_movement_act_into_current_coordinates(
        ledger,
        destination_coordinates,
        act,
        binding=binding,
    )
    movement = _record_assertion_locality_movement_result_from_current_coordinates(
        ledger,
        act=act,
        binding=binding,
        destination_coordinates=destination_coordinates,
    )
    _destination_coordinates, carried = (
        _carry_assertion_locality_movement_result_into_current_coordinates(
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
            "Assertion Locality movement carries no exact result"
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
        or not _source_assertion_is_carried(source_event, source_coordinates)
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
            "Assertion movement binding requires exact current source and destination coordinates"
    )
    identities = {
        "movement_act_identity": ledger.mint_identity("assertion_locality_movement_act"),
        "movement_act_occurrence_identity": ledger.mint_identity(
            "assertion_locality_movement_occurrence"
        ),
        "movement_result_identity": ledger.mint_identity(
            "assertion_locality_movement_result"
        ),
    }
    if len(set(identities.values())) != len(identities):
        raise ByteMeasurementError("Assertion movement lifecycle identities collapsed")
    return ledger.append(
        ASSERTION_LOCALITY_MOVEMENT_SUBJECT_TO_ACT_BINDING_KIND,
        _movement_binding_material(
            source=source,
            source_assertion_coordinates=_source_assertion_coordinates(ledger, source),
            source_event=source_event,
            source_locality=source_event.locality_identity,
            destination_locality=destination_locality,
            source_through_event_occurrence_identity=source_boundary,
            destination_through_event_occurrence_identity=destination_boundary,
            **identities,
        ),
        locality_identity=destination_locality,
    )


def move_recorded_byte_assertions_to_locality(
    ledger: EventLedger,
    *,
    sources: tuple[dict[str, Any], ...],
    destination_locality: str,
) -> tuple[dict[str, Any], ...]:
    """Move one exact result's Assertions in one bounded same-call lifecycle."""

    if not sources:
        return ()
    source_event_identity = sources[0]["recorded_occurrence_identity"]
    if any(
        source["recorded_occurrence_identity"] != source_event_identity
        for source in sources
    ):
        raise ByteMeasurementError(
            "bounded Assertion movement requires one exact source result"
        )
    source_event = ledger.get(source_event_identity)
    if source_event is None or source_event.locality_identity is None:
        raise ByteMeasurementError("Assertion locality movement requires its source")
    if source_event.locality_identity == destination_locality:
        return sources
    exact_sources = {
        source["assertion_position"]: _byte_result_position(
            ledger,
            source_event_identity,
            source["assertion_position"],
        )
        for source in sources
    }
    if any(
        exact_sources.get(source["assertion_position"]) != source
        for source in sources
    ):
        raise ByteMeasurementError(
            "bounded Assertion movement requires each exact source Assertion"
        )
    from seed_runtime.operator_current_coordinates import (
        _carry_assertion_locality_movement_act_into_current_coordinates,
        _carry_assertion_locality_movement_binding_into_current_coordinates,
        _carry_assertion_locality_movement_result_into_current_coordinates,
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
            _carry_assertion_locality_movement_binding_into_current_coordinates(
                ledger,
                destination_coordinates,
                binding,
                source=source,
                source_event=source_event,
                source_current_coordinates=source_coordinates,
            )
        )
        act = _record_assertion_locality_movement_act_from_current_coordinates(
            ledger,
            binding=binding,
            destination_coordinates=destination_coordinates,
        )
        destination_coordinates = _carry_assertion_locality_movement_act_into_current_coordinates(
            ledger,
            destination_coordinates,
            act,
            binding=binding,
        )
        movement = _record_assertion_locality_movement_result_from_current_coordinates(
            ledger,
            act=act,
            binding=binding,
            destination_coordinates=destination_coordinates,
        )
        destination_coordinates, exact = (
            _carry_assertion_locality_movement_result_into_current_coordinates(
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


def _assertion_carried_by_locality_movement_result(
    *,
    movement: Event,
    binding: Event,
    source: dict[str, Any],
) -> dict[str, Any]:
    """Carry the source Assertion with one exact movement result."""

    if (
        movement.material.get("subject_to_act_binding_reference")
        != _movement_binding_reference(binding)
        or binding.material.get("source_assertion_reference")
        != _source_assertion_reference(source)
        or movement.material.get("source_assertion_reference")
        != _source_assertion_reference(source)
    ):
        raise ByteMeasurementError(
            "Assertion locality movement carries no exact source"
        )
    return {
        **_byte_result_position_reference(source),
        "locality_movement_event_identity": movement.identity,
    }


def _validate_moved_byte_assertion(
    ledger: EventLedger,
    movement_event_identity: str,
    *,
    prior_destination_coordinates: dict[str, Any] | None = None,
) -> dict[str, Any] | None:
    movement = ledger.get(movement_event_identity)
    if movement is None or movement.kind != ASSERTION_LOCALITY_MOVEMENT_KIND:
        return None
    if ledger.integrity_of(movement.identity) == CORRUPTED:
        raise ByteMeasurementError("Assertion locality movement is corrupted")
    act_occurrence, binding, source = (
        _read_assertion_locality_movement_act_occurrence(
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
            "Assertion locality movement carries no exact binding"
        )
    requirements = read_requirements_of_yield_relation(
        ledger,
        recorded_result_event_identity=movement.identity,
        yield_relation_event_identity=movement.material.get("yield_relation_identity"),
            act_occurrence_event_identity=movement.material.get(
                "act_occurrence_event_identity"
            ),
        recorded_result_occurrence_coordinate="movement_act_occurrence_identity",
        yielding_act_occurrence_coordinate="movement_act_occurrence_identity",
    )
    yield_relation = ledger.get(
        movement.material.get("yield_relation_identity")
    )
    if (
        not all(requirements.values())
        or yield_relation is None
        or yield_relation.material.get("result_kind")
        != ASSERTION_LOCALITY_MOVEMENT_RESULT_KIND
        or yield_relation.material.get("occurrence_boundary")
        != "assertion_locality_movement"
    ):
        raise ByteMeasurementError("Assertion movement Yield relation is not exact")
    expected = {
        **_movement_result_material(binding),
        "act_occurrence_event_identity": act_occurrence.identity,
        "yield_relation_identity": movement.material.get(
            "yield_relation_identity"
        ),
    }
    if movement.material != expected:
        raise ByteMeasurementError("Assertion locality movement is not exact")
    return _assertion_carried_by_locality_movement_result(
        movement=movement,
        binding=binding,
        source=source,
    )


def _measure_byte_position_pair_counts_through(
    ledger: EventLedger,
    *,
    localities: tuple[str, ...],
    boundary: EventLedgerBoundary,
    source_assertion_reference: dict[str, str],
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
        source_assertion_reference=source_assertion_reference,
        source_movement_event_identity=source_movement_event_identity,
        input_applicability=input_applicability,
        addressed_act_identity=addressed_act_identity,
        act_occurrence_identity=act_occurrence_identity,
        counts=counts,
    )


def _assertions(measured: MeasuredByteInputs) -> list[dict[str, Any]]:
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
            "assertion_subject": source_subject,
        }
    ]

    def assertion(
        *,
        result: str,
        item: MeasuredByteCount,
        content: dict[str, Any],
        referenced_assertion_positions: list[int],
    ):
        subject = {"content": item.content}
        position = len(results)
        return {
            "dimensions": {
                "position": position,
                "content": content,
            },
            "result": result,
            "assertion_subject": subject,
            "referenced_assertion_positions": referenced_assertion_positions,
        }

    for item in measured.counts:
        count_content = {
            "input_count": len(measured.source_material),
            "occurrences_carrying": item.occurrences_carrying,
            "count": item.count,
        }
        count = assertion(
            result="count",
            item=item,
            content=count_content,
            referenced_assertion_positions=[0],
        )
        results.append(count)
        if item.count > 1:
            results.append(
                assertion(
                    result="recurrence",
                    item=item,
                    content={"recurrence_established": True},
                    referenced_assertion_positions=[count["dimensions"]["position"]],
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
                "byte Measurement binding already carries an Act"
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
            "byte Measurement Yield requires one exact Act occurrence"
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
    for kind in (
        RECORDED_YIELD_RELATION_EVENT,
        BYTE_MEASUREMENT_RECORDED_KIND,
    ):
        for event in ledger.iter_locality_kind(act_occurrence.locality_identity, kind):
            if (
                event.material.get("act_occurrence_event_identity")
                == act_occurrence.identity
            ):
                raise ByteMeasurementError(
                    "byte Measurement Act occurrence already has a Yield or result"
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
                    "exact source material, byte count, and same-content Assertions"
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
        "assertions": _assertions(measured),
    }
    yield_relation = _record_yield_relation(
        ledger,
        locality_identity=act_occurrence.locality_identity,
        exact_act="declared exact-byte Measurement",
        act_occurrence_identity=act_occurrence.material[
            "act_occurrence_identity"
        ],
        act_occurrence_event_identity=act_occurrence.identity,
        result_kind=BYTE_MEASUREMENT_RESULT_KIND,
        result_identity=result_identity,
        result_content=result_material,
        occurrence_boundary="byte_measurement",
    )
    return ledger.append(
        BYTE_MEASUREMENT_RECORDED_KIND,
        {
            **result_material,
            "yield_relation_identity": yield_relation.identity,
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
    """Record the Yield and result of one exact recorded byte Measurement Act."""

    supplied = ledger.get(act_occurrence_event_identity)
    if (
        supplied is None
        or supplied.kind != BYTE_MEASUREMENT_ACT_OCCURRENCE_EVENT
        or ledger.integrity_of(supplied.identity) == CORRUPTED
    ):
        raise ByteMeasurementError(
            "byte Measurement Yield requires one exact Act occurrence"
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


def _assertions_of_recorded_byte_measurement(
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
        "yield_relation_identity",
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
                "content": (
                    "exact source material, byte count, and same-content Assertions"
                ),
        }
    ):
        raise ByteMeasurementError(
            f"{event_identity} does not preserve its exact Measurement and "
            "Yield relation"
        )
    yield_relation_identity = material.get("yield_relation_identity")
    yield_relation = ledger.get(yield_relation_identity) if isinstance(yield_relation_identity, str) else None
    if (
        yield_relation is None
        or yield_relation.kind != RECORDED_YIELD_RELATION_EVENT
        or ledger.integrity_of(yield_relation.identity) == CORRUPTED
        or yield_relation.material.get("result_kind")
        != BYTE_MEASUREMENT_RESULT_KIND
        or yield_relation.material.get("coordinates_of_carried_result")
        != [coordinate for coordinate in material if coordinate in BYTE_RESULT_COORDINATES]
        or yield_relation.material.get("dimensions", {}).get("act_occurrence_identity")
        != material["act_occurrence_identity"]
    ):
        raise ByteMeasurementError(
            f"{event_identity} names no exact byte Measurement Yield relation"
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
    _require_exact_result_yield(
        ledger,
        event,
        yield_relation,
        act_occurrence,
        result_name="byte Measurement",
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
        or measured.completeness_boundary.identity != boundary_value["identity"]
        or list(measured.source_localities) != localities_value
    ):
        raise ByteMeasurementError(
            f"{event_identity} does not establish its Seed-native Measurement boundary"
        )
    recorded_assertions = material.get("assertions")
    if type(recorded_assertions) is not list:
        raise ByteMeasurementError(
            f"{event_identity} does not carry the results of its complete bounded source read"
        )
    try:
        expected = _assertions(measured)
    except (KeyError, TypeError, ByteMeasurementError) as error:
        raise ByteMeasurementError(
            f"{event_identity} does not carry the results of its complete bounded source read"
        ) from error
    if recorded_assertions != expected:
        raise ByteMeasurementError(
            f"{event_identity} does not carry the results of its complete bounded source read"
        )
    return tuple(deepcopy(assertion) for assertion in expected)


def assertions_of_recorded_byte_measurement(
    ledger: EventLedger,
    event_identity: str,
    *,
    prior_coordinates: dict[str, Any] | None = None,
) -> tuple[dict[str, Any], ...] | None:
    """Read the exact byte results after replaying their bounded source read."""

    return _assertions_of_recorded_byte_measurement(
        ledger,
        event_identity,
        prior_coordinates=prior_coordinates,
    )


def _byte_result_position(
    ledger: EventLedger,
    event_identity: str,
    assertion_position: int,
    *,
    prior_coordinates: dict[str, Any] | None = None,
) -> dict[str, Any] | None:
    """Resolve one exact result occurrence and result-local position."""

    assertions = _assertions_of_recorded_byte_measurement(
        ledger,
        event_identity,
        prior_coordinates=prior_coordinates,
    )
    if assertions is None:
        return None
    assertion = next(
        (
            item
            for item in assertions
            if item["dimensions"]["position"] == assertion_position
        ),
        None,
    )
    if assertion is None:
        return None
    return {
        "recorded_occurrence_identity": event_identity,
        "assertion_position": assertion_position,
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
    assertions = _assertions_of_recorded_byte_measurement(
        ledger,
        reference["recorded_occurrence_identity"],
        prior_coordinates=source_coordinates,
    )
    assertion = next(
        (
            item
            for item in assertions or ()
            if item["dimensions"]["position"] == reference["assertion_position"]
        ),
        None,
    )
    if event is None or assertion is None:
        raise ByteMeasurementError("byte result position is absent")
    return event, assertion, tuple(event.material["source_localities"])


def _pair_assertions(measured: MeasuredBytePairInputs) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []

    def assertion(
        *,
        result: str,
        item: MeasuredBytePairCount,
        content: dict[str, Any],
        referenced_assertion_positions: list[int],
        referenced_assertions: list[dict[str, Any]],
    ) -> dict[str, Any]:
        subject = {"content": list(item.content)}
        position = len(results)
        return {
            "dimensions": {
                "position": position,
                "content": content,
            },
            "result": result,
            "assertion_subject": subject,
            "referenced_assertions": referenced_assertions,
            "referenced_assertion_positions": referenced_assertion_positions,
        }

    for item in measured.counts:
        count = assertion(
            result="count",
            item=item,
            content={
                "input_count": len(measured.source_material),
                "occurrences_carrying": item.occurrences_carrying,
                "count": item.count,
            },
            referenced_assertion_positions=[],
            referenced_assertions=[measured.source_assertion_reference],
        )
        results.append(count)
        if item.count > 1:
            results.append(
                assertion(
                    result="recurrence",
                    item=item,
                    content={"recurrence_established": True},
                    referenced_assertion_positions=[count["dimensions"]["position"]],
                    referenced_assertions=[],
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
        "source_assertion_reference": _byte_result_position_reference(source),
        "subject_reference": {
            "input_assertion_reference": _byte_result_position_reference(source),
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
    return binding.material.get("source_assertion_reference")


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
            "assertion_locality_movement_occurrences"
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
                reference.get("assertion_position"),
                prior_coordinates=prior_coordinates,
            )
            if type(reference) is dict
            else None
        )
    elif type(movement_identity) is str and movement_identity:
        source = _validate_moved_byte_assertion(ledger, movement_identity)
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
        "input_assertion_reference": _byte_result_position_reference(source),
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
    applicability_assertion: dict[str, Any],
) -> dict[str, Any]:
    return {
        "result_identity": binding.material["applicability_result_identity"],
        "dimensions": {
            "identity": applicability_assertion["dimensions"]["identity"],
            "content": "exact source-Assertion to addressed-Act Applicability",
            "applicability": applicability_assertion["dimensions"]["applicability"],
        },
        "exact_act": "input Applicability",
        "subject_to_act_binding_reference": (
            _pair_subject_to_act_binding_reference(binding)
        ),
        "applicability_act_identity": applicability_assertion["applicability_act_identity"],
        "applicability_act_occurrence_identity": applicability_assertion[
            "applicability_act_occurrence_identity"
        ],
        "addressed_act_identity": applicability_assertion["addressed_act_identity"],
        "input_assertion_reference": _byte_result_position_reference(source),
        "input_movement_event_identity": _byte_result_position_movement_identity(source),
        "applicability": applicability_assertion,
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
        "yield_relation_identity": event.material.get(
            "yield_relation_identity"
        ),
        "act_occurrence_event_identity": applicability_act_occurrence.identity,
    }
    yield_relation = ledger.get(event.material.get("yield_relation_identity"))
    try:
        requirements = read_requirements_of_yield_relation(
            ledger,
            recorded_result_event_identity=event.identity,
            yield_relation_event_identity=(
                event.material.get("yield_relation_identity")
            ),
            act_occurrence_event_identity=applicability_act_occurrence.identity,
            recorded_result_occurrence_coordinate=(
                "applicability_act_occurrence_identity"
            ),
            yielding_act_occurrence_coordinate=(
                "applicability_act_occurrence_identity"
            ),
        )
    except (TypeError, ValueError):
        requirements = {}
    if (
        type(event) is not Event
        or ledger.get(event.identity) != event
        or event.kind != BYTE_PAIR_APPLICABILITY_RECORDED_KIND
        or event.locality_identity != binding.locality_identity
        or ledger.integrity_of(event.identity) == CORRUPTED
        or event.material != expected_material
        or yield_relation is None
        or yield_relation.kind != RECORDED_YIELD_RELATION_EVENT
        or yield_relation.locality_identity != event.locality_identity
        or ledger.integrity_of(yield_relation.identity) == CORRUPTED
        or yield_relation.material.get("result_kind")
        != BYTE_PAIR_APPLICABILITY_RESULT_KIND
        or yield_relation.material.get("occurrence_boundary")
        != "byte_pair_applicability"
        or not all(requirements.values())
        or not _yield_immediately_precedes_result(ledger, yield_relation, event)
    ):
        raise ByteMeasurementError("pair Applicability result is not exact")
    return expected_applicability


def _record_pair_input_applicability_result_from_carried_act(
    ledger: EventLedger,
    *,
    binding: Event,
    source: dict[str, Any],
    applicability_act_occurrence: Event,
    applicability_assertion: dict[str, Any],
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
        applicability_assertion != expected_applicability
        or ledger.append_boundary_through_occurrence(
            applicability_act_occurrence.identity
        )
        != ledger.append_boundary()
    ):
        raise ByteMeasurementError(
            "pair Applicability result requires its exact Act at the current append boundary"
        )
    result_material = _pair_applicability_result_material(
        binding, source, applicability_assertion
    )
    yield_relation = _record_yield_relation(
        ledger,
        locality_identity=binding.locality_identity,
        exact_act="input Applicability",
        act_occurrence_identity=binding.material[
            "applicability_act_occurrence_identity"
        ],
        act_occurrence_event_identity=applicability_act_occurrence.identity,
        result_kind=BYTE_PAIR_APPLICABILITY_RESULT_KIND,
        result_identity=binding.material["applicability_result_identity"],
        result_content=result_material,
        occurrence_boundary="byte_pair_applicability",
        yielding_act_occurrence_coordinate="applicability_act_occurrence_identity",
    )
    if (
        ledger.get(yield_relation.identity) != yield_relation
        or ledger.integrity_of(yield_relation.identity) == CORRUPTED
        or ledger.append_boundary_through_occurrence(yield_relation.identity)
        != ledger.append_boundary()
    ):
        raise ByteMeasurementError(
            "pair Applicability result requires its exact Yield at the current append boundary"
        )
    recorded_material = {
        **_pair_applicability_result_material(
            binding, source, applicability_assertion
        ),
        "yield_relation_identity": yield_relation.identity,
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
        "yield_relation_identity",
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
        "input_assertion_reference": _byte_result_position_reference(source),
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
) -> tuple[Event, Event, dict[str, Any], Event]:
    event = ledger.get(event_identity)
    if (
        event is None
        or event.kind != BYTE_PAIR_MEASUREMENT_ACT_OCCURRENCE_EVENT
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise ByteMeasurementError(
            "pair Measurement Act occurrence is absent or corrupted"
        )
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
            "content": "byte-position-pair count and same-content Assertions",
        },
        "exact_act": "declared byte-position-pair Measurement",
        "addressed_act_identity": binding.material["exact_act_identity"],
        "act_occurrence_identity": binding.material[
            "measurement_act_occurrence_identity"
        ],
        "subject_to_act_binding_reference": (
            _pair_subject_to_act_binding_reference(binding)
        ),
        "source_assertion_reference": measured.source_assertion_reference,
        "source_movement_event_identity": measured.source_movement_event_identity,
        "input_applicability": measured.input_applicability,
        "input_applicability_event_identity": applicability_event.identity,
        "source_localities": list(measured.source_localities),
        "completeness_boundary": {
            "identity": measured.completeness_boundary.identity
        },
        "assertions": _pair_assertions(measured),
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
        source_assertion_reference=_byte_result_position_reference(source),
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
    result_material = _pair_measurement_result_material(
        measured,
        binding=binding,
        applicability_event=applicability_event,
    )
    yield_relation = _record_yield_relation(
        ledger,
        locality_identity=binding.locality_identity,
        exact_act="declared byte-position-pair Measurement",
        act_occurrence_identity=binding.material[
            "measurement_act_occurrence_identity"
        ],
        act_occurrence_event_identity=act_occurrence.identity,
        result_kind=BYTE_PAIR_MEASUREMENT_RESULT_KIND,
        result_identity=binding.material["measurement_result_identity"],
        result_content=result_material,
        occurrence_boundary="byte_pair_measurement",
    )
    if (
        ledger.get(yield_relation.identity) != yield_relation
        or ledger.integrity_of(yield_relation.identity) == CORRUPTED
        or ledger.append_boundary_through_occurrence(yield_relation.identity)
        != ledger.append_boundary()
    ):
        raise ByteMeasurementError(
            "pair Measurement result requires its exact Yield at the current append boundary"
        )
    recorded_material = {
        **_pair_measurement_result_material(
            measured,
            binding=binding,
            applicability_event=applicability_event,
        ),
        "yield_relation_identity": yield_relation.identity,
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
        source_assertion_reference=_byte_result_position_reference(source),
        source_movement_event_identity=_byte_result_position_movement_identity(source),
        input_applicability=applicability_event.material["applicability"],
        addressed_act_identity=binding.material["exact_act_identity"],
        act_occurrence_identity=binding.material[
            "measurement_act_occurrence_identity"
        ],
    )
    yield_relation = ledger.get(event.material.get("yield_relation_identity"))
    expected = {
        **_pair_measurement_result_material(
            measured,
            binding=binding,
            applicability_event=applicability_event,
        ),
        "yield_relation_identity": (
            event.material.get("yield_relation_identity")
        ),
        "act_occurrence_event_identity": act_occurrence.identity,
        "occurrence_preservation": BYTE_PAIR_OCCURRENCE_PRESERVATION,
    }
    try:
        requirements = read_requirements_of_yield_relation(
            ledger,
            recorded_result_event_identity=event.identity,
            yield_relation_event_identity=(
                event.material.get("yield_relation_identity")
            ),
            act_occurrence_event_identity=act_occurrence.identity,
        )
    except (TypeError, ValueError):
        requirements = {}
    if (
        type(event) is not Event
        or ledger.get(event.identity) != event
        or event.kind != BYTE_PAIR_MEASUREMENT_RECORDED_KIND
        or event.locality_identity != binding.locality_identity
        or ledger.integrity_of(event.identity) == CORRUPTED
        or event.material != expected
        or yield_relation is None
        or yield_relation.kind != RECORDED_YIELD_RELATION_EVENT
        or yield_relation.locality_identity != event.locality_identity
        or ledger.integrity_of(yield_relation.identity) == CORRUPTED
        or yield_relation.material.get("result_kind") != BYTE_PAIR_MEASUREMENT_RESULT_KIND
        or yield_relation.material.get("occurrence_boundary") != "byte_pair_measurement"
        or not all(requirements.values())
        or not _yield_immediately_precedes_result(ledger, yield_relation, event)
    ):
        raise ByteMeasurementError(
            "pair Measurement result or Yield is not exact"
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
        _carry_pair_applicability_act_into_current_coordinates,
        _carry_pair_applicability_result_into_current_coordinates,
        _carry_pair_measurement_act_into_current_coordinates,
        _carry_pair_applicability_binding_into_current_coordinates,
        _carry_pair_measurement_binding_into_current_coordinates,
        _carry_pair_measurement_result_into_current_coordinates,
    )

    boundary = _require_carried_pair_measurement_at_current_append_boundary(
        ledger,
        source=source,
        recording_locality_identity=recording_locality_identity,
        current_coordinates=current_coordinates,
    )
    lifecycle_identities = _new_pair_lifecycle_identities(ledger)
    applicability_binding = _append_pair_applicability_binding(
        ledger,
        source=source,
        source_localities=source_localities,
        content=content,
        recording_locality_identity=recording_locality_identity,
        through_event_occurrence_identity=boundary,
        identities=lifecycle_identities,
    )
    current_coordinates = _carry_pair_applicability_binding_into_current_coordinates(
        ledger,
        current_coordinates,
        applicability_binding,
        source,
        prior_through_event_occurrence_identity=boundary,
    )
    measurement_binding = _append_pair_measurement_binding(
        ledger,
        source=source,
        source_localities=source_localities,
        content=content,
        recording_locality_identity=recording_locality_identity,
        through_event_occurrence_identity=applicability_binding.identity,
        identities=lifecycle_identities,
    )
    current_coordinates = _carry_pair_measurement_binding_into_current_coordinates(
        ledger,
        current_coordinates,
        measurement_binding,
        source,
        prior_through_event_occurrence_identity=applicability_binding.identity,
    )
    applicability = _pair_input_applicability(
        ledger,
        source,
        binding=applicability_binding,
        measurement_locality_identity=recording_locality_identity,
        prior_coordinates=current_coordinates,
    )
    applicability_act = (
        _record_pair_input_applicability_act_from_carried_binding(
            ledger,
            binding=applicability_binding,
            source=source,
            current_coordinates=current_coordinates,
        )
    )
    current_coordinates = _carry_pair_applicability_act_into_current_coordinates(
        ledger,
        current_coordinates,
        applicability_act,
        binding=applicability_binding,
        source=source,
        prior_through_event_occurrence_identity=measurement_binding.identity,
    )
    applicability_event = _record_pair_input_applicability_result_from_carried_act(
        ledger,
        binding=applicability_binding,
        source=source,
        applicability_act_occurrence=applicability_act,
        applicability_assertion=applicability,
        current_coordinates=current_coordinates,
    )
    current_coordinates = _carry_pair_applicability_result_into_current_coordinates(
        ledger,
        current_coordinates,
        applicability_event,
        binding=applicability_binding,
        source=source,
        applicability_act_occurrence=applicability_act,
        prior_through_event_occurrence_identity=applicability_act.identity,
    )
    if applicability["dimensions"]["applicability"] != "applicable":
        return applicability_event, current_coordinates
    act_occurrence = (
        _record_pair_measurement_act_from_carried_applicability(
            ledger,
            binding=measurement_binding,
            source=source,
            applicability_event=applicability_event,
            current_coordinates=current_coordinates,
        )
    )
    current_coordinates = _carry_pair_measurement_act_into_current_coordinates(
        ledger,
        current_coordinates,
        act_occurrence,
        binding=measurement_binding,
        source=source,
        applicability_event=applicability_event,
        applicability_act_occurrence=applicability_act,
        prior_through_event_occurrence_identity=applicability_event.identity,
    )
    result = _record_pair_measurement_result_from_carried_act(
        ledger,
        act_occurrence=act_occurrence,
        binding=measurement_binding,
        source=source,
        applicability_event=applicability_event,
        applicability_act_occurrence=applicability_act,
        current_coordinates=current_coordinates,
    )
    current_coordinates = _carry_pair_measurement_result_into_current_coordinates(
        ledger,
        current_coordinates,
        result,
        act_occurrence=act_occurrence,
        binding=measurement_binding,
        source=source,
        applicability_event=applicability_event,
        applicability_act_occurrence=applicability_act,
        prior_through_event_occurrence_identity=act_occurrence.identity,
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
    exact_surface = BYTE_PAIR_RESULT_COORDINATES | {
        "yield_relation_identity",
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
    if (
        binding_reference
        != _pair_subject_to_act_binding_reference(binding)
        or event.locality_identity != binding.locality_identity
        or material.get("result_identity")
        != binding.material["measurement_result_identity"]
        or material.get("source_assertion_reference")
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
        "content": (
            "byte-position-pair count and same-content Assertions"
        ),
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
            f"{event_identity} does not preserve its exact pair Measurement Assertion"
        )
    yield_relation_identity = material.get("yield_relation_identity")
    yield_relation = ledger.get(yield_relation_identity) if isinstance(yield_relation_identity, str) else None
    if (
        yield_relation is None
        or yield_relation.kind != RECORDED_YIELD_RELATION_EVENT
        or ledger.integrity_of(yield_relation.identity) == CORRUPTED
        or yield_relation.material.get("result_kind")
        != BYTE_PAIR_MEASUREMENT_RESULT_KIND
        or yield_relation.material.get("occurrence_boundary") != "byte_pair_measurement"
        or yield_relation.material.get("coordinates_of_carried_result")
        != [
            coordinate
            for coordinate in material
            if coordinate in BYTE_PAIR_RESULT_COORDINATES
        ]
        or yield_relation.material.get("dimensions", {}).get("act_occurrence_identity")
        != material["act_occurrence_identity"]
        or not _yield_immediately_precedes_result(ledger, yield_relation, event)
    ):
        raise ByteMeasurementError(
            f"{event_identity} names no exact byte-position-pair Yield relation"
        )
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
        raise ByteMeasurementError(f"{event_identity} carries no exact input Applicability")
    if (
        act_occurrence.material
        != _pair_measurement_act_material(binding, source, applicability_event)
    ):
        raise ByteMeasurementError(
            f"{event_identity} names no exact responsible pair Measurement Act occurrence"
        )
    _require_exact_result_yield(
        ledger,
        event,
        yield_relation,
        act_occurrence,
        result_name="byte-position-pair",
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
    source_reference = material.get("source_assertion_reference")
    if (
        not isinstance(source_reference, dict)
        or set(source_reference)
        != {"recorded_occurrence_identity", "assertion_position"}
        or not isinstance(source_reference["recorded_occurrence_identity"], str)
        or not source_reference["recorded_occurrence_identity"]
        or type(source_reference["assertion_position"]) is not int
        or source_reference["assertion_position"] < 0
    ):
        raise ByteMeasurementError(f"{event_identity} carries no exact source Assertion")
    if (
        _byte_result_position_reference(source) != source_reference
        or event.locality_identity is None
    ):
        raise ByteMeasurementError(
            f"{event_identity} does not carry its exact input source Assertion"
        )
    _source_event, source_material, source_localities = _read_byte_result_position(
        ledger, source, prior_coordinates=prior_coordinates
    )
    source_content = source_material["dimensions"]["content"]
    if (
        localities_value != list(source_localities)
        or boundary_value != source_content["completeness_boundary"]
        or binding.material.get("source_localities") != localities_value
        or binding.material.get("completeness_boundary_identity")
        != boundary_value["identity"]
    ):
        raise ByteMeasurementError(
            f"{event_identity} does not carry its exact input source boundary"
        )
    applicability_event_identity = material.get("input_applicability_event_identity")
    if (
        applicability_event_identity != applicability_event.identity
        or applicability_event.material.get("applicability")
        != material.get("input_applicability")
    ):
        raise ByteMeasurementError(
            f"{event_identity} does not name its exact recorded input Applicability"
        )
    assertions = material.get("assertions")
    if not isinstance(assertions, list):
        raise ByteMeasurementError(f"{event_identity} carries no pair result Assertions")
    by_pair: dict[tuple[int, int], dict[str, dict[str, Any]]] = {}
    exact_keys = {
        "dimensions",
        "result",
        "assertion_subject",
        "referenced_assertions",
        "referenced_assertion_positions",
    }
    for assertion_position, assertion in enumerate(assertions):
        if not isinstance(assertion, dict) or set(assertion) != exact_keys:
            raise ByteMeasurementError(f"{event_identity} carries a malformed pair Assertion")
        subject = assertion.get("assertion_subject")
        result = assertion.get("result")
        dimensions = assertion.get("dimensions")
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
            or dimensions.get("position") != assertion_position
        ):
            raise ByteMeasurementError(f"{event_identity} carries an unlawful pair Assertion")
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
        group[result] = assertion
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
            or count["referenced_assertions"] != [source_reference]
            or count["referenced_assertion_positions"] != []
        ):
            raise ByteMeasurementError(f"{event_identity} carries an unlawful pair count")
        recurrence = group.get("recurrence")
        if (recurrence is not None) != (count_content["count"] > 1):
            raise ByteMeasurementError(f"{event_identity} carries the wrong recurrence boundary")
        if recurrence is not None and (
            recurrence["dimensions"]["content"] != {"recurrence_established": True}
            or recurrence["referenced_assertions"] != []
            or recurrence["referenced_assertion_positions"]
            != [count["dimensions"]["position"]]
        ):
            raise ByteMeasurementError(
                f"{event_identity} carries an unlawful recurrence Assertion reference"
            )
    validated_results = []
    for assertion in assertions:
        if findings_only:
            content = assertion["dimensions"]["content"]
            content_coordinates: tuple[int, int, int] | bool
            if assertion["result"] == "recurrence":
                content_coordinates = content["recurrence_established"]
            else:
                content_coordinates = (
                    content["input_count"],
                    content["occurrences_carrying"],
                    content["count"],
                )
            validated_results.append(
                _RecordedBytePairFinding(
                    assertion_position=assertion["dimensions"]["position"],
                    recorded_occurrence_identity=event.identity,
                    exact_pair=tuple(
                        assertion["assertion_subject"]["content"]
                    ),
                    result=assertion["result"],
                    _content_coordinates=content_coordinates,
                    _referenced_assertion_positions=tuple(
                        assertion["referenced_assertion_positions"]
                    ),
                )
            )
            continue
        referenced_assertions = list(assertion["referenced_assertions"])
        referenced_assertions.extend(
            {
                "recorded_occurrence_identity": event.identity,
                "assertion_position": local_position,
            }
            for local_position in assertion["referenced_assertion_positions"]
        )
        validated_results.append(RecordedBytePairAssertion(
            assertion_position=assertion["dimensions"]["position"],
            recorded_occurrence_identity=event.identity,
            content=tuple(assertion["assertion_subject"]["content"]),
            result=assertion["result"],
            _material=deepcopy(assertion),
            _referenced_assertions=tuple(deepcopy(referenced_assertions)),
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
) -> tuple[RecordedBytePairAssertion, ...] | tuple[_RecordedBytePairFinding, ...] | None:
    reading = _validated_recorded_byte_position_pair_measurement(
        ledger,
        event_identity,
        findings_only=findings_only,
        prior_coordinates=prior_coordinates,
    )
    return reading.results if reading is not None else None


def assertions_of_recorded_byte_position_pair_measurement(
    ledger: EventLedger,
    event_identity: str,
    *,
    prior_coordinates: dict[str, Any] | None = None,
) -> tuple[RecordedBytePairAssertion, ...] | None:
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
    """Return the exact ordered Applicability and Measurement occurrences."""

    assertions = assertions_of_recorded_byte_position_pair_measurement(
        ledger, event_identity
    )
    if type(assertions) is not tuple:
        raise ByteMeasurementError("pair Measurement result is absent")
    result = ledger.get(event_identity)
    assert result is not None
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
    """Validate the exact input-to-Act Applicability Assertion."""

    read = assertions_of_recorded_byte_position_pair_measurement(ledger, event_identity)
    if read is None:
        return None
    event = ledger.get(event_identity)
    return deepcopy(event.material["input_applicability"])
