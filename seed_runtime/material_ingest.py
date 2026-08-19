"""One exact Ingest occurrence for material supplied at a source boundary."""

from __future__ import annotations

from seed_runtime.event import Event
from seed_runtime.events import CORRUPTED, EventLedger, EventLedgerBoundary
from seed_runtime.identities import new_identity
from seed_runtime.evidence_of_yield_relation import (
    _record_evidence_of_yield_relation,
    read_requirements_of_yield_relation,
)


MATERIAL_INGEST_OCCURRED_KIND = "material.ingest.occurred"
MATERIAL_INGEST_ACT_EVIDENCE_KIND = "material.ingest.act_evidenced"
EVENT_KIND_RESPONSIBILITIES = {
    MATERIAL_INGEST_OCCURRED_KIND: "02.Acts.A",
    MATERIAL_INGEST_ACT_EVIDENCE_KIND: "02.Acts.A",
}
MATERIAL_INGEST_RESPONSIBILITY = (
    "preserve exact material supplied at one source boundary"
)
MATERIAL_RESULT_UNKNOWN = ("represented_relation", "source_relation")


class MaterialIngestError(ValueError):
    pass


def record_exact_ingest_result(
    ledger: EventLedger,
    *,
    result_event: Event,
    responsible_act_evidence_identity: str,
    evidence_of_yield_relation_identity: str,
) -> Event:
    """Record one exact bounded material result after its family-local Yield."""

    if not isinstance(ledger, EventLedger):
        raise TypeError("exact Ingest result requires one EventLedger")
    if (
        type(result_event) is not Event
        or type(result_event.exact_material) is not bytes
        or type(result_event.locality_identity) is not str
        or not result_event.locality_identity
        or type(responsible_act_evidence_identity) is not str
        or not responsible_act_evidence_identity
        or type(evidence_of_yield_relation_identity) is not str
        or not evidence_of_yield_relation_identity
        or "responsible_act_evidence_identity" in result_event.material
        or "evidence_of_yield_relation_identity" in result_event.material
    ):
        raise MaterialIngestError("exact Ingest result occurrence required")
    return ledger.append_many(
        (
            Event(
                identity=result_event.identity,
                kind=result_event.kind,
                material={
                    **result_event.material,
                    "responsible_act_evidence_identity": (
                        responsible_act_evidence_identity
                    ),
                    "evidence_of_yield_relation_identity": (
                        evidence_of_yield_relation_identity
                    ),
                },
                exact_material=result_event.exact_material,
                locality_identity=result_event.locality_identity,
            ),
        )
    )[0]


def ingest_material(
    ledger: EventLedger,
    *,
    locality_identity: str,
    exact_bytes: bytes,
    source_role: str,
    source_boundary: str,
    represented_material: str | None = None,
    known_loss: tuple[str, ...] = (),
    provenance_occurrence_references: tuple[str, ...] = (),
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
    if (
        type(provenance_occurrence_references) is not tuple
        or len(set(provenance_occurrence_references))
        != len(provenance_occurrence_references)
        or any(
            type(reference) is not str
            or not reference
            or ledger.get(reference) is None
            or ledger.integrity_of(reference) == CORRUPTED
            for reference in provenance_occurrence_references
        )
    ):
        raise MaterialIngestError(
            "provenance requires exact intact occurrence references"
        )

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
        "unknown": list(MATERIAL_RESULT_UNKNOWN),
        "provenance_occurrence_references": list(
            provenance_occurrence_references
        ),
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
            "evidence_scope": "Evidence bounded to this exact Ingest occurrence",
        },
        locality_identity=locality_identity,
    )
    material: dict[str, object] = {
        **result,
        "dimensions": {
            "identity": result_identity,
            "source_provenance": source_boundary,
            "responsibility": MATERIAL_INGEST_RESPONSIBILITY,
            "authority": "unestablished",
            "evidence_scope": (
                "bounded to this exact Ingest occurrence and exact material result; "
                "represented relation Unknown"
            ),
            "scope_locality": f"locality:{locality_identity}",
            "occurrence_preservation": "exact Ingest material occurrence recorded",
        },
    }
    evidence_of_yield_relation = _record_evidence_of_yield_relation(
        ledger,
        locality_identity=locality_identity,
        exact_act="Ingest exact material",
        act_occurrence_identity=act_occurrence_identity,
        responsible_act_evidence_identity=responsible_act_evidence.identity,
        result_kind="exact material",
        result_identity=result_identity,
        result_content=result,
        responsibility=MATERIAL_INGEST_RESPONSIBILITY,
        occurrence_boundary="material_ingest",
        responsible_boundary="this Seed",
        coordinates_of_recorded_result={key: (key,) for key in result},
        result_exact_material=exact_bytes,
    )
    return record_exact_ingest_result(
        ledger,
        result_event=Event(
            identity=ledger.allocate_event_identity(),
            kind=MATERIAL_INGEST_OCCURRED_KIND,
            material=material,
            exact_material=exact_bytes,
            locality_identity=locality_identity,
        ),
        responsible_act_evidence_identity=responsible_act_evidence.identity,
        evidence_of_yield_relation_identity=evidence_of_yield_relation.identity,
    )


def ingested_material_bytes(event: Event) -> bytes:
    if not is_exact_ingest_result(event):
        raise MaterialIngestError(
            f"only Ingest occurrences carry exact material: {event.kind}"
        )
    exact = event.exact_material
    if type(exact) is not bytes:
        raise MaterialIngestError("Ingest occurrence carries no exact bytes")
    return exact


def is_exact_ingest_result(event: Event) -> bool:
    """Recognize the bounded generic or operator-specific Ingest result."""

    if type(event) is not Event:
        return False
    if event.kind == MATERIAL_INGEST_OCCURRED_KIND:
        return True
    from seed_runtime.operator_material_acquisition import (
        OPERATOR_MATERIAL_ACQUIRE_RECORDED_KIND,
    )

    return event.kind == OPERATOR_MATERIAL_ACQUIRE_RECORDED_KIND


def iter_exact_ingest_results(
    ledger: EventLedger,
    locality_identity: str,
    *,
    through: EventLedgerBoundary | None = None,
):
    """Yield every exact generic or source-specific Ingest result in order."""

    for event in ledger.list_locality(locality_identity, through=through):
        if is_exact_ingest_result(event):
            yield event


def read_exact_ingest_result(ledger: EventLedger, event_identity: str) -> Event:
    """Read one intact exact-material Ingest result through its Yield."""

    if not isinstance(ledger, EventLedger):
        raise TypeError("exact Ingest read requires one EventLedger")
    if type(event_identity) is not str or not event_identity:
        raise MaterialIngestError("exact Ingest read requires one occurrence identity")
    event = ledger.get(event_identity)
    if (
        event is None
        or not is_exact_ingest_result(event)
        or type(event.locality_identity) is not str
        or not event.locality_identity
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise MaterialIngestError("exact Ingest result is absent or corrupted")
    try:
        requirements = read_requirements_of_yield_relation(
            ledger,
            recorded_result_event_identity=event.identity,
            evidence_of_yield_relation_event_identity=event.material.get(
                "evidence_of_yield_relation_identity"
            ),
            responsible_act_evidence_event_identity=event.material.get(
                "responsible_act_evidence_identity"
            ),
        )
        ingested_material_bytes(event)
    except (TypeError, ValueError) as error:
        raise MaterialIngestError(
            "exact Ingest result carries no intact Act and Yield"
        ) from error
    if not all(requirements.values()):
        raise MaterialIngestError(
            "exact Ingest result carries no intact Act and Yield"
        )
    return event
