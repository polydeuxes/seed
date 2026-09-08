#!/usr/bin/env python3
"""Measure path discrimination and acquisition packaging effects.

The operation starts from raw bytes and mirrors the live consecutive
source-position recurrence rule. It is told no material value, desired path,
coordinate count, or cross-material correspondence.

The output contains hashes rather than source material. It records no Seed
Responsibility, Act, Yield, result, or current Standing occurrence.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from hashlib import sha256
import json
from pathlib import Path
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.observe_cross_surface_structure import SOURCE_GROUPS
from scripts.observe_source_recurrence_division_boundary import (
    _digest,
    _encoded,
    _same_content_surface,
)


OUTPUT = Path("/tmp/seed_source_position_path_discrimination.json")


def _walk(material: bytes) -> dict:
    active_starts = tuple(range(max(0, len(material) - 1)))
    coordinate_count = 2
    addressed_consecutive_paths = 0
    exact_next_coordinate_answers = 0
    any_later_coordinate_answers = 0
    recurring_surfaces = 0
    exact_material_results: list[tuple[int, str]] = []

    while active_starts:
        addressed_consecutive_paths += len(active_starts)
        by_surface: dict[tuple[int, ...], list[int]] = defaultdict(list)
        for start in active_starts:
            later = start + coordinate_count
            if later <= len(material):
                by_surface[
                    _same_content_surface(material[start:later])
                ].append(start)

        recurring = tuple(
            tuple(starts)
            for _surface, starts in sorted(by_surface.items())
            if len(starts) > 1
        )
        recurring_surfaces += len(recurring)

        for starts in recurring:
            exact = material[starts[0] : starts[0] + coordinate_count]
            if all(
                material[start : start + coordinate_count] == exact
                for start in starts[1:]
            ):
                exact_material_results.append((coordinate_count, _digest(exact)))

        recurring_starts = tuple(start for starts in recurring for start in starts)
        exact_next_coordinate_answers += sum(
            start + coordinate_count < len(material)
            for start in recurring_starts
        )
        any_later_coordinate_answers += sum(
            len(material) - (start + coordinate_count)
            for start in recurring_starts
        )
        active_starts = tuple(
            start
            for start in recurring_starts
            if start + coordinate_count < len(material)
        )
        coordinate_count += 1

    return {
        "material_sha256": _digest(material),
        "byte_count": len(material),
        "all_consecutive_path_count": len(material) * max(0, len(material) - 1) // 2,
        "addressed_consecutive_path_count": addressed_consecutive_paths,
        "exact_next_coordinate_answer_count": exact_next_coordinate_answers,
        "any_later_coordinate_answer_count": any_later_coordinate_answers,
        "recurring_surface_count": recurring_surfaces,
        "exact_material_result_count": len(exact_material_results),
        "exact_material_results": [
            {
                "coordinate_count": count,
                "exact_material_sha256": identity,
            }
            for count, identity in exact_material_results
        ],
    }


def _layout(materials: tuple[bytes, ...]) -> dict:
    measurements = [_walk(material) for material in materials if len(material) > 1]
    exact_material_results: dict[tuple[int, str], None] = {}
    for measurement in measurements:
        for result in measurement["exact_material_results"]:
            exact_material_results[
                (
                    result["coordinate_count"],
                    result["exact_material_sha256"],
                )
            ] = None
    joined = b"".join(materials)
    return {
        "acquisition_count": len(materials),
        "ordered_material_sha256": _digest(joined),
        "byte_count": len(joined),
        "addressed_consecutive_path_count": sum(
            measurement["addressed_consecutive_path_count"]
            for measurement in measurements
        ),
        "exact_next_coordinate_answer_count": sum(
            measurement["exact_next_coordinate_answer_count"]
            for measurement in measurements
        ),
        "any_later_coordinate_answer_count": sum(
            measurement["any_later_coordinate_answer_count"]
            for measurement in measurements
        ),
        "recurring_surface_count": sum(
            measurement["recurring_surface_count"]
            for measurement in measurements
        ),
        "exact_material_result_count": sum(
            measurement["exact_material_result_count"]
            for measurement in measurements
        ),
        "distinct_exact_material_result_count": len(exact_material_results),
    }


def observe() -> dict:
    four = SOURCE_GROUPS[0]
    joined = b"".join(four)
    layouts = {
        "one_acquisition": (joined,),
        "four_acquisitions": four,
        "seventeen_byte_acquisitions": tuple(
            joined[start : start + 17] for start in range(0, len(joined), 17)
        ),
    }
    measured = {name: _layout(materials) for name, materials in layouts.items()}
    return {
        "operation": (
            "continue only exact recurrent consecutive source-position paths; "
            "compare one exact next coordinate; repeat the same measurement "
            "with unchanged ordered material under three acquisition layouts"
        ),
        "layouts": measured,
        "same_ordered_material_in_every_layout": len(
            dict.fromkeys(
                layout["ordered_material_sha256"]
                for layout in measured.values()
            )
        ) == 1,
        "known_loss": (
            "Responsibility, Act, Yield, result, current Standing, and exact "
            "continuity across acquisition edges are not recorded"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()

    started = time.perf_counter()
    result = observe()
    result["wall_seconds"] = round(time.perf_counter() - started, 6)
    encoded = _encoded(result)
    args.output.write_bytes(encoded)
    print(
        json.dumps(
            {
                "artifact": str(args.output),
                "artifact_sha256": sha256(encoded).hexdigest(),
                "artifact_bytes": len(encoded),
                "wall_seconds": result["wall_seconds"],
                "same_ordered_material_in_every_layout": result[
                    "same_ordered_material_in_every_layout"
                ],
                "layouts": result["layouts"],
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
