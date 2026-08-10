"""Declared measurement over preserved operator-ingress occurrences.

`01.External.E` is titled *Measurement and recurrence do not establish meaning*,
and `01.External:28` grants the finding and states its conditions:

    A declared measurement may produce bounded findings of exact equality,
    count, recurrence, prefix occurrence, the result of a declared predicate,
    or adjacency within its measurement boundary. Those findings do not
    establish structural, grammatical, or semantic meaning, or constitutional
    standing beyond the measurement assertion. A recurrence assertion must
    disclose the representation or projection measured, the rule by which
    equivalence or sameness was determined, and the bounded scope within which
    occurrences were counted.

Those three disclosures are required fields here, not commentary.

**What this consumes is Seed's own preserved material.** Occurrences come from
the ledger, having been recorded through operator ingress with
``authority="occurrence-only; meaning Unknown"``. Reading a file directly and
measuring it produces a result that vanishes with the process and that no later
act can consume; `#2368` did that and it was withdrawn.

**What this produces is recorded.** Each finding is appended to the ledger, so a
later responsible act may consume it. `05.Testimony:27` permits exactly that: a
bounded comparison may consume preserved findings "only while preserving each
input's attribution, provenance, support basis, subject, scope, authority,
confidence or uncertainty, Unknowns, standing, and forbidden inferences".

**A finding may stand on an earlier finding.** `premise_event_id` records which,
so what a finding depended on travels with it. `#2387` measured why this
matters: the same measurement yields 3.0% with no premise and 88.1% standing on
one that bounds a position.

Nothing here establishes meaning, relation, truth, or any standing beyond the
measurement assertion. `01.Standing.D` refuses relation standing to co-presence,
and co-presence is what a finding reports.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable

from seed_runtime.events import EventLedger
from seed_runtime.event import Event

MEASUREMENT_RECORDED_KIND = "operator.measurement.finding_recorded"
INGRESS_OCCURRED_KIND = "operator.ingress.ingress_occurred"

MEASUREMENT_CONVENTION = "preserved_material_declared_measurement_v1"

BOUNDARY_NOTES: tuple[str, ...] = (
    "A finding reports a count within its stated scope and nothing further.",
    "Recurrence establishes that a representation occurs more than once only.",
    "A highest-count occupant of a position is not the meaning of that position.",
    "Co-presence of representations establishes no relation (01.Standing.D).",
    "A finding standing on a premise is not stronger than a finding without one.",
    "The premise is preserved so the finding cannot be read independently of it.",
    "This produces no meaning, relation, truth, applicability, or admission.",
)


class PreservedMaterialMeasurementError(ValueError):
    """Raised when a measurement cannot be declared or consumed as stated."""


@dataclass(frozen=True)
class DeclaredMeasurement:
    """The three disclosures `01.External:28` requires, plus the premise.

    `representation_measured`, `equivalence_rule`, and `counting_scope` are the
    clause's own words. They are required because the clause requires them, and
    an empty one is refused rather than defaulted.
    """

    representation_measured: str
    equivalence_rule: str
    counting_scope: str
    premise_event_id: str | None = None
    # The representation this measurement measured relative to, when it had
    # one.  A finding can only supply an representation to a later measurement if it
    # records the representation it used, so this is what makes a finding
    # representation-supplying rather than merely informative.
    measured_after: str | None = None
    # The form of positional measurement performed, and the exact
    # representations it was performed relative to.  Without these a finding
    # says what it found but not what question produced it, so nothing can form
    # the next question from it without a reader restating the first.  These
    # are exact strings taken from preserved material; neither names a kind.
    form: str | None = None
    relative_to: tuple[str, ...] = ()
    # Where the position measured sits relative to what it was measured
    # relative to.  Recorded so a measurement can be compared with another
    # that measured elsewhere, and so a coordinate that never varies is
    # observable rather than implicit in the code that indexed it.
    measured_position: dict[str, Any] | None = None

    def __post_init__(self) -> None:
        for name in ("representation_measured", "equivalence_rule", "counting_scope"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise PreservedMaterialMeasurementError(
                    f"a declared measurement must disclose {name}"
                )


@dataclass(frozen=True)
class Occupancy:
    """One representation and the number of positions it occupied."""

    representation: str
    occurrence_count: int


@dataclass(frozen=True)
class MeasurementFinding:
    """A bounded count over preserved occurrences, and what it stood on."""

    declared: DeclaredMeasurement
    positions_measured: int
    occupancies: tuple[Occupancy, ...]
    consumed_event_ids: tuple[str, ...]
    boundary_notes: tuple[str, ...] = field(default=BOUNDARY_NOTES)
    convention: str = MEASUREMENT_CONVENTION

    @property
    def highest_count_occupancy(self) -> Occupancy | None:
        """The occupancy with the highest count, or nothing if none was measured.

        A count, not a rank of importance. `01.External:28` bounds a finding to
        the measurement assertion, so the most frequent occupant of a position
        is the most frequent occupant of a position and carries no standing
        that a less frequent one lacks.
        """

        return self.occupancies[0] if self.occupancies else None

    def to_json_dict(self) -> dict[str, Any]:
        return {
            "convention": self.convention,
            "representation_measured": self.declared.representation_measured,
            "equivalence_rule": self.declared.equivalence_rule,
            "counting_scope": self.declared.counting_scope,
            "premise_event_id": self.declared.premise_event_id,
            "measured_left_representation": self.declared.measured_after,
            "measurement_form": self.declared.form,
            "measured_relative_to": list(self.declared.relative_to),
            "measured_position": self.declared.measured_position,
            "positions_measured": self.positions_measured,
            "occupancies": [
                {"representation": o.representation, "occurrence_count": o.occurrence_count}
                for o in self.occupancies
            ],
            "consumed_event_ids": list(self.consumed_event_ids),
            "boundary_notes": list(self.boundary_notes),
        }


def preserved_ingress_occurrences(
    ledger: EventLedger, *, workspace_id: str, session_id: str
) -> list[Event]:
    """Every occurrence this session preserved, in append order.

    The material measured is what Seed recorded, not what a file contains.

    The session is read as a session. Reading the workspace and discarding the
    rest returned the same occurrences and cost the whole workspace: `#2414`
    measured 757.8ms against 46.4ms on sixteen co-resident bodies, a factor
    equal to how many of them share the ledger.
    """

    return [
        event
        for event in ledger.list_session(workspace_id, session_id)
        if event.kind == INGRESS_OCCURRED_KIND
    ]


def measure_occupancy(
    occurrences: Iterable[Event],
    *,
    declared: DeclaredMeasurement,
    occupant_of: "callable[[str], str | None]",
) -> MeasurementFinding:
    """Count which representations occupy a position across preserved material.

    ``occupant_of`` receives one preserved representation and returns the
    representation occupying the measured position within it, or ``None`` when
    that occurrence has no such position. It performs no interpretation; a
    position that is absent is absent, not Unknown.
    """

    counts: dict[str, int] = {}
    consumed: list[str] = []
    measured = 0
    for event in occurrences:
        if event.kind != INGRESS_OCCURRED_KIND:
            raise PreservedMaterialMeasurementError(
                f"only preserved ingress occurrences may be measured: {event.kind}"
            )
        consumed.append(event.id)
        occupant = occupant_of(event.payload["decoded_text"])
        if occupant is None:
            continue
        measured += 1
        counts[occupant] = counts.get(occupant, 0) + 1
    ordered = tuple(
        Occupancy(representation=r, occurrence_count=n)
        for r, n in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
    )
    return MeasurementFinding(
        declared=declared,
        positions_measured=measured,
        occupancies=ordered,
        consumed_event_ids=tuple(consumed),
    )


def record_measurement_finding(
    ledger: EventLedger,
    *,
    workspace_id: str,
    session_id: str,
    finding: MeasurementFinding,
    extra: dict[str, Any] | None = None,
) -> Event:
    """Preserve a finding so a later responsible act may consume it.

    The recorded authority states the clause's own limit. A finding is
    measurement evidence and is not relation, meaning, or established standing.
    """

    if finding.declared.premise_event_id is not None:
        premise = ledger.get(finding.declared.premise_event_id)
        if premise is None or premise.kind != MEASUREMENT_RECORDED_KIND:
            raise PreservedMaterialMeasurementError(
                "a premise must be a recorded measurement finding"
            )

    payload = {
        "dimensions": {
            "identity": f"measurement:{finding.declared.representation_measured}",
            "content": finding.declared.counting_scope,
            "standing": "measured",
            "source_provenance": "preserved operator-ingress occurrences",
            "responsibility": "declared-measurement-over-preserved-material",
            "authority_warrant": (
                "measurement evidence only; establishes no meaning, relation, "
                "or standing beyond the measurement assertion"
            ),
            "scope_locality": f"workspace:{workspace_id};session:{session_id}",
            "occurrence_preservation": "declared measurement durably recorded",
        },
        "mutates_cluster": False,
        "unknowns": ["what any measured representation means remains Unknown"],
        **finding.to_json_dict(),
        **(extra or {}),
        "lineage": (
            [finding.declared.premise_event_id]
            if finding.declared.premise_event_id
            else []
        ),
    }
    return ledger.append(
        MEASUREMENT_RECORDED_KIND, workspace_id, payload, session_id=session_id
    )


def premise_chain(ledger: EventLedger, event_id: str) -> list[str]:
    """Every finding this one stood on, nearest premise first.

    `05.Testimony:27` requires a consumed input's support basis to be preserved.
    This is that basis, recovered: a finding cannot be read as independent of
    what bounded it.
    """

    chain: list[str] = []
    current = ledger.get(event_id)
    while current is not None:
        premise_id = current.payload.get("premise_event_id")
        if premise_id is None:
            break
        chain.append(premise_id)
        current = ledger.get(premise_id)
    return chain
