"""One exact operator-material boundary occurrence and its exact result."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from seed_runtime.event import Event
from seed_runtime.events import CORRUPTED, EventLedger
from seed_runtime.operator_material_boundary import OperatorBoundaryMaterial


OPERATOR_MATERIAL_SOURCE_SUBJECT_TO_ACT_BINDING_RECORDED_KIND = (
    "operator.material.source_subject_to_act_binding_recorded"
)
OPERATOR_MATERIAL_SOURCE_ACT_OCCURRENCE_EVENT = (
    "operator.material.source_act_occurrence_recorded"
)
OPERATOR_MATERIAL_SOURCE_RECORDED_KIND = "operator.material.source_recorded"
OPERATOR_MATERIAL_SOURCE_RESULT_KIND = "exact operator material boundary result"
OPERATOR_MATERIAL_SOURCE_ACT = "Source"
OPERATOR_MATERIAL_SOURCE_BOOK_CLAUSE = "01.Source.G"
EVENT_KIND_BOOK_CLAUSES = {
    OPERATOR_MATERIAL_SOURCE_SUBJECT_TO_ACT_BINDING_RECORDED_KIND: (
        "01.Source.G"
    ),
    OPERATOR_MATERIAL_SOURCE_ACT_OCCURRENCE_EVENT: "02.Acts.A",
    OPERATOR_MATERIAL_SOURCE_RECORDED_KIND: "01.Source.G",
}


class OperatorMaterialSourceError(ValueError):
    """One operator-material boundary occurrence is not exact."""


def _require_identity(value: Any, message: str) -> str:
    if type(value) is not str or not value:
        raise OperatorMaterialSourceError(message)
    return value


def _current_coordinate_reference(
    ledger: EventLedger,
    *,
    locality_identity: str,
    current_coordinates: dict[str, Any],
    binding_event_identity: str | None = None,
) -> dict[str, str | None]:
    _require_identity(
        locality_identity,
        "operator material source requires one exact Locality",
    )
    if type(current_coordinates) is not dict:
        raise OperatorMaterialSourceError(
            "operator material source requires exact current coordinates"
        )
    if current_coordinates.get("locality_identity") != locality_identity:
        raise OperatorMaterialSourceError(
            "operator material source has a different current-coordinate Locality"
        )
    through_event_identity = current_coordinates.get(
        "through_event_occurrence_identity"
    )
    if binding_event_identity is None:
        latest = ledger.latest_locality_event(locality_identity)
        prior_event_identity = latest.identity if latest is not None else None
    else:
        try:
            earlier = ledger.prior_locality_event(
                binding_event_identity, locality_identity
            )
        except ValueError as error:
            raise OperatorMaterialSourceError(
                "operator material source requires its exact through-occurrence boundary"
            ) from error
        prior_event_identity = earlier.identity if earlier is not None else None
    if through_event_identity != prior_event_identity:
        raise OperatorMaterialSourceError(
            "operator material source requires its exact through-occurrence boundary"
        )
    if through_event_identity is not None:
        _require_identity(
            through_event_identity,
            "operator material source requires one exact through-occurrence boundary",
        )
        boundary_event = ledger.get(through_event_identity)
        if (
            boundary_event is None
            or boundary_event.locality_identity != locality_identity
            or ledger.integrity_of(boundary_event.identity) == CORRUPTED
        ):
            raise OperatorMaterialSourceError(
                "operator material source requires its exact through-occurrence boundary"
            )
    return {
        "locality_identity": locality_identity,
        "through_event_occurrence_identity": through_event_identity,
    }


def _subject_to_act_binding_material(
    *,
    exact_act_identity: str,
    act_occurrence_identity: str,
    result_identity: str,
    source_boundary: str,
    current_coordinate_reference: dict[str, str | None],
) -> dict[str, Any]:
    subject_reference = {"source_boundary": source_boundary}
    return {
        "book_clause_identity": OPERATOR_MATERIAL_SOURCE_BOOK_CLAUSE,
        "subject_reference": subject_reference,
        "act": OPERATOR_MATERIAL_SOURCE_ACT,
        "exact_act_identity": exact_act_identity,
        "act_occurrence_identity": act_occurrence_identity,
        "result_identity": result_identity,
        "current_coordinate_reference": deepcopy(
            current_coordinate_reference
        ),
    }


def _subject_to_act_binding_reference(binding: Event) -> dict[str, Any]:
    return {
        "recorded_occurrence_identity": binding.identity,
        "book_clause_identity": binding.material["book_clause_identity"],
        "exact_act_identity": binding.material["exact_act_identity"],
        "subject_reference": deepcopy(binding.material["subject_reference"]),
    }


def _act_occurrence_material(binding: Event) -> dict[str, Any]:
    material = binding.material
    return {
        "source_boundary": material["subject_reference"]["source_boundary"],
        "exact_act_identity": material["exact_act_identity"],
        "act_occurrence_identity": material["act_occurrence_identity"],
        "act": OPERATOR_MATERIAL_SOURCE_ACT,
        "subject_to_act_binding_reference": (
            _subject_to_act_binding_reference(binding)
        ),
        "current_coordinate_reference": deepcopy(
            material["current_coordinate_reference"]
        ),
        "result_identity": material["result_identity"],
    }


def _result_material(
    act_occurrence: Event,
    *,
    boundary_material: OperatorBoundaryMaterial,
) -> dict[str, Any]:
    material = act_occurrence.material
    if boundary_material.material_boundary != material.get("source_boundary"):
        raise OperatorMaterialSourceError(
            "operator material source result crossed its exact source boundary"
        )
    return {
        "result_identity": material["result_identity"],
        "exact_act_identity": material["exact_act_identity"],
        "act_occurrence_identity": material["act_occurrence_identity"],
        "exact_act": OPERATOR_MATERIAL_SOURCE_ACT,
        "subject_to_act_binding_reference": deepcopy(
            material["subject_to_act_binding_reference"]
        ),
        "current_coordinate_reference": deepcopy(
            material["current_coordinate_reference"]
        ),
        "source_boundary": boundary_material.material_boundary,
    }


def _recorded_result_material(
    result_material: dict[str, Any],
    *,
    act_occurrence_event_identity: str,
) -> dict[str, Any]:
    recorded = {
        "result_identity": result_material["result_identity"],
        "exact_act_identity": result_material["exact_act_identity"],
        "act_occurrence_identity": result_material["act_occurrence_identity"],
        "exact_act": result_material["exact_act"],
        "subject_to_act_binding_reference": result_material[
            "subject_to_act_binding_reference"
        ],
        "current_coordinate_reference": result_material[
            "current_coordinate_reference"
        ],
        "source_boundary": result_material["source_boundary"],
        "source_occurrence_references": [],
    }
    recorded["act_occurrence_event_identity"] = act_occurrence_event_identity
    return recorded


def record_operator_material_source_subject_to_act_binding(
    ledger: EventLedger,
    *,
    locality_identity: str,
    current_coordinates: dict[str, Any],
    source_boundary: str,
) -> Event:
    """Record the exact operator-boundary subject-to-Act binding."""

    if not isinstance(ledger, EventLedger):
        raise TypeError("operator material source requires one EventLedger")
    _require_identity(
        source_boundary,
        "operator material source requires one exact source boundary",
    )
    current_reference = _current_coordinate_reference(
        ledger,
        locality_identity=locality_identity,
        current_coordinates=current_coordinates,
    )
    return _record_operator_material_source_subject_to_act_binding(
        ledger,
        locality_identity=locality_identity,
        source_boundary=source_boundary,
        current_reference=current_reference,
    )


def _record_operator_material_source_subject_to_act_binding_from_current_coordinates(
    ledger: EventLedger,
    *,
    locality_identity: str,
    current_coordinates: dict[str, Any],
    source_boundary: str,
) -> Event:
    _require_identity(
        source_boundary,
        "operator material source requires one exact source boundary",
    )
    current_reference = _current_coordinate_reference(
        ledger,
        locality_identity=locality_identity,
        current_coordinates=current_coordinates,
    )
    return _record_operator_material_source_subject_to_act_binding(
        ledger,
        locality_identity=locality_identity,
        source_boundary=source_boundary,
        current_reference=current_reference,
    )


def _record_operator_material_source_subject_to_act_binding(
    ledger: EventLedger,
    *,
    locality_identity: str,
    source_boundary: str,
    current_reference: dict[str, str | None],
) -> Event:
    exact_act_identity = ledger.mint_identity("operator_material_source_act")
    act_occurrence_identity = ledger.mint_identity(
        "operator_material_source_act_occurrence"
    )
    result_identity = ledger.mint_identity(
        "operator_material_source_result"
    )
    return ledger.append(
        OPERATOR_MATERIAL_SOURCE_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
        _subject_to_act_binding_material(
            exact_act_identity=exact_act_identity,
            act_occurrence_identity=act_occurrence_identity,
            result_identity=result_identity,
            source_boundary=source_boundary,
            current_coordinate_reference=current_reference,
        ),
        locality_identity=locality_identity,
    )


def get_operator_material_source_subject_to_act_binding(
    ledger: EventLedger, binding_event_identity: str
) -> Event:
    """Read one exact recorded subject-to-Act binding."""

    _require_identity(
        binding_event_identity,
        "operator material source requires one binding occurrence",
    )
    binding = ledger.get(binding_event_identity)
    if (
        binding is None
        or binding.kind
        != OPERATOR_MATERIAL_SOURCE_SUBJECT_TO_ACT_BINDING_RECORDED_KIND
        or type(binding.locality_identity) is not str
        or not binding.locality_identity
        or binding.exact_material is not None
        or ledger.integrity_of(binding.identity) == CORRUPTED
    ):
        raise OperatorMaterialSourceError(
            "operator material source binding is absent or corrupted"
        )
    material = binding.material
    current_reference = material.get("current_coordinate_reference")
    subject_reference = material.get("subject_reference")
    identities = (
        material.get("exact_act_identity"),
        material.get("act_occurrence_identity"),
        material.get("result_identity"),
    )
    if (
        type(current_reference) is not dict
        or current_reference.get("locality_identity") != binding.locality_identity
        or type(subject_reference) is not dict
        or type(subject_reference.get("source_boundary")) is not str
        or not subject_reference["source_boundary"]
        or any(type(identity) is not str or not identity for identity in identities)
        or len(set(identities)) != len(identities)
    ):
        raise OperatorMaterialSourceError(
            "operator material source binding coordinates are not exact"
        )
    exact_current_reference = _current_coordinate_reference(
        ledger,
        locality_identity=binding.locality_identity,
        current_coordinates={
            "locality_identity": binding.locality_identity,
            "through_event_occurrence_identity": current_reference.get(
                "through_event_occurrence_identity"
            ),
        },
        binding_event_identity=binding.identity,
    )
    exact_binding_material = _subject_to_act_binding_material(
        exact_act_identity=identities[0],
        act_occurrence_identity=identities[1],
        result_identity=identities[2],
        source_boundary=subject_reference["source_boundary"],
        current_coordinate_reference=exact_current_reference,
    )
    if material != exact_binding_material:
        raise OperatorMaterialSourceError(
            "operator material source binding is not exact"
        )
    return binding


def record_operator_material_source_act_occurrence(
    ledger: EventLedger,
    *,
    subject_to_act_binding_event_identity: str,
    current_coordinates: dict[str, Any],
) -> Event:
    """Record the distinct Act occurrence from its carried binding."""

    binding = get_operator_material_source_subject_to_act_binding(
        ledger, subject_to_act_binding_event_identity
    )
    return _record_operator_material_source_act_occurrence(
        ledger,
        binding=binding,
        current_coordinates=current_coordinates,
    )


def _record_operator_material_source_act_occurrence_from_binding(
    ledger: EventLedger,
    *,
    subject_to_act_binding: Event,
    current_coordinates: dict[str, Any],
) -> Event:
    if (
        type(subject_to_act_binding) is not Event
        or subject_to_act_binding.kind
        != OPERATOR_MATERIAL_SOURCE_SUBJECT_TO_ACT_BINDING_RECORDED_KIND
        or subject_to_act_binding.exact_material is not None
        or type(current_coordinates) is not dict
        or current_coordinates.get(
            "through_event_occurrence_identity"
        )
        != subject_to_act_binding.identity
    ):
        raise OperatorMaterialSourceError(
            "operator material source Act requires its recorded binding"
        )
    return _record_operator_material_source_act_occurrence(
        ledger,
        binding=subject_to_act_binding,
        current_coordinates=current_coordinates,
    )


def _record_operator_material_source_act_occurrence(
    ledger: EventLedger,
    *,
    binding: Event,
    current_coordinates: dict[str, Any],
) -> Event:
    if type(current_coordinates) is not dict:
        raise OperatorMaterialSourceError(
            "operator material source Act requires current coordinates"
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
        raise OperatorMaterialSourceError(
            "operator material source Act requires its exact carried binding"
        )
    return ledger.append(
        OPERATOR_MATERIAL_SOURCE_ACT_OCCURRENCE_EVENT,
        _act_occurrence_material(binding),
        locality_identity=binding.locality_identity,
    )


def get_operator_material_source_act_occurrence(
    ledger: EventLedger, act_occurrence_event_identity: str
) -> Event:
    """Read one exact source Act occurrence occurrence."""

    _require_identity(
        act_occurrence_event_identity,
        "operator material source result requires one Act occurrence occurrence",
    )
    act_occurrence = ledger.get(act_occurrence_event_identity)
    if (
        act_occurrence is None
        or act_occurrence.kind != OPERATOR_MATERIAL_SOURCE_ACT_OCCURRENCE_EVENT
        or type(act_occurrence.locality_identity) is not str
        or not act_occurrence.locality_identity
        or act_occurrence.exact_material is not None
        or ledger.integrity_of(act_occurrence.identity) == CORRUPTED
    ):
        raise OperatorMaterialSourceError(
            "operator material source requires intact Act occurrence"
        )
    reference = act_occurrence.material.get("subject_to_act_binding_reference")
    if type(reference) is not dict:
        raise OperatorMaterialSourceError(
            "operator material source Act carries no exact binding"
        )
    binding = get_operator_material_source_subject_to_act_binding(
        ledger, reference.get("recorded_occurrence_identity")
    )
    if (
        binding.locality_identity != act_occurrence.locality_identity
        or reference != _subject_to_act_binding_reference(binding)
        or act_occurrence.material != _act_occurrence_material(binding)
    ):
        raise OperatorMaterialSourceError(
            "operator material source Act occurrence is not exact"
        )
    try:
        ledger.occurrences_in_append_order(
            (binding.identity, act_occurrence.identity),
            locality_identity=act_occurrence.locality_identity,
        )
    except ValueError as error:
        raise OperatorMaterialSourceError(
            "operator material source Act requires its prior binding"
        ) from error
    return act_occurrence


def record_operator_material_source_result(
    ledger: EventLedger,
    *,
    act_occurrence_event_identity: str,
    boundary_material: OperatorBoundaryMaterial,
) -> Event:
    """Record one exact nonempty boundary result."""

    act_occurrence = get_operator_material_source_act_occurrence(
        ledger, act_occurrence_event_identity
    )
    return _record_operator_material_source_result(
        ledger,
        act_occurrence=act_occurrence,
        boundary_material=boundary_material,
    )


def _record_operator_material_source_result(
    ledger: EventLedger,
    *,
    act_occurrence: Event,
    boundary_material: OperatorBoundaryMaterial,
) -> Event:
    if not isinstance(boundary_material, OperatorBoundaryMaterial):
        raise TypeError("operator material source requires exact boundary material")
    if boundary_material.eof:
        raise OperatorMaterialSourceError(
            "an empty operator boundary establishes no material result"
        )
    if (
        boundary_material.material_boundary
        != act_occurrence.material.get("source_boundary")
    ):
        raise OperatorMaterialSourceError(
            "operator material source result crossed its exact source boundary"
        )
    prior_results = tuple(
        result
        for result in ledger.iter_locality_kind(
            act_occurrence.locality_identity,
            OPERATOR_MATERIAL_SOURCE_RECORDED_KIND,
        )
        if result.material.get("act_occurrence_event_identity")
        == act_occurrence.identity
    )
    if prior_results:
        raise OperatorMaterialSourceError(
            "operator material source Act already has a result"
        )
    recorded_result_event_identity = ledger.allocate_event_identity()
    result_material = _result_material(
        act_occurrence,
        boundary_material=boundary_material,
    )
    return ledger.append_many(
        (
            Event(
                identity=recorded_result_event_identity,
                kind=OPERATOR_MATERIAL_SOURCE_RECORDED_KIND,
                material=_recorded_result_material(
                    result_material,
                    act_occurrence_event_identity=act_occurrence.identity,
                ),
                exact_material=boundary_material.exact_bytes,
                locality_identity=act_occurrence.locality_identity,
            ),
        )
    )[0]


def _recorded_operator_material_source_reading(
    ledger: EventLedger, result_event_identity: str
) -> Event:
    """Read one exact boundary result through its exact binding and Act."""

    _require_identity(
        result_event_identity,
        "operator material source read requires one result occurrence",
    )
    result = ledger.get(result_event_identity)
    if (
        result is None
        or result.kind != OPERATOR_MATERIAL_SOURCE_RECORDED_KIND
        or type(result.locality_identity) is not str
        or not result.locality_identity
        or type(result.exact_material) is not bytes
        or not result.exact_material
        or ledger.integrity_of(result.identity) == CORRUPTED
    ):
        raise OperatorMaterialSourceError(
            "operator material source result is absent or corrupted"
        )
    act_occurrence = get_operator_material_source_act_occurrence(
        ledger, result.material.get("act_occurrence_event_identity")
    )
    boundary = OperatorBoundaryMaterial(
        exact_bytes=result.exact_material,
        eof=False,
        material_boundary=result.material.get("source_boundary"),
    )
    act_result_material = _result_material(
        act_occurrence,
        boundary_material=boundary,
    )
    exact_recorded_material = _recorded_result_material(
        act_result_material,
        act_occurrence_event_identity=act_occurrence.identity,
    )
    if (
        result.locality_identity != act_occurrence.locality_identity
        or result.material != exact_recorded_material
    ):
        raise OperatorMaterialSourceError(
            "operator material source result coordinates are not exact"
        )
    try:
        ordered = ledger.occurrences_in_append_order(
            (
                act_occurrence.material["subject_to_act_binding_reference"][
                    "recorded_occurrence_identity"
                ],
                act_occurrence.identity,
                result.identity,
            ),
            locality_identity=result.locality_identity,
        )
    except (TypeError, ValueError) as error:
        raise OperatorMaterialSourceError(
            "operator material source result carries no intact Act"
        ) from error
    if [occurrence.identity for occurrence in ordered] != [
        act_occurrence.material["subject_to_act_binding_reference"][
            "recorded_occurrence_identity"
        ],
        act_occurrence.identity,
        result.identity,
    ]:
        raise OperatorMaterialSourceError(
            "operator material source result carries no intact Act"
        )
    results = tuple(
        candidate
        for candidate in ledger.iter_locality_kind(
            result.locality_identity,
            OPERATOR_MATERIAL_SOURCE_RECORDED_KIND,
        )
        if candidate.material.get("act_occurrence_event_identity")
        == act_occurrence.identity
    )
    if len(results) != 1 or results[0].identity != result.identity:
        raise OperatorMaterialSourceError(
            "operator material source Act has no single exact result"
        )
    return result


def get_recorded_operator_material_source(
    ledger: EventLedger, result_event_identity: str
) -> dict[str, Any]:
    """Return detached material from one exact operator source result."""

    return deepcopy(
        _recorded_operator_material_source_reading(
            ledger,
            result_event_identity,
        ).material
    )
