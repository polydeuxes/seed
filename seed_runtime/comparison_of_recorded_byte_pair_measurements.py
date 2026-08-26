"""Responsible comparison of earlier and later recorded byte-pair Measurements."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from seed_runtime.byte_measurement import (
    BYTE_PAIR_MEASUREMENT_RECORDED_KIND,
    _RecordedBytePairFinding,
    _validated_recorded_byte_position_pair_measurement,
    get_byte_position_pair_measurement_subject_to_act_binding,
)
from seed_runtime.event import Event
from seed_runtime.events import CORRUPTED, EventLedger
from seed_runtime.yield_relation import (
    RECORDED_YIELD_RELATION_EVENT,
    _record_yield_relation,
    read_requirements_of_yield_relation,
)
from seed_runtime.identities import new_identity
from seed_runtime.material_source import read_exact_material_result
from seed_runtime.operator_invocation_locality import (
    OPERATOR_INVOCATION_LOCALITY_RECORDED_KIND,
    get_recorded_operator_invocation_locality,
)


RECORDED_PAIR_MEASUREMENT_COMPARISON_RESPONSIBILITY_ASSIGNMENT_KIND = (
    "recorded_pair_measurement_comparison.responsibility_assignment_recorded"
)
RECORDED_PAIR_MEASUREMENT_COMPARISON_APPLICABILITY_ACT_OCCURRENCE_EVENT = (
    "recorded_pair_measurement_comparison.applicability_act_occurrence_recorded"
)
RECORDED_PAIR_MEASUREMENT_COMPARISON_APPLICABILITY_RESULT_KIND = (
    "recorded_pair_measurement_comparison.applicability_recorded"
)
RECORDED_PAIR_MEASUREMENT_COMPARISON_ACT_OCCURRENCE_EVENT = (
    "recorded_pair_measurement_comparison.act_occurrence_recorded"
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
    "Applicability and Compare earlier and later exact carried byte-position-pair "
    "Measurement results within one operator material acquisition at prior Standing"
)
RECORDED_PAIR_MEASUREMENT_COMPARISON_ACT = (
    "Compare earlier and later exact carried byte-position-pair Measurement results"
)
RECORDED_PAIR_MEASUREMENT_COMPARISON_APPLICABILITY_ACT = (
    "Applicability of earlier and later recorded Measurement results to one Compare"
)

EVENT_KIND_RESPONSIBILITIES = {
    RECORDED_PAIR_MEASUREMENT_COMPARISON_RESPONSIBILITY_ASSIGNMENT_KIND: "04.Compare.A",
    RECORDED_PAIR_MEASUREMENT_COMPARISON_APPLICABILITY_ACT_OCCURRENCE_EVENT: "02.Acts.A",
    RECORDED_PAIR_MEASUREMENT_COMPARISON_APPLICABILITY_RESULT_KIND: "01.Current.E.1",
    RECORDED_PAIR_MEASUREMENT_COMPARISON_ACT_OCCURRENCE_EVENT: "02.Acts.A",
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

    from seed_runtime.operator_material_source import (
        OPERATOR_MATERIAL_SOURCE_RECORDED_KIND,
        get_recorded_operator_material_source,
    )

    provenance = added.material.get("provenance_occurrence_references")
    reference = (
        added.identity
        if added.kind == OPERATOR_MATERIAL_SOURCE_RECORDED_KIND
        else provenance[0]
        if type(provenance) is list and len(provenance) == 1
        else None
    )
    acquired_event = ledger.get(reference) if type(reference) is str else None
    try:
        acquired = get_recorded_operator_material_source(ledger, reference)
    except (TypeError, ValueError) as error:
        raise RecordedPairMeasurementComparisonError(
            "later Measurement requires one exact operator acquisition occurrence"
        ) from error
    if (
        acquired_event is None
        or acquired_event.kind != OPERATOR_MATERIAL_SOURCE_RECORDED_KIND
        or acquired_event.locality_identity != added.locality_identity
        or acquired_event.exact_material != added.exact_material
    ):
        raise RecordedPairMeasurementComparisonError(
            "later Measurement requires one exact operator acquisition occurrence"
        )
    return acquired_event, acquired


def _operator_source_current_coordinate_reference(
    ledger: EventLedger,
    *,
    source_material: dict[str, Any],
    earlier_measurement: Event,
    earlier_source_occurrence_references: tuple[str, ...],
) -> dict[str, str]:
    from seed_runtime.operator_current_coordinates import (
        read_operator_current_coordinates_through,
    )

    reference = source_material.get("current_coordinate_reference")
    if (
        type(reference) is not dict
        or reference.get("locality_identity")
        != earlier_measurement.locality_identity
        or type(reference.get("through_event_occurrence_identity")) is not str
    ):
        raise RecordedPairMeasurementComparisonError(
            "later Measurement requires one exact operator source occurrence"
        )
    try:
        coordinates = read_operator_current_coordinates_through(
            ledger,
            locality_identity=earlier_measurement.locality_identity,
            through_event_occurrence_identity=reference[
                "through_event_occurrence_identity"
            ],
        )
    except (TypeError, ValueError) as error:
        raise RecordedPairMeasurementComparisonError(
            "operator source occurrence carries no exact prior coordinates"
        ) from error
    carried_sources = {
        occurrence.get("result_occurrence_identity")
        for occurrence in coordinates.get(
            "material_result_occurrences", ()
        )
        if type(occurrence) is dict
    }
    if (
        earlier_measurement.identity
        not in coordinates.get("measurement_occurrences", {})
        or any(
            occurrence not in carried_sources
            for occurrence in earlier_source_occurrence_references
        )
    ):
        raise RecordedPairMeasurementComparisonError(
            "operator source occurrence carries no exact prior coordinates"
        )
    return deepcopy(reference)


def _measurement_reference(event: Event) -> dict[str, str]:
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
    return event, findings, reading.binding


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
        content = (
            subject.get("content") if type(subject) is dict else None
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
            or type(content) is not list
            or len(content) != 2
            or any(type(value) is not int for value in content)
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
                content=tuple(content),
                result=result,
                _content_coordinates=content_coordinates,
                _local_support_assertion_positions=tuple(local_support),
            )
        )
    return tuple(findings)


def _source_occurrence_references(
    ledger: EventLedger, event: Event
) -> tuple[str, ...]:
    reference = event.material.get("subject_to_act_binding_reference")
    assignment_event = get_byte_position_pair_measurement_subject_to_act_binding(
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
        item.get("material_result_occurrence_identity") if type(item) is dict else None
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
            read_exact_material_result(ledger, added.identity)
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
    operator_material_source_result_event_identity = None
    operator_material_source_current_coordinate_reference = None
    if source_role == "this Witness":
        raise RecordedPairMeasurementComparisonError(
            "Witness provenance establishes no comparison input relation"
        )
    elif source_role == "this operator":
        acquired_event, acquired = _operator_acquisition_for_material_result(
            ledger, added
        )
        source_coordinate_reference = (
            _operator_source_current_coordinate_reference(
                ledger,
                source_material=acquired,
                earlier_measurement=earlier,
                earlier_source_occurrence_references=earlier_sources,
            )
        )
        operator_material_source_result_event_identity = acquired_event.identity
        operator_material_source_current_coordinate_reference = deepcopy(
            source_coordinate_reference
        )
        input_relation = "operator material source occurrence after prior coordinates"
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
            f"added occurrence carries {len(invocation_relations)} distinct operator "
            "invocation Locality relations"
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
        "operator_material_source_result_event_identity": (
            operator_material_source_result_event_identity
        ),
        "operator_material_source_current_coordinate_reference": (
            operator_material_source_current_coordinate_reference
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
            read_exact_material_result(ledger, added.identity)
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
    source_coordinate_reference = None
    if source_role == "this operator":
        acquired, acquired_material = _operator_acquisition_for_material_result(
            ledger, added
        )
        exact_results = locality_standing.get("exact_result_occurrences")
        if (
            acquired.locality_identity != earlier.locality_identity
            or acquired.exact_material != added.exact_material
            or type(exact_results) is not dict
            or acquired.identity not in exact_results
        ):
            raise RecordedPairMeasurementComparisonError(
                "operator source occurrence carries no exact prior coordinates"
            )
        source_coordinate_reference = (
            _operator_source_current_coordinate_reference(
                ledger,
                source_material=acquired_material,
                earlier_measurement=earlier,
                earlier_source_occurrence_references=earlier_sources,
            )
        )
        acquisition_identity = acquired.identity
        input_relation = "operator material source occurrence after prior coordinates"
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
            f"added occurrence carries {len(invocation_relations)} distinct operator "
            "invocation Locality relations"
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
        "operator_material_source_result_event_identity": acquisition_identity,
        "operator_material_source_current_coordinate_reference": deepcopy(
            source_coordinate_reference
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


def _assignment_reference(
    assignment: Event, *, result_boundary_identity: str
) -> dict[str, Any]:
    return {
        "recorded_occurrence_identity": assignment.identity,
        "book_clause_identity": assignment.material["book_clause_identity"],
        "exact_act_identity": assignment.material["exact_act_identity"],
        "subject_reference": deepcopy(assignment.material["subject_reference"]),
        "result_boundary_identity": result_boundary_identity,
    }


def _assignment_material(
    *,
    inputs: dict[str, Any],
    standing_boundary_identity: str,
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
        "subject_reference": {
            "earlier_measurement_reference": _measurement_reference(
                inputs["earlier_event"]
            ),
            "later_measurement_reference": _measurement_reference(
                inputs["later_event"]
            ),
        },
        "exact_act_identity": comparison_act_identity,
        "applicability_act_identity": applicability_act_identity,
        "applicability_act_occurrence_identity": applicability_act_occurrence_identity,
        "applicability_result_identity": applicability_result_identity,
        "comparison_act_identity": comparison_act_identity,
        "comparison_act_occurrence_identity": comparison_act_occurrence_identity,
        "comparison_result_identity": comparison_result_identity,
        "result_boundary_identity": comparison_result_identity,
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
        "operator_material_source_result_event_identity": inputs[
            "operator_material_source_result_event_identity"
        ],
        "operator_material_source_current_coordinate_reference": deepcopy(
            inputs["operator_material_source_current_coordinate_reference"]
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
            "operator_material_source_result_event_identity": inputs[
                "operator_material_source_result_event_identity"
            ],
            "operator_material_source_current_coordinate_reference": deepcopy(
                inputs["operator_material_source_current_coordinate_reference"]
            ),
            "destination_operator_locality_identity": inputs[
                "operator_locality_identity"
            ],
        },
        "unknown": [],
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
        locality_standing.get("subject_to_act_binding_occurrences")
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
        "responsibility_assignment_reference": _assignment_reference(
            assignment,
            result_boundary_identity=material["applicability_result_identity"],
        ),
        "applicability_of_input_to_compare": (
            _applicability_of_input_to_compare(assignment)
        ),
        "comparison_rule": RECORDED_PAIR_MEASUREMENT_COMPARISON_RULE,
        "scope": deepcopy(material["scope"]),
    }


def record_recorded_pair_measurement_comparison_applicability_act_occurrence(
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
        RECORDED_PAIR_MEASUREMENT_COMPARISON_APPLICABILITY_ACT_OCCURRENCE_EVENT,
        _applicability_act_material(assignment),
        locality_identity=assignment.locality_identity,
    )


def _applicability_act_reading(
    ledger: EventLedger,
    event_identity: str,
    *,
    assignment_reading: _AssignmentReading | None = None,
) -> tuple[Event, _AssignmentReading]:
    event = ledger.get(_identity(event_identity, "comparison requires Applicability Act occurrence"))
    if (
        event is None
        or event.kind
        != RECORDED_PAIR_MEASUREMENT_COMPARISON_APPLICABILITY_ACT_OCCURRENCE_EVENT
        or event.exact_material is not None
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise RecordedPairMeasurementComparisonError(
            "comparison Applicability Act occurrence is absent or corrupted"
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
            "comparison Applicability Act occurrence is not exact"
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


def get_recorded_pair_measurement_comparison_applicability_act_occurrence(
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
        "unknown": [],
    }


def _recorded_applicability_result_material(
    material: dict[str, Any], *, act_identity: str, yield_relation_identity: str
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
        "unknown": list(material["unknown"]),
        "act_occurrence_event_identity": act_identity,
        "yield_relation_identity": yield_relation_identity,
    }


def record_recorded_pair_measurement_comparison_applicability_result(
    ledger: EventLedger, *, act_occurrence_event_identity: str
) -> Event:
    act = get_recorded_pair_measurement_comparison_applicability_act_occurrence(
        ledger, act_occurrence_event_identity
    )
    result = _applicability_result_material(act)
    return _record_applicability_result_from_act(ledger, act=act, result=result)


def _record_applicability_result_from_act(
    ledger: EventLedger, *, act: Event, result: dict[str, Any]
) -> Event:
    yield_relation = _record_yield_relation(
        ledger,
        locality_identity=act.locality_identity,
        exact_act=RECORDED_PAIR_MEASUREMENT_COMPARISON_APPLICABILITY_ACT,
        act_occurrence_identity=act.material["act_occurrence_identity"],
        act_occurrence_event_identity=act.identity,
        result_kind="recorded pair Measurement comparison Applicability result",
        result_identity=result["result_identity"],
        result_content=result,
        occurrence_boundary="recorded_pair_measurement_comparison_applicability",
    )
    return ledger.append(
        RECORDED_PAIR_MEASUREMENT_COMPARISON_APPLICABILITY_RESULT_KIND,
        _recorded_applicability_result_material(
            result, act_identity=act.identity, yield_relation_identity=yield_relation.identity
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
            event.material.get("act_occurrence_event_identity"),
            assignment_reading=assignment_reading,
        )
    )
    expected = _recorded_applicability_result_material(
        _applicability_result_material(act),
        act_identity=act.identity,
        yield_relation_identity=event.material.get("yield_relation_identity"),
    )
    requirements = read_requirements_of_yield_relation(
        ledger,
        recorded_result_event_identity=event.identity,
        yield_relation_event_identity=event.material.get(
            "yield_relation_identity"
        ),
        act_occurrence_event_identity=act.identity,
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
        locality_standing.get("subject_to_act_binding_occurrences")
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
        "responsibility_assignment_reference": _assignment_reference(
            assignment,
            result_boundary_identity=material["comparison_result_identity"],
        ),
        "applicability_result_event_identity": applicability.identity,
        "applicability_of_input_to_compare": deepcopy(
            applicability.material["applicability_of_input_to_compare"]
        ),
        "participation_of_input_in_compare": (
            _participation_of_input_in_compare(assignment)
        ),
        "comparison_rule": RECORDED_PAIR_MEASUREMENT_COMPARISON_RULE,
        "scope": deepcopy(material["scope"]),
    }


def record_recorded_pair_measurement_comparison_act_occurrence(
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
        != _assignment_reference(
            assignment,
            result_boundary_identity=assignment.material[
                "applicability_result_identity"
            ],
        )
    ):
        raise RecordedPairMeasurementComparisonError(
            "Compare Applicability names another assignment"
        )
    _require_applicability_standing(
        assignment, applicability, locality_standing
    )
    return ledger.append(
        RECORDED_PAIR_MEASUREMENT_COMPARISON_ACT_OCCURRENCE_EVENT,
        _comparison_act_material(assignment, applicability),
        locality_identity=assignment.locality_identity,
    )


def _comparison_act_reading(
    ledger: EventLedger,
    event_identity: str,
    *,
    assignment_reading: _AssignmentReading | None = None,
) -> tuple[Event, _AssignmentReading, Event]:
    event = ledger.get(_identity(event_identity, "comparison requires Act occurrence"))
    if (
        event is None
        or event.kind != RECORDED_PAIR_MEASUREMENT_COMPARISON_ACT_OCCURRENCE_EVENT
        or event.exact_material is not None
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise RecordedPairMeasurementComparisonError(
            "comparison Act occurrence is absent or corrupted"
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
            "comparison Act occurrence carries no Applicability"
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
            "comparison Act occurrence is not exact"
        )
    return event, assignment_reading, applicability


def get_recorded_pair_measurement_comparison_act_occurrence(
    ledger: EventLedger, event_identity: str
) -> Event:
    return _comparison_act_reading(ledger, event_identity)[0]


def _finding_key(finding: Any) -> tuple[str, tuple[int, int] | None]:
    return finding.result, finding.exact_pair


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
            "content": list(key[1]) if key[1] is not None else None,
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
                    "content": list(key[1]) if key[1] is not None else None,
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
        "unknown": [],
    }


def _recorded_comparison_result_material(
    material: dict[str, Any], *, act_identity: str, yield_relation_identity: str
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
        "unknown": list(material["unknown"]),
        "act_occurrence_event_identity": act_identity,
        "yield_relation_identity": yield_relation_identity,
    }


def record_recorded_pair_measurement_comparison_result(
    ledger: EventLedger, *, act_occurrence_event_identity: str
) -> Event:
    act, assignment_reading, _applicability = (
        _comparison_act_reading(
            ledger, act_occurrence_event_identity
        )
    )
    result = _comparison_result_material(act, assignment_reading)
    return _record_comparison_result_from_act(ledger, act=act, result=result)


def _record_comparison_result_from_act(
    ledger: EventLedger, *, act: Event, result: dict[str, Any]
) -> Event:
    yield_relation = _record_yield_relation(
        ledger,
        locality_identity=act.locality_identity,
        exact_act=RECORDED_PAIR_MEASUREMENT_COMPARISON_ACT,
        act_occurrence_identity=act.material["act_occurrence_identity"],
        act_occurrence_event_identity=act.identity,
        result_kind="recorded pair Measurement comparison result",
        result_identity=result["result_identity"],
        result_content=result,
        occurrence_boundary="recorded_pair_measurement_comparison",
    )
    return ledger.append(
        RECORDED_PAIR_MEASUREMENT_COMPARISON_RESULT_KIND,
        _recorded_comparison_result_material(
            result, act_identity=act.identity, yield_relation_identity=yield_relation.identity
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

    from seed_runtime.operator_current_coordinates import (
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
        RECORDED_PAIR_MEASUREMENT_COMPARISON_APPLICABILITY_ACT_OCCURRENCE_EVENT,
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
        RECORDED_PAIR_MEASUREMENT_COMPARISON_ACT_OCCURRENCE_EVENT,
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
            event.material.get("act_occurrence_event_identity"),
            assignment_reading=assignment_reading,
        )
    )
    expected = _recorded_comparison_result_material(
        _comparison_result_material(
            act, assignment_reading
        ),
        act_identity=act.identity,
        yield_relation_identity=event.material.get("yield_relation_identity"),
    )
    requirements = read_requirements_of_yield_relation(
        ledger,
        recorded_result_event_identity=event.identity,
        yield_relation_event_identity=event.material.get(
            "yield_relation_identity"
        ),
        act_occurrence_event_identity=act.identity,
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
