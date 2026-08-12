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
from seed_runtime.ids import new_id

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
    # The identities this measurement consumed, available while the act runs.
    # On the result-Assertion path a recoverable support basis is formed from
    # this population instead of preserving the enumeration in every result;
    # the basis belongs to that path, and this dataclass does not own a second
    # coordinate for it. `#2486` measured why: copying the population into
    # every finding of a body cost 97% of the stored finding.
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
            # Not "support_basis": the result-Assertion coordinate surface owns
            # that key and its fields are merged over this dict, so naming both
            # the same silently replaced one with the other.
            "consumed_event_ids": list(self.consumed_event_ids),
            "consumed_count": len(self.consumed_event_ids),
            "boundary_notes": list(self.boundary_notes),
        }


@dataclass(frozen=True)
class RecurrenceFinding:
    """How often one representation occurred, and across how much material.

    `01.External:28` grants recurrence by name and states its disclosures. This
    is the grant taken directly: what is measured is the representation itself,
    rather than a position defined relative to it.

    That is a fact about what was measured, not about constitutional subject
    identity. The recorded identity remains `measurement:<representation>`, and
    `01.External:28` bounds the result to the measurement assertion. Nothing
    here establishes that the representation is the subject of anything, or
    that Standing concerning it exists.

    Three counts, because one is not readable without the others. A
    representation occurring three times says nothing until the material it
    occurred across is also stated, and occurring three times in one occurrence
    is not the same finding as occurring once in each of three. The clause
    requires the bounded scope be disclosed; `occurrences_examined` is that
    scope's size, and it is preserved rather than left to the reader.
    """

    declared: DeclaredMeasurement
    # Preserved occurrences the measurement ran over. The denominator.
    occurrences_examined: int
    # How many of them carried the representation at least once.
    occurrences_carrying: int
    # How many times it occurred in total across them. This is the recurrence.
    total_count: int
    consumed_event_ids: tuple[str, ...]
    boundary_notes: tuple[str, ...] = field(default=BOUNDARY_NOTES)
    convention: str = MEASUREMENT_CONVENTION

    def to_json_dict(self) -> dict[str, Any]:
        return {
            "convention": self.convention,
            "representation_measured": self.declared.representation_measured,
            "equivalence_rule": self.declared.equivalence_rule,
            "counting_scope": self.declared.counting_scope,
            "premise_event_id": self.declared.premise_event_id,
            "measurement_form": "recurrence",
            "occurrences_examined": self.occurrences_examined,
            "occurrences_carrying": self.occurrences_carrying,
            "total_count": self.total_count,
            "consumed_event_ids": list(self.consumed_event_ids),
            "consumed_count": len(self.consumed_event_ids),
            "boundary_notes": list(self.boundary_notes),
        }


def measure_recurrence(
    occurrences: Iterable[Event],
    *,
    declared: DeclaredMeasurement,
    occurrences_of: "callable[[str], int]",
) -> RecurrenceFinding:
    """Count how often one representation occurs across preserved material.

    ``occurrences_of`` receives one preserved representation and returns how
    many times the measured representation occurs within it under the declared
    equivalence rule. The rule decides what counts as an occurrence, so the
    caller supplies it and this act performs no interpretation: a
    representation that does not occur occurs zero times, which is a finding
    and not an absence of one.

    Refuses the same material `measure_occupancy` refuses, for the same reason.
    A measurement over a bounded population cannot measure text in material
    that has none, and skipping would silently narrow the scope the finding
    goes on to disclose.
    """

    consumed: list[str] = []
    examined = 0
    carrying = 0
    total = 0
    for event in occurrences:
        text = _measurable_text(event)
        consumed.append(event.id)
        count = occurrences_of(text)
        if not isinstance(count, int) or isinstance(count, bool) or count < 0:
            raise PreservedMaterialMeasurementError(
                "a recurrence count must be a non-negative integer, "
                f"not {count!r}"
            )
        examined += 1
        if count:
            carrying += 1
            total += count
    return RecurrenceFinding(
        declared=declared,
        occurrences_examined=examined,
        occurrences_carrying=carrying,
        total_count=total,
        consumed_event_ids=tuple(consumed),
    )


def _measurable_text(event: Event) -> str:
    """The text this occurrence preserved, or a refusal stating why not.

    Both recurrence measurements refuse identically, so the refusal lives in
    one place: a measurement that reports its scope cannot quietly skip part
    of it.
    """

    if event.kind != INGRESS_OCCURRED_KIND:
        raise PreservedMaterialMeasurementError(
            f"only preserved ingress occurrences may be measured: {event.kind}"
        )
    text = event.payload.get("text_representation")
    if text is None:
        text = {"available": "decoded_text" in event.payload}
    if not isinstance(text, dict) or not text.get("available"):
        raise PreservedMaterialMeasurementError(
            f"{event.id} preserves material with no available text "
            "representation, and this measurement measures text"
        )
    return event.payload["decoded_text"]


