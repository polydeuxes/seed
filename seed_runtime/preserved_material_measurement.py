"""Declared measurement over preserved operator-ingest occurrences.

`01.Source.E` is titled *Measurement and recurrence do not establish represented relation*,
and `01.Source:28` grants the finding and states its conditions:

    A declared measurement may yield bounded findings of exact equality,
    count, recurrence, prefix occurrence, the result of a declared predicate,
    or position within its measurement boundary. Those findings do not
    establish grammatical or semantic represented relation, or constitutional
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
MEASUREMENT_ACT_EVIDENCE_KIND = "operator.measurement.finding_act_evidenced"
EVENT_KIND_RESPONSIBILITIES = {
    MEASUREMENT_RECORDED_KIND: "02.Acts.A",
    MEASUREMENT_ACT_EVIDENCE_KIND: "02.Acts.A",
}
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

LIMITS: tuple[str, ...] = (
    "A finding reports a count within its stated scope and nothing further.",
    "Recurrence establishes that a representation occurs more than once only.",
    "A highest-count representation is not the represented relation of that position.",
    "Co-presence of representations establishes no relation (01.Standing.D).",
    "This yields no represented relation, relation, truth, applicability, or admission.",
)


class PreservedMaterialMeasurementError(ValueError):
    """Raised when a measurement cannot use its declared inputs as stated."""


def measurement_input_occurrences(material: Any) -> tuple[str, ...]:
    inputs = material.get("inputs") if isinstance(material, dict) else None
    if not isinstance(inputs, list):
        raise PreservedMaterialMeasurementError(
            "the Measurement finding carries no exact input occurrences"
        )
    occurrences = []
    for item in inputs:
        if (
            not isinstance(item, dict)
            or set(item) != {"occurrence_identity"}
            or not isinstance(item["occurrence_identity"], str)
            or not item["occurrence_identity"]
        ):
            raise PreservedMaterialMeasurementError(
                "the Measurement finding carries an incomplete input occurrence"
            )
        occurrences.append(item["occurrence_identity"])
    return tuple(occurrences)


@dataclass(frozen=True)
class DeclaredMeasurement:
    """The three disclosures `01.Source:28` requires.

    `representation_measured`, `equivalence_rule`, and `counting_scope` are the
    clause's own words. They are required because the clause requires them, and
    an empty one is refused rather than defaulted.
    """

    representation_measured: str
    equivalence_rule: str
    counting_scope: str
    # The representation this measurement measured relative to, when it had
    # one.  A finding can only supply an representation to a later measurement if it
    # records the representation it used, so this is what makes a finding
    # representation-supplying rather than merely informative.
    relative_representation: str | None = None
    distinction: str | None = None
    # Where the position measured sits relative to what it was measured
    # relative to.  Recorded so a measurement can be compared with another
    # that measured elsewhere, and so a coordinate that never varies is
    # recorded rather than implicit in the code that indexed it.
    measured_position: dict[str, Any] | None = None

    def __post_init__(self) -> None:
        for name in ("representation_measured", "equivalence_rule", "counting_scope"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise PreservedMaterialMeasurementError(
                    f"a declared measurement must disclose {name}"
                )


@dataclass(frozen=True)
class RepresentationCount:
    """One representation and its occurrence count."""

    representation: str
    occurrence_count: int


@dataclass(frozen=True)
class MeasurementFinding:
    """A bounded count over preserved occurrences, and what it stood on."""

    declared: DeclaredMeasurement
    position_count: int
    representation_counts: tuple[RepresentationCount, ...]
    # The identities this measurement input_identities, available while the act runs.
    # On the result-Assertion path one exact input support Assertion is supplied from
    # these inputs instead of preserving the enumeration in every result;
    # the support belongs to that path, and this dataclass does not own a second
    # coordinate for it. `#2486` measured why: copying the inputs into
    # every finding of a body cost 97% of the stored finding.
    input_occurrences: tuple[str, ...]
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
    def highest_count_representation(self) -> RepresentationCount | None:
        """The representation with the highest count, if one was measured."""

        return self.representation_counts[0] if self.representation_counts else None

    def to_json_dict(self) -> dict[str, Any]:
        return _finding_coordinates(self)


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
    that Standing with it as subject exists.

    Three counts, because one is not readable without the others. A
    representation occurring three times says nothing until the material it
    occurred across is also stated, and occurring three times in one occurrence
    is not the same finding as occurring once in each of three. The clause
    requires the bounded scope be disclosed; the exact input identities and
    their count carry that scope.
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
    # How many of them carried the representation at least once.
    occurrences_carrying: int
    # How many times the representation recurred across them.
    recurrence_count: int
    input_occurrences: tuple[str, ...]
    downstream_act_identity: str = field(
        default_factory=lambda: new_identity("preserved_recurrence_measurement_act"),
        compare=False,
    )
    act_occurrence_identity: str = field(
        default_factory=lambda: new_identity("preserved_recurrence_measurement_occurrence"),
        compare=False,
    )
    result_identity: str = field(
        default_factory=lambda: new_identity("preserved_recurrence_measurement_result"),
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
    responsible_act_evidence_identity: str | None = None
    # Which preserved Evidence is for this result's exact Yield relation. The
    # Evidence reference is neither the relation nor its Act occurrence by identity.
    # holds that a separately supplied representation with identical fields
    # does not carry the witnessed return's standing "unless that standing is
    # separately represented or preserved". Content equality cannot supply it:
    # an identical validation has identical content by definition, which is
    # exactly the case the relation must distinguish. So the relation travels
    # with the result rather than being validated later by matching bytes.
    #
    # A later representation carrying this same reference is another
    # representation of the same result under exact Yield Evidence. One carrying
    # none has no such Yield relation.
    yield_evidence_identity: str | None = None
    limits: tuple[str, ...] = field(default=LIMITS)

    @property
    def input_count(self) -> int:
        return len(self.input_occurrences)

    def to_json_dict(self) -> dict[str, Any]:
        return _finding_coordinates(self)


def _finding_coordinates(
    finding: MeasurementFinding | RecurrenceFinding,
) -> dict[str, Any]:
    if isinstance(finding, MeasurementFinding):
        return {
            "representation_measured": finding.declared.representation_measured,
            "equivalence_rule": finding.declared.equivalence_rule,
            "counting_scope": finding.declared.counting_scope,
            "relative_representation": finding.declared.relative_representation,
            "measurement_distinction": finding.declared.distinction,
            "measured_position": finding.declared.measured_position,
            "position_count": finding.position_count,
            "representation_counts": [
                {
                    "representation": occurrence.representation,
                    "occurrence_count": occurrence.occurrence_count,
                }
                for occurrence in finding.representation_counts
            ],
            "inputs": [
                {"occurrence_identity": identity}
                for identity in finding.input_occurrences
            ],
            "input_count": len(finding.input_occurrences),
            "limits": list(finding.limits),
        }
    if finding.input_support is None:
        return {
            "result_identity": finding.result_identity,
            "representation_measured": finding.declared.representation_measured,
            "equivalence_rule": finding.declared.equivalence_rule,
            "counting_scope": finding.declared.counting_scope,
            "measurement_distinction": "recurrence",
            "input_localities": list(finding.input_localities),
            "occurrences_carrying": finding.occurrences_carrying,
            "recurrence_count": finding.recurrence_count,
            "inputs": [
                {"occurrence_identity": identity}
                for identity in finding.input_occurrences
            ],
            "input_count": finding.input_count,
            "limits": list(finding.limits),
            "yield_evidence_identity": finding.yield_evidence_identity,
            "responsible_act_evidence_identity": (
                finding.responsible_act_evidence_identity
            ),
        }
    return {
        "result_identity": finding.result_identity,
        "representation_measured": finding.declared.representation_measured,
        "equivalence_rule": finding.declared.equivalence_rule,
        "counting_scope": finding.declared.counting_scope,
        "measurement_distinction": "recurrence",
        "input_localities": list(finding.input_localities),
        "occurrences_carrying": finding.occurrences_carrying,
        "recurrence_count": finding.recurrence_count,
        "input_support": finding.input_support.to_json_dict(),
        "input_count": finding.input_count,
        "limits": list(finding.limits),
        "yield_evidence_identity": finding.yield_evidence_identity,
        "responsible_act_evidence_identity": (
            finding.responsible_act_evidence_identity
        ),
    }


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

    Refuses the same material `measure_position_representations` refuses, for the same reason.
    A measurement over bounded inputs cannot measure text in material
    that has none, and skipping would silently narrow the scope the finding
    goes on to disclose.
    """

    input_identities: list[str] = []
    localities: dict[str | None, None] = {}
    carrying = 0
    recurrence = 0
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
        if count:
            carrying += 1
            recurrence += count
    finding = RecurrenceFinding(
        declared=declared,
        material_provenance=material_provenance,
        input_localities=tuple(localities),
        occurrences_carrying=carrying,
        recurrence_count=recurrence,
        input_occurrences=tuple(input_identities),
    )
    if yield_in is not None:
        act_evidence, evidence = _record_yield(
            yield_in[0],
            locality_identity=yield_in[1],
            finding=finding,
        )
        finding = replace(
            finding,
            responsible_act_evidence_identity=act_evidence.identity,
            yield_evidence_identity=evidence.identity,
        )
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
    The input count asserts a number of occurrences. One preserved
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


