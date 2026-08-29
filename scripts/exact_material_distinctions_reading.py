#!/usr/bin/env python3
"""Exact result readings from independently bounded materials."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import is_dataclass
from io import BytesIO
from pprint import pprint
from typing import Any, Callable

from seed_runtime.byte_measurement import (
    BYTE_MEASUREMENT_RECORDED_KIND,
    BYTE_PAIR_MEASUREMENT_RECORDED_KIND,
    result_positions_of_recorded_byte_measurement,
    result_positions_of_recorded_byte_position_pair_measurement,
)
from seed_runtime.comparison_of_shared_position_measurement_with_recorded_pair_findings import (
    COMPARISON_OF_SHARED_POSITION_MEASUREMENT_WITH_RECORDED_PAIR_FINDINGS_APPLICABILITY_RESULT_KIND,
    COMPARISON_OF_SHARED_POSITION_MEASUREMENT_WITH_RECORDED_PAIR_FINDINGS_RESULT_KIND,
    get_recorded_comparison_of_shared_position_measurement_with_recorded_pair_findings,
    get_recorded_comparison_of_shared_position_measurement_with_recorded_pair_findings_applicability,
)
from seed_runtime.comparison_of_recorded_byte_pair_measurements import (
    RECORDED_PAIR_MEASUREMENT_COMPARISON_RESULT_KIND,
    get_recorded_pair_measurement_comparison,
)
from seed_runtime.events import EventLedger
from seed_runtime.material_source import (
    exact_material_result_bytes,
    iter_exact_material_results,
)
from seed_runtime.measurement_of_compare_distinctions import (
    COMPARE_DISTINCTION_MEASUREMENT_RESULT_KIND,
    get_recorded_compare_distinction_measurement,
)
from seed_runtime.measurement_of_position_coordinates_of_byte_pair_occurrences import (
    BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND,
)
from seed_runtime.measurement_of_shared_position_of_byte_pair_occurrences import (
    SHARED_POSITION_MEASUREMENT_RESULT_KIND,
    get_recorded_shared_position_measurement,
)
from seed_runtime.operator_console import run_persistent_operator_console


LOCALITY = "exact-material-Distinctions-reading"
MATERIALS_WITH_H = (
    b"A+B=C\n",
    b"A+D=E\n",
    b"F+B=G\n",
    b"F+D=H\n",
)
MATERIALS_WITH_X = MATERIALS_WITH_H[:-1] + (b"F+D=X\n",)


class _ExactMaterialBoundaries:
    def __init__(self, materials: tuple[bytes, ...]) -> None:
        self._materials = iter(materials)

    def readline(self) -> bytes:
        return next(self._materials, b"")


def _exact_materials(materials: tuple[bytes, ...]) -> tuple[bytes, ...]:
    if (
        type(materials) is not tuple
        or not materials
        or any(
            type(material) is not bytes
            or not material
            or not material.endswith(b"\n")
            or b"\n" in material[:-1]
            for material in materials
        )
    ):
        raise ValueError(
            "each material must be one nonempty exact line boundary"
        )
    return materials


def _exact_bounded_materials(
    materials: tuple[bytes, ...],
) -> tuple[bytes, ...]:
    if (
        type(materials) is not tuple
        or not materials
        or any(type(material) is not bytes or not material for material in materials)
    ):
        raise ValueError("each material must have one nonempty exact boundary")
    return materials


def _kind_readings(
    ledger: EventLedger,
    *,
    locality_identity: str,
    kind: str,
    reader: Callable[[EventLedger, str], Any],
) -> tuple[tuple[str, Any], ...]:
    return tuple(
        (event.identity, reader(ledger, event.identity))
        for event in ledger.iter_locality_kind(locality_identity, kind)
    )


def _exact_material_distinctions_reading(
    materials: tuple[bytes, ...],
    *,
    locality_identity: str,
    exact_boundaries: bool = False,
) -> tuple[EventLedger, dict[str, tuple[tuple[str, Any], ...]]]:
    exact_materials = (
        _exact_bounded_materials(materials)
        if exact_boundaries
        else _exact_materials(materials)
    )
    ledger = EventLedger()
    current_coordinates = run_persistent_operator_console(
        ledger=ledger,
        locality_identity=locality_identity,
        input_stream=(
            _ExactMaterialBoundaries(exact_materials)
            if exact_boundaries
            else BytesIO(b"".join(exact_materials))
        ),
    )
    through = ledger.append_boundary()

    material_results = tuple(
        (
            result.identity,
            {
                "exact_material": exact_material_result_bytes(result),
                "coordinates": deepcopy(result.material),
            },
        )
        for result in iter_exact_material_results(ledger, locality_identity)
    )
    readings = {
        "material_results": material_results,
        "byte_measurement_result_positions": _kind_readings(
            ledger,
            locality_identity=locality_identity,
            kind=BYTE_MEASUREMENT_RECORDED_KIND,
            reader=lambda exact_ledger, identity: (
                result_positions_of_recorded_byte_measurement(
                    exact_ledger,
                    identity,
                    prior_coordinates=current_coordinates,
                )
            ),
        ),
        "pair_measurement_result_positions": _kind_readings(
            ledger,
            locality_identity=locality_identity,
            kind=BYTE_PAIR_MEASUREMENT_RECORDED_KIND,
            reader=lambda exact_ledger, identity: (
                result_positions_of_recorded_byte_position_pair_measurement(
                    exact_ledger,
                    identity,
                    prior_coordinates=current_coordinates,
                )
            ),
        ),
        "shared_position_measurement_results": _kind_readings(
            ledger,
            locality_identity=locality_identity,
            kind=SHARED_POSITION_MEASUREMENT_RESULT_KIND,
            reader=lambda exact_ledger, identity: (
                get_recorded_shared_position_measurement(
                    exact_ledger,
                    identity,
                    prior_coordinates=current_coordinates,
                )
            ),
        ),
        "pair_compare_results": _kind_readings(
            ledger,
            locality_identity=locality_identity,
            kind=RECORDED_PAIR_MEASUREMENT_COMPARISON_RESULT_KIND,
            reader=lambda exact_ledger, identity: (
                get_recorded_pair_measurement_comparison(
                    exact_ledger,
                    identity,
                    prior_coordinates=current_coordinates,
                )
            ),
        ),
        "shared_position_compare_applicability_results": _kind_readings(
            ledger,
            locality_identity=locality_identity,
            kind=COMPARISON_OF_SHARED_POSITION_MEASUREMENT_WITH_RECORDED_PAIR_FINDINGS_APPLICABILITY_RESULT_KIND,
            reader=lambda exact_ledger, identity: (
                get_recorded_comparison_of_shared_position_measurement_with_recorded_pair_findings_applicability(
                    exact_ledger,
                    identity,
                    prior_coordinates=current_coordinates,
                )
            ),
        ),
        "shared_position_compare_results": _kind_readings(
            ledger,
            locality_identity=locality_identity,
            kind=COMPARISON_OF_SHARED_POSITION_MEASUREMENT_WITH_RECORDED_PAIR_FINDINGS_RESULT_KIND,
            reader=lambda exact_ledger, identity: (
                get_recorded_comparison_of_shared_position_measurement_with_recorded_pair_findings(
                    exact_ledger,
                    identity,
                    prior_coordinates=current_coordinates,
                )
            ),
        ),
        "distinction_measurement_results": _kind_readings(
            ledger,
            locality_identity=locality_identity,
            kind=COMPARE_DISTINCTION_MEASUREMENT_RESULT_KIND,
            reader=lambda exact_ledger, identity: (
                get_recorded_compare_distinction_measurement(
                    exact_ledger,
                    identity,
                    prior_coordinates=current_coordinates,
                )
            ),
        ),
    }
    if ledger.append_boundary() != through:
        raise RuntimeError("reading appended a Seed occurrence")
    return ledger, readings


def exact_material_distinctions_reading(
    materials: tuple[bytes, ...],
    *,
    locality_identity: str = LOCALITY,
) -> dict[str, tuple[tuple[str, Any], ...]]:
    """Read only exact result surfaces after existing Seed physiology runs."""

    _ledger, reading = _exact_material_distinctions_reading(
        materials,
        locality_identity=locality_identity,
    )
    return reading


def exact_bounded_material_distinctions_reading(
    materials: tuple[bytes, ...],
    *,
    locality_identity: str = LOCALITY,
) -> dict[str, tuple[tuple[str, Any], ...]]:
    """Read exact result surfaces from explicitly bounded material."""

    _ledger, reading = _exact_material_distinctions_reading(
        materials,
        locality_identity=locality_identity,
        exact_boundaries=True,
    )
    return reading


def _source_occurrence_positions(
    reading: dict[str, tuple[tuple[str, Any], ...]],
) -> dict[str, int]:
    return {
        occurrence_identity: source_position
        for source_position, (occurrence_identity, _result) in enumerate(
            reading["material_results"]
        )
    }


def _source_positions_from_byte_measurement(
    result_positions: tuple[dict[str, Any], ...],
    source_occurrence_positions: dict[str, int],
) -> tuple[int, ...]:
    source_references = result_positions[0]["subject"][
        "source_occurrence_references"
    ]
    if not source_references:
        raise ValueError("exact source material results are required")
    return tuple(
        source_occurrence_positions[
            reference["material_result_occurrence_identity"]
        ]
        for reference in source_references
    )


def _result_coordinates(
    ledger: EventLedger,
    reading: dict[str, tuple[tuple[str, Any], ...]],
) -> dict[str, tuple[Any, ...]]:
    source_positions = _source_occurrence_positions(reading)
    first_source = ledger.get(reading["material_results"][0][0])
    if first_source is None or type(first_source.locality_identity) is not str:
        raise ValueError("one exact source Locality is required")
    locality_identity = first_source.locality_identity
    coordinates: dict[str, tuple[Any, ...]] = {
        identity: ("material_result", position)
        for identity, position in source_positions.items()
    }

    for identity, result_positions in reading["byte_measurement_result_positions"]:
        coordinates[identity] = (
            "byte_Measurement_result",
            _source_positions_from_byte_measurement(
                result_positions,
                source_positions,
            ),
        )

    for identity, result_positions in reading["pair_measurement_result_positions"]:
        references = result_positions[0].referenced_result_position_references
        if len(references) != 1:
            raise ValueError("one exact byte Measurement result is required")
        source_coordinate = coordinates[
            references[0]["recorded_occurrence_identity"]
        ]
        coordinates[identity] = (
            "pair_Measurement_result",
            source_coordinate[-1],
        )

    for event in ledger.iter_locality_kind(
        locality_identity,
        BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND,
    ):
        source_identity = event.material[
            "source_material_result_occurrence_identity"
        ]
        coordinates[event.identity] = (
            "pair_occurrence_position_Measurement_result",
            source_positions[source_identity],
        )

    for event in ledger.iter_locality_kind(
        locality_identity,
        SHARED_POSITION_MEASUREMENT_RESULT_KIND,
    ):
        source_identity = event.material["result_positions"][0]["content"][
            "source_material_result_occurrence_identity"
        ]
        coordinates[event.identity] = (
            "shared_position_Measurement_result",
            source_positions[source_identity],
            event.material["first_position_result"]["first_position"],
            event.material["first_position_result"]["second_position"],
            event.material["second_position_result"]["second_position"],
        )

    for identity, result in reading["pair_compare_results"]:
        binding = result.get("subject_to_act_binding_reference")
        subjects = (
            binding["subject_reference"]
            if type(binding) is dict
            else result["subject_reference"]
        )
        earlier = coordinates[
            subjects["earlier_measurement_reference"][
                "recorded_occurrence_identity"
            ]
        ][-1]
        later = coordinates[
            subjects["later_measurement_reference"][
                "recorded_occurrence_identity"
            ]
        ][-1]
        coordinates[identity] = ("pair_Compare_result", earlier, later)

    for identity, result in reading["shared_position_compare_applicability_results"]:
        binding = result.get("subject_to_act_binding_reference")
        if type(binding) is dict:
            subjects = binding["subject_reference"]
            shared_position_reference = subjects["shared_position_input"]["subject"]
            comparison_reference = subjects["comparison_input"]["subject"]
        else:
            act = ledger.get(result.get("act_occurrence_event_identity"))
            subjects = (
                act.material.get("subject_reference")
                if act is not None and type(act.material) is dict
                else None
            )
            if type(subjects) is not dict:
                raise ValueError(
                    "shared-position Compare Applicability result has no exact Act subjects"
                )
            shared_position_reference = subjects[
                "shared_position_result_position_reference"
            ]
            comparison_reference = subjects["comparison_result_reference"]
        shared_position_coordinate = coordinates[
            shared_position_reference["recorded_occurrence_identity"]
        ]
        comparison_coordinate = coordinates[
            comparison_reference["recorded_occurrence_identity"]
        ]
        coordinates[identity] = (
            "shared_position_Compare_Applicability_result",
            *shared_position_coordinate[1:],
            comparison_coordinate[-2],
            comparison_coordinate[-1],
        )

    for identity, result in reading["shared_position_compare_results"]:
        subjects = result["finding"]["subject"]
        shared_position_coordinate = coordinates[
            subjects["shared_position_result_position_reference"][
                "recorded_occurrence_identity"
            ]
        ]
        comparison_coordinate = coordinates[
            subjects["recorded_pair_comparison_result_reference"][
                "recorded_occurrence_identity"
            ]
        ]
        coordinates[identity] = (
            "shared_position_Compare_result",
            *shared_position_coordinate[1:],
            comparison_coordinate[-2],
            comparison_coordinate[-1],
        )

    for identity, result in reading["distinction_measurement_results"]:
        source_coordinate = coordinates[
            result["source_result_occurrence_identity"]
        ]
        coordinates[identity] = (
            "Distinctions_Measurement_result",
            *source_coordinate[1:],
        )
    return coordinates


def _result_content(value: Any, coordinates: dict[str, tuple[Any, ...]]) -> Any:
    if is_dataclass(value) and hasattr(value, "material"):
        return _result_content(value.material, coordinates)
    if type(value) is dict:
        content = {}
        for key, item in value.items():
            if key in {
                "locality_identity",
                "source_locality_identity",
                "source_localities",
            }:
                continue
            if type(item) is str and item in coordinates:
                content[key.replace("identity", "coordinate")] = coordinates[item]
                continue
            if "identity" in key:
                continue
            content[key] = _result_content(item, coordinates)
        return content
    if type(value) is list:
        return [_result_content(item, coordinates) for item in value]
    if type(value) is tuple:
        return tuple(_result_content(item, coordinates) for item in value)
    return deepcopy(value)


def _content_by_result_coordinate(
    reading: dict[str, tuple[tuple[str, Any], ...]],
    coordinates: dict[str, tuple[Any, ...]],
) -> dict[str, tuple[tuple[tuple[Any, ...], Any], ...]]:
    return {
        surface: tuple(
            (coordinates[identity], _result_content(result, coordinates))
            for identity, result in results
        )
        for surface, results in reading.items()
    }


def _same_result_content(
    first: dict[str, tuple[tuple[tuple[Any, ...], Any], ...]],
    second: dict[str, tuple[tuple[tuple[Any, ...], Any], ...]],
) -> dict[str, dict[str, tuple[Any, ...]]]:
    result = {}
    for surface in first:
        first_by_coordinate = dict(first[surface])
        second_by_coordinate = dict(second[surface])
        if len(first_by_coordinate) != len(first[surface]) or len(
            second_by_coordinate
        ) != len(second[surface]):
            raise ValueError(
                f"one {surface} coordinate addresses multiple results"
            )
        same = tuple(
            coordinate
            for coordinate, _content in first[surface]
            if coordinate in second_by_coordinate
            and first_by_coordinate[coordinate] == second_by_coordinate[coordinate]
        )
        first_results = tuple(
            (coordinate, content)
            for coordinate, content in first[surface]
            if coordinate not in same
        )
        second_results = tuple(
            (coordinate, content)
            for coordinate, content in second[surface]
            if coordinate not in same
        )
        result[surface] = {
            "same": same,
            "first": first_results,
            "second": second_results,
        }
    return result


def _exact_material_result_content_reading(
    first_materials: tuple[bytes, ...],
    second_materials: tuple[bytes, ...],
    *,
    exact_boundaries: bool,
) -> dict[str, Any]:
    first_ledger, first_reading = _exact_material_distinctions_reading(
        first_materials,
        locality_identity="first-exact-material-Distinctions-reading",
        exact_boundaries=exact_boundaries,
    )
    second_ledger, second_reading = _exact_material_distinctions_reading(
        second_materials,
        locality_identity="second-exact-material-Distinctions-reading",
        exact_boundaries=exact_boundaries,
    )
    first_coordinates = _result_coordinates(first_ledger, first_reading)
    second_coordinates = _result_coordinates(second_ledger, second_reading)
    first_content = _content_by_result_coordinate(
        first_reading,
        first_coordinates,
    )
    second_content = _content_by_result_coordinate(
        second_reading,
        second_coordinates,
    )
    return {
        "first_exact_reading": first_reading,
        "second_exact_reading": second_reading,
        "result_content": _same_result_content(first_content, second_content),
    }


def exact_material_result_content_reading(
    first_materials: tuple[bytes, ...],
    second_materials: tuple[bytes, ...],
) -> dict[str, Any]:
    """Keep exact readings while comparing only source-relative result content."""

    return _exact_material_result_content_reading(
        first_materials,
        second_materials,
        exact_boundaries=False,
    )


def exact_bounded_material_result_content_reading(
    first_materials: tuple[bytes, ...],
    second_materials: tuple[bytes, ...],
) -> dict[str, Any]:
    """Compare source-relative content under explicit material boundaries."""

    return _exact_material_result_content_reading(
        first_materials,
        second_materials,
        exact_boundaries=True,
    )


if __name__ == "__main__":
    material_reading = exact_material_result_content_reading(
        MATERIALS_WITH_H,
        MATERIALS_WITH_X,
    )
    pprint(
        {
            surface: {
                "same": len(result["same"]),
                "first": len(result["first"]),
                "second": len(result["second"]),
            }
            for surface, result in material_reading["result_content"].items()
        }
    )
