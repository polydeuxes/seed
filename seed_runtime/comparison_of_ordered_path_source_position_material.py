"""Compare each exact path-ordered pair of source-position material."""

from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from typing import Any, Iterator, NamedTuple

from seed_runtime.event import Event
from seed_runtime.events import CORRUPTED, EventLedger
from seed_runtime.yield_relation import (
    RECORDED_YIELD_RELATION_EVENT,
    _record_yield_relation,
    read_requirements_of_yield_relation,
)
from seed_runtime.identities import new_identity
from seed_runtime.measurement_of_shared_position_of_byte_pair_occurrences import (
    SHARED_POSITION_MEASUREMENT_RESULT_KIND,
    ordered_source_position_coordinates_beside_ordered_relation_path_assertion,
)


APPLICABILITY_ACT_KIND = (
    "operator.comparison_of_ordered_path_source_position_material."
    "applicability_act_recorded"
)
APPLICABILITY_RESULT_KIND = (
    "operator.comparison_of_ordered_path_source_position_material."
    "applicability_result_recorded"
)
COMPARE_ACT_KIND = (
    "operator.comparison_of_ordered_path_source_position_material."
    "compare_act_recorded"
)
COMPARE_RESULT_KIND = (
    "operator.comparison_of_ordered_path_source_position_material."
    "compare_result_recorded"
)

BOOK_CLAUSE = "04.Compare"
RESPONSIBILITY = "compare ordered path source position material"
APPLICABILITY_ACT = (
    "Applicability of ordered path source position material to Compare"
)
COMPARE_ACT = "Compare ordered path source position material"
RULE = "compare exact material of ordered path source position coordinates"
APPLICABILITY_BOUNDARY = (
    "comparison_of_ordered_path_source_position_material_applicability"
)
COMPARE_BOUNDARY = "comparison_of_ordered_path_source_position_material_compare"

EVENT_KIND_RESPONSIBILITIES = {
    APPLICABILITY_ACT_KIND: "02.Acts.A",
    APPLICABILITY_RESULT_KIND: "01.Current.E.1",
    COMPARE_ACT_KIND: "02.Acts.A",
    COMPARE_RESULT_KIND: "04.Compare",
}


class OrderedPathSourcePositionMaterialComparison(NamedTuple):
    locality_standing: dict[str, Any]
    result_occurrence: Event


_IDENTITY_COORDINATES = (
    "applicability_act_identity",
    "applicability_act_occurrence_identity",
    "applicability_result_identity",
    "compare_act_identity",
    "compare_act_occurrence_identity",
    "compare_result_identity",
    "first_input_relation_identity",
    "second_input_relation_identity",
    "first_participation_relation_identity",
    "second_participation_relation_identity",
)

_PATH_POSITION_PAIRS = ((0, 1), (0, 2), (1, 2))


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
        "yield_relation_identity": event.material[
            "yield_relation_identity"
        ],
    }


