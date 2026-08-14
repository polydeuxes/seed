"""Count productions of exact recurrence-subject coordinate Assertions.

Canonical Assertion identity supplies the grouping rule.  The Measurement
forms no pairs and produces only an exact production set, its count, and a
recurrence result where that count exceeds one.
"""

from __future__ import annotations


from dataclasses import dataclass
import hashlib
import json
from typing import Any, Iterable, Iterator

from seed_runtime.event import Event
from seed_runtime.events import CORRUPTED, EventLedger, EventLedgerBoundary
from seed_runtime.ids import new_id
from seed_runtime.recurrence_subject_measurement import (
    RECURRENCE_SUBJECT_COORDINATES_RECORDED_KIND,
    RecordedRecurrenceSubjectCoordinateAssertion,
    RecurrenceSubjectMeasurementError,
    assertions_of_recorded_recurrence_subject_coordinates,
    iter_recorded_recurrence_subject_coordinate_assertions,
)


COORDINATE_ASSERTION_COUNT_RECORDED_KIND = (
    "operator.measurement.coordinate_assertion_count_recorded"
)
MEASURED_ASSERTION_RESPONSIBILITY = (
    "preserve the fidelity of this measured Assertion's Standing to its "
    "carried coordinates"
)
MEASUREMENT_AUTHORITY = (
    "literal Measurement Evidence only; establishes no relation, similarity, "
    "profile, represented relation, or Standing movement"
)
MEASUREMENT_UNKNOWNS = (
    "why this exact coordinate Assertion has this production count remains Unknown",
)
PRODUCTION_SET_FORBIDDEN_INFERENCES = (
    "an exact production set is not recurrence, relation, similarity, profile, "
    "represented relation, or Standing strength",
)
COUNT_FORBIDDEN_INFERENCES = (
    "count greater than one does not itself produce recurrence, relation, "
    "similarity, profile, represented relation, or Standing movement",
)
RECURRENCE_FORBIDDEN_INFERENCES = (
    "recurrence is repetition, not relation, similarity, profile, represented relation, "
    "independent corroboration, or Standing strength",
)


class CoordinateAssertionMeasurementError(ValueError):
    """The bounded coordinate-Assertion Measurement could not be instantiated."""


@dataclass(frozen=True)
class MeasuredCoordinateAssertionCount:
    source_assertion_id: str
    source_assertion_subject: dict[str, Any]
    exact_coordinate_value: Any
    assertion_scope: dict[str, Any]
    production_refs: tuple[dict[str, str], ...]
    workspace_id: str
    source_session_ids: tuple[str, ...]
    completeness_boundary: EventLedgerBoundary

    @property
    def count(self) -> int:
        return len(self.production_refs)


@dataclass(frozen=True)
class RecordedCoordinateAssertionCount:
    assertion_id: str
    producing_event_id: str
    result: str
    payload: dict[str, Any]

    @property
    def reference(self) -> dict[str, str]:
        return {
            "producing_event_id": self.producing_event_id,
            "assertion_id": self.assertion_id,
        }


def _canonical(value: Any) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def _assertion_identity(
    *, result: str, subject: dict[str, Any], scope: dict[str, Any], content: Any
) -> str:
    represented = {
        "result": result,
        "subject": subject,
        "scope": scope,
        "content": content,
    }
    return "coordinate-assertion-measurement:" + hashlib.sha256(
        _canonical(represented).encode("utf-8")
    ).hexdigest()


def _rehydrate_coordinate_assertion(
    ledger: EventLedger, reference: dict[str, str]
) -> RecordedRecurrenceSubjectCoordinateAssertion:
    event = ledger.get(reference["producing_event_id"])
    if event is None:
        raise CoordinateAssertionMeasurementError(
            "a measured coordinate Assertion is no longer recoverable"
        )
    if ledger.integrity_of(event.id) == CORRUPTED:
        raise CoordinateAssertionMeasurementError(
            "a measured coordinate Assertion became detectably corrupted"
        )
    for assertion in assertions_of_recorded_recurrence_subject_coordinates(event):
        if assertion.assertion_id == reference["assertion_id"]:
            return assertion
    raise CoordinateAssertionMeasurementError(
        "a measured coordinate Assertion reference changed during Measurement"
    )


