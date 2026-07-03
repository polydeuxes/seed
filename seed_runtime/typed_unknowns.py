"""Implementation-local preservation for typed unknown records."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TypedUnknownRecord:
    """Bounded typed Unknown produced from unresolved investigation state."""

    unknown_type: str
    area: str
    reason: str

    def to_public_dict(self) -> dict[str, str]:
        """Return the existing compatibility shape consumed by public surfaces."""

        return {"area": self.area, "reason": self.reason}


def preserve_typed_unknown(
    *, unknown_type: str, area: str, reason: str
) -> TypedUnknownRecord:
    """Preserve constitutional Unknown type without resolving the finding."""

    return TypedUnknownRecord(
        unknown_type=unknown_type,
        area=area,
        reason=reason,
    )


def typed_unknowns_to_public_dicts(
    unknowns: list[TypedUnknownRecord],
) -> list[dict[str, str]]:
    """Project typed Unknown records to the unchanged public unknowns shape."""

    return [unknown.to_public_dict() for unknown in unknowns]
