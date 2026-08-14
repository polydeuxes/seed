"""One occurrence-local bounded comparison of preserved findings.

`01.Standing.E` permits a bounded comparison to have as input multiple independently
preserved source-relative Assertions or findings while preserving each input's coordinates as
that input carries them. `historical comparison report`
records the responsible boundary: **the bounded comparison boundary in which they participate, local
to the instantiated comparison and not named beyond this comparison.**

So this is a call, not a service. Each invocation is one comparison occurrence
with its own responsible boundary. There is no comparator object, no registry, and no persistent
boundary waiting to be filled — a responsible boundary that outlived its occurrence would be
the shared boundary the reconstruction says does not exist.

**What it has as input is what Seed recorded.** The inputs are recorded measurement
findings. The pair findings used in the corpus experiments are computed in
experiment code and never recorded; a comparison over those would have as input an
result Seed does not hold.

**What it yields is distinctions, and a relation only where one is
established.** Two measurements over different bounded exchanges are not in
disagreement because their results differ — each is exact within its own scope.
`01.Standing.E:29` holds: agreement is not truth, and comparison establishes no
support, input support, or corroboration.
"""

from __future__ import annotations


from dataclasses import dataclass
from typing import Any, Iterable

from seed_runtime.events import CORRUPTED, EventLedger
from seed_runtime.event import Event
from seed_runtime.preserved_material_measurement import (
    MEASUREMENT_RECORDED_KIND,
    premise_chain,
)

COMPARISON_RECORDED_KIND = "operator.measurement.comparison_recorded"

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
    "forbidden_inferences": ("boundary_notes",),
}

# This is not an enum; more than one relation may remain established.
UNKNOWN_RELATION = "Unknown"

BOUNDARY_NOTES: tuple[str, ...] = (
    "a distinction between two findings is not a relation between what they measured",
    "differing results across bounded exchanges is not disagreement; each is exact "
    "within its own scope",
    "a representation occurring in both findings establishes no relation between "
    "the bodies that carried it",
    "this comparison establishes no truth, support, input support, source independence, "
    "or corroboration",
)


class BoundedComparisonError(Exception):
    """The comparison boundary could not be instantiated."""


@dataclass(frozen=True)
class PreservedInput:
    """One input as it arrived, with what it lacks named rather than filled."""

    event_id: str
    carried: dict[str, Any]
    absent: tuple[str, ...]
    support_basis: tuple[str, ...]
    integrity: str

    def to_json_dict(self) -> dict[str, Any]:
        return {
            "event_id": self.event_id,
            "carried": dict(self.carried),
            "coordinates_absent": list(self.absent),
            "support_basis": list(self.support_basis),
            "integrity": self.integrity,
        }


@dataclass(frozen=True)
class Distinction:
    """One literal difference or sameness between the inputs."""

    coordinate: str
    same: bool
    values: tuple[Any, ...]

    def to_json_dict(self) -> dict[str, Any]:
        return {
            "coordinate": self.coordinate,
            "same": self.same,
            "values": list(self.values),
        }


@dataclass(frozen=True)
class ComparisonFinding:
    inputs: tuple[PreservedInput, ...]
    distinctions: tuple[Distinction, ...]
    shared_occupants: tuple[str, ...]
    occupants_in_one_only: dict[str, tuple[str, ...]]
    bounded_relation: str
    relation_basis: str

    def to_json_dict(self) -> dict[str, Any]:
        return {
            "inputs": [i.to_json_dict() for i in self.inputs],
            "distinctions": [d.to_json_dict() for d in self.distinctions],
            "shared_occupants": list(self.shared_occupants),
            "occupants_in_one_only": {
                k: list(v) for k, v in self.occupants_in_one_only.items()
            },
            "bounded_relation": self.bounded_relation,
            "relation_basis": self.relation_basis,
        }


def _read(payload: dict[str, Any], path: tuple[str, ...]) -> Any:
    value: Any = payload
    for key in path:
        if not isinstance(value, dict) or key not in value:
            return None
        value = value[key]
    return value


def _preserve(ledger: EventLedger, event: Event) -> PreservedInput:
    carried: dict[str, Any] = {}
    absent: list[str] = []
    for coordinate, path in INPUT_COORDINATES.items():
        value = _read(event.payload, path) if path else None
        if value is None:
            absent.append(coordinate)
        else:
            carried[coordinate] = value
    # Scope has a second half the finding carries separately.
    counting_scope = event.payload.get("counting_scope")
    if counting_scope is not None:
        carried["counting_scope"] = counting_scope
    return PreservedInput(
        event_id=event.id,
        carried=carried,
        absent=tuple(absent),
        support_basis=tuple(premise_chain(ledger, event.id)),
        integrity=ledger.integrity_of(event.id),
    )


def _occupants(event: Event) -> set[str]:
    return {
        occupancy["representation"]
        for occupancy in event.payload.get("occupancies", [])
    }


