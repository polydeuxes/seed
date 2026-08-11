"""Literal counts over recorded positional-result Compare Assertions.

The subject is Seed's own recorded Compare output.  For every exact positional
subject and comparison coordinate, this Measurement counts every exact carried
result.  It does not reduce results to same/different, rank them, or infer
similarity, recurrence, relation, or meaning.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from typing import Any, Iterable, Iterator

from seed_runtime.assertion_comparison import (
    POSITIONAL_RESULT_COMPARISON_RECORDED_KIND,
    AssertionComparisonError,
    RecordedPositionalResultDistinction,
    assertions_of_recorded_positional_result_comparison,
    iter_recorded_positional_result_distinctions,
)
from seed_runtime.events import CORRUPTED, EventLedger, EventLedgerBoundary
from seed_runtime.event import Event
from seed_runtime.ids import new_id


class ComparisonResultMeasurementError(ValueError):
    """The bounded comparison-result Measurement could not be instantiated."""


COMPARISON_RESULT_COUNT_RECORDED_KIND = (
    "operator.measurement.comparison_result_count_recorded"
)
MEASURED_ASSERTION_RESPONSIBILITY = (
    "preserve the fidelity of this measured Assertion's Standing to its "
    "carried coordinates"
)
MEASUREMENT_AUTHORITY = (
    "literal Measurement evidence only; establishes no recurrence, profile, "
    "similarity, relation, meaning, or Standing movement"
)


@dataclass(frozen=True)
class MeasuredComparisonResultCount:
    """One exact carried Compare result and its exact production set."""

    compared_subject: dict[str, Any]
    coordinate: str
    result_content: dict[str, Any]
    production_refs: tuple[dict[str, str], ...]
    workspace_id: str
    source_session_ids: tuple[str, ...]
    completeness_boundary: EventLedgerBoundary

    @property
    def count(self) -> int:
        return len(self.production_refs)


def _canonical(value: Any) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def _digest(value: Any) -> str:
    """Locate candidate equal results; the digest never establishes equality."""

    return hashlib.sha256(_canonical(value).encode("utf-8")).hexdigest()


@dataclass
class _CompactResultGroup:
    """One validated representative and compact occurrence-bound references."""

    representative: tuple[str, str]
    production_refs: list[tuple[str, str]]


def _rehydrate_validated_reference(
    ledger: EventLedger, reference: tuple[str, str]
) -> RecordedPositionalResultDistinction:
    """Recover a result already fully validated in this frozen invocation."""

    producing_event_id, assertion_id = reference
    event = ledger.get(producing_event_id)
    if event is None:
        raise AssertionComparisonError(
            "a measured comparison result is no longer recoverable"
        )
    if ledger.integrity_of(producing_event_id) == CORRUPTED:
        raise AssertionComparisonError(
            "a measured comparison result became detectably corrupted"
        )
    for result in assertions_of_recorded_positional_result_comparison(event):
        if result.assertion_id == assertion_id:
            return result
    raise AssertionComparisonError(
        "a measured comparison result reference changed during Measurement"
    )


def measure_comparison_result_counts(
    ledger: EventLedger,
    *,
    workspace_id: str,
    source_session_ids: Iterable[str],
) -> Iterator[MeasuredComparisonResultCount]:
    """Count every exact carried result in one declared bounded population.

    Exact content is the complete ``{coordinate, present, values, same}``
    result.  In particular, two different distinctions are not collapsed merely
    because both carry ``same=False``.
    """

    sessions = tuple(dict.fromkeys(source_session_ids))
    if not sessions or any(not isinstance(value, str) or not value for value in sessions):
        raise ComparisonResultMeasurementError(
            "comparison-result Measurement requires exact declared source sessions"
        )
    boundary = ledger.capture_boundary()
    missing = [
        session_id
        for session_id in sessions
        if not ledger.has_session(workspace_id, session_id, through=boundary)
    ]
    if missing:
        raise ComparisonResultMeasurementError(
            "declared source sessions are absent through the Measurement boundary: "
            + ", ".join(missing)
        )

    # A digest only locates candidate buckets.  Each candidate match below is
    # rehydrated and compared exactly before its compact reference joins a
    # group.  Thus hash equality is never promoted into the Measurement rule.
    grouped: dict[str, list[_CompactResultGroup]] = {}
    compared_any = False
    for result in iter_recorded_positional_result_distinctions(
        ledger,
        workspace_id=workspace_id,
        session_ids=sessions,
        through=boundary,
    ):
        compared_any = True
        payload = result.payload
        subject = payload["assertion_subject"]["compared_subject"]
        content = payload["dimensions"]["content"]
        exact_result = {
            "compared_subject": subject,
            "coordinate": result.coordinate,
            "content": content,
        }
        digest = _digest(exact_result)
        candidates = grouped.setdefault(digest, [])
        matched = None
        for candidate in candidates:
            representative = _rehydrate_validated_reference(
                ledger, candidate.representative
            )
            representative_exact_result = {
                "compared_subject": representative.payload["assertion_subject"][
                    "compared_subject"
                ],
                "coordinate": representative.coordinate,
                "content": representative.payload["dimensions"]["content"],
            }
            if representative_exact_result == exact_result:
                matched = candidate
                break
        reference = (result.producing_event_id, result.assertion_id)
        if matched is None:
            candidates.append(
                _CompactResultGroup(
                    representative=reference,
                    production_refs=[reference],
                )
            )
        else:
            matched.production_refs.append(reference)

    if not compared_any:
        raise ComparisonResultMeasurementError(
            "no recorded positional-result Compare occurrences to measure"
        )

    # Rehydrate only the representative of the exact result being yielded.
    # Callers may stream the findings; this function never constructs a global
    # collection of full result payloads at its output boundary.
    for candidates in grouped.values():
        for group in candidates:
            representative = _rehydrate_validated_reference(
                ledger, group.representative
            )
            payload = representative.payload
            yield MeasuredComparisonResultCount(
                compared_subject=payload["assertion_subject"]["compared_subject"],
                coordinate=representative.coordinate,
                result_content=payload["dimensions"]["content"],
                production_refs=tuple(
                    {
                        "producing_event_id": producing_event_id,
                        "assertion_id": assertion_id,
                    }
                    for producing_event_id, assertion_id in group.production_refs
                ),
                workspace_id=workspace_id,
                source_session_ids=sessions,
                completeness_boundary=boundary,
            )


def _assertion_identity(
    *,
    result: str,
    subject: dict[str, Any],
    scope: dict[str, Any],
    content: dict[str, Any],
) -> str:
    identified = {
        "result": result,
        "subject": subject,
        "scope": scope,
        "content": content,
    }
    return "comparison-result-measurement:" + hashlib.sha256(
        _canonical(identified).encode("utf-8")
    ).hexdigest()


def assertions_from_comparison_result_count(
    finding: MeasuredComparisonResultCount,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """The exact production set and the count derived from that set."""

    subject = {
        "compared_subject": finding.compared_subject,
        "coordinate": finding.coordinate,
        "exact_comparison_result": finding.result_content,
    }
    scope = {
        "workspace_id": finding.workspace_id,
        "source_session_ids": list(finding.source_session_ids),
    }
    set_content = {"production_refs": list(finding.production_refs)}
    production_set_id = _assertion_identity(
        result="exact_production_set",
        subject=subject,
        scope=scope,
        content=set_content,
    )
    production_set = {
        "dimensions": {
            "identity": production_set_id,
            "content": set_content,
            "standing": "measured",
            "source_provenance": (
                "recorded positional-result comparison Assertion productions"
            ),
            "responsibility": MEASURED_ASSERTION_RESPONSIBILITY,
            "authority_warrant": MEASUREMENT_AUTHORITY,
        },
        "subject_kind": "assertion",
        "responsibility_owner": "this recorded assertion",
        "result": "exact_production_set",
        "assertion_subject": subject,
        "assertion_scope": scope,
        "support_basis": {"assertion_refs": list(finding.production_refs)},
        "completeness_boundary": {
            "commitment": finding.completeness_boundary.commitment
        },
        "completeness_scope": {
            "workspace_id": finding.workspace_id,
            "source_session_ids": list(finding.source_session_ids),
            "occurrence_kind": POSITIONAL_RESULT_COMPARISON_RECORDED_KIND,
        },
        "unknowns": [
            "why this exact comparison result has this count remains Unknown"
        ],
        "forbidden_inferences": [
            "an exact production count is not recurrence, similarity, relation, "
            "meaning, profile membership, or Standing strength"
        ],
    }
    count_content = {"production_count": finding.count}
    count_id = _assertion_identity(
        result="count",
        subject=subject,
        scope=scope,
        content=count_content,
    )
    count = {
        "dimensions": {
            "identity": count_id,
            "content": count_content,
            "standing": "measured",
            "source_provenance": "the exact production-set Assertion carried here",
            "responsibility": MEASURED_ASSERTION_RESPONSIBILITY,
            "authority_warrant": MEASUREMENT_AUTHORITY,
        },
        "subject_kind": "assertion",
        "responsibility_owner": "this recorded assertion",
        "result": "count",
        "assertion_subject": subject,
        "assertion_scope": scope,
        "support_basis": {"local_assertion_ids": [production_set_id]},
        "unknowns": [
            "why this exact comparison result has this count remains Unknown"
        ],
        "forbidden_inferences": [
            "count greater than one does not by itself establish recurrence, "
            "similarity, relation, meaning, profile membership, or Standing strength"
        ],
    }
    return production_set, count


def _comparison_result_count_event(
    *,
    workspace_id: str,
    session_id: str,
    finding: MeasuredComparisonResultCount,
) -> Event:
    if workspace_id != finding.workspace_id:
        raise ComparisonResultMeasurementError(
            "recording workspace must equal the Measurement workspace"
        )
    assertions = assertions_from_comparison_result_count(finding)
    return Event(
        id=new_id("evt"),
        kind=COMPARISON_RESULT_COUNT_RECORDED_KIND,
        workspace_id=workspace_id,
        session_id=session_id,
        payload={
            "dimensions": {
                "identity": "comparison-result-count-measurement-occurrence",
                "content": "two distinct measured Assertions recorded",
                "standing": "recorded",
                "source_provenance": (
                    "recorded positional-result comparison Assertions"
                ),
                "authority_warrant": MEASUREMENT_AUTHORITY,
            },
            "producing_act": "declared Measurement",
            "producer": "this Seed",
            "measurement_subject": "recorded positional-result comparison Assertions",
            "assertions": list(assertions),
        },
    )


def record_comparison_result_count(
    ledger: EventLedger,
    *,
    workspace_id: str,
    session_id: str,
    finding: MeasuredComparisonResultCount,
) -> Event:
    """Record one exact production-set Assertion and its derived count."""

    return ledger.append_many(
        [
            _comparison_result_count_event(
            workspace_id=workspace_id,
            session_id=session_id,
            finding=finding,
            )
        ]
    )[0]


def record_comparison_result_count_layer(
    ledger: EventLedger,
    *,
    workspace_id: str,
    source_session_ids: Iterable[str],
    recording_session_id: str,
) -> int:
    """Measure and record every exact result; batching is persistence-only."""

    if not isinstance(recording_session_id, str) or not recording_session_id:
        raise ComparisonResultMeasurementError(
            "comparison-result recording requires an exact session"
        )
    pending = []
    recorded = 0
    for finding in measure_comparison_result_counts(
        ledger,
        workspace_id=workspace_id,
        source_session_ids=source_session_ids,
    ):
        pending.append(
            _comparison_result_count_event(
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
