"""Bounded Compare over two productions of one canonical Assertion.

Canonical Assertion identity establishes the shared subject.  Distinct
producing Event identities establish that there are two production
occurrences.  Compare reports literal sameness and difference across carried
fidelity coordinates; it establishes no conflict, preference, truth, meaning,
or reason to revise either Assertion.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Any, Iterable

from seed_runtime.events import CORRUPTED, EventLedger
from seed_runtime.recurrence_measurement import (
    RecordedMeasuredAssertion,
    get_recorded_measured_assertion,
)


class AssertionComparisonError(ValueError):
    """The bounded Assertion comparison could not be instantiated."""


@dataclass(frozen=True)
class AssertionProductionInput:
    assertion_id: str
    producing_event_id: str
    integrity: str


@dataclass(frozen=True)
class AssertionCoordinateDistinction:
    coordinate: str
    same: bool
    values: tuple[Any, Any]


@dataclass(frozen=True)
class AssertionProductionComparison:
    assertion_id: str
    inputs: tuple[AssertionProductionInput, AssertionProductionInput]
    distinctions: tuple[AssertionCoordinateDistinction, ...]


COORDINATES: dict[str, tuple[str, ...]] = {
    "standing": ("dimensions", "standing"),
    "source_provenance": ("dimensions", "source_provenance"),
    "responsibility": ("dimensions", "responsibility"),
    "authority_warrant": ("dimensions", "authority_warrant"),
    "scope": ("assertion_scope",),
    "support_basis": ("support_basis",),
    "completeness_boundary": ("completeness_boundary",),
    "completeness_scope": ("completeness_scope",),
    "unknowns": ("unknowns",),
    "forbidden_inferences": ("forbidden_inferences",),
}


def _read(payload: dict[str, Any], path: tuple[str, ...]) -> Any:
    value: Any = payload
    for coordinate in path:
        if not isinstance(value, dict) or coordinate not in value:
            return None
        value = value[coordinate]
    return value


def _exactly_same(left: Any, right: Any) -> bool:
    return json.dumps(left, sort_keys=True, separators=(",", ":")) == json.dumps(
        right, sort_keys=True, separators=(",", ":")
    )


def compare_assertion_productions(
    ledger: EventLedger, references: Iterable[dict[str, str]]
) -> AssertionProductionComparison:
    """Compare two exact productions of the same canonical Assertion."""

    refs = tuple(references)
    if len(refs) != 2:
        raise AssertionComparisonError(
            f"Assertion production Compare consumes exactly two inputs; {len(refs)} supplied"
        )
    required = {"producing_event_id", "assertion_id"}
    if any(set(reference) != required for reference in refs):
        raise AssertionComparisonError(
            "each input must be one exact producing-event and Assertion identity pair"
        )
    if refs[0] == refs[1] or refs[0]["producing_event_id"] == refs[1]["producing_event_id"]:
        raise AssertionComparisonError(
            "one producing occurrence cannot be compared with itself"
        )
    if refs[0]["assertion_id"] != refs[1]["assertion_id"]:
        raise AssertionComparisonError(
            "Assertion production Compare requires one canonical Assertion identity"
        )

    recovered: list[RecordedMeasuredAssertion] = []
    inputs = []
    for reference in refs:
        assertion = get_recorded_measured_assertion(
            ledger,
            producing_event_id=reference["producing_event_id"],
            assertion_id=reference["assertion_id"],
        )
        if assertion is None:
            raise AssertionComparisonError(
                "an Assertion reference does not resolve to its producing occurrence"
            )
        integrity = ledger.integrity_of(assertion.producing_event_id)
        if integrity == CORRUPTED:
            raise AssertionComparisonError(
                "a corrupted producing occurrence cannot participate in Compare"
            )
        recovered.append(assertion)
        inputs.append(
            AssertionProductionInput(
                assertion_id=assertion.assertion_id,
                producing_event_id=assertion.producing_event_id,
                integrity=integrity,
            )
        )

    distinctions = []
    for coordinate, path in COORDINATES.items():
        values = tuple(_read(assertion.payload, path) for assertion in recovered)
        distinctions.append(
            AssertionCoordinateDistinction(
                coordinate=coordinate,
                same=_exactly_same(*values),
                values=values,
            )
        )
    return AssertionProductionComparison(
        assertion_id=refs[0]["assertion_id"],
        inputs=(inputs[0], inputs[1]),
        distinctions=tuple(distinctions),
    )
