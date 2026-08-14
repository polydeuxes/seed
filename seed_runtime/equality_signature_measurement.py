"""Measure the complete literal equality signature of recorded Compare outputs.

One recorded positional-result Compare already carries one result Assertion for
every coordinate in its established comparison surface.  This declared
Measurement preserves the maximal same/different partition of that surface.
It selects no subset and establishes no Equivalence, similarity, relation,
represented relation, or significance for either partition.
"""

from __future__ import annotations


from dataclasses import dataclass
import hashlib
from itertools import chain
import json
from typing import Any, Iterable, Iterator

from seed_runtime.assertion_comparison import (
    POSITIONAL_RESULT_COMPARISON_RECORDED_KIND,
    POSITIONAL_RESULT_COORDINATES,
    AssertionComparisonError,
    RecordedPositionalResultDistinction,
    iter_recorded_positional_result_distinctions,
    _validate_recorded_positional_result_comparison,
)
from seed_runtime.event import Event
from seed_runtime.events import CORRUPTED, EventLedger, EventLedgerBoundary
from seed_runtime.ids import new_id


EQUALITY_SIGNATURE_RECORDED_KIND = (
    "operator.measurement.positional_equality_signature_recorded"
)
SIGNATURE_RESULT = "exact_equality_signature"
MEASURED_ASSERTION_RESPONSIBILITY = (
    "preserve the fidelity of this measured Assertion's Standing to its "
    "carried coordinates"
)
MEASUREMENT_AUTHORITY = (
    "literal Measurement Evidence only; establishes no Equivalence, similarity, "
    "relation, represented relation, significance, or Standing movement"
)
MEASUREMENT_UNKNOWNS = (
    "whether any coordinate agreement or distinction matters to a later exact Act "
    "remains Unknown",
)
FORBIDDEN_INFERENCES = (
    "an exact equality signature is not Equivalence, similarity, relation, "
    "represented relation, significance, interchangeability, or Standing strength",
)


class EqualitySignatureMeasurementError(ValueError):
    """The bounded equality-signature Measurement could not be established."""


@dataclass(frozen=True)
class MeasuredEqualitySignature:
    source_event_id: str
    source_assertions: tuple[RecordedPositionalResultDistinction, ...]
    source_session_ids: tuple[str, ...]
    same_coordinates: tuple[str, ...]
    different_coordinates: tuple[str, ...]


@dataclass(frozen=True)
class RecordedEqualitySignatureAssertion:
    assertion_id: str
    producing_event_id: str
    payload: dict[str, Any]

    @property
    def reference(self) -> dict[str, str]:
        return {
            "producing_event_id": self.producing_event_id,
            "assertion_id": self.assertion_id,
        }


def _canonical(value: Any) -> str:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    )


def _surface() -> tuple[str, ...]:
    return tuple(POSITIONAL_RESULT_COORDINATES)


def _subject() -> dict[str, Any]:
    return {
        "comparison_result": "positional_result_coordinate_distinction",
        "declared_coordinate_surface": list(_surface()),
    }


def _content(
    *, same_coordinates: Iterable[str], different_coordinates: Iterable[str]
) -> dict[str, list[str]]:
    return {
        "same_coordinates": list(same_coordinates),
        "different_coordinates": list(different_coordinates),
    }


def _identity(*, scope: dict[str, Any], content: dict[str, Any]) -> str:
    represented = {
        "result": SIGNATURE_RESULT,
        "subject": _subject(),
        "scope": scope,
        "content": content,
    }
    return "positional-equality-signature:" + hashlib.sha256(
        _canonical(represented).encode("utf-8")
    ).hexdigest()


