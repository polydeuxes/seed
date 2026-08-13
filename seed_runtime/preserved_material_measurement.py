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
from seed_runtime.support_basis import (
    SupportBasis,
    SupportRecovery,
    support_commitment,
)

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
    # The localities the consumed occurrences carried. `06.Standing.B` requires
    # an act consuming material distinguished by locality to preserve the
    # locality of what it consumed, and to keep that distinct from the locality
    # it records into. Recording stamps the recording locality; without this
    # coordinate a finding drawn from two localities and recorded into a third
    # asserts only the third, and the consumed localities survive as nothing
    # but event identities a later reader would have to re-derive.
    consumed_localities: tuple[str, ...]
    # Preserved occurrences the measurement ran over. The denominator.
    occurrences_examined: int
    # How many of them carried the representation at least once.
    occurrences_carrying: int
    # How many times it occurred in total across them. This is the recurrence.
    total_count: int
    consumed_event_ids: tuple[str, ...]
    # The basis of the population consumed, where one was declared. Every
    # finding of one pass stands on the same population, so preserving the
    # enumeration in each copies that population once per representation.
    # `#2486` measured exactly this at 97% of a stored finding and built
    # SupportBasis to carry the basis instead. This path was written without
    # it and measured 96.8% on 500 findings over 2,000 occurrences.
    support_basis: SupportBasis | None = None
    boundary_notes: tuple[str, ...] = field(default=BOUNDARY_NOTES)
    convention: str = MEASUREMENT_CONVENTION

    def to_json_dict(self) -> dict[str, Any]:
        carried: dict[str, Any] = {
            "convention": self.convention,
            "representation_measured": self.declared.representation_measured,
            "equivalence_rule": self.declared.equivalence_rule,
            "counting_scope": self.declared.counting_scope,
            "premise_event_id": self.declared.premise_event_id,
            "measurement_form": "recurrence",
            "consumed_localities": list(self.consumed_localities),
            "occurrences_examined": self.occurrences_examined,
            "occurrences_carrying": self.occurrences_carrying,
            "total_count": self.total_count,
            "consumed_event_ids": list(self.consumed_event_ids),
            "consumed_count": len(self.consumed_event_ids),
            "boundary_notes": list(self.boundary_notes),
        }
        if self.support_basis is not None:
            # The basis replaces the enumeration rather than accompanying it.
            # Carrying both preserves the cost the basis exists to avoid, and
            # leaves two representations of one support free to disagree.
            carried["consumed_support"] = self.support_basis.to_json_dict()
            carried.pop("consumed_event_ids")
        return carried


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
    localities: dict[str, None] = {}
    examined = 0
    carrying = 0
    total = 0
    for event in _distinct_population(occurrences):
        text = _measurable_text(event)
        consumed.append(event.id)
        localities[_locality_of(event)] = None
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
        consumed_localities=tuple(localities),
        occurrences_examined=examined,
        occurrences_carrying=carrying,
        total_count=total,
        consumed_event_ids=tuple(consumed),
    )


def _locality_of(event: Event) -> str:
    """The locality coordinates this occurrence carries, in the recorded form.

    Only the coordinates present. `session_id` is optional, and rendering its
    absence as ``session:None`` would turn a missing witness into an asserted
    locality value. `06.Standing.B` holds that occurrences *may* carry a
    locality; it does not authorize inventing one where none was carried.
    """

    if event.session_id is None:
        return f"workspace:{event.workspace_id}"
    return f"workspace:{event.workspace_id};session:{event.session_id}"


