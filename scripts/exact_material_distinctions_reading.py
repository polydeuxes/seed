#!/usr/bin/env python3
"""Exact result readings from independently bounded materials."""

from __future__ import annotations

from copy import deepcopy
from io import BytesIO
from pprint import pprint
from typing import Any, Callable

from seed_runtime.byte_measurement import (
    BYTE_MEASUREMENT_RECORDED_KIND,
    BYTE_PAIR_MEASUREMENT_RECORDED_KIND,
    result_positions_of_recorded_byte_measurement,
    result_positions_of_recorded_byte_position_pair_measurement,
)
from seed_runtime.comparison_of_ordered_relation_path_with_recorded_pair_findings import (
    COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_APPLICABILITY_RESULT_KIND,
    COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_RESULT_KIND,
    get_recorded_comparison_of_ordered_relation_path_with_recorded_pair_findings,
    get_recorded_comparison_of_ordered_relation_path_with_recorded_pair_findings_applicability,
)
from seed_runtime.comparison_of_recorded_byte_pair_measurements import (
    RECORDED_PAIR_MEASUREMENT_COMPARISON_APPLICABILITY_RESULT_KIND,
    RECORDED_PAIR_MEASUREMENT_COMPARISON_RESULT_KIND,
    get_recorded_pair_measurement_comparison,
    get_recorded_pair_measurement_comparison_applicability,
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
from seed_runtime.operator_console import run_persistent_operator_console
from seed_runtime.operator_current_coordinates import read_operator_current_coordinates


LOCALITY = "exact-material-Distinctions-reading"
MATERIALS_WITH_H = (
    b"A+B=C\n",
    b"A+D=E\n",
    b"F+B=G\n",
    b"F+D=H\n",
)
MATERIALS_WITH_X = MATERIALS_WITH_H[:-1] + (b"F+D=X\n",)


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


def exact_material_distinctions_reading(
    materials: tuple[bytes, ...],
    *,
    locality_identity: str = LOCALITY,
) -> dict[str, tuple[tuple[str, Any], ...]]:
    """Read only exact result surfaces after existing Seed physiology runs."""

    exact_materials = _exact_materials(materials)
    ledger = EventLedger()
    run_persistent_operator_console(
        ledger=ledger,
        locality_identity=locality_identity,
        input_stream=BytesIO(b"".join(exact_materials)),
    )
    current_coordinates = read_operator_current_coordinates(
        ledger,
        locality_identity=locality_identity,
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
            reader=result_positions_of_recorded_byte_measurement,
        ),
        "pair_measurement_result_positions": _kind_readings(
            ledger,
            locality_identity=locality_identity,
            kind=BYTE_PAIR_MEASUREMENT_RECORDED_KIND,
            reader=result_positions_of_recorded_byte_position_pair_measurement,
        ),
        "pair_compare_applicability_results": _kind_readings(
            ledger,
            locality_identity=locality_identity,
            kind=RECORDED_PAIR_MEASUREMENT_COMPARISON_APPLICABILITY_RESULT_KIND,
            reader=get_recorded_pair_measurement_comparison_applicability,
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
        "path_compare_applicability_results": _kind_readings(
            ledger,
            locality_identity=locality_identity,
            kind=COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_APPLICABILITY_RESULT_KIND,
            reader=get_recorded_comparison_of_ordered_relation_path_with_recorded_pair_findings_applicability,
        ),
        "path_compare_results": _kind_readings(
            ledger,
            locality_identity=locality_identity,
            kind=COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_RESULT_KIND,
            reader=lambda exact_ledger, identity: (
                get_recorded_comparison_of_ordered_relation_path_with_recorded_pair_findings(
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
    return readings


if __name__ == "__main__":
    pprint(exact_material_distinctions_reading(MATERIALS_WITH_H))
