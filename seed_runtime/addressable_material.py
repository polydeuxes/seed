"""Exact material addressed through one recorded Ingest occurrence."""

from __future__ import annotations

from dataclasses import asdict, dataclass

from seed_runtime.event import Event
from seed_runtime.events import EventLedger
from seed_runtime.material_ingest import (
    MATERIAL_INGEST_OCCURRED_KIND,
    ingested_material_bytes,
)


class MaterialAddressError(ValueError):
    pass


@dataclass(frozen=True)
class SourceSpan:
    source_reference: str
    start: int
    end: int


@dataclass(frozen=True)
class ExactMaterial:
    material_reference: str
    exact_bytes_hex: str
    source_span: SourceSpan


@dataclass(frozen=True)
class AddressableMaterial:
    material_representation_identity: str
    ingest_event_reference: str
    exact_material: ExactMaterial
    source_role: str
    provenance: tuple[str, ...]
    scope: tuple[str, ...]
    known_loss: tuple[str, ...]
    unknowns: tuple[str, ...]
    authority_limits: tuple[str, ...]

    def to_json_dict(self) -> dict[str, object]:
        return asdict(self)


def address_ingested_material(
    *, ingest_occurrence: Event, ledger: EventLedger
) -> AddressableMaterial:
    if ingest_occurrence.kind != MATERIAL_INGEST_OCCURRED_KIND:
        raise MaterialAddressError("an exact Ingest occurrence is required")
    recorded = ledger.get(ingest_occurrence.identity)
    if recorded is None or recorded != ingest_occurrence:
        raise MaterialAddressError("the supplied Ingest occurrence is not recorded")
    source_role = ingest_occurrence.payload.get("source_role")
    if type(source_role) is not str or not source_role:
        raise MaterialAddressError("the Ingest occurrence carries no source role")
    exact = ingested_material_bytes(ingest_occurrence)
    source_span = SourceSpan(
        source_reference=ingest_occurrence.identity,
        start=0,
        end=len(exact),
    )
    exact_material = ExactMaterial(
        material_reference=ingest_occurrence.identity,
        exact_bytes_hex=exact.hex(),
        source_span=source_span,
    )
    return AddressableMaterial(
        material_representation_identity=f"material-representation:{ingest_occurrence.identity}",
        ingest_event_reference=ingest_occurrence.identity,
        exact_material=exact_material,
        source_role=source_role,
        provenance=(ingest_occurrence.identity,),
        scope=(f"locality:{ingest_occurrence.locality_identity}",),
        known_loss=tuple(ingest_occurrence.payload.get("known_loss", ())),
        unknowns=tuple(ingest_occurrence.payload.get("unknowns", ())),
        authority_limits=(
            "addressability and Locality establish no represented relation, Standing, Authority, or later Act",
        ),
    )
