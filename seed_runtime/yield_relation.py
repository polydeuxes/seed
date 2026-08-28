"""One exact Yield relation from an Act occurrence to its result."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from seed_runtime.event import Event
from seed_runtime.events import CORRUPTED, EventLedger

RECORDED_YIELD_RELATION_EVENT = "operator.yield_relation_recorded"
EVENT_KIND_BOOK_CLAUSES = {
    RECORDED_YIELD_RELATION_EVENT: "02.Acts.A",
}
OCCURRENCE_BOUNDARIES_OF_YIELD_RELATION = frozenset(
    {
        "assertion_locality_movement",
        "addressed_byte_occurrence_reference_determination",
        "addressed_byte_occurrence_reference_determination_applicability",
        "failed_boundary",
        "byte_measurement",
        "byte_pair_applicability",
        "byte_pair_measurement",
        "witness_material_source",
        "occurrence_position_measurement",
        "measurement_of_recurrent_byte_pair_occurrence_position",
        "operator_material_source",
        "recorded_pair_measurement_comparison_applicability",
        "recorded_pair_measurement_comparison",
        "comparison_of_ordered_relation_path_with_recorded_pair_findings_applicability",
        "comparison_of_ordered_relation_path_with_recorded_pair_findings_compare",
        "compare_distinction_measurement",
        "comparison_of_ordered_path_source_position_material_applicability",
        "comparison_of_ordered_path_source_position_material_compare",
        "source_position_compare_applicability",
        "source_position_compare",
        "source_position_measurement",
        "source_position_recurrence_measurement",
        "recurrence_corresponding_source_position_material_measurement",
        "recurrent_result_exact_material_measurement",
        "through_occurrence_boundary_reference",
    }
)
def read_requirements_of_yield_carried_by_result_occurrence(
    ledger: EventLedger,
    *,
    recorded_result_event_identity: str,
    yield_relation_event_identity: str | None,
    recorded_result_occurrence_coordinate: str = "act_occurrence_identity",
) -> dict[str, bool]:
    """Read the exact Yield relation carried by one result occurrence."""

    if not isinstance(ledger, EventLedger):
        raise TypeError("a Yield read requires one EventLedger")
    if (
        type(recorded_result_event_identity) is not str
        or not recorded_result_event_identity
    ):
        raise TypeError("a Yield read requires one result occurrence")
    if (
        type(yield_relation_event_identity) is not str
        or not yield_relation_event_identity
    ):
        return {
            "exact_relation": False,
            "occurrence_witness": False,
            "intact_occurrence": False,
        }
    if (
        type(recorded_result_occurrence_coordinate) is not str
        or not recorded_result_occurrence_coordinate
    ):
        raise TypeError("the carried result occurrence coordinate must be exact")

    recorded_result_event = ledger.get(recorded_result_event_identity)
    yield_relation = ledger.get(
        yield_relation_event_identity
    )
    if recorded_result_event is None or yield_relation is None:
        return {
            "exact_relation": False,
            "occurrence_witness": False,
            "intact_occurrence": False,
        }

    exact_relation = (
        recorded_result_event.material.get(
            "yield_relation_identity"
        )
        == yield_relation.identity
        and yield_relation.kind
        == RECORDED_YIELD_RELATION_EVENT
    )
    occurrence_witness = (
        recorded_result_event.locality_identity
        == yield_relation.locality_identity
        and recorded_result_event.material.get(
            recorded_result_occurrence_coordinate
        )
        == yield_relation.material.get("dimensions", {}).get(
            "act_occurrence_identity"
        )
    )
    if occurrence_witness:
        try:
            ledger.occurrences_in_append_order(
                (
                    yield_relation.identity,
                    recorded_result_event.identity,
                ),
                locality_identity=recorded_result_event.locality_identity,
            )
        except (TypeError, ValueError):
            occurrence_witness = False

    return {
        "exact_relation": exact_relation,
        "occurrence_witness": occurrence_witness,
        "intact_occurrence": (
            ledger.integrity_of(yield_relation.identity)
            != CORRUPTED
        ),
    }


def read_requirements_of_yield_relation(
    ledger: EventLedger,
    *,
    recorded_result_event_identity: str,
    yield_relation_event_identity: str | None,
    act_occurrence_event_identity: str | None,
    recorded_result_occurrence_coordinate: str = "act_occurrence_identity",
    yielding_act_occurrence_coordinate: str = "act_occurrence_identity",
) -> dict[str, bool]:
    """Read the three witness-grammar requirements of one exact Yield relation.

    The caller supplies exact occurrence identities under pressure.  Seed
    resolves the recorded occurrences itself; it does not accept read
    event materials and does not re-encode the exact result.  A missing
    result-yield_relation occurrence makes every requirement absent.  Changing an
    unrelated event coordinate does not.
    """

    if not isinstance(ledger, EventLedger):
        raise TypeError("a Yield relation read requires one EventLedger")
    if not isinstance(recorded_result_event_identity, str) or not recorded_result_event_identity:
        raise TypeError("a Yield relation read requires one event occurrence")
    recorded_result_event = ledger.get(recorded_result_event_identity)
    if recorded_result_event is None:
        return {
            "exact_relation": False,
            "occurrence_witness": False,
            "intact_occurrence": False,
        }
    yield_relation = (
        ledger.get(yield_relation_event_identity)
        if isinstance(yield_relation_event_identity, str)
        else None
    )
    act_occurrence = (
        ledger.get(act_occurrence_event_identity)
        if isinstance(act_occurrence_event_identity, str)
        else None
    )
    if yield_relation is None:
        return {
            "exact_relation": False,
            "occurrence_witness": False,
            "intact_occurrence": False,
        }
    if not isinstance(recorded_result_occurrence_coordinate, str) or not (
        recorded_result_occurrence_coordinate
    ):
        raise TypeError("the event occurrence coordinate must be exact")
    if not isinstance(yielding_act_occurrence_coordinate, str) or not (
        yielding_act_occurrence_coordinate
    ):
        raise TypeError("the responsible-Act occurrence coordinate must be exact")

    act_occurrence_identity_of_recorded_result = recorded_result_event.material.get(
        recorded_result_occurrence_coordinate
    )
    yield_dimensions = yield_relation.material.get("dimensions", {})
    same_occurrence = act_occurrence_identity_of_recorded_result == yield_dimensions.get(
        "act_occurrence_identity"
    )
    if act_occurrence is not None:
        same_occurrence = same_occurrence and act_occurrence_identity_of_recorded_result == (
            act_occurrence.material.get(
                yielding_act_occurrence_coordinate
            )
        )
    else:
        same_occurrence = False

    yield_is_carried = (
        recorded_result_event.material.get("yield_relation_identity") == yield_relation.identity
        and yield_relation.kind == RECORDED_YIELD_RELATION_EVENT
    )
    yield_is_carried = yield_is_carried and (
        recorded_result_event.exact_material == yield_relation.exact_material
    )
    result = yield_relation.material.get("result")
    result_identity = yield_relation.material.get("result_identity")
    coordinates_of_carried_result = yield_relation.material.get("coordinates_of_carried_result")
    coordinates_of_recorded_result = yield_relation.material.get("coordinates_of_recorded_result")
    exact_carried_result = False
    if (
        type(result) is dict
        and type(coordinates_of_carried_result) is list
        and type(coordinates_of_recorded_result) is dict
        and coordinates_of_carried_result == list(result)
        and set(coordinates_of_recorded_result) == set(result)
    ):
        carried_result = {}
        for coordinate in coordinates_of_carried_result:
            carried_at = coordinates_of_recorded_result.get(coordinate)
            if type(carried_at) is not list or not carried_at or not all(
                type(part) is str and part for part in carried_at
            ):
                break
            value = recorded_result_event.material
            for part in carried_at:
                if type(value) is not dict or part not in value:
                    break
                value = value[part]
            else:
                carried_result[coordinate] = value
                continue
            break
        else:
            exact_carried_result = carried_result == result
    yield_is_carried = (
        yield_is_carried
        and exact_carried_result
        and isinstance(result_identity, str)
        and result_identity
        and type(result) is dict
        and result.get("result_identity") == result_identity
        and recorded_result_event.material.get("result_identity") == result_identity
    )
    if act_occurrence is not None:
        exact_act_occurrence = (
            yield_dimensions.get("exact_act")
            == act_occurrence.material.get("act")
        )
        yield_is_carried = yield_is_carried and (
            recorded_result_event.material.get("act_occurrence_event_identity")
            == act_occurrence.identity
            and yield_relation.material.get("act_occurrence_event_identity")
            == act_occurrence.identity
            and exact_act_occurrence
        )
    else:
        yield_is_carried = False

    return {
        "exact_relation": yield_is_carried,
        "occurrence_witness": same_occurrence,
        "intact_occurrence": (
            ledger.integrity_of(yield_relation.identity) != CORRUPTED
            and (
                act_occurrence is not None
                and ledger.integrity_of(act_occurrence.identity) != CORRUPTED
            )
        ),
    }


def _record_yield_relation(
    ledger: EventLedger,
    *,
    locality_identity: str | None,
    exact_act: str,
    act_occurrence_identity: str,
    act_occurrence_event_identity: str,
    result_kind: str,
    result_identity: str,
    result_content: dict[str, Any],
    occurrence_boundary: str,
    yielding_act_occurrence_coordinate: str = "act_occurrence_identity",
    coordinates_of_recorded_result: dict[str, tuple[str, ...]] | None = None,
    result_exact_material: bytes | None = None,
) -> Event:
    """Record Yield after its Act occurrence has fixed the exact result."""

    if not isinstance(act_occurrence_identity, str) or not act_occurrence_identity:
        raise ValueError("Yield requires one exact Act occurrence identity")
    if (
        not isinstance(act_occurrence_event_identity, str)
        or not act_occurrence_event_identity
    ):
        raise ValueError("Yield requires one exact Act occurrence")
    if (
        not isinstance(yielding_act_occurrence_coordinate, str)
        or not yielding_act_occurrence_coordinate
    ):
        raise ValueError("Yield requires one exact Act occurrence coordinate")
    act_occurrence = ledger.get(act_occurrence_event_identity)
    if (
        act_occurrence is None
        or act_occurrence.material.get(yielding_act_occurrence_coordinate)
        != act_occurrence_identity
        or act_occurrence.material.get("act") != exact_act
        or ledger.integrity_of(act_occurrence_event_identity) == CORRUPTED
    ):
        raise ValueError(
            "Yield requires its intact Act occurrence"
        )
    if occurrence_boundary not in OCCURRENCE_BOUNDARIES_OF_YIELD_RELATION:
        raise ValueError(
            "Yield requires one declared occurrence boundary"
        )
    if type(result_content) is not dict:
        raise TypeError("Yield requires one exact result")
    if not isinstance(result_identity, str) or not result_identity:
        raise TypeError("Yield requires one exact result identity")
    if result_content.get("result_identity") != result_identity:
        raise ValueError("Yield result identity must be carried by its result")
    if result_exact_material is not None and type(result_exact_material) is not bytes:
        raise TypeError("Yield exact material must be exact bytes or absent")
    declared_coordinates_of_recorded_result = (
        {coordinate: (coordinate,) for coordinate in result_content}
        if coordinates_of_recorded_result is None
        else coordinates_of_recorded_result
    )
    if type(declared_coordinates_of_recorded_result) is not dict or set(
        declared_coordinates_of_recorded_result
    ) != set(result_content):
        raise ValueError(
            "Yield requires one carried coordinate for every result coordinate"
        )
    preserved_coordinates_of_recorded_result = {}
    for coordinate, carried_at in declared_coordinates_of_recorded_result.items():
        if type(coordinate) is not str or not coordinate:
            raise TypeError("a result coordinate must have one exact name")
        if type(carried_at) is not tuple or not carried_at or not all(
            type(part) is str and part for part in carried_at
        ):
            raise TypeError(
                "a carried coordinate must have one nonempty tuple of exact names"
            )
        preserved_coordinates_of_recorded_result[coordinate] = list(carried_at)

    return ledger.append(
        RECORDED_YIELD_RELATION_EVENT,
        {
            "act_occurrence_event_identity": act_occurrence_event_identity,
            "result_identity": result_identity,
            "dimensions": {
                "identity": (
                    f"yield:{act_occurrence_identity}:{result_identity}"
                ),
                "exact_act": exact_act,
                "act_occurrence_identity": act_occurrence_identity,
            },
            "coordinates_of_carried_result": list(result_content),
            "result": deepcopy(result_content),
            "coordinates_of_recorded_result": preserved_coordinates_of_recorded_result,
            "result_kind": result_kind,
            "occurrence_boundary": occurrence_boundary,
        },
        exact_material=result_exact_material,
        locality_identity=locality_identity,
    )
