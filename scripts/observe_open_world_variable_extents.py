"""Extend frozen scalar-frame occurrences only while exact recurrence survives.

This findings-only observer reads the frozen Unicode-scalar aperture artifact
and the exact source windows it addresses.  It reads no Book, machine grammar,
Rosetta material, dictionary, translation, expected word, or language category.

For each exact recurrent occupant population, its complete frame occurrence is
the initial extent.  Every surviving extent independently attempts one-scalar
left and right extensions.  An enlarged exact surface survives only when at
least two source occurrences carry it.  Branches may split; source occurrence
identities are never merged or manufactured.

When one exact support population shares L further scalars on the left and R
further scalars on the right, every rectangle in that L x R coordinate space
is addressable without being a separately discovered branch.  The observer
therefore records one exact extent family carrying the complete ranges and its
maximal surface.  It branches only where another scalar changes the support
population.  This preserves the finite coordinate space without materializing
every mechanically constructible left/right rectangle.

Usage:
    .venv/bin/python scripts/observe_open_world_variable_extents.py
"""

from __future__ import annotations

import argparse
from collections import defaultdict, deque
from hashlib import sha256
import json
from pathlib import Path
import time

from observe_open_world_apertures import CORPUS, _window


INPUT = Path("/tmp/seed_open_world_scalar_apertures_blind.json")
OUTPUT = Path("/tmp/seed_open_world_variable_extents_blind.json")


def _canonical(value: object) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode()


def _digest(value: object) -> str:
    material = value if isinstance(value, bytes) else _canonical(value)
    return sha256(material).hexdigest()


def _material(source: dict, reference: str) -> str:
    return bytes.fromhex(source["materials"][reference]["utf8_hex"]).decode("utf-8")


def _material_reference(materials: dict[str, dict[str, object]], value: str) -> str:
    encoded = value.encode("utf-8")
    identity = _digest(encoded)
    rendered = {
        "scalar_count": len(value),
        "byte_count": len(encoded),
        "utf8_hex": encoded.hex(),
    }
    if identity in materials and materials[identity] != rendered:
        raise AssertionError("material digest collision")
    materials[identity] = rendered
    return identity


def _node_identity(
    *,
    source: str,
    branch: str,
    left_extension: int,
    right_extension: int,
    ranges: tuple[tuple[int, int, str], ...],
) -> str:
    return _digest(
        {
            "source": source,
            "branch": branch,
            "left_extension": left_extension,
            "right_extension": right_extension,
            "ranges": ranges,
        }
    )


