"""Deterministic Locality current-coordinate read over exact material results."""

from __future__ import annotations


from copy import deepcopy
from typing import Any, Iterable

from seed_runtime.event import Event
from seed_runtime.events import CORRUPTED, EventLedger
from seed_runtime.material_source import (
    read_exact_material_result,
)
from seed_runtime.witness_material_source import WITNESS_MATERIAL_SOURCE_RECORDED_KIND
from seed_runtime.byte_measurement import (
    BYTE_MEASUREMENT_RECORDED_KIND,
    BYTE_MEASUREMENT_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
    BYTE_MEASUREMENT_ACT_OCCURRENCE_EVENT,
    BYTE_PAIR_MEASUREMENT_RECORDED_KIND,
    BYTE_PAIR_MEASUREMENT_RESULT_KIND,
    BYTE_PAIR_APPLICABILITY_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
    BYTE_PAIR_MEASUREMENT_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
    BYTE_PAIR_APPLICABILITY_ACT_OCCURRENCE_EVENT,
    BYTE_PAIR_APPLICABILITY_RECORDED_KIND,
    BYTE_PAIR_MEASUREMENT_ACT_OCCURRENCE_EVENT,
    ASSERTION_LOCALITY_MOVEMENT_SUBJECT_TO_ACT_BINDING_KIND,
    ASSERTION_LOCALITY_MOVEMENT_ACT_OCCURRENCE_EVENT,
    ASSERTION_LOCALITY_MOVEMENT_KIND,
    ASSERTION_LOCALITY_MOVEMENT_RESULT_KIND,
    _assertion_carried_by_locality_movement_result,
    _movement_act_material,
    _movement_binding_material,
    _movement_result_material,
    _source_assertion_is_carried,
    _source_assertion_from_reference,
    _source_assertion_reference,
    _source_assertion_coordinates,
    _findings_of_recorded_byte_position_pair_measurement,
    _read_assertion_locality_movement_subject_to_act_binding,
    _read_assertion_locality_movement_act_occurrence,
    _require_exact_movement_binding_and_source,
    _read_byte_measurement_subject_to_act_binding,
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
    OCCURRENCE_POSITION_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
    _occurrence_position_result_material,
    _position_assertions,
    _require_carried_occurrence_position_binding,
    get_occurrence_position_measurement_subject_to_act_binding,
    get_recorded_occurrence_position_measurement,
)
from seed_runtime.yield_relation import (
    RECORDED_YIELD_RELATION_EVENT,
    read_requirements_of_yield_relation,
)
from seed_runtime.measurement_of_recurrent_byte_pair_occurrence_position import (
    RECORDED_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_MEASUREMENT_SUBJECT_TO_ACT_BINDING_KIND,
    RECORDED_ACT_OCCURRENCE_OF_MEASUREMENT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_EVENT,
    RECORDING_OCCURRENCE_OF_RESULT_OF_MEASUREMENT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_KIND,
    _read_recurrent_byte_pair_occurrence_position_measurement_binding,
    _read_recorded_result_of_measurement_of_recurrent_byte_pair_occurrence_position,
)
from seed_runtime.measurement_of_position_coordinates_of_byte_pair_occurrences import (
    BYTE_PAIR_OCCURRENCE_POSITION_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
    BYTE_PAIR_OCCURRENCE_POSITION_ACT_OCCURRENCE_EVENT,
    BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND,
    _require_carried_byte_pair_occurrence_position_subject_to_act_binding,
    get_byte_pair_occurrence_position_measurement_subject_to_act_binding,
    get_byte_pair_occurrence_position_measurement_act_occurrence,
    get_recorded_byte_pair_occurrence_position_measurement,
)
from seed_runtime.measurement_of_shared_position_of_byte_pair_occurrences import (
    SHARED_POSITION_MEASUREMENT_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
    SHARED_POSITION_APPLICABILITY_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
    SHARED_POSITION_APPLICABILITY_ACT_OCCURRENCE_EVENT,
    SHARED_POSITION_APPLICABILITY_RESULT_KIND,
    SHARED_POSITION_MEASUREMENT_ACT_OCCURRENCE_EVENT,
    SHARED_POSITION_MEASUREMENT_RESULT_KIND,
    _read_binding as _read_shared_position_binding,
    _read_applicability_act as _read_shared_position_applicability_act,
    _read_applicability_result as _read_shared_position_applicability_result,
    _read_measurement_act as _read_shared_position_measurement_act,
    _read_measurement_result as _read_shared_position_measurement_result,
    _measurement_binding_addressed_by_applicability,
)
from seed_runtime.addressed_byte_occurrence_reference_determination import (
    DETERMINATION_SUBJECT_TO_ACT_BINDING_RECORDED_KIND as ADDRESSED_BYTE_REFERENCE_DETERMINATION_BINDING_KIND,
    APPLICABILITY_SUBJECT_TO_ACT_BINDING_RECORDED_KIND as ADDRESSED_BYTE_REFERENCE_APPLICABILITY_BINDING_KIND,
    APPLICABILITY_ACT_OCCURRENCE_EVENT as ADDRESSED_BYTE_REFERENCE_APPLICABILITY_ACT_OCCURRENCE_EVENT,
    APPLICABILITY_RESULT_KIND as ADDRESSED_BYTE_REFERENCE_APPLICABILITY_RESULT_KIND,
    DETERMINATION_ACT_OCCURRENCE_EVENT as ADDRESSED_BYTE_REFERENCE_DETERMINATION_ACT_OCCURRENCE_EVENT,
    DETERMINATION_RESULT_KIND as ADDRESSED_BYTE_REFERENCE_DETERMINATION_RESULT_KIND,
    _read_binding as _read_addressed_byte_reference_binding,
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
    THROUGH_OCCURRENCE_BOUNDARY_REFERENCE_ACT_OCCURRENCE_EVENT,
    THROUGH_OCCURRENCE_BOUNDARY_REFERENCE_RECORDED_KIND,
    THROUGH_OCCURRENCE_BOUNDARY_REFERENCE_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
    get_recorded_through_occurrence_boundary_reference,
    get_through_occurrence_boundary_reference_act_occurrence,
    get_through_occurrence_boundary_reference_subject_to_act_binding,
)
from seed_runtime.recorded_boundary_locality import (
    RECORDED_BOUNDARY_LOCALITY_ACT_OCCURRENCE_EVENT,
    RECORDED_BOUNDARY_LOCALITY_RECORDED_KIND,
    RECORDED_BOUNDARY_LOCALITY_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
    get_recorded_boundary_locality,
    get_recorded_boundary_locality_act_occurrence,
    get_recorded_boundary_locality_subject_to_act_binding,
)
from seed_runtime.operator_material_source import (
    OPERATOR_MATERIAL_SOURCE_ACT_OCCURRENCE_EVENT,
    OPERATOR_MATERIAL_SOURCE_RECORDED_KIND,
    OPERATOR_MATERIAL_SOURCE_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
    get_operator_material_source_act_occurrence,
    get_operator_material_source_subject_to_act_binding,
    get_recorded_operator_material_source,
)
from seed_runtime.operator_destination_locality import (
    OPERATOR_DESTINATION_LOCALITY_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
    OPERATOR_DESTINATION_LOCALITY_ACT_OCCURRENCE_EVENT,
    OPERATOR_DESTINATION_LOCALITY_RECORDED_KIND,
    get_operator_destination_locality_subject_to_act_binding,
    get_operator_destination_locality_act_occurrence,
    get_recorded_operator_destination_locality,
)
from seed_runtime.comparison_of_recorded_byte_pair_measurements import (
    RECORDED_PAIR_MEASUREMENT_COMPARISON_SUBJECT_TO_ACT_BINDING_KIND,
    RECORDED_PAIR_MEASUREMENT_COMPARISON_APPLICABILITY_SUBJECT_TO_ACT_BINDING_KIND,
    RECORDED_PAIR_MEASUREMENT_COMPARISON_APPLICABILITY_ACT_OCCURRENCE_EVENT,
    RECORDED_PAIR_MEASUREMENT_COMPARISON_APPLICABILITY_RESULT_KIND,
    RECORDED_PAIR_MEASUREMENT_COMPARISON_ACT_OCCURRENCE_EVENT,
    RECORDED_PAIR_MEASUREMENT_COMPARISON_RESULT_KIND,
    RecordedPairMeasurementComparisonError,
    _binding_reading as _recorded_pair_comparison_binding_reading,
    _applicability_binding_reading as _recorded_pair_comparison_applicability_binding_reading,
    _applicability_act_reading as _recorded_pair_comparison_applicability_act_reading,
    _applicability_reading as _recorded_pair_comparison_applicability_reading,
    _comparison_act_reading as _recorded_pair_comparison_act_reading,
    _recorded_pair_measurement_comparison_reading,
)
from seed_runtime.comparison_of_ordered_relation_path_with_recorded_pair_findings import (
    COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_SUBJECT_TO_ACT_BINDING_KIND,
    COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_APPLICABILITY_SUBJECT_TO_ACT_BINDING_KIND,
    COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_APPLICABILITY_ACT_OCCURRENCE_EVENT,
    COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_APPLICABILITY_RESULT_KIND,
    COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_COMPARE_ACT_OCCURRENCE_EVENT,
    COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_RESULT_KIND,
    _read_binding as _ordered_relation_path_compare_binding_reading,
    _read_applicability_binding as _ordered_relation_path_compare_applicability_binding_reading,
    _read_applicability_act as _ordered_relation_path_compare_applicability_act_reading,
    _read_applicability_result as _ordered_relation_path_compare_applicability_result_reading,
    _read_compare_act as _ordered_relation_path_compare_act_reading,
    get_recorded_comparison_of_ordered_relation_path_with_recorded_pair_findings,
)
from seed_runtime.measurement_of_compare_distinctions import (
    COMPARE_DISTINCTION_MEASUREMENT_SUBJECT_TO_ACT_BINDING_KIND,
    COMPARE_DISTINCTION_MEASUREMENT_ACT_OCCURRENCE_KIND,
    COMPARE_DISTINCTION_MEASUREMENT_RESULT_KIND,
    _read_binding as _read_compare_distinction_measurement_binding,
    _read_act as _read_compare_distinction_measurement_act,
    get_recorded_compare_distinction_measurement,
)
from seed_runtime.comparison_of_ordered_path_source_position_material import (
    COMPARE_SUBJECT_TO_ACT_BINDING_RECORDED_EVENT as ORDERED_PATH_SOURCE_POSITION_COMPARE_BINDING_EVENT,
    APPLICABILITY_SUBJECT_TO_ACT_BINDING_RECORDED_EVENT as ORDERED_PATH_SOURCE_POSITION_COMPARE_APPLICABILITY_BINDING_EVENT,
    APPLICABILITY_ACT_KIND as ORDERED_PATH_SOURCE_POSITION_COMPARE_APPLICABILITY_ACT_KIND,
    APPLICABILITY_RESULT_KIND as ORDERED_PATH_SOURCE_POSITION_COMPARE_APPLICABILITY_RESULT_KIND,
    COMPARE_ACT_KIND as ORDERED_PATH_SOURCE_POSITION_COMPARE_ACT_KIND,
    COMPARE_RESULT_KIND as ORDERED_PATH_SOURCE_POSITION_COMPARE_RESULT_KIND,
    validate_ordered_path_source_position_material_comparison_event,
)
from seed_runtime.source_position_recurrence import (
    COMPARE_APPLICABILITY_SUBJECT_TO_ACT_BINDING_RECORDED_EVENT,
    COMPARE_SUBJECT_TO_ACT_BINDING_RECORDED_EVENT,
    SOURCE_POSITION_MEASUREMENT_SUBJECT_TO_ACT_BINDING_RECORDED_EVENT,
    RECURRENCE_MEASUREMENT_SUBJECT_TO_ACT_BINDING_RECORDED_EVENT,
    COORDINATE_MEASUREMENT_SUBJECT_TO_ACT_BINDING_RECORDED_EVENT,
    RECURRENT_RESULT_MATERIAL_MEASUREMENT_SUBJECT_TO_ACT_BINDING_RECORDED_EVENT,
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


_SUBJECT_BY_KIND = {
    WITNESS_MATERIAL_SOURCE_RECORDED_KIND: "material_result_occurrence",
}
_MEASUREMENT_ACT_OCCURRENCE_EVENTS = {
    BYTE_MEASUREMENT_ACT_OCCURRENCE_EVENT,
    OCCURRENCE_POSITION_ACT_OCCURRENCE_EVENT,
    RECORDED_ACT_OCCURRENCE_OF_MEASUREMENT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_EVENT,
    BYTE_PAIR_OCCURRENCE_POSITION_ACT_OCCURRENCE_EVENT,
}
_MEASUREMENT_BINDING_KINDS = {
    BYTE_MEASUREMENT_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
    OCCURRENCE_POSITION_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
    RECORDED_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_MEASUREMENT_SUBJECT_TO_ACT_BINDING_KIND,
    BYTE_PAIR_OCCURRENCE_POSITION_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
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
    BYTE_PAIR_MEASUREMENT_ACT_OCCURRENCE_EVENT,
    BYTE_PAIR_MEASUREMENT_RECORDED_KIND,
}
_LOCALITY_CONTINUATION_KINDS = {
    LOCALITY_CONTINUATION_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
    LOCALITY_CONTINUATION_ACT_OCCURRENCE_EVENT,
    LOCALITY_CONTINUATION_RECORDED_KIND,
}
_THROUGH_OCCURRENCE_BOUNDARY_REFERENCE_KINDS = {
    THROUGH_OCCURRENCE_BOUNDARY_REFERENCE_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
    THROUGH_OCCURRENCE_BOUNDARY_REFERENCE_ACT_OCCURRENCE_EVENT,
    THROUGH_OCCURRENCE_BOUNDARY_REFERENCE_RECORDED_KIND,
}
_RECORDED_BOUNDARY_LOCALITY_KINDS = {
    RECORDED_BOUNDARY_LOCALITY_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
    RECORDED_BOUNDARY_LOCALITY_ACT_OCCURRENCE_EVENT,
    RECORDED_BOUNDARY_LOCALITY_RECORDED_KIND,
}
_OPERATOR_MATERIAL_SOURCE_KINDS = {
    OPERATOR_MATERIAL_SOURCE_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
    OPERATOR_MATERIAL_SOURCE_ACT_OCCURRENCE_EVENT,
    OPERATOR_MATERIAL_SOURCE_RECORDED_KIND,
}
_OPERATOR_DESTINATION_LOCALITY_KINDS = {
    OPERATOR_DESTINATION_LOCALITY_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
    OPERATOR_DESTINATION_LOCALITY_ACT_OCCURRENCE_EVENT,
    OPERATOR_DESTINATION_LOCALITY_RECORDED_KIND,
}
_RECORDED_PAIR_MEASUREMENT_COMPARISON_KINDS = {
    RECORDED_PAIR_MEASUREMENT_COMPARISON_SUBJECT_TO_ACT_BINDING_KIND,
    RECORDED_PAIR_MEASUREMENT_COMPARISON_APPLICABILITY_SUBJECT_TO_ACT_BINDING_KIND,
    RECORDED_PAIR_MEASUREMENT_COMPARISON_APPLICABILITY_ACT_OCCURRENCE_EVENT,
    RECORDED_PAIR_MEASUREMENT_COMPARISON_APPLICABILITY_RESULT_KIND,
    RECORDED_PAIR_MEASUREMENT_COMPARISON_ACT_OCCURRENCE_EVENT,
    RECORDED_PAIR_MEASUREMENT_COMPARISON_RESULT_KIND,
}
_SHARED_POSITION_MEASUREMENT_KINDS = {
    SHARED_POSITION_MEASUREMENT_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
    SHARED_POSITION_APPLICABILITY_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
    SHARED_POSITION_APPLICABILITY_ACT_OCCURRENCE_EVENT,
    SHARED_POSITION_APPLICABILITY_RESULT_KIND,
    SHARED_POSITION_MEASUREMENT_ACT_OCCURRENCE_EVENT,
    SHARED_POSITION_MEASUREMENT_RESULT_KIND,
}
_ADDRESSED_BYTE_REFERENCE_DETERMINATION_KINDS = {
    ADDRESSED_BYTE_REFERENCE_DETERMINATION_BINDING_KIND,
    ADDRESSED_BYTE_REFERENCE_APPLICABILITY_BINDING_KIND,
    ADDRESSED_BYTE_REFERENCE_APPLICABILITY_ACT_OCCURRENCE_EVENT,
    ADDRESSED_BYTE_REFERENCE_APPLICABILITY_RESULT_KIND,
    ADDRESSED_BYTE_REFERENCE_DETERMINATION_ACT_OCCURRENCE_EVENT,
    ADDRESSED_BYTE_REFERENCE_DETERMINATION_RESULT_KIND,
}
_COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_KINDS = {
    COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_SUBJECT_TO_ACT_BINDING_KIND,
    COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_APPLICABILITY_SUBJECT_TO_ACT_BINDING_KIND,
    COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_APPLICABILITY_ACT_OCCURRENCE_EVENT,
    COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_APPLICABILITY_RESULT_KIND,
    COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_COMPARE_ACT_OCCURRENCE_EVENT,
    COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_RESULT_KIND,
}
_COMPARE_DISTINCTION_MEASUREMENT_KINDS = {
    COMPARE_DISTINCTION_MEASUREMENT_SUBJECT_TO_ACT_BINDING_KIND,
    COMPARE_DISTINCTION_MEASUREMENT_ACT_OCCURRENCE_KIND,
    COMPARE_DISTINCTION_MEASUREMENT_RESULT_KIND,
}
_ORDERED_PATH_SOURCE_POSITION_MATERIAL_COMPARISON_KINDS = {
    ORDERED_PATH_SOURCE_POSITION_COMPARE_BINDING_EVENT,
    ORDERED_PATH_SOURCE_POSITION_COMPARE_APPLICABILITY_BINDING_EVENT,
    ORDERED_PATH_SOURCE_POSITION_COMPARE_APPLICABILITY_ACT_KIND,
    ORDERED_PATH_SOURCE_POSITION_COMPARE_APPLICABILITY_RESULT_KIND,
    ORDERED_PATH_SOURCE_POSITION_COMPARE_ACT_KIND,
    ORDERED_PATH_SOURCE_POSITION_COMPARE_RESULT_KIND,
}
_SOURCE_POSITION_RECURRENCE_KINDS = {
    COMPARE_APPLICABILITY_SUBJECT_TO_ACT_BINDING_RECORDED_EVENT,
    COMPARE_SUBJECT_TO_ACT_BINDING_RECORDED_EVENT,
    SOURCE_POSITION_MEASUREMENT_SUBJECT_TO_ACT_BINDING_RECORDED_EVENT,
    RECURRENCE_MEASUREMENT_SUBJECT_TO_ACT_BINDING_RECORDED_EVENT,
    COORDINATE_MEASUREMENT_SUBJECT_TO_ACT_BINDING_RECORDED_EVENT,
    RECURRENT_RESULT_MATERIAL_MEASUREMENT_SUBJECT_TO_ACT_BINDING_RECORDED_EVENT,
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
    *_MEASUREMENT_BINDING_KINDS,
    *_MEASUREMENT_RECORDED_KINDS,
    *_ASSERTION_LOCALITY_MOVEMENT_KINDS,
    *_BYTE_PAIR_MEASUREMENT_LIFECYCLE_KINDS,
    *_LOCALITY_CONTINUATION_KINDS,
    *_THROUGH_OCCURRENCE_BOUNDARY_REFERENCE_KINDS,
    *_RECORDED_BOUNDARY_LOCALITY_KINDS,
    *_OPERATOR_MATERIAL_SOURCE_KINDS,
    *_OPERATOR_DESTINATION_LOCALITY_KINDS,
    *_RECORDED_PAIR_MEASUREMENT_COMPARISON_KINDS,
    *_SHARED_POSITION_MEASUREMENT_KINDS,
    *_ADDRESSED_BYTE_REFERENCE_DETERMINATION_KINDS,
    *_COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_KINDS,
    *_COMPARE_DISTINCTION_MEASUREMENT_KINDS,
    *_ORDERED_PATH_SOURCE_POSITION_MATERIAL_COMPARISON_KINDS,
    *_SOURCE_POSITION_RECURRENCE_KINDS,
}


def _measurement_occurrence_coordinates(event) -> dict[str, str]:
    """Carry only the identities of one exact Measurement result."""

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
    binding = ledger.get(binding_reference["recorded_occurrence_identity"])
    if binding is None:
        raise ValueError("result-position Locality movement coordinates are not exact")
    source_reference = binding.material["source_assertion_reference"]
    source_event = ledger.get(source_reference["recorded_occurrence_identity"])
    if source_event is None:
        raise ValueError("result-position Locality movement coordinates are not exact")
    return {
        "recorded_occurrence_identity": event.identity,
        "result_identity": event.material["result_identity"],
        "source_assertion_reference": deepcopy(source_reference),
        "source_assertion_coordinates": deepcopy(
            binding.material["source_assertion_coordinates"]
        ),
        "source_through_event_occurrence_identity": binding.material[
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


_REQUIRED_DIRECT_BINDING_COORDINATES = frozenset(
    {
        "recorded_occurrence_identity",
        "book_clause_identity",
        "exact_act_identity",
        "subject_reference",
    }
)

_DIRECT_BINDING_COORDINATES_WITH_RESULT = (
    _REQUIRED_DIRECT_BINDING_COORDINATES | {"result_identity"}
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
    if event.kind in {
        LOCALITY_CONTINUATION_RECORDED_KIND,
        RECORDED_BOUNDARY_LOCALITY_RECORDED_KIND,
        OPERATOR_DESTINATION_LOCALITY_RECORDED_KIND,
    }:
        act_occurrence = ledger.get(
            event.material.get("act_occurrence_event_identity")
        )
        if act_occurrence is None:
            return _NO_RESULT_COORDINATE
        try:
            ledger.occurrences_in_append_order(
                (act_occurrence.identity, event.identity),
                locality_identity=event.locality_identity,
            )
        except ValueError:
            return _NO_RESULT_COORDINATE
    else:
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
        return None
    if ledger.integrity_of(act_occurrence.identity) == CORRUPTED:
        raise ValueError(
            "recorded subject-to-Act binding requires its intact Act occurrence"
        )
    direct_shape = (
        type(reference) is dict
        and frozenset(reference)
        in {
            _REQUIRED_DIRECT_BINDING_COORDINATES,
            _DIRECT_BINDING_COORDINATES_WITH_RESULT,
        }
        and all(
            type(reference.get(coordinate)) is str
            and reference[coordinate]
            for coordinate in _REQUIRED_DIRECT_BINDING_COORDINATES
            - {"subject_reference"}
        )
        and type(reference.get("subject_reference")) is dict
        and bool(reference["subject_reference"])
    )
    if not direct_shape:
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
    for coordinate in _REQUIRED_DIRECT_BINDING_COORDINATES - {
        "recorded_occurrence_identity",
    }:
        if binding_event.material.get(coordinate) != reference[coordinate]:
            raise ValueError(
                "recorded subject-to-Act binding disagrees with its occurrence"
            )
    declared_results = {
        value
        for coordinate, value in binding_event.material.items()
        if (
            coordinate.endswith("_result_identity")
            or coordinate == "result_identity"
        )
        and type(value) is str
        and value
    }
    result_identity = event.material.get("result_identity")
    if result_identity not in declared_results:
        raise ValueError(
            "recorded subject-to-Act binding disagrees with its occurrence"
        )
    if (
        "result_identity" in reference
        and reference["result_identity"] != result_identity
    ):
        raise ValueError(
            "recorded subject-to-Act binding names another result"
        )
    return deepcopy(reference)


def _shared_position_binding_reading(
    ledger: EventLedger,
    event,
    *,
    prior_coordinates: dict[str, Any],
):
    binding_identity = event.identity
    if event.kind not in {
        SHARED_POSITION_MEASUREMENT_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
        SHARED_POSITION_APPLICABILITY_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
    }:
        reference = event.material.get("subject_to_act_binding_reference")
        binding_identity = (
            reference.get("recorded_occurrence_identity")
            if type(reference) is dict
            else None
        )
    return _read_shared_position_binding(
        ledger,
        binding_identity,
        prior_coordinates=prior_coordinates,
    )


def read_operator_current_coordinates(
    ledger: EventLedger, *, locality_identity: str
) -> dict[str, Any]:
    """Read current Locality coordinates by replaying the whole Locality.

    Equivalent to advancing from empty prior coordinates over every recorded
    occurrence. `#2376` established that advancing prior coordinates over only
    the occurrences after the through-occurrence boundary yields equal
    coordinates, so a caller that already holds those coordinates should use
    :func:`advance_operator_current_coordinates` instead of replaying.
    """

    return advance_operator_current_coordinates(
        ledger,
        (
            event.identity
            for event in ledger.list_locality(locality_identity)
        ),
        locality_identity=locality_identity,
    )


def read_operator_current_coordinates_through(
    ledger: EventLedger,
    *,
    locality_identity: str,
    through_event_occurrence_identity: str | None,
) -> dict[str, Any]:
    """Read one Locality through one exact recorded occurrence.

    ``None`` addresses coordinates before any occurrence. Otherwise the Ledger
    resolves the occurrence to its existing append boundary and then reads only
    that prefix. Later occurrences in the addressed or another Locality are neither
    selected nor copied into the returned coordinates.
    """

    if type(locality_identity) is not str or not locality_identity:
        raise ValueError("current-coordinate read requires one exact Locality identity")
    if through_event_occurrence_identity is None:
        event_identities: Iterable[str] = ()
    else:
        if type(through_event_occurrence_identity) is not str or not through_event_occurrence_identity:
            raise ValueError("current-coordinate read requires one exact through occurrence")
        event = ledger.get(through_event_occurrence_identity)
        if (
            event is None
            or event.locality_identity != locality_identity
            or ledger.integrity_of(through_event_occurrence_identity) == CORRUPTED
        ):
            raise ValueError(
                "current-coordinate through occurrence is absent, corrupted, or in another Locality"
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
    current_coordinates = advance_operator_current_coordinates(
        ledger,
        event_identities,
        locality_identity=locality_identity,
    )
    if current_coordinates["through_event_occurrence_identity"] != through_event_occurrence_identity:
        raise ValueError("current-coordinate read did not reach its exact through occurrence")
    return current_coordinates


class CarriedCoordinateReferenceError(ValueError):
    """One carried coordinate reference could not be resolved."""


def _require_carried_reference_identity(value: Any, message: str) -> str:
    if type(value) is not str or not value:
        raise CarriedCoordinateReferenceError(message)
    return value


def _source_reference_from_checkpoint(
    ledger: EventLedger, recorded_occurrence_identity: str
) -> dict[str, str | None]:
    recorded = get_recorded_through_occurrence_boundary_reference(
        ledger, recorded_occurrence_identity
    )
    source = recorded["source_reference"]
    return {
        "source_locality_identity": source["source_locality_identity"],
        "source_through_event_occurrence_identity": source[
            "through_event_occurrence_identity"
        ],
    }


def _source_reference_from_checkout(
    ledger: EventLedger, recorded_occurrence_identity: str
) -> dict[str, str | None]:
    relation = get_recorded_boundary_locality(
        ledger, recorded_occurrence_identity
    )
    reference = relation["through_occurrence_boundary_reference"]
    reference_occurrence_identity = _require_carried_reference_identity(
        reference.get("recorded_occurrence_identity"),
        "recorded boundary Locality relation carries no exact boundary reference",
    )
    recorded = get_recorded_through_occurrence_boundary_reference(
        ledger, reference_occurrence_identity
    )
    if reference.get("result_identity") != recorded["result_identity"]:
        raise CarriedCoordinateReferenceError(
            "recorded boundary Locality relation names a different boundary result"
        )
    return _source_reference_from_checkpoint(ledger, reference_occurrence_identity)


def read_current_coordinates_through_carried_reference(
    ledger: EventLedger,
    *,
    locality_identity: str,
    recorded_occurrence_identity: str,
) -> dict[str, Any]:
    """Read source coordinates through one reference carried at one Locality.

    Through-occurrence reference, Locality continuation, and recorded-boundary
    Locality relation results remain distinct recorded occurrences. This read
    projects only the exact source Locality through the exact source occurrence.
    """

    _require_carried_reference_identity(
        locality_identity, "carried coordinate read requires a Locality"
    )
    _require_carried_reference_identity(
        recorded_occurrence_identity,
        "carried coordinate read requires one exact occurrence",
    )
    current_coordinates = read_operator_current_coordinates(
        ledger, locality_identity=locality_identity
    )
    direct_references = current_coordinates[
        "recorded_through_occurrence_boundary_references"
    ]
    continuations = current_coordinates["locality_continuation_relation_occurrences"]
    locality_relations = current_coordinates["recorded_boundary_locality_relations"]
    carriers = (direct_references, continuations, locality_relations)
    for carrier in carriers:
        if type(carrier) is not dict or any(
            value is not None for value in carrier.values()
        ):
            raise CarriedCoordinateReferenceError(
                "carried coordinate reference is not exact"
            )
    matches = sum(
        recorded_occurrence_identity in carrier for carrier in carriers
    )
    if matches != 1:
        raise CarriedCoordinateReferenceError(
            "coordinate reference is not carried exactly once at this Locality"
        )
    event = ledger.get(recorded_occurrence_identity)
    if event is None or event.locality_identity != locality_identity:
        raise CarriedCoordinateReferenceError(
            "coordinate reference has a different carrying Locality"
        )

    if recorded_occurrence_identity in direct_references:
        source_reference = _source_reference_from_checkpoint(
            ledger, recorded_occurrence_identity
        )
    elif recorded_occurrence_identity in continuations:
        continuation = get_recorded_locality_continuation(
            ledger, recorded_occurrence_identity
        )
        source_reference = deepcopy(continuation["source_coordinate_reference"])
    else:
        source_reference = _source_reference_from_checkout(
            ledger, recorded_occurrence_identity
        )

    source_locality_identity = _require_carried_reference_identity(
        source_reference.get("source_locality_identity"),
        "coordinate reference carries no exact source Locality",
    )
    through_event_occurrence_identity = source_reference.get(
        "source_through_event_occurrence_identity"
    )
    if through_event_occurrence_identity is not None:
        _require_carried_reference_identity(
            through_event_occurrence_identity,
            "coordinate reference carries no exact through occurrence",
        )
    source_current_coordinates = read_operator_current_coordinates_through(
        ledger,
        locality_identity=source_locality_identity,
        through_event_occurrence_identity=through_event_occurrence_identity,
    )
    return {
        "recorded_occurrence_identity": recorded_occurrence_identity,
        "source_coordinate_reference": source_reference,
        "current_coordinates": source_current_coordinates,
    }


def advance_operator_current_coordinates(
    ledger: EventLedger,
    event_identities: Iterable[str],
    *,
    locality_identity: str,
    prior: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Advance current Locality coordinates over exact Ledger occurrences.

    With no `prior`, this reads the supplied identities from empty coordinates.
    With a `prior`, it begins from the accumulators already established there.
    The Ledger verifies each identity's Locality and append order. The supplied
    identities must be the complete Locality interval after `prior` through the
    final supplied occurrence.

    The caller supplies exact identities recorded by Act occurrences. The
    Ledger resolves those identities rather than accepting occurrence copies.

    Every accumulator read by the live occurrence forms is seeded from `prior`,
    and the per-occurrence paths and refusals below are exactly those used during
    reconstruction. Those refusals consult accumulated coordinates rather than the Ledger,
    which is why seeding preserves them (`#2376`).

    **The advance has as input `prior`.** Its accumulators are taken over rather
    than copied, and the returned coordinates share them. A caller that needs
    the earlier coordinates unchanged must read them again; there is no
    snapshot here.

    Coordinates grow with the Locality, so copying them per advance would cost
    the Locality occurrence count every time and reinstate the quadratic this
    replaced. The console carries one mapping forward.

    The result is fully recomputable from the Ledger and is not itself recorded:
    it returns only current coordinates. An empty coordinate is absence of
    record, not a negative finding. No Yield is established here.
    """
    events = ledger.occurrences_in_append_order(
        event_identities,
        locality_identity=locality_identity,
    )
    material_result_occurrences: list[dict[str, Any]] = []
    measurement_occurrences: dict[str, dict[str, str]] = {}
    assertion_locality_movement_occurrences: dict[str, dict[str, Any]] = {}
    exact_result_occurrences: dict[str, dict[str, Any]] = {}
    locality_continuation_relation_occurrences: dict[str, None] = {}
    recorded_through_occurrence_boundary_references: dict[str, None] = {}
    recorded_boundary_locality_relations: dict[str, None] = {}
    operator_destination_locality_relations: dict[str, None] = {}
    subject_to_act_binding_occurrences: dict[str, None] = {}
    operator_material_source_act_occurrences: dict[str, None] = {}
    applicability_result_occurrences: dict[str, None] = {}
    comparison_result_occurrences: dict[str, None] = {}
    through_event_occurrence_identity: str | None = None
    event_count = 0

    if prior is not None:
        # Every accumulator the live event kinds read, taken over from the
        # prior coordinates that already input the earlier occurrences. Not copied:
        # see the shared-accumulator note above.
        material_result_occurrences = prior["material_result_occurrences"]
        if type(material_result_occurrences) is not list:
            raise ValueError(
                "prior coordinates require exact material result occurrences"
            )
        measurement_occurrences = prior["measurement_occurrences"]
        if type(measurement_occurrences) is not dict:
            raise ValueError(
                "prior coordinates require exact Measurement occurrences"
            )
        assertion_locality_movement_occurrences = prior[
            "assertion_locality_movement_occurrences"
        ]
        if type(assertion_locality_movement_occurrences) is not dict:
            raise ValueError(
                "prior coordinates require exact result-position Locality movement occurrences"
            )
        exact_result_occurrences = prior["exact_result_occurrences"]
        locality_continuation_relation_occurrences = prior[
            "locality_continuation_relation_occurrences"
        ]
        if type(locality_continuation_relation_occurrences) is not dict:
            raise ValueError(
                "prior coordinates require exact Locality continuation relations"
            )
        recorded_through_occurrence_boundary_references = prior[
            "recorded_through_occurrence_boundary_references"
        ]
        if type(recorded_through_occurrence_boundary_references) is not dict:
            raise ValueError(
                "prior current coordinates require exact through-occurrence boundary "
                "references"
            )
        recorded_boundary_locality_relations = prior[
            "recorded_boundary_locality_relations"
        ]
        if type(recorded_boundary_locality_relations) is not dict:
            raise ValueError(
                "prior coordinates require exact recorded boundary Locality relations"
            )
        operator_destination_locality_relations = prior[
            "operator_destination_locality_relations"
        ]
        if type(operator_destination_locality_relations) is not dict:
            raise ValueError(
                "prior coordinates require exact operator destination Locality relations"
            )
        subject_to_act_binding_occurrences = prior[
            "subject_to_act_binding_occurrences"
        ]
        if type(subject_to_act_binding_occurrences) is not dict:
            raise ValueError(
                "prior coordinates require exact subject-to-Act binding occurrences"
            )
        operator_material_source_act_occurrences = prior[
            "operator_material_source_act_occurrences"
        ]
        if type(operator_material_source_act_occurrences) is not dict:
            raise ValueError(
                "prior coordinates require exact operator material source Act occurrences"
            )
        applicability_result_occurrences = prior[
            "applicability_result_occurrences"
        ]
        if type(applicability_result_occurrences) is not dict:
            raise ValueError(
                "prior coordinates require exact Applicability result occurrences"
            )
        comparison_result_occurrences = prior["comparison_result_occurrences"]
        if type(comparison_result_occurrences) is not dict:
            raise ValueError(
                "prior coordinates require exact Compare result occurrences"
            )
        through_event_occurrence_identity = prior["through_event_occurrence_identity"]
        event_count = prior["event_count"]

    if events:
        interval = ledger.locality_occurrence_interval(
            locality_identity=locality_identity,
            after_occurrence_identity=through_event_occurrence_identity,
            through_occurrence_identity=events[-1].identity,
        )
        if tuple(event.identity for event in interval) != tuple(
            event.identity for event in events
        ):
            raise ValueError(
                "current-coordinate advance requires the complete Locality occurrence interval"
            )

    for event in events:
        if event.locality_identity != locality_identity:
            continue
        if not (
            event.kind == WITNESS_MATERIAL_SOURCE_RECORDED_KIND
            or event.kind in _MEASUREMENT_ACT_OCCURRENCE_EVENTS
            or event.kind in _MEASUREMENT_BINDING_KINDS
            or event.kind in _MEASUREMENT_RECORDED_KINDS
            or event.kind in _ASSERTION_LOCALITY_MOVEMENT_KINDS
            or event.kind in _BYTE_PAIR_MEASUREMENT_LIFECYCLE_KINDS
            or event.kind in _LOCALITY_CONTINUATION_KINDS
            or event.kind in _THROUGH_OCCURRENCE_BOUNDARY_REFERENCE_KINDS
            or event.kind in _RECORDED_BOUNDARY_LOCALITY_KINDS
            or event.kind in _OPERATOR_MATERIAL_SOURCE_KINDS
            or event.kind in _OPERATOR_DESTINATION_LOCALITY_KINDS
            or event.kind in _RECORDED_PAIR_MEASUREMENT_COMPARISON_KINDS
            or event.kind in _SHARED_POSITION_MEASUREMENT_KINDS
            or event.kind in _ADDRESSED_BYTE_REFERENCE_DETERMINATION_KINDS
            or event.kind in _COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_KINDS
            or event.kind in _COMPARE_DISTINCTION_MEASUREMENT_KINDS
            or event.kind in _ORDERED_PATH_SOURCE_POSITION_MATERIAL_COMPARISON_KINDS
            or event.kind in _SOURCE_POSITION_RECURRENCE_KINDS
        ):
            continue
        if event.kind not in _SUPPORTED_KINDS:
            raise ValueError(f"unsupported current-coordinate occurrence: {event.kind}")
        prior_through_event_occurrence_identity = through_event_occurrence_identity
        pair_lifecycle_event = event.kind in _BYTE_PAIR_MEASUREMENT_LIFECYCLE_KINDS
        if not pair_lifecycle_event:
            event_count += 1
            through_event_occurrence_identity = event.identity
            result_coordinate = _result_subject_to_act_binding_coordinate(ledger, event)
            if result_coordinate is not _NO_RESULT_COORDINATE:
                exact_result_occurrences[event.identity] = result_coordinate
        if event.kind in _MEASUREMENT_ACT_OCCURRENCE_EVENTS:
            continue
        pair_prior_coordinates = {
            "locality_identity": locality_identity,
            "through_event_occurrence_identity": (
                prior_through_event_occurrence_identity
            ),
            "measurement_occurrences": measurement_occurrences,
            "material_result_occurrences": material_result_occurrences,
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
            "comparison_result_occurrences": comparison_result_occurrences,
        }
        if pair_lifecycle_event:
            if event.kind == BYTE_PAIR_APPLICABILITY_SUBJECT_TO_ACT_BINDING_RECORDED_KIND:
                _read_pair_applicability_subject_to_act_binding(
                    ledger, event.identity, prior_coordinates=pair_prior_coordinates
                )
                subject_to_act_binding_occurrences[event.identity] = None
            elif event.kind == BYTE_PAIR_MEASUREMENT_SUBJECT_TO_ACT_BINDING_RECORDED_KIND:
                _read_pair_measurement_subject_to_act_binding(
                    ledger, event.identity, prior_coordinates=pair_prior_coordinates
                )
                subject_to_act_binding_occurrences[event.identity] = None
            elif event.kind == BYTE_PAIR_APPLICABILITY_ACT_OCCURRENCE_EVENT:
                _read_pair_applicability_act_occurrence(
                    ledger, event.identity, prior_coordinates=pair_prior_coordinates
                )
            elif event.kind == BYTE_PAIR_APPLICABILITY_RECORDED_KIND:
                _read_recorded_pair_input_applicability(
                    ledger, event.identity, prior_coordinates=pair_prior_coordinates
                )
                applicability_result_occurrences[event.identity] = None
            elif event.kind == BYTE_PAIR_MEASUREMENT_ACT_OCCURRENCE_EVENT:
                _read_pair_measurement_act_occurrence(
                    ledger, event.identity, prior_coordinates=pair_prior_coordinates
                )
            else:
                _findings_of_recorded_byte_position_pair_measurement(
                    ledger, event.identity, prior_coordinates=pair_prior_coordinates
                )
                measurement_occurrences[event.identity] = (
                    _measurement_occurrence_coordinates(event)
                )
            event_count += 1
            through_event_occurrence_identity = event.identity
            result_coordinate = _result_subject_to_act_binding_coordinate(ledger, event)
            if result_coordinate is not _NO_RESULT_COORDINATE:
                exact_result_occurrences[event.identity] = result_coordinate
            continue
        if event.kind == BYTE_MEASUREMENT_SUBJECT_TO_ACT_BINDING_RECORDED_KIND:
            _read_byte_measurement_subject_to_act_binding(
                ledger,
                event.identity,
                prior_coordinates={
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
            == RECORDED_PAIR_MEASUREMENT_COMPARISON_APPLICABILITY_SUBJECT_TO_ACT_BINDING_KIND
        ):
            addressed_act_identity = event.material.get("addressed_act_identity")
            comparison_bindings = tuple(
                candidate
                for identity in subject_to_act_binding_occurrences
                for candidate in (ledger.get(identity),)
                if candidate is not None
                and candidate.kind
                == RECORDED_PAIR_MEASUREMENT_COMPARISON_SUBJECT_TO_ACT_BINDING_KIND
                and candidate.material.get("exact_act_identity")
                == addressed_act_identity
            )
            if len(comparison_bindings) != 1:
                raise RecordedPairMeasurementComparisonError(
                    "comparison Applicability binding addresses no carried Compare binding"
                )
            comparison_binding_reading = _recorded_pair_comparison_binding_reading(
                ledger,
                comparison_bindings[0].identity,
                prior_coordinates=pair_prior_coordinates,
            )
            _recorded_pair_comparison_applicability_binding_reading(
                ledger,
                event.identity,
                comparison_binding_reading=comparison_binding_reading,
                prior_coordinates=pair_prior_coordinates,
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
                prior_destination_coordinates={
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
                prior_destination_coordinates={
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
                prior_destination_coordinates={
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
            == OCCURRENCE_POSITION_SUBJECT_TO_ACT_BINDING_RECORDED_KIND
        ):
            get_occurrence_position_measurement_subject_to_act_binding(
                ledger, event.identity
            )
            subject_to_act_binding_occurrences[event.identity] = None
            continue
        if event.kind == BYTE_PAIR_OCCURRENCE_POSITION_SUBJECT_TO_ACT_BINDING_RECORDED_KIND:
            get_byte_pair_occurrence_position_measurement_subject_to_act_binding(
                ledger,
                event.identity,
                prior_coordinates=pair_prior_coordinates,
            )
            subject_to_act_binding_occurrences[event.identity] = None
            continue
        if (
            event.kind
            == RECORDED_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_MEASUREMENT_SUBJECT_TO_ACT_BINDING_KIND
        ):
            _read_recurrent_byte_pair_occurrence_position_measurement_binding(
                ledger,
                event.identity,
                prior_coordinates={
                    "locality_identity": locality_identity,
                    "through_event_occurrence_identity": (
                        prior_through_event_occurrence_identity
                    ),
                    "measurement_occurrences": measurement_occurrences,
                    "material_result_occurrences": material_result_occurrences,
                    "subject_to_act_binding_occurrences": (
                        subject_to_act_binding_occurrences
                    ),
                },
            )
            subject_to_act_binding_occurrences[event.identity] = None
            continue
        if (
            event.kind
            == THROUGH_OCCURRENCE_BOUNDARY_REFERENCE_SUBJECT_TO_ACT_BINDING_RECORDED_KIND
        ):
            get_through_occurrence_boundary_reference_subject_to_act_binding(
                ledger, event.identity
            )
            subject_to_act_binding_occurrences[event.identity] = None
            continue
        if event.kind == THROUGH_OCCURRENCE_BOUNDARY_REFERENCE_ACT_OCCURRENCE_EVENT:
            get_through_occurrence_boundary_reference_act_occurrence(ledger, event.identity)
            continue
        if event.kind == THROUGH_OCCURRENCE_BOUNDARY_REFERENCE_RECORDED_KIND:
            get_recorded_through_occurrence_boundary_reference(ledger, event.identity)
            recorded_through_occurrence_boundary_references[event.identity] = None
            continue
        if (
            event.kind
            == RECORDED_BOUNDARY_LOCALITY_SUBJECT_TO_ACT_BINDING_RECORDED_KIND
        ):
            get_recorded_boundary_locality_subject_to_act_binding(
                ledger, event.identity
            )
            subject_to_act_binding_occurrences[event.identity] = None
            continue
        if event.kind == RECORDED_BOUNDARY_LOCALITY_ACT_OCCURRENCE_EVENT:
            get_recorded_boundary_locality_act_occurrence(
                ledger, event.identity
            )
            continue
        if event.kind == RECORDED_BOUNDARY_LOCALITY_RECORDED_KIND:
            get_recorded_boundary_locality(ledger, event.identity)
            recorded_boundary_locality_relations[event.identity] = None
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
            get_recorded_operator_material_source(ledger, event.identity)
        if (
            event.kind
            == OPERATOR_DESTINATION_LOCALITY_SUBJECT_TO_ACT_BINDING_RECORDED_KIND
        ):
            get_operator_destination_locality_subject_to_act_binding(
                ledger, event.identity
            )
            subject_to_act_binding_occurrences[event.identity] = None
            continue
        if event.kind == OPERATOR_DESTINATION_LOCALITY_ACT_OCCURRENCE_EVENT:
            get_operator_destination_locality_act_occurrence(ledger, event.identity)
            continue
        if event.kind == OPERATOR_DESTINATION_LOCALITY_RECORDED_KIND:
            get_recorded_operator_destination_locality(ledger, event.identity)
            operator_destination_locality_relations[event.identity] = None
            continue
        addressed_byte_reference_prior_coordinates = {
            "locality_identity": locality_identity,
            "through_event_occurrence_identity": (
                prior_through_event_occurrence_identity
            ),
            "measurement_occurrences": measurement_occurrences,
            "material_result_occurrences": material_result_occurrences,
            "subject_to_act_binding_occurrences": (
                subject_to_act_binding_occurrences
            ),
            "applicability_result_occurrences": (
                applicability_result_occurrences
            ),
        }
        if event.kind in {
            ADDRESSED_BYTE_REFERENCE_DETERMINATION_BINDING_KIND,
            ADDRESSED_BYTE_REFERENCE_APPLICABILITY_BINDING_KIND,
        }:
            _read_addressed_byte_reference_binding(
                ledger,
                event.identity,
                prior_coordinates=addressed_byte_reference_prior_coordinates,
            )
            subject_to_act_binding_occurrences[event.identity] = None
            continue
        if event.kind == ADDRESSED_BYTE_REFERENCE_APPLICABILITY_ACT_OCCURRENCE_EVENT:
            _read_addressed_byte_reference_applicability_act(
                ledger,
                event.identity,
                prior_coordinates=addressed_byte_reference_prior_coordinates,
            )
            continue
        if event.kind == ADDRESSED_BYTE_REFERENCE_APPLICABILITY_RESULT_KIND:
            _read_addressed_byte_reference_applicability_result(
                ledger,
                event.identity,
                prior_coordinates=addressed_byte_reference_prior_coordinates,
            )
            applicability_result_occurrences[event.identity] = None
            continue
        if event.kind == ADDRESSED_BYTE_REFERENCE_DETERMINATION_ACT_OCCURRENCE_EVENT:
            _read_addressed_byte_reference_determination_act(
                ledger,
                event.identity,
                prior_coordinates=addressed_byte_reference_prior_coordinates,
            )
            continue
        if (
            event.kind
            == SHARED_POSITION_MEASUREMENT_SUBJECT_TO_ACT_BINDING_RECORDED_KIND
        ):
            _shared_position_binding_reading(
                ledger,
                event,
                prior_coordinates=addressed_byte_reference_prior_coordinates,
            )
            subject_to_act_binding_occurrences[event.identity] = None
            continue
        if (
            event.kind
            == SHARED_POSITION_APPLICABILITY_SUBJECT_TO_ACT_BINDING_RECORDED_KIND
        ):
            applicability_binding, inputs = _shared_position_binding_reading(
                ledger,
                event,
                prior_coordinates=addressed_byte_reference_prior_coordinates,
            )
            measurement_binding = _measurement_binding_addressed_by_applicability(
                ledger,
                applicability_binding,
                inputs,
            )
            if measurement_binding.identity not in subject_to_act_binding_occurrences:
                raise ValueError(
                    "shared-position Applicability binding addresses no exact Measurement binding"
                )
            subject_to_act_binding_occurrences[event.identity] = None
            continue
        if event.kind == SHARED_POSITION_APPLICABILITY_ACT_OCCURRENCE_EVENT:
            _read_shared_position_applicability_act(
                ledger,
                event.identity,
                prior_coordinates=addressed_byte_reference_prior_coordinates,
            )
            continue
        if event.kind == SHARED_POSITION_APPLICABILITY_RESULT_KIND:
            _read_shared_position_applicability_result(
                ledger,
                event.identity,
                prior_coordinates=addressed_byte_reference_prior_coordinates,
            )
            applicability_result_occurrences[event.identity] = None
            continue
        if event.kind == SHARED_POSITION_MEASUREMENT_ACT_OCCURRENCE_EVENT:
            _read_shared_position_measurement_act(
                ledger,
                event.identity,
                prior_coordinates=addressed_byte_reference_prior_coordinates,
            )
            continue
        if (
            event.kind
            == RECORDED_PAIR_MEASUREMENT_COMPARISON_SUBJECT_TO_ACT_BINDING_KIND
        ):
            _recorded_pair_comparison_binding_reading(
                ledger,
                event.identity,
                prior_coordinates=pair_prior_coordinates,
            )
            subject_to_act_binding_occurrences[event.identity] = None
            continue
        if (
            event.kind
            == RECORDED_PAIR_MEASUREMENT_COMPARISON_APPLICABILITY_ACT_OCCURRENCE_EVENT
        ):
            _recorded_pair_comparison_applicability_act_reading(
                ledger,
                event.identity,
                prior_coordinates=pair_prior_coordinates,
            )
            continue
        if (
            event.kind
            == RECORDED_PAIR_MEASUREMENT_COMPARISON_APPLICABILITY_RESULT_KIND
        ):
            _recorded_pair_comparison_applicability_reading(
                ledger,
                event.identity,
                prior_coordinates=pair_prior_coordinates,
            )
            applicability_result_occurrences[event.identity] = None
            continue
        if event.kind == RECORDED_PAIR_MEASUREMENT_COMPARISON_ACT_OCCURRENCE_EVENT:
            _recorded_pair_comparison_act_reading(
                ledger,
                event.identity,
                prior_coordinates=pair_prior_coordinates,
            )
            continue
        if event.kind == RECORDED_PAIR_MEASUREMENT_COMPARISON_RESULT_KIND:
            _recorded_pair_measurement_comparison_reading(
                ledger,
                event.identity,
                prior_coordinates=pair_prior_coordinates,
            )
            comparison_result_occurrences[event.identity] = None
            continue
        if event.kind == COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_SUBJECT_TO_ACT_BINDING_KIND:
            _ordered_relation_path_compare_binding_reading(
                ledger,
                event.identity,
                prior_coordinates=pair_prior_coordinates,
            )
            subject_to_act_binding_occurrences[event.identity] = None
            continue
        if event.kind == COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_APPLICABILITY_SUBJECT_TO_ACT_BINDING_KIND:
            _ordered_relation_path_compare_applicability_binding_reading(
                ledger,
                event.identity,
                prior_coordinates=pair_prior_coordinates,
            )
            subject_to_act_binding_occurrences[event.identity] = None
            continue
        if event.kind == COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_APPLICABILITY_ACT_OCCURRENCE_EVENT:
            _ordered_relation_path_compare_applicability_act_reading(
                ledger,
                event.identity,
                prior_coordinates=pair_prior_coordinates,
            )
            continue
        if event.kind == COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_APPLICABILITY_RESULT_KIND:
            _ordered_relation_path_compare_applicability_result_reading(
                ledger,
                event.identity,
                prior_coordinates=pair_prior_coordinates,
            )
            applicability_result_occurrences[event.identity] = None
            continue
        if event.kind == COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_COMPARE_ACT_OCCURRENCE_EVENT:
            _ordered_relation_path_compare_act_reading(
                ledger,
                event.identity,
                prior_coordinates=pair_prior_coordinates,
            )
            continue
        if event.kind == COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_RESULT_KIND:
            get_recorded_comparison_of_ordered_relation_path_with_recorded_pair_findings(
                ledger,
                event.identity,
                prior_coordinates=pair_prior_coordinates,
            )
            comparison_result_occurrences[event.identity] = None
            continue
        if event.kind == COMPARE_DISTINCTION_MEASUREMENT_SUBJECT_TO_ACT_BINDING_KIND:
            _read_compare_distinction_measurement_binding(
                ledger,
                event.identity,
                prior_coordinates=pair_prior_coordinates,
            )
            subject_to_act_binding_occurrences[event.identity] = None
            continue
        if event.kind == COMPARE_DISTINCTION_MEASUREMENT_ACT_OCCURRENCE_KIND:
            _read_compare_distinction_measurement_act(
                ledger,
                event.identity,
                prior_coordinates=pair_prior_coordinates,
            )
            continue
        if event.kind == COMPARE_DISTINCTION_MEASUREMENT_RESULT_KIND:
            get_recorded_compare_distinction_measurement(
                ledger,
                event.identity,
                prior_coordinates=pair_prior_coordinates,
            )
            measurement_occurrences[event.identity] = (
                _measurement_occurrence_coordinates(event)
            )
            continue
        if event.kind in _ORDERED_PATH_SOURCE_POSITION_MATERIAL_COMPARISON_KINDS:
            validate_ordered_path_source_position_material_comparison_event(
                ledger,
                event.identity,
                current_coordinates=pair_prior_coordinates,
            )
            if event.kind in {
                ORDERED_PATH_SOURCE_POSITION_COMPARE_BINDING_EVENT,
                ORDERED_PATH_SOURCE_POSITION_COMPARE_APPLICABILITY_BINDING_EVENT,
            }:
                subject_to_act_binding_occurrences[event.identity] = None
            elif (
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
            )
            if event.kind in {
                COMPARE_APPLICABILITY_SUBJECT_TO_ACT_BINDING_RECORDED_EVENT,
                COMPARE_SUBJECT_TO_ACT_BINDING_RECORDED_EVENT,
                SOURCE_POSITION_MEASUREMENT_SUBJECT_TO_ACT_BINDING_RECORDED_EVENT,
                RECURRENCE_MEASUREMENT_SUBJECT_TO_ACT_BINDING_RECORDED_EVENT,
                COORDINATE_MEASUREMENT_SUBJECT_TO_ACT_BINDING_RECORDED_EVENT,
                RECURRENT_RESULT_MATERIAL_MEASUREMENT_SUBJECT_TO_ACT_BINDING_RECORDED_EVENT,
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
            locality_continuation_relation_occurrences[event.identity] = None
            continue
        if event.kind == BYTE_MEASUREMENT_RECORDED_KIND:
            assertions_of_recorded_byte_measurement(
                ledger,
                event.identity,
                prior_coordinates=pair_prior_coordinates,
            )
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
                prior_coordinates={
                    "locality_identity": locality_identity,
                    "through_event_occurrence_identity": (
                        prior_through_event_occurrence_identity
                    ),
                    "measurement_occurrences": measurement_occurrences,
                    "material_result_occurrences": material_result_occurrences,
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
            _read_shared_position_measurement_result(
                ledger,
                event.identity,
                prior_coordinates=addressed_byte_reference_prior_coordinates,
            )
            measurement_occurrences[event.identity] = {
                "recorded_occurrence_identity": event.identity,
                "result_identity": event.material["result_identity"],
                "act_occurrence_identity": event.material[
                    "act_occurrence_identity"
                ],
                "act_occurrence_event_identity": event.material[
                    "act_occurrence_event_identity"
                ],
            }
            continue
        if event.kind == BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND:
            get_recorded_byte_pair_occurrence_position_measurement(
                ledger,
                event.identity,
                prior_coordinates=pair_prior_coordinates,
            )
            measurement_occurrences[event.identity] = (
                _measurement_occurrence_coordinates(event)
            )
            continue
        if event.kind == ADDRESSED_BYTE_REFERENCE_DETERMINATION_RESULT_KIND:
            _read_addressed_byte_reference_determination_result(
                ledger,
                event.identity,
                prior_coordinates=addressed_byte_reference_prior_coordinates,
            )
            measurement_occurrences[event.identity] = (
                _addressed_byte_reference_determination_coordinates(event)
            )
            continue
        source_result = read_exact_material_result(
            ledger, event.identity
        )
        material_result_reference = source_result.material["result_identity"]
        occurrence = {
            "subject_reference": material_result_reference,
            "result_occurrence_identity": source_result.identity,
        }
        material_result_occurrences.append(occurrence)

    return {
        "locality_identity": locality_identity,
        "through_event_occurrence_identity": through_event_occurrence_identity,
        "event_count": event_count,
        "material_result_occurrences": material_result_occurrences,
        "measurement_occurrences": measurement_occurrences,
        "assertion_locality_movement_occurrences": (
            assertion_locality_movement_occurrences
        ),
        "exact_result_occurrences": exact_result_occurrences,
        "locality_continuation_relation_occurrences": (
            locality_continuation_relation_occurrences
        ),
        "recorded_through_occurrence_boundary_references": (
            recorded_through_occurrence_boundary_references
        ),
        "recorded_boundary_locality_relations": (
            recorded_boundary_locality_relations
        ),
        "operator_destination_locality_relations": (
            operator_destination_locality_relations
        ),
        "subject_to_act_binding_occurrences": (
            subject_to_act_binding_occurrences
        ),
        "operator_material_source_act_occurrences": (
            operator_material_source_act_occurrences
        ),
        "applicability_result_occurrences": applicability_result_occurrences,
        "comparison_result_occurrences": comparison_result_occurrences,
    }


def _carry_byte_measurement_binding_into_current_coordinates(
    ledger: EventLedger,
    current_coordinates: dict[str, Any],
    event,
    *,
    prior_through_event_occurrence_identity: str,
    through_occurrence_coordinates: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Carry the exact-byte binding produced beside these coordinates."""

    if (
        type(current_coordinates) is not dict
        or current_coordinates.get("locality_identity") != event.locality_identity
        or current_coordinates.get("through_event_occurrence_identity")
        != prior_through_event_occurrence_identity
        or event.identity == prior_through_event_occurrence_identity
        or ledger.get(event.identity) != event
        or ledger.append_boundary_through_occurrence(event.identity)
        != ledger.append_boundary()
    ):
        raise ValueError(
            "byte Measurement binding is not recorded from the supplied current coordinates"
        )
    _read_byte_measurement_subject_to_act_binding(
        ledger,
        event.identity,
        prior_coordinates=(
            current_coordinates
            if through_occurrence_coordinates is None
            else through_occurrence_coordinates
        ),
    )
    bindings = current_coordinates.get("subject_to_act_binding_occurrences")
    event_count = current_coordinates.get("event_count")
    if (
        type(bindings) is not dict
        or event.identity in bindings
        or type(event_count) is not int
        or event_count < 0
    ):
        raise ValueError("byte Measurement binding coordinates are not exact")
    bindings[event.identity] = None
    current_coordinates["through_event_occurrence_identity"] = event.identity
    current_coordinates["event_count"] = event_count + 1
    return current_coordinates


def _carry_assertion_locality_movement_binding_into_current_coordinates(
    ledger: EventLedger,
    current_coordinates: dict[str, Any],
    event,
    *,
    source: dict[str, Any],
    source_event,
    source_current_coordinates: dict[str, Any],
) -> dict[str, Any]:
    """Carry one movement binding produced from exact carried coordinates."""

    bindings = (
        current_coordinates.get("subject_to_act_binding_occurrences")
        if type(current_coordinates) is dict
        else None
    )
    event_count = (
        current_coordinates.get("event_count")
        if type(current_coordinates) is dict
        else None
    )
    source_boundary = (
        source_current_coordinates.get("through_event_occurrence_identity")
        if type(source_current_coordinates) is dict
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
        expected = _movement_binding_material(
            source=source,
            source_assertion_coordinates=_source_assertion_coordinates(
                ledger, source
            ),
            source_event=source_event,
            source_locality=source_event.locality_identity,
            destination_locality=event.locality_identity,
            source_through_event_occurrence_identity=source_boundary,
            destination_through_event_occurrence_identity=(
                current_coordinates.get("through_event_occurrence_identity")
                if type(current_coordinates) is dict
                else None
            ),
            **identities,
        )
    if (
        type(current_coordinates) is not dict
        or event.kind
        != ASSERTION_LOCALITY_MOVEMENT_SUBJECT_TO_ACT_BINDING_KIND
        or ledger.get(event.identity) != event
        or ledger.integrity_of(event.identity) == CORRUPTED
        or source_event is None
        or current_source != source
        or current_source_event != source_event
        or type(source_current_coordinates) is not dict
        or ledger.get(source_event.identity) != source_event
        or ledger.integrity_of(source_event.identity) == CORRUPTED
        or _source_assertion_reference(source).get("recorded_occurrence_identity")
        != source_event.identity
        or source_event.locality_identity != event.material.get("source_locality")
        or source_current_coordinates.get("locality_identity")
        != source_event.locality_identity
        or not _source_assertion_is_carried(
            source_event, source_current_coordinates
        )
        or event.locality_identity
        != current_coordinates.get("locality_identity")
        or event.material != expected
        or type(bindings) is not dict
        or event.identity in bindings
        or type(event_count) is not int
        or event_count < 0
        or ledger.append_boundary_through_occurrence(event.identity)
        != ledger.append_boundary()
    ):
        raise ValueError("Assertion movement binding coordinates are not exact")
    bindings[event.identity] = None
    current_coordinates["through_event_occurrence_identity"] = event.identity
    current_coordinates["event_count"] = event_count + 1
    return current_coordinates


def _carry_assertion_locality_movement_act_into_current_coordinates(
    ledger: EventLedger,
    current_coordinates: dict[str, Any],
    event,
    *,
    binding,
) -> dict[str, Any]:
    """Carry the exact movement Act produced from the binding."""

    bindings = (
        current_coordinates.get("subject_to_act_binding_occurrences")
        if type(current_coordinates) is dict
        else None
    )
    event_count = (
        current_coordinates.get("event_count")
        if type(current_coordinates) is dict
        else None
    )
    try:
        _require_exact_movement_binding_and_source(ledger, binding)
        expected = _movement_act_material(binding)
        ledger.occurrences_in_append_order(
            (binding.identity, event.identity),
            locality_identity=event.locality_identity,
        )
    except (AttributeError, TypeError, ValueError) as error:
        raise ValueError("Assertion movement Act coordinates are not exact") from error
    if (
        type(current_coordinates) is not dict
        or binding.kind
        != ASSERTION_LOCALITY_MOVEMENT_SUBJECT_TO_ACT_BINDING_KIND
        or ledger.get(binding.identity) != binding
        or ledger.integrity_of(binding.identity) == CORRUPTED
        or event.kind != ASSERTION_LOCALITY_MOVEMENT_ACT_OCCURRENCE_EVENT
        or ledger.get(event.identity) != event
        or ledger.integrity_of(event.identity) == CORRUPTED
        or event.locality_identity != binding.locality_identity
        or event.material != expected
        or current_coordinates.get("locality_identity") != event.locality_identity
        or current_coordinates.get("through_event_occurrence_identity")
        != binding.identity
        or type(bindings) is not dict
        or bindings.get(binding.identity, object()) is not None
        or type(event_count) is not int
        or event_count < 0
        or ledger.append_boundary_through_occurrence(event.identity)
        != ledger.append_boundary()
    ):
        raise ValueError("Assertion movement Act coordinates are not exact")
    current_coordinates["through_event_occurrence_identity"] = event.identity
    current_coordinates["event_count"] = event_count + 1
    return current_coordinates


def _carry_assertion_locality_movement_result_into_current_coordinates(
    ledger: EventLedger,
    current_coordinates: dict[str, Any],
    event,
    *,
    act_occurrence,
    binding,
    source: dict[str, Any],
) -> tuple[
    dict[str, Any],
    dict[str, Any],
]:
    """Carry one exact movement result and its already-carried source."""

    bindings = (
        current_coordinates.get("subject_to_act_binding_occurrences")
        if type(current_coordinates) is dict
        else None
    )
    movements = (
        current_coordinates.get("assertion_locality_movement_occurrences")
        if type(current_coordinates) is dict
        else None
    )
    event_count = (
        current_coordinates.get("event_count")
        if type(current_coordinates) is dict
        else None
    )
    yield_relation_identity = event.material.get("yield_relation_identity")
    yield_relation = ledger.get(yield_relation_identity) if type(yield_relation_identity) is str else None
    try:
        current_source, current_source_event = _source_assertion_from_reference(
            ledger, _source_assertion_reference(source)
        )
        expected_act = _movement_act_material(binding)
        expected = {
            **_movement_result_material(binding),
            "act_occurrence_event_identity": act_occurrence.identity,
            "yield_relation_identity": yield_relation_identity,
        }
        requirements = read_requirements_of_yield_relation(
            ledger,
            recorded_result_event_identity=event.identity,
            yield_relation_event_identity=yield_relation_identity,
            act_occurrence_event_identity=act_occurrence.identity,
            recorded_result_occurrence_coordinate="movement_act_occurrence_identity",
            yielding_act_occurrence_coordinate="movement_act_occurrence_identity",
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
        raise ValueError("Assertion movement result coordinates are not exact") from error
    if (
        type(current_coordinates) is not dict
        or binding.kind
        != ASSERTION_LOCALITY_MOVEMENT_SUBJECT_TO_ACT_BINDING_KIND
        or ledger.get(binding.identity) != binding
        or ledger.integrity_of(binding.identity) == CORRUPTED
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
        or event.locality_identity != binding.locality_identity
        or event.material != expected
        or binding.material.get("source_assertion_reference")
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
        or current_coordinates.get("locality_identity") != event.locality_identity
        or current_coordinates.get("through_event_occurrence_identity")
        != act_occurrence.identity
        or type(bindings) is not dict
        or bindings.get(binding.identity, object()) is not None
        or type(movements) is not dict
        or event.identity in movements
        or type(event_count) is not int
        or event_count < 0
        or ledger.append_boundary_through_occurrence(event.identity)
        != ledger.append_boundary()
    ):
        raise ValueError("Assertion movement result coordinates are not exact")
    exact = _assertion_carried_by_locality_movement_result(
        movement=event,
        binding=binding,
        source=source,
    )
    movements[event.identity] = _assertion_locality_movement_occurrence_coordinates(
        ledger, event
    )
    current_coordinates["through_event_occurrence_identity"] = event.identity
    current_coordinates["event_count"] = event_count + 1
    return current_coordinates, exact


def _carry_occurrence_position_measurement_binding_into_current_coordinates(
    ledger: EventLedger,
    current_coordinates: dict[str, Any],
    event,
    finding,
    *,
    prior_through_event_occurrence_identity: str,
) -> dict[str, Any]:
    """Carry the occurrence-position binding into current coordinates."""

    if (
        type(current_coordinates) is not dict
        or current_coordinates.get("locality_identity") != event.locality_identity
        or current_coordinates.get("through_event_occurrence_identity")
        != prior_through_event_occurrence_identity
    ):
        raise ValueError(
            "occurrence position binding must follow its carried finding"
        )
    _require_carried_occurrence_position_binding(
        ledger,
        binding=event,
        finding=finding,
    )
    bindings = current_coordinates.get("subject_to_act_binding_occurrences")
    event_count = current_coordinates.get("event_count")
    if (
        type(bindings) is not dict
        or event.identity in bindings
        or type(event_count) is not int
        or event_count < 0
    ):
        raise ValueError("occurrence position binding coordinates are not exact")
    bindings[event.identity] = None
    current_coordinates["through_event_occurrence_identity"] = event.identity
    current_coordinates["event_count"] = event_count + 1
    return current_coordinates


def _carry_occurrence_position_measurement_result_into_current_coordinates(
    ledger: EventLedger,
    current_coordinates: dict[str, Any],
    event,
    *,
    act_occurrence,
    binding,
    finding,
) -> dict[str, Any]:
    """Carry the occurrence-position result produced by its exact Act."""

    measurements = (
        current_coordinates.get("measurement_occurrences")
        if type(current_coordinates) is dict
        else None
    )
    bindings = (
        current_coordinates.get("subject_to_act_binding_occurrences")
        if type(current_coordinates) is dict
        else None
    )
    event_count = (
        current_coordinates.get("event_count")
        if type(current_coordinates) is dict
        else None
    )
    assertions = _position_assertions(finding)
    result_material = _occurrence_position_result_material(
        finding,
        binding=binding,
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
        or event.locality_identity != binding.locality_identity
        or event.material != expected
        or current_coordinates.get("locality_identity") != event.locality_identity
        or current_coordinates.get("through_event_occurrence_identity")
        != act_occurrence.identity
        or type(measurements) is not dict
        or event.identity in measurements
        or type(bindings) is not dict
        or binding.identity not in bindings
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
        raise ValueError("occurrence position Measurement coordinates are not exact")
    measurements[event.identity] = _measurement_occurrence_coordinates(event)
    current_coordinates["through_event_occurrence_identity"] = event.identity
    current_coordinates["event_count"] = event_count + 1
    return current_coordinates


def _carry_validated_pair_measurement_lifecycle_occurrence_into_current_coordinates(
    ledger: EventLedger,
    current_coordinates: dict[str, Any],
    event,
    *,
    prior_through_event_occurrence_identity: str,
    destination_coordinate: str | None,
) -> dict[str, Any]:
    if (
        type(current_coordinates) is not dict
        or ledger.get(event.identity) != event
        or ledger.integrity_of(event.identity) == CORRUPTED
        or event.locality_identity != current_coordinates.get("locality_identity")
        or current_coordinates.get("through_event_occurrence_identity")
        != prior_through_event_occurrence_identity
        or ledger.append_boundary_through_occurrence(event.identity)
        != ledger.append_boundary()
    ):
        raise ValueError("pair Measurement lifecycle coordinates are not exact")
    try:
        ledger.occurrences_in_append_order(
            (prior_through_event_occurrence_identity, event.identity),
            locality_identity=event.locality_identity,
        )
    except ValueError as error:
        raise ValueError(
            "pair Measurement lifecycle coordinate order is not exact"
        ) from error
    destination = (
        current_coordinates[destination_coordinate]
        if destination_coordinate is not None
        else None
    )
    event_count = current_coordinates.get("event_count")
    if (
        type(event_count) is not int
        or event_count < 0
        or (destination is not None and event.identity in destination)
    ):
        raise ValueError("pair Measurement lifecycle coordinates are not exact")
    if destination is current_coordinates["measurement_occurrences"]:
        destination[event.identity] = _measurement_occurrence_coordinates(event)
    elif destination is not None:
        destination[event.identity] = None
    current_coordinates["through_event_occurrence_identity"] = event.identity
    current_coordinates["event_count"] = event_count + 1
    return current_coordinates


def _carry_pair_applicability_binding_into_current_coordinates(
    ledger: EventLedger,
    current_coordinates: dict[str, Any],
    binding,
    source,
    *,
    prior_through_event_occurrence_identity: str,
) -> dict[str, Any]:
    _require_exact_pair_subject_to_act_binding_event(
        ledger,
        binding,
        source,
        prior_coordinates=current_coordinates,
    )
    return _carry_validated_pair_measurement_lifecycle_occurrence_into_current_coordinates(
        ledger,
        current_coordinates,
        binding,
        prior_through_event_occurrence_identity=prior_through_event_occurrence_identity,
        destination_coordinate="subject_to_act_binding_occurrences",
    )


def _carry_pair_measurement_binding_into_current_coordinates(
    ledger: EventLedger,
    current_coordinates: dict[str, Any],
    binding,
    source,
    *,
    prior_through_event_occurrence_identity: str,
) -> dict[str, Any]:
    _require_exact_pair_subject_to_act_binding_event(
        ledger,
        binding,
        source,
        prior_coordinates=current_coordinates,
    )
    return _carry_validated_pair_measurement_lifecycle_occurrence_into_current_coordinates(
        ledger,
        current_coordinates,
        binding,
        prior_through_event_occurrence_identity=prior_through_event_occurrence_identity,
        destination_coordinate="subject_to_act_binding_occurrences",
    )


def _carry_pair_applicability_act_into_current_coordinates(
    ledger: EventLedger,
    current_coordinates: dict[str, Any],
    event,
    *,
    binding,
    source,
    prior_through_event_occurrence_identity: str,
) -> dict[str, Any]:
    _require_exact_pair_applicability_act_event(
        ledger,
        event,
        binding=binding,
        source=source,
        prior_coordinates=current_coordinates,
    )
    return _carry_validated_pair_measurement_lifecycle_occurrence_into_current_coordinates(
        ledger,
        current_coordinates,
        event,
        prior_through_event_occurrence_identity=prior_through_event_occurrence_identity,
        destination_coordinate=None,
    )


def _carry_pair_applicability_result_into_current_coordinates(
    ledger: EventLedger,
    current_coordinates: dict[str, Any],
    event,
    *,
    binding,
    source,
    applicability_act_occurrence,
    prior_through_event_occurrence_identity: str,
) -> dict[str, Any]:
    _require_exact_pair_applicability_result_event(
        ledger,
        event,
        binding=binding,
        source=source,
        applicability_act_occurrence=applicability_act_occurrence,
        prior_coordinates=current_coordinates,
    )
    return _carry_validated_pair_measurement_lifecycle_occurrence_into_current_coordinates(
        ledger,
        current_coordinates,
        event,
        prior_through_event_occurrence_identity=prior_through_event_occurrence_identity,
        destination_coordinate="applicability_result_occurrences",
    )


def _carry_pair_measurement_act_into_current_coordinates(
    ledger: EventLedger,
    current_coordinates: dict[str, Any],
    event,
    *,
    binding,
    source,
    applicability_event,
    applicability_act_occurrence,
    prior_through_event_occurrence_identity: str,
) -> dict[str, Any]:
    _require_exact_pair_measurement_act_event(
        ledger,
        event,
        binding=binding,
        applicability_binding=_pair_applicability_binding_of_result(
            ledger,
            applicability_event,
            source=source,
            prior_coordinates=current_coordinates,
        ),
        source=source,
        applicability_event=applicability_event,
        applicability_act_occurrence=applicability_act_occurrence,
        prior_coordinates=current_coordinates,
    )
    return _carry_validated_pair_measurement_lifecycle_occurrence_into_current_coordinates(
        ledger,
        current_coordinates,
        event,
        prior_through_event_occurrence_identity=prior_through_event_occurrence_identity,
        destination_coordinate=None,
    )


def _carry_pair_measurement_result_into_current_coordinates(
    ledger: EventLedger,
    current_coordinates: dict[str, Any],
    event,
    *,
    act_occurrence,
    binding,
    source,
    applicability_event,
    applicability_act_occurrence,
    prior_through_event_occurrence_identity: str,
) -> dict[str, Any]:
    _require_exact_pair_measurement_result_event(
        ledger,
        event,
        act_occurrence=act_occurrence,
        binding=binding,
        source=source,
        applicability_event=applicability_event,
        applicability_act_occurrence=applicability_act_occurrence,
        prior_coordinates=current_coordinates,
    )
    exact_results = current_coordinates.get("exact_result_occurrences")
    exact_result = _subject_to_act_binding_of_exact_result(ledger, event)
    if (
        type(exact_results) is not dict
        or event.identity in exact_results
        or exact_result is None
    ):
        raise ValueError("pair Measurement result coordinates are not exact")
    current_coordinates = _carry_validated_pair_measurement_lifecycle_occurrence_into_current_coordinates(
        ledger,
        current_coordinates,
        event,
        prior_through_event_occurrence_identity=prior_through_event_occurrence_identity,
        destination_coordinate="measurement_occurrences",
    )
    exact_results[event.identity] = exact_result
    return current_coordinates


def _carry_byte_pair_occurrence_position_measurement_binding_into_current_coordinates(
    ledger: EventLedger,
    current_coordinates: dict[str, Any],
    event,
    finding,
    *,
    prior_through_event_occurrence_identity: str,
) -> dict[str, Any]:
    """Carry one byte-pair position binding into current coordinates."""

    if (
        type(current_coordinates) is not dict
        or current_coordinates.get("locality_identity") != event.locality_identity
        or current_coordinates.get("through_event_occurrence_identity")
        != prior_through_event_occurrence_identity
    ):
        raise ValueError(
            "byte-pair position binding requires its carried finding"
        )
    _require_carried_byte_pair_occurrence_position_subject_to_act_binding(
        ledger,
        binding=event,
        finding=finding,
    )
    bindings = current_coordinates.get("subject_to_act_binding_occurrences")
    event_count = current_coordinates.get("event_count")
    if (
        type(bindings) is not dict
        or event.identity in bindings
        or type(event_count) is not int
        or event_count < 0
    ):
        raise ValueError("byte-pair position binding coordinates are not exact")
    bindings[event.identity] = None
    current_coordinates["through_event_occurrence_identity"] = event.identity
    current_coordinates["event_count"] = event_count + 1
    return current_coordinates


def _carry_byte_pair_occurrence_position_measurement_result_into_current_coordinates(
    ledger: EventLedger,
    current_coordinates: dict[str, Any],
    event,
    *,
    prior_through_event_occurrence_identity: str,
) -> dict[str, Any]:
    """Carry the position-coordinate result produced by this console call."""

    if (
        type(current_coordinates) is not dict
        or event.kind != BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND
        or current_coordinates.get("locality_identity") != event.locality_identity
        or current_coordinates.get("through_event_occurrence_identity")
        != prior_through_event_occurrence_identity
    ):
        raise ValueError(
            "position-coordinate Measurement must follow its carried Act and Yield"
        )
    measurements = current_coordinates.get("measurement_occurrences")
    bindings = current_coordinates.get("subject_to_act_binding_occurrences")
    material_results = current_coordinates.get("material_result_occurrences")
    exact_results = current_coordinates.get("exact_result_occurrences")
    binding = event.material.get("subject_to_act_binding_reference")
    source_identity = event.material.get("source_material_result_occurrence_identity")
    event_count = current_coordinates.get("event_count")
    if (
        type(measurements) is not dict
        or type(bindings) is not dict
        or type(material_results) is not list
        or type(exact_results) is not dict
        or type(binding) is not dict
        or binding.get("recorded_occurrence_identity") not in bindings
        or event.material.get("act_occurrence_event_identity")
            != prior_through_event_occurrence_identity
        or not any(
            type(occurrence) is dict
            and occurrence.get("result_occurrence_identity") == source_identity
            for occurrence in material_results
        )
        or type(event.material.get("yield_relation_identity"))
        is not str
        or type(event.material.get("assertions")) is not dict
        or event.identity in measurements
        or event.identity in exact_results
        or type(event_count) is not int
        or event_count < 0
    ):
        raise ValueError("position-coordinate Measurement coordinates are not exact")
    exact_result = _subject_to_act_binding_of_exact_result(ledger, event)
    measurements[event.identity] = _measurement_occurrence_coordinates(event)
    exact_results[event.identity] = exact_result
    current_coordinates["through_event_occurrence_identity"] = event.identity
    current_coordinates["event_count"] = event_count + 1
    return current_coordinates


def _advance_current_coordinates_with_operator_material_source_occurrence(
    ledger: EventLedger,
    current_coordinates: dict[str, Any],
    event,
    *,
    prior_through_event_occurrence_identity: str,
) -> dict[str, Any]:
    """Advance current coordinates with one source occurrence from this console call."""

    if (
        type(current_coordinates) is not dict
        or event.kind not in _OPERATOR_MATERIAL_SOURCE_KINDS
        or current_coordinates.get("locality_identity") != event.locality_identity
        or current_coordinates.get("through_event_occurrence_identity")
        != prior_through_event_occurrence_identity
    ):
        raise ValueError("operator material source coordinates are not exact")
    bindings = current_coordinates.get("subject_to_act_binding_occurrences")
    acts = current_coordinates.get("operator_material_source_act_occurrences")
    material_result_occurrences = current_coordinates.get("material_result_occurrences")
    exact_results = current_coordinates.get("exact_result_occurrences")
    event_count = current_coordinates.get("event_count")
    if (
        type(bindings) is not dict
        or type(acts) is not dict
        or type(material_result_occurrences) is not list
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
        ):
            raise ValueError("operator material source result is not exact")
    exact_result = None
    material_result_coordinate = None
    if event.kind == OPERATOR_MATERIAL_SOURCE_RECORDED_KIND:
        exact_result = _subject_to_act_binding_of_exact_result(ledger, event)
        result_identity = event.material.get("result_identity")
        if (
            exact_result is None
            or type(result_identity) is not str
            or not result_identity
        ):
            raise ValueError("operator material source result is not exact")
        material_result_coordinate = {
            "subject_reference": result_identity,
            "result_occurrence_identity": event.identity,
        }
    if event.kind == OPERATOR_MATERIAL_SOURCE_SUBJECT_TO_ACT_BINDING_RECORDED_KIND:
        bindings[event.identity] = None
    elif event.kind == OPERATOR_MATERIAL_SOURCE_ACT_OCCURRENCE_EVENT:
        acts[event.identity] = None
    else:
        exact_results[event.identity] = exact_result
        material_result_occurrences.append(material_result_coordinate)
    current_coordinates["through_event_occurrence_identity"] = event.identity
    current_coordinates["event_count"] = event_count + 1
    return current_coordinates


def _carry_recorded_pair_comparison_occurrence_into_current_coordinates(
    ledger: EventLedger,
    current_coordinates: dict[str, Any],
    event,
    *,
    prior_through_event_occurrence_identity: str,
) -> dict[str, Any]:
    """Carry one pair-Compare occurrence produced by this console call."""

    carried_kinds = _RECORDED_PAIR_MEASUREMENT_COMPARISON_KINDS
    if (
        type(current_coordinates) is not dict
        or event.kind not in carried_kinds
        or current_coordinates.get("locality_identity") != event.locality_identity
        or current_coordinates.get("through_event_occurrence_identity")
        != prior_through_event_occurrence_identity
    ):
        raise ValueError("recorded pair comparison coordinates are not exact")
    bindings = current_coordinates.get("subject_to_act_binding_occurrences")
    applicability = current_coordinates.get("applicability_result_occurrences")
    comparisons = current_coordinates.get("comparison_result_occurrences")
    event_count = current_coordinates.get("event_count")
    if (
        type(bindings) is not dict
        or type(applicability) is not dict
        or type(comparisons) is not dict
        or type(event_count) is not int
        or event_count < 0
    ):
        raise ValueError("recorded pair comparison coordinates are not exact")
    if event.kind == RECORDED_PAIR_MEASUREMENT_COMPARISON_SUBJECT_TO_ACT_BINDING_KIND:
        measurements = current_coordinates.get("measurement_occurrences")
        earlier = event.material.get("earlier_measurement_reference")
        later = event.material.get("later_measurement_reference")
        if (
            type(measurements) is not dict
            or type(earlier) is not dict
            or type(later) is not dict
            or earlier.get("recorded_occurrence_identity") not in measurements
            or later.get("recorded_occurrence_identity") not in measurements
            or event.material.get("through_event_occurrence_identity")
            != prior_through_event_occurrence_identity
            or event.identity in bindings
        ):
            raise ValueError("recorded pair comparison binding is not exact")
    elif (
        event.kind
        == RECORDED_PAIR_MEASUREMENT_COMPARISON_APPLICABILITY_SUBJECT_TO_ACT_BINDING_KIND
    ):
        applicability_binding, _inputs, comparison_binding_reading = (
            _recorded_pair_comparison_applicability_binding_reading(
                ledger,
                event.identity,
                prior_coordinates=current_coordinates,
            )
        )
        comparison_binding = comparison_binding_reading[0]
        if (
            applicability_binding is not event
            or comparison_binding.identity not in bindings
            or event.material.get("through_event_occurrence_identity")
            != prior_through_event_occurrence_identity
            or event.identity in bindings
        ):
            raise ValueError(
                "recorded pair comparison Applicability binding is not exact"
            )
    elif event.kind == RECORDED_PAIR_MEASUREMENT_COMPARISON_APPLICABILITY_ACT_OCCURRENCE_EVENT:
        binding = event.material.get("subject_to_act_binding_reference")
        if (
            type(binding) is not dict
            or binding.get("recorded_occurrence_identity")
            != prior_through_event_occurrence_identity
            or prior_through_event_occurrence_identity not in bindings
        ):
            raise ValueError(
                "recorded pair comparison Applicability Act is not exact"
            )
    elif event.kind == RECORDED_PAIR_MEASUREMENT_COMPARISON_APPLICABILITY_RESULT_KIND:
        binding = event.material.get("subject_to_act_binding_reference")
        if (
            type(binding) is not dict
            or binding.get("recorded_occurrence_identity") not in bindings
            or event.material.get("act_occurrence_event_identity")
            != prior_through_event_occurrence_identity
            or event.material.get("applicability") != "applicable"
            or event.identity in applicability
        ):
            raise ValueError("recorded pair comparison Applicability is not exact")
    elif event.kind == RECORDED_PAIR_MEASUREMENT_COMPARISON_ACT_OCCURRENCE_EVENT:
        binding = event.material.get("subject_to_act_binding_reference")
        if (
            type(binding) is not dict
            or binding.get("recorded_occurrence_identity") not in bindings
            or event.material.get("applicability_result_event_identity")
            != prior_through_event_occurrence_identity
            or prior_through_event_occurrence_identity not in applicability
        ):
            raise ValueError("recorded pair comparison Act is not exact")
    else:
        binding = event.material.get("subject_to_act_binding_reference")
        if (
            type(binding) is not dict
            or binding.get("recorded_occurrence_identity") not in bindings
            or event.material.get("act_occurrence_event_identity")
            != prior_through_event_occurrence_identity
            or event.material.get("applicability_result_event_identity")
            not in applicability
            or event.identity in comparisons
        ):
            raise ValueError("recorded pair comparison result is not exact")
    if event.kind in {
        RECORDED_PAIR_MEASUREMENT_COMPARISON_SUBJECT_TO_ACT_BINDING_KIND,
        RECORDED_PAIR_MEASUREMENT_COMPARISON_APPLICABILITY_SUBJECT_TO_ACT_BINDING_KIND,
    }:
        bindings[event.identity] = None
    elif event.kind == RECORDED_PAIR_MEASUREMENT_COMPARISON_APPLICABILITY_RESULT_KIND:
        applicability[event.identity] = None
    elif event.kind == RECORDED_PAIR_MEASUREMENT_COMPARISON_RESULT_KIND:
        comparisons[event.identity] = None
    current_coordinates["through_event_occurrence_identity"] = event.identity
    current_coordinates["event_count"] = event_count + 1
    return current_coordinates
