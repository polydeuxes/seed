"""One operator interaction entering the shared Ingest boundary."""

from __future__ import annotations

from seed_runtime.events import EventLedger
from seed_runtime.material_ingest import (
    MATERIAL_INGEST_OCCURRED_KIND,
    ingest_material,
)
from seed_runtime.operator_material_boundary import OperatorBoundaryMaterial
from seed_runtime.operator_material_acquisition import (
    get_recorded_operator_material_acquire,
)


def update_operator_ingest_standing(attempts, event) -> None:
    if (
        event.kind != MATERIAL_INGEST_OCCURRED_KIND
        or event.material.get("source_role") != "operator"
    ):
        return
    dimensions = event.material.get("dimensions")
    if not isinstance(dimensions, dict):
        raise ValueError("operator Ingest occurrence carries no dimensions")
    occurrence_identity = dimensions.get("identity")
    if type(occurrence_identity) is not str or not occurrence_identity:
        raise ValueError("operator Ingest occurrence carries no exact identity")
    standing = attempts.setdefault(
        occurrence_identity,
        {
            "dimensional_standing": {},
            "current_standing": {"ingest_occurrence": None},
            "known_loss": [],
            "unknown": [],
            "conflicts": [],
        },
    )
    standing["dimensional_standing"][event.identity] = {
        "event_kind": event.kind,
        "subject_reference": occurrence_identity,
        "dimensions": dimensions,
        "provenance_occurrence_references": list(
            event.material.get("provenance_occurrence_references", ())
        ),
    }
    standing["current_standing"]["ingest_occurrence"] = {
        "subject_reference": occurrence_identity,
        "dimensions": dimensions,
        "evidence_event_identity": event.identity,
    }
    standing["last_event_kind"] = event.kind
    for key in ("known_loss", "unknown", "conflicts"):
        for value in event.material.get(key, ()):
            if value not in standing[key]:
                standing[key].append(value)


def _ingest_standing(*, event):
    attempts: dict[str, dict] = {}
    update_operator_ingest_standing(attempts, event)
    occurrence_identity = event.material["dimensions"]["identity"]
    return attempts[occurrence_identity]


def run_operator_ingest(
    *,
    ledger: EventLedger,
    locality_identity: str,
    boundary_material: OperatorBoundaryMaterial,
    locality_standing: dict[str, object] | None = None,
    supplied_material_representation: str | None = None,
    operator_material_occurrence_reference: str | None = None,
) -> dict[str, object]:
    if boundary_material.eof:
        raise ValueError("operator boundary material must be non-EOF")
    provenance_occurrence_references: tuple[str, ...] = ()
    if operator_material_occurrence_reference is not None:
        acquired = get_recorded_operator_material_acquire(
            ledger, operator_material_occurrence_reference
        )
        acquired_event = ledger.get(operator_material_occurrence_reference)
        if (
            acquired_event is None
            or acquired_event.locality_identity != locality_identity
            or acquired_event.exact_material != boundary_material.exact_bytes
            or acquired["source_boundary"] != boundary_material.material_boundary
            or acquired["known_loss"] != list(boundary_material.known_loss)
        ):
            raise ValueError(
                "operator Ingest requires its exact acquired material occurrence"
            )
        provenance_occurrence_references = (
            operator_material_occurrence_reference,
        )
    event = ingest_material(
        ledger,
        locality_identity=locality_identity,
        exact_bytes=boundary_material.exact_bytes,
        source_role="operator",
        source_boundary=boundary_material.material_boundary,
        represented_material=supplied_material_representation,
        known_loss=boundary_material.known_loss,
        provenance_occurrence_references=provenance_occurrence_references,
    )
    standing = _ingest_standing(event=event)
    if locality_standing is not None:
        standing["locality_standing"] = locality_standing
    return standing
