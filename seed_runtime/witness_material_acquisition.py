"""One exact Witness material-acquisition occurrence."""

from __future__ import annotations

from seed_runtime.event import Event
from seed_runtime.events import CORRUPTED, EventLedger
from seed_runtime.identities import new_identity
from seed_runtime.yield_relation import (
    _record_yield_relation,
    read_requirements_of_yield_relation,
)
from seed_runtime.material_acquisition import (
    MATERIAL_RESULT_UNKNOWN,
    MaterialAcquisitionError,
    _append_exact_material_result_occurrence,
)


WITNESS_MATERIAL_ACQUISITION_RECORDED_KIND = "witness.material.acquire_recorded"
WITNESS_MATERIAL_ACQUISITION_ACT_OCCURRENCE_EVENT = (
    "witness.material.acquire_act_occurrence_recorded"
)
EVENT_KIND_RESPONSIBILITIES = {
    WITNESS_MATERIAL_ACQUISITION_RECORDED_KIND: "02.Acts.A",
    WITNESS_MATERIAL_ACQUISITION_ACT_OCCURRENCE_EVENT: "02.Acts.A",
}
WITNESS_MATERIAL_ACQUISITION_RESPONSIBILITY = (
    "preserve exact material supplied by this Witness at one source boundary"
)


class WitnessMaterialAcquisitionError(MaterialAcquisitionError):
    """One exact Witness material-acquisition occurrence is malformed."""


def _require_read_occurrence_coordinates(
    exact_bytes: bytes, read_occurrences: tuple[object, ...] | list[object]
) -> None:
    """Validate exact mechanical read coordinates carried by one result."""

    if type(read_occurrences) not in (tuple, list):
        raise WitnessMaterialAcquisitionError(
            "exact read occurrence population required"
        )
    next_start = 0
    boundaries: set[str] = set()
    invocation_positions: set[int] = set()
    for occurrence in read_occurrences:
        if type(occurrence) is not dict:
            raise WitnessMaterialAcquisitionError(
                "read occurrences require exact coordinates"
            )
        source = occurrence.get("source_boundary")
        invocation_position = occurrence.get("invocation_position")
        start = occurrence.get("start_position")
        end = occurrence.get("end_position")
        if (
            set(occurrence)
            != {
                "source_boundary",
                "invocation_position",
                "start_position",
                "end_position",
            }
            or type(source) is not str
            or not source
            or source in boundaries
            or type(invocation_position) is not int
            or invocation_position < 0
            or invocation_position in invocation_positions
            or type(start) is not int
            or type(end) is not int
            or start != next_start
            or end <= start
            or end > len(exact_bytes)
        ):
            raise WitnessMaterialAcquisitionError(
                "read occurrences require exact coordinates"
            )
        boundaries.add(source)
        invocation_positions.add(invocation_position)
        next_start = end
    if read_occurrences and next_start != len(exact_bytes):
        raise WitnessMaterialAcquisitionError(
            "read occurrences require the complete exact material"
        )


