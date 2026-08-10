"""Declared measurement whose subject is Seed's own recorded occurrences.

**No new Act.** `#2351` recovered declared measurement and said no new act,
noun, or grammar is required; recurrence and count are already its findings.
This measures a different subject — recorded comparison and measurement
occurrences instead of preserved material — and produces a recurrence finding.
A distinct record shape is warranted (`#2399`: a downstream shape must not
decide an upstream subject); a distinct Responsibility is not.

`#2429` called this a "cohort measurement" and wrote
`cohort-measurement-over-recorded-comparisons` into every record. That named a
Responsibility nothing established, and `cohort`, `population`, `body` and
`survey` were statistical vocabulary the grammar never needed. What the act
reports is:

```text
this measured distinction recurs in N bounded exchanges
under the declared rule and Scope
```

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
from typing import Any

from seed_runtime.bounded_testimony_comparison import COMPARISON_RECORDED_KIND
from seed_runtime.events import EventLedger
from seed_runtime.models import Event
from seed_runtime.preserved_material_measurement import MEASUREMENT_RECORDED_KIND

RECURRENCE_RECORDED_KIND = "operator.measurement.recurrence_recorded"

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
    """What recurred, under the whole declared identity it was measured with."""

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
class RecurrenceFinding:
    """One bounded count over recorded occurrences. A record shape, not a kind."""

    distinction: MeasuredDistinction
    measured_in: tuple[str, ...]
    measured_without_distinction: tuple[str, ...]
    coordinate_not_measured: tuple[str, ...]
    consumed_event_ids: tuple[str, ...]
    bounded_exchanges: tuple[str, ...]

    @property
    def recurrence_count(self) -> int:
        return len(self.measured_in)

    def to_json_dict(self) -> dict[str, Any]:
        return {
            "distinction": self.distinction.to_json_dict(),
            "measured_in": list(self.measured_in),
            "measured_without_distinction": list(self.measured_without_distinction),
            "coordinate_not_measured": list(self.coordinate_not_measured),
            "recurrence_count": self.recurrence_count,
            "bounded_exchanges": list(self.bounded_exchanges),
            "consumed_event_ids": list(self.consumed_event_ids),
        }


def recorded_comparison_occurrences(
    ledger: EventLedger, *, workspace_id: str
) -> list[Event]:
    return [
        e for e in ledger.list(workspace_id) if e.kind == COMPARISON_RECORDED_KIND
    ]


def recorded_measurement_occurrences(
    ledger: EventLedger, *, workspace_id: str
) -> list[Event]:
    return [
        e for e in ledger.list(workspace_id) if e.kind == MEASUREMENT_RECORDED_KIND
    ]


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


def _exchange_of(preserved: dict[str, Any]) -> str | None:
    return preserved.get("carried", {}).get("scope")


def measure_recurrence(
    ledger: EventLedger, *, workspace_id: str
) -> list[RecurrenceFinding]:
    """Count, over recorded occurrences, the exchanges each distinction recurs in.

    Workspace-wide by construction. A comparison is recorded under one
    exchange's session while consuming a finding from another, so filtering the
    consumed occurrences to a single session would make the other exchange look
    as though it never measured the coordinate. `#2429` exposed that mode and it
    is not offered here.
    """

    comparisons = recorded_comparison_occurrences(ledger, workspace_id=workspace_id)
    measurements = recorded_measurement_occurrences(ledger, workspace_id=workspace_id)
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
    bounded_exchanges: set[str] = set()
    for event in measurements:
        declared = _declared_of_measurement(event)
        if declared is None:
            continue
        exchange = event.payload.get("dimensions", {}).get("scope_locality")
        if exchange is None:
            continue
        bounded_exchanges.add(exchange)
        measured_coordinate.setdefault(declared, set()).add(exchange)
        coordinate_evidence.setdefault(declared, set()).add(event.id)

    recurs: dict[MeasuredDistinction, set[str]] = {}
    support: dict[MeasuredDistinction, set[str]] = {}
    for event in comparisons:
        declared = _declared_of_comparison(event)
        if declared is None:
            continue
        inputs = event.payload.get("inputs", [])
        exchanges = [_exchange_of(i) for i in inputs]
        if any(x is None for x in exchanges):
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
    for key in sorted(
        recurs, key=lambda k: (-len(recurs[k]), k.left, k.right_representation)
    ):
        where = recurs[key]
        measured = measured_coordinate.get(key.declared, set())
        findings.append(
            RecurrenceFinding(
                distinction=key,
                measured_in=tuple(sorted(where)),
                measured_without_distinction=tuple(sorted(measured - where)),
                coordinate_not_measured=tuple(sorted(bounded_exchanges - measured)),
                consumed_event_ids=tuple(sorted(support[key])),
                bounded_exchanges=tuple(sorted(bounded_exchanges)),
            )
        )
    return findings


def render_recurrence(finding: RecurrenceFinding) -> str:
    """The literal sentence, and nothing stronger."""

    declared = dict(finding.distinction.declared)
    return (
        f"({declared['measured_left_representation']!r}, "
        f"{finding.distinction.right_representation!r}) recurs in "
        f"{finding.recurrence_count} bounded exchanges at "
        f"{declared['measured_position']} under "
        f"{declared['equivalence_rule']} within {declared['counting_scope']}"
    )


def record_recurrence_finding(
    ledger: EventLedger,
    *,
    workspace_id: str,
    session_id: str,
    finding: RecurrenceFinding,
) -> Event:
    """Preserve one recurrence finding so a later responsible act may consume it."""

    declared = dict(finding.distinction.declared)
    payload = {
        "dimensions": {
            "identity": (
                f"recurrence:{declared['measured_left_representation']}"
                f"|{finding.distinction.right_representation}"
            ),
            "content": render_recurrence(finding),
            "standing": "measured",
            "source_provenance": (
                "recorded comparison occurrences and recorded measurement "
                "occurrences"
            ),
            "responsibility": "declared-measurement",
            "authority_warrant": (
                "measurement evidence only; establishes no relation between the "
                "exchanges, no source independence, and no corroboration"
            ),
            "scope_locality": f"workspace:{workspace_id};session:{session_id}",
            "occurrence_preservation": "recurrence finding durably recorded",
        },
        "measurement_subject": (
            "recorded comparison occurrences and recorded measurement occurrences"
        ),
        "counting_scope": (
            "the bounded exchanges represented among the recorded occurrences "
            "this measurement consumed; an exchange with no relevant recorded "
            "measurement does not appear here at all"
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
        RECURRENCE_RECORDED_KIND, workspace_id, payload, session_id=session_id
    )
