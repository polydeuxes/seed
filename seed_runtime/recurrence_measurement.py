"""Declared measurement whose subject is Seed's own recorded occurrences.

**No new Act.** `#2351` read declared measurement and said no new act,
noun, or grammar is required; recurrence and count are already its findings.
This measures a different subject — recorded comparison and measurement
occurrences instead of preserved material — and yields an exact count of the
bounded localities a distinction was measured in. Recurrence is one read of
that count, established only where the count exceeds one.
A distinct record shape is established (`#2399`: a downstream shape must not
decide an upstream subject); a distinct Responsibility is not.

`#2429` called this a "cohort measurement" and wrote
`cohort-measurement-over-recorded-comparisons` into every record. That named a
Responsibility nothing established, and `cohort`, `inputs`, `body` and
`survey` were statistical vocabulary the grammar never needed. What the act
reports is:

```text
this measured distinction was measured in N of the declared bounded localities
under the declared rule and Scope
```

and recurrence is asserted only where N exceeds one.

**Its result stands on recorded Measurement occurrences.** Each occurrence
already carries the declared identity and every exact representation it measured.
Materializing every pairwise Compare between those occurrences adds no input to
the count and grows quadratically with the number of bounded localities.  The
measurement therefore folds each exact Measurement once.  Compare remains a
separate Act when literal comparison is actually requested.

**Grouping uses the whole declared identity.** `#2429` grouped on left
representation, rule and position, then described the result as "under the
declared rule and scope" while `counting_scope` was not among them. Two
measurements declaring different scopes are not the same measurement, and
`01.Source:28` requires the measured representation, the sameness rule and
the bounded scope to travel with a recurrence assertion.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Any, Iterable, Iterator

from seed_runtime.events import EventLedger, EventLedgerBoundary
from seed_runtime.event import Event
from seed_runtime.identities import new_identity
from seed_runtime.preserved_material_measurement import MEASUREMENT_RECORDED_KIND
from seed_runtime.yield_evidence import _record_yield_evidence

LOCALITY_COUNT_RECORDED_KIND = "operator.measurement.locality_count_recorded"
LOCALITY_COUNT_ACT_EVIDENCE_KIND = (
    "operator.measurement.locality_count_act_evidenced"
)
LOCALITY_COUNT_RESULT_KIND = "locality count Measurement result"
LOCALITY_COUNT_RESPONSIBILITY = (
    "Measure one exact distinction across exact bounded Localities"
)
EVENT_KIND_RESPONSIBILITIES = {
    LOCALITY_COUNT_RECORDED_KIND: "02.Acts.A",
    LOCALITY_COUNT_ACT_EVIDENCE_KIND: "02.Acts.A",
}

MEASURED_ASSERTION_STANDING_COORDINATE_RESPONSIBILITY = (
    "preserve this measured Assertion's carried Standing coordinates"
)

# The declared identity a recurrence assertion is made under. Two occurrences
# that differ on any of these did not measure the same thing, and counting them
# together reports a recurrence nothing observed.
DECLARED_IDENTITY: tuple[str, ...] = (
    "representation_measured",
    "relative_representation",
    "equivalence_rule",
    "counting_scope",
    "measured_position",
    "measurement_distinction",
)

LIMITS: tuple[str, ...] = (
    "independently preserved is not independent; nothing here establishes that "
    "the localities' sources are unrelated",
    "recurrence is repetition, and repetition is not independent corroboration",
    "an exact count is a finding at any value; a count of one establishes no "
    "recurrence",
    "the count reports the bounded localities among the occurrences this "
    "measurement input, not a property of the material",
    "an locality that never measured the coordinate has not declined to measure "
    "the distinction",
    "measuring the same distinction establishes no relation between the "
    "localities that measured it",
)


class RecurrenceMeasurementError(Exception):
    """The measurement boundary could not be instantiated."""


@dataclass(frozen=True)
class MeasuredDistinction:
    """What was measured, under the whole declared identity it was measured with."""

    representation: str
    declared: tuple[tuple[str, str], ...]

    def to_json_dict(self) -> dict[str, Any]:
        return {
            "representation": self.representation,
            **{name: value for name, value in self.declared},
        }

    @property
    def relative_representation(self) -> str:
        return dict(self.declared).get("relative_representation", "")


@dataclass(frozen=True)
class MeasuredCountFinding:
    """One exact count over recorded occurrences. A record shape, not a kind.

    `01.Source:28` lists **count** and **recurrence** as separate findings of
    a declared measurement. `#2430` named this shape `RecurrenceFinding` and
    represented a count of one as "recurs in 1 bounded localities", which asserts
    recurrence where nothing recurred. The count is the finding; recurrence is
    established only where the count establishes it.
    """

    distinction: MeasuredDistinction
    measured_in: tuple[str, ...]
    measured_without_distinction: tuple[str, ...]
    coordinate_not_measured: tuple[str, ...]
    input_occurrences: tuple[str, ...]
    input_ledger_boundary: EventLedgerBoundary
    bounded_localities: tuple[str, ...]
    measured_in_support_event_identities: tuple[str, ...] = ()
    measured_without_distinction_support_event_identities: tuple[str, ...] = ()

    @property
    def locality_count(self) -> int:
        """The exact count. Always a finding, at any value."""
        return len(self.measured_in)

    @property
    def recurrence_established(self) -> bool:
        """Recurrence needs something to have recurred."""
        return self.locality_count > 1

    def to_json_dict(self) -> dict[str, Any]:
        return {
            "distinction": self.distinction.to_json_dict(),
            "measured_in": list(self.measured_in),
            "measured_without_distinction": list(self.measured_without_distinction),
            "coordinate_not_measured": list(self.coordinate_not_measured),
            "locality_count": self.locality_count,
            "recurrence_established": self.recurrence_established,
            "bounded_localities": list(self.bounded_localities),
            "inputs": [
                {"occurrence_identity": identity}
                for identity in self.input_occurrences
            ],
            "input_ledger_boundary": {
                "identity": self.input_ledger_boundary.identity,
            },
        }


@dataclass(frozen=True)
class MeasuredAssertion:
    """One separately accountable result of the recurrence Measurement."""

    identity: str
    result: str
    subject: dict[str, Any]
    content: dict[str, Any]
    scope: dict[str, Any]
    support_event_identities: tuple[str, ...] = ()
    support_assertion_identities: tuple[str, ...] = ()
    completeness_boundary: EventLedgerBoundary | None = None
    completeness_occurrence_kinds: tuple[str, ...] = ()

    def to_json_dict(self) -> dict[str, Any]:
        return {
            "dimensions": {
                "identity": self.identity,
                "content": dict(self.content),
                "standing": "measured",
                "source_provenance": (
                    "recorded comparison occurrences and recorded measurement "
                    "occurrences"
                ),
                "responsibility": MEASURED_ASSERTION_STANDING_COORDINATE_RESPONSIBILITY,
                "authority": "unestablished",
                "evidence_scope": (
                    "measurement evidence only; establishes no relation between "
                    "the localities, no source independence, and no corroboration"
                ),
                "scope_locality": "the exact assertion_scope carried here",
                "occurrence_preservation": (
                    "distinct result preserved by its yielding occurrence"
                ),
            },
            "subject_kind": "assertion",
            "responsible_boundary": "this recorded assertion",
            "result": self.result,
            "assertion_subject": dict(self.subject),
            "assertion_scope": dict(self.scope),
            "input_support": {
                "event_identities": list(self.support_event_identities),
                # These dependencies are local to the same yielding
                # occurrence. Each remains bound to that occurrence's identity
                # before exposing it to a downstream Act.
                "local_assertion_identities": list(self.support_assertion_identities),
            },
            "completeness_boundary": (
                {"identity": self.completeness_boundary.identity}
                if self.completeness_boundary is not None
                else None
            ),
            "completeness_scope": (
                {
                    "locality_identities": list(self.scope["bounded_localities"]),
                    "occurrence_kinds": list(self.completeness_occurrence_kinds),
                    "requires_locality_existence": True,
                }
                if self.completeness_boundary is not None
                else None
            ),
            "unknowns": [
                "what any measured representation means remains Unknown",
                "whether the localities stand in any relation remains Unknown",
                "whether their sources are independent remains Unknown",
            ],
            "limits": list(LIMITS),
        }


@dataclass(frozen=True)
class RecordedMeasuredAssertion:
    """One addressable Assertion preserved inside its yielding occurrence."""

    assertion_identity: str
    recorded_occurrence_reference: str
    yielding_locality_identity: str | None
    result: str
    material: dict[str, Any]
    support_assertion_references: tuple[dict[str, str], ...] = ()

    @property
    def reference(self) -> dict[str, str]:
        return {
            "assertion_identity": self.assertion_identity,
            "recorded_occurrence_reference": self.recorded_occurrence_reference,
        }


def assertions_of_recorded_measurement(event: Event) -> tuple[RecordedMeasuredAssertion, ...]:
    """Read every Assertion from one exact yielding occurrence."""

    if event.kind != LOCALITY_COUNT_RECORDED_KIND:
        raise RecurrenceMeasurementError(
            f"{event.identity} is {event.kind}, not a recurrence Measurement occurrence"
        )
    stated = event.material.get("assertions")
    if not isinstance(stated, list):
        raise RecurrenceMeasurementError(
            f"{event.identity} does not preserve its distinct Assertions"
        )
    read = []
    seen = set()
    for assertion in stated:
        if not isinstance(assertion, dict):
            raise RecurrenceMeasurementError(
                f"{event.identity} carries a non-object Assertion representation"
            )
        dimensions = assertion.get("dimensions")
        identity = dimensions.get("identity") if isinstance(dimensions, dict) else None
        content = dimensions.get("content") if isinstance(dimensions, dict) else None
        result = assertion.get("result")
        subject = assertion.get("assertion_subject")
        scope = assertion.get("assertion_scope")
        if assertion.get("subject_kind") != "assertion":
            raise RecurrenceMeasurementError(
                f"{event.identity} carries a result that is not identified as an Assertion"
            )
        if (
            not isinstance(identity, str)
            or not identity
            or not isinstance(result, str)
            or not isinstance(content, dict)
            or not isinstance(subject, dict)
            or not isinstance(scope, dict)
        ):
            raise RecurrenceMeasurementError(
                f"{event.identity} carries an Assertion without exact identity, result, "
                "subject, scope, and content"
            )
        bounded_localities = scope.get("bounded_localities")
        declared_identity = scope.get("declared_identity")
        if (
            not isinstance(bounded_localities, list)
            or not all(isinstance(value, str) for value in bounded_localities)
            or not isinstance(declared_identity, dict)
            or any(subject.get(name) != value for name, value in declared_identity.items())
        ):
            raise RecurrenceMeasurementError(
                f"{event.identity} carries an Assertion without coherent bounded scope"
            )
        canonical = _canonical_measured_assertion_identity(
            result=result,
            subject=subject,
            bounded_localities=bounded_localities,
            content=content,
        )
        if identity != canonical:
            raise RecurrenceMeasurementError(
                f"{event.identity} carries an Assertion identity that does not match "
                "its carried coordinates"
            )
        if identity in seen:
            raise RecurrenceMeasurementError(
                f"{event.identity} carries duplicate Assertion identity {identity}"
            )
        seen.add(identity)
        read.append(
            RecordedMeasuredAssertion(
                assertion_identity=identity,
                recorded_occurrence_reference=event.identity,
                yielding_locality_identity=event.locality_identity,
                result=result,
                material=assertion,
            )
        )
    identities = {assertion.assertion_identity for assertion in read}
    by_result = {}
    for assertion in read:
        if assertion.result in by_result:
            raise RecurrenceMeasurementError(
                f"{event.identity} carries duplicate Assertion result {assertion.result}"
            )
        by_result[assertion.result] = assertion
    bound = []
    for assertion in read:
        support = assertion.material.get("input_support")
        local_identities = support.get("local_assertion_identities") if isinstance(support, dict) else None
        if not isinstance(local_identities, list) or not all(
            isinstance(value, str) for value in local_identities
        ):
            raise RecurrenceMeasurementError(
                f"{event.identity} carries an Assertion without local Assertion support"
            )
        missing = set(local_identities) - identities
        if missing:
            raise RecurrenceMeasurementError(
                f"{event.identity} carries unresolved local Assertion support: "
                f"{', '.join(sorted(missing))}"
            )
        if assertion.result == "count":
            measured_in = by_result.get("measured_in")
            expected_local_identities = (
                [measured_in.assertion_identity] if measured_in is not None else []
            )
        elif assertion.result == "recurrence":
            count = by_result.get("count")
            expected_local_identities = [count.assertion_identity] if count is not None else []
        else:
            expected_local_identities = []
        if local_identities != expected_local_identities:
            raise RecurrenceMeasurementError(
                f"{event.identity} carries {assertion.result} with the wrong local "
                "Assertion support"
            )
        bound.append(
            RecordedMeasuredAssertion(
                assertion_identity=assertion.assertion_identity,
                recorded_occurrence_reference=assertion.recorded_occurrence_reference,
                yielding_locality_identity=assertion.yielding_locality_identity,
                result=assertion.result,
                material=assertion.material,
                support_assertion_references=tuple(
                    {
                        "recorded_occurrence_reference": event.identity,
                        "assertion_identity": local_identity,
                    }
                    for local_identity in local_identities
                ),
            )
        )
    return tuple(bound)


def iter_recorded_measured_assertions(
    ledger: EventLedger,
    *,
    locality_identities: Iterable[str],
    through: EventLedgerBoundary | None = None,
) -> Iterator[RecordedMeasuredAssertion]:
    """Stream Assertions from exact declared Localities through one boundary."""

    for locality_identity in tuple(dict.fromkeys(locality_identities)):
        for event in ledger.iter_locality_kind(
            locality_identity,
            LOCALITY_COUNT_RECORDED_KIND,
            through=through,
        ):
            yield from assertions_of_recorded_measurement(event)


def get_recorded_measured_assertion(
    ledger: EventLedger, *, recorded_occurrence_reference: str, assertion_identity: str
) -> RecordedMeasuredAssertion | None:
    """Resolve one exact occurrence-bound Assertion reference."""

    event = ledger.get(recorded_occurrence_reference)
    if event is None:
        return None
    for assertion in assertions_of_recorded_measurement(event):
        if assertion.assertion_identity == assertion_identity:
            return assertion
    return None


def _declared_of_measurement(event: Event) -> tuple[tuple[str, str], ...] | None:
    declared = []
    for name in DECLARED_IDENTITY:
        if name not in event.material:
            return None
        declared.append((name, str(event.material[name])))
    return tuple(declared)


def measure_locality_counts(
    ledger: EventLedger,
    *,
    bounded_localities: Iterable[str],
    through: EventLedgerBoundary | None = None,
) -> list[MeasuredCountFinding]:
    """Count, over recorded occurrences, the localities each distinction was measured in.

    Each Measurement occurrence is read once.  Pairwise Compare occurrences
    are neither required nor read: their endpoints contain no representation that
    the Measurement occurrences do not already carry.
    """

    declared_localities = tuple(sorted(set(bounded_localities)))
    if not declared_localities:
        raise RecurrenceMeasurementError(
            "a declared measurement discloses the bounded scope within which "
            "occurrences were counted; no bounded localities were declared"
        )
    # Every probe and both occurrence passes have as input one ledger-local append
    # prefix. The boundary is carried as read provenance; it is not an Event
    # identity and does not strengthen the occurrences read through it.
    input_ledger_boundary = through or ledger.append_boundary()
    if not isinstance(input_ledger_boundary, EventLedgerBoundary):
        raise RecurrenceMeasurementError(
            "a locality count Measurement requires one exact ledger boundary"
        )
    # Declaring the Scope chooses which established localities this measurement
    # reads. It does not establish them: a recorded occurrence within the
    # Locality boundary does. Each declared locality is read through that exact
    # boundary, so the existence check costs one bounded read per declared
    # locality.
    # The pass retains only compact indexes read from Measurement.
    # The existence probe remains separate:
    # declaration chooses among established Localities, and a non-measurement
    # occurrence can establish a Locality without supplying a measured coordinate.
    measured_coordinate: dict[tuple, set[str]] = {}
    coordinate_evidence: dict[tuple, dict[str, set[str]]] = {}
    observed: dict[MeasuredDistinction, set[str]] = {}
    observed_evidence: dict[MeasuredDistinction, set[str]] = {}
    unestablished: list[str] = []
    measurement_seen = False

    for locality in declared_localities:
        if not ledger.has_locality(locality, through=input_ledger_boundary):
            unestablished.append(locality)
            continue
        for event in ledger.iter_locality_kind(
            locality,
            MEASUREMENT_RECORDED_KIND,
            through=input_ledger_boundary,
        ):
            measurement_seen = True
            declared = _declared_of_measurement(event)
            if declared is None:
                continue
            measured_coordinate.setdefault(declared, set()).add(locality)
            coordinate_evidence.setdefault(declared, {}).setdefault(
                locality, set()
            ).add(event.identity)
            for item in event.material.get("representation_counts", []):
                representation = item.get("representation")
                if not isinstance(representation, str):
                    continue
                key = MeasuredDistinction(
                    representation=representation,
                    declared=declared,
                )
                observed.setdefault(key, set()).add(locality)
                observed_evidence.setdefault(key, set()).add(event.identity)

    if unestablished:
        raise RecurrenceMeasurementError(
            "declared bounded localities with no recorded occurrence: "
            f"{', '.join(unestablished)}. Declaring a measurement's Scope "
            "chooses among established localities; it does not establish them"
        )
    if not measurement_seen:
        raise RecurrenceMeasurementError(
            "no recorded Measurement occurrences to measure; preserved material "
            "beside this Act is not a measured input"
        )

    findings = []
    declared_set = set(declared_localities)
    for key in sorted(
        observed,
        key=lambda k: (
            -len(observed[k]),
            k.relative_representation,
            k.representation,
        ),
    ):
        where = observed[key]
        measured = measured_coordinate.get(key.declared, set())
        not_measured = declared_set - measured
        measured_without = measured - where
        measured_without_evidence = {
            event_identity
            for locality in measured_without
            for event_identity in coordinate_evidence.get(key.declared, {}).get(
                locality, set()
            )
        }
        measured_in_evidence = set(observed_evidence[key])
        evidence = measured_in_evidence | measured_without_evidence
        # The third result stands on the complete Measurement-kind read for
        # each declared locality through the preserved ledger boundary. Copying
        # every unrelated Measurement identity into every negative finding neither
        # establishes nor strengthens that completeness. Exact-coordinate,
        # Compare, and comparison-input Evidence remain carried below.
        findings.append(
            MeasuredCountFinding(
                distinction=key,
                measured_in=tuple(sorted(where)),
                measured_without_distinction=tuple(sorted(measured_without)),
                coordinate_not_measured=tuple(sorted(not_measured)),
                input_occurrences=tuple(sorted(evidence)),
                input_ledger_boundary=input_ledger_boundary,
                bounded_localities=declared_localities,
                measured_in_support_event_identities=tuple(
                    sorted(measured_in_evidence)
                ),
                measured_without_distinction_support_event_identities=tuple(
                    sorted(measured_without_evidence)
                ),
            )
        )
    return findings


def measured_count_representation(finding: MeasuredCountFinding) -> str:
    """The literal sentence, and nothing stronger.

    A count of one says it was measured in one locality. It does not say it
    recurred, because it did not.
    """

    declared = dict(finding.distinction.declared)
    verb = "recurs in" if finding.recurrence_established else "was measured in"
    localities = "locality" if finding.locality_count == 1 else "localities"
    return (
        f"({declared['relative_representation']!r}, "
        f"{finding.distinction.representation!r}) {verb} "
        f"{finding.locality_count} bounded {localities} of "
        f"{len(finding.bounded_localities)} declared, at "
        f"{declared['measured_position']} under "
        f"{declared['equivalence_rule']} within {declared['counting_scope']}"
    )


def _canonical_measured_assertion_identity(
    *,
    result: str,
    subject: dict[str, Any],
    bounded_localities: Iterable[str],
    content: dict[str, Any],
) -> str:
    identified = {
        "result": result,
        "distinction": subject,
        "bounded_localities": list(bounded_localities),
        "content": content,
    }
    return "measured-assertion:" + json.dumps(
        identified, sort_keys=True, separators=(",", ":")
    )


def _result_assertion_identity(
    finding: MeasuredCountFinding, result: str, content: dict[str, Any]
) -> str:
    return _canonical_measured_assertion_identity(
        result=result,
        subject=finding.distinction.to_json_dict(),
        bounded_localities=finding.bounded_localities,
        content=content,
    )


def assertions_from_measured_count(
    finding: MeasuredCountFinding,
) -> tuple[MeasuredAssertion, ...]:
    """Every distinct result this recurrence Measurement already established.

    This is result fan-out, not inference from one Assertion to another.  The
    three exact sets retain their shape and therefore carry the completeness
    boundary of the reads that established them.  Count stands on
    the measured-in Assertion, and recurrence stands on count only where the
    count establishes recurrence.
    """

    subject = finding.distinction.to_json_dict()
    scope = {
        "bounded_localities": list(finding.bounded_localities),
        "declared_identity": dict(finding.distinction.declared),
    }

    def exact_set(
        result: str,
        localities: tuple[str, ...],
        support: tuple[str, ...],
        occurrence_kinds: tuple[str, ...],
    ) -> MeasuredAssertion:
        content = {"localities": list(localities)}
        return MeasuredAssertion(
            identity=_result_assertion_identity(finding, result, content),
            result=result,
            subject=subject,
            content=content,
            scope=scope,
            support_event_identities=support,
            completeness_boundary=finding.input_ledger_boundary,
            completeness_occurrence_kinds=occurrence_kinds,
        )

    measured_in = exact_set(
        "measured_in",
        finding.measured_in,
        finding.measured_in_support_event_identities,
        (MEASUREMENT_RECORDED_KIND,),
    )
    measured_without = exact_set(
        "measured_without_distinction",
        finding.measured_without_distinction,
        finding.measured_without_distinction_support_event_identities,
        (MEASUREMENT_RECORDED_KIND,),
    )
    coordinate_not_measured = exact_set(
        "coordinate_not_measured",
        finding.coordinate_not_measured,
        (),
        (MEASUREMENT_RECORDED_KIND,),
    )

    count_content = {"locality_count": finding.locality_count}
    count = MeasuredAssertion(
        identity=_result_assertion_identity(finding, "count", count_content),
        result="count",
        subject=subject,
        content=count_content,
        scope=scope,
        support_assertion_identities=(measured_in.identity,),
    )
    assertions = [
        measured_in,
        measured_without,
        coordinate_not_measured,
        count,
    ]
    if finding.recurrence_established:
        recurrence_content = {"recurrence_established": True}
        assertions.append(
            MeasuredAssertion(
                identity=_result_assertion_identity(
                    finding, "recurrence", recurrence_content
                ),
                result="recurrence",
                subject=subject,
                content=recurrence_content,
                scope=scope,
                support_assertion_identities=(count.identity,),
            )
        )
    return tuple(assertions)


def record_measured_count(
    ledger: EventLedger,
    *,
    locality_identity: str,
    finding: MeasuredCountFinding,
) -> Event:
    """Preserve exact Yield from one recurrence Measurement to its Assertions.

    Yield Evidence binds the exact responsible Measurement occurrence to
    these exact results. Each result Assertion separately bears Responsibility for preserving its
    Standing to its carried coordinates.
    """

    verified = measure_locality_counts(
        ledger,
        bounded_localities=finding.bounded_localities,
        through=finding.input_ledger_boundary,
    )
    if finding not in verified:
        raise RecurrenceMeasurementError(
            "the supplied locality count does not match its exact recorded inputs"
        )
    declared = dict(finding.distinction.declared)
    assertions = assertions_from_measured_count(finding)
    act_identity = new_identity("locality_count_measurement_act")
    act_occurrence_identity = new_identity("locality_count_measurement_act_occurrence")
    result_identity = new_identity("locality_count_measurement_result")
    participation = [
        {
            "subject_reference": event_identity,
            "role": "recorded Measurement occurrence",
            "act_occurrence_identity": act_occurrence_identity,
        }
        for event_identity in finding.input_occurrences
    ]
    result_material = {
        "result_identity": result_identity,
        "dimensions": {
            "identity": result_identity,
            "content": f"{len(assertions)} distinct measured Assertions recorded",
            "source_provenance": (
                "recorded comparison occurrences and recorded measurement "
                "occurrences"
            ),
            "authority": "unestablished",
            "evidence_scope": (
                "measurement evidence only; establishes no relation between the "
                "localities, no source independence, and no corroboration"
            ),
            "scope_locality": f"locality:{locality_identity}",
            "occurrence_preservation": "count finding durably recorded",
        },
        "assertions": [assertion.to_json_dict() for assertion in assertions],
        "downstream_act_identity": act_identity,
        "act_occurrence_identity": act_occurrence_identity,
        "participation": participation,
        "exact_act": "declared measurement",
        "occurrence_result_evidence": (
            "exact Yield Evidence for this recorded Measurement occurrence "
            "and the carried Assertions"
        ),
        "measurement_subject": (
            "recorded comparison occurrences and recorded measurement occurrences"
        ),
        "counting_scope": (
            "the bounded localities declared to this measurement; an locality "
            "outside the declaration is not counted, and no locality enters by "
            "having measured something else"
        ),
        "unknowns": [
            "what any measured representation means remains Unknown",
            "whether the localities stand in any relation remains Unknown",
            "whether their sources are independent remains Unknown",
        ],
        "limits": list(LIMITS),
    }
    act_evidence = ledger.append(
        LOCALITY_COUNT_ACT_EVIDENCE_KIND,
        {
            "downstream_act_identity": act_identity,
            "act_occurrence_identity": act_occurrence_identity,
            "act": "locality count Measurement",
            "responsibility": LOCALITY_COUNT_RESPONSIBILITY,
            "responsible_boundary": "this Seed",
            "participation": participation,
            "authority": "unestablished",
            "evidence_scope": "this exact locality count Measurement occurrence only",
        },
        locality_identity=locality_identity,
    )
    yield_evidence = _record_yield_evidence(
        ledger,
        locality_identity=locality_identity,
        exact_act="locality count Measurement",
        act_occurrence_identity=act_occurrence_identity,
        result_kind=LOCALITY_COUNT_RESULT_KIND,
        result_identity=result_identity,
        result_content=result_material,
        responsibility=LOCALITY_COUNT_RESPONSIBILITY,
        live_boundary="locality_count_measurement",
        responsible_boundary="this Seed",
        recorded_result_coordinates={key: (key,) for key in result_material},
    )
    return ledger.append(
        LOCALITY_COUNT_RECORDED_KIND,
        {
            **result_material,
            "responsible_act_evidence_identity": act_evidence.identity,
            "yield_evidence_identity": yield_evidence.identity,
        },
        locality_identity=locality_identity,
    )