def _result_content(finding) -> dict[str, Any]:
    """Everything the measuring act established about its own result.

    Not `to_json_dict()`. That representation deliberately omits
    `material_provenance`, which is stated once by the recorder, so a
    commitment taken over it cannot tell a result from ledger-read material
    from one from supplied material -- the coordinate
    `#2516` exists to keep. Every carried coordinate is included here,
    `limits` among them.
    """

    content = dict(finding.to_json_dict())
    content["material_provenance"] = getattr(
        finding, "material_provenance", MATERIAL_AS_SUPPLIED
    )
    # The reference to the yield evidence is not part of the content that
    # evidence commits to; it is how a result names its Evidence.
    content.pop("yield_evidence_identity", None)
    content.pop("responsible_act_evidence_identity", None)
    return content


def _recorded_yield_result(
    recorded: Event, yield_coordinates: tuple[str, ...]
) -> dict[str, Any]:
    """Read the exact Yield coordinates from one recorded finding.

    The Yield Evidence names the exact top-level result coordinates. Recording
    may lawfully add other coordinates, so neither an
    exclusion list nor every key left in the recorded material reads this
    boundary. `material_provenance` is the one result coordinate represented
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
                    "the recorded finding does not preserve its result "
                    "material provenance"
                )
            content[key] = dimensions["source_provenance"]
        elif key not in material:
            raise PreservedMaterialMeasurementError(
                f"the recorded finding does not preserve result coordinate {key}"
            )
        else:
            content[key] = material[key]
    return content


def _record_yield(
    ledger: EventLedger, *, locality_identity: str, finding
) -> tuple[Event, Event]:
    """Preserve exact Yield Evidence at the responsible Act boundary.

    The distinction is not that this is private. Privacy is mechanics. It is
    that Standing for the occurrence-to-result relation is preserved at the
    exact Act boundary, and
    the result carries the relation to it — so a separately supplied
    representation with identical fields carries no such relation, which is the
    direct-instantiation counterexample states. An earlier attempt showed this
    publicly, which made it a second recorder: a caller holding any object could
    record a yield over it, establishing only that a caller possessed
    something and called a function.

    What this establishes, and what it does not:

    ```text
      established   exact Yield from this measuring Act occurrence to this result
      not           who is authorized to perform it
      not           which responsible boundary bears the Measurement Responsibility
      not           that nothing else appended this kind directly
    ```

    The three negative coordinates stay unestablished; the material records them
    as such rather than filling them.

    This occurrence is preserved Evidence for a Yield relation. It is not
    that relation or its Act occurrence by identity.
    """

    act_evidence = ledger.append(
        MEASUREMENT_ACT_EVIDENCE_KIND,
        {
            "downstream_act_identity": finding.downstream_act_identity,
            "act_occurrence_identity": finding.act_occurrence_identity,
            "act": "declared Measurement",
            "responsibility": RESPONSIBILITY_UNESTABLISHED,
            "responsible_boundary": "unestablished",
            "authority": "unestablished",
            "evidence_scope": "Evidence for this exact Measurement occurrence only",
        },
        locality_identity=locality_identity,
    )
    yield_evidence = _record_yield_evidence(
        ledger,
        locality_identity=locality_identity,
        exact_act="declared Measurement",
        act_occurrence_identity=finding.act_occurrence_identity,
        responsible_act_evidence_identity=act_evidence.identity,
        result_kind=RECURRENCE_RESULT_KIND,
        result_identity=finding.result_identity,
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
    return act_evidence, yield_evidence


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
    carrying: dict[str, int] = {name: 0 for name in declared}
    recurrence: dict[str, int] = {name: 0 for name in declared}
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
                recurrence[representation] += count
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
            occurrences_carrying=carrying[representation],
            recurrence_count=recurrence[representation],
            input_occurrences=inputs,
            input_support=input_support,
            downstream_act_identity=downstream_act_identity,
            act_occurrence_identity=act_occurrence_identity,
        )
        for representation, declaration in declared.items()
    )
    if yield_in is not None:
        # Every result is fixed before any evidence is preserved. Preserving
        # one at a time would let evidence for the first survive a failure
        # while measuring the rest, and that evidence would be for a result
        # this Act had not fixed every result.
        #
        # The evidence is still appended one at a time, so a later append
        # failing leaves earlier evidence preserved while this call returns
        # nothing. That evidence is not wrong: those results have exact Yield
        # Evidence at this boundary; it does not assert a successful return.
        # Making the appends atomic would
        # let it Assertion the stronger thing, and is not done here.
        witnessed = []
        for finding in findings:
            act_evidence, evidence = _record_yield(
                yield_in[0],
                locality_identity=yield_in[1],
                finding=finding,
            )
            witnessed.append(
                replace(
                    finding,
                    responsible_act_evidence_identity=act_evidence.identity,
                    yield_evidence_identity=evidence.identity,
                )
            )
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


def measure_position_representations(
    occurrences: Iterable[Event],
    *,
    declared: DeclaredMeasurement,
    representation_at: "callable[[str], str | None]",
    preserved_in: EventLedger | None = None,
) -> MeasurementFinding:
    """Count which representations occupy a position across preserved material.

    ``representation_at`` receives one preserved representation and returns the
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
        representation = representation_at(text)
        if representation is None:
            continue
        measured += 1
        counts[representation] = counts.get(representation, 0) + 1
    ordered = tuple(
        RepresentationCount(representation=r, occurrence_count=n)
        for r, n in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
    )
    return MeasurementFinding(
        declared=declared,
        material_provenance=material_provenance,
        position_count=measured,
        representation_counts=ordered,
        input_occurrences=tuple(input_identities),
    )


