"""Declared measurement whose subject is Seed's own recorded occurrences.

**No new Act.** `#2351` recovered declared measurement and said no new act,
noun, or grammar is required; recurrence and count are already its findings.
This measures a different subject — recorded comparison and measurement
occurrences instead of preserved material — and produces an exact count of the
bounded exchanges a distinction was measured in. Recurrence is one reading of
that count, warranted only where the count exceeds one.
A distinct record shape is warranted (`#2399`: a downstream shape must not
decide an upstream subject); a distinct Responsibility is not.

`#2429` called this a "cohort measurement" and wrote
`cohort-measurement-over-recorded-comparisons` into every record. That named a
Responsibility nothing established, and `cohort`, `population`, `body` and
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
`01.External:28` requires the measured representation, the sameness rule and
the bounded scope to travel with a recurrence assertion.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable

from seed_runtime.bounded_testimony_comparison import COMPARISON_RECORDED_KIND
from seed_runtime.events import EventLedger
from seed_runtime.models import Event
from seed_runtime.preserved_material_measurement import MEASUREMENT_RECORDED_KIND

EXCHANGE_COUNT_RECORDED_KIND = "operator.measurement.exchange_count_recorded"

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
    "measurement consumed, not a property of the material",
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

    `01.External:28` lists **count** and **recurrence** as separate findings of
    a declared measurement. `#2430` named this shape `RecurrenceFinding` and
    rendered a count of one as "recurs in 1 bounded exchanges", which asserts
    recurrence where nothing recurred. The count is the finding; recurrence is
    warranted only where the count establishes it.
    """

    distinction: MeasuredDistinction
    measured_in: tuple[str, ...]
    measured_without_distinction: tuple[str, ...]
    coordinate_not_measured: tuple[str, ...]
    consumed_event_ids: tuple[str, ...]
    bounded_exchanges: tuple[str, ...]

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
            "consumed_event_ids": list(self.consumed_event_ids),
        }


def occurrences_of_declared_exchanges(
    ledger: EventLedger, *, workspace_id: str, bounded_exchanges: Iterable[str]
) -> dict[str, list[Event]]:
    """Each declared exchange's recorded occurrences, read one session at a time.

    A bounded exchange **is** the recorded session boundary the durable-console
    work established. `#2432` established existence from
    `dimensions.scope_locality` — a payload description whose meaning that same
    report left Unknown — and read `ledger.list(workspace_id)` to do it, which
    is the whole-workspace-read shape `#2416` removed and measured at 20x.
    """

    return {
        exchange: ledger.list_session(workspace_id, exchange)
        for exchange in bounded_exchanges
    }


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


def _exchange_of(event: Event) -> str | None:
    """The recorded session boundary, a top-level coordinate of the occurrence."""
    return event.session_id