def compare_preserved_findings(
    ledger: EventLedger, event_ids: Iterable[str]
) -> ComparisonFinding:
    """Instantiate one comparison over preserved findings, or refuse.

    The responsible boundary is local to the occurrence. Nothing survives the call.
    """

    ids = tuple(event_ids)
    if len(ids) != 2:
        # Two, exactly. `01.Standing.E` says "multiple", and an earlier form of
        # this function accepted any number and intersected them all — n-ary
        # comparison implemented while its own report called it unbuilt. What
        # more than two inputs jointly establish is not reconstructed, and a set
        # intersection over n findings is not that reconstruction.
        raise BoundedComparisonError(
            "a bounded comparison has as input exactly two preserved findings; "
            f"{len(ids)} supplied. Comparing more than two is unbuilt"
        )
    if len(set(ids)) != len(ids):
        raise BoundedComparisonError(
            "an input compared with itself is not multiple independently "
            "preserved findings"
        )

    events: list[Event] = []
    for event_id in ids:
        event = ledger.get(event_id)
        if event is None:
            raise BoundedComparisonError(f"no such preserved occurrence: {event_id}")
        if event.kind != MEASUREMENT_RECORDED_KIND:
            raise BoundedComparisonError(
                f"{event_id} is {event.kind}, not a recorded measurement finding"
            )
        # This act asserts to preserve what it has as input, so this act verifies
        # what it has as input. A corrupted input cannot be preserved, only copied.
        # `unverifiable` is recorded on the input rather than refused: an
        # in-memory ledger and any occurrence written before the digest
        # existed are both lawfully unverifiable, and refusing them would
        # require a guarantee nothing ever offered.
        if ledger.integrity_of(event_id) == CORRUPTED:
            raise BoundedComparisonError(
                f"{event_id} does not match its recorded digest; a corrupted "
                "occurrence cannot be preserved by a comparison"
            )
        events.append(event)

    inputs = tuple(_preserve(ledger, event) for event in events)

    distinctions: list[Distinction] = []
    for coordinate, field in (
        ("representation_measured", "representation_measured"),
        ("measured_left_representation", "measured_left_representation"),
        ("equivalence_rule", "equivalence_rule"),
        ("counting_scope", "counting_scope"),
        ("measured_position", "measured_position"),
        ("measurement_form", "measurement_form"),
    ):
        values = tuple(event.payload.get(field) for event in events)
        distinctions.append(
            Distinction(coordinate, len(set(map(repr, values))) == 1, values)
        )
    scopes = tuple(i.carried.get("scope") for i in inputs)
    distinctions.append(
        Distinction("bounded_exchange", len(set(map(repr, scopes))) == 1, scopes)
    )

    occupant_sets = [_occupants(event) for event in events]
    shared = occupant_sets[0] & occupant_sets[1]
    only = {
        event.id: tuple(sorted(occupants - shared))
        for event, occupants in zip(events, occupant_sets)
    }

    same = {d.coordinate: d.same for d in distinctions}
    if not (same["representation_measured"] and same["measured_left_representation"]):
        relation = UNKNOWN_RELATION
        basis = "the inputs did not measure the same representation"
    elif not (same["equivalence_rule"] and same["measured_position"]):
        relation = UNKNOWN_RELATION
        basis = "the inputs were not measured under the same rule and position"
    elif not same["bounded_exchange"]:
        relation = UNKNOWN_RELATION
        basis = (
            "the inputs are exact within different bounded exchanges, so differing "
            "results are not disagreement and matching results are not corroboration"
        )
    elif occupant_sets[0] == occupant_sets[1]:
        relation = "agreement"
        basis = "same representation, rule, position and bounded exchange, same occupants"
    else:
        relation = "conflict"
        basis = (
            "same representation, rule, position and bounded exchange, "
            "different occupants"
        )

    return ComparisonFinding(
        inputs=inputs,
        distinctions=tuple(distinctions),
        shared_occupants=tuple(sorted(shared)),
        occupants_in_one_only=only,
        bounded_relation=relation,
        relation_basis=basis,
    )


def record_comparison_finding(
    ledger: EventLedger,
    *,
    workspace_id: str,
    session_id: str,
    finding: ComparisonFinding,
) -> Event:
    """Preserve one comparison occurrence so a later act may have it participate."""

    payload = {
        "dimensions": {
            "identity": "bounded-assertion-comparison",
            "content": f"{len(finding.inputs)} preserved findings compared",
            "standing": "compared",
            "source_provenance": "recorded measurement findings",
            "responsibility": "bounded-comparison-boundary",
            "authority": (
                "comparison evidence only; the bounded relation holds inside this "
                "comparison boundary and establishes nothing beyond it"
            ),
            "scope_locality": f"workspace:{workspace_id};session:{session_id}",
            "occurrence_preservation": "comparison occurrence durably recorded",
        },
        "responsible_boundary": (
            "this comparison occurrence; the responsible boundary is local to the instantiated "
            "comparison and is not named beyond this comparison"
        ),
        "mutates_cluster": False,
        "unknowns": [
            "what any compared representation means remains Unknown",
            "whether the compared bodies stand in any relation remains Unknown",
        ],
        "boundary_notes": list(BOUNDARY_NOTES),
        "input_event_ids": [i.event_id for i in finding.inputs],
        **finding.to_json_dict(),
    }
    return ledger.append(
        COMPARISON_RECORDED_KIND, workspace_id, payload, session_id=session_id
    )
