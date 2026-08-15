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
from seed_runtime.identities import new_identity
from seed_runtime.input_support import InputSupportValidator
from seed_runtime.yield_evidence import _record_yield_evidence
from seed_runtime.recurrence_measurement import (
    RecordedMeasuredAssertion,
    get_recorded_measured_assertion,
)


class AssertionComparisonError(ValueError):
    """The bounded Assertion comparison could not be instantiated."""


@dataclass(frozen=True)
class AssertionYieldInput:
    assertion_identity: str
    recorded_occurrence_reference: str
    integrity: str


@dataclass(frozen=True)
class AssertionCoordinateDistinction:
    coordinate: str
    same: bool
    present: tuple[bool, bool]
    compared_material: tuple[Any, Any]


@dataclass(frozen=True)
class AssertionYieldComparison:
    assertion_identity: str
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
    """One exact coordinate result inside its yielding Compare occurrence."""

    assertion_identity: str
    recorded_occurrence_reference: str
    coordinate: str
    material: dict[str, Any]

    @property
    def reference(self) -> dict[str, str]:
        return {
            "recorded_occurrence_reference": self.recorded_occurrence_reference,
            "assertion_identity": self.assertion_identity,
        }




COORDINATES: dict[str, tuple[str, ...]] = {
    "standing": ("dimensions", "standing"),
    "source_provenance": ("dimensions", "source_provenance"),
    "responsibility": ("dimensions", "responsibility"),
    "authority": ("dimensions", "authority"),
    "scope": ("assertion_scope",),
    "input_support": ("input_support",),
    "completeness_boundary": ("completeness_boundary",),
    "completeness_scope": ("completeness_scope",),
    "unknowns": ("unknowns",),
    "limits": ("limits",),
}



