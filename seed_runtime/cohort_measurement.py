"""Measure the recorded comparison occurrences, not the material.

`measurement_self_survey` established the move one level down: recorded
measurement occurrences are themselves preserved events, and counting over them
is the same kind of act performed on a different subject. This is that, one
level up — the subject is recorded **comparison** occurrences.

**Why it is needed.** A comparison holds that two bounded exchanges both carried
a distinction. That a distinction recurs across *ten* of them is a fact about
the population of preserved testimony, and no single comparison contains it.
`#2420` recorded that gap explicitly: Seed held each pairwise sharing and a
reader supplied "appears in 7 of 16 bodies".

**What it reports, in full.**

    these N independently preserved bodies carry the same measured distinction
    under the declared rule and scope

Every word is load-bearing, and three inferences are refused in the record
itself:

*Independently preserved is not independent.* The bodies were preserved in
separate exchanges. Nothing establishes that their sources are unrelated —
two 19th-century grammar textbooks, or two transcriptions sharing editorial
apparatus, are not independent witnesses. `05.Testimony.E` says repetition is
not independent corroboration, and a cohort is repetition.

*The denominator is a fact about supply.* "Ten of sixteen" reports which bodies
were supplied to this Seed. Supplying three more dictionaries would move every
cohort without anything about the material changing.

*Not carrying and not exposing are different.* A body that never exposed the
measured coordinate has not declined to carry the distinction. Both are
recorded, and neither is inferred from the other's absence.

**Proving the third state needs both recorded kinds.** An earlier form of this
computed "coordinate not exposed" as everything left over after carrying and
not-carrying, from comparisons alone. That is wrong: a body whose finding
exists at the coordinate but which was never compared against a carrier falls
into the same residue, and would have been reported as never having exposed it.
So the recorded **measurement** occurrences supply which bodies measured that
coordinate at all, and the recorded **comparison** occurrences supply which of
them carried the distinction. Neither kind can answer alone.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable

from seed_runtime.bounded_testimony_comparison import COMPARISON_RECORDED_KIND
from seed_runtime.events import EventLedger
from seed_runtime.models import Event
from seed_runtime.preserved_material_measurement import MEASUREMENT_RECORDED_KIND

COHORT_RECORDED_KIND = "operator.measurement.cohort_recorded"

FORBIDDEN_INFERENCES: tuple[str, ...] = (
    "independently preserved is not independent; nothing here establishes that "
    "the bodies' sources are unrelated",
    "a cohort is repetition, and repetition is not independent corroboration",
    "the cohort size reports which bodies were supplied to this Seed, not a "
    "property of the material",
    "a body that never exposed the measured coordinate has not declined to "
    "carry the distinction",
    "carrying the same measured distinction establishes no relation between the "
    "bodies that carried it",
)


class CohortMeasurementError(Exception):
    """The cohort boundary could not be instantiated."""


@dataclass(frozen=True)
class Distinction:
    """What recurred: an exact left, an exact right, at an exact position."""

    left: str
    right: str
    measured_position: str
    equivalence_rule: str

    def to_json_dict(self) -> dict[str, Any]:
        return {
            "left_representation": self.left,
            "right_representation": self.right,
            "measured_position": self.measured_position,
            "equivalence_rule": self.equivalence_rule,
        }


@dataclass(frozen=True)
class Cohort:
    distinction: Distinction
    carried_by: tuple[str, ...]
    exposed_without_it: tuple[str, ...]
    coordinate_not_exposed: tuple[str, ...]
    consumed_event_ids: tuple[str, ...]
    population: tuple[str, ...]

    @property
    def cohort_size(self) -> int:
        return len(self.carried_by)

    def to_json_dict(self) -> dict[str, Any]:
        return {
            "distinction": self.distinction.to_json_dict(),
            "carried_by": list(self.carried_by),
            "exposed_without_it": list(self.exposed_without_it),
            "coordinate_not_exposed": list(self.coordinate_not_exposed),
            "cohort_size": self.cohort_size,
            "population_size": len(self.population),
            "consumed_event_ids": list(self.consumed_event_ids),
        }


def surveyed_occurrences(
    ledger: EventLedger, *, workspace_id: str, session_id: str | None = None
) -> list[Event]:
    """The recorded comparison occurrences this measurement consumes."""

    events = (
        ledger.list(workspace_id)
        if session_id is None
        else ledger.list_session(workspace_id, session_id)
    )
    return [e for e in events if e.kind == COMPARISON_RECORDED_KIND]


def measured_coordinates(
    ledger: EventLedger, *, workspace_id: str, session_id: str | None = None
) -> dict[tuple[str, str, str], set[str]]:
    """Which bounded exchanges measured each coordinate at all.

    Read from recorded measurement occurrences, because no comparison can say
    why a body is absent from it.
    """

    events = (
        ledger.list(workspace_id)
        if session_id is None
        else ledger.list_session(workspace_id, session_id)
    )
    exposed: dict[tuple[str, str, str], set[str]] = {}
    for event in events:
        if event.kind != MEASUREMENT_RECORDED_KIND:
            continue
        left = event.payload.get("measured_left_representation")
        if left is None:
            continue
        key = (
            str(left),
            str(event.payload.get("measured_position")),
            str(event.payload.get("equivalence_rule")),
        )
        scope = event.payload.get("dimensions", {}).get("scope_locality")
        if scope is not None:
            exposed.setdefault(key, set()).add(scope)
    return exposed


def _coordinate(event: Event, name: str) -> Any:
    for distinction in event.payload.get("distinctions", []):
        if distinction["coordinate"] == name:
            return distinction
    return None


def _exchange_of(preserved: dict[str, Any]) -> str | None:
    return preserved.get("carried", {}).get("scope")


def measure_cohorts(
    ledger: EventLedger, *, workspace_id: str, session_id: str | None = None
) -> list[Cohort]:
    """Count, over recorded comparisons, which bodies carried each distinction.

    Only comparisons whose inputs agree on left representation, rule and
    measured position contribute. Two findings measured differently did not
    observe the same distinction, and counting them together would report a
    recurrence nothing observed.
    """

    consumed = surveyed_occurrences(
        ledger, workspace_id=workspace_id, session_id=session_id
    )
    exposed = measured_coordinates(
        ledger, workspace_id=workspace_id, session_id=session_id
    )
    if not consumed:
        raise CohortMeasurementError(
            "no recorded comparison occurrences to measure; this act's subject "
            "is what Compare recorded, not preserved material"
        )

    carried: dict[Distinction, set[str]] = {}
    sources: dict[Distinction, set[str]] = {}
    population: set[str] = set(x for bodies in exposed.values() for x in bodies)

    for event in consumed:
        left = _coordinate(event, "measured_left_representation")
        rule = _coordinate(event, "equivalence_rule")
        position = _coordinate(event, "measured_position")
        if not (left and rule and position):
            continue
        if not (left["same"] and rule["same"] and position["same"]):
            continue

        inputs = event.payload.get("inputs", [])
        exchanges = [_exchange_of(i) for i in inputs]
        if any(x is None for x in exchanges):
            continue
        population.update(exchanges)

        base = dict(
            left=str(left["values"][0]),
            measured_position=str(position["values"][0]),
            equivalence_rule=str(rule["values"][0]),
        )
        for right in event.payload.get("shared_occupants", []):
            key = Distinction(right=right, **base)
            carried.setdefault(key, set()).update(exchanges)
            sources.setdefault(key, set()).add(event.id)

        by_event = {i["event_id"]: x for i, x in zip(inputs, exchanges)}
        for event_id, occupants in event.payload.get(
            "occupants_in_one_only", {}
        ).items():
            for right in occupants:
                # Seen on one side only. The side that had it carries it: a
                # cohort of one is a cohort, and reporting it as carried by
                # nobody would say a distinction no body holds.
                key = Distinction(right=right, **base)
                carried.setdefault(key, set()).add(by_event[event_id])
                sources.setdefault(key, set()).add(event.id)

    cohorts = []
    for key in sorted(
        carried, key=lambda k: (-len(carried[k]), k.left, k.right)
    ):
        holds = carried[key]
        measured = exposed.get(
            (key.left, key.measured_position, key.equivalence_rule), set()
        )
        cohorts.append(
            Cohort(
                distinction=key,
                carried_by=tuple(sorted(holds)),
                # measured the coordinate and is not among those carrying it
                exposed_without_it=tuple(sorted(measured - holds)),
                # never measured the coordinate at all
                coordinate_not_exposed=tuple(sorted(population - measured)),
                consumed_event_ids=tuple(sorted(sources[key])),
                population=tuple(sorted(population)),
            )
        )
    return cohorts


def render_cohort(cohort: Cohort) -> str:
    """The literal sentence, and nothing stronger."""

    return (
        f"{cohort.cohort_size} independently preserved bodies carry "
        f"({cohort.distinction.left!r}, {cohort.distinction.right!r}) at "
        f"{cohort.distinction.measured_position} under "
        f"{cohort.distinction.equivalence_rule}"
    )


def record_cohort(
    ledger: EventLedger,
    *,
    workspace_id: str,
    session_id: str,
    cohort: Cohort,
) -> Event:
    """Preserve one cohort measurement so a later responsible act may consume it."""

    payload = {
        "dimensions": {
            "identity": (
                f"cohort:{cohort.distinction.left}|{cohort.distinction.right}"
            ),
            "content": render_cohort(cohort),
            "standing": "measured",
            "source_provenance": "recorded comparison occurrences",
            "responsibility": "cohort-measurement-over-recorded-comparisons",
            "authority_warrant": (
                "measurement evidence only; establishes no relation between the "
                "bodies, no source independence, and no corroboration"
            ),
            "scope_locality": f"workspace:{workspace_id};session:{session_id}",
            "occurrence_preservation": "cohort measurement durably recorded",
        },
        "surveyed_subject": "recorded comparison occurrences",
        "population_scope": (
            "the bounded exchanges appearing in the consumed comparisons; the "
            "denominator reports which bodies were supplied to this Seed"
        ),
        "mutates_cluster": False,
        "unknowns": [
            "what any carried representation means remains Unknown",
            "whether the carrying bodies stand in any relation remains Unknown",
            "whether their sources are independent remains Unknown",
        ],
        "forbidden_inferences": list(FORBIDDEN_INFERENCES),
        **cohort.to_json_dict(),
    }
    return ledger.append(
        COHORT_RECORDED_KIND, workspace_id, payload, session_id=session_id
    )
