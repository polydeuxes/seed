"""Literal counts over recorded positional-result Compare Assertions.

The subject is Seed's own recorded Compare output.  For every exact positional
subject and comparison coordinate, this Measurement counts every exact carried
result.  It does not reduce results to same/different, rank them, or infer
similarity, recurrence, relation, or meaning.
"""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
import json
from typing import Any, Iterable

from seed_runtime.assertion_comparison import (
    POSITIONAL_RESULT_COMPARISON_RECORDED_KIND,
    AssertionComparisonError,
    RecordedPositionalResultDistinction,
    assertions_of_recorded_positional_result_comparison,
    get_recorded_positional_result_distinction,
)
from seed_runtime.events import EventLedger, EventLedgerBoundary


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


def measure_comparison_result_counts(
    ledger: EventLedger,
    *,
    workspace_id: str,
    source_session_ids: Iterable[str],
) -> list[MeasuredComparisonResultCount]:
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

    grouped: dict[
        tuple[str, str, str],
        tuple[dict[str, Any], str, dict[str, Any], list[dict[str, str]]],
    ] = {}
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
                key = (_canonical(subject), result.coordinate, _canonical(content))
                if key not in grouped:
                    grouped[key] = (
                        deepcopy(subject),
                        result.coordinate,
                        deepcopy(content),
                        [],
                    )
                grouped[key][3].append(result.reference)

    if not compared_any:
        raise ComparisonResultMeasurementError(
            "no recorded positional-result Compare occurrences to measure"
        )

    findings = [
        MeasuredComparisonResultCount(
            compared_subject=subject,
            coordinate=coordinate,
            result_content=content,
            production_refs=tuple(refs),
            workspace_id=workspace_id,
            source_session_ids=sessions,
            completeness_boundary=boundary,
        )
        for subject, coordinate, content, refs in grouped.values()
    ]
    findings.sort(
        key=lambda item: (
            _canonical(item.compared_subject),
            item.coordinate,
            _canonical(item.result_content),
        )
    )
    return findings
