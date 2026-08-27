"""One exact Witness source occurrence and its material result."""

from __future__ import annotations

from copy import deepcopy

from seed_runtime.event import Event
from seed_runtime.events import CORRUPTED, EventLedger
from seed_runtime.yield_relation import (
    _record_yield_relation,
    read_requirements_of_yield_relation,
)
from seed_runtime.material_source import (
    MaterialSourceError,
    _append_exact_material_result_occurrence,
)


WITNESS_MATERIAL_SOURCE_SUBJECT_TO_ACT_BINDING_RECORDED_KIND = (
    "witness.material.source_subject_to_act_binding_recorded"
)
WITNESS_MATERIAL_SOURCE_RECORDED_KIND = "witness.material.source_result_recorded"
WITNESS_MATERIAL_SOURCE_ACT_OCCURRENCE_EVENT = (
    "witness.material.source_act_occurrence_recorded"
)
EVENT_KIND_BOOK_CLAUSES = {
    WITNESS_MATERIAL_SOURCE_SUBJECT_TO_ACT_BINDING_RECORDED_KIND: "01.Source.H",
    WITNESS_MATERIAL_SOURCE_RECORDED_KIND: "02.Acts.A",
    WITNESS_MATERIAL_SOURCE_ACT_OCCURRENCE_EVENT: "02.Acts.A",
}
WITNESS_MATERIAL_SOURCE_ACT = "Preserve exact material supplied by this Witness"


class WitnessMaterialSourceError(MaterialSourceError):
    """One exact Witness material source occurrence is malformed."""


def _subject_to_act_binding_reference(binding: Event) -> dict[str, object]:
    return {
        "recorded_occurrence_identity": binding.identity,
        "book_clause_identity": binding.material["book_clause_identity"],
        "exact_act_identity": binding.material["exact_act_identity"],
        "subject_reference": deepcopy(binding.material["subject_reference"]),
    }


def _subject_to_act_binding_material(
    *,
    source_boundary: str,
    exact_act_identity: str,
    act_occurrence_identity: str,
    result_identity: str,
) -> dict[str, object]:
    return {
        "book_clause_identity": "01.Source.H",
        "subject_reference": {
            "source_boundary": source_boundary,
        },
        "act": WITNESS_MATERIAL_SOURCE_ACT,
        "exact_act_identity": exact_act_identity,
        "act_occurrence_identity": act_occurrence_identity,
        "result_identity": result_identity,
    }


