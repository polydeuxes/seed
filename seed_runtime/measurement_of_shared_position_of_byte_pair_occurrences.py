"""Compose exact yielded pair-position Assertions at one shared position."""

from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from typing import Any, NamedTuple

from seed_runtime.event import Event
from seed_runtime.byte_measurement import SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY
from seed_runtime.events import CORRUPTED, EventLedger
from seed_runtime.evidence_of_yield_relation import (
    RECORDED_EVIDENCE_OF_YIELD_RELATION_KIND,
    _record_evidence_of_yield_relation,
    read_requirements_of_yield_relation,
)
from seed_runtime.identities import new_identity
from seed_runtime.addressed_byte_occurrence_reference_determination import (
    _determination_result_reference,
    _read_determination_result,
)
from seed_runtime.measurement_of_recurrent_byte_pair_occurrence_position import (
    RECORDING_OCCURRENCE_OF_RESULT_OF_MEASUREMENT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_KIND,
    ReferenceToRecordedRecurrentBytePairOccurrencePosition,
    _references_to_addressed_recorded_recurrent_pair_position_results,
    references_to_recorded_recurrent_byte_pair_occurrence_positions,
)
from seed_runtime.measurement_of_position_coordinates_of_byte_pair_occurrences import (
    BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND,
    ReferenceToRecordedPositionOfBytePairOccurrence,
    references_to_addressed_recorded_position_coordinates_of_byte_pair_occurrences,
    references_to_recorded_position_coordinates_of_byte_pair_occurrences,
)


SHARED_POSITION_RESPONSIBILITY_ASSIGNMENT_KIND = (
    "operator.shared_pair_position.responsibility_assignment_recorded"
)
SHARED_POSITION_APPLICABILITY_ACT_EVIDENCE_KIND = (
    "operator.shared_pair_position.applicability_act_evidenced"
)
SHARED_POSITION_APPLICABILITY_RESULT_KIND = (
    "operator.shared_pair_position.applicability_recorded"
)
SHARED_POSITION_MEASUREMENT_ACT_EVIDENCE_KIND = (
    "operator.shared_pair_position.measurement_act_evidenced"
)
SHARED_POSITION_MEASUREMENT_RESULT_KIND = (
    "operator.shared_pair_position.measurement_recorded"
)
BOOK_CLAUSE = "01.Source.D"
MEASUREMENT_RULE = (
    "second position-coordinate reference of first exact recorded pair occurrence "
    "Assertion and first position-coordinate reference of second exact recorded pair "
    "occurrence Assertion identifies one exact byte occurrence"
)
RESPONSIBILITY = (
    "determine Applicability and Yield one ordered path where exact pair occurrence "
    "Assertions carry one exact position-coordinate reference"
)
APPLICABILITY_ACT = (
    "determine Applicability of exact pair occurrence position Assertions to one "
    "shared position Measurement"
)
MEASUREMENT_ACT = "determine one shared position of exact byte pair occurrences"
SHARED_POSITION_ASSERTION_RESPONSIBILITY = (
    "preserve exact coordinates of this Measurement Assertion"
)
APPLICABILITY_RESULT_KIND = "shared pair-position input Applicability result"
MEASUREMENT_RESULT_KIND = "shared pair-position Measurement result"
APPLICABILITY_BOUNDARY = "shared_pair_position_applicability"
MEASUREMENT_BOUNDARY = "shared_pair_position_measurement"
D2_RESULT_REFERENCE_COORDINATE = (
    "addressed_byte_occurrence_reference_determination_result_reference"
)

EVENT_KIND_RESPONSIBILITIES = {
    SHARED_POSITION_RESPONSIBILITY_ASSIGNMENT_KIND: "01.Source.D",
    SHARED_POSITION_APPLICABILITY_ACT_EVIDENCE_KIND: "02.Acts.A",
    SHARED_POSITION_APPLICABILITY_RESULT_KIND: "01.Standing.E.1",
    SHARED_POSITION_MEASUREMENT_ACT_EVIDENCE_KIND: "02.Acts.A",
    SHARED_POSITION_MEASUREMENT_RESULT_KIND: "01.Source.D",
}
ASSERTION_RESPONSIBILITIES = {
    SHARED_POSITION_ASSERTION_RESPONSIBILITY: "01.Standing.D.1"
}


