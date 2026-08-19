"""One exact Witness material-acquisition occurrence."""

from __future__ import annotations

from seed_runtime.event import Event
from seed_runtime.events import CORRUPTED, EventLedger
from seed_runtime.identities import new_identity
from seed_runtime.evidence_of_yield_relation import (
    _record_evidence_of_yield_relation,
    read_requirements_of_yield_relation,
)
from seed_runtime.material_acquisition import (
    MATERIAL_RESULT_UNKNOWN,
    MaterialAcquisitionError,
    _append_exact_material_result_occurrence,
)


WITNESS_MATERIAL_ACQUISITION_RECORDED_KIND = "witness.material.acquire_recorded"
WITNESS_MATERIAL_ACQUISITION_ACT_EVIDENCE_KIND = (
    "witness.material.acquire_act_evidenced"
)
EVENT_KIND_RESPONSIBILITIES = {
    WITNESS_MATERIAL_ACQUISITION_RECORDED_KIND: "02.Acts.A",
    WITNESS_MATERIAL_ACQUISITION_ACT_EVIDENCE_KIND: "02.Acts.A",
}
WITNESS_MATERIAL_ACQUISITION_RESPONSIBILITY = (
    "preserve exact material supplied by this Witness at one source boundary"
)


class WitnessMaterialAcquisitionError(MaterialAcquisitionError):
    """One exact Witness material-acquisition occurrence is malformed."""


def record_witness_material_acquisition(
    ledger: EventLedger,
    *,
    locality_identity: str,
    exact_bytes: bytes,
    source_boundary: str,
    represented_material: str | None = None,
    known_loss: tuple[str, ...] = (),
    provenance_occurrence_references: tuple[str, ...] = (),
) -> Event:
    if type(exact_bytes) is not bytes:
        raise WitnessMaterialAcquisitionError(
            "Witness material acquisition requires exact bytes"
        )
    for name, value in (
        ("locality_identity", locality_identity),
        ("source_boundary", source_boundary),
    ):
        if type(value) is not str or not value.strip():
            raise WitnessMaterialAcquisitionError(
                f"Witness material acquisition requires exact {name}"
            )
    if represented_material is not None and type(represented_material) is not str:
        raise WitnessMaterialAcquisitionError("represented material must be exact material")
    if type(known_loss) is not tuple or any(type(item) is not str for item in known_loss):
        raise WitnessMaterialAcquisitionError("known loss must be an exact tuple of material")
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
        raise WitnessMaterialAcquisitionError(
            "provenance requires exact intact occurrence references"
        )

    material_acquisition_act_identity = new_identity("witness_material_acquisition_act")
    act_occurrence_identity = new_identity("witness_material_acquisition_act_occurrence")
    result_identity = new_identity("witness_material_acquisition_result")
    result: dict[str, object] = {
        "result_identity": result_identity,
        "material_acquisition_act_identity": material_acquisition_act_identity,
        "act_occurrence_identity": act_occurrence_identity,
        "source_role": "this Witness",
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
        WITNESS_MATERIAL_ACQUISITION_ACT_EVIDENCE_KIND,
        {
            "material_acquisition_act_identity": material_acquisition_act_identity,
            "act_occurrence_identity": act_occurrence_identity,
            "act": "Acquire exact material supplied by this Witness",
            "responsibility": WITNESS_MATERIAL_ACQUISITION_RESPONSIBILITY,
            "responsible_boundary": "this Seed",
            "authority": "unestablished",
            "evidence_scope": (
                "Evidence bounded to this exact Witness material-acquisition "
                "occurrence"
            ),
        },
        locality_identity=locality_identity,
    )
    material: dict[str, object] = {
        **result,
        "dimensions": {
            "identity": result_identity,
            "source_provenance": source_boundary,
            "responsibility": WITNESS_MATERIAL_ACQUISITION_RESPONSIBILITY,
            "authority": "unestablished",
            "evidence_scope": (
                "bounded to this exact Witness material-acquisition occurrence "
                "and exact material result; represented relation Unknown"
            ),
            "scope_locality": f"locality:{locality_identity}",
            "occurrence_preservation": (
                "exact Witness material-acquisition occurrence recorded"
            ),
        },
    }
    evidence_of_yield_relation = _record_evidence_of_yield_relation(
        ledger,
        locality_identity=locality_identity,
        exact_act="Acquire exact material supplied by this Witness",
        act_occurrence_identity=act_occurrence_identity,
        responsible_act_evidence_identity=responsible_act_evidence.identity,
        result_kind="exact material",
        result_identity=result_identity,
        result_content=result,
        responsibility=WITNESS_MATERIAL_ACQUISITION_RESPONSIBILITY,
        occurrence_boundary="witness_material_acquisition",
        responsible_boundary="this Seed",
        coordinates_of_recorded_result={key: (key,) for key in result},
        result_exact_material=exact_bytes,
    )
    return _append_exact_material_result_occurrence(
        ledger,
        result_event=Event(
            identity=ledger.allocate_event_identity(),
            kind=WITNESS_MATERIAL_ACQUISITION_RECORDED_KIND,
            material={
                **material,
                "responsible_act_evidence_identity": (
                    responsible_act_evidence.identity
                ),
                "evidence_of_yield_relation_identity": (
                    evidence_of_yield_relation.identity
                ),
            },
            exact_material=exact_bytes,
            locality_identity=locality_identity,
        ),
    )


