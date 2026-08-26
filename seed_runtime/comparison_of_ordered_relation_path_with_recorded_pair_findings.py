"""Compare one yielded relation path with exact recorded pair findings."""

from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from typing import TYPE_CHECKING, Any, NamedTuple

if TYPE_CHECKING:
    from seed_runtime.byte_measurement import (
        RecordedAssertionCarriedByLocalityMovement,
    )

from seed_runtime.comparison_of_recorded_byte_pair_measurements import (
    RECORDED_PAIR_MEASUREMENT_COMPARISON_RESULT_KIND,
    _recorded_pair_measurement_comparison_reading,
)
from seed_runtime.event import Event
from seed_runtime.events import CORRUPTED, EventLedger
from seed_runtime.yield_relation import (
    RECORDED_YIELD_RELATION_EVENT,
    _record_yield_relation,
    read_requirements_of_yield_relation,
)
from seed_runtime.measurement_of_shared_position_of_byte_pair_occurrences import (
    SHARED_POSITION_MEASUREMENT_RESULT_KIND,
    get_recorded_shared_position_measurement,
)


COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_SUBJECT_TO_ACT_BINDING_KIND = (
    "operator.comparison_of_ordered_relation_path_with_recorded_pair_findings.subject_to_act_binding_recorded"
)
COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_APPLICABILITY_SUBJECT_TO_ACT_BINDING_KIND = (
    "operator.comparison_of_ordered_relation_path_with_recorded_pair_findings.applicability_subject_to_act_binding_recorded"
)
COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_APPLICABILITY_ACT_OCCURRENCE_EVENT = (
    "operator.comparison_of_ordered_relation_path_with_recorded_pair_findings.applicability_act_occurrence_recorded"
)
COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_APPLICABILITY_RESULT_KIND = (
    "operator.comparison_of_ordered_relation_path_with_recorded_pair_findings.applicability_recorded"
)
COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_COMPARE_ACT_OCCURRENCE_EVENT = (
    "operator.comparison_of_ordered_relation_path_with_recorded_pair_findings.compare_act_occurrence_recorded"
)
COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_RESULT_KIND = "operator.comparison_of_ordered_relation_path_with_recorded_pair_findings.recorded"

BOOK_CLAUSE = "04.Compare.B"
APPLICABILITY_ACT = (
    "Applicability of one ordered relation path and one recorded pair Compare "
    "result to one Compare"
)
COMPARE_ACT = (
    "Compare each relation of one ordered path with complete recorded findings "
    "of the same exact pair subject"
)
COMPARISON_RULE = (
    "the path source is the exact added Compare occurrence and each path pair "
    "subject carries complete recorded Compare findings"
)
APPLICABILITY_RESULT_KIND = (
    "Applicability result of ordered relation path and recorded pair findings"
)
COMPARE_RESULT_KIND = (
    "Compare result of ordered relation path and recorded pair findings"
)

EVENT_KIND_BOOK_CLAUSES = {
    COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_SUBJECT_TO_ACT_BINDING_KIND: "04.Compare.B",
    COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_APPLICABILITY_SUBJECT_TO_ACT_BINDING_KIND: "01.Current.E.1",
    COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_APPLICABILITY_ACT_OCCURRENCE_EVENT: "02.Acts.A",
    COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_APPLICABILITY_RESULT_KIND: "01.Current.E.1",
    COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_COMPARE_ACT_OCCURRENCE_EVENT: "02.Acts.A",
    COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_RESULT_KIND: "04.Compare.B",
}

_FINDING_CATEGORIES = (
    "same_content_findings",
    "conflicting_findings",
    "findings_of_earlier_result",
    "findings_of_later_result",
    "unknown_findings",
)


class OrderedPathPairFindingCompareSubject(NamedTuple):
    path_result_event_identity: str
    comparison_result_event_identity: str


class RecordedOrderedPathPairFindingCompareBindings(NamedTuple):
    current_coordinates: dict[str, Any]
    binding_occurrences: tuple[Event, ...]


class RecordedOrderedPathPairFindingCompareApplicability(NamedTuple):
    current_coordinates: dict[str, Any]
    applicability_result_occurrences: tuple[Event, ...]


class RecordedOrderedPathPairFindingCompareActOccurrence(NamedTuple):
    current_coordinates: dict[str, Any]
    compare_act_occurrence_occurrences: tuple[Event, ...]


class RecordedOrderedPathPairFindingCompareResults(NamedTuple):
    current_coordinates: dict[str, Any]
    compare_result_occurrences: tuple[Event, ...]


def _identity(value: Any, message: str) -> str:
    if type(value) is not str or not value:
        raise ValueError(message)
    return value


def _advance_carried_current_coordinates(
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
        "yield_relation_identity": event.material[
            "yield_relation_identity"
        ],
    }


def _path_input(
    ledger: EventLedger,
    event_identity: Any,
    *,
    prior_coordinates: dict[str, Any] | None = None,
) -> dict[str, Any]:
    event = _event(
        ledger,
        event_identity,
        kind=SHARED_POSITION_MEASUREMENT_RESULT_KIND,
        message="comparison of ordered relation path with recorded pair findings requires one exact path Measurement result",
    )
    material = get_recorded_shared_position_measurement(
        ledger,
        event.identity,
        prior_coordinates=prior_coordinates,
    )
    assertions = material.get("assertions")
    if type(assertions) is not list or len(assertions) != 1:
        raise ValueError("comparison of ordered relation path with recorded pair findings requires one exact path Assertion")
    assertion = assertions[0]
    first = material.get("first_position_assertion")
    second = material.get("second_position_assertion")
    if (
        type(assertion) is not dict
        or assertion.get("result") != "ordered_relation_path"
        or type(first) is not dict
        or type(second) is not dict
        or assertion.get("assertion_subject", {}).get(
            "first_position_assertion_reference"
        )
        != first.get("assertion_reference")
        or assertion.get("assertion_subject", {}).get(
            "second_position_assertion_reference"
        )
        != second.get("assertion_reference")
    ):
        raise ValueError("comparison of ordered relation path with recorded pair findings requires one exact path Assertion")
    pairs = (first.get("exact_pair"), second.get("exact_pair"))
    if any(
        type(pair) is not list
        or len(pair) != 2
        or any(type(value) is not int or not 0 <= value <= 255 for value in pair)
        for pair in pairs
    ):
        raise ValueError("comparison of ordered relation path with recorded pair findings requires exact pair subjects")
    content = assertion.get("dimensions", {}).get("content")
    assertion_position = assertion.get("dimensions", {}).get("position")
    if assertion_position != 0:
        raise ValueError("comparison of ordered relation path with recorded pair findings requires one exact path Assertion")
    source = (
        content.get("source_material_result_occurrence_identity")
        if type(content) is dict
        else None
    )
    return {
        "event": event,
        "reference": _result_reference(event),
        "assertion": deepcopy(assertion),
        "assertion_reference": {
            "recorded_occurrence_identity": event.identity,
            "assertion_position": assertion_position,
        },
        "pair_subjects": tuple(tuple(pair) for pair in pairs),
        "source_occurrence_identity": _identity(
            source, "comparison of ordered relation path with recorded pair findings requires one exact path source occurrence"
        ),
    }


