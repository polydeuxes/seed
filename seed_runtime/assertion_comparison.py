"""Bounded Compare over two yields of one canonical Assertion.

Canonical Assertion identity establishes the shared subject.  Distinct
yielding Event identities establish that there are two yield
occurrences.  Compare reports literal sameness and difference across carried
Standing coordinates; it establishes no conflict, preference, truth, represented relation,
or reason to revise either Assertion.
"""

from __future__ import annotations


from dataclasses import dataclass
import hashlib
import json
from typing import Any, Iterable

from seed_runtime.events import CORRUPTED, EventLedger
from seed_runtime.event import Event
from seed_runtime.ids import new_id
from seed_runtime.support_basis import SupportValidator
from seed_runtime.yield_evidence import _record_yield_evidence, yield_commitment
from seed_runtime.recurrence_measurement import (
    RecordedMeasuredAssertion,
    get_recorded_measured_assertion,
)


class AssertionComparisonError(ValueError):
    """The bounded Assertion comparison could not be instantiated."""


@dataclass(frozen=True)
class AssertionYieldInput:
    assertion_id: str
    yielding_event_id: str
    integrity: str


@dataclass(frozen=True)
class AssertionCoordinateDistinction:
    coordinate: str
    same: bool
    present: tuple[bool, bool]
    values: tuple[Any, Any]


@dataclass(frozen=True)
class AssertionYieldComparison:
    assertion_id: str
    inputs: tuple[AssertionYieldInput, AssertionYieldInput]
    distinctions: tuple[AssertionCoordinateDistinction, ...]
    act: str = "Compare"
    responsible_boundary: str = "this bounded comparison occurrence"
    responsibility: str = (
        "preserve each input's carried Standing coordinates and report literal "
        "sameness, difference, and absence only"
    )



ASSERTION_YIELD_COMPARISON_RECORDED_KIND = (
    "operator.assertion.yield_comparison_recorded"
)
ASSERTION_COMPARE_INPUT_LOCALITY_EVIDENCE_KIND = (
    "operator.assertion.compare_input_locality_evidenced"
)
ASSERTION_COMPARE_INPUT_APPLICABILITY_KIND = (
    "operator.assertion.compare_input_applicability_recorded"
)
ASSERTION_COMPARE_ACT_EVIDENCE_KIND = (
    "operator.assertion.compare_act_evidenced"
)
ASSERTION_YIELD_COMPARISON_CONVENTION = "assertion_yield_comparison"
ASSERTION_YIELD_COMPARISON_RESULT_KIND = "Assertion Yield Compare result"
EVENT_KIND_RESPONSIBILITIES = {
    ASSERTION_YIELD_COMPARISON_RECORDED_KIND: "02.Acts.A",
    ASSERTION_COMPARE_INPUT_LOCALITY_EVIDENCE_KIND: "06.Standing.B",
    ASSERTION_COMPARE_INPUT_APPLICABILITY_KIND: "01.Standing.E.1",
    ASSERTION_COMPARE_ACT_EVIDENCE_KIND: "02.Acts.A",
}

COMPARISON_ASSERTION_STANDING_COORDINATE_RESPONSIBILITY = (
    "preserve this comparison Assertion's carried Standing coordinates"
)


@dataclass(frozen=True)
class RecordedAssertionYieldDistinction:
    """One addressable coordinate result inside its yielding Compare occurrence."""

    assertion_id: str
    yielding_event_id: str
    coordinate: str
    payload: dict[str, Any]

    @property
    def reference(self) -> dict[str, str]:
        return {
            "yielding_event_id": self.yielding_event_id,
            "assertion_id": self.assertion_id,
        }




COORDINATES: dict[str, tuple[str, ...]] = {
    "standing": ("dimensions", "standing"),
    "source_provenance": ("dimensions", "source_provenance"),
    "responsibility": ("dimensions", "responsibility"),
    "authority": ("dimensions", "authority"),
    "scope": ("assertion_scope",),
    "support_basis": ("support_basis",),
    "completeness_boundary": ("completeness_boundary",),
    "completeness_scope": ("completeness_scope",),
    "unknowns": ("unknowns",),
    "limits": ("limits",),
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
    locality_id: str,
    coordinate: str,
    present: Iterable[bool],
    values: Iterable[Any],
    same: bool,
) -> str:
    identity = {
        "compared_assertion_id": compared_assertion_id,
        "inputs": list(inputs),
        "locality_id": locality_id,
        "coordinate": coordinate,
        "present": list(present),
        "values": list(values),
        "same": same,
    }
    return "assertion-yield-distinction:" + hashlib.sha256(
        _canonical_json(identity).encode("utf-8")
    ).hexdigest()