def measure_coordinate_assertion_counts(
    ledger: EventLedger,
    *,
    workspace_id: str,
    source_session_ids: Iterable[str],
) -> Iterator[MeasuredCoordinateAssertionCount]:
    """Count every canonical coordinate Assertion in one bounded population."""

    sessions = tuple(dict.fromkeys(source_session_ids))
    if not sessions or any(not isinstance(value, str) or not value for value in sessions):
        raise CoordinateAssertionMeasurementError(
            "coordinate-Assertion Measurement requires exact declared source sessions"
        )
    boundary = ledger.capture_boundary()
    missing = [
        session_id
        for session_id in sessions
        if not ledger.has_session(workspace_id, session_id, through=boundary)
    ]
    if missing:
        raise CoordinateAssertionMeasurementError(
            "declared source sessions are absent through the Measurement boundary: "
            + ", ".join(missing)
        )
    grouped: dict[str, list[dict[str, str]]] = {}
    try:
        for assertion in iter_recorded_recurrence_subject_coordinate_assertions(
            ledger,
            workspace_id=workspace_id,
            session_ids=sessions,
            through=boundary,
        ):
            grouped.setdefault(assertion.assertion_id, []).append(assertion.reference)
    except RecurrenceSubjectMeasurementError as exc:
        raise CoordinateAssertionMeasurementError(str(exc)) from exc
    if not grouped:
        raise CoordinateAssertionMeasurementError(
            "no recovered recurrence-subject coordinate Assertions to measure"
        )
    def stream() -> Iterator[MeasuredCoordinateAssertionCount]:
        for source_assertion_id, refs in grouped.items():
            representative = _rehydrate_coordinate_assertion(ledger, refs[0])
            payload = representative.payload
            yield MeasuredCoordinateAssertionCount(
                source_assertion_id=source_assertion_id,
                source_assertion_subject=payload["assertion_subject"],
                exact_coordinate_value=payload["dimensions"]["content"]["exact_value"],
                assertion_scope=payload["assertion_scope"],
                production_refs=tuple(refs),
                workspace_id=workspace_id,
                source_session_ids=sessions,
                completeness_boundary=boundary,
            )

    return stream()


def _finding_assertions(
    finding: MeasuredCoordinateAssertionCount,
) -> tuple[dict[str, Any], ...]:
    subject = {
        "measured_assertion_id": finding.source_assertion_id,
        "coordinate_subject": finding.source_assertion_subject,
        "exact_coordinate_value": finding.exact_coordinate_value,
    }
    scope = dict(finding.assertion_scope)
    set_content = {"production_refs": list(finding.production_refs)}
    set_id = _assertion_identity(
        result="exact_production_set",
        subject=subject,
        scope=scope,
        content=set_content,
    )

    def assertion_shell(
        *, result: str, content: dict[str, Any], identity: str, provenance: str,
        support_basis: dict[str, Any], forbidden: tuple[str, ...]
    ) -> dict[str, Any]:
        return {
            "dimensions": {
                "identity": identity,
                "content": content,
                "standing": "measured",
                "source_provenance": provenance,
                "responsibility": MEASURED_ASSERTION_RESPONSIBILITY,
                "authority": MEASUREMENT_AUTHORITY,
            },
            "subject_kind": "assertion",
            "responsibility_owner": "this recorded assertion",
            "result": result,
            "assertion_subject": subject,
            "assertion_scope": scope,
            "support_basis": support_basis,
            "unknowns": list(MEASUREMENT_UNKNOWNS),
            "forbidden_inferences": list(forbidden),
        }

    production_set = assertion_shell(
        result="exact_production_set",
        content=set_content,
        identity=set_id,
        provenance="recorded recurrence-subject coordinate Assertion productions",
        support_basis={"assertion_refs": list(finding.production_refs)},
        forbidden=PRODUCTION_SET_FORBIDDEN_INFERENCES,
    )
    production_set["completeness_boundary"] = {
        "commitment": finding.completeness_boundary.commitment
    }
    production_set["completeness_scope"] = {
        "workspace_id": finding.workspace_id,
        "source_session_ids": list(finding.source_session_ids),
        "occurrence_kind": RECURRENCE_SUBJECT_COORDINATES_RECORDED_KIND,
    }
    count_content = {"production_count": finding.count}
    count_id = _assertion_identity(
        result="count", subject=subject, scope=scope, content=count_content
    )
    count = assertion_shell(
        result="count",
        content=count_content,
        identity=count_id,
        provenance="the exact production-set Assertion carried here",
        support_basis={"local_assertion_ids": [set_id]},
        forbidden=COUNT_FORBIDDEN_INFERENCES,
    )
    assertions = [production_set, count]
    if finding.count > 1:
        recurrence_content = {"recurrence_established": True}
        recurrence_id = _assertion_identity(
            result="recurrence",
            subject=subject,
            scope=scope,
            content=recurrence_content,
        )
        assertions.append(
            assertion_shell(
                result="recurrence",
                content=recurrence_content,
                identity=recurrence_id,
                provenance="the exact count Assertion carried here",
                support_basis={"local_assertion_ids": [count_id]},
                forbidden=RECURRENCE_FORBIDDEN_INFERENCES,
            )
        )
    return tuple(assertions)