def _expand_branch_exhaustive(
    *,
    source_name: str,
    text: str,
    branch_identity: str,
    initial_ranges: tuple[tuple[int, int, str], ...],
    materials: dict[str, dict[str, object]],
    deadline: float,
) -> tuple[dict[str, dict], tuple[dict, ...], bool]:
    initial_materials = {text[start:end] for start, end, _origin in initial_ranges}
    if len(initial_materials) != 1:
        raise ValueError("one variable-extent branch has no exact initial surface")
    initial_identity = _node_identity(
        source=source_name,
        branch=branch_identity,
        left_extension=0,
        right_extension=0,
        ranges=initial_ranges,
    )
    nodes = {
        initial_identity: {
            "identity": initial_identity,
            "left_extension": 0,
            "right_extension": 0,
            "material": _material_reference(materials, next(iter(initial_materials))),
            "source_scalar_ranges": [
                [start, end, origin] for start, end, origin in initial_ranges
            ],
            "parent_references": [],
            "child_references": [],
        }
    }
    queue = deque((initial_identity,))
    edges = []
    stopped_at_time_boundary = False

    while queue:
        if time.perf_counter() >= deadline:
            stopped_at_time_boundary = True
            break
        parent_identity = queue.popleft()
        parent = nodes[parent_identity]
        parent_ranges = tuple(
            (start, end, origin)
            for start, end, origin in parent["source_scalar_ranges"]
        )
        for direction in ("left", "right"):
            grouped: dict[str, list[tuple[int, int, str]]] = defaultdict(list)
            unavailable = 0
            for start, end, origin in parent_ranges:
                if direction == "left":
                    if start == 0:
                        unavailable += 1
                        continue
                    new_range = (start - 1, end, origin)
                else:
                    if end == len(text):
                        unavailable += 1
                        continue
                    new_range = (start, end + 1, origin)
                grouped[text[new_range[0] : new_range[1]]].append(new_range)

            recurrent_groups = [
                (material, tuple(ranges))
                for material, ranges in sorted(grouped.items())
                if len(ranges) > 1
            ]
            retained_origins = {
                origin
                for _material, ranges in recurrent_groups
                for _start, _end, origin in ranges
            }
            edges.append(
                {
                    "parent_reference": parent_identity,
                    "direction": direction,
                    "incoming_occurrence_count": len(parent_ranges),
                    "boundary_unavailable_count": unavailable,
                    "retained_occurrence_count": len(retained_origins),
                    "lost_occurrence_count": len(parent_ranges) - len(retained_origins),
                    "result_population_count": len(recurrent_groups),
                    "child_references": [],
                }
            )
            edge = edges[-1]
            for material, ranges in recurrent_groups:
                left_extension = parent["left_extension"] + (direction == "left")
                right_extension = parent["right_extension"] + (direction == "right")
                child_identity = _node_identity(
                    source=source_name,
                    branch=branch_identity,
                    left_extension=left_extension,
                    right_extension=right_extension,
                    ranges=ranges,
                )
                edge["child_references"].append(child_identity)
                if child_identity not in nodes:
                    nodes[child_identity] = {
                        "identity": child_identity,
                        "left_extension": left_extension,
                        "right_extension": right_extension,
                        "material": _material_reference(materials, material),
                        "source_scalar_ranges": [
                            [start, end, origin] for start, end, origin in ranges
                        ],
                        "parent_references": [parent_identity],
                        "child_references": [],
                    }
                    queue.append(child_identity)
                elif parent_identity not in nodes[child_identity]["parent_references"]:
                    nodes[child_identity]["parent_references"].append(parent_identity)
                if child_identity not in parent["child_references"]:
                    parent["child_references"].append(child_identity)

    return nodes, tuple(edges), stopped_at_time_boundary


def _common_extension_count(
    text: str,
    ranges: tuple[tuple[int, int, str], ...],
    direction: str,
) -> int:
    count = 0
    while True:
        coordinates = []
        for start, end, _origin in ranges:
            coordinate = start - count - 1 if direction == "left" else end + count
            if coordinate < 0 or coordinate >= len(text):
                return count
            coordinates.append(text[coordinate])
        if len(set(coordinates)) != 1:
            return count
        count += 1