def record_witness_material_acquisition(
    ledger: EventLedger,
    *,
    locality_identity: str,
    exact_bytes: bytes,
    source_boundary: str,
    known_loss: tuple[str, ...] = (),
    provenance_occurrence_references: tuple[str, ...] = (),
    read_occurrences: tuple[dict[str, object], ...] = (),
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
    _require_read_occurrence_coordinates(exact_bytes, read_occurrences)

    material_acquisition_act_identity = new_identity("witness_material_acquisition_act")
    act_occurrence_identity = new_identity("witness_material_acquisition_act_occurrence")
    result_identity = new_identity("witness_material_acquisition_result")
    recorded_result_event_identity = ledger.allocate_event_identity()
    locality_relation = {
        "first_subject": {
            "recorded_occurrence_identity": recorded_result_event_identity,
            "coordinate": "exact_material",
        },
        "relation": "locality",
        "second_subject": "this Seed",
        "relation_occurrence_identity": recorded_result_event_identity,
    }
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
        "locality_relation": locality_relation,
    }
    if read_occurrences:
        result["read_occurrences"] = [
            dict(occurrence) for occurrence in read_occurrences
        ]
    act_occurrence = ledger.append(
        WITNESS_MATERIAL_ACQUISITION_ACT_OCCURRENCE_EVENT,
        {
            "material_acquisition_act_identity": material_acquisition_act_identity,
            "act_occurrence_identity": act_occurrence_identity,
            "act": "Exact material acquisition from this Witness",
            "responsibility": WITNESS_MATERIAL_ACQUISITION_RESPONSIBILITY,
            "responsible_boundary": "this Seed",
        },
        locality_identity=locality_identity,
    )
    material: dict[str, object] = {
        **result,
        "dimensions": {
            "identity": result_identity,
            "source_provenance": source_boundary,
            "responsibility": WITNESS_MATERIAL_ACQUISITION_RESPONSIBILITY,
            "scope_locality": f"locality:{locality_identity}",
            "occurrence_preservation": (
                "exact Witness material-acquisition occurrence recorded"
            ),
        },
    }
    yield_relation = _record_yield_relation(
        ledger,
        locality_identity=locality_identity,
        exact_act="Exact material acquisition from this Witness",
        act_occurrence_identity=act_occurrence_identity,
        act_occurrence_event_identity=act_occurrence.identity,
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
            identity=recorded_result_event_identity,
            kind=WITNESS_MATERIAL_ACQUISITION_RECORDED_KIND,
            material={
                **material,
                "act_occurrence_event_identity": (
                    act_occurrence.identity
                ),
                "yield_relation_identity": (
                    yield_relation.identity
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
    read_occurrences = material.get("read_occurrences", [])
    known_loss = material.get("known_loss")
    unknown = material.get("unknown")
    result_identity = material.get("result_identity")
    material_acquisition_act_identity = material.get("material_acquisition_act_identity")
    act_occurrence_identity = material.get("act_occurrence_identity")
    act_occurrence_event_identity = material.get("act_occurrence_event_identity")
    source_role = material.get("source_role")
    source_boundary = material.get("source_boundary")
    yield_identity = material.get("yield_relation_identity")
    locality_relation = material.get("locality_relation")
    act_occurrence = (
        ledger.get(act_occurrence_event_identity)
        if type(act_occurrence_event_identity) is str
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
        or type(read_occurrences) is not list
        or act_occurrence is None
        or act_occurrence.kind != WITNESS_MATERIAL_ACQUISITION_ACT_OCCURRENCE_EVENT
        or act_occurrence.locality_identity != event.locality_identity
        or act_occurrence.exact_material is not None
        or ledger.integrity_of(act_occurrence.identity) == CORRUPTED
        or locality_relation
        != {
            "first_subject": {
                "recorded_occurrence_identity": event.identity,
                "coordinate": "exact_material",
            },
            "relation": "locality",
            "second_subject": "this Seed",
            "relation_occurrence_identity": event.identity,
        }
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
        "locality_relation": locality_relation,
    }
    if read_occurrences:
        result["read_occurrences"] = read_occurrences
    expected_act_occurrence = {
        "material_acquisition_act_identity": material_acquisition_act_identity,
        "act_occurrence_identity": act_occurrence_identity,
        "act": "Exact material acquisition from this Witness",
        "responsibility": WITNESS_MATERIAL_ACQUISITION_RESPONSIBILITY,
        "responsible_boundary": "this Seed",
    }
    expected_material = {
        **result,
        "dimensions": {
            "identity": result_identity,
            "source_provenance": source_boundary,
            "responsibility": WITNESS_MATERIAL_ACQUISITION_RESPONSIBILITY,
            "scope_locality": f"locality:{event.locality_identity}",
            "occurrence_preservation": (
                "exact Witness material-acquisition occurrence recorded"
            ),
        },
        "act_occurrence_event_identity": act_occurrence.identity,
        "yield_relation_identity": yield_identity,
    }
    if (
        act_occurrence.material != expected_act_occurrence
        or material != expected_material
    ):
        raise MaterialAcquisitionError(
            "Witness material-acquisition result is absent or corrupted"
        )
    try:
        _require_read_occurrence_coordinates(
            event.exact_material, read_occurrences
        )
    except WitnessMaterialAcquisitionError as error:
        raise MaterialAcquisitionError(
            "Witness material acquisition carries malformed read occurrences"
        ) from error
    try:
        ordered = ledger.occurrences_in_append_order(
            (act_occurrence.identity, yield_identity, event.identity),
            locality_identity=event.locality_identity,
        )
        requirements = read_requirements_of_yield_relation(
            ledger,
            recorded_result_event_identity=event.identity,
            yield_relation_event_identity=yield_identity,
            act_occurrence_event_identity=act_occurrence.identity,
        )
    except (TypeError, ValueError) as error:
        raise MaterialAcquisitionError(
            "Witness material acquisition carries no intact Act and Yield"
        ) from error
    if [occurrence.identity for occurrence in ordered] != [
        act_occurrence.identity,
        yield_identity,
        event.identity,
    ] or not all(requirements.values()):
        raise MaterialAcquisitionError(
            "Witness material acquisition carries no intact Act and Yield"
        )
    return event


def read_witness_material_acquire_locality_relation_requirements(
    ledger: EventLedger,
    *,
    recorded_result_event_identity: str,
) -> dict[str, bool]:
    """Read the material-to-this-Seed Locality relation from its acquisition."""

    event = ledger.get(recorded_result_event_identity)
    if event is None or event.kind != WITNESS_MATERIAL_ACQUISITION_RECORDED_KIND:
        return {
            "exact_relation": False,
            "relation_occurrence": False,
            "responsible_acquisition": False,
        }
    try:
        _read_witness_material_acquisition_result(ledger, event)
    except (TypeError, ValueError):
        return {
            "exact_relation": False,
            "relation_occurrence": False,
            "responsible_acquisition": False,
        }
    relation = event.material.get("locality_relation")
    return {
        "exact_relation": bool(
            type(relation) is dict
            and relation.get("first_subject")
            == {
                "recorded_occurrence_identity": event.identity,
                "coordinate": "exact_material",
            }
            and relation.get("relation") == "locality"
            and relation.get("second_subject") == "this Seed"
            and type(event.exact_material) is bytes
        ),
        "relation_occurrence": bool(
            type(relation) is dict
            and relation.get("relation_occurrence_identity") == event.identity
        ),
        "responsible_acquisition": ledger.integrity_of(event.identity) != CORRUPTED,
    }
