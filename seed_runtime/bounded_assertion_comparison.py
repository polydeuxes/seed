"""One occurrence-local bounded comparison of preserved findings.

`01.Standing.E` permits a bounded comparison to have as input multiple separately
preserved source-relative Assertions or findings while preserving each input's coordinates as
that input carries them. `historical comparison report`
records the responsible boundary: **the bounded comparison boundary in which they participate, local
to the instantiated comparison and not named beyond this comparison.**

So this is a call, not a service. Each invocation is one comparison occurrence
with its own responsible boundary. There is no comparator object, no registry, and no persistent
boundary waiting to be filled — a responsible boundary that outlived its occurrence would be
a shared boundary that the exact coordinates do not establish.

**What it has as input is what Seed recorded.** The inputs are recorded measurement
findings. The pair findings used in the corpus experiments are computed in
experiment code and never recorded; a comparison over those would have as input an
result Seed does not hold.

**What it yields is distinctions, and a relation only where one is
established.** Two measurements over different bounded localities are not in
disagreement because their results differ — each is exact within its own scope.
`01.Standing.E:29` holds: agreement is not truth, and comparison establishes no
support, input support, or corroboration.
"""

from __future__ import annotations


from dataclasses import dataclass
from typing import Any, Iterable

from seed_runtime.events import CORRUPTED, EventLedger
from seed_runtime.event import Event
from seed_runtime.identities import new_identity
from seed_runtime.preserved_material_measurement import (
    MEASUREMENT_RECORDED_KIND,
)
from seed_runtime.yield_evidence import _record_yield_evidence

COMPARISON_RECORDED_KIND = "operator.measurement.comparison_recorded"
COMPARISON_ACT_EVIDENCE_KIND = "operator.measurement.comparison_act_evidenced"
COMPARISON_INPUT_LOCALITY_EVIDENCE_KIND = (
    "operator.measurement.comparison_input_locality_evidenced"
)
COMPARISON_INPUT_APPLICABILITY_KIND = (
    "operator.measurement.comparison_input_applicability_recorded"
)
COMPARISON_RESULT_KIND = "bounded Assertion Compare result"
COMPARISON_RESPONSIBILITY = (
    "Compare two exact preserved findings and preserve the bounded result"
)
EVENT_KIND_RESPONSIBILITIES = {
    COMPARISON_RECORDED_KIND: "02.Acts.A",
    COMPARISON_ACT_EVIDENCE_KIND: "02.Acts.A",
    COMPARISON_INPUT_LOCALITY_EVIDENCE_KIND: "06.Standing.B",
    COMPARISON_INPUT_APPLICABILITY_KIND: "01.Standing.E.1",
}

# Coordinates preserved from each recorded measurement finding
# carries each. A coordinate absent from an input is named as absent and never
# supplied: the clause forbids erasing or strengthening what an input carries
# and does not supply what an input lacks.
INPUT_COORDINATES: dict[str, tuple[str, ...]] = {
    "responsibility": ("dimensions", "responsibility"),
    "provenance": ("dimensions", "source_provenance"),
    "subject": ("dimensions", "identity"),
    "scope": ("dimensions", "scope_locality"),
    "authority": ("dimensions", "authority"),
    "confidence_or_uncertainty": (),
    "unknowns": ("unknowns",),
    "standing": ("dimensions", "standing"),
    "limits": ("limits",),
    "input_support": ("input_support",),
}

# This is not an enum; more than one relation may remain established.
UNKNOWN_RELATION = "Unknown"

LIMITS: tuple[str, ...] = (
    "a distinction between two findings is not a relation between what they measured",
    "differing results across bounded localities is not disagreement; each is exact "
    "within its own scope",
    "a representation occurring in both findings establishes no relation between "
    "the bodies that carried it",
    "this comparison establishes no truth, support, input support, source relation, "
    "or corroboration",
)


class BoundedComparisonError(Exception):
    """The comparison boundary could not be instantiated."""


@dataclass(frozen=True)
class PreservedInput:
    """One input as it occurred, with what it lacks named rather than filled."""

    event_identity: str
    carried: dict[str, Any]
    absent: tuple[str, ...]

    def to_json_dict(self) -> dict[str, Any]:
        return {
            "event_identity": self.event_identity,
            "carried": dict(self.carried),
            "coordinates_absent": list(self.absent),
        }


@dataclass(frozen=True)
class Distinction:
    """One literal difference or sameness between the inputs."""

    coordinate: str
    same: bool
    compared_material: tuple[Any, ...]

    def to_json_dict(self) -> dict[str, Any]:
        return {
            "coordinate": self.coordinate,
            "same": self.same,
            "compared_material": list(self.compared_material),
        }


