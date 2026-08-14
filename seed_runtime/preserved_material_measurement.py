"""Declared measurement over preserved operator-ingress occurrences.

`01.Source.E` is titled *Measurement and recurrence do not establish represented relation*,
and `01.Source:28` grants the finding and states its conditions:

    A declared measurement may produce bounded findings of exact equality,
    count, recurrence, prefix occurrence, the result of a declared predicate,
    or adjacency within its measurement boundary. Those findings do not
    establish structural, grammatical, or semantic represented relation, or constitutional
    standing beyond the measurement assertion. A recurrence assertion must
    disclose the representation or representation measured, the rule by which
    equivalence or sameness was determined, and the bounded scope within which
    occurrences were counted.

Those three disclosures are required fields here, not commentary.

**What this is for is Seed's own preserved material.** Occurrences recorded
through operator ingress carry ``authority="occurrence-only; represented relation Unknown"``,
and reading a file directly and measuring it produces a result that vanishes
with the process and that no later act can have as input; `#2368` did that and it was
withdrawn.

A measurement given a ledger reads its material from that ledger. A measurement
given occurrences measures what it was handed, which is lawful and weaker: the
finding then says its material was supplied rather than preserved, and the two
asserts are recorded distinctly. This module used to describe only the first
while doing both.

**What this produces is recorded.** Each finding is appended to the ledger, so a
later responsible act may have it participate. `01.Standing.E` permits exactly that: a
bounded comparison may have as input preserved findings "only while preserving each
input source coordinates, provenance, support basis, subject, scope, authority,
confidence or uncertainty, Unknowns, standing, and forbidden inferences".

**A finding may stand on an earlier finding.** `premise_event_id` records which,
so what a finding depended on travels with it. `#2387` measured why this
matters: the same measurement yields 3.0% with no premise and 88.1% standing on
one that bounds a position.

Nothing here establishes represented relation, relation, truth, or any standing beyond the
measurement assertion. `01.Standing.D` refuses relation standing to co-presence,
and co-presence is what a finding reports.
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from typing import Any, Iterable

from seed_runtime.events import EventLedger
from seed_runtime.event import Event
from seed_runtime.ids import new_id
from seed_runtime.production_evidence import (
    PRODUCTION_EVIDENCE_KIND,
    _record_production_evidence,
    production_commitment as _production_content_commitment,
)
from seed_runtime.support_basis import (
    SupportBasis,
    SupportValidator,
    support_commitment,
)

MEASUREMENT_RECORDED_KIND = "operator.measurement.finding_recorded"
INGRESS_OCCURRED_KIND = "operator.ingress.ingress_occurred"
RECURRENCE_RESULT_KIND = "recurrence Measurement finding"

MEASUREMENT_CONVENTION = "preserved_material_declared_measurement_v1"

# What a finding may say about where the material it measured came from. The
# measuring act knows which of these is true and nothing carried it forward, so
# recording stated the stronger one for every finding. A measurement given a
# ledger reads its material from that ledger; a measurement given occurrences
# measures what it was handed, and no later act can establish that those
# objects carried what the preserved occurrences of the same identity carry.
MATERIAL_READ_FROM_LEDGER = "preserved operator-ingress occurrences"
MATERIAL_AS_SUPPLIED = (
    "occurrences as supplied to this measurement, not read from a ledger"
)

# `#2431` identified "declared-measurement-over-preserved-material" as inherited
# contamination: it wrote the Act into the Responsibility slot for a declared
# measurement whose production Responsibility had never been validated. `#2439`
# then validated the partial shape and kept it partial -- production occurrence "this Seed",
# Act a declared measurement, Standing measured, and a Responsibility that stays
# unestablished. That is ordinary rather than contradictory.
RESPONSIBILITY_UNESTABLISHED = "unestablished"

# What recording composes around a finding's own content. A caller adding to a
# recorded finding may not replace any of it.
_RESERVED_RECORDING_COORDINATES = frozenset(
    {"dimensions", "mutates_cluster", "unknowns", "provenance_occurrence_refs"}
)

BOUNDARY_NOTES: tuple[str, ...] = (
    "A finding reports a count within its stated scope and nothing further.",
    "Recurrence establishes that a representation occurs more than once only.",
    "A highest-count occupant of a position is not the represented relation of that position.",
    "Co-presence of representations establishes no relation (01.Standing.D).",
    "A finding standing on a premise is not stronger than a finding without one.",
    "The premise is preserved so the finding cannot be read independently of it.",
    "This produces no represented relation, relation, truth, applicability, or admission.",
)


class PreservedMaterialMeasurementError(ValueError):
    """Raised when a measurement cannot use its declared inputs as stated."""


@dataclass(frozen=True)
class DeclaredMeasurement:
    """The three disclosures `01.Source:28` requires, plus the premise.

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
    # The identities this measurement input_ids, available while the act runs.
    # On the result-Assertion path a reconstructible support basis is formed from
    # this population instead of preserving the enumeration in every result;
    # the basis belongs to that path, and this dataclass does not own a second
    # coordinate for it. `#2486` measured why: copying the population into
    # every finding of a body cost 97% of the stored finding.
    input_event_ids: tuple[str, ...]
    # Where the measured material came from. Defaults to the weaker Assertion:
    # a finding that did not read from a ledger cannot say it measured
    # preserved material, and silence must not read as the stronger one.
    material_provenance: str = MATERIAL_AS_SUPPLIED
    boundary_notes: tuple[str, ...] = field(default=BOUNDARY_NOTES)
    convention: str = MEASUREMENT_CONVENTION

    @property
    def highest_count_occupancy(self) -> Occupancy | None:
        """The occupancy with the highest count, or nothing if none was measured.

        A count, not a rank of importance. `01.Source:28` bounds a finding to
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
            # Not "support_basis": the result-Assertion coordinate surface carries
            # that key and its fields are merged over this dict, so naming both
            # the same silently replaced one with the other.
            "input_event_ids": list(self.input_event_ids),
            "input_count": len(self.input_event_ids),
            "boundary_notes": list(self.boundary_notes),
        }


@dataclass(frozen=True)
class RecurrenceFinding:
    """How often one representation occurred, and across how much material.

    `01.Source:28` grants recurrence by name and states its disclosures. This
    is the grant taken directly: what is measured is the representation itself,
    rather than a position defined relative to it.

    That is an Assertion about what was measured, not about constitutional subject
    identity. The recorded identity remains `measurement:<representation>`, and
    `01.Source:28` bounds the result to the measurement assertion. Nothing
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
    # The localities the input_ids occurrences carried. `06.Standing.B` requires
    # an act material participating in an Act distinguished by locality to preserve the
    # locality of what it input_ids, and to keep that distinct from the locality
    # it records into. `None` in this tuple is an occurrence that carried no
    # locality, preserved rather than filled in.
    # Recording stamps the recording locality; without this
    # coordinate a finding drawn from two localities and recorded into a third
    # asserts only the third, and the input_ids localities survive as nothing
    # but event identities a later reader would have to re-derive.
    input_localities: tuple[str | None, ...]
    # Preserved occurrences the measurement ran over. The denominator.
    occurrences_examined: int
    # How many of them carried the representation at least once.
    occurrences_carrying: int
    # How many times it occurred in total across them. This is the recurrence.
    total_count: int
    input_event_ids: tuple[str, ...]
    # Where the measured material came from. Defaults to the weaker Assertion:
    # a finding that did not read from a ledger cannot say it measured
    # preserved material, and silence must not read as the stronger one.
    material_provenance: str = MATERIAL_AS_SUPPLIED
    # The basis of the population input_ids, where one was declared. Every
    # finding of one pass stands on the same population, so preserving the
    # enumeration in each copies that population once per representation.
    # `#2486` measured exactly this at 97% of a stored finding and built
    # SupportBasis to carry the basis instead. This path was written without
    # it and measured 96.8% on 500 findings over 2,000 occurrences.
    support_basis: SupportBasis | None = None
    # Which preserved production evidence concerns this result. Named for the
    # evidence rather than for a production occurrence: it holds an occurrence reference,
    # and the production occurrence stays unestablished. `produced_by` said otherwise by
    # ordinary reading while the payload beside it said unestablished. The
    # production branches in the Book HEAD
    # holds that a separately constructed representation with identical fields
    # does not carry the witnessed return's standing "unless that standing is
    # separately represented or preserved". Content equality cannot supply it:
    # an identical validation has identical content by definition, which is
    # exactly the case the relation must distinguish. So the relation travels
    # with the result rather than being validated later by matching bytes.
    #
    # A later representation carrying this same reference is another
    # representation of the same produced result, which is lawful. One carrying
    # none is a representation of nothing produced.
    production_evidence_id: str | None = None
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
            "input_localities": list(self.input_localities),
            "occurrences_examined": self.occurrences_examined,
            "occurrences_carrying": self.occurrences_carrying,
            "total_count": self.total_count,
            "input_event_ids": list(self.input_event_ids),
            "input_count": len(self.input_event_ids),
            "boundary_notes": list(self.boundary_notes),
            "production_evidence_id": self.production_evidence_id,
        }
        if self.support_basis is not None:
            # The basis replaces the enumeration rather than accompanying it.
            # Carrying both preserves the cost the basis exists to avoid, and
            # leaves two representations of one support free to disagree.
            carried["input_support"] = self.support_basis.to_json_dict()
            carried.pop("input_event_ids")
        return carried


