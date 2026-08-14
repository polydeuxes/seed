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
alternative is an Assertion about two preserved findings. `01.Standing.E` reserves
consuming preserved findings to a bounded comparison, and none is performed.

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
from seed_runtime.support_basis import (
    SupportBasis,
    SupportBasisError,
    SupportRecovery,
    declare_complete_population,
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

POSITIONAL_RESULT_FIDELITY_RESPONSIBILITY = (
    "preserve the fidelity of this measured Assertion's Standing to its "
    "carried coordinates"
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
class RecordedAdjacentPairResultAssertion:
    """One exact positional result, addressable at its producing occurrence."""

    assertion_id: str
    producing_event_id: str
    producing_session_id: str | None
    payload: dict[str, object]
    completeness_boundary: EventLedgerBoundary

    @property
    def reference(self) -> dict[str, str]:
        return {
            "producing_event_id": self.producing_event_id,
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
    """A support basis and the exact population object it was formed over.

    **The binding is established by formation, not by adjacency.** An earlier
    revision was a dataclass holding an identities tuple and a `SupportBasis`
    side by side, with prose saying the second was bound to the first and
    nothing enforcing it — so a basis carrying a forged commitment and count
    could be placed beside an honest population and would be carried onto every
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
        self._basis = declare_complete_population(
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
    """The basis for this finding, declared once per population where supplied.

    A supplied basis is required to describe this finding's own scope, boundary
    and extent. It is not re-derived from the identities, because re-deriving is
    the cost being removed — but a basis that does not match is refused rather
    than carried onto an Assertion it does not describe.
    """

    if declared_support is None:
        return declare_complete_population(
            workspace_id=workspace_id,
            session_id=session_id,
            occurrence_kind=INGRESS_OCCURRED_KIND,
            boundary=completeness_boundary,
            identities=finding.consumed_event_ids,
        )
    if finding.consumed_event_ids is not declared_support.identities:
        raise PreservedMaterialMeasurementError(
            "a declared support binding was not formed over the population object "
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

    ``declared_support`` is the basis already declared for this population,
    bound to the identities it was declared over. A layer measures one bounded
    population, so every finding it produces consumed the same identities under
    the same rule and yields the same basis — and declaring it per finding
    recomputed a digest over the whole population once per result, measured at
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
            "responsibility": POSITIONAL_RESULT_FIDELITY_RESPONSIBILITY,
            "authority_warrant": (
                "measurement evidence only; establishes no represented relation, relation, "
                "kind, or standing beyond this measured Assertion"
            ),
            "scope_locality": "the exact assertion_scope carried here",
            "occurrence_preservation": (
                "one exact result preserved by its producing occurrence"
            ),
        },
        "subject_kind": "assertion",
        "responsibility_owner": "this recorded assertion",
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
    """Recover one canonical result Assertion, or refuse what it carries."""

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
        or support.get("basis") != payload.get("consumed_support")
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
        producing_event_id=event.id,
        producing_session_id=event.session_id,
        payload=payload,
        completeness_boundary=EventLedgerBoundary(boundary["commitment"]),
    )


def get_recorded_adjacent_pair_result_assertion(
    ledger: EventLedger, *, producing_event_id: str, assertion_id: str
) -> RecordedAdjacentPairResultAssertion | None:
    """Resolve one exact occurrence-bound positional result Assertion."""

    event = ledger.get(producing_event_id)
    if event is None:
        return None
    if ledger.integrity_of(producing_event_id) == CORRUPTED:
        raise PreservedMaterialMeasurementError(
            "a corrupted producing occurrence cannot expose a result Assertion"
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
    recovery: SupportRecovery | None = None,
) -> None:
    """Recover the carried support basis and require it to reproduce.

    The occurrence no longer carries every supporting identity, so this no
    longer compares two lists. It performs the basis's own declared selection
    against the ledger and refuses unless the result reproduces the committed
    digest.

    The check this replaces also recovered the population from the ledger, so
    the guarantee is substantially the same one in a compact and reusable form.
    It is not stronger for using a commitment.
    """

    try:
        basis = SupportBasis.from_json_dict(event.payload.get("consumed_support"))
    except SupportBasisError as exc:
        raise PreservedMaterialMeasurementError(
            f"{event.id} does not carry a recoverable support basis: {exc}"
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
    if basis.support_count != event.payload.get("consumed_count"):
        raise PreservedMaterialMeasurementError(
            f"{event.id} carries a support count its basis does not support"
        )
    try:
        (recovery or SupportRecovery(ledger)).recover(basis)
    except SupportBasisError as exc:
        raise PreservedMaterialMeasurementError(
            f"the carried support basis does not recover: {exc}"
        ) from exc


def iter_recorded_adjacent_pair_result_assertions(
    ledger: EventLedger,
    *,
    workspace_id: str,
    session_ids: Iterable[str],
    through: EventLedgerBoundary,
) -> Iterator[RecordedAdjacentPairResultAssertion]:
    """Stream exact result Assertions through one caller-captured boundary.

    Complete ingress recovery is cached only for equal session/boundary pairs.
    The cache contains compact Event identities, not material or result Events.
    """

    recovery = SupportRecovery(ledger)
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
                    "a corrupted producing occurrence cannot expose a result Assertion"
                )
            assertion = assertion_of_recorded_adjacent_pair_result(event)
            _validate_result_assertion_ingress(
                ledger, event, assertion, recovery=recovery
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
    first-match behavior, declaration, consumed occurrence identities, and
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
        """The exact population object every finding this index produces carries.

        Exposed so a support binding can be formed over *this* tuple, which is
        what makes reuse checkable in constant time.

        **An equal tuple is not a different population.** Two tuples with the
        same contents describe the same exact ordered population, and the
        support commitment says so. What object identity establishes is
        narrower: that a finding came from the captured population whose basis
        was already declared, without re-deriving anything. An equal copy may
        well be the same population — the fast path simply has not established
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
                consumed_event_ids=self._event_ids,
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
    them, and this function does not consume the results into another layer.
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
    # One population, declared once. Every finding this layer produces consumed
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