def compare_assertion_yields(
    ledger: EventLedger, references: Iterable[dict[str, str]]
) -> AssertionYieldComparison:
    """Compare two exact yields of the same canonical Assertion."""

    exact_references = tuple(references)
    if len(exact_references) != 2:
        raise AssertionComparisonError(
            "Assertion yield Compare has as input exactly two inputs; "
            f"{len(exact_references)} supplied"
        )
    required = {"yielding_event_id", "assertion_id"}
    if any(set(reference) != required for reference in exact_references):
        raise AssertionComparisonError(
            "each input must be one exact yielding-event and Assertion identity pair"
        )
    if (
        exact_references[0] == exact_references[1]
        or exact_references[0]["yielding_event_id"]
        == exact_references[1]["yielding_event_id"]
    ):
        raise AssertionComparisonError(
            "one yielding occurrence cannot be compared with itself"
        )
    if exact_references[0]["assertion_id"] != exact_references[1]["assertion_id"]:
        raise AssertionComparisonError(
            "Assertion yield Compare requires one canonical Assertion identity"
        )

    assertions: list[RecordedMeasuredAssertion] = []
    inputs = []
    for reference in exact_references:
        assertion = get_recorded_measured_assertion(
            ledger,
            yielding_event_id=reference["yielding_event_id"],
            assertion_id=reference["assertion_id"],
        )
        if assertion is None:
            raise AssertionComparisonError(
                "an Assertion reference does not resolve to its yielding occurrence"
            )
        integrity = ledger.integrity_of(assertion.yielding_event_id)
        if integrity == CORRUPTED:
            raise AssertionComparisonError(
                "a corrupted yielding occurrence cannot participate in Compare"
            )
        assertions.append(assertion)
        inputs.append(
            AssertionYieldInput(
                assertion_id=assertion.assertion_id,
                yielding_event_id=assertion.yielding_event_id,
                integrity=integrity,
            )
        )

    distinctions = []
    for coordinate, path in COORDINATES.items():
        coordinate_reads = tuple(
            _read(assertion.payload, path) for assertion in assertions
        )
        present = (coordinate_reads[0][0], coordinate_reads[1][0])
        values = (coordinate_reads[0][1], coordinate_reads[1][1])
        distinctions.append(
            AssertionCoordinateDistinction(
                coordinate=coordinate,
                same=present[0] == present[1] and _exactly_same(*values),
                present=present,
                values=values,
            )
        )
    return AssertionYieldComparison(
        assertion_id=exact_references[0]["assertion_id"],
        inputs=(inputs[0], inputs[1]),
        distinctions=tuple(distinctions),
    )




