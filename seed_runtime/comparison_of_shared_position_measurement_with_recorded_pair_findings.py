"""Compare one shared-position Measurement result with recorded pair findings."""

from __future__ import annotations

from copy import deepcopy
from typing import Any, NamedTuple

from seed_runtime.comparison_of_recorded_byte_pair_measurements import (
    RECORDED_PAIR_MEASUREMENT_COMPARISON_RESULT_KIND,
    _recorded_pair_measurement_comparison_reading,
)
from seed_runtime.event import Event
from seed_runtime.events import CORRUPTED, EventLedger
from seed_runtime.measurement_of_shared_position_of_byte_pair_occurrences import (
    SHARED_POSITION_MEASUREMENT_RESULT_KIND,
    get_recorded_shared_position_measurement,
)


COMPARISON_OF_SHARED_POSITION_MEASUREMENT_WITH_RECORDED_PAIR_FINDINGS_SUBJECT_TO_ACT_BINDING_KIND = (
    "operator.comparison_of_shared_position_measurement_with_recorded_pair_findings.subject_to_act_binding_recorded"
)
COMPARISON_OF_SHARED_POSITION_MEASUREMENT_WITH_RECORDED_PAIR_FINDINGS_APPLICABILITY_SUBJECT_TO_ACT_BINDING_KIND = (
    "operator.comparison_of_shared_position_measurement_with_recorded_pair_findings.applicability_subject_to_act_binding_recorded"
)
COMPARISON_OF_SHARED_POSITION_MEASUREMENT_WITH_RECORDED_PAIR_FINDINGS_APPLICABILITY_ACT_OCCURRENCE_EVENT = (
    "operator.comparison_of_shared_position_measurement_with_recorded_pair_findings.applicability_act_occurrence_recorded"
)
COMPARISON_OF_SHARED_POSITION_MEASUREMENT_WITH_RECORDED_PAIR_FINDINGS_APPLICABILITY_RESULT_KIND = (
    "operator.comparison_of_shared_position_measurement_with_recorded_pair_findings.applicability_recorded"
)
COMPARISON_OF_SHARED_POSITION_MEASUREMENT_WITH_RECORDED_PAIR_FINDINGS_COMPARE_ACT_OCCURRENCE_EVENT = (
    "operator.comparison_of_shared_position_measurement_with_recorded_pair_findings.compare_act_occurrence_recorded"
)
COMPARISON_OF_SHARED_POSITION_MEASUREMENT_WITH_RECORDED_PAIR_FINDINGS_RESULT_KIND = "operator.comparison_of_shared_position_measurement_with_recorded_pair_findings.recorded"

BOOK_CLAUSE = "04.Compare.B"
APPLICABILITY_ACT = (
    "Applicability of one same-position Measurement result position and one "
    "recorded pair Compare result to one Compare"
)
COMPARE_ACT = (
    "Compare each exact pair position of one same-position Measurement result "
    "with complete recorded findings of the same exact pair subject"
)
_ACTIVE_APPLICABILITY_ACT = "Applicability"
_ACTIVE_COMPARE_ACT = "Compare"
COMPARE_RESULT_KIND = (
    "Compare result of shared-position Measurement and recorded pair findings"
)

EVENT_KIND_BOOK_CLAUSES = {
    COMPARISON_OF_SHARED_POSITION_MEASUREMENT_WITH_RECORDED_PAIR_FINDINGS_SUBJECT_TO_ACT_BINDING_KIND: "04.Compare.B",
    COMPARISON_OF_SHARED_POSITION_MEASUREMENT_WITH_RECORDED_PAIR_FINDINGS_APPLICABILITY_SUBJECT_TO_ACT_BINDING_KIND: "01.Current.E.1",
    COMPARISON_OF_SHARED_POSITION_MEASUREMENT_WITH_RECORDED_PAIR_FINDINGS_APPLICABILITY_ACT_OCCURRENCE_EVENT: "02.Acts.A",
    COMPARISON_OF_SHARED_POSITION_MEASUREMENT_WITH_RECORDED_PAIR_FINDINGS_APPLICABILITY_RESULT_KIND: "01.Current.E.1",
    COMPARISON_OF_SHARED_POSITION_MEASUREMENT_WITH_RECORDED_PAIR_FINDINGS_COMPARE_ACT_OCCURRENCE_EVENT: "02.Acts.A",
    COMPARISON_OF_SHARED_POSITION_MEASUREMENT_WITH_RECORDED_PAIR_FINDINGS_RESULT_KIND: "04.Compare.B",
}

_FINDING_CATEGORIES = (
    "same_content_findings",
    "conflicting_findings",
    "findings_of_earlier_result",
    "findings_of_later_result",
)


class SharedPositionMeasurementPairFindingCompareSubject(NamedTuple):
    shared_position_measurement_result_event_identity: str
    comparison_result_event_identity: str


class RecordedSharedPositionMeasurementPairFindingCompareBindings(NamedTuple):
    current_coordinates: dict[str, Any]
    binding_occurrences: tuple[Event, ...]


class RecordedSharedPositionMeasurementPairFindingCompareApplicability(NamedTuple):
    current_coordinates: dict[str, Any]
    applicability_result_occurrences: tuple[Event, ...]


class RecordedSharedPositionMeasurementPairFindingCompareApplicabilityActOccurrence(
    NamedTuple
):
    current_coordinates: dict[str, Any]
    applicability_act_occurrence_occurrences: tuple[Event, ...]


class RecordedSharedPositionMeasurementPairFindingCompareActOccurrence(NamedTuple):
    current_coordinates: dict[str, Any]
    compare_act_occurrence_occurrences: tuple[Event, ...]


class RecordedSharedPositionMeasurementPairFindingCompareResults(NamedTuple):
    current_coordinates: dict[str, Any]
    compare_result_occurrences: tuple[Event, ...]


class SharedPositionMeasurementPairFindingCompareApplicabilityResultActReading(NamedTuple):
    through_event_occurrence_identity: str | None
    applicable_result_occurrence_identities: tuple[str, ...]
    inapplicable_result_occurrence_identities: tuple[str, ...]
    act_occurrences_by_applicability_result: tuple[
        tuple[str, str], ...
    ]
    applicable_result_occurrence_identities_without_act_occurrence: tuple[
        str, ...
    ]


def _identity(value: Any, message: str) -> str:
    if type(value) is not str or not value:
        raise ValueError(message)
    return value


def _advance_current_coordinates(
    ledger: EventLedger,
    current_coordinates: dict[str, Any],
    event_identities: tuple[str, ...],
    *,
    locality_identity: str,
) -> dict[str, Any]:
    """Advance the exact read over occurrences this Compare road recorded."""

    from seed_runtime.operator_current_coordinates import (
        advance_operator_current_coordinates,
    )

    return advance_operator_current_coordinates(
        ledger,
        event_identities,
        locality_identity=locality_identity,
        prior=current_coordinates,
    )


def _event(
    ledger: EventLedger,
    identity: Any,
    *,
    kind: str,
    message: str,
) -> Event:
    occurrence = ledger.get(_identity(identity, message))
    if (
        occurrence is None
        or occurrence.kind != kind
        or occurrence.exact_material is not None
        or ledger.integrity_of(occurrence.identity) == CORRUPTED
    ):
        raise ValueError(message)
    return occurrence


def _result_reference(event: Event) -> dict[str, str]:
    return {
        "recorded_occurrence_identity": event.identity,
        "result_identity": event.material["result_identity"],
        "act_occurrence_identity": event.material["act_occurrence_identity"],
        "act_occurrence_event_identity": event.material[
            "act_occurrence_event_identity"
        ],
    }


def _shared_position_input(
    ledger: EventLedger,
    event_identity: Any,
    *,
    prior_coordinates: dict[str, Any] | None = None,
) -> dict[str, Any]:
    event = _event(
        ledger,
        event_identity,
        kind=SHARED_POSITION_MEASUREMENT_RESULT_KIND,
        message="comparison of shared-position Measurement result with recorded pair findings requires one exact shared_position Measurement result",
    )
    material = get_recorded_shared_position_measurement(
        ledger,
        event.identity,
        prior_coordinates=prior_coordinates,
    )
    result_positions = material.get("result_positions")
    shared_position = (
        result_positions[0]
        if type(result_positions) is list and len(result_positions) == 1
        else None
    )
    first = material.get("first_position_result")
    second = material.get("second_position_result")
    if (
        type(shared_position) is not dict
        or shared_position.get("result_position") != 0
        or type(first) is not dict
        or type(second) is not dict
        or shared_position.get("subject", {}).get(
            "first_position_result_reference"
        )
        != first.get("result_position_reference")
        or shared_position.get("subject", {}).get(
            "second_position_result_reference"
        )
        != second.get("result_position_reference")
    ):
        raise ValueError("comparison of shared-position Measurement result with recorded pair findings requires one exact shared-position result result position")
    pairs = (first.get("exact_pair"), second.get("exact_pair"))
    if any(
        type(pair) is not list
        or len(pair) != 2
        or any(type(value) is not int or not 0 <= value <= 255 for value in pair)
        for pair in pairs
    ):
        raise ValueError("comparison of shared-position Measurement result with recorded pair findings requires exact pair subjects")
    content = shared_position.get("content")
    result_position = shared_position.get("result_position")
    source = (
        content.get("source_material_result_occurrence_identity")
        if type(content) is dict
        else None
    )
    return {
        "event": event,
        "reference": _result_reference(event),
        "result_content": deepcopy(shared_position),
        "result_position_reference": {
            "recorded_occurrence_identity": event.identity,
            "result_position": result_position,
        },
        "pair_subjects": tuple(tuple(pair) for pair in pairs),
        "source_occurrence_identity": _identity(
            source, "comparison of shared-position Measurement result with recorded pair findings requires one exact shared_position source occurrence"
        ),
    }


def _comparison_finding_references(
    comparison_event: Event, comparison: dict[str, Any]
) -> tuple[dict[str, Any], ...]:
    findings = comparison.get("findings")
    if type(findings) is not dict or tuple(findings) != _FINDING_CATEGORIES:
        raise ValueError("comparison of shared-position Measurement result with recorded pair findings requires complete comparison findings")
    references = []
    for category in _FINDING_CATEGORIES:
        entries = findings.get(category)
        if type(entries) is not list:
            raise ValueError(
                "comparison of shared-position Measurement result with recorded pair findings requires complete comparison findings"
            )
        for position, entry in enumerate(entries):
            reference = {
                "recorded_comparison_occurrence_identity": (
                    comparison_event.identity
                ),
                "finding_category": category,
                "finding_position": position,
            }
            _addressed_comparison_finding(
                comparison_event,
                comparison,
                reference,
            )
            references.append(reference)
    return tuple(references)