def _expand_branch(
    *,
    source_name: str,
    text: str,
    branch_identity: str,
    initial_ranges: tuple[tuple[int, int, str], ...],
    materials: dict[str, dict[str, object]],
    deadline: float,
) -> tuple[dict[str, dict], tuple[dict, ...], bool]:
    """Preserve maximal recurrent extent families and support-changing edges."""

    initial_materials = {text[start:end] for start, end, _origin in initial_ranges}
    if len(initial_materials) != 1:
        raise ValueError("one variable-extent branch has no exact initial surface")

    queue = deque(((0, 0, initial_ranges),))
    nodes: dict[str, dict] = {}
    edges = []
    queued_states = {
        _node_identity(
            source=source_name,
            branch=branch_identity,
            left_extension=0,
            right_extension=0,
            ranges=initial_ranges,
        )
    }
    state_parents: dict[str, set[str]] = defaultdict(set)
    stopped_at_time_boundary = False

    while queue:
        if time.perf_counter() >= deadline:
            stopped_at_time_boundary = True
            break
        minimum_left, minimum_right, minimum_ranges = queue.popleft()
        family_identity = _node_identity(
            source=source_name,
            branch=branch_identity,
            left_extension=minimum_left,
            right_extension=minimum_right,
            ranges=minimum_ranges,
        )
        parent_references = tuple(sorted(state_parents[family_identity]))
        common_left = _common_extension_count(text, minimum_ranges, "left")
        common_right = _common_extension_count(text, minimum_ranges, "right")
        maximum_left = minimum_left + common_left
        maximum_right = minimum_right + common_right
        maximum_ranges = tuple(
            (start - common_left, end + common_right, origin)
            for start, end, origin in minimum_ranges
        )
        minimum_materials = {
            text[start:end] for start, end, _origin in minimum_ranges
        }
        maximum_materials = {
            text[start:end] for start, end, _origin in maximum_ranges
        }
        if len(minimum_materials) != 1 or len(maximum_materials) != 1:
            raise AssertionError("one extent family does not carry exact material")
        family = {
            "identity": family_identity,
            "left_extension_range": [minimum_left, maximum_left],
            "right_extension_range": [minimum_right, maximum_right],
            "addressed_extent_count": (common_left + 1) * (common_right + 1),
            "minimum_material": _material_reference(
                materials, next(iter(minimum_materials))
            ),
            "maximal_material": _material_reference(
                materials, next(iter(maximum_materials))
            ),
            "minimum_source_scalar_ranges": [
                [start, end, origin] for start, end, origin in minimum_ranges
            ],
            "maximal_source_scalar_ranges": [
                [start, end, origin] for start, end, origin in maximum_ranges
            ],
            "parent_references": list(parent_references),
            "child_references": [],
        }
        nodes[family_identity] = family

        for direction in ("left", "right"):
            grouped: dict[str, list[tuple[int, int, str]]] = defaultdict(list)
            unavailable = 0
            for start, end, origin in maximum_ranges:
                if direction == "left":
                    if start == 0:
                        unavailable += 1
                        continue
                    grouped_range = (start - 1, end, origin)
                    child_range = (start - 1, end - common_right, origin)
                else:
                    if end == len(text):
                        unavailable += 1
                        continue
                    grouped_range = (start, end + 1, origin)
                    child_range = (start + common_left, end + 1, origin)
                grouped[text[grouped_range[0] : grouped_range[1]]].append(child_range)

            recurrent_groups = [
                (material, tuple(ranges))
                for material, ranges in sorted(grouped.items())
                if len(ranges) > 1
            ]
            retained_origins = {
                origin
                for _material, ranges in recurrent_groups
                for _start, _end, origin in ranges
            }
            edge = {
                "parent_reference": family_identity,
                "direction": direction,
                "incoming_occurrence_count": len(maximum_ranges),
                "boundary_unavailable_count": unavailable,
                "retained_occurrence_count": len(retained_origins),
                "lost_occurrence_count": len(maximum_ranges) - len(retained_origins),
                "result_population_count": len(recurrent_groups),
                "child_references": [],
            }
            edges.append(edge)
            for _material, ranges in recurrent_groups:
                child_left = (
                    maximum_left + 1 if direction == "left" else minimum_left
                )
                child_right = (
                    maximum_right + 1 if direction == "right" else minimum_right
                )
                child_state_identity = _node_identity(
                    source=source_name,
                    branch=branch_identity,
                    left_extension=child_left,
                    right_extension=child_right,
                    ranges=ranges,
                )
                edge["child_references"].append(child_state_identity)
                family["child_references"].append(child_state_identity)
                state_parents[child_state_identity].add(family_identity)
                if child_state_identity in queued_states:
                    continue
                queued_states.add(child_state_identity)
                queue.append((child_left, child_right, ranges))

    for identity, node in nodes.items():
        node["parent_references"] = sorted(state_parents[identity])
        node["child_references"] = sorted(set(node["child_references"]))
    return nodes, tuple(edges), stopped_at_time_boundary


def _expanded_family_coordinates(nodes: dict[str, dict]) -> set[tuple]:
    coordinates = set()
    for family in nodes.values():
        minimum_left, maximum_left = family["left_extension_range"]
        minimum_right, maximum_right = family["right_extension_range"]
        minimum_ranges = tuple(
            (start, end, origin)
            for start, end, origin in family["minimum_source_scalar_ranges"]
        )
        for left_extension in range(minimum_left, maximum_left + 1):
            for right_extension in range(minimum_right, maximum_right + 1):
                left_delta = left_extension - minimum_left
                right_delta = right_extension - minimum_right
                ranges = tuple(
                    (start - left_delta, end + right_delta, origin)
                    for start, end, origin in minimum_ranges
                )
                coordinates.add((left_extension, right_extension, ranges))
    return coordinates


