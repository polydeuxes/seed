"""Bounded Compare over two productions of one canonical Assertion.

Canonical Assertion identity establishes the shared subject.  Distinct
producing Event identities establish that there are two production
occurrences.  Compare reports literal sameness and difference across carried
fidelity coordinates; it establishes no conflict, preference, truth, meaning,
or reason to revise either Assertion.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from typing import Any, Iterable

from seed_runtime.events import CORRUPTED, EventLedger
from seed_runtime.event import Event
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
    present: tuple[bool, bool]
    values: tuple[Any, Any]


@dataclass(frozen=True)
class AssertionProductionComparison:
    assertion_id: str
    inputs: tuple[AssertionProductionInput, AssertionProductionInput]
    distinctions: tuple[AssertionCoordinateDistinction, ...]
    act: str = "Compare"
    owner: str = "this bounded comparison occurrence"
    responsibility: str = (
        "preserve each input's carried fidelity coordinates and report literal "
        "sameness, difference, and absence only"
    )


ASSERTION_PRODUCTION_COMPARISON_RECORDED_KIND = (
    "operator.assertion.production_comparison_recorded"
)

COMPARISON_ASSERTION_FIDELITY_RESPONSIBILITY = (
    "preserve the fidelity of this compared Assertion's Standing to its "
    "carried coordinates"
)


@dataclass(frozen=True)
class RecordedAssertionProductionDistinction:
    """One addressable coordinate result inside its producing Compare occurrence."""

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


def _read(payload: dict[str, Any], path: tuple[str, ...]) -> tuple[bool, Any]:
    value: Any = payload
    for coordinate in path:
        if not isinstance(value, dict) or coordinate not in value:
            return False, None
        value = value[coordinate]
    return True, value


def _exactly_same(left: Any, right: Any) -> bool:
    return json.dumps(left, sort_keys=True, separators=(",", ":")) == json.dumps(
        right, sort_keys=True, separators=(",", ":")
    )


def _canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def _distinction_assertion_identity(
    *,
    compared_assertion_id: str,
    inputs: Iterable[dict[str, str]],
    workspace_id: str,
    session_id: str,
    coordinate: str,
    present: Iterable[bool],
    values: Iterable[Any],
    same: bool,
) -> str:
    identity = {
        "compared_assertion_id": compared_assertion_id,
        "inputs": list(inputs),
        "workspace_id": workspace_id,
        "session_id": session_id,
        "coordinate": coordinate,
        "present": list(present),
        "values": list(values),
        "same": same,
    }
    return "assertion-production-distinction:" + hashlib.sha256(
        _canonical_json(identity).encode("utf-8")
    ).hexdigest()


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
        read = tuple(_read(assertion.payload, path) for assertion in recovered)
        present = (read[0][0], read[1][0])
        values = (read[0][1], read[1][1])
        distinctions.append(
            AssertionCoordinateDistinction(
                coordinate=coordinate,
                same=present[0] == present[1] and _exactly_same(*values),
                present=present,
                values=values,
            )
        )
    return AssertionProductionComparison(
        assertion_id=refs[0]["assertion_id"],
        inputs=(inputs[0], inputs[1]),
        distinctions=tuple(distinctions),
    )


def record_assertion_production_comparison(
    ledger: EventLedger,
    *,
    workspace_id: str,
    session_id: str,
    comparison: AssertionProductionComparison,
) -> Event:
    """Preserve each literal Compare result without performing its Uptake."""

    input_refs = tuple(
        {
            "producing_event_id": item.producing_event_id,
            "assertion_id": item.assertion_id,
        }
        for item in comparison.inputs
    )
    verified = compare_assertion_productions(ledger, input_refs)
    if comparison != verified:
        raise AssertionComparisonError(
            "the supplied comparison does not match its occurrence-bound inputs"
        )
    assertions = []
    for distinction in comparison.distinctions:
        content = {
            "coordinate": distinction.coordinate,
            "present": list(distinction.present),
            "values": list(distinction.values),
            "same": distinction.same,
        }
        identity = _distinction_assertion_identity(
            compared_assertion_id=comparison.assertion_id,
            inputs=input_refs,
            workspace_id=workspace_id,
            session_id=session_id,
            **content,
        )
        assertions.append(
            {
                "dimensions": {
                    "identity": identity,
                    "content": content,
                    "standing": "compared",
                    "source_provenance": (
                        "the two exact occurrence-bound productions carried in "
                        "support_basis"
                    ),
                    "responsibility": COMPARISON_ASSERTION_FIDELITY_RESPONSIBILITY,
                    "authority_warrant": (
                        "literal comparison evidence only; establishes no conflict, "
                        "meaning, preference, revision, or strengthening"
                    ),
                    "scope_locality": "the exact assertion_scope carried here",
                    "occurrence_preservation": (
                        "distinct Compare result preserved by its producing occurrence"
                    ),
                },
                "subject_kind": "assertion",
                "responsibility_owner": "this recorded assertion",
                "result": "assertion_production_coordinate_distinction",
                "assertion_subject": {
                    "compared_assertion_id": comparison.assertion_id,
                    "coordinate": distinction.coordinate,
                },
                "assertion_scope": {
                    "workspace_id": workspace_id,
                    "session_id": session_id,
                    "compared_productions": list(input_refs),
                },
                "support_basis": {"assertion_refs": list(input_refs)},
                "unknowns": [
                    "whether a literal difference is Applicable to either input "
                    "Assertion remains Unknown",
                    "whether any consumer will admit or consume this result remains "
                    "Unknown",
                ],
                "forbidden_inferences": [
                    "literal difference is not conflict",
                    "new availability does not revise either compared Assertion",
                    "recording does not establish Applicability, admission, "
                    "consumption, or Uptake",
                ],
            }
        )
    return ledger.append(
        ASSERTION_PRODUCTION_COMPARISON_RECORDED_KIND,
        workspace_id,
        {
            "dimensions": {
                "identity": "assertion-production-comparison-occurrence",
                "content": f"{len(assertions)} distinct comparison Assertions recorded",
                "standing": "recorded",
                "source_provenance": "two occurrence-bound Assertion productions",
                "authority_warrant": "literal Compare results only",
                "scope_locality": f"workspace:{workspace_id};session:{session_id}",
                "occurrence_preservation": "comparison occurrence durably recorded",
            },
            "producing_act": "Compare",
            "owner": comparison.owner,
            "responsibility": comparison.responsibility,
            "inputs": list(input_refs),
            "assertions": assertions,
            "mutates_cluster": False,
        },
        session_id=session_id,
    )


def assertions_of_recorded_assertion_comparison(
    event: Event,
) -> tuple[RecordedAssertionProductionDistinction, ...]:
    """Recover and verify every addressable result of one recorded Compare."""

    if event.kind != ASSERTION_PRODUCTION_COMPARISON_RECORDED_KIND:
        raise AssertionComparisonError(
            f"{event.id} is {event.kind}, not an Assertion production Compare occurrence"
        )
    stated = event.payload.get("assertions")
    if not isinstance(stated, list):
        raise AssertionComparisonError(
            f"{event.id} does not preserve its distinct comparison Assertions"
        )
    recovered = []
    seen = set()
    for assertion in stated:
        dimensions = assertion.get("dimensions") if isinstance(assertion, dict) else None
        content = dimensions.get("content") if isinstance(dimensions, dict) else None
        identity = dimensions.get("identity") if isinstance(dimensions, dict) else None
        subject = assertion.get("assertion_subject") if isinstance(assertion, dict) else None
        scope = assertion.get("assertion_scope") if isinstance(assertion, dict) else None
        support = assertion.get("support_basis") if isinstance(assertion, dict) else None
        input_refs = support.get("assertion_refs") if isinstance(support, dict) else None
        if (
            assertion.get("subject_kind") != "assertion"
            or assertion.get("result") != "assertion_production_coordinate_distinction"
            or not isinstance(content, dict)
            or not isinstance(subject, dict)
            or not isinstance(scope, dict)
            or not isinstance(input_refs, list)
            or scope.get("compared_productions") != input_refs
            or not isinstance(scope.get("workspace_id"), str)
            or not isinstance(scope.get("session_id"), str)
            or subject.get("compared_assertion_id") is None
            or subject.get("coordinate") != content.get("coordinate")
        ):
            raise AssertionComparisonError(
                f"{event.id} carries an incoherent comparison Assertion"
            )
        required_content = {"coordinate", "present", "values", "same"}
        if set(content) != required_content:
            raise AssertionComparisonError(
                f"{event.id} carries an incomplete comparison result"
            )
        canonical = _distinction_assertion_identity(
            compared_assertion_id=subject["compared_assertion_id"],
            inputs=input_refs,
            workspace_id=scope.get("workspace_id"),
            session_id=scope.get("session_id"),
            coordinate=content["coordinate"],
            present=content["present"],
            values=content["values"],
            same=content["same"],
        )
        if identity != canonical or identity in seen:
            raise AssertionComparisonError(
                f"{event.id} carries a comparison Assertion with invalid identity"
            )
        seen.add(identity)
        recovered.append(
            RecordedAssertionProductionDistinction(
                assertion_id=identity,
                producing_event_id=event.id,
                coordinate=content["coordinate"],
                payload=assertion,
            )
        )
    return tuple(recovered)
