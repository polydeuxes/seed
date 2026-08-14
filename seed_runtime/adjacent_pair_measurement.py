"""Measure a validated adjacent pair by the same battery of bounded questions.

An **adjacent pair** is two representations, one recorded as occupying the
position after the other. Nothing more.

`#2391` validated thirteen such pairs from preserved material without a reader
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
measurements, which `01.Source:28` permits a declared measurement to yield.

**The pairs are not supplied.** :func:`adjacent_pairs_from_finding` reads them out of a
recorded measurement finding, so what this round measures relative to comes
from the previous round's evidence rather than from the caller. Every measurement
records that finding as its premise, so what it stood on travels with it.

**Comparing measurements is not performed here.** Two pairs sharing an
alternative is an Assertion about two preserved findings. `01.Standing.E` reserves
using preserved findings to a bounded comparison, and none is performed.

Nothing here establishes represented relation, grammatical kind, relation, or truth. A pair
is an ordered pair that recurs. That two pairs return the same occupant is a
measured agreement between counts, and `01.Standing.D` refuses relation standing to
co-presence.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from typing import Callable, Iterable, Iterator, Sequence

from seed_runtime.events import CORRUPTED, EventLedger, EventLedgerBoundary
from seed_runtime.event import Event
from seed_runtime.ids import new_id
from seed_runtime.yield_evidence import _record_yield_evidence, yield_commitment
from seed_runtime.support_basis import (
    SupportBasis,
    SupportBasisError,
    SupportValidator,
    declare_complete_inputs,
)
from seed_runtime.preserved_material_measurement import (
    INGRESS_OCCURRED_KIND,
    MEASUREMENT_RECORDED_KIND,
    DeclaredMeasurement,
    MeasurementFinding,
    MEASUREMENT_CONVENTION,
    Occupancy,
    PreservedMaterialMeasurementError,
    measure_occupancy,
    record_measurement_finding,
    record_measurement_findings,
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

PAIR_MEASUREMENT_FORMS: tuple[str, ...] = (
    "preceding",
    "following",
    "before_same_right",
    "after_same_left",
)

POSITIONAL_RESULT_STANDING_COORDINATE_RESPONSIBILITY = (
    "preserve this measured Assertion's carried Standing coordinates"
)
ADJACENT_PAIR_OBSERVATION_RECORDED_KIND = (
    "operator.measurement.adjacent_pair_observation_recorded"
)
ADJACENT_PAIR_OBSERVATION_ACT_EVIDENCE_KIND = (
    "operator.measurement.adjacent_pair_observation_act_evidenced"
)
ADJACENT_PAIR_OBSERVATION_CARRIAGE_EVIDENCE_KIND = (
    "operator.measurement.adjacent_pair_observation_carriage_evidenced"
)
ADJACENT_PAIR_OBSERVATION_CONVENTION = "adjacent_pair_observation_v1"
ADJACENT_PAIR_OBSERVATION_RESPONSIBILITY = (
    "observe one adjacent position on each side of every exact occurrence of "
    "each ordered pair recovered from one exact finding"
)


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


@dataclass(frozen=True)
class PositionedRepresentationOccurrence:
    """One exact representation position inside one preserved occurrence."""

    source_occurrence_id: str
    position: int
    representation: str

    @property
    def identity(self) -> tuple[str, int]:
        return (self.source_occurrence_id, self.position)


@dataclass(frozen=True)
class ExactAdjacentPairOccurrence:
    """One exact occurrence of an already-recovered ordered adjacent pair."""

    pair: AdjacentPair
    left: PositionedRepresentationOccurrence
    right: PositionedRepresentationOccurrence

    def __post_init__(self) -> None:
        if self.left.source_occurrence_id != self.right.source_occurrence_id:
            raise PreservedMaterialMeasurementError(
                "an adjacent pair occurrence cannot cross source occurrences"
            )
        if self.right.position != self.left.position + 1:
            raise PreservedMaterialMeasurementError(
                "an adjacent pair occurrence requires exact displacement-one order"
            )
        if (
            self.left.representation != self.pair.left
            or self.right.representation != self.pair.right
        ):
            raise PreservedMaterialMeasurementError(
                "an adjacent pair occurrence must carry its exact ordered pair"
            )

    @property
    def identity(self) -> tuple[str, int, int]:
        return (
            self.left.source_occurrence_id,
            self.left.position,
            self.right.position,
        )


@dataclass(frozen=True)
class AdjacentPairObservation:
    """One bounded position on each side of one exact pair occurrence.

    The representations are carried observations. They are not classified as
    relation words, and equal representations do not identify equal relations.
    """

    left_occurrence: PositionedRepresentationOccurrence | None
    pair_occurrence: ExactAdjacentPairOccurrence
    right_occurrence: PositionedRepresentationOccurrence | None
    source_occurrence_id: str
    exact_order: tuple[int, ...]
    evidence: dict[str, object]

    def __post_init__(self) -> None:
        source_id = self.source_occurrence_id
        if not isinstance(source_id, str) or not source_id:
            raise PreservedMaterialMeasurementError(
                "an adjacent-pair observation requires one exact source occurrence"
            )
        if self.pair_occurrence.left.source_occurrence_id != source_id:
            raise PreservedMaterialMeasurementError(
                "the pair occurrence is outside the observed source occurrence"
            )
        expected_order = []
        if self.left_occurrence is not None:
            if (
                self.left_occurrence.source_occurrence_id != source_id
                or self.left_occurrence.position
                != self.pair_occurrence.left.position - 1
            ):
                raise PreservedMaterialMeasurementError(
                    "the left occurrence is not exactly adjacent to the pair"
                )
            expected_order.append(self.left_occurrence.position)
        expected_order.extend(
            (
                self.pair_occurrence.left.position,
                self.pair_occurrence.right.position,
            )
        )
        if self.right_occurrence is not None:
            if (
                self.right_occurrence.source_occurrence_id != source_id
                or self.right_occurrence.position
                != self.pair_occurrence.right.position + 1
            ):
                raise PreservedMaterialMeasurementError(
                    "the right occurrence is not exactly adjacent to the pair"
                )
            expected_order.append(self.right_occurrence.position)
        if self.exact_order != tuple(expected_order):
            raise PreservedMaterialMeasurementError(
                "the carried order does not match the exact observed positions"
            )
        evidence = self.evidence
        finding_id = evidence.get("pair_finding_event_id")
        evidence_ids = evidence.get("evidence_occurrence_ids")
        text = evidence.get("exact_decoded_text")
        if (
            evidence.get("source_occurrence_id") != source_id
            or not isinstance(finding_id, str)
            or not finding_id
            or evidence_ids != [finding_id, source_id]
            or evidence.get("source_kind") != INGRESS_OCCURRED_KIND
            or not isinstance(evidence.get("workspace_id"), str)
            or not isinstance(evidence.get("session_id"), str)
            or not isinstance(text, str)
        ):
            raise PreservedMaterialMeasurementError(
                "the adjacent-pair observation does not preserve its exact Evidence"
            )
        positions = _positions(text)
        carried = (
            *((self.left_occurrence,) if self.left_occurrence is not None else ()),
            self.pair_occurrence.left,
            self.pair_occurrence.right,
            *((self.right_occurrence,) if self.right_occurrence is not None else ()),
        )
        if any(
            occurrence.position >= len(positions)
            or positions[occurrence.position] != occurrence.representation
            for occurrence in carried
        ):
            raise PreservedMaterialMeasurementError(
                "the observed occurrences do not match the carried source Evidence"
            )

    @property
    def identity(self) -> tuple[str, str, int, int]:
        return (
            self.evidence["pair_finding_event_id"],
            self.source_occurrence_id,
            self.pair_occurrence.left.position,
            self.pair_occurrence.right.position,
        )

    @property
    def fully_bounded_coordinates(self) -> dict[str, object] | None:
        """Return the neutral coordinates only when both outer positions exist."""

        if self.left_occurrence is None or self.right_occurrence is None:
            return None
        return {
            "identity": {
                "pair_finding_event_id": self.evidence["pair_finding_event_id"],
                "source_occurrence_id": self.source_occurrence_id,
                "positions": list(self.exact_order),
            },
            "left_occurrence": {
                "occurrence": list(self.left_occurrence.identity),
                "representation": self.left_occurrence.representation,
            },
            "pair_occurrence": {
                "occurrence": list(self.pair_occurrence.identity),
                "ordered_pair": [
                    self.pair_occurrence.pair.left,
                    self.pair_occurrence.pair.right,
                ],
            },
            "right_occurrence": {
                "occurrence": list(self.right_occurrence.identity),
                "representation": self.right_occurrence.representation,
            },
            "evidence": dict(self.evidence),
        }


@dataclass(frozen=True)
class RecordedAdjacentPairResultAssertion:
    """One exact positional result, addressable at its yielding occurrence."""

    assertion_id: str
    yielding_event_id: str
    yielding_session_id: str | None
    payload: dict[str, object]
    completeness_boundary: EventLedgerBoundary

    @property
    def reference(self) -> dict[str, str]:
        return {
            "yielding_event_id": self.yielding_event_id,
            "assertion_id": self.assertion_id,
        }


def _canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def _adjacent_pair_result_assertion_identity(
    *, subject: dict[str, object], scope: dict[str, object], content: dict[str, object]
) -> str:
    represented = {
        "result": "position_occupancy",
        "subject": subject,
        "scope": scope,
        "content": content,
    }
    return "position-occupancy-assertion:" + hashlib.sha256(
        _canonical_json(represented).encode("utf-8")
    ).hexdigest()


class _DeclaredSupportBinding:
    """A support basis and the exact input sequence it was formed over.

    **The binding is carried by the representation event, not by adjacency.** An earlier
    revision was a dataclass holding an identities tuple and a `SupportBasis`
    side by side, with prose saying the second was bound to the first and
    nothing enforcing it — so a basis carrying a forged commitment and count
    could be placed beside an honest inputs and would be carried onto every
    Assertion the layer recorded. Putting two things in one dataclass does not
    establish a relation between them.

    There is no way to supply a basis here. This forms it, once, from the
    identities it is given, and retains both.
    """

    __slots__ = ("_identities", "_basis")

    def __init__(
        self,
        *,
        workspace_id: str,
        session_id: str,
        occurrence_kind: str,
        boundary: EventLedgerBoundary,
        identities: tuple[str, ...],
    ) -> None:
        self._identities = identities
        self._basis = declare_complete_inputs(
            workspace_id=workspace_id,
            session_id=session_id,
            occurrence_kind=occurrence_kind,
            boundary=boundary,
            identities=identities,
        )

    @property
    def identities(self) -> tuple[str, ...]:
        return self._identities

    @property
    def basis(self) -> SupportBasis:
        return self._basis


def _support_for(
    *,
    workspace_id: str,
    session_id: str,
    completeness_boundary: EventLedgerBoundary,
    finding: MeasurementFinding,
    declared_support: "_DeclaredSupportBinding | None",
) -> SupportBasis:
    """The basis for this finding, declared once per inputs where supplied.

    A supplied basis is required to describe this finding's own scope, boundary
    and extent. It is not re-derived from the identities, because re-deriving is
    the cost being removed — but a basis that does not match is refused rather
    than carried onto an Assertion it does not describe.
    """

    if declared_support is None:
        return declare_complete_inputs(
            workspace_id=workspace_id,
            session_id=session_id,
            occurrence_kind=INGRESS_OCCURRED_KIND,
            boundary=completeness_boundary,
            identities=finding.input_event_ids,
        )
    if finding.input_event_ids is not declared_support.identities:
        raise PreservedMaterialMeasurementError(
            "a declared support binding was not formed over the input sequence "
            "this finding carries"
        )
    basis = declared_support.basis
    if (
        basis.workspace_id != workspace_id
        or basis.session_id != session_id
        or basis.occurrence_kind != INGRESS_OCCURRED_KIND
        or basis.boundary_commitment != completeness_boundary.commitment
    ):
        raise PreservedMaterialMeasurementError(
            "a declared support basis does not describe this finding's scope"
        )
    return basis


def _adjacent_pair_result_assertion_fields(
    *,
    workspace_id: str,
    session_id: str,
    pair: AdjacentPair,
    finding: MeasurementFinding,
    completeness_boundary: EventLedgerBoundary,
    declared_support: "_DeclaredSupportBinding | None" = None,
) -> dict[str, object]:
    """Form one result Assertion's carried coordinates.

    ``declared_support`` is the basis already declared for these inputs,
    bound to the identities it was declared over. A layer measures one bounded
    inputs, so every finding it yields input the same identities under
    the same rule and yields the same basis — and declaring it per finding
    recomputed a digest over the whole inputs once per result, measured at
    28.7s against 23.1s on 21,972 results over 700 occurrences.

    It is required to match, not trusted. The layer holds one identities tuple
    and every finding carries that same object, so the check is an identity
    comparison rather than a second digest.
    """
    form = finding.declared.form
    if form not in PAIR_MEASUREMENT_FORMS:
        raise PreservedMaterialMeasurementError(
            "an adjacent-pair result Assertion requires one established pair form"
        )
    subject: dict[str, object] = {
        "ordered_pair": [pair.left, pair.right],
        "measurement_form": form,
        "measured_position": finding.declared.measured_position,
        "equivalence_rule": finding.declared.equivalence_rule,
    }
    scope: dict[str, object] = {
        "workspace_id": workspace_id,
        "session_id": session_id,
        "counting_scope": finding.declared.counting_scope,
    }
    content: dict[str, object] = {
        "positions_measured": finding.positions_measured,
        "occupancies": [
            {
                "representation": occupancy.representation,
                "occurrence_count": occupancy.occurrence_count,
            }
            for occupancy in finding.occupancies
        ],
    }
    identity = _adjacent_pair_result_assertion_identity(
        subject=subject, scope=scope, content=content
    )
    return {
        "dimensions": {
            "identity": identity,
            "content": content,
            "standing": "measured",
            "source_provenance": "preserved operator-ingress occurrences",
            "responsibility": POSITIONAL_RESULT_STANDING_COORDINATE_RESPONSIBILITY,
            "authority": (
                "measurement evidence only; establishes no represented relation, relation, "
                "kind, or standing beyond this measured Assertion"
            ),
            "scope_locality": "the exact assertion_scope carried here",
            "occurrence_preservation": (
                "one exact result preserved by its yielding occurrence"
            ),
        },
        "subject_kind": "assertion",
        "responsible_boundary": "this recorded assertion",
        "result": "position_occupancy",
        "assertion_subject": subject,
        "assertion_scope": scope,
        "support_basis": {
            "basis": _support_for(
                workspace_id=workspace_id,
                session_id=session_id,
                completeness_boundary=completeness_boundary,
                finding=finding,
                declared_support=declared_support,
            ).to_json_dict(),
            "premise_event_id": finding.declared.premise_event_id,
        },
        "completeness_boundary": {
            "commitment": completeness_boundary.commitment,
        },
        "completeness_scope": {
            "workspace_id": workspace_id,
            "session_id": session_id,
            "occurrence_kind": INGRESS_OCCURRED_KIND,
        },
        "unknowns": [
            "what any measured representation means remains Unknown",
        ],
        "forbidden_inferences": [
            "literal recurrence is not represented relation or relation",
            "matching result content across different Assertions does not make "
            "them one Assertion",
        ],
    }


def assertion_of_recorded_adjacent_pair_result(
    event: Event,
) -> RecordedAdjacentPairResultAssertion:
    """Reconstruct one canonical result Assertion, or refuse what it carries."""

    if event.kind != MEASUREMENT_RECORDED_KIND:
        raise PreservedMaterialMeasurementError(
            f"{event.id} is not a recorded Measurement result"
        )
    payload = event.payload
    dimensions = payload.get("dimensions")
    subject = payload.get("assertion_subject")
    scope = payload.get("assertion_scope")
    content = dimensions.get("content") if isinstance(dimensions, dict) else None
    boundary = payload.get("completeness_boundary")
    completeness_scope = payload.get("completeness_scope")
    support = payload.get("support_basis")
    identity = dimensions.get("identity") if isinstance(dimensions, dict) else None
    if (
        payload.get("subject_kind") != "assertion"
        or payload.get("result") != "position_occupancy"
        or not isinstance(subject, dict)
        or not isinstance(scope, dict)
        or not isinstance(content, dict)
        or not isinstance(boundary, dict)
        or not isinstance(boundary.get("commitment"), str)
        or not boundary["commitment"]
        or not isinstance(completeness_scope, dict)
        or not isinstance(support, dict)
        or not isinstance(identity, str)
        or not identity
    ):
        raise PreservedMaterialMeasurementError(
            f"{event.id} does not carry one exact positional result Assertion"
        )
    pair = payload.get("measured_relative_to")
    form = payload.get("measurement_form")
    expected_content = {
        "positions_measured": payload.get("positions_measured"),
        "occupancies": payload.get("occupancies"),
    }
    if (
        not isinstance(pair, list)
        or len(pair) != 2
        or not all(isinstance(value, str) and value for value in pair)
        or form not in PAIR_MEASUREMENT_FORMS
        or payload.get("equivalence_rule") != EQUIVALENCE_RULE
        or payload.get("measured_position") != MEASURED_POSITIONS[form]
        or subject
        != {
            "ordered_pair": pair,
            "measurement_form": form,
            "measured_position": payload.get("measured_position"),
            "equivalence_rule": payload.get("equivalence_rule"),
        }
        or scope
        != {
            "workspace_id": event.workspace_id,
            "session_id": event.session_id,
            "counting_scope": payload.get("counting_scope"),
        }
        or content != expected_content
        or completeness_scope
        != {
            "workspace_id": event.workspace_id,
            "session_id": event.session_id,
            "occurrence_kind": INGRESS_OCCURRED_KIND,
        }
        or support.get("basis") != payload.get("input_support")
        or support.get("premise_event_id") != payload.get("premise_event_id")
    ):
        raise PreservedMaterialMeasurementError(
            f"{event.id} carries incoherent positional result coordinates"
        )
    canonical = _adjacent_pair_result_assertion_identity(
        subject=subject, scope=scope, content=content
    )
    if identity != canonical:
        raise PreservedMaterialMeasurementError(
            f"{event.id} carries an Assertion identity that does not match its result"
        )
    return RecordedAdjacentPairResultAssertion(
        assertion_id=identity,
        yielding_event_id=event.id,
        yielding_session_id=event.session_id,
        payload=payload,
        completeness_boundary=EventLedgerBoundary(boundary["commitment"]),
    )


def get_recorded_adjacent_pair_result_assertion(
    ledger: EventLedger, *, yielding_event_id: str, assertion_id: str
) -> RecordedAdjacentPairResultAssertion | None:
    """Resolve one exact occurrence-bound positional result Assertion."""

    event = ledger.get(yielding_event_id)
    if event is None:
        return None
    if ledger.integrity_of(yielding_event_id) == CORRUPTED:
        raise PreservedMaterialMeasurementError(
            "a corrupted yielding occurrence cannot expose a result Assertion"
        )
    assertion = assertion_of_recorded_adjacent_pair_result(event)
    if assertion.assertion_id != assertion_id:
        return None
    _validate_result_assertion_ingress(ledger, event, assertion)
    return assertion


def _validate_result_assertion_ingress(
    ledger: EventLedger,
    event: Event,
    assertion: RecordedAdjacentPairResultAssertion,
    *,
    validation: SupportValidator | None = None,
) -> None:
    """Reconstruct the carried support basis and require it to reproduce.

    The occurrence no longer carries every supporting identity, so this no
    longer compares two lists. It performs the basis's own declared selection
    against the ledger and refuses unless the result reproduces the committed
    digest.

    The check this replaces also validated the inputs from the ledger, so
    the guarantee is substantially the same one in a compact and reusable form.
    It is not stronger for using a commitment.
    """

    try:
        basis = SupportBasis.from_json_dict(event.payload.get("input_support"))
    except SupportBasisError as exc:
        raise PreservedMaterialMeasurementError(
            f"{event.id} does not carry a reconstructible support basis: {exc}"
        ) from exc
    if (
        basis.workspace_id != event.workspace_id
        or basis.session_id != event.session_id
        or basis.occurrence_kind != INGRESS_OCCURRED_KIND
        or basis.boundary_commitment != assertion.completeness_boundary.commitment
    ):
        raise PreservedMaterialMeasurementError(
            f"{event.id} carries a support basis outside its own scope and boundary"
        )
    if basis.support_count != event.payload.get("input_count"):
        raise PreservedMaterialMeasurementError(
            f"{event.id} carries a support count its basis does not support"
        )
    try:
        (validation or SupportValidator(ledger)).validate(basis)
    except SupportBasisError as exc:
        raise PreservedMaterialMeasurementError(
            f"the carried support basis does not reconstruct: {exc}"
        ) from exc


def iter_recorded_adjacent_pair_result_assertions(
    ledger: EventLedger,
    *,
    workspace_id: str,
    session_ids: Iterable[str],
    through: EventLedgerBoundary,
) -> Iterator[RecordedAdjacentPairResultAssertion]:
    """Stream exact result Assertions through one caller-captured boundary.

    Complete ingress validation is cached only for equal session/boundary pairs.
    The cache contains compact Event identities, not material or result Events.
    """

    validation = SupportValidator(ledger)
    for session_id in tuple(dict.fromkeys(session_ids)):
        for event in ledger.iter_session_kind(
            workspace_id,
            session_id,
            MEASUREMENT_RECORDED_KIND,
            through=through,
        ):
            if event.payload.get("subject_kind") != "assertion":
                continue
            if event.payload.get("result") != "position_occupancy":
                continue
            if ledger.integrity_of(event.id) == CORRUPTED:
                raise PreservedMaterialMeasurementError(
                    "a corrupted yielding occurrence cannot expose a result Assertion"
                )
            assertion = assertion_of_recorded_adjacent_pair_result(event)
            _validate_result_assertion_ingress(
                ledger, event, assertion, validation=validation
            )
            yield assertion


def _adjacent_pairs_from_event(event: Event | None) -> list[AdjacentPair]:
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


def _is_established_after_measurement(event: Event) -> bool:
    """Whether a record carries the exact established displacement-1 form."""

    left = event.payload.get("measured_left_representation")
    return (
        event.kind == MEASUREMENT_RECORDED_KIND
        and event.payload.get("convention") == MEASUREMENT_CONVENTION
        and event.payload.get("equivalence_rule") == EQUIVALENCE_RULE
        and event.payload.get("measurement_form") == "after"
        and isinstance(left, str)
        and bool(left)
        and event.payload.get("measured_relative_to") == [left]
        and event.payload.get("measured_position") == MEASURED_POSITIONS["after"]
    )


def adjacent_pairs_from_finding(ledger: EventLedger, finding_event_id: str) -> list[AdjacentPair]:
    """Read pairs out of a recorded finding rather than taking them from a caller.

    The recorded finding names a left representation and the occupancies
    measured after it. Every occupancy is returned; none is filtered by count,
    share, or a threshold. Which of them prove reproducible is what the
    measurement measures, not something decided here.
    """

    return _adjacent_pairs_from_event(ledger.get(finding_event_id))


def _positions(text: str) -> Sequence[str]:
    """Whitespace-delimited positions.

    A reader-supplied resolution, recorded as such. `#2391` established that
    the discrimination survives character n-grams too, so this rule is not
    load-bearing; it is legible.
    """

    return text.split()


def _observe_adjacent_pair_observations(
    occurrences: Iterable[Event],
    pairs: Iterable[AdjacentPair],
    *,
    pair_finding_event_id: str,
) -> tuple[AdjacentPairObservation, ...]:
    """Extend every exact pair occurrence one position in each direction.

    Pair values select what is observed; they do not classify the resulting
    coordinates. Every observation is identified by its preserved source
    occurrence and exact positions. Boundary absence is retained as absence,
    rather than dropping the pair occurrence or filling a position.
    """

    bounded_pairs = tuple(dict.fromkeys(pairs))
    observations: list[AdjacentPairObservation] = []
    for source in occurrences:
        if source.kind != INGRESS_OCCURRED_KIND:
            raise PreservedMaterialMeasurementError(
                f"only preserved ingress occurrences may be observed: {source.kind}"
            )
        text = source.payload.get("decoded_text")
        if not isinstance(text, str):
            raise PreservedMaterialMeasurementError(
                f"{source.id} carries no exact decoded representation"
            )
        positions = _positions(text)
        for pair in bounded_pairs:
            for at in range(len(positions) - 1):
                if positions[at] != pair.left or positions[at + 1] != pair.right:
                    continue
                pair_left = PositionedRepresentationOccurrence(
                    source.id, at, positions[at]
                )
                pair_right = PositionedRepresentationOccurrence(
                    source.id, at + 1, positions[at + 1]
                )
                left = (
                    PositionedRepresentationOccurrence(
                        source.id, at - 1, positions[at - 1]
                    )
                    if at > 0
                    else None
                )
                right = (
                    PositionedRepresentationOccurrence(
                        source.id, at + 2, positions[at + 2]
                    )
                    if at + 2 < len(positions)
                    else None
                )
                exact_order = tuple(
                    position
                    for position in (
                        left.position if left is not None else None,
                        pair_left.position,
                        pair_right.position,
                        right.position if right is not None else None,
                    )
                    if position is not None
                )
                observations.append(
                    AdjacentPairObservation(
                        left_occurrence=left,
                        pair_occurrence=ExactAdjacentPairOccurrence(
                            pair=pair,
                            left=pair_left,
                            right=pair_right,
                        ),
                        right_occurrence=right,
                        source_occurrence_id=source.id,
                        exact_order=exact_order,
                        evidence={
                            "source_occurrence_id": source.id,
                            "pair_finding_event_id": pair_finding_event_id,
                            "evidence_occurrence_ids": [
                                pair_finding_event_id,
                                source.id,
                            ],
                            "source_kind": source.kind,
                            "workspace_id": source.workspace_id,
                            "session_id": source.session_id,
                            "exact_decoded_text": text,
                        },
                    )
                )
    return tuple(observations)


def observe_adjacent_pair_observations_from_finding(
    ledger: EventLedger,
    *,
    finding_event_id: str,
    occurrences: Iterable[Event],
) -> tuple[AdjacentPairObservation, ...]:
    """Observe only adjacent pairs recovered from one recorded finding."""

    finding = ledger.get(finding_event_id)
    if finding is None or ledger.integrity_of(finding_event_id) == CORRUPTED:
        raise PreservedMaterialMeasurementError(
            "adjacent pairs require one intact recorded finding"
        )
    if not _is_established_after_measurement(finding):
        raise PreservedMaterialMeasurementError(
            "adjacent-pair observations require an exact recorded displacement-one finding"
        )
    material = tuple(occurrences)
    recorded_ids = finding.payload.get("input_event_ids")
    if (
        not isinstance(recorded_ids, list)
        or not all(isinstance(value, str) and value for value in recorded_ids)
        or tuple(event.id for event in material) != tuple(recorded_ids)
    ):
        raise PreservedMaterialMeasurementError(
            "the supplied source occurrences differ from the finding's exact Evidence"
        )
    for event in material:
        recorded = ledger.get(event.id)
        if (
            recorded is None
            or recorded.kind != INGRESS_OCCURRED_KIND
            or recorded.workspace_id != finding.workspace_id
            or recorded.session_id != finding.session_id
            or recorded.workspace_id != event.workspace_id
            or recorded.session_id != event.session_id
            or recorded.payload != event.payload
        ):
            raise PreservedMaterialMeasurementError(
                "the finding's source-occurrence Evidence does not reconstruct"
            )
    pairs = _adjacent_pairs_from_event(finding)
    return _observe_adjacent_pair_observations(
        material,
        pairs,
        pair_finding_event_id=finding_event_id,
    )


def compare_adjacent_pair_observations(
    observations: Iterable[AdjacentPairObservation],
) -> dict[str, object]:
    """Report only distinctions that survive exact occurrence counterexamples.

    Representation equality is counted for comparison but never used as
    occurrence identity. The result reports only measured differences.
    """

    bounded = tuple(observations)
    if not all(isinstance(item, AdjacentPairObservation) for item in bounded):
        raise PreservedMaterialMeasurementError(
            "adjacent-pair observation Compare requires exact bounded observations"
        )
    identities = [observation.identity for observation in bounded]
    if len(set(identities)) != len(identities):
        raise PreservedMaterialMeasurementError(
            "the same exact adjacent-pair observation was supplied more than once"
        )
    complete = tuple(
        coordinates
        for observation in bounded
        if (coordinates := observation.fully_bounded_coordinates) is not None
    )
    representation_groups: dict[
        tuple[str, tuple[str, str], str], list[dict[str, object]]
    ] = {}
    pair_groups: dict[tuple[str, str], list[dict[str, object]]] = {}
    outer_groups: dict[tuple[str, str], list[dict[str, object]]] = {}
    for coordinates in complete:
        left = coordinates["left_occurrence"]["representation"]
        pair = tuple(coordinates["pair_occurrence"]["ordered_pair"])
        right = coordinates["right_occurrence"]["representation"]
        representation_groups.setdefault((left, pair, right), []).append(coordinates)
        pair_groups.setdefault(pair, []).append(coordinates)
        outer_groups.setdefault((left, right), []).append(coordinates)

    return {
        "observation_count": len(bounded),
        "fully_bounded_observation_count": len(complete),
        "boundary_observation_count": len(bounded) - len(complete),
        "distinct_fully_bounded_occurrences": len(
            {
                (
                    coordinates["identity"]["pair_finding_event_id"],
                    coordinates["identity"]["source_occurrence_id"],
                    tuple(coordinates["identity"]["positions"]),
                )
                for coordinates in complete
            }
        ),
        "distinct_representation_triples": len(representation_groups),
        "counterexamples": {
            "representation_triple_groups_with_multiple_occurrences": sum(
                len(group) > 1 for group in representation_groups.values()
            ),
            "ordered_pair_groups_with_multiple_endpoint_representations": sum(
                len(
                    {
                        (
                            coordinates["left_occurrence"]["representation"],
                            coordinates["right_occurrence"]["representation"],
                        )
                        for coordinates in group
                    }
                )
                > 1
                for group in pair_groups.values()
            ),
            "endpoint_groups_with_multiple_ordered_pairs": sum(
                len(
                    {
                        tuple(coordinates["pair_occurrence"]["ordered_pair"])
                        for coordinates in group
                    }
                )
                > 1
                for group in outer_groups.values()
            ),
        },
        "distinct_adjacency_coordinates": [
            {
                "left_present": left_present,
                "right_present": right_present,
                "ordered_displacements": list(displacements),
            }
            for left_present, right_present, displacements in sorted(
                {
                    (
                        observation.left_occurrence is not None,
                        observation.right_occurrence is not None,
                        tuple(
                            later - earlier
                            for earlier, later in zip(
                                observation.exact_order,
                                observation.exact_order[1:],
                            )
                        ),
                    )
                    for observation in bounded
                }
            )
        ],
    }


def _adjacent_pair_observation_payload(
    observation: AdjacentPairObservation,
) -> dict[str, object]:
    def positioned(
        occurrence: PositionedRepresentationOccurrence | None,
    ) -> dict[str, object] | None:
        if occurrence is None:
            return None
        return {
            "source_occurrence_id": occurrence.source_occurrence_id,
            "position": occurrence.position,
            "representation": occurrence.representation,
        }

    return {
        "left_occurrence": positioned(observation.left_occurrence),
        "pair_occurrence": {
            "ordered_pair": [
                observation.pair_occurrence.pair.left,
                observation.pair_occurrence.pair.right,
            ],
            "left": positioned(observation.pair_occurrence.left),
            "right": positioned(observation.pair_occurrence.right),
        },
        "right_occurrence": positioned(observation.right_occurrence),
        "source_occurrence_id": observation.source_occurrence_id,
        "exact_order": list(observation.exact_order),
        "evidence": dict(observation.evidence),
    }


def record_adjacent_pair_observations(
    ledger: EventLedger,
    *,
    workspace_id: str,
    session_id: str,
    finding_event_id: str,
) -> Event:
    """Preserve one exact bounded adjacent-pair observation Measurement result."""

    finding = ledger.get(finding_event_id)
    if (
        finding is None
        or finding.workspace_id != workspace_id
        or finding.session_id != session_id
    ):
        raise PreservedMaterialMeasurementError(
            "the recovered pair finding is outside this Measurement locality"
        )
    source_ids = finding.payload.get("input_event_ids")
    if not isinstance(source_ids, list):
        raise PreservedMaterialMeasurementError(
            "the recovered pair finding carries no exact source occurrences"
        )
    source_occurrences = []
    for source_id in source_ids:
        source = ledger.get(source_id) if isinstance(source_id, str) else None
        if source is None:
            raise PreservedMaterialMeasurementError(
                "the recovered pair finding names an absent source occurrence"
            )
        source_occurrences.append(source)
    observations = observe_adjacent_pair_observations_from_finding(
        ledger,
        finding_event_id=finding_event_id,
        occurrences=source_occurrences,
    )
    act_id = new_id("adjacent_pair_observation_measurement_act")
    act_occurrence_id = new_id("adjacent_pair_observation_measurement_occurrence")
    result_payload = {
        "finding_event_id": finding_event_id,
        "source_occurrence_ids": list(source_ids),
        "observations": [
            _adjacent_pair_observation_payload(observation)
            for observation in observations
        ],
    }
    applicable_inputs = [
        {
            "input_ref": finding_event_id,
            "role": "recovered ordered-pair finding",
            "standing": "applicable",
        },
        *[
            {
                "input_ref": source_id,
                "role": "exact preserved source occurrence",
                "standing": "applicable",
            }
            for source_id in source_ids
        ],
    ]
    act_evidence = ledger.append(
        ADJACENT_PAIR_OBSERVATION_ACT_EVIDENCE_KIND,
        workspace_id,
        {
            "target_act_id": act_id,
            "act_occurrence_id": act_occurrence_id,
            "act": "exact adjacent-pair observation Measurement",
            "responsibility": ADJACENT_PAIR_OBSERVATION_RESPONSIBILITY,
            "responsible_boundary": "this Seed",
            "input_applicability": applicable_inputs,
            "result_commitment": yield_commitment(
                ADJACENT_PAIR_OBSERVATION_CONVENTION,
                result_payload,
            ),
            "standing": "occurred",
            "authority": (
                "Evidence concerning this exact bounded Measurement occurrence only"
            ),
        },
        session_id=session_id,
    )
    yield_evidence = _record_yield_evidence(
        ledger,
        workspace_id=workspace_id,
        session_id=session_id,
        convention=ADJACENT_PAIR_OBSERVATION_CONVENTION,
        yielding_act="exact adjacent-pair observation Measurement",
        act_occurrence_id=act_occurrence_id,
        yielded_result_kind="exact adjacent-pair observations",
        result_identity=f"adjacent-pair-observation-result:{act_occurrence_id}",
        yielded_content=result_payload,
        responsibility=ADJACENT_PAIR_OBSERVATION_RESPONSIBILITY,
        responsible_boundary="this Seed",
    )
    carriage_evidence = ledger.append(
        ADJACENT_PAIR_OBSERVATION_CARRIAGE_EVIDENCE_KIND,
        workspace_id,
        {
            "act_occurrence_id": act_occurrence_id,
            "content_kind": "exact adjacent-pair observations",
            "carried_content": result_payload,
            "standing": "carried",
            "authority": (
                "Evidence only for this exact result-to-occurrence Carriage"
            ),
        },
        session_id=session_id,
    )
    return ledger.append(
        ADJACENT_PAIR_OBSERVATION_RECORDED_KIND,
        workspace_id,
        {
            **result_payload,
            "dimensions": {
                "identity": act_occurrence_id,
                "content": "exact adjacent-pair observations around recovered ordered pairs",
                "standing": "measured",
                "source_provenance": [finding_event_id, *source_ids],
                "responsibility": ADJACENT_PAIR_OBSERVATION_RESPONSIBILITY,
                "responsible_boundary": "this Seed",
                "authority": (
                    "measurement Evidence only; establishes no classification, "
                    "represented relation, or Standing beyond this result"
                ),
                "scope_locality": (
                    f"workspace:{workspace_id};session:{session_id}"
                ),
                "occurrence_preservation": (
                    "one exact adjacent-pair observation Measurement occurrence recorded"
                ),
            },
            "target_act_id": act_id,
            "act_occurrence_id": act_occurrence_id,
            "responsible_act_evidence_id": act_evidence.id,
            "yield_evidence_id": yield_evidence.id,
            "carriage_evidence_id": carriage_evidence.id,
            "known_loss": [],
            "unknowns": [
                "what any carried representation means remains Unknown",
            ],
            "conflicts": [],
            "mutates_cluster": False,
        },
        session_id=session_id,
    )


def _adjacent_pair_observation_from_payload(
    value: object,
) -> AdjacentPairObservation:
    if not isinstance(value, dict):
        raise PreservedMaterialMeasurementError(
            "a recorded adjacent-pair observation is not an exact coordinate mapping"
        )

    def positioned(item: object) -> PositionedRepresentationOccurrence | None:
        if item is None:
            return None
        if not isinstance(item, dict):
            raise PreservedMaterialMeasurementError(
                "a recorded position is not an exact coordinate mapping"
            )
        source_id = item.get("source_occurrence_id")
        position = item.get("position")
        representation = item.get("representation")
        if (
            not isinstance(source_id, str)
            or not source_id
            or not isinstance(position, int)
            or isinstance(position, bool)
            or position < 0
            or not isinstance(representation, str)
            or not representation
        ):
            raise PreservedMaterialMeasurementError(
                "a recorded position carries malformed coordinates"
            )
        return PositionedRepresentationOccurrence(
            source_id,
            position,
            representation,
        )

    pair_value = value.get("pair_occurrence")
    if not isinstance(pair_value, dict):
        raise PreservedMaterialMeasurementError(
            "a recorded adjacent-pair observation carries no exact pair occurrence"
        )
    ordered_pair = pair_value.get("ordered_pair")
    if (
        not isinstance(ordered_pair, list)
        or len(ordered_pair) != 2
        or not all(isinstance(item, str) and item for item in ordered_pair)
    ):
        raise PreservedMaterialMeasurementError(
            "a recorded adjacent-pair observation carries no exact ordered pair"
        )
    pair_left = positioned(pair_value.get("left"))
    pair_right = positioned(pair_value.get("right"))
    if pair_left is None or pair_right is None:
        raise PreservedMaterialMeasurementError(
            "a recorded pair occurrence is missing one exact position"
        )
    source_id = value.get("source_occurrence_id")
    exact_order = value.get("exact_order")
    evidence = value.get("evidence")
    if (
        not isinstance(source_id, str)
        or not source_id
        or not isinstance(exact_order, list)
        or not all(
            isinstance(position, int)
            and not isinstance(position, bool)
            and position >= 0
            for position in exact_order
        )
        or not isinstance(evidence, dict)
    ):
        raise PreservedMaterialMeasurementError(
            "a recorded adjacent-pair observation carries malformed bounds"
        )
    return AdjacentPairObservation(
        left_occurrence=positioned(value.get("left_occurrence")),
        pair_occurrence=ExactAdjacentPairOccurrence(
            AdjacentPair(*ordered_pair),
            pair_left,
            pair_right,
        ),
        right_occurrence=positioned(value.get("right_occurrence")),
        source_occurrence_id=source_id,
        exact_order=tuple(exact_order),
        evidence=evidence,
    )


def get_recorded_adjacent_pair_observations(
    ledger: EventLedger,
    event_id: str,
) -> tuple[AdjacentPairObservation, ...] | None:
    """Recover an exact recorded result without repeating its Measurement."""

    carrier = ledger.get(event_id)
    if carrier is None:
        return None
    if (
        carrier.kind != ADJACENT_PAIR_OBSERVATION_RECORDED_KIND
        or ledger.integrity_of(event_id) == CORRUPTED
    ):
        raise PreservedMaterialMeasurementError(
            "the adjacent-pair observation result carrier is absent or corrupted"
        )
    finding_id = carrier.payload.get("finding_event_id")
    source_ids = carrier.payload.get("source_occurrence_ids")
    carried_observations = carrier.payload.get("observations")
    if (
        not isinstance(finding_id, str)
        or not finding_id
        or not isinstance(source_ids, list)
        or not all(isinstance(value, str) and value for value in source_ids)
        or not isinstance(carried_observations, list)
    ):
        raise PreservedMaterialMeasurementError(
            "the adjacent-pair observation result carries malformed result coordinates"
        )
    result_payload = {
        "finding_event_id": finding_id,
        "source_occurrence_ids": source_ids,
        "observations": carried_observations,
    }
    act_evidence_id = carrier.payload.get("responsible_act_evidence_id")
    yield_evidence_id = carrier.payload.get("yield_evidence_id")
    carriage_evidence_id = carrier.payload.get("carriage_evidence_id")
    if not all(
        isinstance(value, str) and value
        for value in (act_evidence_id, yield_evidence_id, carriage_evidence_id)
    ):
        raise PreservedMaterialMeasurementError(
            "the adjacent-pair observation result carries malformed Evidence references"
        )
    act_evidence = ledger.get(act_evidence_id)
    yield_evidence = ledger.get(yield_evidence_id)
    carriage_evidence = ledger.get(carriage_evidence_id)
    if (
        act_evidence is None
        or act_evidence.kind != ADJACENT_PAIR_OBSERVATION_ACT_EVIDENCE_KIND
        or yield_evidence is None
        or yield_evidence.kind != "operator.yield.evidence_recorded"
        or carriage_evidence is None
        or carriage_evidence.kind != ADJACENT_PAIR_OBSERVATION_CARRIAGE_EVIDENCE_KIND
    ):
        raise PreservedMaterialMeasurementError(
            "the adjacent-pair observation result carries incomplete edge Evidence"
        )
    act_occurrence_id = carrier.payload.get("act_occurrence_id")
    target_act_id = carrier.payload.get("target_act_id")
    commitment = yield_commitment(ADJACENT_PAIR_OBSERVATION_CONVENTION, result_payload)
    if (
        not isinstance(act_occurrence_id, str)
        or not isinstance(target_act_id, str)
        or act_evidence.payload.get("target_act_id") != target_act_id
        or act_evidence.payload.get("act_occurrence_id") != act_occurrence_id
        or yield_evidence.payload.get("dimensions", {}).get("act_occurrence_id")
        != act_occurrence_id
        or carriage_evidence.payload.get("act_occurrence_id")
        != act_occurrence_id
        or act_evidence.payload.get("result_commitment") != commitment
        or yield_evidence.payload.get("yield_commitment") != commitment
        or yield_evidence.payload.get("yield_convention")
        != ADJACENT_PAIR_OBSERVATION_CONVENTION
        or carriage_evidence.payload.get("carried_content") != result_payload
    ):
        raise PreservedMaterialMeasurementError(
            "the adjacent-pair observation edge Evidence concerns different coordinates"
        )
    expected_inputs = [
        {
            "input_ref": finding_id,
            "role": "recovered ordered-pair finding",
            "standing": "applicable",
        },
        *[
            {
                "input_ref": source_id,
                "role": "exact preserved source occurrence",
                "standing": "applicable",
            }
            for source_id in source_ids
        ],
    ]
    if act_evidence.payload.get("input_applicability") != expected_inputs:
        raise PreservedMaterialMeasurementError(
            "the adjacent-pair observation Act Evidence concerns different inputs"
        )
    finding = ledger.get(finding_id)
    if (
        finding is None
        or ledger.integrity_of(finding_id) == CORRUPTED
        or not _is_established_after_measurement(finding)
        or finding.workspace_id != carrier.workspace_id
        or finding.session_id != carrier.session_id
        or finding.payload.get("input_event_ids") != source_ids
    ):
        raise PreservedMaterialMeasurementError(
            "the adjacent-pair observation pair-finding Evidence does not reconstruct"
        )
    sources: dict[str, Event] = {}
    for source_id in source_ids:
        source = ledger.get(source_id)
        if (
            source is None
            or source.kind != INGRESS_OCCURRED_KIND
            or ledger.integrity_of(source_id) == CORRUPTED
            or source.workspace_id != carrier.workspace_id
            or source.session_id != carrier.session_id
            or not isinstance(source.payload.get("decoded_text"), str)
        ):
            raise PreservedMaterialMeasurementError(
                "the adjacent-pair observation source Evidence does not reconstruct"
            )
        sources[source_id] = source
    observations = tuple(
        _adjacent_pair_observation_from_payload(value)
        for value in carried_observations
    )
    if any(
        observation.evidence.get("pair_finding_event_id") != finding_id
        or observation.source_occurrence_id not in sources
        or observation.evidence.get("exact_decoded_text")
        != sources[observation.source_occurrence_id].payload.get("decoded_text")
        or observation.evidence.get("workspace_id") != carrier.workspace_id
        or observation.evidence.get("session_id") != carrier.session_id
        for observation in observations
    ):
        raise PreservedMaterialMeasurementError(
            "a carried adjacent-pair observation names different Evidence"
        )
    return observations


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


class AdjacentPairMeasurementIndex:
    """One tokenization of a bounded material set for many pair measurements.

    The index changes representation cost only.  Each answer retains the exact
    first-match behavior, declaration, input occurrence identities, and
    empty-result behavior of :func:`measure_adjacent_pair`.
    """

    def __init__(self, occurrences: Iterable[Event]):
        material = tuple(occurrences)
        for event in material:
            if event.kind != INGRESS_OCCURRED_KIND:
                raise PreservedMaterialMeasurementError(
                    f"only preserved ingress occurrences may be measured: {event.kind}"
                )
        self._event_ids = tuple(event.id for event in material)
        self._contexts = tuple(
            self._index_positions(_positions(event.payload["decoded_text"]))
            for event in material
        )
        # Which occurrences can answer a form at all.
        #
        # Every form is keyed: `preceding` and `following` on the ordered pair,
        # `before_same_right` on the pair's right representation,
        # `after_same_left` on its left. An occurrence carrying none of those
        # returns no occupant, and a measurement already skips a `None`
        # occupant, so visiting it changes no count.
        #
        # `#2484` measured why this is worth inverting rather than scanning.
        # Scanning every occurrence for every pair costs 4 x pairs x
        # occurrences, and that term became prohibitive with depth: 300 lines a
        # body cost 2.6 million lookups, 3,000 cost 161 million, and a run at
        # that depth was abandoned.
        #
        # It is not quadratic, and the measured reason is worth keeping.
        # Quadratic would need distinct pairs to grow linearly with material.
        # They do not — over 200 to 800 lines, pairs ~ lines^0.74-0.92, so the
        # pair x occurrence term predicts lines^1.74-1.92 and the stage
        # measured lines^1.65-1.81. Strongly superlinear, short of quadratic.
        pair_contexts: dict[tuple[str, str], list[int]] = {}
        right_contexts: dict[str, list[int]] = {}
        left_contexts: dict[str, list[int]] = {}
        for position, (first_pair_context, left_alternatives, right_alternatives) in enumerate(
            self._contexts
        ):
            for key in first_pair_context:
                pair_contexts.setdefault(key, []).append(position)
            for key in left_alternatives:
                right_contexts.setdefault(key, []).append(position)
            for key in right_alternatives:
                left_contexts.setdefault(key, []).append(position)
        self._pair_contexts = {key: tuple(v) for key, v in pair_contexts.items()}
        self._right_contexts = {key: tuple(v) for key, v in right_contexts.items()}
        self._left_contexts = {key: tuple(v) for key, v in left_contexts.items()}

    _EMPTY: tuple[int, ...] = ()

    def _answering_contexts(self, pair: "AdjacentPair", form: str) -> tuple[int, ...]:
        """The occurrence positions that can yield an occupant for this form.

        Order is ascending append order, the same order `self._contexts` is
        visited in, so a form whose answer depends on which occurrence is
        reached first is unaffected.

        Key presence is not occupant existence. A candidate occurrence is one
        that *could* answer; `_occupant` still applies the form's own test,
        including the different-left and different-right requirements, and
        still returns `None`.

        Sharing an index key is representation reuse and nothing more. Two
        pairs visiting the same occurrences are not thereby a collective, a
        proposal, a relation, or a basis for Compare.
        """

        if form in {"preceding", "following"}:
            return self._pair_contexts.get((pair.left, pair.right), self._EMPTY)
        if form == "before_same_right":
            return self._right_contexts.get(pair.right, self._EMPTY)
        if form == "after_same_left":
            return self._left_contexts.get(pair.left, self._EMPTY)
        raise PreservedMaterialMeasurementError(f"unknown adjacent-pair form: {form}")

    @property
    def event_ids(self) -> tuple[str, ...]:
        """The exact input sequence every finding this index yields carries.

        Exposed so a support binding can be formed over *this* tuple, which is
        what makes reuse checkable in constant time.

        **An equal tuple is not a different inputs.** Two tuples with the
        same contents describe the same exact ordered inputs, and the
        support commitment says so. What object identity establishes is
        narrower: that a finding came from the captured inputs whose basis
        was already declared, without re-deriving anything. An equal copy may
        well be the same inputs — the fast path simply has not established
        it, so it is refused rather than assumed.
        """

        return self._event_ids

    @staticmethod
    def _index_positions(parts: Sequence[str]) -> tuple[
        dict[tuple[str, str], tuple[str | None, str | None]],
        dict[str, tuple[str, ...]],
        dict[str, tuple[str, ...]],
    ]:
        first_pair_context = {}
        left_alternatives: dict[str, list[str]] = {}
        right_alternatives: dict[str, list[str]] = {}
        for index in range(len(parts) - 1):
            left = parts[index]
            right = parts[index + 1]
            first_pair_context.setdefault(
                (left, right),
                (
                    parts[index - 1] if index > 0 else None,
                    parts[index + 2] if index + 2 < len(parts) else None,
                ),
            )
            lefts = left_alternatives.setdefault(right, [])
            if left not in lefts and len(lefts) < 2:
                lefts.append(left)
            rights = right_alternatives.setdefault(left, [])
            if right not in rights and len(rights) < 2:
                rights.append(right)
        return (
            first_pair_context,
            {key: tuple(values) for key, values in left_alternatives.items()},
            {key: tuple(values) for key, values in right_alternatives.items()},
        )

    @staticmethod
    def _occupant(
        context: tuple[
            dict[tuple[str, str], tuple[str | None, str | None]],
            dict[str, tuple[str, ...]],
            dict[str, tuple[str, ...]],
        ],
        pair: AdjacentPair,
        form: str,
    ) -> str | None:
        first_pair_context, left_alternatives, right_alternatives = context
        if form in {"preceding", "following"}:
            pair_context = first_pair_context.get((pair.left, pair.right))
            if pair_context is None:
                return None
            if form == "preceding":
                return pair_context[0]
            return pair_context[1]
        if form == "before_same_right":
            return next(
                (
                    left
                    for left in left_alternatives.get(pair.right, ())
                    if left != pair.left
                ),
                None,
            )
        if form == "after_same_left":
            return next(
                (
                    right
                    for right in right_alternatives.get(pair.left, ())
                    if right != pair.right
                ),
                None,
            )
        raise PreservedMaterialMeasurementError(f"unknown adjacent-pair form: {form}")

    def measure(
        self,
        pair: AdjacentPair,
        *,
        counting_scope: str,
        premise_event_id: str,
    ) -> dict[str, MeasurementFinding]:
        """Apply every established pair form to one pair without retokenizing."""

        findings = {}
        for form in PAIR_MEASUREMENT_FORMS:
            counts: dict[str, int] = {}
            positions_measured = 0
            for position in self._answering_contexts(pair, form):
                occupant = self._occupant(self._contexts[position], pair, form)
                if occupant is None:
                    continue
                positions_measured += 1
                counts[occupant] = counts.get(occupant, 0) + 1
            occupancies = tuple(
                Occupancy(representation=representation, occurrence_count=count)
                for representation, count in sorted(
                    counts.items(), key=lambda item: (-item[1], item[0])
                )
            )
            findings[form] = MeasurementFinding(
                declared=DeclaredMeasurement(
                    representation_measured=(
                        f"the {form.replace('_', ' ')} position of the ordered pair "
                        f"{pair.left!r} {pair.right!r}"
                    ),
                    equivalence_rule=EQUIVALENCE_RULE,
                    counting_scope=counting_scope,
                    premise_event_id=premise_event_id,
                    form=form,
                    relative_to=(pair.left, pair.right),
                    measured_position=MEASURED_POSITIONS[form],
                ),
                positions_measured=positions_measured,
                occupancies=occupancies,
                input_event_ids=self._event_ids,
            )
        return findings

    def measure_all(
        self,
        pair_premises: Iterable[tuple[AdjacentPair, str]],
        *,
        counting_scope: str,
    ) -> list[tuple[AdjacentPair, dict[str, MeasurementFinding]]]:
        """Measure every supplied pair occurrence, preserving order and premise."""

        return list(
            self.iter_measure_all(
                pair_premises,
                counting_scope=counting_scope,
            )
        )

    def iter_measure_all(
        self,
        pair_premises: Iterable[tuple[AdjacentPair, str]],
        *,
        counting_scope: str,
    ) -> Iterator[tuple[AdjacentPair, dict[str, MeasurementFinding]]]:
        """Stream every supplied pair occurrence with its exact premise."""

        for pair, premise_event_id in pair_premises:
            if not isinstance(premise_event_id, str) or not premise_event_id:
                raise PreservedMaterialMeasurementError(
                    f"no premise occurrence identity supplied for {pair}"
                )
            yield (
                pair,
                self.measure(
                    pair,
                    counting_scope=counting_scope,
                    premise_event_id=premise_event_id,
                ),
            )


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
    completeness_boundary: EventLedgerBoundary,
) -> dict[str, Event]:
    """Preserve every measurement, including the ones that found nothing.

    A question whose answer was absent is recorded as having been asked. A
    battery that quietly dropped its empty results would report only the
    questions that happened to succeed.
    """

    names = tuple(findings)
    events = record_measurement_findings(
        ledger,
        workspace_id=workspace_id,
        session_id=session_id,
        findings=(
            (
                findings[name],
                {
                    "measurement": name,
                    "pair_left": pair.left,
                    "pair_right": pair.right,
                    **_adjacent_pair_result_assertion_fields(
                        workspace_id=workspace_id,
                        session_id=session_id,
                        pair=pair,
                        finding=findings[name],
                        completeness_boundary=completeness_boundary,
                    ),
                },
            )
            for name in names
        ),
    )
    return dict(zip(names, events))


def record_adjacent_pair_measurement_layer(
    ledger: EventLedger,
    *,
    workspace_id: str,
    session_id: str,
    counting_scope: str,
) -> int:
    """Record the four-form battery for every pair supplied by ``after`` findings.

    One ledger boundary fixes both the preserved material and the recorded
    premise occurrences eligible for this layer.  Each occupancy of each
    eligible premise remains a separate ``(pair, premise occurrence)`` input;
    equal pair values from different premises are never collapsed.

    The return is only the number of result occurrences recorded.  Results are
    not retained in a second in-memory collection after the ledger preserves
    them, and this function does not have as input the results into another layer.
    """

    boundary = ledger.capture_boundary()
    material = tuple(
        ledger.iter_session_kind(
            workspace_id,
            session_id,
            INGRESS_OCCURRED_KIND,
            through=boundary,
        )
    )
    index = AdjacentPairMeasurementIndex(material)
    # One inputs, declared once. Every finding this layer yields input
    # exactly these identities through exactly this boundary.
    declared_support = _DeclaredSupportBinding(
        workspace_id=workspace_id,
        session_id=session_id,
        occurrence_kind=INGRESS_OCCURRED_KIND,
        boundary=boundary,
        identities=index.event_ids,
    )
    pair_premises = []
    for premise in ledger.iter_session_kind(
        workspace_id,
        session_id,
        MEASUREMENT_RECORDED_KIND,
        through=boundary,
    ):
        if not _is_established_after_measurement(premise):
            continue
        for pair in _adjacent_pairs_from_event(premise):
            pair_premises.append((pair, premise.id))

    record_batch_size = 256
    pending_records = []
    recorded_count = 0
    for pair, findings in index.iter_measure_all(
        pair_premises,
        counting_scope=counting_scope,
    ):
        pending_records.extend(
            (
                finding,
                {
                    "measurement": name,
                    "pair_left": pair.left,
                    "pair_right": pair.right,
                    **_adjacent_pair_result_assertion_fields(
                        workspace_id=workspace_id,
                        session_id=session_id,
                        pair=pair,
                        finding=finding,
                        completeness_boundary=boundary,
                        declared_support=declared_support,
                    ),
                },
            )
            for name, finding in findings.items()
        )
        if len(pending_records) >= record_batch_size:
            recorded_count += len(
                record_measurement_findings(
                    ledger,
                    workspace_id=workspace_id,
                    session_id=session_id,
                    findings=pending_records,
                )
            )
            pending_records.clear()
    if pending_records:
        recorded_count += len(
            record_measurement_findings(
                ledger,
                workspace_id=workspace_id,
                session_id=session_id,
                findings=pending_records,
            )
        )
    return recorded_count


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
    that yielded any answer. Agreement is the discriminator `#2390` found
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
    in the sense `01.Standing.E` governs, establishes no relation between the
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
    occurrence extends that far, so the displacements returned are a finding about
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