def measure_equality_signatures(
    ledger: EventLedger,
    *,
    workspace_id: str,
    source_session_ids: Iterable[str],
) -> Iterator[MeasuredEqualitySignature]:
    """Measure one complete equality signature per recorded Compare."""

    sessions = tuple(dict.fromkeys(source_session_ids))
    if not sessions or any(not isinstance(item, str) or not item for item in sessions):
        raise EqualitySignatureMeasurementError(
            "equality-signature Measurement requires exact declared source sessions"
        )
    boundary = ledger.capture_boundary()
    missing = [
        item
        for item in sessions
        if not ledger.has_session(workspace_id, item, through=boundary)
    ]
    if missing:
        raise EqualitySignatureMeasurementError(
            "declared source sessions are absent through the Measurement boundary: "
            + ", ".join(missing)
        )

    def measured(
        results: list[RecordedPositionalResultDistinction],
    ) -> MeasuredEqualitySignature:
        by_coordinate = {result.coordinate: result for result in results}
        if len(results) != len(_surface()) or set(by_coordinate) != set(_surface()):
            raise EqualitySignatureMeasurementError(
                "a Compare occurrence did not yield the exact declared surface"
            )
        same = tuple(
            name
            for name in _surface()
            if by_coordinate[name].payload["dimensions"]["content"]["same"]
        )
        different = tuple(name for name in _surface() if name not in same)
        return MeasuredEqualitySignature(
            source_event_id=results[0].producing_event_id,
            source_assertions=tuple(by_coordinate[name] for name in _surface()),
            source_session_ids=sessions,
            same_coordinates=same,
            different_coordinates=different,
        )

    try:
        reconstructed = iter_recorded_positional_result_distinctions(
            ledger,
            workspace_id=workspace_id,
            session_ids=sessions,
            through=boundary,
        )
        first = next(reconstructed)
    except StopIteration as exc:
        raise EqualitySignatureMeasurementError(
            "no reconstructed positional-result Comparisons to measure"
        ) from exc
    except AssertionComparisonError as exc:
        raise EqualitySignatureMeasurementError(str(exc)) from exc

    def stream() -> Iterator[MeasuredEqualitySignature]:
        current_event_id: str | None = None
        current: list[RecordedPositionalResultDistinction] = []
        try:
            for result in chain((first,), reconstructed):
                if current_event_id is None:
                    current_event_id = result.producing_event_id
                if result.producing_event_id != current_event_id:
                    yield measured(current)
                    current = []
                    current_event_id = result.producing_event_id
                current.append(result)
        except AssertionComparisonError as exc:
            raise EqualitySignatureMeasurementError(str(exc)) from exc
        if current:
            yield measured(current)

    return stream()


def _assertion(finding: MeasuredEqualitySignature, *, workspace_id: str) -> dict[str, Any]:
    scope = {
        "workspace_id": workspace_id,
        "source_session_ids": list(finding.source_session_ids),
    }
    content = _content(
        same_coordinates=finding.same_coordinates,
        different_coordinates=finding.different_coordinates,
    )
    identity = _identity(scope=scope, content=content)
    refs = [item.reference for item in finding.source_assertions]
    return {
        "dimensions": {
            "identity": identity,
            "content": content,
            "standing": "measured",
            "source_provenance": (
                "the complete coordinate-result Assertion surface of one recorded Compare"
            ),
            "responsibility": MEASURED_ASSERTION_RESPONSIBILITY,
            "authority": MEASUREMENT_AUTHORITY,
        },
        "subject_kind": "assertion",
        "responsible_boundary": "this recorded assertion",
        "result": SIGNATURE_RESULT,
        "assertion_subject": _subject(),
        "assertion_scope": scope,
        "support_basis": {"assertion_refs": refs},
        "source_compare_event_id": finding.source_event_id,
        "unknowns": list(MEASUREMENT_UNKNOWNS),
        "forbidden_inferences": list(FORBIDDEN_INFERENCES),
    }


