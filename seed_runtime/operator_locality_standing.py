"""Deterministic Locality Standing read over preserved acquisition_result events."""

from __future__ import annotations


from bisect import bisect_left
from contextvars import ContextVar
from copy import deepcopy
from functools import wraps
from typing import Any, Iterable

from seed_runtime.event import Event
from seed_runtime.events import CORRUPTED, EventLedger
from seed_runtime.material_source import (
    read_exact_material_result,
    read_material_locality_relation_requirements,
)
from seed_runtime.witness_material_source import WITNESS_MATERIAL_SOURCE_RECORDED_KIND
from seed_runtime.byte_measurement import (
    BYTE_MEASUREMENT_RECORDED_KIND,
    BYTE_MEASUREMENT_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND,
    BYTE_MEASUREMENT_RESPONSIBLE_ACT_OCCURRENCE_EVENT,
    BYTE_PAIR_MEASUREMENT_RECORDED_KIND,
    BYTE_PAIR_MEASUREMENT_RESULT_KIND,
    BYTE_PAIR_APPLICABILITY_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
    BYTE_PAIR_MEASUREMENT_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
    BYTE_PAIR_APPLICABILITY_ACT_OCCURRENCE_EVENT,
    BYTE_PAIR_APPLICABILITY_RECORDED_KIND,
    BYTE_PAIR_RESPONSIBLE_ACT_OCCURRENCE_EVENT,
    ASSERTION_LOCALITY_MOVEMENT_SUBJECT_TO_ACT_BINDING_KIND,
    ASSERTION_LOCALITY_MOVEMENT_ACT_OCCURRENCE_EVENT,
    ASSERTION_LOCALITY_MOVEMENT_KIND,
    ASSERTION_LOCALITY_MOVEMENT_RESULT_KIND,
    RecordedAssertionCarriedByLocalityMovement,
    RecordedByteAssertion,
    _AssertionLocalityMovementSource,
    _assertion_carried_by_locality_movement_result,
    _movement_act_material,
    _movement_assignment_material,
    _movement_result_material,
    _source_assertion_is_carried,
    _source_assertion_from_reference,
    _source_assertion_reference,
    _findings_of_recorded_byte_position_pair_measurement,
    _read_assertion_locality_movement_subject_to_act_binding,
    _read_assertion_locality_movement_act_occurrence,
    _require_exact_movement_assignment_and_source,
    _read_byte_measurement_responsibility_assignment,
    _read_pair_applicability_subject_to_act_binding,
    _read_pair_measurement_subject_to_act_binding,
    _read_pair_applicability_act_occurrence,
    _read_recorded_pair_input_applicability,
    _read_pair_measurement_act_occurrence,
    _pair_applicability_binding_of_result,
    _require_exact_pair_subject_to_act_binding_event,
    _require_exact_pair_applicability_act_event,
    _require_exact_pair_applicability_result_event,
    _require_exact_pair_measurement_act_event,
    _require_exact_pair_measurement_result_event,
    _validate_moved_byte_assertion,
    assertions_of_recorded_byte_measurement,
)
from seed_runtime.occurrence_position_measurement import (
    OCCURRENCE_POSITION_ACT_OCCURRENCE_EVENT,
    OCCURRENCE_POSITION_RECORDED_KIND,
    OCCURRENCE_POSITION_RESULT_KIND,
    OCCURRENCE_POSITION_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND,
    _occurrence_position_result_material,
    _position_assertions,
    _require_carried_occurrence_position_assignment,
    get_occurrence_position_measurement_responsibility_assignment,
    get_recorded_occurrence_position_measurement,
)
from seed_runtime.yield_relation import (
    RECORDED_YIELD_RELATION_EVENT,
    read_requirements_of_yield_relation,
)
from seed_runtime.measurement_of_recurrent_byte_pair_occurrence_position import (
    RECORDED_RESPONSIBILITY_ASSIGNMENT_OF_MEASUREMENT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_KIND,
    RECORDED_ACT_OCCURRENCE_OF_MEASUREMENT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_EVENT,
    RECORDING_OCCURRENCE_OF_RESULT_OF_MEASUREMENT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_KIND,
    _read_responsibility_assignment_for_measurement_of_recurrent_byte_pair_occurrence_position,
    _read_recorded_result_of_measurement_of_recurrent_byte_pair_occurrence_position,
)
from seed_runtime.measurement_of_position_coordinates_of_byte_pair_occurrences import (
    BYTE_PAIR_OCCURRENCE_POSITION_ASSIGNMENT_KIND,
    BYTE_PAIR_OCCURRENCE_POSITION_ACT_OCCURRENCE_EVENT,
    BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND,
    _require_carried_byte_pair_occurrence_position_assignment,
    get_byte_pair_occurrence_position_measurement_responsibility_assignment,
    get_byte_pair_occurrence_position_measurement_act_occurrence,
    get_recorded_byte_pair_occurrence_position_measurement,
)
from seed_runtime.measurement_of_shared_position_of_byte_pair_occurrences import (
    SHARED_POSITION_RESPONSIBILITY_ASSIGNMENT_KIND,
    SHARED_POSITION_APPLICABILITY_ACT_OCCURRENCE_EVENT,
    SHARED_POSITION_APPLICABILITY_RESULT_KIND,
    SHARED_POSITION_MEASUREMENT_ACT_OCCURRENCE_EVENT,
    SHARED_POSITION_MEASUREMENT_RESULT_KIND,
    _read_assignment as _read_shared_position_assignment,
    _read_applicability_act as _read_shared_position_applicability_act,
    _read_applicability_result as _read_shared_position_applicability_result,
    _read_measurement_act as _read_shared_position_measurement_act,
    _read_measurement_result as _read_shared_position_measurement_result,
    _SharedPositionReplayReading,
    _shared_position_replay_reading,
    _advance_shared_position_replay_reading,
)
from seed_runtime.addressed_byte_occurrence_reference_determination import (
    RESPONSIBILITY_ASSIGNMENT_KIND as ADDRESSED_BYTE_REFERENCE_RESPONSIBILITY_ASSIGNMENT_KIND,
    APPLICABILITY_ACT_OCCURRENCE_EVENT as ADDRESSED_BYTE_REFERENCE_APPLICABILITY_ACT_OCCURRENCE_EVENT,
    APPLICABILITY_RESULT_KIND as ADDRESSED_BYTE_REFERENCE_APPLICABILITY_RESULT_KIND,
    DETERMINATION_ACT_OCCURRENCE_EVENT as ADDRESSED_BYTE_REFERENCE_DETERMINATION_ACT_OCCURRENCE_EVENT,
    DETERMINATION_RESULT_KIND as ADDRESSED_BYTE_REFERENCE_DETERMINATION_RESULT_KIND,
    _read_assignment as _read_addressed_byte_reference_assignment,
    _read_applicability_act as _read_addressed_byte_reference_applicability_act,
    _read_applicability_result as _read_addressed_byte_reference_applicability_result,
    _read_determination_act as _read_addressed_byte_reference_determination_act,
    _read_determination_result as _read_addressed_byte_reference_determination_result,
    _determination_result_reference as _addressed_byte_reference_determination_coordinates,
)
from seed_runtime.operator_locality_continuation import (
    LOCALITY_CONTINUATION_ACT_OCCURRENCE_EVENT,
    LOCALITY_CONTINUATION_RECORDED_KIND,
    LOCALITY_CONTINUATION_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
    get_recorded_locality_continuation,
    get_locality_continuation_subject_to_act_binding,
)
from seed_runtime.operator_checkpoint import (
    STANDING_BOUNDARY_REFERENCE_ACT_OCCURRENCE_EVENT,
    STANDING_BOUNDARY_REFERENCE_RECORDED_KIND,
    STANDING_BOUNDARY_REFERENCE_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
    get_recorded_standing_boundary_reference,
    get_standing_boundary_reference_act_occurrence,
    get_standing_boundary_reference_subject_to_act_binding,
)
from seed_runtime.standing_boundary_locality import (
    RECORDED_STANDING_BOUNDARY_LOCALITY_ACT_OCCURRENCE_EVENT,
    RECORDED_STANDING_BOUNDARY_LOCALITY_RECORDED_KIND,
    RECORDED_STANDING_BOUNDARY_LOCALITY_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
    get_recorded_standing_boundary_locality,
    get_recorded_standing_boundary_locality_act_occurrence,
    get_recorded_standing_boundary_locality_subject_to_act_binding,
)
from seed_runtime.operator_material_source import (
    OPERATOR_MATERIAL_SOURCE_ACT_OCCURRENCE_EVENT,
    OPERATOR_MATERIAL_SOURCE_RECORDED_KIND,
    OPERATOR_MATERIAL_SOURCE_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
    get_operator_material_source_act_occurrence,
    get_operator_material_source_subject_to_act_binding,
    get_recorded_operator_material_source,
)
from seed_runtime.operator_invocation_locality import (
    OPERATOR_INVOCATION_LOCALITY_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
    OPERATOR_INVOCATION_LOCALITY_ACT_OCCURRENCE_EVENT,
    OPERATOR_INVOCATION_LOCALITY_RECORDED_KIND,
    get_operator_invocation_locality_subject_to_act_binding,
    get_operator_invocation_locality_act_occurrence,
    get_recorded_operator_invocation_locality,
)
from seed_runtime.comparison_of_recorded_byte_pair_measurements import (
    RECORDED_PAIR_MEASUREMENT_COMPARISON_RESPONSIBILITY_ASSIGNMENT_KIND,
    RECORDED_PAIR_MEASUREMENT_COMPARISON_APPLICABILITY_ACT_OCCURRENCE_EVENT,
    RECORDED_PAIR_MEASUREMENT_COMPARISON_APPLICABILITY_RESULT_KIND,
    RECORDED_PAIR_MEASUREMENT_COMPARISON_ACT_OCCURRENCE_EVENT,
    RECORDED_PAIR_MEASUREMENT_COMPARISON_RESULT_KIND,
    RecordedPairMeasurementComparisonError,
    _assignment_reading as _recorded_pair_comparison_assignment_reading,
    _applicability_act_reading as _recorded_pair_comparison_applicability_act_reading,
    _applicability_reading as _recorded_pair_comparison_applicability_reading,
    _comparison_act_reading as _recorded_pair_comparison_act_reading,
    _recorded_pair_measurement_comparison_reading,
)
from seed_runtime.comparison_of_ordered_relation_path_with_recorded_pair_findings import (
    COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_RESPONSIBILITY_ASSIGNMENT_KIND,
    COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_APPLICABILITY_ACT_OCCURRENCE_EVENT,
    COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_APPLICABILITY_RESULT_KIND,
    COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_COMPARE_ACT_OCCURRENCE_EVENT,
    COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_RESULT_KIND,
    get_comparison_of_ordered_relation_path_with_recorded_pair_findings_responsibility_assignment,
    get_comparison_of_ordered_relation_path_with_recorded_pair_findings_applicability_act_occurrence,
    get_recorded_comparison_of_ordered_relation_path_with_recorded_pair_findings_applicability,
    get_comparison_of_ordered_relation_path_with_recorded_pair_findings_act_occurrence,
    get_recorded_comparison_of_ordered_relation_path_with_recorded_pair_findings,
)
from seed_runtime.comparison_of_ordered_path_source_position_material import (
    APPLICABILITY_ACT_KIND as ORDERED_PATH_SOURCE_POSITION_COMPARE_APPLICABILITY_ACT_KIND,
    APPLICABILITY_RESULT_KIND as ORDERED_PATH_SOURCE_POSITION_COMPARE_APPLICABILITY_RESULT_KIND,
    COMPARE_ACT_KIND as ORDERED_PATH_SOURCE_POSITION_COMPARE_ACT_KIND,
    COMPARE_RESULT_KIND as ORDERED_PATH_SOURCE_POSITION_COMPARE_RESULT_KIND,
    validate_ordered_path_source_position_material_comparison_event,
)
from seed_runtime.source_position_recurrence import (
    COMPARE_APPLICABILITY_RESPONSIBILITY_KIND,
    COMPARE_RESPONSIBILITY_KIND,
    SOURCE_POSITION_MEASUREMENT_RESPONSIBILITY_KIND,
    RECURRENCE_MEASUREMENT_RESPONSIBILITY_KIND,
    COORDINATE_MEASUREMENT_RESPONSIBILITY_KIND,
    RECURRENT_RESULT_MATERIAL_MEASUREMENT_RESPONSIBILITY_KIND,
    COMPARE_APPLICABILITY_ACT_KIND as SOURCE_POSITION_RECURRENCE_COMPARE_APPLICABILITY_ACT_KIND,
    COMPARE_APPLICABILITY_RESULT_KIND as SOURCE_POSITION_RECURRENCE_COMPARE_APPLICABILITY_RESULT_KIND,
    COMPARE_ACT_KIND as SOURCE_POSITION_RECURRENCE_COMPARE_ACT_KIND,
    COMPARE_RESULT_KIND as SOURCE_POSITION_RECURRENCE_COMPARE_RESULT_KIND,
    SOURCE_POSITION_MEASUREMENT_ACT_KIND,
    SOURCE_POSITION_MEASUREMENT_RESULT_KIND,
    RECURRENCE_MEASUREMENT_ACT_KIND as SOURCE_POSITION_RECURRENCE_MEASUREMENT_ACT_KIND,
    RECURRENCE_MEASUREMENT_RESULT_KIND as SOURCE_POSITION_RECURRENCE_MEASUREMENT_RESULT_KIND,
    COORDINATE_MEASUREMENT_ACT_KIND as CORRESPONDING_COORDINATE_MEASUREMENT_ACT_KIND,
    COORDINATE_MEASUREMENT_RESULT_KIND as CORRESPONDING_COORDINATE_MEASUREMENT_RESULT_KIND,
    RECURRENT_RESULT_MATERIAL_MEASUREMENT_ACT_KIND,
    RECURRENT_RESULT_MATERIAL_MEASUREMENT_RESULT_KIND,
    validate_source_position_recurrence_event,
)
# The writer declares the storage-routing values. A reader declaring another
# copy would create a second contract free to drift from the first.


_OPERATOR_STANDING_VALIDATION_CONTEXT: ContextVar[
    dict[str, Any] | None
] = ContextVar(
    "operator_standing_replay_validation_context",
    default=None,
)
_OPERATOR_STANDING_EXACT_ACCUMULATORS: ContextVar[
    tuple[Any, Any, Any, Any, Any] | None
] = ContextVar("operator_standing_exact_accumulators", default=None)