def _addressed_comparison_finding(
    comparison_event: Event,
    comparison: dict[str, Any],
    reference: dict[str, Any],
) -> dict[str, Any]:
    if (
        type(reference) is not dict
        or set(reference)
        != {
            "recorded_comparison_occurrence_identity",
            "finding_category",
            "finding_position",
        }
        or reference.get("recorded_comparison_occurrence_identity")
        != comparison_event.identity
        or reference.get("finding_category") not in _FINDING_CATEGORIES
        or type(reference.get("finding_position")) is not int
        or reference["finding_position"] < 0
    ):
        raise ValueError(
            "comparison finding reference requires one exact result position"
        )
    findings = comparison.get("findings")
    entries = (
        findings.get(reference["finding_category"])
        if type(findings) is dict
        else None
    )
    position = reference["finding_position"]
    entry = (
        entries[position]
        if type(entries) is list and position < len(entries)
        else None
    )
    subject = entry.get("subject") if type(entry) is dict else None
    pair = subject.get("content") if type(subject) is dict else None
    if (
        type(subject) is not dict
        or type(subject.get("result")) is not str
        or type(pair) is not list
        or len(pair) != 2
        or any(type(value) is not int for value in pair)
    ):
        raise ValueError(
            "comparison finding reference addresses no exact result content"
        )
    return entry


def _comparison_input(
    ledger: EventLedger,
    event_identity: Any,
    *,
    prior_coordinates: dict[str, Any] | None = None,
) -> dict[str, Any]:
    event = _event(
        ledger,
        event_identity,
        kind=RECORDED_PAIR_MEASUREMENT_COMPARISON_RESULT_KIND,
        message="comparison of shared-position Measurement result with recorded pair findings requires one exact recorded comparison result",
    )
    material, subject_reading = (
        _recorded_pair_measurement_comparison_reading(
            ledger,
            event.identity,
            prior_coordinates=prior_coordinates,
        )
    )
    binding, pair_inputs = subject_reading
    binding_reference = material.get("subject_to_act_binding_reference")
    binding_identity = (
        binding_reference.get("recorded_occurrence_identity")
        if type(binding_reference) is dict
        else None
    )
    if binding is not None and (
        binding.identity != binding_identity
        or binding.material.get("comparison_result_identity")
        != material.get("result_identity")
    ):
        raise ValueError(
            "comparison of shared-position Measurement result with recorded pair findings "
            "carries another Compare binding"
        )
    return {
        "event": event,
        "reference": _result_reference(event),
        "result_material": material,
        "added_occurrence_identity": pair_inputs["added_reference"],
        "finding_references": _comparison_finding_references(event, material),
    }


def _shared_position_pair_findings(
    comparison: dict[str, Any], pair: tuple[int, int]
) -> tuple[dict[str, Any], ...]:
    return tuple(
        reference
        for reference in comparison["finding_references"]
        if tuple(
            _addressed_comparison_finding(
                comparison["event"],
                comparison["result_material"],
                reference,
            )["subject"]["content"]
        )
        == pair
    )


def _inputs_from_readings(
    shared_position: dict[str, Any], comparison: dict[str, Any]
) -> dict[str, Any]:
    if shared_position["event"].locality_identity != comparison["event"].locality_identity:
        raise ValueError("comparison of shared-position Measurement result with recorded pair findings requires one exact Locality")
    matches = tuple(
        _shared_position_pair_findings(comparison, pair)
        for pair in shared_position["pair_subjects"]
    )
    return {
        "locality_identity": shared_position["event"].locality_identity,
        "shared_position": shared_position,
        "comparison": comparison,
        "shared_position_pair_findings": matches,
        "same_source": (
            shared_position["source_occurrence_identity"]
            == comparison["added_occurrence_identity"]
        ),
        "applicable": all(matches)
        and shared_position["source_occurrence_identity"]
        == comparison["added_occurrence_identity"],
    }


