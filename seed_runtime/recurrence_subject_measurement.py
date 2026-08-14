"""Measure the immediate subject coordinates of recurrence Assertions.

The input recurrence Assertion contract carries exactly three immediate
coordinates.  This Measurement preserves each complete value opaquely; it does
not traverse nested dictionaries or lists, form cross-subject pairs, or infer
relation, similarity, profile, or represented relation.
"""

from __future__ import annotations


from dataclasses import dataclass
import hashlib
import json
from typing import Any, Iterable, Iterator

from seed_runtime.comparison_result_measurement import (
    ComparisonResultMeasurementError,
    RecordedComparisonResultCountAssertion,
    get_recorded_comparison_result_count_assertion,
    iter_recorded_comparison_result_count_assertions,
)
from seed_runtime.event import Event
from seed_runtime.events import CORRUPTED, EventLedger, EventLedgerBoundary
from seed_runtime.ids import new_id


RECURRENCE_SUBJECT_COORDINATES = (
    "compared_subject",
    "coordinate",
    "exact_comparison_result",
)
RECURRENCE_SUBJECT_COORDINATES_RECORDED_KIND = (
    "operator.measurement.recurrence_subject_coordinates_recorded"
)
MEASURED_ASSERTION_RESPONSIBILITY = (
    "preserve the fidelity of this measured Assertion's Standing to its "
    "carried coordinates"
)
MEASUREMENT_AUTHORITY = (
    "literal Measurement Evidence only; establishes no nested coordinate, "
    "relation, similarity, profile, represented relation, or Standing movement"
)
MEASUREMENT_UNKNOWNS = (
    "why the recurrence subject carries this exact coordinate value remains Unknown",
)
FORBIDDEN_INFERENCES = (
    "an immediate coordinate value is not a nested representation, relation, "
    "similarity, profile, represented relation, or Standing strength",
)


class RecurrenceSubjectMeasurementError(ValueError):
    """The bounded recurrence-subject Measurement could not be instantiated."""


@dataclass(frozen=True)
class MeasuredRecurrenceSubjectCoordinates:
    """The complete immediate coordinate results of one recurrence production."""

    source: RecordedComparisonResultCountAssertion
    coordinates: tuple[tuple[str, Any], ...]


@dataclass(frozen=True)
class RecordedRecurrenceSubjectCoordinateAssertion:
    assertion_id: str
    producing_event_id: str
    coordinate: str
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
    *, coordinate: str, value: Any, scope: dict[str, Any]
) -> str:
    identified = {
        "result": "recurrence_subject_coordinate_value",
        "subject": {
            "source_assertion_result": "recurrence",
            "coordinate": coordinate,
        },
        "scope": scope,
        "content": {"exact_value": value},
    }
    return "recurrence-subject-coordinate:" + hashlib.sha256(
        _canonical(identified).encode("utf-8")
    ).hexdigest()


def measure_recurrence_subject_coordinates(
    ledger: EventLedger,
    *,
    workspace_id: str,
    source_session_ids: Iterable[str],
) -> Iterator[MeasuredRecurrenceSubjectCoordinates]:
    """Measure exactly one reconstructed coordinate layer and nothing beneath it."""

    sessions = tuple(dict.fromkeys(source_session_ids))
    if not sessions or any(not isinstance(value, str) or not value for value in sessions):
        raise RecurrenceSubjectMeasurementError(
            "recurrence-subject Measurement requires exact declared source sessions"
        )
    boundary = ledger.capture_boundary()
    missing = [
        session_id
        for session_id in sessions
        if not ledger.has_session(workspace_id, session_id, through=boundary)
    ]
    if missing:
        raise RecurrenceSubjectMeasurementError(
            "declared source sessions are absent through the Measurement boundary: "
            + ", ".join(missing)
        )
    try:
        reconstructed = iter_recorded_comparison_result_count_assertions(
            ledger,
            workspace_id=workspace_id,
            session_ids=sessions,
            through=boundary,
        )
        first = next(
            assertion for assertion in reconstructed if assertion.result == "recurrence"
        )
    except StopIteration as exc:
        raise RecurrenceSubjectMeasurementError(
            "no reconstructed recurrence Assertions to measure"
        ) from exc
    except ComparisonResultMeasurementError as exc:
        raise RecurrenceSubjectMeasurementError(str(exc)) from exc

    def measured(assertion):
        subject = assertion.payload["assertion_subject"]
        if set(subject) != set(RECURRENCE_SUBJECT_COORDINATES):
            raise RecurrenceSubjectMeasurementError(
                "recurrence Assertion does not carry the established immediate subject surface"
            )
        return MeasuredRecurrenceSubjectCoordinates(
            source=assertion,
            coordinates=tuple(
                (name, subject[name]) for name in RECURRENCE_SUBJECT_COORDINATES
            ),
        )

    def stream() -> Iterator[MeasuredRecurrenceSubjectCoordinates]:
        yield measured(first)
        try:
            for assertion in reconstructed:
                if assertion.result == "recurrence":
                    yield measured(assertion)
        except ComparisonResultMeasurementError as exc:
            raise RecurrenceSubjectMeasurementError(str(exc)) from exc

    return stream()


