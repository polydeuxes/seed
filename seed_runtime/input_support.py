"""Address exact input support through one append boundary."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable

from seed_runtime.events import EventLedger, EventLedgerBoundary

class InputSupportError(ValueError):
    pass


@dataclass(frozen=True)
class InputSupport:
    """Where a finding's support lives, and what it must read to."""

    locality_identity: str
    occurrence_kind: str
    boundary_identity: str
    support_count: int

    def __post_init__(self) -> None:
        for name in ("locality_identity", "occurrence_kind", "boundary_identity"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value:
                raise InputSupportError(f"input support requires {name}")
        if not isinstance(self.support_count, int) or isinstance(self.support_count, bool):
            raise InputSupportError(
                "input support requires an integer support count, not "
                f"{type(self.support_count).__name__}"
            )
        if self.support_count < 0:
            raise InputSupportError("input support cannot carry a negative count")

    def to_json_dict(self) -> dict[str, Any]:
        return {
            "scope": {
                "locality_identity": self.locality_identity,
                "occurrence_kind": self.occurrence_kind,
            },
            "boundary": {"identity": self.boundary_identity},
            "support_count": self.support_count,
        }

    @classmethod
    def from_json_dict(cls, value: Any) -> "InputSupport":
        if not isinstance(value, dict):
            raise InputSupportError("input support is not present")
        try:
            scope = value["scope"]
            return cls(
                locality_identity=scope["locality_identity"],
                occurrence_kind=scope["occurrence_kind"],
                boundary_identity=value["boundary"]["identity"],
                support_count=value["support_count"],
            )
        except (KeyError, TypeError) as exc:
            raise InputSupportError(f"input support is incomplete: {exc}") from exc


def declare_input_support(
    *,
    locality_identity: str,
    occurrence_kind: str,
    boundary: EventLedgerBoundary,
    occurrence_references: Iterable[str],
) -> InputSupport:
    references = tuple(occurrence_references)
    return InputSupport(
        locality_identity=locality_identity,
        occurrence_kind=occurrence_kind,
        boundary_identity=boundary.identity,
        support_count=len(references),
    )


class InputSupportValidator:

    def __init__(self, ledger: EventLedger) -> None:
        self._ledger = ledger
        self._validated: dict[tuple[str, str, str], tuple[str, ...]] = {}
        self.reads = 0
        self.reuses = 0

    @property
    def ledger(self) -> EventLedger:
        return self._ledger

    def validate(self, support: InputSupport) -> tuple[str, ...]:
        key = (
            support.locality_identity,
            support.occurrence_kind,
            support.boundary_identity,
        )
        cached = self._validated.get(key)
        if cached is not None:
            if len(cached) != support.support_count:
                raise InputSupportError(
                    "the validated support does not match its declared count"
                )
            self.reuses += 1
            return cached
        self.reads += 1
        identities = tuple(
            self._ledger.iter_locality_kind_identities(
                support.locality_identity,
                support.occurrence_kind,
                through=EventLedgerBoundary(support.boundary_identity),
            )
        )
        if len(identities) != support.support_count:
            raise InputSupportError(
                "the validated support does not match its declared count"
            )
        self._validated[key] = identities
        return identities