def _inputs(
    ledger: EventLedger,
    *,
    shared_position_measurement_result_event_identity: Any,
    comparison_result_event_identity: Any,
    prior_coordinates: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return _inputs_from_readings(
        _shared_position_input(
            ledger,
            shared_position_measurement_result_event_identity,
            prior_coordinates=prior_coordinates,
        ),
        _comparison_input(
            ledger,
            comparison_result_event_identity,
            prior_coordinates=prior_coordinates,
        ),
    )


def _unassigned_shared_position_measurement_pair_finding_compare_subjects_from_current_coordinates(
    ledger: EventLedger,
    *,
    locality_identity: str,
    current_coordinates: dict[str, Any],
) -> tuple[SharedPositionMeasurementPairFindingCompareSubject, ...]:
    measurement_occurrences = current_coordinates.get("measurement_occurrences")
    comparison_occurrences = current_coordinates.get("comparison_result_occurrences")
    if (
        type(measurement_occurrences) is not dict
        or type(comparison_occurrences) is not dict
    ):
        raise ValueError(
            "shared-position Compare subjects require exact current coordinates"
        )

    shared_position_identities = tuple(
        identity
        for identity in measurement_occurrences
        if (
            (event := ledger.get(identity)) is not None
            and event.kind == SHARED_POSITION_MEASUREMENT_RESULT_KIND
        )
    )
    comparison_identities = tuple(
        identity
        for identity in comparison_occurrences
        if (
            (event := ledger.get(identity)) is not None
            and event.kind == RECORDED_PAIR_MEASUREMENT_COMPARISON_RESULT_KIND
        )
    )

    shared_position_inputs = tuple(
        _shared_position_input(
            ledger,
            shared_position_identity,
            prior_coordinates=current_coordinates,
        )
        for shared_position_identity in shared_position_identities
    )
    comparison_inputs = tuple(
        _comparison_input(
            ledger,
            comparison_identity,
            prior_coordinates=current_coordinates,
        )
        for comparison_identity in comparison_identities
    )

    assigned: set[tuple[str, str]] = set()
    for occurrence in ledger.iter_locality_kind(
        locality_identity,
        COMPARISON_OF_SHARED_POSITION_MEASUREMENT_WITH_RECORDED_PAIR_FINDINGS_SUBJECT_TO_ACT_BINDING_KIND,
    ):
        binding, inputs = _read_binding(
            ledger,
            occurrence.identity,
            prior_coordinates=current_coordinates,
        )
        assigned.add(
            (
                inputs["shared_position"]["event"].identity,
                inputs["comparison"]["event"].identity,
            )
        )
        if binding.locality_identity != locality_identity:
            raise ValueError(
                "shared-position Compare binding belongs to another Locality"
            )

    subjects = []
    for shared_position in shared_position_inputs:
        for comparison in comparison_inputs:
            shared_position_identity = shared_position["event"].identity
            comparison_identity = comparison["event"].identity
            inputs = _inputs_from_readings(shared_position, comparison)
            _require_input_current_coordinates(ledger, inputs, current_coordinates)
            if (shared_position_identity, comparison_identity) not in assigned:
                subjects.append(
                    SharedPositionMeasurementPairFindingCompareSubject(
                        shared_position_measurement_result_event_identity=shared_position_identity,
                        comparison_result_event_identity=comparison_identity,
                    )
                )
    return tuple(subjects)


def unbound_shared_position_measurement_pair_finding_compare_subjects_in_current_coordinates(
    ledger: EventLedger, *, locality_identity: str
) -> tuple[SharedPositionMeasurementPairFindingCompareSubject, ...]:
    """Read every unassigned exact 04.Compare.B subject in current coordinates.

    The read records no binding, Applicability, Compare, or result occurrence.
    """

    if not isinstance(ledger, EventLedger):
        raise TypeError("shared-position Compare subjects require one EventLedger")
    if type(locality_identity) is not str or not locality_identity:
        raise ValueError("shared-position Compare subjects require one exact Locality")

    from seed_runtime.operator_current_coordinates import (
        read_operator_current_coordinates,
    )

    return _unassigned_shared_position_measurement_pair_finding_compare_subjects_from_current_coordinates(
        ledger,
        locality_identity=locality_identity,
        current_coordinates=read_operator_current_coordinates(
            ledger, locality_identity=locality_identity
        ),
    )


def _active_subject_inputs_from_current_coordinates(
    ledger: EventLedger,
    *,
    locality_identity: str,
    current_coordinates: dict[str, Any],
) -> tuple[dict[str, Any], ...]:
    measurements = current_coordinates.get("measurement_occurrences")
    comparisons = current_coordinates.get("comparison_result_occurrences")
    if (
        current_coordinates.get("locality_identity") != locality_identity
        or type(measurements) is not dict
        or type(comparisons) is not dict
    ):
        raise ValueError(
            "shared-position Compare Applicability has no exact current coordinates"
        )
    shared_position_inputs = tuple(
        _shared_position_input(
            ledger,
            identity,
            prior_coordinates=current_coordinates,
        )
        for identity in measurements
        if (
            (event := ledger.get(identity)) is not None
            and event.kind == SHARED_POSITION_MEASUREMENT_RESULT_KIND
        )
    )
    comparison_inputs = tuple(
        _comparison_input(
            ledger,
            identity,
            prior_coordinates=current_coordinates,
        )
        for identity in comparisons
        if (
            (event := ledger.get(identity)) is not None
            and event.kind == RECORDED_PAIR_MEASUREMENT_COMPARISON_RESULT_KIND
        )
    )
    inputs = tuple(
        _inputs_from_readings(shared_position, comparison)
        for shared_position in shared_position_inputs
        for comparison in comparison_inputs
    )
    for reading in inputs:
        _require_input_current_coordinates(ledger, reading, current_coordinates)
    return inputs


def record_shared_position_measurement_pair_finding_compare_applicability_act_occurrences_from_current_coordinates(
    ledger: EventLedger,
    *,
    locality_identity: str,
    current_coordinates: dict[str, Any] | None = None,
) -> RecordedSharedPositionMeasurementPairFindingCompareApplicabilityActOccurrence:
    """Record one Applicability Act for every exact current cross-set member."""

    from seed_runtime.operator_current_coordinates import (
        read_operator_current_coordinates,
    )

    if current_coordinates is None:
        current_coordinates = read_operator_current_coordinates(
            ledger,
            locality_identity=locality_identity,
        )
    inputs_readings = _active_subject_inputs_from_current_coordinates(
        ledger,
        locality_identity=locality_identity,
        current_coordinates=current_coordinates,
    )
    acts_by_subject: dict[tuple[str, str], tuple[Event, dict[str, Any]]] = {}
    for occurrence in ledger.iter_locality_kind(
        locality_identity,
        COMPARISON_OF_SHARED_POSITION_MEASUREMENT_WITH_RECORDED_PAIR_FINDINGS_APPLICABILITY_ACT_OCCURRENCE_EVENT,
    ):
        if "subject_to_act_binding_reference" in occurrence.material:
            continue
        reading = _read_active_applicability_act(
            ledger,
            occurrence.identity,
            prior_coordinates=current_coordinates,
        )
        key = _active_applicability_subject_key(reading[1])
        if key in acts_by_subject:
            raise ValueError(
                "one shared-position Compare subject carries repeated Applicability Acts"
            )
        acts_by_subject[key] = reading

    recorded: list[Event] = []
    for inputs in inputs_readings:
        key = _active_applicability_subject_key(inputs)
        if key in acts_by_subject:
            continue
        act = _record_active_applicability_act(
            ledger,
            inputs=inputs,
            current_coordinates=current_coordinates,
        )
        acts_by_subject[key] = (act, inputs)
        recorded.append(act)
        current_coordinates = _advance_current_coordinates(
            ledger,
            current_coordinates,
            (act.identity,),
            locality_identity=locality_identity,
        )
    return RecordedSharedPositionMeasurementPairFindingCompareApplicabilityActOccurrence(
        current_coordinates=current_coordinates,
        applicability_act_occurrence_occurrences=tuple(recorded),
    )


def record_shared_position_measurement_pair_finding_compare_bindings_from_current_coordinates(
    ledger: EventLedger,
    *,
    locality_identity: str,
    current_coordinates: dict[str, Any] | None = None,
) -> RecordedSharedPositionMeasurementPairFindingCompareBindings:
    """Record each exact Book-assigned 04.Compare.B subject serially."""

    from seed_runtime.operator_current_coordinates import (
        read_operator_current_coordinates,
    )

    if current_coordinates is None:
        current_coordinates = read_operator_current_coordinates(
            ledger, locality_identity=locality_identity
        )
    elif current_coordinates.get("locality_identity") != locality_identity:
        raise ValueError("shared-position Compare requires exact current Locality")
    subjects = _unassigned_shared_position_measurement_pair_finding_compare_subjects_from_current_coordinates(
        ledger,
        locality_identity=locality_identity,
        current_coordinates=current_coordinates,
    )
    bindings: list[Event] = []
    for subject in subjects:
        binding = record_comparison_of_shared_position_measurement_with_recorded_pair_findings_subject_to_act_binding(
            ledger,
            shared_position_measurement_result_event_identity=subject.shared_position_measurement_result_event_identity,
            comparison_result_event_identity=(
                subject.comparison_result_event_identity
            ),
            current_coordinates=current_coordinates,
        )
        bindings.append(binding)
        current_coordinates = _advance_current_coordinates(
            ledger,
            current_coordinates,
            (binding.identity,),
            locality_identity=locality_identity,
        )
    return RecordedSharedPositionMeasurementPairFindingCompareBindings(
        current_coordinates=current_coordinates,
        binding_occurrences=tuple(bindings),
    )


def record_shared_position_measurement_pair_finding_compare_applicability_from_current_coordinates(
    ledger: EventLedger,
    *,
    locality_identity: str,
    current_coordinates: dict[str, Any] | None = None,
) -> RecordedSharedPositionMeasurementPairFindingCompareApplicability:
    """Record one Applicability result for every exact current cross-set member."""

    act_recording = record_shared_position_measurement_pair_finding_compare_applicability_act_occurrences_from_current_coordinates(
        ledger,
        locality_identity=locality_identity,
        current_coordinates=current_coordinates,
    )
    current_coordinates = act_recording.current_coordinates
    acts: list[tuple[Event, dict[str, Any]]] = []
    results_by_act: dict[str, Event] = {}
    for occurrence in ledger.iter_locality_kind(
        locality_identity,
        COMPARISON_OF_SHARED_POSITION_MEASUREMENT_WITH_RECORDED_PAIR_FINDINGS_APPLICABILITY_ACT_OCCURRENCE_EVENT,
    ):
        if "subject_to_act_binding_reference" in occurrence.material:
            continue
        acts.append(
            _read_active_applicability_act(
                ledger,
                occurrence.identity,
                prior_coordinates=current_coordinates,
            )
        )
    for occurrence in ledger.iter_locality_kind(
        locality_identity,
        COMPARISON_OF_SHARED_POSITION_MEASUREMENT_WITH_RECORDED_PAIR_FINDINGS_APPLICABILITY_RESULT_KIND,
    ):
        act_identity = occurrence.material.get("act_occurrence_event_identity")
        act = ledger.get(act_identity) if type(act_identity) is str else None
        if act is None or "subject_to_act_binding_reference" in act.material:
            continue
        result, result_act, _inputs_reading = _read_active_applicability_result(
            ledger,
            occurrence.identity,
            prior_coordinates=current_coordinates,
        )
        if result_act.identity in results_by_act:
            raise ValueError(
                "one shared-position Compare Applicability Act carries repeated results"
            )
        results_by_act[result_act.identity] = result

    recorded: list[Event] = []
    for act_reading in acts:
        if act_reading[0].identity in results_by_act:
            continue
        result = _record_active_applicability_result(
            ledger,
            applicability_act_reading=act_reading,
        )
        results_by_act[act_reading[0].identity] = result
        recorded.append(result)
        current_coordinates = _advance_current_coordinates(
            ledger,
            current_coordinates,
            (result.identity,),
            locality_identity=locality_identity,
        )

    return RecordedSharedPositionMeasurementPairFindingCompareApplicability(
        current_coordinates=current_coordinates,
        applicability_result_occurrences=tuple(recorded),
    )


def _shared_position_measurement_pair_finding_compare_applicability_results_and_acts(
    ledger: EventLedger,
    *,
    locality_identity: str,
    current_coordinates: dict[str, Any],
) -> tuple[
    SharedPositionMeasurementPairFindingCompareApplicabilityResultActReading,
    tuple[
        tuple[
            Event,
            Event,
            Event,
            dict[str, Any],
            tuple[Event, dict[str, Any]],
        ],
        ...,
    ],
    dict[str, Event],
]:
    current_results = current_coordinates.get("applicability_result_occurrences")
    if (
        current_coordinates.get("locality_identity") != locality_identity
        or type(current_results) is not dict
    ):
        raise ValueError(
            "shared-position Compare requires exact current coordinates"
        )

    applicability_readings = []
    for identity in current_results:
        event = ledger.get(identity)
        if (
            event is None
            or event.kind
            != COMPARISON_OF_SHARED_POSITION_MEASUREMENT_WITH_RECORDED_PAIR_FINDINGS_APPLICABILITY_RESULT_KIND
        ):
            continue
        applicability_readings.append(
            _read_applicability_result(
                ledger,
                event.identity,
                prior_coordinates=current_coordinates,
            )
        )

    through_identity = current_coordinates.get(
        "through_event_occurrence_identity"
    )
    if through_identity is None:
        bounded_events = ()
    else:
        through = ledger.append_boundary_through_occurrence(
            _identity(
                through_identity,
                "shared-position Compare has no exact current boundary",
            )
        )
        bounded_events = tuple(
            event
            for event in ledger.list(through=through)
            if event.locality_identity == locality_identity
        )

    results_by_identity = {
        reading[0].identity: reading for reading in applicability_readings
    }
    acts_by_applicability: dict[str, Event] = {}
    for occurrence in bounded_events:
        if (
            occurrence.kind
            != COMPARISON_OF_SHARED_POSITION_MEASUREMENT_WITH_RECORDED_PAIR_FINDINGS_COMPARE_ACT_OCCURRENCE_EVENT
        ):
            continue
        act, _binding, applicability, _inputs_reading = _read_compare_act(
            ledger,
            occurrence.identity,
            prior_coordinates=current_coordinates,
        )
        if applicability.identity not in results_by_identity:
            raise ValueError(
                "shared-position Compare Act addresses no exact current Applicability result"
            )
        if applicability.identity in acts_by_applicability:
            raise ValueError(
                "shared-position Compare Applicability has repeated Compare Act occurrences"
            )
        acts_by_applicability[applicability.identity] = act

    applicable = tuple(
        reading[0].identity
        for reading in applicability_readings
        if reading[0].material["applicability"] == "applicable"
    )
    inapplicable = tuple(
        reading[0].identity
        for reading in applicability_readings
        if reading[0].material["applicability"] == "inapplicable"
    )
    act_occurrences = tuple(
        (identity, acts_by_applicability[identity].identity)
        for identity in applicable
        if identity in acts_by_applicability
    )
    inapplicable_with_act = tuple(
        identity for identity in inapplicable if identity in acts_by_applicability
    )
    if inapplicable_with_act:
        raise ValueError(
            "inapplicable shared-position Compare results have Compare Act occurrences"
        )
    without_act_occurrence = tuple(
        identity for identity in applicable if identity not in acts_by_applicability
    )
    return (
        SharedPositionMeasurementPairFindingCompareApplicabilityResultActReading(
            through_event_occurrence_identity=through_identity,
            applicable_result_occurrence_identities=applicable,
            inapplicable_result_occurrence_identities=inapplicable,
            act_occurrences_by_applicability_result=act_occurrences,
            applicable_result_occurrence_identities_without_act_occurrence=(
                without_act_occurrence
            ),
        ),
        tuple(applicability_readings),
        acts_by_applicability,
    )


def read_shared_position_measurement_pair_finding_compare_applicability_results_and_acts(
    ledger: EventLedger,
    *,
    locality_identity: str,
    current_coordinates: dict[str, Any] | None = None,
) -> SharedPositionMeasurementPairFindingCompareApplicabilityResultActReading:
    """Read exact Applicability results and their bound Acts through one boundary."""

    if current_coordinates is None:
        from seed_runtime.operator_current_coordinates import (
            read_operator_current_coordinates,
        )

        current_coordinates = read_operator_current_coordinates(
            ledger,
            locality_identity=locality_identity,
        )
    result_act_reading, _readings, _acts = (
        _shared_position_measurement_pair_finding_compare_applicability_results_and_acts(
            ledger,
            locality_identity=locality_identity,
            current_coordinates=current_coordinates,
        )
    )
    return result_act_reading


def record_applicable_shared_position_measurement_pair_finding_compare_act_occurrence_from_current_coordinates(
    ledger: EventLedger,
    *,
    locality_identity: str,
    current_coordinates: dict[str, Any] | None = None,
) -> RecordedSharedPositionMeasurementPairFindingCompareActOccurrence:
    """Record one Compare Act occurrence for each applicable result."""

    from seed_runtime.operator_current_coordinates import (
        read_operator_current_coordinates,
    )

    if current_coordinates is None:
        current_coordinates = read_operator_current_coordinates(
            ledger, locality_identity=locality_identity
        )
    elif current_coordinates.get("locality_identity") != locality_identity:
        raise ValueError("shared-position Compare requires exact current Locality")
    (
        _result_act_reading,
        applicability_readings,
        acts_by_applicability,
    ) = _shared_position_measurement_pair_finding_compare_applicability_results_and_acts(
        ledger,
        locality_identity=locality_identity,
        current_coordinates=current_coordinates,
    )

    recorded: list[Event] = []
    for (
        applicability,
        applicability_act,
        _applicability_binding,
        inputs_reading,
        comparison_binding_reading,
    ) in applicability_readings:
        if applicability.material["applicability"] != "applicable":
            if applicability.identity in acts_by_applicability:
                raise ValueError(
                    "inapplicable shared-position Compare input carries a Compare occurrence"
                )
            continue
        if applicability.identity in acts_by_applicability:
            continue
        if comparison_binding_reading[0] is None:
            act = _record_active_compare_act(
                ledger,
                applicability_result_reading=(
                    applicability,
                    applicability_act,
                    inputs_reading,
                ),
                current_coordinates=current_coordinates,
            )
        else:
            act = record_comparison_of_shared_position_measurement_with_recorded_pair_findings_act_occurrence(
                ledger,
                subject_to_act_binding_event_identity=comparison_binding_reading[
                    0
                ].identity,
                applicability_result_event_identity=applicability.identity,
                current_coordinates=current_coordinates,
            )
        acts_by_applicability[applicability.identity] = act
        recorded.append(act)
        current_coordinates = _advance_current_coordinates(
            ledger,
            current_coordinates,
            (act.identity,),
            locality_identity=locality_identity,
        )

    result_act_reading = read_shared_position_measurement_pair_finding_compare_applicability_results_and_acts(
        ledger,
        locality_identity=locality_identity,
        current_coordinates=current_coordinates,
    )
    if (
        result_act_reading.applicable_result_occurrence_identities_without_act_occurrence
    ):
        raise ValueError(
            "shared-position Compare left exact applicable results without Act occurrences"
        )

    return RecordedSharedPositionMeasurementPairFindingCompareActOccurrence(
        current_coordinates=current_coordinates,
        compare_act_occurrence_occurrences=tuple(recorded),
    )


def record_shared_position_measurement_pair_finding_compare_results_from_current_coordinates(
    ledger: EventLedger,
    *,
    locality_identity: str,
    current_coordinates: dict[str, Any] | None = None,
) -> RecordedSharedPositionMeasurementPairFindingCompareResults:
    """Record one result for each exact current Compare Act occurrence."""

    from seed_runtime.operator_current_coordinates import (
        read_operator_current_coordinates,
    )

    if current_coordinates is None:
        current_coordinates = read_operator_current_coordinates(
            ledger, locality_identity=locality_identity
        )
    elif current_coordinates.get("locality_identity") != locality_identity:
        raise ValueError("shared-position Compare results require exact current Locality")
    acts = []
    for occurrence in ledger.iter_locality_kind(
        locality_identity,
        COMPARISON_OF_SHARED_POSITION_MEASUREMENT_WITH_RECORDED_PAIR_FINDINGS_COMPARE_ACT_OCCURRENCE_EVENT,
    ):
        act, _binding, _applicability, _inputs_reading = _read_compare_act(
            ledger,
            occurrence.identity,
            prior_coordinates=current_coordinates,
        )
        acts.append(act)

    results_by_act: dict[str, Event] = {}
    for occurrence in ledger.iter_locality_kind(
        locality_identity,
        COMPARISON_OF_SHARED_POSITION_MEASUREMENT_WITH_RECORDED_PAIR_FINDINGS_RESULT_KIND,
    ):
        get_recorded_comparison_of_shared_position_measurement_with_recorded_pair_findings(
            ledger,
            occurrence.identity,
            prior_coordinates=current_coordinates,
        )
        act_event_identity = occurrence.material.get(
            "act_occurrence_event_identity"
        )
        if type(act_event_identity) is not str or not act_event_identity:
            raise ValueError(
                "shared-position Compare result carries no exact Act occurrence"
            )
        if act_event_identity in results_by_act:
            raise ValueError(
                "shared-position Compare Act occurrence carries repeated results"
            )
        results_by_act[act_event_identity] = occurrence

    recorded: list[Event] = []
    for act in acts:
        if act.identity in results_by_act:
            continue
        result = record_comparison_of_shared_position_measurement_with_recorded_pair_findings_result(
            ledger,
            act_occurrence_event_identity=act.identity,
            current_coordinates=current_coordinates,
        )
        results_by_act[act.identity] = result
        recorded.append(result)
        current_coordinates = _advance_current_coordinates(
            ledger,
            current_coordinates,
            (result.identity,),
            locality_identity=locality_identity,
        )

    return RecordedSharedPositionMeasurementPairFindingCompareResults(
        current_coordinates=current_coordinates,
        compare_result_occurrences=tuple(recorded),
    )


def _require_input_current_coordinates(
    ledger: EventLedger, inputs: dict[str, Any], current_coordinates: Any
) -> str:
    if (
        type(current_coordinates) is not dict
        or current_coordinates.get("locality_identity") != inputs["locality_identity"]
        or type(current_coordinates.get("measurement_occurrences")) is not dict
        or inputs["shared_position"]["event"].identity
        not in current_coordinates["measurement_occurrences"]
        or type(current_coordinates.get("comparison_result_occurrences")) is not dict
        or inputs["comparison"]["event"].identity
        not in current_coordinates["comparison_result_occurrences"]
    ):
        raise ValueError(
            "comparison of shared-position Measurement result with recorded pair findings requires "
            "each exact result in current coordinates"
        )
    boundary = _identity(
        current_coordinates.get("through_event_occurrence_identity"),
        "comparison of shared-position Measurement result with recorded pair findings requires one exact through-occurrence boundary",
    )
    for occurrence in (
        inputs["shared_position"]["event"].identity,
        inputs["comparison"]["event"].identity,
    ):
        if occurrence == boundary:
            continue
        ordered = ledger.occurrences_in_append_order(
            (occurrence, boundary), locality_identity=inputs["locality_identity"]
        )
        if tuple(event.identity for event in ordered) != (occurrence, boundary):
            raise ValueError(
                "comparison of shared-position Measurement result with recorded pair findings through-occurrence boundary does not carry its inputs"
            )
    return boundary


def _binding_reference(event: Event) -> dict[str, str]:
    return {
        "recorded_occurrence_identity": event.identity,
        "book_clause_identity": event.material["book_clause_identity"],
        "exact_act_identity": event.material["exact_act_identity"],
        "subject_reference": deepcopy(event.material["subject_reference"]),
    }


_IDENTITY_COORDINATES = (
    "exact_act_identity",
    "compare_act_occurrence_identity",
    "compare_result_identity",
)


def _new_identities(ledger: EventLedger) -> dict[str, str]:
    return {
        "exact_act_identity": ledger.mint_identity("comparison_of_shared_position_measurement_with_recorded_pair_findings_compare_act"),
        "compare_act_occurrence_identity": ledger.mint_identity(
            "comparison_of_shared_position_measurement_with_recorded_pair_findings_compare_occurrence"
        ),
        "compare_result_identity": ledger.mint_identity("comparison_of_shared_position_measurement_with_recorded_pair_findings_result"),
    }


def _active_applicability_act_material(
    inputs: dict[str, Any], boundary: str
) -> dict[str, Any]:
    return {
        "subject_reference": {
            "shared_position_result_position_reference": deepcopy(
                inputs["shared_position"]["result_position_reference"]
            ),
            "comparison_result_reference": deepcopy(
                inputs["comparison"]["reference"]
            ),
        },
        "act": _ACTIVE_APPLICABILITY_ACT,
        "addressed_act": _ACTIVE_COMPARE_ACT,
        "through_event_occurrence_identity": boundary,
    }


def _active_applicability_subject_key(
    inputs: dict[str, Any],
) -> tuple[str, str]:
    return (
        inputs["shared_position"]["event"].identity,
        inputs["comparison"]["event"].identity,
    )


def _active_applicability_act_inputs(
    ledger: EventLedger,
    event: Event,
    *,
    prior_coordinates: dict[str, Any] | None,
) -> tuple[dict[str, Any], str]:
    material = event.material
    boundary = material.get("through_event_occurrence_identity")
    if prior_coordinates is None:
        from seed_runtime.operator_current_coordinates import (
            read_operator_current_coordinates_through,
        )

        prior_coordinates = read_operator_current_coordinates_through(
            ledger,
            locality_identity=event.locality_identity,
            through_event_occurrence_identity=boundary,
        )
    subject_reference = material.get("subject_reference")
    shared_reference = (
        subject_reference.get("shared_position_result_position_reference")
        if type(subject_reference) is dict
        else None
    )
    comparison_reference = (
        subject_reference.get("comparison_result_reference")
        if type(subject_reference) is dict
        else None
    )
    inputs = _inputs(
        ledger,
        shared_position_measurement_result_event_identity=(
            shared_reference.get("recorded_occurrence_identity")
            if type(shared_reference) is dict
            else None
        ),
        comparison_result_event_identity=(
            comparison_reference.get("recorded_occurrence_identity")
            if type(comparison_reference) is dict
            else None
        ),
        prior_coordinates=prior_coordinates,
    )
    return inputs, boundary


def _record_active_applicability_act(
    ledger: EventLedger,
    *,
    inputs: dict[str, Any],
    current_coordinates: dict[str, Any],
) -> Event:
    boundary = _require_input_current_coordinates(ledger, inputs, current_coordinates)
    return ledger.append(
        COMPARISON_OF_SHARED_POSITION_MEASUREMENT_WITH_RECORDED_PAIR_FINDINGS_APPLICABILITY_ACT_OCCURRENCE_EVENT,
        _active_applicability_act_material(inputs, boundary),
        locality_identity=inputs["locality_identity"],
    )


def _read_active_applicability_act(
    ledger: EventLedger,
    event_identity: Any,
    *,
    prior_coordinates: dict[str, Any] | None = None,
) -> tuple[Event, dict[str, Any]]:
    event = _event(
        ledger,
        event_identity,
        kind=COMPARISON_OF_SHARED_POSITION_MEASUREMENT_WITH_RECORDED_PAIR_FINDINGS_APPLICABILITY_ACT_OCCURRENCE_EVENT,
        message="comparison of shared-position Measurement result with recorded pair findings has no exact Applicability Act occurrence",
    )
    if "subject_to_act_binding_reference" in event.material:
        raise ValueError(
            "comparison of shared-position Measurement result with recorded pair findings Applicability Act carries an authored binding"
        )
    inputs, boundary = _active_applicability_act_inputs(
        ledger,
        event,
        prior_coordinates=prior_coordinates,
    )
    if (
        type(boundary) is not str
        or event.locality_identity != inputs["locality_identity"]
        or event.material
        != _active_applicability_act_material(inputs, boundary)
    ):
        raise ValueError(
            "comparison of shared-position Measurement result with recorded pair findings Applicability Act coordinates are not exact"
        )
    ordered = ledger.occurrences_in_append_order(
        tuple(dict.fromkeys((boundary, event.identity))),
        locality_identity=event.locality_identity,
    )
    if tuple(item.identity for item in ordered) != tuple(
        dict.fromkeys((boundary, event.identity))
    ):
        raise ValueError(
            "comparison of shared-position Measurement result with recorded pair findings Applicability Act does not follow its boundary"
        )
    return event, inputs


def _binding_material(
    inputs: dict[str, Any], boundary: str, identities: dict[str, str]
) -> dict[str, Any]:
    return {
        "subject_reference": {
            "shared_position_measurement_result_reference": deepcopy(inputs["shared_position"]["reference"]),
            "comparison_result_reference": deepcopy(
                inputs["comparison"]["reference"]
            ),
        },
        "exact_act_identity": identities["exact_act_identity"],
        "compare_act_occurrence_identity": identities[
            "compare_act_occurrence_identity"
        ],
        "compare_result_identity": identities["compare_result_identity"],
        "book_clause_identity": BOOK_CLAUSE,
        "shared_position_measurement_result_reference": deepcopy(inputs["shared_position"]["reference"]),
        "shared_position_result_position_reference": deepcopy(
            inputs["shared_position"]["result_position_reference"]
        ),
        "comparison_result_reference": deepcopy(
            inputs["comparison"]["reference"]
        ),
        "source_material_result_occurrence_identity": inputs["shared_position"]
        ["source_occurrence_identity"],
        "comparison_added_occurrence_identity": inputs["comparison"]
        ["added_occurrence_identity"],
        "pair_subjects": [list(pair) for pair in inputs["shared_position"]["pair_subjects"]],
        "through_event_occurrence_identity": boundary,
    }


def _applicability_binding_material(
    *,
    comparison_binding: Event,
    inputs: dict[str, Any],
    boundary: str,
    identities: dict[str, str],
) -> dict[str, Any]:
    addressed_act_identity = comparison_binding.material["exact_act_identity"]
    return {
        "subject_reference": {
            "shared_position_input": {
                "subject": deepcopy(inputs["shared_position"]["result_position_reference"]),
                "addressed_act_identity": addressed_act_identity,
            },
            "comparison_input": {
                "subject": deepcopy(inputs["comparison"]["reference"]),
                "addressed_act_identity": addressed_act_identity,
            },
        },
        "exact_act_identity": identities["exact_act_identity"],
        "applicability_act_occurrence_identity": identities[
            "applicability_act_occurrence_identity"
        ],
        "applicability_result_identity": identities[
            "applicability_result_identity"
        ],
        "addressed_act_identity": addressed_act_identity,
        "addressed_act_occurrence_identity": comparison_binding.material[
            "compare_act_occurrence_identity"
        ],
        "compare_subject_to_act_binding_reference": _binding_reference(
            comparison_binding
        ),
        "book_clause_identity": "01.Current.E.1",
        "shared_position_measurement_result_reference": deepcopy(inputs["shared_position"]["reference"]),
        "shared_position_result_position_reference": deepcopy(
            inputs["shared_position"]["result_position_reference"]
        ),
        "comparison_result_reference": deepcopy(inputs["comparison"]["reference"]),
        "through_event_occurrence_identity": boundary,
    }


def record_comparison_of_shared_position_measurement_with_recorded_pair_findings_subject_to_act_binding(
    ledger: EventLedger,
    *,
    shared_position_measurement_result_event_identity: str,
    comparison_result_event_identity: str,
    current_coordinates: dict[str, Any],
) -> Event:
    inputs = _inputs(
        ledger,
        shared_position_measurement_result_event_identity=shared_position_measurement_result_event_identity,
        comparison_result_event_identity=comparison_result_event_identity,
        prior_coordinates=current_coordinates,
    )
    boundary = _require_input_current_coordinates(ledger, inputs, current_coordinates)
    identities = _new_identities(ledger)
    if len(set(identities.values())) != len(identities):
        raise ValueError("comparison of shared-position Measurement result with recorded pair findings lifecycle identities collapsed")
    return ledger.append(
        COMPARISON_OF_SHARED_POSITION_MEASUREMENT_WITH_RECORDED_PAIR_FINDINGS_SUBJECT_TO_ACT_BINDING_KIND,
        _binding_material(inputs, boundary, identities),
        locality_identity=inputs["locality_identity"],
    )


def _read_binding(
    ledger: EventLedger,
    event_identity: Any,
    *,
    prior_coordinates: dict[str, Any] | None = None,
) -> tuple[Event, dict[str, Any]]:
    event = _event(
        ledger,
        event_identity,
        kind=COMPARISON_OF_SHARED_POSITION_MEASUREMENT_WITH_RECORDED_PAIR_FINDINGS_SUBJECT_TO_ACT_BINDING_KIND,
        message="comparison of shared-position Measurement result with recorded pair findings requires one exact binding",
    )
    material = event.material
    identities = {key: material.get(key) for key in _IDENTITY_COORDINATES}
    if (
        any(type(value) is not str or not value for value in identities.values())
        or len(set(identities.values())) != len(identities)
    ):
        raise ValueError("comparison of shared-position Measurement result with recorded pair findings binding identities are not exact")
    pair_position_reference = material.get("shared_position_measurement_result_reference")
    comparison_reference = material.get("comparison_result_reference")
    boundary = material.get("through_event_occurrence_identity")
    if prior_coordinates is None:
        from seed_runtime.operator_current_coordinates import (
            read_operator_current_coordinates_through,
        )

        prior_coordinates = read_operator_current_coordinates_through(
            ledger,
            locality_identity=event.locality_identity,
            through_event_occurrence_identity=boundary,
        )
    inputs = _inputs(
        ledger,
        shared_position_measurement_result_event_identity=(
            pair_position_reference.get("recorded_occurrence_identity")
            if type(pair_position_reference) is dict
            else None
        ),
        comparison_result_event_identity=(
            comparison_reference.get("recorded_occurrence_identity")
            if type(comparison_reference) is dict
            else None
        ),
        prior_coordinates=prior_coordinates,
    )
    boundary_event = ledger.get(boundary) if type(boundary) is str else None
    expected = _binding_material(inputs, boundary, identities)
    if (
        boundary_event is None
        or boundary_event.locality_identity != event.locality_identity
        or ledger.integrity_of(boundary_event.identity) == CORRUPTED
        or event.locality_identity != inputs["locality_identity"]
        or material != expected
    ):
        raise ValueError("comparison of shared-position Measurement result with recorded pair findings binding coordinates are not exact")
    for input_event in (inputs["shared_position"]["event"], inputs["comparison"]["event"]):
        ordered_identities = (
            (boundary, event.identity)
            if input_event.identity == boundary
            else (input_event.identity, boundary, event.identity)
        )
        ordered = ledger.occurrences_in_append_order(
            ordered_identities,
            locality_identity=event.locality_identity,
        )
        if tuple(item.identity for item in ordered) != ordered_identities:
            raise ValueError("comparison of shared-position Measurement result with recorded pair findings binding does not follow its inputs")
    return event, inputs


def get_comparison_of_shared_position_measurement_with_recorded_pair_findings_subject_to_act_binding(
    ledger: EventLedger, event_identity: str
) -> dict[str, Any]:
    return deepcopy(_read_binding(ledger, event_identity)[0].material)


def _read_applicability_binding(
    ledger: EventLedger,
    event_identity: Any,
    *,
    comparison_binding_reading: tuple[Event, dict[str, Any]] | None = None,
    prior_coordinates: dict[str, Any] | None = None,
) -> tuple[Event, dict[str, Any], tuple[Event, dict[str, Any]]]:
    event = _event(
        ledger,
        event_identity,
        kind=COMPARISON_OF_SHARED_POSITION_MEASUREMENT_WITH_RECORDED_PAIR_FINDINGS_APPLICABILITY_SUBJECT_TO_ACT_BINDING_KIND,
        message="comparison of shared-position Measurement result with recorded pair findings requires one exact Applicability binding",
    )
    material = event.material
    addressed_act_identity = material.get("addressed_act_identity")
    comparison_binding_reference = material.get(
        "compare_subject_to_act_binding_reference"
    )
    if comparison_binding_reading is None:
        comparison_binding_identity = (
            comparison_binding_reference.get("recorded_occurrence_identity")
            if type(comparison_binding_reference) is dict
            else None
        )
        if type(comparison_binding_identity) is not str or not comparison_binding_identity:
            raise ValueError(
                "comparison of shared-position Measurement result with recorded pair findings "
                "Applicability binding addresses no exact Compare binding"
            )
        comparison_binding_reading = _read_binding(
            ledger,
            comparison_binding_identity,
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
        comparison_binding=comparison_binding,
        inputs=inputs,
        boundary=boundary,
        identities=identities,
    )
    if (
        any(type(value) is not str or not value for value in identities.values())
        or len(set(identities.values())) != len(identities)
        or type(boundary) is not str
        or event.locality_identity != comparison_binding.locality_identity
        or addressed_act_identity
        != comparison_binding.material.get("exact_act_identity")
        or comparison_binding_reference
        != _binding_reference(comparison_binding)
        or material != expected
    ):
        raise ValueError(
            "comparison of shared-position Measurement result with recorded pair findings "
            "Applicability binding coordinates are not exact"
        )
    ordered = ledger.occurrences_in_append_order(
        tuple(dict.fromkeys((comparison_binding.identity, boundary, event.identity))),
        locality_identity=event.locality_identity,
    )
    if tuple(item.identity for item in ordered) != tuple(
        dict.fromkeys((comparison_binding.identity, boundary, event.identity))
    ):
        raise ValueError(
            "comparison of shared-position Measurement result with recorded pair findings "
            "Applicability binding does not follow its Compare binding"
        )
    return event, inputs, comparison_binding_reading


def record_comparison_of_shared_position_measurement_with_recorded_pair_findings_applicability_subject_to_act_binding(
    ledger: EventLedger,
    *,
    comparison_binding_event_identity: str,
    current_coordinates: dict[str, Any],
) -> Event:
    comparison_binding_reading = _read_binding(
        ledger,
        comparison_binding_event_identity,
        prior_coordinates=current_coordinates,
    )
    return _record_comparison_of_shared_position_measurement_with_recorded_pair_findings_applicability_subject_to_act_binding_from_reading(
        ledger,
        comparison_binding_reading=comparison_binding_reading,
        current_coordinates=current_coordinates,
    )


def _record_comparison_of_shared_position_measurement_with_recorded_pair_findings_applicability_subject_to_act_binding_from_reading(
    ledger: EventLedger,
    *,
    comparison_binding_reading: tuple[Event, dict[str, Any]],
    current_coordinates: dict[str, Any],
) -> Event:
    comparison_binding, inputs = comparison_binding_reading
    _require_binding_current_coordinates(comparison_binding, current_coordinates)
    boundary = _identity(
        current_coordinates.get("through_event_occurrence_identity"),
        "comparison of shared-position Measurement result with recorded pair findings "
        "Applicability binding requires one exact through-occurrence boundary",
    )
    identities = {
        "exact_act_identity": ledger.mint_identity(
            "comparison_of_shared_position_measurement_with_recorded_pair_findings_applicability_act"
        ),
        "applicability_act_occurrence_identity": ledger.mint_identity(
            "comparison_of_shared_position_measurement_with_recorded_pair_findings_applicability_occurrence"
        ),
        "applicability_result_identity": ledger.mint_identity(
            "comparison_of_shared_position_measurement_with_recorded_pair_findings_applicability_result"
        ),
    }
    if len(set(identities.values())) != len(identities):
        raise ValueError(
            "comparison of shared-position Measurement result with recorded pair findings "
            "Applicability lifecycle identities are compressed"
        )
    return ledger.append(
        COMPARISON_OF_SHARED_POSITION_MEASUREMENT_WITH_RECORDED_PAIR_FINDINGS_APPLICABILITY_SUBJECT_TO_ACT_BINDING_KIND,
        _applicability_binding_material(
            comparison_binding=comparison_binding,
            inputs=inputs,
            boundary=boundary,
            identities=identities,
        ),
        locality_identity=comparison_binding.locality_identity,
    )


def get_comparison_of_shared_position_measurement_with_recorded_pair_findings_applicability_subject_to_act_binding(
    ledger: EventLedger, event_identity: str
) -> dict[str, Any]:
    return deepcopy(_read_applicability_binding(ledger, event_identity)[0].material)


def _require_binding_current_coordinates(binding: Event, current_coordinates: Any) -> None:
    bindings = (
        current_coordinates.get("subject_to_act_binding_occurrences")
        if type(current_coordinates) is dict
        else None
    )
    if (
        type(current_coordinates) is not dict
        or current_coordinates.get("locality_identity") != binding.locality_identity
        or type(bindings) is not dict
        or bindings.get(binding.identity, object()) is not None
    ):
        raise ValueError("comparison of shared-position Measurement result with recorded pair findings requires its exact binding current coordinates")


def _applicability_act_material(binding: Event) -> dict[str, Any]:
    material = binding.material
    return {
        "applicability_act_identity": material["exact_act_identity"],
        "applicability_act_occurrence_identity": material[
            "applicability_act_occurrence_identity"
        ],
        "result_identity": material["applicability_result_identity"],
        "act": APPLICABILITY_ACT,
        "subject_to_act_binding_reference": _binding_reference(binding),
    }


def record_comparison_of_shared_position_measurement_with_recorded_pair_findings_applicability_act_occurrence(
    ledger: EventLedger,
    *,
    applicability_binding_event_identity: str,
    current_coordinates: dict[str, Any],
) -> Event:
    applicability_binding_reading = _read_applicability_binding(
        ledger,
        applicability_binding_event_identity,
        prior_coordinates=current_coordinates,
    )
    return _record_comparison_of_shared_position_measurement_with_recorded_pair_findings_applicability_act_occurrence_from_reading(
        ledger,
        applicability_binding_reading=applicability_binding_reading,
        current_coordinates=current_coordinates,
    )


def _record_comparison_of_shared_position_measurement_with_recorded_pair_findings_applicability_act_occurrence_from_reading(
    ledger: EventLedger,
    *,
    applicability_binding_reading: tuple[
        Event, dict[str, Any], tuple[Event, dict[str, Any]]
    ],
    current_coordinates: dict[str, Any],
) -> Event:
    binding = applicability_binding_reading[0]
    _require_binding_current_coordinates(binding, current_coordinates)
    return ledger.append(
        COMPARISON_OF_SHARED_POSITION_MEASUREMENT_WITH_RECORDED_PAIR_FINDINGS_APPLICABILITY_ACT_OCCURRENCE_EVENT,
        _applicability_act_material(binding),
        locality_identity=binding.locality_identity,
    )


def _read_applicability_act(
    ledger: EventLedger,
    event_identity: Any,
    *,
    applicability_binding_reading: tuple[
        Event, dict[str, Any], tuple[Event, dict[str, Any]]
    ]
    | None = None,
    comparison_binding_reading: tuple[Event, dict[str, Any]] | None = None,
    prior_coordinates: dict[str, Any] | None = None,
) -> tuple[Event, Event, dict[str, Any], tuple[Event, dict[str, Any]]]:
    event = _event(
        ledger,
        event_identity,
        kind=COMPARISON_OF_SHARED_POSITION_MEASUREMENT_WITH_RECORDED_PAIR_FINDINGS_APPLICABILITY_ACT_OCCURRENCE_EVENT,
        message="comparison of shared-position Measurement result with recorded pair findings requires exact Applicability Act occurrence",
    )
    if "subject_to_act_binding_reference" not in event.material:
        active_event, inputs = _read_active_applicability_act(
            ledger,
            event.identity,
            prior_coordinates=prior_coordinates,
        )
        return active_event, None, inputs, (None, inputs)
    reference = event.material.get("subject_to_act_binding_reference")
    binding_identity = (
        reference.get("recorded_occurrence_identity")
        if type(reference) is dict
        else None
    )
    if applicability_binding_reading is None:
        applicability_binding_reading = _read_applicability_binding(
            ledger,
            binding_identity,
            comparison_binding_reading=comparison_binding_reading,
            prior_coordinates=prior_coordinates,
        )
    binding, inputs, comparison_binding_reading = applicability_binding_reading
    if (
        binding_identity != binding.identity
        or event.locality_identity != binding.locality_identity
        or event.material != _applicability_act_material(binding)
    ):
        raise ValueError("comparison of shared-position Measurement result with recorded pair findings Applicability Act occurrence is not exact")
    return event, binding, inputs, comparison_binding_reading


def get_comparison_of_shared_position_measurement_with_recorded_pair_findings_applicability_act_occurrence(
    ledger: EventLedger, event_identity: str
) -> dict[str, Any]:
    return deepcopy(_read_applicability_act(ledger, event_identity)[0].material)


def _active_applicability_result_material(
    act: Event, inputs: dict[str, Any]
) -> dict[str, Any]:
    applicability = "applicable" if inputs["applicable"] else "inapplicable"
    return {
        "act_occurrence_event_identity": act.identity,
        "applicability": applicability,
    }


def _record_active_applicability_result(
    ledger: EventLedger,
    *,
    applicability_act_reading: tuple[Event, dict[str, Any]],
) -> Event:
    act, inputs = applicability_act_reading
    _refuse_result(
        ledger,
        act,
        COMPARISON_OF_SHARED_POSITION_MEASUREMENT_WITH_RECORDED_PAIR_FINDINGS_APPLICABILITY_RESULT_KIND,
    )
    return ledger.append(
        COMPARISON_OF_SHARED_POSITION_MEASUREMENT_WITH_RECORDED_PAIR_FINDINGS_APPLICABILITY_RESULT_KIND,
        _active_applicability_result_material(act, inputs),
        locality_identity=act.locality_identity,
    )


def _read_active_applicability_result(
    ledger: EventLedger,
    event_identity: Any,
    *,
    prior_coordinates: dict[str, Any] | None = None,
) -> tuple[Event, Event, dict[str, Any]]:
    candidate = ledger.get(event_identity) if type(event_identity) is str else None
    act_identity = (
        candidate.material.get("act_occurrence_event_identity")
        if candidate is not None and type(candidate.material) is dict
        else None
    )
    act, inputs = _read_active_applicability_act(
        ledger,
        act_identity,
        prior_coordinates=prior_coordinates,
    )
    result = _read_exact_result(
        ledger,
        event_identity,
        kind=COMPARISON_OF_SHARED_POSITION_MEASUREMENT_WITH_RECORDED_PAIR_FINDINGS_APPLICABILITY_RESULT_KIND,
        act=act,
        expected=_active_applicability_result_material(act, inputs),
    )
    return result, act, inputs


def _applicability_result_material(
    act: Event, binding: Event, inputs: dict[str, Any]
) -> dict[str, Any]:
    applicability = "applicable" if inputs["applicable"] else "inapplicable"
    return {
        "result_identity": binding.material["applicability_result_identity"],
        "dimensions": {
            "identity": binding.material["applicability_result_identity"],
            "content": {
                "same_source_occurrence": inputs["same_source"],
                "pair_finding_counts": [
                    len(matches) for matches in inputs["shared_position_pair_findings"]
                ],
            },
        },
        "exact_act": APPLICABILITY_ACT,
        "addressed_act_identity": binding.material["addressed_act_identity"],
        "addressed_act_occurrence_identity": (
            binding.material["addressed_act_occurrence_identity"]
            if inputs["applicable"]
            else None
        ),
        "applicability_act_identity": binding.material[
            "exact_act_identity"
        ],
        "applicability_act_occurrence_identity": binding.material[
            "applicability_act_occurrence_identity"
        ],
        "subject_to_act_binding_reference": _binding_reference(binding),
        "act_occurrence_event_identity": act.identity,
        "applicability": applicability,
    }


def _recorded_applicability_result_material(
    result: dict[str, Any],
) -> dict[str, Any]:
    return {
        "result_identity": result["result_identity"],
        "dimensions": deepcopy(result["dimensions"]),
        "exact_act": result["exact_act"],
        "addressed_act_identity": result["addressed_act_identity"],
        "addressed_act_occurrence_identity": result[
            "addressed_act_occurrence_identity"
        ],
        "applicability_act_identity": result["applicability_act_identity"],
        "applicability_act_occurrence_identity": result[
            "applicability_act_occurrence_identity"
        ],
        "subject_to_act_binding_reference": deepcopy(
            result["subject_to_act_binding_reference"]
        ),
        "act_occurrence_event_identity": result[
            "act_occurrence_event_identity"
        ],
        "applicability": result["applicability"],
    }


def _refuse_result(ledger: EventLedger, act: Event, result_kind: str) -> None:
    for occurrence in ledger.iter_locality_kind(act.locality_identity, result_kind):
        if occurrence.material.get("act_occurrence_event_identity") == act.identity:
            raise ValueError("Applicability Act already has a result")


def record_comparison_of_shared_position_measurement_with_recorded_pair_findings_applicability_result(
    ledger: EventLedger,
    *,
    act_occurrence_event_identity: str,
    current_coordinates: dict[str, Any] | None = None,
) -> Event:
    applicability_act_reading = _read_applicability_act(
        ledger,
        act_occurrence_event_identity,
        prior_coordinates=current_coordinates,
    )
    if applicability_act_reading[1] is None:
        return _record_active_applicability_result(
            ledger,
            applicability_act_reading=(
                applicability_act_reading[0],
                applicability_act_reading[2],
            ),
        )
    return _record_comparison_of_shared_position_measurement_with_recorded_pair_findings_applicability_result_from_reading(
        ledger,
        applicability_act_reading=applicability_act_reading,
        current_coordinates=current_coordinates,
    )


def _record_comparison_of_shared_position_measurement_with_recorded_pair_findings_applicability_result_from_reading(
    ledger: EventLedger,
    *,
    applicability_act_reading: tuple[
        Event, Event, dict[str, Any], tuple[Event, dict[str, Any]]
    ],
    current_coordinates: dict[str, Any] | None,
) -> Event:
    act, binding, inputs, _comparison_binding_reading = applicability_act_reading
    result = _applicability_result_material(act, binding, inputs)
    _refuse_result(
        ledger,
        act,
        COMPARISON_OF_SHARED_POSITION_MEASUREMENT_WITH_RECORDED_PAIR_FINDINGS_APPLICABILITY_RESULT_KIND,
    )
    return ledger.append(
        COMPARISON_OF_SHARED_POSITION_MEASUREMENT_WITH_RECORDED_PAIR_FINDINGS_APPLICABILITY_RESULT_KIND,
        _recorded_applicability_result_material(result),
        locality_identity=act.locality_identity,
    )


def _read_exact_result(
    ledger: EventLedger,
    event_identity: Any,
    *,
    kind: str,
    act: Event,
    expected: dict[str, Any],
) -> Event:
    event = _event(ledger, event_identity, kind=kind, message="result is absent")
    results = tuple(
        result
        for result in ledger.iter_locality_kind(act.locality_identity, kind)
        if result.material.get("act_occurrence_event_identity") == act.identity
    )
    try:
        ordered = ledger.occurrences_in_append_order(
            (act.identity, event.identity),
            locality_identity=act.locality_identity,
        )
    except (TypeError, ValueError) as error:
        raise ValueError("Applicability result does not follow its Act") from error
    if (
        event.locality_identity != act.locality_identity
        or event.material != expected
        or tuple(item.identity for item in ordered) != (act.identity, event.identity)
        or len(results) != 1
        or results[0].identity != event.identity
    ):
        raise ValueError("Applicability result is not exact")
    return event


def _read_applicability_result(
    ledger: EventLedger,
    event_identity: Any,
    *,
    applicability_binding_reading: tuple[
        Event, dict[str, Any], tuple[Event, dict[str, Any]]
    ]
    | None = None,
    comparison_binding_reading: tuple[Event, dict[str, Any]] | None = None,
    prior_coordinates: dict[str, Any] | None = None,
) -> tuple[
    Event,
    Event,
    Event,
    dict[str, Any],
    tuple[Event, dict[str, Any]],
]:
    candidate = ledger.get(event_identity) if type(event_identity) is str else None
    act_identity = (
        candidate.material.get("act_occurrence_event_identity")
        if candidate is not None and type(candidate.material) is dict
        else None
    )
    act_candidate = ledger.get(act_identity) if type(act_identity) is str else None
    if (
        act_candidate is not None
        and "subject_to_act_binding_reference" not in act_candidate.material
    ):
        event, act, inputs = _read_active_applicability_result(
            ledger,
            event_identity,
            prior_coordinates=prior_coordinates,
        )
        return event, act, None, inputs, (None, inputs)
    act, binding, inputs, comparison_binding_reading = _read_applicability_act(
        ledger,
        act_identity,
        applicability_binding_reading=applicability_binding_reading,
        comparison_binding_reading=comparison_binding_reading,
        prior_coordinates=prior_coordinates,
    )
    event = _read_exact_result(
        ledger,
        event_identity,
        kind=COMPARISON_OF_SHARED_POSITION_MEASUREMENT_WITH_RECORDED_PAIR_FINDINGS_APPLICABILITY_RESULT_KIND,
        act=act,
        expected=_applicability_result_material(act, binding, inputs),
    )
    return event, act, binding, inputs, comparison_binding_reading


def get_recorded_comparison_of_shared_position_measurement_with_recorded_pair_findings_applicability(
    ledger: EventLedger,
    event_identity: str,
    *,
    prior_coordinates: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return deepcopy(
        _read_applicability_result(
            ledger,
            event_identity,
            prior_coordinates=prior_coordinates,
        )[0].material
    )


def _active_compare_subject_reference(inputs: dict[str, Any]) -> dict[str, Any]:
    return {
        "shared_position_result_position_reference": deepcopy(
            inputs["shared_position"]["result_position_reference"]
        ),
        "comparison_result_reference": deepcopy(inputs["comparison"]["reference"]),
    }


def _active_compare_act_material(
    applicability: Event,
    inputs: dict[str, Any],
) -> dict[str, Any]:
    return {
        "act": _ACTIVE_COMPARE_ACT,
        "subject_reference": _active_compare_subject_reference(inputs),
        "applicability_result_event_identity": applicability.identity,
    }


def _record_active_compare_act(
    ledger: EventLedger,
    *,
    applicability_result_reading: tuple[Event, Event, dict[str, Any]],
    current_coordinates: dict[str, Any],
) -> Event:
    applicability, applicability_act, inputs = applicability_result_reading
    applicable = current_coordinates.get("applicability_result_occurrences")
    if (
        type(applicable) is not dict
        or applicable.get(applicability.identity, object()) is not None
        or current_coordinates.get("locality_identity")
        != applicability.locality_identity
        or applicability.material["applicability"] != "applicable"
        or not inputs["applicable"]
    ):
        raise ValueError(
            "shared-position Compare has no exact applicable current coordinates"
        )
    return ledger.append(
        COMPARISON_OF_SHARED_POSITION_MEASUREMENT_WITH_RECORDED_PAIR_FINDINGS_COMPARE_ACT_OCCURRENCE_EVENT,
        _active_compare_act_material(applicability, inputs),
        locality_identity=applicability.locality_identity,
    )


def _read_active_compare_act(
    ledger: EventLedger,
    event_identity: Any,
    *,
    prior_coordinates: dict[str, Any] | None = None,
) -> tuple[Event, Event, Event, dict[str, Any]]:
    event = _event(
        ledger,
        event_identity,
        kind=COMPARISON_OF_SHARED_POSITION_MEASUREMENT_WITH_RECORDED_PAIR_FINDINGS_COMPARE_ACT_OCCURRENCE_EVENT,
        message="comparison of shared-position Measurement result with recorded pair findings has no exact Compare Act occurrence",
    )
    if "subject_to_act_binding_reference" in event.material:
        raise ValueError(
            "comparison of shared-position Measurement result with recorded pair findings Compare Act carries an authored binding"
        )
    applicability, applicability_act, inputs = _read_active_applicability_result(
        ledger,
        event.material.get("applicability_result_event_identity"),
        prior_coordinates=prior_coordinates,
    )
    if (
        not inputs["applicable"]
        or applicability.material["applicability"] != "applicable"
        or event.locality_identity != applicability.locality_identity
        or event.material
        != _active_compare_act_material(applicability, inputs)
    ):
        raise ValueError(
            "comparison of shared-position Measurement result with recorded pair findings Compare Act coordinates are not exact"
        )
    ordered = ledger.occurrences_in_append_order(
        (applicability.identity, event.identity),
        locality_identity=event.locality_identity,
    )
    if tuple(item.identity for item in ordered) != (
        applicability.identity,
        event.identity,
    ):
        raise ValueError(
            "comparison of shared-position Measurement result with recorded pair findings Compare Act does not follow Applicability"
        )
    return event, applicability_act, applicability, inputs


def _require_compare_current_coordinates(
    binding: Event, applicability: Event, current_coordinates: Any
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
        type(current_coordinates) is not dict
        or current_coordinates.get("locality_identity") != binding.locality_identity
        or type(bindings) is not dict
        or bindings.get(binding.identity, object()) is not None
        or type(applicable) is not dict
        or applicable.get(applicability.identity, object()) is not None
    ):
        raise ValueError("shared-position Compare requires exact Applicability current coordinates")


def _compare_act_material(binding: Event, applicability: Event) -> dict[str, Any]:
    material = binding.material
    return {
        "compare_act_identity": material["exact_act_identity"],
        "act_occurrence_identity": material["compare_act_occurrence_identity"],
        "result_identity": material["compare_result_identity"],
        "act": COMPARE_ACT,
        "subject_to_act_binding_reference": _binding_reference(binding),
        "applicability_result_event_identity": applicability.identity,
    }


def record_comparison_of_shared_position_measurement_with_recorded_pair_findings_act_occurrence(
    ledger: EventLedger,
    *,
    subject_to_act_binding_event_identity: str,
    applicability_result_event_identity: str,
    current_coordinates: dict[str, Any],
) -> Event:
    binding_reading = _read_binding(
        ledger,
        subject_to_act_binding_event_identity,
        prior_coordinates=current_coordinates,
    )
    binding, _inputs_reading = binding_reading
    applicability, _act, _applicability_binding, inputs, applicability_compare_binding_reading = (
        _read_applicability_result(
            ledger,
            applicability_result_event_identity,
            comparison_binding_reading=binding_reading,
        )
    )
    if (
        applicability_compare_binding_reading[0].identity != binding.identity
        or not inputs["applicable"]
        or applicability.material["applicability"] != "applicable"
    ):
        raise ValueError("shared-position input is not applicable to Compare")
    _require_compare_current_coordinates(binding, applicability, current_coordinates)
    return ledger.append(
        COMPARISON_OF_SHARED_POSITION_MEASUREMENT_WITH_RECORDED_PAIR_FINDINGS_COMPARE_ACT_OCCURRENCE_EVENT,
        _compare_act_material(binding, applicability),
        locality_identity=binding.locality_identity,
    )


def _read_compare_act(
    ledger: EventLedger,
    event_identity: Any,
    *,
    prior_coordinates: dict[str, Any] | None = None,
) -> tuple[Event, Event, Event, dict[str, Any]]:
    event = _event(
        ledger,
        event_identity,
        kind=COMPARISON_OF_SHARED_POSITION_MEASUREMENT_WITH_RECORDED_PAIR_FINDINGS_COMPARE_ACT_OCCURRENCE_EVENT,
        message="comparison of shared-position Measurement result with recorded pair findings requires exact Compare Act occurrence",
    )
    if "subject_to_act_binding_reference" not in event.material:
        active_event, _applicability_act, applicability, inputs = (
            _read_active_compare_act(
                ledger,
                event.identity,
                prior_coordinates=prior_coordinates,
            )
        )
        return active_event, None, applicability, inputs
    reference = event.material.get("subject_to_act_binding_reference")
    binding_reading = _read_binding(
        ledger,
        reference.get("recorded_occurrence_identity")
        if type(reference) is dict
        else None,
        prior_coordinates=prior_coordinates,
    )
    binding, inputs = binding_reading
    applicability, _act, _applicability_binding, applicability_inputs, applicability_compare_binding_reading = (
        _read_applicability_result(
            ledger,
            event.material.get("applicability_result_event_identity"),
            comparison_binding_reading=binding_reading,
        )
    )
    if (
        applicability_compare_binding_reading[0].identity != binding.identity
        or applicability_inputs["shared_position"]["event"].identity
        != inputs["shared_position"]["event"].identity
        or applicability_inputs["comparison"]["event"].identity
        != inputs["comparison"]["event"].identity
        or not inputs["applicable"]
        or event.locality_identity != binding.locality_identity
        or event.material != _compare_act_material(binding, applicability)
    ):
        raise ValueError("comparison of shared-position Measurement result with recorded pair findings Compare Act occurrence is not exact")
    return event, binding, applicability, inputs


def get_comparison_of_shared_position_measurement_with_recorded_pair_findings_act_occurrence(
    ledger: EventLedger, event_identity: str
) -> dict[str, Any]:
    return deepcopy(_read_compare_act(ledger, event_identity)[0].material)


def _comparison_finding(inputs: dict[str, Any]) -> dict[str, Any]:
    relation_findings = []
    for pair, pair_position_reference, findings in zip(
        inputs["shared_position"]["pair_subjects"],
        (
            inputs["shared_position"]["result_content"]["subject"][
                "first_position_result_reference"
            ],
            inputs["shared_position"]["result_content"]["subject"][
                "second_position_result_reference"
            ],
        ),
        inputs["shared_position_pair_findings"],
    ):
        relation_findings.append(
            {
                "pair_position_result_reference": deepcopy(pair_position_reference),
                "pair_subject": list(pair),
                "comparison_finding_references": deepcopy(list(findings)),
            }
        )
    subject = {
        "shared_position_result_position_reference": deepcopy(
            inputs["shared_position"]["result_position_reference"]
        ),
        "recorded_pair_comparison_result_reference": deepcopy(
            inputs["comparison"]["reference"]
        ),
    }
    return {
        "subject": subject,
        "relation_findings": relation_findings,
    }


def _compare_result_material(
    act: Event, binding: Event | None, applicability: Event, inputs: dict[str, Any]
) -> dict[str, Any]:
    result = {
        "finding": _comparison_finding(inputs),
        "act_occurrence_event_identity": act.identity,
    }
    if binding is not None:
        result["exact_act"] = COMPARE_ACT
        result["applicability_result_event_identity"] = applicability.identity
        result["compare_act_identity"] = binding.material["exact_act_identity"]
        result["result_identity"] = binding.material["compare_result_identity"]
        result["act_occurrence_identity"] = binding.material[
            "compare_act_occurrence_identity"
        ]
        result["subject_to_act_binding_reference"] = _binding_reference(binding)
    return result


def _recorded_compare_result_material(
    result: dict[str, Any]
) -> dict[str, Any]:
    recorded = {
        "finding": deepcopy(result["finding"]),
        "act_occurrence_event_identity": result[
            "act_occurrence_event_identity"
        ],
    }
    if "subject_to_act_binding_reference" in result:
        recorded["exact_act"] = result["exact_act"]
        recorded["applicability_result_event_identity"] = result[
            "applicability_result_event_identity"
        ]
        recorded["compare_act_identity"] = result["compare_act_identity"]
        recorded["result_identity"] = result["result_identity"]
        recorded["act_occurrence_identity"] = result["act_occurrence_identity"]
        recorded["subject_to_act_binding_reference"] = deepcopy(
            result["subject_to_act_binding_reference"]
        )
    return recorded


def record_comparison_of_shared_position_measurement_with_recorded_pair_findings_result(
    ledger: EventLedger,
    *,
    act_occurrence_event_identity: str,
    current_coordinates: dict[str, Any] | None = None,
) -> Event:
    act, binding, applicability, inputs = _read_compare_act(
        ledger,
        act_occurrence_event_identity,
        prior_coordinates=current_coordinates,
    )
    result = _compare_result_material(act, binding, applicability, inputs)
    prior_results = tuple(
        candidate
        for candidate in ledger.iter_locality_kind(
            act.locality_identity,
            COMPARISON_OF_SHARED_POSITION_MEASUREMENT_WITH_RECORDED_PAIR_FINDINGS_RESULT_KIND,
        )
        if candidate.material.get("act_occurrence_event_identity")
        == act.identity
    )
    if prior_results:
        raise ValueError(
            "one comparison of shared-position Measurement result with recorded pair findings Act cannot record two results"
        )
    return ledger.append(
        COMPARISON_OF_SHARED_POSITION_MEASUREMENT_WITH_RECORDED_PAIR_FINDINGS_RESULT_KIND,
        _recorded_compare_result_material(result),
        locality_identity=act.locality_identity,
    )


def get_recorded_comparison_of_shared_position_measurement_with_recorded_pair_findings(
    ledger: EventLedger,
    event_identity: str,
    *,
    prior_coordinates: dict[str, Any] | None = None,
) -> dict[str, Any]:
    candidate = ledger.get(event_identity) if type(event_identity) is str else None
    act_identity = (
        candidate.material.get("act_occurrence_event_identity")
        if candidate is not None and type(candidate.material) is dict
        else None
    )
    act, binding, applicability, inputs = _read_compare_act(
        ledger,
        act_identity,
        prior_coordinates=prior_coordinates,
    )
    event = _event(
        ledger,
        event_identity,
        kind=COMPARISON_OF_SHARED_POSITION_MEASUREMENT_WITH_RECORDED_PAIR_FINDINGS_RESULT_KIND,
        message="comparison result is absent",
    )
    if (
        event.locality_identity != act.locality_identity
        or event.material
        != _recorded_compare_result_material(
            _compare_result_material(act, binding, applicability, inputs)
        )
    ):
        raise ValueError("comparison result coordinates are not exact")
    try:
        ordered = ledger.occurrences_in_append_order(
            (act.identity, event.identity),
            locality_identity=event.locality_identity,
        )
    except ValueError as error:
        raise ValueError("comparison result does not follow its Act") from error
    if [occurrence.identity for occurrence in ordered] != [
        act.identity,
        event.identity,
    ]:
        raise ValueError("comparison result does not follow its Act")
    results = tuple(
        candidate
        for candidate in ledger.iter_locality_kind(
            event.locality_identity,
            COMPARISON_OF_SHARED_POSITION_MEASUREMENT_WITH_RECORDED_PAIR_FINDINGS_RESULT_KIND,
        )
        if candidate.material.get("act_occurrence_event_identity")
        == act.identity
    )
    if len(results) != 1 or results[0].identity != event.identity:
        raise ValueError("comparison Act has no single exact result")
    return deepcopy(event.material)


def _recorded_shared_position_comparison_finding_result_content_for_locality_movement(
    ledger: EventLedger,
    *,
    result_event_identity: str,
    result_position: int,
) -> dict[str, Any]:
    reading = get_recorded_comparison_of_shared_position_measurement_with_recorded_pair_findings(
        ledger, result_event_identity
    )
    finding = reading.get("finding")
    if (
        type(finding) is not dict
        or result_position != 0
    ):
        raise ValueError(
            "shared-position Compare finding Locality movement requires exact source coordinates"
        )
    return deepcopy(finding)


def move_recorded_shared_position_comparison_finding_result_content_to_locality(
    ledger: EventLedger,
    *,
    comparison_result_occurrence_identity: str,
    destination_locality: str,
) -> dict[str, Any]:
    """Carry one exact recorded shared-position Compare finding through 03.Movement.A."""

    reading = get_recorded_comparison_of_shared_position_measurement_with_recorded_pair_findings(
        ledger, comparison_result_occurrence_identity
    )
    finding = reading.get("finding")
    if type(finding) is not dict:
        raise ValueError(
            "shared-position Compare finding result position movement requires one exact finding"
        )
    from seed_runtime.byte_measurement import (
        _move_result_position_reference_to_locality,
    )

    return _move_result_position_reference_to_locality(
        ledger,
        source_result_position_reference={
            "recorded_occurrence_identity": comparison_result_occurrence_identity,
            "result_position": 0,
        },
        destination_locality=destination_locality,
    )


class RecordedDistinctionPin(NamedTuple):
    locality_identity: str
    through_event_occurrence_identity: str
    comparison_result_occurrence_identity: str
    shared_position_result_position_reference: dict[str, Any]
    pair_position_result_reference: dict[str, Any]
    pair_subject: bytes
    recorded_finding_reference: dict[str, Any]


def recorded_distinction_pins_from_current_coordinates(
    ledger: EventLedger,
    *,
    locality_identity: str,
    current_coordinates: dict[str, Any] | None = None,
) -> tuple[RecordedDistinctionPin, ...]:
    """Read every exact finding-reference branch from recorded results."""

    if not isinstance(ledger, EventLedger):
        raise TypeError("recorded distinction pins require an EventLedger")
    if type(locality_identity) is not str or not locality_identity:
        raise ValueError("recorded distinction pins require one exact Locality")
    from seed_runtime.operator_current_coordinates import (
        read_operator_current_coordinates,
    )

    if current_coordinates is None:
        current_coordinates = read_operator_current_coordinates(
            ledger, locality_identity=locality_identity
        )
    elif current_coordinates.get("locality_identity") != locality_identity:
        raise ValueError("recorded distinction pins require exact current coordinates")
    boundary = current_coordinates.get("through_event_occurrence_identity")
    comparisons = current_coordinates.get("comparison_result_occurrences")
    if type(comparisons) is not dict:
        raise ValueError("recorded distinction pins require exact current coordinates")
    sources = tuple(
        event
        for occurrence_identity in comparisons
        if (
            (event := ledger.get(occurrence_identity)) is not None
            and event.kind
            == COMPARISON_OF_SHARED_POSITION_MEASUREMENT_WITH_RECORDED_PAIR_FINDINGS_RESULT_KIND
        )
    )
    if not sources:
        return ()
    boundary_event = ledger.get(boundary) if type(boundary) is str else None
    locality_occurrences = ledger.list_locality(locality_identity)
    if (
        boundary_event is None
        or boundary_event.locality_identity != locality_identity
        or ledger.integrity_of(boundary_event.identity) == CORRUPTED
        or not locality_occurrences
        or locality_occurrences[-1] != boundary_event
    ):
        raise ValueError("recorded distinction pins require exact current coordinates")
    pins = []
    for event in sources:
        occurrence_identity = event.identity
        coordinates = comparisons[occurrence_identity]
        if coordinates is not None:
            raise ValueError("recorded distinction pin source current coordinates is not exact")
        reading = get_recorded_comparison_of_shared_position_measurement_with_recorded_pair_findings(
            ledger,
            occurrence_identity,
            prior_coordinates=current_coordinates,
        )
        finding = reading.get("finding")
        subject = finding.get("subject") if type(finding) is dict else None
        pair_position_reference = (
            subject.get("shared_position_result_position_reference")
            if type(subject) is dict
            else None
        )
        relation_findings = (
            finding.get("relation_findings") if type(finding) is dict else None
        )
        comparison_reference = (
            subject.get("recorded_pair_comparison_result_reference")
            if type(subject) is dict
            else None
        )
        if (
            type(pair_position_reference) is not dict
            or type(comparison_reference) is not dict
            or type(comparison_reference.get("recorded_occurrence_identity"))
            is not str
            or type(relation_findings) is not list
        ):
            raise ValueError("recorded distinction pin source result is not exact")
        recorded_comparison_event = ledger.get(
            comparison_reference["recorded_occurrence_identity"]
        )
        if recorded_comparison_event is None:
            raise ValueError("recorded distinction pin source result is not exact")
        recorded_comparison_material = (
            _recorded_pair_measurement_comparison_reading(
                ledger,
                recorded_comparison_event.identity,
                prior_coordinates=current_coordinates,
            )[0]
        )
        for relation_finding in relation_findings:
            position_reference = (
                relation_finding.get("pair_position_result_reference")
                if type(relation_finding) is dict
                else None
            )
            pair_subject = (
                relation_finding.get("pair_subject")
                if type(relation_finding) is dict
                else None
            )
            references = (
                relation_finding.get("comparison_finding_references")
                if type(relation_finding) is dict
                else None
            )
            if (
                type(position_reference) is not dict
                or type(pair_subject) is not list
                or len(pair_subject) != 2
                or not all(
                    type(value) is int and 0 <= value <= 255
                    for value in pair_subject
                )
                or type(references) is not list
            ):
                raise ValueError("recorded distinction pin coordinates are not exact")
            for reference in references:
                try:
                    addressed_finding = _addressed_comparison_finding(
                        recorded_comparison_event,
                        recorded_comparison_material,
                        reference,
                    )
                except ValueError as error:
                    raise ValueError(
                        "recorded distinction pin reference is not exact"
                    ) from error
                if addressed_finding["subject"].get("content") != pair_subject:
                    raise ValueError("recorded distinction pin reference is not exact")
                pins.append(
                    RecordedDistinctionPin(
                        locality_identity,
                        boundary,
                        occurrence_identity,
                        deepcopy(pair_position_reference),
                        deepcopy(position_reference),
                        bytes(pair_subject),
                        deepcopy(reference),
                    )
                )
    if (
        ledger.get(boundary_event.identity) != boundary_event
        or ledger.integrity_of(boundary_event.identity) == CORRUPTED
        or not (current_locality_occurrences := ledger.list_locality(locality_identity))
        or current_locality_occurrences[-1] != boundary_event
    ):
        raise ValueError("recorded distinction pins require one unchanged current coordinates pin")
    return tuple(pins)
