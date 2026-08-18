"""Deterministic Locality Standing read over preserved ingest events."""

from __future__ import annotations


from bisect import bisect_left
from contextvars import ContextVar
from copy import deepcopy
from functools import wraps
from typing import Any, Iterable

from seed_runtime.events import CORRUPTED, EventLedger
from seed_runtime.material_ingest import MATERIAL_INGEST_OCCURRED_KIND
from seed_runtime.byte_measurement import (
    BYTE_MEASUREMENT_RECORDED_KIND,
    BYTE_MEASUREMENT_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND,
    BYTE_MEASUREMENT_RESPONSIBLE_ACT_EVIDENCE_KIND,
    BYTE_PAIR_MEASUREMENT_RECORDED_KIND,
    BYTE_PAIR_MEASUREMENT_RESULT_KIND,
    BYTE_PAIR_MEASUREMENT_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND,
    BYTE_PAIR_APPLICABILITY_ACT_EVIDENCE_KIND,
    BYTE_PAIR_APPLICABILITY_RECORDED_KIND,
    BYTE_PAIR_RESPONSIBLE_ACT_EVIDENCE_KIND,
    ASSERTION_LOCALITY_MOVEMENT_RESPONSIBILITY_ASSIGNMENT_KIND,
    ASSERTION_LOCALITY_MOVEMENT_ACT_EVIDENCE_KIND,
    ASSERTION_LOCALITY_MOVEMENT_KIND,
    ASSERTION_LOCALITY_MOVEMENT_RESULT_KIND,
    MeasuredByteInputs,
    MeasuredBytePairInputs,
    RecordedByteAssertion,
    _moved_byte_assertion_from_carried_source,
    _movement_act_material,
    _movement_assignment_material,
    _movement_result_material,
    _source_measurement_standing_coordinates,
    _findings_of_recorded_byte_position_pair_measurement,
    _read_assertion_locality_movement_responsibility_assignment,
    _read_assertion_locality_movement_act_evidence,
    _read_byte_measurement_responsibility_assignment,
    _read_pair_measurement_responsibility_assignment,
    _read_pair_applicability_act_evidence,
    _read_recorded_pair_input_applicability,
    _read_pair_measurement_act_evidence,
    _require_exact_pair_measurement_assignment_event,
    _require_exact_pair_applicability_act_event,
    _require_exact_pair_applicability_result_event,
    _require_exact_pair_measurement_act_event,
    _require_exact_pair_measurement_result_event,
    _require_exact_pair_measurement_result_from_measured_inputs,
    _require_exact_byte_measurement_assignment_from_measured_inputs,
    _require_exact_byte_measurement_act_from_measured_inputs,
    _require_exact_byte_measurement_result_from_measured_inputs,
    _validate_moved_byte_assertion,
    assertions_of_recorded_byte_measurement,
)
from seed_runtime.occurrence_position_measurement import (
    OCCURRENCE_POSITION_ACT_EVIDENCE_KIND,
    OCCURRENCE_POSITION_RECORDED_KIND,
    OCCURRENCE_POSITION_RESULT_KIND,
    OCCURRENCE_POSITION_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND,
    _occurrence_position_result_material,
    _position_assertions,
    _require_carried_occurrence_position_assignment,
    get_occurrence_position_measurement_responsibility_assignment,
    get_recorded_occurrence_position_measurement,
)
from seed_runtime.evidence_of_yield_relation import (
    RECORDED_EVIDENCE_OF_YIELD_RELATION_KIND,
    read_requirements_of_yield_relation,
)
from seed_runtime.measurement_of_recurrent_byte_pair_occurrence_position import (
    RECORDED_RESPONSIBILITY_ASSIGNMENT_OF_MEASUREMENT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_KIND,
    RECORDED_EVIDENCE_OF_ACT_OCCURRENCE_OF_MEASUREMENT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_KIND,
    RECORDING_OCCURRENCE_OF_RESULT_OF_MEASUREMENT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_KIND,
    _read_responsibility_assignment_for_measurement_of_recurrent_byte_pair_occurrence_position,
    _read_recorded_result_of_measurement_of_recurrent_byte_pair_occurrence_position,
)
from seed_runtime.measurement_of_position_coordinates_of_byte_pair_occurrences import (
    BYTE_PAIR_OCCURRENCE_POSITION_ASSIGNMENT_KIND,
    BYTE_PAIR_OCCURRENCE_POSITION_ACT_EVIDENCE_KIND,
    BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND,
    _require_carried_byte_pair_occurrence_position_assignment,
    get_byte_pair_occurrence_position_measurement_responsibility_assignment,
    get_byte_pair_occurrence_position_measurement_act_evidence,
    get_recorded_byte_pair_occurrence_position_measurement,
)
from seed_runtime.measurement_of_shared_position_of_byte_pair_occurrences import (
    SHARED_POSITION_RESPONSIBILITY_ASSIGNMENT_KIND,
    SHARED_POSITION_APPLICABILITY_ACT_EVIDENCE_KIND,
    SHARED_POSITION_APPLICABILITY_RESULT_KIND,
    SHARED_POSITION_MEASUREMENT_ACT_EVIDENCE_KIND,
    SHARED_POSITION_MEASUREMENT_RESULT_KIND,
    _read_assignment as _read_shared_position_assignment,
    _read_applicability_act as _read_shared_position_applicability_act,
    _read_applicability_result as _read_shared_position_applicability_result,
    _read_measurement_act as _read_shared_position_measurement_act,
    _read_measurement_result as _read_shared_position_measurement_result,
)
from seed_runtime.addressed_byte_occurrence_reference_determination import (
    RESPONSIBILITY_ASSIGNMENT_KIND as ADDRESSED_BYTE_REFERENCE_RESPONSIBILITY_ASSIGNMENT_KIND,
    APPLICABILITY_ACT_EVIDENCE_KIND as ADDRESSED_BYTE_REFERENCE_APPLICABILITY_ACT_EVIDENCE_KIND,
    APPLICABILITY_RESULT_KIND as ADDRESSED_BYTE_REFERENCE_APPLICABILITY_RESULT_KIND,
    DETERMINATION_ACT_EVIDENCE_KIND as ADDRESSED_BYTE_REFERENCE_DETERMINATION_ACT_EVIDENCE_KIND,
    DETERMINATION_RESULT_KIND as ADDRESSED_BYTE_REFERENCE_DETERMINATION_RESULT_KIND,
    _read_assignment as _read_addressed_byte_reference_assignment,
    _read_applicability_act as _read_addressed_byte_reference_applicability_act,
    _read_applicability_result as _read_addressed_byte_reference_applicability_result,
    _read_determination_act as _read_addressed_byte_reference_determination_act,
    _read_determination_result as _read_addressed_byte_reference_determination_result,
    _determination_result_reference as _addressed_byte_reference_determination_coordinates,
)
from seed_runtime.measurement_of_source_position_coordinates_carrying_addressed_material import (
    RESPONSIBILITY_ASSIGNMENT_KIND as ADDRESSED_MATERIAL_COORDINATE_RESPONSIBILITY_ASSIGNMENT_KIND,
    APPLICABILITY_ACT_EVIDENCE_KIND as ADDRESSED_MATERIAL_COORDINATE_APPLICABILITY_ACT_EVIDENCE_KIND,
    APPLICABILITY_RESULT_KIND as ADDRESSED_MATERIAL_COORDINATE_APPLICABILITY_RESULT_KIND,
    MEASUREMENT_ACT_EVIDENCE_KIND as ADDRESSED_MATERIAL_COORDINATE_MEASUREMENT_ACT_EVIDENCE_KIND,
    MEASUREMENT_RESULT_KIND as ADDRESSED_MATERIAL_COORDINATE_MEASUREMENT_RESULT_KIND,
    _read_assignment as _read_addressed_material_coordinate_assignment,
    _read_applicability_act as _read_addressed_material_coordinate_applicability_act,
    _read_applicability_result as _read_addressed_material_coordinate_applicability_result,
    _read_measurement_act as _read_addressed_material_coordinate_measurement_act,
    _read_measurement_result as _read_addressed_material_coordinate_measurement_result,
    measurement_result_reference as _addressed_material_coordinate_measurement_coordinates,
)
from seed_runtime.operator_standing_continuation import (
    STANDING_LOCALITY_CONTINUATION_ACT_EVIDENCE_KIND,
    STANDING_LOCALITY_CONTINUATION_RECORDED_KIND,
    STANDING_LOCALITY_CONTINUATION_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND,
    get_recorded_standing_locality_continuation,
    get_standing_locality_continuation_responsibility_assignment,
)
from seed_runtime.operator_checkpoint import (
    STANDING_BOUNDARY_REFERENCE_ACT_EVIDENCE_KIND,
    STANDING_BOUNDARY_REFERENCE_RECORDED_KIND,
    STANDING_BOUNDARY_REFERENCE_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND,
    get_recorded_standing_boundary_reference,
    get_standing_boundary_reference_act_evidence,
    get_standing_boundary_reference_responsibility_assignment,
)
from seed_runtime.standing_boundary_locality import (
    RECORDED_STANDING_BOUNDARY_LOCALITY_ACT_EVIDENCE_KIND,
    RECORDED_STANDING_BOUNDARY_LOCALITY_RECORDED_KIND,
    RECORDED_STANDING_BOUNDARY_LOCALITY_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND,
    get_recorded_standing_boundary_locality,
    get_recorded_standing_boundary_locality_act_evidence,
    get_recorded_standing_boundary_locality_responsibility_assignment,
)
from seed_runtime.operator_material_acquisition import (
    OPERATOR_MATERIAL_ACQUIRE_ACT_EVIDENCE_KIND,
    OPERATOR_MATERIAL_ACQUIRE_RECORDED_KIND,
    OPERATOR_MATERIAL_ACQUIRE_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND,
    get_operator_material_acquire_act_evidence,
    get_operator_material_acquire_responsibility_assignment,
    get_recorded_operator_material_acquire,
)
from seed_runtime.operator_system_locality import (
    OPERATOR_SYSTEM_LOCALITY_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND,
    OPERATOR_SYSTEM_LOCALITY_ACT_EVIDENCE_KIND,
    OPERATOR_SYSTEM_LOCALITY_RECORDED_KIND,
    get_operator_system_locality_responsibility_assignment,
    get_operator_system_locality_act_evidence,
    get_recorded_operator_system_locality,
)
from seed_runtime.operator_representation_admission import (
    REPRESENTATION_CANDIDATE_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND,
    REPRESENTATION_CANDIDATE_ACT_EVIDENCE_KIND,
    REPRESENTATION_CANDIDATE_RECORDED_KIND,
    EXACT_MATERIAL_REPRESENTATION_ADMISSION_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND,
    EXACT_MATERIAL_REPRESENTATION_ADMISSION_ACT_EVIDENCE_KIND,
    EXACT_MATERIAL_REPRESENTATION_ADMISSION_RECORDED_KIND,
    get_representation_candidate_responsibility_assignment,
    get_representation_candidate_act_evidence,
    get_recorded_representation_candidate,
    get_exact_material_representation_admission_responsibility_assignment,
    get_exact_material_representation_admission_act_evidence,
    get_recorded_exact_material_representation_admission,
)
from seed_runtime.operator_representation_applicability import (
    REPRESENTATION_EMISSION_APPLICABILITY_ACT_EVIDENCE_KIND,
    REPRESENTATION_EMISSION_APPLICABILITY_RECORDED_KIND,
    get_representation_emission_applicability_act_evidence,
    get_recorded_representation_emission_applicability,
)
from seed_runtime.comparison_of_recorded_byte_pair_measurements import (
    RECORDED_PAIR_MEASUREMENT_COMPARISON_RESPONSIBILITY_ASSIGNMENT_KIND,
    RECORDED_PAIR_MEASUREMENT_COMPARISON_APPLICABILITY_ACT_EVIDENCE_KIND,
    RECORDED_PAIR_MEASUREMENT_COMPARISON_APPLICABILITY_RESULT_KIND,
    RECORDED_PAIR_MEASUREMENT_COMPARISON_ACT_EVIDENCE_KIND,
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
    COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_APPLICABILITY_ACT_EVIDENCE_KIND,
    COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_APPLICABILITY_RESULT_KIND,
    COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_COMPARE_ACT_EVIDENCE_KIND,
    COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_RESULT_KIND,
    get_comparison_of_ordered_relation_path_with_recorded_pair_findings_responsibility_assignment,
    get_comparison_of_ordered_relation_path_with_recorded_pair_findings_applicability_act_evidence,
    get_recorded_comparison_of_ordered_relation_path_with_recorded_pair_findings_applicability,
    get_comparison_of_ordered_relation_path_with_recorded_pair_findings_act_evidence,
    get_recorded_comparison_of_ordered_relation_path_with_recorded_pair_findings,
)
# The writer of these occurrences declares their kinds. A reader declaring its
# own copy would be a second contract, free to drift from the first.
from seed_runtime.operator_representation import (
    REPRESENTATION_RECORDED_KIND as _REPRESENTATION_RECORDED_KIND,
    REPRESENTATION_ACT_EVIDENCE_KIND as _REPRESENTATION_ACT_EVIDENCE_KIND,
    REPRESENTATION_LOCALITY_EVIDENCE_KIND as _REPRESENTATION_LOCALITY_EVIDENCE_KIND,
    REPRESENTATION_EMISSION_ATTEMPT_KIND as _REPRESENTATION_EMISSION_ATTEMPT_KIND,
    REPRESENTATION_EMITTED_KIND as _REPRESENTATION_EMITTED_KIND,
    REPRESENTATION_BOUNDARY_FAILURE_KIND as _REPRESENTATION_BOUNDARY_FAILURE_KIND,
    REPRESENTATION_BOUNDARY_FAILURE_ACT_EVIDENCE_KIND as _REPRESENTATION_BOUNDARY_FAILURE_ACT_EVIDENCE_KIND,
    REPRESENTATION_EMISSION_ACT_EVIDENCE_KIND as _REPRESENTATION_EMISSION_ACT_EVIDENCE_KIND,
    REPRESENTATION_EMISSION_LOCALITY_EVIDENCE_KIND as _REPRESENTATION_EMISSION_LOCALITY_EVIDENCE_KIND,
    REPRESENTATION_EMISSION_ATTEMPT_LOCALITY_EVIDENCE_KIND as _REPRESENTATION_EMISSION_ATTEMPT_LOCALITY_EVIDENCE_KIND,
)


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
    ingest_occurrences: list[dict[str, Any]],
    responsibility_assignment_occurrences: dict[str, None],
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
        or exact[3] is not ingest_occurrences
        or exact[4] is not responsibility_assignment_occurrences
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
            "ingest_occurrences": ingest_occurrences,
            "responsibility_assignment_occurrences": (
                responsibility_assignment_occurrences
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
    MATERIAL_INGEST_OCCURRED_KIND: "ingest_occurrence",
}
_MEASUREMENT_ACT_EVIDENCE_KINDS = {
    BYTE_MEASUREMENT_RESPONSIBLE_ACT_EVIDENCE_KIND,
    OCCURRENCE_POSITION_ACT_EVIDENCE_KIND,
    RECORDED_EVIDENCE_OF_ACT_OCCURRENCE_OF_MEASUREMENT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_KIND,
    BYTE_PAIR_OCCURRENCE_POSITION_ACT_EVIDENCE_KIND,
}
_MEASUREMENT_RESPONSIBILITY_ASSIGNMENT_KINDS = {
    BYTE_MEASUREMENT_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND,
    OCCURRENCE_POSITION_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND,
    RECORDED_RESPONSIBILITY_ASSIGNMENT_OF_MEASUREMENT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_KIND,
    BYTE_PAIR_OCCURRENCE_POSITION_ASSIGNMENT_KIND,
    ASSERTION_LOCALITY_MOVEMENT_RESPONSIBILITY_ASSIGNMENT_KIND,
    BYTE_PAIR_MEASUREMENT_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND,
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
    ASSERTION_LOCALITY_MOVEMENT_RESPONSIBILITY_ASSIGNMENT_KIND,
    ASSERTION_LOCALITY_MOVEMENT_ACT_EVIDENCE_KIND,
    ASSERTION_LOCALITY_MOVEMENT_KIND,
}
_BYTE_PAIR_MEASUREMENT_LIFECYCLE_KINDS = {
    BYTE_PAIR_MEASUREMENT_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND,
    BYTE_PAIR_APPLICABILITY_ACT_EVIDENCE_KIND,
    BYTE_PAIR_APPLICABILITY_RECORDED_KIND,
    BYTE_PAIR_RESPONSIBLE_ACT_EVIDENCE_KIND,
    BYTE_PAIR_MEASUREMENT_RECORDED_KIND,
}
_STANDING_LOCALITY_CONTINUATION_KINDS = {
    STANDING_LOCALITY_CONTINUATION_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND,
    STANDING_LOCALITY_CONTINUATION_ACT_EVIDENCE_KIND,
    STANDING_LOCALITY_CONTINUATION_RECORDED_KIND,
}
_STANDING_BOUNDARY_REFERENCE_KINDS = {
    STANDING_BOUNDARY_REFERENCE_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND,
    STANDING_BOUNDARY_REFERENCE_ACT_EVIDENCE_KIND,
    STANDING_BOUNDARY_REFERENCE_RECORDED_KIND,
}
_RECORDED_STANDING_BOUNDARY_LOCALITY_KINDS = {
    RECORDED_STANDING_BOUNDARY_LOCALITY_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND,
    RECORDED_STANDING_BOUNDARY_LOCALITY_ACT_EVIDENCE_KIND,
    RECORDED_STANDING_BOUNDARY_LOCALITY_RECORDED_KIND,
}
_OPERATOR_MATERIAL_ACQUIRE_KINDS = {
    OPERATOR_MATERIAL_ACQUIRE_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND,
    OPERATOR_MATERIAL_ACQUIRE_ACT_EVIDENCE_KIND,
    OPERATOR_MATERIAL_ACQUIRE_RECORDED_KIND,
}
_OPERATOR_SYSTEM_LOCALITY_KINDS = {
    OPERATOR_SYSTEM_LOCALITY_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND,
    OPERATOR_SYSTEM_LOCALITY_ACT_EVIDENCE_KIND,
    OPERATOR_SYSTEM_LOCALITY_RECORDED_KIND,
}
_REPRESENTATION_CANDIDATE_ADMISSION_KINDS = {
    REPRESENTATION_CANDIDATE_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND,
    REPRESENTATION_CANDIDATE_ACT_EVIDENCE_KIND,
    REPRESENTATION_CANDIDATE_RECORDED_KIND,
    EXACT_MATERIAL_REPRESENTATION_ADMISSION_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND,
    EXACT_MATERIAL_REPRESENTATION_ADMISSION_ACT_EVIDENCE_KIND,
    EXACT_MATERIAL_REPRESENTATION_ADMISSION_RECORDED_KIND,
}
_REPRESENTATION_EMISSION_APPLICABILITY_KINDS = {
    REPRESENTATION_EMISSION_APPLICABILITY_ACT_EVIDENCE_KIND,
    REPRESENTATION_EMISSION_APPLICABILITY_RECORDED_KIND,
}
_RECORDED_PAIR_MEASUREMENT_COMPARISON_KINDS = {
    RECORDED_PAIR_MEASUREMENT_COMPARISON_RESPONSIBILITY_ASSIGNMENT_KIND,
    RECORDED_PAIR_MEASUREMENT_COMPARISON_APPLICABILITY_ACT_EVIDENCE_KIND,
    RECORDED_PAIR_MEASUREMENT_COMPARISON_APPLICABILITY_RESULT_KIND,
    RECORDED_PAIR_MEASUREMENT_COMPARISON_ACT_EVIDENCE_KIND,
    RECORDED_PAIR_MEASUREMENT_COMPARISON_RESULT_KIND,
}
_SHARED_POSITION_MEASUREMENT_KINDS = {
    SHARED_POSITION_RESPONSIBILITY_ASSIGNMENT_KIND,
    SHARED_POSITION_APPLICABILITY_ACT_EVIDENCE_KIND,
    SHARED_POSITION_APPLICABILITY_RESULT_KIND,
    SHARED_POSITION_MEASUREMENT_ACT_EVIDENCE_KIND,
    SHARED_POSITION_MEASUREMENT_RESULT_KIND,
}
_ADDRESSED_BYTE_REFERENCE_DETERMINATION_KINDS = {
    ADDRESSED_BYTE_REFERENCE_RESPONSIBILITY_ASSIGNMENT_KIND,
    ADDRESSED_BYTE_REFERENCE_APPLICABILITY_ACT_EVIDENCE_KIND,
    ADDRESSED_BYTE_REFERENCE_APPLICABILITY_RESULT_KIND,
    ADDRESSED_BYTE_REFERENCE_DETERMINATION_ACT_EVIDENCE_KIND,
    ADDRESSED_BYTE_REFERENCE_DETERMINATION_RESULT_KIND,
}
_ADDRESSED_MATERIAL_COORDINATE_MEASUREMENT_KINDS = {
    ADDRESSED_MATERIAL_COORDINATE_RESPONSIBILITY_ASSIGNMENT_KIND,
    ADDRESSED_MATERIAL_COORDINATE_APPLICABILITY_ACT_EVIDENCE_KIND,
    ADDRESSED_MATERIAL_COORDINATE_APPLICABILITY_RESULT_KIND,
    ADDRESSED_MATERIAL_COORDINATE_MEASUREMENT_ACT_EVIDENCE_KIND,
    ADDRESSED_MATERIAL_COORDINATE_MEASUREMENT_RESULT_KIND,
}
_COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_KINDS = {
    COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_RESPONSIBILITY_ASSIGNMENT_KIND,
    COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_APPLICABILITY_ACT_EVIDENCE_KIND,
    COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_APPLICABILITY_RESULT_KIND,
    COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_COMPARE_ACT_EVIDENCE_KIND,
    COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_RESULT_KIND,
}
_SUPPORTED_KINDS = {
    *_SUBJECT_BY_KIND,
    *_MEASUREMENT_ACT_EVIDENCE_KINDS,
    *_MEASUREMENT_RESPONSIBILITY_ASSIGNMENT_KINDS,
    *_MEASUREMENT_RECORDED_KINDS,
    *_ASSERTION_LOCALITY_MOVEMENT_KINDS,
    *_BYTE_PAIR_MEASUREMENT_LIFECYCLE_KINDS,
    *_STANDING_LOCALITY_CONTINUATION_KINDS,
    *_STANDING_BOUNDARY_REFERENCE_KINDS,
    *_RECORDED_STANDING_BOUNDARY_LOCALITY_KINDS,
    *_OPERATOR_MATERIAL_ACQUIRE_KINDS,
    *_OPERATOR_SYSTEM_LOCALITY_KINDS,
    *_REPRESENTATION_CANDIDATE_ADMISSION_KINDS,
    *_REPRESENTATION_EMISSION_APPLICABILITY_KINDS,
    *_RECORDED_PAIR_MEASUREMENT_COMPARISON_KINDS,
    *_SHARED_POSITION_MEASUREMENT_KINDS,
    *_ADDRESSED_BYTE_REFERENCE_DETERMINATION_KINDS,
    *_ADDRESSED_MATERIAL_COORDINATE_MEASUREMENT_KINDS,
    *_COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_KINDS,
    _REPRESENTATION_RECORDED_KIND,
    _REPRESENTATION_ACT_EVIDENCE_KIND,
    _REPRESENTATION_LOCALITY_EVIDENCE_KIND,
    _REPRESENTATION_EMISSION_ATTEMPT_KIND,
    _REPRESENTATION_EMITTED_KIND,
    _REPRESENTATION_BOUNDARY_FAILURE_KIND,
    _REPRESENTATION_BOUNDARY_FAILURE_ACT_EVIDENCE_KIND,
    _REPRESENTATION_EMISSION_ACT_EVIDENCE_KIND,
    _REPRESENTATION_EMISSION_LOCALITY_EVIDENCE_KIND,
    _REPRESENTATION_EMISSION_ATTEMPT_LOCALITY_EVIDENCE_KIND,
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
        "responsible_act_evidence_identity": event.material[
            "responsible_act_evidence_identity"
        ],
        "evidence_of_yield_relation_identity": event.material["evidence_of_yield_relation_identity"],
    }