def _comparison_finding_references(
    comparison_event: Event, comparison: dict[str, Any]
) -> tuple[dict[str, Any], ...]:
    findings = comparison.get("findings")
    if type(findings) is not dict or tuple(findings) != _FINDING_CATEGORIES:
        raise ValueError("comparison of ordered relation path with recorded pair findings requires complete comparison findings")
    references = []
    for category in _FINDING_CATEGORIES:
        entries = findings.get(category)
        if type(entries) is not list:
            raise ValueError(
                "comparison of ordered relation path with recorded pair findings requires complete comparison findings"
            )
        for position, entry in enumerate(entries):
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
                    "comparison of ordered relation path with recorded pair findings requires complete comparison findings"
                )
            references.append(
                {
                    "recorded_comparison_occurrence_identity": (
                        comparison_event.identity
                    ),
                    "finding_category": category,
                    "finding_position": position,
                    "subject": deepcopy(subject),
                }
            )
    return tuple(references)


def _comparison_input(ledger: EventLedger, event_identity: Any) -> dict[str, Any]:
    event = _event(
        ledger,
        event_identity,
        kind=RECORDED_PAIR_MEASUREMENT_COMPARISON_RESULT_KIND,
        message="comparison of ordered relation path with recorded pair findings requires one exact recorded comparison result",
    )
    material, binding_reading = (
        _recorded_pair_measurement_comparison_reading(ledger, event.identity)
    )
    binding = binding_reading[0]
    binding_reference = material.get("subject_to_act_binding_reference")
    binding_identity = (
        binding_reference.get("recorded_occurrence_identity")
        if type(binding_reference) is dict
        else None
    )
    if (
        binding.identity != binding_identity
        or binding.material.get("comparison_result_identity")
        != material.get("result_identity")
    ):
        raise ValueError(
            "comparison of ordered relation path with recorded pair findings "
            "carries another Compare binding"
        )
    return {
        "event": event,
        "reference": _result_reference(event),
        "binding_event_identity": binding.identity,
        "added_occurrence_identity": binding.material[
            "added_occurrence_reference"
        ],
        "finding_references": _comparison_finding_references(event, material),
    }


def _path_relation_findings(
    references: tuple[dict[str, Any], ...], pair: tuple[int, int]
) -> tuple[dict[str, Any], ...]:
    return tuple(
        reference
        for reference in references
        if tuple(reference["subject"]["content"]) == pair
    )


def _inputs(
    ledger: EventLedger,
    *,
    path_result_event_identity: Any,
    comparison_result_event_identity: Any,
    prior_coordinates: dict[str, Any] | None = None,
) -> dict[str, Any]:
    path = _path_input(
        ledger,
        path_result_event_identity,
        prior_coordinates=prior_coordinates,
    )
    comparison = _comparison_input(ledger, comparison_result_event_identity)
    if path["event"].locality_identity != comparison["event"].locality_identity:
        raise ValueError("comparison of ordered relation path with recorded pair findings requires one exact Locality")
    matches = tuple(
        _path_relation_findings(comparison["finding_references"], pair)
        for pair in path["pair_subjects"]
    )
    return {
        "locality_identity": path["event"].locality_identity,
        "path": path,
        "comparison": comparison,
        "path_relation_findings": matches,
        "same_source": (
            path["source_occurrence_identity"]
            == comparison["added_occurrence_identity"]
        ),
        "applicable": all(matches)
        and path["source_occurrence_identity"]
        == comparison["added_occurrence_identity"],
    }


