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
    get_recorded_positional_result_distinction,
)
from seed_runtime.events import CORRUPTED, EventLedger, EventLedgerBoundary


class ComparisonResultMeasurementError(ValueError):
    """The bounded comparison-result Measurement could not be instantiated."""


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


def _validated_results(
    ledger: EventLedger, event: Any
) -> tuple[RecordedPositionalResultDistinction, ...]:
    """Recover one Compare once, including its ledger-backed replay."""

    results = assertions_of_recorded_positional_result_comparison(event)
    first = results[0]
    if (
        get_recorded_positional_result_distinction(
            ledger,
            producing_event_id=event.id,
            assertion_id=first.assertion_id,
        )
        is None
    ):
        raise AssertionComparisonError(
            "a recorded positional Compare result did not survive replay"
        )
    return results


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
    for session_id in sessions:
        for event in ledger.iter_session_kind(
            workspace_id,
            session_id,
            POSITIONAL_RESULT_COMPARISON_RECORDED_KIND,
            through=boundary,
        ):
            compared_any = True
            for result in _validated_results(ledger, event):
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
                    if representative is None:
                        raise AssertionComparisonError(
                            "a measured comparison result is no longer recoverable"
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
