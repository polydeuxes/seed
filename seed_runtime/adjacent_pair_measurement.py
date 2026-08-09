"""Measure a recovered adjacent pair by the same battery of bounded questions.

An **adjacent pair** is two representations, one recorded as occupying the
position after the other. Nothing more. An earlier draft of this module called
it a *joint*, a word borrowed from conversation about what such pairs might
turn out to be; that word is not used here, because a working name adopted in
discussion is not a recovered distinction and this module should not lend it
one.

`#2391` recovered thirteen such pairs from preserved material without a reader
naming any representation, occupant, or delimiter.

This module takes such a pair and asks the same generic questions of it that
it would ask of any other:

```text
preceding           what occupies the position before the pair
following           what occupies the position after it
before_same_right   what else occupies the left position, before the
                    pair's right representation
after_same_left     what else occupies the right position, after the
                    pair's left representation
```

**The battery is fixed and applied symmetrically.** No question is asked of one
pair and withheld from another, and none of the four is motivated by what a
reader believes the representations are. They are adjacency and occupancy
measurements, which `01.External:28` permits a declared measurement to produce.

**The pairs are not supplied.** :func:`adjacent_pairs_from_finding` reads them out of a
recorded measurement finding, so what this round measures relative to comes
from the previous round's evidence rather than from the caller. Every measurement
records that finding as its premise, so what it stood on travels with it.

**Comparing measurements is not performed here.** Two pairs sharing an
alternative is a fact about two preserved findings. `05.Testimony:27` reserves
consuming preserved findings to a bounded comparison, and none is performed.

Nothing here establishes meaning, grammatical kind, relation, or truth. A pair
is an ordered pair that recurs. That two pairs return the same occupant is a
measured agreement between counts, and `01.Standing.D` refuses relation standing to
co-presence.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable, Sequence

from seed_runtime.events import EventLedger
from seed_runtime.models import Event
from seed_runtime.preserved_material_measurement import (
    MEASUREMENT_RECORDED_KIND,
    DeclaredMeasurement,
    MeasurementFinding,
    PreservedMaterialMeasurementError,
    measure_occupancy,
    record_measurement_finding,
)

EQUIVALENCE_RULE = "byte-for-byte equality; no normalization"

# Where each form measures, stated as coordinates rather than left in the
# indexing.  A measurement that does not say where it looked cannot be compared
# with one that looked elsewhere, and a coordinate that is never written down
# cannot be observed to have never varied.
#
#   anchored_on   which preserved representation the position is taken from
#   direction     which side of it
#   displacement  how many positions away
#
# These describe the forms as they are. Nothing here proposes another
# displacement, and none of the five uses one.
MEASURED_POSITIONS: dict[str, dict[str, object]] = {
    "after": {"anchored_on": "the representation", "direction": "after", "displacement": 1},
    "preceding": {"anchored_on": "left", "direction": "before", "displacement": 1},
    "following": {"anchored_on": "right", "direction": "after", "displacement": 1},
    "before_same_right": {"anchored_on": "right", "direction": "before", "displacement": 1},
    "after_same_left": {"anchored_on": "left", "direction": "after", "displacement": 1},
}


@dataclass(frozen=True)
class AdjacentPair:
    """An ordered pair of representations whose adjacency was found reproducible.

    The name describes the measured arrangement and nothing else. It is not a
    constitutional kind, and it asserts nothing about either representation or
    about any relation between them.
    """

    left: str
    right: str

    def __post_init__(self) -> None:
        if not isinstance(self.left, str) or not isinstance(self.right, str):
            raise PreservedMaterialMeasurementError("a pair is a pair of representations")
        if not self.left or not self.right:
            raise PreservedMaterialMeasurementError("a pair's representations must be exact")

    def __str__(self) -> str:  # pragma: no cover - rendering only
        return f"{self.left!r} -> {self.right!r}"


def adjacent_pairs_from_finding(ledger: EventLedger, finding_event_id: str) -> list[AdjacentPair]:
    """Read pairs out of a recorded finding rather than taking them from a caller.

    The recorded finding names a left representation and the occupancies
    measured after it. Every occupancy is returned; none is filtered by count,
    share, or a threshold. Which of them prove reproducible is what the
    measurement measures, not something decided here.
    """

    event = ledger.get(finding_event_id)
    if event is None or event.kind != MEASUREMENT_RECORDED_KIND:
        raise PreservedMaterialMeasurementError(
            "pairs must be read from a recorded measurement finding"
        )
    left = event.payload.get("measured_left_representation")
    if not isinstance(left, str) or not left:
        raise PreservedMaterialMeasurementError(
            "the recorded finding does not name the representation it measured after"
        )
    return [
        AdjacentPair(left=left, right=occupancy["representation"])
        for occupancy in event.payload["occupancies"]
    ]


def _positions(text: str) -> Sequence[str]:
    """Whitespace-delimited positions.

    A reader-supplied resolution, recorded as such. `#2391` established that
    the discrimination survives character n-grams too, so this rule is not
    load-bearing; it is legible.
    """

    return text.split()


def _position_measurements(pair: AdjacentPair) -> dict[str, Callable[[str], str | None]]:
    """The four questions, each returning one occupant or nothing.

    Absence of the pair in an occurrence yields ``None``: the position is not
    there, which is absence rather than Unknown.
    """

    def find(parts: Sequence[str]) -> int | None:
        for index in range(len(parts) - 1):
            if parts[index] == pair.left and parts[index + 1] == pair.right:
                return index
        return None

    def preceding(text: str) -> str | None:
        parts = _positions(text)
        at = find(parts)
        return parts[at - 1] if at is not None and at > 0 else None

    def following(text: str) -> str | None:
        parts = _positions(text)
        at = find(parts)
        return parts[at + 2] if at is not None and at + 2 < len(parts) else None

    def before_same_right(text: str) -> str | None:
        parts = _positions(text)
        for index in range(len(parts) - 1):
            if parts[index + 1] == pair.right and parts[index] != pair.left:
                return parts[index]
        return None

    def after_same_left(text: str) -> str | None:
        parts = _positions(text)
        for index in range(len(parts) - 1):
            if parts[index] == pair.left and parts[index + 1] != pair.right:
                return parts[index + 1]
        return None

    return {
        "preceding": preceding,
        "following": following,
        "before_same_right": before_same_right,
        "after_same_left": after_same_left,
    }


def measure_adjacent_pair(
    occurrences: Iterable[Event],
    pair: AdjacentPair,
    *,
    counting_scope: str,
    premise_event_id: str,
) -> dict[str, MeasurementFinding]:
    """Apply the whole battery to one pair. Every question, no exceptions."""

    material = list(occurrences)
    findings: dict[str, MeasurementFinding] = {}
    for name, occupant_of in _position_measurements(pair).items():
        findings[name] = measure_occupancy(
            material,
            declared=DeclaredMeasurement(
                representation_measured=(
                    f"the {name.replace('_', ' ')} position of the ordered pair "
                    f"{pair.left!r} {pair.right!r}"
                ),
                equivalence_rule=EQUIVALENCE_RULE,
                counting_scope=counting_scope,
                premise_event_id=premise_event_id,
                form=name,
                relative_to=(pair.left, pair.right),
                measured_position=MEASURED_POSITIONS[name],
            ),
            occupant_of=occupant_of,
        )
    return findings


def record_pair_measurements(
    ledger: EventLedger,
    *,
    workspace_id: str,
    session_id: str,
    pair: AdjacentPair,
    findings: dict[str, MeasurementFinding],
) -> dict[str, Event]:
    """Preserve every measurement, including the ones that found nothing.

    A question whose answer was absent is recorded as having been asked. A
    battery that quietly dropped its empty results would report only the
    questions that happened to succeed.
    """

    recorded: dict[str, Event] = {}
    for name, finding in findings.items():
        recorded[name] = record_measurement_finding(
            ledger,
            workspace_id=workspace_id,
            session_id=session_id,
            finding=finding,
            extra={
                "measurement": name,
                "pair_left": pair.left,
                "pair_right": pair.right,
            },
        )
    return recorded


def occupant_agreement_across_scopes(
    scopes: Sequence[Sequence[Event]],
    pair: AdjacentPair,
    measurement: str,
    *,
    counting_scope: str,
    premise_event_id: str,
) -> tuple[str | None, int, int]:
    """How many independently bounded scopes returned the same occupant.

    Returns the agreed occupant, the number of scopes agreeing, and the number
    that produced any answer. Agreement is the discriminator `#2390` found
    survives; no share threshold is applied and none is proposed.
    """

    answers: list[str] = []
    for scope in scopes:
        finding = measure_adjacent_pair(
            scope, pair, counting_scope=counting_scope, premise_event_id=premise_event_id
        )[measurement]
        highest = finding.highest_count_occupancy
        if highest is not None:
            answers.append(highest.representation)
    if not answers:
        return None, 0, 0
    counts: dict[str, int] = {}
    for answer in answers:
        counts[answer] = counts.get(answer, 0) + 1
    agreed = max(counts.items(), key=lambda kv: (kv[1], kv[0]))
    return agreed[0], agreed[1], len(answers)


def group_by_highest_count_occupant(
    measurements: dict[str, dict[str, MeasurementFinding]],
    measurement: str,
) -> dict[str, list[str]]:
    """Which pairs returned the same occupant for the same question.

    This reports agreement between preserved counts. It performs no comparison
    in the sense `05.Testimony:27` governs, establishes no relation between the
    pairs, and does not make them a kind.
    """

    grouped: dict[str, list[str]] = {}
    for label, findings in measurements.items():
        highest = findings[measurement].highest_count_occupancy
        if highest is None:
            continue
        grouped.setdefault(highest.representation, []).append(label)
    return grouped


def enumerate_representations(
    occurrences: Iterable[Event], *, present_in: Sequence[Sequence[Event]] = ()
) -> list[str]:
    """Every representation the material offers.

    No representation is named here and none is preferred. When ``present_in``
    is supplied, only representations measurable in *every* one of those scopes
    are returned -- a comparability requirement, so that a later measurement can
    ask the same question of each scope, not a judgement that the others are
    uninteresting.

    This is what removes the last supplied representation from the chain. The
    caller no longer says which representation to measure after; the material
    says which representations there are, and later measurements say which of
    them anything reproducible follows from.
    """

    material = list(occurrences)
    everywhere: set[str] | None = None
    for scope in present_in:
        seen = {
            token
            for event in scope
            for token in _positions(event.payload["decoded_text"])
        }
        everywhere = seen if everywhere is None else (everywhere & seen)
    offered = {
        token
        for event in material
        for token in _positions(event.payload["decoded_text"])
    }
    if everywhere is not None:
        offered &= everywhere
    return sorted(offered)


def enumerate_displacements(
    occurrences: Iterable[Event], representation: str, *, direction: str = "after"
) -> list[int]:
    """Every positional displacement at which this material has a position.

    Nothing is preferred and nothing is chosen. An occurrence carrying the
    representation at index *i* has a position at displacement *d* whenever the
    occurrence extends that far, so the displacements returned are a fact about
    how far the material reaches from where the representation sits.

    A displacement absent here is absent because no occurrence reaches it, not
    because it was judged uninteresting. `#2397` recorded that a coordinate
    observed with one value is not thereby an instruction to vary it; this does
    not vary it either, it reports what the material makes measurable.
    """

    if direction not in ("after", "before"):
        raise PreservedMaterialMeasurementError(
            "a displacement is measured before or after, and nothing else"
        )
    reachable: set[int] = set()
    for event in occurrences:
        parts = _positions(event.payload["decoded_text"])
        for index, part in enumerate(parts):
            if part != representation:
                continue
            span = len(parts) - 1 - index if direction == "after" else index
            reachable.update(range(1, span + 1))
    return sorted(reachable)


def measure_at_displacement(
    occurrences: Iterable[Event],
    representation: str,
    *,
    displacement: int,
    direction: str = "after",
    counting_scope: str,
    premise_event_id: str | None = None,
) -> MeasurementFinding:
    """Count what occupies one stated displacement from one representation.

    The displacement is a parameter of the measurement rather than a constant
    of the code, and it is recorded on the finding, so a later survey observes
    the value actually used instead of a value the indexing hid.
    """

    if displacement < 1:
        raise PreservedMaterialMeasurementError(
            "a displacement is at least one position away"
        )
    step = displacement if direction == "after" else -displacement

    def occupant_of(text: str) -> str | None:
        parts = _positions(text)
        for index, part in enumerate(parts):
            if part != representation:
                continue
            at = index + step
            if 0 <= at < len(parts):
                return parts[at]
        return None

    return measure_occupancy(
        occurrences,
        declared=DeclaredMeasurement(
            representation_measured=(
                f"the representation {displacement} position(s) {direction} "
                f"{representation!r}"
            ),
            equivalence_rule=EQUIVALENCE_RULE,
            counting_scope=counting_scope,
            premise_event_id=premise_event_id,
            measured_after=representation,
            form=direction,
            relative_to=(representation,),
            measured_position={
                "anchored_on": "the representation",
                "direction": direction,
                "displacement": displacement,
            },
        ),
        occupant_of=occupant_of,
    )


def measure_after(
    occurrences: Iterable[Event],
    representation: str,
    *,
    counting_scope: str,
    premise_event_id: str | None = None,
) -> MeasurementFinding:
    """Count what occupies the position immediately after a representation.

    One displacement of the family :func:`measure_at_displacement` covers, kept
    because the continuation and its tests name it. It carries no privilege;
    `#2403` records that no displacement is preferred.
    """

    return measure_at_displacement(
        occurrences,
        representation,
        displacement=1,
        direction="after",
        counting_scope=counting_scope,
        premise_event_id=premise_event_id,
    )