def _measurement_event(
    *, workspace_id: str, session_id: str, finding: MeasuredCoordinateAssertionCount
) -> Event:
    assertions = _finding_assertions(finding)
    return Event(
        id=new_id("evt"),
        kind=COORDINATE_ASSERTION_COUNT_RECORDED_KIND,
        workspace_id=workspace_id,
        session_id=session_id,
        payload={
            "dimensions": {
                "identity": "coordinate-assertion-count-measurement-occurrence",
                "content": f"{len(assertions)} distinct measured Assertions recorded",
                "standing": "recorded",
                "source_provenance": (
                    "recorded recurrence-subject coordinate Assertion productions"
                ),
                "authority": MEASUREMENT_AUTHORITY,
            },
            "producing_act": "declared Measurement",
            "measurement_subject": (
                "recorded recurrence-subject coordinate Assertions"
            ),
            "assertions": list(assertions),
        },
    )


def record_coordinate_assertion_count_layer(
    ledger: EventLedger,
    *,
    workspace_id: str,
    source_session_ids: Iterable[str],
    recording_session_id: str,
) -> int:
    """Record every canonical coordinate-Assertion count; batch storage only."""

    if not isinstance(recording_session_id, str) or not recording_session_id:
        raise CoordinateAssertionMeasurementError(
            "coordinate-Assertion recording requires an exact session"
        )
    pending = []
    recorded = 0
    for finding in measure_coordinate_assertion_counts(
        ledger,
        workspace_id=workspace_id,
        source_session_ids=source_session_ids,
    ):
        pending.append(
            _measurement_event(
                workspace_id=workspace_id,
                session_id=recording_session_id,
                finding=finding,
            )
        )
        if len(pending) == 128:
            ledger.append_many(pending)
            recorded += len(pending)
            pending.clear()
    if pending:
        ledger.append_many(pending)
        recorded += len(pending)
    return recorded


