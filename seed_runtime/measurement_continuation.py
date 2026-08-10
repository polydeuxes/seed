"""Form the next measurements from recorded findings, until none is new.

`#2392` removed the last supplied representation: the material offers the
representations, and a recorded finding supplies the pair a later measurement
is performed relative to. One selection remained, and it was ours — after each
round a reader looked at the findings and said *measure on that one next*.

This module removes that. It reads a recorded finding, forms **every**
measurement the fixed forms permit from it, skips the ones already performed
under the same scope and rule, records the rest, and repeats.

**There is no judgement anywhere in the loop.** No count, share, threshold, or
notion of interest decides which finding is continued. Every occupancy of every
finding is carried forward, including those measured once. What a reader would
call a dead end is measured exactly as carefully as anything else, and its
findings are recorded.

**The stopping condition is not constitutional Stopping.** A pass that forms no
measurement the ledger does not already hold ends the run. That is a harness
declining to ask a finite question twice; it establishes no Stop, and
`08.Stopping` is untouched. A pass budget exists for the same reason and is
recorded as a limit rather than a finding.

The forms are fixed and few:

```text
one representation  r        after            what occupies the position after r
two representations a, b     preceding        what occupies the position before
                             following        the position after
                             before_same_right what else occupies the left
                                              position before b
                             after_same_left  what else occupies the right
                                              position after a
```

A finding measured relative to one representation offers each occupancy as a
second, giving pairs. A finding measured relative to two offers each occupancy
as a single representation, giving new anchors. That is the whole recursion,
and it is mechanical.

Nothing here establishes meaning, relation, kind, or truth. Each recorded
finding carries the finding it was formed from as its premise, so a chain of
any depth remains a chain of counts whose support basis is recoverable.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence

from seed_runtime.adjacent_pair_measurement import (
    AdjacentPair,
    measure_adjacent_pair,
    measure_after,
)
from seed_runtime.events import EventLedger
from seed_runtime.event import Event
from seed_runtime.preserved_material_measurement import (
    MEASUREMENT_RECORDED_KIND,
    PreservedMaterialMeasurementError,
    record_measurement_finding,
)

SINGLE_FORMS: tuple[str, ...] = ("after",)
PAIR_FORMS: tuple[str, ...] = (
    "preceding",
    "following",
    "before_same_right",
    "after_same_left",
)


@dataclass(frozen=True)
class PendingMeasurement:
    """One measurement the forms permit but the ledger does not yet hold."""

    form: str
    relative_to: tuple[str, ...]
    premise_event_id: str

    def key(self, counting_scope: str) -> tuple[str, tuple[str, ...], str]:
        """What makes two measurements the same question.

        The form, what it is performed relative to, and the scope it is counted
        within. Two measurements agreeing on all three would return the same
        count, so performing the second adds nothing.
        """

        return (self.form, self.relative_to, counting_scope)


def performed_measurements(
    ledger: EventLedger, *, workspace_id: str, session_id: str
) -> set[tuple[str, tuple[str, ...], str]]:
    """Every question the ledger already answers, as its identifying key."""

    performed = set()
    for event in ledger.list(workspace_id):
        if event.session_id != session_id or event.kind != MEASUREMENT_RECORDED_KIND:
            continue
        form = event.payload.get("measurement_form")
        if form is None:
            continue
        performed.add(
            (
                form,
                tuple(event.payload.get("measured_relative_to", ())),
                event.payload["counting_scope"],
            )
        )
    return performed


def measurements_from_finding(event: Event) -> list[PendingMeasurement]:
    """Every measurement the fixed forms permit from one recorded finding.

    No occupancy is skipped. An occupancy measured once yields exactly the same
    measurements as one measured a thousand times, because nothing here is
    entitled to treat a count as a reason.
    """

    if event.kind != MEASUREMENT_RECORDED_KIND:
        raise PreservedMaterialMeasurementError(
            "measurements are formed from recorded findings only"
        )
    anchor = tuple(event.payload.get("measured_relative_to", ()))
    if not anchor:
        raise PreservedMaterialMeasurementError(
            "the recorded finding does not state what it measured relative to"
        )
    occupants = [o["representation"] for o in event.payload["occupancies"]]
    pending: list[PendingMeasurement] = []
    if len(anchor) == 1:
        for occupant in occupants:
            for form in PAIR_FORMS:
                pending.append(
                    PendingMeasurement(form, (anchor[0], occupant), event.id)
                )
    elif len(anchor) == 2:
        for occupant in occupants:
            for form in SINGLE_FORMS:
                pending.append(PendingMeasurement(form, (occupant,), event.id))
    return pending


def perform(
    occurrences: Sequence[Event],
    pending: PendingMeasurement,
    *,
    counting_scope: str,
):
    """Run one pending measurement using the existing forms unchanged."""

    if pending.form in SINGLE_FORMS:
        return measure_after(
            occurrences,
            pending.relative_to[0],
            counting_scope=counting_scope,
            premise_event_id=pending.premise_event_id,
        )
    pair = AdjacentPair(left=pending.relative_to[0], right=pending.relative_to[1])
    return measure_adjacent_pair(
        occurrences,
        pair,
        counting_scope=counting_scope,
        premise_event_id=pending.premise_event_id,
    )[pending.form]


def continue_measurements(
    ledger: EventLedger,
    occurrences: Iterable[Event],
    *,
    workspace_id: str,
    session_id: str,
    counting_scope: str,
    passes: int,
) -> list[list[Event]]:
    """Continue until a pass forms nothing new, or the pass budget is spent.

    Returns the events recorded by each pass. An empty final entry means the
    forms were exhausted rather than the budget; a full one means the budget
    ran out first, and the difference is worth reading before drawing anything
    from a run.
    """

    material = list(occurrences)
    rounds: list[list[Event]] = []
    for _ in range(passes):
        performed = performed_measurements(
            ledger, workspace_id=workspace_id, session_id=session_id
        )
        pending: list[PendingMeasurement] = []
        seen: set[tuple[str, tuple[str, ...], str]] = set()
        for event in ledger.list(workspace_id):
            if event.session_id != session_id or event.kind != MEASUREMENT_RECORDED_KIND:
                continue
            if not event.payload.get("measured_relative_to"):
                continue
            for candidate in measurements_from_finding(event):
                key = candidate.key(counting_scope)
                if key in performed or key in seen:
                    continue
                seen.add(key)
                pending.append(candidate)
        if not pending:
            rounds.append([])
            break
        recorded: list[Event] = []
        for candidate in pending:
            finding = perform(material, candidate, counting_scope=counting_scope)
            recorded.append(
                record_measurement_finding(
                    ledger,
                    workspace_id=workspace_id,
                    session_id=session_id,
                    finding=finding,
                )
            )
        rounds.append(recorded)
    return rounds