def _addressed_extent_population_count(nodes: dict[str, dict]) -> int:
    """Count the exact coordinate union without instantiating every extent."""

    rectangles_by_support: dict[tuple, list[tuple[int, int, int, int]]] = (
        defaultdict(list)
    )
    for family in nodes.values():
        minimum_left, maximum_left = family["left_extension_range"]
        minimum_right, maximum_right = family["right_extension_range"]
        anchors = tuple(
            (start + minimum_left, end - minimum_right, origin)
            for start, end, origin in family["minimum_source_scalar_ranges"]
        )
        rectangles_by_support[anchors].append(
            (minimum_left, maximum_left, minimum_right, maximum_right)
        )

    count = 0
    for rectangles in rectangles_by_support.values():
        left_boundaries = sorted(
            {
                boundary
                for minimum_left, maximum_left, _minimum_right, _maximum_right in rectangles
                for boundary in (minimum_left, maximum_left + 1)
            }
        )
        for left_start, left_stop in zip(left_boundaries, left_boundaries[1:]):
            right_intervals = sorted(
                (minimum_right, maximum_right + 1)
                for minimum_left, maximum_left, minimum_right, maximum_right in rectangles
                if minimum_left <= left_start <= maximum_left
            )
            if not right_intervals:
                continue
            right_count = 0
            current_start, current_stop = right_intervals[0]
            for interval_start, interval_stop in right_intervals[1:]:
                if interval_start > current_stop:
                    right_count += current_stop - current_start
                    current_start, current_stop = interval_start, interval_stop
                else:
                    current_stop = max(current_stop, interval_stop)
            right_count += current_stop - current_start
            count += (left_stop - left_start) * right_count
    return count