def _read(material: dict[str, Any], path: tuple[str, ...]) -> tuple[bool, Any]:
    value: Any = material
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
    compared_assertion_identity: str,
    inputs: Iterable[dict[str, str]],
    locality_identity: str,
    coordinate: str,
    present: Iterable[bool],
    compared_material: Iterable[Any],
    same: bool,
) -> str:
    identity = {
        "compared_assertion_identity": compared_assertion_identity,
        "inputs": list(inputs),
        "locality_identity": locality_identity,
        "coordinate": coordinate,
        "present": list(present),
        "compared_material": list(compared_material),
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
    required = {"recorded_occurrence_reference", "assertion_identity"}
    if any(set(reference) != required for reference in exact_references):
        raise AssertionComparisonError(
            "each input must be one exact yielding-event and Assertion identity pair"
        )
    if (
        exact_references[0] == exact_references[1]
        or exact_references[0]["recorded_occurrence_reference"]
        == exact_references[1]["recorded_occurrence_reference"]
    ):
        raise AssertionComparisonError(
            "one yielding occurrence cannot be compared with itself"
        )
    if exact_references[0]["assertion_identity"] != exact_references[1]["assertion_identity"]:
        raise AssertionComparisonError(
            "Assertion yield Compare requires one canonical Assertion identity"
        )

    assertions: list[RecordedMeasuredAssertion] = []
    inputs = []
    for reference in exact_references:
        assertion = get_recorded_measured_assertion(
            ledger,
            recorded_occurrence_reference=reference["recorded_occurrence_reference"],
            assertion_identity=reference["assertion_identity"],
        )
        if assertion is None:
            raise AssertionComparisonError(
                "an Assertion reference does not resolve to its yielding occurrence"
            )
        integrity = ledger.integrity_of(assertion.recorded_occurrence_reference)
        if integrity == CORRUPTED:
            raise AssertionComparisonError(
                "a corrupted yielding occurrence cannot participate in Compare"
            )
        assertions.append(assertion)
        inputs.append(
            AssertionYieldInput(
                assertion_identity=assertion.assertion_identity,
                recorded_occurrence_reference=assertion.recorded_occurrence_reference,
                integrity=integrity,
            )
        )

    distinctions = []
    for coordinate, path in COORDINATES.items():
        coordinate_reads = tuple(
            _read(assertion.material, path) for assertion in assertions
        )
        present = (coordinate_reads[0][0], coordinate_reads[1][0])
        compared_material = (coordinate_reads[0][1], coordinate_reads[1][1])
        distinctions.append(
            AssertionCoordinateDistinction(
                coordinate=coordinate,
                same=present[0] == present[1] and _exactly_same(*compared_material),
                present=present,
                compared_material=compared_material,
            )
        )
    return AssertionYieldComparison(
        assertion_identity=exact_references[0]["assertion_identity"],
        inputs=(inputs[0], inputs[1]),
        distinctions=tuple(distinctions),
    )




def record_assertion_yield_comparison(
    ledger: EventLedger,
    *,
    locality_identity: str,
    comparison: AssertionYieldComparison,
) -> Event:
    """Preserve each literal Compare result without establishing later input support."""

    input_references = tuple(
        {
            "recorded_occurrence_reference": item.recorded_occurrence_reference,
            "assertion_identity": item.assertion_identity,
        }
        for item in comparison.inputs
    )
    verified = compare_assertion_yields(ledger, input_references)
    if comparison != verified:
        raise AssertionComparisonError(
            "the supplied comparison does not match its occurrence-bound inputs"
        )
    act_identity = new_identity("assertion_compare_act")
    act_occurrence_identity = new_identity("assertion_compare_act_occurrence")
    result_identity = new_identity("assertion_compare_result")
    participation = []
    for input_reference in input_references:
        role = "compared Assertion"
        locality_evidence = ledger.append(
            ASSERTION_COMPARE_INPUT_LOCALITY_EVIDENCE_KIND,
            {
                "first_subject": input_reference,
                "second_subject": {
                    "downstream_act_identity": act_identity,
                    "act_occurrence_identity": act_occurrence_identity,
                    "role": role,
                },
                "authority": "unestablished",
                "evidence_scope": "this exact Assertion-to-Compare Locality only",
            },
            locality_identity=locality_identity,
        )
        applicability = ledger.append(
            ASSERTION_COMPARE_INPUT_APPLICABILITY_KIND,
            {
                "input_reference": input_reference,
                "downstream_act_identity": act_identity,
                "role": role,
                "locality_evidence_identity": locality_evidence.identity,
                "standing": "applicable",
                "authority": "unestablished",
                "evidence_scope": "this exact input-to-Compare relation only",
            },
            locality_identity=locality_identity,
        )
        participation.append(
            {
                "subject_reference": input_reference,
                "role": role,
                "act_occurrence_identity": act_occurrence_identity,
                "locality_evidence_identity": locality_evidence.identity,
                "applicability_event_identity": applicability.identity,
            }
        )
    assertions = []
    for distinction in comparison.distinctions:
        content = {
            "coordinate": distinction.coordinate,
            "present": list(distinction.present),
            "compared_material": list(distinction.compared_material),
            "same": distinction.same,
        }
        identity = _distinction_assertion_identity(
            compared_assertion_identity=comparison.assertion_identity,
            inputs=input_references,
            locality_identity=locality_identity,
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
                        "input_support"
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
                    "compared_assertion_identity": comparison.assertion_identity,
                    "coordinate": distinction.coordinate,
                },
                "assertion_scope": {
                    "locality_identity": locality_identity,
                    "compared_yields": list(input_references),
                },
                "input_support": {"assertion_references": list(input_references)},
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
    result_material = {
        "result_identity": result_identity,
        "dimensions": {
            "identity": result_identity,
            "content": f"{len(assertions)} distinct comparison Assertions recorded",
            "source_provenance": "two occurrence-bound Assertion yields",
            "authority": "unestablished",
            "evidence_scope": "literal Compare results only",
            "scope_locality": f"locality:{locality_identity}",
            "occurrence_preservation": "comparison occurrence durably recorded",
        },
        "exact_act": "Compare",
        "downstream_act_identity": act_identity,
        "act_occurrence_identity": act_occurrence_identity,
        "participation": participation,
        "responsible_boundary": comparison.responsible_boundary,
        "responsibility": comparison.responsibility,
        "inputs": list(input_references),
        "assertions": assertions,
    }
    act_evidence = ledger.append(
        ASSERTION_COMPARE_ACT_EVIDENCE_KIND,
        {
            "downstream_act_identity": act_identity,
            "act_occurrence_identity": act_occurrence_identity,
            "act": "Compare",
            "responsibility": comparison.responsibility,
            "responsible_boundary": comparison.responsible_boundary,
            "participation": participation,
            "authority": "unestablished",
            "evidence_scope": "this exact bounded Compare occurrence only",
        },
        locality_identity=locality_identity,
    )
    yield_evidence = _record_yield_evidence(
        ledger,
        locality_identity=locality_identity,
        exact_act="Compare",
        act_occurrence_identity=act_occurrence_identity,
        responsible_act_evidence_identity=act_evidence.identity,
        result_kind=ASSERTION_YIELD_COMPARISON_RESULT_KIND,
        result_identity=result_identity,
        result_content=result_material,
        responsibility=comparison.responsibility,
        live_boundary="assertion_yield_compare",
        responsible_boundary=comparison.responsible_boundary,
        recorded_result_coordinates={key: (key,) for key in result_material},
    )
    return ledger.append(
        ASSERTION_YIELD_COMPARISON_RECORDED_KIND,
        {
            **result_material,
            "responsible_act_evidence_identity": act_evidence.identity,
            "yield_evidence_identity": yield_evidence.identity,
        },
        locality_identity=locality_identity,
    )


def assertions_of_recorded_assertion_comparison(
    event: Event,
) -> tuple[RecordedAssertionYieldDistinction, ...]:
    """Read and verify every exact result of one recorded Compare."""

    if event.kind != ASSERTION_YIELD_COMPARISON_RECORDED_KIND:
        raise AssertionComparisonError(
            f"{event.identity} is {event.kind}, not an Assertion yield Compare occurrence"
        )
    stated = event.material.get("assertions")
    outer_inputs = event.material.get("inputs")
    if not isinstance(stated, list):
        raise AssertionComparisonError(
            f"{event.identity} does not preserve its distinct comparison Assertions"
        )
    required_reference = {"recorded_occurrence_reference", "assertion_identity"}
    if (
        not isinstance(outer_inputs, list)
        or len(outer_inputs) != 2
        or any(
            not isinstance(reference, dict)
            or set(reference) != required_reference
            or not all(isinstance(value, str) and value for value in reference.values())
            for reference in outer_inputs
        )
        or outer_inputs[0]["recorded_occurrence_reference"]
        == outer_inputs[1]["recorded_occurrence_reference"]
        or outer_inputs[0]["assertion_identity"] != outer_inputs[1]["assertion_identity"]
    ):
        raise AssertionComparisonError(
            f"{event.identity} does not carry two distinct yields of one Assertion"
        )
    act_occurrence_identity = event.material.get("act_occurrence_identity")
    participation = event.material.get("participation")
    if (
        not isinstance(act_occurrence_identity, str)
        or not act_occurrence_identity
        or not isinstance(participation, list)
        or len(participation) != len(outer_inputs)
        or any(
            not isinstance(item, dict)
            or set(item)
            != {
                "subject_reference",
                "role",
                "act_occurrence_identity",
                "locality_evidence_identity",
                "applicability_event_identity",
            }
            or item["subject_reference"] != input_reference
            or item["role"] != "compared Assertion"
            or item["act_occurrence_identity"] != act_occurrence_identity
            or not isinstance(item["locality_evidence_identity"], str)
            or not item["locality_evidence_identity"]
            or not isinstance(item["applicability_event_identity"], str)
            or not item["applicability_event_identity"]
            for input_reference, item in zip(outer_inputs, participation)
        )
        or len({item["locality_evidence_identity"] for item in participation})
        != len(participation)
        or len({item["applicability_event_identity"] for item in participation})
        != len(participation)
    ):
        raise AssertionComparisonError(
            f"{event.identity} does not preserve exact input Locality, Applicability, "
            "and Participation for its Compare occurrence"
        )
    if len(stated) != len(COORDINATES):
        raise AssertionComparisonError(
            f"{event.identity} does not carry every distinct Compare result"
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
        support = assertion.get("input_support") if isinstance(assertion, dict) else None
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
            or not isinstance(scope.get("locality_identity"), str)
            or scope.get("locality_identity") != event.locality_identity
            or subject.get("compared_assertion_identity")
            != outer_inputs[0]["assertion_identity"]
            or subject.get("coordinate") != content.get("coordinate")
        ):
            raise AssertionComparisonError(
                f"{event.identity} carries an incoherent comparison Assertion"
            )
        required_content = {"coordinate", "present", "compared_material", "same"}
        if set(content) != required_content:
            raise AssertionComparisonError(
                f"{event.identity} carries an incomplete comparison result"
            )
        coordinate = content["coordinate"]
        present = content["present"]
        compared_material = content["compared_material"]
        same = content["same"]
        if (
            coordinate not in COORDINATES
            or coordinate in seen_coordinates
            or not isinstance(present, list)
            or len(present) != 2
            or not all(isinstance(value, bool) for value in present)
            or not isinstance(compared_material, list)
            or len(compared_material) != 2
            or not isinstance(same, bool)
            or same
            != (present[0] == present[1] and _exactly_same(compared_material[0], compared_material[1]))
        ):
            raise AssertionComparisonError(
                f"{event.identity} carries a result outside the Compare output contract"
            )
        seen_coordinates.add(coordinate)
        canonical = _distinction_assertion_identity(
            compared_assertion_identity=subject["compared_assertion_identity"],
            inputs=input_references,
            locality_identity=scope.get("locality_identity"),
            coordinate=content["coordinate"],
            present=content["present"],
            compared_material=content["compared_material"],
            same=content["same"],
        )
        if identity != canonical or identity in seen:
            raise AssertionComparisonError(
                f"{event.identity} carries a comparison Assertion with invalid identity"
            )
        seen.add(identity)
        read.append(
            RecordedAssertionYieldDistinction(
                assertion_identity=identity,
                recorded_occurrence_reference=event.identity,
                coordinate=content["coordinate"],
                material=assertion,
            )
        )
    if seen_coordinates != set(COORDINATES):
        raise AssertionComparisonError(
            f"{event.identity} does not carry the exact Compare coordinate set"
        )
    return tuple(read)
