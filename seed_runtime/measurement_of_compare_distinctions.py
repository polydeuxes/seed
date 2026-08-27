"""Measure every Distinction carried by one exact Compare result."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from typing import Any

from seed_runtime.comparison_of_ordered_relation_path_with_recorded_pair_findings import (
    COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_RESULT_KIND,
    get_recorded_comparison_of_ordered_relation_path_with_recorded_pair_findings,
)
from seed_runtime.event import Event
from seed_runtime.events import CORRUPTED, EventLedger
from seed_runtime.yield_relation import (
    RECORDED_YIELD_RELATION_EVENT,
    _record_yield_relation,
    read_requirements_of_yield_relation,
)


COMPARE_DISTINCTION_MEASUREMENT_SUBJECT_TO_ACT_BINDING_KIND = (
    "operator.measurement.compare_distinctions.subject_to_act_binding_recorded"
)
COMPARE_DISTINCTION_MEASUREMENT_ACT_OCCURRENCE_KIND = (
    "operator.measurement.compare_distinctions.act_occurrence_recorded"
)
COMPARE_DISTINCTION_MEASUREMENT_RESULT_KIND = (
    "operator.measurement.compare_distinctions.recorded"
)

BOOK_CLAUSE = "01.Source.D"
MEASUREMENT_ACT = "Measurement of exact Compare Distinctions"
MEASUREMENT_RESULT = "Measurement result of exact Compare Distinctions"

EVENT_KIND_BOOK_CLAUSES = {
    COMPARE_DISTINCTION_MEASUREMENT_SUBJECT_TO_ACT_BINDING_KIND: "01.Source.D",
    COMPARE_DISTINCTION_MEASUREMENT_ACT_OCCURRENCE_KIND: "02.Acts.A",
    COMPARE_DISTINCTION_MEASUREMENT_RESULT_KIND: "01.Source.D",
}


@dataclass(frozen=True)
class CompareDistinctionMeasurementSubject:
    comparison_result_occurrence_identity: str


def _identity(value: Any, message: str) -> str:
    if type(value) is not str or not value:
        raise ValueError(message)
    return value


def _binding_reference(binding: Event) -> dict[str, Any]:
    return {
        "recorded_occurrence_identity": binding.identity,
        "book_clause_identity": binding.material["book_clause_identity"],
        "exact_act_identity": binding.material["exact_act_identity"],
        "subject_reference": deepcopy(binding.material["subject_reference"]),
        "result_boundary_identity": binding.material["result_boundary_identity"],
    }


def _exact_distinctions(
    ledger: EventLedger,
    *,
    comparison_result_occurrence_identity: str,
    current_coordinates: dict[str, Any],
) -> tuple[dict[str, Any], ...]:
    comparisons = current_coordinates.get("comparison_result_occurrences")
    source = ledger.get(comparison_result_occurrence_identity)
    if (
        type(comparisons) is not dict
        or comparisons.get(comparison_result_occurrence_identity, object()) is not None
        or source is None
        or source.kind
        != COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_RESULT_KIND
        or source.locality_identity != current_coordinates.get("locality_identity")
        or ledger.integrity_of(source.identity) == CORRUPTED
    ):
        raise ValueError("Measurement requires one exact current Compare result")
    reading = get_recorded_comparison_of_ordered_relation_path_with_recorded_pair_findings(
        ledger,
        source.identity,
        prior_coordinates=current_coordinates,
    )
    finding = reading.get("finding")
    subject = finding.get("subject") if type(finding) is dict else None
    path_reference = (
        subject.get("ordered_relation_path_assertion_reference")
        if type(subject) is dict
        else None
    )
    comparison_reference = (
        subject.get("recorded_pair_comparison_result_reference")
        if type(subject) is dict
        else None
    )
    relation_findings = (
        finding.get("relation_findings") if type(finding) is dict else None
    )
    if (
        type(path_reference) is not dict
        or type(comparison_reference) is not dict
        or type(comparison_reference.get("recorded_occurrence_identity")) is not str
        or type(relation_findings) is not list
    ):
        raise ValueError("Measurement requires exact Compare Distinctions")

    distinctions = []
    for relation_finding in relation_findings:
        position_reference = (
            relation_finding.get("path_position_assertion_reference")
            if type(relation_finding) is dict
            else None
        )
        pair_subject = (
            relation_finding.get("pair_subject")
            if type(relation_finding) is dict
            else None
        )
        references = (
            relation_finding.get("comparison_finding_references")
            if type(relation_finding) is dict
            else None
        )
        if (
            type(position_reference) is not dict
            or type(pair_subject) is not list
            or len(pair_subject) != 2
            or not all(type(value) is int and 0 <= value <= 255 for value in pair_subject)
            or type(references) is not list
        ):
            raise ValueError("Measurement requires exact Compare Distinctions")
        for reference in references:
            if (
                type(reference) is not dict
                or set(reference)
                != {
                    "recorded_comparison_occurrence_identity",
                    "finding_category",
                    "finding_position",
                    "subject",
                }
                or reference.get("recorded_comparison_occurrence_identity")
                != comparison_reference["recorded_occurrence_identity"]
                or type(reference.get("finding_position")) is not int
                or reference["finding_position"] < 0
                or type(reference.get("subject")) is not dict
                or reference["subject"].get("content") != pair_subject
            ):
                raise ValueError("Measurement requires exact Compare Distinctions")
            distinctions.append(
                {
                    "ordered_relation_path_assertion_reference": deepcopy(
                        path_reference
                    ),
                    "path_position_assertion_reference": deepcopy(
                        position_reference
                    ),
                    "pair_subject": deepcopy(pair_subject),
                    "recorded_finding_reference": deepcopy(reference),
                }
            )
    return tuple(distinctions)


def _source_coordinates(
    ledger: EventLedger,
    *,
    comparison_result_occurrence_identity: str,
    current_coordinates: dict[str, Any] | None,
) -> tuple[dict[str, Any], tuple[dict[str, Any], ...]]:
    if current_coordinates is None:
        from seed_runtime.operator_current_coordinates import (
            read_operator_current_coordinates,
        )

        source = ledger.get(comparison_result_occurrence_identity)
        if source is None or type(source.locality_identity) is not str:
            raise ValueError("Measurement requires one exact Compare result")
        current_coordinates = read_operator_current_coordinates(
            ledger,
            locality_identity=source.locality_identity,
        )
    distinctions = _exact_distinctions(
        ledger,
        comparison_result_occurrence_identity=comparison_result_occurrence_identity,
        current_coordinates=current_coordinates,
    )
    return current_coordinates, distinctions


def _binding_material(
    *,
    comparison_result_occurrence_identity: str,
    locality_identity: str,
    through_event_occurrence_identity: str,
    exact_act_identity: str,
    act_occurrence_identity: str,
    measurement_result_identity: str,
) -> dict[str, Any]:
    return {
        "subject_reference": {
            "comparison_result_occurrence_identity": (
                comparison_result_occurrence_identity
            ),
        },
        "exact_act_identity": exact_act_identity,
        "act_occurrence_identity": act_occurrence_identity,
        "measurement_result_identity": measurement_result_identity,
        "result_boundary_identity": measurement_result_identity,
        "book_clause_identity": BOOK_CLAUSE,
        "source_locality_identity": locality_identity,
        "through_event_occurrence_identity": through_event_occurrence_identity,
    }


def record_compare_distinction_measurement_subject_to_act_binding(
    ledger: EventLedger,
    *,
    comparison_result_occurrence_identity: str,
    current_coordinates: dict[str, Any],
) -> Event:
    """Record one complete Compare-result subject before Measurement."""

    if not isinstance(ledger, EventLedger) or type(current_coordinates) is not dict:
        raise TypeError("Measurement requires an EventLedger and current coordinates")
    current_coordinates, _distinctions = _source_coordinates(
        ledger,
        comparison_result_occurrence_identity=(
            comparison_result_occurrence_identity
        ),
        current_coordinates=current_coordinates,
    )
    locality_identity = _identity(
        current_coordinates.get("locality_identity"),
        "Measurement requires one exact Locality",
    )
    through_event_occurrence_identity = _identity(
        current_coordinates.get("through_event_occurrence_identity"),
        "Measurement requires one exact through-occurrence boundary",
    )
    boundary = ledger.get(through_event_occurrence_identity)
    if (
        boundary is None
        or boundary.locality_identity != locality_identity
        or ledger.integrity_of(boundary.identity) == CORRUPTED
        or ledger.append_boundary_through_occurrence(boundary.identity)
        != ledger.append_boundary()
    ):
        raise ValueError("Measurement requires exact current coordinates")
    identities = {
        "exact_act_identity": ledger.mint_identity(
            "compare_distinction_measurement_act"
        ),
        "act_occurrence_identity": ledger.mint_identity(
            "compare_distinction_measurement_occurrence"
        ),
        "measurement_result_identity": ledger.mint_identity(
            "compare_distinction_measurement_result"
        ),
    }
    return ledger.append(
        COMPARE_DISTINCTION_MEASUREMENT_SUBJECT_TO_ACT_BINDING_KIND,
        _binding_material(
            comparison_result_occurrence_identity=(
                comparison_result_occurrence_identity
            ),
            locality_identity=locality_identity,
            through_event_occurrence_identity=through_event_occurrence_identity,
            **identities,
        ),
        locality_identity=locality_identity,
    )


def _read_binding(
    ledger: EventLedger,
    binding_event_identity: str,
    *,
    prior_coordinates: dict[str, Any] | None = None,
) -> tuple[Event, tuple[dict[str, Any], ...]]:
    binding = ledger.get(binding_event_identity)
    if (
        binding is None
        or binding.kind
        != COMPARE_DISTINCTION_MEASUREMENT_SUBJECT_TO_ACT_BINDING_KIND
        or type(binding.locality_identity) is not str
        or ledger.integrity_of(binding.identity) == CORRUPTED
    ):
        raise ValueError("Compare Distinction Measurement binding is not exact")
    subject = binding.material.get("subject_reference")
    source_identity = (
        subject.get("comparison_result_occurrence_identity")
        if type(subject) is dict
        else None
    )
    through_identity = binding.material.get("through_event_occurrence_identity")
    if prior_coordinates is None:
        from seed_runtime.operator_current_coordinates import (
            read_operator_current_coordinates_through,
        )

        prior_coordinates = read_operator_current_coordinates_through(
            ledger,
            locality_identity=binding.locality_identity,
            through_event_occurrence_identity=through_identity,
        )
    distinctions = _exact_distinctions(
        ledger,
        comparison_result_occurrence_identity=source_identity,
        current_coordinates=prior_coordinates,
    )
    identities = {
        coordinate: _identity(
            binding.material.get(coordinate),
            "Compare Distinction Measurement binding is not exact",
        )
        for coordinate in (
            "exact_act_identity",
            "act_occurrence_identity",
            "measurement_result_identity",
        )
    }
    carried_bindings = prior_coordinates.get(
        "subject_to_act_binding_occurrences"
    )
    binding_is_carried = (
        type(carried_bindings) is dict
        and carried_bindings.get(binding.identity, object()) is None
    )
    if (
        len(set(identities.values())) != 3
        or prior_coordinates.get("locality_identity") != binding.locality_identity
        or (
            prior_coordinates.get("through_event_occurrence_identity")
            != through_identity
            and not binding_is_carried
        )
        or binding.material
        != _binding_material(
            comparison_result_occurrence_identity=source_identity,
            locality_identity=binding.locality_identity,
            through_event_occurrence_identity=through_identity,
            **identities,
        )
    ):
        raise ValueError("Compare Distinction Measurement binding is not exact")
    return binding, distinctions


def _act_material(binding: Event) -> dict[str, Any]:
    return {
        "addressed_act_identity": binding.material["exact_act_identity"],
        "act_occurrence_identity": binding.material["act_occurrence_identity"],
        "act": MEASUREMENT_ACT,
        "subject_to_act_binding_reference": _binding_reference(binding),
        "source_locality_identity": binding.locality_identity,
    }


def record_compare_distinction_measurement_act_occurrence(
    ledger: EventLedger,
    *,
    binding_event_identity: str,
    current_coordinates: dict[str, Any],
) -> Event:
    """Record the Measurement Act occurrence from its current binding."""

    binding, _distinctions = _read_binding(
        ledger,
        binding_event_identity,
        prior_coordinates=current_coordinates,
    )
    bindings = current_coordinates.get("subject_to_act_binding_occurrences")
    if (
        current_coordinates.get("locality_identity") != binding.locality_identity
        or current_coordinates.get("through_event_occurrence_identity")
        != binding.identity
        or type(bindings) is not dict
        or bindings.get(binding.identity, object()) is not None
    ):
        raise ValueError("Measurement Act requires its exact current binding")
    if any(
        event.material.get("subject_to_act_binding_reference")
        == _binding_reference(binding)
        for event in ledger.iter_locality_kind(
            binding.locality_identity,
            COMPARE_DISTINCTION_MEASUREMENT_ACT_OCCURRENCE_KIND,
        )
    ):
        raise ValueError("Measurement binding already carries an Act occurrence")
    return ledger.append(
        COMPARE_DISTINCTION_MEASUREMENT_ACT_OCCURRENCE_KIND,
        _act_material(binding),
        locality_identity=binding.locality_identity,
    )


def _read_act(
    ledger: EventLedger,
    act_event_identity: str,
    *,
    prior_coordinates: dict[str, Any] | None = None,
) -> tuple[Event, Event, tuple[dict[str, Any], ...]]:
    act = ledger.get(act_event_identity)
    reference = act.material.get("subject_to_act_binding_reference") if act else None
    if (
        act is None
        or act.kind != COMPARE_DISTINCTION_MEASUREMENT_ACT_OCCURRENCE_KIND
        or type(reference) is not dict
        or ledger.integrity_of(act.identity) == CORRUPTED
    ):
        raise ValueError("Compare Distinction Measurement Act is not exact")
    binding, distinctions = _read_binding(
        ledger,
        reference.get("recorded_occurrence_identity"),
        prior_coordinates=prior_coordinates,
    )
    if (
        act.locality_identity != binding.locality_identity
        or reference != _binding_reference(binding)
        or act.material != _act_material(binding)
    ):
        raise ValueError("Compare Distinction Measurement Act is not exact")
    ledger.occurrences_in_append_order(
        (binding.identity, act.identity),
        locality_identity=act.locality_identity,
    )
    return act, binding, distinctions


def _result_material(
    binding: Event,
    distinctions: tuple[dict[str, Any], ...],
) -> dict[str, Any]:
    source_identity = binding.material["subject_reference"][
        "comparison_result_occurrence_identity"
    ]
    return {
        "result_identity": binding.material["measurement_result_identity"],
        "addressed_act_identity": binding.material["exact_act_identity"],
        "act_occurrence_identity": binding.material["act_occurrence_identity"],
        "exact_act": MEASUREMENT_ACT,
        "subject_to_act_binding_reference": _binding_reference(binding),
        "source_result_occurrence_identity": source_identity,
        "completeness_boundary": {
            "source_result_occurrence_identity": source_identity,
            "distinction_count": len(distinctions),
        },
        "findings": deepcopy(list(distinctions)),
        "source_locality_identity": binding.locality_identity,
    }


def _recorded_result_material(
    binding: Event,
    distinctions: tuple[dict[str, Any], ...],
    *,
    act_occurrence_event_identity: str,
    yield_relation_identity: str,
) -> dict[str, Any]:
    result = _result_material(binding, distinctions)
    return {
        "result_identity": result["result_identity"],
        "addressed_act_identity": result["addressed_act_identity"],
        "act_occurrence_identity": result["act_occurrence_identity"],
        "exact_act": result["exact_act"],
        "subject_to_act_binding_reference": deepcopy(
            result["subject_to_act_binding_reference"]
        ),
        "source_result_occurrence_identity": result[
            "source_result_occurrence_identity"
        ],
        "completeness_boundary": deepcopy(result["completeness_boundary"]),
        "findings": deepcopy(result["findings"]),
        "source_locality_identity": result["source_locality_identity"],
        "act_occurrence_event_identity": act_occurrence_event_identity,
        "yield_relation_identity": yield_relation_identity,
    }


def record_compare_distinction_measurement_result(
    ledger: EventLedger,
    *,
    act_occurrence_event_identity: str,
) -> Event:
    """Record the Yield and complete Measurement result."""

    act, binding, distinctions = _read_act(
        ledger,
        act_occurrence_event_identity,
    )
    if any(
        event.material.get("act_occurrence_event_identity") == act.identity
        for event in ledger.iter_locality_kind(
            act.locality_identity,
            COMPARE_DISTINCTION_MEASUREMENT_RESULT_KIND,
        )
    ):
        raise ValueError("Measurement Act already carries a result")
    result = _result_material(binding, distinctions)
    yield_relation = _record_yield_relation(
        ledger,
        locality_identity=act.locality_identity,
        exact_act=MEASUREMENT_ACT,
        act_occurrence_identity=act.material["act_occurrence_identity"],
        act_occurrence_event_identity=act.identity,
        result_kind=MEASUREMENT_RESULT,
        result_identity=result["result_identity"],
        result_content=result,
        occurrence_boundary="compare_distinction_measurement",
    )
    return ledger.append(
        COMPARE_DISTINCTION_MEASUREMENT_RESULT_KIND,
        _recorded_result_material(
            binding,
            distinctions,
            act_occurrence_event_identity=act.identity,
            yield_relation_identity=yield_relation.identity,
        ),
        locality_identity=act.locality_identity,
    )


def get_recorded_compare_distinction_measurement(
    ledger: EventLedger,
    result_event_identity: str,
    *,
    prior_coordinates: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Read one complete Compare Distinction Measurement result."""

    result = ledger.get(result_event_identity)
    if (
        result is None
        or result.kind != COMPARE_DISTINCTION_MEASUREMENT_RESULT_KIND
        or ledger.integrity_of(result.identity) == CORRUPTED
    ):
        raise ValueError("Compare Distinction Measurement result is not exact")
    act, binding, distinctions = _read_act(
        ledger,
        result.material.get("act_occurrence_event_identity"),
        prior_coordinates=prior_coordinates,
    )
    expected = _recorded_result_material(
        binding,
        distinctions,
        act_occurrence_event_identity=act.identity,
        yield_relation_identity=result.material.get("yield_relation_identity"),
    )
    yield_identity = result.material.get("yield_relation_identity")
    yield_event = ledger.get(yield_identity) if type(yield_identity) is str else None
    requirements = read_requirements_of_yield_relation(
        ledger,
        recorded_result_event_identity=result.identity,
        yield_relation_event_identity=yield_identity,
        act_occurrence_event_identity=act.identity,
    )
    if (
        result.locality_identity != act.locality_identity
        or result.material != expected
        or yield_event is None
        or yield_event.kind != RECORDED_YIELD_RELATION_EVENT
        or yield_event.material.get("occurrence_boundary")
        != "compare_distinction_measurement"
        or yield_event.material.get("result_kind") != MEASUREMENT_RESULT
        or not all(requirements.values())
    ):
        raise ValueError("Compare Distinction Measurement result is not exact")
    ledger.occurrences_in_append_order(
        (act.identity, yield_event.identity, result.identity),
        locality_identity=result.locality_identity,
    )
    return deepcopy(result.material)
