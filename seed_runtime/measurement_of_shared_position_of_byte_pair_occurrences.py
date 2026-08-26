"""Compose exact yielded pair-position Assertions at one shared position."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from typing import Any, NamedTuple

from seed_runtime.event import Event
from seed_runtime.events import CORRUPTED, EventLedger
from seed_runtime.yield_relation import (
    RECORDED_YIELD_RELATION_EVENT,
    _record_yield_relation,
    read_requirements_of_yield_relation,
)
from seed_runtime.addressed_byte_occurrence_reference_determination import (
    _determination_result_reference,
    _read_determination_result,
)
from seed_runtime.measurement_of_recurrent_byte_pair_occurrence_position import (
    RECORDED_ACT_OCCURRENCE_OF_MEASUREMENT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_EVENT,
    RECORDED_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_MEASUREMENT_SUBJECT_TO_ACT_BINDING_KIND,
    RECORDING_OCCURRENCE_OF_RESULT_OF_MEASUREMENT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_KIND,
    ReferenceToRecordedRecurrentBytePairOccurrencePosition,
    _references_from_recorded_recurrent_pair_position_result,
    _references_to_addressed_recorded_recurrent_pair_position_results,
    get_recorded_result_of_measurement_of_recurrent_byte_pair_occurrence_position,
    references_to_recorded_recurrent_byte_pair_occurrence_positions,
)
from seed_runtime.measurement_of_position_coordinates_of_byte_pair_occurrences import (
    BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND,
    ReferenceToRecordedPositionOfBytePairOccurrence,
    references_to_addressed_recorded_position_coordinates_of_byte_pair_occurrences,
    references_to_recorded_position_coordinates_of_byte_pair_occurrences,
)


SHARED_POSITION_MEASUREMENT_SUBJECT_TO_ACT_BINDING_RECORDED_KIND = (
    "operator.shared_pair_position.subject_to_act_binding_recorded"
)
SHARED_POSITION_APPLICABILITY_SUBJECT_TO_ACT_BINDING_RECORDED_KIND = (
    "operator.shared_pair_position.applicability_subject_to_act_binding_recorded"
)
SHARED_POSITION_APPLICABILITY_ACT_OCCURRENCE_EVENT = (
    "operator.shared_pair_position.applicability_act_occurrence_recorded"
)
SHARED_POSITION_APPLICABILITY_RESULT_KIND = (
    "operator.shared_pair_position.applicability_recorded"
)
SHARED_POSITION_MEASUREMENT_ACT_OCCURRENCE_EVENT = (
    "operator.shared_pair_position.measurement_act_occurrence_recorded"
)
SHARED_POSITION_MEASUREMENT_RESULT_KIND = (
    "operator.shared_pair_position.measurement_recorded"
)
BOOK_CLAUSE = "01.Source.D"
MEASUREMENT_RULE = (
    "second position-coordinate reference of first exact recorded pair occurrence "
    "Assertion and first position-coordinate reference of second exact recorded pair "
    "occurrence Assertion, each of one exact byte occurrence"
)
APPLICABILITY_ACT = (
    "Applicability of exact pair occurrence position Assertions to one same-position "
    "Measurement"
)
MEASUREMENT_ACT = "Measurement of one same position of exact byte pair occurrences"
APPLICABILITY_RESULT_KIND = "shared pair-position input Applicability result"
MEASUREMENT_RESULT_KIND = "shared pair-position Measurement result"
APPLICABILITY_BOUNDARY = "shared_pair_position_applicability"
MEASUREMENT_BOUNDARY = "shared_pair_position_measurement"
D2_RESULT_REFERENCE_COORDINATE = (
    "addressed_byte_occurrence_reference_determination_result_reference"
)

EVENT_KIND_RESPONSIBILITIES = {
    SHARED_POSITION_MEASUREMENT_SUBJECT_TO_ACT_BINDING_RECORDED_KIND: "01.Source.D",
    SHARED_POSITION_APPLICABILITY_SUBJECT_TO_ACT_BINDING_RECORDED_KIND: "01.Current.E.1",
    SHARED_POSITION_APPLICABILITY_ACT_OCCURRENCE_EVENT: "02.Acts.A",
    SHARED_POSITION_APPLICABILITY_RESULT_KIND: "01.Current.E.1",
    SHARED_POSITION_MEASUREMENT_ACT_OCCURRENCE_EVENT: "02.Acts.A",
    SHARED_POSITION_MEASUREMENT_RESULT_KIND: "01.Source.D",
}
class SharedPairPositionError(ValueError):
    """One shared-position Measurement is incoherent."""


RecordedPairPositionReference = (
    ReferenceToRecordedRecurrentBytePairOccurrencePosition
    | ReferenceToRecordedPositionOfBytePairOccurrence
)


class SharedPairPositionInputs(NamedTuple):
    first: RecordedPairPositionReference
    second: RecordedPairPositionReference

    @property
    def first_relation_second_position_coordinate_reference(self) -> dict[str, Any]:
        return _position_coordinate_reference(self.first, role="second")

    @property
    def second_relation_first_position_coordinate_reference(self) -> dict[str, Any]:
        return _position_coordinate_reference(self.second, role="first")

    @property
    def carries_one_position_coordinate_reference(self) -> bool:
        return (
            self.first_relation_second_position_coordinate_reference
            == self.second_relation_first_position_coordinate_reference
        )

    @property
    def shared_position_coordinate_reference(self) -> dict[str, Any] | None:
        if not self.carries_one_position_coordinate_reference:
            return None
        return self.first_relation_second_position_coordinate_reference


@dataclass(frozen=True)
class _SharedPositionReplayOccurrence:
    event: Event
    kind: str
    material: dict[str, Any]
    exact_material: bytes | None
    locality_identity: str | None


@dataclass
class _SharedPositionReplayReading:
    binding_reading: tuple[Event, SharedPairPositionInputs]
    binding_occurrence: _SharedPositionReplayOccurrence
    input_result_occurrences: tuple[_SharedPositionReplayOccurrence, ...]
    source_occurrences: tuple[_SharedPositionReplayOccurrence, ...]
    pair_measurement_result_occurrences: tuple[_SharedPositionReplayOccurrence, ...]
    subject_to_act_binding_occurrences: tuple[
        _SharedPositionReplayOccurrence, ...
    ]
    act_occurrence_occurrences: tuple[_SharedPositionReplayOccurrence, ...]
    yield_relation_occurrences: tuple[
        _SharedPositionReplayOccurrence, ...
    ]
    applicability_binding_reading: tuple[
        Event, SharedPairPositionInputs
    ] | None = None
    applicability_binding_occurrence: _SharedPositionReplayOccurrence | None = None
    applicability_act_occurrence: _SharedPositionReplayOccurrence | None = None
    applicability_result_occurrence: _SharedPositionReplayOccurrence | None = None
    measurement_act_occurrence: _SharedPositionReplayOccurrence | None = None
    measurement_result_occurrence: _SharedPositionReplayOccurrence | None = None


def _position_coordinate_reference(
    reference: RecordedPairPositionReference,
    *,
    role: str,
) -> dict[str, Any]:
    if type(reference) is ReferenceToRecordedPositionOfBytePairOccurrence:
        if role == "first":
            return reference.first_position_coordinate_reference
        if role == "second":
            return reference.second_position_coordinate_reference
        raise SharedPairPositionError("one exact pair role is required")
    if role == "first":
        position = reference.first_position
        exact_material = reference.exact_pair[:1]
    elif role == "second":
        position = reference.second_position
        exact_material = reference.exact_pair[1:]
    else:
        raise SharedPairPositionError("one exact pair role is required")
    return {
        "source_material_result_occurrence_identity": (
            reference.source_material_result_occurrence_identity
        ),
        "locality_identity": reference.locality_identity,
        "completeness_boundary_identity": (
            reference.completeness_boundary_identity
        ),
        "position": position,
        "exact_material": list(exact_material),
    }


def _identity(value: Any, message: str) -> str:
    if type(value) is not str or not value:
        raise SharedPairPositionError(message)
    return value


def _reference_material(
    reference: RecordedPairPositionReference,
) -> dict[str, Any]:
    material = {
        "recorded_occurrence_identity": reference.recorded_occurrence_identity,
        "assertion_reference": reference.assertion_reference,
        "source_material_result_occurrence_identity": (
            reference.source_material_result_occurrence_identity
        ),
        "locality_identity": reference.locality_identity,
        "completeness_boundary_identity": (
            reference.completeness_boundary_identity
        ),
        "exact_pair": list(reference.exact_pair),
        "first_position": reference.first_position,
        "second_position": reference.second_position,
        "first_position_coordinate_reference": _position_coordinate_reference(
            reference, role="first"
        ),
        "second_position_coordinate_reference": _position_coordinate_reference(
            reference, role="second"
        ),
    }
    if type(reference) is ReferenceToRecordedRecurrentBytePairOccurrencePosition:
        material["support_assertion_references"] = [
            {
                "recorded_occurrence_identity": (
                    reference.pair_measurement_occurrence_identity
                ),
                "assertion_position": reference.recurrence_assertion_position,
            },
            {
                "recorded_occurrence_identity": (
                    reference.pair_measurement_occurrence_identity
                ),
                "assertion_position": reference.count_assertion_position,
            },
        ]
    elif (
        type(reference)
        is ReferenceToRecordedPositionOfBytePairOccurrence
    ):
        material["support_assertion_references"] = []
    else:
        raise SharedPairPositionError(
            "shared-position Measurement requires one exact position Assertion reference"
        )
    return material


def _references(
    ledger: EventLedger,
    *,
    result_occurrence_identity: str,
) -> tuple[RecordedPairPositionReference, ...]:
    result_occurrence_identity = _identity(
        result_occurrence_identity,
        "shared-position Measurement requires one exact result occurrence",
    )
    result = ledger.get(result_occurrence_identity)
    if result is None:
        raise SharedPairPositionError(
            "shared-position Measurement requires one exact result occurrence"
        )
    if (
        result.kind
        == RECORDING_OCCURRENCE_OF_RESULT_OF_MEASUREMENT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_KIND
    ):
        return references_to_recorded_recurrent_byte_pair_occurrence_positions(
            ledger,
            result_occurrence_identity=result_occurrence_identity,
        )
    if result.kind == BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND:
        return references_to_recorded_position_coordinates_of_byte_pair_occurrences(
            ledger,
            result_occurrence_identity,
        )
    raise SharedPairPositionError(
        "shared-position Measurement requires one exact pair-position result"
    )


def _resolve_reference(
    ledger: EventLedger,
    *,
    result_occurrence_identity: str,
    assertion_address: str | int,
) -> RecordedPairPositionReference:
    return _resolve_references(
        ledger,
        result_occurrence_identity=_identity(
            result_occurrence_identity,
            "shared-position Measurement requires one exact result occurrence",
        ),
        assertion_addresses=(assertion_address,),
    )[0]


def _resolve_references(
    ledger: EventLedger,
    *,
    result_occurrence_identity: str,
    assertion_addresses: tuple[str | int, ...],
) -> tuple[RecordedPairPositionReference, ...]:
    result_occurrence_identity = _identity(
        result_occurrence_identity,
        "shared-position Measurement requires one exact result occurrence",
    )
    result = ledger.get(result_occurrence_identity)
    if result is None:
        raise SharedPairPositionError(
            "shared-position Measurement requires one exact result occurrence"
        )
    if result.kind == BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND:
        if any(type(address) is not int or address < 0 for address in assertion_addresses):
            raise SharedPairPositionError(
                "shared-position Measurement requires exact Assertion addresses"
            )
        try:
            return references_to_addressed_recorded_position_coordinates_of_byte_pair_occurrences(
                ledger,
                result_occurrence_identity,
                assertion_addresses,
            )
        except (TypeError, ValueError) as error:
            raise SharedPairPositionError(
                "shared-position Measurement requires carried position Assertions"
            ) from error
    if (
        result.kind
        == RECORDING_OCCURRENCE_OF_RESULT_OF_MEASUREMENT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_KIND
    ):
        try:
            return _references_from_recorded_recurrent_pair_position_result(
                result,
                get_recorded_result_of_measurement_of_recurrent_byte_pair_occurrence_position(
                    ledger, result.identity
                ),
                assertion_positions=assertion_addresses,
            )
        except (TypeError, ValueError) as error:
            raise SharedPairPositionError(
                "shared-position Measurement requires carried position Assertions"
            ) from error
    raise SharedPairPositionError(
        "shared-position Measurement requires one exact pair-position result"
    )


def _inputs(
    ledger: EventLedger,
    *,
    first_result_occurrence_identity: str,
    first_assertion_address: str | int,
    second_result_occurrence_identity: str,
    second_assertion_address: str | int,
    prior_coordinates: dict[str, Any] | None = None,
) -> SharedPairPositionInputs:
    if first_result_occurrence_identity == second_result_occurrence_identity:
        first, second = _resolve_references(
            ledger,
            result_occurrence_identity=second_result_occurrence_identity,
            assertion_addresses=(
                first_assertion_address,
                second_assertion_address,
            ),
        )
    else:
        result_occurrences = tuple(
            ledger.get(identity)
            if type(identity) is str and identity
            else None
            for identity in (
                first_result_occurrence_identity,
                second_result_occurrence_identity,
            )
        )
        if all(
            result is not None
            and result.kind
            == RECORDING_OCCURRENCE_OF_RESULT_OF_MEASUREMENT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_KIND
            for result in result_occurrences
        ):
            first, second = (
                _references_to_addressed_recorded_recurrent_pair_position_results(
                    ledger,
                    result_and_assertion_positions=(
                        (
                            _identity(
                                first_result_occurrence_identity,
                                "shared-position Measurement requires one exact result occurrence",
                            ),
                            first_assertion_address,
                        ),
                        (
                            _identity(
                                second_result_occurrence_identity,
                                "shared-position Measurement requires one exact result occurrence",
                            ),
                            second_assertion_address,
                        ),
                    ),
                    prior_coordinates=prior_coordinates,
                )
            )
            return _validated_inputs(first, second)
        first = _resolve_reference(
            ledger,
            result_occurrence_identity=first_result_occurrence_identity,
            assertion_address=first_assertion_address,
        )
        second = _resolve_reference(
            ledger,
            result_occurrence_identity=second_result_occurrence_identity,
            assertion_address=second_assertion_address,
        )
    return _validated_inputs(first, second)


def _validated_inputs(
    first: RecordedPairPositionReference,
    second: RecordedPairPositionReference,
) -> SharedPairPositionInputs:
    if first.assertion_reference == second.assertion_reference:
        raise SharedPairPositionError(
            "one position Assertion cannot occupy first and second path relations"
        )
    if (
        first.source_material_result_occurrence_identity
        != second.source_material_result_occurrence_identity
        or first.locality_identity != second.locality_identity
        or first.completeness_boundary_identity
        != second.completeness_boundary_identity
    ):
        raise SharedPairPositionError(
            "shared-position inputs require one source occurrence, Locality, and boundary"
        )
    return SharedPairPositionInputs(first=first, second=second)


def _direct_coordinates_from_binding_material(
    material: dict[str, Any],
) -> tuple[bytes, int, int]:
    exact_pair = material.get("exact_pair")
    if (
        type(exact_pair) is not list
        or len(exact_pair) != 2
        or any(
            type(value) is not int or value < 0 or value > 255
            for value in exact_pair
        )
    ):
        raise SharedPairPositionError(
            "shared-position binding carries no exact inputs"
        )
    return (
        bytes(exact_pair),
        material.get("first_position"),
        material.get("second_position"),
    )


def _assertion_address_from_binding_material(
    material: dict[str, Any],
) -> str | int:
    reference = material.get("assertion_reference")
    if (
        type(reference) is not dict
        or reference.get("recorded_occurrence_identity")
        != material.get("recorded_occurrence_identity")
    ):
        raise SharedPairPositionError(
            "shared-position binding carries no exact Assertion address"
        )
    if set(reference) == {"recorded_occurrence_identity", "assertion_identity"}:
        return _identity(
            reference["assertion_identity"],
            "shared-position binding carries no exact Assertion address",
        )
    if (
        set(reference) == {"recorded_occurrence_identity", "assertion_position"}
        and type(reference["assertion_position"]) is int
        and reference["assertion_position"] >= 0
    ):
        return reference["assertion_position"]
    raise SharedPairPositionError(
        "shared-position binding carries no exact Assertion address"
    )


def _inputs_from_binding_material(
    ledger: EventLedger,
    *,
    first: dict[str, Any],
    second: dict[str, Any],
    prior_coordinates: dict[str, Any] | None = None,
) -> SharedPairPositionInputs:
    result_identities = (
        first.get("recorded_occurrence_identity"),
        second.get("recorded_occurrence_identity"),
    )
    results = tuple(
        ledger.get(identity) if type(identity) is str else None
        for identity in result_identities
    )
    if all(
        result is not None and result.kind == BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND
        for result in results
    ):
        materials = (first, second)
        coordinates = tuple(
            _direct_coordinates_from_binding_material(material)
            for material in materials
        )
        assertion_addresses = tuple(
            _assertion_address_from_binding_material(material)
            for material in materials
        )
        try:
            if result_identities[0] == result_identities[1]:
                first_reference, second_reference = (
                    references_to_addressed_recorded_position_coordinates_of_byte_pair_occurrences(
                        ledger,
                        result_identities[0],
                        assertion_addresses,
                        exact_coordinates=coordinates,
                    )
                )
            else:
                first_reference, second_reference = tuple(
                    references_to_addressed_recorded_position_coordinates_of_byte_pair_occurrences(
                        ledger,
                        result_identity,
                        (assertion_identity,),
                        exact_coordinates=(coordinate,),
                    )[0]
                    for result_identity, assertion_identity, coordinate in zip(
                        result_identities,
                        assertion_addresses,
                        coordinates,
                        strict=True,
                    )
                )
        except (TypeError, ValueError) as error:
            raise SharedPairPositionError(
                "shared-position binding carries no exact inputs"
            ) from error
        return _validated_inputs(first_reference, second_reference)
    return _inputs(
        ledger,
        first_result_occurrence_identity=result_identities[0],
        first_assertion_address=_assertion_address_from_binding_material(first),
        second_result_occurrence_identity=result_identities[1],
        second_assertion_address=_assertion_address_from_binding_material(second),
        prior_coordinates=prior_coordinates,
    )


def _require_current_coordinates(
    ledger: EventLedger,
    *,
    inputs: SharedPairPositionInputs,
    current_coordinates: dict[str, Any],
    carried_coordinate: str,
    required_occurrences: tuple[str, ...],
) -> str:
    if type(current_coordinates) is not dict:
        raise SharedPairPositionError(
            "shared-position Measurement requires exact current coordinates"
        )
    carried = current_coordinates.get(carried_coordinate)
    boundary = current_coordinates.get("through_event_occurrence_identity")
    if (
        current_coordinates.get("locality_identity") != inputs.first.locality_identity
        or type(carried) is not dict
        or any(identity not in carried for identity in required_occurrences)
        or type(boundary) is not str
        or not boundary
    ):
        raise SharedPairPositionError(
            "current coordinates lack the exact shared-position inputs"
        )
    ordered = tuple(dict.fromkeys((*required_occurrences, boundary)))
    try:
        resolved = ledger.occurrences_in_append_order(
            ordered,
            locality_identity=inputs.first.locality_identity,
        )
    except (TypeError, ValueError) as error:
        raise SharedPairPositionError(
            "through-occurrence boundary is not after exact shared-position inputs"
        ) from error
    if tuple(event.identity for event in resolved) != ordered:
        raise SharedPairPositionError(
            "through-occurrence boundary is not after exact shared-position inputs"
        )
    return boundary


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


def _binding_material(
    *,
    inputs: SharedPairPositionInputs,
    through_event_occurrence_identity: str,
    identities: dict[str, str],
    determination_result_reference: dict[str, str] | None = None,
) -> dict[str, Any]:
    material = {
        "exact_act_identity": identities["measurement_act_identity"],
        "subject_reference": {
            "first_position_assertion": _reference_material(inputs.first),
            "second_position_assertion": _reference_material(inputs.second),
        },
        "measurement_act_identity": identities["measurement_act_identity"],
        "measurement_act_occurrence_identity": identities[
            "measurement_act_occurrence_identity"
        ],
        "measurement_result_identity": identities[
            "measurement_result_identity"
        ],
        "result_boundary_identity": identities["measurement_result_identity"],
        "book_clause_identity": BOOK_CLAUSE,
        "measurement_rule": MEASUREMENT_RULE,
        "first_position_assertion": _reference_material(inputs.first),
        "second_position_assertion": _reference_material(inputs.second),
        "through_event_occurrence_identity": through_event_occurrence_identity,
        "scope": {
            "locality_identity": inputs.first.locality_identity,
            "source_material_result_occurrence_identity": (
                inputs.first.source_material_result_occurrence_identity
            ),
            "completeness_boundary_identity": (
                inputs.first.completeness_boundary_identity
            ),
        },
        "unknown": [],
    }
    if determination_result_reference is not None:
        material[D2_RESULT_REFERENCE_COORDINATE] = deepcopy(
            determination_result_reference
        )
    return material


def _applicability_binding_material(
    *,
    inputs: SharedPairPositionInputs,
    through_event_occurrence_identity: str,
    measurement_act_identity: str,
    identities: dict[str, str],
    determination_result_reference: dict[str, str] | None = None,
) -> dict[str, Any]:
    first_subject = _reference_material(inputs.first)
    second_subject = _reference_material(inputs.second)
    material = {
        "exact_act_identity": identities["applicability_act_identity"],
        "subject_reference": {
            "first_input": {
                "subject": first_subject,
                "addressed_act_identity": measurement_act_identity,
            },
            "second_input": {
                "subject": second_subject,
                "addressed_act_identity": measurement_act_identity,
            },
        },
        "applicability_act_identity": identities["applicability_act_identity"],
        "applicability_act_occurrence_identity": identities[
            "applicability_act_occurrence_identity"
        ],
        "applicability_result_identity": identities[
            "applicability_result_identity"
        ],
        "addressed_act_identity": measurement_act_identity,
        "result_boundary_identity": identities["applicability_result_identity"],
        "book_clause_identity": "01.Current.E.1",
        "measurement_rule": MEASUREMENT_RULE,
        "first_position_assertion": first_subject,
        "second_position_assertion": second_subject,
        "through_event_occurrence_identity": through_event_occurrence_identity,
        "scope": {
            "locality_identity": inputs.first.locality_identity,
            "source_material_result_occurrence_identity": (
                inputs.first.source_material_result_occurrence_identity
            ),
            "completeness_boundary_identity": (
                inputs.first.completeness_boundary_identity
            ),
            "addressed_act_identity": measurement_act_identity,
        },
        "unknown": [],
    }
    if determination_result_reference is not None:
        material[D2_RESULT_REFERENCE_COORDINATE] = deepcopy(
            determination_result_reference
        )
    return material


_IDENTITY_COORDINATES = (
    "measurement_act_identity",
    "measurement_act_occurrence_identity",
    "measurement_result_identity",
)


def _mint_measurement_identities(ledger: EventLedger) -> dict[str, str]:
    return {
        "measurement_act_identity": ledger.mint_identity(
            "shared_pair_position_measurement_act_identity"
        ),
        "measurement_act_occurrence_identity": ledger.mint_identity(
            "shared_pair_position_measurement_act_occurrence_identity"
        ),
        "measurement_result_identity": ledger.mint_identity(
            "shared_pair_position_measurement_result_identity"
        ),
    }


def _mint_applicability_identities(ledger: EventLedger) -> dict[str, str]:
    return {
        "applicability_act_identity": ledger.mint_identity(
            "shared_pair_position_applicability_act_identity"
        ),
        "applicability_act_occurrence_identity": ledger.mint_identity(
            "shared_pair_position_applicability_act_occurrence_identity"
        ),
        "applicability_result_identity": ledger.mint_identity(
            "shared_pair_position_applicability_result_identity"
        ),
    }


def _record_shared_position_binding(
    ledger: EventLedger,
    *,
    inputs: SharedPairPositionInputs,
    current_coordinates: dict[str, Any],
    required_occurrences: tuple[str, ...],
) -> Event:
    boundary = _require_current_coordinates(
        ledger,
        inputs=inputs,
        current_coordinates=current_coordinates,
        carried_coordinate="measurement_occurrences",
        required_occurrences=required_occurrences,
    )
    identities = _mint_measurement_identities(ledger)
    if len(set(identities.values())) != len(identities):
        raise SharedPairPositionError(
            "shared-position Measurement occurrence identities collapsed"
        )
    return ledger.append(
        SHARED_POSITION_MEASUREMENT_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
        _binding_material(
            inputs=inputs,
            through_event_occurrence_identity=boundary,
            identities=identities,
        ),
        locality_identity=inputs.first.locality_identity,
    )


def _d2_result_inputs(
    ledger: EventLedger,
    *,
    result_event_identity: str,
    prior_coordinates: dict[str, Any],
) -> tuple[Event, SharedPairPositionInputs]:
    try:
        result, _act, _applicability, _assignment, _source, references = (
            _read_determination_result(
                ledger,
                result_event_identity,
                prior_standing=prior_coordinates,
            )
        )
    except (TypeError, ValueError) as error:
        raise SharedPairPositionError(
            "shared-position binding requires one exact D.2 determination result"
        ) from error
    if len(references) != 2:
        raise SharedPairPositionError(
            "shared-position binding requires exactly two ordered D.2 Assertion references"
        )
    try:
        inputs = _validated_inputs(references[0], references[1])
    except (TypeError, ValueError) as error:
        raise SharedPairPositionError(
            "shared-position binding requires exactly two ordered D.2 Assertion references"
        ) from error
    return result, inputs


def _require_exact_d2_result_current_coordinates(
    ledger: EventLedger,
    *,
    result: Event,
    inputs: SharedPairPositionInputs,
    current_coordinates: dict[str, Any],
) -> str:
    measurements = (
        current_coordinates.get("measurement_occurrences")
        if type(current_coordinates) is dict
        else None
    )
    if (
        type(measurements) is not dict
        or measurements.get(result.identity)
        != _determination_result_reference(result)
    ):
        raise SharedPairPositionError(
            "current coordinates carry no exact D.2 determination result"
        )
    return _require_current_coordinates(
        ledger,
        inputs=inputs,
        current_coordinates=current_coordinates,
        carried_coordinate="measurement_occurrences",
        required_occurrences=(result.identity,),
    )


def record_shared_position_subject_to_act_binding_from_addressed_byte_occurrence_reference_determination_result(
    ledger: EventLedger,
    *,
    determination_result_event_identity: str,
    current_coordinates: dict[str, Any],
) -> Event:
    """Bind the two ordered Assertions carried by one current D.2 result."""

    result_identity = _identity(
        determination_result_event_identity,
        "shared-position binding requires one exact D.2 determination result",
    )
    current = current_coordinates
    result, inputs = _d2_result_inputs(
        ledger,
        result_event_identity=result_identity,
        prior_coordinates=current,
    )
    boundary = current.get("through_event_occurrence_identity")
    boundary_event = ledger.get(boundary) if type(boundary) is str else None
    if (
        current != current_coordinates
        or current.get("locality_identity") != result.locality_identity
        or boundary_event is None
        or boundary_event.locality_identity != result.locality_identity
        or ledger.integrity_of(boundary_event.identity) == CORRUPTED
        or ledger.append_boundary_through_occurrence(boundary_event.identity)
        != ledger.append_boundary()
    ):
        raise SharedPairPositionError(
            "shared-position binding requires exact current coordinates"
        )
    result, inputs = _d2_result_inputs(
        ledger,
        result_event_identity=result_identity,
        prior_coordinates=current,
    )
    result_material = deepcopy(result.material)
    current_boundary = current.get("through_event_occurrence_identity")
    carried_result_reference = deepcopy(
        current.get("measurement_occurrences", {}).get(result.identity)
    )
    boundary = _require_exact_d2_result_current_coordinates(
        ledger,
        result=result,
        inputs=inputs,
        current_coordinates=current,
    )
    identities = _mint_measurement_identities(ledger)
    if len(set(identities.values())) != len(identities):
        raise SharedPairPositionError(
            "shared-position Measurement occurrence identities collapsed"
        )

    result_read, inputs_read = _d2_result_inputs(
        ledger,
        result_event_identity=result_identity,
        prior_coordinates=current,
    )
    boundary_event = ledger.get(boundary)
    if (
        result_read != result
        or result.material != result_material
        or inputs_read != inputs
        or current.get("through_event_occurrence_identity") != current_boundary
        or current_boundary != boundary
        or boundary_event is None
        or ledger.integrity_of(boundary_event.identity) == CORRUPTED
        or ledger.append_boundary_through_occurrence(boundary_event.identity)
        != ledger.append_boundary()
        or current.get("measurement_occurrences", {}).get(result.identity)
        != carried_result_reference
        or carried_result_reference != _determination_result_reference(result)
    ):
        raise SharedPairPositionError(
            "D.2 determination result or current coordinates changed before binding"
        )
    return ledger.append(
        SHARED_POSITION_MEASUREMENT_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
        _binding_material(
            inputs=inputs,
            through_event_occurrence_identity=boundary,
            identities=identities,
            determination_result_reference=(
                _determination_result_reference(result)
            ),
        ),
        locality_identity=result.locality_identity,
    )


def record_shared_position_subject_to_act_binding(
    ledger: EventLedger,
    *,
    first_result_occurrence_identity: str,
    first_assertion_address: str | int,
    second_result_occurrence_identity: str,
    second_assertion_address: str | int,
    current_coordinates: dict[str, Any],
) -> Event:
    """Bind recurrent yielded position Assertions only."""

    for identity in (
        first_result_occurrence_identity,
        second_result_occurrence_identity,
    ):
        result = ledger.get(identity) if type(identity) is str else None
        if result is not None and result.kind == BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND:
            raise SharedPairPositionError(
                "direct pair-position Assertions require one D.2 determination result"
            )
    inputs = _inputs(
        ledger,
        first_result_occurrence_identity=first_result_occurrence_identity,
        first_assertion_address=first_assertion_address,
        second_result_occurrence_identity=second_result_occurrence_identity,
        second_assertion_address=second_assertion_address,
        prior_coordinates=current_coordinates,
    )
    required = tuple(
        dict.fromkeys(
            (
                inputs.first.recorded_occurrence_identity,
                inputs.second.recorded_occurrence_identity,
            )
        )
    )
    return _record_shared_position_binding(
        ledger,
        inputs=inputs,
        current_coordinates=current_coordinates,
        required_occurrences=required,
    )


def _read_binding(
    ledger: EventLedger,
    event_identity: str,
    *,
    prior_coordinates: dict[str, Any] | None = None,
) -> tuple[Event, SharedPairPositionInputs]:
    event = ledger.get(_identity(event_identity, "shared-position requires one binding"))
    if (
        event is None
        or event.kind
        not in {
            SHARED_POSITION_MEASUREMENT_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
            SHARED_POSITION_APPLICABILITY_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
        }
        or event.exact_material is not None
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise SharedPairPositionError("shared-position binding is absent or corrupted")
    first = event.material.get("first_position_assertion")
    second = event.material.get("second_position_assertion")
    if type(first) is not dict or type(second) is not dict:
        raise SharedPairPositionError("shared-position binding carries no exact inputs")
    boundary = event.material.get("through_event_occurrence_identity")
    provenance_present = D2_RESULT_REFERENCE_COORDINATE in event.material
    determination_result = None
    determination_reference = None
    if provenance_present:
        determination_reference = event.material.get(
            D2_RESULT_REFERENCE_COORDINATE
        )
        determination_identity = (
            determination_reference.get("recorded_occurrence_identity")
            if type(determination_reference) is dict
            else None
        )
        if prior_coordinates is None:
            from seed_runtime.operator_locality_standing import (
                read_operator_locality_standing_through,
            )

            try:
                prior_coordinates = read_operator_locality_standing_through(
                    ledger,
                    locality_identity=event.locality_identity,
                    through_event_occurrence_identity=boundary,
                )
            except (TypeError, ValueError) as error:
                raise SharedPairPositionError(
                    "shared-position binding has no exact D.2 current coordinates"
                ) from error
        determination_result, inputs = _d2_result_inputs(
            ledger,
            result_event_identity=determination_identity,
            prior_coordinates=prior_coordinates,
        )
        _require_exact_d2_result_current_coordinates(
            ledger,
            result=determination_result,
            inputs=inputs,
            current_coordinates=prior_coordinates,
        )
        if determination_reference != _determination_result_reference(
            determination_result
        ):
            raise SharedPairPositionError(
                "shared-position binding carries no exact D.2 provenance"
            )
    else:
        inputs = _inputs_from_binding_material(
            ledger,
            first=first,
            second=second,
            prior_coordinates=prior_coordinates,
        )
    identity_coordinates = (
        _IDENTITY_COORDINATES
        if event.kind
        == SHARED_POSITION_MEASUREMENT_SUBJECT_TO_ACT_BINDING_RECORDED_KIND
        else (
            "applicability_act_identity",
            "applicability_act_occurrence_identity",
            "applicability_result_identity",
        )
    )
    identities = {
        coordinate: event.material.get(coordinate)
        for coordinate in identity_coordinates
    }
    if (
        any(type(value) is not str or not value for value in identities.values())
        or len(set(identities.values())) != len(identities)
    ):
        raise SharedPairPositionError("shared-position binding identities are not exact")
    boundary_event = ledger.get(boundary) if type(boundary) is str else None
    if (
        boundary_event is None
        or boundary_event.locality_identity != event.locality_identity
        or ledger.integrity_of(boundary_event.identity) == CORRUPTED
    ):
        raise SharedPairPositionError(
            "shared-position binding has no exact through-occurrence boundary"
        )
    if event.kind == SHARED_POSITION_MEASUREMENT_SUBJECT_TO_ACT_BINDING_RECORDED_KIND:
        expected = _binding_material(
            inputs=inputs,
            through_event_occurrence_identity=boundary,
            identities=identities,
            determination_result_reference=determination_reference,
        )
    else:
        expected = _applicability_binding_material(
            inputs=inputs,
            through_event_occurrence_identity=boundary,
            measurement_act_identity=event.material.get(
                "addressed_act_identity"
            ),
            identities=identities,
            determination_result_reference=determination_reference,
        )
    if event.locality_identity != inputs.first.locality_identity or event.material != expected:
        raise SharedPairPositionError("shared-position binding coordinates are not exact")
    ordered = tuple(
        dict.fromkeys(
            (
                inputs.first.recorded_occurrence_identity,
                inputs.second.recorded_occurrence_identity,
                *(
                    (determination_result.identity,)
                    if determination_result is not None
                    else ()
                ),
                boundary,
                event.identity,
            )
        )
    )
    try:
        resolved = ledger.occurrences_in_append_order(
            ordered,
            locality_identity=event.locality_identity,
        )
    except (TypeError, ValueError) as error:
        raise SharedPairPositionError("shared-position binding order is false") from error
    if tuple(item.identity for item in resolved) != ordered:
        raise SharedPairPositionError("shared-position binding order is false")
    return event, inputs


def get_shared_position_subject_to_act_binding(
    ledger: EventLedger, event_identity: str
) -> dict[str, Any]:
    event, _inputs_reading = _read_binding(ledger, event_identity)
    return deepcopy(event.material)


def _applicability_act_material(
    *,
    binding: Event,
    inputs: SharedPairPositionInputs,
    through_event_occurrence_identity: str,
) -> dict[str, Any]:
    return {
        "addressed_act_identity": binding.material["addressed_act_identity"],
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
        "measurement_rule": MEASUREMENT_RULE,
        "through_event_occurrence_identity": through_event_occurrence_identity,
        "input_relations": [
            {
                "role": "first exact pair-occurrence position Assertion",
                "subject": _reference_material(inputs.first),
                "addressed_act_identity": binding.material[
                    "addressed_act_identity"
                ],
            },
            {
                "role": "second exact pair-occurrence position Assertion",
                "subject": _reference_material(inputs.second),
                "addressed_act_identity": binding.material[
                    "addressed_act_identity"
                ],
            },
        ],
        "scope": binding.material["scope"],
        "unknown": binding.material["unknown"],
    }


def record_shared_position_applicability_act_occurrence(
    ledger: EventLedger,
    *,
    binding_event_identity: str,
    current_coordinates: dict[str, Any],
) -> Event:
    measurement_binding, inputs = _read_binding(
        ledger,
        binding_event_identity,
        prior_coordinates=current_coordinates,
    )
    if (
        measurement_binding.kind
        != SHARED_POSITION_MEASUREMENT_SUBJECT_TO_ACT_BINDING_RECORDED_KIND
    ):
        raise SharedPairPositionError(
            "shared-position Applicability requires the governed Measurement binding"
        )
    boundary = _require_current_coordinates(
        ledger,
        inputs=inputs,
        current_coordinates=current_coordinates,
        carried_coordinate="subject_to_act_binding_occurrences",
        required_occurrences=(measurement_binding.identity,),
    )
    identities = _mint_applicability_identities(ledger)
    if len(set(identities.values())) != len(identities):
        raise SharedPairPositionError(
            "shared-position Applicability occurrence identities collapsed"
        )
    applicability_binding = ledger.append(
        SHARED_POSITION_APPLICABILITY_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
        _applicability_binding_material(
            inputs=inputs,
            through_event_occurrence_identity=boundary,
            measurement_act_identity=measurement_binding.material[
                "exact_act_identity"
            ],
            identities=identities,
            determination_result_reference=measurement_binding.material.get(
                D2_RESULT_REFERENCE_COORDINATE
            ),
        ),
        locality_identity=measurement_binding.locality_identity,
    )
    return ledger.append(
        SHARED_POSITION_APPLICABILITY_ACT_OCCURRENCE_EVENT,
        _applicability_act_material(
            binding=applicability_binding,
            inputs=inputs,
            through_event_occurrence_identity=applicability_binding.identity,
        ),
        locality_identity=measurement_binding.locality_identity,
    )


def _read_applicability_act(
    ledger: EventLedger,
    event_identity: str,
    *,
    binding_reading: tuple[Event, SharedPairPositionInputs] | None = None,
    prior_coordinates: dict[str, Any] | None = None,
) -> tuple[Event, Event, SharedPairPositionInputs]:
    event = ledger.get(
        _identity(event_identity, "shared-position Applicability requires Act occurrence")
    )
    if (
        event is None
        or event.kind != SHARED_POSITION_APPLICABILITY_ACT_OCCURRENCE_EVENT
        or event.exact_material is not None
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise SharedPairPositionError("shared-position Applicability Act is corrupted")
    binding_reference = event.material.get("subject_to_act_binding_reference")
    if type(binding_reference) is not dict:
        raise SharedPairPositionError("Applicability Act carries no binding")
    binding_identity = binding_reference.get("recorded_occurrence_identity")
    if binding_reading is None:
        binding_reading = _read_binding(
            ledger,
            binding_identity,
            prior_coordinates=prior_coordinates,
        )
    binding, inputs = binding_reading
    boundary = event.material.get("through_event_occurrence_identity")
    boundary_event = ledger.get(boundary) if type(boundary) is str else None
    expected = _applicability_act_material(
        binding=binding,
        inputs=inputs,
        through_event_occurrence_identity=boundary,
    )
    if (
        binding_identity != binding.identity
        or event.locality_identity != binding.locality_identity
        or boundary_event is None
        or boundary_event.locality_identity != event.locality_identity
        or ledger.integrity_of(boundary_event.identity) == CORRUPTED
        or event.material != expected
    ):
        raise SharedPairPositionError("Applicability Act coordinates are not exact")
    try:
        ledger.occurrences_in_append_order(
            tuple(dict.fromkeys((binding.identity, boundary, event.identity))),
            locality_identity=event.locality_identity,
        )
    except (TypeError, ValueError) as error:
        raise SharedPairPositionError("Applicability Act order is false") from error
    return event, binding, inputs


def get_shared_position_applicability_act_occurrence(
    ledger: EventLedger, event_identity: str
) -> dict[str, Any]:
    event, _binding, _inputs_reading = _read_applicability_act(
        ledger, event_identity
    )
    return deepcopy(event.material)


def _measurement_binding_addressed_by_applicability(
    ledger: EventLedger,
    applicability_binding: Event,
    inputs: SharedPairPositionInputs,
) -> Event:
    addressed_act_identity = applicability_binding.material.get(
        "addressed_act_identity"
    )
    matches = tuple(
        event
        for event in ledger.list_locality(applicability_binding.locality_identity)
        if event.kind
        == SHARED_POSITION_MEASUREMENT_SUBJECT_TO_ACT_BINDING_RECORDED_KIND
        and event.material.get("exact_act_identity") == addressed_act_identity
    )
    if len(matches) != 1:
        raise SharedPairPositionError(
            "shared-position Applicability addresses no exact Measurement binding"
        )
    measurement_binding = matches[0]
    identities = {
        coordinate: measurement_binding.material.get(coordinate)
        for coordinate in _IDENTITY_COORDINATES
    }
    boundary = measurement_binding.material.get("through_event_occurrence_identity")
    determination_reference = measurement_binding.material.get(
        D2_RESULT_REFERENCE_COORDINATE
    )
    expected = _binding_material(
        inputs=inputs,
        through_event_occurrence_identity=boundary,
        identities=identities,
        determination_result_reference=determination_reference,
    )
    if (
        ledger.integrity_of(measurement_binding.identity) == CORRUPTED
        or measurement_binding.locality_identity
        != applicability_binding.locality_identity
        or any(type(value) is not str or not value for value in identities.values())
        or len(set(identities.values())) != len(identities)
        or measurement_binding.material != expected
    ):
        raise SharedPairPositionError(
            "shared-position Applicability addresses other Measurement subjects"
        )
    return measurement_binding


def _applicability_binding_for_inputs(
    ledger: EventLedger,
    event_identity: str,
    inputs: SharedPairPositionInputs,
) -> Event:
    binding = ledger.get(event_identity)
    if (
        binding is None
        or binding.kind
        != SHARED_POSITION_APPLICABILITY_SUBJECT_TO_ACT_BINDING_RECORDED_KIND
        or binding.locality_identity != inputs.first.locality_identity
        or ledger.integrity_of(binding.identity) == CORRUPTED
    ):
        raise SharedPairPositionError(
            "shared-position Applicability binding is absent or corrupted"
        )
    identities = {
        coordinate: binding.material.get(coordinate)
        for coordinate in (
            "applicability_act_identity",
            "applicability_act_occurrence_identity",
            "applicability_result_identity",
        )
    }
    expected = _applicability_binding_material(
        inputs=inputs,
        through_event_occurrence_identity=binding.material.get(
            "through_event_occurrence_identity"
        ),
        measurement_act_identity=binding.material.get(
            "addressed_act_identity"
        ),
        identities=identities,
        determination_result_reference=binding.material.get(
            D2_RESULT_REFERENCE_COORDINATE
        ),
    )
    if (
        any(type(value) is not str or not value for value in identities.values())
        or len(set(identities.values())) != len(identities)
        or binding.material != expected
    ):
        raise SharedPairPositionError(
            "shared-position Applicability binding coordinates are not exact"
        )
    return binding


def _applicability_result_material(
    *,
    ledger: EventLedger,
    act: Event,
    binding: Event,
    inputs: SharedPairPositionInputs,
) -> dict[str, Any]:
    measurement_binding = _measurement_binding_addressed_by_applicability(
        ledger,
        binding,
        inputs,
    )
    applicable = inputs.carries_one_position_coordinate_reference
    applicability = "applicable" if applicable else "inapplicable"
    return {
        "result_identity": binding.material["applicability_result_identity"],
        "dimensions": {
            "identity": binding.material["applicability_result_identity"],
            "content": {
                "first_relation_second_position_coordinate_reference": (
                    inputs.first_relation_second_position_coordinate_reference
                ),
                "second_relation_first_position_coordinate_reference": (
                    inputs.second_relation_first_position_coordinate_reference
                ),
                "shared_position_coordinate_reference": (
                    inputs.shared_position_coordinate_reference
                ),
            },
            "source_provenance": "exact recorded position Assertions",
            "scope": binding.material["scope"],
        },
        "exact_act": APPLICABILITY_ACT,
        "addressed_act_identity": measurement_binding.material[
            "measurement_act_identity"
        ],
        "addressed_act_occurrence_identity": (
            measurement_binding.material["measurement_act_occurrence_identity"]
            if applicable
            else None
        ),
        "applicability_act_identity": binding.material[
            "applicability_act_identity"
        ],
        "applicability_act_occurrence_identity": binding.material[
            "applicability_act_occurrence_identity"
        ],
        "subject_to_act_binding_reference": _binding_reference(
            binding,
            result_boundary_identity=binding.material[
                "applicability_result_identity"
            ],
        ),
        "act_occurrence_event_identity": act.identity,
        "first_position_assertion": _reference_material(inputs.first),
        "second_position_assertion": _reference_material(inputs.second),
        "measurement_rule": MEASUREMENT_RULE,
        "applicability": applicability,
        "scope": binding.material["scope"],
        "unknown": binding.material["unknown"],
    }


def _refuse_existing_result(
    ledger: EventLedger,
    *,
    act: Event,
    result_kind: str,
) -> None:
    act_occurrence_coordinate = (
        "applicability_act_occurrence_identity"
        if act.kind == SHARED_POSITION_APPLICABILITY_ACT_OCCURRENCE_EVENT
        else "act_occurrence_identity"
    )
    act_occurrence_identity = act.material[act_occurrence_coordinate]
    for event in ledger.list_locality(act.locality_identity):
        if event.kind not in {
            result_kind,
            RECORDED_YIELD_RELATION_EVENT,
        }:
            continue
        if (
            event.material.get("act_occurrence_event_identity") == act.identity
            or event.material.get("act_occurrence_identity")
            == act_occurrence_identity
            or event.material.get("applicability_act_occurrence_identity")
            == act_occurrence_identity
            or event.material.get("dimensions", {}).get(
                "act_occurrence_identity"
            )
            == act_occurrence_identity
        ):
            raise SharedPairPositionError(
                "one shared-position Act cannot Yield a second result"
            )


def record_shared_position_applicability_result(
    ledger: EventLedger,
    *,
    applicability_act_occurrence_event_identity: str,
) -> Event:
    act, binding, inputs = _read_applicability_act(
        ledger, applicability_act_occurrence_event_identity
    )
    _refuse_existing_result(
        ledger,
        act=act,
        result_kind=SHARED_POSITION_APPLICABILITY_RESULT_KIND,
    )
    result = _applicability_result_material(
        ledger=ledger,
        act=act,
        binding=binding,
        inputs=inputs,
    )
    yield_relation = _record_yield_relation(
        ledger,
        locality_identity=act.locality_identity,
        exact_act=APPLICABILITY_ACT,
        act_occurrence_identity=act.material[
            "applicability_act_occurrence_identity"
        ],
        act_occurrence_event_identity=act.identity,
        result_kind=APPLICABILITY_RESULT_KIND,
        result_identity=result["result_identity"],
        result_content={
            coordinate: value
            for coordinate, value in result.items()
            if coordinate != "act_occurrence_event_identity"
        },
        occurrence_boundary="shared_pair_position_applicability",
        responsible_act_occurrence_coordinate=(
            "applicability_act_occurrence_identity"
        ),
    )
    return ledger.append(
        SHARED_POSITION_APPLICABILITY_RESULT_KIND,
        _recorded_applicability_result_material(
            result,
            yield_relation_identity=yield_relation.identity,
        ),
        locality_identity=act.locality_identity,
    )


def _recorded_applicability_result_material(
    result: dict[str, Any],
    *,
    yield_relation_identity: str,
) -> dict[str, Any]:
    return {
        "result_identity": result["result_identity"],
        "dimensions": deepcopy(result["dimensions"]),
        "exact_act": result["exact_act"],
        "addressed_act_identity": result["addressed_act_identity"],
        "addressed_act_occurrence_identity": result[
            "addressed_act_occurrence_identity"
        ],
        "applicability_act_identity": result["applicability_act_identity"],
        "applicability_act_occurrence_identity": result[
            "applicability_act_occurrence_identity"
        ],
        "subject_to_act_binding_reference": deepcopy(
            result["subject_to_act_binding_reference"]
        ),
        "act_occurrence_event_identity": result[
            "act_occurrence_event_identity"
        ],
        "first_position_assertion": deepcopy(result["first_position_assertion"]),
        "second_position_assertion": deepcopy(result["second_position_assertion"]),
        "measurement_rule": result["measurement_rule"],
        "applicability": result["applicability"],
        "scope": deepcopy(result["scope"]),
        "unknown": list(result["unknown"]),
        "yield_relation_identity": yield_relation_identity,
    }


def _require_yield(
    ledger: EventLedger,
    *,
    event: Event,
    act: Event,
    occurrence_boundary: str,
    result_kind: str,
    result_occurrence_coordinate: str = "act_occurrence_identity",
    responsible_act_occurrence_coordinate: str = "act_occurrence_identity",
) -> None:
    yield_relation_identity = event.material.get("yield_relation_identity")
    yield_relation = ledger.get(yield_relation_identity) if type(yield_relation_identity) is str else None
    requirements = read_requirements_of_yield_relation(
        ledger,
        recorded_result_event_identity=event.identity,
        yield_relation_event_identity=yield_relation_identity,
        act_occurrence_event_identity=act.identity,
        recorded_result_occurrence_coordinate=result_occurrence_coordinate,
        responsible_act_occurrence_coordinate=(
            responsible_act_occurrence_coordinate
        ),
    )
    if (
        not all(requirements.values())
        or yield_relation is None
        or yield_relation.material.get("occurrence_boundary") != occurrence_boundary
        or yield_relation.material.get("result_kind") != result_kind
    ):
        raise SharedPairPositionError("result carries no exact Yield relation")


def _read_applicability_result(
    ledger: EventLedger,
    event_identity: str,
    *,
    binding_reading: tuple[Event, SharedPairPositionInputs] | None = None,
    prior_coordinates: dict[str, Any] | None = None,
) -> tuple[Event, Event, Event, SharedPairPositionInputs, dict[str, Any]]:
    event = ledger.get(_identity(event_identity, "Applicability requires one result"))
    if (
        event is None
        or event.kind != SHARED_POSITION_APPLICABILITY_RESULT_KIND
        or event.exact_material is not None
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise SharedPairPositionError("shared-position Applicability result is corrupted")
    act_identity = event.material.get("act_occurrence_event_identity")
    act, binding, inputs = _read_applicability_act(
        ledger,
        act_identity,
        binding_reading=binding_reading,
        prior_coordinates=prior_coordinates,
    )
    expected = _applicability_result_material(
        ledger=ledger,
        act=act,
        binding=binding,
        inputs=inputs,
    )
    carried = {
        key: value
        for key, value in event.material.items()
        if key != "yield_relation_identity"
    }
    if event.locality_identity != act.locality_identity or carried != expected:
        raise SharedPairPositionError("Applicability result coordinates are not exact")
    _require_yield(
        ledger,
        event=event,
        act=act,
        occurrence_boundary=APPLICABILITY_BOUNDARY,
        result_kind=APPLICABILITY_RESULT_KIND,
        result_occurrence_coordinate="applicability_act_occurrence_identity",
        responsible_act_occurrence_coordinate=(
            "applicability_act_occurrence_identity"
        ),
    )
    return event, act, binding, inputs, carried


def get_recorded_shared_position_applicability(
    ledger: EventLedger, event_identity: str
) -> dict[str, Any]:
    return deepcopy(_read_applicability_result(ledger, event_identity)[4])


def _measurement_act_material(
    *,
    binding: Event,
    inputs: SharedPairPositionInputs,
    applicability: Event,
    through_event_occurrence_identity: str,
) -> dict[str, Any]:
    return {
        "addressed_act_identity": binding.material["measurement_act_identity"],
        "act_occurrence_identity": binding.material[
            "measurement_act_occurrence_identity"
        ],
        "act": MEASUREMENT_ACT,
        "subject_to_act_binding_reference": _binding_reference(
            binding,
            result_boundary_identity=binding.material[
                "measurement_result_identity"
            ],
        ),
        "applicability_result_reference": {
            "recorded_occurrence_identity": applicability.identity,
            "result_identity": applicability.material["result_identity"],
        },
        "measurement_rule": MEASUREMENT_RULE,
        "through_event_occurrence_identity": through_event_occurrence_identity,
        "participation": [
            {
                "role": "first relation of ordered path",
                "subject": _reference_material(inputs.first),
                "act_occurrence_identity": binding.material[
                    "measurement_act_occurrence_identity"
                ],
            },
            {
                "role": "second relation of ordered path",
                "subject": _reference_material(inputs.second),
                "act_occurrence_identity": binding.material[
                    "measurement_act_occurrence_identity"
                ],
            },
        ],
        "scope": binding.material["scope"],
        "unknown": binding.material["unknown"],
    }


def record_shared_position_measurement_act_occurrence(
    ledger: EventLedger,
    *,
    applicability_result_event_identity: str,
    current_coordinates: dict[str, Any],
) -> Event:
    applicability, _act, applicability_binding, inputs, applicability_material = (
        _read_applicability_result(
            ledger,
            applicability_result_event_identity,
            prior_coordinates=current_coordinates,
        )
    )
    if applicability_material["applicability"] != "applicable":
        raise SharedPairPositionError(
            "inapplicable pair-position inputs cannot participate"
        )
    measurement_binding = _measurement_binding_addressed_by_applicability(
        ledger,
        applicability_binding,
        inputs,
    )
    boundary = _require_current_coordinates(
        ledger,
        inputs=inputs,
        current_coordinates=current_coordinates,
        carried_coordinate="applicability_result_occurrences",
        required_occurrences=(applicability.identity,),
    )
    return ledger.append(
        SHARED_POSITION_MEASUREMENT_ACT_OCCURRENCE_EVENT,
        _measurement_act_material(
            binding=measurement_binding,
            inputs=inputs,
            applicability=applicability,
            through_event_occurrence_identity=boundary,
        ),
        locality_identity=measurement_binding.locality_identity,
    )


def _read_measurement_act(
    ledger: EventLedger,
    event_identity: str,
    *,
    binding_reading: tuple[Event, SharedPairPositionInputs] | None = None,
    prior_coordinates: dict[str, Any] | None = None,
) -> tuple[Event, Event, Event, SharedPairPositionInputs]:
    event = ledger.get(_identity(event_identity, "shared-position requires Act occurrence"))
    if (
        event is None
        or event.kind != SHARED_POSITION_MEASUREMENT_ACT_OCCURRENCE_EVENT
        or event.exact_material is not None
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise SharedPairPositionError("shared-position Measurement Act is corrupted")
    binding_reference = event.material.get("subject_to_act_binding_reference")
    applicability_reference = event.material.get("applicability_result_reference")
    if type(binding_reference) is not dict or type(applicability_reference) is not dict:
        raise SharedPairPositionError("Measurement Act carries no exact inputs")
    if binding_reading is None:
        binding_reading = _read_binding(
            ledger,
            binding_reference.get("recorded_occurrence_identity"),
            prior_coordinates=prior_coordinates,
        )
    binding, inputs = binding_reading
    if (
        binding_reference.get("recorded_occurrence_identity")
        != binding.identity
    ):
        raise SharedPairPositionError("Measurement Act carries no exact inputs")
    applicability_identity = applicability_reference.get("recorded_occurrence_identity")
    applicability_event = ledger.get(applicability_identity)
    applicability_act_event = (
        ledger.get(applicability_event.material.get("act_occurrence_event_identity"))
        if applicability_event is not None
        else None
    )
    applicability_binding_reference = (
        applicability_act_event.material.get("subject_to_act_binding_reference")
        if applicability_act_event is not None
        else None
    )
    applicability_binding = _applicability_binding_for_inputs(
        ledger,
        applicability_binding_reference.get("recorded_occurrence_identity")
        if type(applicability_binding_reference) is dict
        else None,
        inputs,
    )
    (
        applicability,
        _act,
        applicability_binding,
        applicability_inputs,
        applicability_material,
    ) = _read_applicability_result(
        ledger,
        applicability_identity,
        binding_reading=(applicability_binding, inputs),
        prior_coordinates=prior_coordinates,
    )
    boundary = event.material.get("through_event_occurrence_identity")
    boundary_event = ledger.get(boundary) if type(boundary) is str else None
    expected = _measurement_act_material(
        binding=binding,
        inputs=inputs,
        applicability=applicability,
        through_event_occurrence_identity=boundary,
    )
    if (
        applicability_inputs != inputs
        or _measurement_binding_addressed_by_applicability(
            ledger,
            applicability_binding,
            applicability_inputs,
        ).identity
        != binding.identity
        or applicability_material["applicability"] != "applicable"
        or event.locality_identity != binding.locality_identity
        or boundary_event is None
        or boundary_event.locality_identity != event.locality_identity
        or ledger.integrity_of(boundary_event.identity) == CORRUPTED
        or event.material != expected
    ):
        raise SharedPairPositionError("Measurement Act coordinates are not exact")
    try:
        ledger.occurrences_in_append_order(
            tuple(dict.fromkeys((applicability.identity, boundary, event.identity))),
            locality_identity=event.locality_identity,
        )
    except (TypeError, ValueError) as error:
        raise SharedPairPositionError("Measurement Act order is false") from error
    return event, binding, applicability, inputs


def get_shared_position_measurement_act_occurrence(
    ledger: EventLedger, event_identity: str
) -> dict[str, Any]:
    event, _binding, _applicability, _inputs_reading = _read_measurement_act(
        ledger, event_identity
    )
    return deepcopy(event.material)


def _path_assertion(
    *,
    inputs: SharedPairPositionInputs,
    applicability: Event,
) -> dict[str, Any]:
    subject = {
        "first_position_assertion_reference": inputs.first.assertion_reference,
        "second_position_assertion_reference": inputs.second.assertion_reference,
        "measurement_rule": MEASUREMENT_RULE,
    }
    scope = {"source_localities": [inputs.first.locality_identity]}
    content = {
        "shared_position_coordinate_reference": (
            inputs.shared_position_coordinate_reference
        ),
        "source_material_result_occurrence_identity": (
            inputs.first.source_material_result_occurrence_identity
        ),
        "completeness_boundary_identity": (
            inputs.first.completeness_boundary_identity
        ),
    }
    return {
        "dimensions": {
            "position": 0,
            "content": content,
            "source_provenance": "exact recorded pair position Assertions",
        },
        "result": "ordered_relation_path",
        "assertion_subject": subject,
        "assertion_scope": scope,
        "input_support": {
            "assertion_references": [
                inputs.first.assertion_reference,
                inputs.second.assertion_reference,
            ],
            "occurrence_references": [
                inputs.first.source_material_result_occurrence_identity,
                applicability.identity,
            ],
            "local_assertion_references": [],
        },
        "conflicts": "Unknown",
        "unknown": [],
    }


def _measurement_result_material(
    *,
    act: Event,
    binding: Event,
    applicability: Event,
    inputs: SharedPairPositionInputs,
) -> dict[str, Any]:
    assertion = _path_assertion(
        inputs=inputs,
        applicability=applicability,
    )
    return {
        "result_identity": binding.material["measurement_result_identity"],
        "dimensions": {
            "identity": binding.material["measurement_result_identity"],
            "content": "one exact ordered relation-path Assertion",
            "source_provenance": "exact recorded pair position Assertions",
            "scope": binding.material["scope"],
        },
        "exact_act": MEASUREMENT_ACT,
        "addressed_act_identity": binding.material["measurement_act_identity"],
        "act_occurrence_identity": binding.material[
            "measurement_act_occurrence_identity"
        ],
        "subject_to_act_binding_reference": _binding_reference(
            binding,
            result_boundary_identity=binding.material[
                "measurement_result_identity"
            ],
        ),
        "act_occurrence_event_identity": act.identity,
        "applicability_result_reference": {
            "recorded_occurrence_identity": applicability.identity,
            "result_identity": applicability.material["result_identity"],
        },
        "measurement_rule": MEASUREMENT_RULE,
        "source_localities": [inputs.first.locality_identity],
        "completeness_boundary": {
            "identity": inputs.first.completeness_boundary_identity,
        },
        "first_position_assertion": _reference_material(inputs.first),
        "second_position_assertion": _reference_material(inputs.second),
        "assertions": [assertion],
        "scope": binding.material["scope"],
        "unknown": binding.material["unknown"],
    }


def record_shared_position_measurement_result(
    ledger: EventLedger,
    *,
    measurement_act_occurrence_event_identity: str,
) -> Event:
    act, binding, applicability, inputs = _read_measurement_act(
        ledger, measurement_act_occurrence_event_identity
    )
    _refuse_existing_result(
        ledger,
        act=act,
        result_kind=SHARED_POSITION_MEASUREMENT_RESULT_KIND,
    )
    result = _measurement_result_material(
        act=act,
        binding=binding,
        applicability=applicability,
        inputs=inputs,
    )
    yield_relation = _record_yield_relation(
        ledger,
        locality_identity=act.locality_identity,
        exact_act=MEASUREMENT_ACT,
        act_occurrence_identity=act.material["act_occurrence_identity"],
        act_occurrence_event_identity=act.identity,
        result_kind=MEASUREMENT_RESULT_KIND,
        result_identity=result["result_identity"],
        result_content={
            coordinate: value
            for coordinate, value in result.items()
            if coordinate != "act_occurrence_event_identity"
        },
        occurrence_boundary="shared_pair_position_measurement",
    )
    return ledger.append(
        SHARED_POSITION_MEASUREMENT_RESULT_KIND,
        _recorded_measurement_result_material(
            result,
            yield_relation_identity=yield_relation.identity,
        ),
        locality_identity=act.locality_identity,
    )


def _recorded_measurement_result_material(
    result: dict[str, Any],
    *,
    yield_relation_identity: str,
) -> dict[str, Any]:
    return {
        "result_identity": result["result_identity"],
        "dimensions": deepcopy(result["dimensions"]),
        "exact_act": result["exact_act"],
        "addressed_act_identity": result["addressed_act_identity"],
        "act_occurrence_identity": result["act_occurrence_identity"],
        "subject_to_act_binding_reference": deepcopy(
            result["subject_to_act_binding_reference"]
        ),
        "act_occurrence_event_identity": result[
            "act_occurrence_event_identity"
        ],
        "applicability_result_reference": deepcopy(
            result["applicability_result_reference"]
        ),
        "measurement_rule": result["measurement_rule"],
        "source_localities": list(result["source_localities"]),
        "completeness_boundary": deepcopy(result["completeness_boundary"]),
        "first_position_assertion": deepcopy(result["first_position_assertion"]),
        "second_position_assertion": deepcopy(result["second_position_assertion"]),
        "assertions": deepcopy(result["assertions"]),
        "scope": deepcopy(result["scope"]),
        "unknown": list(result["unknown"]),
        "yield_relation_identity": yield_relation_identity,
    }


def _read_measurement_result(
    ledger: EventLedger,
    event_identity: str,
    *,
    binding_reading: tuple[Event, SharedPairPositionInputs] | None = None,
    prior_coordinates: dict[str, Any] | None = None,
) -> tuple[Event, dict[str, Any]]:
    event = ledger.get(_identity(event_identity, "shared-position requires one result"))
    if (
        event is None
        or event.kind != SHARED_POSITION_MEASUREMENT_RESULT_KIND
        or event.exact_material is not None
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise SharedPairPositionError("shared-position Measurement result is corrupted")
    act_identity = event.material.get("act_occurrence_event_identity")
    act, binding, applicability, inputs = _read_measurement_act(
        ledger,
        act_identity,
        binding_reading=binding_reading,
        prior_coordinates=prior_coordinates,
    )
    expected = _measurement_result_material(
        act=act,
        binding=binding,
        applicability=applicability,
        inputs=inputs,
    )
    carried = {
        key: value
        for key, value in event.material.items()
        if key != "yield_relation_identity"
    }
    if event.locality_identity != act.locality_identity or carried != expected:
        raise SharedPairPositionError("Measurement result coordinates are not exact")
    _require_yield(
        ledger,
        event=event,
        act=act,
        occurrence_boundary=MEASUREMENT_BOUNDARY,
        result_kind=MEASUREMENT_RESULT_KIND,
    )
    return event, carried


def _shared_position_replay_occurrence(
    ledger: EventLedger,
    event: Event,
    *,
    expected_material: dict[str, Any] | None = None,
) -> _SharedPositionReplayOccurrence:
    material = (
        deepcopy(event.material)
        if expected_material is None
        else expected_material
    )
    ledger_event = ledger.get(event.identity) if type(event) is Event else None
    if (
        ledger_event is None
        or ledger_event != event
        or ledger_event.kind != event.kind
        or ledger_event.material != material
        or ledger_event.exact_material != event.exact_material
        or ledger_event.locality_identity != event.locality_identity
        or type(event.locality_identity) is not str
        or not event.locality_identity
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise SharedPairPositionError(
            "shared-position replay occurrence is absent or corrupted"
        )
    return _SharedPositionReplayOccurrence(
        event=event,
        kind=event.kind,
        material=material,
        exact_material=event.exact_material,
        locality_identity=event.locality_identity,
    )


def _require_shared_position_replay_occurrence(
    ledger: EventLedger,
    occurrence: _SharedPositionReplayOccurrence,
) -> None:
    ledger_event = ledger.get(occurrence.event.identity)
    if (
        ledger_event is None
        or ledger_event != occurrence.event
        or ledger_event.kind != occurrence.kind
        or ledger_event.material != occurrence.material
        or ledger_event.exact_material != occurrence.exact_material
        or ledger_event.locality_identity != occurrence.locality_identity
        or ledger.integrity_of(occurrence.event.identity) == CORRUPTED
    ):
        raise SharedPairPositionError(
            "shared-position replay requires an intact input occurrence"
        )


def _recurrent_result_binding_act_and_yield_relation(
    ledger: EventLedger,
    result: Event,
) -> tuple[Event, Event, Event]:
    if (
        result.kind
        != RECORDING_OCCURRENCE_OF_RESULT_OF_MEASUREMENT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_KIND
    ):
        raise SharedPairPositionError(
            "shared-position replay recurrent input result is not exact"
        )
    act_identity = result.material.get("act_occurrence_event_identity")
    yield_identity = result.material.get("yield_relation_identity")
    act = ledger.get(act_identity) if type(act_identity) is str else None
    yield_relation = (
        ledger.get(yield_identity) if type(yield_identity) is str else None
    )
    binding_reference = (
        act.material.get("subject_to_act_binding_reference")
        if act is not None
        else None
    )
    binding_identity = (
        binding_reference.get("recorded_occurrence_identity")
        if type(binding_reference) is dict
        else None
    )
    binding = (
        ledger.get(binding_identity)
        if type(binding_identity) is str
        else None
    )
    if (
        act is None
        or act.kind
        != RECORDED_ACT_OCCURRENCE_OF_MEASUREMENT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_EVENT
        or binding is None
        or binding.kind
        != RECORDED_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_MEASUREMENT_SUBJECT_TO_ACT_BINDING_KIND
        or yield_relation is None
        or yield_relation.kind != RECORDED_YIELD_RELATION_EVENT
        or any(
            occurrence.locality_identity != result.locality_identity
            for occurrence in (binding, act, yield_relation)
        )
    ):
        raise SharedPairPositionError(
            "shared-position replay recurrent result carries no exact binding, "
            "Act occurrence, or Yield relation"
        )
    return binding, act, yield_relation


def _shared_position_replay_occurrence_coordinates(
    ledger: EventLedger,
    inputs: SharedPairPositionInputs,
) -> tuple[
    tuple[_SharedPositionReplayOccurrence, ...],
    tuple[_SharedPositionReplayOccurrence, ...],
    tuple[_SharedPositionReplayOccurrence, ...],
    tuple[_SharedPositionReplayOccurrence, ...],
    tuple[_SharedPositionReplayOccurrence, ...],
    tuple[_SharedPositionReplayOccurrence, ...],
]:
    """Read each exact occurrence coordinate required by both inputs."""

    result_identities: list[str] = []
    source_identities: list[str] = []
    pair_result_identities: list[str] = []
    subject_to_act_bindings: list[Event] = []
    act_occurrence_occurrences: list[Event] = []
    yield_relations: list[Event] = []
    for reference in inputs:
        result_identities.append(reference.recorded_occurrence_identity)
        source_identities.append(reference.source_material_result_occurrence_identity)
        pair_result_identity = getattr(
            reference, "pair_measurement_occurrence_identity", None
        )
        if type(pair_result_identity) is str and pair_result_identity:
            pair_result_identities.append(pair_result_identity)
        if (
            type(reference)
            is ReferenceToRecordedRecurrentBytePairOccurrencePosition
        ):
            result = ledger.get(reference.recorded_occurrence_identity)
            if result is None:
                raise SharedPairPositionError(
                    "shared-position replay recurrent input result is absent"
                )
            subject_to_act_binding, act_occurrence, yield_relation = (
                _recurrent_result_binding_act_and_yield_relation(ledger, result)
            )
            subject_to_act_bindings.append(subject_to_act_binding)
            act_occurrence_occurrences.append(act_occurrence)
            yield_relations.append(yield_relation)

    def occurrences_at_identities(
        identities: list[str],
    ) -> tuple[_SharedPositionReplayOccurrence, ...]:
        events = tuple(ledger.get(identity) for identity in dict.fromkeys(identities))
        if any(event is None for event in events):
            raise SharedPairPositionError(
                "shared-position replay requires each exact input occurrence"
            )
        return tuple(
            _shared_position_replay_occurrence(ledger, event)
            for event in events
        )

    def occurrences_for_events(
        events: list[Event],
    ) -> tuple[_SharedPositionReplayOccurrence, ...]:
        return tuple(
            _shared_position_replay_occurrence(ledger, event)
            for event in {
                event.identity: event for event in events
            }.values()
        )

    return (
        occurrences_at_identities(result_identities),
        occurrences_at_identities(source_identities),
        occurrences_at_identities(pair_result_identities),
        occurrences_for_events(subject_to_act_bindings),
        occurrences_for_events(act_occurrence_occurrences),
        occurrences_for_events(yield_relations),
    )


def _shared_position_replay_reading(
    ledger: EventLedger,
    binding_reading: tuple[Event, SharedPairPositionInputs],
) -> _SharedPositionReplayReading:
    binding, inputs = binding_reading
    if type(binding) is not Event or type(inputs) is not SharedPairPositionInputs:
        raise SharedPairPositionError(
            "shared-position replay requires one exact binding reading"
        )
    (
        input_results,
        sources,
        pair_measurement_results,
        subject_to_act_bindings,
        act_occurrence,
        yield_relations,
    ) = _shared_position_replay_occurrence_coordinates(ledger, inputs)
    reading = _SharedPositionReplayReading(
        binding_reading=binding_reading,
        binding_occurrence=_shared_position_replay_occurrence(
            ledger,
            binding,
            expected_material=deepcopy(binding.material),
        ),
        input_result_occurrences=input_results,
        source_occurrences=sources,
        pair_measurement_result_occurrences=pair_measurement_results,
        subject_to_act_binding_occurrences=subject_to_act_bindings,
        act_occurrence_occurrences=act_occurrence,
        yield_relation_occurrences=yield_relations,
    )
    _require_exact_shared_position_replay_reading(ledger, reading)
    return reading


def _require_exact_shared_position_replay_reading(
    ledger: EventLedger,
    reading: _SharedPositionReplayReading,
) -> None:
    binding, inputs = reading.binding_reading
    if (
        type(binding) is not Event
        or type(inputs) is not SharedPairPositionInputs
        or reading.binding_occurrence.event is not binding
        or not reading.input_result_occurrences
        or not reading.source_occurrences
    ):
        raise SharedPairPositionError(
            "shared-position replay binding reading was substituted"
        )
    for occurrence in (
        reading.binding_occurrence,
        reading.applicability_binding_occurrence,
        *reading.input_result_occurrences,
        *reading.source_occurrences,
        *reading.pair_measurement_result_occurrences,
        *reading.subject_to_act_binding_occurrences,
        *reading.act_occurrence_occurrences,
        *reading.yield_relation_occurrences,
        reading.applicability_act_occurrence,
        reading.applicability_result_occurrence,
        reading.measurement_act_occurrence,
        reading.measurement_result_occurrence,
    ):
        if occurrence is not None:
            _require_shared_position_replay_occurrence(ledger, occurrence)
    _validated_inputs(inputs.first, inputs.second)
    if reading.applicability_binding_reading is not None:
        applicability_binding, applicability_inputs = (
            reading.applicability_binding_reading
        )
        if (
            reading.applicability_binding_occurrence is None
            or reading.applicability_binding_occurrence.event
            is not applicability_binding
            or applicability_inputs != inputs
        ):
            raise SharedPairPositionError(
                "shared-position replay Applicability binding was substituted"
            )


def _add_shared_position_applicability_binding(
    ledger: EventLedger,
    reading: _SharedPositionReplayReading,
    binding_reading: tuple[Event, SharedPairPositionInputs],
) -> _SharedPositionReplayReading:
    _require_exact_shared_position_replay_reading(ledger, reading)
    measurement_binding, measurement_inputs = reading.binding_reading
    applicability_binding, applicability_inputs = binding_reading
    if (
        reading.applicability_binding_reading is not None
        or applicability_binding.kind
        != SHARED_POSITION_APPLICABILITY_SUBJECT_TO_ACT_BINDING_RECORDED_KIND
        or applicability_inputs != measurement_inputs
        or applicability_binding.material.get("addressed_act_identity")
        != measurement_binding.material.get("exact_act_identity")
    ):
        raise SharedPairPositionError(
            "shared-position replay Applicability binding is not exact"
        )
    reading.applicability_binding_reading = binding_reading
    reading.applicability_binding_occurrence = _shared_position_replay_occurrence(
        ledger,
        applicability_binding,
        expected_material=deepcopy(applicability_binding.material),
    )
    _require_exact_shared_position_replay_reading(ledger, reading)
    return reading


def _advance_shared_position_replay_reading(
    ledger: EventLedger,
    reading: _SharedPositionReplayReading,
    event: Event,
) -> _SharedPositionReplayReading:
    """Validate one later shared-position occurrence from one exact replay reading."""

    _require_exact_shared_position_replay_reading(ledger, reading)
    binding, _inputs_reading = reading.binding_reading
    if event.locality_identity != binding.locality_identity:
        raise SharedPairPositionError(
            "shared-position replay occurrence entered another Locality"
        )
    occurrence = _shared_position_replay_occurrence(
        ledger,
        event,
        expected_material=deepcopy(event.material),
    )
    if event.kind == SHARED_POSITION_APPLICABILITY_ACT_OCCURRENCE_EVENT:
        if (
            reading.applicability_binding_reading is None
            or reading.applicability_act_occurrence is not None
        ):
            raise SharedPairPositionError(
                "shared-position replay duplicated Applicability Act"
            )
        _read_applicability_act(
            ledger,
            event.identity,
            binding_reading=reading.applicability_binding_reading,
        )
        reading.applicability_act_occurrence = occurrence
    elif event.kind == SHARED_POSITION_APPLICABILITY_RESULT_KIND:
        if (
            reading.applicability_act_occurrence is None
            or reading.applicability_result_occurrence is not None
        ):
            raise SharedPairPositionError(
                "shared-position replay has no exact Applicability Act"
            )
        _read_applicability_result(
            ledger,
            event.identity,
            binding_reading=reading.applicability_binding_reading,
        )
        reading.applicability_result_occurrence = occurrence
    elif event.kind == SHARED_POSITION_MEASUREMENT_ACT_OCCURRENCE_EVENT:
        if (
            reading.applicability_result_occurrence is None
            or reading.measurement_act_occurrence is not None
        ):
            raise SharedPairPositionError(
                "shared-position replay has no exact Applicability result"
            )
        _read_measurement_act(
            ledger,
            event.identity,
            binding_reading=reading.binding_reading,
        )
        reading.measurement_act_occurrence = occurrence
    elif event.kind == SHARED_POSITION_MEASUREMENT_RESULT_KIND:
        if (
            reading.measurement_act_occurrence is None
            or reading.measurement_result_occurrence is not None
        ):
            raise SharedPairPositionError(
                "shared-position replay has no exact Measurement Act"
            )
        _read_measurement_result(
            ledger,
            event.identity,
            binding_reading=reading.binding_reading,
        )
        reading.measurement_result_occurrence = occurrence
    else:
        raise SharedPairPositionError(
            "shared-position replay occurrence is not exact"
        )
    ordered = tuple(
        occurrence.event.identity
        for occurrence in (
            reading.binding_occurrence,
            reading.applicability_act_occurrence,
            reading.applicability_result_occurrence,
            reading.measurement_act_occurrence,
            reading.measurement_result_occurrence,
        )
        if occurrence is not None
    )
    try:
        resolved = ledger.occurrences_in_append_order(
            ordered,
            locality_identity=binding.locality_identity,
        )
    except ValueError as error:
        raise SharedPairPositionError(
            "shared-position replay occurrence order is false"
        ) from error
    if tuple(item.identity for item in resolved) != ordered:
        raise SharedPairPositionError(
            "shared-position replay occurrence order is false"
        )
    return reading


def get_recorded_shared_position_measurement(
    ledger: EventLedger,
    event_identity: str,
    *,
    prior_coordinates: dict[str, Any] | None = None,
) -> dict[str, Any]:
    _event, carried = _read_measurement_result(
        ledger,
        event_identity,
        prior_coordinates=prior_coordinates,
    )
    return deepcopy(carried)


def ordered_relation_path_assertion_adjacent_to_input_position_assertion_coordinates(
    ledger: EventLedger,
    event_identity: str,
    *,
    prior_coordinates: dict[str, Any] | None = None,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    """Read one path Assertion adjacent to two exact input Assertion contents.

    Each input Assertion content has exact pair and position coordinates.
    Returning them adjacent to the path establishes no material carried by the path.
    """

    reading = get_recorded_shared_position_measurement(
        ledger, event_identity, prior_coordinates=prior_coordinates
    )
    assertions = reading.get("assertions")
    first = reading.get("first_position_assertion")
    second = reading.get("second_position_assertion")
    if (
        type(assertions) is not list
        or len(assertions) != 1
        or type(assertions[0]) is not dict
        or assertions[0].get("result") != "ordered_relation_path"
        or type(first) is not dict
        or type(second) is not dict
    ):
        raise SharedPairPositionError(
            "shared-position result carries no exact path and input coordinates"
        )
    return deepcopy(assertions[0]), deepcopy(first), deepcopy(second)


def ordered_source_position_coordinates_adjacent_to_ordered_relation_path_assertion(
    ledger: EventLedger,
    event_identity: str,
    *,
    prior_coordinates: dict[str, Any] | None = None,
) -> tuple[dict[str, Any], tuple[dict[str, Any], ...]]:
    """Read three exact source-position coordinates adjacent to one path Assertion.

    The first returned position addresses the first input role; the second
    returned position addresses the second input role. Returning the positions
    adjacent to the path establishes no position or material carried by the path.
    """

    path, first, second = (
        ordered_relation_path_assertion_adjacent_to_input_position_assertion_coordinates(
            ledger, event_identity, prior_coordinates=prior_coordinates
        )
    )
    first_position = first.get("first_position_coordinate_reference")
    first_shared = first.get("second_position_coordinate_reference")
    second_shared = second.get("first_position_coordinate_reference")
    last_position = second.get("second_position_coordinate_reference")
    path_shared = path.get("dimensions", {}).get("content", {}).get(
        "shared_position_coordinate_reference"
    )
    if (
        any(
            type(coordinate) is not dict
            for coordinate in (
                first_position,
                first_shared,
                second_shared,
                last_position,
                path_shared,
            )
        )
        or first_shared != second_shared
        or path_shared != first_shared
    ):
        raise SharedPairPositionError(
            "shared-position result carries no exact ordered source positions"
        )
    return deepcopy(path), tuple(
        deepcopy(coordinate)
        for coordinate in (first_position, first_shared, last_position)
    )