def _coordinate_assertions(
    finding: MeasuredRecurrenceSubjectCoordinates,
) -> tuple[dict[str, Any], ...]:
    source_scope = finding.source.payload["assertion_scope"]
    scope = {
        "workspace_id": source_scope["workspace_id"],
        "source_session_ids": list(source_scope["source_session_ids"]),
    }
    source_ref = finding.source.reference
    assertions = []
    for coordinate, value in finding.coordinates:
        identity = _assertion_identity(
            coordinate=coordinate,
            value=value,
            scope=scope,
        )
        assertions.append(
            {
                "dimensions": {
                    "identity": identity,
                    "content": {"exact_value": value},
                    "standing": "measured",
                    "source_provenance": (
                        "the exact recurrence Assertion production carried in support_basis"
                    ),
                    "responsibility": MEASURED_ASSERTION_RESPONSIBILITY,
                    "authority": MEASUREMENT_AUTHORITY,
                },
                "subject_kind": "assertion",
                "responsible_boundary": "this recorded assertion",
                "result": "recurrence_subject_coordinate_value",
                "assertion_subject": {
                    "source_assertion_result": "recurrence",
                    "coordinate": coordinate,
                },
                "assertion_scope": scope,
                "support_basis": {"assertion_refs": [source_ref]},
                "unknowns": list(MEASUREMENT_UNKNOWNS),
                "forbidden_inferences": list(FORBIDDEN_INFERENCES),
            }
        )
    return tuple(assertions)


def _measurement_event(
    *,
    workspace_id: str,
    session_id: str,
    finding: MeasuredRecurrenceSubjectCoordinates,
) -> Event:
    if finding.source.payload["assertion_scope"]["workspace_id"] != workspace_id:
        raise RecurrenceSubjectMeasurementError(
            "recording workspace must equal the recurrence Assertion workspace"
        )
    assertions = _coordinate_assertions(finding)
    return Event(
        id=new_id("evt"),
        kind=RECURRENCE_SUBJECT_COORDINATES_RECORDED_KIND,
        workspace_id=workspace_id,
        session_id=session_id,
        payload={
            "dimensions": {
                "identity": "recurrence-subject-coordinate-measurement-occurrence",
                "content": "three distinct immediate coordinate Assertions recorded",
                "standing": "recorded",
                "source_provenance": "one occurrence-bound recurrence Assertion",
                "authority": MEASUREMENT_AUTHORITY,
            },
            "producing_act": "declared Measurement",
            "measurement_subject": "one reconstructed recurrence Assertion subject",
            "source_assertion_ref": finding.source.reference,
            "assertions": list(assertions),
        },
    )