def _distinct_population(occurrences: Iterable[Event]) -> list[Event]:
    """The occurrences to measure, refusing a repeated occurrence identity.

    The rule is not `01.External:28`, which requires the bounded scope to be
    disclosed and says nothing about identity-distinctness. It comes from what
    ``occurrences_examined`` asserts: a number of occurrences. One preserved
    occurrence referenced twice is one occurrence, so counting it twice reports
    a population larger than the one that exists, and every count drawn from it
    carries that inflation.

    Refused rather than deduplicated. Silently collapsing would decide that the
    caller meant one, and refusing rather than pretending is the same choice
    this module makes about material it cannot measure.

    `01.External.E.1` establishes the rule: each counted occurrence is
    distinguished by exact occurrence identity, and repeated reference to one
    preserved occurrence does not establish another. That clause was added
    because this refusal had nothing behind it.
    """

    population = list(occurrences)
    seen: set[str] = set()
    for event in population:
        if event.id in seen:
            raise PreservedMaterialMeasurementError(
                f"{event.id} appears more than once in one measured population"
            )
        seen.add(event.id)
    return population


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
    if "decoded_text" not in event.payload:
        # The occurrence says a text representation was formed and carries no
        # decoded text. That is incoherent material, and reading the coordinate
        # and trusting it would rest the finding on a claim about the material
        # rather than on the material, surfacing as a KeyError rather than as a
        # refusal stating what was wrong.
        #
        # `text_representation.available` records a *historical* outcome: at
        # ingress, this decoder formed a text representation. It is not the
        # present-tense availability `#2496` governs, which is asked of the
        # holder and never read from the ledger. One word carries both, which
        # is why this looked at first like a `#2496` violation and is not one.
        #
        # This refusal closes the incoherent case only. Whether gating on the
        # historical coordinate at all is faithful -- an occurrence recording
        # that no representation was formed, while carrying decoded text, is
        # still refused by the check above -- remains unresolved here.
        raise PreservedMaterialMeasurementError(
            f"{event.id} declares an available text representation but "
            "preserves no decoded text"
        )
    return event.payload["decoded_text"]