def _recorded_pair_comparison_replay_carry(
    ledger: EventLedger, assignment_reading: Any
) -> dict[str, Any]:
    if (
        type(assignment_reading) is not tuple
        or len(assignment_reading) != 2
        or type(assignment_reading[1]) is not dict
    ):
        raise RecordedPairMeasurementComparisonError(
            "comparison replay requires one exact assignment reading"
        )
    assignment, inputs = assignment_reading
    earlier = inputs.get("earlier_event")
    later = inputs.get("later_event")
    occurrences = (assignment, earlier, later)
    if any(
        event is None
        or type(event.identity) is not str
        or type(event.kind) is not str
        or type(event.material) is not dict
        for event in occurrences
    ):
        raise RecordedPairMeasurementComparisonError(
            "comparison replay requires exact assignment inputs"
        )
    carry = {
        "responsibility_assignment": assignment_reading,
        "exact_boundary": ledger.append_boundary(),
        "occurrences": tuple(
            {
                "identity": event.identity,
                "kind": event.kind,
                "locality_identity": event.locality_identity,
                "exact_material": deepcopy(event.exact_material),
                "material": deepcopy(event.material),
            }
            for event in occurrences
        ),
    }
    _validate_recorded_pair_comparison_replay_carry(ledger, carry)
    return carry


def _validate_recorded_pair_comparison_replay_carry(
    ledger: EventLedger, carry: Any
) -> Any:
    if (
        type(carry) is not dict
        or set(carry) != {
            "responsibility_assignment",
            "exact_boundary",
            "occurrences",
        }
        or type(carry["occurrences"]) is not tuple
        or len(carry["occurrences"]) != 3
        or ledger.append_boundary() != carry["exact_boundary"]
    ):
        raise RecordedPairMeasurementComparisonError(
            "comparison replay carry crossed its exact boundary"
        )
    for snapshot in carry["occurrences"]:
        if type(snapshot) is not dict:
            raise RecordedPairMeasurementComparisonError(
                "comparison replay carry is malformed"
            )
        current = ledger.get(snapshot.get("identity"))
        if (
            current is None
            or current.kind != snapshot.get("kind")
            or current.locality_identity != snapshot.get("locality_identity")
            or current.exact_material != snapshot.get("exact_material")
            or current.material != snapshot.get("material")
            or ledger.integrity_of(current.identity) == CORRUPTED
        ):
            raise RecordedPairMeasurementComparisonError(
                "comparison replay carry changed after validation"
            )
    if ledger.append_boundary() != carry["exact_boundary"]:
        raise RecordedPairMeasurementComparisonError(
            "comparison replay carry crossed its exact boundary"
        )
    return carry["responsibility_assignment"]


def _recorded_pair_comparison_assignment_identity(event: Any) -> str | None:
    reference = (
        event.material.get("responsibility_assignment_reference")
        if type(event.material) is dict
        else None
    )
    identity = (
        reference.get("recorded_occurrence_identity")
        if type(reference) is dict
        else None
    )
    return identity if type(identity) is str and identity else None


def _operator_standing_replay_validation(function):
    """Bound exact replay-only Standing context, including nested reads."""

    @wraps(function)
    def bounded(*args, **kwargs):
        token = _OPERATOR_STANDING_VALIDATION_CONTEXT.set(None)
        exact_token = _OPERATOR_STANDING_EXACT_ACCUMULATORS.set(None)
        try:
            return function(*args, **kwargs)
        finally:
            _OPERATOR_STANDING_EXACT_ACCUMULATORS.reset(exact_token)
            _OPERATOR_STANDING_VALIDATION_CONTEXT.reset(token)

    return bounded


def _set_operator_standing_validation_context(
    ledger: EventLedger,
    *,
    locality_identity: str,
    through_event_occurrence_identity: str | None,
    measurement_occurrences: dict[str, Any],
    material_acquisition_result_occurrences: list[dict[str, Any]],
    subject_to_act_binding_occurrences: dict[str, None],
) -> None:
    bound = _OPERATOR_STANDING_VALIDATION_CONTEXT.get()
    exact = _OPERATOR_STANDING_EXACT_ACCUMULATORS.get()
    if (
        type(bound) is not dict
        or bound.get("ledger") is not ledger
        or bound.get("locality_identity") != locality_identity
        or type(exact) is not tuple
        or len(exact) != 5
        or exact[0] is not ledger
        or exact[1] != locality_identity
        or exact[2] is not measurement_occurrences
        or exact[3] is not material_acquisition_result_occurrences
        or exact[4] is not subject_to_act_binding_occurrences
    ):
        raise ValueError(
            "operator Standing replay context requires its exact accumulators"
        )
    _OPERATOR_STANDING_VALIDATION_CONTEXT.set(
        {
            "ledger": ledger,
            "locality_identity": locality_identity,
            "through_event_occurrence_identity": (
                through_event_occurrence_identity
            ),
            "measurement_occurrences": measurement_occurrences,
            "material_acquisition_result_occurrences": material_acquisition_result_occurrences,
            "subject_to_act_binding_occurrences": (
                subject_to_act_binding_occurrences
            ),
        }
    )


def _operator_standing_validation_context(
    ledger: EventLedger, *, locality_identity: str
) -> dict[str, Any] | None:
    context = _OPERATOR_STANDING_VALIDATION_CONTEXT.get()
    if (
        type(context) is not dict
        or context.get("ledger") is not ledger
        or context.get("locality_identity") != locality_identity
    ):
        return None
    return {
        key: value
        for key, value in context.items()
        if key != "ledger"
    }

_SUBJECT_BY_KIND = {
    WITNESS_MATERIAL_SOURCE_RECORDED_KIND: "material_acquisition_result_occurrence",
}
_MEASUREMENT_ACT_OCCURRENCE_EVENTS = {
    BYTE_MEASUREMENT_RESPONSIBLE_ACT_OCCURRENCE_EVENT,
    OCCURRENCE_POSITION_ACT_OCCURRENCE_EVENT,
    RECORDED_ACT_OCCURRENCE_OF_MEASUREMENT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_EVENT,
    BYTE_PAIR_OCCURRENCE_POSITION_ACT_OCCURRENCE_EVENT,
}
_MEASUREMENT_RESPONSIBILITY_ASSIGNMENT_KINDS = {
    BYTE_MEASUREMENT_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND,
    OCCURRENCE_POSITION_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND,
    RECORDED_RESPONSIBILITY_ASSIGNMENT_OF_MEASUREMENT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_KIND,
    BYTE_PAIR_OCCURRENCE_POSITION_ASSIGNMENT_KIND,
    ASSERTION_LOCALITY_MOVEMENT_SUBJECT_TO_ACT_BINDING_KIND,
    BYTE_PAIR_APPLICABILITY_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
    BYTE_PAIR_MEASUREMENT_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
}
_MEASUREMENT_RECORDED_KINDS = {
    BYTE_MEASUREMENT_RECORDED_KIND,
    BYTE_PAIR_MEASUREMENT_RECORDED_KIND,
    OCCURRENCE_POSITION_RECORDED_KIND,
    RECORDING_OCCURRENCE_OF_RESULT_OF_MEASUREMENT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_KIND,
    SHARED_POSITION_MEASUREMENT_RESULT_KIND,
    BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND,
}
_ASSERTION_LOCALITY_MOVEMENT_KINDS = {
    ASSERTION_LOCALITY_MOVEMENT_SUBJECT_TO_ACT_BINDING_KIND,
    ASSERTION_LOCALITY_MOVEMENT_ACT_OCCURRENCE_EVENT,
    ASSERTION_LOCALITY_MOVEMENT_KIND,
}
_BYTE_PAIR_MEASUREMENT_LIFECYCLE_KINDS = {
    BYTE_PAIR_APPLICABILITY_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
    BYTE_PAIR_MEASUREMENT_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
    BYTE_PAIR_APPLICABILITY_ACT_OCCURRENCE_EVENT,
    BYTE_PAIR_APPLICABILITY_RECORDED_KIND,
    BYTE_PAIR_RESPONSIBLE_ACT_OCCURRENCE_EVENT,
    BYTE_PAIR_MEASUREMENT_RECORDED_KIND,
}
_LOCALITY_CONTINUATION_KINDS = {
    LOCALITY_CONTINUATION_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
    LOCALITY_CONTINUATION_ACT_OCCURRENCE_EVENT,
    LOCALITY_CONTINUATION_RECORDED_KIND,
}
_STANDING_BOUNDARY_REFERENCE_KINDS = {
    STANDING_BOUNDARY_REFERENCE_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
    STANDING_BOUNDARY_REFERENCE_ACT_OCCURRENCE_EVENT,
    STANDING_BOUNDARY_REFERENCE_RECORDED_KIND,
}
_RECORDED_STANDING_BOUNDARY_LOCALITY_KINDS = {
    RECORDED_STANDING_BOUNDARY_LOCALITY_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
    RECORDED_STANDING_BOUNDARY_LOCALITY_ACT_OCCURRENCE_EVENT,
    RECORDED_STANDING_BOUNDARY_LOCALITY_RECORDED_KIND,
}
_OPERATOR_MATERIAL_SOURCE_KINDS = {
    OPERATOR_MATERIAL_SOURCE_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
    OPERATOR_MATERIAL_SOURCE_ACT_OCCURRENCE_EVENT,
    OPERATOR_MATERIAL_SOURCE_RECORDED_KIND,
}
_OPERATOR_INVOCATION_LOCALITY_KINDS = {
    OPERATOR_INVOCATION_LOCALITY_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
    OPERATOR_INVOCATION_LOCALITY_ACT_OCCURRENCE_EVENT,
    OPERATOR_INVOCATION_LOCALITY_RECORDED_KIND,
}
_RECORDED_PAIR_MEASUREMENT_COMPARISON_KINDS = {
    RECORDED_PAIR_MEASUREMENT_COMPARISON_RESPONSIBILITY_ASSIGNMENT_KIND,
    RECORDED_PAIR_MEASUREMENT_COMPARISON_APPLICABILITY_ACT_OCCURRENCE_EVENT,
    RECORDED_PAIR_MEASUREMENT_COMPARISON_APPLICABILITY_RESULT_KIND,
    RECORDED_PAIR_MEASUREMENT_COMPARISON_ACT_OCCURRENCE_EVENT,
    RECORDED_PAIR_MEASUREMENT_COMPARISON_RESULT_KIND,
}
_SHARED_POSITION_MEASUREMENT_KINDS = {
    SHARED_POSITION_RESPONSIBILITY_ASSIGNMENT_KIND,
    SHARED_POSITION_APPLICABILITY_ACT_OCCURRENCE_EVENT,
    SHARED_POSITION_APPLICABILITY_RESULT_KIND,
    SHARED_POSITION_MEASUREMENT_ACT_OCCURRENCE_EVENT,
    SHARED_POSITION_MEASUREMENT_RESULT_KIND,
}
_ADDRESSED_BYTE_REFERENCE_DETERMINATION_KINDS = {
    ADDRESSED_BYTE_REFERENCE_RESPONSIBILITY_ASSIGNMENT_KIND,
    ADDRESSED_BYTE_REFERENCE_APPLICABILITY_ACT_OCCURRENCE_EVENT,
    ADDRESSED_BYTE_REFERENCE_APPLICABILITY_RESULT_KIND,
    ADDRESSED_BYTE_REFERENCE_DETERMINATION_ACT_OCCURRENCE_EVENT,
    ADDRESSED_BYTE_REFERENCE_DETERMINATION_RESULT_KIND,
}
_COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_KINDS = {
    COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_RESPONSIBILITY_ASSIGNMENT_KIND,
    COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_APPLICABILITY_ACT_OCCURRENCE_EVENT,
    COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_APPLICABILITY_RESULT_KIND,
    COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_COMPARE_ACT_OCCURRENCE_EVENT,
    COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_RESULT_KIND,
}
_ORDERED_PATH_SOURCE_POSITION_MATERIAL_COMPARISON_KINDS = {
    ORDERED_PATH_SOURCE_POSITION_COMPARE_APPLICABILITY_ACT_KIND,
    ORDERED_PATH_SOURCE_POSITION_COMPARE_APPLICABILITY_RESULT_KIND,
    ORDERED_PATH_SOURCE_POSITION_COMPARE_ACT_KIND,
    ORDERED_PATH_SOURCE_POSITION_COMPARE_RESULT_KIND,
}
_SOURCE_POSITION_RECURRENCE_KINDS = {
    COMPARE_APPLICABILITY_RESPONSIBILITY_KIND,
    COMPARE_RESPONSIBILITY_KIND,
    SOURCE_POSITION_MEASUREMENT_RESPONSIBILITY_KIND,
    RECURRENCE_MEASUREMENT_RESPONSIBILITY_KIND,
    COORDINATE_MEASUREMENT_RESPONSIBILITY_KIND,
    RECURRENT_RESULT_MATERIAL_MEASUREMENT_RESPONSIBILITY_KIND,
    SOURCE_POSITION_RECURRENCE_COMPARE_APPLICABILITY_ACT_KIND,
    SOURCE_POSITION_RECURRENCE_COMPARE_APPLICABILITY_RESULT_KIND,
    SOURCE_POSITION_RECURRENCE_COMPARE_ACT_KIND,
    SOURCE_POSITION_RECURRENCE_COMPARE_RESULT_KIND,
    SOURCE_POSITION_MEASUREMENT_ACT_KIND,
    SOURCE_POSITION_MEASUREMENT_RESULT_KIND,
    SOURCE_POSITION_RECURRENCE_MEASUREMENT_ACT_KIND,
    SOURCE_POSITION_RECURRENCE_MEASUREMENT_RESULT_KIND,
    CORRESPONDING_COORDINATE_MEASUREMENT_ACT_KIND,
    CORRESPONDING_COORDINATE_MEASUREMENT_RESULT_KIND,
    RECURRENT_RESULT_MATERIAL_MEASUREMENT_ACT_KIND,
    RECURRENT_RESULT_MATERIAL_MEASUREMENT_RESULT_KIND,
}
_SUPPORTED_KINDS = {
    *_SUBJECT_BY_KIND,
    *_MEASUREMENT_ACT_OCCURRENCE_EVENTS,
    *_MEASUREMENT_RESPONSIBILITY_ASSIGNMENT_KINDS,
    *_MEASUREMENT_RECORDED_KINDS,
    *_ASSERTION_LOCALITY_MOVEMENT_KINDS,
    *_BYTE_PAIR_MEASUREMENT_LIFECYCLE_KINDS,
    *_LOCALITY_CONTINUATION_KINDS,
    *_STANDING_BOUNDARY_REFERENCE_KINDS,
    *_RECORDED_STANDING_BOUNDARY_LOCALITY_KINDS,
    *_OPERATOR_MATERIAL_SOURCE_KINDS,
    *_OPERATOR_INVOCATION_LOCALITY_KINDS,
    *_RECORDED_PAIR_MEASUREMENT_COMPARISON_KINDS,
    *_SHARED_POSITION_MEASUREMENT_KINDS,
    *_ADDRESSED_BYTE_REFERENCE_DETERMINATION_KINDS,
    *_COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_KINDS,
    *_ORDERED_PATH_SOURCE_POSITION_MATERIAL_COMPARISON_KINDS,
    *_SOURCE_POSITION_RECURRENCE_KINDS,
}