def record_recurrence_subject_coordinate_layer(
    ledger: EventLedger,
    *,
    workspace_id: str,
    source_session_ids: Iterable[str],
    recording_session_id: str,
) -> int:
    """Record one three-result Measurement occurrence per recurrence production."""

    if not isinstance(recording_session_id, str) or not recording_session_id:
        raise RecurrenceSubjectMeasurementError(
            "recurrence-subject recording requires an exact session"
        )
    pending = []
    recorded = 0
    for finding in measure_recurrence_subject_coordinates(
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


def assertions_of_recorded_recurrence_subject_coordinates(
    event: Event,
) -> tuple[RecordedRecurrenceSubjectCoordinateAssertion, ...]:
    """Structurally reconstruct the exact three-result output contract."""

    assertions = event.payload.get("assertions")
    source_ref = event.payload.get("source_assertion_ref")
    if (
        event.kind != RECURRENCE_SUBJECT_COORDINATES_RECORDED_KIND
        or event.payload.get("dimensions")
        != {
            "identity": "recurrence-subject-coordinate-measurement-occurrence",
            "content": "three distinct immediate coordinate Assertions recorded",
            "standing": "recorded",
            "source_provenance": "one occurrence-bound recurrence Assertion",
            "authority": MEASUREMENT_AUTHORITY,
        }
        or event.payload.get("producing_act") != "declared Measurement"
        or event.payload.get("measurement_subject")
        != "one reconstructed recurrence Assertion subject"
        or not isinstance(source_ref, dict)
        or set(source_ref) != {"producing_event_id", "assertion_id"}
        or not isinstance(assertions, list)
        or len(assertions) != len(RECURRENCE_SUBJECT_COORDINATES)
    ):
        raise RecurrenceSubjectMeasurementError(
            f"{event.id} does not carry the established coordinate Measurement"
        )
    reconstructed = []
    seen = set()
    for assertion in assertions:
        dimensions = assertion.get("dimensions")
        subject = assertion.get("assertion_subject")
        scope = assertion.get("assertion_scope")
        content = dimensions.get("content") if isinstance(dimensions, dict) else None
        coordinate = subject.get("coordinate") if isinstance(subject, dict) else None
        if (
            coordinate not in RECURRENCE_SUBJECT_COORDINATES
            or coordinate in seen
            or subject
            != {
                "source_assertion_result": "recurrence",
                "coordinate": coordinate,
            }
            or not isinstance(scope, dict)
            or set(scope) != {"workspace_id", "source_session_ids"}
            or scope.get("workspace_id") != event.workspace_id
            or not isinstance(scope.get("source_session_ids"), list)
            or not scope["source_session_ids"]
            or not isinstance(content, dict)
            or set(content) != {"exact_value"}
            or assertion.get("subject_kind") != "assertion"
            or assertion.get("responsible_boundary") != "this recorded assertion"
            or assertion.get("result") != "recurrence_subject_coordinate_value"
            or assertion.get("support_basis") != {"assertion_refs": [source_ref]}
            or assertion.get("unknowns") != list(MEASUREMENT_UNKNOWNS)
            or assertion.get("forbidden_inferences") != list(FORBIDDEN_INFERENCES)
            or not isinstance(dimensions, dict)
            or dimensions.get("standing") != "measured"
            or dimensions.get("source_provenance")
            != "the exact recurrence Assertion production carried in support_basis"
            or dimensions.get("responsibility") != MEASURED_ASSERTION_RESPONSIBILITY
            or dimensions.get("authority") != MEASUREMENT_AUTHORITY
        ):
            raise RecurrenceSubjectMeasurementError(
                f"{event.id} carries an incoherent coordinate Assertion"
            )
        identity = _assertion_identity(
            coordinate=coordinate,
            value=content["exact_value"],
            scope=scope,
        )
        if dimensions.get("identity") != identity:
            raise RecurrenceSubjectMeasurementError(
                f"{event.id} carries a noncanonical coordinate Assertion"
            )
        seen.add(coordinate)
        reconstructed.append(
            RecordedRecurrenceSubjectCoordinateAssertion(
                assertion_id=identity,
                producing_event_id=event.id,
                coordinate=coordinate,
                payload=assertion,
            )
        )
    if seen != set(RECURRENCE_SUBJECT_COORDINATES):
        raise RecurrenceSubjectMeasurementError(
            f"{event.id} does not carry the complete immediate coordinate surface"
        )
    return tuple(reconstructed)


def get_recorded_recurrence_subject_coordinate_assertion(
    ledger: EventLedger,
    *,
    producing_event_id: str,
    assertion_id: str,
) -> RecordedRecurrenceSubjectCoordinateAssertion | None:
    """Resolve one coordinate result after reconstructing its exact source Assertion."""

    event = ledger.get(producing_event_id)
    if event is None:
        return None
    if ledger.integrity_of(producing_event_id) == CORRUPTED:
        raise RecurrenceSubjectMeasurementError(
            "a corrupted Measurement occurrence cannot expose coordinate Assertions"
        )
    reconstructed = assertions_of_recorded_recurrence_subject_coordinates(event)
    source_ref = event.payload["source_assertion_ref"]
    source = get_recorded_comparison_result_count_assertion(
        ledger,
        producing_event_id=source_ref["producing_event_id"],
        assertion_id=source_ref["assertion_id"],
    )
    if source is None or source.result != "recurrence":
        raise RecurrenceSubjectMeasurementError(
            "coordinate Measurement does not have as input a reconstructed recurrence Assertion"
        )
    source_scope = source.payload["assertion_scope"]
    expected_scope = {
        "workspace_id": source_scope["workspace_id"],
        "source_session_ids": list(source_scope["source_session_ids"]),
    }
    expected = dict(
        zip(
            RECURRENCE_SUBJECT_COORDINATES,
            (source.payload["assertion_subject"][name] for name in RECURRENCE_SUBJECT_COORDINATES),
        )
    )
    for item in reconstructed:
        if (
            item.payload["assertion_scope"] != expected_scope
            or item.payload["dimensions"]["content"]["exact_value"]
            != expected[item.coordinate]
        ):
            raise RecurrenceSubjectMeasurementError(
                "coordinate Measurement result does not match its source Assertion"
            )
        if item.assertion_id == assertion_id:
            return item
    return None


def iter_recorded_recurrence_subject_coordinate_assertions(
    ledger: EventLedger,
    *,
    workspace_id: str,
    session_ids: Iterable[str],
    through: EventLedgerBoundary,
) -> Iterator[RecordedRecurrenceSubjectCoordinateAssertion]:
    """Reconstruct one bounded coordinate-Assertion population efficiently."""

    sessions = tuple(dict.fromkeys(session_ids))
    if not sessions:
        raise RecurrenceSubjectMeasurementError(
            "coordinate-Assertion reconstruction requires exact declared sessions"
        )
    source_sessions = set()
    source_refs = set()
    for session_id in sessions:
        for event in ledger.iter_session_kind(
            workspace_id,
            session_id,
            RECURRENCE_SUBJECT_COORDINATES_RECORDED_KIND,
            through=through,
        ):
            source_ref = event.payload.get("source_assertion_ref")
            if not isinstance(source_ref, dict):
                raise RecurrenceSubjectMeasurementError(
                    "coordinate Measurement does not carry its source reference"
                )
            source_event = ledger.get(source_ref.get("producing_event_id"))
            if (
                source_event is None
                or source_event.workspace_id != workspace_id
                or not source_event.session_id
            ):
                raise RecurrenceSubjectMeasurementError(
                    "coordinate Measurement source is not reconstructible in this workspace"
                )
            source_sessions.add(source_event.session_id)
            source_refs.add(
                (source_ref.get("producing_event_id"), source_ref.get("assertion_id"))
            )

    if not source_refs:
        return

    validated_sources = {}
    try:
        for source in iter_recorded_comparison_result_count_assertions(
            ledger,
            workspace_id=workspace_id,
            session_ids=tuple(sorted(source_sessions)),
            through=through,
        ):
            key = (source.producing_event_id, source.assertion_id)
            if key in source_refs and source.result == "recurrence":
                validated_sources[key] = source
    except ComparisonResultMeasurementError as exc:
        raise RecurrenceSubjectMeasurementError(str(exc)) from exc
    if set(validated_sources) != source_refs:
        raise RecurrenceSubjectMeasurementError(
            "coordinate Measurement population contains an unestablished recurrence source"
        )

    for session_id in sessions:
        for event in ledger.iter_session_kind(
            workspace_id,
            session_id,
            RECURRENCE_SUBJECT_COORDINATES_RECORDED_KIND,
            through=through,
        ):
            if ledger.integrity_of(event.id) == CORRUPTED:
                raise RecurrenceSubjectMeasurementError(
                    "a corrupted Measurement occurrence cannot expose coordinate Assertions"
                )
            reconstructed = assertions_of_recorded_recurrence_subject_coordinates(event)
            source_ref = event.payload["source_assertion_ref"]
            source = validated_sources[
                (source_ref["producing_event_id"], source_ref["assertion_id"])
            ]
            source_scope = source.payload["assertion_scope"]
            expected_scope = {
                "workspace_id": source_scope["workspace_id"],
                "source_session_ids": list(source_scope["source_session_ids"]),
            }
            expected_values = source.payload["assertion_subject"]
            for item in reconstructed:
                if (
                    item.payload["assertion_scope"] != expected_scope
                    or item.payload["dimensions"]["content"]["exact_value"]
                    != expected_values[item.coordinate]
                ):
                    raise RecurrenceSubjectMeasurementError(
                        "coordinate Measurement result does not match its source Assertion"
                    )
                yield item
