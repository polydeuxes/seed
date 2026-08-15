"""One exact Ingest occurrence for material supplied at a source boundary."""

from __future__ import annotations

from seed_runtime.event import Event
from seed_runtime.events import EventLedger
from seed_runtime.identities import new_identity
from seed_runtime.yield_evidence import _record_yield_evidence


MATERIAL_INGEST_OCCURRED_KIND = "material.ingest.occurred"
MATERIAL_INGEST_ACT_EVIDENCE_KIND = "material.ingest.act_evidenced"
EVENT_KIND_RESPONSIBILITIES = {
    MATERIAL_INGEST_OCCURRED_KIND: "02.Acts.A",
    MATERIAL_INGEST_ACT_EVIDENCE_KIND: "02.Acts.A",
}
MATERIAL_INGEST_RESPONSIBILITY = (
    "preserve exact material supplied at one source boundary"
)


class MaterialIngestError(ValueError):
    pass


def ingest_material(
    ledger: EventLedger,
    *,
    locality_identity: str,
    exact_bytes: bytes,
    source_role: str,
    source_boundary: str,
    represented_material: str | None = None,
    known_loss: tuple[str, ...] = (),
) -> Event:
    if type(exact_bytes) is not bytes:
        raise MaterialIngestError("Ingest requires exact bytes")
    for name, value in (
        ("locality_identity", locality_identity),
        ("source_role", source_role),
        ("source_boundary", source_boundary),
    ):
        if type(value) is not str or not value.strip():
            raise MaterialIngestError(f"Ingest requires exact {name}")
    if represented_material is not None and type(represented_material) is not str:
        raise MaterialIngestError("represented material must be exact material")
    if type(known_loss) is not tuple or any(type(item) is not str for item in known_loss):
        raise MaterialIngestError("known loss must be an exact tuple of material")

    ingest_act_identity = new_identity("material_ingest_act")
    act_occurrence_identity = new_identity("material_ingest_act_occurrence")
    result_identity = new_identity("material_ingest_result")
    result: dict[str, object] = {
        "result_identity": result_identity,
        "ingest_act_identity": ingest_act_identity,
        "act_occurrence_identity": act_occurrence_identity,
        "source_role": source_role,
        "source_boundary": source_boundary,
        "known_loss": list(known_loss),
        "unknowns": [
            "what this material represents remains Unknown",
            "the asserted source relation remains Unknown",
        ],
        "provenance_occurrence_references": [],
    }
    if represented_material is not None:
        result["represented_material"] = represented_material

    responsible_act_evidence = ledger.append(
        MATERIAL_INGEST_ACT_EVIDENCE_KIND,
        {
            "ingest_act_identity": ingest_act_identity,
            "act_occurrence_identity": act_occurrence_identity,
            "act": "Ingest exact material",
            "responsibility": MATERIAL_INGEST_RESPONSIBILITY,
            "responsible_boundary": "this Seed",
            "authority": "unestablished",
            "evidence_scope": "Evidence concerning this exact Ingest occurrence only",
        },
        locality_identity=locality_identity,
    )
    yield_evidence = _record_yield_evidence(
        ledger,
        locality_identity=locality_identity,
        exact_act="Ingest exact material",
        act_occurrence_identity=act_occurrence_identity,
        result_kind="exact material",
        result_identity=result_identity,
        result_content=result,
        responsibility=MATERIAL_INGEST_RESPONSIBILITY,
        live_boundary="material_ingest",
        responsible_boundary="this Seed",
        recorded_result_coordinates={key: (key,) for key in result},
        result_exact_material=exact_bytes,
    )
    material: dict[str, object] = {
        **result,
        "dimensions": {
            "identity": result_identity,
            "content": result_identity,
            "source_provenance": source_boundary,
            "responsibility": MATERIAL_INGEST_RESPONSIBILITY,
            "authority": "unestablished",
            "evidence_scope": (
                "this exact Ingest occurrence and exact material result only; "
                "represented relation Unknown"
            ),
            "scope_locality": f"locality:{locality_identity}",
            "occurrence_preservation": "exact Ingest bytes durably recorded",
        },
        "responsible_act_evidence_identity": responsible_act_evidence.identity,
        "yield_evidence_identity": yield_evidence.identity,
    }

    return ledger.append(
        MATERIAL_INGEST_OCCURRED_KIND,
        material,
        exact_material=exact_bytes,
        locality_identity=locality_identity,
    )


def ingested_material_bytes(event: Event) -> bytes:
    if event.kind != MATERIAL_INGEST_OCCURRED_KIND:
        raise MaterialIngestError(
            f"only Ingest occurrences carry exact material: {event.kind}"
        )
    exact = event.exact_material
    if type(exact) is not bytes:
        raise MaterialIngestError("Ingest occurrence carries no exact bytes")
    return exact