@dataclass(frozen=True)
class ComparisonFinding:
    inputs: tuple[PreservedInput, ...]
    distinctions: tuple[Distinction, ...]
    shared_representations: tuple[str, ...]
    representations_in_one_only: dict[str, tuple[str, ...]]
    bounded_relation: str

def _read(material: dict[str, Any], path: tuple[str, ...]) -> Any:
    value: Any = material
    for key in path:
        if not isinstance(value, dict) or key not in value:
            return None
        value = value[key]
    return value


def _preserve(event: Event) -> PreservedInput:
    carried: dict[str, Any] = {}
    absent: list[str] = []
    for coordinate, path in INPUT_COORDINATES.items():
        value = _read(event.material, path) if path else None
        if value is None:
            absent.append(coordinate)
        else:
            carried[coordinate] = value
    # Scope has a second half the finding carries separately.
    counting_scope = event.material.get("counting_scope")
    if counting_scope is not None:
        carried["counting_scope"] = counting_scope
    return PreservedInput(
        event_identity=event.identity,
        carried=carried,
        absent=tuple(absent),
    )


def _representations(event: Event) -> set[str]:
    return {
        item["representation"]
        for item in event.material.get("representation_counts", [])
    }


def compare_preserved_findings(
    ledger: EventLedger, event_identities: Iterable[str]
) -> ComparisonFinding:
    """Instantiate one comparison over preserved findings, or refuse.

    The responsible boundary is local to the occurrence. Nothing survives the call.
    """

    identities = tuple(event_identities)
    if len(identities) != 2:
        # Two, exactly. `01.Standing.E` says "multiple", and an earlier representation of
        # this function accepted any number and intersected them all — n-ary
        # comparison implemented while its own report called it unbuilt. What
        # more than two inputs jointly establish is not read, and a set
        # intersection over n findings is not that read.
        raise BoundedComparisonError(
            "a bounded comparison has as input exactly two preserved findings; "
            f"{len(identities)} supplied. Comparing more than two is unbuilt"
        )
    if len(set(identities)) != len(identities):
        raise BoundedComparisonError(
            "an input compared with itself does not supply multiple distinct "
            "preserved findings"
        )

    events: list[Event] = []
    for event_identity in identities:
        event = ledger.get(event_identity)
        if event is None:
            raise BoundedComparisonError(f"no such preserved occurrence: {event_identity}")
        if event.kind != MEASUREMENT_RECORDED_KIND:
            raise BoundedComparisonError(
                f"{event_identity} is {event.kind}, not a recorded measurement finding"
            )
        # This act asserts to preserve what it has as input, so this act verifies
        # what it has as input. A corrupted input cannot be preserved, only copied.
        # `unverifiable` is recorded on the input rather than refused: an
        # in-memory ledger and any occurrence written before the material identity
        # existed are both lawfully unverifiable, and refusing them would
        # require a guarantee nothing ever offered.
        if ledger.integrity_of(event_identity) == CORRUPTED:
            raise BoundedComparisonError(
                f"{event_identity} does not match its recorded material identity; a corrupted "
                "occurrence cannot be preserved by a comparison"
            )
        events.append(event)

    inputs = tuple(_preserve(event) for event in events)

    distinctions: list[Distinction] = []
    for coordinate, field in (
        ("representation_measured", "representation_measured"),
        ("relative_representation", "relative_representation"),
        ("equivalence_rule", "equivalence_rule"),
        ("counting_scope", "counting_scope"),
        ("measured_position", "measured_position"),
        ("measurement_distinction", "measurement_distinction"),
    ):
        compared_material = tuple(event.material.get(field) for event in events)
        distinctions.append(
            Distinction(coordinate, len(set(map(repr, compared_material))) == 1, compared_material)
        )
    scopes = tuple(i.carried.get("scope") for i in inputs)
    distinctions.append(
        Distinction("bounded_locality", len(set(map(repr, scopes))) == 1, scopes)
    )

    representation_sets = [_representations(event) for event in events]
    shared = representation_sets[0] & representation_sets[1]
    only = {
        event.identity: tuple(sorted(representations - shared))
        for event, representations in zip(events, representation_sets)
    }

    same = {d.coordinate: d.same for d in distinctions}
    if not (same["representation_measured"] and same["relative_representation"]):
        relation = UNKNOWN_RELATION
    elif not (same["equivalence_rule"] and same["measured_position"]):
        relation = UNKNOWN_RELATION
    elif not same["bounded_locality"]:
        relation = UNKNOWN_RELATION
    elif representation_sets[0] == representation_sets[1]:
        relation = "agreement"
    else:
        relation = "conflict"

    return ComparisonFinding(
        inputs=inputs,
        distinctions=tuple(distinctions),
        shared_representations=tuple(sorted(shared)),
        representations_in_one_only=only,
        bounded_relation=relation,
    )