def _carries_exact_result(ledger: EventLedger, event) -> bool:
    """Whether this exact occurrence's intact Yield carries exact result bytes."""

    if (
        type(event.exact_material) is not bytes
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        return False
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
    return all(requirements.values())


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
        "source_standing_through_event_occurrence_identity": source[
            "standing_boundary_event_identity"
        ],
        "addressed_representation_event_identity": source[
            "addressed_representation_event_identity"
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
        continuation = get_recorded_standing_locality_continuation(
            ledger, recorded_occurrence_identity
        )
        source_reference = deepcopy(continuation["source_standing_reference"])
    else:
        source_reference = _source_reference_from_checkout(
            ledger, recorded_occurrence_identity
        )

    source_locality_identity = _require_recorded_standing_identity(
        source_reference.get("source_locality_identity"),
        "recorded Standing reference carries no exact source Locality",
    )
    _require_recorded_standing_identity(
        source_reference.get("addressed_representation_event_identity"),
        "recorded Standing reference carries no addressed Representation",
    )
    through_event_occurrence_identity = source_reference.get(
        "source_standing_through_event_occurrence_identity"
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
    occurrence representations.

    Every accumulator the live event kinds read is seeded from `prior`, and the
    per-event branches and refusals below are the same ones replay uses. Those
    refusals consult accumulated Standing rather than the ledger, which is why
    seeding preserves them (`#2376`).

    **The advance has as input `prior`.** Its accumulators are taken over rather
    than copied, and the returned Standing shares them. A caller that needs the
    earlier Standing to stay as it was must read it again; there is no
    snapshot here.

    That is not defensive weakness, it is the point. Standing grows with the
    Locality, so copying it per advance would cost the Locality event count every
    time and reinstate the quadratic this replaced. The console holds one
    Standing, hands it forward, and keeps no earlier one.

    The result is fully recomputable
    from the ledger and is not itself recorded: it returns only standings,
    limits, and Unknown the Locality's events already carry.  An empty
    coordinate is absence of record, not negative standing and not Unknown.
    No Yield is established for represented relation candidates here; each preserved ingest keeps
    the authority its own event recorded.
    """
    events = ledger.occurrences_in_append_order(
        event_identities,
        locality_identity=locality_identity,
    )
    scope = f"locality:{locality_identity}"
    ingest_occurrences: list[dict[str, Any]] = []
    measurement_occurrences: dict[str, dict[str, str]] = {}
    exact_result_occurrences: dict[str, None] = {}
    representations: dict[str, dict[str, Any]] = {}
    recorded_relation_Standing: dict[str, None] = {}
    recorded_standing_boundary_references: dict[str, None] = {}
    recorded_standing_boundary_locality_relations: dict[str, None] = {}
    operator_invocation_locality_relations: dict[str, None] = {}
    responsibility_assignment_occurrences: dict[str, None] = {}
    operator_material_acquire_act_occurrences: dict[str, None] = {}
    candidate_result_occurrences: dict[str, None] = {}
    admission_result_occurrences: dict[str, None] = {}
    applicability_result_occurrences: dict[str, None] = {}
    comparison_result_occurrences: dict[str, None] = {}
    recorded_pair_comparison_replay_carries: dict[str, dict[str, Any]] = {}
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

    replay_started_from_empty = prior is None
    if prior is not None:
        # Every accumulator the live event kinds read, taken over from the
        # Standing that already input the earlier occurrences.  Not copied:
        # see the shared-accumulator note above.
        ingest_occurrences = prior["ingest_occurrences"]
        measurement_occurrences = prior["measurement_occurrences"]
        if type(measurement_occurrences) is not dict:
            raise ValueError(
                "prior Locality Standing requires exact Measurement occurrences"
            )
        exact_result_occurrences = prior["exact_result_occurrences"]
        representations = prior["representations"]
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
        responsibility_assignment_occurrences = prior[
            "responsibility_assignment_occurrences"
        ]
        if type(responsibility_assignment_occurrences) is not dict:
            raise ValueError(
                "prior Locality Standing requires exact Responsibility assignment occurrences"
            )
        operator_material_acquire_act_occurrences = prior[
            "operator_material_acquire_act_occurrences"
        ]
        if type(operator_material_acquire_act_occurrences) is not dict:
            raise ValueError(
                "prior Locality Standing requires exact operator material acquire Act occurrences"
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

    if replay_started_from_empty:
        _OPERATOR_STANDING_EXACT_ACCUMULATORS.set(
            (
                ledger,
                locality_identity,
                measurement_occurrences,
                ingest_occurrences,
                responsibility_assignment_occurrences,
            )
        )
        _OPERATOR_STANDING_VALIDATION_CONTEXT.set(
            {
                "ledger": ledger,
                "locality_identity": locality_identity,
                "through_event_occurrence_identity": None,
                "measurement_occurrences": measurement_occurrences,
                "ingest_occurrences": ingest_occurrences,
                "responsibility_assignment_occurrences": (
                    responsibility_assignment_occurrences
                ),
            }
        )

    for event in events:
        if event.locality_identity != locality_identity:
            continue
        if replay_started_from_empty:
            _set_operator_standing_validation_context(
                ledger,
                locality_identity=locality_identity,
                through_event_occurrence_identity=(
                    through_event_occurrence_identity
                ),
                measurement_occurrences=measurement_occurrences,
                ingest_occurrences=ingest_occurrences,
                responsibility_assignment_occurrences=(
                    responsibility_assignment_occurrences
                ),
            )
        if not (
            event.kind == MATERIAL_INGEST_OCCURRED_KIND
            or event.kind.startswith("operator.representation.")
            or event.kind in _MEASUREMENT_ACT_EVIDENCE_KINDS
            or event.kind in _MEASUREMENT_RESPONSIBILITY_ASSIGNMENT_KINDS
            or event.kind in _MEASUREMENT_RECORDED_KINDS
            or event.kind in _ASSERTION_LOCALITY_MOVEMENT_KINDS
            or event.kind in _BYTE_PAIR_MEASUREMENT_LIFECYCLE_KINDS
            or event.kind in _STANDING_LOCALITY_CONTINUATION_KINDS
            or event.kind in _STANDING_BOUNDARY_REFERENCE_KINDS
            or event.kind in _RECORDED_STANDING_BOUNDARY_LOCALITY_KINDS
            or event.kind in _OPERATOR_MATERIAL_ACQUIRE_KINDS
            or event.kind in _OPERATOR_SYSTEM_LOCALITY_KINDS
            or event.kind in _REPRESENTATION_CANDIDATE_ADMISSION_KINDS
            or event.kind in _REPRESENTATION_EMISSION_APPLICABILITY_KINDS
            or event.kind in _RECORDED_PAIR_MEASUREMENT_COMPARISON_KINDS
            or event.kind in _SHARED_POSITION_MEASUREMENT_KINDS
            or event.kind in _ADDRESSED_BYTE_REFERENCE_DETERMINATION_KINDS
            or event.kind in _ADDRESSED_MATERIAL_COORDINATE_MEASUREMENT_KINDS
            or event.kind in _COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_KINDS
        ):
            continue
        if event.kind not in _SUPPORTED_KINDS:
            raise ValueError(f"unsupported operator-ingest event: {event.kind}")
        prior_through_event_occurrence_identity = through_event_occurrence_identity
        deferred_lifecycle_event = (
            event.kind in _BYTE_PAIR_MEASUREMENT_LIFECYCLE_KINDS
            or event.kind in _ADDRESSED_MATERIAL_COORDINATE_MEASUREMENT_KINDS
        )
        if not deferred_lifecycle_event:
            event_count += 1
            through_event_occurrence_identity = event.identity
            for key, collected in (
                ("known_loss", known_loss),
                ("unknown", unknown),
                ("conflicts", conflicts),
            ):
                for value in event.material.get(key, ()):
                    _record_distinct(collected, value)
            if _carries_exact_result(ledger, event):
                exact_result_occurrences[event.identity] = None
        if event.kind in _MEASUREMENT_ACT_EVIDENCE_KINDS:
            continue
        pair_prior_standing = {
            "locality_identity": locality_identity,
            "through_event_occurrence_identity": (
                prior_through_event_occurrence_identity
            ),
            "measurement_occurrences": measurement_occurrences,
            "exact_result_occurrences": exact_result_occurrences,
            "responsibility_assignment_occurrences": (
                responsibility_assignment_occurrences
            ),
            "applicability_result_occurrences": (
                applicability_result_occurrences
            ),
        }
        if event.kind in _BYTE_PAIR_MEASUREMENT_LIFECYCLE_KINDS:
            if (
                event.kind
                == BYTE_PAIR_MEASUREMENT_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND
            ):
                _read_pair_measurement_responsibility_assignment(
                    ledger,
                    event.identity,
                    prior_standing=pair_prior_standing,
                )
                responsibility_assignment_occurrences[event.identity] = None
            elif event.kind == BYTE_PAIR_APPLICABILITY_ACT_EVIDENCE_KIND:
                _read_pair_applicability_act_evidence(
                    ledger,
                    event.identity,
                    prior_standing=pair_prior_standing,
                )
            elif event.kind == BYTE_PAIR_APPLICABILITY_RECORDED_KIND:
                _read_recorded_pair_input_applicability(
                    ledger,
                    event.identity,
                    prior_standing=pair_prior_standing,
                )
                applicability_result_occurrences[event.identity] = None
            elif event.kind == BYTE_PAIR_RESPONSIBLE_ACT_EVIDENCE_KIND:
                _read_pair_measurement_act_evidence(
                    ledger,
                    event.identity,
                    prior_standing=pair_prior_standing,
                )
            else:
                _findings_of_recorded_byte_position_pair_measurement(
                    ledger,
                    event.identity,
                    prior_standing=pair_prior_standing,
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
            if _carries_exact_result(ledger, event):
                exact_result_occurrences[event.identity] = None
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
                    "responsibility_assignment_occurrences": (
                        responsibility_assignment_occurrences
                    ),
                },
            )
            responsibility_assignment_occurrences[event.identity] = None
            continue
        if (
            event.kind
            == ASSERTION_LOCALITY_MOVEMENT_RESPONSIBILITY_ASSIGNMENT_KIND
        ):
            _read_assertion_locality_movement_responsibility_assignment(
                ledger,
                event.identity,
                prior_destination_standing={
                    "locality_identity": locality_identity,
                    "through_event_occurrence_identity": (
                        prior_through_event_occurrence_identity
                    ),
                },
            )
            responsibility_assignment_occurrences[event.identity] = None
            continue
        if event.kind == ASSERTION_LOCALITY_MOVEMENT_ACT_EVIDENCE_KIND:
            _read_assertion_locality_movement_act_evidence(
                ledger,
                event.identity,
                prior_destination_standing={
                    "locality_identity": locality_identity,
                    "through_event_occurrence_identity": (
                        prior_through_event_occurrence_identity
                    ),
                    "responsibility_assignment_occurrences": (
                        responsibility_assignment_occurrences
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
                    "responsibility_assignment_occurrences": (
                        responsibility_assignment_occurrences
                    ),
                },
            )
            continue
        if (
            event.kind
            == OCCURRENCE_POSITION_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND
        ):
            get_occurrence_position_measurement_responsibility_assignment(
                ledger, event.identity
            )
            responsibility_assignment_occurrences[event.identity] = None
            continue
        if event.kind == BYTE_PAIR_OCCURRENCE_POSITION_ASSIGNMENT_KIND:
            get_byte_pair_occurrence_position_measurement_responsibility_assignment(
                ledger, event.identity
            )
            responsibility_assignment_occurrences[event.identity] = None
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
                    "ingest_occurrences": ingest_occurrences,
                },
            )
            responsibility_assignment_occurrences[event.identity] = None
            continue
        if (
            event.kind
            == STANDING_BOUNDARY_REFERENCE_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND
        ):
            get_standing_boundary_reference_responsibility_assignment(
                ledger, event.identity
            )
            responsibility_assignment_occurrences[event.identity] = None
            continue
        if event.kind == STANDING_BOUNDARY_REFERENCE_ACT_EVIDENCE_KIND:
            get_standing_boundary_reference_act_evidence(ledger, event.identity)
            continue
        if event.kind == STANDING_BOUNDARY_REFERENCE_RECORDED_KIND:
            get_recorded_standing_boundary_reference(ledger, event.identity)
            recorded_standing_boundary_references[event.identity] = None
            continue
        if (
            event.kind
            == RECORDED_STANDING_BOUNDARY_LOCALITY_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND
        ):
            get_recorded_standing_boundary_locality_responsibility_assignment(
                ledger, event.identity
            )
            responsibility_assignment_occurrences[event.identity] = None
            continue
        if event.kind == RECORDED_STANDING_BOUNDARY_LOCALITY_ACT_EVIDENCE_KIND:
            get_recorded_standing_boundary_locality_act_evidence(
                ledger, event.identity
            )
            continue
        if event.kind == RECORDED_STANDING_BOUNDARY_LOCALITY_RECORDED_KIND:
            get_recorded_standing_boundary_locality(ledger, event.identity)
            recorded_standing_boundary_locality_relations[event.identity] = None
            continue
        if (
            event.kind
            == OPERATOR_MATERIAL_ACQUIRE_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND
        ):
            get_operator_material_acquire_responsibility_assignment(
                ledger, event.identity
            )
            responsibility_assignment_occurrences[event.identity] = None
            continue
        if event.kind == OPERATOR_MATERIAL_ACQUIRE_ACT_EVIDENCE_KIND:
            get_operator_material_acquire_act_evidence(ledger, event.identity)
            operator_material_acquire_act_occurrences[event.identity] = None
            continue
        if event.kind == OPERATOR_MATERIAL_ACQUIRE_RECORDED_KIND:
            get_recorded_operator_material_acquire(ledger, event.identity)
            continue
        if (
            event.kind
            == OPERATOR_SYSTEM_LOCALITY_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND
        ):
            get_operator_system_locality_responsibility_assignment(
                ledger, event.identity
            )
            responsibility_assignment_occurrences[event.identity] = None
            continue
        if event.kind == OPERATOR_SYSTEM_LOCALITY_ACT_EVIDENCE_KIND:
            get_operator_system_locality_act_evidence(ledger, event.identity)
            continue
        if event.kind == OPERATOR_SYSTEM_LOCALITY_RECORDED_KIND:
            get_recorded_operator_system_locality(ledger, event.identity)
            operator_invocation_locality_relations[event.identity] = None
            continue
        if event.kind in {
            REPRESENTATION_CANDIDATE_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND,
            EXACT_MATERIAL_REPRESENTATION_ADMISSION_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND,
        }:
            if (
                event.kind
                == REPRESENTATION_CANDIDATE_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND
            ):
                get_representation_candidate_responsibility_assignment(
                    ledger, event.identity
                )
            else:
                get_exact_material_representation_admission_responsibility_assignment(
                    ledger, event.identity
                )
            responsibility_assignment_occurrences[event.identity] = None
            continue
        if event.kind == REPRESENTATION_CANDIDATE_ACT_EVIDENCE_KIND:
            get_representation_candidate_act_evidence(ledger, event.identity)
            continue
        if event.kind == REPRESENTATION_CANDIDATE_RECORDED_KIND:
            get_recorded_representation_candidate(ledger, event.identity)
            candidate_result_occurrences[event.identity] = None
            continue
        if event.kind == EXACT_MATERIAL_REPRESENTATION_ADMISSION_ACT_EVIDENCE_KIND:
            get_exact_material_representation_admission_act_evidence(
                ledger, event.identity
            )
            continue
        if event.kind == EXACT_MATERIAL_REPRESENTATION_ADMISSION_RECORDED_KIND:
            get_recorded_exact_material_representation_admission(
                ledger, event.identity
            )
            admission_result_occurrences[event.identity] = None
            continue
        if event.kind == REPRESENTATION_EMISSION_APPLICABILITY_ACT_EVIDENCE_KIND:
            get_representation_emission_applicability_act_evidence(
                ledger, event.identity
            )
            continue
        if event.kind == REPRESENTATION_EMISSION_APPLICABILITY_RECORDED_KIND:
            get_recorded_representation_emission_applicability(
                ledger, event.identity
            )
            applicability_result_occurrences[event.identity] = None
            continue
        addressed_byte_reference_prior_standing = {
            "locality_identity": locality_identity,
            "through_event_occurrence_identity": (
                prior_through_event_occurrence_identity
            ),
            "measurement_occurrences": measurement_occurrences,
            "responsibility_assignment_occurrences": (
                responsibility_assignment_occurrences
            ),
            "applicability_result_occurrences": (
                applicability_result_occurrences
            ),
        }
        if event.kind in _ADDRESSED_MATERIAL_COORDINATE_MEASUREMENT_KINDS:
            carried = {
                "scope": scope,
                "locality_identity": locality_identity,
                "through_event_occurrence_identity": (
                    prior_through_event_occurrence_identity
                ),
                "event_count": event_count,
                "ingest_occurrences": ingest_occurrences,
                "measurement_occurrences": measurement_occurrences,
                "exact_result_occurrences": exact_result_occurrences,
                "representations": representations,
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
                "responsibility_assignment_occurrences": (
                    responsibility_assignment_occurrences
                ),
                "operator_material_acquire_act_occurrences": (
                    operator_material_acquire_act_occurrences
                ),
                "candidate_result_occurrences": candidate_result_occurrences,
                "admission_result_occurrences": admission_result_occurrences,
                "applicability_result_occurrences": (
                    applicability_result_occurrences
                ),
                "comparison_result_occurrences": comparison_result_occurrences,
                "known_loss": known_loss,
                "unknown": unknown,
                "conflicts": conflicts,
            }
            _carry_addressed_material_coordinate_measurement_occurrence_into_standing(
                ledger,
                carried,
                event,
                prior_through_event_occurrence_identity=(
                    prior_through_event_occurrence_identity
                ),
            )
            through_event_occurrence_identity = carried[
                "through_event_occurrence_identity"
            ]
            event_count = carried["event_count"]
            continue
        if event.kind == ADDRESSED_BYTE_REFERENCE_RESPONSIBILITY_ASSIGNMENT_KIND:
            _read_addressed_byte_reference_assignment(
                ledger,
                event.identity,
                prior_standing=addressed_byte_reference_prior_standing,
            )
            responsibility_assignment_occurrences[event.identity] = None
            continue
        if event.kind == ADDRESSED_BYTE_REFERENCE_APPLICABILITY_ACT_EVIDENCE_KIND:
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
        if event.kind == ADDRESSED_BYTE_REFERENCE_DETERMINATION_ACT_EVIDENCE_KIND:
            _read_addressed_byte_reference_determination_act(
                ledger,
                event.identity,
                prior_standing=addressed_byte_reference_prior_standing,
            )
            continue
        if event.kind == SHARED_POSITION_RESPONSIBILITY_ASSIGNMENT_KIND:
            _shared_position_assignment_reading(
                ledger,
                event,
                prior_standing=addressed_byte_reference_prior_standing,
            )
            responsibility_assignment_occurrences[event.identity] = None
            continue
        if event.kind == SHARED_POSITION_APPLICABILITY_ACT_EVIDENCE_KIND:
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
            continue
        if event.kind == SHARED_POSITION_APPLICABILITY_RESULT_KIND:
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
            applicability_result_occurrences[event.identity] = None
            continue
        if event.kind == SHARED_POSITION_MEASUREMENT_ACT_EVIDENCE_KIND:
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
            responsibility_assignment_occurrences[event.identity] = None
            continue
        if (
            event.kind
            == RECORDED_PAIR_MEASUREMENT_COMPARISON_APPLICABILITY_ACT_EVIDENCE_KIND
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
        if event.kind == RECORDED_PAIR_MEASUREMENT_COMPARISON_ACT_EVIDENCE_KIND:
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
            responsibility_assignment_occurrences[event.identity] = None
            continue
        if event.kind == COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_APPLICABILITY_ACT_EVIDENCE_KIND:
            get_comparison_of_ordered_relation_path_with_recorded_pair_findings_applicability_act_evidence(
                ledger, event.identity
            )
            continue
        if event.kind == COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_APPLICABILITY_RESULT_KIND:
            get_recorded_comparison_of_ordered_relation_path_with_recorded_pair_findings_applicability(
                ledger, event.identity
            )
            applicability_result_occurrences[event.identity] = None
            continue
        if event.kind == COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_COMPARE_ACT_EVIDENCE_KIND:
            get_comparison_of_ordered_relation_path_with_recorded_pair_findings_act_evidence(
                ledger, event.identity
            )
            continue
        if event.kind == COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_RESULT_KIND:
            get_recorded_comparison_of_ordered_relation_path_with_recorded_pair_findings(
                ledger, event.identity
            )
            comparison_result_occurrences[event.identity] = None
            continue
        if (
            event.kind
            == STANDING_LOCALITY_CONTINUATION_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND
        ):
            get_standing_locality_continuation_responsibility_assignment(
                ledger, event.identity
            )
            responsibility_assignment_occurrences[event.identity] = None
            continue
        if event.kind == STANDING_LOCALITY_CONTINUATION_ACT_EVIDENCE_KIND:
            continue
        if event.kind == STANDING_LOCALITY_CONTINUATION_RECORDED_KIND:
            get_recorded_standing_locality_continuation(ledger, event.identity)
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
                    "ingest_occurrences": ingest_occurrences,
                    "responsibility_assignment_occurrences": (
                        responsibility_assignment_occurrences
                    ),
                },
            )
            measurement_occurrences[event.identity] = (
                _measurement_occurrence_coordinates(event)
            )
            continue
        if event.kind == SHARED_POSITION_MEASUREMENT_RESULT_KIND:
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
                    "responsibility_assignment_occurrences": (
                        responsibility_assignment_occurrences
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
        if event.kind in {
            _REPRESENTATION_ACT_EVIDENCE_KIND,
            _REPRESENTATION_LOCALITY_EVIDENCE_KIND,
        }:
            continue
        if event.kind == _REPRESENTATION_RECORDED_KIND:
            material = event.material
            if material["result_identity"] in representations:
                raise ValueError(
                    "duplicate Representation identity: "
                    f"{material['result_identity']}"
                )
            representations[material["result_identity"]] = {
                "representation_identity": material["result_identity"],
                "representation_event_identity": event.identity,
                "source_occurrence_reference": material[
                    "source_occurrence_reference"
                ],
                "emission_attempt_event_identity": None,
                "emission_attempt_locality_evidence_identity": None,
                "boundary_failure_event_identity": None,
                "emitted_event_identity": None,
                "representation_result": material["representation_result"],
                "locality_standing_through_event_occurrence_identity": material[
                    "locality_standing_through_event_occurrence_identity"
                ],
                "scope": material["dimensions"]["scope_locality"],
                "provenance": material["dimensions"]["source_provenance"],
                "known_loss": material["known_loss"],
                "unknown": material["unknown"],
                "conflicts": material["conflicts"],
            }
            continue
        if event.kind in {
            _REPRESENTATION_EMISSION_ACT_EVIDENCE_KIND,
            _REPRESENTATION_BOUNDARY_FAILURE_ACT_EVIDENCE_KIND,
            _REPRESENTATION_EMISSION_LOCALITY_EVIDENCE_KIND,
        }:
            # These Events preserve exact relation Evidence. They do not add or
            # revise Locality Standing by identity.
            continue
        if event.kind == _REPRESENTATION_EMISSION_ATTEMPT_KIND:
            representation_reference = event.material["representation_reference"]
            if representation_reference not in representations:
                raise ValueError(
                    "representation emission attempt without recorded representation event: "
                    f"{representation_reference}"
                )
            representations[representation_reference]["emission_attempt_event_identity"] = event.identity
            continue
        if event.kind == _REPRESENTATION_EMISSION_ATTEMPT_LOCALITY_EVIDENCE_KIND:
            representation_reference = event.material["representation_reference"]
            if representation_reference not in representations:
                raise ValueError(
                    "emission-attempt Locality Evidence without recorded Representation: "
                    f"{representation_reference}"
                )
            if event.material["attempt_event_identity"] != representations[
                representation_reference
            ]["emission_attempt_event_identity"]:
                raise ValueError(
                    "emission-attempt Locality Evidence names another attempt"
                )
            representations[representation_reference][
                "emission_attempt_locality_evidence_identity"
            ] = event.identity
            continue
        if event.kind == _REPRESENTATION_EMITTED_KIND:
            representation_reference = event.material["representation_reference"]
            if representation_reference not in representations:
                raise ValueError(
                    "representation emission without recorded representation event: "
                    f"{representation_reference}"
                )
            if (
                event.material["representation_event_identity"]
                != representations[representation_reference]["representation_event_identity"]
            ):
                raise ValueError(
                    "representation emission does not name its recorded "
                    "representation Act occurrence"
                )
            if (
                event.material["attempt_reference"]
                != representations[representation_reference]["emission_attempt_event_identity"]
            ):
                raise ValueError(
                    "representation emission does not name its recorded attempt"
                )
            representations[representation_reference]["emitted_event_identity"] = event.identity
            continue
        if event.kind == _REPRESENTATION_BOUNDARY_FAILURE_KIND:
            representation_reference = event.material["representation_reference"]
            if representation_reference not in representations:
                raise ValueError(
                    "representation boundary failure without recorded representation event: "
                    f"{representation_reference}"
                )
            if (
                event.material["attempt_reference"]
                != representations[representation_reference]["emission_attempt_event_identity"]
            ):
                raise ValueError(
                    "representation boundary failure does not name its recorded attempt"
                )
            emitted_event_identity = event.material["emitted_event_identity"]
            if emitted_event_identity is not None and emitted_event_identity != representations[
                representation_reference
            ]["emitted_event_identity"]:
                raise ValueError(
                    "representation boundary failure does not name its accepted emission"
                )
            representations[representation_reference]["boundary_failure_event_identity"] = event.identity
            continue
        ingest_reference = event.material["dimensions"]["identity"]
        occurrence = {
            "subject_reference": ingest_reference,
            "standing": "preserved",
            "authority": event.material["dimensions"]["authority"],
            "evidence_event_identity": event.identity,
            "source_role": event.material["source_role"],
        }
        if isinstance(event.material.get("represented_material"), str):
            occurrence["represented_material"] = event.material[
                "represented_material"
            ]
        ingest_occurrences.append(occurrence)

    return {
        "locality_identity": locality_identity,
        "through_event_occurrence_identity": through_event_occurrence_identity,
        "event_count": event_count,
        "ingest_occurrences": ingest_occurrences,
        "measurement_occurrences": measurement_occurrences,
        "exact_result_occurrences": exact_result_occurrences,
        "representations": representations,
        # No Representation is designated current.  `representations` retains
        # Representation Act and emission occurrences in append order; naming
        # one of them current would assert present relevance that no occurrence
        # establishes.
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
        "responsibility_assignment_occurrences": (
            responsibility_assignment_occurrences
        ),
        "operator_material_acquire_act_occurrences": (
            operator_material_acquire_act_occurrences
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
        ledger, event.identity, prior_standing=locality_standing
    )
    assignments = locality_standing.get("responsibility_assignment_occurrences")
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


def _carry_validated_byte_measurement_occurrence_into_standing(
    ledger: EventLedger,
    locality_standing: dict[str, Any],
    event,
    *,
    prior_through_event_occurrence_identity: str,
    destination_coordinate: str | None,
) -> dict[str, Any]:
    """Carry one exact-byte lifecycle occurrence validated in this call."""

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
        raise ValueError("byte Measurement lifecycle Standing is not exact")
    try:
        ledger.occurrences_in_append_order(
            (prior_through_event_occurrence_identity, event.identity),
            locality_identity=event.locality_identity,
        )
    except ValueError as error:
        raise ValueError(
            "byte Measurement lifecycle Standing order is not exact"
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
        raise ValueError("byte Measurement lifecycle Standing is not exact")
    standing_additions = _exact_standing_additions(
        locality_standing,
        event,
        error_message="byte Measurement lifecycle Standing is not exact",
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


def _carry_byte_measurement_assignment_from_measured_inputs_into_standing(
    ledger: EventLedger,
    locality_standing: dict[str, Any],
    assignment,
    measured: MeasuredByteInputs,
    *,
    expected_material: dict[str, Any],
    retained_assignment,
    retained_measured,
    prior_through_event_occurrence_identity: str,
) -> dict[str, Any]:
    _require_exact_byte_measurement_assignment_from_measured_inputs(
        ledger,
        assignment,
        measured,
        expected_material,
        retained_assignment,
        retained_measured,
    )
    if (
        assignment.material.get("standing_boundary_identity")
        != prior_through_event_occurrence_identity
    ):
        raise ValueError("byte Measurement assignment Standing is not exact")
    return _carry_validated_byte_measurement_occurrence_into_standing(
        ledger,
        locality_standing,
        assignment,
        prior_through_event_occurrence_identity=(
            prior_through_event_occurrence_identity
        ),
        destination_coordinate="responsibility_assignment_occurrences",
    )


def _carry_byte_measurement_act_from_measured_inputs_into_standing(
    ledger: EventLedger,
    locality_standing: dict[str, Any],
    act,
    *,
    assignment,
    measured: MeasuredByteInputs,
    assignment_material: dict[str, Any],
    expected_material: dict[str, Any],
    retained_assignment,
    retained_act,
    retained_measured,
    prior_through_event_occurrence_identity: str,
) -> dict[str, Any]:
    _require_exact_byte_measurement_act_from_measured_inputs(
        ledger,
        act,
        assignment,
        measured,
        assignment_material,
        expected_material,
        retained_assignment,
        retained_act,
        retained_measured,
    )
    if prior_through_event_occurrence_identity != assignment.identity:
        raise ValueError("byte Measurement Act Standing is not exact")
    return _carry_validated_byte_measurement_occurrence_into_standing(
        ledger,
        locality_standing,
        act,
        prior_through_event_occurrence_identity=(
            prior_through_event_occurrence_identity
        ),
        destination_coordinate=None,
    )


def _carry_byte_measurement_result_from_measured_inputs_into_standing(
    ledger: EventLedger,
    locality_standing: dict[str, Any],
    result,
    *,
    evidence,
    act,
    assignment,
    measured: MeasuredByteInputs,
    assignment_material: dict[str, Any],
    act_material: dict[str, Any],
    result_material: dict[str, Any],
    expected_material: dict[str, Any],
    retained_assignment,
    retained_act,
    retained_result,
    retained_measured,
    prior_through_event_occurrence_identity: str,
) -> tuple[dict[str, Any], tuple[RecordedByteAssertion, ...]]:
    assertions = _require_exact_byte_measurement_result_from_measured_inputs(
        ledger,
        result,
        evidence=evidence,
        act=act,
        assignment=assignment,
        measured=measured,
        assignment_material=assignment_material,
        act_material=act_material,
        result_material=result_material,
        expected_material=expected_material,
        retained_assignment=retained_assignment,
        retained_act=retained_act,
        retained_result=retained_result,
        retained_measured=retained_measured,
    )
    if prior_through_event_occurrence_identity != act.identity:
        raise ValueError("byte Measurement result Standing is not exact")
    standing = _carry_validated_byte_measurement_occurrence_into_standing(
        ledger,
        locality_standing,
        result,
        prior_through_event_occurrence_identity=(
            prior_through_event_occurrence_identity
        ),
        destination_coordinate="measurement_occurrences",
    )
    return standing, assertions


def _carry_assertion_locality_movement_assignment_into_standing(
    ledger: EventLedger,
    locality_standing: dict[str, Any],
    event,
    *,
    source: RecordedByteAssertion,
    source_event,
    source_standing: dict[str, Any],
) -> dict[str, Any]:
    """Carry one movement assignment produced from exact same-call inputs."""

    assignments = (
        locality_standing.get("responsibility_assignment_occurrences")
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
            "assignment_identity",
            "assignment_subject_identity",
            "movement_act_identity",
            "movement_act_occurrence_identity",
            "movement_result_identity",
        )
    }
    expected = None
    if (
        type(source) is RecordedByteAssertion
        and source_event is not None
        and type(source_boundary) is str
        and source_boundary
        and all(
            type(identity) is str and identity for identity in identities.values()
        )
        and len(set(identities.values())) == len(identities)
    ):
        expected = _movement_assignment_material(
            source=source,
            source_locality=source_event.locality_identity,
            destination_locality=event.locality_identity,
            source_standing_boundary_identity=source_boundary,
            destination_standing_boundary_identity=(
                locality_standing.get("through_event_occurrence_identity")
                if type(locality_standing) is dict
                else None
            ),
            **identities,
        )
    if (
        type(locality_standing) is not dict
        or event.kind
        != ASSERTION_LOCALITY_MOVEMENT_RESPONSIBILITY_ASSIGNMENT_KIND
        or ledger.get(event.identity) != event
        or ledger.integrity_of(event.identity) == CORRUPTED
        or type(source) is not RecordedByteAssertion
        or source_event is None
        or type(source_standing) is not dict
        or ledger.get(source_event.identity) != source_event
        or ledger.integrity_of(source_event.identity) == CORRUPTED
        or source.recorded_occurrence_identity != source_event.identity
        or source_event.locality_identity != event.material.get("source_locality")
        or source_standing.get("locality_identity")
        != source_event.locality_identity
        or source_standing.get("measurement_occurrences", {}).get(
            source_event.identity
        )
        != _source_measurement_standing_coordinates(source_event)
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
        locality_standing.get("responsibility_assignment_occurrences")
        if type(locality_standing) is dict
        else None
    )
    event_count = (
        locality_standing.get("event_count")
        if type(locality_standing) is dict
        else None
    )
    try:
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
        != ASSERTION_LOCALITY_MOVEMENT_RESPONSIBILITY_ASSIGNMENT_KIND
        or ledger.get(responsibility_assignment.identity)
        != responsibility_assignment
        or ledger.integrity_of(responsibility_assignment.identity) == CORRUPTED
        or event.kind != ASSERTION_LOCALITY_MOVEMENT_ACT_EVIDENCE_KIND
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
    responsible_act_evidence,
    responsibility_assignment,
    source: RecordedByteAssertion,
) -> tuple[dict[str, Any], RecordedByteAssertion]:
    """Carry one exact movement result and its already-carried source."""

    assignments = (
        locality_standing.get("responsibility_assignment_occurrences")
        if type(locality_standing) is dict
        else None
    )
    event_count = (
        locality_standing.get("event_count")
        if type(locality_standing) is dict
        else None
    )
    evidence_identity = event.material.get("evidence_of_yield_relation_identity")
    evidence = ledger.get(evidence_identity) if type(evidence_identity) is str else None
    try:
        expected_act = _movement_act_material(responsibility_assignment)
        expected = {
            **_movement_result_material(responsibility_assignment),
            "responsible_act_evidence_identity": responsible_act_evidence.identity,
            "evidence_of_yield_relation_identity": evidence_identity,
        }
        requirements = read_requirements_of_yield_relation(
            ledger,
            recorded_result_event_identity=event.identity,
            evidence_of_yield_relation_event_identity=evidence_identity,
            responsible_act_evidence_event_identity=responsible_act_evidence.identity,
            recorded_result_occurrence_coordinate="movement_act_occurrence_identity",
            responsible_act_occurrence_coordinate="movement_act_occurrence_identity",
        )
        ledger.occurrences_in_append_order(
            (
                responsible_act_evidence.identity,
                evidence_identity,
                event.identity,
            ),
            locality_identity=event.locality_identity,
        )
    except (AttributeError, KeyError, TypeError, ValueError) as error:
        raise ValueError("Assertion movement result Standing is not exact") from error
    if (
        type(locality_standing) is not dict
        or type(source) is not RecordedByteAssertion
        or responsibility_assignment.kind
        != ASSERTION_LOCALITY_MOVEMENT_RESPONSIBILITY_ASSIGNMENT_KIND
        or ledger.get(responsibility_assignment.identity)
        != responsibility_assignment
        or ledger.integrity_of(responsibility_assignment.identity) == CORRUPTED
        or responsible_act_evidence.kind
        != ASSERTION_LOCALITY_MOVEMENT_ACT_EVIDENCE_KIND
        or ledger.get(responsible_act_evidence.identity) != responsible_act_evidence
        or ledger.integrity_of(responsible_act_evidence.identity) == CORRUPTED
        or responsible_act_evidence.material != expected_act
        or event.kind != ASSERTION_LOCALITY_MOVEMENT_KIND
        or ledger.get(event.identity) != event
        or ledger.integrity_of(event.identity) == CORRUPTED
        or event.locality_identity != responsibility_assignment.locality_identity
        or event.material != expected
        or responsibility_assignment.material.get("source_assertion_reference")
        != source.reference
        or event.material.get("source_assertion_reference") != source.reference
        or evidence is None
        or evidence.kind != RECORDED_EVIDENCE_OF_YIELD_RELATION_KIND
        or evidence.locality_identity != event.locality_identity
        or ledger.integrity_of(evidence.identity) == CORRUPTED
        or evidence.material.get("result_kind")
        != ASSERTION_LOCALITY_MOVEMENT_RESULT_KIND
        or evidence.material.get("occurrence_boundary")
        != "assertion_locality_movement"
        or not all(requirements.values())
        or locality_standing.get("locality_identity") != event.locality_identity
        or locality_standing.get("through_event_occurrence_identity")
        != responsible_act_evidence.identity
        or type(assignments) is not dict
        or assignments.get(responsibility_assignment.identity, object()) is not None
        or type(event_count) is not int
        or event_count < 0
        or ledger.append_boundary_through_occurrence(event.identity)
        != ledger.append_boundary()
    ):
        raise ValueError("Assertion movement result Standing is not exact")
    exact = _moved_byte_assertion_from_carried_source(
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
    assignments = locality_standing.get("responsibility_assignment_occurrences")
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
    responsible_act_evidence,
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
        locality_standing.get("responsibility_assignment_occurrences")
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
        "responsible_act_evidence_identity": responsible_act_evidence.identity,
        "evidence_of_yield_relation_identity": event.material.get(
            "evidence_of_yield_relation_identity"
        ),
    }
    evidence_identity = event.material.get("evidence_of_yield_relation_identity")
    evidence = ledger.get(evidence_identity) if type(evidence_identity) is str else None
    try:
        requirements = read_requirements_of_yield_relation(
            ledger,
            recorded_result_event_identity=event.identity,
            evidence_of_yield_relation_event_identity=evidence_identity,
            responsible_act_evidence_event_identity=responsible_act_evidence.identity,
        )
    except (TypeError, ValueError):
        requirements = {}
    if (
        event.kind != OCCURRENCE_POSITION_RECORDED_KIND
        or event.locality_identity != responsibility_assignment.locality_identity
        or event.material != expected
        or locality_standing.get("locality_identity") != event.locality_identity
        or locality_standing.get("through_event_occurrence_identity")
        != responsible_act_evidence.identity
        or type(measurements) is not dict
        or event.identity in measurements
        or type(assignments) is not dict
        or responsibility_assignment.identity not in assignments
        or evidence is None
        or evidence.kind != RECORDED_EVIDENCE_OF_YIELD_RELATION_KIND
        or evidence.material.get("occurrence_boundary")
        != "occurrence_position_measurement"
        or evidence.material.get("result_kind") != OCCURRENCE_POSITION_RESULT_KIND
        or ledger.integrity_of(evidence.identity) == CORRUPTED
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


def _carry_pair_measurement_assignment_into_standing(
    ledger: EventLedger,
    locality_standing: dict[str, Any],
    assignment,
    source,
    *,
    prior_through_event_occurrence_identity: str,
) -> dict[str, Any]:
    _require_exact_pair_measurement_assignment_event(ledger, assignment, source)
    return _carry_validated_pair_measurement_lifecycle_occurrence_into_standing(
        ledger,
        locality_standing,
        assignment,
        prior_through_event_occurrence_identity=prior_through_event_occurrence_identity,
        destination_coordinate="responsibility_assignment_occurrences",
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
    applicability_act_evidence,
    prior_through_event_occurrence_identity: str,
) -> dict[str, Any]:
    _require_exact_pair_applicability_result_event(
        ledger,
        event,
        assignment=assignment,
        source=source,
        applicability_act_evidence=applicability_act_evidence,
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
    applicability_act_evidence,
    prior_through_event_occurrence_identity: str,
) -> dict[str, Any]:
    _require_exact_pair_measurement_act_event(
        ledger,
        event,
        assignment=assignment,
        source=source,
        applicability_event=applicability_event,
        applicability_act_evidence=applicability_act_evidence,
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
    responsible_act_evidence,
    assignment,
    source,
    applicability_event,
    applicability_act_evidence,
    prior_through_event_occurrence_identity: str,
) -> dict[str, Any]:
    _require_exact_pair_measurement_result_event(
        ledger,
        event,
        responsible_act_evidence=responsible_act_evidence,
        assignment=assignment,
        source=source,
        applicability_event=applicability_event,
        applicability_act_evidence=applicability_act_evidence,
    )
    return _carry_validated_pair_measurement_lifecycle_occurrence_into_standing(
        ledger,
        locality_standing,
        event,
        prior_through_event_occurrence_identity=prior_through_event_occurrence_identity,
        destination_coordinate="measurement_occurrences",
    )


def _carry_pair_measurement_result_from_measured_inputs_into_standing(
    ledger: EventLedger,
    locality_standing: dict[str, Any],
    event,
    *,
    evidence,
    responsible_act_evidence,
    assignment,
    source,
    applicability_event,
    applicability_act_evidence,
    measured: MeasuredBytePairInputs,
    expected_material: dict[str, Any],
    stage_materials: dict[str, dict[str, Any]],
    retained_result,
    retained_measured,
    prior_through_event_occurrence_identity: str,
) -> dict[str, Any]:
    _require_exact_pair_measurement_result_from_measured_inputs(
        ledger,
        event,
        evidence=evidence,
        responsible_act_evidence=responsible_act_evidence,
        assignment=assignment,
        source=source,
        applicability_event=applicability_event,
        applicability_act_evidence=applicability_act_evidence,
        measured=measured,
        expected_material=expected_material,
        stage_materials=stage_materials,
        retained_result=retained_result,
        retained_measured=retained_measured,
    )
    return _carry_validated_pair_measurement_lifecycle_occurrence_into_standing(
        ledger,
        locality_standing,
        event,
        prior_through_event_occurrence_identity=(
            prior_through_event_occurrence_identity
        ),
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
    assignments = locality_standing.get("responsibility_assignment_occurrences")
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
    assignments = locality_standing.get("responsibility_assignment_occurrences")
    ingests = locality_standing.get("ingest_occurrences")
    assignment = event.material.get("responsibility_assignment_reference")
    source_identity = event.material.get("source_ingest_occurrence_identity")
    event_count = locality_standing.get("event_count")
    if (
        type(measurements) is not dict
        or type(assignments) is not dict
        or type(ingests) is not list
        or type(assignment) is not dict
        or assignment.get("recorded_occurrence_identity") not in assignments
        or event.material.get("responsible_act_evidence_identity")
        != prior_through_event_occurrence_identity
        or not any(
            type(occurrence) is dict
            and occurrence.get("evidence_event_identity") == source_identity
            for occurrence in ingests
        )
        or type(event.material.get("evidence_of_yield_relation_identity"))
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


def _carry_operator_material_acquisition_occurrence_into_standing(
    locality_standing: dict[str, Any],
    event,
    *,
    prior_through_event_occurrence_identity: str,
) -> dict[str, Any]:
    """Carry one acquisition occurrence produced by this console call."""

    if (
        type(locality_standing) is not dict
        or event.kind not in _OPERATOR_MATERIAL_ACQUIRE_KINDS
        or locality_standing.get("locality_identity") != event.locality_identity
        or locality_standing.get("through_event_occurrence_identity")
        != prior_through_event_occurrence_identity
    ):
        raise ValueError("operator material acquisition Standing is not exact")
    assignments = locality_standing.get("responsibility_assignment_occurrences")
    acts = locality_standing.get("operator_material_acquire_act_occurrences")
    exact_results = locality_standing.get("exact_result_occurrences")
    event_count = locality_standing.get("event_count")
    if (
        type(assignments) is not dict
        or type(acts) is not dict
        or type(exact_results) is not dict
        or type(event_count) is not int
        or event_count < 0
    ):
        raise ValueError("operator material acquisition Standing is not exact")
    if event.kind == OPERATOR_MATERIAL_ACQUIRE_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND:
        source = event.material.get("source_standing_reference")
        representations = locality_standing.get("representations")
        if (
            type(source) is not dict
            or type(representations) is not dict
            or source.get("locality_standing_through_event_occurrence_identity")
            != prior_through_event_occurrence_identity
            or not any(
                reference.get("representation_event_identity")
                == source.get("addressed_representation_event_identity")
                for reference in representations.values()
                if type(reference) is dict
            )
            or event.identity in assignments
        ):
            raise ValueError("operator material acquisition assignment is not exact")
    elif event.kind == OPERATOR_MATERIAL_ACQUIRE_ACT_EVIDENCE_KIND:
        assignment = event.material.get("responsibility_assignment_reference")
        if (
            type(assignment) is not dict
            or assignment.get("recorded_occurrence_identity")
            != prior_through_event_occurrence_identity
            or prior_through_event_occurrence_identity not in assignments
            or event.identity in acts
        ):
            raise ValueError("operator material acquisition Act is not exact")
    else:
        if (
            event.material.get("responsible_act_evidence_identity")
            != prior_through_event_occurrence_identity
            or prior_through_event_occurrence_identity not in acts
            or type(event.material.get("evidence_of_yield_relation_identity"))
            is not str
            or type(event.exact_material) is not bytes
            or event.identity in exact_results
        ):
            raise ValueError("operator material acquisition result is not exact")
    standing_additions = _exact_standing_additions(
        locality_standing,
        event,
        error_message="operator material acquisition Standing is not exact",
    )
    if event.kind == OPERATOR_MATERIAL_ACQUIRE_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND:
        assignments[event.identity] = None
    elif event.kind == OPERATOR_MATERIAL_ACQUIRE_ACT_EVIDENCE_KIND:
        acts[event.identity] = None
    else:
        exact_results[event.identity] = None
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
    assignments = locality_standing.get("responsibility_assignment_occurrences")
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
    elif event.kind == RECORDED_PAIR_MEASUREMENT_COMPARISON_APPLICABILITY_ACT_EVIDENCE_KIND:
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
            or event.material.get("responsible_act_evidence_identity")
            != prior_through_event_occurrence_identity
            or event.material.get("standing") != "applicable"
            or event.identity in applicability
        ):
            raise ValueError("recorded pair comparison Applicability is not exact")
    elif event.kind == RECORDED_PAIR_MEASUREMENT_COMPARISON_ACT_EVIDENCE_KIND:
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
            or event.material.get("responsible_act_evidence_identity")
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


def _carry_addressed_material_coordinate_measurement_occurrence_into_standing(
    ledger: EventLedger,
    locality_standing: dict[str, Any],
    event,
    *,
    prior_through_event_occurrence_identity: str,
) -> dict[str, Any]:
    """Validate, then carry one addressed-material Measurement occurrence."""

    if (
        type(locality_standing) is not dict
        or event.kind not in _ADDRESSED_MATERIAL_COORDINATE_MEASUREMENT_KINDS
        or ledger.get(event.identity) != event
        or ledger.integrity_of(event.identity) == CORRUPTED
        or event.locality_identity != locality_standing.get("locality_identity")
        or locality_standing.get("through_event_occurrence_identity")
        != prior_through_event_occurrence_identity
        or event.identity == prior_through_event_occurrence_identity
    ):
        raise ValueError("addressed-material Measurement Standing is not exact")
    assignments = locality_standing.get("responsibility_assignment_occurrences")
    applicability = locality_standing.get("applicability_result_occurrences")
    measurements = locality_standing.get("measurement_occurrences")
    event_count = locality_standing.get("event_count")
    if (
        type(assignments) is not dict
        or type(applicability) is not dict
        or type(measurements) is not dict
        or type(event_count) is not int
        or event_count < 0
    ):
        raise ValueError("addressed-material Measurement Standing is not exact")
    if event.kind == ADDRESSED_MATERIAL_COORDINATE_RESPONSIBILITY_ASSIGNMENT_KIND:
        _read_addressed_material_coordinate_assignment(
            ledger, event.identity, prior_standing=locality_standing
        )
        if (
            event.material.get("standing_boundary_identity")
            != prior_through_event_occurrence_identity
            or event.identity in assignments
        ):
            raise ValueError("addressed-material assignment Standing is not exact")
    elif event.kind == ADDRESSED_MATERIAL_COORDINATE_APPLICABILITY_ACT_EVIDENCE_KIND:
        _read_addressed_material_coordinate_applicability_act(
            ledger, event.identity, prior_standing=locality_standing
        )
        assignment = event.material.get("responsibility_assignment_reference")
        if (
            type(assignment) is not dict
            or assignment.get("recorded_occurrence_identity")
            != prior_through_event_occurrence_identity
            or prior_through_event_occurrence_identity not in assignments
        ):
            raise ValueError("addressed-material Applicability Act Standing is not exact")
    elif event.kind == ADDRESSED_MATERIAL_COORDINATE_APPLICABILITY_RESULT_KIND:
        _read_addressed_material_coordinate_applicability_result(
            ledger, event.identity, prior_standing=locality_standing
        )
        assignment = event.material.get("responsibility_assignment_reference")
        if (
            type(assignment) is not dict
            or assignment.get("recorded_occurrence_identity") not in assignments
            or event.material.get("responsible_act_evidence_identity")
            != prior_through_event_occurrence_identity
            or event.identity in applicability
        ):
            raise ValueError("addressed-material Applicability Standing is not exact")
    elif event.kind == ADDRESSED_MATERIAL_COORDINATE_MEASUREMENT_ACT_EVIDENCE_KIND:
        _read_addressed_material_coordinate_measurement_act(
            ledger, event.identity, prior_standing=locality_standing
        )
        assignment = event.material.get("responsibility_assignment_reference")
        applicability_reference = event.material.get("applicability_result_reference")
        if (
            type(assignment) is not dict
            or assignment.get("recorded_occurrence_identity") not in assignments
            or type(applicability_reference) is not dict
            or applicability_reference.get("recorded_occurrence_identity")
            != prior_through_event_occurrence_identity
            or prior_through_event_occurrence_identity not in applicability
        ):
            raise ValueError("addressed-material Measurement Act Standing is not exact")
    else:
        _read_addressed_material_coordinate_measurement_result(
            ledger, event.identity, prior_standing=locality_standing
        )
        assignment = event.material.get("responsibility_assignment_reference")
        applicability_reference = event.material.get("applicability_result_reference")
        if (
            type(assignment) is not dict
            or assignment.get("recorded_occurrence_identity") not in assignments
            or type(applicability_reference) is not dict
            or applicability_reference.get("recorded_occurrence_identity")
            not in applicability
            or event.material.get("responsible_act_evidence_identity")
            != prior_through_event_occurrence_identity
            or event.identity in measurements
        ):
            raise ValueError("addressed-material Measurement result Standing is not exact")
    standing_additions = _exact_standing_additions(
        locality_standing,
        event,
        error_message="addressed-material Measurement Standing is not exact",
    )
    if event.kind == ADDRESSED_MATERIAL_COORDINATE_RESPONSIBILITY_ASSIGNMENT_KIND:
        assignments[event.identity] = None
    elif event.kind == ADDRESSED_MATERIAL_COORDINATE_APPLICABILITY_RESULT_KIND:
        applicability[event.identity] = None
    elif event.kind == ADDRESSED_MATERIAL_COORDINATE_MEASUREMENT_RESULT_KIND:
        measurements[event.identity] = (
            _addressed_material_coordinate_measurement_coordinates(event)
        )
    for key, added in standing_additions.items():
        for value in added:
            _record_distinct(locality_standing[key], value)
    locality_standing["through_event_occurrence_identity"] = event.identity
    locality_standing["event_count"] = event_count + 1
    return locality_standing


def _carry_ordered_relation_path_pair_findings_comparison_occurrence_into_standing(
    locality_standing: dict[str, Any],
    event,
    *,
    prior_through_event_occurrence_identity: str,
) -> dict[str, Any]:
    """Carry one exact 04.Compare.B occurrence produced in this call."""

    if (
        type(locality_standing) is not dict
        or event.kind
        not in _COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_KINDS
        or locality_standing.get("locality_identity") != event.locality_identity
        or locality_standing.get("through_event_occurrence_identity")
        != prior_through_event_occurrence_identity
    ):
        raise ValueError("ordered relation-path comparison Standing is not exact")
    assignments = locality_standing.get("responsibility_assignment_occurrences")
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
        raise ValueError("ordered relation-path comparison Standing is not exact")
    if (
        event.kind
        == COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_RESPONSIBILITY_ASSIGNMENT_KIND
    ):
        measurements = locality_standing.get("measurement_occurrences")
        path = event.material.get("path_result_reference")
        comparison = event.material.get("comparison_result_reference")
        if (
            type(measurements) is not dict
            or type(path) is not dict
            or type(comparison) is not dict
            or path.get("recorded_occurrence_identity") not in measurements
            or comparison.get("recorded_occurrence_identity") not in comparisons
            or event.material.get("standing_boundary_identity")
            != prior_through_event_occurrence_identity
            or event.identity in assignments
        ):
            raise ValueError("ordered relation-path comparison assignment is not exact")
    elif (
        event.kind
        == COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_APPLICABILITY_ACT_EVIDENCE_KIND
    ):
        assignment = event.material.get("responsibility_assignment_reference")
        if (
            type(assignment) is not dict
            or assignment.get("recorded_occurrence_identity")
            != prior_through_event_occurrence_identity
            or prior_through_event_occurrence_identity not in assignments
        ):
            raise ValueError("ordered relation-path Applicability Act is not exact")
    elif (
        event.kind
        == COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_APPLICABILITY_RESULT_KIND
    ):
        assignment = event.material.get("responsibility_assignment_reference")
        if (
            type(assignment) is not dict
            or assignment.get("recorded_occurrence_identity") not in assignments
            or event.material.get("responsible_act_evidence_identity")
            != prior_through_event_occurrence_identity
            or event.material.get("applicability") != "applicable"
            or event.identity in applicability
        ):
            raise ValueError("ordered relation-path Applicability is not exact")
    elif (
        event.kind
        == COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_COMPARE_ACT_EVIDENCE_KIND
    ):
        assignment = event.material.get("responsibility_assignment_reference")
        if (
            type(assignment) is not dict
            or assignment.get("recorded_occurrence_identity") not in assignments
            or event.material.get("applicability_result_event_identity")
            != prior_through_event_occurrence_identity
            or prior_through_event_occurrence_identity not in applicability
        ):
            raise ValueError("ordered relation-path Compare Act is not exact")
    else:
        assignment = event.material.get("responsibility_assignment_reference")
        if (
            type(assignment) is not dict
            or assignment.get("recorded_occurrence_identity") not in assignments
            or event.material.get("responsible_act_evidence_identity")
            != prior_through_event_occurrence_identity
            or event.material.get("applicability_result_event_identity")
            not in applicability
            or event.identity in comparisons
        ):
            raise ValueError("ordered relation-path comparison result is not exact")
    standing_additions = _exact_standing_additions(
        locality_standing,
        event,
        error_message="ordered relation-path comparison Standing is not exact",
    )
    if (
        event.kind
        == COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_RESPONSIBILITY_ASSIGNMENT_KIND
    ):
        assignments[event.identity] = None
    elif (
        event.kind
        == COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_APPLICABILITY_RESULT_KIND
    ):
        applicability[event.identity] = None
    elif (
        event.kind
        == COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_RESULT_KIND
    ):
        comparisons[event.identity] = None
    for key, added in standing_additions.items():
        for value in added:
            _record_distinct(locality_standing[key], value)
    locality_standing["through_event_occurrence_identity"] = event.identity
    locality_standing["event_count"] = event_count + 1
    return locality_standing
