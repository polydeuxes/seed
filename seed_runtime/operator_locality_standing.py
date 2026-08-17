"""Deterministic Locality Standing read over preserved ingest events."""

from __future__ import annotations


from bisect import bisect_left
from copy import deepcopy
from typing import Any, Iterable

from seed_runtime.events import CORRUPTED, EventLedger
from seed_runtime.material_ingest import MATERIAL_INGEST_OCCURRED_KIND
from seed_runtime.byte_measurement import (
    BYTE_MEASUREMENT_RECORDED_KIND,
    BYTE_MEASUREMENT_RESPONSIBLE_ACT_EVIDENCE_KIND,
    BYTE_PAIR_MEASUREMENT_RECORDED_KIND,
    _findings_of_recorded_byte_position_pair_measurement,
    assertions_of_recorded_byte_measurement,
)
from seed_runtime.occurrence_position_measurement import (
    OCCURRENCE_POSITION_ACT_EVIDENCE_KIND,
    OCCURRENCE_POSITION_RECORDED_KIND,
    get_recorded_occurrence_position_measurement,
)
from seed_runtime.measurement_of_recurrent_byte_pair_occurrence_position import (
    RECORDED_EVIDENCE_OF_ACT_OCCURRENCE_OF_MEASUREMENT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_KIND,
    RECORDING_OCCURRENCE_OF_RESULT_OF_MEASUREMENT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_KIND,
    get_recorded_result_of_measurement_of_recurrent_byte_pair_occurrence_position,
)
from seed_runtime.measurement_of_shared_position_of_recurrent_byte_pair_occurrences import (
    SHARED_POSITION_RESPONSIBILITY_ASSIGNMENT_KIND,
    SHARED_POSITION_APPLICABILITY_ACT_EVIDENCE_KIND,
    SHARED_POSITION_APPLICABILITY_RESULT_KIND,
    SHARED_POSITION_MEASUREMENT_ACT_EVIDENCE_KIND,
    SHARED_POSITION_MEASUREMENT_RESULT_KIND,
    get_shared_position_responsibility_assignment,
    get_shared_position_applicability_act_evidence,
    get_recorded_shared_position_applicability,
    get_shared_position_measurement_act_evidence,
    get_recorded_shared_position_measurement,
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
    get_recorded_pair_measurement_comparison_responsibility_assignment,
    get_recorded_pair_measurement_comparison_applicability_act_evidence,
    get_recorded_pair_measurement_comparison_applicability,
    get_recorded_pair_measurement_comparison_act_evidence,
    get_recorded_pair_measurement_comparison,
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
from seed_runtime.evidence_of_yield_relation import read_requirements_of_yield_relation

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

_SUBJECT_BY_KIND = {
    MATERIAL_INGEST_OCCURRED_KIND: "ingest_occurrence",
}
_MEASUREMENT_ACT_EVIDENCE_KINDS = {
    BYTE_MEASUREMENT_RESPONSIBLE_ACT_EVIDENCE_KIND,
    OCCURRENCE_POSITION_ACT_EVIDENCE_KIND,
    RECORDED_EVIDENCE_OF_ACT_OCCURRENCE_OF_MEASUREMENT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_KIND,
}
_MEASUREMENT_RECORDED_KINDS = {
    BYTE_MEASUREMENT_RECORDED_KIND,
    BYTE_PAIR_MEASUREMENT_RECORDED_KIND,
    OCCURRENCE_POSITION_RECORDED_KIND,
    RECORDING_OCCURRENCE_OF_RESULT_OF_MEASUREMENT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_KIND,
    SHARED_POSITION_MEASUREMENT_RESULT_KIND,
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
    *_MEASUREMENT_RECORDED_KINDS,
    *_STANDING_LOCALITY_CONTINUATION_KINDS,
    *_STANDING_BOUNDARY_REFERENCE_KINDS,
    *_RECORDED_STANDING_BOUNDARY_LOCALITY_KINDS,
    *_OPERATOR_MATERIAL_ACQUIRE_KINDS,
    *_OPERATOR_SYSTEM_LOCALITY_KINDS,
    *_REPRESENTATION_CANDIDATE_ADMISSION_KINDS,
    *_REPRESENTATION_EMISSION_APPLICABILITY_KINDS,
    *_RECORDED_PAIR_MEASUREMENT_COMPARISON_KINDS,
    *_SHARED_POSITION_MEASUREMENT_KINDS,
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
    """Whether this exact occurrence's intact Yield carries raw result bytes."""

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


def read_operator_locality_standing(
    ledger: EventLedger, *, locality_identity: str
) -> dict[str, Any]:
    """Project bounded Locality-local Standing by replaying the whole Locality.

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


def read_operator_locality_standing_as_of(
    ledger: EventLedger,
    *,
    locality_identity: str,
    as_of_event_identity: str | None,
) -> dict[str, Any]:
    """Project one Locality through one exact recorded occurrence.

    ``None`` is the exact empty Standing boundary.  Otherwise the ledger first
    resolves the occurrence to its existing append boundary and then reads only
    that prefix.  Later occurrences in the same or another Locality are neither
    selected nor copied into the returned projection.
    """

    if type(locality_identity) is not str or not locality_identity:
        raise ValueError("Standing read requires one exact Locality identity")
    if as_of_event_identity is None:
        event_identities: Iterable[str] = ()
    else:
        if type(as_of_event_identity) is not str or not as_of_event_identity:
            raise ValueError("Standing read requires one exact as-of occurrence")
        event = ledger.get(as_of_event_identity)
        if (
            event is None
            or event.locality_identity != locality_identity
            or ledger.integrity_of(as_of_event_identity) == CORRUPTED
        ):
            raise ValueError(
                "Standing as-of occurrence is absent, corrupted, or in another Locality"
            )
        boundary = ledger.append_boundary_through_occurrence(
            as_of_event_identity
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
    if standing["as_of_event_identity"] != as_of_event_identity:
        raise ValueError("Standing read did not reach its exact as-of occurrence")
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
        "source_standing_as_of_event_identity": source[
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
        ("continuation", locality_standing["recorded_relation_standings"]),
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
    as_of_event_identity = source_reference.get(
        "source_standing_as_of_event_identity"
    )
    if as_of_event_identity is not None:
        _require_recorded_standing_identity(
            as_of_event_identity,
            "recorded Standing reference carries no exact Standing boundary",
        )
    standing = read_operator_locality_standing_as_of(
        ledger,
        locality_identity=source_locality_identity,
        as_of_event_identity=as_of_event_identity,
    )
    return {
        "recorded_occurrence_identity": recorded_occurrence_identity,
        "source_standing_reference": source_reference,
        "standing": standing,
    }


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
    earlier Standing to stay as it was must project it again; there is no
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
    recorded_relation_standings: dict[str, None] = {}
    recorded_standing_boundary_references: dict[str, None] = {}
    recorded_standing_boundary_locality_relations: dict[str, None] = {}
    operator_invocation_locality_relations: dict[str, None] = {}
    responsibility_assignment_occurrences: dict[str, None] = {}
    operator_material_acquire_act_occurrences: dict[str, None] = {}
    candidate_result_occurrences: dict[str, None] = {}
    admission_result_occurrences: dict[str, None] = {}
    applicability_result_occurrences: dict[str, None] = {}
    comparison_result_occurrences: dict[str, None] = {}
    # Kept sorted and distinct in place rather than as a set sorted on return.
    # A set would have to be rebuilt from the prior list and re-sorted on every
    # advance, which costs the accumulated size each time.  These coordinates
    # do not grow on the five live kinds today, but acquisition would make them
    # grow, and the prior-transfer rule has to hold for every accumulator that
    # can.
    known_loss: list[str] = []
    unknown: list[str] = []
    conflicts: list[str] = []
    as_of_event_identity: str | None = None
    event_count = 0

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
        recorded_relation_standings = prior["recorded_relation_standings"]
        if type(recorded_relation_standings) is not dict:
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
        as_of_event_identity = prior["as_of_event_identity"]
        event_count = prior["event_count"]

    for event in events:
        if event.locality_identity != locality_identity:
            continue
        if not (
            event.kind == MATERIAL_INGEST_OCCURRED_KIND
            or event.kind.startswith("operator.representation.")
            or event.kind in _MEASUREMENT_ACT_EVIDENCE_KINDS
            or event.kind in _MEASUREMENT_RECORDED_KINDS
            or event.kind in _STANDING_LOCALITY_CONTINUATION_KINDS
            or event.kind in _STANDING_BOUNDARY_REFERENCE_KINDS
            or event.kind in _RECORDED_STANDING_BOUNDARY_LOCALITY_KINDS
            or event.kind in _OPERATOR_MATERIAL_ACQUIRE_KINDS
            or event.kind in _OPERATOR_SYSTEM_LOCALITY_KINDS
            or event.kind in _REPRESENTATION_CANDIDATE_ADMISSION_KINDS
            or event.kind in _REPRESENTATION_EMISSION_APPLICABILITY_KINDS
            or event.kind in _RECORDED_PAIR_MEASUREMENT_COMPARISON_KINDS
            or event.kind in _SHARED_POSITION_MEASUREMENT_KINDS
            or event.kind in _COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_KINDS
        ):
            continue
        if event.kind not in _SUPPORTED_KINDS:
            raise ValueError(f"unsupported operator-ingest event: {event.kind}")
        event_count += 1
        as_of_event_identity = event.identity
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
        if event.kind == SHARED_POSITION_RESPONSIBILITY_ASSIGNMENT_KIND:
            get_shared_position_responsibility_assignment(
                ledger, event.identity
            )
            responsibility_assignment_occurrences[event.identity] = None
            continue
        if event.kind == SHARED_POSITION_APPLICABILITY_ACT_EVIDENCE_KIND:
            get_shared_position_applicability_act_evidence(
                ledger, event.identity
            )
            continue
        if event.kind == SHARED_POSITION_APPLICABILITY_RESULT_KIND:
            get_recorded_shared_position_applicability(ledger, event.identity)
            applicability_result_occurrences[event.identity] = None
            continue
        if event.kind == SHARED_POSITION_MEASUREMENT_ACT_EVIDENCE_KIND:
            get_shared_position_measurement_act_evidence(
                ledger, event.identity
            )
            continue
        if (
            event.kind
            == RECORDED_PAIR_MEASUREMENT_COMPARISON_RESPONSIBILITY_ASSIGNMENT_KIND
        ):
            get_recorded_pair_measurement_comparison_responsibility_assignment(
                ledger, event.identity
            )
            responsibility_assignment_occurrences[event.identity] = None
            continue
        if (
            event.kind
            == RECORDED_PAIR_MEASUREMENT_COMPARISON_APPLICABILITY_ACT_EVIDENCE_KIND
        ):
            get_recorded_pair_measurement_comparison_applicability_act_evidence(
                ledger, event.identity
            )
            continue
        if (
            event.kind
            == RECORDED_PAIR_MEASUREMENT_COMPARISON_APPLICABILITY_RESULT_KIND
        ):
            get_recorded_pair_measurement_comparison_applicability(
                ledger, event.identity
            )
            applicability_result_occurrences[event.identity] = None
            continue
        if event.kind == RECORDED_PAIR_MEASUREMENT_COMPARISON_ACT_EVIDENCE_KIND:
            get_recorded_pair_measurement_comparison_act_evidence(
                ledger, event.identity
            )
            continue
        if event.kind == RECORDED_PAIR_MEASUREMENT_COMPARISON_RESULT_KIND:
            get_recorded_pair_measurement_comparison(ledger, event.identity)
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
            recorded_relation_standings[event.identity] = None
            continue
        if event.kind == BYTE_MEASUREMENT_RECORDED_KIND:
            assertions_of_recorded_byte_measurement(ledger, event.identity)
            measurement_occurrences[event.identity] = (
                _measurement_occurrence_coordinates(event)
            )
            continue
        if event.kind == BYTE_PAIR_MEASUREMENT_RECORDED_KIND:
            _findings_of_recorded_byte_position_pair_measurement(
                ledger, event.identity
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
            get_recorded_result_of_measurement_of_recurrent_byte_pair_occurrence_position(ledger, event.identity)
            measurement_occurrences[event.identity] = (
                _measurement_occurrence_coordinates(event)
            )
            continue
        if event.kind == SHARED_POSITION_MEASUREMENT_RESULT_KIND:
            get_recorded_shared_position_measurement(ledger, event.identity)
            measurement_occurrences[event.identity] = (
                _measurement_occurrence_coordinates(event)
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
                "locality_standing_as_of_event_identity": material[
                    "locality_standing_as_of_event_identity"
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
        "as_of_event_identity": as_of_event_identity,
        "event_count": event_count,
        "ingest_occurrences": ingest_occurrences,
        "measurement_occurrences": measurement_occurrences,
        "exact_result_occurrences": exact_result_occurrences,
        "representations": representations,
        # No "current" Representation is projected.  Emission order is
        # preserved in `representations`, which retains representation Act and
        # emission occurrences in append order; naming one of them current
        # would assert present relevance that no occurrence establishes.
        # Exactly the relation standings recorded by Locality events;
        # emptiness is absence of record only.
        "recorded_relation_standings": recorded_relation_standings,
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