def record_assertion_yield_comparison(
    ledger: EventLedger,
    *,
    locality_id: str,
    comparison: AssertionYieldComparison,
) -> Event:
    """Preserve each literal Compare result without establishing later input support."""

    input_references = tuple(
        {
            "yielding_event_id": item.yielding_event_id,
            "assertion_id": item.assertion_id,
        }
        for item in comparison.inputs
    )
    verified = compare_assertion_yields(ledger, input_references)
    if comparison != verified:
        raise AssertionComparisonError(
            "the supplied comparison does not match its occurrence-bound inputs"
        )
    act_id = new_id("assertion_compare_act")
    act_occurrence_id = new_id("assertion_compare_act_occurrence")
    result_identity = new_id("assertion_compare_result")
    locality_evidence_ids = []
    applicability_event_ids = []
    participation = []
    for input_reference in input_references:
        role = "compared Assertion"
        locality_evidence = ledger.append(
            ASSERTION_COMPARE_INPUT_LOCALITY_EVIDENCE_KIND,
            {
                "first_subject": input_reference,
                "second_subject": {
                    "downstream_act_id": act_id,
                    "act_occurrence_id": act_occurrence_id,
                    "role": role,
                },
                "authority": "unestablished",
                "evidence_scope": "this exact Assertion-to-Compare Locality only",
            },
            locality_id=locality_id,
        )
        applicability = ledger.append(
            ASSERTION_COMPARE_INPUT_APPLICABILITY_KIND,
            {
                "input_reference": input_reference,
                "downstream_act_id": act_id,
                "role": role,
                "locality_evidence_id": locality_evidence.id,
                "standing": "applicable",
                "authority": "unestablished",
                "evidence_scope": "this exact input-to-Compare relation only",
            },
            locality_id=locality_id,
        )
        locality_evidence_ids.append(locality_evidence.id)
        applicability_event_ids.append(applicability.id)
        participation.append(
            {
                "subject_reference": input_reference,
                "role": role,
                "act_occurrence_id": act_occurrence_id,
                "applicability_event_id": applicability.id,
            }
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
            inputs=input_references,
            locality_id=locality_id,
            **content,
        )
        assertions.append(
            {
                "dimensions": {
                    "identity": identity,
                    "content": content,
                    "standing": "compared",
                    "source_provenance": (
                        "the two exact occurrence-bound yields carried in "
                        "support_basis"
                    ),
                    "responsibility": COMPARISON_ASSERTION_STANDING_COORDINATE_RESPONSIBILITY,
                    "authority": "unestablished",
                    "evidence_scope": (
                        "literal comparison evidence only; establishes no conflict, "
                        "represented relation, preference, revision, or strengthening"
                    ),
                    "scope_locality": "the exact assertion_scope carried here",
                    "occurrence_preservation": (
                        "distinct Compare result preserved by its yielding occurrence"
                    ),
                },
                "subject_kind": "assertion",
                "responsible_boundary": "this recorded assertion",
                "result": "assertion_yield_coordinate_distinction",
                "assertion_subject": {
                    "compared_assertion_id": comparison.assertion_id,
                    "coordinate": distinction.coordinate,
                },
                "assertion_scope": {
                    "locality_id": locality_id,
                    "compared_yields": list(input_references),
                },
                "support_basis": {"assertion_references": list(input_references)},
                "unknowns": [
                    "whether a literal difference is Applicable to either input "
                    "Assertion remains Unknown",
                    "whether any exact Act will admit or have as input this result remains "
                    "Unknown",
                ],
                "limits": [
                    "literal difference is not conflict",
                    "new availability does not revise either compared Assertion",
                    "recording does not establish Applicability, admission, "
                    "participation, or input support",
                ],
            }
        )
    result_payload = {
        "result_identity": result_identity,
        "dimensions": {
            "identity": result_identity,
            "content": f"{len(assertions)} distinct comparison Assertions recorded",
            "source_provenance": "two occurrence-bound Assertion yields",
            "authority": "unestablished",
            "evidence_scope": "literal Compare results only",
            "scope_locality": f"locality:{locality_id}",
            "occurrence_preservation": "comparison occurrence durably recorded",
        },
        "yielding_act": "Compare",
        "downstream_act_id": act_id,
        "act_occurrence_id": act_occurrence_id,
        "input_locality_evidence_ids": locality_evidence_ids,
        "input_applicability_event_ids": applicability_event_ids,
        "participation": participation,
        "responsible_boundary": comparison.responsible_boundary,
        "responsibility": comparison.responsibility,
        "inputs": list(input_references),
        "assertions": assertions,
    }
    act_evidence = ledger.append(
        ASSERTION_COMPARE_ACT_EVIDENCE_KIND,
        {
            "downstream_act_id": act_id,
            "act_occurrence_id": act_occurrence_id,
            "act": "Compare",
            "responsibility": comparison.responsibility,
            "responsible_boundary": comparison.responsible_boundary,
            "input_applicability_event_ids": applicability_event_ids,
            "participation": participation,
            "result_commitment": yield_commitment(
                ASSERTION_YIELD_COMPARISON_CONVENTION, result_payload
            ),
            "authority": "unestablished",
            "evidence_scope": "this exact bounded Compare occurrence only",
        },
        locality_id=locality_id,
    )
    yield_evidence = _record_yield_evidence(
        ledger,
        locality_id=locality_id,
        convention=ASSERTION_YIELD_COMPARISON_CONVENTION,
        yielding_act="Compare",
        act_occurrence_id=act_occurrence_id,
        yielded_result_kind=ASSERTION_YIELD_COMPARISON_RESULT_KIND,
        result_identity=result_identity,
        yielded_content=result_payload,
        responsibility=comparison.responsibility,
        live_boundary="assertion_yield_compare",
        responsible_boundary=comparison.responsible_boundary,
        recorded_result_coordinates={key: (key,) for key in result_payload},
    )
    return ledger.append(
        ASSERTION_YIELD_COMPARISON_RECORDED_KIND,
        {
            **result_payload,
            "responsible_act_evidence_id": act_evidence.id,
            "yield_evidence_id": yield_evidence.id,
        },
        locality_id=locality_id,
    )