def _unassigned_ordered_path_pair_finding_compare_subjects_from_current_coordinates(
    ledger: EventLedger,
    *,
    locality_identity: str,
    current_coordinates: dict[str, Any],
) -> tuple[OrderedPathPairFindingCompareSubject, ...]:
    measurement_occurrences = current_coordinates.get("measurement_occurrences")
    comparison_occurrences = current_coordinates.get("comparison_result_occurrences")
    if (
        type(measurement_occurrences) is not dict
        or type(comparison_occurrences) is not dict
    ):
        raise ValueError(
            "ordered-path Compare subjects require exact current coordinates"
        )

    path_identities = tuple(
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

    assigned: set[tuple[str, str]] = set()
    for occurrence in ledger.iter_locality_kind(
        locality_identity,
        COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_SUBJECT_TO_ACT_BINDING_KIND,
    ):
        binding, inputs = _read_binding(ledger, occurrence.identity)
        assigned.add(
            (
                inputs["path"]["event"].identity,
                inputs["comparison"]["event"].identity,
            )
        )
        if binding.locality_identity != locality_identity:
            raise ValueError(
                "ordered-path Compare binding belongs to another Locality"
            )

    subjects = []
    for path_identity in path_identities:
        for comparison_identity in comparison_identities:
            inputs = _inputs(
                ledger,
                path_result_event_identity=path_identity,
                comparison_result_event_identity=comparison_identity,
            )
            _require_input_current_coordinates(ledger, inputs, current_coordinates)
            if (path_identity, comparison_identity) not in assigned:
                subjects.append(
                    OrderedPathPairFindingCompareSubject(
                        path_result_event_identity=path_identity,
                        comparison_result_event_identity=comparison_identity,
                    )
                )
    return tuple(subjects)


def unbound_ordered_path_pair_finding_compare_subjects_in_current_coordinates(
    ledger: EventLedger, *, locality_identity: str
) -> tuple[OrderedPathPairFindingCompareSubject, ...]:
    """Read every unassigned exact 04.Compare.B subject in current coordinates.

    The read records no binding, Applicability, Participation, Compare, or
    result occurrence.
    """

    if not isinstance(ledger, EventLedger):
        raise TypeError("ordered-path Compare subjects require one EventLedger")
    if type(locality_identity) is not str or not locality_identity:
        raise ValueError("ordered-path Compare subjects require one exact Locality")

    from seed_runtime.operator_current_coordinates import (
        read_operator_current_coordinates,
    )

    return _unassigned_ordered_path_pair_finding_compare_subjects_from_current_coordinates(
        ledger,
        locality_identity=locality_identity,
        current_coordinates=read_operator_current_coordinates(
            ledger, locality_identity=locality_identity
        ),
    )


def record_ordered_path_pair_finding_compare_bindings_from_current_coordinates(
    ledger: EventLedger, *, locality_identity: str
) -> RecordedOrderedPathPairFindingCompareBindings:
    """Record each exact Book-assigned 04.Compare.B subject serially."""

    from seed_runtime.operator_current_coordinates import (
        read_operator_current_coordinates,
    )

    current_coordinates = read_operator_current_coordinates(
        ledger, locality_identity=locality_identity
    )
    subjects = _unassigned_ordered_path_pair_finding_compare_subjects_from_current_coordinates(
        ledger,
        locality_identity=locality_identity,
        current_coordinates=current_coordinates,
    )
    bindings: list[Event] = []
    for subject in subjects:
        binding = record_comparison_of_ordered_relation_path_with_recorded_pair_findings_subject_to_act_binding(
            ledger,
            path_result_event_identity=subject.path_result_event_identity,
            comparison_result_event_identity=(
                subject.comparison_result_event_identity
            ),
            current_coordinates=current_coordinates,
        )
        bindings.append(binding)
        current_coordinates = _advance_carried_current_coordinates(
            ledger,
            current_coordinates,
            (binding.identity,),
            locality_identity=locality_identity,
        )
    return RecordedOrderedPathPairFindingCompareBindings(
        current_coordinates=current_coordinates,
        binding_occurrences=tuple(bindings),
    )


def record_ordered_path_pair_finding_compare_applicability_from_current_coordinates(
    ledger: EventLedger, *, locality_identity: str
) -> RecordedOrderedPathPairFindingCompareApplicability:
    """Record Applicability once for each exact current 04.Compare.B binding."""

    from seed_runtime.operator_current_coordinates import (
        read_operator_current_coordinates,
    )

    current_coordinates = read_operator_current_coordinates(
        ledger, locality_identity=locality_identity
    )
    current_bindings = current_coordinates.get("subject_to_act_binding_occurrences")
    if type(current_bindings) is not dict:
        raise ValueError(
            "ordered-path Compare Applicability requires exact current coordinates"
        )
    bindings = tuple(
        event
        for identity in current_bindings
        if (
            (event := ledger.get(identity)) is not None
            and event.kind
            == COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_SUBJECT_TO_ACT_BINDING_KIND
        )
    )
    for binding in bindings:
        _read_binding(ledger, binding.identity)

    applicability_bindings_by_compare_act: dict[str, Event] = {}
    for occurrence in ledger.iter_locality_kind(
        locality_identity,
        COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_APPLICABILITY_SUBJECT_TO_ACT_BINDING_KIND,
    ):
        applicability_binding, _inputs, comparison_binding_reading = (
            _read_applicability_binding(ledger, occurrence.identity)
        )
        compare_act_identity = comparison_binding_reading[0].material[
            "exact_act_identity"
        ]
        if compare_act_identity in applicability_bindings_by_compare_act:
            raise ValueError(
                "ordered-path Compare carries repeated Applicability binding"
            )
        applicability_bindings_by_compare_act[compare_act_identity] = (
            applicability_binding
        )

    for binding in bindings:
        compare_act_identity = binding.material["exact_act_identity"]
        if compare_act_identity in applicability_bindings_by_compare_act:
            continue
        applicability_binding = record_comparison_of_ordered_relation_path_with_recorded_pair_findings_applicability_subject_to_act_binding(
            ledger,
            comparison_binding_event_identity=binding.identity,
            current_coordinates=current_coordinates,
        )
        applicability_bindings_by_compare_act[compare_act_identity] = (
            applicability_binding
        )
        current_coordinates = _advance_carried_current_coordinates(
            ledger,
            current_coordinates,
            (applicability_binding.identity,),
            locality_identity=locality_identity,
        )

    applicability_bindings = tuple(
        applicability_bindings_by_compare_act[binding.material["exact_act_identity"]]
        for binding in bindings
    )
    acts_by_binding: dict[str, Event] = {}
    for occurrence in ledger.iter_locality_kind(
        locality_identity,
        COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_APPLICABILITY_ACT_OCCURRENCE_EVENT,
    ):
        act, binding, _inputs_reading, _comparison_binding_reading = _read_applicability_act(
            ledger, occurrence.identity
        )
        if binding.identity in acts_by_binding:
            raise ValueError(
                "ordered-path Compare binding carries repeated Applicability Act occurrence"
            )
        acts_by_binding[binding.identity] = act

    results_by_binding: dict[str, Event] = {}
    for occurrence in ledger.iter_locality_kind(
        locality_identity,
        COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_APPLICABILITY_RESULT_KIND,
    ):
        result, _act, binding, _inputs_reading, _comparison_binding_reading = _read_applicability_result(
            ledger, occurrence.identity
        )
        if binding.identity in results_by_binding:
            raise ValueError(
                "ordered-path Compare binding carries repeated Applicability result"
            )
        results_by_binding[binding.identity] = result

    recorded: list[Event] = []
    for binding in applicability_bindings:
        if binding.identity in results_by_binding:
            continue
        act = acts_by_binding.get(binding.identity)
        if act is None:
            act = record_comparison_of_ordered_relation_path_with_recorded_pair_findings_applicability_act_occurrence(
                ledger,
                applicability_binding_event_identity=binding.identity,
                current_coordinates=current_coordinates,
            )
            acts_by_binding[binding.identity] = act
            current_coordinates = _advance_carried_current_coordinates(
                ledger,
                current_coordinates,
                (act.identity,),
                locality_identity=locality_identity,
            )
        result = record_comparison_of_ordered_relation_path_with_recorded_pair_findings_applicability_result(
            ledger,
            act_occurrence_event_identity=act.identity,
        )
        results_by_binding[binding.identity] = result
        recorded.append(result)
        current_coordinates = _advance_carried_current_coordinates(
            ledger,
            current_coordinates,
            (
                result.material["yield_relation_identity"],
                result.identity,
            ),
            locality_identity=locality_identity,
        )

    return RecordedOrderedPathPairFindingCompareApplicability(
        current_coordinates=current_coordinates,
        applicability_result_occurrences=tuple(recorded),
    )


def record_applicable_ordered_path_pair_finding_compare_act_occurrence_from_current_coordinates(
    ledger: EventLedger, *, locality_identity: str
) -> RecordedOrderedPathPairFindingCompareActOccurrence:
    """Record Compare Act occurrence and Participation for each applicable result."""

    from seed_runtime.operator_current_coordinates import (
        read_operator_current_coordinates,
    )

    current_coordinates = read_operator_current_coordinates(
        ledger, locality_identity=locality_identity
    )
    current_results = current_coordinates.get("applicability_result_occurrences")
    if type(current_results) is not dict:
        raise ValueError(
            "ordered-path Compare Participation requires exact current coordinates"
        )
    applicability_readings = []
    for identity in current_results:
        event = ledger.get(identity)
        if (
            event is None
            or event.kind
            != COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_APPLICABILITY_RESULT_KIND
        ):
            continue
        applicability_readings.append(
            _read_applicability_result(ledger, event.identity)
        )

    acts_by_applicability: dict[str, Event] = {}
    for occurrence in ledger.iter_locality_kind(
        locality_identity,
        COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_COMPARE_ACT_OCCURRENCE_EVENT,
    ):
        act, _binding, applicability, _inputs_reading = _read_compare_act(
            ledger, occurrence.identity
        )
        if applicability.identity in acts_by_applicability:
            raise ValueError(
                "ordered-path Compare Applicability carries repeated Compare Act occurrence"
            )
        acts_by_applicability[applicability.identity] = act

    recorded: list[Event] = []
    for (
        applicability,
        _act,
        _applicability_binding,
        _inputs_reading,
        comparison_binding_reading,
    ) in applicability_readings:
        if applicability.material["applicability"] != "applicable":
            if applicability.identity in acts_by_applicability:
                raise ValueError(
                    "inapplicable ordered-path Compare input carries Participation"
                )
            continue
        if applicability.identity in acts_by_applicability:
            continue
        act = record_comparison_of_ordered_relation_path_with_recorded_pair_findings_act_occurrence(
            ledger,
            subject_to_act_binding_event_identity=comparison_binding_reading[0].identity,
            applicability_result_event_identity=applicability.identity,
            current_coordinates=current_coordinates,
        )
        acts_by_applicability[applicability.identity] = act
        recorded.append(act)
        current_coordinates = _advance_carried_current_coordinates(
            ledger,
            current_coordinates,
            (act.identity,),
            locality_identity=locality_identity,
        )

    return RecordedOrderedPathPairFindingCompareActOccurrence(
        current_coordinates=current_coordinates,
        compare_act_occurrence_occurrences=tuple(recorded),
    )


def record_ordered_path_pair_finding_compare_results_from_current_coordinates(
    ledger: EventLedger, *, locality_identity: str
) -> RecordedOrderedPathPairFindingCompareResults:
    """Record one Yield and result for each exact current Compare Act occurrence."""

    from seed_runtime.operator_current_coordinates import (
        read_operator_current_coordinates,
    )

    current_coordinates = read_operator_current_coordinates(
        ledger, locality_identity=locality_identity
    )
    acts = []
    for occurrence in ledger.iter_locality_kind(
        locality_identity,
        COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_COMPARE_ACT_OCCURRENCE_EVENT,
    ):
        act, _binding, _applicability, _inputs_reading = _read_compare_act(
            ledger, occurrence.identity
        )
        acts.append(act)

    results_by_act: dict[str, Event] = {}
    for occurrence in ledger.iter_locality_kind(
        locality_identity,
        COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_RESULT_KIND,
    ):
        get_recorded_comparison_of_ordered_relation_path_with_recorded_pair_findings(
            ledger, occurrence.identity
        )
        act_identity = occurrence.material.get("act_occurrence_identity")
        if type(act_identity) is not str or not act_identity:
            raise ValueError(
                "ordered-path Compare result carries no exact Act occurrence"
            )
        if act_identity in results_by_act:
            raise ValueError(
                "ordered-path Compare Act occurrence carries repeated results"
            )
        results_by_act[act_identity] = occurrence

    recorded: list[Event] = []
    for act in acts:
        if act.identity in results_by_act:
            continue
        result = record_comparison_of_ordered_relation_path_with_recorded_pair_findings_result(
            ledger,
            act_occurrence_event_identity=act.identity,
        )
        results_by_act[act.identity] = result
        recorded.append(result)
        current_coordinates = _advance_carried_current_coordinates(
            ledger,
            current_coordinates,
            (
                result.material["yield_relation_identity"],
                result.identity,
            ),
            locality_identity=locality_identity,
        )

    return RecordedOrderedPathPairFindingCompareResults(
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
        or inputs["path"]["event"].identity
        not in current_coordinates["measurement_occurrences"]
        or type(current_coordinates.get("comparison_result_occurrences")) is not dict
        or inputs["comparison"]["event"].identity
        not in current_coordinates["comparison_result_occurrences"]
    ):
        raise ValueError(
            "comparison of ordered relation path with recorded pair findings requires "
            "each exact result in current coordinates"
        )
    boundary = _identity(
        current_coordinates.get("through_event_occurrence_identity"),
        "comparison of ordered relation path with recorded pair findings requires one exact through-occurrence boundary",
    )
    for occurrence in (
        inputs["path"]["event"].identity,
        inputs["comparison"]["event"].identity,
    ):
        if occurrence == boundary:
            continue
        ordered = ledger.occurrences_in_append_order(
            (occurrence, boundary), locality_identity=inputs["locality_identity"]
        )
        if tuple(event.identity for event in ordered) != (occurrence, boundary):
            raise ValueError(
                "comparison of ordered relation path with recorded pair findings through-occurrence boundary does not carry its inputs"
            )
    return boundary


def _binding_reference(
    event: Event, *, result_boundary_identity: str
) -> dict[str, str]:
    return {
        "recorded_occurrence_identity": event.identity,
        "book_clause_identity": event.material["book_clause_identity"],
        "exact_act_identity": event.material["exact_act_identity"],
        "subject_reference": deepcopy(event.material["subject_reference"]),
        "result_boundary_identity": result_boundary_identity,
    }


_IDENTITY_COORDINATES = (
    "compare_act_identity",
    "compare_act_occurrence_identity",
    "compare_result_identity",
)


def _new_identities(ledger: EventLedger) -> dict[str, str]:
    return {
        "compare_act_identity": ledger.mint_identity("comparison_of_ordered_relation_path_with_recorded_pair_findings_compare_act"),
        "compare_act_occurrence_identity": ledger.mint_identity(
            "comparison_of_ordered_relation_path_with_recorded_pair_findings_compare_occurrence"
        ),
        "compare_result_identity": ledger.mint_identity("comparison_of_ordered_relation_path_with_recorded_pair_findings_result"),
    }


def _binding_material(
    inputs: dict[str, Any], boundary: str, identities: dict[str, str]
) -> dict[str, Any]:
    return {
        "subject_reference": {
            "path_result_reference": deepcopy(inputs["path"]["reference"]),
            "comparison_result_reference": deepcopy(
                inputs["comparison"]["reference"]
            ),
        },
        "exact_act_identity": identities["compare_act_identity"],
        "compare_act_identity": identities["compare_act_identity"],
        "compare_act_occurrence_identity": identities[
            "compare_act_occurrence_identity"
        ],
        "compare_result_identity": identities["compare_result_identity"],
        "result_boundary_identity": identities["compare_result_identity"],
        "book_clause_identity": BOOK_CLAUSE,
        "comparison_rule": COMPARISON_RULE,
        "path_result_reference": deepcopy(inputs["path"]["reference"]),
        "path_assertion_reference": deepcopy(
            inputs["path"]["assertion_reference"]
        ),
        "comparison_result_reference": deepcopy(
            inputs["comparison"]["reference"]
        ),
        "comparison_binding_event_identity": inputs["comparison"][
            "binding_event_identity"
        ],
        "path_source_occurrence_identity": inputs["path"]
        ["source_occurrence_identity"],
        "comparison_added_occurrence_identity": inputs["comparison"]
        ["added_occurrence_identity"],
        "path_pair_subjects": [list(pair) for pair in inputs["path"]["pair_subjects"]],
        "through_event_occurrence_identity": boundary,
        "scope": {
            "locality_identity": inputs["locality_identity"],
        },
        "unknown": [],
    }


def _applicability_binding_material(
    *,
    comparison_binding: Event,
    inputs: dict[str, Any],
    boundary: str,
    identities: dict[str, str],
) -> dict[str, Any]:
    addressed_act_identity = comparison_binding.material["compare_act_identity"]
    return {
        "subject_reference": {
            "path_input": {
                "subject": deepcopy(inputs["path"]["assertion_reference"]),
                "addressed_act_identity": addressed_act_identity,
            },
            "comparison_input": {
                "subject": deepcopy(inputs["comparison"]["reference"]),
                "addressed_act_identity": addressed_act_identity,
            },
        },
        "exact_act_identity": identities["applicability_act_identity"],
        "applicability_act_identity": identities["applicability_act_identity"],
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
        "result_boundary_identity": identities["applicability_result_identity"],
        "book_clause_identity": "01.Current.E.1",
        "comparison_rule": COMPARISON_RULE,
        "path_result_reference": deepcopy(inputs["path"]["reference"]),
        "path_assertion_reference": deepcopy(inputs["path"]["assertion_reference"]),
        "comparison_result_reference": deepcopy(inputs["comparison"]["reference"]),
        "through_event_occurrence_identity": boundary,
        "scope": {
            "locality_identity": inputs["locality_identity"],
            "addressed_act_identity": addressed_act_identity,
        },
        "unknown": [],
    }


def record_comparison_of_ordered_relation_path_with_recorded_pair_findings_subject_to_act_binding(
    ledger: EventLedger,
    *,
    path_result_event_identity: str,
    comparison_result_event_identity: str,
    current_coordinates: dict[str, Any],
) -> Event:
    inputs = _inputs(
        ledger,
        path_result_event_identity=path_result_event_identity,
        comparison_result_event_identity=comparison_result_event_identity,
        prior_coordinates=current_coordinates,
    )
    boundary = _require_input_current_coordinates(ledger, inputs, current_coordinates)
    identities = _new_identities(ledger)
    if len(set(identities.values())) != len(identities):
        raise ValueError("comparison of ordered relation path with recorded pair findings lifecycle identities collapsed")
    return ledger.append(
        COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_SUBJECT_TO_ACT_BINDING_KIND,
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
        kind=COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_SUBJECT_TO_ACT_BINDING_KIND,
        message="comparison of ordered relation path with recorded pair findings requires one exact binding",
    )
    material = event.material
    identities = {key: material.get(key) for key in _IDENTITY_COORDINATES}
    if (
        any(type(value) is not str or not value for value in identities.values())
        or len(set(identities.values())) != len(identities)
    ):
        raise ValueError("comparison of ordered relation path with recorded pair findings binding identities are not exact")
    path_reference = material.get("path_result_reference")
    comparison_reference = material.get("comparison_result_reference")
    boundary = material.get("through_event_occurrence_identity")
    if prior_coordinates is None:
        from seed_runtime.operator_current_coordinates import (
            _operator_current_coordinate_validation_context,
            read_operator_current_coordinates_through,
        )

        prior_coordinates = _operator_current_coordinate_validation_context(
            ledger,
            locality_identity=event.locality_identity,
        )
        if prior_coordinates is None:
            prior_coordinates = read_operator_current_coordinates_through(
                ledger,
                locality_identity=event.locality_identity,
                through_event_occurrence_identity=boundary,
            )
    inputs = _inputs(
        ledger,
        path_result_event_identity=(
            path_reference.get("recorded_occurrence_identity")
            if type(path_reference) is dict
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
        raise ValueError("comparison of ordered relation path with recorded pair findings binding coordinates are not exact")
    for input_event in (inputs["path"]["event"], inputs["comparison"]["event"]):
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
            raise ValueError("comparison of ordered relation path with recorded pair findings binding does not follow its inputs")
    return event, inputs


def get_comparison_of_ordered_relation_path_with_recorded_pair_findings_subject_to_act_binding(
    ledger: EventLedger, event_identity: str
) -> dict[str, Any]:
    return deepcopy(_read_binding(ledger, event_identity)[0].material)


def _read_applicability_binding(
    ledger: EventLedger,
    event_identity: Any,
    *,
    comparison_binding_reading: tuple[Event, dict[str, Any]] | None = None,
) -> tuple[Event, dict[str, Any], tuple[Event, dict[str, Any]]]:
    event = _event(
        ledger,
        event_identity,
        kind=COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_APPLICABILITY_SUBJECT_TO_ACT_BINDING_KIND,
        message="comparison of ordered relation path with recorded pair findings requires one exact Applicability binding",
    )
    material = event.material
    addressed_act_identity = material.get("addressed_act_identity")
    if comparison_binding_reading is None:
        comparison_bindings = tuple(
            candidate
            for candidate in ledger.iter_locality_kind(
                event.locality_identity,
                COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_SUBJECT_TO_ACT_BINDING_KIND,
            )
            if candidate.material.get("exact_act_identity") == addressed_act_identity
        )
        if len(comparison_bindings) != 1:
            raise ValueError(
                "comparison of ordered relation path with recorded pair findings "
                "Applicability binding addresses no exact Compare binding"
            )
        comparison_binding_reading = _read_binding(
            ledger, comparison_bindings[0].identity
        )
    comparison_binding, inputs = comparison_binding_reading
    identity_keys = (
        "applicability_act_identity",
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
        or material != expected
    ):
        raise ValueError(
            "comparison of ordered relation path with recorded pair findings "
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
            "comparison of ordered relation path with recorded pair findings "
            "Applicability binding does not follow its Compare binding"
        )
    return event, inputs, comparison_binding_reading


def record_comparison_of_ordered_relation_path_with_recorded_pair_findings_applicability_subject_to_act_binding(
    ledger: EventLedger,
    *,
    comparison_binding_event_identity: str,
    current_coordinates: dict[str, Any],
) -> Event:
    comparison_binding, inputs = _read_binding(
        ledger,
        comparison_binding_event_identity,
        prior_coordinates=current_coordinates,
    )
    _require_binding_current_coordinates(comparison_binding, current_coordinates)
    boundary = _identity(
        current_coordinates.get("through_event_occurrence_identity"),
        "comparison of ordered relation path with recorded pair findings "
        "Applicability binding requires one exact through-occurrence boundary",
    )
    identities = {
        "applicability_act_identity": ledger.mint_identity(
            "comparison_of_ordered_relation_path_with_recorded_pair_findings_applicability_act"
        ),
        "applicability_act_occurrence_identity": ledger.mint_identity(
            "comparison_of_ordered_relation_path_with_recorded_pair_findings_applicability_occurrence"
        ),
        "applicability_result_identity": ledger.mint_identity(
            "comparison_of_ordered_relation_path_with_recorded_pair_findings_applicability_result"
        ),
    }
    if len(set(identities.values())) != len(identities):
        raise ValueError(
            "comparison of ordered relation path with recorded pair findings "
            "Applicability lifecycle identities are compressed"
        )
    return ledger.append(
        COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_APPLICABILITY_SUBJECT_TO_ACT_BINDING_KIND,
        _applicability_binding_material(
            comparison_binding=comparison_binding,
            inputs=inputs,
            boundary=boundary,
            identities=identities,
        ),
        locality_identity=comparison_binding.locality_identity,
    )


def get_comparison_of_ordered_relation_path_with_recorded_pair_findings_applicability_subject_to_act_binding(
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
        raise ValueError("comparison of ordered relation path with recorded pair findings requires its exact binding current coordinates")


def _applicability_act_material(binding: Event) -> dict[str, Any]:
    material = binding.material
    return {
        "applicability_act_identity": material["applicability_act_identity"],
        "applicability_act_occurrence_identity": material[
            "applicability_act_occurrence_identity"
        ],
        "result_identity": material["applicability_result_identity"],
        "act": APPLICABILITY_ACT,
        "subject_to_act_binding_reference": _binding_reference(
            binding,
            result_boundary_identity=material["applicability_result_identity"],
        ),
        "applicability_of_input_to_compare": [
            {
                "subject_reference": deepcopy(material["path_assertion_reference"]),
                "role": "ordered relation path input",
                "addressed_act_identity": material["addressed_act_identity"],
            },
            {
                "subject_reference": deepcopy(
                    material["comparison_result_reference"]
                ),
                "role": "recorded pair Compare input",
                "addressed_act_identity": material["addressed_act_identity"],
            },
        ],
        "comparison_rule": COMPARISON_RULE,
        "scope": deepcopy(material["scope"]),
    }


def record_comparison_of_ordered_relation_path_with_recorded_pair_findings_applicability_act_occurrence(
    ledger: EventLedger,
    *,
    applicability_binding_event_identity: str,
    current_coordinates: dict[str, Any],
) -> Event:
    binding, _inputs, _comparison_binding_reading = _read_applicability_binding(
        ledger,
        applicability_binding_event_identity,
    )
    _require_binding_current_coordinates(binding, current_coordinates)
    return ledger.append(
        COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_APPLICABILITY_ACT_OCCURRENCE_EVENT,
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
) -> tuple[Event, Event, dict[str, Any], tuple[Event, dict[str, Any]]]:
    event = _event(
        ledger,
        event_identity,
        kind=COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_APPLICABILITY_ACT_OCCURRENCE_EVENT,
        message="comparison of ordered relation path with recorded pair findings requires exact Applicability Act occurrence",
    )
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
        )
    binding, inputs, comparison_binding_reading = applicability_binding_reading
    if (
        binding_identity != binding.identity
        or event.locality_identity != binding.locality_identity
        or event.material != _applicability_act_material(binding)
    ):
        raise ValueError("comparison of ordered relation path with recorded pair findings Applicability Act occurrence is not exact")
    return event, binding, inputs, comparison_binding_reading


def get_comparison_of_ordered_relation_path_with_recorded_pair_findings_applicability_act_occurrence(
    ledger: EventLedger, event_identity: str
) -> dict[str, Any]:
    return deepcopy(_read_applicability_act(ledger, event_identity)[0].material)


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
                "path_relation_finding_counts": [
                    len(matches) for matches in inputs["path_relation_findings"]
                ],
            },
            "source_provenance": "exact yielded path and comparison results",
            "scope": deepcopy(binding.material["scope"]),
        },
        "exact_act": APPLICABILITY_ACT,
        "addressed_act_identity": binding.material["addressed_act_identity"],
        "addressed_act_occurrence_identity": (
            binding.material["addressed_act_occurrence_identity"]
            if inputs["applicable"]
            else None
        ),
        "applicability_act_identity": binding.material[
            "applicability_act_identity"
        ],
        "applicability_act_occurrence_identity": binding.material[
            "applicability_act_occurrence_identity"
        ],
        "subject_to_act_binding_reference": _binding_reference(
            binding,
            result_boundary_identity=binding.material[
                "applicability_result_identity"
            ],
        ),
        "act_occurrence_event_identity": act.identity,
        "applicability_of_input_to_compare": deepcopy(
            act.material["applicability_of_input_to_compare"]
        ),
        "comparison_rule": COMPARISON_RULE,
        "applicability": applicability,
        "scope": deepcopy(binding.material["scope"]),
        "unknown": list(binding.material["unknown"]),
    }


