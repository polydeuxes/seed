"""Declared measurement over preserved operator-ingest occurrences.

`01.Source.E` is titled *Measurement and recurrence do not establish represented relation*,
and `01.Source:28` grants the finding and states its conditions:

    A declared measurement may yield bounded findings of exact equality,
    count, recurrence, prefix occurrence, the result of a declared predicate,
    or adjacency within its measurement boundary. Those findings do not
    establish structural, grammatical, or semantic represented relation, or constitutional
    standing beyond the measurement assertion. A recurrence assertion must
    disclose the representation or representation measured, the rule by which
    equivalence or sameness was determined, and the bounded scope within which
    occurrences were counted.

Those three disclosures are required fields here, not commentary.

**What this is for is Seed's own preserved material.** Occurrences recorded
through operator ingest carry occurrence-only Evidence while the represented relation
remains ``Unknown``,
and read a file directly and measuring it yields a result that vanishes
with the process and that no later act can have as input; `#2368` did that and it was
withdrawn.

A measurement given a ledger reads its material from that ledger. A measurement
given occurrences measures what it was handed, which is lawful and weaker: the
finding then says its material was supplied rather than preserved, and the two
asserts are recorded distinctly. This module used to describe only the first
while doing both.

**What this yields is recorded.** Each finding is appended to the ledger, so a
later responsible act may have it participate. `01.Standing.E` permits exactly that: a
bounded comparison may have as input preserved findings "only while preserving each
input source coordinates, provenance, support support, subject, scope, authority,
confidence or uncertainty, Unknowns, standing, and forbidden inferences".

**A finding may stand on an earlier finding.** `premise_event_identity` records which,
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
from seed_runtime.material_ingest import MATERIAL_INGEST_OCCURRED_KIND
from seed_runtime.identities import new_identity
from seed_runtime.yield_evidence import (
    YIELD_EVIDENCE_KIND,
    _record_yield_evidence,
)
from seed_runtime.input_support import (
    InputSupport,
    InputSupportValidator,
)

MEASUREMENT_RECORDED_KIND = "operator.measurement.finding_recorded"
INGEST_OCCURRED_KIND = MATERIAL_INGEST_OCCURRED_KIND
RECURRENCE_RESULT_KIND = "recurrence Measurement finding"

# What a finding may say about where the material it measured came from. The
# measuring act knows which of these is true and nothing carried it forward, so
# recording stated the stronger one for every finding. A measurement given a
# ledger reads its material from that ledger; a measurement given occurrences
# measures what it was handed, and no later act can establish that those
# objects carried what the preserved occurrences of the same identity carry.
MATERIAL_READ_FROM_LEDGER = "preserved operator-ingest occurrences"
MATERIAL_AS_SUPPLIED = (
    "occurrences as supplied to this measurement, not read from a ledger"
)

# `#2431` identified "declared-measurement-over-preserved-material" as inherited
# contamination: it wrote the Act into the Responsibility slot for a declared
# measurement whose exact Measurement Responsibility had never been validated. `#2439`
# then validated the partial shape and kept it partial -- boundary participant "this Seed",
# Act a declared measurement, Standing measured, and a Responsibility that stays
# unestablished. That is ordinary rather than contradictory.
RESPONSIBILITY_UNESTABLISHED = "unestablished"

# What recording composes around a finding's own content. A caller adding to a
# recorded finding may not replace any of it.
_RESERVED_RECORDING_COORDINATES = frozenset(
    {"dimensions", "unknowns", "provenance_occurrence_references"}
)

LIMITS: tuple[str, ...] = (
    "A finding reports a count within its stated scope and nothing further.",
    "Recurrence establishes that a representation occurs more than once only.",
    "A highest-count occupant of a position is not the represented relation of that position.",
    "Co-presence of representations establishes no relation (01.Standing.D).",
    "A finding standing on a premise is not stronger than a finding without one.",
    "The premise is preserved so the finding cannot be read independently of it.",
    "This yields no represented relation, relation, truth, applicability, or admission.",
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
    premise_event_identity: str | None = None
    # The representation this measurement measured relative to, when it had
    # one.  A finding can only supply an representation to a later measurement if it
    # records the representation it used, so this is what makes a finding
    # representation-supplying rather than merely informative.
    measured_after: str | None = None
    # The positional Measurement distinction, and the exact representations it
    # was performed relative to. Without these a finding says what it found but
    # not what distinction yielded it, so a later distinction would require a
    # reader to restate the first. These
    # are exact strings taken from preserved material; neither names a kind.
    distinction: str | None = None
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
    # The identities this measurement input_identities, available while the act runs.
    # On the result-Assertion path a addressable support support is supplied from
    # these inputs instead of preserving the enumeration in every result;
    # the support belongs to that path, and this dataclass does not own a second
    # coordinate for it. `#2486` measured why: copying the inputs into
    # every finding of a body cost 97% of the stored finding.
    input_event_identities: tuple[str, ...]
    downstream_act_identity: str = field(
        default_factory=lambda: new_identity("preserved_material_measurement_act"),
        compare=False,
    )
    act_occurrence_identity: str = field(
        default_factory=lambda: new_identity("preserved_material_measurement_occurrence"),
        compare=False,
    )
    # Where the measured material came from. Defaults to the weaker Assertion:
    # a finding that did not read from a ledger cannot say it measured
    # preserved material, and silence must not read as the stronger one.
    material_provenance: str = MATERIAL_AS_SUPPLIED
    limits: tuple[str, ...] = field(default=LIMITS)

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
            "representation_measured": self.declared.representation_measured,
            "equivalence_rule": self.declared.equivalence_rule,
            "counting_scope": self.declared.counting_scope,
            "premise_event_identity": self.declared.premise_event_identity,
            "measured_left_representation": self.declared.measured_after,
            "measurement_distinction": self.declared.distinction,
            "measured_relative_to": list(self.declared.relative_to),
            "measured_position": self.declared.measured_position,
            "positions_measured": self.positions_measured,
            "occupancies": [
                {"representation": o.representation, "occurrence_count": o.occurrence_count}
                for o in self.occupancies
            ],
            # Not "input_support": the result-Assertion coordinate surface carries
            # that key and its fields are merged over this dict, so naming both
            # the same silently replaced one with the other.
            "input_event_identities": list(self.input_event_identities),
            "input_count": len(self.input_event_identities),
            "limits": list(self.limits),
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
    # The localities the input_identities occurrences carried. `06.Standing.B` requires
    # an act material participating in an Act distinguished by locality to preserve the
    # locality of what it input_identities, and to keep that distinct from the locality
    # it records into. `None` in this tuple is an occurrence that carried no
    # locality, preserved rather than filled in.
    # Recording stamps the recording locality; without this
    # coordinate a finding drawn from two localities and recorded into a third
    # asserts only the third, and the input_identities localities survive as nothing
    # but event identities a later reader would have to re-derive.
    input_localities: tuple[str | None, ...]
    # Preserved occurrences the measurement ran over. The denominator.
    occurrences_examined: int
    # How many of them carried the representation at least once.
    occurrences_carrying: int
    # How many times it occurred in total across them. This is the recurrence.
    total_count: int
    input_event_identities: tuple[str, ...]
    downstream_act_identity: str = field(
        default_factory=lambda: new_identity("preserved_recurrence_measurement_act"),
        compare=False,
    )
    act_occurrence_identity: str = field(
        default_factory=lambda: new_identity("preserved_recurrence_measurement_occurrence"),
        compare=False,
    )
    # Where the measured material came from. Defaults to the weaker Assertion:
    # a finding that did not read from a ledger cannot say it measured
    # preserved material, and silence must not read as the stronger one.
    material_provenance: str = MATERIAL_AS_SUPPLIED
    # The support of the inputs input_identities, where one was declared. Every
    # finding of one pass stands on the same inputs, so preserving the
    # enumeration in each copies that inputs once per representation.
    # `#2486` measured exactly this at 97% of a stored finding and built
    # InputSupport to carry the support instead. This path was written without
    # it and measured 96.8% on 500 findings over 2,000 occurrences.
    input_support: InputSupport | None = None
    # Which preserved Evidence concerns this result's exact Yield edge. The
    # Evidence reference is neither the edge nor its Act occurrence by identity.
    # holds that a separately supplied representation with identical fields
    # does not carry the witnessed return's standing "unless that standing is
    # separately represented or preserved". Content equality cannot supply it:
    # an identical validation has identical content by definition, which is
    # exactly the case the relation must distinguish. So the relation travels
    # with the result rather than being validated later by matching bytes.
    #
    # A later representation carrying this same reference is another
    # representation of the same yielded result, which is lawful. One carrying
    # none is a representation of nothing yielded.
    yield_evidence_identity: str | None = None
    limits: tuple[str, ...] = field(default=LIMITS)

    def to_json_dict(self) -> dict[str, Any]:
        carried: dict[str, Any] = {
            "representation_measured": self.declared.representation_measured,
            "equivalence_rule": self.declared.equivalence_rule,
            "counting_scope": self.declared.counting_scope,
            "premise_event_identity": self.declared.premise_event_identity,
            "measurement_distinction": "recurrence",
            "input_localities": list(self.input_localities),
            "occurrences_examined": self.occurrences_examined,
            "occurrences_carrying": self.occurrences_carrying,
            "total_count": self.total_count,
            "input_event_identities": list(self.input_event_identities),
            "input_count": len(self.input_event_identities),
            "limits": list(self.limits),
            "yield_evidence_identity": self.yield_evidence_identity,
        }
        if self.input_support is not None:
            # The support replaces the enumeration rather than accompanying it.
            # Carrying both preserves the cost the support exists to avoid, and
            # leaves two representations of one support free to disagree.
            carried["input_support"] = self.input_support.to_json_dict()
            carried.pop("input_event_identities")
        return carried


def measure_recurrence(
    occurrences: Iterable[Event],
    *,
    declared: DeclaredMeasurement,
    occurrences_of: "callable[[str], int]",
    preserved_in: EventLedger | None = None,
    yield_in: "tuple[EventLedger, str] | None" = None,
) -> RecurrenceFinding:
    """Count how often one representation occurs across preserved material.

    ``occurrences_of`` receives one preserved representation and returns how
    many times the measured representation occurs within it under the declared
    equivalence rule. The rule decides what counts as an occurrence, so the
    caller supplies it and this act performs no read: a
    representation that does not occur occurs zero times, which is a finding
    and not an absence of one.

    Refuses the same material `measure_occupancy` refuses, for the same reason.
    A measurement over bounded inputs cannot measure text in material
    that has none, and skipping would silently narrow the scope the finding
    goes on to disclose.
    """

    input_identities: list[str] = []
    localities: dict[str | None, None] = {}
    examined = 0
    carrying = 0
    total = 0
    walked, material_provenance = _as_preserved(
        _distinct_inputs(occurrences), preserved_in
    )
    for event in walked:
        text = _measurable_text(event)
        input_identities.append(event.identity)
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
        input_event_identities=tuple(input_identities),
    )
    if yield_in is not None:
        evidence = _record_yield(
            yield_in[0],
            locality_identity=yield_in[1],
            finding=finding,
        )
        finding = replace(finding, yield_evidence_identity=evidence.identity)
    return finding


def _locality_of(event: Event) -> str | None:
    """The locality this occurrence carries, or nothing where it carries none.

    `06.Standing.B` holds that occurrences *may* carry a bounded locality
    coordinate. Where one is not carried, this returns ``None``, and a finding
    records that absence rather than a value standing in for it.

    """

    if event.locality_identity is None:
        return None
    return f"locality:{event.locality_identity}"


def _distinct_inputs(occurrences: Iterable[Event]) -> list[Event]:
    """The occurrences to measure, refusing a repeated occurrence identity.

    The rule is not `01.Source:28`, which requires the bounded scope to be
    disclosed and says nothing about identity-distinctness. It comes from what
    ``occurrences_examined`` asserts: a number of occurrences. One preserved
    occurrence referenced twice is one occurrence, so counting it twice reports
    a inputs larger than the one that exists, and every count drawn from it
    carries that inflation.

    Refused rather than deduplicated. Silently collapsing would decide that the
    caller meant one. The same refusal applies to material this Act cannot
    measure.

    `01.Source.E.1` establishes the rule: each counted occurrence is
    distinguished by exact occurrence identity, and repeated reference to one
    preserved occurrence does not establish another. That clause was added
    because this refusal had nothing behind it.
    """

    inputs = list(occurrences)
    seen: set[str] = set()
    for event in inputs:
        if event.identity in seen:
            raise PreservedMaterialMeasurementError(
                f"{event.identity} appears more than once in one measured inputs"
            )
        seen.add(event.identity)
    return inputs


def _as_preserved(
    inputs: "list[Event]", ledger: EventLedger | None
) -> "tuple[list[Event], str]":
    """The preserved occurrences these identities name, where a ledger says so.

    An `Event` is directly formable with any identity and any material, so an
    object bearing a preserved identity may carry different material. Checking
    that an occurrence with that identity exists establishes the identity and
    not the material: `#2510` enforced this where a support support was declared,
    by read the occurrence rather than trusting the object, and every other
    path kept trusting the object.

    Where a ledger is supplied the material is read from it. Where none is, the
    act measures what it was given and cannot state that it measured preserved
    material -- which is a limit on the finding, not a license.
    """

    if ledger is None:
        return inputs, MATERIAL_AS_SUPPLIED
    preserved = []
    for event in inputs:
        recorded = ledger.get(event.identity)
        if recorded is None:
            raise PreservedMaterialMeasurementError(
                f"{event.identity} is not preserved in the ledger this measurement "
                "reads its material from"
            )
        preserved.append(recorded)
    return preserved, MATERIAL_READ_FROM_LEDGER


def _additive_only(
    finding, carried: dict[str, Any], extra: dict[str, Any] | None
) -> dict[str, Any]:
    """Refuse additions that replace a carried recording coordinate."""

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


def _result_content(finding) -> dict[str, Any]:
    """Everything the measuring act established about its own result.

    Not `to_json_dict()`. That representation deliberately omits
    `material_provenance`, which is stated once by the recorder, so a
    commitment taken over it cannot tell a result yielded over ledger-read
    material from one yielded over supplied material -- the coordinate
    `#2516` exists to keep. Every carried coordinate is included here,
    `limits` among them.
    """

    content = dict(finding.to_json_dict())
    content["material_provenance"] = getattr(
        finding, "material_provenance", MATERIAL_AS_SUPPLIED
    )
    # The reference to the yield evidence is not part of the content that
    # evidence commits to; it is how a result says which evidence concerns it.
    content.pop("yield_evidence_identity", None)
    return content


def _recorded_yield_result(
    recorded: Event, yield_coordinates: tuple[str, ...]
) -> dict[str, Any]:
    """Read the exact Yield coordinates from one recorded finding.

    The yield evidence names the exact top-level coordinates the act
    yielded. Recording may lawfully add other coordinates, so neither an
    exclusion list nor every key left in the recorded material reads this
    boundary. `material_provenance` is the one yielded coordinate represented
    inside the recorder-established dimensions object.
    """

    material = recorded.material
    content: dict[str, Any] = {}
    for key in yield_coordinates:
        if key == "material_provenance":
            dimensions = material.get("dimensions")
            if (
                not isinstance(dimensions, dict)
                or "source_provenance" not in dimensions
            ):
                raise PreservedMaterialMeasurementError(
                    "the recorded finding does not preserve its yielded "
                    "material provenance"
                )
            content[key] = dimensions["source_provenance"]
        elif key not in material:
            raise PreservedMaterialMeasurementError(
                f"the recorded finding does not preserve yielded coordinate {key}"
            )
        else:
            content[key] = material[key]
    return content


def _record_yield(ledger: EventLedger, *, locality_identity: str, finding) -> Event:
    """Preserve, from inside the yielding act, that it yielded this result.

    The distinction is not that this is private. Privacy is mechanics. It is
    that Standing concerning the occurrence-to-result edge is preserved at the
    exact Act boundary, and
    the result carries the relation to it — so a separately supplied
    representation with identical fields carries no such relation, which is the
    direct-instantiation counterexample states. An earlier attempt exposed this
    publicly, which made it a second recorder: a caller holding any object could
    record a yield over it, establishing only that a caller possessed
    something and called a function.

    What this establishes, and what it does not:

    ```text
      established   this measuring act yielded this exact result
      not           who is authorized to perform it
      not           which responsible boundary bears the Measurement Responsibility
      not           that nothing else appended this kind directly
    ```

    The three negative coordinates stay unestablished; the material records them
    as such rather than filling them.

    This occurrence is preserved Evidence concerning a Yield edge. It is not
    that edge or its Act occurrence by identity.
    """

    return _record_yield_evidence(
        ledger,
        locality_identity=locality_identity,
        exact_act="declared Measurement",
        act_occurrence_identity=finding.act_occurrence_identity,
        result_kind=RECURRENCE_RESULT_KIND,
        result_identity=finding.declared.representation_measured,
        result_content=_result_content(finding),
        responsibility=RESPONSIBILITY_UNESTABLISHED,
        live_boundary="preserved_material_measurement",
        recorded_result_coordinates={
            coordinate: (
                ("dimensions", "source_provenance")
                if coordinate == "material_provenance"
                else (coordinate,)
            )
            for coordinate in _result_content(finding)
        },
    )


def _measurable_text(event: Event) -> str:
    """The represented material this occurrence preserved, or a refusal.

    Both recurrence measurements refuse identically, so the refusal lives in
    one place: a measurement that reports its scope cannot quietly skip part
    of it.
    """

    if event.kind != INGEST_OCCURRED_KIND:
        raise PreservedMaterialMeasurementError(
            f"only preserved ingest occurrences may be measured: {event.kind}"
        )
    represented = event.material.get("represented_material")
    if not isinstance(represented, str):
        raise PreservedMaterialMeasurementError(
            f"{event.identity} preserves no represented material"
        )
    return represented


def measure_recurrences(
    occurrences: Iterable[Event],
    *,
    declared: "dict[str, DeclaredMeasurement]",
    counts_in: "callable[[str], dict[str, int]]",
    preserved_in: EventLedger | None = None,
    yield_in: "tuple[EventLedger, str] | None" = None,
    input_support: InputSupport | None = None,
    support_validator: InputSupportValidator | None = None,
) -> tuple[RecurrenceFinding, ...]:
    """Measure many representations across one pass of the material.

    Measuring many declared representations over the same bounded occurrence
    inputs, one at a time, re-walks and re-splits that inputs once per
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
    representation. Each carries its own declaration, the same input_identities
    inputs, and the same three counts. This differences only how many times the
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
        # One pass has as input one input sequence, so every finding it yields
        # receives that inputs. A declaration disclosing a different
        # counting scope would have its scope assertion preserved beside a
        # inputs the act did not draw from it. `01.Source:28` requires
        # the disclosed scope to be the scope within which occurrences were
        # counted, so the disagreement is refused rather than reconciled.
        raise PreservedMaterialMeasurementError(
            "one pass has as input one input sequence, so every declaration must "
            f"disclose the same counting scope; got {len(scopes)}"
        )
    input_identities: list[str] = []
    localities: dict[str | None, None] = {}
    examined = 0
    carrying: dict[str, int] = {name: 0 for name in declared}
    total: dict[str, int] = {name: 0 for name in declared}
    walked, material_provenance = _as_preserved(
        _distinct_inputs(occurrences), preserved_in
    )
    if input_support is not None and support_validator is not None:
        material_provenance = MATERIAL_READ_FROM_LEDGER
        preserved = []
        for event in walked:
            recorded = support_validator.ledger.get(event.identity)
            if recorded is None:
                raise PreservedMaterialMeasurementError(
                    f"{event.identity} is not preserved in the ledger this support "
                    "support is validated against"
                )
            preserved.append(recorded)
        walked = preserved
    for event in walked:
        text = _measurable_text(event)
        input_identities.append(event.identity)
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
    inputs = tuple(input_identities)
    input_localities = tuple(localities)
    if input_support is not None:
        if support_validator is None:
            raise PreservedMaterialMeasurementError(
                "input support requires its exact ledger boundary"
            )
        if support_validator.validate(input_support) != inputs:
            raise PreservedMaterialMeasurementError(
                "input support and Measurement inputs differ"
            )
    # One invocation performs one bounded Measurement occurrence.  Its exact
    # results remain distinct, but result fan-out does not mint another Act or
    # occurrence for each representation measured during the same pass.
    downstream_act_identity = new_identity("preserved_recurrence_measurement_act")
    act_occurrence_identity = new_identity("preserved_recurrence_measurement_occurrence")
    findings = tuple(
        RecurrenceFinding(
            declared=declaration,
            material_provenance=material_provenance,
            input_localities=input_localities,
            occurrences_examined=examined,
            occurrences_carrying=carrying[representation],
            total_count=total[representation],
            input_event_identities=inputs,
            input_support=input_support,
            downstream_act_identity=downstream_act_identity,
            act_occurrence_identity=act_occurrence_identity,
        )
        for representation, declaration in declared.items()
    )
    if yield_in is not None:
        # Every result is fixed before any evidence is preserved. Preserving
        # one at a time would let evidence for the first survive a failure
        # while measuring the rest, and that evidence would concern a result
        # this act had not finished yielding.
        #
        # The evidence is still appended one at a time, so a later append
        # failing leaves earlier evidence preserved while this call returns
        # nothing. That evidence is not wrong: those results were yielded at
        # this boundary, and the Assertion it carries says yielded rather than
        # returned for exactly this reason. Making the appends atomic would
        # let it Assertion the stronger thing, and is not done here.
        witnessed = []
        for finding in findings:
            evidence = _record_yield(
                yield_in[0],
                locality_identity=yield_in[1],
                finding=finding,
            )
            witnessed.append(replace(finding, yield_evidence_identity=evidence.identity))
        findings = tuple(witnessed)
    return findings


