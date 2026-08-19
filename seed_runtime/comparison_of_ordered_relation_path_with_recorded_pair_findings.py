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
from seed_runtime.evidence_of_yield_relation import (
    RECORDED_EVIDENCE_OF_YIELD_RELATION_KIND,
    _record_evidence_of_yield_relation,
    read_requirements_of_yield_relation,
)
from seed_runtime.identities import new_identity
from seed_runtime.measurement_of_shared_position_of_byte_pair_occurrences import (
    SHARED_POSITION_MEASUREMENT_RESULT_KIND,
    get_recorded_shared_position_measurement,
)


COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_RESPONSIBILITY_ASSIGNMENT_KIND = (
    "operator.comparison_of_ordered_relation_path_with_recorded_pair_findings.responsibility_assignment_recorded"
)
COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_APPLICABILITY_ACT_EVIDENCE_KIND = (
    "operator.comparison_of_ordered_relation_path_with_recorded_pair_findings.applicability_act_evidenced"
)
COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_APPLICABILITY_RESULT_KIND = (
    "operator.comparison_of_ordered_relation_path_with_recorded_pair_findings.applicability_recorded"
)
COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_COMPARE_ACT_EVIDENCE_KIND = (
    "operator.comparison_of_ordered_relation_path_with_recorded_pair_findings.compare_act_evidenced"
)
COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_RESULT_KIND = "operator.comparison_of_ordered_relation_path_with_recorded_pair_findings.recorded"

BOOK_CLAUSE = "04.Compare.B"
RESPONSIBILITY = (
    "determine Applicability and Compare one exact ordered relation path with "
    "recorded pair findings of its exact source occurrence"
)
APPLICABILITY_ACT = (
    "determine Applicability of one ordered relation path and one recorded pair "
    "comparison result to one Compare"
)
COMPARE_ACT = (
    "Compare each relation of one ordered path with complete recorded findings "
    "of the same exact pair subject"
)
COMPARISON_RULE = (
    "the path source is the exact added comparison occurrence and each path pair "
    "subject carries complete recorded comparison findings"
)
APPLICABILITY_RESULT_KIND = (
    "Applicability result of ordered relation path and recorded pair findings"
)
COMPARE_RESULT_KIND = (
    "comparison result of ordered relation path and recorded pair findings"
)

EVENT_KIND_RESPONSIBILITIES = {
    COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_RESPONSIBILITY_ASSIGNMENT_KIND: "04.Compare.B",
    COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_APPLICABILITY_ACT_EVIDENCE_KIND: "02.Acts.A",
    COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_APPLICABILITY_RESULT_KIND: "01.Standing.E.1",
    COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_COMPARE_ACT_EVIDENCE_KIND: "02.Acts.A",
    COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_RESULT_KIND: "04.Compare.B",
}

_FINDING_CATEGORIES = (
    "same_content_findings",
    "conflicting_findings",
    "findings_of_earlier_result",
    "findings_of_later_result",
    "unknown_findings",
)


class OrderedPathPairFindingCompareAssignmentSubject(NamedTuple):
    path_result_event_identity: str
    comparison_result_event_identity: str


class RecordedOrderedPathPairFindingCompareAssignments(NamedTuple):
    locality_standing: dict[str, Any]
    assignment_occurrences: tuple[Event, ...]


class RecordedOrderedPathPairFindingCompareApplicability(NamedTuple):
    locality_standing: dict[str, Any]
    applicability_result_occurrences: tuple[Event, ...]


class RecordedOrderedPathPairFindingCompareActEvidence(NamedTuple):
    locality_standing: dict[str, Any]
    compare_act_evidence_occurrences: tuple[Event, ...]


class RecordedOrderedPathPairFindingCompareResults(NamedTuple):
    locality_standing: dict[str, Any]
    compare_result_occurrences: tuple[Event, ...]


def _identity(value: Any, message: str) -> str:
    if type(value) is not str or not value:
        raise ValueError(message)
    return value


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
        "responsible_act_evidence_identity": event.material[
            "responsible_act_evidence_identity"
        ],
        "evidence_of_yield_relation_identity": event.material[
            "evidence_of_yield_relation_identity"
        ],
    }