def _recorded_applicability_result_material(
    result: dict[str, Any], *, yield_relation_identity: str
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
        "applicability_of_input_to_compare": deepcopy(
            result["applicability_of_input_to_compare"]
        ),
        "comparison_rule": result["comparison_rule"],
        "applicability": result["applicability"],
        "scope": deepcopy(result["scope"]),
        "unknown": list(result["unknown"]),
        "yield_relation_identity": yield_relation_identity,
    }


def _refuse_result(ledger: EventLedger, act: Event, result_kind: str) -> None:
    act_occurrence = (
        act.material.get("applicability_act_occurrence_identity")
        or act.material.get("act_occurrence_identity")
    )
    for occurrence in ledger.list_locality(act.locality_identity):
        if occurrence.kind not in {result_kind, RECORDED_YIELD_RELATION_EVENT}:
            continue
        if (
            occurrence.material.get("act_occurrence_event_identity") == act.identity
            or occurrence.material.get("act_occurrence_identity") == act_occurrence
            or occurrence.material.get("applicability_act_occurrence_identity")
            == act_occurrence
        ):
            raise ValueError("one comparison of ordered relation path with recorded pair findings Act cannot Yield twice")


def record_comparison_of_ordered_relation_path_with_recorded_pair_findings_applicability_result(
    ledger: EventLedger, *, act_occurrence_event_identity: str
) -> Event:
    act, binding, inputs, _comparison_binding_reading = _read_applicability_act(
        ledger, act_occurrence_event_identity
    )
    result = _applicability_result_material(act, binding, inputs)
    _refuse_result(
        ledger,
        act,
        COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_APPLICABILITY_RESULT_KIND,
    )
    yield_relation = _record_yield_relation(
        ledger,
        locality_identity=act.locality_identity,
        exact_act=APPLICABILITY_ACT,
        act_occurrence_identity=act.material[
            "applicability_act_occurrence_identity"
        ],
        act_occurrence_event_identity=act.identity,
        result_kind=APPLICABILITY_RESULT_KIND,
        result_identity=result["result_identity"],
        result_content={
            key: value
            for key, value in result.items()
            if key != "act_occurrence_identity"
        },
        occurrence_boundary="comparison_of_ordered_relation_path_with_recorded_pair_findings_applicability",
        responsible_act_occurrence_coordinate=(
            "applicability_act_occurrence_identity"
        ),
    )
    return ledger.append(
        COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_APPLICABILITY_RESULT_KIND,
        _recorded_applicability_result_material(
            result, yield_relation_identity=yield_relation.identity
        ),
        locality_identity=act.locality_identity,
    )


