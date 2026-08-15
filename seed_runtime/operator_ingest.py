"""One operator interaction entering the shared Ingest boundary."""

from __future__ import annotations

from seed_runtime.addressable_material import address_ingested_material
from seed_runtime.events import EventLedger
from seed_runtime.material_ingest import (
    MATERIAL_INGEST_OCCURRED_KIND,
    ingest_material,
)
from seed_runtime.operator_material_boundary import OperatorBoundaryMaterial


def update_operator_ingest_standing(attempts, event, *, ledger=None) -> None:
    if (
        event.kind != MATERIAL_INGEST_OCCURRED_KIND
        or event.payload.get("source_role") != "operator"
    ):
        return
    dimensions = event.payload.get("dimensions")
    if not isinstance(dimensions, dict):
        raise ValueError("operator Ingest occurrence carries no dimensions")
    occurrence_id = dimensions.get("identity")
    if type(occurrence_id) is not str or not occurrence_id:
        raise ValueError("operator Ingest occurrence carries no exact identity")
    standing = attempts.setdefault(
        occurrence_id,
        {
            "event_ids": [],
            "dimensional_standing": {},
            "current_standing": {"ingest_occurrence": None},
            "known_loss": [],
            "unknowns": [],
            "conflicts": [],
        },
    )
    standing["event_ids"].append(event.id)
    standing["dimensional_standing"][event.id] = {
        "event_kind": event.kind,
        "subject_ref": occurrence_id,
        "dimensions": dimensions,
        "provenance_occurrence_refs": list(
            event.payload.get("provenance_occurrence_refs", ())
        ),
    }
    standing["current_standing"]["ingest_occurrence"] = {
        "subject_ref": occurrence_id,
        "dimensions": dimensions,
        "evidence_event_id": event.id,
    }
    if ledger is not None:
        standing["addressable_material"] = address_ingested_material(
            ingest_occurrence=event,
            ledger=ledger,
        ).to_json_dict()
    standing["last_event_kind"] = event.kind
    for key in ("known_loss", "unknowns", "conflicts"):
        standing[key] = sorted(
            set((*standing[key], *event.payload.get(key, ())))
        )


def _ingest_standing(*, event, ledger):
    attempts: dict[str, dict] = {}
    update_operator_ingest_standing(attempts, event, ledger=ledger)
    occurrence_id = event.payload["dimensions"]["identity"]
    return attempts[occurrence_id]


def run_operator_ingest(
    *,
    ledger: EventLedger,
    locality_id: str,
    boundary_material: OperatorBoundaryMaterial,
    locality_standing: dict[str, object] | None = None,
    supplied_material_representation: str | None = None,
) -> dict[str, object]:
    if boundary_material.eof:
        raise ValueError("operator boundary material must be non-EOF")
    event = ingest_material(
        ledger,
        locality_id=locality_id,
        exact_bytes=boundary_material.exact_bytes,
        source_role="operator",
        source_boundary=boundary_material.material_boundary,
        represented_material=supplied_material_representation,
        known_loss=boundary_material.known_loss,
    )
    standing = _ingest_standing(event=event, ledger=ledger)
    if locality_standing is not None:
        standing["locality_standing"] = locality_standing
    return standing
