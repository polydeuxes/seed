"""Compare each exact shared-position pair of source-position material."""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Iterator, NamedTuple

from seed_runtime.event import Event
from seed_runtime.events import CORRUPTED, EventLedger
from seed_runtime.measurement_of_shared_position_of_byte_pair_occurrences import (
    SHARED_POSITION_MEASUREMENT_RESULT_KIND,
    source_position_coordinates_of_shared_position_result,
)


APPLICABILITY_ACT_KIND = (
    "operator.comparison_of_shared_position_source_position_material."
    "applicability_act_recorded"
)
COMPARE_SUBJECT_TO_ACT_BINDING_RECORDED_EVENT = (
    "operator.comparison_of_shared_position_source_position_material."
    "compare_subject_to_act_binding_recorded"
)
APPLICABILITY_SUBJECT_TO_ACT_BINDING_RECORDED_EVENT = (
    "operator.comparison_of_shared_position_source_position_material."
    "applicability_subject_to_act_binding_recorded"
)
APPLICABILITY_RESULT_KIND = (
    "operator.comparison_of_shared_position_source_position_material."
    "applicability_result_recorded"
)
COMPARE_ACT_KIND = (
    "operator.comparison_of_shared_position_source_position_material."
    "compare_act_recorded"
)
COMPARE_RESULT_KIND = (
    "operator.comparison_of_shared_position_source_position_material."
    "compare_result_recorded"
)

BOOK_CLAUSE = "04.Compare"
APPLICABILITY_ACT = (
    "Applicability of same-position Measurement source position material to Compare"
)
COMPARE_ACT = "Compare same-position Measurement source position material"
EVENT_KIND_BOOK_CLAUSES = {
    COMPARE_SUBJECT_TO_ACT_BINDING_RECORDED_EVENT: "04.Compare",
    APPLICABILITY_SUBJECT_TO_ACT_BINDING_RECORDED_EVENT: "01.Current.E.1",
    APPLICABILITY_ACT_KIND: "02.Acts.A",
    APPLICABILITY_RESULT_KIND: "01.Current.E.1",
    COMPARE_ACT_KIND: "02.Acts.A",
    COMPARE_RESULT_KIND: "04.Compare",
}


class SharedPositionSourcePositionMaterialComparison(NamedTuple):
    current_coordinates: dict[str, Any]
    result_occurrence: Event


_IDENTITY_COORDINATES = (
    "applicability_act_identity",
    "applicability_act_occurrence_identity",
    "applicability_result_identity",
    "compare_act_identity",
    "compare_act_occurrence_identity",
    "compare_result_identity",
)
_APPLICABILITY_IDENTITY_COORDINATES = (
    "exact_act_identity",
    "applicability_act_occurrence_identity",
    "applicability_result_identity",
)
_COMPARE_IDENTITY_COORDINATES = (
    "exact_act_identity",
    "compare_act_occurrence_identity",
    "compare_result_identity",
)

_SOURCE_POSITION_PAIRS = ((0, 1), (0, 2), (1, 2))


def _identity(value: Any, message: str) -> str:
    if type(value) is not str or not value:
        raise ValueError(message)
    return value


