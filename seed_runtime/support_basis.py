"""A support basis, and why it is not a support enumeration.

`05.Testimony:27` requires a consumed input's support basis to be preserved. It
does not require that basis to be preserved as a list of every supporting
occurrence, and until now this runtime preserved it that way — every finding
carried the complete ordered identity of every occurrence it consumed.

`#2486` measured what that cost on real material. At 4,000 lines a body, one
recorded finding is 57,886 bytes and **56,000 of them are that enumeration**:

```text
    300 lines   4,200 B of  6,024 B   70%
  1,000 lines  14,000 B of 15,790 B   89%
  4,000 lines  56,000 B of 57,886 B   97%
```

The same identities are copied into every finding of a body, because every
finding consumed the same complete bounded population. And the cost is paid three
times — writing the enumeration, decoding it on every later read, and then
re-deriving the population from the ledger in order to check it against itself.

**What is preserved here instead is the basis, and the enumeration remains one
Representation of it.**

```text
  scope              workspace, session, occurrence kind
  boundary           the exact append prefix the selection ran through
  selection rule     which occurrences within that scope were taken
  commitment         a digest over the exact ordered result
```

**The selection rule is not metadata.** It is part of the basis's identity. Today
every act consumes the complete population, so scope and boundary alone would
reconstruct it — but an act that consumed three occurrences out of four thousand
would be reconstructed as having consumed all four thousand, and the reference
would be silently false rather than merely lossy. The rule is what keeps a
subset-consuming act representable, and an unrecognised rule is refused rather
than assumed to mean the whole population.

**The commitment is what makes recovery checkable without the enumeration.**
The check it replaces also recovered the population from the ledger and compared
it against the carried list, so this is not a stronger guarantee — it preserves
substantially the same exactness in a form that is compact and reusable. What
the commitment adds is that a later change to the selection code cannot silently
redefine what an old finding's support was, and that one verified population can
serve every finding referencing the same basis.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
from typing import Any, Iterable

from seed_runtime.events import EventLedger, EventLedgerBoundary

_COMMITMENT_DOMAIN = b"seed.support-basis.v1\0"

# Every selection a support basis may declare. A rule outside this set is
# refused: a basis whose selection cannot be performed is not recoverable, and
# guessing that it meant the whole population is the failure this set exists to
# prevent.
COMPLETE_INGRESS_POPULATION = "every preserved occurrence of the scope's kind through the boundary"
SUPPORT_SELECTION_RULES: frozenset[str] = frozenset({COMPLETE_INGRESS_POPULATION})


class SupportBasisError(ValueError):
    """A support basis could not be declared, recovered, or verified."""


def _commit_part(digest: "hashlib._Hash", value: str) -> None:
    """Commit one part so no part can be mistaken for a different division.

    Length-prefixed rather than separated. A separator only divides parts
    unambiguously while no part can contain it, and nothing constrains an
    `Event.id` to avoid one. Constraining identities to suit this digest would
    let a commitment dictate the repository's identity grammar, which is
    backwards; the representation is made unambiguous instead.
    """

    if not isinstance(value, str):
        raise SupportBasisError(
            f"a committed part must be a representation, not {type(value).__name__}"
        )
    encoded = value.encode("utf-8")
    digest.update(len(encoded).to_bytes(8, "big"))
    digest.update(encoded)


def support_commitment(selection_rule: str, identities: Iterable[str]) -> str:
    """A digest over the exact ordered identities the selection produced.

    The rule is committed alongside them, so two selections that happen to
    return the same identities from the same scope are not interchangeable.

    Its Standing is *"I represent this exact ordered support population"*, and a
    representation under which two different populations produce one digest
    cannot carry that. The separated encoding this replaces could not: with
    a NUL between parts, `("a", "b\0c")` and `("a\0b", "c")` encoded
    identically, and so did rule `"a"` with identity `"b"` against rule
    `"a\0b"` with no identities. Neither was a hash collision — both handed
    SHA-256 the same input for different populations.
    """

    digest = hashlib.sha256(_COMMITMENT_DOMAIN)
    _commit_part(digest, selection_rule)
    for identity in identities:
        _commit_part(digest, identity)
    return digest.hexdigest()


@dataclass(frozen=True)
class SupportBasis:
    """Where a finding's support lives, and what it must recover to."""

    workspace_id: str
    session_id: str
    occurrence_kind: str
    boundary_commitment: str
    selection_rule: str
    commitment: str
    support_count: int

    def __post_init__(self) -> None:
        # Established as a representation before it is looked up. Membership of
        # a frozenset hashes its argument, so an unhashable value leaked a raw
        # TypeError rather than the refusal this declares.
        if not isinstance(self.selection_rule, str):
            raise SupportBasisError(
                "a support basis must declare a recognised selection, not "
                f"{type(self.selection_rule).__name__}"
            )
        if self.selection_rule not in SUPPORT_SELECTION_RULES:
            raise SupportBasisError(
                f"a support basis must declare a recognised selection: {self.selection_rule!r}"
            )
        for name in ("workspace_id", "session_id", "occurrence_kind",
                     "boundary_commitment", "commitment"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value:
                raise SupportBasisError(f"a support basis requires {name}")
        # A count coordinate must be able to be a count. `bool` is excluded
        # because it is an `int` in Python and `True == 1`, so a basis carrying
        # `True` would agree with a one-occurrence population — a coordinate
        # claiming an exact count while carrying something that is not one.
        if not isinstance(self.support_count, int) or isinstance(self.support_count, bool):
            raise SupportBasisError(
                "a support basis requires an integer support count, not "
                f"{type(self.support_count).__name__}"
            )
        if self.support_count < 0:
            raise SupportBasisError("a support basis cannot support a negative count")

    def to_json_dict(self) -> dict[str, Any]:
        return {
            "scope": {
                "workspace_id": self.workspace_id,
                "session_id": self.session_id,
                "occurrence_kind": self.occurrence_kind,
            },
            "boundary": {"commitment": self.boundary_commitment},
            "selection_rule": self.selection_rule,
            "commitment": self.commitment,
            "support_count": self.support_count,
        }

    @classmethod
    def from_json_dict(cls, value: Any) -> "SupportBasis":
        if not isinstance(value, dict):
            raise SupportBasisError("a support basis is not present")
        try:
            scope = value["scope"]
            return cls(
                workspace_id=scope["workspace_id"],
                session_id=scope["session_id"],
                occurrence_kind=scope["occurrence_kind"],
                boundary_commitment=value["boundary"]["commitment"],
                selection_rule=value["selection_rule"],
                commitment=value["commitment"],
                support_count=value["support_count"],
            )
        except (KeyError, TypeError) as exc:
            raise SupportBasisError(f"a support basis is incomplete: {exc}") from exc


def declare_complete_population(
    *,
    workspace_id: str,
    session_id: str,
    occurrence_kind: str,
    boundary: EventLedgerBoundary,
    identities: Iterable[str],
) -> SupportBasis:
    """Declare the basis of a selection that has already been performed."""

    ordered = tuple(identities)
    return SupportBasis(
        workspace_id=workspace_id,
        session_id=session_id,
        occurrence_kind=occurrence_kind,
        boundary_commitment=boundary.commitment,
        selection_rule=COMPLETE_INGRESS_POPULATION,
        commitment=support_commitment(COMPLETE_INGRESS_POPULATION, ordered),
        support_count=len(ordered),
    )


class SupportRecovery:
    """Recovers a declared support basis, once per distinct basis.

    **Reuse here is not a skipped verification, and a cache hit does not read
    the ledger.** Every distinct uncached basis is recovered from the ledger,
    has the basis's own selection performed, and is refused unless the result
    reproduces the committed digest. A later reference to that exact verified
    basis may then reuse the recovered population — which is lawful because the
    cache is keyed by the commitment, so a second basis reaches it only by
    committing to exactly the same identities under exactly the same rule, and
    because a hit still rechecks the declared count.

    `#2486` measured the reuse this exists for: recovering one count layer
    performed 205,328 ingress reads over **16** distinct populations.

    An instance is bounded to one act. It holds identities, not occurrences.
    """

    def __init__(self, ledger: EventLedger) -> None:
        self._ledger = ledger
        self._recovered: dict[tuple[str, str, str, str, str], tuple[str, ...]] = {}
        self.reads = 0
        self.reuses = 0

    def recover(self, basis: SupportBasis) -> tuple[str, ...]:
        key = (
            basis.workspace_id,
            basis.session_id,
            basis.occurrence_kind,
            basis.boundary_commitment,
            basis.commitment,
        )
        cached = self._recovered.get(key)
        if cached is not None:
            # The count is rechecked here rather than keyed on. A commitment
            # identifies the actual support, so a basis carrying a count that
            # contradicts it is refused — not admitted as a second population.
            # Without this the count check ran only on the first recovery of a
            # population, so whether a forged count was caught depended on what
            # this act happened to have recovered earlier.
            if len(cached) != basis.support_count:
                raise SupportBasisError(
                    "the recovered support does not match its declared count"
                )
            self.reuses += 1
            return cached
        # No rule check here. A basis refuses any selection outside
        # `SUPPORT_SELECTION_RULES` at construction, and that set has one
        # member, so a basis reaching this point can only carry the complete
        # population — recovery performs every rule a basis can hold.
        #
        # Where a second rule is added, two responsibilities separate here that
        # are currently one: a basis knowing a rule is *recognised*, and a
        # recovery being able to *perform* it. This is where that split goes,
        # and it is not made now because a refusal that cannot fire asserts a
        # distinction the code does not have.
        self.reads += 1
        identities = tuple(
            self._ledger.iter_session_kind_ids(
                basis.workspace_id,
                basis.session_id,
                basis.occurrence_kind,
                through=EventLedgerBoundary(basis.boundary_commitment),
            )
        )
        recovered = support_commitment(basis.selection_rule, identities)
        if recovered != basis.commitment:
            raise SupportBasisError(
                "the recovered support does not reproduce its committed digest"
            )
        if len(identities) != basis.support_count:
            raise SupportBasisError(
                "the recovered support does not match its declared count"
            )
        self._recovered[key] = identities
        return identities
