"""Count productions of exact equality-signature Assertions.

Canonical signature identity supplies the grouping boundary.  This declared
Measurement produces an exact production set, its count, and recurrence only
where the count exceeds one.  It forms no pairs and establishes no
Equivalence, similarity, relation, profile, meaning, or significance.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from typing import Any, Iterable, Iterator

from seed_runtime.equality_signature_measurement import (
    EQUALITY_SIGNATURE_RECORDED_KIND,
    EqualitySignatureMeasurementError,
    RecordedEqualitySignatureAssertion,
    iter_recorded_equality_signatures,
)
from seed_runtime.event import Event
from seed_runtime.events import CORRUPTED, EventLedger, EventLedgerBoundary
from seed_runtime.ids import new_id


EQUALITY_SIGNATURE_COUNT_RECORDED_KIND = (
    "operator.measurement.equality_signature_count_recorded"
)
MEASURED_ASSERTION_RESPONSIBILITY = (
    "preserve the fidelity of this measured Assertion's Standing to its "
    "carried coordinates"
)
MEASUREMENT_AUTHORITY = (
    "literal Measurement Evidence only; establishes no Equivalence, similarity, "
    "relation, profile, meaning, significance, or Standing movement"
)
MEASUREMENT_UNKNOWNS = (
    "why this exact equality signature recurs remains Unknown",
)
PRODUCTION_SET_FORBIDDEN_INFERENCES = (
    "an exact production set is not recurrence, Equivalence, similarity, relation, "
    "profile, meaning, significance, or Standing strength",
)
COUNT_FORBIDDEN_INFERENCES = (
    "a production count does not itself produce recurrence, Equivalence, "
    "similarity, relation, profile, meaning, significance, or Standing strength",
)
RECURRENCE_FORBIDDEN_INFERENCES = (
    "recurrence of an exact equality signature is not Equivalence, similarity, "
    "relation, profile, meaning, significance, or Standing strength",
)


class EqualitySignatureRecurrenceError(ValueError):
    """The signature recurrence Measurement could not be established."""


@dataclass(frozen=True)
class MeasuredEqualitySignatureCount:
    measured_assertion_id: str
    signature_subject: dict[str, Any]
    signature_content: dict[str, Any]
    assertion_scope: dict[str, Any]
    production_refs: tuple[dict[str, str], ...]
    completeness_boundary: EventLedgerBoundary
    source_session_ids: tuple[str, ...]

    @property
    def count(self) -> int:
        return len(self.production_refs)


@dataclass(frozen=True)
class RecordedEqualitySignatureCountAssertion:
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
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    )


def _identity(
    *, result: str, subject: dict[str, Any], scope: dict[str, Any], content: Any
) -> str:
    represented = {
        "result": result,
        "subject": subject,
        "scope": scope,
        "content": content,
    }
    return "equality-signature-measurement:" + hashlib.sha256(
        _canonical(represented).encode("utf-8")
    ).hexdigest()


def measure_equality_signature_counts(
    ledger: EventLedger,
    *,
    workspace_id: str,
    source_session_ids: Iterable[str],
) -> Iterator[MeasuredEqualitySignatureCount]:
    """Group the complete bounded signature population by canonical identity."""

    sessions = tuple(dict.fromkeys(source_session_ids))
    if not sessions or any(not isinstance(item, str) or not item for item in sessions):
        raise EqualitySignatureRecurrenceError(
            "signature-count Measurement requires exact declared source sessions"
        )
    boundary = ledger.capture_boundary()
    missing = [
        item
        for item in sessions
        if not ledger.has_session(workspace_id, item, through=boundary)
    ]
    if missing:
        raise EqualitySignatureRecurrenceError(
            "declared source sessions are absent through the Measurement boundary: "
            + ", ".join(missing)
        )
    grouped: dict[str, tuple[RecordedEqualitySignatureAssertion, list[dict[str, str]]]] = {}
    try:
        for assertion in iter_recorded_equality_signatures(
            ledger,
            workspace_id=workspace_id,
            session_ids=sessions,
            through=boundary,
        ):
            existing = grouped.get(assertion.assertion_id)
            if existing is None:
                grouped[assertion.assertion_id] = (assertion, [assertion.reference])
            else:
                exemplar, refs = existing
                if (
                    exemplar.payload["assertion_subject"]
                    != assertion.payload["assertion_subject"]
                    or exemplar.payload["assertion_scope"]
                    != assertion.payload["assertion_scope"]
                    or exemplar.payload["dimensions"]["content"]
                    != assertion.payload["dimensions"]["content"]
                ):
                    raise EqualitySignatureRecurrenceError(
                        "one canonical signature identity carries different coordinates"
                    )
                refs.append(assertion.reference)
    except EqualitySignatureMeasurementError as exc:
        raise EqualitySignatureRecurrenceError(str(exc)) from exc
    if not grouped:
        raise EqualitySignatureRecurrenceError(
            "no recovered equality-signature Assertions to measure"
        )
    findings = []
    for assertion_id, (exemplar, refs) in grouped.items():
        findings.append(MeasuredEqualitySignatureCount(
            measured_assertion_id=assertion_id,
            signature_subject=dict(exemplar.payload["assertion_subject"]),
            signature_content=dict(exemplar.payload["dimensions"]["content"]),
            assertion_scope=dict(exemplar.payload["assertion_scope"]),
            production_refs=tuple(refs),
            completeness_boundary=boundary,
            source_session_ids=sessions,
        ))
    return iter(findings)


def _subject(finding: MeasuredEqualitySignatureCount) -> dict[str, Any]:
    return {
        "measured_assertion_id": finding.measured_assertion_id,
        "signature_subject": finding.signature_subject,
        "exact_equality_signature": finding.signature_content,
    }


def _assertions(finding: MeasuredEqualitySignatureCount) -> list[dict[str, Any]]:
    subject = _subject(finding)
    scope = finding.assertion_scope
    refs = list(finding.production_refs)
    set_content = {"production_refs": refs}
    count_content = {"production_count": finding.count}
    set_id = _identity(
        result="exact_production_set", subject=subject, scope=scope, content=set_content
    )
    count_id = _identity(
        result="count", subject=subject, scope=scope, content=count_content
    )

    def shell(
        *, result: str, identity: str, content: Any, provenance: str,
        support: dict[str, Any], forbidden: tuple[str, ...]
    ) -> dict[str, Any]:
        return {
            "dimensions": {
                "identity": identity,
                "content": content,
                "standing": "measured",
                "source_provenance": provenance,
                "responsibility": MEASURED_ASSERTION_RESPONSIBILITY,
                "authority_warrant": MEASUREMENT_AUTHORITY,
            },
            "subject_kind": "assertion",
            "responsibility_owner": "this recorded assertion",
            "result": result,
            "assertion_subject": subject,
            "assertion_scope": scope,
            "support_basis": support,
            "unknowns": list(MEASUREMENT_UNKNOWNS),
            "forbidden_inferences": list(forbidden),
        }

    results = [
        {
            **shell(
                result="exact_production_set",
                identity=set_id,
                content=set_content,
                provenance="recorded exact equality-signature Assertion productions",
                support={"assertion_refs": refs},
                forbidden=PRODUCTION_SET_FORBIDDEN_INFERENCES,
            ),
            "completeness_boundary": {
                "commitment": finding.completeness_boundary.commitment
            },
            "completeness_scope": {
                "workspace_id": scope["workspace_id"],
                "source_session_ids": list(finding.source_session_ids),
                "occurrence_kind": EQUALITY_SIGNATURE_RECORDED_KIND,
            },
        },
        shell(
            result="count",
            identity=count_id,
            content=count_content,
            provenance="the exact production-set Assertion carried here",
            support={"local_assertion_ids": [set_id]},
            forbidden=COUNT_FORBIDDEN_INFERENCES,
        ),
    ]
    if finding.count > 1:
        recurrence_content = {"recurrence_established": True}
        results.append(
            shell(
                result="recurrence",
                identity=_identity(
                    result="recurrence",
                    subject=subject,
                    scope=scope,
                    content=recurrence_content,
                ),
                content=recurrence_content,
                provenance="the exact count Assertion carried here",
                support={"local_assertion_ids": [count_id]},
                forbidden=RECURRENCE_FORBIDDEN_INFERENCES,
            )
        )
    return results


def _event(
    *, workspace_id: str, session_id: str, finding: MeasuredEqualitySignatureCount
) -> Event:
    assertions = _assertions(finding)
    return Event(
        id=new_id("evt"),
        kind=EQUALITY_SIGNATURE_COUNT_RECORDED_KIND,
        workspace_id=workspace_id,
        session_id=session_id,
        payload={
            "dimensions": {
                "identity": "equality-signature-count-measurement-occurrence",
                "content": f"{len(assertions)} distinct measured Assertions recorded",
                "standing": "recorded",
                "source_provenance": "recorded exact equality-signature Assertions",
                "authority_warrant": MEASUREMENT_AUTHORITY,
            },
            "producing_act": "declared Measurement",
            "measurement_subject": "recorded exact equality-signature Assertions",
            "assertions": assertions,
        },
    )


def record_equality_signature_count_layer(
    ledger: EventLedger,
    *,
    workspace_id: str,
    source_session_ids: Iterable[str],
    recording_session_id: str,
) -> int:
    if not isinstance(recording_session_id, str) or not recording_session_id:
        raise EqualitySignatureRecurrenceError(
            "signature-count recording requires an exact session"
        )
    pending: list[Event] = []
    recorded = 0
    for finding in measure_equality_signature_counts(
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


def assertions_of_recorded_equality_signature_count(
    event: Event,
) -> tuple[RecordedEqualitySignatureCountAssertion, ...]:
    """Recover the exact set/count/conditional-recurrence output contract."""

    stated = event.payload.get("assertions")
    dimensions = event.payload.get("dimensions")
    if (
        event.kind != EQUALITY_SIGNATURE_COUNT_RECORDED_KIND
        or not isinstance(stated, list)
        or len(stated) not in (2, 3)
        or dimensions
        != {
            "identity": "equality-signature-count-measurement-occurrence",
            "content": f"{len(stated)} distinct measured Assertions recorded",
            "standing": "recorded",
            "source_provenance": "recorded exact equality-signature Assertions",
            "authority_warrant": MEASUREMENT_AUTHORITY,
        }
        or event.payload.get("producing_act") != "declared Measurement"
        or event.payload.get("measurement_subject")
        != "recorded exact equality-signature Assertions"
    ):
        raise EqualitySignatureRecurrenceError(
            f"{event.id} does not carry the established Measurement occurrence"
        )
    by_result = {
        item.get("result"): item for item in stated if isinstance(item, dict)
    }
    if set(by_result) not in (
        {"exact_production_set", "count"},
        {"exact_production_set", "count", "recurrence"},
    ):
        raise EqualitySignatureRecurrenceError(
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
        != {"measured_assertion_id", "signature_subject", "exact_equality_signature"}
        or not isinstance(subject.get("measured_assertion_id"), str)
        or not isinstance(scope, dict)
        or set(scope) != {"workspace_id", "source_session_ids"}
        or scope.get("workspace_id") != event.workspace_id
        or not isinstance(scope.get("source_session_ids"), list)
        or not scope["source_session_ids"]
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
        != EQUALITY_SIGNATURE_RECORDED_KIND
        or count.get("assertion_subject") != subject
        or count.get("assertion_scope") != scope
        or count_content != {"production_count": len(refs)}
        or (recurrence is None) != (len(refs) == 1)
    ):
        raise EqualitySignatureRecurrenceError(
            f"{event.id} carries incoherent Measurement coordinates"
        )

    def require_shell(item, item_dimensions, provenance, support, forbidden):
        if (
            item.get("subject_kind") != "assertion"
            or item.get("responsibility_owner") != "this recorded assertion"
            or not isinstance(item_dimensions, dict)
            or item_dimensions.get("standing") != "measured"
            or item_dimensions.get("source_provenance") != provenance
            or item_dimensions.get("responsibility") != MEASURED_ASSERTION_RESPONSIBILITY
            or item_dimensions.get("authority_warrant") != MEASUREMENT_AUTHORITY
            or item.get("support_basis") != support
            or item.get("unknowns") != list(MEASUREMENT_UNKNOWNS)
            or item.get("forbidden_inferences") != list(forbidden)
        ):
            raise EqualitySignatureRecurrenceError(
                f"{event.id} carries an incoherent measured Assertion shell"
            )

    require_shell(
        production_set,
        set_dimensions,
        "recorded exact equality-signature Assertion productions",
        {"assertion_refs": refs},
        PRODUCTION_SET_FORBIDDEN_INFERENCES,
    )
    set_id = _identity(
        result="exact_production_set", subject=subject, scope=scope, content=set_content
    )
    count_id = _identity(
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
        raise EqualitySignatureRecurrenceError(
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
        recurrence_id = _identity(
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
            raise EqualitySignatureRecurrenceError(
                f"{event.id} carries a noncanonical recurrence Assertion"
            )
        ordered.append(recurrence)
    return tuple(
        RecordedEqualitySignatureCountAssertion(
            assertion_id=item["dimensions"]["identity"],
            producing_event_id=event.id,
            result=item["result"],
            payload=item,
        )
        for item in ordered
    )


def get_recorded_equality_signature_count(
    ledger: EventLedger,
    *,
    producing_event_id: str,
    assertion_id: str,
) -> RecordedEqualitySignatureCountAssertion | None:
    """Resolve one result after proving its complete signature population."""

    event = ledger.get(producing_event_id)
    if event is None:
        return None
    if ledger.integrity_of(event.id) == CORRUPTED:
        raise EqualitySignatureRecurrenceError(
            "a corrupted Measurement occurrence cannot expose result Assertions"
        )
    recovered = assertions_of_recorded_equality_signature_count(event)
    production_set = next(item for item in recovered if item.result == "exact_production_set")
    payload = production_set.payload
    completeness_scope = payload["completeness_scope"]
    boundary = EventLedgerBoundary(payload["completeness_boundary"]["commitment"])
    measured_subject = payload["assertion_subject"]
    expected_refs = []
    try:
        for source in iter_recorded_equality_signatures(
            ledger,
            workspace_id=event.workspace_id,
            session_ids=completeness_scope["source_session_ids"],
            through=boundary,
        ):
            if source.assertion_id != measured_subject["measured_assertion_id"]:
                continue
            if (
                source.payload["assertion_subject"]
                != measured_subject["signature_subject"]
                or source.payload["dimensions"]["content"]
                != measured_subject["exact_equality_signature"]
                or source.payload["assertion_scope"] != payload["assertion_scope"]
            ):
                raise EqualitySignatureRecurrenceError(
                    "measured signature identity does not match its source Assertion"
                )
            expected_refs.append(source.reference)
    except EqualitySignatureMeasurementError as exc:
        raise EqualitySignatureRecurrenceError(str(exc)) from exc
    if expected_refs != payload["support_basis"]["assertion_refs"]:
        raise EqualitySignatureRecurrenceError(
            "the carried production set does not equal the complete bounded read"
        )
    for item in recovered:
        if item.assertion_id == assertion_id:
            return item
    return None
