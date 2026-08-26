"""Determine pair-position Assertions carrying one addressed byte coordinate.

This D.2 lifecycle consumes one exact recorded direct pair-position Measurement
and one exact source-byte position-coordinate reference.  It preserves every
Assertion reference carrying that exact coordinate and no other Assertion; it
establishes no recurrence, shared position, represented relation, or other
relation.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from seed_runtime.event import Event
from seed_runtime.events import CORRUPTED, EventLedger
from seed_runtime.yield_relation import (
    RECORDED_YIELD_RELATION_EVENT,
    _record_yield_relation,
    read_requirements_of_yield_relation,
)
from seed_runtime.measurement_of_position_coordinates_of_byte_pair_occurrences import (
    BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND,
    ReferenceToRecordedPositionOfBytePairOccurrence,
    references_to_recorded_byte_pair_occurrences_carrying_addressed_source_position_coordinate,
)


DETERMINATION_SUBJECT_TO_ACT_BINDING_RECORDED_KIND = (
    "operator.addressed_byte_occurrence_reference_determination."
    "determination_subject_to_act_binding_recorded"
)
APPLICABILITY_SUBJECT_TO_ACT_BINDING_RECORDED_KIND = (
    "operator.addressed_byte_occurrence_reference_determination."
    "applicability_subject_to_act_binding_recorded"
)
APPLICABILITY_ACT_OCCURRENCE_EVENT = (
    "operator.addressed_byte_occurrence_reference_determination."
    "applicability_act_occurrence_recorded"
)
APPLICABILITY_RESULT_KIND = (
    "operator.addressed_byte_occurrence_reference_determination."
    "applicability_recorded"
)
DETERMINATION_ACT_OCCURRENCE_EVENT = (
    "operator.addressed_byte_occurrence_reference_determination."
    "determination_measurement_act_occurrence_recorded"
)
DETERMINATION_RESULT_KIND = (
    "operator.addressed_byte_occurrence_reference_determination."
    "determination_measurement_recorded"
)

BOOK_CLAUSE = "01.Source.D.2"
APPLICABILITY_ACT = "addressed byte occurrence reference Applicability"
DETERMINATION_ACT = (
    "declared Measurement of exact pair-occurrence position Assertion "
    "references carrying one addressed source-byte position-coordinate reference"
)
APPLICABILITY_YIELD_RESULT_KIND = (
    "addressed byte occurrence reference determination Applicability result"
)
DETERMINATION_YIELD_RESULT_KIND = (
    "result of declared Measurement of exact pair-occurrence position "
    "Assertion references carrying one addressed source-byte position-coordinate "
    "reference"
)
APPLICABILITY_BOUNDARY = (
    "addressed_byte_occurrence_reference_determination_applicability"
)
DETERMINATION_BOUNDARY = "addressed_byte_occurrence_reference_determination"
UNKNOWN = []

EVENT_KIND_BOOK_CLAUSES = {
    DETERMINATION_SUBJECT_TO_ACT_BINDING_RECORDED_KIND: "01.Source.D.2",
    APPLICABILITY_SUBJECT_TO_ACT_BINDING_RECORDED_KIND: "01.Current.E.1",
    APPLICABILITY_ACT_OCCURRENCE_EVENT: "02.Acts.A",
    APPLICABILITY_RESULT_KIND: "01.Current.E.1",
    DETERMINATION_ACT_OCCURRENCE_EVENT: "02.Acts.A",
    DETERMINATION_RESULT_KIND: "01.Source.D.2",
}


class AddressedByteOccurrenceReferenceDeterminationError(ValueError):
    """An addressed byte-occurrence determination coordinate is not exact."""


def _identity(value: Any, message: str) -> str:
    if type(value) is not str or not value:
        raise AddressedByteOccurrenceReferenceDeterminationError(message)
    return value


def _direct_result_reference(event: Event) -> dict[str, str]:
    return {
        "recorded_occurrence_identity": event.identity,
        "result_identity": event.material["result_identity"],
        "act_occurrence_identity": event.material["act_occurrence_identity"],
        "act_occurrence_event_identity": event.material[
            "act_occurrence_event_identity"
        ],
        "yield_relation_identity": event.material[
            "yield_relation_identity"
        ],
    }


def _determination_result_reference(event: Event) -> dict[str, str]:
    """Carry the exact identities of one validated D.2 Measurement result."""

    return {
        "recorded_occurrence_identity": event.identity,
        "result_identity": event.material["result_identity"],
        "act_occurrence_identity": event.material[
            "determination_act_occurrence_identity"
        ],
        "act_occurrence_event_identity": event.material[
            "act_occurrence_event_identity"
        ],
        "yield_relation_identity": event.material[
            "yield_relation_identity"
        ],
    }


def _binding_reference(
    event: Event, *, result_boundary_identity: str
) -> dict[str, Any]:
    return {
        "recorded_occurrence_identity": event.identity,
        "book_clause_identity": event.material["book_clause_identity"],
        "exact_act_identity": event.material["exact_act_identity"],
        "subject_reference": deepcopy(event.material["subject_reference"]),
        "result_boundary_identity": result_boundary_identity,
    }


def _applicability_result_reference(event: Event) -> dict[str, str]:
    return {
        "recorded_occurrence_identity": event.identity,
        "result_identity": event.material["result_identity"],
        "applicability_act_occurrence_identity": event.material[
            "applicability_act_occurrence_identity"
        ],
        "act_occurrence_event_identity": event.material[
            "act_occurrence_event_identity"
        ],
        "yield_relation_identity": event.material[
            "yield_relation_identity"
        ],
    }


def _references_carrying_addressed_coordinate(
    ledger: EventLedger,
    *,
    result_event_identity: str,
    coordinate_reference: dict[str, Any],
) -> tuple[ReferenceToRecordedPositionOfBytePairOccurrence, ...]:
    try:
        return references_to_recorded_byte_pair_occurrences_carrying_addressed_source_position_coordinate(
            ledger,
            result_event_identity,
            coordinate_reference,
        )
    except (TypeError, ValueError) as error:
        raise AddressedByteOccurrenceReferenceDeterminationError(
            "determination requires one exact addressed direct result coordinate"
        ) from error


def _source(
    ledger: EventLedger,
    *,
    result_event_identity: str,
    coordinate_reference: dict[str, Any],
) -> tuple[Event, tuple[ReferenceToRecordedPositionOfBytePairOccurrence, ...]]:
    references = _references_carrying_addressed_coordinate(
        ledger,
        result_event_identity=result_event_identity,
        coordinate_reference=coordinate_reference,
    )
    event = ledger.get(result_event_identity)
    if (
        event is None
        or event.kind != BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND
        or event.exact_material is not None
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise AddressedByteOccurrenceReferenceDeterminationError(
            "determination requires one intact direct result"
        )
    return event, references


def _scope(
    *,
    source_result: Event,
    coordinate_reference: dict[str, Any],
) -> dict[str, str]:
    return {
        "locality_identity": source_result.locality_identity,
        "source_material_result_occurrence_identity": coordinate_reference[
            "source_material_result_occurrence_identity"
        ],
        "completeness_boundary_identity": coordinate_reference[
            "completeness_boundary_identity"
        ],
    }


def _current_coordinates_carry_source(
    ledger: EventLedger,
    *,
    current_coordinates: dict[str, Any],
    source_result: Event,
    required_boundary_identity: str,
) -> None:
    measurements = current_coordinates.get("measurement_occurrences") if type(current_coordinates) is dict else None
    through = current_coordinates.get("through_event_occurrence_identity") if type(current_coordinates) is dict else None
    if (
        type(current_coordinates) is not dict
        or current_coordinates.get("locality_identity") != source_result.locality_identity
        or type(measurements) is not dict
        or measurements.get(source_result.identity) != _direct_result_reference(source_result)
        or type(through) is not str
        or not through
        or type(required_boundary_identity) is not str
        or not required_boundary_identity
    ):
        raise AddressedByteOccurrenceReferenceDeterminationError(
            "current coordinates carry no exact addressed direct result"
        )
    ordered = tuple(
        dict.fromkeys((source_result.identity, required_boundary_identity, through))
    )
    try:
        read = ledger.occurrences_in_append_order(
            ordered, locality_identity=source_result.locality_identity
        )
    except (TypeError, ValueError) as error:
        raise AddressedByteOccurrenceReferenceDeterminationError(
            "through-occurrence boundary carries no addressed direct result"
        ) from error
    if tuple(event.identity for event in read) != ordered:
        raise AddressedByteOccurrenceReferenceDeterminationError(
            "through-occurrence boundary carries no addressed direct result"
        )


def _require_exact_current_coordinates(
    ledger: EventLedger,
    *,
    source_result: Event,
    current_coordinates: dict[str, Any],
) -> dict[str, Any]:
    """Validate the exact current coordinates read by this determination."""

    if type(current_coordinates) is not dict:
        raise AddressedByteOccurrenceReferenceDeterminationError(
            "determination requires exact current coordinates"
        )
    boundary = current_coordinates.get("through_event_occurrence_identity")
    _current_coordinates_carry_source(
        ledger,
        current_coordinates=current_coordinates,
        source_result=source_result,
        required_boundary_identity=boundary,
    )
    boundary_event = ledger.get(boundary)
    if (
        boundary_event is None
        or ledger.integrity_of(boundary_event.identity) == CORRUPTED
        or boundary_event.locality_identity != source_result.locality_identity
        or ledger.append_boundary_through_occurrence(boundary_event.identity)
        != ledger.append_boundary()
    ):
        raise AddressedByteOccurrenceReferenceDeterminationError(
            "determination requires current coordinates through the append boundary"
        )
    return current_coordinates


def _require_intact_recorded_occurrence(
    ledger: EventLedger,
    *,
    event: Event,
    kind: str,
    material: dict[str, Any],
    message: str,
) -> None:
    if (
        type(event) is not Event
        or ledger.get(event.identity) != event
        or event.kind != kind
        or event.exact_material is not None
        or ledger.integrity_of(event.identity) == CORRUPTED
        or event.material != material
    ):
        raise AddressedByteOccurrenceReferenceDeterminationError(message)


def _require_stage_at_append_tip(
    ledger: EventLedger, *, event: Event | None, message: str
) -> None:
    if (
        event is None
        or ledger.get(event.identity) != event
        or ledger.integrity_of(event.identity) == CORRUPTED
        or ledger.append_boundary_through_occurrence(event.identity)
        != ledger.append_boundary()
    ):
        raise AddressedByteOccurrenceReferenceDeterminationError(message)


_DETERMINATION_IDENTITY_COORDINATES = (
    "determination_act_identity",
    "determination_act_occurrence_identity",
    "determination_result_identity",
)


_APPLICABILITY_IDENTITY_COORDINATES = (
    "applicability_act_identity",
    "applicability_act_occurrence_identity",
    "applicability_result_identity",
)


def _determination_binding_material(
    *,
    source_result: Event,
    coordinate_reference: dict[str, Any],
    through_event_occurrence_identity: str,
    identities: dict[str, str],
) -> dict[str, Any]:
    subject_reference = {
        "direct_pair_position_result_reference": _direct_result_reference(
            source_result
        ),
        "addressed_source_byte_position_coordinate_reference": deepcopy(
            coordinate_reference
        ),
    }
    return {
        "exact_act_identity": identities["determination_act_identity"],
        "subject_reference": subject_reference,
        "determination_act_identity": identities["determination_act_identity"],
        "determination_act_occurrence_identity": identities[
            "determination_act_occurrence_identity"
        ],
        "determination_result_identity": identities[
            "determination_result_identity"
        ],
        "result_boundary_identity": identities["determination_result_identity"],
        "book_clause_identity": BOOK_CLAUSE,
        "direct_pair_position_result_reference": deepcopy(
            subject_reference["direct_pair_position_result_reference"]
        ),
        "addressed_source_byte_position_coordinate_reference": deepcopy(
            coordinate_reference
        ),
        "through_event_occurrence_identity": through_event_occurrence_identity,
        "scope": _scope(
            source_result=source_result,
            coordinate_reference=coordinate_reference,
        ),
        "unknown": list(UNKNOWN),
    }


def _applicability_binding_material(
    *,
    source_result: Event,
    coordinate_reference: dict[str, Any],
    through_event_occurrence_identity: str,
    determination_act_identity: str,
    identities: dict[str, str],
) -> dict[str, Any]:
    subject = {
        "direct_pair_position_result_reference": _direct_result_reference(
            source_result
        ),
        "addressed_source_byte_position_coordinate_reference": deepcopy(
            coordinate_reference
        ),
    }
    return {
        "exact_act_identity": identities["applicability_act_identity"],
        "subject_reference": {
            "subject": subject,
            "addressed_act_identity": determination_act_identity,
        },
        "applicability_act_identity": identities["applicability_act_identity"],
        "applicability_act_occurrence_identity": identities[
            "applicability_act_occurrence_identity"
        ],
        "applicability_result_identity": identities[
            "applicability_result_identity"
        ],
        "addressed_act_identity": determination_act_identity,
        "result_boundary_identity": identities["applicability_result_identity"],
        "book_clause_identity": "01.Current.E.1",
        "direct_pair_position_result_reference": deepcopy(
            subject["direct_pair_position_result_reference"]
        ),
        "addressed_source_byte_position_coordinate_reference": deepcopy(
            coordinate_reference
        ),
        "through_event_occurrence_identity": through_event_occurrence_identity,
        "scope": {
            **_scope(
                source_result=source_result,
                coordinate_reference=coordinate_reference,
            ),
            "addressed_act_identity": determination_act_identity,
        },
        "unknown": list(UNKNOWN),
    }


def record_addressed_byte_occurrence_reference_determination_subject_to_act_binding(
    ledger: EventLedger,
    *,
    direct_result_event_identity: str,
    addressed_source_byte_position_coordinate_reference: dict[str, Any],
    current_coordinates: dict[str, Any],
) -> Event:
    """Bind one exact addressed source coordinate carried by current coordinates."""

    if not isinstance(ledger, EventLedger):
        raise TypeError("determination binding requires one EventLedger")
    source_result, _references = _source(
        ledger,
        result_event_identity=_identity(
            direct_result_event_identity,
            "determination binding requires one direct result",
        ),
        coordinate_reference=addressed_source_byte_position_coordinate_reference,
    )
    current = _require_exact_current_coordinates(
        ledger, source_result=source_result, current_coordinates=current_coordinates
    )
    identities = {
        "determination_act_identity": ledger.mint_identity(
            "addressed_byte_occurrence_reference_determination_measurement_act"
        ),
        "determination_act_occurrence_identity": ledger.mint_identity(
            "addressed_byte_occurrence_reference_determination_measurement_act_occurrence"
        ),
        "determination_result_identity": ledger.mint_identity(
            "addressed_byte_occurrence_reference_determination_measurement_result"
        ),
    }
    if len(set(identities.values())) != len(identities):
        raise AddressedByteOccurrenceReferenceDeterminationError(
            "determination lifecycle identities collapsed"
        )
    source_material = deepcopy(source_result.material)
    source_read, _references_read = _source(
        ledger,
        result_event_identity=source_result.identity,
        coordinate_reference=addressed_source_byte_position_coordinate_reference,
    )
    _require_intact_recorded_occurrence(
        ledger,
        event=source_result,
        kind=BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND,
        material=source_material,
        message="determination binding requires an intact exact source",
    )
    if source_read != source_result:
        raise AddressedByteOccurrenceReferenceDeterminationError(
            "determination binding requires an intact exact source"
        )
    _require_stage_at_append_tip(
        ledger,
        event=ledger.get(current["through_event_occurrence_identity"]),
        message="determination binding coordinates left the current append boundary",
    )
    return ledger.append(
        DETERMINATION_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
        _determination_binding_material(
            source_result=source_result,
            coordinate_reference=(
                addressed_source_byte_position_coordinate_reference
            ),
            through_event_occurrence_identity=current[
                "through_event_occurrence_identity"
            ],
            identities=identities,
        ),
        locality_identity=source_result.locality_identity,
    )


def _read_binding(
    ledger: EventLedger,
    event_identity: str,
    *,
    prior_coordinates: dict[str, Any] | None = None,
) -> tuple[
    Event,
    Event,
    tuple[ReferenceToRecordedPositionOfBytePairOccurrence, ...],
]:
    event = ledger.get(event_identity)
    if (
        event is None
        or event.kind
        not in {
            DETERMINATION_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
            APPLICABILITY_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
        }
        or event.exact_material is not None
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise AddressedByteOccurrenceReferenceDeterminationError(
            "determination binding is absent or corrupted"
        )
    material = event.material
    source_reference = material.get("direct_pair_position_result_reference")
    coordinate_reference = material.get(
        "addressed_source_byte_position_coordinate_reference"
    )
    source_identity = (
        source_reference.get("recorded_occurrence_identity")
        if type(source_reference) is dict
        else None
    )
    source_result, references = _source(
        ledger,
        result_event_identity=source_identity,
        coordinate_reference=coordinate_reference,
    )
    identity_coordinates = (
        _DETERMINATION_IDENTITY_COORDINATES
        if event.kind == DETERMINATION_SUBJECT_TO_ACT_BINDING_RECORDED_KIND
        else _APPLICABILITY_IDENTITY_COORDINATES
    )
    identities = {key: material.get(key) for key in identity_coordinates}
    through_occurrence = material.get("through_event_occurrence_identity")
    if event.kind == DETERMINATION_SUBJECT_TO_ACT_BINDING_RECORDED_KIND:
        expected = _determination_binding_material(
            source_result=source_result,
            coordinate_reference=coordinate_reference,
            through_event_occurrence_identity=through_occurrence,
            identities=identities,
        )
    else:
        expected = _applicability_binding_material(
            source_result=source_result,
            coordinate_reference=coordinate_reference,
            through_event_occurrence_identity=through_occurrence,
            determination_act_identity=material.get("addressed_act_identity"),
            identities=identities,
        )
    if (
        event.locality_identity != source_result.locality_identity
        or any(type(value) is not str or not value for value in identities.values())
        or len(set(identities.values())) != len(identities)
        or type(through_occurrence) is not str
        or not through_occurrence
        or material != expected
    ):
        raise AddressedByteOccurrenceReferenceDeterminationError(
            "determination binding coordinates are not exact"
        )
    if prior_coordinates is None:
        from seed_runtime.operator_current_coordinates import (
            read_operator_current_coordinates_through,
        )

        prior_coordinates = read_operator_current_coordinates_through(
            ledger,
            locality_identity=source_result.locality_identity,
            through_event_occurrence_identity=through_occurrence,
        )
    _current_coordinates_carry_source(
        ledger,
        current_coordinates=prior_coordinates,
        source_result=source_result,
        required_boundary_identity=through_occurrence,
    )
    try:
        ledger.occurrences_in_append_order(
            (through_occurrence, event.identity),
            locality_identity=event.locality_identity,
        )
    except ValueError as error:
        raise AddressedByteOccurrenceReferenceDeterminationError(
            "determination binding has false through-occurrence order"
        ) from error
    return event, source_result, references


def get_addressed_byte_occurrence_reference_determination_subject_to_act_binding(
    ledger: EventLedger, event_identity: str
) -> Event:
    return _read_binding(ledger, event_identity)[0]


def _determination_binding_addressed_by_applicability(
    ledger: EventLedger,
    applicability_binding: Event,
    source_result: Event,
    references: tuple[ReferenceToRecordedPositionOfBytePairOccurrence, ...],
    *,
    prior_coordinates: dict[str, Any] | None = None,
) -> Event:
    addressed_act_identity = applicability_binding.material.get(
        "addressed_act_identity"
    )
    matches = tuple(
        event
        for event in ledger.iter_locality_kind(
            applicability_binding.locality_identity,
            DETERMINATION_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
        )
        if event.material.get("exact_act_identity") == addressed_act_identity
    )
    if len(matches) != 1:
        raise AddressedByteOccurrenceReferenceDeterminationError(
            "Applicability addresses no exact determination binding"
        )
    determination_binding, read_source, read_references = _read_binding(
        ledger,
        matches[0].identity,
        prior_coordinates=prior_coordinates,
    )
    if read_source != source_result or read_references != references:
        raise AddressedByteOccurrenceReferenceDeterminationError(
            "Applicability addresses other determination subjects"
        )
    return determination_binding


def _require_stage_current_coordinates(
    ledger: EventLedger,
    *,
    current_coordinates: dict[str, Any],
    source_result: Event,
    binding: Event,
    applicability_result: Event | None = None,
) -> None:
    current = _require_exact_current_coordinates(
        ledger, source_result=source_result, current_coordinates=current_coordinates
    )
    bindings = current.get("subject_to_act_binding_occurrences")
    applicability = current.get("applicability_result_occurrences")
    required_tip = binding.identity
    if applicability_result is not None:
        required_tip = applicability_result.identity
    if (
        type(bindings) is not dict
        or bindings.get(binding.identity, object()) is not None
        or current.get("through_event_occurrence_identity") != required_tip
        or (
            applicability_result is not None
            and (
                type(applicability) is not dict
                or applicability.get(applicability_result.identity, object())
                is not None
            )
        )
    ):
        raise AddressedByteOccurrenceReferenceDeterminationError(
            "current coordinates carry no exact determination stage"
        )


def _refuse_existing_act(
    ledger: EventLedger,
    *,
    binding: Event,
    kind: str,
    occurrence_coordinate: str,
) -> None:
    occurrence_identity = binding.material[occurrence_coordinate]
    for event in ledger.iter_locality_kind(binding.locality_identity, kind):
        if (
            event.material.get(occurrence_coordinate) == occurrence_identity
            or (
                type(event.material.get("subject_to_act_binding_reference"))
                is dict
                and event.material["subject_to_act_binding_reference"].get(
                    "recorded_occurrence_identity"
                )
                == binding.identity
            )
        ):
            raise AddressedByteOccurrenceReferenceDeterminationError(
                "determination binding already carries this Act"
            )


def _applicability_act_material(
    *, binding: Event, source_result: Event
) -> dict[str, Any]:
    return {
        "applicability_act_identity": binding.material[
            "applicability_act_identity"
        ],
        "applicability_act_occurrence_identity": binding.material[
            "applicability_act_occurrence_identity"
        ],
        "act": APPLICABILITY_ACT,
        "subject_to_act_binding_reference": _binding_reference(
            binding,
            result_boundary_identity=binding.material[
                "applicability_result_identity"
            ],
        ),
        "direct_pair_position_result_reference": _direct_result_reference(
            source_result
        ),
        "addressed_source_byte_position_coordinate_reference": deepcopy(
            binding.material[
                "addressed_source_byte_position_coordinate_reference"
            ]
        ),
        "addressed_act_identity": binding.material["addressed_act_identity"],
        "scope": deepcopy(binding.material["scope"]),
        "unknown": list(binding.material["unknown"]),
    }


def record_addressed_byte_occurrence_reference_determination_applicability_act_occurrence(
    ledger: EventLedger,
    *,
    binding_event_identity: str,
    binding_current_coordinates: dict[str, Any],
) -> Event:
    determination_binding, source_result, references = _read_binding(
        ledger, binding_event_identity
    )
    if (
        determination_binding.kind
        != DETERMINATION_SUBJECT_TO_ACT_BINDING_RECORDED_KIND
    ):
        raise AddressedByteOccurrenceReferenceDeterminationError(
            "Applicability requires the governed determination binding"
        )
    _require_stage_current_coordinates(
        ledger,
        current_coordinates=binding_current_coordinates,
        source_result=source_result,
        binding=determination_binding,
    )
    determination_binding_material = deepcopy(determination_binding.material)
    source_material = deepcopy(source_result.material)
    _refuse_existing_act(
        ledger,
        binding=determination_binding,
        kind=DETERMINATION_ACT_OCCURRENCE_EVENT,
        occurrence_coordinate="determination_act_occurrence_identity",
    )
    source_read, _references_read = _source(
        ledger,
        result_event_identity=source_result.identity,
        coordinate_reference=determination_binding.material[
            "addressed_source_byte_position_coordinate_reference"
        ],
    )
    _require_intact_recorded_occurrence(
        ledger,
        event=source_result,
        kind=BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND,
        material=source_material,
        message="Applicability Act requires an intact exact source",
    )
    _require_intact_recorded_occurrence(
        ledger,
        event=determination_binding,
        kind=DETERMINATION_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
        material=determination_binding_material,
        message="Applicability Act requires an intact exact determination binding",
    )
    if source_read != source_result:
        raise AddressedByteOccurrenceReferenceDeterminationError(
            "Applicability Act requires an intact exact source"
        )
    _require_stage_at_append_tip(
        ledger,
        event=determination_binding,
        message="determination binding left the current append boundary",
    )
    identities = {
        "applicability_act_identity": ledger.mint_identity(
            "addressed_byte_occurrence_reference_applicability_act"
        ),
        "applicability_act_occurrence_identity": ledger.mint_identity(
            "addressed_byte_occurrence_reference_applicability_act_occurrence"
        ),
        "applicability_result_identity": ledger.mint_identity(
            "addressed_byte_occurrence_reference_applicability_result"
        ),
    }
    applicability_binding = ledger.append(
        APPLICABILITY_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
        _applicability_binding_material(
            source_result=source_result,
            coordinate_reference=determination_binding.material[
                "addressed_source_byte_position_coordinate_reference"
            ],
            through_event_occurrence_identity=determination_binding.identity,
            determination_act_identity=determination_binding.material[
                "determination_act_identity"
            ],
            identities=identities,
        ),
        locality_identity=determination_binding.locality_identity,
    )
    return ledger.append(
        APPLICABILITY_ACT_OCCURRENCE_EVENT,
        _applicability_act_material(
            binding=applicability_binding, source_result=source_result
        ),
        locality_identity=determination_binding.locality_identity,
    )


def _read_applicability_act(
    ledger: EventLedger,
    event_identity: str,
    *,
    prior_coordinates: dict[str, Any] | None = None,
) -> tuple[
    Event,
    Event,
    Event,
    Event,
    Event,
    tuple[ReferenceToRecordedPositionOfBytePairOccurrence, ...],
]:
    event = ledger.get(event_identity)
    if (
        event is None
        or event.kind != APPLICABILITY_ACT_OCCURRENCE_EVENT
        or event.exact_material is not None
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise AddressedByteOccurrenceReferenceDeterminationError(
            "determination Applicability Act occurrence is absent or corrupted"
        )
    reference = event.material.get("subject_to_act_binding_reference")
    binding_identity = (
        reference.get("recorded_occurrence_identity")
        if type(reference) is dict
        else None
    )
    applicability_binding, source_result, references = _read_binding(
        ledger, binding_identity, prior_coordinates=prior_coordinates
    )
    if (
        applicability_binding.kind
        != APPLICABILITY_SUBJECT_TO_ACT_BINDING_RECORDED_KIND
    ):
        raise AddressedByteOccurrenceReferenceDeterminationError(
            "Applicability Act carries no exact Applicability binding"
        )
    determination_binding = _determination_binding_addressed_by_applicability(
        ledger,
        applicability_binding,
        source_result,
        references,
        prior_coordinates=prior_coordinates,
    )
    if (
        reference != _binding_reference(
            applicability_binding,
            result_boundary_identity=applicability_binding.material[
                "applicability_result_identity"
            ],
        )
        or event.locality_identity != applicability_binding.locality_identity
        or event.material
        != _applicability_act_material(
            binding=applicability_binding, source_result=source_result
        )
    ):
        raise AddressedByteOccurrenceReferenceDeterminationError(
            "determination Applicability Act occurrence is not exact"
        )
    try:
        ledger.occurrences_in_append_order(
            (applicability_binding.identity, event.identity),
            locality_identity=event.locality_identity,
        )
    except ValueError as error:
        raise AddressedByteOccurrenceReferenceDeterminationError(
            "determination Applicability Act order is false"
        ) from error
    return event, applicability_binding, determination_binding, source_result, references


def get_addressed_byte_occurrence_reference_determination_applicability_act_occurrence(
    ledger: EventLedger, event_identity: str
) -> Event:
    return _read_applicability_act(ledger, event_identity)[0]


def _applicability_finding(
    *,
    applicability_binding: Event,
    determination_binding: Event,
    source_result: Event,
) -> dict[str, Any]:
    coordinate = applicability_binding.material[
        "addressed_source_byte_position_coordinate_reference"
    ]
    return {
        "first_subject": {
            "direct_pair_position_result_reference": _direct_result_reference(
                source_result
            ),
            "addressed_source_byte_position_coordinate_reference": deepcopy(
                coordinate
            ),
        },
        "relation": "applicable_to",
        "second_subject": {
            "exact_act": DETERMINATION_ACT,
            "act_identity": determination_binding.material["determination_act_identity"],
            "act_occurrence_identity": determination_binding.material[
                "determination_act_occurrence_identity"
            ],
            "result_identity": determination_binding.material[
                "determination_result_identity"
            ],
        },
        "source_material_result_occurrence_identity": coordinate[
            "source_material_result_occurrence_identity"
        ],
        "locality_identity": coordinate["locality_identity"],
        "completeness_boundary_identity": coordinate[
            "completeness_boundary_identity"
        ],
        "subject_to_act_binding_reference": _binding_reference(
            applicability_binding,
            result_boundary_identity=applicability_binding.material[
                "applicability_result_identity"
            ],
        ),
    }


def _applicability_result_material(
    *,
    act: Event,
    applicability_binding: Event,
    determination_binding: Event,
    source_result: Event,
) -> dict[str, Any]:
    return {
        "result_identity": applicability_binding.material["applicability_result_identity"],
        "exact_act": APPLICABILITY_ACT,
        "applicability_act_identity": applicability_binding.material[
            "applicability_act_identity"
        ],
        "applicability_act_occurrence_identity": applicability_binding.material[
            "applicability_act_occurrence_identity"
        ],
        "addressed_act_identity": determination_binding.material[
            "determination_act_identity"
        ],
        "addressed_act_occurrence_identity": determination_binding.material[
            "determination_act_occurrence_identity"
        ],
        "subject_to_act_binding_reference": _binding_reference(
            applicability_binding,
            result_boundary_identity=applicability_binding.material[
                "applicability_result_identity"
            ],
        ),
        "direct_pair_position_result_reference": _direct_result_reference(
            source_result
        ),
        "addressed_source_byte_position_coordinate_reference": deepcopy(
            applicability_binding.material[
                "addressed_source_byte_position_coordinate_reference"
            ]
        ),
        "applicability_finding": _applicability_finding(
            applicability_binding=applicability_binding,
            determination_binding=determination_binding,
            source_result=source_result,
        ),
        "scope": deepcopy(applicability_binding.material["scope"]),
        "unknown": list(applicability_binding.material["unknown"]),
    }


def _refuse_existing_result(
    ledger: EventLedger,
    *,
    act: Event,
    result_kind: str,
    occurrence_coordinate: str,
) -> None:
    occurrence_identity = act.material[occurrence_coordinate]
    for event in ledger.iter_locality_kind(
        act.locality_identity, RECORDED_YIELD_RELATION_EVENT
    ):
        if (
            event.material.get("act_occurrence_event_identity") == act.identity
            or event.material.get("dimensions", {}).get("act_occurrence_identity")
            == occurrence_identity
        ):
            raise AddressedByteOccurrenceReferenceDeterminationError(
                "determination Act already carries a Yield"
            )
    for event in ledger.iter_locality_kind(act.locality_identity, result_kind):
        if (
            event.material.get("act_occurrence_event_identity") == act.identity
            or event.material.get(occurrence_coordinate) == occurrence_identity
        ):
            raise AddressedByteOccurrenceReferenceDeterminationError(
                "determination Act already carries a result"
            )


def _prepare_result_yield(
    ledger: EventLedger,
    *,
    act: Event,
    occurrence_coordinate: str,
    result_event_kind: str,
) -> None:
    _refuse_existing_result(
        ledger,
        act=act,
        result_kind=result_event_kind,
        occurrence_coordinate=occurrence_coordinate,
    )
    if ledger.append_boundary_through_occurrence(act.identity) != ledger.append_boundary():
        raise AddressedByteOccurrenceReferenceDeterminationError(
            "determination result requires its exact Act at the current append boundary"
        )


def _require_yield_at_append_tip(ledger: EventLedger, yield_relation: Event) -> None:
    if (
        ledger.get(yield_relation.identity) != yield_relation
        or yield_relation.kind != RECORDED_YIELD_RELATION_EVENT
        or ledger.integrity_of(yield_relation.identity) == CORRUPTED
        or ledger.append_boundary_through_occurrence(yield_relation.identity)
        != ledger.append_boundary()
    ):
        raise AddressedByteOccurrenceReferenceDeterminationError(
            "determination result requires exact Yield relation at the current append boundary"
        )


def _record_applicability_yield_relation(
    ledger: EventLedger,
    *,
    act: Event,
    material: dict[str, Any],
) -> Event:
    return _record_yield_relation(
        ledger,
        locality_identity=act.locality_identity,
        exact_act=APPLICABILITY_ACT,
        act_occurrence_identity=act.material[
            "applicability_act_occurrence_identity"
        ],
        act_occurrence_event_identity=act.identity,
        result_kind=APPLICABILITY_YIELD_RESULT_KIND,
        result_identity=material["result_identity"],
        result_content=material,
        occurrence_boundary=(
            "addressed_byte_occurrence_reference_determination_applicability"
        ),
        responsible_act_occurrence_coordinate=(
            "applicability_act_occurrence_identity"
        ),
    )


def _record_determination_yield_relation(
    ledger: EventLedger,
    *,
    act: Event,
    material: dict[str, Any],
) -> Event:
    return _record_yield_relation(
        ledger,
        locality_identity=act.locality_identity,
        exact_act=DETERMINATION_ACT,
        act_occurrence_identity=act.material[
            "determination_act_occurrence_identity"
        ],
        act_occurrence_event_identity=act.identity,
        result_kind=DETERMINATION_YIELD_RESULT_KIND,
        result_identity=material["result_identity"],
        result_content=material,
        occurrence_boundary="addressed_byte_occurrence_reference_determination",
        responsible_act_occurrence_coordinate=(
            "determination_act_occurrence_identity"
        ),
    )


def _recorded_applicability_result_material(
    material: dict[str, Any], *, act: Event, yield_relation: Event
) -> dict[str, Any]:
    return {
        "result_identity": material["result_identity"],
        "exact_act": material["exact_act"],
        "applicability_act_identity": material["applicability_act_identity"],
        "applicability_act_occurrence_identity": material[
            "applicability_act_occurrence_identity"
        ],
        "addressed_act_identity": material["addressed_act_identity"],
        "addressed_act_occurrence_identity": material[
            "addressed_act_occurrence_identity"
        ],
        "subject_to_act_binding_reference": deepcopy(
            material["subject_to_act_binding_reference"]
        ),
        "direct_pair_position_result_reference": deepcopy(
            material["direct_pair_position_result_reference"]
        ),
        "addressed_source_byte_position_coordinate_reference": deepcopy(
            material["addressed_source_byte_position_coordinate_reference"]
        ),
        "applicability_finding": deepcopy(material["applicability_finding"]),
        "scope": deepcopy(material["scope"]),
        "unknown": list(material["unknown"]),
        "act_occurrence_event_identity": act.identity,
        "yield_relation_identity": yield_relation.identity,
    }


def record_addressed_byte_occurrence_reference_determination_applicability_result(
    ledger: EventLedger,
    *,
    applicability_act_occurrence_event_identity: str,
) -> Event:
    (
        act,
        applicability_binding,
        determination_binding,
        source_result,
        _references,
    ) = _read_applicability_act(
        ledger, applicability_act_occurrence_event_identity
    )
    material = _applicability_result_material(
        act=act,
        applicability_binding=applicability_binding,
        determination_binding=determination_binding,
        source_result=source_result,
    )
    act_material = deepcopy(act.material)
    applicability_binding_material = deepcopy(applicability_binding.material)
    determination_binding_material = deepcopy(determination_binding.material)
    source_material = deepcopy(source_result.material)
    _prepare_result_yield(
        ledger,
        act=act,
        occurrence_coordinate="applicability_act_occurrence_identity",
        result_event_kind=APPLICABILITY_RESULT_KIND,
    )
    (
        act_read,
        applicability_binding_read,
        determination_binding_read,
        source_read,
        _references_read,
    ) = (
        _read_applicability_act(ledger, act.identity)
    )
    for recorded, read, kind, material_read, message in (
        (
            act,
            act_read,
            APPLICABILITY_ACT_OCCURRENCE_EVENT,
            act_material,
            "Applicability Yield requires an intact exact Act",
        ),
        (
            applicability_binding,
            applicability_binding_read,
            APPLICABILITY_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
            applicability_binding_material,
            "Applicability Yield requires an intact exact Applicability binding",
        ),
        (
            determination_binding,
            determination_binding_read,
            DETERMINATION_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
            determination_binding_material,
            "Applicability Yield requires an intact exact determination binding",
        ),
        (
            source_result,
            source_read,
            BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND,
            source_material,
            "Applicability Yield requires an intact exact source",
        ),
    ):
        _require_intact_recorded_occurrence(
            ledger,
            event=recorded,
            kind=kind,
            material=material_read,
            message=message,
        )
        if read != recorded:
            raise AddressedByteOccurrenceReferenceDeterminationError(message)
    _require_stage_at_append_tip(
        ledger, event=act, message="Applicability Act left the current append boundary"
    )
    yield_relation = _record_applicability_yield_relation(
        ledger,
        act=act,
        material=material,
    )
    (
        act_read,
        applicability_binding_read,
        determination_binding_read,
        source_read,
        _references_read,
    ) = (
        _read_applicability_act(ledger, act.identity)
    )
    if (
        act_read,
        applicability_binding_read,
        determination_binding_read,
        source_read,
    ) != (
        act,
        applicability_binding,
        determination_binding,
        source_result,
    ):
        raise AddressedByteOccurrenceReferenceDeterminationError(
            "Applicability result requires an intact exact stage"
        )
    for recorded, kind, material_read, message in (
        (
            act,
            APPLICABILITY_ACT_OCCURRENCE_EVENT,
            act_material,
            "Applicability result requires an intact exact Act",
        ),
        (
            applicability_binding,
            APPLICABILITY_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
            applicability_binding_material,
            "Applicability result requires an intact exact Applicability binding",
        ),
        (
            determination_binding,
            DETERMINATION_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
            determination_binding_material,
            "Applicability result requires an intact exact determination binding",
        ),
        (
            source_result,
            BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND,
            source_material,
            "Applicability result requires an intact exact source",
        ),
    ):
        _require_intact_recorded_occurrence(
            ledger,
            event=recorded,
            kind=kind,
            material=material_read,
            message=message,
        )
    _require_yield_at_append_tip(ledger, yield_relation)
    return ledger.append(
        APPLICABILITY_RESULT_KIND,
        _recorded_applicability_result_material(
            material, act=act, yield_relation=yield_relation
        ),
        locality_identity=act.locality_identity,
    )


def _require_yield(
    ledger: EventLedger,
    *,
    event: Event,
    act: Event,
    occurrence_coordinate: str,
    occurrence_boundary: str,
    result_kind: str,
) -> None:
    yield_relation_identity = event.material.get("yield_relation_identity")
    yield_relation = ledger.get(yield_relation_identity)
    try:
        requirements = read_requirements_of_yield_relation(
            ledger,
            recorded_result_event_identity=event.identity,
            yield_relation_event_identity=yield_relation_identity,
            act_occurrence_event_identity=act.identity,
            recorded_result_occurrence_coordinate=occurrence_coordinate,
            responsible_act_occurrence_coordinate=occurrence_coordinate,
        )
    except (TypeError, ValueError):
        requirements = {}
    if (
        yield_relation is None
        or yield_relation.kind != RECORDED_YIELD_RELATION_EVENT
        or yield_relation.locality_identity != event.locality_identity
        or ledger.integrity_of(yield_relation.identity) == CORRUPTED
        or yield_relation.material.get("occurrence_boundary") != occurrence_boundary
        or yield_relation.material.get("result_kind") != result_kind
        or not all(requirements.values())
    ):
        raise AddressedByteOccurrenceReferenceDeterminationError(
            "determination result carries no exact Yield"
        )
    try:
        ordered = ledger.occurrences_in_append_order(
            (act.identity, yield_relation.identity, event.identity),
            locality_identity=event.locality_identity,
        )
    except ValueError as error:
        raise AddressedByteOccurrenceReferenceDeterminationError(
            "determination result occurrence order is false"
        ) from error
    if tuple(item.identity for item in ordered) != (
        act.identity,
        yield_relation.identity,
        event.identity,
    ):
        raise AddressedByteOccurrenceReferenceDeterminationError(
            "determination result occurrence order is false"
        )


def _read_applicability_result(
    ledger: EventLedger,
    event_identity: str,
    *,
    prior_coordinates: dict[str, Any] | None = None,
) -> tuple[
    Event,
    Event,
    Event,
    Event,
    Event,
    tuple[ReferenceToRecordedPositionOfBytePairOccurrence, ...],
]:
    event = ledger.get(event_identity)
    if (
        event is None
        or event.kind != APPLICABILITY_RESULT_KIND
        or event.exact_material is not None
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise AddressedByteOccurrenceReferenceDeterminationError(
            "determination Applicability result is absent or corrupted"
        )
    (
        act,
        applicability_binding,
        determination_binding,
        source_result,
        references,
    ) = _read_applicability_act(
            ledger,
            event.material.get("act_occurrence_event_identity"),
            prior_coordinates=prior_coordinates,
        )
    expected = {
        **_applicability_result_material(
            act=act,
            applicability_binding=applicability_binding,
            determination_binding=determination_binding,
            source_result=source_result,
        ),
        "act_occurrence_event_identity": act.identity,
        "yield_relation_identity": event.material.get(
            "yield_relation_identity"
        ),
    }
    if event.locality_identity != act.locality_identity or event.material != expected:
        raise AddressedByteOccurrenceReferenceDeterminationError(
            "determination Applicability result coordinates are not exact"
        )
    _require_yield(
        ledger,
        event=event,
        act=act,
        occurrence_coordinate="applicability_act_occurrence_identity",
        occurrence_boundary=APPLICABILITY_BOUNDARY,
        result_kind=APPLICABILITY_YIELD_RESULT_KIND,
    )
    return (
        event,
        act,
        applicability_binding,
        determination_binding,
        source_result,
        references,
    )


def get_recorded_addressed_byte_occurrence_reference_determination_applicability(
    ledger: EventLedger, event_identity: str
) -> dict[str, Any]:
    return deepcopy(_read_applicability_result(ledger, event_identity)[0].material)


def _determination_act_material(
    *, binding: Event, source_result: Event, applicability_result: Event
) -> dict[str, Any]:
    return {
        "determination_act_identity": binding.material[
            "determination_act_identity"
        ],
        "determination_act_occurrence_identity": binding.material[
            "determination_act_occurrence_identity"
        ],
        "act": DETERMINATION_ACT,
        "subject_to_act_binding_reference": _binding_reference(
            binding,
            result_boundary_identity=binding.material[
                "determination_result_identity"
            ],
        ),
        "applicability_result_reference": _applicability_result_reference(
            applicability_result
        ),
        "direct_pair_position_result_reference": _direct_result_reference(
            source_result
        ),
        "addressed_source_byte_position_coordinate_reference": deepcopy(
            binding.material[
                "addressed_source_byte_position_coordinate_reference"
            ]
        ),
        "result_identity": binding.material["determination_result_identity"],
        "scope": deepcopy(binding.material["scope"]),
        "unknown": list(binding.material["unknown"]),
    }


def record_addressed_byte_occurrence_reference_determination_act_occurrence(
    ledger: EventLedger,
    *,
    applicability_result_event_identity: str,
    current_coordinates: dict[str, Any],
) -> Event:
    (
        applicability,
        app_act,
        applicability_binding,
        determination_binding,
        source_result,
        _references,
    ) = (
        _read_applicability_result(ledger, applicability_result_event_identity)
    )
    _require_stage_current_coordinates(
        ledger,
        current_coordinates=current_coordinates,
        source_result=source_result,
        binding=determination_binding,
        applicability_result=applicability,
    )
    applicability_material = deepcopy(applicability.material)
    app_act_material = deepcopy(app_act.material)
    determination_binding_material = deepcopy(determination_binding.material)
    source_material = deepcopy(source_result.material)
    _refuse_existing_act(
        ledger,
        binding=determination_binding,
        kind=DETERMINATION_ACT_OCCURRENCE_EVENT,
        occurrence_coordinate="determination_act_occurrence_identity",
    )
    (
        applicability_read,
        app_act_read,
        applicability_binding_read,
        determination_binding_read,
        source_read,
        _references_read,
    ) = _read_applicability_result(ledger, applicability.identity)
    for recorded, read, kind, material_read, message in (
        (
            applicability,
            applicability_read,
            APPLICABILITY_RESULT_KIND,
            applicability_material,
            "determination Measurement Act requires an intact exact Applicability",
        ),
        (
            app_act,
            app_act_read,
            APPLICABILITY_ACT_OCCURRENCE_EVENT,
            app_act_material,
            "determination Measurement Act requires an intact exact Applicability Act",
        ),
        (
            applicability_binding,
            applicability_binding_read,
            APPLICABILITY_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
            deepcopy(applicability_binding.material),
            "determination Measurement Act requires an intact exact Applicability binding",
        ),
        (
            determination_binding,
            determination_binding_read,
            DETERMINATION_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
            determination_binding_material,
            "determination Measurement Act requires an intact exact binding",
        ),
        (
            source_result,
            source_read,
            BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND,
            source_material,
            "determination Measurement Act requires an intact exact source",
        ),
    ):
        _require_intact_recorded_occurrence(
            ledger,
            event=recorded,
            kind=kind,
            material=material_read,
            message=message,
        )
        if read != recorded:
            raise AddressedByteOccurrenceReferenceDeterminationError(message)
    _require_stage_at_append_tip(
        ledger,
        event=applicability,
        message="determination Measurement Applicability left the current append boundary",
    )
    return ledger.append(
        DETERMINATION_ACT_OCCURRENCE_EVENT,
        _determination_act_material(
            binding=determination_binding,
            source_result=source_result,
            applicability_result=applicability,
        ),
        locality_identity=determination_binding.locality_identity,
    )


def _read_determination_act(
    ledger: EventLedger,
    event_identity: str,
    *,
    prior_coordinates: dict[str, Any] | None = None,
) -> tuple[
    Event,
    Event,
    Event,
    Event,
    tuple[ReferenceToRecordedPositionOfBytePairOccurrence, ...],
]:
    event = ledger.get(event_identity)
    if (
        event is None
        or event.kind != DETERMINATION_ACT_OCCURRENCE_EVENT
        or event.exact_material is not None
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise AddressedByteOccurrenceReferenceDeterminationError(
            "determination Act occurrence is absent or corrupted"
        )
    applicability_reference = event.material.get("applicability_result_reference")
    applicability_identity = (
        applicability_reference.get("recorded_occurrence_identity")
        if type(applicability_reference) is dict
        else None
    )
    (
        applicability,
        _app_act,
        _applicability_binding,
        determination_binding,
        source_result,
        references,
    ) = (
        _read_applicability_result(
            ledger, applicability_identity, prior_coordinates=prior_coordinates
        )
    )
    if (
        applicability_reference != _applicability_result_reference(applicability)
        or event.locality_identity != determination_binding.locality_identity
        or event.material
        != _determination_act_material(
            binding=determination_binding,
            source_result=source_result,
            applicability_result=applicability,
        )
    ):
        raise AddressedByteOccurrenceReferenceDeterminationError(
            "determination Act occurrence coordinates are not exact"
        )
    try:
        ledger.occurrences_in_append_order(
            (applicability.identity, event.identity),
            locality_identity=event.locality_identity,
        )
    except ValueError as error:
        raise AddressedByteOccurrenceReferenceDeterminationError(
            "determination Act order is false"
        ) from error
    return event, applicability, determination_binding, source_result, references


def get_addressed_byte_occurrence_reference_determination_act_occurrence(
    ledger: EventLedger, event_identity: str
) -> Event:
    return _read_determination_act(ledger, event_identity)[0]


def _determination_result_material(
    *,
    act: Event,
    applicability: Event,
    binding: Event,
    source_result: Event,
    references: tuple[ReferenceToRecordedPositionOfBytePairOccurrence, ...],
) -> dict[str, Any]:
    return {
        "result_identity": binding.material["determination_result_identity"],
        "exact_act": DETERMINATION_ACT,
        "determination_act_identity": binding.material[
            "determination_act_identity"
        ],
        "determination_act_occurrence_identity": binding.material[
            "determination_act_occurrence_identity"
        ],
        "subject_to_act_binding_reference": _binding_reference(
            binding,
            result_boundary_identity=binding.material[
                "determination_result_identity"
            ],
        ),
        "applicability_result_reference": _applicability_result_reference(
            applicability
        ),
        "direct_pair_position_result_reference": _direct_result_reference(
            source_result
        ),
        "addressed_source_byte_position_coordinate_reference": deepcopy(
            binding.material[
                "addressed_source_byte_position_coordinate_reference"
            ]
        ),
        "completeness_boundary": {
            "identity": binding.material["scope"][
                "completeness_boundary_identity"
            ]
        },
        "ordered_assertion_references": [
            reference.assertion_reference for reference in references
        ],
        "unknown": list(binding.material["unknown"]),
    }


def _recorded_determination_result_material(
    material: dict[str, Any], *, act: Event, yield_relation: Event
) -> dict[str, Any]:
    return {
        "result_identity": material["result_identity"],
        "exact_act": material["exact_act"],
        "determination_act_identity": material["determination_act_identity"],
        "determination_act_occurrence_identity": material[
            "determination_act_occurrence_identity"
        ],
        "subject_to_act_binding_reference": deepcopy(
            material["subject_to_act_binding_reference"]
        ),
        "applicability_result_reference": deepcopy(
            material["applicability_result_reference"]
        ),
        "direct_pair_position_result_reference": deepcopy(
            material["direct_pair_position_result_reference"]
        ),
        "addressed_source_byte_position_coordinate_reference": deepcopy(
            material["addressed_source_byte_position_coordinate_reference"]
        ),
        "completeness_boundary": deepcopy(material["completeness_boundary"]),
        "ordered_assertion_references": deepcopy(
            material["ordered_assertion_references"]
        ),
        "unknown": list(material["unknown"]),
        "act_occurrence_event_identity": act.identity,
        "yield_relation_identity": yield_relation.identity,
    }


def record_addressed_byte_occurrence_reference_determination_result(
    ledger: EventLedger,
    *,
    determination_act_occurrence_event_identity: str,
) -> Event:
    act, applicability, binding, source_result, references = (
        _read_determination_act(
            ledger, determination_act_occurrence_event_identity
        )
    )
    material = _determination_result_material(
        act=act,
        applicability=applicability,
        binding=binding,
        source_result=source_result,
        references=references,
    )
    act_material = deepcopy(act.material)
    applicability_material = deepcopy(applicability.material)
    binding_material = deepcopy(binding.material)
    source_material = deepcopy(source_result.material)
    _prepare_result_yield(
        ledger,
        act=act,
        occurrence_coordinate="determination_act_occurrence_identity",
        result_event_kind=DETERMINATION_RESULT_KIND,
    )
    (
        act_read,
        applicability_read,
        binding_read,
        source_read,
        _references_read,
    ) = _read_determination_act(ledger, act.identity)
    for recorded, read, kind, material_read, message in (
        (
            act,
            act_read,
            DETERMINATION_ACT_OCCURRENCE_EVENT,
            act_material,
            "determination Measurement Yield requires an intact exact Act",
        ),
        (
            applicability,
            applicability_read,
            APPLICABILITY_RESULT_KIND,
            applicability_material,
            "determination Measurement Yield requires an intact exact Applicability",
        ),
        (
            binding,
            binding_read,
            DETERMINATION_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
            binding_material,
            "determination Measurement Yield requires an intact exact binding",
        ),
        (
            source_result,
            source_read,
            BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND,
            source_material,
            "determination Measurement Yield requires an intact exact source",
        ),
    ):
        _require_intact_recorded_occurrence(
            ledger,
            event=recorded,
            kind=kind,
            material=material_read,
            message=message,
        )
        if read != recorded:
            raise AddressedByteOccurrenceReferenceDeterminationError(message)
    _require_stage_at_append_tip(
        ledger,
        event=act,
        message="determination Measurement Act left the current append boundary",
    )
    yield_relation = _record_determination_yield_relation(
        ledger,
        act=act,
        material=material,
    )
    (
        act_read,
        applicability_read,
        binding_read,
        source_read,
        _references_read,
    ) = _read_determination_act(ledger, act.identity)
    if (act_read, applicability_read, binding_read, source_read) != (
        act,
        applicability,
        binding,
        source_result,
    ):
        raise AddressedByteOccurrenceReferenceDeterminationError(
            "determination Measurement result requires an intact exact stage"
        )
    for recorded, kind, material_read, message in (
        (
            act,
            DETERMINATION_ACT_OCCURRENCE_EVENT,
            act_material,
            "determination Measurement result requires an intact exact Act",
        ),
        (
            applicability,
            APPLICABILITY_RESULT_KIND,
            applicability_material,
            "determination Measurement result requires an intact exact Applicability",
        ),
        (
            binding,
            DETERMINATION_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
            binding_material,
            "determination Measurement result requires an intact exact binding",
        ),
        (
            source_result,
            BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND,
            source_material,
            "determination Measurement result requires an intact exact source",
        ),
    ):
        _require_intact_recorded_occurrence(
            ledger,
            event=recorded,
            kind=kind,
            material=material_read,
            message=message,
        )
    _require_yield_at_append_tip(ledger, yield_relation)
    return ledger.append(
        DETERMINATION_RESULT_KIND,
        _recorded_determination_result_material(
            material, act=act, yield_relation=yield_relation
        ),
        locality_identity=act.locality_identity,
    )


def _read_determination_result(
    ledger: EventLedger,
    event_identity: str,
    *,
    prior_coordinates: dict[str, Any] | None = None,
) -> tuple[
    Event,
    Event,
    Event,
    Event,
    Event,
    tuple[ReferenceToRecordedPositionOfBytePairOccurrence, ...],
]:
    event = ledger.get(event_identity)
    if (
        event is None
        or event.kind != DETERMINATION_RESULT_KIND
        or event.exact_material is not None
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise AddressedByteOccurrenceReferenceDeterminationError(
            "determination result is absent or corrupted"
        )
    act, applicability, binding, source_result, references = (
        _read_determination_act(
            ledger,
            event.material.get("act_occurrence_event_identity"),
            prior_coordinates=prior_coordinates,
        )
    )
    expected = {
        **_determination_result_material(
            act=act,
            applicability=applicability,
            binding=binding,
            source_result=source_result,
            references=references,
        ),
        "act_occurrence_event_identity": act.identity,
        "yield_relation_identity": event.material.get(
            "yield_relation_identity"
        ),
    }
    if event.locality_identity != act.locality_identity or event.material != expected:
        raise AddressedByteOccurrenceReferenceDeterminationError(
            "determination result coordinates are not exact"
        )
    _require_yield(
        ledger,
        event=event,
        act=act,
        occurrence_coordinate="determination_act_occurrence_identity",
        occurrence_boundary=DETERMINATION_BOUNDARY,
        result_kind=DETERMINATION_YIELD_RESULT_KIND,
    )
    return event, act, applicability, binding, source_result, references


def get_recorded_addressed_byte_occurrence_reference_determination(
    ledger: EventLedger, event_identity: str
) -> dict[str, Any]:
    return deepcopy(_read_determination_result(ledger, event_identity)[0].material)


def _record_addressed_byte_occurrence_reference_determination_lifecycle_from_carried_current_coordinates(
    ledger: EventLedger,
    *,
    direct_result_event_identity: str,
    addressed_source_byte_position_coordinate_reference: dict[str, Any],
    current_coordinates: dict[str, Any],
    mutate_current_coordinates: bool = False,
) -> tuple[dict[str, Any], Event]:
    """Record one D.2 lifecycle while carrying its exact stage readings."""

    from seed_runtime.operator_current_coordinates import (
        _exact_current_coordinate_additions,
        _record_distinct,
    )

    if not isinstance(ledger, EventLedger):
        raise TypeError("determination lifecycle requires one EventLedger")
    current = (
        current_coordinates
        if mutate_current_coordinates
        else deepcopy(current_coordinates)
    )
    locality_identity = current.get("locality_identity")
    boundary = current.get("through_event_occurrence_identity")
    source_result, references = _source(
        ledger,
        result_event_identity=_identity(
            direct_result_event_identity,
            "determination lifecycle requires one direct result",
        ),
        coordinate_reference=(
            addressed_source_byte_position_coordinate_reference
        ),
    )
    _current_coordinates_carry_source(
        ledger,
        current_coordinates=current,
        source_result=source_result,
        required_boundary_identity=boundary,
    )
    _require_stage_at_append_tip(
        ledger,
        event=ledger.get(boundary),
        message="determination binding coordinates left the current append boundary",
    )
    source_material = deepcopy(source_result.material)
    identities = {
        name: ledger.mint_identity(prefix)
        for name, prefix in (
            (
                "determination_act_identity",
                "addressed_byte_occurrence_reference_determination_measurement_act",
            ),
            (
                "determination_act_occurrence_identity",
                "addressed_byte_occurrence_reference_determination_measurement_act_occurrence",
            ),
            (
                "determination_result_identity",
                "addressed_byte_occurrence_reference_determination_measurement_result",
            ),
        )
    }
    if len(set(identities.values())) != len(identities):
        raise AddressedByteOccurrenceReferenceDeterminationError(
            "determination lifecycle identities collapsed"
        )

    exact_stage_material: list[tuple[Event, str, dict[str, Any]]] = [
        (
            source_result,
            BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND,
            source_material,
        )
    ]

    def require_intact() -> None:
        for event, kind, material in exact_stage_material:
            _require_intact_recorded_occurrence(
                ledger,
                event=event,
                kind=kind,
                material=material,
                message="determination requires each carried stage intact",
            )

    def require_prior_at_current_append_boundary(event: Event) -> None:
        require_intact()
        _require_stage_at_append_tip(
            ledger,
            event=event,
            message="determination carried stage left the current append boundary",
        )

    def carry(event: Event, *, prior: str) -> None:
        bindings = current.get("subject_to_act_binding_occurrences")
        applicability_results = current.get("applicability_result_occurrences")
        measurements = current.get("measurement_occurrences")
        count = current.get("event_count")
        if (
            type(bindings) is not dict
            or type(applicability_results) is not dict
            or type(measurements) is not dict
            or type(count) is not int
            or current.get("through_event_occurrence_identity") != prior
            or event.locality_identity != locality_identity
            or ledger.get(event.identity) != event
            or ledger.integrity_of(event.identity) == CORRUPTED
            or ledger.append_boundary_through_occurrence(event.identity)
            != ledger.append_boundary()
        ):
            raise AddressedByteOccurrenceReferenceDeterminationError(
                "produced determination occurrence is not exact"
            )
        if event.kind in {
            DETERMINATION_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
            APPLICABILITY_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
        }:
            lawful = (
                event.material.get("through_event_occurrence_identity") == prior
                and event.identity not in bindings
            )
        elif event.kind == APPLICABILITY_ACT_OCCURRENCE_EVENT:
            lawful = (
                event.material["subject_to_act_binding_reference"][
                    "recorded_occurrence_identity"
                ]
                == prior
                and prior in bindings
            )
        elif event.kind == APPLICABILITY_RESULT_KIND:
            lawful = (
                event.material.get("act_occurrence_event_identity") == prior
                and event.material["subject_to_act_binding_reference"][
                    "recorded_occurrence_identity"
                ]
                in bindings
                and event.identity not in applicability_results
            )
        elif event.kind == DETERMINATION_ACT_OCCURRENCE_EVENT:
            lawful = (
                event.material["applicability_result_reference"][
                    "recorded_occurrence_identity"
                ]
                == prior
                and prior in applicability_results
            )
        elif event.kind == DETERMINATION_RESULT_KIND:
            lawful = (
                event.material.get("act_occurrence_event_identity") == prior
                and event.identity not in measurements
            )
        else:
            lawful = False
        if not lawful:
            raise AddressedByteOccurrenceReferenceDeterminationError(
                "produced determination occurrence has false current coordinates"
            )
        additions = _exact_current_coordinate_additions(
            current,
            event,
            error_message="produced determination coordinates are not exact",
        )
        if event.kind in {
            DETERMINATION_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
            APPLICABILITY_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
        }:
            bindings[event.identity] = None
        elif event.kind == APPLICABILITY_RESULT_KIND:
            applicability_results[event.identity] = None
        elif event.kind == DETERMINATION_RESULT_KIND:
            measurements[event.identity] = _determination_result_reference(event)
        for key, values in additions.items():
            for value in values:
                _record_distinct(current[key], value)
        current["through_event_occurrence_identity"] = event.identity
        current["event_count"] = count + 1

    determination_binding_material = _determination_binding_material(
        source_result=source_result,
        coordinate_reference=(
            addressed_source_byte_position_coordinate_reference
        ),
        through_event_occurrence_identity=boundary,
        identities=identities,
    )
    require_prior_at_current_append_boundary(ledger.get(boundary))
    determination_binding = ledger.append(
        DETERMINATION_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
        _determination_binding_material(
            source_result=source_result,
            coordinate_reference=(
                addressed_source_byte_position_coordinate_reference
            ),
            through_event_occurrence_identity=boundary,
            identities=identities,
        ),
        locality_identity=locality_identity,
    )
    exact_stage_material.append(
        (
            determination_binding,
            DETERMINATION_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
            determination_binding_material,
        )
    )
    require_intact()
    carry(determination_binding, prior=boundary)

    applicability_identities = {
        name: ledger.mint_identity(prefix)
        for name, prefix in (
            (
                "applicability_act_identity",
                "addressed_byte_occurrence_reference_applicability_act",
            ),
            (
                "applicability_act_occurrence_identity",
                "addressed_byte_occurrence_reference_applicability_act_occurrence",
            ),
            (
                "applicability_result_identity",
                "addressed_byte_occurrence_reference_applicability_result",
            ),
        )
    }
    require_prior_at_current_append_boundary(determination_binding)
    applicability_binding = ledger.append(
        APPLICABILITY_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
        _applicability_binding_material(
            source_result=source_result,
            coordinate_reference=addressed_source_byte_position_coordinate_reference,
            through_event_occurrence_identity=determination_binding.identity,
            determination_act_identity=determination_binding.material[
                "determination_act_identity"
            ],
            identities=applicability_identities,
        ),
        locality_identity=locality_identity,
    )
    applicability_binding_material = _applicability_binding_material(
        source_result=source_result,
        coordinate_reference=addressed_source_byte_position_coordinate_reference,
        through_event_occurrence_identity=determination_binding.identity,
        determination_act_identity=determination_binding.material[
            "determination_act_identity"
        ],
        identities=applicability_identities,
    )
    exact_stage_material.append(
        (
            applicability_binding,
            APPLICABILITY_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
            applicability_binding_material,
        )
    )
    require_intact()
    carry(applicability_binding, prior=determination_binding.identity)

    _refuse_existing_act(
        ledger,
        binding=determination_binding,
        kind=APPLICABILITY_ACT_OCCURRENCE_EVENT,
        occurrence_coordinate="determination_act_occurrence_identity",
    )
    applicability_act_material = _applicability_act_material(
        binding=applicability_binding, source_result=source_result
    )
    require_prior_at_current_append_boundary(applicability_binding)
    applicability_act = ledger.append(
        APPLICABILITY_ACT_OCCURRENCE_EVENT,
        _applicability_act_material(
            binding=applicability_binding,
            source_result=source_result,
        ),
        locality_identity=locality_identity,
    )
    exact_stage_material.append(
        (
            applicability_act,
            APPLICABILITY_ACT_OCCURRENCE_EVENT,
            applicability_act_material,
        )
    )
    require_intact()
    carry(applicability_act, prior=applicability_binding.identity)

    applicability_material = _applicability_result_material(
        act=applicability_act,
        applicability_binding=applicability_binding,
        determination_binding=determination_binding,
        source_result=source_result,
    )
    _prepare_result_yield(
        ledger,
        act=applicability_act,
        occurrence_coordinate="applicability_act_occurrence_identity",
        result_event_kind=APPLICABILITY_RESULT_KIND,
    )
    require_prior_at_current_append_boundary(applicability_act)
    applicability_yield_relation = _record_applicability_yield_relation(
        ledger,
        act=applicability_act,
        material=applicability_material,
    )
    exact_stage_material.append(
        (
            applicability_yield_relation,
            RECORDED_YIELD_RELATION_EVENT,
            deepcopy(applicability_yield_relation.material),
        )
    )
    require_intact()
    _require_yield_at_append_tip(ledger, applicability_yield_relation)
    applicability_recorded = _recorded_applicability_result_material(
        applicability_material,
        act=applicability_act,
        yield_relation=applicability_yield_relation,
    )
    applicability = ledger.append(
        APPLICABILITY_RESULT_KIND,
        _recorded_applicability_result_material(
            applicability_material,
            act=applicability_act,
            yield_relation=applicability_yield_relation,
        ),
        locality_identity=locality_identity,
    )
    exact_stage_material.append(
        (applicability, APPLICABILITY_RESULT_KIND, applicability_recorded)
    )
    require_intact()
    carry(applicability, prior=applicability_act.identity)

    _refuse_existing_act(
        ledger,
        binding=determination_binding,
        kind=DETERMINATION_ACT_OCCURRENCE_EVENT,
        occurrence_coordinate="determination_act_occurrence_identity",
    )
    act_material = _determination_act_material(
        binding=determination_binding,
        source_result=source_result,
        applicability_result=applicability,
    )
    require_prior_at_current_append_boundary(applicability)
    act = ledger.append(
        DETERMINATION_ACT_OCCURRENCE_EVENT,
        _determination_act_material(
            binding=determination_binding,
            source_result=source_result,
            applicability_result=applicability,
        ),
        locality_identity=locality_identity,
    )
    exact_stage_material.append(
        (act, DETERMINATION_ACT_OCCURRENCE_EVENT, act_material)
    )
    require_intact()
    carry(act, prior=applicability.identity)

    result_material = _determination_result_material(
        act=act,
        applicability=applicability,
        binding=determination_binding,
        source_result=source_result,
        references=references,
    )
    _prepare_result_yield(
        ledger,
        act=act,
        occurrence_coordinate="determination_act_occurrence_identity",
        result_event_kind=DETERMINATION_RESULT_KIND,
    )
    require_prior_at_current_append_boundary(act)
    yield_relation = _record_determination_yield_relation(
        ledger,
        act=act,
        material=result_material,
    )
    exact_stage_material.append(
        (
            yield_relation,
            RECORDED_YIELD_RELATION_EVENT,
            deepcopy(yield_relation.material),
        )
    )
    require_intact()
    _require_yield_at_append_tip(ledger, yield_relation)
    result_recorded = _recorded_determination_result_material(
        result_material,
        act=act,
        yield_relation=yield_relation,
    )
    result = ledger.append(
        DETERMINATION_RESULT_KIND,
        _recorded_determination_result_material(
            result_material,
            act=act,
            yield_relation=yield_relation,
        ),
        locality_identity=locality_identity,
    )
    exact_stage_material.append(
        (result, DETERMINATION_RESULT_KIND, result_recorded)
    )
    require_intact()
    carry(result, prior=act.identity)
    return current, result