def _path_input(
    ledger: EventLedger,
    path_result_event_identity: Any,
    *,
    path_position_pair: tuple[int, int],
    prior_standing: dict[str, Any],
) -> dict[str, Any]:
    event = _event(
        ledger,
        path_result_event_identity,
        event_kind=SHARED_POSITION_MEASUREMENT_RESULT_KIND,
        message="source position Compare requires an exact ordered path result",
    )
    path, positions = (
        ordered_source_position_coordinates_beside_ordered_relation_path_assertion(
            ledger, event.identity, prior_standing=prior_standing
        )
    )
    if len(positions) != 3:
        raise ValueError("source position Compare requires exact ordered positions")
    if path_position_pair not in _PATH_POSITION_PAIRS:
        raise ValueError("source position Compare requires a path-ordered pair")
    first_path_position, second_path_position = path_position_pair
    first, middle, final = positions
    for coordinate in positions:
        material = coordinate.get("exact_material")
        if (
            type(coordinate.get("identity")) is not str
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
    if (
        first["source_material_result_occurrence_identity"]
        != middle["source_material_result_occurrence_identity"]
        or middle["source_material_result_occurrence_identity"]
        != final["source_material_result_occurrence_identity"]
        or first["completeness_boundary_identity"]
        != middle["completeness_boundary_identity"]
        or middle["completeness_boundary_identity"]
        != final["completeness_boundary_identity"]
        or (first["position"], middle["position"], final["position"])
        != (first["position"], first["position"] + 1, first["position"] + 2)
    ):
        raise ValueError("source position Compare requires exact ordered positions")
    assertions = prior_standing.get("measurement_occurrences")
    if (
        type(assertions) is not dict
        or assertions.get(event.identity) != _result_reference(event)
    ):
        raise ValueError("current Standing carries no exact ordered path result")
    return {
        "event": event,
        "reference": _result_reference(event),
        "path": path,
        "path_assertion_reference": {
            "recorded_occurrence_identity": event.identity,
            "assertion_identity": path["dimensions"]["identity"],
        },
        "positions": tuple(deepcopy(position) for position in positions),
        "path_position_pair": path_position_pair,
        "first_path_position": first_path_position,
        "second_path_position": second_path_position,
        "first": deepcopy(positions[first_path_position]),
        "second": deepcopy(positions[second_path_position]),
        "source_occurrence_identity": first[
            "source_material_result_occurrence_identity"
        ],
        "completeness_boundary_identity": first[
            "completeness_boundary_identity"
        ],
        "locality_identity": event.locality_identity,
    }


def _new_identities() -> dict[str, str]:
    return {
        coordinate: new_identity(
            "ordered_path_source_position_material_" + coordinate
        )
        for coordinate in _IDENTITY_COORDINATES
    }


def _applicability_act_material(
    inputs: dict[str, Any], boundary: str, identities: dict[str, str]
) -> dict[str, Any]:
    return {
        "applicability_act_identity": identities["applicability_act_identity"],
        "applicability_act_occurrence_identity": identities[
            "applicability_act_occurrence_identity"
        ],
        "applicability_result_identity": identities[
            "applicability_result_identity"
        ],
        "compare_act_identity": identities["compare_act_identity"],
        "compare_act_occurrence_identity": identities[
            "compare_act_occurrence_identity"
        ],
        "compare_result_identity": identities["compare_result_identity"],
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
        "comparison_rule": RULE,
        "path_result_reference": deepcopy(inputs["reference"]),
        "path_assertion_reference": deepcopy(inputs["path_assertion_reference"]),
        "path_position_pair": list(inputs["path_position_pair"]),
        "first_source_position_coordinate": deepcopy(inputs["first"]),
        "second_source_position_coordinate": deepcopy(inputs["second"]),
        "standing_boundary_identity": boundary,
        "act_identity": identities["applicability_act_identity"],
        "act": APPLICABILITY_ACT,
        "addressed_act_identity": identities["compare_act_identity"],
        "addressed_act_occurrence_identity": identities[
            "compare_act_occurrence_identity"
        ],
        "applicability_of_input_to_compare": [
            {
                "first_subject": deepcopy(inputs["first"]),
                "relation": "applicability",
                "second_subject": {
                    "act_identity": identities["compare_act_identity"],
                    "act_occurrence_identity": identities[
                        "compare_act_occurrence_identity"
                    ],
                    "role": f"path position {inputs['first_path_position']}",
                },
                "relation_occurrence_identity": identities[
                    "first_input_relation_identity"
                ],
            },
            {
                "first_subject": deepcopy(inputs["second"]),
                "relation": "applicability",
                "second_subject": {
                    "act_identity": identities["compare_act_identity"],
                    "act_occurrence_identity": identities[
                        "compare_act_occurrence_identity"
                    ],
                    "role": f"path position {inputs['second_path_position']}",
                },
                "relation_occurrence_identity": identities[
                    "second_input_relation_identity"
                ],
            },
        ],
        "scope": {
            "locality_identity": inputs["locality_identity"],
            "source_material_result_occurrence_identity": inputs[
                "source_occurrence_identity"
            ],
            "completeness_boundary_identity": inputs[
                "completeness_boundary_identity"
            ],
            "standing_boundary_identity": boundary,
        },
        "unknown": [],
        "conflicts": [],
    }


def _read_applicability_act(
    ledger: EventLedger,
    event_identity: Any,
    *,
    prior_standing: dict[str, Any] | None = None,
) -> tuple[Event, dict[str, Any]]:
    event = _event(
        ledger,
        event_identity,
        event_kind=APPLICABILITY_ACT_KIND,
        message="source position Compare requires an exact Applicability Act",
    )
    material = event.material
    identities = {name: material.get(name) for name in _IDENTITY_COORDINATES}
    if (
        any(type(value) is not str or not value for value in identities.values())
        or len(set(identities.values())) != len(identities)
    ):
        raise ValueError("source position Compare identities are not exact")
    boundary = material.get("standing_boundary_identity")
    if prior_standing is None:
        from seed_runtime.operator_locality_standing import (
            _operator_standing_validation_context,
            read_operator_locality_standing_through,
        )

        prior_standing = _operator_standing_validation_context(
            ledger, locality_identity=event.locality_identity
        )
        if prior_standing is None:
            prior_standing = read_operator_locality_standing_through(
                ledger,
                locality_identity=event.locality_identity,
                through_event_occurrence_identity=boundary,
            )
    path_reference = material.get("path_result_reference")
    inputs = _path_input(
        ledger,
        path_reference.get("recorded_occurrence_identity")
        if type(path_reference) is dict
        else None,
        path_position_pair=(
            tuple(material.get("path_position_pair"))
            if type(material.get("path_position_pair")) is list
            else ()
        ),
        prior_standing=prior_standing,
    )
    boundary_event = ledger.get(boundary) if type(boundary) is str else None
    if (
        boundary_event is None
        or boundary_event.locality_identity != event.locality_identity
        or event.locality_identity != inputs["locality_identity"]
        or material != _applicability_act_material(inputs, boundary, identities)
    ):
        raise ValueError("source position Compare Applicability Act is not exact")
    ledger.occurrences_in_append_order(
        (inputs["event"].identity, boundary, event.identity)
        if inputs["event"].identity != boundary
        else (boundary, event.identity),
        locality_identity=event.locality_identity,
    )
    return event, inputs


def _applicability_result_material(act: Event) -> dict[str, Any]:
    material = act.material
    return {
        "result_identity": material["applicability_result_identity"],
        "dimensions": {
            "identity": material["applicability_result_identity"],
            "content": "ordered path source position material",
            "standing": "applicable",
            "source_provenance": "exact ordered relation path source coordinates",
            "responsibility": RESPONSIBILITY,
            "responsible_boundary": "this Seed",
            "scope": deepcopy(material["scope"]),
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
        "first_participation_relation_identity": material[
            "first_participation_relation_identity"
        ],
        "second_participation_relation_identity": material[
            "second_participation_relation_identity"
        ],
        "first_source_position_coordinate": deepcopy(
            material["first_source_position_coordinate"]
        ),
        "second_source_position_coordinate": deepcopy(
            material["second_source_position_coordinate"]
        ),
        "responsibility": RESPONSIBILITY,
        "responsible_boundary": "this Seed",
        "act_occurrence_event_identity": act.identity,
        "applicability_of_input_to_compare": deepcopy(
            act.material["applicability_of_input_to_compare"]
        ),
        "comparison_rule": RULE,
        "applicability": "applicable",
        "path_result_reference": deepcopy(material["path_result_reference"]),
        "path_position_pair": list(material["path_position_pair"]),
        "standing_boundary_identity": material["standing_boundary_identity"],
        "scope": deepcopy(material["scope"]),
        "unknown": [],
        "conflicts": [],
    }


def _recorded_result_material(
    material: dict[str, Any], yield_relation_identity: str
) -> dict[str, Any]:
    return {**deepcopy(material), "yield_relation_identity": yield_relation_identity}


def _recorded_applicability_result_material(
    material: dict[str, Any], yield_relation_identity: str
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
        "first_participation_relation_identity": material[
            "first_participation_relation_identity"
        ],
        "second_participation_relation_identity": material[
            "second_participation_relation_identity"
        ],
        "first_source_position_coordinate": deepcopy(
            material["first_source_position_coordinate"]
        ),
        "second_source_position_coordinate": deepcopy(
            material["second_source_position_coordinate"]
        ),
        "responsibility": material["responsibility"],
        "responsible_boundary": material["responsible_boundary"],
        "act_occurrence_event_identity": material[
            "act_occurrence_event_identity"
        ],
        "applicability_of_input_to_compare": deepcopy(
            material["applicability_of_input_to_compare"]
        ),
        "comparison_rule": material["comparison_rule"],
        "applicability": material["applicability"],
        "path_result_reference": deepcopy(material["path_result_reference"]),
        "path_position_pair": list(material["path_position_pair"]),
        "standing_boundary_identity": material["standing_boundary_identity"],
        "scope": deepcopy(material["scope"]),
        "unknown": list(material["unknown"]),
        "conflicts": list(material["conflicts"]),
        "yield_relation_identity": yield_relation_identity,
    }


def _recorded_compare_result_material(
    material: dict[str, Any], yield_relation_identity: str
) -> dict[str, Any]:
    return {
        "result_identity": material["result_identity"],
        "compare_act_identity": material["compare_act_identity"],
        "act_occurrence_identity": material["act_occurrence_identity"],
        "act": material["act"],
        "responsibility": material["responsibility"],
        "responsible_boundary": material["responsible_boundary"],
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
        "finding": deepcopy(material["finding"]),
        "path_result_reference": deepcopy(material["path_result_reference"]),
        "path_position_pair": list(material["path_position_pair"]),
        "scope": deepcopy(material["scope"]),
        "unknown": list(material["unknown"]),
        "conflicts": list(material["conflicts"]),
        "act_occurrence_event_identity": material[
            "act_occurrence_event_identity"
        ],
        "yield_relation_identity": yield_relation_identity,
    }


def _read_yielded(
    ledger: EventLedger,
    event_identity: Any,
    *,
    event_kind: str,
    act: Event,
    expected: dict[str, Any],
    occurrence_boundary: str,
    result_kind: str,
    occurrence_coordinate: str,
) -> Event:
    event = _event(
        ledger, event_identity, event_kind=event_kind, message="result is not exact"
    )
    yield_relation_identity = event.material.get("yield_relation_identity")
    yield_relation = ledger.get(yield_relation_identity) if type(yield_relation_identity) is str else None
    requirements = read_requirements_of_yield_relation(
        ledger,
        recorded_result_event_identity=event.identity,
        yield_relation_event_identity=yield_relation_identity,
        act_occurrence_event_identity=act.identity,
        recorded_result_occurrence_coordinate=occurrence_coordinate,
        responsible_act_occurrence_coordinate=occurrence_coordinate,
    )
    if (
        event.locality_identity != act.locality_identity
        or event.material != _recorded_result_material(expected, yield_relation_identity)
        or yield_relation is None
        or yield_relation.material.get("occurrence_boundary") != occurrence_boundary
        or yield_relation.material.get("result_kind") != result_kind
        or not all(requirements.values())
    ):
        raise ValueError("result carries no exact Yield relation")
    return event


def _read_applicability_result(
    ledger: EventLedger,
    event_identity: Any,
    *,
    act_reading: tuple[Event, dict[str, Any]] | None = None,
) -> tuple[Event, Event, dict[str, Any]]:
    candidate = ledger.get(event_identity) if type(event_identity) is str else None
    if act_reading is None:
        act_reading = _read_applicability_act(
            ledger,
            candidate.material.get("act_occurrence_event_identity")
            if candidate is not None
            else None,
        )
    act, inputs = act_reading
    event = _read_yielded(
        ledger,
        event_identity,
        event_kind=APPLICABILITY_RESULT_KIND,
        act=act,
        expected=_applicability_result_material(act),
        occurrence_boundary=APPLICABILITY_BOUNDARY,
        result_kind="Applicability result of ordered path source position material",
        occurrence_coordinate="applicability_act_occurrence_identity",
    )
    return event, act, inputs


def _compare_act_material(applicability: Event) -> dict[str, Any]:
    material = applicability.material
    return {
        "act_identity": material["compare_act_identity"],
        "act_occurrence_identity": material["compare_act_occurrence_identity"],
        "compare_result_identity": material["compare_result_identity"],
        "act": COMPARE_ACT,
        "responsibility": RESPONSIBILITY,
        "responsible_boundary": "this Seed",
        "applicability_result_event_identity": applicability.identity,
        "path_result_reference": deepcopy(material["path_result_reference"]),
        "path_position_pair": list(material["path_position_pair"]),
        "standing_boundary_identity": applicability.identity,
        "applicability_of_input_to_compare": deepcopy(
            applicability.material["applicability_of_input_to_compare"]
        ),
        "participation_of_input_in_compare": [
            {
                "first_subject": deepcopy(
                    material["first_source_position_coordinate"]
                ),
                "relation": "participation",
                "second_subject": {
                    "act_identity": material["compare_act_identity"],
                    "act_occurrence_identity": material[
                        "compare_act_occurrence_identity"
                    ],
                    "role": f"path position {material['path_position_pair'][0]}",
                },
                "relation_occurrence_identity": material[
                    "first_participation_relation_identity"
                ],
            },
            {
                "first_subject": deepcopy(
                    material["second_source_position_coordinate"]
                ),
                "relation": "participation",
                "second_subject": {
                    "act_identity": material["compare_act_identity"],
                    "act_occurrence_identity": material[
                        "compare_act_occurrence_identity"
                    ],
                    "role": f"path position {material['path_position_pair'][1]}",
                },
                "relation_occurrence_identity": material[
                    "second_participation_relation_identity"
                ],
            },
        ],
        "comparison_rule": RULE,
        "scope": deepcopy(material["scope"]),
        "unknown": [],
        "conflicts": [],
    }


def _read_compare_act(
    ledger: EventLedger, event_identity: Any
) -> tuple[Event, Event, dict[str, Any]]:
    event = _event(
        ledger,
        event_identity,
        event_kind=COMPARE_ACT_KIND,
        message="source position Compare requires an exact Compare Act",
    )
    applicability, _applicability_act, inputs = _read_applicability_result(
        ledger,
        event.material.get("applicability_result_event_identity"),
    )
    if (
        event.locality_identity != applicability.locality_identity
        or event.material != _compare_act_material(applicability)
    ):
        raise ValueError("source position Compare Act is not exact")
    return event, applicability, inputs


def _finding(inputs: dict[str, Any]) -> dict[str, Any]:
    first = inputs["first"]
    second = inputs["second"]
    result = (
        "same-content"
        if first["exact_material"] == second["exact_material"]
        else "difference"
    )
    subject = {
        "ordered_relation_path_assertion_reference": deepcopy(
            inputs["path_assertion_reference"]
        ),
        "path_position_pair": list(inputs["path_position_pair"]),
        "first_source_position_coordinate": deepcopy(first),
        "second_source_position_coordinate": deepcopy(second),
    }
    exact = json.dumps(
        {"subject": subject, "result": result},
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return {
        "identity": "ordered-path-source-position-material:"
        + hashlib.sha256(exact).hexdigest(),
        "subject": subject,
        "result": result,
        "source_provenance": "exact ordered relation path source coordinates",
        "scope": {"locality_identity": inputs["locality_identity"]},
        "unknown": [],
        "conflicts": [],
    }


def _compare_result_material(
    act: Event,
    applicability: Event,
    inputs: dict[str, Any],
) -> dict[str, Any]:
    material = act.material
    return {
        "result_identity": material["compare_result_identity"],
        "compare_act_identity": material["act_identity"],
        "act_occurrence_identity": material["act_occurrence_identity"],
        "act": COMPARE_ACT,
        "responsibility": RESPONSIBILITY,
        "responsible_boundary": "this Seed",
        "applicability_result_event_identity": applicability.identity,
        "applicability_of_input_to_compare": deepcopy(
            applicability.material["applicability_of_input_to_compare"]
        ),
        "participation_of_input_in_compare": deepcopy(
            act.material["participation_of_input_in_compare"]
        ),
        "comparison_rule": RULE,
        "finding": _finding(inputs),
        "path_result_reference": deepcopy(inputs["reference"]),
        "path_position_pair": list(inputs["path_position_pair"]),
        "scope": deepcopy(material["scope"]),
        "unknown": [],
        "conflicts": [],
        "act_occurrence_event_identity": act.identity,
    }


def _read_compare_result(
    ledger: EventLedger, event_identity: Any
) -> tuple[Event, Event, Event, dict[str, Any]]:
    candidate = ledger.get(event_identity) if type(event_identity) is str else None
    act, applicability, inputs = _read_compare_act(
        ledger,
        candidate.material.get("act_occurrence_event_identity")
        if candidate is not None
        else None,
    )
    event = _read_yielded(
        ledger,
        event_identity,
        event_kind=COMPARE_RESULT_KIND,
        act=act,
        expected=_compare_result_material(act, applicability, inputs),
        occurrence_boundary=COMPARE_BOUNDARY,
        result_kind="Compare result of ordered path source position material",
        occurrence_coordinate="act_occurrence_identity",
    )
    return event, act, applicability, inputs


def get_recorded_ordered_path_source_position_material_comparison(
    ledger: EventLedger, event_identity: str
) -> dict[str, Any]:
    return deepcopy(_read_compare_result(ledger, event_identity)[0].material)


def validate_ordered_path_source_position_material_comparison_event(
    ledger: EventLedger, event_identity: str
) -> Event:
    event = ledger.get(event_identity)
    if event is None:
        raise ValueError("source position Compare occurrence is not exact")
    if event.kind == APPLICABILITY_ACT_KIND:
        return _read_applicability_act(ledger, event.identity)[0]
    if event.kind == APPLICABILITY_RESULT_KIND:
        return _read_applicability_result(ledger, event.identity)[0]
    if event.kind == COMPARE_ACT_KIND:
        return _read_compare_act(ledger, event.identity)[0]
    if event.kind == COMPARE_RESULT_KIND:
        return _read_compare_result(ledger, event.identity)[0]
    raise ValueError("source position Compare occurrence is not exact")


def _require_tip(ledger: EventLedger, event: Event) -> None:
    if ledger.append_boundary_through_occurrence(event.identity) != ledger.append_boundary():
        raise ValueError("source position Compare stage left its exact boundary")


def _yield_result(
    ledger: EventLedger,
    *,
    act: Event,
    result_kind: str,
    result_identity: str,
    result_content: dict[str, Any],
    exact_act: str,
    occurrence_boundary: str,
    occurrence_coordinate: str,
) -> Event:
    return _record_yield_relation(
        ledger,
        locality_identity=act.locality_identity,
        exact_act=exact_act,
        act_occurrence_identity=act.material[occurrence_coordinate],
        act_occurrence_event_identity=act.identity,
        result_kind=result_kind,
        result_identity=result_identity,
        result_content={
            key: value
            for key, value in result_content.items()
            if key != "act_occurrence_identity"
        },
        occurrence_boundary=occurrence_boundary,
        responsible_act_occurrence_coordinate=occurrence_coordinate,
    )


def _record_ordered_path_source_position_material_comparison(
    ledger: EventLedger,
    *,
    path_result_event_identity: str,
    path_position_pair: tuple[int, int],
    locality_standing: dict[str, Any],
) -> OrderedPathSourcePositionMaterialComparison:
    """Record one exact path-ordered pair Compare."""

    if not isinstance(ledger, EventLedger):
        raise TypeError("source position Compare requires an EventLedger")
    standing = locality_standing
    locality_identity = standing.get("locality_identity")
    boundary = standing.get("through_event_occurrence_identity")
    if (
        type(locality_identity) is not str
        or not locality_identity
        or type(boundary) is not str
        or not boundary
        or ledger.append_boundary().identity != ledger.append_boundary_through_occurrence(
            boundary
        ).identity
    ):
        raise ValueError("source position Compare requires exact current Standing")
    inputs = _path_input(
        ledger,
        path_result_event_identity,
        path_position_pair=path_position_pair,
        prior_standing=standing,
    )
    identities = _new_identities()
    from seed_runtime.operator_locality_standing import (
        _exact_standing_additions,
        _record_distinct,
    )

    def carry(*events: Event) -> None:
        prior = standing["through_event_occurrence_identity"]
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
        for carried in events:
            additions = _exact_standing_additions(
                standing,
                carried,
                error_message="source position Compare Standing is not exact",
            )
            if carried.kind == APPLICABILITY_RESULT_KIND:
                standing["applicability_result_occurrences"][carried.identity] = None
            elif carried.kind == COMPARE_RESULT_KIND:
                standing["comparison_result_occurrences"][carried.identity] = None
            for key, values in additions.items():
                for value in values:
                    _record_distinct(standing[key], value)
            standing["through_event_occurrence_identity"] = carried.identity
            standing["event_count"] += 1

    applicability_act = ledger.append(
        APPLICABILITY_ACT_KIND,
        _applicability_act_material(inputs, boundary, identities),
        locality_identity=locality_identity,
    )
    carry(applicability_act)
    applicability_material = _applicability_result_material(applicability_act)
    _require_tip(ledger, applicability_act)
    applicability_yield = _yield_result(
        ledger,
        act=applicability_act,
        result_kind="Applicability result of ordered path source position material",
        result_identity=applicability_material["result_identity"],
        result_content=applicability_material,
        exact_act=APPLICABILITY_ACT,
        occurrence_boundary=APPLICABILITY_BOUNDARY,
        occurrence_coordinate="applicability_act_occurrence_identity",
    )
    applicability = ledger.append(
        APPLICABILITY_RESULT_KIND,
        _recorded_applicability_result_material(
            applicability_material, applicability_yield.identity
        ),
        locality_identity=locality_identity,
    )
    carry(applicability_yield, applicability)
    compare_act = ledger.append(
        COMPARE_ACT_KIND,
        _compare_act_material(applicability),
        locality_identity=locality_identity,
    )
    carry(compare_act)
    result_material = _compare_result_material(compare_act, applicability, inputs)
    _require_tip(ledger, compare_act)
    result_yield = _yield_result(
        ledger,
        act=compare_act,
        result_kind="Compare result of ordered path source position material",
        result_identity=result_material["result_identity"],
        result_content=result_material,
        exact_act=COMPARE_ACT,
        occurrence_boundary=COMPARE_BOUNDARY,
        occurrence_coordinate="act_occurrence_identity",
    )
    result = ledger.append(
        COMPARE_RESULT_KIND,
        _recorded_compare_result_material(result_material, result_yield.identity),
        locality_identity=locality_identity,
    )
    carry(result_yield, result)
    return OrderedPathSourcePositionMaterialComparison(standing, result)


def yield_ordered_path_source_position_material_comparisons(
    ledger: EventLedger,
    *,
    path_result_event_identity: str,
    locality_standing: dict[str, Any],
) -> Iterator[OrderedPathSourcePositionMaterialComparison]:
    """Yield every distinct path-ordered coordinate pair before returning."""

    standing = locality_standing
    for path_position_pair in _PATH_POSITION_PAIRS:
        comparison = _record_ordered_path_source_position_material_comparison(
            ledger,
            path_result_event_identity=path_result_event_identity,
            path_position_pair=path_position_pair,
            locality_standing=standing,
        )
        standing = comparison.locality_standing
        yield comparison