def assertions_of_recorded_coordinate_assertion_count(
    event: Event,
) -> tuple[RecordedCoordinateAssertionCount, ...]:
    """Recover the exact set/count/conditional-recurrence output contract."""

    stated = event.payload.get("assertions")
    dimensions = event.payload.get("dimensions")
    if (
        event.kind != COORDINATE_ASSERTION_COUNT_RECORDED_KIND
        or not isinstance(stated, list)
        or len(stated) not in (2, 3)
        or dimensions
        != {
            "identity": "coordinate-assertion-count-measurement-occurrence",
            "content": f"{len(stated)} distinct measured Assertions recorded",
            "standing": "recorded",
            "source_provenance": (
                "recorded recurrence-subject coordinate Assertion productions"
            ),
            "authority": MEASUREMENT_AUTHORITY,
        }
        or event.payload.get("producing_act") != "declared Measurement"
        or event.payload.get("measurement_subject")
        != "recorded recurrence-subject coordinate Assertions"
    ):
        raise CoordinateAssertionMeasurementError(
            f"{event.id} does not carry the established Measurement occurrence"
        )
    by_result = {
        item.get("result"): item for item in stated if isinstance(item, dict)
    }
    if set(by_result) not in (
        {"exact_production_set", "count"},
        {"exact_production_set", "count", "recurrence"},
    ):
        raise CoordinateAssertionMeasurementError(
            f"{event.id} does not carry the exact result set"
        )
    production_set = by_result["exact_production_set"]
    count = by_result["count"]
    recurrence = by_result.get("recurrence")
    set_dimensions = production_set.get("dimensions")
    count_dimensions = count.get("dimensions")
    subject = production_set.get("assertion_subject")
    scope = production_set.get("assertion_scope")
    set_content = set_dimensions.get("content") if isinstance(set_dimensions, dict) else None
    count_content = count_dimensions.get("content") if isinstance(count_dimensions, dict) else None
    refs = set_content.get("production_refs") if isinstance(set_content, dict) else None
    boundary = production_set.get("completeness_boundary")
    completeness_scope = production_set.get("completeness_scope")
    if (
        not isinstance(subject, dict)
        or set(subject)
        != {"measured_assertion_id", "coordinate_subject", "exact_coordinate_value"}
        or not isinstance(subject.get("measured_assertion_id"), str)
        or not isinstance(scope, dict)
        or set(scope) != {"workspace_id", "source_session_ids"}
        or scope.get("workspace_id") != event.workspace_id
        or not isinstance(refs, list)
        or not refs
        or any(
            not isinstance(ref, dict)
            or set(ref) != {"producing_event_id", "assertion_id"}
            or ref["assertion_id"] != subject["measured_assertion_id"]
            for ref in refs
        )
        or production_set.get("support_basis") != {"assertion_refs": refs}
        or not isinstance(boundary, dict)
        or set(boundary) != {"commitment"}
        or not isinstance(boundary["commitment"], str)
        or not isinstance(completeness_scope, dict)
        or set(completeness_scope)
        != {"workspace_id", "source_session_ids", "occurrence_kind"}
        or completeness_scope.get("workspace_id") != event.workspace_id
        or not isinstance(completeness_scope.get("source_session_ids"), list)
        or not completeness_scope["source_session_ids"]
        or completeness_scope.get("occurrence_kind")
        != RECURRENCE_SUBJECT_COORDINATES_RECORDED_KIND
        or count.get("assertion_subject") != subject
        or count.get("assertion_scope") != scope
        or count_content != {"production_count": len(refs)}
        or (recurrence is None) != (len(refs) == 1)
    ):
        raise CoordinateAssertionMeasurementError(
            f"{event.id} carries incoherent Measurement coordinates"
        )

    def require_shell(item, dimensions, provenance, support, forbidden):
        if (
            item.get("subject_kind") != "assertion"
            or item.get("responsibility_owner") != "this recorded assertion"
            or not isinstance(dimensions, dict)
            or dimensions.get("standing") != "measured"
            or dimensions.get("source_provenance") != provenance
            or dimensions.get("responsibility") != MEASURED_ASSERTION_RESPONSIBILITY
            or dimensions.get("authority") != MEASUREMENT_AUTHORITY
            or item.get("support_basis") != support
            or item.get("unknowns") != list(MEASUREMENT_UNKNOWNS)
            or item.get("forbidden_inferences") != list(forbidden)
        ):
            raise CoordinateAssertionMeasurementError(
                f"{event.id} carries an incoherent measured Assertion shell"
            )

    require_shell(
        production_set,
        set_dimensions,
        "recorded recurrence-subject coordinate Assertion productions",
        {"assertion_refs": refs},
        PRODUCTION_SET_FORBIDDEN_INFERENCES,
    )
    set_id = _assertion_identity(
        result="exact_production_set", subject=subject, scope=scope, content=set_content
    )
    count_id = _assertion_identity(
        result="count", subject=subject, scope=scope, content=count_content
    )
    require_shell(
        count,
        count_dimensions,
        "the exact production-set Assertion carried here",
        {"local_assertion_ids": [set_id]},
        COUNT_FORBIDDEN_INFERENCES,
    )
    if (
        set_dimensions.get("identity") != set_id
        or count_dimensions.get("identity") != count_id
        or "completeness_boundary" in count
        or "completeness_scope" in count
    ):
        raise CoordinateAssertionMeasurementError(
            f"{event.id} carries a noncanonical Assertion or dependency"
        )
    ordered = [production_set, count]
    if recurrence is not None:
        recurrence_dimensions = recurrence.get("dimensions")
        recurrence_content = (
            recurrence_dimensions.get("content")
            if isinstance(recurrence_dimensions, dict)
            else None
        )
        recurrence_id = _assertion_identity(
            result="recurrence",
            subject=subject,
            scope=scope,
            content={"recurrence_established": True},
        )
        require_shell(
            recurrence,
            recurrence_dimensions,
            "the exact count Assertion carried here",
            {"local_assertion_ids": [count_id]},
            RECURRENCE_FORBIDDEN_INFERENCES,
        )
        if (
            recurrence.get("assertion_subject") != subject
            or recurrence.get("assertion_scope") != scope
            or recurrence_content != {"recurrence_established": True}
            or recurrence_dimensions.get("identity") != recurrence_id
            or "completeness_boundary" in recurrence
            or "completeness_scope" in recurrence
        ):
            raise CoordinateAssertionMeasurementError(
                f"{event.id} carries a noncanonical recurrence Assertion"
            )
        ordered.append(recurrence)
    return tuple(
        RecordedCoordinateAssertionCount(
            assertion_id=item["dimensions"]["identity"],
            producing_event_id=event.id,
            result=item["result"],
            payload=item,
        )
        for item in ordered
    )