class SharedPairPositionError(ValueError):
    """One shared-position Measurement lifecycle is incoherent."""


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
        return self.first_relation_second_position_coordinate_reference[
            "identity"
        ] == self.second_relation_first_position_coordinate_reference["identity"]

    @property
    def shared_position_coordinate_reference(self) -> dict[str, Any] | None:
        if not self.carries_one_position_coordinate_reference:
            return None
        return self.first_relation_second_position_coordinate_reference


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
    coordinates = {
        "source_ingest_occurrence_identity": (
            reference.source_ingest_occurrence_identity
        ),
        "locality_identity": reference.locality_identity,
        "completeness_boundary_identity": (
            reference.completeness_boundary_identity
        ),
        "position": position,
        "exact_material": list(exact_material),
    }
    return {
        "identity": "source-byte-position-coordinate:"
        + hashlib.sha256(
            json.dumps(
                coordinates, sort_keys=True, separators=(",", ":")
            ).encode("utf-8")
        ).hexdigest(),
        **coordinates,
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
        "assertion_identity": reference.assertion_identity,
        "source_ingest_occurrence_identity": (
            reference.source_ingest_occurrence_identity
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
                "assertion_identity": reference.recurrence_assertion_identity,
            },
            {
                "recorded_occurrence_identity": (
                    reference.pair_measurement_occurrence_identity
                ),
                "assertion_identity": reference.count_assertion_identity,
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
    assertion_identity: str,
) -> RecordedPairPositionReference:
    assertion_identity = _identity(
        assertion_identity,
        "shared-position Measurement requires one exact Assertion identity",
    )
    return _resolve_references(
        ledger,
        result_occurrence_identity=_identity(
            result_occurrence_identity,
            "shared-position Measurement requires one exact result occurrence",
        ),
        assertion_identities=(assertion_identity,),
    )[0]


def _resolve_references(
    ledger: EventLedger,
    *,
    result_occurrence_identity: str,
    assertion_identities: tuple[str, ...],
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
        try:
            return references_to_addressed_recorded_position_coordinates_of_byte_pair_occurrences(
                ledger,
                result_occurrence_identity,
                assertion_identities,
            )
        except (TypeError, ValueError) as error:
            raise SharedPairPositionError(
                "shared-position Measurement requires carried position Assertions"
            ) from error
    references = _references(
        ledger,
        result_occurrence_identity=result_occurrence_identity,
    )
    by_identity = {reference.assertion_identity: reference for reference in references}
    if any(identity not in by_identity for identity in assertion_identities):
        raise SharedPairPositionError(
            "shared-position Measurement requires carried position Assertions"
        )
    return tuple(by_identity[identity] for identity in assertion_identities)


def _inputs(
    ledger: EventLedger,
    *,
    first_result_occurrence_identity: str,
    first_assertion_identity: str,
    second_result_occurrence_identity: str,
    second_assertion_identity: str,
) -> SharedPairPositionInputs:
    if first_result_occurrence_identity == second_result_occurrence_identity:
        first, second = _resolve_references(
            ledger,
            result_occurrence_identity=second_result_occurrence_identity,
            assertion_identities=(
                _identity(
                    first_assertion_identity,
                    "shared-position Measurement requires one exact Assertion identity",
                ),
                _identity(
                    second_assertion_identity,
                    "shared-position Measurement requires one exact Assertion identity",
                ),
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
                    result_and_assertion_identities=(
                        (
                            _identity(
                                first_result_occurrence_identity,
                                "shared-position Measurement requires one exact result occurrence",
                            ),
                            _identity(
                                first_assertion_identity,
                                "shared-position Measurement requires one exact Assertion identity",
                            ),
                        ),
                        (
                            _identity(
                                second_result_occurrence_identity,
                                "shared-position Measurement requires one exact result occurrence",
                            ),
                            _identity(
                                second_assertion_identity,
                                "shared-position Measurement requires one exact Assertion identity",
                            ),
                        ),
                    ),
                )
            )
            return _validated_inputs(first, second)
        first = _resolve_reference(
            ledger,
            result_occurrence_identity=first_result_occurrence_identity,
            assertion_identity=first_assertion_identity,
        )
        second = _resolve_reference(
            ledger,
            result_occurrence_identity=second_result_occurrence_identity,
            assertion_identity=second_assertion_identity,
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
        first.source_ingest_occurrence_identity
        != second.source_ingest_occurrence_identity
        or first.locality_identity != second.locality_identity
        or first.completeness_boundary_identity
        != second.completeness_boundary_identity
    ):
        raise SharedPairPositionError(
            "shared-position inputs require one source occurrence, Locality, and boundary"
        )
    return SharedPairPositionInputs(first=first, second=second)


def _direct_coordinates_from_assignment_material(
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
            "shared-position assignment carries no exact inputs"
        )
    return (
        bytes(exact_pair),
        material.get("first_position"),
        material.get("second_position"),
    )


def _inputs_from_assignment_material(
    ledger: EventLedger,
    *,
    first: dict[str, Any],
    second: dict[str, Any],
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
            _direct_coordinates_from_assignment_material(material)
            for material in materials
        )
        assertion_identities = tuple(
            material.get("assertion_identity") for material in materials
        )
        try:
            if result_identities[0] == result_identities[1]:
                first_reference, second_reference = (
                    references_to_addressed_recorded_position_coordinates_of_byte_pair_occurrences(
                        ledger,
                        result_identities[0],
                        assertion_identities,
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
                        assertion_identities,
                        coordinates,
                        strict=True,
                    )
                )
        except (TypeError, ValueError) as error:
            raise SharedPairPositionError(
                "shared-position assignment carries no exact inputs"
            ) from error
        return _validated_inputs(first_reference, second_reference)
    return _inputs(
        ledger,
        first_result_occurrence_identity=result_identities[0],
        first_assertion_identity=first.get("assertion_identity"),
        second_result_occurrence_identity=result_identities[1],
        second_assertion_identity=second.get("assertion_identity"),
    )


def _authority() -> dict[str, str]:
    return {
        "source": "this Book",
        "book_clause_identity": BOOK_CLAUSE,
        "authority_limit": "bounded",
        "act": (
            "determine one exact shared position-coordinate reference and Yield "
            "one ordered relation path"
        ),
        "negative_authority": (
            "establish no represented relation and no emission"
        ),
    }


def _require_standing(
    ledger: EventLedger,
    *,
    inputs: SharedPairPositionInputs,
    locality_standing: dict[str, Any],
    carried_coordinate: str,
    required_occurrences: tuple[str, ...],
) -> str:
    if type(locality_standing) is not dict:
        raise SharedPairPositionError("shared-position Measurement requires Standing")
    carried = locality_standing.get(carried_coordinate)
    boundary = locality_standing.get("through_event_occurrence_identity")
    if (
        locality_standing.get("locality_identity") != inputs.first.locality_identity
        or type(carried) is not dict
        or any(identity not in carried for identity in required_occurrences)
        or type(boundary) is not str
        or not boundary
    ):
        raise SharedPairPositionError(
            "current Standing lacks the exact shared-position inputs"
        )
    ordered = tuple(dict.fromkeys((*required_occurrences, boundary)))
    try:
        resolved = ledger.occurrences_in_append_order(
            ordered,
            locality_identity=inputs.first.locality_identity,
        )
    except (TypeError, ValueError) as error:
        raise SharedPairPositionError(
            "Standing boundary is not after exact shared-position inputs"
        ) from error
    if tuple(event.identity for event in resolved) != ordered:
        raise SharedPairPositionError(
            "Standing boundary is not after exact shared-position inputs"
        )
    return boundary


def _assignment_reference(event: Event) -> dict[str, str]:
    return {
        "recorded_occurrence_identity": event.identity,
        "assignment_identity": event.material["assignment_identity"],
        "assignment_subject_identity": event.material[
            "assignment_subject_identity"
        ],
    }


def _assignment_material(
    *,
    inputs: SharedPairPositionInputs,
    standing_boundary_identity: str,
    identities: dict[str, str],
    determination_result_reference: dict[str, str] | None = None,
) -> dict[str, Any]:
    material = {
        "assignment_identity": identities["assignment_identity"],
        "assignment_subject_identity": identities[
            "assignment_subject_identity"
        ],
        "applicability_act_identity": identities[
            "applicability_act_identity"
        ],
        "applicability_act_occurrence_identity": identities[
            "applicability_act_occurrence_identity"
        ],
        "applicability_result_identity": identities[
            "applicability_result_identity"
        ],
        "measurement_act_identity": identities["measurement_act_identity"],
        "measurement_act_occurrence_identity": identities[
            "measurement_act_occurrence_identity"
        ],
        "measurement_result_identity": identities[
            "measurement_result_identity"
        ],
        "first_input_relation_identity": identities[
            "first_input_relation_identity"
        ],
        "second_input_relation_identity": identities[
            "second_input_relation_identity"
        ],
        "first_participation_relation_identity": identities[
            "first_participation_relation_identity"
        ],
        "second_participation_relation_identity": identities[
            "second_participation_relation_identity"
        ],
        "book_clause_identity": BOOK_CLAUSE,
        "responsibility": RESPONSIBILITY,
        "responsible_boundary": "this Seed",
        "measurement_rule": MEASUREMENT_RULE,
        "first_position_assertion": _reference_material(inputs.first),
        "second_position_assertion": _reference_material(inputs.second),
        "standing_boundary_identity": standing_boundary_identity,
        "scope": {
            "locality_identity": inputs.first.locality_identity,
            "source_ingest_occurrence_identity": (
                inputs.first.source_ingest_occurrence_identity
            ),
            "completeness_boundary_identity": (
                inputs.first.completeness_boundary_identity
            ),
            "standing_boundary_identity": standing_boundary_identity,
        },
        "authority": _authority(),
        "limits": [
            "pair counts establish no shared position",
            "relation path Standing from exact source material is not_established",
        ],
        "unknown": ["what this ordered relation path represents remains Unknown"],
    }
    if determination_result_reference is not None:
        material[D2_RESULT_REFERENCE_COORDINATE] = deepcopy(
            determination_result_reference
        )
    return material


_IDENTITY_COORDINATES = (
    "assignment_identity",
    "assignment_subject_identity",
    "applicability_act_identity",
    "applicability_act_occurrence_identity",
    "applicability_result_identity",
    "measurement_act_identity",
    "measurement_act_occurrence_identity",
    "measurement_result_identity",
    "first_input_relation_identity",
    "second_input_relation_identity",
    "first_participation_relation_identity",
    "second_participation_relation_identity",
)


def _new_assignment_identities() -> dict[str, str]:
    return {
        "assignment_identity": new_identity("shared_pair_position_assignment_identity"),
        "assignment_subject_identity": new_identity(
            "shared_pair_position_assignment_subject_identity"
        ),
        "applicability_act_identity": new_identity(
            "shared_pair_position_applicability_act_identity"
        ),
        "applicability_act_occurrence_identity": new_identity(
            "shared_pair_position_applicability_act_occurrence_identity"
        ),
        "applicability_result_identity": new_identity(
            "shared_pair_position_applicability_result_identity"
        ),
        "measurement_act_identity": new_identity(
            "shared_pair_position_measurement_act_identity"
        ),
        "measurement_act_occurrence_identity": new_identity(
            "shared_pair_position_measurement_act_occurrence_identity"
        ),
        "measurement_result_identity": new_identity(
            "shared_pair_position_measurement_result_identity"
        ),
        "first_input_relation_identity": new_identity(
            "shared_pair_position_first_input_relation_identity"
        ),
        "second_input_relation_identity": new_identity(
            "shared_pair_position_second_input_relation_identity"
        ),
        "first_participation_relation_identity": new_identity(
            "shared_pair_position_first_participation_relation_identity"
        ),
        "second_participation_relation_identity": new_identity(
            "shared_pair_position_second_participation_relation_identity"
        ),
    }


def _record_shared_position_assignment(
    ledger: EventLedger,
    *,
    inputs: SharedPairPositionInputs,
    locality_standing: dict[str, Any],
    required_occurrences: tuple[str, ...],
) -> Event:
    boundary = _require_standing(
        ledger,
        inputs=inputs,
        locality_standing=locality_standing,
        carried_coordinate="measurement_occurrences",
        required_occurrences=required_occurrences,
    )
    identities = _new_assignment_identities()
    if len(set(identities.values())) != len(identities):
        raise SharedPairPositionError("shared-position lifecycle identities collapsed")
    return ledger.append(
        SHARED_POSITION_RESPONSIBILITY_ASSIGNMENT_KIND,
        _assignment_material(
            inputs=inputs,
            standing_boundary_identity=boundary,
            identities=identities,
        ),
        locality_identity=inputs.first.locality_identity,
    )


def _d2_result_inputs(
    ledger: EventLedger,
    *,
    result_event_identity: str,
    prior_standing: dict[str, Any],
) -> tuple[Event, SharedPairPositionInputs]:
    try:
        result, _act, _applicability, _assignment, _source, references = (
            _read_determination_result(
                ledger,
                result_event_identity,
                prior_standing=prior_standing,
            )
        )
    except (TypeError, ValueError) as error:
        raise SharedPairPositionError(
            "shared-position assignment requires one exact D.2 determination result"
        ) from error
    if len(references) != 2:
        raise SharedPairPositionError(
            "shared-position assignment requires exactly two ordered D.2 Assertion references"
        )
    try:
        inputs = _validated_inputs(references[0], references[1])
    except (TypeError, ValueError) as error:
        raise SharedPairPositionError(
            "shared-position assignment requires exactly two ordered D.2 Assertion references"
        ) from error
    return result, inputs


def _require_exact_d2_result_standing(
    ledger: EventLedger,
    *,
    result: Event,
    inputs: SharedPairPositionInputs,
    locality_standing: dict[str, Any],
) -> str:
    measurements = (
        locality_standing.get("measurement_occurrences")
        if type(locality_standing) is dict
        else None
    )
    if (
        type(measurements) is not dict
        or measurements.get(result.identity)
        != _determination_result_reference(result)
    ):
        raise SharedPairPositionError(
            "current Standing carries no exact D.2 determination result"
        )
    return _require_standing(
        ledger,
        inputs=inputs,
        locality_standing=locality_standing,
        carried_coordinate="measurement_occurrences",
        required_occurrences=(result.identity,),
    )


def record_shared_position_responsibility_assignment_from_addressed_byte_occurrence_reference_determination_result(
    ledger: EventLedger,
    *,
    determination_result_event_identity: str,
    locality_standing: dict[str, Any],
) -> Event:
    """Assign from the two ordered Assertions carried by one current D.2 result."""

    result_identity = _identity(
        determination_result_event_identity,
        "shared-position assignment requires one exact D.2 determination result",
    )
    result, inputs = _d2_result_inputs(
        ledger,
        result_event_identity=result_identity,
        prior_standing=locality_standing,
    )
    from seed_runtime.operator_locality_standing import (
        read_operator_locality_standing,
    )

    current = read_operator_locality_standing(
        ledger, locality_identity=result.locality_identity
    )
    if locality_standing != current:
        raise SharedPairPositionError(
            "shared-position assignment requires exact current Standing"
        )
    result, inputs = _d2_result_inputs(
        ledger,
        result_event_identity=result_identity,
        prior_standing=current,
    )
    result_material = deepcopy(result.material)
    current_snapshot = deepcopy(current)
    boundary = _require_exact_d2_result_standing(
        ledger,
        result=result,
        inputs=inputs,
        locality_standing=current,
    )
    identities = _new_assignment_identities()
    if len(set(identities.values())) != len(identities):
        raise SharedPairPositionError("shared-position lifecycle identities collapsed")

    result_read, inputs_read = _d2_result_inputs(
        ledger,
        result_event_identity=result_identity,
        prior_standing=current,
    )
    boundary_event = ledger.get(boundary)
    if (
        result_read != result
        or result.material != result_material
        or inputs_read != inputs
        or current != current_snapshot
        or locality_standing != current_snapshot
        or current_snapshot.get("through_event_occurrence_identity") != boundary
        or boundary_event is None
        or ledger.integrity_of(boundary_event.identity) == CORRUPTED
        or ledger.append_boundary_through_occurrence(boundary_event.identity)
        != ledger.append_boundary()
        or current_snapshot.get("measurement_occurrences", {}).get(result.identity)
        != _determination_result_reference(result)
    ):
        raise SharedPairPositionError(
            "D.2 determination result or current Standing changed before assignment"
        )
    return ledger.append(
        SHARED_POSITION_RESPONSIBILITY_ASSIGNMENT_KIND,
        _assignment_material(
            inputs=inputs,
            standing_boundary_identity=boundary,
            identities=identities,
            determination_result_reference=(
                _determination_result_reference(result)
            ),
        ),
        locality_identity=result.locality_identity,
    )


def record_shared_position_responsibility_assignment(
    ledger: EventLedger,
    *,
    first_result_occurrence_identity: str,
    first_assertion_identity: str,
    second_result_occurrence_identity: str,
    second_assertion_identity: str,
    locality_standing: dict[str, Any],
) -> Event:
    """Assign from recurrent yielded position Assertions only."""

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
        first_assertion_identity=first_assertion_identity,
        second_result_occurrence_identity=second_result_occurrence_identity,
        second_assertion_identity=second_assertion_identity,
    )
    required = tuple(
        dict.fromkeys(
            (
                inputs.first.recorded_occurrence_identity,
                inputs.second.recorded_occurrence_identity,
            )
        )
    )
    return _record_shared_position_assignment(
        ledger,
        inputs=inputs,
        locality_standing=locality_standing,
        required_occurrences=required,
    )


def _read_assignment(
    ledger: EventLedger,
    event_identity: str,
    *,
    prior_standing: dict[str, Any] | None = None,
) -> tuple[Event, SharedPairPositionInputs]:
    event = ledger.get(_identity(event_identity, "shared-position requires one assignment"))
    if (
        event is None
        or event.kind != SHARED_POSITION_RESPONSIBILITY_ASSIGNMENT_KIND
        or event.exact_material is not None
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise SharedPairPositionError("shared-position assignment is absent or corrupted")
    first = event.material.get("first_position_assertion")
    second = event.material.get("second_position_assertion")
    if type(first) is not dict or type(second) is not dict:
        raise SharedPairPositionError("shared-position assignment carries no exact inputs")
    boundary = event.material.get("standing_boundary_identity")
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
        if prior_standing is None:
            from seed_runtime.operator_locality_standing import (
                read_operator_locality_standing_through,
            )

            try:
                prior_standing = read_operator_locality_standing_through(
                    ledger,
                    locality_identity=event.locality_identity,
                    through_event_occurrence_identity=boundary,
                )
            except (TypeError, ValueError) as error:
                raise SharedPairPositionError(
                    "shared-position assignment has no exact D.2 Standing"
                ) from error
        determination_result, inputs = _d2_result_inputs(
            ledger,
            result_event_identity=determination_identity,
            prior_standing=prior_standing,
        )
        _require_exact_d2_result_standing(
            ledger,
            result=determination_result,
            inputs=inputs,
            locality_standing=prior_standing,
        )
        if determination_reference != _determination_result_reference(
            determination_result
        ):
            raise SharedPairPositionError(
                "shared-position assignment carries no exact D.2 provenance"
            )
    else:
        inputs = _inputs_from_assignment_material(
            ledger,
            first=first,
            second=second,
        )
    identities = {
        coordinate: event.material.get(coordinate)
        for coordinate in _IDENTITY_COORDINATES
    }
    if (
        any(type(value) is not str or not value for value in identities.values())
        or len(set(identities.values())) != len(identities)
    ):
        raise SharedPairPositionError("shared-position assignment identities are not exact")
    boundary_event = ledger.get(boundary) if type(boundary) is str else None
    if (
        boundary_event is None
        or boundary_event.locality_identity != event.locality_identity
        or ledger.integrity_of(boundary_event.identity) == CORRUPTED
    ):
        raise SharedPairPositionError("shared-position assignment has no Standing boundary")
    expected = _assignment_material(
        inputs=inputs,
        standing_boundary_identity=boundary,
        identities=identities,
        determination_result_reference=determination_reference,
    )
    if event.locality_identity != inputs.first.locality_identity or event.material != expected:
        raise SharedPairPositionError("shared-position assignment coordinates are not exact")
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
        raise SharedPairPositionError("shared-position assignment order is false") from error
    if tuple(item.identity for item in resolved) != ordered:
        raise SharedPairPositionError("shared-position assignment order is false")
    return event, inputs


def get_shared_position_responsibility_assignment(
    ledger: EventLedger, event_identity: str
) -> dict[str, Any]:
    event, _inputs_reading = _read_assignment(ledger, event_identity)
    return json.loads(json.dumps(event.material))


def _applicability_act_material(
    *,
    assignment: Event,
    inputs: SharedPairPositionInputs,
    standing_boundary_identity: str,
) -> dict[str, Any]:
    return {
        "downstream_act_identity": assignment.material["applicability_act_identity"],
        "applicability_act_occurrence_identity": assignment.material[
            "applicability_act_occurrence_identity"
        ],
        "act": APPLICABILITY_ACT,
        "responsibility": RESPONSIBILITY,
        "responsible_boundary": "this Seed",
        "responsibility_assignment_reference": _assignment_reference(assignment),
        "measurement_rule": MEASUREMENT_RULE,
        "standing_boundary_identity": standing_boundary_identity,
        "input_relations": [
            {
                "identity": assignment.material["first_input_relation_identity"],
                "role": "first exact pair-occurrence position Assertion",
                "subject": _reference_material(inputs.first),
                "downstream_act_identity": assignment.material[
                    "measurement_act_identity"
                ],
            },
            {
                "identity": assignment.material["second_input_relation_identity"],
                "role": "second exact pair-occurrence position Assertion",
                "subject": _reference_material(inputs.second),
                "downstream_act_identity": assignment.material[
                    "measurement_act_identity"
                ],
            },
        ],
        "scope": assignment.material["scope"],
        "authority": assignment.material["authority"],
        "evidence_scope": "this exact Applicability Act occurrence",
        "limits": assignment.material["limits"],
        "unknown": assignment.material["unknown"],
    }


def record_shared_position_applicability_act_evidence(
    ledger: EventLedger,
    *,
    assignment_event_identity: str,
    locality_standing: dict[str, Any],
) -> Event:
    assignment, inputs = _read_assignment(ledger, assignment_event_identity)
    boundary = _require_standing(
        ledger,
        inputs=inputs,
        locality_standing=locality_standing,
        carried_coordinate="responsibility_assignment_occurrences",
        required_occurrences=(assignment.identity,),
    )
    return ledger.append(
        SHARED_POSITION_APPLICABILITY_ACT_EVIDENCE_KIND,
        _applicability_act_material(
            assignment=assignment,
            inputs=inputs,
            standing_boundary_identity=boundary,
        ),
        locality_identity=assignment.locality_identity,
    )


def _read_applicability_act(
    ledger: EventLedger,
    event_identity: str,
    *,
    assignment_reading: tuple[Event, SharedPairPositionInputs] | None = None,
) -> tuple[Event, Event, SharedPairPositionInputs]:
    event = ledger.get(
        _identity(event_identity, "shared-position Applicability requires Act Evidence")
    )
    if (
        event is None
        or event.kind != SHARED_POSITION_APPLICABILITY_ACT_EVIDENCE_KIND
        or event.exact_material is not None
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise SharedPairPositionError("shared-position Applicability Act is corrupted")
    assignment_reference = event.material.get("responsibility_assignment_reference")
    if type(assignment_reference) is not dict:
        raise SharedPairPositionError("Applicability Act carries no assignment")
    assignment_identity = assignment_reference.get("recorded_occurrence_identity")
    if assignment_reading is None:
        assignment_reading = _read_assignment(ledger, assignment_identity)
    assignment, inputs = assignment_reading
    boundary = event.material.get("standing_boundary_identity")
    boundary_event = ledger.get(boundary) if type(boundary) is str else None
    expected = _applicability_act_material(
        assignment=assignment,
        inputs=inputs,
        standing_boundary_identity=boundary,
    )
    if (
        assignment_identity != assignment.identity
        or event.locality_identity != assignment.locality_identity
        or boundary_event is None
        or boundary_event.locality_identity != event.locality_identity
        or ledger.integrity_of(boundary_event.identity) == CORRUPTED
        or event.material != expected
    ):
        raise SharedPairPositionError("Applicability Act coordinates are not exact")
    try:
        ledger.occurrences_in_append_order(
            tuple(dict.fromkeys((assignment.identity, boundary, event.identity))),
            locality_identity=event.locality_identity,
        )
    except (TypeError, ValueError) as error:
        raise SharedPairPositionError("Applicability Act order is false") from error
    return event, assignment, inputs


def get_shared_position_applicability_act_evidence(
    ledger: EventLedger, event_identity: str
) -> dict[str, Any]:
    event, _assignment, _inputs_reading = _read_applicability_act(
        ledger, event_identity
    )
    return json.loads(json.dumps(event.material))


def _applicability_result_material(
    *,
    act: Event,
    assignment: Event,
    inputs: SharedPairPositionInputs,
) -> dict[str, Any]:
    applicable = inputs.carries_one_position_coordinate_reference
    standing = "applicable" if applicable else "inapplicable"
    return {
        "result_identity": assignment.material["applicability_result_identity"],
        "dimensions": {
            "identity": assignment.material["applicability_result_identity"],
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
            "standing": standing,
            "source_provenance": "exact recorded position Assertions",
            "responsibility": RESPONSIBILITY,
            "responsible_boundary": "this Seed",
            "authority": assignment.material["authority"],
            "scope": assignment.material["scope"],
        },
        "exact_act": APPLICABILITY_ACT,
        "downstream_act_identity": assignment.material["measurement_act_identity"],
        "downstream_act_occurrence_identity": (
            assignment.material["measurement_act_occurrence_identity"]
            if applicable
            else None
        ),
        "applicability_act_identity": assignment.material[
            "applicability_act_identity"
        ],
        "applicability_act_occurrence_identity": assignment.material[
            "applicability_act_occurrence_identity"
        ],
        "responsibility": RESPONSIBILITY,
        "responsible_boundary": "this Seed",
        "responsibility_assignment_reference": _assignment_reference(assignment),
        "responsible_act_evidence_identity": act.identity,
        "first_input_relation_identity": assignment.material[
            "first_input_relation_identity"
        ],
        "second_input_relation_identity": assignment.material[
            "second_input_relation_identity"
        ],
        "first_position_assertion": _reference_material(inputs.first),
        "second_position_assertion": _reference_material(inputs.second),
        "measurement_rule": MEASUREMENT_RULE,
        "applicability": standing,
        "scope": assignment.material["scope"],
        "authority": assignment.material["authority"],
        "limits": assignment.material["limits"],
        "unknown": assignment.material["unknown"],
    }


def _record_shared_applicability_yield_evidence(
    ledger: EventLedger, *, act: Event, result: dict[str, Any]
) -> Event:
    return _record_evidence_of_yield_relation(
        ledger,
        locality_identity=act.locality_identity,
        exact_act=APPLICABILITY_ACT,
        act_occurrence_identity=act.material[
            "applicability_act_occurrence_identity"
        ],
        responsible_act_evidence_identity=act.identity,
        result_kind=APPLICABILITY_RESULT_KIND,
        result_identity=result["result_identity"],
        result_content={
            coordinate: value
            for coordinate, value in result.items()
            if coordinate != "responsible_act_evidence_identity"
        },
        responsibility=RESPONSIBILITY,
        occurrence_boundary="shared_pair_position_applicability",
        responsible_boundary="this Seed",
        responsible_act_occurrence_coordinate=(
            "applicability_act_occurrence_identity"
        ),
    )


def _refuse_existing_result(
    ledger: EventLedger,
    *,
    act: Event,
    result_kind: str,
) -> None:
    act_occurrence_coordinate = (
        "applicability_act_occurrence_identity"
        if act.kind == SHARED_POSITION_APPLICABILITY_ACT_EVIDENCE_KIND
        else "act_occurrence_identity"
    )
    act_occurrence_identity = act.material[act_occurrence_coordinate]
    for event in ledger.list_locality(act.locality_identity):
        if event.kind not in {
            result_kind,
            RECORDED_EVIDENCE_OF_YIELD_RELATION_KIND,
        }:
            continue
        if (
            event.material.get("responsible_act_evidence_identity") == act.identity
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
    applicability_act_evidence_event_identity: str,
) -> Event:
    act, assignment, inputs = _read_applicability_act(
        ledger, applicability_act_evidence_event_identity
    )
    _refuse_existing_result(
        ledger,
        act=act,
        result_kind=SHARED_POSITION_APPLICABILITY_RESULT_KIND,
    )
    result = _applicability_result_material(
        act=act,
        assignment=assignment,
        inputs=inputs,
    )
    evidence = _record_shared_applicability_yield_evidence(
        ledger,
        act=act,
        result=result,
    )
    return ledger.append(
        SHARED_POSITION_APPLICABILITY_RESULT_KIND,
        _recorded_applicability_result_material(
            result,
            evidence_of_yield_relation_identity=evidence.identity,
        ),
        locality_identity=act.locality_identity,
    )


def _recorded_applicability_result_material(
    result: dict[str, Any],
    *,
    evidence_of_yield_relation_identity: str,
) -> dict[str, Any]:
    return {
        "result_identity": result["result_identity"],
        "dimensions": deepcopy(result["dimensions"]),
        "exact_act": result["exact_act"],
        "downstream_act_identity": result["downstream_act_identity"],
        "downstream_act_occurrence_identity": result[
            "downstream_act_occurrence_identity"
        ],
        "applicability_act_identity": result["applicability_act_identity"],
        "applicability_act_occurrence_identity": result[
            "applicability_act_occurrence_identity"
        ],
        "responsibility": result["responsibility"],
        "responsible_boundary": result["responsible_boundary"],
        "responsibility_assignment_reference": deepcopy(
            result["responsibility_assignment_reference"]
        ),
        "responsible_act_evidence_identity": result[
            "responsible_act_evidence_identity"
        ],
        "first_input_relation_identity": result[
            "first_input_relation_identity"
        ],
        "second_input_relation_identity": result[
            "second_input_relation_identity"
        ],
        "first_position_assertion": deepcopy(result["first_position_assertion"]),
        "second_position_assertion": deepcopy(result["second_position_assertion"]),
        "measurement_rule": result["measurement_rule"],
        "applicability": result["applicability"],
        "scope": deepcopy(result["scope"]),
        "authority": deepcopy(result["authority"]),
        "limits": list(result["limits"]),
        "unknown": list(result["unknown"]),
        "evidence_of_yield_relation_identity": evidence_of_yield_relation_identity,
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
    evidence_identity = event.material.get("evidence_of_yield_relation_identity")
    evidence = ledger.get(evidence_identity) if type(evidence_identity) is str else None
    requirements = read_requirements_of_yield_relation(
        ledger,
        recorded_result_event_identity=event.identity,
        evidence_of_yield_relation_event_identity=evidence_identity,
        responsible_act_evidence_event_identity=act.identity,
        recorded_result_occurrence_coordinate=result_occurrence_coordinate,
        responsible_act_occurrence_coordinate=(
            responsible_act_occurrence_coordinate
        ),
    )
    if (
        not all(requirements.values())
        or evidence is None
        or evidence.material.get("occurrence_boundary") != occurrence_boundary
        or evidence.material.get("result_kind") != result_kind
    ):
        raise SharedPairPositionError("result carries no exact Evidence of Yield relation")


def _read_applicability_result(
    ledger: EventLedger,
    event_identity: str,
    *,
    assignment_reading: tuple[Event, SharedPairPositionInputs] | None = None,
) -> tuple[Event, Event, Event, SharedPairPositionInputs, dict[str, Any]]:
    event = ledger.get(_identity(event_identity, "Applicability requires one result"))
    if (
        event is None
        or event.kind != SHARED_POSITION_APPLICABILITY_RESULT_KIND
        or event.exact_material is not None
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise SharedPairPositionError("shared-position Applicability result is corrupted")
    act_identity = event.material.get("responsible_act_evidence_identity")
    act, assignment, inputs = _read_applicability_act(
        ledger, act_identity, assignment_reading=assignment_reading
    )
    expected = _applicability_result_material(
        act=act,
        assignment=assignment,
        inputs=inputs,
    )
    carried = {
        key: value
        for key, value in event.material.items()
        if key != "evidence_of_yield_relation_identity"
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
    return event, act, assignment, inputs, carried


def get_recorded_shared_position_applicability(
    ledger: EventLedger, event_identity: str
) -> dict[str, Any]:
    return json.loads(
        json.dumps(_read_applicability_result(ledger, event_identity)[4])
    )


def _measurement_act_material(
    *,
    assignment: Event,
    inputs: SharedPairPositionInputs,
    applicability: Event,
    standing_boundary_identity: str,
) -> dict[str, Any]:
    return {
        "downstream_act_identity": assignment.material["measurement_act_identity"],
        "act_occurrence_identity": assignment.material[
            "measurement_act_occurrence_identity"
        ],
        "act": MEASUREMENT_ACT,
        "responsibility": RESPONSIBILITY,
        "responsible_boundary": "this Seed",
        "responsibility_assignment_reference": _assignment_reference(assignment),
        "applicability_result_reference": {
            "recorded_occurrence_identity": applicability.identity,
            "result_identity": applicability.material["result_identity"],
        },
        "measurement_rule": MEASUREMENT_RULE,
        "standing_boundary_identity": standing_boundary_identity,
        "participation": [
            {
                "identity": assignment.material[
                    "first_participation_relation_identity"
                ],
                "role": "first relation of ordered path",
                "subject": _reference_material(inputs.first),
                "act_occurrence_identity": assignment.material[
                    "measurement_act_occurrence_identity"
                ],
            },
            {
                "identity": assignment.material[
                    "second_participation_relation_identity"
                ],
                "role": "second relation of ordered path",
                "subject": _reference_material(inputs.second),
                "act_occurrence_identity": assignment.material[
                    "measurement_act_occurrence_identity"
                ],
            },
        ],
        "scope": assignment.material["scope"],
        "authority": assignment.material["authority"],
        "evidence_scope": "this exact Measurement Act occurrence",
        "limits": assignment.material["limits"],
        "unknown": assignment.material["unknown"],
    }


def record_shared_position_measurement_act_evidence(
    ledger: EventLedger,
    *,
    applicability_result_event_identity: str,
    locality_standing: dict[str, Any],
) -> Event:
    applicability, _act, assignment, inputs, applicability_material = (
        _read_applicability_result(
            ledger, applicability_result_event_identity
        )
    )
    if applicability_material["applicability"] != "applicable":
        raise SharedPairPositionError(
            "inapplicable pair-position inputs cannot participate"
        )
    boundary = _require_standing(
        ledger,
        inputs=inputs,
        locality_standing=locality_standing,
        carried_coordinate="applicability_result_occurrences",
        required_occurrences=(applicability.identity,),
    )
    return ledger.append(
        SHARED_POSITION_MEASUREMENT_ACT_EVIDENCE_KIND,
        _measurement_act_material(
            assignment=assignment,
            inputs=inputs,
            applicability=applicability,
            standing_boundary_identity=boundary,
        ),
        locality_identity=assignment.locality_identity,
    )


def _read_measurement_act(
    ledger: EventLedger,
    event_identity: str,
    *,
    assignment_reading: tuple[Event, SharedPairPositionInputs] | None = None,
) -> tuple[Event, Event, Event, SharedPairPositionInputs]:
    event = ledger.get(_identity(event_identity, "shared-position requires Act Evidence"))
    if (
        event is None
        or event.kind != SHARED_POSITION_MEASUREMENT_ACT_EVIDENCE_KIND
        or event.exact_material is not None
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise SharedPairPositionError("shared-position Measurement Act is corrupted")
    assignment_reference = event.material.get("responsibility_assignment_reference")
    applicability_reference = event.material.get("applicability_result_reference")
    if type(assignment_reference) is not dict or type(applicability_reference) is not dict:
        raise SharedPairPositionError("Measurement Act carries no exact inputs")
    if assignment_reading is None:
        assignment_reading = _read_assignment(
            ledger, assignment_reference.get("recorded_occurrence_identity")
        )
    assignment, inputs = assignment_reading
    if (
        assignment_reference.get("recorded_occurrence_identity")
        != assignment.identity
    ):
        raise SharedPairPositionError("Measurement Act carries no exact inputs")
    applicability_identity = applicability_reference.get("recorded_occurrence_identity")
    (
        applicability,
        _act,
        applicability_assignment,
        applicability_inputs,
        applicability_material,
    ) = _read_applicability_result(
        ledger,
        applicability_identity,
        assignment_reading=(assignment, inputs),
    )
    boundary = event.material.get("standing_boundary_identity")
    boundary_event = ledger.get(boundary) if type(boundary) is str else None
    expected = _measurement_act_material(
        assignment=assignment,
        inputs=inputs,
        applicability=applicability,
        standing_boundary_identity=boundary,
    )
    if (
        applicability_assignment.identity != assignment.identity
        or applicability_inputs != inputs
        or applicability_material["applicability"] != "applicable"
        or event.locality_identity != assignment.locality_identity
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
    return event, assignment, applicability, inputs


def get_shared_position_measurement_act_evidence(
    ledger: EventLedger, event_identity: str
) -> dict[str, Any]:
    event, _assignment, _applicability, _inputs_reading = _read_measurement_act(
        ledger, event_identity
    )
    return json.loads(json.dumps(event.material))


def _path_assertion(
    *,
    assignment: Event,
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
        "source_ingest_occurrence_identity": (
            inputs.first.source_ingest_occurrence_identity
        ),
        "completeness_boundary_identity": (
            inputs.first.completeness_boundary_identity
        ),
    }
    canonical = json.dumps(
        {
            "result": "ordered_relation_path",
            "subject": subject,
            "scope": scope,
            "content": content,
        },
        separators=(",", ":"),
    ).encode("utf-8")
    identity = "shared-pair-position:" + hashlib.sha256(canonical).hexdigest()
    return {
        "dimensions": {
            "identity": identity,
            "content": content,
            "source_provenance": "exact recorded pair position Assertions",
            "responsibility": SHARED_POSITION_ASSERTION_RESPONSIBILITY,
            "authority": "unestablished",
            "evidence_scope": "this exact shared-position Measurement result",
        },
        "subject_kind": "assertion",
        "responsible_boundary": "this recorded assertion",
        "result": "ordered_relation_path",
        "assertion_subject": subject,
        "assertion_scope": scope,
        "input_support": {
            "assertion_references": [
                inputs.first.assertion_reference,
                inputs.second.assertion_reference,
            ],
            "occurrence_references": [
                inputs.first.source_ingest_occurrence_identity,
                applicability.identity,
            ],
            "local_assertion_references": [],
        },
        "conflicts": "Unknown",
        "unknown": ["what this ordered relation path represents remains Unknown"],
        "limits": [
            "one path bounded by exact position Assertions and one exact shared "
            "position-coordinate reference"
        ],
    }


def _measurement_result_material(
    *,
    act: Event,
    assignment: Event,
    applicability: Event,
    inputs: SharedPairPositionInputs,
) -> dict[str, Any]:
    assertion = _path_assertion(
        assignment=assignment,
        inputs=inputs,
        applicability=applicability,
    )
    return {
        "result_identity": assignment.material["measurement_result_identity"],
        "dimensions": {
            "identity": assignment.material["measurement_result_identity"],
            "content": "one exact ordered relation-path Assertion",
            "source_provenance": "exact recorded pair position Assertions",
            "responsibility": RESPONSIBILITY,
            "responsible_boundary": "this Seed",
            "authority": assignment.material["authority"],
            "scope": assignment.material["scope"],
        },
        "exact_act": MEASUREMENT_ACT,
        "downstream_act_identity": assignment.material["measurement_act_identity"],
        "act_occurrence_identity": assignment.material[
            "measurement_act_occurrence_identity"
        ],
        "responsibility": RESPONSIBILITY,
        "responsible_boundary": SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY,
        "responsibility_assignment_evidence": {
            "responsible_boundary": SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY,
            "source_occurrence_references": [
                {
                    "occurrence_identity": (
                        inputs.first.recorded_occurrence_identity
                    )
                },
                {
                    "occurrence_identity": (
                        inputs.second.recorded_occurrence_identity
                    )
                },
            ],
            "completeness_boundary": (
                inputs.first.completeness_boundary_identity
            ),
            "determination": MEASUREMENT_RULE,
        },
        "responsibility_assignment_reference": _assignment_reference(assignment),
        "responsible_act_evidence_identity": act.identity,
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
        "scope": assignment.material["scope"],
        "authority": assignment.material["authority"],
        "limits": assignment.material["limits"],
        "unknown": assignment.material["unknown"],
    }


def _record_shared_measurement_yield_evidence(
    ledger: EventLedger, *, act: Event, result: dict[str, Any]
) -> Event:
    return _record_evidence_of_yield_relation(
        ledger,
        locality_identity=act.locality_identity,
        exact_act=MEASUREMENT_ACT,
        act_occurrence_identity=act.material["act_occurrence_identity"],
        responsible_act_evidence_identity=act.identity,
        result_kind=MEASUREMENT_RESULT_KIND,
        result_identity=result["result_identity"],
        result_content={
            coordinate: value
            for coordinate, value in result.items()
            if coordinate != "responsible_act_evidence_identity"
        },
        responsibility=RESPONSIBILITY,
        occurrence_boundary="shared_pair_position_measurement",
        responsible_boundary="this Seed",
    )


def record_shared_position_measurement_result(
    ledger: EventLedger,
    *,
    measurement_act_evidence_event_identity: str,
) -> Event:
    act, assignment, applicability, inputs = _read_measurement_act(
        ledger, measurement_act_evidence_event_identity
    )
    _refuse_existing_result(
        ledger,
        act=act,
        result_kind=SHARED_POSITION_MEASUREMENT_RESULT_KIND,
    )
    result = _measurement_result_material(
        act=act,
        assignment=assignment,
        applicability=applicability,
        inputs=inputs,
    )
    evidence = _record_shared_measurement_yield_evidence(
        ledger,
        act=act,
        result=result,
    )
    return ledger.append(
        SHARED_POSITION_MEASUREMENT_RESULT_KIND,
        _recorded_measurement_result_material(
            result,
            evidence_of_yield_relation_identity=evidence.identity,
        ),
        locality_identity=act.locality_identity,
    )


def _recorded_measurement_result_material(
    result: dict[str, Any],
    *,
    evidence_of_yield_relation_identity: str,
) -> dict[str, Any]:
    return {
        "result_identity": result["result_identity"],
        "dimensions": deepcopy(result["dimensions"]),
        "exact_act": result["exact_act"],
        "downstream_act_identity": result["downstream_act_identity"],
        "act_occurrence_identity": result["act_occurrence_identity"],
        "responsibility": result["responsibility"],
        "responsible_boundary": result["responsible_boundary"],
        "responsibility_assignment_evidence": deepcopy(
            result["responsibility_assignment_evidence"]
        ),
        "responsibility_assignment_reference": deepcopy(
            result["responsibility_assignment_reference"]
        ),
        "responsible_act_evidence_identity": result[
            "responsible_act_evidence_identity"
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
        "authority": deepcopy(result["authority"]),
        "limits": list(result["limits"]),
        "unknown": list(result["unknown"]),
        "evidence_of_yield_relation_identity": evidence_of_yield_relation_identity,
    }


def _read_measurement_result(
    ledger: EventLedger,
    event_identity: str,
    *,
    assignment_reading: tuple[Event, SharedPairPositionInputs] | None = None,
) -> tuple[Event, dict[str, Any]]:
    event = ledger.get(_identity(event_identity, "shared-position requires one result"))
    if (
        event is None
        or event.kind != SHARED_POSITION_MEASUREMENT_RESULT_KIND
        or event.exact_material is not None
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise SharedPairPositionError("shared-position Measurement result is corrupted")
    act_identity = event.material.get("responsible_act_evidence_identity")
    act, assignment, applicability, inputs = _read_measurement_act(
        ledger,
        act_identity,
        assignment_reading=assignment_reading,
    )
    expected = _measurement_result_material(
        act=act,
        assignment=assignment,
        applicability=applicability,
        inputs=inputs,
    )
    carried = {
        key: value
        for key, value in event.material.items()
        if key != "evidence_of_yield_relation_identity"
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


def get_recorded_shared_position_measurement(
    ledger: EventLedger, event_identity: str
) -> dict[str, Any]:
    _event, carried = _read_measurement_result(ledger, event_identity)
    return json.loads(json.dumps(carried))


def _incomplete_shared_position_assignment_for_determination(
    ledger: EventLedger,
    *,
    locality_identity: str,
    determination_result_event_identity: str,
) -> Event | None:
    def refers_to_determination(event: Event) -> bool:
        reference = event.material.get(D2_RESULT_REFERENCE_COORDINATE)
        return (
            type(reference) is dict
            and reference.get("recorded_occurrence_identity")
            == determination_result_event_identity
        )

    assignments = [
        event
        for event in ledger.iter_locality_kind(
            locality_identity, SHARED_POSITION_RESPONSIBILITY_ASSIGNMENT_KIND
        )
        if refers_to_determination(event)
    ]
    assignment_identities = {event.identity for event in assignments}
    results = []
    for event in ledger.iter_locality_kind(
        locality_identity, SHARED_POSITION_MEASUREMENT_RESULT_KIND
    ):
        reference = event.material.get("responsibility_assignment_reference")
        if (
            type(reference) is dict
            and reference.get("recorded_occurrence_identity")
            in assignment_identities
        ):
            results.append(event)
    if any(
        ledger.integrity_of(event.identity) == CORRUPTED
        for event in (*assignments, *results)
    ):
        raise SharedPairPositionError("shared-position lifecycle history is corrupted")
    if len(assignments) > 1 or len(results) > 1 or (results and not assignments):
        raise SharedPairPositionError("shared-position lifecycle history is ambiguous")
    return assignments[0] if assignments and not results else None


def _shared_events_for_assignment(
    ledger: EventLedger, *, assignment: Event, kind: str
) -> tuple[Event, ...]:
    matches = []
    for event in ledger.iter_locality_kind(assignment.locality_identity, kind):
        reference = event.material.get("responsibility_assignment_reference")
        if (
            type(reference) is dict
            and reference.get("recorded_occurrence_identity") == assignment.identity
        ):
            if ledger.integrity_of(event.identity) == CORRUPTED:
                raise SharedPairPositionError(
                    "shared-position partial lifecycle is corrupted"
                )
            matches.append(event)
    if len(matches) > 1:
        raise SharedPairPositionError("shared-position partial lifecycle is ambiguous")
    return tuple(matches)


def _shared_yield_for_act(ledger: EventLedger, *, act: Event) -> Event | None:
    matches = [
        event
        for event in ledger.iter_locality_kind(
            act.locality_identity, RECORDED_EVIDENCE_OF_YIELD_RELATION_KIND
        )
        if event.material.get("responsible_act_evidence_identity") == act.identity
    ]
    if any(ledger.integrity_of(event.identity) == CORRUPTED for event in matches):
        raise SharedPairPositionError("shared-position partial Yield is corrupted")
    if len(matches) > 1:
        raise SharedPairPositionError("shared-position partial Yield is ambiguous")
    return matches[0] if matches else None


def _require_shared_partial_yield(
    ledger: EventLedger,
    *,
    evidence: Event,
    act: Event,
    result_material: dict[str, Any],
    yielded_material: dict[str, Any],
    result_event_kind: str,
    yielded_result_kind: str,
    occurrence_boundary: str,
    act_occurrence_coordinate: str,
) -> None:
    expected = {
        "responsible_act_evidence_identity": act.identity,
        "result_identity": yielded_material["result_identity"],
        "dimensions": {
            "identity": (
                f"yield-evidence:{act.material[act_occurrence_coordinate]}:"
                f"{yielded_material['result_identity']}"
            ),
            "exact_act": act.material["act"],
            "act_occurrence_identity": act.material[act_occurrence_coordinate],
            "responsibility": RESPONSIBILITY,
            "responsible_boundary": "this Seed",
            "authority": "unestablished",
        },
        "coordinates_of_carried_result": list(yielded_material),
        "result": deepcopy(yielded_material),
        "coordinates_of_recorded_result": {
            coordinate: [coordinate] for coordinate in yielded_material
        },
        "result_kind": yielded_result_kind,
        "occurrence_boundary": occurrence_boundary,
    }
    if (
        evidence.kind != RECORDED_EVIDENCE_OF_YIELD_RELATION_KIND
        or evidence.exact_material is not None
        or evidence.locality_identity != act.locality_identity
        or evidence.material != expected
        or ledger.get(evidence.identity) != evidence
        or ledger.integrity_of(evidence.identity) == CORRUPTED
        or not ledger.list_locality(act.locality_identity)
        or ledger.list_locality(act.locality_identity)[-1].identity
        != evidence.identity
        or any(
            event.material.get("responsible_act_evidence_identity") == act.identity
            for event in ledger.iter_locality_kind(
                act.locality_identity, result_event_kind
            )
        )
        or result_material.get("responsible_act_evidence_identity") != act.identity
    ):
        raise SharedPairPositionError(
            "shared-position partial Yield cannot be continued"
        )


def _shared_continuation_write_snapshot(
    ledger: EventLedger, *, prior: Event
) -> tuple[Any, int]:
    locality_events = ledger.list_locality(prior.locality_identity)
    if (
        ledger.get(prior.identity) != prior
        or ledger.integrity_of(prior.identity) == CORRUPTED
        or not locality_events
        or locality_events[-1].identity != prior.identity
    ):
        raise SharedPairPositionError(
            "shared-position continuation prior phase is not Locality-current"
        )
    return ledger.append_boundary(), len(ledger.list())


def _require_shared_serialized_append(
    ledger: EventLedger, *, snapshot: tuple[Any, int], event: Event
) -> None:
    _boundary, count = snapshot
    events = ledger.list()
    if (
        len(events) != count + 1
        or events[-1] != event
        or ledger.append_boundary_through_occurrence(event.identity)
        != ledger.append_boundary()
    ):
        raise SharedPairPositionError(
            "shared-position continuation write was not globally serialized"
        )


def _continue_shared_position_measurement_lifecycle(
    ledger: EventLedger,
    *,
    responsibility_assignment_event_identity: str,
    locality_standing: dict[str, Any],
) -> tuple[dict[str, Any], Event]:
    """Continue one exact intact shared-position prefix after reopen."""

    from seed_runtime.operator_locality_standing import advance_operator_locality_standing

    assignment, inputs = _read_assignment(
        ledger, responsibility_assignment_event_identity
    )
    if (
        locality_standing.get("locality_identity") != assignment.locality_identity
        or assignment.identity
        not in locality_standing.get("responsibility_assignment_occurrences", {})
    ):
        raise SharedPairPositionError(
            "shared-position continuation requires its exact current Standing"
        )

    def advance(standing: dict[str, Any], event: Event) -> dict[str, Any]:
        return advance_operator_locality_standing(
            ledger,
            (event.identity,),
            locality_identity=assignment.locality_identity,
            prior=standing,
        )

    applicability_acts = _shared_events_for_assignment(
        ledger, assignment=assignment, kind=SHARED_POSITION_APPLICABILITY_ACT_EVIDENCE_KIND
    )
    applicability_results = _shared_events_for_assignment(
        ledger, assignment=assignment, kind=SHARED_POSITION_APPLICABILITY_RESULT_KIND
    )
    measurement_acts = _shared_events_for_assignment(
        ledger, assignment=assignment, kind=SHARED_POSITION_MEASUREMENT_ACT_EVIDENCE_KIND
    )
    measurement_results = _shared_events_for_assignment(
        ledger, assignment=assignment, kind=SHARED_POSITION_MEASUREMENT_RESULT_KIND
    )
    if measurement_results:
        raise SharedPairPositionError("shared-position lifecycle is already complete")
    if (
        (applicability_results and not applicability_acts)
        or (measurement_acts and not applicability_results)
    ):
        raise SharedPairPositionError("shared-position partial lifecycle order is false")

    if applicability_acts:
        applicability_act = applicability_acts[0]
        _read_applicability_act(ledger, applicability_act.identity)
    else:
        assignment, inputs = _read_assignment(ledger, assignment.identity)
        snapshot = _shared_continuation_write_snapshot(
            ledger, prior=assignment
        )
        applicability_act = ledger.append(
            SHARED_POSITION_APPLICABILITY_ACT_EVIDENCE_KIND,
            _applicability_act_material(
                assignment=assignment,
                inputs=inputs,
                standing_boundary_identity=assignment.identity,
            ),
            locality_identity=assignment.locality_identity,
        )
        _require_shared_serialized_append(
            ledger, snapshot=snapshot, event=applicability_act
        )
        locality_standing = advance(locality_standing, applicability_act)

    if applicability_results:
        applicability = applicability_results[0]
        _read_applicability_result(ledger, applicability.identity)
    else:
        applicability_material = _applicability_result_material(
            act=applicability_act, assignment=assignment, inputs=inputs
        )
        yielded_material = {
            coordinate: value
            for coordinate, value in applicability_material.items()
            if coordinate != "responsible_act_evidence_identity"
        }
        evidence = _shared_yield_for_act(ledger, act=applicability_act)
        if evidence is None:
            _refuse_existing_result(
                ledger,
                act=applicability_act,
                result_kind=SHARED_POSITION_APPLICABILITY_RESULT_KIND,
            )
            applicability_act, assignment, inputs = _read_applicability_act(
                ledger, applicability_act.identity
            )
            snapshot = _shared_continuation_write_snapshot(
                ledger, prior=applicability_act
            )
            evidence = _record_shared_applicability_yield_evidence(
                ledger, act=applicability_act, result=applicability_material
            )
            _require_shared_serialized_append(
                ledger, snapshot=snapshot, event=evidence
            )
        _require_shared_partial_yield(
            ledger,
            evidence=evidence,
            act=applicability_act,
            result_material=applicability_material,
            yielded_material=yielded_material,
            result_event_kind=SHARED_POSITION_APPLICABILITY_RESULT_KIND,
            yielded_result_kind=APPLICABILITY_RESULT_KIND,
            occurrence_boundary=APPLICABILITY_BOUNDARY,
            act_occurrence_coordinate="applicability_act_occurrence_identity",
        )
        snapshot = _shared_continuation_write_snapshot(ledger, prior=evidence)
        applicability = ledger.append(
            SHARED_POSITION_APPLICABILITY_RESULT_KIND,
            _recorded_applicability_result_material(
                applicability_material,
                evidence_of_yield_relation_identity=evidence.identity,
            ),
            locality_identity=assignment.locality_identity,
        )
        _require_shared_serialized_append(
            ledger, snapshot=snapshot, event=applicability
        )
        locality_standing = advance(locality_standing, applicability)

    if measurement_acts:
        measurement_act = measurement_acts[0]
        _read_measurement_act(ledger, measurement_act.identity)
    else:
        applicability, _app_act, assignment, inputs, applicability_material = (
            _read_applicability_result(ledger, applicability.identity)
        )
        snapshot = _shared_continuation_write_snapshot(
            ledger, prior=applicability
        )
        measurement_act = ledger.append(
            SHARED_POSITION_MEASUREMENT_ACT_EVIDENCE_KIND,
            _measurement_act_material(
                assignment=assignment,
                inputs=inputs,
                applicability=applicability,
                standing_boundary_identity=applicability.identity,
            ),
            locality_identity=assignment.locality_identity,
        )
        _require_shared_serialized_append(
            ledger, snapshot=snapshot, event=measurement_act
        )
        locality_standing = advance(locality_standing, measurement_act)

    result_material = _measurement_result_material(
        act=measurement_act,
        assignment=assignment,
        applicability=applicability,
        inputs=inputs,
    )
    yielded_material = {
        coordinate: value
        for coordinate, value in result_material.items()
        if coordinate != "responsible_act_evidence_identity"
    }
    evidence = _shared_yield_for_act(ledger, act=measurement_act)
    if evidence is None:
        _refuse_existing_result(
            ledger,
            act=measurement_act,
            result_kind=SHARED_POSITION_MEASUREMENT_RESULT_KIND,
        )
        measurement_act, assignment, applicability, inputs = _read_measurement_act(
            ledger, measurement_act.identity
        )
        result_material = _measurement_result_material(
            act=measurement_act,
            assignment=assignment,
            applicability=applicability,
            inputs=inputs,
        )
        yielded_material = {
            coordinate: value
            for coordinate, value in result_material.items()
            if coordinate != "responsible_act_evidence_identity"
        }
        snapshot = _shared_continuation_write_snapshot(
            ledger, prior=measurement_act
        )
        evidence = _record_shared_measurement_yield_evidence(
            ledger, act=measurement_act, result=result_material
        )
        _require_shared_serialized_append(
            ledger, snapshot=snapshot, event=evidence
        )
    _require_shared_partial_yield(
        ledger,
        evidence=evidence,
        act=measurement_act,
        result_material=result_material,
        yielded_material=yielded_material,
        result_event_kind=SHARED_POSITION_MEASUREMENT_RESULT_KIND,
        yielded_result_kind=MEASUREMENT_RESULT_KIND,
        occurrence_boundary=MEASUREMENT_BOUNDARY,
        act_occurrence_coordinate="act_occurrence_identity",
    )
    snapshot = _shared_continuation_write_snapshot(ledger, prior=evidence)
    result = ledger.append(
        SHARED_POSITION_MEASUREMENT_RESULT_KIND,
        _recorded_measurement_result_material(
            result_material,
            evidence_of_yield_relation_identity=evidence.identity,
        ),
        locality_identity=assignment.locality_identity,
    )
    _require_shared_serialized_append(
        ledger, snapshot=snapshot, event=result
    )
    locality_standing = advance(locality_standing, result)
    return locality_standing, result


def _record_shared_position_measurement_lifecycle_from_carried_d2_result(
    ledger: EventLedger,
    *,
    determination_result_event_identity: str,
    locality_standing: dict[str, Any],
) -> tuple[dict[str, Any], Event]:
    """Record the existing shared-position road from one exact two-ref D.2 result."""

    from seed_runtime.operator_locality_standing import (
        _exact_standing_additions,
        _record_distinct,
    )

    standing = deepcopy(locality_standing)
    locality_identity = standing.get("locality_identity")
    determination, inputs = _d2_result_inputs(
        ledger,
        result_event_identity=determination_result_event_identity,
        prior_standing=standing,
    )
    if len((inputs.first, inputs.second)) != 2:
        raise SharedPairPositionError(
            "shared-position assignment requires exactly two ordered D.2 Assertion references"
        )
    boundary = _require_exact_d2_result_standing(
        ledger,
        result=determination,
        inputs=inputs,
        locality_standing=standing,
    )
    locality_events = ledger.list_locality(locality_identity)
    if (
        not locality_events
        or locality_events[-1].identity != boundary
        or ledger.integrity_of(boundary) == CORRUPTED
    ):
        raise SharedPairPositionError(
            "shared-position assignment requires exact current Locality Standing"
        )
    initial_global_boundary = ledger.append_boundary()
    determination_material = deepcopy(determination.material)
    identities = _new_assignment_identities()
    if len(set(identities.values())) != len(identities):
        raise SharedPairPositionError("shared-position lifecycle identities collapsed")

    snapshots: list[tuple[Event, str, dict[str, Any]]] = [
        (determination, determination.kind, determination_material)
    ]

    def require_intact() -> None:
        for event, kind, material in snapshots:
            if (
                ledger.get(event.identity) != event
                or event.kind != kind
                or event.exact_material is not None
                or ledger.integrity_of(event.identity) == CORRUPTED
                or event.material != material
            ):
                raise SharedPairPositionError(
                    "shared-position carried source changed"
                )

    def result_reference(event: Event) -> dict[str, str]:
        return {
            "recorded_occurrence_identity": event.identity,
            "result_identity": event.material["result_identity"],
            "act_occurrence_identity": event.material["act_occurrence_identity"],
            "responsible_act_evidence_identity": event.material[
                "responsible_act_evidence_identity"
            ],
            "evidence_of_yield_relation_identity": event.material[
                "evidence_of_yield_relation_identity"
            ],
        }

    def carry(event: Event, *, prior: str) -> None:
        assignments = standing.get("responsibility_assignment_occurrences")
        applicability_results = standing.get("applicability_result_occurrences")
        measurements = standing.get("measurement_occurrences")
        count = standing.get("event_count")
        if (
            type(assignments) is not dict
            or type(applicability_results) is not dict
            or type(measurements) is not dict
            or type(count) is not int
            or standing.get("through_event_occurrence_identity") != prior
            or event.locality_identity != locality_identity
            or ledger.get(event.identity) != event
            or ledger.integrity_of(event.identity) == CORRUPTED
            or ledger.append_boundary_through_occurrence(event.identity)
            != ledger.append_boundary()
        ):
            raise SharedPairPositionError(
                "produced shared-position occurrence is not exact"
            )
        if event.kind == SHARED_POSITION_RESPONSIBILITY_ASSIGNMENT_KIND:
            lawful = (
                event.material.get("standing_boundary_identity") == prior
                and event.identity not in assignments
            )
        elif event.kind == SHARED_POSITION_APPLICABILITY_ACT_EVIDENCE_KIND:
            lawful = (
                event.material["responsibility_assignment_reference"][
                    "recorded_occurrence_identity"
                ]
                == prior
                and prior in assignments
            )
        elif event.kind == SHARED_POSITION_APPLICABILITY_RESULT_KIND:
            lawful = (
                event.material.get("responsible_act_evidence_identity") == prior
                and event.identity not in applicability_results
            )
        elif event.kind == SHARED_POSITION_MEASUREMENT_ACT_EVIDENCE_KIND:
            lawful = (
                event.material["applicability_result_reference"][
                    "recorded_occurrence_identity"
                ]
                == prior
                and prior in applicability_results
            )
        elif event.kind == SHARED_POSITION_MEASUREMENT_RESULT_KIND:
            lawful = (
                event.material.get("responsible_act_evidence_identity") == prior
                and event.identity not in measurements
            )
        else:
            lawful = False
        if not lawful:
            raise SharedPairPositionError(
                "produced shared-position occurrence has false Standing"
            )
        additions = _exact_standing_additions(
            standing,
            event,
            error_message="produced shared-position Standing is not exact",
        )
        if event.kind == SHARED_POSITION_RESPONSIBILITY_ASSIGNMENT_KIND:
            assignments[event.identity] = None
        elif event.kind == SHARED_POSITION_APPLICABILITY_RESULT_KIND:
            applicability_results[event.identity] = None
        elif event.kind == SHARED_POSITION_MEASUREMENT_RESULT_KIND:
            measurements[event.identity] = result_reference(event)
        for key, values in additions.items():
            for value in values:
                _record_distinct(standing[key], value)
        standing["through_event_occurrence_identity"] = event.identity
        standing["event_count"] = count + 1

    assignment_material = _assignment_material(
        inputs=inputs,
        standing_boundary_identity=boundary,
        identities=identities,
        determination_result_reference=_determination_result_reference(
            determination
        ),
    )
    if ledger.append_boundary() != initial_global_boundary:
        raise SharedPairPositionError(
            "shared-position global recording boundary changed before assignment"
        )
    assignment = ledger.append(
        SHARED_POSITION_RESPONSIBILITY_ASSIGNMENT_KIND,
        _assignment_material(
            inputs=inputs,
            standing_boundary_identity=boundary,
            identities=identities,
            determination_result_reference=_determination_result_reference(
                determination
            ),
        ),
        locality_identity=locality_identity,
    )
    snapshots.append((assignment, assignment.kind, deepcopy(assignment_material)))
    require_intact()
    carry(assignment, prior=boundary)

    applicability_act_material = _applicability_act_material(
        assignment=assignment,
        inputs=inputs,
        standing_boundary_identity=assignment.identity,
    )
    applicability_act = ledger.append(
        SHARED_POSITION_APPLICABILITY_ACT_EVIDENCE_KIND,
        _applicability_act_material(
            assignment=assignment,
            inputs=inputs,
            standing_boundary_identity=assignment.identity,
        ),
        locality_identity=locality_identity,
    )
    snapshots.append((applicability_act, applicability_act.kind, deepcopy(applicability_act_material)))
    require_intact()
    carry(applicability_act, prior=assignment.identity)

    applicability_material = _applicability_result_material(
        act=applicability_act,
        assignment=assignment,
        inputs=inputs,
    )
    evidence = _record_shared_applicability_yield_evidence(
        ledger,
        act=applicability_act,
        result=applicability_material,
    )
    require_intact()
    if ledger.append_boundary_through_occurrence(evidence.identity) != ledger.append_boundary():
        raise SharedPairPositionError("shared-position Yield left the append tip")
    applicability_recorded = _recorded_applicability_result_material(
        applicability_material,
        evidence_of_yield_relation_identity=evidence.identity,
    )
    applicability = ledger.append(
        SHARED_POSITION_APPLICABILITY_RESULT_KIND,
        _recorded_applicability_result_material(
            applicability_material,
            evidence_of_yield_relation_identity=evidence.identity,
        ),
        locality_identity=locality_identity,
    )
    snapshots.append((applicability, applicability.kind, deepcopy(applicability_recorded)))
    require_intact()
    carry(applicability, prior=applicability_act.identity)

    act_material = _measurement_act_material(
        assignment=assignment,
        inputs=inputs,
        applicability=applicability,
        standing_boundary_identity=applicability.identity,
    )
    act = ledger.append(
        SHARED_POSITION_MEASUREMENT_ACT_EVIDENCE_KIND,
        _measurement_act_material(
            assignment=assignment,
            inputs=inputs,
            applicability=applicability,
            standing_boundary_identity=applicability.identity,
        ),
        locality_identity=locality_identity,
    )
    snapshots.append((act, act.kind, deepcopy(act_material)))
    require_intact()
    carry(act, prior=applicability.identity)

    measured_material = _measurement_result_material(
        act=act,
        assignment=assignment,
        applicability=applicability,
        inputs=inputs,
    )
    measurement_evidence = _record_shared_measurement_yield_evidence(
        ledger,
        act=act,
        result=measured_material,
    )
    require_intact()
    if ledger.append_boundary_through_occurrence(measurement_evidence.identity) != ledger.append_boundary():
        raise SharedPairPositionError("shared-position Yield left the append tip")
    result_recorded = _recorded_measurement_result_material(
        measured_material,
        evidence_of_yield_relation_identity=measurement_evidence.identity,
    )
    result = ledger.append(
        SHARED_POSITION_MEASUREMENT_RESULT_KIND,
        _recorded_measurement_result_material(
            measured_material,
            evidence_of_yield_relation_identity=measurement_evidence.identity,
        ),
        locality_identity=locality_identity,
    )
    snapshots.append((result, result.kind, deepcopy(result_recorded)))
    require_intact()
    carry(result, prior=act.identity)
    return standing, result