def _record_distinct(collected: list[str], value: str) -> None:
    """Keep one sorted, distinct sequence in place.

    The returned coordinate is a sorted list of distinct strings, as it has
    always been.  Adding a value already present does nothing, so an advance
    that yields no new value costs nothing.
    """

    index = bisect_left(collected, value)
    if index == len(collected) or collected[index] != value:
        collected.insert(index, value)


def _exact_standing_additions(
    locality_standing: dict[str, Any], event, *, error_message: str
) -> dict[str, list[str]]:
    """Validate every added Standing coordinate before changing Standing."""

    additions = {}
    for key in ("known_loss", "unknown", "conflicts"):
        collected = locality_standing.get(key)
        added = event.material.get(key, [])
        if (
            type(collected) is not list
            or type(added) is not list
            or any(type(value) is not str for value in added)
        ):
            raise ValueError(error_message)
        additions[key] = added
    return additions


def _measurement_occurrence_coordinates(event) -> dict[str, str]:
    """Carry only the identities of one already-validated Measurement result."""

    return {
        "recorded_occurrence_identity": event.identity,
        "result_identity": event.material["result_identity"],
        "act_occurrence_identity": event.material["act_occurrence_identity"],
    "act_occurrence_event_identity": event.material[
            "act_occurrence_event_identity"
        ],
        "yield_relation_identity": event.material["yield_relation_identity"],
    }


def _assertion_locality_movement_occurrence_coordinates(
    ledger: EventLedger, event: Event
) -> dict[str, Any]:
    binding_reference = event.material["subject_to_act_binding_reference"]
    assignment = ledger.get(binding_reference["recorded_occurrence_identity"])
    if assignment is None:
        raise ValueError("Assertion Locality movement Standing is not exact")
    source_reference = assignment.material["source_assertion_reference"]
    source_event = ledger.get(source_reference["recorded_occurrence_identity"])
    if source_event is None:
        raise ValueError("Assertion Locality movement Standing is not exact")
    return {
        "recorded_occurrence_identity": event.identity,
        "result_identity": event.material["result_identity"],
        "source_assertion_reference": deepcopy(source_reference),
        "source_assertion_coordinates": deepcopy(
            assignment.material["source_assertion_coordinates"]
        ),
        "source_through_event_occurrence_identity": assignment.material[
            "source_through_event_occurrence_identity"
        ],
        "subject_to_act_binding_reference": deepcopy(binding_reference),
        "act_occurrence_event_identity": event.material[
            "act_occurrence_event_identity"
        ],
        "movement_act_occurrence_identity": event.material[
            "movement_act_occurrence_identity"
        ],
        "yield_relation_identity": event.material[
            "yield_relation_identity"
        ],
    }


_REQUIRED_GENERATED_BINDING_COORDINATES = frozenset(
    {
        "recorded_occurrence_identity",
        "assignment_identity",
        "assignment_subject_identity",
        "book_clause_identity",
        "result_boundary_identity",
    }
)
_REQUIRED_DIRECT_BINDING_COORDINATES = frozenset(
    {
        "recorded_occurrence_identity",
        "book_clause_identity",
        "exact_act_identity",
        "subject_reference",
        "result_boundary_identity",
    }
)


_NO_RESULT_COORDINATE = object()


def _result_subject_to_act_binding_coordinate(
    ledger: EventLedger, event
) -> dict[str, Any] | object:
    """Return one exact A.1 subject-to-Act binding, or its absence.

    Whether a result carries exact bytes or structured coordinates does not
    determine its subject-to-Act binding. Any intact result with an exact Yield
    and an exact recorded binding carries that binding beside the result. A
    yielded result without a recorded binding is not a positive A.1 coordinate.
    An incomplete recorded reference is refused.
    """

    if ledger.integrity_of(event.identity) == CORRUPTED:
        return _NO_RESULT_COORDINATE
    requirements = read_requirements_of_yield_relation(
        ledger,
        recorded_result_event_identity=event.identity,
        yield_relation_event_identity=event.material.get(
            "yield_relation_identity"
        ),
        act_occurrence_event_identity=event.material.get(
            "act_occurrence_event_identity"
        ),
    )
    if not all(requirements.values()):
        return _NO_RESULT_COORDINATE
    ownership = _subject_to_act_binding_of_exact_result(ledger, event)
    if ownership is not None:
        return ownership
    return _NO_RESULT_COORDINATE


def _subject_to_act_binding_of_exact_result(
    ledger: EventLedger, event
) -> dict[str, Any] | None:
    """Read the exact subject-to-Act binding carried by one yielded result.

    The Act occurrence carries the binding, its subject, and the Book clause.
    This read composes none of those coordinates. ``None`` reports that no
    binding was recorded. A malformed or disagreeing recorded reference is
    refused rather than reduced to absence.
    """

    act_occurrence_event_identity = event.material.get("act_occurrence_event_identity")
    if type(act_occurrence_event_identity) is not str or not act_occurrence_event_identity:
        return None
    act_occurrence = ledger.get(act_occurrence_event_identity)
    if act_occurrence is None:
        return None
    reference = act_occurrence.material.get("subject_to_act_binding_reference")
    if reference is None:
        reference = act_occurrence.material.get(
            "responsibility_assignment_reference"
        )
    if reference is None:
        return None
    if ledger.integrity_of(act_occurrence.identity) == CORRUPTED:
        raise ValueError(
            "recorded subject-to-Act binding requires its intact Act occurrence"
        )
    generated_identity_shape = (
        type(reference) is dict
        and _REQUIRED_GENERATED_BINDING_COORDINATES <= set(reference)
        and all(type(value) is str and value for value in reference.values())
    )
    direct_shape = (
        type(reference) is dict
        and set(reference) == _REQUIRED_DIRECT_BINDING_COORDINATES
        and all(
            type(reference.get(coordinate)) is str
            and reference[coordinate]
            for coordinate in _REQUIRED_DIRECT_BINDING_COORDINATES
            - {"subject_reference"}
        )
        and type(reference.get("subject_reference")) is dict
        and bool(reference["subject_reference"])
    )
    if not (generated_identity_shape or direct_shape):
        raise ValueError(
            "recorded subject-to-Act binding requires its exact coordinates"
        )
    binding_event = ledger.get(reference["recorded_occurrence_identity"])
    if (
        binding_event is None
        or binding_event.locality_identity != event.locality_identity
        or ledger.integrity_of(binding_event.identity) == CORRUPTED
    ):
        raise ValueError(
            "recorded subject-to-Act binding requires its exact occurrence"
        )
    required_coordinates = (
        _REQUIRED_GENERATED_BINDING_COORDINATES
        if generated_identity_shape
        else _REQUIRED_DIRECT_BINDING_COORDINATES
    )
    for coordinate in required_coordinates - {
        "recorded_occurrence_identity",
        "result_boundary_identity",
    }:
        if binding_event.material.get(coordinate) != reference[coordinate]:
            raise ValueError(
                "recorded subject-to-Act binding disagrees with its occurrence"
            )
    declared_result_boundaries = {
        value
        for coordinate, value in binding_event.material.items()
        if (
            coordinate == "result_boundary_identity"
            or coordinate.endswith("_result_identity")
            or coordinate == "result_identity"
        )
        and type(value) is str
        and value
    }
    if reference["result_boundary_identity"] not in declared_result_boundaries:
        raise ValueError(
            "recorded subject-to-Act binding disagrees with its occurrence"
        )
    if reference["result_boundary_identity"] != event.material.get(
        "result_identity"
    ):
        raise ValueError(
            "recorded subject-to-Act binding names another result boundary"
        )
    return deepcopy(reference)


def _shared_position_assignment_reading(
    ledger: EventLedger,
    event,
    *,
    prior_standing: dict[str, Any],
):
    assignment_identity = event.identity
    if event.kind != SHARED_POSITION_RESPONSIBILITY_ASSIGNMENT_KIND:
        reference = event.material.get("responsibility_assignment_reference")
        assignment_identity = (
            reference.get("recorded_occurrence_identity")
            if type(reference) is dict
            else None
        )
    return _read_shared_position_assignment(
        ledger,
        assignment_identity,
        prior_standing=prior_standing,
    )


def _shared_position_assignment_identity(event: Event) -> str | None:
    if event.kind == SHARED_POSITION_RESPONSIBILITY_ASSIGNMENT_KIND:
        return event.identity
    reference = event.material.get("responsibility_assignment_reference")
    identity = (
        reference.get("recorded_occurrence_identity")
        if type(reference) is dict
        else None
    )
    return identity if type(identity) is str and identity else None


def read_operator_locality_standing(
    ledger: EventLedger, *, locality_identity: str
) -> dict[str, Any]:
    """Read bounded Locality-local Standing by replaying the whole Locality.

    Equivalent to advancing from no prior Standing over every recorded event.
    `#2376` established that advancing from a prior Standing over only the
    occurrences after its boundary yields the same result, so a caller that
    already holds its Standing and knows what it just recorded should use
    :func:`advance_operator_locality_standing` instead of replaying.
    """

    return advance_operator_locality_standing(
        ledger,
        (
            event.identity
            for event in ledger.list_locality(locality_identity)
        ),
        locality_identity=locality_identity,
    )


def read_operator_locality_standing_through(
    ledger: EventLedger,
    *,
    locality_identity: str,
    through_event_occurrence_identity: str | None,
) -> dict[str, Any]:
    """Read one Locality through one exact recorded occurrence.

    ``None`` is the exact empty Standing boundary.  Otherwise the ledger first
    resolves the occurrence to its existing append boundary and then reads only
    that prefix.  Later occurrences in the same or another Locality are neither
    selected nor copied into the returned Standing.
    """

    if type(locality_identity) is not str or not locality_identity:
        raise ValueError("Standing read requires one exact Locality identity")
    if through_event_occurrence_identity is None:
        event_identities: Iterable[str] = ()
    else:
        if type(through_event_occurrence_identity) is not str or not through_event_occurrence_identity:
            raise ValueError("Standing read requires one exact through occurrence")
        event = ledger.get(through_event_occurrence_identity)
        if (
            event is None
            or event.locality_identity != locality_identity
            or ledger.integrity_of(through_event_occurrence_identity) == CORRUPTED
        ):
            raise ValueError(
                "Standing through occurrence is absent, corrupted, or in another Locality"
            )
        boundary = ledger.append_boundary_through_occurrence(
            through_event_occurrence_identity
        )
        event_identities = (
            occurrence.identity
            for occurrence in ledger.list_locality(
                locality_identity, through=boundary
            )
        )
    standing = advance_operator_locality_standing(
        ledger,
        event_identities,
        locality_identity=locality_identity,
    )
    if standing["through_event_occurrence_identity"] != through_event_occurrence_identity:
        raise ValueError("Standing read did not reach its exact through occurrence")
    return standing


class CarriedRecordedStandingError(ValueError):
    """One carried recorded Standing reference could not be resolved."""


def _require_recorded_standing_identity(value: Any, message: str) -> str:
    if type(value) is not str or not value:
        raise CarriedRecordedStandingError(message)
    return value


def _source_reference_from_checkpoint(
    ledger: EventLedger, recorded_occurrence_identity: str
) -> dict[str, str | None]:
    recorded = get_recorded_standing_boundary_reference(
        ledger, recorded_occurrence_identity
    )
    source = recorded["source_reference"]
    return {
        "source_locality_identity": source["source_locality_identity"],
        "source_through_event_occurrence_identity": source[
            "standing_boundary_event_identity"
        ],
    }


def _source_reference_from_checkout(
    ledger: EventLedger, recorded_occurrence_identity: str
) -> dict[str, str | None]:
    relation = get_recorded_standing_boundary_locality(
        ledger, recorded_occurrence_identity
    )
    anchor = relation["standing_boundary_reference"]
    anchor_occurrence_identity = _require_recorded_standing_identity(
        anchor.get("recorded_occurrence_identity"),
        "recorded Standing Locality relation carries no exact boundary reference",
    )
    recorded = get_recorded_standing_boundary_reference(
        ledger, anchor_occurrence_identity
    )
    if anchor.get("result_identity") != recorded["result_identity"]:
        raise CarriedRecordedStandingError(
            "recorded Standing Locality relation names a different boundary result"
        )
    return _source_reference_from_checkpoint(ledger, anchor_occurrence_identity)


def read_carried_recorded_standing(
    ledger: EventLedger,
    *,
    locality_identity: str,
    recorded_occurrence_identity: str,
) -> dict[str, Any]:
    """Resolve one exact recorded Standing reference carried at one Locality.

    Checkpoint, Standing-continuation, and recorded-boundary Locality relations
    remain distinct durable occurrences.  This reader only gives their common
    source coordinates a common transient read.  It establishes no
    Applicability, Admission, Participation, Compare, or copied Standing at the
    addressing Locality.
    """

    _require_recorded_standing_identity(
        locality_identity, "recorded Standing read requires a Locality"
    )
    _require_recorded_standing_identity(
        recorded_occurrence_identity,
        "recorded Standing read requires one exact carried occurrence",
    )
    locality_standing = read_operator_locality_standing(
        ledger, locality_identity=locality_identity
    )
    carriers = (
        (
            "checkpoint",
            locality_standing["recorded_standing_boundary_references"],
        ),
        ("continuation", locality_standing["recorded_relation_Standing"]),
        (
            "checkout",
            locality_standing["recorded_standing_boundary_locality_relations"],
        ),
    )
    matches = []
    for carrier_name, carrier in carriers:
        if type(carrier) is not dict or any(
            value is not None for value in carrier.values()
        ):
            raise CarriedRecordedStandingError(
                "recorded Standing carrier is not exact"
            )
        if recorded_occurrence_identity in carrier:
            matches.append(carrier_name)
    if len(matches) != 1:
        raise CarriedRecordedStandingError(
            "recorded Standing occurrence is not carried exactly once at this Locality"
        )
    event = ledger.get(recorded_occurrence_identity)
    if event is None or event.locality_identity != locality_identity:
        raise CarriedRecordedStandingError(
            "recorded Standing occurrence has a different carrying Locality"
        )

    if matches[0] == "checkpoint":
        source_reference = _source_reference_from_checkpoint(
            ledger, recorded_occurrence_identity
        )
    elif matches[0] == "continuation":
        continuation = get_recorded_locality_continuation(
            ledger, recorded_occurrence_identity
        )
        source_reference = deepcopy(continuation["source_coordinate_reference"])
    else:
        source_reference = _source_reference_from_checkout(
            ledger, recorded_occurrence_identity
        )

    source_locality_identity = _require_recorded_standing_identity(
        source_reference.get("source_locality_identity"),
        "recorded Standing reference carries no exact source Locality",
    )
    through_event_occurrence_identity = source_reference.get(
        "source_through_event_occurrence_identity"
    )
    if through_event_occurrence_identity is not None:
        _require_recorded_standing_identity(
            through_event_occurrence_identity,
            "recorded Standing reference carries no exact Standing boundary",
        )
    standing = read_operator_locality_standing_through(
        ledger,
        locality_identity=source_locality_identity,
        through_event_occurrence_identity=through_event_occurrence_identity,
    )
    return {
        "recorded_occurrence_identity": recorded_occurrence_identity,
        "source_standing_reference": source_reference,
        "standing": standing,
    }


