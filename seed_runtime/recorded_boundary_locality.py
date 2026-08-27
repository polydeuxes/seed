"""Preserve one exact recorded boundary result at one destination Locality."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from seed_runtime.event import Event
from seed_runtime.events import CORRUPTED, EventLedger
from seed_runtime.operator_checkpoint import get_recorded_through_occurrence_boundary_reference
from seed_runtime.yield_relation import (
    RECORDED_YIELD_RELATION_EVENT,
    _record_yield_relation,
    read_requirements_of_yield_relation,
)


RECORDED_BOUNDARY_LOCALITY_SUBJECT_TO_ACT_BINDING_RECORDED_KIND = (
    "operator.recorded_boundary_locality_subject_to_act_binding_recorded"
)
RECORDED_BOUNDARY_LOCALITY_ACT_OCCURRENCE_EVENT = (
    "operator.recorded_boundary_locality_act_occurrence_recorded"
)
RECORDED_BOUNDARY_LOCALITY_RECORDED_KIND = (
    "operator.recorded_boundary_locality_recorded"
)
RECORDED_BOUNDARY_LOCALITY_RESULT_KIND = (
    "recorded boundary Locality relation result"
)
RECORDED_BOUNDARY_LOCALITY_ACT = (
    "Preserve one exact recorded boundary result at one destination Locality"
)
RECORDED_BOUNDARY_LOCALITY_BOOK_CLAUSE = "06.Locality.C"
EVENT_KIND_BOOK_CLAUSES = {
    RECORDED_BOUNDARY_LOCALITY_SUBJECT_TO_ACT_BINDING_RECORDED_KIND: (
        "06.Locality.C"
    ),
    RECORDED_BOUNDARY_LOCALITY_ACT_OCCURRENCE_EVENT: "02.Acts.A",
    RECORDED_BOUNDARY_LOCALITY_RECORDED_KIND: "06.Locality.A",
}


class RecordedBoundaryLocalityError(ValueError):
    """One exact recorded boundary Locality relation is not established."""


def _require_identity(value: Any, message: str) -> str:
    if type(value) is not str or not value:
        raise RecordedBoundaryLocalityError(message)
    return value


def _through_occurrence_reference(
    ledger: EventLedger, recorded_result_event_identity: str
) -> dict[str, str]:
    recorded = get_recorded_through_occurrence_boundary_reference(
        ledger, recorded_result_event_identity
    )
    return {
        "recorded_occurrence_identity": recorded_result_event_identity,
        "result_identity": recorded["result_identity"],
    }


def _resolve_one_carried_reference(
    ledger: EventLedger,
    *,
    source_current_coordinates: dict[str, Any],
) -> dict[str, str]:
    if type(source_current_coordinates) is not dict:
        raise RecordedBoundaryLocalityError(
            "recorded boundary Locality requires exact source current coordinates"
        )
    source_locality = _require_identity(
        source_current_coordinates.get("locality_identity"),
        "recorded boundary Locality requires one source Locality",
    )
    direct_references = source_current_coordinates.get(
        "recorded_through_occurrence_boundary_references"
    )
    relations = source_current_coordinates.get(
        "recorded_boundary_locality_relations"
    )
    if type(direct_references) is not dict or type(relations) is not dict:
        raise RecordedBoundaryLocalityError(
            "recorded boundary Locality requires exact carried identities"
        )
    carried_occurrences = [
        *(identity for identity, value in direct_references.items() if value is None),
        *(identity for identity, value in relations.items() if value is None),
    ]
    if len(carried_occurrences) != len(direct_references) + len(relations):
        raise RecordedBoundaryLocalityError(
            "recorded boundary Locality carriers are not exact"
        )
    if len(carried_occurrences) != 1:
        raise RecordedBoundaryLocalityError(
            "recorded boundary Locality requires exactly one carried reference"
        )
    event_identity = carried_occurrences[0]
    event = ledger.get(event_identity)
    if event is None or event.locality_identity != source_locality:
        raise RecordedBoundaryLocalityError(
            "recorded boundary Locality names a different carried occurrence"
        )
    if event_identity in direct_references:
        return _through_occurrence_reference(ledger, event_identity)
    relation = get_recorded_boundary_locality(ledger, event_identity)
    return deepcopy(relation["through_occurrence_boundary_reference"])


def _binding_material(
    *,
    exact_act_identity: str,
    act_occurrence_identity: str,
    result_identity: str,
    through_occurrence_boundary_reference: dict[str, str],
    destination_locality_identity: str,
) -> dict[str, Any]:
    return {
        "book_clause_identity": RECORDED_BOUNDARY_LOCALITY_BOOK_CLAUSE,
        "exact_act_identity": exact_act_identity,
        "act_occurrence_identity": act_occurrence_identity,
        "result_identity": result_identity,
        "result_boundary_identity": result_identity,
        "subject_reference": deepcopy(through_occurrence_boundary_reference),
    }


def _binding_reference(binding: Event) -> dict[str, Any]:
    return {
        "recorded_occurrence_identity": binding.identity,
        "book_clause_identity": binding.material["book_clause_identity"],
        "exact_act_identity": binding.material["exact_act_identity"],
        "subject_reference": deepcopy(
            binding.material["subject_reference"]
        ),
        "result_boundary_identity": binding.material[
            "result_boundary_identity"
        ],
    }


def _act_material(binding: Event) -> dict[str, Any]:
    material = binding.material
    return {
        "exact_act_identity": material["exact_act_identity"],
        "act_occurrence_identity": material["act_occurrence_identity"],
        "act": RECORDED_BOUNDARY_LOCALITY_ACT,
        "subject_to_act_binding_reference": _binding_reference(binding),
        "through_occurrence_boundary_reference": deepcopy(
            material["subject_reference"]
        ),
        "destination_locality_identity": binding.locality_identity,
        "result_identity": material["result_identity"],
    }


def _result_material(act: Event) -> dict[str, Any]:
    material = act.material
    return {
        "result_identity": material["result_identity"],
        "exact_act_identity": material["exact_act_identity"],
        "act_occurrence_identity": material["act_occurrence_identity"],
        "exact_act": RECORDED_BOUNDARY_LOCALITY_ACT,
        "subject_to_act_binding_reference": deepcopy(
            material["subject_to_act_binding_reference"]
        ),
        "through_occurrence_boundary_reference": deepcopy(
            material["through_occurrence_boundary_reference"]
        ),
        "destination_locality_identity": act.locality_identity,
    }


def _recorded_result_material(
    result_material: dict[str, Any],
    *, act_occurrence_event_identity: str,
    yield_relation_identity: str,
) -> dict[str, Any]:
    return {
        "result_identity": result_material["result_identity"],
        "exact_act_identity": result_material["exact_act_identity"],
        "act_occurrence_identity": result_material["act_occurrence_identity"],
        "exact_act": result_material["exact_act"],
        "subject_to_act_binding_reference": deepcopy(
            result_material["subject_to_act_binding_reference"]
        ),
        "through_occurrence_boundary_reference": deepcopy(
            result_material["through_occurrence_boundary_reference"]
        ),
        "destination_locality_identity": result_material[
            "destination_locality_identity"
        ],
        "act_occurrence_event_identity": act_occurrence_event_identity,
        "yield_relation_identity": yield_relation_identity,
    }


def record_recorded_boundary_locality_subject_to_act_binding(
    ledger: EventLedger,
    *,
    source_current_coordinates: dict[str, Any],
) -> Event:
    """Bind one direct Locality relation from one carried recorded result."""

    if not isinstance(ledger, EventLedger):
        raise TypeError("recorded boundary Locality requires one EventLedger")
    carried_reference = _resolve_one_carried_reference(
        ledger, source_current_coordinates=source_current_coordinates
    )
    destination = ledger.mint_identity("recorded_boundary_locality")
    if ledger.has_locality(destination):
        raise RecordedBoundaryLocalityError(
            "recorded boundary Locality requires one unused destination Locality"
        )
    identities = {
        "exact_act_identity": ledger.mint_identity(
            "recorded_boundary_locality_act"
        ),
        "act_occurrence_identity": ledger.mint_identity(
            "recorded_boundary_locality_act_occurrence"
        ),
        "result_identity": ledger.mint_identity(
            "recorded_boundary_locality_result"
        ),
    }
    return ledger.append(
        RECORDED_BOUNDARY_LOCALITY_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
        _binding_material(
            through_occurrence_boundary_reference=carried_reference,
            destination_locality_identity=destination,
            **identities,
        ),
        locality_identity=destination,
    )


def get_recorded_boundary_locality_subject_to_act_binding(
    ledger: EventLedger, event_identity: str
) -> Event:
    _require_identity(event_identity, "recorded boundary relation requires binding")
    event = ledger.get(event_identity)
    if (
        event is None
        or event.kind
        != RECORDED_BOUNDARY_LOCALITY_SUBJECT_TO_ACT_BINDING_RECORDED_KIND
        or type(event.locality_identity) is not str
        or event.exact_material is not None
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise RecordedBoundaryLocalityError(
            "recorded boundary relation binding is absent or corrupted"
        )
    material = event.material
    carried_reference = material.get("subject_reference")
    identities = (
        material.get("exact_act_identity"),
        material.get("act_occurrence_identity"),
        material.get("result_identity"),
    )
    if (
        type(carried_reference) is not dict
        or any(type(value) is not str or not value for value in identities)
        or len(set(identities)) != len(identities)
    ):
        raise RecordedBoundaryLocalityError(
            "recorded boundary relation binding identities are not exact"
        )
    expected_reference = _through_occurrence_reference(
        ledger, carried_reference.get("recorded_occurrence_identity")
    )
    expected = _binding_material(
        exact_act_identity=identities[0],
        act_occurrence_identity=identities[1],
        result_identity=identities[2],
        through_occurrence_boundary_reference=expected_reference,
        destination_locality_identity=event.locality_identity,
    )
    if material != expected:
        raise RecordedBoundaryLocalityError(
            "recorded boundary relation binding is not exact"
        )
    return event


def record_recorded_boundary_locality_act_occurrence(
    ledger: EventLedger,
    *, subject_to_act_binding_event_identity: str,
    current_coordinates: dict[str, Any],
) -> Event:
    binding = get_recorded_boundary_locality_subject_to_act_binding(
        ledger, subject_to_act_binding_event_identity
    )
    if type(current_coordinates) is not dict:
        raise RecordedBoundaryLocalityError(
            "recorded boundary relation Act requires current coordinates"
        )
    carried = current_coordinates.get(
        "subject_to_act_binding_occurrences"
    )
    if (
        current_coordinates.get("locality_identity")
        != binding.locality_identity
        or type(carried) is not dict
        or carried.get(binding.identity, object()) is not None
    ):
        raise RecordedBoundaryLocalityError(
            "recorded boundary relation Act requires its carried binding"
        )
    return ledger.append(
        RECORDED_BOUNDARY_LOCALITY_ACT_OCCURRENCE_EVENT,
        _act_material(binding),
        locality_identity=binding.locality_identity,
    )


def get_recorded_boundary_locality_act_occurrence(
    ledger: EventLedger, event_identity: str
) -> Event:
    _require_identity(event_identity, "recorded boundary relation requires Act occurrence")
    event = ledger.get(event_identity)
    if (
        event is None
        or event.kind != RECORDED_BOUNDARY_LOCALITY_ACT_OCCURRENCE_EVENT
        or event.exact_material is not None
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise RecordedBoundaryLocalityError(
            "recorded boundary relation Act occurrence is absent or corrupted"
        )
    reference = event.material.get("subject_to_act_binding_reference")
    if type(reference) is not dict:
        raise RecordedBoundaryLocalityError(
            "recorded boundary relation Act carries no binding"
        )
    binding = get_recorded_boundary_locality_subject_to_act_binding(
        ledger, reference.get("recorded_occurrence_identity")
    )
    if (
        binding.locality_identity != event.locality_identity
        or reference != _binding_reference(binding)
        or event.material != _act_material(binding)
    ):
        raise RecordedBoundaryLocalityError(
            "recorded boundary relation Act occurrence is not exact"
        )
    try:
        ledger.occurrences_in_append_order(
            (binding.identity, event.identity),
            locality_identity=event.locality_identity,
        )
    except ValueError as error:
        raise RecordedBoundaryLocalityError(
            "recorded boundary relation Act requires its prior binding"
        ) from error
    return event


def record_recorded_boundary_locality_result(
    ledger: EventLedger,
    *, act_occurrence_event_identity: str,
) -> Event:
    act = get_recorded_boundary_locality_act_occurrence(
        ledger, act_occurrence_event_identity
    )
    for yield_relation in ledger.iter_locality_kind(
        act.locality_identity, RECORDED_YIELD_RELATION_EVENT
    ):
        if yield_relation.material.get("act_occurrence_event_identity") == act.identity:
            raise RecordedBoundaryLocalityError(
                "recorded boundary relation Act already carries a Yield"
            )
    result_material = _result_material(act)
    yield_relation = _record_yield_relation(
        ledger,
        locality_identity=act.locality_identity,
        exact_act=RECORDED_BOUNDARY_LOCALITY_ACT,
        act_occurrence_identity=act.material["act_occurrence_identity"],
        act_occurrence_event_identity=act.identity,
        result_kind=RECORDED_BOUNDARY_LOCALITY_RESULT_KIND,
        result_identity=result_material["result_identity"],
        result_content=result_material,
        occurrence_boundary="recorded_boundary_locality_relation",
    )
    return ledger.append(
        RECORDED_BOUNDARY_LOCALITY_RECORDED_KIND,
        _recorded_result_material(
            result_material,
            act_occurrence_event_identity=act.identity,
            yield_relation_identity=yield_relation.identity,
        ),
        locality_identity=act.locality_identity,
    )


def get_recorded_boundary_locality(
    ledger: EventLedger, event_identity: str
) -> dict[str, Any]:
    _require_identity(event_identity, "recorded boundary relation requires result")
    event = ledger.get(event_identity)
    if (
        event is None
        or event.kind != RECORDED_BOUNDARY_LOCALITY_RECORDED_KIND
        or event.exact_material is not None
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise RecordedBoundaryLocalityError(
            "recorded boundary relation result is absent or corrupted"
        )
    act = get_recorded_boundary_locality_act_occurrence(
        ledger, event.material.get("act_occurrence_event_identity")
    )
    expected_result = _result_material(act)
    expected = _recorded_result_material(
        expected_result,
        act_occurrence_event_identity=act.identity,
        yield_relation_identity=event.material.get("yield_relation_identity"),
    )
    if event.locality_identity != act.locality_identity or event.material != expected:
        raise RecordedBoundaryLocalityError(
            "recorded boundary relation result coordinates are not exact"
        )
    requirements = read_requirements_of_yield_relation(
        ledger,
        recorded_result_event_identity=event.identity,
        yield_relation_event_identity=event.material["yield_relation_identity"],
        act_occurrence_event_identity=act.identity,
    )
    if not all(requirements.values()):
        raise RecordedBoundaryLocalityError(
            "recorded boundary relation result carries no exact Yield"
        )
    return deepcopy(event.material)