def measure_recurrence(
    occurrences: Iterable[Event],
    *,
    declared: DeclaredMeasurement,
    occurrences_of: "callable[[str], int]",
    preserved_in: EventLedger | None = None,
    produce_in: "tuple[EventLedger, str, str] | None" = None,
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

    input_ids: list[str] = []
    localities: dict[str | None, None] = {}
    examined = 0
    carrying = 0
    total = 0
    walked, material_provenance = _as_preserved(
        _distinct_population(occurrences), preserved_in
    )
    for event in walked:
        text = _measurable_text(event)
        input_ids.append(event.id)
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
    finding = RecurrenceFinding(
        declared=declared,
        material_provenance=material_provenance,
        input_localities=tuple(localities),
        occurrences_examined=examined,
        occurrences_carrying=carrying,
        total_count=total,
        input_event_ids=tuple(input_ids),
    )
    if produce_in is not None:
        evidence = _record_production(
            produce_in[0],
            workspace_id=produce_in[1],
            session_id=produce_in[2],
            finding=finding,
        )
        finding = replace(finding, production_evidence_id=evidence.id)
    return finding


def _locality_of(event: Event) -> str | None:
    """The locality this occurrence carries, or nothing where it carries none.

    `06.Standing.B` holds that occurrences *may* carry a bounded locality
    coordinate. Where one is not carried, this returns ``None``, and a finding
    records that absence rather than a value standing in for it.

    An earlier version rendered a missing `session_id` as ``session:None``, and
    the version after it returned ``workspace:w``. Both replaced an absent
    coordinate with an asserted one: the first invented a locality named None,
    the second answered the locality question with the workspace, which
    `06.Standing.A` lists as a different member of the same boundary. Same
    workspace does not mean same locality, so the workspace cannot stand in for
    a locality that was not carried.
    """

    if event.session_id is None:
        return None
    return f"workspace:{event.workspace_id};session:{event.session_id}"


def _distinct_population(occurrences: Iterable[Event]) -> list[Event]:
    """The occurrences to measure, refusing a repeated occurrence identity.

    The rule is not `01.Source:28`, which requires the bounded scope to be
    disclosed and says nothing about identity-distinctness. It comes from what
    ``occurrences_examined`` asserts: a number of occurrences. One preserved
    occurrence referenced twice is one occurrence, so counting it twice reports
    a population larger than the one that exists, and every count drawn from it
    carries that inflation.

    Refused rather than deduplicated. Silently collapsing would decide that the
    caller meant one, and refusing rather than pretending is the same choice
    this module makes about material it cannot measure.

    `01.Source.E.1` establishes the rule: each counted occurrence is
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


def _as_preserved(
    population: "list[Event]", ledger: EventLedger | None
) -> "tuple[list[Event], str]":
    """The preserved occurrences these identities name, where a ledger says so.

    An `Event` is directly constructible with any id and any payload, so an
    object bearing a preserved identity may carry different material. Checking
    that an occurrence with that identity exists establishes the identity and
    not the material: `#2510` closed this where a support basis was declared,
    by reading the occurrence rather than trusting the object, and every other
    path kept trusting the object.

    Where a ledger is supplied the material is read from it. Where none is, the
    act measures what it was given and cannot state that it measured preserved
    material -- which is a limit on the finding, not a permission.
    """

    if ledger is None:
        return population, MATERIAL_AS_SUPPLIED
    preserved = []
    for event in population:
        recorded = ledger.get(event.id)
        if recorded is None:
            raise PreservedMaterialMeasurementError(
                f"{event.id} is not preserved in the ledger this measurement "
                "reads its material from"
            )
        preserved.append(recorded)
    return preserved, MATERIAL_READ_FROM_LEDGER


def _additive_only(
    finding, carried: dict[str, Any], extra: dict[str, Any] | None
) -> dict[str, Any]:
    """Recording coordinates, refused where they collide with reserved ones.

    Merging `extra` last let a caller record ``extra={"total_count": 999}`` over
    a produced count of three, so the durable result was one no act produced.
    Filtering silently was the first repair and was also wrong: a caller asked
    to record one thing and the recorder recorded another without saying so.

    Checking only the finding's own keys was the second, and left the way in
    open. ``extra={"dimensions": {"identity": "x"}}`` collided with nothing the
    finding carries, then replaced the whole dimensions object -- erasing the
    measurement's source provenance, standing and authority by omission rather
    than by contradiction. `mutates_cluster` and `unknowns` were reachable the
    same way, and `provenance_occurrence_refs`, written after `extra`, was
    silently discarded.

    So the rule is the whole recorded payload, not part of it: recording may
    add a coordinate this payload does not already carry, and may not replace
    one. Refusal rather than silent handling in either direction.

    Recurrence only. The result-Assertion path composes its own dimensions
    through `extra` by design, and refusing that is a migration rather than a
    repair.
    """

    if not extra:
        return {}
    reserved = set(carried)
    if isinstance(finding, RecurrenceFinding):
        reserved |= _RESERVED_RECORDING_COORDINATES
    collisions = sorted(set(extra) & reserved)
    if collisions:
        raise PreservedMaterialMeasurementError(
            "recording may add coordinates and may not replace ones already "
            f"recorded: {', '.join(collisions)}"
        )
    return dict(extra)


def _produced_content(finding) -> dict[str, Any]:
    """Everything the measuring act established about its own result.

    Not `to_json_dict()`. That representation deliberately omits
    `material_provenance`, which is stated once by the recorder, so a
    commitment taken over it cannot tell a result produced over ledger-read
    material from one produced over supplied material -- the coordinate
    `#2516` exists to keep. Every carried coordinate is included here,
    `boundary_notes` among them.
    """

    content = dict(finding.to_json_dict())
    content["material_provenance"] = getattr(
        finding, "material_provenance", MATERIAL_AS_SUPPLIED
    )
    # The reference to the production evidence is not part of the content that
    # evidence commits to; it is how a result says which evidence concerns it.
    content.pop("production_evidence_id", None)
    return content


def _production_commitment(finding) -> str:
    """A commitment over the content above, so any change to it is a change."""

    return _production_content_commitment(
        MEASUREMENT_CONVENTION, _produced_content(finding)
    )


def _recorded_production_commitment(
    recorded: Event, production_coordinates: tuple[str, ...]
) -> str:
    """The production commitment a recorded finding's own content implies.

    The production evidence names the exact top-level coordinates the act
    produced. Recording may lawfully add other coordinates, so neither an
    exclusion list nor every key left in the recorded payload reconstructs this
    boundary. `material_provenance` is the one produced coordinate represented
    inside the recorder-established dimensions object.
    """

    payload = recorded.payload
    content: dict[str, Any] = {}
    for key in production_coordinates:
        if key == "material_provenance":
            dimensions = payload.get("dimensions")
            if (
                not isinstance(dimensions, dict)
                or "source_provenance" not in dimensions
            ):
                raise PreservedMaterialMeasurementError(
                    "the recorded finding does not preserve its produced "
                    "material provenance"
                )
            content[key] = dimensions["source_provenance"]
        elif key not in payload:
            raise PreservedMaterialMeasurementError(
                f"the recorded finding does not preserve produced coordinate {key}"
            )
        else:
            content[key] = payload[key]
    return _production_content_commitment(MEASUREMENT_CONVENTION, content)


def _record_production(
    ledger: EventLedger, *, workspace_id: str, session_id: str, finding
) -> Event:
    """Preserve, from inside the producing act, that it produced this result.

    The distinction is not that this is private. Privacy is mechanics. It is
    that production standing is preserved at the producing boundary, and
    the result carries the relation to it — so a separately constructed
    representation with identical fields carries no such relation, which is the
    direct-instantiation counterexample states. An earlier attempt exposed this
    publicly, which made it a second recorder: a caller holding any object could
    record a production over it, establishing only that a caller possessed
    something and called a function.

    What this establishes, and what it does not:

    ```text
      established   this measuring act produced this exact result
      not           who is authorized to perform it
      not           which responsible boundary bears the production Responsibility
      not           that nothing else appended this kind directly
    ```

    The second and third are the production-occurrence crossing and stay
    unestablished; the payload records them as such rather than filling them. The
    fourth is true of every kind in this ledger.

    This occurrence is preserved evidence concerning a production. It is not
    the production occurrence by identity.
    """

    return _record_production_evidence(
        ledger,
        workspace_id=workspace_id,
        session_id=session_id,
        convention=MEASUREMENT_CONVENTION,
        producing_act="declared Measurement",
        produced_result_kind=RECURRENCE_RESULT_KIND,
        result_identity=finding.declared.representation_measured,
        produced_content=_produced_content(finding),
        responsibility=RESPONSIBILITY_UNESTABLISHED,
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
    if "decoded_text" not in event.payload:
        # The occurrence says a text representation was formed and carries no
        # decoded text. That is incoherent material, and reading the coordinate
        # and trusting it would rest the finding on a Assertion about the material
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
    preserved_in: EventLedger | None = None,
    produce_in: "tuple[EventLedger, str, str] | None" = None,
    support_basis: SupportBasis | None = None,
    support_validator: SupportValidator | None = None,
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
    representation. Each carries its own declaration, the same input_ids
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
        # One pass has as input one population, so every finding it produces
        # receives that population. A declaration disclosing a different
        # counting scope would have its scope assertion preserved beside a
        # population the act did not draw from it. `01.Source:28` requires
        # the disclosed scope to be the scope within which occurrences were
        # counted, so the disagreement is refused rather than reconciled.
        raise PreservedMaterialMeasurementError(
            "one pass has as input one population, so every declaration must "
            f"disclose the same counting scope; got {len(scopes)}"
        )
    input_ids: list[str] = []
    localities: dict[str | None, None] = {}
    examined = 0
    carrying: dict[str, int] = {name: 0 for name in declared}
    total: dict[str, int] = {name: 0 for name in declared}
    walked, material_provenance = _as_preserved(
        _distinct_population(occurrences), preserved_in
    )
    if support_basis is not None and support_validator is not None:
        # A finding asserting support from preserved occurrences must have
        # measured the material those occurrences carry. An `Event` can be
        # constructed directly with any id and any payload, so a caller could
        # hand this act an object bearing a validated identity and different
        # text: the identities would commit correctly, the basis would reconstruct,
        # and the finding would preserve a basis for material it never saw.
        #
        # So where a basis is declared, the material is read from the ledger
        # the basis is validated against. The supplied objects still determine
        # which occurrences participate and in what order; they do not supply
        # what was measured.
        # This read establishes the same provenance `_as_preserved` does, so
        # the finding must carry it. Without this the basis path recorded
        # material as supplied while having read every occurrence from the
        # ledger -- erasing an established provenance rather than inventing an
        # unestablished one, which is the same defect facing the other way.
        material_provenance = MATERIAL_READ_FROM_LEDGER
        preserved = []
        for event in walked:
            recorded = support_validator.ledger.get(event.id)
            if recorded is None:
                raise PreservedMaterialMeasurementError(
                    f"{event.id} is not preserved in the ledger this support "
                    "basis is validated against"
                )
            preserved.append(recorded)
        walked = preserved
    for event in walked:
        text = _measurable_text(event)
        input_ids.append(event.id)
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
    population = tuple(input_ids)
    input_localities = tuple(localities)
    if support_basis is not None:
        # A basis carried but never checked would let a finding preserve a
        # commitment to a population the act did not walk. `support_commitment`
        # is a pure function of the rule and the ordered identities, so the act
        # can confirm the basis commits to what it actually input_ids.
        if support_commitment(support_basis.selection_rule, population) != (
            support_basis.commitment
        ):
            raise PreservedMaterialMeasurementError(
                "the declared support basis does not commit to the population "
                "this measurement input_ids"
            )
        if support_basis.support_count != len(population):
            raise PreservedMaterialMeasurementError(
                f"the declared support basis counts {support_basis.support_count} "
                f"occurrences and this measurement input_ids {len(population)}"
            )
        # Committing to the identities is not describing the population. The
        # commitment is a digest over the rule and the ordered ids and says
        # nothing about scope, so a basis declaring one locality could be
        # accepted for a population drawn from several: the ids match, and the
        # preserved basis then asserts a scope the act never input_ids within.
        # The producing act refuses that now; a later validation failure is a
        # different responsibility and arrives too late to prevent it.
        declared_locality = (
            f"workspace:{support_basis.workspace_id};"
            f"session:{support_basis.session_id}"
        )
        if input_localities != (declared_locality,):
            raise PreservedMaterialMeasurementError(
                f"the declared support basis is scoped to {declared_locality} "
                f"and this measurement input_ids {list(input_localities)}"
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
        # only that the population is *within* that description. A
        # caller supplying three of four occurrences through the same boundary
        # would pass all of them, and the finding would then preserve a basis
        # asserting completeness the act never established.
        #
        # Verifying that requires interpreting the boundary, which only an
        # EventLedger does, so a basis is accepted only where the act is given
        # the means to check it. Implementation inconvenience does not move the
        # obligation to a later reader: once the enumeration is replaced, a
        # validation discovering the lie arrives after the false basis is
        # preserved.
        if support_validator is None:
            raise PreservedMaterialMeasurementError(
                "a support basis declares a selection through a boundary, and "
                "accepting one requires a SupportValidator to establish that "
                "the population is that selection"
            )
        # `reconstruct` performs the basis's own selection through the boundary and
        # refuses unless the result reproduces the committed digest. Together
        # with the commitment check above -- which ties the population walked to
        # that same digest -- the population is the selection declared.
        #
        # A third comparison of the two results was written here and removed: it
        # cannot fail while both checks hold, and mutation testing found no test
        # that could reach it. A guard nothing can reach reads as a proof and is
        # not one.
        support_validator.validate(support_basis)
    findings = tuple(
        RecurrenceFinding(
            declared=declaration,
            material_provenance=material_provenance,
            input_localities=input_localities,
            occurrences_examined=examined,
            occurrences_carrying=carrying[representation],
            total_count=total[representation],
            input_event_ids=population,
            support_basis=support_basis,
        )
        for representation, declaration in declared.items()
    )
    if produce_in is not None:
        # Every result is fixed before any evidence is preserved. Preserving
        # one at a time would let evidence for the first survive a failure
        # while measuring the rest, and that evidence would concern a result
        # this act had not finished producing.
        #
        # The evidence is still appended one at a time, so a later append
        # failing leaves earlier evidence preserved while this call returns
        # nothing. That evidence is not wrong: those results were produced at
        # this boundary, and the Assertion it carries says produced rather than
        # returned for exactly this reason. Making the appends atomic would
        # let it Assertion the stronger thing, and is not done here.
        witnessed = []
        for finding in findings:
            evidence = _record_production(
                produce_in[0],
                workspace_id=produce_in[1],
                session_id=produce_in[2],
                finding=finding,
            )
            witnessed.append(replace(finding, production_evidence_id=evidence.id))
        findings = tuple(witnessed)
    return findings


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
    preserved_in: EventLedger | None = None,
) -> MeasurementFinding:
    """Count which representations occupy a position across preserved material.

    ``occupant_of`` receives one preserved representation and returns the
    representation occupying the measured position within it, or ``None`` when
    that occurrence has no such position. It performs no interpretation; a
    position that is absent is absent, not Unknown.
    """

    counts: dict[str, int] = {}
    input_ids: list[str] = []
    measured = 0
    walked, material_provenance = _as_preserved(
        _distinct_population(occurrences), preserved_in
    )
    for event in walked:
        text = _measurable_text(event)
        input_ids.append(event.id)
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
        material_provenance=material_provenance,
        positions_measured=measured,
        occupancies=ordered,
        input_event_ids=tuple(input_ids),
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
        # A result Assertion carries a reconstructible support basis, so the
        # enumeration it replaces is not written beside it. `#2486` measured
        # the enumeration at 97% of a 4,000-line finding.
        carried["input_support"] = basis
        carried.pop("input_event_ids", None)
    return {
        "dimensions": {
            "identity": f"measurement:{finding.declared.representation_measured}",
            "content": finding.declared.counting_scope,
            "standing": "measured",
            # Stated from the finding rather than asserted here. The measuring
            # act knows whether it read its material from a ledger, and this
            # said "preserved operator-ingress occurrences" for every finding
            # regardless -- inventing a provenance the act had declined.
            "source_provenance": getattr(
                finding, "material_provenance", MATERIAL_AS_SUPPLIED
            ),
            # Not derived from the provenance. An earlier version made this
            # follow material_provenance, which compresses two coordinates
            # `#2439` had just separated and mints the sibling of a string
            # `#2431` had already called contamination. Where the material came
            # from and which responsible boundary bears the production Responsibility are
            # different questions, and only the first has been validated.
            "responsibility": RESPONSIBILITY_UNESTABLISHED,
            "authority": (
                "measurement evidence only; establishes no represented relation, relation, "
                "or standing beyond the measurement assertion"
            ),
            "scope_locality": f"workspace:{workspace_id};session:{session_id}",
            "occurrence_preservation": "declared measurement durably recorded",
        },
        "mutates_cluster": False,
        "unknowns": ["what any measured representation means remains Unknown"],
        **carried,
        **_additive_only(finding, carried, extra),
        "provenance_occurrence_refs": (
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
    # Every recorded finding states `source_provenance` as "preserved
    # operator-ingress occurrences". Premises were established here and the
    # occurrences that Assertion were made about never were, so a finding measured
    # over directly constructed `Event` objects recorded that provenance about
    # material this ledger does not hold. `#2510` closed that at the input
    # boundary only where a support basis was declared; a measurement without
    # one reached the recorder unchecked.
    #
    # An earlier version exempted findings carrying a support basis, calling
    # them verified. Carrying a basis is not being verified against one: both
    # `RecurrenceFinding` and `SupportBasis` are directly constructible, and a
    # finding verified against one ledger may be handed to another. This
    # function has no witness for either, so it exempts nothing.
    #
    # Identities are collected across the whole call before any read, because
    # every finding of one pass carries the same population and checking per
    # finding would restore the cost `#2486` removed.
    input_ids = {
        event_id
        for finding, _ in supplied
        for event_id in finding.input_event_ids
    }
    for event_id in input_ids:
        occurrence = ledger.get(event_id)
        if occurrence is None or occurrence.kind != INGRESS_OCCURRED_KIND:
            raise PreservedMaterialMeasurementError(
                f"{event_id} is recorded as a input_ids preserved occurrence "
                "and this ledger preserves no such ingress occurrence"
            )
    # A recurrence finding is recordable where the act that produced it
    # preserved evidence of doing so. Read across the workspace, since
    # `06.Standing.B` makes producing in one locality and recording in another
    # lawful. Required on this path only: every positional caller records
    # without a production witness, and adopting it there is its own migration.
    for finding, _ in supplied:
        if not isinstance(finding, RecurrenceFinding):
            continue
        if finding.production_evidence_id is None:
            raise PreservedMaterialMeasurementError(
                "this result names no production evidence; a measuring act "
                "preserves that evidence and the result it returns carries it"
            )
        evidence = ledger.get(finding.production_evidence_id)
        if evidence is None or evidence.kind != PRODUCTION_EVIDENCE_KIND:
            raise PreservedMaterialMeasurementError(
                f"{finding.production_evidence_id} is named as this result's "
                "evidence and is not preserved production evidence"
            )
        if evidence.workspace_id != workspace_id:
            raise PreservedMaterialMeasurementError(
                "production evidence and its recorded recurrence finding must "
                "belong to the same workspace"
            )
        if evidence.payload.get("produced_result_kind") != RECURRENCE_RESULT_KIND:
            raise PreservedMaterialMeasurementError(
                f"{finding.production_evidence_id} is production evidence for "
                "a different kind of result"
            )
        if evidence.payload.get("production_convention") != MEASUREMENT_CONVENTION:
            raise PreservedMaterialMeasurementError(
                f"{finding.production_evidence_id} is production evidence "
                "under a different production convention"
            )
        if evidence.payload["production_commitment"] != _production_commitment(
            finding
        ):
            raise PreservedMaterialMeasurementError(
                "the production evidence this result names concerns a "
                "different result"
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
    """Preserve a finding so a later responsible act may have it participate.

    The recorded authority states the clause's own limit. A finding is
    measurement evidence and is not relation, represented relation, or established standing.
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
    recorded premise findings one finding stood on, validated nearest premise
    first. It preserves that dependency relation and asserts nothing about the
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