def _measurement_finding_material(
    *,
    locality_identity: str,
    finding: MeasurementFinding | RecurrenceFinding,
) -> dict[str, Any]:
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
            # Material provenance and the responsible boundary bearing the
            # Measurement Responsibility are distinct coordinates.
            "responsibility": RESPONSIBILITY_UNESTABLISHED,
            "authority": "unestablished",
            "evidence_scope": (
                "measurement evidence only; establishes no represented relation, relation, "
                "or standing beyond the measurement assertion"
            ),
            "scope_locality": f"locality:{locality_identity}",
            "occurrence_preservation": "declared Measurement occurrence recorded",
        },
        "unknowns": [
            "represented relation of any measured Representation remains Unknown"
        ],
        **_finding_coordinates(finding),
    }


def record_measurement_findings(
    ledger: EventLedger,
    *,
    locality_identity: str,
    findings: Iterable[MeasurementFinding | RecurrenceFinding],
) -> list[Event]:
    """Preserve a bounded group of findings in one ledger transaction."""

    supplied = list(findings)
    # Carrying a support is not being verified against one: both
    # `RecurrenceFinding` and `InputSupport` are directly formable, and a
    # finding verified against one ledger may be handed to another. This
    # function has no witness for either, so it exempts nothing.
    #
    # Identities are collected across the whole call before any read, because
    # every finding of one pass carries the same inputs and checking per
    # finding would restore the cost `#2486` removed.
    input_identities = {
        event_identity
        for finding in supplied
        for event_identity in finding.input_occurrences
    }
    for event_identity in input_identities:
        occurrence = ledger.get(event_identity)
        if occurrence is None or occurrence.kind != INGEST_OCCURRED_KIND:
            raise PreservedMaterialMeasurementError(
                f"{event_identity} is recorded as a input_identities preserved occurrence "
                "and this ledger preserves no such ingest occurrence"
            )
    # A recurrence finding is recordable where its Act preserved exact Yield
    # Evidence. Required on this path only: every positional caller records
    # without a yield witness, and adopting it there is its own migration.
    for finding in supplied:
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
                "yield Evidence carries a different Measurement occurrence"
            )
        if evidence.material.get("result") != _result_content(finding):
            raise PreservedMaterialMeasurementError(
                "the yield evidence this result names carries a "
                "different result"
            )
    events = [
        Event(
            identity=new_identity("evt"),
            kind=MEASUREMENT_RECORDED_KIND,
            material=_measurement_finding_material(
                locality_identity=locality_identity,
                finding=finding,
            ),
            locality_identity=locality_identity,
        )
        for finding in supplied
    ]
    return ledger.append_many(events)


def record_measurement_finding(
    ledger: EventLedger,
    *,
    locality_identity: str,
    finding: MeasurementFinding | RecurrenceFinding,
) -> Event:
    """Preserve a finding so a later responsible act may have it participate.

    The recorded authority states the clause's own limit. A finding is
    measurement evidence and is not relation, represented relation, or established standing.
    """

    return record_measurement_findings(
        ledger,
        locality_identity=locality_identity,
        findings=(finding,),
    )[0]