def measure_recurrences(
    occurrences: Iterable[Event],
    *,
    declared: "dict[str, DeclaredMeasurement]",
    counts_in: "callable[[str], dict[str, int]]",
) -> tuple[RecurrenceFinding, ...]:
    """Measure many representations across one pass of the material.

    Measuring every representation of a body one at a time re-walks and
    re-splits the whole body once per representation. On 4,716 representations
    over 2,000 preserved occurrences that is 9.43 million redundant splits and
    9.91s; one pass is 0.02s, measured at **583x**. The acquisition workload is
    exactly this shape — every distinct representation against every occurrence
    — so the redundancy is not incidental to it.

    ``counts_in`` receives one preserved representation and returns how many
    times each measured representation occurs within it, under the declared
    equivalence rule. It is called once per occurrence rather than once per
    representation per occurrence.

    Findings are identical to calling `measure_recurrence` for each
    representation. Each carries its own declaration, the same consumed
    population, and the same three counts. This changes only how many times the
    material is walked.

    A representation counted but not declared is refused. The declared set is
    the measurement boundary, and a counting function returning results outside
    it has exceeded that boundary rather than extended it. A representation
    declared but never counted receives a finding of zero, which is a finding.
    """

    if not declared:
        raise PreservedMaterialMeasurementError(
            "a measurement must declare at least one representation"
        )
    for representation, declaration in declared.items():
        if declaration.representation_measured != representation:
            raise PreservedMaterialMeasurementError(
                f"declaration for {representation!r} measures "
                f"{declaration.representation_measured!r}"
            )
    consumed: list[str] = []
    examined = 0
    carrying: dict[str, int] = {name: 0 for name in declared}
    total: dict[str, int] = {name: 0 for name in declared}
    for event in occurrences:
        text = _measurable_text(event)
        consumed.append(event.id)
        examined += 1
        counted = counts_in(text)
        if not isinstance(counted, dict):
            raise PreservedMaterialMeasurementError(
                f"counts must be returned as a mapping, not {type(counted).__name__}"
            )
        for representation, count in counted.items():
            if representation not in declared:
                raise PreservedMaterialMeasurementError(
                    f"{representation!r} was counted but not declared"
                )
            if not isinstance(count, int) or isinstance(count, bool) or count < 0:
                raise PreservedMaterialMeasurementError(
                    "a recurrence count must be a non-negative integer, "
                    f"not {count!r}"
                )
            if count:
                carrying[representation] += 1
                total[representation] += count
    population = tuple(consumed)
    return tuple(
        RecurrenceFinding(
            declared=declaration,
            occurrences_examined=examined,
            occurrences_carrying=carrying[representation],
            total_count=total[representation],
            consumed_event_ids=population,
        )
        for representation, declaration in declared.items()
    )


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
        text = event.payload.get("text_representation")
        if text is None:
            # An occurrence recorded before `#2490` carries no such coordinate,
            # and carried `decoded_text` exactly when a representation was
            # available, because no occurrence without one was recorded at all.
            # Reading its absence that way is what keeps already-preserved
            # material measurable; it is not a default for new occurrences,
            # which always declare it.
            text = {"available": "decoded_text" in event.payload}
        if not isinstance(text, dict) or not text.get("available"):
            # A declared measurement over the complete ingress population cannot
            # measure text in material that has none. It refuses rather than
            # skipping, because skipping would silently narrow the counting
            # scope the finding goes on to disclose — the scope is part of what
            # the finding is, and a population measured is not a population
            # partly measured. `#2490` began preserving material whose text
            # representation is unavailable; a selection that admits only
            # text-representable material is its own declared scope and does not
            # exist yet.
            raise PreservedMaterialMeasurementError(
                f"{event.id} preserves material with no available text "
                "representation, and this measurement measures text"
            )
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


def _measurement_finding_payload(
    *,
    workspace_id: str,
    session_id: str,
    finding: MeasurementFinding | RecurrenceFinding,
    extra: dict[str, Any] | None,
) -> dict[str, Any]:
    carried = finding.to_json_dict()
    basis = (extra or {}).get("support_basis", {}).get("basis") if extra else None
    if basis is not None:
        # A result Assertion carries a recoverable support basis, so the
        # enumeration it replaces is not written beside it. `#2486` measured
        # the enumeration at 97% of a 4,000-line finding.
        carried["consumed_support"] = basis
        carried.pop("consumed_event_ids", None)
    return {
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
        **carried,
        **(extra or {}),
        "lineage": (
            [finding.declared.premise_event_id]
            if finding.declared.premise_event_id
            else []
        ),
    }


def record_measurement_findings(
    ledger: EventLedger,
    *,
    workspace_id: str,
    session_id: str,
    findings: Iterable[tuple[MeasurementFinding | RecurrenceFinding, dict[str, Any] | None]],
) -> list[Event]:
    """Preserve a bounded group of findings in one ledger transaction."""

    supplied = list(findings)
    premise_ids = {
        finding.declared.premise_event_id
        for finding, _ in supplied
        if finding.declared.premise_event_id is not None
    }
    for premise_id in premise_ids:
        premise = ledger.get(premise_id)
        if premise is None or premise.kind != MEASUREMENT_RECORDED_KIND:
            raise PreservedMaterialMeasurementError(
                "a premise must be a recorded measurement finding"
            )
    events = [
        Event(
            id=new_id("evt"),
            kind=MEASUREMENT_RECORDED_KIND,
            workspace_id=workspace_id,
            payload=_measurement_finding_payload(
                workspace_id=workspace_id,
                session_id=session_id,
                finding=finding,
                extra=extra,
            ),
            session_id=session_id,
        )
        for finding, extra in supplied
    ]
    return ledger.append_many(events)


def record_measurement_finding(
    ledger: EventLedger,
    *,
    workspace_id: str,
    session_id: str,
    finding: MeasurementFinding | RecurrenceFinding,
    extra: dict[str, Any] | None = None,
) -> Event:
    """Preserve a finding so a later responsible act may consume it.

    The recorded authority states the clause's own limit. A finding is
    measurement evidence and is not relation, meaning, or established standing.
    """

    return record_measurement_findings(
        ledger,
        workspace_id=workspace_id,
        session_id=session_id,
        findings=((finding, extra),),
    )[0]


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