@_operator_standing_replay_validation
def advance_operator_locality_standing(
    ledger: EventLedger,
    event_identities: Iterable[str],
    *,
    locality_identity: str,
    prior: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Advance bounded Locality-local Standing over exact ledger occurrences.

    With no `prior`, this reads the supplied identities from an empty Standing.
    With a `prior`, it begins from the accumulators already established there.
    The ledger verifies each supplied identity's Locality and their append order.
    The caller supplies the bounded identities; this function does not infer an
    omitted occurrence.

    The caller supplies exact identities from the responsible Act that recorded
    them. The ledger resolves those identities rather than accepting supplied
    occurrence copies.

    Every accumulator the live event kinds read is seeded from `prior`, and the
    per-event paths and refusals below are the same ones replay uses. Those
    refusals consult accumulated Standing rather than the ledger, which is why
    seeding preserves them (`#2376`).

    **The advance has as input `prior`.** Its accumulators are taken over rather
    than copied, and the returned Standing shares them. A caller that needs the
    earlier Standing to stay as it was must read it again; there is no
    snapshot here.

    That is not defensive weakness. Standing grows with the
    Locality, so copying it per advance would cost the Locality event count every
    time and reinstate the quadratic this replaced. The console holds one
    Standing, hands it forward, and keeps no earlier one.

    The result is fully recomputable
    from the ledger and is not itself recorded: it returns only standings,
    and Unknown the Locality's events already carry.  An empty
    coordinate is absence of record, not negative standing and not Unknown.
    No Yield is established for relation Candidates here.
    """
    events = ledger.occurrences_in_append_order(
        event_identities,
        locality_identity=locality_identity,
    )
    scope = f"locality:{locality_identity}"
    material_acquisition_result_occurrences: list[dict[str, Any]] = []
    measurement_occurrences: dict[str, dict[str, str]] = {}
    assertion_locality_movement_occurrences: dict[str, dict[str, Any]] = {}
    exact_result_occurrences: dict[str, dict[str, Any]] = {}
    recorded_relation_Standing: dict[str, None] = {}
    recorded_standing_boundary_references: dict[str, None] = {}
    recorded_standing_boundary_locality_relations: dict[str, None] = {}
    operator_invocation_locality_relations: dict[str, None] = {}
    subject_to_act_binding_occurrences: dict[str, None] = {}
    operator_material_source_act_occurrences: dict[str, None] = {}
    material_locality_relation_occurrences: dict[
        str, dict[str, Any]
    ] = {}
    candidate_result_occurrences: dict[str, None] = {}
    admission_result_occurrences: dict[str, None] = {}
    applicability_result_occurrences: dict[str, None] = {}
    comparison_result_occurrences: dict[str, None] = {}
    recorded_pair_comparison_replay_carries: dict[str, dict[str, Any]] = {}
    shared_position_replay_readings: dict[
        str, _SharedPositionReplayReading
    ] = {}
    # Kept sorted and distinct in place rather than as a set sorted on return.
    # A set would have to be rebuilt from the prior list and re-sorted on every
    # advance, which costs the accumulated size each time.  These coordinates
    # do not grow on the five live kinds today, but acquisition would make them
    # grow, and the prior-transfer rule has to hold for every accumulator that
    # can.
    known_loss: list[str] = []
    unknown: list[str] = []
    conflicts: list[str] = []
    through_event_occurrence_identity: str | None = None
    event_count = 0

    if prior is not None:
        # Every accumulator the live event kinds read, taken over from the
        # Standing that already input the earlier occurrences.  Not copied:
        # see the shared-accumulator note above.
        material_acquisition_result_occurrences = prior["material_acquisition_result_occurrences"]
        measurement_occurrences = prior["measurement_occurrences"]
        if type(measurement_occurrences) is not dict:
            raise ValueError(
                "prior Locality Standing requires exact Measurement occurrences"
            )
        assertion_locality_movement_occurrences = prior[
            "assertion_locality_movement_occurrences"
        ]
        if type(assertion_locality_movement_occurrences) is not dict:
            raise ValueError(
                "prior Locality Standing requires exact Assertion Locality movement occurrences"
            )
        exact_result_occurrences = prior["exact_result_occurrences"]
        recorded_relation_Standing = prior["recorded_relation_Standing"]
        if type(recorded_relation_Standing) is not dict:
            raise ValueError(
                "prior Locality Standing requires exact recorded relation occurrences"
            )
        recorded_standing_boundary_references = prior[
            "recorded_standing_boundary_references"
        ]
        if type(recorded_standing_boundary_references) is not dict:
            raise ValueError(
                "prior Locality Standing requires exact recorded Standing boundary references"
            )
        recorded_standing_boundary_locality_relations = prior[
            "recorded_standing_boundary_locality_relations"
        ]
        if type(recorded_standing_boundary_locality_relations) is not dict:
            raise ValueError(
                "prior Locality Standing requires exact recorded Standing boundary Locality relations"
            )
        operator_invocation_locality_relations = prior[
            "operator_invocation_locality_relations"
        ]
        if type(operator_invocation_locality_relations) is not dict:
            raise ValueError(
                "prior Locality Standing requires exact operator invocation Locality relations"
            )
        subject_to_act_binding_occurrences = prior[
            "subject_to_act_binding_occurrences"
        ]
        if type(subject_to_act_binding_occurrences) is not dict:
            raise ValueError(
                "prior Locality Standing requires exact Responsibility assignment occurrences"
            )
        operator_material_source_act_occurrences = prior[
            "operator_material_source_act_occurrences"
        ]
        if type(operator_material_source_act_occurrences) is not dict:
            raise ValueError(
                "prior Locality Standing requires exact operator material source Act occurrences"
            )
        material_locality_relation_occurrences = prior[
            "material_locality_relation_occurrences"
        ]
        if type(material_locality_relation_occurrences) is not dict:
            raise ValueError(
                "prior Locality Standing requires exact material Locality relation occurrences"
            )
        candidate_result_occurrences = prior["candidate_result_occurrences"]
        if type(candidate_result_occurrences) is not dict:
            raise ValueError(
                "prior Locality Standing requires exact Candidate result occurrences"
            )
        admission_result_occurrences = prior["admission_result_occurrences"]
        if type(admission_result_occurrences) is not dict:
            raise ValueError(
                "prior Locality Standing requires exact Admission result occurrences"
            )
        applicability_result_occurrences = prior[
            "applicability_result_occurrences"
        ]
        if type(applicability_result_occurrences) is not dict:
            raise ValueError(
                "prior Locality Standing requires exact Applicability result occurrences"
            )
        comparison_result_occurrences = prior["comparison_result_occurrences"]
        if type(comparison_result_occurrences) is not dict:
            raise ValueError(
                "prior Locality Standing requires exact Compare result occurrences"
            )
        known_loss = prior["known_loss"]
        unknown = prior["unknown"]
        conflicts = prior["conflicts"]
        through_event_occurrence_identity = prior["through_event_occurrence_identity"]
        event_count = prior["event_count"]

    _OPERATOR_STANDING_EXACT_ACCUMULATORS.set(
        (
            ledger,
            locality_identity,
            measurement_occurrences,
            material_acquisition_result_occurrences,
            subject_to_act_binding_occurrences,
        )
    )
    _OPERATOR_STANDING_VALIDATION_CONTEXT.set(
        {
            "ledger": ledger,
            "locality_identity": locality_identity,
            "through_event_occurrence_identity": (
                through_event_occurrence_identity
            ),
            "measurement_occurrences": measurement_occurrences,
            "material_acquisition_result_occurrences": material_acquisition_result_occurrences,
            "subject_to_act_binding_occurrences": (
                subject_to_act_binding_occurrences
            ),
        }
    )

    # Source-position events in this exact advance share the same immutable
    # direct result and frequently refer to the same prior results. Validate
    # each referenced occurrence fully on first encounter, then reuse that
    # validated reading for the remainder of this bounded advance. These
    # readings end with the call, so a later replay still detects mutation.
    source_position_recurrence_validated: dict[tuple[str, str], Any] = {}

    for event in events:
        if event.locality_identity != locality_identity:
            continue
        _set_operator_standing_validation_context(
            ledger,
            locality_identity=locality_identity,
            through_event_occurrence_identity=(
                through_event_occurrence_identity
            ),
            measurement_occurrences=measurement_occurrences,
            material_acquisition_result_occurrences=material_acquisition_result_occurrences,
            subject_to_act_binding_occurrences=(
                subject_to_act_binding_occurrences
            ),
        )
        if not (
            event.kind == WITNESS_MATERIAL_SOURCE_RECORDED_KIND
            or event.kind in _MEASUREMENT_ACT_OCCURRENCE_EVENTS
            or event.kind in _MEASUREMENT_RESPONSIBILITY_ASSIGNMENT_KINDS
            or event.kind in _MEASUREMENT_RECORDED_KINDS
            or event.kind in _ASSERTION_LOCALITY_MOVEMENT_KINDS
            or event.kind in _BYTE_PAIR_MEASUREMENT_LIFECYCLE_KINDS
            or event.kind in _LOCALITY_CONTINUATION_KINDS
            or event.kind in _STANDING_BOUNDARY_REFERENCE_KINDS
            or event.kind in _RECORDED_STANDING_BOUNDARY_LOCALITY_KINDS
            or event.kind in _OPERATOR_MATERIAL_SOURCE_KINDS
            or event.kind in _OPERATOR_INVOCATION_LOCALITY_KINDS
            or event.kind in _RECORDED_PAIR_MEASUREMENT_COMPARISON_KINDS
            or event.kind in _SHARED_POSITION_MEASUREMENT_KINDS
            or event.kind in _ADDRESSED_BYTE_REFERENCE_DETERMINATION_KINDS
            or event.kind in _COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_KINDS
            or event.kind in _ORDERED_PATH_SOURCE_POSITION_MATERIAL_COMPARISON_KINDS
            or event.kind in _SOURCE_POSITION_RECURRENCE_KINDS
        ):
            continue
        if event.kind not in _SUPPORTED_KINDS:
            raise ValueError(f"unsupported operator-acquisition_result event: {event.kind}")
        prior_through_event_occurrence_identity = through_event_occurrence_identity
        pair_lifecycle_event = event.kind in _BYTE_PAIR_MEASUREMENT_LIFECYCLE_KINDS
        if not pair_lifecycle_event:
            event_count += 1
            through_event_occurrence_identity = event.identity
            for key, collected in (
                ("known_loss", known_loss),
                ("unknown", unknown),
                ("conflicts", conflicts),
            ):
                for value in event.material.get(key, ()):
                    _record_distinct(collected, value)
            result_coordinate = _result_subject_to_act_binding_coordinate(ledger, event)
            if result_coordinate is not _NO_RESULT_COORDINATE:
                exact_result_occurrences[event.identity] = result_coordinate
        if event.kind in _MEASUREMENT_ACT_OCCURRENCE_EVENTS:
            continue
        pair_prior_standing = {
            "locality_identity": locality_identity,
            "through_event_occurrence_identity": (
                prior_through_event_occurrence_identity
            ),
            "measurement_occurrences": measurement_occurrences,
            "assertion_locality_movement_occurrences": (
                assertion_locality_movement_occurrences
            ),
            "exact_result_occurrences": exact_result_occurrences,
            "subject_to_act_binding_occurrences": (
                subject_to_act_binding_occurrences
            ),
            "applicability_result_occurrences": (
                applicability_result_occurrences
            ),
        }
        if pair_lifecycle_event:
            if event.kind == BYTE_PAIR_APPLICABILITY_SUBJECT_TO_ACT_BINDING_RECORDED_KIND:
                _read_pair_applicability_subject_to_act_binding(
                    ledger, event.identity, prior_standing=pair_prior_standing
                )
                subject_to_act_binding_occurrences[event.identity] = None
            elif event.kind == BYTE_PAIR_MEASUREMENT_SUBJECT_TO_ACT_BINDING_RECORDED_KIND:
                _read_pair_measurement_subject_to_act_binding(
                    ledger, event.identity, prior_standing=pair_prior_standing
                )
                subject_to_act_binding_occurrences[event.identity] = None
            elif event.kind == BYTE_PAIR_APPLICABILITY_ACT_OCCURRENCE_EVENT:
                _read_pair_applicability_act_occurrence(
                    ledger, event.identity, prior_standing=pair_prior_standing
                )
            elif event.kind == BYTE_PAIR_APPLICABILITY_RECORDED_KIND:
                _read_recorded_pair_input_applicability(
                    ledger, event.identity, prior_standing=pair_prior_standing
                )
                applicability_result_occurrences[event.identity] = None
            elif event.kind == BYTE_PAIR_RESPONSIBLE_ACT_OCCURRENCE_EVENT:
                _read_pair_measurement_act_occurrence(
                    ledger, event.identity, prior_standing=pair_prior_standing
                )
            else:
                _findings_of_recorded_byte_position_pair_measurement(
                    ledger, event.identity, prior_standing=pair_prior_standing
                )
                measurement_occurrences[event.identity] = (
                    _measurement_occurrence_coordinates(event)
                )
            event_count += 1
            through_event_occurrence_identity = event.identity
            for key, collected in (
                ("known_loss", known_loss),
                ("unknown", unknown),
                ("conflicts", conflicts),
            ):
                for value in event.material.get(key, ()):
                    _record_distinct(collected, value)
            result_coordinate = _result_subject_to_act_binding_coordinate(ledger, event)
            if result_coordinate is not _NO_RESULT_COORDINATE:
                exact_result_occurrences[event.identity] = result_coordinate
            continue
        if event.kind == BYTE_MEASUREMENT_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND:
            _read_byte_measurement_responsibility_assignment(
                ledger,
                event.identity,
                prior_standing={
                    "locality_identity": locality_identity,
                    "through_event_occurrence_identity": (
                        prior_through_event_occurrence_identity
                    ),
                    "subject_to_act_binding_occurrences": (
                        subject_to_act_binding_occurrences
                    ),
                },
            )
            subject_to_act_binding_occurrences[event.identity] = None
            continue
        if (
            event.kind
            == ASSERTION_LOCALITY_MOVEMENT_SUBJECT_TO_ACT_BINDING_KIND
        ):
            _read_assertion_locality_movement_subject_to_act_binding(
                ledger,
                event.identity,
                prior_destination_standing={
                    "locality_identity": locality_identity,
                    "through_event_occurrence_identity": (
                        prior_through_event_occurrence_identity
                    ),
                },
            )
            subject_to_act_binding_occurrences[event.identity] = None
            continue
        if event.kind == ASSERTION_LOCALITY_MOVEMENT_ACT_OCCURRENCE_EVENT:
            _read_assertion_locality_movement_act_occurrence(
                ledger,
                event.identity,
                prior_destination_standing={
                    "locality_identity": locality_identity,
                    "through_event_occurrence_identity": (
                        prior_through_event_occurrence_identity
                    ),
                    "subject_to_act_binding_occurrences": (
                        subject_to_act_binding_occurrences
                    ),
                },
            )
            continue
        if event.kind == ASSERTION_LOCALITY_MOVEMENT_KIND:
            _validate_moved_byte_assertion(
                ledger,
                event.identity,
                prior_destination_standing={
                    "locality_identity": locality_identity,
                    "through_event_occurrence_identity": (
                        prior_through_event_occurrence_identity
                    ),
                    "subject_to_act_binding_occurrences": (
                        subject_to_act_binding_occurrences
                    ),
                },
            )
            assertion_locality_movement_occurrences[event.identity] = (
                _assertion_locality_movement_occurrence_coordinates(ledger, event)
            )
            continue
        if (
            event.kind
            == OCCURRENCE_POSITION_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND
        ):
            get_occurrence_position_measurement_responsibility_assignment(
                ledger, event.identity
            )
            subject_to_act_binding_occurrences[event.identity] = None
            continue
        if event.kind == BYTE_PAIR_OCCURRENCE_POSITION_ASSIGNMENT_KIND:
            get_byte_pair_occurrence_position_measurement_responsibility_assignment(
                ledger, event.identity
            )
            subject_to_act_binding_occurrences[event.identity] = None
            continue
        if (
            event.kind
            == RECORDED_RESPONSIBILITY_ASSIGNMENT_OF_MEASUREMENT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_KIND
        ):
            _read_responsibility_assignment_for_measurement_of_recurrent_byte_pair_occurrence_position(
                ledger,
                event.identity,
                prior_standing={
                    "locality_identity": locality_identity,
                    "through_event_occurrence_identity": (
                        prior_through_event_occurrence_identity
                    ),
                    "measurement_occurrences": measurement_occurrences,
                    "material_acquisition_result_occurrences": material_acquisition_result_occurrences,
                },
            )
            subject_to_act_binding_occurrences[event.identity] = None
            continue
        if (
            event.kind
            == STANDING_BOUNDARY_REFERENCE_SUBJECT_TO_ACT_BINDING_RECORDED_KIND
        ):
            get_standing_boundary_reference_subject_to_act_binding(
                ledger, event.identity
            )
            subject_to_act_binding_occurrences[event.identity] = None
            continue
        if event.kind == STANDING_BOUNDARY_REFERENCE_ACT_OCCURRENCE_EVENT:
            get_standing_boundary_reference_act_occurrence(ledger, event.identity)
            continue
        if event.kind == STANDING_BOUNDARY_REFERENCE_RECORDED_KIND:
            get_recorded_standing_boundary_reference(ledger, event.identity)
            recorded_standing_boundary_references[event.identity] = None
            continue
        if (
            event.kind
            == RECORDED_STANDING_BOUNDARY_LOCALITY_SUBJECT_TO_ACT_BINDING_RECORDED_KIND
        ):
            get_recorded_standing_boundary_locality_subject_to_act_binding(
                ledger, event.identity
            )
            subject_to_act_binding_occurrences[event.identity] = None
            continue
        if event.kind == RECORDED_STANDING_BOUNDARY_LOCALITY_ACT_OCCURRENCE_EVENT:
            get_recorded_standing_boundary_locality_act_occurrence(
                ledger, event.identity
            )
            continue
        if event.kind == RECORDED_STANDING_BOUNDARY_LOCALITY_RECORDED_KIND:
            get_recorded_standing_boundary_locality(ledger, event.identity)
            recorded_standing_boundary_locality_relations[event.identity] = None
            continue
        if (
            event.kind
            == OPERATOR_MATERIAL_SOURCE_SUBJECT_TO_ACT_BINDING_RECORDED_KIND
        ):
            get_operator_material_source_subject_to_act_binding(
                ledger, event.identity
            )
            subject_to_act_binding_occurrences[event.identity] = None
            continue
        if event.kind == OPERATOR_MATERIAL_SOURCE_ACT_OCCURRENCE_EVENT:
            get_operator_material_source_act_occurrence(ledger, event.identity)
            operator_material_source_act_occurrences[event.identity] = None
            continue
        if event.kind == OPERATOR_MATERIAL_SOURCE_RECORDED_KIND:
            material = get_recorded_operator_material_source(
                ledger, event.identity
            )
            material_locality_relation_occurrences[event.identity] = {
                "locality_relation": deepcopy(material["locality_relation"]),
            }
        if (
            event.kind
            == OPERATOR_INVOCATION_LOCALITY_SUBJECT_TO_ACT_BINDING_RECORDED_KIND
        ):
            get_operator_invocation_locality_subject_to_act_binding(
                ledger, event.identity
            )
            subject_to_act_binding_occurrences[event.identity] = None
            continue
        if event.kind == OPERATOR_INVOCATION_LOCALITY_ACT_OCCURRENCE_EVENT:
            get_operator_invocation_locality_act_occurrence(ledger, event.identity)
            continue
        if event.kind == OPERATOR_INVOCATION_LOCALITY_RECORDED_KIND:
            get_recorded_operator_invocation_locality(ledger, event.identity)
            operator_invocation_locality_relations[event.identity] = None
            continue
        addressed_byte_reference_prior_standing = {
            "locality_identity": locality_identity,
            "through_event_occurrence_identity": (
                prior_through_event_occurrence_identity
            ),
            "measurement_occurrences": measurement_occurrences,
            "material_acquisition_result_occurrences": material_acquisition_result_occurrences,
            "subject_to_act_binding_occurrences": (
                subject_to_act_binding_occurrences
            ),
            "applicability_result_occurrences": (
                applicability_result_occurrences
            ),
        }
        if event.kind == ADDRESSED_BYTE_REFERENCE_RESPONSIBILITY_ASSIGNMENT_KIND:
            _read_addressed_byte_reference_assignment(
                ledger,
                event.identity,
                prior_standing=addressed_byte_reference_prior_standing,
            )
            subject_to_act_binding_occurrences[event.identity] = None
            continue
        if event.kind == ADDRESSED_BYTE_REFERENCE_APPLICABILITY_ACT_OCCURRENCE_EVENT:
            _read_addressed_byte_reference_applicability_act(
                ledger,
                event.identity,
                prior_standing=addressed_byte_reference_prior_standing,
            )
            continue
        if event.kind == ADDRESSED_BYTE_REFERENCE_APPLICABILITY_RESULT_KIND:
            _read_addressed_byte_reference_applicability_result(
                ledger,
                event.identity,
                prior_standing=addressed_byte_reference_prior_standing,
            )
            applicability_result_occurrences[event.identity] = None
            continue
        if event.kind == ADDRESSED_BYTE_REFERENCE_DETERMINATION_ACT_OCCURRENCE_EVENT:
            _read_addressed_byte_reference_determination_act(
                ledger,
                event.identity,
                prior_standing=addressed_byte_reference_prior_standing,
            )
            continue
        if event.kind == SHARED_POSITION_RESPONSIBILITY_ASSIGNMENT_KIND:
            assignment_reading = _shared_position_assignment_reading(
                ledger,
                event,
                prior_standing=addressed_byte_reference_prior_standing,
            )
            shared_position_replay_readings[event.identity] = (
                _shared_position_replay_reading(
                    ledger, assignment_reading
                )
            )
            subject_to_act_binding_occurrences[event.identity] = None
            continue
        if event.kind == SHARED_POSITION_APPLICABILITY_ACT_OCCURRENCE_EVENT:
            assignment_identity = _shared_position_assignment_identity(event)
            replay_reading = shared_position_replay_readings.get(
                assignment_identity
            )
            try:
                if replay_reading is not None:
                    _advance_shared_position_replay_reading(
                        ledger, replay_reading, event
                    )
                else:
                    assignment_reading = _shared_position_assignment_reading(
                        ledger,
                        event,
                        prior_standing=addressed_byte_reference_prior_standing,
                    )
                    _read_shared_position_applicability_act(
                        ledger,
                        event.identity,
                        assignment_reading=assignment_reading,
                    )
            except Exception:
                if assignment_identity is not None:
                    shared_position_replay_readings.pop(
                        assignment_identity, None
                    )
                raise
            continue
        if event.kind == SHARED_POSITION_APPLICABILITY_RESULT_KIND:
            assignment_identity = _shared_position_assignment_identity(event)
            replay_reading = shared_position_replay_readings.get(
                assignment_identity
            )
            try:
                if replay_reading is not None:
                    _advance_shared_position_replay_reading(
                        ledger, replay_reading, event
                    )
                else:
                    assignment_reading = _shared_position_assignment_reading(
                        ledger,
                        event,
                        prior_standing=addressed_byte_reference_prior_standing,
                    )
                    _read_shared_position_applicability_result(
                        ledger,
                        event.identity,
                        assignment_reading=assignment_reading,
                    )
            except Exception:
                if assignment_identity is not None:
                    shared_position_replay_readings.pop(
                        assignment_identity, None
                    )
                raise
            applicability_result_occurrences[event.identity] = None
            continue
        if event.kind == SHARED_POSITION_MEASUREMENT_ACT_OCCURRENCE_EVENT:
            assignment_identity = _shared_position_assignment_identity(event)
            replay_reading = shared_position_replay_readings.get(
                assignment_identity
            )
            try:
                if replay_reading is not None:
                    _advance_shared_position_replay_reading(
                        ledger, replay_reading, event
                    )
                else:
                    assignment_reading = _shared_position_assignment_reading(
                        ledger,
                        event,
                        prior_standing=addressed_byte_reference_prior_standing,
                    )
                    _read_shared_position_measurement_act(
                        ledger,
                        event.identity,
                        assignment_reading=assignment_reading,
                    )
            except Exception:
                if assignment_identity is not None:
                    shared_position_replay_readings.pop(
                        assignment_identity, None
                    )
                raise
            continue
        if (
            event.kind
            == RECORDED_PAIR_MEASUREMENT_COMPARISON_RESPONSIBILITY_ASSIGNMENT_KIND
        ):
            assignment_reading = _recorded_pair_comparison_assignment_reading(
                ledger, event.identity
            )
            recorded_pair_comparison_replay_carries[event.identity] = (
                _recorded_pair_comparison_replay_carry(
                    ledger, assignment_reading
                )
            )
            subject_to_act_binding_occurrences[event.identity] = None
            continue
        if (
            event.kind
            == RECORDED_PAIR_MEASUREMENT_COMPARISON_APPLICABILITY_ACT_OCCURRENCE_EVENT
        ):
            assignment_identity = _recorded_pair_comparison_assignment_identity(
                event
            )
            carry = recorded_pair_comparison_replay_carries.get(
                assignment_identity
            )
            try:
                _act, assignment_reading = (
                    _recorded_pair_comparison_applicability_act_reading(
                        ledger,
                        event.identity,
                        assignment_reading=(
                            _validate_recorded_pair_comparison_replay_carry(
                                ledger, carry
                            )
                            if carry is not None
                            else None
                        ),
                    )
                )
                if carry is None:
                    carry = _recorded_pair_comparison_replay_carry(
                        ledger, assignment_reading
                    )
                else:
                    _validate_recorded_pair_comparison_replay_carry(
                        ledger, carry
                    )
                recorded_pair_comparison_replay_carries[
                    assignment_reading[0].identity
                ] = carry
            except Exception:
                if assignment_identity is not None:
                    recorded_pair_comparison_replay_carries.pop(
                        assignment_identity, None
                    )
                raise
            continue
        if (
            event.kind
            == RECORDED_PAIR_MEASUREMENT_COMPARISON_APPLICABILITY_RESULT_KIND
        ):
            assignment_identity = _recorded_pair_comparison_assignment_identity(
                event
            )
            carry = recorded_pair_comparison_replay_carries.get(
                assignment_identity
            )
            try:
                _material, _applicability, _act, assignment_reading = (
                    _recorded_pair_comparison_applicability_reading(
                        ledger,
                        event.identity,
                        assignment_reading=(
                            _validate_recorded_pair_comparison_replay_carry(
                                ledger, carry
                            )
                            if carry is not None
                            else None
                        ),
                    )
                )
                if carry is None:
                    carry = _recorded_pair_comparison_replay_carry(
                        ledger, assignment_reading
                    )
                else:
                    _validate_recorded_pair_comparison_replay_carry(
                        ledger, carry
                    )
                recorded_pair_comparison_replay_carries[
                    assignment_reading[0].identity
                ] = carry
            except Exception:
                if assignment_identity is not None:
                    recorded_pair_comparison_replay_carries.pop(
                        assignment_identity, None
                    )
                raise
            applicability_result_occurrences[event.identity] = None
            continue
        if event.kind == RECORDED_PAIR_MEASUREMENT_COMPARISON_ACT_OCCURRENCE_EVENT:
            assignment_identity = _recorded_pair_comparison_assignment_identity(
                event
            )
            carry = recorded_pair_comparison_replay_carries.get(
                assignment_identity
            )
            try:
                _act, assignment_reading, _applicability = (
                    _recorded_pair_comparison_act_reading(
                        ledger,
                        event.identity,
                        assignment_reading=(
                            _validate_recorded_pair_comparison_replay_carry(
                                ledger, carry
                            )
                            if carry is not None
                            else None
                        ),
                    )
                )
                if carry is None:
                    carry = _recorded_pair_comparison_replay_carry(
                        ledger, assignment_reading
                    )
                else:
                    _validate_recorded_pair_comparison_replay_carry(
                        ledger, carry
                    )
                recorded_pair_comparison_replay_carries[
                    assignment_reading[0].identity
                ] = carry
            except Exception:
                if assignment_identity is not None:
                    recorded_pair_comparison_replay_carries.pop(
                        assignment_identity, None
                    )
                raise
            continue
        if event.kind == RECORDED_PAIR_MEASUREMENT_COMPARISON_RESULT_KIND:
            assignment_identity = _recorded_pair_comparison_assignment_identity(
                event
            )
            carry = recorded_pair_comparison_replay_carries.get(
                assignment_identity
            )
            try:
                _material, _assignment_reading = (
                    _recorded_pair_measurement_comparison_reading(
                        ledger,
                        event.identity,
                        assignment_reading=(
                            _validate_recorded_pair_comparison_replay_carry(
                                ledger, carry
                            )
                            if carry is not None
                            else None
                        ),
                    )
                )
                if carry is not None:
                    _validate_recorded_pair_comparison_replay_carry(
                        ledger, carry
                    )
            except Exception:
                if assignment_identity is not None:
                    recorded_pair_comparison_replay_carries.pop(
                        assignment_identity, None
                    )
                raise
            if assignment_identity is not None:
                recorded_pair_comparison_replay_carries.pop(
                    assignment_identity, None
                )
            comparison_result_occurrences[event.identity] = None
            continue
        if event.kind == COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_RESPONSIBILITY_ASSIGNMENT_KIND:
            get_comparison_of_ordered_relation_path_with_recorded_pair_findings_responsibility_assignment(
                ledger, event.identity
            )
            subject_to_act_binding_occurrences[event.identity] = None
            continue
        if event.kind == COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_APPLICABILITY_ACT_OCCURRENCE_EVENT:
            get_comparison_of_ordered_relation_path_with_recorded_pair_findings_applicability_act_occurrence(
                ledger, event.identity
            )
            continue
        if event.kind == COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_APPLICABILITY_RESULT_KIND:
            get_recorded_comparison_of_ordered_relation_path_with_recorded_pair_findings_applicability(
                ledger, event.identity
            )
            applicability_result_occurrences[event.identity] = None
            continue
        if event.kind == COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_COMPARE_ACT_OCCURRENCE_EVENT:
            get_comparison_of_ordered_relation_path_with_recorded_pair_findings_act_occurrence(
                ledger, event.identity
            )
            continue
        if event.kind == COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_RESULT_KIND:
            get_recorded_comparison_of_ordered_relation_path_with_recorded_pair_findings(
                ledger, event.identity
            )
            comparison_result_occurrences[event.identity] = None
            continue
        if event.kind in _ORDERED_PATH_SOURCE_POSITION_MATERIAL_COMPARISON_KINDS:
            validate_ordered_path_source_position_material_comparison_event(
                ledger, event.identity
            )
            if (
                event.kind
                == ORDERED_PATH_SOURCE_POSITION_COMPARE_APPLICABILITY_RESULT_KIND
            ):
                applicability_result_occurrences[event.identity] = None
            elif event.kind == ORDERED_PATH_SOURCE_POSITION_COMPARE_RESULT_KIND:
                comparison_result_occurrences[event.identity] = None
            continue
        if event.kind in _SOURCE_POSITION_RECURRENCE_KINDS:
            validate_source_position_recurrence_event(
                ledger,
                event.identity,
                _validated=source_position_recurrence_validated,
            )
            if event.kind in {
                COMPARE_APPLICABILITY_RESPONSIBILITY_KIND,
                COMPARE_RESPONSIBILITY_KIND,
                SOURCE_POSITION_MEASUREMENT_RESPONSIBILITY_KIND,
                RECURRENCE_MEASUREMENT_RESPONSIBILITY_KIND,
                COORDINATE_MEASUREMENT_RESPONSIBILITY_KIND,
                RECURRENT_RESULT_MATERIAL_MEASUREMENT_RESPONSIBILITY_KIND,
            }:
                subject_to_act_binding_occurrences[event.identity] = None
            elif event.kind == SOURCE_POSITION_RECURRENCE_COMPARE_APPLICABILITY_RESULT_KIND:
                applicability_result_occurrences[event.identity] = None
            elif event.kind == SOURCE_POSITION_RECURRENCE_COMPARE_RESULT_KIND:
                comparison_result_occurrences[event.identity] = None
            elif event.kind in {
                SOURCE_POSITION_MEASUREMENT_RESULT_KIND,
                SOURCE_POSITION_RECURRENCE_MEASUREMENT_RESULT_KIND,
                CORRESPONDING_COORDINATE_MEASUREMENT_RESULT_KIND,
                RECURRENT_RESULT_MATERIAL_MEASUREMENT_RESULT_KIND,
            }:
                measurement_occurrences[event.identity] = {
                    "recorded_occurrence_identity": event.identity,
                    "result_identity": event.material["result_identity"],
                    "act_occurrence_identity": event.material[
                        "act_occurrence_identity"
                    ],
                    "act_occurrence_event_identity": event.material[
                        "act_occurrence_event_identity"
                    ],
                    "yield_relation_identity": event.material[
                        "yield_relation_identity"
                    ],
                }
            continue
        if (
            event.kind
            == LOCALITY_CONTINUATION_SUBJECT_TO_ACT_BINDING_RECORDED_KIND
        ):
            get_locality_continuation_subject_to_act_binding(
                ledger, event.identity
            )
            subject_to_act_binding_occurrences[event.identity] = None
            continue
        if event.kind == LOCALITY_CONTINUATION_ACT_OCCURRENCE_EVENT:
            continue
        if event.kind == LOCALITY_CONTINUATION_RECORDED_KIND:
            get_recorded_locality_continuation(ledger, event.identity)
            recorded_relation_Standing[event.identity] = None
            continue
        if event.kind == BYTE_MEASUREMENT_RECORDED_KIND:
            assertions_of_recorded_byte_measurement(ledger, event.identity)
            measurement_occurrences[event.identity] = (
                _measurement_occurrence_coordinates(event)
            )
            continue
        if event.kind == OCCURRENCE_POSITION_RECORDED_KIND:
            get_recorded_occurrence_position_measurement(ledger, event.identity)
            measurement_occurrences[event.identity] = (
                _measurement_occurrence_coordinates(event)
            )
            continue
        if event.kind == RECORDING_OCCURRENCE_OF_RESULT_OF_MEASUREMENT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_KIND:
            _read_recorded_result_of_measurement_of_recurrent_byte_pair_occurrence_position(
                ledger,
                event.identity,
                prior_standing={
                    "locality_identity": locality_identity,
                    "through_event_occurrence_identity": (
                        prior_through_event_occurrence_identity
                    ),
                    "measurement_occurrences": measurement_occurrences,
                    "material_acquisition_result_occurrences": material_acquisition_result_occurrences,
                    "subject_to_act_binding_occurrences": (
                        subject_to_act_binding_occurrences
                    ),
                },
            )
            measurement_occurrences[event.identity] = (
                _measurement_occurrence_coordinates(event)
            )
            continue
        if event.kind == SHARED_POSITION_MEASUREMENT_RESULT_KIND:
            assignment_identity = _shared_position_assignment_identity(event)
            replay_reading = shared_position_replay_readings.get(
                assignment_identity
            )
            try:
                if replay_reading is not None:
                    _advance_shared_position_replay_reading(
                        ledger, replay_reading, event
                    )
                else:
                    assignment_reading = _shared_position_assignment_reading(
                        ledger,
                        event,
                        prior_standing=addressed_byte_reference_prior_standing,
                    )
                    _read_shared_position_measurement_result(
                        ledger,
                        event.identity,
                        assignment_reading=assignment_reading,
                    )
            except Exception:
                if assignment_identity is not None:
                    shared_position_replay_readings.pop(
                        assignment_identity, None
                    )
                raise
            if assignment_identity is not None:
                shared_position_replay_readings.pop(
                    assignment_identity, None
                )
            measurement_occurrences[event.identity] = (
                _measurement_occurrence_coordinates(event)
            )
            continue
        if event.kind == BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND:
            get_recorded_byte_pair_occurrence_position_measurement(ledger, event.identity)
            measurement_occurrences[event.identity] = (
                _measurement_occurrence_coordinates(event)
            )
            continue
        if event.kind == ADDRESSED_BYTE_REFERENCE_DETERMINATION_RESULT_KIND:
            _read_addressed_byte_reference_determination_result(
                ledger,
                event.identity,
                prior_standing={
                    "locality_identity": locality_identity,
                    "through_event_occurrence_identity": (
                        prior_through_event_occurrence_identity
                    ),
                    "measurement_occurrences": measurement_occurrences,
                    "subject_to_act_binding_occurrences": (
                        subject_to_act_binding_occurrences
                    ),
                    "applicability_result_occurrences": (
                        applicability_result_occurrences
                    ),
                },
            )
            measurement_occurrences[event.identity] = (
                _addressed_byte_reference_determination_coordinates(event)
            )
            continue
        source_result = read_exact_material_result(
            ledger, event.identity
        )
        locality_requirements = (
            read_material_locality_relation_requirements(
                ledger,
                recorded_result_event_identity=source_result.identity,
            )
        )
        if not all(locality_requirements.values()):
            raise ValueError(
                "material acquisition carries no exact material Locality relation"
            )
        material_locality_relation_occurrences[source_result.identity] = {
            "locality_relation": deepcopy(
                source_result.material["locality_relation"]
            ),
        }
        material_acquisition_reference = source_result.material["dimensions"][
            "identity"
        ]
        occurrence = {
            "subject_reference": material_acquisition_reference,
            "result_occurrence_identity": source_result.identity,
            "source_role": source_result.material["source_role"],
        }
        material_acquisition_result_occurrences.append(occurrence)

    return {
        "locality_identity": locality_identity,
        "through_event_occurrence_identity": through_event_occurrence_identity,
        "event_count": event_count,
        "material_acquisition_result_occurrences": material_acquisition_result_occurrences,
        "measurement_occurrences": measurement_occurrences,
        "assertion_locality_movement_occurrences": (
            assertion_locality_movement_occurrences
        ),
        "exact_result_occurrences": exact_result_occurrences,
        # Exactly the relation standings recorded by Locality events;
        # emptiness is absence of record only.
        "recorded_relation_Standing": recorded_relation_Standing,
        "recorded_standing_boundary_references": (
            recorded_standing_boundary_references
        ),
        "recorded_standing_boundary_locality_relations": (
            recorded_standing_boundary_locality_relations
        ),
        "operator_invocation_locality_relations": (
            operator_invocation_locality_relations
        ),
        "subject_to_act_binding_occurrences": (
            subject_to_act_binding_occurrences
        ),
        "operator_material_source_act_occurrences": (
            operator_material_source_act_occurrences
        ),
        "material_locality_relation_occurrences": (
            material_locality_relation_occurrences
        ),
        "candidate_result_occurrences": candidate_result_occurrences,
        "admission_result_occurrences": admission_result_occurrences,
        "applicability_result_occurrences": applicability_result_occurrences,
        "comparison_result_occurrences": comparison_result_occurrences,
        "known_loss": known_loss,
        "unknown": unknown,
        "conflicts": conflicts,
    }


def _carry_byte_measurement_assignment_into_standing(
    ledger: EventLedger,
    locality_standing: dict[str, Any],
    event,
    *,
    prior_through_event_occurrence_identity: str,
    responsibility_boundary_replay: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Carry the exact-byte assignment produced beside this Standing."""

    if (
        type(locality_standing) is not dict
        or locality_standing.get("locality_identity") != event.locality_identity
        or locality_standing.get("through_event_occurrence_identity")
        != prior_through_event_occurrence_identity
        or event.identity == prior_through_event_occurrence_identity
        or ledger.get(event.identity) != event
        or ledger.append_boundary_through_occurrence(event.identity)
        != ledger.append_boundary()
    ):
        raise ValueError("byte Measurement assignment must follow carried Standing")
    _read_byte_measurement_responsibility_assignment(
        ledger,
        event.identity,
        prior_standing=(
            locality_standing
            if responsibility_boundary_replay is None
            else responsibility_boundary_replay
        ),
    )
    assignments = locality_standing.get("subject_to_act_binding_occurrences")
    event_count = locality_standing.get("event_count")
    if (
        type(assignments) is not dict
        or event.identity in assignments
        or type(event_count) is not int
        or event_count < 0
    ):
        raise ValueError("byte Measurement assignment Standing is not exact")
    standing_additions = _exact_standing_additions(
        locality_standing,
        event,
        error_message="byte Measurement assignment Standing is not exact",
    )
    assignments[event.identity] = None
    for key, added in standing_additions.items():
        for value in added:
            _record_distinct(locality_standing[key], value)
    locality_standing["through_event_occurrence_identity"] = event.identity
    locality_standing["event_count"] = event_count + 1
    return locality_standing


def _carry_assertion_locality_movement_assignment_into_standing(
    ledger: EventLedger,
    locality_standing: dict[str, Any],
    event,
    *,
    source: _AssertionLocalityMovementSource,
    source_event,
    source_standing: dict[str, Any],
) -> dict[str, Any]:
    """Carry one movement assignment produced from exact same-call inputs."""

    assignments = (
        locality_standing.get("subject_to_act_binding_occurrences")
        if type(locality_standing) is dict
        else None
    )
    event_count = (
        locality_standing.get("event_count")
        if type(locality_standing) is dict
        else None
    )
    source_boundary = (
        source_standing.get("through_event_occurrence_identity")
        if type(source_standing) is dict
        else None
    )
    identities = {
        coordinate: event.material.get(coordinate)
        for coordinate in (
            "movement_act_identity",
            "movement_act_occurrence_identity",
            "movement_result_identity",
        )
    }
    expected = None
    current_source = None
    current_source_event = None
    try:
        current_source, current_source_event = _source_assertion_from_reference(
            ledger, _source_assertion_reference(source)
        )
    except (TypeError, ValueError):
        pass
    if (
        source_event is not None
        and type(source_boundary) is str
        and source_boundary
        and all(
            type(identity) is str and identity for identity in identities.values()
        )
        and len(set(identities.values())) == len(identities)
    ):
        expected = _movement_assignment_material(
            source=source,
            source_event=source_event,
            source_locality=source_event.locality_identity,
            destination_locality=event.locality_identity,
            source_through_event_occurrence_identity=source_boundary,
            destination_through_event_occurrence_identity=(
                locality_standing.get("through_event_occurrence_identity")
                if type(locality_standing) is dict
                else None
            ),
            **identities,
        )
    if (
        type(locality_standing) is not dict
        or event.kind
        != ASSERTION_LOCALITY_MOVEMENT_SUBJECT_TO_ACT_BINDING_KIND
        or ledger.get(event.identity) != event
        or ledger.integrity_of(event.identity) == CORRUPTED
        or source_event is None
        or current_source != source
        or current_source_event != source_event
        or type(source_standing) is not dict
        or ledger.get(source_event.identity) != source_event
        or ledger.integrity_of(source_event.identity) == CORRUPTED
        or _source_assertion_reference(source).get("recorded_occurrence_identity")
        != source_event.identity
        or source_event.locality_identity != event.material.get("source_locality")
        or source_standing.get("locality_identity")
        != source_event.locality_identity
        or not _source_assertion_is_carried(source_event, source_standing)
        or event.locality_identity
        != locality_standing.get("locality_identity")
        or event.material != expected
        or type(assignments) is not dict
        or event.identity in assignments
        or type(event_count) is not int
        or event_count < 0
        or ledger.append_boundary_through_occurrence(event.identity)
        != ledger.append_boundary()
    ):
        raise ValueError("Assertion movement assignment Standing is not exact")
    standing_additions = _exact_standing_additions(
        locality_standing,
        event,
        error_message="Assertion movement assignment Standing is not exact",
    )
    assignments[event.identity] = None
    for key, added in standing_additions.items():
        for value in added:
            _record_distinct(locality_standing[key], value)
    locality_standing["through_event_occurrence_identity"] = event.identity
    locality_standing["event_count"] = event_count + 1
    return locality_standing


def _carry_assertion_locality_movement_act_into_standing(
    ledger: EventLedger,
    locality_standing: dict[str, Any],
    event,
    *,
    responsibility_assignment,
) -> dict[str, Any]:
    """Carry the exact movement Act produced beside its assignment Standing."""

    assignments = (
        locality_standing.get("subject_to_act_binding_occurrences")
        if type(locality_standing) is dict
        else None
    )
    event_count = (
        locality_standing.get("event_count")
        if type(locality_standing) is dict
        else None
    )
    try:
        _require_exact_movement_assignment_and_source(
            ledger, responsibility_assignment
        )
        expected = _movement_act_material(responsibility_assignment)
        ledger.occurrences_in_append_order(
            (responsibility_assignment.identity, event.identity),
            locality_identity=event.locality_identity,
        )
    except (AttributeError, TypeError, ValueError) as error:
        raise ValueError("Assertion movement Act Standing is not exact") from error
    if (
        type(locality_standing) is not dict
        or responsibility_assignment.kind
        != ASSERTION_LOCALITY_MOVEMENT_SUBJECT_TO_ACT_BINDING_KIND
        or ledger.get(responsibility_assignment.identity)
        != responsibility_assignment
        or ledger.integrity_of(responsibility_assignment.identity) == CORRUPTED
        or event.kind != ASSERTION_LOCALITY_MOVEMENT_ACT_OCCURRENCE_EVENT
        or ledger.get(event.identity) != event
        or ledger.integrity_of(event.identity) == CORRUPTED
        or event.locality_identity != responsibility_assignment.locality_identity
        or event.material != expected
        or locality_standing.get("locality_identity") != event.locality_identity
        or locality_standing.get("through_event_occurrence_identity")
        != responsibility_assignment.identity
        or type(assignments) is not dict
        or assignments.get(responsibility_assignment.identity, object()) is not None
        or type(event_count) is not int
        or event_count < 0
        or ledger.append_boundary_through_occurrence(event.identity)
        != ledger.append_boundary()
    ):
        raise ValueError("Assertion movement Act Standing is not exact")
    standing_additions = _exact_standing_additions(
        locality_standing,
        event,
        error_message="Assertion movement Act Standing is not exact",
    )
    for key, added in standing_additions.items():
        for value in added:
            _record_distinct(locality_standing[key], value)
    locality_standing["through_event_occurrence_identity"] = event.identity
    locality_standing["event_count"] = event_count + 1
    return locality_standing


def _carry_assertion_locality_movement_result_into_standing(
    ledger: EventLedger,
    locality_standing: dict[str, Any],
    event,
    *,
    act_occurrence,
    responsibility_assignment,
    source: _AssertionLocalityMovementSource,
) -> tuple[
    dict[str, Any],
    RecordedByteAssertion | RecordedAssertionCarriedByLocalityMovement,
]:
    """Carry one exact movement result and its already-carried source."""

    assignments = (
        locality_standing.get("subject_to_act_binding_occurrences")
        if type(locality_standing) is dict
        else None
    )
    movements = (
        locality_standing.get("assertion_locality_movement_occurrences")
        if type(locality_standing) is dict
        else None
    )
    event_count = (
        locality_standing.get("event_count")
        if type(locality_standing) is dict
        else None
    )
    yield_relation_identity = event.material.get("yield_relation_identity")
    yield_relation = ledger.get(yield_relation_identity) if type(yield_relation_identity) is str else None
    try:
        current_source, current_source_event = _source_assertion_from_reference(
            ledger, _source_assertion_reference(source)
        )
        expected_act = _movement_act_material(responsibility_assignment)
        expected = {
            **_movement_result_material(responsibility_assignment),
            "act_occurrence_event_identity": act_occurrence.identity,
            "yield_relation_identity": yield_relation_identity,
        }
        requirements = read_requirements_of_yield_relation(
            ledger,
            recorded_result_event_identity=event.identity,
            yield_relation_event_identity=yield_relation_identity,
            act_occurrence_event_identity=act_occurrence.identity,
            recorded_result_occurrence_coordinate="movement_act_occurrence_identity",
            responsible_act_occurrence_coordinate="movement_act_occurrence_identity",
        )
        ledger.occurrences_in_append_order(
            (
                act_occurrence.identity,
                yield_relation_identity,
                event.identity,
            ),
            locality_identity=event.locality_identity,
        )
    except (AttributeError, KeyError, TypeError, ValueError) as error:
        raise ValueError("Assertion movement result Standing is not exact") from error
    if (
        type(locality_standing) is not dict
        or responsibility_assignment.kind
        != ASSERTION_LOCALITY_MOVEMENT_SUBJECT_TO_ACT_BINDING_KIND
        or ledger.get(responsibility_assignment.identity)
        != responsibility_assignment
        or ledger.integrity_of(responsibility_assignment.identity) == CORRUPTED
        or current_source != source
        or current_source_event is None
        or ledger.integrity_of(current_source_event.identity) == CORRUPTED
        or act_occurrence.kind
        != ASSERTION_LOCALITY_MOVEMENT_ACT_OCCURRENCE_EVENT
        or ledger.get(act_occurrence.identity) != act_occurrence
        or ledger.integrity_of(act_occurrence.identity) == CORRUPTED
        or act_occurrence.material != expected_act
        or event.kind != ASSERTION_LOCALITY_MOVEMENT_KIND
        or ledger.get(event.identity) != event
        or ledger.integrity_of(event.identity) == CORRUPTED
        or event.locality_identity != responsibility_assignment.locality_identity
        or event.material != expected
        or responsibility_assignment.material.get("source_assertion_reference")
        != _source_assertion_reference(source)
        or event.material.get("source_assertion_reference")
        != _source_assertion_reference(source)
        or yield_relation is None
        or yield_relation.kind != RECORDED_YIELD_RELATION_EVENT
        or yield_relation.locality_identity != event.locality_identity
        or ledger.integrity_of(yield_relation.identity) == CORRUPTED
        or yield_relation.material.get("result_kind")
        != ASSERTION_LOCALITY_MOVEMENT_RESULT_KIND
        or yield_relation.material.get("occurrence_boundary")
        != "assertion_locality_movement"
        or not all(requirements.values())
        or locality_standing.get("locality_identity") != event.locality_identity
        or locality_standing.get("through_event_occurrence_identity")
        != act_occurrence.identity
        or type(assignments) is not dict
        or assignments.get(responsibility_assignment.identity, object()) is not None
        or type(movements) is not dict
        or event.identity in movements
        or type(event_count) is not int
        or event_count < 0
        or ledger.append_boundary_through_occurrence(event.identity)
        != ledger.append_boundary()
    ):
        raise ValueError("Assertion movement result Standing is not exact")
    exact = _assertion_carried_by_locality_movement_result(
        movement=event,
        responsibility_assignment=responsibility_assignment,
        source=source,
    )
    standing_additions = _exact_standing_additions(
        locality_standing,
        event,
        error_message="Assertion movement result Standing is not exact",
    )
    for key, added in standing_additions.items():
        for value in added:
            _record_distinct(locality_standing[key], value)
    movements[event.identity] = _assertion_locality_movement_occurrence_coordinates(
        ledger, event
    )
    locality_standing["through_event_occurrence_identity"] = event.identity
    locality_standing["event_count"] = event_count + 1
    return locality_standing, exact


def _carry_occurrence_position_measurement_assignment_into_standing(
    ledger: EventLedger,
    locality_standing: dict[str, Any],
    event,
    finding,
    *,
    prior_through_event_occurrence_identity: str,
) -> dict[str, Any]:
    """Carry the occurrence-position assignment produced beside this Standing."""

    if (
        type(locality_standing) is not dict
        or locality_standing.get("locality_identity") != event.locality_identity
        or locality_standing.get("through_event_occurrence_identity")
        != prior_through_event_occurrence_identity
    ):
        raise ValueError(
            "occurrence position assignment must follow its carried finding"
        )
    _require_carried_occurrence_position_assignment(
        ledger,
        responsibility_assignment=event,
        finding=finding,
    )
    assignments = locality_standing.get("subject_to_act_binding_occurrences")
    event_count = locality_standing.get("event_count")
    if (
        type(assignments) is not dict
        or event.identity in assignments
        or type(event_count) is not int
        or event_count < 0
    ):
        raise ValueError("occurrence position assignment Standing is not exact")
    standing_additions = _exact_standing_additions(
        locality_standing,
        event,
        error_message="occurrence position assignment Standing is not exact",
    )
    assignments[event.identity] = None
    for key, added in standing_additions.items():
        for value in added:
            _record_distinct(locality_standing[key], value)
    locality_standing["through_event_occurrence_identity"] = event.identity
    locality_standing["event_count"] = event_count + 1
    return locality_standing


def _carry_occurrence_position_measurement_result_into_standing(
    ledger: EventLedger,
    locality_standing: dict[str, Any],
    event,
    *,
    act_occurrence,
    responsibility_assignment,
    finding,
) -> dict[str, Any]:
    """Carry the occurrence-position result produced beside its exact Act."""

    measurements = (
        locality_standing.get("measurement_occurrences")
        if type(locality_standing) is dict
        else None
    )
    assignments = (
        locality_standing.get("subject_to_act_binding_occurrences")
        if type(locality_standing) is dict
        else None
    )
    event_count = (
        locality_standing.get("event_count")
        if type(locality_standing) is dict
        else None
    )
    assertions = _position_assertions(finding)
    result_material = _occurrence_position_result_material(
        finding,
        assignment=responsibility_assignment,
        assertions=assertions,
    )
    expected = {
        **result_material,
        "act_occurrence_event_identity": act_occurrence.identity,
        "yield_relation_identity": event.material.get(
            "yield_relation_identity"
        ),
    }
    yield_relation_identity = event.material.get("yield_relation_identity")
    yield_relation = ledger.get(yield_relation_identity) if type(yield_relation_identity) is str else None
    try:
        requirements = read_requirements_of_yield_relation(
            ledger,
            recorded_result_event_identity=event.identity,
            yield_relation_event_identity=yield_relation_identity,
            act_occurrence_event_identity=act_occurrence.identity,
        )
    except (TypeError, ValueError):
        requirements = {}
    if (
        event.kind != OCCURRENCE_POSITION_RECORDED_KIND
        or event.locality_identity != responsibility_assignment.locality_identity
        or event.material != expected
        or locality_standing.get("locality_identity") != event.locality_identity
        or locality_standing.get("through_event_occurrence_identity")
        != act_occurrence.identity
        or type(measurements) is not dict
        or event.identity in measurements
        or type(assignments) is not dict
        or responsibility_assignment.identity not in assignments
        or yield_relation is None
        or yield_relation.kind != RECORDED_YIELD_RELATION_EVENT
        or yield_relation.material.get("occurrence_boundary")
        != "occurrence_position_measurement"
        or yield_relation.material.get("result_kind") != OCCURRENCE_POSITION_RESULT_KIND
        or ledger.integrity_of(yield_relation.identity) == CORRUPTED
        or not all(requirements.values())
        or ledger.integrity_of(event.identity) == CORRUPTED
        or ledger.append_boundary_through_occurrence(event.identity)
        != ledger.append_boundary()
        or type(event_count) is not int
        or event_count < 0
    ):
        raise ValueError("occurrence position Measurement Standing is not exact")
    standing_additions = _exact_standing_additions(
        locality_standing,
        event,
        error_message="occurrence position Measurement Standing is not exact",
    )
    measurements[event.identity] = _measurement_occurrence_coordinates(event)
    for key, added in standing_additions.items():
        for value in added:
            _record_distinct(locality_standing[key], value)
    locality_standing["through_event_occurrence_identity"] = event.identity
    locality_standing["event_count"] = event_count + 1
    return locality_standing


def _carry_validated_pair_measurement_lifecycle_occurrence_into_standing(
    ledger: EventLedger,
    locality_standing: dict[str, Any],
    event,
    *,
    prior_through_event_occurrence_identity: str,
    destination_coordinate: str | None,
) -> dict[str, Any]:
    if (
        type(locality_standing) is not dict
        or ledger.get(event.identity) != event
        or ledger.integrity_of(event.identity) == CORRUPTED
        or event.locality_identity != locality_standing.get("locality_identity")
        or locality_standing.get("through_event_occurrence_identity")
        != prior_through_event_occurrence_identity
        or ledger.append_boundary_through_occurrence(event.identity)
        != ledger.append_boundary()
    ):
        raise ValueError("pair Measurement lifecycle Standing is not exact")
    try:
        ledger.occurrences_in_append_order(
            (prior_through_event_occurrence_identity, event.identity),
            locality_identity=event.locality_identity,
        )
    except ValueError as error:
        raise ValueError(
            "pair Measurement lifecycle Standing order is not exact"
        ) from error
    destination = (
        locality_standing[destination_coordinate]
        if destination_coordinate is not None
        else None
    )
    event_count = locality_standing.get("event_count")
    if (
        type(event_count) is not int
        or event_count < 0
        or (destination is not None and event.identity in destination)
    ):
        raise ValueError("pair Measurement lifecycle Standing is not exact")
    standing_additions = _exact_standing_additions(
        locality_standing,
        event,
        error_message="pair Measurement lifecycle Standing is not exact",
    )
    if destination is locality_standing["measurement_occurrences"]:
        destination[event.identity] = _measurement_occurrence_coordinates(event)
    elif destination is not None:
        destination[event.identity] = None
    for key, added in standing_additions.items():
        for value in added:
            _record_distinct(locality_standing[key], value)
    locality_standing["through_event_occurrence_identity"] = event.identity
    locality_standing["event_count"] = event_count + 1
    return locality_standing


def _carry_pair_applicability_binding_into_standing(
    ledger: EventLedger,
    locality_standing: dict[str, Any],
    binding,
    source,
    *,
    prior_through_event_occurrence_identity: str,
) -> dict[str, Any]:
    _require_exact_pair_subject_to_act_binding_event(ledger, binding, source)
    return _carry_validated_pair_measurement_lifecycle_occurrence_into_standing(
        ledger,
        locality_standing,
        binding,
        prior_through_event_occurrence_identity=prior_through_event_occurrence_identity,
        destination_coordinate="subject_to_act_binding_occurrences",
    )


def _carry_pair_measurement_binding_into_standing(
    ledger: EventLedger,
    locality_standing: dict[str, Any],
    binding,
    source,
    *,
    prior_through_event_occurrence_identity: str,
) -> dict[str, Any]:
    _require_exact_pair_subject_to_act_binding_event(ledger, binding, source)
    return _carry_validated_pair_measurement_lifecycle_occurrence_into_standing(
        ledger,
        locality_standing,
        binding,
        prior_through_event_occurrence_identity=prior_through_event_occurrence_identity,
        destination_coordinate="subject_to_act_binding_occurrences",
    )


def _carry_pair_applicability_act_into_standing(
    ledger: EventLedger,
    locality_standing: dict[str, Any],
    event,
    *,
    assignment,
    source,
    prior_through_event_occurrence_identity: str,
) -> dict[str, Any]:
    _require_exact_pair_applicability_act_event(
        ledger, event, assignment=assignment, source=source
    )
    return _carry_validated_pair_measurement_lifecycle_occurrence_into_standing(
        ledger,
        locality_standing,
        event,
        prior_through_event_occurrence_identity=prior_through_event_occurrence_identity,
        destination_coordinate=None,
    )


def _carry_pair_applicability_result_into_standing(
    ledger: EventLedger,
    locality_standing: dict[str, Any],
    event,
    *,
    assignment,
    source,
    applicability_act_occurrence,
    prior_through_event_occurrence_identity: str,
) -> dict[str, Any]:
    _require_exact_pair_applicability_result_event(
        ledger,
        event,
        assignment=assignment,
        source=source,
        applicability_act_occurrence=applicability_act_occurrence,
    )
    return _carry_validated_pair_measurement_lifecycle_occurrence_into_standing(
        ledger,
        locality_standing,
        event,
        prior_through_event_occurrence_identity=prior_through_event_occurrence_identity,
        destination_coordinate="applicability_result_occurrences",
    )


def _carry_pair_measurement_act_into_standing(
    ledger: EventLedger,
    locality_standing: dict[str, Any],
    event,
    *,
    assignment,
    source,
    applicability_event,
    applicability_act_occurrence,
    prior_through_event_occurrence_identity: str,
) -> dict[str, Any]:
    _require_exact_pair_measurement_act_event(
        ledger,
        event,
        assignment=assignment,
        applicability_binding=_pair_applicability_binding_of_result(
            ledger, applicability_event, source=source
        ),
        source=source,
        applicability_event=applicability_event,
        applicability_act_occurrence=applicability_act_occurrence,
    )
    return _carry_validated_pair_measurement_lifecycle_occurrence_into_standing(
        ledger,
        locality_standing,
        event,
        prior_through_event_occurrence_identity=prior_through_event_occurrence_identity,
        destination_coordinate=None,
    )


def _carry_pair_measurement_result_into_standing(
    ledger: EventLedger,
    locality_standing: dict[str, Any],
    event,
    *,
    act_occurrence,
    assignment,
    source,
    applicability_event,
    applicability_act_occurrence,
    prior_through_event_occurrence_identity: str,
) -> dict[str, Any]:
    _require_exact_pair_measurement_result_event(
        ledger,
        event,
        act_occurrence=act_occurrence,
        assignment=assignment,
        source=source,
        applicability_event=applicability_event,
        applicability_act_occurrence=applicability_act_occurrence,
    )
    return _carry_validated_pair_measurement_lifecycle_occurrence_into_standing(
        ledger,
        locality_standing,
        event,
        prior_through_event_occurrence_identity=prior_through_event_occurrence_identity,
        destination_coordinate="measurement_occurrences",
    )


def _carry_byte_pair_occurrence_position_measurement_assignment_into_standing(
    ledger: EventLedger,
    locality_standing: dict[str, Any],
    event,
    finding,
    *,
    prior_through_event_occurrence_identity: str,
) -> dict[str, Any]:
    """Carry the byte-pair position assignment produced beside this Standing."""

    if (
        type(locality_standing) is not dict
        or locality_standing.get("locality_identity") != event.locality_identity
        or locality_standing.get("through_event_occurrence_identity")
        != prior_through_event_occurrence_identity
    ):
        raise ValueError(
            "byte-pair position assignment must follow its carried finding"
        )
    _require_carried_byte_pair_occurrence_position_assignment(
        ledger,
        responsibility_assignment=event,
        finding=finding,
    )
    assignments = locality_standing.get("subject_to_act_binding_occurrences")
    event_count = locality_standing.get("event_count")
    if (
        type(assignments) is not dict
        or event.identity in assignments
        or type(event_count) is not int
        or event_count < 0
    ):
        raise ValueError("byte-pair position assignment Standing is not exact")
    standing_additions = _exact_standing_additions(
        locality_standing,
        event,
        error_message="byte-pair position assignment Standing is not exact",
    )
    assignments[event.identity] = None
    for key, added in standing_additions.items():
        for value in added:
            _record_distinct(locality_standing[key], value)
    locality_standing["through_event_occurrence_identity"] = event.identity
    locality_standing["event_count"] = event_count + 1
    return locality_standing


def _carry_byte_pair_occurrence_position_measurement_result_into_standing(
    locality_standing: dict[str, Any],
    event,
    *,
    prior_through_event_occurrence_identity: str,
) -> dict[str, Any]:
    """Carry the position-coordinate result produced by this console call."""

    if (
        type(locality_standing) is not dict
        or event.kind != BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND
        or locality_standing.get("locality_identity") != event.locality_identity
        or locality_standing.get("through_event_occurrence_identity")
        != prior_through_event_occurrence_identity
    ):
        raise ValueError(
            "position-coordinate Measurement must follow its carried Act and Yield"
        )
    measurements = locality_standing.get("measurement_occurrences")
    assignments = locality_standing.get("subject_to_act_binding_occurrences")
    acquisition_results = locality_standing.get("material_acquisition_result_occurrences")
    assignment = event.material.get("responsibility_assignment_reference")
    source_identity = event.material.get("source_material_acquisition_occurrence_identity")
    event_count = locality_standing.get("event_count")
    if (
        type(measurements) is not dict
        or type(assignments) is not dict
        or type(acquisition_results) is not list
        or type(assignment) is not dict
        or assignment.get("recorded_occurrence_identity") not in assignments
        or event.material.get("act_occurrence_event_identity")
            != prior_through_event_occurrence_identity
        or not any(
            type(occurrence) is dict
            and occurrence.get("result_occurrence_identity") == source_identity
            for occurrence in acquisition_results
        )
        or type(event.material.get("yield_relation_identity"))
        is not str
        or type(event.material.get("assertions")) is not dict
        or event.identity in measurements
        or type(event_count) is not int
        or event_count < 0
    ):
        raise ValueError("position-coordinate Measurement Standing is not exact")
    standing_additions = _exact_standing_additions(
        locality_standing,
        event,
        error_message="position-coordinate Measurement Standing is not exact",
    )
    measurements[event.identity] = _measurement_occurrence_coordinates(event)
    for key, added in standing_additions.items():
        for value in added:
            _record_distinct(locality_standing[key], value)
    locality_standing["through_event_occurrence_identity"] = event.identity
    locality_standing["event_count"] = event_count + 1
    return locality_standing


def _carry_operator_material_source_occurrence_into_standing(
    ledger: EventLedger,
    locality_standing: dict[str, Any],
    event,
    *,
    prior_through_event_occurrence_identity: str,
) -> dict[str, Any]:
    """Carry one source occurrence produced by this console call."""

    if (
        type(locality_standing) is not dict
        or event.kind not in _OPERATOR_MATERIAL_SOURCE_KINDS
        or locality_standing.get("locality_identity") != event.locality_identity
        or locality_standing.get("through_event_occurrence_identity")
        != prior_through_event_occurrence_identity
    ):
        raise ValueError("operator material source coordinates are not exact")
    bindings = locality_standing.get("subject_to_act_binding_occurrences")
    acts = locality_standing.get("operator_material_source_act_occurrences")
    locality_relations = locality_standing.get(
        "material_locality_relation_occurrences"
    )
    material_acquisition_result_occurrences = locality_standing.get("material_acquisition_result_occurrences")
    exact_results = locality_standing.get("exact_result_occurrences")
    event_count = locality_standing.get("event_count")
    if (
        type(bindings) is not dict
        or type(acts) is not dict
        or type(locality_relations) is not dict
        or type(material_acquisition_result_occurrences) is not list
        or type(exact_results) is not dict
        or type(event_count) is not int
        or event_count < 0
    ):
        raise ValueError("operator material source coordinates are not exact")
    if event.kind == OPERATOR_MATERIAL_SOURCE_SUBJECT_TO_ACT_BINDING_RECORDED_KIND:
        source = event.material.get("current_coordinate_reference")
        if (
            type(source) is not dict
            or source.get("through_event_occurrence_identity")
            != prior_through_event_occurrence_identity
            or event.identity in bindings
        ):
            raise ValueError("operator material source binding is not exact")
    elif event.kind == OPERATOR_MATERIAL_SOURCE_ACT_OCCURRENCE_EVENT:
        binding = event.material.get("subject_to_act_binding_reference")
        if (
            type(binding) is not dict
            or binding.get("recorded_occurrence_identity")
            != prior_through_event_occurrence_identity
            or prior_through_event_occurrence_identity not in bindings
            or event.identity in acts
        ):
            raise ValueError("operator material source Act is not exact")
    else:
        if (
            event.material.get("act_occurrence_event_identity")
            != prior_through_event_occurrence_identity
            or prior_through_event_occurrence_identity not in acts
            or type(event.material.get("yield_relation_identity"))
            is not str
            or type(event.exact_material) is not bytes
            or event.identity in exact_results
            or event.identity in locality_relations
        ):
            raise ValueError("operator material source result is not exact")
    standing_additions = _exact_standing_additions(
        locality_standing,
        event,
        error_message="operator material source coordinates are not exact",
    )
    if event.kind == OPERATOR_MATERIAL_SOURCE_SUBJECT_TO_ACT_BINDING_RECORDED_KIND:
        bindings[event.identity] = None
    elif event.kind == OPERATOR_MATERIAL_SOURCE_ACT_OCCURRENCE_EVENT:
        acts[event.identity] = None
    else:
        exact_results[event.identity] = _subject_to_act_binding_of_exact_result(
            ledger, event
        )
        locality_relations[event.identity] = {
            "locality_relation": deepcopy(event.material["locality_relation"]),
        }
        material_acquisition_result_occurrences.append(
            {
                "subject_reference": event.material["dimensions"]["identity"],
                "result_occurrence_identity": event.identity,
                "source_role": event.material["source_role"],
            }
        )
    for key, added in standing_additions.items():
        for value in added:
            _record_distinct(locality_standing[key], value)
    locality_standing["through_event_occurrence_identity"] = event.identity
    locality_standing["event_count"] = event_count + 1
    return locality_standing


def _carry_recorded_pair_comparison_occurrence_into_standing(
    locality_standing: dict[str, Any],
    event,
    *,
    prior_through_event_occurrence_identity: str,
) -> dict[str, Any]:
    """Carry one pair-Compare occurrence produced by this console call."""

    carried_kinds = _RECORDED_PAIR_MEASUREMENT_COMPARISON_KINDS
    if (
        type(locality_standing) is not dict
        or event.kind not in carried_kinds
        or locality_standing.get("locality_identity") != event.locality_identity
        or locality_standing.get("through_event_occurrence_identity")
        != prior_through_event_occurrence_identity
    ):
        raise ValueError("recorded pair comparison Standing is not exact")
    assignments = locality_standing.get("subject_to_act_binding_occurrences")
    applicability = locality_standing.get("applicability_result_occurrences")
    comparisons = locality_standing.get("comparison_result_occurrences")
    event_count = locality_standing.get("event_count")
    if (
        type(assignments) is not dict
        or type(applicability) is not dict
        or type(comparisons) is not dict
        or type(event_count) is not int
        or event_count < 0
    ):
        raise ValueError("recorded pair comparison Standing is not exact")
    if event.kind == RECORDED_PAIR_MEASUREMENT_COMPARISON_RESPONSIBILITY_ASSIGNMENT_KIND:
        measurements = locality_standing.get("measurement_occurrences")
        earlier = event.material.get("earlier_measurement_reference")
        later = event.material.get("later_measurement_reference")
        if (
            type(measurements) is not dict
            or type(earlier) is not dict
            or type(later) is not dict
            or earlier.get("recorded_occurrence_identity") not in measurements
            or later.get("recorded_occurrence_identity") not in measurements
            or event.material.get("standing_boundary_identity")
            != prior_through_event_occurrence_identity
            or event.identity in assignments
        ):
            raise ValueError("recorded pair comparison assignment is not exact")
    elif event.kind == RECORDED_PAIR_MEASUREMENT_COMPARISON_APPLICABILITY_ACT_OCCURRENCE_EVENT:
        assignment = event.material.get("responsibility_assignment_reference")
        if (
            type(assignment) is not dict
            or assignment.get("recorded_occurrence_identity")
            != prior_through_event_occurrence_identity
            or prior_through_event_occurrence_identity not in assignments
        ):
            raise ValueError(
                "recorded pair comparison Applicability Act is not exact"
            )
    elif event.kind == RECORDED_PAIR_MEASUREMENT_COMPARISON_APPLICABILITY_RESULT_KIND:
        assignment = event.material.get("responsibility_assignment_reference")
        if (
            type(assignment) is not dict
            or assignment.get("recorded_occurrence_identity") not in assignments
            or event.material.get("act_occurrence_event_identity")
            != prior_through_event_occurrence_identity
            or event.material.get("standing") != "applicable"
            or event.identity in applicability
        ):
            raise ValueError("recorded pair comparison Applicability is not exact")
    elif event.kind == RECORDED_PAIR_MEASUREMENT_COMPARISON_ACT_OCCURRENCE_EVENT:
        assignment = event.material.get("responsibility_assignment_reference")
        if (
            type(assignment) is not dict
            or assignment.get("recorded_occurrence_identity") not in assignments
            or event.material.get("applicability_result_event_identity")
            != prior_through_event_occurrence_identity
            or prior_through_event_occurrence_identity not in applicability
        ):
            raise ValueError("recorded pair comparison Act is not exact")
    else:
        assignment = event.material.get("responsibility_assignment_reference")
        if (
            type(assignment) is not dict
            or assignment.get("recorded_occurrence_identity") not in assignments
            or event.material.get("act_occurrence_event_identity")
            != prior_through_event_occurrence_identity
            or event.material.get("applicability_result_event_identity")
            not in applicability
            or event.identity in comparisons
        ):
            raise ValueError("recorded pair comparison result is not exact")
    standing_additions = _exact_standing_additions(
        locality_standing,
        event,
        error_message="recorded pair comparison Standing is not exact",
    )
    if event.kind == RECORDED_PAIR_MEASUREMENT_COMPARISON_RESPONSIBILITY_ASSIGNMENT_KIND:
        assignments[event.identity] = None
    elif event.kind == RECORDED_PAIR_MEASUREMENT_COMPARISON_APPLICABILITY_RESULT_KIND:
        applicability[event.identity] = None
    elif event.kind == RECORDED_PAIR_MEASUREMENT_COMPARISON_RESULT_KIND:
        comparisons[event.identity] = None
    for key, added in standing_additions.items():
        for value in added:
            _record_distinct(locality_standing[key], value)
    locality_standing["through_event_occurrence_identity"] = event.identity
    locality_standing["event_count"] = event_count + 1
    return locality_standing