def _read_yielded(
    ledger: EventLedger,
    event_identity: Any,
    *,
    kind: str,
    act: Event,
    expected: dict[str, Any],
    occurrence_boundary: str,
    result_name: str,
    occurrence_coordinate: str = "act_occurrence_identity",
) -> Event:
    event = _event(ledger, event_identity, kind=kind, message="yielded result is absent")
    yield_relation_identity = event.material.get("yield_relation_identity")
    carried = {
        key: value
        for key, value in event.material.items()
        if key != "yield_relation_identity"
    }
    yield_relation = ledger.get(yield_relation_identity) if type(yield_relation_identity) is str else None
    requirements = read_requirements_of_yield_relation(
        ledger,
        recorded_result_event_identity=event.identity,
        yield_relation_event_identity=yield_relation_identity,
        act_occurrence_event_identity=act.identity,
        recorded_result_occurrence_coordinate=occurrence_coordinate,
        responsible_act_occurrence_coordinate=occurrence_coordinate,
    )
    if (
        event.locality_identity != act.locality_identity
        or carried != expected
        or yield_relation is None
        or yield_relation.material.get("occurrence_boundary") != occurrence_boundary
        or yield_relation.material.get("result_kind") != result_name
        or not all(requirements.values())
    ):
        raise ValueError("yielded result carries no exact Yield relation")
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
    act, binding, inputs, comparison_binding_reading = _read_applicability_act(
        ledger,
        act_identity,
        applicability_binding_reading=applicability_binding_reading,
        comparison_binding_reading=comparison_binding_reading,
    )
    event = _read_yielded(
        ledger,
        event_identity,
        kind=COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_APPLICABILITY_RESULT_KIND,
        act=act,
        expected=_applicability_result_material(act, binding, inputs),
        occurrence_boundary="comparison_of_ordered_relation_path_with_recorded_pair_findings_applicability",
        result_name=APPLICABILITY_RESULT_KIND,
        occurrence_coordinate="applicability_act_occurrence_identity",
    )
    return event, act, binding, inputs, comparison_binding_reading


