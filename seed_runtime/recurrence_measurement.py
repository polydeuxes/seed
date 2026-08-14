"""Declared measurement whose subject is Seed's own recorded occurrences.

**No new Act.** `#2351` reconstructed declared measurement and said no new act,
noun, or grammar is required; recurrence and count are already its findings.
This measures a different subject — recorded comparison and measurement
occurrences instead of preserved material — and produces an exact count of the
bounded exchanges a distinction was measured in. Recurrence is one reading of
that count, established only where the count exceeds one.
A distinct record shape is established (`#2399`: a downstream shape must not
decide an upstream subject); a distinct Responsibility is not.

`#2429` called this a "cohort measurement" and wrote
`cohort-measurement-over-recorded-comparisons` into every record. That named a
Responsibility nothing established, and `cohort`, `inputs`, `body` and
`survey` were statistical vocabulary the grammar never needed. What the act
reports is:

```text
this measured distinction was measured in N of the declared bounded exchanges
under the declared rule and Scope
```

and recurrence is asserted only where N exceeds one.

**Its result stands on both recorded kinds.** Recorded comparison occurrences
say which exchanges measured the distinction. Recorded measurement occurrences
say which exchanges measured the coordinate at all. Neither answers alone, so
every occurrence of both kinds that produced the result travels as Evidence —
`#2419` holds that preservation must not erase what a result stood on, and
`#2429` recorded only the comparisons.

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

from seed_runtime.bounded_assertion_comparison import COMPARISON_RECORDED_KIND
from seed_runtime.events import EventLedger, EventLedgerBoundary
from seed_runtime.event import Event
from seed_runtime.preserved_material_measurement import MEASUREMENT_RECORDED_KIND

EXCHANGE_COUNT_RECORDED_KIND = "operator.measurement.exchange_count_recorded"

MEASURED_ASSERTION_FIDELITY_RESPONSIBILITY = (
    "preserve the fidelity of this measured Assertion's Standing to its "
    "carried coordinates"
)

# The declared identity a recurrence assertion is made under. Two occurrences
# that differ on any of these did not measure the same thing, and counting them
# together reports a recurrence nothing observed.
DECLARED_IDENTITY: tuple[str, ...] = (
    "representation_measured",
    "measured_left_representation",
    "equivalence_rule",
    "counting_scope",
    "measured_position",
    "measurement_form",
)

FORBIDDEN_INFERENCES: tuple[str, ...] = (
    "independently preserved is not independent; nothing here establishes that "
    "the exchanges' sources are unrelated",
    "recurrence is repetition, and repetition is not independent corroboration",
    "an exact count is a finding at any value; a count of one establishes no "
    "recurrence",
    "the count reports the bounded exchanges among the occurrences this "
    "measurement input, not a property of the material",
    "an exchange that never measured the coordinate has not declined to measure "
    "the distinction",
    "measuring the same distinction establishes no relation between the "
    "exchanges that measured it",
)


class RecurrenceMeasurementError(Exception):
    """The measurement boundary could not be instantiated."""


@dataclass(frozen=True)
class MeasuredDistinction:
    """What was measured, under the whole declared identity it was measured with."""

    right_representation: str
    declared: tuple[tuple[str, str], ...]

    def to_json_dict(self) -> dict[str, Any]:
        return {
            "right_representation": self.right_representation,
            **{name: value for name, value in self.declared},
        }

    @property
    def left(self) -> str:
        return dict(self.declared).get("measured_left_representation", "")


@dataclass(frozen=True)
class MeasuredCountFinding:
    """One exact count over recorded occurrences. A record shape, not a kind.

    `01.Source:28` lists **count** and **recurrence** as separate findings of
    a declared measurement. `#2430` named this shape `RecurrenceFinding` and
    rendered a count of one as "recurs in 1 bounded exchanges", which asserts
    recurrence where nothing recurred. The count is the finding; recurrence is
    established only where the count establishes it.
    """

    distinction: MeasuredDistinction
    measured_in: tuple[str, ...]
    measured_without_distinction: tuple[str, ...]
    coordinate_not_measured: tuple[str, ...]
    input_event_ids: tuple[str, ...]
    input_ledger_boundary: EventLedgerBoundary
    workspace_id: str
    bounded_exchanges: tuple[str, ...]
    measured_in_support_event_ids: tuple[str, ...] = ()
    measured_without_distinction_support_event_ids: tuple[str, ...] = ()

    @property
    def exchange_count(self) -> int:
        """The exact count. Always a finding, at any value."""
        return len(self.measured_in)

    @property
    def recurrence_established(self) -> bool:
        """Recurrence needs something to have recurred."""
        return self.exchange_count > 1

    def to_json_dict(self) -> dict[str, Any]:
        return {
            "distinction": self.distinction.to_json_dict(),
            "measured_in": list(self.measured_in),
            "measured_without_distinction": list(self.measured_without_distinction),
            "coordinate_not_measured": list(self.coordinate_not_measured),
            "exchange_count": self.exchange_count,
            "recurrence_established": self.recurrence_established,
            "bounded_exchanges": list(self.bounded_exchanges),
            "workspace_id": self.workspace_id,
            "input_event_ids": list(self.input_event_ids),
            "input_ledger_boundary": {
                "commitment": self.input_ledger_boundary.commitment,
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
    support_event_ids: tuple[str, ...] = ()
    support_assertion_ids: tuple[str, ...] = ()
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
                "responsibility": MEASURED_ASSERTION_FIDELITY_RESPONSIBILITY,
                "authority": (
                    "measurement evidence only; establishes no relation between "
                    "the exchanges, no source independence, and no corroboration"
                ),
                "scope_locality": "the exact assertion_scope carried here",
                "occurrence_preservation": (
                    "distinct result preserved by its producing occurrence"
                ),
            },
            "subject_kind": "assertion",
            "responsible_boundary": "this recorded assertion",
            "result": self.result,
            "assertion_subject": dict(self.subject),
            "assertion_scope": dict(self.scope),
            "support_basis": {
                "event_ids": list(self.support_event_ids),
                # These dependencies are local to the same producing
                # occurrence. Reconstruction binds each to that occurrence's id
                # before exposing it to a downstream Act.
                "local_assertion_ids": list(self.support_assertion_ids),
            },
            "completeness_boundary": (
                {"commitment": self.completeness_boundary.commitment}
                if self.completeness_boundary is not None
                else None
            ),
            "completeness_scope": (
                {
                    "workspace_id": self.scope["workspace_id"],
                    "session_ids": list(self.scope["bounded_exchanges"]),
                    "occurrence_kinds": list(self.completeness_occurrence_kinds),
                    "requires_session_existence": True,
                }
                if self.completeness_boundary is not None
                else None
            ),
            "unknowns": [
                "what any measured representation means remains Unknown",
                "whether the exchanges stand in any relation remains Unknown",
                "whether their sources are independent remains Unknown",
            ],
            "forbidden_inferences": list(FORBIDDEN_INFERENCES),
        }


@dataclass(frozen=True)
class RecordedMeasuredAssertion:
    """One addressable Assertion preserved inside its producing occurrence."""

    assertion_id: str
    producing_event_id: str
    producing_session_id: str | None
    result: str
    payload: dict[str, Any]
    support_assertion_refs: tuple[dict[str, str], ...] = ()

    @property
    def reference(self) -> dict[str, str]:
        return {
            "assertion_id": self.assertion_id,
            "producing_event_id": self.producing_event_id,
        }


def assertions_of_recorded_measurement(event: Event) -> tuple[RecordedMeasuredAssertion, ...]:
    """Reconstruct every Assertion from one exact producing occurrence."""

    if event.kind != EXCHANGE_COUNT_RECORDED_KIND:
        raise RecurrenceMeasurementError(
            f"{event.id} is {event.kind}, not a recurrence Measurement occurrence"
        )
    stated = event.payload.get("assertions")
    if not isinstance(stated, list):
        raise RecurrenceMeasurementError(
            f"{event.id} does not preserve its distinct Assertions"
        )
    reconstructed = []
    seen = set()
    for assertion in stated:
        if not isinstance(assertion, dict):
            raise RecurrenceMeasurementError(
                f"{event.id} carries a non-object Assertion representation"
            )
        dimensions = assertion.get("dimensions")
        identity = dimensions.get("identity") if isinstance(dimensions, dict) else None
        content = dimensions.get("content") if isinstance(dimensions, dict) else None
        result = assertion.get("result")
        subject = assertion.get("assertion_subject")
        scope = assertion.get("assertion_scope")
        if assertion.get("subject_kind") != "assertion":
            raise RecurrenceMeasurementError(
                f"{event.id} carries a result that is not identified as an Assertion"
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
                f"{event.id} carries an Assertion without exact identity, result, "
                "subject, scope, and content"
            )
        workspace_id = scope.get("workspace_id")
        bounded_exchanges = scope.get("bounded_exchanges")
        declared_identity = scope.get("declared_identity")
        if (
            not isinstance(workspace_id, str)
            or not workspace_id
            or not isinstance(bounded_exchanges, list)
            or not all(isinstance(value, str) for value in bounded_exchanges)
            or not isinstance(declared_identity, dict)
            or any(subject.get(name) != value for name, value in declared_identity.items())
        ):
            raise RecurrenceMeasurementError(
                f"{event.id} carries an Assertion without coherent bounded scope"
            )
        canonical = _canonical_measured_assertion_identity(
            result=result,
            subject=subject,
            workspace_id=workspace_id,
            bounded_exchanges=bounded_exchanges,
            content=content,
        )
        if identity != canonical:
            raise RecurrenceMeasurementError(
                f"{event.id} carries an Assertion identity that does not match "
                "its carried coordinates"
            )
        if identity in seen:
            raise RecurrenceMeasurementError(
                f"{event.id} carries duplicate Assertion identity {identity}"
            )
        seen.add(identity)
        reconstructed.append(
            RecordedMeasuredAssertion(
                assertion_id=identity,
                producing_event_id=event.id,
                producing_session_id=event.session_id,
                result=result,
                payload=assertion,
            )
        )
    identities = {assertion.assertion_id for assertion in reconstructed}
    by_result = {}
    for assertion in reconstructed:
        if assertion.result in by_result:
            raise RecurrenceMeasurementError(
                f"{event.id} carries duplicate Assertion result {assertion.result}"
            )
        by_result[assertion.result] = assertion
    bound = []
    for assertion in reconstructed:
        support = assertion.payload.get("support_basis")
        local_ids = support.get("local_assertion_ids") if isinstance(support, dict) else None
        if not isinstance(local_ids, list) or not all(
            isinstance(value, str) for value in local_ids
        ):
            raise RecurrenceMeasurementError(
                f"{event.id} carries an Assertion without local Assertion support"
            )
        missing = set(local_ids) - identities
        if missing:
            raise RecurrenceMeasurementError(
                f"{event.id} carries unresolved local Assertion support: "
                f"{', '.join(sorted(missing))}"
            )
        if assertion.result == "count":
            measured_in = by_result.get("measured_in")
            expected_local_ids = (
                [measured_in.assertion_id] if measured_in is not None else []
            )
        elif assertion.result == "recurrence":
            count = by_result.get("count")
            expected_local_ids = [count.assertion_id] if count is not None else []
        else:
            expected_local_ids = []
        if local_ids != expected_local_ids:
            raise RecurrenceMeasurementError(
                f"{event.id} carries {assertion.result} with the wrong local "
                "Assertion support"
            )
        bound.append(
            RecordedMeasuredAssertion(
                assertion_id=assertion.assertion_id,
                producing_event_id=assertion.producing_event_id,
                producing_session_id=assertion.producing_session_id,
                result=assertion.result,
                payload=assertion.payload,
                support_assertion_refs=tuple(
                    {
                        "producing_event_id": event.id,
                        "assertion_id": local_id,
                    }
                    for local_id in local_ids
                ),
            )
        )
    return tuple(bound)


def iter_recorded_measured_assertions(
    ledger: EventLedger,
    *,
    workspace_id: str,
    session_ids: Iterable[str],
    through: EventLedgerBoundary | None = None,
) -> Iterator[RecordedMeasuredAssertion]:
    """Stream Assertions from exact declared sessions through one boundary."""

    for session_id in tuple(dict.fromkeys(session_ids)):
        for event in ledger.iter_session_kind(
            workspace_id,
            session_id,
            EXCHANGE_COUNT_RECORDED_KIND,
            through=through,
        ):
            yield from assertions_of_recorded_measurement(event)


def get_recorded_measured_assertion(
    ledger: EventLedger, *, producing_event_id: str, assertion_id: str
) -> RecordedMeasuredAssertion | None:
    """Resolve one exact occurrence-bound Assertion reference."""

    event = ledger.get(producing_event_id)
    if event is None:
        return None
    for assertion in assertions_of_recorded_measurement(event):
        if assertion.assertion_id == assertion_id:
            return assertion
    return None


def occurrences_of_declared_exchanges(
    ledger: EventLedger, *, workspace_id: str, bounded_exchanges: Iterable[str]
) -> Iterator[tuple[str, list[Event]]]:
    """Yield each declared exchange's occurrences for compatibility.

    Recurrence measurement no longer has as input this list-returning helper: its
    two passes use ``iter_session_kind`` so comparison Events are folded one at
    a time. Existing callers that require the complete occurrences of one
    exchange retain the per-exchange API introduced by ``#2441``.
    """
    for exchange in bounded_exchanges:
        yield exchange, ledger.list_session(workspace_id, exchange)


def _declared_of_measurement(event: Event) -> tuple[tuple[str, str], ...] | None:
    declared = []
    for name in DECLARED_IDENTITY:
        if name not in event.payload:
            return None
        declared.append((name, str(event.payload[name])))
    return tuple(declared)


def _declared_of_comparison(event: Event) -> tuple[tuple[str, str], ...] | None:
    """The declared identity, only where both inputs declared it identically."""
    stated = {d["coordinate"]: d for d in event.payload.get("distinctions", [])}
    declared = []
    for name in DECLARED_IDENTITY:
        distinction = stated.get(name)
        if distinction is None or not distinction["same"]:
            return None
        declared.append((name, str(distinction["values"][0])))
    return tuple(declared)


def measure_exchange_counts(
    ledger: EventLedger, *, workspace_id: str, bounded_exchanges: Iterable[str]
) -> list[MeasuredCountFinding]:
    """Count, over recorded occurrences, the exchanges each distinction was measured in.

    `bounded_exchanges` is required and is the declared scope. `#2430` swept
    every measurement in the workspace instead, so an exchange entered the
    denominator by having measured anything at all — a measurement of
    ``"nothing"`` set the denominator of a finding about ``"a"``. That is
    workspace visibility choosing Applicability. `01.Source:28` requires a
    recurrence assertion to disclose the bounded scope within which occurrences
    were counted, and a swept scope is not a declared one.

    A comparison is recorded under one exchange's session while using a
    finding from another, so no session-local mode is offered.
    """

    declared_exchanges = tuple(sorted(set(bounded_exchanges)))
    if not declared_exchanges:
        raise RecurrenceMeasurementError(
            "a declared measurement discloses the bounded scope within which "
            "occurrences were counted; no bounded exchanges were declared"
        )
    # Every probe and both occurrence passes have as input one ledger-local append
    # prefix. The boundary is carried as read provenance; it is not an Event
    # identity and does not strengthen the occurrences read through it.
    input_ledger_boundary = ledger.capture_boundary()
    # Declaring the Scope chooses which established exchanges this measurement
    # concerns. It does not establish them: a recorded occurrence within the
    # session boundary does. Each declared exchange is read through that exact
    # boundary, so the existence check costs one bounded read per declared
    # exchange rather than a pass over the workspace.
    # Pass one retains only compact indexes reconstructed from Measurement. Compare
    # names its inputs by measurement occurrence id, so those indexes must exist
    # before any comparison can be folded. The existence probe remains separate:
    # declaration chooses among established sessions, and a non-measurement
    # occurrence can establish a session without supplying a measured coordinate.
    measured_coordinate: dict[tuple, set[str]] = {}
    coordinate_evidence: dict[tuple, dict[str, set[str]]] = {}
    session_of: dict[str, str] = {}
    unestablished: list[str] = []

    for exchange in declared_exchanges:
        if not ledger.has_session(
            workspace_id, exchange, through=input_ledger_boundary
        ):
            unestablished.append(exchange)
            continue
        for event in ledger.iter_session_kind(
            workspace_id,
            exchange,
            MEASUREMENT_RECORDED_KIND,
            through=input_ledger_boundary,
        ):
            session_of[event.id] = exchange
            declared = _declared_of_measurement(event)
            if declared is None:
                continue
            measured_coordinate.setdefault(declared, set()).add(exchange)
            coordinate_evidence.setdefault(declared, {}).setdefault(
                exchange, set()
            ).add(event.id)

    if unestablished:
        raise RecurrenceMeasurementError(
            "declared bounded exchanges with no recorded occurrence: "
            f"{', '.join(unestablished)}. Declaring a measurement's Scope "
            "chooses among established exchanges; it does not establish them"
        )
    # Pass two folds each Compare occurrence into the aggregates immediately.
    # No comparison Event survives the iteration that supplied it.
    recurs: dict[MeasuredDistinction, set[str]] = {}
    support: dict[MeasuredDistinction, set[str]] = {}
    comparison_seen = False
    for exchange in declared_exchanges:
        for event in ledger.iter_session_kind(
            workspace_id,
            exchange,
            COMPARISON_RECORDED_KIND,
            through=input_ledger_boundary,
        ):
            comparison_seen = True
            declared = _declared_of_comparison(event)
            if declared is None:
                continue
            inputs = event.payload.get("inputs", [])
            # An input's exchange is the recorded session of the occurrence it
            # names, reconstructed from pass one's compact measurement index.
            exchanges = [session_of.get(i.get("event_id")) for i in inputs]
            if any(x is None or x not in declared_exchanges for x in exchanges):
                continue
            by_event = {i["event_id"]: x for i, x in zip(inputs, exchanges)}

            def note(right: str, where: list[str]) -> None:
                key = MeasuredDistinction(
                    right_representation=right, declared=declared
                )
                recurs.setdefault(key, set()).update(where)
                support.setdefault(key, set()).add(event.id)
                support[key].update(i["event_id"] for i in inputs)

            for right in event.payload.get("shared_occupants", []):
                note(right, exchanges)
            for event_id, occupants in event.payload.get(
                "occupants_in_one_only", {}
            ).items():
                for right in occupants:
                    note(right, [by_event[event_id]])

    if not comparison_seen:
        raise RecurrenceMeasurementError(
            "no recorded comparison occurrences to measure; this measurement's "
            "subject is what Compare and Measurement recorded, not preserved "
            "material"
        )

    findings = []
    declared_set = set(declared_exchanges)
    for key in sorted(
        recurs, key=lambda k: (-len(recurs[k]), k.left, k.right_representation)
    ):
        where = recurs[key]
        measured = measured_coordinate.get(key.declared, set())
        not_measured = declared_set - measured
        measured_without = measured - where
        measured_without_evidence = {
            event_id
            for exchange in measured_without
            for event_id in coordinate_evidence.get(key.declared, {}).get(
                exchange, set()
            )
        }
        measured_in_evidence = set(support[key])
        evidence = measured_in_evidence | measured_without_evidence
        # The third result stands on the complete Measurement-kind read for
        # each declared exchange through the preserved ledger boundary. Copying
        # every unrelated Measurement id into every negative finding neither
        # establishes nor strengthens that completeness. Exact-coordinate,
        # Compare, and comparison-input Evidence remain carried below.
        findings.append(
            MeasuredCountFinding(
                distinction=key,
                measured_in=tuple(sorted(where)),
                measured_without_distinction=tuple(sorted(measured_without)),
                coordinate_not_measured=tuple(sorted(not_measured)),
                input_event_ids=tuple(sorted(evidence)),
                input_ledger_boundary=input_ledger_boundary,
                workspace_id=workspace_id,
                bounded_exchanges=declared_exchanges,
                measured_in_support_event_ids=tuple(
                    sorted(measured_in_evidence)
                ),
                measured_without_distinction_support_event_ids=tuple(
                    sorted(measured_without_evidence)
                ),
            )
        )
    return findings


def render_measured_count(finding: MeasuredCountFinding) -> str:
    """The literal sentence, and nothing stronger.

    A count of one says it was measured in one exchange. It does not say it
    recurred, because it did not.
    """

    declared = dict(finding.distinction.declared)
    verb = "recurs in" if finding.recurrence_established else "was measured in"
    exchanges = "exchange" if finding.exchange_count == 1 else "exchanges"
    return (
        f"({declared['measured_left_representation']!r}, "
        f"{finding.distinction.right_representation!r}) {verb} "
        f"{finding.exchange_count} bounded {exchanges} of "
        f"{len(finding.bounded_exchanges)} declared, at "
        f"{declared['measured_position']} under "
        f"{declared['equivalence_rule']} within {declared['counting_scope']}"
    )


def _canonical_measured_assertion_identity(
    *,
    result: str,
    subject: dict[str, Any],
    workspace_id: str,
    bounded_exchanges: Iterable[str],
    content: dict[str, Any],
) -> str:
    identified = {
        "result": result,
        "distinction": subject,
        "workspace_id": workspace_id,
        "bounded_exchanges": list(bounded_exchanges),
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
        workspace_id=finding.workspace_id,
        bounded_exchanges=finding.bounded_exchanges,
        content=content,
    )


def assertions_from_measured_count(
    finding: MeasuredCountFinding,
) -> tuple[MeasuredAssertion, ...]:
    """Every distinct result this recurrence Measurement already established.

    This is result fan-out, not inference from one Assertion to another.  The
    three classifications retain their exact-set shape and therefore carry the
    completeness boundary of the reads that produced them.  Count stands on
    the measured-in Assertion, and recurrence stands on count only where the
    count establishes recurrence.
    """

    subject = finding.distinction.to_json_dict()
    scope = {
        "workspace_id": finding.workspace_id,
        "bounded_exchanges": list(finding.bounded_exchanges),
        "declared_identity": dict(finding.distinction.declared),
    }

    def exact_set(
        result: str,
        exchanges: tuple[str, ...],
        support: tuple[str, ...],
        occurrence_kinds: tuple[str, ...],
    ) -> MeasuredAssertion:
        content = {"exchanges": list(exchanges)}
        return MeasuredAssertion(
            identity=_result_assertion_identity(finding, result, content),
            result=result,
            subject=subject,
            content=content,
            scope=scope,
            support_event_ids=support,
            completeness_boundary=finding.input_ledger_boundary,
            completeness_occurrence_kinds=occurrence_kinds,
        )

    measured_in = exact_set(
        "measured_in",
        finding.measured_in,
        finding.measured_in_support_event_ids,
        (COMPARISON_RECORDED_KIND,),
    )
    measured_without = exact_set(
        "measured_without_distinction",
        finding.measured_without_distinction,
        finding.measured_without_distinction_support_event_ids,
        (MEASUREMENT_RECORDED_KIND, COMPARISON_RECORDED_KIND),
    )
    coordinate_not_measured = exact_set(
        "coordinate_not_measured",
        finding.coordinate_not_measured,
        (),
        (MEASUREMENT_RECORDED_KIND,),
    )

    count_content = {"exchange_count": finding.exchange_count}
    count = MeasuredAssertion(
        identity=_result_assertion_identity(finding, "count", count_content),
        result="count",
        subject=subject,
        content=count_content,
        scope=scope,
        support_assertion_ids=(measured_in.identity,),
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
                support_assertion_ids=(count.identity,),
            )
        )
    return tuple(assertions)


def record_measured_count(
    ledger: EventLedger,
    *,
    workspace_id: str,
    session_id: str,
    finding: MeasuredCountFinding,
) -> Event:
    """Preserve the distinct Assertions one recurrence Measurement produced.

    Production Evidence binds the exact responsible Measurement occurrence to
    these exact results. Each result Assertion separately bears Responsibility for fidelity of its
    Standing to its carried coordinates.
    """

    declared = dict(finding.distinction.declared)
    assertions = assertions_from_measured_count(finding)
    payload = {
        "dimensions": {
            "identity": "declared-measurement-result-occurrence",
            "content": f"{len(assertions)} distinct measured Assertions recorded",
            "standing": "recorded",
            "source_provenance": (
                "recorded comparison occurrences and recorded measurement "
                "occurrences"
            ),
            "authority": (
                "measurement evidence only; establishes no relation between the "
                "exchanges, no source independence, and no corroboration"
            ),
            "scope_locality": f"workspace:{workspace_id};session:{session_id}",
            "occurrence_preservation": "count finding durably recorded",
        },
        "assertions": [assertion.to_json_dict() for assertion in assertions],
        "producing_act": "declared measurement",
        "production_occurrence_evidence": (
            "the recorded producing occurrence this payload is appended as"
        ),
        "measurement_subject": (
            "recorded comparison occurrences and recorded measurement occurrences"
        ),
        "counting_scope": (
            "the bounded exchanges declared to this measurement; an exchange "
            "outside the declaration is not counted, and no exchange enters by "
            "having measured something else"
        ),
        "mutates_cluster": False,
        "unknowns": [
            "what any measured representation means remains Unknown",
            "whether the exchanges stand in any relation remains Unknown",
            "whether their sources are independent remains Unknown",
        ],
        "forbidden_inferences": list(FORBIDDEN_INFERENCES),
    }
    return ledger.append(
        EXCHANGE_COUNT_RECORDED_KIND, workspace_id, payload, session_id=session_id
    )
