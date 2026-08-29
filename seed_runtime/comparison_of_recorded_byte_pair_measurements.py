"""Comparison of earlier and later recorded byte-pair Measurements."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from seed_runtime.byte_measurement import (
    BYTE_PAIR_MEASUREMENT_RECORDED_KIND,
    _RecordedBytePairFinding,
    _read_pair_measurement_subject_to_act_binding,
    _validated_recorded_byte_position_pair_measurement,
    result_positions_of_recorded_byte_measurement,
)
from seed_runtime.event import Event
from seed_runtime.events import CORRUPTED, EventLedger
from seed_runtime.material_source import read_exact_material_result
from seed_runtime.operator_material_source import (
    OPERATOR_MATERIAL_SOURCE_RECORDED_KIND,
)
from seed_runtime.operator_destination_locality import (
    OPERATOR_DESTINATION_LOCALITY_RECORDED_KIND,
    get_recorded_operator_destination_locality,
)
from seed_runtime.witness_material_source import WITNESS_MATERIAL_SOURCE_RECORDED_KIND


RECORDED_PAIR_MEASUREMENT_COMPARISON_SUBJECT_TO_ACT_BINDING_KIND = (
    "recorded_pair_measurement_comparison.subject_to_act_binding_recorded"
)
RECORDED_PAIR_MEASUREMENT_COMPARISON_APPLICABILITY_SUBJECT_TO_ACT_BINDING_KIND = (
    "recorded_pair_measurement_comparison."
    "applicability_subject_to_act_binding_recorded"
)
RECORDED_PAIR_MEASUREMENT_COMPARISON_APPLICABILITY_ACT_OCCURRENCE_EVENT = (
    "recorded_pair_measurement_comparison.applicability_act_occurrence_recorded"
)
RECORDED_PAIR_MEASUREMENT_COMPARISON_APPLICABILITY_RESULT_KIND = (
    "recorded_pair_measurement_comparison.applicability_recorded"
)
RECORDED_PAIR_MEASUREMENT_COMPARISON_ACT_OCCURRENCE_EVENT = (
    "recorded_pair_measurement_comparison.act_occurrence_recorded"
)
RECORDED_PAIR_MEASUREMENT_COMPARISON_RESULT_KIND = (
    "recorded_pair_measurement_comparison.recorded"
)

RECORDED_PAIR_MEASUREMENT_COMPARISON_BOOK_CLAUSE = "04.Compare.A"
RECORDED_PAIR_MEASUREMENT_COMPARISON_ACT = (
    "Compare earlier and later exact byte-position-pair Measurement results"
)
RECORDED_PAIR_MEASUREMENT_COMPARISON_APPLICABILITY_ACT = (
    "Applicability of earlier and later recorded Measurement results to one Compare"
)

EVENT_KIND_BOOK_CLAUSES = {
    RECORDED_PAIR_MEASUREMENT_COMPARISON_SUBJECT_TO_ACT_BINDING_KIND: "04.Compare.A",
    RECORDED_PAIR_MEASUREMENT_COMPARISON_APPLICABILITY_SUBJECT_TO_ACT_BINDING_KIND: "01.Current.E.1",
    RECORDED_PAIR_MEASUREMENT_COMPARISON_APPLICABILITY_ACT_OCCURRENCE_EVENT: "02.Acts.A",
    RECORDED_PAIR_MEASUREMENT_COMPARISON_APPLICABILITY_RESULT_KIND: "01.Current.E.1",
    RECORDED_PAIR_MEASUREMENT_COMPARISON_ACT_OCCURRENCE_EVENT: "02.Acts.A",
    RECORDED_PAIR_MEASUREMENT_COMPARISON_RESULT_KIND: "04.Compare.A",
}


class RecordedPairMeasurementComparisonError(ValueError):
    """One exact recorded pair-Measurement comparison is incoherent."""


_BindingReading = tuple[Event, dict[str, Any]]
_ApplicabilityBindingReading = tuple[Event, dict[str, Any], _BindingReading]


def _identity(value: Any, message: str) -> str:
    if type(value) is not str or not value:
        raise RecordedPairMeasurementComparisonError(message)
    return value


def _operator_source_for_material_result(
    ledger: EventLedger, added: Event
) -> tuple[Event, dict[str, Any]]:
    """Read O1 or an earlier result carrying an O1 source reference."""

    from seed_runtime.operator_material_source import (
        get_recorded_operator_material_source,
    )

    source_references = added.material.get("source_occurrence_references")
    reference = (
        added.identity
        if added.kind == OPERATOR_MATERIAL_SOURCE_RECORDED_KIND
        else source_references[0]
        if type(source_references) is list and len(source_references) == 1
        else None
    )
    source_event = ledger.get(reference) if type(reference) is str else None
    try:
        source_material = get_recorded_operator_material_source(ledger, reference)
    except (TypeError, ValueError) as error:
        raise RecordedPairMeasurementComparisonError(
            "later Measurement requires one exact operator source occurrence"
        ) from error
    if (
        source_event is None
        or source_event.kind != OPERATOR_MATERIAL_SOURCE_RECORDED_KIND
        or source_event.locality_identity != added.locality_identity
        or source_event.exact_material != added.exact_material
    ):
        raise RecordedPairMeasurementComparisonError(
            "later Measurement requires one exact operator source occurrence"
        )
    return source_event, source_material


def _operator_source_current_coordinate_reference(
    ledger: EventLedger,
    *,
    source_material: dict[str, Any],
    earlier_measurement: Event,
    earlier_source_occurrence_references: tuple[str, ...],
) -> dict[str, str]:
    reference = source_material.get("current_coordinate_reference")
    if (
        type(reference) is not dict
        or reference.get("locality_identity")
        != earlier_measurement.locality_identity
        or type(reference.get("through_event_occurrence_identity")) is not str
    ):
        raise RecordedPairMeasurementComparisonError(
            "later Measurement requires one exact operator source occurrence"
        )
    required_occurrences = tuple(
        dict.fromkeys(
            (
                *earlier_source_occurrence_references,
                earlier_measurement.identity,
                reference["through_event_occurrence_identity"],
            )
        )
    )
    try:
        ordered = ledger.occurrences_in_append_order(
            required_occurrences,
            locality_identity=earlier_measurement.locality_identity,
        )
    except (TypeError, ValueError) as error:
        raise RecordedPairMeasurementComparisonError(
            "operator source occurrence carries no exact prior coordinates"
        ) from error
    if tuple(event.identity for event in ordered) != required_occurrences:
        raise RecordedPairMeasurementComparisonError(
            "operator source occurrence carries no exact prior coordinates"
        )
    return deepcopy(reference)


def _measurement_reference(event: Event) -> dict[str, str]:
    return {
        "recorded_occurrence_identity": event.identity,
        "result_identity": event.material["result_identity"],
        "act_occurrence_identity": event.material["act_occurrence_identity"],
        "act_occurrence_event_identity": event.material[
            "act_occurrence_event_identity"
        ],
    }


def _measurement_and_findings(
    ledger: EventLedger,
    event_identity: str,
    *,
    prior_coordinates: dict[str, Any] | None = None,
) -> tuple[Event, tuple[Any, ...], Event | None]:
    event_identity = _identity(
        event_identity, "comparison requires one exact recorded Measurement result"
    )
    event = ledger.get(event_identity)
    if (
        event is None
        or event.kind != BYTE_PAIR_MEASUREMENT_RECORDED_KIND
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise RecordedPairMeasurementComparisonError(
            "comparison requires one intact recorded byte-position-pair Measurement"
        )
    try:
        reading = _validated_recorded_byte_position_pair_measurement(
            ledger,
            event.identity,
            findings_only=True,
            prior_coordinates=prior_coordinates,
        )
    except (TypeError, ValueError) as error:
        raise RecordedPairMeasurementComparisonError(
            "comparison requires one intact recorded byte-position-pair Measurement"
        ) from error
    findings = reading.results if reading is not None else None
    if type(findings) is not tuple or reading is None:
        raise RecordedPairMeasurementComparisonError(
            "comparison requires exact recorded pair findings"
        )
    return event, findings, reading.binding


def _findings_from_carried_measurement(
    event: Event,
) -> tuple[_RecordedBytePairFinding, ...]:
    """Read finding coordinates produced by this same console call."""

    if (
        type(event) is not Event
        or event.kind != BYTE_PAIR_MEASUREMENT_RECORDED_KIND
        or event.exact_material is not None
    ):
        raise RecordedPairMeasurementComparisonError(
            "comparison requires one carried pair Measurement"
        )
    result_positions = event.material.get("result_positions")
    if type(result_positions) is not list:
        raise RecordedPairMeasurementComparisonError(
            "comparison requires one carried pair Measurement"
        )
    findings = []
    positions = set()
    for addressed_content in result_positions:
        dimensions = (
            addressed_content.get("dimensions")
            if type(addressed_content) is dict
            else None
        )
        subject = (
            addressed_content.get("subject")
            if type(addressed_content) is dict
            else None
        )
        result = (
            addressed_content.get("result")
            if type(addressed_content) is dict
            else None
        )
        result_position = (
            dimensions.get("position") if type(dimensions) is dict else None
        )
        content_coordinates = (
            dimensions.get("content") if type(dimensions) is dict else None
        )
        exact_pair = (
            subject.get("content") if type(subject) is dict else None
        )
        referenced_positions = (
            addressed_content.get("referenced_result_positions")
            if type(addressed_content) is dict
            else None
        )
        if (
            type(result_position) is not int
            or result_position < 0
            or result_position in positions
            or type(exact_pair) is not list
            or len(exact_pair) != 2
            or any(
                type(value) is not int or not 0 <= value <= 255
                for value in exact_pair
            )
            or result not in {"count", "recurrence"}
            or type(content_coordinates) is not dict
            or type(referenced_positions) is not list
            or any(
                type(value) is not int or value < 0
                for value in referenced_positions
            )
        ):
            raise RecordedPairMeasurementComparisonError(
                "comparison carried finding coordinates are not exact"
            )
        if result == "recurrence":
            if set(content_coordinates) != {"recurrence_established"} or type(
                content_coordinates["recurrence_established"]
            ) is not bool:
                raise RecordedPairMeasurementComparisonError(
                    "comparison carried finding content is not exact"
                )
            carried_content: tuple[int, int, int] | bool = content_coordinates[
                "recurrence_established"
            ]
        else:
            if set(content_coordinates) != {
                "input_count",
                "occurrences_carrying",
                "count",
            }:
                raise RecordedPairMeasurementComparisonError(
                    "comparison carried finding content is not exact"
                )
            carried_content = tuple(
                content_coordinates[key]
                for key in ("input_count", "occurrences_carrying", "count")
            )
            if any(type(value) is not int for value in carried_content):
                raise RecordedPairMeasurementComparisonError(
                    "comparison carried finding content is not exact"
                )
        positions.add(result_position)
        findings.append(
            _RecordedBytePairFinding(
                result_position=result_position,
                recorded_occurrence_identity=event.identity,
                exact_pair=tuple(exact_pair),
                result=result,
                _content_coordinates=carried_content,
                _referenced_result_positions=tuple(referenced_positions),
            )
        )
    return tuple(findings)


def _source_occurrence_references(
    ledger: EventLedger,
    event: Event,
    *,
    prior_coordinates: dict[str, Any] | None = None,
) -> tuple[str, ...]:
    reference = event.material.get("subject_to_act_binding_reference")
    if reference is None:
        source_reference = event.material.get("source_result_position_reference")
        source_positions = (
            result_positions_of_recorded_byte_measurement(
                ledger,
                source_reference.get("recorded_occurrence_identity"),
                prior_coordinates=prior_coordinates,
            )
            if type(source_reference) is dict
            else None
        )
        source_position = (
            next(
                (
                    position
                    for position in source_positions
                    if position.get("dimensions", {}).get("position")
                    == source_reference.get("result_position")
                ),
                None,
            )
            if type(source_positions) is tuple
            else None
        )
        content = (
            source_position.get("dimensions", {}).get("content")
            if type(source_position) is dict
            else None
        )
        return _source_occurrence_references_from_binding(
            {
                "source_occurrence_references": (
                    content.get("source_material")
                    if type(content) is dict
                    else None
                )
            }
        )
    binding_event = _read_pair_measurement_subject_to_act_binding(
        ledger,
        reference.get("recorded_occurrence_identity")
        if type(reference) is dict
        else None,
        prior_coordinates=prior_coordinates,
    )[0]
    binding = binding_event.material
    return _source_occurrence_references_from_binding(binding)


def _source_occurrence_references_from_binding(
    binding: dict[str, Any],
) -> tuple[str, ...]:
    source_material = (
        binding.get("source_occurrence_references")
        if type(binding) is dict
        else None
    )
    if type(source_material) is not list or not source_material:
        raise RecordedPairMeasurementComparisonError(
            "comparison input carries no exact source occurrence sequence"
        )
    references = tuple(
        item.get("material_result_occurrence_identity") if type(item) is dict else None
        for item in source_material
    )
    if (
        any(type(reference) is not str or not reference for reference in references)
        or len(set(references)) != len(references)
    ):
        raise RecordedPairMeasurementComparisonError(
            "comparison input carries no exact source occurrence sequence"
        )
    return references


def _comparison_inputs(
    ledger: EventLedger,
    *,
    earlier_result_event_identity: str,
    later_result_event_identity: str,
    prior_coordinates: dict[str, Any] | None = None,
) -> dict[str, Any]:
    earlier, earlier_findings, earlier_binding = _measurement_and_findings(
        ledger,
        earlier_result_event_identity,
        prior_coordinates=prior_coordinates,
    )
    later, later_findings, later_binding = _measurement_and_findings(
        ledger,
        later_result_event_identity,
        prior_coordinates=prior_coordinates,
    )
    if earlier.identity == later.identity or earlier.locality_identity != later.locality_identity:
        raise RecordedPairMeasurementComparisonError(
            "comparison requires distinct results in one exact Locality"
        )
    try:
        ordered = ledger.occurrences_in_append_order(
            (earlier.identity, later.identity),
            locality_identity=earlier.locality_identity,
        )
    except (TypeError, ValueError) as error:
        raise RecordedPairMeasurementComparisonError(
            "later comparison input must follow the earlier input"
        ) from error
    if tuple(event.identity for event in ordered) != (earlier.identity, later.identity):
        raise RecordedPairMeasurementComparisonError(
            "later comparison input must follow the earlier input"
        )
    earlier_sources = _source_occurrence_references(
        ledger, earlier, prior_coordinates=prior_coordinates
    )
    later_sources = _source_occurrence_references(
        ledger, later, prior_coordinates=prior_coordinates
    )
    if len(later_sources) != len(earlier_sources) + 1 or later_sources[:-1] != earlier_sources:
        raise RecordedPairMeasurementComparisonError(
            "later Measurement must extend the earlier exact source sequence once"
        )
    added_reference = later_sources[-1]
    added = ledger.get(added_reference)
    source_references = (
        added.material.get("source_occurrence_references")
        if added is not None
        else None
    )
    try:
        if added is not None:
            read_exact_material_result(ledger, added.identity)
    except (TypeError, ValueError) as error:
        raise RecordedPairMeasurementComparisonError(
            "later Measurement requires one exact material result"
        ) from error
    if (
        added is None
        or added.locality_identity != earlier.locality_identity
        or ledger.integrity_of(added.identity) == CORRUPTED
        or type(source_references) is not list
    ):
        raise RecordedPairMeasurementComparisonError(
            "later Measurement requires one added occurrence with exact source coordinates"
        )
    operator_material_source_result_event_identity = None
    operator_material_source_current_coordinate_reference = None
    if added.kind == WITNESS_MATERIAL_SOURCE_RECORDED_KIND:
        raise RecordedPairMeasurementComparisonError(
            "Witness source references establish no recorded-pair Compare input"
        )
    elif added.kind == OPERATOR_MATERIAL_SOURCE_RECORDED_KIND:
        source_event, source_material = _operator_source_for_material_result(
            ledger, added
        )
        source_coordinate_reference = (
            _operator_source_current_coordinate_reference(
                ledger,
                source_material=source_material,
                earlier_measurement=earlier,
                earlier_source_occurrence_references=earlier_sources,
            )
        )
        operator_material_source_result_event_identity = source_event.identity
        operator_material_source_current_coordinate_reference = deepcopy(
            source_coordinate_reference
        )
    else:
        raise RecordedPairMeasurementComparisonError(
            "later Measurement requires one exact operator occurrence"
        )
    destination_relations = tuple(
        event
        for reference in source_references
        for event in (ledger.get(reference),)
        if event is not None and event.kind == OPERATOR_DESTINATION_LOCALITY_RECORDED_KIND
    )
    if len(destination_relations) > 1:
        raise RecordedPairMeasurementComparisonError(
            f"added occurrence carries {len(destination_relations)} distinct operator "
            "destination Locality relations"
        )
    destination_relation = destination_relations[0] if destination_relations else None
    operator_locality_identity = (
        earlier.locality_identity
        if added.kind == OPERATOR_MATERIAL_SOURCE_RECORDED_KIND
        else None
    )
    if destination_relation is not None:
        relation = get_recorded_operator_destination_locality(
            ledger, destination_relation.identity
        )
        if relation["destination_locality_identity"] != earlier.locality_identity:
            raise RecordedPairMeasurementComparisonError(
            "added occurrence has a destination Locality relation to another Locality"
            )
        operator_locality_identity = relation["operator_locality_identity"]
    return {
        "locality_identity": earlier.locality_identity,
        "earlier_event": earlier,
        "later_event": later,
        "earlier_findings": earlier_findings,
        "later_findings": later_findings,
        "earlier_source": earlier_sources,
        "later_source": later_sources,
        "added_reference": added_reference,
        "added_source_references": tuple(source_references),
        "operator_material_source_result_event_identity": (
            operator_material_source_result_event_identity
        ),
        "operator_material_source_current_coordinate_reference": (
            operator_material_source_current_coordinate_reference
        ),
        "operator_destination_locality_relation_event_identity": (
            destination_relation.identity if destination_relation is not None else None
        ),
        "operator_locality_identity": operator_locality_identity,
    }


def _comparison_inputs_from_carried_measurements(
    ledger: EventLedger,
    *,
    earlier: Event,
    later: Event,
    current_coordinates: dict[str, Any],
) -> dict[str, Any]:
    """Revalidate the older result and carry the newly produced result."""

    if (
        type(earlier) is not Event
        or type(later) is not Event
        or earlier.kind != BYTE_PAIR_MEASUREMENT_RECORDED_KIND
        or later.kind != BYTE_PAIR_MEASUREMENT_RECORDED_KIND
        or earlier.identity == later.identity
        or earlier.locality_identity != later.locality_identity
        or type(current_coordinates) is not dict
        or current_coordinates.get("locality_identity") != earlier.locality_identity
    ):
        raise RecordedPairMeasurementComparisonError(
            "comparison requires first and second carried pair Measurements"
        )
    earlier, earlier_findings, earlier_binding = _measurement_and_findings(
        ledger,
        earlier.identity,
        prior_coordinates=current_coordinates,
    )
    carried = current_coordinates.get("measurement_occurrences")
    if (
        type(carried) is not dict
        or earlier.identity not in carried
        or later.identity not in carried
    ):
        raise RecordedPairMeasurementComparisonError(
            "comparison requires first and second carried pair Measurements"
        )
    try:
        ordered = ledger.occurrences_in_append_order(
            (earlier.identity, later.identity),
            locality_identity=earlier.locality_identity,
        )
    except (TypeError, ValueError) as error:
        raise RecordedPairMeasurementComparisonError(
            "later comparison input must follow the earlier input"
        ) from error
    if tuple(event.identity for event in ordered) != (
        earlier.identity,
        later.identity,
    ):
        raise RecordedPairMeasurementComparisonError(
            "later comparison input must follow the earlier input"
        )
    earlier_sources = _source_occurrence_references(
        ledger, earlier, prior_coordinates=current_coordinates
    )
    later_sources = _source_occurrence_references(
        ledger,
        later,
        prior_coordinates=current_coordinates,
    )
    if (
        len(later_sources) != len(earlier_sources) + 1
        or later_sources[:-1] != earlier_sources
    ):
        raise RecordedPairMeasurementComparisonError(
            "later Measurement must extend the earlier exact source sequence once"
        )
    added_reference = later_sources[-1]
    added = ledger.get(added_reference)
    source_references = (
        added.material.get("source_occurrence_references")
        if added is not None
        else None
    )
    try:
        if added is not None:
            read_exact_material_result(ledger, added.identity)
    except (TypeError, ValueError) as error:
        raise RecordedPairMeasurementComparisonError(
            "later Measurement requires one exact material result"
        ) from error
    if (
        added is None
        or added.locality_identity != earlier.locality_identity
        or ledger.integrity_of(added.identity) == CORRUPTED
        or type(source_references) is not list
    ):
        raise RecordedPairMeasurementComparisonError(
            "later Measurement requires one added occurrence with exact source coordinates"
        )
    operator_source_identity = None
    source_coordinate_reference = None
    if added.kind == OPERATOR_MATERIAL_SOURCE_RECORDED_KIND:
        source_event, source_material = _operator_source_for_material_result(
            ledger, added
        )
        exact_results = current_coordinates.get("exact_result_occurrences")
        if (
            source_event.locality_identity != earlier.locality_identity
            or source_event.exact_material != added.exact_material
            or type(exact_results) is not dict
            or source_event.identity not in exact_results
        ):
            raise RecordedPairMeasurementComparisonError(
                "operator source occurrence carries no exact prior coordinates"
            )
        source_coordinate_reference = (
            _operator_source_current_coordinate_reference(
                ledger,
                source_material=source_material,
                earlier_measurement=earlier,
                earlier_source_occurrence_references=earlier_sources,
            )
        )
        operator_source_identity = source_event.identity
        operator_locality_identity = earlier.locality_identity
    elif added.kind == WITNESS_MATERIAL_SOURCE_RECORDED_KIND:
        raise RecordedPairMeasurementComparisonError(
            "Witness source references establish no recorded-pair Compare input"
        )
    else:
        raise RecordedPairMeasurementComparisonError(
            "later Measurement requires one exact operator occurrence"
        )
    destination_relations = tuple(
        event
        for reference in source_references
        for event in (ledger.get(reference),)
        if event is not None and event.kind == OPERATOR_DESTINATION_LOCALITY_RECORDED_KIND
    )
    if len(destination_relations) > 1:
        raise RecordedPairMeasurementComparisonError(
            f"added occurrence carries {len(destination_relations)} distinct operator "
            "destination Locality relations"
        )
    destination_relation = destination_relations[0] if destination_relations else None
    if destination_relation is not None:
        relation = get_recorded_operator_destination_locality(
            ledger, destination_relation.identity
        )
        if relation["destination_locality_identity"] != earlier.locality_identity:
            raise RecordedPairMeasurementComparisonError(
                "added occurrence has a destination Locality relation to another Locality"
            )
        operator_locality_identity = relation["operator_locality_identity"]
    return {
        "locality_identity": earlier.locality_identity,
        "earlier_event": earlier,
        "later_event": later,
        "earlier_findings": earlier_findings,
        "later_findings": _findings_from_carried_measurement(later),
        "earlier_source": earlier_sources,
        "later_source": later_sources,
        "added_reference": added_reference,
        "added_source_references": tuple(source_references),
        "operator_material_source_result_event_identity": operator_source_identity,
        "operator_material_source_current_coordinate_reference": deepcopy(
            source_coordinate_reference
        ),
        "operator_destination_locality_relation_event_identity": (
            destination_relation.identity if destination_relation is not None else None
        ),
        "operator_locality_identity": operator_locality_identity,
    }


def _require_measurement_current_coordinates(
    ledger: EventLedger,
    *,
    inputs: dict[str, Any],
    current_coordinates: dict[str, Any],
) -> str:
    if type(current_coordinates) is not dict:
        raise RecordedPairMeasurementComparisonError(
            "comparison requires exact current Locality coordinates"
        )
    carried = current_coordinates.get("measurement_occurrences")
    boundary_identity = current_coordinates.get("through_event_occurrence_identity")
    required = (
        inputs["earlier_event"].identity,
        inputs["later_event"].identity,
    )
    if (
        current_coordinates.get("locality_identity") != inputs["locality_identity"]
        or type(carried) is not dict
        or any(reference not in carried for reference in required)
        or type(boundary_identity) is not str
        or not boundary_identity
    ):
        raise RecordedPairMeasurementComparisonError(
            "comparison requires each exact Measurement result in current coordinates"
        )
    identities = tuple(dict.fromkeys((*required, boundary_identity)))
    try:
        ordered = ledger.occurrences_in_append_order(
            identities, locality_identity=inputs["locality_identity"]
        )
    except (TypeError, ValueError) as error:
        raise RecordedPairMeasurementComparisonError(
            "comparison through-occurrence boundary lacks a required input"
        ) from error
    if tuple(event.identity for event in ordered) != identities:
        raise RecordedPairMeasurementComparisonError(
            "comparison through-occurrence boundary lacks a required input"
        )
    return boundary_identity


def _binding_reference(binding: Event) -> dict[str, Any]:
    return {
        "recorded_occurrence_identity": binding.identity,
        "book_clause_identity": binding.material["book_clause_identity"],
        "exact_act_identity": binding.material["exact_act_identity"],
        "subject_reference": deepcopy(binding.material["subject_reference"]),
    }


def _binding_material(
    *,
    inputs: dict[str, Any],
    through_event_occurrence_identity: str,
    exact_act_identity: str,
    comparison_act_occurrence_identity: str,
    comparison_result_identity: str,
) -> dict[str, Any]:
    return {
        "subject_reference": {
            "earlier_measurement_reference": _measurement_reference(
                inputs["earlier_event"]
            ),
            "later_measurement_reference": _measurement_reference(
                inputs["later_event"]
            ),
        },
        "exact_act_identity": exact_act_identity,
        "comparison_act_occurrence_identity": comparison_act_occurrence_identity,
        "comparison_result_identity": comparison_result_identity,
        "book_clause_identity": RECORDED_PAIR_MEASUREMENT_COMPARISON_BOOK_CLAUSE,
        "earlier_measurement_reference": _measurement_reference(
            inputs["earlier_event"]
        ),
        "later_measurement_reference": _measurement_reference(inputs["later_event"]),
        "earlier_source_occurrence_references": list(inputs["earlier_source"]),
        "later_source_occurrence_references": list(inputs["later_source"]),
        "added_occurrence_reference": inputs["added_reference"],
        "added_occurrence_source_references": list(
            inputs["added_source_references"]
        ),
        "operator_destination_locality_relation_event_identity": inputs[
            "operator_destination_locality_relation_event_identity"
        ],
        "operator_material_source_result_event_identity": inputs[
            "operator_material_source_result_event_identity"
        ],
        "operator_material_source_current_coordinate_reference": deepcopy(
            inputs["operator_material_source_current_coordinate_reference"]
        ),
        "destination_operator_locality_identity": inputs[
            "operator_locality_identity"
        ],
        "through_event_occurrence_identity": through_event_occurrence_identity,
    }


def _applicability_binding_material(
    *,
    inputs: dict[str, Any],
    through_event_occurrence_identity: str,
    addressed_act_identity: str,
    exact_act_identity: str,
    applicability_act_occurrence_identity: str,
    applicability_result_identity: str,
) -> dict[str, Any]:
    earlier_subject = _measurement_reference(inputs["earlier_event"])
    later_subject = _measurement_reference(inputs["later_event"])
    return {
        "subject_reference": {
            "earlier_input": {
                "subject": earlier_subject,
                "addressed_act_identity": addressed_act_identity,
            },
            "later_input": {
                "subject": later_subject,
                "addressed_act_identity": addressed_act_identity,
            },
        },
        "exact_act_identity": exact_act_identity,
        "applicability_act_occurrence_identity": applicability_act_occurrence_identity,
        "applicability_result_identity": applicability_result_identity,
        "addressed_act_identity": addressed_act_identity,
        "book_clause_identity": "01.Current.E.1",
        "earlier_measurement_reference": earlier_subject,
        "later_measurement_reference": later_subject,
        "through_event_occurrence_identity": through_event_occurrence_identity,
    }


def record_recorded_pair_measurement_comparison_subject_to_act_binding(
    ledger: EventLedger,
    *,
    earlier_result_event_identity: str,
    later_result_event_identity: str,
    current_coordinates: dict[str, Any],
) -> Event:
    """Record one exact Compare subject-to-Act binding."""

    inputs = _comparison_inputs(
        ledger,
        earlier_result_event_identity=earlier_result_event_identity,
        later_result_event_identity=later_result_event_identity,
        prior_coordinates=current_coordinates,
    )
    boundary = _require_measurement_current_coordinates(
        ledger, inputs=inputs, current_coordinates=current_coordinates
    )
    return _record_comparison_subject_to_act_binding(
        ledger, inputs=inputs, through_event_occurrence_identity=boundary
    )


def _record_comparison_subject_to_act_binding(
    ledger: EventLedger,
    *,
    inputs: dict[str, Any],
    through_event_occurrence_identity: str,
) -> Event:
    identities = {
        "exact_act_identity": ledger.mint_identity(
            "recorded_pair_comparison_act"
        ),
        "comparison_act_occurrence_identity": ledger.mint_identity(
            "recorded_pair_comparison_occurrence"
        ),
        "comparison_result_identity": ledger.mint_identity(
            "recorded_pair_comparison_result"
        ),
    }
    if len(set(identities.values())) != len(identities):
        raise RecordedPairMeasurementComparisonError(
            "comparison lifecycle identities are compressed"
        )
    return ledger.append(
        RECORDED_PAIR_MEASUREMENT_COMPARISON_SUBJECT_TO_ACT_BINDING_KIND,
        _binding_material(
            inputs=inputs,
            through_event_occurrence_identity=through_event_occurrence_identity,
            exact_act_identity=identities["exact_act_identity"],
            comparison_act_occurrence_identity=identities[
                "comparison_act_occurrence_identity"
            ],
            comparison_result_identity=identities[
                "comparison_result_identity"
            ],
        ),
        locality_identity=inputs["locality_identity"],
    )


def _binding_reading(
    ledger: EventLedger,
    event_identity: str,
    *,
    prior_coordinates: dict[str, Any] | None = None,
) -> _BindingReading:
    event = ledger.get(_identity(event_identity, "comparison requires one binding"))
    if (
        event is None
        or event.kind
        != RECORDED_PAIR_MEASUREMENT_COMPARISON_SUBJECT_TO_ACT_BINDING_KIND
        or event.exact_material is not None
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise RecordedPairMeasurementComparisonError(
            "comparison binding is absent or corrupted"
        )
    material = event.material
    earlier_reference = material.get("earlier_measurement_reference")
    later_reference = material.get("later_measurement_reference")
    if type(earlier_reference) is not dict or type(later_reference) is not dict:
        raise RecordedPairMeasurementComparisonError(
            "comparison binding carries no exact inputs"
        )
    inputs = _comparison_inputs(
        ledger,
        earlier_result_event_identity=earlier_reference.get(
            "recorded_occurrence_identity"
        ),
        later_result_event_identity=later_reference.get("recorded_occurrence_identity"),
        prior_coordinates=prior_coordinates,
    )
    identity_keys = (
        "exact_act_identity",
        "comparison_act_occurrence_identity",
        "comparison_result_identity",
    )
    identities = {key: material.get(key) for key in identity_keys}
    if any(type(value) is not str or not value for value in identities.values()) or len(
        set(identities.values())
    ) != len(identities):
        raise RecordedPairMeasurementComparisonError(
            "comparison binding identities are not exact"
        )
    boundary = material.get("through_event_occurrence_identity")
    boundary_event = ledger.get(boundary) if type(boundary) is str else None
    if (
        boundary_event is None
        or boundary_event.locality_identity != event.locality_identity
        or ledger.integrity_of(boundary_event.identity) == CORRUPTED
    ):
        raise RecordedPairMeasurementComparisonError(
            "comparison binding carries no intact through-occurrence boundary"
        )
    expected = _binding_material(
        inputs=inputs,
        through_event_occurrence_identity=boundary,
        **identities,
    )
    if event.locality_identity != inputs["locality_identity"] or material != expected:
        raise RecordedPairMeasurementComparisonError(
            "comparison binding coordinates are not exact"
        )
    try:
        ordered_references = tuple(
            dict.fromkeys(
                (
                    inputs["earlier_event"].identity,
                    inputs["later_event"].identity,
                    boundary,
                    event.identity,
                )
            )
        )
        ledger.occurrences_in_append_order(
            ordered_references,
            locality_identity=event.locality_identity,
        )
    except ValueError as error:
        raise RecordedPairMeasurementComparisonError(
            "comparison binding does not follow its exact inputs"
        ) from error
    return event, inputs


def get_recorded_pair_measurement_comparison_subject_to_act_binding(
    ledger: EventLedger, event_identity: str
) -> Event:
    return _binding_reading(ledger, event_identity)[0]


def _applicability_binding_reading(
    ledger: EventLedger,
    event_identity: str,
    *,
    comparison_binding_reading: _BindingReading | None = None,
    prior_coordinates: dict[str, Any] | None = None,
) -> tuple[Event, dict[str, Any], _BindingReading]:
    event = ledger.get(
        _identity(event_identity, "comparison requires one Applicability binding")
    )
    if (
        event is None
        or event.kind
        != RECORDED_PAIR_MEASUREMENT_COMPARISON_APPLICABILITY_SUBJECT_TO_ACT_BINDING_KIND
        or event.exact_material is not None
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise RecordedPairMeasurementComparisonError(
            "comparison Applicability binding is absent or corrupted"
        )
    material = event.material
    addressed_act_identity = material.get("addressed_act_identity")
    if comparison_binding_reading is None:
        comparison_bindings = tuple(
            candidate
            for candidate in ledger.iter_locality_kind(
                event.locality_identity,
                RECORDED_PAIR_MEASUREMENT_COMPARISON_SUBJECT_TO_ACT_BINDING_KIND,
            )
            if candidate.material.get("exact_act_identity") == addressed_act_identity
        )
        if len(comparison_bindings) != 1:
            raise RecordedPairMeasurementComparisonError(
                "comparison Applicability binding addresses no exact Compare binding"
            )
        comparison_binding_reading = _binding_reading(
            ledger,
            comparison_bindings[0].identity,
            prior_coordinates=prior_coordinates,
        )
    comparison_binding, inputs = comparison_binding_reading
    identity_keys = (
        "exact_act_identity",
        "applicability_act_occurrence_identity",
        "applicability_result_identity",
    )
    identities = {key: material.get(key) for key in identity_keys}
    boundary = material.get("through_event_occurrence_identity")
    expected = _applicability_binding_material(
        inputs=inputs,
        through_event_occurrence_identity=boundary,
        addressed_act_identity=comparison_binding.material["exact_act_identity"],
        **identities,
    )
    if (
        any(type(value) is not str or not value for value in identities.values())
        or len(set(identities.values())) != len(identities)
        or type(boundary) is not str
        or event.locality_identity != comparison_binding.locality_identity
        or addressed_act_identity
        != comparison_binding.material.get("exact_act_identity")
        or material != expected
    ):
        raise RecordedPairMeasurementComparisonError(
            "comparison Applicability binding coordinates are not exact"
        )
    try:
        ledger.occurrences_in_append_order(
            tuple(
                dict.fromkeys(
                    (comparison_binding.identity, boundary, event.identity)
                )
            ),
            locality_identity=event.locality_identity,
        )
    except ValueError as error:
        raise RecordedPairMeasurementComparisonError(
            "comparison Applicability binding does not follow its Compare binding"
        ) from error
    return event, inputs, comparison_binding_reading


def get_recorded_pair_measurement_comparison_applicability_subject_to_act_binding(
    ledger: EventLedger, event_identity: str
) -> Event:
    return _applicability_binding_reading(ledger, event_identity)[0]


def record_recorded_pair_measurement_comparison_applicability_subject_to_act_binding(
    ledger: EventLedger,
    *,
    comparison_binding_event_identity: str,
    current_coordinates: dict[str, Any],
) -> Event:
    comparison_binding, inputs = _binding_reading(
        ledger,
        comparison_binding_event_identity,
        prior_coordinates=current_coordinates,
    )
    _require_binding_current_coordinates(comparison_binding, current_coordinates)
    through_event_occurrence_identity = current_coordinates.get(
        "through_event_occurrence_identity"
    )
    identities = {
        "exact_act_identity": ledger.mint_identity(
            "recorded_pair_comparison_applicability_act"
        ),
        "applicability_act_occurrence_identity": ledger.mint_identity(
            "recorded_pair_comparison_applicability_occurrence"
        ),
        "applicability_result_identity": ledger.mint_identity(
            "recorded_pair_comparison_applicability_result"
        ),
    }
    if (
        type(through_event_occurrence_identity) is not str
        or not through_event_occurrence_identity
        or len(set(identities.values())) != len(identities)
    ):
        raise RecordedPairMeasurementComparisonError(
            "comparison Applicability binding coordinates are not exact"
        )
    return ledger.append(
        RECORDED_PAIR_MEASUREMENT_COMPARISON_APPLICABILITY_SUBJECT_TO_ACT_BINDING_KIND,
        _applicability_binding_material(
            inputs=inputs,
            through_event_occurrence_identity=through_event_occurrence_identity,
            addressed_act_identity=comparison_binding.material[
                "exact_act_identity"
            ],
            **identities,
        ),
        locality_identity=comparison_binding.locality_identity,
    )


def _require_binding_current_coordinates(
    binding: Event, current_coordinates: dict[str, Any]
) -> None:
    carried = (
        current_coordinates.get("subject_to_act_binding_occurrences")
        if type(current_coordinates) is dict
        else None
    )
    if (
        type(carried) is not dict
        or carried.get(binding.identity, object()) is not None
        or current_coordinates.get("locality_identity") != binding.locality_identity
    ):
        raise RecordedPairMeasurementComparisonError(
            "comparison requires its exact binding in current coordinates"
        )


def _applicability_act_material(binding: Event) -> dict[str, Any]:
    material = binding.material
    return {
        "applicability_act_identity": material["exact_act_identity"],
        "act_occurrence_identity": material[
            "applicability_act_occurrence_identity"
        ],
        "result_identity": material["applicability_result_identity"],
        "act": RECORDED_PAIR_MEASUREMENT_COMPARISON_APPLICABILITY_ACT,
        "subject_to_act_binding_reference": _binding_reference(binding),
    }


def record_recorded_pair_measurement_comparison_applicability_act_occurrence(
    ledger: EventLedger,
    *,
    applicability_binding_event_identity: str,
    current_coordinates: dict[str, Any],
) -> Event:
    applicability_binding, _inputs, _comparison_binding_reading = (
        _applicability_binding_reading(
            ledger,
            applicability_binding_event_identity,
            prior_coordinates=current_coordinates,
        )
    )
    _require_binding_current_coordinates(applicability_binding, current_coordinates)
    return ledger.append(
        RECORDED_PAIR_MEASUREMENT_COMPARISON_APPLICABILITY_ACT_OCCURRENCE_EVENT,
        _applicability_act_material(applicability_binding),
        locality_identity=applicability_binding.locality_identity,
    )


def _applicability_act_reading(
    ledger: EventLedger,
    event_identity: str,
    *,
    applicability_binding_reading: _ApplicabilityBindingReading | None = None,
    comparison_binding_reading: _BindingReading | None = None,
    prior_coordinates: dict[str, Any] | None = None,
) -> tuple[Event, _ApplicabilityBindingReading]:
    event = ledger.get(_identity(event_identity, "comparison requires Applicability Act occurrence"))
    if (
        event is None
        or event.kind
        != RECORDED_PAIR_MEASUREMENT_COMPARISON_APPLICABILITY_ACT_OCCURRENCE_EVENT
        or event.exact_material is not None
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise RecordedPairMeasurementComparisonError(
            "comparison Applicability Act occurrence is absent or corrupted"
        )
    reference = event.material.get("subject_to_act_binding_reference")
    binding_identity = (
        reference.get("recorded_occurrence_identity")
        if type(reference) is dict
        else None
    )
    if applicability_binding_reading is None:
        applicability_binding_reading = (
            _applicability_binding_reading(
                ledger,
                binding_identity,
                comparison_binding_reading=comparison_binding_reading,
                prior_coordinates=prior_coordinates,
            )
        )
    binding, _inputs, _comparison_binding_reading = applicability_binding_reading
    if (
        binding_identity != binding.identity
        or event.locality_identity != binding.locality_identity
        or event.material != _applicability_act_material(binding)
    ):
        raise RecordedPairMeasurementComparisonError(
            "comparison Applicability Act occurrence is not exact"
        )
    try:
        ledger.occurrences_in_append_order(
            (binding.identity, event.identity),
            locality_identity=event.locality_identity,
        )
    except ValueError as error:
        raise RecordedPairMeasurementComparisonError(
            "comparison Applicability does not follow its binding"
        ) from error
    return event, applicability_binding_reading


def get_recorded_pair_measurement_comparison_applicability_act_occurrence(
    ledger: EventLedger, event_identity: str
) -> Event:
    return _applicability_act_reading(ledger, event_identity)[0]


def _applicability_result_material(act: Event) -> dict[str, Any]:
    return {
        "result_identity": act.material["result_identity"],
        "applicability_act_identity": act.material["applicability_act_identity"],
        "act_occurrence_identity": act.material["act_occurrence_identity"],
        "exact_act": RECORDED_PAIR_MEASUREMENT_COMPARISON_APPLICABILITY_ACT,
        "subject_to_act_binding_reference": deepcopy(
            act.material["subject_to_act_binding_reference"]
        ),
        "applicability": "applicable",
    }


def _recorded_applicability_result_material(
    material: dict[str, Any], *, act_identity: str
) -> dict[str, Any]:
    return {
        "result_identity": material["result_identity"],
        "applicability_act_identity": material["applicability_act_identity"],
        "act_occurrence_identity": material["act_occurrence_identity"],
        "exact_act": material["exact_act"],
        "subject_to_act_binding_reference": deepcopy(
            material["subject_to_act_binding_reference"]
        ),
        "applicability": material["applicability"],
        "act_occurrence_event_identity": act_identity,
    }


def record_recorded_pair_measurement_comparison_applicability_result(
    ledger: EventLedger,
    *,
    act_occurrence_event_identity: str,
    current_coordinates: dict[str, Any] | None = None,
) -> Event:
    act = _applicability_act_reading(
        ledger,
        act_occurrence_event_identity,
        prior_coordinates=current_coordinates,
    )[0]
    result = _applicability_result_material(act)
    return _record_applicability_result_from_act(ledger, act=act, result=result)


def _record_applicability_result_from_act(
    ledger: EventLedger, *, act: Event, result: dict[str, Any]
) -> Event:
    existing = tuple(
        event
        for event in ledger.iter_locality_kind(
            act.locality_identity,
            RECORDED_PAIR_MEASUREMENT_COMPARISON_APPLICABILITY_RESULT_KIND,
        )
        if event.material.get("act_occurrence_event_identity") == act.identity
    )
    if existing:
        raise RecordedPairMeasurementComparisonError(
            "comparison Applicability Act has one result"
        )
    return ledger.append(
        RECORDED_PAIR_MEASUREMENT_COMPARISON_APPLICABILITY_RESULT_KIND,
        _recorded_applicability_result_material(
            result, act_identity=act.identity
        ),
        locality_identity=act.locality_identity,
    )


def _applicability_reading(
    ledger: EventLedger,
    event_identity: str,
    *,
    applicability_binding_reading: _ApplicabilityBindingReading | None = None,
    comparison_binding_reading: _BindingReading | None = None,
    prior_coordinates: dict[str, Any] | None = None,
) -> tuple[
    dict[str, Any],
    Event,
    Event,
    _ApplicabilityBindingReading,
]:
    event = ledger.get(_identity(event_identity, "comparison requires Applicability"))
    if (
        event is None
        or event.kind != RECORDED_PAIR_MEASUREMENT_COMPARISON_APPLICABILITY_RESULT_KIND
        or event.exact_material is not None
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise RecordedPairMeasurementComparisonError(
            "comparison Applicability is absent or corrupted"
        )
    act, applicability_binding_reading = (
        _applicability_act_reading(
            ledger,
            event.material.get("act_occurrence_event_identity"),
            applicability_binding_reading=applicability_binding_reading,
            comparison_binding_reading=comparison_binding_reading,
            prior_coordinates=prior_coordinates,
        )
    )
    expected = _recorded_applicability_result_material(
        _applicability_result_material(act),
        act_identity=act.identity,
    )
    try:
        ordered = ledger.occurrences_in_append_order(
            (act.identity, event.identity),
            locality_identity=event.locality_identity,
        )
    except (TypeError, ValueError) as error:
        raise RecordedPairMeasurementComparisonError(
            "comparison Applicability result does not follow its Act"
        ) from error
    results = tuple(
        candidate
        for candidate in ledger.iter_locality_kind(
            event.locality_identity,
            RECORDED_PAIR_MEASUREMENT_COMPARISON_APPLICABILITY_RESULT_KIND,
        )
        if candidate.material.get("act_occurrence_event_identity") == act.identity
    )
    if (
        event.locality_identity != act.locality_identity
        or event.material != expected
        or tuple(item.identity for item in ordered)
        != (act.identity, event.identity)
        or len(results) != 1
        or results[0].identity != event.identity
    ):
        raise RecordedPairMeasurementComparisonError(
            "comparison Applicability result is not exact for its Act"
        )
    return deepcopy(event.material), event, act, applicability_binding_reading


def get_recorded_pair_measurement_comparison_applicability(
    ledger: EventLedger,
    event_identity: str,
    *,
    prior_coordinates: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return _applicability_reading(
        ledger,
        event_identity,
        prior_coordinates=prior_coordinates,
    )[0]


def _require_applicability_current_coordinates(
    comparison_binding: Event,
    applicability_binding: Event,
    applicability: Event,
    current_coordinates: dict[str, Any],
) -> None:
    bindings = (
        current_coordinates.get("subject_to_act_binding_occurrences")
        if type(current_coordinates) is dict
        else None
    )
    applicable = (
        current_coordinates.get("applicability_result_occurrences")
        if type(current_coordinates) is dict
        else None
    )
    if (
        current_coordinates.get("locality_identity")
        != comparison_binding.locality_identity
        or type(bindings) is not dict
        or bindings.get(comparison_binding.identity, object()) is not None
        or bindings.get(applicability_binding.identity, object()) is not None
        or type(applicable) is not dict
        or applicable.get(applicability.identity, object()) is not None
    ):
        raise RecordedPairMeasurementComparisonError(
            "Compare requires its exact binding and Applicability in current coordinates"
        )


def _comparison_act_material(binding: Event, applicability: Event) -> dict[str, Any]:
    material = binding.material
    return {
        "comparison_act_identity": material["exact_act_identity"],
        "act_occurrence_identity": material["comparison_act_occurrence_identity"],
        "result_identity": material["comparison_result_identity"],
        "act": RECORDED_PAIR_MEASUREMENT_COMPARISON_ACT,
        "subject_to_act_binding_reference": _binding_reference(binding),
        "applicability_result_event_identity": applicability.identity,
    }


def _comparison_act_material_without_applicability(binding: Event) -> dict[str, Any]:
    material = binding.material
    return {
        "comparison_act_identity": material["exact_act_identity"],
        "act_occurrence_identity": material["comparison_act_occurrence_identity"],
        "result_identity": material["comparison_result_identity"],
        "act": RECORDED_PAIR_MEASUREMENT_COMPARISON_ACT,
        "subject_to_act_binding_reference": _binding_reference(binding),
    }


def _record_comparison_act_from_binding_without_applicability(
    ledger: EventLedger,
    *,
    binding: Event,
    current_coordinates: dict[str, Any],
) -> Event:
    binding_reading = _binding_reading(
        ledger,
        binding.identity,
        prior_coordinates=current_coordinates,
    )
    if binding_reading[0] is not binding:
        raise RecordedPairMeasurementComparisonError(
            "Compare carries another exact binding"
        )
    _require_binding_current_coordinates(binding, current_coordinates)
    return ledger.append(
        RECORDED_PAIR_MEASUREMENT_COMPARISON_ACT_OCCURRENCE_EVENT,
        _comparison_act_material_without_applicability(binding),
        locality_identity=binding.locality_identity,
    )


def record_recorded_pair_measurement_comparison_act_occurrence(
    ledger: EventLedger,
    *,
    subject_to_act_binding_event_identity: str,
    applicability_result_event_identity: str,
    current_coordinates: dict[str, Any],
) -> Event:
    binding_reading = _binding_reading(
        ledger,
        subject_to_act_binding_event_identity,
        prior_coordinates=current_coordinates,
    )
    binding, _inputs = binding_reading
    (
        applicability_material,
        applicability,
        _act,
        applicability_binding_reading,
    ) = (
        _applicability_reading(
            ledger,
            applicability_result_event_identity,
            comparison_binding_reading=binding_reading,
        )
    )
    applicability_binding, _applicability_inputs, addressed_binding_reading = (
        applicability_binding_reading
    )
    if (
        addressed_binding_reading[0].identity != binding.identity
        or applicability_binding.material["addressed_act_identity"]
        != binding.material["exact_act_identity"]
        or applicability_material["subject_to_act_binding_reference"]
        != _binding_reference(applicability_binding)
    ):
        raise RecordedPairMeasurementComparisonError(
            "Compare Applicability names another binding"
        )
    _require_applicability_current_coordinates(
        binding, applicability_binding, applicability, current_coordinates
    )
    return ledger.append(
        RECORDED_PAIR_MEASUREMENT_COMPARISON_ACT_OCCURRENCE_EVENT,
        _comparison_act_material(binding, applicability),
        locality_identity=binding.locality_identity,
    )


def _comparison_act_reading(
    ledger: EventLedger,
    event_identity: str,
    *,
    binding_reading: _BindingReading | None = None,
    prior_coordinates: dict[str, Any] | None = None,
) -> tuple[Event, _BindingReading, Event | None]:
    event = ledger.get(_identity(event_identity, "comparison requires Act occurrence"))
    if (
        event is None
        or event.kind != RECORDED_PAIR_MEASUREMENT_COMPARISON_ACT_OCCURRENCE_EVENT
        or event.exact_material is not None
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise RecordedPairMeasurementComparisonError(
            "comparison Act occurrence is absent or corrupted"
        )
    reference = event.material.get("subject_to_act_binding_reference")
    if binding_reading is None:
        binding_reading = _binding_reading(
            ledger,
            reference.get("recorded_occurrence_identity")
            if type(reference) is dict
            else None,
            prior_coordinates=prior_coordinates,
        )
    binding, _inputs = binding_reading
    if "applicability_result_event_identity" not in event.material:
        if (
            event.locality_identity != binding.locality_identity
            or event.material
            != _comparison_act_material_without_applicability(binding)
        ):
            raise RecordedPairMeasurementComparisonError(
                "comparison Act occurrence is not exact"
            )
        return event, binding_reading, None
    applicability = ledger.get(event.material.get("applicability_result_event_identity"))
    if applicability is None:
        raise RecordedPairMeasurementComparisonError(
            "comparison Act occurrence carries no Applicability"
        )
    _material, applicability, _act, applicability_binding_reading = (
        _applicability_reading(
            ledger,
            applicability.identity,
            comparison_binding_reading=binding_reading,
            prior_coordinates=prior_coordinates,
        )
    )
    if (
        applicability_binding_reading[2][0].identity != binding.identity
        or event.locality_identity != binding.locality_identity
        or event.material != _comparison_act_material(binding, applicability)
    ):
        raise RecordedPairMeasurementComparisonError(
            "comparison Act occurrence is not exact"
        )
    return event, binding_reading, applicability


def get_recorded_pair_measurement_comparison_act_occurrence(
    ledger: EventLedger, event_identity: str
) -> Event:
    return _comparison_act_reading(ledger, event_identity)[0]


def _finding_key(finding: Any) -> tuple[str, tuple[int, int] | None]:
    return finding.result, finding.exact_pair


def _finding_content(finding: Any) -> Any:
    content = finding.content
    if type(content) is not dict:
        raise RecordedPairMeasurementComparisonError(
            "comparison input carries no exact finding content"
        )
    return content


def _comparison_of_findings(
    earlier: tuple[Any, ...], later: tuple[Any, ...]
) -> dict[str, list[dict[str, Any]]]:
    earlier_by_key = {_finding_key(item): item for item in earlier}
    later_by_key = {_finding_key(item): item for item in later}
    if len(earlier_by_key) != len(earlier) or len(later_by_key) != len(later):
        raise RecordedPairMeasurementComparisonError(
            "comparison input repeats one finding subject"
        )
    findings = {
        "same_content_findings": [],
        "conflicting_findings": [],
        "findings_of_earlier_result": [],
        "findings_of_later_result": [],
    }
    for key, first in earlier_by_key.items():
        second = later_by_key.get(key)
        subject = {
            "result": key[0],
            "content": list(key[1]) if key[1] is not None else None,
        }
        first_content = _finding_content(first)
        if second is None:
            findings["findings_of_earlier_result"].append(
                {
                    "subject": subject,
                    "earlier_result_position_reference": first.reference,
                    "earlier_content": first_content,
                }
            )
            continue
        second_content = _finding_content(second)
        entry = {
            "subject": subject,
            "earlier_result_position_reference": first.reference,
            "later_result_position_reference": second.reference,
            "earlier_content": first_content,
            "later_content": second_content,
        }
        destination = (
            "same_content_findings"
            if first_content == second_content
            else "conflicting_findings"
        )
        findings[destination].append(entry)
    for key, second in later_by_key.items():
        if key in earlier_by_key:
            continue
        findings["findings_of_later_result"].append(
            {
                "subject": {
                    "result": key[0],
                    "content": list(key[1]) if key[1] is not None else None,
                },
                "later_result_position_reference": second.reference,
                "later_content": _finding_content(second),
            }
        )
    return findings


def _comparison_result_material(
    act: Event,
    binding_reading: _BindingReading,
) -> dict[str, Any]:
    binding_reference = act.material["subject_to_act_binding_reference"]
    binding, inputs = binding_reading
    if binding_reference["recorded_occurrence_identity"] != binding.identity:
        raise RecordedPairMeasurementComparisonError(
            "comparison result carries another binding"
        )
    material = {
        "result_identity": act.material["result_identity"],
        "comparison_act_identity": act.material["comparison_act_identity"],
        "act_occurrence_identity": act.material["act_occurrence_identity"],
        "exact_act": RECORDED_PAIR_MEASUREMENT_COMPARISON_ACT,
        "subject_to_act_binding_reference": deepcopy(binding_reference),
        "findings": _comparison_of_findings(
            inputs["earlier_findings"], inputs["later_findings"]
        ),
    }
    if "applicability_result_event_identity" in act.material:
        material["applicability_result_event_identity"] = act.material[
            "applicability_result_event_identity"
        ]
    return material


def _recorded_comparison_result_material(
    material: dict[str, Any], *, act_identity: str
) -> dict[str, Any]:
    recorded = {
        "result_identity": material["result_identity"],
        "comparison_act_identity": material["comparison_act_identity"],
        "act_occurrence_identity": material["act_occurrence_identity"],
        "exact_act": material["exact_act"],
        "subject_to_act_binding_reference": deepcopy(
            material["subject_to_act_binding_reference"]
        ),
        "findings": deepcopy(material["findings"]),
        "act_occurrence_event_identity": act_identity,
    }
    if "applicability_result_event_identity" in material:
        recorded["applicability_result_event_identity"] = material[
            "applicability_result_event_identity"
        ]
    return recorded


def record_recorded_pair_measurement_comparison_result(
    ledger: EventLedger,
    *,
    act_occurrence_event_identity: str,
    current_coordinates: dict[str, Any] | None = None,
) -> Event:
    act, binding_reading, _applicability = (
        _comparison_act_reading(
            ledger,
            act_occurrence_event_identity,
            prior_coordinates=current_coordinates,
        )
    )
    result = _comparison_result_material(act, binding_reading)
    return _record_comparison_result_from_act(ledger, act=act, result=result)


def _record_comparison_result_from_act(
    ledger: EventLedger, *, act: Event, result: dict[str, Any]
) -> Event:
    prior_results = tuple(
        candidate
        for candidate in ledger.iter_locality_kind(
            act.locality_identity,
            RECORDED_PAIR_MEASUREMENT_COMPARISON_RESULT_KIND,
        )
        if candidate.material.get("act_occurrence_event_identity")
        == act.identity
    )
    if prior_results:
        raise RecordedPairMeasurementComparisonError(
            "comparison Act has one result"
        )
    return ledger.append(
        RECORDED_PAIR_MEASUREMENT_COMPARISON_RESULT_KIND,
        _recorded_comparison_result_material(
            result, act_identity=act.identity
        ),
        locality_identity=act.locality_identity,
    )


def _record_recorded_pair_measurement_comparison_from_carried_measurements(
    ledger: EventLedger,
    *,
    earlier_measurement: Event,
    later_measurement: Event,
    current_coordinates: dict[str, Any],
) -> tuple[Event, dict[str, Any]]:
    """Record one complete Compare from results carried by this console call."""

    from seed_runtime.operator_current_coordinates import (
        _carry_recorded_pair_comparison_occurrence_into_current_coordinates,
    )

    inputs = _comparison_inputs_from_carried_measurements(
        ledger,
        earlier=earlier_measurement,
        later=later_measurement,
        current_coordinates=current_coordinates,
    )
    boundary = _require_measurement_current_coordinates(
        ledger, inputs=inputs, current_coordinates=current_coordinates
    )
    binding = _record_comparison_subject_to_act_binding(
        ledger, inputs=inputs, through_event_occurrence_identity=boundary
    )
    current_coordinates = _carry_recorded_pair_comparison_occurrence_into_current_coordinates(
        ledger,
        current_coordinates,
        binding,
        prior_through_event_occurrence_identity=boundary,
    )
    _require_binding_current_coordinates(binding, current_coordinates)
    comparison_act = _record_comparison_act_from_binding_without_applicability(
        ledger,
        binding=binding,
        current_coordinates=current_coordinates,
    )
    current_coordinates = _carry_recorded_pair_comparison_occurrence_into_current_coordinates(
        ledger,
        current_coordinates,
        comparison_act,
        prior_through_event_occurrence_identity=binding.identity,
    )
    binding_reading = (binding, inputs)
    result_material = _comparison_result_material(
        comparison_act, binding_reading
    )
    result = _record_comparison_result_from_act(
        ledger, act=comparison_act, result=result_material
    )
    current_coordinates = _carry_recorded_pair_comparison_occurrence_into_current_coordinates(
        ledger,
        current_coordinates,
        result,
        prior_through_event_occurrence_identity=comparison_act.identity,
    )
    return result, current_coordinates


def _recorded_pair_measurement_comparison_reading(
    ledger: EventLedger,
    event_identity: str,
    *,
    binding_reading: _BindingReading | None = None,
    prior_coordinates: dict[str, Any] | None = None,
) -> tuple[dict[str, Any], _BindingReading]:
    event = ledger.get(_identity(event_identity, "comparison requires one result"))
    if (
        event is None
        or event.kind != RECORDED_PAIR_MEASUREMENT_COMPARISON_RESULT_KIND
        or event.exact_material is not None
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise RecordedPairMeasurementComparisonError(
            "comparison result is absent or corrupted"
        )
    act, binding_reading, _applicability = (
        _comparison_act_reading(
            ledger,
            event.material.get("act_occurrence_event_identity"),
            binding_reading=binding_reading,
            prior_coordinates=prior_coordinates,
        )
    )
    expected = _recorded_comparison_result_material(
        _comparison_result_material(
            act, binding_reading
        ),
        act_identity=act.identity,
    )
    if (
        event.locality_identity != act.locality_identity
        or event.material != expected
    ):
        raise RecordedPairMeasurementComparisonError(
            "comparison result coordinates are not exact"
        )
    try:
        ordered = ledger.occurrences_in_append_order(
            (act.identity, event.identity),
            locality_identity=event.locality_identity,
        )
    except ValueError as error:
        raise RecordedPairMeasurementComparisonError(
            "comparison result does not follow its Act"
        ) from error
    if [occurrence.identity for occurrence in ordered] != [
        act.identity,
        event.identity,
    ]:
        raise RecordedPairMeasurementComparisonError(
            "comparison result does not follow its Act"
        )
    results = tuple(
        candidate
        for candidate in ledger.iter_locality_kind(
            event.locality_identity,
            RECORDED_PAIR_MEASUREMENT_COMPARISON_RESULT_KIND,
        )
        if candidate.material.get("act_occurrence_event_identity")
        == act.identity
    )
    if len(results) != 1 or results[0].identity != event.identity:
        raise RecordedPairMeasurementComparisonError(
            "comparison Act has no single exact result"
        )
    return deepcopy(event.material), binding_reading


def get_recorded_pair_measurement_comparison(
    ledger: EventLedger,
    event_identity: str,
    *,
    prior_coordinates: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if prior_coordinates is None:
        return _recorded_pair_measurement_comparison_reading(
            ledger,
            event_identity,
        )[0]
    return _recorded_pair_measurement_comparison_reading(
        ledger,
        event_identity,
        prior_coordinates=prior_coordinates,
    )[0]