def get_recorded_coordinate_assertion_count(
    ledger: EventLedger,
    *,
    producing_event_id: str,
    assertion_id: str,
) -> RecordedCoordinateAssertionCount | None:
    """Resolve one result after proving its complete coordinate population."""

    event = ledger.get(producing_event_id)
    if event is None:
        return None
    if ledger.integrity_of(event.id) == CORRUPTED:
        raise CoordinateAssertionMeasurementError(
            "a corrupted Measurement occurrence cannot expose result Assertions"
        )
    recovered = assertions_of_recorded_coordinate_assertion_count(event)
    production_set = next(item for item in recovered if item.result == "exact_production_set")
    payload = production_set.payload
    completeness_scope = payload["completeness_scope"]
    boundary = EventLedgerBoundary(payload["completeness_boundary"]["commitment"])
    expected_refs = []
    measured_subject = payload["assertion_subject"]
    try:
        for source in iter_recorded_recurrence_subject_coordinate_assertions(
            ledger,
            workspace_id=event.workspace_id,
            session_ids=completeness_scope["source_session_ids"],
            through=boundary,
        ):
            if source.assertion_id == measured_subject["measured_assertion_id"]:
                if (
                    source.payload["assertion_subject"]
                    != measured_subject["coordinate_subject"]
                    or source.payload["dimensions"]["content"]["exact_value"]
                    != measured_subject["exact_coordinate_value"]
                    or source.payload["assertion_scope"] != payload["assertion_scope"]
                ):
                    raise CoordinateAssertionMeasurementError(
                        "measured coordinate identity does not match its source Assertion"
                    )
                expected_refs.append(source.reference)
    except RecurrenceSubjectMeasurementError as exc:
        raise CoordinateAssertionMeasurementError(str(exc)) from exc
    if expected_refs != payload["support_basis"]["assertion_refs"]:
        raise CoordinateAssertionMeasurementError(
            "the carried production set does not equal the complete bounded read"
        )
    for item in recovered:
        if item.assertion_id == assertion_id:
            return item
    return None