def ingest_occurrences(
    ledger: EventLedger, *, locality_identity: str
) -> list[Event]:
    """Every preserved ingest occurrence carrying this locality, in append order.

    The material measured is what Seed recorded, not what a file contains.

    `06.Standing.B` holds that a locality is a carried coordinate. It preserves
    nothing and performs nothing; the ledger preserves, and this reads by the
    coordinate the occurrences carry.
    """

    return [
        event
        for event in ledger.list_locality(locality_identity)
        if event.kind == INGEST_OCCURRED_KIND
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
    that occurrence has no such position. It performs no read; a
    position that is absent is absent, not Unknown.
    """

    counts: dict[str, int] = {}
    input_identities: list[str] = []
    measured = 0
    walked, material_provenance = _as_preserved(
        _distinct_inputs(occurrences), preserved_in
    )
    for event in walked:
        text = _measurable_text(event)
        input_identities.append(event.identity)
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
        input_event_identities=tuple(input_identities),
    )


def _measurement_finding_material(
    *,
    locality_identity: str,
    finding: MeasurementFinding | RecurrenceFinding,
    extra: dict[str, Any] | None,
) -> dict[str, Any]:
    carried = finding.to_json_dict()
    return {
        "downstream_act_identity": finding.downstream_act_identity,
        "act_occurrence_identity": finding.act_occurrence_identity,
        "dimensions": {
            "identity": f"measurement:{finding.declared.representation_measured}",
            "content": finding.declared.counting_scope,
            "standing": "measured",
            # Stated from the finding rather than asserted here. The measuring
            # act knows whether it read its material from a ledger, and this
            # said "preserved operator-ingest occurrences" for every finding
            # regardless -- supplying a provenance the act had declined.
            "source_provenance": getattr(
                finding, "material_provenance", MATERIAL_AS_SUPPLIED
            ),
            # Not derived from the provenance. An earlier version made this
            # follow material_provenance, which compresses two coordinates
            # `#2439` had just separated and mints the sibling of a string
            # `#2431` had already called contamination. Where the material came
            # from and which responsible boundary bears the Measurement Responsibility are
            # different distinctions, and only the first has been validated.
            "responsibility": RESPONSIBILITY_UNESTABLISHED,
            "authority": "unestablished",
            "evidence_scope": (
                "measurement evidence only; establishes no represented relation, relation, "
                "or standing beyond the measurement assertion"
            ),
            "scope_locality": f"locality:{locality_identity}",
            "occurrence_preservation": "declared measurement durably recorded",
        },
        "unknowns": ["what any measured representation means remains Unknown"],
        **carried,
        **_additive_only(finding, carried, extra),
        "provenance_occurrence_references": (
            [finding.declared.premise_event_identity]
            if finding.declared.premise_event_identity
            else []
        ),
    }


def record_measurement_findings(
    ledger: EventLedger,
    *,
    locality_identity: str,
    findings: Iterable[tuple[MeasurementFinding | RecurrenceFinding, dict[str, Any] | None]],
) -> list[Event]:
    """Preserve a bounded group of findings in one ledger transaction."""

    supplied = list(findings)
    premise_identities = {
        finding.declared.premise_event_identity
        for finding, _ in supplied
        if finding.declared.premise_event_identity is not None
    }
    for premise_identity in premise_identities:
        premise = ledger.get(premise_identity)
        if premise is None or premise.kind != MEASUREMENT_RECORDED_KIND:
            raise PreservedMaterialMeasurementError(
                "a premise must be a recorded measurement finding"
            )
    # Every recorded finding states `source_provenance` as "preserved
    # operator-ingest occurrences". Premises were established here and the
    # occurrences that Assertion were made about never were, so a finding measured
    # over directly supplied `Event` objects recorded that provenance about
    # material this ledger does not hold. `#2510` enforced that at the input
    # boundary only where a support support was declared; a measurement without
    # one reached the recorder unchecked.
    #
    # An earlier version exempted findings carrying a support support, calling
    # them verified. Carrying a support is not being verified against one: both
    # `RecurrenceFinding` and `InputSupport` are directly formable, and a
    # finding verified against one ledger may be handed to another. This
    # function has no witness for either, so it exempts nothing.
    #
    # Identities are collected across the whole call before any read, because
    # every finding of one pass carries the same inputs and checking per
    # finding would restore the cost `#2486` removed.
    input_identities = {
        event_identity
        for finding, _ in supplied
        for event_identity in finding.input_event_identities
    }
    for event_identity in input_identities:
        occurrence = ledger.get(event_identity)
        if occurrence is None or occurrence.kind != INGEST_OCCURRED_KIND:
            raise PreservedMaterialMeasurementError(
                f"{event_identity} is recorded as a input_identities preserved occurrence "
                "and this ledger preserves no such ingest occurrence"
            )
    # A recurrence finding is recordable where the act that yielded it
    # preserved evidence of doing so. Required on this path only: every positional caller records
    # without a yield witness, and adopting it there is its own migration.
    for finding, _ in supplied:
        if not isinstance(finding, RecurrenceFinding):
            continue
        if finding.yield_evidence_identity is None:
            raise PreservedMaterialMeasurementError(
                "this result names no yield evidence; a measuring act "
                "preserves that evidence and the result it returns carries it"
            )
        evidence = ledger.get(finding.yield_evidence_identity)
        if evidence is None or evidence.kind != YIELD_EVIDENCE_KIND:
            raise PreservedMaterialMeasurementError(
                f"{finding.yield_evidence_identity} is named as this result's "
                "evidence and is not preserved yield evidence"
            )
        if evidence.material.get("result_kind") != RECURRENCE_RESULT_KIND:
            raise PreservedMaterialMeasurementError(
                f"{finding.yield_evidence_identity} is yield evidence for "
                "a different kind of result"
            )
        if (
            evidence.material.get("dimensions", {}).get("act_occurrence_identity")
            != finding.act_occurrence_identity
        ):
            raise PreservedMaterialMeasurementError(
                "yield Evidence concerns a different Measurement occurrence"
            )
        if evidence.material.get("result") != _result_content(finding):
            raise PreservedMaterialMeasurementError(
                "the yield evidence this result names concerns a "
                "different result"
            )
    events = [
        Event(
            identity=new_identity("evt"),
            kind=MEASUREMENT_RECORDED_KIND,
            material=_measurement_finding_material(
                locality_identity=locality_identity,
                finding=finding,
                extra=extra,
            ),
            locality_identity=locality_identity,
        )
        for finding, extra in supplied
    ]
    return ledger.append_many(events)


def record_measurement_finding(
    ledger: EventLedger,
    *,
    locality_identity: str,
    finding: MeasurementFinding | RecurrenceFinding,
    extra: dict[str, Any] | None = None,
) -> Event:
    """Preserve a finding so a later responsible act may have it participate.

    The recorded authority states the clause's own limit. A finding is
    measurement evidence and is not relation, represented relation, or established standing.
    """

    return record_measurement_findings(
        ledger,
        locality_identity=locality_identity,
        findings=((finding, extra),),
    )[0]


def premise_chain(ledger: EventLedger, event_identity: str) -> list[str]:
    """Every finding this one stood on, nearest premise first.

    Not the runtime's `InputSupport` representation. This is the chain of
    recorded premise findings one finding stood on, validated nearest premise
    first. It preserves that dependency relation and asserts nothing about the
    yielding act's support support; the prose called it that before the two
    were distinguished and kept calling it that after.
    """

    chain: list[str] = []
    current = ledger.get(event_identity)
    while current is not None:
        premise_identity = current.material.get("premise_event_identity")
        if premise_identity is None:
            break
        chain.append(premise_identity)
        current = ledger.get(premise_identity)
    return chain