def record_comparison_finding(
    ledger: EventLedger,
    *,
    locality_identity: str,
    finding: ComparisonFinding,
) -> Event:
    """Preserve one comparison occurrence so a later act may have it participate."""

    input_event_identities = [item.event_identity for item in finding.inputs]
    verified = compare_preserved_findings(ledger, input_event_identities)
    if finding != verified:
        raise BoundedComparisonError(
            "the supplied comparison does not match its exact recorded inputs"
        )
    act_identity = new_identity("bounded_comparison_act")
    act_occurrence_identity = new_identity("bounded_comparison_act_occurrence")
    result_identity = new_identity("bounded_comparison_result")
    participation = []
    for input_event_identity in input_event_identities:
        role = "preserved finding compared"
        locality_evidence = ledger.append(
            COMPARISON_INPUT_LOCALITY_EVIDENCE_KIND,
            {
                "first_subject": input_event_identity,
                "second_subject": {
                    "downstream_act_identity": act_identity,
                    "act_occurrence_identity": act_occurrence_identity,
                    "role": role,
                },
                "authority": "unestablished",
                "evidence_scope": "this exact finding-to-Compare Locality only",
            },
            locality_identity=locality_identity,
        )
        applicability = ledger.append(
            COMPARISON_INPUT_APPLICABILITY_KIND,
            {
                "input_reference": input_event_identity,
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
                "subject_reference": input_event_identity,
                "role": role,
                "act_occurrence_identity": act_occurrence_identity,
                "locality_evidence_identity": locality_evidence.identity,
                "applicability_event_identity": applicability.identity,
            }
        )
    result_material = {
        "result_identity": result_identity,
        "dimensions": {
            "identity": result_identity,
            "content": f"{len(finding.inputs)} preserved findings compared",
            "source_provenance": "recorded measurement findings",
            "responsibility": "bounded-comparison-boundary",
            "authority": "unestablished",
            "evidence_scope": (
                "comparison evidence only; the bounded relation holds inside this "
                "comparison boundary and establishes nothing beyond it"
            ),
            "scope_locality": f"locality:{locality_identity}",
            "occurrence_preservation": "comparison occurrence durably recorded",
        },
        "responsible_boundary": (
            "this comparison occurrence; the responsible boundary is local to the instantiated "
            "comparison and is not named beyond this comparison"
        ),
        "downstream_act_identity": act_identity,
        "act_occurrence_identity": act_occurrence_identity,
        "participation": participation,
        "unknowns": [
            "what any compared representation means remains Unknown",
            "whether the compared bodies stand in any relation remains Unknown",
        ],
        "limits": list(LIMITS),
        "inputs": [item.to_json_dict() for item in finding.inputs],
        "distinctions": [item.to_json_dict() for item in finding.distinctions],
        "shared_representations": list(finding.shared_representations),
        "representations_in_one_only": {
            key: list(value)
            for key, value in finding.representations_in_one_only.items()
        },
        "bounded_relation": finding.bounded_relation,
    }
    act_evidence = ledger.append(
        COMPARISON_ACT_EVIDENCE_KIND,
        {
            "downstream_act_identity": act_identity,
            "act_occurrence_identity": act_occurrence_identity,
            "act": "bounded Compare",
            "responsibility": COMPARISON_RESPONSIBILITY,
            "responsible_boundary": "this Seed",
            "participation": participation,
            "authority": "unestablished",
            "evidence_scope": "this exact bounded Compare occurrence only",
        },
        locality_identity=locality_identity,
    )
    yield_evidence = _record_yield_evidence(
        ledger,
        locality_identity=locality_identity,
        exact_act="bounded Compare",
        act_occurrence_identity=act_occurrence_identity,
        result_kind=COMPARISON_RESULT_KIND,
        result_identity=result_identity,
        result_content=result_material,
        responsibility=COMPARISON_RESPONSIBILITY,
        live_boundary="bounded_assertion_compare",
        responsible_boundary="this Seed",
        recorded_result_coordinates={key: (key,) for key in result_material},
    )
    return ledger.append(
        COMPARISON_RECORDED_KIND,
        {
            **result_material,
            "responsible_act_evidence_identity": act_evidence.identity,
            "yield_evidence_identity": yield_evidence.identity,
        },
        locality_identity=locality_identity,
    )