def _exhaustive_coordinates(nodes: dict[str, dict]) -> set[tuple]:
    return {
        (
            node["left_extension"],
            node["right_extension"],
            tuple(
                (start, end, origin)
                for start, end, origin in node["source_scalar_ranges"]
            ),
        )
        for node in nodes.values()
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=INPUT)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--time-boundary-seconds", type=float, default=55.0)
    parser.add_argument("--source", action="append", default=[])
    parser.add_argument("--verify-exhaustive", action="store_true")
    arguments = parser.parse_args()

    begun = time.perf_counter()
    deadline = begun + arguments.time_boundary_seconds
    aperture = json.loads(arguments.input.read_text(encoding="utf-8"))
    observed_sources = []
    stopped_at_time_boundary = False

    for source in aperture["sources"]:
        if arguments.source and source["source"] not in arguments.source:
            continue
        source_begun = time.perf_counter()
        exact_bytes, _line_starts = _window(
            CORPUS.parent / source["source"], source["first_line"]
        )
        text = exact_bytes.decode("utf-8")
        if _digest(exact_bytes) != source["material_sha256"]:
            raise ValueError("variable extent source differs from frozen aperture source")
        materials: dict[str, dict[str, object]] = {}
        frames = []
        frame_number = 0
        for deboundaryer in source["deboundaryers"]:
            separator = deboundaryer["separator_scalar"]
            for frame in deboundaryer["recurrent_substitution_frames"]:
                frame_number += 1
                left = _material(source, frame["left_material"])
                right = _material(source, frame["right_material"])
                branch_results = []
                for occupant_position, occupant in enumerate(frame["occupants"]):
                    occupant_material = _material(source, occupant["material"])
                    branch_identity = _digest(
                        {
                            "source": source["source"],
                            "frame": frame_number,
                            "occupant": occupant_position,
                            "material": occupant_material,
                            "ranges": occupant["source_scalar_ranges"],
                        }
                    )
                    initial_ranges = []
                    occupant_ranges = []
                    for start, end in occupant["source_scalar_ranges"]:
                        full_start = start - len(left) - 1
                        full_end = end + 1 + len(right)
                        expected = left + separator + occupant_material + separator + right
                        if text[full_start:full_end] != expected:
                            raise ValueError("frozen frame does not resolve in exact source")
                        occurrence_identity = _digest(
                            {
                                "source": source["source"],
                                "frame": frame_number,
                                "occupant": occupant_position,
                                "source_scalar_range": [start, end],
                            }
                        )
                        initial_ranges.append(
                            (full_start, full_end, occurrence_identity)
                        )
                        occupant_ranges.append((start, end, occurrence_identity))
                    nodes, edges, stopped = _expand_branch(
                        source_name=source["source"],
                        text=text,
                        branch_identity=branch_identity,
                        initial_ranges=tuple(initial_ranges),
                        materials=materials,
                        deadline=deadline,
                    )
                    if arguments.verify_exhaustive:
                        exhaustive_nodes, _exhaustive_edges, exhaustive_stopped = (
                            _expand_branch_exhaustive(
                                source_name=source["source"],
                                text=text,
                                branch_identity=branch_identity,
                                initial_ranges=tuple(initial_ranges),
                                materials={},
                                deadline=deadline,
                            )
                        )
                        if exhaustive_stopped:
                            raise TimeoutError(
                                "exhaustive verification reached the time boundary"
                            )
                        compressed_coordinates = _expanded_family_coordinates(nodes)
                        exhaustive_coordinates = _exhaustive_coordinates(exhaustive_nodes)
                        if _addressed_extent_population_count(nodes) != len(
                            compressed_coordinates
                        ):
                            raise AssertionError(
                                "compressed extent population count differs from its exact union"
                            )
                        if compressed_coordinates != exhaustive_coordinates:
                            missing = exhaustive_coordinates - compressed_coordinates
                            extra = compressed_coordinates - exhaustive_coordinates
                            raise AssertionError(
                                "extent-family coordinates differ from exhaustive enumeration: "
                                f"compressed={len(compressed_coordinates)} "
                                f"exhaustive={len(exhaustive_coordinates)} "
                                f"missing={len(missing)} extra={len(extra)} "
                                f"missing_sample={next(iter(missing), None)!r} "
                                f"extra_sample={next(iter(extra), None)!r}"
                            )
                    stopped_at_time_boundary |= stopped
                    branch_results.append(
                        {
                            "identity": branch_identity,
                            "occupant_material": _material_reference(
                                materials, occupant_material
                            ),
                            "initial_occurrence_count": len(initial_ranges),
                            "occupant_source_scalar_ranges": [
                                [start, end, origin]
                                for start, end, origin in occupant_ranges
                            ],
                            "addressed_extent_population_count": (
                                _addressed_extent_population_count(nodes)
                            ),
                            "nodes": list(nodes.values()),
                            "edges": list(edges),
                        }
                    )
                    if stopped_at_time_boundary:
                        break
                frames.append(
                    {
                        "frame_number": frame_number,
                        "separator_scalar": separator,
                        "left_material": _material_reference(materials, left),
                        "right_material": _material_reference(materials, right),
                        "branches": branch_results,
                    }
                )
                if stopped_at_time_boundary:
                    break
            if stopped_at_time_boundary:
                break
        observed_sources.append(
            {
                "source": source["source"],
                "first_line": source["first_line"],
                "line_count": source["line_count"],
                "material_sha256": source["material_sha256"],
                "materials": materials,
                "frames": frames,
                "wall_seconds": time.perf_counter() - source_begun,
            }
        )
        branch_count = sum(len(frame["branches"]) for frame in frames)
        family_count = sum(
            len(branch["nodes"])
            for frame in frames
            for branch in frame["branches"]
        )
        addressed_extent_count = sum(
            branch["addressed_extent_population_count"]
            for frame in frames
            for branch in frame["branches"]
        )
        print(
            f"{source['source']:48} frames={len(frames):3}  "
            f"branches={branch_count:3}  families={family_count:5}  "
            f"addressed={addressed_extent_count:7}  "
            f"{observed_sources[-1]['wall_seconds']:.3f}s"
        )
        if stopped_at_time_boundary:
            break

    finding = {
        "source_aperture_artifact_sha256": _digest(arguments.input.read_bytes()),
        "operation": (
            "bidirectional one-scalar extension retaining exact recurrent enlarged "
            "surfaces as maximal support-preserving extent families"
        ),
        "sources": [
            {key: value for key, value in source.items() if key != "wall_seconds"}
            for source in observed_sources
        ],
        "known_loss": (
            "time boundary reached with an unvisited extension frontier"
            if stopped_at_time_boundary
            else None
        ),
    }
    encoded = _canonical(finding)
    arguments.output.write_bytes(encoded)
    print(f"\nartifact: {arguments.output}")
    print(f"artifact bytes: {len(encoded)}")
    print(f"findings sha256: {_digest(encoded)}")
    print(f"complete wall seconds: {time.perf_counter() - begun:.3f}")
    print(f"known loss: {finding['known_loss']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
