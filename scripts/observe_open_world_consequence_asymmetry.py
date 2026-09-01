"""Measure the first outward consequence of source-carried joint variation.

The observer reads the frozen internal-variation source shards and the exact
source windows they address.  It does not ask for a coordinate count, word,
role, organizer, head, root, or direction.

Two separately varying coordinate classes become comparable only where the
source carries a complete substitution square while every other coordinate
class remains exact::

    x0 y0    x0 y1
    x1 y0    x1 y1

Every cell is one recurrent complete production.  The first outward
consequence is the exact scalar immediately to the left and immediately to the
right of each cell occurrence.  Left, right, and joint populations remain
separate.  The observer records whether their exact material populations are
the same or different under each source-carried substitution; it does not turn
a difference into direction or pre-classify a later relation among unequal
populations.

Usage:
    .venv/bin/python scripts/observe_open_world_consequence_asymmetry.py \
        --jobs 14
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from concurrent.futures import ProcessPoolExecutor
from hashlib import sha256
import json
from pathlib import Path
import time

try:
    import numpy as np
except ModuleNotFoundError:  # Focused checks use only dependency-free operations.
    np = None

from observe_open_world_apertures import CORPUS, _window


INPUT = Path("/tmp/seed_open_world_internal_variation_manifest.json")
OUTPUT = Path("/tmp/seed_open_world_consequence_asymmetry_manifest.json")
SOURCE_OUTPUT_DIRECTORY = Path(
    "/tmp/seed_open_world_consequence_asymmetry_sources"
)
OPERATION = (
    "source-carried complete two-coordinate substitution squares followed by "
    "exact immediate left, right, and joint outer-context material-population "
    "same/different findings"
)


def _canonical(value: object) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode()


def _digest(value: object) -> str:
    material = value if isinstance(value, bytes) else _canonical(value)
    return sha256(material).hexdigest()


def _population_mask(values: set, indexes: dict[object, int]) -> int:
    mask = 0
    for value in values:
        index = indexes.get(value)
        if index is None:
            index = len(indexes)
            indexes[value] = index
        mask |= 1 << index
    return mask


def _identity_index(value: object, indexes: dict[object, int]) -> int:
    found = indexes.get(value)
    if found is not None:
        return found
    found = len(indexes)
    indexes[value] = found
    return found


def _source_carried_joint_frames(
    production_values: tuple[tuple[int, ...], ...],
    first_class: int,
    second_class: int,
) -> tuple[dict, ...]:
    """Return exact fixed-remainder frames containing at least one 2x2 square.

    The bipartite cell population is the lossless representation.  Every 2x2
    square remains exactly addressable from it without eagerly instantiating
    all combinations of node pairs.
    """

    if first_class >= second_class:
        raise ValueError("coordinate classes must be in source-class order")
    cells_by_fixed_values: dict[tuple[int, ...], list[tuple[int, int, int]]] = (
        defaultdict(list)
    )
    for production_index, values in enumerate(production_values):
        fixed_values = (
            values[:first_class]
            + values[first_class + 1 : second_class]
            + values[second_class + 1 :]
        )
        cells_by_fixed_values[fixed_values].append(
            (values[first_class], values[second_class], production_index)
        )

    frames = []
    for fixed_values, cells in sorted(cells_by_fixed_values.items()):
        production_by_cell = {
            (first_material, second_material): production_index
            for first_material, second_material, production_index in cells
        }
        if len(production_by_cell) != len(cells):
            raise AssertionError("one complete production occupies one exact cell")
        second_by_first: dict[int, set[int]] = defaultdict(set)
        first_by_second: dict[int, set[int]] = defaultdict(set)
        for first_material, second_material in production_by_cell:
            second_by_first[first_material].add(second_material)
            first_by_second[second_material].add(first_material)
        if len(production_by_cell) < 4:
            continue
        eligible_first_materials = sorted(
            material
            for material, neighbors in second_by_first.items()
            if len(neighbors) >= 2
        )
        eligible_second_material_count = sum(
            len(neighbors) >= 2 for neighbors in first_by_second.values()
        )
        if len(eligible_first_materials) < 2 or eligible_second_material_count < 2:
            continue

        participating_cells = set()
        qualified_first_pairs = set()
        rectangle_count = 0
        first_materials = eligible_first_materials
        for first_offset, first_material in enumerate(first_materials):
            for other_first_material in first_materials[first_offset + 1 :]:
                common_second = (
                    second_by_first[first_material]
                    & second_by_first[other_first_material]
                )
                count = len(common_second)
                rectangle_count += count * (count - 1) // 2
                if count < 2:
                    continue
                qualified_first_pairs.add(
                    (first_material, other_first_material)
                )
                for second_material in common_second:
                    participating_cells.add((first_material, second_material))
                    participating_cells.add(
                        (other_first_material, second_material)
                    )
        if not rectangle_count:
            continue

        qualified_second_pairs = set()
        second_materials = sorted(first_by_second)
        for second_offset, second_material in enumerate(second_materials):
            for other_second_material in second_materials[second_offset + 1 :]:
                if len(
                    first_by_second[second_material]
                    & first_by_second[other_second_material]
                ) >= 2:
                    qualified_second_pairs.add(
                        (second_material, other_second_material)
                    )
        frames.append(
            {
                "fixed_coordinate_material_indexes": list(fixed_values),
                "cell_population": [
                    {
                        "first_coordinate_material_index": first_material,
                        "second_coordinate_material_index": second_material,
                        "production_index": production_by_cell[
                            (first_material, second_material)
                        ],
                    }
                    for first_material, second_material in sorted(production_by_cell)
                    if (first_material, second_material) in participating_cells
                ],
                "complete_substitution_square_count": rectangle_count,
                "_qualified_first_material_pairs": qualified_first_pairs,
                "_qualified_second_material_pairs": qualified_second_pairs,
            }
        )
    return tuple(frames)


def _immediate_outer_context_population(
    text: str,
    *,
    coordinate_count: int,
    starts: tuple[int, ...],
) -> dict:
    left: Counter[str] = Counter()
    right: Counter[str] = Counter()
    joint: Counter[tuple[str, str]] = Counter()
    for start in starts:
        end = start + coordinate_count
        left_value = text[start - 1 : start] if start else "<SOURCE_BOUNDARY>"
        right_value = (
            text[end : end + 1] if end < len(text) else "<SOURCE_BOUNDARY>"
        )
        left[left_value] += 1
        right[right_value] += 1
        joint[(left_value, right_value)] += 1

    def records(population: dict) -> list[dict]:
        return [
            {
                "context_material_utf8_hex": (
                    [item.encode("utf-8").hex() for item in value]
                    if isinstance(value, tuple)
                    else value.encode("utf-8").hex()
                ),
                "source_occurrence_count": occurrence_count,
            }
            for value, occurrence_count in sorted(population.items())
        ]

    return {
        "left": records(left),
        "right": records(right),
        "joint": records(joint),
        "_left_values": set(left),
        "_right_values": set(right),
        "_joint_values": set(joint),
    }


def _frame_substitution_edge_coordinates(
    frame: dict,
) -> tuple[list[tuple[int, int, int]], list[tuple[int, int, int]]]:
    production_by_cell = {
        (
            cell["first_coordinate_material_index"],
            cell["second_coordinate_material_index"],
        ): cell["production_index"]
        for cell in frame["cell_population"]
    }
    second_by_first: dict[int, set[int]] = defaultdict(set)
    first_by_second: dict[int, set[int]] = defaultdict(set)
    for first_material, second_material in production_by_cell:
        second_by_first[first_material].add(second_material)
        first_by_second[second_material].add(first_material)

    first_edges = []
    for second_material, first_materials in sorted(first_by_second.items()):
        ordered = sorted(first_materials)
        for offset, first_material in enumerate(ordered):
            for other_first_material in ordered[offset + 1 :]:
                # An edge participates only where a second control value makes
                # a complete source-carried square possible.
                if (
                    first_material,
                    other_first_material,
                ) not in frame["_qualified_first_material_pairs"]:
                    continue
                first_edges.append(
                    (
                        second_material,
                        production_by_cell[(first_material, second_material)],
                        production_by_cell[
                            (other_first_material, second_material)
                        ],
                    )
                )

    second_edges = []
    for first_material, second_materials in sorted(second_by_first.items()):
        ordered = sorted(second_materials)
        for offset, second_material in enumerate(ordered):
            for other_second_material in ordered[offset + 1 :]:
                if (
                    second_material,
                    other_second_material,
                ) not in frame["_qualified_second_material_pairs"]:
                    continue
                second_edges.append(
                    (
                        first_material,
                        production_by_cell[(first_material, second_material)],
                        production_by_cell[
                            (first_material, other_second_material)
                        ],
                    )
                )
    return first_edges, second_edges


def _compact_context_population(population: dict) -> list[list]:
    return [
        [record["context_material_utf8_hex"], record["source_occurrence_count"]]
        for record in population
    ]


def _same_different_counts(histogram: Counter) -> list[int]:
    return [histogram.get("same", 0), histogram.get("different", 0)]


def _observe_source(
    entry: dict,
    output_directory: str,
    profile_slow_findings: bool = False,
) -> dict:
    if np is None:
        raise RuntimeError("this disposable observer requires numpy")
    begun = time.perf_counter()
    encoded_input = Path(entry["artifact"]).read_bytes()
    if len(encoded_input) != entry["artifact_bytes"]:
        raise ValueError("internal-variation shard byte count changed")
    if _digest(encoded_input) != entry["artifact_sha256"]:
        raise ValueError("internal-variation shard digest changed")
    frozen = json.loads(encoded_input)
    source = frozen["source"]
    exact_bytes, _line_starts = _window(
        CORPUS.parent / source["source"], source["first_line"]
    )
    if _digest(exact_bytes) != source["material_sha256"]:
        raise ValueError("consequence source differs from frozen source")
    text = exact_bytes.decode("utf-8")

    findings = []
    joint_frame_count = 0
    substitution_square_count = 0
    first_edge_count = 0
    second_edge_count = 0
    consequence_relation_histogram: Counter[str] = Counter()
    left_context_indexes: dict[object, int] = {}
    right_context_indexes: dict[object, int] = {}
    joint_context_indexes: dict[object, int] = {}
    left_population_indexes: dict[object, int] = {}
    right_population_indexes: dict[object, int] = {}
    joint_population_indexes: dict[object, int] = {}
    context_population_records = []
    context_population_record_indexes: dict[bytes, int] = {}
    for finding in source["varying_surface_findings"]:
        finding_begun = time.perf_counter()
        first_edge_count_before = first_edge_count
        second_edge_count_before = second_edge_count
        varying_classes = tuple(
            position["coordinate_class_number"]
            for position in finding["variation_positions"]
        )
        if len(varying_classes) < 2:
            continue
        production_values = tuple(
            tuple(production["coordinate_material_indexes"])
            for production in finding["recurrent_exact_productions"]
        )
        frame_begun = time.perf_counter()
        pair_frame_population = []
        participating_production_indexes = set()
        for first_offset, first_class in enumerate(varying_classes):
            for second_class in varying_classes[first_offset + 1 :]:
                frames = _source_carried_joint_frames(
                    production_values, first_class, second_class
                )
                if not frames:
                    continue
                pair_frame_population.append((first_class, second_class, frames))
                for frame in frames:
                    participating_production_indexes.update(
                        cell["production_index"]
                        for cell in frame["cell_population"]
                    )
        frame_elapsed = time.perf_counter() - frame_begun
        if not pair_frame_population:
            if profile_slow_findings and frame_elapsed >= 1:
                print(
                    f"  {source['source']} extent={finding['coordinate_count']} "
                    f"frames={frame_elapsed:.3f}s empty",
                    flush=True,
                )
            continue

        starts = tuple(finding["source_scalar_starts"])
        context_populations: list[dict | None] = [
            None for _production in finding["recurrent_exact_productions"]
        ]
        context_begun = time.perf_counter()
        for production_index in sorted(participating_production_indexes):
            production = finding["recurrent_exact_productions"][production_index]
            production_starts = tuple(
                starts[index] for index in production["support_start_indexes"]
            )
            population = _immediate_outer_context_population(
                    text,
                    coordinate_count=finding["coordinate_count"],
                    starts=production_starts,
                )
            population["_left_mask"] = _population_mask(
                population["_left_values"], left_context_indexes
            )
            population["_right_mask"] = _population_mask(
                population["_right_values"], right_context_indexes
            )
            population["_joint_mask"] = _population_mask(
                population["_joint_values"], joint_context_indexes
            )
            for side, indexes in (
                ("left", left_population_indexes),
                ("right", right_population_indexes),
                ("joint", joint_population_indexes),
            ):
                population[f"_{side}_identity"] = _identity_index(
                    population[f"_{side}_mask"], indexes
                )
            context_populations[production_index] = population
        context_populations_tuple = tuple(context_populations)
        context_identity_arrays = {
            side: np.asarray(
                [
                    -1 if population is None else population[f"_{side}_identity"]
                    for population in context_populations
                ],
                dtype=np.int64,
            )
            for side in ("left", "right", "joint")
        }
        context_elapsed = time.perf_counter() - context_begun

        pair_findings = []
        pair_begun = time.perf_counter()
        for first_class, second_class, frames in pair_frame_population:
            frame_findings = []
            for frame in frames:
                    first_edges, second_edges = (
                        _frame_substitution_edge_coordinates(frame)
                    )
                    joint_frame_count += 1
                    substitution_square_count += frame[
                        "complete_substitution_square_count"
                    ]
                    first_edge_count += len(first_edges)
                    second_edge_count += len(second_edges)
                    first_histograms = {
                        "left_consequence": Counter(),
                        "right_consequence": Counter(),
                        "joint_consequence": Counter(),
                    }
                    second_histograms = {
                        "left_consequence": Counter(),
                        "right_consequence": Counter(),
                        "joint_consequence": Counter(),
                    }
                    for edge_population, histograms in (
                        (first_edges, first_histograms),
                        (second_edges, second_histograms),
                    ):
                        edge_array = np.asarray(edge_population, dtype=np.int64)
                        first_productions = edge_array[:, 1]
                        second_productions = edge_array[:, 2]
                        for side in ("left", "right", "joint"):
                            identities = context_identity_arrays[side]
                            if np.any(identities[first_productions] < 0) or np.any(
                                identities[second_productions] < 0
                            ):
                                raise AssertionError(
                                    "substitution edge addresses an unmeasured production"
                                )
                            same_count = int(
                                np.count_nonzero(
                                    identities[first_productions]
                                    == identities[second_productions]
                                )
                            )
                            different_count = len(edge_population) - same_count
                            if same_count:
                                histograms[f"{side}_consequence"]["same"] = (
                                    same_count
                                )
                                consequence_relation_histogram[
                                    f"{side}:same"
                                ] += same_count
                            if different_count:
                                histograms[f"{side}_consequence"]["different"] = (
                                    different_count
                                )
                                consequence_relation_histogram[
                                    f"{side}:different"
                                ] += different_count
                    frame_findings.append(
                        {
                            "fixed_coordinate_material_indexes": frame[
                                "fixed_coordinate_material_indexes"
                            ],
                            "cell_population": [
                                [
                                    cell["first_coordinate_material_index"],
                                    cell["second_coordinate_material_index"],
                                    cell["production_index"],
                                ]
                                for cell in frame["cell_population"]
                            ],
                            "complete_substitution_square_count": frame[
                                "complete_substitution_square_count"
                            ],
                            "qualified_first_coordinate_material_pairs": [
                                list(pair)
                                for pair in sorted(
                                    frame["_qualified_first_material_pairs"]
                                )
                            ],
                            "qualified_second_coordinate_material_pairs": [
                                list(pair)
                                for pair in sorted(
                                    frame["_qualified_second_material_pairs"]
                                )
                            ],
                            "first_coordinate_substitution_edge_count": len(
                                first_edges
                            ),
                            "second_coordinate_substitution_edge_count": len(
                                second_edges
                            ),
                            "first_coordinate_consequence_relations": {
                                side: _same_different_counts(histogram)
                                for side, histogram in first_histograms.items()
                            },
                            "second_coordinate_consequence_relations": {
                                side: _same_different_counts(histogram)
                                for side, histogram in second_histograms.items()
                            },
                        }
                    )
            pair_findings.append(
                {
                    "first_coordinate_class_number": first_class,
                    "second_coordinate_class_number": second_class,
                    "source_carried_joint_frames": frame_findings,
                }
            )
        production_context_population_indexes = []
        for population in context_populations:
            if population is None:
                production_context_population_indexes.append(None)
                continue
            context_record = [
                _compact_context_population(population["left"]),
                _compact_context_population(population["right"]),
                _compact_context_population(population["joint"]),
                _digest(sorted(population["_left_values"])),
                _digest(sorted(population["_right_values"])),
                _digest(sorted(population["_joint_values"])),
            ]
            context_key = _canonical(context_record)
            context_index = context_population_record_indexes.get(context_key)
            if context_index is None:
                context_index = len(context_population_records)
                context_population_records.append(context_record)
                context_population_record_indexes[context_key] = context_index
            production_context_population_indexes.append(context_index)
        findings.append(
            {
                "internal_variation_finding_reference": finding[
                    "finding_reference"
                ],
                "coordinate_count": finding["coordinate_count"],
                "source_addressed_varying_position_count": len(varying_classes),
                "production_context_population_indexes": (
                    production_context_population_indexes
                ),
                "coordinate_pair_findings": pair_findings,
            }
        )
        if profile_slow_findings and time.perf_counter() - finding_begun >= 1:
            new_edge_count = (
                first_edge_count
                - first_edge_count_before
                + second_edge_count
                - second_edge_count_before
            )
            print(
                f"  {source['source']} extent={finding['coordinate_count']} "
                f"frames={frame_elapsed:.3f}s "
                f"contexts={context_elapsed:.3f}s "
                f"pairs={time.perf_counter() - pair_begun:.3f}s "
                f"edges={new_edge_count}",
                flush=True,
            )

    result = {
        "operation": OPERATION,
        "internal_variation_artifact_sha256": entry["artifact_sha256"],
        "source": source["source"],
        "first_line": source["first_line"],
        "line_count": source["line_count"],
        "material_sha256": source["material_sha256"],
        "joint_surface_finding_count": len(findings),
        "joint_frame_count": joint_frame_count,
        "complete_substitution_square_count": substitution_square_count,
        "first_coordinate_substitution_edge_count": first_edge_count,
        "second_coordinate_substitution_edge_count": second_edge_count,
        "consequence_relation_histogram": dict(
            sorted(consequence_relation_histogram.items())
        ),
        "substitution_edge_address": (
            "one qualified coordinate-material pair plus each exact fixed-other "
            "cell carried by the frame graph; its two production indexes address "
            "the exact context material populations compared by the finding"
        ),
        "cell_population_schema": [
            "first_coordinate_material_index",
            "second_coordinate_material_index",
            "production_index",
        ],
        "context_population_schema": [
            "context_material_utf8_hex",
            "source_occurrence_count",
        ],
        "context_population_record_schema": [
            "left_context_population",
            "right_context_population",
            "joint_context_population",
            "left_material_population_reference",
            "right_material_population_reference",
            "joint_material_population_reference",
        ],
        "context_population_records": context_population_records,
        "consequence_count_schema": ["same", "different"],
        "findings": findings,
        "known_loss": None,
    }
    encoded = _canonical(result)
    artifact_sha256 = _digest(encoded)
    source_reference = _digest(source["source"].encode())
    output = Path(output_directory) / f"{source_reference}-{artifact_sha256}.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(encoded)
    return {
        "source": source["source"],
        "first_line": source["first_line"],
        "line_count": source["line_count"],
        "material_sha256": source["material_sha256"],
        "artifact": str(output),
        "artifact_bytes": len(encoded),
        "artifact_sha256": artifact_sha256,
        "joint_surface_finding_count": len(findings),
        "joint_frame_count": joint_frame_count,
        "complete_substitution_square_count": substitution_square_count,
        "first_coordinate_substitution_edge_count": first_edge_count,
        "second_coordinate_substitution_edge_count": second_edge_count,
        "consequence_relation_histogram": dict(
            sorted(consequence_relation_histogram.items())
        ),
        "wall_seconds": time.perf_counter() - begun,
    }


def _reusable_source_artifact(entry: dict, output_directory: Path) -> dict | None:
    source_reference = _digest(entry["source"].encode())
    for candidate in sorted(
        output_directory.glob(f"{source_reference}-*.json"),
        key=lambda path: path.stat().st_mtime_ns,
        reverse=True,
    ):
        encoded = candidate.read_bytes()
        try:
            finding = json.loads(encoded)
        except (UnicodeDecodeError, json.JSONDecodeError):
            continue
        if (
            finding.get("operation") != OPERATION
            or finding.get("internal_variation_artifact_sha256")
            != entry["artifact_sha256"]
            or finding.get("source") != entry["source"]
            or finding.get("known_loss") is not None
            or finding.get("consequence_count_schema") != ["same", "different"]
            or "context_population_records" not in finding
        ):
            continue
        artifact_sha256 = _digest(encoded)
        if candidate.name != f"{source_reference}-{artifact_sha256}.json":
            continue
        return {
            "source": finding["source"],
            "first_line": finding["first_line"],
            "line_count": finding["line_count"],
            "material_sha256": finding["material_sha256"],
            "artifact": str(candidate),
            "artifact_bytes": len(encoded),
            "artifact_sha256": artifact_sha256,
            "joint_surface_finding_count": finding[
                "joint_surface_finding_count"
            ],
            "joint_frame_count": finding["joint_frame_count"],
            "complete_substitution_square_count": finding[
                "complete_substitution_square_count"
            ],
            "first_coordinate_substitution_edge_count": finding[
                "first_coordinate_substitution_edge_count"
            ],
            "second_coordinate_substitution_edge_count": finding[
                "second_coordinate_substitution_edge_count"
            ],
            "consequence_relation_histogram": finding[
                "consequence_relation_histogram"
            ],
            "wall_seconds": 0.0,
            "reused_complete_artifact": True,
        }
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=INPUT)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument(
        "--source-output-directory",
        type=Path,
        default=SOURCE_OUTPUT_DIRECTORY,
    )
    parser.add_argument("--source", action="append", default=[])
    parser.add_argument("--jobs", type=int, default=1)
    parser.add_argument("--profile-slow-findings", action="store_true")
    parser.add_argument("--no-reuse-complete-source-artifacts", action="store_true")
    arguments = parser.parse_args()
    if arguments.jobs < 1:
        raise ValueError("jobs must be a positive exact process count")

    begun = time.perf_counter()
    encoded_input = arguments.input.read_bytes()
    frozen = json.loads(encoded_input)
    if frozen["known_loss"] is not None:
        raise ValueError("internal-variation manifest carries known loss")
    selected = [
        entry
        for entry in frozen["source_artifacts"]
        if not arguments.source or entry["source"] in arguments.source
    ]
    execution = sorted(
        selected,
        key=lambda entry: (-entry["artifact_bytes"], entry["source"]),
    )
    by_source = {}
    pending_execution = []
    for entry in execution:
        reusable = None
        if not arguments.no_reuse_complete_source_artifacts:
            reusable = _reusable_source_artifact(
                entry, arguments.source_output_directory
            )
        if reusable is None:
            pending_execution.append(entry)
            continue
        by_source[entry["source"]] = reusable
        print(
            f"{entry['source']:48} reused complete {reusable['artifact_sha256'][:12]}",
            flush=True,
        )
    payloads = [
        (
            entry,
            str(arguments.source_output_directory),
            arguments.profile_slow_findings,
        )
        for entry in pending_execution
    ]
    if arguments.jobs == 1:
        observed = map(lambda payload: _observe_source(*payload), payloads)
        executor = None
    else:
        executor = ProcessPoolExecutor(max_workers=arguments.jobs)
        observed = executor.map(
            _observe_source,
            (payload[0] for payload in payloads),
            (payload[1] for payload in payloads),
            (payload[2] for payload in payloads),
        )
    try:
        for entry, result in zip(pending_execution, observed):
            by_source[entry["source"]] = result
            edge_count = (
                result["first_coordinate_substitution_edge_count"]
                + result["second_coordinate_substitution_edge_count"]
            )
            print(
                f"{entry['source']:48} "
                f"surfaces={result['joint_surface_finding_count']:5} "
                f"frames={result['joint_frame_count']:6} "
                f"squares={result['complete_substitution_square_count']:9} "
                f"edges={edge_count:8} "
                f"bytes={result['artifact_bytes']:10} "
                f"{result['wall_seconds']:.3f}s",
                flush=True,
            )
    finally:
        if executor is not None:
            executor.shutdown()

    sources = []
    for entry in selected:
        result = dict(by_source[entry["source"]])
        result.pop("wall_seconds")
        result.pop("reused_complete_artifact", None)
        sources.append(result)
    finding = {
        "internal_variation_manifest_sha256": _digest(encoded_input),
        "operation": OPERATION,
        "source_artifacts": sources,
        "known_loss": None,
    }
    encoded = _canonical(finding)
    arguments.output.write_bytes(encoded)
    print(f"\nartifact: {arguments.output}")
    print(f"artifact bytes: {len(encoded)}")
    print(f"findings sha256: {_digest(encoded)}")
    print(f"complete wall seconds: {time.perf_counter() - begun:.3f}")
    print("known loss: None")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