def _path_input(ledger: EventLedger, event_identity: Any) -> dict[str, Any]:
    event = _event(
        ledger,
        event_identity,
        kind=SHARED_POSITION_MEASUREMENT_RESULT_KIND,
        message="comparison of ordered relation path with recorded pair findings requires one exact path Measurement result",
    )
    material = get_recorded_shared_position_measurement(ledger, event.identity)
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
        != {
            "recorded_occurrence_identity": first.get(
                "recorded_occurrence_identity"
            ),
            "assertion_identity": first.get("assertion_identity"),
        }
        or assertion.get("assertion_subject", {}).get(
            "second_position_assertion_reference"
        )
        != {
            "recorded_occurrence_identity": second.get(
                "recorded_occurrence_identity"
            ),
            "assertion_identity": second.get("assertion_identity"),
        }
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
    source = (
        content.get("source_ingest_occurrence_identity")
        if type(content) is dict
        else None
    )
    return {
        "event": event,
        "reference": _result_reference(event),
        "assertion": deepcopy(assertion),
        "assertion_reference": {
            "recorded_occurrence_identity": event.identity,
            "assertion_identity": assertion["dimensions"]["identity"],
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
            pair = subject.get("representation") if type(subject) is dict else None
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
    material, assignment_reading = (
        _recorded_pair_measurement_comparison_reading(ledger, event.identity)
    )
    assignment = assignment_reading[0]
    assignment_reference = material.get("responsibility_assignment_reference")
    assignment_identity = (
        assignment_reference.get("recorded_occurrence_identity")
        if type(assignment_reference) is dict
        else None
    )
    if (
        assignment.identity != assignment_identity
        or assignment.material.get("comparison_result_identity")
        != material.get("result_identity")
    ):
        raise ValueError("comparison of ordered relation path with recorded pair findings comparison assignment is crossed")
    return {
        "event": event,
        "reference": _result_reference(event),
        "assignment_event_identity": assignment.identity,
        "added_occurrence_identity": assignment.material[
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
        if tuple(reference["subject"]["representation"]) == pair
    )


def _inputs(
    ledger: EventLedger,
    *,
    path_result_event_identity: Any,
    comparison_result_event_identity: Any,
) -> dict[str, Any]:
    path = _path_input(ledger, path_result_event_identity)
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


def unassigned_ordered_path_pair_finding_compare_subjects_in_current_standing(
    ledger: EventLedger, *, locality_identity: str
) -> tuple[OrderedPathPairFindingCompareAssignmentSubject, ...]:
    """Read every unassigned exact 04.Compare.B subject in current Standing.

    The read records no assignment, Applicability, Participation, Compare, or
    result occurrence.
    """

    if not isinstance(ledger, EventLedger):
        raise TypeError("ordered-path Compare subjects require one EventLedger")
    if type(locality_identity) is not str or not locality_identity:
        raise ValueError("ordered-path Compare subjects require one exact Locality")

    from seed_runtime.operator_locality_standing import (
        read_operator_locality_standing,
    )

    standing = read_operator_locality_standing(
        ledger, locality_identity=locality_identity
    )
    measurement_occurrences = standing.get("measurement_occurrences")
    comparison_occurrences = standing.get("comparison_result_occurrences")
    if (
        type(measurement_occurrences) is not dict
        or type(comparison_occurrences) is not dict
    ):
        raise ValueError(
            "ordered-path Compare subjects require exact current Standing"
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
        COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_RESPONSIBILITY_ASSIGNMENT_KIND,
    ):
        assignment, inputs = _read_assignment(ledger, occurrence.identity)
        assigned.add(
            (
                inputs["path"]["event"].identity,
                inputs["comparison"]["event"].identity,
            )
        )
        if assignment.locality_identity != locality_identity:
            raise ValueError(
                "ordered-path Compare assignment belongs to another Locality"
            )

    subjects = []
    for path_identity in path_identities:
        for comparison_identity in comparison_identities:
            inputs = _inputs(
                ledger,
                path_result_event_identity=path_identity,
                comparison_result_event_identity=comparison_identity,
            )
            _require_input_standing(ledger, inputs, standing)
            if (path_identity, comparison_identity) not in assigned:
                subjects.append(
                    OrderedPathPairFindingCompareAssignmentSubject(
                        path_result_event_identity=path_identity,
                        comparison_result_event_identity=comparison_identity,
                    )
                )
    return tuple(subjects)


def record_ordered_path_pair_finding_compare_assignments_from_current_standing(
    ledger: EventLedger, *, locality_identity: str
) -> RecordedOrderedPathPairFindingCompareAssignments:
    """Record each exact Book-assigned 04.Compare.B subject serially."""

    from seed_runtime.operator_locality_standing import (
        read_operator_locality_standing,
    )

    assignments: list[Event] = []
    while True:
        subjects = (
            unassigned_ordered_path_pair_finding_compare_subjects_in_current_standing(
                ledger, locality_identity=locality_identity
            )
        )
        if not subjects:
            return RecordedOrderedPathPairFindingCompareAssignments(
                locality_standing=read_operator_locality_standing(
                    ledger, locality_identity=locality_identity
                ),
                assignment_occurrences=tuple(assignments),
            )
        subject = subjects[0]
        standing = read_operator_locality_standing(
            ledger, locality_identity=locality_identity
        )
        assignments.append(
            record_comparison_of_ordered_relation_path_with_recorded_pair_findings_responsibility_assignment(
                ledger,
                path_result_event_identity=subject.path_result_event_identity,
                comparison_result_event_identity=(
                    subject.comparison_result_event_identity
                ),
                locality_standing=standing,
            )
        )


def record_ordered_path_pair_finding_compare_applicability_from_current_standing(
    ledger: EventLedger, *, locality_identity: str
) -> RecordedOrderedPathPairFindingCompareApplicability:
    """Record Applicability once for each exact current 04.Compare.B assignment."""

    from seed_runtime.operator_locality_standing import (
        read_operator_locality_standing,
    )

    standing = read_operator_locality_standing(
        ledger, locality_identity=locality_identity
    )
    standing_assignments = standing.get("responsibility_assignment_occurrences")
    if type(standing_assignments) is not dict:
        raise ValueError(
            "ordered-path Compare Applicability requires exact current Standing"
        )
    assignments = tuple(
        event
        for identity in standing_assignments
        if (
            (event := ledger.get(identity)) is not None
            and event.kind
            == COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_RESPONSIBILITY_ASSIGNMENT_KIND
        )
    )
    for assignment in assignments:
        _read_assignment(ledger, assignment.identity)

    acts_by_assignment: dict[str, Event] = {}
    for occurrence in ledger.iter_locality_kind(
        locality_identity,
        COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_APPLICABILITY_ACT_EVIDENCE_KIND,
    ):
        act, assignment, _inputs_reading = _read_applicability_act(
            ledger, occurrence.identity
        )
        if assignment.identity in acts_by_assignment:
            raise ValueError(
                "ordered-path Compare assignment carries repeated Applicability Evidence"
            )
        acts_by_assignment[assignment.identity] = act

    results_by_assignment: dict[str, Event] = {}
    for occurrence in ledger.iter_locality_kind(
        locality_identity,
        COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_APPLICABILITY_RESULT_KIND,
    ):
        result, _act, assignment, _inputs_reading = _read_applicability_result(
            ledger, occurrence.identity
        )
        if assignment.identity in results_by_assignment:
            raise ValueError(
                "ordered-path Compare assignment carries repeated Applicability result"
            )
        results_by_assignment[assignment.identity] = result

    recorded: list[Event] = []
    for assignment in assignments:
        if assignment.identity in results_by_assignment:
            continue
        act = acts_by_assignment.get(assignment.identity)
        if act is None:
            standing = read_operator_locality_standing(
                ledger, locality_identity=locality_identity
            )
            act = record_comparison_of_ordered_relation_path_with_recorded_pair_findings_applicability_act_evidence(
                ledger,
                responsibility_assignment_event_identity=assignment.identity,
                locality_standing=standing,
            )
            acts_by_assignment[assignment.identity] = act
        result = record_comparison_of_ordered_relation_path_with_recorded_pair_findings_applicability_result(
            ledger,
            responsible_act_evidence_event_identity=act.identity,
        )
        results_by_assignment[assignment.identity] = result
        recorded.append(result)

    return RecordedOrderedPathPairFindingCompareApplicability(
        locality_standing=read_operator_locality_standing(
            ledger, locality_identity=locality_identity
        ),
        applicability_result_occurrences=tuple(recorded),
    )


def record_applicable_ordered_path_pair_finding_compare_act_evidence_from_current_standing(
    ledger: EventLedger, *, locality_identity: str
) -> RecordedOrderedPathPairFindingCompareActEvidence:
    """Record Compare Act Evidence and Participation for each applicable result."""

    from seed_runtime.operator_locality_standing import (
        read_operator_locality_standing,
    )

    standing = read_operator_locality_standing(
        ledger, locality_identity=locality_identity
    )
    standing_results = standing.get("applicability_result_occurrences")
    if type(standing_results) is not dict:
        raise ValueError(
            "ordered-path Compare Participation requires exact current Standing"
        )
    applicability_readings = []
    for identity in standing_results:
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
        COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_COMPARE_ACT_EVIDENCE_KIND,
    ):
        act, _assignment, applicability, _inputs_reading = _read_compare_act(
            ledger, occurrence.identity
        )
        if applicability.identity in acts_by_applicability:
            raise ValueError(
                "ordered-path Compare Applicability carries repeated Compare Act Evidence"
            )
        acts_by_applicability[applicability.identity] = act

    recorded: list[Event] = []
    for applicability, _act, assignment, _inputs_reading in applicability_readings:
        if applicability.material["applicability"] != "applicable":
            if applicability.identity in acts_by_applicability:
                raise ValueError(
                    "inapplicable ordered-path Compare input carries Participation"
                )
            continue
        if applicability.identity in acts_by_applicability:
            continue
        standing = read_operator_locality_standing(
            ledger, locality_identity=locality_identity
        )
        act = record_comparison_of_ordered_relation_path_with_recorded_pair_findings_act_evidence(
            ledger,
            responsibility_assignment_event_identity=assignment.identity,
            applicability_result_event_identity=applicability.identity,
            locality_standing=standing,
        )
        acts_by_applicability[applicability.identity] = act
        recorded.append(act)

    return RecordedOrderedPathPairFindingCompareActEvidence(
        locality_standing=read_operator_locality_standing(
            ledger, locality_identity=locality_identity
        ),
        compare_act_evidence_occurrences=tuple(recorded),
    )


def record_ordered_path_pair_finding_compare_results_from_current_standing(
    ledger: EventLedger, *, locality_identity: str
) -> RecordedOrderedPathPairFindingCompareResults:
    """Record one Yield and result for each exact current Compare Act Evidence."""

    from seed_runtime.operator_locality_standing import (
        read_operator_locality_standing,
    )

    standing = read_operator_locality_standing(
        ledger, locality_identity=locality_identity
    )
    acts = []
    for occurrence in ledger.iter_locality_kind(
        locality_identity,
        COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_COMPARE_ACT_EVIDENCE_KIND,
    ):
        act, _assignment, _applicability, _inputs_reading = _read_compare_act(
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
        act_identity = occurrence.material.get("responsible_act_evidence_identity")
        if type(act_identity) is not str or not act_identity:
            raise ValueError(
                "ordered-path Compare result carries no exact Act Evidence"
            )
        if act_identity in results_by_act:
            raise ValueError(
                "ordered-path Compare Act Evidence carries repeated results"
            )
        results_by_act[act_identity] = occurrence

    recorded: list[Event] = []
    for act in acts:
        if act.identity in results_by_act:
            continue
        result = record_comparison_of_ordered_relation_path_with_recorded_pair_findings_result(
            ledger,
            responsible_act_evidence_event_identity=act.identity,
        )
        results_by_act[act.identity] = result
        recorded.append(result)
        standing = read_operator_locality_standing(
            ledger, locality_identity=locality_identity
        )

    return RecordedOrderedPathPairFindingCompareResults(
        locality_standing=standing,
        compare_result_occurrences=tuple(recorded),
    )


def _authority() -> dict[str, str]:
    return {
        "source": "this Book",
        "book_clause_identity": BOOK_CLAUSE,
        "standing": "bounded",
        "act": COMPARE_ACT,
        "negative_authority": (
            "establish no source relation, represented relation, or recurrence"
        ),
    }


def _require_input_standing(
    ledger: EventLedger, inputs: dict[str, Any], standing: Any
) -> str:
    if (
        type(standing) is not dict
        or standing.get("locality_identity") != inputs["locality_identity"]
        or type(standing.get("measurement_occurrences")) is not dict
        or inputs["path"]["event"].identity
        not in standing["measurement_occurrences"]
        or type(standing.get("comparison_result_occurrences")) is not dict
        or inputs["comparison"]["event"].identity
        not in standing["comparison_result_occurrences"]
    ):
        raise ValueError(
            "comparison of ordered relation path with recorded pair findings requires "
            "each exact result in current Standing"
        )
    boundary = _identity(
        standing.get("through_event_occurrence_identity"),
        "comparison of ordered relation path with recorded pair findings requires one exact Standing boundary",
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
                "comparison of ordered relation path with recorded pair findings Standing boundary does not carry its inputs"
            )
    return boundary


def _assignment_reference(event: Event) -> dict[str, str]:
    return {
        "recorded_occurrence_identity": event.identity,
        "assignment_identity": event.material["assignment_identity"],
        "assignment_subject_identity": event.material[
            "assignment_subject_identity"
        ],
    }


_IDENTITY_COORDINATES = (
    "assignment_identity",
    "assignment_subject_identity",
    "applicability_act_identity",
    "applicability_act_occurrence_identity",
    "applicability_result_identity",
    "compare_act_identity",
    "compare_act_occurrence_identity",
    "compare_result_identity",
    "path_input_relation_identity",
    "comparison_input_relation_identity",
    "path_participation_relation_identity",
    "comparison_participation_relation_identity",
)


def _new_identities() -> dict[str, str]:
    return {
        "assignment_identity": new_identity("comparison_of_ordered_relation_path_with_recorded_pair_findings_assignment"),
        "assignment_subject_identity": new_identity(
            "comparison_of_ordered_relation_path_with_recorded_pair_findings_assignment_subject"
        ),
        "applicability_act_identity": new_identity(
            "comparison_of_ordered_relation_path_with_recorded_pair_findings_applicability_act"
        ),
        "applicability_act_occurrence_identity": new_identity(
            "comparison_of_ordered_relation_path_with_recorded_pair_findings_applicability_occurrence"
        ),
        "applicability_result_identity": new_identity(
            "comparison_of_ordered_relation_path_with_recorded_pair_findings_applicability_result"
        ),
        "compare_act_identity": new_identity("comparison_of_ordered_relation_path_with_recorded_pair_findings_compare_act"),
        "compare_act_occurrence_identity": new_identity(
            "comparison_of_ordered_relation_path_with_recorded_pair_findings_compare_occurrence"
        ),
        "compare_result_identity": new_identity("comparison_of_ordered_relation_path_with_recorded_pair_findings_result"),
        "path_input_relation_identity": new_identity(
            "comparison_of_ordered_relation_path_with_recorded_pair_findings_path_input_relation"
        ),
        "comparison_input_relation_identity": new_identity(
            "comparison_of_ordered_relation_path_with_recorded_pair_findings_comparison_input_relation"
        ),
        "path_participation_relation_identity": new_identity(
            "comparison_of_ordered_relation_path_with_recorded_pair_findings_path_participation"
        ),
        "comparison_participation_relation_identity": new_identity(
            "comparison_of_ordered_relation_path_with_recorded_pair_findings_comparison_participation"
        ),
    }


def _assignment_material(
    inputs: dict[str, Any], boundary: str, identities: dict[str, str]
) -> dict[str, Any]:
    return {
        "assignment_identity": identities["assignment_identity"],
        "assignment_subject_identity": identities["assignment_subject_identity"],
        "applicability_act_identity": identities["applicability_act_identity"],
        "applicability_act_occurrence_identity": identities[
            "applicability_act_occurrence_identity"
        ],
        "applicability_result_identity": identities[
            "applicability_result_identity"
        ],
        "compare_act_identity": identities["compare_act_identity"],
        "compare_act_occurrence_identity": identities[
            "compare_act_occurrence_identity"
        ],
        "compare_result_identity": identities["compare_result_identity"],
        "path_input_relation_identity": identities[
            "path_input_relation_identity"
        ],
        "comparison_input_relation_identity": identities[
            "comparison_input_relation_identity"
        ],
        "path_participation_relation_identity": identities[
            "path_participation_relation_identity"
        ],
        "comparison_participation_relation_identity": identities[
            "comparison_participation_relation_identity"
        ],
        "book_clause_identity": BOOK_CLAUSE,
        "responsibility": RESPONSIBILITY,
        "responsible_boundary": "this Seed",
        "comparison_rule": COMPARISON_RULE,
        "path_result_reference": deepcopy(inputs["path"]["reference"]),
        "path_assertion_reference": deepcopy(
            inputs["path"]["assertion_reference"]
        ),
        "comparison_result_reference": deepcopy(
            inputs["comparison"]["reference"]
        ),
        "comparison_assignment_event_identity": inputs["comparison"][
            "assignment_event_identity"
        ],
        "path_source_occurrence_identity": inputs["path"]
        ["source_occurrence_identity"],
        "comparison_added_occurrence_identity": inputs["comparison"]
        ["added_occurrence_identity"],
        "path_pair_subjects": [list(pair) for pair in inputs["path"]["pair_subjects"]],
        "standing_boundary_identity": boundary,
        "scope": {
            "locality_identity": inputs["locality_identity"],
            "standing_boundary_identity": boundary,
        },
        "authority": _authority(),
        "limits": [
            "one exact pair subject under each input establishes no source relation",
            "exact result carries recorded comparison findings",
            "the result establishes no later relation or recurrence",
        ],
        "unknown": [
            "what the relation of path and comparison findings represents: Unknown"
        ],
    }


def record_comparison_of_ordered_relation_path_with_recorded_pair_findings_responsibility_assignment(
    ledger: EventLedger,
    *,
    path_result_event_identity: str,
    comparison_result_event_identity: str,
    locality_standing: dict[str, Any],
) -> Event:
    inputs = _inputs(
        ledger,
        path_result_event_identity=path_result_event_identity,
        comparison_result_event_identity=comparison_result_event_identity,
    )
    boundary = _require_input_standing(ledger, inputs, locality_standing)
    identities = _new_identities()
    if len(set(identities.values())) != len(identities):
        raise ValueError("comparison of ordered relation path with recorded pair findings lifecycle identities collapsed")
    return ledger.append(
        COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_RESPONSIBILITY_ASSIGNMENT_KIND,
        _assignment_material(inputs, boundary, identities),
        locality_identity=inputs["locality_identity"],
    )


def _read_assignment(
    ledger: EventLedger, event_identity: Any
) -> tuple[Event, dict[str, Any]]:
    event = _event(
        ledger,
        event_identity,
        kind=COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_RESPONSIBILITY_ASSIGNMENT_KIND,
        message="comparison of ordered relation path with recorded pair findings requires one exact assignment",
    )
    material = event.material
    identities = {key: material.get(key) for key in _IDENTITY_COORDINATES}
    if (
        any(type(value) is not str or not value for value in identities.values())
        or len(set(identities.values())) != len(identities)
    ):
        raise ValueError("comparison of ordered relation path with recorded pair findings assignment identities are not exact")
    path_reference = material.get("path_result_reference")
    comparison_reference = material.get("comparison_result_reference")
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
    )
    boundary = material.get("standing_boundary_identity")
    boundary_event = ledger.get(boundary) if type(boundary) is str else None
    expected = _assignment_material(inputs, boundary, identities)
    if (
        boundary_event is None
        or boundary_event.locality_identity != event.locality_identity
        or ledger.integrity_of(boundary_event.identity) == CORRUPTED
        or event.locality_identity != inputs["locality_identity"]
        or material != expected
    ):
        raise ValueError("comparison of ordered relation path with recorded pair findings assignment coordinates are not exact")
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
            raise ValueError("comparison of ordered relation path with recorded pair findings assignment does not follow its inputs")
    return event, inputs


def get_comparison_of_ordered_relation_path_with_recorded_pair_findings_responsibility_assignment(
    ledger: EventLedger, event_identity: str
) -> dict[str, Any]:
    return deepcopy(_read_assignment(ledger, event_identity)[0].material)


def _require_assignment_standing(assignment: Event, standing: Any) -> None:
    assignments = (
        standing.get("responsibility_assignment_occurrences")
        if type(standing) is dict
        else None
    )
    if (
        type(standing) is not dict
        or standing.get("locality_identity") != assignment.locality_identity
        or type(assignments) is not dict
        or assignments.get(assignment.identity, object()) is not None
    ):
        raise ValueError("comparison of ordered relation path with recorded pair findings requires its exact assignment Standing")


def _applicability_act_material(assignment: Event) -> dict[str, Any]:
    material = assignment.material
    return {
        "applicability_act_identity": material["applicability_act_identity"],
        "applicability_act_occurrence_identity": material[
            "applicability_act_occurrence_identity"
        ],
        "result_identity": material["applicability_result_identity"],
        "act": APPLICABILITY_ACT,
        "responsibility": RESPONSIBILITY,
        "responsible_boundary": "this Seed",
        "responsibility_assignment_reference": _assignment_reference(assignment),
        "applicability_of_input_to_compare": [
            {
                "relation_identity": material["path_input_relation_identity"],
                "subject_reference": deepcopy(material["path_assertion_reference"]),
                "role": "ordered relation path input",
                "addressed_act_identity": material["compare_act_identity"],
            },
            {
                "relation_identity": material[
                    "comparison_input_relation_identity"
                ],
                "subject_reference": deepcopy(
                    material["comparison_result_reference"]
                ),
                "role": "recorded pair comparison input",
                "addressed_act_identity": material["compare_act_identity"],
            },
        ],
        "comparison_rule": COMPARISON_RULE,
        "scope": deepcopy(material["scope"]),
        "authority": deepcopy(material["authority"]),
        "evidence_scope": "Evidence for this exact Applicability occurrence",
    }


def record_comparison_of_ordered_relation_path_with_recorded_pair_findings_applicability_act_evidence(
    ledger: EventLedger,
    *,
    responsibility_assignment_event_identity: str,
    locality_standing: dict[str, Any],
) -> Event:
    assignment, _inputs_reading = _read_assignment(
        ledger, responsibility_assignment_event_identity
    )
    _require_assignment_standing(assignment, locality_standing)
    return ledger.append(
        COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_APPLICABILITY_ACT_EVIDENCE_KIND,
        _applicability_act_material(assignment),
        locality_identity=assignment.locality_identity,
    )


def _read_applicability_act(
    ledger: EventLedger,
    event_identity: Any,
    *,
    assignment_reading: tuple[Event, dict[str, Any]] | None = None,
) -> tuple[Event, Event, dict[str, Any]]:
    event = _event(
        ledger,
        event_identity,
        kind=COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_APPLICABILITY_ACT_EVIDENCE_KIND,
        message="comparison of ordered relation path with recorded pair findings requires exact Applicability Evidence",
    )
    reference = event.material.get("responsibility_assignment_reference")
    assignment_identity = (
        reference.get("recorded_occurrence_identity")
        if type(reference) is dict
        else None
    )
    if assignment_reading is None:
        assignment_reading = _read_assignment(ledger, assignment_identity)
    assignment, inputs = assignment_reading
    if (
        assignment_identity != assignment.identity
        or event.locality_identity != assignment.locality_identity
        or event.material != _applicability_act_material(assignment)
    ):
        raise ValueError("comparison of ordered relation path with recorded pair findings Applicability Evidence is not exact")
    return event, assignment, inputs


def get_comparison_of_ordered_relation_path_with_recorded_pair_findings_applicability_act_evidence(
    ledger: EventLedger, event_identity: str
) -> dict[str, Any]:
    return deepcopy(_read_applicability_act(ledger, event_identity)[0].material)


def _applicability_result_material(
    act: Event, assignment: Event, inputs: dict[str, Any]
) -> dict[str, Any]:
    standing = "applicable" if inputs["applicable"] else "inapplicable"
    return {
        "result_identity": assignment.material["applicability_result_identity"],
        "dimensions": {
            "identity": assignment.material["applicability_result_identity"],
            "content": {
                "same_source_occurrence": inputs["same_source"],
                "path_relation_finding_counts": [
                    len(matches) for matches in inputs["path_relation_findings"]
                ],
            },
            "standing": standing,
            "source_provenance": "exact yielded path and comparison results",
            "responsibility": RESPONSIBILITY,
            "responsible_boundary": "this Seed",
            "authority": deepcopy(assignment.material["authority"]),
            "scope": deepcopy(assignment.material["scope"]),
        },
        "exact_act": APPLICABILITY_ACT,
        "addressed_act_identity": assignment.material["compare_act_identity"],
        "addressed_act_occurrence_identity": (
            assignment.material["compare_act_occurrence_identity"]
            if inputs["applicable"]
            else None
        ),
        "applicability_act_identity": assignment.material[
            "applicability_act_identity"
        ],
        "applicability_act_occurrence_identity": assignment.material[
            "applicability_act_occurrence_identity"
        ],
        "responsibility": RESPONSIBILITY,
        "responsible_boundary": "this Seed",
        "responsibility_assignment_reference": _assignment_reference(assignment),
        "responsible_act_evidence_identity": act.identity,
        "applicability_of_input_to_compare": deepcopy(
            act.material["applicability_of_input_to_compare"]
        ),
        "comparison_rule": COMPARISON_RULE,
        "applicability": standing,
        "scope": deepcopy(assignment.material["scope"]),
        "authority": deepcopy(assignment.material["authority"]),
        "limits": list(assignment.material["limits"]),
        "unknown": list(assignment.material["unknown"]),
    }


def _recorded_applicability_result_material(
    result: dict[str, Any], *, evidence_identity: str
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
        "responsibility": result["responsibility"],
        "responsible_boundary": result["responsible_boundary"],
        "responsibility_assignment_reference": deepcopy(
            result["responsibility_assignment_reference"]
        ),
        "responsible_act_evidence_identity": result[
            "responsible_act_evidence_identity"
        ],
        "applicability_of_input_to_compare": deepcopy(
            result["applicability_of_input_to_compare"]
        ),
        "comparison_rule": result["comparison_rule"],
        "applicability": result["applicability"],
        "scope": deepcopy(result["scope"]),
        "authority": deepcopy(result["authority"]),
        "limits": list(result["limits"]),
        "unknown": list(result["unknown"]),
        "evidence_of_yield_relation_identity": evidence_identity,
    }


def _refuse_result(ledger: EventLedger, act: Event, result_kind: str) -> None:
    act_occurrence = (
        act.material.get("applicability_act_occurrence_identity")
        or act.material.get("act_occurrence_identity")
    )
    for occurrence in ledger.list_locality(act.locality_identity):
        if occurrence.kind not in {result_kind, RECORDED_EVIDENCE_OF_YIELD_RELATION_KIND}:
            continue
        if (
            occurrence.material.get("responsible_act_evidence_identity") == act.identity
            or occurrence.material.get("act_occurrence_identity") == act_occurrence
            or occurrence.material.get("applicability_act_occurrence_identity")
            == act_occurrence
        ):
            raise ValueError("one comparison of ordered relation path with recorded pair findings Act cannot Yield twice")


def record_comparison_of_ordered_relation_path_with_recorded_pair_findings_applicability_result(
    ledger: EventLedger, *, responsible_act_evidence_event_identity: str
) -> Event:
    act, assignment, inputs = _read_applicability_act(
        ledger, responsible_act_evidence_event_identity
    )
    result = _applicability_result_material(act, assignment, inputs)
    _refuse_result(
        ledger,
        act,
        COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_APPLICABILITY_RESULT_KIND,
    )
    evidence = _record_evidence_of_yield_relation(
        ledger,
        locality_identity=act.locality_identity,
        exact_act=APPLICABILITY_ACT,
        act_occurrence_identity=act.material[
            "applicability_act_occurrence_identity"
        ],
        responsible_act_evidence_identity=act.identity,
        result_kind=APPLICABILITY_RESULT_KIND,
        result_identity=result["result_identity"],
        result_content={
            key: value
            for key, value in result.items()
            if key != "responsible_act_evidence_identity"
        },
        responsibility=RESPONSIBILITY,
        occurrence_boundary="comparison_of_ordered_relation_path_with_recorded_pair_findings_applicability",
        responsible_boundary="this Seed",
        responsible_act_occurrence_coordinate=(
            "applicability_act_occurrence_identity"
        ),
    )
    return ledger.append(
        COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_APPLICABILITY_RESULT_KIND,
        _recorded_applicability_result_material(
            result, evidence_identity=evidence.identity
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
    evidence_identity = event.material.get("evidence_of_yield_relation_identity")
    carried = {
        key: value
        for key, value in event.material.items()
        if key != "evidence_of_yield_relation_identity"
    }
    evidence = ledger.get(evidence_identity) if type(evidence_identity) is str else None
    requirements = read_requirements_of_yield_relation(
        ledger,
        recorded_result_event_identity=event.identity,
        evidence_of_yield_relation_event_identity=evidence_identity,
        responsible_act_evidence_event_identity=act.identity,
        recorded_result_occurrence_coordinate=occurrence_coordinate,
        responsible_act_occurrence_coordinate=occurrence_coordinate,
    )
    if (
        event.locality_identity != act.locality_identity
        or carried != expected
        or evidence is None
        or evidence.material.get("occurrence_boundary") != occurrence_boundary
        or evidence.material.get("result_kind") != result_name
        or not all(requirements.values())
    ):
        raise ValueError("yielded result carries no exact Evidence of Yield relation")
    return event


def _read_applicability_result(
    ledger: EventLedger,
    event_identity: Any,
    *,
    assignment_reading: tuple[Event, dict[str, Any]] | None = None,
) -> tuple[Event, Event, Event, dict[str, Any]]:
    candidate = ledger.get(event_identity) if type(event_identity) is str else None
    act_identity = (
        candidate.material.get("responsible_act_evidence_identity")
        if candidate is not None and type(candidate.material) is dict
        else None
    )
    act, assignment, inputs = _read_applicability_act(
        ledger, act_identity, assignment_reading=assignment_reading
    )
    event = _read_yielded(
        ledger,
        event_identity,
        kind=COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_APPLICABILITY_RESULT_KIND,
        act=act,
        expected=_applicability_result_material(act, assignment, inputs),
        occurrence_boundary="comparison_of_ordered_relation_path_with_recorded_pair_findings_applicability",
        result_name=APPLICABILITY_RESULT_KIND,
        occurrence_coordinate="applicability_act_occurrence_identity",
    )
    return event, act, assignment, inputs


def get_recorded_comparison_of_ordered_relation_path_with_recorded_pair_findings_applicability(
    ledger: EventLedger, event_identity: str
) -> dict[str, Any]:
    return deepcopy(_read_applicability_result(ledger, event_identity)[0].material)


def _require_compare_standing(
    assignment: Event, applicability: Event, standing: Any
) -> None:
    assignments = (
        standing.get("responsibility_assignment_occurrences")
        if type(standing) is dict
        else None
    )
    applicable = (
        standing.get("applicability_result_occurrences")
        if type(standing) is dict
        else None
    )
    if (
        type(standing) is not dict
        or standing.get("locality_identity") != assignment.locality_identity
        or type(assignments) is not dict
        or assignments.get(assignment.identity, object()) is not None
        or type(applicable) is not dict
        or applicable.get(applicability.identity, object()) is not None
    ):
        raise ValueError("relation-path Compare requires exact Applicability Standing")


def _compare_act_material(assignment: Event, applicability: Event) -> dict[str, Any]:
    material = assignment.material
    return {
        "compare_act_identity": material["compare_act_identity"],
        "act_occurrence_identity": material["compare_act_occurrence_identity"],
        "result_identity": material["compare_result_identity"],
        "act": COMPARE_ACT,
        "responsibility": RESPONSIBILITY,
        "responsible_boundary": "this Seed",
        "responsibility_assignment_reference": _assignment_reference(assignment),
        "applicability_result_event_identity": applicability.identity,
        "applicability_of_input_to_compare": deepcopy(
            applicability.material["applicability_of_input_to_compare"]
        ),
        "participation_of_input_in_compare": [
            {
                "relation_identity": material[
                    "path_participation_relation_identity"
                ],
                "subject_reference": deepcopy(material["path_assertion_reference"]),
                "role": "ordered relation path",
                "act_occurrence_identity": material[
                    "compare_act_occurrence_identity"
                ],
            },
            {
                "relation_identity": material[
                    "comparison_participation_relation_identity"
                ],
                "subject_reference": deepcopy(
                    material["comparison_result_reference"]
                ),
                "role": "recorded pair comparison result",
                "act_occurrence_identity": material[
                    "compare_act_occurrence_identity"
                ],
            },
        ],
        "comparison_rule": COMPARISON_RULE,
        "scope": deepcopy(material["scope"]),
        "authority": deepcopy(material["authority"]),
        "evidence_scope": "Evidence for this exact Compare occurrence",
    }


def record_comparison_of_ordered_relation_path_with_recorded_pair_findings_act_evidence(
    ledger: EventLedger,
    *,
    responsibility_assignment_event_identity: str,
    applicability_result_event_identity: str,
    locality_standing: dict[str, Any],
) -> Event:
    assignment_reading = _read_assignment(
        ledger, responsibility_assignment_event_identity
    )
    assignment, _inputs_reading = assignment_reading
    applicability, _act, applicability_assignment, inputs = (
        _read_applicability_result(
            ledger,
            applicability_result_event_identity,
            assignment_reading=assignment_reading,
        )
    )
    if (
        applicability_assignment.identity != assignment.identity
        or not inputs["applicable"]
        or applicability.material["applicability"] != "applicable"
    ):
        raise ValueError("relation-path input is not applicable to Compare")
    _require_compare_standing(assignment, applicability, locality_standing)
    return ledger.append(
        COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_COMPARE_ACT_EVIDENCE_KIND,
        _compare_act_material(assignment, applicability),
        locality_identity=assignment.locality_identity,
    )


def _read_compare_act(
    ledger: EventLedger, event_identity: Any
) -> tuple[Event, Event, Event, dict[str, Any]]:
    event = _event(
        ledger,
        event_identity,
        kind=COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_COMPARE_ACT_EVIDENCE_KIND,
        message="comparison of ordered relation path with recorded pair findings requires exact Compare Evidence",
    )
    reference = event.material.get("responsibility_assignment_reference")
    assignment_reading = _read_assignment(
        ledger,
        reference.get("recorded_occurrence_identity")
        if type(reference) is dict
        else None,
    )
    assignment, inputs = assignment_reading
    applicability, _act, applicability_assignment, applicability_inputs = (
        _read_applicability_result(
            ledger,
            event.material.get("applicability_result_event_identity"),
            assignment_reading=assignment_reading,
        )
    )
    if (
        applicability_assignment.identity != assignment.identity
        or applicability_inputs["path"]["event"].identity
        != inputs["path"]["event"].identity
        or applicability_inputs["comparison"]["event"].identity
        != inputs["comparison"]["event"].identity
        or not inputs["applicable"]
        or event.locality_identity != assignment.locality_identity
        or event.material != _compare_act_material(assignment, applicability)
    ):
        raise ValueError("comparison of ordered relation path with recorded pair findings Compare Evidence is not exact")
    return event, assignment, applicability, inputs


def get_comparison_of_ordered_relation_path_with_recorded_pair_findings_act_evidence(
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
    canonical = json.dumps(
        {"subject": subject, "roles": roles}, separators=(",", ":")
    ).encode("utf-8")
    return {
        "identity": "ordered-relation-path-pair-finding-comparison:"
        + hashlib.sha256(canonical).hexdigest(),
        "subject": subject,
        "relation_findings": roles,
        "source_provenance": (
            "exact yielded ordered path and recorded comparison findings"
        ),
        "scope": {"locality_identity": inputs["locality_identity"]},
        "authority": _authority(),
        "limits": [
            "recorded Standing carries comparison findings",
            "the relation establishes no source relation or recurrence",
        ],
        "unknown": [
            "what the relation of the ordered path and recorded comparison findings represents: Unknown"
        ],
    }


def _compare_result_material(
    act: Event, assignment: Event, applicability: Event, inputs: dict[str, Any]
) -> dict[str, Any]:
    return {
        "result_identity": assignment.material["compare_result_identity"],
        "compare_act_identity": assignment.material["compare_act_identity"],
        "act_occurrence_identity": assignment.material[
            "compare_act_occurrence_identity"
        ],
        "exact_act": COMPARE_ACT,
        "responsibility": RESPONSIBILITY,
        "responsible_boundary": "this Seed",
        "responsibility_assignment_reference": _assignment_reference(assignment),
        "applicability_result_event_identity": applicability.identity,
        "applicability_of_input_to_compare": deepcopy(
            applicability.material["applicability_of_input_to_compare"]
        ),
        "participation_of_input_in_compare": deepcopy(
            act.material["participation_of_input_in_compare"]
        ),
        "comparison_rule": COMPARISON_RULE,
        "finding": _comparison_finding(inputs),
        "scope": deepcopy(assignment.material["scope"]),
        "authority": deepcopy(assignment.material["authority"]),
        "limits": list(assignment.material["limits"]),
        "unknown": list(assignment.material["unknown"]),
        "responsible_act_evidence_identity": act.identity,
    }


def _recorded_compare_result_material(
    result: dict[str, Any], *, evidence_identity: str
) -> dict[str, Any]:
    return {
        "result_identity": result["result_identity"],
        "compare_act_identity": result["compare_act_identity"],
        "act_occurrence_identity": result["act_occurrence_identity"],
        "exact_act": result["exact_act"],
        "responsibility": result["responsibility"],
        "responsible_boundary": result["responsible_boundary"],
        "responsibility_assignment_reference": deepcopy(
            result["responsibility_assignment_reference"]
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
        "authority": deepcopy(result["authority"]),
        "limits": list(result["limits"]),
        "unknown": list(result["unknown"]),
        "responsible_act_evidence_identity": result[
            "responsible_act_evidence_identity"
        ],
        "evidence_of_yield_relation_identity": evidence_identity,
    }


def record_comparison_of_ordered_relation_path_with_recorded_pair_findings_result(
    ledger: EventLedger, *, responsible_act_evidence_event_identity: str
) -> Event:
    act, assignment, applicability, inputs = _read_compare_act(
        ledger, responsible_act_evidence_event_identity
    )
    result = _compare_result_material(act, assignment, applicability, inputs)
    _refuse_result(
        ledger,
        act,
        COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_RESULT_KIND,
    )
    evidence = _record_evidence_of_yield_relation(
        ledger,
        locality_identity=act.locality_identity,
        exact_act=COMPARE_ACT,
        act_occurrence_identity=act.material["act_occurrence_identity"],
        responsible_act_evidence_identity=act.identity,
        result_kind=COMPARE_RESULT_KIND,
        result_identity=result["result_identity"],
        result_content={
            key: value
            for key, value in result.items()
            if key != "responsible_act_evidence_identity"
        },
        responsibility=RESPONSIBILITY,
        occurrence_boundary="comparison_of_ordered_relation_path_with_recorded_pair_findings_compare",
        responsible_boundary="this Seed",
    )
    return ledger.append(
        COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_RESULT_KIND,
        _recorded_compare_result_material(
            result, evidence_identity=evidence.identity
        ),
        locality_identity=act.locality_identity,
    )


def get_recorded_comparison_of_ordered_relation_path_with_recorded_pair_findings(
    ledger: EventLedger, event_identity: str
) -> dict[str, Any]:
    candidate = ledger.get(event_identity) if type(event_identity) is str else None
    act_identity = (
        candidate.material.get("responsible_act_evidence_identity")
        if candidate is not None and type(candidate.material) is dict
        else None
    )
    act, assignment, applicability, inputs = _read_compare_act(ledger, act_identity)
    event = _read_yielded(
        ledger,
        event_identity,
        kind=COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_RESULT_KIND,
        act=act,
        expected=_compare_result_material(act, assignment, applicability, inputs),
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
    standing_boundary_identity: str
    comparison_result_occurrence_identity: str
    ordered_relation_path_assertion_reference: dict[str, str]
    path_role: str
    path_position_assertion_reference: dict[str, str]
    pair_subject: bytes
    recorded_finding_reference: dict[str, Any]


def recorded_distinction_pins_from_current_standing(
    ledger: EventLedger, *, locality_identity: str
) -> tuple[RecordedDistinctionPin, ...]:
    """Read every exact finding-reference branch from carried results."""

    if not isinstance(ledger, EventLedger):
        raise TypeError("recorded distinction pins require an EventLedger")
    if type(locality_identity) is not str or not locality_identity:
        raise ValueError("recorded distinction pins require one exact Locality")
    from seed_runtime.operator_locality_standing import (
        read_operator_locality_standing,
    )

    standing = read_operator_locality_standing(
        ledger, locality_identity=locality_identity
    )
    boundary = standing.get("through_event_occurrence_identity")
    comparisons = standing.get("comparison_result_occurrences")
    if type(comparisons) is not dict:
        raise ValueError("recorded distinction pins require exact current Standing")
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
        raise ValueError("recorded distinction pins require exact current Standing")
    pins = []
    for event in sources:
        occurrence_identity = event.identity
        coordinates = comparisons[occurrence_identity]
        if coordinates is not None:
            raise ValueError("recorded distinction pin source Standing is not exact")
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
                    or reference["subject"].get("representation")
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
        raise ValueError("recorded distinction pins require one unchanged current Standing pin")
    return tuple(pins)