def measure_recurrences(
    occurrences: Iterable[Event],
    *,
    declared: "dict[str, DeclaredMeasurement]",
    counts_in: "callable[[str], dict[str, int]]",
    support_basis: SupportBasis | None = None,
    support_recovery: SupportRecovery | None = None,
) -> tuple[RecurrenceFinding, ...]:
    """Measure many representations across one pass of the material.

    Measuring many declared representations over the same bounded occurrence
    population, one at a time, re-walks and re-splits that population once per
    representation. On 4,716 declared representations over 2,000 preserved
    occurrences that is 9.43 million redundant splits and 10.12s; one pass is
    0.02s, measured at **509x** in one tree with only the call path toggled.

    That is a measured property of one workload shape, not an established
    account of acquisition. Where the declared representations come from is not
    established here, and this act receives them already declared.

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
    it has exceeded that boundary rather than extended it.

    ``counts_in`` may return counts sparsely. **A declared representation absent
    from its result occurred zero times in that occurrence**, and that is the
    convention rather than a silence: the declared set already states what was
    looked for, so absence from the result is a reported zero and not an
    unreported measurement. The single-representation path requires an explicit
    integer because it asks about one representation at a time and has no
    declared set to read the absence against.
    """

    if not declared:
        raise PreservedMaterialMeasurementError(
            "a measurement must declare at least one representation"
        )
    scopes = set()
    for representation, declaration in declared.items():
        if declaration.representation_measured != representation:
            raise PreservedMaterialMeasurementError(
                f"declaration for {representation!r} measures "
                f"{declaration.representation_measured!r}"
            )
        scopes.add(declaration.counting_scope)
    if len(scopes) > 1:
        # One pass consumes one population, so every finding it produces
        # receives that population. A declaration disclosing a different
        # counting scope would have its scope assertion preserved beside a
        # population the act did not draw from it. `01.External:28` requires
        # the disclosed scope to be the scope within which occurrences were
        # counted, so the disagreement is refused rather than reconciled.
        raise PreservedMaterialMeasurementError(
            "one pass consumes one population, so every declaration must "
            f"disclose the same counting scope; got {len(scopes)}"
        )
    consumed: list[str] = []
    localities: dict[str, None] = {}
    examined = 0
    carrying: dict[str, int] = {name: 0 for name in declared}
    total: dict[str, int] = {name: 0 for name in declared}
    walked = _distinct_population(occurrences)
    if support_basis is not None and support_recovery is not None:
        # A finding claiming support from preserved occurrences must have
        # measured the material those occurrences carry. An `Event` can be
        # constructed directly with any id and any payload, so a caller could
        # hand this act an object bearing a recovered identity and different
        # text: the identities would commit correctly, the basis would recover,
        # and the finding would preserve a basis for material it never saw.
        #
        # So where a basis is declared, the material is read from the ledger
        # the basis is recovered against. The supplied objects still determine
        # which occurrences are consumed and in what order; they do not supply
        # what was measured.
        preserved = []
        for event in walked:
            recorded = support_recovery.ledger.get(event.id)
            if recorded is None:
                raise PreservedMaterialMeasurementError(
                    f"{event.id} is not preserved in the ledger this support "
                    "basis is recovered against"
                )
            preserved.append(recorded)
        walked = preserved
    for event in walked:
        text = _measurable_text(event)
        consumed.append(event.id)
        localities[_locality_of(event)] = None
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
    consumed_localities = tuple(localities)
    if support_basis is not None:
        # A basis carried but never checked would let a finding preserve a
        # commitment to a population the act did not walk. `support_commitment`
        # is a pure function of the rule and the ordered identities, so the act
        # can confirm the basis commits to what it actually consumed.
        if support_commitment(support_basis.selection_rule, population) != (
            support_basis.commitment
        ):
            raise PreservedMaterialMeasurementError(
                "the declared support basis does not commit to the population "
                "this measurement consumed"
            )
        if support_basis.support_count != len(population):
            raise PreservedMaterialMeasurementError(
                f"the declared support basis counts {support_basis.support_count} "
                f"occurrences and this measurement consumed {len(population)}"
            )
        # Committing to the identities is not describing the population. The
        # commitment is a digest over the rule and the ordered ids and says
        # nothing about scope, so a basis declaring one locality could be
        # accepted for a population drawn from several: the ids match, and the
        # preserved basis then asserts a scope the act never consumed within.
        # The producing act refuses that now; a later recovery failure is a
        # different responsibility and arrives too late to prevent it.
        declared_locality = (
            f"workspace:{support_basis.workspace_id};"
            f"session:{support_basis.session_id}"
        )
        if consumed_localities != (declared_locality,):
            raise PreservedMaterialMeasurementError(
                f"the declared support basis is scoped to {declared_locality} "
                f"and this measurement consumed {list(consumed_localities)}"
            )
        for event in walked:
            if event.kind != support_basis.occurrence_kind:
                raise PreservedMaterialMeasurementError(
                    f"the declared support basis selects "
                    f"{support_basis.occurrence_kind} and {event.id} is "
                    f"{event.kind}"
                )
        # A basis declares a selection rule -- every preserved occurrence of
        # this scope's kind through this boundary -- and the checks above prove
        # only that the population consumed is *within* that description. A
        # caller supplying three of four occurrences through the same boundary
        # would pass all of them, and the finding would then preserve a basis
        # claiming completeness the act never established.
        #
        # Verifying that requires interpreting the boundary, which only an
        # EventLedger does, so a basis is accepted only where the act is given
        # the means to check it. Implementation inconvenience does not move the
        # obligation to a later reader: once the enumeration is replaced, a
        # recovery discovering the lie arrives after the false basis is
        # preserved.
        if support_recovery is None:
            raise PreservedMaterialMeasurementError(
                "a support basis declares a selection through a boundary, and "
                "accepting one requires a SupportRecovery to establish that "
                "the population consumed is that selection"
            )
        # `recover` performs the basis's own selection through the boundary and
        # refuses unless the result reproduces the committed digest. Together
        # with the commitment check above -- which ties the population walked to
        # that same digest -- the population consumed is the selection declared.
        #
        # A third comparison of the two results was written here and removed: it
        # cannot fail while both checks hold, and mutation testing found no test
        # that could reach it. A guard nothing can reach reads as a proof and is
        # not one.
        support_recovery.recover(support_basis)
    return tuple(
        RecurrenceFinding(
            declared=declaration,
            consumed_localities=consumed_localities,
            occurrences_examined=examined,
            occurrences_carrying=carrying[representation],
            total_count=total[representation],
            consumed_event_ids=population,
            support_basis=support_basis,
        )
        for representation, declaration in declared.items()
    )


def preserved_ingress_occurrences(
    ledger: EventLedger, *, workspace_id: str, session_id: str
) -> list[Event]:
    """Every preserved ingress occurrence carrying this locality, in append order.

    The material measured is what Seed recorded, not what a file contains.

    The locality is read as a locality. Reading the whole workspace and
    discarding the rest returned the same occurrences and cost the whole
    workspace: `#2414` measured 757.8ms against 46.4ms on sixteen co-resident
    bodies, a factor equal to how many of them share the ledger.

    `06.Standing.B` holds that a locality is a carried coordinate. It preserves
    nothing and performs nothing; the ledger preserves, and this reads by the
    coordinate the occurrences carry.
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
    for event in _distinct_population(occurrences):
        text = _measurable_text(event)
        consumed.append(event.id)
        occupant = occupant_of(text)
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

    Not the runtime's `SupportBasis` representation. This is the chain of
    recorded premise findings one finding stood on, recovered nearest premise
    first. It preserves that dependency relation and claims nothing about the
    producing act's support basis; the prose called it that before the two
    were distinguished and kept calling it that after.
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