def _event(
    ledger: EventLedger, identity: Any, *, event_kind: str, message: str
) -> Event:
    event = ledger.get(_identity(identity, message))
    if (
        event is None
        or event.kind != event_kind
        or event.exact_material is not None
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise ValueError(message)
    return event


def _result_reference(event: Event) -> dict[str, str]:
    return {
        "recorded_occurrence_identity": event.identity,
        "result_identity": event.material["result_identity"],
        "act_occurrence_identity": event.material["act_occurrence_identity"],
        "act_occurrence_event_identity": event.material[
            "act_occurrence_event_identity"
        ],
    }


def _shared_position_input(
    ledger: EventLedger,
    shared_position_measurement_result_event_identity: Any,
    *,
    source_position_pair: tuple[int, int],
    current_coordinates: dict[str, Any],
) -> dict[str, Any]:
    event = _event(
        ledger,
        shared_position_measurement_result_event_identity,
        event_kind=SHARED_POSITION_MEASUREMENT_RESULT_KIND,
        message="source position Compare requires an exact shared-position Measurement result",
    )
    shared_position, positions = (
        source_position_coordinates_of_shared_position_result(
            ledger, event.identity, prior_coordinates=current_coordinates
        )
    )
    if len(positions) != 3:
        raise ValueError("source position Compare requires exact ordered positions")
    if source_position_pair not in _SOURCE_POSITION_PAIRS:
        raise ValueError("source position Compare requires a shared-position pair")
    first_source_position_index, second_source_position_index = source_position_pair
    for coordinate in positions:
        material = coordinate.get("exact_material")
        if (
            set(coordinate)
            != {
                "source_material_result_occurrence_identity",
                "locality_identity",
                "completeness_boundary_identity",
                "position",
                "exact_material",
            }
            or type(coordinate.get("position")) is not int
            or type(material) is not list
            or len(material) != 1
            or type(material[0]) is not int
            or not 0 <= material[0] <= 255
            or coordinate.get("locality_identity") != event.locality_identity
        ):
            raise ValueError(
                "source position Compare requires exact position coordinates"
            )
    if any(
        coordinate["source_material_result_occurrence_identity"]
        != positions[0]["source_material_result_occurrence_identity"]
        or coordinate["completeness_boundary_identity"]
        != positions[0]["completeness_boundary_identity"]
        for coordinate in positions[1:]
    ) or tuple(coordinate["position"] for coordinate in positions) != tuple(
        range(positions[0]["position"], positions[0]["position"] + 3)
    ):
        raise ValueError("source position Compare requires exact ordered positions")
    measurements = current_coordinates.get("measurement_occurrences")
    if (
        type(measurements) is not dict
        or measurements.get(event.identity) != _result_reference(event)
        or shared_position.get("result_position") != 0
    ):
        raise ValueError("current coordinates have no exact shared-position Measurement result")
    return {
        "event": event,
        "reference": _result_reference(event),
        "shared_position": shared_position,
        "shared_position_result_position_reference": {
            "recorded_occurrence_identity": event.identity,
            "result_position": 0,
        },
        "positions": tuple(deepcopy(position) for position in positions),
        "source_position_pair": source_position_pair,
        "first_source_position_index": first_source_position_index,
        "second_source_position_index": second_source_position_index,
        "first": deepcopy(positions[first_source_position_index]),
        "second": deepcopy(positions[second_source_position_index]),
        "source_occurrence_identity": positions[0][
            "source_material_result_occurrence_identity"
        ],
        "completeness_boundary_identity": positions[0][
            "completeness_boundary_identity"
        ],
        "locality_identity": event.locality_identity,
    }


def _mint_compare_identities(ledger: EventLedger) -> dict[str, str]:
    return {
        coordinate: ledger.mint_identity(
            "shared_position_source_position_material_" + coordinate
        )
        for coordinate in _COMPARE_IDENTITY_COORDINATES
    }


def _mint_applicability_identities(ledger: EventLedger) -> dict[str, str]:
    return {
        coordinate: ledger.mint_identity(
            "shared_position_source_position_material_" + coordinate
        )
        for coordinate in _APPLICABILITY_IDENTITY_COORDINATES
    }


def _binding_reference(event: Event) -> dict[str, Any]:
    return {
        "recorded_occurrence_identity": event.identity,
        "book_clause_identity": event.material["book_clause_identity"],
        "exact_act_identity": event.material["exact_act_identity"],
        "subject_reference": deepcopy(event.material["subject_reference"]),
    }


def _compare_binding_subject(material: dict[str, Any]) -> dict[str, Any]:
    subject = material.get("subject_reference")
    return subject if type(subject) is dict else {}


def _compare_binding_material(
    inputs: dict[str, Any], boundary: str, identities: dict[str, str]
) -> dict[str, Any]:
    return {
        "subject_reference": {
            "shared_position_result_position_reference": deepcopy(
                inputs["shared_position_result_position_reference"]
            ),
            "source_position_pair": list(inputs["source_position_pair"]),
            "first_source_position_coordinate": deepcopy(inputs["first"]),
            "second_source_position_coordinate": deepcopy(inputs["second"]),
        },
        "exact_act_identity": identities["exact_act_identity"],
        "compare_act_occurrence_identity": identities[
            "compare_act_occurrence_identity"
        ],
        "compare_result_identity": identities["compare_result_identity"],
        "book_clause_identity": BOOK_CLAUSE,
        "shared_position_measurement_result_reference": deepcopy(inputs["reference"]),
        "through_event_occurrence_identity": boundary,
        "exact_act": COMPARE_ACT,
    }


def _applicability_binding_material(
    *,
    compare_binding: Event,
    inputs: dict[str, Any],
    boundary: str,
    identities: dict[str, str],
) -> dict[str, Any]:
    compare_act_identity = compare_binding.material["exact_act_identity"]
    compare_act_occurrence_identity = compare_binding.material[
        "compare_act_occurrence_identity"
    ]
    compare_result_identity = compare_binding.material["compare_result_identity"]
    return {
        "subject_reference": {
            "first_input": {
                "subject": deepcopy(inputs["first"]),
                "addressed_act_identity": compare_act_identity,
            },
            "second_input": {
                "subject": deepcopy(inputs["second"]),
                "addressed_act_identity": compare_act_identity,
            },
        },
        "exact_act_identity": identities["exact_act_identity"],
        "applicability_act_occurrence_identity": identities[
            "applicability_act_occurrence_identity"
        ],
        "applicability_result_identity": identities[
            "applicability_result_identity"
        ],
        "addressed_act_identity": compare_act_identity,
        "addressed_act_occurrence_identity": compare_act_occurrence_identity,
        "compare_act_identity": compare_act_identity,
        "compare_act_occurrence_identity": compare_act_occurrence_identity,
        "compare_result_identity": compare_result_identity,
        "compare_subject_to_act_binding_reference": _binding_reference(
            compare_binding
        ),
        "book_clause_identity": "01.Current.E.1",
        "shared_position_measurement_result_reference": deepcopy(inputs["reference"]),
        "shared_position_result_position_reference": deepcopy(
            inputs["shared_position_result_position_reference"]
        ),
        "source_position_pair": list(inputs["source_position_pair"]),
        "first_source_position_coordinate": deepcopy(inputs["first"]),
        "second_source_position_coordinate": deepcopy(inputs["second"]),
        "through_event_occurrence_identity": boundary,
    }


def _applicability_act_material(binding: Event) -> dict[str, Any]:
    material = binding.material
    return {
        "act_identity": material["exact_act_identity"],
        "applicability_act_identity": material["exact_act_identity"],
        "applicability_act_occurrence_identity": material[
            "applicability_act_occurrence_identity"
        ],
        "applicability_result_identity": material["applicability_result_identity"],
        "compare_subject_to_act_binding_reference": deepcopy(
            material["compare_subject_to_act_binding_reference"]
        ),
        "applicability_subject_to_act_binding_reference": _binding_reference(
            binding
        ),
        "act": APPLICABILITY_ACT,
        "addressed_act_identity": material["addressed_act_identity"],
        "addressed_act_occurrence_identity": material[
            "addressed_act_occurrence_identity"
        ],
        "compare_act_identity": material["compare_act_identity"],
        "compare_act_occurrence_identity": material[
            "compare_act_occurrence_identity"
        ],
        "compare_result_identity": material["compare_result_identity"],
        "shared_position_measurement_result_reference": deepcopy(material["shared_position_measurement_result_reference"]),
        "shared_position_result_position_reference": deepcopy(
            material["shared_position_result_position_reference"]
        ),
        "source_position_pair": list(material["source_position_pair"]),
        "first_source_position_coordinate": deepcopy(
            material["first_source_position_coordinate"]
        ),
        "second_source_position_coordinate": deepcopy(
            material["second_source_position_coordinate"]
        ),
        "through_event_occurrence_identity": binding.identity,
    }


def _current_coordinates_through(
    ledger: EventLedger, *, locality_identity: str, boundary: Any
) -> dict[str, Any]:
    from seed_runtime.operator_current_coordinates import (
        read_operator_current_coordinates_through,
    )

    return read_operator_current_coordinates_through(
        ledger,
        locality_identity=locality_identity,
        through_event_occurrence_identity=boundary,
    )


def _read_compare_binding(
    ledger: EventLedger,
    event_identity: Any,
    *,
    current_coordinates: dict[str, Any] | None = None,
) -> tuple[Event, dict[str, Any]]:
    event = _event(
        ledger,
        event_identity,
        event_kind=COMPARE_SUBJECT_TO_ACT_BINDING_RECORDED_EVENT,
        message="source position Compare requires one exact subject-to-Act binding",
    )
    material = event.material
    identities = {
        name: material.get(name) for name in _COMPARE_IDENTITY_COORDINATES
    }
    if (
        any(type(value) is not str or not value for value in identities.values())
        or len(set(identities.values())) != len(identities)
    ):
        raise ValueError("source position Compare binding identities are not exact")
    boundary = material.get("through_event_occurrence_identity")
    if current_coordinates is None:
        current_coordinates = _current_coordinates_through(
            ledger,
            locality_identity=event.locality_identity,
            boundary=boundary,
        )
    shared_position_reference = material.get("shared_position_measurement_result_reference")
    subject = _compare_binding_subject(material)
    inputs = _shared_position_input(
        ledger,
        shared_position_reference.get("recorded_occurrence_identity")
        if type(shared_position_reference) is dict
        else None,
        source_position_pair=(
            tuple(subject.get("source_position_pair"))
            if type(subject.get("source_position_pair")) is list
            else ()
        ),
        current_coordinates=current_coordinates,
    )
    boundary_event = ledger.get(boundary) if type(boundary) is str else None
    if (
        boundary_event is None
        or boundary_event.locality_identity != event.locality_identity
        or event.locality_identity != inputs["locality_identity"]
        or material != _compare_binding_material(inputs, boundary, identities)
    ):
        raise ValueError("source position Compare binding is not exact")
    ledger.occurrences_in_append_order(
        (
            (inputs["event"].identity, boundary, event.identity)
            if inputs["event"].identity != boundary
            else (boundary, event.identity)
        ),
        locality_identity=event.locality_identity,
    )
    return event, inputs


def _read_applicability_binding(
    ledger: EventLedger,
    event_identity: Any,
    *,
    current_coordinates: dict[str, Any] | None = None,
) -> tuple[Event, Event, dict[str, Any]]:
    event = _event(
        ledger,
        event_identity,
        event_kind=APPLICABILITY_SUBJECT_TO_ACT_BINDING_RECORDED_EVENT,
        message=(
            "source position Compare requires one exact Applicability "
            "subject-to-Act binding"
        ),
    )
    material = event.material
    reference = material.get("compare_subject_to_act_binding_reference")
    compare_binding, inputs = _read_compare_binding(
        ledger,
        reference.get("recorded_occurrence_identity")
        if type(reference) is dict
        else None,
        current_coordinates=current_coordinates,
    )
    identities = {
        name: material.get(name) for name in _APPLICABILITY_IDENTITY_COORDINATES
    }
    if (
        any(type(value) is not str or not value for value in identities.values())
        or len(set(identities.values())) != len(identities)
        or material.get("through_event_occurrence_identity")
        != compare_binding.identity
        or material
        != _applicability_binding_material(
            compare_binding=compare_binding,
            inputs=inputs,
            boundary=compare_binding.identity,
            identities=identities,
        )
    ):
        raise ValueError("source position Compare Applicability binding is not exact")
    ledger.occurrences_in_append_order(
        (compare_binding.identity, event.identity),
        locality_identity=event.locality_identity,
    )
    return event, compare_binding, inputs


def _read_applicability_act(
    ledger: EventLedger,
    event_identity: Any,
    *,
    current_coordinates: dict[str, Any] | None = None,
) -> tuple[Event, Event, Event, dict[str, Any]]:
    event = _event(
        ledger,
        event_identity,
        event_kind=APPLICABILITY_ACT_KIND,
        message="source position Compare requires an exact Applicability Act",
    )
    material = event.material
    reference = material.get("applicability_subject_to_act_binding_reference")
    binding, compare_binding, inputs = _read_applicability_binding(
        ledger,
        reference.get("recorded_occurrence_identity")
        if type(reference) is dict
        else None,
        current_coordinates=current_coordinates,
    )
    if (
        event.locality_identity != binding.locality_identity
        or material != _applicability_act_material(binding)
    ):
        raise ValueError("source position Compare Applicability Act is not exact")
    ledger.occurrences_in_append_order(
        (binding.identity, event.identity),
        locality_identity=event.locality_identity,
    )
    return event, binding, compare_binding, inputs


def _applicability_result_material(act: Event) -> dict[str, Any]:
    material = act.material
    return {
        "result_identity": material["applicability_result_identity"],
        "dimensions": {
            "identity": material["applicability_result_identity"],
            "content": "shared-position Measurement source position material",
        },
        "act": APPLICABILITY_ACT,
        "addressed_act_identity": material["compare_act_identity"],
        "addressed_act_occurrence_identity": material[
            "compare_act_occurrence_identity"
        ],
        "applicability_act_identity": material[
            "applicability_act_identity"
        ],
        "applicability_act_occurrence_identity": material[
            "applicability_act_occurrence_identity"
        ],
        "compare_act_identity": material["compare_act_identity"],
        "compare_act_occurrence_identity": material[
            "compare_act_occurrence_identity"
        ],
        "compare_result_identity": material["compare_result_identity"],
        "first_source_position_coordinate": deepcopy(
            material["first_source_position_coordinate"]
        ),
        "second_source_position_coordinate": deepcopy(
            material["second_source_position_coordinate"]
        ),
        "act_occurrence_event_identity": act.identity,
        "applicability": "applicable",
        "shared_position_measurement_result_reference": deepcopy(material["shared_position_measurement_result_reference"]),
        "source_position_pair": list(material["source_position_pair"]),
        "through_event_occurrence_identity": material[
            "through_event_occurrence_identity"
        ],
    }


def _recorded_applicability_result_material(
    material: dict[str, Any],
) -> dict[str, Any]:
    return {
        "result_identity": material["result_identity"],
        "dimensions": deepcopy(material["dimensions"]),
        "act": material["act"],
        "addressed_act_identity": material["addressed_act_identity"],
        "addressed_act_occurrence_identity": material[
            "addressed_act_occurrence_identity"
        ],
        "applicability_act_identity": material["applicability_act_identity"],
        "applicability_act_occurrence_identity": material[
            "applicability_act_occurrence_identity"
        ],
        "compare_act_identity": material["compare_act_identity"],
        "compare_act_occurrence_identity": material[
            "compare_act_occurrence_identity"
        ],
        "compare_result_identity": material["compare_result_identity"],
        "first_source_position_coordinate": deepcopy(
            material["first_source_position_coordinate"]
        ),
        "second_source_position_coordinate": deepcopy(
            material["second_source_position_coordinate"]
        ),
        "act_occurrence_event_identity": material[
            "act_occurrence_event_identity"
        ],
        "applicability": material["applicability"],
        "shared_position_measurement_result_reference": deepcopy(material["shared_position_measurement_result_reference"]),
        "source_position_pair": list(material["source_position_pair"]),
        "through_event_occurrence_identity": material[
            "through_event_occurrence_identity"
        ],
    }


def _recorded_compare_result_material(
    material: dict[str, Any]
) -> dict[str, Any]:
    recorded = {
        "result_identity": material["result_identity"],
        "compare_act_identity": material["compare_act_identity"],
        "act_occurrence_identity": material["act_occurrence_identity"],
        "act": material["act"],
        "finding": deepcopy(material["finding"]),
        "shared_position_measurement_result_reference": deepcopy(material["shared_position_measurement_result_reference"]),
        "source_position_pair": list(material["source_position_pair"]),
        "act_occurrence_event_identity": material[
            "act_occurrence_event_identity"
        ],
    }
    if "subject_to_act_binding_reference" in material:
        recorded["subject_to_act_binding_reference"] = deepcopy(
            material["subject_to_act_binding_reference"]
        )
    else:
        recorded["subject_reference"] = deepcopy(material["subject_reference"])
    if "applicability_result_event_identity" in material:
        recorded["applicability_result_event_identity"] = material[
            "applicability_result_event_identity"
        ]
    return recorded


def _read_exact_result(
    ledger: EventLedger,
    event_identity: Any,
    *,
    event_kind: str,
    act: Event,
    expected: dict[str, Any],
) -> Event:
    event = _event(
        ledger, event_identity, event_kind=event_kind, message="result is not exact"
    )
    results = tuple(
        result
        for result in ledger.iter_locality_kind(act.locality_identity, event_kind)
        if result.material.get("act_occurrence_event_identity") == act.identity
    )
    try:
        ordered = ledger.occurrences_in_append_order(
            (act.identity, event.identity),
            locality_identity=act.locality_identity,
        )
    except (TypeError, ValueError) as error:
        raise ValueError("Applicability result does not follow its Act") from error
    if (
        event.locality_identity != act.locality_identity
        or event.material != expected
        or tuple(item.identity for item in ordered) != (act.identity, event.identity)
        or len(results) != 1
        or results[0].identity != event.identity
    ):
        raise ValueError("Applicability result is not exact")
    return event


def _read_applicability_result(
    ledger: EventLedger,
    event_identity: Any,
    *,
    act_reading: tuple[Event, Event, Event, dict[str, Any]] | None = None,
    current_coordinates: dict[str, Any] | None = None,
) -> tuple[Event, Event, Event, Event, dict[str, Any]]:
    candidate = ledger.get(event_identity) if type(event_identity) is str else None
    if act_reading is None:
        act_reading = _read_applicability_act(
            ledger,
            candidate.material.get("act_occurrence_event_identity")
            if candidate is not None
            else None,
            current_coordinates=current_coordinates,
        )
    act, binding, compare_binding, inputs = act_reading
    event = _read_exact_result(
        ledger,
        event_identity,
        event_kind=APPLICABILITY_RESULT_KIND,
        act=act,
        expected=_applicability_result_material(act),
    )
    return event, act, binding, compare_binding, inputs


def _compare_act_material(
    compare_binding: Event, applicability: Event
) -> dict[str, Any]:
    material = compare_binding.material
    subject = _compare_binding_subject(material)
    return {
        "act_identity": material["exact_act_identity"],
        "act_occurrence_identity": material["compare_act_occurrence_identity"],
        "compare_result_identity": material["compare_result_identity"],
        "act": COMPARE_ACT,
        "subject_to_act_binding_reference": _binding_reference(compare_binding),
        "applicability_result_event_identity": applicability.identity,
        "shared_position_measurement_result_reference": deepcopy(material["shared_position_measurement_result_reference"]),
        "source_position_pair": list(subject["source_position_pair"]),
        "through_event_occurrence_identity": applicability.identity,
    }


def _compare_act_material_without_applicability(
    compare_binding: Event,
) -> dict[str, Any]:
    material = compare_binding.material
    subject = _compare_binding_subject(material)
    return {
        "act_identity": material["exact_act_identity"],
        "act_occurrence_identity": material["compare_act_occurrence_identity"],
        "compare_result_identity": material["compare_result_identity"],
        "act": COMPARE_ACT,
        "subject_to_act_binding_reference": _binding_reference(compare_binding),
        "shared_position_measurement_result_reference": deepcopy(
            material["shared_position_measurement_result_reference"]
        ),
        "source_position_pair": list(subject["source_position_pair"]),
        "through_event_occurrence_identity": compare_binding.identity,
    }


def _compare_act_material_from_inputs(
    inputs: dict[str, Any], boundary: str, identities: dict[str, str]
) -> dict[str, Any]:
    return {
        "act_identity": identities["exact_act_identity"],
        "act_occurrence_identity": identities["compare_act_occurrence_identity"],
        "compare_result_identity": identities["compare_result_identity"],
        "act": COMPARE_ACT,
        "subject_reference": {
            "shared_position_result_position_reference": deepcopy(
                inputs["shared_position_result_position_reference"]
            ),
            "source_position_pair": list(inputs["source_position_pair"]),
            "first_source_position_coordinate": deepcopy(inputs["first"]),
            "second_source_position_coordinate": deepcopy(inputs["second"]),
        },
        "book_clause_identity": BOOK_CLAUSE,
        "shared_position_measurement_result_reference": deepcopy(
            inputs["reference"]
        ),
        "source_position_pair": list(inputs["source_position_pair"]),
        "through_event_occurrence_identity": boundary,
    }


def _read_compare_act(
    ledger: EventLedger,
    event_identity: Any,
    *,
    current_coordinates: dict[str, Any] | None = None,
) -> tuple[Event, Event | None, Event | None, dict[str, Any]]:
    event = _event(
        ledger,
        event_identity,
        event_kind=COMPARE_ACT_KIND,
        message="source position Compare requires an exact Compare Act",
    )
    reference = event.material.get("subject_to_act_binding_reference")
    if reference is None:
        shared_position_reference = event.material.get(
            "shared_position_measurement_result_reference"
        )
        subject = event.material.get("subject_reference")
        source_position_pair = (
            tuple(subject.get("source_position_pair"))
            if type(subject) is dict
            and type(subject.get("source_position_pair")) is list
            else ()
        )
        boundary = event.material.get("through_event_occurrence_identity")
        if current_coordinates is None:
            current_coordinates = _current_coordinates_through(
                ledger,
                locality_identity=event.locality_identity,
                boundary=boundary,
            )
        inputs = _shared_position_input(
            ledger,
            shared_position_reference.get("recorded_occurrence_identity")
            if type(shared_position_reference) is dict
            else None,
            source_position_pair=source_position_pair,
            current_coordinates=current_coordinates,
        )
        identities = {
            "exact_act_identity": event.material.get("act_identity"),
            "compare_act_occurrence_identity": event.material.get(
                "act_occurrence_identity"
            ),
            "compare_result_identity": event.material.get(
                "compare_result_identity"
            ),
        }
        if (
            any(type(value) is not str or not value for value in identities.values())
            or len(set(identities.values())) != len(identities)
            or event.locality_identity != inputs["locality_identity"]
            or event.material
            != _compare_act_material_from_inputs(inputs, boundary, identities)
        ):
            raise ValueError("source position Compare Act is not exact")
        ledger.occurrences_in_append_order(
            tuple(
                dict.fromkeys(
                    (inputs["event"].identity, boundary, event.identity)
                )
            ),
            locality_identity=event.locality_identity,
        )
        return event, None, None, inputs
    compare_binding, inputs = _read_compare_binding(
        ledger,
        reference.get("recorded_occurrence_identity")
        if type(reference) is dict
        else None,
        current_coordinates=current_coordinates,
    )
    if "applicability_result_event_identity" not in event.material:
        if (
            event.locality_identity != compare_binding.locality_identity
            or event.material
            != _compare_act_material_without_applicability(compare_binding)
        ):
            raise ValueError("source position Compare Act is not exact")
        return event, compare_binding, None, inputs
    (
        applicability,
        _applicability_act,
        _applicability_binding,
        applicability_compare_binding,
        applicability_inputs,
    ) = _read_applicability_result(
        ledger,
        event.material.get("applicability_result_event_identity"),
        current_coordinates=current_coordinates,
    )
    if (
        applicability_compare_binding.identity != compare_binding.identity
        or applicability_inputs != inputs
        or event.locality_identity != applicability.locality_identity
        or event.material != _compare_act_material(compare_binding, applicability)
    ):
        raise ValueError("source position Compare Act is not exact")
    return event, compare_binding, applicability, inputs


def _finding(inputs: dict[str, Any]) -> dict[str, Any]:
    first = inputs["first"]
    second = inputs["second"]
    result = (
        "same-content"
        if first["exact_material"] == second["exact_material"]
        else "difference"
    )
    subject = {
        "shared_position_result_position_reference": deepcopy(
            inputs["shared_position_result_position_reference"]
        ),
        "source_position_pair": list(inputs["source_position_pair"]),
        "first_source_position_coordinate": deepcopy(first),
        "second_source_position_coordinate": deepcopy(second),
    }
    return {
        "subject": subject,
        "result": result,
    }


def _compare_result_material(
    act: Event,
    applicability: Event | None,
    inputs: dict[str, Any],
) -> dict[str, Any]:
    material = act.material
    result = {
        "result_identity": material["compare_result_identity"],
        "compare_act_identity": material["act_identity"],
        "act_occurrence_identity": material["act_occurrence_identity"],
        "act": COMPARE_ACT,
        "finding": _finding(inputs),
        "shared_position_measurement_result_reference": deepcopy(inputs["reference"]),
        "source_position_pair": list(inputs["source_position_pair"]),
        "act_occurrence_event_identity": act.identity,
    }
    if "subject_to_act_binding_reference" in material:
        result["subject_to_act_binding_reference"] = deepcopy(
            material["subject_to_act_binding_reference"]
        )
    else:
        result["subject_reference"] = deepcopy(material["subject_reference"])
    if applicability is not None:
        result["applicability_result_event_identity"] = applicability.identity
    return result


def _read_compare_result(
    ledger: EventLedger,
    event_identity: Any,
    *,
    current_coordinates: dict[str, Any] | None = None,
) -> tuple[Event, Event, Event | None, Event | None, dict[str, Any]]:
    candidate = ledger.get(event_identity) if type(event_identity) is str else None
    act, compare_binding, applicability, inputs = _read_compare_act(
        ledger,
        candidate.material.get("act_occurrence_event_identity")
        if candidate is not None
        else None,
        current_coordinates=current_coordinates,
    )
    event = _event(
        ledger,
        event_identity,
        event_kind=COMPARE_RESULT_KIND,
        message="source position Compare result is not exact",
    )
    if (
        event.locality_identity != act.locality_identity
        or event.material
        != _recorded_compare_result_material(
            _compare_result_material(act, applicability, inputs)
        )
    ):
        raise ValueError("source position Compare result is not exact")
    ordered = ledger.occurrences_in_append_order(
        (act.identity, event.identity),
        locality_identity=event.locality_identity,
    )
    if [occurrence.identity for occurrence in ordered] != [
        act.identity,
        event.identity,
    ]:
        raise ValueError("source position Compare result does not follow its Act")
    results = tuple(
        candidate
        for candidate in ledger.iter_locality_kind(
            event.locality_identity, COMPARE_RESULT_KIND
        )
        if candidate.material.get("act_occurrence_event_identity")
        == act.identity
    )
    if len(results) != 1 or results[0].identity != event.identity:
        raise ValueError("source position Compare Act has no single exact result")
    return event, act, compare_binding, applicability, inputs


def get_recorded_shared_position_source_position_material_comparison(
    ledger: EventLedger, event_identity: str
) -> dict[str, Any]:
    return deepcopy(_read_compare_result(ledger, event_identity)[0].material)


def validate_shared_position_source_position_material_comparison_event(
    ledger: EventLedger,
    event_identity: str,
    *,
    current_coordinates: dict[str, Any] | None = None,
) -> Event:
    event = ledger.get(event_identity)
    if event is None:
        raise ValueError("source position Compare occurrence is not exact")
    if event.kind == COMPARE_SUBJECT_TO_ACT_BINDING_RECORDED_EVENT:
        return _read_compare_binding(
            ledger, event.identity, current_coordinates=current_coordinates
        )[0]
    if event.kind == APPLICABILITY_SUBJECT_TO_ACT_BINDING_RECORDED_EVENT:
        return _read_applicability_binding(
            ledger, event.identity, current_coordinates=current_coordinates
        )[0]
    if event.kind == APPLICABILITY_ACT_KIND:
        return _read_applicability_act(
            ledger, event.identity, current_coordinates=current_coordinates
        )[0]
    if event.kind == APPLICABILITY_RESULT_KIND:
        return _read_applicability_result(
            ledger, event.identity, current_coordinates=current_coordinates
        )[0]
    if event.kind == COMPARE_ACT_KIND:
        return _read_compare_act(
            ledger, event.identity, current_coordinates=current_coordinates
        )[0]
    if event.kind == COMPARE_RESULT_KIND:
        return _read_compare_result(
            ledger, event.identity, current_coordinates=current_coordinates
        )[0]
    raise ValueError("source position Compare occurrence is not exact")


def _require_tip(ledger: EventLedger, event: Event) -> None:
    if ledger.append_boundary_through_occurrence(event.identity) != ledger.append_boundary():
        raise ValueError("source position Compare stage left its exact boundary")


def _record_shared_position_source_position_material_comparison(
    ledger: EventLedger,
    *,
    shared_position_measurement_result_event_identity: str,
    source_position_pair: tuple[int, int],
    current_coordinates: dict[str, Any],
) -> SharedPositionSourcePositionMaterialComparison:
    """Record one exact shared-position pair Compare."""

    if not isinstance(ledger, EventLedger):
        raise TypeError("source position Compare requires an EventLedger")
    locality_identity = current_coordinates.get("locality_identity")
    boundary = current_coordinates.get("through_event_occurrence_identity")
    if (
        type(locality_identity) is not str
        or not locality_identity
        or type(boundary) is not str
        or not boundary
        or ledger.append_boundary().identity != ledger.append_boundary_through_occurrence(
            boundary
        ).identity
    ):
        raise ValueError("source position Compare requires exact current coordinates")
    inputs = _shared_position_input(
        ledger,
        shared_position_measurement_result_event_identity,
        source_position_pair=source_position_pair,
        current_coordinates=current_coordinates,
    )
    compare_identities = _mint_compare_identities(ledger)
    def establish_current(*events: Event) -> None:
        prior = current_coordinates["through_event_occurrence_identity"]
        ordered = ledger.occurrences_in_append_order(
            (prior, *(event.identity for event in events)),
            locality_identity=locality_identity,
        )
        if (
            tuple(event.identity for event in ordered)
            != (prior, *(event.identity for event in events))
            or ledger.append_boundary_through_occurrence(events[-1].identity)
            != ledger.append_boundary()
        ):
            raise ValueError("source position Compare left its exact boundary")
        for established in events:
            if established.kind in {
                COMPARE_SUBJECT_TO_ACT_BINDING_RECORDED_EVENT,
                APPLICABILITY_SUBJECT_TO_ACT_BINDING_RECORDED_EVENT,
            }:
                current_coordinates["subject_to_act_binding_occurrences"][
                    established.identity
                ] = None
            elif established.kind == APPLICABILITY_RESULT_KIND:
                current_coordinates["applicability_result_occurrences"][
                    established.identity
                ] = None
            elif established.kind == COMPARE_RESULT_KIND:
                current_coordinates["comparison_result_occurrences"][
                    established.identity
                ] = None
            current_coordinates["through_event_occurrence_identity"] = (
                established.identity
            )
            current_coordinates["event_count"] += 1

    compare_act = ledger.append(
        COMPARE_ACT_KIND,
        _compare_act_material_from_inputs(inputs, boundary, compare_identities),
        locality_identity=locality_identity,
    )
    establish_current(compare_act)
    result_material = _compare_result_material(compare_act, None, inputs)
    _require_tip(ledger, compare_act)
    result = ledger.append(
        COMPARE_RESULT_KIND,
        _recorded_compare_result_material(result_material),
        locality_identity=locality_identity,
    )
    establish_current(result)
    return SharedPositionSourcePositionMaterialComparison(current_coordinates, result)


def yield_shared_position_source_position_material_comparisons(
    ledger: EventLedger,
    *,
    shared_position_measurement_result_event_identity: str,
    current_coordinates: dict[str, Any],
) -> Iterator[SharedPositionSourcePositionMaterialComparison]:
    """Yield every distinct shared-position coordinate pair before returning."""

    for source_position_pair in _SOURCE_POSITION_PAIRS:
        comparison = _record_shared_position_source_position_material_comparison(
            ledger,
            shared_position_measurement_result_event_identity=shared_position_measurement_result_event_identity,
            source_position_pair=source_position_pair,
            current_coordinates=current_coordinates,
        )
        current_coordinates = comparison.current_coordinates
        yield comparison