def get_recorded_comparison_of_ordered_relation_path_with_recorded_pair_findings_applicability(
    ledger: EventLedger, event_identity: str
) -> dict[str, Any]:
    return deepcopy(_read_applicability_result(ledger, event_identity)[0].material)


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
        raise ValueError("relation-path Compare requires exact Applicability current coordinates")


def _compare_act_material(binding: Event, applicability: Event) -> dict[str, Any]:
    material = binding.material
    return {
        "compare_act_identity": material["compare_act_identity"],
        "act_occurrence_identity": material["compare_act_occurrence_identity"],
        "result_identity": material["compare_result_identity"],
        "act": COMPARE_ACT,
        "subject_to_act_binding_reference": _binding_reference(
            binding,
            result_boundary_identity=material["compare_result_identity"],
        ),
        "applicability_result_event_identity": applicability.identity,
        "applicability_of_input_to_compare": deepcopy(
            applicability.material["applicability_of_input_to_compare"]
        ),
        "participation_of_input_in_compare": [
            {
                "subject_reference": deepcopy(material["path_assertion_reference"]),
                "role": "ordered relation path",
                "act_occurrence_identity": material[
                    "compare_act_occurrence_identity"
                ],
            },
            {
                "subject_reference": deepcopy(
                    material["comparison_result_reference"]
                ),
                "role": "recorded pair Compare result",
                "act_occurrence_identity": material[
                    "compare_act_occurrence_identity"
                ],
            },
        ],
        "comparison_rule": COMPARISON_RULE,
        "scope": deepcopy(material["scope"]),
    }