def _read_witness_material_acquisition_result(
    ledger: EventLedger, event: Event
) -> Event:
    material = event.material
    provenance = material.get("provenance_occurrence_references")
    known_loss = material.get("known_loss")
    unknown = material.get("unknown")
    result_identity = material.get("result_identity")
    material_acquisition_act_identity = material.get("material_acquisition_act_identity")
    act_occurrence_identity = material.get("act_occurrence_identity")
    source_role = material.get("source_role")
    source_boundary = material.get("source_boundary")
    act_evidence_identity = material.get("responsible_act_evidence_identity")
    yield_identity = material.get("evidence_of_yield_relation_identity")
    act_evidence = (
        ledger.get(act_evidence_identity)
        if type(act_evidence_identity) is str
        else None
    )
    if (
        event.kind != WITNESS_MATERIAL_ACQUISITION_RECORDED_KIND
        or type(event.locality_identity) is not str
        or not event.locality_identity
        or type(event.exact_material) is not bytes
        or type(result_identity) is not str
        or not result_identity
        or type(material_acquisition_act_identity) is not str
        or not material_acquisition_act_identity
        or type(act_occurrence_identity) is not str
        or not act_occurrence_identity
        or source_role != "this Witness"
        or type(source_boundary) is not str
        or not source_boundary
        or type(known_loss) is not list
        or any(type(item) is not str for item in known_loss)
        or unknown != list(MATERIAL_RESULT_UNKNOWN)
        or type(provenance) is not list
        or len(set(provenance)) != len(provenance)
        or any(
            type(reference) is not str
            or not reference
            or ledger.get(reference) is None
            or ledger.integrity_of(reference) == CORRUPTED
            for reference in provenance
        )
        or act_evidence is None
        or act_evidence.kind != WITNESS_MATERIAL_ACQUISITION_ACT_EVIDENCE_KIND
        or act_evidence.locality_identity != event.locality_identity
        or act_evidence.exact_material is not None
        or ledger.integrity_of(act_evidence.identity) == CORRUPTED
    ):
        raise MaterialAcquisitionError(
            "Witness material-acquisition result is absent or corrupted"
        )
    result: dict[str, object] = {
        "result_identity": result_identity,
        "material_acquisition_act_identity": material_acquisition_act_identity,
        "act_occurrence_identity": act_occurrence_identity,
        "source_role": source_role,
        "source_boundary": source_boundary,
        "known_loss": known_loss,
        "unknown": unknown,
        "provenance_occurrence_references": provenance,
    }
    represented_material = material.get("represented_material")
    if represented_material is not None:
        if type(represented_material) is not str:
            raise MaterialAcquisitionError(
                "Witness material-acquisition result is absent or corrupted"
            )
        result["represented_material"] = represented_material
    expected_act_evidence = {
        "material_acquisition_act_identity": material_acquisition_act_identity,
        "act_occurrence_identity": act_occurrence_identity,
        "act": "Acquire exact material supplied by this Witness",
        "responsibility": WITNESS_MATERIAL_ACQUISITION_RESPONSIBILITY,
        "responsible_boundary": "this Seed",
        "authority": "unestablished",
        "evidence_scope": (
            "Evidence bounded to this exact Witness material-acquisition occurrence"
        ),
    }
    expected_material = {
        **result,
        "dimensions": {
            "identity": result_identity,
            "source_provenance": source_boundary,
            "responsibility": WITNESS_MATERIAL_ACQUISITION_RESPONSIBILITY,
            "authority": "unestablished",
            "evidence_scope": (
                "bounded to this exact Witness material-acquisition occurrence "
                "and exact material result; represented relation Unknown"
            ),
            "scope_locality": f"locality:{event.locality_identity}",
            "occurrence_preservation": (
                "exact Witness material-acquisition occurrence recorded"
            ),
        },
        "responsible_act_evidence_identity": act_evidence.identity,
        "evidence_of_yield_relation_identity": yield_identity,
    }
    if (
        act_evidence.material != expected_act_evidence
        or material != expected_material
    ):
        raise MaterialAcquisitionError(
            "Witness material-acquisition result is absent or corrupted"
        )
    try:
        ordered = ledger.occurrences_in_append_order(
            (act_evidence.identity, yield_identity, event.identity),
            locality_identity=event.locality_identity,
        )
        requirements = read_requirements_of_yield_relation(
            ledger,
            recorded_result_event_identity=event.identity,
            evidence_of_yield_relation_event_identity=yield_identity,
            responsible_act_evidence_event_identity=act_evidence.identity,
        )
    except (TypeError, ValueError) as error:
        raise MaterialAcquisitionError(
            "Witness material acquisition carries no intact Act and Yield"
        ) from error
    if [occurrence.identity for occurrence in ordered] != [
        act_evidence.identity,
        yield_identity,
        event.identity,
    ] or not all(requirements.values()):
        raise MaterialAcquisitionError(
            "Witness material acquisition carries no intact Act and Yield"
        )
    return event