def _require_read_occurrence_coordinates(
    exact_bytes: bytes, read_occurrences: tuple[object, ...] | list[object]
) -> None:
    """Validate exact mechanical read coordinates carried by one result."""

    if type(read_occurrences) not in (tuple, list):
        raise WitnessMaterialSourceError(
            "exact read occurrence population required"
        )
    next_start = 0
    boundaries: set[str] = set()
    invocation_positions: set[int] = set()
    for occurrence in read_occurrences:
        if type(occurrence) is not dict:
            raise WitnessMaterialSourceError(
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
            raise WitnessMaterialSourceError(
                "read occurrences require exact coordinates"
            )
        boundaries.add(source)
        invocation_positions.add(invocation_position)
        next_start = end
    if read_occurrences and next_start != len(exact_bytes):
        raise WitnessMaterialSourceError(
            "read occurrences require the complete exact material"
        )


def record_witness_material_source(
    ledger: EventLedger,
    *,
    locality_identity: str,
    exact_bytes: bytes,
    source_boundary: str,
    time_boundary_reached: bool | None = None,
    output_byte_count_boundary_reached: bool | None = None,
    error_byte_count_boundary_reached: bool | None = None,
    source_occurrence_references: tuple[str, ...] = (),
    read_occurrences: tuple[dict[str, object], ...] = (),
) -> Event:
    if type(exact_bytes) is not bytes:
        raise WitnessMaterialSourceError(
            "Witness source material requires exact bytes"
        )
    for name, value in (
        ("locality_identity", locality_identity),
        ("source_boundary", source_boundary),
    ):
        if type(value) is not str or not value.strip():
            raise WitnessMaterialSourceError(
                f"Witness material source requires exact {name}"
            )
    boundary_outcomes = {
        "time_boundary_reached": time_boundary_reached,
        "output_byte_count_boundary_reached": output_byte_count_boundary_reached,
        "error_byte_count_boundary_reached": error_byte_count_boundary_reached,
    }
    if any(
        value is not None and type(value) is not bool
        for value in boundary_outcomes.values()
    ):
        raise WitnessMaterialSourceError(
            "invocation boundary outcomes must be exact booleans"
        )
    if (
        type(source_occurrence_references) is not tuple
        or len(set(source_occurrence_references))
        != len(source_occurrence_references)
        or any(
            type(reference) is not str
            or not reference
            or ledger.get(reference) is None
            or ledger.integrity_of(reference) == CORRUPTED
            for reference in source_occurrence_references
        )
    ):
        raise WitnessMaterialSourceError(
            "source requires exact intact occurrence references"
        )
    _require_read_occurrence_coordinates(exact_bytes, read_occurrences)

    source_act_identity = ledger.mint_identity("witness_material_source_act")
    act_occurrence_identity = ledger.mint_identity(
        "witness_material_source_act_occurrence"
    )
    result_identity = ledger.mint_identity("witness_material_source_result")
    subject_to_act_binding = ledger.append(
        WITNESS_MATERIAL_SOURCE_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
        _subject_to_act_binding_material(
            source_boundary=source_boundary,
            exact_act_identity=source_act_identity,
            act_occurrence_identity=act_occurrence_identity,
            result_identity=result_identity,
        ),
        locality_identity=locality_identity,
    )
    binding_reference = _subject_to_act_binding_reference(
        subject_to_act_binding
    )
    recorded_result_event_identity = ledger.allocate_event_identity()
    result: dict[str, object] = {
        "result_identity": result_identity,
        "exact_act_identity": source_act_identity,
        "act_occurrence_identity": act_occurrence_identity,
        "source_boundary": source_boundary,
        "subject_to_act_binding_reference": binding_reference,
        "source_occurrence_references": list(
            source_occurrence_references
        ),
    }
    result.update(
        {
            name: value
            for name, value in boundary_outcomes.items()
            if value is not None
        }
    )
    if read_occurrences:
        result["read_occurrences"] = [
            dict(occurrence) for occurrence in read_occurrences
        ]
    act_occurrence = ledger.append(
        WITNESS_MATERIAL_SOURCE_ACT_OCCURRENCE_EVENT,
        {
            "exact_act_identity": source_act_identity,
            "act_occurrence_identity": act_occurrence_identity,
            "act": WITNESS_MATERIAL_SOURCE_ACT,
            "subject_to_act_binding_reference": binding_reference,
        },
        locality_identity=locality_identity,
    )
    material: dict[str, object] = {**result}
    yield_relation = _record_yield_relation(
        ledger,
        locality_identity=locality_identity,
        exact_act=WITNESS_MATERIAL_SOURCE_ACT,
        act_occurrence_identity=act_occurrence_identity,
        act_occurrence_event_identity=act_occurrence.identity,
        result_kind="exact material",
        result_identity=result_identity,
        result_content=result,
        occurrence_boundary="witness_material_source",
        coordinates_of_recorded_result={key: (key,) for key in result},
        result_exact_material=exact_bytes,
    )
    return _append_exact_material_result_occurrence(
        ledger,
        result_event=Event(
            identity=recorded_result_event_identity,
            kind=WITNESS_MATERIAL_SOURCE_RECORDED_KIND,
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


def _read_witness_material_source_result(
    ledger: EventLedger, event: Event
) -> Event:
    material = event.material
    source_references = material.get("source_occurrence_references")
    read_occurrences = material.get("read_occurrences", [])
    result_identity = material.get("result_identity")
    source_act_identity = material.get("exact_act_identity")
    act_occurrence_identity = material.get("act_occurrence_identity")
    act_occurrence_event_identity = material.get("act_occurrence_event_identity")
    source_boundary = material.get("source_boundary")
    binding_reference = material.get("subject_to_act_binding_reference")
    yield_identity = material.get("yield_relation_identity")
    boundary_outcomes = {
        name: material[name]
        for name in (
            "time_boundary_reached",
            "output_byte_count_boundary_reached",
            "error_byte_count_boundary_reached",
        )
        if name in material
    }
    act_occurrence = (
        ledger.get(act_occurrence_event_identity)
        if type(act_occurrence_event_identity) is str
        else None
    )
    binding = (
        ledger.get(binding_reference.get("recorded_occurrence_identity"))
        if type(binding_reference) is dict
        else None
    )
    if (
        event.kind != WITNESS_MATERIAL_SOURCE_RECORDED_KIND
        or type(event.locality_identity) is not str
        or not event.locality_identity
        or type(event.exact_material) is not bytes
        or type(result_identity) is not str
        or not result_identity
        or type(source_act_identity) is not str
        or not source_act_identity
        or type(act_occurrence_identity) is not str
        or not act_occurrence_identity
        or type(source_boundary) is not str
        or not source_boundary
        or binding is None
        or binding.kind
        != WITNESS_MATERIAL_SOURCE_SUBJECT_TO_ACT_BINDING_RECORDED_KIND
        or binding.locality_identity != event.locality_identity
        or binding.exact_material is not None
        or ledger.integrity_of(binding.identity) == CORRUPTED
        or binding_reference != _subject_to_act_binding_reference(binding)
        or any(type(value) is not bool for value in boundary_outcomes.values())
        or type(source_references) is not list
        or len(set(source_references)) != len(source_references)
        or any(
            type(reference) is not str
            or not reference
            or ledger.get(reference) is None
            or ledger.integrity_of(reference) == CORRUPTED
            for reference in source_references
        )
        or type(read_occurrences) is not list
        or act_occurrence is None
        or act_occurrence.kind != WITNESS_MATERIAL_SOURCE_ACT_OCCURRENCE_EVENT
        or act_occurrence.locality_identity != event.locality_identity
        or act_occurrence.exact_material is not None
        or ledger.integrity_of(act_occurrence.identity) == CORRUPTED
    ):
        raise MaterialSourceError(
            "Witness material result is absent or corrupted"
        )
    expected_binding = _subject_to_act_binding_material(
        source_boundary=source_boundary,
        exact_act_identity=source_act_identity,
        act_occurrence_identity=act_occurrence_identity,
        result_identity=result_identity,
    )
    if binding.material != expected_binding:
        raise MaterialSourceError(
            "Witness material result is absent or corrupted"
        )
    result: dict[str, object] = {
        "result_identity": result_identity,
        "exact_act_identity": source_act_identity,
        "act_occurrence_identity": act_occurrence_identity,
        "source_boundary": source_boundary,
        "subject_to_act_binding_reference": binding_reference,
        "source_occurrence_references": source_references,
    }
    result.update(boundary_outcomes)
    if read_occurrences:
        result["read_occurrences"] = read_occurrences
    expected_act_occurrence = {
        "exact_act_identity": source_act_identity,
        "act_occurrence_identity": act_occurrence_identity,
        "act": WITNESS_MATERIAL_SOURCE_ACT,
        "subject_to_act_binding_reference": binding_reference,
    }
    expected_material = {
        **result,
        "act_occurrence_event_identity": act_occurrence.identity,
        "yield_relation_identity": yield_identity,
    }
    if (
        act_occurrence.material != expected_act_occurrence
        or material != expected_material
    ):
        raise MaterialSourceError(
            "Witness material result is absent or corrupted"
        )
    try:
        _require_read_occurrence_coordinates(
            event.exact_material, read_occurrences
        )
    except WitnessMaterialSourceError as error:
        raise MaterialSourceError(
            "Witness material result carries malformed read occurrences"
        ) from error
    try:
        ordered = ledger.occurrences_in_append_order(
            (
                binding.identity,
                act_occurrence.identity,
                yield_identity,
                event.identity,
            ),
            locality_identity=event.locality_identity,
        )
        requirements = read_requirements_of_yield_relation(
            ledger,
            recorded_result_event_identity=event.identity,
            yield_relation_event_identity=yield_identity,
            act_occurrence_event_identity=act_occurrence.identity,
        )
    except (TypeError, ValueError) as error:
        raise MaterialSourceError(
            "Witness material result carries no intact Act and Yield"
        ) from error
    if [occurrence.identity for occurrence in ordered] != [
        binding.identity,
        act_occurrence.identity,
        yield_identity,
        event.identity,
    ] or not all(requirements.values()):
        raise MaterialSourceError(
            "Witness material result carries no intact Act and Yield"
        )
    return event