def record_comparison_of_ordered_relation_path_with_recorded_pair_findings_act_occurrence(
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
        raise ValueError("relation-path input is not applicable to Compare")
    _require_compare_current_coordinates(binding, applicability, current_coordinates)
    return ledger.append(
        COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_COMPARE_ACT_OCCURRENCE_EVENT,
        _compare_act_material(binding, applicability),
        locality_identity=binding.locality_identity,
    )


def _read_compare_act(
    ledger: EventLedger, event_identity: Any
) -> tuple[Event, Event, Event, dict[str, Any]]:
    event = _event(
        ledger,
        event_identity,
        kind=COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_COMPARE_ACT_OCCURRENCE_EVENT,
        message="comparison of ordered relation path with recorded pair findings requires exact Compare Act occurrence",
    )
    reference = event.material.get("subject_to_act_binding_reference")
    binding_reading = _read_binding(
        ledger,
        reference.get("recorded_occurrence_identity")
        if type(reference) is dict
        else None,
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
        or applicability_inputs["path"]["event"].identity
        != inputs["path"]["event"].identity
        or applicability_inputs["comparison"]["event"].identity
        != inputs["comparison"]["event"].identity
        or not inputs["applicable"]
        or event.locality_identity != binding.locality_identity
        or event.material != _compare_act_material(binding, applicability)
    ):
        raise ValueError("comparison of ordered relation path with recorded pair findings Compare Act occurrence is not exact")
    return event, binding, applicability, inputs


def get_comparison_of_ordered_relation_path_with_recorded_pair_findings_act_occurrence(
    ledger: EventLedger, event_identity: str
) -> dict[str, Any]:
    return deepcopy(_read_compare_act(ledger, event_identity)[0].material)


def _comparison_finding(inputs: dict[str, Any]) -> dict[str, Any]:
    roles = []
    for role, pair, path_reference, findings in zip(
        ("first_path_relation", "second_path_relation"),
        inputs["path"]["pair_subjects"],
        (
            inputs["path"]["assertion"]["assertion_subject"][
                "first_position_assertion_reference"
            ],
            inputs["path"]["assertion"]["assertion_subject"][
                "second_position_assertion_reference"
            ],
        ),
        inputs["path_relation_findings"],
    ):
        roles.append(
            {
                "role": role,
                "path_position_assertion_reference": deepcopy(path_reference),
                "pair_subject": list(pair),
                "comparison_finding_references": deepcopy(list(findings)),
            }
        )
    subject = {
        "ordered_relation_path_assertion_reference": deepcopy(
            inputs["path"]["assertion_reference"]
        ),
        "recorded_pair_comparison_result_reference": deepcopy(
            inputs["comparison"]["reference"]
        ),
    }
    exact = json.dumps(
        {"subject": subject, "roles": roles}, separators=(",", ":")
    ).encode("utf-8")
    return {
        "identity": "ordered-relation-path-pair-finding-comparison:"
        + hashlib.sha256(exact).hexdigest(),
        "subject": subject,
        "relation_findings": roles,
        "source_provenance": (
            "exact yielded ordered path and recorded comparison findings"
        ),
        "scope": {"locality_identity": inputs["locality_identity"]},
        "unknown": [],
    }


def _compare_result_material(
    act: Event, binding: Event, applicability: Event, inputs: dict[str, Any]
) -> dict[str, Any]:
    return {
        "result_identity": binding.material["compare_result_identity"],
        "compare_act_identity": binding.material["compare_act_identity"],
        "act_occurrence_identity": binding.material[
            "compare_act_occurrence_identity"
        ],
        "exact_act": COMPARE_ACT,
        "subject_to_act_binding_reference": _binding_reference(
            binding,
            result_boundary_identity=binding.material[
                "compare_result_identity"
            ],
        ),
        "applicability_result_event_identity": applicability.identity,
        "applicability_of_input_to_compare": deepcopy(
            applicability.material["applicability_of_input_to_compare"]
        ),
        "participation_of_input_in_compare": deepcopy(
            act.material["participation_of_input_in_compare"]
        ),
        "comparison_rule": COMPARISON_RULE,
        "finding": _comparison_finding(inputs),
        "scope": deepcopy(binding.material["scope"]),
        "unknown": list(binding.material["unknown"]),
        "act_occurrence_event_identity": act.identity,
    }


def _recorded_compare_result_material(
    result: dict[str, Any], *, yield_relation_identity: str
) -> dict[str, Any]:
    return {
        "result_identity": result["result_identity"],
        "compare_act_identity": result["compare_act_identity"],
        "act_occurrence_identity": result["act_occurrence_identity"],
        "exact_act": result["exact_act"],
        "subject_to_act_binding_reference": deepcopy(
            result["subject_to_act_binding_reference"]
        ),
        "applicability_result_event_identity": result[
            "applicability_result_event_identity"
        ],
        "applicability_of_input_to_compare": deepcopy(
            result["applicability_of_input_to_compare"]
        ),
        "participation_of_input_in_compare": deepcopy(
            result["participation_of_input_in_compare"]
        ),
        "comparison_rule": result["comparison_rule"],
        "finding": deepcopy(result["finding"]),
        "scope": deepcopy(result["scope"]),
        "unknown": list(result["unknown"]),
        "act_occurrence_event_identity": result[
            "act_occurrence_event_identity"
        ],
        "yield_relation_identity": yield_relation_identity,
    }


def record_comparison_of_ordered_relation_path_with_recorded_pair_findings_result(
    ledger: EventLedger, *, act_occurrence_event_identity: str
) -> Event:
    act, binding, applicability, inputs = _read_compare_act(
        ledger, act_occurrence_event_identity
    )
    result = _compare_result_material(act, binding, applicability, inputs)
    _refuse_result(
        ledger,
        act,
        COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_RESULT_KIND,
    )
    yield_relation = _record_yield_relation(
        ledger,
        locality_identity=act.locality_identity,
        exact_act=COMPARE_ACT,
        act_occurrence_identity=act.material["act_occurrence_identity"],
        act_occurrence_event_identity=act.identity,
        result_kind=COMPARE_RESULT_KIND,
        result_identity=result["result_identity"],
        result_content={
            key: value
            for key, value in result.items()
            if key != "act_occurrence_identity"
        },
        occurrence_boundary="comparison_of_ordered_relation_path_with_recorded_pair_findings_compare",
    )
    return ledger.append(
        COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_RESULT_KIND,
        _recorded_compare_result_material(
            result, yield_relation_identity=yield_relation.identity
        ),
        locality_identity=act.locality_identity,
    )


def get_recorded_comparison_of_ordered_relation_path_with_recorded_pair_findings(
    ledger: EventLedger, event_identity: str
) -> dict[str, Any]:
    candidate = ledger.get(event_identity) if type(event_identity) is str else None
    act_identity = (
        candidate.material.get("act_occurrence_event_identity")
        if candidate is not None and type(candidate.material) is dict
        else None
    )
    act, binding, applicability, inputs = _read_compare_act(ledger, act_identity)
    event = _read_yielded(
        ledger,
        event_identity,
        kind=COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_RESULT_KIND,
        act=act,
        expected=_compare_result_material(act, binding, applicability, inputs),
        occurrence_boundary="comparison_of_ordered_relation_path_with_recorded_pair_findings_compare",
        result_name=COMPARE_RESULT_KIND,
    )
    return deepcopy(event.material)


def _recorded_path_comparison_finding_assertion_coordinates_for_locality_movement(
    ledger: EventLedger,
    *,
    result_event_identity: str,
    assertion_identity: str,
) -> dict[str, Any]:
    reading = get_recorded_comparison_of_ordered_relation_path_with_recorded_pair_findings(
        ledger, result_event_identity
    )
    finding = reading.get("finding")
    if (
        type(finding) is not dict
        or finding.get("identity") != assertion_identity
    ):
        raise ValueError(
            "path-comparison finding Locality movement requires exact source coordinates"
        )
    return deepcopy(finding)


def move_recorded_path_comparison_finding_assertion_to_locality(
    ledger: EventLedger,
    *,
    comparison_result_occurrence_identity: str,
    destination_locality: str,
) -> RecordedAssertionCarriedByLocalityMovement:
    """Carry one exact recorded path-comparison finding through 03.Movement.A."""

    reading = get_recorded_comparison_of_ordered_relation_path_with_recorded_pair_findings(
        ledger, comparison_result_occurrence_identity
    )
    finding = reading.get("finding")
    assertion_identity = finding.get("identity") if type(finding) is dict else None
    if type(assertion_identity) is not str or not assertion_identity:
        raise ValueError(
            "path-comparison finding Assertion movement requires one exact finding"
        )
    from seed_runtime.byte_measurement import (
        _move_assertion_reference_to_locality,
    )

    return _move_assertion_reference_to_locality(
        ledger,
        source_assertion_reference={
            "recorded_occurrence_identity": comparison_result_occurrence_identity,
            "assertion_identity": assertion_identity,
        },
        destination_locality=destination_locality,
    )


class RecordedDistinctionPin(NamedTuple):
    locality_identity: str
    through_event_occurrence_identity: str
    comparison_result_occurrence_identity: str
    ordered_relation_path_assertion_reference: dict[str, Any]
    path_role: str
    path_position_assertion_reference: dict[str, Any]
    pair_subject: bytes
    recorded_finding_reference: dict[str, Any]


def recorded_distinction_pins_from_current_coordinates(
    ledger: EventLedger, *, locality_identity: str
) -> tuple[RecordedDistinctionPin, ...]:
    """Read every exact finding-reference branch from carried results."""

    if not isinstance(ledger, EventLedger):
        raise TypeError("recorded distinction pins require an EventLedger")
    if type(locality_identity) is not str or not locality_identity:
        raise ValueError("recorded distinction pins require one exact Locality")
    from seed_runtime.operator_current_coordinates import (
        read_operator_current_coordinates,
    )

    current_coordinates = read_operator_current_coordinates(
        ledger, locality_identity=locality_identity
    )
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
            == COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_RESULT_KIND
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
        reading = get_recorded_comparison_of_ordered_relation_path_with_recorded_pair_findings(
            ledger, occurrence_identity
        )
        finding = reading.get("finding")
        subject = finding.get("subject") if type(finding) is dict else None
        path_reference = (
            subject.get("ordered_relation_path_assertion_reference")
            if type(subject) is dict
            else None
        )
        roles = finding.get("relation_findings") if type(finding) is dict else None
        comparison_reference = (
            subject.get("recorded_pair_comparison_result_reference")
            if type(subject) is dict
            else None
        )
        if (
            type(path_reference) is not dict
            or type(comparison_reference) is not dict
            or type(comparison_reference.get("recorded_occurrence_identity"))
            is not str
            or type(roles) is not list
        ):
            raise ValueError("recorded distinction pin source result is not exact")
        for role in roles:
            role_identity = role.get("role") if type(role) is dict else None
            position_reference = (
                role.get("path_position_assertion_reference")
                if type(role) is dict
                else None
            )
            pair_subject = role.get("pair_subject") if type(role) is dict else None
            references = (
                role.get("comparison_finding_references")
                if type(role) is dict
                else None
            )
            if (
                role_identity
                not in {"first_path_relation", "second_path_relation"}
                or type(position_reference) is not dict
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
                if (
                    type(reference) is not dict
                    or set(reference)
                    != {
                        "recorded_comparison_occurrence_identity",
                        "finding_category",
                        "finding_position",
                        "subject",
                    }
                    or reference.get("recorded_comparison_occurrence_identity")
                    != comparison_reference["recorded_occurrence_identity"]
                    or reference.get("finding_category")
                    not in {
                        "same_content_findings",
                        "conflicting_findings",
                        "findings_of_earlier_result",
                        "findings_of_later_result",
                        "unknown_findings",
                    }
                    or type(reference.get("finding_position")) is not int
                    or reference["finding_position"] < 0
                    or type(reference.get("subject")) is not dict
                    or reference["subject"].get("content")
                    != pair_subject
                ):
                    raise ValueError("recorded distinction pin reference is not exact")
                pins.append(
                    RecordedDistinctionPin(
                        locality_identity,
                        boundary,
                        occurrence_identity,
                        deepcopy(path_reference),
                        role_identity,
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