def measure_exchange_counts(
    ledger: EventLedger, *, workspace_id: str, bounded_exchanges: Iterable[str]
) -> list[MeasuredCountFinding]:
    """Count, over recorded occurrences, the exchanges each distinction was measured in.

    `bounded_exchanges` is required and is the declared scope. `#2430` swept
    every measurement in the workspace instead, so an exchange entered the
    denominator by having measured anything at all — a measurement of
    ``"nothing"`` set the denominator of a finding about ``"a"``. That is
    workspace visibility choosing Applicability. `01.External:28` requires a
    recurrence assertion to disclose the bounded scope within which occurrences
    were counted, and a swept scope is not a declared one.

    A comparison is recorded under one exchange's session while consuming a
    finding from another, so no session-local mode is offered.
    """

    declared_exchanges = tuple(sorted(set(bounded_exchanges)))
    if not declared_exchanges:
        raise RecurrenceMeasurementError(
            "a declared measurement discloses the bounded scope within which "
            "occurrences were counted; no bounded exchanges were declared"
        )
    # Declaring the Scope chooses which established exchanges this measurement
    # concerns. It does not establish them: a recorded occurrence within the
    # session boundary does. Each declared exchange is read through that exact
    # boundary, so the existence check costs one bounded read per declared
    # exchange rather than a pass over the workspace.
    by_exchange = occurrences_of_declared_exchanges(
        ledger, workspace_id=workspace_id, bounded_exchanges=declared_exchanges
    )
    unestablished = [x for x in declared_exchanges if not by_exchange[x]]
    if unestablished:
        raise RecurrenceMeasurementError(
            "declared bounded exchanges with no recorded occurrence: "
            f"{', '.join(unestablished)}. Declaring a measurement's Scope "
            "chooses among established exchanges; it does not establish them"
        )
    occurrences = [e for events in by_exchange.values() for e in events]
    comparisons = [e for e in occurrences if e.kind == COMPARISON_RECORDED_KIND]
    measurements = [e for e in occurrences if e.kind == MEASUREMENT_RECORDED_KIND]
    session_of = {e.id: _exchange_of(e) for e in measurements}
    if not comparisons:
        raise RecurrenceMeasurementError(
            "no recorded comparison occurrences to measure; this measurement's "
            "subject is what Compare and Measurement recorded, not preserved "
            "material"
        )

    # Which exchanges measured each declared identity at all, and the exact
    # occurrences that say so. Both travel: the second is this result's support.
    measured_coordinate: dict[tuple, set[str]] = {}
    coordinate_evidence: dict[tuple, set[str]] = {}
    # Every occurrence that establishes where a declared exchange stands in the
    # result travels with it. `#2430` cited only the occurrences matching the
    # grouped identity, so an exchange could be placed in
    # `coordinate_not_measured` by an occurrence absent from the support.
    presence_evidence: dict[str, set[str]] = {}
    for event in measurements:
        exchange = _exchange_of(event)
        if exchange is None or exchange not in declared_exchanges:
            continue
        presence_evidence.setdefault(exchange, set()).add(event.id)
        declared = _declared_of_measurement(event)
        if declared is None:
            continue
        measured_coordinate.setdefault(declared, set()).add(exchange)
        coordinate_evidence.setdefault(declared, set()).add(event.id)

    recurs: dict[MeasuredDistinction, set[str]] = {}
    support: dict[MeasuredDistinction, set[str]] = {}
    for event in comparisons:
        declared = _declared_of_comparison(event)
        if declared is None:
            continue
        inputs = event.payload.get("inputs", [])
        # An input's exchange is the recorded session of the occurrence it
        # names, recovered from the measurements already read.
        exchanges = [session_of.get(i.get("event_id")) for i in inputs]
        if any(x is None or x not in declared_exchanges for x in exchanges):
            continue
        by_event = {i["event_id"]: x for i, x in zip(inputs, exchanges)}

        def note(right: str, where: list[str]) -> None:
            key = MeasuredDistinction(right_representation=right, declared=declared)
            recurs.setdefault(key, set()).update(where)
            support.setdefault(key, set()).add(event.id)
            support[key].update(coordinate_evidence.get(declared, set()))
            support[key].update(i["event_id"] for i in inputs)

        for right in event.payload.get("shared_occupants", []):
            note(right, exchanges)
        for event_id, occupants in event.payload.get(
            "occupants_in_one_only", {}
        ).items():
            for right in occupants:
                note(right, [by_event[event_id]])

    findings = []
    declared_set = set(declared_exchanges)
    for key in sorted(
        recurs, key=lambda k: (-len(recurs[k]), k.left, k.right_representation)
    ):
        where = recurs[key]
        measured = measured_coordinate.get(key.declared, set())
        not_measured = declared_set - measured
        evidence = set(support[key])
        # the occurrences that placed each exchange in the third result
        for exchange in not_measured | (measured - where):
            evidence.update(presence_evidence.get(exchange, set()))
        findings.append(
            MeasuredCountFinding(
                distinction=key,
                measured_in=tuple(sorted(where)),
                measured_without_distinction=tuple(sorted(measured - where)),
                coordinate_not_measured=tuple(sorted(not_measured)),
                consumed_event_ids=tuple(sorted(evidence)),
                bounded_exchanges=declared_exchanges,
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


def record_measured_count(
    ledger: EventLedger,
    *,
    workspace_id: str,
    session_id: str,
    finding: MeasuredCountFinding,
) -> Event:
    """Preserve one count finding so a later responsible act may consume it."""

    declared = dict(finding.distinction.declared)
    payload = {
        "dimensions": {
            "identity": (
                f"exchange-count:{declared['measured_left_representation']}"
                f"|{finding.distinction.right_representation}"
            ),
            "content": render_measured_count(finding),
            "standing": "measured",
            "source_provenance": (
                "recorded comparison occurrences and recorded measurement "
                "occurrences"
            ),
            # Not the Act. `#2423` recovered that declared measurement has
            # **no production owner in active law** — "the act that would
            # produce the finding has no named owner". Writing the Act here
            # would assert the owner that recovery says is absent, which is
            # what `#2430` did after removing an invented Responsibility.
            "responsibility": (
                "unrecovered; declared measurement has no production owner in "
                "active law (#2423)"
            ),
            "authority_warrant": (
                "measurement evidence only; establishes no relation between the "
                "exchanges, no source independence, and no corroboration"
            ),
            "scope_locality": f"workspace:{workspace_id};session:{session_id}",
            "occurrence_preservation": "count finding durably recorded",
        },
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
        **finding.to_json_dict(),
    }
    return ledger.append(
        EXCHANGE_COUNT_RECORDED_KIND, workspace_id, payload, session_id=session_id
    )