def assertions_of_recorded_assertion_comparison(
    event: Event,
) -> tuple[RecordedAssertionYieldDistinction, ...]:
    """Read and verify every addressable result of one recorded Compare."""

    if event.kind != ASSERTION_YIELD_COMPARISON_RECORDED_KIND:
        raise AssertionComparisonError(
            f"{event.id} is {event.kind}, not an Assertion yield Compare occurrence"
        )
    stated = event.payload.get("assertions")
    outer_inputs = event.payload.get("inputs")
    if not isinstance(stated, list):
        raise AssertionComparisonError(
            f"{event.id} does not preserve its distinct comparison Assertions"
        )
    required_reference = {"yielding_event_id", "assertion_id"}
    if (
        not isinstance(outer_inputs, list)
        or len(outer_inputs) != 2
        or any(
            not isinstance(reference, dict)
            or set(reference) != required_reference
            or not all(isinstance(value, str) and value for value in reference.values())
            for reference in outer_inputs
        )
        or outer_inputs[0]["yielding_event_id"]
        == outer_inputs[1]["yielding_event_id"]
        or outer_inputs[0]["assertion_id"] != outer_inputs[1]["assertion_id"]
    ):
        raise AssertionComparisonError(
            f"{event.id} does not carry two distinct yields of one Assertion"
        )
    act_occurrence_id = event.payload.get("act_occurrence_id")
    locality_ids = event.payload.get("input_locality_evidence_ids")
    applicability_ids = event.payload.get("input_applicability_event_ids")
    participation = event.payload.get("participation")
    if (
        not isinstance(act_occurrence_id, str)
        or not act_occurrence_id
        or not isinstance(locality_ids, list)
        or len(locality_ids) != len(outer_inputs)
        or len(set(locality_ids)) != len(locality_ids)
        or not all(isinstance(value, str) and value for value in locality_ids)
        or not isinstance(applicability_ids, list)
        or len(applicability_ids) != len(outer_inputs)
        or len(set(applicability_ids)) != len(applicability_ids)
        or not all(isinstance(value, str) and value for value in applicability_ids)
        or participation
        != [
            {
                "subject_reference": input_reference,
                "role": "compared Assertion",
                "act_occurrence_id": act_occurrence_id,
                "applicability_event_id": applicability_id,
            }
            for input_reference, applicability_id in zip(
                outer_inputs, applicability_ids
            )
        ]
    ):
        raise AssertionComparisonError(
            f"{event.id} does not preserve exact input Locality, Applicability, "
            "and Participation for its Compare occurrence"
        )
    if len(stated) != len(COORDINATES):
        raise AssertionComparisonError(
            f"{event.id} does not carry every distinct Compare result"
        )
    read = []
    seen = set()
    seen_coordinates = set()
    for assertion in stated:
        dimensions = assertion.get("dimensions") if isinstance(assertion, dict) else None
        content = dimensions.get("content") if isinstance(dimensions, dict) else None
        identity = dimensions.get("identity") if isinstance(dimensions, dict) else None
        subject = assertion.get("assertion_subject") if isinstance(assertion, dict) else None
        scope = assertion.get("assertion_scope") if isinstance(assertion, dict) else None
        support = assertion.get("support_basis") if isinstance(assertion, dict) else None
        input_references = support.get("assertion_references") if isinstance(support, dict) else None
        if (
            assertion.get("subject_kind") != "assertion"
            or assertion.get("result") != "assertion_yield_coordinate_distinction"
            or not isinstance(content, dict)
            or not isinstance(subject, dict)
            or not isinstance(scope, dict)
            or not isinstance(input_references, list)
            or input_references != outer_inputs
            or scope.get("compared_yields") != input_references
            or not isinstance(scope.get("locality_id"), str)
            or scope.get("locality_id") != event.locality_id
            or subject.get("compared_assertion_id")
            != outer_inputs[0]["assertion_id"]
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
        coordinate = content["coordinate"]
        present = content["present"]
        values = content["values"]
        same = content["same"]
        if (
            coordinate not in COORDINATES
            or coordinate in seen_coordinates
            or not isinstance(present, list)
            or len(present) != 2
            or not all(isinstance(value, bool) for value in present)
            or not isinstance(values, list)
            or len(values) != 2
            or not isinstance(same, bool)
            or same
            != (present[0] == present[1] and _exactly_same(values[0], values[1]))
        ):
            raise AssertionComparisonError(
                f"{event.id} carries a result outside the Compare output contract"
            )
        seen_coordinates.add(coordinate)
        canonical = _distinction_assertion_identity(
            compared_assertion_id=subject["compared_assertion_id"],
            inputs=input_references,
            locality_id=scope.get("locality_id"),
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
        read.append(
            RecordedAssertionYieldDistinction(
                assertion_id=identity,
                yielding_event_id=event.id,
                coordinate=content["coordinate"],
                payload=assertion,
            )
        )
    if seen_coordinates != set(COORDINATES):
        raise AssertionComparisonError(
            f"{event.id} does not carry the exact Compare coordinate set"
        )
    return tuple(read)
