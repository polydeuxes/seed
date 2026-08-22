"""Responsible comparison of earlier and later recorded byte-pair Measurements."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from seed_runtime.byte_measurement import (
    BYTE_PAIR_MEASUREMENT_RECORDED_KIND,
    _RecordedBytePairFinding,
    _validated_recorded_byte_position_pair_measurement,
    get_byte_position_pair_measurement_responsibility_assignment,
)
from seed_runtime.event import Event
from seed_runtime.events import CORRUPTED, EventLedger
from seed_runtime.evidence_of_yield_relation import (
    RECORDED_EVIDENCE_OF_YIELD_RELATION_KIND,
    _record_evidence_of_yield_relation,
    read_requirements_of_yield_relation,
)
from seed_runtime.identities import new_identity
from seed_runtime.material_acquisition import read_exact_material_acquisition_result
from seed_runtime.operator_invocation_locality import (
    OPERATOR_INVOCATION_LOCALITY_RECORDED_KIND,
    get_recorded_operator_invocation_locality,
)


RECORDED_PAIR_MEASUREMENT_COMPARISON_RESPONSIBILITY_ASSIGNMENT_KIND = (
    "recorded_pair_measurement_comparison.responsibility_assignment_recorded"
)
RECORDED_PAIR_MEASUREMENT_COMPARISON_APPLICABILITY_ACT_EVIDENCE_KIND = (
    "recorded_pair_measurement_comparison.applicability_act_evidenced"
)
RECORDED_PAIR_MEASUREMENT_COMPARISON_APPLICABILITY_RESULT_KIND = (
    "recorded_pair_measurement_comparison.applicability_recorded"
)
RECORDED_PAIR_MEASUREMENT_COMPARISON_ACT_EVIDENCE_KIND = (
    "recorded_pair_measurement_comparison.act_evidenced"
)
RECORDED_PAIR_MEASUREMENT_COMPARISON_RESULT_KIND = (
    "recorded_pair_measurement_comparison.recorded"
)

RECORDED_PAIR_MEASUREMENT_COMPARISON_BOOK_CLAUSE = "04.Compare.A"
RECORDED_PAIR_MEASUREMENT_COMPARISON_RULE = (
    "compare complete exact findings of earlier and later recorded byte-position-pair "
    "Measurement results"
)
RECORDED_PAIR_MEASUREMENT_COMPARISON_RESPONSIBILITY = (
    "determine Applicability and compare earlier and later exact carried byte-position-pair "
    "Measurement results through one operator material acquisition at prior Standing"
)
RECORDED_PAIR_MEASUREMENT_COMPARISON_ACT = (
    "Compare earlier and later exact carried byte-position-pair Measurement results"
)
RECORDED_PAIR_MEASUREMENT_COMPARISON_APPLICABILITY_ACT = (
    "Determine Applicability of earlier and later recorded Measurement results to one Compare"
)

EVENT_KIND_RESPONSIBILITIES = {
    RECORDED_PAIR_MEASUREMENT_COMPARISON_RESPONSIBILITY_ASSIGNMENT_KIND: "04.Compare.A",
    RECORDED_PAIR_MEASUREMENT_COMPARISON_APPLICABILITY_ACT_EVIDENCE_KIND: "02.Acts.A",
    RECORDED_PAIR_MEASUREMENT_COMPARISON_APPLICABILITY_RESULT_KIND: "01.Standing.E.1",
    RECORDED_PAIR_MEASUREMENT_COMPARISON_ACT_EVIDENCE_KIND: "02.Acts.A",
    RECORDED_PAIR_MEASUREMENT_COMPARISON_RESULT_KIND: "04.Compare.A",
}


class RecordedPairMeasurementComparisonError(ValueError):
    """One exact recorded pair-Measurement comparison is incoherent."""


_AssignmentReading = tuple[Event, dict[str, Any]]


def _identity(value: Any, message: str) -> str:
    if type(value) is not str or not value:
        raise RecordedPairMeasurementComparisonError(message)
    return value


def _operator_acquisition_for_material_result(
    ledger: EventLedger, added: Event
) -> tuple[Event, dict[str, Any]]:
    """Read direct O1 or the older generic result carrying O1 provenance."""

    from seed_runtime.operator_material_acquisition import (
        OPERATOR_MATERIAL_ACQUIRE_RECORDED_KIND,
        get_recorded_operator_material_acquire,
    )

    provenance = added.material.get("provenance_occurrence_references")
    reference = (
        added.identity
        if added.kind == OPERATOR_MATERIAL_ACQUIRE_RECORDED_KIND
        else provenance[0]
        if type(provenance) is list and len(provenance) == 1
        else None
    )
    acquired_event = ledger.get(reference) if type(reference) is str else None
    try:
        acquired = get_recorded_operator_material_acquire(ledger, reference)
    except (TypeError, ValueError) as error:
        raise RecordedPairMeasurementComparisonError(
            "later Measurement requires one exact operator acquisition occurrence"
        ) from error
    if (
        acquired_event is None
        or acquired_event.kind != OPERATOR_MATERIAL_ACQUIRE_RECORDED_KIND
        or acquired_event.locality_identity != added.locality_identity
        or acquired_event.exact_material != added.exact_material
    ):
        raise RecordedPairMeasurementComparisonError(
            "later Measurement requires one exact operator acquisition occurrence"
        )
    return acquired_event, acquired


def _measurement_reference(event: Event) -> dict[str, str]:
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


def _measurement_and_findings(
    ledger: EventLedger, event_identity: str
) -> tuple[Event, tuple[Any, ...], Event]:
    event_identity = _identity(
        event_identity, "comparison requires one exact recorded Measurement result"
    )
    event = ledger.get(event_identity)
    if (
        event is None
        or event.kind != BYTE_PAIR_MEASUREMENT_RECORDED_KIND
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise RecordedPairMeasurementComparisonError(
            "comparison requires one intact recorded byte-position-pair Measurement"
        )
    try:
        reading = _validated_recorded_byte_position_pair_measurement(
            ledger, event.identity, findings_only=True
        )
    except (TypeError, ValueError) as error:
        raise RecordedPairMeasurementComparisonError(
            "comparison requires one intact recorded byte-position-pair Measurement"
        ) from error
    findings = reading.results if reading is not None else None
    if type(findings) is not tuple or reading is None:
        raise RecordedPairMeasurementComparisonError(
            "comparison requires exact recorded pair findings"
        )
    return event, findings, reading.assignment


def _findings_from_carried_measurement(
    event: Event,
) -> tuple[_RecordedBytePairFinding, ...]:
    """Read finding coordinates produced by this same console call."""

    if (
        type(event) is not Event
        or event.kind != BYTE_PAIR_MEASUREMENT_RECORDED_KIND
        or event.exact_material is not None
    ):
        raise RecordedPairMeasurementComparisonError(
            "comparison requires one carried pair Measurement"
        )
    assertions = event.material.get("assertions")
    if type(assertions) is not list:
        raise RecordedPairMeasurementComparisonError(
            "comparison requires one carried pair Measurement"
        )
    findings = []
    identities = set()
    for assertion in assertions:
        dimensions = assertion.get("dimensions") if type(assertion) is dict else None
        subject = (
            assertion.get("assertion_subject")
            if type(assertion) is dict
            else None
        )
        support = assertion.get("input_support") if type(assertion) is dict else None
        result = assertion.get("result") if type(assertion) is dict else None
        identity = dimensions.get("identity") if type(dimensions) is dict else None
        content = dimensions.get("content") if type(dimensions) is dict else None
        representation = (
            subject.get("representation") if type(subject) is dict else None
        )
        local_support = (
            support.get("local_assertion_references")
            if type(support) is dict
            else None
        )
        if (
            type(identity) is not str
            or not identity
            or identity in identities
            or type(representation) is not list
            or len(representation) != 2
            or any(type(value) is not int for value in representation)
            or result not in {"count", "recurrence"}
            or type(content) is not dict
            or type(local_support) is not list
            or any(type(value) is not str or not value for value in local_support)
        ):
            raise RecordedPairMeasurementComparisonError(
                "comparison carried finding coordinates are not exact"
            )
        if result == "recurrence":
            if set(content) != {"recurrence_established"} or type(
                content["recurrence_established"]
            ) is not bool:
                raise RecordedPairMeasurementComparisonError(
                    "comparison carried finding content is not exact"
                )
            content_coordinates = content["recurrence_established"]
        else:
            if set(content) != {"input_count", "occurrences_carrying", "count"}:
                raise RecordedPairMeasurementComparisonError(
                    "comparison carried finding content is not exact"
                )
            content_coordinates = tuple(
                content[key]
                for key in ("input_count", "occurrences_carrying", "count")
            )
            if any(type(value) is not int for value in content_coordinates):
                raise RecordedPairMeasurementComparisonError(
                    "comparison carried finding content is not exact"
                )
        identities.add(identity)
        findings.append(
            _RecordedBytePairFinding(
                assertion_identity=identity,
                recorded_occurrence_identity=event.identity,
                representation=tuple(representation),
                result=result,
                _content_coordinates=content_coordinates,
                _local_support_assertion_identities=tuple(local_support),
            )
        )
    return tuple(findings)


def _source_occurrence_references(
    ledger: EventLedger, event: Event
) -> tuple[str, ...]:
    reference = event.material.get("responsibility_assignment_reference")
    assignment_event = get_byte_position_pair_measurement_responsibility_assignment(
        ledger,
        reference.get("recorded_occurrence_identity")
        if type(reference) is dict
        else None,
    )
    assignment = assignment_event.material
    return _source_occurrence_references_from_assignment(assignment)


def _source_occurrence_references_from_assignment(
    assignment: dict[str, Any],
) -> tuple[str, ...]:
    source_material = (
        assignment.get("source_occurrence_references")
        if type(assignment) is dict
        else None
    )
    if type(source_material) is not list or not source_material:
        raise RecordedPairMeasurementComparisonError(
            "comparison input carries no exact source occurrence sequence"
        )
    references = tuple(
        item.get("material_acquisition_occurrence_identity") if type(item) is dict else None
        for item in source_material
    )
    if (
        any(type(reference) is not str or not reference for reference in references)
        or len(set(references)) != len(references)
    ):
        raise RecordedPairMeasurementComparisonError(
            "comparison input carries no exact source occurrence sequence"
        )
    return references


def _comparison_inputs(
    ledger: EventLedger,
    *,
    earlier_result_event_identity: str,
    later_result_event_identity: str,
) -> dict[str, Any]:
    earlier, earlier_findings, earlier_assignment = _measurement_and_findings(
        ledger, earlier_result_event_identity
    )
    later, later_findings, later_assignment = _measurement_and_findings(
        ledger, later_result_event_identity
    )
    if earlier.identity == later.identity or earlier.locality_identity != later.locality_identity:
        raise RecordedPairMeasurementComparisonError(
            "comparison requires distinct results in one exact Locality"
        )
    try:
        ordered = ledger.occurrences_in_append_order(
            (earlier.identity, later.identity),
            locality_identity=earlier.locality_identity,
        )
    except (TypeError, ValueError) as error:
        raise RecordedPairMeasurementComparisonError(
            "later comparison input must follow the earlier input"
        ) from error
    if tuple(event.identity for event in ordered) != (earlier.identity, later.identity):
        raise RecordedPairMeasurementComparisonError(
            "later comparison input must follow the earlier input"
        )
    earlier_sources = _source_occurrence_references_from_assignment(
        earlier_assignment.material
    )
    later_sources = _source_occurrence_references_from_assignment(
        later_assignment.material
    )
    if len(later_sources) != len(earlier_sources) + 1 or later_sources[:-1] != earlier_sources:
        raise RecordedPairMeasurementComparisonError(
            "later Measurement must extend the earlier exact source sequence once"
        )
    added_reference = later_sources[-1]
    added = ledger.get(added_reference)
    provenance = (
        added.material.get("provenance_occurrence_references")
        if added is not None
        else None
    )
    try:
        if added is not None:
            read_exact_material_acquisition_result(ledger, added.identity)
    except (TypeError, ValueError) as error:
        raise RecordedPairMeasurementComparisonError(
            "later Measurement requires one exact acquisition result"
        ) from error
    cited_prior = tuple(
        reference
        for reference in earlier_sources
        if type(provenance) is list and reference in provenance
    )
    if (
        added is None
        or added.locality_identity != earlier.locality_identity
        or ledger.integrity_of(added.identity) == CORRUPTED
        or type(provenance) is not list
    ):
        raise RecordedPairMeasurementComparisonError(
            "later Measurement requires one added occurrence with exact source coordinates"
        )
    source_role = added.material.get("source_role")
    operator_material_acquire_result_event_identity = None
    operator_material_source_standing_reference = None
    if source_role == "this Witness":
        raise RecordedPairMeasurementComparisonError(
            "Witness provenance establishes no comparison input relation"
        )
    elif source_role == "this operator":
        from seed_runtime.operator_locality_standing import (
            read_operator_locality_standing_through,
        )

        acquired_event, acquired = _operator_acquisition_for_material_result(
            ledger, added
        )
        source_standing_reference = acquired.get("source_standing_reference")
        if (
            type(source_standing_reference) is not dict
            or source_standing_reference.get("locality_identity")
            != earlier.locality_identity
        ):
            raise RecordedPairMeasurementComparisonError(
                "later Measurement requires one exact operator acquisition occurrence"
            )
        try:
            source_standing = read_operator_locality_standing_through(
                ledger,
                locality_identity=earlier.locality_identity,
                through_event_occurrence_identity=source_standing_reference.get(
                    "locality_standing_through_event_occurrence_identity"
                ),
            )
        except (TypeError, ValueError) as error:
            raise RecordedPairMeasurementComparisonError(
                "operator acquisition carries no exact prior Standing"
            ) from error
        carried_sources = {
            occurrence.get("result_occurrence_identity")
            for occurrence in source_standing.get("material_acquisition_result_occurrences", ())
            if type(occurrence) is dict
        }
        carried_representation_event_identities = {
            coordinates.get("representation_event_identity")
            for coordinates in source_standing.get("representations", {}).values()
            if type(coordinates) is dict
        }
        if (
            earlier.identity
            not in source_standing.get("measurement_occurrences", {})
            or any(reference not in carried_sources for reference in earlier_sources)
            or source_standing_reference.get(
                "addressed_representation_event_identity"
            )
            not in carried_representation_event_identities
        ):
            raise RecordedPairMeasurementComparisonError(
                "operator acquisition carries no exact prior Standing"
            )
        operator_material_acquire_result_event_identity = acquired_event.identity
        operator_material_source_standing_reference = deepcopy(
            source_standing_reference
        )
        input_relation = "operator material acquisition at prior Standing"
    else:
        raise RecordedPairMeasurementComparisonError(
            "later Measurement requires one exact operator occurrence"
        )
    invocation_relations = tuple(
        event
        for reference in provenance
        for event in (ledger.get(reference),)
        if event is not None and event.kind == OPERATOR_INVOCATION_LOCALITY_RECORDED_KIND
    )
    if len(invocation_relations) > 1:
        raise RecordedPairMeasurementComparisonError(
            "added occurrence carries several operator invocation Locality relations"
        )
    invocation_relation = invocation_relations[0] if invocation_relations else None
    operator_locality_identity = (
        earlier.locality_identity if source_role == "this operator" else None
    )
    if invocation_relation is not None:
        relation = get_recorded_operator_invocation_locality(
            ledger, invocation_relation.identity
        )
        if relation["destination_locality_identity"] != earlier.locality_identity:
            raise RecordedPairMeasurementComparisonError(
                "added occurrence carries a crossed invocation Locality relation"
            )
        operator_locality_identity = relation["operator_locality_identity"]
    return {
        "locality_identity": earlier.locality_identity,
        "earlier_event": earlier,
        "later_event": later,
        "earlier_findings": earlier_findings,
        "later_findings": later_findings,
        "earlier_source": earlier_sources,
        "later_source": later_sources,
        "added_reference": added_reference,
        "prior_provenance": cited_prior,
        "added_provenance": tuple(provenance),
        "input_relation": input_relation,
        "operator_material_acquire_result_event_identity": (
            operator_material_acquire_result_event_identity
        ),
        "operator_material_source_standing_reference": (
            operator_material_source_standing_reference
        ),
        "operator_invocation_locality_relation_event_identity": (
            invocation_relation.identity if invocation_relation is not None else None
        ),
        "operator_locality_identity": operator_locality_identity,
    }


def _comparison_inputs_from_carried_measurements(
    ledger: EventLedger,
    *,
    earlier: Event,
    later: Event,
    locality_standing: dict[str, Any],
) -> dict[str, Any]:
    """Revalidate the older result and carry the newly produced result."""

    if (
        type(earlier) is not Event
        or type(later) is not Event
        or earlier.kind != BYTE_PAIR_MEASUREMENT_RECORDED_KIND
        or later.kind != BYTE_PAIR_MEASUREMENT_RECORDED_KIND
        or earlier.identity == later.identity
        or earlier.locality_identity != later.locality_identity
        or type(locality_standing) is not dict
        or locality_standing.get("locality_identity") != earlier.locality_identity
    ):
        raise RecordedPairMeasurementComparisonError(
            "comparison requires first and second carried pair Measurements"
        )
    earlier, earlier_findings, earlier_assignment = _measurement_and_findings(
        ledger, earlier.identity
    )
    carried = locality_standing.get("measurement_occurrences")
    if (
        type(carried) is not dict
        or earlier.identity not in carried
        or later.identity not in carried
    ):
        raise RecordedPairMeasurementComparisonError(
            "comparison requires first and second carried pair Measurements"
        )
    try:
        ordered = ledger.occurrences_in_append_order(
            (earlier.identity, later.identity),
            locality_identity=earlier.locality_identity,
        )
    except (TypeError, ValueError) as error:
        raise RecordedPairMeasurementComparisonError(
            "later comparison input must follow the earlier input"
        ) from error
    if tuple(event.identity for event in ordered) != (
        earlier.identity,
        later.identity,
    ):
        raise RecordedPairMeasurementComparisonError(
            "later comparison input must follow the earlier input"
        )
    earlier_sources = _source_occurrence_references_from_assignment(
        earlier_assignment.material
    )
    later_sources = _source_occurrence_references(ledger, later)
    if (
        len(later_sources) != len(earlier_sources) + 1
        or later_sources[:-1] != earlier_sources
    ):
        raise RecordedPairMeasurementComparisonError(
            "later Measurement must extend the earlier exact source sequence once"
        )
    added_reference = later_sources[-1]
    added = ledger.get(added_reference)
    provenance = (
        added.material.get("provenance_occurrence_references")
        if added is not None
        else None
    )
    try:
        if added is not None:
            read_exact_material_acquisition_result(ledger, added.identity)
    except (TypeError, ValueError) as error:
        raise RecordedPairMeasurementComparisonError(
            "later Measurement requires one exact acquisition result"
        ) from error
    cited_prior = tuple(
        reference
        for reference in earlier_sources
        if type(provenance) is list and reference in provenance
    )
    if (
        added is None
        or added.locality_identity != earlier.locality_identity
        or ledger.integrity_of(added.identity) == CORRUPTED
        or type(provenance) is not list
    ):
        raise RecordedPairMeasurementComparisonError(
            "later Measurement requires one added occurrence with exact source coordinates"
        )
    source_role = added.material.get("source_role")
    acquisition_identity = None
    source_standing_reference = None
    if source_role == "this operator":
        acquired, acquired_material = _operator_acquisition_for_material_result(
            ledger, added
        )
        exact_results = locality_standing.get("exact_result_occurrences")
        source_standing_reference = acquired_material.get(
            "source_standing_reference"
        )
        representations = locality_standing.get("representations")
        represented = (
            tuple(representations.values())
            if type(representations) is dict
            else ()
        )
        if (
            acquired.locality_identity != earlier.locality_identity
            or acquired.exact_material != added.exact_material
            or type(exact_results) is not dict
            or acquired.identity not in exact_results
            or type(source_standing_reference) is not dict
            or source_standing_reference.get("locality_identity")
            != earlier.locality_identity
            or not any(
                type(reference) is dict
                and reference.get("representation_event_identity")
                == source_standing_reference.get(
                    "addressed_representation_event_identity"
                )
                for reference in represented
            )
        ):
            raise RecordedPairMeasurementComparisonError(
                "operator acquisition carries no exact prior Standing"
            )
        try:
            ledger.occurrences_in_append_order(
                (
                    earlier.identity,
                    source_standing_reference[
                        "addressed_representation_event_identity"
                    ],
                ),
                locality_identity=earlier.locality_identity,
            )
        except (KeyError, TypeError, ValueError) as error:
            raise RecordedPairMeasurementComparisonError(
                "operator acquisition carries no exact prior Standing"
            ) from error
        acquisition_identity = acquired.identity
        input_relation = "operator material acquisition at prior Standing"
        operator_locality_identity = earlier.locality_identity
    elif source_role == "this Witness":
        raise RecordedPairMeasurementComparisonError(
            "Witness provenance establishes no comparison input relation"
        )
    else:
        raise RecordedPairMeasurementComparisonError(
            "later Measurement requires one exact operator occurrence"
        )
    invocation_relations = tuple(
        event
        for reference in provenance
        for event in (ledger.get(reference),)
        if event is not None and event.kind == OPERATOR_INVOCATION_LOCALITY_RECORDED_KIND
    )
    if len(invocation_relations) > 1:
        raise RecordedPairMeasurementComparisonError(
            "added occurrence carries several operator invocation Locality relations"
        )
    invocation_relation = invocation_relations[0] if invocation_relations else None
    if invocation_relation is not None:
        relation = get_recorded_operator_invocation_locality(
            ledger, invocation_relation.identity
        )
        if relation["destination_locality_identity"] != earlier.locality_identity:
            raise RecordedPairMeasurementComparisonError(
                "added occurrence carries a crossed invocation Locality relation"
            )
        operator_locality_identity = relation["operator_locality_identity"]
    return {
        "locality_identity": earlier.locality_identity,
        "earlier_event": earlier,
        "later_event": later,
        "earlier_findings": earlier_findings,
        "later_findings": _findings_from_carried_measurement(later),
        "earlier_source": earlier_sources,
        "later_source": later_sources,
        "added_reference": added_reference,
        "prior_provenance": cited_prior,
        "added_provenance": tuple(provenance),
        "input_relation": input_relation,
        "operator_material_acquire_result_event_identity": acquisition_identity,
        "operator_material_source_standing_reference": deepcopy(
            source_standing_reference
        ),
        "operator_invocation_locality_relation_event_identity": (
            invocation_relation.identity if invocation_relation is not None else None
        ),
        "operator_locality_identity": operator_locality_identity,
    }


def _require_measurement_standing(
    ledger: EventLedger,
    *,
    inputs: dict[str, Any],
    locality_standing: dict[str, Any],
) -> str:
    if type(locality_standing) is not dict:
        raise RecordedPairMeasurementComparisonError(
            "comparison requires exact current Locality Standing"
        )
    carried = locality_standing.get("measurement_occurrences")
    boundary_identity = locality_standing.get("through_event_occurrence_identity")
    required = (
        inputs["earlier_event"].identity,
        inputs["later_event"].identity,
    )
    if (
        locality_standing.get("locality_identity") != inputs["locality_identity"]
        or type(carried) is not dict
        or any(reference not in carried for reference in required)
        or type(boundary_identity) is not str
        or not boundary_identity
    ):
        raise RecordedPairMeasurementComparisonError(
            "comparison requires each exact Measurement result in current Standing"
        )
    identities = tuple(dict.fromkeys((*required, boundary_identity)))
    try:
        ordered = ledger.occurrences_in_append_order(
            identities, locality_identity=inputs["locality_identity"]
        )
    except (TypeError, ValueError) as error:
        raise RecordedPairMeasurementComparisonError(
            "comparison Standing boundary lacks a required input"
        ) from error
    if tuple(event.identity for event in ordered) != identities:
        raise RecordedPairMeasurementComparisonError(
            "comparison Standing boundary lacks a required input"
        )
    return boundary_identity


def _assignment_reference(assignment: Event) -> dict[str, str]:
    return {
        "recorded_occurrence_identity": assignment.identity,
        "assignment_identity": assignment.material["assignment_identity"],
        "assignment_subject_identity": assignment.material[
            "assignment_subject_identity"
        ],
        "comparison_result_identity": assignment.material[
            "comparison_result_identity"
        ],
    }


def _assignment_material(
    *,
    inputs: dict[str, Any],
    standing_boundary_identity: str,
    assignment_identity: str,
    assignment_subject_identity: str,
    applicability_act_identity: str,
    applicability_act_occurrence_identity: str,
    applicability_result_identity: str,
    comparison_act_identity: str,
    comparison_act_occurrence_identity: str,
    comparison_result_identity: str,
    earlier_input_relation_identity: str,
    later_input_relation_identity: str,
    earlier_participation_relation_identity: str,
    later_participation_relation_identity: str,
) -> dict[str, Any]:
    return {
        "assignment_identity": assignment_identity,
        "assignment_subject_identity": assignment_subject_identity,
        "applicability_act_identity": applicability_act_identity,
        "applicability_act_occurrence_identity": applicability_act_occurrence_identity,
        "applicability_result_identity": applicability_result_identity,
        "comparison_act_identity": comparison_act_identity,
        "comparison_act_occurrence_identity": comparison_act_occurrence_identity,
        "comparison_result_identity": comparison_result_identity,
        "earlier_input_relation_identity": earlier_input_relation_identity,
        "later_input_relation_identity": later_input_relation_identity,
        "earlier_participation_relation_identity": (
            earlier_participation_relation_identity
        ),
        "later_participation_relation_identity": (
            later_participation_relation_identity
        ),
        "book_clause_identity": RECORDED_PAIR_MEASUREMENT_COMPARISON_BOOK_CLAUSE,
        "responsibility": RECORDED_PAIR_MEASUREMENT_COMPARISON_RESPONSIBILITY,
        "responsible_boundary": "this Seed",
        "comparison_rule": RECORDED_PAIR_MEASUREMENT_COMPARISON_RULE,
        "earlier_measurement_reference": _measurement_reference(
            inputs["earlier_event"]
        ),
        "later_measurement_reference": _measurement_reference(inputs["later_event"]),
        "earlier_source_occurrence_references": list(inputs["earlier_source"]),
        "later_source_occurrence_references": list(inputs["later_source"]),
        "added_occurrence_reference": inputs["added_reference"],
        "prior_provenance_occurrence_references": list(inputs["prior_provenance"]),
        "added_occurrence_provenance_references": list(
            inputs["added_provenance"]
        ),
        "operator_invocation_locality_relation_event_identity": inputs[
            "operator_invocation_locality_relation_event_identity"
        ],
        "input_relation": inputs["input_relation"],
        "operator_material_acquire_result_event_identity": inputs[
            "operator_material_acquire_result_event_identity"
        ],
        "operator_material_source_standing_reference": deepcopy(
            inputs["operator_material_source_standing_reference"]
        ),
        "destination_operator_locality_identity": inputs[
            "operator_locality_identity"
        ],
        "standing_boundary_identity": standing_boundary_identity,
        "scope": {
            "locality_identity": inputs["locality_identity"],
            "standing_boundary_identity": standing_boundary_identity,
            "added_occurrence_reference": inputs["added_reference"],
            "operator_invocation_locality_relation_event_identity": inputs[
                "operator_invocation_locality_relation_event_identity"
            ],
            "input_relation": inputs["input_relation"],
            "operator_material_acquire_result_event_identity": inputs[
                "operator_material_acquire_result_event_identity"
            ],
            "operator_material_source_standing_reference": deepcopy(
                inputs["operator_material_source_standing_reference"]
            ),
            "destination_operator_locality_identity": inputs[
                "operator_locality_identity"
            ],
        },
        "limits": [
            "comparison establishes no source relation",
            "comparison establishes no represented relation",
            "comparison establishes no Admission or Applicability for another Act",
        ],
        "unknown": [
            "what the measured difference represents: Unknown"
        ],
    }


def record_recorded_pair_measurement_comparison_responsibility_assignment(
    ledger: EventLedger,
    *,
    earlier_result_event_identity: str,
    later_result_event_identity: str,
    locality_standing: dict[str, Any],
) -> Event:
    """Assign one exact Compare through one exact input relation."""

    inputs = _comparison_inputs(
        ledger,
        earlier_result_event_identity=earlier_result_event_identity,
        later_result_event_identity=later_result_event_identity,
    )
    boundary = _require_measurement_standing(
        ledger, inputs=inputs, locality_standing=locality_standing
    )
    return _record_comparison_responsibility_assignment(
        ledger, inputs=inputs, standing_boundary_identity=boundary
    )


def _record_comparison_responsibility_assignment(
    ledger: EventLedger,
    *,
    inputs: dict[str, Any],
    standing_boundary_identity: str,
) -> Event:
    identities = {
        "assignment_identity": new_identity("recorded_pair_comparison_assignment"),
        "assignment_subject_identity": new_identity(
            "recorded_pair_comparison_assignment_subject"
        ),
        "applicability_act_identity": new_identity(
            "recorded_pair_comparison_applicability_act"
        ),
        "applicability_act_occurrence_identity": new_identity(
            "recorded_pair_comparison_applicability_occurrence"
        ),
        "applicability_result_identity": new_identity(
            "recorded_pair_comparison_applicability_result"
        ),
        "comparison_act_identity": new_identity("recorded_pair_comparison_act"),
        "comparison_act_occurrence_identity": new_identity(
            "recorded_pair_comparison_occurrence"
        ),
        "comparison_result_identity": new_identity(
            "recorded_pair_comparison_result"
        ),
        "earlier_input_relation_identity": new_identity(
            "recorded_pair_comparison_earlier_input_relation"
        ),
        "later_input_relation_identity": new_identity(
            "recorded_pair_comparison_later_input_relation"
        ),
        "earlier_participation_relation_identity": new_identity(
            "recorded_pair_comparison_earlier_participation"
        ),
        "later_participation_relation_identity": new_identity(
            "recorded_pair_comparison_later_participation"
        ),
    }
    if len(set(identities.values())) != len(identities):
        raise RecordedPairMeasurementComparisonError(
            "comparison lifecycle identities are compressed"
        )
    return ledger.append(
        RECORDED_PAIR_MEASUREMENT_COMPARISON_RESPONSIBILITY_ASSIGNMENT_KIND,
        _assignment_material(
            inputs=inputs,
            standing_boundary_identity=standing_boundary_identity,
            assignment_identity=identities["assignment_identity"],
            assignment_subject_identity=identities["assignment_subject_identity"],
            applicability_act_identity=identities["applicability_act_identity"],
            applicability_act_occurrence_identity=identities[
                "applicability_act_occurrence_identity"
            ],
            applicability_result_identity=identities[
                "applicability_result_identity"
            ],
            comparison_act_identity=identities["comparison_act_identity"],
            comparison_act_occurrence_identity=identities[
                "comparison_act_occurrence_identity"
            ],
            comparison_result_identity=identities[
                "comparison_result_identity"
            ],
            earlier_input_relation_identity=identities[
                "earlier_input_relation_identity"
            ],
            later_input_relation_identity=identities[
                "later_input_relation_identity"
            ],
            earlier_participation_relation_identity=identities[
                "earlier_participation_relation_identity"
            ],
            later_participation_relation_identity=identities[
                "later_participation_relation_identity"
            ],
        ),
        locality_identity=inputs["locality_identity"],
    )


def _assignment_reading(
    ledger: EventLedger, event_identity: str
) -> _AssignmentReading:
    event = ledger.get(_identity(event_identity, "comparison requires one assignment"))
    if (
        event is None
        or event.kind
        != RECORDED_PAIR_MEASUREMENT_COMPARISON_RESPONSIBILITY_ASSIGNMENT_KIND
        or event.exact_material is not None
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise RecordedPairMeasurementComparisonError(
            "comparison assignment is absent or corrupted"
        )
    material = event.material
    earlier_reference = material.get("earlier_measurement_reference")
    later_reference = material.get("later_measurement_reference")
    if type(earlier_reference) is not dict or type(later_reference) is not dict:
        raise RecordedPairMeasurementComparisonError(
            "comparison assignment carries no exact inputs"
        )
    inputs = _comparison_inputs(
        ledger,
        earlier_result_event_identity=earlier_reference.get(
            "recorded_occurrence_identity"
        ),
        later_result_event_identity=later_reference.get("recorded_occurrence_identity"),
    )
    identity_keys = (
        "assignment_identity",
        "assignment_subject_identity",
        "applicability_act_identity",
        "applicability_act_occurrence_identity",
        "applicability_result_identity",
        "comparison_act_identity",
        "comparison_act_occurrence_identity",
        "comparison_result_identity",
        "earlier_input_relation_identity",
        "later_input_relation_identity",
        "earlier_participation_relation_identity",
        "later_participation_relation_identity",
    )
    identities = {key: material.get(key) for key in identity_keys}
    if any(type(value) is not str or not value for value in identities.values()) or len(
        set(identities.values())
    ) != len(identities):
        raise RecordedPairMeasurementComparisonError(
            "comparison assignment identities are not exact"
        )
    boundary = material.get("standing_boundary_identity")
    boundary_event = ledger.get(boundary) if type(boundary) is str else None
    if (
        boundary_event is None
        or boundary_event.locality_identity != event.locality_identity
        or ledger.integrity_of(boundary_event.identity) == CORRUPTED
    ):
        raise RecordedPairMeasurementComparisonError(
            "comparison assignment carries no intact Standing boundary"
        )
    expected = _assignment_material(
        inputs=inputs,
        standing_boundary_identity=boundary,
        **identities,
    )
    if event.locality_identity != inputs["locality_identity"] or material != expected:
        raise RecordedPairMeasurementComparisonError(
            "comparison assignment coordinates are not exact"
        )
    try:
        ordered_references = tuple(
            dict.fromkeys(
                (
                    inputs["earlier_event"].identity,
                    inputs["later_event"].identity,
                    boundary,
                    event.identity,
                )
            )
        )
        ledger.occurrences_in_append_order(
            ordered_references,
            locality_identity=event.locality_identity,
        )
    except ValueError as error:
        raise RecordedPairMeasurementComparisonError(
            "comparison assignment does not follow its exact inputs"
        ) from error
    return event, inputs


def get_recorded_pair_measurement_comparison_responsibility_assignment(
    ledger: EventLedger, event_identity: str
) -> Event:
    return _assignment_reading(ledger, event_identity)[0]


def _require_assignment_standing(
    assignment: Event, locality_standing: dict[str, Any]
) -> None:
    carried = (
        locality_standing.get("responsibility_assignment_occurrences")
        if type(locality_standing) is dict
        else None
    )
    if (
        type(carried) is not dict
        or carried.get(assignment.identity, object()) is not None
        or locality_standing.get("locality_identity") != assignment.locality_identity
    ):
        raise RecordedPairMeasurementComparisonError(
            "comparison requires its exact assignment Standing"
        )


def _applicability_of_input_to_compare(assignment: Event) -> list[dict[str, Any]]:
    material = assignment.material
    return [
        {
            "relation_identity": material["earlier_input_relation_identity"],
            "input_role": "earlier recorded pair Measurement result",
            "input_reference": deepcopy(material["earlier_measurement_reference"]),
            "addressed_act_identity": material["comparison_act_identity"],
            "standing": "applicable",
        },
        {
            "relation_identity": material["later_input_relation_identity"],
            "input_role": "later recorded pair Measurement result",
            "input_reference": deepcopy(material["later_measurement_reference"]),
            "addressed_act_identity": material["comparison_act_identity"],
            "standing": "applicable",
        },
    ]


def _applicability_act_material(assignment: Event) -> dict[str, Any]:
    material = assignment.material
    return {
        "applicability_act_identity": material["applicability_act_identity"],
        "act_occurrence_identity": material[
            "applicability_act_occurrence_identity"
        ],
        "result_identity": material["applicability_result_identity"],
        "act": RECORDED_PAIR_MEASUREMENT_COMPARISON_APPLICABILITY_ACT,
        "responsibility": RECORDED_PAIR_MEASUREMENT_COMPARISON_RESPONSIBILITY,
        "responsible_boundary": "this Seed",
        "responsibility_assignment_reference": _assignment_reference(assignment),
        "applicability_of_input_to_compare": (
            _applicability_of_input_to_compare(assignment)
        ),
        "comparison_rule": RECORDED_PAIR_MEASUREMENT_COMPARISON_RULE,
        "scope": deepcopy(material["scope"]),
        "evidence_scope": "Evidence for this exact input-to-Compare relation set",
    }


def record_recorded_pair_measurement_comparison_applicability_act_evidence(
    ledger: EventLedger,
    *,
    responsibility_assignment_event_identity: str,
    locality_standing: dict[str, Any],
) -> Event:
    assignment = get_recorded_pair_measurement_comparison_responsibility_assignment(
        ledger, responsibility_assignment_event_identity
    )
    _require_assignment_standing(assignment, locality_standing)
    return ledger.append(
        RECORDED_PAIR_MEASUREMENT_COMPARISON_APPLICABILITY_ACT_EVIDENCE_KIND,
        _applicability_act_material(assignment),
        locality_identity=assignment.locality_identity,
    )


def _applicability_act_reading(
    ledger: EventLedger,
    event_identity: str,
    *,
    assignment_reading: _AssignmentReading | None = None,
) -> tuple[Event, _AssignmentReading]:
    event = ledger.get(_identity(event_identity, "comparison requires Applicability Evidence"))
    if (
        event is None
        or event.kind
        != RECORDED_PAIR_MEASUREMENT_COMPARISON_APPLICABILITY_ACT_EVIDENCE_KIND
        or event.exact_material is not None
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise RecordedPairMeasurementComparisonError(
            "comparison Applicability Evidence is absent or corrupted"
        )
    reference = event.material.get("responsibility_assignment_reference")
    assignment_identity = (
        reference.get("recorded_occurrence_identity")
        if type(reference) is dict
        else None
    )
    if assignment_reading is None:
        assignment_reading = (
            _assignment_reading(ledger, assignment_identity)
        )
    assignment, _inputs = assignment_reading
    if (
        assignment_identity != assignment.identity
        or event.locality_identity != assignment.locality_identity
        or event.material != _applicability_act_material(assignment)
    ):
        raise RecordedPairMeasurementComparisonError(
            "comparison Applicability Evidence is not exact"
        )
    try:
        ledger.occurrences_in_append_order(
            (assignment.identity, event.identity),
            locality_identity=event.locality_identity,
        )
    except ValueError as error:
        raise RecordedPairMeasurementComparisonError(
            "comparison Applicability does not follow its assignment"
        ) from error
    return event, assignment_reading


def get_recorded_pair_measurement_comparison_applicability_act_evidence(
    ledger: EventLedger, event_identity: str
) -> Event:
    return _applicability_act_reading(ledger, event_identity)[0]


def _applicability_result_material(act: Event) -> dict[str, Any]:
    return {
        "result_identity": act.material["result_identity"],
        "applicability_act_identity": act.material["applicability_act_identity"],
        "act_occurrence_identity": act.material["act_occurrence_identity"],
        "exact_act": RECORDED_PAIR_MEASUREMENT_COMPARISON_APPLICABILITY_ACT,
        "responsibility": RECORDED_PAIR_MEASUREMENT_COMPARISON_RESPONSIBILITY,
        "responsible_boundary": "this Seed",
        "responsibility_assignment_reference": deepcopy(
            act.material["responsibility_assignment_reference"]
        ),
        "applicability_of_input_to_compare": deepcopy(
            act.material["applicability_of_input_to_compare"]
        ),
        "comparison_rule": RECORDED_PAIR_MEASUREMENT_COMPARISON_RULE,
        "scope": deepcopy(act.material["scope"]),
        "standing": "applicable",
        "limits": [
            "Applicability establishes no Participation or comparison result"
        ],
        "unknown": [
            "what the compared difference represents: Unknown"
        ],
    }


def _recorded_applicability_result_material(
    material: dict[str, Any], *, act_identity: str, evidence_identity: str
) -> dict[str, Any]:
    return {
        "result_identity": material["result_identity"],
        "applicability_act_identity": material["applicability_act_identity"],
        "act_occurrence_identity": material["act_occurrence_identity"],
        "exact_act": material["exact_act"],
        "responsibility": material["responsibility"],
        "responsible_boundary": material["responsible_boundary"],
        "responsibility_assignment_reference": deepcopy(
            material["responsibility_assignment_reference"]
        ),
        "applicability_of_input_to_compare": deepcopy(
            material["applicability_of_input_to_compare"]
        ),
        "comparison_rule": material["comparison_rule"],
        "scope": deepcopy(material["scope"]),
        "standing": material["standing"],
        "limits": list(material["limits"]),
        "unknown": list(material["unknown"]),
        "responsible_act_evidence_identity": act_identity,
        "evidence_of_yield_relation_identity": evidence_identity,
    }


def record_recorded_pair_measurement_comparison_applicability_result(
    ledger: EventLedger, *, responsible_act_evidence_event_identity: str
) -> Event:
    act = get_recorded_pair_measurement_comparison_applicability_act_evidence(
        ledger, responsible_act_evidence_event_identity
    )
    result = _applicability_result_material(act)
    return _record_applicability_result_from_act(ledger, act=act, result=result)


def _record_applicability_result_from_act(
    ledger: EventLedger, *, act: Event, result: dict[str, Any]
) -> Event:
    evidence = _record_evidence_of_yield_relation(
        ledger,
        locality_identity=act.locality_identity,
        exact_act=RECORDED_PAIR_MEASUREMENT_COMPARISON_APPLICABILITY_ACT,
        act_occurrence_identity=act.material["act_occurrence_identity"],
        responsible_act_evidence_identity=act.identity,
        result_kind="recorded pair Measurement comparison Applicability result",
        result_identity=result["result_identity"],
        result_content=result,
        responsibility=RECORDED_PAIR_MEASUREMENT_COMPARISON_RESPONSIBILITY,
        occurrence_boundary="recorded_pair_measurement_comparison_applicability",
        responsible_boundary="this Seed",
    )
    return ledger.append(
        RECORDED_PAIR_MEASUREMENT_COMPARISON_APPLICABILITY_RESULT_KIND,
        _recorded_applicability_result_material(
            result, act_identity=act.identity, evidence_identity=evidence.identity
        ),
        locality_identity=act.locality_identity,
    )


def _applicability_reading(
    ledger: EventLedger,
    event_identity: str,
    *,
    assignment_reading: _AssignmentReading | None = None,
) -> tuple[
    dict[str, Any],
    Event,
    Event,
    _AssignmentReading,
]:
    event = ledger.get(_identity(event_identity, "comparison requires Applicability"))
    if (
        event is None
        or event.kind != RECORDED_PAIR_MEASUREMENT_COMPARISON_APPLICABILITY_RESULT_KIND
        or event.exact_material is not None
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise RecordedPairMeasurementComparisonError(
            "comparison Applicability is absent or corrupted"
        )
    act, assignment_reading = (
        _applicability_act_reading(
            ledger,
            event.material.get("responsible_act_evidence_identity"),
            assignment_reading=assignment_reading,
        )
    )
    expected = _recorded_applicability_result_material(
        _applicability_result_material(act),
        act_identity=act.identity,
        evidence_identity=event.material.get("evidence_of_yield_relation_identity"),
    )
    requirements = read_requirements_of_yield_relation(
        ledger,
        recorded_result_event_identity=event.identity,
        evidence_of_yield_relation_event_identity=event.material.get(
            "evidence_of_yield_relation_identity"
        ),
        responsible_act_evidence_event_identity=act.identity,
    )
    if (
        event.locality_identity != act.locality_identity
        or event.material != expected
        or not all(requirements.values())
    ):
        raise RecordedPairMeasurementComparisonError(
            "comparison Applicability carries no exact Yield"
        )
    return deepcopy(event.material), event, act, assignment_reading


def get_recorded_pair_measurement_comparison_applicability(
    ledger: EventLedger, event_identity: str
) -> dict[str, Any]:
    return _applicability_reading(ledger, event_identity)[0]


def _require_applicability_standing(
    assignment: Event,
    applicability: Event,
    locality_standing: dict[str, Any],
) -> None:
    assignments = (
        locality_standing.get("responsibility_assignment_occurrences")
        if type(locality_standing) is dict
        else None
    )
    applicable = (
        locality_standing.get("applicability_result_occurrences")
        if type(locality_standing) is dict
        else None
    )
    if (
        locality_standing.get("locality_identity") != assignment.locality_identity
        or type(assignments) is not dict
        or assignments.get(assignment.identity, object()) is not None
        or type(applicable) is not dict
        or applicable.get(applicability.identity, object()) is not None
    ):
        raise RecordedPairMeasurementComparisonError(
            "Compare requires its exact assignment and Applicability Standing"
        )


def _participation_of_input_in_compare(assignment: Event) -> list[dict[str, Any]]:
    material = assignment.material
    return [
        {
            "relation_identity": material[
                "earlier_participation_relation_identity"
            ],
            "subject_reference": deepcopy(material["earlier_measurement_reference"]),
            "role": "earlier recorded pair Measurement result",
            "act_occurrence_identity": material[
                "comparison_act_occurrence_identity"
            ],
        },
        {
            "relation_identity": material[
                "later_participation_relation_identity"
            ],
            "subject_reference": deepcopy(material["later_measurement_reference"]),
            "role": "later recorded pair Measurement result",
            "act_occurrence_identity": material[
                "comparison_act_occurrence_identity"
            ],
        },
    ]


def _comparison_act_material(assignment: Event, applicability: Event) -> dict[str, Any]:
    material = assignment.material
    return {
        "comparison_act_identity": material["comparison_act_identity"],
        "act_occurrence_identity": material["comparison_act_occurrence_identity"],
        "result_identity": material["comparison_result_identity"],
        "act": RECORDED_PAIR_MEASUREMENT_COMPARISON_ACT,
        "responsibility": RECORDED_PAIR_MEASUREMENT_COMPARISON_RESPONSIBILITY,
        "responsible_boundary": "this Seed",
        "responsibility_assignment_reference": _assignment_reference(assignment),
        "applicability_result_event_identity": applicability.identity,
        "applicability_of_input_to_compare": deepcopy(
            applicability.material["applicability_of_input_to_compare"]
        ),
        "participation_of_input_in_compare": (
            _participation_of_input_in_compare(assignment)
        ),
        "comparison_rule": RECORDED_PAIR_MEASUREMENT_COMPARISON_RULE,
        "scope": deepcopy(material["scope"]),
        "evidence_scope": "Evidence for this exact Compare occurrence",
    }


def record_recorded_pair_measurement_comparison_act_evidence(
    ledger: EventLedger,
    *,
    responsibility_assignment_event_identity: str,
    applicability_result_event_identity: str,
    locality_standing: dict[str, Any],
) -> Event:
    assignment_reading = _assignment_reading(
        ledger, responsibility_assignment_event_identity
    )
    assignment, _inputs = assignment_reading
    applicability_material, applicability, _act, applicability_assignment = (
        _applicability_reading(
            ledger,
            applicability_result_event_identity,
            assignment_reading=assignment_reading,
        )
    )
    if (
        applicability_assignment[0].identity != assignment.identity
        or applicability_material["responsibility_assignment_reference"]
        != _assignment_reference(assignment)
    ):
        raise RecordedPairMeasurementComparisonError(
            "Compare Applicability names another assignment"
        )
    _require_applicability_standing(
        assignment, applicability, locality_standing
    )
    return ledger.append(
        RECORDED_PAIR_MEASUREMENT_COMPARISON_ACT_EVIDENCE_KIND,
        _comparison_act_material(assignment, applicability),
        locality_identity=assignment.locality_identity,
    )


def _comparison_act_reading(
    ledger: EventLedger,
    event_identity: str,
    *,
    assignment_reading: _AssignmentReading | None = None,
) -> tuple[Event, _AssignmentReading, Event]:
    event = ledger.get(_identity(event_identity, "comparison requires Act Evidence"))
    if (
        event is None
        or event.kind != RECORDED_PAIR_MEASUREMENT_COMPARISON_ACT_EVIDENCE_KIND
        or event.exact_material is not None
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise RecordedPairMeasurementComparisonError(
            "comparison Act Evidence is absent or corrupted"
        )
    reference = event.material.get("responsibility_assignment_reference")
    if assignment_reading is None:
        assignment_reading = _assignment_reading(
            ledger,
            reference.get("recorded_occurrence_identity")
            if type(reference) is dict
            else None,
        )
    assignment, _inputs = assignment_reading
    applicability = ledger.get(event.material.get("applicability_result_event_identity"))
    if applicability is None:
        raise RecordedPairMeasurementComparisonError(
            "comparison Act Evidence carries no Applicability"
        )
    _material, applicability, _act, applicability_assignment_reading = (
        _applicability_reading(
            ledger,
            applicability.identity,
            assignment_reading=assignment_reading,
        )
    )
    if (
        applicability_assignment_reading[0].identity != assignment.identity
        or event.locality_identity != assignment.locality_identity
        or event.material != _comparison_act_material(assignment, applicability)
    ):
        raise RecordedPairMeasurementComparisonError(
            "comparison Act Evidence is not exact"
        )
    return event, assignment_reading, applicability


def get_recorded_pair_measurement_comparison_act_evidence(
    ledger: EventLedger, event_identity: str
) -> Event:
    return _comparison_act_reading(ledger, event_identity)[0]


def _finding_key(finding: Any) -> tuple[str, tuple[int, int] | None]:
    return finding.result, finding.representation


def _finding_content(finding: Any) -> Any:
    content = finding.content
    if type(content) is not dict:
        raise RecordedPairMeasurementComparisonError(
            "comparison input carries no exact finding content"
        )
    return content


def _comparison_of_findings(
    earlier: tuple[Any, ...], later: tuple[Any, ...]
) -> dict[str, list[dict[str, Any]]]:
    earlier_by_key = {_finding_key(item): item for item in earlier}
    later_by_key = {_finding_key(item): item for item in later}
    if len(earlier_by_key) != len(earlier) or len(later_by_key) != len(later):
        raise RecordedPairMeasurementComparisonError(
            "comparison input repeats one finding subject"
        )
    findings = {
        "same_content_findings": [],
        "conflicting_findings": [],
        "findings_of_earlier_result": [],
        "findings_of_later_result": [],
        "unknown_findings": [],
    }
    for key, first in earlier_by_key.items():
        second = later_by_key.get(key)
        subject = {
            "result": key[0],
            "representation": list(key[1]) if key[1] is not None else None,
        }
        first_content = _finding_content(first)
        if second is None:
            findings["findings_of_earlier_result"].append(
                {
                    "subject": subject,
                    "earlier_assertion_reference": first.reference,
                    "earlier_content": first_content,
                }
            )
            continue
        second_content = _finding_content(second)
        entry = {
            "subject": subject,
            "earlier_assertion_reference": first.reference,
            "later_assertion_reference": second.reference,
            "earlier_content": first_content,
            "later_content": second_content,
        }
        destination = (
            "same_content_findings"
            if first_content == second_content
            else "conflicting_findings"
        )
        findings[destination].append(entry)
    for key, second in later_by_key.items():
        if key in earlier_by_key:
            continue
        findings["findings_of_later_result"].append(
            {
                "subject": {
                    "result": key[0],
                    "representation": list(key[1]) if key[1] is not None else None,
                },
                "later_assertion_reference": second.reference,
                "later_content": _finding_content(second),
            }
        )
    return findings


def _comparison_result_material(
    act: Event,
    assignment_reading: _AssignmentReading,
) -> dict[str, Any]:
    assignment_reference = act.material["responsibility_assignment_reference"]
    assignment, inputs = assignment_reading
    if assignment_reference["recorded_occurrence_identity"] != assignment.identity:
        raise RecordedPairMeasurementComparisonError(
            "comparison result carries another assignment"
        )
    return {
        "result_identity": act.material["result_identity"],
        "comparison_act_identity": act.material["comparison_act_identity"],
        "act_occurrence_identity": act.material["act_occurrence_identity"],
        "exact_act": RECORDED_PAIR_MEASUREMENT_COMPARISON_ACT,
        "responsibility": RECORDED_PAIR_MEASUREMENT_COMPARISON_RESPONSIBILITY,
        "responsible_boundary": "this Seed",
        "responsibility_assignment_reference": deepcopy(assignment_reference),
        "applicability_result_event_identity": act.material[
            "applicability_result_event_identity"
        ],
        "applicability_of_input_to_compare": deepcopy(
            act.material["applicability_of_input_to_compare"]
        ),
        "participation_of_input_in_compare": deepcopy(
            act.material["participation_of_input_in_compare"]
        ),
        "comparison_rule": RECORDED_PAIR_MEASUREMENT_COMPARISON_RULE,
        "findings": _comparison_of_findings(
            inputs["earlier_findings"], inputs["later_findings"]
        ),
        "scope": deepcopy(act.material["scope"]),
        "limits": [
            "matching content establishes no corroboration or truth",
            "difference establishes no causal source relation or meaning",
            "comparison result establishes no Applicability for another Act",
        ],
        "unknown": [
            "what each measured match or difference represents: Unknown"
        ],
    }


def _recorded_comparison_result_material(
    material: dict[str, Any], *, act_identity: str, evidence_identity: str
) -> dict[str, Any]:
    return {
        "result_identity": material["result_identity"],
        "comparison_act_identity": material["comparison_act_identity"],
        "act_occurrence_identity": material["act_occurrence_identity"],
        "exact_act": material["exact_act"],
        "responsibility": material["responsibility"],
        "responsible_boundary": material["responsible_boundary"],
        "responsibility_assignment_reference": deepcopy(
            material["responsibility_assignment_reference"]
        ),
        "applicability_result_event_identity": material[
            "applicability_result_event_identity"
        ],
        "applicability_of_input_to_compare": deepcopy(
            material["applicability_of_input_to_compare"]
        ),
        "participation_of_input_in_compare": deepcopy(
            material["participation_of_input_in_compare"]
        ),
        "comparison_rule": material["comparison_rule"],
        "findings": deepcopy(material["findings"]),
        "scope": deepcopy(material["scope"]),
        "limits": list(material["limits"]),
        "unknown": list(material["unknown"]),
        "responsible_act_evidence_identity": act_identity,
        "evidence_of_yield_relation_identity": evidence_identity,
    }


def record_recorded_pair_measurement_comparison_result(
    ledger: EventLedger, *, responsible_act_evidence_event_identity: str
) -> Event:
    act, assignment_reading, _applicability = (
        _comparison_act_reading(
            ledger, responsible_act_evidence_event_identity
        )
    )
    result = _comparison_result_material(act, assignment_reading)
    return _record_comparison_result_from_act(ledger, act=act, result=result)


def _record_comparison_result_from_act(
    ledger: EventLedger, *, act: Event, result: dict[str, Any]
) -> Event:
    evidence = _record_evidence_of_yield_relation(
        ledger,
        locality_identity=act.locality_identity,
        exact_act=RECORDED_PAIR_MEASUREMENT_COMPARISON_ACT,
        act_occurrence_identity=act.material["act_occurrence_identity"],
        responsible_act_evidence_identity=act.identity,
        result_kind="recorded pair Measurement comparison result",
        result_identity=result["result_identity"],
        result_content=result,
        responsibility=RECORDED_PAIR_MEASUREMENT_COMPARISON_RESPONSIBILITY,
        occurrence_boundary="recorded_pair_measurement_comparison",
        responsible_boundary="this Seed",
    )
    return ledger.append(
        RECORDED_PAIR_MEASUREMENT_COMPARISON_RESULT_KIND,
        _recorded_comparison_result_material(
            result, act_identity=act.identity, evidence_identity=evidence.identity
        ),
        locality_identity=act.locality_identity,
    )


def _record_recorded_pair_measurement_comparison_from_carried_measurements(
    ledger: EventLedger,
    *,
    earlier_measurement: Event,
    later_measurement: Event,
    locality_standing: dict[str, Any],
) -> tuple[Event, dict[str, Any]]:
    """Record one complete Compare from results carried by this console call."""

    from seed_runtime.operator_locality_standing import (
        _carry_recorded_pair_comparison_occurrence_into_standing,
    )

    inputs = _comparison_inputs_from_carried_measurements(
        ledger,
        earlier=earlier_measurement,
        later=later_measurement,
        locality_standing=locality_standing,
    )
    boundary = _require_measurement_standing(
        ledger, inputs=inputs, locality_standing=locality_standing
    )
    assignment = _record_comparison_responsibility_assignment(
        ledger, inputs=inputs, standing_boundary_identity=boundary
    )
    locality_standing = _carry_recorded_pair_comparison_occurrence_into_standing(
        locality_standing,
        assignment,
        prior_through_event_occurrence_identity=boundary,
    )
    _require_assignment_standing(assignment, locality_standing)
    applicability_act = ledger.append(
        RECORDED_PAIR_MEASUREMENT_COMPARISON_APPLICABILITY_ACT_EVIDENCE_KIND,
        _applicability_act_material(assignment),
        locality_identity=assignment.locality_identity,
    )
    locality_standing = _carry_recorded_pair_comparison_occurrence_into_standing(
        locality_standing,
        applicability_act,
        prior_through_event_occurrence_identity=assignment.identity,
    )
    applicability_material = _applicability_result_material(applicability_act)
    applicability = _record_applicability_result_from_act(
        ledger, act=applicability_act, result=applicability_material
    )
    locality_standing = _carry_recorded_pair_comparison_occurrence_into_standing(
        locality_standing,
        applicability,
        prior_through_event_occurrence_identity=applicability_act.identity,
    )
    _require_applicability_standing(
        assignment, applicability, locality_standing
    )
    comparison_act = ledger.append(
        RECORDED_PAIR_MEASUREMENT_COMPARISON_ACT_EVIDENCE_KIND,
        _comparison_act_material(assignment, applicability),
        locality_identity=assignment.locality_identity,
    )
    locality_standing = _carry_recorded_pair_comparison_occurrence_into_standing(
        locality_standing,
        comparison_act,
        prior_through_event_occurrence_identity=applicability.identity,
    )
    assignment_reading = (assignment, inputs)
    result_material = _comparison_result_material(
        comparison_act, assignment_reading
    )
    result = _record_comparison_result_from_act(
        ledger, act=comparison_act, result=result_material
    )
    locality_standing = _carry_recorded_pair_comparison_occurrence_into_standing(
        locality_standing,
        result,
        prior_through_event_occurrence_identity=comparison_act.identity,
    )
    return result, locality_standing


def _recorded_pair_measurement_comparison_reading(
    ledger: EventLedger,
    event_identity: str,
    *,
    assignment_reading: _AssignmentReading | None = None,
) -> tuple[dict[str, Any], _AssignmentReading]:
    event = ledger.get(_identity(event_identity, "comparison requires one result"))
    if (
        event is None
        or event.kind != RECORDED_PAIR_MEASUREMENT_COMPARISON_RESULT_KIND
        or event.exact_material is not None
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise RecordedPairMeasurementComparisonError(
            "comparison result is absent or corrupted"
        )
    act, assignment_reading, _applicability = (
        _comparison_act_reading(
            ledger,
            event.material.get("responsible_act_evidence_identity"),
            assignment_reading=assignment_reading,
        )
    )
    expected = _recorded_comparison_result_material(
        _comparison_result_material(
            act, assignment_reading
        ),
        act_identity=act.identity,
        evidence_identity=event.material.get("evidence_of_yield_relation_identity"),
    )
    requirements = read_requirements_of_yield_relation(
        ledger,
        recorded_result_event_identity=event.identity,
        evidence_of_yield_relation_event_identity=event.material.get(
            "evidence_of_yield_relation_identity"
        ),
        responsible_act_evidence_event_identity=act.identity,
    )
    if (
        event.locality_identity != act.locality_identity
        or event.material != expected
        or not all(requirements.values())
    ):
        raise RecordedPairMeasurementComparisonError(
            "comparison result carries no exact Yield"
        )
    return deepcopy(event.material), assignment_reading


def get_recorded_pair_measurement_comparison(
    ledger: EventLedger, event_identity: str
) -> dict[str, Any]:
    return _recorded_pair_measurement_comparison_reading(
        ledger, event_identity
    )[0]
