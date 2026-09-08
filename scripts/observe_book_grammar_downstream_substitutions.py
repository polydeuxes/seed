"""Observe source-bounded substitutions through later recurrent structure.

The discovery road treats the active Book and Fidelity grammar as raw bytes.
It does not parse JSON, use grammar names as targets, or record Seed events.
Each source remains independently bounded, and the optional positional argument
selects ``book`` or ``grammar`` so either leg can retain a separate time bound.
Artifacts are observer evidence written beneath ``/tmp``.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from hashlib import sha256
import heapq
import json
from pathlib import Path
import sys
import time


ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / "book_of_seed"
SOURCES = (
    *((path, "book") for path in (BOOK / "README.md", *sorted((BOOK / "chapters").glob("*.md")))),
    (BOOK / "witness_grammar.json", "grammar"),
)
OUTPUT = Path("/tmp/seed_book_grammar_joint_downstream_blind.json")
SAMPLE_COUNT = 48


def digest(value: object) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return sha256(encoded).hexdigest()


def surface_digest(surface: tuple[int, ...]) -> str:
    return sha256(",".join(map(str, surface)).encode()).hexdigest()


def render(material: bytes) -> str:
    return repr(material)[2:-1]


def split_coordinate_sets(length: int, first_difference: int, last_difference: int):
    role_zero = tuple(
        (first_split, second_split)
        for first_split in range(last_difference + 1, length - 1)
        for second_split in range(first_split + 1, length)
    )
    role_one = tuple(
        (first_split, second_split)
        for first_split in range(1, first_difference + 1)
        for second_split in range(last_difference + 1, length)
    )
    role_two = tuple(
        (first_split, second_split)
        for second_split in range(2, first_difference + 1)
        for first_split in range(1, second_split)
    )
    return role_zero, role_one, role_two


def consequence_trace(
    starts: tuple[int, ...],
    coordinate_count: int,
    states: dict[int, dict[int, tuple[int, ...]]],
) -> tuple[dict, ...]:
    found = []
    current_count = coordinate_count
    while True:
        current = states.get(current_count)
        if current is None:
            break
        grouped_starts = defaultdict(list)
        for start in starts:
            if start in current:
                grouped_starts[current[start]].append(start)
        recurrent = tuple(
            sorted(
                (
                    surface_digest(surface),
                    len(found_starts),
                )
                for surface, found_starts in grouped_starts.items()
                if len(found_starts) > 1
            )
        )
        if not recurrent:
            break
        found.append(
            {
                "coordinate_count": current_count,
                "recurrent_structural_results": recurrent,
                "recurrent_structural_result_count": len(recurrent),
                "support_occurrence_count": sum(count for _surface, count in recurrent),
            }
        )
        current_count += 1
    return tuple(found)


def equal_prefix(first: tuple, second: tuple, *, with_counts: bool) -> int:
    depth = 0
    for first_step, second_step in zip(first, second):
        first_results = first_step["recurrent_structural_results"]
        second_results = second_step["recurrent_structural_results"]
        if not with_counts:
            first_results = tuple(surface for surface, _count in first_results)
            second_results = tuple(surface for surface, _count in second_results)
        if first_results != second_results:
            break
        depth += 1
    return depth


def observe_source(path: Path, population: str) -> dict:
    begun = time.perf_counter()
    data = path.read_bytes()
    relative = path.relative_to(ROOT).as_posix()
    active = {
        start: (-1, 0 if data[start] == data[start + 1] else -1)
        for start in range(len(data) - 1)
    }
    states: dict[int, dict[int, tuple[int, ...]]] = {}
    groups: dict[int, tuple[tuple[tuple[int, ...], tuple[int, ...]], ...]] = {}
    coordinate_count = 2
    while active:
        grouped = defaultdict(list)
        for start, surface in active.items():
            grouped[surface].append(start)
        recurrent = {
            surface: tuple(starts)
            for surface, starts in grouped.items()
            if len(starts) > 1
        }
        recurrent_starts = tuple(
            start for starts in recurrent.values() for start in starts
        )
        states[coordinate_count] = {
            start: active[start] for start in recurrent_starts
        }
        groups[coordinate_count] = tuple(recurrent.items())
        next_active = {}
        for start in recurrent_starts:
            next_position = start + coordinate_count
            if next_position >= len(data):
                continue
            byte = data[next_position]
            prior = data.rfind(bytes((byte,)), start, next_position)
            next_active[start] = active[start] + (
                prior - start if prior >= start else -1,
            )
        active = next_active
        coordinate_count += 1

    trace_cache = {}
    exact_split_coordinates = set()
    edge_count = 0
    production_pair_count = 0
    both_alive_histogram = Counter()
    same_surface_histogram = Counter()
    same_exact_histogram = Counter()
    same_complete_histogram = Counter()
    varied_role_histogram = Counter()
    coordinate_count_histogram = Counter()
    pressure = defaultdict(
        lambda: {
            "edge_count": 0,
            "maximum_both_alive_rungs": 0,
            "maximum_same_surface_rungs": 0,
            "sources": set(),
        }
    )
    samples = []
    same_surface_samples = []

    for length, recurrent_groups in groups.items():
        if length < 3:
            continue
        for group_position, (surface, starts) in enumerate(recurrent_groups):
            material_starts = defaultdict(list)
            for start in starts:
                material_starts[data[start : start + length]].append(start)
            recurrent_material = {
                material: tuple(found)
                for material, found in material_starts.items()
                if len(found) > 1
            }
            materials = tuple(sorted(recurrent_material))
            if len(materials) < 2:
                continue
            group_reference = digest(
                {
                    "source": relative,
                    "coordinate_count": length,
                    "surface": surface,
                    "support_positions": starts,
                }
            )
            for first_position, first_material in enumerate(materials):
                for second_material in materials[first_position + 1 :]:
                    differences = tuple(
                        position
                        for position, (first_byte, second_byte) in enumerate(
                            zip(first_material, second_material)
                        )
                        if first_byte != second_byte
                    )
                    if not differences:
                        continue
                    split_sets = split_coordinate_sets(
                        length, differences[0], differences[-1]
                    )
                    addressed_edge_count = sum(len(found) for found in split_sets)
                    if not addressed_edge_count:
                        continue
                    production_pair_count += 1
                    edge_count += addressed_edge_count
                    first_starts = recurrent_material[first_material]
                    second_starts = recurrent_material[second_material]
                    first_key = (length, first_starts)
                    second_key = (length, second_starts)
                    first_trace = trace_cache.get(first_key)
                    if first_trace is None:
                        first_trace = consequence_trace(
                            first_starts, length, states
                        )
                        trace_cache[first_key] = first_trace
                    second_trace = trace_cache.get(second_key)
                    if second_trace is None:
                        second_trace = consequence_trace(
                            second_starts, length, states
                        )
                        trace_cache[second_key] = second_trace
                    both_alive = min(len(first_trace), len(second_trace))
                    same_surface = equal_prefix(
                        first_trace, second_trace, with_counts=False
                    )
                    same_exact = equal_prefix(first_trace, second_trace, with_counts=True)
                    # These are distinct exact materials. At their first
                    # recurrent bound, corresponding-coordinate Measurement
                    # records each literal byte under its exact role. At least
                    # one such literal result differs by construction.
                    same_complete = 0
                    both_alive_histogram[both_alive] += addressed_edge_count
                    same_surface_histogram[same_surface] += addressed_edge_count
                    same_exact_histogram[same_exact] += addressed_edge_count
                    same_complete_histogram[same_complete] += addressed_edge_count
                    coordinate_count_histogram[length] += addressed_edge_count

                    for role, split_coordinates in enumerate(split_sets):
                        if not split_coordinates:
                            continue
                        varied_role_histogram[role] += len(split_coordinates)
                        for first_split, second_split in split_coordinates:
                            exact_split_coordinates.add(
                                (length, group_position, first_split, second_split)
                            )
                            bounds = (0, first_split, second_split, length)
                            first_value = first_material[bounds[role] : bounds[role + 1]]
                            second_value = second_material[bounds[role] : bounds[role + 1]]
                            for value in (first_value, second_value):
                                item = pressure[value]
                                item["edge_count"] += 1
                                item["maximum_both_alive_rungs"] = max(
                                    item["maximum_both_alive_rungs"], both_alive
                                )
                                item["maximum_same_surface_rungs"] = max(
                                    item["maximum_same_surface_rungs"], same_surface
                                )
                                item["sources"].add(relative)

                    representative = next(
                        (
                            (role, split_coordinates[0])
                            for role, split_coordinates in enumerate(split_sets)
                            if split_coordinates
                        ),
                        None,
                    )
                    if representative is not None:
                        role, (first_split, second_split) = representative
                        bounds = (0, first_split, second_split, length)
                        sample = {
                            "source": relative,
                            "group_reference": group_reference,
                            "coordinate_count": length,
                            "split_roles": [first_split, second_split],
                            "varied_role": role,
                            "first_role_material": [
                                render(first_material[bounds[index] : bounds[index + 1]])
                                for index in range(3)
                            ],
                            "second_role_material": [
                                render(second_material[bounds[index] : bounds[index + 1]])
                                for index in range(3)
                            ],
                            "first_support_count": len(first_starts),
                            "second_support_count": len(second_starts),
                            "addressed_split_edge_count": addressed_edge_count,
                            "both_alive_rungs": both_alive,
                            "same_surface_rungs": same_surface,
                            "same_exact_rungs": same_exact,
                            "same_complete_rungs": same_complete,
                            "complete_result_divergence": (
                                "the first corresponding-coordinate material "
                                "result differs at a substituted coordinate"
                            ),
                            "first_trace": first_trace,
                            "second_trace": second_trace,
                        }
                        key = (
                            both_alive,
                            same_surface,
                            same_exact,
                            same_complete,
                            length,
                            addressed_edge_count,
                            digest(sample),
                        )
                        if len(samples) < SAMPLE_COUNT:
                            heapq.heappush(samples, (key, sample))
                        elif key > samples[0][0]:
                            heapq.heapreplace(samples, (key, sample))
                        same_key = (
                            same_surface,
                            same_exact,
                            same_complete,
                            both_alive,
                            length,
                            addressed_edge_count,
                            digest(sample),
                        )
                        if len(same_surface_samples) < SAMPLE_COUNT:
                            heapq.heappush(same_surface_samples, (same_key, sample))
                        elif same_key > same_surface_samples[0][0]:
                            heapq.heapreplace(same_surface_samples, (same_key, sample))

    pressure_results = sorted(
        (
            {
                "material": render(material),
                "coordinate_count": len(material),
                "edge_count": item["edge_count"],
                "maximum_both_alive_rungs": item["maximum_both_alive_rungs"],
                "maximum_same_surface_rungs": item["maximum_same_surface_rungs"],
                "source_count": len(item["sources"]),
            }
            for material, item in pressure.items()
        ),
        key=lambda item: (
            -item["maximum_both_alive_rungs"],
            -item["maximum_same_surface_rungs"],
            -item["coordinate_count"],
            -item["edge_count"],
            item["material"],
        ),
    )
    elapsed = time.perf_counter() - begun
    print(
        f"{population} {relative}: split_surfaces={len(exact_split_coordinates)} "
        f"production_pairs={production_pair_count} edges={edge_count} "
        f"max_alive={max(both_alive_histogram, default=0)} "
        f"max_same={max(same_surface_histogram, default=0)} "
        f"elapsed={elapsed:.3f}s",
        flush=True,
    )
    return {
        "source": relative,
        "population": population,
        "source_digest": sha256(data).hexdigest(),
        "byte_count": len(data),
        "addressed_split_surface_count": len(exact_split_coordinates),
        "recurrent_production_pair_count": production_pair_count,
        "addressed_substitution_edge_count": edge_count,
        "varied_role_histogram": dict(sorted(varied_role_histogram.items())),
        "coordinate_count_histogram": dict(sorted(coordinate_count_histogram.items())),
        "both_alive_rung_histogram": dict(sorted(both_alive_histogram.items())),
        "same_surface_rung_histogram": dict(sorted(same_surface_histogram.items())),
        "same_exact_rung_histogram": dict(sorted(same_exact_histogram.items())),
        "same_complete_rung_histogram": dict(
            sorted(same_complete_histogram.items())
        ),
        "pressure_material_population_count": len(pressure_results),
        "pressure_material": pressure_results,
        "strong_consequence_samples": [
            sample for _key, sample in sorted(samples, reverse=True)
        ],
        "same_surface_consequence_samples": [
            sample for _key, sample in sorted(same_surface_samples, reverse=True)
        ],
        "elapsed_seconds": round(elapsed, 6),
    }


def main():
    begun = time.perf_counter()
    selected_sources = SOURCES
    suffix = ""
    if len(sys.argv) == 2:
        selected_population = sys.argv[1]
        if selected_population not in {"book", "grammar"}:
            raise SystemExit(
                "usage: observe_book_grammar_downstream_substitutions.py "
                "[book|grammar]"
            )
        selected_sources = tuple(
            (path, population)
            for path, population in SOURCES
            if population == selected_population
        )
        suffix = f"_{selected_population}"
    sources = [
        observe_source(path, population) for path, population in selected_sources
    ]
    result = {
        "observer": "blind recurrent occupant substitution with downstream recurrence continuation",
        "current_standing_treatment": (
            "yielded results remain carried; no current Standing completion is inferred"
        ),
        "sources": sources,
        "elapsed_seconds": round(time.perf_counter() - begun, 6),
    }
    structural_result = {
        key: value
        for key, value in result.items()
        if key != "elapsed_seconds"
    }
    structural_result["sources"] = [
        {
            key: value
            for key, value in source.items()
            if key != "elapsed_seconds"
        }
        for source in sources
    ]
    emitted_structural_result = json.loads(json.dumps(structural_result))
    result["structural_output_digest"] = digest(emitted_structural_result)
    output = OUTPUT.with_name(OUTPUT.stem + suffix + OUTPUT.suffix)
    output.write_text(json.dumps(result, indent=2), encoding="utf-8")
    artifact_file_digest = sha256(output.read_bytes()).hexdigest()
    print(
        f"FROZEN {output} bytes={output.stat().st_size} "
        f"structural_digest={result['structural_output_digest']} "
        f"file_digest={artifact_file_digest} "
        f"elapsed={result['elapsed_seconds']:.3f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
