"""Project controlled consequence asymmetry from the frozen source shards.

The complete source artifacts preserve each source-carried bipartite frame and
the exact immediate context population beside every participating production.
This reporter enumerates the implied 2x2 squares only long enough to compare
the two controlled substitution edges of each coordinate.  It writes counts
and exact sample addresses, not an eager copy of all squares.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from concurrent.futures import ProcessPoolExecutor
from hashlib import sha256
from itertools import repeat
import json
from pathlib import Path
import time


INPUT = Path("/tmp/seed_open_world_consequence_asymmetry_manifest.json")
OUTPUT = Path("/tmp/seed_open_world_consequence_asymmetry_pressure.json")


def _canonical(value: object) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode()


def _digest(value: object) -> str:
    material = value if isinstance(value, bytes) else _canonical(value)
    return sha256(material).hexdigest()


def _effect_counts(
    context_references: list[str],
    productions: tuple[int, int, int, int],
) -> tuple[int, int]:
    first_first, first_second, second_first, second_second = productions
    first_coordinate_changes = int(
        context_references[first_first] != context_references[second_first]
    ) + int(context_references[first_second] != context_references[second_second])
    second_coordinate_changes = int(
        context_references[first_first] != context_references[first_second]
    ) + int(context_references[second_first] != context_references[second_second])
    return first_coordinate_changes, second_coordinate_changes


def _observe_source(entry: dict, sample_boundary: int) -> dict:
    encoded = Path(entry["artifact"]).read_bytes()
    if len(encoded) != entry["artifact_bytes"]:
        raise ValueError("consequence source artifact byte count changed")
    if _digest(encoded) != entry["artifact_sha256"]:
        raise ValueError("consequence source artifact digest changed")
    source = json.loads(encoded)
    if source["known_loss"] is not None:
        raise ValueError("consequence source artifact carries known loss")

    square_count = 0
    asymmetry_by_side = {
        side: Counter() for side in ("left", "right", "joint")
    }
    extent_histogram: Counter[int] = Counter()
    asymmetric_extent_histogram: Counter[int] = Counter()
    asymmetric_square_references = []
    surfaces_with_asymmetry = set()
    frames_with_asymmetry = 0

    records = source["context_population_records"]
    for finding_number, finding in enumerate(source["findings"]):
        context_indexes = finding["production_context_population_indexes"]
        context_references = {
            "left": [
                "" if index is None else records[index][3]
                for index in context_indexes
            ],
            "right": [
                "" if index is None else records[index][4]
                for index in context_indexes
            ],
            "joint": [
                "" if index is None else records[index][5]
                for index in context_indexes
            ],
        }
        for pair_number, pair_finding in enumerate(
            finding["coordinate_pair_findings"]
        ):
            for frame_number, frame in enumerate(
                pair_finding["source_carried_joint_frames"]
            ):
                production_by_cell = {
                    (first_material, second_material): production
                    for first_material, second_material, production in frame[
                        "cell_population"
                    ]
                }
                second_by_first: dict[int, set[int]] = defaultdict(set)
                for first_material, second_material in production_by_cell:
                    second_by_first[first_material].add(second_material)
                frame_square_count = 0
                frame_has_asymmetry = False
                for first_material, other_first_material in frame[
                    "qualified_first_coordinate_material_pairs"
                ]:
                    common_second = sorted(
                        second_by_first[first_material]
                        & second_by_first[other_first_material]
                    )
                    for second_offset, second_material in enumerate(common_second):
                        for other_second_material in common_second[
                            second_offset + 1 :
                        ]:
                            productions = (
                                production_by_cell[
                                    (first_material, second_material)
                                ],
                                production_by_cell[
                                    (first_material, other_second_material)
                                ],
                                production_by_cell[
                                    (other_first_material, second_material)
                                ],
                                production_by_cell[
                                    (other_first_material, other_second_material)
                                ],
                            )
                            frame_square_count += 1
                            square_count += 1
                            extent_histogram[finding["coordinate_count"]] += 1
                            square_effects = {}
                            square_has_asymmetry = False
                            for side in ("left", "right", "joint"):
                                first_changes, second_changes = _effect_counts(
                                    context_references[side], productions
                                )
                                asymmetry_by_side[side][
                                    f"{first_changes}:{second_changes}"
                                ] += 1
                                square_effects[side] = [
                                    first_changes,
                                    second_changes,
                                ]
                                square_has_asymmetry |= (
                                    first_changes != second_changes
                                )
                            if not square_has_asymmetry:
                                continue
                            frame_has_asymmetry = True
                            surfaces_with_asymmetry.add(finding_number)
                            asymmetric_extent_histogram[
                                finding["coordinate_count"]
                            ] += 1
                            if len(asymmetric_square_references) < sample_boundary:
                                asymmetric_square_references.append(
                                    {
                                        "internal_variation_finding_reference": finding[
                                            "internal_variation_finding_reference"
                                        ],
                                        "coordinate_count": finding[
                                            "coordinate_count"
                                        ],
                                        "coordinate_classes": [
                                            pair_finding[
                                                "first_coordinate_class_number"
                                            ],
                                            pair_finding[
                                                "second_coordinate_class_number"
                                            ],
                                        ],
                                        "fixed_coordinate_material_indexes": frame[
                                            "fixed_coordinate_material_indexes"
                                        ],
                                        "first_coordinate_material_indexes": [
                                            first_material,
                                            other_first_material,
                                        ],
                                        "second_coordinate_material_indexes": [
                                            second_material,
                                            other_second_material,
                                        ],
                                        "production_indexes": list(productions),
                                        "immediate_consequence_change_counts": (
                                            square_effects
                                        ),
                                        "source_frame_address": [
                                            finding_number,
                                            pair_number,
                                            frame_number,
                                        ],
                                    }
                                )
                if frame_square_count != frame["complete_substitution_square_count"]:
                    raise AssertionError(
                        "frame graph does not reconstruct its exact square count"
                    )
                frames_with_asymmetry += int(frame_has_asymmetry)
    if square_count != source["complete_substitution_square_count"]:
        raise AssertionError(
            "source frame graphs do not reconstruct the exact square population"
        )
    return {
        "source": source["source"],
        "consequence_source_artifact_sha256": entry["artifact_sha256"],
        "joint_surface_finding_count": source["joint_surface_finding_count"],
        "joint_frame_count": source["joint_frame_count"],
        "complete_substitution_square_count": square_count,
        "surfaces_with_immediate_consequence_asymmetry": len(
            surfaces_with_asymmetry
        ),
        "frames_with_immediate_consequence_asymmetry": frames_with_asymmetry,
        "effect_count_by_side": {
            side: dict(sorted(population.items()))
            for side, population in asymmetry_by_side.items()
        },
        "square_count_by_extent": {
            str(extent): count for extent, count in sorted(extent_histogram.items())
        },
        "asymmetric_square_count_by_extent": {
            str(extent): count
            for extent, count in sorted(asymmetric_extent_histogram.items())
        },
        "first_source_order_asymmetric_square_addresses": (
            asymmetric_square_references
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=INPUT)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--sample-boundary-per-source", type=int, default=8)
    parser.add_argument("--jobs", type=int, default=1)
    arguments = parser.parse_args()
    if arguments.jobs < 1:
        raise ValueError("jobs must be a positive exact process count")
    begun = time.perf_counter()
    encoded_input = arguments.input.read_bytes()
    manifest = json.loads(encoded_input)
    if manifest["known_loss"] is not None:
        raise ValueError("consequence manifest carries known loss")

    if arguments.jobs == 1:
        sources = [
            _observe_source(
                entry, sample_boundary=arguments.sample_boundary_per_source
            )
            for entry in manifest["source_artifacts"]
        ]
    else:
        with ProcessPoolExecutor(max_workers=arguments.jobs) as executor:
            sources = list(
                executor.map(
                    _observe_source,
                    manifest["source_artifacts"],
                    repeat(arguments.sample_boundary_per_source),
                )
            )
    aggregate_effects = {
        side: Counter() for side in ("left", "right", "joint")
    }
    extent_population: Counter[int] = Counter()
    asymmetric_extent_population: Counter[int] = Counter()
    for source in sources:
        for side, population in source["effect_count_by_side"].items():
            aggregate_effects[side].update(population)
        extent_population.update(
            {int(key): value for key, value in source["square_count_by_extent"].items()}
        )
        asymmetric_extent_population.update(
            {
                int(key): value
                for key, value in source[
                    "asymmetric_square_count_by_extent"
                ].items()
            }
        )
    finding = {
        "consequence_manifest_sha256": _digest(encoded_input),
        "operation": (
            "within every exact source-carried complete substitution square, "
            "compare the two controlled first-coordinate consequence changes "
            "with the two controlled second-coordinate consequence changes"
        ),
        "source_count": len(sources),
        "joint_surface_finding_count": sum(
            source["joint_surface_finding_count"] for source in sources
        ),
        "joint_frame_count": sum(
            source["joint_frame_count"] for source in sources
        ),
        "complete_substitution_square_count": sum(
            source["complete_substitution_square_count"] for source in sources
        ),
        "surfaces_with_immediate_consequence_asymmetry": sum(
            source["surfaces_with_immediate_consequence_asymmetry"]
            for source in sources
        ),
        "frames_with_immediate_consequence_asymmetry": sum(
            source["frames_with_immediate_consequence_asymmetry"]
            for source in sources
        ),
        "effect_count_by_side": {
            side: dict(sorted(population.items()))
            for side, population in aggregate_effects.items()
        },
        "square_count_by_extent": {
            str(extent): count for extent, count in sorted(extent_population.items())
        },
        "asymmetric_square_count_by_extent": {
            str(extent): count
            for extent, count in sorted(asymmetric_extent_population.items())
        },
        "sources": sources,
        "known_loss": None,
    }
    encoded = _canonical(finding)
    arguments.output.write_bytes(encoded)
    print(f"artifact: {arguments.output}")
    print(f"artifact bytes: {len(encoded)}")
    print(f"findings sha256: {_digest(encoded)}")
    print(f"wall seconds: {time.perf_counter() - begun:.3f}")
    print("known loss: None")
    print(
        "population: "
        f"surfaces={finding['joint_surface_finding_count']} "
        f"frames={finding['joint_frame_count']} "
        f"squares={finding['complete_substitution_square_count']} "
        f"asymmetric_surfaces={finding['surfaces_with_immediate_consequence_asymmetry']} "
        f"asymmetric_frames={finding['frames_with_immediate_consequence_asymmetry']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