def _event(
    *, workspace_id: str, session_id: str, finding: MeasuredEqualitySignature
) -> Event:
    assertion = _assertion(finding, workspace_id=workspace_id)
    return Event(
        id=new_id("evt"),
        kind=EQUALITY_SIGNATURE_RECORDED_KIND,
        workspace_id=workspace_id,
        session_id=session_id,
        payload={
            "dimensions": {
                "identity": "positional-equality-signature-measurement-occurrence",
                "content": "one exact equality-signature Assertion recorded",
                "standing": "recorded",
                "source_provenance": "one recorded positional-result Compare",
                "authority": MEASUREMENT_AUTHORITY,
            },
            "producing_act": "declared Measurement",
            "measurement_subject": "complete positional-result Compare coordinate surface",
            "source_compare_event_id": finding.source_event_id,
            "assertions": [assertion],
        },
    )


def record_equality_signature_layer(
    ledger: EventLedger,
    *,
    workspace_id: str,
    source_session_ids: Iterable[str],
    recording_session_id: str,
) -> int:
    """Measure and durably record every available exact signature once."""

    if not isinstance(recording_session_id, str) or not recording_session_id:
        raise EqualitySignatureMeasurementError(
            "equality-signature recording requires an exact session"
        )
    pending: list[Event] = []
    recorded = 0
    for finding in measure_equality_signatures(
        ledger,
        workspace_id=workspace_id,
        source_session_ids=source_session_ids,
    ):
        pending.append(
            _event(
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


def assertion_of_recorded_equality_signature(
    event: Event,
) -> RecordedEqualitySignatureAssertion:
    """Structurally reconstruct one exact signature Assertion."""

    stated = event.payload.get("assertions")
    if (
        event.kind != EQUALITY_SIGNATURE_RECORDED_KIND
        or not isinstance(stated, list)
        or len(stated) != 1
        or event.payload.get("dimensions")
        != {
            "identity": "positional-equality-signature-measurement-occurrence",
            "content": "one exact equality-signature Assertion recorded",
            "standing": "recorded",
            "source_provenance": "one recorded positional-result Compare",
            "authority": MEASUREMENT_AUTHORITY,
        }
        or event.payload.get("producing_act") != "declared Measurement"
        or event.payload.get("measurement_subject")
        != "complete positional-result Compare coordinate surface"
    ):
        raise EqualitySignatureMeasurementError(
            f"{event.id} does not carry the established Measurement occurrence"
        )
    assertion = stated[0]
    dimensions = assertion.get("dimensions") if isinstance(assertion, dict) else None
    content = dimensions.get("content") if isinstance(dimensions, dict) else None
    scope = assertion.get("assertion_scope") if isinstance(assertion, dict) else None
    support = assertion.get("support_basis") if isinstance(assertion, dict) else None
    refs = support.get("assertion_refs") if isinstance(support, dict) else None
    source_event_id = assertion.get("source_compare_event_id") if isinstance(assertion, dict) else None
    surface = _surface()
    if (
        assertion.get("subject_kind") != "assertion"
        or assertion.get("responsible_boundary") != "this recorded assertion"
        or assertion.get("result") != SIGNATURE_RESULT
        or assertion.get("assertion_subject") != _subject()
        or not isinstance(dimensions, dict)
        or dimensions.get("standing") != "measured"
        or dimensions.get("source_provenance")
        != "the complete coordinate-result Assertion surface of one recorded Compare"
        or dimensions.get("responsibility") != MEASURED_ASSERTION_RESPONSIBILITY
        or dimensions.get("authority") != MEASUREMENT_AUTHORITY
        or not isinstance(content, dict)
        or set(content) != {"same_coordinates", "different_coordinates"}
        or not isinstance(scope, dict)
        or scope.get("workspace_id") != event.workspace_id
        or set(scope) != {"workspace_id", "source_session_ids"}
        or not isinstance(scope.get("source_session_ids"), list)
        or not scope["source_session_ids"]
        or not isinstance(refs, list)
        or len(refs) != len(surface)
        or not isinstance(source_event_id, str)
        or event.payload.get("source_compare_event_id") != source_event_id
        or assertion.get("unknowns") != list(MEASUREMENT_UNKNOWNS)
        or assertion.get("forbidden_inferences") != list(FORBIDDEN_INFERENCES)
    ):
        raise EqualitySignatureMeasurementError(
            f"{event.id} carries an incoherent equality-signature Assertion"
        )
    same = content["same_coordinates"]
    different = content["different_coordinates"]
    if (
        not isinstance(same, list)
        or not isinstance(different, list)
        or same != [name for name in surface if name in same]
        or different != [name for name in surface if name in different]
        or not set(same).isdisjoint(set(different))
        or set(same) | set(different) != set(surface)
        or any(
            not isinstance(ref, dict)
            or set(ref) != {"producing_event_id", "assertion_id"}
            or ref["producing_event_id"] != source_event_id
            for ref in refs
        )
        or dimensions.get("identity") != _identity(scope=scope, content=content)
    ):
        raise EqualitySignatureMeasurementError(
            f"{event.id} carries a noncanonical equality signature"
        )
    return RecordedEqualitySignatureAssertion(
        assertion_id=dimensions["identity"],
        producing_event_id=event.id,
        payload=assertion,
    )


def get_recorded_equality_signature(
    ledger: EventLedger, *, producing_event_id: str, assertion_id: str
) -> RecordedEqualitySignatureAssertion | None:
    """Resolve a signature after replaying its exact source Compare."""

    event = ledger.get(producing_event_id)
    if event is None:
        return None
    reconstructed = _validate_equality_signature(ledger, event)
    return reconstructed if reconstructed.assertion_id == assertion_id else None


def _validate_equality_signature(
    ledger: EventLedger,
    event: Event,
) -> RecordedEqualitySignatureAssertion:
    """Reconstruct one signature from an Event the caller already holds."""

    if ledger.integrity_of(event.id) == CORRUPTED:
        raise EqualitySignatureMeasurementError(
            "a corrupted Measurement occurrence cannot expose its Assertion"
        )
    reconstructed = assertion_of_recorded_equality_signature(event)
    refs = reconstructed.payload["support_basis"]["assertion_refs"]
    source_event_id = reconstructed.payload["source_compare_event_id"]
    source_event = ledger.get(source_event_id)
    if source_event is None:
        raise EqualitySignatureMeasurementError(
            "the source Compare occurrence is not reconstructible"
        )
    if ledger.integrity_of(source_event_id) == CORRUPTED:
        raise EqualitySignatureMeasurementError(
            "a corrupted Compare occurrence cannot support a signature"
        )
    try:
        source = _validate_recorded_positional_result_comparison(ledger, source_event)
    except AssertionComparisonError as exc:
        raise EqualitySignatureMeasurementError(str(exc)) from exc
    by_coordinate = {item.coordinate: item for item in source}
    if (
        len(source) != len(_surface())
        or set(by_coordinate) != set(_surface())
        or [by_coordinate[name].reference for name in _surface()] != refs
    ):
        raise EqualitySignatureMeasurementError(
            "signature support is not the complete source Compare surface"
        )
    expected_same = [
        name
        for name in _surface()
        if by_coordinate[name].payload["dimensions"]["content"]["same"]
    ]
    expected = _content(
        same_coordinates=expected_same,
        different_coordinates=[name for name in _surface() if name not in expected_same],
    )
    if reconstructed.payload["dimensions"]["content"] != expected:
        raise EqualitySignatureMeasurementError(
            "signature does not match its complete source Compare surface"
        )
    return reconstructed


def iter_recorded_equality_signatures(
    ledger: EventLedger,
    *,
    workspace_id: str,
    session_ids: Iterable[str],
    through: EventLedgerBoundary,
) -> Iterator[RecordedEqualitySignatureAssertion]:
    """Validate and stream bounded sequence of signature Assertions."""

    for session_id in tuple(dict.fromkeys(session_ids)):
        for event in ledger.iter_session_kind(
            workspace_id,
            session_id,
            EQUALITY_SIGNATURE_RECORDED_KIND,
            through=through,
        ):
            yield _validate_equality_signature(ledger, event)
