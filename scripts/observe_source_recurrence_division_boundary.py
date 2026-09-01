#!/usr/bin/env python3
"""Observe whether live source recurrence supplies a source-division rule.

The operation mirrors the equality surfaces and source-exhausted continuation
of ``source_position_recurrence`` without recording its Responsibility, Act,
Yield, and result occurrences.  It is an observer of that already-live rule,
not a replacement runtime road.

The frozen artifact carries hashes rather than source material.  No byte,
final coordinate count, recurring surface, or exact material is selected by
the caller.
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


OUTPUT = Path("/tmp/seed_source_recurrence_division_boundary.json")


def _encoded(value: object) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode()


def _digest(material: bytes) -> str:
    return sha256(material).hexdigest()


def _same_content_surface(material: bytes) -> tuple[int, ...]:
    """Return the complete same-content/difference surface without labels."""

    first_coordinate: dict[int, int] = {}
    return tuple(
        first_coordinate.setdefault(value, len(first_coordinate))
        for value in material
    )


def _observe_one_source(source_number: int, material: bytes) -> dict:
    active_starts = tuple(range(max(0, len(material) - 1)))
    steps = []
    exact_material_results = []
    coordinate_count = 2

    while active_starts:
        by_surface: dict[tuple[int, ...], list[int]] = defaultdict(list)
        for start in active_starts:
            later = start + coordinate_count
            if later <= len(material):
                by_surface[
                    _same_content_surface(material[start:later])
                ].append(start)

        recurring = tuple(
            (surface, tuple(starts))
            for surface, starts in sorted(by_surface.items())
            if len(starts) > 1
        )
        exact_at_this_count = []
        for surface, starts in recurring:
            exact = material[starts[0] : starts[0] + coordinate_count]
            if any(
                material[start : start + coordinate_count] != exact
                for start in starts[1:]
            ):
                continue
            finding = {
                "coordinate_count": coordinate_count,
                "same_content_surface_sha256": _digest(_encoded(surface)),
                "exact_material_sha256": _digest(exact),
                "occurrence_positions": list(starts),
            }
            exact_at_this_count.append(finding)
            exact_material_results.append(finding)

        steps.append(
            {
                "coordinate_count": coordinate_count,
                "addressed_consecutive_material_count": len(active_starts),
                "recurring_surface_count": len(recurring),
                "exact_material_result_count": len(exact_at_this_count),
            }
        )

        active_starts = tuple(
            start
            for _surface, starts in recurring
            for start in starts
            if start + coordinate_count < len(material)
        )
        coordinate_count += 1

    return {
        "source_number": source_number,
        "source_material_sha256": _digest(material),
        "source_byte_count": len(material),
        "steps": steps,
        "recurring_surface_count": sum(
            step["recurring_surface_count"] for step in steps
        ),
        "exact_material_result_count": len(exact_material_results),
        "largest_exact_material_coordinate_count": max(
            (
                finding["coordinate_count"]
                for finding in exact_material_results
            ),
            default=0,
        ),
        "exact_material_results": exact_material_results,
    }


def observe_sources(materials: tuple[bytes, ...]) -> dict:
    sources = [
        _observe_one_source(source_number, material)
        for source_number, material in enumerate(materials)
    ]
    return {
        "operation": (
            "all consecutive two-coordinate subjects; complete same-content/"
            "difference surfaces; continue every recurring surface by one source "
            "coordinate until no recurring surface can continue; retain exact "
            "material only when every supporting result carries the same bytes"
        ),
        "sources": sources,
        "source_count": len(sources),
        "known_loss": (
            "Responsibility, Act, Yield, result, and current Standing occurrences "
            "are not recorded by this observer"
        ),
    }


def observe() -> dict:
    return observe_sources(SOURCE_GROUPS[0])


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
                "artifact_sha256": _digest(encoded),
                "artifact_bytes": len(encoded),
                "wall_seconds": result["wall_seconds"],
                "sources": [
                    {
                        "source_number": source["source_number"],
                        "source_byte_count": source["source_byte_count"],
                        "recurring_surface_count": source[
                            "recurring_surface_count"
                        ],
                        "exact_material_result_count": source[
                            "exact_material_result_count"
                        ],
                        "largest_exact_material_coordinate_count": source[
                            "largest_exact_material_coordinate_count"
                        ],
                    }
                    for source in result["sources"]
                ],
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
